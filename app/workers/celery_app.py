"""
Celery Application Configuration
"""

from celery import Celery
from celery.schedules import crontab

from app.config import get_settings

# Get settings
_settings = get_settings()

# Create Celery app
celery_app = Celery(
    "fitness_backend",
    broker=_settings.CELERY_BROKER_URL,
    backend=_settings.CELERY_RESULT_BACKEND
)

# Configuration
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
    task_track_started=True,
    task_time_limit=300,  # 5 minutes
    worker_prefetch_multiplier=1,
)

# Periodic tasks
celery_app.conf.beat_schedule = {
    "generate-summaries-daily": {
        "task": "app.workers.tasks.generate_summaries_task",
        "schedule": crontab(hour=2, minute=0),  # 2 AM daily
    },
    "process-embeddings-queue": {
        "task": "app.workers.tasks.process_embeddings_task",
        "schedule": crontab(minute="*/15"),  # Every 15 minutes
    },
}

# Auto-discover tasks
celery_app.autodiscover_tasks(["app.workers"])
