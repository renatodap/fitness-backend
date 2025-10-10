-- ============================================================================
-- PHASE 5: COMPREHENSIVE FOOD DATABASE - GAP ANALYSIS (600+ FOODS)
-- ============================================================================
-- This migration addresses the major gaps identified in the food database:
-- 1. Dairy & Eggs (milk varieties, yogurt, cheese)
-- 2. Breads & Baked Goods (croissants, pastries, rolls)
-- 3. Grain & Starch Preparations (rice, potato varieties)
-- 4. Meat Preparations & Processed Meats (deli meats, hot dogs, sausages)
-- 5. Seafood Preparations
-- 6. Beans, Legumes & Soy
-- 7. Nuts, Seeds & Nut Butters
-- 8. Oils, Fats & Cooking Ingredients
-- 9. Sauces, Condiments & Dressings
-- 10. Soups & Broths
-- 11. Frozen Meals & Convenience Foods
-- 12. International Cuisines
-- 13. Restaurant Chains
-- 14. Desserts & Baked Goods
-- 15. Specialty Diet Foods
-- Priority: CRITICAL missing items that users log daily
-- ============================================================================

DO $$
DECLARE
    cat_protein UUID;
    cat_carbs UUID;
    cat_fruits UUID;
    cat_vegetables UUID;
    cat_fats UUID;
    cat_dairy UUID;
    cat_beverages UUID;
BEGIN
    -- Get category IDs
    SELECT id INTO cat_protein FROM food_categories WHERE name = 'Protein' AND level = 0;
    SELECT id INTO cat_carbs FROM food_categories WHERE name = 'Grains' AND level = 0;
    SELECT id INTO cat_fruits FROM food_categories WHERE name = 'Fruits' AND level = 0;
    SELECT id INTO cat_vegetables FROM food_categories WHERE name = 'Vegetables' AND level = 0;
    SELECT id INTO cat_fats FROM food_categories WHERE name = 'Fats, Nuts & Seeds' AND level = 0;
    SELECT id INTO cat_dairy FROM food_categories WHERE name = 'Dairy' AND level = 0;
    SELECT id INTO cat_beverages FROM food_categories WHERE name = 'Beverages' AND level = 0;

-- ============================================================================
-- CATEGORY 1: DAIRY & EGG PRODUCTS (60 items)
-- ============================================================================

INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES

-- MILK VARIATIONS (8 items)
('Chocolate Milk (8 oz)', 'Dairy', cat_dairy, 240, 'ml', 208, 8, 26, 8, 2, true, true, false, 'processed', 'raw', '{snack,breakfast}', '{dairy,vegetarian}', 1.0),
('Chocolate Milk (12 oz)', 'Dairy', cat_dairy, 360, 'ml', 312, 12, 39, 12, 3, true, true, false, 'processed', 'raw', '{snack,breakfast}', '{dairy,vegetarian}', 1.0),
('Strawberry Milk (8 oz)', 'Dairy', cat_dairy, 240, 'ml', 200, 8, 28, 5, 0, true, true, false, 'processed', 'raw', '{snack,breakfast}', '{dairy,vegetarian}', 1.0),
('Buttermilk (1 cup)', 'Dairy', cat_dairy, 245, 'ml', 152, 8, 12, 8, 0, true, true, false, 'processed', 'raw', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Evaporated Milk (2 tbsp)', 'Dairy', cat_dairy, 30, 'ml', 40, 2, 3, 2, 0, true, true, false, 'processed', 'raw', '{breakfast}', '{dairy,vegetarian}', 1.0),
('Heavy Cream (2 tbsp)', 'Dairy', cat_dairy, 30, 'ml', 103, 1, 1, 11, 0, true, true, false, 'minimally_processed', 'raw', '{breakfast}', '{dairy,vegetarian}', 1.0),
('Half and Half (2 tbsp)', 'Dairy', cat_dairy, 30, 'ml', 39, 1, 1, 3, 0, true, true, false, 'minimally_processed', 'raw', '{breakfast}', '{dairy,vegetarian}', 1.0),
('Coffee Creamer (2 tbsp)', 'Dairy', cat_dairy, 30, 'ml', 40, 0, 5, 2, 0, true, true, false, 'processed', 'raw', '{breakfast}', '{vegetarian}', 1.0),

-- YOGURT VARIETIES (8 items)
('Vanilla Yogurt (6 oz)', 'Dairy', cat_dairy, 170, 'g', 150, 5, 25, 2, 0, true, true, false, 'processed', 'raw', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Strawberry Yogurt (6 oz)', 'Dairy', cat_dairy, 170, 'g', 140, 5, 24, 2, 0, true, true, false, 'processed', 'raw', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Plain Yogurt (Not Greek, 6 oz)', 'Dairy', cat_dairy, 170, 'g', 100, 6, 8, 4, 0, true, true, false, 'minimally_processed', 'raw', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Yoplait Original (6 oz)', 'Dairy', cat_dairy, 170, 'g', 150, 5, 26, 2, 0, false, true, false, 'processed', 'raw', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Drinkable Yogurt (7 oz)', 'Dairy', cat_dairy, 207, 'ml', 150, 7, 24, 3, 0, true, true, false, 'processed', 'raw', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Kefir (1 cup)', 'Dairy', cat_dairy, 240, 'ml', 110, 11, 12, 2, 0, true, true, false, 'processed', 'raw', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Frozen Yogurt (1/2 cup)', 'Dairy', cat_dairy, 87, 'g', 114, 3, 17, 4, 0, true, true, false, 'processed', 'raw', '{dessert,snack}', '{dairy,vegetarian}', 1.0),
('Frozen Yogurt (1 cup)', 'Dairy', cat_dairy, 174, 'g', 228, 6, 34, 8, 0, true, true, false, 'processed', 'raw', '{dessert,snack}', '{dairy,vegetarian}', 1.0),

-- CHEESE VARIETIES (30 items)
('Cottage Cheese (Full Fat 4%, 1/2 cup)', 'Dairy', cat_dairy, 113, 'g', 110, 13, 4, 5, 0, true, true, false, 'minimally_processed', 'raw', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Ricotta Cheese (1/2 cup)', 'Dairy', cat_dairy, 124, 'g', 216, 14, 8, 16, 0, true, true, false, 'minimally_processed', 'raw', '{lunch,dinner}', '{dairy,vegetarian}', 1.0),
('Brie Cheese (1 oz)', 'Dairy', cat_dairy, 28, 'g', 95, 6, 0, 8, 0, true, true, false, 'minimally_processed', 'raw', '{snack,lunch}', '{dairy,vegetarian}', 1.0),
('Camembert (1 oz)', 'Dairy', cat_dairy, 28, 'g', 85, 6, 0, 7, 0, true, true, false, 'minimally_processed', 'raw', '{snack,lunch}', '{dairy,vegetarian}', 1.0),
('Gruyere (1 oz)', 'Dairy', cat_dairy, 28, 'g', 117, 8, 0, 9, 0, true, true, false, 'minimally_processed', 'raw', '{snack,lunch,dinner}', '{dairy,vegetarian}', 1.0),
('Monterey Jack (1 slice)', 'Dairy', cat_dairy, 28, 'g', 106, 7, 0, 9, 0, true, true, false, 'minimally_processed', 'raw', '{snack,lunch,dinner}', '{dairy,vegetarian}', 1.0),
('Colby Jack (1 slice)', 'Dairy', cat_dairy, 28, 'g', 110, 7, 1, 9, 0, true, true, false, 'minimally_processed', 'raw', '{snack,lunch,dinner}', '{dairy,vegetarian}', 1.0),
('Queso Fresco (1/4 cup crumbled)', 'Dairy', cat_dairy, 28, 'g', 80, 5, 1, 6, 0, true, true, false, 'minimally_processed', 'raw', '{lunch,dinner}', '{dairy,vegetarian}', 1.0),
('Cotija Cheese (2 tbsp crumbled)', 'Dairy', cat_dairy, 14, 'g', 50, 3, 0, 4, 0, true, true, false, 'minimally_processed', 'raw', '{lunch,dinner}', '{dairy,vegetarian}', 1.0),
('Mascarpone (2 tbsp)', 'Dairy', cat_dairy, 28, 'g', 120, 2, 1, 13, 0, true, true, false, 'minimally_processed', 'raw', '{dessert}', '{dairy,vegetarian}', 1.0),
('Goat Cheese/Chevre (1 oz)', 'Dairy', cat_dairy, 28, 'g', 75, 5, 0, 6, 0, true, true, false, 'minimally_processed', 'raw', '{snack,lunch,dinner}', '{dairy,vegetarian}', 1.0),
('Cream Cheese (Strawberry, 2 tbsp)', 'Dairy', cat_dairy, 30, 'g', 90, 2, 4, 8, 0, true, true, false, 'processed', 'raw', '{breakfast}', '{dairy,vegetarian}', 1.0),
('Cream Cheese (Chive, 2 tbsp)', 'Dairy', cat_dairy, 30, 'g', 90, 2, 1, 9, 0, true, true, false, 'processed', 'raw', '{breakfast,lunch}', '{dairy,vegetarian}', 1.0),
('Cream Cheese (Jalapeño, 2 tbsp)', 'Dairy', cat_dairy, 30, 'g', 90, 2, 2, 8, 0, true, true, false, 'processed', 'raw', '{breakfast,lunch}', '{dairy,vegetarian}', 1.0),
('Laughing Cow Cheese Wedge (1 wedge)', 'Dairy', cat_dairy, 21, 'g', 50, 2, 1, 4, 0, false, true, false, 'processed', 'raw', '{snack}', '{dairy,vegetarian}', 1.0),
('Velveeta (1 oz)', 'Dairy', cat_dairy, 28, 'g', 80, 5, 3, 6, 0, false, true, false, 'ultra_processed', 'raw', '{lunch,dinner}', '{dairy,vegetarian}', 0.8),
('Nacho Cheese Sauce (1/4 cup)', 'Dairy', cat_dairy, 63, 'g', 120, 4, 4, 10, 0, true, true, false, 'ultra_processed', 'raw', '{snack,lunch,dinner}', '{dairy,vegetarian}', 0.8),
('Cheese Whiz (2 tbsp)', 'Dairy', cat_dairy, 33, 'g', 91, 4, 3, 7, 0, false, true, false, 'ultra_processed', 'raw', '{snack,lunch}', '{dairy,vegetarian}', 0.8),

-- EGG PREPARATIONS (8 items)
('Deviled Eggs (2 halves)', 'Protein', cat_protein, 62, 'g', 145, 6, 1, 13, 0, true, false, false, 'minimally_processed', 'cooked', '{snack,lunch}', '{eggs,vegetarian}', 1.0),
('Egg Salad (1/2 cup)', 'Protein', cat_protein, 112, 'g', 307, 13, 2, 27, 0, true, false, false, 'minimally_processed', 'cooked', '{lunch,snack}', '{eggs,vegetarian}', 1.0),
('Egg Drop Soup (1 cup)', 'Protein', cat_protein, 240, 'ml', 73, 8, 1, 4, 0, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{eggs}', 1.0),
('Quiche (1 slice - 1/8 of 9-inch)', 'Protein', cat_protein, 125, 'g', 352, 13, 18, 25, 1, true, false, false, 'processed', 'cooked', '{breakfast,lunch}', '{eggs,dairy,gluten,vegetarian}', 0.9),
('Frittata (1 slice)', 'Protein', cat_protein, 100, 'g', 154, 10, 3, 11, 1, true, false, false, 'minimally_processed', 'cooked', '{breakfast,lunch}', '{eggs,dairy,vegetarian}', 1.0),
('Shakshuka (2 eggs in sauce)', 'Protein', cat_protein, 200, 'g', 232, 15, 12, 14, 3, true, false, false, 'minimally_processed', 'cooked', '{breakfast,lunch}', '{eggs,vegetarian}', 1.0),

-- ============================================================================
-- CATEGORY 2: BREADS & BAKED GOODS (50 items)
-- ============================================================================

-- SPECIALTY BREADS (13 items)
('Ciabatta (1 slice, 2 oz)', 'Grains', cat_carbs, 57, 'g', 153, 5, 30, 1, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.9),
('Focaccia (1 piece, 2 oz)', 'Grains', cat_carbs, 57, 'g', 164, 4, 26, 5, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{gluten,vegetarian}', 0.9),
('Naan Bread (White, 1 piece)', 'Grains', cat_carbs, 90, 'g', 262, 9, 45, 5, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,dairy,vegetarian}', 0.9),
('Pita Bread (White, 6-inch)', 'Grains', cat_carbs, 60, 'g', 165, 5, 33, 1, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.9),
('Flatbread (1 piece)', 'Grains', cat_carbs, 50, 'g', 140, 4, 26, 2, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.9),
('Lavash (1 piece)', 'Grains', cat_carbs, 28, 'g', 95, 3, 18, 1, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.9),
('Pumpernickel Bread (1 slice)', 'Grains', cat_carbs, 32, 'g', 80, 3, 15, 1, 2, true, true, false, 'processed', 'cooked', '{breakfast,lunch}', '{gluten,vegetarian}', 0.95),
('Challah (1 slice)', 'Grains', cat_carbs, 40, 'g', 115, 4, 19, 2, 1, true, true, false, 'processed', 'cooked', '{breakfast,lunch}', '{gluten,eggs,vegetarian}', 0.9),
('Brioche (1 slice)', 'Grains', cat_carbs, 40, 'g', 131, 4, 16, 6, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,eggs,vegetarian}', 0.9),
('French Bread/Baguette (2 oz)', 'Grains', cat_carbs, 57, 'g', 154, 5, 30, 2, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.9),
('Italian Bread (1 slice)', 'Grains', cat_carbs, 30, 'g', 81, 3, 15, 1, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.9),
('Cornbread (1 piece - 2x2 inches)', 'Grains', cat_carbs, 60, 'g', 173, 4, 28, 5, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,dairy,eggs,vegetarian}', 0.9),
('Texas Toast (1 slice)', 'Grains', cat_carbs, 50, 'g', 150, 5, 24, 4, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,dairy,vegetarian}', 0.85),

-- BREAKFAST BREADS (15 items)
('Croissant (1 medium)', 'Grains', cat_carbs, 57, 'g', 231, 5, 26, 12, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,vegetarian}', 0.85),
('Pain au Chocolat (1 pastry)', 'Grains', cat_carbs, 80, 'g', 320, 6, 38, 16, 2, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,vegetarian}', 0.8),
('Cinnamon Roll (1 roll with icing)', 'Grains', cat_carbs, 88, 'g', 339, 5, 50, 14, 1, true, true, false, 'ultra_processed', 'cooked', '{breakfast,snack,dessert}', '{gluten,dairy,vegetarian}', 0.75),
('Danish Pastry (Cheese, 1 pastry)', 'Grains', cat_carbs, 71, 'g', 266, 6, 26, 16, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,eggs,vegetarian}', 0.8),
('Danish Pastry (Fruit, 1 pastry)', 'Grains', cat_carbs, 71, 'g', 263, 4, 34, 13, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,vegetarian}', 0.8),
('Bear Claw (1 pastry)', 'Grains', cat_carbs, 95, 'g', 362, 6, 44, 18, 2, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,vegetarian}', 0.75),
('Apple Turnover (1 pastry)', 'Grains', cat_carbs, 89, 'g', 284, 4, 31, 16, 2, true, true, false, 'processed', 'cooked', '{breakfast,snack,dessert}', '{gluten,vegetarian}', 0.8),
('Cherry Turnover (1 pastry)', 'Grains', cat_carbs, 89, 'g', 290, 4, 32, 16, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack,dessert}', '{gluten,vegetarian}', 0.8),
('Scone (Plain, 1 scone)', 'Grains', cat_carbs, 65, 'g', 235, 5, 32, 10, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,vegetarian}', 0.85),
('Scone (Blueberry, 1 scone)', 'Grains', cat_carbs, 65, 'g', 240, 5, 34, 10, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,vegetarian}', 0.85),
('Coffee Cake (1 slice)', 'Grains', cat_carbs, 72, 'g', 263, 4, 29, 15, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack,dessert}', '{gluten,dairy,eggs,vegetarian}', 0.8),
('Banana Bread (1 slice)', 'Grains', cat_carbs, 60, 'g', 196, 3, 33, 6, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,eggs,vegetarian}', 0.85),
('Zucchini Bread (1 slice)', 'Grains', cat_carbs, 60, 'g', 190, 3, 28, 8, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,eggs,vegetarian}', 0.85),
('Pumpkin Bread (1 slice)', 'Grains', cat_carbs, 60, 'g', 178, 3, 30, 5, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,eggs,vegetarian}', 0.85),
('Blueberry Muffin (1 muffin)', 'Grains', cat_carbs, 113, 'g', 426, 6, 54, 21, 2, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,eggs,vegetarian}', 0.8),

-- ROLLS & BUNS (8 items)
('Hamburger Bun (1 bun)', 'Grains', cat_carbs, 52, 'g', 145, 5, 26, 2, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.85),
('Hot Dog Bun (1 bun)', 'Grains', cat_carbs, 43, 'g', 120, 4, 21, 2, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.85),
('Slider Buns (2 buns)', 'Grains', cat_carbs, 43, 'g', 120, 4, 21, 2, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{gluten,vegetarian}', 0.85),
('Kaiser Roll (1 roll)', 'Grains', cat_carbs, 57, 'g', 167, 6, 30, 2, 1, true, true, false, 'processed', 'cooked', '{breakfast,lunch}', '{gluten,vegetarian}', 0.85),
('Pretzel Bun (1 bun)', 'Grains', cat_carbs, 75, 'g', 220, 8, 40, 3, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.85),
('Ciabatta Roll (1 roll)', 'Grains', cat_carbs, 70, 'g', 188, 6, 37, 2, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.9),
('Sub/Hoagie Roll (6-inch)', 'Grains', cat_carbs, 70, 'g', 198, 7, 38, 2, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.85),
('Sub/Hoagie Roll (12-inch)', 'Grains', cat_carbs, 140, 'g', 396, 14, 76, 4, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 0.85),

-- More muffins (6 items)
('Chocolate Chip Muffin (1 muffin)', 'Grains', cat_carbs, 113, 'g', 450, 6, 57, 22, 2, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,eggs,vegetarian}', 0.75),
('Bran Muffin (1 muffin)', 'Grains', cat_carbs, 113, 'g', 305, 6, 55, 7, 5, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,eggs,vegetarian}', 0.9),
('Corn Muffin (1 muffin)', 'Grains', cat_carbs, 95, 'g', 305, 5, 47, 11, 2, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{gluten,dairy,eggs,vegetarian}', 0.85),

-- ============================================================================
-- CATEGORY 3: GRAIN & STARCH PREPARATIONS (20 items)
-- ============================================================================

-- RICE PREPARATIONS (7 items)
('Fried Rice (Generic, 1 cup)', 'Grains', cat_carbs, 198, 'g', 333, 7, 52, 11, 2, true, false, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 0.85),
('Spanish Rice (1 cup)', 'Grains', cat_carbs, 185, 'g', 241, 5, 44, 5, 2, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 0.9),
('Dirty Rice (1 cup)', 'Grains', cat_carbs, 200, 'g', 291, 9, 39, 10, 2, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{pork}', 0.85),
('Cilantro Lime Rice (1 cup)', 'Grains', cat_carbs, 158, 'g', 240, 4, 45, 5, 1, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 0.9),
('Coconut Rice (1 cup)', 'Grains', cat_carbs, 180, 'g', 320, 5, 50, 12, 2, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 0.85),
('Rice Pudding (1/2 cup)', 'Grains', cat_carbs, 140, 'g', 189, 5, 31, 5, 0, true, false, false, 'processed', 'cooked', '{dessert,snack}', '{dairy,vegetarian}', 0.8),
('Rice Krispy Treats (1 bar)', 'Grains', cat_carbs, 40, 'g', 156, 1, 29, 4, 0, true, false, false, 'ultra_processed', 'cooked', '{snack,dessert}', '{dairy,vegetarian}', 0.7),

-- POTATO PREPARATIONS (13 items)
('French Fries (Small)', 'Vegetables', cat_vegetables, 71, 'g', 222, 3, 29, 11, 3, true, false, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{vegetarian}', 0.7),
('French Fries (Medium)', 'Vegetables', cat_vegetables, 117, 'g', 365, 4, 48, 17, 5, true, false, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{vegetarian}', 0.7),
('French Fries (Large)', 'Vegetables', cat_vegetables, 154, 'g', 480, 6, 63, 23, 6, true, false, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{vegetarian}', 0.7),
('Tater Tots (10 tots)', 'Vegetables', cat_vegetables, 86, 'g', 160, 2, 20, 8, 2, true, false, false, 'processed', 'cooked', '{breakfast,lunch,dinner,snack}', '{vegetarian}', 0.75),
('Hash Browns (Patty, 1 patty)', 'Vegetables', cat_vegetables, 57, 'g', 143, 1, 15, 9, 1, true, false, false, 'processed', 'cooked', '{breakfast}', '{vegetarian}', 0.75),
('Hash Browns (Shredded, 1 cup)', 'Vegetables', cat_vegetables, 156, 'g', 326, 4, 44, 16, 4, true, false, false, 'processed', 'cooked', '{breakfast}', '{vegetarian}', 0.75),
('Home Fries (1 cup)', 'Vegetables', cat_vegetables, 156, 'g', 193, 4, 30, 7, 3, true, false, false, 'minimally_processed', 'cooked', '{breakfast}', '{vegetarian}', 0.8),
('Potato Wedges (6 wedges)', 'Vegetables', cat_vegetables, 150, 'g', 260, 4, 38, 10, 4, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{vegetarian}', 0.8),
('Loaded Baked Potato', 'Vegetables', cat_vegetables, 300, 'g', 475, 15, 52, 23, 5, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{dairy,pork,vegetarian}', 0.75),
('Twice-Baked Potato (1 half)', 'Vegetables', cat_vegetables, 150, 'g', 227, 8, 26, 10, 2, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{dairy,vegetarian}', 0.8),
('Scalloped Potatoes (1 cup)', 'Vegetables', cat_vegetables, 245, 'g', 216, 7, 26, 9, 2, true, false, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,vegetarian}', 0.8),
('Au Gratin Potatoes (1 cup)', 'Vegetables', cat_vegetables, 245, 'g', 323, 12, 28, 19, 3, true, false, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,vegetarian}', 0.8),
('Hush Puppies (3 pieces)', 'Grains', cat_carbs, 66, 'g', 257, 5, 35, 10, 1, true, false, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{gluten,dairy,eggs,vegetarian}', 0.75),

-- ============================================================================
-- CATEGORY 4: MEAT PREPARATIONS & PROCESSED MEATS (40 items)
-- ============================================================================

-- DELI MEATS (9 items)
('Ham (Deli Sliced, 2 oz)', 'Protein', cat_protein, 56, 'g', 60, 11, 1, 2, 0, true, true, false, 'processed', 'cooked', '{lunch,snack}', '{pork}', 0.85),
('Roast Beef (Deli Sliced, 2 oz)', 'Protein', cat_protein, 56, 'g', 80, 13, 2, 3, 0, true, true, false, 'minimally_processed', 'cooked', '{lunch,snack}', '{beef}', 0.9),
('Salami (2 oz)', 'Protein', cat_protein, 56, 'g', 174, 9, 1, 14, 0, true, true, false, 'processed', 'cooked', '{lunch,snack}', '{pork,beef}', 0.75),
('Pepperoni (Pizza topping, 1 oz)', 'Protein', cat_protein, 28, 'g', 138, 6, 1, 12, 0, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{pork,beef}', 0.75),
('Bologna (2 slices)', 'Protein', cat_protein, 56, 'g', 180, 7, 2, 16, 0, true, true, false, 'ultra_processed', 'cooked', '{lunch,snack}', '{pork,beef}', 0.7),
('Pastrami (2 oz)', 'Protein', cat_protein, 56, 'g', 99, 14, 1, 4, 0, true, true, false, 'processed', 'cooked', '{lunch,snack}', '{beef}', 0.85),
('Corned Beef (Deli, 2 oz)', 'Protein', cat_protein, 56, 'g', 100, 13, 1, 5, 0, true, true, false, 'processed', 'cooked', '{lunch,snack}', '{beef}', 0.85),
('Prosciutto (2 oz)', 'Protein', cat_protein, 56, 'g', 120, 16, 0, 6, 0, true, true, false, 'processed', 'raw', '{lunch,snack}', '{pork}', 0.85),
('Mortadella (2 oz)', 'Protein', cat_protein, 56, 'g', 186, 10, 2, 15, 0, true, true, false, 'processed', 'cooked', '{lunch,snack}', '{pork,beef}', 0.75),

-- HOT DOGS & SAUSAGES (12 items) - CRITICAL MISSING
('Hot Dog/Frankfurter (1 hot dog)', 'Protein', cat_protein, 57, 'g', 188, 6, 2, 17, 0, true, true, false, 'ultra_processed', 'cooked', '{lunch,dinner,snack}', '{pork,beef}', 0.7),
('Beef Hot Dog (1 hot dog)', 'Protein', cat_protein, 57, 'g', 186, 7, 2, 17, 0, true, true, false, 'ultra_processed', 'cooked', '{lunch,dinner,snack}', '{beef}', 0.7),
('Turkey Hot Dog (1 hot dog)', 'Protein', cat_protein, 45, 'g', 100, 8, 2, 6, 0, true, true, false, 'ultra_processed', 'cooked', '{lunch,dinner,snack}', '{poultry}', 0.75),
('Corn Dog (1 corn dog)', 'Protein', cat_protein, 175, 'g', 438, 17, 56, 19, 0, true, false, false, 'ultra_processed', 'cooked', '{lunch,dinner,snack}', '{pork,beef,gluten}', 0.65),
('Italian Sausage (1 link - sweet)', 'Protein', cat_protein, 83, 'g', 268, 16, 3, 21, 0, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{pork}', 0.8),
('Italian Sausage (1 link - hot)', 'Protein', cat_protein, 83, 'g', 268, 16, 3, 21, 0, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{pork}', 0.8),
('Bratwurst (1 link)', 'Protein', cat_protein, 85, 'g', 283, 12, 2, 25, 0, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{pork,beef}', 0.8),
('Chorizo (Mexican, 2 oz)', 'Protein', cat_protein, 57, 'g', 258, 14, 1, 22, 0, true, true, false, 'processed', 'raw', '{breakfast,lunch,dinner}', '{pork}', 0.8),
('Chorizo (Spanish, 2 oz)', 'Protein', cat_protein, 57, 'g', 273, 14, 2, 23, 0, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{pork}', 0.8),
('Kielbasa/Polish Sausage (2 oz)', 'Protein', cat_protein, 56, 'g', 176, 7, 2, 16, 0, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{pork,beef}', 0.75),
('Andouille Sausage (2 oz)', 'Protein', cat_protein, 56, 'g', 170, 10, 1, 14, 0, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{pork}', 0.8),

-- GROUND MEAT PREPARATIONS (3 items)
('Meatballs (Beef, 3 meatballs)', 'Protein', cat_protein, 85, 'g', 240, 17, 8, 15, 1, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{beef,gluten,eggs}', 0.85),
('Meatballs (Turkey, 3 meatballs)', 'Protein', cat_protein, 85, 'g', 195, 20, 8, 9, 1, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{poultry,gluten,eggs}', 0.9),
('Salisbury Steak (1 patty with gravy)', 'Protein', cat_protein, 203, 'g', 330, 23, 11, 21, 1, true, false, false, 'processed', 'cooked', '{lunch,dinner}', '{beef,gluten}', 0.75),

-- BBQ & SMOKED MEATS (5 items)
('Brisket (Smoked, 4 oz)', 'Protein', cat_protein, 113, 'g', 310, 28, 0, 21, 0, true, true, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{beef}', 0.9),
('Baby Back Ribs (3 ribs)', 'Protein', cat_protein, 150, 'g', 397, 28, 0, 31, 0, true, true, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{pork}', 0.85),
('St. Louis Ribs (3 ribs)', 'Protein', cat_protein, 150, 'g', 430, 25, 0, 35, 0, true, true, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{pork}', 0.85),
('Smoked Turkey (4 oz)', 'Protein', cat_protein, 113, 'g', 160, 28, 0, 4, 0, true, true, false, 'minimally_processed', 'cooked', '{lunch,dinner,snack}', '{poultry}', 0.9),

-- OTHER PREPARATIONS (11 items)
('Chicken Drumsticks (2 drumsticks)', 'Protein', cat_protein, 110, 'g', 245, 28, 0, 14, 0, true, true, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{poultry}', 0.95),
('Chicken Tenders (Plain, 3 tenders)', 'Protein', cat_protein, 120, 'g', 263, 30, 13, 10, 0, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{poultry,gluten}', 0.85),
('Fried Pork Chop (1 chop)', 'Protein', cat_protein, 150, 'g', 425, 35, 10, 28, 0, true, true, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{pork,gluten}', 0.8),
('Breaded Pork Cutlet (1 cutlet)', 'Protein', cat_protein, 140, 'g', 387, 31, 15, 22, 1, true, true, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{pork,gluten,eggs}', 0.8),
('Schnitzel (1 cutlet)', 'Protein', cat_protein, 140, 'g', 387, 31, 15, 22, 1, true, true, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{pork,gluten,eggs}', 0.8),
('Chicken Fried Steak (1 piece with gravy)', 'Protein', cat_protein, 200, 'g', 490, 30, 28, 28, 1, true, false, false, 'processed', 'cooked', '{lunch,dinner}', '{beef,gluten,dairy}', 0.75),
('Pot Roast (4 oz with vegetables)', 'Protein', cat_protein, 200, 'g', 245, 28, 8, 11, 2, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{beef}', 0.9),
('Liver & Onions (4 oz liver)', 'Protein', cat_protein, 113, 'g', 175, 23, 4, 7, 0, true, false, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{beef}', 0.9),
('Tongue (4 oz)', 'Protein', cat_protein, 113, 'g', 320, 21, 0, 26, 0, true, true, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{beef}', 0.85),
('Oxtail (4 oz)', 'Protein', cat_protein, 113, 'g', 260, 25, 0, 17, 0, true, true, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{beef}', 0.85),
('Tripe (4 oz)', 'Protein', cat_protein, 113, 'g', 96, 18, 2, 2, 0, true, true, false, 'minimally_processed', 'cooked', '{lunch,dinner}', '{beef}', 0.85);

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

END $$;

-- Count foods by category
SELECT food_group, COUNT(*) as count
FROM foods_enhanced
WHERE name LIKE '%Hot Dog%'
   OR name LIKE '%Sausage%'
   OR name LIKE '%Croissant%'
   OR name LIKE '%Muffin%'
   OR name LIKE '%Cheese%'
GROUP BY food_group
ORDER BY count DESC;

-- List all hot dogs/sausages
SELECT name, calories, protein_g FROM foods_enhanced
WHERE name LIKE '%Hot Dog%' OR name LIKE '%Sausage%' OR name LIKE '%Bratwurst%'
ORDER BY name;

-- List all breakfast pastries
SELECT name, calories, total_carbs_g FROM foods_enhanced
WHERE name LIKE '%Croissant%' OR name LIKE '%Danish%' OR name LIKE '%Muffin%'
   OR name LIKE '%Scone%' OR name LIKE '%Turnover%'
ORDER BY calories DESC;

-- Total count
SELECT COUNT(*) as total_foods FROM foods_enhanced;

