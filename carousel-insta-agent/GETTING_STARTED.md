# Getting Started with Carousel Instagram Agent

## Quick Start (5 minutes)

### Prerequisites

- Python 3.11+
- Node.js 18+
- PostgreSQL (via Supabase)
- Redis (for Celery)
- API Keys:
  - Anthropic (Claude)
  - OpenAI (DALL-E 3)
  - Perplexity
  - Instagram Graph API
  - Reddit (optional)
  - Twitter (optional)

### 1. Clone and Setup

```bash
git clone https://github.com/yourusername/carousel-insta-agent.git
cd carousel-insta-agent
```

### 2. Backend Setup

```bash
cd backend

# Install dependencies
poetry install

# Copy environment template
cp .env.example .env

# Edit .env with your API keys
nano .env  # or use your preferred editor

# Run database migrations
poetry run alembic upgrade head

# Start backend
poetry run uvicorn app.main:app --reload
```

Backend will run at `http://localhost:8000`

### 3. Start Redis (for background tasks)

```bash
# Using Docker
docker run -d -p 6379:6379 redis:7-alpine

# Or install Redis locally
# macOS: brew install redis && brew services start redis
# Linux: sudo apt-get install redis-server && sudo service redis-server start
```

### 4. Start Celery Worker

```bash
cd backend
poetry run celery -A app.workers.celery_app worker --loglevel=info
```

### 5. Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.local.example .env.local

# Edit .env.local
nano .env.local

# Start development server
npm run dev
```

Frontend will run at `http://localhost:3000`

### 6. Create Your First Carousel

1. Open http://localhost:3000
2. Click "Get Started"
3. Click "New Carousel"
4. Enter topic: "How vector embeddings work in AI"
5. Select type: "Concept Explainer"
6. Click "Generate Carousel"
7. Wait 5-10 minutes for generation
8. Review and publish!

## Using Docker (Alternative)

```bash
# Start all services with Docker Compose
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Environment Variables Reference

### Backend (.env)

**Required:**
- `SUPABASE_URL` - Your Supabase project URL
- `SUPABASE_KEY` - Supabase anon key
- `SUPABASE_SERVICE_KEY` - Supabase service role key
- `ANTHROPIC_API_KEY` - Claude API key
- `OPENAI_API_KEY` - OpenAI API key
- `PERPLEXITY_API_KEY` - Perplexity API key
- `INSTAGRAM_APP_ID` - Instagram app ID
- `INSTAGRAM_APP_SECRET` - Instagram app secret
- `INSTAGRAM_ACCESS_TOKEN` - Long-lived access token
- `INSTAGRAM_BUSINESS_ACCOUNT_ID` - Your Instagram business account ID
- `JWT_SECRET` - Random 32+ character string

**Optional:**
- `REDDIT_CLIENT_ID` - Reddit app client ID
- `REDDIT_CLIENT_SECRET` - Reddit app secret
- `TWITTER_BEARER_TOKEN` - Twitter API bearer token
- `SENTRY_DSN` - Sentry error tracking DSN

### Frontend (.env.local)

```bash
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
```

## Database Setup

### Option 1: Supabase (Recommended)

1. Create account at https://supabase.com
2. Create new project
3. Copy connection details
4. Run migrations:

```bash
cd backend/migrations
psql $DATABASE_URL < 001_initial_schema.sql
```

### Option 2: Local PostgreSQL

```bash
# Create database
createdb carousel_agent

# Run migrations
psql carousel_agent < backend/migrations/001_initial_schema.sql
```

## API Keys Setup

### Anthropic (Claude)

1. Visit https://console.anthropic.com
2. Create API key
3. Copy to `ANTHROPIC_API_KEY`

### OpenAI (DALL-E 3)

1. Visit https://platform.openai.com
2. Create API key
3. Copy to `OPENAI_API_KEY`

### Perplexity

1. Visit https://www.perplexity.ai/settings/api
2. Create API key
3. Copy to `PERPLEXITY_API_KEY`

### Instagram Graph API

**This is the most complex setup:**

1. Create Meta App at https://developers.facebook.com
2. Add Instagram Basic Display product
3. Configure OAuth redirect: `https://yourdomain.com/auth/instagram/callback`
4. Get long-lived access token
5. Convert to never-expiring token
6. Get Instagram Business Account ID

Detailed guide: https://developers.facebook.com/docs/instagram-api/getting-started

### Reddit (Optional)

1. Visit https://www.reddit.com/prefs/apps
2. Create app (script type)
3. Copy client ID and secret

### Twitter (Optional)

1. Visit https://developer.twitter.com
2. Create project and app
3. Enable API v2
4. Copy bearer token

## Troubleshooting

### Backend won't start

```bash
# Check Python version
python --version  # Must be 3.11+

# Reinstall dependencies
poetry install --no-cache

# Check environment variables
poetry run python -c "from app.config import settings; print(settings.SUPABASE_URL)"
```

### Celery worker issues

```bash
# Check Redis connection
redis-cli ping  # Should return PONG

# Reset Celery
poetry run celery -A app.workers.celery_app purge
```

### Frontend build errors

```bash
# Clear cache and reinstall
rm -rf node_modules .next
npm install
npm run build
```

### Database connection errors

```bash
# Test Supabase connection
curl $SUPABASE_URL/rest/v1/ -H "apikey: $SUPABASE_KEY"
```

## Next Steps

1. **Customize Design Templates**: Visit `/templates` to create custom brand designs
2. **Set Up Instagram**: Connect your Instagram business account
3. **Schedule Posts**: Use the scheduling feature for optimal posting times
4. **Monitor Analytics**: Track performance in `/analytics`
5. **API Documentation**: Visit http://localhost:8000/docs

## Production Deployment

See `docs/deployment/README.md` for production deployment guides for:
- Railway
- Fly.io
- Vercel
- AWS
- GCP

## Support

- **Documentation**: See `/docs` directory
- **Issues**: https://github.com/yourusername/carousel-insta-agent/issues
- **Discussions**: https://github.com/yourusername/carousel-insta-agent/discussions

---

**You're ready to create viral AI carousels!** 🚀
