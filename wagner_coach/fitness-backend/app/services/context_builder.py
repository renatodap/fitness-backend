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

        # 6. Recent Coach Interactions
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
        """Get user profile and goals."""
        try:
            # Get profile
            profile_response = (
                self.supabase.table("profiles")
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
            if gender := profile.get("gender"):
                parts.append(f"Gender: {gender}")

            # Physical stats
            if height := profile.get("height_cm"):
                parts.append(f"Height: {height} cm")
            if weight := profile.get("weight_kg"):
                parts.append(f"Weight: {weight} kg")

            # Goals
            if goal := profile.get("primary_goal"):
                parts.append(f"Primary Goal: {goal}")
            if fitness_level := profile.get("fitness_level"):
                parts.append(f"Fitness Level: {fitness_level}")
            if target_weight := profile.get("target_weight_kg"):
                parts.append(f"Target Weight: {target_weight} kg")

            # Preferences
            if workout_pref := profile.get("workout_preferences"):
                parts.append(f"Workout Preferences: {workout_pref}")
            if dietary_pref := profile.get("dietary_preferences"):
                parts.append(f"Dietary Preferences: {dietary_pref}")

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
                self.supabase.table("meal_logs")
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

    async def _get_rag_context(
        self,
        user_id: str,
        query: str,
        source_types: List[str],
        match_count: int = 5,
        include_images: bool = False
    ) -> str:
        """
        Get relevant context using REVOLUTIONARY MULTIMODAL RAG.

        Searches across ALL modalities (text, images, audio transcripts)
        using vector similarity in the multimodal_embeddings table.

        This is what makes the AI coach truly personalized and revolutionary!
        """
        try:
            logger.info(f"🔍 Multimodal RAG search for: '{query}' | sources={source_types}")

            # Search using multimodal service (searches text, images, audio, everything!)
            results = await self.multimodal_service.search_by_text(
                query_text=query,
                user_id=user_id,
                source_types=source_types,
                data_types=['text', 'image'] if include_images else ['text'],  # Can include images!
                limit=match_count,
                threshold=0.5  # Lower threshold for broader context
            )

            if not results:
                logger.info("No RAG results found")
                return ""

            logger.info(f"✅ Found {len(results)} relevant context items")

            parts = []
            for i, result in enumerate(results, 1):
                content_text = result.get("content_text", "")
                similarity = result.get("similarity", 0)
                source_type = result.get("source_type", "unknown")
                data_type = result.get("data_type", "text")
                storage_url = result.get("storage_url")
                metadata = result.get("metadata", {})

                # Format based on data type
                if data_type == "image" and storage_url:
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
