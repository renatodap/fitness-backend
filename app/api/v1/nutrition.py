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


@router.get("/summary/today")
async def get_nutrition_summary_today(
    current_user: dict = Depends(get_current_user)
):
    """Get nutrition summary for today with targets and current consumption."""
    from app.services.supabase_service import get_service_client
    from datetime import datetime, date
    
    supabase = get_service_client()
    user_id = current_user.get("user_id") or current_user.get("id")
    
    try:
        # Get user's nutrition targets from users table
        user_response = supabase.table("users")\
            .select("daily_calorie_target, daily_protein_target_g, daily_carbs_target_g, daily_fat_target_g")\
            .eq("id", user_id)\
            .single()\
            .execute()
        
        user_data = user_response.data if user_response.data else {}
        
        # Default targets if not set
        targets = {
            "calories": user_data.get("daily_calorie_target") or 2000,
            "protein": user_data.get("daily_protein_target_g") or 150,
            "carbs": user_data.get("daily_carbs_target_g") or 200,
            "fat": user_data.get("daily_fat_target_g") or 65
        }
        
        # Get today's meals
        today = date.today()
        start_of_day = datetime.combine(today, datetime.min.time())
        end_of_day = datetime.combine(today, datetime.max.time())
        
        meals_response = supabase.table("meal_logs")\
            .select("total_calories, total_protein_g, total_carbs_g, total_fat_g")\
            .eq("user_id", user_id)\
            .gte("logged_at", start_of_day.isoformat())\
            .lte("logged_at", end_of_day.isoformat())\
            .execute()
        
        meals = meals_response.data if meals_response.data else []
        
        # Calculate totals
        current = {
            "calories": sum(meal.get("total_calories", 0) for meal in meals),
            "protein": sum(meal.get("total_protein_g", 0) for meal in meals),
            "carbs": sum(meal.get("total_carbs_g", 0) for meal in meals),
            "fat": sum(meal.get("total_fat_g", 0) for meal in meals)
        }
        
        return {
            "targets": targets,
            "current": current
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch nutrition summary: {str(e)}"
        )
