-- =============================================================================
-- Migration 008: CONSOLIDATED SCHEMA (Clean Slate)
-- =============================================================================
--
-- PURPOSE:
-- Replace the bloated 80+ table schema with a lean, consolidated structure
-- that focuses on core Wagner Coach features:
-- 1. User profiles & settings (1 table)
-- 2. Quick Entry logging (2 tables: logs + embeddings)
-- 3. Meal tracking (2 tables: logs + foods)
-- 4. Activity tracking (2 tables: activities + segments)
-- 5. Body measurements (1 table)
-- 6. AI coach conversations (1 table)
-- 7. AI generated programs (3 tables: programs + days + items)
-- 8. Integrations (1 table for all connections)
--
-- TOTAL: 13 core tables (down from 80+)
--
-- =============================================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- =============================================================================
-- DROP OBSOLETE TABLES (Backup first in production!)
-- =============================================================================
-- This section removes redundant/obsolete tables
-- WARNING: Only run after backing up data you want to keep

-- Obsolete workout tables (replaced by activities + AI programs)
DROP TABLE IF EXISTS public.workout_workout_tags CASCADE;
DROP TABLE IF EXISTS public.workout_tags CASCADE;
DROP TABLE IF EXISTS public.workout_templates CASCADE;
DROP TABLE IF EXISTS public.workout_completions CASCADE;
DROP TABLE IF EXISTS public.user_workouts CASCADE;
DROP TABLE IF EXISTS public.workouts CASCADE;
DROP TABLE IF EXISTS public.favorite_workouts CASCADE;
DROP TABLE IF EXISTS public.exercise_completions CASCADE;
DROP TABLE IF EXISTS public.exercise_notes CASCADE;
DROP TABLE IF EXISTS public.set_performances CASCADE;
DROP TABLE IF EXISTS public.personal_records CASCADE;
DROP TABLE IF EXISTS public.day_exercises CASCADE;
DROP TABLE IF EXISTS public.user_exercises CASCADE;
DROP TABLE IF EXISTS public.active_workout_sessions CASCADE;

-- Obsolete program tables (replaced by ai_generated_programs)
DROP TABLE IF EXISTS public.program_day_completions CASCADE;
DROP TABLE IF EXISTS public.program_days CASCADE;
DROP TABLE IF EXISTS public.workout_programs CASCADE;
DROP TABLE IF EXISTS public.user_program_enrollments CASCADE;
DROP TABLE IF EXISTS public.program_generation_requests CASCADE;
DROP TABLE IF EXISTS public.program_generation_sessions CASCADE;

-- Obsolete exercise/equipment tables (too granular, move to JSONB)
DROP TABLE IF EXISTS public.exercises CASCADE;
DROP TABLE IF EXISTS public.exercise_categories CASCADE;
DROP TABLE IF EXISTS public.equipment_types CASCADE;
DROP TABLE IF EXISTS public.muscle_groups CASCADE;

-- Redundant embedding tables (consolidate into multimodal_embeddings)
DROP TABLE IF EXISTS public.embeddings CASCADE;
DROP TABLE IF EXISTS public.user_context_embeddings CASCADE;
DROP TABLE IF EXISTS public.profile_embeddings CASCADE;
DROP TABLE IF EXISTS public.goal_embeddings CASCADE;
DROP TABLE IF EXISTS public.user_profile_embeddings CASCADE;

-- Obsolete meal/food tables (consolidate)
DROP TABLE IF EXISTS public.meal_log_foods CASCADE;
DROP TABLE IF EXISTS public.meal_template_foods CASCADE;
DROP TABLE IF EXISTS public.meal_templates CASCADE;
DROP TABLE IF EXISTS public.foods CASCADE; -- Use foods_enhanced only
DROP TABLE IF EXISTS public.user_food_frequency CASCADE;
DROP TABLE IF EXISTS public.user_quick_foods CASCADE;
DROP TABLE IF EXISTS public.user_meal_patterns CASCADE;
DROP TABLE IF EXISTS public.food_combinations CASCADE;

-- Obsolete food data tables (over-engineered)
DROP TABLE IF EXISTS public.food_data_reports CASCADE;
DROP TABLE IF EXISTS public.food_search_analytics CASCADE;
DROP TABLE IF EXISTS public.food_serving_sizes CASCADE;
DROP TABLE IF EXISTS public.food_sync_queue CASCADE;
DROP TABLE IF EXISTS public.api_sync_logs CASCADE;
DROP TABLE IF EXISTS public.barcode_scan_history CASCADE;
DROP TABLE IF EXISTS public.user_submitted_foods CASCADE;
DROP TABLE IF EXISTS public.popular_foods_cache CASCADE;

-- Obsolete recipe tables (future feature)
DROP TABLE IF EXISTS public.recipe_ingredients CASCADE;
DROP TABLE IF EXISTS public.recipes CASCADE;

-- Obsolete restaurant tables (future feature)
DROP TABLE IF EXISTS public.restaurant_menu_items CASCADE;
DROP TABLE IF EXISTS public.restaurant_chains CASCADE;

-- Redundant settings/preference tables (consolidate into profiles)
DROP TABLE IF EXISTS public.user_settings CASCADE;
DROP TABLE IF EXISTS public.user_preferences CASCADE;
DROP TABLE IF EXISTS public.user_preference_profiles CASCADE;
DROP TABLE IF EXISTS public.user_nutrition_preferences CASCADE;
DROP TABLE IF EXISTS public.rest_timer_preferences CASCADE;

-- Obsolete context tables (use quick_entry_embeddings instead)
DROP TABLE IF EXISTS public.user_context_summaries CASCADE;
DROP TABLE IF EXISTS public.conversation_summaries CASCADE;
DROP TABLE IF EXISTS public.user_memory_facts CASCADE;
DROP TABLE IF EXISTS public.user_notes CASCADE;

-- Obsolete misc tables
DROP TABLE IF EXISTS public.user_custom_workouts CASCADE;
DROP TABLE IF EXISTS public.user_milestones CASCADE;
DROP TABLE IF EXISTS public.recommendation_feedback CASCADE;
DROP TABLE IF EXISTS public.coach_recommendations CASCADE;
DROP TABLE IF EXISTS public.coach_conversations CASCADE;
DROP TABLE IF EXISTS public.coach_personas CASCADE;
DROP TABLE IF EXISTS public.fitness_goals CASCADE;
DROP TABLE IF EXISTS public.user_active_programs CASCADE;
DROP TABLE IF EXISTS public.activity_workout_links CASCADE;

-- =============================================================================
-- 1. CORE: USER PROFILES (Consolidated)
-- =============================================================================
-- Single table for all user profile data, settings, preferences, onboarding

CREATE TABLE IF NOT EXISTS public.users (
    -- Identity
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Basic profile
    full_name TEXT,
    email TEXT, -- Cached from auth.users
    age INTEGER CHECK (age >= 13 AND age <= 120),
    biological_sex TEXT CHECK (biological_sex IN ('male', 'female', 'other')),

    -- Physical stats
    height_cm NUMERIC(5, 2) CHECK (height_cm > 0 AND height_cm < 300),
    current_weight_kg NUMERIC(5, 2) CHECK (current_weight_kg > 0 AND current_weight_kg < 500),
    goal_weight_kg NUMERIC(5, 2),

    -- Goals & preferences
    primary_goal TEXT CHECK (primary_goal IN ('build_muscle', 'lose_fat', 'improve_endurance', 'increase_strength', 'sport_performance', 'general_health')),
    experience_level TEXT CHECK (experience_level IN ('beginner', 'intermediate', 'advanced')),
    training_frequency INTEGER CHECK (training_frequency >= 0 AND training_frequency <= 7),
    available_equipment TEXT[] DEFAULT ARRAY[]::TEXT[],
    dietary_restrictions TEXT[] DEFAULT ARRAY[]::TEXT[],
    injury_limitations TEXT[] DEFAULT ARRAY[]::TEXT[],

    -- Nutrition goals
    daily_calorie_target INTEGER,
    daily_protein_target_g INTEGER,
    daily_carbs_target_g INTEGER,
    daily_fat_target_g INTEGER,

    -- Settings (all in one place)
    settings JSONB DEFAULT '{
        "unit_system": "metric",
        "timezone": "UTC",
        "notifications_enabled": true,
        "workout_reminders": true,
        "preferred_workout_time": null,
        "auto_sync_activities": true,
        "privacy": {
            "activities_public": false,
            "share_stats": false
        }
    }'::JSONB,

    -- Onboarding
    onboarding_completed BOOLEAN DEFAULT FALSE,
    onboarding_data JSONB DEFAULT '{}'::JSONB, -- Store all onboarding answers

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    last_active_at TIMESTAMPTZ,

    -- Indexes
    CONSTRAINT users_email_key UNIQUE (email)
);

CREATE INDEX idx_users_email ON public.users(email);
CREATE INDEX idx_users_last_active ON public.users(last_active_at DESC);

-- RLS
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own profile"
    ON public.users FOR SELECT
    USING (auth.uid() = id);

CREATE POLICY "Users can update own profile"
    ON public.users FOR UPDATE
    USING (auth.uid() = id);

CREATE POLICY "Service role has full access"
    ON public.users FOR ALL
    USING (auth.role() = 'service_role');

COMMENT ON TABLE public.users IS 'Consolidated user profiles, settings, preferences, and onboarding data';

-- =============================================================================
-- 2. QUICK ENTRY: Logs (keep from migration 007)
-- =============================================================================
-- Already created in migration 007, just add comments
COMMENT ON TABLE public.quick_entry_logs IS 'Main Quick Entry table: raw input + AI extracted data';
COMMENT ON TABLE public.quick_entry_embeddings IS 'Vector embeddings for semantic search across Quick Entry data';

-- =============================================================================
-- 3. MEALS: Consolidated Food Database
-- =============================================================================
-- Single foods table (keep foods_enhanced, drop old foods table)

-- Drop old food brand/source tables (over-engineered)
DROP TABLE IF EXISTS public.food_brands CASCADE;
DROP TABLE IF EXISTS public.food_sources CASCADE;

-- Use foods_enhanced as the single source of truth
COMMENT ON TABLE public.foods_enhanced IS 'Master food database with nutrition data from multiple sources';

-- =============================================================================
-- 4. MEALS: Meal Logs (Simplified)
-- =============================================================================
-- Keep existing meal_logs, just ensure it's properly indexed

-- Already exists, just add optimization indexes
CREATE INDEX IF NOT EXISTS idx_meal_logs_user_date ON public.meal_logs(user_id, logged_at DESC);
CREATE INDEX IF NOT EXISTS idx_meal_logs_category ON public.meal_logs(user_id, category);
CREATE INDEX IF NOT EXISTS idx_meal_logs_quick_entry ON public.meal_logs(quick_entry_log_id) WHERE quick_entry_log_id IS NOT NULL;

COMMENT ON TABLE public.meal_logs IS 'User meal logs with nutrition data (supports Quick Entry and manual logging)';

-- =============================================================================
-- 5. ACTIVITIES: Consolidated Activity Tracking
-- =============================================================================
-- Keep existing activities table (it's already well-designed)

CREATE INDEX IF NOT EXISTS idx_activities_user_date ON public.activities(user_id, start_date DESC);
CREATE INDEX IF NOT EXISTS idx_activities_type ON public.activities(user_id, activity_type);
CREATE INDEX IF NOT EXISTS idx_activities_source ON public.activities(source);

COMMENT ON TABLE public.activities IS 'All user activities: workouts, runs, sports, etc. (Strava, Garmin, Quick Entry, manual)';

-- Keep activity_segments (useful for detailed analysis)
COMMENT ON TABLE public.activity_segments IS 'Detailed segments/laps/sets within activities';

-- Keep activity_streams (time-series data)
COMMENT ON TABLE public.activity_streams IS 'Time-series data (HR, power, pace, etc.) for activities';

-- =============================================================================
-- 6. BODY MEASUREMENTS: Keep as-is
-- =============================================================================
CREATE INDEX IF NOT EXISTS idx_body_measurements_user_date ON public.body_measurements(user_id, measured_at DESC);

COMMENT ON TABLE public.body_measurements IS 'Body weight, body fat, measurements (supports Quick Entry)';

-- =============================================================================
-- 7. AI COACH: Conversations (Consolidated)
-- =============================================================================
-- Single table for all coach conversations (no need for personas table)

CREATE TABLE IF NOT EXISTS public.coach_messages (
    -- Identity
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Conversation threading
    conversation_id UUID NOT NULL, -- Group messages into conversations

    -- Message data
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
    content TEXT NOT NULL,

    -- RAG context used (for debugging/optimization)
    context_used JSONB, -- What embeddings were retrieved

    -- AI metadata
    ai_provider TEXT CHECK (ai_provider IN ('anthropic', 'groq', 'openai', 'openrouter')),
    ai_model TEXT,
    tokens_used INTEGER,
    cost_usd NUMERIC(10, 6),

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),

    -- Indexes below
    CONSTRAINT coach_messages_conversation_idx UNIQUE (conversation_id, created_at, id)
);

CREATE INDEX idx_coach_messages_user_id ON public.coach_messages(user_id);
CREATE INDEX idx_coach_messages_conversation ON public.coach_messages(conversation_id, created_at);
CREATE INDEX idx_coach_messages_user_recent ON public.coach_messages(user_id, created_at DESC);

-- RLS
ALTER TABLE public.coach_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own messages"
    ON public.coach_messages FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own messages"
    ON public.coach_messages FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Service role can insert assistant messages"
    ON public.coach_messages FOR INSERT
    WITH CHECK (auth.role() = 'service_role');

COMMENT ON TABLE public.coach_messages IS 'All AI coach conversation messages (supports RAG context)';

-- =============================================================================
-- 8. AI PROGRAMS: Consolidated (3 tables)
-- =============================================================================
-- Keep ai_generated_programs, ai_program_days, but consolidate meals+workouts

-- Table 1: Programs (keep as-is)
COMMENT ON TABLE public.ai_generated_programs IS 'AI-generated 12-week programs (workouts + meals)';

-- Table 2: Program days (keep as-is)
COMMENT ON TABLE public.ai_program_days IS 'Daily schedule within AI programs';

-- Table 3: Program items (NEW - consolidates meals + workouts)
CREATE TABLE IF NOT EXISTS public.ai_program_items (
    -- Identity
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_id UUID NOT NULL REFERENCES public.ai_generated_programs(id) ON DELETE CASCADE,
    program_day_id UUID NOT NULL REFERENCES public.ai_program_days(id) ON DELETE CASCADE,

    -- Item type
    item_type TEXT NOT NULL CHECK (item_type IN ('meal', 'workout', 'rest', 'note')),
    item_order INTEGER DEFAULT 0, -- Order within the day

    -- Meal data (if item_type = 'meal')
    meal_type TEXT CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack', 'pre_workout', 'post_workout')),
    meal_name TEXT,
    meal_foods JSONB DEFAULT '[]'::JSONB, -- Array of foods with portions
    meal_recipe TEXT,
    meal_calories NUMERIC,
    meal_protein_g NUMERIC,
    meal_carbs_g NUMERIC,
    meal_fat_g NUMERIC,

    -- Workout data (if item_type = 'workout')
    workout_name TEXT,
    workout_type TEXT CHECK (workout_type IN ('strength', 'cardio', 'sports', 'flexibility', 'mobility', 'active_recovery')),
    workout_duration_minutes INTEGER,
    workout_exercises JSONB DEFAULT '[]'::JSONB, -- Array of exercises with sets/reps
    workout_intensity TEXT CHECK (workout_intensity IN ('low', 'moderate', 'high', 'max')),
    workout_notes TEXT,

    -- Common fields
    description TEXT,
    notes TEXT,
    alternatives JSONB, -- Alternative options

    -- Completion tracking
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMPTZ,
    completion_notes TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_ai_program_items_program ON public.ai_program_items(program_id);
CREATE INDEX idx_ai_program_items_day ON public.ai_program_items(program_day_id);
CREATE INDEX idx_ai_program_items_type ON public.ai_program_items(item_type);

-- RLS
ALTER TABLE public.ai_program_items ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own program items"
    ON public.ai_program_items FOR SELECT
    USING (
        program_id IN (
            SELECT id FROM public.ai_generated_programs WHERE user_id = auth.uid()
        )
    );

CREATE POLICY "Users can update own program items"
    ON public.ai_program_items FOR UPDATE
    USING (
        program_id IN (
            SELECT id FROM public.ai_generated_programs WHERE user_id = auth.uid()
        )
    );

COMMENT ON TABLE public.ai_program_items IS 'Daily meals and workouts within AI programs (replaces separate meal/workout tables)';

-- Drop old separate tables
DROP TABLE IF EXISTS public.ai_program_meals CASCADE;
DROP TABLE IF EXISTS public.ai_program_workouts CASCADE;

-- =============================================================================
-- 9. INTEGRATIONS: Consolidated Connections
-- =============================================================================
-- Single table for all third-party integrations

CREATE TABLE IF NOT EXISTS public.integrations (
    -- Identity
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Integration type
    provider TEXT NOT NULL CHECK (provider IN ('strava', 'garmin', 'apple_health', 'google_fit', 'fitbit', 'polar', 'whoop')),

    -- Connection status
    is_active BOOLEAN DEFAULT TRUE,
    connected_at TIMESTAMPTZ DEFAULT NOW(),
    last_sync_at TIMESTAMPTZ,
    sync_enabled BOOLEAN DEFAULT TRUE,

    -- Provider-specific data
    provider_user_id TEXT, -- Their athlete/user ID
    provider_email TEXT,

    -- OAuth tokens (encrypted at application level)
    access_token TEXT,
    refresh_token TEXT,
    token_expires_at TIMESTAMPTZ,
    scope TEXT,

    -- Sync metadata
    sync_settings JSONB DEFAULT '{
        "auto_sync": true,
        "sync_activities": true,
        "sync_hr": true,
        "sync_sleep": false
    }'::JSONB,

    last_sync_status TEXT CHECK (last_sync_status IN ('success', 'failed', 'partial')),
    last_sync_error TEXT,

    -- Metadata
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    -- Unique per user per provider
    CONSTRAINT integrations_user_provider_key UNIQUE (user_id, provider)
);

CREATE INDEX idx_integrations_user ON public.integrations(user_id);
CREATE INDEX idx_integrations_provider ON public.integrations(provider);
CREATE INDEX idx_integrations_active ON public.integrations(user_id, is_active) WHERE is_active = TRUE;

-- RLS
ALTER TABLE public.integrations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own integrations"
    ON public.integrations FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can manage own integrations"
    ON public.integrations FOR ALL
    USING (auth.uid() = user_id);

COMMENT ON TABLE public.integrations IS 'Third-party integrations (Strava, Garmin, Apple Health, etc.)';

-- Drop old separate connection tables
DROP TABLE IF EXISTS public.strava_connections CASCADE;
DROP TABLE IF EXISTS public.garmin_connections CASCADE;

-- =============================================================================
-- 10. USER GOALS: Simplified
-- =============================================================================
-- Keep user_goals but simplify

COMMENT ON TABLE public.user_goals IS 'User fitness/nutrition goals with progress tracking';

CREATE INDEX IF NOT EXISTS idx_user_goals_user_active ON public.user_goals(user_id, is_active) WHERE is_active = TRUE;

-- =============================================================================
-- 11. WEBHOOKS: Keep for integrations
-- =============================================================================
COMMENT ON TABLE public.webhook_events IS 'Webhook events from Strava, Garmin, etc.';

-- =============================================================================
-- 12. RATE LIMITING: Keep
-- =============================================================================
COMMENT ON TABLE public.rate_limits IS 'API rate limiting per user per endpoint';

-- =============================================================================
-- 13. DAILY SUMMARIES: Keep
-- =============================================================================
COMMENT ON TABLE public.daily_nutrition_summaries IS 'Daily nutrition rollups for performance';

-- =============================================================================
-- UPDATED TRIGGERS
-- =============================================================================

-- Trigger: Update users.updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- =============================================================================
-- CONSOLIDATED VIEWS
-- =============================================================================

-- View: User dashboard summary
CREATE OR REPLACE VIEW public.user_dashboard AS
SELECT
    u.id AS user_id,
    u.full_name,
    u.primary_goal,
    u.experience_level,

    -- Quick stats
    (SELECT COUNT(*) FROM public.meal_logs WHERE user_id = u.id AND logged_at >= CURRENT_DATE) AS meals_today,
    (SELECT COUNT(*) FROM public.activities WHERE user_id = u.id AND start_date >= CURRENT_DATE) AS activities_today,
    (SELECT COUNT(*) FROM public.quick_entry_logs WHERE user_id = u.id AND logged_at >= CURRENT_DATE) AS quick_entries_today,

    -- Active program
    (SELECT name FROM public.ai_generated_programs WHERE user_id = u.id AND is_active = TRUE ORDER BY created_at DESC LIMIT 1) AS active_program_name,

    -- Recent weight
    (SELECT weight_kg FROM public.body_measurements WHERE user_id = u.id ORDER BY measured_at DESC LIMIT 1) AS current_weight_kg,

    -- Integrations
    (SELECT COUNT(*) FROM public.integrations WHERE user_id = u.id AND is_active = TRUE) AS active_integrations,

    u.last_active_at,
    u.created_at
FROM public.users u;

-- View: Recent user activity
CREATE OR REPLACE VIEW public.recent_user_activity AS
SELECT
    user_id,
    'meal' AS activity_type,
    id::TEXT AS activity_id,
    category::TEXT AS activity_subtype,
    logged_at AS activity_date,
    total_calories AS value1,
    total_protein_g AS value2
FROM public.meal_logs
UNION ALL
SELECT
    user_id,
    'activity' AS activity_type,
    id::TEXT AS activity_id,
    activity_type AS activity_subtype,
    start_date AS activity_date,
    distance_meters AS value1,
    elapsed_time_seconds::NUMERIC AS value2
FROM public.activities
UNION ALL
SELECT
    user_id,
    'quick_entry' AS activity_type,
    id::TEXT AS activity_id,
    ai_classification AS activity_subtype,
    logged_at AS activity_date,
    NULL AS value1,
    NULL AS value2
FROM public.quick_entry_logs
ORDER BY activity_date DESC;

-- =============================================================================
-- GRANT PERMISSIONS
-- =============================================================================

GRANT SELECT ON public.user_dashboard TO authenticated;
GRANT SELECT ON public.recent_user_activity TO authenticated;

-- =============================================================================
-- MIGRATION SUMMARY
-- =============================================================================

/*
BEFORE: 80+ tables (bloated, redundant, confusing)
AFTER:  13 core tables (clean, focused, production-ready)

CORE TABLES (13):
1. users - Consolidated profiles, settings, preferences
2. quick_entry_logs - Raw multimodal input
3. quick_entry_embeddings - Vector embeddings for RAG
4. meal_logs - Meal tracking
5. foods_enhanced - Food database
6. activities - All workouts/sports/activities
7. activity_segments - Activity details
8. activity_streams - Time-series data
9. body_measurements - Weight, body fat, etc.
10. coach_messages - AI coach conversations
11. ai_generated_programs - AI programs
12. ai_program_days - Program schedule
13. ai_program_items - Daily meals + workouts (consolidated)

SUPPORTING TABLES (kept):
- integrations (replaces strava_connections, garmin_connections)
- user_goals (simplified)
- webhook_events (needed for integrations)
- rate_limits (needed for API)
- daily_nutrition_summaries (performance optimization)
- quick_entry_stats (analytics)

REMOVED: 60+ obsolete tables including:
- All old workout/exercise tables
- Redundant embedding tables
- Over-engineered food tables
- Duplicate settings tables
- Obsolete program tables
- Unused feature tables (recipes, restaurants, etc.)

RESULT: Clean, maintainable, production-ready database
*/
