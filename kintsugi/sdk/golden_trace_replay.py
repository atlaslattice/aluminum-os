"""Candidate-only GoldenTrace v1 hash-chain replay and claim review.

Source-compatible with existing kintsugi/sdk/golden_trace.py emitter's
sha3-256(sorted JSON fields excluding `integrity`) algorithm. A local checksum
is never an identity proof, provider permission, CANON gate, or deployment.
Zero external network/model/account calls. Uses Python standard library only.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any
from uuid import UUID

HEX64 = re.compile(r"^[a-f0-9]{64}$")
SPHERE = re.compile(r"^(H[0-9]{1,2}\.S[0-9]{1,3}|S[0-9]{1,3})$")
LAYERS = frozenset({"L1-Constitutional", "L2-Kernel", "L3-Engine", "L4-Service", "L5-Extension"})
TYPES = frozenset({
    "action", "failure", "repair", "golden_seam", "invariant_check", "invariant_violation",
    "consent_granted", "consent_denied", "council_vote", "council_consensus", "council_dissent",
    "model_route", "model_fallback", "query", "ingestion", "classification",
    "amendment_proposed", "amendment_enacted", "ghost_seat_invoked", "human_override",
})
REQUIRED = frozenset({"trace_id", "timestamp", "source", "event_type", "sphere_tag",
                      "aluminum_layer", "payload", "integrity"})
ALLOW_EVIDENCE = frozenset({"SOURCE_LINKED", "REPRODUCED", "CALIBRATED", "VALIDATED"})
# Reviewable is not ratified, published, hosted, or permission to act.
ALLOW_CANDIDATE_STATUS = frozenset({"CANDIDATE", "DRAFT", "PREPARED", "SOURCE_LINKED", "HELD_REVIEW"})


def _err(index: int, code: str) -> dict[str, Any]:
    """Never echo potentially private payloads or full file paths."""
    return {"index": index, "code": code}


def verify_trace_chain(events: Any, *, max_events: int = 10000) -> dict[str, Any]:
    """Pure, non-mutating local verification of historical GoldenTrace emitter format.

    Valid SHA3 links prove only that the supplied records have internally
    consistent local digests. They do not prove source completeness, signatures,
    actor identity, receipt durability, authorization, or semantic correctness.
    """
    # This is a public helper: a malformed caller-supplied budget must HOLD,
    # never raise TypeError at len(events) > max_events or unlock an unbounded scan.
    if type(max_events) is not int or not 1 <= max_events <= 10_000:
        return {"status": "HELD_INVALID", "count": 0,
                "errors": [_err(-1, "invalid_event_budget")],
                "authority_effect": "NONE", "signed_identity": "UNVERIFIED"}
    failures: list[dict[str, Any]] = []
    if type(events) is not list:
        return {"status": "HELD_INVALID", "count": 0, "errors": [_err(-1, "events_not_list")],
                "authority_effect": "NONE", "signed_identity": "UNVERIFIED"}
    if not events:
        failures.append(_err(-1, "empty_trace_no_evidence"))
    if len(events) > max_events:
        failures.append(_err(-1, "event_budget_exceeded"))
    seen: set[str] = set()
    previous_hash: str | None = None
    for index, event in enumerate(events[:max_events]):
        if type(event) is not dict:
            failures.append(_err(index, "event_not_object"))
            previous_hash = None
            continue
        missing = REQUIRED - set(event)
        if missing:
            failures.append(_err(index, "required_fields_missing"))
        trace_id = event.get("trace_id")
        try:
            if type(trace_id) is not str:
                raise ValueError("not a string")
            UUID(trace_id)
        except (ValueError, TypeError, AttributeError):
            failures.append(_err(index, "invalid_trace_id"))
        if type(trace_id) is str:
            if trace_id in seen:
                failures.append(_err(index, "duplicate_trace_id"))
            seen.add(trace_id)
        timestamp = event.get("timestamp")
        try:
            if type(timestamp) is not str:
                raise ValueError("not a string")
            when = datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
            if when.tzinfo is None or when.utcoffset() is None:
                raise ValueError("naive timestamp")
        except (ValueError, TypeError, AttributeError):
            failures.append(_err(index, "timestamp_not_offset_aware"))
        src = event.get("source")
        if type(src) is not dict or any(type(src.get(f)) is not str or not src.get(f).strip() for f in ("repo", "module")) or type(src.get("function")) is not str:
            failures.append(_err(index, "source_shape_invalid"))
        if type(event.get("event_type")) is not str or event.get("event_type") not in TYPES:
            failures.append(_err(index, "invalid_event_type"))
        if type(event.get("sphere_tag")) is not str or not SPHERE.fullmatch(event["sphere_tag"]):
            failures.append(_err(index, "invalid_sphere_tag"))
        if type(event.get("aluminum_layer")) is not str or event.get("aluminum_layer") not in LAYERS:
            failures.append(_err(index, "invalid_layer"))
        if type(event.get("payload")) is not dict:
            failures.append(_err(index, "invalid_payload_shape"))
        integrity = event.get("integrity")
        if type(integrity) is not dict:
            failures.append(_err(index, "integrity_missing_or_invalid"))
            previous_hash = None
            continue
        if integrity.get("hash_algorithm") != "sha3-256":
            failures.append(_err(index, "unsupported_hash_algorithm"))
        claimed_hash = integrity.get("hash")
        if type(claimed_hash) is not str or not HEX64.fullmatch(claimed_hash):
            failures.append(_err(index, "invalid_hash_format"))
            previous_hash = None
            continue
        link = integrity.get("previous_trace_hash")
        expected_link = "GENESIS" if index == 0 else previous_hash
        if expected_link is None or link != expected_link:
            failures.append(_err(index, "broken_previous_link"))
        if "signature" in integrity:
            # Signature is unverified, never evidence of actor identity.
            if type(integrity["signature"]) is not str:
                failures.append(_err(index, "invalid_signature_field"))
        to_hash = {k: v for k, v in event.items() if k != "integrity"}
        try:
            body = json.dumps(to_hash, sort_keys=True, allow_nan=False).encode("utf-8")
            actual_hash = hashlib.sha3_256(body).hexdigest()
            if actual_hash != claimed_hash:
                failures.append(_err(index, "hash_mismatch"))
        except (TypeError, ValueError, OverflowError, RecursionError):
            failures.append(_err(index, "unhashable_or_nonfinite_body"))
        previous_hash = claimed_hash
    return {
        "status": "LOCAL_HASH_CHAIN_VALID_NOT_AUTHORITY" if not failures else "HELD_INVALID",
        "count": len(events),
        "errors": failures,
        "hash_algorithm": "sha3-256",
        "authority_effect": "NONE",
        "signed_identity": "UNVERIFIED",
        "source_completeness": "UNVERIFIED",
        "hosted": False,
    }


def review_claim_packet(packet: Any) -> dict[str, Any]:
    """Separate advisory claim/evidence review from hash integrity.

    Never returns RATIFIED, CANON, DEPLOYED or authorized action. Only
    source pointers are considered; no content or private bodies are copied.
    """
    problems: list[str] = []
    if type(packet) is not dict:
        problems.append("packet_not_object")
        packet = {}
    for field in ("claim_id", "statement_id", "source_revision", "review_lane"):
        if type(packet.get(field)) is not str or not packet[field].strip():
            problems.append(field + "_missing")
    for field in ("source_refs", "evidence_refs", "receipt_refs"):
        values = packet.get(field)
        if type(values) is not list or not values or any(type(v) is not str or not v.strip() for v in values):
            problems.append(field + "_missing_or_invalid")
    if packet.get("rights_status") != "AUTHORIZED_WORK_METADATA":
        problems.append("rights_not_verified")
    if type(packet.get("evidence_status")) is not str or packet.get("evidence_status") not in ALLOW_EVIDENCE:
        problems.append("evidence_status_unverified")
    # A missing historical v1 field is tolerated as advisory only; an
    # EXPLICIT null is ambiguous, not an affirmative declaration of NONE.
    if "authority" in packet and packet["authority"] != "NONE":
        problems.append("authority_requested")
    # Fail closed on ambiguous/falsy non-boolean flags (0, null, strings, etc.).
    # A missing flag retains v1 candidate compatibility, never host acceptance.
    status = packet.get("status")
    if (type(status) is not str or status not in ALLOW_CANDIDATE_STATUS
            or ("deployment" in packet and packet["deployment"] is not False)):
        problems.append("promotion_requires_external_gate")
    # Do not equate an explicitly null/false scope with the legacy absent
    # field; either ambiguous value is held before advisory review.
    if "private_mode" in packet and packet["private_mode"] != "NONE":
        problems.append("private_scope_not_work")
    if "revoked" in packet and packet["revoked"] is not False:
        problems.append("source_revoked")
    return {
        "status": "CANDIDATE_REVIEWABLE_NOT_APPROVED" if not problems else "HELD_REVIEW",
        "reasons": list(dict.fromkeys(problems)),
        "authority_effect": "NONE", "deployment": False, "semantic_acceptance": False,
    }


def _unique_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    """Refuse ambiguous repeated keys, including Unicode-escaped equivalents."""
    obj: dict[str, Any] = {}
    for key, value in pairs:
        if key in obj:
            raise ValueError("duplicate JSON key")
        obj[key] = value
    return obj


def _reject_nonfinite_json(_token: str) -> None:
    raise ValueError("nonfinite JSON numeric token")


def main(argv: list[str] | None = None) -> int:
    args = sys.argv[1:] if argv is None else argv
    if len(args) != 1:
        print("Usage: python kintsugi/sdk/golden_trace_replay.py path/to/trace.json", file=sys.stderr)
        return 2
    try:
        # This is an explicitly selected local file, not a provider fetch.
        path = Path(args[0])
        if not path.is_file() or path.stat().st_size > 4_000_000:
            raise ValueError("missing, unsupported, or oversized file")
        events = json.loads(path.read_text(encoding="utf-8"),
                            object_pairs_hook=_unique_json_object,
                            parse_constant=_reject_nonfinite_json)
        report = verify_trace_chain(events)
    except (OSError, UnicodeError, ValueError, json.JSONDecodeError):
        report = {"status": "HELD_INVALID", "count": 0,
                  "errors": [_err(-1, "local_input_unreadable")], "authority_effect": "NONE"}
    print(json.dumps(report, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] == "LOCAL_HASH_CHAIN_VALID_NOT_AUTHORITY" else 1


if __name__ == "__main__":
    raise SystemExit(main())