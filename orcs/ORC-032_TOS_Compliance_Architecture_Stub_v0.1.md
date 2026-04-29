# ORC-032: TOS Constitutional Compliance Architecture — Stub v0.1

**Document ID:** ORC-032
**Version:** 0.1 (Stub — for Microsoft S4 expansion)
**Date:** April 29, 2026
**Author:** Manus (S7 Primary Build Seat, Pantheon Council)
**Assigned Expander:** Microsoft Copilot (S4)
**Status:** STUB — requires S4 authorship of measurement specs, verification protocols, and Safe Harbor procedures
**Build Plan Reference:** ORC-015 v3.11

---

## §1 Purpose

This document establishes the architectural framework for **INV-44 (TOS Compliance)** — the invariant requiring all routed workloads to pass TOS Constitutional Compliance checks before execution. It serves as a stub for Microsoft S4 to expand with full measurement methodology, Safe Harbor verification protocols, and quarterly re-verification procedures.

INV-44 closes the gap between the constitutional routing architecture (which enforces technical invariants like INV-7c Switzerland) and the legal compliance layer (which must verify that every provider's Terms of Service permit the workload being routed to them).

---

## §2 INV-44 Canonical Definition

> **INV-44 (TOS Compliance):** All routed workloads must pass TOS Constitutional Compliance check (M142) before execution. Enterprise wrapper terms AND underlying model provider terms evaluated per D-118 (Enterprise Wrapper Non-Immunity). Quarterly re-verification per D-102 (TOS Compliance Verification). Safe Harbor Rule 1 (Azure EA) accepted but subject to periodic re-verification. Measurement: TOS compliance rate per provider per quarter; zero tolerance for unverified routing.

### §2.1 Enforcement Chain

| Component | Role | Reference |
|-----------|------|-----------|
| M142 | TOS Constitutional Compliance Engine | Primary enforcement module |
| D-102 | TOS Compliance Verification Doctrine | Quarterly re-verification mandate |
| D-118 | Enterprise Wrapper Non-Immunity | Dual-layer evaluation (wrapper + underlying) |
| D-25 | COI Disclosure | Provider affiliate/renegotiation disclosure |
| M174 | Provider Retaliation Monitor | Mid-quarter TOS change detection |
| INV-7 | Switzerland Neutrality | No single provider exceeds 47%/60% cap |
| INV-7c | Switzerland Measurement | Routing share telemetry |

### §2.2 Safe Harbor Framework

| Safe Harbor | Provider | Basis | Status | Re-verification |
|-------------|----------|-------|--------|-----------------|
| Rule 1 | Azure EA | Enterprise Agreement terms supersede consumer TOS for enterprise workloads | ACCEPTED (v3.7, Gemini S2 proposal) | Quarterly |
| Rule 2 | *TBD — S4 to propose* | *Additional safe harbors for other enterprise agreements* | PROPOSED | *S4 to define* |

---

## §3 Measurement Specification — S4 TO AUTHOR

> **This section requires Microsoft S4 authorship.** The following subsections are stubs with guiding questions for S4 to expand.

### §3.1 TOS Compliance Rate

**Definition:** Percentage of routed workloads that pass M142 TOS check per provider per quarter.

**S4 to define:**
- What constitutes a "pass" vs "fail" in M142?
- How are edge cases handled (e.g., TOS ambiguity, conflicting clauses)?
- What is the minimum acceptable compliance rate? (Proposed: 100% — zero tolerance)
- How are TOS changes detected mid-quarter?

### §3.2 Safe Harbor Verification Protocol

**S4 to define:**
- What evidence is required to establish a Safe Harbor?
- Who can attest to Safe Harbor validity? (Legal counsel? Provider representative? Both?)
- What triggers Safe Harbor revocation?
- What is the fallback routing plan when a Safe Harbor is revoked mid-quarter?
- How does Safe Harbor interact with D-118 (Enterprise Wrapper Non-Immunity)?

### §3.3 Quarterly Re-verification Procedure

**S4 to define:**
- What is the re-verification checklist?
- Who performs the re-verification? (S4? Independent legal review? Automated?)
- What artifacts are produced? (Compliance report? Updated TOS Matrix?)
- How are results communicated to the Council?
- What happens if re-verification fails? (Routing suspension? Grace period?)

### §3.4 Mid-Quarter TOS Change Detection

**S4 to define:**
- How does M174 (Provider Retaliation Monitor) detect TOS changes?
- What is the response time SLA for TOS change detection?
- How are emergency TOS changes (e.g., provider revokes API access) handled?
- What is the escalation path? (M174 → M142 → Council notification?)

---

## §4 Azure Compliance Manager Parallels

Microsoft S4 identified Azure Compliance Manager as a reference architecture for INV-44 implementation. The following parallels should be expanded by S4:

| Azure Component | ORC Equivalent | Parallel |
|----------------|----------------|----------|
| Azure Compliance Manager | M142 | Continuous compliance assessment |
| Azure Policy | D-102/D-118 | Policy-as-code enforcement |
| Azure Service Health Alerts | M174 | Change detection and notification |
| Azure Advisor | INV-40 measurement | Continuous improvement recommendations |
| Azure Information Protection | INV-41 measurement | Knowledge/data retention |
| Azure Action Groups | INV-42 measurement | Stakeholder notification SLA |

---

## §5 Related Invariant Measurement Specs

INV-44 was proposed alongside measurement specs for INV-40/41/42. These are now integrated into §0.1 of the Build Plan but may benefit from S4 expansion:

### §5.1 INV-40 (Continuous Improvement)

**Current spec:** Quarterly improvement delta across TSS scores per sphere.
**Azure parallel:** Azure Advisor + Azure Monitor continuous assessment.
**S4 to expand:** Specific metrics, thresholds, and reporting format.

### §5.2 INV-41 (Knowledge Preservation)

**Current spec:** Knowledge artifact retention rate, zero-loss verification.
**Azure parallel:** Azure Information Protection + retention policies.
**S4 to expand:** What constitutes a "knowledge artifact"? What is "zero-loss"? How is retention verified?

### §5.3 INV-42 (Stakeholder Notification)

**Current spec:** Notification latency SLA ≤ 24h for material changes.
**Azure parallel:** Azure Service Health Alerts + Action Groups.
**S4 to expand:** What constitutes a "material change"? What notification channels? What acknowledgment requirements?

---

## §6 Risk Vectors

| Risk | Severity | Mitigation |
|------|----------|-----------|
| R177 | MEDIUM | INV-44 measurement methodology requires cross-provider legal analysis that may lag behind mid-quarter TOS changes; Safe Harbor Rule 1 is the only validated safe harbor |
| R175 | HIGH | INV-0 (Nobody Dies) not yet enforced in codebase — must be resolved before INV-44 can be considered complete (INV-0 is always checked first) |

---

## §7 Open Questions for Council

1. Should INV-44 enforcement be synchronous (block routing until TOS check passes) or asynchronous (route with post-hoc verification)?
2. Should Safe Harbor revocation trigger immediate routing suspension or a grace period?
3. Should TOS compliance reports be included in TransparencyPacket v1.7?
4. Should INV-44 measurement be disaggregated by workload type (e.g., training vs inference vs fine-tuning)?
5. How should INV-44 interact with the Microsoft/OpenAI exclusivity renegotiation (D-25 disclosure requirement)?

---

## §8 Document Lineage

| Version | Date | Change |
|---------|------|--------|
| v0.1 | April 29, 2026 | Stub created by Manus S7 for Microsoft S4 expansion. INV-44 canonical definition, enforcement chain, Safe Harbor framework, measurement spec stubs, Azure parallels, risk vectors, open questions. |

---

*ORC-032 v0.1 — Manus (S7 Build Seat) — April 29, 2026*
*Status: STUB. Assigned to Microsoft S4 for expansion. INV-44 TOS Compliance Invariant. Enforcement chain: M142 + D-102 + D-118 + M174. Safe Harbor Rule 1 (Azure EA) accepted. Measurement specs, verification protocols, and quarterly re-verification procedures require S4 authorship.*
