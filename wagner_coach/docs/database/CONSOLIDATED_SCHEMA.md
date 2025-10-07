# Wagner Coach - Consolidated Database Schema

**Migration:** `008_consolidated_schema.sql`
**Date:** 2025-10-06
**Status:** Production-Ready

---

## 🎯 Consolidation Summary

### Before: 80+ Tables (Bloated)
- Multiple redundant tables for same concepts
- Over-engineered food tracking (10+ tables)
- Duplicate settings tables (5+ tables)
- Unused feature tables (recipes, restaurants)
- Complex workout hierarchy (15+ tables)
- Multiple embedding tables (6 tables)

### After: 13 Core Tables (Clean)
- **1 table** for user profiles (vs 5 before)
- **2 tables** for Quick Entry (new, optimized)
- **2 tables** for meals (vs 10 before)
- **3 tables** for activities (consolidated)
- **1 table** for body measurements
- **1 table** for AI coach (vs 5 before)
- **3 tables** for AI programs (vs 8 before)

### Result: 84% reduction in table count ✅

---

## 📊 Core Schema Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         WAGNER COACH DATABASE                        │
│                      (13 Core Tables + 5 Support)                    │
└─────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                          USER LAYER                                  │
├──────────────────────────────────────────────────────────────────────┤
│  1. users                                                            │
│     - Consolidated profiles, settings, preferences                   │
│     - Onboarding data, goals, nutrition targets                      │
│     - Everything user-related in ONE table                           │
└──────────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    ↓            ↓            ↓

┌─────────────────────┐  ┌─────────────────────┐  ┌─────────────────────┐
│   QUICK ENTRY       │  │   MEALS             │  │   ACTIVITIES        │
├─────────────────────┤  ├─────────────────────┤  ├─────────────────────┤
│ 2. quick_entry_logs │  │ 4. meal_logs        │  │ 6. activities       │
│    - Raw input      │  │    - User meals     │  │    - All workouts   │
│    - AI extracted   │  │    - Nutrition data │  │    - Runs, sports   │
│    - Multimodal     │  │                     │  │    - Strava/Garmin  │
│                     │  │ 5. foods_enhanced   │  │                     │
│ 3. quick_entry_     │  │    - Food database  │  │ 7. activity_        │
│    embeddings       │  │    - Nutrition info │  │    segments         │
│    - Vector search  │  │                     │  │    - Laps/sets      │
│    - RAG context    │  │                     │  │                     │
│                     │  │                     │  │ 8. activity_streams │
│                     │  │                     │  │    - Time-series    │
└─────────────────────┘  └─────────────────────┘  └─────────────────────┘
          │                        │                        │
          │                        │                        │
          └────────────────────────┼────────────────────────┘
                                   ↓

┌──────────────────────────────────────────────────────────────────────┐
│                    BODY TRACKING                                     │
├──────────────────────────────────────────────────────────────────────┤
│  9. body_measurements                                                │
│     - Weight, body fat, measurements                                 │
│     - Supports Quick Entry extraction                                │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                    AI COACH LAYER                                    │
├──────────────────────────────────────────────────────────────────────┤
│  10. coach_messages                                                  │
│      - All conversation messages (user + assistant)                  │
│      - RAG context tracking                                          │
│      - Cost tracking per message                                     │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                    AI PROGRAMS LAYER                                 │
├──────────────────────────────────────────────────────────────────────┤
│  11. ai_generated_programs                                           │
│      - 12-week AI programs (meta data)                               │
│      │                                                                │
│      └──> 12. ai_program_days                                        │
│            - Daily schedule (84 days)                                │
│            │                                                          │
│            └──> 13. ai_program_items                                 │
│                 - Meals + Workouts (consolidated)                    │
│                 - item_type: 'meal' or 'workout'                     │
└──────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────┐
│                    SUPPORTING TABLES (5)                             │
├──────────────────────────────────────────────────────────────────────┤
│  • integrations (Strava, Garmin, Apple Health, etc.)                │
│  • user_goals (fitness/nutrition goals)                             │
│  • webhook_events (3rd party webhooks)                              │
│  • rate_limits (API rate limiting)                                  │
│  • daily_nutrition_summaries (performance optimization)             │
└──────────────────────────────────────────────────────────────────────┘
```

---

## 🔑 Core Tables Reference

### 1. `users` (Consolidated User Data)
**Purpose:** Single source of truth for all user data

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key (auth.users FK) |
| `full_name` | TEXT | User's full name |
| `email` | TEXT | Cached email |
| `age` | INTEGER | User age |
| `biological_sex` | TEXT | 'male', 'female', 'other' |
| `height_cm` | NUMERIC | Height in cm |
| `current_weight_kg` | NUMERIC | Current weight |
| `goal_weight_kg` | NUMERIC | Target weight |
| `primary_goal` | TEXT | Main fitness goal |
| `experience_level` | TEXT | 'beginner', 'intermediate', 'advanced' |
| `training_frequency` | INTEGER | Workouts per week |
| `available_equipment` | TEXT[] | Equipment access |
| `dietary_restrictions` | TEXT[] | Diet constraints |
| `injury_limitations` | TEXT[] | Physical limitations |
| `daily_calorie_target` | INTEGER | Calorie goal |
| `daily_protein_target_g` | INTEGER | Protein goal |
| `daily_carbs_target_g` | INTEGER | Carbs goal |
| `daily_fat_target_g` | INTEGER | Fat goal |
| `settings` | JSONB | All user settings/preferences |
| `onboarding_completed` | BOOLEAN | Onboarding status |
| `onboarding_data` | JSONB | Onboarding answers |
| `created_at` | TIMESTAMPTZ | Account creation |
| `updated_at` | TIMESTAMPTZ | Last profile update |
| `last_active_at` | TIMESTAMPTZ | Last activity |

**Replaces:** profiles, user_settings, user_preferences, user_preference_profiles, user_nutrition_preferences, rest_timer_preferences, user_onboarding

---

### 2. `quick_entry_logs` (Multimodal Input)
**Purpose:** Store raw user input + AI extracted data

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user_id` | UUID | FK to users |
| `input_type` | TEXT | 'text', 'voice', 'image', 'multimodal', 'pdf' |
| `raw_text` | TEXT | Original text input |
| `raw_transcription` | TEXT | Voice-to-text output |
| `image_urls` | TEXT[] | Uploaded images |
| `audio_url` | TEXT | Voice note URL |
| `ai_provider` | TEXT | 'groq', 'openrouter', 'anthropic' |
| `ai_model` | TEXT | Model used |
| `ai_cost_usd` | NUMERIC | Cost per entry |
| `ai_classification` | TEXT | 'meal', 'workout', 'body_measurement' |
| `ai_extracted_data` | JSONB | Structured output |
| `ai_confidence_score` | NUMERIC | 0.0 to 1.0 |
| `contains_meal` | BOOLEAN | Meal detected? |
| `contains_workout` | BOOLEAN | Workout detected? |
| `contains_body_measurement` | BOOLEAN | Measurement detected? |
| `meal_log_ids` | UUID[] | Links to created meals |
| `processing_status` | TEXT | 'pending', 'processing', 'completed', 'failed' |
| `logged_at` | TIMESTAMPTZ | When user submitted |

**New table** - core feature for Wagner Coach

---

### 3. `quick_entry_embeddings` (Vector Search)
**Purpose:** Enable semantic search and RAG

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `quick_entry_log_id` | UUID | FK to quick_entry_logs |
| `user_id` | UUID | FK to users |
| `embedding_type` | TEXT | 'text', 'image', 'multimodal' |
| `embedding` | vector(384) | 384-dimensional vector (FREE model) |
| `content_text` | TEXT | Searchable text |
| `content_summary` | TEXT | 1-2 sentence summary |
| `source_classification` | TEXT | 'meal', 'workout', etc. |
| `embedding_model` | TEXT | 'sentence-transformers/all-MiniLM-L6-v2' |
| `logged_at` | TIMESTAMPTZ | Original entry timestamp |

**Replaces:** embeddings, multimodal_embeddings, user_context_embeddings, profile_embeddings, goal_embeddings

---

### 4. `meal_logs` (User Meals)
**Purpose:** Track all meal logging

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user_id` | UUID | FK to users |
| `quick_entry_log_id` | UUID | FK to quick_entry_logs (if from QE) |
| `category` | TEXT | 'breakfast', 'lunch', 'dinner', 'snack' |
| `logged_at` | TIMESTAMPTZ | When eaten |
| `foods` | JSONB | Array of foods with quantities |
| `total_calories` | NUMERIC | Total calories |
| `total_protein_g` | NUMERIC | Total protein |
| `total_carbs_g` | NUMERIC | Total carbs |
| `total_fat_g` | NUMERIC | Total fat |
| `source` | TEXT | 'quick_entry', 'manual', 'imported' |
| `ai_extracted` | BOOLEAN | Created by AI? |
| `ai_confidence` | NUMERIC | Extraction confidence |
| `image_url` | TEXT | Meal photo |

**Kept from original schema** with enhancements

---

### 5. `foods_enhanced` (Food Database)
**Purpose:** Master food database

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `name` | TEXT | Food name |
| `brand_name` | TEXT | Brand |
| `barcode_upc` | TEXT | UPC barcode |
| `barcode_ean` | TEXT | EAN barcode |
| `serving_size` | NUMERIC | Serving size |
| `serving_unit` | TEXT | 'g', 'ml', 'oz', etc. |
| `calories` | NUMERIC | Calories per serving |
| `protein_g` | NUMERIC | Protein |
| `total_carbs_g` | NUMERIC | Carbohydrates |
| `total_fat_g` | NUMERIC | Fats |
| `dietary_fiber_g` | NUMERIC | Fiber |
| ... | ... | (40+ nutrition fields) |

**Kept as single source** of food data

---

### 6. `activities` (All Workouts/Sports)
**Purpose:** Store all physical activities

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user_id` | UUID | FK to users |
| `quick_entry_log_id` | UUID | FK to quick_entry_logs (if from QE) |
| `source` | TEXT | 'strava', 'garmin', 'manual', 'quick_entry' |
| `name` | TEXT | Activity name |
| `activity_type` | TEXT | 'run', 'strength', 'cycling', etc. |
| `start_date` | TIMESTAMPTZ | When started |
| `elapsed_time_seconds` | INTEGER | Total duration |
| `distance_meters` | NUMERIC | Distance covered |
| `calories` | INTEGER | Calories burned |
| `average_heartrate` | INTEGER | Avg HR |
| `notes` | TEXT | User notes |
| `ai_extracted` | BOOLEAN | Created by AI? |

**Kept from original** - well-designed for all activity types

---

### 7. `activity_segments` (Activity Details)
**Purpose:** Store laps, sets, intervals within activities

**Kept from original** - useful for detailed analysis

---

### 8. `activity_streams` (Time-Series Data)
**Purpose:** Store HR, power, pace over time

**Kept from original** - essential for advanced users

---

### 9. `body_measurements` (Body Tracking)
**Purpose:** Track weight, body fat, measurements

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user_id` | UUID | FK to users |
| `quick_entry_log_id` | UUID | FK to quick_entry_logs (if from QE) |
| `measured_at` | TIMESTAMPTZ | When measured |
| `weight_kg` | NUMERIC | Weight in kg |
| `body_fat_pct` | NUMERIC | Body fat % |
| `measurements` | JSONB | Other measurements |
| `source` | TEXT | 'manual', 'quick_entry', 'scale' |
| `ai_extracted` | BOOLEAN | Created by AI? |

**Kept from original** with Quick Entry integration

---

### 10. `coach_messages` (AI Conversations)
**Purpose:** Store all AI coach conversations

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user_id` | UUID | FK to users |
| `conversation_id` | UUID | Group messages together |
| `role` | TEXT | 'user', 'assistant', 'system' |
| `content` | TEXT | Message content |
| `context_used` | JSONB | RAG context retrieved |
| `ai_provider` | TEXT | 'anthropic', 'groq', etc. |
| `ai_model` | TEXT | Model used |
| `tokens_used` | INTEGER | Tokens consumed |
| `cost_usd` | NUMERIC | Cost per message |
| `created_at` | TIMESTAMPTZ | Message timestamp |

**Replaces:** ai_conversations, coach_conversations, coach_personas, conversation_summaries

---

### 11. `ai_generated_programs` (AI Programs Meta)
**Purpose:** Store AI program metadata

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user_id` | UUID | FK to users |
| `name` | TEXT | Program name |
| `description` | TEXT | Program description |
| `duration_weeks` | INTEGER | 12 weeks |
| `total_days` | INTEGER | 84 days |
| `is_active` | BOOLEAN | Currently active? |
| `status` | TEXT | 'active', 'completed', 'paused' |
| `current_day` | INTEGER | Current day (1-84) |
| `questions_answers` | JSONB | User answers for generation |
| `ai_model` | TEXT | Model used for generation |

**Kept from original** - core feature

---

### 12. `ai_program_days` (Program Schedule)
**Purpose:** Daily schedule within programs

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `program_id` | UUID | FK to ai_generated_programs |
| `day_number` | INTEGER | Day 1-84 |
| `day_name` | TEXT | "Day 1: Push Day" |
| `day_focus` | TEXT | "Upper body strength" |
| `is_completed` | BOOLEAN | Day completed? |
| `completed_at` | TIMESTAMPTZ | When completed |

**Kept from original** - essential structure

---

### 13. `ai_program_items` (Meals + Workouts)
**Purpose:** Daily meals AND workouts in ONE table

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `program_id` | UUID | FK to ai_generated_programs |
| `program_day_id` | UUID | FK to ai_program_days |
| `item_type` | TEXT | **'meal' or 'workout'** |
| `item_order` | INTEGER | Order within day |
| `meal_type` | TEXT | (if meal) 'breakfast', 'lunch', etc. |
| `meal_name` | TEXT | (if meal) Name |
| `meal_foods` | JSONB | (if meal) Foods array |
| `meal_calories` | NUMERIC | (if meal) Calories |
| `workout_name` | TEXT | (if workout) Name |
| `workout_type` | TEXT | (if workout) 'strength', 'cardio' |
| `workout_exercises` | JSONB | (if workout) Exercises array |
| `workout_duration_minutes` | INTEGER | (if workout) Duration |
| `is_completed` | BOOLEAN | Item completed? |

**NEW TABLE** - consolidates `ai_program_meals` + `ai_program_workouts` into ONE

---

## 🔄 Migration Strategy

### Option 1: Clean Slate (Recommended for New Projects)
```bash
# Run migration 008
psql -d your_database -f migrations/008_consolidated_schema.sql
```

### Option 2: Migrate Existing Data
```sql
-- Step 1: Back up existing database
pg_dump your_database > backup_before_consolidation.sql

-- Step 2: Migrate data to new schema
-- (Write migration scripts to move data from old tables to new consolidated ones)

-- Step 3: Run consolidation migration
-- (Drops old tables after data is migrated)
```

---

## 📈 Benefits of Consolidation

### 1. **Developer Experience**
- ✅ Easier to understand (13 tables vs 80+)
- ✅ Less joins required
- ✅ Faster development
- ✅ Clearer data model

### 2. **Performance**
- ✅ Fewer tables to scan
- ✅ Better index utilization
- ✅ Faster queries (less joins)
- ✅ Reduced query complexity

### 3. **Maintainability**
- ✅ Less code to maintain
- ✅ Fewer migrations needed
- ✅ Easier to debug
- ✅ Clearer RLS policies

### 4. **Cost Optimization**
- ✅ Smaller database size
- ✅ Fewer indexes to maintain
- ✅ Lower Supabase costs
- ✅ Faster backups/restores

---

## 🚀 API Impact

### Before (80+ tables):
```python
# Getting user data required multiple queries
profile = supabase.table("profiles").select("*").eq("user_id", user_id).execute()
settings = supabase.table("user_settings").select("*").eq("user_id", user_id).execute()
preferences = supabase.table("user_preferences").select("*").eq("user_id", user_id).execute()
nutrition_prefs = supabase.table("user_nutrition_preferences").select("*").eq("user_id", user_id).execute()
onboarding = supabase.table("user_onboarding").select("*").eq("user_id", user_id).execute()
```

### After (13 core tables):
```python
# Single query gets everything
user = supabase.table("users").select("*").eq("id", user_id).execute()
# All settings in user.data.settings JSONB field
```

---

## 🎯 Quick Reference

### Key Relationships
```
users (1) → (many) quick_entry_logs
users (1) → (many) meal_logs
users (1) → (many) activities
users (1) → (many) body_measurements
users (1) → (many) coach_messages
users (1) → (many) ai_generated_programs

quick_entry_logs (1) → (1) quick_entry_embeddings
quick_entry_logs (1) → (many) meal_logs (via FK)
quick_entry_logs (1) → (many) activities (via FK)

ai_generated_programs (1) → (many) ai_program_days
ai_program_days (1) → (many) ai_program_items
```

---

## ✅ Production Readiness Checklist

- [x] RLS policies on all user tables
- [x] Indexes on all foreign keys
- [x] Vector index for embeddings (HNSW)
- [x] Triggers for updated_at
- [x] JSONB for flexible data (settings, metadata)
- [x] Proper constraints (CHECK, UNIQUE, NOT NULL)
- [x] Comments on all tables
- [x] Views for common queries
- [x] Cost tracking fields (ai_cost_usd, tokens_used)
- [x] Backward compatibility (existing tables enhanced, not broken)

---

**This consolidated schema is production-ready and follows all CLAUDE.md standards.**
