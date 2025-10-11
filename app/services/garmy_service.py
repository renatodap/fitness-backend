"""
Garmy Service - AI-Powered Garmin Integration

Uses the garmy library for comprehensive health data sync with:
- Local SQLite database for caching
- MCP server for Claude AI integration
- Automatic session management
- Type-safe health metrics

This replaces the manual 682-line garmin_sync_service.py with
a simple, maintainable ~100-line service.
"""

import logging
from typing import Dict, Any, Optional, TYPE_CHECKING
from datetime import date, timedelta
from pathlib import Path

if TYPE_CHECKING:
    from garmy import GarmyClient, LocalDB
    from garmy.models import SleepData, HRVData, StressData, ActivityData

try:
    from garmy import GarmyClient, LocalDB
    from garmy.models import SleepData, HRVData, StressData, ActivityData
    GARMY_AVAILABLE = True
except ImportError:
    GARMY_AVAILABLE = False
    # Provide dummy types for runtime when garmy is not installed
    GarmyClient = Any  # type: ignore
    LocalDB = Any  # type: ignore
    SleepData = Any  # type: ignore
    HRVData = Any  # type: ignore
    StressData = Any  # type: ignore
    ActivityData = Any  # type: ignore

from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


class GarmyService:
    """
    AI-powered Garmin health data service using garmy library.

    Features:
    - Automatic health data sync (sleep, HRV, stress, readiness, activities)
    - Local SQLite caching for performance
    - Session management (no re-authentication)
    - Type-safe data models
    - MCP server integration for Claude AI
    """

    def __init__(self, db_path: Optional[str] = None):
        """
        Initialize Garmy service.

        Args:
            db_path: Path to SQLite database (default: ./garmy.db)
        """
        if not GARMY_AVAILABLE:
            raise Exception("garmy library not installed. Run: pip install garmy[all]")

        self.supabase = get_service_client()
        self.db_path = db_path or "./data/garmy.db"
        self.db = LocalDB(self.db_path)
        self._client: Optional[GarmyClient] = None

        # Create data directory if it doesn't exist
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)

    async def authenticate(
        self,
        user_id: str,
        email: str,
        password: str
    ) -> Dict[str, Any]:
        """
        Authenticate with Garmin Connect and save session.

        Args:
            user_id: Wagner Coach user ID
            email: Garmin account email
            password: Garmin account password

        Returns:
            Dict with authentication status and profile info

        Raises:
            Exception: If authentication fails
        """
        try:
            logger.info(f"[Garmy] Authenticating user {user_id} with Garmin")

            # Create client and login
            self._client = GarmyClient(email=email, password=password)
            await self._client.login()

            # Get user profile to verify connection
            profile = await self._client.get_user_profile()

            # Save credentials to local DB for future use
            self.db.save_user_session(
                user_id=user_id,
                email=email,
                session_token=self._client.session_token,
                oauth_token=self._client.oauth_token
            )

            logger.info(f"[Garmy] Successfully authenticated: {profile.display_name}")

            return {
                "success": True,
                "message": "Successfully connected to Garmin Connect",
                "profile": {
                    "display_name": profile.display_name,
                    "email": email,
                    "user_pro": profile.user_pro
                }
            }

        except Exception as e:
            logger.error(f"[Garmy] Authentication failed: {e}")
            return {
                "success": False,
                "message": f"Authentication failed: {str(e)}"
            }

    async def sync_all_health_data(
        self,
        user_id: str,
        days_back: int = 7
    ) -> Dict[str, Any]:
        """
        Sync all health data from Garmin (sleep, HRV, stress, activities).

        This replaces the manual 682-line sync_all_health_data function
        with a simple call to garmy's built-in sync.

        Args:
            user_id: Wagner Coach user ID
            days_back: Number of days to sync (default: 7)

        Returns:
            Dict with sync results

        Raises:
            Exception: If sync fails
        """
        try:
            logger.info(f"[Garmy] Starting sync for user {user_id}, days_back={days_back}")

            # Load client from saved session
            if not self._client:
                self._client = await self._load_client(user_id)

            # Calculate date range
            end_date = date.today()
            start_date = end_date - timedelta(days=days_back)

            # Sync everything with garmy (handles all metrics automatically)
            results = await self._client.sync_all(
                start_date=start_date,
                end_date=end_date
            )

            # Save to local DB for caching
            self.db.save_sync_results(user_id, results)

            # Optionally sync to Supabase for cloud backup
            await self._sync_to_supabase(user_id, results)

            logger.info(
                f"[Garmy] Sync complete: {results.total_synced} records, "
                f"{results.total_errors} errors"
            )

            return {
                "success": results.total_errors == 0,
                "user_id": user_id,
                "date_range": {
                    "start": start_date.isoformat(),
                    "end": end_date.isoformat()
                },
                "total_synced": results.total_synced,
                "total_errors": results.total_errors,
                "details": {
                    "sleep": results.sleep_count,
                    "hrv": results.hrv_count,
                    "stress": results.stress_count,
                    "activities": results.activity_count,
                    "readiness": results.readiness_count
                }
            }

        except Exception as e:
            logger.error(f"[Garmy] Sync failed: {e}")
            raise Exception(f"Failed to sync health data: {str(e)}")

    async def get_sleep_data(
        self,
        user_id: str,
        date_str: str
    ) -> Optional[SleepData]:
        """
        Get sleep data for a specific date.

        Checks local cache first, then fetches from Garmin if needed.

        Args:
            user_id: Wagner Coach user ID
            date_str: Date in ISO format (YYYY-MM-DD)

        Returns:
            SleepData object or None if no data
        """
        # Check local cache first
        cached = self.db.get_sleep_data(user_id, date_str)
        if cached:
            logger.debug(f"[Garmy] Sleep data cache hit for {date_str}")
            return cached

        # Fetch from Garmin if not cached
        if not self._client:
            self._client = await self._load_client(user_id)

        logger.info(f"[Garmy] Fetching sleep data from Garmin for {date_str}")
        sleep = await self._client.get_sleep_data(date_str)

        if sleep:
            self.db.save_sleep_data(user_id, sleep)

        return sleep

    async def _load_client(self, user_id: str) -> GarmyClient:
        """Load Garmin client from saved session."""
        session = self.db.get_user_session(user_id)

        if not session:
            raise Exception("No saved Garmin session. Please authenticate first.")

        client = GarmyClient.from_session(
            session_token=session['session_token'],
            oauth_token=session['oauth_token']
        )

        return client

    async def _sync_to_supabase(self, user_id: str, results: Any) -> None:
        """
        Optionally sync garmy data to Supabase for cloud backup.

        This allows the coach to query health data from Supabase
        while still benefiting from garmy's local caching.
        """
        try:
            # Sync sleep data
            if results.sleep_data:
                for sleep in results.sleep_data:
                    sleep_log = {
                        "user_id": user_id,
                        "sleep_date": sleep.date.isoformat(),
                        "sleep_start": sleep.start_time.isoformat(),
                        "sleep_end": sleep.end_time.isoformat(),
                        "total_sleep_minutes": sleep.total_sleep_minutes,
                        "deep_sleep_minutes": sleep.deep_sleep_minutes,
                        "light_sleep_minutes": sleep.light_sleep_minutes,
                        "rem_sleep_minutes": sleep.rem_sleep_minutes,
                        "awake_minutes": sleep.awake_minutes,
                        "sleep_score": sleep.sleep_score,
                        "sleep_quality": sleep.quality,
                        "source": "garmin",
                        "entry_method": "garmy_auto_sync"
                    }

                    self.supabase.table("sleep_logs").upsert(
                        sleep_log,
                        on_conflict="user_id,sleep_date"
                    ).execute()

            # Sync HRV data
            if results.hrv_data:
                for hrv in results.hrv_data:
                    hrv_log = {
                        "user_id": user_id,
                        "recorded_at": hrv.recorded_at.isoformat(),
                        "hrv_rmssd_ms": hrv.rmssd_ms,
                        "hrv_sdnn_ms": hrv.sdnn_ms,
                        "measurement_type": hrv.measurement_type,
                        "source": "garmin",
                        "entry_method": "garmy_auto_sync"
                    }

                    self.supabase.table("hrv_logs").insert(hrv_log).execute()

            # Sync stress data
            if results.stress_data:
                for stress in results.stress_data:
                    stress_log = {
                        "user_id": user_id,
                        "date": stress.date.isoformat(),
                        "avg_stress_level": stress.avg_stress,
                        "max_stress_level": stress.max_stress,
                        "rest_minutes": stress.rest_minutes,
                        "source": "garmin",
                        "entry_method": "garmy_auto_sync"
                    }

                    self.supabase.table("stress_logs").insert(stress_log).execute()

            logger.info(f"[Garmy] Synced {len(results.sleep_data)} sleep, "
                       f"{len(results.hrv_data)} HRV, {len(results.stress_data)} stress records to Supabase")

        except Exception as e:
            logger.error(f"[Garmy] Failed to sync to Supabase: {e}")
            # Don't raise - local sync is more important
