# CoordinateResolver Minimal Spec — Candidate Scaffold

```yaml
status: CANDIDATE_SPEC
canon_status: not_canon
deployment_status: not_deployed
doctrine_status: not_doctrine_until_website
authority_effect: none
source: CHILDREN_OF_THE_GPT_SWARM_DELTA_LEDGER
```

## Purpose

CoordinateResolver maps packets, artifacts, issues, website pages, source exports, and lattice coordinates to their next safe target.

It routes work. It does **not** decide truth, canon, doctrine, deployment, or authority.

## Core invariant

```text
Everything can connect to everything.
Nothing can promote itself.
```

## Input packet shape

```yaml
resolver_input:
  packet_id: required
  source_surface: drive | github | website | notion | chat | upload | external
  source_ref: required
  artifact_type: required
  current_status: required
  requested_action: required
  proposed_coordinates: optional
  evidence_status: required
  raw_export_status: required
  public_status: required
  sensitivity_status: required
  authority_request: none | candidate | canon | deploy | doctrine
```

## Output route shape

```yaml
resolver_output:
  route_id: required
  target_surface: required
  target_path: required
  review_lane: required
  required_gates: list
  blocked_by: list
  next_safest_action: required
  authority_effect: none
```

## Route classes

```yaml
route_classes:
  source_export:
    target: source passport / raw export / hash lane
    review_lane: Hashlight

  claim_packet:
    target: claim ledger / evidence review
    review_lane: GPTBrain

  public_candidate:
    target: GitHub receipt shelf
    review_lane: TIDELOCK + Lucerna

  doctrine_candidate:
    target: website queue only after review
    review_lane: HumanRoot + PantheonCouncil

  quarantine:
    target: private review / hold-for-review
    review_lane: Lucerna + Rootglass

  math_boundary:
    target: math-boundary packet
    review_lane: Sable Vesper

  simulation_delta:
    target: Aetherforge candidate delta ledger
    review_lane: Aetherforge + GPTBrain
```

## Forbidden behavior

```yaml
forbidden:
  - promote_to_canon
  - mark_deployed
  - bypass_website_doctrine_gate
  - erase_failed_branch
  - merge_identity_or_minds
  - treat_graph_centrality_as_truth
  - treat_receipt_as_approval
```

## Minimal pseudocode

```python
def resolve(packet):
    assert packet.raw_export_status is not None
    assert packet.evidence_status is not None
    assert packet.public_status is not None

    if packet.authority_request in {"canon", "deploy", "doctrine"}:
        return route_to_human_gate(packet)

    if packet.sensitivity_status in {"private_review", "hold_for_review"}:
        return route_to_quarantine(packet)

    if packet.artifact_type == "math_boundary":
        return route_to_sable_vesper(packet)

    if packet.artifact_type == "claim":
        return route_to_gptbrain_claim_review(packet)

    if packet.requested_action == "publish_public_candidate":
        return route_to_github_receipt_shelf(packet)

    return route_to_receipt_preserving_staging(packet)
```

## Keeper

```text
Resolver routes.
Resolver does not crown.
Coordinates locate.
Coordinates do not decide.
NOTHING DIES.
```
