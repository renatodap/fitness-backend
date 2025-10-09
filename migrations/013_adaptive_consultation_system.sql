-- =====================================================
-- ADAPTIVE CONSULTATION SYSTEM
-- Migration 013: Create tables and functions for AI-driven consultation
--
-- This migration creates:
-- 1. Consultation sessions tracking
-- 2. Conversational message storage with structured extraction
-- 3. User consultation profiles (speaking style, preferences)
-- 4. Daily recommendations system
-- 5. Helper functions for calorie/macro calculations
-- =====================================================

-- =====================================================
-- 1. CONSULTATION SESSIONS
-- =====================================================

CREATE TABLE IF NOT EXISTS public.consultation_sessions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Specialist type
    specialist_type TEXT NOT NULL CHECK (specialist_type = ANY (ARRAY[
        'unified_coach'::text,
        'nutritionist'::text,
        'trainer'::text,
        'physiotherapist'::text,
        'sports_psychologist'::text
    ])),

    -- Session status and progress
    status TEXT NOT NULL DEFAULT 'active'::text CHECK (status = ANY (ARRAY[
        'active'::text,
        'completed'::text,
        'paused'::text,
        'abandoned'::text
    ])),
    conversation_stage TEXT CHECK (conversation_stage = ANY (ARRAY[
        'introduction'::text,
        'discovery'::text,
        'health_history'::text,
        'goals'::text,
        'preferences'::text,
        'wrap_up'::text
    ])),
    progress_percentage NUMERIC DEFAULT 0 CHECK (progress_percentage >= 0 AND progress_percentage <= 100),

    -- Session metadata
    session_metadata JSONB DEFAULT '{}'::jsonb,
    total_messages INTEGER DEFAULT 0,
    total_extractions INTEGER DEFAULT 0,

    -- AI costs tracking
    total_tokens_used INTEGER DEFAULT 0,
    total_cost_usd NUMERIC DEFAULT 0,

    -- Timestamps
    started_at TIMESTAMPTZ DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    last_message_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for consultation_sessions
CREATE INDEX IF NOT EXISTS idx_consultation_sessions_user_id ON public.consultation_sessions(user_id);
CREATE INDEX IF NOT EXISTS idx_consultation_sessions_status ON public.consultation_sessions(status);
CREATE INDEX IF NOT EXISTS idx_consultation_sessions_specialist_type ON public.consultation_sessions(specialist_type);

-- RLS for consultation_sessions
ALTER TABLE public.consultation_sessions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own consultation sessions"
    ON public.consultation_sessions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create own consultation sessions"
    ON public.consultation_sessions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own consultation sessions"
    ON public.consultation_sessions FOR UPDATE
    USING (auth.uid() = user_id);

-- =====================================================
-- 2. CONSULTATION MESSAGES
-- =====================================================

CREATE TABLE IF NOT EXISTS public.consultation_messages (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES public.consultation_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Message content
    role TEXT NOT NULL CHECK (role = ANY (ARRAY['user'::text, 'assistant'::text, 'system'::text])),
    content TEXT NOT NULL,

    -- Structured data extraction
    extraction_data JSONB DEFAULT '{}'::jsonb,
    extraction_confidence NUMERIC CHECK (extraction_confidence >= 0 AND extraction_confidence <= 1),
    extraction_category TEXT CHECK (extraction_category = ANY (ARRAY[
        'health_history'::text,
        'nutrition_patterns'::text,
        'training_history'::text,
        'goals'::text,
        'preferences'::text,
        'measurements'::text,
        'lifestyle'::text,
        'psychology'::text
    ])),

    -- AI metadata
    ai_provider TEXT CHECK (ai_provider = ANY (ARRAY['groq'::text, 'openrouter'::text, 'anthropic'::text, 'openai'::text, 'deepseek'::text, 'free'::text])),
    ai_model TEXT,
    tokens_used INTEGER DEFAULT 0,
    cost_usd NUMERIC DEFAULT 0,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for consultation_messages
CREATE INDEX IF NOT EXISTS idx_consultation_messages_session_id ON public.consultation_messages(session_id);
CREATE INDEX IF NOT EXISTS idx_consultation_messages_user_id ON public.consultation_messages(user_id);
CREATE INDEX IF NOT EXISTS idx_consultation_messages_role ON public.consultation_messages(role);
CREATE INDEX IF NOT EXISTS idx_consultation_messages_created_at ON public.consultation_messages(created_at DESC);

-- RLS for consultation_messages
ALTER TABLE public.consultation_messages ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own consultation messages"
    ON public.consultation_messages FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create own consultation messages"
    ON public.consultation_messages FOR INSERT
    WITH CHECK (auth.uid() = user_id);

-- =====================================================
-- 3. CONSULTATION EXTRACTIONS (Aggregated Structured Data)
-- =====================================================

CREATE TABLE IF NOT EXISTS public.consultation_extractions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    session_id UUID NOT NULL REFERENCES public.consultation_sessions(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Extraction category and data
    extraction_category TEXT NOT NULL CHECK (extraction_category = ANY (ARRAY[
        'health_history'::text,
        'nutrition_patterns'::text,
        'training_history'::text,
        'goals'::text,
        'preferences'::text,
        'measurements'::text,
        'lifestyle'::text,
        'psychology'::text
    ])),
    extracted_data JSONB NOT NULL DEFAULT '{}'::jsonb,

    -- Source tracking
    source_message_ids UUID[] DEFAULT ARRAY[]::UUID[],
    confidence_score NUMERIC CHECK (confidence_score >= 0 AND confidence_score <= 1),

    -- Verification
    verified BOOLEAN DEFAULT false,
    verification_notes TEXT,

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for consultation_extractions
CREATE INDEX IF NOT EXISTS idx_consultation_extractions_session_id ON public.consultation_extractions(session_id);
CREATE INDEX IF NOT EXISTS idx_consultation_extractions_user_id ON public.consultation_extractions(user_id);
CREATE INDEX IF NOT EXISTS idx_consultation_extractions_category ON public.consultation_extractions(extraction_category);

-- RLS for consultation_extractions
ALTER TABLE public.consultation_extractions ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own consultation extractions"
    ON public.consultation_extractions FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create own consultation extractions"
    ON public.consultation_extractions FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own consultation extractions"
    ON public.consultation_extractions FOR UPDATE
    USING (auth.uid() = user_id);

-- =====================================================
-- 4. USER CONSULTATION PROFILES (Speaking Style & Preferences)
-- =====================================================

CREATE TABLE IF NOT EXISTS public.user_consultation_profiles (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Speaking style and communication preferences
    speaking_style TEXT DEFAULT 'casual'::text CHECK (speaking_style = ANY (ARRAY[
        'formal'::text,
        'casual'::text,
        'motivational'::text,
        'technical'::text,
        'nurturing'::text
    ])),
    communication_preferences JSONB DEFAULT '{
        "prefers_detailed_explanations": false,
        "prefers_visual_aids": true,
        "tone_preference": "encouraging",
        "language_complexity": "moderate"
    }'::jsonb,

    -- Aggregated insights from consultations
    consultation_history_summary TEXT,
    key_learnings JSONB DEFAULT '{}'::jsonb,

    -- Statistics
    total_consultations INTEGER DEFAULT 0,
    completed_consultations INTEGER DEFAULT 0,
    average_session_duration_minutes INTEGER,

    -- Timestamps
    first_consultation_at TIMESTAMPTZ,
    last_consultation_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for user_consultation_profiles
CREATE INDEX IF NOT EXISTS idx_user_consultation_profiles_speaking_style ON public.user_consultation_profiles(speaking_style);
CREATE INDEX IF NOT EXISTS idx_user_consultation_profiles_last_consultation ON public.user_consultation_profiles(last_consultation_at DESC);

-- RLS for user_consultation_profiles
ALTER TABLE public.user_consultation_profiles ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own consultation profile"
    ON public.user_consultation_profiles FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own consultation profile"
    ON public.user_consultation_profiles FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own consultation profile"
    ON public.user_consultation_profiles FOR UPDATE
    USING (auth.uid() = user_id);

-- =====================================================
-- 5. DAILY RECOMMENDATIONS
-- =====================================================

CREATE TABLE IF NOT EXISTS public.daily_recommendations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

    -- Recommendation details
    recommendation_date DATE NOT NULL,
    recommendation_time TIME,
    recommendation_type TEXT NOT NULL CHECK (recommendation_type = ANY (ARRAY[
        'meal'::text,
        'workout'::text,
        'rest'::text,
        'hydration'::text,
        'supplement'::text,
        'note'::text,
        'check_in'::text
    ])),

    -- Content (varies by type)
    content JSONB NOT NULL DEFAULT '{}'::jsonb,
    reasoning TEXT,

    -- Priority and status
    priority INTEGER DEFAULT 3 CHECK (priority >= 1 AND priority <= 5),
    status TEXT NOT NULL DEFAULT 'pending'::text CHECK (status = ANY (ARRAY[
        'pending'::text,
        'accepted'::text,
        'rejected'::text,
        'completed'::text,
        'expired'::text
    ])),

    -- Context (what data informed this recommendation)
    based_on_data JSONB DEFAULT '{}'::jsonb,
    related_log_ids UUID[] DEFAULT ARRAY[]::UUID[],

    -- User feedback
    user_feedback TEXT,
    feedback_rating INTEGER CHECK (feedback_rating >= 1 AND feedback_rating <= 5),

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    expires_at TIMESTAMPTZ,
    completed_at TIMESTAMPTZ
);

-- Indexes for daily_recommendations
CREATE INDEX IF NOT EXISTS idx_daily_recommendations_user_id ON public.daily_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_daily_recommendations_date ON public.daily_recommendations(recommendation_date DESC);
CREATE INDEX IF NOT EXISTS idx_daily_recommendations_status ON public.daily_recommendations(status);
CREATE INDEX IF NOT EXISTS idx_daily_recommendations_type ON public.daily_recommendations(recommendation_type);
CREATE INDEX IF NOT EXISTS idx_daily_recommendations_priority ON public.daily_recommendations(priority DESC);

-- RLS for daily_recommendations
ALTER TABLE public.daily_recommendations ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own daily recommendations"
    ON public.daily_recommendations FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Users can create own daily recommendations"
    ON public.daily_recommendations FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own daily recommendations"
    ON public.daily_recommendations FOR UPDATE
    USING (auth.uid() = user_id);

-- =====================================================
-- 6. EXTEND EXISTING TABLES
-- =====================================================

-- Extend profiles table for consultation data
ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS communication_preferences JSONB DEFAULT '{}'::jsonb,
ADD COLUMN IF NOT EXISTS consultation_onboarding_completed BOOLEAN DEFAULT false,
ADD COLUMN IF NOT EXISTS estimated_tdee INTEGER,
ADD COLUMN IF NOT EXISTS bmr INTEGER,
ADD COLUMN IF NOT EXISTS activity_multiplier NUMERIC DEFAULT 1.2;

-- Extend ai_generated_programs to link consultations
ALTER TABLE public.ai_generated_programs
ADD COLUMN IF NOT EXISTS consultation_session_id UUID REFERENCES public.consultation_sessions(id);

-- Extend coach_conversations to link consultations
ALTER TABLE public.coach_conversations
ADD COLUMN IF NOT EXISTS consultation_session_id UUID REFERENCES public.consultation_sessions(id);

-- =====================================================
-- 7. HELPER FUNCTIONS FOR CALORIE CALCULATIONS
-- =====================================================

-- Function to calculate BMR (Basal Metabolic Rate) using Mifflin-St Jeor equation
CREATE OR REPLACE FUNCTION public.calculate_bmr(
    weight_kg NUMERIC,
    height_cm NUMERIC,
    age INTEGER,
    biological_sex TEXT
)
RETURNS INTEGER
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    bmr_value NUMERIC;
BEGIN
    IF biological_sex = 'male' THEN
        -- Men: (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5
        bmr_value := (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5;
    ELSIF biological_sex = 'female' THEN
        -- Women: (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161
        bmr_value := (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161;
    ELSE
        -- Default to male formula if not specified
        bmr_value := (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5;
    END IF;

    RETURN ROUND(bmr_value)::INTEGER;
END;
$$;

-- Function to calculate TDEE (Total Daily Energy Expenditure)
CREATE OR REPLACE FUNCTION public.calculate_tdee(
    bmr_value INTEGER,
    activity_level TEXT,
    training_frequency INTEGER DEFAULT 3
)
RETURNS INTEGER
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    activity_multiplier NUMERIC;
    tdee_value NUMERIC;
BEGIN
    -- Determine activity multiplier based on activity level and training frequency
    CASE activity_level
        WHEN 'sedentary' THEN
            activity_multiplier := 1.2;
        WHEN 'lightly_active' THEN
            activity_multiplier := 1.375;
        WHEN 'moderately_active' THEN
            activity_multiplier := 1.55;
        WHEN 'very_active' THEN
            activity_multiplier := 1.725;
        WHEN 'extremely_active' THEN
            activity_multiplier := 1.9;
        ELSE
            -- Default based on training frequency
            IF training_frequency >= 6 THEN
                activity_multiplier := 1.725; -- Very active
            ELSIF training_frequency >= 4 THEN
                activity_multiplier := 1.55; -- Moderately active
            ELSIF training_frequency >= 2 THEN
                activity_multiplier := 1.375; -- Lightly active
            ELSE
                activity_multiplier := 1.2; -- Sedentary
            END IF;
    END CASE;

    tdee_value := bmr_value * activity_multiplier;

    RETURN ROUND(tdee_value)::INTEGER;
END;
$$;

-- Function to calculate macros based on goal
CREATE OR REPLACE FUNCTION public.calculate_macros(
    tdee INTEGER,
    goal_type TEXT,
    body_weight_kg NUMERIC
)
RETURNS JSONB
LANGUAGE plpgsql
IMMUTABLE
AS $$
DECLARE
    daily_calories INTEGER;
    protein_g INTEGER;
    fat_g INTEGER;
    carbs_g INTEGER;
    protein_calories INTEGER;
    fat_calories INTEGER;
    remaining_calories INTEGER;
BEGIN
    -- Adjust calories based on goal
    CASE goal_type
        WHEN 'cut', 'lose_fat', 'fat_loss' THEN
            daily_calories := ROUND(tdee * 0.8)::INTEGER; -- 20% deficit
            protein_g := ROUND(body_weight_kg * 2.2)::INTEGER; -- High protein for muscle preservation
        WHEN 'bulk', 'build_muscle', 'muscle_gain' THEN
            daily_calories := ROUND(tdee * 1.1)::INTEGER; -- 10% surplus
            protein_g := ROUND(body_weight_kg * 2.0)::INTEGER; -- High protein for muscle building
        WHEN 'maintain', 'maintenance', 'recomp' THEN
            daily_calories := tdee;
            protein_g := ROUND(body_weight_kg * 1.8)::INTEGER; -- Moderate-high protein
        ELSE
            daily_calories := tdee;
            protein_g := ROUND(body_weight_kg * 1.6)::INTEGER; -- General fitness
    END CASE;

    -- Calculate fat (25-30% of calories)
    fat_g := ROUND((daily_calories * 0.28) / 9)::INTEGER; -- 9 cal/g fat

    -- Calculate carbs from remaining calories
    protein_calories := protein_g * 4; -- 4 cal/g protein
    fat_calories := fat_g * 9; -- 9 cal/g fat
    remaining_calories := daily_calories - protein_calories - fat_calories;
    carbs_g := ROUND(remaining_calories / 4)::INTEGER; -- 4 cal/g carbs

    -- Ensure non-negative values
    carbs_g := GREATEST(carbs_g, 0);

    RETURN jsonb_build_object(
        'daily_calories', daily_calories,
        'daily_protein_g', protein_g,
        'daily_carbs_g', carbs_g,
        'daily_fat_g', fat_g,
        'protein_percentage', ROUND((protein_calories::NUMERIC / daily_calories) * 100),
        'carbs_percentage', ROUND(((carbs_g * 4)::NUMERIC / daily_calories) * 100),
        'fat_percentage', ROUND(((fat_g * 9)::NUMERIC / daily_calories) * 100)
    );
END;
$$;

-- =====================================================
-- 8. TRIGGER FUNCTIONS
-- =====================================================

-- Update consultation_sessions.total_messages when message added
CREATE OR REPLACE FUNCTION public.update_consultation_message_count()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    UPDATE public.consultation_sessions
    SET
        total_messages = total_messages + 1,
        total_tokens_used = total_tokens_used + COALESCE(NEW.tokens_used, 0),
        total_cost_usd = total_cost_usd + COALESCE(NEW.cost_usd, 0),
        last_message_at = NEW.created_at,
        updated_at = NOW()
    WHERE id = NEW.session_id;

    RETURN NEW;
END;
$$;

CREATE TRIGGER trigger_update_consultation_message_count
    AFTER INSERT ON public.consultation_messages
    FOR EACH ROW
    EXECUTE FUNCTION public.update_consultation_message_count();

-- Update updated_at timestamp
CREATE OR REPLACE FUNCTION public.update_updated_at_column()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$;

CREATE TRIGGER update_consultation_sessions_updated_at
    BEFORE UPDATE ON public.consultation_sessions
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_consultation_extractions_updated_at
    BEFORE UPDATE ON public.consultation_extractions
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

CREATE TRIGGER update_user_consultation_profiles_updated_at
    BEFORE UPDATE ON public.user_consultation_profiles
    FOR EACH ROW
    EXECUTE FUNCTION public.update_updated_at_column();

-- =====================================================
-- 9. INDEXES FOR PERFORMANCE
-- =====================================================

-- GIN indexes for JSONB columns (for fast JSON queries)
CREATE INDEX IF NOT EXISTS idx_consultation_messages_extraction_data
    ON public.consultation_messages USING GIN (extraction_data);

CREATE INDEX IF NOT EXISTS idx_consultation_extractions_extracted_data
    ON public.consultation_extractions USING GIN (extracted_data);

CREATE INDEX IF NOT EXISTS idx_daily_recommendations_content
    ON public.daily_recommendations USING GIN (content);

CREATE INDEX IF NOT EXISTS idx_user_consultation_profiles_communication
    ON public.user_consultation_profiles USING GIN (communication_preferences);

-- =====================================================
-- 10. COMMENTS FOR DOCUMENTATION
-- =====================================================

COMMENT ON TABLE public.consultation_sessions IS 'Tracks AI-driven consultation sessions with different specialists';
COMMENT ON TABLE public.consultation_messages IS 'Stores conversation messages with structured data extraction';
COMMENT ON TABLE public.consultation_extractions IS 'Aggregated structured data extracted from consultations';
COMMENT ON TABLE public.user_consultation_profiles IS 'User communication style and preferences learned from consultations';
COMMENT ON TABLE public.daily_recommendations IS 'AI-generated daily meal/workout recommendations';

COMMENT ON FUNCTION public.calculate_bmr IS 'Calculate Basal Metabolic Rate using Mifflin-St Jeor equation';
COMMENT ON FUNCTION public.calculate_tdee IS 'Calculate Total Daily Energy Expenditure based on BMR and activity';
COMMENT ON FUNCTION public.calculate_macros IS 'Calculate daily macronutrient targets based on TDEE and goal';

-- =====================================================
-- END OF MIGRATION
-- =====================================================
