# Meal Logging Improvements - Verification Checklist

**After running migration**: Use this checklist to verify everything works!

---

## ⚠️ **CRITICAL ISSUES TO CHECK**

### 1. **Database Schema Changes**

#### ✅ Verify `food_servings` table created:
```sql
SELECT COUNT(*) FROM food_servings;
-- Should return > 0 (populated from existing foods)

SELECT * FROM food_servings LIMIT 5;
-- Should show serving names like "100 g", "1 cup", etc.
```

#### ✅ Verify `meal_foods.template_id` removed:
```sql
SELECT column_name
FROM information_schema.columns
WHERE table_name = 'meal_foods' AND column_name = 'template_id';
-- Should return 0 rows
```

#### ✅ Verify indexes created:
```sql
SELECT indexname FROM pg_indexes
WHERE tablename IN ('foods_enhanced', 'meal_foods', 'meal_template_foods', 'food_servings')
ORDER BY tablename, indexname;
-- Should show all new indexes from migration
```

#### ✅ Test SQL functions:
```sql
-- Test expand_meal_template (replace with real template_id)
SELECT * FROM expand_meal_template('your-template-uuid-here');
-- Should return rows of (food_id, quantity, unit) if template has foods

-- Test get_default_serving (replace with real food_id)
SELECT * FROM get_default_serving('your-food-uuid-here');
-- Should return (serving_name, serving_size_g, quantity, unit)
```

---

## 🚨 **POTENTIAL BREAKING CHANGES**

### Issue #1: Backend API must return new fields

The frontend now expects these fields in food search responses:
- `household_serving_size`
- `household_serving_unit`

**Check backend API** (`/api/v1/foods/search`):
```python
# Make sure your backend includes these fields in SELECT:
.select(
    "id, name, brand_name, serving_size, serving_unit, "
    "household_serving_size, household_serving_unit, "  # ← MUST INCLUDE
    "calories, protein_g, carbs_g, fat_g, fiber_g"
)
```

**Test it**:
```bash
curl -H "Authorization: Bearer YOUR_TOKEN" \
  "http://localhost:8000/api/v1/foods/search?q=chicken"

# Response should include:
# {
#   "foods": [{
#     "id": "...",
#     "name": "Chicken Breast",
#     "household_serving_size": "100",  ← Check this exists
#     "household_serving_unit": "g",    ← Check this exists
#     ...
#   }]
# }
```

---

### Issue #2: Existing meal_foods with template_id

**BEFORE migration**, if you had rows like:
```sql
meal_foods: { meal_log_id: 'x', template_id: 'y', item_type: 'template' }
```

**AFTER migration**, those columns are gone!

**Check for orphaned data**:
```sql
-- Check if any meal_foods have NULL food_id (would be templates)
SELECT COUNT(*) FROM meal_foods WHERE food_id IS NULL;
-- Should be 0

-- If > 0, you have orphaned template references!
-- Those meals will be missing foods in the UI
```

**Fix if needed**:
```sql
-- Delete orphaned meal_foods rows (they reference deleted columns)
DELETE FROM meal_foods WHERE food_id IS NULL;

-- OR manually expand them if you know the template_id
-- (This is complex - ask if you need help)
```

---

### Issue #3: Profiles without timezone

**Frontend code assumes `profiles.timezone` exists**.

**Check**:
```sql
SELECT COUNT(*) FROM profiles WHERE timezone IS NULL OR timezone = '';
-- Should be 0 (or very few)
```

**Fix if needed**:
```sql
-- Set default timezone for users without one
UPDATE profiles
SET timezone = 'UTC'
WHERE timezone IS NULL OR timezone = '';
```

**Better**: Add timezone selection to onboarding flow.

---

## ✅ **MANUAL TESTING CHECKLIST**

### Test 1: Timezone Handling

1. **Set your profile timezone**:
```sql
UPDATE profiles
SET timezone = 'America/New_York'
WHERE id = 'your-user-id';
```

2. **Log a meal in UI**:
   - Go to Dashboard → Log Meal
   - Select time: "2:00 PM"
   - Add any food, submit

3. **Verify in database**:
```sql
SELECT logged_at,
       logged_at AT TIME ZONE 'UTC' as utc_time,
       logged_at AT TIME ZONE 'America/New_York' as ny_time
FROM meal_logs
WHERE user_id = 'your-user-id'
ORDER BY created_at DESC LIMIT 1;

-- logged_at should be UTC
-- ny_time should show 2:00 PM (what you entered)
```

**Expected**: `ny_time` column shows `14:00:00` (2 PM EST)

---

### Test 2: Food Portion Defaults

**Test 2a: Never-logged-before food**

1. Search for "Chicken Breast" (never logged before)
2. Click to add
3. **Expected**: Quantity defaults to `100` with unit `g`
4. **NOT**: Quantity = `1` ❌

**Test 2b: Previously-logged food**

1. Log "Oatmeal" at `50g`, save
2. Start a NEW meal
3. Search for "Oatmeal" again
4. **Expected**: Quantity defaults to `50` with unit `g` (your last quantity)

**Test 2c: Household serving**

1. Find a food with `household_serving_size` (e.g., "Bread - 2 slices")
2. Add it
3. **Expected**: Quantity = `2`, unit = `slice`

---

### Test 3: Meal Logging Still Works

**Basic flow**:
1. Dashboard → Log Meal
2. Search for food → Add it
3. Adjust quantity/unit → Save meal
4. Check meal appears in history
5. Check totals calculated correctly

**Edge cases**:
- [ ] Log meal with 1 food
- [ ] Log meal with 10+ foods
- [ ] Log meal with notes
- [ ] Edit existing meal
- [ ] Delete meal
- [ ] Log meal via coach preview (if applicable)

---

### Test 4: Performance (Optional)

**Food search should be MUCH faster now**:

```sql
EXPLAIN ANALYZE
SELECT * FROM foods_enhanced
WHERE search_vector @@ to_tsquery('english', 'chicken')
LIMIT 20;

-- Should use: Bitmap Index Scan on idx_foods_enhanced_search_vector
-- Execution time should be < 50ms
```

---

## 🔥 **QUICK SMOKE TESTS** (Run These First!)

```sql
-- 1. Can select from new table?
SELECT COUNT(*) FROM food_servings;

-- 2. Can call new functions?
SELECT get_default_serving('any-food-id');

-- 3. Can insert meal_foods (no template_id)?
-- This should NOT error:
SELECT * FROM meal_foods LIMIT 1;

-- 4. Check no NULL food_ids:
SELECT COUNT(*) FROM meal_foods WHERE food_id IS NULL;
-- Must be 0

-- 5. Backend API returns new fields?
-- (Test with curl or Postman - see Issue #1 above)
```

---

## 🐛 **KNOWN ISSUES & WORKAROUNDS**

### Issue: "Column template_id does not exist"

**Symptom**: Backend throws error when inserting meal_foods

**Cause**: Backend code still references `template_id` column

**Fix**: Update backend to remove `template_id` from INSERT/UPDATE queries:
```python
# WRONG:
await supabase.table("meal_foods").insert({
    "meal_log_id": meal_id,
    "template_id": template_id,  # ❌ Column removed!
    ...
})

# RIGHT:
await supabase.table("meal_foods").insert({
    "meal_log_id": meal_id,
    "food_id": food_id,  # ✅ Only food_id now
    ...
})
```

---

### Issue: Food shows weird portion like "None g"

**Symptom**: Food displays "None g" or "undefined undefined"

**Cause**: Backend not returning `household_serving_size` fields

**Fix**: Update backend API to include those fields in SELECT (see Issue #1)

---

### Issue: Time shows wrong timezone

**Symptom**: Meal logged at 2 PM shows as 6 PM (or other wrong time)

**Debug**:
```typescript
// In browser console on /nutrition/log page:
console.log('User timezone:', userTimezone);  // Should NOT be 'UTC'
console.log('Meal time input:', mealTime);     // Should be formatted correctly
```

**Fix**: Make sure `profiles.timezone` is set (not NULL, not 'UTC')

---

## ✅ **ROLLBACK PLAN** (If Things Break)

### If migration breaks database:

```sql
-- Restore from backup
pg_restore backup_before_meal_improvements.sql

-- OR manually revert changes:
DROP TABLE IF EXISTS food_servings CASCADE;
DROP FUNCTION IF EXISTS expand_meal_template CASCADE;
DROP FUNCTION IF EXISTS get_default_serving CASCADE;

-- Re-add removed columns (if you need old data):
ALTER TABLE meal_foods ADD COLUMN template_id uuid;
ALTER TABLE meal_foods ADD COLUMN item_type text DEFAULT 'food';
```

### If frontend breaks:

```bash
cd wagner-coach-clean
git checkout HEAD~1 app/nutrition/log/page.tsx  # Revert to previous version
git checkout HEAD~1 lib/api/foods.ts
```

---

## 📊 **SUCCESS CRITERIA**

Everything is working if:

- [x] Database migration ran without errors
- [ ] `food_servings` table has data
- [ ] `meal_foods.template_id` column gone
- [ ] All indexes created
- [ ] SQL functions work
- [ ] Backend returns `household_serving_size` fields
- [ ] No orphaned meal_foods (food_id is NULL)
- [ ] Users have timezone set in profiles
- [ ] Manual tests pass (see above)
- [ ] Meals can be logged normally
- [ ] Portion defaults work as expected
- [ ] Timezone conversions correct

---

## 🆘 **IF THINGS ARE BROKEN**

### Check these logs:

1. **Frontend console** (browser dev tools):
   - Look for errors about undefined fields
   - Check timezone-related errors

2. **Backend logs** (Railway/Fly.io):
   - Look for "column does not exist" errors
   - Check API endpoint errors

3. **Database logs** (Supabase):
   - Check for constraint violations
   - Look for RLS policy blocks

### Common fixes:

```sql
-- Fix 1: Users need timezones
UPDATE profiles SET timezone = 'UTC' WHERE timezone IS NULL;

-- Fix 2: Orphaned meal_foods
DELETE FROM meal_foods WHERE food_id IS NULL;

-- Fix 3: Reset food_servings
TRUNCATE food_servings;
-- Then re-run the data population part of migration
```

---

## 🎯 **NEXT STEPS AFTER VERIFICATION**

Once everything passes:

1. ✅ Mark migration as applied in your tracking system
2. 🚀 Deploy frontend to production (Vercel)
3. 📝 Update API documentation if needed
4. 👥 Test with real users
5. 📊 Monitor error logs for 24-48 hours
6. 🎉 Phase 2: Template search support (optional)

---

**Questions? Issues? Check IMPLEMENTATION_SUMMARY.md for more details.**
