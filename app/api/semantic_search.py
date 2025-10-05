"""
Semantic Search API Endpoints

Provides REST API for vector similarity search:
- Search similar meals, workouts, activities
- Get personalized context for AI recommendations
- Pattern detection across fitness journey
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.services.semantic_search_service import get_semantic_search_service, SemanticSearchService
from app.api.dependencies import get_current_user

router = APIRouter(prefix="/semantic-search", tags=["Semantic Search"])


# Request/Response Models
class SemanticSearchRequest(BaseModel):
    query: str = Field(..., description="Natural language search query")
    source_type: Optional[str] = Field(None, description="Filter by type: meal, workout, activity, etc.")
    limit: int = Field(10, ge=1, le=50, description="Max results to return")
    recency_weight: float = Field(0.3, ge=0.0, le=1.0, description="Weight for recency (0=ignore, 1=only recent)")
    similarity_threshold: float = Field(0.5, ge=0.0, le=1.0, description="Minimum similarity score")


class SemanticSearchResult(BaseModel):
    id: str
    source_type: str
    source_id: str
    content_text: str
    metadata: Dict[str, Any]
    similarity: float
    recency_score: float
    final_score: float
    created_at: str


class ContextBundleResponse(BaseModel):
    similar_entries: List[Dict[str, Any]]
    recent_meals: List[Dict[str, Any]]
    recent_workouts: List[Dict[str, Any]]
    recent_activities: List[Dict[str, Any]]
    summary: str


# Endpoints
@router.post("/search", response_model=List[SemanticSearchResult])
async def semantic_search(
    request: SemanticSearchRequest,
    current_user: dict = Depends(get_current_user),
    search_service: SemanticSearchService = Depends(get_semantic_search_service)
):
    """
    Search for entries similar to query using vector similarity.

    Example queries:
    - "high protein chicken meals"
    - "chest and triceps workouts"
    - "5 mile runs"
    """
    try:
        results = await search_service.search_similar_entries(
            user_id=current_user["id"],
            query_text=request.query,
            source_type=request.source_type,
            limit=request.limit,
            recency_weight=request.recency_weight,
            similarity_threshold=request.similarity_threshold
        )

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/similar-meals", response_model=List[Dict[str, Any]])
async def find_similar_meals(
    query: str,
    limit: int = 5,
    current_user: dict = Depends(get_current_user),
    search_service: SemanticSearchService = Depends(get_semantic_search_service)
):
    """
    Find meals similar to query.

    Example: /similar-meals?query=chicken and rice
    """
    try:
        results = await search_service.find_similar_meals(
            user_id=current_user["id"],
            meal_description=query,
            limit=limit
        )

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/similar-workouts", response_model=List[Dict[str, Any]])
async def find_similar_workouts(
    query: str,
    limit: int = 5,
    current_user: dict = Depends(get_current_user),
    search_service: SemanticSearchService = Depends(get_semantic_search_service)
):
    """
    Find workouts similar to query.

    Example: /similar-workouts?query=upper body push day
    """
    try:
        results = await search_service.find_similar_workouts(
            user_id=current_user["id"],
            workout_description=query,
            limit=limit
        )

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.get("/similar-activities", response_model=List[Dict[str, Any]])
async def find_similar_activities(
    query: str,
    limit: int = 5,
    current_user: dict = Depends(get_current_user),
    search_service: SemanticSearchService = Depends(get_semantic_search_service)
):
    """
    Find activities similar to query.

    Example: /similar-activities?query=morning run
    """
    try:
        results = await search_service.find_similar_activities(
            user_id=current_user["id"],
            activity_description=query,
            limit=limit
        )

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@router.post("/context-bundle", response_model=ContextBundleResponse)
async def get_context_bundle(
    entry_text: str,
    entry_type: str,
    current_user: dict = Depends(get_current_user),
    search_service: SemanticSearchService = Depends(get_semantic_search_service)
):
    """
    Get comprehensive context bundle for AI recommendations.

    Returns similar entries + recent meals, workouts, activities.
    """
    try:
        context = await search_service.get_personalized_context_bundle(
            user_id=current_user["id"],
            current_entry_text=entry_text,
            current_entry_type=entry_type
        )

        return context

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Context retrieval failed: {str(e)}")


@router.get("/context-for-recommendation")
async def get_context_for_recommendation(
    context_query: str,
    max_entries: int = 5,
    current_user: dict = Depends(get_current_user),
    search_service: SemanticSearchService = Depends(get_semantic_search_service)
):
    """
    Get formatted context string for AI coach.

    Example: /context-for-recommendation?context_query=recent high protein meals
    """
    try:
        context_str = await search_service.get_context_for_recommendation(
            user_id=current_user["id"],
            context_query=context_query,
            max_entries=max_entries
        )

        return {"context": context_str}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Context retrieval failed: {str(e)}")


@router.get("/recent/{source_type}", response_model=List[Dict[str, Any]])
async def get_recent_entries(
    source_type: str,
    days: int = 7,
    limit: int = 10,
    current_user: dict = Depends(get_current_user),
    search_service: SemanticSearchService = Depends(get_semantic_search_service)
):
    """
    Get recent entries of a specific type (no semantic search).

    Example: /recent/meal?days=3&limit=5
    """
    try:
        results = await search_service.get_recent_entries_by_type(
            user_id=current_user["id"],
            source_type=source_type,
            days=days,
            limit=limit
        )

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Retrieval failed: {str(e)}")
