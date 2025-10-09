"""
Garmin Service

Garmin Connect integration for activity sync.
"""

import logging
from typing import Any, Dict
from datetime import datetime, timedelta

try:
    from garminconnect import Garmin
    GARMIN_AVAILABLE = True
except ImportError:
    GARMIN_AVAILABLE = False
    logger.warning("garminconnect package not available")

from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


class GarminService:
    """
    Service for Garmin Connect integration.

    Syncs activities, health metrics, and other data from Garmin devices.
    """

    def __init__(self):
        """Initialize with Supabase client."""
        self.supabase = get_service_client()

    async def test_connection(
        self,
        email: str,
        password: str
    ) -> Dict[str, Any]:
        """
        Test Garmin Connect connection.

        Args:
            email: Garmin account email
            password: Garmin account password

        Returns:
            Dict with connection status

        Raises:
            ValueError: If credentials are missing
            Exception: If connection fails
        """
        if not email or not password:
            raise ValueError("Email and password are required")

        if not GARMIN_AVAILABLE:
            raise Exception("garminconnect package not installed")

        try:
            client = Garmin(email, password)
            client.login()

            # Get user profile to verify connection
            profile = client.get_user_summary()

            return {
                "success": True,
                "message": "Successfully connected to Garmin Connect",
                "profile": {
                    "displayName": profile.get("displayName"),
                    "email": email
                }
            }

        except Exception as e:
            logger.error(f"Garmin connection failed: {e}")
            raise Exception(f"Failed to connect to Garmin: {str(e)}")

    async def sync_activities(
        self,
        user_id: str,
        email: str,
        password: str,
        days_back: int = 30
    ) -> Dict[str, Any]:
        """
        Sync activities from Garmin Connect.

        Args:
            user_id: User UUID
            email: Garmin email
            password: Garmin password
            days_back: Number of days to sync

        Returns:
            Dict with sync results
        """
        if not all([user_id, email, password]):
            raise ValueError("All fields are required")

        if not GARMIN_AVAILABLE:
            raise Exception("garminconnect package not installed")

        try:
            client = Garmin(email, password)
            client.login()

            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days_back)

            # Get activities
            activities = client.get_activities_by_date(
                start_date.strftime("%Y-%m-%d"),
                end_date.strftime("%Y-%m-%d")
            )

            # Store activities in database
            stored_count = 0
            for activity in activities:
                try:
                    await self._store_activity(user_id, activity)
                    stored_count += 1
                except Exception as e:
                    logger.error(f"Error storing activity: {e}")

            return {
                "success": True,
                "activities": activities,
                "count": len(activities),
                "stored": stored_count,
                "dateRange": {
                    "start": start_date.strftime("%Y-%m-%d"),
                    "end": end_date.strftime("%Y-%m-%d")
                }
            }

        except Exception as e:
            logger.error(f"Garmin sync failed: {e}")
            raise Exception(f"Failed to sync activities: {str(e)}")

    async def _store_activity(self, user_id: str, activity: Dict[str, Any]) -> None:
        """Store activity in database."""
        activity_data = {
            "user_id": user_id,
            "external_id": activity.get("activityId"),
            "source": "garmin",
            "type": activity.get("activityType", {}).get("typeKey", "unknown"),
            "date": activity.get("startTimeLocal", "").split("T")[0],
            "duration_minutes": (activity.get("duration", 0) / 60) if activity.get("duration") else 0,
            "distance_miles": (activity.get("distance", 0) / 1609.34) if activity.get("distance") else 0,
            "calories": activity.get("calories", 0),
            "elevation_feet": (activity.get("elevationGain", 0) * 3.28084) if activity.get("elevationGain") else 0,
            "raw_data": activity
        }

        # Insert or update
        self.supabase.table("activities").upsert(activity_data).execute()
