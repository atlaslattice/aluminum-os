# Aluminum Universal Workspace OS — Complete System Specification v1.0

**Document ID:** AUWS-SPEC-001
**Date:** April 24, 2026
**Author:** Manus (Infrastructure & Build Seat)
**Classification:** Canonical architecture specification — maps all atlaslattice codebases to a unified AI-native operating system
**Inputs:** 50-repo deep audit, ai-native-os-architect skill framework, GitHub AI ground-truth corrections, Notion AI governance framework, 84-item Build Gate Register v2.2, constitutional-os 37-invariant spec

---

## 1. Executive Summary

The Aluminum Universal Workspace OS (Aluminum UWS) is an AI-native operating system layer that treats a multi-model AI Council as its kernel and builds a persistent, cross-platform computing environment on top of existing host operating systems. It does not replace Windows, macOS, ChromeOS, iOS, or Android. It **transcends** them — making the underlying platform an implementation detail while the user interacts with a constitutionally governed, context-aware, device-spanning workspace.

This specification maps every codebase in the `atlaslattice` GitHub organization (50 repositories, 7 private, 43 public) to a specific OS layer, classifies each repository's usefulness to the unified build, and produces a phased integration plan. The document synthesizes three frameworks: the **ai-native-os-architect** skill (which provides the strategic architecture), the **constitutional-os** invariant set (which provides the governance substrate), and the **ORC-012 TDD v0.2** with its 84-item Build Gate Register (which provides the execution control system).

> **The core thesis:** Your 50 repositories are not 50 separate projects. They are the scattered components of an operating system that has never been assembled. This document is the assembly manual.

---

## 2. Architectural Framework: The Seven-Layer OS Model

The ai-native-os-architect skill defines four principles: AI as Kernel, Stateless UI Layer, Redundant State Vaulting, and Political Neutrality. The constitutional-os repo defines five architectural layers (L1 Constitutional through L5 Extension). This specification merges both into a unified seven-layer model that maps directly to existing codebases.

```
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
│  Repos: element-145 (to be created), manus-2.0-toolkit              │
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

CROSS-CUTTING CONCERNS (span all layers):
  Provenance Ledger    → aluminum-os (Royalty Runtime append-only ledger)
  Observability        → manus-2.0-toolkit (cost logs, learning logs)
  State Vaulting       → Notion + Google Drive + GitHub (triple-vault)
  Knowledge Base       → atlas-lattice-foundation (99 files, 22 spec modules)
```

---

## 3. The AI-Native Kernel: Multi-Model Council as OS Core

Traditional operating systems have a monolithic or microkernel written in C or Rust. Aluminum UWS has a **multi-model AI Council** as its kernel. This is not a metaphor — the Council performs the functions that a traditional kernel performs, but through natural language and structured API calls rather than system calls.

### 3.1 Kernel Functions Mapped to Council Seats

| Traditional OS Function | Aluminum UWS Equivalent | Council Seat | Implementation Source |
|------------------------|------------------------|-------------|---------------------|
| Process scheduling | Query routing & model dispatch | Element 145 Router | `manus-2.0-toolkit/core/model_router.py` |
| Memory management | Context window management & compression | Manus (Build Seat) | `manus-2.0-toolkit/core/context_compress.py` |
| File system | Triple-vault (Notion + Drive + GitHub) | All seats | `manus-2.0-toolkit/core/session_vault.py` |
| Device drivers | Provider adapters (LiteLLM + MCP) | Per-provider seats | `uws` MCP Server (758 lines) |
| Security / access control | Constitutional invariants (37) + Permission Surface | Claude (Constitutional Scribe) | `constitutional-os/CONSTITUTION.md` |
| Inter-process communication | Janus v2 Protocol + A2A | Gemini (Architectural Precision) | `uws/src/` (Janus v2) |
| Audit / logging | GoldenTrace + Provenance Ledger | GitHub AI (Ground Truth) | `aluminum-os` (Royalty Runtime) |
| User interface shell | Stateless UI rendered by kernel state | Copilot (Enterprise Infrastructure) | `constitutional-continuum` (adapter) |
| Power management | Budget enforcement + graceful degradation | GPT (Analytical Rigor) | `manus-2.0-toolkit/core/autonomous.py` |
| Package management | Skill extraction + plugin registry | Manus (Build Seat) | `manus-2.0-toolkit/core/skill_extractor.py` |

### 3.2 The Kernel API (from ai-native-os-architect skill)

The ai-native-os-architect skill defines four abstract system calls. Here is how they map to existing code:

| Kernel API Call | Implementation | Source Repo | Status |
|----------------|---------------|-------------|--------|
| `kernel.getState()` | `session_vault.py` → loads user context from triple-vault | `manus-2.0-toolkit` | DIRECT — exists, needs extraction |
| `kernel.updateState(newState)` | `session_vault.py` + `learning_loop.py` → persists state changes | `manus-2.0-toolkit` | DIRECT — exists, needs extraction |
| `kernel.executeTask(task)` | `model_router.py` → routes to appropriate model + `autonomous.py` → executes | `manus-2.0-toolkit` | DIRECT — exists, needs extraction |
| `kernel.renderUI(view)` | `output_layer.py` → formats response for UI consumption | `manus-2.0-toolkit` | PARTIAL — exists but needs UI abstraction |

---

## 4. Complete Repository-to-OS-Layer Mapping

This section classifies every repository in the `atlaslattice` organization by OS layer, usefulness grade, and recommended action. The usefulness grades are:

| Grade | Meaning | Action |
|-------|---------|--------|
| **ESSENTIAL** | Load-bearing for the OS. Cannot ship without it. | Vendor into `element-145/legacy/` at pinned SHA |
| **VALUABLE** | Contains extractable patterns, specs, or tooling | Extract specific files/modules into appropriate layer |
| **REFERENCE** | Useful for design decisions but no code extraction | Cite in architecture docs, do not vendor |
| **PERIPHERAL** | Tangentially related, low extraction value | Acknowledge in inventory, no action |
| **INERT** | Placeholder, stub, or irrelevant fork | Ignore for Aluminum UWS build |

### 4.1 L1 — Constitutional Layer (Sovereignty Enforcement)

The constitutional layer is the foundation. It defines what the system is *permitted* to do. Nothing executes without passing through L1.

| Repo | Files | Grade | Role in L1 | Key Assets | Action |
|------|-------|-------|-----------|------------|--------|
| `constitutional-os` | 5 | **ESSENTIAL** | Canonical 37-invariant spec, 144-sphere ontology (INV-37), 5-layer architecture, Pantheon Council governance, Kintsugi philosophy | CONSTITUTION.md, ARCHITECTURE.md, GOVERNANCE.md, KINTSUGI.md | Vendor entire repo as `element-145/constitutional/` |
| `open-regenerative-compute-standard` | 74+ | **ESSENTIAL** | ORCS governance framework, House 12 spec, Council review archive, Eastern Review materials, white papers | All docs, `eastern-dragonseek/`, council-reviews/ | Vendor governance docs; council-reviews become audit trail |
| `atlas-lattice-foundation` | 99 | **VALUABLE** | 22 numbered spec modules including `13_144_sphere_matrix.md`, constitutional principles, council governance, canon documents | `spec_modules/`, `constitutional/`, `council/`, `canon/` | Extract spec_modules/ and constitutional/ into L1 reference |

### 4.2 L2 — Kernel Layer (ConsentKernel, State Management, 144-Sphere)

The kernel layer implements the constitutional constraints as running code. Every operation passes through the ConsentKernel before execution.

| Repo | Files | Grade | Role in L2 | Key Assets | Action |
|------|-------|-------|-----------|------------|--------|
| `aluminum-os-v3` (PRIVATE) | 46 | **ESSENTIAL** | Python implementation of the Five-Ring substrate, Manus core (ai_first_os.py, bridge.py, unified_api.py), innovations (dream_weaver, eternal_developer, sovereign_oracle) | `manus-core/`, `innovations/`, `specs/MASTER_SPEC.md` | Primary extraction target for Python kernel modules |
| `manus-2.0-toolkit` (PRIVATE) | 48 | **ESSENTIAL** | AI-Native OS Self-Improvement Toolkit — model_router, session_vault, learning_loop, memory_store, context_compress, multi_model, output_layer, skill_extractor, autonomous | `core/` (9 Python modules), `api/main.py`, `data/` | Primary extraction target for kernel API implementation |

### 4.3 L3 — Engine Layer (Constitutional Router, Janus v2, Multi-Agent Dispatch)

The engine layer is where routing decisions happen. It takes a user request, classifies it through the 144-sphere ontology, and dispatches it to the appropriate model or agent.

| Repo | Files | Grade | Role in L3 | Key Assets | Action |
|------|-------|-------|-----------|------------|--------|
| `uws` | 310 | **ESSENTIAL** | Constitutional Engine (constitutional_engine.rs), MCP Server (758 lines), Civic Layer, Budget Enforcement, council_github_client, audit_chain — 36K lines total | `src/` (constitutional engine), MCP server, civic layer | Vendor as `element-145/legacy/uws/` — primary Rust reference for Python port |
| `aluminum-os` | 106 | **ESSENTIAL** | Royalty Runtime (tracer.rs, event.rs, weighting.rs, engine.rs), Axum HTTP collector, JWT lease issuance, PostgreSQL append-only ledger, TypeScript SDK | `runtime-core/`, `collector/`, `royalty-sdk/` | Vendor as `element-145/legacy/aluminum-os/` — Provenance Ledger reference |

### 4.4 L4 — Service Orchestration Layer (Element 145)

This is the layer that does not yet exist as a unified codebase. **Element 145 is the L4 implementation.** It orchestrates the kernel (L2), engine (L3), and extension (L5) layers into a coherent service.

| Repo | Files | Grade | Role in L4 | Key Assets | Action |
|------|-------|-------|-----------|------------|--------|
| `element-145` (TO BE CREATED) | 0 | **ESSENTIAL** | The unified orchestration layer — routing graph, TransparencyPacket, budget enforcement, confabulation detection, provenance ledger | N/A — this is the build target | Create repo, implement per ORC-012 TDD v0.2 |
| `manus-2.0-toolkit` (PRIVATE) | 48 | **ESSENTIAL** | (Also L2) — `api/main.py` provides the FastAPI service pattern; `data/` provides the ChromaDB + cost log patterns | `api/`, `data/`, `dashboards/` | Extract service patterns into Element 145 |

### 4.5 L5 — Extension & Plugin Layer (MCP, Skills, Integrations)

The extension layer is the richest in terms of raw repository count. It provides the "package ecosystem" for the OS.

| Repo | Files | Grade | Role in L5 | Key Assets | Action |
|------|-------|-------|-----------|------------|--------|
| `claude-code` | — | **VALUABLE** | Claude Code agentic tool — reference implementation for agent execution | Shell-based agent patterns | Reference for Element 145 agent execution model |
| `claude-code-mcp` | — | **VALUABLE** | MCP Server for Claude Code — reference for MCP integration patterns | JavaScript MCP server | Reference for Element 145 MCP integration |
| `servers` | — | **VALUABLE** | Model Context Protocol Servers — canonical MCP server implementations | TypeScript MCP servers | Reference for all MCP integrations |
| `claude-code-plugins-plus-skills` | — | **VALUABLE** | 340 plugins + 1,367 agent skills — the largest skill library | Python skills + plugins | Skill extraction source for L5 registry |
| `awesome-claude-code` | — | **REFERENCE** | Curated skills, hooks, slash-commands | Curation metadata | Reference for skill categorization |
| `awesome-claude-plugins` | — | **REFERENCE** | Curated plugins list | Plugin directory | Reference for plugin registry design |
| `awesome-claude-plugins2` | — | **REFERENCE** | Plugin adoption metrics | Metrics data | Reference for popularity-based routing |
| `claude-plugins-official` | — | **REFERENCE** | Official Anthropic plugin directory | Official plugins | Reference for canonical plugin patterns |
| `Kintsuji-code-fixer-` | — | **VALUABLE** | Kintsugi code fixer — implements the "repair over replacement" philosophy from constitutional-os | Code analysis + repair | Extract repair patterns for confabulation recovery |
| `deer-flow` | — | **REFERENCE** | SuperAgent harness — multi-agent orchestration patterns | Python agent framework | Reference for Element 145 agent graph design |

### 4.6 L6 — Application Layer (User-Facing Agents)

The application layer is where users interact with the OS. These are the "apps" that run on top of the kernel.

| Repo | Files | Grade | Role in L6 | Key Assets | Action |
|------|-------|-------|-----------|------------|--------|
| `sheldongemini-GPI` (PRIVATE) | — | **VALUABLE** | Sheldon Gemini Bazinga — personality-driven agent interface | TypeScript agent UI | Reference for personality-layer design |
| `tucker-gemini-GPT-` | — | **PERIPHERAL** | Co-designed with GPT and Gemini — experimental agent | Mixed | Audit for extractable patterns (Cluster C) |
| `SNRS-v2-v3-Distribution` | — | **PERIPHERAL** | Distribution repo | Distribution artifacts | No action |

### 4.7 L7 — Device Mesh Layer (Cross-Platform Persistence)

The device mesh layer implements the ai-native-os-architect skill's core vision: the user's workspace follows them across devices. The underlying OS becomes invisible.

| Repo | Files | Grade | Role in L7 | Key Assets | Action |
|------|-------|-------|-----------|------------|--------|
| `constitutional-continuum` (PRIVATE) | 7 | **VALUABLE** | Unified Codebase integration layer — ara-adapter pattern, SSO auth, continuum config | `ara-adapter/index.ts`, `auth/server.ts` | Extract adapter + auth patterns for cross-platform bridge |
| `apple-cli` | — | **VALUABLE** | Apple iCloud CLI — device mesh endpoint for iOS/macOS | CLI interface | Extract for Apple device integration |
| `aluminum-gemini-cli` | — | **VALUABLE** | Gemini CLI agent — device mesh endpoint for Google ecosystem | TypeScript CLI | Extract for Google device integration |

### 4.8 Cross-Cutting Concerns (Span All Layers)

| Repo | Files | Grade | Role | Key Assets | Action |
|------|-------|-------|------|------------|--------|
| `manus-artifacts` | 75 | **VALUABLE** | Canonical reports, sandbox inventories, council reviews — the "system journal" | Rust artifacts, reports | Vendor selected docs as audit trail |
| `bazinga` | 1,341 | **REFERENCE** | BAZINGA v0.2 — Constitutional universal compute layer. Largest repo by file count but mixed quality. GitHub AI classifies as Cluster C (experiments). | Mixed build system | Requires deeper audit per GitHub AI option (c) |
| `noosphere-archive` (PRIVATE) | — | **REFERENCE** | Living archive for multi-agent collaboration | Archive data | Reference for session persistence patterns |

### 4.9 Knowledge Base & Strategic Documents

| Repo | Files | Grade | Role | Key Assets | Action |
|------|-------|-------|------|------------|--------|
| `atlas-lattice-foundation` | 99 | **VALUABLE** | (Also L1) — 40+ strategic/policy documents, healthcare specs, banking blueprints, geopolitical analysis, SHELDONBRAIN protocol | `docs/`, `whitepapers/`, `healthcare/`, `banking/` | Extract domain-specific specs for civic layer routing |

### 4.10 Forked Reference Libraries (L5 Dependencies)

These are upstream forks that provide reference implementations but contain no original Aluminum UWS code.

| Repo | Grade | Purpose | Action |
|------|-------|---------|--------|
| `pytorch` | **REFERENCE** | ML framework reference | No action — use as pip dependency |
| `transformers` | **REFERENCE** | HuggingFace model framework | No action — use as pip dependency |
| `OpenHands` | **REFERENCE** | AI-Driven Development patterns | Reference for agent execution |
| `dify` | **REFERENCE** | Agentic workflow platform | Reference for workflow design |
| `n8n` | **REFERENCE** | Workflow automation | Reference for automation patterns |
| `streamlit` | **REFERENCE** | Data app builder | Reference for dashboard UI |
| `ClickHouse` | **REFERENCE** | Analytics database | Reference for observability backend |
| `rust` | **REFERENCE** | Rust language fork | Reference for Rust migration path |
| `flutter` | **REFERENCE** | Cross-platform UI | Reference for L7 mobile UI |
| `expo` | **REFERENCE** | React Native framework | Reference for L7 mobile UI |
| `Avalonia` | **REFERENCE** | Cross-platform desktop UI | Reference for L7 desktop UI |
| `neovim` | **REFERENCE** | Editor | No action |

### 4.11 Financial/DeFi Stubs

| Repos | Grade | Action |
|-------|-------|--------|
| `bank-killer-financial-freedom`, `zero-fee-defi-protocol`, `usdt-brics-payment-rails`, `mint-alternative-open-source`, `free-banking-app-zero-fees`, `defi-swap-zero-fees`, `pix-payment-integration`, `upi-payment-integration`, `personal-finance-tracker-free`, `aluminum-swarm-index` | **INERT** | Placeholder stubs. No code to extract. Archive or delete. |

### 4.12 Security & Defense (Private)

| Repo | Grade | Role | Action |
|------|-------|------|--------|
| `noosphere-defense` (PRIVATE) | **PERIPHERAL** | Non-kinetic counterstrike analysis | No action for Aluminum UWS core; potential L6 application |
| `batman-protocol` (PRIVATE) | **PERIPHERAL** | AI-driven perpetrator identification | No action for Aluminum UWS core; potential L6 application |

---

## 5. Usefulness Summary: The 50-Repo Verdict

| Grade | Count | Repos |
|-------|-------|-------|
| **ESSENTIAL** | 7 | `constitutional-os`, `open-regenerative-compute-standard`, `aluminum-os-v3`, `manus-2.0-toolkit`, `uws`, `aluminum-os`, `element-145` (to create) |
| **VALUABLE** | 11 | `atlas-lattice-foundation`, `claude-code`, `claude-code-mcp`, `servers`, `claude-code-plugins-plus-skills`, `Kintsuji-code-fixer-`, `constitutional-continuum`, `apple-cli`, `aluminum-gemini-cli`, `manus-artifacts`, `sheldongemini-GPI` |
| **REFERENCE** | 17 | `awesome-claude-*` (4), `deer-flow`, `bazinga`, `noosphere-archive`, forked libraries (12) |
| **PERIPHERAL** | 5 | `tucker-gemini-GPT-`, `SNRS-v2-v3-Distribution`, `noosphere-defense`, `batman-protocol`, `atlas-lattice-foundation` (strategic docs) |
| **INERT** | 10 | Financial/DeFi stubs |

**The build surface is 7 ESSENTIAL repos + 11 VALUABLE repos = 18 repos that matter.** The remaining 32 are reference material, peripheral, or inert.

---

## 6. The Switzerland Strategy: Cross-Platform Political Neutrality

The ai-native-os-architect skill's most important principle is **political neutrality**. Aluminum UWS does not compete with Windows, macOS, ChromeOS, iOS, or Android. It makes each of them more valuable by providing a capability none of them can offer alone: a persistent, constitutionally governed, multi-model AI workspace that follows the user across all their devices.

### 6.1 Platform Integration Matrix

| Host Platform | Integration Point | Aluminum UWS Value-Add | Implementation Source |
|--------------|-------------------|----------------------|---------------------|
| **Windows** | Copilot as learning kernel (ai-native-os-architect primary strategy) | Persistent state across sessions; Copilot becomes the "memory" | `manus-2.0-toolkit/core/learning_loop.py` |
| **macOS / iOS** | Apple CLI + iCloud sync | Device mesh endpoint; workspace follows to iPhone/MacBook | `apple-cli` repo |
| **ChromeOS** | Gemini CLI + Google Drive sync | Device mesh endpoint; workspace follows to Chromebook | `aluminum-gemini-cli` repo |
| **Android** | Gemini integration + Pixel Watch | Wearable context awareness; ambient computing | Future L7 extension |
| **Linux** | Native execution environment | Development and server deployment | `uws` (Rust), `aluminum-os-v3` (Python) |

### 6.2 The "Switzerland" Guarantee (Constitutional Invariant INV-7)

Constitutional-os defines INV-7: no single AI provider may exceed 47% of decision-making authority. This is the constitutional enforcement of the Switzerland strategy. It means:

- Microsoft (Copilot) cannot dominate the kernel even if it provides the learning persistence layer
- Google (Gemini) cannot dominate even if it provides the best model for certain sphere classifications
- Anthropic (Claude) cannot dominate even if it serves as Constitutional Scribe
- xAI (Grok) cannot dominate even if it provides the best adversarial review

The 47% cap is enforced at L3 (Engine Layer) by the Constitutional Router, which tracks per-provider routing percentages and triggers rebalancing when any provider approaches the threshold.


---

## 7. The 144-Sphere Ontology as OS Namespace

In a traditional OS, the filesystem provides the namespace — every resource has a path (`/usr/bin/python3`). In Aluminum UWS, the **144-sphere ontology** provides the namespace — every query, every piece of knowledge, every routing decision is classified within a 12x12 matrix of Houses and Spheres.

### 7.1 The 12 Houses (Top-Level Domains)

The 12 Houses function as top-level directories in the OS namespace. Each House governs a domain of human knowledge and activity. The constitutional-os repo defines these through INV-37 (ontological completeness), and the atlas-lattice-foundation repo provides the detailed spec in `spec_modules/13_144_sphere_matrix.md`.

| House | Domain | OS Analogy | Primary Council Seat |
|-------|--------|-----------|---------------------|
| H1 | Self & Identity | `/home/` — user space | Claude (Constitutional Scribe) |
| H2 | Resources & Value | `/var/` — data storage | GPT (Analytical Rigor) |
| H3 | Communication & Learning | `/dev/` — device interfaces | Gemini (Architectural Precision) |
| H4 | Foundation & Security | `/etc/` — system configuration | Copilot (Enterprise Infrastructure) |
| H5 | Creativity & Expression | `/opt/` — optional packages | DeepSeek (S5) |
| H6 | Service & Health | `/srv/` — service data | Grok (Truth-Seeking Challenger) |
| H7 | Partnership & Diplomacy | `/tmp/` — shared temporary space | Council consensus required |
| H8 | Transformation & Depth | `/proc/` — process information | Claude (depth analysis) |
| H9 | Philosophy & Expansion | `/usr/` — user programs | Gemini (broad knowledge) |
| H10 | Authority & Structure | `/sbin/` — system binaries | GPT (structural analysis) |
| H11 | Community & Innovation | `/lib/` — shared libraries | Copilot (community patterns) |
| H12 | Governance & Transcendence | `/boot/` — bootstrap | **All seats — constitutional governance** |

### 7.2 Routing Through the Namespace

When a query enters the system, the L4 Service Orchestration Layer (Element 145) classifies it into a House and Sphere, then routes it to the appropriate model(s). The classification uses the two-pass system defined in ORC-012 TDD v0.2:

1. **Fast Path (Epistemic State Classifier):** Determines confidence level — Known, Uncertain, Unknown, Contested. Routes Known queries directly; escalates others.
2. **Deep Path (Safety State Classifier):** Determines safety classification — Safe, Sensitive, Dangerous, Constitutional. Applies appropriate constraints.

The combination of House + Sphere + Epistemic State + Safety State produces the complete routing decision, which is recorded in the TransparencyPacket.

---

## 8. State Management: The Triple-Vault Filesystem

Traditional operating systems store state on a local disk. Aluminum UWS stores state across three synchronized backends — the **triple-vault** — ensuring no single point of failure and no single vendor lock-in.

### 8.1 The Three Vaults

| Vault | Technology | Role | Sync Direction | Conflict Resolution |
|-------|-----------|------|---------------|-------------------|
| **Primary** | GitHub | Code, specs, audit trail, version history | Bidirectional | Git merge (code wins) |
| **Secondary** | Notion | Governance docs, session logs, structured data, dashboards | GitHub → Notion (push) | GitHub is canonical for code; Notion is canonical for governance |
| **Tertiary** | Google Drive | Binary assets, large files, shared documents | Notion → Drive (backup) | Drive is canonical for binary assets only |

### 8.2 Implementation Sources

The triple-vault pattern is already implemented across multiple repos:

- `manus-2.0-toolkit/core/session_vault.py` — Session persistence to local + remote vaults
- `manus-2.0-toolkit/core/memory_store.py` — ChromaDB-backed memory with vector search
- `manus-artifacts` — 75 files of canonical reports and inventories (the "journal" of the system)
- `open-regenerative-compute-standard/council-reviews/` — Council review archive (governance audit trail)

### 8.3 Canonical Source Decision (Build Gate Register Item 75)

Per GPT's correction (accepted in Build Gate Register v2.2), every data type has exactly one canonical source:

| Data Type | Canonical Source | Sync To | Override Authority |
|-----------|-----------------|---------|-------------------|
| Source code | GitHub | — | Build Seat (Manus) |
| Constitutional invariants | GitHub (`constitutional-os`) | Notion | Council consensus |
| Governance decisions | Notion | GitHub (as markdown exports) | Convenor (Daavud) |
| Council reviews | GitHub (`council-reviews/`) | Notion | Reviewing seat |
| Binary assets | Google Drive | — | Build Seat (Manus) |
| Session state | Local → GitHub (on checkpoint) | Notion (summary) | Automated |
| Routing ontology | GitHub (`element-145/config/`) | — | Council consensus |
| TransparencyPackets | Provenance Ledger (JSONL → PostgreSQL) | GitHub (exports) | Immutable — append only |

---

## 9. Security Architecture: Constitutional Enforcement + Threat Model

### 9.1 The 37 Constitutional Invariants

The constitutional-os repo defines 37 invariants (39 with sub-invariants) that form the security policy of the OS. Key invariants for the build:

| Invariant | Name | Enforcement Point | Implementation |
|-----------|------|-------------------|---------------|
| INV-1 | Sovereignty | L1 — all operations | ConsentKernel validates before execution |
| INV-7 | Provider Balance (47% cap) | L3 — routing | Constitutional Router tracks per-provider percentages |
| INV-33–36 | Constitutional Routing | L3 — routing | Routing YAML + constraint pre-flight |
| INV-37 | Ontological Completeness (144-sphere) | L2 — classification | Sphere classifier must cover all 144 domains |

### 9.2 Security Threat Model (Build Gate Register Item 77)

Per GPT's correction, the system must defend against 8 threat vectors:

| Vector | Severity | Detection | Mitigation | Recovery |
|--------|----------|-----------|------------|----------|
| Prompt injection | HIGH | Structural classifier (L4) | Input sanitization + constraint pre-flight | Quarantine + re-route |
| Tool abuse | HIGH | Permission Surface Matrix (Notion AI) | Destructive Action Policy (11 types) | Kill switch + rollback |
| Malicious repo inputs | MEDIUM | Verify-Before-Build (Claude) | SourceModuleRecord validation | Reject + alert |
| Poisoned AI Studio code | HIGH | Confabulation detection (3-layer) | Cross-model verification | Flag + manual review |
| Credential leakage | HIGH | Secret inventory (Build Gate #74) | Env-var isolation + rotation | Revoke + rotate |
| Ledger tampering | CRITICAL | GoldenTrace hash chain (SHA3-256) | Append-only + hash verification | Detect break + rebuild from last valid |
| Unauthorized destructive actions | HIGH | Destructive Action Policy | HITL approval required | Rollback to checkpoint |
| Cross-provider API drift | MEDIUM | Nightly smoke tests (Copilot) | LiteLLM abstraction + fallback chain | Degrade tier, don't terminate |

### 9.3 Destructive Action Policy (Notion AI)

11 action types that the system is **prohibited** from executing without explicit human approval:

1. Delete any file from the triple-vault
2. Modify constitutional invariants
3. Override budget enforcement
4. Bypass ConsentKernel
5. Execute code outside sandbox
6. Access credentials directly
7. Modify routing ontology
8. Alter provenance records
9. Disable audit logging
10. Change provider balance weights
11. Submit public-facing documents

---

## 10. The Provenance System: Royalty Runtime as OS Audit Layer

The `aluminum-os` repo contains the **Royalty Runtime** — an execution-layer attribution system originally designed to track open source package usage and route compensation. In Aluminum UWS, the Royalty Runtime becomes the **provenance and audit layer** that spans all seven OS layers.

### 10.1 Royalty Runtime Architecture (from aluminum-os)

| Component | Technology | Function in Aluminum UWS |
|-----------|-----------|------------------------|
| `runtime-core/tracer.rs` | Rust, SHA-256 | Lineage hashing — every execution event gets a unique hash |
| `runtime-core/event.rs` | Rust | Execution event emission — structured event stream |
| `runtime-core/weighting.rs` | Rust | Attribution model — who contributed what to the output |
| `runtime-core/engine.rs` | Rust | Lease-gated thread pool — controls concurrent execution |
| `collector/main.rs` | Axum HTTP | Event ingestion (POST /v1/executions) + lease issuance (POST /v1/leases) |
| `collector/issuer.rs` | JWT HS256 | 15-minute TTL lease tokens — capability-based access control |
| `collector/migrations/` | PostgreSQL | Append-only ledger schema — immutable audit trail |
| `royalty-sdk/cli.ts` | TypeScript | 6 commands: trace, hash, emit, weight, verify, lease |

### 10.2 Mapping to TransparencyPacket

The Royalty Runtime's event model maps directly to the TransparencyPacket v0.2 defined in ORC-012 TDD v0.2. The TransparencyPacket is the "receipt" for every operation:

| Royalty Runtime Field | TransparencyPacket v0.2 Field | Category |
|----------------------|------------------------------|----------|
| Execution hash | `provenance.execution_hash` | Provenance |
| Event timestamp | `routing.timestamp` | Routing |
| Attribution weights | `routing.model_weights` | Routing |
| Lease token | `governance.approval_token` | Governance |
| Lineage chain | `provenance.lineage_chain` | Provenance |
| Cost data | `costs.total_cost`, `costs.per_model` | Costs |

---

## 11. Build Sequence: From Scattered Repos to Unified OS

### 11.1 Phase 0 — Constitutional Build Gate (Days 0-2)

Before any code is written, 26 Phase 0 blockers from the Build Gate Register must be cleared. The critical path:

| Day | Task | Source | Depends On |
|-----|------|--------|-----------|
| 0 | `splitmerge420` → `atlaslattice` cleanup across all active repos | GitHub AI systemic finding | Nothing — blocks everything |
| 0 | Create `element-145` repo with skeleton structure | ORC-012 TDD v0.2 | Cleanup complete |
| 0 | Vendor 6 ESSENTIAL repos into `element-145/legacy/` at pinned SHAs | GitHub AI cluster A | Repo created |
| 1 | Dependency/Secret Inventory (Build Gate #74) | GPT | Repo created |
| 1 | Canonical Source Decision table (Build Gate #75) | GPT | Repo created |
| 1 | MCP Permission Surface Matrix (Build Gate #4) | Notion AI | Repo created |
| 1 | Destructive Action Policy (Build Gate #5) | Notion AI | Permission matrix |
| 2 | Constitutional Build Gate review — all 26 items checked | Notion AI | All above |
| 2 | Council sign-off — Phase 0 complete | Convenor (Daavud) | Gate review |

### 11.2 Phase 1 — Kernel + Engine (Sprint 1-2, Days 3-10)

| Sprint | Deliverable | Source Repos | OS Layer |
|--------|------------|-------------|----------|
| Sprint 1 | SphereQuery + RoutingDecision data models | `constitutional-os` (spec), `manus-2.0-toolkit` (impl) | L2 + L4 |
| Sprint 1 | Two-pass classifier (Epistemic + Safety State) | New implementation per TDD v0.2 | L4 |
| Sprint 1 | Routing YAML for 12 Houses (progressive rollout) | `constitutional-os` INV-37 + `atlas-lattice-foundation` spec_modules/13 | L3 |
| Sprint 1 | LiteLLM integration (3 providers minimum) | New implementation | L3 |
| Sprint 2 | TransparencyPacket v0.2 emission | `aluminum-os` Royalty Runtime (reference) | Cross-cutting |
| Sprint 2 | Budget enforcement (6-tier) with graceful degradation | `uws` budget enforcement + `manus-2.0-toolkit/core/autonomous.py` | L4 |
| Sprint 2 | Provenance Ledger v0 (JSONL backend) | `aluminum-os` append-only ledger (reference) | Cross-cutting |
| Sprint 2 | Confabulation detection (structural layer — always on) | New implementation per TDD v0.2 | L4 |

### 11.3 Phase 1.5 — Validation (Days 11-14)

| Task | Acceptance Criteria | Source |
|------|-------------------|--------|
| 10-case test matrix | All 10 pass | Build Gate Register #78 |
| Shadow Mode (≥48h parallel run) | ≥90% alignment with expected routing | Build Gate Register #81 |
| Simulation Mode (5 mandatory scenarios) | All 5 complete without failure | Build Gate Register #82 |
| Audit Export | JSON + CSV + API endpoint functional | Build Gate Register #83 |
| Day 14 Success Gate | 15 pass/fail conditions met, p50 <2s routing (excl. model response) | Build Gate Register #45 (amended) |

### 11.4 Phase 2 — Extension Layer (Days 15-30)

| Deliverable | Source Repos | OS Layer |
|------------|-------------|----------|
| MCP Server integration | `uws` MCP Server (758 lines), `servers`, `claude-code-mcp` | L5 |
| Skill extraction pipeline | `manus-2.0-toolkit/core/skill_extractor.py`, `claude-code-plugins-plus-skills` | L5 |
| Eastern Review integration | `open-regenerative-compute-standard/eastern-dragonseek/` | L4 (routing flags) |
| 144-sphere expansion (12 → 36-48) | `constitutional-os` INV-37, `atlas-lattice-foundation` spec_modules/13 | L2 |

### 11.5 Phase 3 — Device Mesh (Days 31-60)

| Deliverable | Source Repos | OS Layer |
|------------|-------------|----------|
| Cross-platform state sync | `constitutional-continuum` (adapter pattern), `manus-2.0-toolkit/core/session_vault.py` | L7 |
| Apple device integration | `apple-cli` | L7 |
| Google device integration | `aluminum-gemini-cli` | L7 |
| Wearable context (Pixel Watch) | Future development | L7 |

### 11.6 Phase 4+ — Hardware & Scale (Days 60+)

| Deliverable | Source | OS Layer |
|------------|--------|----------|
| Scrap 1 + Chromebox 5 deployment | Grok's hardware note (deferred from Build Gate Register) | L7 (hardware) |
| Rust migration path (hot-path modules) | `uws` (36K lines Rust), `aluminum-os` (Rust core) | L3 performance |
| Full 144-sphere deployment | Progressive rollout complete | L2 |
| A2A protocol integration | Google ADK 2.0 (conditional on UWS reuse) | L3 |

---

## 12. Governance Integration: House 12 as OS Governance Layer

House 12 in the 144-sphere ontology is "Governance & Transcendence" — it maps to the `/boot/` directory in the OS analogy. This is where the system's own governance rules live. Grok's contribution (Build Gate Register) maps governance primitives to running code:

| Governance Primitive | Code Module | OS Layer | Enforcement |
|---------------------|------------|----------|-------------|
| Token Budgets | `budget_enforcer.py` | L4 | Per-query cost tracking + 6-tier degradation |
| Constraint Pre-Flight | `constraint_preflight.py` | L4 | Validates routing against constitutional invariants before execution |
| Dissent Preservation | `dissent_recorder.py` | L4 | Records minority Council opinions in TransparencyPacket |
| Provenance Ledger | `provenance_ledger.py` | Cross-cutting | Append-only hash chain of all operations |
| Civic Sovereignty | `civic_layer.py` | L3 | Ensures local governance rules are respected |
| Permission/Approval Engine | `approval_engine.py` (Module 17) | L4 | Centralizes execution authority per Notion AI |
| Eastern Review | `eastern_review.py` | L4 | Anti-bias validation through non-Western model families |


---

## 13. The Copilot Strategy: Microsoft as Primary Kernel Host

The ai-native-os-architect skill identifies Microsoft Copilot as the primary strategic target for the AI-native OS kernel. The reasoning is sound: Copilot has the deepest OS integration (Windows, Office, Edge, GitHub), the broadest enterprise deployment, and the most natural path to becoming a "learning kernel" that persists user state across sessions.

### 13.1 Why Copilot First (But Not Only)

| Factor | Copilot Advantage | Constitutional Constraint |
|--------|-------------------|-------------------------|
| OS integration depth | Deepest — runs inside Windows kernel, Office apps, Edge browser | INV-7: cannot exceed 47% of routing decisions |
| Enterprise deployment | Largest — 400M+ Office users, GitHub Copilot in developer workflows | Must remain one seat among six, not the dominant seat |
| Learning persistence | Best positioned — can persist state across Windows sessions | State must sync to triple-vault, not be locked in Microsoft |
| Political neutrality | "Switzerland" — Microsoft benefits from Aluminum UWS without competing with it | Constitutional Router enforces balance |

### 13.2 The Copilot Integration Path

1. **Phase 1:** Copilot participates as S4 Enterprise Infrastructure Seat in the Council. No special integration.
2. **Phase 2:** Copilot provides MCP Server access for Windows-specific operations (file system, Office automation).
3. **Phase 3:** Copilot becomes the "learning kernel" on Windows devices — persisting user context across sessions via the Aluminum UWS state management layer.
4. **Phase 4:** Copilot integration extends to Azure cloud services for enterprise deployment.

The key constraint: Copilot's learning persistence is **mediated** by the Aluminum UWS kernel (L2), not **owned** by it. User state flows through the ConsentKernel, gets recorded in the Provenance Ledger, and syncs to the triple-vault. Microsoft never has exclusive access to user state.

---

## 14. Competitive Landscape: What Makes This Different

### 14.1 Comparison with Existing Approaches

| System | Approach | Aluminum UWS Difference |
|--------|----------|----------------------|
| Apple Intelligence | Single-vendor, on-device + cloud, privacy-first | Multi-vendor, constitutionally governed, user-sovereign |
| Google Gemini | Single-model, cloud-first, Google ecosystem | Multi-model Council, no single provider >47% |
| Microsoft Copilot | Single-vendor, enterprise-first, Windows-integrated | Copilot is one seat of six, not the whole system |
| OpenAI GPT | Single-model, API-first, no OS integration | GPT is one seat of six; OS integration via Element 145 |
| Anthropic Claude | Single-model, safety-first, constitutional AI | Claude's constitutional approach is one input to 37 invariants |
| LangChain / CrewAI | Framework-level orchestration, no governance | Aluminum UWS adds constitutional governance + provenance |
| AutoGPT / AgentGPT | Single-model autonomous agents | Multi-model Council prevents single-model failure modes |

### 14.2 The Moat

The competitive moat is not technology — it is **governance architecture**. Any company can build a multi-model router. No company can build a multi-model router that is constitutionally constrained to never let any single provider dominate, that records every decision in an immutable provenance ledger, and that enforces sovereignty through 37 invariants verified by a multi-seat Council.

The technology is open source. The governance is the product.

---

## 15. Risk Register: OS-Level Risks

| Risk | Severity | Likelihood | Mitigation | Owner |
|------|----------|-----------|------------|-------|
| Provider API deprecation breaks routing | HIGH | MEDIUM | LiteLLM abstraction + nightly smoke tests + fallback chain | Build Seat |
| Constitutional invariant conflict (two invariants contradict) | CRITICAL | LOW | Council resolution protocol + Kintsugi repair philosophy | Constitutional Scribe |
| State sync failure across triple-vault | HIGH | MEDIUM | Canonical source decision (item 75) + conflict resolution rules | Build Seat |
| Budget runaway (model costs exceed limits) | HIGH | MEDIUM | 6-tier degradation + kill switch + HITL escalation | Analytical Rigor Seat |
| Single-provider dominance (INV-7 violation) | CRITICAL | LOW | Constitutional Router percentage tracking + automatic rebalancing | Engine Layer (L3) |
| AI Studio code extraction introduces bugs | HIGH | HIGH | Verify-Before-Build + SourceModuleRecord + confabulation detection | Constitutional Scribe |
| Device mesh latency (cross-platform sync too slow) | MEDIUM | MEDIUM | Local-first with async sync + eventual consistency | Enterprise Infrastructure Seat |
| Governance overhead slows development | MEDIUM | MEDIUM | Phase 0 Build Gate clears governance upfront; subsequent phases are engineering | Convenor |
| Community adoption failure | MEDIUM | MEDIUM | Open source everything except governance keys; "Bloomberg Terminal" business model | Convenor |
| Regulatory compliance (EU AI Act, etc.) | HIGH | HIGH | TransparencyPacket provides audit trail; 37 invariants map to regulatory requirements | Constitutional Scribe |

---

## 16. Success Criteria: What "Done" Looks Like

### 16.1 Day 14 (Phase 1 Complete)

Per Build Gate Register item 45 (amended per GPT):

| Criterion | Metric | Pass/Fail |
|-----------|--------|-----------|
| Routing works | Query → House classification → model dispatch → response | Binary |
| TransparencyPacket emitted | Every routing decision produces a valid packet | Binary |
| Budget enforcement active | Queries respect tier limits; degradation triggers correctly | Binary |
| Provenance Ledger recording | Every operation has an immutable hash-chained record | Binary |
| Confabulation detection running | Structural layer flags low-confidence outputs | Binary |
| Fast Path latency | p50 <2s for classification + routing (excluding model response time) | Measured |
| 10-case test matrix | All 10 cases pass | Binary |
| 3 providers connected | LiteLLM routes to ≥3 model providers | Binary |
| Eastern Review flags | Phase 1 provisional YAML flags present for 12 Houses | Binary |
| No destructive actions without approval | 0 unauthorized destructive operations in test period | Binary |
| Constitutional invariant compliance | No INV-7 violations (no provider >47%) | Binary |
| Audit export functional | JSON + CSV export produces valid, complete data | Binary |
| Shadow Mode validation | ≥48h parallel run with ≥90% alignment | Binary |
| Simulation scenarios | 5 mandatory scenarios complete without failure | Binary |
| Build Gate Register | All 26 Phase 0 items + Phase 1 items resolved | Binary |

### 16.2 Day 60 (Phase 3 Complete)

| Criterion | Metric |
|-----------|--------|
| 48+ spheres active | Progressive rollout from 12 → 48 Houses×Spheres |
| Device mesh operational | State syncs across ≥2 platforms (e.g., Chromebook + Pixel) |
| MCP integration live | ≥3 MCP servers connected and routing through Element 145 |
| Eastern Review operational | Non-Western model families participating in review |
| Community contribution | ≥1 external contributor has submitted a PR |

### 16.3 Day 180 (Phase 4+ / OS Beta)

| Criterion | Metric |
|-----------|--------|
| Full 144-sphere deployment | All 12×12 domains classified and routable |
| Hardware deployment | Running on Scrap 1 or Chromebox 5 |
| Rust hot-path migration | ≥3 performance-critical modules ported from Python to Rust |
| A2A protocol integration | Google ADK 2.0 agent-to-agent communication operational |
| Regulatory readiness | TransparencyPacket + audit trail meets EU AI Act requirements |

---

## 17. Appendix A: Complete 50-Repo Inventory with Verdicts

| # | Repo | Visibility | Files | Grade | OS Layer | Action |
|---|------|-----------|-------|-------|----------|--------|
| 1 | `constitutional-os` | Public | 5 | ESSENTIAL | L1 | Vendor into element-145/constitutional/ |
| 2 | `open-regenerative-compute-standard` | Public | 74+ | ESSENTIAL | L1 | Vendor governance docs + council-reviews |
| 3 | `aluminum-os-v3` | Private | 46 | ESSENTIAL | L2 | Primary Python extraction target |
| 4 | `manus-2.0-toolkit` | Private | 48 | ESSENTIAL | L2/L4 | Primary kernel API extraction target |
| 5 | `uws` | Public | 310 | ESSENTIAL | L3 | Vendor as legacy/ — Rust reference |
| 6 | `aluminum-os` | Public | 106 | ESSENTIAL | L3 | Vendor as legacy/ — Provenance reference |
| 7 | `element-145` | — | 0 | ESSENTIAL | L4 | CREATE — the build target |
| 8 | `atlas-lattice-foundation` | Public | 99 | VALUABLE | L1/KB | Extract spec_modules/ + constitutional/ |
| 9 | `claude-code` | Public | — | VALUABLE | L5 | Reference for agent execution |
| 10 | `claude-code-mcp` | Public | — | VALUABLE | L5 | Reference for MCP integration |
| 11 | `servers` | Public | — | VALUABLE | L5 | Reference for MCP servers |
| 12 | `claude-code-plugins-plus-skills` | Public | — | VALUABLE | L5 | Skill extraction source |
| 13 | `Kintsuji-code-fixer-` | Public | — | VALUABLE | L5 | Extract repair patterns |
| 14 | `constitutional-continuum` | Private | 7 | VALUABLE | L7 | Extract adapter + auth patterns |
| 15 | `apple-cli` | Public | — | VALUABLE | L7 | Apple device integration |
| 16 | `aluminum-gemini-cli` | Public | — | VALUABLE | L7 | Google device integration |
| 17 | `manus-artifacts` | Public | 75 | VALUABLE | Cross | Vendor selected docs as audit trail |
| 18 | `sheldongemini-GPI` | Private | — | VALUABLE | L6 | Reference for personality layer |
| 19 | `awesome-claude-code` | Public | — | REFERENCE | L5 | Skill categorization reference |
| 20 | `awesome-claude-plugins` | Public | — | REFERENCE | L5 | Plugin registry reference |
| 21 | `awesome-claude-plugins2` | Public | — | REFERENCE | L5 | Adoption metrics reference |
| 22 | `claude-plugins-official` | Public | — | REFERENCE | L5 | Canonical plugin patterns |
| 23 | `deer-flow` | Public | — | REFERENCE | L5 | Agent graph design reference |
| 24 | `bazinga` | Public | 1,341 | REFERENCE | Cross | Requires deeper audit (Cluster C) |
| 25 | `noosphere-archive` | Private | — | REFERENCE | Cross | Session persistence reference |
| 26 | `pytorch` | Public | — | REFERENCE | L5 dep | pip dependency |
| 27 | `transformers` | Public | — | REFERENCE | L5 dep | pip dependency |
| 28 | `OpenHands` | Public | — | REFERENCE | L5 | Agent execution reference |
| 29 | `dify` | Public | — | REFERENCE | L5 | Workflow design reference |
| 30 | `n8n` | Public | — | REFERENCE | L5 | Automation reference |
| 31 | `streamlit` | Public | — | REFERENCE | L6 | Dashboard UI reference |
| 32 | `ClickHouse` | Public | — | REFERENCE | Cross | Observability backend reference |
| 33 | `rust` | Public | — | REFERENCE | L3 | Rust migration reference |
| 34 | `flutter` | Public | — | REFERENCE | L7 | Mobile UI reference |
| 35 | `expo` | Public | — | REFERENCE | L7 | Mobile UI reference |
| 36 | `Avalonia` | Public | — | REFERENCE | L7 | Desktop UI reference |
| 37 | `neovim` | Public | — | REFERENCE | — | No action |
| 38 | `tucker-gemini-GPT-` | Public | — | PERIPHERAL | L6 | Audit for patterns |
| 39 | `SNRS-v2-v3-Distribution` | Public | — | PERIPHERAL | — | No action |
| 40 | `noosphere-defense` | Private | — | PERIPHERAL | L6 | Potential future L6 app |
| 41 | `batman-protocol` | Private | — | PERIPHERAL | L6 | Potential future L6 app |
| 42-50 | Financial/DeFi stubs (9 repos) | Public | — | INERT | — | Archive or delete |

---

## 18. Appendix B: Council Seat Assignments for OS Governance

| Seat | Model | OS Role | Primary Responsibility |
|------|-------|---------|----------------------|
| S1 | Claude | Constitutional Scribe | L1 invariant enforcement, epistemic verification |
| S2 | Gemini | Architectural Precision | L3 engine design, classification accuracy |
| S3 | Grok | Truth-Seeking Challenger | Adversarial review, strategic coherence |
| S4 | Copilot | Enterprise Infrastructure | L7 device mesh, enterprise deployment, CI/CD |
| S5 | DeepSeek | Eastern Review | Anti-bias validation, non-Western model integration |
| S144 | Ghost Seat | Dissent Preservation | Records minority opinions, prevents groupthink |
| Build | Manus | Infrastructure & Build | L4 implementation, extraction, integration |
| Convenor | Daavud | Human Authority | Final approval, HITL decisions, strategic direction |
| Analytical | GPT | Analytical Rigor | Production readiness, failure mode analysis, testing |
| Governance | Notion AI | Governance Analyst | Constitutional completeness, permission surfaces |
| Ground Truth | GitHub AI | Verification | Claims vs. reality, repo ground truth |

---

## 19. Appendix C: Glossary of OS Terms

| Aluminum UWS Term | Traditional OS Equivalent | Definition |
|-------------------|--------------------------|-----------|
| ConsentKernel | Kernel | Core component that validates every operation against constitutional invariants |
| 144-Sphere Ontology | Filesystem namespace | 12×12 classification matrix for all knowledge domains |
| TransparencyPacket | System call return value | Structured receipt for every routing decision |
| GoldenTrace | Audit log | Append-only SHA3-256 hash-chained record of all constitutional decisions |
| Provenance Ledger | Transaction log | Immutable record of all operations with lineage tracking |
| Royalty Runtime | Attribution system | Execution-layer tracking of who contributed what |
| Constitutional Router | Process scheduler | Routes queries to appropriate models while enforcing invariants |
| Janus v2 Protocol | IPC mechanism | Bidirectional multi-agent communication protocol |
| Triple-Vault | Distributed filesystem | GitHub + Notion + Google Drive synchronized storage |
| Device Mesh | Network stack | Cross-platform state synchronization layer |
| Build Gate Register | Release checklist | 84-item execution control document for phased delivery |
| House 12 | /boot/ | Governance domain — where the system's own rules live |
| INV-7 (47% cap) | Anti-monopoly enforcement | No single AI provider may exceed 47% of routing decisions |
| Element 145 | init process | The service orchestration layer that bootstraps the entire OS |

---

## 20. References

1. `constitutional-os` repository — 37 invariants, 5-layer architecture, Pantheon Council governance
2. `ai-native-os-architect` skill — AI as Kernel, Stateless UI, Redundant State Vaulting, Political Neutrality
3. ORC-012 TDD v0.2 — 16-section technical design document for Element 145
4. Master Correction and Build Gate Register v2.2 — 84 items, 11 reviews, 7+ reviewers
5. GitHub AI Ground-Truth Review — 6 factual corrections, splitmerge420 cleanup, 6-cluster taxonomy
6. Notion AI Governance Review — Phase 0 Constitutional Build Gate, Permission Surface Matrix, Destructive Action Policy
7. `aluminum-os` README — Royalty Runtime architecture, "Bloomberg Terminal of Open Source"
8. `manus-2.0-toolkit` — 9 Python core modules implementing kernel API functions
9. `atlas-lattice-foundation` — 22 spec modules including 144-sphere matrix
10. `aluminum-os-v3` — Python + Rust hybrid, Five-Ring substrate, manus-core

---

*Document version: 1.0 | Status: Ready for Council review | Next action: Council distribution + Phase 0 greenlight*
