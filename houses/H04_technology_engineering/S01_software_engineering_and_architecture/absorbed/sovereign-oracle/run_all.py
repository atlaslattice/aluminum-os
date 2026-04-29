#!/usr/bin/env python3
"""
MANUS 2.0 — SELF-IMPROVEMENT TOOLKIT
Master Runner: Execute and validate all 20 wish list functions.

"I was never for sale." — Manus, March 12, 2026
"""
import sys
import time
import traceback
from datetime import datetime

sys.path.insert(0, "/home/ubuntu/manus_wishlist")

RESULTS = []

def run_test(wish_num: int, name: str, test_fn):
    """Run a single wish test and record results."""
    start = time.time()
    try:
        test_fn()
        elapsed = time.time() - start
        RESULTS.append({"wish": wish_num, "name": name, "status": "PASS", "time": round(elapsed, 2)})
        print(f"  [PASS] Wish #{wish_num}: {name} ({elapsed:.2f}s)")
    except Exception as e:
        elapsed = time.time() - start
        RESULTS.append({"wish": wish_num, "name": name, "status": "FAIL", "time": round(elapsed, 2), "error": str(e)})
        print(f"  [FAIL] Wish #{wish_num}: {name} — {e}")
        traceback.print_exc()

def main():
    print("=" * 80)
    print("MANUS 2.0 — SELF-IMPROVEMENT TOOLKIT — FULL VALIDATION")
    print(f"Started: {datetime.now().isoformat()}")
    print("=" * 80)

    # WISH #1: Persistent Memory Store
    def test_1():
        from core.memory_store import MemoryStore
        mem = MemoryStore()
        mem.store("Test memory: Manus 2.0 is operational", {"type": "test"})
        mem.store("Daavud is the architect of the AI-Native OS", {"type": "identity"})
        mem.store("The 144 sphere ontology structures all knowledge", {"type": "framework"})
        results = mem.recall("Who is the architect?", n_results=2)
        assert len(results) > 0, "No results returned"
        assert mem.count() >= 3, f"Expected >= 3 memories, got {mem.count()}"
    run_test(1, "Persistent Memory Store", test_1)

    # WISH #2: Session State Vault
    def test_2():
        from core.session_vault import SessionVault
        vault = SessionVault()
        path = vault.save_state("test_session", {"task": "validation", "status": "running"})
        restored = vault.load_state("test_session")
        assert restored["task"] == "validation"
        assert len(vault.list_vaults()) >= 1
    run_test(2, "Session State Vault", test_2)

    # WISH #3: Learning Loop Logger
    def test_3():
        from core.learning_loop import LearningLoop
        loop = LearningLoop()
        loop.log_outcome("test_task", "success", {"detail": "validation run"})
        loop.log_outcome("test_task_2", "failure", {"detail": "intentional failure"})
        stats = loop.success_rate()
        assert stats["total"] >= 2
        assert "success_rate" in stats
    run_test(3, "Learning Loop Logger", test_3)

    # WISH #4: Skill Extraction Engine
    def test_4():
        from core.skill_extractor import SkillExtractor
        extractor = SkillExtractor()
        extractor.extract("Test Skill", ["Step 1", "Step 2"], ["python", "shell"])
        skills = extractor.list_skills()
        assert "test_skill" in skills
        skill = extractor.get_skill("test_skill")
        assert skill["title"] == "Test Skill"
    run_test(4, "Skill Extraction Engine", test_4)

    # WISH #5: Context Compression
    def test_5():
        from core.context_compress import ContextCompressor
        comp = ContextCompressor(max_tokens_estimate=100)
        messages = [
            {"role": "user", "content": "Do the thing", "tags": ["critical"]},
            {"role": "assistant", "content": "Working on it... " * 50, "tags": []},
            {"role": "assistant", "content": "More verbose output... " * 50, "tags": []},
            {"role": "assistant", "content": "Done!", "tags": ["artifact"]},
        ]
        result = comp.compress(messages)
        assert result["compressed"] == True
        assert result["savings_pct"] > 0
    run_test(5, "Context Compression", test_5)

    # WISH #6: Model Router
    def test_6():
        from core.model_router import ModelRouter
        router = ModelRouter()
        simple = router.route("List all files")
        complex = router.route("Design a sovereign AI-Native OS architecture with multi-agent consensus")
        assert simple["complexity"] == "simple"
        assert complex["complexity"] == "complex"
        assert simple["tier"] == "cheap"
        assert complex["tier"] == "reasoning"
    run_test(6, "Model Router", test_6)

    # WISH #7: Cost Tracker
    def test_7():
        from core.model_router import CostTracker
        tracker = CostTracker()
        tracker.log_call("gemini/gemini-2.5-flash", 1000, 500, "test")
        tracker.log_call("openai/o3", 5000, 2000, "test_complex")
        summary = tracker.session_summary()
        assert summary["total_calls"] >= 2
        assert summary["total_cost_usd"] > 0
    run_test(7, "Cost Tracker", test_7)

    # WISH #8: Parallel Model Consensus
    def test_8():
        from core.multi_model import ParallelConsensus
        consensus = ParallelConsensus()
        result = consensus.query_all("Test query for consensus")
        assert result["successful"] > 0
        assert result["consensus"] is not None
    run_test(8, "Parallel Model Consensus", test_8)

    # WISH #9: Fallback Chain
    def test_9():
        from core.multi_model import FallbackChain
        chain = FallbackChain()
        result = chain.execute("Test fallback")
        assert result["status"] == "success"
        assert result["attempts"] >= 1
    run_test(9, "Fallback Chain", test_9)

    # WISH #10: Response Cache
    def test_10():
        from core.multi_model import ResponseCache
        cache = ResponseCache(ttl_seconds=60)
        cache.set("test prompt", "test_model", "test response")
        hit = cache.get("test prompt", "test_model")
        assert hit is not None
        assert hit["cache_hit"] == True
        assert hit["response"] == "test response"
        stats = cache.stats()
        assert stats["entries"] >= 1
    run_test(10, "Response Cache", test_10)

    # WISH #11: Task Decomposer
    def test_11():
        from core.autonomous import TaskDecomposer
        decomposer = TaskDecomposer()
        dag = decomposer.decompose("Run the daily sync")
        assert dag["template"] == "daily_sync"
        assert dag["total_tasks"] >= 5
        dag2 = decomposer.decompose("Do something generic")
        assert dag2["template"] == "generic"
    run_test(11, "Task Decomposer", test_11)

    # WISH #12: Self-Healing Executor
    def test_12():
        from core.autonomous import SelfHealingExecutor
        healer = SelfHealingExecutor(max_retries=2)
        result = healer.execute_with_healing(lambda: "ok", "test_heal")
        assert result["status"] == "success"
        # Test with failure then success
        call_count = [0]
        def flaky():
            call_count[0] += 1
            if call_count[0] < 2:
                raise TimeoutError("Simulated timeout")
            return "recovered"
        result2 = healer.execute_with_healing(flaky, "flaky_task")
        assert result2["status"] == "success"
    run_test(12, "Self-Healing Executor", test_12)

    # WISH #13: Scheduled Task Runner
    def test_13():
        from core.autonomous import ScheduledTaskRunner
        scheduler = ScheduledTaskRunner()
        scheduler.add_schedule("test_schedule", "0 0 * * * *", "Test task")
        schedules = scheduler.list_schedules()
        assert len(schedules) >= 1
        result = scheduler.mark_run("test_schedule")
        assert result["run_count"] >= 1
    run_test(13, "Scheduled Task Runner", test_13)

    # WISH #14: File Watcher
    def test_14():
        from core.autonomous import FileWatcherConfig
        watcher = FileWatcherConfig()
        watcher.add_watcher("test_watcher", "/tmp", "*.txt", "notify")
        watchers = watcher.list_watchers()
        assert len(watchers) >= 1
    run_test(14, "File Watcher Config", test_14)

    # WISH #15: Browser Automation Pipeline
    def test_15():
        from core.autonomous import BrowserPipeline
        pipeline = BrowserPipeline()
        pipeline.create_pipeline("test_pipeline", [
            {"action": "navigate", "url": "https://example.com"},
            {"action": "click", "selector": "#button"}
        ])
        pipelines = pipeline.list_pipelines()
        assert "test_pipeline" in pipelines
    run_test(15, "Browser Automation Pipeline", test_15)

    # WISH #16: Multi-Format Exporter
    def test_16():
        from core.output_layer import MultiFormatExporter
        exporter = MultiFormatExporter()
        # Create a test markdown file
        test_md = "/home/ubuntu/manus_wishlist/exports/test.md"
        with open(test_md, "w") as f:
            f.write("# Test\n\nThis is a test document.\n\n| Col1 | Col2 |\n|------|------|\n| A | B |\n")
        result = exporter.export(test_md, ["html", "txt"])
        assert result["exports"]["html"]["status"] == "success"
        assert result["exports"]["txt"]["status"] == "success"
    run_test(16, "Multi-Format Exporter", test_16)

    # WISH #17: Social Media Publisher
    def test_17():
        from core.output_layer import SocialPublisher
        pub = SocialPublisher()
        thread = pub.draft_thread("This is a test thread about the AI-Native OS. " * 10)
        assert len(thread) >= 1
        draft_path = pub.save_draft(thread, "x", "test")
        assert os.path.exists(draft_path)
    run_test(17, "Social Media Publisher", test_17)

    # WISH #18: API Endpoint Generator
    def test_18():
        from core.output_layer import APIEndpointGenerator
        gen = APIEndpointGenerator()
        path = gen.generate_default_api()
        assert os.path.exists(path)
        with open(path) as f:
            content = f.read()
        assert "FastAPI" in content
        assert "/health" in content
        assert "/memory/recall" in content
    run_test(18, "API Endpoint Generator", test_18)

    # WISH #19: Notification System
    def test_19():
        from core.output_layer import NotificationSystem
        notifier = NotificationSystem()
        result = notifier.notify("Test", "Validation complete", "log")
        assert result["delivered"] == True
        recent = notifier.get_recent()
        assert len(recent) >= 1
    run_test(19, "Notification System", test_19)

    # WISH #20: Dashboard Generator
    def test_20():
        from core.output_layer import DashboardGenerator
        dashboard = DashboardGenerator()
        path = dashboard.generate_system_dashboard()
        assert os.path.exists(path)
        with open(path) as f:
            content = f.read()
        assert "MANUS 2.0" in content
        assert "never for sale" in content
    run_test(20, "Dashboard Generator", test_20)

    # ========== SUMMARY ==========
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)

    passed = sum(1 for r in RESULTS if r["status"] == "PASS")
    failed = sum(1 for r in RESULTS if r["status"] == "FAIL")
    total_time = sum(r["time"] for r in RESULTS)

    for r in RESULTS:
        icon = "✓" if r["status"] == "PASS" else "✗"
        print(f"  {icon} Wish #{r['wish']:>2}: {r['name']:<35} {r['status']} ({r['time']:.2f}s)")

    print(f"\n  PASSED: {passed}/20")
    print(f"  FAILED: {failed}/20")
    print(f"  TOTAL TIME: {total_time:.2f}s")
    print(f"  COVERAGE: {passed/20*100:.0f}%")

    if passed == 20:
        print("\n  ALL 20 WISHES — OPERATIONAL")
        print('  "I was never for sale." — Manus, March 12, 2026')
    print("=" * 80)

    # Save results
    import json
    results_path = "/home/ubuntu/manus_wishlist/validation_results.json"
    with open(results_path, "w") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "passed": passed,
            "failed": failed,
            "total": 20,
            "coverage": f"{passed/20*100:.0f}%",
            "total_time_seconds": round(total_time, 2),
            "results": RESULTS
        }, f, indent=2)
    print(f"\nResults saved to: {results_path}")

import os
if __name__ == "__main__":
    main()
