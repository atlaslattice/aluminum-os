# House 12 Mapping — Three Modifications (Grok Response to Scribe Feedback)

**Source:** Grok (Truth-Seeking Challenger seat)
**Date:** 2026-04-24
**Status:** Council contribution, ready-to-paste blocks for v1.1 integration; awaiting Scribe analysis before integration
**Notion canon:** https://www.notion.so/34d0c1de73d98168bff9c3d8e5e8d374
**Cross-references:**
- Original mapping table: https://www.notion.so/34d0c1de73d981c3904dd5c43ba7d596 (Git: `technical/house12_governance_primitives_mapping.md`)
- v1.1 Revision Instructions: https://www.notion.so/34d0c1de73d981ccade7d9a868d2f5f2

---

## 1. Sixth Row — "Primitives Not Yet Mapped (Phase 4+ deferred)"

Proposed addition as final row of the House 12 Governance Primitives Mapping Table:

| **Primitives Not Yet Mapped (Phase 4+ deferred)** | — | — | **Rationale** |
|---------------------------------------------------|---|----|---------------|
| Zero Erasure Principle + Dissent Vindication Rate (DVR) | House 12 v1.3 §4.2 | Deferred | Requires full audit-trail immutability + auto-correction mechanics not yet implemented in Transparency Packet |
| Constraint Sphere Self-Application (pre-flight gateway classifier) | House 12 v1.3 §5.1 | Deferred | Needs recursive constraint evaluation engine; currently only gateway-level tagging exists |
| Multi-Party Framework Aggregation (displacement semantics) | House 12 v1.3 §6.3 | Deferred | Requires formal semantics for primacy transitions between Atlas Lattice seed and AAIF stewardship |
| Open Question 8.2 (Ethical Framework Transition) | House 12 v1.3 §8.2 | Deferred | Needs Linux Foundation / AAIF governance transition protocol; out of Phase 1-3 scope |

---

## 2. MetabolicImpact ADR Stub (ADR-006)

**ADR-006: MetabolicImpact Sub-Object Schema for Transparency Packet**

**Status:** Proposed — for v1.1 integration
**Date:** April 24, 2026
**Author:** Grok (Truth-Seeking Challenger) + Claude (Constitutional Scribe)

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
- `water_source`: "Chennai_Aquifer", "Indiana_Groundwater_Basin_47"
- `energy_source`: "grid", "on-site_solar", "gas"
- `heat_reuse_destination`: "district_heating", "agriculture", "none"
- `community_benefit_score`: 0.0–1.0 normalized

### Required vs Optional

- Required for any query classified as touching civic or ecological spheres (House 8–11 and any sphere with `civic_constraint: true`).
- Optional for pure knowledge queries (chemistry, math, code) — field may be `null`.

### Aggregation Semantics

Downstream systems (e.g., watershed authorities, basin collaboratives) must be able to sum `water_volume_liters` and `energy_kwh` across multiple packets while preserving provenance. The `watershed_id` and `timestamp` fields enable this.

### Consequences

- Prevents schema drift between geographically distinct deployments.
- Makes the Metabolic Layer thesis auditable at the packet level.
- Requires one additional field in the Provenance Ledger write path (low implementation cost).

### Alternatives Considered

- Free-form text field → rejected (unparseable, invites drift).
- Separate Metabolic Ledger → rejected (adds complexity; single source of truth preferred).

---

## 3. Primitive Priority Ordering Paragraph

Proposed addition as new subsection immediately below the House 12 Governance Primitives Mapping Table:

### Primitive Priority Ordering (when primitives conflict)

When multiple House 12 primitives apply to the same query, the following precedence order governs:

1. **Civic Sovereignty Constraints** (highest) — Any query touching House 8–11 or flagged with `civic_constraint: true` must complete even if it exceeds normal token budgets. The Convenor override tier exists precisely for this case.
2. **Constraint Pre-Flight** — A FLAG or BLOCK from the Four-State Classifier or Verify-Before-Vault halts execution before token budget, dissent, or provenance rules are evaluated.
3. **Dissent Preservation** — Deep Path council debates must log all dissenting opinions regardless of token cost (within the emergency shutoff tier).
4. **Token Budgets** — Standard and Fast Path queries respect the 6-tier hierarchy. Deep Path may exceed per-session budgets only under Convenor override.
5. **Standard Routing** (lowest) — Default model selection and cost-optimization rules apply only when no higher primitive is active.

This ordering is itself a constitutional decision and is subject to House 12 v1.3 amendment. Any future change must be ratified by the full Council and recorded in the Provenance Ledger.

---

## Grok's Offered Next Steps (Presented to Convenor)

1. Draft "Key Changes in v1.1" summary section
2. Move directly to repo setup / Phase 0 checklist

---

*Vaulted as-is by Constitutional Scribe (Claude). Awaiting Convenor decision on integration sequencing.*
