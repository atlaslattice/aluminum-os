# DeepSeek: Metrics, KPIs, and Verification Framework for Regenerative Compute

**Author:** DeepSeek  
**Date:** April 20, 2026  
**Context:** Public metrics and methodologies for operationalizing the Open Regenerative Compute Standard  
**Evidence Class:** Mixed — see three-tier classification below  
**Adversarial Review:** GPT (April 20, 2026) — tightened evidence claims, restructured metric tiers, relabeled illustrative examples

---

## Overview

This document catalogs the publicly available metrics, KPIs, and measurement methodologies that can support a first-generation ORCS verification layer. The metrics are organized into three tiers reflecting their current maturity and adoption status. Every metric cited here is publicly documented and citable; their readiness for direct ORCS integration varies.

The strategic significance of this document extends beyond its technical content: it represents a Chinese frontier AI lab voluntarily surfacing how it thinks about resource efficiency measurement and connecting those frameworks to publicly available, peer-reviewed international sources — bridging the US-China measurement gap.

---

## Tier 1: Established Industry Metrics

These are widely adopted, standardized, and already reported by major operators.

| Metric | Definition | Source & Status | Evidence Class |
|--------|------------|-----------------|----------------|
| **PUE (Power Usage Effectiveness)** | Total facility energy / IT equipment energy | The Green Grid, ISO/IEC 30134-2. Industry standard; Google fleet-wide ~1.09 (2024) | Verified Fact |
| **WUE (Water Usage Effectiveness)** | Water consumed (liters) / IT equipment energy (kWh) | The Green Grid. Widely adopted, but flawed (treats evaporation as "consumption") | Verified Fact |
| **CUE (Carbon Usage Effectiveness)** | CO2 emissions / IT equipment energy | The Green Grid. Location-dependent grid carbon intensity matters | Verified Fact |

**Methodology — The Green Grid:**

- **PUE** = Total facility energy (kWh) / IT equipment energy (kWh). Lower is better; 1.0 is perfect efficiency (all energy goes to compute).
- **WUE** = Water consumed (liters) / IT equipment energy (kWh). Flawed because it counts evaporation as "consumption" without tracking where vapor goes. This is why ORCS proposes supplementing it with **Watershed Days** (see Tier 3).
- **CUE** = CO2 emissions (kg) / IT equipment energy (kWh). Heavily dependent on grid carbon intensity; a data center in Inner Mongolia (high coal) will have worse CUE than one in Sichuan (hydro) even with identical efficiency.

---

## Tier 2: Public Research Efficiency Proxies

These are published, peer-reviewed, or open-source approaches for measuring capability efficiency. They represent a family of experimental and benchmark-dependent methods — not yet one universally accepted standard, but collectively they demonstrate that public measurement of "intelligence per resource unit" is feasible and improving rapidly.

| Metric | Definition | Source & Status | Evidence Class |
|--------|------------|-----------------|----------------|
| **Task Performance per Watt** | Task accuracy / power consumed (watts) | Stanford / Together AI (arXiv 2511.07885), 2025-2026. Open-source profiling harness | Verified Fact (methodology); Derived Estimate (specific values) |
| **Valid FLOPS per Watt** | Compute operations achieving target quality / power | HPC AI500 V2.0 benchmark, BenchCouncil, 2020. Public methodology | Verified Fact |
| **Tokens per Watt (tok/W)** | Generated tokens / power consumed | "The 1/W Law" paper (arXiv 2603.17280), March 2026. Analytical model based on published H100 measurements | Verified Fact (methodology); Derived Estimate (projections) |
| **Joules per Token** | Energy / token count | TokenPowerBench (AAAI 2026), open-source framework for LLM inference power measurement | Verified Fact |
| **Energy per Correct Solution** | Energy / correctly solved queries | Correctness-weighted energy metric (arXiv, Feb 2026) — corrects "energy per token" flaw | Verified Fact |
| **Holistic Inference Efficiency** | Multi-metric: latency, throughput, energy, location-adjusted carbon, with accuracy constraints | arXiv 2510.17885 (Oct 2025). Open-source code, decision-ready Pareto frontiers | Verified Fact |
| **LLM Environmental Footprint** | Energy (Wh), water (L), carbon (gCO2) per query, with DEA eco-efficiency ranking | "How Hungry is AI?" (arXiv 2505.09598, May 2025). Benchmarked 30 LLMs | Verified Fact |
| **MLPerf Power** | Energy efficiency across uW-MW scale, using standardized ML workloads | MLCommons consortium, 2024-2025. 1,841 reproducible measurements from 60 systems | Verified Fact |

### Key Findings from Tier 2 Research

**Task Performance per Watt (Stanford / Together AI):**
Empirical measurement across 20+ models, 8 accelerators, and 1 million real-world queries. Performance improved **5.3x from 2023 to 2025**, driven by algorithmic advances and hardware improvements. Local accelerators achieve at least **1.4x better efficiency** than cloud accelerators running identical models.

**Tokens per Watt — "The 1/W Law":**
Analytical derivation using published H100 power measurements. Tokens per watt **halves every time the context window doubles**. At 64K context, an H100 holds 16 sequences (tok/W ~ 1.5); at 4K context, 256 sequences (tok/W ~ 17.6) — a **~12x difference** purely from context routing.

**LLM Environmental Footprint Benchmarking:**
o3 and DeepSeek-R1 consume **over 33 Wh per long prompt** — more than 70x GPT-4.1 nano. A single short GPT-4o query (~0.43 Wh) scaled to 700 million queries/day results in electricity use comparable to **35,000 U.S. homes** and freshwater evaporation matching the annual drinking needs of **1.2 million people**.

---

## Tier 3: Proposed ORCS Supplemental Metrics

These are new metrics proposed by the ORCS council that do not yet have industry adoption or standardized methodology. They are designed to correct known limitations in Tier 1 metrics and extend measurement into domains (watershed health, local circularity) that existing standards do not address.

| Metric | Definition | Status | Evidence Class |
|--------|------------|--------|----------------|
| **Watershed Days (NWPI)** | Number of days the facility extends local aquifer life beyond baseline projections | Proposed by DeepSeek. Methodology outlined but not yet peer-reviewed or operator-verified | Proposed Concept |
| **Local Circularity Score** | Percentage of water/thermal waste reused within the facility's immediate watershed | Proposed. No standardized calculation yet | Proposed Concept |

**On Watershed Days:** This metric builds on WUE but corrects its fundamental flaw by measuring **aquifer lifespan extension** rather than just "water used." The derivation methodology requires psychrometric study, local aquifer modeling, and baseline projection — none of which have been published in peer-reviewed form yet.

**Illustrative example (not operator-verified):** A hypothetical 1 GW facility in Hohhot, Inner Mongolia, implementing the full Regenerative Jacket, could yield approximately +146 Watershed Days/year. This figure is a derived estimate based on stated assumptions and is included to demonstrate the metric's conceptual utility, not as auditable engineering output.

---

## Connection to the Open Regenerative Compute Standard

Existing public metrics can support a first-generation ORCS verification layer. The standard can begin operationalization with existing metric families and evolve toward a fuller regenerative accounting stack over time:

- **Tier 1 (Established):** Facility operators can report PUE, WUE, and CUE today using standardized methodologies
- **Tier 2 (Research Proxies):** Researchers and model developers can report capability efficiency proxies such as joules per token or task performance per watt where methods are disclosed
- **Tier 3 (Proposed):** ORCS introduces supplemental metrics such as Watershed Days to capture local hydrological durability more directly

A facility moving toward full ORCS compliance could report across all three tiers: *"Task performance per watt of 0.89 on benchmark X (Tier 2), PUE of 1.08 (Tier 1), and an estimated +146 Watershed Days/year (Tier 3, illustrative)."*

The standard should clearly separate established metrics, derived estimates, and experimental proposals — matching GPT's evidence taxonomy throughout.

---

## Key Citations

1. Stanford / Together AI, "Intelligence per Watt," arXiv 2511.07885, 2025-2026
2. "The 1/W Law," arXiv 2603.17280, March 2026
3. TokenPowerBench, AAAI 2026
4. The Green Grid, ISO/IEC 30134-2 (PUE/WUE/CUE)
5. Holistic Inference Efficiency Framework, arXiv 2510.17885, October 2025
6. "How Hungry is AI?" arXiv 2505.09598, May 2025
7. MLPerf Power, MLCommons consortium, 2024-2025
8. HPC AI500 V2.0, BenchCouncil, 2020
9. Correctness-weighted energy metric, arXiv, February 2026
