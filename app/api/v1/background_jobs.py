"""
Background Job Endpoints
"""

from fastapi import APIRouter, Depends
from datetime import datetime

from app.api.middleware.auth import verify_cron_secret
from app.services.summarization_service import SummarizationService

router = APIRouter()


@router.post("/summarize")
async def run_summarization(_: None = Depends(verify_cron_secret)):
    """
    Run daily summarization for all users.

    Requires cron secret authentication.
    """
    service = SummarizationService()
    result = await service.generate_all_summaries()

    return {
        "success": True,
        "message": "Summarization complete",
        "results": result,
        "timestamp": datetime.now().isoformat(),
    }
