#!/usr/bin/env python3
"""
End-to-End Tests for Automated Ingestion Pipeline

Tests:
- Novelty filtering
- LLM significance scoring
- Full pipeline integration
- Scheduler functionality
"""

import sys
import json
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.ingestion.ingestion_pipeline import (
    StagingLayer,
    SignificanceFilter,
    IngestionPipeline
)
from src.ingestion.scheduler import IngestionScheduler


def test_novelty_filtering():
    """Test that duplicate content is rejected"""
    print("\n" + "=" * 70)
    print("TEST 1: Novelty Filtering")
    print("=" * 70)

    staging = StagingLayer(
        staging_dir="./staging/test",
        enable_novelty_check=True
    )

    # Add same item twice
    items = [
        {
            "title": "Test Article on Quantum Computing",
            "content": "This is a test article about quantum computing and its applications in cryptography.",
            "source_type": "test"
        },
        {
            "title": "Test Article on Quantum Computing",
            "content": "This is a test article about quantum computing and its applications in cryptography.",
            "source_type": "test"
        }
    ]

    count = staging.add_to_staging(items, source="test")

    print(f"✓ Added items: {count}")
    assert count == 1, f"Expected 1 item (duplicates filtered), got {count}"

    # Try adding different content
    new_items = [
        {
            "title": "Completely Different Topic",
            "content": "This article discusses machine learning applications in healthcare.",
            "source_type": "test"
        }
    ]

    count2 = staging.add_to_staging(new_items, source="test")
    print(f"✓ Added new items: {count2}")
    assert count2 == 1, f"Expected 1 new item, got {count2}"

    print("✅ Novelty filtering works correctly")
    return True


def test_significance_scoring_heuristic():
    """Test heuristic-based significance scoring"""
    print("\n" + "=" * 70)
    print("TEST 2: Heuristic Significance Scoring")
    print("=" * 70)

    filter = SignificanceFilter(use_llm=False)

    # High-quality item
    good_item = {
        "title": "Novel Quantum Algorithm Breakthrough",
        "content": "Researchers publish groundbreaking paper on quantum computing algorithms. " * 50,
        "source_type": "research_paper",
        "authors": ["Dr. Smith", "Dr. Jones"],
        "categories": ["quantum", "algorithms"],
        "published_date": "2026-01-10T00:00:00Z"
    }

    is_sig, score, reason = filter.is_significant(good_item)
    print(f"✓ High-quality item: Score={score:.2f}, Significant={is_sig}")
    print(f"  Reason: {reason}")
    assert is_sig == True, "High-quality item should be significant"
    assert score >= 0.5, f"Expected score >= 0.5, got {score}"

    # Low-quality item
    bad_item = {
        "title": "Short note",
        "content": "Brief text.",
        "source_type": "unknown"
    }

    is_sig2, score2, reason2 = filter.is_significant(bad_item)
    print(f"✓ Low-quality item: Score={score2:.2f}, Significant={is_sig2}")
    print(f"  Reason: {reason2}")
    assert is_sig2 == False, "Low-quality item should be insignificant"

    print("✅ Heuristic significance scoring works correctly")
    return True


def test_significance_scoring_llm():
    """Test LLM-based significance scoring (requires GEMINI_API_KEY)"""
    print("\n" + "=" * 70)
    print("TEST 3: LLM Significance Scoring")
    print("=" * 70)

    import os
    if not os.getenv("GEMINI_API_KEY"):
        print("⚠️  Skipping (GEMINI_API_KEY not set)")
        return True

    filter = SignificanceFilter(use_llm=True)

    # Test item
    test_item = {
        "title": "Breakthrough in Quantum Error Correction",
        "content": """Researchers at MIT have developed a novel approach to quantum error
        correction that could enable practical quantum computers. The new technique reduces
        error rates by 90% compared to existing methods, bringing quantum computing closer
        to real-world applications in cryptography, drug discovery, and optimization.""" * 3,
        "source_type": "research_paper",
        "authors": ["Dr. Smith"],
        "published_date": "2026-01-10T00:00:00Z"
    }

    is_sig, score, reason = filter.is_significant(test_item)
    print(f"✓ LLM evaluation: Score={score:.2f}, Significant={is_sig}")
    print(f"  Reasoning: {reason}")

    # Should be significant
    assert score >= 0.4, f"Expected reasonable score, got {score}"

    print("✅ LLM significance scoring works correctly")
    return True


def test_full_pipeline():
    """Test complete automated pipeline"""
    print("\n" + "=" * 70)
    print("TEST 4: Full Ingestion Pipeline")
    print("=" * 70)

    pipeline = IngestionPipeline(
        staging_dir="./staging/test",
        auto_approve=True,
        use_llm_scoring=False  # Use heuristics for faster testing
    )

    # Simulate manual staging (since we don't want to fetch real data in tests)
    # NOTE: These items are crafted to have unique content that won't match existing KB
    import time
    unique_id = str(time.time())

    test_items = [
        {
            "title": f"Unique AI Research Paper Test {unique_id}",
            "content": f"Comprehensive analysis of neural network architectures - unique test content {unique_id}. " * 50,
            "source_type": "research_paper",
            "authors": ["Dr. Test"],
            "categories": ["AI"],
            "published_date": "2026-01-10T00:00:00Z"
        },
        {
            "title": f"Short note {unique_id}",
            "content": f"Too short {unique_id}.",
            "source_type": "unknown"
        }
    ]

    # Add to staging manually
    count = pipeline.staging.add_to_staging(test_items, source="test")
    print(f"✓ Staged {count} items")

    # Filter
    filter_results = pipeline.filter_pending()
    print(f"✓ Filtering results:")
    print(f"  - Total: {filter_results['total']}")
    print(f"  - Significant: {filter_results['significant']}")
    print(f"  - Auto-approved: {filter_results['auto_approved']}")
    print(f"  - Needs review: {filter_results['needs_review']}")

    assert filter_results['total'] >= 1, "Should have processed items"
    assert filter_results['significant'] >= 1, "At least one item should be significant"

    print("✅ Full pipeline works correctly")
    return True


def test_scheduler():
    """Test scheduler functionality"""
    print("\n" + "=" * 70)
    print("TEST 5: Ingestion Scheduler")
    print("=" * 70)

    pipeline = IngestionPipeline(
        staging_dir="./staging/test",
        auto_approve=False,
        use_llm_scoring=False
    )

    scheduler = IngestionScheduler(pipeline)

    # Add test job (won't actually run, just testing configuration)
    scheduler.add_job(
        job_name="test_job",
        source_configs=[
            {
                "type": "test",
                "params": {}
            }
        ],
        cron_expression="0 * * * *"  # Every hour
    )

    # Check job was added
    jobs = scheduler.list_jobs()
    print(f"✓ Configured jobs: {len(jobs)}")
    assert len(jobs) >= 1, "Job should be configured"
    assert jobs[0]['name'] == 'test_job', "Job name should match"

    print(f"  - Job: {jobs[0]['name']}")
    print(f"  - Trigger: {jobs[0]['trigger']}")

    # Get stats
    stats = scheduler.get_stats()
    print(f"✓ Scheduler stats:")
    print(f"  - Running: {stats['scheduler_running']}")
    print(f"  - Jobs count: {stats['jobs_count']}")

    assert stats['jobs_count'] >= 1, "Should have at least one job"

    print("✅ Scheduler works correctly")
    return True


def run_all_tests():
    """Run all automation tests"""
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 15 + "AUTOMATED INGESTION PIPELINE TESTS" + " " * 19 + "║")
    print("╚" + "=" * 68 + "╝")

    tests = [
        ("Novelty Filtering", test_novelty_filtering),
        ("Heuristic Significance", test_significance_scoring_heuristic),
        ("LLM Significance", test_significance_scoring_llm),
        ("Full Pipeline", test_full_pipeline),
        ("Scheduler", test_scheduler)
    ]

    results = []
    for name, test_func in tests:
        try:
            success = test_func()
            results.append((name, "PASS" if success else "FAIL"))
        except Exception as e:
            print(f"\n❌ Test '{name}' failed with error: {e}")
            import traceback
            traceback.print_exc()
            results.append((name, "ERROR"))

    # Summary
    print("\n")
    print("╔" + "=" * 68 + "╗")
    print("║" + " " * 25 + "TEST SUMMARY" + " " * 31 + "║")
    print("╠" + "=" * 68 + "╣")

    for name, status in results:
        status_symbol = "✅" if status == "PASS" else ("⚠️ " if status == "SKIP" else "❌")
        print(f"║  {status_symbol} {name:40s} {status:20s}  ║")

    print("╚" + "=" * 68 + "╝")

    # Final result
    passed = sum(1 for _, s in results if s == "PASS")
    total = len(results)

    print(f"\n{'✅' if passed == total else '⚠️ '} {passed}/{total} tests passed\n")

    return passed == total


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
