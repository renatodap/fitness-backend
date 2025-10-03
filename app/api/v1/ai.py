"""
AI Context API Endpoints
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.middleware.auth import get_current_user
from app.services.rag_service import RAGService

router = APIRouter()


class ContextRequest(BaseModel):
    """Request for user context."""
    query: str
    include_history: bool = True


@router.post("/context")
async def get_context(
    request: ContextRequest,
    user_id: str = Depends(get_current_user)
):
    """Get comprehensive user context for AI coaching."""
    service = RAGService()

    context = await service.get_user_context(
        user_id=user_id,
        query=request.query,
        include_history=request.include_history
    )

    return {
        "success": True,
        "context": context
    }


@router.post("/prompt-context")
async def get_prompt_context(
    request: ContextRequest,
    user_id: str = Depends(get_current_user)
):
    """Get formatted prompt context string."""
    service = RAGService()

    context_str = await service.build_prompt_context(
        user_id=user_id,
        query=request.query
    )

    return {
        "success": True,
        "context": context_str
    }
