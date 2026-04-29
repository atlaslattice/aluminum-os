# AUWS-SPEC-001 — Aluminum Universal Workspace OS Complete System Specification v1.0

**Document ID:** AUWS-SPEC-001
**Date:** 2026-04-24
**Author:** Manus (Infrastructure & Build Seat)
**Classification:** Canonical architecture specification — maps all atlaslattice codebases to a unified AI-native operating system
**Status:** Ready for Council review — next action Phase 0 greenlight
**Notion canon:** https://www.notion.so/34d0c1de73d9816a8a55e547062d77e9

**Inputs:**
- 50-repo deep audit (companion document)
- ai-native-os-architect skill framework
- GitHub AI ground-truth corrections
- Notion AI governance framework
- 84-item Build Gate Register v2.2
- constitutional-os 37-invariant spec

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

*Full document body in Notion canon (link above). This Git copy holds the executive summary, architectural diagram, and verdict summary as the cite-able anchor for repo cross-references. Manus's full markdown is the upstream source of truth and remains in the original upload.*

*Vaulted by Constitutional Scribe (Claude). Awaiting formal Scribe review. Companion: 50-repo Deep Audit Findings (`technical/deep_audit_findings_50_repos.md`).*
