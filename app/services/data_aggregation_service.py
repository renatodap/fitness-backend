"""
Data Aggregation Service

Handles intelligent data aggregation from multiple sources with priority-based conflict resolution.

Source Priority:
1. Garmin - Highest priority (direct sensor data)
2. Apple Watch - High quality wearable
3. Fitbit - Popular wearable
4. Whoop - Specialized recovery tracker
5. Oura - Sleep-focused ring
6. Manual - User entered
7. Quick Entry - AI extracted (lowest priority)

When multiple sources provide the same data (e.g., sleep duration), we use the highest
priority source. For non-conflicting fields, we merge data from all sources.
"""

import logging
from typing import Dict, List, Optional, Any
from datetime import date, datetime
from dataclasses import dataclass

from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


# Source priority mapping (lower number = higher priority)
SOURCE_PRIORITY = {
    "garmin": 1,
    "apple": 2,
    "fitbit": 3,
    "whoop": 4,
    "oura": 5,
    "polar": 6,
    "suunto": 7,
    "wahoo": 8,
    "manual": 9,
    "quick_entry": 10,
}


@dataclass
class AggregatedData:
    """Result of data aggregation with metadata."""
    primary_source: str
    sources_used: List[str]
    data: Dict[str, Any]
    conflicts_resolved: int
    merge_notes: List[str]


class DataAggregationService:
    """
    Service for aggregating data from multiple sources with intelligent conflict resolution.

    Handles:
    - Activity data (duration, distance, calories, heart rate)
    - Sleep data (duration, stages, quality)
    - Health metrics (steps, active calories, intensity minutes)
    - Notes and supplementary information
    """

    def __init__(self):
        """Initialize with Supabase client."""
        self.supabase = get_service_client()

    def get_source_priority(self, source: str) -> int:
        """Get priority value for a source (lower = higher priority)."""
        return SOURCE_PRIORITY.get(source.lower(), 100)

    def resolve_conflict(
        self,
        field_name: str,
        values: Dict[str, Any],
        field_type: str = "numeric"
    ) -> tuple[Any, str]:
        """
        Resolve conflicting values from multiple sources.

        Args:
            field_name: Name of the field (for logging)
            values: Dict mapping source to value
            field_type: Type of field ("numeric", "text", "boolean", "timestamp")

        Returns:
            Tuple of (resolved_value, winning_source)
        """
        if not values:
            return None, None

        # Sort sources by priority (lowest number = highest priority)
        sorted_sources = sorted(values.keys(), key=self.get_source_priority)

        # Use highest priority source
        winning_source = sorted_sources[0]
        winning_value = values[winning_source]

        # For numeric fields, check if values are similar across sources
        if field_type == "numeric" and len(values) > 1:
            numeric_values = [v for v in values.values() if v is not None and isinstance(v, (int, float))]
            if len(numeric_values) >= 2:
                avg = sum(numeric_values) / len(numeric_values)
                max_deviation = max(abs(v - avg) for v in numeric_values)

                # If values are within 10% of each other, average them
                if avg > 0 and (max_deviation / avg) < 0.10:
                    winning_value = round(sum(numeric_values) / len(numeric_values), 2)
                    logger.debug(f"[DataAgg] {field_name}: Averaged similar values from {list(values.keys())}")

        logger.debug(f"[DataAgg] {field_name}: Using {winning_source} value: {winning_value}")
        return winning_value, winning_source

    async def get_aggregated_activity(
        self,
        user_id: str,
        activity_date: date,
        activity_type: Optional[str] = None
    ) -> Optional[AggregatedData]:
        """
        Get aggregated activity data for a specific date.

        If multiple activities exist for the same date and type, merge them
        using source priority rules.

        Args:
            user_id: User UUID
            activity_date: Date to query
            activity_type: Optional activity type filter

        Returns:
            AggregatedData with best-source activity or None
        """
        try:
            # Query all activities for the date
            query = self.supabase.table("activities") \
                .select("*") \
                .eq("user_id", user_id) \
                .eq("is_duplicate", False) \
                .gte("start_date", f"{activity_date.isoformat()}T00:00:00Z") \
                .lte("start_date", f"{activity_date.isoformat()}T23:59:59Z")

            if activity_type:
                query = query.eq("type", activity_type)

            result = query.execute()

            if not result.data or len(result.data) == 0:
                return None

            activities = result.data

            # If only one activity, return it directly
            if len(activities) == 1:
                activity = activities[0]
                return AggregatedData(
                    primary_source=activity["source"],
                    sources_used=[activity["source"]],
                    data=activity,
                    conflicts_resolved=0,
                    merge_notes=[]
                )

            # Multiple activities - aggregate them
            return await self._aggregate_activities(activities)

        except Exception as e:
            logger.error(f"[DataAgg] Failed to aggregate activity: {e}")
            return None

    async def _aggregate_activities(self, activities: List[Dict[str, Any]]) -> AggregatedData:
        """Aggregate multiple activities using source priority."""

        # Sort by source priority
        sorted_activities = sorted(activities, key=lambda a: self.get_source_priority(a["source"]))

        primary_activity = sorted_activities[0]
        sources_used = [a["source"] for a in activities]
        conflicts_resolved = 0
        merge_notes = []

        # Start with primary activity data
        aggregated = primary_activity.copy()

        # Core fields that might conflict
        conflict_fields = [
            ("duration_minutes", "numeric"),
            ("distance_meters", "numeric"),
            ("calories", "numeric"),
            ("average_heartrate", "numeric"),
            ("max_heartrate", "numeric"),
            ("average_pace", "text"),
            ("elevation_gain_meters", "numeric"),
            ("perceived_exertion", "numeric"),
        ]

        # Resolve conflicts for each field
        for field_name, field_type in conflict_fields:
            values = {}
            for activity in activities:
                if activity.get(field_name) is not None:
                    values[activity["source"]] = activity[field_name]

            if len(values) > 1:
                resolved_value, winning_source = self.resolve_conflict(field_name, values, field_type)
                aggregated[field_name] = resolved_value
                conflicts_resolved += 1

                if winning_source != primary_activity["source"]:
                    merge_notes.append(f"{field_name} from {winning_source}")

        # Merge notes from all sources
        all_notes = []
        for activity in activities:
            if activity.get("notes"):
                source_label = f"[{activity['source'].upper()}]"
                all_notes.append(f"{source_label} {activity['notes']}")

        if all_notes:
            aggregated["notes"] = "\n\n".join(all_notes)
            merge_notes.append(f"Combined notes from {len(all_notes)} sources")

        # Merge exercises (for strength training)
        if aggregated.get("type") == "strength_training":
            all_exercises = []
            for activity in activities:
                if activity.get("exercises"):
                    all_exercises.extend(activity["exercises"])

            if all_exercises:
                aggregated["exercises"] = all_exercises
                merge_notes.append(f"Combined {len(all_exercises)} exercises")

        logger.info(
            f"[DataAgg] Aggregated {len(activities)} activities: "
            f"primary={primary_activity['source']}, conflicts={conflicts_resolved}"
        )

        return AggregatedData(
            primary_source=primary_activity["source"],
            sources_used=sources_used,
            data=aggregated,
            conflicts_resolved=conflicts_resolved,
            merge_notes=merge_notes
        )

    async def get_aggregated_sleep(
        self,
        user_id: str,
        sleep_date: date
    ) -> Optional[AggregatedData]:
        """
        Get aggregated sleep data for a specific date.

        Sleep data can come from:
        - Garmin (full sleep stages + HRV)
        - Apple Watch (basic sleep tracking)
        - Manual entry (user logged)
        - Morning check-in (quality rating only)

        Args:
            user_id: User UUID
            sleep_date: Date of sleep (the night)

        Returns:
            AggregatedData with best-source sleep or None
        """
        try:
            result = self.supabase.table("sleep_logs") \
                .select("*") \
                .eq("user_id", user_id) \
                .eq("sleep_date", sleep_date.isoformat()) \
                .execute()

            if not result.data or len(result.data) == 0:
                return None

            sleep_logs = result.data

            # If only one log, return it
            if len(sleep_logs) == 1:
                log = sleep_logs[0]
                return AggregatedData(
                    primary_source=log["source"],
                    sources_used=[log["source"]],
                    data=log,
                    conflicts_resolved=0,
                    merge_notes=[]
                )

            # Multiple logs - aggregate
            return await self._aggregate_sleep_logs(sleep_logs)

        except Exception as e:
            logger.error(f"[DataAgg] Failed to aggregate sleep: {e}")
            return None

    async def _aggregate_sleep_logs(self, logs: List[Dict[str, Any]]) -> AggregatedData:
        """Aggregate multiple sleep logs using source priority."""

        sorted_logs = sorted(logs, key=lambda l: self.get_source_priority(l["source"]))

        primary_log = sorted_logs[0]
        sources_used = [l["source"] for l in logs]
        conflicts_resolved = 0
        merge_notes = []

        aggregated = primary_log.copy()

        # Sleep-specific conflict fields
        conflict_fields = [
            ("total_sleep_minutes", "numeric"),
            ("deep_sleep_minutes", "numeric"),
            ("light_sleep_minutes", "numeric"),
            ("rem_sleep_minutes", "numeric"),
            ("awake_minutes", "numeric"),
            ("sleep_score", "numeric"),
            ("avg_hrv_ms", "numeric"),
            ("avg_heart_rate", "numeric"),
            ("lowest_heart_rate", "numeric"),
        ]

        for field_name, field_type in conflict_fields:
            values = {}
            for log in logs:
                if log.get(field_name) is not None:
                    values[log["source"]] = log[field_name]

            if len(values) > 1:
                resolved_value, winning_source = self.resolve_conflict(field_name, values, field_type)
                aggregated[field_name] = resolved_value
                conflicts_resolved += 1

                if winning_source != primary_log["source"]:
                    merge_notes.append(f"{field_name} from {winning_source}")

        # Merge notes
        all_notes = []
        for log in logs:
            if log.get("notes"):
                all_notes.append(f"[{log['source'].upper()}] {log['notes']}")

        if all_notes:
            aggregated["notes"] = "\n\n".join(all_notes)

        logger.info(
            f"[DataAgg] Aggregated {len(logs)} sleep logs: "
            f"primary={primary_log['source']}, conflicts={conflicts_resolved}"
        )

        return AggregatedData(
            primary_source=primary_log["source"],
            sources_used=sources_used,
            data=aggregated,
            conflicts_resolved=conflicts_resolved,
            merge_notes=merge_notes
        )

    async def get_best_source_data(
        self,
        user_id: str,
        table_name: str,
        date_field: str,
        target_date: date
    ) -> Optional[Dict[str, Any]]:
        """
        Generic method to get best-source data from any table.

        Args:
            user_id: User UUID
            table_name: Table to query (e.g., 'hrv_logs', 'stress_logs')
            date_field: Date field name to filter on
            target_date: Date to query

        Returns:
            Best-source record or None
        """
        try:
            result = self.supabase.table(table_name) \
                .select("*") \
                .eq("user_id", user_id) \
                .eq(date_field, target_date.isoformat()) \
                .execute()

            if not result.data or len(result.data) == 0:
                return None

            records = result.data

            # If single record, return it
            if len(records) == 1:
                return records[0]

            # Multiple records - return highest priority source
            sorted_records = sorted(records, key=lambda r: self.get_source_priority(r.get("source", "manual")))

            best_record = sorted_records[0]

            logger.debug(
                f"[DataAgg] {table_name}: Using {best_record.get('source')} "
                f"(had {len(records)} sources)"
            )

            return best_record

        except Exception as e:
            logger.error(f"[DataAgg] Failed to get best source from {table_name}: {e}")
            return None
