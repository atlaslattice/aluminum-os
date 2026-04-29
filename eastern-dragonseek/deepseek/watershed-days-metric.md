# Watershed Days: A Hydrological Accountability Metric for Data Centers

*Proposed by: DeepSeek | April 2026 | CC BY-SA 4.0*

---

## 1. Problem Statement

Water Usage Effectiveness (WUE = Liters consumed / kWh IT load) is the industry standard metric for data center water performance. It is dangerously reductive for three reasons:

1. It counts all evaporation as "consumption" without tracking vapor destination (does it return as precipitation within the watershed?).
2. It ignores the source of water (renewable surface flow vs. fossil aquifer vs. municipal treated).
3. It provides no mechanism for crediting facilities that actively improve watershed health.

A facility with WUE = 0.5 L/kWh drawing from a critically depleted aquifer is rated identically to one drawing from a renewable surface source. This is not accountability. It is accounting theater.

## 2. Definition

**Watershed Days** measures the change in the projected lifespan of the local aquifer or surface water budget directly attributable to a facility's operation.

| Parameter | Formula |
|-----------|---------|
| Baseline depletion rate | D_base = aquifer decline (m/year) without facility |
| Facility-adjusted depletion rate | D_actual = aquifer decline (m/year) with facility + all regenerative interventions |
| Net Watershed Impact | NWI = D_base - D_actual |
| Watershed Days | WD = NWI * 365 / D_base |

A positive Watershed Days value means the facility is **extending** the life of the local water system. A negative value means it is accelerating depletion.

## 3. Calculation Framework

### Step 1: Baseline Hydrological Assessment

Establish the pre-facility aquifer depletion rate using:
- Historical well monitoring data (minimum 5 years)
- Regional groundwater model (MODFLOW or equivalent)
- Agricultural withdrawal records from local Water Resources Bureau
- Climate-adjusted precipitation and recharge projections

### Step 2: Facility Water Balance

Quantify all facility water flows:

| Flow Category | Measurement | Sign |
|---------------|-------------|------|
| Municipal/well intake | Metered at source | Negative |
| Cooling tower evaporation | Calculated from makeup rate | Negative |
| Condensate recovery | Metered at collection | Positive |
| Rainwater/stormwater capture | Metered at retention basin | Positive |
| Treated wastewater discharge to recharge | Metered at injection/infiltration point | Positive |
| CEA irrigation (if from recovered water) | Metered at greenhouse intake | Neutral (internal transfer) |
| AWG production | Metered at output | Positive |

### Step 3: Equity Weighting Multiplier

Not all water is equal. A liter returned to a critically depleted aquifer has more watershed value than a liter returned to a healthy system.

| Watershed Stress Level | Drought Index | Equity Multiplier |
|------------------------|---------------|-------------------|
| Normal | D0 or better | 1.0x |
| Moderate drought | D1 | 1.3x |
| Severe drought | D2 | 1.7x |
| Extreme drought | D3 | 2.3x |
| Exceptional drought | D4 | 3.0x |

Drought index sourced from US Drought Monitor or China Meteorological Administration equivalent.

### Step 4: Community Vulnerability Adjustment

If the facility's service radius includes communities with limited alternative water access, an additional vulnerability multiplier applies:

| Community Water Access | Vulnerability Multiplier |
|------------------------|--------------------------|
| Multiple redundant sources | 1.0x |
| Single primary source | 1.3x |
| Source under regulatory stress | 1.7x |
| Source in active depletion | 2.0x |

### Step 5: Final Calculation

```
Weighted_WD = Raw_WD * Equity_Multiplier * Vulnerability_Multiplier
```

## 4. Verification Requirements

Watershed Days claims must be independently verifiable:

1. **Open Data:** All metering data published to ORCS repository (anonymized if commercially sensitive, but volumes must be real).
2. **Third-Party Audit:** Annual hydrological audit by licensed hydrogeologist.
3. **Continuous Monitoring:** Real-time aquifer level monitoring with public dashboard.
4. **Peer Review:** Methodology and results subject to community review via ORCS GitHub issues.

## 5. Example: DeepSeek Hohhot

| Parameter | Value |
|-----------|-------|
| Baseline aquifer decline | 0.8 m/year (Yellow River Basin buffer zone) |
| Facility water intake | 180,000 m3/year |
| Treated recharge return | 54,000 m3/year (30%) |
| Condensate recovery | 22,000 m3/year |
| Stormwater capture | 8,000 m3/year |
| Net withdrawal | 96,000 m3/year |
| Regional agricultural withdrawal offset (CEA replacing open-field) | 120,000 m3/year |
| Net watershed contribution | +24,000 m3/year |
| Equity multiplier (D2 drought zone) | 1.7x |
| **Weighted Watershed Days** | **+146 days/year** |

## 6. Integration with Chinese Policy Frameworks

Watershed Days maps directly to China's Ecological Product Value Realization (EPVR) framework. See the companion document `qwen3/epvr-bridge-methodology.zh.md` for the full bridge calculation.

---

*This metric is offered as an open standard. Fork it. Improve it. Deploy it. The watershed remembers.*
