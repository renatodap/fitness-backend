# Unified Coach Backend - Quick Start Guide

**Run this to test the new unified Coach backend immediately!**

---

## Step 1: Run Database Migration (2 minutes)

### Option A: Supabase Dashboard (Easiest)

1. **Open Supabase Dashboard**
   - Go to: https://supabase.com/dashboard/project/YOUR_PROJECT/sql/new

2. **Copy Migration SQL**
   ```bash
   # Copy this file's contents
   wagner-coach-backend/migrations/009_unified_coach_schema.sql
   ```

3. **Paste and Run**
   - Paste into SQL Editor
   - Click "Run"
   - Wait for success message: "✅ Migration 009 complete"

4. **Verify Tables Created**
   ```sql
   -- Run this query to verify:
   SELECT table_name
   FROM information_schema.tables
   WHERE table_schema = 'public'
   AND table_name IN ('coach_messages', 'coach_message_embeddings');

   -- Should return 2 rows
   ```

---

### Option B: Supabase CLI (If installed)

```bash
cd wagner-coach-backend
supabase db push --file migrations/009_unified_coach_schema.sql
```

---

## Step 2: Verify Environment Variables (1 minute)

Make sure these are set in `.env`:

```bash
# AI APIs
ANTHROPIC_API_KEY=sk-ant-...  # Get from https://console.anthropic.com
GROQ_API_KEY=gsk_...          # Get from https://console.groq.com

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_KEY=eyJhb...
SUPABASE_SERVICE_KEY=eyJhb...  # From Supabase Settings > API

# Security
JWT_SECRET=your-secret-key-min-32-chars
```

---

## Step 3: Start Backend Locally (1 minute)

```bash
cd wagner-coach-backend

# Install dependencies (if not done)
poetry install

# Start server
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Server should start at**: http://localhost:8000

---

## Step 4: Test API Endpoints (5 minutes)

### A. Health Check (No auth required)

```bash
curl http://localhost:8000/api/v1/coach/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "service": "unified_coach_api",
  "version": "1.0.0",
  "features": [
    "auto_log_detection",
    "rag_powered_chat",
    "message_vectorization",
    "conversation_history"
  ]
}
```

---

### B. Send Message (Requires JWT)

**First, get a JWT token:**
1. Go to your frontend (http://localhost:3000)
2. Sign in
3. Open browser DevTools > Application > Local Storage
4. Copy the `supabase.auth.token` value

**Then test the endpoint:**

```bash
# Replace YOUR_JWT_TOKEN with actual token
export JWT_TOKEN="eyJhbGci..."

# Test with a CHAT message (question)
curl -X POST http://localhost:8000/api/v1/coach/message \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "What should I eat for breakfast?",
    "conversation_id": null,
    "has_image": false,
    "has_audio": false
  }'
```

**Expected response (CHAT mode):**
```json
{
  "success": true,
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "message_id": "456e7890-e89b-12d3-a456-426614174000",
  "is_log_preview": false,
  "message": "Based on your goals, I'd recommend...",
  "rag_context": {
    "sources_count": 10,
    "coach_messages_count": 0,
    "quick_entries_count": 10
  },
  "tokens_used": 350,
  "cost_usd": 0.0105
}
```

---

**Test with a LOG message:**

```bash
curl -X POST http://localhost:8000/api/v1/coach/message \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I just ate 3 eggs and oatmeal for breakfast",
    "conversation_id": null
  }'
```

**Expected response (LOG mode):**
```json
{
  "success": true,
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "message_id": "789e0123-e89b-12d3-a456-426614174000",
  "is_log_preview": true,
  "log_preview": {
    "log_type": "meal",
    "confidence": 0.95,
    "data": {
      "meal_type": "breakfast",
      "calories": 450,
      "protein": 35,
      "carbs": 40,
      "fats": 15,
      "foods": ["eggs", "oatmeal"]
    },
    "reasoning": "Past tense eating with specific foods",
    "summary": "Breakfast: 450 cal, 35g protein"
  }
}
```

---

### C. Confirm Log

```bash
# Use the conversation_id and message_id from previous response
curl -X POST http://localhost:8000/api/v1/coach/confirm-log \
  -H "Authorization: Bearer $JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
    "user_message_id": "789e0123-e89b-12d3-a456-426614174000",
    "log_type": "meal",
    "log_data": {
      "meal_type": "breakfast",
      "calories": 450,
      "protein": 35,
      "carbs": 40,
      "fats": 15,
      "foods": ["eggs", "oatmeal"]
    }
  }'
```

**Expected response:**
```json
{
  "success": true,
  "log_id": "abc12345-e89b-12d3-a456-426614174000",
  "quick_entry_log_id": "def67890-e89b-12d3-a456-426614174000",
  "system_message_id": "ghi09876-e89b-12d3-a456-426614174000",
  "system_message": "✅ Meal logged! 450 calories, 35g protein"
}
```

---

### D. Get Conversation History

```bash
curl -X GET "http://localhost:8000/api/v1/coach/conversations?limit=10" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected response:**
```json
{
  "success": true,
  "conversations": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Breakfast nutrition advice",
      "message_count": 3,
      "last_message_at": "2025-10-06T10:30:00Z",
      "created_at": "2025-10-06T10:00:00Z",
      "archived": false,
      "last_message_preview": "✅ Meal logged! 450 calories, 35g protein"
    }
  ],
  "total_count": 1,
  "has_more": false
}
```

---

### E. Get Messages in Conversation

```bash
# Replace with actual conversation_id from previous response
curl -X GET "http://localhost:8000/api/v1/coach/conversations/123e4567-e89b-12d3-a456-426614174000/messages" \
  -H "Authorization: Bearer $JWT_TOKEN"
```

**Expected response:**
```json
{
  "success": true,
  "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
  "messages": [
    {
      "id": "789e0123-e89b-12d3-a456-426614174000",
      "role": "user",
      "content": "I just ate 3 eggs and oatmeal for breakfast",
      "message_type": "chat",
      "created_at": "2025-10-06T10:00:00Z",
      "is_vectorized": true
    },
    {
      "id": "ghi09876-e89b-12d3-a456-426614174000",
      "role": "system",
      "content": "✅ Meal logged! 450 calories, 35g protein",
      "message_type": "log_confirmed",
      "created_at": "2025-10-06T10:00:10Z",
      "quick_entry_log_id": "def67890-e89b-12d3-a456-426614174000"
    }
  ],
  "total_count": 2,
  "has_more": false
}
```

---

## Step 5: Check Database (Verify Data Saved)

**Go to Supabase Dashboard > Table Editor**

Check these tables:
1. **coach_conversations** - Should have new conversation
2. **coach_messages** - Should have 2-3 messages (user + system)
3. **coach_message_embeddings** - Should have 2-3 embeddings
4. **quick_entry_logs** - Should have log record (if you confirmed a log)
5. **meal_logs** - Should have meal (if you confirmed a meal log)

---

## Step 6: Check FastAPI Auto-Docs

Open in browser:
- http://localhost:8000/docs (Swagger UI)
- http://localhost:8000/redoc (ReDoc)

You should see all 6 Coach endpoints documented:
1. POST /api/v1/coach/message
2. POST /api/v1/coach/confirm-log
3. GET /api/v1/coach/conversations
4. GET /api/v1/coach/conversations/{id}/messages
5. PATCH /api/v1/coach/conversations/{id}/archive
6. GET /api/v1/coach/health

---

## 🎉 Success Criteria

✅ Migration ran successfully
✅ Health check returns 200
✅ Chat message returns AI response
✅ Log message returns preview
✅ Confirm log saves to database
✅ Conversation history shows conversations
✅ Messages endpoint shows message list
✅ All data visible in Supabase dashboard
✅ FastAPI docs show all endpoints

**If all checks pass: Backend is working! 🚀**

---

## 🐛 Troubleshooting

### Error: "coach_messages table does not exist"
- Run migration 009 again
- Check Supabase Dashboard > Database > Tables
- Verify `coach_messages` and `coach_message_embeddings` exist

### Error: "ANTHROPIC_API_KEY not set"
- Check `.env` file has `ANTHROPIC_API_KEY=sk-ant-...`
- Restart backend server after adding env vars

### Error: "Invalid JWT token"
- Get fresh token from frontend (tokens expire)
- Check token format: `Bearer eyJhbGci...`
- Verify `JWT_SECRET` in `.env` matches frontend

### Error: "403 Forbidden"
- Check Row-Level Security policies are applied
- Verify user_id in JWT matches database records
- Try using `SUPABASE_SERVICE_KEY` for testing

---

## 📚 Next: Frontend Implementation

Once backend is working, implement the frontend:

1. **Delete AI Chat page** (`app/ai-chat/`)
2. **Rename bottom nav** "Quick Entry" → "Coach"
3. **Build ChatGPT-like UI** (message bubbles, input, sidebar)
4. **Connect to API** (use new endpoints)
5. **Test end-to-end** (chat + log flows)

See `UNIFIED_COACH_BACKEND_COMPLETE.md` for detailed frontend plan.

---

**Backend testing complete! Ready for frontend development.** 🎉
