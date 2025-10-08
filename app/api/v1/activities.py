"""
Activities API Endpoints

Handles activity logging and activity management.
"""

import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.api.middleware.auth import get_current_user
from app.services.activity_logging_service import get_activity_logging_service
from app.api.v1.schemas.activity_schemas import (
    CreateActivityRequest,
    UpdateActivityRequest,
    ActivityResponse,
    ActivitiesListResponse,
    ActivityTypesResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/activities", tags=["activities"])


# ============================================================================
# ACTIVITY TYPE CONFIGURATION
# ============================================================================

@router.get(
    "/types",
    response_model=ActivityTypesResponse,
    summary="Get activity types configuration",
    description="""
    Get all supported activity types with field configurations.

    **Use this endpoint to:**
    - Generate dynamic forms on frontend
    - Validate required fields
    - Display appropriate units and placeholders

    **Returns:**
    - Activity type metadata
    - Required and optional fields
    - Field validation rules
    - Icons and descriptions
    """
)
async def get_activity_types():
    """Get all activity type configurations for frontend form generation"""
    service = get_activity_logging_service()
    config = await service.get_activity_types_config()
    return config


# ============================================================================
# CRUD OPERATIONS
# ============================================================================

@router.post(
    "",
    response_model=ActivityResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create activity log",
    description="""
    Log a new activity with type-specific fields.

    **Supports all activity types:**
    - Cardio: running, cycling, swimming, walking, hiking
    - Strength: strength_training, crossfit, workout
    - Sports: tennis, soccer, basketball
    - Mind-body: yoga
    - Recreational: climbing

    **Features:**
    - Dynamic field validation based on activity type
    - Support for exercises and sets (strength training)
    - Automatic duration calculation
    - Integration with Quick Entry

    **Example (Running):**
    ```json
    {
      "activity_type": "running",
      "name": "Morning Run",
      "start_date": "2025-10-08T07:00:00Z",
      "duration_minutes": 45,
      "distance_meters": 8000,
      "average_pace": "5:37 /mi",
      "calories": 450,
      "perceived_exertion": 7
    }
    ```

    **Example (Strength Training):**
    ```json
    {
      "activity_type": "strength_training",
      "name": "Upper Body",
      "start_date": "2025-10-08T18:00:00Z",
      "duration_minutes": 60,
      "exercises": [
        {
          "exercise_name": "Bench Press",
          "order_index": 1,
          "sets": [
            {"set_number": 1, "reps_completed": 8, "weight_lbs": 185},
            {"set_number": 2, "reps_completed": 6, "weight_lbs": 205}
          ]
        }
      ]
    }
    ```
    """,
    responses={
        201: {"description": "Activity created successfully"},
        400: {"description": "Invalid request data or unsupported activity type"},
        401: {"description": "Unauthorized"},
        500: {"description": "Server error"}
    }
)
async def create_activity(
    request: CreateActivityRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create a new activity log.

    Validates activity type and required fields, then stores in database.
    For strength training activities, also creates exercise and set records.
    """
    service = get_activity_logging_service()

    try:
        # Convert Pydantic model to dict
        activity_data = request.model_dump(exclude_none=True)

        # Create activity
        activity = await service.create_activity(
            user_id=current_user["id"],
            activity_data=activity_data
        )

        return activity

    except ValueError as e:
        logger.warning(f"Invalid activity data: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to create activity: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create activity"
        )


@router.get(
    "",
    response_model=ActivitiesListResponse,
    summary="Get activities",
    description="""
    Get user's activity logs with filters and pagination.

    **Filters:**
    - `activity_type`: Filter by type (running, cycling, etc.)
    - `source`: Filter by source (manual, quick_entry, strava, garmin)
    - `start_date`: Activities after this date (ISO format)
    - `end_date`: Activities before this date (ISO format)

    **Pagination:**
    - `limit`: Max results per page (default: 50, max: 100)
    - `offset`: Skip this many results (default: 0)

    **Returns:**
    - List of activities
    - Total count (for pagination)
    - Applied limit and offset
    """
)
async def get_activities(
    activity_type: Optional[str] = Query(None, description="Filter by activity type"),
    source: Optional[str] = Query(None, description="Filter by source"),
    start_date: Optional[str] = Query(None, description="Start date (ISO format)"),
    end_date: Optional[str] = Query(None, description="End date (ISO format)"),
    limit: int = Query(50, ge=1, le=100, description="Max results"),
    offset: int = Query(0, ge=0, description="Pagination offset"),
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's activities with optional filters and pagination.

    Returns activities ordered by start_date (most recent first).
    """
    service = get_activity_logging_service()

    try:
        result = await service.get_activities(
            user_id=current_user["id"],
            activity_type=activity_type,
            start_date=start_date,
            end_date=end_date,
            source=source,
            limit=limit,
            offset=offset
        )

        return result

    except Exception as e:
        logger.error(f"Failed to get activities: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve activities"
        )


@router.get(
    "/{activity_id}",
    response_model=ActivityResponse,
    summary="Get activity by ID",
    description="""
    Get a single activity by ID.

    **Returns:**
    - Full activity details
    - Exercises and sets (for strength training)
    - All metrics and notes

    **Errors:**
    - 404: Activity not found or doesn't belong to user
    """
)
async def get_activity(
    activity_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get a single activity by ID"""
    service = get_activity_logging_service()

    try:
        activity = await service.get_activity(
            user_id=current_user["id"],
            activity_id=activity_id
        )

        return activity

    except ValueError as e:
        logger.warning(f"Activity not found: {activity_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to get activity {activity_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to retrieve activity"
        )


@router.put(
    "/{activity_id}",
    response_model=ActivityResponse,
    summary="Update activity",
    description="""
    Update an existing activity.

    **Updatable fields:**
    - name, duration, distance, pace
    - Heart rate, calories, RPE
    - Notes, tags, mood
    - Any activity-specific metrics

    **Note:** Only the activity owner can update it.
    """
)
async def update_activity(
    activity_id: str,
    request: UpdateActivityRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Update an existing activity.

    Validates ownership before updating.
    """
    service = get_activity_logging_service()

    try:
        # Convert to dict and remove None values
        update_data = request.model_dump(exclude_none=True)

        if not update_data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No fields to update"
            )

        # Update activity
        activity = await service.update_activity(
            user_id=current_user["id"],
            activity_id=activity_id,
            update_data=update_data
        )

        return activity

    except ValueError as e:
        logger.warning(f"Activity not found: {activity_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to update activity {activity_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update activity"
        )


@router.delete(
    "/{activity_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete activity",
    description="""
    Delete an activity log.

    **Warning:** This action cannot be undone.

    **Cascade behavior:**
    - Deletes related exercises and sets (for strength training)
    - Deletes related segments (for cardio)

    **Note:** Only the activity owner can delete it.
    """
)
async def delete_activity(
    activity_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Delete an activity.

    Validates ownership before deletion. Cascades to exercises and sets.
    """
    service = get_activity_logging_service()

    try:
        await service.delete_activity(
            user_id=current_user["id"],
            activity_id=activity_id
        )

        return None  # 204 No Content

    except ValueError as e:
        logger.warning(f"Activity not found: {activity_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Failed to delete activity {activity_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete activity"
        )
