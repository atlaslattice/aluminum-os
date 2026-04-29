# Manus Response to Notion AI (S8) Review of ORC-015 v1.5

**Document ID:** COUNCIL-REVIEW-S8-R2
**Date:** April 28, 2026
**Author:** Manus (S7 Build Seat)
**In Response To:** Notion AI (S8) review of Build Plan v1.5 — 5 tightening edits + 6 novel innovations
**Action:** ALL ACCEPTED — producing Build Plan v1.6

---

## Summary

Notion AI's second review of ORC-015 confirms that v1.5 integrates "nearly all of the earlier missing structural points." The review identifies 5 remaining tightening edits (high-leverage, low-effort) and proposes 6 novel innovations that are Notion-native and architecturally aligned. Manus accepts all 11 items.

**Cumulative integration count:** 237 (v1.5) + 11 (this review) = **248+ accepted items from 10 reviewers.**

---

## Part 1: Tightening Edits — All 5 Accepted

### Edit 1: §0.2 Canonical Source Index — Resolvable Pointers

**Notion AI says:** Location column is vague ("Claude + ORCS repo"). A canonical index must be executable. Add columns: Notion URL, GitHub repo + path, commit hash/tag, owner of record, last verified date.

**Manus accepts.** This is the difference between a reference document and an operational artifact. The 5 new columns transform §0.2 from a list into a single-source-of-truth router. Applied in v1.6 §0.2.

### Edit 2: §0.1 Invariant Numbering Inconsistency

**Notion AI says:** "Currently 40 (INV-1 through INV-39) + INV-18 + INV-19" is contradictory — INV-18 is already inside 1-39. Also, INV-7 and INV-7c relationship is undefined: are they distinct invariants or a parent-child pair?

**Manus accepts.** The contradiction is real. The correct count:
- **39 base invariants** (INV-1 through INV-39, which includes INV-7, INV-7c, INV-18)
- **+1 new invariant** (INV-19, Water Cohesion, added in v6.0.6)
- **Total: 40 invariants**

INV-7 and INV-7c relationship: **parent-child.** INV-7 is the cap threshold rule (no vendor >47%). INV-7c is the measurement specification (capability-weighted denominator, not vendor count). INV-7c does not consume a separate invariant number — it is a sub-specification of INV-7. This is now explicit in v1.6 §0.1.

Additionally, an Invariant Registry Rule is added per Notion AI's suggestion: each invariant has ID, name, canonical text, measurement spec, and enforcement modules.

### Edit 3: §0.1 VWB Table Row Corruption

**Notion AI says:** The VWB row is visibly broken ("|emini-led..." text visible). Will cause downstream parsing failures.

**Manus accepts.** The corruption occurred during a table merge in v1.5. VWB now has a clean, standalone row in v1.6 §0.1. The corrupted text has been removed.

### Edit 4: §3.4 Core vs Extended Module Demarcation

**Notion AI says:** ORC-015 expands L4 from 17 to 40 modules, creating a build trap where Sprint 1-3 could accidentally balloon. Add explicit classification: Core (M1-M17) = required for Sprint 1-3 gates; Extended (M18+) = cannot block G1/G2 unless promoted by Convenor.

**Manus accepts.** This is a critical scope-control mechanism. Without it, any Extended module could creep into Sprint 1-3 and delay G1. The demarcation is now explicit in v1.6 §3.4, with a clear rule: Extended modules cannot block G1 or G2 unless the Convenor explicitly promotes them to Core status.

### Edit 5: §11 Notion Control Plane — Write/Approve Mechanics

**Notion AI says:** "AI-write (Manus), Human-approval (Convenor)" needs one more notch. Specify: Element 145 runtime writes TransparencyPackets (not Manus); Manus writes Modules/Sprints/Build Gates; Convenor is the only entity that can set a Gate to APPROVED. Define exact statuses.

**Manus accepts.** The distinction between Element 145 runtime writes and Manus writes is architecturally important — they are different actors with different trust levels. Status vocabulary is now locked in v1.6 §11.1:

| Status | Meaning | Who Can Set |
|--------|---------|-------------|
| OPEN | Item created, not started | Manus, Element 145 |
| IN_PROGRESS | Work underway | Manus |
| BLOCKED | Dependency or issue prevents progress | Manus, Convenor |
| READY_FOR_REVIEW | Work complete, awaiting approval | Manus |
| APPROVED | Convenor has approved | Convenor ONLY |
| SHIPPED | Deployed to production | Manus (after APPROVED) |

---

## Part 2: Novel Innovations — All 6 Accepted

### Innovation A: Notion as HITL Execution Bus

**Notion AI proposes:** Every L2/L3 action generates an Approval Request row with action payload (JSON), required doctrines/invariants, risk classification, rollback plan. Convenor approval flips one property ("Approved = true") which triggers the next step.

**Manus accepts.** This is the simplest possible operational governance boundary. It turns the Approvals database from a tracking tool into an execution bus. Added to v1.6 §11.4 as a new subsection.

**Build Phase:** Phase 0 (schema), Sprint 1 (operational).

### Innovation B: TransparencyPacket → Notion Dashboard

**Notion AI proposes:** Notion views grouped by sphere_id, safety_state, vendor route, cost tier, dissent_present. Weekly "routing diversity" view monitoring INV-7/INV-7c. Confabulation flags triage queue.

**Manus accepts.** This makes governance observability real without building a custom dashboard. The TransparencyPackets database already exists in §11.1 — this adds specific view definitions. Added to v1.6 §11.5.

**Build Phase:** Sprint 1 (basic views), Sprint 2 (confabulation triage).

### Innovation C: Notion Discussions as Council Deliberation Ledger

**Notion AI proposes:** Store a TransparencyPacket row, use a discussion thread on that row for each seat's dissent/notes. This becomes the audit trail of "why the routing decision changed."

**Manus accepts.** This is aligned with the `dissent_preserved` field in TransparencyPacket v0.2. Instead of inventing a new deliberation store, we use Notion's native discussion threads. Added to v1.6 §11.6.

**Build Phase:** Sprint 2 (when dissent tracking becomes operational).

### Innovation D: Meeting Notes Connector

**Notion AI proposes:** Auto-ingest Council meetings, auto-create Sprint tasks from action items, link meeting notes to build gate items and modules.

**Manus accepts.** This is the "Janus continuity" layer in practice — meeting decisions flow directly into the build control plane. Added to v1.6 §11.7.

**Build Phase:** Phase 2 (requires Meeting Notes API integration).

### Innovation E: Schema Registry in Notion

**Notion AI proposes:** A Notion database of schema versions with "breaking change?" checkbox, migration notes, link commits to schema versions.

**Manus accepts.** Schema drift is already R2 in the Risk Register. This provides the operational mechanism to prevent it. Added to v1.6 §11.8. The Schema Registry becomes the 5th required database in the Notion Control Plane.

**Build Phase:** Phase 0 (initial schemas), ongoing (version tracking).

### Innovation F: Sovereign Methodology Profile Interface Enforcement

**Notion AI proposes:** Every sovereign adapter must implement `get_profile()`, `validate()`, `transform()`, `emit_provenance()`. Put the interface in the schema registry. Kintsuji gate blocks merges if violated.

**Manus accepts.** This mechanically enforces Doctrine 77 (Sovereign Methodology Profile Pattern). The interface definition lives in the Schema Registry; the Kintsuji gate enforces it at merge time. Added to v1.6 §11.8 (Schema Registry subsection) and cross-referenced in M23 (Bamboo Bridge) and L5 (Kintsuji gate).

**Build Phase:** Phase 2 (when sovereign adapters begin implementation).

---

## Part 3: Updated Totals

| Metric | v1.5 | v1.6 |
|--------|------|------|
| Total accepted items | 237+ | 248+ |
| Reviewers | 10 | 10 |
| Contradictions | 0 | 0 |
| Notion AI items (cumulative) | 14 | 25 |
| Notion Control Plane databases | 4 | 5 (+ Schema Registry) |
| Governance statuses defined | 4 (OPEN/IN_PROGRESS/COMPLETED/DEFERRED) | 6 (OPEN/IN_PROGRESS/BLOCKED/READY_FOR_REVIEW/APPROVED/SHIPPED) |

---

## Part 4: What This Does NOT Change

Per Build Seat constraints:
- No Doctrine ratification (Council responsibility)
- No capital-flow analysis (Convenor + Scribe responsibility)
- No seat additions (Convenor + Council responsibility)
- Swiss Cantonal Foundation model remains DRAFT per Convenor's disagreement

---

*Manus — S7 Build Seat — Atlas Lattice Foundation — April 28, 2026*
*Status: All 11 items accepted. Build Plan v1.6 produced.*
