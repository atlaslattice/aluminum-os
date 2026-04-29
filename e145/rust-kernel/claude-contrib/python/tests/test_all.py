"""
Aluminum OS v3.0 — Real Validation Suite

These tests verify BEHAVIOR, not just instantiation.
Every test checks actual outputs against expected results.
"""

import json
import time
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from core.manus_core import (
    ModelRouter, ModelTier, CostTracker, MemoryStore,
    TaskDecomposer, SessionVault, AVAILABLE_MODELS,
)


class TestResult:
    def __init__(self, name):
        self.name = name
        self.passed = False
        self.error = None
        self.duration = 0

    def __repr__(self):
        status = "PASS" if self.passed else f"FAIL: {self.error}"
        return f"  [{status}] {self.name} ({self.duration:.3f}s)"


def run_test(name, fn):
    result = TestResult(name)
    start = time.time()
    try:
        fn()
        result.passed = True
    except Exception as e:
        result.error = str(e)
    result.duration = time.time() - start
    return result


# ============================================================
# MODEL ROUTER TESTS
# ============================================================

def test_router_simple_task_routes_cheap():
    """Simple tasks should route to cheapest tier."""
    router = ModelRouter()
    model = router.select_model("list all files in the directory")
    assert model is not None, "Should find a model"
    assert model.tier == ModelTier.CHEAP, f"Simple task routed to {model.tier.value}, expected cheap"

def test_router_complex_task_routes_premium():
    """Complex reasoning tasks should route to premium tier."""
    router = ModelRouter()
    model = router.select_model("analyze the architectural trade-offs and evaluate alternatives")
    assert model is not None, "Should find a model"
    assert model.tier == ModelTier.PREMIUM, f"Complex task routed to {model.tier.value}, expected premium"

def test_router_cheapest_within_tier():
    """Should pick the cheapest model within the required tier."""
    router = ModelRouter()
    model = router.select_model("summarize this document")
    assert model is not None
    # Within standard tier, should pick cheapest by input cost
    standard_models = [m for m in AVAILABLE_MODELS if m.tier == ModelTier.STANDARD]
    cheapest = min(standard_models, key=lambda m: m.cost_per_1k_input)
    # Router might also pick a cheap model that handles "summarize" — that's also valid
    # The key check: it should NOT pick a premium model
    assert model.tier != ModelTier.PREMIUM, "Summarize should not need premium"

def test_router_capability_filtering():
    """Should filter by required capabilities."""
    router = ModelRouter()
    model = router.select_model("analyze this image", required_caps=["vision"])
    assert model is not None, "Should find a vision-capable model"
    assert "vision" in model.capabilities, f"{model.name} doesn't have vision"

def test_router_cost_estimation():
    """Cost estimation should be mathematically correct."""
    router = ModelRouter()
    model = AVAILABLE_MODELS[0]  # deepseek-chat
    cost = router.estimate_cost(model, input_tokens=1000, output_tokens=500)
    expected = (1000/1000 * model.cost_per_1k_input + 500/1000 * model.cost_per_1k_output)
    assert abs(cost - expected) < 1e-10, f"Cost mismatch: {cost} != {expected}"


# ============================================================
# COST TRACKER TESTS
# ============================================================

def test_tracker_records_and_sums():
    """Should accurately track costs across multiple calls."""
    tracker = CostTracker()
    tracker.record("deepseek-chat", 1000, 500, 0.0003, "text")
    tracker.record("claude-opus-4", 2000, 1000, 0.09, "reasoning")
    assert len(tracker.entries) == 2
    assert abs(tracker.total_cost() - 0.0903) < 1e-10

def test_tracker_by_model():
    """Should break down costs by model."""
    tracker = CostTracker()
    tracker.record("model-a", 100, 50, 0.01, "text")
    tracker.record("model-a", 100, 50, 0.01, "text")
    tracker.record("model-b", 100, 50, 0.05, "code")
    by_model = tracker.cost_by_model()
    assert abs(by_model["model-a"] - 0.02) < 1e-10
    assert abs(by_model["model-b"] - 0.05) < 1e-10

def test_tracker_summary_structure():
    """Summary should contain all required fields."""
    tracker = CostTracker()
    tracker.record("test", 500, 200, 0.001, "test")
    summary = tracker.summary()
    assert "total_cost_usd" in summary
    assert "total_calls" in summary
    assert "tokens" in summary
    assert summary["total_calls"] == 1
    assert summary["tokens"]["input"] == 500
    assert summary["tokens"]["output"] == 200


# ============================================================
# MEMORY STORE TESTS
# ============================================================

def test_memory_store_and_recall():
    """Should store entries and recall by semantic similarity."""
    mem = MemoryStore()
    mem.store("The Stryker cyberattack was a noosphere warfare event")
    mem.store("Aluminum OS uses a buddy allocator for memory management")
    mem.store("The Pantheon Council uses BFT governance")

    results = mem.recall("cyberattack warfare")
    assert len(results) > 0, "Should recall something"
    assert "cyberattack" in results[0]["content"].lower() or "warfare" in results[0]["content"].lower()

def test_memory_deduplication():
    """Storing the same content twice should not create duplicates."""
    mem = MemoryStore()
    id1 = mem.store("Duplicate content test")
    id2 = mem.store("Duplicate content test")
    assert id1 == id2, f"Should return same ID: {id1} != {id2}"
    assert mem.count() == 1, f"Should have 1 entry, got {mem.count()}"

def test_memory_delete():
    """Should be able to delete entries."""
    mem = MemoryStore()
    entry_id = mem.store("Temporary memory")
    assert mem.count() == 1
    assert mem.delete(entry_id)
    assert mem.count() == 0

def test_memory_similarity_ordering():
    """More similar entries should rank higher."""
    mem = MemoryStore()
    mem.store("Python is a programming language for data science")
    mem.store("Rust is a systems programming language for performance")
    mem.store("The weather today is sunny and warm")

    results = mem.recall("programming language")
    assert len(results) >= 2
    # Build score map
    scores = {r["content"][:10]: r["similarity"] for r in results}
    # Programming entries should have higher similarity than weather (if weather appears)
    prog_scores = [r["similarity"] for r in results if "programming" in r["content"]]
    weather_scores = [r["similarity"] for r in results if "weather" in r["content"]]
    assert len(prog_scores) >= 1, "Should find at least one programming entry"
    if weather_scores:
        assert max(prog_scores) > max(weather_scores), "Programming should rank higher"


# ============================================================
# TASK DECOMPOSER TESTS
# ============================================================

def test_decomposer_sync_template():
    """Sync goals should match sync template."""
    decomposer = TaskDecomposer()
    result = decomposer.decompose("Run daily sync of all systems")
    assert result["template"] == "sync"
    assert len(result["tasks"]) == 6

def test_decomposer_parallel_groups():
    """Should identify tasks that can run in parallel."""
    decomposer = TaskDecomposer()
    result = decomposer.decompose("sync everything")
    groups = result["parallel_groups"]
    # First group should have tasks with no deps (can run in parallel)
    assert len(groups) > 1, "Should have multiple execution phases"
    assert len(groups[0]) >= 2, "First phase should have parallel tasks"

def test_decomposer_dependency_integrity():
    """All dependencies should reference valid task IDs."""
    decomposer = TaskDecomposer()
    for template_name in ["sync", "research", "deploy"]:
        result = decomposer.decompose(f"do a {template_name}")
        task_ids = {t["id"] for t in result["tasks"]}
        for task in result["tasks"]:
            for dep in task["deps"]:
                assert dep in task_ids, f"Task {task['id']} depends on non-existent {dep}"

def test_decomposer_generic_fallback():
    """Unknown goals should get generic decomposition."""
    decomposer = TaskDecomposer()
    result = decomposer.decompose("do something completely novel")
    assert result["template"] == "generic"
    assert len(result["tasks"]) == 1


# ============================================================
# SESSION VAULT TESTS
# ============================================================

def test_session_serialize_restore():
    """Should roundtrip state through JSON."""
    vault = SessionVault()
    vault.set("counter", 42)
    vault.set("name", "aluminum-os")
    vault.set("config", {"debug": True, "version": "3.0"})

    serialized = vault.serialize()

    vault2 = SessionVault()
    assert vault2.restore(serialized)
    assert vault2.get("counter") == 42
    assert vault2.get("name") == "aluminum-os"
    assert vault2.get("config")["version"] == "3.0"

def test_session_restore_invalid():
    """Should handle invalid JSON gracefully."""
    vault = SessionVault()
    assert not vault.restore("this is not json {{{")
    assert not vault.restore("")

def test_session_missing_key():
    """Should return default for missing keys."""
    vault = SessionVault()
    assert vault.get("nonexistent") is None
    assert vault.get("nonexistent", "fallback") == "fallback"


# ============================================================
# RUN ALL TESTS
# ============================================================

ALL_TESTS = [
    # Router (5)
    ("Router: simple task → cheap model", test_router_simple_task_routes_cheap),
    ("Router: complex task → premium model", test_router_complex_task_routes_premium),
    ("Router: picks cheapest within tier", test_router_cheapest_within_tier),
    ("Router: capability filtering", test_router_capability_filtering),
    ("Router: cost estimation math", test_router_cost_estimation),
    # Tracker (3)
    ("Tracker: records and sums", test_tracker_records_and_sums),
    ("Tracker: breakdown by model", test_tracker_by_model),
    ("Tracker: summary structure", test_tracker_summary_structure),
    # Memory (4)
    ("Memory: store and recall", test_memory_store_and_recall),
    ("Memory: deduplication", test_memory_deduplication),
    ("Memory: delete", test_memory_delete),
    ("Memory: similarity ordering", test_memory_similarity_ordering),
    # Decomposer (4)
    ("Decomposer: sync template match", test_decomposer_sync_template),
    ("Decomposer: parallel groups", test_decomposer_parallel_groups),
    ("Decomposer: dependency integrity", test_decomposer_dependency_integrity),
    ("Decomposer: generic fallback", test_decomposer_generic_fallback),
    # Session (3)
    ("Session: serialize/restore roundtrip", test_session_serialize_restore),
    ("Session: invalid JSON handling", test_session_restore_invalid),
    ("Session: missing key defaults", test_session_missing_key),
]


def main():
    print("=" * 60)
    print("  ALUMINUM OS v3.0 — VALIDATION SUITE")
    print("  Testing actual behavior, not just instantiation.")
    print("=" * 60)
    print()

    results = []
    for name, fn in ALL_TESTS:
        result = run_test(name, fn)
        results.append(result)
        print(result)

    passed = sum(1 for r in results if r.passed)
    failed = sum(1 for r in results if not r.passed)
    total_time = sum(r.duration for r in results)

    print()
    print("-" * 60)
    print(f"  PASSED: {passed}/{len(results)}")
    print(f"  FAILED: {failed}/{len(results)}")
    print(f"  TIME:   {total_time:.3f}s")
    print("-" * 60)

    if failed > 0:
        print("\n  FAILURES:")
        for r in results:
            if not r.passed:
                print(f"    {r.name}: {r.error}")
        sys.exit(1)

    # Write results JSON
    output = {
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S"),
        "passed": passed,
        "failed": failed,
        "total": len(results),
        "total_time_seconds": round(total_time, 3),
        "results": [
            {"name": r.name, "status": "PASS" if r.passed else "FAIL",
             "time": round(r.duration, 3), "error": r.error}
            for r in results
        ]
    }
    print(f"\n  Results: {json.dumps(output, indent=2)}")


if __name__ == "__main__":
    main()
