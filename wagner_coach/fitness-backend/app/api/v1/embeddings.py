"""
Embedding API Endpoints
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import List, Optional

from app.api.middleware.auth import get_current_user, verify_webhook_secret
from app.services.embedding_service import EmbeddingService


router = APIRouter()


class GenerateEmbeddingRequest(BaseModel):
    """Request to generate embedding."""
    content: str
    content_type: str
    content_id: str


class SearchRequest(BaseModel):
    """Request to search embeddings."""
    query: str
    limit: Optional[int] = 5
    threshold: Optional[float] = 0.7


@router.post("/generate")
async def generate_embedding(
    request: GenerateEmbeddingRequest,
    user_id: str = Depends(get_current_user)
):
    """Generate and store embedding for content."""
    service = EmbeddingService()

    embedding_id = await service.generate_and_store(
        user_id=user_id,
        content=request.content,
        content_type=request.content_type,
        content_id=request.content_id
    )

    return {
        "success": True,
        "embedding_id": embedding_id,
        "message": "Embedding generated successfully"
    }


@router.post("/search")
async def search_embeddings(
    request: SearchRequest,
    user_id: str = Depends(get_current_user)
):
    """Search for similar content."""
    service = EmbeddingService()

    results = await service.search_similar(
        query=request.query,
        user_id=user_id,
        limit=request.limit,
        threshold=request.threshold
    )

    return {
        "success": True,
        "results": results,
        "count": len(results)
    }


@router.post("/process-queue")
async def process_queue(_: None = Depends(verify_webhook_secret)):
    """Process embedding queue (webhook endpoint)."""
    service = EmbeddingService()
    result = await service.process_queue(limit=100)

    return {
        "success": True,
        "message": "Queue processing complete",
        "results": result
    }
