"""
Enrichment Service for Quick Entry Data

DETERMINISTIC enrichment using mathematical calculations, not LLMs.
This saves costs and provides consistent, reliable results.

Enrichment types:
1. Meal quality scores (nutrition balance, macro ratios)
2. Workout progressive overload detection
3. Activity performance scoring
4. Smart tag generation
5. Recovery time estimation
6. Sentiment analysis for notes (using Groq for ultra-cheap sentiment detection)
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


class EnrichmentService:
    """
    Deterministic enrichment service for quick entry data.

    Most calculations are mathematical and rule-based (no LLM calls).
    Exception: Sentiment analysis uses Groq for ultra-cheap LLM sentiment detection.
    """

    def __init__(self):
        self.supabase = get_service_client()
        # Import here to avoid circular dependency
        from app.services.groq_service import get_groq_service
        self.groq_service = get_groq_service()

    # =============================================================================
    # MEAL ENRICHMENT
    # =============================================================================

    def enrich_meal(
        self,
        user_id: str,
        meal_data: Dict[str, Any],
        user_targets: Optional[Dict[str, int]] = None
    ) -> Dict[str, Any]:
        """
        Enrich meal data with quality scores, macro balance, adherence to goals.

        Args:
            user_id: User ID
            meal_data: Meal data from LLM extraction
            user_targets: User's daily nutrition targets

        Returns:
            Enriched meal data with scores and tags
        """
        enrichment = {}

        # Get user targets if not provided
        if not user_targets:
            user_targets = self._get_user_nutrition_targets(user_id)

        # Calculate meal quality score (0-10)
        enrichment['meal_quality_score'] = self._calculate_meal_quality_score(meal_data)

        # Calculate macro balance score (0-10)
        enrichment['macro_balance_score'] = self._calculate_macro_balance_score(meal_data)

        # Calculate adherence to goals (0-10)
        if user_targets:
            enrichment['adherence_to_goals'] = self._calculate_goal_adherence(
                meal_data, user_targets
            )

        # Generate smart tags
        enrichment['tags'] = self._generate_meal_tags(meal_data)

        return enrichment

    def _calculate_meal_quality_score(self, meal_data: Dict[str, Any]) -> float:
        """
        Calculate meal quality score (0-10) based on nutritional content.

        Factors:
        - Protein content (higher is better)
        - Fiber content (higher is better)
        - Sugar content (lower is better, unless post-workout)
        - Sodium content (moderate is better)
        - Calorie density
        """
        score = 5.0  # Start at neutral

        protein = meal_data.get('protein_g', 0)
        carbs = meal_data.get('carbs_g', 0)
        fat = meal_data.get('fat_g', 0)
        fiber = meal_data.get('fiber_g', 0)
        sugar = meal_data.get('sugar_g', 0)
        sodium = meal_data.get('sodium_mg', 0)
        calories = meal_data.get('calories', 0)

        # High protein bonus (+2 points for 30g+)
        if protein >= 30:
            score += 2.0
        elif protein >= 20:
            score += 1.0

        # High fiber bonus (+1 point for 5g+)
        if fiber >= 5:
            score += 1.0
        elif fiber >= 3:
            score += 0.5

        # Low sugar bonus (+1 point for <10g)
        if sugar < 10:
            score += 1.0
        elif sugar > 30:
            score -= 1.0

        # Moderate sodium (+0.5 for 200-600mg, -1 for >1500mg)
        if 200 <= sodium <= 600:
            score += 0.5
        elif sodium > 1500:
            score -= 1.0

        # Balanced macros (+1 if reasonable ratios)
        total_macros = protein + carbs + fat
        if total_macros > 0:
            protein_pct = (protein * 4 / calories * 100) if calories > 0 else 0
            carbs_pct = (carbs * 4 / calories * 100) if calories > 0 else 0
            fat_pct = (fat * 9 / calories * 100) if calories > 0 else 0

            # Good balance: 20-40% protein, 20-50% carbs, 20-35% fat
            if 20 <= protein_pct <= 40 and 20 <= carbs_pct <= 50 and 20 <= fat_pct <= 35:
                score += 1.0

        # Clamp score to 0-10
        return max(0.0, min(10.0, score))

    def _calculate_macro_balance_score(self, meal_data: Dict[str, Any]) -> float:
        """
        Calculate macro balance score (0-10) based on protein:carb:fat ratio.

        Ideal ratios depend on meal type:
        - Pre-workout: Higher carbs
        - Post-workout: Higher protein + carbs
        - General: Balanced (30:40:30)
        """
        protein = meal_data.get('protein_g', 0)
        carbs = meal_data.get('carbs_g', 0)
        fat = meal_data.get('fat_g', 0)
        calories = meal_data.get('calories', 0)

        if calories == 0:
            return 5.0

        # Calculate macronutrient percentages
        protein_cals = protein * 4
        carbs_cals = carbs * 4
        fat_cals = fat * 9
        total_cals = protein_cals + carbs_cals + fat_cals

        if total_cals == 0:
            return 5.0

        protein_pct = (protein_cals / total_cals) * 100
        carbs_pct = (carbs_cals / total_cals) * 100
        fat_pct = (fat_cals / total_cals) * 100

        # Ideal balance: 30% protein, 40% carbs, 30% fat
        ideal_protein = 30
        ideal_carbs = 40
        ideal_fat = 30

        # Calculate deviation from ideal
        protein_deviation = abs(protein_pct - ideal_protein)
        carbs_deviation = abs(carbs_pct - ideal_carbs)
        fat_deviation = abs(fat_pct - ideal_fat)

        avg_deviation = (protein_deviation + carbs_deviation + fat_deviation) / 3

        # Convert deviation to score (0 deviation = 10, 50+ deviation = 0)
        score = 10 - (avg_deviation / 5)

        return max(0.0, min(10.0, score))

    def _calculate_goal_adherence(
        self,
        meal_data: Dict[str, Any],
        user_targets: Dict[str, int]
    ) -> float:
        """
        Calculate adherence to daily nutrition goals (0-10).

        Compares meal macros to user's daily targets.
        """
        score = 5.0  # Start neutral

        protein = meal_data.get('protein_g', 0)
        carbs = meal_data.get('carbs_g', 0)
        fat = meal_data.get('fat_g', 0)
        calories = meal_data.get('calories', 0)

        target_protein = user_targets.get('daily_protein_target_g', 0)
        target_carbs = user_targets.get('daily_carbs_target_g', 0)
        target_fat = user_targets.get('daily_fat_target_g', 0)
        target_calories = user_targets.get('daily_calorie_target', 0)

        # Assume this is 1 of 3-4 meals per day
        expected_protein_per_meal = target_protein / 3.5 if target_protein else 0
        expected_carbs_per_meal = target_carbs / 3.5 if target_carbs else 0
        expected_fat_per_meal = target_fat / 3.5 if target_fat else 0
        expected_calories_per_meal = target_calories / 3.5 if target_calories else 0

        # Calculate adherence for each macro
        if expected_protein_per_meal > 0:
            protein_ratio = protein / expected_protein_per_meal
            if 0.8 <= protein_ratio <= 1.2:
                score += 1.5  # Within 20% of target
            elif 0.6 <= protein_ratio <= 1.4:
                score += 0.5  # Within 40% of target

        if expected_carbs_per_meal > 0:
            carbs_ratio = carbs / expected_carbs_per_meal
            if 0.8 <= carbs_ratio <= 1.2:
                score += 1.0
            elif 0.6 <= carbs_ratio <= 1.4:
                score += 0.3

        if expected_calories_per_meal > 0:
            calories_ratio = calories / expected_calories_per_meal
            if 0.8 <= calories_ratio <= 1.2:
                score += 1.5
            elif 0.6 <= calories_ratio <= 1.4:
                score += 0.5

        return max(0.0, min(10.0, score))

    def _generate_meal_tags(self, meal_data: Dict[str, Any]) -> List[str]:
        """
        Generate smart tags for meal categorization.
        """
        tags = []

        protein = meal_data.get('protein_g', 0)
        carbs = meal_data.get('carbs_g', 0)
        fat = meal_data.get('fat_g', 0)
        calories = meal_data.get('calories', 0)
        fiber = meal_data.get('fiber_g', 0)
        sugar = meal_data.get('sugar_g', 0)

        # Macro-based tags
        if protein >= 30:
            tags.append('high-protein')
        elif protein >= 20:
            tags.append('moderate-protein')

        if carbs >= 50:
            tags.append('high-carb')
        elif carbs <= 20:
            tags.append('low-carb')

        if fat >= 20:
            tags.append('high-fat')
        elif fat <= 10:
            tags.append('low-fat')

        # Calorie tags
        if calories >= 600:
            tags.append('high-calorie')
        elif calories <= 300:
            tags.append('low-calorie')

        # Quality tags
        if fiber >= 5:
            tags.append('high-fiber')

        if sugar < 10:
            tags.append('low-sugar')
        elif sugar >= 30:
            tags.append('high-sugar')

        # Meal type inference
        meal_type = meal_data.get('meal_type', '')
        if meal_type:
            tags.append(meal_type)

        # Balanced meal
        if 20 <= protein <= 40 and 30 <= carbs <= 60 and 10 <= fat <= 25:
            tags.append('balanced')

        return tags

    def _get_user_nutrition_targets(self, user_id: str) -> Dict[str, int]:
        """
        Fetch user's nutrition targets from user_onboarding table.
        """
        try:
            result = self.supabase.table("user_onboarding").select(
                "daily_calorie_target, daily_protein_target_g, daily_carbs_target_g, daily_fat_target_g"
            ).eq("user_id", user_id).execute()

            if result.data:
                return result.data[0]
            return {}

        except Exception as e:
            logger.error(f"Failed to fetch user nutrition targets: {e}")
            return {}

    # =============================================================================
    # WORKOUT ENRICHMENT
    # =============================================================================

    def enrich_workout(
        self,
        user_id: str,
        workout_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Enrich workout data with progressive overload detection, recovery needs.

        Args:
            user_id: User ID
            workout_data: Workout data from LLM extraction

        Returns:
            Enriched workout data
        """
        enrichment = {}

        # Detect progressive overload by comparing to recent similar workouts
        enrichment['progressive_overload_status'] = self._detect_progressive_overload(
            user_id, workout_data
        )

        # Estimate recovery time needed
        enrichment['recovery_needed_hours'] = self._estimate_recovery_time(workout_data)

        # Generate smart tags
        enrichment['tags'] = self._generate_workout_tags(workout_data)

        return enrichment

    def _detect_progressive_overload(
        self,
        user_id: str,
        workout_data: Dict[str, Any]
    ) -> Optional[str]:
        """
        Detect progressive overload by comparing volume load to recent workouts.

        Returns: 'improving', 'maintaining', 'declining', or None
        """
        try:
            current_volume = workout_data.get('volume_load', 0)
            if current_volume == 0:
                return None

            # Fetch recent workouts (last 14 days)
            two_weeks_ago = (datetime.utcnow() - timedelta(days=14)).isoformat()

            result = self.supabase.table("workout_completions").select(
                "volume_load, started_at"
            ).eq("user_id", user_id).gte(
                "started_at", two_weeks_ago
            ).order("started_at", desc=True).limit(10).execute()

            if not result.data or len(result.data) < 2:
                return None

            # Calculate average volume from recent workouts
            recent_volumes = [w['volume_load'] for w in result.data if w.get('volume_load')]
            if not recent_volumes:
                return None

            avg_recent_volume = sum(recent_volumes) / len(recent_volumes)

            # Compare current to average
            if current_volume > avg_recent_volume * 1.05:
                return 'improving'
            elif current_volume < avg_recent_volume * 0.95:
                return 'declining'
            else:
                return 'maintaining'

        except Exception as e:
            logger.error(f"Progressive overload detection failed: {e}")
            return None

    def _estimate_recovery_time(self, workout_data: Dict[str, Any]) -> Optional[int]:
        """
        Estimate recovery time needed based on workout intensity and volume.

        Returns: Hours of recovery needed
        """
        volume_load = workout_data.get('volume_load', 0)
        duration = workout_data.get('duration_minutes', 0)
        rpe = workout_data.get('rpe', 5)
        muscle_groups = workout_data.get('muscle_groups', [])

        # Base recovery time
        recovery_hours = 24

        # Adjust for RPE (effort)
        if rpe >= 9:
            recovery_hours += 24
        elif rpe >= 7:
            recovery_hours += 12

        # Adjust for volume
        if volume_load > 20000:
            recovery_hours += 12
        elif volume_load > 10000:
            recovery_hours += 6

        # Adjust for muscle groups (compound > isolation)
        if len(muscle_groups) >= 3:
            recovery_hours += 12

        return recovery_hours

    def _generate_workout_tags(self, workout_data: Dict[str, Any]) -> List[str]:
        """
        Generate smart tags for workout categorization.
        """
        tags = []

        muscle_groups = workout_data.get('muscle_groups', [])
        volume_load = workout_data.get('volume_load', 0)
        rpe = workout_data.get('rpe', 0)
        exercises = workout_data.get('exercises', [])

        # Muscle group tags
        tags.extend(muscle_groups)

        # Intensity tags
        if rpe >= 9:
            tags.append('high-intensity')
        elif rpe >= 7:
            tags.append('moderate-intensity')
        else:
            tags.append('light-intensity')

        # Volume tags
        if volume_load > 15000:
            tags.append('high-volume')
        elif volume_load < 5000:
            tags.append('low-volume')

        # Exercise count
        if len(exercises) >= 6:
            tags.append('full-workout')
        elif len(exercises) <= 3:
            tags.append('quick-workout')

        return tags

    # =============================================================================
    # ACTIVITY ENRICHMENT
    # =============================================================================

    def enrich_activity(
        self,
        user_id: str,
        activity_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Enrich activity data with performance scores and recovery needs.
        """
        enrichment = {}

        # Calculate performance score by comparing to recent similar activities
        enrichment['performance_score'] = self._calculate_performance_score(
            user_id, activity_data
        )

        # Estimate recovery time
        enrichment['recovery_needed_hours'] = self._estimate_activity_recovery(activity_data)

        # Generate smart tags
        enrichment['tags'] = self._generate_activity_tags(activity_data)

        return enrichment

    def _calculate_performance_score(
        self,
        user_id: str,
        activity_data: Dict[str, Any]
    ) -> Optional[float]:
        """
        Calculate performance score (0-10) by comparing to recent similar activities.
        """
        try:
            activity_type = activity_data.get('activity_type')
            duration = activity_data.get('duration_minutes', 0)
            distance = activity_data.get('distance_km', 0)

            if not activity_type or duration == 0:
                return None

            # Fetch recent similar activities
            two_weeks_ago = (datetime.utcnow() - timedelta(days=14)).isoformat()

            result = self.supabase.table("activities").select(
                "distance_meters, elapsed_time_seconds"
            ).eq("user_id", user_id).eq(
                "activity_type", activity_type
            ).gte("start_date", two_weeks_ago).limit(10).execute()

            if not result.data or len(result.data) < 2:
                return 5.0  # Neutral score if no history

            # Calculate average pace
            recent_paces = []
            for activity in result.data:
                dist_km = activity['distance_meters'] / 1000
                time_min = activity['elapsed_time_seconds'] / 60
                if dist_km > 0 and time_min > 0:
                    pace = time_min / dist_km  # min/km
                    recent_paces.append(pace)

            if not recent_paces:
                return 5.0

            avg_pace = sum(recent_paces) / len(recent_paces)

            # Compare current pace to average
            current_pace = duration / distance if distance > 0 else 0

            if current_pace == 0:
                return 5.0

            # Faster than average = higher score
            pace_improvement = ((avg_pace - current_pace) / avg_pace) * 100

            if pace_improvement > 10:
                return 9.0
            elif pace_improvement > 5:
                return 8.0
            elif pace_improvement > 0:
                return 7.0
            elif pace_improvement > -5:
                return 5.0
            else:
                return 3.0

        except Exception as e:
            logger.error(f"Performance score calculation failed: {e}")
            return None

    def _estimate_activity_recovery(self, activity_data: Dict[str, Any]) -> Optional[int]:
        """
        Estimate recovery time needed for cardio activity.
        """
        duration = activity_data.get('duration_minutes', 0)
        rpe = activity_data.get('rpe', 5)

        recovery_hours = 12  # Base

        if duration > 90:
            recovery_hours += 12
        elif duration > 60:
            recovery_hours += 6

        if rpe >= 9:
            recovery_hours += 12
        elif rpe >= 7:
            recovery_hours += 6

        return recovery_hours

    def _generate_activity_tags(self, activity_data: Dict[str, Any]) -> List[str]:
        """
        Generate smart tags for activity categorization.
        """
        tags = []

        activity_type = activity_data.get('activity_type', '')
        duration = activity_data.get('duration_minutes', 0)
        distance = activity_data.get('distance_km', 0)
        rpe = activity_data.get('rpe', 0)

        # Activity type
        if activity_type:
            tags.append(activity_type)

        # Duration tags
        if duration >= 90:
            tags.append('long-duration')
        elif duration <= 30:
            tags.append('short-duration')

        # Distance tags
        if distance >= 15:
            tags.append('long-distance')
        elif distance <= 5:
            tags.append('short-distance')

        # Effort tags
        if rpe >= 8:
            tags.append('high-effort')
        elif rpe <= 5:
            tags.append('easy')

        tags.append('cardio')

        return tags

    # =============================================================================
    # NOTE ENRICHMENT (with AI Sentiment Analysis)
    # =============================================================================

    async def enrich_note(
        self,
        user_id: str,
        note_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Enrich user note with sentiment analysis, detected themes, action items.

        Uses Groq llama-3.1-8b-instant for ultra-cheap sentiment analysis (~$0.00005/note).

        Args:
            user_id: User ID
            note_data: Note data (title, content)

        Returns:
            Enriched note data with sentiment, themes, action items
        """
        enrichment = {}

        content = note_data.get('content', '')
        title = note_data.get('title', '')

        if not content:
            return enrichment

        # Use Groq for sentiment analysis and theme detection
        try:
            sentiment_result = await self._analyze_sentiment_with_groq(content)
            enrichment.update(sentiment_result)
        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            # Fallback to simple keyword-based sentiment
            enrichment.update(self._simple_sentiment_analysis(content))

        # Generate tags from content
        enrichment['tags'] = self._generate_note_tags(content, title)

        return enrichment

    async def _analyze_sentiment_with_groq(self, content: str) -> Dict[str, Any]:
        """
        Analyze sentiment using Groq llama-3.1-8b-instant.

        Cost: ~$0.00005 per note (ultra-cheap!)
        """
        from app.services.groq_service import get_groq_service
        groq = get_groq_service()

        prompt = f"""Analyze the sentiment and themes in this user's fitness journal entry.

Entry:
{content}

Return JSON with:
{{
  "sentiment": "positive|neutral|negative",
  "sentiment_score": -1.0 to 1.0 (negative to positive),
  "detected_themes": ["motivation", "struggle", "progress", "injury", "goal-setting", etc.],
  "related_goals": ["lose weight", "build muscle", "improve endurance", etc.],
  "action_items": ["specific actions user mentioned or implied"]
}}

Focus on fitness-related themes. Keep action_items concise.
Return ONLY valid JSON."""

        response = await groq.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are a fitness journal analyst. Extract sentiment and themes from user notes."},
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.1,
            max_tokens=512
        )

        import json
        result = json.loads(response.choices[0].message.content)

        return {
            'sentiment': result.get('sentiment', 'neutral'),
            'sentiment_score': result.get('sentiment_score', 0.0),
            'detected_themes': result.get('detected_themes', []),
            'related_goals': result.get('related_goals', []),
            'action_items': result.get('action_items', [])
        }

    def _simple_sentiment_analysis(self, content: str) -> Dict[str, Any]:
        """
        Fallback: Simple keyword-based sentiment analysis.
        """
        content_lower = content.lower()

        # Positive keywords
        positive_keywords = [
            'great', 'amazing', 'awesome', 'love', 'motivated', 'strong',
            'progress', 'pr', 'personal record', 'feeling good', 'energized',
            'proud', 'accomplished', 'crushing it', 'excited'
        ]

        # Negative keywords
        negative_keywords = [
            'tired', 'exhausted', 'sore', 'pain', 'injury', 'struggling',
            'frustrated', 'unmotivated', 'weak', 'disappointed', 'failed',
            'giving up', 'hard', 'difficult', 'can\'t'
        ]

        positive_count = sum(1 for word in positive_keywords if word in content_lower)
        negative_count = sum(1 for word in negative_keywords if word in content_lower)

        # Calculate sentiment score
        total = positive_count + negative_count
        if total == 0:
            sentiment_score = 0.0
            sentiment = 'neutral'
        else:
            sentiment_score = (positive_count - negative_count) / total
            if sentiment_score > 0.3:
                sentiment = 'positive'
            elif sentiment_score < -0.3:
                sentiment = 'negative'
            else:
                sentiment = 'neutral'

        # Detect basic themes
        themes = []
        if any(word in content_lower for word in ['motivated', 'motivation', 'excited']):
            themes.append('motivation')
        if any(word in content_lower for word in ['tired', 'sore', 'exhausted']):
            themes.append('recovery')
        if any(word in content_lower for word in ['progress', 'pr', 'personal record', 'stronger']):
            themes.append('progress')
        if any(word in content_lower for word in ['goal', 'want to', 'plan to']):
            themes.append('goal-setting')

        return {
            'sentiment': sentiment,
            'sentiment_score': round(sentiment_score, 2),
            'detected_themes': themes,
            'related_goals': [],
            'action_items': []
        }

    def _generate_note_tags(self, content: str, title: str) -> List[str]:
        """
        Generate tags from note content.
        """
        tags = []
        combined = f"{title} {content}".lower()

        # Topic tags
        if any(word in combined for word in ['workout', 'training', 'exercise', 'lift']):
            tags.append('workout')
        if any(word in combined for word in ['meal', 'food', 'nutrition', 'diet', 'eating']):
            tags.append('nutrition')
        if any(word in combined for word in ['sleep', 'rest', 'recovery', 'sore']):
            tags.append('recovery')
        if any(word in combined for word in ['goal', 'target', 'aim', 'plan']):
            tags.append('goal-setting')
        if any(word in combined for word in ['progress', 'improve', 'gain', 'pr']):
            tags.append('progress')
        if any(word in combined for word in ['struggle', 'difficult', 'hard', 'challenge']):
            tags.append('struggle')

        return tags


# Global instance
_enrichment_service: Optional[EnrichmentService] = None


def get_enrichment_service() -> EnrichmentService:
    """Get the global EnrichmentService instance."""
    global _enrichment_service
    if _enrichment_service is None:
        _enrichment_service = EnrichmentService()
    return _enrichment_service
