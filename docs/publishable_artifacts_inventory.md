# Publishable Artifacts Inventory — Aluminum UWS Ecosystem

**Author:** Manus AI | **Date:** April 27, 2026  
**Purpose:** Identify all deployable UIs, websites, and integrable artifacts across AI Studio (52 files) and GitHub (50 repos) for Manus server publication

---

## Executive Summary

After re-auditing all 52 AI Studio codebases and 50 GitHub repos, I've identified **25 deployable web applications** from AI Studio and **2 deployable repos** from GitHub. Of these, **8 are Aluminum-related flagship apps** that should be published immediately, **9 are valuable supporting tools**, and the rest are reference implementations or duplicates.

The AI Studio apps are "Antigravity builds" — single-file React+Tailwind applications that were built inside Google AI Studio's code generation environment. They contain complete HTML+React+Tailwind code that can be extracted and deployed as static sites on Manus servers with minimal modification (primarily: replacing hardcoded API keys with environment variables).

---

## Priority 1: Aluminum Flagship Apps (Deploy Immediately)

These are the crown jewels — complete, working UIs that demonstrate the Aluminum UWS ecosystem.

| # | App | Source | Size | Stack | What It Is |
|---|-----|--------|------|-------|------------|
| 1 | **Janus Enhanced Ingestion** | AI Studio #03 | 2.26M chars | React + Tailwind + Three.js + WebAudio | The most complete ORCS app. House classification, Sphere Lattice 3D visualization, AraConsole, dual Gemini/Grok services, ethics vetting, confabulation detection, token tracking, live voice, telemetry. 16 Gemini model versions. 30 components, 18 files. |
| 2 | **Grokbrain Ingestion UI** | AI Studio #09 | 527K chars | React + IndexedDB + WebAudio + Canvas | RAG + orchestration hub. Pinecone vector search, Notion integration, Keep RAG sim, Krakoa MCP sim, Nexus orchestration, live voice with audio visualization. 27 components, 14 files. |
| 3 | **Sanctuary v2 Council Manager** | AI Studio #02 | 111K chars | React + Tailwind | The Council UI. CouncilView with concurrent multi-model API calls, DashboardView, DeploymentView, LibraryView, SettingsView, Sidebar. 14 components, 12 files. |
| 4 | **ATLAS v3 Governance Lattice** | AI Studio #40 | 49K chars | React + Tailwind | Quasicrystalline Governance Lattice. Federation Oracle visualization. 5 components, 10 files. |
| 5 | **Swiss Governance Simulator** | AI Studio #42 | 43K chars | React + Tailwind | Interactive simulation of Swiss direct democracy. Citizen initiative to federal law. 9 components, 10 files. |
| 6 | **Sphere Agent Abstraction** | AI Studio #44 | 41K chars | React + Tailwind | Sphere agent dataclass abstraction. Core typing for the 144-sphere system. 6 components, 10 files. |
| 7 | **Sheldongemini-GPI** | GitHub (private) | 26 files | React + Vite + @google/genai | Sheldon Gemini Bazinga — Vite+React chat interface with Gemini integration. Already structured as a proper npm project. |
| 8 | **Atlas Lattice Core Repo** | AI Studio #31 | 194K chars | React + Tailwind + Three.js | Structured repo layout with ChatInterface, Library, MarkdownRenderer, Sidebar, Arbiter chat. 14 components, 11 files. |

---

## Priority 2: Supporting Tools (Deploy After Flagships)

| # | App | Source | Size | Stack | What It Is |
|---|-----|--------|------|-------|------------|
| 9 | **Council of Sams** | AI Studio #36 | 94K chars | React + Tailwind | Multi-agent deliberation: specialized Sam nodes, contrarian, synthesizer. YAML agent configs. |
| 10 | **Tucker Pendragon** | AI Studio #16 | 164K chars | React + Tailwind + Three.js | Diplomatic alignment agent. Full React app with AlignmentChart, NexusSimulation, PhilosophyPanel, SystemBlueprint. |
| 11 | **ShellGemini v11 Genesis Forge** | AI Studio #12 | 118K chars | React + Tailwind | MindLab, BodyLab, SynthesisView. Dual-analysis with Gemini 3 models. |
| 12 | **Elon Tensor ATLAS** | AI Studio #38 | 72K chars | React + Tailwind | Synthetic resonance of decision architecture powered by ATLAS governance kernel. |
| 13 | **Neuromorphic SNN** | AI Studio #39 | 70K chars | React + Tailwind | Spiking Neural Networks simulation. Energy efficiency, anomaly detection. |
| 14 | **Kintsuji Merge Template** | AI Studio #33 | 123K chars | React + Tailwind | Kintsugi merge request template with 13 components. Code repair philosophy. |
| 15 | **Synergy Projects** | AI Studio #51 | 51K chars | React + Tailwind | Cross-project synergy analysis and integration. |
| 16 | **Acoustic Resonator** | AI Studio #41 | 48K chars | React + Tailwind | Self-tuning RLC resonator with feedback loops. |
| 17 | **Signal Processing** | AI Studio #45 | 40K chars | React + Tailwind | DSP with scipy: butterworth filters, FFT, convolution. |

---

## Priority 3: Reference / Duplicates (Don't Deploy Separately)

| # | App | Source | Reason |
|---|-----|--------|--------|
| 18 | Grokbrain Examination (#28) | AI Studio | Subset of Grokbrain Ingestion UI — analysis session, not standalone |
| 19 | Bazinga Strategic Realignment (#34) | AI Studio | Same code as Genesis Forge (#12) — duplicate |
| 20 | Sanctuary v2 Deployment (#22) | AI Studio | Exact duplicate of Sanctuary v2 (#02) |
| 21 | Tucker V4 Chat (#19) | AI Studio | Minimal chat wrapper — superseded by Tucker Pendragon |
| 22 | WatsonX Collaborative (#43) | AI Studio | Same code as Pantheon Engine (#06) — duplicate |
| 23 | Pantheon Engine (#06) | AI Studio | Clean but minimal — subsumed by Council of Sams |
| 24 | Code Aggregation (#50) | AI Studio | Meta-tool, not user-facing |
| 25 | Grey Synthesis Tensor (#47) | AI Studio | Backend-focused, no meaningful UI |
| 26 | DeepSeek Unified (#17) | AI Studio | Backend Python class, no UI |

---

## GitHub Repos — Deployable as Web Apps

| Repo | Type | Status | Deploy Path |
|------|------|--------|-------------|
| **sheldongemini-GPI** (private) | Vite + React + TypeScript | Ready — proper npm project structure | Clone → `pnpm install` → `pnpm build` → deploy static |
| **constitutional-continuum** (private) | TypeScript | Minimal (7 files) — needs build | Needs investigation, likely not standalone UI |

---

## GitHub Repos — Valuable for Integration (Not Standalone Deployable)

| Repo | What to Extract | Integration Target |
|------|----------------|-------------------|
| `aluminum-os` | Royalty Runtime (Rust, 1,190 lines) | Element 145 audit layer |
| `aluminum-os-v3` | Python port (7,905 lines) | Direct Element 145 extraction |
| `uws` | MCP Server, Civic Layer, Budget Enforcement (36K lines) | Element 145 core modules |
| `manus-2.0-toolkit` | Kernel API (20 functions) | UWS kernel interface |
| `constitutional-os` | 37 invariants, 144-sphere ontology | Governance enforcement |
| `atlas-lattice-foundation` | Foundation infrastructure | Deployment tooling |
| `bazinga` | Constitutional universal compute layer | Reference architecture |
| `manus-artifacts` | Aluminum OS / SHELDONBRAIN artifacts | Pattern library |

---

## Deployment Strategy for Manus Servers

### Approach: Extract → Adapt → Deploy

The AI Studio apps are embedded in conversation JSON. The extraction pipeline is:

1. **Extract** the React/HTML code from the JSON conversation chunks
2. **Adapt** by replacing hardcoded API keys with environment variables
3. **Wrap** in a proper Vite project structure (already done for sheldongemini-GPI)
4. **Deploy** to Manus servers as static sites

### Recommended Deployment Order

| Phase | Apps | Why This Order |
|-------|------|----------------|
| **Phase A** (immediate) | Janus Enhanced Ingestion, Sanctuary v2 Council Manager | These are the two apps that demonstrate the full ORCS pipeline — routing, governance, and multi-model council |
| **Phase B** (next) | ATLAS v3 Governance Lattice, Swiss Governance Simulator, Sphere Agent Abstraction | These demonstrate the governance and ontology layers |
| **Phase C** (supporting) | Grokbrain Ingestion UI, Atlas Lattice Core Repo, Council of Sams | These demonstrate RAG, orchestration, and multi-agent deliberation |
| **Phase D** (showcase) | Tucker Pendragon, Genesis Forge, Neuromorphic SNN, Elon Tensor ATLAS | These demonstrate specialized capabilities |

### Technical Requirements per App

| App | API Keys Needed | External Services | Deployment Complexity |
|-----|----------------|-------------------|----------------------|
| Janus Enhanced Ingestion | Gemini API, Grok API | Google AI, xAI | HIGH — 16 model versions, dual-service |
| Grokbrain Ingestion UI | Gemini API | Google AI, Pinecone (simulated) | MEDIUM — IndexedDB handles local state |
| Sanctuary v2 Council Manager | Gemini API (multi-model) | Google AI | MEDIUM — concurrent API calls |
| ATLAS v3 Governance Lattice | Gemini API | Google AI | LOW — mostly visualization |
| Swiss Governance Simulator | Gemini API | Google AI | LOW — simulation logic is client-side |
| Sphere Agent Abstraction | Gemini API | Google AI | LOW — type definitions + visualization |
| Sheldongemini-GPI | Gemini API | Google AI | LOW — already a proper Vite project |
| Atlas Lattice Core Repo | Gemini API | Google AI | LOW — standard React app |

---

## Key Findings

### What's Actually Deployable Right Now (Zero Modification)

1. **sheldongemini-GPI** — Already a proper Vite project. Clone, install, build, deploy.

### What Needs Extraction + Minor Adaptation

2-8. All Priority 1 AI Studio apps — need the React code extracted from JSON and wrapped in a Vite scaffold. The code itself is complete and working (it ran in AI Studio's Antigravity environment).

### What's NOT Deployable (Backend Required)

- `aluminum-os` / `aluminum-os-v3` / `uws` — These are Rust/Python backend systems, not web UIs
- `bazinga` — Build system / compute layer, not a frontend
- `manus-artifacts` — Artifacts collection, not an app

### Security Concern

Several AI Studio apps contain **hardcoded API keys** (visible in the extracted code). These MUST be replaced with environment variables before any public deployment. Specifically:
- Atlas Lattice Core (#05) contains a visible Gemini API key in the code
- Several apps reference `YOUR_API_KEY` placeholders (safe)
- Janus and Grokbrain use runtime key injection (safe)

---

## Integration Opportunities Beyond Deployment

| Artifact | Integration Path | Value |
|----------|-----------------|-------|
| `classify_content()` from Sheldon-Grok v2 | Direct reuse in Element 145 classifier | HIGH — working 144-sphere classifier |
| `nexusOrchestrator.ts` from Grokbrain | Pattern for ADK routing graph | HIGH — multi-agent orchestration |
| `CouncilView` from Sanctuary v2 | Direct reuse for Council debate UI | HIGH — the exact UI we need |
| `sphereService.ts` from Janus | House 0 Directory data layer | HIGH — sphere ontology operations |
| `geminiService.ts` pattern | Refactor to LiteLLM wrapper | MEDIUM — provider abstraction |
| `memoryService.ts` from Janus | Agent memory bank pattern | MEDIUM — persistence layer |
| Governance simulation from Gaia Core | House 12 enforcement engine | HIGH — constitutional constraints |
| `LiveVoiceMode` from Grokbrain | Voice interaction for Ara | MEDIUM — mature audio interface |

---

## Recommendation

**Start with sheldongemini-GPI** — it's already a proper project, deploy it to Manus in 10 minutes.

Then **extract Janus Enhanced Ingestion** — it's the crown jewel, 2.26M chars of working ORCS pipeline code. This becomes the reference implementation for Element 145's UI layer.

Then **extract Sanctuary v2** — it's the Council UI that Element 145 needs for multi-model debate visualization.

The rest can be deployed as a portfolio/showcase of the Aluminum UWS ecosystem capabilities.

**Total estimated deployment time:**
- Phase A (2 apps): 2-3 hours (extraction + adaptation + deploy)
- Phase B (3 apps): 3-4 hours
- Phase C (3 apps): 3-4 hours  
- Phase D (4 apps): 4-5 hours
- Full portfolio: ~15 hours of focused work

---

## Claude's Synthesis Document Integration

You mentioned Claude is producing an extensive synthesis document. When it arrives, it should be cross-referenced against this inventory to:
1. Confirm which apps map to which Element 145 modules
2. Identify any gaps where no existing app covers a required capability
3. Prioritize extraction order based on Claude's dependency analysis
