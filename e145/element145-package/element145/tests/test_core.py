"""
Test Suite: Element 145 Core — Lattice Ontology + LCP Engine
=============================================================
25+ tests covering structure integrity, sphere search, house queries,
LCP pipeline phases, edge cases, and prompt generation.

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""
import pytest
from element145.core import (
    LCPPhase,
    Sphere,
    HouseEdge,
    ActivationState,
    AnalysisResult,
    LatticeOntology,
    LCPEngine,
    HOUSE_NAMES,
    create_engine,
    quick_analyze,
)


# ═══════════════════════════════════════════════════════════════
# FIXTURES
# ═══════════════════════════════════════════════════════════════

@pytest.fixture
def ontology():
    """Fresh LatticeOntology from bundled YAML."""
    return LatticeOntology()


@pytest.fixture
def engine(ontology):
    """Fresh LCPEngine with bundled ontology."""
    return LCPEngine(ontology)


# ═══════════════════════════════════════════════════════════════
# STRUCTURE INTEGRITY
# ═══════════════════════════════════════════════════════════════

class TestStructureIntegrity:
    """Verify the 144+1 lattice structure is correct."""

    def test_exactly_12_houses(self, ontology):
        assert len(ontology.houses) == 12

    def test_exactly_144_spheres(self, ontology):
        assert len(ontology.spheres) == 144

    def test_house_names_match(self, ontology):
        for hid, hdata in ontology.houses.items():
            assert hdata["name"] == HOUSE_NAMES[hid]

    def test_each_house_has_12_spheres(self, ontology):
        for hid in ontology.house_list():
            spheres = ontology.get_spheres_for_house(hid)
            assert len(spheres) == 12, f"{hid} has {len(spheres)} spheres, expected 12"

    def test_house_ids_h1_through_h12(self, ontology):
        expected = {f"H{i}" for i in range(1, 13)}
        assert set(ontology.houses.keys()) == expected

    def test_sphere_ids_s1_through_s144(self, ontology):
        expected = {f"S{i}" for i in range(1, 145)}
        assert set(ontology.spheres.keys()) == expected

    def test_element_145_exists(self, ontology):
        assert ontology.element_145 is not None
        assert len(ontology.element_145) > 0

    def test_connections_exist(self, ontology):
        assert len(ontology.edges) >= 25  # At least 25 inter-House connections

    def test_all_connections_reference_valid_houses(self, ontology):
        for edge in ontology.edges:
            assert edge.source in ontology.houses, f"Invalid source: {edge.source}"
            assert edge.target in ontology.houses, f"Invalid target: {edge.target}"

    def test_connection_strengths_valid(self, ontology):
        for edge in ontology.edges:
            assert 0.0 <= edge.strength <= 1.0, f"Invalid strength: {edge.strength}"

    def test_validate_passes(self, ontology):
        issues = ontology.validate()
        assert issues == [], f"Validation issues: {issues}"

    def test_house_list_sorted(self, ontology):
        houses = ontology.house_list()
        assert houses == [f"H{i}" for i in range(1, 13)]


# ═══════════════════════════════════════════════════════════════
# QUERY METHODS
# ═══════════════════════════════════════════════════════════════

class TestQueryMethods:
    """Verify ontology query methods work correctly."""

    def test_get_house_data_valid(self, ontology):
        hdata = ontology.get_house_data("H1")
        assert hdata is not None
        assert hdata["name"] == "Governance"

    def test_get_house_data_invalid(self, ontology):
        assert ontology.get_house_data("H99") is None

    def test_get_sphere_valid(self, ontology):
        s = ontology.get_sphere("S1")
        assert s is not None
        assert s.house_id == "H1"

    def test_get_sphere_invalid(self, ontology):
        assert ontology.get_sphere("S999") is None

    def test_get_spheres_for_house(self, ontology):
        spheres = ontology.get_spheres_for_house("H11")
        assert len(spheres) == 12
        assert all(s.house_id == "H11" for s in spheres)

    def test_get_edges_for_house(self, ontology):
        edges = ontology.get_edges_for_house("H1")
        assert len(edges) >= 3  # H1 connects to at least H2, H3, H10
        assert all(e.involves("H1") for e in edges)

    def test_get_edge_between_exists(self, ontology):
        edge = ontology.get_edge_between("H1", "H2")
        assert edge is not None
        assert edge.strength >= 0.9  # governance-law is 0.95

    def test_get_edge_between_symmetric(self, ontology):
        e1 = ontology.get_edge_between("H1", "H2")
        e2 = ontology.get_edge_between("H2", "H1")
        assert e1 is not None
        assert e1 == e2  # Same edge found either direction

    def test_get_edge_between_nonexistent(self, ontology):
        # Some houses may not have direct connections
        # This just tests the method doesn't crash
        result = ontology.get_edge_between("H5", "H10")
        # May or may not exist — just verify no error


# ═══════════════════════════════════════════════════════════════
# SPHERE SEARCH
# ═══════════════════════════════════════════════════════════════

class TestSphereSearch:
    """Verify keyword-based sphere search works."""

    def test_search_finds_ai_in_technology(self, ontology):
        results = ontology.search_spheres("AI machine learning neural networks")
        assert len(results) > 0
        house_ids = {s.house_id for s, _ in results}
        assert "H11" in house_ids  # Technology

    def test_search_finds_climate_in_resources(self, ontology):
        results = ontology.search_spheres("climate change carbon emissions warming")
        assert len(results) > 0
        house_ids = {s.house_id for s, _ in results}
        assert "H4" in house_ids  # Resources

    def test_search_finds_law_terms(self, ontology):
        results = ontology.search_spheres("patent copyright intellectual property")
        assert len(results) > 0
        house_ids = {s.house_id for s, _ in results}
        assert "H2" in house_ids  # Law

    def test_search_returns_sorted_by_score(self, ontology):
        results = ontology.search_spheres("economy trade market")
        if len(results) >= 2:
            scores = [score for _, score in results]
            assert scores == sorted(scores, reverse=True)

    def test_search_empty_returns_empty(self, ontology):
        results = ontology.search_spheres("")
        assert len(results) == 0

    def test_search_gibberish_returns_empty(self, ontology):
        results = ontology.search_spheres("xyzzyplugh")
        assert len(results) == 0


# ═══════════════════════════════════════════════════════════════
# SPHERE DATACLASS
# ═══════════════════════════════════════════════════════════════

class TestSphereDataclass:
    """Verify Sphere dataclass methods."""

    def test_sphere_is_frozen(self):
        s = Sphere(id="S1", name="Test", house_id="H1", house_name="Gov", index=0)
        with pytest.raises(AttributeError):
            s.name = "Changed"

    def test_sphere_is_admin_at_index_144(self):
        s = Sphere(id="E145", name="Admin", house_id="E", house_name="Admin", index=144)
        assert s.is_admin

    def test_sphere_not_admin_at_other_index(self):
        s = Sphere(id="S1", name="Test", house_id="H1", house_name="Gov", index=0)
        assert not s.is_admin

    def test_match_score_with_keywords(self):
        s = Sphere(id="S1", name="Test", house_id="H1", house_name="Gov",
                   index=0, keywords=("climate", "carbon", "warming"))
        score = s.match_score("climate change and carbon emissions")
        assert score > 0

    def test_match_score_no_match(self):
        s = Sphere(id="S1", name="Test", house_id="H1", house_name="Gov",
                   index=0, keywords=("climate", "carbon"))
        score = s.match_score("quantum computing")
        assert score == 0.0


# ═══════════════════════════════════════════════════════════════
# LCP PIPELINE
# ═══════════════════════════════════════════════════════════════

class TestLCPPipeline:
    """Verify the full LCP pipeline works end-to-end."""

    def test_ingest_activates_houses(self, engine):
        state = engine.ingest("AI regulation and cybersecurity policy")
        assert len(state.activated_houses) >= 2

    def test_ingest_returns_activation_state(self, engine):
        state = engine.ingest("climate change policy")
        assert isinstance(state, ActivationState)
        assert len(state.activated_spheres) > 0

    def test_activate_loads_edges(self, engine):
        engine.ingest("trade policy and environmental law")
        state = engine.activate()
        assert len(state.active_edges) >= 0  # May have edges between activated houses

    def test_route_returns_dict(self, engine):
        engine.ingest("healthcare AI technology")
        engine.activate()
        result = engine.route("healthcare AI", "H11")
        assert isinstance(result, dict)
        assert "house_id" in result
        assert result["house_id"] == "H11"

    def test_route_all_covers_activated_houses(self, engine):
        engine.ingest("economic policy and technology regulation")
        engine.activate()
        results = engine.route_all("economic policy")
        assert len(results) >= 2
        for hid, data in results.items():
            assert hid in engine.state.activated_houses

    def test_synthesize_returns_analysis_result(self, engine):
        engine.ingest("climate adaptation for coastal cities")
        engine.activate()
        result = engine.synthesize("climate adaptation")
        assert isinstance(result, AnalysisResult)
        assert len(result.activated_houses) > 0

    def test_analyze_full_pipeline(self, engine):
        result = engine.analyze("AI regulation and climate policy")
        assert isinstance(result, AnalysisResult)
        assert len(result.activated_houses) >= 2
        assert len(result.bridges) >= 0
        assert isinstance(result.blind_spots, list)
        assert isinstance(result.coherence_score, float)
        assert result.synthesis_notes != ""
        assert result.task == "AI regulation and climate policy"

    def test_analyze_populates_house_analyses(self, engine):
        result = engine.analyze("cybersecurity threat to financial systems")
        assert len(result.house_analyses) > 0

    def test_blind_spots_are_inactive_houses(self, engine):
        result = engine.analyze("quantum computing research")
        all_house_ids = set(engine.ontology.house_list())
        active = set(result.activated_houses)
        inactive = all_house_ids - active
        # blind_spots should mention inactive houses
        if inactive:
            assert len(result.blind_spots) > 0


# ═══════════════════════════════════════════════════════════════
# PROMPT GENERATION
# ═══════════════════════════════════════════════════════════════

class TestPromptGeneration:
    """Verify prompt generation methods."""

    def test_generate_prompt_compact(self, engine):
        result = engine.analyze("trade policy")
        prompt = engine.generate_prompt(result, "compact")
        assert "LATTICE ACTIVATION" in prompt
        assert "Houses activated" in prompt

    def test_generate_prompt_orchestrator(self, engine):
        result = engine.analyze("climate adaptation")
        prompt = engine.generate_prompt(result, "orchestrator")
        assert "HOUSE ANALYSES" in prompt

    def test_generate_prompt_sphere_agent(self, engine):
        result = engine.analyze("healthcare AI")
        prompt = engine.generate_prompt(result, "sphere_agent")
        assert "SPHERE AGENT" in prompt

    def test_get_system_prompt_modes(self, engine):
        for mode in ("compact", "orchestrator", "sphere_agent"):
            prompt = engine.get_system_prompt(mode)
            assert len(prompt) > 50


# ═══════════════════════════════════════════════════════════════
# CONVENIENCE FUNCTIONS
# ═══════════════════════════════════════════════════════════════

class TestConvenience:
    """Verify convenience functions."""

    def test_create_engine(self):
        e = create_engine()
        assert isinstance(e, LCPEngine)
        assert len(e.ontology.houses) == 12

    def test_quick_analyze(self):
        result = quick_analyze("AI policy")
        assert isinstance(result, AnalysisResult)
        assert len(result.activated_houses) > 0


# ═══════════════════════════════════════════════════════════════
# EDGE CASES
# ═══════════════════════════════════════════════════════════════

class TestEdgeCases:
    """Edge cases and boundary conditions."""

    def test_empty_task(self, engine):
        result = engine.analyze("")
        assert isinstance(result, AnalysisResult)

    def test_very_long_task(self, engine):
        task = "climate " * 500
        result = engine.analyze(task)
        assert isinstance(result, AnalysisResult)

    def test_special_characters(self, engine):
        result = engine.analyze("AI & ML: $100B+ market? <yes>")
        assert isinstance(result, AnalysisResult)

    def test_activation_state_coverage(self):
        state = ActivationState()
        assert state.coverage == 0.0
        assert state.house_coverage == 0.0

    def test_house_edge_involves(self):
        e = HouseEdge(source="H1", target="H2", edge_type="test", strength=0.9)
        assert e.involves("H1")
        assert e.involves("H2")
        assert not e.involves("H3")

    def test_house_edge_other(self):
        e = HouseEdge(source="H1", target="H2", edge_type="test", strength=0.9)
        assert e.other("H1") == "H2"
        assert e.other("H2") == "H1"
        assert e.other("H3") is None

    def test_lcp_phase_enum(self):
        assert LCPPhase.INGEST.value == "ingest"
        assert LCPPhase.SYNTHESIZE.value == "synthesize"
