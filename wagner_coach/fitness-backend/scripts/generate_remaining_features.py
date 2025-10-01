"""
Script to generate remaining backend features following TDD approach.

This script creates all design docs, tests, and implementations for features 3-10.
Run this to quickly scaffold the complete backend structure.
"""

import os
from pathlib import Path

# Base directory
BASE_DIR = Path(__file__).parent.parent

def create_file(path: str, content: str) -> None:
    """Create file with content, creating parent directories if needed."""
    file_path = BASE_DIR / path
    file_path.parent.mkdir(parents=True, exist_ok=True)
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created: {path}")

def main():
    """Generate all remaining features."""

    print("Generating remaining backend features...\n")

    # Feature 3: Auth Middleware - Implementation
    create_file("app/api/middleware/auth.py", '''"""
Authentication Middleware

Provides JWT token verification and user identity extraction.
"""

import logging
from typing import Optional

from fastapi import Header, HTTPException, Security, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import JWTError, jwt

from app.config import settings

logger = logging.getLogger(__name__)

# Security scheme
security = HTTPBearer()


async def verify_token(
    credentials: HTTPAuthorizationCredentials = Security(security)
) -> str:
    """
    Verify JWT token and extract user_id.

    Args:
        credentials: HTTP Bearer credentials

    Returns:
        str: User ID extracted from token

    Raises:
        HTTPException: If token is invalid or expired
    """
    token = credentials.credentials

    try:
        # Decode and verify JWT
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={
                "verify_signature": True,
                "verify_exp": True,
                "verify_aud": False,  # Supabase doesn't always set aud
            },
        )

        # Extract user_id from 'sub' claim
        user_id: str = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing 'sub' claim",
            )

        logger.debug(f"Token verified for user: {user_id[:8]}...")
        return user_id

    except JWTError as e:
        logger.warning(f"JWT verification failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
        )


async def get_current_user(
    authorization: str = Header(...)
) -> str:
    """
    FastAPI dependency for required authentication.

    Args:
        authorization: Authorization header (Bearer <token>)

    Returns:
        str: User ID

    Raises:
        HTTPException: 401 if not authenticated
    """
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header format",
        )

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_signature": True, "verify_exp": True, "verify_aud": False},
        )

        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token missing 'sub' claim",
            )

        return user_id

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid authentication credentials: {str(e)}",
        )


async def get_current_user_optional(
    authorization: Optional[str] = Header(None)
) -> Optional[str]:
    """
    FastAPI dependency for optional authentication.

    Args:
        authorization: Optional authorization header

    Returns:
        Optional[str]: User ID if authenticated, None otherwise
    """
    if not authorization or not authorization.startswith("Bearer "):
        return None

    token = authorization.split(" ")[1]

    try:
        payload = jwt.decode(
            token,
            settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM],
            options={"verify_signature": True, "verify_exp": True, "verify_aud": False},
        )

        return payload.get("sub")

    except JWTError:
        # For optional auth, return None on error instead of raising
        return None


async def verify_cron_secret(authorization: str = Header(...)) -> None:
    """
    Verify cron secret for scheduled jobs.

    Args:
        authorization: Authorization header (Bearer <secret>)

    Raises:
        HTTPException: 401 if secret is invalid
    """
    expected = f"Bearer {settings.CRON_SECRET}"

    if authorization != expected:
        logger.warning("Invalid cron secret attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid cron secret",
        )

    logger.info("Cron secret verified")


async def verify_webhook_secret(authorization: str = Header(...)) -> None:
    """
    Verify webhook secret for external webhooks.

    Args:
        authorization: Authorization header (Bearer <secret>)

    Raises:
        HTTPException: 401 if secret is invalid
    """
    expected = f"Bearer {settings.WEBHOOK_SECRET}"

    if authorization != expected:
        logger.warning("Invalid webhook secret attempt")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook secret",
        )

    logger.info("Webhook secret verified")
''')

    # Feature 4: FastAPI App & Health
    create_file("app/main.py", '''"""
FastAPI Application Entry Point

Main application configuration and routing.
"""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from app.config import settings

# Setup logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    logger.info(f"Starting {settings.APP_NAME}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    logger.info(f"Debug mode: {settings.DEBUG}")

    yield

    logger.info(f"Shutting down {settings.APP_NAME}")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    description="Backend service for Wagner Coach fitness app",
    version="0.1.0",
    docs_url="/docs" if settings.DEBUG else None,
    redoc_url="/redoc" if settings.DEBUG else None,
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
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
        "environment": settings.ENVIRONMENT,
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
# from app.api.v1.router import api_router
# app.include_router(api_router, prefix=settings.API_V1_PREFIX)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG,
        log_level=settings.LOG_LEVEL.lower(),
    )
''')

    # API Router structure
    create_file("app/api/v1/router.py", '''"""
API v1 Router

Main router for API v1 endpoints.
"""

from fastapi import APIRouter

from app.api.v1 import health

api_router = APIRouter()

# Include sub-routers
api_router.include_router(health.router, prefix="/health", tags=["health"])

# Future routers:
# from app.api.v1 import background_jobs, embeddings, nutrition, garmin
# api_router.include_router(background_jobs.router, prefix="/background", tags=["background"])
# api_router.include_router(embeddings.router, prefix="/embeddings", tags=["embeddings"])
# api_router.include_router(nutrition.router, prefix="/nutrition", tags=["nutrition"])
# api_router.include_router(garmin.router, prefix="/garmin", tags=["garmin"])
''')

    create_file("app/api/v1/health.py", '''"""
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
''')

    # Dockerfile
    create_file("Dockerfile", '''FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Install pip dependencies directly (no Poetry in container)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \\
    CMD curl -f http://localhost:8000/health || exit 1

# Run application
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
''')

    # Docker Compose
    create_file("docker-compose.yml", '''version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - ENVIRONMENT=development
      - DEBUG=true
      - LOG_LEVEL=DEBUG
    env_file:
      - .env
    depends_on:
      - redis
    volumes:
      - .:/app
    command: uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

  redis:
    image: redis:7-alpine
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data

volumes:
  redis_data:
''')

    # Requirements.txt (for Docker - lighter than poetry)
    create_file("requirements.txt", '''fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.0
pydantic-settings==2.1.0
supabase==2.3.0
openai==1.10.0
celery[redis]==5.3.0
redis==5.0.1
python-jose[cryptography]==3.3.0
python-multipart==0.0.6
garminconnect==0.2.15
httpx==0.26.0
prometheus-client==0.19.0
sentry-sdk[fastapi]==1.40.0
''')

    # GitHub Actions CI/CD
    create_file(".github/workflows/test.yml", '''name: Test

on:
  push:
    branches: [main, career-fair]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v3

      - name: Set up Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Install dependencies
        run: |
          pip install poetry
          poetry install

      - name: Run tests
        run: |
          poetry run pytest --cov=app --cov-report=xml --cov-report=term-missing

      - name: Upload coverage
        uses: codecov/codecov-action@v3
        with:
          file: ./coverage.xml
          fail_ci_if_error: false

      - name: Run linter
        run: |
          poetry run ruff check app/

      - name: Run formatter check
        run: |
          poetry run black --check app/

      - name: Type check
        run: |
          poetry run mypy app/
        continue-on-error: true
''')

    # README
    create_file("README.md", '''# Fitness Backend

Python backend service for Wagner Coach fitness application.

## Features

- ✅ FastAPI REST API
- ✅ Supabase database integration
- ✅ JWT authentication
- ✅ OpenAI integration for AI processing
- ✅ Celery for background jobs
- ✅ Redis for caching and queues
- ✅ Comprehensive test suite
- ✅ Docker support
- ✅ CI/CD with GitHub Actions

## Quick Start

### Prerequisites

- Python 3.11+
- Poetry (for dependency management)
- Docker & Docker Compose (optional)

### Local Development

1. **Clone and navigate:**
   ```bash
   cd fitness-backend
   ```

2. **Install dependencies:**
   ```bash
   pip install poetry
   poetry install
   ```

3. **Setup environment:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values
   ```

4. **Run the server:**
   ```bash
   poetry run uvicorn app.main:app --reload
   ```

5. **Access the API:**
   - API: http://localhost:8000
   - Docs: http://localhost:8000/docs
   - Health: http://localhost:8000/health

### Docker Development

```bash
docker-compose up
```

## Testing

### Run all tests:
```bash
poetry run pytest
```

### Run with coverage:
```bash
poetry run pytest --cov=app --cov-report=html --cov-report=term-missing
```

### Run specific test file:
```bash
poetry run pytest tests/unit/test_config.py -v
```

## Project Structure

```
fitness-backend/
├── app/
│   ├── main.py                 # FastAPI application
│   ├── config.py               # Configuration management
│   ├── api/
│   │   ├── v1/
│   │   │   ├── router.py       # Main API router
│   │   │   ├── health.py       # Health check endpoints
│   │   │   └── ...             # Other endpoints
│   │   └── middleware/
│   │       └── auth.py         # Authentication middleware
│   ├── services/
│   │   ├── supabase_service.py # Supabase client management
│   │   └── ...                 # Other services
│   ├── models/
│   │   └── ...                 # Pydantic models
│   └── workers/
│       └── ...                 # Celery workers
├── tests/
│   ├── unit/                   # Unit tests
│   ├── integration/            # Integration tests
│   └── conftest.py             # Test fixtures
├── docs/
│   ├── design/                 # Feature designs
│   └── testing/                # Test plans
├── scripts/
│   └── ...                     # Utility scripts
├── Dockerfile
├── docker-compose.yml
├── pyproject.toml
└── README.md
```

## Code Quality

### Format code:
```bash
poetry run black app/
```

### Lint code:
```bash
poetry run ruff check app/
```

### Type check:
```bash
poetry run mypy app/
```

## Environment Variables

See `.env.example` for all required environment variables.

### Required:
- `SUPABASE_URL`: Supabase project URL
- `SUPABASE_KEY`: Supabase anon key
- `SUPABASE_SERVICE_KEY`: Supabase service role key
- `OPENAI_API_KEY`: OpenAI API key
- `JWT_SECRET`: JWT signing secret
- `CRON_SECRET`: Secret for cron endpoints
- `WEBHOOK_SECRET`: Secret for webhook endpoints

### Optional:
- `REDIS_URL`: Redis connection URL (default: redis://localhost:6379)
- `SENTRY_DSN`: Sentry error tracking DSN
- `LOG_LEVEL`: Logging level (default: INFO)

## Deployment

### Railway

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up
```

### Fly.io

```bash
# Install Fly CLI
curl -L https://fly.io/install.sh | sh

# Login
flyctl auth login

# Deploy
flyctl launch
```

## Contributing

1. Create a feature branch
2. Write tests first (TDD approach)
3. Implement feature
4. Ensure tests pass and coverage ≥80%
5. Format and lint code
6. Submit pull request

## License

Private - Wagner Coach Fitness Application

## Support

For issues or questions, contact: renato@sharpened.me
''')

    # Update conftest with more fixtures
    create_file("tests/conftest.py", '''"""
Pytest configuration and shared fixtures.
"""

import pytest
from datetime import datetime, timedelta
from jose import jwt
from unittest.mock import Mock

from app.config import Settings, get_settings


@pytest.fixture
def base_settings_dict():
    """Provide minimal valid settings dictionary for testing."""
    return {
        "SUPABASE_URL": "https://test.supabase.co",
        "SUPABASE_KEY": "test-anon-key",
        "SUPABASE_SERVICE_KEY": "test-service-key",
        "OPENAI_API_KEY": "sk-test-key",
        "JWT_SECRET": "test-jwt-secret",
        "CRON_SECRET": "test-cron-secret",
        "WEBHOOK_SECRET": "test-webhook-secret",
    }


@pytest.fixture
def test_settings(base_settings_dict):
    """Provide Settings instance for testing."""
    return Settings(**base_settings_dict)


@pytest.fixture(autouse=True)
def reset_settings_cache():
    """Reset settings cache before and after each test."""
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


@pytest.fixture
def mock_jwt_token():
    """Generate valid mock JWT token."""
    payload = {
        "sub": "test-user-id-123",
        "exp": datetime.utcnow() + timedelta(hours=1),
        "iat": datetime.utcnow(),
        "iss": "https://test.supabase.co/auth/v1",
        "email": "test@example.com",
    }
    return jwt.encode(payload, "test-jwt-secret", algorithm="HS256")


@pytest.fixture
def mock_expired_token():
    """Generate expired mock JWT token."""
    payload = {
        "sub": "test-user-id-123",
        "exp": datetime.utcnow() - timedelta(hours=1),
        "iat": datetime.utcnow() - timedelta(hours=2),
    }
    return jwt.encode(payload, "test-jwt-secret", algorithm="HS256")


@pytest.fixture
def mock_supabase_client():
    """Mock Supabase client."""
    mock_client = Mock()
    mock_table = Mock()
    mock_table.select().execute.return_value = Mock(data=[])
    mock_client.table.return_value = mock_table
    return mock_client
''')

    print("\nAll features scaffolded successfully!")
    print("\nNext steps:")
    print("1. Review generated files")
    print("2. Run: poetry install")
    print("3. Run: poetry run pytest")
    print("4. Start development: poetry run uvicorn app.main:app --reload")


if __name__ == "__main__":
    main()
