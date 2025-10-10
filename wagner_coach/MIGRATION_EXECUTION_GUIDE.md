# 🚀 Complete Migration Execution Guide

## Overview

This guide walks you through the complete process of:
1. Cleaning all existing food data
2. Repopulating with fresh, clean seed data
3. Verifying data quality
4. Testing the new intuitive serving system

---

## Prerequisites

- Railway CLI installed (`npm i -g @railway/cli`)
- PostgreSQL client (`psql`) installed
- Railway project linked (`railway link`)

---

## Step 1: Backup Current Data (OPTIONAL BUT RECOMMENDED)

```bash
# Connect to Railway database
railway run psql $DATABASE_URL

# Create backup of current foods (optional)
\copy (SELECT * FROM foods_enhanced) TO 'backup_foods_enhanced.csv' CSV HEADER;
\copy (SELECT * FROM meal_logs) TO 'backup_meal_logs.csv' CSV HEADER;
\copy (SELECT * FROM meal_foods) TO 'backup_meal_foods.csv' CSV HEADER;

# Exit
\q
```

---

## Step 2: Run Cleanup Migration (006)

**⚠️ WARNING: This will DELETE all food and meal data!**

```bash
# Navigate to migrations directory
cd wagner-coach-backend/migrations

# Run cleanup migration
railway run psql $DATABASE_URL < 006_clean_all_food_data.sql
```

**Expected output:**
```
Starting deletion process...
Deleting meal_foods...
DELETE 0 (or count of existing records)
Deleting meal_logs...
DELETE 0
Deleting meal_template_foods...
DELETE 0
Deleting meal_templates...
DELETE 0
Deleting foods_enhanced...
DELETE 0
Deletion complete.
```

---

## Step 3: Repopulate Food Database (003a → 005)

Run all seed migrations **in order**:

```bash
# Still in migrations directory

# Phase 1: Atomic foods - Proteins & Carbs
railway run psql $DATABASE_URL < 003a_seed_atomic_foods_proteins_carbs.sql

# Phase 2: Fruits, Vegetables & Fats
railway run psql $DATABASE_URL < 003b_seed_fruits_vegetables_fats.sql

# Phase 3: Beverages & Supplements
railway run psql $DATABASE_URL < 003c_seed_beverages_supplements.sql

# Phase 4: Real-world foods (Phase 1)
railway run psql $DATABASE_URL < 003d_seed_real_world_foods_phase1.sql

# Phase 5: Real-world foods (Phase 2)
railway run psql $DATABASE_URL < 003e_seed_real_world_foods_phase2.sql

# Phase 6: Real-world foods (Phase 3)
railway run psql $DATABASE_URL < 003f_seed_real_world_foods_phase3.sql

# Phase 7: Real-world produce (Phase 4)
railway run psql $DATABASE_URL < 003g_seed_real_world_produce_phase4.sql

# Phase 8: Comprehensive foods (Phase 5)
railway run psql $DATABASE_URL < 005_seed_comprehensive_foods_phase5.sql
```

**Each migration should output:**
```
INSERT 0 X (where X is the number of foods inserted)
```

---

## Step 4: Verify Data Quality

Run the comprehensive verification script:

```bash
railway run psql $DATABASE_URL < VERIFY_FOOD_DATA_QUALITY.sql
```

**Review the output for:**
- ✅ Total food count
- ✅ Percentage with household serving units (should be >70%)
- ✅ Nutrition data completeness (should be >95%)
- ✅ No duplicate foods
- ✅ No data integrity issues

---

## Step 5: Optional - Add Future Enhancements

### Option A: Multiple Serving Options (007)

Adds support for small/medium/large banana, etc.

```bash
railway run psql $DATABASE_URL < 007_food_serving_conversions.sql
```

### Option B: User Preferences (008)

Tracks user's preferred serving sizes for personalized defaults.

```bash
railway run psql $DATABASE_URL < 008_user_food_preferences.sql
```

---

## Step 6: Test the Frontend

### Start the dev server

```bash
# Navigate to frontend directory
cd ../../wagner-coach-clean

# Start development server
npm run dev
```

### Test scenarios

1. **Navigate to `/nutrition/log`**
2. **Add a food with household serving:**
   - Search for "pizza"
   - Click edit on the quantity
   - **Verify:** Toggle appears between "Common Servings" and "Grams"
   - **Verify:** Default shows "slices" with conversion to grams
   - **Test:** Adjust slices → grams update automatically
   - **Test:** Switch to "Grams" mode → adjust grams → servings update

3. **Add a food without household serving:**
   - Search for a generic food without household_serving_unit
   - **Verify:** Only shows "Grams" mode (no toggle)
   - **Verify:** Still works with +/- buttons

4. **Check nutrition calculation:**
   - Add multiple foods
   - Adjust quantities
   - **Verify:** Nutrition totals update correctly

---

## Quick Reference Commands

### Check food count
```bash
railway run psql $DATABASE_URL -c "SELECT COUNT(*) FROM foods_enhanced;"
```

### Check household serving coverage
```bash
railway run psql $DATABASE_URL -c "SELECT COUNT(CASE WHEN household_serving_unit IS NOT NULL THEN 1 END)::float / COUNT(*) * 100 AS percentage FROM foods_enhanced;"
```

### List sample foods with servings
```bash
railway run psql $DATABASE_URL -c "SELECT name, household_serving_unit, household_serving_size FROM foods_enhanced WHERE household_serving_unit IS NOT NULL LIMIT 10;"
```

### Reset everything and start over
```bash
railway run psql $DATABASE_URL < 006_clean_all_food_data.sql
# Then run all 003a through 005 again
```

---

## Troubleshooting

### Issue: Migration fails with "relation does not exist"
**Solution:** Run the base schema migration first:
```bash
railway run psql $DATABASE_URL < 000_SCHEMA.sql
```

### Issue: Duplicate key violations during seed
**Solution:** Clean database first:
```bash
railway run psql $DATABASE_URL < 006_clean_all_food_data.sql
```

### Issue: Frontend shows old data
**Solution:** 
1. Clear browser cache
2. Restart dev server
3. Check API is calling correct endpoint

### Issue: Nutrition calculations are wrong
**Solution:** Verify serving_size in database:
```bash
railway run psql $DATABASE_URL -c "SELECT name, serving_size, calories FROM foods_enhanced WHERE name ILIKE '%pizza%';"
```

---

## Expected Results

After completing all migrations, you should have:

✅ **~200-400 foods** in the database  
✅ **70%+ with household servings** (slices, scoops, medium, etc.)  
✅ **95%+ with complete nutrition data** (calories, protein, carbs, fat)  
✅ **Dual-input UI** working for foods with household servings  
✅ **Fallback to grams** for foods without household servings  
✅ **Real-time nutrition updates** as quantity changes  
✅ **Bidirectional conversion** between servings ↔ grams  

---

## Next Steps

1. **User Testing:** Have real users try logging meals
2. **Feedback:** Collect pain points and confusion
3. **Iteration:** Adjust serving sizes based on usage data
4. **Enhancement:** Add migration 007 for multiple serving options
5. **Personalization:** Add migration 008 for user preferences

---

## Support

If you encounter issues:
1. Check the `VERIFY_FOOD_DATA_QUALITY.sql` output
2. Review the `INTUITIVE_SERVING_SYSTEM.md` documentation
3. Test individual components in isolation
4. Check browser console for frontend errors
5. Review Railway logs for backend errors

---

## Clean Slate (Nuclear Option)

If everything is broken and you want to start completely fresh:

```bash
# Drop and recreate entire schema
railway run psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"

# Run base schema
railway run psql $DATABASE_URL < 000_SCHEMA.sql

# Run all improvements
railway run psql $DATABASE_URL < 001_meal_logging_improvements.sql
railway run psql $DATABASE_URL < 002_food_architecture_cleanup.sql

# Repopulate food data (003a through 005)
# Follow Step 3 above
```

**⚠️ WARNING: This deletes EVERYTHING including user accounts and meal logs!**

---

## Success Criteria

Migration is successful when:
- [x] All seed migrations complete without errors
- [x] Verification script shows ✓ Good/Excellent for all checks
- [x] Frontend loads food list without errors
- [x] Can log a meal with household serving (e.g., pizza slice)
- [x] Can toggle between servings and grams
- [x] Nutrition calculations are accurate
- [x] No console errors in browser
- [x] Mobile responsive UI works

---

**Last Updated:** 2025-01-10  
**Migration Version:** 006 → 008  
**Frontend Version:** FoodQuantityEditor v1.0
