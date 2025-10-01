"""
API v1 Router

Main router for API v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1 import (
    health,
    background_jobs,
    embeddings,
    ai,
    nutrition,
    integrations,
    coach
)

api_router = APIRouter()

# Include all sub-routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(background_jobs.router, prefix="/background", tags=["background"])
api_router.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])
api_router.include_router(ai.router, prefix="/ai", tags=["ai"])
api_router.include_router(nutrition.router, prefix="/nutrition", tags=["nutrition"])
api_router.include_router(integrations.router, prefix="/integrations", tags=["integrations"])
api_router.include_router(coach.router, prefix="/coach", tags=["coach"])
