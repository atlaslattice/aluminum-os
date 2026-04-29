"""
Element-145 API — Reference Deployment for Aluminum OS Phase 5

Endpoints:
  POST /route    — Route a query through bridge_v2 logic
  POST /classify — Classify text to House/Sphere
  GET  /spheres  — Return all 144 spheres
  GET  /lattice  — Return full 12x12+1 ontology structure
  GET  /health   — Health check
"""

import os
import hashlib
from typing import Optional

import yaml
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="Element-145 API",
    version="1.0.0",
    description="Lattice Context Protocol API — Routes, classifies, and serves the 12×12+1 ontology",
)

# CORS
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "http://localhost:5173,http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── Load Ontology ────────────────────────────────────────────────────────────

ONTOLOGY_PATH = os.getenv("LATTICE_ONTOLOGY_PATH", "lattice_ontology.yaml")
REGISTRY_PATH = os.getenv("MODULE_REGISTRY_PATH", "module_registry.yaml")

_ontology = None
_registry = None


def get_ontology():
    global _ontology
    if _ontology is None:
        if os.path.exists(ONTOLOGY_PATH):
            with open(ONTOLOGY_PATH) as f:
                _ontology = yaml.safe_load(f)
        else:
            _ontology = {"houses": [], "element_145": {"name": "Admin Coupling Node"}}
    return _ontology


def get_registry():
    global _registry
    if _registry is None:
        if os.path.exists(REGISTRY_PATH):
            with open(REGISTRY_PATH) as f:
                _registry = yaml.safe_load(f)
        else:
            _registry = {"modules": []}
    return _registry


# ─── Models ───────────────────────────────────────────────────────────────────


class RouteRequest(BaseModel):
    query: str
    context: Optional[dict] = None


class ClassifyRequest(BaseModel):
    text: str


class RouteResponse(BaseModel):
    model: str
    route_path: str
    cost_estimate: float
    tokens_used: int
    complexity: str
    house: str
    sphere: str


class ClassifyResponse(BaseModel):
    house: str
    house_name: str
    sphere: str
    sphere_name: str
    confidence: float


# ─── Classification Logic ─────────────────────────────────────────────────────

KEYWORD_MAP = {
    "H01": {"philosophy", "consciousness", "ethics", "logic", "metaphysics", "epistemology"},
    "H02": {"math", "computer", "algorithm", "data", "statistics", "quantum", "ai", "ml", "neural", "code", "software", "programming"},
    "H03": {"physics", "chemistry", "biology", "astronomy", "geology", "climate"},
    "H04": {"engineering", "technology", "cloud", "devops", "infrastructure", "deploy", "api"},
    "H05": {"art", "music", "literature", "film", "design", "creative", "poetry"},
    "H07": {"agriculture", "environment", "energy", "water", "sustainability"},
    "H08": {"education", "teaching", "learning", "curriculum", "academic"},
    "H09": {"medicine", "health", "genomics", "pharmaceutical", "biotech"},
    "H10": {"history", "archaeology", "anthropology", "heritage"},
    "H11": {"economics", "finance", "trade", "market", "banking", "labor"},
    "H12": {"law", "governance", "regulation", "policy", "constitutional", "rights"},
}

HOUSE_NAMES = {
    "H01": "Philosophy & Logic",
    "H02": "Formal Sciences",
    "H03": "Natural Sciences",
    "H04": "Technology & Engineering",
    "H05": "Arts & Creative Expression",
    "H07": "Applied Sciences",
    "H08": "Education",
    "H09": "Life Sciences",
    "H10": "History & Heritage",
    "H11": "Social Sciences",
    "H12": "Law & Governance",
}


def classify_text(text: str) -> dict:
    """Simple keyword-based classification. Production would use embeddings."""
    text_lower = text.lower()
    scores = {}
    for house, keywords in KEYWORD_MAP.items():
        score = sum(1 for k in keywords if k in text_lower)
        if score > 0:
            scores[house] = score

    if not scores:
        return {"house": "H02", "house_name": "Formal Sciences", "sphere": "S01", "sphere_name": "General", "confidence": 0.3}

    best_house = max(scores, key=scores.get)
    confidence = min(scores[best_house] / 3.0, 1.0)

    return {
        "house": best_house,
        "house_name": HOUSE_NAMES.get(best_house, "Unknown"),
        "sphere": "S01",
        "sphere_name": "General",
        "confidence": round(confidence, 3),
    }


# ─── Routing Logic ────────────────────────────────────────────────────────────


def assess_complexity(query: str) -> str:
    q = query.lower()
    high_keywords = ["quantum", "lattice", "proof", "theorem", "topology", "governance"]
    med_keywords = ["code", "write", "draft", "analyze", "compare", "explain"]
    if any(k in q for k in high_keywords):
        return "HIGH"
    if any(k in q for k in med_keywords):
        return "MEDIUM"
    return "LOW"


def route_query(query: str, context: Optional[dict] = None) -> dict:
    """Route a query to the appropriate model/path."""
    complexity = assess_complexity(query)
    classification = classify_text(query)

    model_map = {"LOW": "local-cache", "MEDIUM": "gemini-flash", "HIGH": "gemini-2.5-flash"}
    cost_map = {"LOW": 0.001, "MEDIUM": 0.005, "HIGH": 0.015}

    return {
        "model": model_map[complexity],
        "route_path": f"BRIDGE → {classification['house']}/{classification['sphere']} → {model_map[complexity]}",
        "cost_estimate": cost_map[complexity],
        "tokens_used": len(query.split()) * 2,
        "complexity": complexity,
        "house": classification["house"],
        "sphere": classification["sphere"],
    }


# ─── Endpoints ────────────────────────────────────────────────────────────────


@app.get("/health")
def health():
    ontology = get_ontology()
    houses = len(ontology.get("houses", []))
    return {
        "status": "healthy",
        "version": "1.0.0",
        "ontology_houses": houses,
        "element_145": ontology.get("element_145") is not None,
    }


@app.post("/route", response_model=RouteResponse)
def route(req: RouteRequest):
    result = route_query(req.query, req.context)
    return RouteResponse(**result)


@app.post("/classify", response_model=ClassifyResponse)
def classify(req: ClassifyRequest):
    result = classify_text(req.text)
    return ClassifyResponse(**result)


@app.get("/spheres")
def spheres():
    ontology = get_ontology()
    all_spheres = []
    for house in ontology.get("houses", []):
        for sphere in house.get("spheres", []):
            all_spheres.append({
                "house_id": house.get("id"),
                "house_name": house.get("name"),
                "sphere_id": sphere.get("id"),
                "sphere_name": sphere.get("name"),
            })
    return {"total": len(all_spheres), "spheres": all_spheres}


@app.get("/lattice")
def lattice():
    return get_ontology()


@app.get("/registry")
def registry():
    return get_registry()
