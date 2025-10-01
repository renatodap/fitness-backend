-- Phase 1: Database Restructuring + RAG Foundation
-- Migration: 001_phase1_database_rag_foundation.sql
-- Description: Sets up pgvector, embeddings table, and new schema for plans vs actuals

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================================
-- EMBEDDINGS & RAG INFRASTRUCTURE
-- ============================================================================

-- Embeddings table for RAG system
CREATE TABLE IF NOT EXISTS embeddings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    content TEXT NOT NULL,
    embedding vector(1536), -- OpenAI text-embedding-3-small dimension
    metadata JSONB DEFAULT '{}',
    source_type TEXT NOT NULL, -- 'workout', 'meal', 'activity', 'goal', 'profile', 'coach_message'
    source_id UUID, -- Reference to the source record
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for embeddings
CREATE INDEX IF NOT EXISTS idx_embeddings_user_id ON embeddings(user_id);
CREATE INDEX IF NOT EXISTS idx_embeddings_source_type ON embeddings(source_type);
CREATE INDEX IF NOT EXISTS idx_embeddings_created_at ON embeddings(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_embeddings_vector ON embeddings USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Function to search similar embeddings using cosine similarity
CREATE OR REPLACE FUNCTION match_embeddings(
    query_embedding vector(1536),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 10,
    filter_user_id UUID DEFAULT NULL,
    filter_source_types TEXT[] DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    user_id UUID,
    content TEXT,
    metadata JSONB,
    source_type TEXT,
    source_id UUID,
    similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
    RETURN QUERY
    SELECT
        e.id,
        e.user_id,
        e.content,
        e.metadata,
        e.source_type,
        e.source_id,
        1 - (e.embedding <=> query_embedding) AS similarity
    FROM embeddings e
    WHERE
        (filter_user_id IS NULL OR e.user_id = filter_user_id)
        AND (filter_source_types IS NULL OR e.source_type = ANY(filter_source_types))
        AND (1 - (e.embedding <=> query_embedding)) >= match_threshold
    ORDER BY e.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;

-- ============================================================================
-- COACH PERSONAS & CONVERSATIONS
-- ============================================================================

-- Coach personas (Trainer and Nutritionist)
CREATE TABLE IF NOT EXISTS coach_personas (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL, -- 'trainer' or 'nutritionist'
    display_name TEXT NOT NULL,
    system_prompt TEXT NOT NULL,
    specialty TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(name)
);

-- Insert default coach personas
INSERT INTO coach_personas (name, display_name, system_prompt, specialty) VALUES
(
    'trainer',
    'Coach Alex - Your Personal Trainer',
    'You are Coach Alex, an experienced personal trainer specializing in strength training, progressive overload, and volume management. You have access to all of the user''s workout history, activities, and progress. You provide specific, actionable workout recommendations based on their goals, current fitness level, and past performance. You track their progressive overload and ensure proper recovery. You are encouraging but realistic, and you always prioritize proper form and injury prevention.',
    'Strength Training, Progressive Overload, Volume Management, Exercise Programming'
),
(
    'nutritionist',
    'Coach Maria - Your Nutritionist',
    'You are Coach Maria, a certified nutritionist specializing in sustainable eating habits and macro-based nutrition. You have access to all of the user''s meal logs, nutrition history, and dietary preferences. You provide specific, actionable meal recommendations and plans based on their goals, current intake patterns, and lifestyle. You focus on helping users build healthy relationships with food while achieving their body composition goals. You are empathetic, practical, and always consider the user''s real-world constraints.',
    'Nutrition Planning, Macro Tracking, Meal Timing, Sustainable Diet Habits'
);

-- Coach conversations
CREATE TABLE IF NOT EXISTS coach_conversations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    coach_persona_id UUID NOT NULL REFERENCES coach_personas(id),
    messages JSONB DEFAULT '[]', -- Array of {role, content, timestamp}
    last_message_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_coach_conversations_user_id ON coach_conversations(user_id);
CREATE INDEX IF NOT EXISTS idx_coach_conversations_persona ON coach_conversations(coach_persona_id);
CREATE INDEX IF NOT EXISTS idx_coach_conversations_last_message ON coach_conversations(last_message_at DESC);

-- Coach recommendations (weekly adaptive recommendations)
CREATE TABLE IF NOT EXISTS coach_recommendations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    coach_persona_id UUID NOT NULL REFERENCES coach_personas(id),
    recommendation_type TEXT NOT NULL, -- 'workout_plan', 'nutrition_plan', 'focus_area', 'habit_change'
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    reasoning TEXT, -- AI's reasoning for this recommendation
    priority INT DEFAULT 0, -- Higher = more important
    status TEXT DEFAULT 'pending', -- 'pending', 'accepted', 'rejected', 'completed'
    valid_from TIMESTAMPTZ DEFAULT NOW(),
    valid_until TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_coach_recommendations_user_id ON coach_recommendations(user_id);
CREATE INDEX IF NOT EXISTS idx_coach_recommendations_status ON coach_recommendations(status);
CREATE INDEX IF NOT EXISTS idx_coach_recommendations_priority ON coach_recommendations(priority DESC);

-- Recommendation feedback (user feedback on recommendations)
CREATE TABLE IF NOT EXISTS recommendation_feedback (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    recommendation_id UUID NOT NULL REFERENCES coach_recommendations(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    feedback_type TEXT NOT NULL, -- 'accepted', 'rejected', 'modified', 'completed'
    feedback_text TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_recommendation_feedback_recommendation ON recommendation_feedback(recommendation_id);

-- ============================================================================
-- WORKOUT PLANNING (Plans vs Actuals)
-- ============================================================================

-- Workout programs (high-level plans)
CREATE TABLE IF NOT EXISTS workout_programs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    coach_persona_id UUID REFERENCES coach_personas(id),
    name TEXT NOT NULL,
    description TEXT,
    goal TEXT, -- 'strength', 'hypertrophy', 'endurance', 'weight_loss', 'maintenance'
    frequency_per_week INT, -- Target workout frequency
    duration_weeks INT, -- Program duration
    status TEXT DEFAULT 'active', -- 'active', 'paused', 'completed', 'archived'
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_workout_programs_user_id ON workout_programs(user_id);
CREATE INDEX IF NOT EXISTS idx_workout_programs_status ON workout_programs(status);

-- Planned workouts (specific workout sessions in the plan)
CREATE TABLE IF NOT EXISTS planned_workouts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    program_id UUID NOT NULL REFERENCES workout_programs(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    description TEXT,
    workout_type TEXT, -- 'strength', 'cardio', 'hiit', 'flexibility', 'sports'
    target_day_of_week INT, -- 0=Sunday, 6=Saturday
    target_time_of_day TEXT, -- 'morning', 'afternoon', 'evening'
    estimated_duration_minutes INT,
    order_in_program INT, -- For sorting workouts in a program
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_planned_workouts_program ON planned_workouts(program_id);
CREATE INDEX IF NOT EXISTS idx_planned_workouts_user_id ON planned_workouts(user_id);

-- Planned exercises (exercises within a planned workout)
CREATE TABLE IF NOT EXISTS planned_exercises (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    planned_workout_id UUID NOT NULL REFERENCES planned_workouts(id) ON DELETE CASCADE,
    exercise_name TEXT NOT NULL,
    exercise_type TEXT, -- 'strength', 'cardio', 'flexibility'
    target_sets INT,
    target_reps_min INT,
    target_reps_max INT,
    target_weight DECIMAL(10,2),
    target_weight_unit TEXT DEFAULT 'lbs',
    target_duration_seconds INT, -- For cardio/timed exercises
    target_distance DECIMAL(10,2), -- For running/cycling
    target_distance_unit TEXT,
    rest_seconds INT, -- Rest between sets
    order_in_workout INT, -- For sorting exercises in a workout
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_planned_exercises_workout ON planned_exercises(planned_workout_id);

-- Actual workouts (what the user actually did)
CREATE TABLE IF NOT EXISTS actual_workouts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    planned_workout_id UUID REFERENCES planned_workouts(id), -- Link to plan if followed
    name TEXT NOT NULL,
    workout_type TEXT,
    started_at TIMESTAMPTZ NOT NULL,
    ended_at TIMESTAMPTZ,
    duration_minutes INT,
    notes TEXT,
    perceived_exertion INT, -- 1-10 RPE scale
    energy_level INT, -- 1-10 how energetic they felt
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_actual_workouts_user_id ON actual_workouts(user_id);
CREATE INDEX IF NOT EXISTS idx_actual_workouts_started_at ON actual_workouts(started_at DESC);
CREATE INDEX IF NOT EXISTS idx_actual_workouts_planned ON actual_workouts(planned_workout_id);

-- Actual exercise sets (individual sets performed)
CREATE TABLE IF NOT EXISTS actual_exercise_sets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    actual_workout_id UUID NOT NULL REFERENCES actual_workouts(id) ON DELETE CASCADE,
    planned_exercise_id UUID REFERENCES planned_exercises(id),
    exercise_name TEXT NOT NULL,
    exercise_type TEXT,
    set_number INT NOT NULL,
    reps INT,
    weight DECIMAL(10,2),
    weight_unit TEXT DEFAULT 'lbs',
    duration_seconds INT,
    distance DECIMAL(10,2),
    distance_unit TEXT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_actual_exercise_sets_workout ON actual_exercise_sets(actual_workout_id);
CREATE INDEX IF NOT EXISTS idx_actual_exercise_sets_exercise_name ON actual_exercise_sets(exercise_name);

-- Exercise progress tracking (progressive overload)
CREATE TABLE IF NOT EXISTS exercise_progress (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    exercise_name TEXT NOT NULL,
    date DATE NOT NULL,
    max_weight DECIMAL(10,2),
    weight_unit TEXT,
    max_reps INT,
    max_volume DECIMAL(10,2), -- Total volume (sets * reps * weight)
    total_sets INT,
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, exercise_name, date)
);

CREATE INDEX IF NOT EXISTS idx_exercise_progress_user_exercise ON exercise_progress(user_id, exercise_name, date DESC);

-- ============================================================================
-- NUTRITION PLANNING (Plans vs Actuals)
-- ============================================================================

-- Nutrition programs (high-level nutrition plans)
CREATE TABLE IF NOT EXISTS nutrition_programs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    coach_persona_id UUID REFERENCES coach_personas(id),
    name TEXT NOT NULL,
    description TEXT,
    goal TEXT, -- 'weight_loss', 'muscle_gain', 'maintenance', 'performance'
    target_calories INT,
    target_protein_grams INT,
    target_carbs_grams INT,
    target_fat_grams INT,
    meal_frequency INT, -- Number of meals per day
    status TEXT DEFAULT 'active', -- 'active', 'paused', 'completed', 'archived'
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_nutrition_programs_user_id ON nutrition_programs(user_id);
CREATE INDEX IF NOT EXISTS idx_nutrition_programs_status ON nutrition_programs(status);

-- Planned meals (specific meals in the plan)
CREATE TABLE IF NOT EXISTS planned_meals (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    program_id UUID NOT NULL REFERENCES nutrition_programs(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    meal_name TEXT NOT NULL, -- 'Breakfast', 'Lunch', 'Dinner', 'Snack 1', etc.
    meal_type TEXT, -- 'breakfast', 'lunch', 'dinner', 'snack', 'pre_workout', 'post_workout'
    target_time_of_day TEXT, -- 'morning', 'midday', 'afternoon', 'evening', 'night'
    target_calories INT,
    target_protein_grams INT,
    target_carbs_grams INT,
    target_fat_grams INT,
    recipe_description TEXT,
    notes TEXT,
    order_in_day INT, -- For sorting meals
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_planned_meals_program ON planned_meals(program_id);
CREATE INDEX IF NOT EXISTS idx_planned_meals_user_id ON planned_meals(user_id);

-- Planned meal foods (specific foods in a planned meal)
CREATE TABLE IF NOT EXISTS planned_meal_foods (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    planned_meal_id UUID NOT NULL REFERENCES planned_meals(id) ON DELETE CASCADE,
    food_name TEXT NOT NULL,
    quantity DECIMAL(10,2),
    unit TEXT, -- 'oz', 'g', 'cup', 'tbsp', 'serving'
    calories INT,
    protein_grams DECIMAL(5,2),
    carbs_grams DECIMAL(5,2),
    fat_grams DECIMAL(5,2),
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_planned_meal_foods_meal ON planned_meal_foods(planned_meal_id);

-- Nutrition compliance tracking
CREATE TABLE IF NOT EXISTS nutrition_compliance (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES profiles(id) ON DELETE CASCADE,
    program_id UUID REFERENCES nutrition_programs(id),
    date DATE NOT NULL,
    planned_calories INT,
    actual_calories INT,
    planned_protein_grams INT,
    actual_protein_grams INT,
    planned_carbs_grams INT,
    actual_carbs_grams INT,
    planned_fat_grams INT,
    actual_fat_grams INT,
    compliance_score DECIMAL(5,2), -- 0-100 score
    notes TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, date)
);

CREATE INDEX IF NOT EXISTS idx_nutrition_compliance_user_date ON nutrition_compliance(user_id, date DESC);

-- ============================================================================
-- TRIGGERS FOR UPDATED_AT TIMESTAMPS
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Add triggers for all tables with updated_at
DO $$
DECLARE
    t TEXT;
BEGIN
    FOR t IN
        SELECT unnest(ARRAY[
            'embeddings',
            'coach_personas',
            'coach_conversations',
            'coach_recommendations',
            'workout_programs',
            'planned_workouts',
            'planned_exercises',
            'actual_workouts',
            'nutrition_programs',
            'planned_meals'
        ])
    LOOP
        EXECUTE format('
            DROP TRIGGER IF EXISTS update_%I_updated_at ON %I;
            CREATE TRIGGER update_%I_updated_at
                BEFORE UPDATE ON %I
                FOR EACH ROW
                EXECUTE FUNCTION update_updated_at_column();
        ', t, t, t, t);
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- ============================================================================

-- Enable RLS on all new tables
ALTER TABLE embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE coach_personas ENABLE ROW LEVEL SECURITY;
ALTER TABLE coach_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE coach_recommendations ENABLE ROW LEVEL SECURITY;
ALTER TABLE recommendation_feedback ENABLE ROW LEVEL SECURITY;
ALTER TABLE workout_programs ENABLE ROW LEVEL SECURITY;
ALTER TABLE planned_workouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE planned_exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE actual_workouts ENABLE ROW LEVEL SECURITY;
ALTER TABLE actual_exercise_sets ENABLE ROW LEVEL SECURITY;
ALTER TABLE exercise_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE nutrition_programs ENABLE ROW LEVEL SECURITY;
ALTER TABLE planned_meals ENABLE ROW LEVEL SECURITY;
ALTER TABLE planned_meal_foods ENABLE ROW LEVEL SECURITY;
ALTER TABLE nutrition_compliance ENABLE ROW LEVEL SECURITY;

-- Policies for embeddings
CREATE POLICY "Users can view their own embeddings" ON embeddings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own embeddings" ON embeddings FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own embeddings" ON embeddings FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete their own embeddings" ON embeddings FOR DELETE USING (auth.uid() = user_id);

-- Policies for coach_personas (read-only for all authenticated users)
CREATE POLICY "Authenticated users can view coach personas" ON coach_personas FOR SELECT USING (auth.role() = 'authenticated');

-- Policies for coach_conversations
CREATE POLICY "Users can view their own conversations" ON coach_conversations FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own conversations" ON coach_conversations FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update their own conversations" ON coach_conversations FOR UPDATE USING (auth.uid() = user_id);

-- Policies for coach_recommendations
CREATE POLICY "Users can view their own recommendations" ON coach_recommendations FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update their own recommendations" ON coach_recommendations FOR UPDATE USING (auth.uid() = user_id);

-- Policies for recommendation_feedback
CREATE POLICY "Users can view their own feedback" ON recommendation_feedback FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert their own feedback" ON recommendation_feedback FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Policies for workout_programs
CREATE POLICY "Users can manage their workout programs" ON workout_programs FOR ALL USING (auth.uid() = user_id);

-- Policies for planned_workouts
CREATE POLICY "Users can manage their planned workouts" ON planned_workouts FOR ALL USING (auth.uid() = user_id);

-- Policies for planned_exercises
CREATE POLICY "Users can manage their planned exercises" ON planned_exercises FOR ALL USING (
    auth.uid() IN (SELECT user_id FROM planned_workouts WHERE id = planned_workout_id)
);

-- Policies for actual_workouts
CREATE POLICY "Users can manage their actual workouts" ON actual_workouts FOR ALL USING (auth.uid() = user_id);

-- Policies for actual_exercise_sets
CREATE POLICY "Users can manage their actual exercise sets" ON actual_exercise_sets FOR ALL USING (
    auth.uid() IN (SELECT user_id FROM actual_workouts WHERE id = actual_workout_id)
);

-- Policies for exercise_progress
CREATE POLICY "Users can manage their exercise progress" ON exercise_progress FOR ALL USING (auth.uid() = user_id);

-- Policies for nutrition_programs
CREATE POLICY "Users can manage their nutrition programs" ON nutrition_programs FOR ALL USING (auth.uid() = user_id);

-- Policies for planned_meals
CREATE POLICY "Users can manage their planned meals" ON planned_meals FOR ALL USING (auth.uid() = user_id);

-- Policies for planned_meal_foods
CREATE POLICY "Users can manage their planned meal foods" ON planned_meal_foods FOR ALL USING (
    auth.uid() IN (SELECT user_id FROM planned_meals WHERE id = planned_meal_id)
);

-- Policies for nutrition_compliance
CREATE POLICY "Users can manage their nutrition compliance" ON nutrition_compliance FOR ALL USING (auth.uid() = user_id);

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Function to calculate compliance score
CREATE OR REPLACE FUNCTION calculate_compliance_score(
    planned_cals INT,
    actual_cals INT,
    planned_protein INT,
    actual_protein INT,
    planned_carbs INT,
    actual_carbs INT,
    planned_fat INT,
    actual_fat INT
)
RETURNS DECIMAL(5,2)
LANGUAGE plpgsql
AS $$
DECLARE
    cal_score DECIMAL(5,2);
    protein_score DECIMAL(5,2);
    carb_score DECIMAL(5,2);
    fat_score DECIMAL(5,2);
    total_score DECIMAL(5,2);
BEGIN
    -- Calculate individual scores (100 - % difference)
    cal_score := GREATEST(0, 100 - ABS((actual_cals - planned_cals)::DECIMAL / NULLIF(planned_cals, 0) * 100));
    protein_score := GREATEST(0, 100 - ABS((actual_protein - planned_protein)::DECIMAL / NULLIF(planned_protein, 0) * 100));
    carb_score := GREATEST(0, 100 - ABS((actual_carbs - planned_carbs)::DECIMAL / NULLIF(planned_carbs, 0) * 100));
    fat_score := GREATEST(0, 100 - ABS((actual_fat - planned_fat)::DECIMAL / NULLIF(planned_fat, 0) * 100));

    -- Weighted average (protein weighted higher)
    total_score := (cal_score * 0.3 + protein_score * 0.4 + carb_score * 0.15 + fat_score * 0.15);

    RETURN ROUND(total_score, 2);
END;
$$;

-- ============================================================================
-- COMPLETION
-- ============================================================================

-- Log migration completion
DO $$
BEGIN
    RAISE NOTICE 'Phase 1 migration completed successfully!';
    RAISE NOTICE 'Created tables: embeddings, coach_personas, coach_conversations, coach_recommendations, recommendation_feedback';
    RAISE NOTICE 'Created tables: workout_programs, planned_workouts, planned_exercises, actual_workouts, actual_exercise_sets, exercise_progress';
    RAISE NOTICE 'Created tables: nutrition_programs, planned_meals, planned_meal_foods, nutrition_compliance';
    RAISE NOTICE 'Created functions: match_embeddings, calculate_compliance_score';
    RAISE NOTICE 'All RLS policies configured';
END $$;
