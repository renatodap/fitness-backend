"""
Nutrition API Endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.api.middleware.auth import get_current_user
from app.services.meal_parser_service import MealParserService

router = APIRouter()


class ParseMealRequest(BaseModel):
    """Request to parse meal description."""
    description: Optional[str] = None
    text: Optional[str] = None  # Alternative field name for compatibility
    user_id: Optional[str] = None  # Optional user_id override


@router.post("/parse")
async def parse_meal(
    request: ParseMealRequest,
    user_id: str = Depends(get_current_user)
):
    """Parse natural language meal description."""
    service = MealParserService()

    result = await service.parse(
        description=request.description,
        user_id=user_id
    )

    return {
        "success": True,
        "meal": result.model_dump()
    }


@router.post("/meal/parse")
async def parse_meal_alt(
    request: ParseMealRequest,
    user_id: str = Depends(get_current_user)
):
    """Parse natural language meal description (alternative endpoint for compatibility)."""
    # Support both 'description' and 'text' field names
    description = request.description or request.text
    if not description:
        raise HTTPException(status_code=400, detail="description or text field is required")

    # Use user_id from request body if provided, otherwise use authenticated user
    target_user_id = request.user_id or user_id

    service = MealParserService()

    result = await service.parse(
        description=description,
        user_id=target_user_id
    )

    return {
        "success": True,
        "meal": result.model_dump()
    }
