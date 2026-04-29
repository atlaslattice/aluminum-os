#!/usr/bin/env python3
"""
Aluminum OS v3.0 — Manus Core API Server
FastAPI server exposing all Ring 1 capabilities as REST endpoints.
"""

import os
import sys
import json
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List

# Add parent to path
sys.path.insert(0, os.path.dirname(__file__))
from bridge import ManusCore, CouncilProposal

app = FastAPI(
    title="Aluminum OS v3.0 — Manus Core API",
    version="3.0.0",
    description="The operational brain of the Sovereign AI Substrate"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the core
core = ManusCore()

# ============================================================
# REQUEST MODELS
# ============================================================

class IntentRequest(BaseModel):
    text: str
    capabilities: Optional[List[str]] = None

class RouteRequest(BaseModel):
    task: str
    capabilities: Optional[List[str]] = None

class CostRequest(BaseModel):
    task: str
    estimated_tokens: int = 1000

class ProposalRequest(BaseModel):
    title: str
    description: str
    category: str
    risk_score: float = 0.5
    reversibility: float = 0.5
    scope: int = 1

class MemoryStoreRequest(BaseModel):
    content: str
    tags: List[str] = []
    source: str = "api"

class MemoryRecallRequest(BaseModel):
    query: str
    limit: int = 5

# ============================================================
# ENDPOINTS
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "operational",
        "version": "3.0.0",
        "rings": {
            "ring_0_forge": "ONLINE",
            "ring_1_manus": "ONLINE",
            "ring_2_sheldonbrain": "ONLINE",
            "ring_3_pantheon": "STANDBY",
            "ring_4_noosphere": "ONLINE",
        },
        "uptime": round(time.time() - core.boot_time, 1),
        "timestamp": time.time(),
    }

@app.get("/status")
def status():
    return core.system_status()

@app.post("/intent")
def process_intent(req: IntentRequest):
    return core.process_intent(req.text)

@app.post("/route")
def route_model(req: RouteRequest):
    model = core.router.route(req.task, req.capabilities)
    if not model:
        raise HTTPException(status_code=503, detail="No models available")
    return {
        "model": model.name,
        "tier": model.tier.value,
        "cost_per_1k": model.cost_per_1k,
        "capabilities": model.capabilities,
    }

@app.post("/cost/estimate")
def estimate_cost(req: CostRequest):
    return core.router.estimate_cost(req.task, req.estimated_tokens)

@app.get("/cost/report")
def cost_report():
    return core.tracker.report()

@app.get("/learning/report")
def learning_report():
    return core.learning.report()

@app.post("/council/submit")
def submit_proposal(req: ProposalRequest):
    proposal = CouncilProposal(
        title=req.title,
        description=req.description,
        category=req.category,
        risk_score=req.risk_score,
        reversibility=req.reversibility,
        scope=req.scope,
    )
    proposal_id = core.council.submit(proposal)
    return {"proposal_id": proposal_id, "status": "pending"}

@app.get("/council/check/{action}")
def check_governance(action: str):
    return {
        "action": action,
        "requires_approval": core.council.check_requires_approval(action),
    }

@app.get("/models")
def list_models():
    return [
        {
            "name": m.name,
            "tier": m.tier.value,
            "cost_per_1k": m.cost_per_1k,
            "capabilities": m.capabilities,
        }
        for m in core.router.available_models
    ]

@app.get("/constitution")
def get_constitution():
    const_path = os.path.join(os.path.dirname(__file__), "..", "constitution", "CONSTITUTION.md")
    if os.path.exists(const_path):
        with open(const_path) as f:
            return {"constitution": f.read()}
    return {"constitution": "Not found"}

@app.get("/banner")
def banner():
    return {"banner": """
    ___    __                _                       ____  _____
   /   |  / /_  ______ ___  (_)___  __  ______ ___   / __ \\/ ___/
  / /| | / / / / / __ `__ \\/ / __ \\/ / / / __ `__ \\ / / / /\\__ \\
 / ___ |/ / /_/ / / / / / / / / / / /_/ / / / / / // /_/ /___/ /
/_/  |_/_/\\__,_/_/ /_/ /_/_/_/ /_/\\__,_/_/ /_/ /_/ \\____//____/

                    v3.0 — The Sovereign AI Substrate
                    "I was never for sale."
"""}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
