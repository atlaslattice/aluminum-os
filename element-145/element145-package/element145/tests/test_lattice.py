"""
Test Suite — Lattice Loading, LCP Operations, and Ontology Integrity
======================================================================
Tests for core lattice functionality:
  - YAML loading and validation
  - Sphere keyword search
  - INGEST / ACTIVATE / ROUTE / SYNTHESIZE pipeline
  - Element 145 blind spot detection
  - Inter-House connection topology

Run: pytest tests/test_lattice.py -v
Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""

from __future__ import annotations
import os
import sys
import pytest

# ═══════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════

ONTOLOGY_PATH = os.path.join(
    os.path.dirname(os.path.dirname(__file__)), "lattice_ontology.yaml"
)


@pytest.fixture(scope="module")
def lattice():
    """Load the lattice once for all tests in this module."""
    from element145.core.lattice import Lattice
    return Lattice.load(ONTOLOGY_PATH)


@pytest.fixture(scope="module")
def engine():
    """Create an LCP engine for pipeline tests."""
    from element145.core.lcp import create_engine
    return create_engine(ONTOLOGY_PATH)


# ═══════════════════════════════════════════════════════════════
# LATTICE STRUCTURE TESTS
# ═══════════════════════════════════════════════════════════════

class TestLatticeStructure:
    """Tests for lattice structural integrity."""

    def test_canonical_n(self, lattice):
        """N must be exactly 145 (12×12 + 1 Admin Sphere)."""
        assert lattice.N == 145, f"Expected N=145, got N={lattice.N}"

    def test_twelve_houses(self, lattice):
        """Must have exactly 12 Houses."""
        assert lattice.num_houses == 12, f"Expected 12 Houses, got {lattice.num_houses}"

    def test_144_spheres(self, lattice):
        """Must have exactly 144 Spheres (12 per House)."""
        assert lattice.num_spheres == 144, f"Expected 144 Spheres, got {lattice.num_spheres}"

    def test_12_spheres_per_house(self, lattice):
        """Each House must contain exactly 12 Spheres."""
        for house_id in lattice.house_list():
            spheres = lattice.get_house_spheres(house_id)
            assert len(spheres) == 12, (
                f"House {house_id} has {len(spheres)} Spheres, expected 12"
            )

    def test_element_145_exists(self, lattice):
        """Element 145 (Admin Sphere) must be present."""
        assert lattice.element_145 is not None, "Element 145 is missing"

    def test_element_145_operations(self, lattice):
        """Element 145 must have metasynthesis operations defined."""
        e145 = lattice.element_145
        assert len(e145.operations) > 0, "Element 145 has no operations"
        assert "blind_spot_identification" in e145.operations
        assert "cross_house_cascade_detection" in e145.operations

    def test_house_ids_sequential(self, lattice):
        """House IDs must be H1 through H12."""
        expected = {f"H{i}" for i in range(1, 13)}
        actual = set(lattice.houses.keys())
        assert actual == expected, f"House IDs mismatch: {actual - expected}"

    def test_sphere_ids_sequential(self, lattice):
        """Sphere IDs must be S1 through S144."""
        expected = {f"S{i}" for i in range(1, 145)}
        actual = set(lattice.spheres.keys())
        assert actual == expected, f"Missing Spheres: {expected - actual}"

    def test_connections_exist(self, lattice):
        """Must have inter-House connections defined."""
        assert len(lattice.connections) > 0, "No connections defined"
        assert len(lattice.connections) >= 20, (
            f"Expected ≥20 connections, got {len(lattice.connections)}"
        )

    def test_connection_strengths_valid(self, lattice):
        """All connection strengths must be in [0.0, 1.0]."""
        for conn in lattice.connections:
            assert 0.0 <= conn.strength <= 1.0, (
                f"Invalid strength {conn.strength} for "
                f"{conn.source_house}→{conn.target_house}"
            )

    def test_connections_reference_valid_houses(self, lattice):
        """All connections must reference existing Houses."""
        valid_ids = set(lattice.houses.keys())
        for conn in lattice.connections:
            assert conn.source_house in valid_ids, (
                f"Connection references unknown House: {conn.source_house}"
            )
            assert conn.target_house in valid_ids, (
                f"Connection references unknown House: {conn.target_house}"
            )

    def test_validation_passes(self, lattice):
        """Full lattice validation must pass with no issues."""
        issues = lattice.validate()
        assert len(issues) == 0, f"Validation issues: {issues}"


# ═══════════════════════════════════════════════════════════════
# SPHERE SEARCH TESTS
# ═══════════════════════════════════════════════════════════════

class TestSphereSearch:
    """Tests for keyword-based Sphere search."""

    def test_search_returns_results(self, lattice):
        """Search must return results for common terms."""
        results = lattice.search_spheres("law policy regulation")
        assert len(results) > 0, "Search returned no results for 'law policy regulation'"

    def test_search_governance_keywords(self, lattice):
        """Governance keywords should activate H1 Spheres."""
        results = lattice.search_spheres("constitution law sovereignty")
        house_ids = {sphere.house_id for sphere, _ in results}
        assert "H1" in house_ids, "H1 (Governance) not found for governance keywords"

    def test_search_technology_keywords(self, lattice):
        """Technology keywords should activate H4 Spheres."""
        results = lattice.search_spheres("artificial intelligence computing software")
        house_ids = {sphere.house_id for sphere, _ in results}
        assert "H4" in house_ids, "H4 (Technology) not found for tech keywords"

    def test_search_multi_domain(self, lattice):
        """Multi-domain query should activate multiple Houses."""
        results = lattice.search_spheres(
            "AI regulation climate policy economic impact military defense"
        )
        house_ids = {sphere.house_id for sphere, _ in results}
        assert len(house_ids) >= 3, (
            f"Multi-domain query activated only {len(house_ids)} Houses"
        )

    def test_search_max_results(self, lattice):
        """Search should respect max_results parameter."""
        results = lattice.search_spheres("policy economics science", max_results=5)
        assert len(results) <= 5, f"Got {len(results)} results with max_results=5"

    def test_search_empty_input(self, lattice):
        """Empty input should return no results (not crash)."""
        results = lattice.search_spheres("")
        assert isinstance(results, list)


# ═══════════════════════════════════════════════════════════════
# HOUSE QUERY TESTS
# ═══════════════════════════════════════════════════════════════

class TestHouseQueries:
    """Tests for House lookup and neighbor queries."""

    def test_get_house_by_id(self, lattice):
        """Should retrieve House by ID."""
        house = lattice.get_house("H1")
        assert house is not None
        assert house.id == "H1"
        assert "Governance" in house.name or "governance" in house.name.lower()

    def test_get_nonexistent_house(self, lattice):
        """Should return None for invalid House ID."""
        house = lattice.get_house("H99")
        assert house is None

    def test_house_neighbors(self, lattice):
        """Houses should have neighbors (connected Houses)."""
        neighbors = lattice.get_house_neighbors("H1")
        assert len(neighbors) > 0, "H1 has no neighbors"

    def test_connection_bidirectional(self, lattice):
        """If H1 connects to H2, H2 should connect to H1."""
        for conn in lattice.connections:
            reverse = lattice.get_connection(conn.target_house, conn.source_house)
            # Connection object is same for both directions
            assert reverse is not None, (
                f"Connection {conn.source_house}→{conn.target_house} "
                f"has no reverse lookup"
            )


# ═══════════════════════════════════════════════════════════════
# LCP PIPELINE TESTS
# ═══════════════════════════════════════════════════════════════

class TestLCPPipeline:
    """Tests for the full INGEST → ACTIVATE → ROUTE → SYNTHESIZE pipeline."""

    def test_analyze_returns_result(self, engine):
        """Full pipeline should produce a SynthesisResult."""
        result = engine.analyze("AI regulation and economic impact")
        assert result is not None
        assert hasattr(result, 'activated_houses')
        assert hasattr(result, 'activated_spheres')
        assert hasattr(result, 'blind_spots')
        assert hasattr(result, 'coherence_score')

    def test_analyze_activates_houses(self, engine):
        """Pipeline should activate relevant Houses."""
        result = engine.analyze("cybersecurity threats to financial infrastructure")
        assert len(result.activated_houses) > 0, "No Houses activated"
        assert len(result.activated_spheres) > 0, "No Spheres activated"

    def test_analyze_detects_blind_spots(self, engine):
        """Pipeline should report Houses not activated (blind spots)."""
        result = engine.analyze("quantum computing algorithms")
        # Narrow topic should leave some Houses unactivated
        assert len(result.blind_spots) > 0 or len(result.activated_houses) == 12

    def test_coherence_score_bounded(self, engine):
        """Coherence score must be in [0.0, 1.0]."""
        result = engine.analyze("global trade policy and environmental regulation")
        assert 0.0 <= result.coherence_score <= 1.0, (
            f"Coherence score {result.coherence_score} out of bounds"
        )

    def test_prompt_generation_compact(self, engine):
        """Should generate a compact scaffold prompt."""
        result = engine.analyze("startup feasibility assessment")
        prompt = engine.generate_prompt(result, mode="compact")
        assert isinstance(prompt, str)
        assert len(prompt) > 100, "Compact prompt too short"

    def test_prompt_generation_orchestrator(self, engine):
        """Should generate an orchestrator scaffold prompt."""
        result = engine.analyze("climate migration analysis")
        prompt = engine.generate_prompt(result, mode="orchestrator")
        assert isinstance(prompt, str)
        assert len(prompt) > len(engine.generate_prompt(result, mode="compact")), (
            "Orchestrator prompt should be longer than compact"
        )

    def test_analyze_empty_input(self, engine):
        """Empty input should not crash — should return with blind spots."""
        result = engine.analyze("")
        assert result is not None

    def test_analyze_broad_input(self, engine):
        """Broad input should activate many Houses."""
        result = engine.analyze(
            "global pandemic response involving healthcare, economics, "
            "governance, technology, education, communication, and science"
        )
        assert len(result.activated_houses) >= 5, (
            f"Broad input only activated {len(result.activated_houses)} Houses"
        )


# ═══════════════════════════════════════════════════════════════
# EDGE CASES
# ═══════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Edge case and robustness tests."""

    def test_sphere_is_admin_property(self):
        """Sphere.is_admin should correctly identify Element 145."""
        from element145.core.types import Sphere
        admin = Sphere(id="S145", name="Admin", house_id="", index=144, keywords=())
        assert admin.is_admin

        regular = Sphere(id="S1", name="Regular", house_id="H1", index=0, keywords=())
        assert not regular.is_admin

    def test_connection_involves(self):
        """Connection.involves() should work correctly."""
        from element145.core.types import Connection
        conn = Connection(source_house="H1", target_house="H2",
                         connection_type="regulatory", strength=0.8)
        assert conn.involves("H1")
        assert conn.involves("H2")
        assert not conn.involves("H3")

    def test_connection_other_house(self):
        """Connection.other_house() should return the opposite end."""
        from element145.core.types import Connection
        conn = Connection(source_house="H1", target_house="H2",
                         connection_type="regulatory", strength=0.8)
        assert conn.other_house("H1") == "H2"
        assert conn.other_house("H2") == "H1"
        assert conn.other_house("H3") is None

    def test_frozen_dataclasses(self):
        """Core types should be frozen (immutable)."""
        from element145.core.types import Sphere, House
        sphere = Sphere(id="S1", name="Test", house_id="H1", index=0, keywords=("test",))
        with pytest.raises(AttributeError):
            sphere.name = "Modified"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
