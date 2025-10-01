# Wagner Coach: Incremental Build Plan 🎯

**Philosophy:** Add ONE feature at a time. Keep app functional at every step.

**Date:** 2025-09-30
**Status:** Phase 1 Complete - Ready for Incremental Build

---

## 🎯 Core Principle

**After EACH increment, the app must be:**
1. ✅ Fully functional
2. ✅ Deployable to production
3. ✅ Testable by users
4. ✅ Providing value (even if limited)

**Benefits:**
- Lower risk (can stop/pivot anytime)
- Faster user feedback
- Clear progress milestones
- Easy to test and debug
- Can launch early and iterate

---

## 📋 Incremental Build Sequence

### ✅ INCREMENT 0: Foundation (DONE)
**Status:** Complete
**What Works:**
- Backend API running
- Database schema designed
- AI coach services implemented
- All tests passing

**What's Usable:** Nothing (migration not applied)

---

### 🎯 INCREMENT 1: Basic Coach Chat (Days 1-2)

**Goal:** Users can chat with AI trainer, get basic responses

**What to Build:**
1. [ ] Apply database migration
2. [ ] Create simple frontend chat page (`/coach/trainer`)
3. [ ] Wire up POST `/api/v1/coach/chat` endpoint
4. [ ] Test with manual curl/Postman first
5. [ ] Create basic chat UI (input box + message history)

**Implementation:**

```typescript
// app/coach/trainer/page.tsx
'use client'

import { useState } from 'react'

export default function TrainerChatPage() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)

  const sendMessage = async () => {
    if (!input.trim()) return

    const userMessage = { role: 'user', content: input }
    setMessages([...messages, userMessage])
    setInput('')
    setLoading(true)

    try {
      const response = await fetch('/api/coach/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          coach_type: 'trainer',
          message: input
        })
      })

      const data = await response.json()
      setMessages([...messages, userMessage, {
        role: 'assistant',
        content: data.message
      }])
    } catch (error) {
      console.error('Chat failed:', error)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Chat with Coach Alex</h1>

      <div className="space-y-4 mb-4 h-96 overflow-y-auto">
        {messages.map((msg, i) => (
          <div key={i} className={msg.role === 'user' ? 'text-right' : 'text-left'}>
            <div className={`inline-block p-3 rounded ${
              msg.role === 'user' ? 'bg-blue-500 text-white' : 'bg-gray-200'
            }`}>
              {msg.content}
            </div>
          </div>
        ))}
      </div>

      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && sendMessage()}
          placeholder="Ask your trainer..."
          className="flex-1 p-2 border rounded"
        />
        <button
          onClick={sendMessage}
          disabled={loading}
          className="px-4 py-2 bg-blue-500 text-white rounded"
        >
          {loading ? 'Sending...' : 'Send'}
        </button>
      </div>
    </div>
  )
}
```

```typescript
// app/api/coach/chat/route.ts
import { NextRequest, NextResponse } from 'next/server'

const BACKEND_URL = process.env.NEXT_PUBLIC_BACKEND_URL || 'http://localhost:8000'

export async function POST(req: NextRequest) {
  try {
    const body = await req.json()

    // Get auth token from session/cookie
    const token = req.headers.get('authorization') || 'Bearer demo-token'

    const response = await fetch(`${BACKEND_URL}/api/v1/coach/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': token
      },
      body: JSON.stringify(body)
    })

    const data = await response.json()
    return NextResponse.json(data)
  } catch (error) {
    return NextResponse.json({ error: 'Chat failed' }, { status: 500 })
  }
}
```

**Testing:**
1. Visit `/coach/trainer`
2. Type "What should I do today?"
3. Verify response appears
4. Try 5 different questions
5. Check responses are different each time

**Success Criteria:**
- ✅ Chat page loads
- ✅ Can send messages
- ✅ Receives responses from AI
- ✅ Messages display correctly
- ✅ No errors in console

**What's Usable After:** Users can chat with AI trainer (basic, but functional)

**Time:** 1-2 days

---

### 🎯 INCREMENT 2: Add Nutritionist Chat (Day 3)

**Goal:** Users can also chat with nutritionist

**What to Build:**
1. [ ] Create `/coach/nutritionist` page (copy trainer page)
2. [ ] Change `coach_type` to 'nutritionist'
3. [ ] Update UI to show Coach Maria instead of Coach Alex
4. [ ] Add navigation to switch between coaches

**Implementation:**

```typescript
// components/CoachNav.tsx
export function CoachNav() {
  return (
    <div className="flex gap-4 mb-4">
      <Link href="/coach/trainer" className="px-4 py-2 bg-blue-500 text-white rounded">
        🏋️ Trainer
      </Link>
      <Link href="/coach/nutritionist" className="px-4 py-2 bg-green-500 text-white rounded">
        🥗 Nutritionist
      </Link>
    </div>
  )
}
```

**Testing:**
1. Visit both `/coach/trainer` and `/coach/nutritionist`
2. Ask each coach relevant questions
3. Verify responses are different
4. Verify navigation works

**Success Criteria:**
- ✅ Both coaches accessible
- ✅ Trainer gives workout advice
- ✅ Nutritionist gives nutrition advice
- ✅ Navigation works

**What's Usable After:** Complete dual-coach chat system

**Time:** 4 hours

---

### 🎯 INCREMENT 3: Manual Workout Logging (Days 4-5)

**Goal:** Users can manually log a workout

**What to Build:**
1. [ ] Create `/workouts/log` page
2. [ ] Simple form: workout name, date, exercises
3. [ ] POST to Supabase `actual_workouts` table
4. [ ] Generate embedding for logged workout
5. [ ] Show success message

**Implementation:**

```typescript
// app/workouts/log/page.tsx
'use client'

export default function LogWorkoutPage() {
  const [workout, setWorkout] = useState({
    name: '',
    date: new Date().toISOString().split('T')[0],
    exercises: [{ name: '', sets: 3, reps: 10, weight: 0 }]
  })

  const addExercise = () => {
    setWorkout({
      ...workout,
      exercises: [...workout.exercises, { name: '', sets: 3, reps: 10, weight: 0 }]
    })
  }

  const saveWorkout = async () => {
    // Save to Supabase
    const { data, error } = await supabase
      .from('actual_workouts')
      .insert({
        name: workout.name,
        started_at: new Date(workout.date).toISOString(),
        duration_minutes: 60, // default
        exercises: workout.exercises
      })

    if (!error) {
      alert('Workout logged!')
      // Optionally: trigger embedding generation
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Log Workout</h1>

      <input
        placeholder="Workout Name"
        value={workout.name}
        onChange={(e) => setWorkout({ ...workout, name: e.target.value })}
        className="w-full p-2 border rounded mb-4"
      />

      <input
        type="date"
        value={workout.date}
        onChange={(e) => setWorkout({ ...workout, date: e.target.value })}
        className="w-full p-2 border rounded mb-4"
      />

      {workout.exercises.map((ex, i) => (
        <div key={i} className="grid grid-cols-4 gap-2 mb-2">
          <input
            placeholder="Exercise"
            value={ex.name}
            onChange={(e) => {
              const newEx = [...workout.exercises]
              newEx[i].name = e.target.value
              setWorkout({ ...workout, exercises: newEx })
            }}
            className="col-span-2 p-2 border rounded"
          />
          <input
            type="number"
            placeholder="Sets"
            value={ex.sets}
            onChange={(e) => {
              const newEx = [...workout.exercises]
              newEx[i].sets = parseInt(e.target.value)
              setWorkout({ ...workout, exercises: newEx })
            }}
            className="p-2 border rounded"
          />
          <input
            type="number"
            placeholder="Weight"
            value={ex.weight}
            onChange={(e) => {
              const newEx = [...workout.exercises]
              newEx[i].weight = parseInt(e.target.value)
              setWorkout({ ...workout, exercises: newEx })
            }}
            className="p-2 border rounded"
          />
        </div>
      ))}

      <button onClick={addExercise} className="mb-4 px-4 py-2 bg-gray-300 rounded">
        + Add Exercise
      </button>

      <button onClick={saveWorkout} className="w-full px-4 py-2 bg-blue-500 text-white rounded">
        Save Workout
      </button>
    </div>
  )
}
```

**Testing:**
1. Go to `/workouts/log`
2. Enter workout details
3. Click save
4. Verify saved in database
5. Chat with trainer and ask about this workout
6. Verify trainer references it

**Success Criteria:**
- ✅ Can log workout
- ✅ Workout saves to database
- ✅ Embedding generated
- ✅ Trainer can reference it in chat

**What's Usable After:** Users can log workouts and chat about them with AI

**Time:** 1-2 days

---

### 🎯 INCREMENT 4: Manual Meal Logging (Day 6)

**Goal:** Users can manually log meals

**What to Build:**
1. [ ] Create `/nutrition/log` page
2. [ ] Similar to workout logging
3. [ ] Save to `meals` table (or `meal_logs` if that exists)
4. [ ] Generate embedding
5. [ ] Nutritionist can reference it

**Implementation:** Similar to workout logging, simpler form

**Testing:**
1. Log a meal
2. Chat with nutritionist about it
3. Verify nutritionist references it

**Success Criteria:**
- ✅ Can log meals
- ✅ Meals save to database
- ✅ Nutritionist references them

**What's Usable After:** Complete manual logging system (workouts + meals)

**Time:** 1 day

---

### 🎯 INCREMENT 5: View History (Days 7-8)

**Goal:** Users can see their logged workouts and meals

**What to Build:**
1. [ ] Create `/workouts` page - list all workouts
2. [ ] Create `/nutrition` page - list all meals
3. [ ] Simple table/card view
4. [ ] Click to see details
5. [ ] Basic filtering (by date range)

**Implementation:**

```typescript
// app/workouts/page.tsx
export default async function WorkoutsPage() {
  const { data: workouts } = await supabase
    .from('actual_workouts')
    .select('*')
    .order('started_at', { ascending: false })
    .limit(20)

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Your Workouts</h1>

      <Link href="/workouts/log" className="mb-4 inline-block px-4 py-2 bg-blue-500 text-white rounded">
        + Log Workout
      </Link>

      <div className="space-y-4">
        {workouts?.map((workout) => (
          <div key={workout.id} className="p-4 border rounded">
            <h3 className="font-bold">{workout.name}</h3>
            <p className="text-sm text-gray-600">
              {new Date(workout.started_at).toLocaleDateString()}
            </p>
            <p className="text-sm">{workout.duration_minutes} minutes</p>
          </div>
        ))}
      </div>
    </div>
  )
}
```

**Testing:**
1. Log 3-5 workouts
2. Visit `/workouts`
3. Verify all show up
4. Verify sorted by date

**Success Criteria:**
- ✅ Can view workout history
- ✅ Can view meal history
- ✅ Data displays correctly

**What's Usable After:** Complete logging + viewing system

**Time:** 1-2 days

---

### 🎯 INCREMENT 6: Simple Dashboard (Day 9)

**Goal:** Homepage shows overview and quick actions

**What to Build:**
1. [ ] Update `/` homepage
2. [ ] Show: Recent workouts (3), Recent meals (3)
3. [ ] Quick action buttons: Log Workout, Log Meal, Chat with Trainer
4. [ ] Simple stats: Total workouts this week, Total meals logged

**Implementation:**

```typescript
// app/page.tsx
export default async function DashboardPage() {
  const { data: recentWorkouts } = await supabase
    .from('actual_workouts')
    .select('*')
    .order('started_at', { ascending: false })
    .limit(3)

  const { data: recentMeals } = await supabase
    .from('meals')
    .select('*')
    .order('consumed_at', { ascending: false })
    .limit(3)

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-3xl font-bold mb-8">Wagner Coach</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8">
        <Link href="/workouts/log" className="p-6 bg-blue-500 text-white rounded text-center">
          🏋️ Log Workout
        </Link>
        <Link href="/nutrition/log" className="p-6 bg-green-500 text-white rounded text-center">
          🥗 Log Meal
        </Link>
        <Link href="/coach/trainer" className="p-6 bg-purple-500 text-white rounded text-center">
          💬 Chat with Coach
        </Link>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div>
          <h2 className="text-xl font-bold mb-4">Recent Workouts</h2>
          {recentWorkouts?.map((w) => (
            <div key={w.id} className="mb-2 p-3 border rounded">
              <p className="font-semibold">{w.name}</p>
              <p className="text-sm text-gray-600">
                {new Date(w.started_at).toLocaleDateString()}
              </p>
            </div>
          ))}
          <Link href="/workouts" className="text-blue-500">View All →</Link>
        </div>

        <div>
          <h2 className="text-xl font-bold mb-4">Recent Meals</h2>
          {recentMeals?.map((m) => (
            <div key={m.id} className="mb-2 p-3 border rounded">
              <p className="font-semibold">{m.name}</p>
              <p className="text-sm text-gray-600">
                {m.calories} cal, {m.protein_grams}g protein
              </p>
            </div>
          ))}
          <Link href="/nutrition" className="text-blue-500">View All →</Link>
        </div>
      </div>
    </div>
  )
}
```

**Testing:**
1. Visit homepage
2. Verify recent items show
3. Click all quick actions
4. Verify navigation works

**Success Criteria:**
- ✅ Dashboard shows overview
- ✅ Quick actions work
- ✅ Navigation works
- ✅ Feels like a complete app

**What's Usable After:** Fully functional basic fitness tracker with AI coach

**Time:** 1 day

---

### 🎯 INCREMENT 7: Text-Based Quick Entry (Days 10-12)

**Goal:** "Just had eggs and toast" → automatically parsed and logged

**What to Build:**
1. [ ] Add quick entry input on dashboard
2. [ ] Use existing meal parser endpoint
3. [ ] Show parsed result for confirmation
4. [ ] Click confirm to save
5. [ ] Add to workout parser too

**Implementation:**

```typescript
// components/QuickEntry.tsx
'use client'

export function QuickEntry() {
  const [input, setInput] = useState('')
  const [parsed, setParsed] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleParse = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/nutrition/parse', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: input })
      })
      const data = await response.json()
      setParsed(data.meal)
    } catch (error) {
      console.error('Parse failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleConfirm = async () => {
    // Save to database
    const { error } = await supabase
      .from('meals')
      .insert(parsed)

    if (!error) {
      alert('Meal logged!')
      setInput('')
      setParsed(null)
    }
  }

  return (
    <div className="mb-8">
      <h2 className="text-xl font-bold mb-4">Quick Entry</h2>
      <div className="flex gap-2">
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="e.g., Just had eggs and toast"
          className="flex-1 p-3 border rounded"
        />
        <button
          onClick={handleParse}
          disabled={loading}
          className="px-6 py-3 bg-blue-500 text-white rounded"
        >
          {loading ? 'Parsing...' : 'Parse'}
        </button>
      </div>

      {parsed && (
        <div className="mt-4 p-4 border rounded">
          <h3 className="font-bold mb-2">Parsed Meal:</h3>
          <p><strong>Name:</strong> {parsed.name}</p>
          <p><strong>Calories:</strong> {parsed.calories}</p>
          <p><strong>Protein:</strong> {parsed.protein_grams}g</p>
          <div className="mt-4 flex gap-2">
            <button
              onClick={handleConfirm}
              className="px-4 py-2 bg-green-500 text-white rounded"
            >
              ✓ Confirm & Log
            </button>
            <button
              onClick={() => setParsed(null)}
              className="px-4 py-2 bg-gray-300 rounded"
            >
              ✗ Cancel
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
```

**Testing:**
1. Type "just had coffee and a bagel"
2. Click parse
3. Verify parsed correctly
4. Confirm and save
5. Check nutritionist chat references it

**Success Criteria:**
- ✅ Can parse natural language
- ✅ >70% accuracy
- ✅ User can edit before saving
- ✅ Saves correctly

**What's Usable After:** Easy text-based entry (big upgrade from manual forms)

**Time:** 2-3 days

---

### 🎯 INCREMENT 8: Voice Entry (Days 13-16) **CRITICAL**

**Goal:** Click mic button → speak → auto-parsed and logged

**What to Build:**
1. [ ] Add voice recording button to quick entry
2. [ ] Use browser MediaRecorder API
3. [ ] Send audio to backend
4. [ ] Backend: Whisper transcription → parse → return
5. [ ] Show parsed result for confirmation

**Implementation:**

```typescript
// components/VoiceInput.tsx
'use client'

export function VoiceInput({ onTranscript }) {
  const [isRecording, setIsRecording] = useState(false)
  const [mediaRecorder, setMediaRecorder] = useState(null)

  const startRecording = async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true })
      const recorder = new MediaRecorder(stream)
      const chunks = []

      recorder.ondataavailable = (e) => chunks.push(e.data)
      recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: 'audio/webm' })
        const formData = new FormData()
        formData.append('audio', blob)

        // Send to backend
        const response = await fetch('/api/voice/transcribe', {
          method: 'POST',
          body: formData
        })
        const data = await response.json()
        onTranscript(data.transcript)
      }

      recorder.start()
      setMediaRecorder(recorder)
      setIsRecording(true)
    } catch (error) {
      console.error('Microphone access denied:', error)
    }
  }

  const stopRecording = () => {
    if (mediaRecorder) {
      mediaRecorder.stop()
      setIsRecording(false)
    }
  }

  return (
    <button
      onClick={isRecording ? stopRecording : startRecording}
      className={`px-4 py-2 rounded ${
        isRecording ? 'bg-red-500 text-white animate-pulse' : 'bg-blue-500 text-white'
      }`}
    >
      {isRecording ? '🔴 Recording...' : '🎤 Voice Entry'}
    </button>
  )
}
```

```python
# Backend: app/api/v1/voice.py
@router.post("/transcribe")
async def transcribe_voice(
    audio: UploadFile,
    user_id: str = Depends(get_current_user)
):
    try:
        # Save temp file
        temp_path = f"/tmp/{user_id}_{uuid4()}.webm"
        with open(temp_path, "wb") as f:
            f.write(await audio.read())

        # Transcribe with Whisper
        with open(temp_path, "rb") as audio_file:
            transcript = await client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_file
            )

        # Clean up
        os.remove(temp_path)

        return {
            "success": True,
            "transcript": transcript.text
        }

    except Exception as e:
        logger.error(f"Transcription failed: {e}")
        raise HTTPException(status_code=500, detail="Transcription failed")
```

**Testing:**
1. Click voice button
2. Say "Just had eggs and toast"
3. Verify transcription appears
4. Verify auto-parses
5. Test 20+ voice entries
6. Measure accuracy

**Success Criteria:**
- ✅ Voice recording works
- ✅ Transcription accurate (>90%)
- ✅ Parsing accurate (>85%)
- ✅ Faster than manual entry
- ✅ Users prefer it

**What's Usable After:** Voice entry working - MAJOR feature

**Time:** 3-4 days

---

### 🎯 INCREMENT 9: Photo Entry (Days 17-20) **CRITICAL**

**Goal:** Take pic of meal → auto-parsed with nutrition

**What to Build:**
1. [ ] Add camera button to quick entry
2. [ ] Use mobile camera API
3. [ ] Send photo to backend
4. [ ] Backend: GPT-4 Vision analysis → parse → return
5. [ ] Show parsed result for confirmation

**Implementation:**

```typescript
// components/PhotoInput.tsx
'use client'

export function PhotoInput({ onMealParsed }) {
  const handleCapture = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    const formData = new FormData()
    formData.append('image', file)

    try {
      const response = await fetch('/api/photo/analyze', {
        method: 'POST',
        body: formData
      })
      const data = await response.json()
      onMealParsed(data.meal)
    } catch (error) {
      console.error('Photo analysis failed:', error)
    }
  }

  return (
    <label className="px-4 py-2 bg-green-500 text-white rounded cursor-pointer">
      📷 Photo Entry
      <input
        type="file"
        accept="image/*"
        capture="environment"
        className="hidden"
        onChange={handleCapture}
      />
    </label>
  )
}
```

```python
# Backend: app/api/v1/photo.py
@router.post("/analyze")
async def analyze_meal_photo(
    image: UploadFile,
    user_id: str = Depends(get_current_user)
):
    try:
        # Read image
        image_data = await image.read()
        base64_image = base64.b64encode(image_data).decode()

        # Analyze with GPT-4 Vision
        response = await client.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": "Analyze this meal photo. List all foods, estimate portions, and calculate nutrition (calories, protein, carbs, fat). Format as JSON."
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}"
                        }
                    }
                ]
            }],
            max_tokens=500
        )

        # Parse response
        analysis = json.loads(response.choices[0].message.content)

        return {
            "success": True,
            "meal": analysis,
            "confidence": "medium",  # Could extract from response
            "requires_confirmation": True
        }

    except Exception as e:
        logger.error(f"Photo analysis failed: {e}")
        raise HTTPException(status_code=500, detail="Analysis failed")
```

**Testing:**
1. Take photo of meal
2. Verify foods identified
3. Verify portions estimated
4. Test 50+ photos
5. Measure accuracy

**Success Criteria:**
- ✅ Photo capture works
- ✅ Food identification >80%
- ✅ Portion estimates reasonable
- ✅ Faster than manual entry
- ✅ Users find it useful

**What's Usable After:** Complete quick entry system (text + voice + photo)

**Time:** 3-4 days

---

### 🎯 INCREMENT 10: Weekly Recommendations (Days 21-22)

**Goal:** Coach generates weekly suggestions

**What to Build:**
1. [ ] Create `/recommendations` page
2. [ ] Button to generate recommendations
3. [ ] Show list of recommendations
4. [ ] Can accept/reject each one
5. [ ] Coach references accepted recommendations

**Implementation:**

```typescript
// app/recommendations/page.tsx
'use client'

export default function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState([])
  const [loading, setLoading] = useState(false)

  const generate = async () => {
    setLoading(true)
    try {
      const response = await fetch('/api/coach/recommendations/generate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ coach_type: 'trainer' })
      })
      const data = await response.json()
      setRecommendations(data.recommendations)
    } finally {
      setLoading(false)
    }
  }

  const updateStatus = async (id, status) => {
    await fetch(`/api/coach/recommendations/${id}`, {
      method: 'PATCH',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ status })
    })
    // Refresh list
    generate()
  }

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Your Recommendations</h1>

      <button
        onClick={generate}
        disabled={loading}
        className="mb-4 px-4 py-2 bg-blue-500 text-white rounded"
      >
        {loading ? 'Generating...' : '✨ Generate Weekly Recommendations'}
      </button>

      <div className="space-y-4">
        {recommendations.map((rec) => (
          <div key={rec.id} className="p-4 border rounded">
            <h3 className="font-bold mb-2">{rec.title}</h3>
            <p className="mb-2">{rec.description}</p>
            <p className="text-sm text-gray-600 mb-4">Reasoning: {rec.reasoning}</p>

            {rec.status === 'pending' && (
              <div className="flex gap-2">
                <button
                  onClick={() => updateStatus(rec.id, 'accepted')}
                  className="px-4 py-2 bg-green-500 text-white rounded"
                >
                  ✓ Accept
                </button>
                <button
                  onClick={() => updateStatus(rec.id, 'rejected')}
                  className="px-4 py-2 bg-red-500 text-white rounded"
                >
                  ✗ Reject
                </button>
              </div>
            )}

            {rec.status === 'accepted' && (
              <span className="text-green-600">✓ Accepted</span>
            )}
          </div>
        ))}
      </div>
    </div>
  )
}
```

**Testing:**
1. Generate recommendations
2. Verify they reference user data
3. Accept some, reject others
4. Chat with trainer about accepted recommendations
5. Verify trainer knows about them

**Success Criteria:**
- ✅ Recommendations are personalized
- ✅ Reference actual user data
- ✅ Are actionable
- ✅ Users find them helpful

**What's Usable After:** Complete MVP with recommendations

**Time:** 1-2 days

---

### 🎯 INCREMENT 11: Basic Analytics (Days 23-24)

**Goal:** Show progress charts

**What to Build:**
1. [ ] Create `/progress` page
2. [ ] Chart: Workouts per week (last 4 weeks)
3. [ ] Chart: Average calories per day
4. [ ] Chart: Protein intake over time
5. [ ] Use simple charting library (recharts)

**Implementation:**

```typescript
// app/progress/page.tsx
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip } from 'recharts'

export default async function ProgressPage() {
  // Fetch data for last 30 days
  const { data: workouts } = await supabase
    .from('actual_workouts')
    .select('started_at')
    .gte('started_at', new Date(Date.now() - 30*24*60*60*1000).toISOString())

  // Group by week
  const weeklyWorkouts = groupByWeek(workouts)

  return (
    <div className="max-w-4xl mx-auto p-4">
      <h1 className="text-2xl font-bold mb-8">Your Progress</h1>

      <div className="mb-8">
        <h2 className="text-xl font-bold mb-4">Workouts Per Week</h2>
        <LineChart width={600} height={300} data={weeklyWorkouts}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="week" />
          <YAxis />
          <Tooltip />
          <Line type="monotone" dataKey="count" stroke="#8884d8" />
        </LineChart>
      </div>

      {/* Similar charts for calories, protein, etc. */}
    </div>
  )
}
```

**Testing:**
1. Log data for 2-3 weeks
2. Visit progress page
3. Verify charts show correctly
4. Verify data accurate

**Success Criteria:**
- ✅ Charts display
- ✅ Data accurate
- ✅ Easy to understand
- ✅ Shows trends

**What's Usable After:** Complete app with analytics

**Time:** 1-2 days

---

### 🎯 INCREMENT 12: Mobile Optimization (Days 25-26)

**Goal:** App works great on mobile

**What to Build:**
1. [ ] Responsive design (already mostly there if using Tailwind)
2. [ ] PWA configuration
3. [ ] Add to home screen capability
4. [ ] Offline support (basic)
5. [ ] Touch-friendly buttons

**Implementation:**

```javascript
// public/sw.js (Service Worker for PWA)
self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open('wagner-coach-v1').then((cache) => cache.addAll([
      '/',
      '/coach/trainer',
      '/workouts',
      '/nutrition',
    ]))
  )
})
```

```typescript
// app/layout.tsx - Add PWA meta tags
export const metadata = {
  manifest: '/manifest.json',
  themeColor: '#3b82f6',
  viewport: 'width=device-width, initial-scale=1, maximum-scale=1',
}
```

**Testing:**
1. Test on iPhone
2. Test on Android
3. Verify all features work
4. Test camera/microphone on mobile
5. Test add to home screen

**Success Criteria:**
- ✅ Works on mobile
- ✅ Looks good on mobile
- ✅ Camera/mic work
- ✅ Can install as PWA

**What's Usable After:** Mobile-ready app

**Time:** 1-2 days

---

## 📊 After Each Increment

### Deployment Checklist

After EVERY increment:

1. [ ] Run tests locally
2. [ ] Test in browser
3. [ ] Commit to git
4. [ ] Push to GitHub
5. [ ] Deploy to Vercel (frontend auto-deploys)
6. [ ] Deploy to Railway (backend may need trigger)
7. [ ] Test on production
8. [ ] Get user feedback if possible

### User Testing

After increments 7, 8, 9, 10, 11:

1. [ ] Have 1-2 people test
2. [ ] Watch them use it
3. [ ] Note what confuses them
4. [ ] Note what they like
5. [ ] Iterate based on feedback

---

## 🎯 Decision Points

### After INCREMENT 7 (Text Quick Entry)
**Question:** Is text parsing accurate enough (>70%)?
- ✅ YES → Proceed to voice
- ❌ NO → Iterate on prompts, test more

### After INCREMENT 8 (Voice Entry)
**Question:** Is voice entry better than manual? (>85% accuracy)
- ✅ YES → This is THE feature, emphasize it
- ⚠️ 70-85% → Keep improving
- ❌ <70% → Might need to pivot

### After INCREMENT 9 (Photo Entry)
**Question:** Do users actually use photo entry?
- ✅ YES → You have something special
- ⚠️ SOMETIMES → Make it better
- ❌ NO → Focus on voice instead

### After INCREMENT 10 (Recommendations)
**Question:** Are recommendations helpful?
- ✅ YES → Generate them weekly automatically
- ⚠️ MIXED → Iterate on prompts
- ❌ NO → Maybe users just want chat

### After INCREMENT 11 (Analytics)
**Question:** Do users care about charts?
- ✅ YES → Add more analytics
- ⚠️ MIXED → Keep basic analytics
- ❌ NO → Don't build more

---

## 💰 Cost Tracking

Monitor costs after each increment:

| Increment | Feature | Est. Cost/User/Month |
|-----------|---------|---------------------|
| 1-2 | Chat | $0.50 |
| 7 | Text parsing | $0.20 |
| 8 | Voice | $0.30 |
| 9 | Photo | $0.50 |
| 10 | Recommendations | $0.10 |
| **TOTAL** | | **$1.60** |

**Red flags:**
- If any feature costs >$1/user → Optimize or limit
- If total >$3/user → Serious problem

---

## 📅 Timeline Summary

| Week | Increments | Features | Usable Product? |
|------|-----------|----------|-----------------|
| 1 | 1-4 | Chat + Manual logging | ✅ Basic tracker with AI |
| 2 | 5-7 | History + Dashboard + Text entry | ✅ Functional tracker |
| 3 | 8 | Voice entry | ✅ Quick entry working |
| 3-4 | 9 | Photo entry | ✅ Complete quick entry |
| 4 | 10-11 | Recommendations + Analytics | ✅ Full MVP |
| 4 | 12 | Mobile optimization | ✅ Production-ready |

**Total:** 4 weeks to full MVP

---

## 🎯 Success Metrics

### Week 1 Goals
- [ ] 5 test users
- [ ] All can chat with coach
- [ ] All can log workouts manually

### Week 2 Goals
- [ ] 10 test users
- [ ] Text quick entry >70% accurate
- [ ] Users logging 3+ items/week

### Week 3 Goals
- [ ] Voice entry >85% accurate
- [ ] 50% of entries via quick entry
- [ ] Users prefer quick entry over manual

### Week 4 Goals
- [ ] Photo entry working
- [ ] 50 test users
- [ ] Retention >60% at week 2
- [ ] Ready for public beta

---

## 🚨 Stop/Pivot Triggers

**Stop if:**
- After Increment 8, voice accuracy <65%
- After Increment 9, photo accuracy <60%
- After Week 3, retention <30%
- Costs >$5/user/month

**Pivot if:**
- Quick entry doesn't work, but chat is popular → Focus on chat-based coaching
- Analytics popular, quick entry not → Focus on analytics/tracking
- Users want programs, not chat → Focus on program generation

---

## ✅ Final Checklist Before Launch

After Increment 12:

1. [ ] All features working on production
2. [ ] Tested on iPhone and Android
3. [ ] At least 20 beta users have tried it
4. [ ] Retention >50% at week 2
5. [ ] Costs <$2/user/month
6. [ ] No critical bugs
7. [ ] Have positive user testimonials
8. [ ] Clear value proposition
9. [ ] Pricing decided ($10/month?)
10. [ ] Marketing plan ready

---

## 🎯 Bottom Line

**Philosophy:** Ship small, ship often, always keep it working

**Key Advantages:**
- Can test with users at ANY increment
- Can stop/pivot anytime
- Always have a working product
- Easy to debug (only changed one thing)
- Clear progress milestones

**Next Step:** Start Increment 1 - Apply migration and build basic chat

**Remember:** After EACH increment, the app should work. If it doesn't, fix it before moving to the next one.

**Let's build this incrementally! 🚀**
