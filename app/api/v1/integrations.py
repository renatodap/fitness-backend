"""
Integration API Endpoints

This module provides Garmin Connect integration using the garminconnect library
for comprehensive health data sync.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field

from app.api.middleware.auth import get_current_user
from app.services.garmin_sync_service import GarminSyncService

router = APIRouter()


class GarminTestRequest(BaseModel):
    """Request to test Garmin connection."""
    email: str = Field(..., description="Garmin Connect email")
    password: str = Field(..., description="Garmin Connect password")


class GarminSyncRequest(BaseModel):
    """Request to sync Garmin health data."""
    email: str = Field(..., description="Garmin Connect email")
    password: str = Field(..., description="Garmin Connect password")
    days_back: int = Field(
        default=7,
        ge=1,
        le=90,
        description="Number of days to sync (1-90)"
    )


@router.post("/garmin/test")
async def test_garmin(
    request: GarminTestRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Test Garmin Connect connection.

    Authenticates with Garmin and verifies connectivity.
    """
    try:
        service = GarminSyncService()

        result = await service.test_connection(
            email=request.email,
            password=request.password
        )

        if not result["success"]:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=result["message"]
            )

        return result

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to test Garmin connection: {str(e)}"
        )


@router.post("/garmin/sync")
async def sync_garmin(
    request: GarminSyncRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Sync all health data from Garmin Connect.

    Syncs the following data types:
    - Sleep tracking (duration, stages, quality, HRV)
    - HRV logs (morning heart rate variability)
    - Stress tracking (daily stress levels)
    - Body Battery (energy reserves)
    - Daily steps & activity
    - Training load & status
    - Daily readiness (calculated from all factors)

    All data is synced to Supabase for cloud access.
    """
    try:
        service = GarminSyncService()

        # Sync all health data
        result = await service.sync_all_health_data(
            user_id=user_id,
            email=request.email,
            password=request.password,
            days_back=request.days_back
        )

        return result

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to sync Garmin data: {str(e)}"
        )
