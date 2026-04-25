# Aluminum Universal Workspace OS — Complete System Specification v1.0

**Document ID:** AUWS-SPEC-001  
**Date:** April 24, 2026  
**Author:** Manus (Infrastructure & Build Seat)  
**Classification:** Canonical architecture specification — maps all atlaslattice codebases to a unified AI-native operating system  
**Inputs:** 50-repo deep audit, ai-native-os-architect skill framework, GitHub AI ground-truth corrections, Notion AI governance framework, 84-item Build Gate Register v2.2, constitutional-os 37-invariant spec

---

## Repository Vault Note

This file is vaulted in `atlaslattice/aluminum-os` as the implementation-facing canonical system assembly manual for Aluminum Universal Workspace OS.

The original uploaded document should also be mirrored or referenced from `open-regenerative-compute-standard` as the standards-side canonical artifact if desired.

---

## 1. Executive Summary

The Aluminum Universal Workspace OS (Aluminum UWS) is an AI-native operating system layer that treats a multi-model AI Council as its kernel and builds a persistent, cross-platform computing environment on top of existing host operating systems. It does not replace Windows, macOS, ChromeOS, iOS, or Android. It **transcends** them — making the underlying platform an implementation detail while the user interacts with a constitutionally governed, context-aware, device-spanning workspace.

This specification maps every codebase in the `atlaslattice` GitHub organization (50 repositories, 7 private, 43 public) to a specific OS layer, classifies each repository's usefulness to the unified build, and produces a phased integration plan. The document synthesizes three frameworks: the **ai-native-os-architect** skill (which provides the strategic architecture), the **constitutional-os** invariant set (which provides the governance substrate), and the **ORC-012 TDD v0.2** with its 84-item Build Gate Register (which provides the execution control system).

> **The core thesis:** Your 50 repositories are not 50 separate projects. They are the scattered components of an operating system that has never been assembled. This document is the assembly manual.

---

## 2. Architectural Framework: The Seven-Layer OS Model

The ai-native-os-architect skill defines four principles: AI as Kernel, Stateless UI Layer, Redundant State Vaulting, and Political Neutrality. The constitutional-os repo defines five architectural layers (L1 Constitutional through L5 Extension). This specification merges both into a unified seven-layer model that maps directly to existing codebases.

```text
┌─────────────────────────────────────────────────────────────────────┐
│  L7 — DEVICE MESH LAYER                                            │
│  Cross-platform persistence, device handoff, hardware abstraction   │
│  Repos: apple-cli, aluminum-gemini-cli, constitutional-continuum    │
├─────────────────────────────────────────────────────────────────────┤
│  L6 — APPLICATION LAYER                                             │
│  User-facing agents, dashboards, domain-specific tools              │
│  Repos: sheldongemini-GPI, tucker-gemini-GPT-, deer-flow            │
├─────────────────────────────────────────────────────────────────────┤
│  L5 — EXTENSION & PLUGIN LAYER                                      │
│  MCP servers, Claude plugins, agent skills, integrations            │
│  Repos: claude-code-*, awesome-claude-*, servers, Kintsuji          │
├─────────────────────────────────────────────────────────────────────┤
│  L4 — SERVICE ORCHESTRATION LAYER                                   │
│  Element 145 routing, multi-model dispatch, budget enforcement      │
│  Repos: element-145 (to be created or implemented under aluminum-os/services/), manus-2.0-toolkit │
├─────────────────────────────────────────────────────────────────────┤
│  L3 — ENGINE LAYER                                                  │
│  Constitutional Router, Janus v2 Protocol, multi-agent dispatch     │
│  Repos: uws (constitutional_engine.rs, council_github_client)       │
├─────────────────────────────────────────────────────────────────────┤
│  L2 — KERNEL LAYER                                                  │
│  ConsentKernel, GoldenTrace audit, state management, 144-sphere     │
│  Repos: constitutional-os (spec), aluminum-os-v3 (Python impl)      │
├─────────────────────────────────────────────────────────────────────┤
│  L1 — CONSTITUTIONAL LAYER                                          │
│  37 invariants, sovereignty enforcement, ORCS governance            │
│  Repos: constitutional-os, open-regenerative-compute-standard       │
└─────────────────────────────────────────────────────────────────────┘

CROSS-CUTTING CONCERNS:
  Provenance Ledger    → aluminum-os / Royalty Runtime append-only ledger
  Observability        → manus-2.0-toolkit cost logs, learning logs
  State Vaulting       → Notion + Google Drive + GitHub triple-vault
  Knowledge Base       → atlas-lattice-foundation
```

---

## 3. Integrated Implementation Hierarchy

This document resolves the current repo question as follows:

```text
open-regenerative-compute-standard
  = standards, ORCS, canonical AUWS specs, council reviews

aluminum-os
  = implementation umbrella, strategy, architecture docs, services, packages

uws
  = operational CLI command surface and provider dispatch

aluminum-os/services/element-145
  = L4 service orchestration runtime scaffold
```

Element 145 may later become its own repository if and only if it becomes an independently versioned/deployed product. For Phase 0, keeping it under `aluminum-os/services/element-145/` preserves architectural cohesion.

---

## 4. AI-Native Kernel: Council as OS Core

Traditional operating systems have a monolithic or microkernel written in C or Rust. Aluminum UWS has a **multi-model AI Council** as its kernel. The Council performs functions analogous to process scheduling, memory management, file systems, device drivers, security, IPC, audit logging, shell rendering, power management, and package management through structured API calls and governance rules.

Key mappings:

| Traditional OS Function | Aluminum UWS Equivalent | Implementation Source |
|---|---|---|
| Process scheduling | Query routing + model dispatch | Element 145 / `manus-2.0-toolkit/core/model_router.py` |
| Memory management | Context compression + session state | `manus-2.0-toolkit/core/context_compress.py` |
| File system | Triple-vault: GitHub + Notion + Drive | `session_vault.py` pattern |
| Device drivers | Provider adapters + MCP | `uws`, MCP servers |
| Security/access | Constitutional invariants + Permission Surface | `constitutional-os` |
| IPC | Janus v2 + A2A | `uws/src/` |
| Audit/logging | GoldenTrace + Provenance Ledger | `aluminum-os` |
| User interface shell | Stateless UI rendered by kernel state | continuum/adapter patterns |

---

## 5. Current Essential Build Surface

The complete spec classifies the build surface as:

| Grade | Count | Repos |
|---|---:|---|
| ESSENTIAL | 7 | `constitutional-os`, `open-regenerative-compute-standard`, `aluminum-os-v3`, `manus-2.0-toolkit`, `uws`, `aluminum-os`, `element-145` target |
| VALUABLE | 11 | `atlas-lattice-foundation`, `claude-code`, `claude-code-mcp`, `servers`, `claude-code-plugins-plus-skills`, `Kintsuji-code-fixer-`, `constitutional-continuum`, `apple-cli`, `aluminum-gemini-cli`, `manus-artifacts`, `sheldongemini-GPI` |
| REFERENCE | 17 | curated Claude/plugin refs, forks, workflow frameworks, libraries |
| PERIPHERAL | 5 | experimental/user-facing/special-domain repos |
| INERT | 10 | financial/DeFi stubs and placeholders |

The active build surface is therefore:

```text
7 ESSENTIAL + 11 VALUABLE = 18 repos that matter now
```

---

## 6. Key Architectural Decisions To Carry Forward

### 6.1 Provider neutrality

Aluminum UWS must remain parent-company agnostic. Google, Microsoft, Apple, GitHub, Notion, OpenAI, Anthropic, xAI, DeepSeek, and future systems are providers, council seats, vaults, or integrations — not owners of the substrate.

### 6.2 INV-7 provider cap

No single AI provider may exceed 47% of decision-making authority. This is enforced at L3 by the Constitutional Router and recorded in TransparencyPackets.

### 6.3 Triple-vault filesystem

| Vault | Role |
|---|---|
| GitHub | code, specs, audit trail, version history |
| Notion | governance docs, session logs, structured dashboards |
| Google Drive | binary assets, large files, shared docs |
| Local | offline continuity and user sovereignty |

Every data type must have a single canonical source and explicit sync targets.

### 6.4 144-sphere ontology as OS namespace

The 144-sphere ontology functions like a filesystem namespace. Queries, artifacts, routing decisions, and memory objects should eventually attach House/Sphere metadata.

### 6.5 TransparencyPacket as receipt

Every meaningful routing/execution decision emits a structured TransparencyPacket containing routing, governance, provenance, model weighting, cost, and audit data.

### 6.6 Element 145 as init/service orchestration layer

Element 145 is the L4 init process / service orchestration layer. It bootstraps and coordinates the kernel, engine, extension layer, budget enforcement, classifier, and provenance systems.

---

## 7. Build Sequence Summary

### Phase 0 — Constitutional Build Gate

Critical outputs:

- atlaslattice cleanup;
- Element 145 scaffold under `aluminum-os/services/element-145/` or standalone repo later;
- dependency/secret inventory;
- canonical source decision table;
- MCP Permission Surface Matrix;
- Destructive Action Policy;
- Constitutional Build Gate review;
- Council sign-off.

### Phase 1 — Kernel + Engine

- SphereQuery + RoutingDecision models;
- two-pass classifier;
- routing YAML for 12 Houses;
- LiteLLM integration with at least 3 providers;
- TransparencyPacket v0.2;
- budget enforcement;
- JSONL provenance ledger;
- structural confabulation detection.

### Phase 1.5 — Validation

- 10-case test matrix;
- 48-hour shadow mode;
- five simulation scenarios;
- audit export;
- Day 14 success gate.

### Phase 2 — Extension Layer

- MCP server integration;
- skill extraction pipeline;
- Eastern Review integration;
- 144-sphere progressive rollout.

### Phase 3 — Device Mesh

- cross-platform state sync;
- Apple device integration;
- Google device integration;
- wearable context.

### Phase 4+ — Hardware and Scale

- Chromebox/Scrap deployment;
- Rust hot-path migration;
- full 144-sphere deployment;
- A2A protocol integration.

---

## 8. Day 14 Success Gate

Phase 1 is successful when:

- routing works end-to-end;
- every routing decision emits a valid TransparencyPacket;
- budget enforcement is active;
- provenance ledger records immutable decisions;
- confabulation detection is running;
- p50 classification + routing latency is under 2 seconds excluding model response time;
- 10-case test matrix passes;
- at least 3 providers are connected;
- Eastern Review flags exist for 12 Houses;
- no destructive actions occur without approval;
- no INV-7 violation occurs;
- audit export works;
- shadow mode validates for 48 hours with at least 90% expected routing alignment;
- 5 simulation scenarios complete;
- Build Gate Register items are resolved.

---

## 9. Glossary

| Aluminum UWS Term | Traditional OS Equivalent | Definition |
|---|---|---|
| ConsentKernel | Kernel | Validates operations against constitutional invariants |
| 144-Sphere Ontology | Filesystem namespace | 12×12 classification matrix |
| TransparencyPacket | System call return receipt | Structured receipt for routing decisions |
| GoldenTrace | Audit log | Append-only hash-chained decision record |
| Provenance Ledger | Transaction log | Immutable operation record |
| Royalty Runtime | Attribution system | Execution-layer attribution and lineage tracking |
| Constitutional Router | Process scheduler | Routes queries while enforcing invariants |
| Janus v2 Protocol | IPC mechanism | Multi-agent communication protocol |
| Triple-Vault | Distributed filesystem | GitHub + Notion + Drive + local stores |
| Device Mesh | Network stack | Cross-platform state sync |
| Build Gate Register | Release checklist | Execution control document |
| House 12 | `/boot/` | Governance domain |
| INV-7 | Anti-monopoly enforcement | No provider exceeds 47% routing authority |
| Element 145 | init process | L4 service orchestration layer |

---

## 10. Action Items Derived From This Spec

1. Link this spec from `docs/architecture/SOURCE_OF_TRUTH.md`.
2. Mirror or reference this spec in `open-regenerative-compute-standard`.
3. Place the uploaded Element 145 scaffold under `services/element-145/` in `aluminum-os`.
4. Create `docs/architecture/element-145-runtime-map.md` mapping scaffold modules to AUWS layers.
5. Create `docs/architecture/identity-sidecar.md` as next Phase 0 contract.
6. Continue `uws` provider-dispatch and GoldenTrace/swarm-review respawns in parallel.

---

## 11. Status

**Status:** Candidate canonical, implementation-facing.  
**Next step:** Integrate with `SOURCE_OF_TRUTH.md`, vault Element 145 scaffold, then run correctness/security review before Phase 1 implementation.

