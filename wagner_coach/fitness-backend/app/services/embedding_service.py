"""
Embedding Service

Generates text embeddings using OpenAI for vector search.
"""

import logging
from typing import Any, Dict, List, Optional
from openai import AsyncOpenAI

from app.config import settings
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
        threshold: float = 0.7
    ) -> List[Dict[str, Any]]:
        """
        Search for similar content using vector similarity.

        Args:
            query: Query text
            user_id: User UUID to search within
            limit: Maximum number of results
            threshold: Minimum similarity threshold (0-1)

        Returns:
            List of similar content with similarity scores
        """
        if not query:
            raise ValueError("Query cannot be empty")

        # Generate query embedding
        query_embedding = await self.generate_embedding(query)

        # Search using RPC function
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
