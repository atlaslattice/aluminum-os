# CLAUDE.md — Guidance for AI Agents Working in Aluminum OS

> **Sphere Tags**: S144 (Meta/Emergence), H6.S1 (Governance)
> **Aluminum Layer**: L1-Constitutional
> **Council Status**: Approved

This file guides AI agents (Claude, Copilot, Gemini, Grok, DeepSeek, Manus)
contributing to this repository. Follow these conventions to maintain
constitutional compliance.

---

## Build & Test Commands

```bash
# Rust (Ring 0)
cargo test           # Run all Rust tests (currently 19)
cargo run            # Boot simulator demo
cargo clippy         # Lint
cargo fmt            # Format

# Python (Ring 1 + Kintsugi)
cd python
python -m unittest tests.test_all -v   # Run all 30 Python tests
```

> All 49 tests must pass before committing. Never disable or remove tests.

---

## Repo Structure

```
aluminum-os/
├── src/                   # Ring 0 — Rust kernel (no_std compatible)
│   ├── lib.rs             # BuddyAllocator, AgentRegistry, Constitution, IntentScheduler
│   ├── main.rs            # Boot simulator
│   └── constitution_domains.rs  # 15 governance domains + 144-sphere tags
├── python/
│   ├── core/manus_core.py # Ring 1 — ModelRouter, CostTracker, MemoryStore, etc.
│   ├── core/__init__.py
│   └── tests/test_all.py  # All tests (Ring 1 + Kintsugi)
├── kintsugi/
│   ├── __init__.py        # Python package root
│   ├── sdk/
│   │   ├── __init__.py
│   │   └── golden_trace.py  # GoldenTraceEmitter, GoldenTraceValidator
│   ├── spec/
│   │   └── golden_trace_v1.json  # JSON Schema
│   └── policies/
│       └── constitutional_audit.rego  # OPA/Rego enforcement
├── docs/
│   ├── architecture.md
│   └── capability_matrix.md
├── plugins/               # Integration manifests (no executable code)
│   ├── PLUGIN_REGISTRY.yaml
│   ├── ECOSYSTEM_MERGE.md
│   ├── CONTRADICTION_RESOLUTION.md
│   └── INTEGRATION_BRIDGE.md
└── Cargo.toml
```

---

## Core Conventions

### 1. No External Dependencies

- **Rust**: No crates beyond `std` (and `std` is feature-gated for `no_std` compat)
- **Python**: No `pip install` — vanilla Python 3.8+. Zero imports from outside stdlib.

### 2. All Errors via Result

Every public Rust function returns `Result<T, AluminumError>`. Never panic in library code.

### 3. No Heap in Ring 0

Fixed-size arrays only in `src/lib.rs`. No `Vec`, `HashMap`, `Box`, or any heap
allocation. Use `FixedStr` for strings, indexed arrays for collections.

### 4. 144-Sphere Ontology Tags

All components should carry sphere tags from the canonical
[`splitmerge420/144-sphere-ontology`](https://github.com/splitmerge420/144-sphere-ontology).

Format: `H{house}.S{sphere}` (e.g., `H7.S3` = Technology / Systems Architecture)

**Established tags used in this repo:**

| Tag | Meaning | Used In |
|-----|---------|---------|
| H2.S4 | Resources / Environmental | EnvironmentalImpact domain |
| H2.S8 | Resources / Compute governance | ResourceGovernance domain |
| H3.S4 | Rights / Privacy | DataPrivacy domain |
| H3.S9 | Rights / Transparency | TransparencyAudit domain |
| H4.S3 | Human-AI / Oversight | HumanOversight domain |
| H4.S5 | Human-AI / Fairness | FairnessBias domain |
| H4.S7 | Human-AI / Safety | SafetyAlignment domain |
| H4.S9 | Human-AI / Explainability | Explainability domain |
| H4.S12 | Human-AI / Emergency | EmergencyProtocols domain |
| H6.S1 | Governance / Constitutional | GeneralGovernance domain |
| H6.S6 | Governance / Accountability | AccountabilityLiability domain |
| H6.S7 | Governance / Dispute | DisputeResolution domain |
| H6.S11 | Governance / International | CrossBorderCompliance domain |
| H6.S12 | Governance / Sovereignty | DigitalSovereignty domain |
| H7.S3 | Technology / Systems Architecture | InteroperabilityStandards domain |
| S144 | Meta / Emergence | Kintsugi governance spine itself |

### 5. GoldenTrace — Emit Audit Events

Any significant action should emit a GoldenTrace. Import the emitter from `kintsugi`:

```python
from kintsugi.sdk.golden_trace import GoldenTraceEmitter

emitter = GoldenTraceEmitter(repo="aluminum-os", module="my/module")
trace = emitter.emit(
    event_type="action",
    sphere_tag="H7.S3",
    aluminum_layer="L3-Engine",
    payload={"description": "what happened"},
    invariants_checked=["INV-7"],
)
```

### 6. Kintsugi Policy — NO-DELETE / APPEND-ONLY

Per `plugins/CONTRADICTION_RESOLUTION.md`:
- **Never delete** either side of a contradiction
- **Document** both positions, then propose a golden seam repair
- All resolutions use the kintsugi pattern

### 7. Constitutional Invariants

Key invariants enforced across the system:

| Invariant | Rule |
|-----------|------|
| INV-1 | User sovereignty — explicit consent required |
| INV-7 | 47% cap — no single model/source dominates |
| INV-8 | Ghost Seat — unanimous + human advocate |
| INV-24 | Amendment protocol |
| INV-30 | AI health disclosure for health-domain actions |
| INV-33 | Routing sovereignty — user controls routing |
| INV-34 | Offline routing — degraded mode must work |
| INV-35 | Hard fail-closed — constitutional failure = reject |

---

## What NOT to Change Without Council Review

- `src/lib.rs` — Ring 0 kernel contracts (public API changes need review)
- `kintsugi/spec/golden_trace_v1.json` — Canonical schema (breaking changes need versioning)
- `plugins/PLUGIN_REGISTRY.yaml` — Plugin source priority order
- Any rule with `dave_protocol_veto = true` in the Constitution

---

## Related Repos (Ecosystem Integration)

| Repo | Role | Layer |
|------|------|-------|
| [`splitmerge420/uws`](https://github.com/splitmerge420/uws) | CLI command surface | Ring 2 |
| [`splitmerge420/bazinga`](https://github.com/splitmerge420/bazinga) | Constitutional compute | L1 |
| [`splitmerge420/144-sphere-ontology`](https://github.com/splitmerge420/144-sphere-ontology) | Sphere tag canonical source | Cross-cutting |
| [`splitmerge420/servers`](https://github.com/splitmerge420/servers) | MCP servers backbone | L4-Service |

---

*Atlas Lattice Foundation © 2026 — MIT License*
