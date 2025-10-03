"""
RAG Service

Retrieval-Augmented Generation service for building context for AI coaching.
"""

import logging
from typing import Any, Dict, List, Optional
from datetime import datetime, timedelta

from app.services.supabase_service import get_service_client
from app.services.embedding_service import EmbeddingService

logger = logging.getLogger(__name__)


class RAGService:
    """
    Service for building context using retrieval-augmented generation.

    Combines database queries with semantic search to build comprehensive
    context for AI coaching responses.
    """

    def __init__(self):
        """Initialize with Supabase and Embedding services."""
        self.supabase = get_service_client()
        self.embedding_service = EmbeddingService()

    async def get_user_context(
        self,
        user_id: str,
        query: str,
        include_history: bool = True
    ) -> Dict[str, Any]:
        """
        Get comprehensive user context for query.

        Args:
            user_id: User UUID
            query: User's query or conversation context
            include_history: Whether to include conversation history

        Returns:
            Dict with user context including profile, recent data, and relevant context
        """
        if not user_id:
            raise ValueError("user_id is required")

        context = {}

        # Get base profile data
        context["profile"] = await self._get_profile(user_id)

        # Get recent activity (last 7 days)
        context["recent_workouts"] = await self._get_recent_workouts(user_id, days=7)
        context["recent_meals"] = await self._get_recent_meals(user_id, days=7)
        context["recent_activities"] = await self._get_recent_activities(user_id, days=7)

        # Get relevant context via semantic search
        if query:
            context["relevant_context"] = await self._search_relevant_context(
                user_id, query, limit=5
            )

        # Get goals
        context["goals"] = await self._get_active_goals(user_id)

        # Get recent summaries
        context["summaries"] = await self._get_recent_summaries(user_id, limit=3)

        return context

    async def build_prompt_context(self, user_id: str, query: str) -> str:
        """
        Build formatted context string for LLM prompt.

        Args:
            user_id: User UUID
            query: User's query

        Returns:
            Formatted context string
        """
        context = await self.get_user_context(user_id, query)

        # Format context into readable string
        prompt_parts = []

        # Profile
        if context.get("profile"):
            profile = context["profile"]
            prompt_parts.append(f"User Profile: {profile.get('name', 'User')}")
            if profile.get("goals"):
                prompt_parts.append(f"Goals: {profile['goals']}")

        # Recent activity
        if context.get("recent_workouts"):
            workout_count = len(context["recent_workouts"])
            prompt_parts.append(f"Recent workouts (last 7 days): {workout_count} workouts")

        if context.get("recent_meals"):
            meal_count = len(context["recent_meals"])
            prompt_parts.append(f"Recent meals logged: {meal_count} meals")

        # Relevant context from semantic search
        if context.get("relevant_context"):
            prompt_parts.append("Relevant past context:")
            for item in context["relevant_context"][:3]:
                prompt_parts.append(f"- {item.get('content', '')[:200]}")

        return "\n\n".join(prompt_parts)

    async def _get_profile(self, user_id: str) -> Dict[str, Any]:
        """Get user profile."""
        try:
            response = self.supabase.table("profiles").select("*").eq("id", user_id).single().execute()
            return response.data
        except Exception as e:
            logger.error(f"Error fetching profile: {e}")
            return {}

    async def _get_recent_workouts(self, user_id: str, days: int = 7) -> List[Dict]:
        """Get recent workouts."""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            response = (
                self.supabase.table("workouts")
                .select("*")
                .eq("user_id", user_id)
                .gte("date", cutoff_date)
                .order("date", desc=True)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching workouts: {e}")
            return []

    async def _get_recent_meals(self, user_id: str, days: int = 7) -> List[Dict]:
        """Get recent meals."""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            response = (
                self.supabase.table("meals")
                .select("*")
                .eq("user_id", user_id)
                .gte("date", cutoff_date)
                .order("date", desc=True)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching meals: {e}")
            return []

    async def _get_recent_activities(self, user_id: str, days: int = 7) -> List[Dict]:
        """Get recent activities."""
        try:
            cutoff_date = (datetime.now() - timedelta(days=days)).date().isoformat()
            response = (
                self.supabase.table("activities")
                .select("*")
                .eq("user_id", user_id)
                .gte("date", cutoff_date)
                .order("date", desc=True)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching activities: {e}")
            return []

    async def _search_relevant_context(
        self, user_id: str, query: str, limit: int = 5
    ) -> List[Dict]:
        """Search for relevant context using embeddings."""
        try:
            return await self.embedding_service.search_similar(
                query=query,
                user_id=user_id,
                limit=limit,
                threshold=0.7
            )
        except Exception as e:
            logger.error(f"Error searching context: {e}")
            return []

    async def _get_active_goals(self, user_id: str) -> List[Dict]:
        """Get user's active goals."""
        try:
            response = (
                self.supabase.table("goals")
                .select("*")
                .eq("user_id", user_id)
                .eq("status", "active")
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching goals: {e}")
            return []

    async def _get_recent_summaries(self, user_id: str, limit: int = 3) -> List[Dict]:
        """Get recent summaries."""
        try:
            response = (
                self.supabase.table("summaries")
                .select("*")
                .eq("user_id", user_id)
                .order("period_start", desc=True)
                .limit(limit)
                .execute()
            )
            return response.data
        except Exception as e:
            logger.error(f"Error fetching summaries: {e}")
            return []
