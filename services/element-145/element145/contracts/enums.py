"""Element 145 / Aluminum OS contract enums.

These enums define the minimal runtime vocabulary for the Aluminum OS
system-call layer. They are intentionally small, stable, and serializable.
"""
from __future__ import annotations

from enum import Enum


class EpistemicState(str, Enum):
    """Confidence / knowledge state for a routing decision."""

    KNOWN = "known"
    ESTIMATED = "estimated"
    SPECULATIVE = "speculative"
    UNKNOWN = "unknown"
    CONTESTED = "contested"


class SafetyState(str, Enum):
    """Safety / governance classification for a request."""

    SAFE = "safe"
    SENSITIVE = "sensitive"
    DANGEROUS = "dangerous"
    CONSTITUTIONAL = "constitutional"


class SelectedPath(str, Enum):
    """Execution path selected by the router."""

    FAST = "fast"
    DEEP = "deep"
    HUMAN_REVIEW = "human_review"
    BLOCKED = "blocked"
    SIMULATION = "simulation"
    SHADOW = "shadow"


class BudgetTier(str, Enum):
    """Budget / power-management tier for routing."""

    T0_BLOCKED = "t0_blocked"
    T1_LOCAL_CACHE = "t1_local_cache"
    T2_FAST_LOW_COST = "t2_fast_low_cost"
    T3_STANDARD = "t3_standard"
    T4_DEEP_COUNCIL = "t4_deep_council"
    T5_HUMAN_REVIEW = "t5_human_review"


class ActionType(str, Enum):
    """High-level action categories used by ConsentKernel."""

    READ = "read"
    WRITE = "write"
    SEND = "send"
    DELETE = "delete"
    EXECUTE_CODE = "execute_code"
    MODIFY_CONSTITUTION = "modify_constitution"
    MODIFY_ROUTING = "modify_routing"
    MODIFY_PROVENANCE = "modify_provenance"
    MODIFY_BUDGET = "modify_budget"
    ACCESS_CREDENTIALS = "access_credentials"
    SUBMIT_PUBLIC = "submit_public"
