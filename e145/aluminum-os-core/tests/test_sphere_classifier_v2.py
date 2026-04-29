"""
Pytest verification — sphere_classifier_v2.py
===============================================
Verifies the self-test claim from the 4-Priority Integration Sprint:
  "Classifies 'gene editing CRISPR' -> H06.S05, generates correct
   Pinecone metadata. Passing."

API: KeywordClassifier().classify(text) returns list of dicts with
     keys: address, sphere, house, house_id, score

Run: pytest test_sphere_classifier_v2.py -v
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sphere_classifier_v2 import KeywordClassifier, pinecone_metadata


@pytest.fixture
def classifier():
    """Create a KeywordClassifier instance."""
    return KeywordClassifier()


class TestClassifierStructure:
    """Verify the classifier is properly initialized."""

    def test_classifier_creates(self, classifier):
        """Classifier should instantiate without errors."""
        assert classifier is not None

    def test_classifier_has_classify(self, classifier):
        """Classifier should have a classify method."""
        assert hasattr(classifier, "classify")


class TestCRISPRClassification:
    """Verify the sprint self-test claim for gene editing CRISPR."""

    def test_crispr_classifies_to_health_biology(self, classifier):
        """
        Sprint claim: 'gene editing CRISPR' -> H06.
        H06 is Health & Biology. Verify classification hits H06.
        """
        result = classifier.classify("gene editing CRISPR")
        house_ids = [r["house_id"] for r in result]
        assert "H06" in house_ids, f"Expected H06 in classification, got {house_ids}"

    def test_crispr_generates_pinecone_metadata(self):
        """
        Sprint claim: generates correct Pinecone metadata.
        Verify the pinecone_metadata function produces correct structure.
        """
        result = pinecone_metadata("gene editing CRISPR")
        assert isinstance(result, dict)
        # Should have house and sphere identification
        assert "house_id" in result or "house" in result or "address" in result


class TestDiverseClassifications:
    """Verify classifier handles diverse inputs correctly."""

    def test_technology_input(self, classifier):
        """Technology-related input should classify to H02."""
        result = classifier.classify("artificial intelligence machine learning neural networks")
        house_ids = [r["house_id"] for r in result]
        assert "H02" in house_ids, f"Expected H02 for AI/ML, got {house_ids}"

    def test_economics_input(self, classifier):
        """Economics-related input should classify to H03."""
        result = classifier.classify("macroeconomics monetary policy inflation GDP")
        house_ids = [r["house_id"] for r in result]
        assert "H03" in house_ids, f"Expected H03 for economics, got {house_ids}"

    def test_empty_input_no_crash(self, classifier):
        """Empty input should not crash."""
        result = classifier.classify("")
        assert result is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
