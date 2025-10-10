# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

---

## Repository Overview

Wagner Coach is an **AI-powered fitness & nutrition coaching platform** with multimodal capabilities. The codebase is organized as a monorepo with two independent repositories:

- **Backend**: Python/FastAPI (`wagner-coach-backend/`)
- **Frontend**: Next.js/React (`wagner-coach-clean/`)

Both repositories deploy independently and communicate via REST API.

---

## Essential Commands

### Backend (Python/FastAPI)

Navigate to `wagner-coach-backend/` first:

```bash
cd wagner-coach-backend
```

**Setup:**
```bash
# Install dependencies
pip install poetry
poetry install

# Setup environment
cp .env.example .env
# Edit .env with actual values
```

**Development:**
```bash
# Run development server
poetry run uvicorn app.main:app --reload

# Access API
# - API: http://localhost:8000
# - Docs: http://localhost:8000/docs
# - Health: http://localhost:8000/health
```

**Testing:**
```bash
# Run all tests
poetry run pytest

# Run with coverage (requires ≥80%)
poetry run pytest --cov=app --cov-report=html --cov-report=term-missing

# Run specific test file
poetry run pytest tests/unit/test_config.py -v

# Run tests in watch mode
poetry run pytest-watch
```

**Code Quality:**
```bash
# Format code
poetry run black app/

# Lint code
poetry run ruff check app/

# Type check
poetry run mypy app/

# Run all quality checks
poetry run black app/ && poetry run ruff check app/ && poetry run mypy app/
```

**Database Migrations:**
```bash
# Create new migration
cd migrations
touch 006_add_feature.sql

# Test migration locally
supabase db push

# Update current schema
supabase db dump > migrations/current.sql
```

---

### Frontend (Next.js/React)

Navigate to `wagner-coach-clean/` first:

```bash
cd wagner-coach-clean
```

**Setup:**
```bash
# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
# Edit .env.local with actual values
```

**Development:**
```bash
# Run development server
npm run dev

# Access app
# - App: http://localhost:3000
```

**Testing:**
```bash
# Run all tests
npm test

# Run tests in watch mode
npm run test:watch

# Run with coverage (requires ≥80%)
npm run test:coverage
```

**Code Quality:**
```bash
# Lint code
npm run lint

# Build for production (also type-checks)
npm run build
```

**Production:**
```bash
# Build and start production server
npm run build
npm run start
```

---

## Architecture Overview

### System Flow

```
User (Mobile/Web)
    ↓
Next.js Frontend (Vercel) - wagner-coach-clean/
    ↓
FastAPI Backend (Railway) - wagner-coach-backend/
    ↓
Supabase (Database + Auth + Storage)
    ↓
AI APIs (Claude, Groq, OpenRouter, FREE models)
```

### Backend Architecture (`wagner-coach-backend/`)

**Tech Stack:**
- Python 3.11+ with FastAPI
- Supabase for database (PostgreSQL with pgvector)
- Multiple AI providers (cost-optimized routing)
- Poetry for dependency management
- pytest for testing (TDD approach)

**Key Directories:**
- `app/api/v1/` - API endpoints (coach.py, programs.py, quick_entry.py, nutrition.py, etc.)
- `app/services/` - Business logic (coach_service.py, quick_entry_service.py, dual_model_router.py, etc.)
- `app/models/` - Pydantic models for request/response/database schemas
- `app/core/` - Core utilities (exceptions.py, security.py, logging.py)
- `migrations/` - SQL database migrations (versioned schema changes)
- `tests/` - Unit and integration tests

**AI Cost Optimization:**
The backend implements intelligent AI model routing to maintain **$0.50/user/month**:
1. FREE models first (embeddings, Whisper transcription)
2. Groq for simple text tasks ($0.05-0.10/M tokens)
3. OpenRouter for medium complexity ($0.50-1.00/M tokens)
4. Claude only for complex reasoning ($3-15/M tokens)

**Authentication:**
- JWT-based authentication via Supabase Auth
- Row-level security (RLS) enforced at database level
- Middleware validates tokens on protected endpoints

---

### Frontend Architecture (`wagner-coach-clean/`)

**Tech Stack:**
- Next.js 15 (App Router)
- React 19
- TypeScript (strict mode)
- Tailwind CSS with shadcn/ui components
- Supabase Auth for authentication
- Jest for testing

**Key Directories:**
- `app/` - Next.js pages and routing
  - `(auth)/` - Authentication pages (login, signup, onboarding)
  - `dashboard/` - Main dashboard
  - `coach-v2/` - AI coach chat interface
  - `programs/` - AI-generated workout programs
  - `nutrition/` - Meal logging and history
  - `activities/` - Workout tracking with Garmin/Strava sync
  - `analytics/` - Progress visualization
  - `profile/` and `settings/` - User management
- `components/` - React components
  - `ui/` - shadcn/ui base components (button, card, input, etc.)
  - Feature-specific subdirectories (Coach/, Programs/, QuickEntry/, etc.)
- `lib/` - Utilities and API clients
  - `api/` - Backend API integration functions
  - `supabase/` - Supabase client configuration
  - `utils/` - Helper functions
- `hooks/` - Custom React hooks
- `types/` - TypeScript type definitions

**Mobile-First Design:**
- Responsive breakpoints: 320px (mobile), 768px (tablet), 1024px+ (desktop)
- Bottom navigation for mobile
- Touch-friendly buttons (minimum 44x44px)
- Optimized images via Next.js Image component

---

## Critical Development Patterns

### When Working on Backend Features

1. **Always read** `wagner-coach-backend/CLAUDE.md` first
2. **Follow TDD**: Write tests BEFORE implementation
3. **Use Pydantic models** for all data validation
4. **Create migrations** for any schema changes in `migrations/`
5. **Choose cheapest AI model** that meets quality requirements
6. **Add structured logging** with user_id and request_id context
7. **Validate authentication** on protected endpoints
8. **Target ≥80% test coverage**

**Example workflow for new endpoint:**
```bash
cd wagner-coach-backend

# 1. Write tests first
touch tests/unit/test_new_feature.py

# 2. Create Pydantic models
# Edit app/models/requests/new_feature.py

# 3. Implement service layer
# Edit app/services/new_feature_service.py

# 4. Create API endpoint
# Edit app/api/v1/new_feature.py

# 5. Run tests until passing
poetry run pytest tests/unit/test_new_feature.py -v

# 6. Verify coverage
poetry run pytest --cov=app.services.new_feature_service --cov-report=term-missing
```

---

### When Working on Frontend Features

1. **Always read** `wagner-coach-clean/CLAUDE.md` first
2. **Define TypeScript interfaces** before implementation
3. **Write component tests** using React Testing Library
4. **Implement loading states** for all async operations
5. **Add error handling** with user-friendly messages
6. **Test responsive design** at mobile, tablet, and desktop breakpoints
7. **Verify accessibility** (WCAG AA standards, keyboard navigation)
8. **Use Tailwind utilities** and shadcn/ui components for consistency

**Example workflow for new page:**
```bash
cd wagner-coach-clean

# 1. Create page directory and component
mkdir -p app/new-feature
touch app/new-feature/page.tsx

# 2. Define TypeScript types
# Edit types/new-feature.ts

# 3. Write component tests
# Edit __tests__/new-feature.test.tsx

# 4. Implement component with loading/error states
# Edit app/new-feature/page.tsx

# 5. Run tests
npm test -- new-feature.test.tsx

# 6. Verify in browser (mobile + desktop)
npm run dev
```

---

## Database Management

**All database code lives in `wagner-coach-backend/migrations/`**

The database uses Supabase (PostgreSQL) with:
- 40+ tables covering users, nutrition, workouts, programs, AI data
- pgvector extension for multimodal RAG (embeddings)
- Row-level security (RLS) policies for data isolation
- Real-time subscriptions for live updates

**Migration workflow:**
1. Create numbered migration file: `migrations/006_add_feature.sql`
2. Write both UP and DOWN migrations
3. Add RLS policies for new tables
4. Test locally: `supabase db push`
5. Update current schema: `supabase db dump > migrations/current.sql`
6. Commit to version control

---

## Multi-Repo Coordination

### When Implementing Full Features

A complete feature typically requires changes in both repos:

1. **Backend first** (API-first approach):
   - Create migration if schema changes needed
   - Write backend tests
   - Implement API endpoint
   - Deploy to staging
   - Verify with Postman/curl

2. **Frontend second**:
   - Update TypeScript types from API response
   - Write component tests
   - Implement UI with loading/error states
   - Test responsive design
   - Deploy to staging

3. **Integration testing**:
   - Test full user flow (UI → API → DB → UI)
   - Verify mobile experience
   - Check error handling
   - Monitor AI costs

### Independent Deployments

Backend and frontend deploy independently:
- **Backend**: Railway (auto-deploy on git push to main)
- **Frontend**: Vercel (auto-deploy on git push to main)

For breaking changes, deploy backend first with backward compatibility, then frontend.

---

## Production Standards

### Security Checklist
- [ ] JWT validation on protected endpoints (backend)
- [ ] Input validation with Pydantic (backend) and Zod (frontend)
- [ ] RLS policies on all database tables
- [ ] No sensitive data exposed to frontend
- [ ] HTTPS only in production

### UX Checklist
- [ ] Loading states on all async operations
- [ ] User-friendly error messages (actionable, specific)
- [ ] Mobile responsive (320px to 1920px)
- [ ] Accessibility (WCAG AA, keyboard navigation)
- [ ] Sufficient contrast (4.5:1 for text, 3:1 for UI)

### Performance Checklist
- [ ] Lighthouse Performance score ≥90
- [ ] API response time <500ms (non-AI endpoints)
- [ ] Images optimized (Next.js Image component)
- [ ] Code splitting with dynamic imports

### Testing Checklist
- [ ] Backend: pytest coverage ≥80%
- [ ] Frontend: Jest coverage ≥80%
- [ ] E2E tests for critical flows
- [ ] Manual testing on real mobile devices

### AI Cost Efficiency
- [ ] Use cheapest model that produces acceptable results
- [ ] Log all AI API calls with cost estimates
- [ ] Monitor monthly costs per user
- [ ] Target: $0.50/user/month

---

## Common Tasks

### Run the full stack locally
```bash
# Terminal 1: Backend
cd wagner-coach-backend
poetry run uvicorn app.main:app --reload

# Terminal 2: Frontend
cd wagner-coach-clean
npm run dev
```

### Run all tests across both repos
```bash
# Backend tests
cd wagner-coach-backend
poetry run pytest --cov=app --cov-report=term-missing

# Frontend tests
cd wagner-coach-clean
npm run test:coverage
```

### Format and lint everything
```bash
# Backend
cd wagner-coach-backend
poetry run black app/ && poetry run ruff check app/

# Frontend
cd wagner-coach-clean
npm run lint
```

### Deploy to staging
```bash
# Backend: Push to backend staging branch
cd wagner-coach-backend
git push origin main

# Frontend: Push to frontend staging branch
cd wagner-coach-clean
git push origin main
```

---

## Important Rules from CLAUDE.md

### Development Process
- **TDD is mandatory**: Write tests BEFORE implementation (both repos)
- **API verification required**: Every endpoint must pass 7-step validation checklist
- **No 'any' types**: Use specific TypeScript types or 'unknown' if necessary
- **Explicit error handling**: No bare except clauses (Python), no ignored errors (TypeScript)

### Code Quality
- **Backend**: Type hints on all functions, docstrings (Google style), Pydantic models
- **Frontend**: Strict TypeScript mode, explicit return types, interfaces for all data
- **Both**: ≥80% test coverage required

### AI Cost Management
**Always use the cheapest model that works:**
1. FREE first (embeddings, Whisper)
2. Groq second (text parsing, extraction)
3. OpenRouter third (image analysis)
4. Claude last (complex reasoning, coaching)

### Security
- Never expose service role keys to frontend
- All environment secrets in `.env` files (not committed)
- JWT validation on every protected endpoint
- RLS policies enforce data isolation at database level

---

## Key Documentation Files

- **Root coordination**: `CLAUDE.md` (read this first for any work)
- **Backend standards**: `wagner-coach-backend/CLAUDE.md`
- **Frontend standards**: `wagner-coach-clean/CLAUDE.md`
- **Backend README**: `wagner-coach-backend/README.md`
- **Frontend README**: `wagner-coach-clean/README.md`

---

## Environment Setup

### Backend `.env` (in `wagner-coach-backend/`)
```bash
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
REDIS_URL=redis://localhost:6379  # Optional
SENTRY_DSN=xxx  # Optional
LOG_LEVEL=INFO  # Optional
```

### Frontend `.env.local` (in `wagner-coach-clean/`)
```bash
NEXT_PUBLIC_SUPABASE_URL=xxx
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx
NEXT_PUBLIC_API_BASE_URL=https://api.wagnercoach.com
NEXT_PUBLIC_APP_URL=https://wagnercoach.com
```

**CRITICAL**: Never share service role keys with the frontend!

---

## Quick Decision Tree

**Where should I work?**

- **New API endpoint or backend logic** → `wagner-coach-backend/`
- **New UI component or page** → `wagner-coach-clean/`
- **Database schema change** → `wagner-coach-backend/migrations/`
- **Full feature (API + UI)** → Both repos (backend first, then frontend)

**What should I read first?**

1. This WARP.md (you're here!)
2. Root `CLAUDE.md` for project overview
3. Repo-specific `CLAUDE.md` for detailed standards:
   - Backend: `wagner-coach-backend/CLAUDE.md`
   - Frontend: `wagner-coach-clean/CLAUDE.md`

---

**Wagner Coach is an AI-powered coaching platform at scale. Build with production quality, cost efficiency, and exceptional UX.** 💪🤖
