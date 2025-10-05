# Production-Level Development Standards - Wagner Coach Backend

This document defines the mandatory standards for all production-level code in the Wagner Coach backend API. Claude Code must follow these standards for every feature, endpoint, and deployment.

---

## Core Principle
**Production-level means the code is ready to be used by real users, withstand scrutiny from other developers, pass legal requirements, and operate reliably at scale with efficient AI API costs.**

---

## 1. Development Process (TDD + API Verification)

All features **MUST** follow this 7-step sequence:

### Step 1: Feature Design
- Create `docs/design/{feature}.md` with:
  - User stories
  - API contracts (request/response schemas)
  - Database schema changes
  - AI model selection & cost estimation
  - Error scenarios
  - Rate limiting requirements

### Step 2: Test Design
- Create `docs/testing/{feature}_test.md` with:
  - Test scenarios (happy path, edge cases, errors)
  - Expected inputs/outputs
  - Mock data structures
  - Coverage targets (≥80%)
  - Load testing scenarios for AI endpoints

### Step 3: Code Design
- Define Pydantic models first
- Create database migrations (if needed)
- Plan service layer structure
- Define error classes
- Select AI models (cost vs quality)

### Step 4: Test Implementation
- Write tests **BEFORE** implementation
- Unit tests for services & utilities
- Integration tests for API endpoints
- Database tests with test fixtures
- Mock external APIs (OpenAI, Groq, Supabase)

### Step 5: Feature Implementation
- Implement until all tests pass
- Follow code quality standards (Section 2)
- Handle all error cases gracefully
- Add structured logging
- Implement rate limiting

### Step 6: Validation
- Verify ≥80% code coverage
- Run all linters (ruff, black, mypy)
- Manual testing with Postman/curl
- Load testing for AI endpoints
- Cost analysis for AI calls

### Step 7: API Verification (MANDATORY)
Every endpoint must be production-ready:

#### 7a. Request Validation
- [ ] All inputs validated with Pydantic
- [ ] Required fields enforced
- [ ] Data types strictly checked
- [ ] Input sanitization applied

#### 7b. Authentication & Authorization
- [ ] JWT validation working
- [ ] User context extracted correctly
- [ ] Row-level security enforced
- [ ] Service role key usage documented

#### 7c. Error Responses
- [ ] User-friendly error messages
- [ ] Proper HTTP status codes (200, 201, 400, 401, 403, 404, 500)
- [ ] Structured error format ({"error": "message", "details": {}})
- [ ] No internal details leaked to users

#### 7d. Response Format
- [ ] Consistent JSON structure
- [ ] Datetime in ISO 8601 format
- [ ] Pagination for list endpoints
- [ ] Null handling documented

#### 7e. Performance & Monitoring
- [ ] Response time <500ms (non-AI endpoints)
- [ ] AI endpoints have streaming or progress updates
- [ ] Logging with context (user_id, request_id)
- [ ] Cost tracking for AI calls

---

## 2. Code Quality Standards

### Python Best Practices
```python
# ✅ REQUIRED
- Python 3.11+
- Type hints on all functions
- Docstrings for all public functions (Google style)
- Pydantic models for all data structures
- Explicit error handling with custom exceptions
- No bare except clauses

# ❌ FORBIDDEN
- Any type hints (use specific types)
- Mutable default arguments
- Global state (use dependency injection)
- Hardcoded secrets
- print() statements (use logging)
```

### File Structure
```
wagner-coach-backend/
├── app/
│   ├── main.py                    # FastAPI app initialization
│   ├── config.py                  # Configuration & env vars
│   ├── api/
│   │   ├── v1/
│   │   │   ├── router.py          # Main router
│   │   │   ├── coach.py           # Coach chat endpoints
│   │   │   ├── programs.py        # AI program generation
│   │   │   ├── quick_entry.py     # Multimodal input processing
│   │   │   ├── embeddings.py      # Vector search
│   │   │   ├── integrations.py    # Strava/Garmin
│   │   │   └── health.py          # Health checks
│   │   └── middleware/
│   │       ├── auth.py            # JWT authentication
│   │       ├── rate_limit.py      # Rate limiting
│   │       └── logging.py         # Request logging
│   ├── services/
│   │   ├── supabase_service.py    # Database client
│   │   ├── coach_service.py       # AI coach logic
│   │   ├── context_builder.py     # RAG retrieval
│   │   ├── quick_entry_service.py # Multimodal processing
│   │   ├── program_service.py     # Program generation
│   │   ├── dual_model_router.py   # AI model routing
│   │   ├── multimodal_embedding_service.py  # Vector embeddings
│   │   ├── meal_parser_service.py # Natural language parsing
│   │   └── garmin_service.py      # Garmin integration
│   ├── models/
│   │   ├── requests/              # Request Pydantic models
│   │   ├── responses/             # Response Pydantic models
│   │   └── database/              # Database models
│   ├── core/
│   │   ├── exceptions.py          # Custom exceptions
│   │   ├── security.py            # JWT & auth utilities
│   │   └── logging.py             # Logging configuration
│   └── workers/
│       └── celery_app.py          # Background tasks
├── migrations/                    # SQL migrations
├── tests/
│   ├── unit/                      # Unit tests
│   ├── integration/               # Integration tests
│   └── conftest.py                # Pytest fixtures
├── docs/
│   ├── design/                    # Feature designs
│   ├── testing/                   # Test plans
│   └── api/                       # API documentation
├── scripts/                       # Utility scripts
├── pyproject.toml                 # Poetry dependencies
├── pytest.ini                     # Pytest configuration
├── .env.example                   # Environment variables template
└── README.md
```

### Naming Conventions
- **Files**: `snake_case.py`
- **Classes**: `PascalCase`
- **Functions**: `snake_case`
- **Constants**: `UPPER_SNAKE_CASE`
- **Private methods**: `_leading_underscore`
- **Pydantic models**: `PascalCase` (e.g., `CreateMealRequest`, `CoachResponse`)

### Code Organization
```python
# Module structure (top to bottom)
1. Module docstring
2. Imports (stdlib, third-party, local)
3. Constants
4. Type definitions
5. Pydantic models (if small)
6. Functions/classes
7. Main execution block (if applicable)

# Example:
"""
Coach service for AI-powered fitness & nutrition coaching.

This module handles:
- Chat message processing with RAG
- Context retrieval from user data
- Streaming responses
- Cost-optimized model routing
"""
from typing import AsyncGenerator, Optional
from datetime import datetime

from fastapi import HTTPException
from anthropic import AsyncAnthropic
import structlog

from app.models.requests import ChatRequest
from app.models.responses import ChatResponse
from app.services.context_builder import build_context

logger = structlog.get_logger()

MAX_CONTEXT_TOKENS = 4000
CHAT_RATE_LIMIT = 100  # messages per day

class CoachService:
    """AI coach service with RAG and streaming support."""

    def __init__(self, supabase_client, anthropic_client: AsyncAnthropic):
        self.supabase = supabase_client
        self.anthropic = anthropic_client

    async def chat(
        self,
        user_id: str,
        message: str,
        conversation_type: str = "general"
    ) -> AsyncGenerator[str, None]:
        """
        Process chat message with RAG context and stream response.

        Args:
            user_id: User's unique identifier
            message: User's chat message
            conversation_type: Type of conversation (general, nutrition, training)

        Yields:
            str: Chunks of AI response

        Raises:
            HTTPException: If rate limit exceeded or API fails
        """
        # Implementation
```

---

## 3. Security Standards

### Environment Variables
```python
# ✅ REQUIRED
from pydantic_settings import BaseSettings
from pydantic import Field, validator

class Settings(BaseSettings):
    # Supabase
    SUPABASE_URL: str = Field(..., env="SUPABASE_URL")
    SUPABASE_KEY: str = Field(..., env="SUPABASE_KEY")
    SUPABASE_SERVICE_KEY: str = Field(..., env="SUPABASE_SERVICE_KEY")

    # AI APIs
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: str = Field(..., env="ANTHROPIC_API_KEY")
    GROQ_API_KEY: str = Field(..., env="GROQ_API_KEY")
    OPENROUTER_API_KEY: str = Field(..., env="OPENROUTER_API_KEY")

    # Security
    JWT_SECRET: str = Field(..., env="JWT_SECRET")
    CRON_SECRET: str = Field(..., env="CRON_SECRET")
    WEBHOOK_SECRET: str = Field(..., env="WEBHOOK_SECRET")

    # Optional
    REDIS_URL: str = Field("redis://localhost:6379", env="REDIS_URL")
    SENTRY_DSN: Optional[str] = Field(None, env="SENTRY_DSN")
    LOG_LEVEL: str = Field("INFO", env="LOG_LEVEL")

    @validator("JWT_SECRET")
    def validate_jwt_secret(cls, v):
        if len(v) < 32:
            raise ValueError("JWT_SECRET must be at least 32 characters")
        return v

    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
```

### API Security
```python
# ✅ REQUIRED
- JWT authentication on all protected endpoints
- Rate limiting (100 chat msgs/day, 50 program generations/month)
- Input validation with Pydantic (prevent injection)
- Sanitize user inputs (especially URLs, file uploads)
- CORS properly configured
- Security headers (helmet equivalent in FastAPI)
- Row-level security in Supabase queries

# Example auth dependency:
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> dict:
    """Extract and validate JWT token."""
    try:
        token = credentials.credentials
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub")

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication token"
            )

        return {"user_id": user_id, "email": payload.get("email")}
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired"
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

### Data Handling
- Never log sensitive data (API keys, JWT tokens, passwords)
- Sanitize error messages before returning to clients
- Use HTTPS only in production
- Validate file uploads (size, type, content)
- Implement rate limiting on all AI endpoints
- Use Supabase RLS policies for all queries
- Hash sensitive data (use bcrypt for passwords)

---

## 4. AI API Cost Optimization

### Cost-Aware Model Routing

Wagner Coach uses a **dual-API strategy** with FREE open-source models:

```python
# Model selection strategy (lowest cost to highest quality)

AI_ROUTING = {
    # FREE Models (Hugging Face, local)
    "embeddings_text": "sentence-transformers/all-MiniLM-L6-v2",  # FREE
    "embeddings_image": "openai/clip-vit-base-patch32",  # FREE
    "voice_transcription": "openai/whisper-tiny",  # FREE

    # Simple tasks: Groq ($0.05-0.10/M tokens) or DeepSeek ($0.14/M)
    "quick_entry_text": "groq/llama-3.3-70b-versatile",
    "meal_parsing": "deepseek/deepseek-chat",
    "tag_extraction": "groq/llama-3.3-70b-versatile",

    # Medium tasks: OpenRouter ($0.50-1.00/M tokens)
    "quick_entry_image": "meta-llama/llama-4-scout",
    "workout_recommendations": "openrouter/meta-llama/llama-3.1-70b",

    # Complex tasks: Claude ($3-15/M tokens)
    "coach_chat": "anthropic/claude-3-5-sonnet-20241022",
    "program_generation": "anthropic/claude-3-5-sonnet-20241022",
    "weekly_analysis": "anthropic/claude-3-5-sonnet-20241022",
}

# Target costs per user per month
TARGET_COSTS = {
    "embeddings": 0.00,  # FREE local models
    "quick_entry": 0.05,  # Groq/DeepSeek
    "coach_chat": 0.30,   # Claude with caching
    "programs": 0.15,     # Claude (infrequent)
    "total": 0.50         # $0.50/user/month
}
```

### Cost Monitoring
```python
import structlog

logger = structlog.get_logger()

async def log_api_call(
    provider: str,
    model: str,
    tokens_in: int,
    tokens_out: int,
    cost: float,
    user_id: str,
    endpoint: str
):
    """Log all AI API calls for cost tracking."""
    logger.info(
        "ai_api_call",
        provider=provider,
        model=model,
        tokens_in=tokens_in,
        tokens_out=tokens_out,
        cost=cost,
        user_id=user_id,
        endpoint=endpoint,
        timestamp=datetime.utcnow().isoformat()
    )

    # Store in database for analytics
    await supabase.table("api_usage_logs").insert({
        "user_id": user_id,
        "provider": provider,
        "model": model,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "cost": cost,
        "endpoint": endpoint,
        "created_at": datetime.utcnow().isoformat()
    }).execute()
```

---

## 5. Database Best Practices

### Supabase Patterns
```python
# ✅ REQUIRED
- Use async Supabase client
- Always filter by user_id (RLS)
- Use select() with specific columns (not *)
- Handle errors gracefully
- Use transactions for multi-table operations
- Leverage pgvector for embeddings

# Example service method:
async def get_user_meals(
    self,
    user_id: str,
    start_date: str,
    end_date: str,
    limit: int = 50
) -> list[dict]:
    """
    Retrieve user's meal logs with filtering.

    Args:
        user_id: User's unique identifier
        start_date: Start date (ISO format)
        end_date: End date (ISO format)
        limit: Maximum number of results

    Returns:
        List of meal log dictionaries

    Raises:
        HTTPException: If database query fails
    """
    try:
        response = await self.supabase.table("meal_logs") \
            .select("id, logged_at, meal_type, calories, protein, carbs, fats, foods") \
            .eq("user_id", user_id) \
            .gte("logged_at", start_date) \
            .lte("logged_at", end_date) \
            .order("logged_at", desc=True) \
            .limit(limit) \
            .execute()

        return response.data
    except Exception as e:
        logger.error("Failed to fetch meal logs", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve meal history"
        )
```

### Migrations
```sql
-- All migrations must:
-- 1. Be reversible (include DOWN migration)
-- 2. Have RLS policies
-- 3. Have indexes on foreign keys
-- 4. Document purpose and changes

-- Example migration: migrations/006_add_user_preferences.sql

-- UP Migration
CREATE TABLE IF NOT EXISTS user_preferences (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    training_days_per_week INTEGER DEFAULT 3,
    dietary_preference TEXT DEFAULT 'none',
    equipment_access TEXT[] DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- RLS Policies
ALTER TABLE user_preferences ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own preferences"
ON user_preferences FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own preferences"
ON user_preferences FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own preferences"
ON user_preferences FOR UPDATE
USING (auth.uid() = user_id);

-- Indexes
CREATE INDEX idx_user_preferences_user_id ON user_preferences(user_id);

-- DOWN Migration (in comments or separate file)
-- DROP TABLE IF EXISTS user_preferences CASCADE;
```

---

## 6. Testing Standards

### Test Coverage
- Minimum 80% overall coverage
- 100% coverage for critical paths:
  - Authentication
  - AI API calls
  - Payment processing (when added)
  - Data access with RLS

### Testing Tools
```toml
# pyproject.toml
[tool.poetry.group.dev.dependencies]
pytest = "^7.4.0"
pytest-asyncio = "^0.21.0"
pytest-cov = "^4.1.0"
httpx = "^0.24.1"  # For async client testing
pytest-mock = "^3.11.1"
faker = "^19.3.0"
```

### Test Structure
```python
# tests/integration/test_coach_api.py
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_coach_chat_requires_auth():
    """Test that coach chat endpoint requires authentication."""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/v1/coach/chat", json={
            "message": "Hello coach"
        })
        assert response.status_code == 401

@pytest.mark.asyncio
async def test_coach_chat_success(authenticated_client, mock_anthropic):
    """Test successful coach chat with mocked AI."""
    response = await authenticated_client.post("/api/v1/coach/chat", json={
        "message": "What should I eat for breakfast?",
        "conversation_type": "nutrition"
    })

    assert response.status_code == 200
    data = response.json()
    assert "response" in data
    assert len(data["response"]) > 0

@pytest.mark.asyncio
async def test_coach_chat_rate_limit(authenticated_client):
    """Test rate limiting on coach chat."""
    # Make 101 requests to exceed limit
    for i in range(101):
        response = await authenticated_client.post("/api/v1/coach/chat", json={
            "message": f"Message {i}"
        })

    assert response.status_code == 429
    assert "rate limit" in response.json()["error"].lower()
```

### Test Commands
```bash
# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html --cov-report=term-missing

# Run specific test file
poetry run pytest tests/unit/test_meal_parser.py -v

# Run tests matching pattern
poetry run pytest -k "coach" -v
```

---

## 7. Error Handling & Logging

### Custom Exceptions
```python
# app/core/exceptions.py
class WagnerCoachException(Exception):
    """Base exception for Wagner Coach backend."""
    pass

class AuthenticationError(WagnerCoachException):
    """Raised when authentication fails."""
    pass

class RateLimitError(WagnerCoachException):
    """Raised when rate limit is exceeded."""
    pass

class AIServiceError(WagnerCoachException):
    """Raised when AI API call fails."""
    pass

class ValidationError(WagnerCoachException):
    """Raised when input validation fails."""
    pass
```

### Error Handling Pattern
```python
from fastapi import APIRouter, HTTPException, status
import structlog

router = APIRouter()
logger = structlog.get_logger()

@router.post("/coach/chat")
async def coach_chat(
    request: ChatRequest,
    current_user: dict = Depends(get_current_user)
):
    """Process coach chat message."""
    try:
        user_id = current_user["user_id"]

        # Check rate limit
        if await is_rate_limited(user_id, "chat"):
            raise RateLimitError("Daily chat limit exceeded")

        # Build context with RAG
        context = await build_context(user_id, request.message)

        # Call AI with streaming
        response_generator = await coach_service.chat(
            user_id=user_id,
            message=request.message,
            context=context,
            conversation_type=request.conversation_type
        )

        return StreamingResponse(
            response_generator,
            media_type="text/event-stream"
        )

    except RateLimitError as e:
        logger.warning("Rate limit exceeded", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="You've reached your daily chat limit. Please try again tomorrow."
        )

    except AIServiceError as e:
        logger.error("AI service failed", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="AI service is temporarily unavailable. Please try again."
        )

    except Exception as e:
        logger.error("Unexpected error in coach chat", user_id=user_id, error=str(e))
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred. Please try again."
        )
```

### Structured Logging
```python
# app/core/logging.py
import structlog
import logging
from app.config import settings

def configure_logging():
    """Configure structured logging with structlog."""
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )

    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, settings.LOG_LEVEL.upper())
    )
```

---

## 8. API Documentation

### Endpoint Documentation
```python
from fastapi import APIRouter, status
from app.models.requests import CreateMealRequest
from app.models.responses import MealResponse, ErrorResponse

router = APIRouter()

@router.post(
    "/meals",
    response_model=MealResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid input"},
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Log a meal",
    description="""
    Log a meal with detailed nutrition information.

    This endpoint:
    - Validates meal data
    - Stores in database with user_id
    - Generates embeddings for semantic search
    - Returns created meal with ID

    **Rate limit**: 100 meals per day
    """,
    tags=["nutrition"]
)
async def create_meal(
    request: CreateMealRequest,
    current_user: dict = Depends(get_current_user)
):
    """Create a new meal log entry."""
    # Implementation
```

### Pydantic Models
```python
from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Optional

class CreateMealRequest(BaseModel):
    """Request model for creating a meal log."""

    meal_type: str = Field(..., description="Type of meal (breakfast, lunch, dinner, snack)")
    logged_at: datetime = Field(default_factory=datetime.utcnow, description="When meal was consumed")
    calories: int = Field(..., ge=0, le=10000, description="Total calories")
    protein: float = Field(..., ge=0, le=1000, description="Protein in grams")
    carbs: float = Field(..., ge=0, le=1000, description="Carbohydrates in grams")
    fats: float = Field(..., ge=0, le=1000, description="Fats in grams")
    foods: list[str] = Field(default=[], description="List of foods in meal")
    notes: Optional[str] = Field(None, max_length=500, description="Additional notes")

    @validator("meal_type")
    def validate_meal_type(cls, v):
        allowed = ["breakfast", "lunch", "dinner", "snack"]
        if v not in allowed:
            raise ValueError(f"meal_type must be one of {allowed}")
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "meal_type": "breakfast",
                "logged_at": "2025-10-05T08:30:00Z",
                "calories": 450,
                "protein": 35,
                "carbs": 40,
                "fats": 15,
                "foods": ["eggs", "oatmeal", "banana"],
                "notes": "Post-workout meal"
            }
        }

class MealResponse(BaseModel):
    """Response model for meal operations."""

    id: str
    user_id: str
    meal_type: str
    logged_at: datetime
    calories: int
    protein: float
    carbs: float
    fats: float
    foods: list[str]
    notes: Optional[str]
    created_at: datetime
```

---

## 9. Deployment Checklist

### Pre-Deployment
- [ ] All tests passing (pytest)
- [ ] Coverage ≥80%
- [ ] No linting errors (ruff, black)
- [ ] Type checking passes (mypy)
- [ ] Environment variables documented in .env.example
- [ ] Database migrations tested
- [ ] Supabase RLS policies verified
- [ ] Rate limiting configured
- [ ] Error tracking configured (Sentry)
- [ ] Health check endpoint working
- [ ] API documentation generated (FastAPI docs)

### Railway/Fly.io Deployment
```bash
# Environment variables to set:
SUPABASE_URL=xxx
SUPABASE_KEY=xxx
SUPABASE_SERVICE_KEY=xxx
OPENAI_API_KEY=xxx
ANTHROPIC_API_KEY=xxx
GROQ_API_KEY=xxx
OPENROUTER_API_KEY=xxx
JWT_SECRET=xxx
CRON_SECRET=xxx
WEBHOOK_SECRET=xxx
REDIS_URL=xxx
SENTRY_DSN=xxx
LOG_LEVEL=INFO
ENVIRONMENT=production

# Deployment settings:
- Build command: poetry install --no-dev && poetry run uvicorn app.main:app
- Health check: /health
- Port: 8000
- Python version: 3.11
```

### Post-Deployment
- [ ] Health check returns 200
- [ ] Authentication working
- [ ] Database connection verified
- [ ] AI endpoints responding
- [ ] Strava/Garmin webhooks configured
- [ ] Error tracking receiving events
- [ ] Monitor logs for errors
- [ ] Verify rate limiting working
- [ ] Check API response times
- [ ] Monitor AI API costs

---

## 10. Wagner Coach-Specific Patterns

### Multimodal Quick Entry
```python
# Quick entry processes text, voice, images, and PDFs
# ALWAYS use the cheapest model that works

async def process_quick_entry(
    user_id: str,
    input_type: str,  # "text", "image", "audio", "multimodal"
    content: dict
) -> dict:
    """
    Process quick entry with appropriate AI model.

    Model selection:
    - Text only: Groq Llama 3.3 70B ($0.05/M tokens)
    - Image: Llama 4 Scout ($0.50/M tokens)
    - Audio: FREE Whisper Tiny (local)
    - Multimodal: Combination of above
    """
    if input_type == "text":
        return await process_text_entry(user_id, content["text"])
    elif input_type == "image":
        return await process_image_entry(user_id, content["image_url"])
    elif input_type == "audio":
        # Transcribe with FREE Whisper
        text = await transcribe_audio(content["audio_url"])
        return await process_text_entry(user_id, text)
    elif input_type == "multimodal":
        # Combine results from multiple modalities
        return await process_multimodal_entry(user_id, content)
```

### RAG Context Building
```python
async def build_context(user_id: str, query: str, max_tokens: int = 4000) -> str:
    """
    Build context for AI chat using RAG.

    Steps:
    1. Generate query embedding (FREE sentence-transformers)
    2. Search multimodal_embeddings table (pgvector)
    3. Retrieve top 10 relevant items
    4. Format as context string
    5. Truncate to max_tokens
    """
    # Generate embedding with FREE model
    embedding = await generate_embedding(query)

    # Search with pgvector
    results = await supabase.rpc(
        "search_multimodal_embeddings",
        {
            "query_embedding": embedding,
            "user_id_filter": user_id,
            "match_threshold": 0.7,
            "match_count": 10
        }
    ).execute()

    # Build context string
    context_parts = []
    for item in results.data:
        context_parts.append(f"[{item['content_type']}] {item['content']}")

    context = "\n\n".join(context_parts)

    # Truncate to token limit
    return truncate_to_tokens(context, max_tokens)
```

### AI Program Generation
```python
async def generate_program(user_id: str, answers: dict) -> str:
    """
    Generate 12-week AI program (84 days).

    Uses Claude 3.5 Sonnet due to complexity:
    - Requires long-term planning
    - Progressive overload logic
    - Meal planning with variety
    - Cost: ~$0.15 per generation (acceptable for infrequent use)
    """
    system_prompt = """
    You are an expert fitness and nutrition coach creating a personalized 12-week program.

    Generate:
    1. Weekly workout splits (training days, rest days)
    2. Daily workout plans (exercises, sets, reps, intensity)
    3. Daily meal plans (breakfast, lunch, dinner, snacks with macros)
    4. Progressive overload strategy
    5. Weekly check-ins and adjustments

    Format as JSON with this structure:
    {
        "program_name": "...",
        "weeks": [
            {
                "week_number": 1,
                "days": [
                    {
                        "day_number": 1,
                        "workout": {...},
                        "meals": [...]
                    }
                ]
            }
        ]
    }
    """

    # Use Claude with long context
    response = await anthropic_client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=16000,  # Long programs require many tokens
        system=system_prompt,
        messages=[{
            "role": "user",
            "content": f"User profile: {json.dumps(answers)}"
        }]
    )

    # Log cost
    await log_api_call(
        provider="anthropic",
        model="claude-3-5-sonnet-20241022",
        tokens_in=response.usage.input_tokens,
        tokens_out=response.usage.output_tokens,
        cost=calculate_cost(response.usage),
        user_id=user_id,
        endpoint="/programs/generate"
    )

    return response.content[0].text
```

---

## 11. Quick Reference: Daily Checklist

When implementing any backend feature:
- [ ] Create design doc with API contracts
- [ ] Create test plan
- [ ] Write Pydantic request/response models
- [ ] Write tests first (TDD)
- [ ] Implement service logic
- [ ] Implement API endpoint
- [ ] Add authentication & authorization
- [ ] Add rate limiting (if needed)
- [ ] Add error handling
- [ ] Add structured logging
- [ ] Select cheapest AI model that works
- [ ] Log AI API costs
- [ ] Verify database RLS policies
- [ ] Test with Postman/curl
- [ ] Run pytest with coverage
- [ ] Update API documentation
- [ ] Code review (self or peer)

---

## Summary: Production-Level Backend

Code is production-level when:
1. ✅ All 7 TDD steps completed
2. ✅ API fully documented (FastAPI auto-docs)
3. ✅ Authentication & authorization working
4. ✅ Rate limiting implemented
5. ✅ Error handling comprehensive
6. ✅ Structured logging configured
7. ✅ Test coverage ≥80%
8. ✅ Database RLS policies verified
9. ✅ AI costs optimized & monitored
10. ✅ Ready for real users without shame

**If you can deploy it to production and sleep well at night, it's production-level.**

---

**Remember**: Users don't see your code, they experience your API. Make every endpoint reliable, secure, and cost-efficient.
