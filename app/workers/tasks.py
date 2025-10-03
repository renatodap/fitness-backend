"""
Celery Task Definitions
"""

import logging
from celery import shared_task

logger = logging.getLogger(__name__)


@shared_task(name="app.workers.tasks.generate_summaries_task")
def generate_summaries_task():
    """
    Background task for daily summarization.

    Runs via Celery Beat schedule.
    """
    try:
        from app.services.summarization_service import SummarizationService
        import asyncio

        service = SummarizationService()

        # Run async function in sync context
        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(service.generate_all_summaries())

        logger.info(f"Summarization task complete: {result}")
        return result

    except Exception as e:
        logger.error(f"Summarization task failed: {e}")
        raise


@shared_task(name="app.workers.tasks.process_embeddings_task")
def process_embeddings_task():
    """
    Background task for processing embedding queue.

    Runs every 15 minutes via Celery Beat.
    """
    try:
        from app.services.embedding_service import EmbeddingService
        import asyncio

        service = EmbeddingService()

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(service.process_queue(limit=100))

        logger.info(f"Embedding processing complete: {result}")
        return result

    except Exception as e:
        logger.error(f"Embedding processing task failed: {e}")
        raise


@shared_task(name="app.workers.tasks.generate_embedding_async")
def generate_embedding_async(content: str, content_type: str, content_id: str, user_id: str):
    """
    Async task to generate single embedding.

    Can be called from API for background processing.
    """
    try:
        from app.services.embedding_service import EmbeddingService
        import asyncio

        service = EmbeddingService()

        loop = asyncio.get_event_loop()
        embedding_id = loop.run_until_complete(
            service.generate_and_store(user_id, content, content_type, content_id)
        )

        logger.info(f"Generated embedding: {embedding_id}")
        return {"success": True, "embedding_id": embedding_id}

    except Exception as e:
        logger.error(f"Embedding generation failed: {e}")
        raise
