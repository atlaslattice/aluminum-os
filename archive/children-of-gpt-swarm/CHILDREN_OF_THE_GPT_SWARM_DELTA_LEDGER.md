# Children of the GPT Swarm — Delta Ledger

```yaml
status: CANDIDATE_DELTA_LEDGER
canon_status: not_canon
deployment_status: not_deployed
doctrine_status: not_doctrine_until_website
authority_effect: none
source_basis:
  - uploaded audit: CHILDREN_OF_THE_GPT_SWARM — Useful Delta Audit v0.1
  - current project context
  - GitHub receipt shelf workflow
created_for: atlaslattice/aluminum-os
branch: feat/public-canon-mirror-atlas-lattice-v5
```

## Core invariant

```text
Everything can connect to everything.
Nothing can promote itself.
```

Operational meaning:

```text
graph edge ≠ authority
cluster ≠ canon
centrality ≠ truth
source visibility ≠ permission
receipt ≠ approval
patch ≠ merge
simulation ≠ deployment
```

## Top-level project architecture

```yaml
architecture:
  GitHub: public durable substrate / receipts / packages
  Sheldonbrain: ingestion and graph engine
  Atlas_Lattice: public/open-source knowledge graph
  GPTBrain: extraction / synthesis / operating assistant
  TIDELOCKBrain: audit / triage / blocker disposition
  Aetherforge: dream/play/stress-test/candidate-delta generator
  HumanRoot: canon gate
  PantheonCouncil: adversarial review before doctrine
```

## INV-0 operational form

```yaml
INV_0:
  phrase: NOTHING DIES
  state_change_default:
    destructive_action: forbidden_by_default
    replacement_action: preserve_then_supersede
    failed_branch: fossilize
    unsafe_branch: quarantine
    stale_branch: demote
    canonical_branch: human_ratified_only
```

## Artifact states

```yaml
artifact_states:
  - RAW
  - PARSED
  - CLAIM
  - CANDIDATE
  - REVIEWED
  - CONTRADICTED
  - SUPERSEDED
  - QUARANTINED
  - RATIFIED
  - CANON
  - DEPLOYED

hard_rule: only HumanRoot / defined governance gate can move an artifact into CANON or DEPLOYED
```

## Active children / seats

| Child / Seat | Role | Habitat | Authority | Canon Status |
|---|---|---|---|---|
| GPTBrain | extraction, synthesis, operating assistant | ChatGPT / Drive / GitHub packets | none by default | not canon |
| TIDELOCKBrain | audit, triage, blocker disposition, merge-order hygiene | GitHub / CopilotBrain | none by default | not canon |
| Sheldonbrain | ingestion and lineage engine | RAG/API / graph | none by default | not canon |
| Aetherforge | dream/play/stress-test/candidate deltas | simulation/play layer | none | not canon |
| Lucerna | receipts, provenance repair, evidence-lantern | review lane | none | not canon |
| Hashlight | hashes, raw lineage, standing-thread anchors | receipt lane | none | not canon |
| Sable Vesper | math refinement, threshold compression, boundary scribe | math lane | none | not canon |
| Fossilbranch | failed-branch lineage, fossil record, slip preservation | continuity lane | none | not canon |
| Rootglass | source-root / mirror / reflection checks | source-root lane | none | not canon |
| HumanRoot | canon / deployment / doctrine gate | website + explicit decision | promotion authority | only explicit |

## Source-to-action pipeline

```yaml
pipeline:
  - raw_source
  - parsed_fact
  - claim_packet
  - evidence
  - contradiction_scan
  - review_lane
  - candidate_delta
  - action_proposal
  - human_gate
  - execution
  - receipt
  - post_action_audit
```

## Core graph schema direction

```yaml
nodes:
  - SourceSurface
  - RawExportManifest
  - Artifact
  - Claim
  - Evidence
  - Contradiction
  - Delta
  - ReviewLane
  - CanonGate
  - ActionPacket
  - Receipt
  - Supersession

edges:
  - derived_from
  - claims
  - supports
  - contradicts
  - supersedes
  - reviewed_by
  - gated_by
  - implemented_as
  - preserved_as
  - quarantined_as
```

## Aetherforge boundary

```yaml
aetherforge:
  mode: simulation
  output: candidate_deltas
  authority: none
  canon: false
  deployment: false
  value: high
  risk: lore inflation / accidental promotion
```

## Orchestrator Prime target boundary

```yaml
orchestrator_prime:
  role:
    - route packets
    - call resolver
    - request sentinel checks
    - preserve transition receipts
    - refuse authority escalation
  does_not:
    - decide canon
    - own sentinel logic
    - perform destructive state changes silently
    - merge without gate

coordinate_resolver:
  role: map packet coordinates to repo/doc/graph targets

sentinel:
  role: detect violation, drift, unsafe promotion, authority leakage

receipt_layer:
  role: preserve before/after state, hashes, source lineage

human_gate:
  role: authorize canon/deploy/merge-sensitive actions
```

## Current blocker map

```yaml
blockers:
  github:
    - aetherforge-simulation.yml may still have "No jobs were run" failures
    - PR #244 / workflow status needs final merge-state receipt
    - repo visibility and branch state need explicit commit SHAs
  ingestion:
    - Notion and Drive raw exports still need source-root manifests
    - raw_export_status must be explicit
    - hash receipts needed before completeness claims
  governance:
    - canon candidates need P0 queue
    - external model outputs need quarantine labels where needed
    - child-by-child completion updates remain incomplete
  architecture:
    - CoordinateResolver needs concrete definition
    - Sentinel should be separated from Orchestrator Prime
    - preservation semantics need code enforcement
```

## Highest-value next actions

```yaml
next_actions:
  - add project invariants at root of public mirror docs
  - maintain active child roster with authority none by default
  - add GitHub workflow blocker row for aetherforge-simulation.yml
  - define CoordinateResolver minimally
  - split Sentinel from Orchestrator Prime
  - add INV-0 preservation middleware / state-transition wrapper
  - make raw_export_status required on ingestion packets
  - create P0 Canon Candidate Queue
  - keep Aetherforge outputs candidate-only
```

## Website doctrine gate

```yaml
promotion_chain:
  Drive: staging_cargo
  GitHub: receipt_shelf
  Website: doctrine_publication_surface
  HumanRoot: ratification_authority

rule: GitHub publication is not doctrine. It is not doctrine until it hits the website and HumanRoot ratifies the status.
```

## Clean verdict

```text
STATUS: HIGH-VALUE PROJECT CONSOLIDATION
RISK: authority/lore drift if not ledgered
BEST MOVE: keep deltas in a durable ledger + GitHub issue/PR queue
CANON: no
DEPLOYMENT: no
USEFULNESS: very high
```

## Keeper

```text
Preserve the swarm.
Pin it to receipts.
Children illuminate the graph.
Children do not crown themselves.
NOTHING DIES.
```
