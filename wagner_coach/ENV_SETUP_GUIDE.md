# 🔐 Environment Configuration Guide

**Complete guide for setting up API keys and environment variables**

## 📋 Required API Keys

### 1. Groq API (Speed & Streaming)

**What it's for:** Ultra-fast real-time responses, streaming chat, quick categorizations

**How to get it:**
1. Visit https://console.groq.com
2. Sign up for free account
3. Navigate to "API Keys" section
4. Click "Create API Key"
5. Copy the key (starts with `gsk_`)

**Free Tier:**
- 30 requests per minute
- Unlimited total requests
- Access to Llama 3.3 70B, Llama 3.1 8B, Mixtral, DeepSeek

### 2. OpenRouter API (Accuracy & Features)

**What it's for:** Vision analysis, complex reasoning, program generation, fallback

**How to get it:**
1. Visit https://openrouter.ai
2. Sign up for free account
3. Go to "Keys" section
4. Click "Create Key"
5. Copy the key (starts with `sk-or-v1-`)

**Free Tier:**
- 50 requests per day per model
- Access to 300+ models
- Includes vision models (Llama-4 Scout, Yi-Vision)
- DeepSeek R1, DeepSeek V3, Gemini 2.0/2.5

### 3. Supabase (Database & Auth)

**What it's for:** Database, authentication, storage

**How to get it:**
1. Visit https://supabase.com
2. Create new project
3. Get the following from project settings:
   - Project URL
   - Anon/Public Key
   - Service Role Key (keep secret!)

## 🔧 Local Development Setup

### Frontend (.env.local)

Create `wagner-coach-clean/.env.local`:

```bash
# Groq API (Speed)
NEXT_PUBLIC_GROQ_API_KEY=gsk_your_groq_key_here

# OpenRouter API (Accuracy/Features)
NEXT_PUBLIC_OPENROUTER_API_KEY=sk-or-v1-your_openrouter_key_here

# Supabase
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key

# App URL
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

### Backend (.env)

Create `fitness-backend/.env`:

```bash
# Groq API (Speed)
GROQ_API_KEY=gsk_your_groq_key_here

# OpenRouter API (Accuracy/Features)
OPENROUTER_API_KEY=sk-or-v1-your_openrouter_key_here

# Supabase
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_SERVICE_KEY=your_supabase_service_role_key

# App Settings
ENVIRONMENT=development
LOG_LEVEL=INFO
```

### Quick Setup Script

**Windows (PowerShell):**
```powershell
# Frontend
cd wagner-coach-clean
Copy-Item .env.example .env.local
notepad .env.local  # Add your keys

# Backend
cd ..\fitness-backend
Copy-Item .env.example .env
notepad .env  # Add your keys
```

**macOS/Linux:**
```bash
# Frontend
cd wagner-coach-clean
cp .env.example .env.local
nano .env.local  # Add your keys

# Backend
cd ../fitness-backend
cp .env.example .env
nano .env  # Add your keys
```

## 🚀 Production Setup (Vercel)

### Vercel Environment Variables

1. **Go to Vercel Dashboard**
   - Navigate to your project
   - Click "Settings" → "Environment Variables"

2. **Add the following variables:**

| Variable Name | Value | Environment |
|---------------|-------|-------------|
| `GROQ_API_KEY` | `gsk_...` | Production, Preview, Development |
| `OPENROUTER_API_KEY` | `sk-or-v1-...` | Production, Preview, Development |
| `NEXT_PUBLIC_GROQ_API_KEY` | `gsk_...` | Production, Preview, Development |
| `NEXT_PUBLIC_OPENROUTER_API_KEY` | `sk-or-v1-...` | Production, Preview, Development |
| `NEXT_PUBLIC_SUPABASE_URL` | `https://...` | Production, Preview, Development |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `eyJ...` | Production, Preview, Development |
| `NEXT_PUBLIC_APP_URL` | `https://your-app.vercel.app` | Production |
| `NEXT_PUBLIC_APP_URL` | `https://preview-url.vercel.app` | Preview |
| `NEXT_PUBLIC_APP_URL` | `http://localhost:3000` | Development |

3. **Redeploy**
   - After adding variables, redeploy your app
   - Vercel will pick up the new environment variables

### Using Vercel CLI

```bash
# Install Vercel CLI
npm i -g vercel

# Link project
vercel link

# Add environment variables
vercel env add GROQ_API_KEY production
vercel env add OPENROUTER_API_KEY production
vercel env add NEXT_PUBLIC_GROQ_API_KEY production
vercel env add NEXT_PUBLIC_OPENROUTER_API_KEY production

# Deploy
vercel --prod
```

## 🔒 Security Best Practices

### DO's ✅

1. **Use `.env.local` for frontend** (not `.env`)
   - `.env.local` is gitignored
   - Prevents accidental commits

2. **Prefix public keys** with `NEXT_PUBLIC_`
   - Only these are exposed to browser
   - Server-side keys stay secret

3. **Keep service keys secret**
   - Never expose Supabase service role key
   - Never commit backend .env files

4. **Rotate keys regularly**
   - Change keys every 3-6 months
   - Immediately if compromised

5. **Use different keys per environment**
   - Development keys
   - Production keys
   - Never mix them

### DON'Ts ❌

1. **Never commit .env files**
   - Add to `.gitignore`
   - Use `.env.example` templates

2. **Never hardcode API keys**
   - Always use environment variables
   - Never in source code

3. **Never expose service keys**
   - Backend keys stay on server
   - Use anon keys for frontend

4. **Never share keys publicly**
   - Not in screenshots
   - Not in documentation
   - Not in support tickets

## 🧪 Testing Your Setup

### 1. Check Environment Variables Loaded

**Frontend:**
```typescript
// In any component or page
console.log('Groq Key:', process.env.NEXT_PUBLIC_GROQ_API_KEY ? '✅ Loaded' : '❌ Missing');
console.log('OpenRouter Key:', process.env.NEXT_PUBLIC_OPENROUTER_API_KEY ? '✅ Loaded' : '❌ Missing');
```

**Backend:**
```python
# In any service file
import os
print('Groq Key:', '✅ Loaded' if os.getenv('GROQ_API_KEY') else '❌ Missing')
print('OpenRouter Key:', '✅ Loaded' if os.getenv('OPENROUTER_API_KEY') else '❌ Missing')
```

### 2. Test API Connections

**Test Groq:**
```bash
curl https://api.groq.com/openai/v1/models \
  -H "Authorization: Bearer $GROQ_API_KEY"
```

**Test OpenRouter:**
```bash
curl https://openrouter.ai/api/v1/models \
  -H "Authorization: Bearer $OPENROUTER_API_KEY"
```

### 3. Verify Dual Router

**Frontend:**
```typescript
import { dualRouter } from '@/lib/ai/dual-model-router';

// Should log initialization messages
// ✅ Groq API initialized
// ✅ OpenRouter API initialized
```

**Backend:**
```python
from app.services.dual_model_router import dual_router

# Should print:
# [DualRouter] ✅ Groq API initialized
# [DualRouter] ✅ OpenRouter API initialized
```

## 🛠️ Troubleshooting

### Issue: "API key not found"

**Solution:**
```bash
# 1. Check file exists
ls -la .env.local  # Frontend
ls -la .env       # Backend

# 2. Check key is in file
cat .env.local | grep GROQ
cat .env | grep GROQ

# 3. Restart dev server
# Frontend
npm run dev

# Backend
python -m uvicorn app.main:app --reload
```

### Issue: "Invalid API key"

**Solution:**
1. Copy key again from provider
2. Check for extra spaces or quotes
3. Ensure key starts with correct prefix:
   - Groq: `gsk_`
   - OpenRouter: `sk-or-v1-`

### Issue: "Rate limit exceeded"

**Solution:**
```typescript
// Reset failure tracking
dualRouter.resetFailures();

// System will automatically use fallback provider
```

### Issue: Vercel deployment fails

**Solution:**
1. Check all required variables are set
2. Verify variable names (case-sensitive)
3. Ensure `NEXT_PUBLIC_` prefix for client-side keys
4. Redeploy after adding variables

## 📊 Environment Variable Reference

### Frontend (NEXT_PUBLIC_*)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `NEXT_PUBLIC_GROQ_API_KEY` | Yes | Groq API key for speed | `gsk_...` |
| `NEXT_PUBLIC_OPENROUTER_API_KEY` | Yes | OpenRouter key for features | `sk-or-v1-...` |
| `NEXT_PUBLIC_SUPABASE_URL` | Yes | Supabase project URL | `https://...supabase.co` |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Yes | Supabase anon key | `eyJ...` |
| `NEXT_PUBLIC_APP_URL` | Yes | App URL for headers | `http://localhost:3000` |

### Backend (Server-side)

| Variable | Required | Description | Example |
|----------|----------|-------------|---------|
| `GROQ_API_KEY` | Yes | Groq API key | `gsk_...` |
| `OPENROUTER_API_KEY` | Yes | OpenRouter API key | `sk-or-v1-...` |
| `SUPABASE_URL` | Yes | Supabase project URL | `https://...supabase.co` |
| `SUPABASE_SERVICE_KEY` | Yes | Supabase service key (SECRET!) | `eyJ...` |
| `ENVIRONMENT` | No | Environment name | `development` |
| `LOG_LEVEL` | No | Logging level | `INFO` |

## 🔄 Migration Checklist

Migrating from old setup to dual-API:

- [ ] Get Groq API key
- [ ] Get OpenRouter API key
- [ ] Update frontend `.env.local`:
  - [ ] Add `NEXT_PUBLIC_GROQ_API_KEY`
  - [ ] Add `NEXT_PUBLIC_OPENROUTER_API_KEY`
- [ ] Update backend `.env`:
  - [ ] Add `GROQ_API_KEY`
  - [ ] Add `OPENROUTER_API_KEY`
- [ ] Restart dev servers
- [ ] Verify both APIs initialized
- [ ] Test dual router functionality
- [ ] Update Vercel environment variables
- [ ] Redeploy to production
- [ ] Monitor usage and fallbacks

## 📝 Quick Reference

### Get API Keys
- Groq: https://console.groq.com/keys
- OpenRouter: https://openrouter.ai/keys
- Supabase: https://supabase.com/dashboard/project/_/settings/api

### File Locations
- Frontend: `wagner-coach-clean/.env.local`
- Backend: `fitness-backend/.env`
- Examples: `.env.example` (template)

### Important Prefixes
- Client-side: `NEXT_PUBLIC_*`
- Server-side: No prefix
- Groq keys: `gsk_*`
- OpenRouter keys: `sk-or-v1-*`

### Restart Commands
```bash
# Frontend
npm run dev

# Backend
python -m uvicorn app.main:app --reload
```

---

**Status:** 📚 Complete setup guide for dual-API environment configuration

*Last Updated: 2025-10-02*
