# Substrate-Retrieval Doctrine

**Document ID:** DOCTRINE-SUBSTRATE-RETRIEVAL-001
**Date:** 2026-04-29
**Author:** Claude S1 (editorial reframing) + Manus S7 (integration)
**Status:** PROVISIONAL — Pending Council Ratification
**Ontology Version:** v4.0-DRAFT.3b

---

## §1 Core Thesis

The Atlas Lattice is a **substrate-organized retrieval graph**, not a keyword index.

VIP Elements (E145-E152) are **addressing primitives for retrieval** — they make cross-domain queries cheap by encoding which adjacencies matter for novel-insight generation. Houses (H1-H12) are **discipline containers** — they organize knowledge by the methods and traditions that produce it.

The product is not a database. It is a **substrate-organized novel-insight engine** that compounds with ingestion.

---

## §2 Retrieval Cost Principle

Substrate addressing makes cross-domain retrieval **cheap**.

**Example:** A query about "how do indigenous water sovereignty doctrines interact with state water law in the southwest" resolves via:

| Node | Role |
|------|------|
| E147.12 | Indigenous Water Knowledge & Sovereignty |
| E147.02 | Water Rights & Law |
| H10-S3 | Anthropology (discipline home) |
| H12-S5 | Constitutional/Indigenous Law (discipline home) |

This multi-node traversal is cheap because the substrate addressing encoded the adjacency at schema time. Keyword-based systems (LCC, Dewey) cannot do this without full-text search over the entire corpus.

**General principle:** When a VIP element exists for a substrate, any query that invokes that substrate as a *condition* (not merely as a *topic*) should route VIP-primary. The VIP's sub-domains encode the cross-House adjacencies that make retrieval cheap.

---

## §3 LCC Parity as Empirical Floor

LCC coverage (21/21 classes) is the **empirical floor** — it confirms the Lattice has not missed any domain that organized human knowledge production has discovered.

But LCC is a retrieval-by-keyword index. The Lattice is a retrieval-by-substrate graph. They serve different jobs:

| Dimension | LCC/Dewey | Atlas Lattice |
|-----------|-----------|---------------|
| Retrieval mode | Keyword/subject heading | Substrate traversal |
| Cross-domain | Manual see-also references | Encoded in VIP sub-domain adjacencies |
| Novel insight | Not designed for | Core purpose |
| Ingestion model | Cataloger assigns headings | Parsing pipeline writes substrate tags |
| AI integration | None | AI seats are retrieval + synthesis layer |

Coverage parity is the validation criterion. Structural difference is the value proposition.

---

## §4 Convenor-Grounded Ingestion

### §4.1 Verified-First, Then Scale

Early ingestion is small but **verified** (Convenor-attributed ground truth). The parsing pipeline trained on Convenor-verified ingestion gets ground truth that is actually grounded.

This is methodologically different from "scrape everything" — the early ingestion is small but verified, which is what makes the later ingestion large but trustable.

### §4.2 Ingestion Pipeline Architecture

The ingestion pipeline writes substrate tags to the Lattice. Its current addressing:

- **E145.04** (Ontology Management) — schema maintenance
- **E145.05** (Toolchain) — parsing/ingestion infrastructure

**Open question (§7 item 12):** As the ingestion pipeline becomes load-bearing, it may warrant a separate VIP or sub-domain ("Ingestion & Parsing Substrate"). Deferred to future Council pass.

### §4.3 Attribution Chain

Every ingested document carries:

1. **Source attribution** — who wrote it
2. **Substrate tags** — which H#-S# and E### nodes it maps to
3. **Verification status** — Convenor-verified, Council-reviewed, or unverified
4. **Ingestion timestamp** — when it entered the Lattice

---

## §5 Novel-Insight Engine Framing

Most knowledge management is "search what you already had." The Lattice is "synthesize what wasn't articulated yet, by substrate-traversal across nodes that hold ground-truth Convenor-attributed insight."

The architecture stack:

| Layer | Component | Role |
|-------|-----------|------|
| Schema | Ontology (12×12 + 8 VIPs) | Defines which adjacencies exist |
| Ingestion | Parsing/tagging pipeline | Writes substrate tags to nodes |
| Storage | Lattice graph (substrate-organized) | Holds tagged knowledge |
| Retrieval | AI seats (10-seat Council) | Traverse substrate graph for queries |
| Synthesis | Multi-LLM federation | Generate novel insights from traversal |

This is the federation-strategic-asset framing from v3.0 PROPOSAL §5.2 made operational.

---

## §6 Implications for Routing

1. **VIPs are retrieval primitives.** When routing, the question is not "which VIP is architecturally elegant?" but "which VIP makes this retrieval cheap?"

2. **Authoritative pairs encode retrieval shortcuts.** The 5 authoritative pairs (§4.3 of the spec) are the most common retrieval shortcuts — they encode the most frequent discipline-substrate adjacencies.

3. **Cross-VIP intersection patterns encode compound queries.** The 7 intersection patterns (§4.4) are the most common multi-substrate queries.

---

## §7 Provenance

This doctrine is derived from Claude S1's substrate-retrieval reframing memo (2026-04-29), integrated by Manus S7 into the v4.0-DRAFT.3b specification. The three key insights:

1. VIPs are addressing primitives for retrieval, not just architectural elegance
2. Convenor-grounded ingestion first matters because of attribution-and-verification
3. The "brain of novel insights" framing is what makes this commercially meaningful

---

*End of Substrate-Retrieval Doctrine*
