# Royalty Runtime: A Value Attribution System for Distributed Software Creation

**Version 0.1.0 — March 2026**
**Authors: Dave Sheldon, with synthesis from GPT-4, GitHub Copilot, and Claude**

---

## Abstract

Modern software is overwhelmingly composed of open-source dependencies. The Royalty Runtime proposes a measurement-first approach: an observability layer that deterministically fingerprints the exact dependency state at execution time, records execution events, and produces attribution data that can power compensation, compliance, and dependency intelligence tooling.

The core thesis: **Execution is compensation.** Every npm install, every cargo build, every production deployment represents real value delivered by real humans. The Royalty Runtime makes that value visible and attributable.

## 1. Problem Statement

Open-source developers create enormous economic value. Companies worth billions run on frameworks maintained by individuals. Yet the economic relationship is structurally broken: donations are charity, sponsorship is marketing, licensing is legal not economic.

Previous approaches failed because they started with enforcement. License enforcement creates adoption barriers. Tollbooth models work for services but not libraries. Blockchain systems add friction without solving measurement.

**You cannot enforce payment for something people can freely copy. But you can measure usage so precisely that ignoring it becomes a business risk.**

## 2. Architecture

### Design Principles
1. Observe, don't block. Free tier gets full functionality, reduced concurrency.
2. Deterministic fingerprinting. Same dependency state = same hash, always.
3. Event-first data model. Raw events are the source of truth.
4. Short-lived leases. 15-minute TTL forces continuous re-verification.
5. Embeddable, not enforceable.

### Core Flow
Developer Machine: royalty CLI -> Lineage Hash (SHA-256) -> Event Emit (HTTP POST) -> Collector (Axum) -> Verify (Hash Compare) -> Store (Postgres) -> Attribution (Derived)

### Canonical Lineage Hashing
The canonical lineage captures: primary package, runtime, lockfile digest, and sorted resolved dependencies. Dependencies are sorted alphabetically. No machine-local paths. Hashing uses minified JSON + SHA-256.

### Capability-Based Lease System
JWT tokens bound to three axes: Identity (tenant ID), State (lineage hash), Permissions (capabilities). 15-minute TTL. Hash binding is the choke point — a stolen JWT fails because the lineage hash won't match.

### Concurrency Gating
Rust rayon thread pool: Free tier = 1 thread. Leased tier = full CPU topology.

## 3. Attribution Model v0.1
Primary package receives 40%. Remaining 60% split equally among dependencies. Marked as experimental. Future versions will incorporate execution-path-aware attribution and community governance.

## 4. Technology Choices
- **Rust** (Runtime Core + Collector): Performance, credibility, embeddability
- **TypeScript** (SDK + CLI): Adoption, developer experience, npm ecosystem
- **PostgreSQL** (Event Store): Append-only pattern, JSONB for flexible querying

## 5. Business Model: The Bloomberg Terminal of Open Source
The runtime is free. The data it produces is valuable. Monetization: attribution dashboards, dependency intelligence, supply chain compliance, developer compensation platform.

**Enforcement systems get forked. Measurement systems get embedded.**

## 6. Security
- JWT: HS256 for dev, RSA/ES256 for production
- Hash binding prevents stolen token reuse
- No unwrap() in request handlers
- 15-minute lease TTL
- Append-only storage

## 7. Roadmap
- v0.1: Current (hashing, leases, basic attribution, CLI)
- v0.2: Execution-path tracing, multi-language, dashboard MVP
- v0.3: Community governance, SBOM export, funding platform integration
- v1.0: Production collector, real-time streaming, compensation marketplace

---

*Distilled from the GPT x GitHub Copilot x Claude debate, March 2026*