#!/usr/bin/env python3
"""
Ontology Classifier for 144-Sphere Knowledge System
Automatically classifies documents into Houses and Spheres using Gemini AI
"""

import os
import sys
import json
from pathlib import Path
from typing import Dict, Optional, Tuple
from dotenv import load_dotenv
import structlog

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

# Try both local and cloud Gemini
try:
    import google.generativeai as genai
    USE_GENERATIVE_AI = True
except ImportError:
    USE_GENERATIVE_AI = False

try:
    from vertexai.generative_models import GenerativeModel
    import vertexai
    USE_VERTEX_AI = os.getenv("USE_VERTEX_AI", "false").lower() == "true"
except ImportError:
    USE_VERTEX_AI = False

from src.config.ontology import OntologyManager

load_dotenv()
logger = structlog.get_logger()


class OntologyClassifier:
    """
    Classifies documents into the 144-sphere ontology using AI
    """

    def __init__(self, use_vertex: bool = None):
        """
        Initialize classifier

        Args:
            use_vertex: Use Vertex AI if True, generative AI if False, auto-detect if None
        """
        if use_vertex is None:
            use_vertex = USE_VERTEX_AI

        self.use_vertex = use_vertex and USE_VERTEX_AI
        self.model = None

        # Load ontology
        try:
            self.ontology = OntologyManager()
            logger.info("ontology_loaded", houses=len(self.ontology.houses), spheres=len(self.ontology.spheres))
        except Exception as e:
            logger.error("ontology_load_failed", error=str(e))
            self.ontology = None

        # Initialize appropriate model
        if self.use_vertex:
            self._init_vertex_ai()
        elif USE_GENERATIVE_AI:
            self._init_generative_ai()
        else:
            logger.warning("no_gemini_available", message="No Gemini API available")

    def _init_vertex_ai(self):
        """Initialize Vertex AI Gemini"""
        try:
            project_id = os.getenv("GCP_PROJECT_ID")
            region = os.getenv("GCP_REGION", "us-central1")

            vertexai.init(project=project_id, location=region)
            self.model = GenerativeModel("gemini-2.0-flash-exp")
            logger.info("vertex_ai_initialized", project=project_id, region=region)
        except Exception as e:
            logger.error("vertex_ai_init_failed", error=str(e))
            self.use_vertex = False

    def _init_generative_ai(self):
        """Initialize Google Generative AI (local API)"""
        try:
            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                logger.warning("no_gemini_key", message="GEMINI_API_KEY not set")
                return

            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-2.0-flash-exp")
            logger.info("generative_ai_initialized")
        except Exception as e:
            logger.error("generative_ai_init_failed", error=str(e))

    def _build_ontology_prompt(self) -> str:
        """Build a structured prompt describing the 144-sphere ontology"""
        if not self.ontology:
            return "No ontology available"

        prompt = "# 144-Sphere Knowledge Ontology\n\n"
        prompt += "The knowledge system is organized into 12 Houses, each containing 12 Spheres (144 total):\n\n"

        for house in self.ontology.houses:
            prompt += f"## House {house.index + 1}: {house.name}\n"
            prompt += "Spheres:\n"
            for sphere in house.spheres:
                prompt += f"  {sphere.index}. {sphere.name}\n"
            prompt += "\n"

        return prompt

    def classify_conversation(
        self,
        title: str,
        content_sample: str,
        max_sample_length: int = 2000
    ) -> Tuple[str, str, float]:
        """
        Classify a conversation into House and Sphere

        Args:
            title: Conversation title
            content_sample: Sample of conversation content (will be truncated)
            max_sample_length: Maximum length of content to analyze

        Returns:
            Tuple of (house_name, sphere_name, confidence_score)
        """
        if not self.model or not self.ontology:
            logger.warning("classifier_not_initialized", message="Using fallback classification")
            return self._fallback_classification(title, content_sample)

        # Truncate content if too long
        if len(content_sample) > max_sample_length:
            content_sample = content_sample[:max_sample_length] + "..."

        # Build classification prompt
        ontology_desc = self._build_ontology_prompt()

        classification_prompt = f"""{ontology_desc}

# Classification Task

Analyze the following conversation and classify it into the most appropriate House and Sphere from the ontology above.

**Conversation Title:** {title}

**Conversation Content (sample):**
{content_sample}

**Instructions:**
1. Read the conversation carefully
2. Identify the primary domain/topic
3. Select the SINGLE most relevant House
4. Select the SINGLE most relevant Sphere within that House
5. Provide a confidence score (0.0-1.0)

**Respond with ONLY a JSON object in this exact format:**
{{
    "house": "exact house name from ontology",
    "sphere": "exact sphere name from ontology",
    "confidence": 0.85,
    "reasoning": "brief explanation of why this classification was chosen"
}}

IMPORTANT: Return ONLY the JSON, no other text."""

        try:
            # Generate classification
            if self.use_vertex:
                response = self.model.generate_content(classification_prompt)
                response_text = response.text
            else:
                response = self.model.generate_content(classification_prompt)
                response_text = response.text

            # Parse JSON response
            # Clean up response (remove markdown code blocks if present)
            response_text = response_text.strip()
            if response_text.startswith("```json"):
                response_text = response_text[7:]
            if response_text.startswith("```"):
                response_text = response_text[3:]
            if response_text.endswith("```"):
                response_text = response_text[:-3]
            response_text = response_text.strip()

            result = json.loads(response_text)

            house_name = result.get("house", "")
            sphere_name = result.get("sphere", "")
            confidence = float(result.get("confidence", 0.5))
            reasoning = result.get("reasoning", "")

            # Validate house exists in ontology
            house = self.ontology.get_house(house_name)
            if not house:
                logger.warning("invalid_house", house=house_name, falling_back=True)
                return self._fallback_classification(title, content_sample)

            # Validate sphere exists in house
            sphere = house.get_sphere_by_name(sphere_name)
            if not sphere:
                logger.warning("invalid_sphere", house=house_name, sphere=sphere_name, falling_back=True)
                # Use first sphere in house as fallback
                sphere = house.spheres[0] if house.spheres else None
                if not sphere:
                    return self._fallback_classification(title, content_sample)

            logger.info(
                "conversation_classified",
                title=title[:50],
                house=house.name,
                sphere=sphere.name,
                confidence=confidence,
                reasoning=reasoning[:100] if reasoning else ""
            )

            return house.name, sphere.name, confidence

        except Exception as e:
            logger.error("classification_failed", error=str(e), title=title[:50])
            return self._fallback_classification(title, content_sample)

    def _fallback_classification(self, title: str, content: str) -> Tuple[str, str, float]:
        """
        Simple keyword-based fallback classification when AI is unavailable

        Returns: (house, sphere, confidence)
        """
        if not self.ontology:
            # Ultimate fallback when even ontology isn't loaded
            return "Formal Sciences", "Computer Science", 0.3

        # Simple keyword matching
        text = (title + " " + content).lower()

        # Define keyword patterns for common topics (house_name, sphere_name, keywords)
        patterns = [
            ("Formal Sciences", "Computer Science", [
                "code", "programming", "software", "algorithm", "python", "javascript",
                "api", "database", "cloud", "gcp", "vertex", "ai model", "rag", "vector"
            ]),
            ("Formal Sciences", "Mathematics", [
                "math", "equation", "calculus", "algebra", "geometry", "statistics", "probability"
            ]),
            ("Natural Sciences", "Physics", [
                "physics", "quantum", "energy", "force", "motion", "relativity", "particle"
            ]),
            ("Applied Sciences", "Engineering", [
                "engineering", "design", "build", "construction", "mechanical", "electrical"
            ]),
            ("Social Sciences", "Psychology", [
                "psychology", "behavior", "mental", "cognitive", "emotion", "therapy"
            ]),
            ("Humanities", "Philosophy", [
                "philosophy", "ethics", "morality", "existence", "metaphysics", "epistemology"
            ]),
            ("Humanities", "Literature", [
                "literature", "novel", "poetry", "writing", "author", "book", "story"
            ]),
            ("Social Sciences", "Economics", [
                "economics", "market", "finance", "trade", "monetary", "fiscal", "gdp"
            ]),
            ("Applied Sciences", "Medicine", [
                "medicine", "health", "disease", "treatment", "doctor", "patient", "clinical"
            ]),
            ("Natural Sciences", "Biology", [
                "biology", "cell", "organism", "evolution", "genetics", "dna", "species"
            ]),
        ]

        # Score each pattern
        best_match = None
        best_score = 0

        for house_name, sphere_name, keywords in patterns:
            score = sum(1 for kw in keywords if kw in text)
            if score > best_score:
                # Validate this house/sphere exists in ontology
                house = self.ontology.get_house(house_name)
                if house:
                    sphere = house.get_sphere_by_name(sphere_name)
                    if sphere:
                        best_score = score
                        best_match = (house.name, sphere.name)

        if best_match:
            confidence = min(0.7, best_score / 10)  # Max 0.7 confidence for keyword matching
            logger.info("fallback_classification", house=best_match[0], sphere=best_match[1], confidence=confidence)
            return best_match[0], best_match[1], confidence

        # Ultimate fallback - use first house and first sphere
        logger.warning("using_default_classification")
        first_house = self.ontology.houses[0]
        first_sphere = first_house.spheres[0]
        return first_house.name, first_sphere.name, 0.3


def classify_document(title: str, content: str, use_vertex: bool = None) -> Dict[str, any]:
    """
    Convenience function to classify a single document

    Args:
        title: Document title
        content: Document content
        use_vertex: Use Vertex AI if True, otherwise use generative AI

    Returns:
        Dictionary with classification results
    """
    classifier = OntologyClassifier(use_vertex=use_vertex)
    house, sphere, confidence = classifier.classify_conversation(title, content)

    return {
        "house": house,
        "sphere": sphere,
        "confidence": confidence
    }


if __name__ == "__main__":
    # Test the classifier
    print("Testing Ontology Classifier\n")

    test_conversations = [
        {
            "title": "Building a RAG system with Python",
            "content": "I'm working on a retrieval-augmented generation system using LangChain and Qdrant..."
        },
        {
            "title": "Understanding quantum mechanics",
            "content": "Let's discuss the double-slit experiment and wave-particle duality..."
        },
        {
            "title": "Ancient Greek philosophy",
            "content": "Socrates, Plato, and Aristotle formed the foundation of Western philosophy..."
        }
    ]

    classifier = OntologyClassifier()

    for conv in test_conversations:
        house, sphere, conf = classifier.classify_conversation(conv["title"], conv["content"])
        print(f"Title: {conv['title']}")
        print(f"  → House: {house}")
        print(f"  → Sphere: {sphere}")
        print(f"  → Confidence: {conf:.2f}")
        print()
