"""
Meals API Endpoints

Handles manual meal logging and meal management.

HOW NUTRITION WORKS:
- Base nutrition stored in foods table per serving_size (typically 100g)
- User inputs in servings (e.g., "1.5 breasts") OR grams (e.g., "210g")
- Backend converts between servings↔grams using household_serving_grams if available
- Nutrition calculated: multiplier = gram_quantity / serving_size
- Each macronutrient: value * multiplier
- Stored in meal_foods with pre-calculated nutrition

Critical Fields for Calculations:
- serving_size (required): Base amount for nutrition (e.g., 100)
- serving_unit (required): Unit for serving_size (e.g., 'g')
- household_serving_unit (optional): User-friendly name (e.g., 'breast', 'banana')
- household_serving_grams (optional): Grams per household serving (e.g., 140g for breast)
- ALL macros: calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, total_sugars_g, sodium_mg

See quantity_converter.py for implementation details.
"""

import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status, UploadFile, File
from pydantic import BaseModel, Field

from app.api.middleware.auth import get_current_user
from app.services.meal_logging_service_v2 import get_meal_logging_service_v2 as get_meal_logging_service
from app.services.photo_meal_matcher_service import get_photo_meal_matcher_service
from app.services.photo_meal_constructor_service import get_photo_meal_constructor_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/meals", tags=["meals"])


# Request Models
class FoodItemRequest(BaseModel):
    """Food or template item in a meal."""
    item_type: str = Field(default="food", description="Type: 'food' or 'template'")
    food_id: Optional[str] = Field(None, description="Food UUID from foods_enhanced table (required if item_type='food')")
    template_id: Optional[str] = Field(None, description="Template UUID from meal_templates (required if item_type='template')")

    # Accept both old format (quantity/unit) and new format (serving_quantity/serving_unit)
    quantity: Optional[float] = Field(None, gt=0, description="Quantity of food/template (legacy)")
    unit: Optional[str] = Field(None, description="Unit (g, oz, cup, serving, etc.) (legacy)")

    # New format from frontend
    serving_quantity: Optional[float] = Field(None, gt=0, description="Serving quantity")
    serving_unit: Optional[str] = Field(None, description="Serving unit")
    gram_quantity: Optional[float] = Field(None, description="Gram quantity (optional)")
    last_edited_field: Optional[str] = Field(None, description="Last edited field (servings/grams)")

    class Config:
        json_schema_extra = {
            "examples": [
                {"item_type": "food", "food_id": "uuid-1", "serving_quantity": 6, "serving_unit": "oz", "gram_quantity": 170},
                {"item_type": "template", "template_id": "uuid-2", "quantity": 1, "unit": "serving"}
            ]
        }


class CreateMealRequest(BaseModel):
    """Request to create a meal log."""
    name: Optional[str] = Field(None, max_length=200, description="Meal name (optional)")
    category: str = Field(..., description="Meal type (breakfast, lunch, dinner, snack)")
    logged_at: str = Field(..., description="ISO timestamp when meal was consumed")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes")
    foods: List[FoodItemRequest] = Field(..., min_items=1, description="Foods in this meal")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Chicken and Rice Bowl",
                "category": "lunch",
                "logged_at": "2025-10-06T12:30:00Z",
                "notes": "Post-workout meal",
                "foods": [
                    {"food_id": "uuid-1", "quantity": 6, "unit": "oz"},
                    {"food_id": "uuid-2", "quantity": 1, "unit": "cup"}
                ]
            }
        }


class UpdateMealRequest(BaseModel):
    """Request to update a meal log."""
    name: Optional[str] = Field(None, max_length=200)
    category: Optional[str] = None
    logged_at: Optional[str] = None
    notes: Optional[str] = Field(None, max_length=500)
    foods: Optional[List[FoodItemRequest]] = None


# Response Models
class FoodItemResponse(BaseModel):
    """Food or template item in a meal response."""
    item_type: str  # 'food' or 'template'
    food_id: Optional[str]
    template_id: Optional[str]
    name: str
    brand: Optional[str]
    quantity: float
    unit: str
    serving_size: Optional[float]
    serving_unit: Optional[str]
    calories: float
    protein_g: float
    carbs_g: float
    fat_g: float
    fiber_g: float
    sugar_g: Optional[float]
    sodium_mg: Optional[float]
    order: int


class MealResponse(BaseModel):
    """Meal log response."""
    id: str
    user_id: str
    name: Optional[str]
    category: str
    logged_at: str
    notes: Optional[str]
    template_id: Optional[str] = None  # Template used to create this meal (optional)
    created_from_template: bool = False  # Whether meal was created from template
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    total_sugar_g: Optional[float]
    total_sodium_mg: Optional[float]
    foods: List[dict]  # Will be FoodItemResponse but keeping as dict for flexibility
    source: str
    estimated: bool
    created_at: str
    updated_at: str


class MealsListResponse(BaseModel):
    """List of meals with pagination."""
    meals: List[MealResponse]
    total: int
    limit: int
    offset: int


# Endpoints
@router.post(
    "",
    response_model=MealResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create meal log",
    description="""
    Create a new meal log with foods.

    **Features:**
    - Add multiple foods to a meal
    - Automatic nutrition calculation
    - Unit conversion (g, oz, cup, etc.)
    - Tracks food popularity

    **Example:**
    ```json
    {
      "name": "Chicken and Rice",
      "category": "lunch",
      "logged_at": "2025-10-06T12:30:00Z",
      "foods": [
        {"food_id": "uuid", "quantity": 6, "unit": "oz"},
        {"food_id": "uuid", "quantity": 1, "unit": "cup"}
      ]
    }
    ```
    """,
    responses={
        201: {"description": "Meal created successfully"},
        400: {"description": "Invalid request data"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def create_meal(
    request: CreateMealRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new meal log.

    Args:
        request: Meal data with foods
        current_user: Authenticated user from JWT

    Returns:
        Created meal with full nutrition data
    """
    try:
        logger.info(f"Create meal request: user_id={current_user['user_id']}, foods_count={len(request.foods)}")

        # Get service
        meal_service = get_meal_logging_service()

        # Convert foods to dict format
        food_items = [food.model_dump() for food in request.foods]

        # Create meal
        meal = await meal_service.create_meal(
            user_id=current_user["user_id"],
            name=request.name,
            category=request.category,
            logged_at=request.logged_at,
            notes=request.notes,
            food_items=food_items
        )

        return MealResponse(**meal)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Create meal failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create meal. Please try again."
        )


@router.get(
    "",
    response_model=MealsListResponse,
    summary="Get user's meals",
    description="""
    Get user's meal logs with filtering and pagination.

    **Filters:**
    - Date range (start_date, end_date)
    - Meal type (category)
    - Pagination (limit, offset)

    **Example:**
    `/meals?start_date=2025-10-01&category=lunch&limit=20`
    """,
    responses={
        200: {"description": "Meals retrieved"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def get_meals(
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    category: Optional[str] = Query(None, description="Meal type filter"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's meal logs.

    Args:
        start_date: Optional start date filter
        end_date: Optional end date filter
        category: Optional meal type filter
        limit: Max results
        offset: Pagination offset
        current_user: Authenticated user from JWT

    Returns:
        List of meals with pagination info
    """
    try:
        logger.info(f"Get meals request: user_id={current_user['user_id']}, limit={limit}, offset={offset}")

        # Get service
        meal_service = get_meal_logging_service()

        # Get meals
        result = await meal_service.get_user_meals(
            user_id=current_user["user_id"],
            start_date=start_date,
            end_date=end_date,
            category=category,
            limit=limit,
            offset=offset
        )

        return MealsListResponse(**result)

    except Exception as e:
        logger.error(f"Get meals failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve meals. Please try again."
        )


@router.get(
    "/{meal_id}",
    response_model=MealResponse,
    summary="Get meal by ID",
    description="Get detailed information about a specific meal.",
    responses={
        200: {"description": "Meal details"},
        404: {"description": "Meal not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def get_meal(
    meal_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get meal by ID.

    Args:
        meal_id: Meal UUID
        current_user: Authenticated user from JWT

    Returns:
        Meal details
    """
    try:
        logger.info(f"Get meal request: meal_id={meal_id}, user_id={current_user['user_id']}")

        # Get service
        meal_service = get_meal_logging_service()

        # Get meal
        meal = await meal_service.get_meal_by_id(
            meal_id=meal_id,
            user_id=current_user["user_id"]
        )

        return MealResponse(**meal)

    except ValueError as e:
        logger.warning(f"Meal not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Get meal failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve meal. Please try again."
        )


@router.patch(
    "/{meal_id}",
    response_model=MealResponse,
    summary="Update meal",
    description="""
    Update an existing meal.

    **Updatable fields:**
    - name
    - category
    - logged_at
    - notes
    - foods (full replacement)

    **Note:** Updating foods will recalculate all nutrition totals.
    """,
    responses={
        200: {"description": "Meal updated"},
        404: {"description": "Meal not found"},
        401: {"description": "Unauthorized"},
        400: {"description": "Invalid request data"},
        500: {"description": "Server error"}
    }
)
async def update_meal(
    meal_id: str,
    request: UpdateMealRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing meal.

    Args:
        meal_id: Meal UUID
        request: Fields to update
        current_user: Authenticated user from JWT

    Returns:
        Updated meal
    """
    try:
        logger.info(f"Update meal request: meal_id={meal_id}, user_id={current_user['user_id']}")

        # Get service
        meal_service = get_meal_logging_service()

        # Build updates dict (exclude None values)
        updates = request.model_dump(exclude_none=True)

        # Convert foods to dict format if present
        if "foods" in updates:
            updates["foods"] = [food.model_dump() if hasattr(food, 'model_dump') else food for food in updates["foods"]]

        # Update meal
        meal = await meal_service.update_meal(
            meal_id=meal_id,
            user_id=current_user["user_id"],
            updates=updates
        )

        return MealResponse(**meal)

    except ValueError as e:
        logger.warning(f"Meal not found or validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in str(e).lower() else status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Update meal failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update meal. Please try again."
        )


@router.delete(
    "/{meal_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete meal",
    description="Delete a meal log. This action cannot be undone.",
    responses={
        204: {"description": "Meal deleted"},
        404: {"description": "Meal not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def delete_meal(
    meal_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete a meal log.

    Args:
        meal_id: Meal UUID
        current_user: Authenticated user from JWT

    Returns:
        204 No Content on success
    """
    try:
        logger.info(f"Delete meal request: meal_id={meal_id}, user_id={current_user['user_id']}")

        # Get service
        meal_service = get_meal_logging_service()

        # Delete meal
        await meal_service.delete_meal(
            meal_id=meal_id,
            user_id=current_user["user_id"]
        )

        # Return 204 No Content
        return None

    except ValueError as e:
        logger.warning(f"Meal not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Delete meal failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete meal. Please try again."
        )


# ============================================================================
# PHOTO MEAL LOGGING ENDPOINTS
# ============================================================================


class PhotoMealPreviewResponse(BaseModel):
    """Response from photo analysis with meal preview."""
    preview_id: str
    meal_type: str
    description: str
    logged_at: str
    foods: List[dict]
    totals: dict
    meta: dict


class ConfirmPhotoMealRequest(BaseModel):
    """Request to confirm and save a photo-detected meal."""
    preview_id: str
    meal_type: str
    description: Optional[str] = None
    logged_at: str
    foods: List[dict]  # Food items from preview
    notes: Optional[str] = None


class AnalyzeTextMealRequest(BaseModel):
    """Request to analyze text food descriptions from client-side image analysis."""
    food_items: List[dict] = Field(..., description="Foods detected by client (name, quantity, unit, grams)")
    meal_type: str = Field(..., description="Meal type from client analysis")
    description: str = Field(..., description="Overall meal description")


@router.post(
    "/photo/analyze-text",
    response_model=PhotoMealPreviewResponse,
    status_code=status.HTTP_200_OK,
    summary="Analyze text food descriptions from client-side photo analysis",
    description="""
    Match text food descriptions to database foods and generate meal preview.

    **NEW FLOW (Client-Side Analysis):**
    1. Frontend analyzes photo with OpenAI Vision (detects foods, NO nutrition)
    2. Frontend sends text food descriptions to this endpoint
    3. Backend matches foods with database
    4. Backend constructs meal preview with accurate nutrition
    5. Return preview for user confirmation

    **IMPORTANT:** This endpoint does NOT save the meal to the database.
    Use `/photo/confirm` to save after user confirmation.

    **Why client-side?** Keeps images on user's device, saves backend storage/bandwidth.
    """,
    responses={
        200: {"description": "Foods matched successfully, meal preview returned"},
        400: {"description": "Invalid input or matching failed"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def analyze_text_meal(
    request: AnalyzeTextMealRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Match text food descriptions to database and return meal preview.

    Args:
        request: Food descriptions from client-side analysis
        current_user: Authenticated user from JWT

    Returns:
        PhotoMealPreviewResponse with matched foods and nutrition
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Text meal analysis request: user_id={user_id}, foods={len(request.food_items)}")

        # Step 1: Match detected foods with database
        matcher_service = get_photo_meal_matcher_service()
        match_result = await matcher_service.match_photo_foods(
            detected_foods=request.food_items,
            user_id=user_id
        )

        logger.info(
            f"Food matching complete: {match_result['total_matched']}/{match_result['total_detected']} matched"
        )

        # Step 2: Construct meal preview
        constructor_service = get_photo_meal_constructor_service()
        meal_preview = await constructor_service.construct_meal_preview(
            matched_foods=match_result["matched_foods"],
            meal_metadata={
                "meal_type": request.meal_type,
                "description": request.description
            },
            user_id=user_id
        )

        logger.info(f"✅ Text meal preview constructed: preview_id={meal_preview['preview_id']}")

        return PhotoMealPreviewResponse(**meal_preview)

    except ValueError as e:
        logger.warning(f"Text analysis validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Text meal analysis failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to match foods. Please try again."
        )


@router.post(
    "/photo/confirm",
    response_model=MealResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Confirm and save photo-detected meal",
    description="""
    Confirm and save a photo-detected meal to the database.

    **Flow:**
    1. User reviews meal preview from `/photo/analyze`
    2. User confirms or edits the meal
    3. Frontend sends confirmation request
    4. Backend saves meal to database

    **This endpoint:**
    - Saves meal to `meals` table
    - Saves food items to `meal_foods` table
    - Calculates and stores nutrition totals
    - Returns saved meal with ID
    """,
    responses={
        201: {"description": "Meal saved successfully"},
        400: {"description": "Invalid request data"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def confirm_photo_meal(
    request: ConfirmPhotoMealRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Confirm and save a photo-detected meal.

    Args:
        request: Confirmed meal data from preview
        current_user: Authenticated user from JWT

    Returns:
        Saved meal with ID
    """
    try:
        user_id = current_user["user_id"]
        logger.info(f"Confirm photo meal: user_id={user_id}, preview_id={request.preview_id}")

        # Build meal data for creation
        # Convert preview food items to create_meal format
        food_items = []
        for food in request.foods:
            food_items.append({
                "food_id": food["food_id"],
                "quantity": food["grams"],  # Use grams as base quantity
                "unit": "g"
            })

        # Use existing meal logging service to save
        meal_service = get_meal_logging_service()
        meal = await meal_service.create_meal(
            user_id=user_id,
            name=request.description,
            category=request.meal_type,
            logged_at=request.logged_at,
            notes=f"Photo-detected meal. {request.notes or ''}".strip(),
            food_items=food_items
        )

        logger.info(f"✅ Photo meal saved: meal_id={meal['id']}")

        return MealResponse(**meal)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Confirm photo meal failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to save meal. Please try again."
        )
