# Wagner Coach - AI-Powered Fitness & Nutrition Platform

> **Revolutionary multimodal AI coaching that understands your fitness journey through text, voice, and photos.**

![Status](https://img.shields.io/badge/status-MVP%20Development-yellow)
![Tech Stack](https://img.shields.io/badge/stack-Next.js%20%2B%20FastAPI%20%2B%20Supabase-blue)
![AI Models](https://img.shields.io/badge/AI-Claude%20%2B%20Groq%20%2B%20FREE%20Models-green)
![Cost](https://img.shields.io/badge/cost-%240.50%2Fuser%2Fmonth-success)

---

## 🚀 What is Wagner Coach?

Wagner Coach is an **AI-powered fitness and nutrition coaching platform** that provides personalized training and meal plans through intelligent, context-aware conversations. Unlike traditional apps that require manual data entry, Wagner Coach understands natural language, processes photos, and learns from voice input to make fitness tracking effortless.

### 🎯 Key Features

- **🤖 AI Coach**: Chat with an intelligent coach that remembers your entire fitness journey
- **📸 Quick Entry**: Log meals and workouts via text, voice, or photos in seconds
- **🏋️ AI Programs**: Get personalized 12-week programs tailored to your goals
- **🔍 Semantic Search**: Find anything in your history using natural language
- **📊 Smart Analytics**: AI-driven insights about your progress and patterns
- **⚡ Real-time Sync**: Connect with Strava and Garmin for automatic activity tracking

---

## 💡 What Makes Wagner Coach Different?

| Feature | MyFitnessPal | Noom | **Wagner Coach** |
|---------|--------------|------|------------------|
| Multimodal Input | ❌ | ❌ | ✅ Text + Voice + Photo |
| AI Coach with RAG | ❌ | ❌ | ✅ Full context awareness |
| Quick Entry (5 sec) | ❌ Manual | ❌ Manual | ✅ AI-powered |
| Cost per user/month | N/A | $59 | **$0.50** (95% cheaper) |
| Personalized Programs | ❌ | 💰 Premium | ✅ AI-generated free |
| Semantic Search | ❌ | ❌ | ✅ RAG-powered |

---

## 🏗️ Architecture

Wagner Coach uses a modern, scalable architecture:

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
│                    (Mobile / Web)                           │
└────────────────────────┬────────────────────────────────────┘
                         │
         ┌───────────────┴────────────────┐
         │                                │
         ▼                                ▼
┌──────────────────┐            ┌─────────────────┐
│   FRONTEND       │            │   BACKEND       │
│   Next.js 14     │◄──────────►│   FastAPI       │
│   Vercel         │   REST API │   Railway       │
└──────────────────┘            └────────┬────────┘
                                         │
                         ┌───────────────┴────────────────┐
                         │                                │
                         ▼                                ▼
                ┌─────────────────┐           ┌──────────────────┐
                │   SUPABASE      │           │   AI SERVICES    │
                │   PostgreSQL    │           │   Claude, Groq   │
                │   Auth, Storage │           │   FREE Models    │
                └─────────────────┘           └──────────────────┘
```

### Tech Stack

**Frontend** (`wagner-coach-clean/`)
- Next.js 14 (App Router)
- React 18
- TypeScript
- Tailwind CSS + shadcn/ui
- Supabase Auth

**Backend** (`wagner-coach-backend/`)
- FastAPI (Python 3.11)
- Pydantic for validation
- Supabase client
- Celery for background jobs
- Poetry for dependency management

**Database**
- Supabase PostgreSQL
- pgvector extension (for RAG)
- 40+ tables
- Row-level security (RLS)

**AI Services**
- **FREE Models**: Embeddings (sentence-transformers), Voice (Whisper)
- **Groq**: Quick entry text processing ($0.05/M tokens)
- **OpenRouter**: Image analysis ($0.50/M tokens)
- **Anthropic Claude**: Coach chat & programs ($3-15/M tokens)

---

## 📁 Repository Structure

This project uses a **multi-repository architecture**:

```
wagner_coach/                          # Root (this directory)
├── CLAUDE.md                          # Master development guide (READ FIRST!)
├── README.md                          # This file
├── docs/                              # Shared documentation
│   ├── architecture/                  # System architecture
│   ├── features/                      # Feature specifications
│   ├── database/                      # Database schemas
│   └── business/                      # Business & product docs
│
├── wagner-coach-backend/              # Backend API (separate git repo)
│   ├── CLAUDE.md                      # Backend development standards
│   ├── app/                           # FastAPI application
│   ├── migrations/                    # SQL migrations
│   └── tests/                         # Backend tests
│
└── wagner-coach-clean/                # Frontend (separate git repo)
    ├── CLAUDE.md                      # Frontend development standards
    ├── app/                           # Next.js pages
    ├── components/                    # React components
    └── lib/                           # API clients & utilities
```

### Why Separate Repos?

- **Independent deployment**: Backend (Railway) and Frontend (Vercel) deploy separately
- **Different tech stacks**: Python vs TypeScript
- **Team separation**: Backend and frontend developers can work independently
- **Versioning**: API can be versioned independently from UI

---

## 🚦 Getting Started

### Prerequisites

- **Node.js** 18+ (for frontend)
- **Python** 3.11+ (for backend)
- **Poetry** (Python dependency manager)
- **Supabase** account
- **API Keys**: Claude, Groq, OpenRouter (optional: OpenAI)

### Quick Setup

#### 1. Clone the Repos

```bash
cd Projects/wagner_coach

# Frontend already cloned as wagner-coach-clean/
# Backend already cloned as wagner-coach-backend/
```

#### 2. Setup Backend

```bash
cd wagner-coach-backend

# Install dependencies
pip install poetry
poetry install

# Setup environment
cp .env.example .env
# Edit .env with your API keys

# Run migrations
supabase db push

# Start server
poetry run uvicorn app.main:app --reload

# Backend runs at http://localhost:8000
# API docs at http://localhost:8000/docs
```

#### 3. Setup Frontend

```bash
cd ../wagner-coach-clean

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
# Edit .env.local with your Supabase credentials

# Start development server
npm run dev

# Frontend runs at http://localhost:3000
```

#### 4. Test the Stack

1. Open http://localhost:3000
2. Create an account
3. Try Quick Entry (text, voice, or photo)
4. Chat with the AI coach
5. Generate a personalized program

---

## 📖 Documentation

### For Developers

**START HERE**: Read `CLAUDE.md` in this directory - it's the master guide that explains how everything works together.

Then read the specific CLAUDE.md for your work:
- **Backend work**: `wagner-coach-backend/CLAUDE.md`
- **Frontend work**: `wagner-coach-clean/CLAUDE.md`

### Key Documents

- **Architecture**: `docs/architecture/COMPLETE_APP_ANALYSIS.md` - Complete system analysis
- **Features**: `docs/features/` - Feature specifications and implementation guides
- **Database**: `docs/database/ACTUAL_SCHEMA_ANALYSIS.md` - Database schema documentation

### API Documentation

- **Backend API**: http://localhost:8000/docs (FastAPI auto-generated docs)
- **Supabase API**: https://supabase.com/dashboard/project/YOUR_PROJECT/api

---

## 🧪 Testing

### Backend Tests

```bash
cd wagner-coach-backend

# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html

# Run specific test
poetry run pytest tests/unit/test_coach_service.py -v
```

### Frontend Tests

```bash
cd wagner-coach-clean

# Run all tests
npm test

# Run with coverage
npm run test:coverage

# Run in watch mode
npm run test:watch
```

### E2E Tests

```bash
cd wagner-coach-clean

# Run Playwright tests
npm run test:e2e

# Run in UI mode
npm run test:e2e:ui
```

---

## 🚀 Deployment

### Backend (Railway)

```bash
cd wagner-coach-backend

# Install Railway CLI
npm i -g @railway/cli

# Login
railway login

# Deploy
railway up

# Deployed to: https://api.wagnercoach.com
```

### Frontend (Vercel)

```bash
cd wagner-coach-clean

# Install Vercel CLI
npm i -g vercel

# Deploy
vercel --prod

# Deployed to: https://wagnercoach.com
```

### Environment Variables

Both repos need environment variables set in their respective platforms:

**Backend (Railway)**:
- `SUPABASE_URL`, `SUPABASE_KEY`, `SUPABASE_SERVICE_KEY`
- `ANTHROPIC_API_KEY`, `GROQ_API_KEY`, `OPENROUTER_API_KEY`
- `JWT_SECRET`, `CRON_SECRET`, `WEBHOOK_SECRET`

**Frontend (Vercel)**:
- `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`
- `NEXT_PUBLIC_API_BASE_URL`, `NEXT_PUBLIC_APP_URL`

---

## 💰 Cost Analysis

Wagner Coach is designed to be **extremely cost-efficient** compared to competitors:

### Per User Per Month

| Service | Cost |
|---------|------|
| FREE Models (embeddings, transcription) | $0.00 |
| Groq (quick entry text) | $0.05 |
| OpenRouter (image processing) | $0.10 |
| Claude (coach chat, programs) | $0.35 |
| **Total** | **$0.50** |

### At Scale (10,000 users)

| Item | Cost |
|------|------|
| AI APIs | $5,000/month |
| Supabase | $1,000/month |
| Railway (backend) | $500/month |
| Vercel (frontend) | $200/month |
| **Total** | **$6,700/month** |

**Revenue (50% paid at $12/month)**: $60,000/month
**Gross Margin**: 88.8% 🚀

---

## 🗺️ Roadmap

### ✅ Phase 1: MVP (Complete)
- Core AI coach with RAG
- Quick entry (text, voice, photos)
- Manual logging
- Strava/Garmin sync
- Basic analytics

### 🚧 Phase 2: Engagement (In Progress)
- Daily nudges & reminders
- Streak tracking
- Weekly reports
- Progress photos comparison
- Goal milestones

### 📅 Phase 3: Intelligence (Next)
- Predictive meal suggestions
- Auto-program adjustments
- Pattern recognition
- Nutrition trend analysis
- PR tracking

### 🔮 Phase 4: Social (Future)
- Challenges & leaderboards
- Friend sharing
- Community feed
- Private groups

### 💎 Phase 5: Monetization (Future)
- Free tier: 10 coach msgs/week, basic logging
- Premium ($12/mo): Unlimited chat, programs, analytics
- Pro ($25/mo): Advanced analytics, API access
- Marketplace: User-generated programs

---

## 🤝 Contributing

### Development Workflow

1. **Read CLAUDE.md** - Master guide + repo-specific guide
2. **Create feature doc** in `docs/features/`
3. **Follow TDD** - Tests first, then implementation
4. **Test on mobile** - Real devices, not just browser
5. **Check accessibility** - Screen readers, keyboard nav
6. **Monitor AI costs** - Use cheapest model that works
7. **Deploy to staging** - Test before production
8. **Get code review** - At least one reviewer

### Code Standards

- **Backend**: Follow `wagner-coach-backend/CLAUDE.md`
- **Frontend**: Follow `wagner-coach-clean/CLAUDE.md`
- **Both**: 80%+ test coverage, TypeScript strict mode, production-level quality

---

## 📞 Support & Contact

- **Email**: renato@sharpened.me
- **Issues**: Create issues in respective repos
- **Documentation**: See `docs/` folder

---

## 📄 License

Private - Wagner Coach Fitness Application
© 2025 Renato Hugo

---

## 🎯 Vision

Wagner Coach aims to become **"The Perplexity of Fitness"** - an AI that understands your entire fitness journey and gives you answers before you ask. We're building the future of personalized health & fitness coaching, accessible to everyone at a fraction of the cost of traditional coaching.

**Built with Claude Code, powered by AI, designed for humans.** 💪🤖

---

## 📊 Current Status

- **Completion**: ~70% (infrastructure done, UX polish needed)
- **Users**: Pre-launch (testing with friends & family)
- **Features**: Core functionality working, engagement features in progress
- **Next Milestone**: MVP launch with 100 users

**Join us on this journey to revolutionize fitness coaching!** 🚀
