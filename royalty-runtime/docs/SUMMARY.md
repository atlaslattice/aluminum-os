# Royalty Runtime — Session Architecture Summary

**March 23, 2026**

## Origin

The Royalty Runtime emerged from a multi-hour, multi-AI debate between Dave Sheldon, GPT-4, GitHub Copilot, and Claude. Started with theological analysis, evolved through open source economics, and crystallized into a concrete architecture for measuring and attributing value in the software dependency ecosystem.

Critical pivot: enforcement model -> measurement model. This happened after Copilot's computer died mid-session and GPT-4 carried the architectural thread alone.

## The Stack

- **royalty CLI (TypeScript)**: trace, hash, emit, weight, verify, lease
- **@royalty/sdk (TypeScript)**: buildLineagePayload, acquireExecutionLease
- **runtime-core (Rust)**: tracer, event, weighting, engine
- **royalty-collector (Rust/Axum)**: POST /v1/executions, POST /v1/leases
- **PostgreSQL**: execution_events (append-only ledger)

## File Manifest — 25 Files

### Runtime Core (9 files)
Cargo.toml, lib.rs, tracer.rs (SHA-256 hashing), event.rs (execution events), weighting.rs (40/60 attribution), engine.rs (JWT lease verification + rayon concurrency), hash_stability.rs (8 tests), adversarial_lease.rs (6 tests), throughput_bench.rs

### Collector (4 files)
Cargo.toml, main.rs (Axum server), issuer.rs (JWT lease issuance), init_executions.sql (Postgres schema, 15 columns, 7 indexes)

### TypeScript SDK (6 files)
package.json, tsconfig.json, index.ts, cli.ts (6 commands), lease.ts (capability-based leases), dependency-graph.ts + test (6 tests)

### Documentation (5 files)
README.md, WHITEPAPER.md, MANIFESTO.md, PROVENANCE.md, SUMMARY.md

## Test Coverage: 20 tests total
- 8 Rust hash stability tests
- 6 Rust adversarial lease security tests
- 6 TypeScript hash determinism tests

## Key Design Decisions
1. Measurement over enforcement
2. Deterministic cross-language hashing (Rust + TypeScript)
3. Append-only events with full payload for replayability
4. 15-minute lease TTL
5. Simple attribution first (40/60 split)
6. Rust for core, TypeScript for adoption

## Integration Map
- Aluminum OS: Native subsystem
- UWS CLI: Developer-facing commands
- CI/CD: GitHub Actions step
- Package managers: Future npm/cargo plugins

---

*Built in a single session. Debated across four AI models. Documented for the humans who will carry it forward.*