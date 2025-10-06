# Meal Nutritional Estimation Update

## Summary

Updated the Quick Entry system to **ALWAYS estimate nutritional values** (macros, calories, and micronutrients) regardless of input precision or confidence level.

## Problem

Previously, the system would return `null` for nutritional values when:
- Meal descriptions were vague (e.g., "chicken and rice")
- Portion sizes were not specified
- Confidence was low

This meant users could log meals without getting any nutritional feedback, defeating the purpose of tracking.

## Solution

### 1. Updated Groq Service V2 (`app/services/groq_service_v2.py`)

**Changed estimation rules** (lines 84-100):

**Before:**
- For vague meals without portions → set macros to `null`
- Only estimate for restaurant meals or specific portions

**After:**
- **ALWAYS estimate macros** - Never return null
- For vague inputs, use typical portion assumptions:
  - Protein: assume 4-6 oz for chicken/meat, 2-3 eggs
  - Grains: assume 1 cup cooked rice/pasta
  - Vegetables: assume 1-2 cups
- Mark estimates with low confidence and suggest improvements
- Include micronutrients when possible (fiber, sugar, sodium)

**Updated example output** (lines 191-246):

Input: `"chicken and rice"` (vague, no portions)

**Before:**
```json
{
  "calories": null,
  "protein_g": null,
  "carbs_g": null,
  "fat_g": null
}
```

**After:**
```json
{
  "calories": 450,
  "protein_g": 50,
  "carbs_g": 45,
  "fat_g": 6,
  "fiber_g": 2,
  "sugar_g": 0,
  "sodium_mg": 200,
  "confidence": 0.5,
  "estimated": true,
  "needs_clarification": true
}
```

**Updated important rules** (lines 401-408):

```
IMPORTANT:
- ALWAYS estimate macros/nutrition - NEVER use null for calories, protein, carbs, fat
- For vague inputs, use typical portion assumptions and mark with low confidence
- Include micronutrients (fiber, sugar, sodium) when possible
- Set needs_clarification=true if portions not specified
- Provide actionable suggestions for improving accuracy
```

### 2. Updated Quick Entry Service (`app/services/quick_entry_service.py`)

**Added compatibility layer** (lines 579-593):

The service now handles both:
- **Old flat structure**: `{ "calories": 450, "protein_g": 50, ... }`
- **New nested structure**: `{ "primary_fields": {...}, "secondary_fields": {...} }`

This ensures backward compatibility while supporting the new Groq V2 output format.

```python
# Flatten primary_fields and secondary_fields into single data dict
if "primary_fields" in raw_data:
    # New Groq V2 structure - merge primary and secondary fields
    data.update(raw_data.get("primary_fields", {}))
    data.update(raw_data.get("secondary_fields", {}))
    data["estimated"] = raw_data.get("estimated", True)
    data["needs_clarification"] = raw_data.get("needs_clarification", False)
else:
    # Old flat structure
    data = raw_data
```

## Benefits

1. **Always actionable** - Users always get nutritional estimates
2. **Transparency** - Low confidence estimates are clearly marked
3. **Guidance** - Suggestions help users improve data quality
4. **Micronutrients** - More complete nutritional picture (fiber, sugar, sodium)
5. **Flexible** - Works with any level of input detail

## Examples

### Vague Input

**Input:** `"chicken and rice"`

**Response:**
- Calories: 450 (estimated)
- Protein: 50g (estimated)
- Carbs: 45g (estimated)
- Fat: 6g (estimated)
- Confidence: 0.5 (low)
- Suggestion: "For accuracy, specify portions: '6oz chicken, 1 cup rice'"

### Restaurant Meal

**Input:** `"Chicken Margherita at Olive Garden"`

**Response:**
- Calories: 870 (estimated from menu)
- Protein: 62g (estimated)
- Carbs: 48g (estimated)
- Fat: 38g (estimated)
- Fiber: 5g
- Sugar: 12g
- Sodium: 1580mg
- Confidence: 0.85 (high)
- Suggestion: "Restaurant portions tend to be larger - estimate ~870 calories"

### Specific Input

**Input:** `"6oz grilled chicken breast with 1 cup brown rice and broccoli"`

**Response:**
- Calories: 558
- Protein: 63g
- Carbs: 57g
- Fat: 8.6g
- Fiber: 9g
- Sugar: 3g
- Sodium: 150mg
- Confidence: 0.9 (very high)
- Suggestion: "Great macro balance!"

## Testing

Run the test script to verify estimates:

```bash
cd wagner-coach-backend
python test_meal_estimation.py
```

The test verifies that ALL meal inputs (vague, specific, restaurant) receive nutritional estimates.

## API Response Format

The Quick Entry API now returns:

```json
{
  "success": true,
  "entry_type": "meal",
  "confidence": 0.5,
  "data": {
    "meal_name": "Chicken and rice",
    "meal_type": "lunch",
    "calories": 450,
    "protein_g": 50,
    "carbs_g": 45,
    "fat_g": 6,
    "fiber_g": 2,
    "sugar_g": 0,
    "sodium_mg": 200,
    "foods": [
      {"name": "Chicken breast", "quantity": "5 oz (assumed)"},
      {"name": "Rice, cooked", "quantity": "1 cup (assumed)"}
    ],
    "estimated": true,
    "needs_clarification": true
  },
  "suggestions": [
    "Estimate based on typical portions: ~450 cal, ~50g protein",
    "For accuracy, specify portions: '6oz chicken, 1 cup rice'"
  ],
  "entry_id": "uuid-here"
}
```

## Database Schema

The `meal_logs` table already supports these fields:

- `total_calories` - Estimated calories
- `total_protein_g` - Estimated protein
- `total_carbs_g` - Estimated carbs
- `total_fat_g` - Estimated fat
- `total_fiber_g` - Estimated fiber
- `total_sugar_g` - Estimated sugar
- `total_sodium_mg` - Estimated sodium
- `estimated` - Boolean flag (true for AI estimates)
- `confidence_score` - 0.0-1.0 confidence level
- `foods` - JSONB array of food items with quantities

No schema changes required.

## Compliance with Requirements

✅ **Always estimates macros** - No null values for nutrition
✅ **Always estimates calories** - Even for vague inputs
✅ **Includes micronutrients** - Fiber, sugar, sodium when possible
✅ **Confidence awareness** - Low confidence for vague inputs
✅ **User guidance** - Suggestions for improving accuracy
✅ **Backward compatible** - Works with existing data structures

## Next Steps

1. **Frontend update** - Show confidence levels and "estimated" badge in UI
2. **User education** - Explain how to improve accuracy with specific portions
3. **Feedback loop** - Allow users to correct estimates
4. **Learning** - Track which estimates users accept/reject
5. **Micronutrient expansion** - Add vitamins, minerals when data available

---

**Result:** Users can now log any meal (vague or specific) and ALWAYS receive nutritional estimates with appropriate confidence levels and improvement suggestions.
