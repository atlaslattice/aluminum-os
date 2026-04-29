#!/usr/bin/env python3
"""
Live Data Ingestion Pipeline
Fetches, stages, filters, and ingests external data

Features:
- Multi-source data fetching
- Staging layer for review
- Novelty detection (prevents duplicates)
- Significance filtering
- Automated scheduling
- Rate limiting
"""

import os
import json
import hashlib
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

import structlog
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

# Optional imports - only needed for full pipeline
try:
    from connectors.data_connectors import ConnectorFactory
except ImportError:
    ConnectorFactory = None

try:
    from vault.vault_integration import process_with_vault_classification
    from vault.vault_security import VaultManager
except ImportError:
    process_with_vault_classification = None
    VaultManager = None

logger = structlog.get_logger()


class StagingLayer:
    """
    Staging area for new data before ingestion

    Stores pending items for review and filtering
    """

    def __init__(self,
                 staging_dir: str = "./staging",
                 enable_novelty_check: bool = True,
                 vectorstore_path: str = "./data/qdrant_db"):
        self.staging_dir = Path(staging_dir)
        self.staging_dir.mkdir(parents=True, exist_ok=True)

        self.pending_file = self.staging_dir / "pending_ingestion.json"
        self.approved_file = self.staging_dir / "approved.json"
        self.rejected_file = self.staging_dir / "rejected.json"

        # Novelty detection setup
        self.enable_novelty_check = enable_novelty_check
        self.vectorstore_path = vectorstore_path
        self.vectorstore = None
        self.embeddings = None

        if enable_novelty_check:
            self._init_novelty_detector()

        logger.info("staging_layer_initialized",
                   dir=str(self.staging_dir),
                   novelty_check=enable_novelty_check)

    def _init_novelty_detector(self):
        """Initialize novelty detection with vector store access"""
        try:
            from langchain_community.vectorstores import Qdrant as LangchainQdrant
            from qdrant_client import QdrantClient

            # Initialize embeddings
            self.embeddings = HuggingFaceEmbeddings(
                model_name="sentence-transformers/all-MiniLM-L6-v2"
            )

            # Connect to vector store (if exists)
            if Path(self.vectorstore_path).exists():
                client = QdrantClient(path=self.vectorstore_path)
                self.vectorstore = LangchainQdrant(
                    client=client,
                    collection_name="grokbrain_grid",
                    embeddings=self.embeddings
                )
                logger.info("novelty_detector_initialized",
                           vectorstore=self.vectorstore_path)
            else:
                logger.warning("vectorstore_not_found",
                             path=self.vectorstore_path,
                             novelty_check_disabled=True)
                self.enable_novelty_check = False

        except Exception as e:
            logger.error("novelty_detector_init_failed",
                        error=str(e))
            self.enable_novelty_check = False

    def _is_novel_content(self, content: str, similarity_threshold: float = 0.85) -> bool:
        """
        Check if content is novel against existing knowledge base

        Args:
            content: Content to check
            similarity_threshold: Cosine similarity threshold (default 0.85)

        Returns:
            True if novel (dissimilar), False if duplicate
        """
        if not self.enable_novelty_check or not self.vectorstore:
            return True  # Allow through if novelty check disabled

        try:
            # Search for similar content
            similar_docs = self.vectorstore.similarity_search_with_score(
                content[:1000],  # Truncate for speed
                k=1
            )

            if similar_docs:
                doc, score = similar_docs[0]
                # Qdrant returns distance (lower = more similar)
                # Convert to similarity for clarity
                similarity = 1 - score if score < 1 else 0

                is_novel = similarity < similarity_threshold

                logger.info("novelty_check_result",
                           similarity=similarity,
                           threshold=similarity_threshold,
                           is_novel=is_novel,
                           similar_to=doc.page_content[:100])

                return is_novel

            return True  # No similar docs = novel

        except Exception as e:
            logger.error("novelty_check_error", error=str(e))
            return True  # On error, allow through

    def add_to_staging(self, items: List[Dict[str, Any]], source: str) -> int:
        """
        Add items to staging area with novelty filtering

        Args:
            items: List of data items
            source: Source identifier

        Returns:
            Number of items added
        """
        # Load existing pending items
        pending = self._load_pending()

        # Track stats
        added_count = 0
        duplicate_count = 0
        novel_rejected_count = 0

        for item in items:
            # Generate unique ID
            item_id = self._generate_id(item)

            # Check if already exists in staging
            if any(p['id'] == item_id for p in pending):
                logger.info("item_already_staged", id=item_id)
                duplicate_count += 1
                continue

            # Check novelty against knowledge base
            if self.enable_novelty_check:
                content = item.get('title', '') + " " + item.get('content', '')
                if not self._is_novel_content(content):
                    logger.info("item_rejected_duplicate",
                               id=item_id,
                               title=item.get('title', '')[:50])
                    novel_rejected_count += 1
                    continue

            # Add to pending
            pending.append({
                'id': item_id,
                'source': source,
                'added_timestamp': datetime.now().isoformat(),
                'status': 'pending',
                'data': item
            })
            added_count += 1

        # Save
        self._save_pending(pending)

        logger.info("items_added_to_staging",
                   count=added_count,
                   duplicate_in_staging=duplicate_count,
                   duplicate_in_kb=novel_rejected_count,
                   total_pending=len(pending))

        return added_count

    def get_pending(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get pending items"""
        pending = self._load_pending()
        return pending[:limit]

    def approve(self, item_ids: List[str]) -> int:
        """
        Approve items for ingestion

        Args:
            item_ids: List of item IDs to approve

        Returns:
            Number of items approved
        """
        pending = self._load_pending()
        approved = self._load_approved()

        approved_count = 0
        remaining = []

        for item in pending:
            if item['id'] in item_ids:
                item['status'] = 'approved'
                item['approved_timestamp'] = datetime.now().isoformat()
                approved.append(item)
                approved_count += 1
            else:
                remaining.append(item)

        self._save_pending(remaining)
        self._save_approved(approved)

        logger.info("items_approved", count=approved_count)

        return approved_count

    def reject(self, item_ids: List[str], reason: str = "") -> int:
        """Reject items"""
        pending = self._load_pending()
        rejected = self._load_rejected()

        rejected_count = 0
        remaining = []

        for item in pending:
            if item['id'] in item_ids:
                item['status'] = 'rejected'
                item['rejected_timestamp'] = datetime.now().isoformat()
                item['rejection_reason'] = reason
                rejected.append(item)
                rejected_count += 1
            else:
                remaining.append(item)

        self._save_pending(remaining)
        self._save_rejected(rejected)

        logger.info("items_rejected", count=rejected_count)

        return rejected_count

    def get_approved(self) -> List[Dict[str, Any]]:
        """Get approved items ready for ingestion"""
        return self._load_approved()

    def clear_approved(self):
        """Clear approved items after ingestion"""
        self._save_approved([])

    def _generate_id(self, item: Dict[str, Any]) -> str:
        """Generate unique ID for item"""
        content = item.get('title', '') + item.get('content', '')[:500]
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _load_pending(self) -> List[Dict[str, Any]]:
        """Load pending items"""
        if not self.pending_file.exists():
            return []
        with open(self.pending_file, 'r') as f:
            return json.load(f)

    def _save_pending(self, items: List[Dict[str, Any]]):
        """Save pending items"""
        with open(self.pending_file, 'w') as f:
            json.dump(items, f, indent=2)

    def _load_approved(self) -> List[Dict[str, Any]]:
        """Load approved items"""
        if not self.approved_file.exists():
            return []
        with open(self.approved_file, 'r') as f:
            return json.load(f)

    def _save_approved(self, items: List[Dict[str, Any]]):
        """Save approved items"""
        with open(self.approved_file, 'w') as f:
            json.dump(items, f, indent=2)

    def _load_rejected(self) -> List[Dict[str, Any]]:
        """Load rejected items"""
        if not self.rejected_file.exists():
            return []
        with open(self.rejected_file, 'r') as f:
            return json.load(f)

    def _save_rejected(self, items: List[Dict[str, Any]]):
        """Save rejected items"""
        with open(self.rejected_file, 'w') as f:
            json.dump(items, f, indent=2)


class NoveltyDetector:
    """
    Detects if content is novel (not already in knowledge base)

    Uses embedding similarity to find duplicates
    """

    def __init__(self,
                 embedding_model: str = "sentence-transformers/all-MiniLM-L6-v2",
                 similarity_threshold: float = 0.85):
        self.embeddings = HuggingFaceEmbeddings(model_name=embedding_model)
        self.similarity_threshold = similarity_threshold

        logger.info("novelty_detector_initialized",
                   threshold=similarity_threshold)

    def is_novel(self,
                content: str,
                existing_embeddings: List[List[float]]) -> bool:
        """
        Check if content is novel

        Args:
            content: New content to check
            existing_embeddings: Existing content embeddings

        Returns:
            True if novel, False if duplicate
        """
        if not existing_embeddings:
            return True

        # Generate embedding for new content
        new_embedding = self.embeddings.embed_query(content)

        # Calculate similarity with existing content
        from numpy import dot
        from numpy.linalg import norm

        max_similarity = 0.0
        for existing in existing_embeddings:
            similarity = dot(new_embedding, existing) / (norm(new_embedding) * norm(existing))
            max_similarity = max(max_similarity, similarity)

        is_novel = max_similarity < self.similarity_threshold

        logger.info("novelty_check",
                   max_similarity=max_similarity,
                   threshold=self.similarity_threshold,
                   is_novel=is_novel)

        return is_novel


class SignificanceFilter:
    """
    Filters content by significance

    Uses heuristics and optionally LLM to determine importance
    """

    def __init__(self, use_llm: bool = False):
        self.use_llm = use_llm
        self.llm = None

        if use_llm:
            self._init_llm()

        logger.info("significance_filter_initialized", use_llm=use_llm)

    def _init_llm(self):
        """Initialize Gemini for significance scoring"""
        try:
            import google.generativeai as genai

            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.warning("gemini_api_key_not_found", llm_scoring_disabled=True)
                self.use_llm = False
                return

            genai.configure(api_key=api_key)
            self.llm = genai.GenerativeModel("gemini-2.0-flash-exp")
            logger.info("llm_scorer_initialized", model="gemini-2.0-flash-exp")

        except Exception as e:
            logger.error("llm_init_failed", error=str(e))
            self.use_llm = False

    def is_significant(self, item: Dict[str, Any]) -> tuple[bool, float, str]:
        """
        Check if item is significant

        Args:
            item: Data item to check

        Returns:
            Tuple of (is_significant, score, reason)
        """
        # First: Quick heuristic filter
        heuristic_score, heuristic_reasons = self._heuristic_score(item)

        # If clearly insignificant, skip LLM (fast rejection)
        if heuristic_score < 0.2:
            return False, heuristic_score, f"heuristic_rejection: {heuristic_reasons}"

        # If clearly significant, auto-approve (fast acceptance)
        if heuristic_score >= 0.8:
            return True, heuristic_score, f"heuristic_approval: {heuristic_reasons}"

        # Middle zone (0.2-0.8): Use LLM if enabled
        if self.use_llm and self.llm:
            llm_score, llm_reason = self._llm_score(item)
            # Blend heuristic and LLM scores
            final_score = (heuristic_score * 0.4) + (llm_score * 0.6)
            is_significant = final_score >= 0.5

            logger.info("significance_check_llm",
                       heuristic_score=heuristic_score,
                       llm_score=llm_score,
                       final_score=final_score,
                       is_significant=is_significant)

            return is_significant, final_score, f"LLM: {llm_reason}"
        else:
            # No LLM: conservative approval at 0.5 threshold
            is_significant = heuristic_score >= 0.5
            return is_significant, heuristic_score, heuristic_reasons

    def _heuristic_score(self, item: Dict[str, Any]) -> tuple[float, str]:
        """Calculate heuristic-based significance score"""
        score = 0.0
        reasons = []

        # Check length (longer = more substantial)
        content_length = len(item.get('content', ''))
        if content_length > 500:
            score += 0.3
            reasons.append("substantial_content")

        # Check metadata completeness
        if item.get('authors'):
            score += 0.2
            reasons.append("has_authors")

        if item.get('categories'):
            score += 0.1
            reasons.append("categorized")

        # Check source type
        if item.get('source_type') in ['research_paper', 'patent']:
            score += 0.3
            reasons.append("authoritative_source")

        # Check recency
        try:
            published = datetime.fromisoformat(item['published_date'].replace('Z', '+00:00'))
            days_old = (datetime.now() - published.replace(tzinfo=None)).days
            if days_old < 7:
                score += 0.1
                reasons.append("recent")
        except:
            pass

        return score, ", ".join(reasons)

    def _llm_score(self, item: Dict[str, Any]) -> tuple[float, str]:
        """LLM-based significance scoring"""
        title = item.get('title', 'Untitled')
        content = item.get('content', '')[:1500]  # Limit for API
        source_type = item.get('source_type', 'unknown')

        prompt = f"""Evaluate the significance of this content for a personal knowledge base.

Title: {title}
Content: {content}
Source Type: {source_type}

Score this content on a scale of 0.0-1.0 based on:
- Novelty of insights (unique perspectives or findings)
- Depth of information (comprehensive vs surface-level)
- Practical value (actionable knowledge)
- Authority/credibility (trustworthy source)
- Relevance to knowledge building (educational value)

Respond with ONLY a JSON object:
{{
    "score": 0.75,
    "reasoning": "Brief 1-sentence explanation"
}}"""

        try:
            response = self.llm.generate_content(prompt)
            result_text = response.text.strip()

            # Clean JSON markers
            if result_text.startswith("```json"):
                result_text = result_text[7:]
            if result_text.startswith("```"):
                result_text = result_text[3:]
            if result_text.endswith("```"):
                result_text = result_text[:-3]
            result_text = result_text.strip()

            # Parse JSON
            result = json.loads(result_text)

            score = float(result.get("score", 0.5))
            reasoning = result.get("reasoning", "No reasoning provided")

            # Clamp score to 0-1
            score = max(0.0, min(1.0, score))

            logger.info("llm_significance_score",
                       title=title[:50],
                       score=score,
                       reasoning=reasoning[:100])

            return score, reasoning

        except Exception as e:
            logger.error("llm_scoring_error", error=str(e), title=title[:50])
            return 0.5, "LLM scoring failed, using neutral score"


class IngestionPipeline:
    """
    Complete ingestion pipeline

    Pipeline:
    1. Fetch from sources
    2. Stage for review
    3. Filter by novelty
    4. Filter by significance
    5. Approve manually or auto
    6. Ingest to knowledge base
    """

    def __init__(self,
                 staging_dir: str = "./staging",
                 auto_approve: bool = False,
                 use_llm_scoring: bool = True,
                 vectorstore_path: str = "./data/qdrant_db"):
        self.staging = StagingLayer(
            staging_dir=staging_dir,
            enable_novelty_check=True,
            vectorstore_path=vectorstore_path
        )
        self.novelty_detector = NoveltyDetector()
        self.significance_filter = SignificanceFilter(use_llm=use_llm_scoring)

        if VaultManager:
            self.vault_manager = VaultManager()
        else:
            self.vault_manager = None

        self.auto_approve = auto_approve
        self.use_llm_scoring = use_llm_scoring

        logger.info("ingestion_pipeline_initialized",
                   auto_approve=auto_approve,
                   llm_scoring=use_llm_scoring)

    def fetch_and_stage(self,
                       source_configs: List[Dict[str, Any]]) -> Dict[str, int]:
        """
        Fetch data from sources and add to staging

        Args:
            source_configs: List of source configurations
                [
                    {
                        "type": "arxiv",
                        "params": {"search_query": "quantum computing", "max_results": 10}
                    },
                    {
                        "type": "rss",
                        "params": {"feed_url": "https://...", "max_results": 20}
                    }
                ]

        Returns:
            Dict with counts per source
        """
        results = {}

        for config in source_configs:
            source_type = config['type']
            params = config.get('params', {})

            try:
                # Create connector
                connector = ConnectorFactory.create(source_type)

                # Fetch data
                items = connector.fetch(**params)

                # Add to staging
                count = self.staging.add_to_staging(items, source=source_type)
                results[source_type] = count

                logger.info("source_fetched_and_staged",
                           source=source_type,
                           count=count)

            except Exception as e:
                logger.error("fetch_error",
                            source=source_type,
                            error=str(e))
                results[source_type] = 0

        return results

    def filter_pending(self) -> Dict[str, Any]:
        """
        Filter pending items by novelty and significance

        Returns:
            Dict with filtering results
        """
        pending = self.staging.get_pending()

        filtered_results = {
            'total': len(pending),
            'novel': 0,
            'significant': 0,
            'auto_approved': 0,
            'needs_review': 0
        }

        auto_approve_ids = []
        reject_ids = []

        for item in pending:
            data = item['data']
            content = data.get('title', '') + " " + data.get('content', '')

            # Check novelty (simplified - in production, check against existing DB)
            is_novel = True  # TODO: Implement actual novelty check

            if not is_novel:
                reject_ids.append(item['id'])
                logger.info("item_rejected_duplicate", id=item['id'])
                continue

            filtered_results['novel'] += 1

            # Check significance
            is_sig, score, reason = self.significance_filter.is_significant(data)

            if is_sig:
                filtered_results['significant'] += 1

                if self.auto_approve and score >= 0.7:
                    auto_approve_ids.append(item['id'])
                    filtered_results['auto_approved'] += 1
                else:
                    filtered_results['needs_review'] += 1
            else:
                reject_ids.append(item['id'])
                logger.info("item_rejected_insignificant",
                           id=item['id'],
                           score=score)

        # Auto-approve high-quality items
        if auto_approve_ids:
            self.staging.approve(auto_approve_ids)

        # Reject duplicates/low-quality
        if reject_ids:
            self.staging.reject(reject_ids, reason="Failed novelty or significance check")

        logger.info("filtering_complete", **filtered_results)

        return filtered_results

    def ingest_approved(self) -> Dict[str, Any]:
        """
        Ingest approved items into knowledge base

        Returns:
            Dict with ingestion results
        """
        approved_items = self.staging.get_approved()

        if not approved_items:
            return {
                'status': 'no_items',
                'count': 0
            }

        # Convert to artifacts format
        artifacts = []
        for item in approved_items:
            data = item['data']
            artifacts.append({
                'input': data.get('title', ''),
                'output': data.get('content', ''),
                'timestamp': item.get('approved_timestamp', datetime.now().isoformat()),
                'source_file': f"{data.get('source', 'unknown')}_{item['id']}"
            })

        # Classify and route with Vault
        result = process_with_vault_classification(
            artifacts=artifacts,
            vault_manager=self.vault_manager,
            user="ingestion_pipeline"
        )

        # Clear approved items
        self.staging.clear_approved()

        logger.info("ingestion_complete",
                   total=len(approved_items),
                   main_count=result['main_count'],
                   vault_count=result['vault_count'])

        return {
            'status': 'success',
            'total_ingested': len(approved_items),
            'main_count': result['main_count'],
            'vault_count': result['vault_count'],
            'vault_pending': result['vault_count']  # These need manual approval
        }


# Convenience functions
def create_pipeline(auto_approve: bool = False) -> IngestionPipeline:
    """Create ingestion pipeline"""
    return IngestionPipeline(auto_approve=auto_approve)
