"""
Summarization Service

Generates automated summaries of user fitness data.
"""

import logging
from datetime import date, datetime, timedelta
from typing import Any, Dict, List, Optional
from enum import Enum
from collections import Counter

from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


class SummaryPeriodType(str, Enum):
    """Summary period types."""
    WEEKLY = "weekly"
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"


class SummarizationService:
    """
    Service for generating user activity summaries.

    Generates weekly, monthly, and quarterly summaries by aggregating
    user workout, nutrition, and activity data.
    """

    def __init__(self):
        """Initialize with Supabase client."""
        self.supabase = get_service_client()

    async def generate_all_summaries(self) -> Dict[str, Any]:
        """
        Generate summaries for all users.

        Returns:
            Dict with results: {processed, errors, summaries_created}
        """
        results = {"processed": 0, "errors": 0, "summaries_created": 0}

        try:
            # Get all users
            response = self.supabase.table("profiles").select("id").execute()
            users = response.data

            logger.info(f"Processing summaries for {len(users)} users")

            for user in users:
                try:
                    count = await self.generate_user_summaries(user["id"])
                    results["processed"] += 1
                    results["summaries_created"] += count
                except Exception as e:
                    logger.error(f"Error processing user {user['id']}: {e}")
                    results["errors"] += 1

            logger.info(f"Summarization complete: {results}")
            return results

        except Exception as e:
            logger.error(f"Error in generate_all_summaries: {e}")
            raise

    async def generate_user_summaries(self, user_id: str) -> int:
        """
        Generate all applicable summaries for a user.

        Args:
            user_id: User UUID

        Returns:
            int: Number of summaries created

        Raises:
            ValueError: If user_id is invalid
        """
        if not user_id:
            raise ValueError("user_id is required")

        today = datetime.now().date()
        summaries_created = 0

        # Always generate weekly summary
        await self.generate_weekly_summary(user_id)
        summaries_created += 1

        # Generate monthly summary on 1st of month
        if self._is_first_day_of_month(today):
            await self.generate_monthly_summary(user_id)
            summaries_created += 1

        # Generate quarterly summary on 1st of quarter
        if self._is_first_day_of_quarter(today):
            await self.generate_quarterly_summary(user_id)
            summaries_created += 1

        return summaries_created

    async def generate_weekly_summary(
        self, user_id: str, end_date: Optional[date] = None
    ) -> Dict[str, Any]:
        """
        Generate weekly summary (last 7 days).

        Args:
            user_id: User UUID
            end_date: End date for summary (default: today)

        Returns:
            Summary data dictionary
        """
        if end_date is None:
            end_date = datetime.now().date()

        start_date = end_date - timedelta(days=6)

        # Fetch data
        workouts_data = await self._fetch_workouts(user_id, start_date, end_date)
        nutrition_data = await self._fetch_nutrition(user_id, start_date, end_date)
        activities_data = await self._fetch_activities(user_id, start_date, end_date)

        # Build summary
        summary = {
            "period_type": SummaryPeriodType.WEEKLY.value,
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "workouts": self._aggregate_workouts(workouts_data),
            "nutrition": self._aggregate_nutrition(nutrition_data),
            "activities": self._aggregate_activities(activities_data),
        }

        # Save summary
        await self._save_summary(user_id, summary)

        return summary

    async def generate_monthly_summary(
        self, user_id: str, month: Optional[int] = None, year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate monthly summary.

        Args:
            user_id: User UUID
            month: Month (1-12, default: previous month)
            year: Year (default: current year or previous)

        Returns:
            Summary data dictionary
        """
        today = datetime.now().date()

        if month is None or year is None:
            # Default to previous month
            last_month = today.replace(day=1) - timedelta(days=1)
            month = last_month.month
            year = last_month.year

        # Calculate date range
        start_date = date(year, month, 1)
        if month == 12:
            end_date = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            end_date = date(year, month + 1, 1) - timedelta(days=1)

        # Fetch and aggregate data
        workouts_data = await self._fetch_workouts(user_id, start_date, end_date)
        nutrition_data = await self._fetch_nutrition(user_id, start_date, end_date)
        activities_data = await self._fetch_activities(user_id, start_date, end_date)

        summary = {
            "period_type": SummaryPeriodType.MONTHLY.value,
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "workouts": self._aggregate_workouts(workouts_data),
            "nutrition": self._aggregate_nutrition(nutrition_data),
            "activities": self._aggregate_activities(activities_data),
        }

        await self._save_summary(user_id, summary)
        return summary

    async def generate_quarterly_summary(
        self, user_id: str, quarter: Optional[int] = None, year: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate quarterly summary.

        Args:
            user_id: User UUID
            quarter: Quarter (1-4, default: previous quarter)
            year: Year

        Returns:
            Summary data dictionary
        """
        today = datetime.now().date()

        if quarter is None or year is None:
            current_quarter = self._get_quarter(today)
            if current_quarter == 1:
                quarter = 4
                year = today.year - 1
            else:
                quarter = current_quarter - 1
                year = today.year

        # Calculate date range
        quarter_months = {1: (1, 3), 2: (4, 6), 3: (7, 9), 4: (10, 12)}
        start_month, end_month = quarter_months[quarter]

        start_date = date(year, start_month, 1)
        end_date = date(year, end_month + 1, 1) - timedelta(days=1) if end_month < 12 else date(year, 12, 31)

        # Fetch and aggregate
        workouts_data = await self._fetch_workouts(user_id, start_date, end_date)
        nutrition_data = await self._fetch_nutrition(user_id, start_date, end_date)
        activities_data = await self._fetch_activities(user_id, start_date, end_date)

        summary = {
            "period_type": SummaryPeriodType.QUARTERLY.value,
            "period_start": start_date.isoformat(),
            "period_end": end_date.isoformat(),
            "workouts": self._aggregate_workouts(workouts_data),
            "nutrition": self._aggregate_nutrition(nutrition_data),
            "activities": self._aggregate_activities(activities_data),
        }

        await self._save_summary(user_id, summary)
        return summary

    async def _fetch_workouts(
        self, user_id: str, start_date: date, end_date: date
    ) -> List[Dict]:
        """Fetch workouts for date range."""
        try:
            response = (
                self.supabase.table("workouts")
                .select("*")
                .eq("user_id", user_id)
                .gte("date", start_date.isoformat())
                .lte("date", end_date.isoformat())
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching workouts: {e}")
            return []

    async def _fetch_nutrition(
        self, user_id: str, start_date: date, end_date: date
    ) -> List[Dict]:
        """Fetch nutrition logs for date range."""
        try:
            response = (
                self.supabase.table("meals")
                .select("*")
                .eq("user_id", user_id)
                .gte("date", start_date.isoformat())
                .lte("date", end_date.isoformat())
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching nutrition: {e}")
            return []

    async def _fetch_activities(
        self, user_id: str, start_date: date, end_date: date
    ) -> List[Dict]:
        """Fetch activities for date range."""
        try:
            response = (
                self.supabase.table("activities")
                .select("*")
                .eq("user_id", user_id)
                .gte("date", start_date.isoformat())
                .lte("date", end_date.isoformat())
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching activities: {e}")
            return []

    def _aggregate_workouts(self, workouts: List[Dict]) -> Dict[str, Any]:
        """Aggregate workout statistics."""
        if not workouts:
            return {
                "total_workouts": 0,
                "total_duration_minutes": 0,
                "total_calories": 0,
                "workout_types": {},
                "avg_duration_minutes": 0,
            }

        total_duration = sum(w.get("duration_minutes", 0) for w in workouts)
        workout_types = Counter(w.get("type", "unknown") for w in workouts)

        return {
            "total_workouts": len(workouts),
            "total_duration_minutes": total_duration,
            "total_calories": sum(w.get("calories", 0) for w in workouts),
            "workout_types": dict(workout_types),
            "avg_duration_minutes": total_duration / len(workouts) if workouts else 0,
        }

    def _aggregate_nutrition(self, meals: List[Dict]) -> Dict[str, Any]:
        """Aggregate nutrition statistics."""
        if not meals:
            return {
                "total_meals_logged": 0,
                "avg_calories_per_day": 0,
                "avg_protein_g_per_day": 0,
                "avg_carbs_g_per_day": 0,
                "avg_fat_g_per_day": 0,
                "days_logged": 0,
            }

        # Get unique days
        days = set(m.get("date") for m in meals if m.get("date"))
        days_logged = len(days)

        total_calories = sum(m.get("calories", 0) for m in meals)
        total_protein = sum(m.get("protein_g", 0) for m in meals)
        total_carbs = sum(m.get("carbs_g", 0) for m in meals)
        total_fat = sum(m.get("fat_g", 0) for m in meals)

        return {
            "total_meals_logged": len(meals),
            "avg_calories_per_day": total_calories / days_logged if days_logged > 0 else 0,
            "avg_protein_g_per_day": total_protein / days_logged if days_logged > 0 else 0,
            "avg_carbs_g_per_day": total_carbs / days_logged if days_logged > 0 else 0,
            "avg_fat_g_per_day": total_fat / days_logged if days_logged > 0 else 0,
            "days_logged": days_logged,
        }

    def _aggregate_activities(self, activities: List[Dict]) -> Dict[str, Any]:
        """Aggregate activity statistics."""
        if not activities:
            return {
                "total_activities": 0,
                "total_distance_miles": 0,
                "total_elevation_feet": 0,
                "activity_types": {},
            }

        activity_types = Counter(a.get("type", "unknown") for a in activities)

        return {
            "total_activities": len(activities),
            "total_distance_miles": sum(a.get("distance_miles", 0) for a in activities),
            "total_elevation_feet": sum(a.get("elevation_feet", 0) for a in activities),
            "activity_types": dict(activity_types),
        }

    async def _save_summary(self, user_id: str, summary: Dict[str, Any]) -> None:
        """Save summary to database."""
        try:
            # Try insert first
            self.supabase.table("summaries").insert({
                "user_id": user_id,
                "period_type": summary["period_type"],
                "period_start": summary["period_start"],
                "period_end": summary["period_end"],
                "data": summary,
            }).execute()
        except Exception as e:
            # If duplicate, update instead
            if "duplicate" in str(e).lower():
                self.supabase.table("summaries").update({
                    "data": summary,
                    "updated_at": datetime.now().isoformat(),
                }).eq("user_id", user_id).eq(
                    "period_type", summary["period_type"]
                ).eq("period_start", summary["period_start"]).execute()
            else:
                raise

    def _is_first_day_of_month(self, date: date) -> bool:
        """Check if date is first day of month."""
        return date.day == 1

    def _is_first_day_of_quarter(self, date: date) -> bool:
        """Check if date is first day of quarter."""
        return date.day == 1 and date.month in [1, 4, 7, 10]

    def _get_quarter(self, date: date) -> int:
        """Get quarter (1-4) for a date."""
        return (date.month - 1) // 3 + 1
