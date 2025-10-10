# Food Quantity System Redesign - Complete Plan

## Executive Summary

**Problem:** The current food quantity system is fundamentally broken. Users cannot properly edit food quantities because:
1. Only one quantity representation is stored (either servings OR grams, not both)
2. Conversions are lossy and inconsistent
3. When users edit one field, the other doesn't update correctly
4. Nutrition calculations are unreliable due to conversion errors

**Solution:** Redesign the system to **store and track both serving quantities and gram quantities simultaneously**, with bidirectional real-time synchronization.

**Impact:** This requires:
- Database schema changes (3 new columns in `meal_foods`)
- Backend API updates (Python service layer)
- Frontend component redesign (React components)
- Data migration (existing meal logs)
- Comprehensive testing

**Timeline:** 3-5 days for full implementation and testing

---

## Current System Analysis

### Database Schema (Current State)

```sql
-- foods_enhanced table
CREATE TABLE foods_enhanced (
    id UUID PRIMARY KEY,
    name TEXT NOT NULL,
    serving_size NUMERIC NOT NULL DEFAULT 100,  -- grams per serving
    serving_unit TEXT NOT NULL DEFAULT 'g',
    household_serving_size TEXT,                 -- e.g., "1" or "0.5"
    household_serving_unit TEXT,                 -- e.g., "slice", "medium", "scoop"
    calories NUMERIC,
    protein_g NUMERIC,
    -- ... other nutrition fields
);

-- meal_foods table (CURRENT - PROBLEMATIC)
CREATE TABLE meal_foods (
    id UUID PRIMARY KEY,
    meal_log_id UUID NOT NULL,
    food_id UUID,
    quantity NUMERIC NOT NULL,    -- ⚠️ SINGLE VALUE - AMBIGUOUS
    unit TEXT NOT NULL,            -- ⚠️ "g", "slice", "serving", etc.
    calories NUMERIC,              -- Calculated but may be wrong
    protein_g NUMERIC,
    -- ... other nutrition fields
);
```

### The Core Problem

**Example Scenario:**
1. User selects "Bread, whole wheat"
   - `household_serving_size`: "1"
   - `household_serving_unit`: "slice"
   - `serving_size`: 28 (grams per slice)

2. User logs "2 slices"
   - Stored as: `quantity=2`, `unit="slice"`
   - Backend calculates: 2 × 28g = 56g
   - Nutrition calculated from 56g ✓

3. User wants to edit to "50g" instead
   - Current system: Changes `quantity=50`, `unit="g"`
   - **PROBLEM:** Lost the serving representation!
   - If user switches back to servings, system shows "50 servings" ❌

4. **The Math is Broken:**
   - No way to maintain both "2 slices" and "56g" simultaneously
   - Conversions are lossy
   - User experience is confusing and frustrating

---

## Proposed Solution

### New Database Schema

```sql
-- meal_foods table (NEW - FIXED)
ALTER TABLE meal_foods 
ADD COLUMN serving_quantity NUMERIC(10,3),      -- e.g., 2.5
ADD COLUMN serving_unit VARCHAR(50),            -- e.g., "slice", "medium", NULL
ADD COLUMN gram_quantity NUMERIC(10,3),         -- ALWAYS in grams
ADD COLUMN last_edited_field VARCHAR(20) DEFAULT 'grams';  -- 'serving' or 'grams'

-- Keep old columns temporarily for migration safety
-- Will be removed after 2 weeks of stability
```

### How It Works

**Storage:**
- `serving_quantity`: The number of servings (e.g., 2.5 slices)
- `serving_unit`: The unit name (e.g., "slice", "medium", "scoop")
- `gram_quantity`: The equivalent weight in grams (e.g., 70g)
- `last_edited_field`: Tracks which field the user last edited

**Example Data:**
```json
{
  "food_id": "uuid-bread",
  "serving_quantity": 2,
  "serving_unit": "slice",
  "gram_quantity": 56,
  "last_edited_field": "serving"
}
```

**User Edits Serving → Grams Update:**
```
User changes: 2 slices → 3 slices
Backend calculates: 3 × 28g = 84g
Database stores:
  - serving_quantity: 3
  - serving_unit: "slice"
  - gram_quantity: 84
  - last_edited_field: "serving"
Nutrition calculated from: 84g ✓
```

**User Edits Grams → Serving Updates:**
```
User changes: 84g → 70g
Backend calculates: 70g ÷ 28g/slice = 2.5 slices
Database stores:
  - serving_quantity: 2.5
  - serving_unit: "slice"
  - gram_quantity: 70
  - last_edited_field: "grams"
Nutrition calculated from: 70g ✓
```

---

## Implementation Plan

### Phase 1: Database Migration (Day 1)

**File:** `migrations/009_dual_quantity_tracking.sql`

```sql
-- ============================================================
-- Migration 009: Dual Quantity Tracking for Meal Foods
-- ============================================================
-- Purpose: Add separate columns for serving and gram quantities
--          to enable accurate bidirectional quantity tracking
-- ============================================================

BEGIN;

-- Step 1: Add new columns
ALTER TABLE meal_foods 
ADD COLUMN IF NOT EXISTS serving_quantity NUMERIC(10,3),
ADD COLUMN IF NOT EXISTS serving_unit VARCHAR(50),
ADD COLUMN IF NOT EXISTS gram_quantity NUMERIC(10,3),
ADD COLUMN IF NOT EXISTS last_edited_field VARCHAR(20) DEFAULT 'grams'
    CHECK (last_edited_field IN ('serving', 'grams'));

-- Step 2: Create temporary function for data migration
CREATE OR REPLACE FUNCTION migrate_meal_food_quantities()
RETURNS void AS $$
DECLARE
    food_record RECORD;
    food_info RECORD;
    calculated_grams NUMERIC;
    calculated_servings NUMERIC;
BEGIN
    FOR food_record IN 
        SELECT mf.id, mf.food_id, mf.quantity, mf.unit
        FROM meal_foods mf
        WHERE mf.gram_quantity IS NULL
    LOOP
        -- Get food serving info
        SELECT serving_size, household_serving_size, household_serving_unit
        INTO food_info
        FROM foods_enhanced
        WHERE id = food_record.food_id;
        
        -- Calculate gram quantity
        IF food_record.unit = 'g' THEN
            calculated_grams := food_record.quantity;
            
            -- Calculate serving quantity from grams
            IF food_info.household_serving_size IS NOT NULL 
               AND food_info.household_serving_size::numeric > 0 THEN
                calculated_servings := calculated_grams / food_info.household_serving_size::numeric;
            ELSIF food_info.serving_size > 0 THEN
                calculated_servings := calculated_grams / food_info.serving_size;
            ELSE
                calculated_servings := calculated_grams / 100.0;
            END IF;
            
            UPDATE meal_foods
            SET gram_quantity = calculated_grams,
                serving_quantity = calculated_servings,
                serving_unit = food_info.household_serving_unit,
                last_edited_field = 'grams'
            WHERE id = food_record.id;
            
        ELSIF food_record.unit = food_info.household_serving_unit THEN
            -- User logged in household servings (e.g., "2 slices")
            calculated_servings := food_record.quantity;
            
            IF food_info.household_serving_size IS NOT NULL 
               AND food_info.household_serving_size::numeric > 0 THEN
                calculated_grams := calculated_servings * food_info.household_serving_size::numeric;
            ELSE
                calculated_grams := calculated_servings * COALESCE(food_info.serving_size, 100);
            END IF;
            
            UPDATE meal_foods
            SET gram_quantity = calculated_grams,
                serving_quantity = calculated_servings,
                serving_unit = food_info.household_serving_unit,
                last_edited_field = 'serving'
            WHERE id = food_record.id;
            
        ELSE
            -- Generic "serving" or other unit
            calculated_servings := food_record.quantity;
            calculated_grams := calculated_servings * COALESCE(food_info.serving_size, 100);
            
            UPDATE meal_foods
            SET gram_quantity = calculated_grams,
                serving_quantity = calculated_servings,
                serving_unit = COALESCE(food_info.household_serving_unit, 'serving'),
                last_edited_field = 'serving'
            WHERE id = food_record.id;
        END IF;
    END LOOP;
END;
$$ LANGUAGE plpgsql;

-- Step 3: Run migration
SELECT migrate_meal_food_quantities();

-- Step 4: Verify migration
DO $$
DECLARE
    null_count INTEGER;
BEGIN
    SELECT COUNT(*) INTO null_count
    FROM meal_foods
    WHERE gram_quantity IS NULL;
    
    IF null_count > 0 THEN
        RAISE EXCEPTION 'Migration incomplete: % rows have NULL gram_quantity', null_count;
    END IF;
    
    RAISE NOTICE 'Migration successful: All meal_foods have quantity data';
END $$;

-- Step 5: Add NOT NULL constraints (after data is migrated)
ALTER TABLE meal_foods 
ALTER COLUMN gram_quantity SET NOT NULL,
ALTER COLUMN last_edited_field SET NOT NULL;

-- Step 6: Add indices for performance
CREATE INDEX IF NOT EXISTS idx_meal_foods_gram_quantity 
    ON meal_foods(gram_quantity);

-- Step 7: Drop temporary function
DROP FUNCTION migrate_meal_food_quantities();

-- Step 8: Add comment
COMMENT ON COLUMN meal_foods.serving_quantity IS 
    'Quantity in household serving units (e.g., 2.5 slices)';
COMMENT ON COLUMN meal_foods.serving_unit IS 
    'Household serving unit name (e.g., slice, medium, scoop) or NULL for generic servings';
COMMENT ON COLUMN meal_foods.gram_quantity IS 
    'Quantity in grams (always stored, used for all nutrition calculations)';
COMMENT ON COLUMN meal_foods.last_edited_field IS 
    'Tracks which field user last edited: serving or grams';

COMMIT;
```

**Migration Testing:**
```sql
-- Test script to verify migration
SELECT 
    mf.id,
    f.name,
    f.household_serving_unit,
    f.household_serving_size,
    f.serving_size,
    mf.quantity AS old_quantity,
    mf.unit AS old_unit,
    mf.serving_quantity,
    mf.serving_unit,
    mf.gram_quantity,
    mf.last_edited_field
FROM meal_foods mf
JOIN foods_enhanced f ON f.id = mf.food_id
LIMIT 20;
```

---

### Phase 2: Backend API Updates (Day 2)

#### File: `app/models/food_quantity.py` (NEW)

```python
"""
Food Quantity Models - Dual Quantity Tracking
"""
from decimal import Decimal
from typing import Optional, Literal
from pydantic import BaseModel, Field, validator


class FoodQuantity(BaseModel):
    """
    Represents both serving and gram quantities for a food item.
    
    This model ensures bidirectional tracking - we always know both
    how many servings AND how many grams the user has logged.
    """
    serving_quantity: Decimal = Field(..., gt=0, description="Number of servings")
    serving_unit: Optional[str] = Field(None, description="Serving unit name (slice, medium, etc.)")
    gram_quantity: Decimal = Field(..., gt=0, description="Quantity in grams")
    last_edited_field: Literal['serving', 'grams'] = Field(
        'grams',
        description="Which field user last edited"
    )
    
    @validator('serving_quantity', 'gram_quantity')
    def validate_positive(cls, v):
        if v <= 0:
            raise ValueError("Quantity must be positive")
        if v > 100000:  # Sanity check: 100kg max
            raise ValueError("Quantity exceeds reasonable limits")
        return v
    
    class Config:
        json_schema_extra = {
            "example": {
                "serving_quantity": 2.5,
                "serving_unit": "slice",
                "gram_quantity": 70,
                "last_edited_field": "serving"
            }
        }


class FoodQuantityRequest(BaseModel):
    """Request model for updating food quantity."""
    input_quantity: Decimal = Field(..., gt=0)
    input_field: Literal['serving', 'grams']
```

#### File: `app/services/quantity_converter.py` (NEW)

```python
"""
Food Quantity Conversion Logic

This module handles all conversions between servings and grams.
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class FoodQuantityConverter:
    """
    Handles bidirectional conversion between servings and grams.
    
    Key Principles:
    1. Gram quantity is the source of truth for nutrition calculations
    2. Conversions use household serving size when available
    3. All conversions are reversible without data loss
    4. Edge cases are handled gracefully with sensible fallbacks
    """
    
    @staticmethod
    def calculate_quantities(
        food_data: Dict[str, Any],
        input_quantity: Decimal,
        input_field: str
    ) -> Dict[str, Any]:
        """
        Calculate both serving and gram quantities from user input.
        
        Args:
            food_data: Food information from foods_enhanced table
            input_quantity: The quantity entered by user
            input_field: 'serving' or 'grams' - which field user edited
            
        Returns:
            Dict with serving_quantity, serving_unit, gram_quantity, last_edited_field
        """
        # Extract food serving information
        serving_size = Decimal(str(food_data.get('serving_size', 100)))
        household_serving_size = food_data.get('household_serving_size')
        household_serving_unit = food_data.get('household_serving_unit')
        
        # Parse household serving size (may be string like "1" or "0.5")
        household_grams_per_serving = None
        if household_serving_size:
            try:
                household_grams_per_serving = Decimal(str(household_serving_size))
            except (ValueError, TypeError):
                logger.warning(f"Invalid household_serving_size: {household_serving_size}")
        
        # Determine grams per serving (priority: household > standard)
        grams_per_serving = household_grams_per_serving if household_grams_per_serving else serving_size
        
        # Ensure we have a valid serving size
        if grams_per_serving <= 0:
            logger.warning(f"Invalid serving size: {grams_per_serving}, using 100g default")
            grams_per_serving = Decimal('100')
        
        # Calculate based on input field
        if input_field == 'serving':
            # User edited servings → calculate grams
            serving_quantity = input_quantity
            gram_quantity = serving_quantity * grams_per_serving
            
        else:  # input_field == 'grams'
            # User edited grams → calculate servings
            gram_quantity = input_quantity
            serving_quantity = gram_quantity / grams_per_serving
        
        # Round to reasonable precision
        serving_quantity = serving_quantity.quantize(
            Decimal('0.001'), 
            rounding=ROUND_HALF_UP
        )
        gram_quantity = gram_quantity.quantize(
            Decimal('0.1'), 
            rounding=ROUND_HALF_UP
        )
        
        return {
            'serving_quantity': float(serving_quantity),
            'serving_unit': household_serving_unit or 'serving',
            'gram_quantity': float(gram_quantity),
            'last_edited_field': input_field
        }
    
    @staticmethod
    def calculate_nutrition(
        food_data: Dict[str, Any],
        gram_quantity: Decimal
    ) -> Dict[str, float]:
        """
        Calculate nutrition values based on gram quantity.
        
        CRITICAL: Nutrition is ALWAYS calculated from grams for consistency.
        
        Args:
            food_data: Food information from foods_enhanced table
            gram_quantity: Quantity in grams
            
        Returns:
            Dict with nutrition values (calories, protein_g, etc.)
        """
        serving_size = Decimal(str(food_data.get('serving_size', 100)))
        
        # Calculate multiplier
        multiplier = gram_quantity / serving_size
        
        # Calculate each nutrient
        return {
            'calories': float((Decimal(str(food_data.get('calories', 0))) * multiplier).quantize(Decimal('0.1'))),
            'protein_g': float((Decimal(str(food_data.get('protein_g', 0))) * multiplier).quantize(Decimal('0.1'))),
            'carbs_g': float((Decimal(str(food_data.get('total_carbs_g', 0))) * multiplier).quantize(Decimal('0.1'))),
            'fat_g': float((Decimal(str(food_data.get('total_fat_g', 0))) * multiplier).quantize(Decimal('0.1'))),
            'fiber_g': float((Decimal(str(food_data.get('dietary_fiber_g', 0))) * multiplier).quantize(Decimal('0.1'))),
            'sugar_g': float((Decimal(str(food_data.get('total_sugars_g', 0))) * multiplier).quantize(Decimal('0.1'))),
            'sodium_mg': float((Decimal(str(food_data.get('sodium_mg', 0))) * multiplier).quantize(Decimal('0.1'))),
        }
```

#### Updates to `meal_logging_service_v2.py`

```python
# Add imports
from app.services.quantity_converter import FoodQuantityConverter
from app.models.food_quantity import FoodQuantity, FoodQuantityRequest

# Update create_meal method
async def create_meal(
    self,
    user_id: str,
    category: str,
    logged_at: str,
    food_items: List[Dict[str, Any]],
    name: Optional[str] = None,
    notes: Optional[str] = None
) -> Dict[str, Any]:
    """Create meal with dual quantity tracking."""
    
    # ... existing validation ...
    
    # Process each food item
    meal_foods_data = []
    for item in food_items:
        food_id = item.get('food_id')
        input_quantity = Decimal(str(item['quantity']))
        input_field = item.get('input_field', 'grams')  # Default to grams for backward compatibility
        
        # Fetch food data
        food_response = self.supabase.table('foods_enhanced') \
            .select('*') \
            .eq('id', food_id) \
            .single() \
            .execute()
        
        food_data = food_response.data
        
        # Calculate both quantities
        quantities = FoodQuantityConverter.calculate_quantities(
            food_data=food_data,
            input_quantity=input_quantity,
            input_field=input_field
        )
        
        # Calculate nutrition from gram quantity
        nutrition = FoodQuantityConverter.calculate_nutrition(
            food_data=food_data,
            gram_quantity=Decimal(str(quantities['gram_quantity']))
        )
        
        # Build meal_food record
        meal_food = {
            'food_id': food_id,
            'serving_quantity': quantities['serving_quantity'],
            'serving_unit': quantities['serving_unit'],
            'gram_quantity': quantities['gram_quantity'],
            'last_edited_field': quantities['last_edited_field'],
            'calories': nutrition['calories'],
            'protein_g': nutrition['protein_g'],
            'carbs_g': nutrition['carbs_g'],
            'fat_g': nutrition['fat_g'],
            'fiber_g': nutrition['fiber_g'],
            'sugar_g': nutrition['sugar_g'],
            'sodium_mg': nutrition['sodium_mg'],
        }
        
        meal_foods_data.append(meal_food)
    
    # ... rest of method ...
```

---

### Phase 3: Frontend Implementation (Day 3)

#### File: `lib/utils/food-quantity-converter.ts` (NEW)

```typescript
/**
 * Food Quantity Converter - Frontend
 * 
 * Handles bidirectional conversion between servings and grams.
 * Mirrors backend logic for consistent UX.
 */

export interface FoodEnhanced {
  id: string;
  name: string;
  serving_size: number;
  serving_unit: string;
  household_serving_size: string | null;
  household_serving_unit: string | null;
  calories: number;
  protein_g: number;
  total_carbs_g: number;
  total_fat_g: number;
  dietary_fiber_g: number;
  total_sugars_g: number;
  sodium_mg: number;
}

export interface FoodQuantity {
  servingQuantity: number;
  servingUnit: string | null;
  gramQuantity: number;
  lastEditedField: 'serving' | 'grams';
}

export interface NutritionValues {
  calories: number;
  protein_g: number;
  carbs_g: number;
  fat_g: number;
  fiber_g: number;
  sugar_g: number;
  sodium_mg: number;
}

export class FoodQuantityConverter {
  /**
   * Calculate both quantities from user input
   */
  static calculateQuantities(
    food: FoodEnhanced,
    inputQuantity: number,
    inputField: 'serving' | 'grams'
  ): FoodQuantity {
    // Get grams per serving (priority: household > standard)
    const householdGrams = food.household_serving_size 
      ? parseFloat(food.household_serving_size) 
      : null;
    
    const gramsPerServing = householdGrams && householdGrams > 0 
      ? householdGrams 
      : (food.serving_size || 100);
    
    let servingQuantity: number;
    let gramQuantity: number;
    
    if (inputField === 'serving') {
      // User edited servings → calculate grams
      servingQuantity = inputQuantity;
      gramQuantity = servingQuantity * gramsPerServing;
    } else {
      // User edited grams → calculate servings
      gramQuantity = inputQuantity;
      servingQuantity = gramQuantity / gramsPerServing;
    }
    
    // Round to reasonable precision
    servingQuantity = Math.round(servingQuantity * 1000) / 1000;
    gramQuantity = Math.round(gramQuantity * 10) / 10;
    
    return {
      servingQuantity,
      servingUnit: food.household_serving_unit || 'serving',
      gramQuantity,
      lastEditedField: inputField
    };
  }
  
  /**
   * Calculate nutrition from gram quantity
   */
  static calculateNutrition(
    food: FoodEnhanced,
    gramQuantity: number
  ): NutritionValues {
    const servingSize = food.serving_size || 100;
    const multiplier = gramQuantity / servingSize;
    
    const round = (val: number) => Math.round(val * 10) / 10;
    
    return {
      calories: round((food.calories || 0) * multiplier),
      protein_g: round((food.protein_g || 0) * multiplier),
      carbs_g: round((food.total_carbs_g || 0) * multiplier),
      fat_g: round((food.total_fat_g || 0) * multiplier),
      fiber_g: round((food.dietary_fiber_g || 0) * multiplier),
      sugar_g: round((food.total_sugars_g || 0) * multiplier),
      sodium_mg: round((food.sodium_mg || 0) * multiplier),
    };
  }
  
  /**
   * Format serving display with proper pluralization
   */
  static formatServingDisplay(quantity: number, unit: string | null): string {
    if (!unit) return `${quantity} serving${quantity !== 1 ? 's' : ''}`;
    
    const pluralMap: Record<string, string> = {
      'slice': 'slices',
      'piece': 'pieces',
      'scoop': 'scoops',
      'cup': 'cups',
      'medium': 'medium',
      'small': 'small',
      'large': 'large',
    };
    
    const displayUnit = quantity === 1 ? unit : (pluralMap[unit] || `${unit}s`);
    return `${quantity} ${displayUnit}`;
  }
}
```

#### File: `components/nutrition/DualQuantityEditor.tsx` (NEW)

```tsx
'use client'

import React, { useState, useEffect } from 'react'
import { Minus, Plus } from 'lucide-react'
import { FoodQuantityConverter, type FoodEnhanced, type FoodQuantity, type NutritionValues } from '@/lib/utils/food-quantity-converter'

interface DualQuantityEditorProps {
  food: FoodEnhanced
  initialQuantity: FoodQuantity
  onChange: (quantity: FoodQuantity, nutrition: NutritionValues) => void
}

export function DualQuantityEditor({
  food,
  initialQuantity,
  onChange
}: DualQuantityEditorProps) {
  const [quantity, setQuantity] = useState<FoodQuantity>(initialQuantity)
  const [nutrition, setNutrition] = useState<NutritionValues>(
    FoodQuantityConverter.calculateNutrition(food, initialQuantity.gramQuantity)
  )
  
  const hasHouseholdServing = Boolean(food.household_serving_unit)
  
  const handleServingChange = (value: number) => {
    if (value <= 0) return
    
    const newQuantity = FoodQuantityConverter.calculateQuantities(
      food,
      value,
      'serving'
    )
    
    const newNutrition = FoodQuantityConverter.calculateNutrition(
      food,
      newQuantity.gramQuantity
    )
    
    setQuantity(newQuantity)
    setNutrition(newNutrition)
    onChange(newQuantity, newNutrition)
  }
  
  const handleGramChange = (value: number) => {
    if (value <= 0) return
    
    const newQuantity = FoodQuantityConverter.calculateQuantities(
      food,
      value,
      'grams'
    )
    
    const newNutrition = FoodQuantityConverter.calculateNutrition(
      food,
      newQuantity.gramQuantity
    )
    
    setQuantity(newQuantity)
    setNutrition(newNutrition)
    onChange(newQuantity, newNutrition)
  }
  
  return (
    <div className="space-y-4">
      {/* Serving Input - Only show if food has household serving */}
      {hasHouseholdServing && (
        <div className="space-y-2">
          <label className="text-xs text-iron-gray uppercase font-medium block">
            {quantity.servingUnit || 'Servings'}
          </label>
          <div className="flex items-center gap-2">
            <button
              onClick={() => handleServingChange(Math.max(0.25, quantity.servingQuantity - 0.25))}
              className="bg-iron-gray/20 hover:bg-iron-gray/40 px-3 py-2 text-iron-white rounded transition-colors"
              aria-label="Decrease servings"
            >
              <Minus size={16} />
            </button>
            <input
              type="number"
              value={quantity.servingQuantity.toFixed(2)}
              onChange={(e) => handleServingChange(parseFloat(e.target.value) || 0)}
              step="0.25"
              min="0"
              className="flex-1 bg-iron-black border border-iron-gray/50 px-4 py-2 text-iron-white text-center rounded focus:outline-none focus:ring-2 focus:ring-iron-orange text-lg font-medium"
            />
            <button
              onClick={() => handleServingChange(quantity.servingQuantity + 0.25)}
              className="bg-iron-gray/20 hover:bg-iron-gray/40 px-3 py-2 text-iron-white rounded transition-colors"
              aria-label="Increase servings"
            >
              <Plus size={16} />
            </button>
          </div>
        </div>
      )}
      
      {/* Grams Input - Always shown */}
      <div className="space-y-2">
        <label className="text-xs text-iron-gray uppercase font-medium block">
          Grams
        </label>
        <div className="flex items-center gap-2">
          <button
            onClick={() => handleGramChange(Math.max(1, quantity.gramQuantity - 10))}
            className="bg-iron-gray/20 hover:bg-iron-gray/40 px-3 py-2 text-iron-white rounded transition-colors text-sm"
            aria-label="Decrease by 10g"
          >
            -10
          </button>
          <button
            onClick={() => handleGramChange(Math.max(1, quantity.gramQuantity - 1))}
            className="bg-iron-gray/20 hover:bg-iron-gray/40 px-3 py-2 text-iron-white rounded transition-colors"
            aria-label="Decrease by 1g"
          >
            <Minus size={16} />
          </button>
          <input
            type="number"
            value={quantity.gramQuantity.toFixed(1)}
            onChange={(e) => handleGramChange(parseFloat(e.target.value) || 0)}
            step="1"
            min="0"
            className="flex-1 bg-iron-black border border-iron-gray/50 px-4 py-2 text-iron-white text-center rounded focus:outline-none focus:ring-2 focus:ring-iron-orange text-lg font-medium"
          />
          <button
            onClick={() => handleGramChange(quantity.gramQuantity + 1)}
            className="bg-iron-gray/20 hover:bg-iron-gray/40 px-3 py-2 text-iron-white rounded transition-colors"
            aria-label="Increase by 1g"
          >
            <Plus size={16} />
          </button>
          <button
            onClick={() => handleGramChange(quantity.gramQuantity + 10)}
            className="bg-iron-gray/20 hover:bg-iron-gray/40 px-3 py-2 text-iron-white rounded transition-colors text-sm"
            aria-label="Increase by 10g"
          >
            +10
          </button>
        </div>
      </div>
      
      {/* Nutrition Preview */}
      <div className="flex justify-around gap-2 text-xs text-iron-gray bg-iron-gray/5 rounded-md p-3 border border-iron-gray/20">
        <div className="text-center">
          <div className="text-iron-white font-bold text-base">
            {Math.round(nutrition.calories)}
          </div>
          <div className="uppercase">cal</div>
        </div>
        <div className="text-center">
          <div className="text-iron-white font-bold text-base">
            {nutrition.protein_g.toFixed(1)}g
          </div>
          <div className="uppercase">protein</div>
        </div>
        <div className="text-center">
          <div className="text-iron-white font-bold text-base">
            {nutrition.carbs_g.toFixed(1)}g
          </div>
          <div className="uppercase">carbs</div>
        </div>
        <div className="text-center">
          <div className="text-iron-white font-bold text-base">
            {nutrition.fat_g.toFixed(1)}g
          </div>
          <div className="uppercase">fat</div>
        </div>
      </div>
    </div>
  )
}
```

---

### Phase 4: Testing (Day 4)

#### Test Scenarios

**1. Basic Conversions:**
```typescript
// Test: 2 slices bread → 56g
const bread = {
  serving_size: 28,
  household_serving_size: "28",
  household_serving_unit: "slice"
};

const result = FoodQuantityConverter.calculateQuantities(bread, 2, 'serving');
expect(result.gramQuantity).toBe(56);
expect(result.servingQuantity).toBe(2);
```

**2. Bidirectional Updates:**
```typescript
// Test: Change grams → servings update
const result1 = FoodQuantityConverter.calculateQuantities(bread, 70, 'grams');
expect(result1.servingQuantity).toBeCloseTo(2.5);

// Test: Change servings → grams update
const result2 = FoodQuantityConverter.calculateQuantities(bread, 2.5, 'serving');
expect(result2.gramQuantity).toBe(70);
```

**3. Edge Cases:**
```typescript
// Foods without household servings
const chicken = {
  serving_size: 100,
  household_serving_size: null,
  household_serving_unit: null
};

const result = FoodQuantityConverter.calculateQuantities(chicken, 150, 'grams');
expect(result.servingQuantity).toBe(1.5);
```

---

## Deployment Checklist

- [ ] **Day 1: Database**
  - [ ] Backup production database
  - [ ] Test migration on staging
  - [ ] Run migration on production
  - [ ] Verify data integrity

- [ ] **Day 2: Backend**
  - [ ] Deploy backend changes
  - [ ] Test API endpoints
  - [ ] Monitor error rates
  - [ ] Verify conversion accuracy

- [ ] **Day 3: Frontend**
  - [ ] Deploy frontend changes
  - [ ] Test in production
  - [ ] Monitor user feedback
  - [ ] Fix any UI issues

- [ ] **Day 4: Testing**
  - [ ] Run full test suite
  - [ ] Manual testing of common scenarios
  - [ ] Performance testing
  - [ ] User acceptance testing

- [ ] **Day 5: Cleanup**
  - [ ] Remove old conversion logic
  - [ ] Update documentation
  - [ ] Archive migration scripts
  - [ ] Celebrate! 🎉

---

## Success Metrics

1. **Zero conversion errors** in production logs
2. **< 50ms** additional latency for quantity calculations
3. **100% data migration** success (no NULL quantities)
4. **Positive user feedback** on dual input system
5. **No rollbacks needed**

---

## Rollback Plan

If critical issues arise:

1. **Database Rollback:**
   ```sql
   BEGIN;
   -- Old columns are still there
   -- Just revert application to use them
   UPDATE meal_foods SET quantity = gram_quantity, unit = 'g';
   COMMIT;
   ```

2. **Application Rollback:**
   - Deploy previous backend version
   - Deploy previous frontend version
   - System continues working with old logic

3. **Data Safety:**
   - All old columns preserved for 2 weeks
   - Can reconstruct old state if needed
   - Zero data loss risk

---

## Conclusion

This redesign solves the fundamental architectural flaw in the current system by **storing both representations simultaneously**. Users can edit either field, and both stay in perfect sync. Math is always correct. Nutrition calculations are consistent. User experience is intuitive.

**Let's lock the fuck in and build this right.** 💪
