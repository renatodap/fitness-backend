# Database Migrations

This directory contains SQL migration scripts for the Wagner Coach database schema.

## Phase 1: AI Coach RAG Foundation

**Migration File:** `001_phase1_database_rag_foundation.sql`

### What's Included

This migration sets up the foundation for AI coach functionality with RAG (Retrieval-Augmented Generation):

#### 1. Vector Search Infrastructure
- Enables `pgvector` extension
- Creates `embeddings` table for storing vector embeddings
- Adds `match_embeddings()` function for semantic search
- Sets up indexes for efficient vector similarity search

#### 2. Coach Personas System
- `coach_personas` table with Trainer and Nutritionist
- Default personas with specialized system prompts
- `coach_conversations` table for chat history
- `coach_recommendations` table for weekly adaptive recommendations
- `recommendation_feedback` table for user feedback

#### 3. Workout Planning (Plans vs Actuals)
- `workout_programs` - High-level workout plans
- `planned_workouts` - Specific workout sessions in the plan
- `planned_exercises` - Exercises within planned workouts
- `actual_workouts` - What the user actually did
- `actual_exercise_sets` - Individual sets performed
- `exercise_progress` - Progressive overload tracking

#### 4. Nutrition Planning (Plans vs Actuals)
- `nutrition_programs` - High-level nutrition plans
- `planned_meals` - Specific meals in the plan
- `planned_meal_foods` - Foods within planned meals
- `nutrition_compliance` - Daily compliance tracking

### How to Apply

#### Option 1: Supabase Dashboard
1. Go to your Supabase project dashboard
2. Navigate to SQL Editor
3. Create a new query
4. Copy and paste the contents of `001_phase1_database_rag_foundation.sql`
5. Click "Run" to execute the migration

#### Option 2: Supabase CLI
```bash
# Install Supabase CLI if not already installed
npm install -g supabase

# Login to Supabase
supabase login

# Link to your project
supabase link --project-ref YOUR_PROJECT_REF

# Run the migration
supabase db push --include-all

# Or apply directly via psql
psql YOUR_DATABASE_URL -f migrations/001_phase1_database_rag_foundation.sql
```

#### Option 3: Direct psql Connection
```bash
psql "postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres" -f migrations/001_phase1_database_rag_foundation.sql
```

### Verification

After running the migration, verify it was successful:

```sql
-- Check if pgvector is enabled
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Check if tables were created
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'public'
AND table_name IN (
    'embeddings',
    'coach_personas',
    'coach_conversations',
    'workout_programs',
    'nutrition_programs'
);

-- Check if coach personas were inserted
SELECT name, display_name FROM coach_personas;

-- Check if functions were created
SELECT routine_name
FROM information_schema.routines
WHERE routine_schema = 'public'
AND routine_name IN ('match_embeddings', 'calculate_compliance_score');
```

Expected output:
- `pgvector` extension should be listed
- All 14 new tables should exist
- 2 coach personas (trainer, nutritionist) should be present
- 2 functions should be created

### New API Endpoints

After applying this migration, the following API endpoints will be available:

#### Coach Endpoints (`/api/v1/coach/`)
- `POST /chat` - Chat with AI coach (trainer or nutritionist)
- `POST /recommendations/generate` - Generate weekly recommendations
- `GET /recommendations` - Get active recommendations
- `PATCH /recommendations/{id}` - Update recommendation status
- `GET /personas` - Get all coach personas
- `GET /conversations/{coach_type}` - Get conversation history

### Testing the New Functionality

```bash
# 1. Chat with trainer
curl -X POST http://localhost:8000/api/v1/coach/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "coach_type": "trainer",
    "message": "What workout should I do today?"
  }'

# 2. Generate weekly recommendations
curl -X POST http://localhost:8000/api/v1/coach/recommendations/generate \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -d '{
    "coach_type": "trainer"
  }'

# 3. Get active recommendations
curl http://localhost:8000/api/v1/coach/recommendations \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"

# 4. Get coach personas
curl http://localhost:8000/api/v1/coach/personas \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

### Rollback

If you need to rollback this migration:

```sql
-- Drop all new tables (in reverse dependency order)
DROP TABLE IF EXISTS recommendation_feedback CASCADE;
DROP TABLE IF EXISTS coach_recommendations CASCADE;
DROP TABLE IF EXISTS coach_conversations CASCADE;
DROP TABLE IF EXISTS coach_personas CASCADE;
DROP TABLE IF EXISTS nutrition_compliance CASCADE;
DROP TABLE IF EXISTS planned_meal_foods CASCADE;
DROP TABLE IF EXISTS planned_meals CASCADE;
DROP TABLE IF EXISTS nutrition_programs CASCADE;
DROP TABLE IF EXISTS exercise_progress CASCADE;
DROP TABLE IF EXISTS actual_exercise_sets CASCADE;
DROP TABLE IF EXISTS actual_workouts CASCADE;
DROP TABLE IF EXISTS planned_exercises CASCADE;
DROP TABLE IF EXISTS planned_workouts CASCADE;
DROP TABLE IF EXISTS workout_programs CASCADE;
DROP TABLE IF EXISTS embeddings CASCADE;

-- Drop functions
DROP FUNCTION IF EXISTS match_embeddings CASCADE;
DROP FUNCTION IF EXISTS calculate_compliance_score CASCADE;
DROP FUNCTION IF EXISTS update_updated_at_column CASCADE;

-- Optionally disable pgvector (only if not used elsewhere)
-- DROP EXTENSION IF EXISTS vector CASCADE;
```

### Next Steps

After applying Phase 1 migration:

1. **Test the endpoints** - Verify all API endpoints are working
2. **Create embeddings** - Start generating embeddings for existing data
3. **Test RAG** - Verify semantic search is returning relevant results
4. **Frontend integration** - Update frontend to use new coach endpoints
5. **Phase 2** - Implement quick entry system (voice, photo, text)

### Troubleshooting

**Error: extension "vector" does not exist**
- Solution: Ensure pgvector extension is available in your Postgres instance
- For Supabase: Enable the `pgvector` extension in dashboard under Database > Extensions

**Error: relation "profiles" does not exist**
- Solution: Ensure the base schema (profiles table) exists before running this migration

**Error: authentication failed**
- Solution: Check your database connection string and credentials

**RLS Policy Issues**
- Solution: Ensure `auth.uid()` function is available (standard in Supabase)
- Test by querying as an authenticated user

### Support

For issues or questions:
1. Check the main documentation in `AI_FITNESS_COACH_MASTER_PLAN.md`
2. Review the backend service implementations in `app/services/`
3. Check logs for detailed error messages

---

**Status:** Phase 1 Migration Ready ✅
**Last Updated:** 2025-09-30
**Compatible With:** PostgreSQL 12+, Supabase (with pgvector extension)
