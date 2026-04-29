# Canonical Repository Hierarchy

> **Doctrine D-84 (Filesystem-as-Ontology):** The directory structure IS the ontology.
> Numbering locked from Build Plan v3.14 onward.

This document defines the authoritative source-of-truth for every artifact in the Atlas Lattice / Aluminum OS ecosystem. When the same artifact appears in multiple locations, the **canonical** location governs.

---

## Tier 1: Canonical Repositories (Source of Truth)

| Repository | URL | Governs |
|---|---|---|
| **aluminum-os** | `github.com/atlaslattice/aluminum-os` | Master ontology (12×12+1), all 144 sphere manifests, registries, doctrines, ORC documents, council reviews, Element 145 core |
| **element-145** | `github.com/atlaslattice/element-145` | Installable Python package: LCP, SHUGS operator, integrations, agent scaffolds, sprint modules |
| **orcs-repo** | `github.com/atlaslattice/orcs-repo` | ORC governance documents, Pantheon Council reviews, Build Plan versioning |

## Tier 2: Component Repositories (Deployable Services)

| Repository | URL | Governs | Upstream Canonical |
|---|---|---|---|
| **sheldongemini-GPI** | `github.com/atlaslattice/sheldongemini-GPI` | Sheldon Gemini chat frontend (React + Gemini 2.5 Flash) | element-145 (ontology), aluminum-os (scaffolds) |
| **sheldonbrain-rag-api** | `github.com/atlaslattice/sheldonbrain-rag-api` | Pinecone RAG backend (Cloud Run) | element-145 (classifier), aluminum-os (ontology) |
| **aluminum-os-v3** | `github.com/atlaslattice/aluminum-os-v3` | Rust implementations: Pantheon, Noosphere, Sheldonbrain, Manus Core | aluminum-os (spec), element-145 (ontology) |

## Tier 3: Archive / Reference Repositories

| Repository | URL | Status | Notes |
|---|---|---|---|
| **noosphere-archive** | `github.com/atlaslattice/noosphere-archive` | Archive | Pre-lattice Noosphere concept. Superseded by element-145 synthesizer. |
| **noosphere-defense** | `github.com/atlaslattice/noosphere-defense` | Archive | Defense-domain Noosphere variant. Content migrated to H06 (Defense + Security). |

---

## Duplication Resolution Rules

When the same artifact exists in multiple repos, these rules determine which governs:

1. **Ontology files** (lattice_ontology.yaml, 12x12_matrix.yaml, sphere manifests): `aluminum-os` governs. All other repos consume via import or copy.

2. **Python code** (LCP, SHUGS, classifier, bridge, synthesizer): `element-145` governs. The copy in `aluminum-os/element-145/` is a snapshot; `element-145` repo is the development head.

3. **ORC documents**: `orcs-repo` governs for governance text. `aluminum-os/orcs/` is a distribution copy.

4. **Council reviews**: `orcs-repo/council-reviews/` governs. `aluminum-os/council-reviews/` is a distribution copy.

5. **Rust implementations**: `aluminum-os-v3` governs. These are not duplicated elsewhere.

6. **Frontend code**: `sheldongemini-GPI` governs. Not duplicated.

7. **RAG backend**: `sheldonbrain-rag-api` governs. Not duplicated.

---

## Cross-Repo Dependency Graph

```
aluminum-os (master ontology)
├── element-145 (installable package, consumes ontology)
│   ├── sheldongemini-GPI (frontend, consumes element-145 API)
│   ├── sheldonbrain-rag-api (RAG backend, consumes element-145 classifier)
│   └── aluminum-os-v3 (Rust services, consumes element-145 spec)
└── orcs-repo (governance, references aluminum-os structure)
```

---

## Fork Repositories (~190)

All fork repositories under `atlaslattice` are **non-canonical reference copies** of upstream open-source projects. They exist for:
- Dependency pinning (specific versions used by Aluminum OS components)
- Potential future contribution (patches to upstream)
- Research reference (papers, tools, datasets)

Forks are **never** the source of truth for any Aluminum OS artifact. They should be archived when no longer actively referenced.

---

## Version Synchronization

| Artifact | Canonical Version | Lock Mechanism |
|---|---|---|
| Lattice ontology | v3.14 | SHA-256 hash in `ontology-lock.json` (D-89) |
| Element 145 package | v0.1.0-CANDIDATE-2 | `pyproject.toml` version field |
| Build Plan | v3.14 | `orcs-repo/build-plan/` directory |
| ORC numbering | ORC-012 through ORC-036 | Sequential, append-only |
| Doctrine numbering | D-01 through D-89 | Sequential, append-only |

---

*Last updated: 2026-04-29. Maintained by Manus S7 per Convenor delegation.*
