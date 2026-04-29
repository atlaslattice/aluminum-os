#!/usr/bin/env python3
"""
Sheldonbrain RAG API Server
FastAPI REST API for querying and managing the knowledge base

Features:
- Query knowledge base with Vault security
- Ingest new documents with staging
- Health checks and system stats
- Integration endpoints for Notion, Zapier, OpenAI Assistants
- Rate limiting and authentication
- CORS support for web clients
"""

import os
import json
import time
from typing import List, Dict, Any, Optional
from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, HTTPException, Depends, Header, Request, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from dotenv import load_dotenv

# Sheldonbrain imports
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from src.vault.vault_security import VaultManager, VaultAccessLevel, VaultSecurityError
from src.vault.vault_integration import query_with_vault_awareness, process_with_vault_classification
from langchain_core.documents import Document
from langchain_community.vectorstores import Qdrant as LangchainQdrant
from langchain_huggingface import HuggingFaceEmbeddings
from qdrant_client import QdrantClient
import structlog

# Import Zapier webhooks router
try:
    from .zapier_webhooks import router as zapier_router, initialize_zapier_services
except ImportError:
    from zapier_webhooks import router as zapier_router, initialize_zapier_services

# Import ingestion scheduler
try:
    from ingestion.scheduler import create_default_scheduler
except ImportError:
    create_default_scheduler = None

# Load environment
load_dotenv()

# Configure logging
structlog.configure(processors=[structlog.processors.JSONRenderer()])
logger = structlog.get_logger()

# Initialize FastAPI app
app = FastAPI(
    title="Sheldonbrain RAG API",
    description="REST API for the Sheldonbrain RAG knowledge system",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Include Zapier webhooks router
app.include_router(zapier_router)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
vault_manager: Optional[VaultManager] = None
main_vectorstore: Optional[LangchainQdrant] = None
embedding_model: Optional[HuggingFaceEmbeddings] = None
ingestion_scheduler = None  # Will be initialized on startup if enabled

# API Key authentication
API_KEY = os.getenv("SHELDONBRAIN_API_KEY", "dev-api-key-change-in-production")


# Pydantic models
class QueryRequest(BaseModel):
    query: str = Field(..., description="Search query")
    user: str = Field(default="api_user", description="User making the request")
    destination: str = Field(default="internal", description="Where results will be used (internal, notion, zapier, etc.)")
    include_vault: Optional[bool] = Field(default=None, description="Override Vault inclusion policy")
    limit: int = Field(default=5, ge=1, le=20, description="Maximum results to return")


class QueryResponse(BaseModel):
    query: str
    results: List[Dict[str, Any]]
    count: int
    vault_used: bool
    timestamp: str


class IngestRequest(BaseModel):
    documents: List[Dict[str, Any]] = Field(..., description="Documents to ingest")
    user: str = Field(default="api_user", description="User ingesting data")
    require_approval: bool = Field(default=True, description="Require approval for Vault documents")


class IngestResponse(BaseModel):
    status: str
    main_count: int
    vault_count: int
    vault_status: Optional[str] = None
    message: str


class HealthResponse(BaseModel):
    status: str
    timestamp: str
    version: str
    services: Dict[str, str]


class StatsResponse(BaseModel):
    main_db: Dict[str, Any]
    vault_db: Dict[str, Any]
    timestamp: str


# Authentication dependency
async def verify_api_key(x_api_key: str = Header(...)):
    """Verify API key from request header"""
    if x_api_key != API_KEY:
        logger.warning("unauthorized_api_access", api_key=x_api_key[:8] + "***")
        raise HTTPException(status_code=401, detail="Invalid API key")
    return x_api_key


# Rate limiting (simple in-memory implementation)
class RateLimiter:
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests = {}

    def check_rate_limit(self, client_id: str) -> bool:
        """Check if client has exceeded rate limit"""
        now = time.time()
        minute_ago = now - 60

        # Clean old requests
        if client_id in self.requests:
            self.requests[client_id] = [
                req_time for req_time in self.requests[client_id]
                if req_time > minute_ago
            ]

        # Check limit
        if client_id not in self.requests:
            self.requests[client_id] = []

        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False

        # Add request
        self.requests[client_id].append(now)
        return True


rate_limiter = RateLimiter(requests_per_minute=60)


# Lazy initialization helper
def initialize_services():
    """Lazy initialize services on first use"""
    global vault_manager, main_vectorstore, embedding_model

    if vault_manager is not None:
        return  # Already initialized

    logger.info("lazy_initializing_services")

    # Initialize Vault Manager
    vault_manager = VaultManager(
        vault_path="./data/qdrant_db_vault",
        main_path="./data/qdrant_db"
    )

    # Initialize embeddings
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # Initialize main vectorstore
    try:
        main_vectorstore = LangchainQdrant(
            client=vault_manager.main_client,
            collection_name="grokbrain_grid",
            embeddings=embedding_model
        )
        logger.info("services_initialized")
    except Exception as e:
        logger.error("vectorstore_init_error", error=str(e))
        main_vectorstore = None


# Startup/shutdown events
@app.on_event("startup")
async def startup_event():
    """Fast startup - services initialized lazily on first request"""
    global ingestion_scheduler

    logger.info("api_server_starting")

    # Initialize Zapier webhook services (lightweight)
    initialize_zapier_services()

    # Initialize ingestion scheduler if enabled
    if os.getenv("ENABLE_SCHEDULED_INGESTION", "false").lower() == "true":
        if create_default_scheduler:
            try:
                ingestion_scheduler = create_default_scheduler()
                ingestion_scheduler.start()
                logger.info("ingestion_scheduler_started",
                           jobs=len(ingestion_scheduler.list_jobs()))
            except Exception as e:
                logger.error("ingestion_scheduler_failed", error=str(e))
        else:
            logger.warning("scheduler_module_not_available")

    logger.info("api_server_ready")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    global ingestion_scheduler

    logger.info("api_server_shutting_down")

    # Stop scheduler
    if ingestion_scheduler:
        try:
            ingestion_scheduler.stop()
            logger.info("ingestion_scheduler_stopped")
        except Exception as e:
            logger.error("scheduler_shutdown_error", error=str(e))


# Middleware for rate limiting
@app.middleware("http")
async def rate_limit_middleware(request: Request, call_next):
    """Apply rate limiting to all requests"""
    client_id = request.client.host

    if not rate_limiter.check_rate_limit(client_id):
        logger.warning("rate_limit_exceeded", client=client_id)
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Try again later."}
        )

    response = await call_next(request)
    return response


# Health check endpoint
@app.get("/health", response_model=HealthResponse, tags=["System"])
async def health_check():
    """
    Health check endpoint
    Returns system status and service availability
    """
    services = {
        "vault_manager": "ok" if vault_manager else "unavailable",
        "main_vectorstore": "ok" if main_vectorstore else "unavailable",
        "embedding_model": "ok" if embedding_model else "unavailable"
    }

    return HealthResponse(
        status="healthy" if all(s == "ok" for s in services.values()) else "degraded",
        timestamp=datetime.now().isoformat(),
        version="1.0.0",
        services=services
    )


# Stats endpoint
@app.get("/stats", response_model=StatsResponse, tags=["System"])
async def get_stats(api_key: str = Depends(verify_api_key)):
    """
    Get system statistics
    Requires authentication
    """
    initialize_services()

    if not vault_manager:
        raise HTTPException(status_code=503, detail="Vault manager not initialized")

    # Get Vault stats
    vault_stats = vault_manager.get_vault_stats()

    # Get main DB stats
    main_stats = {}
    if main_vectorstore:
        try:
            client = main_vectorstore.client
            collection_info = client.get_collection("grokbrain_grid")
            main_stats = {
                "total_documents": collection_info.points_count,
                "collection_name": "grokbrain_grid",
                "status": "active"
            }
        except Exception as e:
            main_stats = {"status": "error", "error": str(e)}
    else:
        main_stats = {"status": "unavailable"}

    return StatsResponse(
        main_db=main_stats,
        vault_db=vault_stats,
        timestamp=datetime.now().isoformat()
    )


# Query endpoint
@app.post("/query", response_model=QueryResponse, tags=["Knowledge Base"])
async def query_knowledge_base(
    request: QueryRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Query the knowledge base

    Respects Vault security policies based on destination:
    - internal: Can include Vault data (with PII filtering)
    - notion/zapier/external: Vault data excluded

    Requires authentication via X-API-Key header
    """
    initialize_services()

    if not vault_manager or not main_vectorstore:
        raise HTTPException(status_code=503, detail="Services not initialized")

    logger.info("api_query_received",
               query=request.query,
               user=request.user,
               destination=request.destination)

    try:
        # Query with Vault awareness
        results = query_with_vault_awareness(
            query=request.query,
            vault_manager=vault_manager,
            main_vectorstore=main_vectorstore,
            user=request.user,
            destination=request.destination,
            include_vault=request.include_vault
        )

        # Limit results
        results = results[:request.limit]

        # Check if Vault was used
        vault_used = any(r.get("vault_protected") for r in results)

        logger.info("api_query_completed",
                   user=request.user,
                   results_count=len(results),
                   vault_used=vault_used)

        return QueryResponse(
            query=request.query,
            results=results,
            count=len(results),
            vault_used=vault_used,
            timestamp=datetime.now().isoformat()
        )

    except VaultSecurityError as e:
        logger.error("vault_security_error", error=str(e), user=request.user)
        raise HTTPException(status_code=403, detail=str(e))

    except Exception as e:
        logger.error("query_error", error=str(e), user=request.user)
        raise HTTPException(status_code=500, detail=f"Query failed: {str(e)}")


# Ingest endpoint
@app.post("/ingest", response_model=IngestResponse, tags=["Knowledge Base"])
async def ingest_documents(
    request: IngestRequest,
    background_tasks: BackgroundTasks,
    api_key: str = Depends(verify_api_key)
):
    """
    Ingest new documents into the knowledge base

    Documents are automatically classified:
    - Vault data: Queued for manual approval
    - Main data: Added immediately

    Requires authentication via X-API-Key header
    """
    initialize_services()

    if not vault_manager:
        raise HTTPException(status_code=503, detail="Vault manager not initialized")

    logger.info("api_ingest_received",
               user=request.user,
               document_count=len(request.documents))

    try:
        # Convert to artifacts format
        artifacts = []
        for doc_data in request.documents:
            artifacts.append({
                "input": doc_data.get("input", ""),
                "output": doc_data.get("output", ""),
                "timestamp": doc_data.get("timestamp", datetime.now().isoformat()),
                "source_file": doc_data.get("source", "api_upload")
            })

        # Classify and route
        classification_result = process_with_vault_classification(
            artifacts=artifacts,
            vault_manager=vault_manager,
            user=request.user
        )

        # TODO: Process main documents through ingestion pipeline in background
        # For now, we just classify and queue

        logger.info("api_ingest_completed",
                   user=request.user,
                   main_count=classification_result["main_count"],
                   vault_count=classification_result["vault_count"])

        return IngestResponse(
            status="success",
            main_count=classification_result["main_count"],
            vault_count=classification_result["vault_count"],
            vault_status=classification_result["vault_result"]["status"] if classification_result["vault_result"] else None,
            message=f"Classified {classification_result['main_count']} main documents, {classification_result['vault_count']} queued for Vault approval"
        )

    except Exception as e:
        logger.error("ingest_error", error=str(e), user=request.user)
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")


# Notion integration endpoint
@app.post("/integrations/notion/query", tags=["Integrations"])
async def notion_query(
    request: QueryRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Query endpoint specifically for Notion integration

    Automatically sets destination to 'notion' and excludes Vault data
    Formats response for Notion consumption
    """
    # Override destination
    request.destination = "notion"
    request.include_vault = False

    result = await query_knowledge_base(request, api_key)

    # Format for Notion
    notion_formatted = {
        "blocks": [
            {
                "type": "paragraph",
                "text": f"Query: {result.query}"
            },
            {
                "type": "heading_2",
                "text": f"Found {result.count} results"
            }
        ]
    }

    for idx, res in enumerate(result.results[:3], 1):
        notion_formatted["blocks"].append({
            "type": "paragraph",
            "text": f"{idx}. {res['content'][:200]}..."
        })

    return notion_formatted


# Zapier integration endpoint
@app.post("/integrations/zapier/query", tags=["Integrations"])
async def zapier_query(
    request: QueryRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Query endpoint specifically for Zapier integration

    Automatically sets destination to 'zapier' and excludes Vault data
    Returns simplified format for Zapier
    """
    # Override destination
    request.destination = "zapier"
    request.include_vault = False

    result = await query_knowledge_base(request, api_key)

    # Simplified format for Zapier
    return {
        "query": result.query,
        "top_result": result.results[0]["content"] if result.results else "No results found",
        "all_results": [r["content"][:500] for r in result.results],
        "count": result.count
    }


# OpenAI Assistant integration endpoint
@app.post("/integrations/openai/query", tags=["Integrations"])
async def openai_assistant_query(
    request: QueryRequest,
    api_key: str = Depends(verify_api_key)
):
    """
    Query endpoint for OpenAI Assistants API integration

    Returns structured data suitable for OpenAI function calling
    Excludes Vault data by default
    """
    # Override destination
    request.destination = "openai_assistant"
    request.include_vault = False

    result = await query_knowledge_base(request, api_key)

    # Format for OpenAI function response
    return {
        "answer": result.results[0]["content"] if result.results else "No relevant information found",
        "sources": [
            {
                "content": r["content"],
                "score": r["score"],
                "metadata": r.get("metadata", {})
            }
            for r in result.results
        ],
        "confidence": result.results[0]["score"] if result.results else 0.0
    }


# Vault management endpoints (admin only)
@app.get("/vault/pending", tags=["Vault Management"])
async def get_vault_pending(api_key: str = Depends(verify_api_key)):
    """Get pending Vault additions"""
    initialize_services()

    pending_file = "./logs/vault_pending_additions.json"

    if not Path(pending_file).exists():
        return {"pending": [], "count": 0}

    with open(pending_file, 'r') as f:
        pending = json.load(f)

    return {"pending": pending, "count": len(pending)}


@app.post("/vault/approve", tags=["Vault Management"])
async def approve_vault_additions(
    document_ids: List[str],
    user: str = "admin",
    api_key: str = Depends(verify_api_key)
):
    """Approve pending Vault additions"""
    initialize_services()

    if not vault_manager:
        raise HTTPException(status_code=503, detail="Vault manager not initialized")

    result = vault_manager.approve_pending_additions(document_ids, user=user)

    return result


# Scheduler management endpoints
@app.get("/scheduler/status", tags=["Scheduler"])
async def get_scheduler_status(api_key: str = Depends(verify_api_key)):
    """
    Get ingestion scheduler status

    Returns information about scheduled jobs and execution statistics
    """
    if not ingestion_scheduler:
        return {
            "status": "disabled",
            "message": "Scheduler not enabled. Set ENABLE_SCHEDULED_INGESTION=true"
        }

    return ingestion_scheduler.get_stats()


@app.get("/scheduler/jobs", tags=["Scheduler"])
async def list_scheduler_jobs(api_key: str = Depends(verify_api_key)):
    """List all scheduled jobs"""
    if not ingestion_scheduler:
        raise HTTPException(status_code=503, detail="Scheduler not enabled")

    jobs = ingestion_scheduler.list_jobs()
    return {"jobs": jobs, "count": len(jobs)}


@app.post("/scheduler/trigger/{job_name}", tags=["Scheduler"])
async def trigger_job_manual(
    job_name: str,
    api_key: str = Depends(verify_api_key)
):
    """
    Manually trigger a scheduled job to run immediately

    Args:
        job_name: Name of the job to trigger (e.g., "arxiv_daily")
    """
    if not ingestion_scheduler:
        raise HTTPException(status_code=503, detail="Scheduler not enabled")

    try:
        ingestion_scheduler.trigger_job_manual(job_name)
        return {
            "status": "triggered",
            "job": job_name,
            "message": f"Job '{job_name}' will run shortly"
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to trigger job: {str(e)}")


# Root endpoint
@app.get("/", tags=["System"])
async def root():
    """API root - provides basic information"""
    return {
        "name": "Sheldonbrain RAG API",
        "version": "1.0.0",
        "status": "running",
        "docs": "/docs",
        "health": "/health"
    }


# Run server
if __name__ == "__main__":
    import uvicorn

    # Cloud Run uses PORT env var, fallback to API_PORT for local development
    port = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
    host = os.getenv("API_HOST", "0.0.0.0")

    logger.info("starting_api_server", host=host, port=port)

    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=True,  # Disable in production
        log_level="info"
    )
