"""
Meal Templates API Endpoints

Handles meal template management with support for recursive templates.
"""

import logging
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field

from app.api.middleware.auth import get_current_user
from app.services.meal_template_service import get_meal_template_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/templates", tags=["templates"])


# Request Models
class TemplateItemRequest(BaseModel):
    """Food or template item in a meal template."""
    item_type: str = Field(default="food", description="Type: 'food' or 'template'")
    food_id: Optional[str] = Field(None, description="Food UUID (required if item_type='food')")
    template_id: Optional[str] = Field(None, description="Child template UUID (required if item_type='template')")
    quantity: float = Field(..., gt=0, description="Quantity")
    unit: str = Field(..., description="Unit (g, oz, cup, serving, etc.)")

    class Config:
        json_schema_extra = {
            "examples": [
                {"item_type": "food", "food_id": "uuid-1", "quantity": 6, "unit": "oz"},
                {"item_type": "template", "template_id": "uuid-2", "quantity": 1, "unit": "serving"}
            ]
        }


class CreateTemplateRequest(BaseModel):
    """Request to create a meal template."""
    name: str = Field(..., min_length=1, max_length=200, description="Template name")
    category: str = Field(..., description="Meal type (breakfast, lunch, dinner, snack)")
    description: Optional[str] = Field(None, max_length=500, description="Optional description")
    tags: Optional[List[str]] = Field(None, description="Optional tags for categorization")
    food_items: List[TemplateItemRequest] = Field(..., min_items=1, description="Foods/templates in this template")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "High Protein Breakfast",
                "category": "breakfast",
                "description": "My go-to high protein breakfast",
                "tags": ["high-protein", "quick"],
                "food_items": [
                    {"item_type": "food", "food_id": "uuid-1", "quantity": 4, "unit": "oz"},
                    {"item_type": "food", "food_id": "uuid-2", "quantity": 1, "unit": "cup"}
                ]
            }
        }


class UpdateTemplateRequest(BaseModel):
    """Request to update a meal template."""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    category: Optional[str] = None
    description: Optional[str] = Field(None, max_length=500)
    tags: Optional[List[str]] = None
    is_favorite: Optional[bool] = None


class CreateMealFromTemplateRequest(BaseModel):
    """Request to create a meal from a template."""
    logged_at: Optional[str] = Field(None, description="Timestamp when meal was consumed")
    notes: Optional[str] = Field(None, max_length=500, description="Optional notes")

    class Config:
        json_schema_extra = {
            "example": {
                "logged_at": "2025-10-09T08:30:00Z",
                "notes": "Used this template for breakfast"
            }
        }


# Response Models
class TemplateItemResponse(BaseModel):
    """Template item in response."""
    item_type: str
    food_id: Optional[str]
    template_id: Optional[str]
    name: str
    quantity: float
    unit: str
    order_index: int


class TemplateResponse(BaseModel):
    """Template response."""
    id: str
    user_id: str
    name: str
    category: str
    description: Optional[str]
    tags: Optional[List[str]]
    is_favorite: bool
    use_count: int
    last_used_at: Optional[str]
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    total_fiber_g: float
    items: List[dict]
    created_at: str
    updated_at: str


class TemplatesListResponse(BaseModel):
    """List of templates with pagination."""
    templates: List[TemplateResponse]
    total: int
    limit: int
    offset: int


# Endpoints
@router.post(
    "",
    response_model=TemplateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create meal template",
    description="""
    Create a new reusable meal template.

    **Features:**
    - Add multiple foods to a template
    - Add other templates (recursive nesting)
    - Automatic nutrition calculation
    - Track usage statistics

    **Example:**
    ```json
    {
      "name": "High Protein Breakfast",
      "category": "breakfast",
      "description": "My go-to breakfast",
      "tags": ["high-protein", "quick"],
      "food_items": [
        {"item_type": "food", "food_id": "uuid", "quantity": 4, "unit": "oz"},
        {"item_type": "template", "template_id": "uuid", "quantity": 1, "unit": "serving"}
      ]
    }
    ```
    """,
    responses={
        201: {"description": "Template created successfully"},
        400: {"description": "Invalid request data"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def create_template(
    request: CreateTemplateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new meal template."""
    try:
        logger.info(f"Create template request: user_id={current_user['user_id']}, name={request.name}")

        # Get service
        template_service = get_meal_template_service()

        # Convert items to dict format
        food_items = [item.model_dump() for item in request.food_items]

        # Create template
        template = await template_service.create_template(
            user_id=current_user["user_id"],
            name=request.name,
            category=request.category,
            description=request.description,
            tags=request.tags,
            food_items=food_items
        )

        return TemplateResponse(**template)

    except ValueError as e:
        logger.warning(f"Validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Create template failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create template. Please try again."
        )


@router.get(
    "",
    response_model=TemplatesListResponse,
    summary="Get user's templates",
    description="""
    Get user's meal templates with filtering.

    **Filters:**
    - Category (breakfast, lunch, dinner, snack)
    - Favorites only
    - Tags (any match)
    - Pagination (limit, offset)

    **Example:**
    `/templates?category=breakfast&favorites_only=true&limit=20`
    """,
    responses={
        200: {"description": "Templates retrieved"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def get_templates(
    category: Optional[str] = Query(None, description="Category filter"),
    favorites_only: bool = Query(False, description="Only show favorites"),
    tags: Optional[str] = Query(None, description="Comma-separated tags"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_user: dict = Depends(get_current_user)
):
    """Get user's meal templates."""
    try:
        logger.info(f"Get templates request: user_id={current_user['user_id']}")

        # Parse tags
        tag_list = tags.split(",") if tags else None

        # Get service
        template_service = get_meal_template_service()

        # Get templates
        result = await template_service.get_user_templates(
            user_id=current_user["user_id"],
            category=category,
            favorites_only=favorites_only,
            tags=tag_list,
            limit=limit,
            offset=offset
        )

        return TemplatesListResponse(**result)

    except Exception as e:
        logger.error(f"Get templates failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve templates. Please try again."
        )


@router.get(
    "/{template_id}",
    response_model=TemplateResponse,
    summary="Get template by ID",
    description="Get detailed information about a specific template.",
    responses={
        200: {"description": "Template details"},
        404: {"description": "Template not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def get_template(
    template_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get template by ID."""
    try:
        logger.info(f"Get template request: template_id={template_id}, user_id={current_user['user_id']}")

        # Get service
        template_service = get_meal_template_service()

        # Get template
        template = await template_service.get_template_by_id(
            template_id=template_id,
            user_id=current_user["user_id"]
        )

        return TemplateResponse(**template)

    except ValueError as e:
        logger.warning(f"Template not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Get template failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve template. Please try again."
        )


@router.patch(
    "/{template_id}",
    response_model=TemplateResponse,
    summary="Update template",
    description="""
    Update an existing template.

    **Updatable fields:**
    - name
    - category
    - description
    - tags
    - is_favorite
    """,
    responses={
        200: {"description": "Template updated"},
        404: {"description": "Template not found"},
        401: {"description": "Unauthorized"},
        400: {"description": "Invalid request data"},
        500: {"description": "Server error"}
    }
)
async def update_template(
    template_id: str,
    request: UpdateTemplateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update an existing template."""
    try:
        logger.info(f"Update template request: template_id={template_id}, user_id={current_user['user_id']}")

        # Get service
        template_service = get_meal_template_service()

        # Build updates dict (exclude None values)
        updates = request.model_dump(exclude_none=True)

        # Update template
        template = await template_service.update_template(
            template_id=template_id,
            user_id=current_user["user_id"],
            updates=updates
        )

        return TemplateResponse(**template)

    except ValueError as e:
        logger.warning(f"Template not found or validation error: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND if "not found" in str(e).lower() else status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Update template failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update template. Please try again."
        )


@router.delete(
    "/{template_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete template",
    description="Delete a meal template. This action cannot be undone.",
    responses={
        204: {"description": "Template deleted"},
        404: {"description": "Template not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def delete_template(
    template_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete a meal template."""
    try:
        logger.info(f"Delete template request: template_id={template_id}, user_id={current_user['user_id']}")

        # Get service
        template_service = get_meal_template_service()

        # Delete template
        await template_service.delete_template(
            template_id=template_id,
            user_id=current_user["user_id"]
        )

        # Return 204 No Content
        return None

    except ValueError as e:
        logger.warning(f"Template not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Delete template failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete template. Please try again."
        )


@router.post(
    "/{template_id}/create-meal",
    status_code=status.HTTP_201_CREATED,
    summary="Create meal from template",
    description="""
    Create a meal log from a template (one-click meal logging).

    This endpoint:
    - Flattens recursive template structure
    - Creates meal_log entry
    - Adds all foods from template (and nested templates)
    - Increments template usage count
    - Updates last_used_at timestamp

    **Example:**
    ```json
    {
      "logged_at": "2025-10-09T12:30:00Z",
      "notes": "Lunch using my favorite template"
    }
    ```
    """,
    responses={
        201: {"description": "Meal created from template"},
        404: {"description": "Template not found"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def create_meal_from_template(
    template_id: str,
    request: CreateMealFromTemplateRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a meal from a template."""
    try:
        logger.info(f"Create meal from template: template_id={template_id}, user_id={current_user['user_id']}")

        # Get service
        template_service = get_meal_template_service()

        # Create meal
        meal = await template_service.create_meal_from_template(
            template_id=template_id,
            user_id=current_user["user_id"],
            logged_at=request.logged_at,
            notes=request.notes
        )

        return {"data": meal}

    except ValueError as e:
        logger.warning(f"Template not found: {e}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Create meal from template failed: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create meal from template. Please try again."
        )
