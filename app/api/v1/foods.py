"""
Foods API Endpoints

Handles food search, recent foods, and food database queries.
"""

import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.api.middleware.auth import get_current_user
from app.services.food_search_service import get_food_search_service
from app.api.v1.schemas.food_matching_schemas import (
    MatchDetectedFoodsRequest,
    MatchDetectedFoodsResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/foods", tags=["foods"])


# Response Models
class FoodNutrition(BaseModel):
    """Nutrition information for a food."""
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = Field(None, alias="total_carbs_g")
    fat_g: Optional[float] = Field(None, alias="total_fat_g")
    fiber_g: Optional[float] = Field(None, alias="dietary_fiber_g")
    sugar_g: Optional[float] = Field(None, alias="total_sugars_g")
    sodium_mg: Optional[float] = None

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


class FoodSearchResult(BaseModel):
    """Search result for a food item or meal template."""
    id: str
    name: str
    brand_name: Optional[str] = None
    food_group: Optional[str] = None
    serving_size: float
    serving_unit: str
    calories: Optional[float] = None
    protein_g: Optional[float] = None
    carbs_g: Optional[float] = Field(None, alias="total_carbs_g")
    fat_g: Optional[float] = Field(None, alias="total_fat_g")
    fiber_g: Optional[float] = Field(None, alias="dietary_fiber_g")
    sugar_g: Optional[float] = Field(None, alias="total_sugars_g")
    sodium_mg: Optional[float] = None
    is_recent: bool = False
    is_generic: Optional[bool] = None
    is_branded: Optional[bool] = None
    data_quality_score: Optional[float] = None
    last_quantity: Optional[float] = None
    last_unit: Optional[str] = None
    last_logged_at: Optional[str] = None
    log_count: Optional[int] = None

    # Template-specific fields (NEW)
    is_template: bool = False
    is_user_template: Optional[bool] = None
    is_restaurant: Optional[bool] = None
    is_community: Optional[bool] = None
    template_category: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[list[str]] = None
    is_favorite: Optional[bool] = None
    use_count: Optional[int] = None
    popularity_score: Optional[int] = None

    class Config:
        populate_by_name = True
        allow_population_by_field_name = True


class FoodSearchResponse(BaseModel):
    """Response for food search."""
    foods: list[FoodSearchResult]
    total: int
    limit: int
    query: str


class RecentFoodsResponse(BaseModel):
    """Response for recent foods."""
    foods: list[FoodSearchResult]


@router.get(
    "/search",
    response_model=FoodSearchResponse,
    summary="Search foods and meal templates",
    description="""
    Search food database AND meal templates with intelligent ranking.

    Features:
    - Fast autocomplete with partial matching
    - Searches both individual foods AND meal templates
    - Prioritizes user's recent foods
    - Includes user's private meal templates
    - Includes public templates (restaurant meals, community meals)
    - Ranks by popularity and quality
    - Case-insensitive search

    **Template types:**
    - 🕐 Recent foods (recently logged)
    - 💾 Your meal templates (saved meals)
    - 🍽️ Restaurant meals (Chipotle, Subway, etc.)
    - 👥 Community templates (shared meals)
    - 🥗 Individual foods (database)

    **Example queries:**
    - "chicken" → Shows chicken foods + templates containing chicken
    - "chipotle" → Shows Chipotle restaurant templates
    - "protein shake" → Shows protein shake templates + whey protein
    - "banana" → Shows banana food + smoothie templates
    """,
    responses={
        200: {"description": "Search results (foods + templates)"},
        400: {"description": "Invalid query"},
        500: {"description": "Search failed"}
    }
)
async def search_foods(
    q: str = Query(..., min_length=1, max_length=100, description="Search query"),
    limit: int = Query(20, ge=1, le=100, description="Maximum results"),
    include_recent: bool = Query(True, description="Include user's recent foods"),
    include_templates: bool = Query(True, description="Include meal templates"),
    current_user: dict = Depends(get_current_user)
):
    """
    Search foods AND meal templates with autocomplete and smart ranking.

    Args:
        q: Search query string (required)
        limit: Maximum number of results (default: 20)
        include_recent: Include user's recently logged foods (default: true)
        include_templates: Include meal templates - user, restaurant, community (default: true)
        current_user: Authenticated user from JWT

    Returns:
        FoodSearchResponse with matching foods AND templates (mixed in same list)
    """
    try:
        logger.info(f"Unified search request: query='{q}', user_id={current_user['user_id']}, include_templates={include_templates}")

        # Get search service
        search_service = get_food_search_service()

        # Search foods + templates
        result = await search_service.search_foods(
            query=q,
            user_id=current_user["user_id"],
            limit=limit,
            include_recent=include_recent,
            include_templates=include_templates
        )

        # Convert to response model
        return FoodSearchResponse(**result)

    except Exception as e:
        logger.error(f"Unified search failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Search failed. Please try again."
        )


@router.get(
    "/recent",
    response_model=RecentFoodsResponse,
    summary="Get recent foods",
    description="""
    Get user's recently logged foods for quick access.

    Returns foods sorted by:
    - Frequency (most logged first)
    - Recency (most recent first)

    Includes last logged quantity and unit for convenience.
    """,
    responses={
        200: {"description": "Recent foods"},
        500: {"description": "Failed to retrieve recent foods"}
    }
)
async def get_recent_foods(
    limit: int = Query(20, ge=1, le=50, description="Maximum results"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's recently logged foods.

    Args:
        limit: Maximum number of foods to return (default: 20)
        current_user: Authenticated user from JWT

    Returns:
        RecentFoodsResponse with recent foods
    """
    try:
        logger.info(f"Recent foods request: user_id={current_user['user_id']}, limit={limit}")

        # Get search service
        search_service = get_food_search_service()

        # Get recent foods
        result = await search_service.get_recent_foods(
            user_id=current_user["user_id"],
            limit=limit
        )

        # Convert to response model
        return RecentFoodsResponse(**result)

    except Exception as e:
        logger.error(f"Get recent foods failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve recent foods. Please try again."
        )


@router.post(
    "/match-detected",
    response_model=MatchDetectedFoodsResponse,
    summary="Match detected foods to database",
    description="""
    Match food names detected from image analysis to database foods with full nutrition.

    This endpoint:
    - Searches database for matching food records
    - Uses fuzzy matching for better results
    - Prioritizes user's recent foods
    - Detects cooking methods (grilled, fried, raw, etc.)
    - Returns full nutrition data for matched foods
    - Preserves detected quantities and units

    **Use case:** Convert AI-detected food names to database records for meal logging.

    **Example request:**
    ```json
    {
      "detected_foods": [
        {"name": "grilled chicken", "quantity": "150", "unit": "g"},
        {"name": "brown rice", "quantity": "1", "unit": "cup"}
      ]
    }
    ```
    """,
    responses={
        200: {"description": "Foods successfully matched"},
        400: {"description": "Invalid request"},
        500: {"description": "Matching failed"}
    }
)
async def match_detected_foods(
    request: MatchDetectedFoodsRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Match detected food names to database records.

    Args:
        request: List of detected foods with names, quantities, and units
        current_user: Authenticated user from JWT

    Returns:
        MatchDetectedFoodsResponse with matched/unmatched foods
    """
    try:
        logger.info(
            f"Food matching request: user_id={current_user['user_id']}, "
            f"foods_count={len(request.detected_foods)}"
        )

        # Get search service
        search_service = get_food_search_service()

        # Convert Pydantic models to dicts
        detected_foods_dicts = [food.model_dump() for food in request.detected_foods]

        # Match foods
        result = await search_service.match_detected_foods(
            detected_foods=detected_foods_dicts,
            user_id=current_user["user_id"]
        )

        logger.info(
            f"Food matching complete: matched={result['total_matched']}/{result['total_detected']}, "
            f"rate={result['match_rate']:.2f}"
        )

        # Convert to response model
        return MatchDetectedFoodsResponse(**result)

    except Exception as e:
        logger.error(f"Food matching failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to match foods. Please try again."
        )


@router.get(
    "/{food_id}",
    response_model=FoodSearchResult,
    summary="Get food by ID",
    description="Get detailed information about a specific food.",
    responses={
        200: {"description": "Food details"},
        404: {"description": "Food not found"},
        500: {"description": "Server error"}
    }
)
async def get_food_by_id(
    food_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get food by ID.

    Args:
        food_id: Food UUID
        current_user: Authenticated user from JWT

    Returns:
        Food details
    """
    try:
        logger.info(f"Get food by ID: food_id={food_id}, user_id={current_user['user_id']}")

        # Get search service
        search_service = get_food_search_service()

        # Query food by ID
        response = search_service.supabase.table("foods_enhanced") \
            .select("id, name, brand_name, food_group, serving_size, serving_unit, calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, total_sugars_g, sodium_mg, is_generic, is_branded, data_quality_score") \
            .eq("id", food_id) \
            .limit(1) \
            .execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Food with ID '{food_id}' not found"
            )

        food_data = response.data[0]
        food_data["is_recent"] = False  # Not from recent foods query

        return FoodSearchResult(**food_data)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Get food by ID failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve food. Please try again."
        )
