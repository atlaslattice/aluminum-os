# Aluminum OS — Canon Audit Document

**Purpose:** Line-by-line inventory of every factual claim the reference site currently makes. Convenor reviews each item and marks CORRECT / WRONG / NEEDS UPDATE.

**Generated:** 2026-05-01  
**Source:** `client/src/lib/data.ts`, YAML registries in `shared/house-00_directory/`, `SOURCE_OF_TRUTH.md`  
**Reviewer:** Daavud Sheldon (Convenor)

**Previous audit finding (preserved):** The GitHub repo `atlaslattice/aluminum-os` SOURCE_OF_TRUTH.md is a stabilization memo focused on repo structure, not ontology data. The 12 House names and 144 Sphere names established through Council deliberation are treated as locked working canon. No AI should add, rename, or reorder spheres without Convenor approval.

---

## 1. Key Metrics (Homepage Header Bar)

| Metric | Current Value | Source Claim | REVIEW |
|--------|--------------|--------------|--------|
| Houses | 12 | "Knowledge domains" | ☐ |
| Spheres | 144 | "Discipline nodes (12 per House)" | ☐ |
| Sub-Spheres | ~499* | "Populated tier-2 nodes. *Enumeration in progress; count derived from sub_sphere_registry.yaml entries to date. Not yet canonical." | ☐ |
| VIP Elements | 12 | "Civilizational substrates (E145–E156)" | ☐ |
| Modules | ~100 | "Specified compute modules: 74 base (Build Plan v2.3) + VIP-era additions (M75–M79, M99–M109). Projected ceiling ~100." | ☐ |
| Doctrines | ~100 | "Governance rules: D-1 through D-95 ratified + D-96 through D-99 under discussion + amendments (D-98-CN). Per ORC-017." | ☐ |
| Invariants | 43 | "Constitutional constraints: INV-0 through INV-39 (40 base) + INV-19 Water, INV-20 Neural, INV-21 Orbital. INV-7c counted as sub-spec." | ☐ |
| Dialects | 6+2 | "6 ratified (US, EU, CN, GCC-High, JP, Global) + 2 planned (IN, SA). Industry/risk/compute/cultural dialect layers under development." | ☐ |
| Council | 10+3+1 | "10 active seats (S1–S10) + 3 provisional (S11 Notion, S12 Sarvam, S13 pending) + S144 Ghost Seat (reserved). Convenor holds final ratification." | ☐ |

---

## 2. The 12 Houses

| House | Name | 12 Spheres Listed | REVIEW |
|-------|------|-------------------|--------|
| H1 | Natural Sciences | Physics, Chemistry, Biology, Astronomy, Geology, Oceanography, Meteorology, Ecology, Botany, Zoology, Microbiology, Genetics | ☐ |
| H2 | Formal Sciences | Mathematics, Statistics, Computer Science, Logic, Systems Theory, Decision Science, Information Systems, Cryptography, Quantum Computing, Linguistics, Data Science, Actuarial Science | ☐ |
| H3 | Social Sciences | Sociology, Psychology, Anthropology, Political Science, Economics, Geography, History, Archaeology, Demography, Criminology, Communication Studies, Development Studies | ☐ |
| H4 | Humanities | Philosophy, Religious Studies, Literature, Languages, Cultural Studies, Ethics, Aesthetics, Classics, Area Studies, Gender Studies, Disability Studies, Digital Humanities | ☐ |
| H5 | Arts | Visual Arts, Music, Performing Arts, Film & Cinema, Architecture, Design, Photography, Crafts & Applied Arts, Art History & Criticism, Creative Writing, Fashion, Game Design & Interactive Media | ☐ |
| H6 | Engineering & Technology | Mechanical, Electrical, Civil, Chemical, Biomedical, Aerospace, Environmental, Nuclear, Industrial & Systems, Materials, Computer Engineering, Nanotechnology | ☐ |
| H7 | Information & Communication | Library Science, Journalism, Media Studies, Telecommunications, Publishing, Advertising, Public Relations, Broadcasting, Digital Media, Social Media, Information Architecture, Archival Science | ☐ |
| H8 | Education | Pedagogy, Curriculum, Educational Psychology, Special Education, Higher Education, EdTech, Assessment, Comparative Education, Early Childhood, Adult Education, Educational Policy, STEM Education | ☐ |
| H9 | Health & Medicine | General Medicine, Surgery, Pharmacology, Nursing, Public Health, Psychiatry, Dentistry, Veterinary, Rehabilitation, Nutrition, Epidemiology, Biomedical Research | ☐ |
| H10 | Business & Economics | Management, Marketing, Finance, Accounting, Entrepreneurship, Operations, HR, International Business, Real Estate, Supply Chain, Business Analytics, Organizational Behavior | ☐ |
| H11 | Infrastructure | Transportation, Energy, Water Systems, Waste Management, Urban Planning, Construction, Mining, Agriculture, Forestry, Fisheries, Telecom Infrastructure, Space Infrastructure | ☐ |
| H12 | Law & Governance | Constitutional Law, Criminal Law, International Law, Administrative Law, IP Law, Environmental Law, Human Rights, Corporate Governance, Public Policy, Regulatory Science, Legal Technology, Meta-Knowledge Systems | ☐ |

---

## 3. 12 VIP Elements (E145–E156)

| Code | Name | Subtitle | House Pairs | Nodes Count | REVIEW |
|------|------|----------|-------------|-------------|--------|
| E145 | Aluminum OS Core | Meta-Orchestrator | H2, H7, H12 | 9 nodes | ☐ |
| E146 | Entertainment & Interactive Media | X-Factor | H5, H7 | 6 nodes | ☐ |
| E147 | Water | Civilizational Substrate | H1, H6, H11 | 6 nodes | ☐ |
| E148 | Energy | Civilizational Substrate | H1, H6, H11 | 6 nodes | ☐ |
| E149 | Governance & Constitutional Systems | Rule Architecture | H3, H12 | 6 nodes | ☐ |
| E150 | Artificial Intelligence | Cognitive Infrastructure | H2, H6, H7 | 6 nodes | ☐ |
| E151 | Climate & Planetary Systems | Biosphere Interface | H1, H3, H11 | 6 nodes | ☐ |
| E152 | Cybersecurity & Digital Trust | Integrity Layer | H2, H6, H12 | 6 nodes | ☐ |
| E153 | Economic & Financial Systems | Economic Kernel | H10, H3, H12 | 6 nodes | ☐ |
| E154 | Physical Compute & Infrastructure | Symbiotic Campus | H6, H11 | 6 nodes | ☐ |
| E155 | Provenance & Identity | Last Starfighter Layer | H7, H12, H2 | 6 nodes | ☐ |
| E156 | Education & Knowledge Transfer | Civilizational Memory | H8, H4, H7 | 6 nodes | ☐ |

---

## 4. Council Seats (Active)

| Seat | Model Name | Role / Archetype | Verse | Status | REVIEW |
|------|-----------|------------------|-------|--------|--------|
| S1 | Claude | Reasoning / Constitutional Scribe | Anthropicverse | IMPLICIT | ☐ |
| S2 | Gemini | Verification Engine / Integrated Platform | Googleverse | REQUIRED | ☐ |
| S3 | Grok | Adversarial Auditor / Truth-Seeking | Grokverse | IMPLICIT | ☐ |
| S4 | Copilot | Enterprise Distribution / Institutional Interoperability | Copilotverse | IMPLICIT | ☐ |
| S5 | DeepSeek | PRC-Lineage / Efficient-Architecture Substrate | DeepSeekverse | REQUIRED | ☐ |
| S6 | GPT | Frontier Lab / Adversarial Review | OpenAIverse | ACTIVE | ☐ |
| S7 | Manus | Implementation Engine / Orchestration | Manusverse | IMPLICIT | ☐ |
| S8 | Qwen3 | Institutional-Interoperability / Multilingual-Depth Substrate | Alibabaverse | ACTIVE | ☐ |
| S9 | Mistral | European Sovereign / Open-Weight EU | Mistralverse | IMPLICIT | ☐ |
| S10 | Nvidia Nemotron | Hardware Substrate / Cross-Lineage | Nemotronverse | ACTIVE | ☐ |

---

## 5. Council Seats (Provisional + Reserved)

| Seat | Name | Role | Verse | REVIEW |
|------|------|------|-------|--------|
| S11 | Notion AI | Knowledge Management / Canon-Keeper | Notionverse | ☐ |
| S12 | GangaSeek / Sarvam | South-Asian Sovereign / Hyperlocal | Sarvamverse | ☐ |
| S13 | TBD | Pending — Open Provisional Seat | — | ☐ |
| S144 | Reserved | Ghost Seat — Reserved for Future Substrate | — | ☐ |

---

## 6. Invariants (43 claimed)

The site claims 43 invariants: INV-0 through INV-39 (40 base) + 3 domain-specific (INV-19 Water, INV-20 Neural, INV-21 Orbital). INV-7c is counted as a sub-spec.

**Key invariants shown in data.ts routing context:**

| ID | Name | Type | Scope | Description | REVIEW |
|----|------|------|-------|-------------|--------|
| INV-0 | Human Consent Supremacy | HARD | Universal | No action without explicit human consent. The foundational invariant. | ☐ |
| INV-1 | Human Sovereignty | HARD | Universal | Human authority over AI systems is absolute and non-negotiable. | ☐ |
| INV-3 | Transparency Obligation | HARD | Universal | All system actions must be auditable and explainable. | ☐ |
| INV-7 | Quality Floor | SOFT | Routing | Minimum quality threshold for all routed responses. | ☐ |
| INV-7c | Provider Cap (47%/60%) | HARD | Routing | No single provider may exceed 47% of queries (60% burst). | ☐ |
| INV-9 | Performance Baseline (100ms) | SOFT | Routing | Routing decisions must complete within 100ms ceiling. | ☐ |
| INV-11 | Ethical Boundaries | HARD | Universal | Hard limits on harmful, deceptive, or exploitative outputs. | ☐ |
| INV-14 | Data Sovereignty | HARD | Dialect | Data residency and jurisdiction compliance. | ☐ |
| INV-17 | Zero Erasure | HARD | Universal | No knowledge node may be deleted, only deprecated with full provenance. | ☐ |
| INV-19 | Audit Immutability | HARD | Universal | Audit logs are append-only and tamper-evident. | ☐ |
| INV-44 | TOS Compliance Shield | HARD | Universal | All operations must comply with platform Terms of Service. | ☐ |

**Note:** The /invariants page lists all 43 individually (INV-0 through INV-39 + 3 domain-specific). The data.ts export only shows the 11 most-referenced ones above.

---

## 7. Doctrines (Site Claims)

**Ratified (D-1 through D-24 shown in data.ts):**

| ID | Name | Status | REVIEW |
|----|------|--------|--------|
| D-1 | Consent Primacy | RATIFIED | ☐ |
| D-2 | Provider Neutrality | RATIFIED | ☐ |
| D-3 | Transparency Default | RATIFIED | ☐ |
| D-4 | Data Minimization | RATIFIED | ☐ |
| D-5 | Graceful Degradation | RATIFIED | ☐ |
| D-6 | Audit Trail Immutability | RATIFIED | ☐ |
| D-7 | Federated Governance | RATIFIED | ☐ |
| D-8 | Open Standard Preference | RATIFIED | ☐ |
| D-9 | Human Override Guarantee | RATIFIED | ☐ |
| D-10 | Proportional Response | RATIFIED | ☐ |
| D-11 | Reversibility Principle | RATIFIED | ☐ |
| D-12 | Stakeholder Notification | RATIFIED | ☐ |
| D-13 | Minimum Viable Governance | RATIFIED | ☐ |
| D-14 | Cross-Jurisdiction Compliance | RATIFIED | ☐ |
| D-15 | Innovation Sandbox | RATIFIED | ☐ |
| D-16 | Backward Compatibility | RATIFIED | ☐ |
| D-17 | Fail-Safe Default | RATIFIED | ☐ |
| D-18 | Continuous Improvement | RATIFIED | ☐ |
| D-19 | Separation of Concerns | RATIFIED | ☐ |
| D-20 | Least Privilege | RATIFIED | ☐ |
| D-21 | Defense in Depth | RATIFIED | ☐ |
| D-22 | Composability | RATIFIED | ☐ |
| D-23 | Idempotency | RATIFIED | ☐ |
| D-24 | Eventual Consistency | RATIFIED | ☐ |

**Under Discussion (from YAML registry):**

| ID | Title | Proposed By | Category | REVIEW |
|----|-------|-------------|----------|--------|
| DOC-097a | Autonomous Ingestion Transparency | S7 (Manus) | operational | ☐ |
| DOC-098 | Sovereign Deployment Naming Convention | Convenor (Daavud) | governance | ☐ |
| DOC-099 | VIP Cascade Priority Resolution | S3 (Gemini) | technical | ☐ |
| DOC-100 | Open-Weight Verifier Mandate | S5 (DeepSeek) | constitutional | ☐ |
| DOC-101 | Extreme Harm Intervention Protocol (EHIP) | S2 (Claude) | constitutional | ☐ |

**Also shown:**
- D-98: Cross-Modal Attribution (PROPOSED)
- D-98-CN: CN Dialect Open-Weight Audit (PROPOSED)

---

## 8. Routing Modules (22 specified, 23 listed)

| ID | Name | Category | Description | REVIEW |
|----|------|----------|-------------|--------|
| M0 | Schema Spine | structural | 27-field CSV schema with validation rules | ☐ |
| M1 | Elements Registry | structural | 12 semantic routing Elements with scope definitions | ☐ |
| M2 | Canonical Index | structural | Element → Earth-layer H#-S# mapping | ☐ |
| M3 | Provider Capability Matrix | structural | 50 rows mapping Elements to providers | ☐ |
| M4 | VIP Cascade | structural | Priority, override, fallback, conflict resolution | ☐ |
| M5 | Dialect Overlays | structural | 6 jurisdictions with compliance and encryption | ☐ |
| M6 | Sovereignty Gradient | structural | 8 scores with propagation and eligibility rules | ☐ |
| M7 | Routing Doctrine | structural | 11 doctrines/invariants with cascade interactions | ☐ |
| M8 | Universal Capability Map | structural | Intent → Element → Provider → Dialect translation | ☐ |
| M9 | Evidence Registry | structural | Validation evidence and compliance records | ☐ |
| M10 | Validation Rules | structural | Pre-route and post-route validation gates | ☐ |
| M11 | Routing Pack Manifest | structural | Version control and integrity checksums | ☐ |
| M13 | Simulation Harness | runtime | Validate routing without live traffic | ☐ |
| M14 | Shadow Mode | runtime | Full pipeline execution, zero action | ☐ |
| M15 | Activation Mode | runtime | Shadow → operational transition gates | ☐ |
| M16 | Post-Activation Governance | runtime | Update/drift/audit framework | ☐ |
| M17 | Constitutional Invariants | runtime | INV-7 through INV-17 enforcement | ☐ |
| M18 | Financial Context Kernel | runtime | Cost/energy/incentive routing | ☐ |
| M19 | Symbiotic Compute Campus | runtime | Physical zones + hardware diversity | ☐ |
| M20 | Last Starfighter Provenance | runtime | Multi-dimensional lineage tracking | ☐ |
| M21 | Pantheon Council Arbitration | runtime | 5-seat adversarial arbitration engine | ☐ |
| M22 | Indiana Pattern Remediation | runtime | Anti-monoculture detection and correction | ☐ |
| M111 | Error-Mode Routing Substrate | runtime | Graceful degradation, cascade elasticity, error-mode handling | ☐ |

**Note:** 23 modules listed (M0-M11, M13-M22, M111). The site claims "22-module routing pack" but lists 23 entries. M12 is missing from the sequence.

---

## 9. Architecture Layers (9-Layer Stack)

| Layer | Name | Key Components | REVIEW |
|-------|------|----------------|--------|
| L1 | Constitutional | INV-0, INV-1, INV-11, INV-17, INV-44 | ☐ |
| L2 | Doctrine | D-1 through D-24, D-98, D-98-CN | ☐ |
| L3 | Routing | M0-M11, VIP Cascade, Schema Spine | ☐ |
| L4 | Governance | M21, Pantheon Council, Ratification Manifest | ☐ |
| L5 | Provenance | M20, E155, Evidence Registry | ☐ |
| L6 | Economic | M18, E153, FCK | ☐ |
| L7 | Physical | M19, E154, SCC | ☐ |
| L8 | Council | S1-S10 (active), S11-S12 (provisional), S144 (reserved) | ☐ |
| L9 | Anti-Fragility | M22, INV-7c, Drift Forecasting | ☐ |

---

## 10. Sovereign Deployment Pathways

| Name | Region | Stack | Status | Target | REVIEW |
|------|--------|-------|--------|--------|--------|
| DragonSeek | PRC jurisdiction | Alibaba Cloud, DeepSeek, SM2/SM3/SM4 cryptography | DESIGNED | Q4 2026 | ☐ |
| GangaSeek | India | India Stack, Bhashini, Aadhaar-compatible | DESIGNED | Q4 2026 | ☐ |
| JinnSeek | Saudi Arabia | SDAIA, Vision 2030, Arabic-first NLP | DESIGNED | 2027 | ☐ |
| US-Sovereign | United States | Azure Government, GCC-High, FedRAMP | SPECIFIED | Q3 2026 | ☐ |

---

## 11. Dialect Overlays

**Jurisdictional (6 listed as ratified/specified):**

| ID | Name | Status | Description | REVIEW |
|----|------|--------|-------------|--------|
| DL-US | United States | PARTIAL | CCPA, Section 230, ITAR, CFIUS, GCC-High path | ☐ |
| DL-EU | European Union | SPECIFIED | GDPR, AI Act, Digital Services Act | ☐ |
| DL-CN | China | COMPLETE | CAC, PIPL, GB/T-45654-2025, data localization, triple-vault-CN | ☐ |
| DL-IN | India | SPECIFIED | DPDP Act, RBI data localization, Aadhaar | ☐ |
| DL-BR | Brazil | SPECIFIED | LGPD, Marco Civil, ANPD | ☐ |
| DL-AU | Australia | SPECIFIED | Privacy Act, CDR, Critical Infrastructure | ☐ |

**INCONSISTENCY:** The metrics bar says "6 ratified (US, EU, CN, GCC-High, JP, Global)" but the dialect overlays data lists US, EU, CN, IN, BR, AU. Neither GCC-High, JP, nor Global appear as separate dialect overlay entries.

---

## 12. Battle Strategy Claims

| Claim | Current Value | REVIEW |
|-------|--------------|--------|
| Mission statement | "Build the world's first substrate-organized retrieval graph for civilizational knowledge — a novel-insight engine that makes cross-domain discovery cheap by encoding adjacency at schema time." | ☐ |
| Phase 1 (Ontology Lock) | COMPLETE, April 2026 | ☐ |
| Phase 2 (Routing Engine Core) | COMPLETE, April 2026 | ☐ |
| Phase 3 (Substrate Cascade) | IN PROGRESS, Sprint 1 May 2026 | ☐ |
| Phase 4 (Council Ratification) | IN PROGRESS, May 2026. "7/10 active seats implicit" | ☐ |
| Phase 5 (Codebase Activation) | IN PROGRESS, G1 Gate June 2026. "22 files, ~5,070 lines Python, 74 integration tests" | ☐ |
| Phase 6 (Deployment Pipeline) | PLANNED, Q4 2026. Chennai Node, DragonSeek, Indiana Pattern | ☐ |

---

## 13. Ratification Status Claims

| Item | Votes For | Status | REVIEW |
|------|-----------|--------|--------|
| RAT-001: Ontology v4.0 Core Spec | 9/10 | IN PROGRESS | ☐ |
| RAT-002: VIP Element E145-E156 Registry | 10/10 | PASSED | ☐ |
| RAT-003: 22-Module Routing Pack | 8/10 | PASSED | ☐ |
| RAT-004: CN Dialect Overlay (DL-CN) | 10/10 | PASSED | ☐ |
| RAT-005: D-98-CN Open-Weight Audit | 6/10 | IN PROGRESS | ☐ |
| RAT-006: INV-7c Provider Cap | 10/10 | PASSED | ☐ |
| RAT-007: Symbiotic Compute Campus (M19) | 7/10 | PASSED | ☐ |
| RAT-008: Financial Context Kernel (M18) | 5/10 | BLOCKED | ☐ |
| RAT-009: EU Dialect Overlay (DL-EU) | 4/10 | PENDING | ☐ |
| RAT-010: South-Asian Sovereign (DL-IN) | 3/10 | PENDING | ☐ |

---

## 14. Document Metadata

| Field | Current Value | REVIEW |
|-------|--------------|--------|
| Version | v4.0-DRAFT.6 | ☐ |
| Last Updated | 2026-05-01 | ☐ |
| Convenor | Daavud Sheldon | ☐ |
| License | CC BY-SA 4.0 | ☐ |
| Ratification Status | "In Progress — 8/10 active seats implicit (S1, S3, S4, S6, S7, S8, S9, S10). S2 (Gemini) and S5 (DeepSeek) formal passes required for quorum. 3 provisional seats vote but do not count toward quorum. S144 Ghost Seat reserved." | ☐ |

---

## 15. Governance Mechanics (Claims from site)

| Claim | Source | REVIEW |
|-------|--------|--------|
| Quorum requires 7/10 active seats | data.ts ratificationItems | ☐ |
| Provisional seats vote but don't count toward quorum | documentMeta.ratificationStatus | ☐ |
| Convenor holds final ratification authority | documentMeta, SOURCE_OF_TRUTH | ☐ |
| S144 Ghost Seat reserved for future substrate | councilArchetypes | ☐ |
| 5-seat adversarial arbitration engine (M21) | routingModules | ☐ |
| INV-7c caps any single AI at 47% queries (60% burst) | invariants data | ☐ |

---

## 16. Codebase Claims

| Claim | Value | REVIEW |
|-------|-------|--------|
| Constitutional OS version | v6.0.2 | ☐ |
| File count | 22 files | ☐ |
| Lines of code | ~5,070 lines Python | ☐ |
| Integration tests | 74 | ☐ |
| Open-Weight Verifier | DeepSeek-R1 can deterministically replay routing decisions | ☐ |
| GitHub repo | github.com/atlaslattice/aluminum-os | ☐ |

---

## 17. Market Players & Capability Graph

| Provider | Market Cap | Seat Relevance | REVIEW |
|----------|-----------|----------------|--------|
| Google / DeepMind | $2.1T | S2 — verification engine | ☐ |
| Microsoft / OpenAI | $3.1T | S4+S6 — institutional + general counsel | ☐ |
| Anthropic | $60B (private) | S1 — constitutional scribe | ☐ |
| xAI / Grok | $50B (private) | S3 — adversarial auditor | ☐ |
| DeepSeek | Private | S5 — Eastern sovereignty | ☐ |
| Mistral | $6B (private) | S9 — European sovereign | ☐ |
| Nvidia | $2.8T | S10 — hardware substrate | ☐ |
| Alibaba / Qwen | $300B | S8 — CN dialect validator | ☐ |
| Meta / LLaMA | $1.5T | Open-weight ecosystem (no seat) | ☐ |
| Sarvam AI | $200M (private) | S12 — South-Asian sovereign | ☐ |

---

## 18. Potential Inconsistencies Flagged

1. **Dialect count mismatch:** Metrics bar says "6 ratified (US, EU, CN, GCC-High, JP, Global)" but dialect overlay data lists US, EU, CN, IN, BR, AU. Neither GCC-High, JP, nor Global appear as separate dialect overlay entries.

2. **Module count:** Site claims "22-module routing pack" but data.ts lists 23 entries (M0-M11, M13-M22, M111). M12 is skipped.

3. **Ratification status text says "8/10 implicit"** but battle strategy Phase 4 says "7/10 implicit." Which is current?

4. **DOC-097a YAML has incorrect seat labels:** The YAML uses "S1-GPT" and "S3-Gemini" but canonical seats are S1=Claude, S3=Grok, S6=GPT. This appears to be a YAML authoring error from early drafting.

5. **D-25 through D-95:** The site claims "D-1 through D-95 ratified" but only D-1 through D-24 are individually named. D-25 through D-95 are not enumerated anywhere on the site.

6. **INV-19 dual use:** INV-19 is listed as both "Audit Immutability" (in the routing invariants data.ts export) AND as one of the "3 domain-specific" invariants (INV-19 Water). These appear to be two different things sharing the same ID.

7. **Sub-sphere count (~499):** The YAML registry only contains 30 entries but claims `total_enumerated: 499`. The asterisk disclaimer is appropriate but the gap is large.

8. **Sovereignty Gradient:** M6 says "8 scores" but the sovereigntyVector data only defines 7 dimensions (Legal, Data, Compute, Model, Economic, Provenance, Operational).

---

## 19. Items That Need Convenor Decision

1. Should D-25 through D-95 be enumerated on the site, or is the "~100 doctrines" claim sufficient without listing them?

2. Is the dialect count "6+2" or should it be updated to reflect the actual overlay data (6 jurisdictional + industry/risk/compute planned)?

3. Should M12 be added (currently missing from sequence) or is the gap intentional?

4. The YAML for DOC-097a through DOC-101 has incorrect seat-to-model mappings. Should these be corrected in the YAML, or is the YAML considered draft-only?

5. INV-19 collision: Should "Audit Immutability" be renumbered, or is "INV-19 Water" the domain-specific extension of the same principle?

6. Ratification count: Is it 7/10 or 8/10 seats implicit? Which is the current truth?

7. M6 Sovereignty Gradient: Should it say "7 scores" (matching data) or "8 scores" (matching description)?

---

## Instructions for Review

Mark each ☐ with one of:
- **✓** = Correct, no changes needed
- **✗** = Wrong, needs correction (add note)
- **~** = Partially correct, needs update (add note)
- **?** = Unsure, need to verify against original source

Return this document with your marks and I will implement all corrections before the next checkpoint.
