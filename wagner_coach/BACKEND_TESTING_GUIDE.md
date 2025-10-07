# Backend Testing Guide - Meal Logging with Relational Schema

**Date**: 2025-10-07
**Status**: ✅ Migrations Complete | ✅ Backend Updated | ⏳ Ready for Testing

---

## 🎯 What Was Completed

### 1. Database Migrations (Run on Supabase)
✅ **Migration 007**: Created `meal_foods` relational table with triggers
✅ **Migration 008**: Seeded 70+ common foods with complete nutrition
✅ **Migration 009**: Added helper functions and indexes

**Result**: Database now uses proper many-to-many relationship instead of JSONB denormalization.

### 2. Backend Service Updates
✅ **food_search_service.py**: Updated to query `meal_foods` table with JOIN
✅ **meals.py API**: Switched to `meal_logging_service_v2`
✅ **Committed & Pushed**: Changes in Git (commit `94e5fa0`)

**Result**: Backend now uses relational schema with auto-calculated nutrition totals via triggers.

---

## 🚀 Next Steps: Testing

### Step 1: Start Backend Server

```bash
cd wagner-coach-backend

# Ensure .env has all required variables:
# - SUPABASE_URL
# - SUPABASE_KEY
# - SUPABASE_SERVICE_KEY
# - OPENAI_API_KEY (etc.)

# Start the server
uvicorn app.main:app --reload --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

If you see errors about missing modules, install dependencies:
```bash
poetry install
```

---

### Step 2: Test Food Search Endpoints

#### Get Your JWT Token

**Option A**: From Supabase Dashboard
1. Go to Supabase Dashboard → Authentication → Users
2. Click on your test user
3. Copy the JWT token from "User JWT"

**Option B**: From Frontend Console
1. Open your frontend in browser
2. Open DevTools → Console
3. Run: `localStorage.getItem('supabase.auth.token')`
4. Copy the access_token value

#### Test Search Foods

```bash
# Replace YOUR_JWT_TOKEN with actual token
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  "http://localhost:8000/api/v1/foods/search?q=chicken&limit=10"
```

**Expected Response**:
```json
{
  "foods": [
    {
      "id": "uuid",
      "name": "Chicken Breast, Grilled, Skinless",
      "brand_name": null,
      "food_group": "Protein",
      "serving_size": 100,
      "serving_unit": "g",
      "calories": 165,
      "protein_g": 31,
      "carbs_g": 0,
      "fat_g": 3.6,
      "fiber_g": 0,
      "sugar_g": 0,
      "sodium_mg": 74,
      "is_recent": false,
      "is_generic": true
    },
    ...
  ],
  "total": 5,
  "limit": 10,
  "query": "chicken"
}
```

#### Test Recent Foods

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  "http://localhost:8000/api/v1/foods/recent?limit=10"
```

**Expected Response** (if you have logged meals before):
```json
{
  "foods": [
    {
      "id": "uuid",
      "name": "Chicken Breast, Grilled, Skinless",
      "last_quantity": 200,
      "last_unit": "g",
      "last_logged_at": "2025-10-06T12:30:00Z",
      "log_count": 5,
      "is_recent": true,
      ...
    }
  ]
}
```

If you haven't logged meals yet, this will return `{"foods": []}`.

---

### Step 3: Test Meal Logging Flow

#### Create a Meal

```bash
curl -X POST "http://localhost:8000/api/v1/meals" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Chicken and Rice Bowl",
    "category": "lunch",
    "logged_at": "2025-10-07T12:30:00Z",
    "notes": "Post-workout meal",
    "foods": [
      {
        "food_id": "CHICKEN_BREAST_UUID",
        "quantity": 200,
        "unit": "g"
      },
      {
        "food_id": "BROWN_RICE_UUID",
        "quantity": 1,
        "unit": "cup"
      }
    ]
  }'
```

**How to Get Food UUIDs**:
1. First search for foods: `/api/v1/foods/search?q=chicken`
2. Copy the `id` field from the response
3. Use those UUIDs in the create meal request

**Expected Response**:
```json
{
  "id": "meal-uuid",
  "user_id": "your-user-id",
  "name": "Chicken and Rice Bowl",
  "category": "lunch",
  "logged_at": "2025-10-07T12:30:00Z",
  "notes": "Post-workout meal",
  "total_calories": 495,  // Auto-calculated by trigger!
  "total_protein_g": 39,   // Auto-calculated by trigger!
  "total_carbs_g": 45,     // Auto-calculated by trigger!
  "total_fat_g": 7.2,      // Auto-calculated by trigger!
  "foods": [
    {
      "food_id": "uuid",
      "name": "Chicken Breast, Grilled, Skinless",
      "quantity": 200,
      "unit": "g",
      "calories": 330,
      ...
    },
    {
      "food_id": "uuid",
      "name": "Brown Rice, Cooked",
      "quantity": 1,
      "unit": "cup",
      "calories": 165,
      ...
    }
  ],
  "source": "manual",
  "created_at": "2025-10-07T12:35:00Z"
}
```

#### Get Meal by ID

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  "http://localhost:8000/api/v1/meals/MEAL_UUID"
```

#### Get All User Meals

```bash
curl -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  "http://localhost:8000/api/v1/meals?limit=20"
```

#### Update Meal

```bash
curl -X PATCH "http://localhost:8000/api/v1/meals/MEAL_UUID" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "notes": "Updated notes",
    "foods": [
      {
        "food_id": "CHICKEN_BREAST_UUID",
        "quantity": 250,
        "unit": "g"
      }
    ]
  }'
```

**Expected**: Totals recalculated automatically.

#### Delete Meal

```bash
curl -X DELETE "http://localhost:8000/api/v1/meals/MEAL_UUID" \
  -H "Authorization: Bearer YOUR_JWT_TOKEN"
```

**Expected**: 204 No Content (success)

---

### Step 4: Test Frontend Integration

Once backend is running on `localhost:8000`:

1. **Start Frontend**:
   ```bash
   cd wagner-coach-clean
   npm run dev
   ```

2. **Navigate to Meal Logging**:
   - Go to `/nutrition/log`
   - Search for "chicken" in the food search
   - Should see results from database

3. **Test AI Coach Meal Preview**:
   - Go to `/coach`
   - Type: "I had 6oz chicken breast and 1 cup rice for lunch"
   - AI should detect it as a meal
   - Preview should show the same UI as manual logging
   - Edit and save

4. **Verify Data**:
   - Check `/nutrition` dashboard
   - Should see logged meals
   - Totals should be accurate

---

## 🔍 Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'app'`
```bash
cd wagner-coach-backend
poetry install
poetry run uvicorn app.main:app --reload --port 8000
```

**Error**: `SUPABASE_URL environment variable not set`
- Copy `.env.example` to `.env`
- Fill in all required environment variables

### Food Search Returns Empty

**Check**: Did migration 008 seed the foods?
```sql
-- Run on Supabase SQL Editor
SELECT COUNT(*) FROM foods_enhanced;
-- Should return ~70
```

**Check**: Is JWT token valid?
```bash
# Decode JWT to see expiration
echo "YOUR_JWT_TOKEN" | jwt decode -
```

### Meal Creation Fails

**Error**: `Food with ID 'xyz' not found`
- Use `/api/v1/foods/search` to get valid food IDs
- Copy the `id` field from search results

**Error**: `duplicate key value violates unique constraint`
- You might be trying to add the same food twice to one meal
- The schema has `UNIQUE(meal_log_id, food_id)`

### Totals Not Calculating

**Check**: Are triggers enabled?
```sql
-- Run on Supabase SQL Editor
SELECT * FROM pg_trigger
WHERE tgname LIKE '%meal_foods%';
-- Should see 3 triggers
```

---

## ✅ Success Criteria

You know it's working when:

1. ✅ Backend starts without errors
2. ✅ `/api/v1/foods/search?q=chicken` returns foods from database
3. ✅ Can create a meal with multiple foods
4. ✅ Meal totals are auto-calculated correctly
5. ✅ Frontend food search shows database results
6. ✅ AI coach meal preview uses same UI as manual logging
7. ✅ Can save meal from coach preview
8. ✅ Meals appear in nutrition dashboard

---

## 📊 Database Verification

### Check Schema Status

```sql
-- Run on Supabase SQL Editor

-- 1. Check meal_foods table exists
SELECT COUNT(*) FROM meal_foods;

-- 2. Check foods seeded
SELECT COUNT(*) FROM foods_enhanced;
-- Should be ~70

-- 3. Check triggers exist
SELECT tgname, tgtype FROM pg_trigger
WHERE tgrelid = 'meal_foods'::regclass;

-- 4. Check helper functions exist
SELECT proname FROM pg_proc
WHERE proname IN (
  'get_meal_with_foods',
  'calculate_food_nutrition',
  'update_daily_nutrition_summary'
);

-- 5. Test a food search
SELECT id, name, calories, protein_g
FROM foods_enhanced
WHERE name ILIKE '%chicken%'
LIMIT 5;
```

---

## 🎉 What's Changed

### Old Schema (JSONB) ❌
```
meal_logs
├── id
├── foods (JSONB array)  ❌ Denormalized
├── total_calories (manual sum)
└── ...
```

**Problems**:
- No foreign keys
- Manual totals (prone to errors)
- Can't query "all meals with chicken"

### New Schema (Relational) ✅
```
meal_logs                        meal_foods                    foods_enhanced
├── id ─────────────────────────┬─ meal_log_id                ├── id
├── total_calories (auto)  ←────┼─ calories (cached)         ├── name
└── ...                         └─ ...                        └── ...
```

**Benefits**:
- ✅ Foreign key constraints
- ✅ Auto-calculated totals (triggers)
- ✅ Can query by food type
- ✅ Atomic operations

---

## 📝 Next Actions

### Immediate (You)
1. Start backend server: `uvicorn app.main:app --reload --port 8000`
2. Test food search endpoint with curl
3. Get a food ID from search results
4. Create a test meal
5. Verify totals are calculated correctly

### Testing (QA)
1. Test full meal logging flow (create, edit, delete)
2. Test AI coach meal detection and preview
3. Test on mobile devices
4. Verify nutrition calculations are accurate

### Production Deployment
1. Deploy backend to Railway/Fly.io
2. Run migrations on production Supabase
3. Monitor errors in Sentry
4. Verify API response times
5. Check AI cost logs

---

**Status**: ✅ Ready for local testing

Start your backend server and test the endpoints! 🚀
