"""
Activity Logging Service

Handles all activity CRUD operations with database integration.
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone

from app.services.supabase_service import get_service_client
from app.activity_config.activity_types import get_activity_type_config, get_all_activity_types

logger = logging.getLogger(__name__)


class ActivityLoggingService:
    """Service for activity logging operations"""

    def __init__(self):
        self.supabase = get_service_client()

    async def create_activity(
        self,
        user_id: str,
        activity_data: dict
    ) -> dict:
        """
        Create a new activity log.

        Args:
            user_id: User's unique identifier
            activity_data: Activity data from request

        Returns:
            Created activity with ID

        Raises:
            ValueError: If activity type not supported or required fields missing
            Exception: If database operation fails
        """
        # Validate activity type
        activity_type = activity_data.get("activity_type")
        config = get_activity_type_config(activity_type)

        if not config:
            raise ValueError(f"Unsupported activity type: {activity_type}")

        # Validate required fields
        self._validate_required_fields(activity_data, config)

        # Prepare activity record
        activity_record = self._prepare_activity_record(user_id, activity_data)

        try:
            # Insert activity
            response = self.supabase.table("activities").insert(activity_record).execute()

            if not response.data or len(response.data) == 0:
                raise Exception("Failed to create activity")

            activity = response.data[0]

            # If strength training with exercises, create exercise records
            if config.supports_exercises and "exercises" in activity_data:
                await self._create_activity_exercises(
                    activity["id"],
                    activity_data["exercises"]
                )
                # Reload activity with exercises
                activity = await self.get_activity(user_id, activity["id"])

            logger.info(f"Created activity {activity['id']} for user {user_id}")
            return activity

        except Exception as e:
            logger.error(f"Failed to create activity: {e}")
            raise

    async def get_activity(
        self,
        user_id: str,
        activity_id: str
    ) -> dict:
        """
        Get a single activity by ID.

        Args:
            user_id: User's unique identifier
            activity_id: Activity ID

        Returns:
            Activity data with exercises if applicable

        Raises:
            ValueError: If activity not found or doesn't belong to user
        """
        try:
            # Fetch activity
            response = self.supabase.table("activities") \
                .select("*") \
                .eq("id", activity_id) \
                .eq("user_id", user_id) \
                .single() \
                .execute()

            if not response.data:
                raise ValueError(f"Activity {activity_id} not found")

            activity = response.data

            # Fetch exercises if strength training
            if activity.get("activity_type") in ["strength_training", "crossfit", "workout"]:
                exercises = await self._get_activity_exercises(activity_id)
                activity["exercises"] = exercises
            else:
                activity["exercises"] = []

            return activity

        except Exception as e:
            logger.error(f"Failed to get activity {activity_id}: {e}")
            raise

    async def get_activities(
        self,
        user_id: str,
        activity_type: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        source: Optional[str] = None,
        limit: int = 50,
        offset: int = 0
    ) -> Dict[str, Any]:
        """
        Get user's activities with filters and pagination.

        Args:
            user_id: User's unique identifier
            activity_type: Filter by activity type
            start_date: Filter activities after this date (ISO format)
            end_date: Filter activities before this date (ISO format)
            source: Filter by source (manual, quick_entry, strava, etc.)
            limit: Maximum number of results
            offset: Pagination offset

        Returns:
            Dictionary with activities list and pagination info
        """
        try:
            # Build query
            query = self.supabase.table("activities") \
                .select("*", count="exact") \
                .eq("user_id", user_id)

            # Apply filters
            if activity_type:
                query = query.eq("activity_type", activity_type)

            if source:
                query = query.eq("source", source)

            if start_date:
                query = query.gte("start_date", start_date)

            if end_date:
                query = query.lte("start_date", end_date)

            # Order and paginate
            query = query.order("start_date", desc=True) \
                .range(offset, offset + limit - 1)

            response = query.execute()

            activities = response.data or []
            total = response.count or 0

            return {
                "activities": activities,
                "total": total,
                "limit": limit,
                "offset": offset
            }

        except Exception as e:
            logger.error(f"Failed to get activities: {e}")
            raise

    async def update_activity(
        self,
        user_id: str,
        activity_id: str,
        update_data: dict
    ) -> dict:
        """
        Update an existing activity.

        Args:
            user_id: User's unique identifier
            activity_id: Activity ID
            update_data: Fields to update

        Returns:
            Updated activity

        Raises:
            ValueError: If activity not found or doesn't belong to user
        """
        try:
            # Verify ownership
            await self.get_activity(user_id, activity_id)

            # Add updated_at timestamp
            update_data["updated_at"] = datetime.now(timezone.utc).isoformat()

            # Update activity
            response = self.supabase.table("activities") \
                .update(update_data) \
                .eq("id", activity_id) \
                .eq("user_id", user_id) \
                .execute()

            if not response.data or len(response.data) == 0:
                raise ValueError(f"Failed to update activity {activity_id}")

            logger.info(f"Updated activity {activity_id}")

            # Return updated activity with exercises
            return await self.get_activity(user_id, activity_id)

        except Exception as e:
            logger.error(f"Failed to update activity {activity_id}: {e}")
            raise

    async def delete_activity(
        self,
        user_id: str,
        activity_id: str
    ) -> bool:
        """
        Delete an activity.

        Args:
            user_id: User's unique identifier
            activity_id: Activity ID

        Returns:
            True if deleted successfully

        Raises:
            ValueError: If activity not found or doesn't belong to user
        """
        try:
            # Verify ownership
            await self.get_activity(user_id, activity_id)

            # Delete activity (cascade will delete related exercises/sets)
            response = self.supabase.table("activities") \
                .delete() \
                .eq("id", activity_id) \
                .eq("user_id", user_id) \
                .execute()

            logger.info(f"Deleted activity {activity_id}")
            return True

        except Exception as e:
            logger.error(f"Failed to delete activity {activity_id}: {e}")
            raise

    async def get_activity_types_config(self) -> dict:
        """
        Get all activity type configurations for frontend form generation.

        Returns:
            Dictionary of activity type configs
        """
        configs = get_all_activity_types()
        return {
            "activity_types": {
                k: v.to_dict() for k, v in configs.items()
            }
        }

    # ========================================================================
    # PRIVATE HELPER METHODS
    # ========================================================================

    def _validate_required_fields(self, activity_data: dict, config) -> None:
        """Validate that all required fields are present"""
        for field in config.primary_fields:
            if field.required and field.name not in activity_data:
                raise ValueError(f"Missing required field: {field.name}")

    def _prepare_activity_record(self, user_id: str, activity_data: dict) -> dict:
        """Prepare activity record for database insertion"""
        # Start with user_id
        record = {
            "user_id": user_id,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "updated_at": datetime.now(timezone.utc).isoformat()
        }

        # Map request fields to database columns
        field_mapping = {
            # Core fields
            "activity_type": "activity_type",
            "sport_type": "sport_type",
            "name": "name",
            "start_date": "start_date",
            "end_date": "end_date",
            "timezone": "timezone",
            "elapsed_time_seconds": "elapsed_time_seconds",
            "duration_minutes": "duration_minutes",

            # Cardio
            "distance_meters": "distance_meters",
            "average_speed": "average_speed",
            "max_speed": "max_speed",
            "average_pace": "average_pace",

            # Elevation
            "total_elevation_gain": "total_elevation_gain",
            "total_elevation_loss": "total_elevation_loss",
            "elevation_high": "elevation_high",
            "elevation_low": "elevation_low",

            # Heart rate
            "average_heartrate": "average_heartrate",
            "max_heartrate": "max_heartrate",
            "min_heartrate": "min_heartrate",

            # Power
            "average_power": "average_power",
            "max_power": "max_power",
            "normalized_power": "normalized_power",

            # Cadence
            "average_cadence": "average_cadence",
            "max_cadence": "max_cadence",

            # Swimming
            "pool_length": "pool_length",
            "total_strokes": "total_strokes",
            "average_stroke_rate": "average_stroke_rate",
            "average_swolf": "average_swolf",
            "lap_count": "lap_count",

            # Strength
            "total_reps": "total_reps",
            "total_sets": "total_sets",
            "total_weight_lifted_kg": "total_weight_lifted_kg",
            "exercise_count": "exercise_count",

            # Tennis
            "total_shots": "total_shots",
            "forehand_count": "forehand_count",
            "backhand_count": "backhand_count",
            "serve_count": "serve_count",
            "ace_count": "ace_count",
            "winner_count": "winner_count",
            "unforced_error_count": "unforced_error_count",
            "sets_played": "sets_played",
            "games_played": "games_played",

            # Yoga
            "poses_held": "poses_held",
            "average_hold_duration": "average_hold_duration",
            "flexibility_score": "flexibility_score",

            # Calories
            "calories": "calories",
            "active_calories": "active_calories",

            # Subjective
            "perceived_exertion": "perceived_exertion",
            "rpe": "rpe",
            "mood": "mood",
            "energy_level": "energy_level",
            "soreness_level": "soreness_level",
            "workout_rating": "workout_rating",

            # Weather
            "weather_conditions": "weather_conditions",
            "temperature_celsius": "temperature_celsius",
            "humidity_percentage": "humidity_percentage",
            "wind_speed_kmh": "wind_speed_kmh",
            "indoor": "indoor",

            # Location
            "location": "location",
            "route_name": "route_name",
            "city": "city",

            # Notes
            "notes": "notes",
            "private_notes": "private_notes",

            # Metadata
            "tags": "tags",
            "trainer": "trainer",
            "race": "race",
            "workout_type": "workout_type",
            "source": "source",
            "quick_entry_log_id": "quick_entry_log_id",
        }

        # Map all provided fields
        for request_field, db_field in field_mapping.items():
            if request_field in activity_data:
                value = activity_data[request_field]
                # Convert datetime objects to ISO strings
                if isinstance(value, datetime):
                    value = value.isoformat()
                record[db_field] = value

        # Calculate duration_minutes from elapsed_time_seconds if not provided
        if "duration_minutes" not in record and "elapsed_time_seconds" in record:
            record["duration_minutes"] = round(record["elapsed_time_seconds"] / 60)

        # Calculate elapsed_time_seconds from duration_minutes if not provided
        if "elapsed_time_seconds" not in record and "duration_minutes" in record:
            record["elapsed_time_seconds"] = record["duration_minutes"] * 60

        return record

    async def _create_activity_exercises(
        self,
        activity_id: str,
        exercises_data: List[dict]
    ) -> None:
        """Create exercise records for strength training activities"""
        for exercise_data in exercises_data:
            # Create activity_exercise record
            exercise_record = {
                "activity_id": activity_id,
                "exercise_name": exercise_data.get("exercise_name"),
                "order_index": exercise_data.get("order_index", 0),
                "notes": exercise_data.get("notes"),
                "created_at": datetime.now(timezone.utc).isoformat()
            }

            response = self.supabase.table("activity_exercises") \
                .insert(exercise_record) \
                .execute()

            if response.data and len(response.data) > 0:
                exercise_id = response.data[0]["id"]

                # Create sets for this exercise
                if "sets" in exercise_data:
                    await self._create_activity_sets(exercise_id, exercise_data["sets"])

    async def _create_activity_sets(
        self,
        activity_exercise_id: str,
        sets_data: List[dict]
    ) -> None:
        """Create set records for an exercise"""
        for set_data in sets_data:
            set_record = {
                "activity_exercise_id": activity_exercise_id,
                "set_number": set_data.get("set_number"),
                "reps_completed": set_data.get("reps_completed"),
                "weight_lbs": set_data.get("weight_lbs"),
                "weight_kg": set_data.get("weight_kg"),
                "rpe": set_data.get("rpe"),
                "rest_seconds": set_data.get("rest_seconds"),
                "completed": set_data.get("completed", True),
                "notes": set_data.get("notes"),
                "created_at": datetime.now(timezone.utc).isoformat()
            }

            self.supabase.table("activity_sets") \
                .insert(set_record) \
                .execute()

    async def _get_activity_exercises(self, activity_id: str) -> List[dict]:
        """Get all exercises for an activity"""
        try:
            # Fetch exercises
            response = self.supabase.table("activity_exercises") \
                .select("*") \
                .eq("activity_id", activity_id) \
                .order("order_index") \
                .execute()

            exercises = response.data or []

            # Fetch sets for each exercise
            for exercise in exercises:
                sets_response = self.supabase.table("activity_sets") \
                    .select("*") \
                    .eq("activity_exercise_id", exercise["id"]) \
                    .order("set_number") \
                    .execute()

                exercise["sets"] = sets_response.data or []

            return exercises

        except Exception as e:
            logger.error(f"Failed to get activity exercises: {e}")
            return []


# Singleton instance
_activity_logging_service = None


def get_activity_logging_service() -> ActivityLoggingService:
    """Get or create activity logging service instance"""
    global _activity_logging_service
    if _activity_logging_service is None:
        _activity_logging_service = ActivityLoggingService()
    return _activity_logging_service
