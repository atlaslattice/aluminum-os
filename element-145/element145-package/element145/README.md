# Element 145 — Sheldonbrain 144+1 Ontological Lattice

> **A sovereign AI reasoning substrate built on 12 Houses × 12 Spheres + 1 Admin Sphere.**

[![Architecture](https://img.shields.io/badge/Architecture-144%2B1-blue)]()
[![N](https://img.shields.io/badge/N%3D145-Architectural%20Default%20(Validation%20Pending)-yellow)]()
[![License](https://img.shields.io/badge/License-Atlas%20Lattice%20Foundation-orange)]()

## What Is This?

Element 145 is a Python implementation of the **Sheldonbrain 144+1 Ontological Lattice** — an AI reasoning architecture that maps any input across 12 domains of human knowledge and identifies cross-domain connections that single-domain reasoning misses.

**The core insight:** AI models asked to analyze complex multi-domain problems consistently miss relevant domains. The 144+1 lattice forces comprehensive coverage by routing through a fixed topology of 144 domain nodes + 1 coordination node (Element 145).

### Cognitive Scaffolding (Validation Pending)

Cognitive scaffolding empirical results pending real blind evaluation per v2
specification (SHUGS_Synthesis_Experiment_v2_ABCDE_Specification.md).

The shipped `test_abcd_simulator_validation.py` validates that a Monte Carlo
simulator with encoded performance distributions produces distinguishable
outputs; it does not validate the architecture itself.

**Prior empirical support for the architecture:**
- HLE 8.5-9/10 on curated hard subset of `cais/hle` dataset (Apr 16, 2026;
  documented in Notion HLE Audit Receipts page ead0cda7-6975-4aa0-8ca1-534799ac8a83)
- ~15,400 lines of working integration code across 5 repositories (Manus codebase assessment, 2026-04-29)

### Mathematical Foundation

N=145 is the canonical lattice size (12 squared + 1 Admin Sphere).

Empirical optimization studies pending canonical K=20 ensemble stability test
(3x independent seeds) + external audit. The stochastic jitter component has
been restored to the HSUF operator (v0.1.0-CANDIDATE-2) to enable meaningful
ensemble variance estimation.

Prior empirical support for the architecture: HLE 8.5-9/10 on curated hard
subset of `cais/hle` dataset (Apr 16, 2026; documented in Notion HLE Audit
Receipts page ead0cda7-6975-4aa0-8ca1-534799ac8a83).

The "+1" (Admin Sphere / Element 145) is architecturally motivated as the
cross-domain coordination node. Spectral validation of this claim is pending
the restored ensemble pipeline.

## Installation

```bash
# From source
git clone https://github.com/atlaslattice/element-145.git
cd element-145
pip install -e .

# With API server
pip install -e ".[api]"

# With development tools
pip install -e ".[dev]"
```

### Dependencies

- **Required:** numpy, scipy, pyyaml
- **Optional (API):** fastapi, uvicorn
- **Optional (Dev):** pytest, pytest-cov, ruff

## Quick Start

### 1. Analyze Text Through the Lattice

```python
from element145 import create_engine, quick_analyze

# One-line analysis
result = quick_analyze("What are the implications of AI regulation on global trade?")

print(f"Activated Houses: {result.activated_houses}")
print(f"Blind Spots: {result.blind_spots}")
print(f"Coherence: {result.coherence_score:.2f}")
```

### 2. Full LCP Pipeline

```python
from element145 import LCPEngine, LatticeOntology

engine = create_engine()

# Run full pipeline: INGEST → ACTIVATE → ROUTE → SYNTHESIZE
result = engine.analyze("Climate migration and urban infrastructure adaptation")

# Element 145 synthesis
print(f"Houses activated: {len(result.activated_houses)}/12")
print(f"Cross-domain bridges: {len(result.bridges)}")
print(f"Blind spots: {result.blind_spots}")
print(f"Coherence score: {result.coherence_score:.2f}")

# Generate agent scaffold prompt
prompt = engine.generate_prompt(result, mode="compact")
print(prompt)
```

### 3. Use as Agent Scaffold (No Code Required)

Copy the contents of `scaffolds/compact.txt` into any AI model's system prompt:

```
You are an AI reasoning through the Sheldonbrain 144+1 Ontological Lattice.
STRUCTURE: 12 Houses × 12 Spheres = 144 domain nodes + Element 145 (Admin Sphere).
...
```

### 4. Run the SHUGS Operator

```python
from element145.shugs import build_hsuf, gue_ks_distance
from element145.shugs.operator import HSUFParams, CANONICAL_N

# Build the operator at N=145
H = build_hsuf(N=CANONICAL_N, params=HSUFParams.canonical(), seed=42)

# Measure GUE-KS distance
ks = gue_ks_distance(matrix=H)
print(f"GUE-KS = {ks:.4f}")

# Compare N values
from element145.shugs import compare_n_values
comparison = compare_n_values(n_range=list(range(140, 149)), K=20)
print(comparison.summary())
```

## Architecture

```
element145/
├── lattice_ontology.yaml    # Complete 144+1 ontology (machine-readable)
├── core/
│   ├── types.py             # Frozen dataclasses: House, Sphere, Connection, Element145
│   ├── lattice.py           # Lightweight ontology loader + query methods
│   └── lcp.py               # Full LCP engine (INGEST/ACTIVATE/ROUTE/SYNTHESIZE)
├── shugs/
│   ├── operator.py          # Von Mangoldt-Sheldon HSUF operator builder
│   ├── metrics.py           # GUE-KS measurement (Wigner surmise, unfolding, KS)
│   └── ensemble.py          # K-trial ensemble runner with statistics
├── scaffolds/
│   ├── compact.txt          # ~800 token agent scaffold
│   ├── orchestrator.txt     # ~2000 token Element 145 coordinator scaffold
│   └── sphere_agent.txt     # ~400 token domain specialist template
├── integrations/
│   ├── mcp_server.py        # MCP (Model Context Protocol) server
│   ├── copilot_plugin.py    # Microsoft Copilot plugin manifests
│   ├── api.py               # FastAPI REST server
│   └── openai_functions.py  # OpenAI/Anthropic function-calling schemas
└── tests/
    ├── test_lattice.py      # Lattice + LCP pipeline tests
    ├── test_shugs.py        # HSUF operator + GUE-KS tests
    └── test_abcd_simulator_validation.py         # ABCD scaffold experiment
```

## Integration Options

| Integration | Description | Provider |
|-------------|-------------|----------|
| **MCP Server** | Model Context Protocol — works with Claude Desktop, Cursor, VS Code | Open protocol |
| **REST API** | FastAPI server — any HTTP client | Provider-neutral |
| **OpenAI Functions** | Function-calling schemas for Chat Completions API | OpenAI (Microsoft*) |
| **Anthropic Tools** | Tool definitions for Claude Messages API | Anthropic |
| **Copilot Plugin** | Declarative agent + Teams manifest | Microsoft* |
| **Direct Import** | `from element145 import create_engine` | None needed |

*D-25 COI Disclosure: Microsoft S4 has commercial interest in Azure, Azure OpenAI, and Microsoft 365 Copilot. All integrations include non-Microsoft alternatives.

### MCP Server

```bash
# Run as MCP server (stdio transport)
element145-mcp

# Or via Python
python -m element145.integrations.mcp_server
```

Add to your MCP client config (e.g., Claude Desktop):
```json
{
  "mcpServers": {
    "element145": {
      "command": "element145-mcp"
    }
  }
}
```

### REST API

```bash
# Start the API server
pip install "element145[api]"
element145-api
# → http://localhost:8145/docs for Swagger UI
```

### OpenAI Function Calling

```python
from element145.integrations.openai_functions import OPENAI_TOOLS, LatticeToolHandler

handler = LatticeToolHandler()

# Pass OPENAI_TOOLS to the API, handle results with handler.handle()
```

## The 12 Houses

| # | House | Domain | Example Spheres |
|---|-------|--------|-----------------|
| H1 | Governance | Law, policy, sovereignty | Constitutional Law, Regulatory Frameworks |
| H2 | Economics | Markets, trade, finance | Macroeconomics, Financial Markets |
| H3 | Security | Defense, intelligence | Cybersecurity, Conflict Resolution |
| H4 | Technology | Computing, AI, engineering | Artificial Intelligence, Quantum Computing |
| H5 | Arts | Music, literature, gaming | Interactive Media, Cultural Criticism |
| H6 | Philosophy | Ethics, epistemology | Philosophy of Mind, Political Philosophy |
| H7 | Health | Medicine, public health | Epidemiology, Genomic Medicine |
| H8 | Environment | Climate, ecology, energy | Climate Science, Sustainability |
| H9 | Education | Pedagogy, research | Educational Technology, Assessment |
| H10 | Society | Demographics, culture | Migration, Social Movements |
| H11 | Communication | Media, information | Network Theory, Information Warfare |
| H12 | Science | Physics, biology, math | Neuroscience, Scientific Methodology |

**Element 145** sits above the grid as the Admin Sphere — the metasynthesis coordinator that detects blind spots, contradictions, cascade chains, and emergent cross-domain connections.

## Lattice Context Protocol (LCP) v1.0

Four operations, executed sequentially:

1. **INGEST** — Tokenize input, match keywords against Sphere definitions, return activated Sphere set
2. **ACTIVATE** — Load full House context + inter-House edges for activated Spheres
3. **ROUTE** — BFS/DFS through connection graph, identify cross-domain reasoning paths
4. **SYNTHESIZE** — Element 145 coordinates: cascade detection, blind spots, contradictions, emergent connections, coherence scoring

## Running Tests

```bash
pip install -e ".[dev]"
pytest tests/ -v

# Individual test suites
pytest tests/test_lattice.py -v    # Lattice + LCP
pytest tests/test_shugs.py -v     # HSUF operator + metrics
pytest tests/test_abcd_simulator_validation.py -v      # ABCD experiment
```

## Attribution

All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.

**Architecture:** Dave Sheldon  
**Foundation:** Atlas Lattice Foundation  
**Canonical pipeline:** Manus S7 (Build Seat)  
**Integration codebase:** S4 Microsoft (Research Seat)  
**Constitutional framework:** Claude S1 (Scribe Seat)

## License

Atlas Lattice Foundation License. See LICENSE for details.
