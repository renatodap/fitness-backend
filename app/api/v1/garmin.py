"""
Garmin Connect Integration API Endpoints

Provides endpoints for:
- Testing Garmin connection
- Syncing health data (sleep, HRV, readiness, etc.)
- Manual entry for non-Garmin users
- Health metrics retrieval
"""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any

from app.api.v1.dependencies import get_current_user
from app.services.garmin_sync_service import GarminSyncService
from app.models.requests.garmin_requests import (
    GarminConnectionTestRequest,
    GarminSyncRequest,
    ManualSleepEntryRequest,
    ManualReadinessCheckInRequest
)
from app.models.responses.garmin_responses import (
    GarminConnectionTestResponse,
    GarminSyncResponse,
    SleepLogResponse,
    ReadinessResponse
)

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/garmin", tags=["garmin"])


@router.post(
    "/test-connection",
    response_model=GarminConnectionTestResponse,
    summary="Test Garmin Connect connection",
    description="""
    Test connection to Garmin Connect with user credentials.

    This endpoint:
    - Validates Garmin email and password
    - Tests API authentication
    - Returns user profile info if successful

    **Does not** store credentials or sync data - just tests connection.
    """,
    responses={
        200: {"description": "Connection successful"},
        400: {"description": "Invalid credentials"},
        500: {"description": "Connection failed"}
    }
)
async def test_garmin_connection(
    request: GarminConnectionTestRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Test Garmin Connect connection."""
    logger.info(f"[Garmin API] Testing connection for user {current_user['user_id']}")

    try:
        garmin_service = GarminSyncService()
        result = await garmin_service.test_connection(request.email, request.password)

        return GarminConnectionTestResponse(**result)

    except Exception as e:
        logger.error(f"[Garmin API] Connection test failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Failed to connect to Garmin: {str(e)}"
        )


@router.post(
    "/sync",
    response_model=GarminSyncResponse,
    summary="Sync health data from Garmin Connect",
    description="""
    Sync comprehensive health data from Garmin Connect.

    Syncs the following data types:
    - Sleep tracking (duration, stages, quality, HRV during sleep)
    - HRV logs (morning heart rate variability)
    - Stress tracking (daily stress levels)
    - Body Battery (energy reserves)
    - Daily steps & activity (move IQ, intensity minutes)
    - Training load & status (acute/chronic load, TSS)
    - Daily readiness (calculated from all factors)

    **Rate limit**: 10 syncs per hour per user

    **Processing time**: 10-30 seconds for 7 days of data
    """,
    responses={
        200: {"description": "Sync successful"},
        400: {"description": "Invalid request or credentials"},
        429: {"description": "Rate limit exceeded"},
        500: {"description": "Sync failed"}
    }
)
async def sync_garmin_data(
    request: GarminSyncRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Sync all health data from Garmin Connect."""
    user_id = current_user["user_id"]

    logger.info(f"[Garmin API] Starting sync for user {user_id}, days_back={request.days_back}")

    try:
        garmin_service = GarminSyncService()

        # Sync all health data
        result = await garmin_service.sync_all_health_data(
            user_id=user_id,
            email=request.email,
            password=request.password,
            days_back=request.days_back
        )

        logger.info(
            f"[Garmin API] Sync complete for user {user_id}: "
            f"{result['total_synced']} records synced, {result['total_errors']} errors"
        )

        # Convert nested dicts to Pydantic models
        return GarminSyncResponse(**result)

    except Exception as e:
        logger.error(f"[Garmin API] Sync failed for user {user_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync Garmin data: {str(e)}"
        )


@router.post(
    "/manual/sleep",
    response_model=Dict[str, Any],
    summary="Manually log sleep data",
    description="""
    Manually log sleep data for users without Garmin devices.

    This endpoint allows users to:
    - Log sleep duration and quality
    - Track sleep patterns over time
    - Contribute to readiness calculations

    **Manual entry** is used when Garmin auto-sync is not available.
    """
)
async def manual_sleep_entry(
    request: ManualSleepEntryRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Manual sleep entry for non-Garmin users."""
    user_id = current_user["user_id"]

    logger.info(f"[Garmin API] Manual sleep entry for user {user_id}: {request.sleep_date}")

    try:
        from app.services.supabase_service import get_service_client
        supabase = get_service_client()

        # Calculate duration
        from datetime import datetime
        start = datetime.fromisoformat(request.sleep_start.replace("Z", "+00:00"))
        end = datetime.fromisoformat(request.sleep_end.replace("Z", "+00:00"))
        duration_minutes = int((end - start).total_seconds() / 60)

        # Estimate sleep score from quality and duration
        quality_scores = {"poor": 40, "fair": 60, "good": 75, "excellent": 90}
        base_score = quality_scores[request.sleep_quality]

        # Adjust for duration (7-9 hours is optimal)
        duration_hours = duration_minutes / 60
        if 7 <= duration_hours <= 9:
            duration_bonus = 10
        elif 6 <= duration_hours < 7 or 9 < duration_hours <= 10:
            duration_bonus = 5
        else:
            duration_bonus = 0

        sleep_score = min(100, base_score + duration_bonus)

        # Build sleep log
        sleep_log = {
            "user_id": user_id,
            "sleep_date": request.sleep_date,
            "sleep_start": request.sleep_start,
            "sleep_end": request.sleep_end,
            "total_sleep_minutes": duration_minutes,
            "sleep_score": sleep_score,
            "sleep_quality": request.sleep_quality,
            "source": "manual",
            "entry_method": "form",
            "notes": request.notes
        }

        result = supabase.table("sleep_logs").upsert(sleep_log, on_conflict="user_id,sleep_date").execute()

        if not result.data:
            raise Exception("Failed to save sleep log")

        return {
            "success": True,
            "message": "Sleep log saved successfully",
            "data": result.data[0]
        }

    except Exception as e:
        logger.error(f"[Garmin API] Manual sleep entry failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save sleep log: {str(e)}"
        )


@router.post(
    "/manual/readiness",
    response_model=Dict[str, Any],
    summary="Morning readiness check-in",
    description="""
    Morning check-in for daily readiness assessment.

    This endpoint:
    - Collects subjective readiness factors (energy, soreness, stress, mood)
    - Combines with objective data (sleep, HRV) if available
    - Calculates daily readiness score
    - Provides training recommendations

    **Best practice**: Complete check-in within 1 hour of waking up.
    """
)
async def manual_readiness_checkin(
    request: ManualReadinessCheckInRequest,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Morning check-in for readiness."""
    user_id = current_user["user_id"]

    logger.info(f"[Garmin API] Readiness check-in for user {user_id}")

    try:
        from app.services.supabase_service import get_service_client
        from datetime import date

        supabase = get_service_client()
        today = date.today().isoformat()

        # Calculate readiness score from subjective factors
        readiness_score = 50  # Start at neutral

        # Energy contributes 25% (scale: 1-10 → -15 to +15)
        readiness_score += (request.energy_level - 5.5) * 3

        # Soreness contributes 20% (scale: 0-10 → 0 to -20)
        readiness_score -= (request.soreness_level * 2)

        # Stress contributes 20% (scale: 0-10 → 0 to -20)
        readiness_score -= (request.stress_level * 2)

        # Mood contributes 20% (scale: terrible to amazing)
        mood_scores = {"terrible": -15, "bad": -7, "okay": 0, "good": 10, "amazing": 20}
        readiness_score += mood_scores[request.mood]

        # Motivation contributes 15% (scale: 1-10 → -7 to +8)
        readiness_score += (request.motivation_level - 5) * 1.5

        # Clamp to 0-100
        readiness_score = max(0, min(100, int(readiness_score)))

        # Determine status
        if readiness_score >= 80:
            readiness_status = "optimal"
        elif readiness_score >= 65:
            readiness_status = "high"
        elif readiness_score >= 50:
            readiness_status = "balanced"
        elif readiness_score >= 35:
            readiness_status = "low"
        else:
            readiness_status = "poor"

        # Try to get sleep score from today's sleep log
        sleep_query = supabase.table("sleep_logs") \
            .select("sleep_score") \
            .eq("user_id", user_id) \
            .eq("sleep_date", today) \
            .execute()

        sleep_score = sleep_query.data[0]["sleep_score"] if sleep_query.data else None

        # Build readiness record
        readiness_log = {
            "user_id": user_id,
            "date": today,
            "readiness_score": readiness_score,
            "readiness_status": readiness_status,
            "sleep_score": sleep_score,
            "energy_level": request.energy_level,
            "soreness_level": request.soreness_level,
            "stress_level": request.stress_level,
            "mood": request.mood,
            "motivation_level": request.motivation_level,
            "calculation_method": "manual_partial" if sleep_score else "manual_full",
            "factors_used": {
                "energy": request.energy_level,
                "soreness": request.soreness_level,
                "stress": request.stress_level,
                "mood": request.mood,
                "motivation": request.motivation_level
            }
        }

        result = supabase.table("daily_readiness").upsert(readiness_log, on_conflict="user_id,date").execute()

        if not result.data:
            raise Exception("Failed to save readiness check-in")

        return {
            "success": True,
            "message": "Readiness check-in saved successfully",
            "data": result.data[0],
            "recommendation": _get_readiness_recommendation(readiness_status, readiness_score)
        }

    except Exception as e:
        logger.error(f"[Garmin API] Readiness check-in failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save readiness check-in: {str(e)}"
        )


@router.get(
    "/health-summary",
    summary="Get health metrics summary",
    description="""
    Get summary of all health metrics for a date range.

    Returns:
    - Aggregated stats (avg sleep, avg readiness, total steps, etc.)
    - Data counts for each metric type
    - Trends and insights
    """
)
async def get_health_summary(
    days: int = 7,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """Get health metrics summary."""
    user_id = current_user["user_id"]

    try:
        from app.services.supabase_service import get_service_client
        from datetime import date, timedelta

        supabase = get_service_client()

        end_date = date.today()
        start_date = end_date - timedelta(days=days)

        # Query all metrics
        sleep_query = supabase.table("sleep_logs") \
            .select("total_sleep_minutes, sleep_score") \
            .eq("user_id", user_id) \
            .gte("sleep_date", start_date.isoformat()) \
            .lte("sleep_date", end_date.isoformat()) \
            .execute()

        readiness_query = supabase.table("daily_readiness") \
            .select("readiness_score") \
            .eq("user_id", user_id) \
            .gte("date", start_date.isoformat()) \
            .lte("date", end_date.isoformat()) \
            .execute()

        steps_query = supabase.table("daily_steps_and_activity") \
            .select("total_steps") \
            .eq("user_id", user_id) \
            .gte("date", start_date.isoformat()) \
            .lte("date", end_date.isoformat()) \
            .execute()

        # Calculate averages
        sleep_data = sleep_query.data if sleep_query.data else []
        readiness_data = readiness_query.data if readiness_query.data else []
        steps_data = steps_query.data if steps_query.data else []

        avg_sleep_hours = sum(s["total_sleep_minutes"] for s in sleep_data) / len(sleep_data) / 60 if sleep_data else None
        avg_sleep_score = sum(s["sleep_score"] for s in sleep_data if s.get("sleep_score")) / len([s for s in sleep_data if s.get("sleep_score")]) if sleep_data else None
        avg_readiness = sum(r["readiness_score"] for r in readiness_data) / len(readiness_data) if readiness_data else None
        total_steps = sum(s["total_steps"] for s in steps_data) if steps_data else None

        return {
            "user_id": user_id,
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "sleep_data_count": len(sleep_data),
            "readiness_data_count": len(readiness_data),
            "steps_data_count": len(steps_data),
            "avg_sleep_hours": round(avg_sleep_hours, 1) if avg_sleep_hours else None,
            "avg_sleep_score": round(avg_sleep_score, 1) if avg_sleep_score else None,
            "avg_readiness_score": round(avg_readiness, 1) if avg_readiness else None,
            "total_steps": total_steps
        }

    except Exception as e:
        logger.error(f"[Garmin API] Health summary failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to get health summary: {str(e)}"
        )


def _get_readiness_recommendation(status: str, score: int) -> str:
    """Get training recommendation based on readiness."""
    if status == "optimal":
        return "You're in peak condition! Great day for high-intensity training or challenging workouts."
    elif status == "high":
        return "Good readiness! You can handle moderate to high intensity today. Listen to your body."
    elif status == "balanced":
        return "Moderate readiness. Consider medium intensity workouts or active recovery."
    elif status == "low":
        return "Low readiness. Focus on light activity, stretching, or mobility work today."
    else:
        return "Poor readiness. Prioritize rest and recovery today. Light walking or gentle yoga at most."
