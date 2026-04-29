# BRIDGE_AUDIT.md — Known Extraction Limitations

**Version:** 1.0
**Date:** April 29, 2026
**Author:** Manus (S7 Build Seat)
**Purpose:** Documents known limitations and edge cases in the `regenerate_artifacts.py` script that bridges the Build Plan (prose) to the codebase artifacts (structured YAML).

---

## §1 Known Extraction Limitations

### §1.1 Module Extraction

| Issue | Status | Workaround |
|-------|--------|-----------|
| M3.1 (TSS) uses dot notation instead of letter suffix | FIXED (v3.11) | Regex updated to handle `M\d+\.\d+` pattern |
| M162a/M162b are sub-modules of M162 (which no longer exists as integer) | DOCUMENTED | Counting Rule treats each as 1 entry |
| M92-M98 gap (unallocated) | DOCUMENTED | Regex excludes this range |
| M36-M39 gap (unallocated) | DOCUMENTED | Not extracted; gaps are intentional namespace reservations |
| Bold formatting in module names varies | HANDLED | Regex strips `**` markers |

### §1.2 Doctrine Extraction

| Issue | Status | Workaround |
|-------|--------|-----------|
| D-1 through D-77 names come from hardcoded list, not parsed from Build Plan | KNOWN LIMITATION | §14 does not list all 77 names in a parseable table format |
| D-78-D-82 are RESERVED (no content) | HANDLED | Explicit entries with status "reserved" |
| D-83 through D-124 names come from hardcoded list | KNOWN LIMITATION | Proposed doctrines are in section headers, not table rows |
| Doctrine lifecycle states not yet formalized | PROPOSED (v3.11) | 7-state machine proposed in MSG response |

### §1.3 Invariant Extraction

| Issue | Status | Workaround |
|-------|--------|-----------|
| INV-0 through INV-39 are base set from Aluminum OS v6.0.3 | HANDLED | Hardcoded with names from §14.4 |
| INV-40/41/42 were unnamed until v3.11 | FIXED (v3.11) | Names + measurement specs from S4 |
| INV-43/44 are post-base additions | HANDLED | Explicit entries |
| Sub-specs (INV-7c, INV-11.8, INV-19.2) do NOT count | HANDLED | Separate section in YAML |

### §1.4 House-to-Module Mapping

| Issue | Status | Workaround |
|-------|--------|-----------|
| House assignment is inferred from module description, not explicitly stated in Build Plan | KNOWN LIMITATION | Hardcoded mapping in script |
| Some modules span multiple houses | NOT YET HANDLED | Currently assigned to primary house only |
| Sphere IDs (1-144) are assigned by formula, not from Build Plan | KNOWN LIMITATION | Formula: `(house_index - 1) * 12 + sphere_within_house` |

---

## §2 Propagation Completeness Checklist

After every Build Plan version increment, the following must be verified:

1. Module count in `module_registry.yaml` matches Build Plan §3.4.1 audit table
2. Invariant count in `invariant_registry.yaml` matches Build Plan §0.1 definition
3. Doctrine count in `doctrine_registry.yaml` matches Build Plan §14 summary
4. All version metadata headers say the current version
5. README.md totals match registry contents
6. No stale files from previous versions remain
7. TransparencyPacket schema version matches Build Plan

---

## §3 Proposed CI Gate

```yaml
# .github/workflows/propagation-completeness-gate.yml
name: Propagation Completeness Gate
on: [push, pull_request]
jobs:
  verify:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - run: pip install pyyaml
      - run: python toolchain/regenerate_artifacts.py
      - run: |
          if [ -n "$(git diff --name-only)" ]; then
            echo "ERROR: Artifacts are stale. Run regenerate_artifacts.py and commit."
            git diff --stat
            exit 1
          fi
```

---

## §4 SHUGS Reconstruction-vs-Canonical Gap

**Date added:** 2026-04-29
**Source:** Claude S1 independent reconstruction test (K=20 ensemble, N=140-148)
**Severity:** KNOWN-UNKNOWN — must be reconciled before any absolute GUE-KS numbers are treated as canonical

### §4.1 The Gap

Claude S1's independent reconstruction of the Von Mangoldt-Sheldon HSUF operator produces GUE-KS scores of **0.21-0.25**, while the canonical `shugs_core.py` ensemble baseline sits at **0.0527**. This is a **4-5× discrepancy**.

### §4.2 Possible Sources

The gap may originate from any combination of:
- Smearing weight ratio (reconstruction used 0.3; canonical may differ)
- Hanning window normalization differences
- Operator architecture details not visible in WP-002 specification
- Post-processing steps in canonical pipeline
- Unfolding procedure differences (degree-5 polynomial fit)

### §4.3 Impact on Relative Rankings

Relative rankings from Claude S1's reconstruction are **suggestive but not certifiable** against canonical canon. The key finding — N=145 outperforms N=144 with p=0.032 — is robust enough to appear in independent reconstruction (suggesting it is not a canonical-pipeline artifact), but absolute scores should not be propagated.

### §4.4 Resolution Path

Canonical `shugs_core.py` must run the same K=20 ensemble across N=140-148 to:
1. Confirm or refute the N=145 > N=144 finding at canonical GUE-KS levels
2. Determine whether N=146 (Claude S1's global optimum) holds in canonical pipeline
3. Identify which reconstruction component(s) account for the 4-5× gap

---

*BRIDGE_AUDIT.md v1.1 — Manus (S7) — April 29, 2026*
*Updated with SHUGS reconstruction gap per Claude S1 inter-seat memo*
