# Tucker V4 Configurator

**Co-designed with GPT-4.1 and Gemini 2.5 Pro**

**Source:** Google AI Studio (aistudio.google.com) + splitmerge420/tucker-gemini-GPT-
**Migrated:** 2026-03-21
**Original repo:** https://github.com/splitmerge420/tucker-gemini-GPT-
**Classification:** Chatbot / Constitutional AI Interface
**Aluminum OS Integration:** ALUM-INT-008

---

## What This Does

Tucker is a constitutional chatbot originally built in Google AI Studio, co-designed with GPT-4.1
and Gemini 2.5 Pro. It serves as the conversational interface layer for Aluminum OS — routing
user queries through the Pantheon Council, applying Kintsugi constitutional policies, and
synthesizing responses across multiple AI models.

Tucker V4 (Configurator) is the canonical production build. Tucker V3 (Explorer) is the research
and deep-synthesis variant.

## Atlas Lattice Relevance

Tucker is the **public-facing conversational interface** for the Atlas Lattice Foundation.
Unlike Sheldonbrain (Dave's private memory engine) or Janus (continuity system), Tucker is
**designed to be public** — it represents the foundation's ability to engage externally while
remaining constitutionally governed.

Integration points within Aluminum OS:
- **Ring 3** (Pantheon Council): All Tucker responses reviewed by Council quorum
- **Ring 4** (Noosphere): Tucker runs as App #35 (`ALUM-INT-008`)
- **Kintsugi layer**: All responses pre-screened against KINTSUGI-001 through KINTSUGI-016
- **Model Router**: Tucker uses 3-tier routing (GPT primary → Gemini synthesis → Claude oversight)
- **Janus integration**: Tucker session state tracked in Janus Daily Pulse

## Architecture

```
Tucker V4 Request Flow:
  User Input
    → ConstitutionalRouter (Ring 0: pre-screen against INV-1 through INV-37)
    → Model Router (Ring 1: GPT-4.1 primary / Gemini synthesis / Claude oversight)
    → Pantheon Council (Ring 3: quorum vote, flag or approve)
    → Kintsugi Audit (Ring 4: OPA policy evaluation, PQC-signed log)
    → Response Delivery
    → Janus Heartbeat update
```

## Personas

| Persona | Description |
|---|---|
| **Tucker V4 Default** | Balanced GPT+Gemini synthesis, constitutional oversight |
| **Tucker V3 Explorer** | Deep research mode, DeerFlow style multi-source |
| **Tucker Coder** | Code-first, Rust+Python+TypeScript, aluminum-os aware |
| **Tucker Sovereign** | Constitutional mode, Atlas Lattice governance |
| **Tucker Health** | Healthcare focus, HIPAA-aware, FHIR R4 |

## Files

| File | Description |
|---|---|
| `README.md` | This file |
| `MIGRATION_NOTES.md` | Migration status and what's needed |
| `index.html` | Tucker V4 standalone web app (from AI Studio) |

## Dedup Note

There are 17+ identical Tucker V4 Configurator instances in Google AI Studio.
**Only one canonical version is kept here.** Tucker V3 Explorer is in `../tucker-v3-explorer/`.
All other duplicates should be deleted from AI Studio.

---

*Tucker V4 Configurator — Google AI Studio Migration — Constitutional Scribe — Atlas Lattice Foundation — 2026-03-21*
