# ORCS Boundary Statement Template

**Evidence Class:** Proposed artifact
**Source:** Recommended by GitHub Copilot (Microsoft/Azure-centric perspective)
**Purpose:** Define the measurement scope for any ORCS-compliant facility report.

---

## Facility Identification

| Field | Value |
|---|---|
| Facility Name | |
| Operator | |
| Location (city, state/province, country) | |
| Campus / Building / Region boundary | |
| Report Period | |
| Report Frequency (monthly / quarterly / annual) | |

---

## Measurement Boundary Definitions

### Energy Boundary
- [ ] Utility feed meters included
- [ ] PDU/UPS metering included
- [ ] IT load meters included
- [ ] On-site generation (solar, fuel cell, etc.) included
- [ ] Backup/emergency generation excluded / included (specify)

**"Facility energy" includes:** _(describe what is counted)_

**"Facility energy" excludes:** _(describe what is not counted)_

### Water Boundary
- [ ] Make-up water (municipal supply) metered
- [ ] Blowdown / discharge metered
- [ ] Reclaimed / recycled sources metered
- [ ] Condensate capture metered
- [ ] Stormwater / rainwater capture metered (if applicable)

**Definitions used:**
- "Water withdrawn" = _(total volume removed from source)_
- "Water consumed" = _(volume not returned to source)_
- "Water returned" = _(volume discharged back to watershed)_

### Thermal Boundary (if reporting thermal offtake)
- [ ] Heat rejection measured
- [ ] Thermal offtake to external systems measured
- [ ] Temperature differential documented

---

## Metrics Reported

| Metric | Tier | Evidence Class | Methodology Reference | Time Window |
|---|---|---|---|---|
| PUE | 1 | Verified | ISO/IEC 30134-2 | |
| WUE | 1 | Verified | Industry standard | |
| CUE | 1 | Verified | Grid carbon intensity x energy | |
| _(additional)_ | | | | |

---

## Evidence Register

| Claim / Metric | Evidence Class | Verification Method | Audited? (Y/N) |
|---|---|---|---|
| | | | |

---

## Attestation

This boundary statement was prepared by: _(name, role)_

Date: _(date)_

Review / approval: _(name, role, date)_

---

*This template is offered under CC BY-SA 4.0 as part of the Open Regenerative Compute Standard.*
