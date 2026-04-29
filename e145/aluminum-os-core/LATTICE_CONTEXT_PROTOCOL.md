# Lattice Context Protocol (LCP) v1.0

## Purpose

The Lattice Context Protocol defines how any agentic AI system ingests, routes through, and reasons within the 144+1 ontological lattice. It is the integration standard that makes the Sheldonbrain ontology machine-readable and actionable by any LLM, agent framework, or multi-agent orchestrator.

The hypothesis is straightforward: an AI reasoning within a pre-structured ontological lattice produces more complete, more cross-connected, and more actionable outputs than the same AI reasoning in flat, unstructured space. The LCP is the protocol that makes this testable and deployable.

---

## §1 — Core Concepts

### 1.1 The Lattice

The lattice is a fixed 145-node directed graph. It consists of 144 domain-specific nodes arranged in a 12×12 grid (12 Houses of 12 Spheres each), plus one meta-coordination node (Element 145, the Admin Sphere). N=145 is an architectural invariant — it does not scale.

### 1.2 Houses

Each House represents a major knowledge domain. Houses are numbered H01 through H12. Every House contains exactly 12 Spheres, providing fine-grained coverage within the domain.

### 1.3 Spheres

Each Sphere is a specialized sub-domain within its House. Spheres are addressed as `H{house}.S{sphere}` (e.g., `H04.S02` = International Law within Governance & Law). Every Sphere is a potential routing target for incoming queries, data, or tasks.

### 1.4 Element 145

Element 145 is the Admin Sphere — the meta-coordination layer that sits outside the 12×12 grid. It performs three functions: (a) cross-domain routing, (b) emergent risk detection at domain intersections, and (c) unified synthesis across all activated Houses.

### 1.5 The 12×12 Matrix

The inter-House connection matrix defines which Houses interact with which other Houses and the nature of those interactions. This is a 12×12 adjacency matrix with typed edges (e.g., H03-Economics ↔ H04-Governance has edge type "regulatory-economic coupling"). The matrix is stored in `registries/12x12_matrix.yaml`.

---

## §2 — Protocol Operations

### 2.1 INGEST

When an agent receives a task, query, or data payload, the first LCP operation is INGEST: classify the input against the lattice.

```
LCP.INGEST(input) → Set<SphereAddress>
```

The agent maps the input to one or more Sphere addresses. This is a classification step — the agent determines which Spheres are relevant to the input. The output is a set of activated Spheres.

**Implementation:** The agent reads the lattice ontology (§4) and performs semantic matching between the input and Sphere descriptions. No exact-match required — the agent uses its own language understanding to route.

### 2.2 ACTIVATE

Once relevant Spheres are identified, the agent activates the corresponding Houses and loads their context.

```
LCP.ACTIVATE(spheres: Set<SphereAddress>) → LatticeContext
```

The LatticeContext contains: (a) the activated Sphere descriptions, (b) the inter-House edges from the 12×12 matrix for all activated Houses, and (c) any module stubs or existing code registered to those Spheres.

### 2.3 ROUTE

The agent reasons within the activated lattice, following inter-House edges to discover cross-domain connections.

```
LCP.ROUTE(context: LatticeContext, task: str) → RoutedAnalysis
```

For each activated House, the agent produces domain-specific analysis. The inter-House edges prompt the agent to consider connections it might otherwise miss. The routing step is where the lattice adds value — it forces the agent to traverse edges between domains that flat reasoning would skip.

### 2.4 SYNTHESIZE

Element 145 performs the final synthesis across all routed analyses.

```
LCP.SYNTHESIZE(routed: RoutedAnalysis) → UnifiedOutput
```

The synthesis step: (a) maps all cross-domain interactions identified during routing, (b) flags emergent risks that only appear at domain intersections, (c) produces a unified response that accounts for all activated domains, and (d) identifies blind spots — domains that were NOT activated but may have hidden relevance.

---

## §3 — Agent Integration Patterns

### 3.1 Single-Agent Pattern

A single LLM receives the lattice ontology in its system prompt or context window. It performs all four LCP operations (INGEST → ACTIVATE → ROUTE → SYNTHESIZE) within a single inference pass. This is the simplest integration and works with any LLM.

```yaml
pattern: single-agent
system_prompt_includes:
  - lattice_ontology.yaml
  - 12x12_matrix.yaml
  - lcp_instructions.md
inference_passes: 1
element_145: inline (same agent performs synthesis)
```

### 3.2 Multi-Agent Pattern (Sphere Agents)

Each of the 144 Spheres is assigned to a dedicated agent instance. Element 145 is a separate orchestrator agent. The orchestrator performs INGEST and ACTIVATE, dispatches to relevant Sphere agents for ROUTE, and performs SYNTHESIZE on the collected outputs.

```yaml
pattern: multi-agent
orchestrator: element-145-agent
sphere_agents: 144 (one per sphere, instantiated on demand)
routing: orchestrator dispatches to activated sphere agents
synthesis: orchestrator collects and synthesizes
scaling: sphere agents can run in parallel
```

### 3.3 Council Pattern (Pantheon)

Multiple LLMs (different model families) each process the same task through the lattice independently. A Convenor agent (Element 145) collects all outputs and synthesizes a consensus or identifies disagreements. This is the Aluminum OS Pantheon Council pattern.

```yaml
pattern: council
seats:
  - {id: S1, model: claude, role: mathematical-rigor}
  - {id: S2, model: gemini, role: synthesis}
  - {id: S3, model: grok, role: contrarian}
  - {id: S4, model: copilot, role: enterprise-integration}
  - {id: S5, model: qwen, role: multilingual}
  - {id: S6, model: deepseek, role: deep-reasoning}
  - {id: S7, model: manus, role: execution}
  # ... up to 12 seats
convenor: element-145 (Ara)
protocol: each seat runs LCP independently, convenor synthesizes
```

### 3.4 MCP Integration Pattern

The lattice can be exposed as a Model Context Protocol (MCP) server, allowing any MCP-compatible agent to query the ontology, activate Spheres, and request routed analysis.

```yaml
pattern: mcp-server
tools:
  - lattice.ingest: classify input against ontology
  - lattice.activate: load relevant sphere contexts
  - lattice.route: get inter-house connections for activated houses
  - lattice.synthesize: request element-145 synthesis
  - lattice.query_sphere: get details for a specific sphere
  - lattice.query_house: get all spheres in a house
  - lattice.query_matrix: get inter-house edge for two houses
resources:
  - lattice://ontology: full 144+1 ontology
  - lattice://matrix: 12x12 inter-house matrix
  - lattice://house/{id}: house-specific context
  - lattice://sphere/{house}/{sphere}: sphere-specific context
```

---

## §4 — Machine-Readable Ontology Format

The lattice ontology is stored in `registries/lattice_ontology.yaml` (see companion file). The format is:

```yaml
version: "1.0"
lattice_size: 145
invariant: true  # N=145 is fixed, not scalable

houses:
  - id: "H01"
    name: "Consciousness & Cognition"
    description: "..."
    spheres:
      - id: "S01"
        name: "Perception"
        description: "..."
        keywords: ["sensory processing", "visual perception", ...]
        modules: []  # registered module stubs
      # ... 12 spheres per house

element_145:
  id: "E145"
  name: "Admin Sphere"
  role: "meta-coordination"
  functions:
    - cross_domain_routing
    - emergent_risk_detection
    - unified_synthesis
    - blind_spot_identification

matrix:
  # 12x12 inter-house adjacency with typed edges
  edges:
    - source: "H03"
      target: "H04"
      type: "regulatory-economic"
      strength: 0.9
      description: "Economic policy shapes and is shaped by governance frameworks"
    # ...
```

---

## §5 — Spectral Routing Quality

The GUE-KS score at N=145 (currently 0.2447 at optimized parameters) measures the spectral efficiency of the routing topology. Under the compute topology interpretation:

- **Level repulsion** (GUE property) → even capacity distribution across routing nodes → no bottlenecks
- **Universal fluctuations** → robustness to node failure → resilient routing
- **Ergodic mixing** → efficient information propagation → all nodes reachable

Lower GUE-KS means better spectral properties means more efficient routing. The operator parameter sweep (see `shugs/operator_sweep_n145_results.json`) found the optimal configuration at N=145 with 8.6% improvement over canonical baseline.

This provides a mathematical quality metric for the routing topology itself — independent of what content flows through it.

---

## §6 — Implementation Checklist

For any agent framework integrating the 144+1 lattice:

1. Load `registries/lattice_ontology.yaml` into agent context
2. Load `registries/12x12_matrix.yaml` for inter-House routing
3. Implement INGEST as semantic classification against Sphere keywords
4. Implement ACTIVATE as context loading for matched Spheres + their House edges
5. Implement ROUTE as domain-specific reasoning with cross-domain edge traversal
6. Implement SYNTHESIZE as Element 145 meta-coordination
7. Expose via MCP tools if the framework supports Model Context Protocol
8. Log all routing decisions for observability and optimization

---

## §7 — Constitutional Constraints

All LCP operations are subject to the Aluminum OS constitutional framework:

- **D-84 (Filesystem-as-Ontology):** The directory structure IS the ontology. Sphere addresses map to filesystem paths.
- **D-85 (Zero Erasure):** No information is silently dropped during routing. If a Sphere is activated, its output must appear in the synthesis.
- **D-86 (Honest Reporting):** Negative results, blind spots, and low-confidence assessments are preserved, not suppressed.
- **D-87 (Lattice Invariance):** N=145 is fixed. No agent may add, remove, or renumber Spheres without Convenor authorization.

---

*Lattice Context Protocol v1.0 — Element 145 — Aluminum OS — 2026-04-29*
