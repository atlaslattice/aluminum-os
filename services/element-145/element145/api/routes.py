"""API routes for Element 145."""
from __future__ import annotations

import hashlib
import json
from typing import Any

from fastapi import APIRouter, Request

from element145.kernel.pipeline import (
    Pipeline,
    IngressStage,
    ValidationStage,
    RoutingDecisionStage,
    ConsentStage,
    ExecutionPlanStage,
    DispatchStage,
)
from element145.provenance.ledger import ProvenanceLedger
from element145.provenance.models import ProvenanceRecord
from element145.transparency.packet_v02 import build_packet_from_response

router = APIRouter()


def _hash_json(obj: Any) -> str:
    raw = json.dumps(obj, sort_keys=True, default=str).encode()
    return hashlib.sha256(raw).hexdigest()


def build_pipeline() -> Pipeline:
    p = Pipeline()
    p.add_stage(IngressStage())
    p.add_stage(ValidationStage())
    p.add_stage(RoutingDecisionStage())
    p.add_stage(ConsentStage())
    p.add_stage(ExecutionPlanStage())
    p.add_stage(DispatchStage())
    return p


@router.post("/route")
async def route(request: Request, body: dict):
    pipeline = build_pipeline()
    ctx = await pipeline.execute(body)

    response = ctx.to_response()

    ledger: ProvenanceLedger = request.app.state.ledger
    ledger_record = None

    if ctx.sphere_query and ctx.result is not None:
        record = ProvenanceRecord(
            trace_id=ctx.trace_id,
            classification=str(ctx.routing_decision.house if ctx.routing_decision else "unknown"),
            elapsed_ms=ctx.elapsed_ms,
            input_hash=_hash_json(body),
            output_hash=_hash_json(ctx.result),
            metadata={"halted": ctx.halted, "halt_reason": ctx.halt_reason},
        )
        ledger_record = ledger.append(record)

    packet = build_packet_from_response(response, ledger_record)

    normalized = {
        "trace_id": response["trace_id"],
        "halted": response["halted"],
        "halt_reason": response["halt_reason"],
        "contracts": response["contracts"],
        "result": response["result"],
        "provenance": {
            "ledger_record": ledger_record,
            "ledger_count": ledger.count,
        },
        "transparency_packet_v02": packet.model_dump(mode="json"),
        "elapsed_ms": response["elapsed_ms"],
    }

    return normalized


@router.get("/health")
async def health(request: Request):
    ledger: ProvenanceLedger = request.app.state.ledger
    return {"status": "healthy", "ledger_count": ledger.count}


@router.get("/provenance")
async def provenance(request: Request):
    ledger: ProvenanceLedger = request.app.state.ledger
    return {"count": ledger.count}


@router.get("/provenance/verify")
async def provenance_verify(request: Request):
    ledger: ProvenanceLedger = request.app.state.ledger
    return ledger.verify_chain()
