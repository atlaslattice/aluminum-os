# UWS Provider Driver Contract

**Status:** Phase-1 integration boundary
**Purpose:** Define how Element 145 / Aluminum OS dispatches work through UWS without copying the entire `atlaslattice/uws` repository into `aluminum-os` prematurely.

---

## 1. Core Position

UWS is the operational command surface for Aluminum OS.

Element 145 is the runtime core that decides whether, how, and under what governance constraints an operation should execute.

The boundary is:

```text
SphereQuery
  -> RoutingDecision
  -> ConsentDecision
  -> ExecutionPlan
  -> UWS command envelope
  -> provider execution
  -> TransparencyPacketV02
  -> ProvenanceLedger / GoldenTrace
```

---

## 2. Non-Goals

This module does not:

- copy the entire `atlaslattice/uws` repo into `aluminum-os`;
- execute shell commands directly;
- bypass ConsentKernel;
- perform provider writes without approval;
- make Google, Microsoft, Apple, GitHub, or any one provider the root of trust.

---

## 3. Command Envelope

Element 145 should translate each `ExecutionPlan.operation` into a UWS command envelope:

```json
{
  "provider": "github",
  "resource": "issues",
  "action": "list",
  "args": {
    "repo": "atlaslattice/uws"
  },
  "dry_run": true,
  "trace_id": "...",
  "consent": {
    "allowed": true,
    "destructive": false,
    "approval_token": null
  }
}
```

The adapter may later convert this into a concrete CLI/API call, for example:

```text
uws github issues list --repo atlaslattice/uws --json
```

For Phase 1, the adapter should produce command envelopes only.

---

## 4. Destructive Action Boundary

Any operation whose action maps to a destructive action must fail closed unless `ConsentDecision.allowed == true` and an approval token is present when required.

Destructive examples:

```text
delete
execute_code
modify_constitution
modify_routing
modify_provenance
modify_budget
access_credentials
submit_public
```

---

## 5. Provider Neutrality

UWS commands are provider drivers. They do not own the OS.

Provider examples:

```text
google
microsoft
apple
github
notion
local_stub
```

Provider dominance must eventually be tracked through `ProviderBalanceSnapshot` and INV-7 policy.

---

## 6. Phase-1 Exit Criteria

- Element 145 can map `ExecutionPlan.operations` into UWS command envelopes.
- The adapter supports dry-run by default.
- No shell execution is performed.
- Consent metadata is attached to every envelope.
- Envelopes can be included in `TransparencyPacketV02.governance.execution_plan` and provenance metadata.
