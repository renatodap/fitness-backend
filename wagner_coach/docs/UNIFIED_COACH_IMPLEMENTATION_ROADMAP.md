# Unified Coach Implementation Roadmap

**Feature:** Single "Coach" interface replacing AI Chat + Quick Entry
**Status:** Backend 60% complete | Frontend 0% | Database 40%
**Estimated Time:** 15-20 hours remaining

---

## ✅ COMPLETED (Backend Architecture)

### 1. Design & Architecture ✅
- [x] Complete production-level architecture designed
- [x] ChatGPT-like interface spec
- [x] Dual-mode logic (chat vs log detection)
- [x] RAG context building strategy
- [x] Cost optimization plan ($0.16/user/month)
- [x] Database schema enhancements defined

**Files Created:**
- `docs/design/unified_coach_interface.md` - Complete architecture
- `docs/database/QUICK_ENTRY_NEW_SCHEMA_UPDATE.md` - Schema details

### 2. Backend Services ✅
- [x] Message Classifier Service (`message_classifier_service.py`)
  - Classifies: CHAT vs LOG
  - Uses Groq Llama 3.3 70B ($0.05/M tokens)
  - High-confidence classification

- [x] Unified Coach Service (`unified_coach_service.py`)
  - Handles both chat and log modes
  - RAG context building from all embeddings
  - Claude streaming responses
  - Log preview generation
  - Message vectorization
  - Conversation management

**Files Created:**
- `app/services/message_classifier_service.py`
- `app/services/unified_coach_service.py`

### 3. Quick Entry Integration ✅
- [x] Quick Entry uses new schema (quick_entry_logs + embeddings)
- [x] All logs linked via FK to quick_entry_logs
- [x] Vector embeddings for RAG
- [x] Cost tracking per entry

**Files Updated:**
- `app/services/quick_entry_service.py` - Now uses new schema

---

## 📋 REMAINING WORK (Critical Path)

### PHASE 1: Backend API Endpoints (2-3 hours)

#### 1.1 Replace Old Coach API
**File:** `app/api/v1/coach.py`

**Current State:** Old coach API exists
**Required:** Replace with unified API

```python
# NEW ENDPOINTS NEEDED:

@router.post("/message")
# Send any message (chat or log)
# Routes to unified_coach_service.process_message()

@router.post("/message/multimodal")
# Send message with image/audio
# Handles file uploads

@router.post("/confirm-log")
# Confirm log preview
# Routes to unified_coach_service.confirm_log()

@router.get("/conversations")
# Get chat history
# Supports pagination

@router.get("/conversations/{conversation_id}")
# Get specific conversation messages

@router.delete("/conversations/{conversation_id}")
# Delete conversation
```

**Implementation:**
- Replace entire `app/api/v1/coach.py` with new unified endpoints
- Remove old chat endpoints
- Add streaming support for real-time responses
- Add rate limiting (200 messages/day)

---

### PHASE 2: Database Migrations (1-2 hours)

#### 2.1 Update coach_messages Table
**File:** `migrations/009_unified_coach_schema.sql`

```sql
-- Add columns to existing coach_messages table
ALTER TABLE public.coach_messages
    ADD COLUMN IF NOT EXISTS message_type TEXT CHECK (message_type IN ('chat', 'log_preview', 'log_confirmed', 'system')) DEFAULT 'chat',
    ADD COLUMN IF NOT EXISTS metadata JSONB DEFAULT '{}'::JSONB,
    ADD COLUMN IF NOT EXISTS quick_entry_log_id UUID REFERENCES public.quick_entry_logs(id),
    ADD COLUMN IF NOT EXISTS context_used JSONB,
    ADD COLUMN IF NOT EXISTS tokens_used INTEGER,
    ADD COLUMN IF NOT EXISTS cost_usd NUMERIC(10, 6),
    ADD COLUMN IF NOT EXISTS ai_provider TEXT,
    ADD COLUMN IF NOT EXISTS ai_model TEXT,
    ADD COLUMN IF NOT EXISTS is_vectorized BOOLEAN DEFAULT FALSE;

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_coach_messages_user_conversation ON public.coach_messages(user_id, conversation_id);
CREATE INDEX IF NOT EXISTS idx_coach_messages_message_type ON public.coach_messages(message_type);
CREATE INDEX IF NOT EXISTS idx_coach_messages_quick_entry ON public.coach_messages(quick_entry_log_id) WHERE quick_entry_log_id IS NOT NULL;
```

#### 2.2 Create coach_message_embeddings Table

```sql
CREATE TABLE IF NOT EXISTS public.coach_message_embeddings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    message_id UUID NOT NULL REFERENCES public.coach_messages(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    embedding vector(384) NOT NULL,  -- FREE model: sentence-transformers
    content_text TEXT NOT NULL,
    embedding_model TEXT NOT NULL DEFAULT 'sentence-transformers/all-MiniLM-L6-v2',
    created_at TIMESTAMPTZ DEFAULT NOW(),

    CONSTRAINT unique_message_embedding UNIQUE (message_id)
);

-- Vector similarity index
CREATE INDEX idx_coach_message_embeddings_vector
    ON public.coach_message_embeddings
    USING hnsw (embedding vector_cosine_ops)
    WITH (m = 16, ef_construction = 64);

-- Standard indexes
CREATE INDEX idx_coach_message_embeddings_user ON public.coach_message_embeddings(user_id);
CREATE INDEX idx_coach_message_embeddings_role ON public.coach_message_embeddings(role);

-- RLS
ALTER TABLE public.coach_message_embeddings ENABLE ROW LEVEL SECURITY;

CREATE POLICY "Users can view own message embeddings"
    ON public.coach_message_embeddings FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Service role can insert embeddings"
    ON public.coach_message_embeddings FOR INSERT
    WITH CHECK (auth.role() = 'service_role');
```

#### 2.3 Create Database Function for RAG

```sql
-- Search coach message embeddings
CREATE OR REPLACE FUNCTION public.search_coach_message_embeddings(
    query_embedding vector(384),
    user_id_filter UUID,
    match_threshold FLOAT DEFAULT 0.6,
    match_count INT DEFAULT 5
)
RETURNS TABLE (
    message_id UUID,
    role TEXT,
    content_text TEXT,
    similarity FLOAT,
    created_at TIMESTAMPTZ
)
LANGUAGE plpgsql
SECURITY DEFINER
AS $$
BEGIN
    RETURN QUERY
    SELECT
        cme.message_id,
        cme.role,
        cme.content_text,
        1 - (cme.embedding <=> query_embedding) AS similarity,
        cme.created_at
    FROM public.coach_message_embeddings cme
    WHERE cme.user_id = user_id_filter
        AND (1 - (cme.embedding <=> query_embedding)) > match_threshold
    ORDER BY cme.embedding <=> query_embedding
    LIMIT match_count;
END;
$$;
```

---

### PHASE 3: Frontend - Remove Old Pages (30 min)

#### 3.1 Delete AI Chat Page
**Files to Delete:**
- `wagner-coach-clean/app/chat/page.tsx` (or wherever AI chat lives)
- Any related components

#### 3.2 Update Bottom Navigation
**File:** `wagner-coach-clean/components/BottomNav.tsx` (or similar)

**Change:**
```typescript
// OLD:
{name: "Quick Entry", icon: "⚡", href: "/quick-entry"}
{name: "Chat", icon: "💬", href: "/chat"}

// NEW:
{name: "Coach", icon: "🤖", href: "/coach"}
```

---

### PHASE 4: Frontend - Build New Coach UI (6-8 hours)

#### 4.1 Create ChatGPT-like Interface
**File:** `wagner-coach-clean/app/coach/page.tsx`

```typescript
'use client'

import { useState, useEffect, useRef } from 'react'
import { useAuth } from '@/lib/auth'
import { MessageBubble } from '@/components/coach/MessageBubble'
import { LogPreviewCard } from '@/components/coach/LogPreviewCard'
import { ChatInput } from '@/components/coach/ChatInput'
import { LoadingDots } from '@/components/LoadingDots'

export default function CoachPage() {
  const { user } = useAuth()
  const [messages, setMessages] = useState([])
  const [conversationId, setConversationId] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [pendingLogPreview, setPendingLogPreview] = useState(null)
  const messagesEndRef = useRef(null)

  // Auto-scroll to bottom
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  // Load conversation history
  useEffect(() => {
    loadConversationHistory()
  }, [])

  const loadConversationHistory = async () => {
    try {
      const response = await fetch('/api/v1/coach/conversations', {
        headers: { 'Authorization': `Bearer ${user.token}` }
      })
      const data = await response.json()

      if (data.messages) {
        setMessages(data.messages)
        setConversationId(data.conversation_id)
      }
    } catch (error) {
      console.error('Failed to load history:', error)
    }
  }

  const sendMessage = async (text, imageFile = null, audioFile = null) => {
    // Add user message to UI immediately (optimistic update)
    const userMessage = {
      id: Date.now(),
      role: 'user',
      content: text,
      timestamp: new Date().toISOString()
    }
    setMessages(prev => [...prev, userMessage])
    setIsLoading(true)

    try {
      // Send to API
      const formData = new FormData()
      formData.append('message', text)
      if (conversationId) formData.append('conversation_id', conversationId)
      if (imageFile) formData.append('image', imageFile)
      if (audioFile) formData.append('audio', audioFile)

      const response = await fetch('/api/v1/coach/message/multimodal', {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${user.token}` },
        body: formData
      })

      const data = await response.json()
      setConversationId(data.conversation_id)

      if (data.mode === 'chat') {
        // CHAT MODE: Add AI response
        const aiMessage = {
          id: data.ai_message_id,
          role: 'assistant',
          content: data.response,
          timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, aiMessage])

      } else if (data.mode === 'log_preview') {
        // LOG MODE: Show preview card
        setPendingLogPreview({
          user_message_id: data.user_message_id,
          log_type: data.log_type,
          log_data: data.log_preview,
          original_text: text
        })
      }

    } catch (error) {
      console.error('Failed to send message:', error)
      // Show error message
      const errorMessage = {
        id: Date.now(),
        role: 'system',
        content: '❌ Failed to send message. Please try again.',
        timestamp: new Date().toISOString()
      }
      setMessages(prev => [...prev, errorMessage])
    } finally {
      setIsLoading(false)
    }
  }

  const confirmLog = async () => {
    if (!pendingLogPreview) return

    try {
      const response = await fetch('/api/v1/coach/confirm-log', {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${user.token}`,
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          conversation_id: conversationId,
          user_message_id: pendingLogPreview.user_message_id,
          log_type: pendingLogPreview.log_type,
          log_data: pendingLogPreview.log_data,
          original_text: pendingLogPreview.original_text
        })
      })

      const data = await response.json()

      if (data.success) {
        // Add success message
        const successMessage = {
          id: data.system_message_id,
          role: 'system',
          content: data.message,
          timestamp: new Date().toISOString()
        }
        setMessages(prev => [...prev, successMessage])
        setPendingLogPreview(null)
      }

    } catch (error) {
      console.error('Failed to confirm log:', error)
    }
  }

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white border-b px-4 py-3 flex items-center justify-between">
        <h1 className="text-xl font-semibold">Coach</h1>
        <button onClick={() => {/* New conversation */}} className="text-sm text-blue-600">
          + New Chat
        </button>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map(msg => (
          <MessageBubble
            key={msg.id}
            role={msg.role}
            content={msg.content}
            timestamp={msg.timestamp}
          />
        ))}

        {/* Log Preview Card */}
        {pendingLogPreview && (
          <LogPreviewCard
            logType={pendingLogPreview.log_type}
            logData={pendingLogPreview.log_data}
            onConfirm={confirmLog}
            onEdit={() => {/* Show edit modal */}}
            onCancel={() => setPendingLogPreview(null)}
          />
        )}

        {isLoading && (
          <div className="flex items-center space-x-2 text-gray-500">
            <LoadingDots />
            <span className="text-sm">Coach is thinking...</span>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Input */}
      <ChatInput
        onSend={sendMessage}
        disabled={isLoading}
      />
    </div>
  )
}
```

#### 4.2 Create Components

**`components/coach/MessageBubble.tsx`:**
```typescript
export function MessageBubble({ role, content, timestamp }) {
  const isUser = role === 'user'
  const isSystem = role === 'system'

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`
        max-w-[80%] rounded-2xl px-4 py-2
        ${isUser ? 'bg-blue-600 text-white' :
          isSystem ? 'bg-green-100 text-green-800' :
          'bg-gray-200 text-gray-900'}
      `}>
        <p className="text-sm whitespace-pre-wrap">{content}</p>
        <span className="text-xs opacity-70 mt-1 block">
          {new Date(timestamp).toLocaleTimeString()}
        </span>
      </div>
    </div>
  )
}
```

**`components/coach/LogPreviewCard.tsx`:**
```typescript
export function LogPreviewCard({ logType, logData, onConfirm, onEdit, onCancel }) {
  return (
    <div className="bg-white border-2 border-blue-200 rounded-xl p-4 shadow-md">
      <div className="flex items-center justify-between mb-3">
        <h3 className="font-semibold text-lg">
          {logType === 'meal' && '🍽️ Meal Detected'}
          {logType === 'workout' && '💪 Workout Detected'}
          {logType === 'activity' && '🏃 Activity Detected'}
          {logType === 'measurement' && '⚖️ Measurement Detected'}
        </h3>
        <span className="text-sm text-gray-500">Review & Confirm</span>
      </div>

      {/* Display extracted data based on type */}
      {logType === 'meal' && (
        <div className="space-y-2 mb-4">
          <p className="font-medium">{logData.meal_type}</p>
          <div className="text-sm text-gray-700">
            {logData.foods?.map((food, i) => (
              <div key={i}>• {food.name} ({food.quantity})</div>
            ))}
          </div>
          <div className="flex gap-4 text-sm font-semibold mt-3">
            <span>{logData.calories} cal</span>
            <span>{logData.protein_g}g protein</span>
            <span>{logData.carbs_g}g carbs</span>
            <span>{logData.fat_g}g fat</span>
          </div>
        </div>
      )}

      {logType === 'workout' && (
        <div className="space-y-2 mb-4">
          <p className="font-medium">{logData.workout_name}</p>
          <div className="text-sm text-gray-700">
            {logData.exercises?.map((ex, i) => (
              <div key={i}>
                • {ex.name}: {ex.sets}x{ex.reps} @ {ex.weight_lbs} lbs
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Action buttons */}
      <div className="flex gap-2">
        <button
          onClick={onEdit}
          className="flex-1 py-2 px-4 border border-gray-300 rounded-lg text-sm font-medium hover:bg-gray-50"
        >
          Edit
        </button>
        <button
          onClick={onConfirm}
          className="flex-1 py-2 px-4 bg-blue-600 text-white rounded-lg text-sm font-medium hover:bg-blue-700"
        >
          Confirm
        </button>
        <button
          onClick={onCancel}
          className="py-2 px-3 text-gray-500 hover:bg-gray-50 rounded-lg"
        >
          ✕
        </button>
      </div>
    </div>
  )
}
```

**`components/coach/ChatInput.tsx`:**
```typescript
export function ChatInput({ onSend, disabled }) {
  const [text, setText] = useState('')
  const [imageFile, setImageFile] = useState(null)
  const fileInputRef = useRef(null)

  const handleSend = () => {
    if (!text.trim() && !imageFile) return
    onSend(text, imageFile)
    setText('')
    setImageFile(null)
  }

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  return (
    <div className="bg-white border-t p-4">
      {imageFile && (
        <div className="mb-2 p-2 bg-blue-50 rounded flex items-center justify-between">
          <span className="text-sm">📷 Image attached</span>
          <button onClick={() => setImageFile(null)}>✕</button>
        </div>
      )}

      <div className="flex items-end gap-2">
        <button
          onClick={() => fileInputRef.current?.click()}
          className="p-2 text-gray-600 hover:bg-gray-100 rounded"
          disabled={disabled}
        >
          📷
        </button>
        <input
          type="file"
          ref={fileInputRef}
          accept="image/*"
          onChange={(e) => setImageFile(e.target.files[0])}
          className="hidden"
        />

        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Ask anything or log your meal/workout..."
          className="flex-1 p-3 border rounded-xl resize-none focus:outline-none focus:ring-2 focus:ring-blue-500"
          rows={2}
          disabled={disabled}
        />

        <button
          onClick={handleSend}
          disabled={disabled || (!text.trim() && !imageFile)}
          className="p-3 bg-blue-600 text-white rounded-xl hover:bg-blue-700 disabled:bg-gray-300"
        >
          ➤
        </button>
      </div>
    </div>
  )
}
```

---

### PHASE 5: Testing & Optimization (2-3 hours)

#### 5.1 Backend Testing
```bash
# Test chat flow
curl -X POST http://localhost:8000/api/v1/coach/message \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "What should I eat for breakfast?"}'

# Test log flow
curl -X POST http://localhost:8000/api/v1/coach/message \
  -H "Authorization: Bearer TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"message": "I ate 3 eggs and oatmeal"}'
```

#### 5.2 Frontend Testing
- [ ] Chat message sends and receives response
- [ ] Log detection shows preview card
- [ ] Edit log works
- [ ] Confirm log saves to database
- [ ] Chat history loads
- [ ] Image upload works
- [ ] Voice input works
- [ ] Mobile responsive (test on phone)
- [ ] Streaming responses work

#### 5.3 Cost Verification
```sql
-- Check monthly costs per user
SELECT
    user_id,
    SUM(cost_usd) AS total_cost_usd,
    COUNT(*) AS message_count,
    COUNT(*) FILTER (WHERE message_type = 'chat') AS chat_count,
    COUNT(*) FILTER (WHERE message_type = 'log_confirmed') AS log_count
FROM coach_messages
WHERE created_at >= NOW() - INTERVAL '30 days'
GROUP BY user_id
ORDER BY total_cost_usd DESC;

-- Target: <$0.20/user/month
```

---

## 🚀 DEPLOYMENT STEPS

### 1. Backend Deployment
```bash
# 1. Run database migrations
psql -d your_database -f migrations/009_unified_coach_schema.sql

# 2. Deploy backend to Railway/Fly.io
git add .
git commit -m "feat: unified Coach interface (backend)"
git push origin main

# 3. Verify health check
curl https://api.wagnercoach.com/health
```

### 2. Frontend Deployment
```bash
# 1. Build and test locally
cd wagner-coach-clean
npm run build
npm run start

# 2. Deploy to Vercel
vercel --prod

# 3. Test on production URL
open https://wagnercoach.com/coach
```

### 3. Post-Deployment Verification
- [ ] Backend health check passes
- [ ] Frontend loads correctly
- [ ] Chat messages work
- [ ] Log detection works
- [ ] Confirm log saves data
- [ ] Check error logging (Sentry)
- [ ] Monitor costs (first 24 hours)
- [ ] Test on mobile (iOS + Android)

---

## 💰 COST TARGET VERIFICATION

**Monthly Cost per User:**
- Classification: 150 messages × $0.00001 = $0.0015
- Chat responses: 100 × $0.0015 = $0.15
- Log extractions: 50 × $0.0001 = $0.005
- Embeddings: FREE

**Total: $0.16/user/month** ✅ (Target: $0.50)

---

## 📊 SUCCESS METRICS

**The unified Coach is production-ready when:**

✅ Users can send any message (chat or log)
✅ Log detection is automatic and accurate (>90%)
✅ RAG context improves AI responses
✅ Chat history persists across sessions
✅ Response time <2 seconds (chat), <3 seconds (log)
✅ Cost stays under $0.20/user/month
✅ 95%+ message success rate
✅ Mobile UX is smooth (60fps scrolling)
✅ Users prefer it over old interface

---

## 📁 FILES REFERENCE

### ✅ Created (Backend)
- `app/services/message_classifier_service.py`
- `app/services/unified_coach_service.py`
- `docs/design/unified_coach_interface.md`
- `docs/database/QUICK_ENTRY_NEW_SCHEMA_UPDATE.md`

### 📝 To Create (Backend)
- `migrations/009_unified_coach_schema.sql`
- `app/api/v1/coach.py` (replace existing)

### 📝 To Create (Frontend)
- `app/coach/page.tsx` (new main page)
- `components/coach/MessageBubble.tsx`
- `components/coach/LogPreviewCard.tsx`
- `components/coach/ChatInput.tsx`
- `components/BottomNav.tsx` (update)

### 🗑️ To Delete (Frontend)
- `app/chat/page.tsx` (old AI chat)
- Related chat components

---

## ⏱️ TIME ESTIMATE

| Phase | Task | Time |
|-------|------|------|
| 1 | Backend API endpoints | 2-3h |
| 2 | Database migrations | 1-2h |
| 3 | Delete old frontend pages | 0.5h |
| 4 | Build new Coach UI | 6-8h |
| 5 | Testing & optimization | 2-3h |
| 6 | Deployment | 1h |
| **TOTAL** | | **12-17h** |

---

## 🎯 NEXT IMMEDIATE STEPS

1. **Create database migration** (`009_unified_coach_schema.sql`)
2. **Replace coach API** (`app/api/v1/coach.py`)
3. **Update router** to use new endpoints
4. **Test backend** with Postman
5. **Build frontend** components
6. **Test end-to-end**
7. **Deploy to staging**
8. **User testing**
9. **Deploy to production**

---

**Bottom Line: Backend architecture is 60% complete. Need to finish API endpoints, database migrations, and build entire frontend UI. Estimated 12-17 hours of focused work to reach production-ready state.**
