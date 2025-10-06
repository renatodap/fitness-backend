# Wagner Coach - Master Development Guide

**READ THIS FIRST before implementing ANY feature in the Wagner Coach fitness application.**

This is the master CLAUDE.md that coordinates all development across the Wagner Coach platform. Each repository has its own detailed CLAUDE.md with specific standards - this document explains how they work together.

---

## 🎯 Core Mission

Wagner Coach is a **revolutionary AI-powered fitness & nutrition coaching platform** with multimodal capabilities that surpass mainstream competitors. We combine:

- **Multimodal AI Input**: Text, voice, photos (Quick Entry)
- **RAG-Powered Coach**: Semantic search across ALL user data
- **Cost-Optimized AI**: 95% cheaper than competitors ($0.50/user/month)
- **Instant Personalization**: AI understands context from day 1

---

## 📁 Repository Structure

Wagner Coach uses a **multi-repository architecture** with 2 independent repos:

```
Projects/wagner_coach/                # Root coordination folder (this file)
├── CLAUDE.md                         # This master guide (READ FIRST)
├── README.md                         # Project overview
├── docs/                             # Shared documentation
│   ├── architecture/                 # System architecture docs
│   ├── features/                     # Feature specifications
│   ├── database/                     # Database schemas & analysis
│   └── business/                     # Business & product docs
│
├── wagner-coach-backend/             # Independent backend repo (Python/FastAPI)
│   ├── CLAUDE.md                     # Backend-specific standards (READ FOR BACKEND)
│   ├── app/                          # FastAPI application
│   ├── migrations/                   # SQL migrations
│   ├── tests/                        # Backend tests
│   └── ...
│
└── wagner-coach-clean/               # Independent frontend repo (Next.js/React)
    ├── CLAUDE.md                     # Frontend-specific standards (READ FOR FRONTEND)
    ├── app/                          # Next.js pages
    ├── components/                   # React components
    ├── lib/                          # API clients & utilities
    └── ...
```

### Why This Structure?

1. **Backend (Python/FastAPI)** - Separate repo for:
   - Independent deployment (Railway/Fly.io)
   - Different tech stack (Python vs TypeScript)
   - API versioning (can deploy backend without redeploying frontend)
   - Team separation (backend/frontend devs)

2. **Frontend (Next.js/React)** - Separate repo for:
   - Independent deployment (Vercel)
   - Fast iteration on UI
   - Different testing strategy
   - CDN optimization

3. **Database (Supabase)** - NOT a separate repo because:
   - Migrations live in backend repo (`wagner-coach-backend/migrations/`)
   - Backend owns the schema
   - Supabase provides RLS (no separate DB layer needed)
   - SQL files are versioned with backend code

4. **Root Coordination** - This folder for:
   - Master documentation
   - Architecture decisions
   - Feature specifications
   - Business/product docs

---

## 🚀 Quick Start Guide

### Which CLAUDE.md Should I Read?

**ALWAYS read this master CLAUDE.md first**, then:

| Working on...                    | Read this CLAUDE.md                          |
|----------------------------------|----------------------------------------------|
| Backend API, services, database  | `wagner-coach-backend/CLAUDE.md`            |
| Frontend UI, components, pages   | `wagner-coach-clean/CLAUDE.md`              |
| Architecture, features, planning | This file + `docs/` folder                  |
| New to project                   | Start here, then read both repo CLAUDE.md   |

### Development Workflow

1. **Read the master CLAUDE.md** (you're here! ✅)
2. **Check feature docs** in `docs/features/` to understand what exists
3. **Read the relevant repo CLAUDE.md** for specific standards
4. **Follow TDD** as defined in that repo's CLAUDE.md
5. **Test across the stack** (backend tests + frontend tests + integration)
6. **Deploy independently** (backend to Railway, frontend to Vercel)

---

## 🏗️ System Architecture

### High-Level Flow

```
User (Mobile/Web)
    ↓
Next.js Frontend (Vercel)
    ↓
FastAPI Backend (Railway)
    ↓
Supabase (Database + Auth + Storage)
    ↓
AI APIs (Claude, Groq, OpenRouter, FREE models)
```

### Key Components

#### 1. Frontend (Next.js)
- **Path**: `wagner-coach-clean/`
- **Tech**: Next.js 14, React, TypeScript, Tailwind, shadcn/ui
- **Deployment**: Vercel
- **Responsibilities**:
  - User interface & UX
  - Authentication UI (Supabase Auth)
  - Client-side state management
  - API calls to backend
  - Bottom navigation
  - Responsive design (mobile-first)

#### 2. Backend (FastAPI)
- **Path**: `wagner-coach-backend/`
- **Tech**: Python 3.11, FastAPI, Supabase, Pydantic
- **Deployment**: Railway or Fly.io
- **Responsibilities**:
  - RESTful API endpoints
  - AI processing (Coach, Quick Entry, Programs)
  - Database operations (via Supabase client)
  - Authentication validation (JWT)
  - Rate limiting
  - Background jobs (Celery)
  - Integrations (Strava, Garmin)

#### 3. Database (Supabase PostgreSQL)
- **Service**: Supabase (managed PostgreSQL)
- **Tech**: PostgreSQL 15, pgvector extension
- **Responsibilities**:
  - User data storage (40+ tables)
  - Row-level security (RLS)
  - Vector embeddings (multimodal RAG)
  - Real-time subscriptions
  - File storage (meal photos, audio)
  - Authentication (Supabase Auth)

#### 4. AI Services
- **FREE Models** (Hugging Face, local):
  - Text embeddings: `sentence-transformers/all-MiniLM-L6-v2`
  - Image embeddings: `openai/clip-vit-base-patch32`
  - Voice transcription: `openai/whisper-tiny`

- **Groq** ($0.05-0.10/M tokens):
  - Quick entry text processing: `llama-3.3-70b-versatile`
  - Meal parsing: `llama-3.3-70b-versatile`

- **OpenRouter** ($0.50-1.00/M tokens):
  - Quick entry image: `meta-llama/llama-4-scout`
  - Workout recommendations: `llama-3.1-70b`

- **Anthropic Claude** ($3-15/M tokens):
  - Coach chat: `claude-3-5-sonnet-20241022`
  - AI program generation: `claude-3-5-sonnet-20241022`

---

## 🔧 When to Work in Each Repo

### Work in Backend (`wagner-coach-backend/`) when:
- Creating new API endpoints
- Adding AI processing logic
- Modifying database schemas (migrations)
- Integrating external APIs (Strava, Garmin)
- Optimizing AI costs (model routing)
- Adding background jobs
- Implementing authentication logic
- **Always read**: `wagner-coach-backend/CLAUDE.md`

### Work in Frontend (`wagner-coach-clean/`) when:
- Creating new pages or UI components
- Improving user experience
- Adding client-side forms
- Implementing responsive designs
- Adding loading/error states
- Improving accessibility
- Optimizing performance (images, code splitting)
- **Always read**: `wagner-coach-clean/CLAUDE.md`

### Work in Both Repos when:
- Adding new features (API + UI)
- Changing data models (migration + TypeScript types)
- Updating authentication flow
- Adding new integrations
- **Read both CLAUDE.md files**

---

## 📋 Feature Implementation Checklist

When implementing a new feature (e.g., "Workout Progress Photos"):

### 1. Planning Phase
- [ ] Create feature doc: `docs/features/workout_progress_photos.md`
- [ ] Define user stories and flows
- [ ] Design database schema changes (if needed)
- [ ] Design API contracts (request/response)
- [ ] Design UI mockups
- [ ] Estimate AI costs (if using AI)

### 2. Backend Implementation
- [ ] Switch to backend repo: `cd wagner-coach-backend`
- [ ] Read backend CLAUDE.md
- [ ] Create migration (if schema changes): `migrations/XXX_add_progress_photos.sql`
- [ ] Write backend tests (TDD)
- [ ] Implement service layer
- [ ] Create API endpoints
- [ ] Add authentication & rate limiting
- [ ] Test with Postman/curl
- [ ] Deploy to staging (Railway)

### 3. Frontend Implementation
- [ ] Switch to frontend repo: `cd wagner-coach-clean`
- [ ] Read frontend CLAUDE.md
- [ ] Update TypeScript types
- [ ] Write component tests (TDD)
- [ ] Implement UI components
- [ ] Add API client functions
- [ ] Add loading & error states
- [ ] Test responsive design
- [ ] Test accessibility
- [ ] Deploy to staging (Vercel)

### 4. Integration Testing
- [ ] Test full user flow (UI → API → DB → UI)
- [ ] Verify mobile experience
- [ ] Check error handling
- [ ] Verify loading states
- [ ] Test with real data
- [ ] Get user feedback

### 5. Deployment
- [ ] Deploy backend to production
- [ ] Run database migrations
- [ ] Deploy frontend to production
- [ ] Monitor errors (Sentry)
- [ ] Monitor AI costs
- [ ] Update documentation

---

## 🗄️ Database Management

### Where Database Code Lives

**All database code lives in the backend repo** (`wagner-coach-backend/`):

```
wagner-coach-backend/
├── migrations/                       # SQL migration files
│   ├── 001_initial_schema.sql
│   ├── 002_add_rls_policies.sql
│   ├── 003_ai_generated_programs.sql
│   ├── 004_multimodal_vector.sql
│   └── current.sql                  # Complete current schema
└── docs/
    └── database/                    # Database documentation
        ├── schema.md
        └── rls_policies.md
```

### Why No Separate Database Repo?

1. **Tight Coupling**: Migrations depend on backend code
2. **Simplicity**: One less repo to manage
3. **Supabase**: Provides its own DB management tools
4. **RLS**: Row-level security is defined in SQL migrations
5. **Version Control**: Migrations are versioned with backend code

### Creating a New Migration

```bash
# 1. Create new migration file
cd wagner-coach-backend/migrations
touch 006_add_workout_photos.sql

# 2. Write migration (with UP and DOWN)
-- UP Migration
CREATE TABLE workout_progress_photos (...);
ALTER TABLE workout_progress_photos ENABLE ROW LEVEL SECURITY;
-- RLS policies...

# 3. Test migration locally
supabase db push

# 4. Update current.sql with complete schema
supabase db dump > migrations/current.sql

# 5. Commit to repo
git add migrations/
git commit -m "feat(db): add workout progress photos table"
```

---

## 🔐 Environment Variables

Each repo has its own `.env` file:

### Backend `.env` (`wagner-coach-backend/.env`)
```bash
# Supabase
SUPABASE_URL=xxx
SUPABASE_KEY=xxx
SUPABASE_SERVICE_KEY=xxx

# AI APIs
OPENAI_API_KEY=xxx
ANTHROPIC_API_KEY=xxx
GROQ_API_KEY=xxx
OPENROUTER_API_KEY=xxx

# Security
JWT_SECRET=xxx
CRON_SECRET=xxx
WEBHOOK_SECRET=xxx

# Optional
REDIS_URL=redis://localhost:6379
SENTRY_DSN=xxx
LOG_LEVEL=INFO
```

### Frontend `.env.local` (`wagner-coach-clean/.env.local`)
```bash
# Supabase (public keys only)
NEXT_PUBLIC_SUPABASE_URL=xxx
NEXT_PUBLIC_SUPABASE_ANON_KEY=xxx

# Backend API
NEXT_PUBLIC_API_BASE_URL=https://api.wagnercoach.com

# App URL
NEXT_PUBLIC_APP_URL=https://wagnercoach.com
```

**CRITICAL**: Never share service role keys with frontend!

---

## 🚀 Deployment Strategy

### Independent Deployments

Backend and frontend deploy **independently**:

```
Backend (Railway/Fly.io)
├── Domain: api.wagnercoach.com
├── Deploy: git push (auto-deploy on main)
├── Environment: Production
└── Health: /health endpoint

Frontend (Vercel)
├── Domain: wagnercoach.com
├── Deploy: git push (auto-deploy on main)
├── Environment: Production
└── Health: / (landing page)
```

### Deployment Order

When deploying breaking changes:

1. **Backend first**: Deploy API with backward compatibility
2. **Test**: Verify old frontend still works
3. **Frontend**: Deploy new frontend using new API
4. **Cleanup**: Remove deprecated API endpoints after 24 hours

### Rollback Strategy

- **Backend issue**: Roll back Railway deployment
- **Frontend issue**: Roll back Vercel deployment
- **Database issue**: Restore Supabase snapshot
- **Both repos broken**: Roll back both independently

---

## 💰 AI Cost Management

Wagner Coach targets **$0.50/user/month** for AI costs.

### Cost Breakdown (per user/month)
```
FREE Models (embeddings, transcription): $0.00
Groq (quick entry, parsing):             $0.05
OpenRouter (image processing):           $0.10
Claude (coach chat, programs):           $0.35
─────────────────────────────────────────────
Total:                                   $0.50
```

### Cost Optimization Rules

**ALWAYS use the cheapest model that produces acceptable results:**

1. **FREE first**: If a FREE model works, use it (embeddings, Whisper)
2. **Groq second**: For simple text tasks (parsing, extraction)
3. **OpenRouter third**: For medium complexity (image analysis)
4. **Claude last**: Only for complex reasoning (coach chat, programs)

### Monitoring Costs

- **Backend logs** all AI calls with cost estimates
- **Database** stores usage in `api_usage_logs` table
- **Monthly reports** aggregate costs per user
- **Alerts** trigger if user exceeds $1.00/month

---

## 🧪 Testing Strategy

### Unit Tests (Each Repo)
- **Backend**: `pytest` (80%+ coverage)
- **Frontend**: `Vitest` + React Testing Library (80%+ coverage)

### Integration Tests (Backend)
- API endpoint tests
- Database integration tests
- Mock external AI APIs

### E2E Tests (Frontend)
- Playwright for critical user flows:
  - Sign up → Onboarding → Dashboard
  - Quick Entry (text, voice, image)
  - Coach chat
  - Program generation

### Manual Testing Checklist
- [ ] Mobile (iOS Safari, Android Chrome)
- [ ] Tablet (iPad)
- [ ] Desktop (Chrome, Firefox, Safari)
- [ ] Accessibility (VoiceOver, NVDA)
- [ ] Lighthouse (Performance ≥90, Accessibility 100)

---

## 📚 Documentation Organization

```
docs/
├── architecture/                     # System design
│   ├── COMPLETE_APP_ANALYSIS.md     # Full app analysis
│   └── tech_stack.md
├── features/                         # Feature specs
│   ├── QUICK_ENTRY_*.md             # Quick Entry docs
│   ├── coach_chat.md
│   └── programs.md
├── database/                         # Database docs
│   ├── ACTUAL_SCHEMA_ANALYSIS.md
│   └── rls_policies.md
└── business/                         # Business docs
    ├── pricing.md
    └── roadmap.md
```

---

## 🎓 Onboarding New Developers

### Day 1: Setup
1. Read this CLAUDE.md
2. Read `docs/architecture/COMPLETE_APP_ANALYSIS.md`
3. Clone both repos
4. Set up local environment (backend + frontend)
5. Run tests in both repos

### Day 2: Backend
1. Read `wagner-coach-backend/CLAUDE.md`
2. Explore backend codebase
3. Run backend locally
4. Test API with Postman
5. Implement a small backend feature (with tests)

### Day 3: Frontend
1. Read `wagner-coach-clean/CLAUDE.md`
2. Explore frontend codebase
3. Run frontend locally
4. Implement a small UI component (with tests)
5. Test on mobile device

### Day 4-5: Full Feature
1. Pick a small feature from backlog
2. Implement backend (API + tests)
3. Implement frontend (UI + tests)
4. Deploy to staging
5. Get code review

---

## 🔥 Critical Production Standards

**EVERY feature must meet these standards across both repos:**

### 1. Security
- ✅ Authentication on protected endpoints (backend)
- ✅ Input validation (backend Pydantic, frontend Zod)
- ✅ RLS policies on database tables
- ✅ No sensitive data in frontend
- ✅ HTTPS only in production

### 2. User Experience
- ✅ Loading states on all async operations
- ✅ Error messages (user-friendly, actionable)
- ✅ Mobile responsive (320px to 1920px)
- ✅ Accessibility (WCAG AA)
- ✅ Keyboard navigation

### 3. Performance
- ✅ Lighthouse Performance ≥90
- ✅ API response time <500ms (non-AI)
- ✅ Images optimized (Next.js Image)
- ✅ Code splitting (dynamic imports)

### 4. Testing
- ✅ Backend: pytest coverage ≥80%
- ✅ Frontend: Vitest coverage ≥80%
- ✅ E2E tests for critical flows
- ✅ Manual testing on real devices

### 5. AI Cost Efficiency
- ✅ Use cheapest model that works
- ✅ Log all AI API calls with costs
- ✅ Monitor monthly costs per user
- ✅ Target: $0.50/user/month

### 6. Documentation
- ✅ Feature documented in `docs/features/`
- ✅ API endpoints documented (FastAPI auto-docs)
- ✅ TypeScript types defined
- ✅ README updated if needed

---

## 🚨 Common Pitfalls to Avoid

### 1. Database Schema Changes
❌ **DON'T**: Modify schema without migration
✅ **DO**: Create migration in backend repo first

### 2. Breaking API Changes
❌ **DON'T**: Change API contract without versioning
✅ **DO**: Add new endpoint `/v2/` or use optional fields

### 3. Hardcoded Values
❌ **DON'T**: Hardcode API URLs, secrets, config
✅ **DO**: Use environment variables

### 4. Expensive AI Models
❌ **DON'T**: Default to Claude for everything
✅ **DO**: Use cheapest model that produces good results

### 5. No Loading States
❌ **DON'T**: Leave users staring at blank screen
✅ **DO**: Show skeleton screens, spinners, progress

### 6. Poor Error Messages
❌ **DON'T**: "Error 500" or "Something went wrong"
✅ **DO**: "Failed to save meal. Please check your connection and try again."

### 7. Skipping Tests
❌ **DON'T**: "I'll add tests later"
✅ **DO**: Write tests FIRST (TDD)

### 8. Mobile Ignorance
❌ **DON'T**: Only test on desktop
✅ **DO**: Test on real mobile devices (iOS + Android)

---

## 📞 Getting Help

### Documentation
1. **Start here**: This CLAUDE.md
2. **Feature specs**: `docs/features/`
3. **Architecture**: `docs/architecture/COMPLETE_APP_ANALYSIS.md`
4. **Backend**: `wagner-coach-backend/CLAUDE.md`
5. **Frontend**: `wagner-coach-clean/CLAUDE.md`

### Code Examples
- **Backend patterns**: Look in `wagner-coach-backend/app/services/`
- **Frontend patterns**: Look in `wagner-coach-clean/components/`
- **API examples**: Check FastAPI docs at `/docs` endpoint
- **Database examples**: See `wagner-coach-backend/migrations/`

---

## ✅ Quick Decision Tree

**Use this when unsure where to start:**

```
Q: What are you implementing?

├─ New API endpoint or backend logic
│  └─ Work in: wagner-coach-backend/
│     └─ Read: wagner-coach-backend/CLAUDE.md
│
├─ New UI component or page
│  └─ Work in: wagner-coach-clean/
│     └─ Read: wagner-coach-clean/CLAUDE.md
│
├─ Database schema change
│  └─ Work in: wagner-coach-backend/migrations/
│     └─ Read: wagner-coach-backend/CLAUDE.md (Database section)
│
├─ Full feature (API + UI)
│  └─ Work in: Both repos
│     └─ Read: Both CLAUDE.md files
│        ├─ Start with backend (API first)
│        └─ Then frontend (UI consumes API)
│
└─ Architecture decision or planning
   └─ Create doc in: docs/architecture/ or docs/features/
      └─ Read: This file + docs/architecture/
```

---

## 🎯 Success Criteria

**A feature is production-ready when:**

1. ✅ **Backend** meets all standards in `wagner-coach-backend/CLAUDE.md`
2. ✅ **Frontend** meets all standards in `wagner-coach-clean/CLAUDE.md`
3. ✅ **Tests pass** in both repos (≥80% coverage)
4. ✅ **Works on mobile** (real device testing)
5. ✅ **Accessible** (WCAG AA, screen reader tested)
6. ✅ **Cost-efficient** (using cheapest AI models)
7. ✅ **Documented** (feature doc + code comments)
8. ✅ **Deployed** (staging first, then production)
9. ✅ **Monitored** (no errors in Sentry, costs within budget)
10. ✅ **User-tested** (at least 5 users tried it)

**If you can confidently answer "yes" to all 10, ship it!** 🚀

---

## 🧭 Remember

- **Read this master CLAUDE.md first**, always
- **Then read the repo-specific CLAUDE.md** for detailed standards
- **Follow TDD** in both repos
- **Test on mobile** (real devices)
- **Optimize AI costs** (cheapest model first)
- **Document everything** (code + feature docs)
- **Deploy independently** (backend and frontend)
- **Monitor production** (errors + costs)

---

**Wagner Coach is not just a fitness app - it's a platform for AI-powered coaching at scale. Build accordingly.** 💪🤖
