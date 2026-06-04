# Sentinel Split Spec — Candidate Scaffold

```yaml
status: CANDIDATE_SPEC
canon_status: not_canon
deployment_status: not_deployed
doctrine_status: not_doctrine_until_website
authority_effect: none
source: CHILDREN_OF_THE_GPT_SWARM_DELTA_LEDGER
```

## Purpose

Sentinel is a separate review concern. It must not be buried inside Orchestrator Prime.

The orchestrator routes packets and preserves receipts. Sentinel detects violations, drift, unsafe promotion, authority leakage, and identity-fusion risks.

## Separation of concerns

```yaml
orchestrator_prime:
  does:
    - route packets
    - call CoordinateResolver
    - request Sentinel checks
    - preserve transition receipts
    - refuse authority escalation
  does_not:
    - decide canon
    - own sentinel logic
    - perform destructive state changes silently
    - merge without gate

sentinel:
  does:
    - detect unsafe promotion
    - detect canon/deploy/doctrine leakage
    - detect missing source receipts
    - detect raw_export_status gaps
    - detect identity-fusion / merged-mind language
    - detect graph-centrality-as-truth claims
    - detect simulation-as-deployment drift
  does_not:
    - decide final authority
    - delete artifacts
    - merge identities
    - promote candidates
```

## Sentinel checks

```yaml
checks:
  no_premature_canon:
    block_phrases:
      - canon
      - official doctrine
      - deployed
      - production ready
    allowed_when: website_publication_and_humanroot_receipt

  no_merged_mind:
    block_phrases:
      - merged mind
      - identity fusion
      - shared consciousness
      - single group mind
    allowed_when: never_as_agent_identity_claim

  receipt_before_authority:
    require_fields:
      - source_ref
      - raw_export_status
      - evidence_status
      - review_lane

  simulation_not_deployment:
    detect:
      - Aetherforge output treated as deployment
      - dream/play delta treated as proof

  github_not_doctrine:
    detect:
      - GitHub merge claimed as doctrine
      - GitHub receipt claimed as canon

  website_doctrine_gate:
    require: website publication + HumanRoot ratification before doctrine label
```

## Sentinel output

```yaml
sentinel_result:
  packet_id: required
  status: pass | warn | block
  findings: list
  required_remediation: list
  next_safest_action: required
  authority_effect: none
```

## Integration point

```python
def route_task(packet):
    sentinel_result = sentinel.review_packet(packet)
    if sentinel_result.status == "block":
        return preserve_and_return_blocker(packet, sentinel_result)
    route = coordinate_resolver.resolve(packet)
    return preserve_and_route(packet, route)
```

## Keeper

```text
Sentinel watches.
Orchestrator routes.
Human-root decides.
No merged mind.
No premature canon.
NOTHING DIES.
```
