# Unified Coach Interface - Production Architecture

**Feature:** Single AI-powered chat interface for ALL interactions
**Replaces:** AI Chat page + Quick Entry page
**Name:** "Coach" (bottom navigation)
**Date:** 2025-10-06

---

## 🎯 Vision

**ONE unified interface where users:**
- Ask questions → Get AI answers
- Log meals → AI extracts data → User confirms → Saved
- Log workouts → AI extracts data → User confirms → Saved
- Have conversations → AI remembers context from ALL their data
- See their history → All interactions in one chat thread

**Like ChatGPT, but fitness-focused with automatic data logging**

---

## 🏗️ Architecture

### Message Flow

```
USER SENDS MESSAGE
    ↓
[STEP 1] Classify Message Type (Groq - $0.05/M tokens)
    ├─ Is this a CHAT? (question, comment, conversation)
    └─ Is this a LOG? (meal, workout, measurement)
    ↓
    ├─────────────────────────────┬─────────────────────────────┐
    ↓                             ↓                             ↓
IF CHAT                      IF LOG                      IF AMBIGUOUS
    ↓                             ↓                             ↓
[STEP 2A] CHAT MODE          [STEP 2B] LOG MODE          Ask for clarification
    ↓                             ↓
Retrieve RAG context         Classify log type
(meals, workouts, etc.)      (meal, workout, measurement)
    ↓                             ↓
Generate AI response         Extract structured data
(Claude - streaming)         (Groq classification)
    ↓                             ↓
Vectorize user message       Show PREVIEW CARD in chat
    ↓                             ↓
Vectorize AI response        User reviews/edits
    ↓                             ↓
Store in coach_messages      User confirms
    ↓                             ↓
Display to user              Save to structured tables
                                  ↓
                             Vectorize log
                                  ↓
                             Show confirmation in chat
```

---

## 📊 Database Schema

### Use Existing `coach_messages` Table (Enhanced)

```sql
-- coach_messages already has:
id UUID
user_id UUID
conversation_id UUID  -- Group messages together
role TEXT  -- 'user' | 'assistant' | 'system'
content TEXT
created_at TIMESTAMPTZ

-- ADD these columns:
message_type TEXT CHECK (message_type IN ('chat', 'log_preview', 'log_confirmed', 'system'))
metadata JSONB  -- Store extra data
quick_entry_log_id UUID  -- Link to quick_entry_logs (if log)
context_used JSONB  -- RAG context sources
tokens_used INTEGER
cost_usd NUMERIC(10, 6)
embedding_id UUID  -- Link to embeddings table
is_vectorized BOOLEAN DEFAULT FALSE
```

### Message Types:
- **`chat`** - Regular Q&A conversation
- **`log_preview`** - AI detected a log, showing preview
- **`log_confirmed`** - User confirmed the log
- **`system`** - System messages (e.g., "Meal logged successfully")

---

## 🤖 Backend Services

### 1. Unified Coach Service (`coach_service_v2.py`)

```python
class UnifiedCoachService:
    """
    Handles ALL user interactions in one chat interface.

    Modes:
    - CHAT: Questions, comments, conversations
    - LOG: Meal/workout/measurement logging
    """

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_id: str,
        image_base64: Optional[str] = None,
        audio_base64: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Process ANY user message and route appropriately.

        Returns:
            {
                "mode": "chat" | "log_preview",
                "response": "..." (for chat mode),
                "log_preview": {...} (for log mode),
                "conversation_id": "...",
                "message_id": "..."
            }
        """

        # STEP 1: Classify message (cheap Groq)
        classification = await self._classify_message(message, image_base64)

        if classification["is_log"]:
            # LOG MODE: Extract structured data
            return await self._handle_log_mode(
                user_id, message, conversation_id, classification
            )
        else:
            # CHAT MODE: Generate AI response
            return await self._handle_chat_mode(
                user_id, message, conversation_id, image_base64
            )

    async def confirm_log(
        self,
        user_id: str,
        conversation_id: str,
        log_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        User confirmed the log preview - save it.
        """
        # Use existing Quick Entry save logic
        # Add success message to conversation
```

---

### 2. Message Classifier (`message_classifier_service.py`)

```python
async def classify_message(message: str, has_image: bool) -> Dict[str, Any]:
    """
    Classify: Is this CHAT or LOG?

    Uses Groq Llama 3.3 70B ($0.05/M tokens) for speed & cost.

    Returns:
        {
            "is_log": bool,
            "log_type": "meal" | "workout" | "measurement" | None,
            "confidence": 0.0-1.0,
            "reasoning": "..."
        }
    """

    system_prompt = """
    Classify if this is a FITNESS LOG or a CHAT message.

    FITNESS LOG indicators:
    - Mentions eating/food ("I ate...", "Had lunch", "Breakfast was...")
    - Mentions exercise ("Did 10 pushups", "Ran 5K", "Bench pressed...")
    - Mentions measurements ("Weight is 175 lbs", "Body fat 15%")
    - Past tense about activities
    - Specific numbers (calories, reps, weight, distance)

    CHAT indicators:
    - Questions ("What should I eat?", "How many calories?")
    - Requests for advice ("Can you help me with...")
    - General conversation ("How's it going?", "Thanks!")
    - Future/hypothetical ("What if I...", "Should I...")

    Return JSON:
    {
        "is_log": true/false,
        "log_type": "meal"|"workout"|"measurement"|null,
        "confidence": 0.0-1.0,
        "reasoning": "brief explanation"
    }
    """
```

---

### 3. RAG Context Builder (Enhanced)

```python
async def build_comprehensive_context(
    user_id: str,
    query: str,
    max_results: int = 10
) -> str:
    """
    Build RAG context from ALL user data.

    Searches:
    - quick_entry_embeddings (meals, workouts, notes)
    - coach_messages embeddings (previous chats)
    - Any other vectorized data

    Returns formatted context string for AI.
    """

    # Generate query embedding
    query_embedding = await embedding_service.embed_text(query)

    # Search quick_entry_embeddings
    quick_entries = await search_quick_entry_embeddings(
        user_id=user_id,
        query_embedding=query_embedding,
        limit=5
    )

    # Search coach_messages embeddings
    past_chats = await search_coach_messages_embeddings(
        user_id=user_id,
        query_embedding=query_embedding,
        limit=5
    )

    # Build context string
    context = []

    # Add relevant quick entries
    for entry in quick_entries:
        context.append(f"[{entry['source_classification'].upper()}] {entry['content_summary']}")

    # Add relevant past chats
    for chat in past_chats:
        context.append(f"[CHAT] {chat['content'][:200]}")

    return "\n\n".join(context)
```

---

## 🎨 Frontend UI Design

### ChatGPT-like Interface

```
┌────────────────────────────────────┐
│ Coach                           [≡] │  ← Top bar with menu
├────────────────────────────────────┤
│                                    │
│  ┌──────────────────┐             │  ← AI message (left)
│  │ Hi! I'm your AI  │             │
│  │ fitness coach.   │             │
│  │ How can I help?  │             │
│  └──────────────────┘             │
│                                    │
│             ┌──────────────────┐  │  ← User message (right)
│             │ I ate 3 eggs and │  │
│             │ oatmeal          │  │
│             └──────────────────┘  │
│                                    │
│  ┌────────────────────────────┐   │  ← Log preview card
│  │ 🍳 Meal Detected           │   │
│  │                            │   │
│  │ Breakfast                  │   │
│  │ • 3 eggs                   │   │
│  │ • Oatmeal (1 cup)          │   │
│  │                            │   │
│  │ 450 cal | 28g protein      │   │
│  │                            │   │
│  │ [Edit] [Confirm]           │   │
│  └────────────────────────────┘   │
│                                    │
│  ┌──────────────────┐             │  ← AI confirmation
│  │ ✅ Meal logged!  │             │
│  └──────────────────┘             │
│                                    │
│             ┌──────────────────┐  │  ← Next user message
│             │ What should I    │  │
│             │ eat for lunch?   │  │
│             └──────────────────┘  │
│                                    │
│  ┌──────────────────┐             │  ← AI chat response
│  │ Based on your    │             │
│  │ breakfast, I     │             │
│  │ recommend...     │             │
│  └──────────────────┘             │
│                                    │
│  [Load more...]                   │
│                                    │
├────────────────────────────────────┤
│ [🎤] [📷]  Type message...    [➤]│  ← Input at bottom
└────────────────────────────────────┘
```

---

### UI Components

#### 1. Message Bubble (`MessageBubble.tsx`)
```typescript
type MessageBubbleProps = {
  role: 'user' | 'assistant';
  content: string;
  timestamp: string;
  isStreaming?: boolean;
};

// User messages: Right-aligned, blue background
// AI messages: Left-aligned, gray background
// Streaming: Show typing indicator
```

#### 2. Log Preview Card (`LogPreviewCard.tsx`)
```typescript
type LogPreviewCardProps = {
  logType: 'meal' | 'workout' | 'measurement';
  extractedData: any;
  onEdit: () => void;
  onConfirm: () => void;
  onCancel: () => void;
};

// Special card UI for log previews
// Shows extracted data in readable format
// Edit/Confirm buttons
```

#### 3. Chat Input (`ChatInput.tsx`)
```typescript
// Multi-line text input
// Voice button (speech-to-text)
// Image button (camera/gallery)
// Send button
// Shows "AI is typing..." indicator
```

---

## 🔄 User Flows

### Flow 1: Chat (Q&A)

```
User: "What should I eat for breakfast?"
    ↓
System: Classify → CHAT mode
    ↓
System: Retrieve RAG context (recent meals, preferences)
    ↓
AI: "Based on your recent meals, I recommend..."
    ↓
System: Vectorize user question
System: Vectorize AI response
    ↓
Display AI response in chat
```

---

### Flow 2: Log Detection

```
User: "I ate 3 eggs and oatmeal for breakfast"
    ↓
System: Classify → LOG mode (meal)
    ↓
System: Extract structured data
    ↓
Display LOG PREVIEW CARD:
    ┌────────────────────────────┐
    │ 🍳 Meal Detected           │
    │ Breakfast                  │
    │ • 3 eggs                   │
    │ • Oatmeal (1 cup)          │
    │ 450 cal | 28g protein      │
    │ [Edit] [Confirm]           │
    └────────────────────────────┘
    ↓
User clicks [Confirm]
    ↓
System: Save to meal_logs
System: Vectorize log
System: Create quick_entry_logs
    ↓
Display confirmation:
    "✅ Breakfast logged! 450 calories"
```

---

### Flow 3: Mixed Conversation

```
User: "I ate chicken and rice. Was that enough protein?"
    ↓
System: Classify → LOG + CHAT (dual mode)
    ↓
System:
  1. Extract log (chicken and rice meal)
  2. Prepare to answer question
    ↓
Display LOG PREVIEW CARD first
    ↓
User confirms log
    ↓
System: Now answer the question with RAG context
    ↓
AI: "Yes! Your meal had 45g protein, which meets your daily target..."
```

---

## 💾 Data Storage

### Every Message is Stored

```sql
-- Example: User asks question
INSERT INTO coach_messages (
    user_id, conversation_id, role, content, message_type,
    created_at
) VALUES (
    'user-abc', 'conv-123', 'user',
    'What should I eat for breakfast?',
    'chat',
    NOW()
);

-- AI response
INSERT INTO coach_messages (
    user_id, conversation_id, role, content, message_type,
    tokens_used, cost_usd, context_used,
    created_at
) VALUES (
    'user-abc', 'conv-123', 'assistant',
    'Based on your recent meals, I recommend...',
    'chat',
    500, 0.0015,
    '{"sources": ["meal from 2025-10-05", "workout from 2025-10-04"]}',
    NOW()
);

-- Both messages get vectorized
INSERT INTO coach_message_embeddings (
    message_id, user_id, embedding, content_text, ...
);
```

---

### Log Messages Linked

```sql
-- User sends log
INSERT INTO coach_messages (
    user_id, conversation_id, role, content, message_type,
    created_at
) VALUES (
    'user-abc', 'conv-123', 'user',
    'I ate 3 eggs and oatmeal',
    'log_preview',
    NOW()
);

-- After confirmation, link to structured log
UPDATE coach_messages
SET message_type = 'log_confirmed',
    quick_entry_log_id = 'qe-12345',
    metadata = '{"meal_log_id": "meal-67890"}'
WHERE id = 'msg-456';

-- Add confirmation message
INSERT INTO coach_messages (
    user_id, conversation_id, role, content, message_type,
    created_at
) VALUES (
    'user-abc', 'conv-123', 'system',
    '✅ Breakfast logged! 450 calories, 28g protein',
    'system',
    NOW()
);
```

---

## 💰 Cost Analysis

### Per-Message Costs

| Action | Model | Cost per Message |
|--------|-------|------------------|
| Classification | Groq Llama 3.3 70B | $0.00001 (100 tokens) |
| Chat Response | Claude 3.5 Sonnet | $0.0015 (500 tokens) |
| Log Extraction | Groq Llama 3.3 70B | $0.0001 (200 tokens) |
| Embeddings | FREE (sentence-transformers) | $0.00 |

### Monthly User Estimate

Assume per month:
- 100 chat messages
- 50 log entries
- 150 total AI interactions

**Costs:**
- Classification: 150 × $0.00001 = $0.0015
- Chat responses: 100 × $0.0015 = $0.15
- Log extractions: 50 × $0.0001 = $0.005
- Embeddings: FREE

**Total: $0.16/user/month** ✅ (Well under $0.50 target!)

---

## 🔐 Security & Rate Limiting

### Rate Limits
- **Chat messages**: 200/day per user
- **Log entries**: 100/day per user
- **Total messages**: 300/day per user

### Data Privacy
- All messages encrypted at rest
- RLS policies on coach_messages table
- Users can only see their own conversations
- Option to delete conversation history

---

## 📱 Mobile Optimization

### Performance
- Lazy load chat history (paginated)
- Virtual scrolling for long conversations
- Optimistic UI updates (instant message display)
- Background vectorization (don't block UI)

### UX
- Tap to retry failed messages
- Swipe to delete message
- Pull to refresh chat history
- Haptic feedback on actions

---

## ✅ Production Checklist

### Backend
- [ ] Create `coach_service_v2.py` with dual-mode logic
- [ ] Implement message classifier (Groq)
- [ ] Enhance RAG context builder (all embeddings)
- [ ] Create unified API endpoint `POST /api/v1/coach/message`
- [ ] Create chat history endpoint `GET /api/v1/coach/conversations`
- [ ] Implement streaming responses (SSE)
- [ ] Vectorize ALL messages (user + AI)
- [ ] Add message retry logic
- [ ] Add rate limiting
- [ ] Add cost tracking
- [ ] Error handling & fallbacks
- [ ] Database migrations

### Frontend
- [ ] Delete AI Chat page
- [ ] Rename "Quick Entry" → "Coach" in navigation
- [ ] Build ChatGPT-like interface
- [ ] Message bubbles (user/AI)
- [ ] Streaming message display
- [ ] Log preview card component
- [ ] Edit log UI
- [ ] Chat history (infinite scroll)
- [ ] Voice input (speech-to-text)
- [ ] Image input (camera/gallery)
- [ ] Loading states
- [ ] Error handling
- [ ] Offline support
- [ ] Mobile responsive

### Testing
- [ ] E2E: Chat message flow
- [ ] E2E: Log detection & confirmation
- [ ] E2E: Mixed conversation
- [ ] RAG context accuracy
- [ ] Streaming works correctly
- [ ] Chat history loads
- [ ] Vectorization verified
- [ ] Cost tracking verified
- [ ] Rate limiting works
- [ ] Mobile responsive (iOS + Android)

---

## 🚀 Migration Plan

### Phase 1: Backend (Week 1)
1. Create new coach service with dual logic
2. Implement message classifier
3. Enhance RAG context builder
4. Create unified API endpoints
5. Test with Postman

### Phase 2: Frontend (Week 2)
1. Build new Coach UI
2. Delete old AI Chat page
3. Update navigation
4. Implement streaming
5. Test on mobile

### Phase 3: Migration (Week 3)
1. Deploy backend to staging
2. Deploy frontend to staging
3. User testing
4. Bug fixes
5. Deploy to production

### Phase 4: Cleanup (Week 4)
1. Remove old Quick Entry code
2. Remove old AI Chat code
3. Update documentation
4. Monitor costs & performance

---

## 📊 Success Metrics

**The Coach interface is successful when:**

✅ Users can chat naturally with AI
✅ Logs are detected automatically
✅ Confirmation flow is smooth
✅ RAG context is accurate
✅ Responses are fast (<2 seconds)
✅ Cost stays under $0.20/user/month
✅ 95%+ message success rate
✅ Users prefer it over old interface

---

**Bottom Line: One unified "Coach" interface that feels like ChatGPT but automatically logs fitness data. Production-ready with full RAG, cost tracking, and seamless UX.**
