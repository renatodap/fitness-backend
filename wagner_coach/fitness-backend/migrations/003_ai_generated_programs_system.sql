-- Migration: AI Generated Programs System
-- Description: Comprehensive system for AI-generated personalized programs with meals and workouts

-- ============================================================================
-- PART 1: AI GENERATED PROGRAMS
-- ============================================================================

-- Main AI-generated programs table
CREATE TABLE IF NOT EXISTS ai_generated_programs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    goals TEXT[], -- User goals this program addresses
    duration_weeks INTEGER NOT NULL DEFAULT 12, -- 3 months = 12 weeks
    total_days INTEGER NOT NULL DEFAULT 84, -- 12 weeks * 7 days
    start_date DATE,
    end_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    status TEXT DEFAULT 'active' CHECK (status IN ('active', 'completed', 'paused', 'abandoned')),

    -- AI Generation Context
    generation_prompt TEXT, -- Full prompt sent to AI
    generation_context JSONB DEFAULT '{}', -- User data used (profile, goals, preferences)
    questions_answers JSONB DEFAULT '[]', -- Questions asked and user answers
    ai_model TEXT DEFAULT 'gpt-4o', -- Model used for generation

    -- Program Metadata
    difficulty_level TEXT CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
    primary_focus TEXT[], -- e.g., ['strength', 'endurance', 'weight_loss']
    equipment_needed TEXT[],
    dietary_approach TEXT, -- e.g., 'balanced', 'high_protein', 'keto', 'vegan'

    -- Progress Tracking
    current_day INTEGER DEFAULT 1,
    days_completed INTEGER DEFAULT 0,
    meals_completed INTEGER DEFAULT 0,
    workouts_completed INTEGER DEFAULT 0,
    adherence_percentage NUMERIC DEFAULT 100 CHECK (adherence_percentage >= 0 AND adherence_percentage <= 100),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,

    CONSTRAINT ai_generated_programs_valid_dates CHECK (end_date IS NULL OR end_date >= start_date)
);

-- Indexes for ai_generated_programs
CREATE INDEX IF NOT EXISTS idx_ai_programs_user_active ON ai_generated_programs(user_id, is_active) WHERE is_active = TRUE;
CREATE INDEX IF NOT EXISTS idx_ai_programs_status ON ai_generated_programs(user_id, status);
CREATE INDEX IF NOT EXISTS idx_ai_programs_dates ON ai_generated_programs(start_date, end_date);

-- ============================================================================
-- PART 2: PROGRAM DAILY SCHEDULE
-- ============================================================================

-- Daily schedule within AI program
CREATE TABLE IF NOT EXISTS ai_program_days (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_id UUID NOT NULL REFERENCES ai_generated_programs(id) ON DELETE CASCADE,
    day_number INTEGER NOT NULL CHECK (day_number >= 1 AND day_number <= 365), -- Support up to 1 year
    day_date DATE, -- Actual calendar date (computed from start_date + day_number)
    day_of_week TEXT CHECK (day_of_week IN ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')),

    -- Day Overview
    day_name TEXT, -- e.g., "Upper Body + Cardio", "Rest & Recovery"
    day_focus TEXT, -- e.g., "Strength", "Endurance", "Active Recovery"
    day_notes TEXT, -- Special instructions for this day

    -- Completion Tracking
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMPTZ,
    completion_notes TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT ai_program_days_unique UNIQUE (program_id, day_number)
);

-- Indexes for ai_program_days
CREATE INDEX IF NOT EXISTS idx_ai_program_days_program ON ai_program_days(program_id, day_number);
CREATE INDEX IF NOT EXISTS idx_ai_program_days_date ON ai_program_days(program_id, day_date);
CREATE INDEX IF NOT EXISTS idx_ai_program_days_completed ON ai_program_days(program_id, is_completed);

-- ============================================================================
-- PART 3: PROGRAM MEALS
-- ============================================================================

-- Meals scheduled in the program
CREATE TABLE IF NOT EXISTS ai_program_meals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_day_id UUID NOT NULL REFERENCES ai_program_days(id) ON DELETE CASCADE,
    program_id UUID NOT NULL REFERENCES ai_generated_programs(id) ON DELETE CASCADE,

    -- Meal Identification
    meal_type TEXT NOT NULL CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack', 'pre_workout', 'post_workout')),
    meal_time TIME, -- Suggested time to eat
    meal_order INTEGER DEFAULT 0, -- Order within the day

    -- Meal Details
    name TEXT NOT NULL, -- e.g., "High Protein Breakfast Bowl"
    description TEXT,
    recipe_instructions TEXT,
    preparation_time_minutes INTEGER,

    -- Foods/Ingredients
    foods JSONB DEFAULT '[]', -- Array of {food_id, food_name, quantity, unit, calories, protein, carbs, fat}

    -- Nutrition Totals
    total_calories NUMERIC,
    total_protein_g NUMERIC,
    total_carbs_g NUMERIC,
    total_fat_g NUMERIC,
    total_fiber_g NUMERIC,

    -- Additional Info
    meal_tags TEXT[], -- e.g., ['quick', 'meal_prep', 'vegetarian']
    alternatives JSONB DEFAULT '[]', -- Alternative meals if user doesn't like this one
    notes TEXT,

    -- Completion Tracking
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMPTZ,
    actual_foods_eaten JSONB, -- What user actually ate vs planned

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for ai_program_meals
CREATE INDEX IF NOT EXISTS idx_ai_program_meals_day ON ai_program_meals(program_day_id);
CREATE INDEX IF NOT EXISTS idx_ai_program_meals_program ON ai_program_meals(program_id);
CREATE INDEX IF NOT EXISTS idx_ai_program_meals_type ON ai_program_meals(program_id, meal_type);
CREATE INDEX IF NOT EXISTS idx_ai_program_meals_completed ON ai_program_meals(program_id, is_completed);

-- ============================================================================
-- PART 4: PROGRAM WORKOUTS
-- ============================================================================

-- Workouts scheduled in the program
CREATE TABLE IF NOT EXISTS ai_program_workouts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    program_day_id UUID NOT NULL REFERENCES ai_program_days(id) ON DELETE CASCADE,
    program_id UUID NOT NULL REFERENCES ai_generated_programs(id) ON DELETE CASCADE,

    -- Workout Identification
    workout_type TEXT NOT NULL CHECK (workout_type IN ('strength', 'cardio', 'sports', 'flexibility', 'mobility', 'rest', 'active_recovery')),
    workout_subtype TEXT, -- 'running', 'cycling', 'swimming', 'lifting', 'track', 'hiit', 'yoga', etc.
    workout_order INTEGER DEFAULT 0, -- Order within the day (can have multiple workouts per day)

    -- Workout Details
    name TEXT NOT NULL, -- e.g., "Upper Body Strength - Push Focus"
    description TEXT,
    duration_minutes INTEGER,

    -- For Strength Training
    exercises JSONB DEFAULT '[]', -- Array of {exercise_id, name, sets, reps, weight, rest_seconds, notes}

    -- For Cardio/Sports
    workout_details JSONB DEFAULT '{}', -- {distance, distance_unit, pace, intervals, heart_rate_zones, etc}

    -- Workout Characteristics
    intensity TEXT CHECK (intensity IN ('low', 'moderate', 'high', 'max')),
    target_rpe INTEGER CHECK (target_rpe >= 1 AND target_rpe <= 10), -- Rate of Perceived Exertion
    estimated_calories_burned INTEGER,

    -- Equipment & Location
    equipment_needed TEXT[],
    location TEXT, -- 'gym', 'home', 'outdoor', 'track', etc.

    -- Instructions
    warmup_notes TEXT,
    cooldown_notes TEXT,
    technique_cues TEXT[],
    notes TEXT,

    -- Alternatives
    alternatives JSONB DEFAULT '[]', -- Alternative workouts if user can't do this one

    -- Completion Tracking
    is_completed BOOLEAN DEFAULT FALSE,
    completed_at TIMESTAMPTZ,
    actual_duration_minutes INTEGER,
    actual_rpe INTEGER,
    actual_exercises JSONB, -- What user actually did vs planned
    completion_notes TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for ai_program_workouts
CREATE INDEX IF NOT EXISTS idx_ai_program_workouts_day ON ai_program_workouts(program_day_id);
CREATE INDEX IF NOT EXISTS idx_ai_program_workouts_program ON ai_program_workouts(program_id);
CREATE INDEX IF NOT EXISTS idx_ai_program_workouts_type ON ai_program_workouts(program_id, workout_type);
CREATE INDEX IF NOT EXISTS idx_ai_program_workouts_completed ON ai_program_workouts(program_id, is_completed);

-- ============================================================================
-- PART 5: USER ACTIVE PROGRAM TRACKING
-- ============================================================================

-- Track which program user is currently following
CREATE TABLE IF NOT EXISTS user_active_programs (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    program_id UUID NOT NULL REFERENCES ai_generated_programs(id) ON DELETE CASCADE,

    -- Progress
    started_at TIMESTAMPTZ DEFAULT NOW(),
    current_day INTEGER DEFAULT 1,
    last_activity_date DATE,

    -- Settings
    auto_advance_days BOOLEAN DEFAULT TRUE, -- Automatically move to next day
    notification_preferences JSONB DEFAULT '{}',

    updated_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT user_active_programs_unique UNIQUE (user_id)
);

-- Index for user_active_programs
CREATE INDEX IF NOT EXISTS idx_user_active_programs_program ON user_active_programs(program_id);

-- ============================================================================
-- PART 6: PROGRAM GENERATION SESSIONS
-- ============================================================================

-- Track program generation attempts and questions
CREATE TABLE IF NOT EXISTS program_generation_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Session State
    status TEXT DEFAULT 'in_progress' CHECK (status IN ('in_progress', 'completed', 'abandoned')),
    current_step INTEGER DEFAULT 1,
    total_steps INTEGER DEFAULT 3, -- Number of questions to ask

    -- Generation Data
    user_profile_snapshot JSONB, -- Snapshot of user's profile at generation time
    questions JSONB DEFAULT '[]', -- Questions asked by AI
    answers JSONB DEFAULT '[]', -- User's answers

    -- Result
    generated_program_id UUID REFERENCES ai_generated_programs(id),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ
);

-- Index for program_generation_sessions
CREATE INDEX IF NOT EXISTS idx_program_generation_sessions_user ON program_generation_sessions(user_id, status);

-- ============================================================================
-- PART 7: ROW LEVEL SECURITY
-- ============================================================================

-- Enable RLS on all new tables
ALTER TABLE ai_generated_programs ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_program_days ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_program_meals ENABLE ROW LEVEL SECURITY;
ALTER TABLE ai_program_workouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_active_programs ENABLE ROW LEVEL SECURITY;
ALTER TABLE program_generation_sessions ENABLE ROW LEVEL SECURITY;

-- Policies for ai_generated_programs
CREATE POLICY "Users can view their own programs"
    ON ai_generated_programs FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own programs"
    ON ai_generated_programs FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own programs"
    ON ai_generated_programs FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own programs"
    ON ai_generated_programs FOR DELETE
    USING (auth.uid() = user_id);

-- Policies for ai_program_days
CREATE POLICY "Users can view their program days"
    ON ai_program_days FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM ai_generated_programs
        WHERE ai_generated_programs.id = ai_program_days.program_id
        AND ai_generated_programs.user_id = auth.uid()
    ));

CREATE POLICY "Users can update their program days"
    ON ai_program_days FOR UPDATE
    USING (EXISTS (
        SELECT 1 FROM ai_generated_programs
        WHERE ai_generated_programs.id = ai_program_days.program_id
        AND ai_generated_programs.user_id = auth.uid()
    ));

-- Policies for ai_program_meals
CREATE POLICY "Users can view their program meals"
    ON ai_program_meals FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM ai_generated_programs
        WHERE ai_generated_programs.id = ai_program_meals.program_id
        AND ai_generated_programs.user_id = auth.uid()
    ));

CREATE POLICY "Users can update their program meals"
    ON ai_program_meals FOR UPDATE
    USING (EXISTS (
        SELECT 1 FROM ai_generated_programs
        WHERE ai_generated_programs.id = ai_program_meals.program_id
        AND ai_generated_programs.user_id = auth.uid()
    ));

-- Policies for ai_program_workouts
CREATE POLICY "Users can view their program workouts"
    ON ai_program_workouts FOR SELECT
    USING (EXISTS (
        SELECT 1 FROM ai_generated_programs
        WHERE ai_generated_programs.id = ai_program_workouts.program_id
        AND ai_generated_programs.user_id = auth.uid()
    ));

CREATE POLICY "Users can update their program workouts"
    ON ai_program_workouts FOR UPDATE
    USING (EXISTS (
        SELECT 1 FROM ai_generated_programs
        WHERE ai_generated_programs.id = ai_program_workouts.program_id
        AND ai_generated_programs.user_id = auth.uid()
    ));

-- Policies for user_active_programs
CREATE POLICY "Users can view their active program"
    ON user_active_programs FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update their active program"
    ON user_active_programs FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their active program"
    ON user_active_programs FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- Policies for program_generation_sessions
CREATE POLICY "Users can view their generation sessions"
    ON program_generation_sessions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can update their generation sessions"
    ON program_generation_sessions FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their generation sessions"
    ON program_generation_sessions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- ============================================================================
-- PART 8: HELPER FUNCTIONS
-- ============================================================================

-- Function to get user's current program with today's schedule
CREATE OR REPLACE FUNCTION get_user_current_program_day(p_user_id UUID)
RETURNS TABLE (
    program_id UUID,
    program_name TEXT,
    day_id UUID,
    day_number INTEGER,
    day_date DATE,
    day_name TEXT,
    meals JSONB,
    workouts JSONB
) LANGUAGE plpgsql AS $$
BEGIN
    RETURN QUERY
    SELECT
        p.id AS program_id,
        p.name AS program_name,
        d.id AS day_id,
        d.day_number,
        d.day_date,
        d.day_name,
        COALESCE(
            json_agg(DISTINCT jsonb_build_object(
                'id', m.id,
                'type', m.meal_type,
                'name', m.name,
                'time', m.meal_time,
                'calories', m.total_calories,
                'is_completed', m.is_completed
            )) FILTER (WHERE m.id IS NOT NULL),
            '[]'::json
        )::jsonb AS meals,
        COALESCE(
            json_agg(DISTINCT jsonb_build_object(
                'id', w.id,
                'type', w.workout_type,
                'name', w.name,
                'duration', w.duration_minutes,
                'is_completed', w.is_completed
            )) FILTER (WHERE w.id IS NOT NULL),
            '[]'::json
        )::jsonb AS workouts
    FROM user_active_programs uap
    JOIN ai_generated_programs p ON p.id = uap.program_id
    JOIN ai_program_days d ON d.program_id = p.id AND d.day_number = uap.current_day
    LEFT JOIN ai_program_meals m ON m.program_day_id = d.id
    LEFT JOIN ai_program_workouts w ON w.program_day_id = d.id
    WHERE uap.user_id = p_user_id
    GROUP BY p.id, p.name, d.id, d.day_number, d.day_date, d.day_name;
END;
$$;

-- Function to advance user to next program day
CREATE OR REPLACE FUNCTION advance_program_day(p_user_id UUID)
RETURNS BOOLEAN LANGUAGE plpgsql AS $$
DECLARE
    v_current_day INTEGER;
    v_total_days INTEGER;
BEGIN
    SELECT uap.current_day, p.total_days
    INTO v_current_day, v_total_days
    FROM user_active_programs uap
    JOIN ai_generated_programs p ON p.id = uap.program_id
    WHERE uap.user_id = p_user_id;

    IF v_current_day < v_total_days THEN
        UPDATE user_active_programs
        SET current_day = current_day + 1,
            last_activity_date = CURRENT_DATE,
            updated_at = NOW()
        WHERE user_id = p_user_id;

        RETURN TRUE;
    END IF;

    RETURN FALSE;
END;
$$;

-- ============================================================================
-- PART 9: TRIGGERS
-- ============================================================================

-- Trigger to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS update_ai_programs_updated_at ON ai_generated_programs;
CREATE TRIGGER update_ai_programs_updated_at
    BEFORE UPDATE ON ai_generated_programs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_user_active_programs_updated_at ON user_active_programs;
CREATE TRIGGER update_user_active_programs_updated_at
    BEFORE UPDATE ON user_active_programs
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

DROP TRIGGER IF EXISTS update_program_generation_sessions_updated_at ON program_generation_sessions;
CREATE TRIGGER update_program_generation_sessions_updated_at
    BEFORE UPDATE ON program_generation_sessions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

DO $$
BEGIN
    RAISE NOTICE 'AI Generated Programs System migration completed successfully';
    RAISE NOTICE 'Created tables: ai_generated_programs, ai_program_days, ai_program_meals, ai_program_workouts';
    RAISE NOTICE 'Created tracking tables: user_active_programs, program_generation_sessions';
    RAISE NOTICE 'Added RLS policies for all tables';
    RAISE NOTICE 'Created helper functions: get_user_current_program_day(), advance_program_day()';
END $$;
