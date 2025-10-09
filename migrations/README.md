# Wagner Coach Database Migrations

**Last Updated:** 2025-10-09
**Status:** Consolidated & Cleaned

## 📁 Migration Strategy

All database migrations are now consolidated in this single directory:
```
wagner-coach-backend/migrations/
```

**Other migration directories have been superseded and should be ignored:**
- ❌ `wagner-coach-backend/supabase/migrations/` - Old location
- ❌ `wagner-coach-clean/supabase/migrations/` - Frontend migrations (deprecated)

---

## 🗄️ Current Live Schema

The **authoritative source of truth** for the database schema is the live Supabase database. The user provided the complete live schema with 46 tables.

**IMPORTANT:** When making schema changes:
1. Always check the live database first
2. Create incremental migrations that build on the current state
3. Never assume the database matches old migration files
4. Use the live schema as your baseline

---

## 📝 Migration Files (Chronological)

### Active Migrations (Applied & Verified)
These migrations represent the historical changes that led to the current schema:

1. **007_fix_meal_nutrition_calculations.sql** (Oct 7) - Fixed meal nutrition calculation logic
2. **008_fix_food_serving_sizes.sql** (Oct 7) - Fixed food serving size conversions
3. **010_add_ai_food_tracking.sql** (Oct 7) - Added AI food tracking capabilities
4. **011_fix_missing_nutrition_data.sql** (Oct 7) - Fixed missing nutrition data in foods_enhanced
5. **012_add_auto_log_preference.sql** (Oct 8) - Added auto_log_enabled to user_preferences
6. **013_adaptive_consultation_system.sql** (Oct 8) - Added adaptive AI consultation with specialists
7. **014_add_user_events_calendar.sql** (Oct 9) - Added events and calendar system
8. **015_garmin_health_integration.sql** (Oct 9) - Added Garmin health integration (8 tables)
9. **016_remove_strava_integration.sql** (Oct 9) - Removed Strava (replaced by Garmin)
10. **017_activity_deduplication.sql** (Oct 9) - Added activity merge request system
11. **020_nutrition_base_schema.sql** (Oct 9) - Consolidated nutrition schema
12. **021_recursive_meal_templates.sql** (Oct 9) - Added recursive meal templates
13. **022_fix_meal_triggers_for_templates.sql** (Oct 9) - Fixed triggers for templates
14. **add_user_timezone.sql** (Oct 8) - Added user timezone support

### Cleanup Script (To Be Run)
- **DROP_UNUSED_TABLES.sql** (Oct 9) - Drops 13 unused tables after comprehensive codebase analysis

---

## 🧹 Cleanup Actions Taken

### Deleted Migration Directories
1. Deleted scattered migrations from `wagner-coach-backend/supabase/migrations/`
2. Deleted frontend migrations from `wagner-coach-clean/supabase/migrations/`
3. Consolidated all migrations to this single directory

### Migration Files Removed (Superseded)
- `20241006000000_nutrition_goals_system.sql` - Superseded by consolidated nutrition schema
- `20241006212000_clean_and_restore_fk.sql` - Superseded by current schema
- `20251002_ai_program_rls.sql` - RLS policies in live schema
- `20251002_enhanced_onboarding.sql` - Onboarding in live schema
- `20251002_onboarding_system.sql` - Onboarding in live schema
- `20251008_auto_create_profiles.sql` - Profile creation in live schema
- `20251009_add_get_or_create_user_preferences_function.sql` - Function in live schema
- `currentschema_20251002.sql` - Outdated snapshot (Oct 2), replaced by current live schema

---

## 🎯 Moving Forward: How to Create New Migrations

### Step 1: Understand Current State
```sql
-- Query the live database to see current schema
SELECT table_name, column_name, data_type
FROM information_schema.columns
WHERE table_schema = 'public'
ORDER BY table_name, ordinal_position;
```

### Step 2: Create Incremental Migration
Create a new migration file in this directory with naming convention:
```
<number>_<descriptive_name>.sql
```

Example: `023_add_social_features.sql`

### Step 3: Migration Template
```sql
-- ============================================================
-- Migration: 023_add_social_features.sql
-- Description: Add social features (friends, sharing)
-- Created: 2025-10-XX
-- Dependencies: Current live schema (46 tables)
-- ============================================================

-- UP Migration
CREATE TABLE IF NOT EXISTS user_friends (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    friend_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    status TEXT NOT NULL CHECK (status IN ('pending', 'accepted', 'blocked')),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, friend_id)
);

-- RLS Policies
ALTER TABLE user_friends ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own friend relationships"
ON user_friends FOR SELECT
USING (auth.uid() = user_id OR auth.uid() = friend_id);

CREATE POLICY "Users can create friend requests"
ON user_friends FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Indexes
CREATE INDEX idx_user_friends_user_id ON user_friends(user_id);
CREATE INDEX idx_user_friends_friend_id ON user_friends(friend_id);
CREATE INDEX idx_user_friends_status ON user_friends(status);

-- ============================================================
-- DOWN Migration (for rollback)
-- ============================================================
-- DROP TABLE IF EXISTS user_friends CASCADE;
```

### Step 4: Test Locally
```bash
# Apply migration to local Supabase
supabase db push --file migrations/023_add_social_features.sql

# Verify it worked
supabase db diff
```

### Step 5: Apply to Production
```bash
# Deploy to production Supabase
# (Manual application via Supabase dashboard SQL editor)
```

---

## ⚠️ Critical Rules

1. **Never modify old migration files** - They are historical records
2. **Always create new migrations** - Even for fixes
3. **Always test migrations locally first** - Use local Supabase instance
4. **Always include rollback (DOWN) migrations** - In comments if not automated
5. **Always add RLS policies** - Security first
6. **Always add indexes** - For foreign keys and frequently queried columns
7. **Always use CASCADE** - For foreign key deletions (when appropriate)
8. **Always check live schema first** - Don't assume database state

---

## 🗑️ Unused Tables (Identified for Deletion)

Run `DROP_UNUSED_TABLES.sql` to remove these 13 unused tables:
1. strava_activities
2. strava_auth
3. workout_logs
4. workout_log_exercises
5. workout_sets
6. workout_exercises
7. workouts
8. workout_days
9. custom_foods
10. nutrition_goals
11. weekly_workout_goals
12. coach_tool_calls
13. custom_exercises

**Before running:** Backup your database!

---

## 📊 Current Live Schema Summary

**46 Total Tables:**
- 33 Active (in use by backend)
- 13 Unused (to be deleted)

**Active Tables by Feature:**
- **Auth & Profiles** (2): profiles, user_preferences
- **Nutrition** (8): meal_logs, meal_foods, meal_templates, meal_template_items, foods_enhanced, user_food_popularity, plus 2 deprecated
- **Activities** (3): activities, activity_exercises, activity_sets
- **Events** (2): events, event_checkins
- **Coach** (2): coach_conversations, coach_messages
- **Consultation** (4): consultation_sessions, consultation_messages, consultation_extractions, consultation_daily_recommendations
- **Programs** (4): ai_generated_programs, ai_program_days, ai_program_workouts, ai_program_meals
- **Garmin** (8): garmin_tokens, garmin_health_snapshot, garmin_daily_summaries, garmin_sleep_data, garmin_stress_data, garmin_hrv_data, garmin_body_battery_data, garmin_respiration_data
- **Embeddings** (1): multimodal_embeddings
- **Monitoring** (1): api_usage_logs

---

## 🎓 Best Practices

### DO ✅
- Keep migrations small and focused
- Use descriptive migration names
- Include comments explaining "why" not just "what"
- Test rollback before deploying
- Document breaking changes
- Use transactions for multi-step migrations

### DON'T ❌
- Modify existing migrations
- Assume database state
- Skip RLS policies
- Forget indexes on foreign keys
- Delete data without backup
- Deploy untested migrations

---

## 📚 Resources

- **Supabase Migrations Docs**: https://supabase.com/docs/guides/database/migrations
- **PostgreSQL Docs**: https://www.postgresql.org/docs/
- **pgvector Extension**: https://github.com/pgvector/pgvector

---

**END OF README**

This consolidation represents the clean, production-ready state of Wagner Coach database migrations as of 2025-10-09.
