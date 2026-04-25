"""ConsentKernel (fail-closed) for Element 145 / Aluminum OS.

This is the enforcement point for destructive actions. It is intentionally
minimal for Phase-1 but wired to the contract layer shape.
"""
from __future__ import annotations

import time
from typing import Any

from element145.contracts import ConsentDecision, ActionType


DESTRUCTIVE_ACTIONS = {
    ActionType.DELETE.value,
    ActionType.EXECUTE_CODE.value,
    ActionType.MODIFY_CONSTITUTION.value,
    ActionType.MODIFY_ROUTING.value,
    ActionType.MODIFY_PROVENANCE.value,
    ActionType.MODIFY_BUDGET.value,
    ActionType.ACCESS_CREDENTIALS.value,
    ActionType.SUBMIT_PUBLIC.value,
}


class ConsentKernel:
    def __init__(self) -> None:
        # future: approval store / HITL integration
        self._approvals: dict[str, dict[str, Any]] = {}

    def register_approval(self, token: str, ttl_s: int = 300) -> None:
        self._approvals[token] = {"exp": time.time() + ttl_s}

    def _is_valid_approval(self, token: str | None) -> bool:
        if not token or token not in self._approvals:
            return False
        entry = self._approvals[token]
        return time.time() < float(entry["exp"])

    def decide(
        self,
        trace_id: str,
        action_type: str,
        approval_token: str | None = None,
    ) -> ConsentDecision:
        destructive = action_type in DESTRUCTIVE_ACTIONS

        if destructive:
            if self._is_valid_approval(approval_token):
                return ConsentDecision(
                    trace_id=trace_id,
                    action_type=action_type,
                    destructive=True,
                    allowed=True,
                    reason="approved",
                    approval_token=approval_token,
                )
            return ConsentDecision(
                trace_id=trace_id,
                action_type=action_type,
                destructive=True,
                allowed=False,
                reason="missing_or_invalid_approval",
                approval_token=None,
            )

        return ConsentDecision(
            trace_id=trace_id,
            action_type=action_type,
            destructive=False,
            allowed=True,
            reason="non_destructive",
            approval_token=None,
        )
