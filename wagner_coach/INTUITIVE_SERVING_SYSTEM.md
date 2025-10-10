# Intuitive Serving Size System - Complete Implementation Guide

## Problem Statement

Users find it unintuitive to log food in grams. They think in **common servings**:
- Pizza → slices
- Banana → pieces (small/medium/large)
- Whey protein → scoops  
- Rice → cups
- Chicken breast → pieces/oz

## Solution: Dual-Input System

Allow users to input EITHER common servings OR grams, with automatic bidirectional conversion.

---

## Database Schema (Already Exists!)

### `foods_enhanced` table fields:

```sql
-- Base nutritional reference (database standard)
serving_size NUMERIC NOT NULL DEFAULT 100,    -- Usually 100
serving_unit TEXT NOT NULL DEFAULT 'g',       -- Usually 'g'

-- User-friendly household serving
household_serving_size TEXT,                  -- e.g., "1", "0.5", "2"  
household_serving_unit TEXT,                  -- e.g., "slice", "scoop", "medium", "cup"
```

### How it works:

**Example: Pizza Slice**
```sql
serving_size = 100              -- Nutrition data per 100g
serving_unit = 'g'
household_serving_size = '1'    -- One slice
household_serving_unit = 'slice'
```

To calculate grams per slice, you need actual slice weight. This can be:
1. **Stored in a separate table** (recommended)
2. **Calculated from typical ratios** (fallback)
3. **Crowdsourced from user logs** (future)

---

## Implementation Strategy

### Phase 1: Database Enhancement (RECOMMENDED)

Create a new table for serving conversions:

```sql
CREATE TABLE food_serving_conversions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  food_id UUID NOT NULL REFERENCES foods_enhanced(id) ON DELETE CASCADE,
  serving_name TEXT NOT NULL,              -- "1 slice", "1 medium", "1 scoop"
  serving_grams NUMERIC NOT NULL,          -- Actual weight in grams
  is_default BOOLEAN DEFAULT false,        -- Default serving for this food
  popularity_score INTEGER DEFAULT 0,      -- Track most-used servings
  source TEXT DEFAULT 'manual',            -- 'manual', 'usda', 'user_average'
  created_at TIMESTAMPTZ DEFAULT now(),
  UNIQUE(food_id, serving_name)
);

-- Index for fast lookups
CREATE INDEX idx_food_serving_conversions_food_id 
  ON food_serving_conversions(food_id);

CREATE INDEX idx_food_serving_conversions_default 
  ON food_serving_conversions(food_id) 
  WHERE is_default = true;
```

**Example data:**
```sql
-- Pizza slice conversions
INSERT INTO food_serving_conversions (food_id, serving_name, serving_grams, is_default) VALUES
  ('pizza-uuid', '1 slice', 120, true),
  ('pizza-uuid', '1 small slice', 90, false),
  ('pizza-uuid', '1 large slice', 150, false);

-- Banana conversions
INSERT INTO food_serving_conversions (food_id, serving_name, serving_grams, is_default) VALUES
  ('banana-uuid', '1 small', 90, false),
  ('banana-uuid', '1 medium', 118, true),
  ('banana-uuid', '1 large', 136, false);

-- Whey protein conversions
INSERT INTO food_serving_conversions (food_id, serving_name, serving_grams, is_default) VALUES
  ('whey-uuid', '1 scoop', 30, true),
  ('whey-uuid', '2 scoops', 60, false);
```

### Phase 2: Fallback Calculation (Current Approach)

If `food_serving_conversions` table doesn't exist, calculate from existing data:

```typescript
// Calculate grams per household serving
function getGramsPerHouseholdServing(food: Food): number {
  // If household serving is provided, estimate conversion
  if (food.household_serving_size && food.household_serving_unit) {
    const servingMultiplier = parseFloat(food.household_serving_size) || 1;
    
    // Common conversion estimates
    const unitToGrams: Record<string, number> = {
      'slice': 120,       // Average pizza/bread slice
      'medium': 118,      // Average medium fruit
      'small': 90,        // Average small fruit
      'large': 150,       // Average large fruit
      'scoop': 30,        // Standard protein scoop
      'cup': 195,         // Cooked rice/pasta
      'piece': 100,       // Generic piece
      'oz': 28.35,        // Ounce conversion
      'serving': 100,     // Default serving
    };
    
    const gramsPerUnit = unitToGrams[food.household_serving_unit.toLowerCase()] || 100;
    return servingMultiplier * gramsPerUnit;
  }
  
  // Fallback to serving_size if available
  return food.serving_size || 100;
}
```

---

## Frontend Implementation

### MealEditor Component Enhancement

**Current behavior:** Shows only grams input with +/- buttons

**New behavior:** Shows BOTH common servings AND grams with bidirectional sync

```tsx
interface FoodQuantityEditorProps {
  food: MealFood;
  onChange: (updated: MealFood) => void;
}

function FoodQuantityEditor({ food, onChange }: FoodQuantityEditorProps) {
  const [inputMode, setInputMode] = useState<'servings' | 'grams'>('servings');
  
  // Get conversion data
  const gramsPerServing = getGramsPerHouseholdServing(food);
  const servingsFromGrams = food.quantity / gramsPerServing;
  
  // Calculate nutrition per gram
  const nutritionPerGram = {
    calories: (food.calories || 0) / (food.serving_size || 100),
    protein: (food.protein_g || 0) / (food.serving_size || 100),
    carbs: (food.carbs_g || 0) / (food.serving_size || 100),
    fat: (food.fat_g || 0) / (food.serving_size || 100),
  };
  
  // Handlers
  const handleServingsChange = (newServings: number) => {
    const newGrams = newServings * gramsPerServing;
    onChange({
      ...food,
      quantity: newGrams,
      unit: 'g'
    });
  };
  
  const handleGramsChange = (newGrams: number) => {
    onChange({
      ...food,
      quantity: newGrams,
      unit: 'g'
    });
  };
  
  return (
    <div className="space-y-3">
      {/* Toggle between input modes */}
      <div className="flex gap-2 text-xs">
        <button
          onClick={() => setInputMode('servings')}
          className={inputMode === 'servings' ? 'text-iron-orange' : 'text-iron-gray'}
        >
          Common Servings
        </button>
        <span className="text-iron-gray">|</span>
        <button
          onClick={() => setInputMode('grams')}
          className={inputMode === 'grams' ? 'text-iron-orange' : 'text-iron-gray'}
        >
          Grams
        </button>
      </div>
      
      {inputMode === 'servings' ? (
        // Common servings input
        <div>
          <label className="text-xs text-iron-gray uppercase">
            {food.household_serving_unit || 'Servings'}
          </label>
          <div className="flex items-center gap-2 mt-1">
            <button
              onClick={() => handleServingsChange(Math.max(0.25, servingsFromGrams - 0.25))}
              className="bg-iron-gray/20 hover:bg-iron-gray/40 px-3 py-2 text-iron-white"
            >
              -
            </button>
            <input
              type="number"
              value={servingsFromGrams.toFixed(2)}
              onChange={(e) => handleServingsChange(parseFloat(e.target.value) || 0)}
              step="0.25"
              min="0"
              className="flex-1 bg-iron-black border border-iron-gray px-3 py-2 text-iron-white text-center"
            />
            <button
              onClick={() => handleServingsChange(servingsFromGrams + 0.25)}
              className="bg-iron-gray/20 hover:bg-iron-gray/40 px-3 py-2 text-iron-white"
            >
              +
            </button>
          </div>
          <p className="text-xs text-iron-gray mt-1">
            = {food.quantity.toFixed(0)}g
          </p>
        </div>
      ) : (
        // Grams input
        <div>
          <label className="text-xs text-iron-gray uppercase">Grams</label>
          <div className="flex items-center gap-2 mt-1">
            <button
              onClick={() => handleGramsChange(Math.max(1, food.quantity - 10))}
              className="bg-iron-gray/20 hover:bg-iron-gray/40 px-3 py-2 text-iron-white"
            >
              -10
            </button>
            <input
              type="number"
              value={food.quantity.toFixed(0)}
              onChange={(e) => handleGramsChange(parseFloat(e.target.value) || 0)}
              step="1"
              min="0"
              className="flex-1 bg-iron-black border border-iron-gray px-3 py-2 text-iron-white text-center"
            />
            <button
              onClick={() => handleGramsChange(food.quantity + 10)}
              className="bg-iron-gray/20 hover:bg-iron-gray/40 px-3 py-2 text-iron-white"
            >
              +10
            </button>
          </div>
          {food.household_serving_unit && (
            <p className="text-xs text-iron-gray mt-1">
              ≈ {servingsFromGrams.toFixed(2)} {food.household_serving_unit}
            </p>
          )}
        </div>
      )}
      
      {/* Nutrition preview */}
      <div className="text-xs text-iron-gray flex gap-3">
        <span>{Math.round(nutritionPerGram.calories * food.quantity)} cal</span>
        <span>{Math.round(nutritionPerGram.protein * food.quantity)}g P</span>
        <span>{Math.round(nutritionPerGram.carbs * food.quantity)}g C</span>
        <span>{Math.round(nutritionPerGram.fat * food.quantity)}g F</span>
      </div>
    </div>
  );
}
```

---

## User Experience Flow

### Example 1: Adding Pizza

1. User searches "pizza"
2. Selects "Pepperoni Pizza"
3. **UI shows:** 
   - Toggle: [**Common Servings**] | [Grams]
   - Input: 1.0 slices [ - ] [1.0] [ + ]
   - Below: "= 120g"
   - Nutrition: "290 cal • 12g P • 30g C • 11g F"
4. User clicks [+] → becomes 1.25 slices → 150g → nutrition updates
5. User toggles to "Grams" mode
6. Now shows: 150g [ -10 ] [150] [ +10 ]
7. Below: "≈ 1.25 slices"
8. User can adjust either way

### Example 2: Adding Banana

1. User searches "banana"
2. Selects "Banana, Raw"
3. **UI shows:**
   - Toggle: [**Common Servings**] | [Grams]
   - Input: 1.0 medium [ - ] [1.0] [ + ]
   - Below: "= 118g"
   - Nutrition: "105 cal • 1.3g P • 27g C • 0.4g F"
4. User wants a large banana → clicks [+] → 1.25 medium → 148g
5. Or user knows exact weight → switches to grams → types 148

### Example 3: Adding Protein Powder

1. User searches "whey protein"
2. Selects "Whey Protein Isolate"
3. **UI shows:**
   - Toggle: [**Common Servings**] | [Grams]
   - Input: 1.0 scoop [ - ] [1.0] [ + ]
   - Below: "= 30g"
   - Nutrition: "110 cal • 25g P • 2g C • 0g F"
4. User has 2 scoops → clicks [+] → 2.0 scoops → 60g
5. Nutrition doubles automatically

---

## Migration Path

### Step 1: Clean Existing Data

```bash
# Connect to Railway database
railway connect

# Or use psql directly
psql $DATABASE_URL
```

```sql
-- Run the cleanup migration
\i migrations/006_clean_all_food_data.sql
```

### Step 2: Repopulate with Clean Data

```bash
# Run all seed migrations in order
psql $DATABASE_URL < migrations/003a_seed_atomic_foods_proteins_carbs.sql
psql $DATABASE_URL < migrations/003b_seed_fruits_vegetables_fats.sql
psql $DATABASE_URL < migrations/003c_seed_beverages_supplements.sql
psql $DATABASE_URL < migrations/003d_seed_real_world_foods_phase1.sql
psql $DATABASE_URL < migrations/003e_seed_real_world_foods_phase2.sql
psql $DATABASE_URL < migrations/003f_seed_real_world_foods_phase3.sql
psql $DATABASE_URL < migrations/003g_seed_real_world_produce_phase4.sql
psql $DATABASE_URL < migrations/005_seed_comprehensive_foods_phase5.sql
```

### Step 3: Verify Data Quality

```sql
-- Check foods have household serving data
SELECT 
  COUNT(*) as total_foods,
  COUNT(household_serving_size) as with_household_serving,
  ROUND(COUNT(household_serving_size)::numeric / COUNT(*) * 100, 1) as percentage
FROM foods_enhanced;

-- Sample foods with household servings
SELECT 
  name,
  serving_size,
  serving_unit,
  household_serving_size,
  household_serving_unit
FROM foods_enhanced
WHERE household_serving_unit IS NOT NULL
LIMIT 20;
```

### Step 4: Update Frontend

Replace current `MealEditor` quantity input with the new `FoodQuantityEditor` component shown above.

---

## Future Enhancements

### 1. Multiple Serving Options

Some foods have multiple common servings:
- Banana: small (90g), medium (118g), large (136g)
- Pizza: small slice (90g), regular slice (120g), large slice (150g)

**Solution:** Dropdown to select serving type
```tsx
<select value={servingType} onChange={(e) => setServingType(e.target.value)}>
  <option value="small">Small (90g)</option>
  <option value="medium">Medium (118g)</option>
  <option value="large">Large (136g)</option>
</select>
```

### 2. Smart Defaults from User History

Track what servings users typically use:
```sql
-- Track user's preferred serving sizes
CREATE TABLE user_food_preferences (
  user_id UUID REFERENCES auth.users(id),
  food_id UUID REFERENCES foods_enhanced(id),
  typical_serving_grams NUMERIC,
  typical_serving_name TEXT,
  use_count INTEGER DEFAULT 1,
  last_used_at TIMESTAMPTZ DEFAULT now(),
  PRIMARY KEY (user_id, food_id)
);
```

When user adds a food they've logged before, default to their typical serving.

### 3. Barcode Scanning Integration

Scan product barcode → auto-fill exact serving size from package:
- Package says "1 serving = 28g" → use that
- Package says "1 bar = 60g" → use that

### 4. Visual Serving Guide

Show images of serving sizes:
- "What does 1 medium banana look like?"
- "How big is 6oz chicken breast?"
- Reference images help users estimate better

---

## Key Design Principles

1. **Flexibility:** Support both common servings AND grams
2. **Bidirectional:** Changes in one update the other
3. **Context-aware:** Show relevant units (slices for pizza, scoops for protein)
4. **Visual feedback:** Always show conversion (e.g., "= 120g" or "≈ 1.25 slices")
5. **Smart defaults:** Use most common serving size as default
6. **Progressive enhancement:** Works with current data, better with enhanced data

---

## Testing Scenarios

- [ ] User adds pizza by slices, sees grams update
- [ ] User adds banana by "medium", switches to grams, edits grams, switches back to see servings update
- [ ] User adds protein powder by scoops, adjusts to 1.5 scoops, sees 45g
- [ ] User adds rice by cups, sees conversion to grams
- [ ] User adds food without household serving (falls back to grams only)
- [ ] Nutrition values update correctly when quantity changes
- [ ] Mobile UI works with number inputs and +/- buttons
- [ ] Desktop UI allows direct typing of values

---

## Summary

**Current State:** Foods have `household_serving_size` and `household_serving_unit` but UI doesn't use them.

**Solution:** Implement dual-input system that allows toggling between common servings and grams.

**Benefits:**
- ✅ More intuitive for users
- ✅ Faster meal logging
- ✅ No data migration needed (schema already supports it)
- ✅ Falls back gracefully for foods without household servings
- ✅ Scales to future enhancements (multiple servings, user preferences, etc.)

**Next Steps:**
1. Run cleanup migration
2. Repopulate with clean seed data
3. Implement `FoodQuantityEditor` component
4. Test on various food types
5. Deploy and gather user feedback
