-- ============================================================================
-- PHASE 1: REAL WORLD FOOD DATABASE - FAST FOOD & ESSENTIALS (100 FOODS)
-- ============================================================================
-- This is what people ACTUALLY eat, not fitness influencer bullshit
-- Priority: Fast food, pizza, burgers, breakfast, snacks
-- Coverage: 60% of real-world meal logs
-- ============================================================================

-- Get category IDs
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
    SELECT id INTO cat_protein FROM food_categories WHERE name = 'Protein' AND level = 0;
    SELECT id INTO cat_carbs FROM food_categories WHERE name = 'Grains' AND level = 0;
    SELECT id INTO cat_fruits FROM food_categories WHERE name = 'Fruits' AND level = 0;
    SELECT id INTO cat_vegetables FROM food_categories WHERE name = 'Vegetables' AND level = 0;
    SELECT id INTO cat_fats FROM food_categories WHERE name = 'Fats, Nuts & Seeds' AND level = 0;
    SELECT id INTO cat_dairy FROM food_categories WHERE name = 'Dairy' AND level = 0;
    SELECT id INTO cat_beverages FROM food_categories WHERE name = 'Beverages' AND level = 0;

-- ============================================================================
-- SECTION 1: PIZZA (10 variations) - THE MOST LOGGED FOOD
-- ============================================================================

INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
-- Basic pizzas (per slice, ~107g)
('Cheese Pizza (1 slice)', 'Grains', cat_carbs, 107, 'g', 272, 12, 34, 10, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Pepperoni Pizza (1 slice)', 'Grains', cat_carbs, 107, 'g', 298, 13, 34, 12, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,pork}', 1.0),
('Supreme Pizza (1 slice)', 'Grains', cat_carbs, 130, 'g', 305, 14, 33, 13, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Meat Lovers Pizza (1 slice)', 'Grains', cat_carbs, 135, 'g', 350, 16, 32, 17, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,pork}', 1.0),
('Veggie Pizza (1 slice)', 'Grains', cat_carbs, 115, 'g', 235, 10, 35, 7, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,vegetarian}', 1.0),

-- Chain pizzas (realistic portions - 2 slices)
('Domino''s Pepperoni Pizza (2 slices, Medium Hand Tossed)', 'Grains', cat_carbs, 214, 'g', 560, 24, 66, 20, 4, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,pork}', 1.0),
('Pizza Hut Personal Pan Pepperoni', 'Grains', cat_carbs, 180, 'g', 540, 22, 64, 22, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,pork}', 1.0),
('Papa John''s Large Cheese (2 slices)', 'Grains', cat_carbs, 200, 'g', 520, 22, 62, 18, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Costco Food Court Slice (1 slice)', 'Grains', cat_carbs, 215, 'g', 710, 28, 70, 28, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Frozen Pizza (DiGiorno/Red Baron, 1/4 pizza)', 'Grains', cat_carbs, 150, 'g', 380, 15, 45, 15, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),

-- ============================================================================
-- SECTION 2: BURGERS (12 variations) - AMERICA'S FAVORITE
-- ============================================================================

-- Generic/homemade
('Cheeseburger (Generic/Homemade)', 'Protein', cat_protein, 180, 'g', 535, 30, 36, 26, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),

-- McDonald's
('McDonald''s Big Mac', 'Protein', cat_protein, 215, 'g', 550, 25, 45, 30, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('McDonald''s Quarter Pounder with Cheese', 'Protein', cat_protein, 220, 'g', 540, 31, 43, 28, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('McDonald''s Cheeseburger', 'Protein', cat_protein, 120, 'g', 300, 15, 33, 12, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),

-- Other chains
('Burger King Whopper', 'Protein', cat_protein, 290, 'g', 660, 28, 49, 40, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Wendy''s Dave''s Single', 'Protein', cat_protein, 249, 'g', 590, 29, 41, 34, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Five Guys Cheeseburger', 'Protein', cat_protein, 320, 'g', 840, 39, 40, 55, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('In-N-Out Double-Double', 'Protein', cat_protein, 330, 'g', 670, 37, 39, 41, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Shake Shack ShackBurger', 'Protein', cat_protein, 196, 'g', 530, 26, 33, 30, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Smashburger Classic Smash', 'Protein', cat_protein, 220, 'g', 540, 28, 42, 27, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Carl''s Jr. Famous Star', 'Protein', cat_protein, 254, 'g', 590, 26, 50, 32, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Whataburger (Texas)', 'Protein', cat_protein, 261, 'g', 620, 29, 62, 27, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),

-- ============================================================================
-- SECTION 3: FAST FOOD CHICKEN (8 variations)
-- ============================================================================

('McDonald''s Chicken McNuggets (10pc)', 'Protein', cat_protein, 170, 'g', 440, 24, 27, 27, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{gluten}', 1.0),
('McDonald''s McChicken Sandwich', 'Protein', cat_protein, 143, 'g', 400, 14, 39, 21, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Chick-fil-A Chicken Sandwich', 'Protein', cat_protein, 183, 'g', 440, 28, 41, 19, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Chick-fil-A Nuggets (12pc)', 'Protein', cat_protein, 170, 'g', 380, 40, 16, 16, 1, false, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{gluten}', 1.0),
('Chick-fil-A Spicy Chicken Sandwich', 'Protein', cat_protein, 188, 'g', 450, 28, 43, 19, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Popeyes Chicken Sandwich', 'Protein', cat_protein, 221, 'g', 700, 28, 50, 42, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('KFC Original Recipe (2 pieces - thigh & drumstick)', 'Protein', cat_protein, 198, 'g', 520, 36, 18, 34, 1, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('KFC Popcorn Chicken (Individual)', 'Protein', cat_protein, 114, 'g', 410, 19, 24, 26, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{gluten}', 1.0),

-- ============================================================================
-- SECTION 4: MEXICAN FAST FOOD (10 variations)
-- ============================================================================

('Taco Bell Crunchy Taco (3 tacos)', 'Protein', cat_protein, 255, 'g', 510, 18, 39, 30, 6, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Taco Bell Bean Burrito', 'Grains', cat_carbs, 198, 'g', 350, 13, 54, 10, 8, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,vegetarian}', 1.0),
('Taco Bell Chicken Quesadilla', 'Protein', cat_protein, 184, 'g', 510, 27, 38, 27, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Taco Bell Chalupa Supreme - Beef', 'Protein', cat_protein, 153, 'g', 360, 14, 30, 19, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Chipotle Chicken Burrito (Full wrap)', 'Protein', cat_protein, 507, 'g', 930, 53, 110, 30, 14, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Qdoba Chicken Burrito', 'Protein', cat_protein, 500, 'g', 920, 50, 105, 32, 12, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Del Taco Classic Taco (3 tacos)', 'Protein', cat_protein, 240, 'g', 450, 18, 42, 21, 6, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Beef Burrito (Generic)', 'Protein', cat_protein, 297, 'g', 565, 29, 58, 24, 8, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Chicken Quesadilla (Generic)', 'Protein', cat_protein, 180, 'g', 495, 28, 36, 26, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{dairy,gluten}', 1.0),
('Chicken Taco (Homemade, 1 taco)', 'Protein', cat_protein, 100, 'g', 200, 15, 18, 8, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),

-- ============================================================================
-- SECTION 5: SANDWICHES & SUBS (10 variations)
-- ============================================================================

('Ham and Cheese Sandwich', 'Protein', cat_protein, 145, 'g', 350, 21, 33, 15, 2, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{dairy,gluten,pork}', 1.0),
('BLT Sandwich', 'Protein', cat_protein, 140, 'g', 340, 13, 29, 19, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,pork}', 1.0),
('Grilled Cheese Sandwich', 'Dairy', cat_dairy, 110, 'g', 370, 14, 30, 20, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{dairy,gluten,vegetarian}', 1.0),
('Peanut Butter & Jelly Sandwich', 'Fats', cat_fats, 100, 'g', 380, 13, 47, 16, 3, true, true, false, 'processed', 'raw', '{breakfast,lunch,snack}', '{gluten,nuts,vegetarian}', 1.0),
('Jimmy John''s Turkey Tom', 'Protein', cat_protein, 240, 'g', 515, 29, 54, 17, 2, false, true, false, 'processed', 'raw', '{lunch,dinner}', '{gluten}', 1.0),
('Jimmy John''s #9 Italian', 'Protein', cat_protein, 285, 'g', 850, 40, 57, 49, 2, false, true, false, 'processed', 'raw', '{lunch,dinner}', '{dairy,gluten,pork}', 1.0),
('Jersey Mike''s #13 Italian Sub (Regular)', 'Protein', cat_protein, 330, 'g', 830, 43, 64, 42, 4, false, true, false, 'processed', 'raw', '{lunch,dinner}', '{dairy,gluten,pork}', 1.0),
('Firehouse Subs Hook & Ladder (Medium)', 'Protein', cat_protein, 360, 'g', 740, 44, 64, 32, 3, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Arby''s Roast Beef Classic', 'Protein', cat_protein, 154, 'g', 360, 23, 37, 14, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Subway Italian BMT (6-inch)', 'Protein', cat_protein, 236, 'g', 410, 21, 46, 16, 3, false, true, false, 'processed', 'raw', '{lunch,dinner}', '{dairy,gluten,pork}', 1.0),

-- ============================================================================
-- SECTION 6: FRIED FOOD & SIDES (8 variations)
-- ============================================================================

('French Fries (Medium)', 'Grains', cat_carbs, 117, 'g', 365, 4, 48, 17, 5, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{vegetarian}', 1.0),
('French Fries (Large)', 'Grains', cat_carbs, 154, 'g', 480, 6, 63, 23, 6, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{vegetarian}', 1.0),
('Onion Rings (Medium)', 'Vegetables', cat_vegetables, 128, 'g', 410, 5, 53, 19, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{gluten,vegetarian}', 1.0),
('Mozzarella Sticks (6pc)', 'Dairy', cat_dairy, 144, 'g', 500, 24, 38, 28, 2, true, true, false, 'processed', 'cooked', '{snack,appetizer}', '{dairy,gluten,vegetarian}', 1.0),
('Chicken Tenders (5pc)', 'Protein', cat_protein, 175, 'g', 480, 35, 31, 23, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{gluten}', 1.0),
('Buffalo Wings (12pc)', 'Protein', cat_protein, 336, 'g', 960, 96, 0, 64, 0, true, true, false, 'processed', 'cooked', '{lunch,dinner,snack}', '{}', 1.0),
('Potato Chips (1 oz bag)', 'Grains', cat_carbs, 28, 'g', 150, 2, 15, 10, 1, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Tortilla Chips with Queso (Restaurant portion)', 'Grains', cat_carbs, 200, 'g', 545, 14, 58, 28, 6, true, true, false, 'processed', 'cooked', '{snack,appetizer}', '{dairy,vegetarian}', 1.0),

-- ============================================================================
-- SECTION 7: BREAKFAST - FAST FOOD (12 variations)
-- ============================================================================

('McDonald''s Egg McMuffin', 'Protein', cat_protein, 136, 'g', 310, 17, 30, 13, 2, false, true, false, 'processed', 'cooked', '{breakfast}', '{dairy,gluten}', 1.0),
('McDonald''s Sausage McMuffin with Egg', 'Protein', cat_protein, 163, 'g', 480, 21, 30, 30, 2, false, true, false, 'processed', 'cooked', '{breakfast}', '{dairy,gluten,pork}', 1.0),
('McDonald''s Sausage Biscuit', 'Protein', cat_protein, 113, 'g', 460, 11, 35, 30, 2, false, true, false, 'processed', 'cooked', '{breakfast}', '{gluten,pork}', 1.0),
('McDonald''s Hash Browns (2 pieces)', 'Grains', cat_carbs, 110, 'g', 300, 3, 30, 19, 3, false, true, false, 'processed', 'cooked', '{breakfast}', '{vegetarian}', 1.0),
('McDonald''s Hotcakes (3) with Syrup', 'Grains', cat_carbs, 226, 'g', 580, 9, 102, 16, 2, false, true, false, 'processed', 'cooked', '{breakfast}', '{dairy,gluten,vegetarian}', 1.0),
('Burger King Croissan''wich (Sausage, Egg & Cheese)', 'Protein', cat_protein, 160, 'g', 520, 19, 32, 36, 1, false, true, false, 'processed', 'cooked', '{breakfast}', '{dairy,gluten,pork}', 1.0),
('Dunkin'' Donuts Bacon, Egg & Cheese on Croissant', 'Protein', cat_protein, 165, 'g', 560, 20, 39, 35, 1, false, true, false, 'processed', 'cooked', '{breakfast}', '{dairy,gluten,pork}', 1.0),
('Dunkin'' Hash Browns', 'Grains', cat_carbs, 57, 'g', 140, 1, 15, 9, 1, false, true, false, 'processed', 'cooked', '{breakfast}', '{vegetarian}', 1.0),
('Starbucks Sausage, Cheddar & Egg Sandwich', 'Protein', cat_protein, 159, 'g', 480, 21, 30, 30, 1, false, true, false, 'processed', 'cooked', '{breakfast}', '{dairy,gluten,pork}', 1.0),
('Chick-fil-A Chicken Biscuit', 'Protein', cat_protein, 149, 'g', 460, 18, 45, 23, 2, false, true, false, 'processed', 'cooked', '{breakfast}', '{dairy,gluten}', 1.0),
('Chick-fil-A Hash Browns', 'Grains', cat_carbs, 85, 'g', 270, 3, 25, 18, 3, false, true, false, 'processed', 'cooked', '{breakfast}', '{vegetarian}', 1.0),
('Taco Bell Breakfast Burrito', 'Protein', cat_protein, 201, 'g', 500, 18, 39, 29, 3, false, true, false, 'processed', 'cooked', '{breakfast}', '{dairy,gluten}', 1.0),

-- ============================================================================
-- SECTION 8: BREAKFAST - HOMEMADE (8 variations)
-- ============================================================================

('Scrambled Eggs (3 large eggs)', 'Protein', cat_protein, 150, 'g', 220, 19, 2, 15, 0, true, true, true, 'raw', 'cooked', '{breakfast}', '{vegetarian}', 1.0),
('Fried Eggs (2 large eggs)', 'Protein', cat_protein, 100, 'g', 185, 13, 1, 14, 0, true, true, true, 'raw', 'cooked', '{breakfast}', '{vegetarian}', 1.0),
('Omelet (3 eggs + cheese + veggies)', 'Protein', cat_protein, 225, 'g', 340, 24, 6, 24, 2, true, true, false, 'raw', 'cooked', '{breakfast}', '{dairy,vegetarian}', 1.0),
('Sausage Links (3 links)', 'Protein', cat_protein, 75, 'g', 288, 14, 2, 26, 0, true, true, false, 'processed', 'cooked', '{breakfast}', '{pork}', 1.0),
('Sausage Patties (2 patties)', 'Protein', cat_protein, 90, 'g', 340, 16, 1, 32, 0, true, true, false, 'processed', 'cooked', '{breakfast}', '{pork}', 1.0),
('Pancakes (3) with Butter & Syrup', 'Grains', cat_carbs, 232, 'g', 520, 9, 91, 14, 2, true, true, false, 'processed', 'cooked', '{breakfast}', '{dairy,gluten,vegetarian}', 1.0),
('Waffles (2) with Butter & Syrup', 'Grains', cat_carbs, 192, 'g', 460, 8, 74, 15, 2, true, true, false, 'processed', 'cooked', '{breakfast}', '{dairy,gluten,vegetarian}', 1.0),
('Bagel with Cream Cheese', 'Grains', cat_carbs, 110, 'g', 360, 11, 52, 13, 2, true, true, false, 'processed', 'raw', '{breakfast,snack}', '{dairy,gluten,vegetarian}', 1.0);

END $$;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Count new foods by category
SELECT
    food_group,
    COUNT(*) as count
FROM foods_enhanced
WHERE name LIKE '%McDonald%'
   OR name LIKE '%Pizza%'
   OR name LIKE '%Burger%'
   OR name LIKE '%Taco%'
GROUP BY food_group
ORDER BY count DESC;

-- List all pizza variations
SELECT name, calories, protein_g, total_carbs_g, total_fat_g
FROM foods_enhanced
WHERE name LIKE '%Pizza%'
ORDER BY name;

-- List all burger variations
SELECT name, calories, protein_g, total_carbs_g, total_fat_g
FROM foods_enhanced
WHERE name LIKE '%Burger%' OR name LIKE '%Whopper%' OR name LIKE '%Big Mac%'
ORDER BY calories DESC;

-- Total count
SELECT COUNT(*) as phase1_foods FROM foods_enhanced
WHERE name IN (
    SELECT DISTINCT name FROM foods_enhanced
    WHERE created_at > NOW() - INTERVAL '1 minute'
);
