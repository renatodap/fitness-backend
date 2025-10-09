"""
Events API Endpoints

Handles user events (races, competitions, shows) and calendar functionality.

Endpoints:
- POST /events - Create new event
- GET /events/upcoming - Get upcoming events
- GET /events/primary - Get primary event
- GET /events/{event_id} - Get event details
- GET /events/{event_id}/countdown - Get event countdown
- PATCH /events/{event_id} - Update event
- DELETE /events/{event_id} - Delete event
- POST /events/{event_id}/generate-program - Generate event-specific program
- POST /events/{event_id}/complete - Mark event as completed
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from datetime import date
from typing import List, Optional, Dict, Any

from app.services.event_service import get_event_service
from app.api.middleware.auth import get_current_user

router = APIRouter(prefix="/events", tags=["Events & Calendar"])


# =====================================================
# REQUEST MODELS
# =====================================================

class CreateEventRequest(BaseModel):
    """Request model for creating event."""
    event_name: str = Field(..., min_length=1, max_length=200, description="Event name")
    event_type: str = Field(..., description="Event type (marathon, powerlifting_meet, etc.)")
    event_date: date = Field(..., description="Event date")
    event_subtype: Optional[str] = Field(None, description="Event subtype (Boston Marathon, etc.)")
    location: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    country: Optional[str] = None
    goal_performance: Optional[str] = Field(None, description="Goal (Sub 3:30, 300kg total, etc.)")
    target_time: Optional[str] = Field(None, description="Target time for timed events")
    target_weight_class: Optional[str] = Field(None, description="Weight class for strength sports")
    priority: int = Field(default=3, ge=1, le=5, description="Priority (1=highest, 5=lowest)")
    is_primary_goal: bool = Field(default=False, description="Set as primary event")
    registration_url: Optional[str] = None
    event_website: Optional[str] = None
    notes: Optional[str] = None
    tags: List[str] = Field(default_factory=list)

    class Config:
        json_schema_extra = {
            "example": {
                "event_name": "Boston Marathon 2026",
                "event_type": "marathon",
                "event_date": "2026-04-20",
                "location": "Boston, MA",
                "goal_performance": "Sub 3:30",
                "priority": 1,
                "is_primary_goal": True
            }
        }


class UpdateEventRequest(BaseModel):
    """Request model for updating event."""
    event_name: Optional[str] = None
    event_date: Optional[date] = None
    goal_performance: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = Field(None, ge=1, le=5)
    is_primary_goal: Optional[bool] = None
    notes: Optional[str] = None
    tags: Optional[List[str]] = None


class CompleteEventRequest(BaseModel):
    """Request model for completing event."""
    result_notes: Optional[str] = Field(None, description="Result notes (Finished 23rd overall)")
    result_data: Optional[Dict[str, Any]] = Field(None, description="Detailed results")


# =====================================================
# RESPONSE MODELS
# =====================================================

class EventResponse(BaseModel):
    """Response model for event."""
    id: str
    user_id: str
    event_name: str
    event_type: str
    event_date: date
    status: str
    priority: int
    is_primary_goal: bool
    goal_performance: Optional[str] = None
    location: Optional[str] = None
    training_start_date: Optional[date] = None
    taper_start_date: Optional[date] = None
    peak_week_date: Optional[date] = None
    linked_program_id: Optional[str] = None
    created_at: str


class EventCountdownResponse(BaseModel):
    """Response model for event countdown."""
    event_id: str
    event_name: str
    event_type: str
    event_date: date
    days_until_event: int
    weeks_until_event: int
    current_training_phase: str
    phase_progress_percentage: float
    is_taper_week: bool
    is_peak_week: bool
    is_pre_training: bool
    milestones: Dict[str, str]
    countdown_message: str


class EventWithCountdownResponse(EventResponse):
    """Event response with countdown data."""
    days_until_event: int
    weeks_until_event: int
    current_training_phase: str
    countdown_message: str


# =====================================================
# ENDPOINTS
# =====================================================

@router.post("/", response_model=EventResponse, status_code=status.HTTP_201_CREATED)
async def create_event(
    request: CreateEventRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Create new event.

    Creates event with auto-calculated training dates based on event type.
    """
    try:
        event_service = get_event_service()

        event = await event_service.create_event(
            user_id=current_user["id"],
            **request.dict()
        )

        return event

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error creating event: {str(e)}"
        )


@router.get("/upcoming", response_model=List[EventWithCountdownResponse])
async def get_upcoming_events(
    days_ahead: int = 365,
    current_user: dict = Depends(get_current_user)
):
    """
    Get upcoming events for user.

    Returns events with countdown data.
    """
    try:
        event_service = get_event_service()

        events = await event_service.get_upcoming_events(
            user_id=current_user["id"],
            days_ahead=days_ahead
        )

        # Enrich with countdown data
        enriched_events = []
        for event in events:
            countdown = await event_service.get_event_countdown(event['id'])
            enriched_events.append({
                **event,
                'days_until_event': countdown['days_until_event'],
                'weeks_until_event': countdown['weeks_until_event'],
                'current_training_phase': countdown['current_training_phase'],
                'countdown_message': countdown['countdown_message']
            })

        return enriched_events

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching events: {str(e)}"
        )


@router.get("/primary", response_model=Optional[EventWithCountdownResponse])
async def get_primary_event(
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's primary event.

    Returns None if no primary event set.
    """
    try:
        event_service = get_event_service()

        event = await event_service.get_primary_event(current_user["id"])

        if not event:
            return None

        # Enrich with countdown
        countdown = await event_service.get_event_countdown(event['id'])

        return {
            **event,
            'days_until_event': countdown['days_until_event'],
            'weeks_until_event': countdown['weeks_until_event'],
            'current_training_phase': countdown['current_training_phase'],
            'countdown_message': countdown['countdown_message']
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching primary event: {str(e)}"
        )


@router.get("/primary/countdown", response_model=EventCountdownResponse)
async def get_primary_event_countdown(
    current_user: dict = Depends(get_current_user)
):
    """
    Get countdown for user's primary event.

    Returns countdown data for the primary event.
    Returns 404 if no primary event is set.
    """
    try:
        event_service = get_event_service()

        event = await event_service.get_primary_event(current_user["id"])

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No primary event set"
            )

        countdown = await event_service.get_event_countdown(event['id'])

        return countdown

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching primary event countdown: {str(e)}"
        )


@router.get("/", response_model=List[EventResponse])
async def get_all_events(
    include_completed: bool = False,
    current_user: dict = Depends(get_current_user)
):
    """Get all events for user."""
    try:
        event_service = get_event_service()

        events = await event_service.get_all_events(
            user_id=current_user["id"],
            include_completed=include_completed
        )

        return events

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching events: {str(e)}"
        )


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Get event details."""
    try:
        event_service = get_event_service()

        # Verify access
        events = await event_service.get_all_events(
            user_id=current_user["id"],
            include_completed=True
        )

        event = next((e for e in events if e['id'] == event_id), None)

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        return event

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching event: {str(e)}"
        )


@router.get("/{event_id}/countdown", response_model=EventCountdownResponse)
async def get_event_countdown(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Get countdown information for event.

    Returns:
    - Days/weeks until event
    - Current training phase
    - Phase progress percentage
    - Key milestones
    """
    try:
        event_service = get_event_service()

        countdown = await event_service.get_event_countdown(event_id)

        return countdown

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching countdown: {str(e)}"
        )


@router.patch("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: str,
    request: UpdateEventRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update event details."""
    try:
        event_service = get_event_service()

        # Only include non-None values
        updates = {k: v for k, v in request.dict().items() if v is not None}

        if not updates:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="No updates provided"
            )

        event = await event_service.update_event(
            event_id=event_id,
            user_id=current_user["id"],
            updates=updates
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        return event

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating event: {str(e)}"
        )


@router.delete("/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_event(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):
    """Delete event."""
    try:
        event_service = get_event_service()

        await event_service.delete_event(
            event_id=event_id,
            user_id=current_user["id"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting event: {str(e)}"
        )


@router.post("/{event_id}/generate-program")
async def generate_event_program(
    event_id: str,
    current_user: dict = Depends(get_current_user)
):
    """
    Generate event-specific training program.

    Creates AI program periodized to peak at event date.
    """
    try:
        event_service = get_event_service()

        program_id = await event_service.generate_event_specific_program(
            user_id=current_user["id"],
            event_id=event_id
        )

        return {
            "success": True,
            "program_id": program_id,
            "message": "Event-specific program generated successfully"
        }

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error generating program: {str(e)}"
        )


@router.post("/{event_id}/complete", response_model=EventResponse)
async def complete_event(
    event_id: str,
    request: CompleteEventRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Mark event as completed with results.

    Updates event status and stores result data.
    """
    try:
        event_service = get_event_service()

        event = await event_service.complete_event(
            event_id=event_id,
            user_id=current_user["id"],
            result_notes=request.result_notes,
            result_data=request.result_data
        )

        if not event:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Event not found"
            )

        return event

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error completing event: {str(e)}"
        )
