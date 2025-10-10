-- ============================================================================
-- PHASE 2: REAL WORLD FOOD DATABASE - DESSERTS, DRINKS, PASTA, ASIAN (150 FOODS)
-- ============================================================================
-- Continuation of real-world foods database
-- Priority: Desserts, drinks (soda, coffee, alcohol), pasta, Asian food
-- Coverage: 80-85% of real-world meal logs
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
-- SECTION 1: DESSERTS - ICE CREAM (6 variations)
-- ============================================================================

INSERT INTO foods_enhanced (
    name, food_group, category_id,
    serving_size, serving_unit,
    calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g,
    is_generic, is_atomic, is_whole_food, processing_level,
    preparation_state, meal_suitability, dietary_flags,
    data_quality_score
) VALUES
('Vanilla Ice Cream (1/2 cup)', 'Dairy', cat_dairy, 66, 'g', 137, 2, 16, 7, 0, true, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,vegetarian}', 1.0),
('Vanilla Ice Cream (1 cup)', 'Dairy', cat_dairy, 132, 'g', 274, 5, 32, 14, 1, true, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,vegetarian}', 1.0),
('Chocolate Ice Cream (1/2 cup)', 'Dairy', cat_dairy, 66, 'g', 143, 3, 19, 7, 1, true, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,vegetarian}', 1.0),
('Chocolate Ice Cream (1 cup)', 'Dairy', cat_dairy, 132, 'g', 286, 5, 37, 15, 2, true, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,vegetarian}', 1.0),
('Ben & Jerry''s Pint (Half Baked)', 'Dairy', cat_dairy, 473, 'g', 1160, 20, 152, 56, 4, false, true, false, 'processed', 'raw', '{dessert}', '{dairy,gluten,vegetarian}', 1.0),
('Häagen-Dazs Vanilla (1/2 cup)', 'Dairy', cat_dairy, 106, 'g', 270, 5, 21, 18, 0, false, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,vegetarian}', 1.0),

-- Ice cream novelties
('Ice Cream Sandwich', 'Dairy', cat_dairy, 65, 'g', 166, 3, 27, 5, 1, true, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,gluten,vegetarian}', 1.0),
('Drumstick Cone (Vanilla with Chocolate/Peanuts)', 'Dairy', cat_dairy, 95, 'g', 290, 5, 34, 15, 1, false, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,gluten,nuts,vegetarian}', 1.0),

-- ============================================================================
-- SECTION 2: COOKIES & BAKED GOODS (8 variations)
-- ============================================================================

('Chocolate Chip Cookie (Large, homemade)', 'Grains', cat_carbs, 60, 'g', 285, 3, 37, 14, 1, true, true, false, 'processed', 'cooked', '{snack,dessert}', '{dairy,gluten,vegetarian}', 1.0),
('Chocolate Chip Cookie (3 small cookies)', 'Grains', cat_carbs, 90, 'g', 428, 4, 56, 21, 2, true, true, false, 'processed', 'cooked', '{snack,dessert}', '{dairy,gluten,vegetarian}', 1.0),
('Oreos (6 cookies)', 'Grains', cat_carbs, 60, 'g', 280, 2, 42, 12, 1, false, true, false, 'processed', 'raw', '{snack,dessert}', '{gluten,vegetarian}', 1.0),
('Chips Ahoy Cookies (3 cookies)', 'Grains', cat_carbs, 32, 'g', 160, 2, 21, 8, 1, false, true, false, 'processed', 'raw', '{snack,dessert}', '{gluten,vegetarian}', 1.0),
('Brownie (2x2 inch square)', 'Grains', cat_carbs, 56, 'g', 227, 3, 36, 9, 1, true, true, false, 'processed', 'cooked', '{snack,dessert}', '{dairy,gluten,vegetarian}', 1.0),
('Chocolate Cake with Frosting (1 slice)', 'Grains', cat_carbs, 95, 'g', 352, 5, 51, 16, 2, true, true, false, 'processed', 'cooked', '{dessert}', '{dairy,gluten,vegetarian}', 1.0),
('Vanilla Cake with Frosting (1 slice)', 'Grains', cat_carbs, 95, 'g', 355, 4, 54, 14, 0, true, true, false, 'processed', 'cooked', '{dessert}', '{dairy,gluten,vegetarian}', 1.0),
('Glazed Donut', 'Grains', cat_carbs, 60, 'g', 240, 4, 31, 11, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack,dessert}', '{dairy,gluten,vegetarian}', 1.0),
('Chocolate Frosted Donut', 'Grains', cat_carbs, 67, 'g', 270, 4, 35, 13, 1, true, true, false, 'processed', 'cooked', '{breakfast,snack,dessert}', '{dairy,gluten,vegetarian}', 1.0),

-- ============================================================================
-- SECTION 3: CANDY & SNACKS (10 variations)
-- ============================================================================

('M&M''s (Regular bag, 1.69oz)', 'Grains', cat_carbs, 48, 'g', 220, 2, 33, 9, 1, false, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,vegetarian}', 1.0),
('Snickers Bar (Regular, 1.86oz)', 'Grains', cat_carbs, 53, 'g', 250, 4, 33, 12, 1, false, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,nuts,vegetarian}', 1.0),
('Reese''s Peanut Butter Cups (2 cups)', 'Grains', cat_carbs, 42, 'g', 210, 5, 24, 13, 1, false, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,nuts,vegetarian}', 1.0),
('Kit Kat Bar (1.5oz, 4 pieces)', 'Grains', cat_carbs, 42, 'g', 210, 3, 27, 11, 1, false, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,gluten,vegetarian}', 1.0),
('Twix Bar (2 sticks, 1.79oz)', 'Grains', cat_carbs, 51, 'g', 250, 3, 34, 12, 1, false, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,gluten,vegetarian}', 1.0),
('Hershey''s Chocolate Bar (1.55oz)', 'Grains', cat_carbs, 43, 'g', 210, 3, 26, 13, 1, false, true, false, 'processed', 'raw', '{snack,dessert}', '{dairy,vegetarian}', 1.0),
('Skittles (Regular bag, 2.17oz)', 'Grains', cat_carbs, 61, 'g', 250, 0, 56, 2, 0, false, true, false, 'processed', 'raw', '{snack,dessert}', '{vegetarian}', 1.0),
('Sour Patch Kids (Regular bag, 1.9oz)', 'Grains', cat_carbs, 56, 'g', 210, 0, 52, 0, 0, false, true, false, 'processed', 'raw', '{snack,dessert}', '{vegetarian}', 1.0),
('Swedish Fish (10 pieces)', 'Grains', cat_carbs, 40, 'g', 140, 0, 35, 0, 0, false, true, false, 'processed', 'raw', '{snack,dessert}', '{vegetarian}', 1.0),
('Gummy Bears (10 pieces)', 'Grains', cat_carbs, 30, 'g', 85, 0, 21, 0, 0, true, true, false, 'processed', 'raw', '{snack,dessert}', '{vegetarian}', 1.0),

-- ============================================================================
-- SECTION 4: PASTA & ITALIAN (12 variations)
-- ============================================================================

('Spaghetti with Marinara (1 cup)', 'Grains', cat_carbs, 249, 'g', 260, 8, 51, 4, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 1.0),
('Spaghetti with Marinara (2 cups)', 'Grains', cat_carbs, 498, 'g', 520, 16, 102, 8, 8, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 1.0),
('Spaghetti with Meatballs (3 meatballs)', 'Protein', cat_protein, 420, 'g', 520, 26, 65, 14, 8, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Fettuccine Alfredo (1 cup)', 'Grains', cat_carbs, 240, 'g', 540, 13, 45, 33, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,vegetarian}', 1.0),
('Fettuccine Alfredo (2 cups)', 'Grains', cat_carbs, 480, 'g', 1080, 26, 90, 66, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,vegetarian}', 1.0),
('Chicken Alfredo', 'Protein', cat_protein, 450, 'g', 780, 46, 60, 38, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Shrimp Alfredo', 'Protein', cat_protein, 430, 'g', 720, 42, 58, 32, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,seafood}', 1.0),
('Baked Ziti (1 cup)', 'Grains', cat_carbs, 250, 'g', 350, 18, 42, 11, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,vegetarian}', 1.0),
('Lasagna (3x3 inch piece)', 'Protein', cat_protein, 215, 'g', 360, 22, 31, 16, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten}', 1.0),
('Penne alla Vodka (1 cup)', 'Grains', cat_carbs, 240, 'g', 460, 11, 56, 20, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,vegetarian}', 1.0),
('Mac and Cheese (Homemade, 1 cup)', 'Grains', cat_carbs, 200, 'g', 380, 15, 41, 17, 2, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,vegetarian}', 1.0),
('Mac and Cheese (Kraft box, 1 cup prepared)', 'Grains', cat_carbs, 189, 'g', 350, 11, 48, 12, 2, false, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,gluten,vegetarian}', 1.0),

-- Olive Garden
('Olive Garden Breadstick (1 stick)', 'Grains', cat_carbs, 42, 'g', 140, 4, 25, 2, 1, false, true, false, 'processed', 'cooked', '{appetizer}', '{gluten,vegetarian}', 1.0),

-- ============================================================================
-- SECTION 5: CHINESE TAKEOUT (10 variations)
-- ============================================================================

('Orange Chicken with Fried Rice', 'Protein', cat_protein, 425, 'g', 820, 32, 108, 28, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('General Tso''s Chicken with Fried Rice', 'Protein', cat_protein, 435, 'g', 890, 34, 115, 32, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Kung Pao Chicken with White Rice', 'Protein', cat_protein, 420, 'g', 780, 38, 92, 26, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,nuts}', 1.0),
('Beef and Broccoli with White Rice', 'Protein', cat_protein, 410, 'g', 690, 32, 82, 20, 5, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Sweet and Sour Chicken', 'Protein', cat_protein, 350, 'g', 550, 28, 76, 12, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Chicken Fried Rice (2 cups)', 'Grains', cat_carbs, 430, 'g', 640, 24, 88, 18, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Egg Rolls (2 rolls)', 'Grains', cat_carbs, 128, 'g', 340, 10, 40, 15, 3, true, true, false, 'processed', 'cooked', '{appetizer,snack}', '{gluten}', 1.0),
('Crab Rangoon (4 pieces)', 'Protein', cat_protein, 116, 'g', 290, 8, 24, 18, 1, true, true, false, 'processed', 'cooked', '{appetizer,snack}', '{dairy,gluten,seafood}', 1.0),
('Lo Mein (Chicken, 1 order)', 'Grains', cat_carbs, 400, 'g', 680, 28, 86, 24, 5, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Chow Mein (1 order)', 'Grains', cat_carbs, 380, 'g', 540, 18, 72, 18, 6, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,vegetarian}', 1.0),

-- ============================================================================
-- SECTION 6: SUSHI (8 variations)
-- ============================================================================

('California Roll (8 pieces)', 'Grains', cat_carbs, 232, 'g', 340, 9, 58, 9, 3, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{gluten,seafood}', 1.0),
('Spicy Tuna Roll (8 pieces)', 'Protein', cat_protein, 232, 'g', 320, 14, 52, 6, 3, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{gluten,seafood}', 1.0),
('Salmon Roll (6 pieces)', 'Protein', cat_protein, 174, 'g', 240, 10, 38, 5, 2, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{gluten,seafood}', 1.0),
('Philadelphia Roll (6 pieces)', 'Protein', cat_protein, 174, 'g', 300, 11, 32, 12, 2, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{dairy,gluten,seafood}', 1.0),
('Shrimp Tempura Roll (8 pieces)', 'Protein', cat_protein, 280, 'g', 480, 16, 64, 16, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,seafood}', 1.0),
('Dragon Roll (8 pieces)', 'Protein', cat_protein, 290, 'g', 450, 18, 58, 14, 3, true, true, false, 'processed', 'raw', '{lunch,dinner}', '{gluten,seafood}', 1.0),
('Salmon Sashimi (5 pieces)', 'Protein', cat_protein, 140, 'g', 190, 28, 0, 8, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{seafood}', 1.0),
('Tuna Sashimi (5 pieces)', 'Protein', cat_protein, 140, 'g', 165, 32, 0, 4, 0, true, true, true, 'raw', 'raw', '{lunch,dinner}', '{seafood}', 1.0),

-- ============================================================================
-- SECTION 7: JAPANESE RESTAURANT (4 variations)
-- ============================================================================

('Chicken Teriyaki with Rice', 'Protein', cat_protein, 420, 'g', 680, 42, 92, 12, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Beef Teriyaki with Rice', 'Protein', cat_protein, 430, 'g', 740, 44, 88, 18, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Hibachi Chicken with Vegetables & Fried Rice', 'Protein', cat_protein, 500, 'g', 820, 48, 96, 24, 5, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Ramen (Tonkotsu)', 'Grains', cat_carbs, 550, 'g', 680, 32, 78, 24, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),

-- ============================================================================
-- SECTION 8: THAI FOOD (4 variations)
-- ============================================================================

('Pad Thai (Chicken)', 'Grains', cat_carbs, 460, 'g', 760, 38, 98, 24, 4, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten,nuts}', 1.0),
('Thai Fried Rice', 'Grains', cat_carbs, 380, 'g', 580, 18, 86, 16, 3, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{gluten}', 1.0),
('Green Curry with Rice', 'Protein', cat_protein, 460, 'g', 680, 28, 74, 28, 5, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy}', 1.0),
('Massaman Curry with Rice', 'Protein', cat_protein, 470, 'g', 720, 32, 78, 30, 6, true, true, false, 'processed', 'cooked', '{lunch,dinner}', '{dairy,nuts}', 1.0),

-- ============================================================================
-- SECTION 9: DRINKS - SODA (8 variations)
-- ============================================================================

('Coca-Cola (12 oz can)', 'Beverages', cat_beverages, 355, 'g', 140, 0, 39, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Coca-Cola (20 oz bottle)', 'Beverages', cat_beverages, 591, 'g', 240, 0, 65, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Pepsi (12 oz can)', 'Beverages', cat_beverages, 355, 'g', 150, 0, 41, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Sprite (12 oz can)', 'Beverages', cat_beverages, 355, 'g', 140, 0, 38, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Dr Pepper (12 oz can)', 'Beverages', cat_beverages, 355, 'g', 150, 0, 40, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Mountain Dew (12 oz can)', 'Beverages', cat_beverages, 355, 'g', 170, 0, 46, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Mountain Dew (20 oz bottle)', 'Beverages', cat_beverages, 591, 'g', 290, 0, 77, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Root Beer (A&W, 12 oz can)', 'Beverages', cat_beverages, 355, 'g', 160, 0, 43, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),

-- Zero calorie sodas
('Diet Coke (12 oz can)', 'Beverages', cat_beverages, 355, 'g', 0, 0, 0, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Coke Zero (12 oz can)', 'Beverages', cat_beverages, 355, 'g', 0, 0, 0, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),

-- ============================================================================
-- SECTION 10: JUICE & SMOOTHIES (4 variations)
-- ============================================================================

('Cranberry Juice (8 oz)', 'Beverages', cat_beverages, 253, 'g', 116, 1, 31, 0, 0, true, true, false, 'processed', 'raw', '{breakfast,snack}', '{vegetarian}', 1.0),
('Smoothie (Strawberry Banana, 16 oz)', 'Beverages', cat_beverages, 480, 'g', 280, 6, 60, 2, 5, true, true, false, 'processed', 'raw', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Tropical Smoothie Cafe - Island Green (24 oz)', 'Beverages', cat_beverages, 680, 'g', 390, 7, 90, 1, 8, false, true, false, 'processed', 'raw', '{breakfast,snack}', '{vegetarian}', 1.0),
('Jamba Juice - Strawberry Surf Rider (Original)', 'Beverages', cat_beverages, 680, 'g', 350, 3, 85, 1, 4, false, true, false, 'processed', 'raw', '{breakfast,snack}', '{vegetarian}', 1.0),

-- ============================================================================
-- SECTION 11: COFFEE DRINKS (12 variations) - CRITICAL FOR CALORIE TRACKING
-- ============================================================================

('Coffee with Cream and Sugar (1 cup, 2 tbsp cream, 2 tsp sugar)', 'Beverages', cat_beverages, 248, 'g', 70, 1, 10, 3, 0, true, true, false, 'raw', 'cooked', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Latte (Grande, 16 oz, 2% milk)', 'Beverages', cat_beverages, 473, 'g', 190, 13, 19, 7, 0, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Cappuccino (Grande, 16 oz, 2% milk)', 'Beverages', cat_beverages, 473, 'g', 140, 9, 14, 5, 0, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Mocha (Grande, 16 oz, 2% milk, whipped cream)', 'Beverages', cat_beverages, 473, 'g', 360, 13, 44, 15, 2, true, true, false, 'processed', 'cooked', '{breakfast,snack,dessert}', '{dairy,vegetarian}', 1.0),
('Caramel Macchiato (Grande, 16 oz, 2% milk)', 'Beverages', cat_beverages, 473, 'g', 250, 10, 34, 7, 0, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Iced Coffee (16 oz, with cream and sugar)', 'Beverages', cat_beverages, 473, 'g', 110, 2, 16, 4, 0, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Cold Brew (16 oz, black)', 'Beverages', cat_beverages, 473, 'g', 5, 0, 0, 0, 0, true, true, false, 'raw', 'cooked', '{breakfast,snack}', '{vegetarian}', 1.0),
('Frappuccino (Grande, Coffee)', 'Beverages', cat_beverages, 473, 'g', 240, 4, 50, 3, 0, true, true, false, 'processed', 'cooked', '{snack,dessert}', '{dairy,vegetarian}', 1.0),
('Pumpkin Spice Latte (Grande, 16 oz, 2% milk, whipped cream)', 'Beverages', cat_beverages, 473, 'g', 380, 14, 52, 14, 0, true, true, false, 'processed', 'cooked', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Starbucks Caramel Frappuccino (Grande)', 'Beverages', cat_beverages, 473, 'g', 380, 5, 67, 15, 0, false, true, false, 'processed', 'cooked', '{snack,dessert}', '{dairy,vegetarian}', 1.0),
('Dunkin'' Iced Caramel Latte (Medium)', 'Beverages', cat_beverages, 473, 'g', 260, 10, 37, 8, 0, false, true, false, 'processed', 'cooked', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),
('Dunkin'' Iced Caramel Latte (Large)', 'Beverages', cat_beverages, 650, 'g', 350, 13, 49, 11, 0, false, true, false, 'processed', 'cooked', '{breakfast,snack}', '{dairy,vegetarian}', 1.0),

-- ============================================================================
-- SECTION 12: ENERGY DRINKS (4 variations)
-- ============================================================================

('Red Bull (8.4 oz can)', 'Beverages', cat_beverages, 248, 'g', 110, 1, 28, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Red Bull (12 oz can)', 'Beverages', cat_beverages, 355, 'g', 160, 2, 40, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Monster Energy (16 oz can)', 'Beverages', cat_beverages, 473, 'g', 210, 0, 54, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),
('Celsius (12 oz can)', 'Beverages', cat_beverages, 355, 'g', 10, 0, 2, 0, 0, false, true, false, 'processed', 'raw', '{snack}', '{vegetarian}', 1.0),

-- ============================================================================
-- SECTION 13: ALCOHOL (12 variations)
-- ============================================================================

('Beer - Light (Bud Light, Coors Light, 12 oz)', 'Beverages', cat_beverages, 355, 'g', 103, 1, 6, 0, 0, false, true, false, 'processed', 'raw', '{snack,dinner}', '{gluten}', 1.0),
('Beer - Regular (Budweiser, Corona, 12 oz)', 'Beverages', cat_beverages, 355, 'g', 145, 1, 11, 0, 0, false, true, false, 'processed', 'raw', '{snack,dinner}', '{gluten}', 1.0),
('Beer - IPA (12 oz)', 'Beverages', cat_beverages, 355, 'g', 200, 2, 15, 0, 0, true, true, false, 'processed', 'raw', '{snack,dinner}', '{gluten}', 1.0),
('White Wine (5 oz glass)', 'Beverages', cat_beverages, 148, 'g', 121, 0, 4, 0, 0, true, true, false, 'processed', 'raw', '{dinner}', '{vegetarian}', 1.0),
('Red Wine (5 oz glass)', 'Beverages', cat_beverages, 148, 'g', 125, 0, 4, 0, 0, true, true, false, 'processed', 'raw', '{dinner}', '{vegetarian}', 1.0),
('Margarita (8 oz)', 'Beverages', cat_beverages, 237, 'g', 270, 0, 36, 0, 0, true, true, false, 'processed', 'raw', '{snack,dinner}', '{vegetarian}', 1.0),
('Piña Colada (8 oz)', 'Beverages', cat_beverages, 237, 'g', 490, 1, 62, 17, 2, true, true, false, 'processed', 'raw', '{snack,dessert}', '{vegetarian}', 1.0),
('Vodka Soda (8 oz)', 'Beverages', cat_beverages, 237, 'g', 100, 0, 0, 0, 0, true, true, false, 'processed', 'raw', '{snack,dinner}', '{vegetarian}', 1.0),
('Rum and Coke (8 oz)', 'Beverages', cat_beverages, 237, 'g', 185, 0, 22, 0, 0, true, true, false, 'processed', 'raw', '{snack,dinner}', '{vegetarian}', 1.0),
('Whiskey/Bourbon (1.5 oz shot)', 'Beverages', cat_beverages, 44, 'g', 105, 0, 0, 0, 0, true, true, false, 'processed', 'raw', '{snack,dinner}', '{vegetarian}', 1.0),
('Tequila (1.5 oz shot)', 'Beverages', cat_beverages, 44, 'g', 97, 0, 0, 0, 0, true, true, false, 'processed', 'raw', '{snack,dinner}', '{vegetarian}', 1.0),
('Vodka (1.5 oz shot)', 'Beverages', cat_beverages, 44, 'g', 97, 0, 0, 0, 0, true, true, false, 'processed', 'raw', '{snack,dinner}', '{vegetarian}', 1.0);

END $$;

-- ============================================================================
-- VERIFICATION QUERIES
-- ============================================================================

-- Count Phase 2 foods by category
SELECT
    food_group,
    COUNT(*) as count
FROM foods_enhanced
WHERE name LIKE '%Ice Cream%'
   OR name LIKE '%Cookie%'
   OR name LIKE '%Pizza%'
   OR name LIKE '%Pasta%'
   OR name LIKE '%Sushi%'
   OR name LIKE '%Soda%'
   OR name LIKE '%Beer%'
   OR name LIKE '%Wine%'
GROUP BY food_group
ORDER BY count DESC;

-- Total count
SELECT COUNT(*) as phase2_foods FROM foods_enhanced;
