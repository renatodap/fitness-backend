# Fitness Backend

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
