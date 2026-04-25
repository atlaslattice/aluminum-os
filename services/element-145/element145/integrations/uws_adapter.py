"""UWS adapter for Element 145 (Phase-1 dry-run).

Maps ExecutionPlan.operations to UWS command envelopes without executing them.
"""
from __future__ import annotations

from typing import Any, List, Dict


def to_uws_envelopes(
    *,
    trace_id: str,
    operations: List[Dict[str, Any]],
    consent: Dict[str, Any],
    dry_run: bool = True,
) -> List[Dict[str, Any]]:
    envelopes: List[Dict[str, Any]] = []

    for op in operations:
        provider = op.get("provider", "local_stub")
        action = op.get("type", "read")

        envelope = {
            "provider": provider,
            "resource": op.get("resource", "generic"),
            "action": action,
            "args": op.get("args", {}),
            "dry_run": dry_run,
            "trace_id": trace_id,
            "consent": {
                "allowed": consent.get("allowed"),
                "destructive": consent.get("destructive"),
                "approval_token": consent.get("approval_token"),
            },
        }

        envelopes.append(envelope)

    return envelopes
