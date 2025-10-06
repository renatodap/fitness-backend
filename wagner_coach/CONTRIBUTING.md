# Contributing to Wagner Coach

Thank you for your interest in contributing to Wagner Coach! This document provides guidelines and workflows for contributing to the project.

---

## 🎯 Before You Start

### Required Reading

1. **`CLAUDE.md`** (this directory) - Master development guide **[READ FIRST!]**
2. **Backend work**: `wagner-coach-backend/CLAUDE.md`
3. **Frontend work**: `wagner-coach-clean/CLAUDE.md`
4. **Architecture**: `docs/architecture/COMPLETE_APP_ANALYSIS.md`

**These documents define production-level standards that ALL code must meet.**

---

## 🏗️ Repository Structure

Wagner Coach uses a **multi-repository architecture**:

```
wagner_coach/                   # Root (this directory)
├── wagner-coach-backend/       # Python/FastAPI backend
└── wagner-coach-clean/         # Next.js/React frontend
```

Each repository can be deployed independently.

---

## 🚀 Getting Started

### 1. Setup Development Environment

#### Backend Setup
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

# Start development server
poetry run uvicorn app.main:app --reload
```

#### Frontend Setup
```bash
cd wagner-coach-clean

# Install dependencies
npm install

# Setup environment
cp .env.example .env.local
# Edit .env.local with your Supabase credentials

# Start development server
npm run dev
```

### 2. Verify Setup

- Backend: http://localhost:8000/docs
- Frontend: http://localhost:3000
- Database: Supabase dashboard

---

## 📝 Development Workflow

### For Every Feature

Follow the **7-step TDD process** defined in `CLAUDE.md`:

1. **Feature Design** - Create `docs/design/{feature}.md`
2. **Test Design** - Create `docs/testing/{feature}_test.md`
3. **Code Design** - Define types/interfaces/models
4. **Test Implementation** - Write tests FIRST
5. **Feature Implementation** - Implement until tests pass
6. **Validation** - Run linters, coverage, manual testing
7. **UI Verification** (frontend only) - Verify accessibility, responsive design

### Example: Adding a New Feature

```bash
# 1. Create feature documentation
docs/features/workout_photos.md

# 2. Backend work
cd wagner-coach-backend

# Create migration if needed
touch migrations/007_add_workout_photos.sql

# Write tests first
touch tests/unit/test_workout_photos.py

# Implement feature
touch app/services/workout_photos_service.py
touch app/api/v1/workout_photos.py

# Run tests
poetry run pytest --cov=app

# 3. Frontend work
cd ../wagner-coach-clean

# Write tests first
touch __tests__/components/WorkoutPhotos.test.tsx

# Implement feature
touch components/WorkoutPhotos/PhotoUpload.tsx
touch lib/api/workout-photos.ts

# Run tests
npm test

# 4. Integration testing
# Test full flow: UI → API → DB → UI

# 5. Deploy to staging
# Backend first, then frontend
```

---

## ✅ Code Quality Standards

### All Code Must Meet These Standards:

#### Backend (Python/FastAPI)
- [ ] Type hints on all functions
- [ ] Docstrings (Google style)
- [ ] Pydantic models for validation
- [ ] Tests with ≥80% coverage
- [ ] Passes `ruff check` and `black`
- [ ] Passes `mypy` type checking
- [ ] Error handling with custom exceptions
- [ ] Structured logging
- [ ] No hardcoded secrets

#### Frontend (Next.js/React)
- [ ] TypeScript strict mode
- [ ] No `any` types
- [ ] Component tests with ≥80% coverage
- [ ] Passes ESLint
- [ ] Responsive design (mobile, tablet, desktop)
- [ ] Accessible (WCAG AA)
- [ ] Loading states on all async operations
- [ ] User-friendly error messages
- [ ] Lighthouse Performance ≥90

#### Both
- [ ] Follows TDD (tests written first)
- [ ] Production-ready (ready for real users)
- [ ] Documentation updated
- [ ] No functionality changes unless explicitly required

---

## 🧪 Testing Requirements

### Backend Tests
```bash
cd wagner-coach-backend

# Run all tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=app --cov-report=html --cov-report=term-missing

# Coverage must be ≥80%
```

### Frontend Tests
```bash
cd wagner-coach-clean

# Run unit tests
npm test

# Run with coverage
npm run test:coverage

# Run E2E tests
npm run test:e2e

# Coverage must be ≥80%
```

---

## 🔐 Security Guidelines

### Environment Variables
- **NEVER** commit `.env` or `.env.local` files
- **ALWAYS** use `.env.example` template
- **VALIDATE** all env vars on startup
- **MASK** sensitive values in logs

### API Security
- **ALWAYS** validate inputs with Pydantic (backend) or Zod (frontend)
- **ALWAYS** use JWT authentication on protected endpoints
- **ALWAYS** implement rate limiting on AI endpoints
- **ALWAYS** use Supabase RLS policies
- **NEVER** trust client-side validation alone

### Secrets Management
- **Backend**: Use environment variables, never hardcode
- **Frontend**: Only use `NEXT_PUBLIC_` for safe-to-expose values
- **Production**: Store secrets in Railway/Vercel, not in code

---

## 💰 AI Cost Management

Wagner Coach targets **$0.50/user/month** for AI costs.

### Model Selection Priority
1. **FREE models** first (embeddings, Whisper)
2. **Groq** for simple tasks ($0.05/M tokens)
3. **OpenRouter** for medium tasks ($0.50/M tokens)
4. **Claude** for complex tasks ($3-15/M tokens)

### Required
- **Log all AI calls** with cost estimates
- **Monitor costs** in database (`api_usage_logs`)
- **Optimize prompts** for token efficiency
- **Use caching** where possible (Claude prompt caching)

---

## 📋 Pull Request Process

### Before Submitting

1. **Read CLAUDE.md** - Ensure compliance with standards
2. **Run tests** - Backend and frontend (≥80% coverage)
3. **Run linters** - Fix all errors
4. **Manual testing** - Test on real mobile device
5. **Accessibility** - Test with screen reader
6. **Documentation** - Update relevant docs

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Checklist
- [ ] Tests pass (≥80% coverage)
- [ ] Linters pass (ruff, eslint)
- [ ] Mobile tested (real device)
- [ ] Accessible (WCAG AA)
- [ ] Documentation updated
- [ ] CLAUDE.md standards met

## Testing
How was this tested?

## Screenshots (if UI changes)
```

### Review Process

1. **Self-review** - Check your own code first
2. **Automated checks** - Tests, linters, coverage
3. **Code review** - At least one reviewer
4. **Testing review** - Verify tests are comprehensive
5. **Deploy to staging** - Test in staging environment
6. **Final approval** - Merge to main

---

## 🚀 Deployment

### Staging
- **Backend**: Push to `staging` branch
- **Frontend**: Push to `staging` branch
- Test thoroughly before production

### Production
- **Backend first**: Deploy backend with backward compatibility
- **Test**: Verify old frontend still works
- **Frontend**: Deploy frontend using new API
- **Monitor**: Check Sentry for errors, monitor AI costs

---

## 🐛 Bug Reports

### Include
- **Environment**: Development/Staging/Production
- **Steps to reproduce**
- **Expected behavior**
- **Actual behavior**
- **Screenshots** (if applicable)
- **Browser/Device** (if frontend)
- **Error logs** (check Sentry)

---

## 💡 Feature Requests

### Include
- **User story**: As a [role], I want [feature] so that [benefit]
- **Use cases**: Specific scenarios
- **Design mockups**: If UI changes
- **API contracts**: If new endpoints
- **Database changes**: If schema changes
- **AI cost estimate**: If using AI
- **Priority**: Critical/High/Medium/Low

---

## 🎓 Learning Resources

### For New Contributors

1. **FastAPI**: https://fastapi.tiangolo.com/
2. **Next.js**: https://nextjs.org/docs
3. **Supabase**: https://supabase.com/docs
4. **Testing**:
   - Backend: https://docs.pytest.org/
   - Frontend: https://testing-library.com/
5. **Accessibility**: https://www.w3.org/WAI/WCAG21/quickref/

---

## 📞 Questions?

- **Documentation**: Read `CLAUDE.md` files first
- **Architecture**: See `docs/architecture/`
- **Features**: See `docs/features/`
- **Contact**: renato@sharpened.me

---

## ⚖️ License

Private - Wagner Coach Fitness Application
© 2025 Renato Hugo

---

## 🙏 Thank You!

Your contributions help make Wagner Coach the best AI-powered fitness platform. We appreciate your adherence to production-level standards and commitment to quality.

**Happy coding!** 💪🤖
