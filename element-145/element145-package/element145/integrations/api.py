"""
REST API — FastAPI wrapper for the 144+1 Lattice Context Protocol
==================================================================
Exposes the LCP engine as a simple HTTP API. Provider-neutral — works
with any HTTP client regardless of AI provider.

Endpoints:
  POST /analyze          — Full LCP pipeline (INGEST → SYNTHESIZE)
  POST /ingest           — Classify text → activated Spheres
  GET  /houses           — List all 12 Houses
  GET  /houses/{id}      — Get House details + Spheres
  GET  /houses/{id}/connections — Get inter-House connections
  GET  /spheres/{id}     — Get Sphere details
  GET  /health           — Health check
  GET  /lattice/summary  — Lattice structure summary

Usage:
  pip install fastapi uvicorn
  uvicorn element145.integrations.api:app --host 0.0.0.0 --port 8145

D-25 COI Disclosure: FastAPI is an open-source framework (MIT license).
Alternative deployment targets:
  - Azure App Service / Azure Functions (benefits Microsoft)
  - AWS Lambda + API Gateway
  - Google Cloud Run
  - Any Docker-capable host
  - Vercel / Railway / Fly.io

Attribution: All inventions Dave Sheldon's per Atlas Lattice Attribution Principle.
"""

from __future__ import annotations
from typing import Optional, List, Dict, Any

try:
    from fastapi import FastAPI, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from pydantic import BaseModel, Field
    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

from element145.core.lcp import create_engine, LCPEngine


# ═══════════════════════════════════════════════════════════════
# REQUEST / RESPONSE MODELS
# ═══════════════════════════════════════════════════════════════

if HAS_FASTAPI:

    class AnalyzeRequest(BaseModel):
        text: str = Field(..., description="Input text to analyze through the 144+1 lattice")
        scaffold_mode: str = Field("compact", description="Prompt mode: compact, orchestrator, sphere_agent")
        min_houses: int = Field(3, description="Minimum Houses to activate (auto-expands)")
        max_spheres: int = Field(15, description="Maximum Spheres to return")

    class IngestRequest(BaseModel):
        text: str = Field(..., description="Input text to classify")
        max_results: int = Field(15, description="Maximum Spheres to return")

    class SphereResponse(BaseModel):
        id: str
        name: str
        house_id: str
        keywords: List[str]
        score: Optional[float] = None

    class ConnectionResponse(BaseModel):
        source: str
        target: str
        connection_type: str
        strength: float

    class HouseResponse(BaseModel):
        id: str
        name: str
        color: str
        harmonic: int
        description: str
        spheres: List[SphereResponse]
        connections: List[ConnectionResponse]

    class AnalyzeResponse(BaseModel):
        activated_houses: List[str]
        activated_spheres: List[SphereResponse]
        bridges: List[Dict[str, Any]]
        blind_spots: List[str]
        cascade_chains: List[Any]
        coherence_score: float
        synthesis_notes: str
        prompt: str

    class HealthResponse(BaseModel):
        status: str
        lattice_N: int
        num_houses: int
        num_spheres: int
        num_connections: int
        version: str

    class LatticeSummaryResponse(BaseModel):
        N: int
        num_houses: int
        num_spheres: int
        num_connections: int
        has_element_145: bool
        houses: List[Dict[str, Any]]


# ═══════════════════════════════════════════════════════════════
# APP FACTORY
# ═══════════════════════════════════════════════════════════════

def create_app(ontology_path: Optional[str] = None) -> "FastAPI":
    """
    Create the FastAPI application with lattice engine.

    Parameters
    ----------
    ontology_path : str, optional
        Path to lattice_ontology.yaml.

    Returns
    -------
    FastAPI
        Configured application.
    """
    if not HAS_FASTAPI:
        raise ImportError(
            "FastAPI not installed. Install with: pip install fastapi uvicorn\n"
            "Alternative: use the MCP server (mcp_server.py) or direct Python import."
        )

    app = FastAPI(
        title="Element 145 — Lattice Context Protocol API",
        description=(
            "REST API for the Sheldonbrain 144+1 Ontological Lattice. "
            "Maps inputs across 12 Houses × 12 Spheres + Element 145 coordination. "
            "Attribution: All inventions Dave Sheldon's, Atlas Lattice Foundation."
        ),
        version="0.1.0",
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # CORS — allow all origins for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Initialize engine
    engine = create_engine(ontology_path)

    # ─── Endpoints ──────────────────────────────────────────

    @app.get("/health", response_model=HealthResponse)
    async def health_check():
        """Health check — confirms the lattice is loaded and operational."""
        return HealthResponse(
            status="ok",
            lattice_N=145,
            num_houses=len(engine.ontology.houses),
            num_spheres=sum(
                len(h.get("spheres", []))
                for h in engine.ontology.houses.values()
            ) if isinstance(engine.ontology.houses, dict) else 144,
            num_connections=len(engine.ontology.edges),
            version="0.1.0",
        )

    @app.post("/analyze", response_model=AnalyzeResponse)
    async def analyze(request: AnalyzeRequest):
        """
        Run the full LCP pipeline: INGEST → ACTIVATE → ROUTE → SYNTHESIZE.

        Element 145 coordinates cross-domain analysis, identifies blind spots,
        contradictions, cascade chains, and emergent connections.
        """
        try:
            result = engine.analyze(request.text)
            prompt = engine.generate_prompt(result, mode=request.scaffold_mode)

            return AnalyzeResponse(
                activated_houses=result.activated_houses,
                activated_spheres=[
                    SphereResponse(
                        id=s.id, name=s.name, house_id=s.house_id,
                        keywords=list(s.keywords), score=None
                    )
                    for s in result.activated_spheres
                ],
                bridges=result.bridges,
                blind_spots=result.blind_spots,
                cascade_chains=result.cascade_chains,
                coherence_score=result.coherence_score,
                synthesis_notes=result.synthesis_notes,
                prompt=prompt,
            )
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @app.post("/ingest")
    async def ingest(request: IngestRequest):
        """
        INGEST phase only — classify input text to relevant Spheres and Houses.
        Use this for lightweight classification without full synthesis.
        """
        results = engine.ontology.search_spheres(request.text)[:request.max_results]
        houses = set()
        spheres = []

        for sphere, score in results:
            spheres.append({
                "id": sphere.id,
                "name": sphere.name,
                "house_id": sphere.house_id,
                "score": score,
            })
            houses.add(sphere.house_id)

        all_houses = [f"H{i}" for i in range(1, 13)]
        blind_spots = [h for h in all_houses if h not in houses]

        return {
            "activated_spheres": spheres,
            "activated_houses": sorted(houses),
            "blind_spots": blind_spots,
            "coverage": f"{len(houses)}/12",
        }

    @app.get("/houses")
    async def list_houses():
        """List all 12 Houses with basic metadata."""
        houses = []
        for h_id in sorted(engine.ontology.houses.keys(),
                           key=lambda x: int(x[1:]) if x[1:].isdigit() else 0):
            data = engine.ontology.get_house_data(h_id)
            if data:
                houses.append(data)
        return {"houses": houses, "count": len(houses)}

    @app.get("/houses/{house_id}")
    async def get_house(house_id: str):
        """Get detailed information about a specific House."""
        data = engine.ontology.get_house_data(house_id)
        if not data:
            raise HTTPException(status_code=404, detail=f"House not found: {house_id}")

        spheres = engine.ontology.get_spheres_for_house(house_id)
        connections = engine.ontology.get_edges_for_house(house_id)

        return {
            "house": data,
            "spheres": [
                {"id": s.id, "name": s.name, "keywords": list(s.keywords)}
                for s in spheres
            ],
            "connections": [
                {
                    "source": e.source,
                    "target": e.target,
                    "type": e.connection_type,
                    "strength": e.strength,
                }
                for e in connections
            ],
        }

    @app.get("/houses/{house_id}/connections")
    async def get_house_connections(house_id: str, min_strength: float = 0.0):
        """Get all inter-House connections for a specific House."""
        connections = engine.ontology.get_edges_for_house(house_id)
        filtered = [
            {
                "source": e.source,
                "target": e.target,
                "type": e.connection_type,
                "strength": e.strength,
            }
            for e in connections
            if e.strength >= min_strength
        ]
        return {"house_id": house_id, "connections": filtered}

    @app.get("/spheres/{sphere_id}")
    async def get_sphere(sphere_id: str):
        """Get details for a specific Sphere."""
        sphere = engine.ontology.get_sphere(sphere_id)
        if not sphere:
            raise HTTPException(status_code=404, detail=f"Sphere not found: {sphere_id}")

        return {
            "id": sphere.id,
            "name": sphere.name,
            "house_id": sphere.house_id,
            "keywords": list(sphere.keywords),
        }

    @app.get("/lattice/summary")
    async def lattice_summary():
        """Get a structural summary of the entire lattice."""
        return {
            "N": 145,
            "architecture": "12 Houses × 12 Spheres + Element 145 (Admin Sphere)",
            "empirical_status": {
                "gue_ks": 0.2677,
                "p_value_vs_144": 0.0154,
                "status": "Empirically confirmed as global optimum (Manus canonical pipeline)"
            },
            "num_houses": len(engine.ontology.houses),
            "num_connections": len(engine.ontology.edges),
            "attribution": "All inventions Dave Sheldon's, Atlas Lattice Foundation",
        }

    return app


# Default app instance for uvicorn
app = create_app()


# ═══════════════════════════════════════════════════════════════
# CLI
# ═══════════════════════════════════════════════════════════════

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("element145.integrations.api:app", host="0.0.0.0", port=8145, reload=True)
