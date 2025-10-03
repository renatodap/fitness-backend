"""
Health Check Endpoints
"""

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app.services.supabase_service import get_supabase_service

router = APIRouter()


@router.get("/")
async def health_check():
    """Detailed health check."""
    db_healthy = get_supabase_service().health_check()

    return JSONResponse(
        status_code=200 if db_healthy else 503,
        content={
            "status": "healthy" if db_healthy else "degraded",
            "checks": {
                "database": "pass" if db_healthy else "fail",
            },
        },
    )


@router.get("/ready")
async def readiness_check():
    """Readiness check for load balancers."""
    return {"status": "ready"}


@router.get("/live")
async def liveness_check():
    """Liveness check for orchestrators."""
    return {"status": "alive"}
