#!/usr/bin/env python3
"""
Sphere Classifier v2.0 — Lattice-Aware Classification

Replaces the original sphere_classifier.py (which used grokbrain_v4 ontology)
with a classifier that uses the canonical 12×12+1 lattice ontology.

Two classification modes:
  1. Keyword-based (fast, no dependencies) — uses lattice_ontology_v2.classify_text()
  2. Embedding-based (accurate, requires sentence-transformers) — uses cosine similarity
     against pre-computed sphere description embeddings

The embedding-based classifier generates rich descriptions for each of the 144 spheres
from the KEYWORDS table, then uses HuggingFace sentence-transformers to compute
similarity between input text and sphere descriptions.

Usage:
    # Keyword mode (fast, no ML dependencies)
    from sphere_classifier_v2 import KeywordClassifier
    kc = KeywordClassifier()
    results = kc.classify("quantum computing threatens encryption")

    # Embedding mode (accurate, requires sentence-transformers)
    from sphere_classifier_v2 import EmbeddingClassifier
    ec = EmbeddingClassifier()
    results = ec.classify("quantum computing threatens encryption")

    # Both return:
    # [{"address": "H02.S11", "sphere": "Quantum Tech", "house": "Technology & Engineering",
    #   "score": 0.87, "house_id": "H02"}]

Pinecone Integration:
    When storing vectors in Pinecone, use the metadata schema:
    {
        "text": "...",
        "house": "H02",
        "sphere": "H02.S11",
        "house_name": "Technology & Engineering",
        "sphere_name": "Quantum Tech",
        "timestamp": "2026-04-29T...",
        "source": "manus"
    }
"""

import os
import sys
from typing import List, Dict, Optional, Tuple
import numpy as np

# Import the canonical ontology
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from lattice_ontology_v2 import (
    SPHERES, HOUSE_NAMES, HOUSE_IDS,
    KEYWORDS, INTER_HOUSE_EDGES, ELEMENT_145,
    sphere_index, house_for_sphere, address_for_index,
    classify_text, get_connected_houses, get_activated_context,
)


# ============================================================================
# KEYWORD CLASSIFIER (no ML dependencies)
# ============================================================================

class KeywordClassifier:
    """Fast keyword-based sphere classifier using the 12×12+1 ontology.

    This is a thin wrapper around lattice_ontology_v2.classify_text()
    that provides the same interface as the old SphereClassifier.
    """

    def __init__(self):
        self.num_spheres = 144
        self.ready = True

    def classify(self, text: str, top_k: int = 5) -> List[Dict]:
        """Classify text into lattice spheres using keyword matching.

        Args:
            text: Input text to classify
            top_k: Number of top matches to return

        Returns:
            List of classification results with address, sphere, house, score
        """
        return classify_text(text, top_k=top_k)

    def classify_with_context(self, text: str) -> Dict:
        """Full INGEST + ACTIVATE pipeline.

        Classifies text, then activates connected Houses via inter-House edges.

        Args:
            text: Input text to process

        Returns:
            Dict with primary_spheres, activated_houses, edges
        """
        return get_activated_context(text)


# ============================================================================
# EMBEDDING CLASSIFIER (requires sentence-transformers)
# ============================================================================

class EmbeddingClassifier:
    """Embedding-based sphere classifier using sentence-transformers.

    Generates rich descriptions for each of the 144 spheres from the
    KEYWORDS table, then uses cosine similarity to match input text.

    This replaces the original sphere_classifier.py's HuggingFace approach
    but uses the new 12×12+1 ontology instead of grokbrain_v4 categories.
    """

    def __init__(self, model_name: str = "sentence-transformers/all-MiniLM-L6-v2"):
        """Initialize with a sentence-transformer model.

        Args:
            model_name: HuggingFace model name for embeddings
        """
        try:
            from sentence_transformers import SentenceTransformer
            print(f"Loading embedding model: {model_name}")
            self.model = SentenceTransformer(model_name)
            self.ready = True
        except ImportError:
            print("WARNING: sentence-transformers not installed. "
                  "Install with: pip install sentence-transformers")
            print("Falling back to keyword classifier.")
            self.model = None
            self.ready = False

        self.num_spheres = 144
        self.sphere_descriptions = self._generate_descriptions()

        if self.ready:
            print("Computing sphere embeddings...")
            self.sphere_embeddings = self.model.encode(
                self.sphere_descriptions, show_progress_bar=True
            )
            print(f"Sphere embeddings shape: {self.sphere_embeddings.shape}")

    def _generate_descriptions(self) -> List[str]:
        """Generate rich text descriptions for each of the 144 spheres."""
        descriptions = []
        for idx in range(144):
            house_idx, house_name = house_for_sphere(idx)
            sphere_name = SPHERES[idx]
            keywords = KEYWORDS.get(idx, [])
            address = address_for_index(idx)

            desc = (
                f"{sphere_name} is a domain within {house_name}. "
                f"It covers topics including {', '.join(keywords[:5])}. "
                f"Lattice address: {address}."
            )
            descriptions.append(desc)
        return descriptions

    def classify(self, text: str, top_k: int = 5) -> List[Dict]:
        """Classify text using embedding similarity.

        Args:
            text: Input text to classify
            top_k: Number of top matches to return

        Returns:
            List of classification results with address, sphere, house, score
        """
        if not self.ready:
            # Fallback to keyword classifier
            return classify_text(text, top_k=top_k)

        # Encode input
        text_embedding = self.model.encode([text])[0]

        # Compute cosine similarity against all sphere embeddings
        similarities = np.dot(self.sphere_embeddings, text_embedding) / (
            np.linalg.norm(self.sphere_embeddings, axis=1) * np.linalg.norm(text_embedding)
        )

        # Get top-k indices
        top_indices = np.argsort(similarities)[-top_k:][::-1]

        results = []
        for idx in top_indices:
            idx = int(idx)
            house_idx, house_name = house_for_sphere(idx)
            results.append({
                "address": address_for_index(idx),
                "sphere": SPHERES[idx],
                "house": house_name,
                "house_id": HOUSE_IDS[house_idx],
                "score": round(float(similarities[idx]), 4),
            })

        return results

    def classify_with_context(self, text: str) -> Dict:
        """Full INGEST + ACTIVATE pipeline using embeddings.

        Classifies text with embeddings, then activates connected Houses.
        """
        primary = self.classify(text, top_k=5)
        if not primary:
            return {"primary_spheres": [], "activated_houses": [], "edges": []}

        primary_houses = list(set(s["house_id"] for s in primary))
        activated = set(primary_houses)
        all_edges = []

        for house_id in primary_houses:
            connections = get_connected_houses(house_id)
            for conn in connections:
                if conn["strength"] >= 0.6:
                    activated.add(conn["house"])
                    all_edges.append({
                        "from": house_id,
                        "to": conn["house"],
                        "type": conn["type"],
                        "strength": conn["strength"],
                    })

        return {
            "primary_spheres": primary,
            "activated_houses": sorted(list(activated)),
            "edges": all_edges,
        }


# ============================================================================
# PINECONE METADATA SCHEMA
# ============================================================================

def pinecone_metadata(text: str, source: str = "manus",
                      classifier: Optional[KeywordClassifier] = None) -> Dict:
    """Generate Pinecone-compatible metadata with lattice tagging.

    This function classifies text and returns metadata suitable for
    Pinecone vector storage, including House and Sphere tags.

    Args:
        text: The text being stored
        source: Source identifier
        classifier: Optional classifier instance (creates one if not provided)

    Returns:
        Dict with text, house, sphere, house_name, sphere_name, timestamp, source
    """
    from datetime import datetime

    if classifier is None:
        classifier = KeywordClassifier()

    results = classifier.classify(text, top_k=1)

    if results:
        top = results[0]
        return {
            "text": text,
            "house": top["house_id"],
            "sphere": top["address"],
            "house_name": top["house"],
            "sphere_name": top["sphere"],
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
        }
    else:
        return {
            "text": text,
            "house": "E145",
            "sphere": "E145",
            "house_name": "Admin Sphere",
            "sphere_name": "Unclassified",
            "timestamp": datetime.utcnow().isoformat(),
            "source": source,
        }


# ============================================================================
# MIGRATION UTILITY — Reclassify existing Pinecone vectors
# ============================================================================

def migrate_pinecone_vectors(index, namespace: str = "baseline",
                             batch_size: int = 100, dry_run: bool = True):
    """Reclassify existing Pinecone vectors from old ontology to 12×12+1.

    This is a one-time migration script. It reads all vectors from the
    specified namespace, reclassifies them using the new ontology, and
    updates their metadata.

    Args:
        index: Pinecone Index object
        namespace: Pinecone namespace to migrate
        batch_size: Number of vectors to process per batch
        dry_run: If True, only print changes without applying them

    Returns:
        Dict with migration statistics
    """
    classifier = KeywordClassifier()
    stats = {"total": 0, "reclassified": 0, "unchanged": 0, "errors": 0}

    print(f"{'DRY RUN: ' if dry_run else ''}Migrating vectors in namespace '{namespace}'")

    # Fetch all vector IDs (Pinecone doesn't support full scan easily,
    # so this is a placeholder for the actual implementation)
    try:
        # List vectors (requires Pinecone v3+ API)
        results = index.query(
            vector=[0.0] * 768,  # Dummy vector for listing
            top_k=10000,
            include_metadata=True,
            namespace=namespace,
        )

        for match in results.matches:
            stats["total"] += 1
            text = match.metadata.get("text", "")
            if not text:
                stats["errors"] += 1
                continue

            # Reclassify
            new_meta = pinecone_metadata(text, source=match.metadata.get("source", "migrated"))

            # Check if classification changed
            old_sphere = match.metadata.get("sphere", "")
            if old_sphere != new_meta["sphere"]:
                stats["reclassified"] += 1
                if not dry_run:
                    # Update metadata
                    index.upsert(
                        vectors=[(match.id, match.values, {**match.metadata, **new_meta})],
                        namespace=namespace,
                    )
                print(f"  {match.id}: {old_sphere} → {new_meta['sphere']} ({new_meta['sphere_name']})")
            else:
                stats["unchanged"] += 1

    except Exception as e:
        print(f"Migration error: {e}")
        stats["errors"] += 1

    print(f"\nMigration {'preview' if dry_run else 'complete'}: {stats}")
    return stats


# ============================================================================
# SELF-TEST
# ============================================================================

if __name__ == "__main__":
    print("=== Sphere Classifier v2.0 Self-Test ===\n")

    # Test keyword classifier
    kc = KeywordClassifier()
    print("--- Keyword Classifier ---")
    tests = [
        "quantum computing and error correction algorithms",
        "climate change policy and carbon pricing mechanisms",
        "CRISPR gene editing for treating genetic disorders",
        "cybersecurity threat detection using machine learning",
        "Kantian deontological ethics and moral philosophy",
        "UN peacekeeping operations in conflict zones",
        "GDP growth and inflation targeting by central banks",
    ]

    for text in tests:
        results = kc.classify(text, top_k=3)
        print(f"\n'{text[:60]}...'")
        for r in results:
            print(f"  {r['address']} {r['sphere']} ({r['house']}) score={r['score']}")

    # Test context activation
    print("\n--- Context Activation ---")
    ctx = kc.classify_with_context("quantum computing threatens encryption standards for banking")
    print(f"Primary: {[s['address'] for s in ctx['primary_spheres']]}")
    print(f"Activated houses: {ctx['activated_houses']}")
    print(f"Edges: {len(ctx['edges'])}")

    # Test Pinecone metadata generation
    print("\n--- Pinecone Metadata ---")
    meta = pinecone_metadata("The Federal Reserve raised interest rates to combat inflation")
    for k, v in meta.items():
        if k != "text":
            print(f"  {k}: {v}")
