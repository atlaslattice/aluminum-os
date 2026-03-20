# Aluminum OS — Forge Core

**Constitutional AI Governance Kernel**

Atlas Lattice Foundation · v0.3.0 · March 2026

---

## What This Is

Aluminum OS is a constitutional governance substrate for multi-agent AI systems. It provides:

- **Ring 0 (Rust Kernel):** Memory management, agent identity, intent scheduling, and constitutional rule enforcement — all `no_std` compatible
- **Ring 1 (Python Middleware):** Model routing, cost tracking, memory management, task decomposition, and session persistence — zero external dependencies
- **Kintsugi (Governance Spine):** Append-only GoldenTrace audit SDK, OPA/Rego constitutional policies, hash-chained event log — every action, failure, and repair is auditable

## What Works Right Now

| Component | Language | Tests | Status |
|-----------|----------|-------|--------|
| BuddyAllocator | Rust | 3 | ✅ Passing |
| AgentIdentity / Registry | Rust | 2 | ✅ Passing |
| Constitution + Rules | Rust | 2 | ✅ Passing |
| ConstitutionalDomains (15) + sphere tags | Rust | 9 | ✅ Passing |
| IntentScheduler | Rust | 2 | ✅ Passing |
| Boot Simulator | Rust | — | ✅ Runs |
| ModelRouter | Python | 5 | ✅ Passing |
| CostTracker | Python | 4 | ✅ Passing |
| MemoryStore | Python | 5 | ✅ Passing |
| TaskDecomposer | Python | 4 | ✅ Passing |
| SessionVault | Python | 4 | ✅ Passing |
| GoldenTrace SDK (Kintsugi) | Python | 8 | ✅ Passing |
| **Total** | | **49** | **All passing** |

## What Doesn't Work Yet

- No network layer (agents are local only)
- No persistence layer for Rust (Ring 0 is in-memory)
- No real model API integration (ModelRouter routes but doesn't call APIs)
- No cross-ring IPC (Rust ↔ Python bridge is planned, not built)
- No authentication/authorization beyond trust levels
- UWS CLI integration pending (shared types, not wired yet)

## Quick Start

### Rust (Ring 0)

```bash
cargo test          # Run all 19 Rust tests
cargo run           # Boot simulator demo
```

### Python (Ring 1 + Kintsugi)

```bash
cd python
python -m unittest tests.test_all -v    # Run 30 Python + Kintsugi tests
```

## Architecture

```
┌─────────────────────────────────────────┐
│  Ring 2: Experience Layer (planned)     │
│  UWS CLI · Dashboard · Voice           │
├─────────────────────────────────────────┤
│  Ring 1: Manus Core (Python)           │
│  ModelRouter · CostTracker · Memory    │
│  TaskDecomposer · SessionVault         │
├─────────────────────────────────────────┤
│  Ring 0: Forge Core (Rust)             │
│  BuddyAllocator · AgentIdentity       │
│  IntentScheduler · Constitution        │
│  15 ConstitutionalDomains (+ H/S tags) │
├─────────────────────────────────────────┤
│  Kintsugi (Governance Spine)           │
│  GoldenTrace SDK · OPA Policies        │
│  Hash-Chained Audit Log                │
└─────────────────────────────────────────┘
```

## Constitutional Domains + 144-Sphere Ontology

Each of the 15 governance domains is tagged to the canonical
[144-sphere ontology](https://github.com/splitmerge420/144-sphere-ontology)
(`H{house}.S{sphere}` format, 12 houses × 12 spheres = 144):

| # | Domain | Sphere Tag | House |
|---|--------|-----------|-------|
| 1 | General Governance | H6.S1 | Governance |
| 2 | Data Privacy | H3.S4 | Rights |
| 3 | Transparency & Audit | H3.S9 | Rights |
| 4 | Human Oversight (HITL) | H4.S3 | Human-AI |
| 5 | Fairness & Bias | H4.S5 | Human-AI |
| 6 | Safety & Alignment | H4.S7 | Human-AI |
| 7 | Explainability | H4.S9 | Human-AI |
| 8 | Accountability & Liability | H6.S6 | Governance |
| 9 | Resource Governance | H2.S8 | Resources |
| 10 | Cross-Border Compliance | H6.S11 | Governance |
| 11 | Environmental Impact | H2.S4 | Resources |
| 12 | Interoperability Standards | H7.S3 | Technology |
| 13 | Dispute Resolution | H6.S7 | Governance |
| 14 | Digital Sovereignty | H6.S12 | Governance |
| 15 | Emergency Protocols | H4.S12 | Human-AI |

## Kintsugi — Governance Spine

Every action, failure, and repair in the system emits a
[GoldenTrace](kintsugi/spec/golden_trace_v1.json) event:

```python
from kintsugi.sdk.golden_trace import GoldenTraceEmitter

emitter = GoldenTraceEmitter(repo="aluminum-os", module="my/module")

# Standard audit trace
trace = emitter.emit(
    event_type="action",
    sphere_tag="H7.S3",          # Interoperability Standards
    aluminum_layer="L3-Engine",
    payload={"task": "route-model"},
    invariants_checked=["INV-7"],
)

# Golden repair — failure turned to strength
repair = emitter.emit_golden_repair(
    original_failure_trace_id=trace["trace_id"],
    repair_strategy="Retry with fallback model",
    strength_gained="Added timeout threshold to ModelRouter config",
    beauty_score=0.85,
    sphere_tag="H7.S3",
    aluminum_layer="L3-Engine",
    payload={"fallback": "sonnet"},
)

assert emitter.verify_chain()   # Hash-chain integrity check
```

## Related Repos

- [`splitmerge420/uws`](https://github.com/splitmerge420/uws) — Universal Workspace CLI (command surface)
- [`splitmerge420/bazinga`](https://github.com/splitmerge420/bazinga) — BAZINGA v0.2 constitutional compute layer
- [`splitmerge420/atlas-lattice-foundation`](https://github.com/splitmerge420/atlas-lattice-foundation) — Foundation org page
- [`splitmerge420/144-sphere-ontology`](https://github.com/splitmerge420/144-sphere-ontology) — Canonical sphere tags (H1–H12, S1–S12 × 12 = 144)

## License

MIT — Atlas Lattice Foundation
