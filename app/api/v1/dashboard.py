"""
Dashboard API endpoints for adaptive dashboard system.

This module provides endpoints for:
- Getting dashboard context (user state, program info, events)
- Tracking behavior signals (dashboard_opens, card_dismissals)
- Logging app open events
- Updating dashboard preferences
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from datetime import datetime, timedelta
from typing import Optional, Literal
import structlog

from app.api.v1.dependencies import get_current_user
from app.services.supabase_service import get_service_client

logger = structlog.get_logger()

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


# ==================== Request Models ====================

class BehaviorSignalRequest(BaseModel):
    """Request model for logging behavior signals."""
    signal_type: Literal[
        "dashboard_open",
        "card_interaction",
        "card_dismissal",
        "setting_change"
    ] = Field(..., description="Type of behavior signal")
    signal_value: str = Field(..., description="Signal value (e.g., card name, setting changed)")
    metadata: Optional[dict] = Field(default={}, description="Additional metadata")


class AppOpenRequest(BaseModel):
    """Request model for logging app open events."""
    source: Optional[str] = Field(None, description="Source of app open (notification, widget, direct)")
    time_of_day: str = Field(..., description="Time of day (morning, afternoon, evening, night)")


class DashboardPreferenceRequest(BaseModel):
    """Request model for updating dashboard preference."""
    preference: Literal["simple", "balanced", "detailed"] = Field(
        ...,
        description="Dashboard variant preference"
    )


# ==================== Response Models ====================

class UserContext(BaseModel):
    """User context for dashboard rendering."""
    hasCompletedConsultation: bool
    hasActiveProgram: bool
    streakDays: int
    tracksWeight: bool
    showsWeightCard: bool
    showsRecoveryCard: bool
    showsWorkoutCard: bool


class ProgramContext(BaseModel):
    """Program context for dashboard rendering."""
    dayNumber: Optional[int] = None
    adherenceLast3Days: Optional[int] = None
    weekNumber: Optional[int] = None
    programName: Optional[str] = None


class EventContext(BaseModel):
    """Event context for dashboard rendering."""
    name: str
    date: str
    daysUntil: int


class EventsContext(BaseModel):
    """Events context wrapper."""
    primaryEvent: Optional[EventContext] = None


class DashboardContextResponse(BaseModel):
    """Complete dashboard context response."""
    user: UserContext
    program: Optional[ProgramContext] = None
    events: Optional[EventsContext] = None


class BehaviorSignalResponse(BaseModel):
    """Response for behavior signal logging."""
    success: bool
    message: str


class PreferenceUpdateResponse(BaseModel):
    """Response for preference update."""
    success: bool
    new_preference: str


class DailyAdherence(BaseModel):
    """Daily adherence data point."""
    day: str
    percent: int


class WeeklyAnalyticsResponse(BaseModel):
    """Weekly analytics data."""
    adherencePercent: int
    averageCalories: int
    targetCalories: int
    mealsLogged: int
    workoutsCompleted: int
    dailyAdherence: list[DailyAdherence]


# ==================== Helper Functions ====================

async def calculate_streak(user_id: str) -> int:
    """
    Calculate user's current streak (consecutive days with logged meals).

    Args:
        user_id: User's unique identifier

    Returns:
        Number of consecutive days with meal logs
    """
    try:
        supabase = get_service_client()

        # Get meal logs for last 60 days (ordered by date)
        sixty_days_ago = (datetime.utcnow() - timedelta(days=60)).isoformat()

        response = supabase.table("meals") \
            .select("logged_at") \
            .eq("user_id", user_id) \
            .gte("logged_at", sixty_days_ago) \
            .order("logged_at", desc=True) \
            .execute()

        if not response.data:
            return 0

        # Extract dates (ignore time)
        dates = set()
        for log in response.data:
            log_date = datetime.fromisoformat(log["logged_at"].replace("Z", "+00:00")).date()
            dates.add(log_date)

        # Calculate streak from today backwards
        streak = 0
        current_date = datetime.utcnow().date()

        while current_date in dates:
            streak += 1
            current_date -= timedelta(days=1)

        return streak

    except Exception as e:
        logger.error("Failed to calculate streak", user_id=user_id, error=str(e))
        return 0


async def get_program_context(user_id: str) -> Optional[ProgramContext]:
    """
    Get user's active program context.

    Args:
        user_id: User's unique identifier

    Returns:
        ProgramContext or None if no active program
    """
    try:
        supabase = get_service_client()

        # Get active program
        response = supabase.table("ai_generated_programs") \
            .select("id, name, start_date, duration_weeks") \
            .eq("user_id", user_id) \
            .eq("status", "active") \
            .single() \
            .execute()

        if not response.data:
            return None

        program = response.data
        start_date = datetime.fromisoformat(program["start_date"].replace("Z", "+00:00")).date()
        current_date = datetime.utcnow().date()

        # Calculate day number and week number
        days_elapsed = (current_date - start_date).days + 1
        week_number = ((days_elapsed - 1) // 7) + 1

        # Calculate adherence last 3 days
        three_days_ago = (datetime.utcnow() - timedelta(days=3)).isoformat()

        # Count expected actions (meals + workouts)
        # Assuming 3 meals/day + program day workouts
        expected = 3 * 3  # 3 days × 3 meals = 9 expected

        # Count actual logs
        meals_response = supabase.table("meals") \
            .select("id", count="exact") \
            .eq("user_id", user_id) \
            .gte("logged_at", three_days_ago) \
            .execute()

        actual = meals_response.count or 0
        adherence_percent = min(100, int((actual / expected) * 100)) if expected > 0 else 0

        return ProgramContext(
            dayNumber=days_elapsed,
            adherenceLast3Days=adherence_percent,
            weekNumber=week_number,
            programName=program["name"]
        )

    except Exception as e:
        logger.error("Failed to get program context", user_id=user_id, error=str(e))
        return None


async def get_events_context(user_id: str) -> Optional[EventsContext]:
    """
    Get user's upcoming events context.

    Args:
        user_id: User's unique identifier

    Returns:
        EventsContext or None if no upcoming events
    """
    try:
        supabase = get_service_client()

        # Get next upcoming event (within 60 days)
        current_date = datetime.utcnow().date()
        sixty_days_ahead = (current_date + timedelta(days=60)).isoformat()

        response = supabase.table("events") \
            .select("event_name, event_date") \
            .eq("user_id", user_id) \
            .gte("event_date", current_date.isoformat()) \
            .lte("event_date", sixty_days_ahead) \
            .order("event_date", desc=False) \
            .limit(1) \
            .execute()

        if not response.data:
            return None

        event = response.data[0]
        event_date = datetime.fromisoformat(event["event_date"]).date()
        days_until = (event_date - current_date).days

        primary_event = EventContext(
            name=event["event_name"],
            date=event["event_date"],
            daysUntil=days_until
        )

        return EventsContext(primaryEvent=primary_event)

    except Exception as e:
        logger.error("Failed to get events context", user_id=user_id, error=str(e))
        return None


# ==================== Endpoints ====================

@router.get(
    "/context",
    response_model=DashboardContextResponse,
    summary="Get dashboard context",
    description="""
    Get complete context for rendering adaptive dashboard.

    Returns:
    - User state (consultation status, tracking preferences, streak)
    - Active program details (day number, adherence, week number)
    - Upcoming events (primary event within 30 days)

    This endpoint is called on dashboard load to determine which cards to show.
    """
)
async def get_dashboard_context(
    current_user: dict = Depends(get_current_user)
):
    """Get complete dashboard context for user."""
    try:
        user_id = current_user["user_id"]
        supabase = get_service_client()

        # Get user profile
        profile_response = supabase.table("profiles") \
            .select("consultation_onboarding_completed, shows_weight_card, shows_recovery_card, shows_workout_card") \
            .eq("id", user_id) \
            .single() \
            .execute()

        profile = profile_response.data if profile_response.data else {}

        # Get active program status
        program_response = supabase.table("ai_generated_programs") \
            .select("id") \
            .eq("user_id", user_id) \
            .eq("status", "active") \
            .limit(1) \
            .execute()

        has_active_program = len(program_response.data) > 0 if program_response.data else False

        # Calculate streak
        streak = await calculate_streak(user_id)

        # Check if user tracks weight (2+ weight logs in last 14 days)
        fourteen_days_ago = (datetime.utcnow() - timedelta(days=14)).isoformat()
        weight_response = supabase.table("body_measurements") \
            .select("id", count="exact") \
            .eq("user_id", user_id) \
            .gte("measured_at", fourteen_days_ago) \
            .execute()

        tracks_weight = (weight_response.count or 0) >= 2

        # Build user context
        user_context = UserContext(
            hasCompletedConsultation=profile.get("consultation_onboarding_completed") or False,
            hasActiveProgram=has_active_program,
            streakDays=streak,
            tracksWeight=tracks_weight,
            showsWeightCard=profile.get("shows_weight_card") or tracks_weight,
            showsRecoveryCard=profile.get("shows_recovery_card") or False,
            showsWorkoutCard=profile.get("shows_workout_card", True) if profile.get("shows_workout_card") is not None else True
        )

        # Get program context (if active)
        program_context = await get_program_context(user_id) if has_active_program else None

        # Get events context
        events_context = await get_events_context(user_id)

        return DashboardContextResponse(
            user=user_context,
            program=program_context,
            events=events_context
        )

    except Exception as e:
        logger.error("Failed to get dashboard context", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to load dashboard context"
        )


@router.post(
    "/behavior",
    response_model=BehaviorSignalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log behavior signal",
    description="""
    Log user behavior signals for adaptive dashboard learning.

    Signal types:
    - dashboard_open: User opened dashboard
    - card_interaction: User interacted with a card (click, expand, etc.)
    - card_dismissal: User dismissed a card
    - setting_change: User changed a setting

    These signals help the system learn user preferences over time.
    """
)
async def log_behavior_signal(
    request: BehaviorSignalRequest,
    current_user: dict = Depends(get_current_user)
):
    """Log behavior signal for adaptive learning."""
    try:
        user_id = current_user["user_id"]
        supabase = get_service_client()

        # Insert behavior signal
        supabase.table("behavior_signals") \
            .insert({
                "user_id": user_id,
                "signal_type": request.signal_type,
                "signal_value": request.signal_value,
                "metadata": request.metadata,
                "created_at": datetime.utcnow().isoformat()
            }) \
            .execute()

        logger.info(
            "Behavior signal logged",
            user_id=user_id,
            signal_type=request.signal_type,
            signal_value=request.signal_value
        )

        return BehaviorSignalResponse(
            success=True,
            message="Behavior signal logged successfully"
        )

    except Exception as e:
        logger.error("Failed to log behavior signal", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to log behavior signal"
        )


@router.post(
    "/app-open",
    response_model=BehaviorSignalResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Log app open event",
    description="""
    Log app open event for usage analytics and adaptive dashboard.

    Tracks:
    - When users open the app
    - Time of day patterns
    - Source of app open (notification, widget, direct)
    """
)
async def log_app_open(
    request: AppOpenRequest,
    current_user: dict = Depends(get_current_user)
):
    """Log app open event."""
    try:
        user_id = current_user["user_id"]
        supabase = get_service_client()

        # Insert app open event
        supabase.table("app_opens") \
            .insert({
                "user_id": user_id,
                "source": request.source,
                "time_of_day": request.time_of_day,
                "opened_at": datetime.utcnow().isoformat()
            }) \
            .execute()

        logger.info(
            "App open logged",
            user_id=user_id,
            source=request.source,
            time_of_day=request.time_of_day
        )

        return BehaviorSignalResponse(
            success=True,
            message="App open logged successfully"
        )

    except Exception as e:
        logger.error("Failed to log app open", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to log app open"
        )


@router.put(
    "/preference",
    response_model=PreferenceUpdateResponse,
    summary="Update dashboard preference",
    description="""
    Update user's dashboard variant preference.

    Variants:
    - simple: Minimalist, next-action focused
    - balanced: Overview with key metrics (default)
    - detailed: Full analytics and trends
    """
)
async def update_dashboard_preference(
    request: DashboardPreferenceRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update user's dashboard preference."""
    try:
        user_id = current_user["user_id"]
        supabase = get_service_client()

        # Update profile
        supabase.table("profiles") \
            .update({"dashboard_preference": request.preference}) \
            .eq("id", user_id) \
            .execute()

        logger.info(
            "Dashboard preference updated",
            user_id=user_id,
            new_preference=request.preference
        )

        return PreferenceUpdateResponse(
            success=True,
            new_preference=request.preference
        )

    except Exception as e:
        logger.error("Failed to update dashboard preference", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update dashboard preference"
        )
