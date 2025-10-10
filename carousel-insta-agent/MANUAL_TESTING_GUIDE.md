# Manual Testing Guide

## Prerequisites Checklist

Before testing, ensure you have:
- [ ] All API keys configured in `.env`
- [ ] Supabase database running with migrations applied
- [ ] Redis running (for Celery)
- [ ] Backend server running (`poetry run uvicorn app.main:app --reload`)
- [ ] Celery worker running (`poetry run celery -A app.workers.celery_app worker --loglevel=info`)
- [ ] Frontend running (`npm run dev`)

## Test 1: End-to-End Carousel Generation

### Objective
Verify the complete carousel generation pipeline works.

### Steps

1. **Start all services**
   ```bash
   # Terminal 1 - Backend
   cd backend
   poetry run uvicorn app.main:app --reload

   # Terminal 2 - Worker
   cd backend
   poetry run celery -A app.workers.celery_app worker --loglevel=info

   # Terminal 3 - Frontend
   cd frontend
   npm run dev
   ```

2. **Open the application**
   - Navigate to `http://localhost:3000`
   - Should see landing page

3. **Create a carousel**
   - Click "Get Started" or "Create Carousel"
   - Fill in form:
     - Topic: "How vector embeddings work in AI"
     - Type: "Concept Explainer"
     - Slides: 8
     - Voice: "Educational & Engaging"
   - Click "Generate Carousel"

4. **Monitor generation** (in Celery terminal)
   - Should see log: "carousel_generation_started"
   - Should see: "research_started"
   - Should see: "outline_generated"
   - Should see: "slides_copy_generated"
   - Should see: "dalle_generation_started" (for each slide)
   - Should see: "carousel_generation_complete"

5. **Check for errors**
   - ❌ **If Perplexity fails:** Check API key, check rate limits
   - ❌ **If Claude fails:** Check API key, check quota
   - ❌ **If DALL-E fails:** Check API key, check billing
   - ❌ **If database fails:** Check Supabase connection

6. **View completed carousel**
   - Should redirect to carousel detail page
   - Should see 8 generated slides
   - Should see caption with hashtags
   - Should see total cost (~$2.60-3.00)

### Expected Results
- ✅ Carousel status changes: pending → researching → writing → designing → completed
- ✅ Total time: 5-10 minutes
- ✅ Cost: ~$2.60-3.00
- ✅ All slides have images and copy
- ✅ Caption is generated

### Common Issues
| Issue | Cause | Solution |
|-------|-------|----------|
| "Research failed" | Perplexity API key invalid | Check `PERPLEXITY_API_KEY` in `.env` |
| "Failed to generate outline" | Claude API key invalid | Check `ANTHROPIC_API_KEY` in `.env` |
| "Image generation failed" | OpenAI API key invalid or quota | Check `OPENAI_API_KEY` and billing |
| "Database operation failed" | Supabase connection issue | Check `SUPABASE_URL` and keys |
| Worker not processing | Celery/Redis issue | Restart Redis and Celery worker |

---

## Test 2: Instagram Publishing Flow

### Objective
Test publishing a completed carousel to Instagram.

### Prerequisites
- [ ] Instagram Business Account connected to Facebook Page
- [ ] Instagram API credentials configured
- [ ] Long-lived access token generated (60-day)
- [ ] At least one completed carousel in system

### Steps

1. **Verify Instagram API credentials**
   ```bash
   # Test access token is valid
   curl -X GET "https://graph.facebook.com/v18.0/me?access_token=YOUR_TOKEN"

   # Should return your account info
   ```

2. **Get a completed carousel**
   - Navigate to Dashboard
   - Find a carousel with status="completed"
   - Click on it

3. **Publish to Instagram**
   - Click "Publish to Instagram" button
   - Choose "Publish Immediately"
   - Click "Confirm"

4. **Monitor publishing process**
   ```bash
   # In backend terminal, watch for:
   # - "instagram_publish_started"
   # - "dalle_generation_started" (if images need re-generation)
   # - "instagram_published" or "instagram_publish_failed"
   ```

5. **Verify on Instagram**
   - Open Instagram app or web
   - Go to your business profile
   - Should see new carousel post
   - Verify all 8 slides are present
   - Verify caption and hashtags

### Expected Results
- ✅ Carousel status changes to "published"
- ✅ `instagram_post_id` is saved
- ✅ Post appears on Instagram within 1-2 minutes
- ✅ All slides are in correct order
- ✅ Caption with hashtags is applied

### Common Issues
| Issue | Cause | Solution |
|-------|-------|----------|
| "Token expired" | Access token is invalid | Refresh long-lived token |
| "Image URL not accessible" | Images not publicly accessible | Use public storage (not localhost) |
| "Rate limit exceeded" | Too many posts | Wait 24 hours, Instagram limits 25 posts/day |
| "Invalid image format" | Image not in supported format | Verify PNG/JPG, max 8MB |
| "Caption too long" | >2200 characters | Truncate caption |

---

## Test 3: Error Recovery

### Objective
Verify system handles failures gracefully.

### Test 3a: API Failure Mid-Generation

1. **Start carousel generation**
2. **Simulate API failure** (disconnect internet or rate limit API)
3. **Observe behavior**
   - Should retry 3 times with exponential backoff
   - Should log retry attempts
   - After 3 failures, should mark carousel as "failed"
   - Should NOT charge user for failed attempts

### Test 3b: Frontend Error Handling

1. **Break a component** (temporarily add `throw new Error("test")` in dashboard)
2. **Navigate to dashboard**
3. **Verify error boundary**
   - Should show error UI (not white screen)
   - Should have "Refresh" and "Go to Dashboard" buttons
   - Should log error to console (or Sentry)

### Test 3c: Database Connection Loss

1. **Stop Supabase** (or invalidate credentials)
2. **Try to create carousel**
3. **Verify**
   - Should show clear error message
   - Should not crash frontend
   - Should log error properly

---

## Test 4: Cost Tracking

### Objective
Verify all AI API calls are logged and costs tracked.

### Steps

1. **Generate a carousel** (complete flow)

2. **Check database for cost logs**
   ```sql
   SELECT * FROM api_usage_logs
   WHERE carousel_id = 'YOUR_CAROUSEL_ID'
   ORDER BY created_at;
   ```

3. **Verify cost breakdown**
   - Should have entries for:
     - Perplexity (research)
     - Claude (outline, copywriting, caption)
     - OpenAI (8 DALL-E image generations)
   - Total should match `carousels.total_cost`

4. **Check cost accuracy**
   - Perplexity: ~$0.30
   - Claude: ~$1.50
   - DALL-E: ~$0.64 (8 images × $0.080)
   - **Total: ~$2.44-3.00**

### Expected Results
- ✅ All API calls logged
- ✅ Costs accurate (±10%)
- ✅ Total cost displayed in UI
- ✅ Cost breakdown available

---

## Test 5: Performance

### Objective
Measure system performance under load.

### Test 5a: Single Carousel Generation Time

1. Generate carousel
2. Time from start to completion
3. **Expected: 5-10 minutes**

### Test 5b: Concurrent Generations

1. Start 3 carousel generations simultaneously
2. Monitor Celery worker load
3. Verify all complete successfully
4. **Expected: 5-15 minutes** (depends on API rate limits)

### Test 5c: Database Query Performance

```bash
# Check slow queries in Supabase dashboard
# All queries should be < 100ms
```

---

## Test 6: Security

### Objective
Verify security measures are working.

### Test 6a: Authentication

1. **Try accessing protected endpoint without token**
   ```bash
   curl -X GET http://localhost:8000/api/v1/carousels/
   ```
   - Should return 401 Unauthorized

2. **Try accessing another user's carousel**
   - Should return 404 or 403

### Test 6b: Rate Limiting

1. **Make 100 requests rapidly**
   ```bash
   for i in {1..100}; do
     curl -X GET http://localhost:8000/api/v1/carousels/ \
       -H "Authorization: Bearer YOUR_TOKEN"
   done
   ```
2. **Verify rate limit kicks in**
   - Should return 429 Too Many Requests after limit

### Test 6c: Input Validation

1. **Try invalid carousel type**
   - Should return 422 Unprocessable Entity

2. **Try SQL injection in topic**
   ```json
   {"topic": "'; DROP TABLE carousels; --"}
   ```
   - Should be safely escaped (using ORM)

---

## Test Checklist Summary

### Critical Tests (Must Pass)
- [ ] Test 1: End-to-end carousel generation
- [ ] Test 2: Instagram publishing
- [ ] Test 3a: Error recovery with retries
- [ ] Test 3b: Frontend error boundaries
- [ ] Test 4: Cost tracking accuracy

### Important Tests (Should Pass)
- [ ] Test 5a: Generation time < 10 minutes
- [ ] Test 5b: Concurrent generations work
- [ ] Test 6a: Authentication required
- [ ] Test 6b: Rate limiting works

### Nice to Have (Can Skip for MVP)
- [ ] Test 5c: Database performance
- [ ] Test 6c: Advanced security tests

---

## Troubleshooting Tips

### Backend Won't Start
```bash
# Check Python version
python --version  # Should be 3.11+

# Check dependencies
poetry install

# Check environment variables
poetry run python -c "from app.config import settings; print(settings.SUPABASE_URL)"
```

### Celery Worker Issues
```bash
# Check Redis
redis-cli ping  # Should return PONG

# Clear Celery queue
poetry run celery -A app.workers.celery_app purge

# Restart worker with debug logging
poetry run celery -A app.workers.celery_app worker --loglevel=debug
```

### Frontend Issues
```bash
# Clear Next.js cache
rm -rf .next

# Reinstall dependencies
rm -rf node_modules
npm install

# Check API connection
curl http://localhost:8000/health
```

### Database Issues
```bash
# Test Supabase connection
curl $SUPABASE_URL/rest/v1/ -H "apikey: $SUPABASE_KEY"

# Run migrations
cd backend/migrations
psql $DATABASE_URL < 001_initial_schema.sql
```

---

## Success Criteria

**System is ready for demo if:**
- ✅ Can generate ONE carousel end-to-end
- ✅ Generation takes < 10 minutes
- ✅ Cost is < $3.50
- ✅ Frontend doesn't crash on errors
- ✅ Can publish to Instagram successfully

**System is production-ready if:**
- ✅ All critical tests pass
- ✅ Error recovery works (retries)
- ✅ Cost tracking accurate
- ✅ Rate limiting works
- ✅ Can handle 3+ concurrent generations
- ✅ Security tests pass
