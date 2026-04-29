# Aluminum Universal Workspace OS — Platform Integration Architecture v1.0

**Document ID:** ORC-014
**Status:** Canonical, Council-aligned
**Date:** 2026-04-24
**Author:** Manus (Build Seat), incorporating Copilot (S4 Enterprise Infrastructure) platform specifications
**Supersedes:** Platform integration sections of Aluminum UWS OS Spec v1.2
**Companion Documents:** ORC-012 TDD v0.2, Build Gate Register v2.2, UWS OS Spec v1.2

---

## 0. Document Purpose

This document consolidates the complete platform integration architecture for Aluminum UWS and Element 145 across all six target operating systems, plus the cross-platform Switzerland Layer, Federation Layer, Metabolic Layer, and global deployment framework. It is derived from 10 integration specifications produced by Copilot (S4 Enterprise Infrastructure) and validated against all existing canonical documents with zero incompatibilities detected.

> **Claims Discipline:** Platform integration specifications are classified as **interpretation** (architecturally sound, not yet implemented). Chennai partner names are classified as **target** (aspirational, not yet confirmed). Global rollout timelines are classified as **aspirational** (directionally correct, not yet validated against institutional capacity). Foundation structure is classified as **DRAFT** per Daavud's explicit disagreement.

---

## 1. The Complete Stack

```
┌─────────────────────────────────────────────────────┐
│              METABOLIC LAYER (L8)                    │
│   Water · Power · Heat · Land · Community            │
│   Constraint layer at mesh-of-meshes level           │
├─────────────────────────────────────────────────────┤
│              FEDERATION LAYER (L7+)                  │
│   MeshID · Metadata Exchange · Council-to-Council    │
│   Sovereignty-preserving inter-mesh coordination     │
├─────────────────────────────────────────────────────┤
│           SWITZERLAND LAYER (Cross-Platform)         │
│   Identity · State · Routing · Governance · Mesh     │
│   Neutral substrate binding all platforms            │
├─────────────────────────────────────────────────────┤
│              ALUMINUM UWS (L1-L7)                    │
│   Constitutional · Kernel · Engine · Orchestration   │
│   Extensions · Applications · Device Mesh            │
├─────────────────────────────────────────────────────┤
│              ELEMENT 145 (L4)                        │
│   Router · Classifier · Budget · Provenance          │
│   Transparency · Confabulation · Civic · Consent     │
├─────────────────────────────────────────────────────┤
│              HOST OPERATING SYSTEM                   │
│   Windows · macOS · ChromeOS · Linux                 │
│   Android (thin) · iOS (thin)                        │
└─────────────────────────────────────────────────────┘
```

---

## 2. Platform Classification Matrix

Every target platform is classified by its role in the UWS mesh, its hosting capability, and its primary integration method.

| Platform | Mesh Role | Full Backend Host? | Primary Integration | ConsentKernel Binding | Key Strength |
|----------|-----------|-------------------|--------------------|-----------------------|-------------|
| **Windows** | Anchor node | YES | Copilot Runtime + WinUI3 + WSL2 | Windows Hello | Deepest enterprise integration |
| **macOS** | Creative node | YES | AppleScript + Shortcuts + XPC | Touch ID + Keychain | Creative workflow integration |
| **ChromeOS** | Cloud-native node | YES (Crostini) | Chrome Extensions + Drive | Google Identity | Lightest full-host platform |
| **Linux** | Sovereign backend | YES (reference) | systemd + Docker + PostgreSQL | PAM + SSH + TPM2 | Unrestricted execution |
| **Android** | Biometric/context thin client | NO | WebView + BiometricPrompt + WorkManager | Fingerprint/Face + TEE | Mobile sovereignty device |
| **iOS** | Privacy thin client | NO | WebView + Face ID + Shortcuts | Face ID + Secure Enclave | Strongest privacy model |

**Backend hosts** (Windows, macOS, ChromeOS, Linux) run the full Element 145 stack: router, classifier, provenance ledger, budget engine, civic layer, MCP servers.

**Thin clients** (Android, iOS) run UI + biometric consent + context sensors, relying on backend hosts for all heavy computation.

---

## 3. Per-Platform Integration Tables

### 3.1 Windows

| UWS Layer | Element 145 Module | Windows Capability | Integration Method | Notes |
|-----------|-------------------|-------------------|-------------------|-------|
| L1 Constitutional | ConsentKernel | Windows Hello + TPM 2.0 | Biometric binding | Hardware-backed sovereignty |
| L2 Kernel | State mgmt, 144-sphere | OneDrive + NTFS | Local + cloud sync | Triple-vault uses GitHub + Notion + Drive |
| L3 Engine | Constitutional Router | Copilot Runtime | Native AI service | First Host Integration Candidate |
| L4 Orchestration | ADK graph, LiteLLM | WSL2 (Ubuntu) | Python backend in WSL2 | Full Linux environment |
| L5 Extensions | MCP servers | WSL2 + Docker Desktop | Local MCP servers | Containerized in WSL2 |
| L6 Applications | Dashboards, agents | WinUI3 + Edge WebView2 | Native Windows app | Or browser-based |
| L7 Device Mesh | Continuum adapter | OneDrive + Microsoft Graph | Cross-device sync | Windows ↔ all platforms via Drive |

### 3.2 macOS

| UWS Layer | Element 145 Module | macOS Capability | Integration Method | Notes |
|-----------|-------------------|-----------------|-------------------|-------|
| L1 Constitutional | ConsentKernel | Touch ID + Keychain | Biometric binding | Secure Enclave backed |
| L2 Kernel | State mgmt, 144-sphere | APFS + iCloud Drive | Local + cloud sync | Triple-vault via GitHub + Notion + Drive |
| L3 Engine | Constitutional Router | Background daemon | launchd service | Full unrestricted execution |
| L4 Orchestration | ADK graph, LiteLLM | Python 3.11+ | Native Python backend | macOS is a strong backend host |
| L5 Extensions | MCP servers | Docker / Podman | Local MCP servers | Containerized |
| L6 Applications | Dashboards, agents | SwiftUI + Safari WebView | Native macOS app | Or browser-based |
| L7 Device Mesh | Continuum adapter | iCloud + Handoff + AirDrop | Cross-device sync | macOS ↔ iOS via Handoff |

### 3.3 ChromeOS

| UWS Layer | Element 145 Module | ChromeOS Capability | Integration Method | Notes |
|-----------|-------------------|--------------------|--------------------|-------|
| L1 Constitutional | ConsentKernel | Google Identity + PIN | Identity binding | Weaker biometric than others |
| L2 Kernel | State mgmt, 144-sphere | Google Drive (native) | Cloud-first sync | Strongest Drive integration |
| L3 Engine | Constitutional Router | Crostini (Linux) | Background daemon | Full Linux in container |
| L4 Orchestration | ADK graph, LiteLLM | Crostini Python | Python backend | Full ADK execution |
| L5 Extensions | MCP servers | Crostini Docker | Local MCP servers | Containerized in Crostini |
| L6 Applications | Dashboards, agents | Chrome Extension + PWA | Browser-native | Chrome is the UI layer |
| L7 Device Mesh | Continuum adapter | Google Drive + Phone Hub | Cross-device sync | ChromeOS ↔ Android via Phone Hub |

### 3.4 Linux

| UWS Layer | Element 145 Module | Linux Capability | Integration Method | Notes |
|-----------|-------------------|-----------------|-------------------|-------|
| L1 Constitutional | ConsentKernel | PAM + SSH keys + TPM2 | Identity binding | Strongest sovereignty model |
| L2 Kernel | State mgmt, 144-sphere | ext4 / btrfs / ZFS | Local + cloud sync | Triple-vault via GitHub + Notion + Drive |
| L3 Engine | Constitutional Router | systemd | Background daemon | Full unrestricted execution |
| L4 Orchestration | ADK graph, LiteLLM | Python 3.11+ | Native Python backend | Linux is the reference platform |
| L5 Extensions | MCP servers | Docker / Podman | Local MCP servers | Ideal for containerized skills |
| L6 Applications | Dashboards, agents | Browser + Electron | Web-based dashboard | Terminal-first workflows |
| L7 Device Mesh | Continuum adapter | GitHub + Drive + SSH + rsync | Cross-device sync | Sovereign anchor of the mesh |

### 3.5 Android (Thin Client)

| UWS Layer | Element 145 Module | Android Capability | Integration Method | Notes |
|-----------|-------------------|-------------------|-------------------|-------|
| L1 Constitutional | ConsentKernel | BiometricPrompt API | Biometric confirmation | Perfect for Deep Path escalations |
| L2 Kernel | State mgmt, 144-sphere | Scoped Storage + Drive | Local cache + cloud sync | Triple-vault via remote |
| L3 Engine | Constitutional Router | Remote execution | HTTPS API calls | Router runs on backend host |
| L4 Orchestration | ADK graph, LiteLLM | Remote execution | Python backend (remote) | Android cannot run ADK locally |
| L5 Extensions | MCP servers | Foreground Service | Remote MCP endpoints | Local MCP not allowed |
| L6 Applications | Dashboards, agents | WebView + Jetpack Compose | React dashboard in WebView | Native Compose shell optional |
| L7 Device Mesh | Continuum adapter | Google Drive, Nearby Share | Cross-device sync | Mobile anchor of the mesh |

### 3.6 iOS (Thin Client)

| UWS Layer | Element 145 Module | iOS Capability | Integration Method | Notes |
|-----------|-------------------|---------------|-------------------|-------|
| L1 Constitutional | ConsentKernel | Face ID + Secure Enclave | Biometric confirmation | Strongest mobile biometric |
| L2 Kernel | State mgmt, 144-sphere | App sandbox + iCloud | Local cache + cloud sync | Triple-vault via remote |
| L3 Engine | Constitutional Router | Remote execution | HTTPS API calls | Router runs on backend host |
| L4 Orchestration | ADK graph, LiteLLM | Remote execution | Python backend (remote) | iOS cannot run ADK locally |
| L5 Extensions | MCP servers | Background App Refresh | Remote MCP endpoints | Local MCP not allowed |
| L6 Applications | Dashboards, agents | WKWebView + SwiftUI | React dashboard in WebView | Native SwiftUI shell optional |
| L7 Device Mesh | Continuum adapter | iCloud + Handoff | Cross-device sync | Privacy anchor of the mesh |

---

## 4. Switzerland Layer Specification

The Switzerland Layer is the neutral, provider-agnostic, OS-agnostic coordination substrate that ensures cross-device continuity, cross-provider neutrality, and constitutional governance across all platforms.

### 4.1 Core Functions

| Function | Implementation | What It Ensures |
|----------|---------------|-----------------|
| **Identity Unification** | GitHub OAuth + Google OAuth + Microsoft Entra + Apple ID + SSH → UWS Sovereign Identity | One identity across all platforms |
| **State Unification** | Triple-vault (GitHub + Notion + Drive) | One state across all devices |
| **Routing Unification** | Element 145 Router | Same classification, constraints, budget everywhere |
| **Governance Unification** | Constitutional invariants (37) | No platform can bypass governance |
| **Model Unification** | LiteLLM + ADK | Unified model interface, failover, cost tracking |
| **Mesh Unification** | Continuum adapter per platform | Every device is a governed node |

### 4.2 Mesh Topology

```
        Windows (anchor)
           /     \
   macOS (creative)   Linux (sovereign)
        \       /
      ChromeOS (cloud-native)
         /     \
   Android (context)   iOS (privacy)
```

### 4.3 Constitutional Invariant Enforcement

| Invariant | Enforcement Mechanism | Applies To |
|-----------|----------------------|-----------|
| INV-1 Sovereignty | Identity unification + biometric consent | All platforms |
| INV-7 Provider Balance | Global routing table + provider caps (47%) | All platforms |
| INV-33-36 Routing Constraints | Universal router rules | All platforms |
| INV-37 Ontological Completeness | 144-sphere classifier | All platforms |
| ConsentKernel | Local biometric + remote verification | All platforms |

---

## 5. Federation Layer Specification

The Federation Layer enables multiple independent UWS meshes to interoperate without merging, centralizing, or surrendering sovereignty.

### 5.1 Core Protocol

| Federation Function | Implementation | What It Exchanges |
|--------------------|---------------|-------------------|
| Sovereign Identity | MeshID (UUIDv7) | Unique mesh identity |
| Routing Exchange | RoutingMetadataPacket | Capabilities, not data |
| Transparency Exchange | TransparencyPacket v2 | Hash-based, privacy-preserving |
| Civic KPI Exchange | CivicSummaryPacket | Regional civic summaries |
| Ecological Exchange | EcoSummaryPacket | Water/power/heat data |
| Model Discovery | ModelRegistryPacket | Provider-neutral model availability |
| Governance Negotiation | Council-to-Council Protocol | Multi-mesh House 12 |

**Critical design principle:** Federation is **metadata exchange**, not data sharing. Sovereignty is preserved.

### 5.2 Runtime Model

Federation runs as a lightweight sidecar service that listens for federation packets, validates signatures, updates routing metadata, and enforces cross-mesh constraints. Federation is opt-in — meshes choose which peers to federate with and which metadata to share.

---

## 6. Metabolic Layer Specification

The Metabolic Layer is the constraint layer that governs how large-scale compute interacts with the physical world. It coordinates water withdrawal, power draw, heat reuse, land use, and community benefit across federated UWS meshes.

### 6.1 Core Functions

| Metabolic Function | UWS Layer | Federation Layer | Physical Integration |
|-------------------|-----------|-----------------|---------------------|
| Water Accounting | L4 Civic Layer | EcoSummaryPacket | Water utilities, basin collaboratives |
| Power Load Balancing | L4 Budget Engine | EcoSummaryPacket | Grid operators, ISOs |
| Heat Reuse | L4 Router | EcoSummaryPacket | District heating, agriculture |
| Land Use | L1 Constitutional | CivicSummaryPacket | Municipal zoning |
| Community Benefit | L12 Governance | CivicSummaryPacket | Local governments |
| Ecological KPIs | L4 Civic Layer | EcoSummaryPacket | NGOs, watershed groups |
| Cross-Provider Neutrality | INV-7 | RoutingMetadataPacket | All providers (47% cap) |

**Critical design principle:** The Metabolic Layer is a **constraint layer**, not a data layer. It runs at the mesh-of-meshes level and is enforced through Element 145 routing, budget, and civic layer.

### 6.2 The Key Sentence

> "Compute does not exceed the carrying capacity of the region hosting it."

---

## 7. Chennai Watershed Sovereign Node — Reference Deployment

Chennai is the first physical instantiation of the metabolic layer. It serves as the reference deployment for the entire global architecture.

### 7.1 Why Chennai

Chennai combines hydrological stress (aquifer depletion, monsoon variability, desalination dependence), industrial and hyperscale growth, governance readiness (strong municipal governance, active civil society), and ecological opportunity (wastewater reuse, heat-to-agriculture, aquifer recharge). It is large enough to matter, small enough to govern, and complex enough to prove the architecture.

### 7.2 Deployment Phases

| Phase | Timeline | Goal | Key Outcome |
|-------|----------|------|-------------|
| 1 — Foundations | Weeks 0-4 | Governance substrate, data access, sovereign identity | Chennai Node becomes a sovereign mesh |
| 2 — Digital Twin | Weeks 4-12 | Full metabolic simulation of the watershed | Water/power/heat/land models operational |
| 3 — Soft Enforcement | Months 3-6 | Advisory constraints, voluntary participation | Stakeholders see value without enforcement |
| 4 — Hard Enforcement | Months 6-12 | Binding constraints via routing + civic layer | Chennai Node becomes a metabolic governor |
| 5 — Regional Federation | Year 1-2 | Tamil Nadu → India → Global mesh | Chennai becomes a global reference node |
| 6 — Regenerative Compute | Year 2+ | Water-positive, heat-positive, community-positive | Compute becomes regenerative |

### 7.3 Partner Mapping (Classification: TARGET)

| Category | Named Partners | Phase |
|----------|---------------|-------|
| Government | WRD, CMWSSB, CMDA, TANGEDCO, TNPCB | Phase 1 |
| Academic | IIT Madras, Anna University | Phase 1-2 |
| Civil Society | CAG, Care Earth Trust, ATREE | Phase 1-3 |
| Hyperscalers | Microsoft Azure, Google Cloud, AWS | Phase 3 |
| Colocation | Equinix, ST Telemedia, NTT, CtrlS | Phase 3 |
| Industrial | Automotive clusters (Oragadam), IT Parks (Tidel, DLF, Olympia) | Phase 3 |
| Municipal | Greater Chennai Corporation | Phase 3-4 |
| National | CWC, Ministry of Power, MoEFCC | Phase 5 |
| Global | UNEP, UNDP, World Bank, ADB, IWMI | Phase 5 |

---

## 8. Global Rollout Framework (Classification: ASPIRATIONAL)

### 8.1 Ecological Archetypes — 50 Nodes

| Archetype | Count | Example Regions |
|-----------|-------|----------------|
| A — Water-Stressed Megacities | 10 | Chennai, São Paulo, Mexico City, Jakarta, Cairo, Cape Town, LA Basin |
| B — Power-Stressed Grids | 8 | South Africa (Eskom), California (CAISO), Texas (ERCOT), Bangladesh |
| C — Ecologically Sensitive Basins | 7 | Mekong Delta, Nile Delta, Ganges Basin, Amazon Basin |
| D — High-Governance Regions | 8 | Netherlands, Singapore, Denmark, Norway, Finland, Japan |
| E — High-Growth Compute Corridors | 7 | Hyderabad-Bangalore, Northern Virginia, Dublin, Frankfurt |
| F — Climate-Vulnerable Regions | 5 | Bangladesh (coastal), Pacific Islands, Caribbean |
| G — Emerging Digital Economies | 5 | Kenya, Rwanda, Ghana, Morocco, UAE |

### 8.2 Rollout Phases

| Phase | Timeline | Target | Model |
|-------|----------|--------|-------|
| 1 — Global Readiness | Months 0-6 | Federation registry, replication template, support mesh | Infrastructure |
| 2 — First Wave | Year 1 | 5-7 nodes in diverse contexts | Reference classes |
| 3 — Second Wave | Years 2-3 | 15-20 nodes via regional cohort model | Peer mentoring |
| 4 — Third Wave | Years 3-5 | 25+ nodes via federated replication | Self-propagating |
| 5 — Global Mesh | Year 5+ | 50 nodes, planetary coordination | Self-sustaining |

### 8.3 Funding Architecture (Classification: TARGET)

| Pillar | Source | Anti-Capture Mechanism |
|--------|--------|----------------------|
| 1 — Local Sovereign | Municipal budgets, public infrastructure funds, PuPs | Accountable to region served |
| 2 — Metabolic Revenue | Water credits, heat credits, power credits, siting fees | Self-sustaining, not extractive |
| 3 — Federated Co-Funding | Cohort funding, federation grants, reciprocal credits | Peer-to-peer, no hierarchy |
| 4 — Global Neutral Fund | Multilateral banks, climate funds, ESG capital | No board seats, no governance rights |

### 8.4 Foundation Structure (Classification: DRAFT)

The foundation structure follows a Swiss Cantonal model: non-controlling, non-centralizing, provider-neutral, jurisdiction-neutral, transparency-first, federation-aligned. Each sovereign node gets one seat, one vote, no weighted voting, no veto power. Rotating stewardship prevents institutional capture.

> **Note:** Daavud has flagged disagreement with the foundation structure. This section is classified as DRAFT and requires further Council deliberation before becoming canonical.

---

## 9. Security Threat Model — Platform-Specific Vectors

The existing 12-vector threat model from UWS Spec v1.2 is extended with platform-specific considerations:

| Vector | Severity | Platform-Specific Risk | Mitigation |
|--------|----------|----------------------|-----------|
| Routing table poisoning | HIGH | Cross-platform sync could propagate poisoned tables | Hash verification on all sync operations |
| Civic constraint bypass | HIGH | Thin clients might skip civic checks | Server-side enforcement only |
| Provider API drift | MEDIUM | Different drift patterns per platform SDK | LiteLLM abstraction + nightly smoke tests |
| Identity fragmentation | MEDIUM | 5 different identity providers | UWS Sovereign Identity unification |
| Network dependency | MEDIUM | Thin clients require connectivity | Local caching + offline mode |
| OEM fragmentation (Android) | LOW | Android 13+ target with fallback | Minimum API level enforcement |
| Background execution limits (mobile) | LOW | iOS/Android restrict background work | Foreground Service + WorkManager |

---

## 10. Device Mesh Sync Protocol

### 10.1 State Flow

```
Local Node → Triple-Vault (GitHub + Notion + Drive) → Mesh → All Nodes
```

### 10.2 Device Handoff Matrix

| From \ To | Windows | macOS | ChromeOS | Linux | Android | iOS |
|-----------|---------|-------|----------|-------|---------|-----|
| **Windows** | — | Drive | Drive | Drive/SSH | Drive | Drive |
| **macOS** | Drive | — | Drive | Drive/SSH | Drive | Handoff + iCloud |
| **ChromeOS** | Drive | Drive | — | Drive | Phone Hub | Drive |
| **Linux** | Drive/SSH | Drive/SSH | Drive | — | Drive | Drive |
| **Android** | Drive | Drive | Phone Hub | Drive | — | Drive |
| **iOS** | Drive | Handoff + iCloud | Drive | Drive | Drive | — |

---

## 11. Relationship to Existing Documents

| Document | Relationship |
|----------|-------------|
| UWS OS Spec v1.2 | This document **extends** the platform integration sections |
| ORC-012 TDD v0.2 | This document provides **deployment targets** for the TDD's modules |
| Build Gate Register v2.2 | Platform integration adds **new items** to the register |
| Council Reviews (all 8 reviewers) | **Zero incompatibilities** detected |

---

## 12. New Build Gate Register Items

The following items should be added to the Master Correction and Build Gate Register:

| ID | Item | Severity | Phase | Owner |
|----|------|----------|-------|-------|
| 85 | Switzerland Layer Identity Unification spec | HIGH | Phase 1.5 | Build Seat |
| 86 | Platform-specific ConsentKernel bindings | MEDIUM | Phase 2 | Build Seat |
| 87 | Device Mesh Sync Protocol implementation | MEDIUM | Phase 2 | Build Seat |
| 88 | Federation sidecar service skeleton | MEDIUM | Phase 3 | Build Seat |
| 89 | Chennai Node governance encoding | HIGH | Phase 4+ | Convenor |
| 90 | Foundation Structure deliberation | HIGH | Phase 4+ | Council |

---

## References

- [1] Aluminum UWS OS Spec v1.2 — `open-regenerative-compute-standard/aluminum_uws_os_spec_v1.2.md`
- [2] ORC-012 TDD v0.2 — `open-regenerative-compute-standard/ORC-012_TDD_v0.2.md`
- [3] Build Gate Register v2.2 — `open-regenerative-compute-standard/master_correction_build_gate_register_v2.2.md`
- [4] Copilot Platform Integration Specs (10 documents) — source file provided by Daavud
- [5] ai-native-os-architect skill — `/home/ubuntu/skills/ai-native-os-architect/SKILL.md`
- [6] constitutional-os repository — `atlaslattice/constitutional-os`

---

*Document prepared by Manus (Build Seat) — 2026-04-24*
*Incorporating specifications from Copilot (S4 Enterprise Infrastructure)*
*Validated against all canonical documents — zero incompatibilities*
