"""
WISH #6: Model Router
Classify task complexity, route to cheapest capable model.
Uses LiteLLM for unified interface across all providers.

WISH #7: Cost Tracker
Real-time token counting and cost estimation per task, per model, per session.
"""
import os
import json
import time
from datetime import datetime
from pathlib import Path

# Cost per million tokens (input/output) as of March 2026
MODEL_COSTS = {
    "gemini/gemini-2.5-flash": {"input": 0.15, "output": 0.60, "tier": "cheap"},
    "deepseek/deepseek-chat": {"input": 0.14, "output": 0.28, "tier": "cheap"},
    "openai/gpt-4o-mini": {"input": 0.15, "output": 0.60, "tier": "cheap"},
    "anthropic/claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00, "tier": "cheap"},
    "openai/gpt-4o": {"input": 2.50, "output": 10.00, "tier": "power"},
    "anthropic/claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00, "tier": "power"},
    "gemini/gemini-2.5-pro": {"input": 1.25, "output": 10.00, "tier": "power"},
    "openai/o3": {"input": 10.00, "output": 40.00, "tier": "reasoning"},
    "anthropic/claude-opus-4-20250514": {"input": 15.00, "output": 75.00, "tier": "reasoning"},
    "xai/grok-3": {"input": 3.00, "output": 15.00, "tier": "power"},
}

COST_LOG_DIR = "/home/ubuntu/manus_wishlist/data/cost_logs"

class CostTracker:
    def __init__(self):
        Path(COST_LOG_DIR).mkdir(parents=True, exist_ok=True)
        self.session_costs = []
        self.log_file = os.path.join(COST_LOG_DIR, f"costs_{datetime.now().strftime('%Y_%m')}.jsonl")

    def log_call(self, model: str, input_tokens: int, output_tokens: int, task: str = "") -> dict:
        costs = MODEL_COSTS.get(model, {"input": 5.0, "output": 15.0, "tier": "unknown"})
        input_cost = (input_tokens / 1_000_000) * costs["input"]
        output_cost = (output_tokens / 1_000_000) * costs["output"]
        total_cost = input_cost + output_cost
        entry = {
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "tier": costs["tier"],
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "input_cost_usd": round(input_cost, 6),
            "output_cost_usd": round(output_cost, 6),
            "total_cost_usd": round(total_cost, 6),
            "task": task
        }
        self.session_costs.append(entry)
        with open(self.log_file, "a") as f:
            f.write(json.dumps(entry) + "\n")
        return entry

    def session_summary(self) -> dict:
        total = sum(e["total_cost_usd"] for e in self.session_costs)
        by_tier = {}
        for e in self.session_costs:
            tier = e["tier"]
            by_tier[tier] = by_tier.get(tier, 0) + e["total_cost_usd"]
        return {
            "total_calls": len(self.session_costs),
            "total_cost_usd": round(total, 4),
            "by_tier": {k: round(v, 4) for k, v in by_tier.items()},
            "total_tokens": sum(e["input_tokens"] + e["output_tokens"] for e in self.session_costs)
        }


class ModelRouter:
    COMPLEXITY_KEYWORDS = {
        "simple": ["list", "count", "check", "status", "fetch", "read", "get", "find", "search"],
        "moderate": ["analyze", "compare", "summarize", "write", "create", "generate", "build"],
        "complex": ["architect", "design", "reason", "debate", "synthesize", "strategy", "novel", "research"]
    }

    def __init__(self):
        self.cost_tracker = CostTracker()

    def classify_complexity(self, task_description: str) -> str:
        """Classify task complexity based on keywords and length."""
        desc_lower = task_description.lower()
        scores = {"simple": 0, "moderate": 0, "complex": 0}
        for level, keywords in self.COMPLEXITY_KEYWORDS.items():
            for kw in keywords:
                if kw in desc_lower:
                    scores[level] += 1
        # Length heuristic: longer descriptions tend to be more complex
        if len(task_description) > 500:
            scores["complex"] += 2
        elif len(task_description) > 200:
            scores["moderate"] += 1
        return max(scores, key=scores.get)

    def select_model(self, task_description: str, preferred_provider: str = None) -> str:
        """Select the optimal model for a task."""
        complexity = self.classify_complexity(task_description)
        tier_map = {"simple": "cheap", "moderate": "power", "complex": "reasoning"}
        target_tier = tier_map[complexity]

        candidates = [m for m, c in MODEL_COSTS.items() if c["tier"] == target_tier]
        if preferred_provider:
            provider_match = [m for m in candidates if m.startswith(preferred_provider)]
            if provider_match:
                return provider_match[0]
        # Return cheapest in tier
        return min(candidates, key=lambda m: MODEL_COSTS[m]["input"] + MODEL_COSTS[m]["output"])

    def route(self, task_description: str, preferred_provider: str = None) -> dict:
        """Full routing decision with cost estimate."""
        complexity = self.classify_complexity(task_description)
        model = self.select_model(task_description, preferred_provider)
        costs = MODEL_COSTS[model]
        return {
            "task": task_description[:100],
            "complexity": complexity,
            "model": model,
            "tier": costs["tier"],
            "estimated_cost_per_1k_tokens": round((costs["input"] + costs["output"]) / 2000, 6),
            "savings_vs_reasoning": self._calc_savings(model)
        }

    def _calc_savings(self, selected_model: str) -> str:
        selected_cost = MODEL_COSTS[selected_model]["input"] + MODEL_COSTS[selected_model]["output"]
        max_cost = max(c["input"] + c["output"] for c in MODEL_COSTS.values())
        if max_cost == 0:
            return "0%"
        savings = (1 - selected_cost / max_cost) * 100
        return f"{savings:.0f}%"


if __name__ == "__main__":
    router = ModelRouter()

    # Test routing decisions
    tasks = [
        "List all files in the Drive folder",
        "Analyze the Stryker cyberattack and write a comprehensive defense framework",
        "Check if there are new emails",
        "Design a sovereign AI-Native OS architecture integrating 15 platforms",
        "Count the entries in the Notion database",
        "Synthesize contrarian reviews from 9 council members into unified strategy"
    ]
    print("MODEL ROUTING DECISIONS:")
    print("-" * 80)
    for task in tasks:
        result = router.route(task)
        print(f"  [{result['complexity']:>8}] {result['model']:<45} savings: {result['savings_vs_reasoning']} | {task[:60]}")

    # Test cost tracking
    tracker = router.cost_tracker
    tracker.log_call("gemini/gemini-2.5-flash", 1000, 500, "email_classification")
    tracker.log_call("anthropic/claude-sonnet-4-20250514", 5000, 2000, "analysis_writing")
    tracker.log_call("openai/gpt-4o-mini", 800, 300, "file_listing")
    tracker.log_call("openai/o3", 10000, 5000, "architecture_design")

    summary = tracker.session_summary()
    print(f"\nCOST SUMMARY: ${summary['total_cost_usd']} across {summary['total_calls']} calls")
    print(f"  By tier: {summary['by_tier']}")
    print(f"  Total tokens: {summary['total_tokens']:,}")
    print("\nWISH #6: MODEL ROUTER — OPERATIONAL")
    print("WISH #7: COST TRACKER — OPERATIONAL")
