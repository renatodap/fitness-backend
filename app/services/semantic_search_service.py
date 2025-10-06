"""
Semantic Search Service using Existing multimodal_embeddings Table

Provides vector similarity search for:
- Finding similar past meals, workouts, activities
- Retrieving relevant context for AI coach recommendations
- Pattern detection across user's fitness journey

Uses existing infrastructure:
- multimodal_embeddings table (pgvector)
- sentence-transformers (all-MiniLM-L6-v2, 384 dimensions)
- Cosine similarity search
"""

import logging
from typing import Any, Dict, List, Optional, Literal
from datetime import datetime, timedelta

from app.services.supabase_service import get_service_client
from app.services.multimodal_embedding_service import get_multimodal_service

logger = logging.getLogger(__name__)


SourceType = Literal["meal", "workout", "activity", "voice_note", "progress_photo", "quick_entry"]


class SemanticSearchService:
    """
    Semantic search using vector embeddings in multimodal_embeddings table.

    Enables:
    - "Find meals similar to chicken and rice"
    - "Show my hardest workouts"
    - "What did I eat last time I felt this way?"
    - AI coach context retrieval for personalized recommendations
    """

    def __init__(self):
        self.supabase = get_service_client()
        self.embedding_service = get_multimodal_service()

    async def search_similar_entries(
        self,
        user_id: str,
        query_text: str,
        source_type: Optional[SourceType] = None,
        limit: int = 10,
        recency_weight: float = 0.3,
        similarity_threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search for entries similar to query text using vector similarity.

        Args:
            user_id: User ID
            query_text: Natural language query (e.g., "chicken and rice meals")
            source_type: Filter by source type (meal, workout, activity, etc.)
            limit: Max results to return
            recency_weight: Weight for recency (0=ignore time, 1=only recent)
            similarity_threshold: Minimum similarity score (0-1)

        Returns:
            List of similar entries with metadata and scores
        """
        logger.info(f"[SemanticSearch] Query: '{query_text}' for user {user_id}")

        try:
            # Generate embedding for query text
            query_embedding = await self.embedding_service.embed_text(query_text)

            # Convert to list for SQL query
            query_embedding_list = query_embedding.tolist() if hasattr(query_embedding, 'tolist') else query_embedding

            # Use the semantic_search_entries RPC function from migration
            # This function is created in supabase_migration_semantic_search_helpers.sql
            result = self.supabase.rpc('semantic_search_entries', {
                'p_user_id': user_id,
                'p_query_embedding': query_embedding_list,
                'p_source_type': source_type,
                'p_limit': limit,
                'p_recency_weight': recency_weight,
                'p_similarity_threshold': similarity_threshold
            }).execute()

            if not result.data:
                logger.info(f"[SemanticSearch] No results found")
                return []

            logger.info(f"[SemanticSearch] Found {len(result.data)} results")
            return result.data

        except Exception as e:
            logger.error(f"[SemanticSearch] Search failed: {e}")
            # Fallback to simple SQL query without vector search
            return await self._fallback_search(user_id, query_text, source_type, limit)

    async def _fallback_search(
        self,
        user_id: str,
        query_text: str,
        source_type: Optional[str],
        limit: int
    ) -> List[Dict[str, Any]]:
        """
        Fallback: Simple text search without vector similarity.
        """
        try:
            query = self.supabase.table("multimodal_embeddings").select(
                "id, source_type, source_id, content_text, metadata, data_type, storage_url, created_at"
            ).eq("user_id", user_id)

            if source_type:
                query = query.eq("source_type", source_type)

            # Simple text search
            if query_text:
                query = query.ilike("content_text", f"%{query_text}%")

            result = query.order("created_at", desc=True).limit(limit).execute()

            return result.data if result.data else []

        except Exception as e:
            logger.error(f"[SemanticSearch] Fallback search failed: {e}")
            return []

    async def get_context_for_recommendation(
        self,
        user_id: str,
        context_query: str,
        max_entries: int = 5
    ) -> str:
        """
        Get relevant context for AI coach recommendations.

        Args:
            user_id: User ID
            context_query: What context to retrieve (e.g., "recent high-protein meals")
            max_entries: Max entries to include in context

        Returns:
            Formatted context string for AI coach
        """
        logger.info(f"[SemanticSearch] Getting context: '{context_query}'")

        # Search for relevant entries
        results = await self.search_similar_entries(
            user_id=user_id,
            query_text=context_query,
            limit=max_entries,
            recency_weight=0.5  # Balance similarity and recency
        )

        if not results:
            return "No relevant context found."

        # Format context for AI coach
        context_parts = []
        for entry in results:
            source_type = entry.get('source_type', 'unknown')
            content = entry.get('content_text', '')
            metadata = entry.get('metadata', {})
            created_at = entry.get('created_at', '')
            similarity = entry.get('similarity', 0)

            # Format based on source type
            if source_type == 'meal':
                context_parts.append(
                    f"[MEAL - {created_at}] {content}\n"
                    f"  Calories: {metadata.get('calories', 'N/A')}, "
                    f"Protein: {metadata.get('protein_g', 'N/A')}g, "
                    f"Quality Score: {metadata.get('meal_quality_score', 'N/A')}/10"
                )
            elif source_type == 'workout':
                context_parts.append(
                    f"[WORKOUT - {created_at}] {content}\n"
                    f"  Volume: {metadata.get('volume_load', 'N/A')}, "
                    f"RPE: {metadata.get('rpe', 'N/A')}/10, "
                    f"Status: {metadata.get('progressive_overload_status', 'N/A')}"
                )
            elif source_type == 'activity':
                context_parts.append(
                    f"[ACTIVITY - {created_at}] {content}\n"
                    f"  Duration: {metadata.get('duration_minutes', 'N/A')}min, "
                    f"Distance: {metadata.get('distance_km', 'N/A')}km, "
                    f"Performance: {metadata.get('performance_score', 'N/A')}/10"
                )
            else:
                context_parts.append(f"[{source_type.upper()} - {created_at}] {content}")

        context_str = "\n\n".join(context_parts)
        return f"Relevant Context (similarity-ranked):\n\n{context_str}"

    async def find_similar_meals(
        self,
        user_id: str,
        meal_description: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find meals similar to a description.

        Example: "high protein chicken meals" → returns similar past meals
        """
        return await self.search_similar_entries(
            user_id=user_id,
            query_text=meal_description,
            source_type="meal",
            limit=limit,
            recency_weight=0.2  # Prioritize similarity over recency
        )

    async def find_similar_workouts(
        self,
        user_id: str,
        workout_description: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find workouts similar to a description.

        Example: "chest and triceps workout" → returns similar past workouts
        """
        return await self.search_similar_entries(
            user_id=user_id,
            query_text=workout_description,
            source_type="workout",
            limit=limit,
            recency_weight=0.3
        )

    async def find_similar_activities(
        self,
        user_id: str,
        activity_description: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Find activities similar to a description.

        Example: "5 mile run" → returns similar past runs
        """
        return await self.search_similar_entries(
            user_id=user_id,
            query_text=activity_description,
            source_type="activity",
            limit=limit,
            recency_weight=0.4
        )

    async def get_recent_entries_by_type(
        self,
        user_id: str,
        source_type: SourceType,
        days: int = 7,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get recent entries of a specific type (without semantic search).

        Useful for getting latest meals, workouts, activities.
        """
        try:
            since_date = (datetime.utcnow() - timedelta(days=days)).isoformat()

            result = self.supabase.table("multimodal_embeddings").select(
                "id, source_type, source_id, content_text, metadata, data_type, storage_url, created_at"
            ).eq("user_id", user_id).eq(
                "source_type", source_type
            ).gte("created_at", since_date).order(
                "created_at", desc=True
            ).limit(limit).execute()

            return result.data if result.data else []

        except Exception as e:
            logger.error(f"[SemanticSearch] Get recent entries failed: {e}")
            return []

    async def get_personalized_context_bundle(
        self,
        user_id: str,
        current_entry_text: str,
        current_entry_type: str
    ) -> Dict[str, Any]:
        """
        Get comprehensive context bundle for AI recommendations.

        Returns relevant meals, workouts, activities, and notes based on current entry.

        Example use case: User logs a meal, AI coach gets similar past meals +
        recent workouts to provide personalized macro recommendations.
        """
        logger.info(f"[SemanticSearch] Building context bundle for {current_entry_type}")

        context = {
            "similar_entries": [],
            "recent_meals": [],
            "recent_workouts": [],
            "recent_activities": [],
            "summary": ""
        }

        try:
            # Get similar entries of same type
            context["similar_entries"] = await self.search_similar_entries(
                user_id=user_id,
                query_text=current_entry_text,
                source_type=current_entry_type if current_entry_type in ["meal", "workout", "activity"] else None,
                limit=3,
                recency_weight=0.3
            )

            # Get recent entries for broader context
            context["recent_meals"] = await self.get_recent_entries_by_type(
                user_id=user_id,
                source_type="meal",
                days=3,
                limit=5
            )

            context["recent_workouts"] = await self.get_recent_entries_by_type(
                user_id=user_id,
                source_type="workout",
                days=7,
                limit=3
            )

            context["recent_activities"] = await self.get_recent_entries_by_type(
                user_id=user_id,
                source_type="activity",
                days=7,
                limit=3
            )

            # Build summary
            summary_parts = [
                f"Similar {current_entry_type}s: {len(context['similar_entries'])}",
                f"Recent meals (3 days): {len(context['recent_meals'])}",
                f"Recent workouts (7 days): {len(context['recent_workouts'])}",
                f"Recent activities (7 days): {len(context['recent_activities'])}"
            ]
            context["summary"] = " | ".join(summary_parts)

            logger.info(f"[SemanticSearch] Context bundle: {context['summary']}")
            return context

        except Exception as e:
            logger.error(f"[SemanticSearch] Context bundle failed: {e}")
            return context


# Global instance
_semantic_search_service: Optional[SemanticSearchService] = None


def get_semantic_search_service() -> SemanticSearchService:
    """Get the global SemanticSearchService instance."""
    global _semantic_search_service
    if _semantic_search_service is None:
        _semantic_search_service = SemanticSearchService()
    return _semantic_search_service
