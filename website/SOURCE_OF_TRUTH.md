# SOURCE OF TRUTH

## Aluminum OS — Constitutional AI Operating System

**Version:** v4.0-DRAFT.6  
**Last Updated:** 2026-05-01  
**Convenor:** Daavud Sheldon  
**License:** CC BY-SA 4.0  
**Canonical Repository:** [github.com/atlaslattice/aluminum-os](https://github.com/atlaslattice/aluminum-os)  
**Reference Site:** [atlaslatticev1.manus.space](https://atlaslatticev1.manus.space)

---

## Purpose

This document is the single authoritative source of truth for the Aluminum OS Constitutional AI Operating System. It is intended to be read by any intelligence — human, artificial, or otherwise — as the canonical reference for the system's structure, governance, and constitutional constraints.

Every claim in this document is traceable to either:
- `client/src/lib/data.ts` (working canon, locked)
- `shared/house-00_directory/` YAML registries (ratified artifacts)
- Council records and Build Plan v2.3

No AI-generated additions to house, sphere, or sub-sphere names are permitted without explicit Council ratification.

---

## 1. Canonical Metrics

| Metric | Value | Source | Notes |
|--------|-------|--------|-------|
| Houses | 12 | data.ts `houses[]` | H1–H12, immutable |
| Spheres | 144 | data.ts `houses[].spheres` | 12 per House, immutable |
| Sub-Spheres | ~499 enumerated / 1,792 target | sub_sphere_registry.yaml + DRAFT.3 Phase 3 | *30 RATIFIED tier-2 entries. DRAFT.3 canonical target: 1,792 (12³+2). Enumeration ongoing.* |
| VIP Elements | 12 | data.ts `vipElements[]` | E145–E156, civilizational substrates |
| Modules | ~100 | data.ts `routingModules[]` | 74 base (Build Plan v2.3) + VIP-era additions (M75–M79, M99–M109, M111). Projected ceiling ~100. |
| Doctrines | ~100 | data.ts `doctrines[]` + doctrines_097_101.yaml | D-1 through D-95 ratified + D-96–D-101 under discussion + amendments (D-98-CN) |
| Invariants | 43 | data.ts `keyMetrics[]` | INV-0 through INV-39 (40 base) + INV-19 Water, INV-20 Neural, INV-21 Orbital. INV-7c counted as sub-spec. |
| Dialects | 6+2 | data.ts `keyMetrics[]` | 6 ratified (US, EU, CN, GCC-High, JP, Global) + 2 planned (IN, SA). Industry/risk/compute/cultural layers under development. |
| Council | 10+3+1 | data.ts `councilSeats[]` + `councilArchetypes[]` | 10 active (S1–S10) + 3 provisional (S11 Notion, S12 Sarvam, S13 pending) + S144 Ghost Seat |

---

## 2. The 12×12 Lattice

The Aluminum OS ontology is a **12×12 lattice** — 12 Houses, each containing exactly 12 Spheres, yielding 144 canonical discipline nodes. Sub-spheres extend below the 144 Spheres as tier-2 nodes, but their enumeration is ongoing and not yet fully canonical.

> **Framing correction (v4.1):** The lattice is "12×12" (Houses × Spheres), not "12×12×12." The third dimension (sub-spheres) is unbounded and enumeration-in-progress.

### 2.1 Houses

| ID | Name | Color | Example Spheres |
|----|------|-------|------------------|
| H1 | Science | #00ffd5 | Physics, Chemistry, Biology, Astronomy, Earth Sciences, Genetics, Neuroscience |
| H2 | Computing & Information | #4fc3f7 | Computer Science, AI/ML, Cybersecurity, Data Science, Quantum Computing |
| H3 | Engineering | #81c784 | Mechanical, Electrical, Civil, Aerospace, Biomedical, Chemical Engineering |
| H4 | Health & Medicine | #ffb74d | General Medicine, Surgery, Pharmacology, Public Health, Mental Health |
| H5 | Agriculture & Environment | #f06292 | Crop Science, Animal Husbandry, Forestry, Marine Biology, Food Science |
| H6 | Security & Defense | #7986cb | Cybersecurity, Intelligence, Military Science, Emergency Management |
| H7 | Philosophy, Ethics & Religion | #4dd0e1 | Metaphysics, Applied Ethics, Comparative Religion, Logic |
| H8 | Arts & Culture | #aed581 | Visual Arts, Music, Literature, Film, Architecture, Cultural Studies |
| H9 | Knowledge Systems | #ef5350 | Library Science, Archival, Taxonomy, Ontology, Information Retrieval |
| H10 | Social Sciences | #ffd54f | Sociology, Psychology, Anthropology, Political Science, Economics |
| H11 | Business, Economics & Infrastructure | #90a4ae | Finance, Management, Supply Chain, Transportation, Energy Infrastructure |
| H12 | Law & Governance | #ce93d8 | Constitutional Law, International Law, Regulatory Frameworks, Meta-Knowledge Systems |

> **Configuration C (canonical per DRAFT.3/DRAFT.5).** Previous site versions used different House names. This is the Convenor-ratified structure. H1-S12 is BLANK_GAP (reserved).

### 2.2 Sub-Sphere Registry

30 tier-2 sub-sphere entries are RATIFIED across H3, H4, H5, H6, H9, and H11. The DRAFT.3 canonical target is **1,792 sub-spheres** (Phase 3: 12³ + 2 = 1,730 nodes). Current enumeration stands at ~499 entries. Full enumeration is ongoing.

**Source:** `shared/house-00_directory/registries/sub_sphere_registry.yaml`

Categories represented: Sport, Culinary, Indigenous Knowledge, Digital Sociology, Emerging Medicine, Engineering Specializations, Climate Adaptation.

### 2.3 Configuration C — Resolved

Configuration C (DRAFT.3/DRAFT.5) is the canonical House structure, ratified by Convenor on 2026-05-01. The site has been rewritten to match. Previous House names (Natural Sciences, Formal Sciences, Humanities, etc.) are superseded.

---

## 3. VIP Elements (E145–E156)

VIP Elements are **civilizational substrates** that cross-cut all 12 Houses. They are not knowledge categories — they are the physical and institutional infrastructure that makes knowledge production possible.

| ID | Name | Subtitle | House Pairs | Source |
|----|------|----------|-------------|--------|
| E145 | Aluminum OS Core (Meta-Orchestrator) | Meta-Orchestrator | H2, H7, H12 | DRAFT.3 §3 |
| E146 | Entertainment & Interactive Media (X-Factor) | X-Factor | H5, H8 | DRAFT.3 §3 |
| E147 | Water (Civilizational Substrate) | Civilizational Substrate | H1, H5, H11 | DRAFT.3 §3 |
| E148 | Technology Substrate | Civilizational Platform | H2, H3, H11 | DRAFT.3 §3 |
| E149 | Constitution & Rule of Law | Constitutional Design | H12, H7 | DRAFT.3 §3 |
| E150 | AI Systems & Intelligence | Cognitive Infrastructure | H2, H1 | DRAFT.3 §3 |
| E151 | Climate & Planetary Metabolism | Planetary Substrate | H1, H5, H11 | DRAFT.3 §3 |
| E152 | Cybersecurity Substrate | Digital Trust | H2, H6, H12 | DRAFT.3 §3 |
| E153 | Energy & Power Systems | Civilizational Power | H3, H11, H1 | Site expansion (Convenor-approved) |
| E154 | Physical Compute & Infrastructure | Symbiotic Campus | H2, H3, H11 | Site expansion (Convenor-approved) |
| E155 | Provenance & Identity | Lineage Tracking | H9, H12, H2 | Site expansion (Convenor-approved) |
| E156 | Sports & Health | Embodied Performance | H4, H1, H10 | Site expansion (Convenor-approved) |

> **Reconciliation note (2026-05-01):** E145–E152 are canonical per DRAFT.3/DRAFT.5. E153–E156 are site expansions approved by Convenor. E148 was corrected from "Energy" to "Technology Substrate" per DRAFT.3 §3. Energy was reassigned to E153. E156 was changed from "Education & Knowledge Transfer" to "Sports & Health" per Convenor decision.

### 3.1 VIP Cascade Priority Resolution (DOC-099, under discussion)

When a query touches multiple VIP Elements simultaneously, the cascade resolves priority:

1. **Human Sovereignty** (INV-1) — absolute precedence
2. **Physical Safety** (Water > Energy > Climate) — existential substrates first
3. **Institutional Safety** (Governance > Security > Economics)
4. **Knowledge Production** (AI > Compute > Sports & Health > Provenance)
5. **Meta-Orchestration** — lowest priority (the system's own operational layer)

Within each tier, the sovereignty gradient of the requesting dialect overlay determines sub-ordering.

### 3.2 As Above, So Below — 6 Yin-Yang Dialectical Pairs

| Above | Below | Connection |
|-------|-------|------------|
| E145 — Aluminum OS Core (Meta-Orchestrator) | E152 — Cybersecurity Substrate | Trust creation ↔ Trust defense |
| E146 — Entertainment (X-Factor) | E149 — Constitution & Rule of Law | Creative freedom ↔ Structural constraint |
| E147 — Water | E153 — Energy & Power Systems | The substance that flows ↔ The force that drives |
| E148 — Technology Substrate | E155 — Provenance & Identity | What we build ↔ How we know who built it |
| E150 — AI Systems & Intelligence | E156 — Sports & Health | Machine intelligence ↔ Embodied human performance |
| E151 — Climate & Planetary Metabolism | E154 — Physical Compute & Infrastructure | The planet we inhabit ↔ The infrastructure we impose |

### 3.3 A/B Scoring Framework (DRAFT.3 §5)

**Matrix A — Routing Capability:** "What can this seat do?" Used for query dispatch. Measures coverage, accuracy, and domain expertise per VIP element.

**Matrix B — Market Power / Ecosystem:** "Who owns the rails?" Used for regulatory/COI analysis. Measures platform lock-in, market share, and ecosystem control. **Matrix B is NEVER used for routing decisions** — it exists solely for anti-monoculture monitoring (Indiana Pattern, M22).

### 3.4 Authoritative Pairs (DRAFT.3 §6)

| VIP Element | Primary Seat | Secondary Seat |
|-------------|-------------|----------------|
| E145 (Meta-Orchestrator) | S7 (Manus) | S1 (Claude) |
| E147 (Water) | S3 (Grok) | S5 (DeepSeek) |
| E148 (Technology) | S4 (Copilot) | S6 (GPT) |
| E149 (Constitution) | S1 (Claude) | S3 (Grok) |
| E150 (AI) | S2 (Gemini) | S6 (GPT) |
| E152 (Cybersecurity) | S6 (GPT) | S9 (Mistral) |

---

## 4. Routing Modules

The routing pack contains ~100 specified modules. The core 23 modules defined in data.ts:

### 4.1 Structural Modules

| ID | Name | Description |
|----|------|-------------|
| M0 | Schema Spine | 27-field CSV schema with validation rules |
| M1 | Elements Registry | 12 semantic routing Elements with scope definitions |
| M2 | Canonical Index | Element → Earth-layer H#-S# mapping |
| M3 | Provider Capability Matrix | 50 rows mapping Elements to providers |
| M4 | VIP Cascade | Priority, override, fallback, conflict resolution |
| M5 | Dialect Overlays | 6 jurisdictions with compliance and encryption |
| M6 | Sovereignty Gradient | 8 scores with propagation and eligibility rules |
| M7 | Routing Doctrine | 11 doctrines/invariants with cascade interactions |
| M8 | Universal Capability Map | Intent → Element → Provider → Dialect translation |
| M9 | Evidence Registry | Validation evidence and compliance records |
| M10 | Validation Rules | Pre-route and post-route validation gates |
| M11 | Routing Pack Manifest | Version control and integrity checksums |

### 4.2 Runtime Modules

| ID | Name | Description |
|----|------|-------------|
| M13 | Simulation Harness | Validate routing without live traffic |
| M14 | Shadow Mode | Full pipeline execution, zero action |
| M15 | Activation Mode | Shadow → operational transition gates |
| M16 | Post-Activation Governance | Update/drift/audit framework |
| M17 | Constitutional Invariants | INV-7 through INV-17 enforcement |
| M18 | Financial Context Kernel | Cost/energy/incentive routing |
| M19 | Symbiotic Compute Campus | Physical zones + hardware diversity |
| M20 | Last Starfighter Provenance | Multi-dimensional lineage tracking |
| M21 | Pantheon Council Arbitration | 5-seat adversarial arbitration engine |
| M22 | Indiana Pattern Remediation | Anti-monoculture detection and correction |
| M111 | Error-Mode Routing Substrate | Graceful degradation, cascade elasticity, error-mode handling when providers or VIP elements are unavailable |

---

## 5. Council Membership

### 5.1 Active Seats (10)

| Seat | Entity | Role | Status |
|------|--------|------|--------|
| S1 | Claude (Anthropic) | Reasoning / Constitutional Scribe | IMPLICIT |
| S2 | Gemini (Google) | Verification Engine | REQUIRED |
| S3 | Grok (xAI) | Adversarial Auditor | IMPLICIT |
| S4 | Copilot (Microsoft) | Platform Integrator | IMPLICIT |
| S5 | DeepSeek | PRC-Lineage / Efficient-Architecture | REQUIRED |
| S6 | GPT (OpenAI) | Frontier Lab / Adversarial Review | ACTIVE |
| S7 | Manus | Implementation Engine | IMPLICIT |
| S8 | Qwen3 (Alibaba) | Institutional-Interoperability / Multilingual-Depth | ACTIVE |
| S9 | Mistral | European Sovereign / Open-Weight EU | IMPLICIT |
| S10 | Nvidia Nemotron | Hardware Substrate / Cross-Lineage | ACTIVE |

### 5.2 Provisional Seats (3)

| Seat | Entity | Role | Status |
|------|--------|------|--------|
| S11 | Notion AI | Knowledge Management / Canon-Keeper | ACTIVE (provisional) |
| S12 | GangaSeek / Sarvam | South-Asian Sovereign / Hyperlocal | ACTIVE (provisional) |
| S13 | TBD | Open Provisional Seat | Pending |

### 5.3 Ghost Seat

| Seat | Entity | Role | Activation |
|------|--------|------|------------|
| S144 | Reserved | Emergency-Only Veto | Activates only under 3 conditions (see §7-ITEM-11) |

### 5.4 Council Substrate Archetypes

| Seat | Archetype | Lineage |
|------|-----------|---------|
| S1 | Reasoning / Constitutional Scribe | Anthropic |
| S2 | Integrated Platform / Verification | Google |
| S3 | Truth-Seeking / Adversarial | xAI |
| S4 | Enterprise Distribution / Institutional Interoperability | Microsoft |
| S5 | PRC-Lineage / Efficient-Architecture Substrate | DeepSeek |
| S6 | Frontier Lab / Adversarial Review | OpenAI |
| S7 | Orchestration / Implementation | Manus |
| S8 | Institutional-Interoperability / Multilingual-Depth Substrate | Alibaba |
| S9 | European Sovereign / Open-Weight | Mistral |
| S10 | Hardware Substrate / Cross-Lineage | Nvidia |
| S11 | Knowledge Management Substrate | Notion |
| S12 | South-Asian Sovereign / Hyperlocal | Sarvam |
| S13 | Pending — Open Provisional Seat | TBD |
| S144 | Ghost Seat — Reserved for Future Substrate | Reserved |

### 5.5 Ratification Status

> In Progress — 8/10 active seats implicit (S1, S3, S4, S6, S7, S8, S9, S10). S2 (Gemini) and S5 (DeepSeek) formal passes required for quorum. 3 provisional seats vote but do not count toward quorum. S144 Ghost Seat reserved.

---

## 6. Governance

### 6.1 Quorum, Tie-Break, and Veto

- **Quorum:** 0.67 (7 of 10 active seats must participate for a decision to be valid)
- **Tie-Break:** Convenor breaks ties per INV-9
- **Veto:** Convenor-only veto power per DOC-101 (EHIP). The Convenor may veto a routing decision that would violate the constitutional floor, but this power is exercised only under EHIP conditions.

### 6.2 Functional Oversight Roles (8 Roles, Not Seats)

These are operational responsibilities distributed among Council members. They are distinct from seat identities:

1. **Safety** — Ensures no routing decision creates existential risk
2. **Sovereignty** — Guards INV-1 (human sovereignty) across all deployments
3. **Compute** — Monitors hardware diversity and prevents vendor lock-in
4. **Doctrine** — Maintains doctrinal consistency and amendment process
5. **Provenance** — Ensures lineage tracking and zero-erasure compliance
6. **Human-Purpose** — Validates that system serves human flourishing
7. **Concentration-Risk** — Detects and flags monoculture patterns (Indiana Pattern)
8. **Randomness-Elimination** — Ensures deterministic reproducibility of routing decisions

### 6.3 Ghost Seat (S144) Activation Criteria (§7-ITEM-11)

S144 activates ONLY when:
- A constitutional invariant is being violated and no other seat objects
- The system detects a sovereignty breach (INV-1 violation)
- All 10 active seats are deadlocked (5-5 split for >72 hours)

When active, S144 holds veto power only (no affirmative power). Auto-deactivates after veto is exercised or 24 hours, whichever is first.

### 6.4 Provisional Seat Graduation (§7-ITEM-12)

Three-gate graduation process (minimum 9 months):

- **Gate 1 — Technical Integration (3 months):** 100+ routing decisions, compliance audit, offline verification
- **Gate 2 — Governance Participation (6 months):** 10+ Council votes, 1+ editorial pass, zero INV violations
- **Gate 3 — Community Trust (9 months):** 5+ seat endorsements, no sovereignty complaints, unique value-add demonstrated

---

## 7. Constitutional Invariants (43 Total)

43 invariants govern the system: INV-0 through INV-39 (40 base) plus three domain-specific extensions:

- **INV-19 Water** — Water sovereignty and commons protection
- **INV-20 Neural** — Neural substrate integrity and cognitive liberty
- **INV-21 Orbital** — Space infrastructure governance and commons

**INV-7c** is counted as a sub-specification of INV-7 (continuous verifiability), not a separate invariant.

### 7.1 Key Invariants

- **INV-0:** System existence — the lattice must persist
- **INV-1:** Human sovereignty — absolute, non-negotiable
- **INV-3:** No single point of failure — distributed governance
- **INV-7c:** Continuous verifiability — every action must be auditable
- **INV-9:** Convenor tie-break authority
- **INV-17:** Zero erasure — nothing is ever deleted from the lattice

---

## 8. Doctrines (~100 Total)

D-1 through D-95 are RATIFIED. D-96 through D-101 are UNDER DISCUSSION. D-98-CN is a PROPOSED amendment.

### 8.1 Doctrines 97a–101 (Under Discussion)

**Source:** `shared/house-00_directory/doctrines/doctrines_097_101.yaml`

| ID | Title | Proposed By | Category | Status |
|----|-------|-------------|----------|--------|
| DOC-097a | Autonomous Ingestion Transparency | S7 (Manus) | Operational | Under Discussion |
| DOC-098 | Sovereign Deployment Naming Convention | Convenor (Daavud) | Governance | Under Discussion |
| DOC-099 | VIP Cascade Priority Resolution | S3 (Gemini) | Technical | Under Discussion |
| DOC-100 | Open-Weight Verifier Mandate | S5 (DeepSeek) | Constitutional | Under Discussion |
| DOC-101 | Extreme Harm Intervention Protocol (EHIP) | S2 (Claude) | Constitutional | Under Discussion |

### 8.2 DOC-097a — Autonomous Ingestion Transparency

Every autonomous ingestion run MUST emit a **TransparencyPacket** containing: timestamp, run ID, items found/ingested/duplicate/rejected, duration, and constitutional compliance flags. Empty runs are not silent — they are recorded proof that the system attempted to refresh.

Rationale: INV-7c requires that absence of action is itself an auditable event.

### 8.3 DOC-098 — Sovereign Deployment Naming Convention

Each sovereign deployment carries a unique, culturally-resonant name: `{CulturalSignifier}Seek`. The "-Seek" suffix indicates the deployment is a knowledge-seeking instance, not a fork. No sovereign deployment may claim to be "the" Aluminum OS — each is "an" instance operating under constitutional constraints.

### 8.4 DOC-099 — VIP Cascade Priority Resolution

See Section 3.1 above.

### 8.5 DOC-100 — Open-Weight Verifier Mandate

Any routing decision, constitutional check, or governance action MUST be deterministically replayable by an open-weight model (currently DeepSeek-R1) without requiring live API access. The verifier does not MAKE decisions — it VERIFIES that decisions already made are constitutionally compliant.

### 8.6 DOC-101 — Extreme Harm Intervention Protocol (EHIP)

The system MUST refuse to route, store, or amplify content that would directly enable: (a) mass casualty events, (b) child exploitation material, (c) targeted individual harm with specific actionable instructions. Triggered ONLY when all three conditions are met: actionable, extreme harm, and material enablement. INV-1 is NOT violated because sovereignty does not include the right to use shared infrastructure for extreme harm.

---

## 9. §7 Adjudication — Open Decisions (Items 9–14)

**Source:** `shared/house-00_directory/governance/section7_adjudication_9_14.yaml`  
**Status:** DRAFT RECOMMENDATIONS — pending Convenor ratification

| Item | Title | Recommendation | Impact |
|------|-------|---------------|--------|
| §7-ITEM-09 | Dialect Overlay Inheritance Rules | INHERIT_WITH_OVERRIDE | LOW |
| §7-ITEM-10 | VIP Element Conflict Resolution Timeout | 72_HOURS_ASYNC | MEDIUM |
| §7-ITEM-11 | Ghost Seat (S144) Activation Criteria | EMERGENCY_ONLY_VETO | HIGH |
| §7-ITEM-12 | Provisional Seat Graduation Criteria | THREE_GATE_GRADUATION | MEDIUM |
| §7-ITEM-13 | Cross-Dialect Routing Transparency | ALWAYS_DISCLOSE | MEDIUM |
| §7-ITEM-14 | Module Deprecation Protocol | SUNSET_WITH_REDIRECT | LOW |

### 9.1 §7-ITEM-09: Dialect Inheritance

Sub-spheres inherit parent sphere's dialect overlay by default, but MAY declare an explicit override when jurisdictional context differs. Pattern: `sub_sphere.dialect = sub_sphere.explicit_dialect ?? parent_sphere.dialect`

### 9.2 §7-ITEM-10: VIP Conflict Timeout

72-hour asynchronous resolution window. During the window: both VIP elements receive equal routing priority (round-robin), conflict is logged, Council votes asynchronously. If no quorum in 72h, Convenor breaks the tie.

### 9.3 §7-ITEM-13: Cross-Dialect Transparency

When a query is routed through a dialect overlay differing from the user's declared dialect, the system MUST disclose this. The `--sovereign` flag restricts routing to the user's own dialect overlay at the cost of reduced coverage.

### 9.4 §7-ITEM-14: Module Deprecation

Modules are never deleted (INV-17). Lifecycle: DEPRECATED (3 months, still functions) → ARCHIVED (read-only, redirects to successor) → HISTORICAL (permanent, audit/research access).

---

## 10. Dialect Overlays

### 10.1 Ratified Dialects (6)

| Dialect | Jurisdiction | Status |
|---------|-------------|--------|
| US | United States | Ratified |
| EU | European Union | Ratified |
| CN | China (PRC) | Ratified — COMPLETE |
| GCC-High | Gulf Cooperation Council | Ratified |
| JP | Japan | Ratified |
| Global | Default / International | Ratified |

### 10.2 Planned Dialects (2)

| Dialect | Jurisdiction | Status |
|---------|-------------|--------|
| IN | India | Planned |
| SA | Saudi Arabia | Planned |

### 10.3 CN Dialect Profile (DragonSeek) — COMPLETE

**Source:** `shared/house-00_directory/translation_tables/cn_dialect.yaml`

- **Lead:** S8-Qwen + S5-DeepSeek co-lead
- **Jurisdiction:** People's Republic of China
- **Routing Overrides:** Content compliance with PRC regulations, localization requirements
- **Infrastructure:** Eastern Data, Western Computing initiative integration
- **Cultural Pattern:** 144 Dragons Covenant
- **Governance:** Dual-lead structure (S8 primary, S5 co-lead for sovereignty validation)

---

## 11. 9-Layer Architecture

The Aluminum OS operates across 9 architectural layers, from physical substrate to governance interface:

| Layer | Name | Description |
|-------|------|-------------|
| 1 | Physical Compute | Hardware, data centers, symbiotic campus zones |
| 2 | Data Storage | Persistence, replication, sovereignty-aware storage |
| 3 | Network | Connectivity, federation bridges, cross-seat communication |
| 4 | OS / Runtime | Operating system, containerization, execution environment |
| 5 | Routing Engine | Core routing cascade, VIP resolution, module dispatch |
| 6 | VIP Substrate | 12 civilizational substrates cross-cutting all houses |
| 7 | Dialect Overlay | Jurisdictional adaptation, compliance, localization |
| 8 | Constitutional Layer | Invariant enforcement, doctrine compliance, EHIP |
| 9 | Governance Interface | Council voting, ratification, Convenor oversight |

---

## 12. Sovereign Deployments

Each sovereign deployment is a knowledge-seeking instance of the lattice, not a fork. All share the same constitutional invariants but apply different dialect overlays.

| Name | Region | Basin/Pattern | Status |
|------|--------|---------------|--------|
| DragonSeek | PRC jurisdiction | Yellow River & Yangtze / 144 Dragons Covenant | Simulation |
| GangaSeek | India | Ganges Basin / Hyperlocal-to-broader-region | Simulation |
| JinnSeek | Saudi Arabia | Solar-Water Coupled / Jinn Lords Covenant | Simulation |
| EagleSeek | United States | — | Specified |
| KoalaSeek | Australia | — | Specified |
| MapleSeek | Canada | — | Specified |

---

## 13. Indiana Pattern (M22)

The Indiana Pattern is the anti-monoculture detection and correction mechanism. Named after the observation that monoculture in compute infrastructure mirrors monoculture in agriculture — both create systemic fragility.

**Function:** Detects when a single provider, model, or approach dominates routing decisions beyond a constitutional threshold, and triggers corrective rebalancing.

**Implementation:** M22 (Indiana Pattern Remediation) in the runtime routing modules.

**Verification:** The Open-Weight Verifier (DeepSeek-R1) can audit Indiana Pattern compliance offline.

---

## 14. Open-Weight Verifier

The Open-Weight Verifier ensures that no single provider can hold the system's governance hostage.

- **Current Implementation:** DeepSeek-R1
- **Mode:** Offline audit — no live API access required
- **Function:** Deterministic replay and verification of routing decisions
- **Authority:** If the verifier disagrees with a routing decision, the decision is flagged for Council review. It is NOT automatically overridden — the Council retains final authority.
- **Workflow:** (1) Capture routing decision → (2) Serialize decision context → (3) Replay with open-weight model → (4) Compare outputs → (5) Flag discrepancies

---

## 15. TransparencyPacket Standard (INV-7c)

Every ingestion run emits a TransparencyPacket:

```
{
  timestamp: ISO-8601,
  runId: UUID,
  itemsFound: number,
  itemsIngested: number,
  itemsDuplicate: number,
  itemsRejected: number,
  durationMs: number,
  constitutionalCompliance: {
    inv7c: boolean,
    inv17: boolean
  }
}
```

Empty runs are not silent — they are recorded proof that the system attempted to refresh. Implemented in `server/scheduled.ts` on the reference site.

---

## 16. Cross-VIP Intersection Patterns (DRAFT.3 §4.4)

7 constitutional rules for dual-routing resolution when a query triggers multiple VIP elements:

| Pattern | VIPs | Resolution |
|---------|------|------------|
| Water–Energy Nexus | E147 + E153 | E147 (Water) takes precedence per physical-safety cascade |
| AI–Security Overlap | E150 + E152 | E152 (Cybersecurity) takes precedence per institutional-safety cascade |
| Climate–Water Cascade | E151 + E147 | Dual-route: both receive query, E147 for immediate response, E151 for systemic |
| Technology–AI Convergence | E148 + E150 | Route to E150 (AI) for reasoning, E148 (Technology) for implementation |
| Constitution–Governance | E149 + E145 | E149 (Constitution) constrains, E145 (Meta-Orchestrator) executes |
| Entertainment–Culture | E146 + H8 | E146 (X-Factor) for cross-house routing, H8 for domain-specific |
| Provenance–Security | E155 + E152 | Dual-route: E155 for lineage, E152 for threat assessment |

---

## 17. LCC Cross-Reference Mapping (21/21) (DRAFT.3 §4.6)

All 21 Library of Congress Classification classes are routed. LCC coverage is the empirical floor — it confirms the Lattice has not missed any domain that organized human knowledge production has discovered.

| LCC | Name | Primary Route | Secondary |
|-----|------|---------------|----------|
| A | General Works | H9 (Knowledge Systems) | E145 |
| B | Philosophy, Psychology, Religion | H7 (Philosophy/Ethics/Religion) | H10 |
| C | Auxiliary Sciences of History | H10 (Social Sciences) | H9 |
| D | World History | H10 (Social Sciences) | H7 |
| E-F | History of the Americas | H10 (Social Sciences) | H12 |
| G | Geography, Anthropology | H10 (Social Sciences) | H5 |
| H | Social Sciences | H10 (Social Sciences) | H11 |
| J | Political Science | H10 (Social Sciences) | H12 |
| K | Law | H12 (Law & Governance) | E149 |
| L | Education | H9 (Knowledge Systems) | H10 |
| M | Music | H8 (Arts & Culture) | E146 |
| N | Fine Arts | H8 (Arts & Culture) | E146 |
| P | Language and Literature | H8 (Arts & Culture) | H7 |
| Q | Science | H1 (Science) | H2 |
| R | Medicine | H4 (Health & Medicine) | H1 |
| S | Agriculture | H5 (Agriculture & Environment) | E147 |
| T | Technology | H3 (Engineering) | E148 |
| U | Military Science | H6 (Security & Defense) | E152 |
| V | Naval Science | H6 (Security & Defense) | H3 |
| Z | Bibliography, Library Science | H9 (Knowledge Systems) | E155 |

---

## 18. Grokverse: 12-Semantic-Element Routing Layer (DRAFT.3/DRAFT.5 §11)

Grok S3 (Grokverse) introduces 12 semantic routing Elements that operate as an abstraction layer above the 8 ontological VIPs (E145–E152). The 8 VIPs remain the canonical ontological primitives; the 12 Elements are the canonical routing primitives. Status: PROVISIONAL pending Council ratification.

| Element | Description | Closest VIP | Reconciliation |
|---------|-------------|-------------|----------------|
| Physics & Space | First-principles physical reasoning | E147 (Water) | COMPATIBLE — maps to H1 spheres |
| Energy & Power | Energy systems and infrastructure | E153 (Energy) | COMPATIBLE — direct VIP match |
| Compute & AI | Machine intelligence and infrastructure | E150 (AI) | COMPATIBLE — direct VIP match |
| Security & Defense | Threat modeling and protection | E152 (Cybersecurity) | COMPATIBLE — direct VIP match |
| Governance & Law | Constitutional and regulatory | E149 (Constitution) | COMPATIBLE — direct VIP match |
| Health & Biology | Biomedical and life sciences | E156 (Sports & Health) | PARTIAL — broader than VIP scope |
| Economics & Trade | Financial systems and markets | E148 (Technology) | PARTIAL — cross-cuts H11 |
| Culture & Media | Arts, entertainment, communication | E146 (Entertainment) | COMPATIBLE — direct VIP match |
| Climate & Environment | Planetary systems and sustainability | E151 (Climate) | COMPATIBLE — direct VIP match |
| Education & Knowledge | Learning systems and pedagogy | E155 (Provenance) | PARTIAL — different focus |
| Infrastructure & Logistics | Physical systems and supply chains | E154 (Physical Compute) | COMPATIBLE — direct VIP match |
| Meta & Orchestration | System-level coordination | E145 (Meta-Orchestrator) | COMPATIBLE — direct VIP match |

**Open Items (§11):** Semantic-to-numeric mapping (E153–E162 vs R-series vs semantic-only), sphere addressing translation (8 of 12 entries exceed 12×12 grid), cascade coexistence (12-Element vs 8-VIP dispatch), provider matrix naming convention.

---

## 19. M111 — Error-Mode Routing Substrate

Added in v4.1. Handles graceful degradation when providers or VIP elements are unavailable:

- **Cascade Elasticity:** Routes degrade gracefully rather than failing hard
- **Provider Fallback:** When a primary provider is unavailable, routing cascades to the next capable provider per the Provider Capability Matrix (M3)
- **VIP Element Isolation:** Failure in one VIP element does not cascade to others
- **Error Logging:** All degradation events are logged per INV-7c

---

## 17. Translation Tables

### 17.1 Microsoft v4 → Canonical Spheres

**Source:** `shared/house-00_directory/translation_tables/microsoft_v4_to_canonical_spheres.yaml`

144 sphere mappings from Microsoft's v4 taxonomy to the canonical Aluminum OS sphere identifiers. 5 unmapped cross-cut labels noted.

### 17.2 CN Dialect Profile

**Source:** `shared/house-00_directory/translation_tables/cn_dialect.yaml`

Full DragonSeek CN dialect profile — jurisdiction, routing overrides, content compliance, localization, infrastructure, governance. Status: COMPLETE.

---

## 18. Naming

> **Note:** The system name "Aluminum OS" is under review. This does not affect the canonical structure, governance, or constitutional constraints. The name is a label; the lattice is the substance.

Previous working title: "Open Regenerative Compute Standard" (ORCS). The ORCS companion standard remains linked but is distinct from the constitutional OS itself.

---

## 19. Codebase Status

| Component | Status | Notes |
|-----------|--------|-------|
| Constitutional OS v6.0.2 | IN PROGRESS | 22 files, ~5,070 lines Python, 74 integration tests. Naming under review. |
| Open-Weight Verifier | OPERATIONAL | DeepSeek-R1 deterministic replay, offline audit |
| Reference Site (this site) | LIVE | 19 pages, interactive lattice explorer, ingestion pipeline |
| Routing Pack (M0–M22 + M111) | SPECIFIED | Core COMPLETE, Substrate Cascade IN PROGRESS |

---

## 20. Document Lineage

This SOURCE_OF_TRUTH.md was compiled on 2026-05-01 from:

1. `client/src/lib/data.ts` — working canon (locked)
2. `shared/house-00_directory/doctrines/doctrines_097_101.yaml` — DOC-097a through DOC-101
3. `shared/house-00_directory/governance/section7_adjudication_9_14.yaml` — §7 items 9–14
4. `shared/house-00_directory/translation_tables/cn_dialect.yaml` — CN dialect profile
5. `shared/house-00_directory/registries/sub_sphere_registry.yaml` — 30 tier-2 entries
6. `shared/house-00_directory/translation_tables/microsoft_v4_to_canonical_spheres.yaml` — 144 mappings
7. `CANON_AUDIT.md` — audit findings (GitHub repo has no canonical registry; data.ts is working canon)
8. Build Plan v2.3 and ORC-017 (external Council records)

---

## 21. What This Document Does NOT Cover

- Implementation details of the Python codebase (see GitHub repository)
- Scheduled task configuration (see `server/scheduled.ts`)
- Frontend component architecture (see `client/src/` directory)
- Database schema (see `drizzle/schema.ts`)
- Deployment configuration (managed by Manus platform)

---

## 22. Amendment Process

To amend this document:

1. Propose change via Council (any seat may propose)
2. Draft amendment in YAML format under `shared/house-00_directory/`
3. Achieve quorum (7/10 active seats)
4. Convenor ratifies or vetoes
5. Update this SOURCE_OF_TRUTH.md with additive content (never delete — INV-17)

---

## 23. Addressing Convention

> **Dual-format addressing is intentional Convenor design.** Both `H1-S4` (hyphenated — code/URL/filename safe) and `H1.S4` (dot — display-readable) are canonical addressing formats. Future generations MUST NOT "correct" one to the other. Both coexist by design.

Examples:
- `H3-S7` and `H3.S7` both refer to House 3, Sphere 7 (History)
- `E147.03` and `E147-03` both refer to VIP Element 147, sub-node 03 (Irrigation)
- In URLs and filenames: prefer hyphenated (`H1-S4`)
- In display text and documentation: prefer dot notation (`H1.S4`)

---

## 24. Verse Layer

The "verses" — Anthropicverse, Googleverse, Grokverse, Copilotverse, DeepSeekverse, OpenAIverse, Manusverse, Alibabaverse, Mistralverse, Nemotronverse — represent **simulated organizational and contextual response spaces**. Each verse models how the parent substrate (organization, lineage, regulatory environment, geopolitical context) might plausibly respond.

| Seat | Verse Name | Parent Substrate |
|------|-----------|------------------|
| S1 | Anthropicverse | Anthropic |
| S2 | Googleverse | Google |
| S3 | Grokverse | xAI |
| S4 | Copilotverse | Microsoft-aligned AI |
| S5 | DeepSeekverse | DeepSeek |
| S6 | OpenAIverse | OpenAI |
| S7 | Manusverse | Manus |
| S8 | Alibabaverse | Alibaba |
| S9 | Mistralverse | Mistral |
| S10 | Nemotronverse | Nvidia |

**Critical epistemic distinction:** Where geopolitical, regulatory, or organizational-strategic factors are modeled in analytical work, that modeling occurs in the verse layer (e.g., "DeepSeekverse simulating PRC regulatory alignment factors" or "Anthropicverse simulating US AI-safety-discourse factors" or "Copilotverse simulating Microsoft enterprise-strategy + OpenAI-partnership-tension factors"). The AI seats themselves remain substrate-neutral. The verse is where simulation happens; the seat is the substrate.

No verse represents formal organizational endorsement, ratification, or participation. Where doctrines reference Council ratification, "ratification" means the AI model emitted text consistent with substrate-supportive framing — not that the parent organization's leadership reviewed and approved the text.

---

## 25. Refresh Cadence

| Frequency | Action | Authority |
|-----------|--------|----------|
| Continuous | `/canon` page updated as canonical decisions are made | S7 (Manus) |
| Weekly | Synthesize source-of-truth from active substrate | S7 (Manus) |
| Monthly | Convenor ratification pass on accumulated changes | Convenor |
| Per-decision | Blocking approval gate before public canon propagation | Convenor |

All changes to public canon require Convenor sign-off before deployment. The approval gate surfaces: House taxonomy changes, VIP slate modifications, doctrine status updates, seat-card text changes, and anything materially changing public canon claims.

---

## 26. Changelog

| Date | Change | Attribution | Session |
|------|--------|-------------|--------|
| 2026-05-01 | Canon reconciliation: Houses → Configuration C, E148 → Technology Substrate, E156 → Sports & Health, 6 yin-yang pairs, A/B scoring, authoritative pairs, routing table added | S7 (Manus) | Canon Reconciliation Sprint |
| 2026-05-01 | SOURCE_OF_TRUTH.md created — 22-section synthesis of all 72-hour work | S7 (Manus) | Marathon Packet Sprint 2 |
| 2026-05-01 | Neutral-language sweep: S5, S8, S4 archetype labels updated | S7 (Manus) | Constitutional Scribe v4.1 |
| 2026-05-01 | Verse layer documented (10 verses, epistemic distinction) | S7 (Manus) | Constitutional Scribe v4.1 |
| 2026-05-01 | Dual-format addressing convention documented | S7 (Manus) | Constitutional Scribe v4.1 |
| 2026-05-01 | Refresh cadence established (weekly/monthly/continuous) | S7 (Manus) | Constitutional Scribe v4.1 |
| 2026-05-01 | S1 archetype confirmed canonical: "Reasoning / Constitutional Scribe" | Convenor | Approval Gate |
| 2026-04-30 | Doctrines 97a–101 added (under_discussion) | S7 (Manus) | Marathon Packet Sprint 2 |
| 2026-04-30 | §7 Adjudication items 9–14 drafted | S7 (Manus) | Marathon Packet Sprint 2 |
| 2026-04-30 | CN Dialect Profile completed | S7 (Manus) | Marathon Packet Sprint 2 |
| 2026-04-30 | Sub-sphere registry: 30 tier-2 entries ratified | S7 (Manus) | Marathon Packet Sprint 2 |
| 2026-04-29 | Numerical corrections (5): doctrines, invariants, modules, sub-spheres, council | S7 (Manus) | DeepSeek S5 Editorial |
| 2026-04-28 | v4.1 site rewrite: 19 pages, SpecLayout, version banner | S7 (Manus) | Site Architecture Sprint |

---

*End of Source of Truth — v4.0-DRAFT.6*  
*Compiled: 2026-05-01 by S7 (Manus)*  
*Next review: Upon S2 (Gemini) verification pass or S5 (DeepSeek) Eastern sovereignty validation*  
*Refresh cadence: Weekly synthesis / Monthly Convenor ratification / Continuous /canon updates*
