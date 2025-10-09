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
    coach,
    programs,
    quick_entry,
    foods,
    meals,
    templates,
    activities,
    consultation,
    events,
    garmin,
    merge_requests,
    test_groq,
    debug
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
api_router.include_router(programs.router, prefix="/programs", tags=["programs"])
api_router.include_router(quick_entry.router, tags=["quick-entry"])  # No prefix, routes define their own
api_router.include_router(foods.router, tags=["foods"])  # Food search and database
api_router.include_router(meals.router, tags=["meals"])  # Meal logging CRUD
api_router.include_router(templates.router, tags=["templates"])  # Meal templates (prefix: /templates)
api_router.include_router(activities.router, tags=["activities"])  # Activity logging CRUD
api_router.include_router(consultation.router)  # Consultation endpoints (prefix defined in router)
api_router.include_router(events.router)  # Events & Calendar endpoints (prefix defined in router)
api_router.include_router(garmin.router)  # Garmin health integration (prefix: /garmin)
api_router.include_router(merge_requests.router, tags=["merge-requests"])  # Activity deduplication & merge requests
api_router.include_router(test_groq.router, tags=["test"])  # Test endpoints
api_router.include_router(debug.router, tags=["debug"])  # Debug endpoints (remove in production)
