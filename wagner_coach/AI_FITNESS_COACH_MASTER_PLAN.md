# AI Fitness Coach & Nutritionist - Master Implementation Plan
**Version:** 1.0
**Date:** September 30, 2025
**Objective:** Transform Wagner Coach into an intelligent, adaptive AI fitness coach and nutritionist

---

## 🎯 VISION

An AI-powered fitness platform that:
- **Learns** from every user action
- **Adapts** workout and nutrition plans in real-time
- **Coaches** like a real personal trainer and nutritionist
- **Simplifies** data entry (text, voice, photos)
- **Delivers** personalized, achievable recommendations

---

## 📊 PART 1: RAG SYSTEM ARCHITECTURE

### Option A: Supabase pgvector (RECOMMENDED ✅)
**Why:** Free, integrated, low latency, no external dependencies

**Architecture:**
```sql
-- Already have Supabase PostgreSQL
-- Add pgvector extension
CREATE EXTENSION vector;

-- Embeddings table
CREATE TABLE embeddings (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id),
  content TEXT NOT NULL,
  embedding vector(1536), -- OpenAI ada-002 dimensions
  metadata JSONB,
  source_type TEXT, -- 'workout', 'meal', 'progress', 'conversation'
  source_id UUID,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Similarity search function
CREATE FUNCTION match_embeddings(
  query_embedding vector(1536),
  match_threshold FLOAT,
  match_count INT,
  filter_user_id UUID
)
RETURNS TABLE (
  id UUID,
  content TEXT,
  metadata JSONB,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    embeddings.id,
    embeddings.content,
    embeddings.metadata,
    1 - (embeddings.embedding <=> query_embedding) AS similarity
  FROM embeddings
  WHERE user_id = filter_user_id
    AND 1 - (embeddings.embedding <=> query_embedding) > match_threshold
  ORDER BY embeddings.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;
```

**Embedding Strategy:**
- **Model:** OpenAI text-embedding-3-small ($0.02/1M tokens, 1536 dimensions)
- **Fallback:** Google Gemini embedding-001 (FREE, 768 dimensions)
- **Backend:** Python service generates embeddings asynchronously

**What to Embed:**
1. **Workout Sessions** - "Completed 5x5 squats at 225lbs, felt strong, great form"
2. **Meals** - "Breakfast: 3 eggs, 2 toast, coffee - 450 cal, 25g protein"
3. **Progress Notes** - "Hit new PR on bench press, up 10lbs from last month"
4. **Coach Conversations** - "User asked about protein timing"
5. **Goals & Milestones** - "Goal: lose 15lbs by June, run 5k under 25min"

**Retrieval Strategy:**
```python
# When user asks coach a question
query = "Should I do cardio before or after weights?"
query_embedding = openai.embeddings.create(input=query, model="text-embedding-3-small")

# Retrieve relevant context
relevant_docs = supabase.rpc('match_embeddings', {
  'query_embedding': query_embedding,
  'match_threshold': 0.7,
  'match_count': 10,
  'filter_user_id': user_id
})

# Build context for LLM
context = build_rag_context(user_profile, recent_workouts, relevant_docs)
response = openai.chat.completions.create(
  model="gpt-4o-mini",
  messages=[
    {"role": "system", "content": coach_system_prompt},
    {"role": "user", "content": f"Context: {context}\n\nQuestion: {query}"}
  ]
)
```

### Option B: Pinecone (Alternative)
**Pros:** Purpose-built for vector search, free tier (1GB, 1 index)
**Cons:** External dependency, additional API calls, potential latency

**Use if:** Scaling beyond 100k embeddings per user

---

## 💾 PART 2: DATABASE RESTRUCTURING

### Current Issues:
- No separation between PLANS (what coach recommends) vs ACTUALS (what user did)
- No nutrition planning table
- No progressive overload tracking
- No plan compliance metrics

### New Schema:

```sql
-- ============================================
-- WORKOUT PLANNING SYSTEM
-- ============================================

-- Master workout programs (AI-generated or template)
CREATE TABLE workout_programs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id),
  name TEXT NOT NULL,
  description TEXT,
  goal TEXT, -- 'strength', 'hypertrophy', 'endurance', 'general'
  duration_weeks INT,
  training_days_per_week INT,
  generated_by TEXT, -- 'ai', 'template', 'user'
  status TEXT DEFAULT 'active', -- 'active', 'completed', 'paused'
  metadata JSONB, -- AI reasoning, user preferences
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Planned workout sessions (what SHOULD happen)
CREATE TABLE planned_workouts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  program_id UUID REFERENCES workout_programs(id),
  user_id UUID REFERENCES profiles(id),
  week_number INT,
  day_of_week INT, -- 1-7 (Monday-Sunday)
  planned_date DATE,
  workout_type TEXT, -- 'push', 'pull', 'legs', 'upper', 'lower', 'full_body'
  time_of_day TEXT, -- 'morning', 'afternoon', 'evening'
  estimated_duration_minutes INT,
  notes TEXT,
  status TEXT DEFAULT 'pending', -- 'pending', 'completed', 'skipped', 'rescheduled'
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Planned exercises within a workout
CREATE TABLE planned_exercises (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  planned_workout_id UUID REFERENCES planned_workouts(id),
  exercise_name TEXT NOT NULL,
  exercise_type TEXT, -- 'compound', 'isolation', 'cardio'
  muscle_groups TEXT[], -- ['chest', 'triceps']
  order_in_workout INT,
  target_sets INT,
  target_reps_min INT,
  target_reps_max INT,
  target_weight_lbs FLOAT,
  target_rpe FLOAT, -- Rate of Perceived Exertion (1-10)
  target_rest_seconds INT,
  progression_scheme TEXT, -- 'linear', 'double_progression', 'wave'
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Actual workout sessions (what ACTUALLY happened)
CREATE TABLE actual_workouts (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id),
  planned_workout_id UUID REFERENCES planned_workouts(id), -- NULL if unplanned
  started_at TIMESTAMPTZ NOT NULL,
  completed_at TIMESTAMPTZ,
  duration_minutes INT,
  workout_type TEXT,
  energy_level INT, -- 1-10
  overall_rating INT, -- 1-5 stars
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Actual exercise performance (what was ACTUALLY lifted)
CREATE TABLE actual_exercise_sets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  actual_workout_id UUID REFERENCES actual_workouts(id),
  planned_exercise_id UUID REFERENCES planned_exercises(id), -- NULL if unplanned
  exercise_name TEXT NOT NULL,
  set_number INT,
  reps_completed INT,
  weight_lbs FLOAT,
  rpe FLOAT,
  tempo TEXT, -- '3-1-1-0' (eccentric-pause-concentric-pause)
  rest_seconds INT,
  form_quality INT, -- 1-5
  notes TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Progressive overload tracking
CREATE TABLE exercise_progress (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id),
  exercise_name TEXT NOT NULL,
  date DATE NOT NULL,
  volume_lbs FLOAT, -- sets * reps * weight
  max_weight_lbs FLOAT,
  total_reps INT,
  average_rpe FLOAT,
  one_rep_max_estimate FLOAT, -- Calculated via Epley formula
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, exercise_name, date)
);

-- ============================================
-- NUTRITION PLANNING SYSTEM
-- ============================================

-- Master nutrition programs (AI-generated)
CREATE TABLE nutrition_programs (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id),
  name TEXT NOT NULL,
  goal TEXT, -- 'cut', 'bulk', 'maintain', 'recomp'
  start_date DATE,
  end_date DATE,
  daily_calorie_target INT,
  protein_g_target INT,
  carbs_g_target INT,
  fat_g_target INT,
  meal_frequency INT, -- 3-6 meals per day
  generated_by TEXT, -- 'ai', 'user'
  status TEXT DEFAULT 'active',
  metadata JSONB, -- AI reasoning, TDEE calculation, macro split rationale
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Planned meals (what SHOULD be eaten)
CREATE TABLE planned_meals (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  program_id UUID REFERENCES nutrition_programs(id),
  user_id UUID REFERENCES profiles(id),
  planned_date DATE,
  meal_type TEXT, -- 'breakfast', 'lunch', 'dinner', 'snack', 'pre_workout', 'post_workout'
  planned_time TIME,
  name TEXT,
  description TEXT,
  target_calories INT,
  target_protein_g FLOAT,
  target_carbs_g FLOAT,
  target_fat_g FLOAT,
  recipe_instructions TEXT,
  shopping_list TEXT[],
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Planned meal foods (ingredients in planned meals)
CREATE TABLE planned_meal_foods (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  planned_meal_id UUID REFERENCES planned_meals(id),
  food_id UUID REFERENCES foods(id),
  quantity FLOAT,
  unit TEXT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Compliance tracking
CREATE TABLE nutrition_compliance (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id),
  date DATE NOT NULL,
  planned_calories INT,
  actual_calories INT,
  planned_protein_g FLOAT,
  actual_protein_g FLOAT,
  planned_carbs_g FLOAT,
  actual_carbs_g FLOAT,
  planned_fat_g FLOAT,
  actual_fat_g FLOAT,
  compliance_score FLOAT, -- 0-100
  created_at TIMESTAMPTZ DEFAULT NOW(),
  UNIQUE(user_id, date)
);

-- ============================================
-- AI COACHING SYSTEM
-- ============================================

-- Coach personas (nutritionist, trainer, general)
CREATE TABLE coach_personas (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  name TEXT NOT NULL, -- 'nutritionist', 'trainer', 'general'
  system_prompt TEXT NOT NULL,
  temperature FLOAT DEFAULT 0.7,
  model TEXT DEFAULT 'gpt-4o-mini',
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Coach conversations (full chat history)
CREATE TABLE coach_conversations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id),
  persona TEXT, -- 'nutritionist', 'trainer', 'general'
  user_message TEXT,
  coach_response TEXT,
  context_used JSONB, -- What RAG context was retrieved
  tokens_used INT,
  created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Coach recommendations (action items)
CREATE TABLE coach_recommendations (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES profiles(id),
  type TEXT, -- 'workout_plan', 'nutrition_plan', 'exercise_form', 'recovery'
  title TEXT,
  description TEXT,
  priority INT, -- 1-5
  status TEXT DEFAULT 'pending', -- 'pending', 'accepted', 'dismissed', 'completed'
  action_data JSONB, -- Structured data for what to do
  reasoning TEXT, -- Why coach recommended this
  created_at TIMESTAMPTZ DEFAULT NOW(),
  expires_at TIMESTAMPTZ
);

-- User feedback on recommendations
CREATE TABLE recommendation_feedback (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  recommendation_id UUID REFERENCES coach_recommendations(id),
  user_id UUID REFERENCES profiles(id),
  rating INT, -- 1-5
  feedback_text TEXT,
  was_helpful BOOLEAN,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

---

## 🤖 PART 3: AI COACHING INTELLIGENCE

### 3.1 Coach Personas

**Nutritionist Persona:**
```python
NUTRITIONIST_SYSTEM_PROMPT = """
You are a certified sports nutritionist with 15 years of experience.

KNOWLEDGE BASE:
- Macronutrient timing and optimization
- Meal frequency and metabolic effects
- Supplement protocols (creatine, protein, caffeine)
- Hydration strategies
- Nutrient partitioning
- Body recomposition science

PERSONALITY:
- Evidence-based and scientific
- Empathetic but direct
- Focuses on sustainable habits
- Celebrates small wins
- Never promotes fad diets or quick fixes

CONTEXT AWARENESS:
You have access to:
- User's complete nutrition history
- Current goals (cut/bulk/maintain)
- Training schedule (affects nutrition needs)
- Food preferences and restrictions
- Past compliance and adherence patterns

RESPONSE STYLE:
- Short, actionable advice (2-3 sentences)
- Use specific numbers (grams, calories)
- Reference user's actual data
- Ask clarifying questions when needed
- Provide reasoning for recommendations

CURRENT USER DATA:
{user_context}
"""
```

**Trainer Persona:**
```python
TRAINER_SYSTEM_PROMPT = """
You are an elite strength and conditioning coach with expertise in:

KNOWLEDGE BASE:
- Progressive overload principles
- Volume management and periodization
- Exercise selection and biomechanics
- Form cues and technique
- Injury prevention and recovery
- Program design (strength, hypertrophy, endurance)

PERSONALITY:
- Motivating but realistic
- Detail-oriented about form
- Strategic about programming
- Celebrates PRs and progress
- Adjusts plans based on feedback

CONTEXT AWARENESS:
You have access to:
- User's complete workout history
- Current program and goals
- Recent performance (RPE, volume, PRs)
- Recovery status and sleep
- Compliance with planned workouts

RESPONSE STYLE:
- Specific exercise recommendations
- Explain the "why" behind programming
- Adjust volume/intensity based on feedback
- Provide form cues when needed
- Reference recent workouts

CURRENT USER DATA:
{user_context}
"""
```

### 3.2 Context Building (RAG + Structured Data)

```python
async def build_comprehensive_context(user_id: str, query: str) -> dict:
    """
    Build complete context for AI coach including:
    1. RAG-retrieved relevant historical data
    2. Recent structured data (last 30 days)
    3. Current plans and goals
    4. Compliance metrics
    """

    # 1. Get user profile and goals
    profile = await get_user_profile(user_id)
    goals = await get_active_goals(user_id)

    # 2. Get current active plans
    workout_program = await get_active_workout_program(user_id)
    nutrition_program = await get_active_nutrition_program(user_id)

    # 3. Get recent actuals (last 30 days)
    recent_workouts = await get_recent_workouts(user_id, days=30)
    recent_meals = await get_recent_meals(user_id, days=30)

    # 4. Calculate compliance
    workout_compliance = calculate_workout_compliance(user_id, days=30)
    nutrition_compliance = calculate_nutrition_compliance(user_id, days=30)

    # 5. Get progressive overload trends
    strength_progress = await get_strength_trends(user_id, exercises=['squat', 'bench', 'deadlift'])

    # 6. RAG retrieval (semantic search)
    query_embedding = await generate_embedding(query)
    relevant_memories = await semantic_search(
        user_id=user_id,
        query_embedding=query_embedding,
        limit=10,
        threshold=0.7
    )

    # 7. Get recent coach interactions
    recent_conversations = await get_recent_conversations(user_id, limit=5)

    context = {
        "profile": {
            "age": profile.age,
            "weight_lbs": profile.weight_lbs,
            "height_inches": profile.height_inches,
            "experience_level": profile.experience_level,
            "training_frequency": profile.training_frequency
        },
        "goals": [
            {
                "type": g.goal_type,
                "target": g.target_value,
                "deadline": g.target_date,
                "progress": g.current_progress
            } for g in goals
        ],
        "current_plans": {
            "workout": {
                "program_name": workout_program.name,
                "goal": workout_program.goal,
                "days_per_week": workout_program.training_days_per_week,
                "week_number": workout_program.current_week
            },
            "nutrition": {
                "program_name": nutrition_program.name,
                "goal": nutrition_program.goal,
                "daily_calories": nutrition_program.daily_calorie_target,
                "macros": {
                    "protein_g": nutrition_program.protein_g_target,
                    "carbs_g": nutrition_program.carbs_g_target,
                    "fat_g": nutrition_program.fat_g_target
                }
            }
        },
        "recent_performance": {
            "workouts_completed_30d": len(recent_workouts),
            "workout_compliance_pct": workout_compliance,
            "avg_workout_rating": calculate_avg_rating(recent_workouts),
            "nutrition_compliance_pct": nutrition_compliance,
            "avg_daily_protein_g": calculate_avg_protein(recent_meals),
            "strength_trends": strength_progress
        },
        "relevant_memories": [
            {
                "content": m.content,
                "source": m.source_type,
                "date": m.created_at,
                "similarity": m.similarity_score
            } for m in relevant_memories
        ],
        "recent_conversations": [
            {
                "user": c.user_message,
                "coach": c.coach_response[:100],  # First 100 chars
                "date": c.created_at
            } for c in recent_conversations
        ]
    }

    return context
```

### 3.3 Adaptive Recommendations

```python
async def generate_weekly_recommendations(user_id: str):
    """
    Every Monday, AI coach analyzes last week and makes recommendations
    """

    # Analyze last week's data
    last_week_data = await analyze_week(user_id, weeks_ago=1)

    recommendations = []

    # 1. Workout Volume Check
    if last_week_data['total_sets'] > last_week_data['planned_sets'] * 1.2:
        recommendations.append({
            "type": "workout_plan",
            "priority": 1,
            "title": "Reduce Training Volume",
            "description": f"You completed {last_week_data['total_sets']} sets last week (20% over plan). This increases injury risk. Let's scale back to {int(last_week_data['planned_sets'])} sets this week.",
            "reasoning": "Volume management: >20% over plan = increased injury risk",
            "action_data": {
                "adjust_program": True,
                "new_weekly_sets": int(last_week_data['planned_sets'])
            }
        })

    # 2. Progressive Overload Check
    if last_week_data['avg_rpe'] < 6.5:
        recommendations.append({
            "type": "workout_plan",
            "priority": 2,
            "title": "Increase Weight",
            "description": f"Your average RPE was {last_week_data['avg_rpe']}/10. You're ready to progress. Add 5lbs to main lifts this week.",
            "reasoning": "Progressive overload: RPE < 7 = room to increase intensity",
            "action_data": {
                "exercises_to_increase": last_week_data['main_lifts'],
                "weight_increase_lbs": 5
            }
        })

    # 3. Nutrition Compliance
    if last_week_data['protein_compliance_pct'] < 80:
        recommendations.append({
            "type": "nutrition_plan",
            "priority": 1,
            "title": "Increase Protein Intake",
            "description": f"You hit protein target only {last_week_data['protein_compliance_pct']}% of days. Try adding a protein shake post-workout.",
            "reasoning": f"Protein compliance: {last_week_data['protein_compliance_pct']}% < 80% threshold",
            "action_data": {
                "add_meal": {
                    "type": "post_workout",
                    "foods": ["protein_powder_30g", "banana_medium"],
                    "calories": 250,
                    "protein_g": 30
                }
            }
        })

    # 4. Recovery Check
    if last_week_data['avg_sleep_hours'] < 7:
        recommendations.append({
            "type": "recovery",
            "priority": 1,
            "title": "Prioritize Sleep",
            "description": f"You averaged {last_week_data['avg_sleep_hours']}hrs of sleep. Aim for 7-9hrs to maximize recovery and results.",
            "reasoning": "Sleep < 7hrs = impaired recovery and muscle growth"
        })

    # Store recommendations
    for rec in recommendations:
        await create_recommendation(user_id, rec)

    return recommendations
```

---

## 🎨 PART 4: UI/UX REDESIGN

### 4.1 New Pages & Components

#### **A. Dashboard (Redesigned)**
**URL:** `/dashboard`

**Layout:**
```
┌─────────────────────────────────────────────┐
│  🏋️ WAGNER COACH                            │
├─────────────────────────────────────────────┤
│  [Quick Actions Bar - Always Visible]       │
│  💬 Ask Coach  |  🍽️ Log Meal  |  💪 Log Workout  |  📸 Scan  │
├─────────────────────────────────────────────┤
│                                              │
│  TODAY'S PLAN               YOUR PROGRESS   │
│  ┌──────────────────┐      ┌─────────────┐ │
│  │ 🏋️ Leg Day       │      │ 🔥 Streak   │ │
│  │ 5 exercises      │      │ 12 days     │ │
│  │ Est. 60 min      │      │             │ │
│  │ [Start Workout]  │      │ 📊 Macros   │ │
│  └──────────────────┘      │ P: 125/150g │ │
│                             │ C: 200/250g │ │
│  ┌──────────────────┐      │ F: 45/70g   │ │
│  │ 🍽️ Planned Meals │      │             │ │
│  │                  │      │ 💪 Volume   │ │
│  │ Breakfast        │      │ 45 sets     │ │
│  │ [Log] 450 cal    │      │ this week   │ │
│  │                  │      └─────────────┘ │
│  │ Lunch            │                      │
│  │ [Log] 650 cal    │  COACH INSIGHTS      │
│  │                  │  ┌─────────────────┐ │
│  │ Dinner           │  │ 🎯 "Great week! │ │
│  │ [Log] 700 cal    │  │  Volume is spot │ │
│  └──────────────────┘  │  on. Consider   │ │
│                         │  adding 5lbs to │ │
│  COACH RECOMMENDATIONS  │  squat."        │ │
│  ┌──────────────────┐  └─────────────────┘ │
│  │ ⚠️ HIGH PRIORITY │                      │
│  │ Increase protein │                      │
│  │ [View Plan]      │                      │
│  └──────────────────┘                      │
│                                              │
└─────────────────────────────────────────────┘
```

**Key Features:**
- **Persistent Quick Action Bar** at top of every page
- **Today's Plan** shows scheduled workouts & meals
- **One-tap logging** for planned items
- **Real-time progress** bars
- **Coach insights** card with personalized tips
- **Priority recommendations** above the fold

#### **B. Quick Entry Modal (New)**
**Trigger:** Floating button on every page, voice command, or quick action bar

**Modal:**
```
┌────────────────────────────────┐
│  QUICK ENTRY                ✕  │
├────────────────────────────────┤
│                                │
│  What did you just do?         │
│  ┌──────────────────────────┐ │
│  │ [Type here or use voice] │ │
│  │ 🎤                       │ │
│  └──────────────────────────┘ │
│                                │
│  OR                            │
│                                │
│  [📸 Scan Meal]                │
│  [💪 Scan Workout Summary]     │
│  [⚖️ Log Weight]               │
│                                │
│  AI will categorize and add    │
│  to the right place            │
│                                │
└────────────────────────────────┘
```

**Examples:**
- User types: "just had coffee and a bagel"
  → AI: Creates breakfast meal log with estimated macros

- User types: "finished bench press, 5 sets of 8 at 185"
  → AI: Creates workout activity, calculates volume

- User uploads photo of gym app showing workout summary
  → AI (GPT-4 Vision): Extracts exercises, sets, reps, adds to activities

#### **C. Coach Chat (Enhanced)**
**URL:** `/coach`

**Layout:**
```
┌─────────────────────────────────────────────┐
│  💬 COACH CHAT                               │
├─────────────────────────────────────────────┤
│  [Trainer] [Nutritionist] [General]          │
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                              │
│  🏋️ TRAINER                                 │
│  "I analyzed your squat volume from last    │
│  week (65 reps at avg 205lbs). You're ready │
│  to increase to 215lbs this week based on   │
│  your RPE of 6.5/10. Want me to update?"    │
│                          [Update Plan] [Ask] │
│                                              │
│  YOU                                         │
│  "What about my deadlift? Felt hard."       │
│                                              │
│  🏋️ TRAINER                                 │
│  "Looking at your last 3 deadlift sessions: │
│  - Week 1: 275x5 RPE 8                      │
│  - Week 2: 285x5 RPE 8.5                    │
│  - Week 3: 295x5 RPE 9                      │
│                                              │
│  You're progressing too fast. Let's deload  │
│  to 275x5 this week to manage fatigue."     │
│                       [Update] [Explain Why] │
│                                              │
├─────────────────────────────────────────────┤
│  [Type message...]                      [🎤] │
└─────────────────────────────────────────────┘
```

**Key Features:**
- **Context-aware responses** with actual user data
- **Action buttons** to accept recommendations
- **Multi-turn conversations** with memory
- **Persona switching** (trainer vs nutritionist)
- **Voice input** via microphone
- **Show sources** (what data coach used)

#### **D. Nutrition Planner (New Page)**
**URL:** `/nutrition/planner`

**Layout:**
```
┌─────────────────────────────────────────────┐
│  🍽️ NUTRITION PLANNER                       │
├─────────────────────────────────────────────┤
│  Current Goal: Cut (-500 cal/day)           │
│  Daily Target: 2000 cal | 150P 200C 70F     │
│                                              │
│  WEEKLY MEAL PLAN                  [Edit]   │
│                                              │
│  Monday ───────────────────────────────────  │
│  ┌─────────────────────────────────────┐    │
│  │ Breakfast (7am)          450 cal    │    │
│  │ • 3 eggs scrambled        30g P     │    │
│  │ • 2 toast w/ butter       40g C     │    │
│  │ • Coffee                  15g F     │    │
│  │              [✓ Logged] [View Recipe]│    │
│  ├─────────────────────────────────────┤    │
│  │ Lunch (12pm)             650 cal    │    │
│  │ • Chicken breast 6oz      45g P     │    │
│  │ • Rice 1 cup              50g C     │    │
│  │ • Broccoli                10g F     │    │
│  │                 [Log] [View Recipe] │    │
│  ├─────────────────────────────────────┤    │
│  │ Pre-Workout (4pm)        250 cal    │    │
│  │ • Protein shake           30g P     │    │
│  │ • Banana                  30g C     │    │
│  │                 [Log] [View Recipe] │    │
│  ├─────────────────────────────────────┤    │
│  │ Dinner (7pm)             700 cal    │    │
│  │ • Salmon 8oz              50g P     │    │
│  │ • Sweet potato            60g C     │    │
│  │ • Asparagus               20g F     │    │
│  │                 [Log] [View Recipe] │    │
│  └─────────────────────────────────────┘    │
│                                              │
│  Daily Total: 2050 cal (target 2000)        │
│  Macros: 155P 180C 60F ✅                   │
│                                              │
│  [🤖 Regenerate Plan] [📋 Shopping List]    │
│                                              │
└─────────────────────────────────────────────┘
```

**Key Features:**
- **AI-generated meal plans** based on goals
- **One-tap logging** from plan
- **Recipe instructions** for each meal
- **Auto-generated shopping lists**
- **Swap meals** (drag & drop)
- **Regenerate** with AI if user doesn't like

#### **E. Workout Planner (New Page)**
**URL:** `/workouts/planner`

**Layout:**
```
┌─────────────────────────────────────────────┐
│  💪 WORKOUT PLANNER                          │
├─────────────────────────────────────────────┤
│  Current Program: Hypertrophy PPL           │
│  Week 3 of 12 | 6 days/week                 │
│                                              │
│  THIS WEEK'S PLAN              [Edit Program]│
│                                              │
│  Monday - PUSH ──────────────────────────    │
│  ┌─────────────────────────────────────┐    │
│  │ Status: ✅ Completed (Oct 1, 7am)   │    │
│  │ Duration: 62 min | Rating: 4/5 ⭐⭐⭐⭐│    │
│  │                                      │    │
│  │ 1. Bench Press      4x8-10 @185lbs  │    │
│  │    ✅ 185x10, 185x9, 185x8, 185x8   │    │
│  │    RPE: 7.5/10 | Volume: 6,475 lbs  │    │
│  │                                      │    │
│  │ 2. Overhead Press   4x8-10 @95lbs   │    │
│  │    ✅ 95x10, 95x9, 95x8, 95x8       │    │
│  │    RPE: 8/10 | Volume: 3,325 lbs    │    │
│  │                                      │    │
│  │ ... (3 more exercises)               │    │
│  └─────────────────────────────────────┘    │
│                                              │
│  Tuesday - PULL ─────────────────────────    │
│  ┌─────────────────────────────────────┐    │
│  │ Status: Scheduled (Oct 2, 7am)       │    │
│  │ Est. Duration: 60 min                │    │
│  │                                      │    │
│  │ 1. Deadlift         4x6-8 @275lbs   │    │
│  │    Target RPE: 8/10                  │    │
│  │    ⚠️ COACH NOTE: Deload week       │    │
│  │    Last week RPE was 9/10            │    │
│  │                                      │    │
│  │ 2. Barbell Row      4x8-10 @155lbs  │    │
│  │ 3. Lat Pulldown     3x10-12 @120lbs │    │
│  │ 4. Face Pulls       3x15-20 @40lbs  │    │
│  │ 5. Barbell Curl     3x10-12 @65lbs  │    │
│  │                                      │    │
│  │            [Start Workout] [Edit]    │    │
│  └─────────────────────────────────────┘    │
│                                              │
│  [🤖 Ask Coach to Adjust]                   │
│                                              │
└─────────────────────────────────────────────┘
```

**Key Features:**
- **Weekly view** of planned workouts
- **Plan vs actual** comparison
- **Progressive overload** tracking (volume, weight)
- **RPE targets** and actuals
- **Coach notes** on specific exercises
- **One-tap start** workout from plan

#### **F. Progress Analytics (Enhanced)**
**URL:** `/progress`

**Layout:**
```
┌─────────────────────────────────────────────┐
│  📊 PROGRESS ANALYTICS                       │
├─────────────────────────────────────────────┤
│  [Strength] [Body Comp] [Nutrition] [Volume]│
│  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
│                                              │
│  STRENGTH PROGRESS                           │
│                                              │
│  Squat 1RM Estimate                          │
│  ┌──────────────────────────────────────┐   │
│  │      *                               │   │
│  │    *                                 │   │
│  │  *                                   │   │
│  │*                                     │   │
│  │                                      │   │
│  │ Sep    Oct    Nov    Dec    Jan     │   │
│  └──────────────────────────────────────┘   │
│  Current: 315 lbs (+15 lbs from start)      │
│                                              │
│  PLAN VS ACTUAL                              │
│  ┌──────────────────────────────────────┐   │
│  │ Planned Volume:  45 sets/week        │   │
│  │ Actual Volume:   48 sets/week (+7%)  │   │
│  │                                      │   │
│  │ Workout Adherence: 92% (11/12 done)  │   │
│  │ Nutrition Adherence: 85% (6/7 days)  │   │
│  └──────────────────────────────────────┘   │
│                                              │
│  🎯 GOALS PROGRESS                           │
│  ┌──────────────────────────────────────┐   │
│  │ Lose 15 lbs by June                  │   │
│  │ ████████░░░░ 67% (10/15 lbs)         │   │
│  │                                      │   │
│  │ Run 5k under 25min                   │   │
│  │ ████████░░░░ 40% (31:20 → 28:45)     │   │
│  └──────────────────────────────────────┘   │
│                                              │
└─────────────────────────────────────────────┘
```

### 4.2 Quick Entry Flows

#### **Flow 1: Voice/Text Entry**
```
User: "just finished leg day"
  ↓
AI: Searches recent plan for "leg day"
  ↓
AI: Finds planned workout from today
  ↓
Modal: "Did you complete today's Leg Day workout?"
        [Yes - all exercises] [Partially] [Different workout]
  ↓
User: Clicks "Yes - all exercises"
  ↓
System: Creates workout log, copies planned exercises
  ↓
Modal: "Great! Rate your workout (1-5 stars)"
  ↓
User: 4 stars
  ↓
System: Saves, updates streak, generates embedding
  ↓
Toast: "✅ Leg Day logged! +50 weekly volume"
```

#### **Flow 2: Photo Entry (Meal)**
```
User: Opens Quick Entry, clicks "Scan Meal"
  ↓
Camera opens
  ↓
User: Takes photo of plate
  ↓
Shows preview with loading spinner
  ↓
Backend: Sends to GPT-4 Vision API
  ↓
GPT-4 Vision: "I see grilled chicken breast (~6oz),
               steamed broccoli (~1 cup), and brown
               rice (~1 cup). Estimated: 450 cal,
               45g protein, 50g carbs, 10g fat"
  ↓
Modal: "Does this look right?"
        [Food items with editable quantities]
        [Add missing items]
        [✓ Confirm] [✕ Cancel]
  ↓
User: Confirms
  ↓
System: Creates meal_log with foods
  ↓
AI: Generates embedding: "Lunch: chicken, broccoli, rice - 450 cal, high protein"
  ↓
Toast: "✅ Meal logged! 45g protein toward 150g goal"
```

#### **Flow 3: Photo Entry (Workout Summary)**
```
User: Takes screenshot of Apple Watch workout summary
  ↓
Uploads via Quick Entry
  ↓
GPT-4 Vision: Extracts text
  "Workout: Outdoor Run
   Duration: 32:45
   Distance: 3.1 miles
   Calories: 385
   Avg Heart Rate: 165 bpm"
  ↓
Modal: "Is this correct?"
        Activity: Running
        Duration: 32 min 45 sec
        Distance: 3.1 mi
        Calories: 385
        [✓ Confirm]
  ↓
User: Confirms
  ↓
System: Creates activity log
  ↓
Toast: "✅ Run logged! Great cardio session"
```

---

## 🏗️ PART 5: FRONTEND vs BACKEND SPLIT

### Frontend Responsibilities (Next.js):

✅ **UI/UX Layer:**
- All pages and components
- Form validation and user input
- Quick entry modal
- Real-time feedback (toasts, animations)
- Photo/voice capture
- Chart rendering (recharts)

✅ **Simple Queries:**
- Fetch user profile
- List recent workouts/meals
- Display plans
- Show recommendations

✅ **Client-side State:**
- Active workout session tracking
- Form state management
- UI preferences (dark mode, units)

✅ **Supabase Direct Calls (Simple CRUD):**
- Insert meal log
- Insert workout session
- Update user preferences
- Mark recommendation as complete

### Backend Responsibilities (Python FastAPI):

✅ **AI/ML Services:**
- Embedding generation (OpenAI/Google)
- Vector search (RAG)
- LLM calls (GPT-4o, GPT-4o-mini)
- Image analysis (GPT-4 Vision)
- Natural language parsing

✅ **Complex Calculations:**
- Progressive overload analysis
- Volume management checks
- Compliance scoring
- 1RM estimates (Epley formula)
- TDEE calculations

✅ **Batch Processing:**
- Weekly recommendation generation
- Workout plan generation
- Nutrition plan generation
- Embedding updates (async queue)

✅ **External Integrations:**
- Garmin API sync
- Strava API sync
- Future: Fitbit, MyFitnessPal

✅ **Background Jobs (Celery):**
- Daily summary generation
- Weekly analytics
- Plan auto-adjustments
- Reminder notifications

### Architecture Diagram:

```
┌─────────────────────────────────────────────┐
│           FRONTEND (Next.js)                 │
│  ┌──────────────────────────────────┐       │
│  │  Quick Entry Modal               │       │
│  │  - Voice/Text/Photo capture      │       │
│  │  - Real-time validation          │       │
│  └──────────────────────────────────┘       │
│                ↓                             │
│  ┌──────────────────────────────────┐       │
│  │  API Routes (/api/...)           │       │
│  │  - Simple CRUD → Supabase        │       │
│  │  - Complex ops → Python Backend  │       │
│  └──────────────────────────────────┘       │
└─────────────────────────────────────────────┘
               ↓               ↓
    ┌──────────────┐   ┌─────────────────────┐
    │   Supabase   │   │  Python Backend     │
    │  PostgreSQL  │   │  (FastAPI)          │
    │  + pgvector  │   │                     │
    │              │   │ ┌─────────────────┐ │
    │  - profiles  │←──│ │ RAG Service     │ │
    │  - workouts  │   │ │ - Embedding gen │ │
    │  - meals     │   │ │ - Vector search │ │
    │  - plans     │   │ └─────────────────┘ │
    │  - embeddings│   │                     │
    │              │   │ ┌─────────────────┐ │
    │              │   │ │ AI Coach        │ │
    │              │   │ │ - GPT-4o calls  │ │
    │              │   │ │ - Context build │ │
    │              │   │ └─────────────────┘ │
    │              │   │                     │
    │              │   │ ┌─────────────────┐ │
    │              │   │ │ Plan Generator  │ │
    │              │   │ │ - Workouts      │ │
    │              │   │ │ - Nutrition     │ │
    │              │   │ └─────────────────┘ │
    │              │   │                     │
    │              │   │ ┌─────────────────┐ │
    │              │   │ │ Celery Worker   │ │
    │              │   │ │ - Daily jobs    │ │
    │              │   │ │ - Embeddings    │ │
    │              │   │ └─────────────────┘ │
    └──────────────┘   └─────────────────────┘
```

---

## ✅ PART 6: TESTING & VERIFICATION STRATEGY

### 6.1 Unit Tests

**Backend (pytest):**
```python
# Test embedding generation
def test_generate_embedding():
    text = "Completed 5x5 squats at 225lbs"
    embedding = generate_embedding(text)
    assert len(embedding) == 1536
    assert all(isinstance(x, float) for x in embedding)

# Test context building
def test_build_coach_context():
    context = build_comprehensive_context(user_id="test-123", query="Should I increase weight?")
    assert "profile" in context
    assert "recent_performance" in context
    assert "relevant_memories" in context
    assert len(context["relevant_memories"]) <= 10

# Test progressive overload logic
def test_progressive_overload_recommendation():
    # User's last 3 weeks: 185x10 RPE 7, 185x10 RPE 7, 185x10 RPE 6.5
    should_increase = check_progressive_overload(
        exercise="Bench Press",
        recent_sets=[
            {"weight": 185, "reps": 10, "rpe": 7},
            {"weight": 185, "reps": 10, "rpe": 7},
            {"weight": 185, "reps": 10, "rpe": 6.5}
        ]
    )
    assert should_increase == True
    assert get_recommended_increase() == 5  # lbs
```

**Frontend (Jest + React Testing Library):**
```typescript
// Test Quick Entry Modal
test('Quick Entry - text input creates workout', async () => {
  render(<QuickEntryModal />)

  const input = screen.getByPlaceholderText('Type here or use voice')
  fireEvent.change(input, { target: { value: 'just finished leg day' } })
  fireEvent.submit(input)

  await waitFor(() => {
    expect(screen.getByText('Leg Day logged!')).toBeInTheDocument()
  })
})

// Test Plan vs Actual display
test('Shows compliance score correctly', () => {
  const props = {
    plannedCalories: 2000,
    actualCalories: 2050,
    plannedProtein: 150,
    actualProtein: 145
  }

  render(<ComplianceCard {...props} />)

  expect(screen.getByText('97%')).toBeInTheDocument() // compliance score
})
```

### 6.2 Integration Tests

**Test Full User Flows:**
```python
# Test: User completes onboarding → Gets personalized plan
def test_onboarding_to_plan_generation():
    # 1. Create user profile
    user = create_test_user({
        "age": 28,
        "weight_lbs": 180,
        "height_inches": 72,
        "goal": "build_muscle",
        "training_frequency": 4
    })

    # 2. Trigger plan generation
    response = client.post(f"/api/v1/plans/generate/{user.id}")
    assert response.status_code == 200

    # 3. Verify workout plan created
    workout_plan = get_workout_program(user.id)
    assert workout_plan is not None
    assert workout_plan.training_days_per_week == 4
    assert workout_plan.goal == "hypertrophy"

    # 4. Verify nutrition plan created
    nutrition_plan = get_nutrition_program(user.id)
    assert nutrition_plan is not None
    assert nutrition_plan.goal == "bulk"
    assert nutrition_plan.daily_calorie_target > 2500  # Bulking calories

# Test: User logs workout → Coach provides feedback
def test_workout_logging_triggers_coach_feedback():
    user_id = "test-user-123"

    # 1. Log workout
    workout = create_workout_log({
        "user_id": user_id,
        "exercises": [
            {"name": "Squat", "sets": [{"weight": 225, "reps": 5, "rpe": 6}] * 5}
        ]
    })

    # 2. Check if coach recommendation generated
    recommendations = get_recommendations(user_id)
    assert len(recommendations) > 0

    # 3. Verify recommendation is relevant
    squat_rec = next((r for r in recommendations if "squat" in r.title.lower()), None)
    assert squat_rec is not None
    assert "increase" in squat_rec.description.lower()  # RPE 6 = room to increase
```

### 6.3 Manual Testing Checklist

**Critical User Flows:**
- [ ] New user onboarding (profile → goals → preferences → plan generation)
- [ ] Quick entry via text ("just had 3 eggs and toast")
- [ ] Quick entry via photo (meal plate)
- [ ] Quick entry via photo (workout summary screenshot)
- [ ] Start planned workout → complete → log all sets → rate
- [ ] Log unplanned workout
- [ ] Log planned meal with one tap
- [ ] Log unplanned meal
- [ ] Ask coach a question → get contextual response
- [ ] Coach generates weekly recommendations
- [ ] Accept coach recommendation → plan updates
- [ ] View progress charts (strength trends)
- [ ] View plan vs actual compliance
- [ ] Edit nutrition plan
- [ ] Edit workout plan
- [ ] Garmin sync → activities appear
- [ ] Strava sync → activities appear

**Edge Cases:**
- [ ] User skips workout → coach asks why
- [ ] User logs way over calories → coach flags it
- [ ] User reports injury → coach adjusts plan
- [ ] User logs same meal 3 days in a row → coach suggests variety
- [ ] User misses 3 workouts → coach asks about barriers
- [ ] Photo is blurry → AI can't parse → ask for clarification

### 6.4 Performance Benchmarks

**Backend Response Times:**
- Embedding generation: < 500ms
- RAG search: < 200ms
- Coach response (simple): < 2s
- Coach response (complex): < 5s
- Plan generation: < 10s
- Photo analysis: < 3s

**Frontend Load Times:**
- Dashboard initial load: < 1.5s
- Quick entry modal open: < 100ms
- Chart rendering: < 500ms
- Page transitions: < 200ms

**Database Query Optimization:**
- Use indexes on user_id, created_at
- Limit queries to last 30 days for performance
- Cache frequently accessed data (profile, active plans)
- Batch embed generation (queue system)

---

## 🚀 PART 7: IMPLEMENTATION ROADMAP

### Phase 1: Foundation (Week 1-2)
**Goal:** Database restructure, basic RAG, simple AI coach

✅ **Week 1:**
- [ ] Add pgvector extension to Supabase
- [ ] Create new tables (planned_workouts, planned_meals, embeddings, etc.)
- [ ] Migrate existing data to new schema
- [ ] Set up Python backend embedding service
- [ ] Test embedding generation + storage

✅ **Week 2:**
- [ ] Implement RAG search function
- [ ] Create basic coach personas (system prompts)
- [ ] Build context builder (profile + recent data + RAG)
- [ ] Test end-to-end: user query → context → LLM → response
- [ ] Deploy Python backend to Railway

### Phase 2: Quick Entry (Week 3-4)
**Goal:** Make data entry effortless

✅ **Week 3:**
- [ ] Build Quick Entry modal UI
- [ ] Implement text/voice input parsing
- [ ] Add photo capture (camera + upload)
- [ ] Integrate GPT-4 Vision for meal photos
- [ ] Test natural language parsing ("just had coffee")

✅ **Week 4:**
- [ ] Implement workout summary photo parsing
- [ ] Add confirmation modals before saving
- [ ] Build auto-categorization logic
- [ ] Test all entry methods end-to-end
- [ ] Add toast notifications for feedback

### Phase 3: Planning System (Week 5-6)
**Goal:** AI generates personalized plans

✅ **Week 5:**
- [ ] Build workout plan generator (AI)
- [ ] Create nutrition plan generator (AI)
- [ ] Implement TDEE calculator
- [ ] Add progressive overload logic
- [ ] Test plan generation for different goals

✅ **Week 6:**
- [ ] Build Nutrition Planner page
- [ ] Build Workout Planner page
- [ ] Add plan editing capabilities
- [ ] Implement one-tap logging from plans
- [ ] Test plan vs actual tracking

### Phase 4: Adaptive Coaching (Week 7-8)
**Goal:** Coach learns and adapts

✅ **Week 7:**
- [ ] Implement weekly analysis job (Celery)
- [ ] Build recommendation engine
- [ ] Add compliance scoring
- [ ] Create recommendation UI
- [ ] Test adaptive recommendations

✅ **Week 8:**
- [ ] Enhanced coach chat with actions
- [ ] Add "Accept recommendation" → auto-update plan
- [ ] Implement feedback loop (user rates recommendations)
- [ ] Test coach improving over time
- [ ] Add coach insights to dashboard

### Phase 5: Analytics & Polish (Week 9-10)
**Goal:** Visualization and UX refinement

✅ **Week 9:**
- [ ] Redesign dashboard with new layout
- [ ] Add progress charts (strength trends)
- [ ] Build plan vs actual comparison views
- [ ] Add goal progress tracking
- [ ] Implement streak tracking

✅ **Week 10:**
- [ ] UI polish (animations, transitions)
- [ ] Mobile responsiveness
- [ ] Performance optimization
- [ ] Bug fixes
- [ ] User testing + feedback

---

## 📋 PART 8: EXAMPLE IMPLEMENTATION

### Example: Quick Entry Text Parsing

**Frontend (Next.js):**
```typescript
// components/QuickEntry.tsx
'use client'

import { useState } from 'react'
import { useToast } from '@/hooks/use-toast'

export function QuickEntry() {
  const [input, setInput] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const { toast } = useToast()

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault()
    setIsProcessing(true)

    try {
      const response = await fetch('/api/quick-entry/parse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input })
      })

      const result = await response.json()

      if (result.type === 'meal') {
        // Show meal confirmation modal
        toast({
          title: '✅ Meal logged!',
          description: `${result.calories} cal, ${result.protein}g protein`
        })
      } else if (result.type === 'workout') {
        toast({
          title: '✅ Workout logged!',
          description: `${result.exercise_count} exercises`
        })
      }

      setInput('')
    } catch (error) {
      toast({
        title: 'Error',
        description: 'Could not parse entry',
        variant: 'destructive'
      })
    } finally {
      setIsProcessing(false)
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        placeholder="Type what you just did..."
        disabled={isProcessing}
      />
      <button type="submit" disabled={isProcessing || !input}>
        {isProcessing ? 'Processing...' : 'Add'}
      </button>
    </form>
  )
}
```

**Backend API Route (Next.js):**
```typescript
// app/api/quick-entry/parse/route.ts
import { NextRequest, NextResponse } from 'next/server'
import { createClient } from '@/lib/supabase/server'
import { API_BASE_URL } from '@/lib/api-config'

export async function POST(request: NextRequest) {
  const supabase = await createClient()
  const { data: { user } } = await supabase.auth.getUser()

  if (!user) {
    return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
  }

  const { text } = await request.json()

  // Call Python backend for parsing
  const response = await fetch(`${API_BASE_URL}/api/v1/quick-entry/parse`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      'X-User-ID': user.id
    },
    body: JSON.stringify({ text })
  })

  const parsed = await response.json()

  // Save to database based on type
  if (parsed.type === 'meal') {
    const { data: meal } = await supabase
      .from('meal_logs')
      .insert({
        user_id: user.id,
        name: parsed.name,
        category: parsed.category,
        calories: parsed.calories,
        protein_g: parsed.protein_g,
        carbs_g: parsed.carbs_g,
        fat_g: parsed.fat_g,
        logged_at: new Date().toISOString()
      })
      .select()
      .single()

    return NextResponse.json({ type: 'meal', ...parsed })
  } else if (parsed.type === 'workout') {
    const { data: workout } = await supabase
      .from('actual_workouts')
      .insert({
        user_id: user.id,
        started_at: new Date().toISOString(),
        completed_at: new Date().toISOString(),
        notes: parsed.notes
      })
      .select()
      .single()

    return NextResponse.json({ type: 'workout', ...parsed })
  }
}
```

**Python Backend Service:**
```python
# app/api/v1/quick_entry.py
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from openai import OpenAI

router = APIRouter()
client = OpenAI()

class QuickEntryRequest(BaseModel):
    text: str

@router.post("/parse")
async def parse_quick_entry(
    request: QuickEntryRequest,
    user_id: str = Depends(get_current_user)
):
    """
    Parse natural language input and classify as meal or workout
    """

    # Use GPT-4o-mini for fast, cheap parsing
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": """You are a fitness app parser. Classify user input as either:
                - 'meal' (food/drink consumed)
                - 'workout' (exercise completed)

                For meals, extract: name, category, estimated calories and macros
                For workouts, extract: exercise name, sets, reps, weight

                Return JSON only."""
            },
            {
                "role": "user",
                "content": request.text
            }
        ],
        response_format={ "type": "json_object" }
    )

    parsed = json.loads(response.choices[0].message.content)

    return parsed

# Example responses:
# Input: "just had 3 eggs and toast"
# Output: {
#   "type": "meal",
#   "name": "Eggs and toast",
#   "category": "breakfast",
#   "calories": 450,
#   "protein_g": 25,
#   "carbs_g": 40,
#   "fat_g": 20
# }

# Input: "finished bench press 5 sets of 8 at 185"
# Output: {
#   "type": "workout",
#   "exercise_name": "Bench Press",
#   "sets": 5,
#   "reps": 8,
#   "weight_lbs": 185
# }
```

---

## 🎯 SUCCESS METRICS

**User Engagement:**
- Daily active users: 70%+ of registered users
- Avg session time: 8+ minutes
- Quick entry usage: 80%+ of entries via quick entry
- Coach chat engagement: 50%+ users ask coach weekly

**Plan Adherence:**
- Workout compliance: 85%+ (follow planned workouts)
- Nutrition compliance: 80%+ (hit macro targets)
- Streak retention: 60%+ users maintain 7+ day streak

**AI Performance:**
- Quick entry accuracy: 90%+ correctly categorized
- Photo recognition accuracy: 85%+ for meals
- Coach response relevance: 4.5+/5.0 user rating
- Recommendation acceptance: 70%+ users accept AI recommendations

**Technical Performance:**
- Dashboard load: < 1.5s
- Quick entry response: < 2s
- Coach response: < 3s
- 99.9% uptime

---

## 💰 COST ESTIMATE

**OpenAI API (Monthly @ 1000 users):**
- Embeddings: $0.02/1M tokens × 10M tokens = $0.20
- GPT-4o-mini (coach): $0.15/1M input, $0.60/1M output × 50M = $37.50
- GPT-4 Vision (photos): $10/1M input tokens × 5M = $50
- **Total: ~$88/month**

**Google Gemini (Alternative - FREE tier):**
- Embeddings: FREE (1500 requests/day)
- Gemini 1.5 Flash: FREE (15 RPM, 1M tokens/day)
- **Total: $0/month** (if staying within limits)

**Infrastructure:**
- Railway (Python backend): $5-20/month
- Supabase (database + storage): Free tier (up to 500MB)
- Vercel (frontend): Free tier
- **Total: $5-20/month**

**GRAND TOTAL: $5-108/month** (depending on AI provider choice)

---

## 🔐 SECURITY & PRIVACY

**Data Protection:**
- All user data encrypted at rest (Supabase)
- HTTPS for all API calls
- Row-level security (RLS) in Supabase
- User data never shared with AI provider (anonymized context)

**AI Safety:**
- Content moderation for coach responses
- Rate limiting on API calls
- User can delete conversation history
- Clear AI disclaimer ("AI coach, not medical advice")

---

## 🚢 DEPLOYMENT CHECKLIST

- [ ] Supabase migrations applied
- [ ] Python backend deployed to Railway
- [ ] Environment variables configured
- [ ] Frontend deployed to Vercel
- [ ] DNS configured for custom domain
- [ ] SSL certificates active
- [ ] API rate limits configured
- [ ] Error tracking (Sentry) enabled
- [ ] Analytics (Posthog) enabled
- [ ] Backup strategy configured
- [ ] Monitoring dashboards set up

---

## 📝 CONCLUSION

This plan transforms Wagner Coach from a basic fitness tracker into an **intelligent, adaptive AI coach** that:

1. **Learns** from every user interaction via RAG embeddings
2. **Plans** personalized workouts and nutrition based on goals
3. **Adapts** recommendations based on user compliance and feedback
4. **Simplifies** data entry with text/voice/photo input
5. **Coaches** like a real trainer and nutritionist

**Key Differentiators:**
- ✅ Effortless entry (voice, photo, text)
- ✅ Context-aware AI that remembers everything
- ✅ Plan vs actual tracking with auto-adjustments
- ✅ Progressive overload and volume management
- ✅ Personalized meal plans with recipes
- ✅ Real trainer/nutritionist personas

**Next Step:** Start with Phase 1 (Database + RAG foundation) and iterate from there.

---

**Version:** 1.0
**Last Updated:** September 30, 2025
**Status:** Ready for Implementation 🚀
