"""
FastAPI Application Entry Point

Main application configuration and routing.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings, get_settings

# Ensure settings is initialized
if settings is None:
    _settings = get_settings()
else:
    _settings = settings

# Setup logging
logging.basicConfig(
    level=getattr(logging, _settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info(f"Starting {_settings.APP_NAME}")
    logger.info(f"Environment: {_settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {_settings.DEBUG}")
    logger.info(f"CORS Origins: {_settings.cors_origins_list}")
    logger.info(f"Allow All Origins: {_settings.ALLOW_ALL_ORIGINS}")

    yield

    logger.info(f"Shutting down {_settings.APP_NAME}")


# Create FastAPI app
app = FastAPI(
    title=_settings.APP_NAME,
    description="Backend service for Wagner Coach fitness app",
    version="0.1.0",
    docs_url="/docs" if _settings.DEBUG else None,
    redoc_url="/redoc" if _settings.DEBUG else None,
    lifespan=lifespan,
)

# CORS middleware
if _settings.ALLOW_ALL_ORIGINS:
    # WARNING: This is a security risk in production!
    # Only use during development or with proper IP restrictions
    logger.warning("⚠️  ALLOW_ALL_ORIGINS is enabled - allowing all origins (NOT for production!)")
    logger.warning("⚠️  Set ALLOW_ALL_ORIGINS=false before deploying to production!")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
else:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=_settings.cors_origins_list,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Fitness Backend API",
        "version": "0.1.0",
        "status": "healthy",
        "environment": _settings.ENVIRONMENT,
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    from app.services.supabase_service import get_supabase_service

    # Check database connection
    db_healthy = get_supabase_service().health_check()

    status_code = 200 if db_healthy else 503

    return JSONResponse(
        status_code=status_code,
        content={
            "status": "healthy" if db_healthy else "unhealthy",
            "version": "0.1.0",
            "services": {
                "database": "connected" if db_healthy else "disconnected",
            },
        },
    )


# Import and include routers
from app.api.v1.router import api_router
app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
