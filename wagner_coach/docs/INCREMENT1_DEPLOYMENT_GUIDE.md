# INCREMENT 1: Deployment Guide

## Document Information
- **Increment**: 1
- **Feature**: Basic Coach Chat
- **Version**: 1.0
- **Last Updated**: 2025-10-01

---

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Local Development Setup](#local-development-setup)
3. [Backend Setup](#backend-setup)
4. [Frontend Setup](#frontend-setup)
5. [Testing the Integration](#testing-the-integration)
6. [Production Deployment](#production-deployment)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Required Software
- **Node.js**: Version 18.x or higher
- **npm**: Version 9.x or higher (comes with Node.js)
- **Python**: Version 3.12 or higher
- **pip**: Latest version
- **Git**: For version control

### Required Accounts
- **Supabase Account**: For authentication and database
  - Sign up at: https://supabase.com
  - Create a new project
  - Note your project URL and keys

- **OpenAI Account**: For AI coach responses
  - Sign up at: https://platform.openai.com
  - Create an API key
  - Ensure you have credits/billing set up

### Recommended Tools
- **VS Code**: With Python and TypeScript extensions
- **Postman/Insomnia**: For API testing
- **Railway CLI** (for production deployment)
- **Vercel CLI** (for frontend deployment)

### System Requirements
- **RAM**: Minimum 8GB (16GB recommended)
- **Disk Space**: 2GB free space
- **OS**: Windows 10/11, macOS 10.15+, or Linux

---

## Local Development Setup

### 1. Clone the Repository

```bash
# Navigate to your projects directory
cd ~/Documents/Projects

# If not already cloned
git clone <repository-url> wagner_coach
cd wagner_coach
```

### 2. Verify Project Structure

```bash
wagner_coach/
├── fitness-backend/          # Python FastAPI backend
│   ├── app/
│   ├── tests/
│   ├── requirements.txt
│   └── ...
├── wagner-coach-clean/       # Next.js frontend
│   ├── app/
│   ├── components/
│   ├── package.json
│   └── ...
└── docs/                     # Documentation
    ├── design/
    ├── testing/
    └── ...
```

---

## Backend Setup

### Step 1: Navigate to Backend Directory

```bash
cd fitness-backend
```

### Step 2: Create Python Virtual Environment

**On Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**On macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected packages include:**
- fastapi
- uvicorn
- pydantic
- openai
- supabase
- python-dotenv
- And more...

### Step 4: Create Environment File

Create a file named `.env` in the `fitness-backend` directory:

```bash
# On Windows
type nul > .env

# On macOS/Linux
touch .env
```

### Step 5: Configure Environment Variables

Edit `.env` and add the following:

```env
# Supabase Configuration
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your-service-role-key-here

# OpenAI Configuration
OPENAI_API_KEY=sk-your-openai-api-key-here

# Application Settings
ENVIRONMENT=development
DEBUG=True
LOG_LEVEL=INFO

# Server Configuration
HOST=0.0.0.0
PORT=8000

# CORS Settings (for local frontend)
CORS_ORIGINS=["http://localhost:3000","http://127.0.0.1:3000"]
```

**Where to find your keys:**

1. **Supabase Keys**:
   - Go to: https://app.supabase.com
   - Select your project
   - Click "Settings" → "API"
   - Copy "Project URL" → Use as `SUPABASE_URL`
   - Copy "service_role" secret → Use as `SUPABASE_SERVICE_KEY`

2. **OpenAI API Key**:
   - Go to: https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)
   - Save it securely (you won't see it again)

### Step 6: Run Database Migrations (if needed)

```bash
# Check if migrations are needed
python -c "from app.database import init_db; init_db()"
```

### Step 7: Start the Backend Server

```bash
uvicorn app.main:app --reload --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

### Step 8: Verify Backend is Running

Open a new terminal and test the health endpoint:

```bash
curl http://localhost:8000/health
```

**Expected response:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-01T12:00:00Z"
}
```

Or visit in browser: http://localhost:8000/docs (Swagger UI)

---

## Frontend Setup

### Step 1: Navigate to Frontend Directory

Open a **new terminal** window:

```bash
cd wagner-coach-clean
```

### Step 2: Install Dependencies

```bash
npm install
```

**This will install:**
- Next.js 14
- React 18
- TypeScript
- Tailwind CSS
- Supabase client
- And more...

### Step 3: Create Environment File

```bash
# On Windows
type nul > .env.local

# On macOS/Linux
touch .env.local
```

### Step 4: Configure Environment Variables

Edit `.env.local` and add:

```env
# Backend API URL
NEXT_PUBLIC_BACKEND_URL=http://localhost:8000

# Supabase Configuration (Public keys - safe for frontend)
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your-anon-key-here
```

**Where to find Supabase Anon Key:**
- Go to: https://app.supabase.com
- Select your project
- Click "Settings" → "API"
- Copy "anon" public key → Use as `NEXT_PUBLIC_SUPABASE_ANON_KEY`

### Step 5: Start the Frontend Development Server

```bash
npm run dev
```

**Expected output:**
```
> wagner-coach-clean@0.1.0 dev
> next dev

  ▲ Next.js 14.x.x
  - Local:        http://localhost:3000
  - Network:      http://192.168.x.x:3000

 ✓ Ready in 2.3s
```

### Step 6: Verify Frontend is Running

Open your browser and navigate to:
- http://localhost:3000

You should see the Wagner Coach homepage.

---

## Testing the Integration

### Step 1: Create a Test User (if needed)

1. Navigate to your Supabase project dashboard
2. Go to "Authentication" → "Users"
3. Click "Add user" → "Create new user"
4. Enter email and password
5. Click "Create user"

**OR** use the signup flow on your frontend (if implemented)

### Step 2: Access the Coach Chat Page

1. Log in to your application (if auth is required)
2. Navigate to: http://localhost:3000/coach/trainer
3. You should see the chat interface with:
   - "Chat with Coach Alex" header
   - Welcome message
   - Text input area
   - Send button

### Step 3: Test Basic Functionality

**Test 1: Send a Message**
1. Type in the input field: "What's a good workout for beginners?"
2. Click "Send" or press Enter
3. **Expected**:
   - Your message appears (blue bubble, right side)
   - Loading indicator shows (bouncing dots)
   - AI response appears (gray bubble, left side)
   - Input clears automatically

**Test 2: Error Handling**
1. Stop the backend server (Ctrl+C in backend terminal)
2. Try to send a message
3. **Expected**:
   - Error message displays in red banner
   - Your message is removed (optimistic rollback)
   - Input is restored with your text
   - App remains functional

**Test 3: Character Limit**
1. Type or paste 1001+ characters
2. **Expected**:
   - Input stops at 1000 characters
   - Counter shows "1000/1000"
   - Send button remains enabled

**Test 4: Empty Message**
1. Leave input empty or type only spaces
2. **Expected**:
   - Send button is disabled
   - Cannot send empty message

**Test 5: Multiple Messages**
1. Restart backend server
2. Send 3-5 messages in sequence
3. **Expected**:
   - All messages appear in order
   - Conversation flows naturally
   - Auto-scroll to bottom
   - No errors or crashes

### Step 4: Test on Different Devices

**Desktop Browser**:
- Chrome: http://localhost:3000/coach/trainer
- Firefox: http://localhost:3000/coach/trainer
- Safari: http://localhost:3000/coach/trainer

**Mobile Simulation**:
1. Open Chrome DevTools (F12)
2. Click device toolbar icon (phone/tablet)
3. Select "iPhone SE" or "iPad"
4. Test chat interface
5. **Expected**:
   - Layout adapts to screen size
   - Touch targets are adequate
   - Virtual keyboard doesn't hide input

**Network Throttling**:
1. Open Chrome DevTools → Network tab
2. Set throttling to "Slow 3G"
3. Send a message
4. **Expected**:
   - Loading indicator shows longer
   - Eventually receives response
   - No errors or timeouts

### Step 5: Verify API Communication

**Check Backend Logs**:
In your backend terminal, you should see logs like:
```
INFO:     127.0.0.1:xxxxx - "POST /api/v1/coach/chat HTTP/1.1" 200 OK
```

**Check Frontend Console**:
1. Open browser DevTools (F12) → Console
2. Send a message
3. Look for any errors (should be none)
4. Check Network tab → XHR/Fetch for API calls

---

## Production Deployment

### Backend Deployment (Railway)

#### Step 1: Install Railway CLI

```bash
# On macOS/Linux
curl -fsSL https://railway.app/install.sh | sh

# On Windows (using npm)
npm install -g @railway/cli
```

#### Step 2: Login to Railway

```bash
railway login
```

This opens a browser window for authentication.

#### Step 3: Initialize Railway Project

```bash
cd fitness-backend
railway init
```

Select "Create new project" and give it a name (e.g., "wagner-coach-backend")

#### Step 4: Set Environment Variables

```bash
railway variables set SUPABASE_URL="https://your-project.supabase.co"
railway variables set SUPABASE_SERVICE_KEY="your-service-role-key"
railway variables set OPENAI_API_KEY="sk-your-openai-key"
railway variables set ENVIRONMENT="production"
railway variables set DEBUG="False"
```

**OR** use Railway Dashboard:
1. Go to: https://railway.app/dashboard
2. Select your project
3. Click "Variables" tab
4. Add all environment variables

#### Step 5: Deploy to Railway

```bash
railway up
```

This deploys your backend. Railway will:
1. Detect Python project
2. Install dependencies
3. Start the server
4. Provide a public URL

#### Step 6: Get Your Backend URL

```bash
railway domain
```

**OR** check Railway Dashboard → Settings → Domains

Your URL will be something like:
`https://wagner-coach-backend.railway.app`

#### Step 7: Test Production Backend

```bash
curl https://your-backend-url.railway.app/health
```

**Expected:**
```json
{
  "status": "healthy",
  "timestamp": "2025-10-01T..."
}
```

### Frontend Deployment (Vercel)

#### Step 1: Install Vercel CLI

```bash
npm install -g vercel
```

#### Step 2: Login to Vercel

```bash
vercel login
```

Follow the authentication flow.

#### Step 3: Configure Project

```bash
cd wagner-coach-clean
vercel
```

Answer the prompts:
- **Set up and deploy?** Y
- **Which scope?** Select your account
- **Link to existing project?** N
- **Project name?** wagner-coach (or your choice)
- **Directory?** ./ (press Enter)
- **Override settings?** N

#### Step 4: Set Environment Variables

**Via Vercel Dashboard** (Recommended):
1. Go to: https://vercel.com/dashboard
2. Select your project
3. Click "Settings" → "Environment Variables"
4. Add these variables:

```
NEXT_PUBLIC_BACKEND_URL = https://your-backend-url.railway.app
NEXT_PUBLIC_SUPABASE_URL = https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY = your-anon-key
```

**Important**: Select "Production", "Preview", and "Development" for each variable.

#### Step 5: Deploy to Production

```bash
vercel --prod
```

This deploys to production. Vercel will:
1. Build your Next.js app
2. Optimize assets
3. Deploy to global CDN
4. Provide production URL

Your URL will be something like:
`https://wagner-coach.vercel.app`

#### Step 6: Test Production Frontend

1. Visit: https://your-frontend-url.vercel.app/coach/trainer
2. Log in (create account if needed)
3. Send a test message
4. **Expected**:
   - Full chat functionality works
   - Connects to Railway backend
   - AI responses received
   - No CORS errors

### Post-Deployment Configuration

#### Update CORS Settings

Edit `fitness-backend/app/main.py` to include production frontend URL:

```python
origins = [
    "http://localhost:3000",
    "https://wagner-coach.vercel.app",  # Add your Vercel URL
    "https://your-custom-domain.com",    # If you have one
]
```

Deploy the update:
```bash
cd fitness-backend
railway up
```

#### Configure Custom Domain (Optional)

**For Backend (Railway)**:
1. Railway Dashboard → Settings → Domains
2. Click "Add Domain"
3. Enter your domain (e.g., api.wagnercoach.com)
4. Update DNS records as instructed

**For Frontend (Vercel)**:
1. Vercel Dashboard → Settings → Domains
2. Click "Add Domain"
3. Enter your domain (e.g., wagnercoach.com)
4. Update DNS records as instructed

---

## Troubleshooting

### Backend Issues

#### Issue: `Module not found` errors

**Solution**:
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

# Reinstall dependencies
pip install -r requirements.txt
```

#### Issue: `SUPABASE_URL not set` error

**Solution**:
```bash
# Check .env file exists
cat .env

# Verify variables are set
echo $SUPABASE_URL

# Reload environment
source venv/bin/activate
uvicorn app.main:app --reload
```

#### Issue: OpenAI API errors

**Solution**:
1. Verify API key is correct (starts with `sk-`)
2. Check billing status: https://platform.openai.com/account/billing
3. Test key directly:
```bash
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

#### Issue: Port 8000 already in use

**Solution**:
```bash
# Find process using port 8000
lsof -i :8000          # macOS/Linux
netstat -ano | findstr :8000  # Windows

# Kill the process or use different port
uvicorn app.main:app --reload --port 8001
```

### Frontend Issues

#### Issue: `NEXT_PUBLIC_BACKEND_URL` not defined

**Solution**:
```bash
# Check .env.local exists
cat .env.local

# Restart dev server
npm run dev
```

#### Issue: CORS errors in browser console

**Symptom**:
```
Access to fetch at 'http://localhost:8000/api/v1/coach/chat' from origin
'http://localhost:3000' has been blocked by CORS policy
```

**Solution**:
1. Check backend CORS configuration in `app/main.py`
2. Ensure frontend URL is in allowed origins
3. Restart backend server

#### Issue: Authentication errors (401)

**Solution**:
1. Check if user is logged in (Supabase session)
2. Verify Supabase keys are correct
3. Check browser console for auth errors
4. Try logging out and back in

#### Issue: Build errors on Vercel

**Solution**:
1. Check build logs in Vercel dashboard
2. Ensure all dependencies are in `package.json`
3. Verify Node.js version compatibility
4. Try building locally:
```bash
npm run build
```

### Database Issues

#### Issue: Supabase connection errors

**Solution**:
1. Verify project is not paused (free tier auto-pauses)
2. Check Supabase dashboard for service status
3. Verify URL and keys are correct
4. Try regenerating service role key

#### Issue: Missing tables or schemas

**Solution**:
```bash
# Run migrations/setup scripts
cd fitness-backend
python -c "from app.database import init_db; init_db()"
```

### Deployment Issues

#### Issue: Railway deployment fails

**Solution**:
1. Check build logs in Railway dashboard
2. Verify `requirements.txt` is complete
3. Ensure Python version is compatible
4. Check Railway service limits

#### Issue: Vercel deployment fails

**Solution**:
1. Check build logs in Vercel dashboard
2. Verify `package.json` scripts are correct
3. Ensure no TypeScript errors:
```bash
npm run build
```
4. Check Vercel service limits

---

## Verification Checklist

### Local Development ✅
- [ ] Backend server runs on http://localhost:8000
- [ ] Frontend runs on http://localhost:3000
- [ ] Can access /docs (Swagger UI) on backend
- [ ] Can log in on frontend
- [ ] Chat page loads at /coach/trainer
- [ ] Can send messages and receive AI responses
- [ ] Error handling works (test by stopping backend)
- [ ] No console errors in browser DevTools

### Production Deployment ✅
- [ ] Backend deployed to Railway
- [ ] Frontend deployed to Vercel
- [ ] All environment variables set correctly
- [ ] CORS configured for production URLs
- [ ] Custom domains configured (if applicable)
- [ ] HTTPS enabled on both frontend and backend
- [ ] Health check passes on production backend
- [ ] Can access production chat page
- [ ] Can send messages in production
- [ ] Error logging configured

### Security ✅
- [ ] API keys not committed to Git
- [ ] `.env` and `.env.local` in `.gitignore`
- [ ] Service role keys only on backend
- [ ] Anon keys only on frontend
- [ ] CORS properly restricted
- [ ] Authentication required for chat endpoint
- [ ] Rate limiting enabled

---

## Additional Resources

### Documentation
- [Feature Design](design/increment1_basic_coach_chat.md)
- [Test Design](testing/increment1_basic_coach_chat_test.md)
- [Completion Report](INCREMENT1_COMPLETION_REPORT.md)
- [Manual Test Checklist](INCREMENT1_MANUAL_TEST_CHECKLIST.md)

### External Links
- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Supabase Documentation](https://supabase.com/docs)
- [OpenAI API Documentation](https://platform.openai.com/docs)
- [Railway Documentation](https://docs.railway.app/)
- [Vercel Documentation](https://vercel.com/docs)

### Support
- **Backend Issues**: Check FastAPI logs and Railway dashboard
- **Frontend Issues**: Check browser console and Vercel logs
- **API Issues**: Use Swagger UI (http://localhost:8000/docs)
- **Database Issues**: Check Supabase dashboard

---

## Quick Reference Commands

### Backend
```bash
# Activate virtual environment
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Run server
uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/unit/test_coach_service_increment1.py
pytest tests/integration/test_coach_api_increment1.py

# Deploy to Railway
railway up
```

### Frontend
```bash
# Install dependencies
npm install

# Run dev server
npm run dev

# Build for production
npm run build

# Deploy to Vercel
vercel --prod
```

### Useful URLs
- Local Frontend: http://localhost:3000/coach/trainer
- Local Backend: http://localhost:8000/docs
- Backend Health: http://localhost:8000/health

---

**Document Version**: 1.0
**Last Updated**: 2025-10-01
**Status**: Complete and Ready for Use
