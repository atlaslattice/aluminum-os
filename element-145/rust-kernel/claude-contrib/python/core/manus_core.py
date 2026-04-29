"""
Aluminum OS v3.0 — Manus Core Bridge (Ring 1)

Model routing, cost tracking, and memory management.
Honest about what requires external services vs what runs standalone.
"""

import hashlib
import json
import time
from dataclasses import dataclass, field
from typing import Optional, Dict, List, Any
from enum import Enum


# ============================================================
# MODEL ROUTER — Route tasks to cheapest capable model
# This is STANDALONE — no API keys needed for routing logic.
# Actual inference calls require API keys.
# ============================================================

class ModelTier(Enum):
    CHEAP = "cheap"        # ~$0.0002/1K tokens
    STANDARD = "standard"  # ~$0.002/1K tokens
    PREMIUM = "premium"    # ~$0.02/1K tokens


@dataclass
class ModelConfig:
    name: str
    tier: ModelTier
    cost_per_1k_input: float
    cost_per_1k_output: float
    max_context: int
    capabilities: list
    api_key_env: str  # env var name — NOT the actual key


# Real pricing as of March 2026
AVAILABLE_MODELS = [
    ModelConfig("deepseek-chat", ModelTier.CHEAP, 0.00014, 0.00028, 64000,
                ["text", "code", "math"], "DEEPSEEK_API_KEY"),
    ModelConfig("gemini-2.0-flash", ModelTier.CHEAP, 0.0001, 0.0004, 1000000,
                ["text", "code", "vision", "long_context"], "GEMINI_API_KEY"),
    ModelConfig("claude-3-5-haiku", ModelTier.STANDARD, 0.001, 0.005, 200000,
                ["text", "code"], "ANTHROPIC_API_KEY"),
    ModelConfig("gpt-4o-mini", ModelTier.STANDARD, 0.00015, 0.0006, 128000,
                ["text", "code", "vision"], "OPENAI_API_KEY"),
    ModelConfig("claude-sonnet-4", ModelTier.PREMIUM, 0.003, 0.015, 200000,
                ["text", "code", "vision", "reasoning"], "ANTHROPIC_API_KEY"),
    ModelConfig("gpt-4o", ModelTier.PREMIUM, 0.005, 0.015, 128000,
                ["text", "code", "vision", "reasoning"], "OPENAI_API_KEY"),
    ModelConfig("claude-opus-4", ModelTier.PREMIUM, 0.015, 0.075, 200000,
                ["text", "code", "vision", "reasoning"], "ANTHROPIC_API_KEY"),
]

# Keywords that indicate task complexity
COMPLEXITY_SIGNALS = {
    "simple": ["list", "count", "check", "status", "fetch", "get", "read", "format"],
    "medium": ["summarize", "classify", "extract", "convert", "filter", "translate"],
    "complex": ["analyze", "design", "architect", "research", "create", "write", "debug"],
    "reasoning": ["prove", "derive", "optimize", "strategy", "compare", "evaluate", "plan"],
}


class ModelRouter:
    """Routes tasks to the cheapest model that can handle them."""

    def __init__(self, models: list = None):
        self.models = models or AVAILABLE_MODELS

    def classify_complexity(self, task: str) -> str:
        """Determine task complexity from keywords."""
        task_lower = task.lower()
        for level in ["reasoning", "complex", "medium", "simple"]:
            for keyword in COMPLEXITY_SIGNALS[level]:
                if keyword in task_lower:
                    return level
        return "medium"  # default

    def required_tier(self, complexity: str) -> ModelTier:
        """Map complexity to minimum model tier."""
        return {
            "simple": ModelTier.CHEAP,
            "medium": ModelTier.STANDARD,
            "complex": ModelTier.PREMIUM,
            "reasoning": ModelTier.PREMIUM,
        }.get(complexity, ModelTier.STANDARD)

    def select_model(self, task: str, required_caps: list = None) -> Optional[ModelConfig]:
        """Select the cheapest model that meets task requirements."""
        complexity = self.classify_complexity(task)
        min_tier = self.required_tier(complexity)
        required_caps = required_caps or ["text"]

        candidates = []
        for model in self.models:
            # Must meet minimum tier
            tier_order = [ModelTier.CHEAP, ModelTier.STANDARD, ModelTier.PREMIUM]
            if tier_order.index(model.tier) < tier_order.index(min_tier):
                continue
            # Must have required capabilities
            if all(cap in model.capabilities for cap in required_caps):
                candidates.append(model)

        if not candidates:
            return None

        # Sort by input cost (cheapest first)
        candidates.sort(key=lambda m: m.cost_per_1k_input)
        return candidates[0]

    def estimate_cost(self, model: ModelConfig, input_tokens: int, output_tokens: int) -> float:
        """Estimate cost for a specific call."""
        return (input_tokens / 1000 * model.cost_per_1k_input +
                output_tokens / 1000 * model.cost_per_1k_output)


# ============================================================
# COST TRACKER — Real-time spend monitoring
# Standalone — stores everything in memory.
# ============================================================

@dataclass
class CostEntry:
    timestamp: float
    model: str
    input_tokens: int
    output_tokens: int
    cost_usd: float
    task_type: str


class CostTracker:
    """Track token usage and cost across all model calls."""

    def __init__(self):
        self.entries: List[CostEntry] = []
        self.session_start = time.time()

    def record(self, model: str, input_tokens: int, output_tokens: int,
               cost_usd: float, task_type: str = "unknown"):
        self.entries.append(CostEntry(
            timestamp=time.time(),
            model=model,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost_usd=cost_usd,
            task_type=task_type,
        ))

    def total_cost(self) -> float:
        return sum(e.cost_usd for e in self.entries)

    def total_tokens(self) -> dict:
        return {
            "input": sum(e.input_tokens for e in self.entries),
            "output": sum(e.output_tokens for e in self.entries),
            "total": sum(e.input_tokens + e.output_tokens for e in self.entries),
        }

    def cost_by_model(self) -> dict:
        by_model: Dict[str, float] = {}
        for e in self.entries:
            by_model[e.model] = by_model.get(e.model, 0) + e.cost_usd
        return by_model

    def cost_by_task_type(self) -> dict:
        by_type: Dict[str, float] = {}
        for e in self.entries:
            by_type[e.task_type] = by_type.get(e.task_type, 0) + e.cost_usd
        return by_type

    def summary(self) -> dict:
        elapsed = time.time() - self.session_start
        return {
            "total_cost_usd": round(self.total_cost(), 6),
            "total_calls": len(self.entries),
            "tokens": self.total_tokens(),
            "by_model": self.cost_by_model(),
            "by_task_type": self.cost_by_task_type(),
            "session_seconds": round(elapsed, 1),
        }


# ============================================================
# MEMORY STORE — Semantic memory with deduplication
# Uses simple TF-IDF-like similarity. No external DB required.
# ChromaDB is optional for production; this works standalone.
# ============================================================

@dataclass
class MemoryEntry:
    id: str
    content: str
    metadata: dict
    timestamp: float
    content_hash: str
    tokens: set = field(default_factory=set)


class MemoryStore:
    """In-memory semantic store with deduplication and similarity search.

    This is the standalone version. For production with large datasets,
    swap the backend to ChromaDB or Pinecone — the interface stays the same.
    """

    def __init__(self):
        self.entries: Dict[str, MemoryEntry] = {}

    def _hash(self, content: str) -> str:
        return hashlib.sha256(content.encode()).hexdigest()[:16]

    def _tokenize(self, text: str) -> set:
        """Simple whitespace tokenization with lowercasing."""
        return set(text.lower().split())

    def store(self, content: str, metadata: dict = None) -> str:
        """Store a memory. Returns ID. Deduplicates by content hash."""
        content_hash = self._hash(content)

        # Check for duplicate
        for entry in self.entries.values():
            if entry.content_hash == content_hash:
                return entry.id  # Already stored

        entry_id = f"mem_{content_hash}"
        self.entries[entry_id] = MemoryEntry(
            id=entry_id,
            content=content,
            metadata=metadata or {},
            timestamp=time.time(),
            content_hash=content_hash,
            tokens=self._tokenize(content),
        )
        return entry_id

    def recall(self, query: str, top_k: int = 5) -> list:
        """Recall memories similar to query using Jaccard similarity."""
        query_tokens = self._tokenize(query)
        if not query_tokens:
            return []

        scored = []
        for entry in self.entries.values():
            if not entry.tokens:
                continue
            intersection = query_tokens & entry.tokens
            union = query_tokens | entry.tokens
            similarity = len(intersection) / len(union) if union else 0
            if similarity > 0:
                scored.append((similarity, entry))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {"id": e.id, "content": e.content, "similarity": round(s, 3), "metadata": e.metadata}
            for s, e in scored[:top_k]
        ]

    def count(self) -> int:
        return len(self.entries)

    def delete(self, entry_id: str) -> bool:
        if entry_id in self.entries:
            del self.entries[entry_id]
            return True
        return False


# ============================================================
# TASK DECOMPOSER — Break goals into dependency graphs
# Standalone — pure logic, no external services.
# ============================================================

@dataclass
class SubTask:
    id: int
    name: str
    dependencies: list
    tool: str
    status: str = "pending"


class TaskDecomposer:
    """Break high-level goals into executable DAGs."""

    TEMPLATES = {
        "sync": [
            SubTask(1, "fetch_emails", [], "gmail"),
            SubTask(2, "classify_emails", [1], "llm"),
            SubTask(3, "create_notion_entries", [2], "notion"),
            SubTask(4, "scan_drive_changes", [], "drive"),
            SubTask(5, "update_notion_from_drive", [4], "notion"),
            SubTask(6, "consolidate_state", [3, 5], "notion"),
        ],
        "research": [
            SubTask(1, "search_sources", [], "web_search"),
            SubTask(2, "read_sources", [1], "web_fetch"),
            SubTask(3, "extract_findings", [2], "llm"),
            SubTask(4, "cross_reference", [3], "llm"),
            SubTask(5, "write_analysis", [4], "llm"),
            SubTask(6, "vault_to_drive", [5], "drive"),
        ],
        "deploy": [
            SubTask(1, "scaffold_project", [], "shell"),
            SubTask(2, "write_code", [1], "llm"),
            SubTask(3, "run_tests", [2], "shell"),
            SubTask(4, "fix_failures", [3], "llm"),
            SubTask(5, "build_artifact", [4], "shell"),
            SubTask(6, "deploy", [5], "shell"),
        ],
    }

    def decompose(self, goal: str) -> dict:
        """Match goal to a template or return generic decomposition."""
        goal_lower = goal.lower()
        for pattern, tasks in self.TEMPLATES.items():
            if pattern in goal_lower:
                return {
                    "goal": goal,
                    "template": pattern,
                    "tasks": [
                        {"id": t.id, "name": t.name, "deps": t.dependencies,
                         "tool": t.tool, "status": t.status}
                        for t in tasks
                    ],
                    "parallel_groups": self._find_parallel_groups(tasks),
                }

        # Generic: single sequential task
        return {
            "goal": goal,
            "template": "generic",
            "tasks": [{"id": 1, "name": "execute_goal", "deps": [], "tool": "llm", "status": "pending"}],
            "parallel_groups": [[1]],
        }

    def _find_parallel_groups(self, tasks: list) -> list:
        """Group tasks that can execute in parallel (same dependency depth)."""
        groups = []
        completed = set()
        remaining = list(tasks)

        while remaining:
            # Tasks whose deps are all completed
            ready = [t for t in remaining if all(d in completed for d in t.dependencies)]
            if not ready:
                break  # Circular dependency guard
            groups.append([t.id for t in ready])
            completed.update(t.id for t in ready)
            remaining = [t for t in remaining if t.id not in completed]

        return groups


# ============================================================
# SESSION STATE — Serialize/restore working state
# ============================================================

class SessionVault:
    """Save and restore session state as JSON."""

    def __init__(self):
        self.state: Dict[str, Any] = {}

    def set(self, key: str, value: Any):
        self.state[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self.state.get(key, default)

    def serialize(self) -> str:
        """Export state to JSON string."""
        return json.dumps(self.state, indent=2, default=str)

    def restore(self, data: str) -> bool:
        """Restore state from JSON string."""
        try:
            self.state = json.loads(data)
            return True
        except (json.JSONDecodeError, TypeError):
            return False

    def keys(self) -> list:
        return list(self.state.keys())
