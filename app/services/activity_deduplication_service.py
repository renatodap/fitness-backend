"""
Activity Deduplication Service

Detects and manages duplicate activities from multiple sources (Garmin, Manual, Quick Entry).

Detection Signals:
- Time proximity: Activities within ±30 minutes
- Duration similarity: Within 10% of each other
- Distance similarity: Within 10% (if both have distance)
- Same activity type
- Heart rate similarity: Within 10 bpm (if both have HR)
- Calories similarity: Within 10% (if both have calories)

Confidence Scoring (0-100):
- 100: Perfect match (all signals match exactly)
- 90-99: Very high confidence (time ±5min, duration/distance ±5%)
- 80-89: High confidence (time ±15min, duration/distance ±10%)
- 50-79: Medium confidence (time ±30min, some signals match)
- <50: Low confidence (weak match)

Auto-Merge Rules:
- Confidence >95%: Always auto-merge
- Confidence >90% AND same source: Auto-merge (likely sync duplicate)
- Confidence 80-95%: Create merge request (user approval needed)
- Confidence <80%: Ignore (different activities)
"""

import logging
from typing import Optional, List, Dict, Any, Tuple
from datetime import datetime, timedelta
from dataclasses import dataclass

from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)

# Deduplication thresholds
TIME_WINDOW_MINUTES = 30  # Activities within ±30 minutes
DURATION_THRESHOLD_PCT = 10  # Duration within 10%
DISTANCE_THRESHOLD_PCT = 10  # Distance within 10%
HR_THRESHOLD_BPM = 10  # Heart rate within 10 bpm
CALORIES_THRESHOLD_PCT = 10  # Calories within 10%

# Confidence thresholds
CONFIDENCE_AUTO_MERGE = 95  # Auto-merge if >95%
CONFIDENCE_HIGH = 80  # Create merge request if >80%
CONFIDENCE_SAME_SOURCE_AUTO = 90  # Auto-merge same source if >90%


@dataclass
class DuplicateMatch:
    """Result of duplicate detection."""
    primary_activity_id: str
    duplicate_activity_id: str
    confidence_score: int
    merge_reason: Dict[str, Any]
    should_auto_merge: bool


class ActivityDeduplicationService:
    """
    Service for detecting and managing duplicate activities.

    Handles:
    - Duplicate detection across all sources
    - Confidence scoring based on multiple signals
    - Automatic merging for high-confidence matches
    - Merge request creation for user approval
    """

    def __init__(self):
        """Initialize with Supabase service client."""
        self.supabase = get_service_client()

    def calculate_time_diff_minutes(
        self,
        time1: str,
        time2: str
    ) -> int:
        """Calculate time difference in minutes between two ISO timestamps."""
        dt1 = datetime.fromisoformat(time1.replace('Z', '+00:00'))
        dt2 = datetime.fromisoformat(time2.replace('Z', '+00:00'))
        return abs(int((dt1 - dt2).total_seconds() / 60))

    def calculate_percentage_diff(
        self,
        value1: float,
        value2: float
    ) -> float:
        """Calculate percentage difference between two values."""
        if value1 == 0 and value2 == 0:
            return 0.0
        if value1 == 0 or value2 == 0:
            return 100.0

        avg = (value1 + value2) / 2
        diff = abs(value1 - value2)
        return (diff / avg) * 100

    def detect_duplicate(
        self,
        activity1: Dict[str, Any],
        activity2: Dict[str, Any]
    ) -> Optional[DuplicateMatch]:
        """
        Detect if two activities are duplicates and calculate confidence.

        Args:
            activity1: First activity dict
            activity2: Second activity dict

        Returns:
            DuplicateMatch if duplicate detected, None otherwise
        """
        # Check if same user
        if activity1['user_id'] != activity2['user_id']:
            return None

        # Check if already marked as duplicate
        if activity1.get('is_duplicate') or activity2.get('is_duplicate'):
            return None

        # Initialize match signals
        signals = {
            'time_match': False,
            'duration_match': False,
            'distance_match': False,
            'type_match': False,
            'hr_match': False,
            'calories_match': False,
        }

        merge_reason = {}

        # Signal 1: Time proximity (±30 minutes)
        time_diff = self.calculate_time_diff_minutes(
            activity1['start_date'],
            activity2['start_date']
        )
        merge_reason['time_diff_minutes'] = time_diff

        if time_diff <= TIME_WINDOW_MINUTES:
            signals['time_match'] = True
        else:
            # Time difference too large, not a duplicate
            return None

        # Signal 2: Activity type match
        type1 = activity1.get('type', '').lower()
        type2 = activity2.get('type', '').lower()
        signals['type_match'] = (type1 == type2)
        merge_reason['same_type'] = signals['type_match']

        # Signal 3: Duration similarity (±10%)
        duration1 = activity1.get('duration_minutes', 0)
        duration2 = activity2.get('duration_minutes', 0)

        if duration1 > 0 and duration2 > 0:
            duration_diff_pct = self.calculate_percentage_diff(duration1, duration2)
            merge_reason['duration_diff_pct'] = round(duration_diff_pct, 2)

            if duration_diff_pct <= DURATION_THRESHOLD_PCT:
                signals['duration_match'] = True

        # Signal 4: Distance similarity (±10%, if both have distance)
        distance1 = activity1.get('distance_meters', 0)
        distance2 = activity2.get('distance_meters', 0)

        if distance1 > 0 and distance2 > 0:
            distance_diff_pct = self.calculate_percentage_diff(distance1, distance2)
            merge_reason['distance_diff_pct'] = round(distance_diff_pct, 2)

            if distance_diff_pct <= DISTANCE_THRESHOLD_PCT:
                signals['distance_match'] = True

        # Signal 5: Heart rate similarity (±10 bpm, if both have HR)
        hr1 = activity1.get('average_heartrate', 0)
        hr2 = activity2.get('average_heartrate', 0)

        if hr1 > 0 and hr2 > 0:
            hr_diff = abs(hr1 - hr2)
            merge_reason['hr_diff_bpm'] = hr_diff

            if hr_diff <= HR_THRESHOLD_BPM:
                signals['hr_match'] = True

        # Signal 6: Calories similarity (±10%, if both have calories)
        cal1 = activity1.get('calories', 0)
        cal2 = activity2.get('calories', 0)

        if cal1 > 0 and cal2 > 0:
            cal_diff_pct = self.calculate_percentage_diff(cal1, cal2)
            merge_reason['calories_diff_pct'] = round(cal_diff_pct, 2)

            if cal_diff_pct <= CALORIES_THRESHOLD_PCT:
                signals['calories_match'] = True

        # Calculate confidence score
        confidence = self._calculate_confidence(
            signals=signals,
            merge_reason=merge_reason,
            activity1=activity1,
            activity2=activity2
        )

        # Not confident enough, ignore
        if confidence < CONFIDENCE_HIGH:
            return None

        # Determine which activity is primary (prefer higher quality source)
        primary, duplicate = self._determine_primary_activity(activity1, activity2)

        # Determine if should auto-merge
        same_source = activity1['source'] == activity2['source']
        should_auto_merge = (
            confidence >= CONFIDENCE_AUTO_MERGE or
            (same_source and confidence >= CONFIDENCE_SAME_SOURCE_AUTO)
        )

        merge_reason['signals_matched'] = [k for k, v in signals.items() if v]
        merge_reason['same_source'] = same_source

        return DuplicateMatch(
            primary_activity_id=primary['id'],
            duplicate_activity_id=duplicate['id'],
            confidence_score=confidence,
            merge_reason=merge_reason,
            should_auto_merge=should_auto_merge
        )

    def _calculate_confidence(
        self,
        signals: Dict[str, bool],
        merge_reason: Dict[str, Any],
        activity1: Dict[str, Any],
        activity2: Dict[str, Any]
    ) -> int:
        """
        Calculate confidence score (0-100) based on matching signals.

        Scoring:
        - Base: 40 points for time + type match
        - Duration match: +20 points
        - Distance match: +20 points
        - HR match: +10 points
        - Calories match: +10 points
        - Bonus for very close matches: +10 points
        """
        score = 0

        # Base score: Time proximity + type match
        if signals['time_match'] and signals['type_match']:
            score += 40

        # Duration match
        if signals['duration_match']:
            score += 20
            # Bonus for very close duration (<5%)
            if merge_reason.get('duration_diff_pct', 100) < 5:
                score += 5

        # Distance match
        if signals['distance_match']:
            score += 20
            # Bonus for very close distance (<5%)
            if merge_reason.get('distance_diff_pct', 100) < 5:
                score += 5

        # Heart rate match
        if signals['hr_match']:
            score += 10

        # Calories match
        if signals['calories_match']:
            score += 10

        # Bonus for very close time match (<5 minutes)
        if merge_reason.get('time_diff_minutes', 100) < 5:
            score += 10

        # Bonus for exact time match
        if merge_reason.get('time_diff_minutes', 100) == 0:
            score += 10

        return min(100, score)

    def _determine_primary_activity(
        self,
        activity1: Dict[str, Any],
        activity2: Dict[str, Any]
    ) -> Tuple[Dict[str, Any], Dict[str, Any]]:
        """
        Determine which activity should be primary (kept) vs duplicate (merged).

        Priority:
        1. Data completeness (more fields filled)
        2. Source quality (Garmin > Apple > Manual > Quick Entry)
        3. Created first (earlier created_at)
        """
        from app.services.data_aggregation_service import SOURCE_PRIORITY

        # Count data completeness
        def count_data_fields(activity: Dict[str, Any]) -> int:
            fields = [
                'duration_minutes', 'distance_meters', 'calories',
                'average_heartrate', 'max_heartrate', 'average_pace',
                'elevation_gain_meters', 'notes'
            ]
            return sum(1 for f in fields if activity.get(f))

        completeness1 = count_data_fields(activity1)
        completeness2 = count_data_fields(activity2)

        # Compare data completeness (prefer more complete)
        if completeness1 > completeness2:
            return activity1, activity2
        elif completeness2 > completeness1:
            return activity2, activity1

        # Compare source quality
        priority1 = SOURCE_PRIORITY.get(activity1['source'].lower(), 100)
        priority2 = SOURCE_PRIORITY.get(activity2['source'].lower(), 100)

        if priority1 < priority2:  # Lower priority number = better
            return activity1, activity2
        elif priority2 < priority1:
            return activity2, activity1

        # Same quality, prefer earlier created
        created1 = datetime.fromisoformat(activity1['created_at'].replace('Z', '+00:00'))
        created2 = datetime.fromisoformat(activity2['created_at'].replace('Z', '+00:00'))

        if created1 <= created2:
            return activity1, activity2
        else:
            return activity2, activity1

    async def detect_duplicates_for_activity(
        self,
        activity_id: str,
        user_id: str
    ) -> List[DuplicateMatch]:
        """
        Detect duplicates for a specific activity.

        Args:
            activity_id: Activity UUID to check
            user_id: User UUID (for security)

        Returns:
            List of DuplicateMatch results
        """
        try:
            # Get the activity
            result = self.supabase.table("activities") \
                .select("*") \
                .eq("id", activity_id) \
                .eq("user_id", user_id) \
                .eq("is_duplicate", False) \
                .single() \
                .execute()

            if not result.data:
                logger.warning(f"[Dedup] Activity not found: {activity_id}")
                return []

            activity = result.data

            # Get potential duplicates (same user, similar time, not already duplicate)
            start_time = datetime.fromisoformat(activity['start_date'].replace('Z', '+00:00'))
            time_window_start = (start_time - timedelta(minutes=TIME_WINDOW_MINUTES)).isoformat()
            time_window_end = (start_time + timedelta(minutes=TIME_WINDOW_MINUTES)).isoformat()

            candidates_result = self.supabase.table("activities") \
                .select("*") \
                .eq("user_id", user_id) \
                .eq("is_duplicate", False) \
                .neq("id", activity_id) \
                .gte("start_date", time_window_start) \
                .lte("start_date", time_window_end) \
                .execute()

            if not candidates_result.data:
                return []

            # Check each candidate
            matches = []
            for candidate in candidates_result.data:
                match = self.detect_duplicate(activity, candidate)
                if match:
                    matches.append(match)

            logger.info(f"[Dedup] Found {len(matches)} potential duplicates for activity {activity_id}")
            return matches

        except Exception as e:
            logger.error(f"[Dedup] Failed to detect duplicates: {e}")
            return []

    async def create_merge_requests(
        self,
        matches: List[DuplicateMatch],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Create merge requests for detected duplicates.

        Args:
            matches: List of DuplicateMatch results
            user_id: User UUID

        Returns:
            Dict with results (created, auto_merged counts)
        """
        try:
            created = 0
            auto_merged = 0

            for match in matches:
                if match.should_auto_merge:
                    # Auto-merge high confidence duplicates
                    await self._auto_merge_duplicate(match, user_id)
                    auto_merged += 1
                else:
                    # Create merge request for user approval
                    await self._create_merge_request(match, user_id)
                    created += 1

            logger.info(
                f"[Dedup] Created {created} merge requests, "
                f"auto-merged {auto_merged} for user {user_id}"
            )

            return {
                "success": True,
                "merge_requests_created": created,
                "auto_merged": auto_merged
            }

        except Exception as e:
            logger.error(f"[Dedup] Failed to create merge requests: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def _create_merge_request(
        self,
        match: DuplicateMatch,
        user_id: str
    ) -> None:
        """Create a merge request in the database."""
        self.supabase.table("activity_merge_requests").insert({
            "user_id": user_id,
            "primary_activity_id": match.primary_activity_id,
            "duplicate_activity_id": match.duplicate_activity_id,
            "confidence_score": match.confidence_score,
            "status": "pending",
            "merge_reason": match.merge_reason
        }).execute()

    async def _auto_merge_duplicate(
        self,
        match: DuplicateMatch,
        user_id: str
    ) -> None:
        """Automatically merge a high-confidence duplicate."""
        # Mark as duplicate
        self.supabase.table("activities").update({
            "is_duplicate": True,
            "duplicate_of": match.primary_activity_id
        }).eq("id", match.duplicate_activity_id).execute()

        # Create merge request record (for history)
        self.supabase.table("activity_merge_requests").insert({
            "user_id": user_id,
            "primary_activity_id": match.primary_activity_id,
            "duplicate_activity_id": match.duplicate_activity_id,
            "confidence_score": match.confidence_score,
            "status": "auto_merged",
            "merge_reason": match.merge_reason,
            "resolved_at": datetime.utcnow().isoformat(),
            "resolved_by": "auto"
        }).execute()

    async def get_pending_merge_requests(
        self,
        user_id: str,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get pending merge requests for user.

        Args:
            user_id: User UUID
            limit: Maximum results

        Returns:
            List of merge requests with activity details
        """
        try:
            result = self.supabase.table("activity_merge_requests") \
                .select("*, primary:primary_activity_id(*), duplicate:duplicate_activity_id(*)") \
                .eq("user_id", user_id) \
                .eq("status", "pending") \
                .order("confidence_score", desc=True) \
                .limit(limit) \
                .execute()

            return result.data or []

        except Exception as e:
            logger.error(f"[Dedup] Failed to get merge requests: {e}")
            return []
