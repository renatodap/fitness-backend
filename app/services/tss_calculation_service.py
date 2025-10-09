"""
Training Stress Score (TSS) Calculation Service

Calculates TSS for activities using multiple methods:
1. Heart Rate-based TSS (for activities with HR data from devices)
2. RPE-based TSS (for manual activities with perceived exertion)
3. Activity-specific defaults (for activities without HR or RPE)

TSS Formula:
TSS = (Duration × Intensity² ) / Normalization × 100

Where:
- Duration: Activity duration in hours
- Intensity: Normalized intensity factor (0-1 scale)
- Normalization: Factor to calibrate scores (typically 60 for 1 hour at threshold)

TSS is used for:
- Training load tracking (acute/chronic load ratio)
- Recovery time estimation
- Periodization planning
- Overtraining prevention
"""

import logging
from typing import Optional, Dict, Any
from datetime import datetime

from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


# Activity-specific TSS multipliers
# These adjust TSS based on activity type impact
ACTIVITY_MULTIPLIERS = {
    # High impact activities (1.0 = reference)
    "running": 1.0,
    "trail_run": 1.1,  # More demanding than road running
    "cycling": 1.0,
    "mountain_biking": 1.1,

    # Moderate impact
    "swimming": 0.85,  # Lower impact but still cardio
    "rowing": 0.9,
    "hiking": 0.7,
    "walking": 0.5,

    # Strength and conditioning
    "strength_training": 0.7,  # High effort but shorter duration
    "crossfit": 0.85,
    "hiit": 0.9,

    # Low impact / recovery
    "yoga": 0.3,
    "pilates": 0.4,
    "stretching": 0.2,

    # Sports (variable intensity)
    "tennis": 0.8,
    "soccer": 0.85,
    "basketball": 0.85,
    "climbing": 0.75,

    # Default for unknown activities
    "workout": 0.7,
}


class TSSCalculationService:
    """
    Service for calculating Training Stress Score (TSS) for activities.

    TSS quantifies the training stress of a workout, allowing for:
    - Tracking training load over time
    - Preventing overtraining
    - Planning recovery periods
    - Periodizing training programs
    """

    def __init__(self):
        """Initialize with Supabase client."""
        self.supabase = get_service_client()

    def calculate_tss_from_hr(
        self,
        duration_minutes: int,
        average_hr: int,
        max_hr: Optional[int] = None,
        threshold_hr: Optional[int] = None,
        resting_hr: int = 60
    ) -> int:
        """
        Calculate TSS using heart rate data.

        Uses HR to determine intensity, which is more accurate than RPE for
        activities with continuous HR monitoring (Garmin, Apple Watch, etc.)

        Args:
            duration_minutes: Activity duration in minutes
            average_hr: Average heart rate during activity
            max_hr: Maximum heart rate (defaults to 220 - age)
            threshold_hr: Lactate threshold HR (defaults to 85% of max HR)
            resting_hr: Resting heart rate (default: 60 bpm)

        Returns:
            TSS value (integer)

        Formula:
        Intensity Factor (IF) = (avg_hr - resting_hr) / (threshold_hr - resting_hr)
        TSS = (duration_hours × IF × IF) / normalization × 100
        """
        # Default threshold HR to 85% of max HR (or 170 if no max provided)
        if threshold_hr is None:
            if max_hr:
                threshold_hr = int(max_hr * 0.85)
            else:
                threshold_hr = 170  # Conservative default

        # Calculate intensity factor (IF)
        # IF represents what fraction of threshold intensity the workout was
        hr_range = threshold_hr - resting_hr
        if hr_range <= 0:
            logger.warning(f"[TSS] Invalid HR range: threshold={threshold_hr}, resting={resting_hr}")
            return 0

        intensity_factor = (average_hr - resting_hr) / hr_range

        # Clamp IF between 0.3 and 1.5 (outside this range is unrealistic)
        intensity_factor = max(0.3, min(1.5, intensity_factor))

        # Calculate TSS
        # TSS = (hours × IF²) / normalization × 100
        # Normalization = 1 (one hour at threshold = 100 TSS)
        duration_hours = duration_minutes / 60
        tss = (duration_hours * intensity_factor * intensity_factor) * 100

        result = int(round(tss))

        logger.debug(
            f"[TSS] HR-based: duration={duration_minutes}min, "
            f"avg_hr={average_hr}, threshold_hr={threshold_hr}, "
            f"IF={intensity_factor:.2f}, TSS={result}"
        )

        return result

    def calculate_tss_from_rpe(
        self,
        duration_minutes: int,
        rpe: int,
        activity_type: str = "workout"
    ) -> int:
        """
        Calculate TSS using Rate of Perceived Exertion (RPE).

        For manual activities without HR data, RPE provides a subjective
        intensity measure (1-10 scale).

        Args:
            duration_minutes: Activity duration in minutes
            rpe: Perceived exertion (1-10 scale)
            activity_type: Type of activity (for multiplier)

        Returns:
            TSS value (integer)

        Formula:
        Intensity Factor = 0.5 + (RPE / 20)
        TSS = (duration_hours × IF²) × activity_multiplier × 100
        """
        # Validate RPE range
        if not (1 <= rpe <= 10):
            logger.warning(f"[TSS] Invalid RPE: {rpe}, clamping to 1-10")
            rpe = max(1, min(10, rpe))

        # Map RPE to intensity factor
        # RPE 1-2 → IF 0.50-0.55 (very easy)
        # RPE 5   → IF 0.75 (moderate)
        # RPE 10  → IF 1.00 (maximum)
        intensity_factor = 0.5 + (rpe / 20)

        # Get activity multiplier
        multiplier = ACTIVITY_MULTIPLIERS.get(activity_type.lower(), 0.7)

        # Calculate TSS
        duration_hours = duration_minutes / 60
        tss = (duration_hours * intensity_factor * intensity_factor) * multiplier * 100

        result = int(round(tss))

        logger.debug(
            f"[TSS] RPE-based: duration={duration_minutes}min, RPE={rpe}, "
            f"type={activity_type}, multiplier={multiplier}, "
            f"IF={intensity_factor:.2f}, TSS={result}"
        )

        return result

    def calculate_tss_default(
        self,
        duration_minutes: int,
        activity_type: str = "workout",
        intensity: str = "moderate"
    ) -> int:
        """
        Calculate TSS using duration and estimated intensity.

        Fallback for activities without HR or RPE data.

        Args:
            duration_minutes: Activity duration in minutes
            activity_type: Type of activity
            intensity: Estimated intensity ('easy', 'moderate', 'hard', 'very_hard')

        Returns:
            TSS value (integer)
        """
        # Map intensity to RPE equivalent
        intensity_to_rpe = {
            "easy": 3,
            "moderate": 5,
            "hard": 7,
            "very_hard": 9
        }

        rpe = intensity_to_rpe.get(intensity.lower(), 5)

        return self.calculate_tss_from_rpe(duration_minutes, rpe, activity_type)

    async def calculate_and_store_tss(
        self,
        activity_id: str,
        user_id: str,
        force_recalculate: bool = False
    ) -> Optional[int]:
        """
        Calculate TSS for an activity and store it in the database.

        Automatically selects the best calculation method based on available data:
        1. HR-based if average_heartrate exists
        2. RPE-based if perceived_exertion exists
        3. Default estimation otherwise

        Args:
            activity_id: Activity UUID
            user_id: User UUID (for security)
            force_recalculate: If True, recalculate even if TSS already exists

        Returns:
            Calculated TSS value or None if failed
        """
        try:
            # Fetch activity
            result = self.supabase.table("activities") \
                .select("*") \
                .eq("id", activity_id) \
                .eq("user_id", user_id) \
                .single() \
                .execute()

            if not result.data:
                logger.error(f"[TSS] Activity not found: {activity_id}")
                return None

            activity = result.data

            # Skip if TSS already exists (unless force)
            if activity.get("tss") and not force_recalculate:
                logger.debug(f"[TSS] Activity {activity_id} already has TSS: {activity['tss']}")
                return activity["tss"]

            # Extract data
            duration_minutes = activity.get("duration_minutes", 0)
            if duration_minutes <= 0:
                logger.warning(f"[TSS] Invalid duration for activity {activity_id}")
                return None

            activity_type = activity.get("type", "workout")
            average_hr = activity.get("average_heartrate")
            max_hr = activity.get("max_heartrate")
            rpe = activity.get("perceived_exertion")

            # Calculate TSS using best available method
            if average_hr and average_hr > 0:
                # Method 1: HR-based (most accurate)
                tss = self.calculate_tss_from_hr(
                    duration_minutes=duration_minutes,
                    average_hr=average_hr,
                    max_hr=max_hr
                )
                calc_method = "hr"
            elif rpe and rpe > 0:
                # Method 2: RPE-based
                tss = self.calculate_tss_from_rpe(
                    duration_minutes=duration_minutes,
                    rpe=rpe,
                    activity_type=activity_type
                )
                calc_method = "rpe"
            else:
                # Method 3: Default estimation (assume moderate intensity)
                tss = self.calculate_tss_default(
                    duration_minutes=duration_minutes,
                    activity_type=activity_type,
                    intensity="moderate"
                )
                calc_method = "default"

            # Store TSS in database
            update_result = self.supabase.table("activities") \
                .update({"tss": tss}) \
                .eq("id", activity_id) \
                .execute()

            if not update_result.data:
                logger.error(f"[TSS] Failed to update activity {activity_id} with TSS")
                return None

            logger.info(
                f"[TSS] Calculated TSS for activity {activity_id}: "
                f"{tss} (method: {calc_method}, duration: {duration_minutes}min)"
            )

            return tss

        except Exception as e:
            logger.error(f"[TSS] Failed to calculate TSS for activity {activity_id}: {e}")
            return None

    async def recalculate_all_tss(
        self,
        user_id: str,
        days_back: int = 90
    ) -> Dict[str, Any]:
        """
        Recalculate TSS for all user activities in the last N days.

        Useful for:
        - Initial setup after implementing TSS
        - Updating TSS calculation logic
        - Fixing data inconsistencies

        Args:
            user_id: User UUID
            days_back: Number of days to recalculate (default: 90)

        Returns:
            Dict with recalculation results
        """
        try:
            from datetime import datetime, timedelta

            cutoff_date = (datetime.now() - timedelta(days=days_back)).isoformat()

            # Get all activities without TSS or with force recalculate
            result = self.supabase.table("activities") \
                .select("id") \
                .eq("user_id", user_id) \
                .gte("start_date", cutoff_date) \
                .execute()

            if not result.data:
                return {
                    "success": True,
                    "activities_processed": 0,
                    "tss_calculated": 0,
                    "errors": 0
                }

            activities = result.data
            calculated = 0
            errors = 0

            for activity in activities:
                tss = await self.calculate_and_store_tss(
                    activity_id=activity["id"],
                    user_id=user_id,
                    force_recalculate=True
                )

                if tss is not None:
                    calculated += 1
                else:
                    errors += 1

            logger.info(
                f"[TSS] Recalculated TSS for user {user_id}: "
                f"{calculated}/{len(activities)} activities"
            )

            return {
                "success": True,
                "activities_processed": len(activities),
                "tss_calculated": calculated,
                "errors": errors
            }

        except Exception as e:
            logger.error(f"[TSS] Failed to recalculate all TSS: {e}")
            return {
                "success": False,
                "error": str(e)
            }
