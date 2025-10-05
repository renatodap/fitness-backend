# Actual Schema Analysis - Quick Entry Implementation

## 🎯 Current State: What EXISTS vs What's NEEDED

### ✅ **Tables That EXIST and Can Be Used:**

#### 1. **`meal_logs`** ✅ (EXISTS!)
```sql
CREATE TABLE public.meal_logs (
  id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id uuid NOT NULL REFERENCES auth.users(id),
  name text,
  category USER-DEFINED (meal_category enum),
  logged_at timestamptz DEFAULT now(),
  notes text,
  total_calories numeric DEFAULT 0,
  total_protein_g numeric DEFAULT 0,
  total_carbs_g numeric DEFAULT 0,
  total_fat_g numeric DEFAULT 0,
  total_fiber_g numeric DEFAULT 0,
  created_at timestamptz DEFAULT now(),
  updated_at timestamptz DEFAULT now()
);
```

**Missing fields needed for quick entry:**
- ❌ `foods` JSONB (array of food items)
- ❌ `source` TEXT (quick_entry vs manual)
- ❌ `estimated` BOOLEAN (was nutrition estimated by AI)
- ❌ `confidence_score` DECIMAL (AI confidence)
- ❌ `image_url` TEXT (photo of meal)
- ❌ `meal_quality_score` DECIMAL (AI enrichment)
- ❌ `macro_balance_score` DECIMAL (AI enrichment)
- ❌ `adherence_to_goals` DECIMAL (AI enrichment)
- ❌ `tags` TEXT[] (smart tags)
- ❌ `total_sugar_g` DECIMAL
- ❌ `total_sodium_mg` DECIMAL

#### 2. **`activities`** ✅ (EXISTS!)
```sql
CREATE TABLE public.activities (
  id uuid PRIMARY KEY,
  user_id uuid NOT NULL,
  source text (strava/garmin/manual/etc),
  name text NOT NULL,
  activity_type text NOT NULL,
  start_date timestamptz NOT NULL,
  elapsed_time_seconds integer NOT NULL,
  distance_meters numeric,
  calories integer,
  perceived_exertion integer (1-10),
  mood text,
  energy_level integer (1-5),
  notes text,
  ... (MANY more fields)
);
```

**Missing fields needed for quick entry:**
- ❌ `performance_score` DECIMAL (AI enrichment)
- ❌ `effort_level` DECIMAL (AI enrichment)
- ❌ `recovery_needed_hours` INTEGER (AI enrichment)
- ❌ `tags` TEXT[] (smart tags)

**Note:** This table is VERY comprehensive already!

#### 3. **`workout_completions`** ✅ (EXISTS!)
```sql
CREATE TABLE public.workout_completions (
  id integer PRIMARY KEY,
  user_id uuid,
  workout_id integer,
  started_at timestamptz,
  completed_at timestamptz,
  notes text,
  rpe integer (1-10),
  mood text,
  energy_level integer (1-5),
  workout_rating integer (1-5),
  difficulty_rating integer (1-10),
  duration_minutes integer,
  embedding vector (pgvector!)
);
```

**Missing fields needed for quick entry:**
- ❌ `exercises` JSONB (detailed exercise data)
- ❌ `volume_load` INTEGER (total weight lifted)
- ❌ `estimated_calories` INTEGER
- ❌ `muscle_groups` TEXT[]
- ❌ `progressive_overload_status` TEXT
- ❌ `recovery_needed_hours` INTEGER
- ❌ `tags` TEXT[]

#### 4. **`multimodal_embeddings`** ✅ (EXISTS!)
```sql
CREATE TABLE public.multimodal_embeddings (
  id uuid PRIMARY KEY,
  user_id uuid NOT NULL,
  data_type text ('text', 'image', 'audio', 'video', 'pdf', etc),
  content_text text,
  embedding vector NOT NULL,
  metadata jsonb DEFAULT '{}',
  source_type text (meal/workout/activity/goal/etc - VERY COMPREHENSIVE LIST),
  source_id uuid,
  storage_url text,
  storage_bucket text,
  file_name text,
  file_size_bytes bigint,
  mime_type text,
  embedding_model text DEFAULT 'all-MiniLM-L6-v2',
  embedding_dimensions integer DEFAULT 384,
  confidence_score numeric,
  processing_status text,
  created_at timestamptz,
  updated_at timestamptz
);
```

**Status:** ✅ **PERFECT!** This table is exactly what we need. No changes required.

#### 5. **`user_onboarding`** ✅ (EXISTS - Can serve as fitness profile)
```sql
CREATE TABLE public.user_onboarding (
  user_id uuid PRIMARY KEY,
  primary_goal text,
  user_persona text,
  current_activity_level text,
  desired_training_frequency integer,
  biological_sex text,
  age integer,
  current_weight_kg numeric,
  height_cm numeric,
  daily_meal_preference integer,
  experience_level text,
  ... (many more fields)
);
```

**Missing fields for nutrition targets:**
- ❌ `daily_calorie_target` INTEGER
- ❌ `daily_protein_target_g` INTEGER
- ❌ `daily_carbs_target_g` INTEGER
- ❌ `daily_fat_target_g` INTEGER
- ❌ `goal_weight_kg` DECIMAL
- ❌ `goal_body_fat_pct` DECIMAL
- ❌ `estimated_tdee` INTEGER

#### 6. **`user_goals`** ✅ (EXISTS!)
```sql
CREATE TABLE public.user_goals (
  id uuid PRIMARY KEY,
  user_id uuid NOT NULL,
  goal_type USER-DEFINED (enum),
  goal_description text NOT NULL,
  target_value numeric,
  target_unit text,
  target_date date,
  priority integer (1-5),
  status USER-DEFINED (active/completed/etc),
  progress_value numeric,
  created_at timestamptz,
  updated_at timestamptz,
  completed_at timestamptz
);
```

**Status:** ✅ Good as-is.

### ❌ **Tables That DON'T EXIST (But Needed):**

#### 1. **`body_measurements`** ❌ (MISSING)
No table exists for tracking weight, body fat, measurements.

**Solution:** Create new table.

#### 2. **`user_notes`** ❌ (MISSING)
No table exists for reflections, thoughts, feelings.

**Solution:** Create new table.

---

## 🔧 Required Schema Updates

### Migration 1: Alter `meal_logs` Table

```sql
-- Add missing columns to meal_logs
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

-- Add index for tags
CREATE INDEX IF NOT EXISTS idx_meal_logs_tags ON meal_logs USING GIN(tags);
```

### Migration 2: Alter `activities` Table

```sql
-- Add AI enrichment columns to activities
ALTER TABLE activities
  ADD COLUMN IF NOT EXISTS performance_score DECIMAL(4,2) CHECK (performance_score >= 0 AND performance_score <= 10),
  ADD COLUMN IF NOT EXISTS effort_level DECIMAL(4,2) CHECK (effort_level >= 0 AND effort_level <= 10),
  ADD COLUMN IF NOT EXISTS recovery_needed_hours INTEGER,
  ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT ARRAY[]::TEXT[];

-- Add index for tags
CREATE INDEX IF NOT EXISTS idx_activities_tags ON activities USING GIN(tags);

-- Note: 'quick_entry' should be added to source CHECK constraint
ALTER TABLE activities DROP CONSTRAINT IF EXISTS activities_source_check;
ALTER TABLE activities ADD CONSTRAINT activities_source_check
  CHECK (source IN ('strava', 'garmin', 'manual', 'apple', 'fitbit', 'polar', 'suunto', 'wahoo', 'quick_entry'));
```

### Migration 3: Alter `workout_completions` Table

```sql
-- Add AI enrichment columns to workout_completions
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
```

### Migration 4: Create `body_measurements` Table

```sql
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
  measurements JSONB,

  -- Metadata
  source TEXT DEFAULT 'manual' CHECK (source IN ('manual', 'scale', 'dexa', 'inbody', 'quick_entry')),
  notes TEXT,

  -- AI enrichment
  trend_direction TEXT CHECK (trend_direction IN ('up', 'down', 'stable')),
  rate_of_change_weekly DECIMAL(5,2),
  goal_progress_pct DECIMAL(5,2) CHECK (goal_progress_pct >= 0 AND goal_progress_pct <= 100),
  health_assessment TEXT CHECK (health_assessment IN ('healthy', 'caution', 'concern')),
  tags TEXT[] DEFAULT ARRAY[]::TEXT[],

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes
CREATE INDEX idx_body_measurements_user_time ON body_measurements(user_id, measured_at DESC);
CREATE INDEX idx_body_measurements_tags ON body_measurements USING GIN(tags);

-- RLS
ALTER TABLE body_measurements ENABLE ROW LEVEL SECURITY;

CREATE POLICY body_measurements_select ON body_measurements
  FOR SELECT USING (auth.uid() = user_id);

CREATE POLICY body_measurements_insert ON body_measurements
  FOR INSERT WITH CHECK (auth.uid() = user_id);

CREATE POLICY body_measurements_update ON body_measurements
  FOR UPDATE USING (auth.uid() = user_id);

CREATE POLICY body_measurements_delete ON body_measurements
  FOR DELETE USING (auth.uid() = user_id);
```

### Migration 5: Create `user_notes` Table

```sql
CREATE TABLE IF NOT EXISTS user_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Note content
  title TEXT,
  content TEXT NOT NULL,
  category TEXT CHECK (category IN ('reflection', 'goal', 'plan', 'observation', 'general')),
  tags TEXT[] DEFAULT ARRAY[]::TEXT[],

  -- AI enrichment
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

-- RLS
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
CREATE TRIGGER update_user_notes_updated_at
  BEFORE UPDATE ON user_notes
  FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();
```

### Migration 6: Alter `user_onboarding` for Nutrition Targets

```sql
-- Add nutrition target fields to user_onboarding
ALTER TABLE user_onboarding
  ADD COLUMN IF NOT EXISTS daily_calorie_target INTEGER,
  ADD COLUMN IF NOT EXISTS daily_protein_target_g INTEGER,
  ADD COLUMN IF NOT EXISTS daily_carbs_target_g INTEGER,
  ADD COLUMN IF NOT EXISTS daily_fat_target_g INTEGER,
  ADD COLUMN IF NOT EXISTS goal_weight_kg DECIMAL(6,2),
  ADD COLUMN IF NOT EXISTS goal_body_fat_pct DECIMAL(4,2),
  ADD COLUMN IF NOT EXISTS estimated_tdee INTEGER,
  ADD COLUMN IF NOT EXISTS goal_type TEXT CHECK (goal_type IN ('cut', 'bulk', 'maintain', 'recomp'));
```

---

## 📝 Complete Migration SQL File

I'll create a single migration file that includes all these updates.

---

## 🔄 Backend Service Updates Required

### 1. **Update `quick_entry_service.py` Save Logic**

The current implementation tries to save to tables that match our ideal schema, but needs to be updated to use the actual schema:

**Changes needed:**
- ✅ `meal_logs`: Works mostly, just add new fields
- ✅ `activities`: Works, add new fields
- ✅ `workout_completions`: Works, add new fields
- ❌ `body_measurements`: Create new table first
- ❌ `user_notes`: Create new table first

### 2. **Multimodal Embeddings Integration**

✅ **Already perfect!** The existing `multimodal_embeddings` table has:
- Vector embeddings (pgvector) ✅
- Comprehensive source_type enum (includes meal, workout, activity, quick_entry, etc.) ✅
- Rich metadata JSONB ✅
- Storage URLs for images ✅

**No changes needed** - just use it as-is.

### 3. **User Profile/Goals Integration**

Use existing tables:
- `user_onboarding` → Add nutrition targets
- `user_goals` → Already perfect
- `profiles` → Already has fitness data

---

## 💰 Cost Optimization Strategy (No Change)

Use same strategy:
- **Groq** for classification, vision, audio ($0.00013/entry)
- **OpenRouter Claude Sonnet 4** for AI recommendations ($0.0135/chat)

---

## ✅ Summary

**Good News:** Most tables already exist and are well-designed!

**Required Actions:**
1. ✅ Run migration to ADD columns to existing tables (meal_logs, activities, workout_completions)
2. ✅ Run migration to CREATE 2 new tables (body_measurements, user_notes)
3. ✅ Update `quick_entry_service.py` to use correct column names
4. ✅ Integrate Groq API for cost optimization
5. ✅ Add enrichment functions
6. ✅ Implement semantic search (table already exists!)

**Timeline:** 2-3 days (much faster than starting from scratch!)
