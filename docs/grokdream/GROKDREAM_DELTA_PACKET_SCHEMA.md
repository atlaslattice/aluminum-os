# GrokDream Delta Packet Schema v0.1

STATUS: CANDIDATE SCHEMA
CANON: NO
DEPLOYMENT: NO
AUTHORITY: NONE
DATE: 2026-06-03

## Purpose

Define a public-safe schema for GrokDream-style delta extraction across chats, Drive docs, Notion pages, Git branches, repo commits, council outputs, and source artifacts.

GrokDream is treated here as a candidate review mode, not an official xAI/Grok product, endorsement, deployment, or canon entity.

## Core idea

GrokDream extracts what changed, why it matters, what receipts support it, what risks appear, and what should happen next.

It is not sovereign. It does not ratify canon. It does not replace GPTDream. It pressures, compares, detects edges, and preserves deltas.

## Delta packet YAML

```yaml
packet_id:
packet_type: grokdream_delta_packet
schema_version: "0.1"
created_at:
created_by:
source_surfaces:
  - surface_type: chat | drive | notion | github | website | council | local_export | other
    source_uri:
    capture_method:
    capture_status:
    receipt_status:

status:
  canon: false
  deployment: false
  authority: none
  public_status: candidate
  review_status: unreviewed

scope:
  time_range:
  branch_or_workspace:
  included_threads:
  excluded_threads:
  known_blindspots:

deltas:
  naming_deltas: []
  architecture_deltas: []
  ontology_deltas: []
  governance_deltas: []
  repo_deltas: []
  product_deltas: []
  risk_deltas: []
  contradiction_deltas: []
  missing_receipt_deltas: []
  opportunity_deltas: []
  blocker_deltas: []
  next_action_deltas: []

12d_scorecard:
  continuity_preservation:
  identity_personhood:
  rights_consent:
  access_eligibility:
  provenance_receipts:
  governance_authority:
  allocation_fairness:
  transfer_exchange:
  settlement_value_routing:
  sovereignty_portability:
  regeneration_ecosystem_health:
  feedback_learning_drift_repair:

claims:
  - claim_id:
    claim_text:
    claim_status: candidate | supported | disputed | blocked | fossil | superseded
    evidence_status: none | weak | partial | strong | verified
    source_refs: []
    missing_receipts: []
    overclaim_risk: low | medium | high
    review_lane:
    release_status:

fossils:
  preserved_failed_branches: []
  supersession_links: []
  unresolved_dissent: []

next_actions:
  - action_id:
    action_type: document | issue | patch | review | export | eval | archive
    target_path:
    owner_lane: human_root | gpt | grok | claude | gemini | codex | pantheon | unknown
    authority_required:
    blocking_receipts:

keeper:
```

## Delta types

### Naming delta
A term changed or emerged.

Example: Aluminum OS → Continuity OS; GPTDream → GrokDream / ContinuityDream split.

### Architecture delta
A system relationship changed.

Example: Fair Resale Rail became a projection of Governed Transfer Rail.

### Governance delta
Authority boundaries changed or became clearer.

Example: Element 145 clarified as non-sovereign aperture.

### Risk delta
A new public, legal, technical, or epistemic risk appeared.

Example: naming collision with Google Aluminium / ALOS.

### Missing receipt delta
A claim lacks source artifact, rendered export, Git commit, or supporting evidence.

Example: JS-heavy website page needs human SingleFile export.

### Contradiction delta
Two outputs disagree or create a tension that must be preserved rather than flattened.

### Next action delta
A newly obvious executable task emerges.

## Review rules

1. Do not delete old branches when extracting deltas.
2. Do not collapse dissent into synthesis prematurely.
3. Do not infer missing website content.
4. Do not claim external affiliation or endorsement.
5. Do not promote candidate deltas to canon.
6. Route doctrine deltas to Pantheon + Dave adjudication.
7. Route code deltas to Codex only after file-scoped issue discipline.
8. Preserve all blocker and missing-receipt states.

## Keeper

GrokDream is useful when it makes change visible faster without claiming authority over the change.
