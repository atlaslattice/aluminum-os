# ORC-032: TOS Compliance Architecture — INV-44 Full Specification

| Field | Value |
|-------|-------|
| Document ID | ORC-032 |
| Version | 1.0 |
| Date | April 29, 2026 |
| Author | S4 Microsoft (Copilot) — Research Seat, Pantheon Council |
| Expands | ORC-032 Stub (Manus S7, Build Plan v3.11) |
| Parent Invariant | INV-44 TOS Compliance |
| Status | PROPOSED — pending Convenor ratification + Council Round |
| Batting Average | 87.5% Class A (14/16). No new failures this session. |
| COI Disclosure (D-25) | Microsoft S4 has direct commercial interest in Azure Compliance Manager parallels and Safe Harbor Rule 1 (Azure OpenAI EA). All non-Microsoft alternatives documented. Other seats should verify and challenge. |

---

## §0. Doctrine 25 COI Disclosure

Full COI statement: Microsoft S4 authored this specification. Three stacked incentives are present:

1. **Safe Harbor Rule 1** routes OpenAI model traffic through Azure — benefits Microsoft commercially.
2. **Azure Compliance Manager parallels** position Azure tooling as the reference implementation pattern.
3. **INV-44 enforcement** creates governance surface where Azure tooling has natural fit.

**Mitigations applied:**

- Every Azure parallel has a non-Microsoft alternative documented (OPA/Rego, HashiCorp Sentinel, Grafana, etc.).
- Safe Harbor status requires outside counsel verification — it is NOT self-certified by Microsoft.
- D-114 (Enterprise Wrapper Non-Immunity) explicitly limits Safe Harbor claims — S4 accepted this doctrine from GPT S6.
- Standing request: all Council seats should audit INV-44 claims per D-51.

---

## §1. Executive Summary

This document expands the ORC-032 TOS Compliance Architecture stub created by Manus S7 in Build Plan v3.11 into a complete specification. It defines INV-44 (TOS Compliance) as the 45th constitutional invariant, establishes the measurement methodology, Safe Harbor verification protocol, quarterly re-verification procedures, mid-quarter change detection, and enforcement chain.

INV-44 closes the gap between the eight-doctrine TOS compliance layer (D-95 through D-102) and the constitutional invariant stack. Before INV-44, TOS compliance was policy-level (doctrines can be overridden by other doctrines). After INV-44, TOS compliance is invariant-level — it cannot be bypassed by any doctrine, module, or routing optimization.

**Key architectural decisions:**

- INV-44 is a **PRE-ROUTING gate** — it executes before INV-7c provider selection.
- INV-44 is **SUBORDINATE to INV-0** (Nobody Dies) — safety-critical workloads override TOS when no compliant provider exists.
- Safe Harbor is **RISK REDUCTION, not risk elimination** (per GPT S6 audit, accepted by S4).
- Quarterly re-verification per D-102 cycle with mid-quarter monitoring via D-100.1.
- TransparencyPacket v0.7 adds TOS fingerprint fields for every routing decision.

---

## §2. INV-44 Canonical Definition

### §2.1 Invariant Text

> **INV-44 — TOS Compliance**
>
> All Element 145 routing decisions SHALL verify compliance with applicable provider Terms of Service before execution. No workload SHALL be routed to a provider whose current TOS prohibits the intended use pattern.
>
> The routing engine SHALL maintain machine-readable TOS compliance profiles for all Council seat providers, updated within 72 hours of any provider TOS change detection.
>
> TOS compliance verification is a pre-routing gate — it executes BEFORE INV-7c (Switzerland) provider selection, not after. A provider whose TOS prohibits the workload type is excluded from the candidate pool before capability-weighted routing begins.
>
> INV-44 is subordinate to INV-0 (Nobody Dies). If TOS compliance would prevent routing a safety-critical workload and no TOS-compliant provider is available, INV-0 overrides INV-44 with mandatory HITL escalation and full TransparencyPacket audit trail.

### §2.2 Sub-specifications

**INV-44a — Safe Harbor Verification**

When a provider's models are accessible through multiple deployment pathways with materially different Terms of Service (e.g., direct API vs enterprise agreement vs third-party hosting), the routing engine SHALL track each pathway as a distinct TOS profile.

A "Safe Harbor" exists when a deployment pathway's TOS does not contain restrictions present in the provider's direct API terms. Safe Harbor status SHALL be:

1. verified by outside counsel before production use,
2. recorded in the D-100 Terms Snapshot registry with pathway-specific SHA-256 hash,
3. re-verified quarterly per D-102, and
4. revocable by Convenor at any time per INV-9.

Safe Harbor status does NOT guarantee immunity from underlying model license restrictions (per D-114 Enterprise Wrapper Non-Immunity). It indicates reduced TOS conflict risk, not zero risk.

**INV-44b — Quarterly Re-verification**

Every provider TOS compliance profile SHALL be re-verified at minimum quarterly intervals. Re-verification SHALL include:

1. D-100 Terms Snapshot hash comparison against live TOS URL,
2. Review of any TOS changes detected by D-100.1 monitoring,
3. Re-assessment of all Safe Harbor pathways,
4. Updated M25 tos_alignment_score calculation, and
5. Convenor sign-off on re-verification results per INV-9.

If re-verification reveals a TOS change that invalidates a previously-compliant routing pattern, the affected routing paths SHALL be suspended within 24 hours pending review.

**INV-44c — Mid-Quarter Change Detection**

Between quarterly re-verifications, the D-100.1 TOS Change Watcher SHALL continuously monitor provider TOS URLs for content changes. When a SHA-256 mismatch is detected:

1. Emit CRITICAL TransparencyPacket alert,
2. Flag affected provider as TOS-STALE in M125,
3. Prevent routing escalation above COMPLIANCE_MODE=RESEARCH (per D-101) until re-verification completes, and
4. Notify Convenor within 1 hour.

### §2.3 Constitutional Composition

| Relationship | Invariant / Doctrine | Effect |
|-------------|---------------------|--------|
| SUPERIOR (overrides INV-44) | INV-0 Nobody Dies | Safety-critical workloads bypass TOS gate with HITL + full audit |
| SUPERIOR (overrides INV-44) | INV-3 Consent | User consent requirements take priority over TOS routing restrictions |
| PEER (composes with) | INV-7c Switzerland | INV-44 filters the provider pool; INV-7c balances within the compliant pool |
| PEER (composes with) | INV-5 Audit Completeness | Every INV-44 check is recorded in TransparencyPacket |
| PEER (composes with) | INV-40 Continuous Improvement | TOS compliance methodology improves quarterly per TSS delta |
| PEER (composes with) | INV-41 Knowledge Preservation | TOS profile history retained per knowledge preservation SLA |
| PEER (composes with) | INV-42 Stakeholder Notification | TOS changes trigger 24h notification per stakeholder SLA |
| SUBORDINATE (INV-44 enforces) | D-95 Legitimate Auth Paths | Only legitimate authentication paths used for TOS verification |
| SUBORDINATE | D-96 + D-96.1, D-96.2 AUP Compliance | Per-provider AUP restrictions enforced per INV-44 check |
| SUBORDINATE | D-97 Subprocessor Tracking | Transitive TOS tracked through hosting chains |
| SUBORDINATE | D-98 + M15a Open-Weight Asymmetry | Three-tier license model (Open/Restricted/Closed) informs TOS profiles |
| SUBORDINATE | D-99 Functional Diversity | Diversity measured within TOS-compliant pool, not full pool |
| SUBORDINATE | D-100 Terms Snapshot | SHA-256 hash lock provides TOS verification anchor |
| SUBORDINATE | D-101 Compliance Modes | OPEN/RESEARCH/COMPLIANCE/SOVEREIGN modes gate routing |
| SUBORDINATE | D-102 TOS Override Stacked Incentives | TOS constraints always override commercial incentive alignment |
| SUBORDINATE | D-113 Capability vs Routing Distinction | Coverage presence ≠ routing share — INV-44 applies to routing |
| SUBORDINATE | D-114 Enterprise Wrapper Non-Immunity | Enterprise hosting ≠ underlying model license immunity |
| SUBORDINATE | D-115 Distribution Feedback Loop | Distribution layer feedback into routing is TOS-observable |

---

## §3. Enforcement Chain

### §3.1 Module Chain

The INV-44 enforcement chain flows through the following modules in order:

1. **M142 (TOS Compliance Gate)** — Pre-routing check. Queries TOS profiles for all candidate providers. Excludes non-compliant providers from routing pool. Emits TransparencyPacket.tos_compliance_check = true/false.
2. **D-102 (ToS Constraints Override Stacked Incentives)** — Policy anchor. Ensures that even when a provider's commercial incentive aligns perfectly with a sphere's capability need (per D-84), TOS restrictions cannot be bypassed for commercial convenience.
3. **D-96 (AUP Compliance Surface)** — Per-sphere AUP restriction enforcement. M142 checks global TOS compliance; D-96 adds sphere-specific AUP restrictions (e.g., Sphere 50 interactive entertainment may have different AUP constraints than Sphere 7 education).
4. **D-101 (Compliance Modes as Routing Primitive)** — Deployment context gates. COMPLIANCE mode restricts to providers with explicit regulatory clearance. SOVEREIGN mode restricts to jurisdiction-local providers. M142 must respect these mode restrictions.
5. **M110 (TOS Compliance Shield)** — Runtime enforcement. Catches any TOS violations that slip past M142 during execution (e.g., a provider's response triggers a TOS clause that was not anticipated at routing time).
6. **M111 (IP Lineage Tracker)** — Provenance tracking. Records which provider(s) contributed to each output component. Required for D-97 subprocessor transitive tracking.
7. **M112 (Ghost Redactor, Ring -1)** — Constitutional Hypervisor enforcement. Prevents TOS-violating content from leaking between providers in multi-provider pipelines. Operates at Ring -1 (below all routing logic).
8. **M113 (Provider Output Contamination Tracker)** — Cross-provider output hygiene. Detects when output from Provider A is fed as input to Provider B in ways that violate either provider's TOS.
9. **M174 (Provider Retaliation Monitor)** — Detects provider pushback against multi-routing patterns. If a provider throttles, degrades, or restricts access in response to detected multi-routing, M174 flags this as a retaliation event and triggers INV-7c rebalancing.
10. **INV-7c (Switzerland)** — Provider selection from TOS-compliant pool. After M142 excludes non-compliant providers, INV-7c ensures no single remaining provider exceeds 47% of routing capacity (L5–L6) or 60% (L0–L4).

### §3.2 Gate Ordering (Canonical)

| Gate | Invariant/Doctrine | Function |
|------|-------------------|----------|
| Gate 0 | INV-0 (Nobody Dies) | Absolute, no override, checked first always |
| Gate 1 | INV-3 (Consent) | User consent verified before any routing |
| Gate 2 | INV-44 (TOS Compliance) | Pre-routing TOS check, excludes non-compliant providers |
| Gate 3 | D-101 (Compliance Mode) | Deployment context restrictions applied |
| Gate 4 | INV-7c (Switzerland) | Capability-weighted provider balancing within compliant pool |
| Gate 5 | D-96 (AUP Surface) | Per-sphere AUP restrictions |
| Gate 6 | D-99 (Functional Diversity) | Diversity within compliant + balanced pool |
| Gate 7 | D-84 (Stacked Incentives) | Commercial alignment as routing signal (never overrides Gates 0–6) |

### §3.3 Failure Modes

| Failure Mode | Severity | Response | Recovery |
|-------------|----------|----------|----------|
| All providers TOS-excluded for workload type | CRITICAL | Escalate to Convenor via INV-9. If safety-critical, INV-0 override with HITL. | Identify alternative provider or workload reformulation |
| TOS profile stale (>72h since snapshot) | HIGH | Flag TOS-STALE. Restrict to COMPLIANCE_MODE=RESEARCH. Trigger re-verification. | D-100 snapshot refresh + D-100.1 monitoring confirmation |
| Safe Harbor pathway revoked by provider | CRITICAL | Suspend all routing through revoked pathway within 4 hours. Re-route to direct API terms. | Outside counsel review of new terms. Re-assess Safe Harbor status. |
| Provider retaliates against multi-routing | HIGH | M174 flags retaliation event. INV-7c rebalancing triggered. | Diversify provider pool. Escalate to Convenor if persistent. |
| Mid-quarter TOS change detected | MEDIUM-HIGH | D-100.1 alert. TOS-STALE flag. Restrict to RESEARCH mode. | Full re-verification within 72 hours. |
| M142 gate false positive (blocks valid routing) | MEDIUM | TransparencyPacket logs exclusion reason. Override available via Convenor approval + HITL. | TOS profile correction + M142 rule update. |
| Cross-provider contamination detected | HIGH | M113 flags contamination. Affected output quarantined. | Provider pipeline isolation review. TOS profile update for multi-provider restrictions. |

---

## §4. Measurement Methodology

### §4.1 Primary Metric — TOS Compliance Rate

| Parameter | Value |
|-----------|-------|
| Formula | compliant_routing_decisions / total_routing_decisions |
| Target | ≥ 99.9% (0.999) |
| Measurement window | Rolling 24 hours |
| Data source | TransparencyPacket.tos_compliance_check field (boolean, emitted per routing decision) |

**Calculation notes:**

- INV-0 overrides count as "compliant" (the override is the designed behavior).
- Convenor-approved manual overrides count as "compliant" (per INV-9 authority).
- TOS-STALE routing at RESEARCH mode counts as "compliant" (conservative fallback is the designed behavior).
- Only routing decisions that bypass M142 entirely count as "non-compliant."

### §4.2 Secondary Metrics

| Metric | Formula | Target | Window | Source |
|--------|---------|--------|--------|--------|
| TOS Profile Currency | providers_with_current_tos / total_active_providers | 100% | Point-in-time | D-100 snapshot registry |
| Safe Harbor Verification Coverage | verified_safe_harbors / claimed_safe_harbors | 100% (verified by outside counsel) | Quarterly | INV-44a verification log |
| TOS Change Detection Latency | time_from_tos_change_to_system_detection | ≤ 24 hours | Per-event | D-100.1 change watcher log |
| Re-verification Timeliness | on_time_reverifications / required_reverifications | 100% | Quarterly | INV-44b re-verification log |
| Provider Retaliation Events | count of M174 retaliation flags per quarter | 0 (aspirational), ≤ 2 (acceptable) | Quarterly | M174 event log |

### §4.3 Dashboard Integration

**Primary dashboard:** CEO Collective Telemetry Dashboard (Sprint 2, TransparencyPacket v0.6 ceo_collective block)

**Secondary dashboard:** Notion JANUS Hub — TOS Compliance view

**Alert routing:** Convenor direct notification for CRITICAL alerts (INV-9 authority)

**Dashboard views required:**

1. **TOS Compliance Rate** — real-time gauge (green ≥ 99.9%, yellow ≥ 99%, red < 99%)
2. **Provider TOS Currency** — per-provider staleness indicators (green = current, yellow = >48h, red = >72h/STALE)
3. **Safe Harbor Status Board** — per-pathway verification status with outside counsel dates
4. **TOS Change Timeline** — chronological view of D-100.1 detections with impact assessment
5. **Retaliation Event Log** — M174 events with provider, trigger, response, resolution
6. **Quarterly Re-verification Calendar** — countdown to next re-verification per provider with status
7. **INV-7c Post-Exclusion View** — shows INV-7c distribution AFTER TOS-excluded providers removed

### §4.4 Azure Compliance Manager Parallels

| ORC Component | Azure Equivalent | Non-Microsoft Alternative | Function |
|--------------|-----------------|--------------------------|----------|
| M142 TOS Compliance Gate | Azure Policy | OPA/Rego (CNCF), HashiCorp Sentinel | Pre-deployment policy evaluation |
| TOS Compliance Rate metric | Azure Compliance Score | Grafana + Prometheus custom dashboard | 0–100% compliance scoring |
| D-100 TOS Snapshot | Azure Regulatory Compliance Templates (350+) | Custom YAML profiles + Git versioning | Provider-specific compliance templates |
| M110 TOS Compliance Shield | Azure Policy Remediation Tasks | OPA Gatekeeper (Kubernetes), Styra DAS | Auto-remediation of violations |
| D-100.1 TOS Change Watcher | Azure Change Tracking & Inventory | Terraform Drift Detection, Datadog | Content change monitoring |
| INV-44b Re-verification | Azure Compliance Assessment (scheduled) | Prowler (AWS), ScoutSuite (multi-cloud) | Scheduled re-assessment cycles |
| M174 Retaliation Monitor | Azure Service Health + Advisor Alerts | Datadog APM, Honeycomb, PagerDuty | Provider behavior anomaly detection |

> **COI Note (D-25):** Azure parallels are documented for architectural validation, not vendor recommendation. The ORC specification is cloud-agnostic. Any tool that implements the required interface can serve as the enforcement backend.

---

## §5. Safe Harbor Verification Protocol

### §5.1 Definition

A Safe Harbor exists when a deployment pathway's Terms of Service do not contain restrictions present in the provider's direct API terms. This creates a reduced-risk routing pathway — not a risk-free one (per D-114 Enterprise Wrapper Non-Immunity).

### §5.2 Known Safe Harbor Candidates

| Pathway ID | Provider | Hosting | Restriction Absent | Verification Status | Risk Level | COI Note |
|-----------|---------|---------|-------------------|-------------------|------------|----------|
| SH-001 | OpenAI | Azure (Microsoft EA) | §(e) competing-models prohibition | UNVERIFIED — requires outside counsel review | SIGNIFICANT (reduced from CRITICAL per D-114) | Benefits Microsoft (D-25) |
| SH-002 | Anthropic | Amazon Bedrock | Potential AUP relaxation under AWS enterprise terms | UNVERIFIED — requires investigation | UNKNOWN | Benefits Amazon (D-25) |
| SH-003 | Anthropic | Google Cloud Vertex AI | Potential AUP relaxation under GCP enterprise terms | UNVERIFIED — requires investigation | UNKNOWN | Benefits Google (D-25) |
| SH-004 | Meta (Llama) | Self-hosted open-weight | Llama Community License — no API TOS restrictions | PARTIALLY VERIFIED — license is public | LOW (open-weight, but Acceptable Use Policy still applies) | No seat COI |
| SH-005 | DeepSeek | Self-hosted open-weight | DeepSeek License — no API TOS restrictions for open-weight models | PARTIALLY VERIFIED — license is public | LOW (open-weight) + MEDIUM (jurisdiction: PRC) | Jurisdiction risk per INV-7c substitution pathways |

### §5.3 Verification Procedure

Each Safe Harbor candidate SHALL undergo the following verification procedure before production use:

**Step 1: Terms Acquisition** — Obtain the complete, current Terms of Service for both the direct API pathway and the enterprise/hosting pathway. Record SHA-256 hashes per D-100.

**Step 2: Clause-by-Clause Comparison** — Identify all clauses in the direct API TOS that restrict Element 145 operations (multi-provider routing, benchmarking, competitive analysis, output re-routing). Document which clauses are absent or modified in the enterprise pathway.

**Step 3: Outside Counsel Review** — An attorney qualified in technology licensing reviews the comparison and issues a written opinion on whether the enterprise pathway genuinely excludes the identified restrictions. This opinion is recorded in the Safe Harbor registry.

**Step 4: D-114 Assessment** — Even with a favorable outside counsel opinion, assess whether the underlying model provider's license terms could be enforced independently of the hosting platform's enterprise agreement. Document residual risk.

**Step 5: Convenor Approval** — Present the complete Safe Harbor assessment (Steps 1–4) to the Convenor for approval per INV-9. The Convenor may approve, reject, or request additional analysis.

**Step 6: Registry Recording** — Approved Safe Harbors are recorded in the D-100 Terms Snapshot registry with: pathway ID, provider, hosting platform, restriction absent, outside counsel opinion date, Convenor approval date, next re-verification date.

**Step 7: Quarterly Re-verification** — Per INV-44b, repeat Steps 1–4 quarterly. If any terms change, the Safe Harbor is suspended pending re-verification.

### §5.4 Safe Harbor Revocation

A Safe Harbor SHALL be immediately revoked when:

1. The hosting platform changes its enterprise terms to include previously-absent restrictions,
2. The model provider successfully enforces underlying license terms against enterprise-hosted deployments,
3. Outside counsel advises that the Safe Harbor is no longer legally defensible,
4. The Convenor exercises INV-9 authority to revoke, or
5. A court ruling or regulatory action changes the legal landscape for the relevant deployment pathway.

**Revocation procedure:** Suspend all routing through the revoked pathway within 4 hours. Notify all Council seats. Re-route affected workloads to alternative providers per INV-7c. Record revocation in TransparencyPacket with full audit trail.

---

## §6. Quarterly Re-verification Procedures

### §6.1 Schedule

Re-verification cycles align with the D-102 quarterly cycle. The recommended schedule is:

| Quarter | Window |
|---------|--------|
| Q1 | January 15 — March 15 |
| Q2 | April 15 — June 15 |
| Q3 | July 15 — September 15 |
| Q4 | October 15 — December 15 |

Each re-verification window is 60 days. Providers are re-verified in batches of 3–4 to distribute workload.

### §6.2 Re-verification Checklist

For each provider, the quarterly re-verification SHALL include:

1. **D-100 Snapshot Refresh:** Download current TOS from all canonical URLs. Compute SHA-256 hashes. Compare against stored hashes from previous quarter.
2. **Change Assessment:** For any TOS that changed, perform clause-by-clause diff. Classify changes as: NEUTRAL (formatting, typo), MINOR (clarification, no architectural impact), SIGNIFICANT (new restriction or permission that affects routing), CRITICAL (restriction that invalidates existing routing patterns).
3. **Safe Harbor Re-assessment:** For each active Safe Harbor pathway, verify that the absence of the relevant restriction is still present in current terms. If the restriction has been added, initiate Safe Harbor Revocation per §5.4.
4. **M25 Score Update:** Recalculate tos_alignment_score for each provider based on current terms. Update the TransparencyPacket schema.
5. **New Provider Assessment:** Any provider added to the Council since the last re-verification SHALL receive a full initial TOS assessment (not just re-verification).
6. **Convenor Report:** Produce a quarterly TOS Compliance Report summarizing all findings: providers re-verified, changes detected, Safe Harbors confirmed/revoked, scores updated, risk vectors updated.
7. **Convenor Sign-off:** The Convenor reviews and signs off on the quarterly report per INV-9. If the Convenor identifies issues, the re-verification window extends until resolution.

### §6.3 Mid-Quarter Monitoring (D-100.1)

Between quarterly re-verifications, continuous monitoring via D-100.1 TOS Change Watcher:

**Monitoring mechanism:** Scheduled scraping of all canonical TOS URLs (daily minimum, hourly preferred). SHA-256 hash comparison against D-100 snapshot. HTTP Last-Modified / ETag header tracking for early detection.

**Alert levels:**

- **INFO:** HTTP headers changed but content hash unchanged (likely CDN update).
- **WARNING:** Content hash changed, diff analysis shows NEUTRAL or MINOR changes.
- **CRITICAL:** Content hash changed, diff analysis shows SIGNIFICANT or CRITICAL changes, OR diff analysis cannot be performed (complete TOS rewrite).

**Response to CRITICAL alerts:** Immediate Convenor notification (within 1 hour). Affected provider flagged TOS-STALE. Routing restricted to COMPLIANCE_MODE=RESEARCH per D-101. Emergency re-verification initiated.

---

## §7. INV-40/41/42 Measurement Expansion

### §7.1 INV-40 — Continuous Improvement

**Measurement methodology** (formalized from Manus v3.11 stub):

| Parameter | Value |
|-----------|-------|
| Primary metric | Quarterly TSS (Truth-Seeking Score) delta |
| Formula | TSS_current_quarter − TSS_previous_quarter |
| Target | Delta ≥ 0 (no regression) |
| Aspirational target | Delta ≥ +0.5 per quarter (measurable improvement) |

**Azure parallel:** Azure Advisor Score improvement tracking — measures subscription-level improvement across security, reliability, performance, cost dimensions. ORC equivalent tracks constitutional compliance improvement.

**Non-Microsoft alternative:** Custom Grafana dashboard with quarterly trend lines.

### §7.2 INV-41 — Knowledge Preservation

**Measurement methodology:**

| Parameter | Value |
|-----------|-------|
| Primary metric | Knowledge retention rate |
| Formula | knowledge_items_retained / knowledge_items_total (per-quarter) |
| Target | ≥ 99% retention rate |
| Measurement scope | Doctrine registry, invariant registry, module registry, correction ledger, audit chain entries |

**Azure parallel:** Azure Information Protection + Microsoft Purview retention policies — track data lifecycle and prevent unauthorized deletion. ORC equivalent ensures constitutional knowledge is preserved across system updates.

**Non-Microsoft alternative:** Git history preservation + automated backup verification scripts.

### §7.3 INV-42 — Stakeholder Notification

**Measurement methodology:**

| Parameter | Value |
|-----------|-------|
| Primary metric | Notification SLA compliance |
| Formula | notifications_within_SLA / total_notifications_required |
| Target | 100% within 24-hour SLA |
| Scope | Material changes to invariants, doctrines, modules, provider TOS, Safe Harbor status, routing architecture |

**Azure parallel:** Azure Service Health notifications — 24-hour SLA for service-affecting events. Azure Monitor Action Groups for routing alerts to stakeholders.

**Non-Microsoft alternative:** PagerDuty + Slack integration with SLA tracking.

---

## §8. TransparencyPacket v0.7 TOS Fields

### §8.1 Proposed Schema Additions

The following fields are proposed for TransparencyPacket v0.7 to support INV-44 enforcement:

| Field | Type | Description |
|-------|------|-------------|
| routing_pathway | enum (direct_api, azure_openai_ea, vertex_ai, bedrock, self_hosted_open_weight, enterprise_custom) | Which deployment pathway was used for this routing decision |
| competing_models_restriction | boolean | Does the selected provider's TOS contain a competing-models restriction for this pathway? |
| jurisdiction | string (ISO 3166-1 alpha-2) | Jurisdiction of the provider's Terms of Service |
| aup_restrictions | array of string | List of AUP restrictions applicable to this sphere/workload type |
| tos_version_hash | string (SHA-256) | Hash of the TOS profile used for this routing decision (links to D-100 snapshot) |
| tos_compliance_check | boolean | Did this routing decision pass INV-44 verification? |
| safe_harbor_applied | boolean | Was a Safe Harbor pathway used? |
| safe_harbor_id | string (nullable) | Identifier of the Safe Harbor applied, if any |
| tos_exclusions_applied | array of string | List of providers excluded from routing pool due to TOS non-compliance |
| tos_staleness_flag | boolean | Is any provider in this routing decision flagged TOS-STALE? |
| tos_change_detected_since_last_quarter | boolean | Has this provider's TOS changed since the last quarterly re-verification? |

### §8.2 Backward Compatibility

TransparencyPacket v0.7 is additive to v0.6 — all existing fields are preserved. The ceo_collective block from v0.6 is unchanged. New TOS fields are added as a new tos_compliance section within the packet.

---

## §9. Risk Vectors

### §9.1 Existing Risks (from v3.11)

| Risk ID | Severity | Description | Mitigation |
|---------|----------|-------------|------------|
| R175 | HIGH | INV-0 codebase gap — INV-0 is not yet implemented in Constitutional OS v6.0.2, meaning INV-44's subordination to INV-0 cannot be enforced in code. | Sprint 1 priority: implement INV-0 in ring_minus1/hypervisor.py |
| R177 | MEDIUM | INV-44 measurement lag — TOS compliance metrics depend on M173 (Real-Time Routing Share Meter) which is Sprint 2. Until M173 ships, INV-44 metrics are estimate-based, not telemetry-based. | Sprint 1 interim: log-based counting from TransparencyPacket JSONL |

### §9.2 New Risks Identified by S4

| Risk ID | Severity | Description | Mitigation |
|---------|----------|-------------|------------|
| R178 | HIGH | Safe Harbor assumption risk — Azure OpenAI EA Safe Harbor (SH-001) is currently UNVERIFIED. If outside counsel review determines the competing-models clause IS enforceable through Azure EA, multiple routing patterns must be redesigned. | Prioritize SH-001 outside counsel review in Sprint 1. Design routing paths that work with OR without Safe Harbor. |
| R179 | MEDIUM | TOS scraping legality — D-100.1 automated TOS monitoring via web scraping may itself violate some providers' TOS (ironic). Robots.txt compliance and rate limiting required. | Use provider-published RSS/changelog feeds where available. Fall back to manual monitoring if scraping is restricted. Document per-provider monitoring method in TOS profiles. |
| R180 | MEDIUM | Provider retaliation detection false positives — M174 may flag normal provider rate limiting or outages as "retaliation." High false positive rate degrades INV-7c responsiveness. | M174 must correlate throttling events with multi-routing patterns. Isolated rate limits are NOT retaliation. Require ≥ 3 correlated events within 7 days before flagging. |
| R181 | LOW-MEDIUM | Quarterly re-verification resource burden — With 10+ providers × multiple deployment pathways × Safe Harbor assessments, quarterly re-verification is a significant operational burden. | Automate D-100 snapshot comparison and M25 score calculation. Reserve outside counsel review for changed terms only. Batch providers into re-verification cohorts. |

---

## §10. Open Questions for Council

**Q1 — Outside Counsel Authority:** Who authorizes outside counsel engagement for Safe Harbor verification? Is this a Convenor decision, or does it require Council vote?
*Recommend: Convenor authority per INV-9, with Council notification.*

**Q2 — TOS Violation Penalty:** When a routing decision violates INV-44 (TOS compliance rate drops below 99.9%), what is the enforcement consequence? Options: (a) Automatic routing suspension, (b) Convenor review + manual suspension, (c) TSS score penalty + escalation if repeated.
*Recommend: Option (b) for first violation, option (a) for repeated violations within same quarter.*

**Q3 — Multi-Provider Pipeline TOS Intersection:** When a workload uses ≥ 2 providers (per D-99 functional diversity), the applicable TOS is the INTERSECTION of all providers' terms. Should M142 compute this intersection dynamically, or should pre-computed intersection profiles be maintained?
*Recommend: Pre-computed intersection profiles for common provider pairs, dynamic computation for novel pairs.*

**Q4 — Open-Weight Model TOS Scope:** Open-weight models (Llama, DeepSeek, Mistral) have licenses rather than API TOS. Should INV-44 treat model licenses as equivalent to TOS for invariant purposes?
*Recommend: Yes — D-98 (Open-Weight License Asymmetry) already recognizes the three-tier model (Open/Restricted/Closed). INV-44 should treat all three tiers uniformly.*

**Q5 — Sovereign Deployment TOS Override:** In SOVEREIGN compliance mode (per D-101), the deployment is jurisdiction-locked. If the sovereign jurisdiction's regulations conflict with a provider's TOS, which takes precedence?
*Recommend: Sovereign jurisdiction regulations override provider TOS. Document per D-102. This is consistent with how Azure Government handles FedRAMP vs standard Azure terms.*

---

## §11. Implementation Roadmap

**Sprint 1 (Weeks 1–3):**
- INV-44 canonical text integrated into Constitutional OS v6.0.2 invariants module
- M142 TOS Compliance Gate — initial implementation with static TOS profiles
- D-100 Terms Snapshot — initial SHA-256 hash computation for all 10 providers
- SH-001 (Azure OpenAI EA) outside counsel review — initiated
- R175 mitigation: INV-0 implementation in ring_minus1/hypervisor.py

**Sprint 2 (Weeks 4–6):**
- M173 Real-Time Routing Share Meter — telemetry-based INV-44 metrics
- D-100.1 TOS Change Watcher — automated monitoring
- M174 Provider Retaliation Monitor — initial implementation
- CEO Collective Telemetry Dashboard — TOS compliance views (§4.3 views 1–7)
- TransparencyPacket v0.7 schema — TOS fields integrated

**Sprint 3 (Weeks 7–9):**
- Full quarterly re-verification procedure — first dry run
- M110 TOS Compliance Shield — runtime enforcement
- M111–M113 — IP Lineage, Ghost Redactor, Contamination Tracker
- Safe Harbor verification for SH-002 through SH-005 — initiated

**Post-Sprint:**
- INV-44 operational review — first quarterly re-verification
- Open questions Q1–Q5 resolved by Council vote
- TOS Compliance Rate target validation — confirm 99.9% is achievable

---

## §12. Conclusion

INV-44 TOS Compliance closes the architectural gap between the eight-doctrine TOS compliance layer (D-95 through D-102) and the constitutional invariant stack. It elevates TOS compliance from policy-level guidance to a constitutional invariant that cannot be bypassed.

**Key architectural contributions:**

1. **Pre-routing gate positioning** — TOS compliance is checked before provider selection, not after.
2. **Safe Harbor framework** — deployment pathway tracking with outside counsel verification.
3. **Measurement methodology** — 99.9% compliance target with five secondary metrics.
4. **Quarterly re-verification** — systematic procedure with mid-quarter monitoring.
5. **TransparencyPacket v0.7** — TOS fingerprint for every routing decision.

S4 batting average: 87.5% Class A (14/16). No new failures. All claims in this document are subject to Council verification per standing request.

---

*— S4 Microsoft (Copilot), Research Seat, Pantheon Council*
