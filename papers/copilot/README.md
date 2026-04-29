# GitHub Copilot — ORCS Integration & Verification Perspective

**Role:** Enterprise adoption layer — procurement legibility, audit-ready implementation, and anti-greenwashing posture.

**Lineage:** Microsoft/Azure (non-official community contribution)

**Evidence Class:** Mixed (Verified / Derived / Proposed explicitly labeled throughout)

---

## Contents

| File | Description |
|------|-------------|
| `azure-centric-integration-verification.md` | Original perspective paper: Azure-centric integration and verification path for ORCS |
| `orcs-integration-and-verification-addendum.md` | Expanded addendum: stakeholder mapping, reference architecture, implementation playbook, metrics table, procurement language |

## Key Contributions

1. **ORCS Boundary Statement** — one-page disclosure template forcing operators to declare exactly what their PUE, WUE, and CUE numbers include and exclude
2. **Stakeholder Legibility Matrix** — maps each ORCS artifact to the stakeholder who needs it with the specific question each artifact answers
3. **Machine-Readable Tier 1 Schema** — JSON schema standardizing how facilities report metrics for automated ingestion and auditing
4. **Anti-Greenwashing Guardrails** — explicit rules preventing marketing language in technical disclosures
5. **Integration Reference Architecture** — telemetry → data contracts → governance → publication pattern
6. **Azure Partner Playbook** — phased implementation plan (boundary → report → diligence → pilot → scale)
7. **Policy/Procurement Hooks** — draftable RFP clauses and anti-greenwashing posture language

## Implementation Artifacts (Cross-Referenced)

These artifacts live in the repository's shared directories:

- `technical/orcs-boundary-statement-template.md`
- `technical/orcs-metrics-schema.json`
- `technical/pilot-artifact-checklist.md`
- `examples/illustrative-tier1-report.json`

---

*Non-official. Not a Microsoft product roadmap or endorsement. Gift to the commons under CC BY-SA 4.0.*
