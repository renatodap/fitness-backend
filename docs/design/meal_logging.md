# Meal Logging Feature Design

**Version:** 1.0
**Status:** Production
**Last Updated:** 2025-10-06

---

## 📋 Overview

Comprehensive meal logging system inspired by MyFitnessPal's intuitive UX, with both manual logging and AI-powered quick entry editing capabilities.

### Core Capabilities
1. **Manual Meal Logging** - Log meals by searching food database and building meal
2. **Quick Entry Editing** - Edit AI-detected meals before saving
3. **Food Database Search** - Fast autocomplete search with 10,000+ foods
4. **Meal Builder** - Add/remove/edit foods with quantity and unit selection
5. **Recent Foods** - Quick access to recently logged foods
6. **Meal Templates** - Save and reuse common meals

---

## 🎯 User Stories

### Story 1: Manual Meal Logging
**As a user**, I want to manually log a meal by searching for foods and adding them to my meal, so that I can track my nutrition accurately.

**Acceptance Criteria:**
- User can navigate to /meals/log page from dashboard
- User can search for foods with autocomplete suggestions
- User can select foods and specify quantity/unit
- User can add multiple foods to a single meal
- User can remove foods from meal
- User can edit food quantities and units
- User can select meal type (breakfast, lunch, dinner, snack)
- User can set meal time
- User can add notes
- Nutrition totals update in real-time as foods are added/removed
- User can save meal to database

### Story 2: Quick Entry Meal Editing
**As a user**, I want to edit AI-detected meals before saving, so that I can correct any mistakes and adjust quantities.

**Acceptance Criteria:**
- After AI processes quick entry, user sees editable meal preview
- User can add additional foods AI missed
- User can remove incorrectly detected foods
- User can adjust quantities and units for each food
- User can change meal type and time
- User can add/edit notes
- Nutrition totals update in real-time
- User must confirm before saving

### Story 3: Food Search with Autocomplete
**As a user**, I want to quickly find foods using autocomplete search, so that I can log meals efficiently.

**Acceptance Criteria:**
- Search shows results as user types (debounced)
- Results show food name, brand, and serving size
- Results prioritize: recent foods > frequent foods > database matches
- Results show nutrition preview on hover
- User can select food with keyboard (↓↑ Enter) or mouse
- Search supports partial matches and typos

### Story 4: Recent/Favorite Foods
**As a user**, I want quick access to recently logged foods, so that I can log repeat meals faster.

**Acceptance Criteria:**
- Recent foods tab shows last 20 unique foods logged
- Foods show with last logged quantity/unit
- User can add recent food with single click
- Recent foods persist across sessions

---

## 🗄️ Database Schema

### Existing Tables (No Changes Needed)

#### `foods_enhanced`
Already has comprehensive schema:
```sql
CREATE TABLE foods_enhanced (
  id UUID PRIMARY KEY,
  name TEXT NOT NULL,
  brand_name TEXT,
  food_group TEXT,
  serving_size NUMERIC NOT NULL DEFAULT 100,
  serving_unit TEXT NOT NULL DEFAULT 'g',
  calories NUMERIC,
  protein_g NUMERIC,
  total_carbs_g NUMERIC,
  total_fat_g NUMERIC,
  dietary_fiber_g NUMERIC,
  total_sugars_g NUMERIC,
  sodium_mg NUMERIC,
  -- ... many more nutrients
  search_vector TSVECTOR,
  popularity_score INTEGER DEFAULT 0,
  search_count INTEGER DEFAULT 0,
  is_generic BOOLEAN DEFAULT FALSE,
  is_branded BOOLEAN DEFAULT FALSE,
  data_quality_score NUMERIC,
  created_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### `meal_logs`
Already has all needed fields:
```sql
CREATE TABLE meal_logs (
  id UUID PRIMARY KEY,
  user_id UUID NOT NULL,
  name TEXT,
  category meal_category NOT NULL DEFAULT 'other',  -- breakfast, lunch, dinner, snack
  logged_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  notes TEXT,
  total_calories NUMERIC DEFAULT 0,
  total_protein_g NUMERIC DEFAULT 0,
  total_carbs_g NUMERIC DEFAULT 0,
  total_fat_g NUMERIC DEFAULT 0,
  total_fiber_g NUMERIC DEFAULT 0,
  total_sugar_g NUMERIC,
  total_sodium_mg NUMERIC,
  foods JSONB DEFAULT '[]'::jsonb,  -- Array of food items
  source TEXT DEFAULT 'manual',  -- 'manual' | 'quick_entry'
  estimated BOOLEAN DEFAULT FALSE,
  confidence_score NUMERIC,
  image_url TEXT,
  meal_quality_score NUMERIC,
  macro_balance_score NUMERIC,
  adherence_to_goals NUMERIC,
  tags TEXT[],
  quick_entry_log_id UUID,
  ai_extracted BOOLEAN DEFAULT FALSE,
  ai_confidence NUMERIC,
  extraction_metadata JSONB DEFAULT '{}'::jsonb,
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW()
);
```

#### `foods` JSONB Structure
Each item in the `foods` JSONB array:
```typescript
{
  food_id: string;       // UUID from foods_enhanced
  name: string;          // Food name (for display)
  brand: string | null;  // Brand name if applicable
  quantity: number;      // e.g., 2
  unit: string;          // e.g., "oz", "g", "cup", "serving"
  serving_size: number;  // Base serving size from foods_enhanced
  serving_unit: string;  // Base serving unit from foods_enhanced
  calories: number;      // Scaled calories for this quantity
  protein_g: number;     // Scaled protein
  carbs_g: number;       // Scaled carbs
  fat_g: number;         // Scaled fat
  fiber_g: number;       // Scaled fiber
  sugar_g: number | null;
  sodium_mg: number | null;
  order: number;         // Display order in meal
}
```

### New Tables (Optional Enhancement)

#### `user_recent_foods` (Optional)
Track recently logged foods per user for quick access:
```sql
CREATE TABLE user_recent_foods (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id),
  food_id UUID NOT NULL REFERENCES foods_enhanced(id),
  last_quantity NUMERIC,
  last_unit TEXT,
  last_logged_at TIMESTAMPTZ NOT NULL,
  log_count INTEGER DEFAULT 1,
  UNIQUE(user_id, food_id)
);

CREATE INDEX idx_user_recent_foods_user_time ON user_recent_foods(user_id, last_logged_at DESC);
```

---

## 🔌 API Endpoints

### 1. Food Search
**`GET /api/v1/foods/search`**

Search foods with autocomplete and smart ranking.

**Query Parameters:**
- `q` (required): Search query
- `limit` (optional): Max results (default: 20)
- `include_recent` (optional): Include user's recent foods (default: true)

**Response:**
```json
{
  "foods": [
    {
      "id": "uuid",
      "name": "Chicken Breast, Grilled",
      "brand": null,
      "food_group": "Poultry",
      "serving_size": 100,
      "serving_unit": "g",
      "calories": 165,
      "protein_g": 31,
      "carbs_g": 0,
      "fat_g": 3.6,
      "fiber_g": 0,
      "is_recent": false,
      "last_logged_quantity": null,
      "last_logged_unit": null,
      "data_quality_score": 1.0
    }
  ],
  "total": 145,
  "limit": 20
}
```

### 2. Get Recent Foods
**`GET /api/v1/foods/recent`**

Get user's recently logged foods.

**Query Parameters:**
- `limit` (optional): Max results (default: 20)

**Response:**
```json
{
  "foods": [
    {
      "id": "uuid",
      "name": "Chicken Breast, Grilled",
      "brand": null,
      "serving_size": 100,
      "serving_unit": "g",
      "calories": 165,
      "protein_g": 31,
      "carbs_g": 0,
      "fat_g": 3.6,
      "fiber_g": 0,
      "last_quantity": 6,
      "last_unit": "oz",
      "last_logged_at": "2025-10-05T18:30:00Z",
      "log_count": 15
    }
  ]
}
```

### 3. Create Meal Log (Manual)
**`POST /api/v1/meals`**

Create new meal log with foods.

**Request:**
```json
{
  "name": "Chicken and Rice Bowl",
  "category": "lunch",
  "logged_at": "2025-10-06T12:30:00Z",
  "notes": "Post-workout meal",
  "foods": [
    {
      "food_id": "uuid-chicken",
      "quantity": 6,
      "unit": "oz"
    },
    {
      "food_id": "uuid-rice",
      "quantity": 1,
      "unit": "cup"
    },
    {
      "food_id": "uuid-broccoli",
      "quantity": 2,
      "unit": "cup"
    }
  ]
}
```

**Response:**
```json
{
  "id": "uuid",
  "user_id": "uuid",
  "name": "Chicken and Rice Bowl",
  "category": "lunch",
  "logged_at": "2025-10-06T12:30:00Z",
  "notes": "Post-workout meal",
  "total_calories": 650,
  "total_protein_g": 55,
  "total_carbs_g": 70,
  "total_fat_g": 8,
  "total_fiber_g": 6,
  "foods": [
    {
      "food_id": "uuid-chicken",
      "name": "Chicken Breast, Grilled",
      "brand": null,
      "quantity": 6,
      "unit": "oz",
      "serving_size": 100,
      "serving_unit": "g",
      "calories": 280,
      "protein_g": 52,
      "carbs_g": 0,
      "fat_g": 6,
      "fiber_g": 0,
      "order": 1
    }
    // ... other foods
  ],
  "source": "manual",
  "created_at": "2025-10-06T12:30:15Z"
}
```

### 4. Update Meal Log
**`PATCH /api/v1/meals/{meal_id}`**

Update existing meal (edit foods, quantities, etc.).

**Request:**
```json
{
  "name": "Updated Meal Name",
  "category": "dinner",
  "notes": "Updated notes",
  "foods": [
    // Full updated foods array
  ]
}
```

### 5. Delete Meal Log
**`DELETE /api/v1/meals/{meal_id}`**

Delete a meal log.

### 6. Get User Meals
**`GET /api/v1/meals`**

Get user's meal logs with filtering.

**Query Parameters:**
- `start_date` (optional): Filter by date range
- `end_date` (optional): Filter by date range
- `category` (optional): Filter by meal type
- `limit` (optional): Max results (default: 50)
- `offset` (optional): Pagination offset

---

## 💰 AI Cost Optimization

**FREE for manual logging** - No AI calls needed.

**Quick Entry Editing:**
- Initial AI parsing: ~$0.0001 (Groq Llama 3.3 70B)
- No additional cost for editing/confirmation
- Total: $0.0001 per quick entry

---

## 🎨 Frontend Components

### 1. Manual Meal Logging Page (`/meals/log`)

```
┌─────────────────────────────────────────┐
│  ← Back to Dashboard                    │
│                                          │
│  Log Meal                                │
│                                          │
│  ┌─────────────────────────────────┐    │
│  │ 🔍 Search foods...              │    │
│  └─────────────────────────────────┘    │
│                                          │
│  Recent Foods:                           │
│  ┌─────┬─────┬─────┬─────┬─────┐       │
│  │ 🍗  │ 🍚  │ 🥦  │ 🥚  │ 🐟  │       │
│  └─────┴─────┴─────┴─────┴─────┘       │
│                                          │
│  Foods in this meal:                     │
│  ┌─────────────────────────────────┐    │
│  │ Chicken Breast, Grilled         │    │
│  │ ┌─────┐ ┌─────────┐  🗑️        │    │
│  │ │  6  │ │   oz  ▾ │            │    │
│  │ └─────┘ └─────────┘            │    │
│  │ 280 cal · 52g protein           │    │
│  └─────────────────────────────────┘    │
│                                          │
│  ┌─────────────────────────────────┐    │
│  │ Brown Rice, Cooked              │    │
│  │ ┌─────┐ ┌─────────┐  🗑️        │    │
│  │ │  1  │ │  cup  ▾ │            │    │
│  │ └─────┘ └─────────┘            │    │
│  │ 216 cal · 5g protein            │    │
│  └─────────────────────────────────┘    │
│                                          │
│  Meal Details:                           │
│  ┌────────────────┬────────────────┐    │
│  │ Meal Type:     │ Time:          │    │
│  │ Lunch        ▾ │ 12:30 PM     ▾ │    │
│  └────────────────┴────────────────┘    │
│                                          │
│  Notes (optional):                       │
│  ┌─────────────────────────────────┐    │
│  │ Post-workout meal               │    │
│  └─────────────────────────────────┘    │
│                                          │
│  ┌─────────────────────────────────┐    │
│  │  TOTALS                         │    │
│  │  650 cal · 55g P · 70g C · 8g F│    │
│  └─────────────────────────────────┘    │
│                                          │
│  ┌──────────────────────────────────┐   │
│  │       💾 Save Meal               │   │
│  └──────────────────────────────────┘   │
└─────────────────────────────────────────┘
```

### 2. Food Search Autocomplete Component

```typescript
interface FoodSearchProps {
  onSelect: (food: Food) => void;
  placeholder?: string;
  includeRecent?: boolean;
}

const FoodSearch: React.FC<FoodSearchProps>
```

### 3. Meal Editor Component

```typescript
interface MealEditorProps {
  initialFoods?: FoodItem[];
  onFoodsChange: (foods: FoodItem[]) => void;
  mealType: MealType;
  onMealTypeChange: (type: MealType) => void;
  mealTime: Date;
  onMealTimeChange: (time: Date) => void;
  notes: string;
  onNotesChange: (notes: string) => void;
}

const MealEditor: React.FC<MealEditorProps>
```

### 4. Food Item Row Component

```typescript
interface FoodItemRowProps {
  food: FoodItem;
  onQuantityChange: (quantity: number) => void;
  onUnitChange: (unit: string) => void;
  onRemove: () => void;
  availableUnits: string[];
}

const FoodItemRow: React.FC<FoodItemRowProps>
```

---

## 🧪 Testing Strategy

### Backend Tests

#### Unit Tests
- `test_food_search_ranking()` - Verify search results ranking
- `test_food_search_partial_match()` - Verify partial matching
- `test_food_search_typo_tolerance()` - Verify fuzzy matching
- `test_meal_nutrition_calculation()` - Verify totals calculation
- `test_unit_conversion()` - Verify unit conversions
- `test_recent_foods_tracking()` - Verify recent foods logic

#### Integration Tests
- `test_create_meal_endpoint()` - Test meal creation API
- `test_update_meal_endpoint()` - Test meal update API
- `test_delete_meal_endpoint()` - Test meal deletion API
- `test_food_search_endpoint()` - Test search API
- `test_recent_foods_endpoint()` - Test recent foods API
- `test_meal_with_authentication()` - Test auth middleware

### Frontend Tests

#### Component Tests
- `FoodSearch.test.tsx` - Test autocomplete behavior
- `MealEditor.test.tsx` - Test meal building
- `FoodItemRow.test.tsx` - Test quantity/unit editing
- `MealLoggingPage.test.tsx` - Test full page flow

#### E2E Tests (Playwright)
- `meal-logging-manual.spec.ts` - Test manual logging flow
- `meal-logging-quick-entry-edit.spec.ts` - Test quick entry editing
- `food-search.spec.ts` - Test search UX
- `recent-foods.spec.ts` - Test recent foods

---

## 📊 Success Metrics

### Performance
- Food search results < 100ms
- Meal save < 500ms
- Page load < 1s

### UX
- Average foods per meal: 3-5
- Time to log meal: < 60 seconds
- Search abandonment rate: < 10%

### Accuracy
- Food search relevance: > 90%
- Nutrition calculation errors: 0%

---

## 🚀 Rollout Plan

### Phase 1: Backend Foundation
1. ✅ Seed food database (500+ foods)
2. ✅ Create food search endpoint
3. ✅ Create meal CRUD endpoints
4. ✅ Write backend tests

### Phase 2: Frontend Foundation
1. Create `/meals/log` page
2. Create food search component
3. Create meal editor component
4. Create food item row component

### Phase 3: Integration
1. Connect frontend to backend
2. Add loading/error states
3. Add optimistic updates
4. Add keyboard shortcuts

### Phase 4: Polish
1. Add recent foods
2. Add meal templates (future)
3. Add barcode scanning (future)
4. Add macro targets visualization

---

## 🎯 Future Enhancements

1. **Barcode Scanning** - Scan barcodes to add foods
2. **Meal Templates** - Save common meals for quick logging
3. **Meal Photos** - Attach photos to meals
4. **Copy Meals** - Copy yesterday's breakfast
5. **Meal Sharing** - Share meal ideas with friends
6. **Nutrition Insights** - AI analysis of meal quality
7. **Recipe Builder** - Create recipes from meals
8. **Shopping Lists** - Generate from meal plans

---

**Status:** Ready for implementation
**Estimated Time:** 3-4 days (Backend: 1.5 days, Frontend: 1.5 days, Testing: 1 day)
