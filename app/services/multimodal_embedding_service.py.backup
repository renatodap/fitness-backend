"""
Multimodal Embedding Service - REVOLUTIONARY VECTOR DATABASE

Generates embeddings for text, images, audio using FREE open-source models:
- Text: sentence-transformers (all-MiniLM-L6-v2) - 384 dimensions
- Images: OpenAI CLIP (ViT-B/32) - 512 dimensions
- Audio: Whisper transcription → text embedding

Stores in Supabase with pgvector for lightning-fast semantic search.
"""

import logging
import base64
import io
import uuid
from typing import List, Dict, Any, Optional, Union
from datetime import datetime

# Open-source ML models
from sentence_transformers import SentenceTransformer
from PIL import Image

# Note: torch/transformers removed to reduce dependencies
# Image embeddings now use OpenAI or are disabled

# Supabase
from app.services.supabase_service import get_service_client
from app.config import settings

logger = logging.getLogger(__name__)


class MultimodalEmbeddingService:
    """
    Revolutionary multimodal embedding service.

    Features:
    - FREE text embeddings (sentence-transformers)
    - FREE image embeddings (CLIP)
    - FREE audio transcription (Whisper) → text embedding
    - Unified vector storage in Supabase pgvector
    - Fast semantic search across ALL modalities
    """

    _instance = None
    _text_model = None
    _clip_model = None
    _clip_processor = None

    def __new__(cls):
        """Singleton pattern to avoid reloading models."""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        """Initialize models (lazy loading)."""
        if self._initialized:
            return

        self.supabase = get_service_client()
        self._initialized = True

        logger.info("🚀 Initializing MultimodalEmbeddingService...")

        # Text model dimensions
        self.text_dimensions = 384
        self.clip_dimensions = 512

        logger.info("✅ MultimodalEmbeddingService initialized (models will load on first use)")

    def _load_text_model(self):
        """Lazy load text embedding model."""
        if MultimodalEmbeddingService._text_model is None:
            logger.info("📝 Loading text embedding model (all-MiniLM-L6-v2)...")
            MultimodalEmbeddingService._text_model = SentenceTransformer('all-MiniLM-L6-v2')
            logger.info("✅ Text model loaded")
        return MultimodalEmbeddingService._text_model

    def _load_clip_model(self):
        """CLIP model disabled - use OpenAI for image embeddings instead."""
        raise NotImplementedError(
            "CLIP image embeddings disabled to reduce dependencies. "
            "Use OpenAI Vision API for image analysis instead."
        )

    # ========================================================================
    # EMBEDDING GENERATION
    # ========================================================================

    async def embed_text(self, text: str) -> List[float]:
        """
        Generate text embedding using sentence-transformers.

        Args:
            text: Text to embed

        Returns:
            384-dimensional embedding vector

        Raises:
            ValueError: If text is empty
        """
        if not text or not text.strip():
            raise ValueError("Text cannot be empty")

        try:
            model = self._load_text_model()
            embedding = model.encode(text, convert_to_tensor=False, normalize_embeddings=True)

            # Convert to list and ensure 384 dimensions
            embedding_list = embedding.tolist()

            if len(embedding_list) != 384:
                raise ValueError(f"Expected 384 dimensions, got {len(embedding_list)}")

            logger.debug(f"✅ Generated text embedding: {len(embedding_list)} dimensions")
            return embedding_list

        except Exception as e:
            logger.error(f"❌ Text embedding failed: {e}")
            raise

    async def embed_image(self, image_base64: str) -> List[float]:
        """
        Image embeddings disabled - use OpenAI Vision API instead.

        Args:
            image_base64: Base64-encoded image

        Returns:
            512-dimensional embedding vector

        Raises:
            NotImplementedError: CLIP disabled to reduce dependencies
        """
        raise NotImplementedError(
            "Image embeddings disabled to reduce dependencies (torch/transformers removed). "
            "Use OpenAI Vision API for image understanding instead of embeddings."
        )

    
    async def embed_text_with_clip(self, text: str) -> List[float]:
        """
        CLIP text embeddings disabled - use regular text embeddings instead.

        Args:
            text: Text to embed

        Returns:
            512-dimensional CLIP text embedding

        Raises:
            NotImplementedError: CLIP disabled to reduce dependencies
        """
        raise NotImplementedError(
            "CLIP text embeddings disabled. Use embed_text() for regular text embeddings instead."
        )

    
    async def batch_embed_text(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batch (faster).

        Args:
            texts: List of texts to embed

        Returns:
            List of 384-dimensional embeddings
        """
        if not texts:
            raise ValueError("Texts list cannot be empty")

        try:
            model = self._load_text_model()
            embeddings = model.encode(
                texts,
                convert_to_tensor=False,
                normalize_embeddings=True,
                batch_size=32
            )

            embeddings_list = [emb.tolist() for emb in embeddings]
            logger.debug(f"✅ Generated {len(embeddings_list)} text embeddings in batch")
            return embeddings_list

        except Exception as e:
            logger.error(f"❌ Batch text embedding failed: {e}")
            raise

    # ========================================================================
    # STORAGE
    # ========================================================================

    async def store_embedding(
        self,
        user_id: str,
        embedding: List[float],
        data_type: str,
        source_type: str,
        source_id: Optional[str] = None,
        content_text: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        storage_url: Optional[str] = None,
        storage_bucket: Optional[str] = None,
        file_name: Optional[str] = None,
        file_size_bytes: Optional[int] = None,
        mime_type: Optional[str] = None,
        confidence_score: Optional[float] = None,
        embedding_model: str = "all-MiniLM-L6-v2"
    ) -> str:
        """
        Store embedding in multimodal_embeddings table.

        Args:
            user_id: User UUID
            embedding: Embedding vector
            data_type: 'text', 'image', 'audio', 'video', 'pdf', 'structured', 'mixed'
            source_type: 'meal', 'workout', 'activity', 'goal', etc.
            source_id: UUID of source record (optional)
            content_text: Text content or transcription
            metadata: Additional metadata (JSONB)
            storage_url: Supabase Storage URL for files
            storage_bucket: Storage bucket name
            file_name: Original file name
            file_size_bytes: File size in bytes
            mime_type: MIME type
            confidence_score: Confidence in embedding quality (0-1)
            embedding_model: Model used for embedding

        Returns:
            Embedding UUID
        """
        try:
            # Prepare data
            data = {
                "user_id": user_id,
                "embedding": embedding,
                "data_type": data_type,
                "source_type": source_type,
                "source_id": source_id or str(uuid.uuid4()),
                "content_text": content_text,
                "metadata": metadata or {},
                "storage_url": storage_url,
                "storage_bucket": storage_bucket,
                "file_name": file_name,
                "file_size_bytes": file_size_bytes,
                "mime_type": mime_type,
                "confidence_score": confidence_score,
                "embedding_model": embedding_model,
                "embedding_dimensions": len(embedding),
                "processing_status": "completed"
            }

            # Insert into database
            result = self.supabase.table("multimodal_embeddings").insert(data).execute()

            embedding_id = result.data[0]["id"]

            logger.info(
                f"✅ Stored embedding: {embedding_id} | "
                f"user={user_id[:8]}... | type={data_type} | source={source_type}"
            )

            return embedding_id

        except Exception as e:
            logger.error(f"❌ Failed to store embedding: {e}")
            raise

    async def queue_embedding(
        self,
        user_id: str,
        data_type: str,
        source_type: str,
        source_id: str,
        content_text: Optional[str] = None,
        storage_url: Optional[str] = None,
        metadata: Optional[Dict] = None
    ) -> str:
        """
        Queue an embedding for background processing.

        Args:
            user_id: User UUID
            data_type: Type of data
            source_type: Source type
            source_id: Source ID
            content_text: Optional text content
            storage_url: Optional storage URL
            metadata: Optional metadata

        Returns:
            Queued embedding ID
        """
        try:
            result = self.supabase.rpc(
                "queue_embedding_processing",
                {
                    "p_user_id": user_id,
                    "p_data_type": data_type,
                    "p_source_type": source_type,
                    "p_source_id": source_id,
                    "p_content_text": content_text,
                    "p_storage_url": storage_url,
                    "p_metadata": metadata or {}
                }
            ).execute()

            embedding_id = result.data
            logger.info(f"📥 Queued embedding for processing: {embedding_id}")
            return embedding_id

        except Exception as e:
            logger.error(f"❌ Failed to queue embedding: {e}")
            raise

    # ========================================================================
    # SEARCH
    # ========================================================================

    async def search_similar(
        self,
        query_embedding: List[float],
        user_id: str,
        data_types: Optional[List[str]] = None,
        source_types: Optional[List[str]] = None,
        metadata_filter: Optional[Dict[str, Any]] = None,
        date_from: Optional[datetime] = None,
        date_to: Optional[datetime] = None,
        limit: int = 10,
        threshold: float = 0.5
    ) -> List[Dict[str, Any]]:
        """
        Search for similar embeddings using vector similarity.

        Args:
            query_embedding: Query embedding vector
            user_id: User UUID to search within
            data_types: Filter by data types (e.g., ['text', 'image'])
            source_types: Filter by source types (e.g., ['meal', 'workout'])
            metadata_filter: Filter by metadata (JSONB contains)
            date_from: Filter by date range (start)
            date_to: Filter by date range (end)
            limit: Maximum number of results
            threshold: Minimum similarity threshold (0-1)

        Returns:
            List of similar embeddings with similarity scores
        """
        try:
            response = self.supabase.rpc(
                "match_multimodal_embeddings",
                {
                    "query_embedding": query_embedding,
                    "match_threshold": threshold,
                    "match_count": limit,
                    "filter_user_id": user_id,
                    "filter_data_types": data_types,
                    "filter_source_types": source_types,
                    "filter_metadata": metadata_filter,
                    "filter_date_from": date_from.isoformat() if date_from else None,
                    "filter_date_to": date_to.isoformat() if date_to else None
                }
            ).execute()

            results = response.data or []

            logger.info(
                f"🔍 Search completed: {len(results)} results | "
                f"threshold={threshold} | user={user_id[:8]}..."
            )

            return results

        except Exception as e:
            logger.error(f"❌ Search failed: {e}")
            raise

    async def search_by_text(
        self,
        query_text: str,
        user_id: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search using a text query.

        Automatically generates text embedding and searches.
        """
        query_embedding = await self.embed_text(query_text)
        return await self.search_similar(
            query_embedding=query_embedding,
            user_id=user_id,
            **kwargs
        )

    async def search_by_image(
        self,
        image_base64: str,
        user_id: str,
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Search using an image query.

        Automatically generates image embedding and searches.
        """
        query_embedding = await self.embed_image(image_base64)
        return await self.search_similar(
            query_embedding=query_embedding,
            user_id=user_id,
            **kwargs
        )

    # ========================================================================
    # STATISTICS & UTILITIES
    # ========================================================================

    async def get_user_stats(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's embedding statistics.

        Returns:
            Statistics about user's embeddings (counts, storage, etc.)
        """
        try:
            response = self.supabase.rpc(
                "get_user_embedding_stats",
                {"p_user_id": user_id}
            ).execute()

            stats = response.data[0] if response.data else {}
            logger.debug(f"📊 User stats: {stats}")
            return stats

        except Exception as e:
            logger.error(f"❌ Failed to get user stats: {e}")
            raise

    async def delete_embedding(self, embedding_id: str, user_id: str) -> bool:
        """
        Delete an embedding.

        Args:
            embedding_id: Embedding UUID
            user_id: User UUID (for security)

        Returns:
            True if deleted
        """
        try:
            self.supabase.table("multimodal_embeddings").delete().eq(
                "id", embedding_id
            ).eq("user_id", user_id).execute()

            logger.info(f"🗑️ Deleted embedding: {embedding_id}")
            return True

        except Exception as e:
            logger.error(f"❌ Failed to delete embedding: {e}")
            raise


# Singleton instance
_multimodal_service: Optional[MultimodalEmbeddingService] = None

def get_multimodal_service() -> MultimodalEmbeddingService:
    """Get singleton instance of MultimodalEmbeddingService."""
    global _multimodal_service
    if _multimodal_service is None:
        _multimodal_service = MultimodalEmbeddingService()
    return _multimodal_service
