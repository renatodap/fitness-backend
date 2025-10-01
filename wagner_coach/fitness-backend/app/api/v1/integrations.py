"""
Integration API Endpoints
"""

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.middleware.auth import get_current_user
from app.services.garmin_service import GarminService

router = APIRouter()


class GarminTestRequest(BaseModel):
    """Request to test Garmin connection."""
    email: str
    password: str


class GarminSyncRequest(BaseModel):
    """Request to sync Garmin activities."""
    email: str
    password: str
    days_back: int = 30


@router.post("/garmin/test")
async def test_garmin(
    request: GarminTestRequest,
    user_id: str = Depends(get_current_user)
):
    """Test Garmin Connect connection."""
    service = GarminService()

    result = await service.test_connection(
        email=request.email,
        password=request.password
    )

    return result


@router.post("/garmin/sync")
async def sync_garmin(
    request: GarminSyncRequest,
    user_id: str = Depends(get_current_user)
):
    """Sync activities from Garmin Connect."""
    service = GarminService()

    result = await service.sync_activities(
        user_id=user_id,
        email=request.email,
        password=request.password,
        days_back=request.days_back
    )

    return result
