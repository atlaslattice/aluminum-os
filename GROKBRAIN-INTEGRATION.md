# GROKBRAIN-INTEGRATION.md

**Grok CLI as Native Substrate for Aluminum OS Memory, Provenance, and Agent Action Layer**

- **Status**: Proposal (Hyperspace Benchmark Session)
- **Date**: 2026-05-30
- **Context**: Lattice Pulse — Task 2 (Agentic + GitHub)
- **Branch**: feature/grokbrain-integration

---

## 1. Purpose

This document proposes integrating the advanced capabilities of **Grok CLI** (specifically its GrokBrain layer) as a first-class, native substrate for Aluminum OS.

It focuses on three interlocking systems:

1. **12×12 Master Index** — A multi-dimensional retrieval and epistemic index
2. **Continuous Parser v1** — High-velocity, tool-native memory consolidation
3. **Native Grok CLI Tool Calling** — Deep, low-hallucination action surface via MCP connectors (GitHub, Notion, etc.)

The goal is to strengthen Aluminum OS’s memory, provenance, and agent execution layers while remaining fully aligned with its constitutional invariants.

---

## 2. Alignment with the Aluminum OS 12×12 Lattice

Aluminum OS already possesses a canonical **12×12 Lattice** (12 Houses × 12 Spheres = 144 nodes), as documented in `SOURCE_OF_TRUTH.md`.

This is not a coincidence with GrokBrain’s proposed "12×12 Master Index."

### Proposed Mapping

| Aluminum OS Concept       | GrokBrain Counterpart                  | Relationship |
|---------------------------|----------------------------------------|--------------|
| 12 Houses × 12 Spheres    | Primary ontological axis               | Ontology     |
| 12 Knowledge Facets       | Secondary epistemic axis               | Implementation layer |
| VIP Elements (E145–E156) | High-priority cross-cutting dimensions | Routing priority |
| Sub-spheres (~1,792 target) | Granular chunking & retrieval          | Resolution   |

GrokBrain’s 12×12 Index is positioned as the **operational and epistemic retrieval engine** that runs *over* Aluminum’s ontological lattice, adding dimensions for certainty, provenance strength, contradiction risk, and temporal volatility.

---

## 3. Continuous Parser v1

**Continuous Parser v1** is the production-grade evolution of the **Consolidation Agent** described in `memory/SHELDONBRAIN_LLM-Native_Memory_Architecture_v1.0.md`.

### Key Differences from SHELDONBRAIN v1.0

- Powered by Grok CLI’s native tool-calling surface (not generic LLM tool use)
- Direct, authenticated access to GitHub, Notion, and other providers via MCP
- Built-in epistemic labeling at ingestion time
- Tight integration with Aluminum’s constitutional audit requirements

### Pipeline

```
Raw Events (GitHub events, Notion changes, conversations, tool results)
        ↓
Continuous Parser v1 (Grok CLI)
        ↓ (Structuring + Epistemic Labeling)
Tier 1: LLM-Native Working Memory (SQLite + structured facets)
        ↓ (Promotion logic)
Tier 2: Curated RAG (Pinecone) with provenance metadata
```

This realizes the hybrid architecture envisioned in SHELDONBRAIN while making the ingestion layer dramatically more reliable and auditable.

---

## 4. Epistemic Labeling Layer

Every memory fragment written through GrokBrain carries a structured `epistemic` envelope. This is not optional metadata — it is a constitutional primitive.

### Core Schema (Tailored to Aluminum Invariants)

```json
{
  "content": "...",
  "epistemic": {
    "source_type": "council_vote | tool_result | model_inference | user_statement | mcp_sync",
    "source_ref": "string (commit, issue, notion_page, session_id, etc.)",
    "certainty": 0.0,
    "certainty_rationale": "string",
    "verification_status": "unverified | self_consistent | cross_checked | user_confirmed | contradicted | deprecated",
    "lattice_coordinates": "H12-S7",           // Direct mapping to Aluminum 12x12
    "provenance_chain": ["..."],
    "constitutional_audit": ["INV-7c", "E155", "INV-17"],
    "valid_from": "ISO8601",
    "valid_until": "ISO8601 or null",
    "contradicts": [],
    "reinforced_by": []
  }
}
```

### Concrete Examples

**Example 1: Council Decision (High Provenance)**

```json
{
  "content": "DragonSeek selected as primary sovereign deployment for PRC-lineage efficiency requirements.",
  "epistemic": {
    "source_type": "council_vote",
    "source_ref": "governance/council/2026-05-01.md#S5-S7",
    "certainty": 0.93,
    "verification_status": "cross_checked",
    "lattice_coordinates": "H12-S7",
    "provenance_chain": ["S5 vote", "S3 (Grok) adversarial audit", "Convenor tie-break (INV-9)"],
    "constitutional_audit": ["INV-3", "INV-9", "DOC-100", "E155"]
  }
}
```

**Example 2: Tool Observation (GitHub MCP)**

```json
{
  "content": "New sub-sphere enumeration added to H3-S4 (Aerospace Engineering Specializations).",
  "epistemic": {
    "source_type": "mcp_sync",
    "source_ref": "github:atlaslattice/aluminum-os@commit/672f0e5d",
    "certainty": 1.0,
    "verification_status": "self_consistent",
    "lattice_coordinates": "H3-S4",
    "provenance_chain": ["GitHub MCP push", "Continuous Parser v1 ingestion"],
    "constitutional_audit": ["INV-7c"]
  }
}
```

**Example 3: Model Inference with Caution (Low Certainty)**

```json
{
  "content": "User preference: prefers DragonSeek dialect for technical depth over Global dialect.",
  "epistemic": {
    "source_type": "model_inference",
    "source_ref": "grok-session-019e7bcc-...",
    "certainty": 0.61,
    "certainty_rationale": "Inferred from 3 conversations; not yet user-confirmed or cross-checked against Notion preferences.",
    "verification_status": "unverified",
    "lattice_coordinates": "H2-S7",
    "constitutional_audit": ["INV-1"]
  }
}
```

This labeling system makes every piece of knowledge **auditable by default**, directly supporting INV-7c and E155.

---

## 5. Native Grok CLI Tool Calling as the Action Surface

The local `grok` binary the user runs on Windows (v0.2.14) currently feels primitive because it is still a thin client.

The **hyperspace backend** (this agent session) demonstrates the actual power:

- Direct GitHub API operations as the authenticated user (atlaslattice)
- Ability to create branches and push files without local git or the local CLI
- Rich MCP connectors (GitHub, Notion, Gamma)
- Plan mode, subagents, todo gates, and strict tool discipline

**Recommendation**: Treat the Grok CLI agent runtime (not the thin TUI client) as a privileged provider driver in Aluminum OS terminology.

---

## 6. Integration Architecture

```
Aluminum OS 12×12 Lattice (Ontology + Invariants)
             |
             v
GrokBrain 12×12 Master Index + Epistemic Layer
             |
             v
Continuous Parser v1 (Grok-powered)
      +------+------+
      |             |
   Tier 1       Tier 2
(Working Memory) (Curated RAG)
```

Grok CLI becomes the high-bandwidth, high-trust ingestion and action engine for the entire substrate.

---

## 7. Recommended Implementation Phases

**Phase 0 (This PR)**
- Land this document on `feature/grokbrain-integration`
- Reference it from `SOURCE_OF_TRUTH.md` and `memory/SHELDONBRAIN...md`

**Phase 1**
- Prototype Continuous Parser v1 as a dedicated Grok agent definition + skill
- Add epistemic labeling to existing SHELDONBRAIN consolidation flow

**Phase 2**
- Expose GitHub + Notion MCP as first-class Aluminum provider drivers
- Build lattice-aware memory search that respects House/Sphere coordinates

**Phase 3**
- Full Council integration: GrokBrain as an always-available S3-augmented memory participant

---

## 8. Constitutional Compliance Checklist

- [x] Strengthens INV-7c (Continuous Verifiability)
- [x] Directly supports E155 (Provenance & Identity)
- [x] Compatible with INV-17 (Zero Erasure)
- [x] Does not claim authority over canon
- [x] Positions Grok as participant/substrate, not owner
- [x] References existing ratified documents (SOURCE_OF_TRUTH, SHELDONBRAIN v1.0)

---

*Created via hyperspace GitHub MCP session as part of Grok CLI benchmark.*
