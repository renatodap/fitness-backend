# Database Migrations

This directory contains all SQL migrations for the Wagner Coach backend database.

## Migration Execution Order

**IMPORTANT**: Migrations must be executed in the exact order listed below.

### 1. Schema Migrations (Structural Changes)

#### `000_SCHEMA.sql`
- **Status**: Reference only (do not run)
- **Purpose**: Complete current database schema for documentation
- **Note**: This file represents the current state of the database and should not be executed

#### `001_meal_logging_improvements.sql`
- **Status**: Already applied
- **Purpose**: Initial meal logging improvements
- **Changes**:
  - Timezone handling fixes
  - Food portion defaults (household_serving_size, household_serving_unit)
  - Improved meal_logs structure

#### `002_food_architecture_cleanup.sql`
- **Status**: Ready to apply
- **Purpose**: Separate atomic foods from composite meals
- **Breaking Changes**: YES - removes restaurant fields from foods_enhanced
- **Changes**:
  - Removes `is_restaurant`, `restaurant_name`, `menu_item_id` from foods_enhanced
  - Adds categorization fields: `is_atomic`, `cuisine_type`, `meal_suitability`, `preparation_state`
  - Enhances meal_templates with: `is_public`, `is_restaurant`, `source`, `popularity_score`
  - Creates new tables: `user_favorite_foods`, `food_categories`, `food_pairings`
  - Seeds default food categories (Protein, Carbs, Fats, Vegetables, Fruits, Dairy, Beverages, Supplements)
  - Drops old problematic trigger functions

---

### 2. Data Cleanup (Optional - Fresh Start)

#### `002a_cleanup_seed_data.sql`
- **Status**: Optional (use only for fresh data seeding)
- **Purpose**: Clean up existing seed data before re-seeding
- **WARNING**: Deletes all existing foods and public meal templates
- **Use Case**: Run this ONLY if you want to start fresh with new seed data
- **What it does**:
  - Deletes all public meal templates and their foods
  - Deletes all foods from foods_enhanced
  - Preserves food categories for re-seeding

---

### 3. Seed Data - Atomic Foods (~225 foods)

#### `003a_seed_atomic_foods_proteins_carbs.sql`
- **Purpose**: Seed proteins and carbohydrates (110 foods)
- **Contents**:
  - **Proteins (60)**: Poultry (8), Beef (10), Pork (8), Fish (12), Seafood (6), Eggs & Dairy (8), Plant Protein (8)
  - **Carbohydrates (50)**: Rice (8), Pasta (8), Bread (10), Grains (10), Potatoes (6), Other Carbs (8)

#### `003b_seed_fruits_vegetables_fats.sql`
- **Purpose**: Seed fruits, vegetables, and fats (80 foods)
- **Contents**:
  - **Fruits (25)**: Banana, Apple, Berries, Melons, Tropical fruits, etc.
  - **Vegetables (30)**: Leafy greens, Cruciferous, Colorful veggies, Root vegetables
  - **Fats & Oils (15)**: Olive oil, Coconut oil, Nuts, Seeds
  - **Nut Butters & Spreads (10)**: Peanut butter, Almond butter, Hummus, etc.

#### `003c_seed_beverages_supplements.sql`
- **Purpose**: Seed beverages, supplements, and condiments (35 foods)
- **Contents**:
  - **Beverages (15)**: Water, Coffee, Milk alternatives, Juices
  - **Supplements (8)**: Protein powders, Creatine, BCAAs
  - **Condiments (12)**: Soy sauce, Hot sauce, Vinegars, Honey, etc.

---

### 4. Seed Data - Meal Templates (~30 templates)

#### `004a_seed_meal_templates_community.sql`
- **Purpose**: Seed community meal templates and initial restaurant templates (15 templates)
- **Contents**:
  - **Community Templates (10)**: Protein Shake, Chicken & Rice Bowl, Oatmeal Power Bowl, etc.
  - **Restaurant Templates (5)**: Chipotle (3), Subway (2)

#### `004b_seed_meal_templates_restaurants.sql`
- **Purpose**: Seed additional restaurant meal templates (15 templates)
- **Contents**:
  - **Starbucks (5)**: Egg White Bites, Protein Box, Oatmeal, Turkey Sandwich, Chicken Wrap
  - **Panera (5)**: Mediterranean Bowl, Greek Salad, Turkey BLT, Chicken Soup, Breakfast Bowl
  - **Sweetgreen (5)**: Harvest Bowl, Kale Caesar, Fish Taco Bowl, Shroomami, Guacamole Greens

---

## Execution Instructions

### Fresh Database Setup (First Time)

```bash
# Run migrations in order
psql -U postgres -d wagner_coach -f 000_SCHEMA.sql  # Skip if already done
psql -U postgres -d wagner_coach -f 001_meal_logging_improvements.sql
psql -U postgres -d wagner_coach -f 002_food_architecture_cleanup.sql

# Seed atomic foods
psql -U postgres -d wagner_coach -f 003a_seed_atomic_foods_proteins_carbs.sql
psql -U postgres -d wagner_coach -f 003b_seed_fruits_vegetables_fats.sql
psql -U postgres -d wagner_coach -f 003c_seed_beverages_supplements.sql

# Seed meal templates
psql -U postgres -d wagner_coach -f 004a_seed_meal_templates_community.sql
psql -U postgres -d wagner_coach -f 004b_seed_meal_templates_restaurants.sql
```

### Re-seed Data Only (Existing Database)

```bash
# Clean up existing seed data
psql -U postgres -d wagner_coach -f 002a_cleanup_seed_data.sql

# Re-seed atomic foods
psql -U postgres -d wagner_coach -f 003a_seed_atomic_foods_proteins_carbs.sql
psql -U postgres -d wagner_coach -f 003b_seed_fruits_vegetables_fats.sql
psql -U postgres -d wagner_coach -f 003c_seed_beverages_supplements.sql

# Re-seed meal templates
psql -U postgres -d wagner_coach -f 004a_seed_meal_templates_community.sql
psql -U postgres -d wagner_coach -f 004b_seed_meal_templates_restaurants.sql
```

---

## Migration Naming Convention

- `000_*.sql` - Schema reference (do not run)
- `001_*.sql` - Initial migrations (already applied)
- `002_*.sql` - Architectural changes (schema modifications)
- `002a_*.sql` - Optional data cleanup scripts
- `003[a-z]_*.sql` - Seed data for atomic foods
- `004[a-z]_*.sql` - Seed data for meal templates

---

## Data Summary

After running all seed scripts, you will have:

- **~225 atomic foods** (single ingredients only)
- **~30 public meal templates** (composite meals)
- **8 top-level food categories** (Protein, Carbs, Fats, Vegetables, Fruits, Dairy, Beverages, Supplements)
- **~20 subcategories** (Poultry, Beef, Rice, Pasta, etc.)
- **5 restaurant chains** represented (Chipotle, Subway, Starbucks, Panera, Sweetgreen)

---

## Architecture Principles

### Atomic vs Composite

- **Atomic Foods** (`foods_enhanced` with `is_atomic = true`):
  - Single ingredients: Chicken breast, Rice, Broccoli, Banana
  - Simple whole foods or minimally processed items
  - No composite meals or restaurant items

- **Composite Meals** (`meal_templates`):
  - Combinations of atomic foods: "Chicken & Rice Bowl"
  - Restaurant meals: "Chipotle Chicken Bowl"
  - Community templates: "Classic Protein Shake"
  - Can be public (`is_public = true`) or private (`is_public = false`)

### Public vs Private Templates

- **Public Templates** (`is_public = true`, `user_id = NULL`):
  - Available to all users
  - Restaurant meals, community favorites
  - Cannot be edited by users

- **Private Templates** (`is_public = false`, `user_id = <user's uuid>`):
  - User-created meal templates
  - Can be edited/deleted by owner
  - Require valid user_id

---

## Troubleshooting

### Error: Duplicate key violation on meal_templates

**Cause**: Trying to insert templates that already exist

**Solution**: Run `002a_cleanup_seed_data.sql` first to clean existing data

### Error: Column "sort_order" does not exist

**Cause**: Using old seed scripts with wrong column name

**Solution**: Use updated scripts that use `order_index` instead of `sort_order`

### Error: Food category not found

**Cause**: Running seed scripts without food categories

**Solution**: Ensure `002_food_architecture_cleanup.sql` was run first (it seeds categories)

---

## Contributing

When creating new migrations:

1. Use sequential numbering (`005_`, `006_`, etc.)
2. Use descriptive names (`005_add_user_preferences.sql`)
3. Include comments explaining purpose and changes
4. Add verification queries at the end
5. Test on development database first
6. Update this README with migration details

---

## Notes

- All migrations use PostgreSQL syntax
- RLS (Row Level Security) policies are included where needed
- Foreign key constraints ensure data integrity
- Indexes are created for performance
- Verification queries help confirm successful execution
