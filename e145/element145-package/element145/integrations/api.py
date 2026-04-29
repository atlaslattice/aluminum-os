"""
Element 145 REST API — FastAPI Integration
=============================================
8 endpoints exposing the full 144+1 lattice and LCP pipeline.

Endpoints:
  GET  /health                    — Health check
  POST /analyze                   — Full LCP pipeline (INGEST→ACTIVATE→ROUTE→SYNTHESIZE)
  POST /ingest                    — INGEST phase only
  GET  /houses                    — List all 12 Houses
  GET  /houses/{house_id}         — House detail with Spheres
  GET  /houses/{house_id}/connections — Inter-House connections
  GET  /spheres/{sphere_id}       — Sphere detail
  GET  /lattice/summary           — Full lattice summary

Alternative REST frameworks: Flask, Django, Starlette, Falcon.
D-25 COI Disclosure: S4 Microsoft seat built this integration.

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from element145.core import (
    LCPEngine,
    LatticeOntology,
    AnalysisResult,
    HOUSE_NAMES,
)

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

# ═══════════════════════════════════════════════════════════════
# REQUEST / RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════

if HAS_FASTAPI:

    class AnalyzeRequest(BaseModel):
        task: str = Field(..., description="Analysis task or question")
        min_relevance: float = Field(0.05, description="Minimum sphere relevance threshold")

    class IngestRequest(BaseModel):
        text: str = Field(..., description="Input text to classify")
        min_relevance: float = Field(0.05, description="Minimum relevance threshold")

    class SphereResponse(BaseModel):
        id: str
        name: str
        house_id: str
        house_name: str
        index: int
        keywords: List[str]

    class BridgeResponse(BaseModel):
        houses: List[str]
        names: List[str]
        type: str
        strength: float
        description: str

    class AnalysisResponse(BaseModel):
        task: str
        activated_houses: List[str]
        activated_sphere_count: int
        bridges: List[Dict[str, Any]]
        blind_spots: List[str]
        cascade_chains: List[Dict[str, Any]]
        coherence_score: float
        synthesis_notes: str
        house_analyses: Dict[str, Any]

    class HouseResponse(BaseModel):
        id: str
        name: str
        index: int
        color: str
        description: str
        spheres: List[SphereResponse]
        connections: List[Dict[str, Any]]

    class ConnectionResponse(BaseModel):
        source: str
        target: str
        type: str
        strength: float
        description: str
        examples: List[str]

    class LatticeSummaryResponse(BaseModel):
        name: str
        version: str
        total_houses: int
        total_spheres: int
        total_connections: int
        canonical_n: int
        houses: List[Dict[str, str]]
        element_145: Dict[str, Any]

# ═══════════════════════════════════════════════════════════════
# APP FACTORY
# ═══════════════════════════════════════════════════════════════

def create_app(ontology_path: Optional[str] = None) -> "FastAPI":
    """Create and configure the FastAPI application."""
    if not HAS_FASTAPI:
        raise ImportError(
            "FastAPI not installed. Install with: pip install element145[api]"
        )

    app = FastAPI(
        title="Element 145 — Lattice Context Protocol API",
        description=(
            "REST API for the Sheldonbrain 144+1 Ontological Lattice. "
            "12 Houses × 12 Spheres + Element 145 (Admin Sphere). "
            "N=145 empirically confirmed as global optimum. "
            "Attribution: All inventions Dave Sheldon's, Atlas Lattice Foundation."
        ),
        version="2.0.0",
        license_info={"name": "Atlas Lattice Foundation License"},
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    engine = LCPEngine(LatticeOntology(ontology_path))

    # ─── Health ───────────────────────────────────────────

    @app.get("/health")
    async def health():
        issues = engine.ontology.validate()
        return {
            "status": "healthy" if not issues else "degraded",
            "version": "2.0.0",
            "houses": len(engine.ontology.houses),
            "spheres": len(engine.ontology.spheres),
            "connections": len(engine.ontology.edges),
            "canonical_n": 145,
            "issues": issues,
        }

    # ─── Full Pipeline ────────────────────────────────────

    @app.post("/analyze", response_model=AnalysisResponse)
    async def analyze(req: AnalyzeRequest):
        result = engine.analyze(req.task, req.min_relevance)
        return AnalysisResponse(
            task=result.task,
            activated_houses=result.activated_houses,
            activated_sphere_count=len(result.activated_spheres),
            bridges=result.bridges,
            blind_spots=result.blind_spots,
            cascade_chains=result.cascade_chains,
            coherence_score=result.coherence_score,
            synthesis_notes=result.synthesis_notes,
            house_analyses=result.house_analyses,
        )

    # ─── Ingest Only ──────────────────────────────────────

    @app.post("/ingest")
    async def ingest(req: IngestRequest):
        state = engine.ingest(req.text, req.min_relevance)
        return {
            "activated_houses": sorted(state.activated_houses),
            "activated_spheres": {
                sid: {
                    "name": engine.ontology.spheres[sid].name,
                    "house": engine.ontology.spheres[sid].house_id,
                    "relevance": score,
                }
                for sid, score in sorted(
                    state.activated_spheres.items(),
                    key=lambda x: x[1], reverse=True,
                )
                if sid in engine.ontology.spheres
            },
            "house_coverage": state.house_coverage,
            "sphere_coverage": state.coverage,
        }

    # ─── Houses ───────────────────────────────────────────

    @app.get("/houses")
    async def list_houses():
        return {
            "houses": [
                {"id": hid, "name": hdata.get("name", hid),
                 "index": hdata.get("index", 0),
                 "sphere_count": len(engine.ontology.get_spheres_for_house(hid)),
                 "connection_count": len(engine.ontology.get_edges_for_house(hid))}
                for hid, hdata in sorted(engine.ontology.houses.items(),
                                          key=lambda x: int(x[0][1:]))
            ],
            "total": len(engine.ontology.houses),
        }

    @app.get("/houses/{house_id}")
    async def get_house(house_id: str):
        hdata = engine.ontology.get_house_data(house_id)
        if hdata is None:
            raise HTTPException(status_code=404, detail=f"House {house_id} not found")
        spheres = engine.ontology.get_spheres_for_house(house_id)
        edges = engine.ontology.get_edges_for_house(house_id)
        return {
            **hdata,
            "spheres": [
                {"id": s.id, "name": s.name, "index": s.index,
                 "keywords": list(s.keywords)}
                for s in spheres
            ],
            "connections": [
                {"source": e.source, "target": e.target,
                 "type": e.edge_type, "strength": e.strength,
                 "to": e.other(house_id)}
                for e in edges
            ],
        }

    @app.get("/houses/{house_id}/connections")
    async def get_house_connections(house_id: str):
        hdata = engine.ontology.get_house_data(house_id)
        if hdata is None:
            raise HTTPException(status_code=404, detail=f"House {house_id} not found")
        edges = engine.ontology.get_edges_for_house(house_id)
        return {
            "house_id": house_id,
            "house_name": hdata.get("name", house_id),
            "connections": [
                {"source": e.source, "target": e.target,
                 "type": e.edge_type, "strength": e.strength,
                 "description": e.description,
                 "examples": list(e.examples),
                 "connected_to": e.other(house_id)}
                for e in edges
            ],
            "total": len(edges),
        }

    # ─── Spheres ──────────────────────────────────────────

    @app.get("/spheres/{sphere_id}")
    async def get_sphere(sphere_id: str):
        s = engine.ontology.get_sphere(sphere_id)
        if s is None:
            raise HTTPException(status_code=404, detail=f"Sphere {sphere_id} not found")
        return {
            "id": s.id,
            "name": s.name,
            "house_id": s.house_id,
            "house_name": s.house_name,
            "index": s.index,
            "keywords": list(s.keywords),
            "is_admin": s.is_admin,
        }

    # ─── Lattice Summary ─────────────────────────────────

    @app.get("/lattice/summary")
    async def lattice_summary():
        return {
            "name": "Sheldonbrain 144+1 Ontological Lattice",
            "version": "2.0.0",
            "structure": "12 Houses × 12 Spheres + Element 145 (Admin Sphere)",
            "canonical_n": 145,
            "gue_ks_canonical": 0.2677,
            "gue_ks_optimized": 0.2447,
            "total_houses": len(engine.ontology.houses),
            "total_spheres": len(engine.ontology.spheres),
            "total_connections": len(engine.ontology.edges),
            "houses": [
                {"id": hid, "name": hdata.get("name", hid)}
                for hid, hdata in sorted(engine.ontology.houses.items(),
                                          key=lambda x: int(x[0][1:]))
            ],
            "element_145": engine.ontology.element_145,
            "attribution": "All inventions Dave Sheldon's, Atlas Lattice Foundation",
        }

    return app

# ═══════════════════════════════════════════════════════════════
# ENTRY POINT
# ═══════════════════════════════════════════════════════════════

def main():
    """CLI entry point: element145-api"""
    if not HAS_FASTAPI:
        print("Error: FastAPI not installed. Install with: pip install element145[api]")
        return

    import argparse
    parser = argparse.ArgumentParser(description="Element 145 REST API Server")
    parser.add_argument("--host", default="0.0.0.0", help="Bind host")
    parser.add_argument("--port", type=int, default=8145, help="Bind port")
    parser.add_argument("--ontology", type=str, default=None,
                        help="Path to lattice_ontology.yaml")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload")
    args = parser.parse_args()

    import uvicorn
    app = create_app(args.ontology)
    uvicorn.run(app, host=args.host, port=args.port, reload=args.reload)


if __name__ == "__main__":
    main()
