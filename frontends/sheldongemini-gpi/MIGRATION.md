# SheldonGemini-GPI Frontend Migration Plan

## Status: MIGRATED (Track 3 — endpoint migration COMPLETE 2026-04-29)

## Current State
- React + TypeScript frontend (1,905 lines + 230 lines new latticeApi.ts)
- Uses Gemini 2.5 Flash for chat via `geminiService.ts`
- All 6 services migrated to real lattice endpoints with offline fallback

## Simulated Services → Real Endpoints (ALL MIGRATED)

| Sim File | Description | Target Endpoint | Status |
|----------|-------------|-----------------|--------|
| `externalDataSim.ts` | Mock Notion + Pinecone RAG | `sheldonbrain-rag-api /query` | ✅ DONE |
| `keepRagSim.ts` | Mock Google Keep RAG | `sheldonbrain-rag-api /query` (Keep namespace) | ✅ DONE |
| `krakoaMcpSim.ts` | Mock Krakoa MCP (GDrive mount) | `krakoa_mcp_server.py` (real MCP) | ✅ DONE |
| `nexusOrchestrator.ts` | Routing simulation | `bridge_v2.py /route` API | ✅ DONE |
| `physicsSim.ts` | Sheldon Mass bootstrap sim | Keep as simulation (no backend needed) | ✅ KEPT |
| `stealthSingularitySim.ts` | Noosphere coherence sim | Keep as simulation (no backend needed) | ✅ KEPT |
| `grokData.ts` | Static sphere list (144) | Kept static (rarely changes) | ✅ KEPT |

## New File: `latticeApi.ts`

Unified API client that all migrated services route through. Provides:
- `queryRag()` — RAG queries with namespace support (notion, keep, pinecone)
- `classifyText()` — sphere classification via sphere_classifier_v2
- `getLatticeStructure()` — full 12x12 ontology
- `getSpheres()` — sphere list for UI
- `hyperMount()` / `hapticPulse()` — Krakoa MCP tools
- `routeViaBridge()` — bridge_v2 model routing
- `latticeQuery()` — unified classify+RAG+bridge pipeline

## Architecture

```
Frontend Components
    ↓ (import)
externalDataSim.ts / keepRagSim.ts / krakoaMcpSim.ts / nexusOrchestrator.ts
    ↓ (import)
latticeApi.ts (unified client)
    ↓ (fetch)
┌─────────────────────────────────────────────┐
│  sheldonbrain-rag-api (Cloud Run)           │
│  - POST /query (Pinecone RAG)              │
│  - POST /classify (sphere_classifier_v2)   │
│  - GET /lattice (ontology structure)       │
│  - GET /spheres (sphere list)              │
├─────────────────────────────────────────────┤
│  krakoa_mcp_server (MCP over HTTP/WS)      │
│  - krakoa_drive_mount                      │
│  - krakoa_haptic_pulse                     │
├─────────────────────────────────────────────┤
│  bridge_v2 API                             │
│  - POST /route (model selection + routing) │
└─────────────────────────────────────────────┘
```

## Configuration (Environment Variables)

```env
VITE_RAG_API_URL=https://sheldonbrain-rag-api-HASH.run.app
VITE_KRAKOA_MCP_URL=ws://localhost:8765
VITE_BRIDGE_API_URL=http://localhost:8080
VITE_GEMINI_API_KEY=<key>
```

## Offline Behavior

All migrated services gracefully degrade when their backend is unavailable:
- RAG queries return mock data from hardcoded fallback stores
- MCP calls return "QUEUED" status with informative messages
- Bridge routing falls back to client-side complexity assessment
- No crashes, no blank screens — always functional

## Remaining Work
- [ ] Deploy sheldonbrain-rag-api with `/classify`, `/lattice`, `/spheres` endpoints
- [ ] Configure CORS for production frontend domain
- [ ] Set up krakoa_mcp_server HTTP endpoint (currently WS only)
- [ ] Wire `grokData.ts` SPHERES to live `/spheres` endpoint (optional — static is fine)
