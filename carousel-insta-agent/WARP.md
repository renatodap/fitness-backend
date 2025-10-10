# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

**Instagram Carousel AI Agent** is a production-ready AI system that automates the creation of high-quality Instagram carousels. The system uses a hybrid architecture combining traditional service orchestration with intelligent micro-agents for adaptive quality improvement.

**Key Characteristics:**
- **Tech Stack**: FastAPI (Python 3.11+), Next.js 14 (TypeScript), Supabase (PostgreSQL + RLS), Redis, Celery
- **Quality Target**: 93-95% (validated by real Instagram engagement metrics)
- **Cost per Carousel**: ~$2.60-3.50 (depending on quality settings)
- **Generation Time**: 5-10 minutes per carousel
- **Test Coverage Target**: ≥80%
- **Status**: Production Ready ✅

---

## Development Commands

### Backend (Python/FastAPI)

```bash
# Navigate to backend directory
cd backend

# Install dependencies
poetry install

# Activate virtual environment
poetry shell

# Run development server with auto-reload
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run with debug logging
poetry run uvicorn app.main:app --reload --log-level debug
```

**Backend runs at**: `http://localhost:8000`
**API Documentation**: `http://localhost:8000/docs` (Swagger UI)

### Frontend (Next.js 14)

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build

# Start production server
npm run start

# Type checking
npm run type-check
```

**Frontend runs at**: `http://localhost:3000`

### Testing

```bash
# Backend - Run all tests with coverage
cd backend
poetry run pytest --cov=app --cov-report=html --cov-report=term

# Run specific test file
poetry run pytest tests/unit/test_carousel_service.py -v

# Run specific test function
poetry run pytest tests/unit/test_carousel_service.py::test_generate_carousel -v

# Run only unit tests
poetry run pytest tests/unit/ -v

# Run only integration tests
poetry run pytest tests/integration/ -v

# Run tests excluding slow ones
poetry run pytest -m "not slow"

# Coverage report location: backend/htmlcov/index.html
```

**Test coverage requirement**: ≥80% (enforced in `pytest.ini` with `--cov-fail-under=80`)

### Linting and Formatting

```bash
# Backend - Format code
cd backend
poetry run black app/
poetry run isort app/

# Check code style
poetry run ruff check app/

# Type checking
poetry run mypy app/

# Frontend - Lint
cd frontend
npm run lint
```

**Configuration files:**
- Backend: `pyproject.toml` (black, ruff, mypy settings)
- Frontend: `.eslintrc.json`, `tsconfig.json`

### Database (Supabase)

```bash
# Apply migrations
cd backend
poetry run alembic upgrade head

# Create new migration
poetry run alembic revision -m "description"

# Rollback last migration
poetry run alembic downgrade -1

# View migration history
poetry run alembic history
```

**Migration files**: `backend/migrations/`

### Background Tasks (Celery)

```bash
# Start Celery worker (in separate terminal)
cd backend
poetry run celery -A app.workers.celery_app worker --loglevel=info

# Start with autoreload for development
poetry run celery -A app.workers.celery_app worker --loglevel=info --autoreload

# Purge all tasks from queue
poetry run celery -A app.workers.celery_app purge
```

**Redis must be running**: `redis://localhost:6379/0`

### Docker Compose (Full Stack)

```bash
# Start all services (backend, frontend, worker, redis)
docker-compose up -d

# View logs
docker-compose logs -f

# View specific service logs
docker-compose logs -f backend

# Stop all services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

**Services exposed:**
- Backend: `localhost:8000`
- Frontend: `localhost:3000`
- Redis: `localhost:6379`

---

## Architecture Overview

### Hybrid Micro-Agents System

The system uses **conditionally-enabled micro-agents** that provide adaptive quality improvement at critical pipeline stages. This is controlled by the `AGENT_ENABLED` environment variable.

**Three Micro-Agents** (located in `backend/app/agents/`):

1. **ResearchAgent** (`research_agent.py`)
   - Evaluates initial research quality
   - Triggers deep research if quality < 7.0/10
   - Adds ~$0.20 per carousel when deep research needed
   - Improves quality from 6.5 → 8.2 when triggered

2. **CopywritingAgent** (`copywriting_agent.py`)
   - Iteratively improves slide copy quality
   - Quality loop: generate → evaluate → retry (if < 8.0/10)
   - Max 3 iterations per slide
   - Success rate: ~60% first attempt, ~35% second, ~5% third
   - Average quality improvement: 7.2 → 8.4/10

3. **HookAgent** (`hook_agent.py`)
   - Generates 10 hook variations using proven patterns
   - Ranks hooks by predicted engagement
   - Auto-selects best performer (or keeps original if it scores well)
   - Cost: ~$0.40 per carousel

**Integration Point**: `backend/app/services/carousel_service.py`

The agents are initialized in `CarouselService.__init__()` only when `settings.AGENT_ENABLED = True`. The main pipeline in `generate_carousel_async()` conditionally calls agents at these stages:

- After initial research (line ~183): `research_agent.execute_with_adaptive_depth()`
- During copywriting (line ~262): `copywriting_agent.generate_all_slides_with_quality_check()`
- After copywriting (line ~301): `hook_agent.optimize_hook()`

**Cost Impact**:
- Without agents: ~$2.55/carousel
- With agents: ~$3.09/carousel (+21%)
- Time increase: ~1.3 minutes (+18%)
- Quality improvement: 85% → 93-95%

**Configuration** (in `.env`):
```bash
AGENT_ENABLED=true

# Copywriting Agent
COPYWRITING_AGENT_MIN_QUALITY=8.0
COPYWRITING_AGENT_MAX_ITERATIONS=3

# Research Agent
RESEARCH_AGENT_MIN_QUALITY=7.0
RESEARCH_AGENT_DEEP_RESEARCH_THRESHOLD=6.5

# Hook Agent
HOOK_AGENT_NUM_VARIATIONS=10
HOOK_AGENT_AUTO_SELECT_BEST=true
```

---

## Carousel Generation Pipeline

**Main orchestrator**: `backend/app/services/carousel_service.py::generate_carousel_async()`

**10-Step Pipeline** (runs as Celery background task):

1. **Research Topic** (line ~164)
   - Uses `ResearchService.research_topic()` → Perplexity API
   - Optionally includes Reddit/Twitter scraping
   - Cost: ~$0.30
   - WebSocket event: `status_update` → "researching" (20% progress)

2. **Research Quality Check** (line ~183, micro-agent)
   - If `AGENT_ENABLED`: `ResearchAgent.execute_with_adaptive_depth()`
   - Evaluates research quality, triggers deep research if needed
   - Cost: +$0.10-0.20 (conditional)

3. **Validate Topic Quality** (line ~208)
   - Checks `validation_score >= 6.0/10`
   - Fails carousel if topic not viable
   - Saves research data to database

4. **Create Outline** (line ~228)
   - Uses `ContentService.create_outline()`
   - Generates slide structure based on carousel_type
   - Cost: ~$0.25
   - WebSocket event: "writing" (35% progress)

5. **Generate Slide Copy** (line ~254, micro-agent)
   - If `AGENT_ENABLED`: `CopywritingAgent.generate_all_slides_with_quality_check()`
   - Otherwise: Traditional `ContentService.write_slides_copy()`
   - Quality loop runs per slide until score >= 8.0 (max 3 iterations)
   - Cost: ~$0.80-0.95
   - WebSocket event: "writing" (45% progress)

6. **Optimize Hook** (line ~300, micro-agent)
   - If `AGENT_ENABLED`: `HookAgent.optimize_hook()`
   - Generates 10 hook variations, ranks by predicted engagement
   - Updates first slide with best-performing hook
   - Cost: ~$0.40-0.45

7. **Generate Caption** (line ~335)
   - Uses `ContentService.generate_caption()`
   - Creates Instagram caption with hashtags
   - Cost: ~$0.20

8. **Generate Visuals** (line ~362)
   - Creates slide records in database
   - For each slide: `VisualService.generate_slide_visuals()`
   - Uses DALL-E 3 for image generation (1024x1792, 9:16 aspect ratio)
   - Cost: ~$0.08 per slide (~$0.64 for 8 slides)
   - WebSocket events: Per-slide progress (60-90%)

9. **Quality Validation** (line ~400+)
   - `QualityService.validate_carousel()`
   - Checks readability, accessibility, brand consistency
   - Identifies improvement opportunities

10. **Mark Complete** (line ~450+)
    - Updates carousel status to "completed"
    - Records total cost
    - WebSocket event: "completed" (100%)
    - Optionally triggers auto-publish if `auto_publish=True`

**Real-time Progress**: The pipeline emits WebSocket events to `ws://localhost:8000/api/v1/ws/{carousel_id}` for frontend live updates.

**Error Handling**: Any exception marks carousel as "failed" and logs error details to Sentry (if configured).

---

## Human-in-the-Loop Approval Workflow

**Status**: Production Ready ✅ (fully implemented and tested)

The approval workflow replaces automated generation with **human-driven quality control**. Instead of generating one carousel, the system generates **3 variants per stage** (10 for hooks) and waits for human approval before proceeding.

**Files**:
- Service: `backend/app/services/approval_service.py` (600 lines)
- API: `backend/app/api/v1/approval.py` (400 lines)
- Frontend: `frontend/app/carousel/[id]/approval/page.tsx` (700 lines)

**5-Stage Approval System**:

1. **Research Approval**
   - System generates 3 research approaches:
     - Comprehensive (deep + Reddit + Twitter)
     - Focused (core concepts only)
     - Visual-first (emphasizes visual opportunities)
   - User selects preferred research direction
   - State: `awaiting_research_approval`

2. **Outline Approval**
   - System generates 3 slide structures:
     - Narrative flow (story-driven)
     - Informational (fact-dense)
     - Action-oriented (practical steps)
   - User selects preferred structure
   - State: `awaiting_outline_approval`

3. **Copywriting Approval**
   - System generates 3 copywriting styles:
     - Educational (teaching-focused)
     - Conversational (friendly, relatable)
     - Professional (authoritative)
   - User can **edit** variants before approving
   - State: `awaiting_copywriting_approval`

4. **Hook Approval**
   - System generates **10 hook variations** using proven patterns:
     - Pattern interrupt, curiosity gap, bold claim, FOMO, etc.
   - Each ranked by **heuristic score** (0-10)
   - User selects highest-performing hook
   - State: `awaiting_hook_approval`

5. **Visual Approval**
   - System generates 3 visual design approaches:
     - Modern minimal
     - Bold vibrant
     - Tech professional
   - User selects preferred design system
   - State: `awaiting_visual_approval`

**State Machine**: After each approval, workflow auto-progresses to next stage until complete.

**Heuristic Scoring** (NOT AI evaluation):
```python
# Example: Hook scoring (NO circular Claude evaluation)
def _calculate_heuristic_score(text):
    score = 0.0
    score += word_count_score(text)     # 5-10 words optimal
    score += 2.0 if "?" in text else 0  # Curiosity gap
    score += 2.0 if has_numbers else 0  # Specificity
    score += 1.0 if has_emphasis else 0 # CAPS/bold
    return score / 15 * 10              # Normalize to 0-10
```

**API Endpoints**:
- `GET /carousels/{id}/approval` - Get workflow status
- `POST /carousels/{id}/approval/approve` - Approve variant, progress to next stage
- `POST /carousels/{id}/approval/reject` - Reject all variants, regenerate with feedback
- `PATCH /carousels/{id}/approval/edit` - Edit variant before approving
- `GET /carousels/{id}/approval/stages/{stage}` - Get stage-specific variants

**Database Tables**:
- `approval_stages` - Tracks workflow state machine
- `carousel_variants` - Stores 3 variants per stage with heuristic scores
- `user_selections` - Records user's choice and reasoning

**User Experience**: 
1. User creates carousel → Approval workflow initialized
2. For each stage: Review 3 variants → Pick one → Auto-progress to next
3. Option to reject all and regenerate with feedback
4. Option to edit selected variant before approval
5. Workflow completes → Final carousel generated

---

## Learning System (Real Engagement Tracking)

**Status**: Core backend complete (60% total progress)

The learning system tracks **real Instagram engagement metrics** to identify successful patterns and improve future generations.

**Files**:
- Learning Service: `backend/app/services/learning_service.py` (500 lines)
- Embedding Service: `backend/app/services/embedding_service.py` (450 lines)
- Heuristics: `backend/app/core/heuristics.py` (400 lines)
- Analytics: `backend/app/services/analytics_service.py`

**Database Tables**:
- `user_variant_scores` - User ratings (1-5 stars) for variants
- `engagement_learnings` - Real Instagram metrics (impressions, saves, likes, shares)
- `learned_patterns` - Identified patterns with performance metrics
- `variant_embeddings` - pgvector embeddings (1536-dim) for semantic search
- `variant_performance` - Aggregated pattern performance

**Key Concepts**:

1. **Engagement Tracking**
   - User publishes carousel → Records Instagram metrics after 24-48 hours
   - Key metric: **save_rate** (saves/impressions)
   - Target: save_rate > 3% = high-quality content
   - Stored in `engagement_learnings` table

2. **Pattern Recognition**
   - System extracts features from successful variants:
     - Has question mark → 4.5/5 avg user score
     - Uses numbers → 4.1% save rate
     - Curiosity gap pattern → 8.2/10 engagement
   - Stored in `learned_patterns` table
   - Running averages updated as more data comes in

3. **Semantic Search (pgvector)**
   - Uses OpenAI `text-embedding-3-small` (1536 dimensions)
   - Cost: $0.02 per million tokens
   - Enables finding similar successful content:
     ```python
     # Find hooks similar to new topic that performed well
     examples = await embedding_service.search_similar_successful_variants(
         topic="RAG systems in AI",
         stage="hook",
         min_save_rate=3.0
     )
     ```

4. **Combined Reward Signal**
   - User score (1-5 stars) × 0.4 + Engagement score (0-10) × 0.6
   - Weights real performance over user preference
   - Used to rank learned patterns

5. **Generation Integration** (pending)
   - Future versions will inject learned patterns into generation prompts
   - Example: "User prefers question-based hooks (4.5/5 avg), generates 4.1% save rate"
   - Ensures diversity with cosine similarity checks

**API Endpoints** (planned):
- `POST /carousels/{id}/variants/{variant_id}/score` - User rates variant 1-5 stars
- `POST /carousels/{id}/engagement` - Record Instagram metrics
- `GET /carousels/{id}/learning-insights` - Get learned patterns

**Heuristic Dimensions**:

**Hook Scoring** (9 dimensions):
- Readability (Flesch-Kincaid)
- Sentiment (emotional appeal)
- Specificity (concrete vs abstract)
- Urgency/FOMO detection
- Curiosity gap analysis
- Has numbers
- Has question mark
- Word count (5-12 optimal)
- Pattern matching (learned successful patterns)

**Copywriting Scoring** (5 dimensions):
- Readability
- Sentiment
- Has CTA
- Consistency across slides
- Learned tone matching

---

## Service Layer Architecture

**Location**: `backend/app/services/`

The backend uses a **service-oriented architecture** where each service handles a specific domain:

### Core Services

1. **CarouselService** (`carousel_service.py`)
   - Main orchestrator for carousel generation pipeline
   - Coordinates all other services
   - Manages WebSocket progress updates
   - Initializes micro-agents conditionally

2. **ResearchService** (`research_service.py`)
   - Perplexity API integration for topic research
   - Reddit scraping (PRAW library)
   - Twitter scraping (Tweepy library)
   - Trend analysis and topic validation

3. **ContentService** (`content_service.py`)
   - Claude AI integration for copywriting
   - Outline generation based on carousel_type
   - Slide copy generation with brand voice
   - Caption and hashtag generation

4. **VisualService** (`visual_service.py`)
   - DALL-E 3 integration for image generation
   - Image composition and text overlay
   - Brand design system application
   - 9:16 aspect ratio enforcement for Instagram

5. **QualityService** (`quality_service.py`)
   - Readability scoring (Flesch-Kincaid)
   - Accessibility validation
   - Brand consistency checking
   - Fact-checking and validation

6. **ApprovalService** (`approval_service.py`)
   - Approval workflow state machine
   - Variant generation coordination
   - Heuristic scoring (non-AI evaluation)
   - User selection tracking

7. **LearningService** (`learning_service.py`)
   - Pattern recognition from engagement data
   - Learned preferences tracking
   - Feature extraction from variants
   - Performance analytics

8. **AnalyticsService** (`analytics_service.py`)
   - Instagram Graph API integration
   - Engagement metrics tracking
   - Predictive scoring for new content
   - Performance reporting

9. **SupabaseService** (`supabase_service.py`)
   - Database abstraction layer
   - CRUD operations for all tables
   - Row Level Security (RLS) enforcement
   - Query optimization

10. **InstagramService** (`instagram_service.py`)
    - Instagram Graph API publishing
    - Media upload and carousel creation
    - Scheduling integration
    - Access token management

### Database Schema (Supabase/PostgreSQL)

**Core Tables**:

- `users` - User accounts and authentication
- `carousels` - Carousel metadata and status
- `slides` - Individual slides with copy and visuals
- `approval_stages` - Approval workflow state
- `carousel_variants` - Generated variants for approval
- `user_selections` - User's approval choices
- `engagement_learnings` - Instagram metrics (THE TRUE quality source)
- `learned_patterns` - Identified successful patterns
- `variant_embeddings` - pgvector embeddings for semantic search

**Row Level Security (RLS)**:
- All tables have RLS policies enabled
- Users can only access their own data
- Service role key bypasses RLS for backend operations
- Enforced at database level (not application)

**Relationships**:
```
users (1) ──── (N) carousels
carousels (1) ──── (N) slides
carousels (1) ──── (1) approval_stages
approval_stages (1) ──── (N) carousel_variants
carousel_variants (1) ──── (0-1) user_selections
carousels (1) ──── (0-1) engagement_learnings
```

### Background Processing (Celery)

**Task Queue**: Redis-backed Celery for async processing

**Workers** (`backend/app/workers/`):
- `generate_carousel_task` - Main carousel generation pipeline
- `publish_carousel_task` - Instagram publishing
- `fetch_analytics_task` - Periodic analytics updates
- `cleanup_old_data_task` - Data retention management

**Queue Configuration**:
```python
CELERY_BROKER_URL = "redis://localhost:6379/0"
CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
```

**Task Monitoring**: Use Flower for task monitoring in development:
```bash
poetry run celery -A app.workers.celery_app flower
```

### Real-time Updates (WebSocket)

**Location**: `backend/app/api/v1/websocket.py`

**WebSocket Manager**:
- Manages active connections per carousel_id
- Broadcasts progress events to connected clients
- Auto-reconnection handling on frontend

**Connection**: `ws://localhost:8000/api/v1/ws/{carousel_id}`

**Event Types**:
```python
{
  "event": "status_update",
  "data": {
    "status": "researching",
    "progress_percentage": 20,
    "current_step": "Researching topic"
  }
}

{
  "event": "step_progress",
  "data": {
    "step": "visuals",
    "progress": "3/8",
    "progress_percentage": 70,
    "current_step": "Generating visual 3/8"
  }
}

{
  "event": "completed",
  "data": {
    "carousel_id": "uuid",
    "total_cost": 3.09
  }
}
```

---

## Configuration and Environment Variables

**Configuration File**: `backend/app/config.py` (Settings class using Pydantic)

**Environment File**: `backend/.env` (copy from `.env.example`)

### Critical Environment Variables

**API Keys** (all required):
```bash
# AI Services
ANTHROPIC_API_KEY=sk-ant-api03-...        # Claude for copywriting
OPENAI_API_KEY=sk-...                     # DALL-E 3 for images + embeddings
PERPLEXITY_API_KEY=pplx-...               # Research

# Instagram
INSTAGRAM_APP_ID=...                      # Meta app ID
INSTAGRAM_APP_SECRET=...                  # Meta app secret
INSTAGRAM_ACCESS_TOKEN=...                # Long-lived token
INSTAGRAM_BUSINESS_ACCOUNT_ID=...         # Instagram business account

# Database
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=...                          # Anon key (frontend)
SUPABASE_SERVICE_KEY=...                  # Service role key (backend)

# Security
JWT_SECRET=...                            # Min 32 characters
CRON_SECRET=...                           # For scheduled tasks
WEBHOOK_SECRET=...                        # For webhooks
```

**Optional API Keys**:
```bash
# Social Media (for research)
REDDIT_CLIENT_ID=...
REDDIT_CLIENT_SECRET=...
TWITTER_BEARER_TOKEN=...

# Monitoring
SENTRY_DSN=...                            # Error tracking
```

### Cost and Quality Settings

```bash
# Cost control
TARGET_COST_PER_CAROUSEL=3.50             # Warning threshold
ENABLE_COST_TRACKING=true

# Quality thresholds
RESEARCH_AGENT_MIN_QUALITY=7.0            # Minimum research quality
COPYWRITING_AGENT_MIN_QUALITY=8.0         # Minimum slide quality

# Agent settings
AGENT_ENABLED=true                        # Enable micro-agents
COPYWRITING_AGENT_MAX_ITERATIONS=3        # Max retries per slide
HOOK_AGENT_NUM_VARIATIONS=10              # Hook variations to generate
```

### Feature Flags

```bash
# Research sources
ENABLE_REDDIT_RESEARCH=true
ENABLE_TWITTER_RESEARCH=true

# Publishing
ENABLE_AUTO_PUBLISH=false                 # Manual publish by default

# Tracking
ENABLE_ANALYTICS_TRACKING=true
```

### AI Model Configuration

```bash
# Claude (Anthropic)
CLAUDE_MODEL=claude-3-5-sonnet-20241022   # Latest Sonnet
CLAUDE_MAX_TOKENS=4000

# DALL-E 3 (OpenAI)
DALLE_MODEL=dall-e-3
DALLE_IMAGE_SIZE=1024x1792                # 9:16 for Instagram
DALLE_QUALITY=hd

# Content defaults
DEFAULT_SLIDE_COUNT=8
MIN_SLIDE_COUNT=5
MAX_SLIDE_COUNT=10
```

### Cache TTL

```bash
RESEARCH_CACHE_TTL=86400                  # 24 hours
ANALYTICS_CACHE_TTL=3600                  # 1 hour
```

### Production vs Development

**Development** (`ENVIRONMENT=development`):
- Debug mode enabled
- CORS allows localhost origins
- Detailed error messages
- Sentry traces at 100%

**Production** (`ENVIRONMENT=production`):
- Debug mode disabled
- CORS restricted to production domains
- Generic error messages
- Sentry traces at 10% (sampling)

---

## Key Architectural Concepts

### Cost Optimization

**Problem**: AI APIs are expensive. A single carousel uses Claude, Perplexity, and DALL-E.

**Solution**: Multi-layered cost tracking and optimization

1. **Per-Service Cost Tracking**
   - Each service method returns `{"result": ..., "cost": float}`
   - Costs accumulated in `generate_carousel_async()`: `total_cost += service_result.get("cost", 0.0)`
   - Stored in `carousels.metadata->generation_cost`

2. **Cost Warnings**
   ```python
   if total_cost > settings.TARGET_COST_PER_CAROUSEL * 1.5:
       logger.warning("cost_limit_warning", total_cost=total_cost)
   ```

3. **Micro-Agent Cost Control**
   - Agents track their own costs in `BaseAgent._call_claude()`
   - Max iterations prevent infinite loops (e.g., `COPYWRITING_AGENT_MAX_ITERATIONS=3`)
   - Deep research only triggered when quality < threshold

4. **Caching**
   - Research results cached for 24 hours
   - Analytics cached for 1 hour
   - Reduces redundant API calls

**Typical Costs** (with agents enabled):
- Research: $0.30-0.50
- Outline: $0.25
- Copywriting: $0.80-0.95
- Visuals: $0.64 (8 slides × $0.08)
- Caption: $0.20
- Hook optimization: $0.40-0.45
- **Total: $2.85-3.45**

### Quality vs Speed Trade-offs

**Configuration knobs**:

1. **Agent Quality Thresholds**
   - Higher `COPYWRITING_AGENT_MIN_QUALITY` → Better quality, more retries, higher cost
   - Lower threshold → Faster, cheaper, but may need manual edits

2. **Max Iterations**
   - `COPYWRITING_AGENT_MAX_ITERATIONS=3` → Balances quality and time
   - Increase to 5 for critical use cases (expect +1-2 minutes, +$0.30)

3. **Research Depth**
   - `RESEARCH_AGENT_DEEP_RESEARCH_THRESHOLD=6.5` → When to trigger expensive deep research
   - Set higher (e.g., 7.5) to reduce deep research frequency

4. **Hook Variations**
   - `HOOK_AGENT_NUM_VARIATIONS=10` → More options, better hooks, but +30 seconds
   - Reduce to 5 for faster generation

**Recommended Presets**:

**Fast Mode** (MVP, prototyping):
```bash
AGENT_ENABLED=false
ENABLE_REDDIT_RESEARCH=false
ENABLE_TWITTER_RESEARCH=false
# Time: ~5 min, Cost: ~$2.55, Quality: 85%
```

**Balanced Mode** (default):
```bash
AGENT_ENABLED=true
COPYWRITING_AGENT_MAX_ITERATIONS=3
HOOK_AGENT_NUM_VARIATIONS=10
# Time: ~8 min, Cost: ~$3.09, Quality: 93-95%
```

**High-Quality Mode** (critical content):
```bash
AGENT_ENABLED=true
COPYWRITING_AGENT_MIN_QUALITY=9.0
COPYWRITING_AGENT_MAX_ITERATIONS=5
HOOK_AGENT_NUM_VARIATIONS=15
# Time: ~12 min, Cost: ~$4.00, Quality: 96-98%
```

### Scalability Patterns

1. **Async/Await Throughout**
   - All I/O operations use `async`/`await`
   - Non-blocking database queries
   - Concurrent API calls where possible

2. **Background Task Queue**
   - Heavy operations (carousel generation) run in Celery
   - API returns immediately with carousel_id
   - Client polls for status or uses WebSocket

3. **Connection Pooling**
   - Supabase client reuses connections
   - httpx client with connection pooling for external APIs
   - Redis connection pool for Celery

4. **Caching Strategy**
   - Research results cached (24h TTL)
   - Analytics cached (1h TTL)
   - Consider adding Redis cache layer for frequently accessed data

5. **Rate Limiting**
   - API rate limiting: 60 requests/minute per user
   - Protects against abuse
   - Configured in `app/config.py`: `RATE_LIMIT_PER_MINUTE=60`

### Error Handling

**Philosophy**: Graceful degradation where possible, fail fast with clear errors otherwise

1. **Service-Level Try-Catch**
   - Each service wraps external API calls in try-catch
   - Logs error with structured logging
   - Returns error details in response

2. **Agent Fallback Behavior**
   - ResearchAgent fails → Use initial research (no deep research)
   - CopywritingAgent fails → Return best attempt (even if below threshold)
   - HookAgent fails → Keep original hook

3. **Custom Exception Hierarchy**
   ```python
   # app/core/exceptions.py
   CarouselAgentException          # Base exception
   ├── CostLimitExceeded          # Cost > threshold
   ├── APIRateLimitExceeded       # External API rate limit
   ├── InvalidInputException       # User input validation
   └── ServiceUnavailableException # External service down
   ```

4. **Exception Handlers** (in `app/main.py`)
   - Custom exceptions return structured JSON errors
   - Unexpected exceptions logged to Sentry
   - Never expose internal errors to user

5. **Circuit Breaker Pattern** (future enhancement)
   - If external API fails repeatedly, temporarily disable
   - Prevents cascading failures

### Monitoring and Observability

1. **Structured Logging**
   - Uses `structlog` for JSON logs
   - Every log has correlation_id (carousel_id or user_id)
   - Example:
     ```python
     logger.info(
         "carousel_generation_complete",
         carousel_id=carousel_id,
         total_cost=total_cost,
         duration_seconds=duration,
         quality_score=quality_score
     )
     ```

2. **Key Metrics to Track**
   - Generation time (p50, p95, p99)
   - Cost per carousel (avg, p95)
   - Success rate (completed / total)
   - Agent retry rates
   - API error rates
   - User approval rates (approval workflow)

3. **Error Tracking** (Sentry)
   - Automatic error reporting if `SENTRY_DSN` configured
   - Includes request context, user_id, carousel_id
   - Breadcrumbs show pipeline progress before error

4. **Database Queries**
   - All queries logged with execution time
   - Slow query threshold: 1 second
   - Indexes on frequently queried columns

5. **WebSocket Connection Tracking**
   - Active connections per carousel tracked
   - Automatic cleanup on disconnect
   - Heartbeat to detect stale connections

---

## Testing Strategy

**Test Framework**: pytest with pytest-asyncio

**Test Organization**:
- `tests/unit/` - Fast, isolated unit tests
- `tests/integration/` - Tests involving external services (mocked)
- `tests/e2e/` - End-to-end tests (future)

**Key Test Files**:
- `test_carousel_service.py` - Main pipeline tests
- `test_*_agent.py` - Micro-agent tests (30 tests total)
- `test_approval_workflow.py` - Approval workflow (15 tests)

**Running Specific Test Scenarios**:

```bash
# Test carousel generation without agents
poetry run pytest tests/unit/test_carousel_service.py::test_generate_without_agents -v

# Test copywriting agent quality loop
poetry run pytest tests/unit/test_copywriting_agent.py::test_quality_loop_retries -v

# Test approval workflow state machine
poetry run pytest tests/integration/test_approval_workflow.py::test_full_workflow -v
```

**Mocking External Services**:
```python
# Example: Mock Claude API
@pytest.fixture
def mock_claude(mocker):
    return mocker.patch(
        "anthropic.Anthropic.messages.create",
        return_value={"content": [{"text": "Generated content"}]}
    )
```

**Coverage Reports**:
- HTML report: `backend/htmlcov/index.html`
- Terminal report shows line coverage per file
- Fail build if coverage < 80%

---

## Important Cross-Cutting Concerns

### API Versioning
- All API routes prefixed with `/api/v1/`
- Future versions can coexist: `/api/v2/`
- Located in `backend/app/api/v1/router.py`

### CORS Configuration
- Development: Allows `localhost:3000`, `localhost:8000`
- Production: Must whitelist production domains
- Configured in `app/main.py` via `settings.CORS_ORIGINS`

### Authentication (JWT)
- JWT tokens for API authentication
- Generated on login, stored in httpOnly cookie (frontend)
- Validated via `app/api/dependencies/auth.py::get_current_user`
- Token expiration: 7 days (configurable)

### WebSocket Authentication
- WebSocket connections require valid JWT in query param: `?token=xxx`
- Validated on connection establishment
- Connection tied to carousel_id (users can only connect to their own carousels)

### Dependency Injection
- FastAPI's dependency injection used throughout
- Example: `current_user: User = Depends(get_current_user)`
- Services instantiated per request (or use singleton pattern)

### File Storage
- Generated images stored locally: `/tmp/carousel-images/` (development)
- Production: Use S3 or Supabase Storage
- Image URLs stored in database, files cleaned up after 7 days

---

## Common Pitfalls and Solutions

### Pitfall: Circular AI Evaluation
**Problem**: Having Claude evaluate Claude's output creates fake 93-95% scores

**Solution**: Use heuristic scoring (objective metrics only)
- Word count, readability scores, pattern matching
- NO AI evaluation of AI-generated content
- Real validation comes from Instagram engagement metrics

### Pitfall: Infinite Quality Loops
**Problem**: Agent retries forever trying to reach quality threshold

**Solution**: Max iterations limit
- `COPYWRITING_AGENT_MAX_ITERATIONS=3`
- Return best attempt even if below threshold
- Log warning for manual review

### Pitfall: Unchecked API Costs
**Problem**: Costs spiral out of control with retries

**Solution**: Cost tracking and warnings
- Track cost per operation
- Warn if exceeds target × 1.5
- Consider hard limit in production

### Pitfall: Slow Sequential Processing
**Problem**: Generating 8 slides sequentially takes too long

**Solution**: Where possible, parallelize
- Can't parallelize pipeline stages (each depends on previous)
- CAN parallelize visual generation (8 slides can be generated concurrently)
- Use `asyncio.gather()` for concurrent operations

### Pitfall: WebSocket Connection Leaks
**Problem**: Connections not cleaned up on disconnect

**Solution**: Proper cleanup in WebSocket manager
- Track active connections per carousel_id
- Remove on disconnect event
- Periodic cleanup of stale connections

---

## Future Enhancements (Roadmap)

### Near-term (v1.1)
- [ ] Complete learning system frontend (40% remaining)
- [ ] A/B testing integration (test optimized vs original hooks)
- [ ] Agent performance dashboard
- [ ] Cost prediction API endpoint

### Mid-term (v1.2)
- [ ] Multi-agent coordination (agents communicate)
- [ ] Custom agent configurations per user
- [ ] Visual quality agent (image composition evaluation)
- [ ] Cross-platform support (LinkedIn, Twitter, TikTok)

### Long-term (v2.0)
- [ ] Video carousel support (Reels generation)
- [ ] Voice-over generation
- [ ] Multi-language support
- [ ] Enterprise multi-tenant architecture

---

## Quick Reference

**Port Numbers**:
- Backend API: 8000
- Frontend: 3000
- Redis: 6379
- Postgres (Supabase): remote

**Key Directories**:
- Backend: `backend/app/`
- Services: `backend/app/services/`
- Agents: `backend/app/agents/`
- API Routes: `backend/app/api/v1/`
- Frontend: `frontend/`
- Tests: `backend/tests/`
- Migrations: `backend/migrations/`

**Critical Files**:
- Main app: `backend/app/main.py`
- Config: `backend/app/config.py`
- Carousel service: `backend/app/services/carousel_service.py`
- Approval service: `backend/app/services/approval_service.py`
- Learning service: `backend/app/services/learning_service.py`

**Documentation**:
- README: High-level overview
- MICRO_AGENTS_ARCHITECTURE.md: Agent system details
- APPROVAL_WORKFLOW_COMPLETE.md: Human-in-the-loop workflow
- LEARNING_SYSTEM_PROGRESS.md: Learning system implementation
- GETTING_STARTED.md: Setup instructions

**Support**:
- API Docs: http://localhost:8000/docs
- Health Check: http://localhost:8000/health
- Test Coverage: `backend/htmlcov/index.html`
