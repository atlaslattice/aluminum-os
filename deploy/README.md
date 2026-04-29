# Phase 5: Reference Deployment

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    REFERENCE DEPLOYMENT                       │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Frontend   │    │   RAG API    │    │  Element-145  │  │
│  │  (Static)    │───▶│ (Cloud Run)  │    │  (Cloud Run)  │  │
│  │              │    │              │    │               │  │
│  │ Vercel /     │    │ POST /query  │    │ POST /route   │  │
│  │ Cloudflare   │    │ POST /classify│   │ POST /classify│  │
│  │              │    │ GET /lattice │    │ GET /spheres  │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                    │          │
│         └────────────────────┼────────────────────┘          │
│                              │                               │
│                    ┌─────────▼─────────┐                    │
│                    │  Krakoa MCP       │                    │
│                    │  (Optional VM)    │                    │
│                    │  WS :8765         │                    │
│                    └───────────────────┘                    │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

## Environment Variables

### Frontend (`frontends/sheldongemini-gpi/`)

```env
VITE_RAG_API_URL=https://sheldonbrain-rag-api-<HASH>.run.app
VITE_E145_API_URL=https://element145-api-<HASH>.run.app
VITE_MCP_URL=ws://localhost:8765
VITE_GEMINI_API_KEY=<your-gemini-key>
```

### RAG API (`sheldonbrain-rag-api`)

```env
PINECONE_API_KEY=<key>
PINECONE_INDEX=sheldonbrain-memory
GOOGLE_API_KEY=<gemini-key>
ONTOLOGY_VERSION=v2
CORS_ORIGINS=https://your-frontend.vercel.app,http://localhost:5173
```

### Element-145 API (new — to be deployed)

```env
GOOGLE_API_KEY=<gemini-key>
LATTICE_ONTOLOGY_PATH=./lattice_ontology.yaml
MODULE_REGISTRY_PATH=./module_registry.yaml
PORT=8080
```

## Deployment Targets

| Component | Target | Method | Status |
|-----------|--------|--------|--------|
| RAG API | Cloud Run | `gcloud run deploy` | ✅ LIVE |
| Element-145 API | Cloud Run | Dockerfile below | 🔲 PENDING |
| Frontend | Vercel / Static | `vercel deploy` | 🔲 PENDING |
| Krakoa MCP | GCE VM / local | Docker Compose | 🔲 OPTIONAL |

## Verification Checklist

After deployment, verify these paths work end-to-end:

```bash
# 1. RAG API is live and lattice-tagging works
curl -X POST $RAG_API_URL/query \
  -H "Content-Type: application/json" \
  -d '{"query": "What is the roommate agreement?", "namespace": "keep"}'

# 2. Element-145 API routing works
curl -X POST $E145_API_URL/route \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain quantum entanglement", "context": {}}'

# 3. Classification works
curl -X POST $E145_API_URL/classify \
  -H "Content-Type: application/json" \
  -d '{"text": "Design a neural network architecture"}'

# 4. Frontend loads and can reach APIs
# Open browser → verify chat, query, routing, offline fallback
```
