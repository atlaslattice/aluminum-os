#!/usr/bin/env python3
"""
Zapier Webhook Endpoints
Dedicated webhooks for Zapier automation workflows

Workflow:
1. G-Drive → Zapier → /zapier/ingest → Staging
2. Staging → Notion (for review)
3. LLM Agent (Zapier) → /zapier/review → Updates status
4. Manual approval → /zapier/approve → Vector DB
"""

import os
from typing import List, Dict, Any, Optional
from datetime import datetime

from fastapi import APIRouter, HTTPException, Header, Depends
from pydantic import BaseModel, Field
import structlog

# Sheldonbrain imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from config import get_ontology, VAULT_HOUSE
from integrations import NotionIngestionClient
from ingestion.ingestion_pipeline import StagingLayer, SignificanceFilter

logger = structlog.get_logger()

# Create router
router = APIRouter(prefix="/zapier", tags=["Zapier Webhooks"])

# Initialize services (will be set on startup)
ontology = None
notion_client = None
staging_layer = None
significance_filter = None


# Pydantic Models
class ZapierIngestRequest(BaseModel):
    """Request model for ingesting content from Zapier"""
    title: str = Field(..., description="Document title")
    content: str = Field(..., description="Document content")
    source: str = Field(..., description="Source URL or identifier")
    source_type: str = Field(default="zapier", description="Type of source (gdrive, arxiv, etc.)")
    metadata: Optional[Dict[str, Any]] = Field(default=None, description="Additional metadata")
    auto_categorize: bool = Field(default=True, description="Automatically categorize into sphere")
    push_to_notion: bool = Field(default=True, description="Push to Notion for review")


class ZapierIngestResponse(BaseModel):
    """Response model for ingest webhook"""
    status: str
    item_id: str
    title: str
    categorized: bool
    house: Optional[str] = None
    sphere: Optional[str] = None
    sphere_id: Optional[str] = None
    notion_page_id: Optional[str] = None
    notion_url: Optional[str] = None
    message: str


class ZapierReviewRequest(BaseModel):
    """Request model for LLM review callback"""
    item_id: str = Field(..., description="Item ID from staging")
    review_status: str = Field(..., description="approved, rejected, needs_human_review")
    confidence_score: float = Field(default=0.0, ge=0.0, le=1.0, description="LLM confidence score")
    llm_feedback: Optional[str] = Field(default=None, description="LLM's reasoning")
    suggested_house: Optional[str] = Field(default=None, description="LLM's suggested house")
    suggested_sphere: Optional[str] = Field(default=None, description="LLM's suggested sphere")


class ZapierReviewResponse(BaseModel):
    """Response model for review callback"""
    status: str
    item_id: str
    action_taken: str
    message: str


class ZapierApproveRequest(BaseModel):
    """Request model for manual approval"""
    item_ids: List[str] = Field(..., description="List of item IDs to approve")
    user: str = Field(default="zapier_user", description="User approving")
    ingest_to_vector_db: bool = Field(default=True, description="Ingest to vector database")


class ZapierApproveResponse(BaseModel):
    """Response model for approval"""
    status: str
    approved_count: int
    failed_count: int
    message: str


class ZapierStatusRequest(BaseModel):
    """Request model for status query"""
    item_id: Optional[str] = Field(default=None, description="Specific item ID")
    status_filter: Optional[str] = Field(default=None, description="Filter by status")
    limit: int = Field(default=10, ge=1, le=100, description="Max results")


class ZapierStatusResponse(BaseModel):
    """Response model for status query"""
    items: List[Dict[str, Any]]
    count: int
    summary: Dict[str, int]


# Initialize function (called on API startup)
def initialize_zapier_services():
    """Initialize Zapier webhook services"""
    global ontology, notion_client, staging_layer, significance_filter

    try:
        # Load ontology
        ontology = get_ontology()
        logger.info("zapier_ontology_loaded", spheres=len(ontology.spheres))

        # Initialize Notion client (if credentials available)
        try:
            notion_client = NotionIngestionClient()
            logger.info("zapier_notion_client_initialized")
        except Exception as e:
            logger.warning("zapier_notion_client_unavailable", error=str(e))
            notion_client = None

        # Initialize staging layer
        staging_layer = StagingLayer(staging_dir="./staging/zapier")
        logger.info("zapier_staging_layer_initialized")

        # Initialize significance filter
        significance_filter = SignificanceFilter(use_llm=False)
        logger.info("zapier_significance_filter_initialized")

        logger.info("zapier_services_initialized")
        return True

    except Exception as e:
        logger.error("zapier_services_init_failed", error=str(e))
        return False


# Webhook Endpoints

@router.post("/ingest", response_model=ZapierIngestResponse)
async def zapier_ingest_webhook(request: ZapierIngestRequest):
    """
    Webhook for ingesting content from Zapier triggers

    Workflow:
    1. Receive content from Zapier (G-Drive, RSS, etc.)
    2. Auto-categorize into 12 Houses sphere (optional)
    3. Add to staging layer
    4. Push to Notion for review (optional)
    5. Return item details

    Example Zapier trigger:
    - New file in Google Drive → Trigger webhook
    - New RSS item → Trigger webhook
    - Scheduled fetch → Trigger webhook
    """
    if not staging_layer or not ontology:
        raise HTTPException(status_code=503, detail="Zapier services not initialized")

    logger.info("zapier_ingest_received",
               title=request.title[:50],
               source=request.source)

    try:
        # Auto-categorize if requested
        categorized = False
        house = None
        sphere_name = None
        sphere_id = None
        sphere_obj = None

        if request.auto_categorize:
            # Try to categorize based on content
            sphere_obj = ontology.categorize_content(request.content, method="keyword")

            if sphere_obj:
                house = sphere_obj.house
                sphere_name = sphere_obj.name
                sphere_id = sphere_obj.sphere_id
                categorized = True
                logger.info("zapier_content_categorized",
                           title=request.title[:30],
                           sphere=sphere_name)

        # If not categorized, use metadata hints or default
        if not categorized and request.metadata:
            suggested_house = request.metadata.get("house")
            suggested_sphere = request.metadata.get("sphere")

            if suggested_sphere:
                sphere_obj = ontology.get_sphere(suggested_sphere)
                if sphere_obj:
                    house = sphere_obj.house
                    sphere_name = sphere_obj.name
                    sphere_id = sphere_obj.sphere_id
                    categorized = True

        # Default to first sphere if still not categorized
        if not categorized:
            sphere_obj = ontology.spheres[0]  # Default to Physics
            house = sphere_obj.house
            sphere_name = sphere_obj.name
            sphere_id = sphere_obj.sphere_id
            logger.warning("zapier_using_default_sphere", title=request.title[:30])

        # Prepare item for staging
        item_data = {
            "title": request.title,
            "content": request.content,
            "source": request.source,
            "source_type": request.source_type,
            "published_date": datetime.now().isoformat(),
            "metadata": request.metadata or {}
        }

        # Add to staging
        items = [item_data]
        count = staging_layer.add_to_staging(items, source="zapier")

        if count == 0:
            raise HTTPException(status_code=400, detail="Failed to add item to staging (duplicate?)")

        # Get item ID (generated by staging layer)
        pending = staging_layer.get_pending(limit=1)
        if not pending:
            raise HTTPException(status_code=500, detail="Item added but could not retrieve ID")

        item_id = pending[0]['id']

        # Push to Notion if requested
        notion_page_id = None
        notion_url = None

        if request.push_to_notion and notion_client and sphere_obj:
            try:
                page = notion_client.create_page(
                    title=request.title,
                    content=request.content[:2000],  # Notion limit
                    source=request.source,
                    house=house,
                    sphere_name=sphere_name,
                    sphere_id=sphere_id,
                    element=sphere_obj.element,
                    god=sphere_obj.god,
                    timestamp=datetime.now().isoformat(),
                    status="Pending Review"
                )

                notion_page_id = page["id"]
                notion_url = page["url"]

                logger.info("zapier_pushed_to_notion",
                           item_id=item_id,
                           page_id=notion_page_id)

            except Exception as e:
                logger.error("zapier_notion_push_failed",
                            error=str(e),
                            item_id=item_id)
                # Don't fail the whole request if Notion fails

        logger.info("zapier_ingest_complete",
                   item_id=item_id,
                   title=request.title[:30])

        return ZapierIngestResponse(
            status="success",
            item_id=item_id,
            title=request.title,
            categorized=categorized,
            house=house,
            sphere=sphere_name,
            sphere_id=sphere_id,
            notion_page_id=notion_page_id,
            notion_url=notion_url,
            message=f"Content ingested and categorized as {house} :: {sphere_name}"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("zapier_ingest_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


@router.post("/review", response_model=ZapierReviewResponse)
async def zapier_review_callback(request: ZapierReviewRequest):
    """
    Webhook for LLM review callback from Zapier

    Workflow:
    1. Zapier LLM agent reviews staged content
    2. LLM sends review result to this endpoint
    3. Update staging status based on review
    4. If approved → auto-approve for ingestion
    5. If rejected → mark as rejected
    6. If needs_human_review → keep in pending

    Example Zapier flow:
    - Trigger: New item in Notion (from /zapier/ingest)
    - Action: Send to LLM for review
    - Action: Send review result to this webhook
    """
    if not staging_layer:
        raise HTTPException(status_code=503, detail="Staging layer not initialized")

    logger.info("zapier_review_received",
               item_id=request.item_id,
               status=request.review_status)

    try:
        # Get item from staging
        pending = staging_layer.get_pending(limit=1000)  # Get all to find specific one
        item = next((i for i in pending if i['id'] == request.item_id), None)

        if not item:
            raise HTTPException(status_code=404, detail=f"Item {request.item_id} not found in staging")

        action_taken = "none"

        # Handle review status
        if request.review_status == "approved" and request.confidence_score >= 0.7:
            # High confidence approval → auto-approve
            staging_layer.approve([request.item_id])
            action_taken = "auto_approved"
            logger.info("zapier_item_auto_approved",
                       item_id=request.item_id,
                       confidence=request.confidence_score)

        elif request.review_status == "rejected":
            # Rejected → mark as rejected
            reason = request.llm_feedback or "LLM review failed"
            staging_layer.reject([request.item_id], reason=reason)
            action_taken = "rejected"
            logger.info("zapier_item_rejected",
                       item_id=request.item_id,
                       reason=reason[:100])

        elif request.review_status == "needs_human_review" or request.confidence_score < 0.7:
            # Low confidence → keep in pending
            action_taken = "flagged_for_human_review"
            logger.info("zapier_item_flagged",
                       item_id=request.item_id,
                       confidence=request.confidence_score)

        else:
            action_taken = "kept_pending"

        return ZapierReviewResponse(
            status="success",
            item_id=request.item_id,
            action_taken=action_taken,
            message=f"Review processed: {action_taken}"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("zapier_review_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Review processing failed: {str(e)}")


@router.post("/approve", response_model=ZapierApproveResponse)
async def zapier_approve_webhook(request: ZapierApproveRequest):
    """
    Webhook for manual approval of staged content

    Workflow:
    1. Receive approval from Zapier (manual trigger or automated)
    2. Approve items in staging
    3. Optionally ingest to vector database
    4. Return approval results

    Example Zapier flow:
    - Trigger: Button click in Notion
    - Action: Send approval to this webhook
    """
    if not staging_layer:
        raise HTTPException(status_code=503, detail="Staging layer not initialized")

    logger.info("zapier_approve_received",
               count=len(request.item_ids),
               user=request.user)

    try:
        # Approve items
        approved_count = staging_layer.approve(request.item_ids)

        # TODO: Ingest to vector database if requested
        # For now, just approve in staging

        if approved_count == 0:
            raise HTTPException(status_code=404, detail="No items found to approve")

        logger.info("zapier_items_approved",
                   count=approved_count,
                   user=request.user)

        return ZapierApproveResponse(
            status="success",
            approved_count=approved_count,
            failed_count=len(request.item_ids) - approved_count,
            message=f"Approved {approved_count} items"
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("zapier_approve_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Approval failed: {str(e)}")


@router.post("/status", response_model=ZapierStatusResponse)
async def zapier_status_query(request: ZapierStatusRequest):
    """
    Query status of staged items

    Useful for:
    - Checking pending items
    - Monitoring approved items
    - Tracking rejected items

    Example Zapier flow:
    - Trigger: Schedule (daily)
    - Action: Query status
    - Action: Send notification if items pending
    """
    if not staging_layer:
        raise HTTPException(status_code=503, detail="Staging layer not initialized")

    logger.info("zapier_status_query",
               item_id=request.item_id,
               filter=request.status_filter)

    try:
        # Get items based on filter
        if request.item_id:
            # Get specific item
            pending = staging_layer.get_pending(limit=1000)
            items = [i for i in pending if i['id'] == request.item_id]

        elif request.status_filter == "approved":
            items = staging_layer.get_approved()[:request.limit]

        elif request.status_filter == "pending":
            items = staging_layer.get_pending(limit=request.limit)

        else:
            # Get all pending by default
            items = staging_layer.get_pending(limit=request.limit)

        # Calculate summary
        summary = {
            "total": len(items),
            "pending": len([i for i in items if i.get('status') == 'pending']),
            "approved": len([i for i in items if i.get('status') == 'approved']),
            "rejected": len([i for i in items if i.get('status') == 'rejected'])
        }

        logger.info("zapier_status_query_complete", count=len(items))

        return ZapierStatusResponse(
            items=items,
            count=len(items),
            summary=summary
        )

    except Exception as e:
        logger.error("zapier_status_error", error=str(e))
        raise HTTPException(status_code=500, detail=f"Status query failed: {str(e)}")


@router.get("/webhook-test")
async def zapier_webhook_test():
    """
    Test endpoint for Zapier webhook setup

    Use this to verify your Zapier webhook configuration
    Returns a simple success message
    """
    return {
        "status": "success",
        "message": "Zapier webhook is working!",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "ontology": ontology is not None,
            "notion": notion_client is not None,
            "staging": staging_layer is not None
        }
    }


# Export router and initializer
__all__ = ["router", "initialize_zapier_services"]
