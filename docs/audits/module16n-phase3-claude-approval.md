# Module 16N Phase 3 — Claude / Scribe Approval Notes

**Status:** Approved to proceed  
**Branch:** `element145-copilot-phase1-reconcile`

---

## Phase 3 Scope

Proceed with:

1. CLI commands:
   - `bootstrap`
   - `checkpoint`
   - `artifact`
   - `flush-outbox`
2. Real outbox replay with kind-dispatched resend.
3. `/route` integration after TransparencyPacket creation.
4. Best-effort Notion write with outbox-backed recovery.

---

## Required Refinements

### A. Idempotency on `packet_id`

`log_transparency_packet()` must use `packet_id` as an idempotency key. If a packet already exists in Notion, skip duplicate creation.

This matters for outbox replay.

### B. TransparencyPacket schema alignment

Current runtime uses `TransparencyPacketV02`. Copilot's parallel governance pipeline reportedly ships a canonical schema in `element145/transparency/models.py` with:

- deterministic SHA-256 fingerprint;
- `verify()` method;
- `to_disclosure()` for audit-safe serialization.

Adopt or reconcile this schema in Phase 3 or Phase 3.5 once the artifact is available.

---

## Failure Modes To Document

- malformed queued packet: preserve in outbox and mark failed replay result;
- Notion unavailable for hours: queue accumulates, runtime continues, manual flush required;
- duplicate packet: skip write, return idempotent success;
- missing database/token: queue locally, do not crash core runtime.

---

## Canonical Boundary

Notion is the shared audit/persistence layer for parallel-pipelines architecture, not the kernel and not execution authority.
