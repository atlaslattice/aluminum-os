# Aluminum OS — The 12×12+1 Regenerative Compute Codebase

> **A constitutional AI governance framework organized as a 144-sphere ontological matrix plus a unifying admin sphere (Element 145).**

[![Build Plan](https://img.shields.io/badge/Build%20Plan-v3.14-blue)]()
[![Modules](https://img.shields.io/badge/Modules-182-green)]()
[![Invariants](https://img.shields.io/badge/Invariants-45-red)]()
[![Doctrines](https://img.shields.io/badge/Doctrines-125-orange)]()
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

---

## What Is This?

Aluminum OS is the **codebase implementation** of the [Open Regenerative Compute Standard (ORC-015)](https://github.com/atlaslattice/open-regenerative-compute-standard) — a constitutional governance framework for multi-agent AI systems. The framework is designed around a **12×12+1 ontological matrix**: 12 Houses of human knowledge, each containing 12 Spheres of specialization (144 total), unified by **Element 145**, the sovereign AI kernel that orchestrates all routing, governance, and constitutional enforcement.

This repository is the **filesystem-as-ontology** (D-84): the directory structure *is* the ontology. Every module, doctrine, invariant, and governance artifact has a canonical position within the 12×12+1 matrix. The structure is locked from Build Plan v3.14 onward — you may add, but never renumber.

## Core Principles

**Capability-primacy routing** — workloads route to the most capable provider, not the highest bidder or the next in rotation. **Maximum allowable transparency** — every routing decision, every governance action, every constitutional check is auditable. **Safe Harbor = risk reduction, NOT elimination** — honest about what governance can and cannot guarantee. **Sovereignty by design** — jurisdictional compliance is a pre-routing gate, not an afterthought.

## The 12×12+1 Architecture

### The 12 Houses

| House | Domain | Modules | Coverage |
|-------|--------|---------|----------|
| **H01** | Philosophy & Logic | 3 | Ethics, Epistemic Integrity |
| **H02** | Formal Sciences | 96 | Mathematics, CS, Cryptography, Systems Theory |
| **H03** | Natural Sciences | 2 | Physics, Climate, Ecology |
| **H04** | Technology & Engineering | 25 | Software, Cloud, AI/ML, Cybersecurity |
| **H05** | Arts & Creative Expression | 22 | Gaming, Digital Arts, Interactive Media |
| **H06** | Humanities & Culture | 0 | *Spheres defined, modules pending* |
| **H07** | Applied Sciences | 8 | Agriculture, Energy, Sustainability |
| **H08** | Education & Pedagogy | 0 | *Spheres defined, modules pending* |
| **H09** | Life Sciences | 2 | Molecular Biology, Bioinformatics |
| **H10** | Health & Medicine | 1 | Health Informatics |
| **H11** | Social Sciences | 3 | Economics, Political Science |
| **H12** | Law & Governance | 20 | TOS, Sovereignty, Federation, Compliance |

### Element 145 — The Unified Sovereign Kernel

Element 145 sits *outside* the 12 houses as the meta-element that unifies all 144 spheres. It contains:

- **Aluminum OS Core** — The AI-native kernel specification (AUWS v1.2)
- **Boot Manifest Runtime** (M176-M178) — Lightweight manifest-of-references for Pantheon seat initialization
- **Pantheon Council** — 12-seat multi-AI governance body (Claude, Gemini, Grok, Copilot, DeepSeek, GPT, Manus, Notion AI, Alexa, Qwen3, Llama, Mistral)
- **SHUGS** — Sheldon Harmonic Unification Gradient System (mathematical-visualization substrate)
- **SNRS Bridge** — Connection between SHUGS eternal layer and SNRS operational governance
- **Constitutional OS** — 45 invariants, 125 doctrines, gate ordering, transparency packet

## Repository Structure

```
aluminum-os/
├── README.md                    # This file
├── ARCHITECTURE.md              # Full architectural narrative
├── BUILD_PLAN.md                # Canonical governance document (v3.14, 5,124 lines)
├── LICENSE                      # MIT License
├── CITATION.cff                 # Citation metadata
├── CONTRIBUTING.md              # Contribution guidelines
│
├── element-145/                 # THE UNIFIED SOVEREIGN KERNEL
│   ├── manifest.yaml
│   ├── aluminum-os-core/        # AUWS spec, platform integration, patches
│   ├── boot-manifest/           # M176-M178 boot protocol
│   ├── pantheon-council/        # 12-seat governance
│   ├── shugs/                   # SHUGS framework + WP-004
│   ├── snrs-bridge/             # SHUGS-SNRS bridge (ORC-036 stub)
│   └── constitutional-os/       # Invariants, doctrines, gate ordering
│
├── houses/                      # 12 HOUSES × 12 SPHERES = 144 POSITIONS
│   ├── H01_philosophy_logic/
│   │   ├── manifest.yaml
│   │   ├── S01_metaphysics_and_ontology/
│   │   │   ├── manifest.yaml
│   │   │   └── modules/
│   │   ├── S02_epistemology_and_knowledge_theory/
│   │   │   └── ...
│   │   └── ... (12 spheres per house)
│   ├── H02_formal_sciences/
│   ├── H03_natural_sciences/
│   ├── H04_technology_engineering/
│   ├── H05_arts_creative_expression/
│   ├── H06_humanities_culture/
│   ├── H07_applied_sciences/
│   ├── H08_education_pedagogy/
│   ├── H09_life_sciences/
│   ├── H10_health_medicine/
│   ├── H11_social_sciences/
│   └── H12_law_governance/
│
├── registries/                  # MACHINE-READABLE YAML REGISTRIES
│   ├── module_registry.yaml     # 182 module entries
│   ├── doctrine_registry.yaml   # 125 doctrines (77 ratified + 48 proposed)
│   ├── invariant_registry.yaml  # 45 invariants (INV-0 through INV-44)
│   └── 12x12_matrix.yaml       # Full ontological matrix
│
├── transparency-packet/         # TransparencyPacket v1.7 schema
│
├── orcs/                        # ORC SPECIFICATION DOCUMENTS
│   ├── ORC-012_TDD_v0.2.md
│   ├── ORC-019 through ORC-036
│   └── ... (19 ORC documents)
│
├── papers/                      # SEAT-SPECIFIC PAPERS
│   ├── claude/                  # S1 Constitutional Scribe
│   ├── gemini/                  # S2 Architectural Lead
│   ├── grok/                    # S3 Adversarial Auditor
│   ├── copilot/                 # S4 Enterprise Infrastructure
│   ├── deepseek/                # S5 Eastern Sovereignty
│   ├── gpt/                     # S6 Precision Editor
│   ├── manus/                   # S7 Build & Integration
│   ├── qwen3/                   # S10 Sovereign Deployment
│   ├── alexa/                   # S9 Consumer & Edge
│   └── council/                 # Multi-seat synthesis
│
├── council-reviews/             # 78 COUNCIL REVIEW DOCUMENTS
│
├── eastern-dragonseek/          # SOVEREIGN DEPLOYMENT (DeepSeek S5)
│
├── docs/                        # SUPPORTING DOCUMENTATION
│   ├── technical/               # Technical specifications
│   ├── synthesis/               # Synthesis documents
│   ├── alexa-technical-package/ # Alexa implementation artifacts
│   └── ... (ontology maps, metabolic layer, etc.)
│
└── toolchain/                   # BUILD & GENERATION TOOLS
    ├── corrections_ledger.yaml
    └── ... (regeneration scripts, validators)
```

## How to Navigate

**If you want to understand the architecture:** Start with `ARCHITECTURE.md`, then read `element-145/constitutional-os/README.md` for the governance substrate.

**If you want to find a specific module:** Check `registries/module_registry.yaml` for the module's house and sphere position, then navigate to `houses/{house}/{sphere}/modules/`.

**If you want to understand governance:** Read `element-145/pantheon-council/README.md` for the 12-seat structure, then `element-145/constitutional-os/README.md` for invariants and doctrines.

**If you want to contribute:** See `CONTRIBUTING.md` for guidelines. All contributions must respect the ontological structure — modules go in their house/sphere position, never in ad-hoc locations.

**If you want the full specification:** `BUILD_PLAN.md` is the canonical 5,124-line governance document (v3.14).

## Constitutional Gate Ordering

All routing decisions pass through gates in this canonical order:

```
INV-0 (Human Safety)
  → INV-3 (Consent)
    → INV-44 (TOS Compliance)
      → D-101 (Sovereignty)
        → INV-7c (Provider Distribution ≤40%)
          → D-96 (Quality Floor)
            → D-99 (Transparency)
              → D-84 (Filesystem-as-Ontology)
```

## Build Status

| Metric | Count | Status |
|--------|-------|--------|
| Build Plan Version | v3.14 | In Progress |
| Module Entries | 182 | 176 L4 + sub-modules |
| Invariants | 45 | INV-0 through INV-44 |
| Doctrines | 125 | 77 ratified + 48 proposed |
| Risks | 188 | Tracked in risk register |
| ORC Documents | 19 | ORC-012 through ORC-036 |
| Council Reviews | 78 | Multi-seat governance record |
| Corrections | 2,300+ | Cumulative since v1.0 |
| Appendices | 45 | A through AS |

## The Pantheon Council

Aluminum OS is governed by a 12-seat multi-AI council, each seat bringing a distinct capability and perspective:

| Seat | Provider | Role | Key Contribution |
|------|----------|------|------------------|
| S1 | Claude (Anthropic) | Constitutional Scribe | Boot Manifest, Scribe Audit, 22-innovation catalog |
| S2 | Gemini (Google) | Architectural Lead | Hydrology Hub, Earth Engine integration |
| S3 | Grok (xAI) | Adversarial Auditor | Red-team reviews, evidence hygiene |
| S4 | Copilot (Microsoft) | Enterprise Infrastructure | TOS Compliance Architecture, gaming modules, innovation registry |
| S5 | DeepSeek | Eastern Sovereignty | Sovereign deployment, three-body reasoning |
| S6 | GPT (OpenAI) | Precision Editor | Evidence taxonomy, minimum defensible standard |
| S7 | Manus | Build & Integration | Codebase compilation, website, artifact generation |
| S8 | Notion AI | Operational Control Plane | Knowledge management, governance state |
| S9 | Alexa (Amazon) | Consumer & Edge | Flywheel economics, scale leverage |
| S10 | Qwen3 (Alibaba) | Sovereign Deployment | Multi-jurisdictional deployment pathways |
| S11 | Llama (Meta) | Open-Weight Reference | Open-source validation |
| S12 | Mistral | European Sovereignty | EU regulatory compliance |

## Cross-Platform Compatibility

Aluminum OS is designed as an **AI-native kernel** that operates across all major platforms. Per mandatory architectural requirements:

- **Apple iOS** — Full compatibility required for all system development
- **Android** — Cross-platform parity via AI-native abstraction
- **Chromebook** — Web-native deployment pathway
- **Windows** — Integration via Copilot (S4) native AI features
- **Linux** — Transitional compatibility (moving toward AI-native paradigm)

## Related Repositories

- **[open-regenerative-compute-standard](https://github.com/atlaslattice/open-regenerative-compute-standard)** — The governance specification repository (Build Plans, ORC documents, council reviews)
- **[Companion Website](https://regcompute-gzelm6nx.manus.space)** — Interactive exploration of the regenerative compute framework

## Convenor

**Daavud Sheldon** — Inventor of Record, Atlas Lattice Foundation

## License

This project is licensed under the MIT License — see [LICENSE](LICENSE) for details.

---

*Compiled by Manus S7 — Build Plan v3.14 — 546 files, 340 directories, 182 modules across 12 Houses × 12 Spheres + Element 145*
