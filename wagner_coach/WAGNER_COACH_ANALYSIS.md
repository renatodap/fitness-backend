# Wagner Coach - Complete System Analysis

## System Architecture

### Frontend: wagner-coach-clean (Next.js 14)
- Framework: Next.js 14 with App Router
- UI: React + TypeScript + TailwindCSS
- Database: Supabase (PostgreSQL)
- Authentication: Supabase Auth

### Backend: fitness-backend (Python/FastAPI)
- Framework: FastAPI
- Purpose: AI/ML services, integrations
- Port: 8000 (default)
- Base URL: `http://localhost:8000` (dev) or `NEXT_PUBLIC_BACKEND_URL` (prod)

---

## Complete User Flows & Pages

### 1. Authentication Flow
- **Route:** `/auth`
- **CRUD:** Create user account (Supabase Auth)
- **Backend:** None (Supabase native)

### 2. Onboarding Flow
- **Route:** `/auth/onboarding`
- **CRUD:** Create user profile, goals, preferences
- **Components:** BasicInfoStep, GoalsStep, EquipmentStep, PreferencesStep, PersonalizationStep
- **Backend:** Supabase only

### 3. Dashboard
- **Route:** `/dashboard`
- **Read Operations:**
  - User profile
  - Today's activities count
  - Today's meals count
  - Active programs count
  - Upcoming workouts
- **Backend:** Supabase only

### 4. Profile Management
- **Routes:**
  - `/profile` - View profile
  - `/profile/edit` - Edit profile
  - `/profile/goals/add` - Add goals
- **CRUD:**
  - READ: User profile data
  - UPDATE: Profile information
  - CREATE/UPDATE: User goals
- **Backend:** Supabase only

### 5. Activities Flow
- **Routes:**
  - `/activities` - List all activities
  - `/activities/add` - Manual activity entry
  - `/activities/[id]` - View activity details
  - `/activities/edit/[id]` - Edit activity
- **CRUD:**
  - CREATE: New activity (manual entry)
  - READ: Activities list, activity details
  - UPDATE: Edit activity
  - DELETE: Remove activity
- **API Routes:**
  - `/api/activities/sync` - Sync from integrations
  - `/api/activities/garmin` - Import from Garmin
- **Backend Integration:** Garmin sync uses Python backend

### 6. Workouts Flow
- **Routes:**
  - `/workouts` - List workouts
  - `/workouts/builder` - Build custom workout
  - `/workouts/browse` - Browse workout library
  - `/workout` - Start workout
  - `/workout/[id]` - View workout details
  - `/workout/active/[sessionId]` - Active workout session
- **CRUD:**
  - CREATE: Custom workouts, workout sessions
  - READ: Workouts library, workout details, session data
  - UPDATE: Workout progress, exercise sets
  - DELETE: Custom workouts
- **Components:**
  - RestTimer - Workout rest timer
  - PRTracker - Personal records tracking
  - ExerciseHistory - Exercise history view
- **Backend:** Supabase only

### 7. Programs Flow
- **Routes:**
  - `/programs` - List programs
  - `/programs/[id]` - View program details
- **CRUD:**
  - CREATE: User program enrollment
  - READ: Available programs, enrolled programs
  - UPDATE: Program progress
  - DELETE: Remove enrollment
- **Backend:** Supabase only

### 8. Nutrition Flow
- **Routes:**
  - `/nutrition` - Nutrition dashboard
  - `/nutrition/add` - Add meal (3 methods)
  - `/nutrition/edit/[id]` - Edit meal
  - `/nutrition/foods/create` - Create custom food
  - `/nutrition/add-food/[mealId]` - Add food to existing meal
  - `/nutrition/history` - Nutrition history
- **Entry Methods:**
  1. Build from Foods (MealBuilder)
  2. AI Natural Language (NaturalLanguageEntry)
  3. Photo Analysis (PhotoCapture)
- **CRUD:**
  - CREATE: Meals, foods, meal logs
  - READ: Meals history, daily summary, food database
  - UPDATE: Edit meals
  - DELETE: Remove meals
- **API Routes:**
  - `/api/nutrition/meals` - CRUD for meals
  - `/api/nutrition/meals/[id]` - Single meal operations
  - `/api/nutrition/meals/relog` - Re-log meal
  - `/api/nutrition/foods` - CRUD for foods
  - `/api/nutrition/foods/search` - Search food database
  - `/api/nutrition/parse` - Parse natural language
  - `/api/nutrition/analyze-photo` - AI photo analysis
  - `/api/nutrition/dashboard` - Dashboard data
- **Backend Integration:**
  - Python backend for meal parsing (`/api/v1/nutrition/parse`)
  - Fallback to local OpenAI parser if backend unavailable
- **Components:**
  - MealBuilder - Build meals from food database
  - NaturalLanguageEntry - AI-powered text entry
  - PhotoCapture - Camera/upload for AI analysis
  - FoodSearch - Search food database
  - DailySummary - Daily nutrition overview
  - MealList - List of logged meals

### 9. Analytics
- **Route:** `/analytics`
- **CRUD:**
  - READ: Workout analytics, progress trends
- **Components:** WorkoutAnalytics
- **Backend:** Supabase only

### 10. AI Coach
- **Route:** `/coach`
- **API Routes:**
  - `/api/coach` - Chat with AI coach
  - `/api/coach/enhanced` - Enhanced coaching
  - `/api/ai/chat` - AI chat interface
  - `/api/ai/context` - Get AI context (Supabase)
  - `/api/ai/context-backend` - Get AI context (Python backend)
  - `/api/ai/prompt-context` - Get prompt context
- **Backend Integration:**
  - Python backend RAG service for context (`/api/v1/ai/context`)
  - OpenRouter for LLM inference
- **Components:**
  - MessageBubble - Chat interface
  - QuickActions - Quick coaching actions

### 11. Quick Entry
- **Route:** `/quick-entry`
- **API Route:** `/api/quick-entry/analyze`
- **Purpose:** Rapid data entry for workouts/nutrition
- **Components:** QuickEntry, SafeQuickEntry
- **Backend:** Mixed (Supabase + AI)

### 12. Settings
- **Route:** `/settings`
- **CRUD:**
  - READ/UPDATE: User preferences, unit system
- **Components:**
  - UnitSystemToggle - Imperial/Metric toggle
  - IntegrationsSection - Manage integrations
- **Backend:** Supabase only

### 13. Integrations
- **Strava:**
  - `/api/strava/auth` - OAuth flow
  - `/api/strava/callback` - OAuth callback
  - `/api/strava/disconnect` - Disconnect
  - `/api/strava/sync` - Sync activities
  - `/api/strava/webhook` - Webhook handler
- **Garmin:**
  - `/api/garmin/sync` - Sync activities
  - `/api/connections/garmin` - Connection management
  - `/api/integrations/garmin/test` - Test credentials (Python backend)
- **Backend Integration:**
  - Python backend for Garmin API (`/api/v1/integrations/garmin/test`, `/api/v1/integrations/garmin/sync`)
- **Components:**
  - StravaConnection - Strava integration UI
  - GarminConnection - Garmin integration UI

---

## Backend API Endpoints (Python FastAPI)

### Health
- `GET /` - Root endpoint
- `GET /health` - Health check with DB status

### AI & Context (v1)
- `POST /api/v1/ai/context` - Get user context for AI
- `POST /api/v1/ai/prompt-context` - Get formatted prompt context

### Nutrition (v1)
- `POST /api/v1/nutrition/parse` - Parse meal description with AI

### Integrations (v1)
- `POST /api/v1/integrations/garmin/test` - Test Garmin credentials
- `POST /api/v1/integrations/garmin/sync` - Sync Garmin activities

### Embeddings (v1)
- `POST /api/v1/embeddings` - Generate embeddings
- `POST /api/v1/embeddings/search` - Search embeddings

### Background Jobs (v1)
- `POST /api/v1/background/summaries` - Generate summaries

---

## Critical Integration Points

### Frontend → Python Backend
1. **AI Context** (`/api/ai/context-backend` → `/api/v1/ai/context`)
2. **Meal Parsing** (`/api/nutrition/parse` → `/api/v1/nutrition/parse`)
3. **Garmin Test** (`/api/integrations/garmin/test` → `/api/v1/integrations/garmin/test`)
4. **Garmin Sync** (Multiple routes → `/api/v1/integrations/garmin/sync`)

### Authentication Flow
- Frontend API routes pass user ID via `X-User-ID` header
- Backend middleware extracts user ID from header (`get_current_user`)

---

## Database Schema (Supabase)

### Core Tables
- `profiles` - User profiles
- `activities` - Logged activities
- `workouts` - Workout templates
- `user_workouts` - User workout instances
- `workout_sessions` - Active workout tracking
- `programs` - Training programs
- `user_program_enrollments` - Program memberships
- `meal_logs` - Nutrition logs
- `foods` - Food database
- `meal_foods` - Foods in meals (junction)
- `user_goals` - User fitness goals
- `user_workout_favorites` - Favorited workouts
- `user_custom_workouts` - Custom workouts
- `strava_activities` - Synced from Strava
- `integration_tokens` - OAuth tokens

### RPC Functions
- `get_rag_context_for_user(p_user_id)` - Get consolidated user context for AI

---

## Issues to Verify & Fix

### 1. Backend Connectivity
- [ ] Python backend not running
- [ ] Need to verify NEXT_PUBLIC_BACKEND_URL environment variable
- [ ] Test all Python backend endpoints

### 2. API Route Issues
- [ ] Verify meal parsing fallback logic works
- [ ] Test Garmin integration endpoints
- [ ] Test AI context endpoints

### 3. Authentication
- [ ] Verify X-User-ID header passing
- [ ] Test auth middleware in Python backend

### 4. Missing Endpoints
The frontend expects these endpoints that may not exist:
- `/api/v1/nutrition/meal/parse` (Frontend calls this, backend has `/api/v1/nutrition/parse`)

---

## Testing Checklist

### Backend Endpoints
- [ ] `GET /health`
- [ ] `POST /api/v1/ai/context`
- [ ] `POST /api/v1/nutrition/parse`
- [ ] `POST /api/v1/integrations/garmin/test`
- [ ] `POST /api/v1/integrations/garmin/sync`

### Frontend API Routes
- [ ] `/api/nutrition/parse`
- [ ] `/api/ai/context-backend`
- [ ] `/api/integrations/garmin/test`
- [ ] `/api/nutrition/meals` (POST, GET)
- [ ] `/api/nutrition/foods/search`
- [ ] `/api/coach`

### User Flows
- [ ] User registration & onboarding
- [ ] Manual activity entry
- [ ] Workout session (start, track, complete)
- [ ] Meal logging (all 3 methods)
- [ ] AI coach interaction
- [ ] Garmin sync
- [ ] Strava sync

---

## Next Steps

1. Start Python backend
2. Fix endpoint path mismatches
3. Test all critical integrations
4. Verify authentication flow
5. Test each user flow end-to-end
