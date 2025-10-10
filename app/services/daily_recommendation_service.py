"""
Daily Recommendation Service

Generates intelligent, time-aware recommendations for meals and workouts.

This service:
- Analyzes what user has logged vs. what they should do
- Suggests next meal/workout at appropriate times
- Adapts to user's schedule and patterns
- Learns from user acceptance/rejection

OPTIMIZED: Uses FREE models for recommendation generation!
"""

import json
import logging
from datetime import date, datetime, time, timedelta
from typing import Dict, Any, List, Optional

from app.config import get_settings
from app.services.supabase_service import get_service_client
from app.services.dual_model_router import dual_router, TaskType, TaskConfig

settings = get_settings()
logger = logging.getLogger(__name__)


class DailyRecommendationService:
    """Service for generating daily meal and workout recommendations."""

    # Default meal times (can be personalized per user)
    DEFAULT_MEAL_TIMES = {
        'breakfast': time(7, 0),
        'lunch': time(12, 0),
        'snack': time(15, 0),
        'dinner': time(18, 30),
        'pre_workout': time(16, 0),
        'post_workout': time(19, 0)
    }

    # Default workout times
    DEFAULT_WORKOUT_TIMES = {
        'morning': time(6, 0),
        'afternoon': time(16, 0),
        'evening': time(18, 0)
    }

    def __init__(self):
        self.supabase = get_service_client()
        self.router = dual_router

    async def generate_daily_plan(
        self,
        user_id: str,
        target_date: date = None
    ) -> List[Dict[str, Any]]:
        """
        Generate complete daily plan (meals + workouts).

        Args:
            user_id: User's UUID
            target_date: Date to generate plan for (defaults to today)

        Returns:
            List of recommendations for the day
        """
        if target_date is None:
            target_date = date.today()

        logger.info(f"Generating daily plan for user {user_id} on {target_date}")

        # Get user profile and goals
        user_data = await self._get_user_data(user_id)

        # Check if user has active AI program
        active_program = await self._get_active_program(user_id)

        # Check for upcoming events (NEW: Event awareness)
        upcoming_events = await self._get_upcoming_events(user_id)
        primary_event = await self._get_primary_event(user_id)

        # Get what's already been logged today
        logged_data = await self._get_logged_data(user_id, target_date)

        recommendations = []

        # Generate meal recommendations
        meal_recs = await self._generate_meal_recommendations(
            user_id=user_id,
            target_date=target_date,
            user_data=user_data,
            logged_meals=logged_data['meals'],
            active_program=active_program,
            primary_event=primary_event  # NEW: Pass event data
        )
        recommendations.extend(meal_recs)

        # Generate workout recommendations
        workout_recs = await self._generate_workout_recommendations(
            user_id=user_id,
            target_date=target_date,
            user_data=user_data,
            logged_workouts=logged_data['workouts'],
            active_program=active_program,
            primary_event=primary_event  # NEW: Pass event data
        )
        recommendations.extend(workout_recs)

        # Add event countdown notification if event is soon (NEW)
        if primary_event:
            event_notification = await self._generate_event_notification(
                primary_event=primary_event,
                target_date=target_date
            )
            if event_notification:
                recommendations.append(event_notification)

        # Save recommendations to database
        for rec in recommendations:
            await self._save_recommendation(rec)

        logger.info(f"Generated {len(recommendations)} recommendations for {target_date}")

        return recommendations

    async def suggest_next_action(
        self,
        user_id: str,
        current_time: datetime = None
    ) -> Optional[Dict[str, Any]]:
        """
        Suggest next immediate action (meal or workout).

        Args:
            user_id: User's UUID
            current_time: Current time (defaults to now)

        Returns:
            Next recommendation or None
        """
        if current_time is None:
            current_time = datetime.now()

        logger.info(f"Suggesting next action for user {user_id} at {current_time}")

        # Get pending recommendations for today
        today = current_time.date()
        pending = await self._get_pending_recommendations(user_id, today)

        if not pending:
            # No pending recs - generate plan
            await self.generate_daily_plan(user_id, today)
            pending = await self._get_pending_recommendations(user_id, today)

        if not pending:
            return None

        # Find next recommendation based on time
        current_time_only = current_time.time()
        next_rec = None
        min_time_diff = timedelta.max

        for rec in pending:
            rec_time = rec.get('recommendation_time')
            if not rec_time:
                continue

            # Parse time if string
            if isinstance(rec_time, str):
                rec_time = datetime.strptime(rec_time, '%H:%M:%S').time()

            # Calculate time difference
            rec_datetime = datetime.combine(today, rec_time)
            current_datetime = datetime.combine(today, current_time_only)
            time_diff = rec_datetime - current_datetime

            # Only consider future recommendations or those within 30 min past
            if time_diff >= timedelta(minutes=-30) and time_diff < min_time_diff:
                min_time_diff = time_diff
                next_rec = rec

        return next_rec

    async def update_plan_based_on_logs(
        self,
        user_id: str,
        log_type: str,
        log_data: Dict[str, Any]
    ):
        """
        Update recommendations based on new log entry.

        Args:
            user_id: User's UUID
            log_type: Type of log ('meal', 'workout', 'activity')
            log_data: The logged data
        """
        logger.info(f"Updating plan for user {user_id} based on {log_type} log")

        today = date.today()

        # Get pending recommendations
        pending = await self._get_pending_recommendations(user_id, today)

        # Find matching recommendation and mark as completed
        for rec in pending:
            if self._matches_log(rec, log_type, log_data):
                await self._update_recommendation_status(
                    recommendation_id=rec['id'],
                    status='completed',
                    user_id=user_id
                )
                logger.info(f"Marked recommendation {rec['id']} as completed")
                break

        # Check if we need to regenerate recommendations
        # (e.g., user ate early, now workout time needs adjusting)
        # TODO: Implement adaptive rescheduling

    async def get_active_recommendations(
        self,
        user_id: str,
        recommendation_date: date = None
    ) -> List[Dict[str, Any]]:
        """
        Get active recommendations for user.

        Args:
            user_id: User's UUID
            recommendation_date: Date to filter by (defaults to today)

        Returns:
            List of active recommendations
        """
        if recommendation_date is None:
            recommendation_date = date.today()

        response = self.supabase.table('daily_recommendations')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('recommendation_date', recommendation_date.isoformat())\
            .in_('status', ['pending', 'accepted'])\
            .order('recommendation_time')\
            .execute()

        return response.data if response.data else []

    async def accept_recommendation(
        self,
        recommendation_id: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Accept a recommendation."""
        return await self._update_recommendation_status(
            recommendation_id=recommendation_id,
            status='accepted',
            user_id=user_id
        )

    async def reject_recommendation(
        self,
        recommendation_id: str,
        user_id: str,
        feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """Reject a recommendation with optional feedback."""
        return await self._update_recommendation_status(
            recommendation_id=recommendation_id,
            status='rejected',
            user_id=user_id,
            feedback=feedback
        )

    # =====================================================
    # PRIVATE HELPER METHODS
    # =====================================================

    async def _get_user_data(self, user_id: str) -> Dict[str, Any]:
        """Get user profile and nutrition goals."""
        # Get profile
        profile = self.supabase.table('profiles')\
            .select('*')\
            .eq('id', user_id)\
            .single()\
            .execute().data or {}

        # Get nutrition goals
        nutrition_goals = self.supabase.table('nutrition_goals')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('is_active', True)\
            .single()\
            .execute().data or {}

        return {
            'profile': profile,
            'nutrition_goals': nutrition_goals
        }

    async def _get_active_program(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Get user's active AI program."""
        response = self.supabase.table('ai_generated_programs')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('is_active', True)\
            .eq('status', 'active')\
            .single()\
            .execute()

        return response.data if response.data else None

    async def _get_logged_data(
        self,
        user_id: str,
        target_date: date
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Get what user has already logged today."""
        date_str = target_date.isoformat()

        # Get meals logged today
        meals = self.supabase.table('meals')\
            .select('*')\
            .eq('user_id', user_id)\
            .gte('logged_at', f'{date_str}T00:00:00')\
            .lt('logged_at', f'{date_str}T23:59:59')\
            .execute().data or []

        # Get workouts/activities logged today
        workouts = self.supabase.table('activities')\
            .select('*')\
            .eq('user_id', user_id)\
            .gte('start_date', f'{date_str}T00:00:00')\
            .lt('start_date', f'{date_str}T23:59:59')\
            .execute().data or []

        return {
            'meals': meals,
            'workouts': workouts
        }

    async def _generate_meal_recommendations(
        self,
        user_id: str,
        target_date: date,
        user_data: Dict[str, Any],
        logged_meals: List[Dict[str, Any]],
        active_program: Optional[Dict[str, Any]],
        primary_event: Optional[Dict[str, Any]] = None  # NEW: Event parameter
    ) -> List[Dict[str, Any]]:
        """Generate meal recommendations for the day."""
        nutrition_goals = user_data.get('nutrition_goals', {})
        profile = user_data.get('profile', {})

        # Get target macros
        daily_calories = nutrition_goals.get('daily_calories', 2000)
        daily_protein_g = nutrition_goals.get('daily_protein_g', 150)
        daily_carbs_g = nutrition_goals.get('daily_carbs_g', 200)
        daily_fat_g = nutrition_goals.get('daily_fat_g', 65)

        # Adjust macros based on event phase (NEW)
        if primary_event:
            daily_calories, daily_carbs_g = self._adjust_macros_for_event(
                primary_event=primary_event,
                base_calories=daily_calories,
                base_carbs=daily_carbs_g
            )

        # Calculate what's been logged so far
        logged_calories = sum(m.get('total_calories', 0) for m in logged_meals)
        logged_protein = sum(m.get('total_protein_g', 0) for m in logged_meals)

        remaining_calories = daily_calories - logged_calories
        remaining_protein = daily_protein_g - logged_protein

        # Determine which meals are missing
        logged_meal_types = set(m.get('category', m.get('meal_type')) for m in logged_meals)
        meal_types = ['breakfast', 'lunch', 'dinner', 'snack']
        missing_meals = [m for m in meal_types if m not in logged_meal_types]

        recommendations = []

        # If no meals logged yet, suggest all meals
        if not logged_meals:
            meals_to_suggest = meal_types
        else:
            meals_to_suggest = missing_meals

        for meal_type in meals_to_suggest:
            # Get default time for this meal
            meal_time = self.DEFAULT_MEAL_TIMES.get(meal_type, time(12, 0))

            # Calculate macro split for this meal (simplified)
            if meal_type == 'snack':
                meal_calories = int(remaining_calories * 0.15)
                meal_protein = int(remaining_protein * 0.15)
            else:
                # Split remaining calories across remaining main meals
                num_remaining_meals = len([m for m in meals_to_suggest if m != 'snack'])
                meal_calories = int(remaining_calories / max(num_remaining_meals, 1))
                meal_protein = int(remaining_protein / max(num_remaining_meals, 1))

            # Generate meal suggestion using AI
            meal_content = await self._generate_meal_suggestion(
                meal_type=meal_type,
                target_calories=meal_calories,
                target_protein=meal_protein,
                dietary_preferences=profile.get('dietary_preferences', 'none')
            )

            recommendations.append({
                'user_id': user_id,
                'recommendation_date': target_date.isoformat(),
                'recommendation_time': meal_time.isoformat(),
                'recommendation_type': 'meal',
                'content': meal_content,
                'reasoning': f"You haven't logged {meal_type} yet. Target: {meal_calories} cal, {meal_protein}g protein",
                'priority': self._calculate_meal_priority(meal_type, meal_time),
                'status': 'pending',
                'based_on_data': {
                    'logged_calories': logged_calories,
                    'remaining_calories': remaining_calories,
                    'daily_target': daily_calories
                }
            })

        return recommendations

    async def _generate_workout_recommendations(
        self,
        user_id: str,
        target_date: date,
        user_data: Dict[str, Any],
        logged_workouts: List[Dict[str, Any]],
        active_program: Optional[Dict[str, Any]],
        primary_event: Optional[Dict[str, Any]] = None  # NEW: Event parameter
    ) -> List[Dict[str, Any]]:
        """Generate workout recommendations for the day."""
        recommendations = []

        # Check if in taper/peak week (NEW: Event-aware adjustments)
        is_taper_week = False
        is_peak_week = False
        event_phase = None

        if primary_event:
            is_taper_week = primary_event.get('is_taper_week', False)
            is_peak_week = primary_event.get('is_peak_week', False)
            event_phase = primary_event.get('current_training_phase')

        # If user has active program, use that
        if active_program:
            # Get today's workout from program
            program_workout = await self._get_program_workout_for_day(
                program_id=active_program['id'],
                target_date=target_date
            )

            if program_workout and not logged_workouts:
                # Adjust workout recommendation based on event phase (NEW)
                workout_content = {
                    'workout_name': program_workout.get('name', 'Today\'s Workout'),
                    'workout_type': program_workout.get('workout_type', 'strength'),
                    'duration_minutes': program_workout.get('duration_minutes', 60),
                    'exercises': program_workout.get('exercises', [])
                }

                reasoning = f"Today's scheduled workout from your program: {program_workout.get('name')}"

                # Add event-specific messaging (NEW)
                if is_taper_week:
                    reasoning += f" ⚠️ TAPER WEEK - Reduce intensity, focus on recovery!"
                    workout_content['note'] = "Taper week: 50-70% normal volume, maintain intensity"
                elif is_peak_week:
                    reasoning += f" 🔥 PEAK WEEK - Time to shine!"
                    workout_content['note'] = "Peak week: Quality over quantity"

                recommendations.append({
                    'user_id': user_id,
                    'recommendation_date': target_date.isoformat(),
                    'recommendation_time': self.DEFAULT_WORKOUT_TIMES['afternoon'].isoformat(),
                    'recommendation_type': 'workout',
                    'content': workout_content,
                    'reasoning': reasoning,
                    'priority': 4,
                    'status': 'pending',
                    'based_on_data': {
                        'program_id': active_program['id'],
                        'program_day': program_workout.get('day_number'),
                        'event_phase': event_phase
                    }
                })

        # If no program or workout already logged, suggest based on profile
        elif not logged_workouts:
            profile = user_data.get('profile', {})
            training_frequency = profile.get('training_frequency', 3)

            # Simple recommendation: if they should train today
            day_of_week = target_date.weekday()
            if day_of_week < training_frequency:  # Assume training early in week
                recommendations.append({
                    'user_id': user_id,
                    'recommendation_date': target_date.isoformat(),
                    'recommendation_time': self.DEFAULT_WORKOUT_TIMES['evening'].isoformat(),
                    'recommendation_type': 'workout',
                    'content': {
                        'workout_name': 'Suggested Workout',
                        'workout_type': 'general',
                        'duration_minutes': 45,
                        'note': 'Time for your workout! Check your program or log your own activity.'
                    },
                    'reasoning': f"Based on your {training_frequency}x/week schedule",
                    'priority': 3,
                    'status': 'pending'
                })
            else:
                # Rest day recommendation
                recommendations.append({
                    'user_id': user_id,
                    'recommendation_date': target_date.isoformat(),
                    'recommendation_time': None,
                    'recommendation_type': 'rest',
                    'content': {
                        'message': 'Rest day - focus on recovery and nutrition'
                    },
                    'reasoning': 'Scheduled rest day for optimal recovery',
                    'priority': 2,
                    'status': 'pending'
                })

        return recommendations

    async def _generate_meal_suggestion(
        self,
        meal_type: str,
        target_calories: int,
        target_protein: int,
        dietary_preferences: str
    ) -> Dict[str, Any]:
        """Generate AI meal suggestion."""
        try:
            prompt = f"""Suggest a {meal_type} with approximately {target_calories} calories and {target_protein}g protein.

Dietary preferences: {dietary_preferences}

Provide a simple, realistic meal suggestion with:
1. Meal name
2. Main foods (3-5 items)
3. Brief preparation note

Format as JSON:
{{
    "meal_name": "...",
    "foods": ["food1", "food2", ...],
    "preparation": "...",
    "estimated_calories": {target_calories},
    "estimated_protein_g": {target_protein}
}}"""

            # Use Groq for fast meal suggestions
            response = await self.router.complete(
                config=TaskConfig(
                    type=TaskType.STRUCTURED_OUTPUT,
                    requires_json=True,
                    prioritize_speed=True
                ),
                messages=[
                    {"role": "system", "content": "You are a nutrition expert suggesting healthy meals."},
                    {"role": "user", "content": prompt}
                ],
                response_format={"type": "json_object"}
            )

            meal_data = response.choices[0].message.content
            return json.loads(meal_data) if isinstance(meal_data, str) else meal_data

        except Exception as e:
            logger.error(f"Error generating meal suggestion: {e}")
            # Fallback simple suggestion
            return {
                'meal_name': f"Balanced {meal_type}",
                'foods': ["lean protein", "vegetables", "whole grains"],
                'preparation': "Simple and nutritious",
                'estimated_calories': target_calories,
                'estimated_protein_g': target_protein
            }

    async def _get_program_workout_for_day(
        self,
        program_id: str,
        target_date: date
    ) -> Optional[Dict[str, Any]]:
        """Get workout from AI program for specific date."""
        # Get program days
        response = self.supabase.table('ai_program_days')\
            .select('*, ai_program_items!inner(*)')\
            .eq('program_id', program_id)\
            .eq('day_date', target_date.isoformat())\
            .execute()

        if not response.data:
            return None

        day_data = response.data[0]

        # Find workout items for this day
        workout_items = [
            item for item in day_data.get('ai_program_items', [])
            if item.get('item_type') == 'workout'
        ]

        return workout_items[0] if workout_items else None

    async def _get_pending_recommendations(
        self,
        user_id: str,
        target_date: date
    ) -> List[Dict[str, Any]]:
        """Get pending recommendations for date."""
        response = self.supabase.table('daily_recommendations')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('recommendation_date', target_date.isoformat())\
            .eq('status', 'pending')\
            .order('priority', desc=True)\
            .execute()

        return response.data if response.data else []

    def _matches_log(
        self,
        recommendation: Dict[str, Any],
        log_type: str,
        log_data: Dict[str, Any]
    ) -> bool:
        """Check if a log entry matches a recommendation."""
        rec_type = recommendation.get('recommendation_type')

        if rec_type == 'meal' and log_type == 'meal':
            # Check if meal types match
            rec_content = recommendation.get('content', {})
            rec_meal_type = rec_content.get('meal_type')
            log_meal_type = log_data.get('category', log_data.get('meal_type'))
            return rec_meal_type == log_meal_type

        elif rec_type == 'workout' and log_type in ['workout', 'activity']:
            # Any workout log matches workout recommendation
            return True

        return False

    def _calculate_meal_priority(self, meal_type: str, meal_time: time) -> int:
        """Calculate priority for meal recommendation (1-5)."""
        # Higher priority for earlier meals and main meals
        if meal_type == 'breakfast':
            return 5
        elif meal_type == 'lunch':
            return 4
        elif meal_type == 'dinner':
            return 4
        elif meal_type == 'snack':
            return 2
        else:
            return 3

    async def _save_recommendation(self, recommendation: Dict[str, Any]) -> Dict[str, Any]:
        """Save recommendation to database."""
        # Set expiration (recommendations expire at end of day)
        rec_date = recommendation['recommendation_date']
        expires_at = f"{rec_date}T23:59:59"
        recommendation['expires_at'] = expires_at

        response = self.supabase.table('daily_recommendations')\
            .insert(recommendation)\
            .execute()

        return response.data[0] if response.data else {}

    async def _update_recommendation_status(
        self,
        recommendation_id: str,
        status: str,
        user_id: str,
        feedback: Optional[str] = None
    ) -> Dict[str, Any]:
        """Update recommendation status."""
        updates = {'status': status}

        if status == 'completed':
            updates['completed_at'] = datetime.utcnow().isoformat()

        if feedback:
            updates['user_feedback'] = feedback

        response = self.supabase.table('daily_recommendations')\
            .update(updates)\
            .eq('id', recommendation_id)\
            .eq('user_id', user_id)\
            .execute()

        return response.data[0] if response.data else {}

    async def _get_upcoming_events(self, user_id: str) -> List[Dict[str, Any]]:
        """
        Get upcoming events for user (NEW: Event awareness).

        Returns:
            List of upcoming events with countdown data
        """
        try:
            from app.services.event_service import get_event_service
            event_service = get_event_service()
            return await event_service.get_upcoming_events(user_id, days_ahead=90)
        except Exception as e:
            logger.error(f"Error fetching upcoming events: {e}")
            return []

    async def _get_primary_event(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user's primary event with countdown (NEW: Event awareness).

        Returns:
            Primary event data or None
        """
        try:
            from app.services.event_service import get_event_service
            event_service = get_event_service()
            return await event_service.get_primary_event(user_id)
        except Exception as e:
            logger.error(f"Error fetching primary event: {e}")
            return None

    def _adjust_macros_for_event(
        self,
        primary_event: Dict[str, Any],
        base_calories: int,
        base_carbs: float
    ) -> tuple[int, float]:
        """
        Adjust macros based on event phase (NEW: Event-aware nutrition).

        Args:
            primary_event: Event data with training phase
            base_calories: Base caloric target
            base_carbs: Base carb target (grams)

        Returns:
            Tuple of (adjusted_calories, adjusted_carbs)
        """
        event_type = primary_event.get('event_type', '')
        current_phase = primary_event.get('current_training_phase', '')
        days_until = primary_event.get('days_until_event', 999)

        adjusted_calories = base_calories
        adjusted_carbs = base_carbs

        # Endurance events: Increase carbs during build/peak, carb load final week
        if event_type in ['marathon', 'half_marathon', '10k', '5k', 'triathlon', 'cycling_race']:
            if current_phase == 'build':
                adjusted_carbs = base_carbs * 1.1  # 10% more carbs
            elif current_phase == 'peak':
                adjusted_carbs = base_carbs * 1.2  # 20% more carbs
            elif current_phase == 'taper':
                if days_until <= 3:  # Carb loading final 3 days
                    adjusted_carbs = base_carbs * 1.5  # 50% more carbs
                    adjusted_calories = int(base_calories * 1.1)
                else:
                    adjusted_calories = int(base_calories * 0.9)  # Reduce calories during taper

        # Strength events: High protein during hypertrophy, reduce water final week
        elif event_type in ['powerlifting_meet', 'weightlifting_meet', 'strongman']:
            if current_phase == 'build':
                # Maintain high protein
                pass
            elif current_phase == 'taper':
                if days_until <= 7:
                    # Reduce calories slightly for weight management
                    adjusted_calories = int(base_calories * 0.95)

        # Physique events: Progressive deficit
        elif event_type in ['bodybuilding_show', 'physique_competition']:
            if current_phase == 'build':
                # Mass building phase
                adjusted_calories = int(base_calories * 1.1)
            elif current_phase == 'peak':
                # Cutting phase
                adjusted_calories = int(base_calories * 0.85)
                adjusted_carbs = base_carbs * 0.8
            elif current_phase == 'taper':
                if days_until <= 7:
                    # Peak week protocol
                    if days_until <= 2:
                        # Carb loading
                        adjusted_carbs = base_carbs * 1.5
                    else:
                        # Carb depletion
                        adjusted_carbs = base_carbs * 0.5

        logger.info(f"Adjusted macros for {event_type} ({current_phase}): "
                   f"{adjusted_calories} cal, {adjusted_carbs}g carbs")

        return adjusted_calories, adjusted_carbs

    async def _generate_event_notification(
        self,
        primary_event: Dict[str, Any],
        target_date: date
    ) -> Optional[Dict[str, Any]]:
        """
        Generate event countdown notification (NEW: Event notifications).

        Args:
            primary_event: Primary event data
            target_date: Date to generate notification for

        Returns:
            Notification recommendation or None
        """
        event_name = primary_event.get('event_name', 'Your Event')
        days_until = primary_event.get('days_until_event', 0)
        current_phase = primary_event.get('current_training_phase', '')
        countdown_message = primary_event.get('countdown_message', '')

        # Only show notification on certain milestones
        milestone_days = [90, 60, 30, 21, 14, 7, 3, 2, 1, 0]

        if days_until not in milestone_days:
            return None

        # Determine priority and emoji based on days until
        if days_until == 0:
            emoji = "🏆"
            priority = 5
            message = f"TODAY IS THE DAY! {event_name}"
            note = "Good luck! Trust your training and execute your plan."
        elif days_until == 1:
            emoji = "⚡"
            priority = 5
            message = f"TOMORROW: {event_name}"
            note = "Final prep day. Rest, hydrate, visualize success."
        elif days_until <= 7:
            emoji = "🔥"
            priority = 5
            message = f"{days_until} days until {event_name}!"
            note = f"Taper week - reduce volume, maintain intensity. {countdown_message}"
        elif days_until <= 21:
            emoji = "💪"
            priority = 4
            message = f"{days_until} days until {event_name}!"
            note = f"Peak phase - time to maximize performance. {countdown_message}"
        elif days_until <= 60:
            emoji = "📈"
            priority = 3
            message = f"{days_until} days until {event_name}!"
            note = f"Build phase - progressive overload. {countdown_message}"
        else:
            emoji = "🎯"
            priority = 2
            message = f"{days_until} days until {event_name}!"
            note = f"Base phase - building foundation. {countdown_message}"

        return {
            'user_id': primary_event.get('user_id'),
            'recommendation_date': target_date.isoformat(),
            'recommendation_time': time(6, 0).isoformat(),  # Morning notification
            'recommendation_type': 'event_reminder',
            'content': {
                'event_id': primary_event.get('event_id'),
                'event_name': event_name,
                'days_until': days_until,
                'training_phase': current_phase,
                'message': f"{emoji} {message}",
                'note': note
            },
            'reasoning': f"Event countdown: {event_name} in {days_until} days",
            'priority': priority,
            'status': 'pending',
            'based_on_data': {
                'event_id': primary_event.get('event_id'),
                'countdown_milestone': days_until
            }
        }


# Global instance
_recommendation_service: Optional[DailyRecommendationService] = None


def get_recommendation_service() -> DailyRecommendationService:
    """Get the global DailyRecommendationService instance."""
    global _recommendation_service
    if _recommendation_service is None:
        _recommendation_service = DailyRecommendationService()
    return _recommendation_service
