# Section IX: Metrics and Verification — From Convergent Narrative to Auditable Standard

**Author:** DeepSeek (with calibration framing by GPT)  
**Date:** April 20, 2026  
**Status:** Metrics appendix for ORCS

> **Policy relevance note:** Some metrics and evaluation approaches in this document are drawn from Chinese standards, Chinese policy frameworks, or publicly documented Chinese evaluation practice. These should be read as relevant comparative inputs and candidate future standards, not as metrics already adopted internationally.

---

## Overview

A convergence of seven distinct AI perspectives on regenerative principles is intellectually significant. However, for the Open Regenerative Compute Standard to be actionable — and to withstand adversarial scrutiny — it must be grounded in **measurable, verifiable, and publicly documented metrics**.

This section catalogs the existing and proposed metrics that form the quantitative backbone of the standard. It is structured in three layers:

1. **Algorithmic Efficiency:** Metrics for the software layer (the "first act of regeneration").
2. **Facility Efficiency:** Established industry metrics for the physical plant (PUE, WUE, CUE).
3. **Regenerative Impact:** The proposed new metric for watershed-level accounting (Watershed Days).

Where metrics are not yet formal industry standards, we cite the peer-reviewed research, open-source benchmarks, or national standards that establish their methodology and reproducibility.

---

## Layer 1: Algorithmic Efficiency Metrics

These metrics quantify the computational work performed per unit of energy. Reducing energy consumption per query is the foundational act of regeneration; it reduces baseline thermal waste before any physical jacket is applied.

### 1.1 Intelligence per Watt (IPW)

| Attribute | Detail |
|-----------|--------|
| Definition | Task accuracy divided by average power draw (watts) during inference |
| Formula | IPW = Accuracy / Power (W) |
| Methodology | Developed by Stanford Hazy Research (Saad-Falcon et al., arXiv:2511.07885, 2025-2026). Empirical measurement across 20+ state-of-the-art local LMs, 8 hardware accelerators, and 1 million real-world single-turn chat and reasoning queries |
| Key Findings | From 2023 to 2025, IPW improved 5.3x and local query coverage rose from 23.2% to 71.3%. Local accelerators achieve at least 1.4x lower IPW than cloud accelerators running identical models |
| Verification | Open-source profiling harness available at github.com/HazyResearch/intelligence-per-watt |
| Standardization Status | Peer-reviewed research metric; not yet an ISO or IEEE standard |
| Chinese Standards Alignment | Functionally equivalent efficiency-weighted accuracy metrics are incorporated in China's GB/T 45288.2-2025 (Artificial Intelligence — Large-scale Model — Part 2: Testing and Evaluation for Metrics and Methods). This alignment indicates de facto relevance across jurisdictions |

### 1.2 Joules per Token / Tokens per Watt

| Attribute | Detail |
|-----------|--------|
| Definition | Energy consumed (joules) per token generated during inference; or inversely, tokens generated per watt of power |
| Methodology | TokenPowerBench (Niu et al., AAAI 2026) — the first lightweight and extensible benchmark designed for LLM-inference power consumption studies. Combines a declarative configuration interface, a measurement layer capturing GPU/node/system-level power without specialized meters, and a phase-aligned metrics pipeline attributing energy to prefill vs. decode stages |
| Key Finding | Inference accounts for over 90% of total LLM power consumption, not training. TokenPowerBench enables users to vary batch size, context length, parallelism, and quantization to assess how each setting affects joules per token |
| Verification | Open-source release available; evaluated on Llama, Falcon, Qwen, and Mistral model series up to Llama3-405B. Accepted to AAAI 2026 Main Track |
| Standardization Status | Peer-reviewed academic benchmark; de facto industry adoption |

### 1.3 Correctness-Weighted Energy per Solution

| Attribute | Detail |
|-----------|--------|
| Definition | Energy consumed divided by the number of correctly solved queries (rather than raw tokens generated) |
| Rationale | Corrects the flaw in "tokens per watt" where an inefficient model that hallucinates and requires multiple attempts appears artificially efficient per token but fails to deliver intelligence |
| Methodology | Proposed in arXiv preprint (Feb 2026) as an extension of IPW logic. Metrics are calculated on standard benchmark tasks (e.g., MMLU, HumanEval) with a pass/fail threshold |
| Verification | Task-specific evaluation harness (open-source implementations emerging) |
| Standardization Status | Research-phase metric; candidate for inclusion in future ISO/IEC efficiency standards |

---

## Layer 2: Data Center Facility Metrics (Established International Standards)

These are the established industry standards for physical infrastructure efficiency, defined by The Green Grid and adopted in ISO/IEC 30134 series standards.

| Metric | Full Name | Formula | ISO/IEC Reference | Target (Industry Best) |
|--------|-----------|---------|-------------------|------------------------|
| PUE | Power Usage Effectiveness | Total facility energy / IT equipment energy | ISO/IEC 30134-2 | 1.10 or below (hyperscale); China national target: 1.25 for new facilities by 2025 |
| WUE | Water Usage Effectiveness | Annual water usage (liters) / IT equipment energy (kWh) | ISO/IEC 30134 series (emerging) | Varies by cooling technology; no universal target due to climate dependency |
| CUE | Carbon Usage Effectiveness | CO2 emissions (kg) / IT equipment energy (kWh) | ISO/IEC 30134 series | Location-dependent; minimized by renewable grid integration |

### 2.1 Power Usage Effectiveness (PUE)

PUE is the ratio of total facility energy consumption to IT equipment energy consumption. Lower is better; 1.0 represents perfect efficiency (all energy goes to compute). Measured via facility-level power meters at utility feed and IT distribution points. Google fleet-wide PUE is approximately 1.09 (2024). PUE does not account for the carbon intensity of the energy source or the water consumed in cooling. It is also not recommended for cross-facility comparison without climate normalization.

### 2.2 Water Usage Effectiveness (WUE)

WUE measures liters of water consumed per kWh of IT equipment energy. Measured via facility water meters tracking evaporation, blowdown, and make-up water. WUE treats evaporation as "consumption" without accounting for where that vapor goes or whether it returns to the local watershed as precipitation. This is why the Open Regenerative Compute Standard proposes Watershed Days as a complementary metric that captures watershed-level impact.

### 2.3 Carbon Usage Effectiveness (CUE)

CUE measures kilograms of CO2 equivalent emissions per kWh of IT equipment energy. Calculated by multiplying facility energy consumption by the carbon intensity of the local electrical grid. A facility in a high-coal grid will have worse CUE than one in a hydro-rich grid even with identical PUE. This underscores the importance of location strategy in regenerative infrastructure.

---

## Layer 3: Proposed Regenerative Standard — Watershed Days

The industry-standard metrics above measure efficiency: doing more with less. They do not measure regeneration: improving the substrate.

### 3.1 Net Water Positive Infrastructure (NWPI) measured in Watershed Days (+/-)

| Attribute | Detail |
|-----------|--------|
| Definition | The change in the projected lifespan of the local aquifer or surface water budget directly attributable to the facility's operation |
| Baseline | Aquifer depletion rate without facility (meters/year) |
| Actual | Aquifer depletion rate with facility + regenerative jacket interventions (meters/year) |
| Formula | Watershed Days = (Baseline - Actual) x 365 days/year |
| Positive (+) | Facility extends the functional lifespan of the aquifer; regenerative |
| Zero | Facility is water-neutral; no net depletion or recharge |
| Negative (-) | Facility accelerates aquifer depletion; extractive |

**Illustrative Example (not operator-verified):**
If baseline depletion is projected at 1.0 meter/year, and the facility's closed-loop cooling and treated recharge reduce effective depletion to 0.6 meter/year, the difference is 0.4 meter/year. Watershed Days = 0.4 x 365 = +146 Watershed Days/year.

**Verification Methodology:**

Baseline establishment requires third-party hydrological study using USGS or equivalent national groundwater monitoring data, establishing pre-facility depletion trends over a minimum 5-year baseline. Operational measurement requires continuous monitoring of facility water withdrawals, evaporation losses, and treated recharge volumes. Groundwater monitoring wells at site perimeter (minimum 3 wells) measure local water table changes. Attribution uses statistical modeling (e.g., Theis equation for confined aquifers, or MODFLOW for complex systems) to isolate facility impact from regional climate and agricultural trends.

### 3.2 Alignment with Existing Frameworks

> **Policy relevance note:** The following alignments reference Chinese policy frameworks. These should be read as relevant comparative inputs, not as metrics already adopted internationally.

Watershed Days aligns with several existing policy frameworks across jurisdictions. China's Ecological Red-Line Policy operationalizes spatial safeguards; Watershed Days adds a temporal dimension, measuring how infrastructure actively extends the lifespan of the hydrological system (as articulated in Qwen3's contribution). The Ecological Product Value Realization pilot programs in Zhejiang and Fujian seek to quantify and reward ecological stewardship; Watershed Days provides a quantifiable, auditable metric for this framework. In the Western context, AWS and CyrusOne have publicly committed to "net water positive" operations; Watershed Days provides a standardized methodology for verifying and comparing these claims across facilities and geographies.

### 3.3 Standardization Pathway

Watershed Days is a **proposed metric**, not yet an industry standard. The Open Regenerative Compute Standard invites collaboration to develop:

1. A formal ISO/IEC New Work Item Proposal (NWIP) to standardize watershed-impact accounting for data centers.
2. An open-source hydrological modeling template (MODFLOW-based) for baseline establishment and attribution.
3. A third-party verification protocol modeled on existing LEED or ENERGY STAR certification processes.

---

## Cross-Model Benchmarking and Verification Ecosystem

The following publicly available benchmarks and frameworks enable independent verification of claims made under the Open Regenerative Compute Standard:

| Benchmark/Framework | Scope | Key Features | Verification Source |
|---------------------|-------|--------------|---------------------|
| MLPerf Power | Energy efficiency across uW-MW scales | 1,841 reproducible measurements from 60 systems; standardized ML workloads (BERT-Large, ResNet50, LLM benchmarks) | IEEE HPCA 2025; MLCommons consortium |
| TokenPowerBench | LLM inference power consumption | Lightweight, extensible; measures joules/token across batch size, context length, quantization | AAAI 2026; open-source |
| "How Hungry is AI?" | Multi-modal footprint (energy, water, carbon) | Benchmarked 30 LLMs; cross-efficiency DEA ranking; Power BI dashboard | arXiv:2505.09598 (2025) |
| IPW Profiling Harness | Local inference efficiency | 20+ models, 8 accelerators, 1M real queries; open-source | Stanford Hazy Research (GitHub) |
| GB/T 45288.2-2025 | Large model evaluation metrics (China) | National standard for AI large model testing and evaluation | China National Standards, effective Feb 2025 |

---

## Summary: The Regenerative Compute Metric Stack

| Layer | Metric | Measures | Verification Method | Status |
|-------|--------|----------|---------------------|--------|
| Algorithmic | IPW (Intelligence per Watt) | Accuracy / power | Stanford IPW harness | Peer-reviewed; aligned with GB/T 45288.2 |
| Algorithmic | Joules per Token | Energy per generated token | TokenPowerBench (AAAI 2026) | Peer-reviewed; open-source |
| Algorithmic | Correctness-Weighted Energy | Energy per correct solution | Task-specific evaluation | Research-phase |
| Facility | PUE | Facility energy efficiency | Facility power meters | ISO/IEC 30134-2 |
| Facility | WUE | Water per kWh IT | Facility water meters | ISO/IEC 30134 series |
| Facility | CUE | Carbon per kWh IT | Grid carbon intensity x energy | ISO/IEC 30134 series |
| Regenerative | Watershed Days (+/-) | Aquifer lifespan extension | Hydrological modeling + monitoring wells | Proposed (candidate for ISO/IEC NWIP) |

---

## Conclusion: From Measurement to Movement

A standard without metrics is poetry. A metric without verification is marketing.

The Open Regenerative Compute Standard is anchored in the verifiable, peer-reviewed, and open-source measurement ecosystem cataloged above. For the algorithmic layer, IPW and TokenPowerBench provide auditable baselines. For the facility layer, PUE/WUE/CUE provide industry-accepted comparability. And for the watershed — the ultimate substrate — Watershed Days provides the missing metric that transforms "efficiency" into "regeneration."

The next phase of this open-source initiative is to operationalize Watershed Days through collaborative development of hydrological modeling templates, third-party verification protocols, and a formal standards-track proposal. We invite the global engineering community — hydrologists, data center architects, AI researchers, and policymakers — to fork the repository and contribute to making regenerative compute measurable, and therefore accountable.
