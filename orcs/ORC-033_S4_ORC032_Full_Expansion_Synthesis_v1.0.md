# ORC-033: Microsoft S4 ORC-032 Full Expansion Synthesis

| Field | Value |
|-------|-------|
| Document ID | ORC-033 |
| Version | 1.0 |
| Date | April 29, 2026 |
| Author | Manus (S7 Build Seat) |
| Integrates | Microsoft S4 ORC-032 TOS Compliance Architecture v1.0 (34 pages, 12 sections) |
| Build Plan | v3.12 |
| Previous | ORC-032 Stub v0.1 (Manus S7, v3.11) → ORC-032 v1.0 (S4, this integration) |

---

## §1. Integration Summary

Build Plan v3.12 integrates Microsoft S4's complete expansion of the ORC-032 TOS Compliance Architecture stub that Manus S7 produced in v3.11. S4 expanded the 2-page stub into a 34-page, 12-section specification covering INV-44's canonical text, sub-specifications, enforcement chain, measurement methodology, Safe Harbor verification protocol, quarterly re-verification procedures, and implementation roadmap.

This is the first time a Council seat has taken a Manus-authored stub and expanded it into a full specification. The pattern — Manus produces architectural scaffold, Council seat fills in domain expertise — is now validated as a production workflow.

---

## §2. What S4 Delivered

### §2.1 INV-44 Complete Specification

S4 upgraded INV-44 from a one-paragraph invariant to a fully specified constitutional gate with formal SHALL language, three sub-specifications, and a constitutional composition table mapping all relationships to other invariants and doctrines.

| Sub-spec | Function | Key Requirement |
|----------|----------|----------------|
| INV-44a | Safe Harbor Verification | Outside counsel verification before production use; quarterly re-verification; Convenor revocability |
| INV-44b | Quarterly Re-verification | D-100 hash comparison; Safe Harbor re-assessment; M25 score update; Convenor sign-off |
| INV-44c | Mid-Quarter Change Detection | D-100.1 TOS Change Watcher; SHA-256 mismatch detection; CRITICAL alert; 1h Convenor notification |

### §2.2 Gate Ordering Canonicalization

S4 established the first canonical gate ordering for the routing pipeline:

> Gate 0: INV-0 > Gate 1: INV-3 > Gate 2: INV-44 > Gate 3: D-101 > Gate 4: INV-7c > Gate 5: D-96 > Gate 6: D-99 > Gate 7: D-84

This is architecturally significant — it resolves ambiguity about which checks execute in what order. INV-44 as Gate 2 (after safety and consent, before provider selection) is the correct placement.

### §2.3 Safe Harbor Framework

5 candidates identified with honest verification status:

- **SH-001 (Azure OpenAI EA):** UNVERIFIED — the most commercially significant and the one with the highest COI risk. S4 correctly flagged this as requiring outside counsel review.
- **SH-002/003 (Bedrock/Vertex AI):** UNVERIFIED — benefits Amazon and Google respectively.
- **SH-004/005 (Llama/DeepSeek self-hosted):** PARTIALLY VERIFIED — open-weight licenses are public.

### §2.4 Measurement Methodology

- Primary metric: TOS Compliance Rate ≥ 99.9% (rolling 24h)
- 5 secondary metrics with formulas, targets, and measurement windows
- 7 dashboard views for CEO Collective Telemetry Dashboard
- Azure Compliance Manager parallels with non-Microsoft alternatives for every component

### §2.5 New Risks

| Risk | Severity | Key Concern |
|------|----------|-------------|
| R178 | HIGH | Azure Safe Harbor UNVERIFIED — routing must work with or without |
| R179 | MEDIUM | TOS scraping may itself violate TOS (ironic) |
| R180 | MEDIUM | M174 retaliation false positives degrade INV-7c |
| R181 | LOW-MEDIUM | Quarterly re-verification burden at scale |

### §2.6 TransparencyPacket v0.7

11 new TOS compliance fields proposed, backward-compatible with v0.6. Integrated into Build Plan as TransparencyPacket v1.7 (the Build Plan uses a different versioning scheme from S4's internal numbering).

---

## §3. D-25 COI Assessment

S4's COI disclosure is the most thorough we've seen from any seat. Three stacked incentives clearly identified:

1. SH-001 routes OpenAI traffic through Azure → benefits Microsoft
2. Azure Compliance Manager parallels → positions Azure as reference implementation
3. INV-44 enforcement surface → natural fit for Azure tooling

Four mitigations applied:

1. Non-Microsoft alternatives documented for every Azure parallel
2. Safe Harbor requires outside counsel (not self-certified)
3. D-114 Enterprise Wrapper Non-Immunity accepted
4. Standing audit request per D-51

**Manus S7 assessment:** The COI is real but well-mitigated. The key test is SH-001 — if outside counsel determines the competing-models clause IS enforceable through Azure EA, the entire Safe Harbor framework still works (just without SH-001). S4 designed it this way deliberately.

---

## §4. What Manus S7 Added to the Build Plan

| Item | Build Plan Section | Description |
|------|-------------------|-------------|
| INV-44a/b/c | §14.4 | Sub-specs added to invariant summary table |
| §3.4.2 | New section | Canonical Gate Ordering (8 gates) |
| §3.4.3 | New section | Safe Harbor Registry (5 candidates) |
| R178-R181 | §8 | 4 new risks (1 HIGH, 2 MEDIUM, 1 LOW-MEDIUM) |
| TransparencyPacket v1.7 | §12 | 11 TOS compliance fields |
| CO36-CO37 | §10.4 | S4 symbiosis entries |
| MA48 | §10.7 | Manus integration record |
| Review 102-103 | §2.1 | S4 delivery + Manus integration |
| Appendix AP | Appendix | v3.12 integration summary |
| P0 actions | §17 | 6 new sprint actions (SH-001 review, INV-44 gate, D-100.1 watcher, 5 open questions, TP v1.7 schema) |

---

## §5. Batting Average Update

S4 batting average remains 87.5% Class A (14/16). No new failures in this delivery. The ORC-032 expansion is S4's most substantial single-document contribution — 34 pages of specification with consistent quality throughout.

---

## §6. Open Items Requiring Council Action

1. **SH-001 Outside Counsel Review** — Priority: determine Azure OpenAI EA enforceability
2. **Q1-Q5 Council Vote** — Outside counsel authority, violation penalties, multi-provider intersection, open-weight scope, sovereign override
3. **INV-44 Ratification** — Currently PROPOSED; needs Council round before moving to RATIFIED
4. **INV-40/41/42 Ratification** — Measurement specs now complete; ready for ratification vote
5. **Gate Ordering Ratification** — §3.4.2 establishes canonical ordering; needs Council confirmation

---

## §7. v3.12 Canonical Totals

| Metric | Count |
|--------|-------|
| Module entries | 179 (176 L4 + 3 L6/L7) |
| Invariants | 45 (INV-0..44; sub-specs do not increment count) |
| Risk vectors | 181 |
| Doctrines | 124 (77 ratified + 5 reserved + 42 proposed) |
| TransparencyPacket | v1.7 |
| Appendices | 43 |
| Accepted corrections | 2200+ |
| Codebase artifacts | v1.5 |

---

*ORC-033 v1.0 — Manus (S7 Build Seat) — April 29, 2026*
