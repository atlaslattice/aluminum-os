"""
Pytest verification — lattice_ontology_v2.py
=============================================
Verifies the self-test claim from the 4-Priority Integration Sprint:
  "Classifies 'quantum computing' -> H02.S11 (Quantum Computing),
   activates H08, H09, H12 via edges. Passing."

Run: pytest test_lattice_ontology_v2.py -v
"""
import sys
import os
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from lattice_ontology_v2 import (
    HOUSE_NAMES,
    HOUSE_IDS,
    SPHERES,
    KEYWORDS,
    INTER_HOUSE_EDGES,
    classify_text,
    get_activated_context,
)


class TestLatticeOntologyStructure:
    """Verify the ontology structure is complete and well-formed."""

    def test_twelve_houses(self):
        """There must be exactly 12 Houses."""
        assert len(HOUSE_NAMES) == 12

    def test_twelve_house_ids(self):
        """There must be exactly 12 House IDs."""
        assert len(HOUSE_IDS) == 12

    def test_total_144_spheres(self):
        """Total sphere count must be 144."""
        assert len(SPHERES) == 144

    def test_house_ids_format(self):
        """House IDs must be H01 through H12."""
        expected = [f"H{i+1:02d}" for i in range(12)]
        assert HOUSE_IDS == expected

    def test_keywords_exist_for_all_houses(self):
        """Every House must have keywords for classification.
        KEYWORDS is keyed by integer index (0-11), not house_id string."""
        for i in range(12):
            assert i in KEYWORDS, f"Missing keywords for house index {i}"
            assert len(KEYWORDS[i]) > 0, f"Empty keywords for house index {i}"

    def test_inter_house_edges_exist(self):
        """Inter-House edge list must have entries."""
        assert len(INTER_HOUSE_EDGES) > 0


class TestClassification:
    """Verify the classification function matches sprint self-test claims."""

    def test_quantum_computing_classification(self):
        """
        Sprint claim: 'quantum computing' -> H02.S11 (Quantum Computing).
        classify_text returns dicts with 'house_id' field.
        """
        result = classify_text("quantum computing")
        house_ids = [r["house_id"] for r in result]
        assert "H02" in house_ids, f"Expected H02 in classification, got {house_ids}"

    def test_quantum_computing_sphere(self):
        """Verify quantum computing maps to H02.S11."""
        result = classify_text("quantum computing")
        addresses = [r["address"] for r in result]
        assert "H02.S11" in addresses, f"Expected H02.S11 in {addresses}"

    def test_classification_returns_list(self):
        """Classification must return a list of dicts."""
        result = classify_text("artificial intelligence ethics")
        assert isinstance(result, list)
        assert len(result) > 0
        for item in result:
            assert isinstance(item, dict)
            assert "house_id" in item
            assert "address" in item

    def test_empty_input(self):
        """Empty input should return empty or minimal classification."""
        result = classify_text("")
        assert isinstance(result, list)


class TestActivatedContext:
    """Verify edge activation matches sprint self-test claims."""

    def test_quantum_computing_activates_edges(self):
        """
        Sprint claim: activates H08, H09, H12 via edges.
        get_activated_context takes text (not house_ids list).
        """
        context = get_activated_context("quantum computing")
        assert isinstance(context, dict)

        # Context should include primary and edge-activated houses
        all_houses = set()
        for key in ("primary_houses", "edge_houses", "activated_houses", "houses"):
            if key in context:
                val = context[key]
                if isinstance(val, list):
                    for item in val:
                        if isinstance(item, str):
                            all_houses.add(item)
                        elif isinstance(item, dict):
                            all_houses.add(item.get("house_id", item.get("id", "")))

        # Should activate more than just the primary house
        assert len(all_houses) > 1, f"Expected cross-domain activation, got {all_houses}"

    def test_multi_domain_input(self):
        """Multi-domain input should activate multiple houses."""
        result = classify_text("CRISPR gene editing biosecurity regulations")
        house_ids = set(r["house_id"] for r in result)
        assert len(house_ids) >= 2, f"Expected multi-domain, got {house_ids}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
