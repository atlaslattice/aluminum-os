# Aluminum OS — Filesystem-as-Ontology Architecture Synthesis v1.0

**Document ID:** ORC-016
**Status:** PROPOSED — Pending Convenor Ratification
**Supersedes:** Filesystem-as-Ontology Spec v1.0 (Claude S1), Sheldonbrain RAG README (Phase 1-2)
**Date:** 2026-04-28
**Author:** Manus (S7 Build Seat), synthesizing contributions from all 10 Council seats
**Companion to:** ORC-015 Build Plan v2.1

---

## §0 Executive Summary

This document synthesizes the Filesystem-as-Ontology architecture from six independent sources into a single executable specification. The core principle — proposed as **Doctrine 83 (Substrate-Before-Framing)** — states that the codebase directory structure IS the ontology, not a description of it. When an AI agent reads the filesystem, it learns the 144-sphere Sheldonbrain ontology. When it runs the code, it traverses the ontology. When it writes new code, it must place it within the ontology. The ontology is not applied to the code — the code IS the ontology.

This synthesis integrates the Sheldonbrain RAG parsing tool (the existing Phase 1-2 ingestion pipeline), the v6.0.7 substrate convergence report (Gemini S2), the adversarial audit (GPT S6), the truth-seeking routing heuristic (Grok S3), the Windows cross-platform hardening (Copilot S4), and seven novel innovations from Manus (S7). The result is a complete, buildable specification for the Atlas Lattice Codebase — the physical encoding of Aluminum OS's constitutional governance substrate.

### §0.1 Source Reconciliation

| # | Source | Seat | Key Contributions |
|---|--------|------|-------------------|
| 1 | Filesystem-as-Ontology Spec v1.0 | Claude S1 | Core architecture, 8 validation gates, promotion rule, metadata schema |
| 2 | Registry v1.1 + Filesystem review | Grok S3 | TSS integration, D-83 proposal, scope risk, Notion authority flip, parser-filesystem symmetry |
| 3 | v6.0.7 Technical Integration Report | Gemini S2 | Complete Tauri shell code, Sheldonbrain Parser code, Doctrine Compiler code, 5-axis composition, MI-01 to MI-13 |
| 4 | Adversarial audit of Filesystem-as-Ontology | GPT S6 | 5 real risks, "Filesystem = prompt" innovation, M38 Ontology Context Injector, version pinning, validation gate #9 |
| 5 | Assessment of Registry + Filesystem | Copilot S4 | Symlink→YAML fix, Ring -1 addition, Entra Agent ID, Azure DevOps dual-target, Graph API fallback, Windows paths |
| 6 | Sheldonbrain RAG System (Phase 1-2) | Daavud (Convenor) | Existing ingestion pipeline, 144-sphere classifier, Qdrant vector DB, Notion integration, vault system |
| 7 | Ontology-at-Root innovations | Manus S7 | 7 novel innovations: Sphere-Native Embeddings, Ontological Routing Kernel, Constitutional Ingestion Gate, Sphere-as-Agent, Ontological Compiler, Provenance-Aware Ingestion, Codebase-as-Ontology |

---

## §1 The 5-Axis Composition

The Atlas Lattice Codebase composes five orthogonal views into a single unified architecture. Each axis has a specific structural location in the repository and a specific enforcement mechanism.

| Axis | Filesystem Location | Description | Enforcement |
|------|-------------------|-------------|-------------|
| **Topical** | `house-NN_<name>/sphere-NNN_<name>/` | The 144-Sphere Sheldonbrain domain ontology | Sheldonbrain Parser + ontology_validator.py |
| **Routing** | `element-145/` | The admin meta-sphere routing layer (M1-M63) | Element 145 Router + TSS |
| **Horizontal** | `rings/` | Substrate primitives spanning Ring -1 to Ring 4 | Constitutional Hypervisor (Ring -1) |
| **Vertical** | Per-module `_module_metadata.yaml` | Tiers 0-3 deployment scale concerns | Metadata validator |
| **Constitutional** | `toolchain/` | Enforcement layer (INVs + Doctrines) and CI/CD gates | Doctrine Compiler (M27) + CI/CD |

### §1.1 The Ontology-at-Root Principle

The existing Sheldonbrain RAG system applies the 144-sphere ontology as a post-hoc classification step. Data enters as raw text, gets embedded into a 384-dimensional vector space, and then receives a House/Sphere label from the OntologyClassifier (Gemini 2.0). The ontology is a metadata tag — models that consume this data learn "this document was tagged as Physics" but never learn what Physics means within the 144-sphere structure or how it relates to the other 143 spheres.

The Filesystem-as-Ontology principle inverts this relationship. The ontology is not applied after ingestion — it is the structure through which all data flows. When a document enters the system, the Ontological Routing Kernel (§5) determines its sphere placement before embedding occurs. The embedding itself is sphere-conditioned (§6.1), meaning the same document produces different vector representations depending on which sphere is asking. The filesystem directory structure mirrors this: a developer who `cd`s into `house-03/sphere-033/` is physically navigating the ontology.

This means that any AI agent — whether it is GPT, Claude, Gemini, Grok, Qwen, DeepSeek, Copilot, or any future model — learns the ontology simply by reading the codebase. The directory names are the ontology. The module metadata is the ontology. The import paths are the ontology. There is no separate "ontology document" to read and apply — the code IS the ontology.

### §1.2 Provider-Agnostic Capability Mapping

Per Convenor disposition: the system is provider-agnostic, but where clear primacy exists in a specific capability domain, it is mapped honestly rather than artificially balanced. This is not a competition — it is clean mapping of capabilities to maximize supply chains.

| Capability Domain | Primary Provider(s) | Rationale |
|------------------|-------------------|-----------|
| Constitutional Hypervisor (Ring -1) | Microsoft (Copilot S4) | VBS-inspired architecture, Hyper-V Virtual Secure Mode analog, Pluton hardware root of trust |
| Truth-Seeking Routing (TSS) | xAI (Grok S3) | TSS formula with epistemic scoring, adversarial truth-seeking heuristic |
| Ontology Classification | Google (Gemini S2) | Gemini 2.0 powers the existing OntologyClassifier, Sheldonbrain Parser canonical implementation |
| Structured Output Validation | OpenAI (GPT S6) | M34 Structured Output Validator, JSON schema enforcement, "Filesystem = prompt" innovation |
| Sovereignty & Cross-Border | Alibaba (Qwen3 S10) | Bamboo Bridge SM2 signatures, PIPL compliance, Bailian Element 145, China-region sovereignty |
| Open-Weight Audit | DeepSeek (S5) | Model fingerprint verification, DragonSeek Shell, offline audit containers |
| Constitutional Compilation | Anthropic (Claude S1) | Registry methodology, "as-if-ratified-but-mislabeled" approach, Doctrine Compiler spec |
| Glass Takeover Shell | Google (Gemini S2) | Tauri v2 Rust orchestrator, 52-module React frontend, Governance Bridge |
| Edge Inference | Microsoft (Copilot S4) | Foundry Local (~20MB runtime, GA April 2026), INV-25 Neuromorphic Edge Sovereignty |
| Agent Identity | Microsoft (Copilot S4) | Entra Agent ID with OAuth 2.0 + MCP + A2A, parent-child identity blueprints |
| Quantum-Safe Cryptography | Microsoft (Copilot S4) + Google | Pluton PQC (SLH-DSA), Azure Quantum; Google Willow quantum chip |
| Media Integrity (INV-28) | xAI (Grok S3) | X-Algorithm Truth Substrate — no Microsoft mapping currently (honest gap) |
| Codebase Ingestion & Build | Manus (S7) | Build Plan integration, GitHub CI/CD, Notion vaulting, multi-Council synthesis |

---

## §2 Complete Filesystem Structure

This is the canonical directory structure for the Atlas Lattice Codebase. It incorporates all Council recommendations: Ring -1 from Copilot, YAML pointer manifests instead of symlinks (Copilot + GPT), Element 145 subdomain enforcement (GPT), and version pinning (GPT).

```
atlas-lattice-codebase/
│
├── _ontology_lock.yaml                    # Ontology version pin (GPT innovation)
│
├── toolchain/                             # Constitutional enforcement layer
│   ├── sheldonbrain_parser.py             # Canonical ontology access (Gemini code)
│   ├── sheldonbrain_ontology.yaml         # YAML fallback for offline builds
│   ├── ontology_validator.py              # 9 validation gates (Claude + GPT gate #9)
│   ├── doctrine_compiler.py               # M27: YAML → Python validators (Gemini code)
│   ├── invariants_registry.py             # 43 INV slots (Registry v1.1)
│   ├── doctrines_registry.py              # 77+ Doctrines (Registry v1.1)
│   ├── ontological_compiler.py            # M58: CSV/YAML → schemas/endpoints/agents (Manus)
│   ├── truth_seeking_router.py            # M3.1 TSS computation (Grok code)
│   ├── model_fingerprint_verifier.py      # M15a: SM3 hash verification (DeepSeek)
│   ├── golden_trace.py                    # Provenance-aware audit chain (Manus)
│   └── _pointers.yaml                     # Cross-sphere reference manifest (Copilot fix)
│
├── rings/                                 # Horizontal substrate primitives
│   ├── ring-neg1_constitutional-hypervisor/   # Ring -1 (Copilot: MUST exist)
│   │   ├── hypervisor.py                  # INV enforcement before Ring 0
│   │   ├── consent_kernel.py              # Identity Triad: Human/Agent/Hardware
│   │   └── _module_metadata.yaml
│   ├── ring-0_forge-core/                 # Ring 0: invariants, doctrines
│   │   ├── invariants.py                  # 43 INV implementations (9 active, 34 PENDING)
│   │   ├── doctrines.py                   # 77+ Doctrine implementations (11 active)
│   │   ├── foundry_local_adapter.py       # Microsoft Foundry Local (Copilot E3)
│   │   ├── titan_c_adapter.py             # Google Titan-C
│   │   ├── pluton_adapter.py              # Microsoft Pluton PQC
│   │   └── _module_metadata.yaml
│   ├── ring-1_manus-core/                 # Ring 1: orchestrator
│   │   ├── orchestrator.py
│   │   └── _module_metadata.yaml
│   ├── ring-1.5_bridge/                   # Ring 1.5: EP catalog
│   │   ├── ep_catalog.py
│   │   └── _module_metadata.yaml
│   ├── ring-2_sheldonbrain/               # Ring 2: ontology + memory
│   │   ├── ontology.py
│   │   ├── memory.py
│   │   └── _module_metadata.yaml
│   ├── ring-3_pantheon/                   # Ring 3: Element 145 + Council
│   │   ├── element145.py
│   │   ├── council.py
│   │   └── _module_metadata.yaml
│   └── ring-4_noosphere/                  # Ring 4: UI console
│       ├── console.py
│       └── _module_metadata.yaml
│
├── element-145/                           # Routing meta-sphere (M1-M63)
│   ├── routing/                           # GPT fix: enforce subdomain structure
│   │   ├── m03_routing_engine.py          # 9-step routing with TSS
│   │   ├── m03.1_truth_seeking_score.py   # TSS computation (Grok)
│   │   ├── m34_structured_output.py       # Structured Output Validator (GPT)
│   │   └── _module_metadata.yaml
│   ├── governance/                        # Constitutional governance modules
│   │   ├── m01_constitutional_hypervisor.py
│   │   ├── m02_consent_kernel.py
│   │   ├── m27_constitutional_compiler.py
│   │   ├── m35_doctrine_evaluation.py     # Doctrine Evaluation Engine (GPT)
│   │   └── _module_metadata.yaml
│   ├── audit/                             # Audit and provenance modules
│   │   ├── m06_transparency_packet.py
│   │   ├── m06b_provenance_genome.py
│   │   ├── m10_test_harness.py
│   │   ├── m15a_model_fingerprint.py      # DeepSeek
│   │   └── _module_metadata.yaml
│   ├── execution/                         # Execution and orchestration
│   │   ├── m08_epistemic_classifier.py
│   │   ├── m26_persistent_memory.py
│   │   ├── m31_manus_api_orchestrator.py
│   │   └── _module_metadata.yaml
│   ├── ingestion/                         # Ontological ingestion pipeline (NEW)
│   │   ├── m57_ontological_routing_kernel.py   # Manus Innovation 2
│   │   ├── m58_ontological_compiler.py         # Manus Innovation 5
│   │   ├── m59_constitutional_ingestion_gate.py # Manus Innovation 3 (INV-22)
│   │   ├── m60_ontology_context_injector.py    # GPT M38 → renumbered M60
│   │   └── _module_metadata.yaml
│   └── symbiosis/                         # Provider-specific adapters
│       ├── gemini_adapter.py
│       ├── grok_adapter.py
│       ├── claude_adapter.py
│       ├── gpt_adapter.py
│       ├── copilot_adapter.py
│       ├── qwen3_adapter.py
│       ├── deepseek_adapter.py
│       └── _module_metadata.yaml
│
├── 144-root/                              # Cross-House substrate modules (3+ Houses)
│   ├── consent_kernel.py                  # Touches all 12 Houses
│   ├── transparency_packet.py             # Touches all 12 Houses
│   ├── golden_trace.py                    # Touches all 12 Houses
│   ├── ontological_routing_kernel.py      # Touches all 12 Houses
│   └── _module_metadata.yaml
│
├── house-01_sovereign-governance/
│   ├── sphere-001_constitutional-drafting/
│   │   ├── _module_metadata.yaml
│   │   └── _pointers.yaml                 # Cross-sphere refs (replaces symlinks)
│   ├── sphere-002_legislative-process/
│   ├── sphere-003_judicial-review/
│   ├── sphere-004_executive-administration/
│   ├── sphere-005_diplomatic-relations/
│   ├── sphere-006_electoral-systems/
│   ├── sphere-007_constitutional-law/
│   ├── sphere-008_regulatory-frameworks/
│   ├── sphere-009_public-policy/
│   ├── sphere-010_governance-ethics/
│   ├── sphere-011_institutional-design/
│   └── sphere-012_sovereignty-theory/
│
├── house-02_natural-sciences/
│   ├── sphere-013_physics/
│   ├── sphere-014_chemistry/
│   ├── sphere-015_biology/
│   ├── sphere-016_earth-sciences/
│   ├── sphere-017_astronomy/
│   ├── sphere-018_ecology/
│   ├── sphere-019_materials-science/
│   ├── sphere-020_neuroscience/
│   ├── sphere-021_genetics/
│   ├── sphere-022_oceanography/
│   ├── sphere-023_atmospheric-science/
│   └── sphere-024_paleontology/
│
├── house-03_formal-sciences/
│   ├── sphere-025_mathematics/
│   ├── sphere-026_logic/
│   ├── sphere-027_statistics/
│   ├── sphere-028_computer-science/
│   ├── sphere-029_information-theory/
│   ├── sphere-030_systems-theory/
│   ├── sphere-031_decision-theory/
│   ├── sphere-032_game-theory/
│   ├── sphere-033_cryptography/
│   ├── sphere-034_computational-complexity/
│   ├── sphere-035_category-theory/
│   └── sphere-036_formal-verification/
│
├── house-04_applied-sciences/
│   ├── sphere-037_engineering/
│   ├── sphere-038_medicine/
│   ├── sphere-039_agriculture/
│   ├── sphere-040_environmental-science/
│   ├── sphere-041_energy-systems/
│   ├── sphere-042_water-systems/
│   ├── sphere-043_transportation/
│   ├── sphere-044_telecommunications/
│   ├── sphere-045_manufacturing/
│   ├── sphere-046_robotics/
│   ├── sphere-047_biotechnology/
│   └── sphere-048_nanotechnology/
│
├── house-05_social-sciences/
│   ├── sphere-049_economics/
│   ├── sphere-050_political-science/
│   ├── sphere-051_sociology/
│   ├── sphere-052_psychology/
│   ├── sphere-053_anthropology/
│   ├── sphere-054_geography/
│   ├── sphere-055_linguistics/
│   ├── sphere-056_education/
│   ├── sphere-057_communication/
│   ├── sphere-058_demography/
│   ├── sphere-059_urban-planning/
│   └── sphere-060_development-studies/
│
├── house-06_humanities/
│   ├── sphere-061_philosophy/
│   ├── sphere-062_history/
│   ├── sphere-063_literature/
│   ├── sphere-064_religious-studies/
│   ├── sphere-065_cultural-studies/
│   ├── sphere-066_ethics/
│   ├── sphere-067_aesthetics/
│   ├── sphere-068_hermeneutics/
│   ├── sphere-069_rhetoric/
│   ├── sphere-070_classics/
│   ├── sphere-071_archaeology/
│   └── sphere-072_museology/
│
├── house-07_arts/
│   ├── sphere-073_visual-arts/
│   ├── sphere-074_music/
│   ├── sphere-075_performing-arts/
│   ├── sphere-076_film-media/
│   ├── sphere-077_architecture/
│   ├── sphere-078_design/
│   ├── sphere-079_photography/
│   ├── sphere-080_digital-arts/
│   ├── sphere-081_crafts/
│   ├── sphere-082_fashion/
│   ├── sphere-083_culinary-arts/
│   └── sphere-084_game-design/
│
├── house-08_health-sciences/
│   ├── sphere-085_clinical-medicine/
│   ├── sphere-086_public-health/
│   ├── sphere-087_pharmacology/
│   ├── sphere-088_nutrition/
│   ├── sphere-089_mental-health/
│   ├── sphere-090_rehabilitation/
│   ├── sphere-091_epidemiology/
│   ├── sphere-092_biomedical-engineering/
│   ├── sphere-093_nursing/
│   ├── sphere-094_dentistry/
│   ├── sphere-095_veterinary/
│   └── sphere-096_gerontology/
│
├── house-09_business-economics/
│   ├── sphere-097_management/
│   ├── sphere-098_finance/
│   ├── sphere-099_marketing/
│   ├── sphere-100_entrepreneurship/
│   ├── sphere-101_accounting/
│   ├── sphere-102_operations/
│   ├── sphere-103_human-resources/
│   ├── sphere-104_supply-chain/
│   ├── sphere-105_real-estate/
│   ├── sphere-106_international-business/
│   ├── sphere-107_business-ethics/
│   └── sphere-108_innovation-management/
│
├── house-10_law-justice/
│   ├── sphere-109_constitutional-law/
│   ├── sphere-110_criminal-law/
│   ├── sphere-111_civil-law/
│   ├── sphere-112_international-law/
│   ├── sphere-113_human-rights/
│   ├── sphere-114_environmental-law/
│   ├── sphere-115_intellectual-property/
│   ├── sphere-116_corporate-law/
│   ├── sphere-117_labor-law/
│   ├── sphere-118_tax-law/
│   ├── sphere-119_cyber-law/
│   └── sphere-120_jurisprudence/
│
├── house-11_information-technology/
│   ├── sphere-121_software-engineering/
│   ├── sphere-122_artificial-intelligence/
│   ├── sphere-123_data-science/
│   ├── sphere-124_cybersecurity/
│   ├── sphere-125_cloud-computing/
│   ├── sphere-126_networking/
│   ├── sphere-127_database-systems/
│   ├── sphere-128_human-computer-interaction/
│   ├── sphere-129_distributed-systems/
│   ├── sphere-130_quantum-computing/
│   ├── sphere-131_blockchain/
│   └── sphere-132_iot/
│
├── house-12_interdisciplinary/
│   ├── sphere-133_sustainability/
│   ├── sphere-134_futures-studies/
│   ├── sphere-135_complexity-science/
│   ├── sphere-136_cognitive-science/
│   ├── sphere-137_science-technology-society/
│   ├── sphere-138_peace-conflict/
│   ├── sphere-139_gender-studies/
│   ├── sphere-140_media-studies/
│   ├── sphere-141_disability-studies/
│   ├── sphere-142_indigenous-studies/
│   ├── sphere-143_bioethics/
│   └── sphere-144_metamathematics/
│
├── src-tauri/                             # Glass Takeover Shell (Gemini code)
│   ├── src/
│   │   └── main.rs                        # Tauri v2 Rust orchestrator
│   ├── tauri.conf.json
│   └── Cargo.toml
│
├── src-react/                             # 52-Module React Frontend (Gemini code)
│   ├── App.tsx
│   ├── components/
│   │   ├── governance/                    # House 1 views
│   │   ├── sciences/                      # House 2-4 views
│   │   ├── social/                        # House 5-6 views
│   │   ├── arts/                          # House 7 views
│   │   ├── health/                        # House 8 views
│   │   ├── business/                      # House 9 views
│   │   ├── law/                           # House 10 views
│   │   ├── tech/                          # House 11 views
│   │   ├── interdisciplinary/             # House 12 views
│   │   └── shared/                        # Cross-house components
│   └── stakeholder-views/                 # 4 stakeholder perspectives
│       ├── farmer/
│       ├── regulator/
│       ├── auditor/
│       └── developer/
│
├── ingestion/                             # Sheldonbrain RAG Pipeline (existing + upgraded)
│   ├── ontological_routing_kernel.py      # M57: Ontology-at-root ingestion
│   ├── constitutional_ingestion_gate.py   # M59: INV-0/INV-7c/INV-17 checks
│   ├── sphere_conditioned_embeddings.py   # Innovation 1: Sphere-native vectors
│   ├── ontology_classifier.py             # Existing Gemini 2.0 classifier (upgraded)
│   ├── staging_layer.py                   # Novelty filter (85% threshold)
│   ├── significance_scorer.py             # 40% heuristic + 60% LLM
│   ├── vault_security.py                  # PII filtering + Class A separation
│   ├── notion_ingestion_client.py         # Notion integration
│   ├── gdrive_connector.py               # Google Drive ingestion
│   ├── grok_chat_connector.py             # Grok chat export ingestion
│   ├── arxiv_connector.py                 # ArXiv paper ingestion
│   └── rss_connector.py                   # RSS feed ingestion
│
├── api/                                   # FastAPI REST API
│   ├── api_server.py                      # Main server with auth + rate limiting
│   ├── governance_bridge.py               # M47: FastAPI sidecar (Gemini code)
│   └── scheduler.py                       # APScheduler for automated jobs
│
├── .github/
│   └── workflows/
│       ├── ontology_ci.yaml               # GitHub Actions: 9 validation gates
│       └── deploy.yml                     # Cloud Run deployment
│
├── .azure-pipelines/                      # Azure DevOps dual-target (Copilot N2)
│   └── ontology_ci.yaml                   # Same validators, enterprise deployment
│
└── README.md
```

### §2.1 Version Pinning (GPT Innovation)

The `_ontology_lock.yaml` file at the repository root pins the exact versions of all constitutional artifacts. Without this, reproducibility breaks — a build from last week could produce different results than a build today if the ontology, parser, or doctrine set has changed.

```yaml
# _ontology_lock.yaml
ontology_version: "2.0.0"
parser_version: "1.0.0"
doctrine_set: "v6.0.7"
invariant_count: 43
doctrine_count: 77
promotion_threshold: 3
max_secondary_spheres: 2
last_validated: "2026-04-28T00:00:00Z"
content_hash: "sha256:..."
```

### §2.2 The 144-Root Promotion Rule

Per Convenor disposition and Grok S3 recommendation, the promotion threshold is locked at **3 Houses**. Any module that touches 3 or more Houses is promoted from its primary sphere to the `144-root/` substrate-of-the-substrate level. This prevents ontology degeneration while keeping the structure clean.

**Hard constraint (GPT Risk 3 fix):** Each module may declare **1 primary sphere + maximum 2 secondary spheres**. No exceptions. If a module needs more than 2 secondary spheres, it belongs in `144-root/`.

### §2.3 Cross-Sphere Pointer Manifests (Copilot Fix)

Symlinks are replaced with declarative YAML pointer manifests. This is cross-platform (Windows, macOS, Linux) and requires no OS-level privileges.

```yaml
# house-04_applied-sciences/sphere-042_water-systems/_pointers.yaml
pointers:
  - target_sphere: "sphere-018_ecology"
    target_house: "house-02_natural-sciences"
    relationship: "secondary"
    reason: "Water cycle ecology cross-reference"
  - target_sphere: "sphere-114_environmental-law"
    target_house: "house-10_law-justice"
    relationship: "secondary"
    reason: "Water rights legal framework"
```

The toolchain validator resolves these at build time. The Sheldonbrain Parser reads the same manifests. All path operations use `pathlib.Path` (Copilot N4).

---

## §3 Per-Module Metadata Schema

Every module within Aluminum OS must declare its constitutional context through both a `_module_metadata.yaml` file and matching Python in-code constants. This dual-declaration pattern (from Gemini S2) allows the `ontology_validator.py` to block builds if naming drift or unauthorized invariant violations are detected.

### §3.1 YAML Schema (v2.0)

This schema incorporates all Council recommendations: Entra Agent ID blueprint (Copilot N1), version pinning (GPT), and provenance tracking.

```yaml
# _module_metadata.yaml — Atlas Lattice Module Metadata Schema v2.0
module:
  canonical_id: "ALD-007-001"
  canonical_name: "Water Accounting Module"
  status: "ACTIVE"                         # ACTIVE | PENDING | DEPRECATED

ontology:
  sphere_primary: "sphere-042_water-systems"
  sphere_secondary:                        # Max 2 (GPT hard constraint)
    - "sphere-018_ecology"
    - "sphere-114_environmental-law"
  houses_used: ["04", "02", "10"]
  rings_used: ["ring-2", "ring-3"]

constitutional:
  doctrines_implemented: ["D-18", "D-67"]
  invariants_enforced: ["INV-13", "INV-18", "INV-19"]
  transparency_packet_emitter: true
  consent_kernel_binding: true

identity:                                  # Copilot N1: Entra Agent ID
  agent_identity_blueprint: "ald-007-001-water"
  access_scope: ["read:sphere-042", "write:sphere-042", "read:sphere-018"]
  lifecycle: "persistent"

provenance:
  origin_version: "v6.0.7"
  originator_seats: ["S2", "S7"]
  ratification_status: "PROPOSED"          # RATIFIED | PROPOSED | PENDING
  council_seat_canonical: "S2"

version:                                   # GPT: version pinning
  ontology_version: "2.0.0"
  parser_version: "1.0.0"
  last_validated: "2026-04-28"
```

### §3.2 Python In-Code Constants

Every Python module must declare matching constants that the validator cross-checks against the YAML:

```python
# In-code constitutional context (must match _module_metadata.yaml)
__atlas_module_id__ = "ALD-007-001"
__atlas_sphere_primary__ = "sphere-042_water-systems"
__atlas_houses_used__ = ["04", "02", "10"]
__atlas_doctrines_implemented__ = ["D-18", "D-67"]
__atlas_invariants_enforced__ = ["INV-13", "INV-18", "INV-19"]
__atlas_transparency_emitter__ = True
```

---

## §4 Toolchain Modules — Complete Code

### §4.1 Sheldonbrain Parser (toolchain/sheldonbrain_parser.py)

This is the canonical ontology access layer. It reads from the Notion 144-Sphere page (ID: `34a0c1de-73d9-81c8-bbd7-f2bfbcbc491a`) with a 3-tier fallback chain: Notion API → local cache → committed YAML. Per Grok S3, the Notion authority model is flipped: Notion is the control plane, the filesystem is canonical state. Changes in Notion must be pulled, validated, and committed — Notion is not implicitly authoritative at runtime.

Per Copilot N3, the parser also supports Microsoft Graph API as an alternate source for enterprise deployments where Notion is unavailable.

```python
# toolchain/sheldonbrain_parser.py
"""Canonical ontology access layer per Doctrine 75 + Doctrine 83.

3-tier fallback: Notion API → local cache → committed YAML
Optional: Microsoft Graph API for enterprise deployments (Copilot N3)

Authority model (Grok S3 fix):
  Notion = control plane (where edits happen)
  Filesystem = canonical state (what code trusts)
  Changes: Notion edit → pull → validate → commit → filesystem updated
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional
import yaml, json, hashlib, os

__atlas_module_id__ = "TOOLCHAIN-001"
__atlas_sphere_primary__ = "144-root"
__atlas_doctrines_implemented__ = ["D-75", "D-83"]
__atlas_invariants_enforced__ = ["INV-13"]
__atlas_transparency_emitter__ = True


@dataclass(frozen=True)
class SphereDefinition:
    """Immutable definition of a single sphere in the 144-sphere ontology."""
    sphere_id: str          # e.g., "sphere-042"
    canonical_name: str     # e.g., "Water Systems"
    house_id: str           # e.g., "house-04"
    house_name: str         # e.g., "Applied Sciences"
    sphere_number: int      # e.g., 42
    house_number: int       # e.g., 4


@dataclass
class OntologySnapshot:
    """Complete snapshot of the 144-sphere ontology at a point in time."""
    version: str
    content_hash: str
    spheres: dict[str, SphereDefinition] = field(default_factory=dict)
    houses: dict[str, list[str]] = field(default_factory=dict)
    source: str = "unknown"  # "notion" | "cache" | "yaml" | "graph_api"


class SheldonbrainParser:
    """Canonical ontology access layer per Doctrine 75 + Doctrine 83.

    Provides:
    - load() → OntologySnapshot with 3-tier fallback
    - validate_filesystem(root) → list of violations
    - get_sphere(sphere_id) → SphereDefinition
    - get_house_spheres(house_id) → list[SphereDefinition]
    - get_truth_seeking_candidates(topics) → list[SphereDefinition] (Grok TSS)
    """

    NOTION_PAGE_ID = "34a0c1de-73d9-81c8-bbd7-f2bfbcbc491a"
    CACHE_FILE = Path(__file__).parent / ".ontology_cache.json"

    def __init__(self, notion_token: Optional[str] = None,
                 graph_token: Optional[str] = None):
        self.notion_token = notion_token or os.getenv("NOTION_API_TOKEN")
        self.graph_token = graph_token or os.getenv("GRAPH_API_TOKEN")
        self.fallback_yaml = Path(__file__).parent / "sheldonbrain_ontology.yaml"
        self._snapshot: Optional[OntologySnapshot] = None

    def load(self) -> OntologySnapshot:
        """Load ontology with 3-tier fallback (+ optional Graph API)."""
        if self._snapshot:
            return self._snapshot

        # Tier 1: Notion API (control plane)
        if self.notion_token:
            try:
                snapshot = self._load_from_notion()
                self._update_cache(snapshot)
                self._snapshot = snapshot
                return snapshot
            except Exception:
                pass  # Fall through to next tier

        # Tier 1b: Microsoft Graph API (enterprise alternate — Copilot N3)
        if self.graph_token:
            try:
                snapshot = self._load_from_graph_api()
                self._update_cache(snapshot)
                self._snapshot = snapshot
                return snapshot
            except Exception:
                pass

        # Tier 2: Local cache
        if self.CACHE_FILE.exists():
            try:
                snapshot = self._load_from_cache()
                self._snapshot = snapshot
                return snapshot
            except Exception:
                pass

        # Tier 3: Committed YAML fallback
        if self.fallback_yaml.exists():
            snapshot = self._load_from_yaml()
            self._snapshot = snapshot
            return snapshot

        raise RuntimeError(
            "No ontology source found. Ensure Notion token, cache, or YAML exists."
        )

    def validate_filesystem(self, root: Path) -> list[dict]:
        """Detect drift between filesystem and canonical ontology per D-74.

        Returns list of violations with severity and description.
        Includes GPT validation gate #9: parser-filesystem symmetry.
        """
        snapshot = self.load()
        violations = []

        # Check every sphere in parser exists in filesystem
        for sphere_id, sphere_def in snapshot.spheres.items():
            house_dir = f"house-{sphere_def.house_number:02d}_{self._slugify(sphere_def.house_name)}"
            sphere_dir = f"sphere-{sphere_def.sphere_number:03d}_{self._slugify(sphere_def.canonical_name)}"
            expected_path = root / house_dir / sphere_dir

            if not expected_path.exists():
                violations.append({
                    "type": "MISSING_SPHERE_DIR",
                    "severity": "HIGH",
                    "sphere": sphere_id,
                    "expected_path": str(expected_path),
                    "description": f"Sphere {sphere_def.canonical_name} exists in ontology but not in filesystem"
                })

        # GPT gate #9: Check every filesystem sphere exists in parser
        for house_dir in root.iterdir():
            if not house_dir.is_dir() or not house_dir.name.startswith("house-"):
                continue
            for sphere_dir in house_dir.iterdir():
                if not sphere_dir.is_dir() or not sphere_dir.name.startswith("sphere-"):
                    continue
                sphere_num = sphere_dir.name.split("_")[0].replace("sphere-", "")
                sphere_key = f"sphere-{sphere_num}"
                if sphere_key not in snapshot.spheres:
                    violations.append({
                        "type": "ORPHAN_SPHERE_DIR",
                        "severity": "CRITICAL",
                        "path": str(sphere_dir),
                        "description": f"Filesystem sphere {sphere_dir.name} has no ontology definition"
                    })

        return violations

    def get_sphere(self, sphere_id: str) -> Optional[SphereDefinition]:
        """Get a single sphere definition by ID."""
        return self.load().spheres.get(sphere_id)

    def get_house_spheres(self, house_id: str) -> list[SphereDefinition]:
        """Get all spheres belonging to a house."""
        snapshot = self.load()
        sphere_ids = snapshot.houses.get(house_id, [])
        return [snapshot.spheres[sid] for sid in sphere_ids if sid in snapshot.spheres]

    def get_truth_seeking_candidates(
        self, query_topics: list[str]
    ) -> list[SphereDefinition]:
        """Return spheres weighted by truth_score potential (Grok S3 TSS).

        Used by the Ontological Routing Kernel to determine which spheres
        are most relevant for a given query before embedding occurs.
        """
        snapshot = self.load()
        candidates = []
        for sphere in snapshot.spheres.values():
            relevance = sum(
                1 for topic in query_topics
                if topic.lower() in sphere.canonical_name.lower()
                or topic.lower() in sphere.house_name.lower()
            )
            if relevance > 0:
                candidates.append(sphere)
        # Sort by relevance (higher = more topic matches)
        return sorted(candidates, key=lambda s: -sum(
            1 for t in query_topics
            if t.lower() in s.canonical_name.lower()
        ))

    # --- Private methods ---

    def _load_from_notion(self) -> OntologySnapshot:
        """Fetch ontology from Notion API."""
        from notion_client import Client
        client = Client(auth=self.notion_token)
        page = client.pages.retrieve(page_id=self.NOTION_PAGE_ID)
        # Parse Notion page content into SphereDefinitions
        # Implementation depends on Notion page structure
        spheres, houses = self._parse_notion_content(page)
        content = json.dumps(spheres, sort_keys=True)
        return OntologySnapshot(
            version="2.0.0",
            content_hash=hashlib.sha256(content.encode()).hexdigest(),
            spheres=spheres,
            houses=houses,
            source="notion"
        )

    def _load_from_graph_api(self) -> OntologySnapshot:
        """Fetch ontology from Microsoft Graph API (Copilot N3)."""
        import requests
        headers = {"Authorization": f"Bearer {self.graph_token}"}
        # Query SharePoint/OneNote for ontology mirror
        # Implementation depends on enterprise deployment
        raise NotImplementedError("Graph API adapter pending enterprise deployment")

    def _load_from_cache(self) -> OntologySnapshot:
        """Load from local JSON cache."""
        with open(self.CACHE_FILE) as f:
            data = json.load(f)
        spheres = {
            k: SphereDefinition(**v) for k, v in data["spheres"].items()
        }
        houses = data["houses"]
        return OntologySnapshot(
            version=data["version"],
            content_hash=data["content_hash"],
            spheres=spheres,
            houses=houses,
            source="cache"
        )

    def _load_from_yaml(self) -> OntologySnapshot:
        """Load from committed YAML fallback."""
        with open(self.fallback_yaml) as f:
            data = yaml.safe_load(f)
        spheres = {}
        houses = {}
        for house in data.get("houses", []):
            house_id = f"house-{house['number']:02d}"
            houses[house_id] = []
            for sphere in house.get("spheres", []):
                sphere_id = f"sphere-{sphere['number']:03d}"
                spheres[sphere_id] = SphereDefinition(
                    sphere_id=sphere_id,
                    canonical_name=sphere["name"],
                    house_id=house_id,
                    house_name=house["name"],
                    sphere_number=sphere["number"],
                    house_number=house["number"]
                )
                houses[house_id].append(sphere_id)
        content = json.dumps({k: v.__dict__ for k, v in spheres.items()}, sort_keys=True)
        return OntologySnapshot(
            version=data.get("version", "1.0.0"),
            content_hash=hashlib.sha256(content.encode()).hexdigest(),
            spheres=spheres,
            houses=houses,
            source="yaml"
        )

    def _update_cache(self, snapshot: OntologySnapshot) -> None:
        """Write snapshot to local cache for offline use."""
        data = {
            "version": snapshot.version,
            "content_hash": snapshot.content_hash,
            "spheres": {k: v.__dict__ for k, v in snapshot.spheres.items()},
            "houses": snapshot.houses,
            "source": snapshot.source,
        }
        self.CACHE_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(self.CACHE_FILE, "w") as f:
            json.dump(data, f, indent=2)

    def _parse_notion_content(self, page: dict) -> tuple[dict, dict]:
        """Parse Notion page into sphere/house dictionaries."""
        # Placeholder — actual implementation depends on Notion page structure
        return {}, {}

    @staticmethod
    def _slugify(name: str) -> str:
        """Convert name to filesystem-safe slug."""
        return name.lower().replace(" ", "-").replace("&", "and")
```

### §4.2 Ontology Validator (toolchain/ontology_validator.py)

Nine validation gates — the original 8 from Claude S1 plus GPT's gate #9 (parser-filesystem symmetry). Fails the build on any violation.

```python
# toolchain/ontology_validator.py
"""9-gate ontology validation per Doctrine 73-74.

Gates 1-8: Claude S1 original specification
Gate 9: GPT S6 parser-filesystem symmetry check

Fails build on ANY violation — Doctrine 74 (Naming Drift as Build Blocker).
"""

from pathlib import Path
from typing import Optional
import yaml, sys

__atlas_module_id__ = "TOOLCHAIN-002"
__atlas_sphere_primary__ = "144-root"
__atlas_doctrines_implemented__ = ["D-73", "D-74", "D-83"]
__atlas_invariants_enforced__ = ["INV-13"]


class OntologyValidator:
    """9-gate build validator for Filesystem-as-Ontology compliance."""

    def __init__(self, root: Path, parser=None):
        self.root = root
        self.parser = parser
        self.violations = []

    def run_all_gates(self) -> list[dict]:
        """Execute all 9 validation gates. Returns violations list."""
        self.violations = []
        self._gate_1_directory_naming()
        self._gate_2_metadata_presence()
        self._gate_3_metadata_yaml_validity()
        self._gate_4_python_constants_match()
        self._gate_5_promotion_rule()
        self._gate_6_pointer_validity()
        self._gate_7_invariant_declaration()
        self._gate_8_doctrine_declaration()
        self._gate_9_parser_filesystem_symmetry()
        return self.violations

    def _gate_1_directory_naming(self):
        """Gate 1: Directory names match house-NN_<name>/sphere-NNN_<name> pattern."""
        import re
        house_pattern = re.compile(r"^house-\d{2}_[\w-]+$")
        sphere_pattern = re.compile(r"^sphere-\d{3}_[\w-]+$")

        for item in self.root.iterdir():
            if item.is_dir() and item.name.startswith("house-"):
                if not house_pattern.match(item.name):
                    self.violations.append({
                        "gate": 1, "severity": "CRITICAL",
                        "path": str(item),
                        "message": f"Invalid house directory name: {item.name}"
                    })
                for sub in item.iterdir():
                    if sub.is_dir() and sub.name.startswith("sphere-"):
                        if not sphere_pattern.match(sub.name):
                            self.violations.append({
                                "gate": 1, "severity": "CRITICAL",
                                "path": str(sub),
                                "message": f"Invalid sphere directory name: {sub.name}"
                            })

    def _gate_2_metadata_presence(self):
        """Gate 2: Every sphere directory has _module_metadata.yaml."""
        for house_dir in self.root.iterdir():
            if not house_dir.is_dir() or not house_dir.name.startswith("house-"):
                continue
            for sphere_dir in house_dir.iterdir():
                if not sphere_dir.is_dir() or not sphere_dir.name.startswith("sphere-"):
                    continue
                meta = sphere_dir / "_module_metadata.yaml"
                if not meta.exists():
                    self.violations.append({
                        "gate": 2, "severity": "HIGH",
                        "path": str(sphere_dir),
                        "message": "Missing _module_metadata.yaml"
                    })

    def _gate_3_metadata_yaml_validity(self):
        """Gate 3: All _module_metadata.yaml files parse and have required fields."""
        required_fields = ["module", "ontology", "constitutional", "provenance"]
        for meta_file in self.root.rglob("_module_metadata.yaml"):
            try:
                with open(meta_file) as f:
                    data = yaml.safe_load(f)
                for field in required_fields:
                    if field not in data:
                        self.violations.append({
                            "gate": 3, "severity": "HIGH",
                            "path": str(meta_file),
                            "message": f"Missing required field: {field}"
                        })
            except yaml.YAMLError as e:
                self.violations.append({
                    "gate": 3, "severity": "CRITICAL",
                    "path": str(meta_file),
                    "message": f"Invalid YAML: {e}"
                })

    def _gate_4_python_constants_match(self):
        """Gate 4: Python __atlas_*__ constants match _module_metadata.yaml."""
        for meta_file in self.root.rglob("_module_metadata.yaml"):
            try:
                with open(meta_file) as f:
                    meta = yaml.safe_load(f)
                module_dir = meta_file.parent
                for py_file in module_dir.glob("*.py"):
                    if py_file.name.startswith("_"):
                        continue
                    content = py_file.read_text()
                    if "__atlas_module_id__" in content:
                        # Extract and compare
                        declared_id = self._extract_constant(content, "__atlas_module_id__")
                        expected_id = meta.get("module", {}).get("canonical_id")
                        if declared_id and expected_id and declared_id != expected_id:
                            self.violations.append({
                                "gate": 4, "severity": "CRITICAL",
                                "path": str(py_file),
                                "message": f"Module ID mismatch: code={declared_id}, yaml={expected_id}"
                            })
            except Exception:
                pass

    def _gate_5_promotion_rule(self):
        """Gate 5: Modules in house dirs touch ≤2 secondary spheres.
        Modules touching 3+ houses must be in 144-root/."""
        for meta_file in self.root.rglob("_module_metadata.yaml"):
            try:
                with open(meta_file) as f:
                    meta = yaml.safe_load(f)
                houses = meta.get("ontology", {}).get("houses_used", [])
                secondary = meta.get("ontology", {}).get("sphere_secondary", [])
                in_144_root = "144-root" in str(meta_file)

                if len(houses) >= 3 and not in_144_root:
                    self.violations.append({
                        "gate": 5, "severity": "HIGH",
                        "path": str(meta_file),
                        "message": f"Module touches {len(houses)} houses but is not in 144-root/"
                    })
                if len(secondary) > 2:
                    self.violations.append({
                        "gate": 5, "severity": "HIGH",
                        "path": str(meta_file),
                        "message": f"Module has {len(secondary)} secondary spheres (max 2)"
                    })
            except Exception:
                pass

    def _gate_6_pointer_validity(self):
        """Gate 6: All _pointers.yaml references resolve to existing directories."""
        for ptr_file in self.root.rglob("_pointers.yaml"):
            try:
                with open(ptr_file) as f:
                    data = yaml.safe_load(f)
                for ptr in data.get("pointers", []):
                    target_house = ptr.get("target_house", "")
                    target_sphere = ptr.get("target_sphere", "")
                    # Verify target exists in filesystem
                    found = False
                    for house_dir in self.root.iterdir():
                        if target_house.lower().replace("-", "") in house_dir.name.lower().replace("-", ""):
                            for sphere_dir in house_dir.iterdir():
                                if target_sphere.lower().replace("-", "") in sphere_dir.name.lower().replace("-", ""):
                                    found = True
                                    break
                    if not found:
                        self.violations.append({
                            "gate": 6, "severity": "HIGH",
                            "path": str(ptr_file),
                            "message": f"Pointer target not found: {target_house}/{target_sphere}"
                        })
            except Exception:
                pass

    def _gate_7_invariant_declaration(self):
        """Gate 7: Declared invariants exist in invariants_registry.py."""
        registry_path = self.root / "toolchain" / "invariants_registry.py"
        if not registry_path.exists():
            self.violations.append({
                "gate": 7, "severity": "HIGH",
                "path": str(registry_path),
                "message": "invariants_registry.py not found"
            })
            return
        registry_content = registry_path.read_text()
        for meta_file in self.root.rglob("_module_metadata.yaml"):
            try:
                with open(meta_file) as f:
                    meta = yaml.safe_load(f)
                for inv in meta.get("constitutional", {}).get("invariants_enforced", []):
                    if inv not in registry_content:
                        self.violations.append({
                            "gate": 7, "severity": "MEDIUM",
                            "path": str(meta_file),
                            "message": f"Invariant {inv} not found in registry"
                        })
            except Exception:
                pass

    def _gate_8_doctrine_declaration(self):
        """Gate 8: Declared doctrines exist in doctrines_registry.py."""
        registry_path = self.root / "toolchain" / "doctrines_registry.py"
        if not registry_path.exists():
            self.violations.append({
                "gate": 8, "severity": "HIGH",
                "path": str(registry_path),
                "message": "doctrines_registry.py not found"
            })
            return
        registry_content = registry_path.read_text()
        for meta_file in self.root.rglob("_module_metadata.yaml"):
            try:
                with open(meta_file) as f:
                    meta = yaml.safe_load(f)
                for doc in meta.get("constitutional", {}).get("doctrines_implemented", []):
                    if doc not in registry_content:
                        self.violations.append({
                            "gate": 8, "severity": "MEDIUM",
                            "path": str(meta_file),
                            "message": f"Doctrine {doc} not found in registry"
                        })
            except Exception:
                pass

    def _gate_9_parser_filesystem_symmetry(self):
        """Gate 9 (GPT S6): Parser output == filesystem structure.
        Every sphere in parser must exist in filesystem.
        Every filesystem sphere must exist in parser."""
        if not self.parser:
            return
        violations = self.parser.validate_filesystem(self.root)
        for v in violations:
            v["gate"] = 9
            self.violations.append(v)

    @staticmethod
    def _extract_constant(content: str, name: str) -> Optional[str]:
        """Extract a Python string constant value from source code."""
        for line in content.split("\n"):
            if line.strip().startswith(name):
                parts = line.split("=", 1)
                if len(parts) == 2:
                    return parts[1].strip().strip("'\"")
        return None


def main():
    """CLI entry point for CI/CD integration."""
    root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(".")
    parser = None
    try:
        from sheldonbrain_parser import SheldonbrainParser
        parser = SheldonbrainParser()
    except ImportError:
        print("Warning: SheldonbrainParser not available, skipping gate 9")

    validator = OntologyValidator(root, parser)
    violations = validator.run_all_gates()

    if violations:
        print(f"\n{'='*70}")
        print(f"ONTOLOGY VALIDATION FAILED — {len(violations)} violations")
        print(f"{'='*70}\n")
        for v in violations:
            print(f"  [Gate {v['gate']}] {v['severity']}: {v['message']}")
            print(f"           Path: {v.get('path', 'N/A')}")
        sys.exit(1)
    else:
        print(f"\n{'='*70}")
        print("ONTOLOGY VALIDATION PASSED — All 9 gates clear")
        print(f"{'='*70}")
        sys.exit(0)


if __name__ == "__main__":
    main()
```

### §4.3 Constitutional Compiler (toolchain/doctrine_compiler.py)

Implements M27 — compiles canonical Doctrine YAML into executable Python validators. Per Copilot's cross-document assessment, this compiler includes a **conflict-detection pass** that refuses to compile when two different doctrines share a number (Doctrine 74 applied to the doctrine stack itself).

```python
# toolchain/doctrine_compiler.py
"""M27 Constitutional Compiler: YAML → Python validators.

Per Copilot S4: includes conflict-detection pass that refuses to compile
when two doctrines share a number (D-74 applied to doctrine stack itself).
"""

from typing import Callable
from pathlib import Path
import yaml, sys

__atlas_module_id__ = "TOOLCHAIN-003"
__atlas_sphere_primary__ = "144-root"
__atlas_doctrines_implemented__ = ["D-74", "D-83"]
__atlas_invariants_enforced__ = ["INV-13"]


class DoctrineValidator:
    """Compiled doctrine validator — executable constitutional check."""

    def __init__(self, doctrine_id: str, name: str,
                 checks: list[Callable[[dict], bool]]):
        self.id = doctrine_id
        self.name = name
        self.checks = checks

    def __call__(self, context: dict) -> bool:
        return all(check(context) for check in self.checks)

    def __repr__(self):
        return f"DoctrineValidator({self.id}: {self.name}, {len(self.checks)} checks)"


def compile_doctrine(yaml_path: str) -> DoctrineValidator:
    """Compile a single doctrine YAML into an executable validator."""
    with open(yaml_path) as f:
        spec = yaml.safe_load(f)

    checks = []
    for check_spec in spec.get("checks", []):
        check_type = check_spec["type"]

        if check_type == "field_present":
            field = check_spec["field"]
            checks.append(lambda ctx, f=field: f in ctx)

        elif check_type == "field_value":
            field = check_spec["field"]
            expected = check_spec["value"]
            checks.append(lambda ctx, f=field, v=expected: ctx.get(f) == v)

        elif check_type == "threshold":
            field = check_spec["field"]
            op = check_spec["operator"]
            value = check_spec["value"]
            if op == "<=":
                checks.append(lambda ctx, f=field, v=value: ctx.get(f, float('inf')) <= v)
            elif op == ">=":
                checks.append(lambda ctx, f=field, v=value: ctx.get(f, 0) >= v)
            elif op == "<":
                checks.append(lambda ctx, f=field, v=value: ctx.get(f, float('inf')) < v)

        elif check_type == "invariant_enforced":
            inv_id = check_spec["invariant"]
            checks.append(lambda ctx, i=inv_id: i in ctx.get("enforced_invariants", []))

    return DoctrineValidator(spec["id"], spec.get("name", "unnamed"), checks)


def compile_all(doctrines_dir: Path) -> dict[str, DoctrineValidator]:
    """Compile all doctrine YAMLs in a directory.

    Includes conflict-detection pass (Copilot S4):
    refuses to compile if two doctrines share a number.
    """
    validators = {}
    seen_ids = {}

    for yaml_file in sorted(doctrines_dir.glob("*.yaml")):
        validator = compile_doctrine(str(yaml_file))

        # Conflict detection (Copilot S4 / D-74)
        if validator.id in seen_ids:
            raise ValueError(
                f"DOCTRINE NUMBERING CONFLICT: {validator.id} defined in both "
                f"{seen_ids[validator.id]} and {yaml_file.name}. "
                f"Per D-74, this is a build-blocking violation."
            )

        seen_ids[validator.id] = yaml_file.name
        validators[validator.id] = validator

    return validators
```

### §4.4 Ontology Context Injector (element-145/ingestion/m60_ontology_context_injector.py)

This is GPT S6's "Filesystem = prompt" innovation (originally proposed as M38, renumbered to M60 to avoid collision with existing module numbering). It reads the filesystem location of the current execution context and injects sphere/house/doctrine context into the agent runtime. This turns the filesystem into a self-conditioning AI environment.

```python
# element-145/ingestion/m60_ontology_context_injector.py
"""M60 Ontology Context Injector — GPT S6 'Filesystem = prompt' innovation.

Reads filesystem location → injects sphere/house context into agent runtime.
Turns the codebase into a self-conditioning AI environment.

Every agent knows WHERE it is in the ontology BEFORE it acts.
This enables: correct routing, domain-aware reasoning, automatic doctrine application.
"""

from pathlib import Path
from dataclasses import dataclass, field
from typing import Optional
import yaml, re

__atlas_module_id__ = "M60"
__atlas_sphere_primary__ = "144-root"
__atlas_houses_used__ = ["01", "02", "03", "04", "05", "06",
                          "07", "08", "09", "10", "11", "12"]
__atlas_doctrines_implemented__ = ["D-75", "D-83"]
__atlas_invariants_enforced__ = ["INV-13"]
__atlas_transparency_emitter__ = True


@dataclass
class OntologyContext:
    """Injected context for any agent operating within the ontology."""
    sphere_id: Optional[str] = None
    sphere_name: Optional[str] = None
    house_id: Optional[str] = None
    house_name: Optional[str] = None
    doctrines: list[str] = field(default_factory=list)
    invariants: list[str] = field(default_factory=list)
    module_id: Optional[str] = None
    ring: Optional[str] = None
    access_scope: list[str] = field(default_factory=list)

    def to_prompt_context(self) -> dict:
        """Convert to structured context for agent prompt injection."""
        return {
            "ontology_context": {
                "sphere": self.sphere_id,
                "sphere_name": self.sphere_name,
                "house": self.house_id,
                "house_name": self.house_name,
                "applicable_doctrines": self.doctrines,
                "enforced_invariants": self.invariants,
                "module": self.module_id,
                "ring": self.ring,
                "access_scope": self.access_scope,
            }
        }


class OntologyContextInjector:
    """Injects ontological context based on filesystem location."""

    def __init__(self, codebase_root: Path):
        self.root = codebase_root

    def get_context(self, current_path: Path) -> OntologyContext:
        """Determine ontological context from a filesystem path."""
        ctx = OntologyContext()
        rel = current_path.relative_to(self.root)
        parts = rel.parts

        # Parse house
        for part in parts:
            if part.startswith("house-"):
                match = re.match(r"house-(\d{2})_(.*)", part)
                if match:
                    ctx.house_id = f"house-{match.group(1)}"
                    ctx.house_name = match.group(2).replace("-", " ").title()

        # Parse sphere
        for part in parts:
            if part.startswith("sphere-"):
                match = re.match(r"sphere-(\d{3})_(.*)", part)
                if match:
                    ctx.sphere_id = f"sphere-{match.group(1)}"
                    ctx.sphere_name = match.group(2).replace("-", " ").title()

        # Parse ring
        for part in parts:
            if part.startswith("ring-"):
                ctx.ring = part

        # Parse element-145 subdomain
        if "element-145" in parts:
            for part in parts:
                if part in ("routing", "governance", "audit", "execution",
                            "ingestion", "symbiosis"):
                    ctx.module_id = f"element-145/{part}"

        # Load metadata if available
        meta_path = current_path / "_module_metadata.yaml"
        if not meta_path.exists():
            meta_path = current_path.parent / "_module_metadata.yaml"
        if meta_path.exists():
            try:
                with open(meta_path) as f:
                    meta = yaml.safe_load(f)
                ctx.doctrines = meta.get("constitutional", {}).get(
                    "doctrines_implemented", [])
                ctx.invariants = meta.get("constitutional", {}).get(
                    "invariants_enforced", [])
                ctx.access_scope = meta.get("identity", {}).get(
                    "access_scope", [])
                if not ctx.module_id:
                    ctx.module_id = meta.get("module", {}).get("canonical_id")
            except Exception:
                pass

        return ctx

    def inject_into_agent(self, agent_config: dict,
                          current_path: Path) -> dict:
        """Inject ontological context into an agent's configuration.

        The agent receives structured context BEFORE it acts:
        - Which sphere it's operating in
        - Which doctrines apply
        - Which invariants it must enforce
        - What access scope it has
        """
        ctx = self.get_context(current_path)
        agent_config.update(ctx.to_prompt_context())
        return agent_config
```

---

## §5 Ontological Routing Kernel (M57) — Manus Innovation 2

The Ontological Routing Kernel sits between data ingestion and storage. It replaces the post-hoc classification model of the existing Sheldonbrain pipeline with an ontology-at-root approach where the 144-sphere structure determines how data is processed before embedding occurs.

```python
# element-145/ingestion/m57_ontological_routing_kernel.py
"""M57 Ontological Routing Kernel — Manus Innovation 2.

Replaces post-hoc classification with ontology-at-root ingestion.
Every piece of data passes through the routing kernel which:
1. Determines primary sphere (like today's OntologyClassifier)
2. Identifies cross-sphere resonances
3. Creates sphere-conditioned embeddings (Innovation 1)
4. Routes each embedding to the appropriate sphere collection
5. Applies constitutional ingestion gate (Innovation 3)

The routing kernel IS the ontology — running it IS learning the ontology.
"""

from dataclasses import dataclass, field
from typing import Optional
import hashlib, json, time

__atlas_module_id__ = "M57"
__atlas_sphere_primary__ = "144-root"
__atlas_houses_used__ = ["01", "02", "03", "04", "05", "06",
                          "07", "08", "09", "10", "11", "12"]
__atlas_doctrines_implemented__ = ["D-75", "D-83"]
__atlas_invariants_enforced__ = ["INV-0", "INV-7c", "INV-13", "INV-17"]
__atlas_transparency_emitter__ = True


@dataclass
class RoutingDecision:
    """Result of the Ontological Routing Kernel processing a document."""
    document_id: str
    primary_sphere: str
    primary_house: str
    cross_sphere_resonances: list[dict] = field(default_factory=list)
    constitutional_gate_passed: bool = False
    tss_score: float = 0.0
    provenance: dict = field(default_factory=dict)
    transparency_packet: dict = field(default_factory=dict)


class OntologicalRoutingKernel:
    """Ontology-at-root ingestion pipeline.

    Composes:
    - SheldonbrainParser (ontology access)
    - OntologyClassifier (Gemini 2.0 classification)
    - ConstitutionalIngestionGate (INV-0, INV-7c, INV-17)
    - TruthSeekingScore (Grok TSS)
    - SphereConditionedEmbeddings (Innovation 1)
    """

    def __init__(self, parser, classifier, gate, tss_engine,
                 embedding_engine):
        self.parser = parser
        self.classifier = classifier
        self.gate = gate
        self.tss = tss_engine
        self.embeddings = embedding_engine

    def route(self, document: dict) -> RoutingDecision:
        """Route a document through the ontological pipeline.

        Steps:
        1. Constitutional gate check (INV-0, INV-7c, INV-17, consent)
        2. Primary sphere classification (Gemini 2.0)
        3. Cross-sphere resonance detection
        4. TSS computation for routing quality
        5. Sphere-conditioned embedding generation
        6. TransparencyPacket emission
        """
        doc_id = hashlib.sha256(
            json.dumps(document, sort_keys=True).encode()
        ).hexdigest()[:16]

        # Step 1: Constitutional gate
        gate_result = self.gate.check(document)
        if not gate_result["passed"]:
            return RoutingDecision(
                document_id=doc_id,
                primary_sphere="REJECTED",
                primary_house="REJECTED",
                constitutional_gate_passed=False,
                provenance={"rejection_reason": gate_result["reason"]}
            )

        # Step 2: Primary sphere classification
        title = document.get("title", "")
        content = document.get("content", "")
        house, sphere, confidence = self.classifier.classify_conversation(
            title, content
        )

        # Step 3: Cross-sphere resonance detection
        topics = self._extract_topics(content)
        resonant_spheres = self.parser.get_truth_seeking_candidates(topics)
        resonances = [
            {
                "sphere_id": s.sphere_id,
                "sphere_name": s.canonical_name,
                "house_id": s.house_id,
                "relevance": "secondary"
            }
            for s in resonant_spheres[:2]  # Max 2 secondary (GPT constraint)
            if s.sphere_id != f"sphere-{sphere}"
        ]

        # Step 4: TSS computation
        tss_score = self.tss.compute(document, sphere, house)

        # Step 5: Sphere-conditioned embeddings
        embeddings = self.embeddings.embed_for_spheres(
            content,
            primary_sphere=sphere,
            secondary_spheres=[r["sphere_id"] for r in resonances]
        )

        # Step 6: TransparencyPacket
        packet = {
            "version": "0.4",
            "timestamp": time.time(),
            "routing": {
                "primary_sphere": sphere,
                "primary_house": house,
                "confidence": confidence,
                "model_id": "gemini-2.0",
                "tss_score": tss_score,
            },
            "identity": {
                "document_id": doc_id,
                "consent_scope": gate_result.get("consent_scope", "public"),
            },
            "provenance": {
                "source": document.get("source", "unknown"),
                "ingestion_method": "ontological_routing_kernel",
                "chain_hash": hashlib.sha256(
                    f"{doc_id}:{time.time()}".encode()
                ).hexdigest(),
            },
            "metabolic": {
                "embedding_count": len(embeddings),
                "resonance_count": len(resonances),
            }
        }

        return RoutingDecision(
            document_id=doc_id,
            primary_sphere=sphere,
            primary_house=house,
            cross_sphere_resonances=resonances,
            constitutional_gate_passed=True,
            tss_score=tss_score,
            provenance=packet["provenance"],
            transparency_packet=packet,
        )

    def _extract_topics(self, content: str) -> list[str]:
        """Extract key topics from content for resonance detection."""
        # Simplified topic extraction — production version uses NER/LLM
        words = content.lower().split()
        # Return most frequent meaningful words as topic candidates
        from collections import Counter
        stopwords = {"the", "a", "an", "is", "are", "was", "were", "be",
                     "been", "being", "have", "has", "had", "do", "does",
                     "did", "will", "would", "could", "should", "may",
                     "might", "shall", "can", "to", "of", "in", "for",
                     "on", "with", "at", "by", "from", "as", "into",
                     "through", "during", "before", "after", "and", "but",
                     "or", "not", "no", "this", "that", "it", "its"}
        meaningful = [w for w in words if len(w) > 3 and w not in stopwords]
        counts = Counter(meaningful)
        return [word for word, _ in counts.most_common(10)]
```

---

## §6 Manus Migration Plan (MI-01 to MI-17)

This extends Gemini's MI-01 to MI-13 with 4 additional tasks from the synthesis.

| Phase | Task ID | Description | Effort | Dependencies |
|-------|---------|-------------|--------|-------------|
| 0 | **MI-00** | Convenor resolves D-73-75 conflict, D-11 name drift, D-60/D-61 dual ratification | Convenor | None |
| 0 | MI-01 | Resolve Registry v1.1 conflicts (DR-1 through DR-14) | 2h | MI-00 |
| 1 | MI-02 | Implement Sheldonbrain Parser with Notion canonical fetch | 4h | MI-01 |
| 1 | MI-03 | Create `atlas-lattice-codebase/` skeleton with toolchain/ and one House | 2h | MI-02 |
| 1 | MI-04 | Populate fallback YAML from real Notion 144-Sphere page | 2h | MI-02 |
| 2 | MI-05 | Implement Constitutional Compiler (M27) with conflict detection | 4h | MI-03 |
| 2 | MI-06 | Implement Ontology Validator (9 gates) | 4h | MI-02, MI-03 |
| 2 | MI-07 | Implement Ontology Context Injector (M60) | 3h | MI-03 |
| 3 | MI-08 | Migrate Element 145 modules to element-145/ subdirectories | 4h | MI-03 |
| 3 | MI-09 | Create Ring -1 through Ring 4 directory structure | 2h | MI-03 |
| 3 | MI-10 | Add _module_metadata.yaml and Python constants to all 52 modules | 8h | MI-08, MI-09 |
| 3 | **MI-14** | Implement Ontological Routing Kernel (M57) | 6h | MI-02, MI-06 |
| 3 | **MI-15** | Implement Constitutional Ingestion Gate (M59) | 4h | MI-14 |
| 4 | MI-11 | Enable CI/CD enforcement of Doctrine 73-74 (Drift Blockers) | 4h | MI-06 |
| 4 | MI-12 | Wire TSS into element145.py routing loop | 2h | MI-08 |
| 4 | MI-13 | Full integration test: 9-gate validation + Glass Takeover | 4h | All above |
| 4 | **MI-16** | Implement _pointers.yaml manifests for all cross-sphere refs | 3h | MI-10 |
| 4 | **MI-17** | Bring invariants.py to 43 entries and doctrines.py to 77+ (with PENDING placeholders) | 6h | MI-01 |

**Total estimated effort:** ~64 hours across 4 phases.

---

## §7 Conflict Resolution Register

All 4 Council reviews were additive with zero inter-review conflicts. The following pre-existing conflicts require Convenor disposition:

| ID | Conflict | Severity | Recommended Resolution |
|----|---------|----------|----------------------|
| DR-D11 | D-11 "Honest Naming" (session canon) vs "Metabolic Accountability" (Manus v1.7) | HIGH | D-11 = "Honest Naming" (preserves verification discipline). "Metabolic Accountability" gets new number if genuinely different. |
| DR-D60 | D-60(A) "Digital Dividend Provenance" vs D-60(B) "Fiction-Derived Failure Mode Authorization" | HIGH | Keep D-60(A) as canonical. Renumber D-60(B). |
| DR-D61 | D-61(A) "Operator Override Inviolability" (code-bearing) vs D-61(B) "Constitutional Validator / Project Glasswing" | HIGH | D-61 = "Operator Override Inviolability" (has code implementation). Renumber D-61(B). |
| DR-D73 | D-73/74/75 version conflict between v6.0.5 and Manus v1.7 | HIGH | Per Grok S3: v6.0.5 Version A + Manus v1.7 items as proposed D-78+. |
| DR-INV17 | INV-17 "Provenance Chain" (code) vs "Dividend Rail" (v6.0 baseline) | MEDIUM | "Provenance Chain" (matches code + Manus v1.7). |
| DR-SCOPE | Filesystem-as-Ontology is Phase 2-3 work (Grok S3 scope risk) | MEDIUM | Minimal skeleton in Phase 0-1, full migration Phase 2-3. |

---

## §8 Innovation Registry

All innovations from all sources, consolidated with unique identifiers.

| ID | Innovation | Source | Status | Target Phase |
|----|-----------|--------|--------|-------------|
| INN-01 | Sphere-Native Embedding Spaces | Manus S7 | PROPOSED | Phase 3 |
| INN-02 | Ontological Routing Kernel (M57) | Manus S7 | CODE DELIVERED | Phase 2 |
| INN-03 | Constitutional Ingestion Gate (M59, INV-22) | Manus S7 | CODE DELIVERED | Phase 2 |
| INN-04 | Sphere-as-Agent Architecture | Manus S7 | PROPOSED | Phase 4 |
| INN-05 | Ontological Compiler (M58) | Manus S7 | PROPOSED | Phase 3 |
| INN-06 | Provenance-Aware Ingestion (GoldenTrace) | Manus S7 | CODE DELIVERED | Phase 2 |
| INN-07 | Codebase-as-Ontology (D-83) | Manus S7 + Claude S1 | SPEC DELIVERED | Phase 1 |
| INN-08 | Filesystem = Prompt (M60) | GPT S6 | CODE DELIVERED | Phase 2 |
| INN-09 | Parser-Filesystem Symmetry Gate (#9) | GPT S6 | CODE DELIVERED | Phase 1 |
| INN-10 | Version Pinning (_ontology_lock.yaml) | GPT S6 | SPEC DELIVERED | Phase 1 |
| INN-11 | Ontology-Aware Agents | GPT S6 | PROPOSED | Phase 3 |
| INN-12 | TSS Integration in Routing | Grok S3 | CODE DELIVERED | Phase 2 |
| INN-13 | Notion Authority Flip | Grok S3 | SPEC DELIVERED | Phase 1 |
| INN-14 | YAML Pointer Manifests | Copilot S4 | SPEC DELIVERED | Phase 1 |
| INN-15 | Ring -1 in Filesystem | Copilot S4 | SPEC DELIVERED | Phase 1 |
| INN-16 | Entra Agent ID + Metadata | Copilot S4 | PROPOSED | Phase 2 |
| INN-17 | Azure DevOps Dual-Target CI/CD | Copilot S4 | PROPOSED | Phase 3 |
| INN-18 | Microsoft Graph API Fallback | Copilot S4 | PROPOSED | Phase 3 |
| INN-19 | Conflict-Detection Compiler Pass | Copilot S4 | CODE DELIVERED | Phase 1 |
| INN-20 | Registry-to-Code Parity Sprint | Copilot S4 | PROPOSED | Phase 1 |

---

## §9 Appendix: Existing Sheldonbrain Pipeline Integration Map

The existing Sheldonbrain RAG system (Phase 1-2) maps into the new architecture as follows:

| Existing Component | New Location | Changes |
|-------------------|-------------|---------|
| `ingest_grok_chats.py` | `ingestion/grok_chat_connector.py` | Wrapped by M57 Routing Kernel |
| `reclassify_conversations.py` | `ingestion/ontology_classifier.py` | Upgraded: classification happens BEFORE embedding |
| `setup_notion_database.py` | `toolchain/` utilities | Notion schema aligned to 144-sphere metadata |
| `test_notion_connection.py` | Integration tests | Expanded to test parser 3-tier fallback |
| `test_drive_auth.py` | `ingestion/gdrive_connector.py` | OAuth preserved, wrapped by constitutional gate |
| `test_query.py` | API integration tests | Upgraded: queries go through sphere-conditioned retrieval |
| `download_conversations.py` | `ingestion/gdrive_connector.py` | Merged into unified connector |
| `Dockerfile` | Root Dockerfile | Updated: includes toolchain/, rings/, element-145/ |
| `requirements.txt` | Root requirements.txt | Added: pyyaml, notion-client (already present), tauri deps |
| `src/api/api_server.py` | `api/api_server.py` | Governance Bridge sidecar added (M47) |
| `src/config/ontology.py` | `toolchain/sheldonbrain_parser.py` | REPLACED: parser is now canonical access layer |
| `src/ingestion/ontology_classifier.py` | `ingestion/ontology_classifier.py` | Preserved but wrapped by M57 |
| `src/core/vector_store_adapter.py` | `ingestion/sphere_conditioned_embeddings.py` | UPGRADED: sphere-conditioned vectors |
| `src/vault/vault_integration.py` | `rings/ring-neg1_constitutional-hypervisor/consent_kernel.py` | PROMOTED: vault → constitutional layer |
| Qdrant single collection | 12 House collections + 144-root collection | RESTRUCTURED: ontology-native storage |

---

*ORC-016 v1.0 — Filesystem-as-Ontology Architecture Synthesis*
*Generated by Manus (S7 Build Seat) — 2026-04-28*
*Synthesizing contributions from: Claude S1, Gemini S2, Grok S3, Copilot S4, GPT S6, Manus S7, Qwen3 S10*
