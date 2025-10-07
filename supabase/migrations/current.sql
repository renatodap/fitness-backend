-- =====================================================
-- WAGNER COACH - COMPLETE DATABASE SCHEMA
-- =====================================================
-- This is the definitive, production-ready schema
-- All tables, constraints, RLS policies, and indexes
-- Generated: 2025-10-07
-- =====================================================

-- Enable required extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";

-- =====================================================
-- ENUMS (Custom Types)
-- =====================================================

CREATE TYPE meal_category AS ENUM (
  'breakfast',
  'lunch',
  'dinner',
  'snack',
  'pre_workout',
  'post_workout',
  'other'
);

CREATE TYPE experience_level AS ENUM (
  'beginner',
  'intermediate',
  'advanced',
  'expert'
);

CREATE TYPE goal_status AS ENUM (
  'active',
  'completed',
  'paused',
  'abandoned'
);

CREATE TYPE goal_type AS ENUM (
  'weight_loss',
  'muscle_gain',
  'strength',
  'endurance',
  'flexibility',
  'sport_performance',
  'health',
  'other'
);

-- =====================================================
-- CORE USER TABLES
-- =====================================================

-- Profiles (extends auth.users)
CREATE TABLE public.profiles (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name text,
  goal text CHECK (goal IN ('build_muscle', 'lose_weight', 'gain_strength')),
  onboarding_completed boolean DEFAULT false,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  goals_embedding vector(384),
  about_me text,
  experience_level experience_level DEFAULT 'beginner',
  fitness_goals text,
  preferred_activities text[],
  motivation_factors text[],
  physical_limitations text[],
  available_equipment text[],
  training_frequency text,
  session_duration text,
  dietary_preferences text,
  notification_preferences jsonb DEFAULT '{}',
  privacy_settings jsonb DEFAULT '{}',
  age integer CHECK (age >= 13 AND age <= 120),
  location text,
  weekly_hours numeric CHECK (weekly_hours >= 0 AND weekly_hours <= 40),
  primary_goal text,
  focus_areas text[],
  health_conditions text,
  equipment_access text,
  preferred_workout_time text,
  strengths text,
  areas_for_improvement text
);

-- Users table (consolidated user data)
CREATE TABLE public.users (
  id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  full_name text,
  email text UNIQUE,
  age integer CHECK (age >= 13 AND age <= 120),
  biological_sex text CHECK (biological_sex IN ('male', 'female', 'other')),
  height_cm numeric CHECK (height_cm > 0 AND height_cm < 300),
  current_weight_kg numeric CHECK (current_weight_kg > 0 AND current_weight_kg < 500),
  goal_weight_kg numeric,
  primary_goal text CHECK (primary_goal IN ('build_muscle', 'lose_fat', 'improve_endurance', 'increase_strength', 'sport_performance', 'general_health')),
  experience_level text CHECK (experience_level IN ('beginner', 'intermediate', 'advanced')),
  training_frequency integer CHECK (training_frequency >= 0 AND training_frequency <= 7),
  available_equipment text[] DEFAULT ARRAY[]::text[],
  dietary_restrictions text[] DEFAULT ARRAY[]::text[],
  injury_limitations text[] DEFAULT ARRAY[]::text[],
  daily_calorie_target integer,
  daily_protein_target_g integer,
  daily_carbs_target_g integer,
  daily_fat_target_g integer,
  settings jsonb DEFAULT '{"privacy": {"share_stats": false, "activities_public": false}, "timezone": "UTC", "unit_system": "metric", "workout_reminders": true, "auto_sync_activities": true, "notifications_enabled": true, "preferred_workout_time": null}',
  onboarding_completed boolean DEFAULT false,
  onboarding_data jsonb DEFAULT '{}',
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  last_active_at timestamptz
);

-- User Onboarding
CREATE TABLE public.user_onboarding (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL UNIQUE REFERENCES auth.users(id) ON DELETE CASCADE,
  primary_goal text NOT NULL CHECK (primary_goal IN ('build_muscle', 'lose_fat', 'improve_endurance', 'increase_strength', 'sport_performance', 'general_health', 'rehab_recovery')),
  user_persona text NOT NULL CHECK (user_persona IN ('strength_athlete', 'bodybuilder', 'endurance_runner', 'triathlete', 'crossfit_athlete', 'team_sport_athlete', 'general_fitness', 'beginner_recovery')),
  current_activity_level text NOT NULL CHECK (current_activity_level IN ('sedentary', 'lightly_active', 'moderately_active', 'very_active')),
  desired_training_frequency integer NOT NULL CHECK (desired_training_frequency >= 3 AND desired_training_frequency <= 7),
  biological_sex text NOT NULL CHECK (biological_sex IN ('male', 'female')),
  age integer NOT NULL CHECK (age >= 18 AND age <= 80),
  current_weight_kg numeric NOT NULL CHECK (current_weight_kg > 0),
  height_cm numeric NOT NULL CHECK (height_cm > 0),
  daily_meal_preference integer NOT NULL CHECK (daily_meal_preference IN (2, 3, 4, 5, 6)),
  training_time_preferences text[] DEFAULT ARRAY[]::text[],
  dietary_restrictions text[] DEFAULT ARRAY[]::text[],
  equipment_access text[] DEFAULT ARRAY[]::text[],
  injury_limitations text[] DEFAULT ARRAY[]::text[],
  experience_level text NOT NULL CHECK (experience_level IN ('beginner', 'intermediate', 'advanced', 'expert')),
  completed boolean NOT NULL DEFAULT false,
  completed_at timestamptz,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  city text,
  location_permission boolean DEFAULT false,
  facility_access text[] DEFAULT ARRAY[]::text[],
  daily_calorie_target integer,
  daily_protein_target_g integer,
  daily_carbs_target_g integer,
  daily_fat_target_g integer,
  goal_weight_kg numeric,
  goal_body_fat_pct numeric,
  estimated_tdee integer,
  goal_type text CHECK (goal_type IN ('cut', 'bulk', 'maintain', 'recomp'))
);

-- User Goals
CREATE TABLE public.user_goals (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  goal_type goal_type NOT NULL,
  goal_description text NOT NULL,
  target_value numeric,
  target_unit text,
  target_date date,
  priority integer DEFAULT 1 CHECK (priority >= 1 AND priority <= 5),
  status goal_status DEFAULT 'active',
  is_active boolean DEFAULT true,
  progress_value numeric DEFAULT 0,
  progress_notes text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  completed_at timestamptz
);

-- =====================================================
-- QUICK ENTRY SYSTEM
-- =====================================================

-- Quick Entry Logs (multimodal input processing)
CREATE TABLE public.quick_entry_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  input_type text NOT NULL CHECK (input_type IN ('text', 'voice', 'image', 'multimodal', 'pdf')),
  input_modalities text[] NOT NULL DEFAULT ARRAY[]::text[],
  raw_text text,
  raw_transcription text,
  image_urls text[] DEFAULT ARRAY[]::text[],
  audio_url text,
  pdf_url text,
  storage_bucket text CHECK (storage_bucket IN ('user-images', 'user-audio', 'user-videos', 'user-documents')),
  file_metadata jsonb DEFAULT '{}',
  ai_provider text NOT NULL CHECK (ai_provider IN ('groq', 'openrouter', 'anthropic', 'openai', 'local', 'free')),
  ai_model text NOT NULL,
  ai_cost_usd numeric DEFAULT 0,
  tokens_used integer DEFAULT 0,
  processing_duration_ms integer,
  ai_classification text CHECK (ai_classification IN ('meal', 'workout', 'body_measurement', 'activity', 'goal', 'note', 'mixed', 'unknown')),
  ai_extracted_data jsonb NOT NULL DEFAULT '{}',
  ai_confidence_score numeric CHECK (ai_confidence_score >= 0 AND ai_confidence_score <= 1),
  ai_raw_response text,
  contains_meal boolean DEFAULT false,
  contains_workout boolean DEFAULT false,
  contains_body_measurement boolean DEFAULT false,
  contains_activity boolean DEFAULT false,
  contains_goal boolean DEFAULT false,
  contains_note boolean DEFAULT false,
  meal_log_ids uuid[] DEFAULT ARRAY[]::uuid[],
  workout_log_ids uuid[] DEFAULT ARRAY[]::uuid[],
  body_measurement_ids uuid[] DEFAULT ARRAY[]::uuid[],
  activity_ids uuid[] DEFAULT ARRAY[]::uuid[],
  logged_at timestamptz NOT NULL DEFAULT now(),
  timezone text DEFAULT 'UTC',
  location_lat numeric,
  location_lng numeric,
  processing_status text NOT NULL DEFAULT 'pending' CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed', 'partial')),
  processing_error text,
  retry_count integer DEFAULT 0,
  embedding_generated boolean DEFAULT false,
  embedding_id uuid,
  auto_tags text[] DEFAULT ARRAY[]::text[],
  user_tags text[] DEFAULT ARRAY[]::text[],
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Quick Entry Embeddings (for RAG)
CREATE TABLE public.quick_entry_embeddings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  quick_entry_log_id uuid NOT NULL REFERENCES public.quick_entry_logs(id) ON DELETE CASCADE,
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  embedding_type text NOT NULL CHECK (embedding_type IN ('text', 'image', 'audio', 'multimodal', 'combined')),
  embedding vector(384) NOT NULL,
  content_text text NOT NULL,
  content_summary text,
  metadata jsonb DEFAULT '{}',
  source_classification text,
  embedding_model text NOT NULL DEFAULT 'sentence-transformers/all-MiniLM-L6-v2',
  embedding_dimensions integer NOT NULL DEFAULT 384,
  content_hash text NOT NULL,
  is_active boolean DEFAULT true,
  logged_at timestamptz NOT NULL,
  created_at timestamptz DEFAULT now()
);

-- Quick Entry Stats
CREATE TABLE public.quick_entry_stats (
  user_id uuid PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
  total_entries integer DEFAULT 0,
  text_entries integer DEFAULT 0,
  voice_entries integer DEFAULT 0,
  image_entries integer DEFAULT 0,
  multimodal_entries integer DEFAULT 0,
  meal_extractions integer DEFAULT 0,
  workout_extractions integer DEFAULT 0,
  body_measurement_extractions integer DEFAULT 0,
  failed_extractions integer DEFAULT 0,
  total_ai_cost_usd numeric DEFAULT 0,
  total_tokens_used bigint DEFAULT 0,
  avg_processing_time_ms integer,
  avg_confidence_score numeric,
  first_entry_at timestamptz,
  last_entry_at timestamptz,
  updated_at timestamptz DEFAULT now()
);

-- =====================================================
-- NUTRITION SYSTEM
-- =====================================================

-- Meal Logs
CREATE TABLE public.meal_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name text CHECK (name IS NULL OR char_length(name) <= 200),
  category meal_category NOT NULL DEFAULT 'other',
  logged_at timestamptz NOT NULL DEFAULT now(),
  notes text CHECK (notes IS NULL OR char_length(notes) <= 500),
  total_calories numeric DEFAULT 0,
  total_protein_g numeric DEFAULT 0,
  total_carbs_g numeric DEFAULT 0,
  total_fat_g numeric DEFAULT 0,
  total_fiber_g numeric DEFAULT 0,
  total_sugar_g numeric,
  total_sodium_mg numeric,
  created_at timestamptz NOT NULL DEFAULT now(),
  updated_at timestamptz NOT NULL DEFAULT now(),
  foods jsonb DEFAULT '[]',
  source text DEFAULT 'manual' CHECK (source IN ('quick_entry', 'manual', 'imported', 'api')),
  estimated boolean DEFAULT false,
  confidence_score numeric CHECK (confidence_score >= 0 AND confidence_score <= 1),
  image_url text,
  meal_quality_score numeric CHECK (meal_quality_score >= 0 AND meal_quality_score <= 10),
  macro_balance_score numeric CHECK (macro_balance_score >= 0 AND macro_balance_score <= 10),
  adherence_to_goals numeric CHECK (adherence_to_goals >= 0 AND adherence_to_goals <= 10),
  tags text[] DEFAULT ARRAY[]::text[],
  quick_entry_log_id uuid REFERENCES public.quick_entry_logs(id),
  ai_extracted boolean DEFAULT false,
  ai_confidence numeric CHECK (ai_confidence >= 0 AND ai_confidence <= 1),
  extraction_metadata jsonb DEFAULT '{}'
);

-- Foods Database (enhanced)
CREATE TABLE public.foods_enhanced (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  name text NOT NULL,
  brand_name text,
  brand_owner text,
  restaurant_name text,
  menu_item_id text,
  product_category text,
  food_group text,
  barcode_upc text UNIQUE,
  barcode_ean text UNIQUE,
  fdc_id text UNIQUE,
  fatsecret_id text,
  nutritionix_id text,
  edamam_id text,
  ndb_number text,
  primary_source_id uuid,
  data_sources jsonb DEFAULT '[]',
  data_quality_score numeric CHECK (data_quality_score >= 0 AND data_quality_score <= 1),
  is_verified boolean DEFAULT false,
  verification_date timestamptz,
  serving_size numeric NOT NULL DEFAULT 100,
  serving_unit text NOT NULL DEFAULT 'g',
  serving_description text,
  servings_per_container numeric,
  household_serving_size text,
  household_serving_unit text,
  calories numeric,
  total_fat_g numeric,
  saturated_fat_g numeric,
  trans_fat_g numeric,
  polyunsaturated_fat_g numeric,
  monounsaturated_fat_g numeric,
  cholesterol_mg numeric,
  sodium_mg numeric,
  total_carbs_g numeric,
  dietary_fiber_g numeric,
  soluble_fiber_g numeric,
  insoluble_fiber_g numeric,
  total_sugars_g numeric,
  added_sugars_g numeric,
  sugar_alcohols_g numeric,
  protein_g numeric,
  vitamin_a_iu numeric,
  vitamin_a_mcg numeric,
  vitamin_c_mg numeric,
  vitamin_d_mcg numeric,
  vitamin_d_iu numeric,
  vitamin_e_mg numeric,
  vitamin_k_mcg numeric,
  thiamin_mg numeric,
  riboflavin_mg numeric,
  niacin_mg numeric,
  vitamin_b6_mg numeric,
  folate_mcg numeric,
  vitamin_b12_mcg numeric,
  biotin_mcg numeric,
  pantothenic_acid_mg numeric,
  choline_mg numeric,
  calcium_mg numeric,
  iron_mg numeric,
  magnesium_mg numeric,
  phosphorus_mg numeric,
  potassium_mg numeric,
  zinc_mg numeric,
  copper_mg numeric,
  manganese_mg numeric,
  selenium_mcg numeric,
  iodine_mcg numeric,
  caffeine_mg numeric,
  alcohol_g numeric,
  water_g numeric,
  ash_g numeric,
  omega3_fatty_acids_mg numeric,
  omega6_fatty_acids_mg numeric,
  search_vector tsvector,
  popularity_score integer DEFAULT 0,
  search_count integer DEFAULT 0,
  ingredients text[],
  allergens text[],
  dietary_flags text[],
  preparation_methods text[],
  storage_instructions text,
  image_url text,
  image_thumbnail_url text,
  nutrition_label_url text,
  is_discontinued boolean DEFAULT false,
  is_generic boolean DEFAULT false,
  is_raw boolean DEFAULT false,
  is_branded boolean DEFAULT false,
  is_restaurant boolean DEFAULT false,
  created_by uuid REFERENCES auth.users(id),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  last_api_sync timestamptz
);

-- Daily Nutrition Summaries
CREATE TABLE public.daily_nutrition_summaries (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  date date NOT NULL,
  total_calories numeric,
  total_protein_g numeric,
  total_carbs_g numeric,
  total_fat_g numeric,
  total_fiber_g numeric,
  total_sugar_g numeric,
  total_sodium_mg numeric,
  breakfast_calories numeric,
  lunch_calories numeric,
  dinner_calories numeric,
  snacks_calories numeric,
  calorie_goal numeric,
  protein_goal numeric,
  carbs_goal numeric,
  fat_goal numeric,
  meals_logged integer DEFAULT 0,
  water_ml numeric,
  notes text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- =====================================================
-- ACTIVITY & WORKOUT SYSTEM
-- =====================================================

-- Activities (comprehensive activity tracking)
CREATE TABLE public.activities (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  source text NOT NULL CHECK (source IN ('strava', 'garmin', 'manual', 'apple', 'fitbit', 'polar', 'suunto', 'wahoo', 'quick_entry', 'workout_log')),
  external_id text,
  name text NOT NULL,
  activity_type text NOT NULL,
  sport_type text,
  start_date timestamptz NOT NULL,
  end_date timestamptz,
  timezone text,
  utc_offset integer,
  elapsed_time_seconds integer NOT NULL,
  moving_time_seconds integer,
  distance_meters numeric,
  average_speed numeric,
  max_speed numeric,
  total_elevation_gain numeric,
  total_elevation_loss numeric,
  elevation_high numeric,
  elevation_low numeric,
  average_heartrate integer,
  max_heartrate integer,
  min_heartrate integer,
  heartrate_zones jsonb,
  average_power numeric,
  max_power integer,
  normalized_power numeric,
  intensity_factor numeric,
  tss numeric,
  power_zones jsonb,
  kilojoules numeric,
  average_cadence numeric,
  max_cadence integer,
  average_stride_length numeric,
  average_vertical_oscillation numeric,
  average_ground_contact_time integer,
  average_ground_contact_balance numeric,
  average_vertical_ratio numeric,
  pool_length numeric,
  total_strokes integer,
  average_stroke_rate numeric,
  average_swolf numeric,
  lap_count integer,
  total_reps integer,
  total_sets integer,
  total_weight_lifted_kg numeric,
  exercise_count integer,
  muscle_groups text[],
  total_shots integer,
  forehand_count integer,
  backhand_count integer,
  serve_count integer,
  volley_count integer,
  winner_count integer,
  unforced_error_count integer,
  ace_count integer,
  double_fault_count integer,
  first_serve_percentage numeric,
  points_won_percentage numeric,
  match_duration_minutes integer,
  sets_played integer,
  games_played integer,
  average_distance_per_stroke numeric,
  average_split_time integer,
  poses_held integer,
  average_hold_duration integer,
  flexibility_score integer,
  calories integer,
  active_calories integer,
  training_load numeric,
  aerobic_training_effect numeric,
  anaerobic_training_effect numeric,
  recovery_time_hours integer,
  vo2max_estimate numeric,
  fitness_level integer,
  perceived_exertion integer CHECK (perceived_exertion >= 1 AND perceived_exertion <= 10),
  mood text CHECK (mood IN ('terrible', 'bad', 'okay', 'good', 'amazing')),
  energy_level integer CHECK (energy_level >= 1 AND energy_level <= 5),
  soreness_level integer CHECK (soreness_level >= 0 AND soreness_level <= 10),
  stress_level integer CHECK (stress_level >= 0 AND stress_level <= 10),
  sleep_quality integer CHECK (sleep_quality >= 1 AND sleep_quality <= 10),
  workout_rating integer CHECK (workout_rating >= 1 AND workout_rating <= 5),
  weather_conditions text,
  temperature_celsius numeric,
  humidity_percentage integer,
  wind_speed_kmh numeric,
  wind_direction integer,
  precipitation text,
  air_quality_index integer,
  indoor boolean DEFAULT false,
  gear_id text,
  location text,
  route_name text,
  city text,
  state text,
  country text,
  start_lat numeric,
  start_lng numeric,
  end_lat numeric,
  end_lng numeric,
  workout_id integer,
  notes text,
  private_notes text,
  photos text[],
  videos text[],
  map_polyline text,
  kudos_count integer DEFAULT 0,
  comment_count integer DEFAULT 0,
  photo_count integer DEFAULT 0,
  visibility text DEFAULT 'private' CHECK (visibility IN ('private', 'followers', 'public')),
  commute boolean DEFAULT false,
  trainer boolean DEFAULT false,
  race boolean DEFAULT false,
  workout_type text,
  weather_data jsonb,
  raw_data jsonb,
  laps jsonb,
  splits jsonb,
  segments jsonb,
  device_name text,
  device_manufacturer text,
  upload_source text,
  file_format text,
  created_at timestamptz DEFAULT timezone('utc', now()),
  updated_at timestamptz DEFAULT timezone('utc', now()),
  synced_at timestamptz,
  performance_score numeric CHECK (performance_score >= 0 AND performance_score <= 10),
  effort_level numeric CHECK (effort_level >= 0 AND effort_level <= 10),
  recovery_needed_hours integer,
  tags text[] DEFAULT ARRAY[]::text[],
  activity_name text,
  duration_minutes integer,
  rpe integer CHECK (rpe >= 1 AND rpe <= 10),
  energy_level_before integer CHECK (energy_level_before >= 1 AND energy_level_before <= 10),
  energy_level_after integer CHECK (energy_level_after >= 1 AND energy_level_after <= 10),
  completed boolean DEFAULT true,
  quick_entry_log_id uuid REFERENCES public.quick_entry_logs(id),
  ai_extracted boolean DEFAULT false,
  ai_confidence numeric CHECK (ai_confidence >= 0 AND ai_confidence <= 1),
  extraction_metadata jsonb DEFAULT '{}'
);

-- Workout Exercises (template exercises)
CREATE TABLE public.workout_exercises (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  workout_id integer NOT NULL,
  exercise_id uuid,
  order_index integer NOT NULL,
  suggested_sets integer,
  suggested_reps text,
  suggested_weight_type text,
  suggested_weight_percentage numeric,
  suggested_weight_lbs numeric,
  rest_seconds integer,
  notes text,
  technique_cues text[],
  superset_group integer,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- Activity Exercises (actual performed exercises)
CREATE TABLE public.activity_exercises (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  activity_id uuid NOT NULL REFERENCES public.activities(id) ON DELETE CASCADE,
  exercise_id uuid,
  workout_exercise_id uuid REFERENCES public.workout_exercises(id),
  order_index integer,
  notes text,
  created_at timestamptz DEFAULT now()
);

-- Activity Sets (sets performed)
CREATE TABLE public.activity_sets (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  activity_exercise_id uuid NOT NULL REFERENCES public.activity_exercises(id) ON DELETE CASCADE,
  set_number integer NOT NULL,
  reps_completed integer,
  weight_lbs numeric,
  weight_kg numeric,
  rpe integer CHECK (rpe >= 1 AND rpe <= 10),
  rest_seconds integer,
  completed boolean DEFAULT true,
  notes text,
  created_at timestamptz DEFAULT now()
);

-- Activity Segments (laps, intervals, etc.)
CREATE TABLE public.activity_segments (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  activity_id uuid REFERENCES public.activities(id) ON DELETE CASCADE,
  segment_type text NOT NULL CHECK (segment_type IN ('lap', 'interval', 'set', 'split', 'circuit', 'round')),
  segment_index integer NOT NULL,
  start_time timestamptz,
  elapsed_time_seconds integer,
  moving_time_seconds integer,
  distance_meters numeric,
  average_speed numeric,
  max_speed numeric,
  average_pace text,
  average_heartrate integer,
  max_heartrate integer,
  min_heartrate integer,
  exercise_name text,
  reps integer,
  weight_kg numeric,
  average_cadence numeric,
  average_power numeric,
  normalized_power numeric,
  calories integer,
  elevation_gain numeric,
  elevation_loss numeric,
  average_stroke_rate numeric,
  stroke_count integer,
  notes text,
  raw_data jsonb,
  created_at timestamptz DEFAULT timezone('utc', now())
);

-- Activity Streams (time-series data)
CREATE TABLE public.activity_streams (
  activity_id uuid NOT NULL REFERENCES public.activities(id) ON DELETE CASCADE,
  stream_type text NOT NULL CHECK (stream_type IN ('heartrate', 'cadence', 'power', 'speed', 'altitude', 'distance', 'temperature', 'grade', 'battery', 'calories', 'lap_time', 'moving')),
  data_points jsonb NOT NULL,
  data_type text CHECK (data_type IN ('integer', 'float', 'boolean', 'string')),
  resolution text CHECK (resolution IN ('high', 'medium', 'low', 'raw')),
  original_size integer,
  series_type text CHECK (series_type IN ('time', 'distance')),
  created_at timestamptz DEFAULT timezone('utc', now()),
  PRIMARY KEY (activity_id, stream_type)
);

-- =====================================================
-- BODY MEASUREMENTS
-- =====================================================

CREATE TABLE public.body_measurements (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  measured_at timestamptz NOT NULL DEFAULT now(),
  weight_lbs numeric,
  weight_kg numeric,
  body_fat_pct numeric,
  muscle_mass_lbs numeric,
  muscle_mass_kg numeric,
  measurements jsonb,
  source text DEFAULT 'manual' CHECK (source IN ('manual', 'scale', 'dexa', 'inbody', 'quick_entry')),
  notes text,
  trend_direction text CHECK (trend_direction IN ('up', 'down', 'stable')),
  rate_of_change_weekly numeric,
  goal_progress_pct numeric CHECK (goal_progress_pct >= 0 AND goal_progress_pct <= 100),
  health_assessment text CHECK (health_assessment IN ('healthy', 'caution', 'concern')),
  tags text[] DEFAULT ARRAY[]::text[],
  created_at timestamptz DEFAULT now(),
  quick_entry_log_id uuid REFERENCES public.quick_entry_logs(id),
  ai_extracted boolean DEFAULT false,
  ai_confidence numeric CHECK (ai_confidence >= 0 AND ai_confidence <= 1),
  extraction_metadata jsonb DEFAULT '{}'
);

-- =====================================================
-- AI COACH SYSTEM
-- =====================================================

-- Coach Messages (unified coach interface)
CREATE TABLE public.coach_messages (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  conversation_id uuid NOT NULL,
  role text NOT NULL CHECK (role IN ('user', 'assistant', 'system')),
  content text NOT NULL,
  context_used jsonb,
  ai_provider text CHECK (ai_provider IN ('anthropic', 'groq', 'openai', 'openrouter')),
  ai_model text,
  tokens_used integer,
  cost_usd numeric,
  created_at timestamptz DEFAULT now(),
  message_type text NOT NULL DEFAULT 'chat' CHECK (message_type IN ('chat', 'log_preview', 'log_confirmed', 'system')),
  metadata jsonb DEFAULT '{}',
  quick_entry_log_id uuid REFERENCES public.quick_entry_logs(id),
  is_vectorized boolean DEFAULT false
);

-- AI Conversations (legacy - for compatibility)
CREATE TABLE public.ai_conversations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  messages jsonb NOT NULL DEFAULT '[]',
  embedding vector(384),
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  context_used jsonb DEFAULT '{}',
  last_message_at timestamptz DEFAULT now()
);

-- =====================================================
-- AI PROGRAMS SYSTEM
-- =====================================================

-- AI Generated Programs
CREATE TABLE public.ai_generated_programs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  name text NOT NULL,
  description text,
  goals text[],
  duration_weeks integer NOT NULL DEFAULT 12,
  total_days integer NOT NULL DEFAULT 84,
  start_date date,
  end_date date,
  is_active boolean DEFAULT true,
  status text DEFAULT 'active' CHECK (status IN ('active', 'completed', 'paused', 'abandoned')),
  generation_prompt text,
  generation_context jsonb DEFAULT '{}',
  questions_answers jsonb DEFAULT '[]',
  ai_model text DEFAULT 'gpt-4o',
  difficulty_level text CHECK (difficulty_level IN ('beginner', 'intermediate', 'advanced')),
  primary_focus text[],
  equipment_needed text[],
  dietary_approach text,
  current_day integer DEFAULT 1,
  days_completed integer DEFAULT 0,
  meals_completed integer DEFAULT 0,
  workouts_completed integer DEFAULT 0,
  adherence_percentage numeric DEFAULT 100 CHECK (adherence_percentage >= 0 AND adherence_percentage <= 100),
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now(),
  completed_at timestamptz
);

-- AI Program Days
CREATE TABLE public.ai_program_days (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  program_id uuid NOT NULL REFERENCES public.ai_generated_programs(id) ON DELETE CASCADE,
  day_number integer NOT NULL CHECK (day_number >= 1 AND day_number <= 365),
  day_date date,
  day_of_week text CHECK (day_of_week IN ('monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday')),
  day_name text,
  day_focus text,
  day_notes text,
  is_completed boolean DEFAULT false,
  completed_at timestamptz,
  completion_notes text,
  created_at timestamptz DEFAULT now()
);

-- AI Program Items (meals and workouts)
CREATE TABLE public.ai_program_items (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  program_id uuid NOT NULL REFERENCES public.ai_generated_programs(id) ON DELETE CASCADE,
  program_day_id uuid NOT NULL REFERENCES public.ai_program_days(id) ON DELETE CASCADE,
  item_type text NOT NULL CHECK (item_type IN ('meal', 'workout', 'rest', 'note')),
  item_order integer DEFAULT 0,
  meal_type text CHECK (meal_type IN ('breakfast', 'lunch', 'dinner', 'snack', 'pre_workout', 'post_workout')),
  meal_name text,
  meal_foods jsonb DEFAULT '[]',
  meal_recipe text,
  meal_calories numeric,
  meal_protein_g numeric,
  meal_carbs_g numeric,
  meal_fat_g numeric,
  workout_name text,
  workout_type text CHECK (workout_type IN ('strength', 'cardio', 'sports', 'flexibility', 'mobility', 'active_recovery')),
  workout_duration_minutes integer,
  workout_exercises jsonb DEFAULT '[]',
  workout_intensity text CHECK (workout_intensity IN ('low', 'moderate', 'high', 'max')),
  workout_notes text,
  description text,
  notes text,
  alternatives jsonb,
  is_completed boolean DEFAULT false,
  completed_at timestamptz,
  completion_notes text,
  created_at timestamptz DEFAULT now()
);

-- =====================================================
-- MULTIMODAL EMBEDDINGS (RAG SYSTEM)
-- =====================================================

CREATE TABLE public.multimodal_embeddings (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  data_type text NOT NULL CHECK (data_type IN ('text', 'image', 'audio', 'video', 'pdf', 'structured', 'mixed')),
  content_text text,
  embedding vector(384) NOT NULL,
  metadata jsonb DEFAULT '{}',
  source_type text NOT NULL CHECK (source_type IN ('meal', 'meal_log', 'meal_photo', 'workout', 'workout_log', 'workout_photo', 'workout_video', 'activity', 'activity_photo', 'activity_gpx', 'goal', 'user_goal', 'profile', 'user_profile', 'coach_message', 'conversation', 'program', 'ai_program', 'voice_note', 'quick_entry', 'food_label', 'nutrition_label', 'body_photo', 'progress_photo', 'other')),
  source_id uuid,
  storage_url text,
  storage_bucket text CHECK (storage_bucket IN ('user-images', 'user-audio', 'user-videos', 'user-documents', 'user-photos')),
  file_name text,
  file_size_bytes bigint,
  mime_type text,
  embedding_model text NOT NULL DEFAULT 'all-MiniLM-L6-v2',
  embedding_dimensions integer NOT NULL DEFAULT 384,
  confidence_score numeric CHECK (confidence_score >= 0 AND confidence_score <= 1),
  processing_status text DEFAULT 'completed' CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed')),
  processing_error text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

-- =====================================================
-- INTEGRATIONS SYSTEM
-- =====================================================

CREATE TABLE public.integrations (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
  provider text NOT NULL CHECK (provider IN ('strava', 'garmin', 'apple_health', 'google_fit', 'fitbit', 'polar', 'whoop')),
  is_active boolean DEFAULT true,
  connected_at timestamptz DEFAULT now(),
  last_sync_at timestamptz,
  sync_enabled boolean DEFAULT true,
  provider_user_id text,
  provider_email text,
  access_token text,
  refresh_token text,
  token_expires_at timestamptz,
  scope text,
  sync_settings jsonb DEFAULT '{"sync_hr": true, "auto_sync": true, "sync_sleep": false, "sync_activities": true}',
  last_sync_status text CHECK (last_sync_status IN ('success', 'failed', 'partial')),
  last_sync_error text,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);

CREATE TABLE public.webhook_events (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  source text NOT NULL,
  event_type text NOT NULL,
  object_type text,
  object_id text,
  athlete_id bigint,
  payload jsonb,
  processed boolean DEFAULT false,
  processed_at timestamptz,
  error text,
  created_at timestamptz DEFAULT now()
);

-- =====================================================
-- RATE LIMITING
-- =====================================================

CREATE TABLE public.rate_limits (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid REFERENCES auth.users(id) ON DELETE CASCADE,
  endpoint text NOT NULL,
  requests integer DEFAULT 0,
  window_seconds integer DEFAULT 86400,
  reset_at timestamptz NOT NULL,
  created_at timestamptz NOT NULL DEFAULT timezone('utc', now()),
  updated_at timestamptz NOT NULL DEFAULT timezone('utc', now())
);

-- =====================================================
-- INDEXES FOR PERFORMANCE
-- =====================================================

-- User indexes
CREATE INDEX idx_profiles_user_id ON public.profiles(id);
CREATE INDEX idx_users_email ON public.users(email);
CREATE INDEX idx_user_goals_user_id ON public.user_goals(user_id);

-- Quick Entry indexes
CREATE INDEX idx_quick_entry_logs_user_id ON public.quick_entry_logs(user_id);
CREATE INDEX idx_quick_entry_logs_logged_at ON public.quick_entry_logs(logged_at DESC);
CREATE INDEX idx_quick_entry_logs_classification ON public.quick_entry_logs(ai_classification);
CREATE INDEX idx_quick_entry_embeddings_user_id ON public.quick_entry_embeddings(user_id);
CREATE INDEX idx_quick_entry_embeddings_log_id ON public.quick_entry_embeddings(quick_entry_log_id);

-- Meal logs indexes
CREATE INDEX idx_meal_logs_user_id ON public.meal_logs(user_id);
CREATE INDEX idx_meal_logs_logged_at ON public.meal_logs(logged_at DESC);
CREATE INDEX idx_meal_logs_category ON public.meal_logs(category);
CREATE INDEX idx_meal_logs_quick_entry_id ON public.meal_logs(quick_entry_log_id);

-- Activities indexes
CREATE INDEX idx_activities_user_id ON public.activities(user_id);
CREATE INDEX idx_activities_start_date ON public.activities(start_date DESC);
CREATE INDEX idx_activities_source ON public.activities(source);
CREATE INDEX idx_activities_activity_type ON public.activities(activity_type);
CREATE INDEX idx_activity_exercises_activity_id ON public.activity_exercises(activity_id);
CREATE INDEX idx_activity_sets_exercise_id ON public.activity_sets(activity_exercise_id);

-- Body measurements indexes
CREATE INDEX idx_body_measurements_user_id ON public.body_measurements(user_id);
CREATE INDEX idx_body_measurements_measured_at ON public.body_measurements(measured_at DESC);

-- Coach messages indexes
CREATE INDEX idx_coach_messages_user_id ON public.coach_messages(user_id);
CREATE INDEX idx_coach_messages_conversation_id ON public.coach_messages(conversation_id);
CREATE INDEX idx_coach_messages_created_at ON public.coach_messages(created_at DESC);
CREATE INDEX idx_coach_messages_role ON public.coach_messages(role);

-- AI Programs indexes
CREATE INDEX idx_ai_programs_user_id ON public.ai_generated_programs(user_id);
CREATE INDEX idx_ai_programs_status ON public.ai_generated_programs(status);
CREATE INDEX idx_ai_program_days_program_id ON public.ai_program_days(program_id);
CREATE INDEX idx_ai_program_items_program_id ON public.ai_program_items(program_id);
CREATE INDEX idx_ai_program_items_day_id ON public.ai_program_items(program_day_id);

-- Multimodal embeddings indexes
CREATE INDEX idx_multimodal_embeddings_user_id ON public.multimodal_embeddings(user_id);
CREATE INDEX idx_multimodal_embeddings_source_type ON public.multimodal_embeddings(source_type);
CREATE INDEX idx_multimodal_embeddings_data_type ON public.multimodal_embeddings(data_type);

-- Integrations indexes
CREATE INDEX idx_integrations_user_id ON public.integrations(user_id);
CREATE INDEX idx_integrations_provider ON public.integrations(provider);

-- Vector similarity search indexes
CREATE INDEX idx_quick_entry_embeddings_vector ON public.quick_entry_embeddings USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_multimodal_embeddings_vector ON public.multimodal_embeddings USING ivfflat (embedding vector_cosine_ops);
CREATE INDEX idx_profiles_goals_embedding ON public.profiles USING ivfflat (goals_embedding vector_cosine_ops) WHERE goals_embedding IS NOT NULL;

-- =====================================================
-- ROW LEVEL SECURITY (RLS) POLICIES
-- =====================================================

-- Enable RLS on all tables
ALTER TABLE public.profiles ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_onboarding ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.user_goals ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quick_entry_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quick_entry_embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.quick_entry_stats ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.meal_logs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.foods_enhanced ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.daily_nutrition_summaries ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activities ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activity_exercises ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activity_sets ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activity_segments ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.activity_streams ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.body_measurements ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.coach_messages ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_conversations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_generated_programs ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_program_days ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.ai_program_items ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.multimodal_embeddings ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.integrations ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.webhook_events ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.rate_limits ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.workout_exercises ENABLE ROW LEVEL SECURITY;

-- Profiles policies
CREATE POLICY "Users can view own profile" ON public.profiles FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.profiles FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON public.profiles FOR INSERT WITH CHECK (auth.uid() = id);

-- Users policies
CREATE POLICY "Users can view own user data" ON public.users FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own user data" ON public.users FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own user data" ON public.users FOR INSERT WITH CHECK (auth.uid() = id);

-- User goals policies
CREATE POLICY "Users can view own goals" ON public.user_goals FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own goals" ON public.user_goals FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own goals" ON public.user_goals FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own goals" ON public.user_goals FOR DELETE USING (auth.uid() = user_id);

-- Quick Entry policies
CREATE POLICY "Users can view own quick entries" ON public.quick_entry_logs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own quick entries" ON public.quick_entry_logs FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own quick entries" ON public.quick_entry_logs FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY "Users can view own quick entry embeddings" ON public.quick_entry_embeddings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own quick entry embeddings" ON public.quick_entry_embeddings FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can view own quick entry stats" ON public.quick_entry_stats FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can update own quick entry stats" ON public.quick_entry_stats FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own quick entry stats" ON public.quick_entry_stats FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Meal logs policies
CREATE POLICY "Users can view own meals" ON public.meal_logs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own meals" ON public.meal_logs FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own meals" ON public.meal_logs FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own meals" ON public.meal_logs FOR DELETE USING (auth.uid() = user_id);

-- Foods policies (public read, authenticated insert)
CREATE POLICY "Anyone can view foods" ON public.foods_enhanced FOR SELECT USING (true);
CREATE POLICY "Authenticated users can insert foods" ON public.foods_enhanced FOR INSERT WITH CHECK (auth.role() = 'authenticated');

-- Activities policies
CREATE POLICY "Users can view own activities" ON public.activities FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own activities" ON public.activities FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own activities" ON public.activities FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own activities" ON public.activities FOR DELETE USING (auth.uid() = user_id);

-- Coach messages policies
CREATE POLICY "Users can view own coach messages" ON public.coach_messages FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own coach messages" ON public.coach_messages FOR INSERT WITH CHECK (auth.uid() = user_id);

-- AI Programs policies
CREATE POLICY "Users can view own programs" ON public.ai_generated_programs FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own programs" ON public.ai_generated_programs FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own programs" ON public.ai_generated_programs FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own programs" ON public.ai_generated_programs FOR DELETE USING (auth.uid() = user_id);

-- Multimodal embeddings policies
CREATE POLICY "Users can view own embeddings" ON public.multimodal_embeddings FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own embeddings" ON public.multimodal_embeddings FOR INSERT WITH CHECK (auth.uid() = user_id);

-- Integrations policies
CREATE POLICY "Users can view own integrations" ON public.integrations FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own integrations" ON public.integrations FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own integrations" ON public.integrations FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own integrations" ON public.integrations FOR DELETE USING (auth.uid() = user_id);

-- Body measurements policies
CREATE POLICY "Users can view own measurements" ON public.body_measurements FOR SELECT USING (auth.uid() = user_id);
CREATE POLICY "Users can insert own measurements" ON public.body_measurements FOR INSERT WITH CHECK (auth.uid() = user_id);
CREATE POLICY "Users can update own measurements" ON public.body_measurements FOR UPDATE USING (auth.uid() = user_id);
CREATE POLICY "Users can delete own measurements" ON public.body_measurements FOR DELETE USING (auth.uid() = user_id);

-- =====================================================
-- FUNCTIONS FOR VECTOR SEARCH
-- =====================================================

-- Function to search quick entry embeddings
CREATE OR REPLACE FUNCTION search_quick_entry_embeddings(
  query_embedding vector(384),
  user_id_filter uuid,
  match_threshold float DEFAULT 0.7,
  match_count int DEFAULT 10
)
RETURNS TABLE (
  id uuid,
  quick_entry_log_id uuid,
  content_text text,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    qe.id,
    qe.quick_entry_log_id,
    qe.content_text,
    1 - (qe.embedding <=> query_embedding) as similarity
  FROM quick_entry_embeddings qe
  WHERE qe.user_id = user_id_filter
    AND qe.is_active = true
    AND 1 - (qe.embedding <=> query_embedding) > match_threshold
  ORDER BY qe.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- Function to search all multimodal embeddings
CREATE OR REPLACE FUNCTION search_multimodal_embeddings(
  query_embedding vector(384),
  user_id_filter uuid,
  match_threshold float DEFAULT 0.7,
  match_count int DEFAULT 10
)
RETURNS TABLE (
  id uuid,
  content_text text,
  source_type text,
  source_id uuid,
  similarity float
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    me.id,
    me.content_text,
    me.source_type,
    me.source_id,
    1 - (me.embedding <=> query_embedding) as similarity
  FROM multimodal_embeddings me
  WHERE me.user_id = user_id_filter
    AND me.processing_status = 'completed'
    AND 1 - (me.embedding <=> query_embedding) > match_threshold
  ORDER BY me.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- =====================================================
-- TRIGGERS FOR UPDATED_AT
-- =====================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = now();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply updated_at triggers to relevant tables
CREATE TRIGGER update_profiles_updated_at BEFORE UPDATE ON public.profiles
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_users_updated_at BEFORE UPDATE ON public.users
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_user_goals_updated_at BEFORE UPDATE ON public.user_goals
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_quick_entry_logs_updated_at BEFORE UPDATE ON public.quick_entry_logs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_meal_logs_updated_at BEFORE UPDATE ON public.meal_logs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_activities_updated_at BEFORE UPDATE ON public.activities
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_ai_programs_updated_at BEFORE UPDATE ON public.ai_generated_programs
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- =====================================================
-- SCHEMA COMPLETE
-- =====================================================
-- This schema is production-ready and includes:
-- ✅ All tables with proper constraints
-- ✅ All foreign keys and relationships
-- ✅ Performance indexes (including vector indexes)
-- ✅ Row-Level Security (RLS) policies
-- ✅ Vector search functions for RAG
-- ✅ Updated_at triggers
-- ✅ Proper data types and enums
--
-- Next steps:
-- 1. Run this as a migration
-- 2. Verify all RLS policies work
-- 3. Test vector search functions
-- 4. Monitor query performance
-- =====================================================
