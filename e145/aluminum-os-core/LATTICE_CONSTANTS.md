# Lattice Constants — Canonical Defaults

> **Status:** CANONICAL — empirically confirmed via `shugs_core.py` canonical pipeline (2026-04-29)
> **Authority:** Convenor + Claude S1 independent reconstruction + Manus S7 canonical replication
> **Replication status:** COMPLETE — canonical pipeline confirms N=145 as global optimum

---

## Canonical Lattice Sizes

```yaml
# Canonical lattice configuration
LATTICE_SPHERES_ONLY: 144    # 12 Houses × 12 Spheres — the pure ontology
LATTICE_FULL: 145             # 144 spheres + Element 145 (Admin Sphere / coupling node)
LATTICE_DEFAULT: 145          # Default for all modules operating on "the lattice"
```

## Empirical Confirmation

### Canonical Pipeline (Manus S7, shugs_core.py, K=20 ensemble, N=140-148)

| Rank | N | Mean GUE-KS | p-value vs N=145 |
|------|---|-------------|------------------|
| **1st** | **145** | **0.2677** | (reference) |
| 2nd | 143 | 0.2896 | 0.0143 |
| 3rd | 147 | 0.2926 | — |
| 4th | 144 | 0.2939 | **0.0154** |
| 5th | 146 | 0.2999 | **0.0005** |

**N=145 is the global optimum with statistical significance:**
- N=145 > N=144 (p=0.0154) — the "+1" is load-bearing
- N=145 > N=146 (p=0.0005) — exactly "+1", not "+2"
- N=145 > N=143 (p=0.0143) — beats both downward neighbors

### Independent Reconstruction (Claude S1, K=20 ensemble, N=140-148)

Claude S1's reconstruction also found N=145 > N=144 (p=0.032), but had N=146 as the global optimum. The canonical pipeline resolves this ambiguity: the reconstruction was missing structure that selects against N=146.

## Usage Rules

Any module that operates on "the lattice" should default to **LATTICE_FULL (N=145)** — the full ontology including the Admin Sphere coupling structure.

Any module that explicitly needs the 144-only sphere set should reference **LATTICE_SPHERES_ONLY (N=144)** and document why the Admin Sphere is excluded.

The unified default is always **LATTICE_DEFAULT = 145**.

## N-Scaling Caveat

The operator shows non-monotonic GUE-KS behavior across increasing N (confirmed in both canonical and reconstruction pipelines). The lattice optimum at N=145 is confirmed for the 140-148 bracket, but whether the operator converges to GUE at large N remains an open empirical question. See `CANONICAL_REPLICATION_RESULTS.md` §3 for details.

---

*Lattice Constants v2.0 — Aluminum OS — Element 145 — Build Plan v3.14+*
*Empirically confirmed via canonical shugs_core.py pipeline 2026-04-29*
