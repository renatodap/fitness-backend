-- Migration 014: Add User Events & Calendar System
-- Created: 2025-10-09
-- Purpose: Enable users to add events (races, competitions, shows) and generate event-specific programs

-- =====================================================
-- USER EVENTS TABLE
-- =====================================================

CREATE TABLE IF NOT EXISTS public.user_events (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Event Details
  event_name TEXT NOT NULL,
  event_type TEXT NOT NULL CHECK (event_type IN (
    'marathon', 'half_marathon', '10k', '5k',
    'triathlon', 'cycling_race', 'swimming_meet',
    'powerlifting_meet', 'weightlifting_meet', 'strongman',
    'bodybuilding_show', 'physique_competition',
    'crossfit_competition', 'obstacle_race',
    'team_sport_game', 'tennis_match', 'golf_tournament',
    'hiking_trip', 'skiing_trip', 'climbing_expedition',
    'fitness_test', 'photo_shoot', 'wedding', 'vacation',
    'other'
  )),
  event_subtype TEXT, -- e.g., "Boston Marathon", "Olympic Distance Triathlon"

  -- Date & Location
  event_date DATE NOT NULL,
  event_end_date DATE, -- For multi-day events
  registration_deadline DATE,
  location TEXT,
  city TEXT,
  state TEXT,
  country TEXT,
  timezone TEXT DEFAULT 'UTC',

  -- Goals & Performance
  goal_performance TEXT, -- "Sub 3:30 marathon", "300kg total", "Top 10 finish"
  target_time TEXT, -- "3:29:00" for timed events
  target_weight_class TEXT, -- "83kg" for weightlifting
  target_distance_km NUMERIC, -- 42.195 for marathon

  -- Priority & Status
  priority INTEGER DEFAULT 3 CHECK (priority >= 1 AND priority <= 5), -- 1=highest, 5=lowest
  status TEXT DEFAULT 'upcoming' CHECK (status IN (
    'upcoming', 'registered', 'training', 'tapering', 'completed', 'cancelled'
  )),
  is_primary_goal BOOLEAN DEFAULT false, -- Only one primary goal at a time

  -- Training Period
  training_start_date DATE, -- When to begin specific training
  taper_start_date DATE, -- When to begin taper (auto-calculated or manual)
  peak_week_date DATE, -- When to peak (usually 7-14 days before event)

  -- External Links
  registration_url TEXT,
  event_website TEXT,
  event_logo_url TEXT,

  -- Metadata
  notes TEXT,
  private_notes TEXT,
  tags TEXT[] DEFAULT ARRAY[]::TEXT[],

  -- AI Program Integration
  linked_program_id UUID REFERENCES public.ai_generated_programs(id),
  program_periodization JSONB DEFAULT '{}', -- AI-generated periodization plan

  -- Reminders & Notifications
  reminder_settings JSONB DEFAULT '{
    "one_month_before": true,
    "two_weeks_before": true,
    "one_week_before": true,
    "three_days_before": true,
    "one_day_before": true
  }'::jsonb,

  -- Tracking
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),
  completed_at TIMESTAMPTZ,
  result_notes TEXT, -- Post-event: "Finished 23rd overall, 3:45:32"
  result_data JSONB -- Detailed results
);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX idx_user_events_user_id ON user_events(user_id);
CREATE INDEX idx_user_events_event_date ON user_events(event_date);
CREATE INDEX idx_user_events_status ON user_events(user_id, status);
CREATE INDEX idx_user_events_primary ON user_events(user_id, is_primary_goal) WHERE is_primary_goal = true;
CREATE INDEX idx_user_events_upcoming ON user_events(user_id, event_date) WHERE status IN ('upcoming', 'registered', 'training', 'tapering');

-- =====================================================
-- RLS POLICIES
-- =====================================================

ALTER TABLE user_events ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own events"
  ON user_events FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own events"
  ON user_events FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own events"
  ON user_events FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete own events"
  ON user_events FOR DELETE
  USING (auth.uid() = user_id);

-- =====================================================
-- TRIGGERS
-- =====================================================

-- Trigger for updated_at
CREATE TRIGGER update_user_events_updated_at
  BEFORE UPDATE ON user_events
  FOR EACH ROW
  EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- FUNCTIONS
-- =====================================================

-- Function to auto-calculate taper/peak dates based on event type
CREATE OR REPLACE FUNCTION calculate_event_training_dates()
RETURNS TRIGGER AS $$
BEGIN
  -- Auto-calculate taper start (typically 2 weeks before for endurance, 1 week for strength)
  IF NEW.taper_start_date IS NULL THEN
    IF NEW.event_type IN ('marathon', 'half_marathon', 'triathlon') THEN
      NEW.taper_start_date := NEW.event_date - INTERVAL '14 days';
    ELSIF NEW.event_type IN ('powerlifting_meet', 'weightlifting_meet', 'bodybuilding_show') THEN
      NEW.taper_start_date := NEW.event_date - INTERVAL '7 days';
    ELSE
      NEW.taper_start_date := NEW.event_date - INTERVAL '10 days';
    END IF;
  END IF;

  -- Auto-calculate peak week (1 week before event)
  IF NEW.peak_week_date IS NULL THEN
    NEW.peak_week_date := NEW.event_date - INTERVAL '7 days';
  END IF;

  -- Auto-calculate training start if not provided
  IF NEW.training_start_date IS NULL THEN
    IF NEW.event_type IN ('marathon', 'half_marathon') THEN
      NEW.training_start_date := NEW.event_date - INTERVAL '16 weeks';
    ELSIF NEW.event_type IN ('triathlon') THEN
      NEW.training_start_date := NEW.event_date - INTERVAL '20 weeks';
    ELSIF NEW.event_type IN ('powerlifting_meet', 'weightlifting_meet') THEN
      NEW.training_start_date := NEW.event_date - INTERVAL '12 weeks';
    ELSIF NEW.event_type IN ('bodybuilding_show', 'physique_competition') THEN
      NEW.training_start_date := NEW.event_date - INTERVAL '16 weeks';
    ELSE
      NEW.training_start_date := NEW.event_date - INTERVAL '12 weeks';
    END IF;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER set_event_training_dates
  BEFORE INSERT OR UPDATE ON user_events
  FOR EACH ROW
  EXECUTE FUNCTION calculate_event_training_dates();

-- Function to ensure only one primary event
CREATE OR REPLACE FUNCTION ensure_single_primary_event()
RETURNS TRIGGER AS $$
BEGIN
  -- If setting this event as primary, unset all others
  IF NEW.is_primary_goal = true THEN
    UPDATE user_events
    SET is_primary_goal = false
    WHERE user_id = NEW.user_id
      AND id != NEW.id
      AND is_primary_goal = true;
  END IF;

  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER ensure_single_primary_event_trigger
  BEFORE INSERT OR UPDATE ON user_events
  FOR EACH ROW
  EXECUTE FUNCTION ensure_single_primary_event();

-- =====================================================
-- HELPER VIEWS
-- =====================================================

-- View for upcoming events with countdown
CREATE OR REPLACE VIEW user_events_with_countdown AS
SELECT
  e.*,
  (e.event_date - CURRENT_DATE) AS days_until_event,
  CASE
    WHEN e.event_date < CURRENT_DATE THEN 'past'
    WHEN CURRENT_DATE >= e.taper_start_date THEN 'taper'
    WHEN CURRENT_DATE >= e.peak_week_date THEN 'peak'
    WHEN CURRENT_DATE >= e.training_start_date THEN 'build'
    ELSE 'pre_training'
  END AS current_training_phase
FROM user_events e
WHERE e.status IN ('upcoming', 'registered', 'training', 'tapering');

-- =====================================================
-- COMMENTS
-- =====================================================

COMMENT ON TABLE user_events IS 'User events (races, competitions, shows) with AI program integration for event-specific periodization';
COMMENT ON COLUMN user_events.event_type IS 'Type of event (marathon, powerlifting_meet, bodybuilding_show, etc.)';
COMMENT ON COLUMN user_events.is_primary_goal IS 'Only one event can be primary at a time - drives main program periodization';
COMMENT ON COLUMN user_events.linked_program_id IS 'AI program generated specifically for this event';
COMMENT ON COLUMN user_events.program_periodization IS 'AI-generated periodization plan (phases, volume progression, taper protocol)';
COMMENT ON FUNCTION calculate_event_training_dates() IS 'Auto-calculates training_start_date, taper_start_date, and peak_week_date based on event type';
COMMENT ON VIEW user_events_with_countdown IS 'Events with calculated countdown and current training phase';

-- =====================================================
-- DOWN MIGRATION (for rollback)
-- =====================================================

/*
-- To rollback this migration:

DROP VIEW IF EXISTS user_events_with_countdown;
DROP TRIGGER IF EXISTS ensure_single_primary_event_trigger ON user_events;
DROP TRIGGER IF EXISTS set_event_training_dates ON user_events;
DROP TRIGGER IF EXISTS update_user_events_updated_at ON user_events;
DROP FUNCTION IF EXISTS ensure_single_primary_event();
DROP FUNCTION IF EXISTS calculate_event_training_dates();
DROP TABLE IF EXISTS user_events CASCADE;
*/
