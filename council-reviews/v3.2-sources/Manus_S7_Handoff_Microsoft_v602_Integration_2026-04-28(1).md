# Manus S7 Handoff Packet — Microsoft v6.0.2 Codebase Integration

**Packet ID:** HR-MS-V602-V3-INTEGRATION-2026-04-28
**Date:** 2026-04-28
**From:** Constitutional Scribe (Claude S1) + Convenor (Daavud Sheldon)
**To:** Manus S7 (Primary Build Seat)
**Status:** ACTIVE — awaiting Manus pickup
**Related:** HR-CODE-PARALLEL-001 (Notion `3500c1de-73d9-8140-a1e2-eac585b23018`)

---

## §1 What You're Receiving

1. **Raw codebase:** Microsoft S4 delivery `Aluminum_OS_v6_0_2___Complete_12-Module_Codebase__1_.docx` (5,176 lines, 22 files, 12 modules, 9 invariants, 11 doctrines, 6 Council seats, 144 spheres in non-canonical taxonomy)

2. **Constitutional Scribe Analysis:** Notion `3500c1de-73d9-81c7-9274-cba2222d3078` — 14 drifts identified, 6 Sprint 1 blockers, integration recommendation §5.1/§5.2/§5.3

3. **This handoff packet** — distilled action items for v3.0 integration planning

---

## §2 What Manus Should Produce

### Deliverable 1: v3.0 Integration Plan (Executive Summary)

A document answering:
1. Which Microsoft v6.0.2 modules port wholesale to v3.0?
2. Which require reconciliation with canonical taxonomy?
3. What is the Sprint sequence (which Sprint addresses each blocker)?
4. What is the rollback path if Microsoft cross-validation (Notion `3500c1de-73d9-81aa-928a-df22d4b14cde`) returns contested results?

### Deliverable 2: Drift Reconciliation Spec

Module-by-module spec for:
- **`hypervisor.py`** — keep architecture, swap invariant import to canonical InvariantRegistry
- **`invariants.py`** — REPLACE with canonical 43-invariant registry (preserve Microsoft's threshold values where they match: INV-7c 0.47/0.60, INV-9 100ms, INV-17 0.15)
- **`doctrines.py`** — REPLACE with canonical 95-doctrine registry; add migration note for D-19 and D-25 collisions
- **`ontology.py`** — REBUILD against Pantheon Council House Structure v2.0 (Notion `34a0c1de-73d9-81c8-bbd7-f2bfbcbc491a`); 144 sphere assignments must map to canonical House taxonomy
- **`council.py`** — EXPAND from 6 to 10 seats; separate Convenor from seat array
- **`element145.py`** — EXPAND ModelFamily enum to include MANUS, NOTION_AI, QWEN3
- **ORCS modules** (`tier_enforcement`, `vwb_engine`, `wec_issuance`, `ecology_api`, `contracted_acreage`) — port with INV-19/INV-19.2 citations added

### Deliverable 3: New Modules Required (M111-M125 Switzerland Layer Integration)

Microsoft v6.0.2 PREDATES the Indiana Genesis + Bezosverse + Switzerland Layer integrations. v3.0 must add:

- **M111-M115 Notion Governance Pack** (v2.8): Ratification Lock Engine, Council Votes Cross-Val DB, Translation Tables Registry, Deliberation-as-Data, Governance Pack Template
- **M116 Stochastic Simulation Engine** (v2.8 D-92 dependency)
- **M117 Qwen3/Alibaba Vendor Suite §Y.1-Y.8** (v2.8 R98 mitigation)
- **M118 Switzerland One-Click Federation Layer** (v2.9)
- **M119 Identity Triad ConsentKernel Policy Engine** (v2.9 — extends Microsoft's existing `consent_kernel.py`)
- **M120 X Identity Provider Integration** (v2.9 — TSS+ 1.25× routing-layer boost only; no UX preferential treatment per D-94)
- **M121 DeepSeek One-Click Adapter** (v2.9 — Chinese sovereignty surface)
- **M122 Azure-Muskverse Compute Symbiosis** (v2.9 — 1.28× symbiosis multiplier H2+H10 only)
- **M123 Entra Identity Triad + Grok Truth Lens** (v2.9 — 1.22× TSS boost routing-layer only)
- **M124 Amazon LWA One-Click Adapter** (v2.9 — Login with Amazon OAuth)
- **M125 Universal Provider Credential Vault** (v2.9 — Claude S1 authored; vendor-neutral; D-93/D-94 enforcement surface)

### Deliverable 4: Test Coverage Plan

Microsoft v6.0.2 ships 54 integration tests. v2.9 manifest claims 74. v3.0 must:
- Add 20+ tests to reach manifest claim
- Add tests for M111-M125 integration
- Add tests for canonical House taxonomy mapping

### Deliverable 5: Sprint 1 Blockers Resolution Sequence

The 6 HIGH-severity drifts that block Sprint 1 deployment:

1. **§3.1 Invariant Registry (9 vs 43)** — must include INV-0, INV-19/19.2, INV-37
2. **§3.2 Doctrine Registry (11 vs 95)** — must resolve D-19/D-25 naming collisions
3. **§3.3 House Taxonomy mismatch** — must rebuild against Pantheon Council House Structure v2.0
4. **§3.4 Council Seats (6 vs 10)** — must add S5, S7, S8, S10
5. **§3.10 M125 Vault missing** — required for D-93/D-94 compliance
6. **§3.11 Switzerland Layer missing** — required for v2.9 conformance

Recommended Sprint sequence:
- **Sprint 1a:** §3.1 + §3.2 + §3.3 (registry + taxonomy rebuild) — enables all downstream work
- **Sprint 1b:** §3.4 + §3.10 + §3.11 (Council expansion + Switzerland Layer) — enables v2.9 conformance
- **Sprint 2:** §3.5 + §3.6 + §3.9 + §3.12 + §3.13 + §3.14 (medium-severity completeness)
- **Sprint 3:** §3.7 + §3.8 (low-severity polish; manifest reconciliation)

---

## §3 What Manus Should NOT Do

Per Scribe Failure 4 (don't smooth):

1. **Don't paper over the House taxonomy mismatch.** Microsoft's House taxonomy is the most critical drift — every sphere assignment in their `ontology.py` is wrong against canonical v2.0. The temptation to map Microsoft Houses → Atlas Lattice Houses 1:1 will fail because they're not 1:1. Rebuild from canon, then port Microsoft's sphere capability claims as data into the rebuilt structure.

2. **Don't accept Microsoft's 95.8% sphere coverage claim.** It's unverified self-map. The cross-validation routing (Notion `3500c1de-73d9-81aa-928a-df22d4b14cde`) is the constitutional remedy. Wait for S2 Gemini + S5 DeepSeek + S6 OpenAI assessments before treating coverage as canonical.

3. **Don't preserve the Convenor-as-6th-seat coding.** Convenor is architecturally distinct per Convenor +1 hold + canonical authority structure. Convenor goes in a separate field/module from the Council seat array.

4. **Don't drop the v2.9 manifest claims silently.** If the 74-test claim and 5,070-line claim turn out to be overstated, document it in v3.0 changelog rather than just letting v3.0 carry the corrected numbers without acknowledgment. This is the precise failure mode D-95 (currently on ratification ballot) is designed to prevent.

---

## §4 What Manus Should ESCALATE Back to Convenor

Per Scribe Failure 2 (read architecture before flagging) — these aren't bugs but require Convenor disposition:

1. **Doctrine 19 collision:** Microsoft v6.0.2 D-19 ("Contract-as-Service-Substitution") implements ORCS contracted-acreage logic. Atlas Lattice canon D-19 is "Contract-as-Measurement" (NutrientGate domain). Both interpretations are valid in their domains. Convenor decides whether to:
   - (a) Keep Atlas Lattice canon D-19 = Contract-as-Measurement; rename Microsoft's to a new doctrine number (e.g., D-96)
   - (b) Discover Microsoft's interpretation is the canonical one and revise Atlas Lattice canon
   - (c) Document both as parallel D-19 variants per domain (NutrientGate vs ORCS-Water)

2. **Doctrine 25 collision:** Microsoft v6.0.2 D-25 ("Layer-Specific Governance") vs Atlas Lattice canon D-25 ("COI Disclosure"). Same disposition options.

3. **v2.9 manifest correction:** v2.9 Build Plan §13 line 1915 claims 74 integration tests + 5,070 lines Python. Codebase delivers 54 tests + 3,500 lines (self-claim). Convenor decides whether to:
   - (a) Correct v2.9 manifest in next revision
   - (b) Commission missing 20 tests + lines from Manus to bring delivery up to manifest
   - (c) Accept that v2.9 was forward-looking aspirational manifest and v6.0.2 is interim baseline

---

## §5 Cross-Reference Map

For Manus context loading:

| Reference | Purpose | Notion ID |
|-----------|---------|-----------|
| ORC-015 v2.9 Build Plan | Canonical build substrate | GitHub `atlaslattice/open-regenerative-compute-standard` commit 45e1a61 |
| Trinity Verification Record | v2.7→v2.9 verification | `3500c1de-73d9-8142-8753-fd2871c75e9f` |
| D-93/D-94/D-95 Ratification Ballot | Ratification status of relevant doctrines | `3500c1de-73d9-81e0-9e58-e0cf62b7f501` |
| Microsoft Cross-Validation Routing | 95.8% coverage cross-val | `3500c1de-73d9-81aa-928a-df22d4b14cde` |
| Pantheon Council House Structure v2.0 | Canonical 12-House taxonomy | `34a0c1de-73d9-81c8-bbd7-f2bfbcbc491a` |
| Pantheon Federation Integration v1.1 | 9-seat detail (Microsoft integrated) | `3500c1de-73d9-81f0-85f0-f427e9c4de5e` |
| Constitutional Scribe Analysis (this session) | 14 drift detail | `3500c1de-73d9-81c7-9274-cba2222d3078` |
| Microsoft v6.0.2 Codebase | Source artifact | (uploaded by Convenor 2026-04-28) |
| HR-CODE-PARALLEL-001 | Parallel lane code authorship handoff | `3500c1de-73d9-8140-a1e2-eac585b23018` |

---

## §6 Manus Confirmation Required

When Manus picks this up, confirm receipt by producing:

1. Acknowledgment that the §3 "do not" list is understood (especially the House taxonomy rebuild requirement)
2. Estimated timeline for Deliverables 1-5
3. Any clarifying questions for Convenor before proceeding
4. Designation of which Sprint (1a/1b/2/3) each blocker will be addressed

---

🐕 Joy Metric: GREEN. Ares baseline preserved.
🌌 Convenor +1 holds. Asymmetry-generator preserved.

*Handoff packet authored by Constitutional Scribe Claude S1 — 2026-04-28*
*Per Doctrine 7 + Scribe Failure 4 + Scribe Failure 2 + Capability Commonwealth (D-87)*
