"""
Garmin Sync Service - Comprehensive Health Data Integration

Syncs all health metrics from Garmin Connect to Wagner Coach database:
- Sleep tracking (duration, stages, quality, HRV)
- Daily readiness (training readiness, recovery metrics)
- HRV logs (heart rate variability tracking)
- Stress tracking (stress levels, rest time)
- Body Battery (energy reserves)
- Daily steps & activity (move IQ, intensity minutes)
- Training load & status (acute/chronic load, TSS)

Supports both automatic sync and manual entry fallbacks.
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta, date
from dataclasses import dataclass

try:
    from garminconnect import Garmin
    GARMIN_AVAILABLE = True
except ImportError:
    GARMIN_AVAILABLE = False

from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


@dataclass
class SyncResult:
    """Result of a sync operation."""
    success: bool
    synced_count: int
    skipped_count: int
    error_count: int
    errors: List[str]
    date_range: Dict[str, str]


class GarminSyncService:
    """
    Comprehensive Garmin Connect sync service for health metrics.

    This service handles bidirectional sync:
    - Pull data from Garmin Connect API
    - Store in Wagner Coach database
    - Handle duplicates and conflicts
    - Support manual entry as fallback
    """

    def __init__(self):
        """Initialize with Supabase client."""
        self.supabase = get_service_client()
        self._garmin_client: Optional[Garmin] = None

    def _get_garmin_client(self, email: str, password: str) -> Garmin:
        """
        Get authenticated Garmin client.

        Args:
            email: Garmin account email
            password: Garmin account password

        Returns:
            Authenticated Garmin client

        Raises:
            Exception: If garminconnect not available or login fails
        """
        if not GARMIN_AVAILABLE:
            raise Exception("garminconnect package not installed. Run: pip install garminconnect")

        if self._garmin_client is None:
            try:
                self._garmin_client = Garmin(email, password)
                self._garmin_client.login()
                logger.info(f"[GarminSync] Authenticated with Garmin Connect: {email}")
            except Exception as e:
                logger.error(f"[GarminSync] Authentication failed: {e}")
                raise Exception(f"Failed to authenticate with Garmin: {str(e)}")

        return self._garmin_client

    async def test_connection(self, email: str, password: str) -> Dict[str, Any]:
        """
        Test Garmin Connect connection.

        Args:
            email: Garmin account email
            password: Garmin account password

        Returns:
            Dict with connection status and user profile
        """
        try:
            client = self._get_garmin_client(email, password)
            profile = client.get_user_summary()

            return {
                "success": True,
                "message": "Successfully connected to Garmin Connect",
                "profile": {
                    "display_name": profile.get("displayName"),
                    "email": email
                }
            }
        except Exception as e:
            logger.error(f"[GarminSync] Connection test failed: {e}")
            return {
                "success": False,
                "message": f"Connection failed: {str(e)}"
            }

    async def sync_all_health_data(
        self,
        user_id: str,
        email: str,
        password: str,
        days_back: int = 7
    ) -> Dict[str, Any]:
        """
        Sync ALL health data from Garmin (sleep, HRV, readiness, etc.).

        Args:
            user_id: User UUID
            email: Garmin email
            password: Garmin password
            days_back: Number of days to sync (default: 7)

        Returns:
            Dict with comprehensive sync results for all metrics
        """
        client = self._get_garmin_client(email, password)

        # Calculate date range
        end_date = date.today()
        start_date = end_date - timedelta(days=days_back)

        logger.info(f"[GarminSync] Starting full sync for user {user_id}: {start_date} to {end_date}")

        results = {}

        # Sync each health metric
        results["sleep"] = await self.sync_sleep_data(user_id, client, start_date, end_date)
        results["hrv"] = await self.sync_hrv_data(user_id, client, start_date, end_date)
        results["stress"] = await self.sync_stress_data(user_id, client, start_date, end_date)
        results["body_battery"] = await self.sync_body_battery_data(user_id, client, start_date, end_date)
        results["steps_activity"] = await self.sync_steps_activity_data(user_id, client, start_date, end_date)
        results["training_load"] = await self.sync_training_load_data(user_id, client, start_date, end_date)
        results["readiness"] = await self.sync_readiness_data(user_id, client, start_date, end_date)

        # Calculate totals
        total_synced = sum(r["synced_count"] for r in results.values())
        total_errors = sum(r["error_count"] for r in results.values())

        logger.info(f"[GarminSync] Full sync complete: {total_synced} records synced, {total_errors} errors")

        return {
            "success": total_errors == 0,
            "user_id": user_id,
            "date_range": {
                "start": start_date.isoformat(),
                "end": end_date.isoformat()
            },
            "total_synced": total_synced,
            "total_errors": total_errors,
            "details": results
        }

    async def sync_sleep_data(
        self,
        user_id: str,
        client: Garmin,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """
        Sync sleep data from Garmin.

        Garmin provides:
        - Sleep stages (deep, light, REM, awake)
        - Sleep score (0-100)
        - Sleep duration & times
        - HRV during sleep
        - Resting heart rate
        - Respiration rate
        - SpO2 levels
        """
        synced = 0
        errors = []

        try:
            current_date = start_date

            while current_date <= end_date:
                try:
                    # Get sleep data for specific date
                    sleep_data = client.get_sleep_data(current_date.isoformat())

                    if sleep_data and sleep_data.get("dailySleepDTO"):
                        sleep_dto = sleep_data["dailySleepDTO"]

                        # Extract sleep stages (convert seconds to minutes)
                        deep_sleep = sleep_dto.get("deepSleepSeconds", 0) // 60
                        light_sleep = sleep_dto.get("lightSleepSeconds", 0) // 60
                        rem_sleep = sleep_dto.get("remSleepSeconds", 0) // 60
                        awake_minutes = sleep_dto.get("awakeSleepSeconds", 0) // 60

                        total_sleep = deep_sleep + light_sleep + rem_sleep

                        # Calculate sleep score (if not provided, estimate from stages)
                        sleep_score = sleep_dto.get("sleepScores", {}).get("overall", {}).get("value")
                        if not sleep_score and total_sleep > 0:
                            # Estimate: deep=40%, light=40%, REM=20% is ideal
                            deep_pct = (deep_sleep / total_sleep) * 100
                            rem_pct = (rem_sleep / total_sleep) * 100
                            sleep_score = min(100, int((deep_pct * 0.4) + (rem_pct * 0.3) + 30))

                        # Determine quality
                        if sleep_score:
                            if sleep_score >= 80:
                                quality = "excellent"
                            elif sleep_score >= 65:
                                quality = "good"
                            elif sleep_score >= 50:
                                quality = "fair"
                            else:
                                quality = "poor"
                        else:
                            quality = "good" if total_sleep >= 420 else "fair"

                        # Parse timestamps
                        sleep_start = datetime.fromisoformat(sleep_dto.get("sleepStartTimestampLocal", "").replace("Z", "+00:00"))
                        sleep_end = datetime.fromisoformat(sleep_dto.get("sleepEndTimestampLocal", "").replace("Z", "+00:00"))

                        # Build sleep log record
                        sleep_log = {
                            "user_id": user_id,
                            "sleep_date": current_date.isoformat(),
                            "sleep_start": sleep_start.isoformat(),
                            "sleep_end": sleep_end.isoformat(),
                            "total_sleep_minutes": total_sleep,
                            "deep_sleep_minutes": deep_sleep,
                            "light_sleep_minutes": light_sleep,
                            "rem_sleep_minutes": rem_sleep,
                            "awake_minutes": awake_minutes,
                            "sleep_score": sleep_score,
                            "sleep_quality": quality,
                            "interruptions": sleep_dto.get("awakeCount", 0),
                            "restlessness_level": min(10, sleep_dto.get("restlessMomentCount", 0) // 5),
                            "avg_hrv_ms": sleep_dto.get("avgSleepStress"),  # Garmin's sleep stress correlates with HRV
                            "avg_heart_rate": sleep_dto.get("averageHeartRate"),
                            "lowest_heart_rate": sleep_dto.get("lowestHeartRate"),
                            "avg_respiration_rate": sleep_dto.get("avgRespirationRate"),
                            "avg_spo2_percentage": sleep_dto.get("avgSpO2Value"),
                            "source": "garmin",
                            "entry_method": "auto_sync",
                            "notes": f"Garmin sleep score: {sleep_score}/100"
                        }

                        # Upsert to database (unique constraint on user_id + sleep_date)
                        result = self.supabase.table("sleep_logs").upsert(sleep_log, on_conflict="user_id,sleep_date").execute()

                        if result.data:
                            synced += 1
                            logger.debug(f"[GarminSync] Sleep synced: {current_date} - {total_sleep}min, score: {sleep_score}")

                except Exception as e:
                    error_msg = f"Sleep sync failed for {current_date}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(f"[GarminSync] {error_msg}")

                current_date += timedelta(days=1)

            return {
                "synced_count": synced,
                "error_count": len(errors),
                "skipped_count": (end_date - start_date).days + 1 - synced - len(errors),
                "errors": errors
            }

        except Exception as e:
            logger.error(f"[GarminSync] Sleep sync failed: {e}")
            return {
                "synced_count": 0,
                "error_count": 1,
                "skipped_count": 0,
                "errors": [str(e)]
            }

    async def sync_hrv_data(
        self,
        user_id: str,
        client: Garmin,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """
        Sync HRV (Heart Rate Variability) data from Garmin.

        HRV is a key recovery metric showing autonomic nervous system balance.
        """
        synced = 0
        errors = []

        try:
            # Get HRV data (often part of stress/wellness data)
            current_date = start_date

            while current_date <= end_date:
                try:
                    hrv_data = client.get_hrv_data(current_date.isoformat())

                    if hrv_data and "hrvSummary" in hrv_data:
                        hrv_summary = hrv_data["hrvSummary"]

                        # Extract HRV metrics
                        hrv_log = {
                            "user_id": user_id,
                            "recorded_at": f"{current_date.isoformat()}T08:00:00Z",  # Morning HRV
                            "hrv_rmssd_ms": hrv_summary.get("lastNightAvg"),  # RMSSD is gold standard
                            "hrv_sdnn_ms": hrv_summary.get("weeklyAvg"),  # Weekly average
                            "measurement_type": "morning",
                            "quality_score": 100,  # Garmin data is high quality
                            "notes": f"Garmin 7-day baseline: {hrv_summary.get('weeklyAvg')}ms",
                            "source": "garmin",
                            "entry_method": "auto_sync"
                        }

                        result = self.supabase.table("hrv_logs").insert(hrv_log).execute()

                        if result.data:
                            synced += 1
                            logger.debug(f"[GarminSync] HRV synced: {current_date} - {hrv_log['hrv_rmssd_ms']}ms")

                except Exception as e:
                    errors.append(f"HRV sync failed for {current_date}: {str(e)}")

                current_date += timedelta(days=1)

            return {"synced_count": synced, "error_count": len(errors), "skipped_count": 0, "errors": errors}

        except Exception as e:
            logger.error(f"[GarminSync] HRV sync failed: {e}")
            return {"synced_count": 0, "error_count": 1, "skipped_count": 0, "errors": [str(e)]}

    async def sync_stress_data(
        self,
        user_id: str,
        client: Garmin,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Sync stress tracking data from Garmin."""
        synced = 0
        errors = []

        try:
            current_date = start_date

            while current_date <= end_date:
                try:
                    stress_data = client.get_stress_data(current_date.isoformat())

                    if stress_data:
                        avg_stress = stress_data.get("avgStressLevel")
                        max_stress = stress_data.get("maxStressLevel")
                        rest_time = stress_data.get("restStressDuration", 0) // 60  # Convert to minutes

                        stress_log = {
                            "user_id": user_id,
                            "recorded_at": f"{current_date.isoformat()}T12:00:00Z",
                            "avg_stress_level": avg_stress,
                            "max_stress_level": max_stress,
                            "rest_time_minutes": rest_time,
                            "notes": f"Garmin stress tracking (0-100 scale)",
                            "source": "garmin",
                            "entry_method": "auto_sync"
                        }

                        result = self.supabase.table("stress_logs").insert(stress_log).execute()

                        if result.data:
                            synced += 1

                except Exception as e:
                    errors.append(f"Stress sync failed for {current_date}: {str(e)}")

                current_date += timedelta(days=1)

            return {"synced_count": synced, "error_count": len(errors), "skipped_count": 0, "errors": errors}

        except Exception as e:
            return {"synced_count": 0, "error_count": 1, "skipped_count": 0, "errors": [str(e)]}

    async def sync_body_battery_data(
        self,
        user_id: str,
        client: Garmin,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Sync Body Battery data from Garmin (energy reserves)."""
        synced = 0
        errors = []

        try:
            current_date = start_date

            while current_date <= end_date:
                try:
                    # Body Battery is Garmin's proprietary energy metric
                    bb_data = client.get_body_battery(current_date.isoformat(), current_date.isoformat())

                    if bb_data and len(bb_data) > 0:
                        for entry in bb_data:
                            bb_log = {
                                "user_id": user_id,
                                "recorded_at": entry.get("startTimestampLocal"),
                                "battery_level": entry.get("bodyBatteryLevel"),
                                "charged_value": entry.get("charged"),
                                "drained_value": entry.get("drained"),
                                "notes": f"Garmin Body Battery (0-100)",
                                "source": "garmin",
                                "entry_method": "auto_sync"
                            }

                            result = self.supabase.table("body_battery_logs").insert(bb_log).execute()

                            if result.data:
                                synced += 1

                except Exception as e:
                    errors.append(f"Body Battery sync failed for {current_date}: {str(e)}")

                current_date += timedelta(days=1)

            return {"synced_count": synced, "error_count": len(errors), "skipped_count": 0, "errors": errors}

        except Exception as e:
            return {"synced_count": 0, "error_count": 1, "skipped_count": 0, "errors": [str(e)]}

    async def sync_steps_activity_data(
        self,
        user_id: str,
        client: Garmin,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Sync daily steps and activity data from Garmin."""
        synced = 0
        errors = []

        try:
            current_date = start_date

            while current_date <= end_date:
                try:
                    daily_stats = client.get_stats(current_date.isoformat())

                    if daily_stats:
                        steps_log = {
                            "user_id": user_id,
                            "date": current_date.isoformat(),
                            "total_steps": daily_stats.get("totalSteps", 0),
                            "step_goal": daily_stats.get("dailyStepGoal", 10000),
                            "total_distance_meters": daily_stats.get("totalDistanceMeters", 0),
                            "active_calories": daily_stats.get("activeKilocalories", 0),
                            "floors_climbed": daily_stats.get("floorsAscended", 0),
                            "moderate_intensity_minutes": daily_stats.get("moderateIntensityMinutes", 0),
                            "vigorous_intensity_minutes": daily_stats.get("vigorousIntensityMinutes", 0),
                            "source": "garmin",
                            "entry_method": "auto_sync"
                        }

                        result = self.supabase.table("daily_steps_and_activity").upsert(steps_log, on_conflict="user_id,date").execute()

                        if result.data:
                            synced += 1

                except Exception as e:
                    errors.append(f"Steps/activity sync failed for {current_date}: {str(e)}")

                current_date += timedelta(days=1)

            return {"synced_count": synced, "error_count": len(errors), "skipped_count": 0, "errors": errors}

        except Exception as e:
            return {"synced_count": 0, "error_count": 1, "skipped_count": 0, "errors": [str(e)]}

    async def sync_training_load_data(
        self,
        user_id: str,
        client: Garmin,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """Sync training load and status from Garmin."""
        synced = 0
        errors = []

        try:
            # Get training status (includes load, recovery time, VO2 max)
            training_status = client.get_training_status()

            if training_status:
                load_log = {
                    "user_id": user_id,
                    "date": end_date.isoformat(),  # Latest date
                    "acute_load": training_status.get("acuteTrainingLoad"),
                    "chronic_load": training_status.get("chronicTrainingLoad"),
                    "load_ratio": training_status.get("loadRatio"),
                    "training_status": training_status.get("trainingStatusKey"),  # productive, maintaining, peaking, etc.
                    "recovery_time_hours": (training_status.get("recoveryTimeInSeconds", 0) // 3600),
                    "fitness_level": training_status.get("fitnessLevel"),
                    "source": "garmin",
                    "entry_method": "auto_sync"
                }

                result = self.supabase.table("training_load_history").insert(load_log).execute()

                if result.data:
                    synced += 1

            return {"synced_count": synced, "error_count": len(errors), "skipped_count": 0, "errors": errors}

        except Exception as e:
            return {"synced_count": 0, "error_count": 1, "skipped_count": 0, "errors": [str(e)]}

    async def sync_readiness_data(
        self,
        user_id: str,
        client: Garmin,
        start_date: date,
        end_date: date
    ) -> Dict[str, Any]:
        """
        Sync/calculate daily readiness data.

        Garmin doesn't have a single "readiness" metric, so we calculate it
        from available data (sleep, HRV, training load, stress).
        """
        synced = 0
        errors = []

        try:
            current_date = start_date

            while current_date <= end_date:
                try:
                    # Fetch all components for readiness calculation
                    # This is done after other syncs complete

                    # Get sleep score
                    sleep_query = self.supabase.table("sleep_logs") \
                        .select("sleep_score") \
                        .eq("user_id", user_id) \
                        .eq("sleep_date", current_date.isoformat()) \
                        .execute()

                    sleep_score = sleep_query.data[0]["sleep_score"] if sleep_query.data else None

                    # Get HRV status (compare to baseline)
                    hrv_query = self.supabase.table("hrv_logs") \
                        .select("hrv_rmssd_ms") \
                        .eq("user_id", user_id) \
                        .gte("recorded_at", f"{current_date.isoformat()}T00:00:00Z") \
                        .lte("recorded_at", f"{current_date.isoformat()}T23:59:59Z") \
                        .execute()

                    hrv_value = hrv_query.data[0]["hrv_rmssd_ms"] if hrv_query.data else None

                    # Calculate HRV status
                    hrv_status = None
                    if hrv_value:
                        baseline = await self._get_hrv_baseline(user_id)
                        if baseline:
                            ratio = hrv_value / baseline
                            if ratio >= 1.1:
                                hrv_status = "excellent"
                            elif ratio >= 0.95:
                                hrv_status = "balanced"
                            elif ratio >= 0.8:
                                hrv_status = "unbalanced"
                            else:
                                hrv_status = "poor"

                    # Get training load ratio
                    load_query = self.supabase.table("training_load_history") \
                        .select("load_ratio, acute_load, chronic_load") \
                        .eq("user_id", user_id) \
                        .order("date", desc=True) \
                        .limit(1) \
                        .execute()

                    load_data = load_query.data[0] if load_query.data else {}

                    # Calculate readiness score (adaptive based on available data)
                    factors_used = {}
                    readiness_score = 50  # Start at 50 (neutral)

                    if sleep_score:
                        readiness_score += (sleep_score - 70) * 0.5  # +/- 15 points
                        factors_used["sleep"] = sleep_score

                    if hrv_status:
                        hrv_points = {"excellent": 20, "balanced": 10, "unbalanced": -10, "poor": -20}
                        readiness_score += hrv_points.get(hrv_status, 0)
                        factors_used["hrv"] = hrv_status

                    if load_data.get("load_ratio"):
                        ratio = load_data["load_ratio"]
                        if 0.8 <= ratio <= 1.3:
                            readiness_score += 10  # Optimal training load
                        elif ratio > 1.5:
                            readiness_score -= 20  # Overtraining risk
                        factors_used["load_ratio"] = ratio

                    # Clamp to 0-100
                    readiness_score = max(0, min(100, int(readiness_score)))

                    # Determine readiness status
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

                    # Build readiness record
                    readiness_log = {
                        "user_id": user_id,
                        "date": current_date.isoformat(),
                        "readiness_score": readiness_score,
                        "readiness_status": readiness_status,
                        "sleep_score": sleep_score,
                        "hrv_status": hrv_status,
                        "acute_training_load": load_data.get("acute_load"),
                        "chronic_training_load": load_data.get("chronic_load"),
                        "load_ratio": load_data.get("load_ratio"),
                        "calculation_method": "auto_calculated",
                        "factors_used": factors_used
                    }

                    result = self.supabase.table("daily_readiness").upsert(readiness_log, on_conflict="user_id,date").execute()

                    if result.data:
                        synced += 1
                        logger.debug(f"[GarminSync] Readiness calculated: {current_date} - {readiness_score} ({readiness_status})")

                except Exception as e:
                    errors.append(f"Readiness calc failed for {current_date}: {str(e)}")

                current_date += timedelta(days=1)

            return {"synced_count": synced, "error_count": len(errors), "skipped_count": 0, "errors": errors}

        except Exception as e:
            return {"synced_count": 0, "error_count": 1, "skipped_count": 0, "errors": [str(e)]}

    async def _get_hrv_baseline(self, user_id: str) -> Optional[float]:
        """Calculate 7-day HRV baseline."""
        try:
            seven_days_ago = (date.today() - timedelta(days=7)).isoformat()

            query = self.supabase.rpc(
                "calculate_hrv_baseline",
                {"p_user_id": user_id, "p_end_date": date.today().isoformat()}
            ).execute()

            return query.data if query.data else None
        except Exception as e:
            logger.error(f"[GarminSync] HRV baseline calculation failed: {e}")
            return None
