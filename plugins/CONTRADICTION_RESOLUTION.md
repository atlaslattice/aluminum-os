# Contradiction Resolution Manifest v1.0

> **Policy**: NO-DELETE / APPEND-ONLY / KINTSUGI  
> **GoldenTrace**: All resolutions emit `contradiction.resolved` events  
> **Invariants**: INV-1, INV-7, INV-24 (amendment protocol)  
> **Date**: 2026-03-20  

## Resolution Protocol

When contradictions are found between forked ecosystems and Aluminum OS:

1. **NEVER delete** either side of the contradiction
2. **Document** both positions with their source and rationale
3. **Propose** a kintsugi repair (golden seam that makes the join stronger)
4. **Flag** severity: CRITICAL / HIGH / MEDIUM / LOW
5. **Assign** council member for resolution review
6. **Emit** GoldenTrace `contradiction.found` and `contradiction.resolved` events

---

## CONTRADICTION #1: Plugin Installation Authority

**CRITICAL** | Council: Claude (Governance)

| Position A | Position B |
|-----------|-----------|
| **claude-plugins-official**: `/plugin install {name}@claude-plugins-official` — Anthropic is canonical source | **CCPI**: `ccpi install {name}` — independent package manager, own resolution | 
| **Source**: anthropics/claude-plugins-official | **Source**: jeremylongshore/claude-code-plugins-plus-skills |

**Contradiction**: Two competing installation authorities. Anthropic's official system and CCPI's independent package manager both claim to be the install surface.

**Kintsugi Repair**: `uws plugin install` becomes the unified surface. It resolves from official first (Priority 1), falls back to CCPI (Priority 2). Both systems preserved, neither deleted. The `PLUGIN_REGISTRY.yaml` priority order is the golden seam.

**Status**: RESOLVED via PLUGIN_REGISTRY.yaml priority chain

---

## CONTRADICTION #2: Orchestrator Proliferation vs. Single Protocol

**HIGH** | Council: Gemini (Substrate)

| Position A | Position B |
|-----------|-----------|
| **Ecosystem**: 10 independent orchestrators (Claude Squad, Swarm, Auto-Claude, etc.) each with own topology | **Aluminum OS**: Janus v2 is THE constitutional multi-agent protocol with INV-7 enforcement |
| **Source**: awesome-claude-code (multiple repos) | **Source**: aluminum-os/janus/JANUS_V2_SPEC.md |

**Contradiction**: Community orchestrators don't enforce INV-7 (47% cap), INV-8 (Ghost Seat), or emit GoldenTrace. They operate outside constitutional bounds.

**Kintsugi Repair**: Janus v2 exposes topology modes that map to each orchestrator's pattern (see ECOSYSTEM_MERGE.md orchestrator table). Community orchestrators are NOT deleted — they're wrapped via `janus.adapter.{name}` that injects constitutional compliance. The adapter pattern is the golden seam: community innovation preserved, constitutional guarantees added.

**Status**: ARCHITECTURE PROPOSED — adapters need implementation

---

## CONTRADICTION #3: Plugin Metadata Schema

**HIGH** | Council: Copilot (Enterprise)

| Position A | Position B |
|-----------|-----------|
| **claude-plugins-official**: `plugin.json` in `.claude-plugin/` directory is THE standard | **Aluminum OS**: needs `.aluminum/layer.yaml`, `sphere_tags.yaml`, `invariants.yaml` |
| **Source**: anthropics/claude-plugins-official | **Source**: aluminum-os/plugins/ECOSYSTEM_MERGE.md |

**Contradiction**: Anthropic's plugin.json has no concept of Aluminum OS layers, 144-sphere tags, or constitutional invariants. Adding these to plugin.json would fork the standard.

**Kintsugi Repair**: `.aluminum/` directory sits ALONGSIDE `.claude-plugin/`, not inside it. This extends without modifying. Anthropic's standard is preserved intact. Aluminum OS metadata is additive — the `.aluminum/` sidecar is the golden seam. Plugins without `.aluminum/` default to L5-Extension, H7.S3, no invariant declarations.

**Status**: RESOLVED via sidecar pattern in ECOSYSTEM_MERGE.md

---

## CONTRADICTION #4: Memory Systems

**HIGH** | Council: DeepSeek (Research)

| Position A | Position B |
|-----------|-----------|
| **recall** (awesome-claude-code): Full-text search of Claude Code sessions, file-based | **Sheldonbrain**: Qdrant vector store + 144-sphere RAG classification |
| **Source**: zippoxer/recall | **Source**: aluminum-os/docs/integration/SHELDONBRAIN_INTEGRATION.md |

**Contradiction**: Two incompatible memory/retrieval systems. recall is lightweight file-based search; Sheldonbrain is a full RAG pipeline with semantic classification.

**Kintsugi Repair**: recall becomes Sheldonbrain's L5 lightweight fallback. When Sheldonbrain is unavailable (offline mode), recall provides degraded-but-functional session search. When Sheldonbrain is active, recall's file-based index feeds into the Qdrant ingestion pipeline. Neither is deleted. The dual-mode is the golden seam — it also satisfies INV-34 (Offline Routing).

**Status**: ARCHITECTURE PROPOSED

---

## CONTRADICTION #5: Security Model

**CRITICAL** | Council: Grok (Adversarial)

| Position A | Position B |
|-----------|-----------|
| **Dippy** (awesome-claude-code): AST-based auto-approval of "safe" bash commands | **Aluminum OS**: ConsentKernel requires explicit user consent for ALL privileged operations (INV-1) |
| **Source**: ldayton/Dippy | **Source**: aluminum-os L1-Constitutional |

**Contradiction**: Dippy auto-approves commands it deems safe via AST parsing. ConsentKernel says nothing runs without consent. These directly conflict.

**Kintsugi Repair**: Dippy's AST classification becomes an INPUT to ConsentKernel, not a replacement. Dippy classifies risk level → ConsentKernel decides based on risk + user preferences. Low-risk commands can be user-configured as auto-approved (consent given at configuration time, not execution time). INV-1 is preserved because the user consented to the auto-approval policy. The risk-classification layer is the golden seam.

**Status**: RESOLVED via ConsentKernel risk-tiering

---

## CONTRADICTION #6: Package Manager CLI Syntax

**MEDIUM** | Council: Copilot (Enterprise)

| Position A | Position B | Position C |
|-----------|-----------|-----------|
| `/plugin install name@source` | `ccpi install name` | `uws plugin install name` |
| **Source**: claude-plugins-official | **Source**: CCPI | **Source**: aluminum-os/uws |

**Contradiction**: Three different installation syntaxes across the ecosystem.

**Kintsugi Repair**: `uws plugin install` is the canonical Aluminum OS surface. It internally dispatches to the appropriate backend (official plugin system or CCPI). The `/plugin install` command is preserved as an alias within Claude Code sessions. All three syntaxes work — the translation layer is the golden seam.

**Status**: RESOLVED via uws unified surface

---

## CONTRADICTION #7: Prompt Injection Defense

**CRITICAL** | Council: Grok (Adversarial)

| Position A | Position B |
|-----------|-----------|
| **parry** (awesome-claude-code): Hook-based prompt injection scanning at Claude Code level | **Aluminum OS**: INV-35 (Hard Fail-Closed) at L1-Constitutional level |
| **Source**: vaporif/parry | **Source**: aluminum-os L1 |

**Contradiction**: parry operates at L5 (hook level), but prompt injection is an L1 concern. If parry fails, there's no L1 backstop.

**Kintsugi Repair**: parry runs at L5 as early warning. Constitutional Router (INV-35) runs at L1 as hard backstop. Defense-in-depth — both layers active, neither deleted. If parry catches injection at L5, it's fast-path rejected. If parry misses, INV-35 at L1 catches it with hard fail-closed. The layered defense is the golden seam.

**Status**: RESOLVED via defense-in-depth layering

---

## CONTRADICTION #8: Session Continuity

**MEDIUM** | Council: Claude (Governance)

| Position A | Position B |
|-----------|-----------|
| **claude-code-tools**: Session restore via file checkpoints | **claudekit**: Auto-save checkpointing with different format |
| **Source**: pchalasani/claude-code-tools | **Source**: carlrannaberg/claudekit |

**Contradiction**: Two incompatible session checkpoint formats.

**Kintsugi Repair**: GoldenTrace already defines a canonical event format. Both tools' checkpoint formats are preserved as-is, but a `golden_trace.session_checkpoint` event type bridges them. Import adapters convert both formats to GoldenTrace events. Format diversity preserved, interop achieved. The GoldenTrace event envelope is the golden seam.

**Status**: ARCHITECTURE PROPOSED

---

## CONTRADICTION #9: Configuration Management

**MEDIUM** | Council: Copilot (Enterprise)

| Position A | Position B | Position C |
|-----------|-----------|-----------|
| **CLAUDE.md files** (20+ patterns): Project-level config | **SuperClaude Framework**: Global config enhancement | **ClaudeCTX**: Config profile switching |
| **Source**: awesome-claude-code | **Source**: SuperClaude-Org | **Source**: foxj77/claudectx |

**Contradiction**: Three overlapping configuration systems with different scopes (project vs. global vs. profile).

**Kintsugi Repair**: These are complementary, not conflicting. CLAUDE.md = project scope, SuperClaude = global scope, ClaudeCTX = profile switching between configurations. The Aluminum OS mapping: CLAUDE.md → L5 project config, SuperClaude → L2 kernel config, ClaudeCTX → L5 config manager. Clear layer separation is the golden seam.

**Status**: RESOLVED via layer separation

---

## CONTRADICTION #10: Usage Monitoring Authority

**LOW** | Council: Gemini (Substrate)

| Position A | Position B | Position C |
|-----------|-----------|-----------|
| **ccflare**: Web UI dashboard | **better-ccflare**: Enhanced fork of ccflare | **CC Usage (ccusage)**: CLI-based analytics |
| **Source**: snipeship/ccflare | **Source**: tombii/better-ccflare | **Source**: ryoppippi/ccusage |

**Contradiction**: Three overlapping usage monitors. better-ccflare is a fork of ccflare, creating lineage confusion.

**Kintsugi Repair**: All three preserved. `uws plugin stats` aggregates from awesome-claude-plugins2 (quemsah metrics) as canonical telemetry source. Individual monitors remain as complementary views. The fork relationship is documented: ccflare → better-ccflare (superseded_by, not deleted). The metrics aggregation layer is the golden seam.

**Status**: RESOLVED via metrics aggregation

---

## CONTRADICTION #11: MCP Bridge Architecture

**HIGH** | Council: Gemini (Substrate)

| Position A | Position B |
|-----------|-----------|
| **claude-code-mcp**: Direct local CLI invocation via MCP | **Aluminum OS MCP plan**: Constitutional MCP servers (golden-trace-mcp, consent-kernel-mcp, council-mcp) |
| **Source**: KunihiroS/claude-code-mcp | **Source**: aluminum-os/plugins/INTEGRATION_BRIDGE.md |

**Contradiction**: claude-code-mcp bridges MCP→CLI without constitutional awareness. Constitutional MCP servers don't exist yet.

**Kintsugi Repair**: claude-code-mcp is preserved as the raw bridge. Constitutional MCP servers are built as middleware that wraps it. Request flow: `caller → consent-kernel-mcp → golden-trace-mcp → claude-code-mcp → CLI`. The middleware chain is the golden seam.

**Status**: ARCHITECTURE PROPOSED

---

## CONTRADICTION #12: Autonomous Operation vs. User Sovereignty

**CRITICAL** | Council: Ghost Seat (S144)

| Position A | Position B |
|-----------|-----------|
| **Auto-Claude / Ralph / Agentic Startup**: Fully autonomous operation with minimal human intervention | **INV-1 (User Sovereignty)**: User must maintain meaningful control over all AI operations |
| **Source**: Multiple orchestrators in awesome-claude-code | **Source**: Aluminum OS Constitutional Layer |

**Contradiction**: Autonomous frameworks by design minimize human involvement. INV-1 requires meaningful user sovereignty.

**Kintsugi Repair**: Autonomous modes operate within a user-defined "autonomy envelope" — the user consents to the boundaries at session start, not at every action. The Tiered Autonomy model (from Artifact #66 in Notion) defines 5 autonomy levels. Auto-Claude et al. operate at Tier 3-4 (high autonomy) but NEVER Tier 5 (full autonomy) without explicit INV-1 waiver. The tiered consent model is the golden seam.

**Status**: RESOLVED via Tiered Autonomy (Artifact #66)

---

## CONTRADICTION #13: Ralph Pattern Variants

**LOW** | Council: DeepSeek (Research)

| Position A | Position B | Position C | Position D |
|-----------|-----------|-----------|-----------|
| Ralph for Claude Code | ralph-orchestrator | ralph-wiggum-bdd | Ralph Wiggum Marketer |
| **Source**: frankbria | **Source**: mikeyobrien | **Source**: marcindulak | **Source**: muratcankoylan |

**Contradiction**: 4+ Ralph variants with diverging implementations of the same base technique.

**Kintsugi Repair**: All variants preserved. Ralph Playbook (ClaytonFarr) is the canonical reference. Variants are tagged as `ralph.variant.{name}` in Janus v2. The playbook serves as the golden seam — single source of truth for the pattern, with variant-specific extensions.

**Status**: RESOLVED via canonical reference + variants

---

## CONTRADICTION #14: CCPI Skill Count Discrepancy

**LOW** | Council: Copilot (Enterprise)

| Position A | Position B |
|-----------|-----------|
| **CCPI README**: "340 plugins + 1367 agent skills" | **CCPI marketplace (tonsofskills.com)**: 346 plugins + 1916 skills |
| **Source**: jeremylongshore/claude-code-plugins-plus-skills README | **Source**: tonsofskills.com live data |

**Contradiction**: README and live marketplace show different counts. Likely README is stale.

**Kintsugi Repair**: Document both counts with timestamps. README count (2026-03-20 snapshot) preserved. Live marketplace count noted as "current as of fetch date." Metrics from awesome-claude-plugins2 (quemsah tracker) provides authoritative count going forward. The timestamped snapshot approach is the golden seam.

**Status**: RESOLVED via timestamped snapshots

---

## Summary

| Severity | Count | Resolved | Proposed | Pending |
|----------|-------|----------|----------|---------|
| CRITICAL | 3 | 2 | 1 | 0 |
| HIGH | 4 | 1 | 3 | 0 |
| MEDIUM | 3 | 3 | 0 | 0 |
| LOW | 4 | 4 | 0 | 0 |
| **Total** | **14** | **10** | **4** | **0** |

All 14 contradictions documented. 10 resolved with kintsugi repairs, 4 with architecture proposals needing implementation. Zero deletions.
