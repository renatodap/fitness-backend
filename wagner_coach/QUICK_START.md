# Quick Start Guide

## Prerequisites
- Python 3.12+
- Node.js 18+
- Supabase account
- OpenAI API key

## Backend Setup (Required for Coach Chat)

1. **Navigate to backend:**
   ```bash
   cd fitness-backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Create `.env` file:**
   ```bash
   SUPABASE_URL=your_supabase_url
   SUPABASE_KEY=your_anon_key
   SUPABASE_SERVICE_KEY=your_service_role_key
   OPENAI_API_KEY=your_openai_key
   JWT_SECRET=your_jwt_secret
   ```

5. **Start backend:**
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```

   Backend will run at: http://localhost:8000

## Frontend Setup

1. **Navigate to frontend:**
   ```bash
   cd wagner-coach-clean
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Create `.env.local` file:**
   ```bash
   NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
   NEXT_PUBLIC_SUPABASE_ANON_KEY=your_anon_key
   NEXT_PUBLIC_BACKEND_URL=http://localhost:8000
   ```

4. **Start frontend:**
   ```bash
   npm run dev
   ```

   Frontend will run at: http://localhost:3000

## Access the App

1. Navigate to http://localhost:3000
2. Click "Sign In"
3. After auth, you'll see the dashboard with quick actions:
   - **Chat with Trainer** → /coach/trainer
   - **Chat with Nutritionist** → /coach/nutritionist  
   - **Log Workout** → /workouts/log
   - **Log Meal** → /nutrition/log
   - **Sync Activities** → /activities/sync-status

## Troubleshooting

### "Cannot reach backend server" error:
- Ensure backend is running: `cd fitness-backend && uvicorn app.main:app --reload`
- Check NEXT_PUBLIC_BACKEND_URL in frontend `.env.local`
- Verify backend URL in console logs

### Coach chat returns 500 error:
- Check backend logs for Python errors
- Verify OpenAI API key is set in backend `.env`
- Ensure Supabase credentials are correct

### Build errors:
- Check import paths (case-sensitive: `@/components/Coach/` not `@/components/coach/`)
- Run `npm install` in frontend
- Run `pip install -r requirements.txt` in backend

## Features Implemented

✅ INCREMENT 1: Basic Coach Chat (Trainer)
✅ INCREMENT 2: Nutritionist Chat
✅ INCREMENT 3: Manual Workout Logging
✅ INCREMENT 4: Meal Logging with Macros
✅ INCREMENT 5: Activity Sync Status

## RAG/Vector Context

The coaches use RAG (Retrieval-Augmented Generation) with vector embeddings:
- `context_builder.py` builds context from user data
- `embedding_service.py` generates & searches vector embeddings
- Coaches retrieve relevant historical data via vector similarity search
- Context includes: recent workouts, meals, activities, goals, progress

To verify RAG is working, check backend logs when chatting with coaches.
