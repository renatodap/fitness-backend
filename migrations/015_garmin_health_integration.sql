-- Migration 015: Garmin Health Integration
-- Creates comprehensive health tracking tables for Garmin data + manual entry
-- Adds activity deduplication fields
-- Created: 2025-10-09

-- ============================================================================
-- TABLE 1: sleep_logs
-- Tracks sleep data from Garmin auto-sync OR manual entry
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.sleep_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  sleep_date DATE NOT NULL,

  -- Time range
  sleep_start TIMESTAMPTZ NOT NULL,
  sleep_end TIMESTAMPTZ NOT NULL,

  -- Duration breakdown (minutes)
  total_sleep_minutes INTEGER CHECK (total_sleep_minutes >= 0 AND total_sleep_minutes <= 1440),
  deep_sleep_minutes INTEGER CHECK (deep_sleep_minutes >= 0),
  light_sleep_minutes INTEGER CHECK (light_sleep_minutes >= 0),
  rem_sleep_minutes INTEGER CHECK (rem_sleep_minutes >= 0),
  awake_minutes INTEGER CHECK (awake_minutes >= 0),

  -- Quality metrics
  sleep_score INTEGER CHECK (sleep_score >= 0 AND sleep_score <= 100),
  sleep_quality TEXT CHECK (sleep_quality IN ('poor', 'fair', 'good', 'excellent')),
  interruptions INTEGER DEFAULT 0 CHECK (interruptions >= 0),
  restlessness_level INTEGER CHECK (restlessness_level >= 0 AND restlessness_level <= 10),

  -- Physiological metrics (optional, from sensors)
  avg_hrv_ms NUMERIC CHECK (avg_hrv_ms >= 0),
  avg_heart_rate INTEGER CHECK (avg_heart_rate > 0 AND avg_heart_rate < 200),
  lowest_heart_rate INTEGER CHECK (lowest_heart_rate > 0 AND lowest_heart_rate < 200),
  avg_respiration_rate NUMERIC CHECK (avg_respiration_rate >= 0 AND avg_respiration_rate <= 60),
  avg_spo2_percentage NUMERIC CHECK (avg_spo2_percentage >= 0 AND avg_spo2_percentage <= 100),

  -- Data source
  source TEXT DEFAULT 'manual' CHECK (source IN ('garmin', 'apple', 'fitbit', 'whoop', 'oura', 'manual')),
  entry_method TEXT DEFAULT 'form' CHECK (entry_method IN ('auto_sync', 'form', 'quick_entry', 'voice')),

  -- Notes
  notes TEXT CHECK (char_length(notes) <= 1000),

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Unique constraint: one sleep log per user per date
  CONSTRAINT unique_sleep_per_user_date UNIQUE (user_id, sleep_date)
);

-- Indexes for sleep_logs
CREATE INDEX idx_sleep_logs_user_date ON public.sleep_logs(user_id, sleep_date DESC);
CREATE INDEX idx_sleep_logs_source ON public.sleep_logs(user_id, source);

-- RLS for sleep_logs
ALTER TABLE public.sleep_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own sleep logs"
  ON public.sleep_logs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own sleep logs"
  ON public.sleep_logs FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own sleep logs"
  ON public.sleep_logs FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own sleep logs"
  ON public.sleep_logs FOR DELETE
  USING (auth.uid() = user_id);


-- ============================================================================
-- TABLE 2: daily_readiness
-- Tracks daily readiness score and all contributing factors
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.daily_readiness (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,

  -- Overall readiness
  readiness_score INTEGER CHECK (readiness_score >= 0 AND readiness_score <= 100),
  readiness_status TEXT CHECK (readiness_status IN ('poor', 'low', 'balanced', 'high', 'optimal')),

  -- Objective factors (from sensors)
  sleep_score INTEGER CHECK (sleep_score >= 0 AND sleep_score <= 100),
  hrv_status TEXT CHECK (hrv_status IN ('poor', 'unbalanced', 'balanced', 'excellent')),
  resting_heart_rate INTEGER CHECK (resting_heart_rate > 0 AND resting_heart_rate < 200),
  recovery_time_hours INTEGER CHECK (recovery_time_hours >= 0 AND recovery_time_hours <= 168),

  -- Subjective factors (from user check-ins)
  energy_level INTEGER CHECK (energy_level >= 1 AND energy_level <= 10),
  soreness_level INTEGER CHECK (soreness_level >= 0 AND soreness_level <= 10),
  stress_level INTEGER CHECK (stress_level >= 0 AND stress_level <= 10),
  mood TEXT CHECK (mood IN ('terrible', 'bad', 'okay', 'good', 'amazing')),
  motivation_level INTEGER CHECK (motivation_level >= 1 AND motivation_level <= 10),

  -- Optional: manual sleep quality rating (1-5 stars)
  sleep_quality_rating INTEGER CHECK (sleep_quality_rating >= 1 AND sleep_quality_rating <= 5),
  sleep_hours_estimate NUMERIC CHECK (sleep_hours_estimate >= 0 AND sleep_hours_estimate <= 24),

  -- Training context (auto-calculated or from Garmin)
  acute_training_load NUMERIC CHECK (acute_training_load >= 0),
  chronic_training_load NUMERIC CHECK (chronic_training_load >= 0),
  load_ratio NUMERIC CHECK (load_ratio >= 0 AND load_ratio <= 3),
  training_status TEXT CHECK (training_status IN ('detraining', 'maintaining', 'productive', 'peaking', 'overreaching', 'unproductive')),

  -- Data source tracking
  source TEXT DEFAULT 'manual',
  calculation_method TEXT CHECK (calculation_method IN ('auto_garmin', 'auto_calculated', 'manual_full', 'manual_partial')),
  factors_used JSONB DEFAULT '{}',
  notes TEXT CHECK (char_length(notes) <= 1000),

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Unique constraint
  CONSTRAINT unique_readiness_per_user_date UNIQUE (user_id, date)
);

-- Indexes for daily_readiness
CREATE INDEX idx_readiness_user_date ON public.daily_readiness(user_id, date DESC);
CREATE INDEX idx_readiness_score ON public.daily_readiness(user_id, readiness_score DESC);

-- RLS for daily_readiness
ALTER TABLE public.daily_readiness ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own readiness data"
  ON public.daily_readiness FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own readiness data"
  ON public.daily_readiness FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own readiness data"
  ON public.daily_readiness FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own readiness data"
  ON public.daily_readiness FOR DELETE
  USING (auth.uid() = user_id);


-- ============================================================================
-- TABLE 3: hrv_logs
-- Tracks HRV measurements
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.hrv_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  recorded_at TIMESTAMPTZ NOT NULL,

  -- HRV metrics
  hrv_rmssd_ms NUMERIC NOT NULL CHECK (hrv_rmssd_ms >= 0 AND hrv_rmssd_ms <= 300),
  hrv_sdrr_ms NUMERIC CHECK (hrv_sdrr_ms >= 0),
  measurement_type TEXT CHECK (measurement_type IN ('sleep', 'morning', 'resting', 'workout', 'manual')),

  -- Context
  quality_score INTEGER CHECK (quality_score >= 0 AND quality_score <= 100),
  baseline_deviation NUMERIC,  -- Percentage deviation from user's baseline
  status TEXT CHECK (status IN ('low', 'unbalanced', 'balanced', 'high')),

  -- Source
  source TEXT DEFAULT 'manual',
  measurement_device TEXT,  -- e.g., 'garmin_watch', 'chest_strap', 'phone_app', 'manual_estimate'

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for hrv_logs
CREATE INDEX idx_hrv_logs_user_time ON public.hrv_logs(user_id, recorded_at DESC);
-- Note: Removed DATE(recorded_at) index - can query efficiently using recorded_at with date ranges

-- RLS for hrv_logs
ALTER TABLE public.hrv_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own HRV logs"
  ON public.hrv_logs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own HRV logs"
  ON public.hrv_logs FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own HRV logs"
  ON public.hrv_logs FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own HRV logs"
  ON public.hrv_logs FOR DELETE
  USING (auth.uid() = user_id);


-- ============================================================================
-- TABLE 4: stress_logs
-- Tracks daily stress levels
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.stress_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,

  -- Garmin all-day stress (0-100)
  avg_stress_level INTEGER CHECK (avg_stress_level >= 0 AND avg_stress_level <= 100),
  max_stress_level INTEGER CHECK (max_stress_level >= 0 AND max_stress_level <= 100),
  rest_stress_level INTEGER CHECK (rest_stress_level >= 0 AND rest_stress_level <= 100),

  -- Manual spot measurements (0-10 scale)
  morning_stress INTEGER CHECK (morning_stress >= 0 AND morning_stress <= 10),
  afternoon_stress INTEGER CHECK (afternoon_stress >= 0 AND afternoon_stress <= 10),
  evening_stress INTEGER CHECK (evening_stress >= 0 AND evening_stress <= 10),

  -- Time in stress zones (Garmin continuous tracking)
  rest_minutes INTEGER DEFAULT 0 CHECK (rest_minutes >= 0),       -- Stress 0-25
  low_stress_minutes INTEGER DEFAULT 0 CHECK (low_stress_minutes >= 0),  -- Stress 26-50
  medium_stress_minutes INTEGER DEFAULT 0 CHECK (medium_stress_minutes >= 0), -- Stress 51-75
  high_stress_minutes INTEGER DEFAULT 0 CHECK (high_stress_minutes >= 0),  -- Stress 76-100

  -- Stress events timeline (JSONB: [{time, level, duration}, ...])
  stress_events JSONB DEFAULT '[]',

  -- Notes
  notes TEXT CHECK (char_length(notes) <= 1000),

  -- Source
  source TEXT DEFAULT 'manual',

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Unique constraint
  CONSTRAINT unique_stress_per_user_date UNIQUE (user_id, date)
);

-- Indexes for stress_logs
CREATE INDEX idx_stress_logs_user_date ON public.stress_logs(user_id, date DESC);

-- RLS for stress_logs
ALTER TABLE public.stress_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own stress logs"
  ON public.stress_logs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own stress logs"
  ON public.stress_logs FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own stress logs"
  ON public.stress_logs FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own stress logs"
  ON public.stress_logs FOR DELETE
  USING (auth.uid() = user_id);


-- ============================================================================
-- TABLE 5: body_battery_logs
-- Tracks Garmin Body Battery or manual energy levels
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.body_battery_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,

  -- Garmin Body Battery (0-100)
  starting_level INTEGER CHECK (starting_level >= 0 AND starting_level <= 100),
  ending_level INTEGER CHECK (ending_level >= 0 AND ending_level <= 100),
  lowest_level INTEGER CHECK (lowest_level >= 0 AND lowest_level <= 100),
  highest_level INTEGER CHECK (highest_level >= 0 AND highest_level <= 100),

  -- Drain vs recharge totals
  total_drain INTEGER CHECK (total_drain >= 0),
  total_recharge INTEGER CHECK (total_recharge >= 0),

  -- Manual energy tracking alternative (simpler for non-Garmin users)
  morning_energy INTEGER CHECK (morning_energy >= 1 AND morning_energy <= 10),
  afternoon_energy INTEGER CHECK (afternoon_energy >= 1 AND afternoon_energy <= 10),
  evening_energy INTEGER CHECK (evening_energy >= 1 AND evening_energy <= 10),

  -- Detailed timeline (JSONB: [{timestamp, level, event: 'sleep'|'activity'|'stress'|'rest'}, ...])
  timeline JSONB,

  -- Notes
  notes TEXT CHECK (char_length(notes) <= 1000),

  -- Source
  source TEXT DEFAULT 'manual',

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Unique constraint
  CONSTRAINT unique_body_battery_per_user_date UNIQUE (user_id, date)
);

-- Indexes for body_battery_logs
CREATE INDEX idx_body_battery_user_date ON public.body_battery_logs(user_id, date DESC);

-- RLS for body_battery_logs
ALTER TABLE public.body_battery_logs ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own body battery logs"
  ON public.body_battery_logs FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own body battery logs"
  ON public.body_battery_logs FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own body battery logs"
  ON public.body_battery_logs FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own body battery logs"
  ON public.body_battery_logs FOR DELETE
  USING (auth.uid() = user_id);


-- ============================================================================
-- TABLE 6: daily_steps_and_activity
-- Tracks daily steps, intensity minutes, floors, calories
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.daily_steps_and_activity (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,

  -- Steps
  total_steps INTEGER DEFAULT 0 CHECK (total_steps >= 0),
  step_goal INTEGER CHECK (step_goal >= 0),
  distance_meters NUMERIC CHECK (distance_meters >= 0),

  -- Intensity minutes (WHO guidelines: 150 moderate OR 75 vigorous per week)
  moderate_intensity_minutes INTEGER DEFAULT 0 CHECK (moderate_intensity_minutes >= 0),
  vigorous_intensity_minutes INTEGER DEFAULT 0 CHECK (vigorous_intensity_minutes >= 0),

  -- Other movement
  floors_climbed INTEGER DEFAULT 0 CHECK (floors_climbed >= 0),
  floors_goal INTEGER CHECK (floors_goal >= 0),

  -- Calories
  total_calories INTEGER CHECK (total_calories >= 0),
  active_calories INTEGER CHECK (active_calories >= 0),
  bmr_calories INTEGER CHECK (bmr_calories >= 0),

  -- Move IQ events (auto-detected activities)
  move_iq_events JSONB DEFAULT '[]',

  -- Source
  source TEXT DEFAULT 'manual',

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Unique constraint
  CONSTRAINT unique_steps_per_user_date UNIQUE (user_id, date)
);

-- Indexes for daily_steps_and_activity
CREATE INDEX idx_steps_user_date ON public.daily_steps_and_activity(user_id, date DESC);

-- RLS for daily_steps_and_activity
ALTER TABLE public.daily_steps_and_activity ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own steps data"
  ON public.daily_steps_and_activity FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own steps data"
  ON public.daily_steps_and_activity FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own steps data"
  ON public.daily_steps_and_activity FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own steps data"
  ON public.daily_steps_and_activity FOR DELETE
  USING (auth.uid() = user_id);


-- ============================================================================
-- TABLE 7: training_load_history
-- Tracks training load (TSS), acute/chronic load, training status
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.training_load_history (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date DATE NOT NULL,

  -- Training load (TSS-based)
  acute_load NUMERIC CHECK (acute_load >= 0),      -- Last 7 days total
  chronic_load NUMERIC CHECK (chronic_load >= 0),  -- Last 42 days average
  load_ratio NUMERIC CHECK (load_ratio >= 0 AND load_ratio <= 3),  -- Acute/Chronic

  -- Load distribution
  load_focus TEXT CHECK (load_focus IN ('anaerobic', 'high_aerobic', 'low_aerobic', 'mixed')),
  load_breakdown JSONB,  -- {anaerobic: 20, high_aerobic: 50, low_aerobic: 30}

  -- Training status (Garmin or calculated)
  training_status TEXT CHECK (training_status IN ('detraining', 'maintaining', 'productive', 'peaking', 'overreaching', 'unproductive')),
  training_effect_label TEXT,  -- 'No Benefit', 'Minor', 'Maintaining', 'Improving', 'Highly Improving'

  -- VO2 Max tracking
  vo2max_estimate NUMERIC CHECK (vo2max_estimate >= 0 AND vo2max_estimate <= 100),
  fitness_age INTEGER CHECK (fitness_age >= 10 AND fitness_age <= 120),

  -- Lactate threshold (for runners/cyclists)
  lactate_threshold_hr INTEGER CHECK (lactate_threshold_hr > 0 AND lactate_threshold_hr < 220),
  lactate_threshold_pace NUMERIC,  -- seconds per km

  -- Source
  source TEXT DEFAULT 'calculated',

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Unique constraint
  CONSTRAINT unique_training_load_per_user_date UNIQUE (user_id, date)
);

-- Indexes for training_load_history
CREATE INDEX idx_training_load_user_date ON public.training_load_history(user_id, date DESC);
CREATE INDEX idx_training_load_status ON public.training_load_history(user_id, training_status);

-- RLS for training_load_history
ALTER TABLE public.training_load_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own training load"
  ON public.training_load_history FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own training load"
  ON public.training_load_history FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own training load"
  ON public.training_load_history FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own training load"
  ON public.training_load_history FOR DELETE
  USING (auth.uid() = user_id);


-- ============================================================================
-- ACTIVITY DEDUPLICATION FIELDS
-- Add fields to existing activities table for duplicate detection
-- ============================================================================

-- Add deduplication fields to activities table
ALTER TABLE public.activities
  ADD COLUMN IF NOT EXISTS is_duplicate BOOLEAN DEFAULT FALSE,
  ADD COLUMN IF NOT EXISTS merged_into_id UUID REFERENCES public.activities(id) ON DELETE SET NULL,
  ADD COLUMN IF NOT EXISTS merged_from_sources TEXT[] DEFAULT '{}',
  ADD COLUMN IF NOT EXISTS merge_count INTEGER DEFAULT 0;

-- Index for efficient duplicate queries
CREATE INDEX IF NOT EXISTS idx_activities_duplicates
  ON public.activities(user_id, is_duplicate, start_date)
  WHERE is_duplicate = FALSE;

-- Index for merged activities lookup
CREATE INDEX IF NOT EXISTS idx_activities_merged_into
  ON public.activities(merged_into_id)
  WHERE merged_into_id IS NOT NULL;


-- ============================================================================
-- ACTIVITY MERGE REQUESTS TABLE
-- Tracks pending user decisions on duplicate activities
-- ============================================================================
CREATE TABLE IF NOT EXISTS public.activity_merge_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- The two activities in question
  new_activity_id UUID NOT NULL REFERENCES public.activities(id) ON DELETE CASCADE,
  existing_activity_id UUID NOT NULL REFERENCES public.activities(id) ON DELETE CASCADE,

  -- Confidence score (0-1) that these are duplicates
  confidence NUMERIC NOT NULL CHECK (confidence >= 0 AND confidence <= 1),

  -- Status
  status TEXT DEFAULT 'pending' CHECK (status IN ('pending', 'merged', 'kept_separate', 'dismissed')),

  -- User decision
  user_decision TEXT CHECK (user_decision IN ('merge', 'keep_both', 'delete_new', 'delete_existing')),
  decided_at TIMESTAMPTZ,

  -- Notes
  system_reasoning TEXT,
  user_notes TEXT,

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for activity_merge_requests
CREATE INDEX idx_merge_requests_user_status ON public.activity_merge_requests(user_id, status);
CREATE INDEX idx_merge_requests_created ON public.activity_merge_requests(created_at DESC);

-- RLS for activity_merge_requests
ALTER TABLE public.activity_merge_requests ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own merge requests"
  ON public.activity_merge_requests FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can update own merge requests"
  ON public.activity_merge_requests FOR UPDATE
  USING (auth.uid() = user_id);


-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Function to calculate HRV baseline (7-day rolling average)
CREATE OR REPLACE FUNCTION public.calculate_hrv_baseline(
  p_user_id UUID,
  p_end_date DATE DEFAULT NULL
)
RETURNS NUMERIC AS $$
DECLARE
  baseline NUMERIC;
  end_date_param DATE;
BEGIN
  -- Use provided date or default to current date
  end_date_param := COALESCE(p_end_date, CURRENT_DATE);

  SELECT AVG(hrv_rmssd_ms)
  INTO baseline
  FROM public.hrv_logs
  WHERE user_id = p_user_id
    AND DATE(recorded_at) > (end_date_param - INTERVAL '7 days')
    AND DATE(recorded_at) <= end_date_param
    AND quality_score >= 70  -- Only include quality measurements
  GROUP BY user_id;

  RETURN baseline;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- Function to calculate acute training load (7 days)
CREATE OR REPLACE FUNCTION public.calculate_acute_load(
  p_user_id UUID,
  p_end_date DATE DEFAULT NULL
)
RETURNS NUMERIC AS $$
DECLARE
  load NUMERIC;
  end_date_param DATE;
BEGIN
  -- Use provided date or default to current date
  end_date_param := COALESCE(p_end_date, CURRENT_DATE);

  SELECT SUM(COALESCE(tss, 0))
  INTO load
  FROM public.activities
  WHERE user_id = p_user_id
    AND DATE(start_date) > (end_date_param - INTERVAL '7 days')
    AND DATE(start_date) <= end_date_param
    AND is_duplicate = FALSE;

  RETURN COALESCE(load, 0);
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- Function to calculate chronic training load (42 days average)
CREATE OR REPLACE FUNCTION public.calculate_chronic_load(
  p_user_id UUID,
  p_end_date DATE DEFAULT NULL
)
RETURNS NUMERIC AS $$
DECLARE
  load NUMERIC;
  end_date_param DATE;
BEGIN
  -- Use provided date or default to current date
  end_date_param := COALESCE(p_end_date, CURRENT_DATE);

  SELECT AVG(daily_tss)
  INTO load
  FROM (
    SELECT DATE(start_date) as activity_date, SUM(COALESCE(tss, 0)) as daily_tss
    FROM public.activities
    WHERE user_id = p_user_id
      AND DATE(start_date) > (end_date_param - INTERVAL '42 days')
      AND DATE(start_date) <= end_date_param
      AND is_duplicate = FALSE
    GROUP BY DATE(start_date)
  ) daily_loads;

  RETURN COALESCE(load, 0);
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;


-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

-- Add comment to track migration
COMMENT ON TABLE public.sleep_logs IS 'Migration 015: Sleep tracking with Garmin auto-sync + manual entry support';
COMMENT ON TABLE public.daily_readiness IS 'Migration 015: Daily readiness scores with adaptive calculation';
COMMENT ON TABLE public.hrv_logs IS 'Migration 015: Heart rate variability tracking';
COMMENT ON TABLE public.stress_logs IS 'Migration 015: Daily stress level tracking';
COMMENT ON TABLE public.body_battery_logs IS 'Migration 015: Garmin Body Battery or manual energy tracking';
COMMENT ON TABLE public.daily_steps_and_activity IS 'Migration 015: Daily steps, intensity minutes, and calories';
COMMENT ON TABLE public.training_load_history IS 'Migration 015: Training load tracking with TSS';
COMMENT ON TABLE public.activity_merge_requests IS 'Migration 015: Activity deduplication user review system';
