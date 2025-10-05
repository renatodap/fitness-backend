# Deployment Guide - Wagner Coach Backend

This guide covers deploying the Wagner Coach backend to production.

---

## 🚀 Deployment Platforms

Wagner Coach backend can be deployed to:
- **Railway** (Recommended - easy setup)
- **Fly.io** (More control)
- **Heroku** (Alternative)
- **Self-hosted** (Docker)

This guide focuses on **Railway** deployment.

---

## 📋 Pre-Deployment Checklist

### 1. Code Quality
- [ ] All tests passing: `poetry run pytest`
- [ ] Coverage ≥80%: `poetry run pytest --cov=app --cov-report=term-missing`
- [ ] Linting passes: `poetry run ruff check app/`
- [ ] Formatting correct: `poetry run black app/ --check`
- [ ] Type checking passes: `poetry run mypy app/`
- [ ] No hardcoded secrets in code

### 2. Environment Configuration
- [ ] `.env.example` is up to date
- [ ] All required environment variables documented
- [ ] Production secrets generated (strong, unique)
- [ ] API keys are production keys (not test keys)

### 3. Database
- [ ] All migrations applied locally and tested
- [ ] Supabase RLS policies enabled on all tables
- [ ] Database backups configured
- [ ] Connection pooling reviewed

### 4. Security
- [ ] `ENVIRONMENT=production`
- [ ] `DEBUG=false`
- [ ] `ALLOW_ALL_ORIGINS=false`
- [ ] `CORS_ORIGINS` set to specific frontend domain(s)
- [ ] JWT_SECRET is strong (min 32 chars)
- [ ] All secrets rotated from development

### 5. Monitoring
- [ ] Sentry DSN configured
- [ ] Logging level set to INFO or WARNING
- [ ] Health check endpoint tested (`/health`)

---

## 🏗️ Railway Deployment

### Step 1: Install Railway CLI

```bash
npm i -g @railway/cli
```

### Step 2: Login to Railway

```bash
railway login
```

### Step 3: Initialize Project

```bash
cd wagner-coach-backend
railway init
```

Follow prompts to create a new project.

### Step 4: Set Environment Variables

```bash
# Set all required variables
railway variables set ENVIRONMENT=production
railway variables set DEBUG=false
railway variables set LOG_LEVEL=INFO

# Database (Supabase)
railway variables set SUPABASE_URL=https://your-project.supabase.co
railway variables set SUPABASE_KEY=your-anon-key
railway variables set SUPABASE_SERVICE_KEY=your-service-key

# AI APIs
railway variables set OPENAI_API_KEY=sk-...
railway variables set ANTHROPIC_API_KEY=sk-ant-...
railway variables set GROQ_API_KEY=gsk_...
railway variables set OPENROUTER_API_KEY=sk-or-...

# Security
railway variables set JWT_SECRET=$(openssl rand -hex 32)
railway variables set CRON_SECRET=$(openssl rand -hex 16)
railway variables set WEBHOOK_SECRET=$(openssl rand -hex 16)

# CORS
railway variables set ALLOW_ALL_ORIGINS=false
railway variables set CORS_ORIGINS=https://wagnercoach.com,https://www.wagnercoach.com

# Monitoring (optional)
railway variables set SENTRY_DSN=https://...@sentry.io/...

# Redis (if using Railway Redis plugin)
railway variables set REDIS_URL=${{REDIS.REDIS_URL}}
```

### Step 5: Add Railway Configuration

The project already includes:
- `Procfile` - Tells Railway how to start the app
- `railway.toml` - Railway configuration
- `runtime.txt` - Python version

### Step 6: Deploy

```bash
railway up
```

### Step 7: Get Deployment URL

```bash
railway domain
```

This will give you a URL like `https://your-app.railway.app`

### Step 8: Custom Domain (Optional)

```bash
railway domain add api.wagnercoach.com
```

Follow DNS instructions to point domain to Railway.

---

## 🔧 Post-Deployment Configuration

### 1. Verify Health Check

```bash
curl https://your-app.railway.app/health
```

Should return:
```json
{
  "status": "healthy",
  "version": "0.1.0",
  "services": {
    "database": "connected"
  }
}
```

### 2. Test API Endpoints

```bash
# Root endpoint
curl https://your-app.railway.app/

# API docs (should be disabled in production)
curl https://your-app.railway.app/docs
# Expected: 404 Not Found (docs disabled when DEBUG=false)
```

### 3. Monitor Logs

```bash
railway logs
```

Watch for:
- ✅ Application startup messages
- ✅ Database connection successful
- ✅ No error messages
- ⚠️ Security warnings (ALLOW_ALL_ORIGINS, etc.)

### 4. Configure Webhooks

If using Strava/Garmin integrations:

**Strava**:
1. Go to: https://www.strava.com/settings/api
2. Set callback URL: `https://your-app.railway.app/api/v1/integrations/strava/webhook`

**Garmin**:
1. Configure in Garmin Connect API
2. Set webhook URL: `https://your-app.railway.app/api/v1/integrations/garmin/webhook`

---

## 🗄️ Database Migrations

### Apply Migrations to Production

**IMPORTANT**: Always test migrations locally first!

```bash
# Connect to production Supabase via dashboard
# OR use Supabase CLI

# View current schema
supabase db dump --remote > current_prod_schema.sql

# Apply new migration
supabase db push --remote

# Verify migration succeeded
supabase db diff --remote
```

### Migration Best Practices
- ✅ Always have a rollback plan
- ✅ Test migrations on staging first
- ✅ Backup database before migrations
- ✅ Use transactions when possible
- ✅ Document schema changes in migration file

---

## 📊 Monitoring & Logging

### Railway Dashboard
- View logs in real-time
- Monitor resource usage (CPU, memory)
- Check deployment history
- Manage environment variables

### Sentry (Error Tracking)
1. Create project at https://sentry.io
2. Get DSN from project settings
3. Add to Railway: `railway variables set SENTRY_DSN=https://...`
4. View errors in Sentry dashboard

### Health Monitoring
Set up uptime monitoring with:
- **UptimeRobot**: https://uptimerobot.com
- **Pingdom**: https://pingdom.com
- **Healthchecks.io**: https://healthchecks.io

Monitor: `https://your-app.railway.app/health`

---

## 🔄 Continuous Deployment

### Auto-Deploy on Git Push

Railway can automatically deploy when you push to `main`:

```bash
# In your local repo
git push origin main
```

Railway will:
1. Detect new commit
2. Build new Docker image
3. Run tests (if configured)
4. Deploy to production
5. Keep previous version as rollback

### Manual Deploy

```bash
railway up
```

---

## 🐛 Troubleshooting

### Deployment Fails

**Check logs**:
```bash
railway logs
```

**Common issues**:
- Missing environment variables → Add via `railway variables set`
- Port binding error → Railway auto-assigns port via `$PORT` env var
- Python version mismatch → Check `runtime.txt`
- Dependencies missing → Verify `pyproject.toml` and `poetry.lock`

### Database Connection Issues

**Check**:
- Supabase URL correct (including `https://`)
- Service key valid
- Supabase project not paused (free tier)
- IP allowlist disabled or Railway IP added

### CORS Errors

**Verify**:
```bash
railway variables get ALLOW_ALL_ORIGINS  # Should be "false"
railway variables get CORS_ORIGINS       # Should include frontend domain
```

### High Memory Usage

**Monitor**:
```bash
railway status
```

**Solutions**:
- Reduce workers in `Procfile`
- Upgrade Railway plan
- Optimize database queries
- Add caching (Redis)

---

## 📈 Scaling

### Horizontal Scaling (Multiple Instances)

Railway Pro plan:
```bash
railway scale --replicas 3
```

### Vertical Scaling (More Resources)

Upgrade Railway plan:
- Starter: 512 MB RAM, 1 vCPU
- Pro: 8 GB RAM, 8 vCPU

### Database Scaling

Supabase:
- Free: 500 MB, 2 connections
- Pro: 8 GB, 60 connections
- Team: 32 GB, 120 connections

---

## 🔐 Security Hardening

### After Deployment

1. **Rotate all secrets** (different from dev)
2. **Enable 2FA** on Railway account
3. **Restrict access** to Railway dashboard
4. **Monitor logs** for suspicious activity
5. **Set up alerts** for errors (Sentry)
6. **Review RLS policies** in Supabase

---

## 📋 Production Maintenance

### Weekly
- [ ] Check error logs (Sentry)
- [ ] Review API usage and costs
- [ ] Monitor uptime (>99%)
- [ ] Check for failed background jobs

### Monthly
- [ ] Update dependencies: `poetry update`
- [ ] Review security alerts
- [ ] Check database size and optimize
- [ ] Review AI API costs

### Quarterly
- [ ] Rotate secrets (JWT, webhooks)
- [ ] Security audit
- [ ] Performance optimization
- [ ] Capacity planning

---

## 🔄 Rollback Procedure

### If Deployment Breaks Production

**Railway**:
```bash
# View deployments
railway deployments

# Rollback to previous deployment
railway rollback <deployment-id>
```

**Database**:
```sql
-- If migration broke database
-- Restore from Supabase backup
-- OR apply DOWN migration manually
```

---

## 📞 Support

### Railway Issues
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- Status: https://status.railway.app

### Supabase Issues
- Docs: https://supabase.com/docs
- Discord: https://discord.supabase.com
- Status: https://status.supabase.com

---

## ✅ Post-Deployment Checklist

After successful deployment:

- [ ] Health check returns 200
- [ ] API endpoints responding correctly
- [ ] Database connection working
- [ ] Authentication working (JWT validation)
- [ ] AI endpoints responding (test coach chat)
- [ ] Webhooks configured (Strava, Garmin)
- [ ] Sentry receiving events
- [ ] Logs looking normal (no errors)
- [ ] Frontend can connect to backend
- [ ] Mobile app tested (if applicable)
- [ ] Uptime monitoring configured
- [ ] Team notified of deployment
- [ ] Documentation updated

---

**Production deployment is complete!** 🚀

Monitor closely for first 24 hours, then continue regular maintenance schedule.

For issues, check Railway logs, Sentry errors, and Supabase dashboard.
