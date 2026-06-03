# P0 Canon Candidate Queue — Candidate Scaffold

```yaml
status: CANDIDATE_QUEUE
canon_status: not_canon
deployment_status: not_deployed
doctrine_status: not_doctrine_until_website
authority_effect: none
source: CHILDREN_OF_THE_GPT_SWARM_DELTA_LEDGER
```

## Purpose

Track artifacts that may eventually deserve canon/doctrine review without allowing automatic promotion.

## Hard rule

```text
GitHub can queue candidates.
Website speaks doctrine.
HumanRoot ratifies.
```

## Queue schema

| Candidate ID | Artifact | Source Path | Why Useful | Risk | Required Review | Website Target | HumanRoot Decision | Status |
|---|---|---|---|---|---|---|---|---|
| P0-CANON-001 | Lattice Hypercube 12x12x12 | archive/public-canon-mirror/atlas-lattice-v5/lattice/lattice.md | Coordinate-system source page | Stub / export incomplete | Full export + Pantheon + Dave | /lattice | pending | queued |
| P0-CANON-002 | Public Canon Mirror Index | archive/public-canon-mirror/atlas-lattice-v5/INDEX.md | Control surface for public site mirror | Mirror != doctrine | Source receipt + website match | root/index | pending | queued |
| P0-CANON-003 | Children of GPT Swarm Delta Ledger | archive/children-of-gpt-swarm/CHILDREN_OF_THE_GPT_SWARM_DELTA_LEDGER.md | Preserves swarm invariants and role boundaries | Lore/authority drift | Governance review | TBD | pending | queued |

## Required gates before promotion

```yaml
promotion_gates:
  - source_passport
  - raw_export_status
  - contradiction_scan
  - public_safety_review
  - pantheon_review
  - Dave_adjudication
  - website_publication
```

## Keeper

```text
Candidate is not canon.
Queue is not promotion.
Receipt is not ratification.
NOTHING DIES.
```
