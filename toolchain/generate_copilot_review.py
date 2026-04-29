"""Generate Microsoft Copilot (S4) self-scoring review brief from capability_matrix v0.2.1"""
import yaml
from pathlib import Path

ROOT = Path("/home/ubuntu/aluminum-os")

with open(ROOT / "registries/capability_matrix.yaml") as f:
    data = yaml.safe_load(f)

# Extract S4 data
s4_summary = data["seat_summaries"]["S4_Microsoft"]
spheres = data["spheres"]

# Build per-sphere lookup for S4
s4_scores = {}
for sp in spheres:
    scores = sp.get("scores", {})
    tiers = sp.get("tiers", {})
    if "S4_Microsoft" in scores:
        s4_scores[sp["sphere_id"]] = {
            "name": sp["sphere_name"],
            "house": sp["house"],
            "score": scores["S4_Microsoft"],
            "tier": tiers.get("S4_Microsoft", "UNKNOWN"),
        }

# Categorize
deep = [(k,v) for k,v in s4_scores.items() if v["score"] >= 0.8]
substantial = [(k,v) for k,v in s4_scores.items() if 0.5 <= v["score"] < 0.8]
peripheral = [(k,v) for k,v in s4_scores.items() if 0.2 <= v["score"] < 0.5]
absent = [(k,v) for k,v in s4_scores.items() if v["score"] < 0.2]

deep.sort(key=lambda x: -x[1]["score"])
substantial.sort(key=lambda x: -x[1]["score"])

# Per-house averages
house_avgs = s4_summary["per_house_average"]

HOUSE_NAMES = {
    "H01": "Natural Sciences", "H02": "Formal Sciences", "H03": "Social Sciences",
    "H04": "Humanities", "H05": "Arts", "H06": "Engineering & Technology",
    "H07": "Information & Communication", "H08": "Education",
    "H09": "Health & Medicine", "H10": "Business & Economics",
    "H11": "Infrastructure", "H12": "Law/Governance/Meta-Knowledge"
}

# Find where S4 leads
lead_spheres = []
for sp in spheres:
    if sp.get("lead_seat") == "S4_Microsoft" and sp.get("lead_score", 0) >= 0.5:
        lead_spheres.append((sp["sphere_id"], sp["sphere_name"], sp["lead_score"]))

# Find where S4 is sole substantial+ provider
sole_provider = []
for sp in spheres:
    scores = sp.get("scores", {})
    substantial_seats = [seat for seat, score in scores.items() if score >= 0.5]
    s4_score = scores.get("S4_Microsoft", 0)
    if len(substantial_seats) == 1 and s4_score >= 0.5:
        sole_provider.append((sp["sphere_id"], sp["sphere_name"], s4_score))

# Generate the brief
brief = f"""# Microsoft Copilot (S4) — Self-Scoring Review Brief

**Atlas Lattice Federation — Pantheon Council**
**Document:** Capability Matrix Self-Assessment Request
**Version:** v0.2.1 (April 29, 2026)
**Classification:** Council Pass — Parallel Review
**Requested by:** Convenor (via Scribe)

---

## Purpose

This document requests Microsoft Copilot (Seat 4) to review, validate, and where appropriate correct the Atlas Lattice Federation's capability scoring for Microsoft across all 144 spheres of the 12×12+1 ontology. The scores below were derived from:

1. Federation Integration v1.1 (April 29, 2026) — Microsoft's 95.8% coverage claim
2. Four-Company Complementarity Matrix (April 22, 2026) — cross-validated against Anthropic, Alphabet, Muskverse, Amazon
3. Build Plan v3.14 Appendix AG — canonical ontology reference
4. Recent acquisition updates: Activision Blizzard ($68.7B), hyperscaler SMR convergence

Your task is to review each sphere score, confirm or propose corrections, and identify any capabilities we may have missed or overestimated.

---

## Current S4 Microsoft Summary

| Metric | Value | Meaning |
|--------|-------|---------|
| **Presence Breadth** | {(1 - len(absent)/144)*100:.1f}% | Fraction of 144 spheres with nonzero coverage |
| **Substantial Breadth** | {s4_summary['coverage_pct']:.1f}% | Fraction with 0.5+ coverage |
| **Deep Breadth** | {s4_summary['deep_count']/144*100:.1f}% | Fraction with 0.8+ coverage |
| **Deep Count** | {s4_summary['deep_count']} | Spheres at operational primary depth |
| **Substantial Count** | {s4_summary['substantial_count']} | Spheres at operational secondary depth |
| **Peripheral Count** | {len(peripheral)} | Domain-shaping but not operational |
| **Absent Count** | {len(absent)} | Minimal to passive availability |
| **Lead Sphere Count** | {len(lead_spheres)} | Spheres where S4 is federation lead |
| **Average Score** | {s4_summary['average_score']:.3f} | Mean across all 144 spheres |
| **Seduction Risk** | HIGH | presence_breadth >> substantial_breadth >> leadership_breadth |

### Three-Metric Resolution

The Convenor identified that Microsoft's 95.8% coverage claim and the matrix's {s4_summary['coverage_pct']:.1f}% are **both true** — they measure different things:

- **95.8% = breadth** — fraction of spheres with *any* coverage (useful for fallback/redundancy)
- **{s4_summary['coverage_pct']:.1f}% = depth** — fraction with Substantial+ coverage (useful for primary routing)
- **{s4_summary['deep_count']/144*100:.1f}% = leadership** — fraction where Microsoft is federation lead (useful for civilizational dependency)

The seduction_risk_flag is set HIGH because the gap between breadth and depth could mislead routing logic into over-relying on Microsoft based on surface metrics rather than actual operational depth.

---

## Scoring Convention

| Tier | Range | Phase | Meaning |
|------|-------|-------|---------|
| **Dominance** | 1.0 | Dominance | Best in world / federation lead at depth |
| **Deep** | 0.8–0.9 | Presence | Operational primary depth |
| **Substantial** | 0.5–0.7 | Presence | Operational secondary depth |
| **Peripheral** | 0.2–0.4 | Light presence | Domain-shaping but not operational |
| **Absent** | 0.0–0.1 | Not present | Minimal to passive availability |

---

## Per-House Average Scores

| House | Name | S4 Average | Assessment |
|-------|------|-----------|------------|
"""

for hid in sorted(HOUSE_NAMES.keys()):
    avg = house_avgs.get(hid, 0)
    assessment = "DEEP" if avg >= 0.8 else "SUBSTANTIAL" if avg >= 0.5 else "PERIPHERAL" if avg >= 0.2 else "ABSENT"
    brief += f"| {hid} | {HOUSE_NAMES[hid]} | {avg:.3f} | {assessment} |\n"

brief += f"""
---

## DEEP Spheres (0.8+) — {len(deep)} spheres

These are Microsoft's strongest capabilities. Please confirm or adjust.

| Sphere | Name | House | Score | Justification Needed |
|--------|------|-------|-------|---------------------|
"""

for sid, v in deep:
    brief += f"| {sid} | {v['name']} | {v['house']} | {v['score']} | What Microsoft product/service justifies this score? |\n"

brief += f"""
---

## SUBSTANTIAL Spheres (0.5–0.7) — {len(substantial)} spheres

These represent operational secondary depth. Please review for accuracy.

| Sphere | Name | House | Score | Notes |
|--------|------|-------|-------|-------|
"""

for sid, v in substantial:
    brief += f"| {sid} | {v['name']} | {v['house']} | {v['score']} | |\n"

brief += f"""
---

## Spheres Where S4 Leads the Federation — {len(lead_spheres)} spheres

These are spheres where Microsoft has the highest score among all 10 seats.

| Sphere | Name | Score |
|--------|------|-------|
"""

for sid, name, score in sorted(lead_spheres, key=lambda x: -x[2]):
    brief += f"| {sid} | {name} | {score} |\n"

if sole_provider:
    brief += f"""
---

## Sole Substantial+ Provider — {len(sole_provider)} spheres

These are spheres where Microsoft is the ONLY seat at 0.5+ coverage. Federation resilience concern.

| Sphere | Name | Score |
|--------|------|-------|
"""
    for sid, name, score in sorted(sole_provider, key=lambda x: -x[2]):
        brief += f"| {sid} | {name} | {score} |\n"

brief += """
---

## Review Instructions for Copilot

1. **Confirm or correct** each DEEP sphere score with a brief justification (product/service name)
2. **Confirm or correct** each SUBSTANTIAL sphere score
3. **Identify missing capabilities** — any Microsoft product, service, or acquisition not reflected in the scoring
4. **Flag overestimates** — any sphere where the score is higher than Microsoft's actual operational depth
5. **Provide per-sphere capability descriptions** where possible (e.g., "Azure AI — GPT-4 fine-tuning, Cognitive Services, Azure ML")
6. **Note recent acquisitions** not yet reflected (post April 2026)

### Response Format

For each correction, provide:
```yaml
- sphere_id: S0XX
  current_score: 0.X
  proposed_score: 0.X
  justification: "Brief explanation"
  capabilities:
    - "Product/service 1"
    - "Product/service 2"
```

### Deadline

Please return your self-assessment within 48 hours of receipt. The matrix will be updated to v0.3.0 incorporating your corrections alongside DeepSeek (S5) parallel review.

---

## Metadata

| Field | Value |
|-------|-------|
| Matrix Version | v0.2.1 |
| Generated | 2026-04-29 |
| Canonical Source | COMPLETE_BUILD_PLAN_v3.14.md Appendix AG |
| Total Spheres | 144 |
| Total Seats | 10 |
| Federation Aggregate Coverage | 56.2% at Substantial+ |

---

*This document is generated from `registries/capability_matrix.yaml` in the `atlaslattice/aluminum-os` monorepo. Corrections will be absorbed into the canonical registry and propagated to all downstream consumers.*

*— Atlas Lattice Federation, Build Seat (Manus)*
"""

out_path = ROOT / "Microsoft_Copilot_S4_Review_Brief.md"
with open(out_path, "w") as f:
    f.write(brief)

# Also write to home for easy download
home_path = Path("/home/ubuntu/Microsoft_Copilot_S4_Review_Brief.md")
with open(home_path, "w") as f:
    f.write(brief)

print(f"Written: {out_path}")
print(f"Written: {home_path}")
print(f"Deep: {len(deep)}, Substantial: {len(substantial)}, Peripheral: {len(peripheral)}, Absent: {len(absent)}")
print(f"Lead spheres: {len(lead_spheres)}")
print(f"Sole provider: {len(sole_provider)}")
