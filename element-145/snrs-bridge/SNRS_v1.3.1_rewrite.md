# SNRS v1.3.1 (Rewrite) — Sovereign Node Radius Stack
## Phase‑1 Monte Carlo scaffold (comparative, causal, and loggable)

**Intent:** This is not a calibrated forecast engine. It is a *comparative* Monte Carlo scaffold to test whether a **reuse‑first, population‑first dignity node** can plausibly clear feasibility boundaries under conservative assumptions, across:
- node sizes
- scenario classes (A/B/C)
- governance regimes (high‑trust / low‑trust)
- centralized node vs subcluster decomposition

**Core standard:** Preserve SNRS causal structure, avoid decorative outputs, and produce interpretable comparative deltas.

**Version:** 1.3.1‑rewrite  
**Date:** 2026-04-12  
**Federation:** GPT, DeepSeek, Grok, Gemini, Claude, Copilot  
**Outputs:** NPV distribution, probability(NPV>0), terminal‑year physical savings, hard‑savings feasibility thresholds.

---

## 0) Design rules (so agents don’t “fix” it into nonsense)

1. **System of record is the model, not the narrative.** Narrative claims must match code.
2. **Phase‑1 constraint:** prioritize *comparative validity* over micro‑calibration.
3. **Every flow must have a stock.** If a value is “earned,” there must be a modeled process that produces it.
4. **Subcluster comparison must be distributionally valid** (median-of-sums, not sum-of-medians).
5. **Interpretability > sophistication:** prefer a few clear mechanisms to many weak ones.

---

## 1) Model objects (stocks and flows)

### 1.1 Stocks
- **Recoverable housing stock (units):** upper bound on convertible units, local to node.
- **Converted units (units):** units brought into node service.
- **Occupied units (units):** converted units adjusted by abandonment.
- **Write‑off stock processed (units):** demolition/dismantling stream if modeled.

### 1.2 Flows
- **Conversion flow:** new converted units per year (bounded by stock cap).
- **Abandonment flow:** fraction of occupied units leaving service per year.
- **Demolition/dismantling flow (optional):** write‑off units processed per year (separate from conversion).

---

## 2) Inputs and distributions (triangular unless noted)
Use triangular distributions to encode conservative uncertainty and keep federation‑auditable.

**Housing shares (normalized):**
- Ready share ~ Tri(0.2, 0.3, 0.4)
- Salvageable share ~ Tri(0.3, 0.4, 0.5)
- Write‑off share ~ Tri(0.05, 0.1, 0.15)

**Retrofit costs:**
- Ready cost C_ready ~ Tri(20k, 35k, 60k)
- Salvage cost C_salv ~ Tri(50k, 80k, 120k)

**Net material recovery:**
- R_ready ~ Tri(1k, 2.5k, 5k)
- R_salv ~ Tri(5k, 10k, 15k)
- R_writeoff ~ Tri(2k, 4k, 8k)  *(only applies if write‑off processing is modeled)*

**Hard savings per unit per year (swept for thresholds):**
- S_hard ∈ [0..8000] USD/unit/year

**Efficiency savings fractions:**
- f_energy ~ Tri(0.2, 0.3, 0.4)
- f_water ~ Tri(0.3, 0.4, 0.5)

**Healthcare savings:**
- H_save ~ Tri(200, 350, 500) USD/person/year

**Adoption timing:**
- T80 ~ Tri(40, 55, 70) years  *(time to reach 80% of asymptote)*
- policy lag ~ Tri(2, 3.5, 5) years
- conversion lag ~ Tri(1, 2, 3) years

**Decay / abandonment:**
- degradation base ~ Tri(0.01, 0.02, 0.03) per year (maintenance stressor)
- abandonment base ~ Tri(0.005, 0.01, 0.02) per year

**Capability formation (only in scenarios B/C):**
- participation ~ Tri(0.1, 0.2, 0.3)
- retention ~ Tri(0.5, 0.65, 0.8)
- maintenance reduction ~ Tri(0.05, 0.1, 0.15)
- degradation reduction ~ Tri(0.1, 0.2, 0.3)

**Food loop (only in scenarios B/C):**
- food_offset ~ Tri(0.1, 0.2, 0.3)
- nutrient_recovery ~ Tri(0.1, 0.25, 0.4)
- fert_offset ~ Tri(0.05, 0.1, 0.2)
- food_capex ~ Tri(100, 300, 600) USD/person
- food_opex ~ Tri(20, 50, 100) USD/person/year

**Computation (only in scenarios B/C):**
- comp_opex ~ Tri(10, 25, 50) USD/person/year
- comp_offset ~ Tri(0.01, 0.03, 0.05) (fraction of energy+water savings captured as extra benefit)

**Local reuse richness (stock cap multiplier):**
- reuse_richness ~ Tri(0.5, 1.0, 1.5)

**Global constants:**
- horizon: 100 years, start 2025
- discount rate: 3%
- persons_per_unit: 1.5
- baseline energy cost: 300 USD/unit/year
- baseline water cost: 150 USD/unit/year
- baseline maintenance: 500 USD/unit/year
- annual food spend proxy: 1200 USD/person/year
- baseline fertilizer proxy: 50 USD/person/year

---

## 3) Scenario multipliers (explicitly labeled assumptions)

Scenarios A/B/C are *assumption bundles*:

| parameter | A (Bare) | B (Dignity) | C (Full) |
|---|---:|---:|---:|
| wrapper_capex | 0.8 | 1.0 | 1.2 |
| hard_savings mult | 1.0 | 1.2 | 1.4 |
| efficiency mult | 1.0 | 1.1 | 1.2 |
| policy lag mult | 1.0 | 0.9 | 0.8 |
| participation mult | 1.0 | 1.1 | 1.2 |
| degradation mult | 1.0 | 0.9 | 0.8 |

Governance (trust) multipliers:

| parameter | high‑trust | low‑trust |
|---|---:|---:|
| policy lag factor | 0.8 | 1.5 |
| abandonment factor | 0.5 | 2.0 |
| participation factor | 1.2 | 0.7 |

---

## 4) Functional forms (strictly causal)

### 4.1 Recoverable stock cap (units)