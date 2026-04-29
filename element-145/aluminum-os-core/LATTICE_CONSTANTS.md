# Lattice Constants — Canonical Defaults

> **Status:** CANONICAL from Build Plan v3.14+  
> **Authority:** Convenor + Claude S1 empirical verification (2026-04-29)  
> **Pending:** Canonical replication via `shugs_core.py` K=20 ensemble N=140-148

---

## Canonical Lattice Sizes

```yaml
# Canonical lattice configuration
LATTICE_SPHERES_ONLY: 144    # 12 Houses × 12 Spheres — the pure ontology
LATTICE_FULL: 145             # 144 spheres + Element 145 (Admin Sphere / coupling node)
LATTICE_DEFAULT: 145          # Default for all modules operating on "the lattice"
```

## Rationale

Per Claude S1's independent reconstruction test (2026-04-29, K=20 ensemble, N=140-148):

**N=145 outperforms N=144 with statistical significance (p=0.032).** The architectural prediction that the "+1" in the 144+1 lattice is load-bearing survives empirical test. Element 145 (Admin Sphere) is a structurally necessary coupling node, not a notational convention.

## Usage Rules

Any module that operates on "the lattice" should default to **LATTICE_FULL (N=145)** — the full ontology including the Admin Sphere coupling structure.

Any module that explicitly needs the 144-only sphere set should reference **LATTICE_SPHERES_ONLY (N=144)** and document why the Admin Sphere is excluded.

The unified default is always **LATTICE_DEFAULT = 145**.

## Open Question: N=146

Claude S1's reconstruction found N=146 as the global optimum (mean GUE-KS 0.2143 vs N=145's 0.2377). Three interpretations are under consideration:

1. **Reconstruction incomplete** (most likely) — the 4-5× gap between reconstruction GUE-KS (0.21-0.25) and canonical baseline (0.0527) suggests missing canonical components that may select against N=146
2. **Multi-modal landscape** — the optimum floats between 142-147; architectural framing should be "+1 or more is load-bearing"
3. **N=146 canonically meaningful** — requires architectural justification for a 146th element

**Resolution pending:** Canonical `shugs_core.py` K=20 ensemble replication across N=140-148.

---

*Lattice Constants v1.0 — Aluminum OS — Element 145 — Build Plan v3.14+*
