"""
Context Detector Service

Detects user context to enable intelligent personality modulation.

This service adds MINIMAL safety intelligence while keeping the hardcore
intensity-driven personality. It detects:
- Injuries/pain mentions
- Rest day situations
- Over-training patterns
- Under-eating patterns
- Goal-crushing momentum

95% of interactions remain full intensity. 5% adapt for science-backed safety.
"""

import logging
import re
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

logger = logging.getLogger(__name__)


class ContextDetector:
    """
    Detect user context for personality modulation.

    Strategy:
    1. Check message text for injury/pain keywords
    2. Analyze recent activity data for over-training
    3. Analyze recent nutrition data for under-eating
    4. Determine if user is crushing goals or needs support
    """

    def __init__(self):
        # Injury/pain keywords (multilingual)
        self.injury_keywords = [
            # English
            r'\b(hurt|pain|injury|injured|sore|pulled|strain|sprain|ache|aching)\b',
            r'\b(can\'t move|too sore|really sore|very sore)\b',
            # Portuguese
            r'\b(dor|dolorido|machucado|lesão|lesionado)\b',
            # Spanish
            r'\b(dolor|dolorido|lesión|lesionado)\b',
        ]

        # Recovery/rest keywords
        self.rest_keywords = [
            r'\b(rest day|resting|recovery|recovering|taking a break)\b',
            r'\b(dia de descanso|descansando|recuperação)\b',
            r'\b(día de descanso|descansando|recuperación)\b',
        ]

    async def detect_context(
        self,
        user_id: str,
        message: str,
        recent_activities: Optional[List[Dict[str, Any]]] = None,
        nutrition_summary: Optional[Dict[str, Any]] = None,
        user_profile: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Detect user context for personality modulation.

        Args:
            user_id: User's UUID
            message: Current message text
            recent_activities: Recent workout data (optional)
            nutrition_summary: Today's nutrition summary (optional)
            user_profile: User profile with targets (optional)

        Returns:
            {
                "context": "normal" | "injury" | "rest_day" | "over_training" | "under_eating" | "crushing_it",
                "confidence": float (0.0-1.0),
                "reasoning": str,
                "safety_concern": bool,
                "suggested_tone": str
            }
        """
        logger.info(f"[ContextDetector] Analyzing context for user: {user_id[:8]}...")

        # CHECK 1: Injury/pain mentions (HIGHEST PRIORITY)
        injury_detected = self._detect_injury_mention(message)
        if injury_detected:
            logger.warning(f"[ContextDetector] INJURY detected: {injury_detected['reasoning']}")
            return {
                "context": "injury",
                "confidence": injury_detected["confidence"],
                "reasoning": injury_detected["reasoning"],
                "safety_concern": True,
                "suggested_tone": "supportive_recovery"
            }

        # CHECK 2: Rest day (explicit mention or no recent activity)
        rest_day = self._detect_rest_day(message, recent_activities)
        if rest_day:
            logger.info(f"[ContextDetector] REST DAY detected: {rest_day['reasoning']}")
            return {
                "context": "rest_day",
                "confidence": rest_day["confidence"],
                "reasoning": rest_day["reasoning"],
                "safety_concern": False,
                "suggested_tone": "rest_is_part_of_process"
            }

        # CHECK 3: Over-training (too many consecutive high-intensity days)
        if recent_activities:
            over_training = self._detect_over_training(recent_activities)
            if over_training:
                logger.warning(f"[ContextDetector] OVER-TRAINING detected: {over_training['reasoning']}")
                return {
                    "context": "over_training",
                    "confidence": over_training["confidence"],
                    "reasoning": over_training["reasoning"],
                    "safety_concern": True,
                    "suggested_tone": "smart_rest"
                }

        # CHECK 4: Under-eating (significant calorie deficit)
        if nutrition_summary and user_profile:
            under_eating = self._detect_under_eating(nutrition_summary, user_profile)
            if under_eating:
                logger.warning(f"[ContextDetector] UNDER-EATING detected: {under_eating['reasoning']}")
                return {
                    "context": "under_eating",
                    "confidence": under_eating["confidence"],
                    "reasoning": under_eating["reasoning"],
                    "safety_concern": True,
                    "suggested_tone": "fuel_performance"
                }

        # CHECK 5: Crushing goals (hitting targets consistently)
        if nutrition_summary and user_profile:
            crushing_it = self._detect_crushing_goals(nutrition_summary, user_profile, recent_activities)
            if crushing_it:
                logger.info(f"[ContextDetector] CRUSHING IT detected: {crushing_it['reasoning']}")
                return {
                    "context": "crushing_it",
                    "confidence": crushing_it["confidence"],
                    "reasoning": crushing_it["reasoning"],
                    "safety_concern": False,
                    "suggested_tone": "celebrate_loud"
                }

        # DEFAULT: Normal Goggins mode
        logger.info("[ContextDetector] Normal context - FULL GOGGINS MODE")
        return {
            "context": "normal",
            "confidence": 1.0,
            "reasoning": "No special context detected - full intensity mode",
            "safety_concern": False,
            "suggested_tone": "full_goggins"
        }

    def _detect_injury_mention(self, message: str) -> Optional[Dict[str, Any]]:
        """
        Detect injury/pain mentions in message text.

        Returns context dict if detected, None otherwise.
        """
        message_lower = message.lower()

        for pattern in self.injury_keywords:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return {
                    "confidence": 0.9,
                    "reasoning": f"User mentioned injury/pain: '{message[:50]}...'"
                }

        return None

    def _detect_rest_day(
        self,
        message: str,
        recent_activities: Optional[List[Dict[str, Any]]]
    ) -> Optional[Dict[str, Any]]:
        """
        Detect rest day from message or activity patterns.

        Returns context dict if detected, None otherwise.
        """
        message_lower = message.lower()

        # Check for explicit rest day mention
        for pattern in self.rest_keywords:
            if re.search(pattern, message_lower, re.IGNORECASE):
                return {
                    "confidence": 0.85,
                    "reasoning": "User explicitly mentioned rest/recovery"
                }

        # Check recent activity patterns (if provided)
        if recent_activities:
            # Count workouts in last 3 days
            three_days_ago = datetime.utcnow() - timedelta(days=3)
            recent_workouts = [
                a for a in recent_activities
                if datetime.fromisoformat(a.get("logged_at", "").replace("Z", "+00:00")) > three_days_ago
            ]

            # If no workouts in 3 days, might be rest period
            if len(recent_workouts) == 0:
                return {
                    "confidence": 0.6,
                    "reasoning": "No workouts logged in last 3 days - possible rest period"
                }

        return None

    def _detect_over_training(
        self,
        recent_activities: List[Dict[str, Any]]
    ) -> Optional[Dict[str, Any]]:
        """
        Detect over-training from activity patterns.

        Over-training indicators:
        - 7+ consecutive days of intense training
        - Very high weekly volume (>12 hours)
        - Multiple high-intensity sessions per day

        Returns context dict if detected, None otherwise.
        """
        if not recent_activities:
            return None

        # Count consecutive training days in last 7 days
        seven_days_ago = datetime.utcnow() - timedelta(days=7)
        week_activities = [
            a for a in recent_activities
            if datetime.fromisoformat(a.get("logged_at", "").replace("Z", "+00:00")) > seven_days_ago
        ]

        # Calculate unique training days
        training_dates = set()
        total_duration = 0
        for activity in week_activities:
            date = activity.get("logged_at", "").split("T")[0]
            training_dates.add(date)
            total_duration += activity.get("duration_minutes", 0)

        # RED FLAG 1: 7+ consecutive training days
        if len(training_dates) >= 7:
            return {
                "confidence": 0.8,
                "reasoning": f"User trained {len(training_dates)} consecutive days - rest needed"
            }

        # RED FLAG 2: Excessive weekly volume (>12 hours = 720 minutes)
        if total_duration > 720:
            return {
                "confidence": 0.75,
                "reasoning": f"Weekly volume: {total_duration}min (>12 hours) - recovery recommended"
            }

        return None

    def _detect_under_eating(
        self,
        nutrition_summary: Dict[str, Any],
        user_profile: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """
        Detect under-eating from nutrition data.

        Under-eating indicators:
        - Calories <70% of target
        - Protein <50% of target
        - Zero calories logged (possible skipped meals)

        Returns context dict if detected, None otherwise.
        """
        # Get today's totals
        summary = nutrition_summary.get("summary", {})
        total_calories = summary.get("total_calories", 0)
        total_protein = summary.get("total_protein_g", 0)

        # Get targets
        profile = user_profile.get("profile", {})
        target_calories = profile.get("daily_calorie_target", 2000)
        target_protein = profile.get("daily_protein_target_g", 150)

        # RED FLAG 1: Calories significantly below target (<70%)
        if target_calories > 0:
            calorie_ratio = total_calories / target_calories
            if calorie_ratio < 0.7 and total_calories > 0:
                return {
                    "confidence": 0.85,
                    "reasoning": f"Calories: {total_calories}/{target_calories} ({calorie_ratio*100:.0f}%) - significantly under target"
                }

        # RED FLAG 2: Protein critically low (<50%)
        if target_protein > 0:
            protein_ratio = total_protein / target_protein
            if protein_ratio < 0.5 and total_protein > 0:
                return {
                    "confidence": 0.8,
                    "reasoning": f"Protein: {total_protein}g/{target_protein}g ({protein_ratio*100:.0f}%) - critically low"
                }

        # RED FLAG 3: No food logged (possible skipped meals)
        if total_calories == 0:
            return {
                "confidence": 0.6,
                "reasoning": "No food logged today - ensure proper fueling"
            }

        return None

    def _detect_crushing_goals(
        self,
        nutrition_summary: Dict[str, Any],
        user_profile: Dict[str, Any],
        recent_activities: Optional[List[Dict[str, Any]]]
    ) -> Optional[Dict[str, Any]]:
        """
        Detect goal-crushing momentum.

        Indicators:
        - Calories within 10% of target
        - Protein at or above target
        - Consistent workout schedule

        Returns context dict if detected, None otherwise.
        """
        # Get today's totals
        summary = nutrition_summary.get("summary", {})
        total_calories = summary.get("total_calories", 0)
        total_protein = summary.get("total_protein_g", 0)

        # Get targets
        profile = user_profile.get("profile", {})
        target_calories = profile.get("daily_calorie_target", 2000)
        target_protein = profile.get("daily_protein_target_g", 150)

        # Check nutrition targets
        nutrition_on_point = False
        if target_calories > 0 and target_protein > 0:
            calorie_ratio = total_calories / target_calories
            protein_ratio = total_protein / target_protein

            # Calories within 10% and protein at/above target
            if 0.9 <= calorie_ratio <= 1.1 and protein_ratio >= 0.9:
                nutrition_on_point = True

        # Check workout consistency
        workout_consistent = False
        if recent_activities:
            seven_days_ago = datetime.utcnow() - timedelta(days=7)
            week_activities = [
                a for a in recent_activities
                if datetime.fromisoformat(a.get("logged_at", "").replace("Z", "+00:00")) > seven_days_ago
            ]

            # 3-5 workouts in last week = consistent
            if 3 <= len(week_activities) <= 5:
                workout_consistent = True

        # CRUSHING IT: Both nutrition and workouts on point
        if nutrition_on_point and workout_consistent:
            return {
                "confidence": 0.9,
                "reasoning": "Nutrition dialed in + consistent training - crushing it!"
            }

        # Partial win: Nutrition on point
        if nutrition_on_point:
            return {
                "confidence": 0.7,
                "reasoning": "Nutrition targets hit - excellent work!"
            }

        return None


# Singleton instance
_context_detector: Optional[ContextDetector] = None


def get_context_detector() -> ContextDetector:
    """Get the global ContextDetector instance."""
    global _context_detector
    if _context_detector is None:
        _context_detector = ContextDetector()
    return _context_detector
