# Wagner Coach - Complete Feature Documentation

**Last Updated:** 2025-10-09
**Version:** 1.0 (Post-Cleanup)

This document describes ALL features currently implemented and accessible in the Wagner Coach fitness application. This is the single source of truth for what the app can do.

---

## 🎯 Core Philosophy

Wagner Coach is an **AI-powered fitness & nutrition coaching platform** that combines:
- **Multimodal AI Input** - Text, voice, and photo meal logging
- **RAG-Powered Coach** - Semantic search across all user data
- **Cost-Optimized AI** - $0.50/user/month (95% cheaper than competitors)
- **Instant Personalization** - AI understands context from day 1

---

## 🔐 Authentication & Onboarding

### Features
- **Email/Password Authentication** via Supabase Auth
- **Onboarding Flow** - Collect basic user info (name, goal)
- **Goal Selection** - 3 fitness goals:
  - Build Muscle (hypertrophy focus)
  - Lose Weight (fat loss focus)
  - Gain Strength (powerlifting focus)

### Pages
- `/auth` - Login/signup page
- `/auth/onboarding` - New user onboarding

### Database Tables
- `profiles` - User profiles with name, goal, preferences

---

## 🏠 Dashboard

### Features
- **Nutrition Summary** - Today's calories, protein, carbs, fat
- **Activity Summary** - Today's workouts and activity count
- **Event Countdown** - Days until primary goal event (race, competition)
- **Daily Recommendations** - AI-generated personalized tips from consultation
- **Quick Actions** - 3 primary actions + 2 secondary:
  - **Primary Actions** (large, prominent):
    - Log Meal → `/nutrition/log` (manual entry)
    - Scan Meal → `/meal-scan` (AI photo analysis)
    - Ask Coach → `/coach-v2` (AI chat)
  - **Secondary Actions** (smaller):
    - Log Activity → `/activities/log`
    - Start Consultation → `/consultation`

### Pages
- `/dashboard` - Main landing page after login

### Database Tables
- `meal_logs`, `activities`, `events`, `consultation_daily_recommendations`

---

## 🤖 AI Coach (Unified Chat Interface)

### Features
- **Unified Chat** - Single interface for all AI coaching needs
- **Auto-Log Detection** - AI automatically detects when user is logging data (meal, activity)
- **Preview Cards** - Shows structured preview before saving logs
- **Streaming Responses** - Real-time AI response streaming
- **RAG Context** - Retrieves relevant user data for personalized responses
- **Two Logging Modes**:
  - **Preview Mode** - User reviews and edits before saving (default)
  - **Auto-Save Mode** - Logs saved instantly, editable later
- **Chat History** - Persistent conversations with retrieval

### Pages
- `/coach-v2` - Unified coach chat interface (SimpleChatClient)

### Backend Endpoints
- `POST /api/v1/coach/chat` - Send message, get streaming response
- `POST /api/v1/coach/confirm-log` - Confirm and save log preview
- `POST /api/v1/coach/cancel-log` - Cancel log preview
- `GET /api/v1/coach/conversations` - Get user's conversation history
- `GET /api/v1/coach/conversations/{id}` - Get specific conversation with messages

### Database Tables
- `coach_conversations` - Conversation metadata
- `coach_messages` - Individual chat messages
- `multimodal_embeddings` - Vectorized messages for RAG
- `user_preferences` - Stores auto_log_enabled preference

---

## 📸 Meal Scan (AI Photo Analysis)

### Features
- **Photo Upload** - Take or upload meal photo
- **AI Vision Analysis** - Identifies foods and estimates nutrition
- **Structured Preview** - Shows detected foods with quantities
- **Save to History** - Logs meal with nutrition data

### Pages
- `/meal-scan` - MealScanClient for AI meal photo analysis

### Backend Endpoints
- `POST /api/v1/quick-entry/image` - Process meal photo with AI

### Database Tables
- `meal_logs`, `meal_foods`, `foods_enhanced`

---

## 🍽️ Nutrition Tracking

### Manual Meal Logging

#### Features
- **Meal Type Selection** - Breakfast, lunch, dinner, snack, pre-workout, post-workout
- **Food Search** - Search 884,603 foods from comprehensive database
- **Recent Foods** - Quick access to frequently logged foods
- **Quantity & Units** - Flexible portions (g, oz, cup, serving, etc.)
- **Auto-Calculation** - Nutrition totals calculated automatically
- **Notes** - Optional meal notes (up to 500 characters)

#### Pages
- `/nutrition/log` - Manual meal logging form with food search

### Nutrition Dashboard

#### Features
- **Daily View** - View meals for any date
- **Date Navigation** - Previous/next day buttons with "Today" shortcut
- **Nutrition Summary** - Daily totals (calories, protein, carbs, fat, fiber)
- **Meals by Category** - Grouped by meal type (breakfast, lunch, etc.)
- **Meal Actions**:
  - **Edit** - Modify meal details and foods
  - **Delete** - Remove meal from history
  - **Copy** - Duplicate meal to another date
- **Quick Actions** - Copy meals from previous day

#### Pages
- `/nutrition` - Main nutrition dashboard (NutritionDashboard)
- `/nutrition/edit/[id]` - Edit existing meal
- `/nutrition/history` - Historical nutrition view (alternate layout)
- `/nutrition/add` - Alternative meal entry form

### Meal Templates

#### Features
- **Save Frequent Meals** - Create reusable meal templates
- **Recursive Templates** - Templates can contain other templates
- **Quick Logging** - Log entire meals with one tap

#### Backend Endpoints
- `GET /api/v1/templates` - List user's meal templates
- `POST /api/v1/templates` - Create new template
- `GET /api/v1/templates/{id}` - Get template details

#### Database Tables
- `meal_templates`, `meal_template_items`

### Backend Endpoints
- `POST /api/v1/meals` - Create meal log
- `GET /api/v1/meals` - Get user's meals (with date filtering)
- `GET /api/v1/meals/{id}` - Get specific meal
- `PATCH /api/v1/meals/{id}` - Update meal
- `DELETE /api/v1/meals/{id}` - Delete meal
- `GET /api/v1/foods/search` - Search food database
- `GET /api/v1/foods/recent` - Get recently logged foods

### Database Tables
- `meal_logs` - Meal metadata (category, time, source)
- `meal_foods` - Foods in each meal with quantities
- `foods_enhanced` - Comprehensive food database (884,603 foods)
- `user_food_popularity` - Tracks frequently logged foods

---

## 🏃 Activity Tracking

### Activity Logging

#### Features
- **12 Activity Types** - Running, cycling, swimming, walking, hiking, strength training, yoga, pilates, HIIT, cardio, sports, other
- **Dynamic Forms** - Different fields based on activity type:
  - **Cardio** (run, bike, swim, walk, hike): Distance, duration, pace, heart rate, elevation
  - **Strength** (weight training): Exercises, sets, reps, weight per set
  - **Flexibility** (yoga, pilates): Duration, difficulty, focus areas
  - **HIIT/Cardio**: Duration, intervals, intensity, calories
  - **Sports**: Sport type, duration, intensity, score
- **Auto-Calculations** - Pace, calories, training load
- **Notes** - Activity notes (up to 1000 characters)

#### Pages
- `/activities/log` - Dynamic activity logging form

### Daily Activities View

#### Features
- **Date Navigation** - View activities for any date
- **Daily Summary** - Total workouts, duration, calories, distance
- **Activity List** - All activities for selected date with:
  - Activity icon (🏃, 🚴, 🏊, etc.)
  - Duration, distance, calories, heart rate
  - Notes preview
  - Edit and delete actions
- **Empty States** - Helpful prompts for days with no activities

#### Pages
- `/activities/daily` - Daily activities view (ActivitiesDailyClient)
- `/activities/edit/[id]` - Edit existing activity
- `/activities/add` - Alternative activity entry (ManualActivityForm)

### Activity Exercises & Sets

#### Features
- **Exercise Tracking** - Log individual exercises in strength workouts
- **Set Tracking** - Track sets with weight, reps, rest periods
- **Progressive Overload** - View historical data for each exercise

#### Database Tables
- `activity_exercises` - Exercises within strength training activities
- `activity_sets` - Individual sets with weight/reps data

### Backend Endpoints
- `POST /api/v1/activities` - Create activity log
- `GET /api/v1/activities` - Get user's activities (with date filtering)
- `GET /api/v1/activities/{id}` - Get specific activity
- `PATCH /api/v1/activities/{id}` - Update activity
- `DELETE /api/v1/activities/{id}` - Delete activity

### Database Tables
- `activities` - Activity metadata with **sport-specific fields**:
  - `distance_meters`, `pace_seconds_per_km`, `elevation_gain_meters` (cardio)
  - `sport_type`, `team_score`, `opponent_score` (sports)
  - `intervals_count`, `work_seconds`, `rest_seconds` (HIIT)
  - `average_heart_rate`, `max_heart_rate`, `calories`
  - `difficulty`, `focus_areas` (yoga/pilates)
- `activity_exercises` - Exercises in strength workouts
- `activity_sets` - Sets with weight/reps

---

## 🎯 Events & Calendar

### Features
- **Event Creation** - Create goal events (races, competitions, milestones)
- **Event Types** - Race, competition, assessment, milestone, other
- **Primary Goal** - One primary event for countdown and program periodization
- **Event Details** - Name, date, type, distance, location, notes
- **Event Edit** - Modify event details
- **Event Delete** - Remove events
- **Event List** - View all upcoming and past events

### Pages
- `/events` - Event list page with primary goal highlight
- `/events/create` - Create new event
- `/events/[id]` - Event details page
- `/events/[id]/edit` - Edit existing event

### Backend Endpoints
- `POST /api/v1/events` - Create event
- `GET /api/v1/events` - Get user's events
- `GET /api/v1/events/{id}` - Get specific event
- `PATCH /api/v1/events/{id}` - Update event
- `DELETE /api/v1/events/{id}` - Delete event
- `POST /api/v1/events/{id}/set-primary` - Set as primary goal event

### Database Tables
- `events` - Goal events (races, competitions)
- `event_checkins` - Weekly check-ins for event preparation

---

## 🧠 AI Consultation System

### Features
- **4 Specialist Types**:
  - **Strength Coach** - Resistance training, progressive overload
  - **Endurance Coach** - Cardio, stamina, aerobic capacity
  - **Nutrition Coach** - Meal planning, macros, eating habits
  - **Recovery Coach** - Sleep, stress, injury prevention
- **Adaptive Conversations** - AI adjusts questions based on responses
- **Conversation Stages**:
  1. Greeting & Goal Understanding
  2. Assessment (specialist-specific questions)
  3. Recommendations (personalized advice)
  4. Goal Setting & Action Plan
- **Structured Data Extraction** - AI extracts key info (goals, injuries, schedule, etc.)
- **Daily Recommendations** - AI generates daily tips based on consultation
- **Progress Tracking** - Visual progress bar shows completion percentage
- **Session Resume** - Continue incomplete consultations
- **Consultation History** - View past consultations and extracted data

### Pages
- `/consultation` - Main consultation interface with specialist selection and chat

### Backend Endpoints
- `POST /api/v1/consultation/start` - Start new consultation session
- `POST /api/v1/consultation/message` - Send message, get streaming response
- `GET /api/v1/consultation/active` - Check for active consultation session
- `POST /api/v1/consultation/complete` - Mark consultation as complete
- `GET /api/v1/consultation/history` - Get consultation history with extractions
- `GET /api/v1/consultation/daily-recommendations` - Get today's AI-generated tips

### Database Tables
- `consultation_sessions` - Consultation metadata with specialist type, stage, progress
- `consultation_messages` - Chat messages within consultation
- `consultation_extractions` - Structured data extracted by AI (goals, injuries, schedule)
- `consultation_daily_recommendations` - AI-generated daily tips

---

## 📅 AI Program Generation

### Features
- **12-Week Programs** - Fully personalized 84-day training & nutrition plans
- **Consultation Required** - Must complete consultation before generating program
- **Event-Specific Periodization** - Programs tailored to primary goal event
- **Progressive Overload** - Intensity increases over 12 weeks
- **Daily Workouts** - Exercises, sets, reps, rest periods
- **Daily Meals** - Breakfast, lunch, dinner, snacks with macros
- **Weekly Structure** - Training days, rest days, active recovery
- **Program Calendar** - Visual 12-week calendar view
- **Day Detail View** - See full workout and meal plan for specific day

### Pages
- `/programs` - Program list and creation (ProgramsClient)
- `/programs/create` - Generate new AI program
- `/programs/[program_id]` - Program overview with calendar
- `/programs/[program_id]/day/[day_number]` - Detailed day view with workout & meals

### Backend Endpoints
- `POST /api/v1/programs/generate` - Generate AI program (requires consultation)
- `GET /api/v1/programs` - Get user's programs
- `GET /api/v1/programs/{id}` - Get program details
- `GET /api/v1/programs/{id}/day/{day_number}` - Get day details

### Database Tables
- `ai_generated_programs` - Program metadata (name, event, start/end date)
- `ai_program_days` - Daily structure (workout day, rest day, active recovery)
- `ai_program_workouts` - Daily workout plans with exercises
- `ai_program_meals` - Daily meal plans with foods and macros

---

## ❤️ Recovery Hub (Garmin Integration)

### Features
- **9 Recovery Tabs**:
  1. **Today** - Overall recovery summary
  2. **Sleep** - Sleep duration, quality, stages, score
  3. **HRV** (Heart Rate Variability) - Morning HRV trends
  4. **Readiness** - Overall readiness score
  5. **Stress** - Stress levels throughout day
  6. **Body Battery** - Garmin's energy reserve metric
  7. **Training Load** - 7-day training load and recovery time
  8. **Correlations** - HRV vs training load, sleep vs performance
  9. **History** - Historical recovery data with trends
- **Empty States** - All tabs currently show empty states directing to Garmin connection
- **Garmin Connection** - OAuth flow to connect Garmin device
- **Auto-Sync** - Daily sync of health data from Garmin
- **AI Coach Integration** - Recovery data available to coach for personalized recommendations

### Pages
- `/recovery` - Recovery hub with 9 tabs (all currently empty states)
- `/profile` - Garmin connection via GarminConnection component
- `/settings` - Garmin connection via GarminConnection component

### Backend Endpoints
- `POST /api/v1/garmin/request-token` - Start Garmin OAuth flow
- `POST /api/v1/garmin/exchange-token` - Complete OAuth and save tokens
- `POST /api/v1/garmin/disconnect` - Disconnect Garmin account
- `GET /api/v1/garmin/status` - Check Garmin connection status
- `POST /api/v1/garmin/webhook` - Receive health data from Garmin (background sync)
- `POST /api/v1/garmin/deauthorization` - Handle Garmin account deletion

### Database Tables
- `garmin_tokens` - OAuth tokens for Garmin API access
- `garmin_health_snapshot` - Daily health metrics from Garmin
- `garmin_daily_summaries` - Daily summary stats (sleep, steps, HR)
- `garmin_sleep_data` - Detailed sleep stages and quality
- `garmin_stress_data` - Stress levels throughout day
- `garmin_hrv_data` - Heart rate variability readings
- `garmin_body_battery_data` - Garmin Body Battery energy reserve
- `garmin_respiration_data` - Breathing rate data

---

## 👤 Profile & Settings

### Profile Features
- **User Stats** - Total meals logged, activities logged, programs completed
- **Integrations** - Garmin connection status with connect/disconnect
- **Unit System Toggle** - Metric (kg/km) vs Imperial (lbs/mi)
- **Profile Edit** - Update name, email, preferences

### Settings Features
- **Goal Selection** - Change fitness goal (build muscle, lose weight, gain strength)
- **Coach Behavior** - Toggle auto-log mode (preview vs auto-save)
- **Garmin Integration** - Connect/disconnect Garmin device
- **Sign Out** - Log out of application

### Pages
- `/profile` - Main profile page with stats and integrations
- `/profile/edit` - Edit profile information
- `/profile/preferences` - Detailed preference settings
- `/settings` - Settings page with goal, coach behavior, Garmin

### Database Tables
- `profiles` - User profiles with name, goal, unit_system
- `user_preferences` - Extended preferences including auto_log_enabled

---

## 🔄 Background Jobs & Workers

### Features
- **Embedding Generation** - Vectorize meals, activities, coach messages for RAG
- **Celery Workers** - Background task processing
- **Daily Recommendations** - Generate daily tips from consultation data

### Backend Endpoints
- `POST /api/v1/background/generate-embeddings` - Trigger embedding generation
- `GET /api/v1/background/job-status/{job_id}` - Check job status

### Database Tables
- `multimodal_embeddings` - Vector embeddings for semantic search (pgvector)

---

## 🔍 Semantic Search (RAG)

### Features
- **Multimodal Embeddings** - Vectorize all user data (meals, activities, coach messages)
- **Semantic Search** - Find relevant context for AI coach
- **pgvector Extension** - Efficient vector similarity search
- **FREE Embedding Model** - `sentence-transformers/all-MiniLM-L6-v2` (no API cost)

### Backend Services
- `MultimodalEmbeddingService` - Generate embeddings for all content types
- `SemanticSearchService` - Query embeddings for relevant context

### Database Tables
- `multimodal_embeddings` - Vectorized content with metadata

---

## 🧪 Debug & Testing

### Features
- **Health Checks** - API status monitoring
- **Groq Testing** - Test Groq AI model integration
- **Debug Endpoints** - Development-only debugging tools

### Backend Endpoints
- `GET /api/v1/health` - Health check
- `POST /api/v1/test-groq/chat` - Test Groq AI integration
- `GET /api/v1/debug/*` - Various debug endpoints (remove in production)

---

## 📱 Bottom Navigation (Always Visible)

### 6 Main Tabs
1. **Dashboard** → `/dashboard` - Home screen with quick actions
2. **Events** → `/events` - Goal events and calendar
3. **Recovery** → `/recovery` - Garmin health data hub
4. **Coach** → `/coach-v2` - AI coach chat
5. **Scan** → `/meal-scan` - AI photo meal logging
6. **Profile** → `/profile` - User profile and settings

---

## 🗄️ Complete Database Schema (46 Tables)

### Active Tables (33 - Keep All)
1. `profiles` - User profiles
2. `user_preferences` - Extended user preferences
3. `meal_logs` - Meal metadata
4. `meal_foods` - Foods in meals
5. `meal_templates` - Reusable meal templates
6. `meal_template_items` - Foods in templates
7. `foods_enhanced` - Comprehensive food database (884,603 foods)
8. `user_food_popularity` - Frequently logged foods
9. `activities` - Activity logs with sport-specific fields
10. `activity_exercises` - Exercises in strength workouts
11. `activity_sets` - Sets with weight/reps
12. `events` - Goal events (races, competitions)
13. `event_checkins` - Weekly event prep check-ins
14. `coach_conversations` - Coach chat conversations
15. `coach_messages` - Individual chat messages
16. `consultation_sessions` - AI consultation sessions
17. `consultation_messages` - Consultation chat messages
18. `consultation_extractions` - Structured consultation data
19. `consultation_daily_recommendations` - AI daily tips
20. `ai_generated_programs` - 12-week AI programs
21. `ai_program_days` - Daily program structure
22. `ai_program_workouts` - Daily workouts
23. `ai_program_meals` - Daily meal plans
24. `multimodal_embeddings` - Vector embeddings for RAG
25. `garmin_tokens` - Garmin OAuth tokens
26. `garmin_health_snapshot` - Daily health metrics
27. `garmin_daily_summaries` - Daily Garmin summaries
28. `garmin_sleep_data` - Sleep stages and quality
29. `garmin_stress_data` - Stress levels
30. `garmin_hrv_data` - Heart rate variability
31. `garmin_body_battery_data` - Body Battery energy
32. `garmin_respiration_data` - Breathing rate
33. `api_usage_logs` - AI API cost tracking

### Unused Tables (13 - TO BE DELETED)
Run `migrations/DROP_UNUSED_TABLES.sql` to remove:
1. `strava_activities` - Strava removed
2. `strava_auth` - Strava removed
3. `workout_logs` - Old workout system
4. `workout_log_exercises` - Old workout system
5. `workout_sets` - Old workout system
6. `workout_exercises` - Old workout system
7. `workouts` - Old workout system
8. `workout_days` - Old workout system
9. `custom_foods` - Replaced by foods_enhanced
10. `nutrition_goals` - No references
11. `weekly_workout_goals` - No references
12. `coach_tool_calls` - No references
13. `custom_exercises` - No references

---

## 🚀 Tech Stack Summary

### Frontend
- **Next.js 14** - App Router, React Server Components
- **TypeScript** - Strict type safety
- **Tailwind CSS** - Utility-first styling
- **shadcn/ui** - Accessible component library

### Backend
- **FastAPI** - Python async API framework
- **Pydantic** - Data validation
- **Supabase** - PostgreSQL database, Auth, Storage
- **pgvector** - Vector similarity search
- **Celery** - Background task processing
- **Redis** - Task queue & caching

### AI Services
- **FREE Models** - Embeddings (sentence-transformers), Transcription (Whisper Tiny)
- **Groq** - Fast text processing (Llama 3.3 70B, $0.05-0.10/M tokens)
- **OpenRouter** - Image processing (Llama 4 Scout, $0.50-1.00/M tokens)
- **Anthropic Claude** - Complex reasoning (Claude 3.5 Sonnet, $3-15/M tokens)
- **Target Cost** - $0.50/user/month

---

## 📊 Feature Status

### ✅ Fully Implemented & Active
- Authentication & Onboarding
- Dashboard with Quick Actions
- AI Coach (Unified Chat)
- Meal Scan (AI Photo Analysis)
- Manual Meal Logging
- Nutrition Dashboard & History
- Activity Logging (12 types)
- Daily Activities View
- Events & Calendar
- AI Consultation System
- AI Program Generation (12-week)
- Profile & Settings
- Garmin OAuth Integration

### 🚧 Partial Implementation (Empty States)
- Recovery Hub (9 tabs) - Infrastructure ready, awaiting Garmin data sync

### ❌ Removed (Legacy Code Deleted)
- Old Coach (/coach, /quick-entry, /quick-entry-optimized)
- Old Workout Systems (/workout, /workouts)
- Strava Integration (replaced by Garmin)
- Custom Foods/Exercises (replaced by enhanced databases)

---

## 🎯 Future Enhancements (Not Yet Implemented)

These features are NOT currently implemented but are planned:
- Analytics dashboard with progress charts
- Social features (share meals, activities)
- Challenges & competitions
- Premium AI features (video analysis, form check)
- Integration with Apple Health, Google Fit
- Meal plan marketplace
- Personal trainer marketplace

---

## 📝 Notes

- All pages are responsive (mobile, tablet, desktop)
- All forms have loading states, error handling, validation
- All API endpoints have authentication, rate limiting, error responses
- All database tables have RLS (Row Level Security) policies
- All AI calls are logged with cost tracking
- Sport-specific fields in `activities` table are intentionally preserved for future use

---

**END OF FEATURES.MD**
This document represents the complete, cleaned, production-ready Wagner Coach application as of 2025-10-09.
