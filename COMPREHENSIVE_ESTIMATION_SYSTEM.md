# Comprehensive Estimation System - Wagner Coach Quick Entry

## Overview

Wagner Coach Quick Entry now provides **intelligent comprehensive estimation** for ALL log types, ensuring that every entry - no matter how vague - receives:

1. **Mandatory timestamps** with intelligent time inference
2. **Complete field estimates** for all relevant data (calories, duration, distance, etc.)
3. **Appropriate confidence levels** based on input specificity
4. **Actionable suggestions** for improving accuracy

## Philosophy

**Users should be able to log ANYTHING, ANYTIME, with ANY level of detail - and always get useful estimates.**

- Vague input: "ate chicken" → Full nutritional estimate with assumed portions
- Time context: "morning run" → Timestamp inferred as 7:00 AM today
- Minimal data: "chest workout" → Typical exercises, duration, and calories estimated

The system NEVER returns null for core fields. It always provides best-guess estimates with appropriate confidence levels and guidance for improvement.

---

## 🕐 Timestamp Inference System

### Core Principle
**Every log MUST have a timestamp.** The AI infers time from context clues or uses current time as fallback.

### Time Inference Rules

#### Meal-Related Keywords
| User Input | Inferred Time | Field Name |
|------------|---------------|------------|
| "ate chicken" | Current time | `logged_at` |
| "had breakfast" | Today 7:30 AM | `logged_at` |
| "eggs for breakfast" | Today 7:30 AM | `logged_at` |
| "lunch was a burrito" | Today 12:30 PM | `logged_at` |
| "dinner last night" | Yesterday 6:30 PM | `logged_at` |
| "snack earlier" | 2 hours ago | `logged_at` |
| "pre-workout meal" | 1 hour ago | `logged_at` |
| "post-workout shake" | 30 minutes ago | `logged_at` |

#### Activity-Related Keywords
| User Input | Inferred Time | Field Name |
|------------|---------------|------------|
| "went for a run" | Current time or last hour | `start_date` |
| "morning run" | Today 7:00 AM | `start_date` |
| "ran after work" | Today 5:30 PM | `start_date` |
| "cycling yesterday" | Yesterday 3:00 PM | `start_date` |
| "evening walk" | Today 7:00 PM | `start_date` |

#### Workout-Related Keywords
| User Input | Inferred Time | Field Names |
|------------|---------------|-------------|
| "bench pressed" | Current time | `started_at`, `completed_at` |
| "morning workout" | Today 7:00 AM | `started_at`, `completed_at` |
| "lifted after work" | Today 5:30 PM | `started_at`, `completed_at` |
| "leg day yesterday" | Yesterday 4:00 PM | `started_at`, `completed_at` |

#### Measurement Keywords
| User Input | Inferred Time | Field Name |
|------------|---------------|------------|
| "weighed myself" | Current time | `measured_at` |
| "morning weigh-in" | Today 7:00 AM | `measured_at` |

#### Meal Type Inference from Time
When time is known but meal type isn't specified:

- **6:00 AM - 10:00 AM** → `breakfast`
- **11:00 AM - 2:00 PM** → `lunch`
- **5:00 PM - 9:00 PM** → `dinner`
- **All other times** → `snack`

---

## 🍽️ Meal Log Estimation

### Always Estimated Fields

| Field | Estimation Logic | Example |
|-------|------------------|---------|
| `logged_at` | Time inference + current time fallback | "2025-10-05T12:30:00Z" |
| `meal_type` | Inferred from time or keywords | "lunch" |
| `calories` | Based on typical portions | 450 |
| `protein_g` | Based on typical portions | 50 |
| `carbs_g` | Based on typical portions | 45 |
| `fat_g` | Based on typical portions | 6 |
| `fiber_g` | When possible | 2 |
| `sugar_g` | When possible | 0 |
| `sodium_mg` | When possible | 200 |

### Portion Assumptions (when not specified)

| Food Type | Assumed Portion |
|-----------|----------------|
| Chicken/meat | 4-6 oz |
| Eggs | 2-3 eggs |
| Rice (cooked) | 1 cup |
| Pasta (cooked) | 1 cup |
| Vegetables | 1-2 cups |
| Protein powder | 1 scoop |

### Examples

#### Vague Input
**Input:** `"ate chicken"`

**Output:**
- `logged_at`: "2025-10-05T14:30:00Z" (current time)
- `meal_type`: "snack" (based on 2:30 PM)
- `calories`: 235
- `protein_g`: 44
- `carbs_g`: 0
- `fat_g`: 5
- Confidence: 0.5 (low)
- Suggestion: "Estimated 5oz chicken breast. For accuracy, add portions and sides."

#### Time Context
**Input:** `"had eggs for breakfast"`

**Output:**
- `logged_at`: "2025-10-05T07:30:00Z" (breakfast time)
- `meal_type`: "breakfast"
- `calories`: 216 (3 eggs)
- `protein_g`: 18
- `carbs_g`: 1.2
- `fat_g`: 15
- Confidence: 0.6 (medium)
- Suggestion: "Assumed 3 eggs. Specify if different: '2 eggs' or '4 eggs'."

#### Restaurant Meal
**Input:** `"Chicken Margherita at Olive Garden"`

**Output:**
- `logged_at`: "2025-10-05T19:00:00Z" (current time, dinner)
- `meal_type`: "dinner"
- `calories`: 870
- `protein_g`: 62
- `carbs_g`: 48
- `fat_g`: 38
- `fiber_g`: 5
- `sodium_mg`: 1580
- Confidence: 0.85 (high)
- Suggestion: "Restaurant portions vary - estimated from menu data."

---

## 🏃 Activity Log Estimation

### Always Estimated Fields

| Field | Estimation Logic | Example |
|-------|------------------|---------|
| `start_date` | Time inference + current time fallback | "2025-10-05T07:00:00Z" |
| `activity_type` | Extracted from text | "running" |
| `duration_minutes` | Typical duration for activity type | 35 |
| `distance_km` | Based on duration + typical pace | 5.5 |
| `distance_miles` | Converted from km | 3.4 |
| `calories_burned` | Based on activity + duration | 420 |
| `pace` | Calculated from distance + duration | "6:22/km" |
| `rpe` (1-10) | Inferred from context words | 5 |
| `mood` | Inferred from context words | "good" |

### Duration Assumptions (when not specified)

| Activity | Assumed Duration |
|----------|-----------------|
| "went for a run" | 30-40 minutes |
| "easy run" | 35-45 minutes |
| "long run" | 60-90 minutes |
| "quick workout" | 20-30 minutes |
| "cycling" | 45-60 minutes |

### RPE Inference

| Context Words | Inferred RPE |
|---------------|-------------|
| "easy", "light", "recovery" | 3-4 |
| "moderate", "steady" | 5-6 |
| "hard", "tough", "challenging" | 7-8 |
| "max effort", "all out" | 9-10 |

### Examples

#### Vague Input
**Input:** `"went for a run this morning"`

**Output:**
- `start_date`: "2025-10-05T07:00:00Z" (morning time)
- `activity_type`: "running"
- `duration_minutes`: 35
- `distance_km`: 5.5
- `calories_burned`: 420
- `pace`: "6:22/km"
- `rpe`: 5
- Confidence: 0.5 (low)
- Suggestion: "Estimated ~35min, 5.5km based on typical morning run."

#### Effort Context
**Input:** `"easy 10k after work"`

**Output:**
- `start_date`: "2025-10-05T17:30:00Z" (after work)
- `activity_type`: "running"
- `distance_km`: 10
- `duration_minutes`: 65
- `calories_burned`: 750
- `pace`: "6:30/km"
- `rpe`: 4 (easy)
- Confidence: 0.75 (medium-high)
- Suggestion: "Duration estimated for easy pace. Confirm actual time."

---

## 💪 Workout Log Estimation

### Always Estimated Fields

| Field | Estimation Logic | Example |
|-------|------------------|---------|
| `started_at` | Time inference + current time fallback | "2025-10-05T07:00:00Z" |
| `completed_at` | started_at + duration | "2025-10-05T07:50:00Z" |
| `duration_minutes` | Typical duration for workout type | 50 |
| `exercises` | Typical exercises for workout type | Array of exercises |
| `estimated_calories` | Based on duration + intensity | 300 |
| `muscle_groups` | Inferred from exercises | ["chest", "triceps"] |
| `rpe` | Inferred from context | 6 |

### Workout Type Defaults

When user says "chest day" or "leg day" without specifics:

#### Chest Day
```json
[
  {"name": "Bench Press", "sets": 4, "reps": "8-10"},
  {"name": "Incline Dumbbell Press", "sets": 3, "reps": "10-12"},
  {"name": "Cable Flyes", "sets": 3, "reps": 12}
]
```

#### Leg Day
```json
[
  {"name": "Squats", "sets": 4, "reps": "6-8"},
  {"name": "Romanian Deadlifts", "sets": 3, "reps": "8-10"},
  {"name": "Leg Press", "sets": 3, "reps": 12}
]
```

#### Back Day
```json
[
  {"name": "Deadlifts", "sets": 4, "reps": 5},
  {"name": "Barbell Rows", "sets": 4, "reps": 8},
  {"name": "Pull-ups", "sets": 3, "reps": "max"}
]
```

### Examples

#### Vague Input
**Input:** `"did chest workout this morning"`

**Output:**
- `started_at`: "2025-10-05T07:00:00Z"
- `completed_at`: "2025-10-05T07:50:00Z"
- `duration_minutes`: 50
- `exercises`: [Bench Press 4x8-10, Incline DB Press 3x10-12, Cable Flyes 3x12]
- `estimated_calories`: 300
- `muscle_groups`: ["chest", "triceps", "shoulders"]
- `rpe`: 6
- Confidence: 0.5 (low)
- Suggestion: "Typical chest exercises added. Confirm accuracy and add weights."

#### Context Clues
**Input:** `"leg day after work, squats felt heavy"`

**Output:**
- `started_at`: "2025-10-05T17:30:00Z" (after work)
- `duration_minutes`: 60
- `exercises`: [Squats 4x6-8 (felt heavy), RDLs 3x8-10, Leg Press 3x12]
- `estimated_calories`: 350
- `rpe`: 8 (inferred from "felt heavy")
- `mood`: "challenging"
- Confidence: 0.6 (medium)
- Suggestion: "RPE 8 inferred from 'felt heavy'. Add weights for tracking."

---

## 📊 Confidence Levels & User Guidance

### Confidence Scoring

| Confidence | Range | Meaning | Example |
|------------|-------|---------|---------|
| High | 0.8-1.0 | Specific data provided | "6oz chicken, 1 cup rice" |
| Medium | 0.5-0.8 | Reasonable assumptions | "eggs for breakfast" |
| Low | 0.3-0.5 | Very vague, wild estimates | "ate chicken" |

### Flags

- `estimated: true` - Values are AI estimates (vs. user-provided exact data)
- `needs_clarification: true` - Critical data was assumed, user should verify

### Validation

Each response includes:

```json
{
  "validation": {
    "errors": [],
    "warnings": ["Time and portions assumed"],
    "missing_critical": ["exact_portions", "exact_time"]
  }
}
```

### Suggestions

Actionable guidance for improving accuracy:

```json
{
  "suggestions": [
    "Estimated ~450 cal based on typical portions",
    "For accuracy: 'had 6oz chicken and 1 cup rice for lunch at 12pm'",
    "Low confidence - assumed 5oz chicken + 1 cup rice"
  ]
}
```

---

## 🧪 Testing

### Running Tests

```bash
# Test meal estimation only
python test_meal_estimation.py

# Test ALL entry types comprehensively
python test_comprehensive_estimation.py
```

### Test Coverage

The comprehensive test covers:

- ✅ Vague meals with time inference
- ✅ Vague activities with duration/distance estimation
- ✅ Vague workouts with exercise generation
- ✅ Time context parsing (breakfast, morning, after work, etc.)
- ✅ Timestamp validation
- ✅ Required field validation
- ✅ Confidence level appropriateness

---

## 📱 Frontend Integration

### Displaying Estimates

The frontend should:

1. **Show confidence visually**
   - High confidence: Green checkmark
   - Medium confidence: Yellow info icon
   - Low confidence: Orange warning icon

2. **Mark estimated fields**
   - Show "estimated" badge on values
   - Allow users to click to edit/confirm

3. **Display suggestions**
   - Show helpful tips in expandable section
   - Guide users to improve accuracy

4. **Enable easy editing**
   - Let users tap any field to edit
   - Save corrections to improve future estimates

### Example UI

```
┌────────────────────────────────────────┐
│ Meal Logged                            │
├────────────────────────────────────────┤
│ 🍗 Chicken and Rice                    │
│                                        │
│ 🕐 Today at 12:30 PM (estimated) ⓘ    │
│ 🍽️ Lunch                               │
│                                        │
│ ⚠️ Low Confidence - Estimated Values  │
│                                        │
│ Calories: 450 cal (tap to edit)       │
│ Protein: 50g                           │
│ Carbs: 45g                             │
│ Fat: 6g                                │
│                                        │
│ 💡 Suggestions                         │
│ • Estimated 5oz chicken + 1 cup rice  │
│ • For accuracy: "6oz chicken, 1 cup"  │
│                                        │
│ [Edit Details] [Looks Good ✓]         │
└────────────────────────────────────────┘
```

---

## 🎯 Benefits

### For Users
1. **Frictionless logging** - Log anything, anytime, any detail level
2. **Always get feedback** - Never lose tracking data
3. **Learn portion sizes** - See typical portions in suggestions
4. **Improve over time** - Guidance helps build better habits

### For the App
1. **More data** - Users log more because it's easier
2. **Better AI context** - More data = better coaching
3. **User retention** - Less friction = more engagement
4. **Competitive advantage** - No other app does this well

---

## 🔄 Future Enhancements

1. **Learning from corrections**
   - Track when users edit estimates
   - Learn user's typical portions
   - Personalize future estimates

2. **Contextual improvements**
   - "I ate the same thing as yesterday" → copy previous meal
   - "usual breakfast" → user's common breakfast
   - Photo recognition → improved portion estimates

3. **Micronutrient expansion**
   - Vitamins (A, C, D, etc.)
   - Minerals (iron, calcium, etc.)
   - Advanced tracking for serious athletes

4. **Time zone awareness**
   - Respect user's timezone
   - Handle travel scenarios
   - DST adjustments

---

## 📄 Implementation Files

- `app/services/groq_service_v2.py` - Core estimation logic with comprehensive prompts
- `app/services/quick_entry_service.py` - Data flattening and database saving
- `test_comprehensive_estimation.py` - Test suite for all entry types
- `COMPREHENSIVE_ESTIMATION_SYSTEM.md` - This documentation

---

## ✅ Summary

Wagner Coach Quick Entry now provides **production-ready comprehensive estimation** that:

1. ✅ **NEVER leaves fields null** for core data
2. ✅ **ALWAYS estimates timestamps** with intelligent time inference
3. ✅ **Handles vague inputs gracefully** with typical assumptions
4. ✅ **Provides appropriate confidence levels** based on data quality
5. ✅ **Guides users to improve** with actionable suggestions
6. ✅ **Works across ALL entry types** (meals, activities, workouts, measurements)

**Result:** Users can log ANYTHING with ANY level of detail and ALWAYS get useful, actionable estimates with clear guidance for improvement.
