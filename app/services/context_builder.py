"""
Context Builder Service

Builds comprehensive context for AI coaches using RAG and structured data.
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from app.services.supabase_service import get_service_client
from app.services.embedding_service import EmbeddingService
from app.services.multimodal_embedding_service import get_multimodal_service

# Import Garmy MCP for AI-powered health data queries
try:
    from app.workers.garmy_mcp_server import get_mcp_server
    GARMY_MCP_AVAILABLE = True
except ImportError:
    GARMY_MCP_AVAILABLE = False

logger = logging.getLogger(__name__)


class ContextBuilder:
    """Service for building AI coach context using RAG and structured data."""

    def __init__(self):
        self.supabase = get_service_client()
        self.embedding_service = EmbeddingService()
        self.multimodal_service = get_multimodal_service()  # REVOLUTIONARY multimodal RAG

    async def build_trainer_context(
        self,
        user_id: str,
        query: Optional[str] = None,
        days_lookback: int = 30
    ) -> str:
        """
        Build context for the trainer persona.

        Args:
            user_id: User ID
            query: Optional query to focus the context on specific topics
            days_lookback: Number of days to look back for recent data

        Returns:
            Formatted context string
        """
        context_parts = ["=== TRAINER CONTEXT ===\n"]

        # 1. User Profile & Goals
        profile_context = await self._get_user_profile_context(user_id)
        if profile_context:
            context_parts.append("## User Profile & Goals")
            context_parts.append(profile_context)
            context_parts.append("")

        # 2. Current Workout Program (if any)
        program_context = await self._get_active_workout_program(user_id)
        if program_context:
            context_parts.append("## Current Workout Program")
            context_parts.append(program_context)
            context_parts.append("")

        # 2b. AI-Generated Program (if any)
        ai_program_context = await self._get_active_ai_program(user_id)
        if ai_program_context and ai_program_context != "No active AI-generated program":
            context_parts.append("## AI-Generated Program")
            context_parts.append(ai_program_context)
            context_parts.append("")

        # 3. Recent Workouts (structured data)
        recent_workouts = await self._get_recent_workouts(user_id, days_lookback)
        if recent_workouts:
            context_parts.append("## Recent Workouts")
            context_parts.append(recent_workouts)
            context_parts.append("")

        # 4. Exercise Progress Tracking
        exercise_progress = await self._get_exercise_progress(user_id)
        if exercise_progress:
            context_parts.append("## Exercise Progress (Progressive Overload)")
            context_parts.append(exercise_progress)
            context_parts.append("")

        # 5. RAG: Relevant Historical Context
        if query:
            rag_context = await self._get_rag_context(
                user_id=user_id,
                query=query,
                source_types=["workout", "activity", "goal"],
                match_count=5
            )
            if rag_context:
                context_parts.append("## Relevant Historical Context")
                context_parts.append(rag_context)
                context_parts.append("")

        # 6. Recovery Metrics (Garmin Health Data)
        recovery_metrics = await self._get_recovery_metrics(user_id, days_lookback)
        if recovery_metrics:
            context_parts.append("## Recovery & Health Metrics")
            context_parts.append(recovery_metrics)
            context_parts.append("")

        # 6b. Recovery-Performance Correlations
        recovery_correlations = await self._get_recovery_performance_correlations(user_id, days_lookback)
        if recovery_correlations:
            context_parts.append("## Recovery-Performance Insights")
            context_parts.append(recovery_correlations)
            context_parts.append("")

        # 7. Recent Coach Interactions
        recent_interactions = await self._get_recent_coach_interactions(
            user_id=user_id,
            coach_type="trainer",
            limit=5
        )
        if recent_interactions:
            context_parts.append("## Recent Coach Interactions")
            context_parts.append(recent_interactions)
            context_parts.append("")

        return "\n".join(context_parts)

    async def build_nutritionist_context(
        self,
        user_id: str,
        query: Optional[str] = None,
        days_lookback: int = 30
    ) -> str:
        """
        Build context for the nutritionist persona.

        Args:
            user_id: User ID
            query: Optional query to focus the context on specific topics
            days_lookback: Number of days to look back for recent data

        Returns:
            Formatted context string
        """
        context_parts = ["=== NUTRITIONIST CONTEXT ===\n"]

        # 1. User Profile & Goals
        profile_context = await self._get_user_profile_context(user_id)
        if profile_context:
            context_parts.append("## User Profile & Goals")
            context_parts.append(profile_context)
            context_parts.append("")

        # 2. Current Nutrition Program (if any)
        program_context = await self._get_active_nutrition_program(user_id)
        if program_context:
            context_parts.append("## Current Nutrition Program")
            context_parts.append(program_context)
            context_parts.append("")

        # 2b. AI-Generated Program (if any)
        ai_program_context = await self._get_active_ai_program(user_id)
        if ai_program_context and ai_program_context != "No active AI-generated program":
            context_parts.append("## AI-Generated Program")
            context_parts.append(ai_program_context)
            context_parts.append("")

        # 3. Recent Meals (structured data)
        recent_meals = await self._get_recent_meals(user_id, days_lookback)
        if recent_meals:
            context_parts.append("## Recent Meals")
            context_parts.append(recent_meals)
            context_parts.append("")

        # 4. Nutrition Compliance
        compliance = await self._get_nutrition_compliance(user_id, days_lookback)
        if compliance:
            context_parts.append("## Nutrition Compliance")
            context_parts.append(compliance)
            context_parts.append("")

        # 5. RAG: Relevant Historical Context
        if query:
            rag_context = await self._get_rag_context(
                user_id=user_id,
                query=query,
                source_types=["meal", "goal"],
                match_count=5
            )
            if rag_context:
                context_parts.append("## Relevant Historical Context")
                context_parts.append(rag_context)
                context_parts.append("")

        # 6. Recent Coach Interactions
        recent_interactions = await self._get_recent_coach_interactions(
            user_id=user_id,
            coach_type="nutritionist",
            limit=5
        )
        if recent_interactions:
            context_parts.append("## Recent Coach Interactions")
            context_parts.append(recent_interactions)
            context_parts.append("")

        return "\n".join(context_parts)

    async def build_unified_coach_context(
        self,
        user_id: str,
        query: Optional[str] = None,
        days_lookback: int = 30
    ) -> str:
        """
        Build unified context for the combined fitness + nutrition coach.

        This combines both workout and nutrition data to provide holistic guidance.

        Args:
            user_id: User ID
            query: Optional query to focus the context on specific topics
            days_lookback: Number of days to look back for recent data

        Returns:
            Formatted context string with both fitness and nutrition data
        """
        context_parts = ["=== UNIFIED COACH CONTEXT ===\n"]

        # 1. User Profile & Goals
        profile_context = await self._get_user_profile_context(user_id)
        if profile_context:
            context_parts.append("## User Profile & Goals")
            context_parts.append(profile_context)
            context_parts.append("")

        # 1b. AI-Generated Program (if any)
        ai_program_context = await self._get_active_ai_program(user_id)
        if ai_program_context and ai_program_context != "No active AI-generated program":
            context_parts.append("## AI-Generated Program")
            context_parts.append(ai_program_context)
            context_parts.append("")

        # === TRAINING DATA ===
        context_parts.append("# TRAINING DATA")
        context_parts.append("")

        # 2. Current Workout Program
        workout_program_context = await self._get_active_workout_program(user_id)
        if workout_program_context:
            context_parts.append("## Current Workout Program")
            context_parts.append(workout_program_context)
            context_parts.append("")

        # 3. Recent Workouts
        recent_workouts = await self._get_recent_workouts(user_id, days_lookback)
        if recent_workouts:
            context_parts.append("## Recent Workouts")
            context_parts.append(recent_workouts)
            context_parts.append("")

        # 4. Exercise Progress Tracking
        exercise_progress = await self._get_exercise_progress(user_id)
        if exercise_progress:
            context_parts.append("## Exercise Progress (Progressive Overload)")
            context_parts.append(exercise_progress)
            context_parts.append("")

        # === NUTRITION DATA ===
        context_parts.append("# NUTRITION DATA")
        context_parts.append("")

        # 5. Current Nutrition Program
        nutrition_program_context = await self._get_active_nutrition_program(user_id)
        if nutrition_program_context:
            context_parts.append("## Current Nutrition Program")
            context_parts.append(nutrition_program_context)
            context_parts.append("")

        # 6. Recent Meals
        recent_meals = await self._get_recent_meals(user_id, days_lookback)
        if recent_meals:
            context_parts.append("## Recent Meals")
            context_parts.append(recent_meals)
            context_parts.append("")

        # 7. Nutrition Compliance
        compliance = await self._get_nutrition_compliance(user_id, days_lookback)
        if compliance:
            context_parts.append("## Nutrition Compliance")
            context_parts.append(compliance)
            context_parts.append("")

        # === RECOVERY & HEALTH DATA ===
        context_parts.append("# RECOVERY & HEALTH DATA")
        context_parts.append("")

        # 8. Recovery Metrics (Garmin Health Data)
        recovery_metrics = await self._get_recovery_metrics(user_id, days_lookback)
        if recovery_metrics:
            context_parts.append("## Recovery & Health Metrics")
            context_parts.append(recovery_metrics)
            context_parts.append("")

        # 8b. Recovery-Performance Correlations
        recovery_correlations = await self._get_recovery_performance_correlations(user_id, days_lookback)
        if recovery_correlations:
            context_parts.append("## Recovery-Performance Insights")
            context_parts.append(recovery_correlations)
            context_parts.append("")

        # === HISTORICAL CONTEXT (RAG) ===
        if query:
            rag_context = await self._get_rag_context(
                user_id=user_id,
                query=query,
                source_types=["workout", "meal", "activity", "goal"],
                match_count=5
            )
            if rag_context:
                context_parts.append("## Relevant Historical Context")
                context_parts.append(rag_context)
                context_parts.append("")

        # 8. Recent Coach Interactions
        recent_interactions = await self._get_recent_coach_interactions(
            user_id=user_id,
            coach_type="coach",
            limit=5
        )
        if recent_interactions:
            context_parts.append("## Recent Coach Interactions")
            context_parts.append(recent_interactions)
            context_parts.append("")

        return "\n".join(context_parts)

    async def _get_user_profile_context(self, user_id: str) -> str:
        """
        Get comprehensive user profile and goals.

        Returns all relevant user data for AI coaching context:
        - Basic info (name, age, gender)
        - Physical stats (height, weight, goals)
        - Experience level and training frequency
        - Equipment access and limitations
        - Dietary restrictions and preferences
        - Settings and onboarding data
        """
        try:
            # Get user data (consolidated users table has all the data we need)
            profile_response = (
                self.supabase.table("users")
                .select("*")
                .eq("id", user_id)
                .single()
                .execute()
            )

            if not profile_response.data:
                return ""

            profile = profile_response.data
            parts = []

            # Basic info
            if full_name := profile.get("full_name"):
                parts.append(f"Name: {full_name}")
            if age := profile.get("age"):
                parts.append(f"Age: {age}")
            if bio_sex := profile.get("biological_sex"):
                parts.append(f"Biological Sex: {bio_sex}")

            # Physical stats
            if height := profile.get("height_cm"):
                parts.append(f"Height: {height} cm")
            if weight := profile.get("current_weight_kg"):
                parts.append(f"Current Weight: {weight} kg")
            if goal_weight := profile.get("goal_weight_kg"):
                parts.append(f"Goal Weight: {goal_weight} kg")

            # Experience & Training
            if experience := profile.get("experience_level"):
                parts.append(f"Experience Level: {experience}")
            if freq := profile.get("training_frequency"):
                # training_frequency is an integer in users table
                parts.append(f"Training Frequency: {freq} days per week")
            if goal := profile.get("primary_goal"):
                parts.append(f"Primary Goal: {goal}")

            # Equipment Access
            if equipment := profile.get("available_equipment"):
                if isinstance(equipment, list) and equipment:
                    parts.append(f"Available Equipment: {', '.join(equipment)}")
                elif isinstance(equipment, str) and equipment:
                    parts.append(f"Available Equipment: {equipment}")

            # Dietary Restrictions
            if diet_restrictions := profile.get("dietary_restrictions"):
                if isinstance(diet_restrictions, list) and diet_restrictions:
                    parts.append(f"Dietary Restrictions: {', '.join(diet_restrictions)}")
                elif isinstance(diet_restrictions, str) and diet_restrictions:
                    parts.append(f"Dietary Restrictions: {diet_restrictions}")

            # Injury/Physical Limitations
            if injuries := profile.get("injury_limitations"):
                if isinstance(injuries, list) and injuries:
                    parts.append(f"Injury/Physical Limitations: {', '.join(injuries)}")
                elif isinstance(injuries, str) and injuries:
                    parts.append(f"Injury/Physical Limitations: {injuries}")

            # Nutrition Targets
            if cal_target := profile.get("daily_calorie_target"):
                parts.append(f"Daily Calorie Target: {cal_target} kcal")
            if protein_target := profile.get("daily_protein_target_g"):
                parts.append(f"Daily Protein Target: {protein_target}g")
            if carbs_target := profile.get("daily_carbs_target_g"):
                parts.append(f"Daily Carbs Target: {carbs_target}g")
            if fat_target := profile.get("daily_fat_target_g"):
                parts.append(f"Daily Fat Target: {fat_target}g")

            # Preferences (legacy fields)
            if workout_pref := profile.get("workout_preferences"):
                parts.append(f"Workout Preferences: {workout_pref}")
            if dietary_pref := profile.get("dietary_preferences"):
                parts.append(f"Dietary Preferences: {dietary_pref}")

            # Settings JSONB (additional user preferences)
            if settings := profile.get("settings"):
                if isinstance(settings, dict) and settings:
                    # Extract key settings that are relevant for coaching
                    if rest_timer := settings.get("rest_timer_default"):
                        parts.append(f"Rest Timer Default: {rest_timer}s")
                    if units := settings.get("preferred_units"):
                        parts.append(f"Preferred Units: {units}")
                    # Add any other relevant settings from JSONB

            # Onboarding Data JSONB (program generation answers)
            if onboarding := profile.get("onboarding_data"):
                if isinstance(onboarding, dict) and onboarding:
                    parts.append("\n## User Program Preferences:")
                    # Extract relevant onboarding answers for context
                    for key, value in onboarding.items():
                        if value and key not in ['created_at', 'updated_at']:
                            # Format key as readable label
                            label = key.replace('_', ' ').title()
                            parts.append(f"  - {label}: {value}")

            return "\n".join(parts)

        except Exception as e:
            logger.error(f"Error getting user profile context: {e}")
            return ""

    async def _get_active_workout_program(self, user_id: str) -> str:
        """Get active workout program."""
        try:
            response = (
                self.supabase.table("workout_programs")
                .select("*")
                .eq("user_id", user_id)
                .eq("status", "active")
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            if not response.data:
                return "No active workout program"

            program = response.data[0]
            parts = []

            if name := program.get("name"):
                parts.append(f"Program: {name}")
            if desc := program.get("description"):
                parts.append(f"Description: {desc}")
            if goal := program.get("goal"):
                parts.append(f"Goal: {goal}")
            if freq := program.get("frequency_per_week"):
                parts.append(f"Frequency: {freq}x per week")
            if start := program.get("start_date"):
                parts.append(f"Started: {start}")

            return "\n".join(parts)

        except Exception as e:
            logger.error(f"Error getting active workout program: {e}")
            return ""

    async def _get_active_nutrition_program(self, user_id: str) -> str:
        """Get active nutrition program."""
        try:
            response = (
                self.supabase.table("nutrition_programs")
                .select("*")
                .eq("user_id", user_id)
                .eq("status", "active")
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            if not response.data:
                return "No active nutrition program"

            program = response.data[0]
            parts = []

            if name := program.get("name"):
                parts.append(f"Program: {name}")
            if desc := program.get("description"):
                parts.append(f"Description: {desc}")
            if goal := program.get("goal"):
                parts.append(f"Goal: {goal}")
            if cals := program.get("target_calories"):
                parts.append(f"Target Calories: {cals}")
            if protein := program.get("target_protein_grams"):
                parts.append(f"Target Protein: {protein}g")
            if carbs := program.get("target_carbs_grams"):
                parts.append(f"Target Carbs: {carbs}g")
            if fat := program.get("target_fat_grams"):
                parts.append(f"Target Fat: {fat}g")

            return "\n".join(parts)

        except Exception as e:
            logger.error(f"Error getting active nutrition program: {e}")
            return ""

    async def _get_active_ai_program(self, user_id: str) -> str:
        """
        Get user's active AI-generated program with current status.

        Returns comprehensive program context including:
        - Program metadata (name, duration, current day)
        - Program generation questions/answers
        - Current week's schedule overview
        - Today's planned meals and workouts
        - Upcoming days (next 3 days)
        """
        try:
            # Get active AI-generated program
            program_response = (
                self.supabase.table("ai_generated_programs")
                .select("*")
                .eq("user_id", user_id)
                .eq("is_active", True)
                .order("created_at", desc=True)
                .limit(1)
                .execute()
            )

            if not program_response.data:
                return "No active AI-generated program"

            program = program_response.data[0]
            parts = []

            # Program metadata
            if name := program.get("name"):
                parts.append(f"AI Program: {name}")
            if desc := program.get("description"):
                parts.append(f"Description: {desc}")

            duration_weeks = program.get("duration_weeks", 12)
            total_days = program.get("total_days", 84)
            current_day = program.get("current_day", 1)

            parts.append(f"Duration: {duration_weeks} weeks ({total_days} days)")
            parts.append(f"Current Day: {current_day}/{total_days}")
            parts.append(f"Status: {program.get('status', 'active')}")

            # Program generation preferences (from questions_answers JSONB)
            if qa := program.get("questions_answers"):
                if isinstance(qa, dict) and qa:
                    parts.append("\n## Program Preferences:")
                    for key, value in qa.items():
                        if value and key not in ['created_at', 'updated_at', 'session_id']:
                            label = key.replace('_', ' ').title()
                            parts.append(f"  - {label}: {value}")

            # Get today's program day
            program_id = program["id"]
            today_response = (
                self.supabase.table("ai_program_days")
                .select("*, ai_program_items(*)")
                .eq("program_id", program_id)
                .eq("day_number", current_day)
                .single()
                .execute()
            )

            if today_response.data:
                today = today_response.data
                parts.append(f"\n## Today (Day {current_day}):")

                if day_name := today.get("day_name"):
                    parts.append(f"  {day_name}")
                if day_focus := today.get("day_focus"):
                    parts.append(f"  Focus: {day_focus}")

                # Today's meals and workouts
                if items := today.get("ai_program_items"):
                    meals = [item for item in items if item.get("item_type") == "meal"]
                    workouts = [item for item in items if item.get("item_type") == "workout"]

                    if meals:
                        parts.append("\n  Planned Meals:")
                        for meal in sorted(meals, key=lambda x: x.get("item_order", 0)):
                            meal_type = meal.get("meal_type", "Meal")
                            meal_name = meal.get("meal_name", "")
                            calories = meal.get("meal_calories", 0)
                            parts.append(f"    - {meal_type.title()}: {meal_name} ({calories} kcal)")

                    if workouts:
                        parts.append("\n  Planned Workouts:")
                        for workout in sorted(workouts, key=lambda x: x.get("item_order", 0)):
                            workout_name = workout.get("workout_name", "Workout")
                            workout_type = workout.get("workout_type", "")
                            duration = workout.get("workout_duration_minutes", 0)
                            parts.append(f"    - {workout_name} ({workout_type}, {duration} min)")

            # Get upcoming days (next 3 days)
            upcoming_response = (
                self.supabase.table("ai_program_days")
                .select("day_number, day_name, day_focus")
                .eq("program_id", program_id)
                .gt("day_number", current_day)
                .lte("day_number", current_day + 3)
                .order("day_number", desc=False)
                .execute()
            )

            if upcoming_response.data and len(upcoming_response.data) > 0:
                parts.append("\n## Upcoming Days:")
                for day in upcoming_response.data:
                    day_num = day.get("day_number")
                    day_name = day.get("day_name", f"Day {day_num}")
                    day_focus = day.get("day_focus", "")
                    parts.append(f"  - Day {day_num}: {day_name} ({day_focus})")

            return "\n".join(parts)

        except Exception as e:
            logger.error(f"Error getting active AI program: {e}")
            return ""

    async def _get_recent_workouts(self, user_id: str, days: int) -> str:
        """Get recent workouts."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)

            response = (
                self.supabase.table("workout_completions")
                .select("*")
                .eq("user_id", user_id)
                .gte("completed_at", cutoff_date.isoformat())
                .order("completed_at", desc=True)
                .limit(10)
                .execute()
            )

            if not response.data:
                return "No recent workouts"

            workouts = response.data
            parts = []

            for workout in workouts:
                workout_parts = []
                workout_name = workout.get('workout_name', 'Workout')
                workout_parts.append(f"- {workout_name} ({workout.get('completed_at')})")
                workout_parts.append(f"  Duration: {workout.get('duration_minutes', 'N/A')} min")

                if rpe := workout.get('rpe'):
                    workout_parts.append(f"  RPE: {rpe}/10")

                if notes := workout.get('notes'):
                    workout_parts.append(f"  Notes: {notes}")

                if exercises := workout.get('exercises'):
                    if isinstance(exercises, list):
                        workout_parts.append(f"  Exercises: {len(exercises)}")

                parts.append("\n".join(workout_parts))

            return "\n\n".join(parts)

        except Exception as e:
            logger.error(f"Error getting recent workouts: {e}")
            return ""

    async def _get_recent_meals(self, user_id: str, days: int) -> str:
        """Get recent meals."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)

            response = (
                self.supabase.table("meals")
                .select("*")
                .eq("user_id", user_id)
                .gte("logged_at", cutoff_date.isoformat())
                .order("logged_at", desc=True)
                .limit(10)
                .execute()
            )

            if not response.data:
                return "No recent meals"

            meals = response.data
            parts = []

            for meal in meals:
                meal_parts = []
                meal_name = meal.get('description') or meal.get('name', 'Meal')
                meal_parts.append(f"- {meal_name} ({meal.get('logged_at')})")

                cals = meal.get('calories') or meal.get('total_calories', 0)
                protein = meal.get('protein_g') or meal.get('total_protein_g', 0)
                carbs = meal.get('carbs_g') or meal.get('total_carbs_g', 0)
                fat = meal.get('fat_g') or meal.get('total_fat_g', 0)

                meal_parts.append(f"  Cals: {cals}, P: {protein}g, C: {carbs}g, F: {fat}g")

                parts.append("\n".join(meal_parts))

            return "\n\n".join(parts)

        except Exception as e:
            logger.error(f"Error getting recent meals: {e}")
            return ""

    async def _get_exercise_progress(self, user_id: str) -> str:
        """Get exercise progress tracking data."""
        try:
            # Get top exercises by frequency
            response = (
                self.supabase.table("exercise_progress")
                .select("*")
                .eq("user_id", user_id)
                .order("date", desc=True)
                .limit(20)
                .execute()
            )

            if not response.data:
                return "No exercise progress tracked yet"

            progress_data = response.data

            # Group by exercise
            exercise_dict: Dict[str, List[Dict[str, Any]]] = {}
            for entry in progress_data:
                exercise_name = entry.get("exercise_name")
                if exercise_name not in exercise_dict:
                    exercise_dict[exercise_name] = []
                exercise_dict[exercise_name].append(entry)

            parts = []
            for exercise_name, entries in list(exercise_dict.items())[:5]:  # Top 5 exercises
                latest = entries[0]
                parts.append(
                    f"- {exercise_name}: {latest.get('max_weight')}{latest.get('weight_unit')} "
                    f"x {latest.get('max_reps')} reps (Latest: {latest.get('date')})"
                )

            return "\n".join(parts)

        except Exception as e:
            logger.error(f"Error getting exercise progress: {e}")
            return ""

    async def _get_nutrition_compliance(self, user_id: str, days: int) -> str:
        """Get nutrition compliance data."""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)

            response = (
                self.supabase.table("nutrition_compliance")
                .select("*")
                .eq("user_id", user_id)
                .gte("date", cutoff_date.date().isoformat())
                .order("date", desc=True)
                .execute()
            )

            if not response.data:
                return "No compliance data yet"

            compliance_data = response.data

            # Calculate averages
            total_score = sum(entry.get("compliance_score", 0) for entry in compliance_data)
            avg_score = total_score / len(compliance_data) if compliance_data else 0

            parts = []
            parts.append(f"Average Compliance Score: {avg_score:.1f}%")
            parts.append(f"Days Tracked: {len(compliance_data)}")

            # Recent trend (last 7 days)
            recent_7 = compliance_data[:7]
            if recent_7:
                recent_avg = sum(entry.get("compliance_score", 0) for entry in recent_7) / len(recent_7)
                parts.append(f"Last 7 Days Average: {recent_avg:.1f}%")

            return "\n".join(parts)

        except Exception as e:
            logger.error(f"Error getting nutrition compliance: {e}")
            return ""

    async def _get_recovery_metrics(self, user_id: str, days: int) -> str:
        """
        Get Garmin recovery and health metrics.

        Fetches:
        - Sleep data (duration, quality, stages, HRV during sleep)
        - HRV status (daily averages, trends)
        - Stress levels (current, daily average, rest periods)
        - Body Battery (current level, charge/drain, daily patterns)
        - Readiness score (overall recovery status)

        Args:
            user_id: User's unique identifier
            days: Number of days to look back

        Returns:
            Formatted recovery metrics string with trends and insights
        """
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            parts = []

            # === SLEEP DATA ===
            sleep_response = (
                self.supabase.table("sleep_logs")
                .select("*")
                .eq("user_id", user_id)
                .eq("source", "garmin")  # Filter for Garmin data only
                .gte("sleep_date", cutoff_date.date().isoformat())
                .order("sleep_date", desc=True)
                .limit(7)  # Last 7 nights
                .execute()
            )

            if sleep_response.data:
                sleep_data = sleep_response.data
                parts.append("### Sleep Quality")

                # Latest sleep
                latest_sleep = sleep_data[0]
                total_duration = latest_sleep.get("total_sleep_minutes", 0) / 60  # Convert to hours
                sleep_score = latest_sleep.get("sleep_score")
                deep_sleep = latest_sleep.get("deep_sleep_minutes", 0) / 60  # Convert to hours
                rem_sleep = latest_sleep.get("rem_sleep_minutes", 0) / 60  # Convert to hours
                light_sleep = latest_sleep.get("light_sleep_minutes", 0) / 60  # Convert to hours
                awake_time = latest_sleep.get("awake_minutes", 0)  # Already in minutes
                avg_hrv = latest_sleep.get("avg_hrv_ms")

                parts.append(f"Last Night ({latest_sleep.get('sleep_date')}):")
                parts.append(f"  - Total Sleep: {total_duration:.1f} hours")
                if sleep_score:
                    parts.append(f"  - Sleep Score: {sleep_score}/100")
                parts.append(f"  - Deep Sleep: {deep_sleep:.1f}h | REM: {rem_sleep:.1f}h | Light: {light_sleep:.1f}h")
                if awake_time > 0:
                    parts.append(f"  - Awake Time: {awake_time:.0f} minutes")
                if avg_hrv:
                    parts.append(f"  - Average HRV: {avg_hrv} ms")

                # 7-day average
                if len(sleep_data) >= 3:
                    avg_duration = sum(s.get("total_sleep_minutes", 0) for s in sleep_data) / len(sleep_data) / 60
                    avg_score = sum(s.get("sleep_score", 0) for s in sleep_data if s.get("sleep_score")) / len([s for s in sleep_data if s.get("sleep_score")])
                    parts.append(f"\n7-Day Average:")
                    parts.append(f"  - Sleep Duration: {avg_duration:.1f} hours")
                    if avg_score > 0:
                        parts.append(f"  - Sleep Score: {avg_score:.1f}/100")

                parts.append("")

            # === HRV STATUS ===
            hrv_response = (
                self.supabase.table("hrv_logs")
                .select("*")
                .eq("user_id", user_id)
                .eq("source", "garmin")  # Filter for Garmin data only
                .gte("recorded_at", cutoff_date.isoformat())
                .order("recorded_at", desc=True)
                .limit(7)
                .execute()
            )

            if hrv_response.data:
                hrv_data = hrv_response.data
                parts.append("### Heart Rate Variability (HRV)")

                # Latest HRV
                latest_hrv = hrv_data[0]
                hrv_rmssd = latest_hrv.get("hrv_rmssd_ms")
                hrv_sdnn = latest_hrv.get("hrv_sdnn_ms")
                measurement_type = latest_hrv.get("measurement_type", "").title()

                parts.append(f"Latest ({latest_hrv.get('recorded_at', '')[:10]}):")
                if hrv_rmssd:
                    parts.append(f"  - HRV RMSSD: {hrv_rmssd} ms")
                if hrv_sdnn:
                    parts.append(f"  - HRV SDNN: {hrv_sdnn} ms")
                if measurement_type:
                    parts.append(f"  - Measurement Type: {measurement_type}")

                # Trend
                if len(hrv_data) >= 3:
                    recent_avg = sum(h.get("hrv_rmssd_ms", 0) for h in hrv_data[:3] if h.get("hrv_rmssd_ms")) / len([h for h in hrv_data[:3] if h.get("hrv_rmssd_ms")])
                    older_avg = sum(h.get("hrv_rmssd_ms", 0) for h in hrv_data[3:] if h.get("hrv_rmssd_ms")) / len([h for h in hrv_data[3:] if h.get("hrv_rmssd_ms")]) if len(hrv_data) > 3 else recent_avg

                    if recent_avg > 0 and older_avg > 0:
                        trend = "improving" if recent_avg > older_avg else "declining" if recent_avg < older_avg else "stable"
                        parts.append(f"  - Trend: {trend}")

                parts.append("")

            # === STRESS LEVELS ===
            stress_response = (
                self.supabase.table("stress_logs")
                .select("*")
                .eq("user_id", user_id)
                .eq("source", "garmin")  # Filter for Garmin data only
                .gte("recorded_at", cutoff_date.isoformat())
                .order("recorded_at", desc=True)
                .limit(7)
                .execute()
            )

            if stress_response.data:
                stress_data = stress_response.data
                parts.append("### Stress Levels")

                # Latest stress
                latest_stress = stress_data[0]
                avg_stress = latest_stress.get("avg_stress_level")
                max_stress = latest_stress.get("max_stress_level")
                rest_time = latest_stress.get("rest_minutes", 0) / 60  # Convert to hours

                parts.append(f"Latest ({latest_stress.get('recorded_at', '')[:10]}):")
                if avg_stress:
                    parts.append(f"  - Average Stress: {avg_stress}/100")
                if max_stress:
                    parts.append(f"  - Peak Stress: {max_stress}/100")
                if rest_time > 0:
                    parts.append(f"  - Rest Time: {rest_time:.1f}h")

                # Weekly average
                if len(stress_data) >= 3:
                    weekly_avg_stress = sum(s.get("avg_stress_level", 0) for s in stress_data if s.get("avg_stress_level")) / len([s for s in stress_data if s.get("avg_stress_level")])
                    parts.append(f"\n7-Day Average Stress: {weekly_avg_stress:.1f}/100")

                parts.append("")

            # === BODY BATTERY ===
            battery_response = (
                self.supabase.table("body_battery_logs")
                .select("*")
                .eq("user_id", user_id)
                .eq("source", "garmin")  # Filter for Garmin data only
                .gte("date", cutoff_date.date().isoformat())
                .order("date", desc=True)
                .limit(7)
                .execute()
            )

            if battery_response.data:
                battery_data = battery_response.data
                parts.append("### Body Battery (Energy Levels)")

                # Latest body battery
                latest_battery = battery_data[0]
                battery_level = latest_battery.get("battery_level")
                charged = latest_battery.get("charged_value")
                drained = latest_battery.get("drained_value")

                parts.append(f"Latest ({latest_battery.get('date')}):")
                if battery_level is not None:
                    parts.append(f"  - Current Level: {battery_level}/100")
                if charged:
                    parts.append(f"  - Charged: +{charged}")
                if drained:
                    parts.append(f"  - Drained: -{drained}")
                if charged and drained:
                    net = charged - drained
                    net_label = f"+{net}" if net > 0 else str(net)
                    parts.append(f"  - Net Change: {net_label}")

                # 7-day pattern
                if len(battery_data) >= 3:
                    avg_level = sum(b.get("battery_level", 0) for b in battery_data) / len(battery_data)
                    parts.append(f"\n7-Day Average:")
                    parts.append(f"  - Average Level: {avg_level:.1f}/100")

                parts.append("")

            # === READINESS SCORE ===
            readiness_response = (
                self.supabase.table("daily_readiness")
                .select("*")
                .eq("user_id", user_id)
                .gte("date", cutoff_date.date().isoformat())
                .order("date", desc=True)
                .limit(7)
                .execute()
            )

            if readiness_response.data:
                readiness_data = readiness_response.data
                parts.append("### Training Readiness")

                # Latest readiness
                latest_readiness = readiness_data[0]
                score = latest_readiness.get("readiness_score")
                status = latest_readiness.get("readiness_status", "").title()

                parts.append(f"Latest ({latest_readiness.get('date')}):")
                if score is not None:
                    parts.append(f"  - Readiness Score: {score}/100")
                    if score >= 75:
                        recommendation = "HIGH - Ready for intense training"
                    elif score >= 50:
                        recommendation = "MODERATE - Good for moderate training"
                    else:
                        recommendation = "LOW - Focus on recovery, light activity only"
                    parts.append(f"  - Status: {recommendation}")
                if status:
                    parts.append(f"  - Readiness Status: {status}")

                # 7-day trend
                if len(readiness_data) >= 3:
                    avg_readiness = sum(r.get("readiness_score", 0) for r in readiness_data if r.get("readiness_score")) / len([r for r in readiness_data if r.get("readiness_score")])
                    parts.append(f"\n7-Day Average: {avg_readiness:.1f}/100")

                parts.append("")

            # === RECOVERY INSIGHTS ===
            if sleep_response.data or hrv_response.data or readiness_response.data:
                parts.append("### Recovery Insights")

                # Determine overall recovery status
                recovery_signals = []

                if sleep_response.data:
                    latest_sleep = sleep_response.data[0]
                    sleep_hours = latest_sleep.get("total_sleep_minutes", 0) / 60
                    if sleep_hours >= 7:
                        recovery_signals.append("Good sleep duration")
                    elif sleep_hours < 6:
                        recovery_signals.append("⚠️ Insufficient sleep (<6h)")

                if hrv_response.data:
                    latest_hrv = hrv_response.data[0]
                    hrv_value = latest_hrv.get("hrv_rmssd_ms", 0)
                    if hrv_value >= 50:
                        recovery_signals.append("HRV is balanced/high")
                    elif hrv_value > 0 and hrv_value < 40:
                        recovery_signals.append("⚠️ Low HRV detected")

                if stress_response.data:
                    latest_stress = stress_response.data[0]
                    avg_stress = latest_stress.get("avg_stress_level", 0)
                    if avg_stress < 30:
                        recovery_signals.append("Low stress levels")
                    elif avg_stress > 50:
                        recovery_signals.append("⚠️ Elevated stress levels")

                if readiness_response.data:
                    latest_readiness = readiness_response.data[0]
                    score = latest_readiness.get("readiness_score", 0)
                    if score >= 75:
                        recovery_signals.append("High training readiness")
                    elif score < 50:
                        recovery_signals.append("⚠️ Low training readiness")

                if recovery_signals:
                    for signal in recovery_signals:
                        parts.append(f"  • {signal}")
                    parts.append("")

                    # Training recommendation
                    warning_count = sum(1 for s in recovery_signals if "⚠️" in s)
                    if warning_count == 0:
                        parts.append("**Training Recommendation**: Fully recovered, ready for high-intensity training")
                    elif warning_count == 1:
                        parts.append("**Training Recommendation**: Moderate recovery, suitable for moderate intensity")
                    else:
                        parts.append("**Training Recommendation**: Poor recovery, prioritize rest and light activity")

            if not parts:
                return "No recovery data available from Garmin. Consider connecting your Garmin device for personalized recovery insights."

            return "\n".join(parts)

        except Exception as e:
            logger.error(f"Error getting recovery metrics: {e}")
            return ""

    async def _get_recovery_performance_correlations(self, user_id: str, days: int) -> str:
        """
        Analyze correlations between recovery metrics and training performance.

        Identifies patterns such as:
        - How sleep quality affects workout performance (RPE, completion)
        - HRV trends vs training load tolerance
        - Stress impact on recovery and performance
        - Body battery patterns and workout energy
        - Readiness score vs workout completion rates

        Args:
            user_id: User's unique identifier
            days: Number of days to analyze (minimum 14 for meaningful correlations)

        Returns:
            Formatted insights string with actionable recommendations
        """
        try:
            if days < 14:
                return ""  # Need at least 2 weeks of data for correlations

            cutoff_date = datetime.utcnow() - timedelta(days=days)
            parts = []

            # Fetch recovery data
            sleep_data = (
                self.supabase.table("sleep_logs")
                .select("sleep_date, total_sleep_minutes, sleep_score, avg_hrv_ms")
                .eq("user_id", user_id)
                .eq("source", "garmin")
                .gte("sleep_date", cutoff_date.date().isoformat())
                .order("sleep_date", desc=False)
                .execute()
            ).data or []

            hrv_data = (
                self.supabase.table("hrv_logs")
                .select("recorded_at, hrv_rmssd_ms, hrv_sdnn_ms")
                .eq("user_id", user_id)
                .eq("source", "garmin")
                .gte("recorded_at", cutoff_date.isoformat())
                .order("recorded_at", desc=False)
                .execute()
            ).data or []

            stress_data = (
                self.supabase.table("stress_logs")
                .select("recorded_at, avg_stress_level, max_stress_level")
                .eq("user_id", user_id)
                .eq("source", "garmin")
                .gte("recorded_at", cutoff_date.isoformat())
                .order("recorded_at", desc=False)
                .execute()
            ).data or []

            readiness_data = (
                self.supabase.table("daily_readiness")
                .select("date, readiness_score")
                .eq("user_id", user_id)
                .gte("date", cutoff_date.date().isoformat())
                .order("date", desc=False)
                .execute()
            ).data or []

            # Fetch workout performance data
            workouts = (
                self.supabase.table("workout_completions")
                .select("completed_at, rpe, duration_minutes, exercises")
                .eq("user_id", user_id)
                .gte("completed_at", cutoff_date.isoformat())
                .order("completed_at", desc=False)
                .execute()
            ).data or []

            # Fetch activities for additional performance data
            activities = (
                self.supabase.table("activities")
                .select("start_date, duration_minutes, average_heartrate, perceived_exertion")
                .eq("user_id", user_id)
                .gte("start_date", cutoff_date.isoformat())
                .order("start_date", desc=False)
                .execute()
            ).data or []

            if not (sleep_data or hrv_data or readiness_data) or not (workouts or activities):
                return ""  # Need both recovery and performance data

            # === CORRELATION 1: Sleep Quality vs Workout Performance ===
            if sleep_data and workouts:
                # Map sleep data to workout days
                sleep_by_date = {s['sleep_date']: s for s in sleep_data}

                good_sleep_workouts = []
                poor_sleep_workouts = []

                for workout in workouts:
                    workout_date = workout['completed_at'].split('T')[0]
                    prev_night = sleep_by_date.get(workout_date)

                    if prev_night:
                        sleep_hours = prev_night.get('total_sleep_minutes', 0) / 60
                        sleep_score = prev_night.get('sleep_score', 0)
                        rpe = workout.get('rpe', 0)

                        # Categorize sleep quality
                        if sleep_hours >= 7 and sleep_score >= 70:
                            good_sleep_workouts.append({'rpe': rpe, 'duration': workout.get('duration_minutes', 0)})
                        elif sleep_hours < 6 or sleep_score < 50:
                            poor_sleep_workouts.append({'rpe': rpe, 'duration': workout.get('duration_minutes', 0)})

                if good_sleep_workouts and poor_sleep_workouts:
                    good_avg_rpe = sum(w['rpe'] for w in good_sleep_workouts if w['rpe']) / len([w for w in good_sleep_workouts if w['rpe']]) if any(w['rpe'] for w in good_sleep_workouts) else 0
                    poor_avg_rpe = sum(w['rpe'] for w in poor_sleep_workouts if w['rpe']) / len([w for w in poor_sleep_workouts if w['rpe']]) if any(w['rpe'] for w in poor_sleep_workouts) else 0

                    if good_avg_rpe > 0 and poor_avg_rpe > 0:
                        parts.append("### Sleep Quality → Workout Performance")
                        parts.append(f"After good sleep (7+ hours, score ≥70): Average RPE {good_avg_rpe:.1f}/10")
                        parts.append(f"After poor sleep (<6 hours, score <50): Average RPE {poor_avg_rpe:.1f}/10")

                        if poor_avg_rpe > good_avg_rpe:
                            diff = poor_avg_rpe - good_avg_rpe
                            parts.append(f"\n💡 **Insight**: Poor sleep increases workout difficulty by {diff:.1f} RPE points. Prioritize 7-8 hours of sleep before hard training days.")
                        parts.append("")

            # === CORRELATION 2: HRV Trends vs Training Load ===
            if hrv_data and (workouts or activities):
                # Calculate weekly training load (total duration)
                weekly_loads = {}

                for workout in workouts:
                    week = workout['completed_at'][:10]  # Use date as week proxy
                    weekly_loads[week] = weekly_loads.get(week, 0) + workout.get('duration_minutes', 0)

                for activity in activities:
                    week = activity['start_date'][:10]
                    weekly_loads[week] = weekly_loads.get(week, 0) + activity.get('duration_minutes', 0)

                # Map HRV to weeks
                hrv_by_week = {}
                for hrv in hrv_data:
                    week = hrv['recorded_at'][:10]  # Get date part from timestamp
                    hrv_by_week[week] = hrv.get('hrv_rmssd_ms', 0)

                # Find correlations
                high_load_low_hrv_count = 0
                moderate_load_balanced_hrv_count = 0

                for week, load in weekly_loads.items():
                    hrv_val = hrv_by_week.get(week, 0)

                    if load > 300 and hrv_val > 0:  # High load weeks (5+ hours training)
                        if hrv_val < 50:  # Low HRV
                            high_load_low_hrv_count += 1
                    elif 120 <= load <= 300 and hrv_val >= 50:  # Moderate load, balanced HRV
                        moderate_load_balanced_hrv_count += 1

                if high_load_low_hrv_count > 0:
                    parts.append("### HRV Trends → Training Load Tolerance")
                    parts.append(f"⚠️ Detected {high_load_low_hrv_count} week(s) with high training load (5+ hours) and low HRV (<50ms)")
                    parts.append("\n💡 **Insight**: Your HRV drops during heavy training weeks. Consider:")
                    parts.append("  • Incorporating more deload weeks (50-60% volume)")
                    parts.append("  • Adding extra rest days when HRV drops below personal baseline")
                    parts.append("  • Prioritizing sleep quality during high-volume training blocks")
                    parts.append("")

            # === CORRELATION 3: Readiness Score vs Workout Completion ===
            if readiness_data and workouts:
                readiness_by_date = {r['date']: r for r in readiness_data}

                high_readiness_workouts = 0
                low_readiness_workouts = 0
                high_readiness_total = 0
                low_readiness_total = 0

                for workout in workouts:
                    workout_date = workout['completed_at'].split('T')[0]
                    readiness = readiness_by_date.get(workout_date)

                    if readiness:
                        score = readiness.get('readiness_score', 0)

                        if score >= 75:
                            high_readiness_workouts += 1
                            high_readiness_total += 1
                        elif score < 50:
                            low_readiness_workouts += 1
                            low_readiness_total += 1

                # Count days with readiness scores
                high_readiness_days = len([r for r in readiness_data if r.get('readiness_score', 0) >= 75])
                low_readiness_days = len([r for r in readiness_data if r.get('readiness_score', 0) < 50])

                if high_readiness_days > 0 and low_readiness_days > 0:
                    parts.append("### Training Readiness → Workout Patterns")
                    parts.append(f"High readiness days (≥75): {high_readiness_workouts} workouts completed")
                    parts.append(f"Low readiness days (<50): {low_readiness_workouts} workouts completed")

                    if low_readiness_workouts > high_readiness_workouts:
                        parts.append("\n💡 **Insight**: You often train on low readiness days. This may lead to:")
                        parts.append("  • Increased injury risk")
                        parts.append("  • Slower recovery")
                        parts.append("  • Reduced performance gains")
                        parts.append("\n**Recommendation**: When readiness <50, consider active recovery (walking, yoga, stretching) instead of intense training.")
                    parts.append("")

            # === CORRELATION 4: Stress Patterns ===
            if stress_data:
                high_stress_days = len([s for s in stress_data if s.get('avg_stress_level', 0) > 50])
                total_days = len(stress_data)

                if total_days > 0:
                    stress_pct = (high_stress_days / total_days) * 100

                    if stress_pct > 30:
                        parts.append("### Stress Management")
                        parts.append(f"High stress days (>50): {high_stress_days}/{total_days} days ({stress_pct:.0f}%)")
                        parts.append("\n💡 **Insight**: Elevated stress levels detected frequently. High stress impairs:")
                        parts.append("  • Recovery quality (slower muscle repair)")
                        parts.append("  • Sleep quality (disrupted REM sleep)")
                        parts.append("  • Training adaptations (elevated cortisol)")
                        parts.append("\n**Recommendations**:")
                        parts.append("  • Practice stress management: meditation, deep breathing, nature walks")
                        parts.append("  • Schedule easier training days after high-stress workdays")
                        parts.append("  • Consider adaptogenic supplements (ashwagandha, rhodiola) - consult your doctor first")
                        parts.append("")

            # === SUMMARY RECOMMENDATIONS ===
            if parts:
                parts.append("### Personalized Recovery Strategy")

                # Sleep recommendation
                if sleep_data:
                    avg_sleep = sum(s.get('total_sleep_minutes', 0) for s in sleep_data) / len(sleep_data) / 60
                    if avg_sleep < 7:
                        parts.append(f"🎯 **Priority #1**: Increase sleep to 7-9 hours (current average: {avg_sleep:.1f}h)")

                # HRV recommendation
                if hrv_data:
                    recent_hrv = hrv_data[-7:] if len(hrv_data) >= 7 else hrv_data
                    avg_recent_hrv = sum(h.get('hrv_rmssd_ms', 0) for h in recent_hrv if h.get('hrv_rmssd_ms')) / len([h for h in recent_hrv if h.get('hrv_rmssd_ms')]) if any(h.get('hrv_rmssd_ms') for h in recent_hrv) else 0

                    if avg_recent_hrv > 0 and avg_recent_hrv < 50:
                        parts.append(f"🎯 **Priority #2**: Improve HRV (current: {avg_recent_hrv:.0f}ms) through stress reduction and better sleep")

                # Training load recommendation
                if workouts or activities:
                    total_workouts = len(workouts) + len(activities)
                    avg_per_week = (total_workouts / days) * 7

                    if avg_per_week > 6:
                        parts.append(f"🎯 **Priority #3**: Reduce training frequency (current: {avg_per_week:.1f} sessions/week) - add 1-2 rest days")
                    elif avg_per_week < 3:
                        parts.append(f"🎯 **Opportunity**: Increase training frequency (current: {avg_per_week:.1f} sessions/week) for better results")

            if not parts:
                return ""

            return "\n".join(parts)

        except Exception as e:
            logger.error(f"Error analyzing recovery-performance correlations: {e}")
            return ""

    async def _search_coach_embeddings(
        self,
        query: str,
        user_id: str,
        limit: int = 5,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search coach_message_embeddings for relevant past conversations.

        This allows the AI coach to reference and learn from previous interactions,
        creating continuity and personalized coaching based on conversation history.

        Args:
            query: Search query text
            user_id: User UUID
            limit: Maximum number of results
            threshold: Minimum similarity threshold (0-1)

        Returns:
            List of relevant coach messages with similarity scores
        """
        try:
            logger.info(f"🔍 Searching coach embeddings for: '{query[:50]}...'")

            # Generate query embedding
            query_embedding = await self.embedding_service.generate_embedding(query)

            # Search coach_message_embeddings table using pgvector similarity
            # Note: This assumes coach_message_embeddings has a vector column and similarity function
            response = self.supabase.rpc(
                "match_coach_message_embeddings",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": threshold,
                    "match_count": limit,
                    "filter_user_id": user_id
                }
            ).execute()

            results = response.data or []

            if results:
                logger.info(f"✅ Found {len(results)} relevant coach messages")
            else:
                logger.info("No relevant coach messages found")

            return results

        except Exception as e:
            logger.error(f"❌ Error searching coach embeddings: {e}")
            logger.warning("Falling back to empty results (RPC function may not exist yet)")
            return []

    async def _get_rag_context(
        self,
        user_id: str,
        query: str,
        source_types: List[str],
        match_count: int = 5,
        include_images: bool = False
    ) -> str:
        """
        Get relevant context using REVOLUTIONARY MULTIMODAL RAG + COACH HISTORY.

        Searches across:
        1. Multimodal embeddings (text, images, audio transcripts)
        2. Coach conversation embeddings (past interactions)

        Combines and ranks results by similarity for optimal context.

        This is what makes the AI coach truly personalized and revolutionary!
        """
        try:
            logger.info(f"🔍 Multimodal RAG search for: '{query}' | sources={source_types}")

            # SEARCH 1: Multimodal embeddings (meals, workouts, activities)
            multimodal_results = await self.multimodal_service.search_by_text(
                query_text=query,
                user_id=user_id,
                source_types=source_types,
                data_types=['text', 'image'] if include_images else ['text'],  # Can include images!
                limit=match_count,
                threshold=0.5  # Lower threshold for broader context
            )

            # SEARCH 2: Coach conversation embeddings (past conversations)
            coach_results = await self._search_coach_embeddings(
                query=query,
                user_id=user_id,
                limit=3,  # Fewer coach results, they tend to be longer
                threshold=0.5
            )

            # MERGE results from both sources
            all_results = multimodal_results + coach_results

            if not all_results:
                logger.info("No RAG results found from any source")
                return ""

            # RANK by similarity (descending)
            all_results.sort(key=lambda x: x.get("similarity", 0), reverse=True)

            # LIMIT to match_count after merging
            results = all_results[:match_count]

            logger.info(f"✅ Found {len(results)} relevant context items ({len(multimodal_results)} multimodal + {len(coach_results)} coach)")

            parts = []
            for i, result in enumerate(results, 1):
                content_text = result.get("content_text", "")
                similarity = result.get("similarity", 0)
                source_type = result.get("source_type", "unknown")
                data_type = result.get("data_type", "text")
                storage_url = result.get("storage_url")
                metadata = result.get("metadata", {})
                role = result.get("role")  # For coach messages

                # Format based on data type and source
                if role:  # This is a coach conversation message
                    # Format coach conversation context
                    role_label = "User" if role == "user" else "Coach"
                    parts.append(
                        f"{i}. [PAST CONVERSATION - {role_label}] (similarity: {similarity:.2f})\n"
                        f"   {content_text}"
                    )
                elif data_type == "image" and storage_url:
                    # For images, include URL and any extracted text
                    parts.append(
                        f"{i}. [{source_type}] IMAGE (similarity: {similarity:.2f})\n"
                        f"   Image URL: {storage_url}\n"
                        f"   Context: {content_text or 'Visual content'}"
                    )
                elif data_type == "audio":
                    # For audio, include transcription
                    parts.append(
                        f"{i}. [{source_type}] AUDIO (similarity: {similarity:.2f})\n"
                        f"   Transcription: {content_text}"
                    )
                else:
                    # For text
                    parts.append(
                        f"{i}. [{source_type}] (similarity: {similarity:.2f})\n{content_text}"
                    )

                # Add metadata context if available
                if metadata:
                    key_meta = []
                    if metadata.get('calories'):
                        key_meta.append(f"Calories: {metadata['calories']}")
                    if metadata.get('duration_minutes'):
                        key_meta.append(f"Duration: {metadata['duration_minutes']}min")
                    if metadata.get('protein_g'):
                        key_meta.append(f"Protein: {metadata['protein_g']}g")

                    if key_meta:
                        parts.append(f"   Metadata: {', '.join(key_meta)}")

            return "\n\n".join(parts)

        except Exception as e:
            logger.error(f"❌ Error getting multimodal RAG context: {e}")
            # Fallback to old embedding service if multimodal fails
            try:
                logger.warning("Falling back to legacy embedding service")
                results = await self.embedding_service.search_similar(
                    query=query,
                    user_id=user_id,
                    limit=match_count,
                    threshold=0.7,
                    source_types=source_types
                )

                if not results:
                    return ""

                parts = []
                for i, result in enumerate(results, 1):
                    content = result.get("content", "")
                    similarity = result.get("similarity", 0)
                    source_type = result.get("source_type", "unknown")

                    parts.append(
                        f"{i}. [{source_type}] (similarity: {similarity:.2f})\n{content}"
                    )

                return "\n\n".join(parts)
            except:
                return ""

    async def _get_recent_coach_interactions(
        self,
        user_id: str,
        coach_type: str,
        limit: int = 5
    ) -> str:
        """Get recent coach interactions."""
        try:
            # Get coach persona ID
            persona_response = (
                self.supabase.table("coach_personas")
                .select("id")
                .eq("name", coach_type)
                .single()
                .execute()
            )

            if not persona_response.data:
                return ""

            persona_id = persona_response.data["id"]

            # Get conversation
            conv_response = (
                self.supabase.table("coach_conversations")
                .select("messages")
                .eq("user_id", user_id)
                .eq("coach_persona_id", persona_id)
                .order("last_message_at", desc=True)
                .limit(1)
                .execute()
            )

            if not conv_response.data:
                return "No previous interactions"

            messages = conv_response.data[0].get("messages", [])
            recent_messages = messages[-limit * 2:]  # Get last N user/assistant pairs

            parts = []
            for msg in recent_messages:
                role = msg.get("role", "unknown")
                content = msg.get("content", "")
                timestamp = msg.get("timestamp", "")

                if role == "user":
                    parts.append(f"User: {content}")
                elif role == "assistant":
                    parts.append(f"Coach: {content}")

            return "\n\n".join(parts)

        except Exception as e:
            logger.error(f"Error getting recent coach interactions: {e}")
            return ""


# Global instance
_context_builder: Optional[ContextBuilder] = None


def get_context_builder() -> ContextBuilder:
    """Get the global ContextBuilder instance."""
    global _context_builder
    if _context_builder is None:
        _context_builder = ContextBuilder()
    return _context_builder
