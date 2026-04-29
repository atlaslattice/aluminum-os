#!/usr/bin/env python3
"""
Ingestion Scheduler
Runs periodic data fetches from external sources

Features:
- Cron-based scheduling
- Multiple concurrent sources
- Error handling & retry
- Stats tracking
"""

import os
import sys
import time
from datetime import datetime
from typing import Dict, List, Any
from pathlib import Path

import structlog
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger

# Add parent directory for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.ingestion.ingestion_pipeline import IngestionPipeline

logger = structlog.get_logger()


class IngestionScheduler:
    """
    Manages scheduled ingestion jobs

    Supports:
    - Cron-based scheduling
    - Multiple concurrent sources
    - Error handling & retry
    - Stats tracking
    """

    def __init__(self, pipeline: IngestionPipeline = None):
        self.pipeline = pipeline or IngestionPipeline(
            auto_approve=True,
            use_llm_scoring=True
        )
        self.scheduler = BackgroundScheduler(
            daemon=True,
            job_defaults={
                'coalesce': True,  # Combine missed runs
                'max_instances': 1,  # Only one instance per job
                'misfire_grace_time': 3600  # 1 hour grace
            }
        )
        self.job_stats = {}

        logger.info("ingestion_scheduler_initialized")

    def add_job(self,
                job_name: str,
                source_configs: List[Dict],
                cron_expression: str):
        """
        Add scheduled ingestion job

        Args:
            job_name: Unique job identifier
            source_configs: List of source configurations
            cron_expression: Cron schedule (e.g., "0 */6 * * *" = every 6 hours)

        Example:
            scheduler.add_job(
                "arxiv_daily",
                [{"type": "arxiv", "params": {"category": "cs.AI"}}],
                "0 6 * * *"  # Daily at 6 AM
            )
        """
        trigger = CronTrigger.from_crontab(cron_expression)

        self.scheduler.add_job(
            func=self._run_ingestion_job,
            trigger=trigger,
            args=[job_name, source_configs],
            id=job_name,
            name=job_name,
            replace_existing=True
        )

        logger.info("ingestion_job_scheduled",
                   job_name=job_name,
                   cron=cron_expression,
                   sources=[c.get('type') for c in source_configs])

    def _run_ingestion_job(self, job_name: str, source_configs: List[Dict]):
        """Execute ingestion job"""
        start_time = time.time()

        logger.info("ingestion_job_started", job=job_name)

        try:
            # Fetch and stage
            fetch_results = self.pipeline.fetch_and_stage(source_configs)

            # Filter by novelty & significance
            filter_results = self.pipeline.filter_pending()

            # Ingest approved items
            ingest_results = self.pipeline.ingest_approved()

            # Track stats
            duration = time.time() - start_time
            self.job_stats[job_name] = {
                "last_run": datetime.now().isoformat(),
                "duration_seconds": round(duration, 2),
                "fetched": sum(fetch_results.values()),
                "filtered": filter_results,
                "ingested": ingest_results.get("total_ingested", 0),
                "status": "success"
            }

            logger.info("ingestion_job_completed",
                       job=job_name,
                       duration=duration,
                       fetched=sum(fetch_results.values()),
                       ingested=ingest_results.get("total_ingested", 0))

        except Exception as e:
            duration = time.time() - start_time
            logger.error("ingestion_job_failed",
                        job=job_name,
                        error=str(e))

            self.job_stats[job_name] = {
                "last_run": datetime.now().isoformat(),
                "duration_seconds": round(duration, 2),
                "status": "failed",
                "error": str(e)
            }

    def trigger_job_manual(self, job_name: str):
        """Manually trigger a job to run immediately"""
        job = self.scheduler.get_job(job_name)
        if not job:
            raise ValueError(f"Job '{job_name}' not found")

        # Trigger immediately
        job.modify(next_run_time=datetime.now())
        logger.info("job_triggered_manually", job=job_name)

    def remove_job(self, job_name: str):
        """Remove a scheduled job"""
        self.scheduler.remove_job(job_name)
        logger.info("job_removed", job=job_name)

    def list_jobs(self) -> List[Dict]:
        """Get list of all scheduled jobs"""
        jobs = []
        for job in self.scheduler.get_jobs():
            # Get next run time safely
            try:
                next_run = job.next_run_time
                next_run_str = next_run.isoformat() if next_run else None
            except AttributeError:
                # APScheduler 4.x compatibility
                next_run_str = None

            jobs.append({
                "name": job.name,
                "id": job.id,
                "next_run": next_run_str,
                "trigger": str(job.trigger)
            })
        return jobs

    def start(self):
        """Start scheduler"""
        if not self.scheduler.running:
            self.scheduler.start()
            logger.info("ingestion_scheduler_started",
                       jobs_count=len(self.scheduler.get_jobs()))

    def stop(self):
        """Stop scheduler"""
        if self.scheduler.running:
            self.scheduler.shutdown(wait=False)
            logger.info("ingestion_scheduler_stopped")

    def get_stats(self) -> Dict:
        """Get job statistics"""
        return {
            "scheduler_running": self.scheduler.running,
            "jobs_count": len(self.scheduler.get_jobs()),
            "jobs": self.list_jobs(),
            "job_stats": self.job_stats
        }


def create_default_scheduler() -> IngestionScheduler:
    """
    Create scheduler with default jobs

    Default jobs:
    - ArXiv AI papers (daily at 6 AM)
    - RSS feeds (every 6 hours)

    Configure via environment variables:
    - ARXIV_SCHEDULE (default: "0 6 * * *")
    - RSS_SCHEDULE (default: "0 */6 * * *")
    - ENABLE_ARXIV_JOB (default: "true")
    - ENABLE_RSS_JOB (default: "false")
    """
    pipeline = IngestionPipeline(
        auto_approve=True,
        use_llm_scoring=True
    )

    scheduler = IngestionScheduler(pipeline)

    # Job 1: ArXiv papers (daily at 6 AM by default)
    if os.getenv("ENABLE_ARXIV_JOB", "true").lower() == "true":
        arxiv_schedule = os.getenv("ARXIV_SCHEDULE", "0 6 * * *")
        arxiv_category = os.getenv("ARXIV_CATEGORY", "cs.AI")

        scheduler.add_job(
            job_name="arxiv_daily",
            source_configs=[
                {
                    "type": "arxiv",
                    "params": {
                        "category": arxiv_category,
                        "max_results": 20,
                        "days_back": 1
                    }
                }
            ],
            cron_expression=arxiv_schedule
        )
        logger.info("arxiv_job_configured",
                   schedule=arxiv_schedule,
                   category=arxiv_category)

    # Job 2: RSS feeds (every 6 hours by default)
    if os.getenv("ENABLE_RSS_JOB", "false").lower() == "true":
        rss_schedule = os.getenv("RSS_SCHEDULE", "0 */6 * * *")
        rss_feeds = os.getenv("RSS_FEED_URLS", "").split(",")

        if rss_feeds and rss_feeds[0]:  # Only if feeds configured
            scheduler.add_job(
                job_name="rss_feeds",
                source_configs=[
                    {
                        "type": "rss",
                        "params": {
                            "feed_urls": rss_feeds,
                            "max_results": 10
                        }
                    }
                ],
                cron_expression=rss_schedule
            )
            logger.info("rss_job_configured",
                       schedule=rss_schedule,
                       feeds_count=len(rss_feeds))

    return scheduler


# CLI for testing
if __name__ == "__main__":
    import json

    print("=" * 70)
    print("INGESTION SCHEDULER TEST")
    print("=" * 70)
    print()

    # Create scheduler
    scheduler = create_default_scheduler()

    # Show configured jobs
    print("Configured jobs:")
    for job in scheduler.list_jobs():
        print(f"  - {job['name']}: {job['trigger']}")
        print(f"    Next run: {job['next_run']}")
    print()

    # Start scheduler
    print("Starting scheduler...")
    scheduler.start()
    print("Scheduler running:", scheduler.scheduler.running)
    print()

    # Show stats
    stats = scheduler.get_stats()
    print("Stats:", json.dumps(stats, indent=2))
    print()

    print("Scheduler is running in background.")
    print("Press Ctrl+C to stop...")

    try:
        while True:
            time.sleep(60)
    except KeyboardInterrupt:
        print("\nStopping scheduler...")
        scheduler.stop()
        print("Stopped.")
