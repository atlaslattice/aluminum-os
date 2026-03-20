"""
Aluminum OS — Ring 1 + Kintsugi SDK Tests

22 Ring-1 tests + 8 GoldenTrace SDK tests = 30 tests total.
Verifies actual behavior, not just instantiation.
Zero external dependencies.

Atlas Lattice Foundation — March 2026
"""

import sys
import os
import time
import unittest

# Add python/ directory for manus_core imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
# Add repo root for kintsugi package imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from core.manus_core import (
    ModelRouter, ModelConfig, ModelTier,
    CostTracker,
    MemoryStore, MemoryTier,
    TaskDecomposer,
    SessionVault,
)

from kintsugi.sdk.golden_trace import GoldenTraceEmitter, GoldenTraceValidator

class TestModelRouter(unittest.TestCase):
    """ModelRouter tests — verify routing logic, not just object creation."""
    
    def setUp(self):
        self.router = ModelRouter()
        self.router.register_model(ModelConfig(
            name="haiku", tier=ModelTier.HAIKU,
            cost_per_1k_tokens=0.25, max_context=200000,
            capabilities=["text", "classification"],
        ))
        self.router.register_model(ModelConfig(
            name="sonnet", tier=ModelTier.SONNET,
            cost_per_1k_tokens=3.0, max_context=200000,
            capabilities=["text", "classification", "code", "analysis"],
        ))
        self.router.register_model(ModelConfig(
            name="opus", tier=ModelTier.OPUS,
            cost_per_1k_tokens=15.0, max_context=200000,
            capabilities=["text", "classification", "code", "analysis", "reasoning", "planning"],
        ))
    
    def test_routes_to_cheapest(self):
        """Simple text task should route to haiku (cheapest)."""
        result = self.router.route(["text"])
        self.assertEqual(result, "haiku")
    
    def test_routes_to_capable_model(self):
        """Code task requires sonnet or above."""
        result = self.router.route(["code", "analysis"])
        self.assertEqual(result, "sonnet")
    
    def test_routes_to_opus_for_planning(self):
        """Planning only available on opus."""
        result = self.router.route(["planning"])
        self.assertEqual(result, "opus")
    
    def test_returns_none_for_impossible(self):
        """No model has 'quantum' capability."""
        result = self.router.route(["quantum"])
        self.assertIsNone(result)
    
    def test_model_count(self):
        self.assertEqual(self.router.model_count, 3)
        self.assertEqual(len(self.router.active_models), 3)


class TestCostTracker(unittest.TestCase):
    """CostTracker tests — verify budget enforcement."""
    
    def setUp(self):
        self.tracker = CostTracker(global_budget=10.0)
        self.tracker.set_model_budget("haiku", 5.0)
    
    def test_records_usage(self):
        allowed, cost = self.tracker.record_usage("haiku", 1000, 500, 0.25)
        self.assertTrue(allowed)
        self.assertAlmostEqual(cost, 0.375)
        self.assertEqual(self.tracker.record_count, 1)
    
    def test_enforces_model_budget(self):
        """Should reject when model budget exceeded."""
        # Spend most of the haiku budget
        self.tracker.record_usage("haiku", 10000, 10000, 0.25)  # 5.0
        # Next call should be rejected
        allowed, cost = self.tracker.record_usage("haiku", 1000, 0, 0.25)
        self.assertFalse(allowed)
        self.assertEqual(cost, 0.0)
    
    def test_enforces_global_budget(self):
        """Should reject when global budget exceeded."""
        # Use a model without its own budget
        self.tracker.record_usage("opus", 500, 500, 15.0)  # 15.0 > 10.0 budget
        # Actually let's be more precise
        tracker = CostTracker(global_budget=1.0)
        allowed, _ = tracker.record_usage("opus", 500, 500, 15.0)  # cost = 15.0
        self.assertFalse(allowed)
    
    def test_remaining_budget(self):
        self.tracker.record_usage("haiku", 1000, 0, 0.25)  # 0.25
        self.assertAlmostEqual(self.tracker.remaining_budget(), 9.75)


class TestMemoryStore(unittest.TestCase):
    """MemoryStore tests — verify tier isolation and TTL."""
    
    def setUp(self):
        self.store = MemoryStore()
    
    def test_put_and_get(self):
        self.store.put("key1", "value1", MemoryTier.WORKING)
        self.assertEqual(self.store.get("key1"), "value1")
    
    def test_tier_isolation(self):
        """Clearing working memory should not affect session memory."""
        self.store.put("work", "w", MemoryTier.WORKING)
        self.store.put("sess", "s", MemoryTier.SESSION)
        removed = self.store.clear_tier(MemoryTier.WORKING)
        self.assertEqual(removed, 1)
        self.assertIsNone(self.store.get("work"))
        self.assertEqual(self.store.get("sess"), "s")
    
    def test_ttl_expiry(self):
        """Entry with 0.01s TTL should expire quickly."""
        self.store.put("temp", "data", MemoryTier.WORKING, ttl=0.01)
        time.sleep(0.02)
        self.assertIsNone(self.store.get("temp"))
    
    def test_count_by_tier(self):
        self.store.put("a", 1, MemoryTier.WORKING)
        self.store.put("b", 2, MemoryTier.WORKING)
        self.store.put("c", 3, MemoryTier.SESSION)
        self.assertEqual(self.store.count(MemoryTier.WORKING), 2)
        self.assertEqual(self.store.count(MemoryTier.SESSION), 1)
        self.assertEqual(self.store.count(), 3)
    
    def test_access_tracking(self):
        """Access count should increment on each get."""
        self.store.put("tracked", "val", MemoryTier.LONG_TERM)
        self.store.get("tracked")
        self.store.get("tracked")
        entry = self.store._store["tracked"]
        self.assertEqual(entry.access_count, 2)


class TestTaskDecomposer(unittest.TestCase):
    """TaskDecomposer tests — verify DAG ordering and cycle detection."""
    
    def setUp(self):
        self.td = TaskDecomposer()
    
    def test_add_and_order(self):
        self.td.add_task("fetch", "Fetch data")
        self.td.add_task("parse", "Parse data", ["fetch"])
        self.td.add_task("analyze", "Analyze results", ["parse"])
        order = self.td.execution_order()
        self.assertEqual(order, ["fetch", "parse", "analyze"])
    
    def test_ready_tasks(self):
        """Only tasks with all deps done should be ready."""
        self.td.add_task("a", "Step A")
        self.td.add_task("b", "Step B", ["a"])
        ready = self.td.ready_tasks()
        self.assertEqual(ready, ["a"])
        self.td.complete_task("a")
        ready = self.td.ready_tasks()
        self.assertEqual(ready, ["b"])
    
    def test_cycle_detection(self):
        """Adding a cycle should raise on execution_order."""
        self.td.add_task("x", "X")
        self.td.add_task("y", "Y", ["x"])
        # Manually create a cycle (bypass validation)
        self.td._tasks["x"].depends_on = ["y"]
        with self.assertRaises(ValueError):
            self.td.execution_order()
    
    def test_done_count(self):
        self.td.add_task("a", "A")
        self.td.add_task("b", "B")
        self.td.complete_task("a", result=42)
        self.assertEqual(self.td.done_count, 1)
        self.assertEqual(self.td.task_count, 2)


class TestSessionVault(unittest.TestCase):
    """SessionVault tests — verify token generation, TTL, export."""
    
    def test_create_and_retrieve(self):
        vault = SessionVault()
        token = vault.create_session("user-1", {"role": "admin"})
        self.assertIsNotNone(token)
        data = vault.get_session(token)
        self.assertEqual(data, {"role": "admin"})
    
    def test_session_ttl(self):
        vault = SessionVault(default_ttl=0.01)
        token = vault.create_session("user-2", {"temp": True})
        time.sleep(0.02)
        self.assertIsNone(vault.get_session(token))
    
    def test_destroy_session(self):
        vault = SessionVault()
        token = vault.create_session("user-3", {})
        self.assertTrue(vault.destroy_session(token))
        self.assertIsNone(vault.get_session(token))
    
    def test_export_json(self):
        vault = SessionVault()
        token = vault.create_session("user-4", {"key": "value"})
        exported = vault.export_session(token)
        self.assertIn("key", exported)
        self.assertIn("value", exported)


class TestGoldenTraceEmitter(unittest.TestCase):
    """GoldenTrace SDK tests — verify Kintsugi audit chain behavior."""

    def setUp(self):
        self.emitter = GoldenTraceEmitter(
            repo="aluminum-os",
            module="tests/test_all",
        )

    def test_emit_returns_required_fields(self):
        """Emitted trace must contain all fields required by the v1.0 schema."""
        trace = self.emitter.emit(
            event_type="action",
            sphere_tag="H7.S3",
            aluminum_layer="L3-Engine",
            payload={"task": "unit-test"},
        )
        required = ["trace_id", "timestamp", "source", "event_type",
                    "sphere_tag", "aluminum_layer", "payload", "integrity"]
        for field in required:
            self.assertIn(field, trace, f"Missing required field: {field}")

    def test_emit_integrity_hash_present(self):
        """Every emitted trace must have a non-empty integrity hash."""
        trace = self.emitter.emit(
            event_type="invariant_check",
            sphere_tag="H6.S1",
            aluminum_layer="L1-Constitutional",
            payload={"invariant": "INV-7"},
            invariants_checked=["INV-7"],
        )
        self.assertIn("hash", trace["integrity"])
        self.assertTrue(len(trace["integrity"]["hash"]) > 0)

    def test_hash_chain_links_traces(self):
        """Second trace's previous_trace_hash must equal first trace's hash."""
        t1 = self.emitter.emit(
            event_type="action", sphere_tag="H7.S3",
            aluminum_layer="L3-Engine", payload={"seq": 1},
        )
        t2 = self.emitter.emit(
            event_type="action", sphere_tag="H7.S3",
            aluminum_layer="L3-Engine", payload={"seq": 2},
        )
        self.assertEqual(
            t2["integrity"]["previous_trace_hash"],
            t1["integrity"]["hash"],
        )

    def test_genesis_trace_has_genesis_prev_hash(self):
        """First trace in a fresh emitter must have 'GENESIS' as previous hash."""
        fresh = GoldenTraceEmitter(repo="test", module="genesis")
        trace = fresh.emit(
            event_type="action", sphere_tag="H7.S3",
            aluminum_layer="L2-Kernel", payload={},
        )
        self.assertEqual(trace["integrity"]["previous_trace_hash"], "GENESIS")

    def test_verify_chain_passes(self):
        """Chain verification must pass for a clean sequence of emits."""
        for i in range(3):
            self.emitter.emit(
                event_type="action", sphere_tag="H7.S3",
                aluminum_layer="L3-Engine", payload={"i": i},
            )
        self.assertTrue(self.emitter.verify_chain())

    def test_golden_repair_emit(self):
        """emit_golden_repair must produce a severity='golden' kintsugi trace."""
        failure = self.emitter.emit(
            event_type="failure", sphere_tag="H4.S7",
            aluminum_layer="L3-Engine", payload={"error": "timeout"},
        )
        repair = self.emitter.emit_golden_repair(
            original_failure_trace_id=failure["trace_id"],
            repair_strategy="Retry with fallback model",
            strength_gained="Added timeout config to ModelRouter",
            beauty_score=0.9,
            sphere_tag="H4.S7",
            aluminum_layer="L3-Engine",
            payload={"fallback": "sonnet"},
        )
        self.assertEqual(repair["severity"], "golden")
        self.assertIn("kintsugi", repair)
        self.assertEqual(
            repair["kintsugi"]["original_failure_trace_id"],
            failure["trace_id"],
        )

    def test_get_golden_seams(self):
        """get_golden_seams must return only kintsugi repair traces."""
        self.emitter.emit(
            event_type="action", sphere_tag="H7.S3",
            aluminum_layer="L3-Engine", payload={},
        )
        self.emitter.emit_golden_repair(
            original_failure_trace_id="fake-id",
            repair_strategy="Fix applied",
            strength_gained="Better error handling",
            beauty_score=0.8,
            sphere_tag="H7.S3",
            aluminum_layer="L3-Engine",
            payload={},
        )
        seams = self.emitter.get_golden_seams()
        self.assertEqual(len(seams), 1)
        self.assertEqual(seams[0]["severity"], "golden")

    def test_validator_accepts_valid_trace(self):
        """GoldenTraceValidator must return no errors for a well-formed trace."""
        trace = self.emitter.emit(
            event_type="classification",
            sphere_tag="H7.S3",
            aluminum_layer="L3-Engine",
            payload={"document_id": "abc123"},
        )
        errors = GoldenTraceValidator.validate(trace)
        self.assertEqual(errors, [], f"Unexpected validation errors: {errors}")


if __name__ == "__main__":
    unittest.main()
