# Aluminum OS

> An open-source AI-native workspace substrate: one safe, auditable command surface across productivity ecosystems.

Aluminum OS gives humans and AI agents a unified way to operate across Google Workspace, Microsoft 365, Apple/iCloud, Android, Chrome, GitHub, Notion, and future tools.

The immediate wedge is practical: **one command surface, normalized JSON, explicit consent, and auditable operations.**

The long-term vision is larger: identity, memory, governance, provenance, and multi-agent orchestration as a coherent operating substrate for AI-native work.

---

## What This Is

Aluminum OS is the umbrella architecture and reference implementation for an AI-native workspace layer.

It is organized around four layers:

```text
Human / AI intent
        |
        v
alum / uws command surface
        |
        v
Aluminum substrate: identity, memory, governance, provenance, agent runtime
        |
        v
Provider drivers: Google Workspace, Microsoft 365, Apple/iCloud, Android, Chrome, GitHub, Notion, Slack, Linear, and future plugins
```

### Current operational core

The current executable command-surface work lives in [`atlaslattice/uws`](https://github.com/atlaslattice/uws).

`uws` is the Universal Workspace CLI: a schema-driven, JSON-first interface designed for both humans and AI agents. It is the near-term build path for Aluminum.

### Current architecture anchor

Start here:

- [`docs/architecture/SOURCE_OF_TRUTH.md`](docs/architecture/SOURCE_OF_TRUTH.md) — current repo doctrine and source-of-truth map
- [`enterprise/Aluminum_OS_Enterprise_Specification_v1.0.md`](enterprise/Aluminum_OS_Enterprise_Specification_v1.0.md) — enterprise architecture specification

---

## Core Thesis

Traditional operating systems abstract hardware.

Aluminum abstracts **workspace ecosystems**.

Just as kernel drivers let software operate across different hardware devices, Aluminum provider drivers let humans and AI agents operate across Google, Microsoft, Apple, Android, Chrome, GitHub, Notion, and future systems without rewriting workflows for every silo.

The AI agent becomes the shell.
The user's intent becomes the program.
Provider drivers become device drivers.
Governance and provenance become the safety layer.

---

## Product Shape

The intended user-facing command surface is `alum`:

```bash
alum mail list --provider all
alum mail send --to alice@example.com --confirm
alum calendar create --ai "schedule a team sync tomorrow at 10"
alum drive search "Q1 budget" --provider all
alum sync contacts --from apple --to google
alum ai "summarize my unread email and today's meetings"
```

Under the hood, early `alum` commands should route through `uws` until Aluminum-native provider drivers are stable.

---

## Key Principles

- **Useful before mythic.** Ship the thing people can use first.
- **One command surface.** Agents and humans should not need different APIs for every provider.
- **JSON-first.** Every operation should be machine-readable and automation-safe.
- **Consent-aware.** Writes, shares, deletes, and external sends should be explicit and auditable.
- **Provenance-native.** Important actions should leave a trace: who/what acted, on what data, under what authority.
- **Provider-neutral.** Google, Microsoft, Apple, and others are drivers, not prisons.
- **Agent-ready.** Manus, Claude, Gemini, GPT, Copilot, and future agents should be able to operate through stable contracts.

---

## Repository Roles

This repository, `aluminum-os`, is the umbrella repo for:

- architecture;
- governance and constitutional substrate;
- provenance and audit design;
- memory substrate design;
- agent runtime design;
- product roadmap;
- reference packages and prototypes.

Related repositories:

- [`atlaslattice/uws`](https://github.com/atlaslattice/uws) — current Universal Workspace CLI / command-surface implementation.
- [`atlaslattice/manus-artifacts`](https://github.com/atlaslattice/manus-artifacts) — artifact archive and staging area.
- `aluminum-os-v3`, `constitutional-os`, and related repos — candidate source-material repos to reconcile into the canonical architecture.

---

## Royalty Runtime

Royalty Runtime remains valuable, but it is now treated as a subsystem or adjacent product line rather than the entire public identity of Aluminum OS.

Its core idea is still important:

> Enforcement systems get forked. Measurement systems get embedded.

In the Aluminum architecture, Royalty Runtime fits naturally under provenance, attribution, dependency intelligence, and open-source value measurement.

Suggested future location:

```text
packages/
  royalty-runtime/
```

---

## Near-Term Build Path

### Phase 0 — Stabilize

- Maintain a source-of-truth map.
- Inventory artifacts and specs.
- Define canonical repo roles.
- Open implementation issues with clear acceptance criteria.

### Phase 1 — Ship `uws`

- Provider driver interface.
- Google/Microsoft/Apple command normalization.
- Safe write confirmations.
- Audit logs.
- Agent skill files.

### Phase 2 — Introduce `alum`

- Provider-agnostic commands.
- Friendly user-facing grammar.
- Routing through `uws` where possible.
- First demo: mail/calendar/drive across at least two providers.

### Phase 3 — Add substrate services

- Agent Control Plane.
- Governance engine.
- Provenance graph.
- Memory substrate.
- Consent and policy enforcement.

### Phase 4 — Long-term OS track

- Bare-metal and microkernel research.
- Formal verification.
- Capability-native runtime.
- Hardware-aware AI execution.

The bare-metal track is real research, but it should not block the middleware/product path.

---

## Status

Current status: **architecture consolidation and executable command-surface stabilization.**

This repository contains important specifications and source material. The immediately buildable implementation path runs through `uws`, then `alum`, then substrate services.

---

## License

MIT unless otherwise specified in subdirectories.

---

## Working Doctrine

Build the thing people can use first.

The universal command surface is the wedge. Governance, provenance, memory, and agent orchestration make it defensible. Bare-metal OS work is the moonshot track, not the blocker.
