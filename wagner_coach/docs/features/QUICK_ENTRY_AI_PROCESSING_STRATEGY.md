# Quick Entry AI Processing Strategy - Ultra-Comprehensive Guide

## 🧠 Executive Summary

This document defines **exactly how the AI processes, structures, stores, and leverages every input type** in the quick-entry-optimized system to provide hyper-personalized fitness coaching through:

1. **Intelligent Data Structuring**: Multi-table relational database with normalized schemas
2. **Multimodal Vector Embeddings**: Text + image embeddings for semantic context retrieval
3. **Temporal Intelligence**: Time-aware patterns, trends, and recency weighting
4. **Cross-Modal Context**: Unified user profile built from all data sources
5. **Adaptive Recommendations**: Context-aware suggestions based on full user history

---

## 📊 Part 1: Database Architecture & Data Structuring

### 1.1 Core Database Tables

#### **Table: `meal_logs`**
Stores all food/nutrition entries.

```sql
CREATE TABLE meal_logs (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),

  -- CORE MEAL DATA
  name TEXT NOT NULL,                    -- "Grilled chicken with rice and broccoli"
  category TEXT NOT NULL,                -- breakfast/lunch/dinner/snack/supplement
  logged_at TIMESTAMPTZ NOT NULL,        -- When meal was consumed

  -- NUTRITION (all optional, can be estimated)
  total_calories DECIMAL,                -- 450
  total_protein_g DECIMAL,               -- 45.0
  total_carbs_g DECIMAL,                 -- 40.0
  total_fat_g DECIMAL,                   -- 8.0
  total_fiber_g DECIMAL,                 -- 6.0
  total_sugar_g DECIMAL,                 -- Optional
  total_sodium_mg DECIMAL,               -- Optional

  -- MEAL COMPOSITION (structured JSON)
  foods JSONB,                           -- [{"name": "Chicken breast", "quantity": "6 oz", "calories": 250}]

  -- METADATA
  notes TEXT,                            -- User feelings, context
  source TEXT DEFAULT 'quick_entry',     -- quick_entry/manual/imported
  estimated BOOLEAN DEFAULT false,       -- Was nutrition estimated by AI?
  confidence_score DECIMAL,              -- 0.0-1.0 AI confidence
  image_url TEXT,                        -- Supabase storage URL if photo attached

  -- CONTEXT ENRICHMENT (AI-generated)
  meal_quality_score DECIMAL,            -- 0-10, AI assessment of nutritional quality
  macro_balance_score DECIMAL,           -- 0-10, how balanced are macros
  adherence_to_goals DECIMAL,            -- 0-10, how well does this fit user's goals
  tags TEXT[],                           -- ["high-protein", "meal-prep", "restaurant"]

  -- TIMESTAMPS
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for fast retrieval
CREATE INDEX idx_meal_logs_user_time ON meal_logs(user_id, logged_at DESC);
CREATE INDEX idx_meal_logs_category ON meal_logs(user_id, category);
CREATE INDEX idx_meal_logs_tags ON meal_logs USING GIN(tags);
```

**AI Processing Logic for Meals:**

1. **Classification Phase** (during `/preview`):
   ```python
   # Extract structured data from LLM
   meal_data = {
       "type": "meal",
       "confidence": 0.95,
       "data": {
           "meal_name": "Grilled chicken with rice and broccoli",
           "meal_type": "lunch",
           "foods": [
               {"name": "Grilled chicken breast", "quantity": "6 oz"},
               {"name": "Brown rice", "quantity": "1 cup"},
               {"name": "Steamed broccoli", "quantity": "2 cups"}
           ],
           "calories": 450,
           "protein_g": 45,
           "carbs_g": 40,
           "fat_g": 8,
           "fiber_g": 6,
           "estimated": True  # AI estimated nutrition
       }
   }
   ```

2. **Enrichment Phase** (before saving):
   ```python
   # AI enriches with contextual scores
   async def enrich_meal_data(meal_data, user_profile):
       # Calculate nutritional quality
       quality_score = calculate_meal_quality(
           protein=meal_data['protein_g'],
           carbs=meal_data['carbs_g'],
           fat=meal_data['fat_g'],
           fiber=meal_data['fiber_g']
       )

       # Calculate macro balance (ideal ratios)
       macro_balance = calculate_macro_balance(
           protein_pct=meal_data['protein_g'] * 4 / meal_data['calories'],
           carb_pct=meal_data['carbs_g'] * 4 / meal_data['calories'],
           fat_pct=meal_data['fat_g'] * 9 / meal_data['calories']
       )

       # Check adherence to user goals
       adherence = calculate_goal_adherence(
           meal_calories=meal_data['calories'],
           user_daily_target=user_profile['daily_calorie_target'],
           user_macro_targets=user_profile['macro_targets']
       )

       # Generate smart tags
       tags = generate_meal_tags(meal_data)
       # ["high-protein", "low-carb", "balanced", "whole-foods"]

       return {
           **meal_data,
           "meal_quality_score": quality_score,
           "macro_balance_score": macro_balance,
           "adherence_to_goals": adherence,
           "tags": tags
       }
   ```

3. **Database Save**:
   ```python
   meal_log = {
       "user_id": user_id,
       "name": enriched_data["meal_name"],
       "category": enriched_data["meal_type"],
       "logged_at": datetime.utcnow(),
       "total_calories": enriched_data["calories"],
       "total_protein_g": enriched_data["protein_g"],
       "total_carbs_g": enriched_data["carbs_g"],
       "total_fat_g": enriched_data["fat_g"],
       "total_fiber_g": enriched_data["fiber_g"],
       "foods": enriched_data["foods"],
       "notes": enriched_data.get("notes"),
       "estimated": enriched_data["estimated"],
       "confidence_score": enriched_data["confidence"],
       "image_url": image_url if image else None,
       "meal_quality_score": enriched_data["meal_quality_score"],
       "macro_balance_score": enriched_data["macro_balance_score"],
       "adherence_to_goals": enriched_data["adherence_to_goals"],
       "tags": enriched_data["tags"]
   }

   supabase.table("meal_logs").insert(meal_log).execute()
   ```

---

#### **Table: `activities`**
Stores cardio activities (running, cycling, swimming, sports).

```sql
CREATE TABLE activities (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),

  -- CORE ACTIVITY DATA
  name TEXT NOT NULL,                    -- "Morning run"
  activity_type TEXT NOT NULL,           -- running/cycling/walking/swimming/sport
  sport_type TEXT,                       -- basketball/tennis/soccer (if sport)
  start_date TIMESTAMPTZ NOT NULL,       -- When activity started

  -- PERFORMANCE METRICS
  elapsed_time_seconds INTEGER,          -- 2700 (45 minutes)
  moving_time_seconds INTEGER,           -- Time actually moving (excludes breaks)
  distance_meters DECIMAL,               -- 7500.0 (7.5km)
  elevation_gain_meters DECIMAL,         -- Optional

  -- INTENSITY
  average_heart_rate INTEGER,            -- BPM
  max_heart_rate INTEGER,                -- BPM
  calories INTEGER,                      -- Estimated calories burned
  perceived_exertion INTEGER,            -- RPE 1-10

  -- SUBJECTIVE
  mood TEXT,                             -- great/good/okay/poor
  energy_level TEXT,                     -- high/medium/low
  notes TEXT,                            -- User reflections

  -- METADATA
  source TEXT DEFAULT 'manual',          -- manual/strava/garmin/apple_health
  weather JSONB,                         -- {"temp": 65, "condition": "sunny"}

  -- CONTEXT ENRICHMENT (AI-generated)
  performance_score DECIMAL,             -- 0-10, how well did they perform
  effort_level DECIMAL,                  -- 0-10, intensity assessment
  recovery_needed_hours INTEGER,         -- AI estimate of recovery time
  tags TEXT[],                           -- ["tempo-run", "race-pace", "easy-recovery"]

  -- TIMESTAMPS
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_activities_user_time ON activities(user_id, start_date DESC);
CREATE INDEX idx_activities_type ON activities(user_id, activity_type);
```

**AI Processing Logic for Activities:**

1. **Classification**:
   ```python
   activity_data = {
       "type": "activity",
       "confidence": 0.92,
       "data": {
           "activity_name": "Morning run",
           "activity_type": "running",
           "duration_minutes": 45,
           "distance_km": 7.5,
           "pace": "6:00/km",
           "calories_burned": 550,
           "rpe": 7,
           "mood": "great",
           "notes": "Felt strong, cool weather"
       }
   }
   ```

2. **Enrichment**:
   ```python
   async def enrich_activity_data(activity_data, user_profile):
       # Calculate performance score
       # Compare pace/distance to user's historical data
       historical_runs = await get_similar_activities(
           user_id=user_profile['id'],
           activity_type='running',
           limit=20
       )

       avg_pace_history = calculate_avg_pace(historical_runs)
       current_pace = activity_data['pace']

       performance_score = calculate_performance_score(
           current_pace=current_pace,
           avg_pace=avg_pace_history,
           distance=activity_data['distance_km']
       )

       # Estimate effort level from RPE, duration, distance
       effort_level = calculate_effort_level(
           rpe=activity_data['rpe'],
           duration=activity_data['duration_minutes'],
           distance=activity_data['distance_km']
       )

       # Calculate recovery needed based on effort and duration
       recovery_hours = estimate_recovery_time(
           effort_level=effort_level,
           duration=activity_data['duration_minutes'],
           user_fitness_level=user_profile['estimated_fitness_level']
       )

       # Generate contextual tags
       tags = generate_activity_tags(activity_data, performance_score)
       # ["tempo-run", "above-average-pace", "moderate-effort"]

       return {
           **activity_data,
           "performance_score": performance_score,
           "effort_level": effort_level,
           "recovery_needed_hours": recovery_hours,
           "tags": tags
       }
   ```

3. **Save with calculated fields**:
   ```python
   activity_log = {
       "user_id": user_id,
       "name": enriched["activity_name"],
       "activity_type": enriched["activity_type"],
       "start_date": datetime.utcnow(),
       "elapsed_time_seconds": enriched["duration_minutes"] * 60,
       "moving_time_seconds": enriched["duration_minutes"] * 60,
       "distance_meters": enriched["distance_km"] * 1000,
       "calories": enriched["calories_burned"],
       "perceived_exertion": enriched["rpe"],
       "mood": enriched["mood"],
       "energy_level": enriched.get("energy_level"),
       "notes": enriched["notes"],
       "performance_score": enriched["performance_score"],
       "effort_level": enriched["effort_level"],
       "recovery_needed_hours": enriched["recovery_needed_hours"],
       "tags": enriched["tags"]
   }
   ```

---

#### **Table: `workout_completions`**
Stores strength training workouts.

```sql
CREATE TABLE workout_completions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  workout_template_id UUID REFERENCES workout_templates(id), -- If following program

  -- CORE WORKOUT DATA
  workout_name TEXT,                     -- "Upper Body Push" or template name
  started_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ NOT NULL,
  duration_minutes INTEGER,

  -- EXERCISES PERFORMED (detailed JSON)
  exercises JSONB,                       -- [{"name": "Bench Press", "sets": [...]}]

  -- SUBJECTIVE ASSESSMENT
  rpe INTEGER,                           -- 1-10 overall session RPE
  mood TEXT,                             -- great/good/okay/poor
  energy_level TEXT,                     -- high/medium/low
  workout_rating INTEGER,                -- 1-10, how good was the workout
  difficulty_rating INTEGER,             -- 1-10, how hard was it
  notes TEXT,

  -- CONTEXT ENRICHMENT (AI-generated)
  volume_load INTEGER,                   -- Total weight lifted (sets × reps × weight)
  estimated_calories INTEGER,            -- Calories burned estimate
  muscle_groups TEXT[],                  -- ["chest", "shoulders", "triceps"]
  progressive_overload_status TEXT,      -- improving/maintaining/declining
  recovery_needed_hours INTEGER,
  tags TEXT[],

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_workouts_user_time ON workout_completions(user_id, started_at DESC);
```

**Exercise Sets Schema (JSONB)**:
```json
{
  "exercises": [
    {
      "name": "Bench Press",
      "exercise_id": "uuid-if-from-library",
      "sets": [
        {
          "set_number": 1,
          "reps": 8,
          "weight_lbs": 185,
          "rpe": 7,
          "completed": true,
          "notes": "Felt strong"
        },
        {
          "set_number": 2,
          "reps": 8,
          "weight_lbs": 185,
          "rpe": 8,
          "completed": true
        }
      ],
      "total_volume": 2960  // 2 sets × 8 reps × 185 lbs
    }
  ]
}
```

**AI Processing Logic for Workouts:**

1. **Classification**:
   ```python
   workout_data = {
       "type": "workout",
       "confidence": 0.94,
       "data": {
           "workout_name": "Upper Body Push",
           "workout_type": "strength",
           "exercises": [
               {
                   "name": "Bench Press",
                   "sets": 4,
                   "reps": "8",
                   "weight_lbs": 185
               },
               {
                   "name": "Shoulder Press",
                   "sets": 3,
                   "reps": "10",
                   "weight_lbs": 95
               }
           ],
           "duration_minutes": 75,
           "rpe": 8,
           "notes": "New PR on bench!"
       }
   }
   ```

2. **Enrichment with Progressive Overload Analysis**:
   ```python
   async def enrich_workout_data(workout_data, user_profile):
       # Calculate total volume load
       volume_load = 0
       muscle_groups = set()

       for exercise in workout_data['exercises']:
           sets = exercise['sets']
           reps = parse_reps(exercise['reps'])  # Handle "8-10" → avg 9
           weight = exercise['weight_lbs']

           exercise_volume = sets * reps * weight
           volume_load += exercise_volume

           # Map exercise to muscle groups
           muscles = get_muscle_groups_for_exercise(exercise['name'])
           muscle_groups.update(muscles)

       # Compare to previous similar workouts (progressive overload check)
       similar_workouts = await get_similar_workouts(
           user_id=user_profile['id'],
           workout_name=workout_data['workout_name'],
           limit=5
       )

       overload_status = analyze_progressive_overload(
           current_volume=volume_load,
           historical_volumes=[w['volume_load'] for w in similar_workouts]
       )
       # Returns: "improving", "maintaining", or "declining"

       # Estimate calories burned
       calories = estimate_strength_training_calories(
           duration_minutes=workout_data['duration_minutes'],
           volume_load=volume_load,
           user_weight_lbs=user_profile['weight_lbs']
       )

       # Estimate recovery needed
       recovery_hours = estimate_workout_recovery(
           volume_load=volume_load,
           rpe=workout_data['rpe'],
           muscle_groups=list(muscle_groups),
           user_recovery_rate=user_profile.get('recovery_rate', 'medium')
       )

       # Generate tags
       tags = generate_workout_tags(
           workout_data=workout_data,
           overload_status=overload_status,
           muscle_groups=muscle_groups
       )
       # ["push-day", "progressive-overload", "high-volume", "upper-body"]

       return {
           **workout_data,
           "volume_load": volume_load,
           "estimated_calories": calories,
           "muscle_groups": list(muscle_groups),
           "progressive_overload_status": overload_status,
           "recovery_needed_hours": recovery_hours,
           "tags": tags
       }
   ```

3. **Save with structured exercise data**:
   ```python
   # Transform exercises into detailed JSONB structure
   exercises_jsonb = []
   for ex in enriched['exercises']:
       # Expand sets into detailed structure
       sets_data = []
       for set_num in range(1, ex['sets'] + 1):
           sets_data.append({
               "set_number": set_num,
               "reps": ex['reps'],
               "weight_lbs": ex['weight_lbs'],
               "completed": True
           })

       exercises_jsonb.append({
           "name": ex['name'],
           "sets": sets_data,
           "total_volume": ex['sets'] * parse_reps(ex['reps']) * ex['weight_lbs']
       })

   workout_log = {
       "user_id": user_id,
       "workout_name": enriched["workout_name"],
       "started_at": datetime.utcnow(),
       "completed_at": datetime.utcnow(),
       "duration_minutes": enriched["duration_minutes"],
       "exercises": exercises_jsonb,
       "rpe": enriched["rpe"],
       "notes": enriched["notes"],
       "volume_load": enriched["volume_load"],
       "estimated_calories": enriched["estimated_calories"],
       "muscle_groups": enriched["muscle_groups"],
       "progressive_overload_status": enriched["progressive_overload_status"],
       "recovery_needed_hours": enriched["recovery_needed_hours"],
       "tags": enriched["tags"]
   }
   ```

---

#### **Table: `body_measurements`**
Stores weight, body composition, and measurements.

```sql
CREATE TABLE body_measurements (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),

  -- MEASUREMENTS
  measured_at TIMESTAMPTZ NOT NULL,
  weight_lbs DECIMAL,
  body_fat_pct DECIMAL,
  muscle_mass_lbs DECIMAL,

  -- DETAILED MEASUREMENTS (JSONB)
  measurements JSONB,                    -- {"chest_in": 42, "waist_in": 32, ...}

  -- METADATA
  source TEXT DEFAULT 'manual',          -- manual/scale/dexa/inbody
  notes TEXT,

  -- CONTEXT ENRICHMENT (AI-generated)
  trend_direction TEXT,                  -- up/down/stable
  rate_of_change_weekly DECIMAL,         -- +0.5 lbs/week
  goal_progress_pct DECIMAL,             -- 0-100%, progress toward user goal
  health_assessment TEXT,                -- healthy/caution/concern
  tags TEXT[],

  created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_measurements_user_time ON body_measurements(user_id, measured_at DESC);
```

**AI Processing Logic for Measurements:**

1. **Enrichment with Trend Analysis**:
   ```python
   async def enrich_measurement_data(measurement_data, user_profile):
       # Get historical measurements
       history = await get_measurement_history(
           user_id=user_profile['id'],
           days_back=30,
           measurement_type='weight'
       )

       # Calculate trend
       trend = calculate_trend_direction(
           current=measurement_data['weight_lbs'],
           history=[m['weight_lbs'] for m in history]
       )
       # Returns: "up", "down", or "stable"

       # Calculate rate of change
       rate_weekly = calculate_weekly_change_rate(
           current=measurement_data['weight_lbs'],
           history=history
       )
       # Returns: +0.5 (gaining 0.5 lbs/week)

       # Calculate progress toward goal
       user_goal_weight = user_profile.get('goal_weight_lbs')
       starting_weight = user_profile.get('starting_weight_lbs')

       if user_goal_weight and starting_weight:
           goal_progress = calculate_goal_progress(
               current=measurement_data['weight_lbs'],
               starting=starting_weight,
               goal=user_goal_weight
           )
       else:
           goal_progress = None

       # Health assessment based on rate of change
       health_status = assess_health_status(
           rate_weekly=rate_weekly,
           body_fat_pct=measurement_data.get('body_fat_pct'),
           user_goal_type=user_profile.get('goal_type')  # cut/bulk/maintain
       )
       # Returns: "healthy", "caution" (too fast), "concern" (unhealthy)

       tags = generate_measurement_tags(
           trend=trend,
           goal_progress=goal_progress,
           health_status=health_status
       )

       return {
           **measurement_data,
           "trend_direction": trend,
           "rate_of_change_weekly": rate_weekly,
           "goal_progress_pct": goal_progress,
           "health_assessment": health_status,
           "tags": tags
       }
   ```

---

#### **Table: `user_notes`**
Stores general notes, reflections, goals, thoughts.

```sql
CREATE TABLE user_notes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),

  -- NOTE CONTENT
  title TEXT,
  content TEXT NOT NULL,
  category TEXT,                         -- reflection/goal/plan/observation
  tags TEXT[],

  -- CONTEXT ENRICHMENT (AI-generated)
  sentiment TEXT,                        -- positive/neutral/negative
  sentiment_score DECIMAL,               -- -1.0 to +1.0
  detected_themes TEXT[],                -- ["motivation", "struggle", "success"]
  related_goals TEXT[],                  -- Goals mentioned in note
  action_items TEXT[],                   -- AI-extracted action items

  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_notes_user_time ON user_notes(user_id, created_at DESC);
CREATE INDEX idx_notes_category ON user_notes(user_id, category);
```

**AI Processing Logic for Notes:**

1. **Sentiment & Theme Analysis**:
   ```python
   async def enrich_note_data(note_data, user_profile):
       # Sentiment analysis
       sentiment_result = analyze_sentiment(note_data['content'])
       # Returns: {"sentiment": "positive", "score": 0.75}

       # Theme detection using LLM
       themes = await detect_themes(
           content=note_data['content'],
           user_context=user_profile
       )
       # Returns: ["motivation", "progress", "energy"]

       # Extract mentioned goals
       goals = await extract_goals(note_data['content'])
       # Returns: ["bench 225", "lose 10 lbs"]

       # Extract action items
       action_items = await extract_action_items(note_data['content'])
       # Returns: ["start meal prep", "sleep 8 hours"]

       return {
           **note_data,
           "sentiment": sentiment_result['sentiment'],
           "sentiment_score": sentiment_result['score'],
           "detected_themes": themes,
           "related_goals": goals,
           "action_items": action_items
       }
   ```

---

## 🔥 Part 2: Vector Embedding Strategy for RAG

### 2.1 The Multimodal Embeddings Table

**Core insight:** Every entry gets vectorized and stored in a unified embeddings table for semantic search across ALL user data.

```sql
CREATE TABLE multimodal_embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),

  -- EMBEDDING VECTOR
  embedding VECTOR(384),                 -- sentence-transformers embedding

  -- SOURCE TRACKING
  data_type TEXT NOT NULL,               -- text/image/multimodal
  source_type TEXT NOT NULL,             -- meal/activity/workout/voice_note/progress_photo
  source_id UUID NOT NULL,               -- ID from source table (meal_logs.id, etc.)

  -- CONTENT
  content_text TEXT,                     -- Full text content for retrieval
  content_summary TEXT,                  -- AI-generated summary for display

  -- METADATA (rich contextual information)
  metadata JSONB NOT NULL,               -- All contextual data

  -- TEMPORAL
  logged_at TIMESTAMPTZ NOT NULL,        -- When event occurred

  -- IMAGE STORAGE (if applicable)
  storage_url TEXT,
  storage_bucket TEXT,
  file_name TEXT,

  -- QUALITY METRICS
  confidence_score DECIMAL,              -- AI confidence in extraction
  embedding_model TEXT,                  -- Model used for embedding

  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Critical indexes for fast vector similarity search
CREATE INDEX idx_embeddings_user ON multimodal_embeddings(user_id);
CREATE INDEX idx_embeddings_source ON multimodal_embeddings(user_id, source_type);
CREATE INDEX idx_embeddings_time ON multimodal_embeddings(user_id, logged_at DESC);

-- Vector similarity search index (pgvector extension)
CREATE INDEX idx_embeddings_vector ON multimodal_embeddings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
```

### 2.2 Embedding Generation Strategy

#### **Text Embeddings** (all text-based entries)

```python
from sentence_transformers import SentenceTransformer

# FREE local model - ultra-fast, 384 dimensions
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

async def generate_text_embedding(text_content: str, metadata: dict):
    """
    Generate embedding for text-based entry.

    Creates a RICH text representation that includes:
    - The actual content
    - Contextual metadata
    - Temporal information
    - User intent
    """

    # Build comprehensive text for embedding
    # This creates a semantically rich representation
    embedding_text = build_embedding_text(text_content, metadata)

    # Example embedding text for a meal:
    # """
    # Meal: Grilled chicken with rice and broccoli
    # Type: Lunch
    # Nutrition: 450 calories, 45g protein, 40g carbs, 8g fat
    # Quality: High protein, balanced macros, whole foods
    # User feeling: Satisfied, energized
    # Context: Meal prep, healthy choice, aligned with goals
    # """

    # Generate embedding
    embedding = embedding_model.encode(embedding_text)

    return embedding.tolist()


def build_embedding_text(content: str, metadata: dict) -> str:
    """
    Build rich text representation for embedding.

    Includes:
    - Primary content
    - Structured metadata
    - Contextual tags
    - User sentiment
    - Performance indicators
    """

    if metadata['entry_type'] == 'meal':
        return f"""
        Meal: {metadata.get('meal_name', content)}
        Category: {metadata.get('meal_type', 'unknown')}
        Nutrition: {metadata.get('calories')}cal, {metadata.get('protein_g')}g protein, {metadata.get('carbs_g')}g carbs, {metadata.get('fat_g')}g fat
        Quality Score: {metadata.get('meal_quality_score')}/10
        Macro Balance: {metadata.get('macro_balance_score')}/10
        Goal Adherence: {metadata.get('adherence_to_goals')}/10
        Tags: {', '.join(metadata.get('tags', []))}
        Notes: {metadata.get('notes', '')}
        Time: {metadata.get('logged_at')}
        """.strip()

    elif metadata['entry_type'] == 'activity':
        return f"""
        Activity: {metadata.get('activity_name', content)}
        Type: {metadata.get('activity_type')}
        Duration: {metadata.get('duration_minutes')} minutes
        Distance: {metadata.get('distance_km')} km
        Pace: {metadata.get('pace')}
        Effort: RPE {metadata.get('rpe')}/10
        Calories Burned: {metadata.get('calories_burned')}
        Performance Score: {metadata.get('performance_score')}/10
        Mood: {metadata.get('mood')}
        Tags: {', '.join(metadata.get('tags', []))}
        Notes: {metadata.get('notes', '')}
        Time: {metadata.get('logged_at')}
        """.strip()

    elif metadata['entry_type'] == 'workout':
        exercises_str = '\n'.join([
            f"- {ex['name']}: {ex.get('sets')}x{ex.get('reps')} @ {ex.get('weight_lbs')}lbs"
            for ex in metadata.get('exercises', [])
        ])

        return f"""
        Workout: {metadata.get('workout_name', content)}
        Type: {metadata.get('workout_type')}
        Duration: {metadata.get('duration_minutes')} minutes
        Exercises:
        {exercises_str}
        Volume Load: {metadata.get('volume_load')} lbs
        Muscle Groups: {', '.join(metadata.get('muscle_groups', []))}
        Progressive Overload: {metadata.get('progressive_overload_status')}
        Effort: RPE {metadata.get('rpe')}/10
        Tags: {', '.join(metadata.get('tags', []))}
        Notes: {metadata.get('notes', '')}
        Time: {metadata.get('logged_at')}
        """.strip()

    elif metadata['entry_type'] == 'measurement':
        return f"""
        Measurement Update
        Weight: {metadata.get('weight_lbs')} lbs
        Body Fat: {metadata.get('body_fat_pct')}%
        Trend: {metadata.get('trend_direction')}
        Rate of Change: {metadata.get('rate_of_change_weekly')} lbs/week
        Goal Progress: {metadata.get('goal_progress_pct')}%
        Health Status: {metadata.get('health_assessment')}
        Notes: {metadata.get('notes', '')}
        Time: {metadata.get('logged_at')}
        """.strip()

    elif metadata['entry_type'] == 'note':
        return f"""
        Note: {metadata.get('title', '')}
        Content: {content}
        Category: {metadata.get('category')}
        Sentiment: {metadata.get('sentiment')} ({metadata.get('sentiment_score')})
        Themes: {', '.join(metadata.get('detected_themes', []))}
        Related Goals: {', '.join(metadata.get('related_goals', []))}
        Action Items: {', '.join(metadata.get('action_items', []))}
        Time: {metadata.get('created_at')}
        """.strip()

    else:
        # Fallback for unknown types
        return f"{content}\n\nMetadata: {str(metadata)}"
```

#### **Image Embeddings** (meal photos, progress photos)

```python
from transformers import CLIPProcessor, CLIPModel
import torch

# FREE CLIP model for image embeddings
clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

async def generate_image_embedding(image_base64: str, metadata: dict):
    """
    Generate CLIP embedding for images.

    Enables:
    - Semantic image search
    - Similar meal photo retrieval
    - Progress photo comparisons
    - Visual pattern recognition
    """

    # Decode base64 to PIL Image
    import base64
    from PIL import Image
    from io import BytesIO

    image_bytes = base64.b64decode(image_base64)
    image = Image.open(BytesIO(image_bytes))

    # Process image with CLIP
    inputs = clip_processor(images=image, return_tensors="pt")

    # Generate embedding
    with torch.no_grad():
        image_features = clip_model.get_image_features(**inputs)

    # Normalize and convert to list
    embedding = image_features / image_features.norm(dim=-1, keepdim=True)

    return embedding[0].tolist()
```

#### **Multimodal Embeddings** (text + image combined)

```python
async def generate_multimodal_embedding(
    text: str,
    image_base64: Optional[str],
    metadata: dict
):
    """
    Combine text and image embeddings for richer semantic search.

    Strategy: Weighted average of text + image embeddings
    """

    if image_base64:
        # Generate both embeddings
        text_emb = await generate_text_embedding(text, metadata)
        image_emb = await generate_image_embedding(image_base64, metadata)

        # Combine with weighted average (70% text, 30% image)
        # Text typically more important for retrieval
        combined = [
            0.7 * t + 0.3 * i
            for t, i in zip(text_emb, image_emb)
        ]

        return combined
    else:
        # Text only
        return await generate_text_embedding(text, metadata)
```

### 2.3 Metadata Schema for Embeddings

**Critical:** The `metadata` JSONB field stores ALL contextual information needed for retrieval.

```python
# Example metadata for a MEAL embedding
meal_embedding_metadata = {
    # CLASSIFICATION
    "entry_type": "meal",
    "source": "quick_entry",
    "source_id": "uuid-of-meal-log",

    # TEMPORAL
    "logged_at": "2025-10-05T12:30:00Z",
    "meal_type": "lunch",
    "day_of_week": "Saturday",
    "time_of_day": "afternoon",

    # NUTRITION
    "calories": 450,
    "protein_g": 45,
    "carbs_g": 40,
    "fat_g": 8,
    "fiber_g": 6,
    "meal_name": "Grilled chicken with rice and broccoli",
    "foods": ["chicken breast", "brown rice", "broccoli"],

    # QUALITY METRICS
    "meal_quality_score": 9.2,
    "macro_balance_score": 8.5,
    "adherence_to_goals": 9.0,
    "estimated": False,

    # CONTEXT
    "tags": ["high-protein", "meal-prep", "whole-foods", "balanced"],
    "notes": "Felt satisfied and energized after",

    # USER STATE (enriched from other data)
    "user_energy_level": "high",
    "user_mood": "great",
    "training_day": True,  # Had workout earlier
    "goal_alignment": "excellent",

    # EMBEDDINGS
    "has_image": False,
    "confidence_score": 0.95
}

# Example metadata for an ACTIVITY embedding
activity_embedding_metadata = {
    "entry_type": "activity",
    "source": "quick_entry",
    "source_id": "uuid-of-activity",

    # TEMPORAL
    "logged_at": "2025-10-05T07:00:00Z",
    "day_of_week": "Saturday",
    "time_of_day": "morning",

    # ACTIVITY DETAILS
    "activity_name": "Morning run",
    "activity_type": "running",
    "duration_minutes": 45,
    "distance_km": 7.5,
    "pace": "6:00/km",
    "calories_burned": 550,

    # INTENSITY
    "rpe": 7,
    "effort_level": 7.5,
    "performance_score": 8.2,

    # SUBJECTIVE
    "mood": "great",
    "energy_level": "high",
    "notes": "Felt strong, cool weather",

    # CONTEXT
    "tags": ["tempo-run", "above-average-pace", "moderate-effort"],
    "recovery_needed_hours": 24,
    "weather": {"temp": 65, "condition": "sunny"},

    # PATTERNS
    "is_improvement": True,  # Better than recent runs
    "consistency_streak": 5,  # 5 runs this week

    "confidence_score": 0.92
}

# Example metadata for a WORKOUT embedding
workout_embedding_metadata = {
    "entry_type": "workout",
    "source": "quick_entry",
    "source_id": "uuid-of-workout",

    # TEMPORAL
    "logged_at": "2025-10-05T18:00:00Z",
    "day_of_week": "Saturday",
    "time_of_day": "evening",

    # WORKOUT DETAILS
    "workout_name": "Upper Body Push",
    "workout_type": "strength",
    "duration_minutes": 75,
    "exercises": [
        {"name": "Bench Press", "sets": 4, "reps": 8, "weight_lbs": 185},
        {"name": "Shoulder Press", "sets": 3, "reps": 10, "weight_lbs": 95}
    ],

    # PERFORMANCE
    "volume_load": 4340,  # Total lbs lifted
    "progressive_overload_status": "improving",
    "muscle_groups": ["chest", "shoulders", "triceps"],

    # INTENSITY
    "rpe": 8,
    "workout_rating": 9,
    "difficulty_rating": 8,

    # CONTEXT
    "tags": ["push-day", "progressive-overload", "high-volume", "upper-body"],
    "notes": "New PR on bench!",
    "recovery_needed_hours": 48,

    # ACHIEVEMENTS
    "personal_records": ["Bench Press: 185lbs x 8 reps"],
    "is_pr": True,

    "confidence_score": 0.94
}
```

### 2.4 Storing Embeddings in Database

```python
async def store_embedding(
    user_id: str,
    embedding: List[float],
    data_type: str,
    source_type: str,
    source_id: str,
    content_text: str,
    metadata: dict,
    **kwargs
):
    """
    Store embedding in multimodal_embeddings table.

    This is the CORE of the RAG system - every entry gets vectorized.
    """

    # Generate AI summary for quick display
    content_summary = await generate_summary(content_text, metadata)
    # "Lunch: Chicken with rice (450cal, 45g protein) - High quality meal"

    embedding_record = {
        "user_id": user_id,
        "embedding": embedding,  # pgvector handles this
        "data_type": data_type,
        "source_type": source_type,
        "source_id": source_id,
        "content_text": content_text,
        "content_summary": content_summary,
        "metadata": metadata,  # JSONB - stores everything
        "logged_at": metadata.get('logged_at', datetime.utcnow()),
        "confidence_score": kwargs.get('confidence_score', 0.9),
        "embedding_model": kwargs.get('embedding_model', 'all-MiniLM-L6-v2'),
        "storage_url": kwargs.get('storage_url'),
        "storage_bucket": kwargs.get('storage_bucket'),
        "file_name": kwargs.get('file_name')
    }

    result = supabase.table("multimodal_embeddings").insert(embedding_record).execute()

    logger.info(f"✅ Stored embedding: {source_type} ({source_id})")

    return result.data[0]['id']
```

---

## 🎯 Part 3: Context Retrieval for AI Recommendations

### 3.1 Semantic Search Functions

**Core capability:** Find relevant user history based on semantic similarity, not just keywords.

```python
async def semantic_search(
    user_id: str,
    query: str,
    filters: Optional[dict] = None,
    limit: int = 10,
    recency_weight: float = 0.3
) -> List[dict]:
    """
    Search user's history using vector similarity.

    Args:
        user_id: User ID
        query: Natural language query
        filters: Optional filters (source_type, date range, tags)
        limit: Max results
        recency_weight: Weight for recency (0-1, higher = prefer recent)

    Returns:
        List of relevant entries with similarity scores
    """

    # Generate embedding for query
    query_embedding = await generate_text_embedding(query, {})

    # Build SQL with vector similarity + filters
    sql_query = """
    SELECT
        id,
        source_type,
        source_id,
        content_summary,
        metadata,
        logged_at,
        1 - (embedding <=> $1) AS similarity,

        -- Recency score (exponential decay)
        EXP(-EXTRACT(EPOCH FROM (NOW() - logged_at)) / (86400 * 30)) AS recency_score,

        -- Combined score
        (1 - recency_weight) * (1 - (embedding <=> $1)) +
        recency_weight * EXP(-EXTRACT(EPOCH FROM (NOW() - logged_at)) / (86400 * 30)) AS final_score

    FROM multimodal_embeddings
    WHERE user_id = $2
    """

    # Add optional filters
    params = [query_embedding, user_id]
    param_count = 2

    if filters:
        if 'source_type' in filters:
            param_count += 1
            sql_query += f" AND source_type = ${param_count}"
            params.append(filters['source_type'])

        if 'date_range' in filters:
            param_count += 1
            sql_query += f" AND logged_at >= ${param_count}"
            params.append(filters['date_range']['start'])

            param_count += 1
            sql_query += f" AND logged_at <= ${param_count}"
            params.append(filters['date_range']['end'])

        if 'tags' in filters:
            # JSONB array contains check
            sql_query += f" AND metadata @> '{{\"tags\": {json.dumps(filters['tags'])}}}'"

    sql_query += f"""
    ORDER BY final_score DESC
    LIMIT {limit}
    """

    # Execute query
    results = await supabase.rpc('execute_query', {
        'query': sql_query,
        'params': params
    }).execute()

    return results.data
```

### 3.2 Context Building for AI Coach

**When a user asks the AI coach a question, we build RICH context from their history.**

```python
async def build_ai_context(
    user_id: str,
    user_query: str,
    context_type: str = 'general'
) -> dict:
    """
    Build comprehensive context for AI coach based on user query.

    Context types:
    - general: Mixed context from all sources
    - nutrition: Focus on meals and nutrition patterns
    - training: Focus on workouts and activities
    - progress: Focus on measurements and achievements
    """

    # 1. Get user profile summary
    user_profile = await get_user_profile_summary(user_id)

    # 2. Semantic search for relevant history
    relevant_entries = await semantic_search(
        user_id=user_id,
        query=user_query,
        limit=20,
        recency_weight=0.4  # Prefer recent but not exclusively
    )

    # 3. Get recent summary stats
    recent_stats = await get_recent_stats(user_id, days=7)

    # 4. Get active goals and streaks
    goals = await get_active_goals(user_id)
    streaks = await get_consistency_streaks(user_id)

    # 5. Build context object
    context = {
        "user_profile": user_profile,
        "relevant_history": relevant_entries,
        "recent_stats": recent_stats,
        "goals": goals,
        "streaks": streaks,
        "context_type": context_type
    }

    return context


async def get_user_profile_summary(user_id: str) -> dict:
    """
    Get comprehensive user profile summary.
    """

    # Current stats
    latest_weight = await get_latest_measurement(user_id, 'weight')
    latest_body_fat = await get_latest_measurement(user_id, 'body_fat')

    # Goals
    goal_weight = await get_user_goal(user_id, 'weight')
    goal_type = await get_user_goal(user_id, 'type')  # cut/bulk/maintain

    # Activity levels
    weekly_workout_count = await count_recent_entries(user_id, 'workout', days=7)
    weekly_cardio_count = await count_recent_entries(user_id, 'activity', days=7)

    # Nutrition adherence
    avg_daily_calories = await get_avg_nutrition(user_id, 'calories', days=7)
    avg_daily_protein = await get_avg_nutrition(user_id, 'protein', days=7)

    return {
        "current_weight_lbs": latest_weight,
        "current_body_fat_pct": latest_body_fat,
        "goal_weight_lbs": goal_weight,
        "goal_type": goal_type,
        "weekly_workouts": weekly_workout_count,
        "weekly_cardio": weekly_cardio_count,
        "avg_daily_calories": avg_daily_calories,
        "avg_daily_protein": avg_daily_protein
    }


async def get_recent_stats(user_id: str, days: int = 7) -> dict:
    """
    Get summary statistics for recent period.
    """

    since_date = datetime.utcnow() - timedelta(days=days)

    # Meals
    meals = await supabase.table("meal_logs").select("*").eq("user_id", user_id).gte("logged_at", since_date).execute()

    total_calories = sum(m['total_calories'] or 0 for m in meals.data)
    total_protein = sum(m['total_protein_g'] or 0 for m in meals.data)
    avg_meal_quality = sum(m['meal_quality_score'] or 0 for m in meals.data) / len(meals.data) if meals.data else 0

    # Workouts
    workouts = await supabase.table("workout_completions").select("*").eq("user_id", user_id).gte("started_at", since_date).execute()

    total_volume = sum(w['volume_load'] or 0 for w in workouts.data)
    progressive_overload_count = sum(1 for w in workouts.data if w.get('progressive_overload_status') == 'improving')

    # Activities
    activities = await supabase.table("activities").select("*").eq("user_id", user_id).gte("start_date", since_date).execute()

    total_cardio_minutes = sum(a['elapsed_time_seconds'] or 0 for a in activities.data) / 60
    total_distance_km = sum(a['distance_meters'] or 0 for a in activities.data) / 1000

    return {
        "period_days": days,
        "total_calories": total_calories,
        "avg_daily_calories": total_calories / days,
        "total_protein_g": total_protein,
        "avg_daily_protein": total_protein / days,
        "avg_meal_quality": avg_meal_quality,
        "workout_count": len(workouts.data),
        "progressive_overload_percentage": (progressive_overload_count / len(workouts.data) * 100) if workouts.data else 0,
        "total_training_volume_lbs": total_volume,
        "cardio_sessions": len(activities.data),
        "total_cardio_minutes": total_cardio_minutes,
        "total_distance_km": total_distance_km
    }
```

### 3.3 AI Recommendation Generation

**Use retrieved context to generate hyper-personalized recommendations.**

```python
async def generate_recommendation(
    user_id: str,
    user_query: str,
    recommendation_type: str = 'general'
) -> str:
    """
    Generate AI recommendation based on user query and full context.

    Recommendation types:
    - general: Mixed advice
    - meal_suggestion: What to eat
    - workout_suggestion: What to train
    - recovery_advice: Rest and recovery
    - progress_analysis: Progress assessment
    """

    # Build comprehensive context
    context = await build_ai_context(user_id, user_query, recommendation_type)

    # Build system prompt with context
    system_prompt = build_coach_system_prompt(context)

    # Build user prompt
    user_prompt = f"""
    User Question: {user_query}

    Based on my complete history and current situation, provide personalized advice.
    """

    # Call LLM with rich context
    response = await dual_router.complete(
        config=TaskConfig(
            type=TaskType.LONG_CONTEXT,
            prioritize_accuracy=True
        ),
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        temperature=0.7
    )

    return response.choices[0].message.content


def build_coach_system_prompt(context: dict) -> str:
    """
    Build comprehensive system prompt with user context.
    """

    profile = context['user_profile']
    stats = context['recent_stats']
    relevant = context['relevant_history']

    # Extract relevant history summaries
    history_summaries = '\n'.join([
        f"- {entry['content_summary']} (similarity: {entry['similarity']:.2f})"
        for entry in relevant[:10]
    ])

    system_prompt = f"""You are an expert fitness coach providing personalized advice.

USER PROFILE:
- Current Weight: {profile['current_weight_lbs']} lbs
- Body Fat: {profile['current_body_fat_pct']}%
- Goal: {profile['goal_type']} to {profile['goal_weight_lbs']} lbs
- Training Frequency: {profile['weekly_workouts']} workouts/week, {profile['weekly_cardio']} cardio sessions/week
- Nutrition: Averaging {profile['avg_daily_calories']:.0f} cal/day, {profile['avg_daily_protein']:.0f}g protein/day

RECENT ACTIVITY (Last 7 Days):
- Calories: {stats['avg_daily_calories']:.0f}/day
- Protein: {stats['avg_daily_protein']:.0f}g/day
- Meal Quality: {stats['avg_meal_quality']:.1f}/10
- Workouts: {stats['workout_count']} sessions
- Progressive Overload: {stats['progressive_overload_percentage']:.0f}% of workouts improving
- Training Volume: {stats['total_training_volume_lbs']:,.0f} lbs total
- Cardio: {stats['total_cardio_minutes']:.0f} minutes, {stats['total_distance_km']:.1f} km

RELEVANT HISTORY (Most Similar Entries):
{history_summaries}

Based on this complete context, provide:
1. Specific, actionable advice
2. Data-driven recommendations
3. Personalized suggestions based on their patterns
4. Encouragement based on their progress

Be concise, direct, and supportive. Reference specific data points from their history when relevant.
"""

    return system_prompt
```

---

## 🎨 Part 4: Advanced Context Patterns

### 4.1 Pattern Detection

**AI should detect patterns in user behavior and proactively suggest improvements.**

```python
async def detect_patterns(user_id: str) -> List[dict]:
    """
    Detect behavioral patterns in user data.

    Returns list of detected patterns with recommendations.
    """

    patterns = []

    # Pattern 1: Meal timing consistency
    meal_times = await analyze_meal_timing_pattern(user_id, days=30)
    if meal_times['consistency_score'] < 0.5:
        patterns.append({
            "type": "meal_timing_inconsistency",
            "severity": "moderate",
            "description": "Meal times vary significantly day-to-day",
            "recommendation": "Try to eat meals at similar times each day for better metabolic regulation",
            "data": meal_times
        })

    # Pattern 2: Weekend diet deviation
    weekend_deviation = await analyze_weekend_nutrition(user_id, weeks=4)
    if weekend_deviation['calorie_increase_pct'] > 30:
        patterns.append({
            "type": "weekend_overeating",
            "severity": "high",
            "description": f"Weekend calories average {weekend_deviation['calorie_increase_pct']:.0f}% higher than weekdays",
            "recommendation": "Plan weekend meals in advance and track just as consistently",
            "data": weekend_deviation
        })

    # Pattern 3: Progressive overload plateau
    overload_trend = await analyze_progressive_overload_trend(user_id, weeks=8)
    if overload_trend['stalled_exercises'] > 2:
        patterns.append({
            "type": "strength_plateau",
            "severity": "moderate",
            "description": f"{overload_trend['stalled_exercises']} exercises have stalled for 3+ weeks",
            "recommendation": "Consider deload week or exercise variation to break through plateau",
            "data": overload_trend
        })

    # Pattern 4: Recovery inadequacy
    recovery_analysis = await analyze_recovery_adequacy(user_id, weeks=4)
    if recovery_analysis['under_recovered_percentage'] > 30:
        patterns.append({
            "type": "insufficient_recovery",
            "severity": "high",
            "description": "Training intensity outpacing recovery capacity",
            "recommendation": "Add 1-2 rest days per week or reduce session volume",
            "data": recovery_analysis
        })

    # Pattern 5: Protein intake variability
    protein_consistency = await analyze_protein_consistency(user_id, days=30)
    if protein_consistency['cv'] > 0.3:  # Coefficient of variation > 30%
        patterns.append({
            "type": "inconsistent_protein",
            "severity": "moderate",
            "description": "Daily protein intake varies significantly",
            "recommendation": f"Aim for consistent {protein_consistency['target_protein']:.0f}g protein daily",
            "data": protein_consistency
        })

    return patterns
```

### 4.2 Contextual Meal Suggestions

**When user asks "what should I eat?", AI considers:**
- Time of day
- Recent meals (avoid repetition)
- Remaining daily macros
- Training schedule (pre/post workout)
- Food preferences (learned from history)
- Previous high-rated meals

```python
async def suggest_meal(user_id: str, meal_type: str, context: str = None) -> dict:
    """
    Suggest personalized meal based on complete user context.
    """

    # Get today's nutrition so far
    today_nutrition = await get_today_nutrition(user_id)

    # Get user's macro targets
    user_targets = await get_user_macro_targets(user_id)

    # Calculate remaining macros
    remaining = {
        "calories": user_targets['calories'] - today_nutrition['calories'],
        "protein": user_targets['protein'] - today_nutrition['protein'],
        "carbs": user_targets['carbs'] - today_nutrition['carbs'],
        "fat": user_targets['fat'] - today_nutrition['fat']
    }

    # Get recent meals (avoid repetition)
    recent_meals = await get_recent_meals(user_id, days=3)
    recent_foods = set()
    for meal in recent_meals:
        if meal.get('foods'):
            recent_foods.update([f['name'] for f in meal['foods']])

    # Get user's favorite meals (high-rated in history)
    favorite_meals = await semantic_search(
        user_id=user_id,
        query=f"{meal_type} high quality satisfying",
        filters={"source_type": "meal"},
        limit=20
    )

    # Filter favorites by macro fit and freshness
    suitable_meals = []
    for meal in favorite_meals:
        metadata = meal['metadata']

        # Skip if eaten recently
        meal_foods = set([f['name'] for f in metadata.get('foods', [])])
        if meal_foods & recent_foods:  # Intersection
            continue

        # Check macro fit
        meal_cals = metadata.get('calories', 0)
        meal_protein = metadata.get('protein_g', 0)

        # Meal should provide at least 20% of remaining, max 60%
        if remaining['calories'] > 0:
            cal_fit = 0.2 <= meal_cals / remaining['calories'] <= 0.6
            protein_fit = meal_protein >= remaining['protein'] * 0.25

            if cal_fit and protein_fit:
                suitable_meals.append(meal)

    # Check training context
    todays_workouts = await get_todays_workouts(user_id)
    is_training_day = len(todays_workouts) > 0

    # Build recommendation
    if suitable_meals:
        # Found good historical meal
        best_meal = suitable_meals[0]
        suggestion = {
            "type": "historical_favorite",
            "meal": best_meal['metadata'],
            "reason": "Based on your past preferences and today's macro targets",
            "macro_fit": {
                "calories": best_meal['metadata']['calories'],
                "protein": best_meal['metadata']['protein_g'],
                "carbs": best_meal['metadata']['carbs_g'],
                "fat": best_meal['metadata']['fat_g']
            },
            "remaining_after": {
                "calories": remaining['calories'] - best_meal['metadata']['calories'],
                "protein": remaining['protein'] - best_meal['metadata']['protein_g']
            }
        }
    else:
        # Generate new suggestion with LLM
        suggestion_prompt = f"""
        Suggest a {meal_type} meal for a user with these requirements:

        Remaining macros for today:
        - Calories: {remaining['calories']:.0f}
        - Protein: {remaining['protein']:.0f}g
        - Carbs: {remaining['carbs']:.0f}g
        - Fat: {remaining['fat']:.0f}g

        Context:
        - Training day: {is_training_day}
        - Recent foods to avoid: {', '.join(list(recent_foods)[:10])}

        Provide a specific meal suggestion with foods, portions, and macro breakdown.
        """

        llm_suggestion = await dual_router.complete(
            config=TaskConfig(type=TaskType.STRUCTURED_OUTPUT),
            messages=[{"role": "user", "content": suggestion_prompt}],
            response_format={"type": "json_object"}
        )

        suggestion = {
            "type": "ai_generated",
            "meal": json.loads(llm_suggestion.choices[0].message.content),
            "reason": "Custom suggestion based on your remaining macros and preferences"
        }

    return suggestion
```

### 4.3 Workout Optimization

**When planning workouts, AI considers:**
- Muscle recovery status
- Recent training volume
- Progressive overload opportunities
- Weak points (lagging muscle groups)
- Preference patterns

```python
async def suggest_workout(user_id: str) -> dict:
    """
    Suggest optimal workout based on recovery and training patterns.
    """

    # Get muscle recovery status
    recovery_status = await calculate_muscle_recovery(user_id)
    # Returns: {"chest": 0.9, "legs": 0.3, "back": 0.85, ...}
    # 1.0 = fully recovered, 0.0 = very fatigued

    # Get recent training split
    recent_workouts = await get_recent_workouts(user_id, days=7)
    muscle_frequency = calculate_muscle_frequency(recent_workouts)
    # Returns: {"chest": 2, "legs": 1, "back": 2, ...}

    # Find most recovered and undertrained muscles
    workout_priority = {}
    for muscle, recovery in recovery_status.items():
        frequency = muscle_frequency.get(muscle, 0)

        # Priority = high recovery + low frequency
        priority = recovery * (1 / (frequency + 1))
        workout_priority[muscle] = priority

    # Sort by priority
    sorted_muscles = sorted(workout_priority.items(), key=lambda x: x[1], reverse=True)

    # Get top 2-3 muscle groups
    target_muscles = [m[0] for m in sorted_muscles[:3]]

    # Find similar past workouts
    similar_workouts = await semantic_search(
        user_id=user_id,
        query=f"workout {' '.join(target_muscles)} strength training",
        filters={"source_type": "workout"},
        limit=5
    )

    # Check for progressive overload opportunities
    if similar_workouts:
        last_workout = similar_workouts[0]['metadata']

        # Suggest slight increase
        suggested_exercises = []
        for ex in last_workout.get('exercises', []):
            suggested_exercises.append({
                "name": ex['name'],
                "sets": ex['sets'],
                "reps": ex['reps'],
                "weight_lbs": ex['weight_lbs'] * 1.025,  # 2.5% increase
                "note": "Progressive overload from last session"
            })

        suggestion = {
            "type": "progressive_overload",
            "workout_name": last_workout['workout_name'],
            "target_muscles": target_muscles,
            "exercises": suggested_exercises,
            "reason": f"Targeting {', '.join(target_muscles)} - fully recovered and due for training",
            "expected_volume": calculate_volume(suggested_exercises)
        }
    else:
        # No history, generate fresh workout
        suggestion = await generate_fresh_workout(target_muscles)

    return suggestion
```

---

## 🚀 Part 5: Real-World Recommendation Scenarios

### Scenario 1: "What should I eat for lunch?"

**AI's internal process:**

1. **Retrieve context**:
   - Today's meals so far: Breakfast (eggs, toast, 400 cal, 25g protein)
   - Daily targets: 2200 cal, 180g protein
   - Remaining: 1800 cal, 155g protein
   - Recent lunches: Chipotle bowl (yesterday), chicken salad (2 days ago)
   - Training today: Yes, upper body push at 6 PM

2. **Semantic search**:
   - Query: "lunch high protein satisfying"
   - Results: 20 past lunches with high ratings

3. **Filter and rank**:
   - Remove recent repeats (Chipotle, chicken salad)
   - Filter by macro fit (500-700 cal, 40-60g protein)
   - Rank by quality score and similarity

4. **Generate recommendation**:
   ```
   "Since you're training upper body later today, I recommend a high-protein lunch
   around 600 calories. Based on your history, you enjoyed these options:

   1. **Grilled chicken bowl with quinoa and veggies** (580 cal, 52g protein)
      - You rated this 9/10 two weeks ago
      - Great macro balance and you noted feeling energized after

   2. **Salmon with sweet potato and broccoli** (620 cal, 48g protein)
      - High in omega-3s for recovery
      - You've had this 3 times and always rated it highly

   Both meals will leave you with ~1200 calories for dinner and snacks, with
   ~100g protein remaining - perfect for post-workout meal.

   Want me to suggest a specific post-workout dinner too?"
   ```

### Scenario 2: "Why am I not losing weight?"

**AI's internal process:**

1. **Retrieve measurement history**:
   - 8 weeks of weight data
   - Trend: Down 2 lbs in first 4 weeks, stable last 4 weeks

2. **Analyze nutrition patterns**:
   - Average daily calories: 2100
   - Target: 1900
   - Weekday average: 1850
   - Weekend average: 2600 ← **ISSUE DETECTED**

3. **Check adherence**:
   - Logged meals: 75% of days
   - Missing weekend data often

4. **Calculate actual deficit**:
   - Weekly average: (1850 * 5 + 2600 * 2) / 7 = 2043 cal/day
   - Estimated TDEE: 2200
   - Actual deficit: 157 cal/day (very small)

5. **Generate insight**:
   ```
   "I found the issue! Your weight loss stalled because:

   **The Problem:**
   - Weekday nutrition is excellent: averaging 1,850 cal/day (perfectly on target)
   - BUT weekends average 2,600 cal/day - 700 calories over target
   - This erases most of your weekday deficit

   **The Math:**
   - Weekday deficit: 350 cal/day × 5 days = 1,750 cal deficit
   - Weekend surplus: 600 cal/day × 2 days = 1,200 cal surplus
   - Net weekly deficit: Only 550 calories (should be 2,450 for 0.7 lbs/week loss)

   **The Solution:**
   1. Bring weekend calories to 2,000 (not 1,900 - allow some flexibility!)
   2. This creates 1,400 cal weekly deficit = 0.4 lbs/week loss
   3. OR keep weekends the same but reduce weekdays to 1,750 (harder)

   I noticed you often don't log on weekends - that's probably why you didn't catch this.
   Try logging just Saturday and Sunday for the next 2 weeks and I bet you'll see the scale move!

   Your training is great (4 workouts/week consistently), so nutrition is the only variable to fix."
   ```

### Scenario 3: "Plan my workouts for this week"

**AI's internal process:**

1. **Check training history**:
   - Last 4 weeks: 4 workouts/week consistently
   - Split: Push/Pull/Legs/Upper
   - Last trained: Legs (2 days ago)

2. **Calculate muscle recovery**:
   - Chest: 95% recovered (last trained 6 days ago)
   - Back: 90% recovered (last trained 5 days ago)
   - Legs: 40% recovered (trained 2 days ago)
   - Shoulders: 100% recovered

3. **Check progressive overload status**:
   - Bench press: Stalled at 185x8 for 3 weeks
   - Deadlift: Improved last session (315x5 → 325x5)
   - Squat: Missed last week

4. **Generate weekly plan**:
   ```
   "Here's your optimal training plan for this week:

   **Monday - Push Day (Chest/Shoulders/Triceps)**
   - Bench Press: 4x8 at 185 lbs (try for 9 reps on set 1)
   - Incline DB Press: 3x10 at 65 lbs (up from 60 lbs)
   - Shoulder Press: 3x10 at 95 lbs
   - Lateral Raises: 3x12 at 25 lbs
   - Tricep Pushdowns: 3x15 at 50 lbs
   *Goal: Break through bench plateau - extra rest between sets*

   **Tuesday - Rest**

   **Wednesday - Pull Day (Back/Biceps)**
   - Deadlift: 3x5 at 330 lbs (continue progression!)
   - Barbell Rows: 4x8 at 155 lbs
   - Lat Pulldowns: 3x10 at 140 lbs
   - Face Pulls: 3x15
   - Barbell Curls: 3x10 at 75 lbs
   *You're crushing deadlifts - keep pushing here*

   **Thursday - Rest or Light Cardio**

   **Friday - Legs (Quads/Glutes/Hamstrings)**
   - Squats: 5x5 at 230 lbs (you missed last week - nail this!)
   - Romanian Deadlifts: 3x10 at 185 lbs
   - Leg Press: 3x12 at 270 lbs
   - Leg Curls: 3x12
   - Calf Raises: 4x15
   *Extra focus on squat form - you mentioned knee discomfort before*

   **Saturday - Upper Body Hypertrophy**
   - Lighter weights, higher reps for muscle growth
   - Focus on exercises you enjoy
   - 10-12 rep range, shorter rest

   **Sunday - Rest**

   **Key Focus This Week:**
   1. Break through bench plateau (eat more before workout, extra rest)
   2. Continue deadlift momentum
   3. Nail squats after missing last week

   This plan gives you 4 workouts with 3 full rest days. Volume is slightly higher
   than last week since you're recovered. Let me know how Monday's push day goes!"
   ```

### Scenario 4: "I'm feeling really tired and unmotivated"

**AI's internal process:**

1. **Sentiment analysis**: Negative sentiment detected

2. **Retrieve recent patterns**:
   - Training: 6 workouts last week (usual is 4)
   - Sleep notes: "tired" mentioned 4 times in past week
   - Calories: Below target 5 of 7 days
   - RPE: Average 8.5/10 (usual is 7/10)

3. **Cross-reference**:
   - Last rest day: 6 days ago
   - Total training volume: Up 30% from previous week
   - Cardio: Added 3 sessions (usually 1-2)

4. **Diagnosis**: Overtraining + undereating

5. **Generate empathetic response**:
   ```
   "I can see why you're feeling this way - your body is telling you something important!

   **What I'm seeing in your data:**

   1. **Training overload:**
      - Last week: 6 workouts (50% more than your usual 4)
      - Added extra cardio (3 sessions vs. usual 1-2)
      - RPE averaging 8.5/10 (usually 7/10)
      - Zero rest days in the past 6 days

   2. **Underfueling:**
      - Eating below target 5 of 7 days
      - Average deficit: 300 cal/day (on top of increased training)
      - This is a recipe for burnout

   3. **Recovery signals:**
      - You mentioned "tired" in 4 different entries this week
      - Workout ratings dropped from 8/10 to 6/10
      - Your body is screaming for rest

   **My recommendation:**

   1. **Take 2 full rest days** - today and tomorrow
      - No gym, no cardio
      - Light walking is fine
      - Focus on sleep (aim for 8+ hours)

   2. **Eat at maintenance** for 3 days
      - 2,200 calories (not your usual 1,900)
      - Extra carbs for glycogen replenishment
      - This is not "ruining progress" - it's recovery

   3. **Resume training Friday** with lighter session
      - Reduce weights by 10%
      - Focus on form and mind-muscle connection
      - Keep it to 45 minutes

   4. **Next week: back to 4 workouts**
      - Your body responds best to this frequency
      - More is not always better

   You've been crushing it and making great progress (down 8 lbs in 6 weeks!).
   This isn't laziness - it's your body asking for recovery. Athletes perform best
   when they respect the rest-adaptation cycle.

   Trust the process. Take the rest. You'll come back stronger. 💪

   How does this plan sound?"
   ```

---

## 📈 Part 6: Data Quality & Confidence Scoring

### 6.1 Confidence Scoring for Entries

**Every entry gets a confidence score based on data completeness and source.**

```python
def calculate_entry_confidence(entry_data: dict, source: str) -> float:
    """
    Calculate confidence score for an entry (0.0 - 1.0).

    Higher confidence = more reliable data for AI recommendations.
    """

    confidence = 0.5  # Base confidence

    # Source reliability
    source_weights = {
        "manual_detailed": 1.0,      # User manually entered all details
        "quick_entry_confirmed": 0.9, # User confirmed AI extraction
        "quick_entry_edited": 0.95,   # User confirmed + edited
        "imported_verified": 0.85,    # Imported from trusted source (MyFitnessPal)
        "quick_entry_auto": 0.7,      # Auto-saved without confirmation
        "estimated": 0.6              # Fully AI estimated
    }

    confidence *= source_weights.get(source, 0.5)

    # Data completeness (for meals)
    if entry_data.get('entry_type') == 'meal':
        completeness_score = 0

        # Has calories
        if entry_data.get('calories'):
            completeness_score += 0.25

        # Has macros
        if all([entry_data.get('protein_g'), entry_data.get('carbs_g'), entry_data.get('fat_g')]):
            completeness_score += 0.25

        # Has detailed foods
        if entry_data.get('foods') and len(entry_data['foods']) > 0:
            completeness_score += 0.25

        # Has image
        if entry_data.get('has_image'):
            completeness_score += 0.25

        confidence *= (0.7 + 0.3 * completeness_score)

    # Recency (newer = slightly more confident)
    days_old = (datetime.utcnow() - entry_data['logged_at']).days
    recency_factor = max(0.9, 1.0 - (days_old / 365) * 0.1)
    confidence *= recency_factor

    return min(confidence, 1.0)
```

### 6.2 Handling Low-Confidence Data

```python
async def get_reliable_nutrition_average(user_id: str, days: int = 7) -> dict:
    """
    Calculate nutrition averages using only high-confidence entries.
    """

    meals = await supabase.table("meal_logs") \
        .select("*") \
        .eq("user_id", user_id) \
        .gte("logged_at", datetime.utcnow() - timedelta(days=days)) \
        .gte("confidence_score", 0.7) \  # Only reliable data
        .execute()

    if not meals.data:
        # Fallback to all data if no high-confidence entries
        meals = await supabase.table("meal_logs") \
            .select("*") \
            .eq("user_id", user_id) \
            .gte("logged_at", datetime.utcnow() - timedelta(days=days)) \
            .execute()

    # Calculate weighted averages
    total_calories = 0
    total_protein = 0
    total_weight = 0

    for meal in meals.data:
        weight = meal.get('confidence_score', 0.5)
        total_calories += (meal.get('total_calories', 0) or 0) * weight
        total_protein += (meal.get('total_protein_g', 0) or 0) * weight
        total_weight += weight

    return {
        "avg_calories": total_calories / total_weight if total_weight > 0 else 0,
        "avg_protein": total_protein / total_weight if total_weight > 0 else 0,
        "sample_size": len(meals.data),
        "avg_confidence": total_weight / len(meals.data) if meals.data else 0
    }
```

---

## 🎓 Summary: The Complete AI Processing Pipeline

### Input → Processing → Storage → Retrieval → Recommendation

```
┌─────────────────────────────────────────────────────────────────┐
│ USER INPUT                                                      │
│ Text: "Grilled chicken with rice 450 calories"                 │
│ Image: [meal photo]                                             │
│ Type: Auto-detect                                               │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ AI CLASSIFICATION (LLM)                                         │
│ - Extract: meal name, type, macros, foods                      │
│ - Classify: type = "meal", confidence = 0.95                   │
│ - Enrich: quality scores, tags, goal alignment                 │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ USER CONFIRMATION                                                │
│ - User reviews extracted data                                   │
│ - User edits if needed (e.g., 450 → 500 calories)             │
│ - User clicks "Confirm & Log"                                  │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ DATABASE STORAGE                                                 │
│                                                                  │
│ 1. Save to `meal_logs` table:                                  │
│    - Structured meal data                                       │
│    - Nutrition (calories, macros)                              │
│    - Enriched metadata (quality scores, tags)                  │
│    - Confidence score                                           │
│                                                                  │
│ 2. Generate embedding:                                          │
│    - Build rich text representation                             │
│    - Generate 384-dim vector                                    │
│                                                                  │
│ 3. Save to `multimodal_embeddings` table:                      │
│    - Vector embedding                                           │
│    - Full metadata JSON                                         │
│    - Links to source (meal_logs.id)                            │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ CONTEXT BUILDING (when user asks AI for advice)                │
│                                                                  │
│ User: "What should I eat for dinner?"                          │
│                                                                  │
│ AI Process:                                                     │
│ 1. Semantic search: Find relevant meal history                 │
│ 2. Get today's nutrition: Calculate remaining macros           │
│ 3. Get training context: Check if workout scheduled            │
│ 4. Get preferences: Find high-rated past meals                 │
│ 5. Detect patterns: Avoid recent foods                         │
│                                                                  │
│ Retrieved Context:                                              │
│ - 20 similar past meals (vector similarity)                    │
│ - Today's meals: 1200 cal, 80g protein consumed               │
│ - Remaining: 1000 cal, 100g protein                            │
│ - Workout: Upper body at 8 PM (post-workout meal needed)       │
│ - Recent foods: chicken, rice (avoid repetition)               │
└─────────────────┬───────────────────────────────────────────────┘
                  │
                  ▼
┌─────────────────────────────────────────────────────────────────┐
│ AI RECOMMENDATION                                                │
│                                                                  │
│ "Based on your training today and remaining macros, I          │
│ recommend a high-protein post-workout dinner around 700 cal:   │
│                                                                  │
│ **Salmon with sweet potato and asparagus**                     │
│ - 680 cal, 55g protein, 45g carbs, 28g fat                    │
│ - You rated this 9/10 two weeks ago                           │
│ - Great for recovery with omega-3s                             │
│ - Leaves room for evening snack if needed                      │
│                                                                  │
│ This will bring your daily totals to:                          │
│ - 1,880 cal (target: 2,000)                                    │
│ - 135g protein (target: 180)                                   │
│                                                                  │
│ Perfect macro balance for today! 🎯"                           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🔥 Final Thoughts: Why This Architecture Wins

1. **Rich Data Capture**: Every entry stores not just raw data but contextual enrichments
2. **Semantic Memory**: Vector embeddings enable intelligent retrieval, not just keyword search
3. **Temporal Intelligence**: Time-aware scoring ensures recent data weighs appropriately
4. **Cross-Modal Fusion**: Text + image + structured data unified in one system
5. **Confidence-Aware**: AI knows when to trust data vs. when to ask for clarification
6. **Pattern Detection**: Proactive insights without user needing to ask
7. **Hyper-Personalization**: Every recommendation grounded in user's actual history
8. **Scalable**: Architecture handles millions of entries efficiently (indexed vectors, JSONB)

**This isn't just a logging app. It's a comprehensive AI fitness coach with perfect memory.**
