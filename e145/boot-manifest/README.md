# Boot Manifest Runtime (M176-M178)

## Modules
- **M176** — Boot Manifest Runtime: Lightweight manifest-of-references (~1-2K tokens)
  that every Pantheon seat boots from. Fetch-on-demand, not preload.
- **M177** — Pre-Session Research Queue: Ordered fetch list derived from manifest.
  Prioritized by sphere relevance to current task.
- **M178** — Cross-Instance State Synchronizer: Ensures instance state symmetry
  across Council seats per D-124.

## Key Invariant
- **INV-43** — Boot Manifest Freshness: 24h max staleness, dual-source
  (Notion primary, Git fallback)

## Key Doctrines
- **D-122** — Manifest-as-Boot-Payload: Binding only after M176 DELIVERED
- **D-123** — Platform Split: Notion for prose/governance, Git for structured data/code
- **D-124** — Instance Interchangeability: State symmetry, not identity

## Boot Protocol v2 Fallback
Until M176 reaches DELIVERED status, seats boot via Boot Protocol v2
(direct Notion page fetch + Git registry pull). D-122 becomes binding
only after M176 is production-validated.

---
*Element 145 — Boot Manifest — Build Plan v3.14+*
