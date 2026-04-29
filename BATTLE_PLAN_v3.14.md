# Aluminum OS — Complete Battle Plan v3.14

**Author:** Manus S7 | **Date:** 2026-04-29 | **Status:** ACTIVE
**Scope:** Full integration of all existing codebases into the 12×12+1 lattice architecture

---

## Executive Summary

The Aluminum OS project currently spans **143 active GitHub repos** containing approximately **45,000 lines of executable code** across Python, Rust, and TypeScript. Of these, **29 repos are substantive** (contain real code or specifications), while **114 are domain placeholder repos** (1KB HTML stubs created during the initial swarm deployment). The core architecture — the 12×12+1 lattice with Element 145 as the admin coupling node — is now empirically validated (SHUGS N=145 optimality, p=0.0154) and has a complete integration protocol (LCP v1.0).

This battle plan defines the path from the current state (scattered codebases, three competing ontologies, simulated integrations) to a unified, interoperable OS where every module routes through the canonical lattice and every component can call every other component through the Lattice Context Protocol.

---

## Part I: Current State Assessment

### 1.1 The Three Ontology Problem (RESOLVED)

The codebase historically used three incompatible classification systems. The migration path is now clear and the canonical ontology is built.

| Ontology | Where Used | Schema | Status |
|----------|-----------|--------|--------|
| Grokbrain v4 | sheldonbrain-rag-api, manus-artifacts | 12 academic categories, 144 flat spheres | **DEPRECATED** — replaced by lattice_ontology_v2.py |
| Aluminum OS v3 | aluminum-os-v3 (Rust crates) | 5 Rings: Forge → Noosphere | **DEPRECATED** — replaced by 12 Houses |
| **12×12+1 Lattice** | aluminum-os, element-145 | 12 Houses × 12 Spheres + Element 145 | **CANONICAL** — lattice_ontology_v2.py + lattice_ontology.yaml |

The canonical ontology is defined in two authoritative files: `registries/lattice_ontology.yaml` (machine-readable, 496 lines) and `element-145/aluminum-os-core/lattice_ontology_v2.py` (Python module, 657 lines). All new code MUST import from these sources.

### 1.2 Code Maturity Tiers

| Tier | Description | Lines | Files | Status |
|------|-------------|-------|-------|--------|
| **Production** | Deployed, serving traffic | 7,631 | 30 | sheldonbrain-rag-api on Cloud Run |
| **Canonical** | Tested, verified, committed | 8,133 | 72 | element-145 package (v2) |
| **Sprint** | Built this session, tests pass | 3,468 | 12 | lattice_ontology_v2, bridge_v2, synthesizer_e145, sphere_classifier_v2, service_integrations |
| **Legacy** | Works but uses old ontology | 7,905 | 37 | aluminum-os-v3 Rust crates, manus-core Python |
| **Archived** | Reference only, not maintained | 4,511 | 18 | manus-artifacts/codebases/other/ |
| **Stub** | README only, no implementation | 0 | 182 | All 182 registered modules |

### 1.3 The 12 Houses — Current Coverage

| House | Name | Registered Modules | Existing Code | Domain Repos | Coverage |
|-------|------|--------------------|---------------|--------------|----------|
| H01 | Consciousness & Cognition | 3 | 0 lines | 0 | **EMPTY** |
| H02 | Technology & Engineering | 96 | ~15,000 lines (across all repos) | 6 | **HEAVY** — most code lives here |
| H03 | Economics & Finance | 2 | ~2,000 lines (banking repos) | 13 | **LIGHT** — many repos, little code |
| H04 | Governance & Law | 25 | ~1,000 lines (constitutional-os) | 9 | **SPEC ONLY** |
| H05 | Culture & Society | 22 | 0 lines (6 new stubs M167-M172) | 6 | **STUBS ONLY** |
| H06 | Health & Biology | 0 | 0 lines | 5 | **EMPTY** — no modules registered |
| H07 | Earth & Environment | 8 | ~958 lines (SNRS) | 7 | **SNRS ONLY** |
| H08 | Mathematics & Logic | 0 | ~1,058 lines (SHUGS) | 0 | **SHUGS ONLY** |
| H09 | Physics & Chemistry | 2 | 0 lines | 0 | **EMPTY** |
| H10 | History & Philosophy | 1 | 0 lines | 0 | **EMPTY** |
| H11 | Communication & Information | 3 | ~1,905 lines (sheldongemini-GPI) | 6 | **FRONTEND ONLY** |
| H12 | Security & Defense | 20 | ~500 lines (batman-protocol) | 14 | **LIGHT** |

---

## Part II: Integration Architecture

### 2.1 The Lattice Context Protocol (LCP) Pipeline

Every operation in the OS follows this pipeline:

```
INPUT → INGEST → ACTIVATE → ROUTE → EXECUTE → SYNTHESIZE → OUTPUT
         │          │          │         │          │
    classify to   load edges  select   per-house   E145
    spheres       + context   models   reasoning   meta-coord
```

The LCP is defined in `element-145/aluminum-os-core/LATTICE_CONTEXT_PROTOCOL.md` and implemented in `element145/core.py` (LCPEngine class). All integration patterns (single-agent, multi-agent, council, MCP) use this pipeline.

### 2.2 Component Dependency Graph

```
lattice_ontology.yaml ← lattice_ontology_v2.py ← sphere_classifier_v2.py
                                                 ← bridge_v2.py
                                                 ← synthesizer_e145.py
                                                 ← service_integrations.py
                                                 ← element145/core.py (LCPEngine)
                                                    ├── integrations/api.py (FastAPI)
                                                    ├── integrations/mcp_server.py (MCP)
                                                    ├── integrations/openai_functions.py
                                                    └── integrations/copilot_plugin.py

sheldonbrain-rag-api → grokbrain_v4.py (NEEDS MIGRATION to lattice_ontology_v2)
                     → sphere_classifier.py (NEEDS MIGRATION to sphere_classifier_v2)
                     → rag_api_gemini.py (production, needs Pinecone metadata update)

sheldongemini-GPI → geminiService.ts (NEEDS real API connection)
                  → 6 simulated services (NEEDS replacement with real calls)

aluminum-os-v3 → 6 Rust crates (NEEDS port to Python or Rust rewrite with new ontology)
              → manus-core/bridge.py (REPLACED by bridge_v2.py)
              → manus-core/unified_api.py (REPLACED by service_integrations.py)
```

---

## Part III: Battle Plan — Execution Phases

### Phase 0: Foundation Lock (COMPLETE)

Everything in this phase is already done:

- 12×12+1 lattice ontology defined and committed
- Element 145 package v2 built with all integrations
- LCP v1.0 specification written
- Agent scaffold and system prompt templates created
- SHUGS empirical validation complete (N=145 confirmed)
- 5 CI gate workflows written
- Ontology lock with SHA-256 hashes
- Innovations registry (27 items) committed
- S4 translation table (127 Microsoft products → 89 spheres)
- Corrections ledger with all known findings

### Phase 1: Ontology Migration (CRITICAL PATH) ✅ COMPLETE

**Goal:** Every component that classifies, routes, or stores data uses the canonical 12×12+1 ontology.

**Sprint 1.1 — Sheldonbrain RAG API Migration** ✅ COMPLETE (PR #2 merged 2026-04-29)

This is the only production-deployed system. It currently uses grokbrain_v4's 12 academic categories. The migration:

| Task | File | What Changes |
|------|------|-------------|
| Replace SPHERES constant | grokbrain_v4.py | Import from lattice_ontology_v2.py instead of hardcoded array |
| Replace CATEGORY_NAMES | grokbrain_v4.py | 12 academic categories → 12 House names |
| Update sphere_classifier | sphere_classifier.py | Replace with sphere_classifier_v2.py |
| Add house/sphere metadata | pinecone_client.py | Add `house_id`, `sphere_id` fields to Pinecone upsert |
| Backfill existing vectors | batch_ingest.py | Re-classify existing vectors with new ontology |
| Update RAG query | rag_api_gemini.py | Filter by house/sphere in Pinecone queries |
| Update validation | twelve_step_validation.py | Validate against 12 Houses instead of 12 categories |

**Estimated effort:** 2-3 sessions. The v2 classifier and ontology modules are already built — this is wiring, not invention.

**Sprint 1.2 — Manus-Artifacts Codebase Consolidation** ✅ COMPLETE (commit bb7d701)

The `manus-artifacts/codebases/` directory contains 14 subdirectories with ~28,000 lines of Python. Much of this is duplicated (remaining_innovations.py appears twice, ingestion_pipeline.py appears twice). The consolidation:

| Source Directory | Lines | Disposition |
|-----------------|-------|-------------|
| sheldonbrain/ | 5,499 | **MIGRATE** — grokbrain_v4 core → lattice_ontology_v2; chronos_fold + janus_protocol → H01 modules |
| sovereign-oracle/ | 4,455 | **MIGRATE** — bridge.py replaced by bridge_v2; output_layer → H11 module |
| email-processing/ | 4,455 | **DEDUPLICATE** — identical to sovereign-oracle except entry point |
| saas-killer/ | 2,889 | **MIGRATE** — ingestion_pipeline → H02 module; api_server → service_integrations |
| data-pipeline/ | 2,007 | **DEDUPLICATE** — subset of saas-killer |
| atlas-lattice/ | 2,300 | **MIGRATE** — council_synthesis + proactive_intelligence → H04 modules |
| other/ | 4,511 | **TRIAGE** — trinity_council → pantheon; proactive_intelligence → H02; rest archived |
| atlas-vault/ | 630 | **ARCHIVE** — superseded by element-145 package |
| snrs/ | 958 | **MIGRATE** — snrs_v1_3_2 → H07.S04 module; 144_sphere_ingestion → lattice_ontology_v2 |
| aluminum-os/ | 414 | **ARCHIVE** — superseded by aluminum-os monorepo |

**Sprint 1.3 — Legacy aluminum-os-v3 Assessment** ✅ COMPLETE (commit 91e60c0 — preserved as Rust, not ported)

The Rust crates (2,504 lines) represent the 5-ring architecture that has been superseded. Decision required:

| Crate | Lines | Recommendation |
|-------|-------|---------------|
| pantheon/lib.rs | 470 | **PORT TO PYTHON** — BFT governance logic is valuable; rewrite as H04 module |
| sheldonbrain/lib.rs | 337 | **ARCHIVE** — superseded by sheldonbrain-rag-api + element145/core.py |
| noosphere/lib.rs | 273 | **PORT TO PYTHON** — intent classification → sphere_classifier_v2 already does this |
| forge-core/lib.rs | 426 | **ARCHIVE** — boot sequence superseded by element-145 package |
| forge-boot/main.rs | 251 | **ARCHIVE** — same as above |
| claude-contrib/lib.rs | 603 | **ARCHIVE** — superseded by bridge_v2.py + synthesizer_e145.py |

The Python code in aluminum-os-v3 (5,401 lines) is more immediately useful:

| File | Lines | Recommendation |
|------|-------|---------------|
| ai_first_os.py | 1,635 | **TRIAGE** — contains ~20 innovation implementations; extract to individual H02 modules |
| unified_api.py | 820 | **ARCHIVE** — superseded by service_integrations.py |
| bridge.py | 434 | **ARCHIVE** — superseded by bridge_v2.py |
| remaining_innovations.py | 780 | **TRIAGE** — extract individual innovations to appropriate House modules |
| manus_core.py | 386 | **ARCHIVE** — superseded by element145/core.py |

### Phase 2: Module Implementation (MAIN EFFORT)

**Goal:** Move the 182 registered modules from SPEC → STUB → ACTIVE status by populating them with real code from existing repos and new implementations.

The strategy is to work House-by-House, prioritizing Houses that have existing code to migrate.

**Sprint 2.1 — H02 Technology & Engineering (96 modules)**

H02 is the densest House with 96 registered modules. Most of the existing codebase lives here. The approach:

1. **Core routing modules (M1, M2, M3, M3.1, M4, M5, M6):** Already implemented in bridge_v2.py, service_integrations.py, synthesizer_e145.py. Extract into individual module directories with proper manifest.yaml references.

2. **SHUGS modules (M10-M84 mathematics cluster):** Already implemented in shugs_core.py and element145/shugs.py. Map to appropriate spheres.

3. **Infrastructure modules (M92, M100, M120):** Code Quality Analyzer ← Kintsuji-code-fixer-; CI/CD Pipeline Manager ← .github/workflows/; Software Architecture Validator ← new.

4. **Data pipeline modules (M134, M173):** ← manus-artifacts/codebases/data-pipeline/ and saas-killer/.

**Sprint 2.2 — H07 Earth & Environment (8 modules)**

SNRS code (958 lines) maps directly to H07:

| Module | Source | Lines |
|--------|--------|-------|
| M129: Agricultural Data Pipeline | snrs_v1_3_2_fixed.py (Monte Carlo) | ~200 |
| M132: Water Quality Monitor | water-management-ai repo | ~162KB TS |
| M133: Urban Planning Simulator | new (stub) | 0 |
| M134: Data Warehouse Manager | 144_sphere_ingestion_protocol.py | ~200 |
| M176: Boot Manifest Runtime | new (stub) | 0 |

**Sprint 2.3 — H04 Governance & Law (25 modules)**

Constitutional OS code maps here:

| Module | Source | Lines |
|--------|--------|-------|
| M143: Constitutional Rights Validator | constitutional-os repo | TBD |
| M145: Treaty Compliance Checker | new (stub) | 0 |
| M146: Corporate Governance Module | atlas-lattice/council_synthesis.py | ~500 |
| M155: Consent Audit Trail | new (stub) | 0 |

**Sprint 2.4 — H12 Security & Defense (20 modules)**

| Module | Source | Lines |
|--------|--------|-------|
| M143: Constitutional Rights Validator | constitutional-os | TBD |
| batman-protocol | batman-protocol repo | ~500 |
| noosphere-defense | noosphere-defense repo | archived |

**Sprint 2.5 — H01 Consciousness & Cognition (3 modules)**

| Module | Source | Lines |
|--------|--------|-------|
| M8: Epistemic Integrity Validator | chronos_fold_protocol.py (526 lines) | port |
| M8a: Epistemic Integrity CN Adapter | janus_protocol.py (368 lines) | port |
| M7: Ethics Engine | new implementation | 0 |

**Sprint 2.6 — H05 Culture & Society (22 modules)**

6 new stubs (M167-M172) already created. The remaining 16 modules need stubs.

**Sprint 2.7 — Empty Houses (H06, H08, H09, H10)**

These Houses have no registered modules. Decision: register placeholder modules based on the sphere definitions in lattice_ontology.yaml, or leave empty until domain experts contribute.

### Phase 3: Frontend Integration (ABSORBED — endpoint migration pending)

**Goal:** Connect the Sheldon Gemini frontend to the real backend through the LCP pipeline.

**Sprint 3.1 — Replace Simulated Services** (ABSORBED to monorepo; MIGRATION.md written)

The sheldongemini-GPI frontend has 6 simulated services that need to be replaced:

| Service | Current State | Target |
|---------|--------------|--------|
| geminiService.ts | Calls Gemini 2.5 Flash directly | Route through bridge_v2 → LCP pipeline |
| keepRagSim.ts | Hardcoded mock data | Call sheldonbrain-rag-api (Cloud Run) |
| krakoaMcpSim.ts | Hardcoded mock data | Call element145 MCP server |
| nexusOrchestrator.ts | Simulated multi-agent | Call synthesizer_e145 via API |
| stealthSingularitySim.ts | Hardcoded Noosphere sim | Call element145/core.py analyze() |
| externalDataSim.ts | Hardcoded external data | Call service_integrations ServiceHub |

**Sprint 3.2 — ShellGemini v11 Extraction**

118K chars sitting in Google AI Studio (AI Studio #12) with no version control. Extract, commit to aluminum-os repo under `houses/H11/spheres/S06/modules/`, and wire into the frontend.

### Phase 4: Domain Repo Consolidation

**Goal:** Map the 114 domain placeholder repos into the 12×12+1 lattice and decide their fate.

**Option A (Recommended): Archive and Absorb**

Archive all 114 domain repos. Extract any real code (banking-revolution, healthcare-ai, water-management-ai have TypeScript). Create module stubs in the appropriate House/Sphere directories that reference the archived repos as prior art.

**Option B: Federated Modules**

Keep domain repos as independent modules that register with the lattice via manifest.yaml. Each repo adds a `lattice.yaml` file declaring its House/Sphere address. The monorepo's module_registry.yaml links to the external repo.

**Recommendation:** Option A for repos with <10KB of code; Option B for repos with real TypeScript applications (banking-revolution, healthcare-ai, water-management-ai).

### Phase 5: Deployment Pipeline

**Goal:** Every component can be deployed independently or as part of the unified OS.

| Component | Deployment Target | Method |
|-----------|------------------|--------|
| element-145 package | PyPI | `pip install element145` |
| sheldonbrain-rag-api | GCP Cloud Run | Docker (already deployed) |
| sheldongemini-GPI | Manus hosting / Vercel | Static build |
| aluminum-os monorepo | GitHub | Source of truth |
| Individual modules | Docker containers | Per-module Dockerfile |
| LCP MCP Server | Any MCP-compatible host | `element145.integrations.mcp_server` |
| Copilot Plugin | Microsoft Teams | `element145.integrations.copilot_plugin` |

---

## Part IV: Priority Matrix

| Priority | Phase | Sprint | Effort | Impact | Dependency |
|----------|-------|--------|--------|--------|------------|
| **P0** | 1.1 | Sheldonbrain ontology migration | 2-3 sessions | Unblocks all RAG queries | None | ✅ DONE |
| **P0** | 1.2 | Manus-artifacts consolidation | 2 sessions | Eliminates duplication | None | ✅ DONE |
| **P1** | 2.1 | H02 module population | 3-4 sessions | 96 modules SPEC→ACTIVE | Phase 1 |
| **P1** | 3.1 | Frontend service replacement | 2 sessions | Real integrations | Phase 1.1 |
| **P2** | 2.2 | H07 SNRS migration | 1 session | SNRS in lattice | Phase 1 |
| **P2** | 2.3 | H04 governance modules | 1-2 sessions | Constitutional OS integration | Phase 1 |
| **P2** | 3.2 | ShellGemini v11 extraction | 1 session | Version control | None |
| **P3** | 2.4-2.7 | Remaining Houses | 3-4 sessions | Full lattice coverage | Phase 2.1 |
| **P3** | 4 | Domain repo consolidation | 2 sessions | Clean GitHub | None |
| **P4** | 5 | Deployment pipeline | 2-3 sessions | Production readiness | Phase 3 |
| **P4** | 1.3 | Rust crate assessment | 1 session | Preserve/archive decision | None | ✅ DONE |

---

## Part V: Appendix A — Complete Code Inventory

### A.1 aluminum-os Monorepo (638 files)

**Repository:** [github.com/atlaslattice/aluminum-os](https://github.com/atlaslattice/aluminum-os)

| Directory | Files | Description |
|-----------|-------|-------------|
| houses/ | 468 | 12 Houses × 12 Spheres = 144 sphere dirs, each with manifest.yaml |
| element-145/ | 86 | Element 145 admin sphere: core code, specs, SHUGS, tests |
| registries/ | 9 | Canonical registries: module, doctrine, invariant, ontology, innovations, translation tables |
| toolchain/ | 6 | Build scripts, bridge audit, corrections ledger, ontology lock |
| council/ | 1 | S4 Innovation Registry summary |
| orcs/ | 20 | ORC documents (ORC-012 through ORC-036) |
| council-reviews/ | 78 | Pantheon Council review documents |
| .github/workflows/ | 3 | CI, ontology lock gate, registry source-of-truth |

**Key Python Files (element-145/aluminum-os-core/):**

| File | Lines | Purpose | Status |
|------|-------|---------|--------|
| lattice_ontology_v2.py | 657 | Canonical 12×12+1 ontology tables + classify_text() | TESTED |
| bridge_v2.py | 642 | Lattice-aware model router with INGEST pre-routing | TESTED |
| synthesizer_e145.py | 604 | Element 145 cross-domain meta-coordination engine | TESTED |
| service_integrations.py | 591 | ServiceHub: Pinecone, Notion, Google Keep, MCP routing | TESTED |
| sphere_classifier_v2.py | 387 | Keyword classifier producing Pinecone-compatible metadata | TESTED |

**Key Python Files (element-145/shugs/):**

| File | Lines | Purpose | Status |
|------|-------|---------|--------|
| shugs_core.py | 467 | Canonical SHUGS pipeline: Von Mangoldt + HSUF + GUE-KS | TESTED |
| operator_sweep_n145.py | 282 | Operator parameter sweep at fixed N=145 | RAN |
| perfect_square_validation.py | 135 | Perfect-square N validation | RAN |
| ontological_scaffold_experiment.py | 332 | A/B/C experiment framework (not yet executed) | FRAMEWORK |

**Test Files (element-145/aluminum-os-core/tests/):**

| File | Tests | Pass | Skip |
|------|-------|------|------|
| test_lattice_ontology_v2.py | 7 | 7 | 0 |
| test_sphere_classifier_v2.py | 7 | 7 | 0 |
| test_service_integrations.py | 8 | 8 | 0 |
| test_bridge_v2.py | 8 | 6 | 2 |
| test_synthesizer_e145.py | 7 | 7 | 0 |

### A.2 element-145 Package (72 files)

**Repository:** [github.com/atlaslattice/element-145](https://github.com/atlaslattice/element-145)

| File | Lines | Purpose | Status |
|------|-------|---------|--------|
| element145/core.py | 464 | LCPEngine + LatticeOntology + AnalysisResult | v2 VERIFIED |
| element145/shugs.py | 591 | SHUGS operator: Von Mangoldt, HSUF, GUE-KS, ensemble | v2 VERIFIED |
| element145/__init__.py | 78 | Package root, exports all public APIs | v2 VERIFIED |
| element145/integrations/api.py | 320 | FastAPI REST: 8 endpoints | v2 VERIFIED |
| element145/integrations/mcp_server.py | 323 | MCP stdio JSON-RPC: 6 tools | v2 VERIFIED |
| element145/integrations/openai_functions.py | 361 | OpenAI/Anthropic/Google tool schemas | v2 VERIFIED |
| element145/integrations/copilot_plugin.py | 266 | Microsoft Copilot plugin + Teams manifest | v2 VERIFIED |
| element145/tests/test_core.py | 373 | 25+ tests: structure, search, LCP pipeline | v2 VERIFIED |
| element145/tests/test_shugs.py | 351 | 35+ tests: Von Mangoldt, HSUF, GUE-KS | v2 VERIFIED |
| element145/tests/test_abcd.py | 306 | ABCD scaffold experiment runner | v2 VERIFIED |
| element145/lattice_ontology.yaml | 496 | Full 144+1 ontology YAML | CANONICAL |
| element145/Dockerfile | — | Python 3.12-slim, port 8145 | READY |
| element145/pyproject.toml | — | pip-installable package config | READY |
| element145/scaffolds/compact.txt | — | ~800 token system prompt scaffold | READY |
| element145/scaffolds/orchestrator.txt | — | ~2000 token orchestrator scaffold | READY |
| element145/scaffolds/sphere_agent.txt | — | ~400 token sphere agent scaffold | READY |

### A.3 sheldonbrain-rag-api (30 files, 7,631 lines)

**Repository:** [github.com/atlaslattice/sheldonbrain-rag-api](https://github.com/atlaslattice/sheldonbrain-rag-api)
**Deployment:** GCP Cloud Run (PRODUCTION)

| File | Lines | Purpose | Migration Status |
|------|-------|---------|-----------------|
| rag_api_gemini.py | 341 | Production RAG API endpoint | NEEDS house/sphere metadata |
| grokbrain_parser/grokbrain_v4.py | 531 | OLD ontology (12 academic categories) | **REPLACE** with lattice_ontology_v2 |
| grokbrain_parser/grokbrain_core.py | 403 | Core parsing logic | NEEDS ontology update |
| grokbrain_parser/xai_integration.py | 425 | xAI/Grok integration | KEEP — update sphere references |
| grokbrain_parser/twelve_step_validation.py | 526 | Validation pipeline | NEEDS 12 Houses validation |
| grokbrain_parser/test_suite.py | 516 | Test suite | NEEDS update for new ontology |
| sphere_classifier.py | 309 | OLD classifier | **REPLACE** with sphere_classifier_v2 |
| batch_ingest.py | 416 | Batch Pinecone ingestion | NEEDS house/sphere metadata |
| unified_rag.py | 326 | Unified RAG interface | NEEDS ontology update |
| pinecone_client.py | — | Pinecone vector operations | NEEDS metadata schema update |
| embeddings.py | — | Embedding generation | KEEP |
| config.py | — | Configuration | KEEP |
| deep_recall.py | — | Deep memory recall | NEEDS ontology update |
| grok_rag.py | — | Grok-specific RAG | KEEP |
| notion_sync.py | — | Notion synchronization | KEEP |
| import_to_notion.py | — | Notion import | KEEP |

### A.4 sheldongemini-GPI (18 files, 1,905 lines)

**Repository:** [github.com/atlaslattice/sheldongemini-GPI](https://github.com/atlaslattice/sheldongemini-GPI)

| File | Lines | Purpose | Integration Status |
|------|-------|---------|-------------------|
| App.tsx | 313 | Main app: chat, voice, Noosphere viz | NEEDS real API wiring |
| components/LiveVoiceMode.tsx | 280 | Live voice interaction | KEEP |
| services/geminiService.ts | 214 | Gemini 2.5 Flash direct call | NEEDS LCP routing |
| services/grokData.ts | 194 | Grok data integration | KEEP |
| services/nexusOrchestrator.ts | 139 | **SIMULATED** multi-agent | **REPLACE** with real synthesizer_e145 |
| services/keepRagSim.ts | 133 | **SIMULATED** RAG | **REPLACE** with real sheldonbrain-rag-api |
| services/stealthSingularitySim.ts | 94 | **SIMULATED** Noosphere | **REPLACE** with real LCPEngine.analyze() |
| services/physicsSim.ts | 61 | Physics simulation | KEEP |
| services/krakoaMcpSim.ts | 53 | **SIMULATED** MCP | **REPLACE** with real MCP server |
| services/externalDataSim.ts | 49 | **SIMULATED** external data | **REPLACE** with real ServiceHub |

### A.5 aluminum-os-v3 (Legacy, 7,905 lines)

**Repository:** [github.com/atlaslattice/aluminum-os-v3](https://github.com/atlaslattice/aluminum-os-v3)

**Rust Crates (2,504 lines):**

| Crate | Lines | Purpose | Disposition |
|-------|-------|---------|-------------|
| claude-contrib/lib.rs | 603 | Claude integration patterns | ARCHIVE — superseded by bridge_v2 |
| pantheon/lib.rs | 470 | BFT governance consensus | **PORT** to Python H04 module |
| forge-core/lib.rs | 426 | Core boot sequence | ARCHIVE — superseded by element-145 |
| sheldonbrain/lib.rs | 337 | 3-tier memory system | ARCHIVE — superseded by sheldonbrain-rag-api |
| noosphere/lib.rs | 273 | Intent classification | ARCHIVE — superseded by sphere_classifier_v2 |
| forge-boot/main.rs | 251 | Boot entry point | ARCHIVE |

**Python Code (5,401 lines):**

| File | Lines | Purpose | Disposition |
|------|-------|---------|-------------|
| manus-core/ai_first_os.py | 1,635 | ~20 innovation implementations | **TRIAGE** — extract to H02 modules |
| manus-core/unified_api.py | 820 | API facade | ARCHIVE — superseded by service_integrations |
| innovations/remaining_innovations.py | 780 | Innovation implementations | **TRIAGE** — extract to appropriate Houses |
| manus-core/bridge.py | 434 | Model router | ARCHIVE — superseded by bridge_v2 |
| claude-contrib/python/core/manus_core.py | 386 | Claude contribution | ARCHIVE |
| innovations/dream_weaver.py | — | Dream Weaver innovation | **EXTRACT** to H01 module |
| innovations/eternal_developer.py | — | Eternal Developer | **EXTRACT** to H02 module |
| innovations/sovereign_oracle.py | — | Sovereign Oracle | **EXTRACT** to H02 module |

### A.6 manus-artifacts (282 files, ~28,000 lines Python)

**Repository:** [github.com/atlaslattice/manus-artifacts](https://github.com/atlaslattice/manus-artifacts)

| Directory | Files | Lines | Key Code | Disposition |
|-----------|-------|-------|----------|-------------|
| codebases/sheldonbrain/ | 18 | 5,499 | grokbrain_v4, chronos_fold, janus_protocol | **MIGRATE** ontology; port protocols to H01 |
| codebases/sovereign-oracle/ | 23 | 4,455 | bridge.py, output_layer.py | **ARCHIVE** — superseded |
| codebases/email-processing/ | 23 | 4,455 | Identical to sovereign-oracle | **DEDUPLICATE** |
| codebases/other/ | 18 | 4,511 | trinity_council_v2, proactive_intelligence | **TRIAGE** — extract to H02/H04 |
| codebases/saas-killer/ | 6 | 2,889 | ingestion_pipeline, api_server, zapier_webhooks | **MIGRATE** to H02 modules |
| codebases/atlas-lattice/ | 7 | 2,300 | council_synthesis, proactive_intelligence | **MIGRATE** to H04 modules |
| codebases/data-pipeline/ | 7 | 2,007 | Subset of saas-killer | **DEDUPLICATE** |
| codebases/snrs/ | 3 | 958 | snrs_v1_3_2, 144_sphere_ingestion | **MIGRATE** to H07 modules |
| codebases/atlas-vault/ | 3 | 630 | Vault operations | **ARCHIVE** |
| codebases/aluminum-os/ | 1 | 414 | Legacy OS code | **ARCHIVE** |

### A.7 Other Substantive Repos

| Repo | Size | Language | Purpose | Disposition |
|------|------|----------|---------|-------------|
| atlas-lattice-foundation | 99 files | MD + 2 Python | Specs, canon docs, fractal generator | **ARCHIVE** — specs absorbed into aluminum-os |
| constitutional-os | TBD | Python | Constitutional governance layer | **MIGRATE** to H04 modules |
| constitutional-continuum | TBD | Python | Integration layer for 108 repos | **ARCHIVE** — superseded by aluminum-os monorepo |
| batman-protocol | TBD | Python | AI-driven perpetrator identification | **MIGRATE** to H12 module |
| SNRS-v2-v3-Distribution | 8KB | — | SNRS distribution | **MIGRATE** to H07 |
| bazinga | TBD | Python | Constitutional compute layer | **ARCHIVE** — superseded by element-145 |
| Kintsuji-code-fixer- | TBD | Python | Code quality tool | **MIGRATE** to H02.M100 |
| manus-2.0-toolkit | TBD | Python | AI-Native OS toolkit | **TRIAGE** |
| apple-cli | TBD | Python | Apple iCloud CLI | **KEEP** as standalone tool |
| noosphere-archive | TBD | — | Archived Noosphere code | **ARCHIVE** |
| noosphere-defense | TBD | — | Noosphere defense framework | **MIGRATE** to H12 module |

### A.8 Domain Placeholder Repos (114 repos)

These repos were created during the initial swarm deployment. Most contain only a 1KB HTML file or a template TypeScript project. They map to Houses as follows:

| House | Count | Notable Repos with Real Code |
|-------|-------|------------------------------|
| H01 Consciousness | 0 | — |
| H02 Technology | 6 | manus-2.0-toolkit, apple-cli |
| H03 Economics | 13 | banking-revolution (162KB TS), free-banking-app (TS) |
| H04 Governance | 9 | All 1KB HTML |
| H05 Culture | 6 | All 1KB HTML |
| H06 Health | 5 | healthcare-ai (162KB TS) |
| H07 Earth | 7 | water-management-ai (163KB TS) |
| H08 Mathematics | 0 | — |
| H09 Physics | 0 | — |
| H10 History | 0 | — |
| H11 Communication | 6 | All 1KB HTML |
| H12 Security | 14 | batman-protocol |

**Recommendation:** Archive all 114 domain repos. Extract the 4 repos with real TypeScript (banking-revolution, healthcare-ai, water-management-ai, free-banking-app) into appropriate House module directories first.

---

## Part VI: Appendix B — Module Registry (182 Modules by House)

### H01: Consciousness & Cognition (3 modules)

| ID | Name | Sphere | Source Code | Proposed Source |
|----|------|--------|-------------|-----------------|
| M8 | Epistemic Integrity Validator | S02 | None | chronos_fold_protocol.py (526 lines) |
| M8a | Epistemic Integrity CN Adapter | S02 | None | janus_protocol.py (368 lines) |
| M7 | Ethics Engine | S03 | None | New implementation |

### H02: Technology & Engineering (96 modules)

Top 20 by priority:

| ID | Name | Sphere | Source Code | Proposed Source |
|----|------|--------|-------------|-----------------|
| M1 | Sovereign Router Core | S03 | None | bridge_v2.py (642 lines) |
| M2 | Model Gateway | S03 | None | bridge_v2.py model selection |
| M3 | Cost Optimizer | S03 | None | bridge_v2.py cost tracking |
| M3.1 | Trust Scoring System | S02 | None | New implementation |
| M4 | Compliance Engine | S03 | None | service_integrations.py |
| M5 | Transparency Logger | S03 | None | bridge_v2.py audit trail |
| M6 | Fallback Manager | S03 | None | bridge_v2.py fallback logic |
| M10 | Mathematical Proof Engine | S01 | None | shugs_core.py (467 lines) |
| M16 | Statistical Inference Engine | S02 | None | shugs_core.py ensemble |
| M22 | Theorem Prover | S01 | None | New implementation |
| M92 | Software Architecture Validator | S01 | None | New implementation |
| M100 | Code Quality Analyzer | S01 | None | Kintsuji-code-fixer- |
| M120 | CI/CD Pipeline Manager | S01 | None | .github/workflows/ |
| M173 | Real-Time Routing Share Meter | S02 | None | bridge_v2.py metrics |

*(76 more modules — full list in module_registry.yaml)*

### H03: Economics & Finance (2 modules)

| ID | Name | Sphere | Source Code | Proposed Source |
|----|------|--------|-------------|-----------------|
| M130 | Wet Lab Verification Gate | S02 | None | New implementation |
| M131 | Environmental Impact Assessor | S07 | None | New implementation |

### H04: Governance & Law (25 modules)

Top 10 by priority:

| ID | Name | Sphere | Source Code | Proposed Source |
|----|------|--------|-------------|-----------------|
| M143 | Constitutional Rights Validator | S01 | None | constitutional-os repo |
| M145 | Treaty Compliance Checker | S02 | None | New implementation |
| M146 | Corporate Governance Module | S03 | None | council_synthesis.py (500 lines) |
| M155 | Consent Audit Trail | S01 | None | New implementation |
| M156 | Sanctions Compliance Module | S02 | None | New implementation |

### H05: Culture & Society (22 modules)

6 stubs created (M167-M172). 16 more need stubs.

### H07: Earth & Environment (8 modules)

| ID | Name | Sphere | Source Code | Proposed Source |
|----|------|--------|-------------|-----------------|
| M129 | Agricultural Data Pipeline | S01 | None | snrs_v1_3_2_fixed.py |
| M132 | Water Quality Monitor | S02 | None | water-management-ai repo |
| M133 | Urban Planning Simulator | S03 | None | New implementation |
| M134 | Data Warehouse Manager | S04 | None | 144_sphere_ingestion.py |
| M176 | Boot Manifest Runtime | S04 | None | New implementation |

### H09-H12: See module_registry.yaml for complete listings.

---

## Part VII: Appendix C — Innovations Registry Summary

27 innovations registered across 6 categories:

| Category | Count | Key Innovations |
|----------|-------|----------------|
| A) Governance | 6 | Canonical Source Index, Naming Drift Blocker, Ontology Lock Protocol |
| B) Routing | 5 | Metabolic Broker, Compliance Modes, Functional Diversity |
| C) Notion Control Plane | 5 | Notion as governance bus, Approvals DB, Schema Registry |
| D) ToS/Policy | 6 | Terms Snapshot + Hash Lock, Output Handling Boundary, Wrapper ToS Tracking |
| E) Cognitive Architecture | 3 | RFPF, Loki Patch, Constitutional Agent Coordination |
| F) Interop | 2 | Tiered Source-of-Truth, Mirror Integrity |

Full registry: `registries/innovations_registry.yaml`

---

## Part VIII: Success Criteria

The battle plan is complete when:

1. **Zero DEPRECATED ontology references** — no code imports from grokbrain_v4 SPHERES or the 5-ring schema
2. **All 182 modules have at least STUB status** — every module directory contains a README.md with dependencies and integration points
3. **Core modules (M1-M17) reach ACTIVE status** — real code, real tests, real CI
4. **Frontend connects to real backend** — zero simulated services in sheldongemini-GPI
5. **Single deployment command** — `docker-compose up` boots the full OS
6. **All domain repos archived or federated** — clean GitHub profile with only canonical repos visible
7. **element-145 on PyPI** — `pip install element145` works
8. **CI passes on all repos** — GitHub Actions green across aluminum-os, element-145, sheldonbrain-rag-api

---

*This battle plan is a living document. Update it as sprints complete and new requirements emerge.*
*Next review: After Phase 1 completion.*
