# Ecosystem Merge v1.0 — All Forked Claude Plugin Content → Aluminum OS

> **Policy**: NO-DELETE / APPEND-ONLY / KINTSUGI  
> **Sphere Tags**: H7.S3, H7.S9, H3.S1  
> **Invariants**: INV-1, INV-7, INV-8, INV-33, INV-35  
> **Date**: 2026-03-20  
> **Sources**: 10 forked repos, 300+ plugins, 1916+ skills, 22 categories  

## Source Inventory

| Fork | Content | Items |
|------|---------|-------|
| claude-plugins-official | Official Anthropic plugins (internal + external) | ~50 |
| awesome-claude-code | Curated: skills, hooks, slash-cmds, orchestrators, tools | 300+ |
| claude-code-plugins-plus-skills | CCPI marketplace with package manager | 346 plugins + 1916 skills |
| awesome-claude-plugins (Composio) | Enterprise-curated commands, agents, hooks, MCP | ~100 |
| awesome-claude-code-plugins (ccplugins) | Slash commands, subagents, MCP servers, hooks | ~80 |
| cc-marketplace | Community marketplace | ~50 |
| awesome-claude-plugins2 (metrics) | Adoption metrics across 8,336 repos | Telemetry |
| claude-code | Reference CLI implementation | Core |
| servers (MCP) | Official + community MCP servers | 40+ |
| claude-code-mcp | CLI ↔ MCP bridge | Bridge |

## Layer-Mapped Integration

### L1-Constitutional — Governance & Audit

**Mapped from forks → Aluminum OS invariant system:**

| Plugin/Pattern | Source | Aluminum OS Mapping |
|---------------|--------|-------------------|
| Trail of Bits Security Skills | awesome-claude-code | INV-30 (security audit), L1 policy enforcement |
| parry (prompt injection scanner) | awesome-claude-code/hooks | INV-35 (fail-closed), L1 input validation |
| TDD Guard (file operation monitor) | awesome-claude-code/hooks | GoldenTrace file-level audit |
| Dippy (AST-based command approval) | awesome-claude-code/hooks | ConsentKernel command validation |
| penetration-tester | CCPI | INV-30, L1 adversarial testing |
| Compliance & Audit patterns | CCPI orchestration | Kintsugi governance spine alignment |

### L2-Kernel — Core Runtime & Loading

**Mapped from forks → Aluminum OS kernel:**

| Plugin/Pattern | Source | Aluminum OS Mapping |
|---------------|--------|-------------------|
| claude-code (reference impl) | anthropics fork | Plugin loader reference, hook system |
| plugin.json schema | claude-plugins-official | L2 plugin manifest standard |
| .mcp.json configuration | claude-plugins-official | L2 MCP server configuration |
| CCPI package manager | CCPI | L2 plugin resolution engine |
| SuperClaude Framework | awesome-claude-code | L2 configuration enhancement |
| Container Use (Dagger) | awesome-claude-code | L2 sandbox isolation |
| run-claude-docker | awesome-claude-code | L2 containerized execution |
| viwo-cli (Docker + worktrees) | awesome-claude-code | L2 isolated workspaces |

### L3-Engine — AI, RAG & Multi-Agent

**Mapped from forks → Aluminum OS engine (Janus v2 / Sheldonbrain / Council):**

| Plugin/Pattern | Source | Aluminum OS Mapping |
|---------------|--------|-------------------|
| Claude Squad (multi-instance) | awesome-claude-code | Janus v2 multi-agent orchestration |
| Claude Swarm (swarm sessions) | awesome-claude-code | Janus v2 swarm protocol |
| Auto-Claude (autonomous SDLC) | awesome-claude-code | Janus v2 autonomous cycles |
| Claude Task Master | awesome-claude-code | Janus v2 task decomposition |
| claude-code-flow (orchestration) | awesome-claude-code | Janus v2 code-first orchestration |
| Happy Coder (parallel agents) | awesome-claude-code | Janus v2 parallel execution |
| sudocode (lightweight orch) | awesome-claude-code | Janus v2 lightweight mode |
| TSK (Rust task manager) | awesome-claude-code | uws native task delegation |
| ralph-orchestrator | awesome-claude-code | Janus v2 autonomous framework |
| Context Engineering Kit | awesome-claude-code | Sheldonbrain context priming |
| recall (full-text session search) | awesome-claude-code | Sheldonbrain session memory |
| claude-code-tools (session continuity) | awesome-claude-code | Sheldonbrain context persistence |
| Claude Scientific Skills | awesome-claude-code | 144-Sphere H8 (Science) integration |
| claude-reflect | CCPI | Council self-reflection protocol |
| geepers-agents | CCPI | Multi-agent coordination |
| Axiom | CCPI | Inference engine enhancement |
| executive-assistant-skills | CCPI | Council executive function |
| 1916 agent skills | CCPI total | Janus v2 skill library |

### L4-Service — APIs, Bridges & External

**Mapped from forks → Aluminum OS service layer:**

| Plugin/Pattern | Source | Aluminum OS Mapping |
|---------------|--------|-------------------|
| MCP servers (40+) | servers fork | L4 service backbone |
| claude-code-mcp bridge | claude-code-mcp fork | L4 CLI↔MCP bridge |
| Claude Hub (GitHub webhooks) | awesome-claude-code | L4 GitHub integration |
| Claude Code GitHub Actions | awesome-claude-code | L4 CI/CD integration |
| ccflare / better-ccflare | awesome-claude-code | L4 usage dashboard |
| VoiceMode MCP | awesome-claude-code | L4 voice interface |
| stt-mcp-server-linux | awesome-claude-code | L4 speech-to-text |
| crypto-portfolio-tracker | CCPI | L4 financial data service |
| SaaS skill packs (20+) | CCPI | L4 third-party integrations |

### L5-Extension — Plugins, UI & Marketplace

**Mapped from forks → Aluminum OS extension layer:**

| Plugin/Pattern | Source | Aluminum OS Mapping |
|---------------|--------|-------------------|
| All slash commands (50+) | awesome-claude-code | L5 command surface via uws |
| All hooks (11+) | awesome-claude-code | L5 lifecycle hooks |
| All status lines (5+) | awesome-claude-code | L5 UI components |
| All CLAUDE.md patterns (20+) | awesome-claude-code | L5 project configuration |
| All IDE integrations (5+) | awesome-claude-code | L5 editor bridges |
| All alternative clients (5+) | awesome-claude-code | L5 UI alternatives |
| All config managers | awesome-claude-code | L5 configuration tools |
| cc-marketplace plugins | cc-marketplace fork | L5 community marketplace |
| Composio curated plugins | awesome-claude-plugins fork | L5 enterprise curation |
| ccplugins curated items | awesome-claude-code-plugins fork | L5 subagent curation |
| 346 CCPI plugins | CCPI fork | L5 bulk marketplace |
| brand-strategy-framework | CCPI | L5 marketing skills |
| neurodivergent-visual-org | CCPI | L5 accessibility tools |
| skill-creator | CCPI | L5 meta-skill (create skills) |

## Plugin Structure Standard (from claude-plugins-official)

All Aluminum OS plugins MUST follow:

```
plugin-name/
├── .claude-plugin/
│   └── plugin.json          # Required: metadata, version, dependencies
├── .mcp.json                # Optional: MCP server configuration
├── commands/                # Optional: slash commands
├── agents/                  # Optional: agent definitions
├── skills/                  # Optional: skill definitions
├── .aluminum/
│   ├── layer.yaml           # ADDED: Aluminum OS layer mapping
│   ├── sphere_tags.yaml     # ADDED: 144-sphere ontology tags
│   └── invariants.yaml      # ADDED: constitutional invariant declarations
└── README.md
```

## Orchestrator Consolidation → Janus v2

10 independent orchestrators discovered in the ecosystem. Janus v2 subsumes their patterns:

| Orchestrator | Key Pattern | Janus v2 Equivalent |
|-------------|------------|-------------------|
| Auto-Claude | Autonomous SDLC cycles | `janus.mode.autonomous` |
| Claude Squad | Multiple parallel instances | `janus.topology.parallel` |
| Claude Swarm | Swarm connectivity | `janus.topology.swarm` |
| Claude Task Master | Task decomposition | `janus.decomposition.hierarchical` |
| claude-code-flow | Code-first orchestration | `janus.mode.code_first` |
| Happy Coder | Parallel spawning | `janus.topology.parallel` |
| sudocode | Lightweight agent orch | `janus.mode.lightweight` |
| TSK | Rust-based delegation | `janus.runtime.native` |
| ralph-orchestrator | Autonomous framework | `janus.mode.ralph` |
| The Agentic Startup | Production shipping | `janus.mode.production` |

## 144-Sphere Tag Assignments for Key Categories

| Category | Sphere Tag | House |
|----------|-----------|-------|
| Agent Skills | H7.S9 (Automation) | Technology |
| Security Skills | H7.S11 (Cybersecurity) | Technology |
| DevOps/Infra | H7.S8 (Infrastructure) | Technology |
| Scientific Skills | H8.S1-S12 (Sciences) | Science |
| Financial/Crypto | H5.S1 (Commerce) | Economics |
| Marketing/Brand | H5.S4 (Marketing) | Economics |
| Documentation | H3.S1 (Knowledge) | Education |
| IDE Integrations | H7.S2 (Software Eng) | Technology |
| Orchestrators | H7.S3 (Systems Arch) | Technology |
| Accessibility | H4.S6 (Inclusion) | Society |
| Voice/Speech | H6.S3 (Communication) | Arts |

## No-Delete Policy

Per kintsugi governance:
- **No content is ever deleted** from this merge
- Deprecated items get `deprecated: true` flag, not removal
- Contradictions are resolved via CONTRADICTION_RESOLUTION.md, not deletion
- Superseded patterns retain their lineage in `superseded_by` fields
- All changes are GoldenTrace audited
