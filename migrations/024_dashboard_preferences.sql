-- Migration: Dashboard Preferences and Behavior Tracking
-- Description: Adds dashboard personalization system with auto-detection
-- Date: 2025-10-11

-- ============================================================================
-- PHASE 1: Profile Dashboard Preferences
-- ============================================================================

-- Add dashboard preference columns to profiles
ALTER TABLE profiles
ADD COLUMN IF NOT EXISTS dashboard_preference TEXT DEFAULT 'balanced'
  CHECK (dashboard_preference IN ('simple', 'balanced', 'detailed')),
ADD COLUMN IF NOT EXISTS shows_weight_card BOOLEAN DEFAULT NULL,
ADD COLUMN IF NOT EXISTS shows_recovery_card BOOLEAN DEFAULT NULL,
ADD COLUMN IF NOT EXISTS shows_workout_card BOOLEAN DEFAULT TRUE,
ADD COLUMN IF NOT EXISTS weight_tracking_detected_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS recovery_tracking_detected_at TIMESTAMPTZ,
ADD COLUMN IF NOT EXISTS dashboard_preference_set_at TIMESTAMPTZ;

-- Create index for dashboard preference queries
CREATE INDEX IF NOT EXISTS idx_profiles_dashboard_preference
ON profiles(dashboard_preference);

-- ============================================================================
-- PHASE 2: Behavior Tracking
-- ============================================================================

-- User behavior signals for adaptive dashboard
CREATE TABLE IF NOT EXISTS user_behavior_signals (
  user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Engagement metrics
  macro_views INT DEFAULT 0,
  weight_logs INT DEFAULT 0,
  plan_interactions INT DEFAULT 0,
  coach_messages INT DEFAULT 0,
  daily_opens_avg FLOAT DEFAULT 0,
  recovery_logs INT DEFAULT 0,

  -- Card-specific interactions
  expanded_cards JSONB DEFAULT '[]'::jsonb,

  -- Tracking window
  tracking_started_at TIMESTAMPTZ DEFAULT NOW(),
  last_updated_at TIMESTAMPTZ DEFAULT NOW(),
  last_adaptation_shown_at TIMESTAMPTZ,

  -- Metadata
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create index for behavior queries
CREATE INDEX IF NOT EXISTS idx_user_behavior_signals_user_id
ON user_behavior_signals(user_id);

CREATE INDEX IF NOT EXISTS idx_user_behavior_signals_last_updated
ON user_behavior_signals(last_updated_at);

-- ============================================================================
-- PHASE 3: Dashboard Adaptations Log
-- ============================================================================

-- Track dashboard adaptation suggestions and user responses
CREATE TABLE IF NOT EXISTS dashboard_adaptations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Adaptation details
  adaptation_type TEXT NOT NULL,
  -- Types: 'dashboard_variant_change', 'card_added', 'card_removed',
  --        'card_priority_changed', 'feature_suggestion'

  old_value TEXT,
  new_value TEXT,

  -- Context
  reason TEXT NOT NULL,
  trigger_data JSONB DEFAULT '{}'::jsonb,

  -- User response
  user_accepted BOOLEAN,
  user_feedback TEXT,

  -- Timestamps
  suggested_at TIMESTAMPTZ DEFAULT NOW(),
  responded_at TIMESTAMPTZ,

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Create indexes for adaptation queries
CREATE INDEX IF NOT EXISTS idx_dashboard_adaptations_user_id
ON dashboard_adaptations(user_id);

CREATE INDEX IF NOT EXISTS idx_dashboard_adaptations_type
ON dashboard_adaptations(adaptation_type);

CREATE INDEX IF NOT EXISTS idx_dashboard_adaptations_suggested_at
ON dashboard_adaptations(suggested_at DESC);

-- ============================================================================
-- PHASE 4: Helper Functions
-- ============================================================================

-- Function to increment behavior signal
CREATE OR REPLACE FUNCTION increment_behavior_signal(
  p_user_id UUID,
  p_signal_type TEXT,
  p_increment INT DEFAULT 1
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN
  -- Insert or update behavior signal
  INSERT INTO user_behavior_signals (user_id)
  VALUES (p_user_id)
  ON CONFLICT (user_id) DO NOTHING;

  -- Update specific signal
  CASE p_signal_type
    WHEN 'macro_views' THEN
      UPDATE user_behavior_signals
      SET macro_views = macro_views + p_increment,
          last_updated_at = NOW()
      WHERE user_id = p_user_id;

    WHEN 'weight_logs' THEN
      UPDATE user_behavior_signals
      SET weight_logs = weight_logs + p_increment,
          last_updated_at = NOW()
      WHERE user_id = p_user_id;

    WHEN 'plan_interactions' THEN
      UPDATE user_behavior_signals
      SET plan_interactions = plan_interactions + p_increment,
          last_updated_at = NOW()
      WHERE user_id = p_user_id;

    WHEN 'coach_messages' THEN
      UPDATE user_behavior_signals
      SET coach_messages = coach_messages + p_increment,
          last_updated_at = NOW()
      WHERE user_id = p_user_id;

    WHEN 'recovery_logs' THEN
      UPDATE user_behavior_signals
      SET recovery_logs = recovery_logs + p_increment,
          last_updated_at = NOW()
      WHERE user_id = p_user_id;

    ELSE
      -- Unknown signal type, do nothing
      NULL;
  END CASE;
END;
$$;

-- Function to check if weight card should be shown
CREATE OR REPLACE FUNCTION should_show_weight_card(p_user_id UUID)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
  weight_logs_count INT;
  explicit_preference BOOLEAN;
BEGIN
  -- Check explicit preference first
  SELECT shows_weight_card INTO explicit_preference
  FROM profiles
  WHERE id = p_user_id;

  -- If explicitly set, use that
  IF explicit_preference IS NOT NULL THEN
    RETURN explicit_preference;
  END IF;

  -- Otherwise, auto-detect based on recent logs
  -- Count weight measurements in last 14 days
  SELECT COUNT(*) INTO weight_logs_count
  FROM measurements
  WHERE user_id = p_user_id
    AND measurement_type = 'weight'
    AND measurement_date >= NOW() - INTERVAL '14 days';

  -- Show if 2+ logs in last 14 days
  RETURN weight_logs_count >= 2;
END;
$$;

-- Function to check if recovery card should be shown
CREATE OR REPLACE FUNCTION should_show_recovery_card(p_user_id UUID)
RETURNS BOOLEAN
LANGUAGE plpgsql
AS $$
DECLARE
  recovery_logs_count INT;
  explicit_preference BOOLEAN;
BEGIN
  -- Check explicit preference first
  SELECT shows_recovery_card INTO explicit_preference
  FROM profiles
  WHERE id = p_user_id;

  -- If explicitly set, use that
  IF explicit_preference IS NOT NULL THEN
    RETURN explicit_preference;
  END IF;

  -- Otherwise, auto-detect based on recent logs
  -- Count recovery logs (sleep, soreness, etc.) in last 7 days
  -- Assuming recovery data is in activities table with specific types
  SELECT COUNT(*) INTO recovery_logs_count
  FROM activities
  WHERE user_id = p_user_id
    AND activity_type IN ('sleep', 'recovery', 'rest')
    AND start_date >= NOW() - INTERVAL '7 days';

  -- Show if 3+ logs in last 7 days
  RETURN recovery_logs_count >= 3;
END;
$$;

-- ============================================================================
-- PHASE 5: Auto-Detection Triggers
-- ============================================================================

-- Trigger to auto-enable weight card
CREATE OR REPLACE FUNCTION auto_enable_weight_card()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
  weight_logs_last_14_days INT;
  current_shows_weight BOOLEAN;
BEGIN
  -- Only check if measurement is weight
  IF NEW.measurement_type = 'weight' THEN
    -- Get current preference
    SELECT shows_weight_card INTO current_shows_weight
    FROM profiles
    WHERE id = NEW.user_id;

    -- Only auto-enable if NULL (not explicitly set)
    IF current_shows_weight IS NULL THEN
      -- Count recent weight logs
      SELECT COUNT(*) INTO weight_logs_last_14_days
      FROM measurements
      WHERE user_id = NEW.user_id
        AND measurement_type = 'weight'
        AND measurement_date >= NOW() - INTERVAL '14 days';

      -- If 2+ logs, auto-enable
      IF weight_logs_last_14_days >= 2 THEN
        UPDATE profiles
        SET shows_weight_card = TRUE,
            weight_tracking_detected_at = NOW()
        WHERE id = NEW.user_id;

        -- Log the adaptation
        INSERT INTO dashboard_adaptations (
          user_id,
          adaptation_type,
          old_value,
          new_value,
          reason
        ) VALUES (
          NEW.user_id,
          'card_added',
          'NULL',
          'weight_card',
          'Auto-detected weight tracking pattern (2+ logs in 14 days)'
        );
      END IF;
    END IF;
  END IF;

  RETURN NEW;
END;
$$;

-- Apply trigger to measurements table
CREATE TRIGGER trigger_auto_enable_weight_card
AFTER INSERT ON measurements
FOR EACH ROW
EXECUTE FUNCTION auto_enable_weight_card();

-- ============================================================================
-- PHASE 6: Data Backfill for Existing Users
-- ============================================================================

-- Initialize behavior signals for all existing users
INSERT INTO user_behavior_signals (user_id)
SELECT id FROM auth.users
ON CONFLICT (user_id) DO NOTHING;

-- Set dashboard preference to 'balanced' for existing users without preference
UPDATE profiles
SET dashboard_preference = 'balanced'
WHERE dashboard_preference IS NULL;

-- Auto-detect weight tracking for existing users
UPDATE profiles p
SET shows_weight_card = TRUE,
    weight_tracking_detected_at = NOW()
WHERE shows_weight_card IS NULL
  AND (
    SELECT COUNT(*)
    FROM measurements m
    WHERE m.user_id = p.id
      AND m.measurement_type = 'weight'
      AND m.measurement_date >= NOW() - INTERVAL '14 days'
  ) >= 2;

-- ============================================================================
-- PHASE 7: Comments and Documentation
-- ============================================================================

COMMENT ON COLUMN profiles.dashboard_preference IS 'User dashboard layout: simple (minimal), balanced (default), detailed (power user)';
COMMENT ON COLUMN profiles.shows_weight_card IS 'Explicitly show/hide weight card. NULL = auto-detect based on behavior';
COMMENT ON COLUMN profiles.shows_recovery_card IS 'Explicitly show/hide recovery card. NULL = auto-detect based on behavior';
COMMENT ON COLUMN profiles.shows_workout_card IS 'Show workout section on dashboard. Default TRUE';

COMMENT ON TABLE user_behavior_signals IS 'Tracks user behavior patterns for adaptive dashboard recommendations';
COMMENT ON TABLE dashboard_adaptations IS 'Log of dashboard adaptation suggestions and user responses';

COMMENT ON FUNCTION increment_behavior_signal IS 'Safely increment a specific behavior signal for a user';
COMMENT ON FUNCTION should_show_weight_card IS 'Determine if weight card should be visible based on preference or auto-detection';
COMMENT ON FUNCTION should_show_recovery_card IS 'Determine if recovery card should be visible based on preference or auto-detection';
