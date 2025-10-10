-- ============================================================================
-- PHASE 4: REAL WORLD PRODUCE DATABASE - FRUITS & VEGETABLES (130 FOODS)
-- ============================================================================
-- What people ACTUALLY buy: dried fruits, frozen produce, canned vegetables,
-- keto substitutes (cauliflower rice, zoodles), salad toppings, pickled items
-- Priority: Tier 1 (must-haves), Tier 2 (common), Tier 3 (specialty)
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
-- TIER 1: MUST-HAVE FRUITS (15 items)
-- ============================================================================

INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES

-- Citrus (critical for water, cooking, drinks)
('Lemon (1 whole)', 'Fruits', cat_fruits, 58, 'g', 17, 1, 5, 0, 2, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Lime (1 whole)', 'Fruits', cat_fruits, 67, 'g', 20, 0, 7, 0, 2, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Tangerine/Clementine (1 medium)', 'Fruits', cat_fruits, 74, 'g', 35, 1, 9, 0, 1, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),

-- Dried fruits (calorie-dense, people snack on these)
('Raisins (1/4 cup, small box)', 'Fruits', cat_fruits, 41, 'g', 123, 1, 33, 0, 2, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Dried Cranberries/Craisins (1/4 cup)', 'Fruits', cat_fruits, 40, 'g', 130, 0, 33, 0, 2, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Dried Apricots (5 pieces)', 'Fruits', cat_fruits, 35, 'g', 83, 1, 22, 0, 2, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Dried Mango (1/4 cup)', 'Fruits', cat_fruits, 40, 'g', 140, 1, 35, 0, 1, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Prunes/Dried Plums (5 pieces)', 'Fruits', cat_fruits, 42, 'g', 100, 1, 27, 0, 3, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Dates (Deglet Noor, 5 dates)', 'Fruits', cat_fruits, 42, 'g', 117, 1, 31, 0, 3, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Banana Chips (1 oz)', 'Fruits', cat_fruits, 28, 'g', 147, 1, 17, 10, 2, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),

-- Canned fruits (what people actually buy)
('Applesauce (Sweetened, 1/2 cup)', 'Fruits', cat_fruits, 128, 'g', 97, 0, 25, 0, 2, true, true, false, 'processed', 'raw', '{snack,dessert}', '{vegetarian,vegan}', 1.0),
('Applesauce (Unsweetened, 1/2 cup)', 'Fruits', cat_fruits, 122, 'g', 52, 0, 14, 0, 1, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Canned Peaches (in juice, 1/2 cup)', 'Fruits', cat_fruits, 124, 'g', 55, 1, 14, 0, 1, true, true, false, 'processed', 'raw', '{snack,dessert}', '{vegetarian,vegan}', 1.0),
('Canned Pineapple Chunks (in juice, 1/2 cup)', 'Fruits', cat_fruits, 124, 'g', 75, 1, 20, 0, 1, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Fruit Cocktail (in syrup, 1/2 cup)', 'Fruits', cat_fruits, 124, 'g', 91, 0, 23, 0, 1, true, true, false, 'processed', 'raw', '{snack,dessert}', '{vegetarian,vegan}', 1.0),

-- ============================================================================
-- TIER 1: FROZEN FRUITS (5 items) - For smoothies
-- ============================================================================

('Frozen Strawberries (1 cup)', 'Fruits', cat_fruits, 150, 'g', 53, 1, 14, 0, 3, true, true, true, 'raw', 'raw', '{snack,breakfast}', '{vegetarian,vegan}', 1.0),
('Frozen Blueberries (1 cup)', 'Fruits', cat_fruits, 150, 'g', 79, 1, 19, 1, 4, true, true, true, 'raw', 'raw', '{snack,breakfast}', '{vegetarian,vegan}', 1.0),
('Frozen Mixed Berries (1 cup)', 'Fruits', cat_fruits, 150, 'g', 64, 1, 16, 0, 4, true, true, true, 'raw', 'raw', '{snack,breakfast}', '{vegetarian,vegan}', 1.0),
('Frozen Mango Chunks (1 cup)', 'Fruits', cat_fruits, 165, 'g', 99, 1, 25, 1, 3, true, true, true, 'raw', 'raw', '{snack,breakfast}', '{vegetarian,vegan}', 1.0),
('Frozen Banana Slices (1 cup)', 'Fruits', cat_fruits, 150, 'g', 134, 2, 34, 0, 4, true, true, true, 'raw', 'raw', '{snack,breakfast}', '{vegetarian,vegan}', 1.0),

-- ============================================================================
-- TIER 1: MUST-HAVE VEGETABLES (30 items)
-- ============================================================================

-- Keto/Low-Carb Substitutes (HUGE trend)
('Cauliflower Rice (1 cup)', 'Vegetables', cat_vegetables, 107, 'g', 25, 2, 5, 0, 2, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Zucchini Noodles/Zoodles (1 cup)', 'Vegetables', cat_vegetables, 124, 'g', 20, 2, 4, 0, 1, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Spaghetti Squash (1 cup cooked)', 'Vegetables', cat_vegetables, 155, 'g', 42, 1, 10, 0, 2, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- Pre-cut convenience vegetables
('Baby Carrots (10 carrots)', 'Vegetables', cat_vegetables, 85, 'g', 35, 1, 8, 0, 2, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Coleslaw Mix (Pre-shredded, 1 cup)', 'Vegetables', cat_vegetables, 89, 'g', 22, 1, 5, 0, 2, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- Alliums (critical for cooking)
('Red Onion (1/2 cup sliced)', 'Vegetables', cat_vegetables, 58, 'g', 23, 1, 5, 0, 1, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Scallions/Green Onions (1/4 cup sliced)', 'Vegetables', cat_vegetables, 25, 'g', 8, 0, 2, 0, 1, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Shallots (2 tbsp minced)', 'Vegetables', cat_vegetables, 20, 'g', 14, 1, 3, 0, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- Tomato products (critical for cooking)
('Grape Tomatoes (1 cup)', 'Vegetables', cat_vegetables, 149, 'g', 27, 1, 6, 0, 2, true, true, true, 'raw', 'raw', '{snack,lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Sun-Dried Tomatoes (1/4 cup)', 'Vegetables', cat_vegetables, 27, 'g', 70, 4, 15, 1, 3, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Canned Diced Tomatoes (1/2 cup)', 'Vegetables', cat_vegetables, 121, 'g', 25, 1, 6, 0, 1, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Tomato Paste (2 tbsp)', 'Vegetables', cat_vegetables, 33, 'g', 27, 1, 6, 0, 1, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Tomato Sauce (1/2 cup)', 'Vegetables', cat_vegetables, 122, 'g', 39, 2, 9, 0, 2, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- Pickled/Fermented (common toppings people forget)
('Dill Pickles (1 large spear)', 'Vegetables', cat_vegetables, 65, 'g', 7, 0, 1, 0, 1, true, true, false, 'processed', 'raw', '{snack,lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Bread & Butter Pickles (4 chips)', 'Vegetables', cat_vegetables, 28, 'g', 21, 0, 5, 0, 0, true, true, false, 'processed', 'raw', '{snack,lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Kimchi (1/2 cup)', 'Vegetables', cat_vegetables, 75, 'g', 11, 1, 2, 0, 1, true, true, false, 'processed', 'raw', '{lunch,dinner,snack}', '{vegetarian,vegan}', 1.0),
('Sauerkraut (1/2 cup)', 'Vegetables', cat_vegetables, 71, 'g', 14, 1, 3, 0, 2, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- Olives (pizza, salads, appetizers)
('Black Olives (Sliced, 2 tbsp)', 'Fats', cat_fats, 17, 'g', 20, 0, 1, 2, 1, true, true, false, 'processed', 'raw', '{snack,lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Kalamata Olives (10 olives)', 'Fats', cat_fats, 40, 'g', 45, 0, 2, 4, 1, true, true, false, 'processed', 'raw', '{snack,lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Green Olives (10 olives)', 'Fats', cat_fats, 34, 'g', 41, 0, 1, 4, 1, true, true, false, 'processed', 'raw', '{snack,lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- Canned vegetables (budget staples)
('Canned Corn (1/2 cup)', 'Vegetables', cat_vegetables, 82, 'g', 66, 2, 15, 1, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Canned Green Beans (1/2 cup)', 'Vegetables', cat_vegetables, 68, 'g', 14, 1, 3, 0, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Canned Peas (1/2 cup)', 'Vegetables', cat_vegetables, 85, 'g', 59, 4, 11, 0, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- Frozen vegetables (what people actually buy)
('Frozen Broccoli (1 cup)', 'Vegetables', cat_vegetables, 91, 'g', 25, 3, 5, 0, 3, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Frozen Cauliflower (1 cup)', 'Vegetables', cat_vegetables, 107, 'g', 27, 2, 5, 0, 2, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Frozen Mixed Vegetables (1 cup)', 'Vegetables', cat_vegetables, 91, 'g', 59, 3, 12, 0, 4, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Frozen Stir-Fry Vegetable Mix (1 cup)', 'Vegetables', cat_vegetables, 108, 'g', 30, 2, 6, 0, 2, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Frozen Spinach (1/2 cup cooked)', 'Vegetables', cat_vegetables, 95, 'g', 30, 4, 5, 0, 3, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- Salad toppings (hidden calories!)
('Croutons (1/4 cup)', 'Grains', cat_carbs, 30, 'g', 122, 4, 22, 2, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 1.0),
('Bacon Bits (Real, 2 tbsp)', 'Protein', cat_protein, 14, 'g', 60, 6, 0, 5, 0, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{pork}', 1.0),

-- ============================================================================
-- TIER 2: TROPICAL & SPECIALTY FRUITS (10 items)
-- ============================================================================

('Dragonfruit/Pitaya (1 cup cubed)', 'Fruits', cat_fruits, 227, 'g', 136, 3, 29, 0, 7, true, true, true, 'raw', 'raw', '{snack,breakfast}', '{vegetarian,vegan}', 1.0),
('Lychee (10 fruits)', 'Fruits', cat_fruits, 80, 'g', 54, 1, 14, 0, 1, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Guava (1 fruit)', 'Fruits', cat_fruits, 55, 'g', 37, 1, 8, 1, 3, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Passion Fruit (1 fruit)', 'Fruits', cat_fruits, 18, 'g', 17, 0, 4, 0, 2, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Starfruit/Carambola (1 fruit)', 'Fruits', cat_fruits, 91, 'g', 28, 1, 6, 0, 3, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Persimmon (1 fruit)', 'Fruits', cat_fruits, 168, 'g', 118, 1, 31, 0, 6, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Blood Orange (1 medium)', 'Fruits', cat_fruits, 131, 'g', 70, 1, 18, 0, 3, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Apricot (3 fruits)', 'Fruits', cat_fruits, 105, 'g', 51, 1, 12, 0, 2, true, true, true, 'raw', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Maraschino Cherries (3 cherries)', 'Fruits', cat_fruits, 21, 'g', 20, 0, 5, 0, 0, true, true, false, 'processed', 'raw', '{dessert,snack}', '{vegetarian}', 1.0),
('Coconut (Dried/Sweetened, 2 tbsp)', 'Fruits', cat_fruits, 15, 'g', 71, 1, 7, 5, 1, true, true, false, 'processed', 'raw', '{snack,dessert}', '{vegetarian,vegan}', 1.0),

-- ============================================================================
-- TIER 2: ASIAN VEGETABLES (10 items)
-- ============================================================================

('Snap Peas/Sugar Snap Peas (1 cup)', 'Vegetables', cat_vegetables, 98, 'g', 41, 3, 7, 0, 3, true, true, true, 'raw', 'raw', '{snack,lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Baby Corn (1/2 cup)', 'Vegetables', cat_vegetables, 65, 'g', 13, 1, 3, 0, 1, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Water Chestnuts (Canned, 1/2 cup sliced)', 'Vegetables', cat_vegetables, 70, 'g', 35, 1, 9, 0, 2, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Bamboo Shoots (Canned, 1/2 cup sliced)', 'Vegetables', cat_vegetables, 66, 'g', 13, 1, 2, 0, 1, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Bean Sprouts (1 cup)', 'Vegetables', cat_vegetables, 104, 'g', 31, 3, 6, 0, 2, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Napa Cabbage (1 cup shredded)', 'Vegetables', cat_vegetables, 70, 'g', 9, 1, 2, 0, 1, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Broccolini (1 cup)', 'Vegetables', cat_vegetables, 85, 'g', 29, 3, 6, 0, 2, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Chinese Broccoli/Gai Lan (1 cup)', 'Vegetables', cat_vegetables, 88, 'g', 19, 1, 3, 1, 2, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Daikon Radish (1 cup cubed)', 'Vegetables', cat_vegetables, 116, 'g', 21, 1, 5, 0, 2, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Jicama (1 cup cubed)', 'Vegetables', cat_vegetables, 120, 'g', 46, 1, 11, 0, 6, true, true, true, 'raw', 'raw', '{snack,lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- ============================================================================
-- TIER 2: MORE VEGETABLES (15 items)
-- ============================================================================

-- Peppers
('Yellow Bell Pepper (1 medium)', 'Vegetables', cat_vegetables, 186, 'g', 50, 2, 12, 0, 2, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Orange Bell Pepper (1 medium)', 'Vegetables', cat_vegetables, 186, 'g', 46, 1, 11, 0, 2, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Jalapeño Pepper (1 pepper)', 'Vegetables', cat_vegetables, 14, 'g', 4, 0, 1, 0, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Poblano Pepper (1 pepper)', 'Vegetables', cat_vegetables, 68, 'g', 17, 1, 3, 0, 1, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- Squash
('Yellow Squash (1 cup cooked)', 'Vegetables', cat_vegetables, 180, 'g', 36, 2, 8, 1, 3, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Pumpkin Puree (Canned, 1/2 cup)', 'Vegetables', cat_vegetables, 122, 'g', 42, 1, 10, 0, 4, true, true, false, 'processed', 'raw', '{breakfast,dessert}', '{vegetarian,vegan}', 1.0),

-- Leafy greens
('Collard Greens (1 cup cooked)', 'Vegetables', cat_vegetables, 190, 'g', 49, 4, 9, 1, 5, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Mustard Greens (1 cup cooked)', 'Vegetables', cat_vegetables, 140, 'g', 21, 3, 3, 0, 3, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- Artichoke
('Artichoke Hearts (Canned/Jarred, 1/2 cup)', 'Vegetables', cat_vegetables, 100, 'g', 45, 2, 10, 0, 5, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Artichoke (1 whole cooked)', 'Vegetables', cat_vegetables, 120, 'g', 64, 4, 14, 0, 7, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- Other
('Hearts of Palm (1/2 cup sliced)', 'Vegetables', cat_vegetables, 73, 'g', 18, 2, 3, 0, 2, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Fennel Bulb (1 cup sliced)', 'Vegetables', cat_vegetables, 87, 'g', 27, 1, 6, 0, 3, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Okra (1 cup cooked)', 'Vegetables', cat_vegetables, 160, 'g', 36, 3, 7, 0, 4, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Green Chilies (Canned, diced, 1/4 cup)', 'Vegetables', cat_vegetables, 65, 'g', 13, 1, 3, 0, 1, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Roasted Red Peppers (Jarred, 1/4 cup)', 'Vegetables', cat_vegetables, 60, 'g', 20, 1, 4, 0, 1, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- ============================================================================
-- TIER 3: FRESH HERBS (10 items)
-- ============================================================================

('Basil (Fresh, 1/4 cup chopped)', 'Vegetables', cat_vegetables, 10, 'g', 2, 0, 0, 0, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Cilantro (Fresh, 1/4 cup chopped)', 'Vegetables', cat_vegetables, 4, 'g', 1, 0, 0, 0, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Parsley (Fresh, 1/4 cup chopped)', 'Vegetables', cat_vegetables, 15, 'g', 5, 0, 1, 0, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Mint (Fresh, 1/4 cup chopped)', 'Vegetables', cat_vegetables, 15, 'g', 6, 1, 1, 0, 1, true, true, true, 'raw', 'raw', '{snack,dessert}', '{vegetarian,vegan}', 1.0),
('Dill (Fresh, 2 tbsp chopped)', 'Vegetables', cat_vegetables, 2, 'g', 1, 0, 0, 0, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Rosemary (Fresh, 1 tbsp chopped)', 'Vegetables', cat_vegetables, 2, 'g', 2, 0, 0, 0, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Thyme (Fresh, 1 tbsp leaves)', 'Vegetables', cat_vegetables, 3, 'g', 3, 0, 1, 0, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Ginger (Fresh, 1 tbsp grated)', 'Vegetables', cat_vegetables, 6, 'g', 5, 0, 1, 0, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Chives (Fresh, 1 tbsp chopped)', 'Vegetables', cat_vegetables, 3, 'g', 1, 0, 0, 0, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Oregano (Fresh, 1 tbsp)', 'Vegetables', cat_vegetables, 2, 'g', 1, 0, 0, 0, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- ============================================================================
-- TIER 3: VEGETABLE CHIPS & SUBSTITUTES (5 items)
-- ============================================================================

('Kale Chips (1 oz)', 'Vegetables', cat_vegetables, 28, 'g', 130, 3, 13, 7, 2, true, true, false, 'processed', 'cooked', '{snack}', '{vegetarian,vegan}', 1.0),
('Sweet Potato Chips (1 oz)', 'Vegetables', cat_vegetables, 28, 'g', 142, 1, 18, 7, 2, true, true, false, 'processed', 'cooked', '{snack}', '{vegetarian,vegan}', 1.0),
('Beet Chips (1 oz)', 'Vegetables', cat_vegetables, 28, 'g', 120, 2, 16, 5, 3, true, true, false, 'processed', 'cooked', '{snack}', '{vegetarian,vegan}', 1.0),
('Mixed Veggie Chips (Terra, 1 oz)', 'Vegetables', cat_vegetables, 28, 'g', 150, 1, 16, 9, 3, false, true, false, 'processed', 'cooked', '{snack}', '{vegetarian,vegan}', 1.0),
('Carrot Noodles (1 cup)', 'Vegetables', cat_vegetables, 110, 'g', 45, 1, 10, 0, 3, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),

-- ============================================================================
-- TIER 3: MISC PRODUCE (10 items)
-- ============================================================================

('Fruit Leather/Roll-Ups (1 roll)', 'Fruits', cat_fruits, 21, 'g', 74, 0, 18, 1, 1, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Canned Mandarin Oranges (in juice, 1/2 cup)', 'Fruits', cat_fruits, 124, 'g', 46, 1, 12, 0, 1, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Canned Pears (in juice, 1/2 cup)', 'Fruits', cat_fruits, 124, 'g', 62, 0, 16, 0, 2, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Apple Chips (1 oz)', 'Fruits', cat_fruits, 28, 'g', 140, 0, 20, 7, 3, true, true, false, 'processed', 'cooked', '{snack}', '{vegetarian,vegan}', 1.0),
('Dried Figs (3 pieces)', 'Fruits', cat_fruits, 50, 'g', 125, 2, 32, 0, 5, true, true, false, 'processed', 'raw', '{snack}', '{vegetarian,vegan}', 1.0),
('Rhubarb (1 cup chopped)', 'Vegetables', cat_vegetables, 122, 'g', 26, 1, 6, 0, 2, true, true, true, 'raw', 'raw', '{dessert}', '{vegetarian,vegan}', 1.0),
('Lima Beans (Frozen, 1/2 cup)', 'Vegetables', cat_vegetables, 85, 'g', 95, 6, 18, 0, 5, true, true, true, 'raw', 'cooked', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Frozen Brussels Sprouts (1 cup)', 'Vegetables', cat_vegetables, 88, 'g', 37, 3, 8, 0, 3, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Leeks (1/2 cup sliced)', 'Vegetables', cat_vegetables, 45, 'g', 27, 1, 6, 0, 1, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0),
('Red Cabbage (1 cup shredded)', 'Vegetables', cat_vegetables, 70, 'g', 22, 1, 5, 0, 1, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{vegetarian,vegan}', 1.0);

END $$;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Count Phase 4 foods by category
SELECT
    food_group,
    COUNT(*) as count
FROM foods_enhanced
WHERE name LIKE '%Dried%'
   OR name LIKE '%Frozen%'
   OR name LIKE '%Canned%'
   OR name LIKE '%Pickles%'
   OR name LIKE '%Kimchi%'
   OR name LIKE '%Cauliflower Rice%'
   OR name LIKE '%Zoodles%'
   OR name LIKE '%Olives%'
   OR name LIKE '%Croutons%'
GROUP BY food_group
ORDER BY count DESC;

-- List dried fruits (calorie-dense!)
SELECT name, calories, total_carbs_g FROM foods_enhanced
WHERE name LIKE '%Dried%' OR name LIKE '%Raisins%' OR name LIKE '%Prunes%'
ORDER BY calories DESC;

-- List keto substitutes
SELECT name, calories, total_carbs_g FROM foods_enhanced
WHERE name LIKE '%Cauliflower Rice%'
   OR name LIKE '%Zoodles%'
   OR name LIKE '%Spaghetti Squash%'
ORDER BY name;

-- Total count across all phases
SELECT COUNT(*) as total_foods FROM foods_enhanced;
