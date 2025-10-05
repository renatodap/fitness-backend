# Security Policy - Wagner Coach Backend

This document outlines security policies and best practices for the Wagner Coach backend.

---

## 🔐 Security Standards

### Authentication & Authorization
- ✅ JWT tokens for API authentication
- ✅ Supabase RLS (Row-Level Security) for database access
- ✅ Service role key only used server-side
- ✅ Rate limiting on all AI endpoints

### Data Protection
- ✅ All sensitive data encrypted in transit (HTTPS)
- ✅ Passwords never stored (Supabase Auth handles this)
- ✅ API keys masked in logs
- ✅ User data isolated by user_id (RLS policies)

### Input Validation
- ✅ Pydantic models validate all API inputs
- ✅ SQL injection prevented (Supabase client uses parameterized queries)
- ✅ XSS prevention (API returns JSON, not HTML)
- ✅ File upload validation (size, type, content)

---

## ⚠️ Production Security Checklist

### Before Deploying to Production

#### Environment Variables
- [ ] `ENVIRONMENT=production`
- [ ] `DEBUG=false`
- [ ] `ALLOW_ALL_ORIGINS=false`
- [ ] `CORS_ORIGINS` set to specific frontend domain(s)
- [ ] `JWT_SECRET` is strong (min 32 characters, generated with `openssl rand -hex 32`)
- [ ] `CRON_SECRET` is unique (generated with `openssl rand -hex 16`)
- [ ] `WEBHOOK_SECRET` is unique (generated with `openssl rand -hex 16`)
- [ ] All API keys are production keys (not test/dev keys)

#### API Configuration
- [ ] API docs disabled in production (`docs_url=None`)
- [ ] HTTPS enforced (Railway/Fly.io handles this)
- [ ] Rate limiting configured on all AI endpoints
- [ ] CORS restricted to specific origins

#### Database
- [ ] Supabase RLS enabled on all tables
- [ ] Service role key never exposed to clients
- [ ] Database backups configured
- [ ] Connection pooling configured

#### Monitoring
- [ ] Sentry configured for error tracking
- [ ] Structured logging enabled
- [ ] Health check endpoint working (`/health`)
- [ ] API usage logs being written

---

## 🚨 Known Security Considerations

### ALLOW_ALL_ORIGINS Flag
**Status**: ✅ FIXED - Now disabled by default

**Risk**: Allows requests from any origin (CORS bypass)

**Mitigation**:
- Default value changed to `False` in `app/config.py`
- Backend logs warning when enabled
- `.env.example` includes deployment checklist
- Must explicitly set to `true` in development if needed

**Configuration**:
```bash
# In .env (development)
ALLOW_ALL_ORIGINS=false  # Default is False
CORS_ORIGINS=http://localhost:3000,https://wagnercoach.com

# In production
ALLOW_ALL_ORIGINS=false  # MUST be False
CORS_ORIGINS=https://wagnercoach.com,https://www.wagnercoach.com
```

### API Keys in Environment Variables
**Status**: ✅ Properly handled

**Implementation**:
- All API keys loaded from environment variables
- Never hardcoded in source code
- Masked in logs and API responses
- `.env` file in `.gitignore`

### Rate Limiting
**Status**: ✅ IMPLEMENTED

**Implementation**: Redis-based sliding window rate limiter

**Applied To**:
- Coach chat endpoints: 100 messages/day per user
- Quick entry endpoints: 200 entries/day per user
- Program generation: 5 programs/month per user

**How It Works**:
```python
from app.api.middleware.rate_limit import coach_chat_rate_limit

@router.post("/chat")
@coach_chat_rate_limit()
async def chat_with_coach(request: ChatRequest, current_user: dict = Depends(get_current_user)):
    # Endpoint automatically rate-limited
    pass
```

**Rate Limits**:
| Endpoint | Limit | Window | Key |
|----------|-------|--------|-----|
| Coach Chat | 100 requests | 24 hours | `coach_chat:{user_id}` |
| Quick Entry (Text) | 200 requests | 24 hours | `quick_entry:{user_id}` |
| Quick Entry (Multimodal) | 200 requests | 24 hours | `quick_entry:{user_id}` |
| Program Generation | 5 requests | 30 days | `program_generation:{user_id}` |

**Error Response** (429 Too Many Requests):
```json
{
  "error": "Rate limit exceeded",
  "message": "You have exceeded the rate limit of 100 requests per 24 hour(s). Please try again later.",
  "retry_after": 3600,
  "limit": 100,
  "window": 86400
}
```

**Testing**:
```bash
poetry run pytest tests/unit/test_rate_limit.py -v
```

---

## 🔒 Supabase RLS Policies

All database tables MUST have RLS enabled with appropriate policies.

### User Tables (profiles, user_preferences, etc.)
```sql
-- Users can only view/edit their own data
CREATE POLICY "Users can view own data"
ON table_name FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can update own data"
ON table_name FOR UPDATE
USING (auth.uid() = user_id);
```

### Content Tables (meals, workouts, activities, etc.)
```sql
-- Users can only view/edit their own content
CREATE POLICY "Users can view own content"
ON table_name FOR SELECT
USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own content"
ON table_name FOR INSERT
WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own content"
ON table_name FOR UPDATE
USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own content"
ON table_name FOR DELETE
USING (auth.uid() = user_id);
```

### Verify RLS
```bash
# Check all tables have RLS enabled
supabase db dump --schema public | grep "ENABLE ROW LEVEL SECURITY"

# Should see output for every table
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE meals ENABLE ROW LEVEL SECURITY;
# etc.
```

---

## 🛡️ API Security Headers

### Required Headers (Handled by FastAPI/Railway)
```python
# HTTPS enforced by hosting platform
# Content-Security-Policy: handled by client
# X-Content-Type-Options: nosniff (FastAPI default)
# X-Frame-Options: DENY (FastAPI default)
```

### CORS Configuration
```python
# Production settings
CORS_ORIGINS=https://wagnercoach.com
ALLOW_ALL_ORIGINS=false
```

---

## 🔑 Secrets Management

### Development
- Store in `.env` file (in `.gitignore`)
- Use `.env.example` as template
- Never commit `.env` to git

### Production (Railway/Fly.io)
- Set via platform dashboard (Railway Secrets / Fly Secrets)
- Never store in source code
- Rotate secrets regularly (every 90 days)

### Secret Generation
```bash
# JWT Secret (32 bytes)
openssl rand -hex 32

# Other secrets (16 bytes)
openssl rand -hex 16

# Base64 secrets
openssl rand -base64 32
```

---

## 📊 Logging & Monitoring

### What to Log
- ✅ API requests (without sensitive data)
- ✅ Authentication events (success/failure)
- ✅ AI API calls (model, tokens, cost)
- ✅ Errors and exceptions
- ✅ Database query errors

### What NOT to Log
- ❌ Passwords
- ❌ API keys
- ❌ JWT tokens
- ❌ User personal data (email, name) unless necessary
- ❌ Credit card info (if payment added)

### Sensitive Data Masking
```python
# Implemented in config.py
settings.model_dump()  # Automatically masks sensitive fields
# Output: {"OPENAI_API_KEY": "***REDACTED***", ...}
```

---

## 🚨 Incident Response

### Security Incident Detected

1. **Immediate Actions**:
   - Disable affected endpoint/feature
   - Rotate compromised secrets
   - Review access logs
   - Notify users if data breach

2. **Investigation**:
   - Check Sentry error logs
   - Review Supabase logs
   - Analyze API usage patterns
   - Identify root cause

3. **Remediation**:
   - Fix vulnerability
   - Deploy patch
   - Update security documentation
   - Add tests to prevent recurrence

4. **Post-Incident**:
   - Document lessons learned
   - Update security policies
   - Conduct security audit

---

## 🔍 Security Audit Checklist

### Monthly Audit
- [ ] Review Sentry error logs
- [ ] Check for failed login attempts
- [ ] Verify RLS policies still active
- [ ] Check for unusual API usage patterns
- [ ] Review AI API costs (could indicate abuse)

### Quarterly Audit
- [ ] Rotate all secrets (JWT, webhooks, cron)
- [ ] Update dependencies (`poetry update`)
- [ ] Run security scan (`safety check` or `bandit`)
- [ ] Review access logs
- [ ] Penetration testing (manual or automated)

### Dependency Security
```bash
# Check for known vulnerabilities
poetry run safety check

# Update dependencies
poetry update

# Lock file for reproducible builds
poetry lock
```

---

## 📞 Reporting Security Issues

### Do NOT Open Public Issues

If you discover a security vulnerability:

1. **Email**: renato@sharpened.me
2. **Subject**: [SECURITY] Brief description
3. **Include**:
   - Description of vulnerability
   - Steps to reproduce
   - Potential impact
   - Suggested fix (if any)

### Response Time
- Initial response: Within 24 hours
- Status update: Within 7 days
- Fix deployed: Within 30 days (depending on severity)

---

## ✅ Security Best Practices

### For Developers
- ✅ Follow TDD (tests catch security bugs early)
- ✅ Review CLAUDE.md security section before coding
- ✅ Validate ALL inputs (never trust user data)
- ✅ Use Pydantic models (automatic validation)
- ✅ Never log sensitive data
- ✅ Keep dependencies updated
- ✅ Use type hints (catch errors at dev time)

### For Deployment
- ✅ Use production environment variables
- ✅ Enable HTTPS (handled by Railway/Fly.io)
- ✅ Set strong secrets (min 32 chars)
- ✅ Enable Sentry for error tracking
- ✅ Test security before deploying
- ✅ Monitor logs after deployment

---

## 📚 Additional Resources

- **Supabase Security**: https://supabase.com/docs/guides/platform/going-into-prod
- **FastAPI Security**: https://fastapi.tiangolo.com/tutorial/security/
- **OWASP Top 10**: https://owasp.org/www-project-top-ten/
- **Python Security**: https://python.readthedocs.io/en/stable/library/security_warnings.html

---

**Security is everyone's responsibility. Report issues, follow best practices, and keep Wagner Coach safe!** 🔐
