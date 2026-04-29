# House 12 Governance Primitives → Element 145 Module Mapping

**Source:** Grok (Truth-Seeking Challenger seat) — contribution from v1.1 synthesis review
**Date:** 2026-04-24
**Status:** Council contribution, awaiting Scribe analysis and integration decision
**Manus assessment:** High-value, accepted into v1.1 synthesis pipeline
**Placement recommendation (Grok):** Section 4.4 of v1.1, or standalone appendix titled "House 12 → Element 145 Crosswalk"
**Notion canon:** https://www.notion.so/34d0c1de73d981c3904dd5c43ba7d596

---

## The Mapping

| House 12 Primitive | Element 145 Module(s) | Implementation Path | Notes |
|--------------------|----------------------|---------------------|-------|
| **Token Budgets (6-tier)** | Budget Enforcement | Extend CostTracker from `aluminum-os-v3/bridge.py` | Add per-turn, per-session, per-user/day, system/day, emergency shutoff, Convenor override tiers |
| **Constraint Pre-Flight** | Four-State Classifier + Verify-Before-Vault | Gateway-level tag (KNOWN/ESTIMATED/SPECULATIVE/UNKNOWN) + secondary model review | Fail-closed on FLAG/BLOCK; routing table determines reviewer model per sphere |
| **Dissent Preservation** | Deep Path Council Debates | Pantheon quorum + Grok-contrarian role + Sheldon-synthesizer | Max(3, 45% of available non-conflicted) quorum; explicit dissent logging in Transparency Packet |
| **Provenance Ledger** | Transparency Packet + Audit Chain | Direct extraction from UWS `audit_chain.rs` + new schema | Cryptographic hashing, append-only, MetabolicImpact sub-object for watershed accountability |
| **Civic Sovereignty Constraints** | Civic Layer + MSP-001 | Generalize UWS INV-33 through INV-36 jurisdiction logic | Hard vs soft constraint distinction; consent enforcement + multi-source location validation |

---

## Grok's Stated Rationale

This table makes the constitutional lineage explicit and gives future implementers (and external partners) a clear map from principle to code.

---

## Grok's Placement Recommendation for v1.1

- Insert as **Section 4.4** (right after the module coverage tables) or as a short standalone appendix titled "House 12 → Element 145 Crosswalk"
- Reference it in every ADR that touches governance, routing, or civic constraints

---

## Grok's Offered Next Steps (Presented to Convenor)

1. Ready-to-paste Markdown block for the v1.1 document
2. "Key Changes in v1.1" summary section
3. Move on to next steps (repo setup / Phase 0 checklist)

---

*Vaulted as-is by Constitutional Scribe (Claude) for Council review prior to v1.1 integration. Analysis appended separately.*
