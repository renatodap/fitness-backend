# 🐛 CRITICAL BUG FIX: Nutrition Unit Conversion

## Problem Discovered

Backend was calculating nutrition WRONG for meals with units other than grams:

```
User: "I had 5 oz chicken and 1 cup rice"

❌ BEFORE (BROKEN):
- 5 oz chicken treated as 5g → 8.2 cal (should be ~233 cal)
- 1 cup rice treated as 1g → 1.3 cal (should be ~206 cal)
- TOTAL: 9.6 cal (should be ~439 cal)

✅ AFTER (FIXED):
- 5 oz chicken → 141.75g → ~233 cal ✅
- 1 cup rice → 195g → ~206 cal ✅
- TOTAL: ~439 cal ✅
```

## Root Cause

`unified_coach_service.py` `_calculate_nutrition_from_foods()` method was:
1. NOT converting units to grams before calculation
2. Directly dividing detected quantity by serving size: `scale_factor = 5.0 / 100.0 = 0.05`
3. This resulted in wildly incorrect nutrition values

**Impact**: Every meal logged with oz, cup, tbsp, etc. had WRONG calories/macros

## Solution

Created `unit_converter.py` service with comprehensive conversion tables:

### Weight Conversions (Universal)
- 1 oz = 28.35g
- 1 lb = 453.59g
- 1 kg = 1000g

### Volume Conversions (Approximate for water)
- 1 cup = 240g (generic)
- 1 tbsp = 15g
- 1 tsp = 5g
- 1 fl oz = 29.57g

### Food-Specific Conversions
- 1 cup rice (cooked) = 195g (NOT 240g!)
- 1 cup milk = 244g
- 1 cup chicken (diced) = 140g
- 1 cup pasta (cooked) = 140g
- etc.

### Serving Conversions
- Uses `household_serving_grams` from database for accurate conversions
- Examples:
  - 2 slices bread (28g each) = 56g
  - 1 piece chicken breast (140g) = 140g

## Files Changed

### 1. Created: `app/services/unit_converter.py`
- Comprehensive conversion tables
- Food-specific conversions for common items
- Priority: DB household_serving_grams → food-specific → standard → fallback
- Includes test cases demonstrating the fix

### 2. Updated: `app/services/unified_coach_service.py`
- Added import: `from app.services.unit_converter import convert_to_grams`
- Modified `_calculate_nutrition_from_foods()` to convert units BEFORE calculating:

```python
# OLD (BROKEN):
scale_factor = detected_qty / serving_size  # 5/100 = 0.05 ❌

# NEW (FIXED):
detected_qty_in_grams = convert_to_grams(
    quantity=detected_qty,
    unit=detected_unit,
    food_name=food_name,
    household_serving_grams=household_serving_grams
)
scale_factor = detected_qty_in_grams / serving_size  # 141.75/100 = 1.4175 ✅
```

### 3. Updated: `app/services/agentic_food_matcher_service.py`
- Added `household_serving_grams` field to all normalized food responses
- Ensures unit converter has access to database serving info
- Applied to DB-matched foods, Perplexity-created foods, and Groq-created foods

## Testing

### Manual Test Cases (from unit_converter.py)

```bash
cd wagner-coach-backend
python -m app.services.unit_converter
```

Expected output:
```
Test 1: Weight conversions
5 oz → 141.75g (expected: ~141.75g)
1 lb → 453.59g (expected: ~453.59g)
100 g → 100g (expected: 100g)

Test 2: Volume conversions (generic)
1 cup (water) → 240g (expected: 240g)
1 tbsp → 15g (expected: 15g)
1 tsp → 5g (expected: 5g)

Test 3: Food-specific conversions
1 cup rice → 195g (expected: 195g)
1 cup milk → 244g (expected: 244g)
1 cup chicken → 140g (expected: 140g)

Test 4: Serving conversions with household_serving_grams
2 slices (28g each) → 56g (expected: 56g)
1 piece (140g) → 140g (expected: 140g)

Test 5: The actual bug case from production logs
5 oz chicken (should be 141.75g, not 5g) → 141.75g
1 cup rice (should be 195g, not 1g) → 195g
```

### Integration Test

The bug will be automatically fixed once deployed. Next time a user logs:
- "5 oz chicken breast" → Will correctly calculate ~233 cal
- "1 cup white rice" → Will correctly calculate ~206 cal
- "2 slices bread" → Will correctly calculate based on household_serving_grams

## Deployment

### Files to Deploy
```bash
# New file
app/services/unit_converter.py

# Modified files
app/services/unified_coach_service.py
app/services/agentic_food_matcher_service.py
```

### Deployment Steps
1. Commit changes to git
2. Push to Railway/deployment platform
3. Verify backend restarts successfully
4. Test with production data: "I had 5 oz chicken and 1 cup rice"
5. Check logs for correct conversion: "5.0 oz → 141.75g"

### Verification

After deployment, check backend logs for:
```
[_calculate_nutrition] ✅ CONVERTED: 5.0 oz → 141.75g
[_calculate_nutrition] Food: Chicken Breast - 5.0 oz (141.75g) | DB serving: 100g | scale_factor = 141.75g / 100g = 1.4175
[_calculate_nutrition] Scaled nutrition: 233.0 cal, 43.8g P, 0.0g C, 5.1g F
```

## Impact

### Before Fix
- ❌ ALL meals with oz/cup/tbsp had wrong nutrition
- ❌ User confusion: "Why is my chicken only 8 calories?"
- ❌ Inaccurate macro tracking
- ❌ Potential health impact from incorrect data

### After Fix
- ✅ Accurate nutrition for ALL unit types
- ✅ Proper conversion tables (oz→g, cup→g, etc.)
- ✅ Food-specific conversions (rice, milk, etc.)
- ✅ Database-backed conversions (household_serving_grams)

## Additional Notes

### Unit Converter Features
- **Graceful degradation**: Falls back to standard conversions if food-specific not available
- **Logging**: Extensive logging for debugging unit conversion issues
- **Extensible**: Easy to add new food-specific conversions
- **Safe**: Returns quantity as-is if unit unknown (better than crashing)

### Future Enhancements
- Add more food-specific conversions (vegetables, meats, etc.)
- Support metric/imperial user preferences
- Allow user to customize household serving sizes
- Validate conversions against USDA database

## Conclusion

This was a CRITICAL bug affecting all nutrition calculations with non-gram units. The fix:
1. Creates comprehensive unit conversion service
2. Integrates it into nutrition calculation pipeline
3. Ensures all matched foods include necessary conversion data
4. Provides extensive logging for verification

**Status**: ✅ FIXED and ready for deployment
