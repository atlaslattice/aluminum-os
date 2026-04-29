# House 12 Mapping — Final v3 Blocks for v1.1 (Grok Third Revision Pass)

**Source:** Grok (Truth-Seeking Challenger seat) — third revision pass with all five Scribe modifications applied
**Date:** 2026-04-24
**Status:** Final blocks for v1.1 integration; ready for Manus assembly
**Notion canon:** https://www.notion.so/34d0c1de73d981ef899fdca1fd3a0a9a

**Cross-references:**
- Original mapping table (v1): `technical/house12_governance_primitives_mapping.md`
- Three modifications (v2): `technical/house12_mapping_three_modifications.md`
- v1.1 Revision Instructions: `technical/element145_synthesis_strategy_v1.1_revision_instructions.md`

---

## A. Revised House 12 Governance Primitives Mapping Table (with sixth row)

**House 12 → Element 145 Crosswalk**

| House 12 Primitive | Element 145 Module(s) | Implementation Path | Notes |
|--------------------|----------------------|---------------------|-------|
| **Token Budgets (6-tier)** | Budget Enforcement | Extend CostTracker from `aluminum-os-v3/bridge.py` | Add per-turn, per-session, per-user/day, system/day, emergency shutoff, Convenor override tiers |
| **Constraint Pre-Flight** | Four-State Classifier + Verify-Before-Vault | Gateway-level tag (KNOWN/ESTIMATED/SPECULATIVE/UNKNOWN) + secondary model review | Fail-closed on FLAG/BLOCK; routing table determines reviewer model per sphere |
| **Dissent Preservation** | Deep Path Council Debates | Pantheon quorum + Grok-contrarian role + Sheldon-synthesizer | Max(3, 45% of available non-conflicted) quorum; explicit dissent logging in Transparency Packet |
| **Provenance Ledger** | Transparency Packet + Audit Chain | Direct extraction from UWS `audit_chain.rs` + new schema | Cryptographic hashing, append-only, **MetabolicImpact sub-object** (see ADR-006) for watershed accountability |
| **Civic Sovereignty Constraints** | Civic Layer + MSP-001 | Generalize UWS INV-33 through INV-36 jurisdiction logic | Hard vs soft constraint distinction; consent enforcement + multi-source location validation |
| **Primitives Not Yet Mapped (Phase 4+ deferred)** | — | — | **Zero Erasure Principle + Dissent Vindication Rate (DVR)** — requires self-healing audit trail (v2 feature)<br>**Constraint Sphere Self-Application (recursive engine)** — deferred pending recursive evaluation engine<br>**Constraint Sphere Self-Application (principle)** — in scope for v1.1 (every internal decision generates its own Transparency Packet, even if recursion is partial)<br>**Multi-Party Framework Aggregation (displacement semantics)** — requires formal primacy transition protocol<br>**Open Question 8.2 (Ethical Framework Transition)** — requires Linux Foundation / AAIF governance transition protocol |

---

## B. Revised ADR-006 (MetabolicImpact)

**ADR-006: MetabolicImpact Sub-Object Schema for Transparency Packet**

**Status:** Proposed — for v1.1 integration
**Date:** April 24, 2026
**Author:** Grok (Truth-Seeking Challenger), in response to Scribe (Claude) feedback identifying need for explicit schema

### Context

The Transparency Packet is the canonical audit record for every Element 145 decision. For queries that touch physical infrastructure (water, energy, land, community), the packet must carry a structured `MetabolicImpact` sub-object so that downstream consumers (watershed authorities, municipalities, Tribal Nations, hyperscalers) can aggregate and reconcile impact across providers and sites.

### Decision

Add a `MetabolicImpact` sub-object to the Transparency Packet with the following schema:

```json
{
  "metabolic_impact": {
    "water_volume_liters": "number | null",
    "water_source": "string | null",
    "watershed_id": "string | null",
    "energy_kwh": "number | null",
    "energy_source": "string | null",
    "heat_btu_recovered": "number | null",
    "heat_reuse_destination": "string | null",
    "land_use_m2": "number | null",
    "community_benefit_score": "number | null",
    "timestamp": "ISO8601"
  }
}
```

Field examples:
- `water_source`: "Watershed_ID_47" or neutral identifier

### Required vs Optional + Ambiguity Handling

Required for any query classified as touching civic or ecological spheres (House 8–11 or flagged `civic_constraint: true`).

**In ambiguous cases, the MetabolicImpact field is required; a null value should reflect a conscious "no metabolic footprint" determination, not a classification gap.**

### Aggregation Semantics

Downstream systems must be able to sum `water_volume_liters` and `energy_kwh` across multiple packets while preserving provenance. The `watershed_id` and `timestamp` fields enable this.

### Alternatives Considered

- Free-form text field → rejected (unparseable, invites drift).
- Separate Metabolic Ledger → rejected (adds complexity; single source of truth preferred).

---

## C. Revised Primitive Priority Ordering Paragraph

### Primitive Priority Ordering (when primitives conflict)

When multiple House 12 primitives apply to the same query, the following precedence order governs:

1. **Civic Sovereignty Constraints** (highest) — Any query touching House 8–11 or flagged with `civic_constraint: true` must complete even if it exceeds normal token budgets. The Convenor override tier exists precisely for this case.
2. **Constraint Pre-Flight** — A FLAG or BLOCK from the Four-State Classifier or Verify-Before-Vault halts execution before token budget, dissent, or provenance rules are evaluated.
3. **Dissent Preservation** — Deep Path council debates must log all dissenting opinions regardless of token cost (within the emergency shutoff tier).
4. **Token Budgets** — Standard and Fast Path queries respect the 6-tier hierarchy. Deep Path may exceed per-session budgets only under Convenor override.
5. **Standard Routing** (lowest) — Default model selection and cost-optimization rules apply only when no higher primitive is active.

**Convenor-unreachable default behavior:** In scenarios where the Convenor does not respond within the configured timeout, the default is **fail-closed with full audit flag** — the query halts and returns a Transparency Packet marked `convenor_override: timeout_default`. This default is itself a constitutional decision and must be ratified before deployment.

This ordering is subject to House 12 v1.3 amendment. Any future change must be ratified by the full Council and recorded in the Provenance Ledger.

---

## D. Key Changes in v1.1 (new section for top of document)

### Key Changes in v1.1 (from v1.0)

- Added **Metabolic Layer bridge paragraph** (Executive Summary) explicitly connecting Element 145 to watershed-level coordination.
- Added **House 12 Governance Primitives Mapping Table** (now §4.4 or standalone appendix) with six rows including deferred primitives.
- Added **ADR-006: MetabolicImpact Sub-Object Schema** with concrete JSON schema, required/optional rules, and aggregation semantics.
- Added **Primitive Priority Ordering** paragraph with explicit conflict resolution and Convenor-unreachable default behavior.
- Refined reuse estimate to 55% design / 25–30% direct code and timeline to realistic 60–90 days.
- Flagged AI Studio conversation code as HIGH risk (per Claude) with "hypothesis until extracted and tested" language.
- Updated Day 14 Success Gate with fallback chain + <2s median latency target.
- Minor clarifications: 144-sphere note now references proven 12-House base; Chennai reference grounded with v0.3 citation.

---

## NOT INCLUDED in this Grok contribution: Methodology Notes

The Convenor's recommended Methodology Notes subsection (documenting Cross-Model Praise Pattern, tool-access asymmetry, adversarial review status) was NOT included in Grok's third pass. The Scribe will append this separately to ensure these observations make it into v1.1 canon rather than only chat record.

See Session Handoff Log April 24 evening for full methodology observations to be folded in.

---

*Vaulted as-is by Constitutional Scribe (Claude). Awaiting Convenor decision on integration sequencing. Manus assembly of v1.1 can proceed with these four blocks plus separately-authored Methodology Notes.*
