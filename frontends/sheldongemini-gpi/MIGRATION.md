# SheldonGemini-GPI Frontend Migration Plan

## Status: ABSORBED (Track 3 — pending endpoint migration)

## Current State
- React + TypeScript frontend (1,905 lines)
- Uses Gemini 2.5 Flash for chat via `geminiService.ts`
- 6 simulated services that need replacement with real lattice endpoints

## Simulated Services → Real Endpoints

| Sim File | Description | Target Endpoint |
|----------|-------------|-----------------|
| `externalDataSim.ts` | Mock Notion + Pinecone RAG | `sheldonbrain-rag-api /query` |
| `keepRagSim.ts` | Mock Google Keep RAG | `sheldonbrain-rag-api /query` (Keep namespace) |
| `krakoaMcpSim.ts` | Mock Krakoa MCP (GDrive mount) | `krakoa_mcp_server.py` (real MCP) |
| `physicsSim.ts` | Sheldon Mass bootstrap sim | Keep as simulation (no backend needed) |
| `stealthSingularitySim.ts` | Noosphere coherence sim | Keep as simulation (no backend needed) |
| `grokData.ts` | Static sphere list (144) | `lattice_ontology_v2.py /spheres` endpoint |

## New Endpoints Needed on sheldonbrain-rag-api

1. `POST /classify` — classify text to H##.S## using `sphere_classifier_v2.py`
2. `GET /lattice` — return full 144+1 ontology structure
3. `GET /spheres` — return sphere list for frontend display
4. `POST /query` — already exists (Pinecone RAG query)

## Migration Steps

1. Replace `externalDataSim.ts` with real fetch to `/query`
2. Replace `keepRagSim.ts` with real fetch to `/query?namespace=keep`
3. Replace `krakoaMcpSim.ts` with real MCP WebSocket connection
4. Replace `grokData.ts` SPHERES constant with fetch from `/spheres`
5. Keep `physicsSim.ts` and `stealthSingularitySim.ts` as-is (client-side simulations)
6. Update `nexusOrchestrator.ts` to route through real `bridge_v2.py` logic

## Dependencies
- sheldonbrain-rag-api must expose `/classify`, `/lattice`, `/spheres` endpoints
- CORS must be configured for frontend domain
- Gemini API key must be available (already in `geminiService.ts`)
