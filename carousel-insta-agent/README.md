# Instagram Carousel AI Agent

> **Production-ready AI system for automated Instagram carousel generation focused on AI content**

## 🎯 Overview

This system automatically generates high-quality Instagram carousels by:
- Researching trending AI topics using Perplexity, Reddit, and Twitter APIs
- Creating engaging copy with Claude AI
- Generating professional visuals with DALL-E 3
- Publishing and tracking performance via Instagram Graph API

**Cost per carousel**: ~$2.60-3.00 | **Time to generate**: 5-10 minutes

## 🏗️ Architecture

### Backend (Python FastAPI)
- **Research Layer**: Trend analysis, topic research, competitor analysis
- **Content Layer**: AI-powered copywriting, outline generation, caption creation
- **Visual Layer**: Image generation, composition, design systems
- **Publishing Layer**: Instagram integration, scheduling, analytics
- **Database**: Supabase (PostgreSQL with RLS)

### Frontend (Next.js 14)
- **Dashboard**: Carousel creation wizard with real-time progress
- **Preview System**: Interactive carousel editing before publishing
- **Analytics**: Performance tracking, A/B testing, content calendar
- **Content Library**: Historical carousels, templates, series planning

## 🚀 Quick Start

### Prerequisites
```bash
- Python 3.11+
- Node.js 18+
- Supabase account
- API keys: Anthropic, OpenAI, Perplexity, Instagram
```

### Setup

1. **Clone and install backend**
```bash
cd backend
poetry install
cp .env.example .env
# Add your API keys to .env
```

2. **Setup frontend**
```bash
cd frontend
npm install
cp .env.local.example .env.local
# Add your environment variables
```

3. **Run database migrations**
```bash
cd backend
poetry run alembic upgrade head
```

4. **Start development servers**
```bash
# Terminal 1 - Backend
cd backend
poetry run uvicorn app.main:app --reload

# Terminal 2 - Frontend
cd frontend
npm run dev

# Terminal 3 - Background workers
cd backend
poetry run celery -A app.workers.celery_app worker --loglevel=info
```

Access the app at `http://localhost:3000`

## 📁 Project Structure

```
carousel-insta-agent/
├── backend/                    # FastAPI Python backend
│   ├── app/
│   │   ├── api/v1/            # API endpoints
│   │   │   ├── carousels.py   # Carousel CRUD & generation
│   │   │   ├── research.py    # Research endpoints
│   │   │   ├── analytics.py   # Performance tracking
│   │   │   └── instagram.py   # Instagram publishing
│   │   ├── services/          # Core business logic
│   │   │   ├── research/      # Topic research, trend analysis
│   │   │   ├── content/       # Copywriting, outline generation
│   │   │   ├── visual/        # Image generation, composition
│   │   │   ├── publishing/    # Instagram integration
│   │   │   └── analytics/     # Performance tracking
│   │   ├── models/            # Pydantic models
│   │   ├── core/              # Config, security, logging
│   │   └── workers/           # Celery background tasks
│   ├── tests/                 # Pytest suite (80%+ coverage)
│   ├── migrations/            # Database migrations
│   ├── scripts/               # Utility scripts
│   └── pyproject.toml         # Python dependencies
├── frontend/                  # Next.js 14 TypeScript app
│   ├── app/                   # App router pages
│   │   ├── dashboard/         # Main dashboard
│   │   ├── create/            # Carousel creation wizard
│   │   ├── analytics/         # Performance analytics
│   │   └── calendar/          # Content calendar
│   ├── components/            # React components
│   │   ├── carousel/          # Carousel preview, editor
│   │   ├── ui/                # shadcn/ui components
│   │   └── dashboard/         # Dashboard widgets
│   ├── lib/                   # Utilities, API client
│   └── public/                # Static assets
├── docs/                      # Documentation
│   ├── api/                   # API documentation
│   ├── design/                # Design decisions
│   └── deployment/            # Deployment guides
└── docker-compose.yml         # Local development setup
```

## 🎨 Features

### Core Functionality
- ✅ **Automated Research**: Perplexity API + Reddit/Twitter scraping
- ✅ **AI Copywriting**: Claude-powered hooks, captions, slide copy
- ✅ **Visual Generation**: DALL-E 3 image creation with consistent branding
- ✅ **Quality Validation**: Fact-checking, accessibility, readability
- ✅ **Instagram Publishing**: Graph API integration with scheduling
- ✅ **Performance Analytics**: Real-time tracking of engagement metrics

### Advanced Features
- 🔄 **A/B Testing**: Generate variants for hooks, visuals, CTAs
- 📊 **Predictive Analytics**: Engagement forecasting before posting
- 🎯 **Content Series**: Multi-part carousel planning
- 📱 **Cross-Platform**: Repurpose for LinkedIn, Twitter, TikTok
- 🎬 **Supplementary Content**: Auto-generate Story teasers and Reels
- 🤖 **Learning System**: Improves from historical performance data

## 💻 Usage

### Create a Carousel

```python
# Backend API
POST /api/v1/carousels/generate
{
    "topic": "How embeddings work in AI",
    "carousel_type": "technical_explainer",
    "slide_count": 8,
    "auto_publish": false,
    "generate_variants": true
}

# Response (after 5-10 minutes)
{
    "carousel_id": "uuid",
    "status": "completed",
    "slides": [...],
    "caption": "...",
    "predicted_engagement": {
        "impressions": 3200,
        "saves": 280,
        "shares": 45
    },
    "variants": [...],
    "optimal_posting_time": "2025-10-10T19:15:00Z"
}
```

### Via Frontend Dashboard
1. Navigate to `/create`
2. Enter topic and select carousel type
3. Watch real-time generation progress
4. Review and edit generated carousel
5. Schedule or publish immediately
6. Track performance in `/analytics`

## 🔧 Configuration

### Environment Variables

**Backend (.env)**
```bash
# Supabase
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key

# AI APIs
ANTHROPIC_API_KEY=your_anthropic_key
OPENAI_API_KEY=your_openai_key
PERPLEXITY_API_KEY=your_perplexity_key

# Instagram
INSTAGRAM_APP_ID=your_instagram_app_id
INSTAGRAM_APP_SECRET=your_instagram_app_secret
INSTAGRAM_ACCESS_TOKEN=your_long_lived_token

# Optional
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_secret
TWITTER_BEARER_TOKEN=your_twitter_bearer_token

# Infrastructure
REDIS_URL=redis://localhost:6379
SENTRY_DSN=your_sentry_dsn (optional)
LOG_LEVEL=INFO
```

**Frontend (.env.local)**
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

## 📊 Cost Breakdown

Per carousel (8 slides):
- **Research** (Perplexity): $0.30
- **Copywriting** (Claude Sonnet): $1.50
- **Images** (DALL-E 3): $0.80
- **Total**: **$2.60-3.00**

At 5 carousels/week: **$50-60/month**

## 🧪 Testing

```bash
# Backend tests
cd backend
poetry run pytest --cov=app --cov-report=html

# Frontend tests
cd frontend
npm run test
npm run test:e2e
```

**Target coverage**: ≥80%

## 🚢 Deployment

### Railway (Recommended)
```bash
# Backend
railway up --service backend

# Frontend
railway up --service frontend

# Workers
railway up --service workers
```

### Docker
```bash
docker-compose up -d
```

See `docs/deployment/` for detailed guides.

## 📈 Performance Targets

- **Generation time**: < 10 minutes per carousel
- **API response**: < 500ms (non-AI endpoints)
- **Uptime**: 99.9%
- **Test coverage**: ≥80%
- **Cost per carousel**: < $3.50

## 🛠️ Development

### Backend Development
```bash
# Run with auto-reload
poetry run uvicorn app.main:app --reload --log-level debug

# Run tests
poetry run pytest -v

# Lint and format
poetry run ruff check app/
poetry run black app/
poetry run mypy app/
```

### Frontend Development
```bash
# Development server
npm run dev

# Build
npm run build

# Lint
npm run lint
```

## 📚 Documentation

- [API Documentation](docs/api/README.md) - Complete API reference
- [Service Architecture](docs/design/ARCHITECTURE.md) - System design
- [Deployment Guide](docs/deployment/README.md) - Production deployment
- [Contributing](docs/CONTRIBUTING.md) - Contribution guidelines

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Follow the coding standards in `CLAUDE.md`
4. Write tests (maintain ≥80% coverage)
5. Commit with conventional commits
6. Push and create a Pull Request

## 📝 License

MIT License - see LICENSE file for details

## 🙏 Acknowledgments

- Anthropic (Claude AI)
- OpenAI (DALL-E 3)
- Perplexity AI
- Supabase

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/carousel-insta-agent/issues)
- **Docs**: [Documentation](docs/)
- **Email**: support@yourproject.com

---

**Built with production-level standards** | Following Wagner Coach Backend guidelines
