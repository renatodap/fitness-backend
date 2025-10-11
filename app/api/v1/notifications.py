"""
Notifications API endpoints for adaptive notification system.

This module provides endpoints for:
- Analyzing user behavior patterns for notification suggestions
- Managing notification schedules
- Getting notification recommendations
- Tracking notification engagement
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field, validator
from datetime import datetime, time, timedelta, date
from typing import Optional, List, Literal
from collections import defaultdict
import structlog

from app.api.v1.dependencies import get_current_user
from app.services.supabase_service import get_supabase_client

logger = structlog.get_logger()

router = APIRouter(prefix="/notifications", tags=["notifications"])


# ==================== Request Models ====================

class CreateNotificationScheduleRequest(BaseModel):
    """Request model for creating notification schedule."""
    enabled: bool = Field(True, description="Whether notifications are enabled")
    notification_time: str = Field(..., description="Time in HH:MM format (e.g., '07:00')")
    timezone: str = Field("UTC", description="User's timezone")
    days_of_week: List[int] = Field(default=[1, 2, 3, 4, 5, 6, 7], description="Days of week (1=Mon, 7=Sun)")
    notification_type: Literal["daily_reminder", "meal_reminder", "workout_reminder", "custom"] = Field(
        "daily_reminder",
        description="Type of notification"
    )
    message_template: Optional[str] = Field(None, description="Custom message template")

    @validator("notification_time")
    def validate_time_format(cls, v):
        """Validate time format HH:MM."""
        try:
            time.fromisoformat(v + ":00")
            return v
        except ValueError:
            raise ValueError("Time must be in HH:MM format (e.g., '07:00')")

    @validator("days_of_week")
    def validate_days(cls, v):
        """Validate days are 1-7."""
        if not all(1 <= day <= 7 for day in v):
            raise ValueError("Days must be between 1 (Monday) and 7 (Sunday)")
        return v


class UpdateNotificationScheduleRequest(BaseModel):
    """Request model for updating notification schedule."""
    enabled: Optional[bool] = None
    notification_time: Optional[str] = None
    timezone: Optional[str] = None
    days_of_week: Optional[List[int]] = None
    notification_type: Optional[str] = None
    message_template: Optional[str] = None


class NotificationEngagementRequest(BaseModel):
    """Request model for tracking notification engagement."""
    notification_log_id: str = Field(..., description="Notification log ID")
    action_taken: str = Field(..., description="Action taken (e.g., 'logged_meal', 'opened_dashboard', 'dismissed')")


# ==================== Response Models ====================

class NotificationScheduleResponse(BaseModel):
    """Response model for notification schedule."""
    id: str
    user_id: str
    enabled: bool
    notification_time: str
    timezone: str
    days_of_week: List[int]
    notification_type: str
    message_template: Optional[str]
    is_auto_detected: bool
    detection_confidence: float
    pattern_frequency: int
    last_sent_at: Optional[str]
    created_at: str
    updated_at: str


class NotificationPattern(BaseModel):
    """Detected user behavior pattern."""
    pattern_type: str
    time_bucket: str
    frequency: int
    confidence: float
    recommended_time: str
    recommendation_reason: str


class NotificationRecommendationResponse(BaseModel):
    """Response with notification recommendations."""
    has_recommendation: bool
    pattern: Optional[NotificationPattern]
    message: str


class NotificationAnalysisResponse(BaseModel):
    """Response with complete notification analysis."""
    patterns_detected: List[NotificationPattern]
    current_schedule: Optional[NotificationScheduleResponse]
    recommendation: Optional[NotificationPattern]
    analysis_period_days: int


# ==================== Helper Functions ====================

async def analyze_app_open_patterns(user_id: str, days: int = 14) -> List[NotificationPattern]:
    """
    Analyze app_opens table to find consistent time patterns.

    Args:
        user_id: User's unique identifier
        days: Number of days to analyze (default 14)

    Returns:
        List of detected patterns with confidence scores
    """
    try:
        supabase = await get_supabase_client()

        # Get app opens for last N days
        start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()

        response = await supabase.table("app_opens") \
            .select("opened_at, time_of_day") \
            .eq("user_id", user_id) \
            .gte("opened_at", start_date) \
            .order("opened_at", desc=False) \
            .execute()

        if not response.data:
            return []

        # Group by 30-minute time buckets
        time_buckets = defaultdict(int)

        for open_event in response.data:
            opened_at = datetime.fromisoformat(open_event["opened_at"].replace("Z", "+00:00"))
            hour = opened_at.hour
            minute_bucket = (opened_at.minute // 30) * 30
            bucket_key = f"{hour:02d}:{minute_bucket:02d}-{hour:02d}:{minute_bucket + 30:02d}"
            time_buckets[bucket_key] += 1

        # Find patterns with frequency >= 10 (70% of days in 2 weeks)
        patterns = []
        threshold = max(10, int(days * 0.7))

        for time_bucket, frequency in time_buckets.items():
            if frequency >= threshold:
                # Calculate confidence (frequency / days analyzed)
                confidence = min(1.0, frequency / days)

                # Recommended time is 5 minutes before bucket start
                bucket_start = time_bucket.split("-")[0]
                hour, minute = map(int, bucket_start.split(":"))
                recommended_time = datetime(2000, 1, 1, hour, minute) - timedelta(minutes=5)

                patterns.append(NotificationPattern(
                    pattern_type="app_open_pattern",
                    time_bucket=time_bucket,
                    frequency=frequency,
                    confidence=confidence,
                    recommended_time=recommended_time.strftime("%H:%M"),
                    recommendation_reason=f"You opened the app {frequency} times during this window in the last {days} days"
                ))

        # Sort by confidence (highest first)
        patterns.sort(key=lambda p: p.confidence, reverse=True)

        return patterns

    except Exception as e:
        logger.error("Failed to analyze app open patterns", user_id=user_id, error=str(e))
        return []


async def analyze_meal_log_patterns(user_id: str, days: int = 14) -> List[NotificationPattern]:
    """
    Analyze meal_logs table to find consistent meal logging times.

    Args:
        user_id: User's unique identifier
        days: Number of days to analyze (default 14)

    Returns:
        List of detected meal logging patterns
    """
    try:
        supabase = await get_supabase_client()

        # Get meal logs for last N days
        start_date = (datetime.utcnow() - timedelta(days=days)).isoformat()

        response = await supabase.table("meal_logs") \
            .select("logged_at, meal_type") \
            .eq("user_id", user_id) \
            .gte("logged_at", start_date) \
            .order("logged_at", desc=False) \
            .execute()

        if not response.data:
            return []

        # Group breakfast logs by 30-minute time buckets
        breakfast_buckets = defaultdict(int)

        for meal in response.data:
            if meal["meal_type"] == "breakfast":
                logged_at = datetime.fromisoformat(meal["logged_at"].replace("Z", "+00:00"))
                hour = logged_at.hour
                minute_bucket = (logged_at.minute // 30) * 30
                bucket_key = f"{hour:02d}:{minute_bucket:02d}-{hour:02d}:{minute_bucket + 30:02d}"
                breakfast_buckets[bucket_key] += 1

        # Find patterns
        patterns = []
        threshold = max(7, int(days * 0.5))

        for time_bucket, frequency in breakfast_buckets.items():
            if frequency >= threshold:
                confidence = min(1.0, frequency / days)

                # Recommended time is 15 minutes before average breakfast time
                bucket_start = time_bucket.split("-")[0]
                hour, minute = map(int, bucket_start.split(":"))
                recommended_time = datetime(2000, 1, 1, hour, minute) - timedelta(minutes=15)

                patterns.append(NotificationPattern(
                    pattern_type="meal_log_pattern",
                    time_bucket=time_bucket,
                    frequency=frequency,
                    confidence=confidence,
                    recommended_time=recommended_time.strftime("%H:%M"),
                    recommendation_reason=f"You logged breakfast {frequency} times during this window. Reminder 15 min before?"
                ))

        patterns.sort(key=lambda p: p.confidence, reverse=True)

        return patterns

    except Exception as e:
        logger.error("Failed to analyze meal log patterns", user_id=user_id, error=str(e))
        return []


# ==================== Endpoints ====================

@router.get(
    "/analyze",
    response_model=NotificationAnalysisResponse,
    summary="Analyze user patterns for notification recommendations",
    description="""
    Analyze user's behavior patterns to recommend notification times.

    Analyzes:
    - App open patterns (consistent times user opens app)
    - Meal logging patterns (consistent breakfast/meal times)

    Returns recommendations with confidence scores.
    """
)
async def analyze_notification_patterns(
    days: int = 14,
    current_user: dict = Depends(get_current_user)
):
    """Analyze user behavior patterns for notification recommendations."""
    try:
        user_id = current_user["user_id"]

        # Analyze patterns
        app_open_patterns = await analyze_app_open_patterns(user_id, days)
        meal_log_patterns = await analyze_meal_log_patterns(user_id, days)

        all_patterns = app_open_patterns + meal_log_patterns

        # Get current schedule
        supabase = await get_supabase_client()
        schedule_response = await supabase.table("notification_schedules") \
            .select("*") \
            .eq("user_id", user_id) \
            .limit(1) \
            .execute()

        current_schedule = None
        if schedule_response.data:
            sched = schedule_response.data[0]
            current_schedule = NotificationScheduleResponse(
                id=sched["id"],
                user_id=sched["user_id"],
                enabled=sched["enabled"],
                notification_time=str(sched["notification_time"]),
                timezone=sched["timezone"],
                days_of_week=sched["days_of_week"],
                notification_type=sched["notification_type"],
                message_template=sched.get("message_template"),
                is_auto_detected=sched["is_auto_detected"],
                detection_confidence=sched["detection_confidence"],
                pattern_frequency=sched["pattern_frequency"],
                last_sent_at=sched.get("last_sent_at"),
                created_at=sched["created_at"],
                updated_at=sched["updated_at"]
            )

        # Top recommendation (highest confidence)
        recommendation = all_patterns[0] if all_patterns else None

        return NotificationAnalysisResponse(
            patterns_detected=all_patterns,
            current_schedule=current_schedule,
            recommendation=recommendation,
            analysis_period_days=days
        )

    except Exception as e:
        logger.error("Failed to analyze notification patterns", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to analyze notification patterns"
        )


@router.post(
    "/schedule",
    response_model=NotificationScheduleResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Create notification schedule",
    description="""
    Create a new notification schedule.

    Can be manually created or based on auto-detected patterns.
    """
)
async def create_notification_schedule(
    request: CreateNotificationScheduleRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create notification schedule."""
    try:
        user_id = current_user["user_id"]
        supabase = await get_supabase_client()

        # Check if schedule already exists
        existing = await supabase.table("notification_schedules") \
            .select("id") \
            .eq("user_id", user_id) \
            .execute()

        if existing.data:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Notification schedule already exists. Use PUT to update."
            )

        # Create schedule
        response = await supabase.table("notification_schedules") \
            .insert({
                "user_id": user_id,
                "enabled": request.enabled,
                "notification_time": request.notification_time + ":00",
                "timezone": request.timezone,
                "days_of_week": request.days_of_week,
                "notification_type": request.notification_type,
                "message_template": request.message_template,
                "is_auto_detected": False,  # Manual creation
                "detection_confidence": 0.0,
                "pattern_frequency": 0
            }) \
            .execute()

        schedule = response.data[0]

        logger.info(
            "Notification schedule created",
            user_id=user_id,
            notification_time=request.notification_time
        )

        return NotificationScheduleResponse(
            id=schedule["id"],
            user_id=schedule["user_id"],
            enabled=schedule["enabled"],
            notification_time=str(schedule["notification_time"]),
            timezone=schedule["timezone"],
            days_of_week=schedule["days_of_week"],
            notification_type=schedule["notification_type"],
            message_template=schedule.get("message_template"),
            is_auto_detected=schedule["is_auto_detected"],
            detection_confidence=schedule["detection_confidence"],
            pattern_frequency=schedule["pattern_frequency"],
            last_sent_at=schedule.get("last_sent_at"),
            created_at=schedule["created_at"],
            updated_at=schedule["updated_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to create notification schedule", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create notification schedule"
        )


@router.get(
    "/schedule",
    response_model=Optional[NotificationScheduleResponse],
    summary="Get notification schedule",
    description="Get user's current notification schedule."
)
async def get_notification_schedule(
    current_user: dict = Depends(get_current_user)
):
    """Get notification schedule."""
    try:
        user_id = current_user["user_id"]
        supabase = await get_supabase_client()

        response = await supabase.table("notification_schedules") \
            .select("*") \
            .eq("user_id", user_id) \
            .limit(1) \
            .execute()

        if not response.data:
            return None

        schedule = response.data[0]

        return NotificationScheduleResponse(
            id=schedule["id"],
            user_id=schedule["user_id"],
            enabled=schedule["enabled"],
            notification_time=str(schedule["notification_time"]),
            timezone=schedule["timezone"],
            days_of_week=schedule["days_of_week"],
            notification_type=schedule["notification_type"],
            message_template=schedule.get("message_template"),
            is_auto_detected=schedule["is_auto_detected"],
            detection_confidence=schedule["detection_confidence"],
            pattern_frequency=schedule["pattern_frequency"],
            last_sent_at=schedule.get("last_sent_at"),
            created_at=schedule["created_at"],
            updated_at=schedule["updated_at"]
        )

    except Exception as e:
        logger.error("Failed to get notification schedule", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to get notification schedule"
        )


@router.put(
    "/schedule",
    response_model=NotificationScheduleResponse,
    summary="Update notification schedule",
    description="Update user's notification schedule."
)
async def update_notification_schedule(
    request: UpdateNotificationScheduleRequest,
    current_user: dict = Depends(get_current_user)
):
    """Update notification schedule."""
    try:
        user_id = current_user["user_id"]
        supabase = await get_supabase_client()

        # Build update dict (only non-None values)
        update_data = {}
        if request.enabled is not None:
            update_data["enabled"] = request.enabled
        if request.notification_time is not None:
            update_data["notification_time"] = request.notification_time + ":00"
        if request.timezone is not None:
            update_data["timezone"] = request.timezone
        if request.days_of_week is not None:
            update_data["days_of_week"] = request.days_of_week
        if request.notification_type is not None:
            update_data["notification_type"] = request.notification_type
        if request.message_template is not None:
            update_data["message_template"] = request.message_template

        # Update
        response = await supabase.table("notification_schedules") \
            .update(update_data) \
            .eq("user_id", user_id) \
            .execute()

        if not response.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Notification schedule not found. Create one first."
            )

        schedule = response.data[0]

        logger.info(
            "Notification schedule updated",
            user_id=user_id,
            changes=update_data
        )

        return NotificationScheduleResponse(
            id=schedule["id"],
            user_id=schedule["user_id"],
            enabled=schedule["enabled"],
            notification_time=str(schedule["notification_time"]),
            timezone=schedule["timezone"],
            days_of_week=schedule["days_of_week"],
            notification_type=schedule["notification_type"],
            message_template=schedule.get("message_template"),
            is_auto_detected=schedule["is_auto_detected"],
            detection_confidence=schedule["detection_confidence"],
            pattern_frequency=schedule["pattern_frequency"],
            last_sent_at=schedule.get("last_sent_at"),
            created_at=schedule["created_at"],
            updated_at=schedule["updated_at"]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error("Failed to update notification schedule", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to update notification schedule"
        )


@router.delete(
    "/schedule",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete notification schedule",
    description="Delete user's notification schedule."
)
async def delete_notification_schedule(
    current_user: dict = Depends(get_current_user)
):
    """Delete notification schedule."""
    try:
        user_id = current_user["user_id"]
        supabase = await get_supabase_client()

        await supabase.table("notification_schedules") \
            .delete() \
            .eq("user_id", user_id) \
            .execute()

        logger.info("Notification schedule deleted", user_id=user_id)

    except Exception as e:
        logger.error("Failed to delete notification schedule", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete notification schedule"
        )
