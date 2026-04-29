# Domain Repository Index

This directory contains the consolidation manifest for all 200+ repos in the `atlaslattice` GitHub organization.

## Strategy

Rather than absorbing all domain repos into the monorepo (which would bloat it unnecessarily), we use a **REFERENCE** strategy:

1. **Core repos** (17) → Already absorbed into `aluminum-os` monorepo
2. **Domain/swarm repos** (91) → Indexed via `domain_repo_index.yaml` with House/Sphere mapping
3. **Forks** (59) → Reference only (upstream maintained)
4. **Empty repos** (6) → Archived or pending initialization

## How It Works

Each domain repo has a lattice position (House + Sphere) assigned in `domain_repo_index.yaml`. This allows:
- The lattice router to find relevant repos when a query matches their domain
- The SNRS to classify incoming requests and route to the appropriate domain app
- The governance layer to track which repos implement which ethical/regulatory functions

## File Structure

```
domain_repos/
├── README.md                    ← This file
├── domain_repo_index.yaml       ← 91 domain repos with House/Sphere mapping
└── core_repo_status.yaml        ← 17 core repos absorption status
```
