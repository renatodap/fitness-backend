-- ============================================================================
-- Quick Entry Schema Updates Migration
-- Created: 2025-01-05
-- Purpose: Update existing tables and create missing tables for quick entry
-- ============================================================================

-- ============================================================================
-- STEP 1: Update existing meal_logs table
-- ============================================================================

-- Add missing columns for quick entry functionality
ALTER TABLE meal_logs
  ADD COLUMN IF NOT EXISTS foods JSONB DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS source TEXT DEFAULT 'manual' CHECK (source IN ('quick_entry', 'manual', 'imported', 'api')),
  ADD COLUMN IF NOT EXISTS estimated BOOLEAN DEFAULT false,
  ADD COLUMN IF NOT EXISTS confidence_score DECIMAL(3,2) CHECK (confidence_score >= 0 AND confidence_score <= 1),
  ADD COLUMN IF NOT EXISTS image_url TEXT,
  ADD COLUMN IF NOT EXISTS meal_quality_score DECIMAL(4,2) CHECK (meal_quality_score >= 0 AND meal_quality_score <= 10),
  ADD COLUMN IF NOT EXISTS macro_balance_score DECIMAL(4,2) CHECK (macro_balance_score >= 0 AND macro_balance_score <= 10),
  ADD COLUMN IF NOT EXISTS adherence_to_goals DECIMAL(4,2) CHECK (adherence_to_goals >= 0 AND adherence_to_goals <= 10),
  ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT ARRAY[]::TEXT[],
  ADD COLUMN IF NOT EXISTS total_sugar_g DECIMAL(6,2),
  ADD COLUMN IF NOT EXISTS total_sodium_mg DECIMAL(7,2);

-- Add index for quick entry filtering
CREATE INDEX IF NOT EXISTS idx_meal_logs_source ON meal_logs(user_id, source);
CREATE INDEX IF NOT EXISTS idx_meal_logs_tags ON meal_logs USING GIN(tags);

-- Add comment
COMMENT ON COLUMN meal_logs.foods IS 'JSONB array of food items: [{"name": "Chicken", "quantity": "6 oz", "calories": 250}]';
COMMENT ON COLUMN meal_logs.meal_quality_score IS 'AI-generated quality score (0-10) based on nutrition balance';
COMMENT ON COLUMN meal_logs.tags IS 'Smart tags like ["high-protein", "meal-prep", "low-carb"]';

-- ============================================================================
-- STEP 2: Update existing activities table
-- ============================================================================

-- Add AI enrichment columns
ALTER TABLE activities
  ADD COLUMN IF NOT EXISTS performance_score DECIMAL(4,2) CHECK (performance_score >= 0 AND performance_score <= 10),
  ADD COLUMN IF NOT EXISTS effort_level DECIMAL(4,2) CHECK (effort_level >= 0 AND effort_level <= 10),
  ADD COLUMN IF NOT EXISTS recovery_needed_hours INTEGER,
  ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT ARRAY[]::TEXT[];

-- Update source constraint to include 'quick_entry'
ALTER TABLE activities DROP CONSTRAINT IF EXISTS activities_source_check;
ALTER TABLE activities ADD CONSTRAINT activities_source_check
  CHECK (source IN ('strava', 'garmin', 'manual', 'apple', 'fitbit', 'polar', 'suunto', 'wahoo', 'quick_entry'));

-- Add index
CREATE INDEX IF NOT EXISTS idx_activities_tags ON activities USING GIN(tags);

-- Add comments
COMMENT ON COLUMN activities.performance_score IS 'AI-calculated performance (0-10) compared to historical data';
COMMENT ON COLUMN activities.recovery_needed_hours IS 'AI-estimated recovery time needed';

-- ============================================================================
-- STEP 3: Update existing workout_completions table
-- ============================================================================

-- Add AI enrichment columns
ALTER TABLE workout_completions
  ADD COLUMN IF NOT EXISTS exercises JSONB DEFAULT '[]'::jsonb,
  ADD COLUMN IF NOT EXISTS volume_load INTEGER,
  ADD COLUMN IF NOT EXISTS estimated_calories INTEGER,
  ADD COLUMN IF NOT EXISTS muscle_groups TEXT[] DEFAULT ARRAY[]::TEXT[],
  ADD COLUMN IF NOT EXISTS progressive_overload_status TEXT CHECK (progressive_overload_status IN ('improving', 'maintaining', 'declining')),
  ADD COLUMN IF NOT EXISTS recovery_needed_hours INTEGER,
  ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT ARRAY[]::TEXT[];

-- Add indexes
CREATE INDEX IF NOT EXISTS idx_workout_completions_muscle_groups ON workout_completions USING GIN(muscle_groups);
CREATE INDEX IF NOT EXISTS idx_workout_completions_tags ON workout_completions USING GIN(tags);

-- Add comments
COMMENT ON COLUMN workout_completions.exercises IS 'JSONB array of exercises: [{"name": "Bench Press", "sets": [...]}]';
COMMENT ON COLUMN workout_completions.volume_load IS 'Total weight lifted (sets × reps × weight)';
COMMENT ON COLUMN workout_completions.progressive_overload_status IS 'AI-detected trend vs previous workouts';

-- ============================================================================
-- STEP 4: Create body_measurements table (NEW)
-- ============================================================================

CREATE TABLE IF NOT EXISTS body_measurements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Measurements
  measured_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  weight_lbs DECIMAL(6,2),
  weight_kg DECIMAL(6,2),
  body_fat_pct DECIMAL(4,2),
  muscle_mass_lbs DECIMAL(6,2),
  muscle_mass_kg DECIMAL(6,2),

  -- Detailed measurements (JSONB)
  -- Format: {"chest_in": 42.0, "waist_in": 32.0, "hips_in": 38.0, "arms_in": 15.5}
  measurements JSONB,

  -- Metadata
  source TEXT DEFAULT 'manual' CHECK (source IN ('manual', 'scale', 'dexa', 'inbody', 'quick_entry')),
  notes TEXT,

  -- AI enrichment
  trend_direction TEXT CHECK (trend_direction IN ('up', 'down', 'stable')),
  rate_of_change_weekly DECIMAL(5,2), -- Can be negative
  goal_progress_pct DECIMAL(5,2) CHECK (goal_progress_pct >= 0 AND goal_progress_pct <= 100),
  health_assessment TEXT CHECK (health_assessment IN ('healthy', 'caution', 'concern')),
  tags TEXT[] DEFAULT ARRAY[]::TEXT[],

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_body_measurements_user_time ON body_measurements(user_id, measured_at DESC);
CREATE INDEX idx_body_measurements_created ON body_measurements(user_id, created_at DESC);
CREATE INDEX idx_body_measurements_tags ON body_measurements USING GIN(tags);

-- RLS Policies
ALTER TABLE body_measurements ENABLE ROW LEVEL SECURITY;

CREATE POLICY body_measurements_select ON body_measurements
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY body_measurements_insert ON body_measurements
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY body_measurements_update ON body_measurements
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY body_measurements_delete ON body_measurements
  FOR DELETE USING (auth.uid() = user_id);

-- Comments
COMMENT ON TABLE body_measurements IS 'Tracks weight, body composition, and body measurements';
COMMENT ON COLUMN body_measurements.measurements IS 'JSONB object with detailed measurements (chest, waist, hips, arms, etc.)';
COMMENT ON COLUMN body_measurements.trend_direction IS 'AI-detected trend based on recent measurements';

-- ============================================================================
-- STEP 5: Create user_notes table (NEW)
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Note content
  title TEXT,
  content TEXT NOT NULL,
  category TEXT CHECK (category IN ('reflection', 'goal', 'plan', 'observation', 'general')),
  tags TEXT[] DEFAULT ARRAY[]::TEXT[],

  -- AI enrichment (sentiment analysis)
  sentiment TEXT CHECK (sentiment IN ('positive', 'neutral', 'negative')),
  sentiment_score DECIMAL(3,2) CHECK (sentiment_score >= -1 AND sentiment_score <= 1),
  detected_themes TEXT[] DEFAULT ARRAY[]::TEXT[],
  related_goals TEXT[] DEFAULT ARRAY[]::TEXT[],
  action_items TEXT[] DEFAULT ARRAY[]::TEXT[],

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_user_notes_user_time ON user_notes(user_id, created_at DESC);
CREATE INDEX idx_user_notes_category ON user_notes(user_id, category);
CREATE INDEX idx_user_notes_tags ON user_notes USING GIN(tags);

-- RLS Policies
ALTER TABLE user_notes ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_notes_select ON user_notes
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY user_notes_insert ON user_notes
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY user_notes_update ON user_notes
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY user_notes_delete ON user_notes
  FOR DELETE USING (auth.uid() = user_id);

-- Trigger for updated_at
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_user_notes_updated_at
  BEFORE UPDATE ON user_notes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Comments
COMMENT ON TABLE user_notes IS 'Stores user reflections, goals, plans, and observations';
COMMENT ON COLUMN user_notes.detected_themes IS 'AI-detected themes like ["motivation", "struggle", "progress"]';
COMMENT ON COLUMN user_notes.action_items IS 'AI-extracted action items from note content';

-- ============================================================================
-- STEP 6: Update user_onboarding with nutrition targets
-- ============================================================================

-- Add nutrition and goal fields
ALTER TABLE user_onboarding
  ADD COLUMN IF NOT EXISTS daily_calorie_target INTEGER,
  ADD COLUMN IF NOT EXISTS daily_protein_target_g INTEGER,
  ADD COLUMN IF NOT EXISTS daily_carbs_target_g INTEGER,
  ADD COLUMN IF NOT EXISTS daily_fat_target_g INTEGER,
  ADD COLUMN IF NOT EXISTS goal_weight_kg DECIMAL(6,2),
  ADD COLUMN IF NOT EXISTS goal_body_fat_pct DECIMAL(4,2),
  ADD COLUMN IF NOT EXISTS estimated_tdee INTEGER,
  ADD COLUMN IF NOT EXISTS goal_type TEXT CHECK (goal_type IN ('cut', 'bulk', 'maintain', 'recomp'));

-- Add comments
COMMENT ON COLUMN user_onboarding.daily_calorie_target IS 'Daily calorie target based on goals';
COMMENT ON COLUMN user_onboarding.estimated_tdee IS 'Estimated Total Daily Energy Expenditure';
COMMENT ON COLUMN user_onboarding.goal_type IS 'Weight goal: cut (lose), bulk (gain), maintain, or recomp';

-- ============================================================================
-- STEP 7: Helper functions for quick entry
-- ============================================================================

-- Function: Get recent meal stats
CREATE OR REPLACE FUNCTION get_recent_meal_stats(
  p_user_id UUID,
  p_days INTEGER DEFAULT 7
)
RETURNS TABLE (
  total_meals BIGINT,
  avg_calories DECIMAL,
  avg_protein DECIMAL,
  avg_carbs DECIMAL,
  avg_fat DECIMAL,
  avg_quality_score DECIMAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    COUNT(*)::BIGINT,
    AVG(total_calories),
    AVG(total_protein_g),
    AVG(total_carbs_g),
    AVG(total_fat_g),
    AVG(meal_quality_score)
  FROM meal_logs
  WHERE user_id = p_user_id
    AND logged_at >= NOW() - (p_days || ' days')::INTERVAL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Get recent workout stats
CREATE OR REPLACE FUNCTION get_recent_workout_stats(
  p_user_id UUID,
  p_days INTEGER DEFAULT 7
)
RETURNS TABLE (
  total_workouts BIGINT,
  total_volume_load BIGINT,
  avg_duration_minutes DECIMAL,
  avg_rpe DECIMAL,
  progressive_overload_count BIGINT
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    COUNT(*)::BIGINT,
    SUM(volume_load)::BIGINT,
    AVG(duration_minutes),
    AVG(rpe::DECIMAL),
    COUNT(CASE WHEN progressive_overload_status = 'improving' THEN 1 END)::BIGINT
  FROM workout_completions
  WHERE user_id = p_user_id
    AND started_at >= NOW() - (p_days || ' days')::INTERVAL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Get recent activity stats
CREATE OR REPLACE FUNCTION get_recent_activity_stats(
  p_user_id UUID,
  p_days INTEGER DEFAULT 7
)
RETURNS TABLE (
  total_activities BIGINT,
  total_distance_km DECIMAL,
  total_time_minutes DECIMAL,
  total_calories BIGINT,
  avg_performance_score DECIMAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    COUNT(*)::BIGINT,
    SUM(distance_meters / 1000.0)::DECIMAL,
    SUM(elapsed_time_seconds / 60.0)::DECIMAL,
    SUM(calories)::BIGINT,
    AVG(performance_score)
  FROM activities
  WHERE user_id = p_user_id
    AND start_date >= NOW() - (p_days || ' days')::INTERVAL;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- Function: Semantic search using existing multimodal_embeddings table
CREATE OR REPLACE FUNCTION semantic_search_quick_entry(
  p_user_id UUID,
  p_query_embedding vector(384),
  p_source_type TEXT DEFAULT NULL,
  p_limit INTEGER DEFAULT 10,
  p_recency_weight DECIMAL DEFAULT 0.3
)
RETURNS TABLE (
  id UUID,
  source_type TEXT,
  source_id UUID,
  content_text TEXT,
  metadata JSONB,
  similarity DECIMAL,
  recency_score DECIMAL,
  final_score DECIMAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    e.id,
    e.source_type,
    e.source_id,
    e.content_text,
    e.metadata,
    (1 - (e.embedding <=> p_query_embedding))::DECIMAL AS similarity,
    EXP(-EXTRACT(EPOCH FROM (NOW() - e.created_at)) / (86400 * 30))::DECIMAL AS recency_score,
    ((1 - p_recency_weight) * (1 - (e.embedding <=> p_query_embedding)) +
     p_recency_weight * EXP(-EXTRACT(EPOCH FROM (NOW() - e.created_at)) / (86400 * 30)))::DECIMAL AS final_score
  FROM multimodal_embeddings e
  WHERE e.user_id = p_user_id
    AND (p_source_type IS NULL OR e.source_type = p_source_type)
  ORDER BY final_score DESC
  LIMIT p_limit;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

-- ============================================================================
-- VERIFICATION & SUMMARY
-- ============================================================================

DO $$
DECLARE
  meal_logs_foods_exists BOOLEAN;
  activities_tags_exists BOOLEAN;
  workouts_exercises_exists BOOLEAN;
  body_measurements_exists BOOLEAN;
  user_notes_exists BOOLEAN;
BEGIN
  -- Check if migrations applied successfully
  SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'meal_logs' AND column_name = 'foods'
  ) INTO meal_logs_foods_exists;

  SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'activities' AND column_name = 'tags'
  ) INTO activities_tags_exists;

  SELECT EXISTS (
    SELECT 1 FROM information_schema.columns
    WHERE table_name = 'workout_completions' AND column_name = 'exercises'
  ) INTO workouts_exercises_exists;

  SELECT EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'body_measurements'
  ) INTO body_measurements_exists;

  SELECT EXISTS (
    SELECT 1 FROM information_schema.tables
    WHERE table_schema = 'public' AND table_name = 'user_notes'
  ) INTO user_notes_exists;

  -- Print summary
  RAISE NOTICE '============================================';
  RAISE NOTICE 'Quick Entry Schema Migration Complete!';
  RAISE NOTICE '============================================';
  RAISE NOTICE 'Updated Tables:';
  RAISE NOTICE '  ✓ meal_logs: Added foods column: %', meal_logs_foods_exists;
  RAISE NOTICE '  ✓ activities: Added tags column: %', activities_tags_exists;
  RAISE NOTICE '  ✓ workout_completions: Added exercises column: %', workouts_exercises_exists;
  RAISE NOTICE '';
  RAISE NOTICE 'Created Tables:';
  RAISE NOTICE '  ✓ body_measurements: %', body_measurements_exists;
  RAISE NOTICE '  ✓ user_notes: %', user_notes_exists;
  RAISE NOTICE '';
  RAISE NOTICE 'Helper Functions: 4 created';
  RAISE NOTICE 'RLS Policies: Enabled on new tables';
  RAISE NOTICE '';
  RAISE NOTICE 'Next Steps:';
  RAISE NOTICE '1. Update quick_entry_service.py to use correct columns';
  RAISE NOTICE '2. Integrate Groq API for cost optimization';
  RAISE NOTICE '3. Add enrichment functions (quality scores, tags)';
  RAISE NOTICE '4. Test end-to-end quick entry flow';
  RAISE NOTICE '============================================';
END $$;
