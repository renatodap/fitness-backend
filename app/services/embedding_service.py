"""
Embedding Service

Generates text embeddings using OpenAI for vector search.
"""

import logging
from typing import Any, Dict, List, Optional
from openai import AsyncOpenAI

from app.config import get_settings
from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


class EmbeddingService:
    """
    Service for generating and managing text embeddings.

    Uses OpenAI's text-embedding-3-small model to generate embeddings
    for semantic search and RAG applications.
    """

    def __init__(self):
        """Initialize with OpenAI and Supabase clients."""
        settings = get_settings()
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.supabase = get_service_client()
        self.model = "text-embedding-3-small"
        self.dimensions = 1536

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for text.

        Args:
            text: Text to embed

        Returns:
            List of floats representing the embedding vector

        Raises:
            ValueError: If text is empty
            Exception: If OpenAI API fails
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            response = await self.openai.embeddings.create(
                model=self.model,
                input=text,
                dimensions=self.dimensions
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"Failed to generate embedding: {e}")
            raise

    async def process_queue(self, limit: int = 50) -> Dict[str, Any]:
        """
        Process pending embedding queue items.

        Args:
            limit: Maximum number of items to process

        Returns:
            Dict with processing results
        """
        results = {"processed": 0, "failed": 0, "processedItems": [], "failedItems": []}

        try:
            # Get pending items via RPC
            response = self.supabase.rpc(
                "process_embedding_queue",
                {"p_limit": limit}
            ).execute()

            queue_items = response.data or []
            logger.info(f"Processing {len(queue_items)} embedding queue items")

            for item in queue_items:
                try:
                    # Generate embedding
                    embedding = await self.generate_embedding(item["content"])

                    # Store embedding
                    self.supabase.rpc(
                        "complete_embedding_generation",
                        {
                            "p_queue_id": item["queue_id"],
                            "p_embedding": embedding
                        }
                    ).execute()

                    results["processed"] += 1
                    results["processedItems"].append(item["queue_id"])

                except Exception as e:
                    logger.error(f"Error processing {item['queue_id']}: {e}")

                    # Mark as failed
                    self.supabase.rpc(
                        "fail_embedding_generation",
                        {
                            "p_queue_id": item["queue_id"],
                            "p_error_message": str(e)
                        }
                    ).execute()

                    results["failed"] += 1
                    results["failedItems"].append(item["queue_id"])

            logger.info(f"Embedding processing complete: {results}")
            return results

        except Exception as e:
            logger.error(f"Error in process_queue: {e}")
            raise

    async def generate_and_store(
        self,
        user_id: str,
        content: str,
        content_type: str,
        content_id: str
    ) -> str:
        """
        Generate embedding and store directly.

        Args:
            user_id: User UUID
            content: Text to embed
            content_type: Type of content (activity, workout, meal, etc.)
            content_id: ID of the source content

        Returns:
            Embedding ID

        Raises:
            ValueError: If required fields are missing
        """
        if not all([user_id, content, content_type, content_id]):
            raise ValueError("All fields are required")

        # Generate embedding
        embedding = await self.generate_embedding(content)

        # Store in database
        result = self.supabase.table("embeddings").insert({
            "user_id": user_id,
            "content": content,
            "content_type": content_type,
            "content_id": content_id,
            "embedding": embedding,
        }).execute()

        return result.data[0]["id"]

    async def search_similar(
        self,
        query: str,
        user_id: str,
        limit: int = 5,
        threshold: float = 0.7,
        source_types: Optional[List[str]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar content using vector similarity.

        Args:
            query: Query text
            user_id: User UUID to search within
            limit: Maximum number of results
            threshold: Minimum similarity threshold (0-1)
            source_types: Optional list of source types to filter by

        Returns:
            List of similar content with similarity scores
        """
        if not query:
            raise ValueError("Query cannot be empty")

        # Generate query embedding
        query_embedding = await self.generate_embedding(query)

        # Try new match_embeddings function first (Phase 1 migration)
        try:
            response = self.supabase.rpc(
                "match_embeddings",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": threshold,
                    "match_count": limit,
                    "filter_user_id": user_id,
                    "filter_source_types": source_types
                }
            ).execute()
            return response.data or []
        except Exception as e:
            # Fallback to old search_embeddings if new function doesn't exist yet
            logger.warning(f"match_embeddings not available, falling back: {e}")
            response = self.supabase.rpc(
                "search_embeddings",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": threshold,
                    "match_count": limit,
                    "p_user_id": user_id
                }
            ).execute()
            return response.data or []

    async def batch_generate(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors

        Raises:
            ValueError: If texts list is empty
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")

        try:
            response = await self.openai.embeddings.create(
                model=self.model,
                input=texts,
                dimensions=self.dimensions
            )
            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Failed to generate batch embeddings: {e}")
            raise

    async def create_embedding_with_metadata(
        self,
        user_id: str,
        content: str,
        source_type: str,
        source_id: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Create and store an embedding with metadata (Phase 1 schema).

        Args:
            user_id: User ID
            content: Text content to embed
            source_type: Type of source (workout, meal, activity, goal, profile, coach_message)
            source_id: Optional ID of source record
            metadata: Optional metadata dictionary

        Returns:
            Dictionary with embedding record

        Raises:
            Exception if creation fails
        """
        if not all([user_id, content, source_type]):
            raise ValueError("user_id, content, and source_type are required")

        try:
            # Generate embedding
            embedding_vector = await self.generate_embedding(content)

            # Insert into database with new schema
            result = self.supabase.table("embeddings").insert({
                "user_id": user_id,
                "content": content,
                "embedding": embedding_vector,
                "source_type": source_type,
                "source_id": source_id,
                "metadata": metadata or {}
            }).execute()

            logger.info(
                f"Created embedding for user {user_id}, "
                f"source_type={source_type}, source_id={source_id}"
            )

            return result.data[0] if result.data else {}

        except Exception as e:
            logger.error(f"Failed to create embedding with metadata: {str(e)}")
            raise

    async def embed_workout(
        self,
        user_id: str,
        workout_id: str,
        workout_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create embedding for a workout with formatted content.

        Args:
            user_id: User ID
            workout_id: Workout ID
            workout_data: Workout data dictionary

        Returns:
            Created embedding record
        """
        content = self._format_workout_for_embedding(workout_data)

        metadata = {
            "workout_name": workout_data.get("name"),
            "workout_type": workout_data.get("workout_type"),
            "date": workout_data.get("started_at"),
            "duration_minutes": workout_data.get("duration_minutes"),
        }

        return await self.create_embedding_with_metadata(
            user_id=user_id,
            content=content,
            source_type="workout",
            source_id=workout_id,
            metadata=metadata
        )

    async def embed_meal(
        self,
        user_id: str,
        meal_id: str,
        meal_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create embedding for a meal with formatted content.

        Args:
            user_id: User ID
            meal_id: Meal ID
            meal_data: Meal data dictionary

        Returns:
            Created embedding record
        """
        content = self._format_meal_for_embedding(meal_data)

        metadata = {
            "meal_name": meal_data.get("name"),
            "meal_type": meal_data.get("meal_type"),
            "date": meal_data.get("consumed_at"),
            "calories": meal_data.get("calories"),
            "protein_grams": meal_data.get("protein_grams"),
        }

        return await self.create_embedding_with_metadata(
            user_id=user_id,
            content=content,
            source_type="meal",
            source_id=meal_id,
            metadata=metadata
        )

    def _format_workout_for_embedding(self, workout_data: Dict[str, Any]) -> str:
        """Format workout data as text for embedding."""
        parts = []

        if name := workout_data.get("name"):
            parts.append(f"Workout: {name}")
        if workout_type := workout_data.get("workout_type"):
            parts.append(f"Type: {workout_type}")
        if date := workout_data.get("started_at"):
            parts.append(f"Date: {date}")
        if duration := workout_data.get("duration_minutes"):
            parts.append(f"Duration: {duration} minutes")

        if exercises := workout_data.get("exercises"):
            parts.append("Exercises:")
            for ex in exercises:
                ex_name = ex.get("exercise_name", "Unknown")
                sets = ex.get("sets", [])
                if sets:
                    set_info = ", ".join([
                        f"{s.get('reps')}x{s.get('weight')}{s.get('weight_unit', 'lbs')}"
                        for s in sets
                        if s.get('reps') and s.get('weight')
                    ])
                    parts.append(f"  - {ex_name}: {set_info}")
                else:
                    parts.append(f"  - {ex_name}")

        if notes := workout_data.get("notes"):
            parts.append(f"Notes: {notes}")
        if rpe := workout_data.get("perceived_exertion"):
            parts.append(f"Perceived Exertion: {rpe}/10")
        if energy := workout_data.get("energy_level"):
            parts.append(f"Energy Level: {energy}/10")

        return "\n".join(parts)

    def _format_meal_for_embedding(self, meal_data: Dict[str, Any]) -> str:
        """Format meal data as text for embedding."""
        parts = []

        if name := meal_data.get("name"):
            parts.append(f"Meal: {name}")
        if meal_type := meal_data.get("meal_type"):
            parts.append(f"Type: {meal_type}")
        if date := meal_data.get("consumed_at"):
            parts.append(f"Date: {date}")
        if calories := meal_data.get("calories"):
            parts.append(f"Calories: {calories}")

        macros = []
        if protein := meal_data.get("protein_grams"):
            macros.append(f"{protein}g protein")
        if carbs := meal_data.get("carbs_grams"):
            macros.append(f"{carbs}g carbs")
        if fat := meal_data.get("fat_grams"):
            macros.append(f"{fat}g fat")
        if macros:
            parts.append(f"Macros: {', '.join(macros)}")

        if foods := meal_data.get("foods"):
            parts.append("Foods:")
            for food in foods:
                food_name = food.get("food_name", "Unknown")
                quantity = food.get("quantity", "")
                unit = food.get("unit", "")
                parts.append(f"  - {food_name} ({quantity} {unit})")

        if notes := meal_data.get("notes"):
            parts.append(f"Notes: {notes}")

        return "\n".join(parts)
