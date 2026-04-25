# Full Inventory: Aluminum OS Ecosystem

> Cross-repo audit conducted 2026-03-23.
> Covers `atlaslattice/uws` and `atlaslattice/aluminum-os`.

---

## atlaslattice/uws

**Description:** Universal Workspace CLI — Google, Microsoft 365, Apple, Android and Chrome in one tool. Built for humans and AI agents. The command surface of Aluminum OS.

**Default branch:** `uws-universal`

### Rust Source (`src/`)

36+ Rust source files including:

| File | Purpose |
|------|---------|
| `main.rs` | Entry point, command routing, telemetry hook |
| `royalty_observability.rs` | Execution telemetry — lineage hashing, event emission |
| `royalty_weight.rs` | Attribution weighting — 40/60 primary-plus-equal-split model |
| `fusion_engine.rs` | Cross-ecosystem file namespace abstraction |
| `constitutional_engine.rs` | 8-invariant governance enforcement |
| `agentic_sovereignty.rs` | AI agent autonomy framework |
| `gpt_pantheon.rs` | GPT integration layer |
| `grok_bazinga.rs` | Grok integration layer |
| `claude_miracles.rs` | Claude integration layer |
| `audit_chain.rs` | Append-only audit ledger |
| `council_github_client.rs` | GitHub operations with governance |

### Skills Directory (`skills/`)

**95+ skill directories** organized into:

- **27 Google Workspace skills:** admin-reports, calendar, calendar-agenda, calendar-insert, chat, chat-send, classroom, docs, docs-write, drive, drive-upload, events, events-renew, events-subscribe, forms, gmail, gmail-send, gmail-triage, gmail-watch, keep, meet, people, sheets, sheets-append, sheets-read, slides, tasks
- **5 GWS workflow automations:** email-to-task, file-announce, meeting-prep, standup-report, weekly-digest
- **3 ModelArmor skills:** create-template, sanitize-prompt, sanitize-response
- **3 Microsoft integrations:** ms-onedrive, ms-outlook, ms-teams
- **2 Apple integrations:** apple-calendar, apple-contacts
- **40+ recipe automations:** backup-sheet-as-csv, batch-invite-to-event, block-focus-time, bulk-download-folder, create-classroom-course, create-doc-from-template, draft-email-from-doc, find-free-time, label-and-archive-emails, plan-weekly-schedule, reschedule-meeting, share-doc-and-notify, sync-contacts-to-sheet, and more
- **10 persona packs:** content-creator, customer-support, event-coordinator, exec-assistant, hr-coordinator, it-admin, project-manager, researcher, sales-ops, team-lead
- **1 core module:** uws-core

### Key Directories

| Directory | Contents |
|-----------|----------|
| `bridge/` | Chromium bridge specification |
| `docs/` | Alexandria CLI spec, ecosystem map, session logs |
| `experiments/royalty-runtime/` | 5 papers: ARCHITECTURE.md, OBSERVABILITY-PIVOT.md, README.md, ROADMAP.md, SUMMARY.md |
| `ingestion/` | 144-sphere ontology, master ingestion, verified ontology |
| `insights/` | Analysis and intelligence |
| `janus/` | Janus Council specs: boot sequence, heartbeat, v2 spec |
| `mcp_server/` | Model Context Protocol server (server.py) |
| `registry/` | personas.yaml, recipes.yaml |
| `scripts/` | Build and automation scripts |
| `templates/modelarmor/` | ModelArmor templates |
| `tests/` | Test suite |
| `toolchain/` | Build toolchain configuration |
| `.agent/` | Agent configuration |
| `.claude/` | Claude Code configuration |
| `.gemini/` | Gemini configuration |
| `.github/` | GitHub Actions, Copilot settings |

### Root Documentation (20+ files)

Architecture and synthesis docs:
- `ALUMINUM.md`, `ALUMINUM_OS_V1_ARCHITECTURE.md`
- `AGENTS.md`, `CLAUDE.md`, `CONTEXT.md`
- `FEATURE_MANIFEST.md`, `FUSION_ENGINE.md`
- `GEMINI_SYNTHESIS.md`, `COPILOT_CLI_SPEC.md`, `COPILOT_INTEGRATION_GUIDE.md`
- `GROK_REVIEW.md`

Wishlist fulfillment docs (multi-AI collaboration artifacts):
- `AGENTIC_SOVEREIGNTY_FULFILLED.md`
- `CLAUDE_MIRACLES_FULFILLED.md`
- `CONSTITUTIONAL_WISHLIST_FULFILLED.md`
- `GOOGLE_WISHLIST_FULFILLED.md`
- `GPT_WISHLIST_FULFILLED.md`
- `GROK_WISHLIST_FULFILLED.md`
- `MICROSOFT_WISHLIST_FULFILLED.md`

Research and audit files:
- `copilot_365_features_research.txt`
- `gemini_cli_research.txt`
- `gpt_pantheon_audit.md`
- `diagnostics_audit.txt`
- `copilot-janus-checkpoint-2026-03-20-FULL.md`

### Active PR: #18

**Branch:** `copilot/add-royalty-runtime-observability-layer`
**Title:** feat: Royalty Oracle step 3 — v0 package attribution weighting (`uws royalty weight`)
**Files added:** `royalty_weight.rs`, `royalty_observability.rs`
**Files modified:** `main.rs`, `Cargo.toml`, `Cargo.lock`, plus formatting fixes across constitutional_engine.rs, council_github_client.rs, audit_chain.rs

---

## atlaslattice/aluminum-os

**Description:** The full Aluminum OS kernel and subsystem repository.

**Default branch:** `master`

### Root Directories (20+)

architecture, council, governance, enterprise, intelligence, kernel, kintsugi, memory, plugins, protocols, prototype, research, specifications, integrations, health, infrastructure, python, src, docs, royalty-runtime

### Royalty Runtime (`royalty-runtime/`) — 27 files

**Runtime Core (Rust) — 9 files:**
- `runtime-core/Cargo.toml`
- `runtime-core/src/lib.rs`
- `runtime-core/src/tracer.rs` — canonical lineage hashing (SHA-256)
- `runtime-core/src/event.rs` — execution event emission
- `runtime-core/src/weighting.rs` — attribution model (40/60 split)
- `runtime-core/src/engine.rs` — lease-gated thread pool
- `runtime-core/tests/hash_stability.rs` — 8 deterministic hash tests
- `runtime-core/tests/adversarial_lease.rs` — 6 security tests
- `runtime-core/benches/throughput_bench.rs` — Criterion benchmarks

**Collector (Rust/Axum) — 4 files:**
- `collector/Cargo.toml`
- `collector/src/main.rs` — POST /v1/executions + POST /v1/leases
- `collector/src/issuer.rs` — JWT signing (HS256, 15-min TTL)
- `collector/migrations/20260323_init_executions.sql` — PostgreSQL schema

**TypeScript SDK — 7 files:**
- `royalty-sdk/package.json`
- `royalty-sdk/tsconfig.json`
- `royalty-sdk/src/index.ts`
- `royalty-sdk/src/cli.ts` — 6 CLI commands
- `royalty-sdk/src/lease.ts` — capability-based lease acquisition
- `royalty-sdk/src/utils/dependency-graph.ts` — tree hashing
- `royalty-sdk/src/utils/dependency-graph.test.ts` — 6 Vitest tests

**Documentation — 7 files:**
- `docs/WHITEPAPER.md` — full technical architecture
- `docs/MANIFESTO.md` — open source compensation philosophy
- `docs/PROVENANCE.md` — historical context and parallels
- `docs/SUMMARY.md` — session architecture overview
- `docs/CONVERGENCE.md` — 6 novel architectural concepts (NEW)
- `docs/INVENTORY.md` — this file (NEW)
- `README.md` — project introduction

---

## Totals

| Category | Count |
|----------|-------|
| Rust source files (uws) | 36+ |
| Rust source files (aluminum-os/royalty-runtime) | 13 |
| TypeScript files (aluminum-os/royalty-runtime) | 5 |
| Skill directories (uws) | 95+ |
| Recipe automations (uws) | 40+ |
| Persona packs (uws) | 10 |
| Documentation files (both repos) | 40+ |
| SQL migrations | 1 |
| Config files (both repos) | 15+ |
| **Estimated total files across both repos** | **300+** |

---

## Session Output (2026-03-23)

Files created and pushed during this session:

- 25 royalty-runtime files to aluminum-os
- 2 new docs (CONVERGENCE.md, INVENTORY.md) to aluminum-os
- 1 README.md replaced on aluminum-os root
- 1 Gamma pitch deck generated (10 slides, Stratos theme)
- PR #18 code reviewed and documented for cross-AI collaboration
- Full architectural analysis with 6 novel convergence concepts

**Session file count: 29 files pushed + 1 pitch deck generated**
