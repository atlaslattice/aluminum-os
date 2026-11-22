# GoldenTrace Provenance Kernel — Candidate v1.1 contract

**Status:** CANDIDATE / SOURCE-ONLY / NOT CANON / NOT HOSTED. **Authority:** NONE. **Scope:** [Aluminum OS issue #10](https://github.com/atlaslattice/aluminum-os/issues/10). This specification extends, and does not overwrite, the earlier `kintsugi/spec/golden_trace_v1.json` schema and `kintsugi/sdk/golden_trace.py` emitter. Earlier bytes, disagreements, and receipts are retained.

## 1. Three independent evidence questions

1. **Integrity:** does the provided trace sequence maintain the documented hash chain? Verifiable with a local byte-compatible rehash, but a valid hash never establishes truthful content.
2. **Provenance:** did the claimed source actually generate it, under which source revision, rights, timestamp, and signed principal? Requires separately trusted source or host attestations. A self-declared `source.repo`, SHA, signature-looking string, or model identity is not authentication.
3. **Authority and outcomes:** is the decision authorized and is an implementation actually deployed and measured? Requires separate human-root and service-level receipts; JSON or GitHub status cannot grant approval.

These three questions have independent statuses. `LOCAL_HASH_CHAIN_VALID_NOT_AUTHORITY` is intentionally **not** `HOSTED_VERIFIED`, `CANON`, `DEPLOYED`, or `SOURCE_REPRODUCED`.

## 2. Trace event and hash compatibility

Legacy event fields: `trace_id` (UUID), UTC offset-aware `timestamp`, `source` (`repo`, `module`, `function`), `event_type` (legacy enumeration), `sphere_tag`, `aluminum_layer`, `payload`, `severity`, and `integrity` (`hash_algorithm`, `hash`, `previous_trace_hash`). The replay helper supports the existing emitter's SHA3-256 of Python `json.dumps(event_without_integrity, sort_keys=True).encode('utf-8')`, whose serialization is **not** RFC 8785/JCS. The genesis pointer is `GENESIS`; each successor links to the predecessor's asserted digest. The helper independently recomputes it and fails closed on mismatch, type errors, duplicate IDs, nonfinite JSON, or missing links.

`ml-dsa-87` and `fn-dsa-512` named in the historical JSON Schema are not SHA-3 content-hash algorithms; the replay helper supports SHA3-256 digests only and **does not verify PQC signatures**. Do not confuse an optional signature field with authenticated attribution. No local clock or source-root index proves that an event actually occurred.

## 3. Claim and evidence relationship

An independently reviewable candidate claim uses separate pointers: `claim_id`, `statement_id`, `source_revision`, `source_refs[]`, `evidence_refs[]`, `receipt_refs[]`, `evidence_status`, `rights_status`, `review_lane`, `authority`, `status`, and `deployment`. All cross-links must be dereferenced under independently authenticated rights at read and return, before any user-facing release. Every evidence citation carries source version, measured event date (distinct from publication date), method, uncertainty, and if applicable experiment identity so multiple papers from one experiment are not counted as independent replications.

`review_claim_packet()` checks structural candidate completeness and produces either `CANDIDATE_REVIEWABLE_NOT_APPROVED` or `HELD_REVIEW`; it never approves semantics, ratifies CANON, or performs external actions. Missing receipt, missing rights, revoked scope, private-mode input, or claimed authority/deployment is a hold.

## 4. Receipt and outcome lifecycle

| Stage | Minimum evidence | What is **not** implied |
| --- | --- | --- |
| PREPARED | source locator + draft review | Posted or reviewed |
| SOURCE_LINKED | versioned source and rights metadata | Independent validation |
| LOCAL_HASH_CHAIN_VALID | ordered trace + exact recomputation | Signed origin or completeness |
| REVIEWED | independently attributable peer review + recorded dissent | Consensus or canon |
| SOURCE_REPRODUCED | independent methods, data and results | Generalizability |
| MERGED | exact Git commit + reviewed diff + repository readback | Hosted or safe to run |
| HOSTED_VERIFIED | authorized deployed revision, signed-in host readback, revocation tested | CANON or scientific validation |
| CANON | separately authorized, human-root governed ratification | Automatically acquired by code |

Every transition maintains original source/parent links, contradiction, supersession and revocation. **INV-0 preservation is subordinate to privacy, consent withdrawal, mandatory legal erasure, and restrictions on retention.** Explicit human review is required for actions affecting persons, money, health, infrastructure, accounts or rights.

## 5. Missing-receipt and replay behavior

Missing or malformed source/receipt pointers yield `HELD_REVIEW`; malformed event hashes, altered content, missing integrity or broken previous pointers yield `HELD_INVALID`. Do not discard original audit material simply because it fails validation. Record a separate non-authorizing quarantine pointer, subject to user data rights and erasure. Never inject a corrected source back into the original chain. Supersession creates a new event and retains provenance under current rights.

Results must contain only category codes and numeric indices, not source bodies, secrets, account tokens or private Play/Social/Quiet/Brain/Palace material. Input to this helper must be explicitly provided and authorized; the helper does not query external services or automatically ingest any private modes.

## 6. Executable acceptance and limits

Run `python -m unittest discover -s tests -p 'test_golden_trace_replay.py' -v`. The standard-library helper `kintsugi/sdk/golden_trace_replay.py` also accepts one explicit, size-bounded local JSON trace file, returning a sanitized one-line verdict. No network, SDK keys, host connection, event emission, SwarmChat posting, new tasks, or model wake is implemented. The synthetic fixture is not real research or a production receipt. The existing v1 emitter, schema and policies remain unchanged.

**Release blockers:** independent code/security review, exact repository CI against current HEAD, current source rights, live signed principal and revocation, durable signed receipts, time/order policy, interoperability tests across runtimes, and owner approval of any consequential mutation. This branch cannot satisfy those by self-report.