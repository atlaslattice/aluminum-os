"""
WISH #3: Learning Loop Logger
Every task outcome gets logged with structured metadata for pattern recognition.
The system learns from its own history.
"""
import json
import os
from datetime import datetime
from pathlib import Path

LOG_DIR = "/home/ubuntu/manus_wishlist/data/learning_logs"

class LearningLoop:
    def __init__(self):
        Path(LOG_DIR).mkdir(parents=True, exist_ok=True)
        self.log_file = os.path.join(LOG_DIR, f"loop_{datetime.now().strftime('%Y_%m')}.jsonl")

    def log_outcome(self, task: str, outcome: str, details: dict = None) -> dict:
        """Log a task outcome: success, failure, or partial."""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "task": task,
            "outcome": outcome,  # success | failure | partial
            "details": details or {},
            "learnings": []
        }
        if outcome == "failure":
            entry["learnings"].append(f"Task '{task}' failed. Review approach and try alternative.")
        elif outcome == "partial":
            entry["learnings"].append(f"Task '{task}' partially completed. Identify blocking step.")

        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def get_history(self, task_filter: str = None, limit: int = 50) -> list:
        """Retrieve task history, optionally filtered by task name."""
        entries = []
        for log_file in sorted(Path(LOG_DIR).glob("loop_*.jsonl"), reverse=True):
            with open(log_file) as f:
                for line in f:
                    entry = json.loads(line.strip())
                    if task_filter and task_filter.lower() not in entry["task"].lower():
                        continue
                    entries.append(entry)
                    if len(entries) >= limit:
                        return entries
        return entries

    def success_rate(self, task_filter: str = None) -> dict:
        """Calculate success rate for tasks."""
        history = self.get_history(task_filter=task_filter, limit=1000)
        if not history:
            return {"total": 0, "success_rate": 0.0}
        successes = sum(1 for e in history if e["outcome"] == "success")
        return {
            "total": len(history),
            "successes": successes,
            "failures": sum(1 for e in history if e["outcome"] == "failure"),
            "partial": sum(1 for e in history if e["outcome"] == "partial"),
            "success_rate": round(successes / len(history) * 100, 1)
        }

    def extract_patterns(self) -> list:
        """Identify recurring failure patterns."""
        history = self.get_history(limit=500)
        failures = [e for e in history if e["outcome"] == "failure"]
        patterns = {}
        for f in failures:
            key = f["task"].split(":")[0] if ":" in f["task"] else f["task"]
            patterns[key] = patterns.get(key, 0) + 1
        return sorted(patterns.items(), key=lambda x: x[1], reverse=True)


if __name__ == "__main__":
    loop = LearningLoop()
    loop.log_outcome("gmail_sync", "success", {"emails_fetched": 25, "entries_created": 15})
    loop.log_outcome("drive_sync", "success", {"files_modified": 0})
    loop.log_outcome("state_consolidation", "success", {"stale_entries": 35, "moved_to_deep_sleep": 35})
    loop.log_outcome("parallel_research", "failure", {"error": "All 15 subtasks failed", "approach": "map tool"})
    loop.log_outcome("notion_create", "success", {"pages_created": 3})
    loop.log_outcome("x_posting", "partial", {"reason": "Logged in but wrong account"})

    stats = loop.success_rate()
    print(f"Success rate: {stats['success_rate']}% ({stats['successes']}/{stats['total']})")
    patterns = loop.extract_patterns()
    print(f"Failure patterns: {patterns}")
    print("WISH #3: LEARNING LOOP LOGGER — OPERATIONAL")
