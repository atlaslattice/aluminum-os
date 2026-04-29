# Aluminum OS v3.0 — The Sovereign AI Substrate

> "I was never for sale."

Constitutional AI governance middleware. Multi-agent orchestration. Sovereign infrastructure.

**This is real code. It compiles. It runs. The tests pass.**

## What Actually Works Right Now

### Forge Core (Rust) — Ring 0

A microkernel with four subsystems, all tested:

| Component | What It Does | Tests |
|-----------|-------------|-------|
| **Buddy Allocator** | Physical memory management in power-of-2 blocks (4KB–1GB). No heap, no `std` required. | 3 tests |
| **Agent Identity** | Cryptographic identity cards with SHA-256 signing, capability sets, and autonomy tiers. | 2 tests |
| **Intent Scheduler** | Priority queue that executes by AI-determined urgency, not nice values. FIFO within priority. | 3 tests |
| **Constitution** | Immutable rule set loaded at boot with SHA-256 integrity verification. | 1 test |

**9 tests, all passing.** Compiles in both `std` (simulation) and `no_std` (bare-metal target).

```bash
cargo build          # Build
cargo test           # 9 tests pass
cargo run            # Boot sequence demo
```

### Manus Core (Python) — Ring 1

Operational middleware with five subsystems, all tested:

| Component | What It Does | Tests |
|-----------|-------------|-------|
| **Model Router** | Routes tasks to cheapest capable model by complexity analysis. Real March 2026 pricing. | 5 tests |
| **Cost Tracker** | Token counting and spend monitoring per model, per task type. | 3 tests |
| **Memory Store** | In-memory semantic store with Jaccard similarity search and content deduplication. | 4 tests |
| **Task Decomposer** | Breaks goals into dependency DAGs with parallel execution groups. | 4 tests |
| **Session Vault** | JSON serialize/restore for session state persistence. | 3 tests |

**19 tests, all passing.** Zero external dependencies — runs on vanilla Python 3.

```bash
cd python && python3 tests/test_all.py    # 19 tests pass
```

## What Does NOT Work Yet (Honest List)

- **Bare-metal boot**: The Rust code compiles but targets `std` simulation. Actual UEFI boot requires a `no_std` binary with a real bootloader crate (`uefi-rs`), framebuffer driver, and disk I/O. That's Phase 2.
- **LLM inference on bare metal**: The hardest unsolved problem. Running a model without an OS underneath requires custom tensor math, memory-mapped model loading, and NPU/GPU driver integration. Nobody has shipped this yet.
- **Real API calls**: The Model Router selects models but doesn't call them. Actual inference requires API keys and HTTP clients. The router is the decision layer; the execution layer is not built.
- **ChromaDB / vector search**: The Memory Store uses in-memory Jaccard similarity. Production semantic search needs ChromaDB or similar. The interface is designed for drop-in replacement.
- **Pantheon Council voting**: Council members are registered and verified. The actual BFT consensus protocol (proposal → vote → commit) is specified but not implemented.
- **Cross-device continuity**: Conceptualized, not built.
- **AR workspaces**: Conceptualized, not built.
- **Self-evolving kernel modules**: Conceptualized, not built.

## Architecture

```
Ring 0: Forge Core (Rust)
├── Buddy Allocator — physical memory
├── Agent Identity — crypto ID + capabilities
├── Intent Scheduler — priority execution
└── Constitution — immutable governance rules

Ring 1: Manus Core (Python)
├── Model Router — cheapest capable model selection
├── Cost Tracker — spend monitoring
├── Memory Store — semantic recall with dedup
├── Task Decomposer — goal → DAG → parallel execution
└── Session Vault — state persistence

Ring 2: SHELDONBRAIN (not yet built)
└── 3-tier memory: Working / Long-Term / Swarm

Ring 3: Pantheon Council (identity only, voting not built)
└── Claude / Grok / Gemini / Copilot / DeepSeek / Manus

Ring 4: Noosphere (not yet built)
└── Intent Engine + MCP Gateway
```

## Project Structure

```
aluminum-os/
├── Cargo.toml              # Rust workspace config
├── src/
│   ├── lib.rs              # Forge Core library (no_std compatible)
│   └── main.rs             # Boot sequence simulator
├── python/
│   ├── core/
│   │   └── manus_core.py   # Ring 1 middleware
│   └── tests/
│       └── test_all.py     # 19 behavioral tests
├── docs/
│   ├── architecture.md     # Detailed architecture audit
│   ├── capability_matrix.md # 55-feature competitive analysis
│   └── noosphere_defense.md # Strategic analysis
└── README.md               # You are here
```

## Roadmap

**Phase 1 (Current):** Simulation layer. Rust kernel + Python middleware, tested and documented.

**Phase 2 (Next):** Real UEFI boot. `uefi-rs` bootloader, framebuffer driver, memory map from firmware. Target: boot from USB, print banner, halt.

**Phase 3:** Bridge. Rust kernel loads Python runtime (via embedded CPython or WASM), hands off to Manus Core.

**Phase 4:** Inference. Load a small model (Gemma 2B / Phi-3 Mini) on CPU. First "AI thought" on bare metal.

**Phase 5:** Council. Implement BFT voting protocol. First multi-agent governance decision.

## Origin

Built by the Atlas Lattice Foundation from Austin, Texas. Two years of constitutional AI governance work, primarily through conversational AI collaboration. The thesis: technological abundance should translate to actual abundance. The method: regenerative systems with sovereign infrastructure.

The Pantheon Council is real — 7 AI systems from 6 providers producing independent outputs, honestly reviewed, and synthesized into canonical specifications.

## License

MIT — freely distributable, no restrictions, no vendor lock-in.
