# PATTERN-BASED ESTIMATION - Smart Logging for Returning Users

## Purpose
Use the user's **historical data** to make **smarter, more accurate estimates** based on their actual patterns.

This is the intelligence layer that makes Wagner Coach learn from each user's behavior.

---

## Core Principle

**Learn from the user's past. Estimate based on THEIR patterns, not generic assumptions.**

---

## 🧠 How It Works

### Step 1: Semantic Search
When user logs entry, search their past logs for **similar entries**:

```
User input: "morning run"
↓
Search multimodal_embeddings for similar past activities
↓
Find: 15 past "morning run" logs
↓
Analyze patterns in those logs
```

### Step 2: Pattern Extraction
Extract statistical patterns from similar past logs:

```json
{
  "pattern_type": "morning_run",
  "sample_size": 15,
  "patterns": {
    "typical_distance_km": 5.2,
    "distance_range": [3.8, 6.5],
    "typical_duration_min": 32,
    "duration_range": [25, 40],
    "typical_pace": "6:09/km",
    "typical_calories": 380,
    "typical_time": "07:15 AM",
    "consistency": 0.85
  }
}
```

### Step 3: Smart Estimation
Use patterns to make **confident estimates**:

```json
{
  "distance_km": 5.2,           // From user's pattern
  "duration_minutes": 32,        // From user's pattern
  "pace": "6:09/km",            // Calculated from pattern
  "calories_burned": 380,        // From user's pattern
  "confidence": 0.85,            // High (user is consistent)
  "estimated_from": "user_pattern"
}
```

---

## 📊 Pattern Recognition Rules

### Minimum Sample Size
- **3+ similar logs** → start using patterns
- **5+ similar logs** → confident patterns
- **10+ similar logs** → very confident patterns

### Similarity Threshold
- Semantic similarity > 0.7 → consider as "similar"
- Time context matches (morning/evening)
- Activity type matches

### Pattern Confidence
```python
if sample_size >= 10 and consistency >= 0.8:
    confidence = "high"  # 0.8-1.0
elif sample_size >= 5 and consistency >= 0.6:
    confidence = "medium"  # 0.6-0.8
elif sample_size >= 3:
    confidence = "low"  # 0.4-0.6
else:
    confidence = "baseline"  # Use THE_LINE
```

---

## 🎯 Pattern Types

### 1. Activity Patterns

#### Example: "morning run"
**User's History**:
- Last 15 morning runs: avg 5.2km in 32min
- Typical start time: 7:15 AM
- Typical calories: 380

**Smart Estimation**:
```json
{
  "start_date": "2025-10-05T07:15:00Z",  // User's typical time
  "duration_minutes": 32,                 // User's avg
  "distance_km": 5.2,                     // User's avg  ← SMART!
  "pace": "6:09/km",                      // Calculated
  "calories_burned": 380,                 // User's avg
  "confidence": 0.85,
  "estimated_from": "pattern (15 similar runs)"
}
```

### 2. Workout Patterns

#### Example: "chest workout"
**User's History**:
- Last 8 chest workouts typically include:
  - Bench Press: 185lbs, 4 sets, 8 reps
  - Incline DB Press: 70lbs, 3 sets, 10 reps
  - Cable Flyes: 30lbs, 3 sets, 12 reps
- Typical duration: 52min

**Smart Estimation**:
```json
{
  "started_at": "2025-10-05T14:30:00Z",
  "duration_minutes": 52,                 // User's avg
  "exercises": [                          // User's typical! ← SMART!
    {
      "name": "Bench Press",
      "sets": 4,
      "reps": 8,
      "weight_lbs": 185,
      "note": "Estimated from your typical chest workout"
    },
    {
      "name": "Incline Dumbbell Press",
      "sets": 3,
      "reps": 10,
      "weight_lbs": 70
    },
    {
      "name": "Cable Flyes",
      "sets": 3,
      "reps": 12,
      "weight_lbs": 30
    }
  ],
  "confidence": 0.75,
  "estimated_from": "pattern (8 similar workouts)"
}
```

### 3. Meal Patterns

#### Example: "chicken and rice"
**User's History**:
- Last 12 "chicken and rice" meals:
  - Avg: 6oz chicken, 1.5 cups rice
  - Avg macros: 520 cal, 55g protein, 52g carbs, 8g fat
  - Usually dinner (6:30 PM)

**Smart Estimation**:
```json
{
  "logged_at": "2025-10-05T18:30:00Z",   // User's typical time
  "meal_type": "dinner",
  "calories": 520,                        // User's avg ← SMART!
  "protein_g": 55,                        // User's avg
  "carbs_g": 52,                          // User's avg
  "fat_g": 8,
  "foods": [
    {"name": "Chicken breast", "quantity": "6 oz"},     // User's portion
    {"name": "Rice, cooked", "quantity": "1.5 cups"}    // User's portion
  ],
  "confidence": 0.80,
  "estimated_from": "pattern (12 similar meals)"
}
```

### 4. Exercise-Specific Patterns

#### Example: "bench pressed"
**User's History**:
- Last 10 bench press logs:
  - Avg weight: 185lbs
  - Avg sets: 4
  - Avg reps: 8
  - Typical progression: +5lbs every 2-3 weeks

**Smart Estimation**:
```json
{
  "exercises": [
    {
      "name": "Bench Press",
      "sets": 4,              // User's typical ← SMART!
      "reps": 8,              // User's typical
      "weight_lbs": 185,      // User's typical
      "note": "Estimated from your last 10 bench sessions"
    }
  ],
  "confidence": 0.85,
  "estimated_from": "pattern (10 bench press logs)"
}
```

---

## 🚦 Decision Flow

```
User logs: "morning run"
    ↓
Search past logs for "morning run" semantically similar entries
    ↓
Found 15 similar logs?
    ├─ YES → Extract patterns
    │         ├─ Distance avg: 5.2km (range 3.8-6.5km)
    │         ├─ Duration avg: 32min (range 25-40min)
    │         ├─ Consistency: 85%
    │         ↓
    │         Use pattern-based estimation:
    │         - distance_km: 5.2
    │         - duration_minutes: 32
    │         - confidence: 0.85
    │         - estimated_from: "user_pattern"
    │
    └─ NO → Use baseline (THE_LINE)
              - distance_km: null
              - duration_minutes: 35 (generic)
              - confidence: 0.5
              - estimated_from: "baseline"
```

---

## 📏 Pattern Boundaries (Don't Go Crazy)

### ✅ SAFE Pattern-Based Estimates

1. **Within user's typical range**
   - User runs 4-6km → estimate 5.2km ✅
   - DON'T estimate 10km if user never runs that far

2. **Recent patterns preferred**
   - Weight last 30 days: More relevant
   - Weight from 6 months ago: Less relevant

3. **Consistent patterns only**
   - User always does 4 sets bench → estimate 4 sets ✅
   - User varies 3-6 sets → estimate null (inconsistent)

4. **Clear matches**
   - "chest workout" matches past "chest workout" logs ✅
   - "upper body" is too vague → don't assume chest

### ⚠️ CONDITIONAL Pattern Use

1. **Time-based patterns**
   - "morning run" → use morning run patterns ✅
   - "run" → use all run patterns (morning + evening)

2. **Exercise variations**
   - "bench press" → use bench press patterns ✅
   - "chest workout" → use if user consistently does same exercises

3. **Portion sizes**
   - "chicken and rice" → use if user typically logs both together ✅
   - "chicken" → only chicken portions, not assumed sides

### ❌ NEVER Pattern-Estimate

1. **Wildly different context**
   - User logs "long run" but never runs >10km
   - DON'T estimate 15km just because it's "long"

2. **No clear pattern**
   - User's chest workouts are all different
   - DON'T pick one arbitrary workout

3. **Stale patterns**
   - User hasn't logged activity in 6+ months
   - Use baseline, not old patterns

4. **Sample size too small**
   - Only 1-2 similar logs
   - Use baseline, not "pattern"

---

## 🎯 Confidence Calculation

```python
def calculate_pattern_confidence(similar_logs, consistency_score, recency_score):
    """
    Calculate confidence in pattern-based estimate.

    Args:
        similar_logs: Number of similar past logs found
        consistency_score: 0-1, how consistent the pattern is
        recency_score: 0-1, how recent the pattern is

    Returns:
        confidence: 0-1
    """
    # Sample size factor
    if similar_logs >= 10:
        size_factor = 1.0
    elif similar_logs >= 5:
        size_factor = 0.8
    elif similar_logs >= 3:
        size_factor = 0.6
    else:
        return 0.5  # Use baseline

    # Combined score
    confidence = (size_factor * 0.4 +
                  consistency_score * 0.4 +
                  recency_score * 0.2)

    return min(confidence, 0.95)  # Cap at 0.95 (never 100% certain)
```

---

## 💡 Smart Suggestions Based on Patterns

### Example 1: Deviation Detection
```
User input: "morning run"
Pattern: Usually 5.2km in 32min
Estimate: 5.2km, 32min

Suggestion: "Your typical morning run is 5.2km in ~32min.
            Edit if today was different!"
```

### Example 2: Progress Tracking
```
User input: "bench press"
Pattern: Last month avg 180lbs → This month avg 185lbs (+5lbs)
Estimate: 185lbs

Suggestion: "You've increased bench press by 5lbs this month!
            Progressive overload working 💪"
```

### Example 3: Consistency Praise
```
User input: "morning run"
Pattern: 15 runs in last 30 days, very consistent
Estimate: 5.2km, 32min

Suggestion: "15 morning runs this month - you're crushing it!
            Consistency: 🔥"
```

---

## 🔄 Pattern Learning Flow

```
Log 1: "morning run, 5k in 30min"
  ↓
  Store with embedding
  ↓
  No pattern yet (only 1 log)

Log 2: "morning run, 5.5k in 33min"
  ↓
  Search finds Log 1 (similar)
  ↓
  Still too few (only 2 logs)

Log 3: "morning run, 4.8k in 28min"
  ↓
  Search finds Log 1 & 2
  ↓
  Pattern emerging! (3 logs)
  ↓
  Start using pattern: avg 5.1km, 30min
  ↓
  Confidence: LOW (only 3 samples)

Log 10: "morning run"
  ↓
  Search finds 9 similar logs
  ↓
  Strong pattern: avg 5.2km, 32min, consistency 85%
  ↓
  Estimate: 5.2km, 32min
  ↓
  Confidence: HIGH (10 samples, consistent)
```

---

## 🎮 Real-World Examples

### Scenario 1: Consistent Runner
**User Profile**:
- Runs 3-5 miles every Mon/Wed/Fri morning
- Usually 6:30-7:30 AM
- Pace: 8:00-8:30/mile
- 25 logged runs

**Input**: `"morning run"`

**Baseline Estimate** (new user):
```json
{
  "distance_km": null,
  "duration_minutes": 35,
  "confidence": 0.5
}
```

**Pattern-Based Estimate** (this user):
```json
{
  "start_date": "2025-10-05T06:45:00Z",  // User's typical time
  "distance_km": 6.2,                     // 4 miles avg
  "duration_minutes": 32,                 // User's avg
  "pace": "8:12/mile",                    // User's avg
  "calories_burned": 385,
  "confidence": 0.88,                     // HIGH
  "estimated_from": "pattern (25 similar runs)",
  "suggestion": "Your typical morning run: 4 miles in ~32min"
}
```

### Scenario 2: Structured Lifter
**User Profile**:
- Chest day every Monday
- Always does: Bench 185x8x4, Incline 70x10x3, Flyes 30x12x3
- Very consistent (12 logged chest workouts)

**Input**: `"chest workout"`

**Baseline Estimate** (new user):
```json
{
  "exercises": [],
  "duration_minutes": 50,
  "confidence": 0.5
}
```

**Pattern-Based Estimate** (this user):
```json
{
  "started_at": "2025-10-05T14:30:00Z",
  "duration_minutes": 48,
  "exercises": [
    {"name": "Bench Press", "sets": 4, "reps": 8, "weight_lbs": 185},
    {"name": "Incline DB Press", "sets": 3, "reps": 10, "weight_lbs": 70},
    {"name": "Cable Flyes", "sets": 3, "reps": 12, "weight_lbs": 30}
  ],
  "confidence": 0.82,
  "estimated_from": "pattern (12 chest workouts)",
  "suggestion": "Your typical chest routine loaded. Adjust weights if you progressed!"
}
```

### Scenario 3: Meal Prep Person
**User Profile**:
- Meal preps chicken+rice+broccoli every Sunday
- Eats same portion for lunch Mon-Fri
- 20 logged identical meals

**Input**: `"lunch"`

**Baseline Estimate** (new user):
```json
{
  "foods": [],
  "calories": null,
  "confidence": 0.3
}
```

**Pattern-Based Estimate** (this user):
```json
{
  "logged_at": "2025-10-05T12:30:00Z",
  "meal_type": "lunch",
  "calories": 485,
  "protein_g": 52,
  "carbs_g": 48,
  "fat_g": 8,
  "foods": [
    {"name": "Chicken breast", "quantity": "6 oz"},
    {"name": "Brown rice", "quantity": "1.5 cups"},
    {"name": "Broccoli", "quantity": "2 cups"}
  ],
  "confidence": 0.92,                      // VERY HIGH
  "estimated_from": "pattern (20 identical lunches)",
  "suggestion": "Your usual meal prep lunch loaded. Edit if different today!"
}
```

---

## 🚨 Safety Rails

### Don't Go Crazy - Even With Patterns

1. **Cap estimates at pattern range**
   - User runs 3-6km → estimate within 3-6km
   - DON'T estimate 8km even if "felt long"

2. **Require minimum consistency**
   - Consistency < 60% → don't use pattern
   - User varies too much → use baseline

3. **Age out stale patterns**
   - No logs in 60 days → use baseline
   - Patterns must be recent to be relevant

4. **Allow user deviation**
   - Always provide "Edit" option
   - Show that estimate is from pattern
   - Never force pattern on user

5. **Detect behavior changes**
   - User normally runs 5k, suddenly logs 10k
   - DON'T auto-estimate 5k for next run
   - Adapt to new pattern

---

## Summary

**Pattern-Based Estimation makes Wagner Coach learn from each user**:

- ✅ New users: Conservative baseline (THE_LINE)
- ✅ 3-5 logs: Start using patterns (low confidence)
- ✅ 5-10 logs: Confident patterns (medium confidence)
- ✅ 10+ logs: Very confident patterns (high confidence)

**The app gets smarter with every log.**

**But never goes crazy** - always within user's typical behavior, with clear confidence levels and edit options.
