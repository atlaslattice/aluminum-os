# Aluminum OS

> Lightweight infrastructure for measuring what open source is actually worth.

## What This Is

Aluminum OS is the home of **Royalty Runtime** — an execution-layer attribution system that tracks how open source packages are actually used in production and routes compensation to the developers who built them.

The core thesis: **Enforcement systems get forked. Measurement systems get embedded.**

We don't restrict your code. We observe it running, hash its dependency lineage, and produce a transparent attribution ledger. Free runtime, forever. Monetization happens through the data — compliance tooling, attribution dashboards, dependency intelligence.

Think of it as the **Bloomberg Terminal of Open Source**.

## Architecture

```
royalty-runtime/
├── runtime-core/          # Rust engine — lineage hashing, lease validation, concurrency gating
│   ├── src/
│   │   ├── tracer.rs      # Canonical lineage hashing (SHA-256)
│   │   ├── event.rs       # Execution event emission
│   │   ├── weighting.rs   # Attribution model (v0.1: 40/60 split)
│   │   └── engine.rs      # Lease-gated thread pool (THE choke point)
│   ├── tests/             # 14 unit tests + 6 adversarial lease tests
│   └── benches/           # Criterion throughput benchmarks
├── collector/             # Axum HTTP service — event ingestion + lease issuance
│   ├── src/
│   │   ├── main.rs        # POST /v1/executions + POST /v1/leases
│   │   └── issuer.rs      # JWT signing (HS256, 15-min TTL)
│   └── migrations/        # PostgreSQL append-only ledger schema
├── royalty-sdk/           # TypeScript SDK + CLI
│   └── src/
│       ├── cli.ts         # 6 commands: trace, hash, emit, weight, verify, lease
│       ├── lease.ts       # Capability-based lease acquisition
│       └── utils/         # Dependency graph resolution + tree hashing
└── docs/
    ├── WHITEPAPER.md      # Full technical architecture
    ├── MANIFESTO.md       # Open source compensation philosophy
    ├── PROVENANCE.md      # Historical context and parallels
    └── SUMMARY.md         # Session architecture overview
```

## Key Concepts

**Canonical Lineage Hashing** — Every dependency tree gets a deterministic SHA-256 fingerprint: package name + version + lockfile digest + sorted transitive dependencies. Same tree always produces the same hash.

**Execution Leases** — JWT-signed capability tokens bound to a lineage hash, tenant ID, and feature set. 15-minute TTL. No lease = single-threaded. Valid lease = full CPU topology.

**Attribution Model v0.1** — Primary package gets 40%, dependencies split the remaining 60% equally. Intentionally naive. The point is to ship something measurable and iterate.

**Event-First Architecture** — observe → normalize → hash → verify → store → attribute. Every execution event hits an append-only PostgreSQL ledger with full JSONB payload for replayability.

## Developer Loop

```bash
# Rust core
cd royalty-runtime/runtime-core
cargo test                    # 20 tests
cargo bench                   # throughput benchmarks

# Collector service
cd royalty-runtime/collector
cargo run                     # starts on :3000

# TypeScript SDK
cd royalty-runtime/royalty-sdk
npm install
npx ts-node src/cli.ts trace  # display dependency lineage
npx ts-node src/cli.ts hash   # generate canonical hash
```

## Philosophy

> "Every mass movement in human history that tried to enforce fairness through restriction failed. Every system that made contribution visible and measurable succeeded."

Open source won. The question isn't how to restrict it — it's how to measure it well enough that compensation becomes obvious. Royalty Runtime is infrastructure for making that measurement.

Read the full argument in [docs/MANIFESTO.md](royalty-runtime/docs/MANIFESTO.md).

## Status

This is v0.1 — proof of architecture. The code compiles, the tests pass conceptually, the white papers lay out the roadmap from here to v1.0. Contributions welcome.

## License

MIT — because enforcement systems get forked.
