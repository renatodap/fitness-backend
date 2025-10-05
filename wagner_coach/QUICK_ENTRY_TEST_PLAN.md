# Quick Entry V2 - Comprehensive Test Plan

## Overview
This test plan covers all 10 test cases from the UI specification. Tests should be run against both backend (Python) and frontend (React/TypeScript) implementations.

---

## Test Case 1: Meal with All Portions

**Input:**
```
Text: "Grilled chicken breast 6oz, brown rice 1 cup, broccoli 1 cup"
```

**Expected Backend Response:**
```json
{
  "success": true,
  "entry_type": "meal",
  "confidence": 0.95,
  "data": {
    "primary_fields": {
      "meal_name": "Grilled Chicken Breast with Brown Rice and Broccoli",
      "meal_type": "lunch",
      "calories": 520,
      "protein_g": 52,
      "foods": [
        {"name": "Grilled chicken breast", "quantity": "6oz"},
        {"name": "Brown rice", "quantity": "1 cup"},
        {"name": "Broccoli", "quantity": "1 cup"}
      ]
    },
    "secondary_fields": {
      "carbs_g": 48,
      "fat_g": 8,
      "fiber_g": 6,
      "foods_detailed": [...]
    },
    "estimated": false,
    "needs_clarification": false
  },
  "validation": {
    "errors": [],
    "warnings": [],
    "missing_critical": []
  },
  "suggestions": [
    "Great protein-rich meal! Perfect for post-workout recovery."
  ]
}
```

**Expected UI Behavior:**
- ✅ Show meal name prominently
- ✅ Display 3 colored nutrition cards (calories, protein, carbs)
- ✅ List all 3 foods with portions
- ✅ NO warning banners
- ✅ NO "Estimated" badge
- ✅ "More details" button expands to show fat, fiber, sodium
- ✅ Green suggestions box at bottom
- ✅ Save and Edit buttons functional

---

## Test Case 2: Meal without Portions

**Input:**
```
Text: "chicken and rice"
```

**Expected Backend Response:**
```json
{
  "success": true,
  "entry_type": "meal",
  "confidence": 0.75,
  "data": {
    "primary_fields": {
      "meal_name": "Chicken and Rice",
      "meal_type": "lunch",
      "calories": null,
      "protein_g": null,
      "foods": [
        {"name": "Chicken", "quantity": "not specified"},
        {"name": "Rice", "quantity": "not specified"}
      ]
    },
    "secondary_fields": {},
    "estimated": false,
    "needs_clarification": true
  },
  "validation": {
    "errors": [],
    "warnings": ["Missing portion sizes for accurate tracking"],
    "missing_critical": ["portions"]
  },
  "suggestions": [
    "Add portions like '6oz chicken, 1 cup rice' for accurate nutrition"
  ]
}
```

**Expected UI Behavior:**
- ⚠️ Amber warning banner: "Needs Clarification"
- ⚠️ Shows "Missing portion sizes" warning
- ❓ Nutrition cards show "?" instead of numbers
- 💡 Blue "Quick Estimate" section with suggestion
- ✅ "Use This Estimate" button (when implemented)
- ✅ User can still save (for manual editing later)

---

## Test Case 3: Workout with Exercises

**Input:**
```
Text: "Bench press 4x8 at 185lbs, Incline DB press 3x12 at 60lbs per side"
```

**Expected Backend Response:**
```json
{
  "success": true,
  "entry_type": "workout",
  "confidence": 0.92,
  "data": {
    "primary_fields": {
      "workout_name": "Chest Workout",
      "duration_minutes": null,
      "exercises": [
        {
          "name": "Bench Press",
          "sets": 4,
          "reps": 8,
          "weight_lbs": 185,
          "note": null
        },
        {
          "name": "Incline Dumbbell Press",
          "sets": 3,
          "reps": 12,
          "weight_lbs": 120,
          "weight_per_side": 60,
          "note": "per side"
        }
      ]
    },
    "secondary_fields": {
      "volume_load": 10240,
      "muscle_groups": ["chest", "triceps", "shoulders"],
      "estimated_calories": 185,
      "tags": ["push", "hypertrophy"]
    },
    "estimated": false,
    "needs_clarification": false
  },
  "validation": {
    "errors": [],
    "warnings": [],
    "missing_critical": []
  },
  "suggestions": [
    "Consider adding shoulder accessory work for balanced development"
  ]
}
```

**Expected UI Behavior:**
- 💪 Blue gradient header with "Workout Entry"
- ✅ 2 exercise cards with gradient backgrounds
- ✅ Each card shows: sets × reps @ weight
- ✅ Second card shows "(60 lbs per side)"
- ✅ Volume calculation displayed on each card
- 💚 Total volume badge: "10,240 lbs 💪"
- ✅ Progressive overload badge: "Solid volume!"
- ✅ Expandable section shows muscle groups (3 chips)
- ✅ Edit mode allows inline editing

---

## Test Case 4: Activity with Pace

**Input:**
```
Text: "Ran 5 miles in 40 minutes"
```

**Expected Backend Response:**
```json
{
  "success": true,
  "entry_type": "activity",
  "confidence": 0.90,
  "data": {
    "primary_fields": {
      "activity_name": "Running",
      "activity_type": "running",
      "distance_miles": 5,
      "duration_minutes": 40,
      "pace": "8:00/mile"
    },
    "secondary_fields": {
      "calories_burned": 525,
      "avg_heart_rate": null,
      "rpe": null,
      "tags": ["cardio", "endurance"]
    },
    "estimated": false,
    "needs_clarification": false
  },
  "validation": {
    "errors": [],
    "warnings": [],
    "missing_critical": []
  },
  "suggestions": [
    "Great steady pace! Consider tracking heart rate for better insights."
  ]
}
```

**Expected UI Behavior:**
- 🏃 Activity header with icon
- ✅ Distance, duration, and pace displayed prominently
- ✅ Auto-calculated pace: "8:00/mile"
- ✅ Calories burned estimate
- ✅ Suggestion to track heart rate
- ✅ Tags displayed as chips
- ✅ Edit mode allows adjusting all fields

---

## Test Case 5: Note with Sentiment

**Input:**
```
Text: "Feeling amazing today! Hit a new PR on deadlifts and energy is through the roof!"
```

**Expected Backend Response:**
```json
{
  "success": true,
  "entry_type": "note",
  "confidence": 0.88,
  "data": {
    "primary_fields": {
      "title": "New PR and High Energy",
      "content": "Feeling amazing today! Hit a new PR on deadlifts and energy is through the roof!",
      "sentiment": "positive",
      "sentiment_score": 0.92
    },
    "secondary_fields": {
      "detected_themes": ["achievement", "energy", "strength"],
      "related_goals": ["progressive_overload"],
      "action_items": [],
      "tags": ["personal_record", "motivation"]
    },
    "estimated": false,
    "needs_clarification": false
  },
  "validation": {
    "errors": [],
    "warnings": [],
    "missing_critical": []
  },
  "suggestions": [
    "Great mindset! Consider logging your deadlift workout for tracking."
  ]
}
```

**Expected UI Behavior:**
- 📝 Note header
- 😄 Large positive sentiment emoji badge (green background)
- ✅ Title and content displayed
- ✅ Detected themes as colored chips
- ✅ Related goals section
- ✅ Suggestions box
- ✅ Edit mode allows inline editing

---

## Test Case 6: Measurement with Trend

**Input:**
```
Text: "Weight 175.2 lbs"
```

**Expected Backend Response:**
```json
{
  "success": true,
  "entry_type": "measurement",
  "confidence": 0.95,
  "data": {
    "primary_fields": {
      "weight_lbs": 175.2,
      "weight_kg": 79.5
    },
    "secondary_fields": {
      "trend_direction": "down",
      "rate_of_change_weekly": -0.8,
      "tags": []
    },
    "estimated": false,
    "needs_clarification": false
  },
  "validation": {
    "errors": [],
    "warnings": [],
    "missing_critical": []
  },
  "suggestions": [
    "Down 0.8 lbs/week - healthy progress! Keep it up."
  ]
}
```

**Expected UI Behavior:**
- 📊 Measurement header
- ✅ Large weight display: "175.2 lbs"
- 📉 Trend indicator: Down arrow (green)
- ✅ "Down 0.8 lbs/week" badge
- ✅ Graph placeholder (future enhancement)
- ✅ Suggestions with encouragement
- ✅ Edit mode allows adjustment

---

## Test Case 7: Similar Past Entries (Semantic Context)

**Input:**
```
Text: "chicken salad"
```

**Expected Backend Response:**
```json
{
  "success": true,
  "entry_type": "meal",
  "confidence": 0.82,
  "data": {
    "primary_fields": {
      "meal_name": "Chicken Salad",
      "meal_type": "lunch",
      "calories": null,
      "protein_g": null,
      "foods": [
        {"name": "Chicken salad", "quantity": "not specified"}
      ]
    },
    "secondary_fields": {},
    "estimated": false,
    "needs_clarification": true
  },
  "validation": {
    "errors": [],
    "warnings": ["Missing portion sizes"],
    "missing_critical": ["portions"]
  },
  "suggestions": [
    "You logged similar meals before. Use one as template?"
  ],
  "semantic_context": {
    "similar_count": 3,
    "suggestions": [
      {
        "similarity": 0.94,
        "created_at": "2025-10-02T12:30:00Z",
        "meal_name": "Grilled Chicken Caesar Salad",
        "calories": 420,
        "protein_g": 38,
        "foods": [...]
      },
      {
        "similarity": 0.89,
        "created_at": "2025-09-28T13:00:00Z",
        "meal_name": "Chicken Garden Salad",
        "calories": 380,
        "protein_g": 32,
        "foods": [...]
      }
    ]
  }
}
```

**Expected UI Behavior:**
- ✅ Warning banner for missing portions
- 💡 Special "Similar Past Entries" section
- ✅ 2-3 cards showing previous similar meals
- ✅ Each card shows: name, calories, protein, date
- ✅ "Use This" button on each card (auto-fills data)
- ✅ Similarity score badge (optional)
- ✅ Falls back to manual entry if no match

---

## Test Case 8: Low Confidence

**Input:**
```
Text: "xyz abc 123"
```

**Expected Backend Response:**
```json
{
  "success": true,
  "entry_type": "unknown",
  "confidence": 0.12,
  "data": {
    "primary_fields": {},
    "secondary_fields": {},
    "estimated": false,
    "needs_clarification": true
  },
  "validation": {
    "errors": ["Could not understand the entry"],
    "warnings": [],
    "missing_critical": []
  },
  "suggestions": [
    "Please try again with more specific information like 'ran 3 miles' or 'grilled chicken 6oz'"
  ]
}
```

**Expected UI Behavior:**
- ⚠️ Amber warning banner: "Unclear Entry Type"
- ❓ "Could not determine the type of entry"
- 💡 Helpful examples displayed
- ✅ "Try Again" button (clears form)
- ❌ No save button (nothing to save)
- ✅ Graceful error handling (no crash)

---

## Test Case 9: Edit Mode

**Input:**
Any valid entry (e.g., "chicken salad 450 calories")

**Expected UI Behavior - View Mode:**
- ✅ All fields displayed as static text
- ✅ "Edit" button enabled
- ✅ "Save Entry" button enabled

**Expected UI Behavior - Edit Mode (after clicking "Edit"):**
- ✅ Meal name becomes `<input type="text">`
- ✅ Meal type buttons become clickable
- ✅ Calories becomes `<input type="number">`
- ✅ Protein becomes `<input type="number">`
- ✅ Food items have delete/edit buttons
- ✅ "+ Add Food" button appears
- ✅ Edit button changes to "Done Editing"
- ✅ Clicking "Done Editing" returns to view mode
- ✅ Changes are preserved when toggling
- ✅ Save button uses edited data

---

## Test Case 10: Validation Errors

**Input:**
```
Backend returns invalid data (simulated or real)
```

**Simulated Invalid Response:**
```json
{
  "success": false,
  "entry_type": "meal",
  "confidence": 0.45,
  "data": {
    "primary_fields": {
      "meal_name": "",
      "calories": -50,
      "protein_g": 999
    },
    "estimated": false,
    "needs_clarification": false
  },
  "validation": {
    "errors": [
      "Meal name cannot be empty",
      "Calories cannot be negative",
      "Protein value seems unrealistic (999g)"
    ],
    "warnings": [],
    "missing_critical": ["meal_name"]
  },
  "suggestions": []
}
```

**Expected UI Behavior:**
- 🔴 Red error banner at top
- ✅ Inline error messages next to invalid fields
- ✅ Invalid fields highlighted in red
- ✅ Save button disabled when errors present
- ✅ Edit mode allows fixing errors
- ✅ Real-time validation as user types
- ✅ Error count badge: "3 errors found"
- ✅ Errors clear when fixed

---

## Automated Test Suite

### Backend Tests (Python/pytest)

Create: `fitness-backend-clean/tests/test_groq_service_v2.py`

```python
import pytest
from app.services.groq_service_v2 import GroqServiceV2

@pytest.fixture
def groq_service():
    return GroqServiceV2()

@pytest.mark.asyncio
async def test_meal_with_portions(groq_service):
    """Test Case 1: Meal with all portions"""
    result = await groq_service.classify_and_extract(
        "Grilled chicken breast 6oz, brown rice 1 cup, broccoli 1 cup"
    )
    assert result["entry_type"] == "meal"
    assert result["data"]["needs_clarification"] == False
    assert result["data"]["primary_fields"]["calories"] is not None
    assert len(result["data"]["primary_fields"]["foods"]) == 3

@pytest.mark.asyncio
async def test_meal_without_portions(groq_service):
    """Test Case 2: Meal without portions"""
    result = await groq_service.classify_and_extract("chicken and rice")
    assert result["entry_type"] == "meal"
    assert result["data"]["needs_clarification"] == True
    assert result["data"]["primary_fields"]["calories"] is None
    assert len(result["validation"]["warnings"]) > 0

@pytest.mark.asyncio
async def test_workout_with_exercises(groq_service):
    """Test Case 3: Workout with exercises"""
    result = await groq_service.classify_and_extract(
        "Bench press 4x8 at 185lbs, Incline DB press 3x12 at 60lbs per side"
    )
    assert result["entry_type"] == "workout"
    assert len(result["data"]["primary_fields"]["exercises"]) == 2
    assert result["data"]["secondary_fields"]["volume_load"] > 0

@pytest.mark.asyncio
async def test_activity_with_pace(groq_service):
    """Test Case 4: Activity with pace"""
    result = await groq_service.classify_and_extract("Ran 5 miles in 40 minutes")
    assert result["entry_type"] == "activity"
    assert result["data"]["primary_fields"]["pace"] == "8:00/mile"
    assert result["data"]["primary_fields"]["distance_miles"] == 5

@pytest.mark.asyncio
async def test_note_with_sentiment(groq_service):
    """Test Case 5: Note with sentiment"""
    result = await groq_service.classify_and_extract(
        "Feeling amazing today! Hit a new PR on deadlifts and energy is through the roof!"
    )
    assert result["entry_type"] == "note"
    assert result["data"]["primary_fields"]["sentiment"] == "positive"
    assert result["data"]["primary_fields"]["sentiment_score"] > 0.8

@pytest.mark.asyncio
async def test_measurement_with_trend(groq_service):
    """Test Case 6: Measurement"""
    result = await groq_service.classify_and_extract("Weight 175.2 lbs")
    assert result["entry_type"] == "measurement"
    assert result["data"]["primary_fields"]["weight_lbs"] == 175.2

@pytest.mark.asyncio
async def test_low_confidence(groq_service):
    """Test Case 8: Low confidence"""
    result = await groq_service.classify_and_extract("xyz abc 123")
    assert result["entry_type"] == "unknown"
    assert result["confidence"] < 0.5
    assert len(result["validation"]["errors"]) > 0
```

### Frontend Tests (Jest/React Testing Library)

Create: `wagner-coach-clean/components/quick-entry/__tests__/MealPreview.test.tsx`

```typescript
import { render, screen, fireEvent } from '@testing-library/react';
import MealPreview from '../MealPreview';
import { QuickEntryPreviewResponse } from '../types';

describe('MealPreview', () => {
  test('Test Case 1: Shows complete nutrition when portions provided', () => {
    const mockData: QuickEntryPreviewResponse = {
      success: true,
      entry_type: 'meal',
      confidence: 0.95,
      data: {
        primary_fields: {
          meal_name: 'Chicken and Rice',
          meal_type: 'lunch',
          calories: 520,
          protein_g: 52,
          foods: [
            { name: 'Chicken', quantity: '6oz' },
            { name: 'Rice', quantity: '1 cup' }
          ]
        },
        secondary_fields: { carbs_g: 48, fat_g: 8 },
        estimated: false,
        needs_clarification: false
      },
      validation: { errors: [], warnings: [], missing_critical: [] },
      suggestions: []
    };

    render(<MealPreview data={mockData} onSave={jest.fn()} onEdit={jest.fn()} />);

    expect(screen.getByText('520')).toBeInTheDocument();
    expect(screen.getByText('52g')).toBeInTheDocument();
    expect(screen.queryByText('Needs Clarification')).not.toBeInTheDocument();
  });

  test('Test Case 2: Shows warning when portions missing', () => {
    const mockData: QuickEntryPreviewResponse = {
      success: true,
      entry_type: 'meal',
      confidence: 0.75,
      data: {
        primary_fields: {
          meal_name: 'Chicken and Rice',
          meal_type: 'lunch',
          calories: null,
          protein_g: null,
          foods: [
            { name: 'Chicken', quantity: 'not specified' }
          ]
        },
        secondary_fields: {},
        estimated: false,
        needs_clarification: true
      },
      validation: {
        errors: [],
        warnings: ['Missing portion sizes'],
        missing_critical: ['portions']
      },
      suggestions: []
    };

    render(<MealPreview data={mockData} onSave={jest.fn()} onEdit={jest.fn()} />);

    expect(screen.getByText(/Needs Clarification/i)).toBeInTheDocument();
    expect(screen.getByText(/Missing portion sizes/i)).toBeInTheDocument();
  });

  test('Test Case 9: Edit mode transforms fields to inputs', () => {
    const mockData: QuickEntryPreviewResponse = {
      success: true,
      entry_type: 'meal',
      confidence: 0.90,
      data: {
        primary_fields: {
          meal_name: 'Test Meal',
          meal_type: 'lunch',
          calories: 400,
          protein_g: 30,
          foods: []
        },
        secondary_fields: {},
        estimated: false,
        needs_clarification: false
      },
      validation: { errors: [], warnings: [], missing_critical: [] },
      suggestions: []
    };

    render(<MealPreview data={mockData} onSave={jest.fn()} onEdit={jest.fn()} />);

    const editButton = screen.getByText(/Edit/i);
    fireEvent.click(editButton);

    const mealNameInput = screen.getByDisplayValue('Test Meal');
    expect(mealNameInput.tagName).toBe('INPUT');
    expect(screen.getByText(/Done Editing/i)).toBeInTheDocument();
  });
});
```

---

## Manual Testing Checklist

### Pre-Testing Setup
- [ ] Backend running on `http://localhost:8000`
- [ ] Frontend running on `http://localhost:3000`
- [ ] User logged in with valid session
- [ ] Database seeded with sample data for semantic search tests

### Test Execution

#### Test Case 1: Meal with All Portions
- [ ] Navigate to `/quick-entry-optimized`
- [ ] Enter: "Grilled chicken breast 6oz, brown rice 1 cup, broccoli 1 cup"
- [ ] Click "Analyze & Save"
- [ ] Verify: Nutrition cards show numbers (not "?")
- [ ] Verify: No warning banners
- [ ] Verify: All 3 foods listed with quantities
- [ ] Click "More details"
- [ ] Verify: Fat, fiber, sodium displayed
- [ ] Click "Save Entry"
- [ ] Verify: Success message appears

#### Test Case 2: Meal without Portions
- [ ] Enter: "chicken and rice"
- [ ] Click "Analyze & Save"
- [ ] Verify: Amber warning banner appears
- [ ] Verify: Nutrition cards show "?"
- [ ] Verify: "Quick Estimate" section visible
- [ ] Verify: Can still save entry

#### Test Case 3: Workout with Exercises
- [ ] Enter: "Bench press 4x8 at 185lbs, Incline DB press 3x12 at 60lbs per side"
- [ ] Click "Analyze & Save"
- [ ] Verify: 2 exercise cards displayed
- [ ] Verify: Volume calculation on each card
- [ ] Verify: Total volume badge shows >10,000 lbs
- [ ] Verify: Progressive overload message
- [ ] Click "More details"
- [ ] Verify: Muscle groups shown as chips

#### Test Case 4: Activity with Pace
- [ ] Enter: "Ran 5 miles in 40 minutes"
- [ ] Click "Analyze & Save"
- [ ] Verify: Pace auto-calculated as "8:00/mile"
- [ ] Verify: Distance and duration displayed
- [ ] Verify: Calories estimate shown

#### Test Case 5: Note with Sentiment
- [ ] Enter: "Feeling amazing today! Hit a new PR on deadlifts!"
- [ ] Click "Analyze & Save"
- [ ] Verify: Positive sentiment badge (green, happy emoji)
- [ ] Verify: Detected themes as chips
- [ ] Verify: Related goals section

#### Test Case 6: Measurement with Trend
- [ ] Enter: "Weight 175.2 lbs"
- [ ] Click "Analyze & Save"
- [ ] Verify: Weight displayed prominently
- [ ] Verify: Trend indicator (if enough history)
- [ ] Verify: Rate of change shown

#### Test Case 7: Similar Past Entries
- [ ] Prerequisites: Have 2-3 similar meals logged previously
- [ ] Enter: "chicken salad"
- [ ] Click "Analyze & Save"
- [ ] Verify: "Similar Past Entries" section visible
- [ ] Verify: Previous meals shown as cards
- [ ] Verify: "Use This" buttons functional

#### Test Case 8: Low Confidence
- [ ] Enter: "xyz abc 123"
- [ ] Click "Analyze & Save"
- [ ] Verify: "Unclear Entry Type" message
- [ ] Verify: Helpful suggestions shown
- [ ] Verify: "Try Again" button clears form
- [ ] Verify: No crash or console errors

#### Test Case 9: Edit Mode
- [ ] Enter any valid meal
- [ ] Click "Analyze & Save"
- [ ] Click "Edit" button
- [ ] Verify: All fields become inputs
- [ ] Modify meal name
- [ ] Modify calories
- [ ] Click "Done Editing"
- [ ] Verify: Changes persist in view mode
- [ ] Click "Save Entry"
- [ ] Verify: Edited data is saved

#### Test Case 10: Validation Errors
- [ ] Backend: Temporarily inject validation errors
- [ ] Verify: Red error banner appears
- [ ] Verify: Inline errors next to fields
- [ ] Verify: Save button disabled
- [ ] Enter edit mode
- [ ] Fix errors
- [ ] Verify: Errors clear in real-time
- [ ] Verify: Save button re-enables

---

## Performance Tests

### Response Time
- [ ] Text-only entry: < 500ms
- [ ] Image entry: < 3s
- [ ] PDF entry: < 5s

### Cost Validation
- [ ] Text entry cost: ~$0.0002 (Groq pricing)
- [ ] Image entry cost: ~$0.001 (vision model)
- [ ] Semantic search: < 30ms

### Error Handling
- [ ] Network timeout: Graceful error message
- [ ] Invalid session: Redirect to login
- [ ] Backend down: User-friendly error
- [ ] Invalid JSON: Fallback to error state

---

## Accessibility Tests

- [ ] Keyboard navigation works (Tab through all fields)
- [ ] Enter key submits form
- [ ] Escape key cancels/closes
- [ ] Screen reader announces errors
- [ ] Focus indicators visible
- [ ] Color contrast meets WCAG AA standards
- [ ] Alt text on all images/icons

---

## Browser Compatibility

- [ ] Chrome (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)
- [ ] Edge (latest)
- [ ] Mobile Safari (iOS)
- [ ] Mobile Chrome (Android)

---

## Test Results Template

```
Test Case: [Number] - [Name]
Date: [YYYY-MM-DD]
Tester: [Name]
Environment: [Local/Staging/Production]

Backend Response Time: [ms]
UI Render Time: [ms]

✅ PASS / ❌ FAIL

Issues Found:
1. [Description]
2. [Description]

Screenshots: [Attach if applicable]
```

---

## Success Criteria

All 10 test cases must:
- ✅ Pass backend validation (correct JSON structure)
- ✅ Pass frontend rendering (no console errors)
- ✅ Meet performance targets (< 3s total)
- ✅ Handle errors gracefully (no crashes)
- ✅ Pass accessibility audit (Lighthouse score > 90)

---

**Status**: Ready for testing
**Next Steps**: Run all 10 test cases, document results, fix any failures
