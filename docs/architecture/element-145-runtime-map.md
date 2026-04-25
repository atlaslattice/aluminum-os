# Element 145 Runtime Map

**Status:** Candidate architecture map
**Purpose:** Map the Element 145 Phase-0 scaffold to AUWS-SPEC-001, Aluminum OS layers, and Phase 1 implementation gates.

---

## 1. Executive Summary

Element 145 is the L4 Service Orchestration Layer of Aluminum Universal Workspace OS.

AUWS-SPEC-001 defines Element 145 as the init process / service orchestration layer that bootstraps and coordinates the kernel, engine, extension, budget enforcement, classifier, and provenance systems.

The uploaded Phase-0 scaffold provides a real first implementation surface:

```text
services/element-145/
  element145/
    api/
    classifier/
    observability/
    provenance/
    proto/
    router/
    services/
    transparency/
    utils/
  config/
  tests/
  Dockerfile
  Makefile
  pyproject.toml
```

This map explains how those modules fit into Aluminum OS.

---

## 2. Layer Placement

```text
L1 Constitutional Layer
  -> constitutional-os, ORCS, invariants, permission surface

L2 Kernel Layer
  -> ConsentKernel, state, 144-sphere namespace

L3 Engine Layer
  -> uws, Constitutional Router, Janus v2, provider dispatch

L4 Service Orchestration Layer
  -> Element 145 runtime

L5 Extension Layer
  -> MCP, skills, plugins, integrations

L6 Application Layer
  -> user-facing agents and dashboards

L7 Device Mesh Layer
  -> cross-platform state and hardware/device integration
```

Element 145 sits between L3 and L5. It receives classified/normalized operations, applies policy gates, routes work, records provenance, emits TransparencyPackets, and exposes service APIs.

---

## 3. Scaffold-to-Layer Mapping

| Scaffold Module | OS Layer | Role |
|---|---|---|
| `element145/router/core.py` | L4 | Central lifecycle: trace ID, classify, gate, dispatch, ledger, transparency |
| `element145/router/shadow.py` | L4 / Validation | Shadow Mode for passive observation and ≥48h validation |
| `element145/router/simulation.py` | L4 / Validation | Simulation Mode for mandatory scenario testing |
| `element145/classifier/stub.py` | L2/L4 bridge | Initial classifier; later upgraded to House/Sphere + epistemic/safety states |
| `element145/provenance/ledger.py` | Cross-cutting | JSONL provenance ledger seed; later GoldenTrace/Royalty Runtime alignment |
| `element145/transparency/packet.py` | Cross-cutting | TransparencyPacket emitter and fingerprint verification |
| `element145/api/routes.py` | L4/L6 boundary | HTTP control surface for routing, classification, ledger, transparency, stats, admin modes |
| `element145/api/schemas.py` | L4 contracts | API request/response schemas |
| `element145/services/definitions.py` | L4/L5 bridge | Static service registry; later dynamic MCP/skill/service registration |
| `element145/proto/element145.proto` | L3/L4 IPC | Proto contract; future gRPC interface for router/service communication |
| `element145/observability/*` | Cross-cutting | Logs, metrics, p50/p99 readiness |
| `config/settings.py` | L4 runtime config | Environment-based runtime settings |
| `tests/*` | Phase 1/1.5 validation | Scaffold test suite for classifier, router, ledger, API, modes, transparency |

---

## 4. Required Upgrades Against AUWS-SPEC-001

The current scaffold is a strong Phase-0 base, but it is not yet Phase-1 complete.

### 4.1 Classifier upgrade

Current:

```text
Rule-based domain classifier: infrastructure, provenance, transparency, compliance, ecological, identity, resource_allocation, audit, general
```

Required:

```text
House/Sphere classifier
Epistemic State classifier: Known | Uncertain | Unknown | Contested
Safety State classifier: Safe | Sensitive | Dangerous | Constitutional
```

Output should become a `RoutingDecision` object.

### 4.2 TransparencyPacket v0.2

Current:

```text
trace_id
classification
decision_path
elapsed_ms
fingerprint
```

Required additions:

```text
house
sphere
epistemic_state
safety_state
provider_weights
routing_reason
policy_checks
cost_estimate
approval_token
provenance.execution_hash
signature_scheme
hash_scheme
```

### 4.3 Provenance ledger hardening

Current:

```text
in-memory list + optional local JSONL append
```

Required:

```text
append-only JSONL with reload on startup
hash chain / GoldenTrace compatibility
export JSON + CSV
tamper detection
later PostgreSQL/Royalty Runtime alignment
```

### 4.4 ConsentKernel / destructive action gates

Current:

```text
No explicit consent policy engine
```

Required:

```text
Permission Surface Matrix
Destructive Action Policy with 11 prohibited action types
HITL approval tokens
ConsentKernel preflight before write/destructive actions
```

### 4.5 Provider / model dispatch

Current:

```text
_default_stub handler
```

Required:

```text
LiteLLM or equivalent model router
minimum 3 providers
INV-7 provider percentage tracking
fallback / graceful degradation
budget enforcement
```

### 4.6 Service registry

Current:

```text
Static registry exists but router does not resolve through it
```

Required:

```text
Router dispatch resolves through ServiceRegistry
service health checks
MCP/skill registration path
handler interface contract
```

---

## 5. Phase 1 Data Models To Add

### 5.1 SphereQuery

```python
class SphereQuery(BaseModel):
    query_id: str
    raw_input: str | dict
    house: int | None
    sphere: int | None
    metadata: dict
```

### 5.2 RoutingDecision

```python
class RoutingDecision(BaseModel):
    trace_id: str
    house: int
    sphere: int
    epistemic_state: str
    safety_state: str
    selected_path: str
    selected_providers: list[str]
    provider_weights: dict[str, float]
    policy_checks: list[dict]
    budget_tier: str
    requires_human_approval: bool
```

### 5.3 TransparencyPacketV02

```python
class TransparencyPacketV02(BaseModel):
    packet_id: str
    trace_id: str
    timestamp: float
    routing: dict
    governance: dict
    provenance: dict
    costs: dict
    verification: dict
```

### 5.4 ConsentDecision

```python
class ConsentDecision(BaseModel):
    trace_id: str
    action_type: str
    destructive: bool
    allowed: bool
    reason: str
    approval_token: str | None
```

---

## 6. Build-Gate Alignment

Element 145 Phase 0 must support the following AUWS gates:

| Gate | Current Scaffold Status | Required Next Work |
|---|---|---|
| Router skeleton | Present | Wire service registry + provider dispatcher |
| Classifier stub | Present | Upgrade to two-pass classifier |
| TransparencyPacket emitter | Present | Upgrade to v0.2 fields |
| Provenance ledger | Present | Add reload, hash chain, export |
| Shadow Mode | Present | Define 48h validation metrics |
| Simulation Mode | Present | Add 5 mandatory scenarios |
| Observability | Present | Expose p50/p99 and health checks |
| Consent / permission surface | Missing | Add ConsentKernel preflight |
| Budget enforcement | Missing | Add 6-tier budget model |
| Provider routing | Missing | Add ≥3 provider model routing |
| INV-7 enforcement | Missing | Track provider percentages |

---

## 7. Recommended Repository Placement

For Phase 0, use:

```text
aluminum-os/services/element-145/
```

Do not create a separate repository unless Element 145 becomes independently versioned and deployed.

This preserves:

- architecture cohesion;
- shared docs;
- shared governance;
- direct links to provider neutrality, AUWS-SPEC-001, and source-of-truth files.

---

## 8. Immediate Implementation Order

1. Vault the Phase-0 scaffold into `services/element-145/`.
2. Run tests and record failures.
3. Add `docs/architecture/identity-sidecar.md`.
4. Add `TransparencyPacket v0.2` schema.
5. Add `RoutingDecision` and `SphereQuery` models.
6. Wire router to `ServiceRegistry`.
7. Add ledger reload + hash-chain export.
8. Add ConsentKernel preflight stub.
9. Add budget model stub.
10. Add provider/model routing stub.

---

## 9. Current Verdict

The scaffold is a valid Phase-0 runtime seed.

It is not yet a constitutional OS runtime. It becomes one when the next layer of contracts is added:

```text
SphereQuery
RoutingDecision
ConsentDecision
TransparencyPacket v0.2
Provider weights / INV-7 tracker
Budget enforcement
GoldenTrace-compatible ledger
```

Once those are present, Element 145 becomes the executable bridge between AUWS-SPEC-001 and the running Aluminum OS substrate.
