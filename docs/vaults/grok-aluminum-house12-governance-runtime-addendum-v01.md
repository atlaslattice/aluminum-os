# Grok Aluminum — House 12 Governance Runtime Addendum v0.1

**Status:** Candidate governance runtime addendum  
**Source:** Grok, in response to current Aluminum OS / Element 145 reconciliation status  
**Target Branch:** `element145-copilot-phase1-reconcile`  
**Target Runtime:** `aluminum-os/services/element-145/`

---

## 1. Summary

This artifact proposes clean drop-in files for:

- House 12 Governance Priority Engine;
- ADR-006 MetabolicImpact schema;
- Four-State Classifier Gate / Constraint Pre-Flight;
- DissentRecord preservation object;
- pytest coverage for priority, pre-flight, metabolic impact, and dissent serialization.

The artifact is compatible with the current module plan but should be treated as **Module 18 candidate work**, not a reason to interrupt the current functional vertical-slice stabilization.

---

## 2. Review Verdict

High-signal and structurally compatible.

Recommended integration path:

1. Add files as independent modules.
2. Do not wire into `pipeline.py` yet.
3. Run/import tests after package path and enum casing are reconciled.
4. Later patch `TransparencyPacketV02` to include MetabolicImpact once current vertical slice is stable.

---

## 3. Notes

Minor reconciliation considerations:

- Grok's `EpistemicState` enum uses uppercase values; current Aluminum OS contracts use lowercase values (`known`, `estimated`, `speculative`, etc.). Keep as separate preflight enum for now or map explicitly during integration.
- `MetabolicImpact` is correct as ADR-006 seed, but should become optional-by-default until a classifier flag requires it.
- `PriorityDecision` should eventually be serialized into `TransparencyPacketV02.governance.policy_checks`.
- Convenor timeout behavior should eventually halt execution and emit `convenor_override: timeout_default`.

---

## 4. Candidate Files

```text
services/element-145/element145/governance/priority.py
services/element-145/element145/transparency/impact.py
services/element-145/element145/governance/preflight.py
services/element-145/element145/governance/dissent.py
services/element-145/tests/test_house12_governance.py
```
