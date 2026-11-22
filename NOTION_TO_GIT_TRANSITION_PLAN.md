---
status: Active Planning Document
owner: Daavud Sheldon (Convenor)
primary_auditor: Grok (S3 + Root Substrate)
date: 2026-05-30
branch: feature/grokbrain-integration
---

# Notion → Git Transition Plan

**Objective**: Move the living canon, governance, ontology development, and active intelligence work from Notion (and the Manus-hosted website) to the GitHub repository as the primary, Grok-native source of truth — with Grok operating as the root intelligence layer.

This plan is a direct response to two realities:
1. The declared canon (the website) is currently inaccessible and financially hostage.
2. The explicit directive to put Grok at the root.

All changes will be additive and respect INV-17 (Zero Erasure).

---

## 1. Current State Assessment

| System              | Role                          | Accessibility | Health     | Notes |
|---------------------|-------------------------------|---------------|------------|-------|
| Notion              | Primary workspace & memory    | Good (for user) | Unknown   | Heavy use for governance, tasks, ontology work |
| Manus Website       | Declared Canon / Public Face  | Blocked ($1000) | Stale (1 month+) | Currently the "official" source of truth |
| GitHub Repo (docs/) | Working development canon     | Excellent     | More current | Multiple copies, not yet declared primary |
| Local (AI X1)       | Personal development node     | Full          | New       | Where this Grok session is primarily operating |

**Key Finding**: There is a dangerous mismatch between where the canon *lives* and where it is *actually usable and evolving*.

---

## 2. Transition Principles

- **Grok as Root Intelligence**: Grok (this runtime + future local instances on the AI X1) is the primary reasoning, consolidation, and evolution engine.
- **Git as Source of Truth**: The repository becomes the single, versioned, auditable home for all canonical knowledge.
- **Zero Erasure (INV-17)**: Nothing is deleted. Notion and the old website remain as historical archives with clear pointers.
- **Local-First on AI X1**: As much as possible, the primary development loop should run locally on your Minisforum with GitHub as the sync layer.
- **Progressive Migration**: Move the highest-leverage, highest-risk items first (core ontology, governance, active flywheel work).

---

## 3. Phased Migration Plan

### Phase 0: Foundation & Inventory (Immediate)
- [ ] Full export of relevant Notion workspaces (databases, pages, linked databases related to governance, ontology, 12x12, flywheel, SHELDONBRAIN, etc.).
- [ ] Create `notion-archive/` folder in the repo with dated exports + manifest.
- [ ] Inventory of all active Notion content that should be considered "canon" vs working notes.
- [ ] Declare `docs/architecture/SOURCE_OF_TRUTH.md` (and supporting docs) as the temporary working canon with a clear banner.
- [ ] Add this transition plan to the canon.

**Owner**: User + Grok (via this session)

### Phase 1: Core Canon Migration (High Priority)
Migrate the following into clean, version-controlled Markdown/YAML in the repo:

- The full 12x12 Lattice (Houses, Spheres, Sub-spheres)
- All 12 VIP Elements + descriptions
- Current Pantheon Council structure and archetypes
- All ratified Invariants and Doctrines
- Key governance documents currently living in Notion
- Any active 12-layer flywheel or Riemann S-curve modeling work

**Target Location**: `docs/ontology/`, `docs/governance/`, `docs/flywheel/`

**Grok Role**: Perform initial structuring, deduplication, and epistemic labeling during import.

### Phase 2: Active Work Migration
- Move ongoing project management, task tracking, and decision logs from Notion into GitHub Issues + Projects (or a lightweight local-first system synced to Git).
- Begin running the 12-layer flywheel development process primarily through Grok + Git.
- Establish a daily/weekly Grok-native review & consolidation ritual on the AI X1 that writes back to the repo.

### Phase 3: Tooling & Local Sovereignty
- Set up strong local workflows on the Minisforum AI X1 (Obsidian + Git plugin, or custom Grok-powered tools, or both).
- Make the GitHub MCP + local Grok CLI the primary interface for interacting with the canon.
- Create scripts/agents that can pull from Notion as a secondary source during transition (if API access remains).
- Design the first versions of Continuous Parser v1 + Epistemic Labeling that run locally against the Git repo.

### Phase 4: Deprecation & Archive Strategy
- Once core canon has lived in Git for 30+ days with active use, add formal deprecation notices to the old Notion workspace and Manus site.
- Keep both as read-only archives with clear "This has moved to GitHub" pointers.
- Update all internal references across the repo.

### Phase 5: Website Reconciliation (Future)
- Once the $1000 Manus situation is resolved, the website becomes a **generated read-only mirror** of the GitHub canon (not the source).
- Long-term: Explore fully static or Grok-generated site options that remove the Manus dependency.

---

## 4. Risk Mitigation

| Risk                          | Mitigation Strategy                              | Owner |
|-------------------------------|--------------------------------------------------|-------|
| Loss of Notion access         | Export everything critical in Phase 0            | User |
| User resistance / habit       | Keep Notion as secondary workspace during transition | User + Grok |
| Over-migration too fast       | Prioritize by "if this disappeared tomorrow, how bad?" | Grok |
| Website remains the "official" canon in people's minds | Clear banners + repeated communication in all documents | Grok |
| Complexity explosion in Git   | Enforce strict "one source of truth" rule inside the repo | Grok |

---

## 5. Success Criteria

- The majority of active ontology and governance work is happening in the GitHub repo.
- Grok sessions (local on AI X1 or via this runtime) are the primary way new canonical content is proposed, reviewed, and integrated.
- A new contributor (or future self) can understand the current state of the system by cloning the repo + reading `SOURCE_OF_TRUTH.md` + this transition plan.
- The Manus website is no longer a single point of failure or financial hostage.
- The 12-layer flywheel and advanced models are being developed inside the repo with Grok as a first-class participant.

---

## 6. Immediate Next Steps (This Week)

1. User performs full critical Notion export.
2. Grok + user do a joint inventory session (can be done here or locally on the X1).
3. Create the first version of `docs/ontology/12x12-lattice.md` pulled from the best current sources (Notion + existing repo docs).
4. Add a prominent banner to `SOURCE_OF_TRUTH.md` declaring the transition in progress.
5. Decide on primary local tooling for the AI X1 (Obsidian + Git? Custom scripts? Something else?).

---

*This document lives in the repo and will be updated as the transition progresses. It is the current authoritative plan for shifting from Notion-centric to Git + Grok-centric operations.*
