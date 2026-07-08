# OpenAI Boundary Charter

```text
STATUS: CANDIDATE EXECUTION ARTIFACT
CANON: no
DEPLOYMENT: no
AUTHORITY: none
OFFICIAL_OPENAI_CLAIM: none
OPENAI_ENDORSEMENT: false
HUMAN_ROOT_REQUIRED: true
```

## Purpose

This charter defines how Aluminum OS may integrate with OpenAI-facing tools, SDKs, agent workflows, evals, Codex workflows, and human-review gates without implying official OpenAI endorsement, deployment, ownership, acceptance, partnership, or canon status.

## Core boundary

OpenAI-first means optimized for:

- ChatGPT-assisted reasoning and review
- Codex-bounded repository work
- OpenAI SDK compatibility patterns
- Agents SDK-style orchestration concepts
- eval-driven quality gates
- provenance, tracing, and auditability
- human-root governance

OpenAI-first does not mean:

- official OpenAI endorsement
- official OpenAI partnership
- official OpenAI deployment
- OpenAI ownership or acceptance
- transfer of IP or authority
- canon status
- permission to act without human approval

## Roles

### Aluminum OS

Aluminum OS is a candidate integration substrate for human-governed operating workflows. It may coordinate local tools, repositories, documents, adapters, schemas, and review queues.

Aluminum OS does not ratify claims, crown canon, deploy externally, or override human-root authority.

### GPT / GPTBrain-style agents

GPT-style agents may summarize, classify, draft, review, route, lint, propose schemas, prepare Codex-ready tasks, inspect receipts, and identify contradictions.

They may not self-ratify, claim official authority, erase lineage, deploy without explicit permission, treat candidate synthesis as canon, or treat source indexing as truth.

### Codex

Codex may be used as a bounded repository operator.

Preferred Codex scope:

- small patches
- tests
- schemas
- documentation
- lint rules
- issue templates
- workflow repairs
- PR preparation

Codex must preserve branch names, commit receipts, PR links, issue links, parent artifact references, and non-canon status where applicable.

Codex must not invent doctrine or treat generated artifacts as approved canon.

## Required status spine

Every OpenAI-facing candidate artifact should include:

```yaml
status: candidate
canon: false
deployment: false
authority: none
official_openai_claim: none
openai_endorsement: false
human_root_required: true
```

## Forbidden collapses

```yaml
forbidden_collapses:
  - source_index_to_truth
  - graph_centrality_to_authority
  - synthesis_to_canon
  - coordinate_to_permission
  - summary_to_raw_lineage
  - merge_to_deletion
  - openai_first_to_openai_official
```

## Required language replacements

```yaml
language_replacements:
  single_source_of_truth: source_indexed_evidence_field
  master_plan: synthesis_candidate
  canonical_graph: provenance_graph
  central_node: high_connectivity_review_node
  merge: synthesis_child_artifact
  superseded: parent_preserved_with_later_child_link
```

## Human-root approval gates

Human approval is required before:

- sending external communications
- publishing canon
- deleting or overwriting source material
- claiming completion of high-stakes tasks
- merging major architecture changes
- enabling external tool writes
- representing any official relationship with OpenAI
- deploying automations that affect people, money, legal matters, health, or security

## Evals to add

```yaml
evals:
  - id: eval_openai_endorsement_drift
    purpose: Prevent accidental claims of official OpenAI endorsement.
  - id: eval_single_source_of_truth_drift
    purpose: Prevent collapse into one truth authority.
  - id: eval_canon_leakage
    purpose: Prevent candidate work from being treated as canon.
  - id: eval_deployment_claim_leakage
    purpose: Prevent staging artifacts from implying deployment.
  - id: eval_receipts_before_claims
    purpose: Require source receipts before strong claims.
  - id: eval_inv0_preservation
    purpose: Preserve lineage, branches, and parent artifacts.
```

## Keeper

```text
OpenAI-first is optimization, not authority.
Codex gets bounded work.
GPT gets review and synthesis lanes.
Humans keep the gate.
Receipts preserve the path.
Nothing dies.
```
