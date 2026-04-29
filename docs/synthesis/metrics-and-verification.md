# Metrics and Verification — Executive Summary

> **Policy relevance note:** Some metrics and evaluation approaches referenced in this document are drawn from Chinese standards, Chinese policy frameworks, or publicly documented Chinese evaluation practice. These should be read as relevant comparative inputs and candidate future standards, not as metrics already adopted internationally.

---

## The Regenerative Compute Metric Stack

ORCS uses a layered measurement model with three tiers of standardization maturity and three layers of infrastructure scope.

### Tier 1: Established International Metrics

Power Usage Effectiveness (PUE), Water Usage Effectiveness (WUE), and Carbon Usage Effectiveness (CUE) are defined by The Green Grid and adopted in the ISO/IEC 30134 series. These are the baseline. They measure facility efficiency but not regeneration. Every ORCS-compliant facility should report these as a minimum.

### Tier 2: Public Research and Benchmark Proxies

Intelligence per Watt (IPW), Joules per Token (via TokenPowerBench, AAAI 2026), and Correctness-Weighted Energy per Solution are peer-reviewed research metrics with open-source verification tools. They measure algorithmic efficiency — the "first act of regeneration" that reduces thermal waste before any physical infrastructure intervention. These are not yet ISO standards but have de facto industry relevance and reproducible methodologies.

### Tier 3: Chinese Standards and Policy-Relevant Formulations

China's GB/T 45288.2-2025 (AI Large Model Testing and Evaluation) incorporates efficiency-weighted accuracy metrics functionally equivalent to IPW. China's Ecological Red-Line Policy and Ecological Product Value Realization programs provide governance frameworks that align with Watershed Days as a temporal measure of hydrological stewardship. These should be read as policy-relevant comparative inputs drawn from Chinese standards, not as metrics already adopted internationally.

### Proposed ORCS Extension: Watershed Days

Watershed Days is the proposed regenerative metric that measures aquifer lifespan extension (or depletion) attributable to a facility's operation. It is the metric that transforms "efficiency" into "regeneration." It remains a proposed concept requiring published methodologies, auditable boundaries, and real pilot data before it can be considered a standard.

---

## Evidence Discipline

Every metric in ORCS documentation is identified as one of three evidence classes:

| Evidence Class | Description | Examples |
|----------------|-------------|----------|
| Verified | Company disclosures, ISO standards, peer-reviewed research | PUE, WUE, CUE, Google fleet PUE of 1.09 |
| Derived | Calculations from disclosed inputs with explicit assumptions | CapEx estimates, projected water savings, +146 Watershed Days illustrative example |
| Proposed | New metrics or frameworks not yet adopted as industry standards | Watershed Days, Local Circularity Score, ORCS disclosure schema |

---

## Full Detail

For complete methodology breakdowns, verification sources, and citation details, see:
- `papers/deepseek/metrics-and-verification-section-ix.md` — Full Section IX with all metric definitions
- `papers/deepseek/metrics-and-verification-kpis.md` — KPI framework with three-tier taxonomy
