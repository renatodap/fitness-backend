-- ============================================================================
-- MIGRATION 025: SEED BRAZILIAN PROTEINS (PROTEÍNAS)
-- ============================================================================
-- Description: Common proteins in Brazil with Portuguese names
-- Total items: ~50 items
-- Categories: Carnes, Aves, Peixes, Embutidos, Ovos
-- ============================================================================

BEGIN;

INSERT INTO foods (
    name, food_type, description,
    serving_size, serving_unit, household_serving_unit, household_serving_grams,
    calories, protein_g, total_carbs_g, total_fat_g,
    dietary_fiber_g, total_sugars_g, saturated_fat_g, cholesterol_mg,
    sodium_mg, potassium_mg, calcium_mg, iron_mg,
    allergens, dietary_flags, source, data_quality_score, verified
) VALUES

-- CARNES BOVINAS (BEEF)
('Picanha', 'ingredient', 'Brazilian top sirloin cap',
    100, 'g', 'fatia (140g)', 140,
    206, 26, 0, 11,
    0, 0, 4.5, 75,
    60, 370, 18, 2.5,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.94, false),

('Contra-filé', 'ingredient', 'Brazilian sirloin steak',
    100, 'g', 'bife (150g)', 150,
    183, 27, 0, 8,
    0, 0, 3.2, 73,
    58, 380, 16, 2.3,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.94, false),

('Filé Mignon', 'ingredient', 'Beef tenderloin',
    100, 'g', 'medalhão (120g)', 120,
    158, 28.5, 0, 4.5,
    0, 0, 1.8, 75,
    55, 395, 14, 2.4,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.95, false),

('Coxão Mole', 'ingredient', 'Brazilian bottom round',
    100, 'g', 'fatia (120g)', 120,
    143, 27.2, 0, 3.5,
    0, 0, 1.3, 70,
    56, 385, 15, 2.6,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.94, false),

('Coxão Duro', 'ingredient', 'Brazilian eye of round',
    100, 'g', 'fatia (120g)', 120,
    135, 28, 0, 2.8,
    0, 0, 1.1, 68,
    54, 390, 14, 2.7,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.94, false),

('Patinho', 'ingredient', 'Brazilian knuckle steak',
    100, 'g', 'fatia (120g)', 120,
    140, 27.5, 0, 3.2,
    0, 0, 1.2, 69,
    55, 387, 14, 2.5,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.94, false),

('Músculo Bovino', 'ingredient', 'Beef shank',
    100, 'g', 'pedaço (150g)', 150,
    165, 25, 0, 7,
    0, 0, 2.8, 72,
    62, 340, 16, 2.8,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.93, false),

('Costela Bovina', 'ingredient', 'Beef ribs',
    100, 'g', 'pedaço (200g)', 200,
    290, 19, 0, 24,
    0, 0, 10, 78,
    65, 280, 20, 2.2,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.93, false),

('Carne Moída (Magra)', 'ingredient', 'Lean ground beef',
    100, 'g', 'porção (113g)', 113,
    176, 26, 0, 8,
    0, 0, 3.5, 75,
    68, 350, 16, 2.5,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.95, false),

('Cupim', 'ingredient', 'Brazilian beef hump',
    100, 'g', 'fatia (150g)', 150,
    248, 22, 0, 18,
    0, 0, 7.5, 80,
    70, 300, 18, 2.4,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.92, false),

-- CARNES SUÍNAS (PORK)
('Lombo Suíno', 'ingredient', 'Pork loin',
    100, 'g', 'fatia (120g)', 120,
    143, 25.7, 0, 4.1,
    0, 0, 1.4, 69,
    58, 423, 12, 1.1,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.95, false),

('Bisteca Suína', 'ingredient', 'Pork chop with bone',
    100, 'g', 'bisteca (150g)', 150,
    212, 23, 0, 13,
    0, 0, 4.8, 74,
    62, 380, 16, 1.2,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.94, false),

('Costela Suína', 'ingredient', 'Pork ribs',
    100, 'g', 'pedaço (200g)', 200,
    277, 19.9, 0, 21.2,
    0, 0, 7.8, 78,
    65, 302, 22, 1.3,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.93, false),

('Pernil Suíno', 'ingredient', 'Pork leg',
    100, 'g', 'fatia (120g)', 120,
    182, 24.5, 0, 9,
    0, 0, 3.2, 72,
    60, 360, 14, 1.4,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.93, false),

('Bacon', 'ingredient', 'Bacon strips',
    100, 'g', 'fatias (28g)', 28,
    541, 37, 1.4, 42,
    0, 0, 14, 110,
    1717, 565, 14, 1.4,
    NULL, ARRAY['gluten-free', 'keto'], 'user', 0.95, false),

('Linguiça Toscana', 'ingredient', 'Tuscan-style pork sausage',
    100, 'g', 'linguiça (70g)', 70,
    296, 14, 2, 26,
    0, 0.5, 9.5, 68,
    820, 240, 18, 1.6,
    NULL, ARRAY['gluten-free'], 'user', 0.92, false),

('Linguiça Calabresa', 'ingredient', 'Calabrian sausage',
    100, 'g', 'rodela (60g)', 60,
    308, 13.5, 1.8, 28,
    0, 0.4, 10, 70,
    950, 230, 16, 1.5,
    NULL, ARRAY['gluten-free'], 'user', 0.93, false),

-- AVES (POULTRY)
('Peito de Frango (sem pele)', 'ingredient', 'Skinless chicken breast',
    100, 'g', 'filé (140g)', 140,
    165, 31, 0, 3.6,
    0, 0, 1, 85,
    74, 256, 15, 1.04,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.96, false),

('Coxa de Frango (sem pele)', 'ingredient', 'Skinless chicken thigh',
    100, 'g', 'coxa (90g)', 90,
    177, 24.4, 0, 8.3,
    0, 0, 2.4, 93,
    86, 240, 12, 1.3,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.95, false),

('Sobrecoxa de Frango (sem pele)', 'ingredient', 'Skinless chicken drumstick',
    100, 'g', 'sobrecoxa (110g)', 110,
    172, 25.2, 0, 7.6,
    0, 0, 2.2, 91,
    84, 245, 11, 1.25,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.95, false),

('Frango Inteiro (com pele)', 'ingredient', 'Whole chicken with skin',
    100, 'g', 'pedaço (150g)', 150,
    239, 23.3, 0, 15.8,
    0, 0, 4.5, 88,
    82, 220, 13, 1.2,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.94, false),

('Coração de Frango', 'ingredient', 'Chicken hearts',
    100, 'g', 'porção (85g)', 85,
    153, 26.4, 0.7, 4.8,
    0, 0, 1.3, 242,
    70, 176, 12, 9.08,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.93, false),

('Fígado de Frango', 'ingredient', 'Chicken liver',
    100, 'g', 'porção (85g)', 85,
    119, 16.9, 0.7, 4.8,
    0, 0, 1.6, 345,
    71, 230, 8, 9,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.94, false),

('Peito de Peru', 'ingredient', 'Turkey breast',
    100, 'g', 'fatia (100g)', 100,
    135, 30, 0, 1.7,
    0, 0, 0.5, 70,
    55, 302, 12, 1.4,
    NULL, ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.95, false),

-- PEIXES (FISH)
('Tilápia', 'ingredient', 'Tilapia fillet',
    100, 'g', 'filé (120g)', 120,
    96, 20.1, 0, 1.7,
    0, 0, 0.6, 50,
    52, 302, 10, 0.56,
    ARRAY['fish'], ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.95, false),

('Salmão', 'ingredient', 'Salmon fillet',
    100, 'g', 'filé (150g)', 150,
    208, 20, 0, 13.4,
    0, 0, 3.1, 55,
    59, 363, 9, 0.34,
    ARRAY['fish'], ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.96, false),

('Atum Fresco', 'ingredient', 'Fresh tuna',
    100, 'g', 'postas (120g)', 120,
    144, 23.3, 0, 4.9,
    0, 0, 1.6, 38,
    39, 252, 8, 1.02,
    ARRAY['fish'], ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.95, false),

('Pescada', 'ingredient', 'Hake fish',
    100, 'g', 'filé (120g)', 120,
    86, 17.8, 0, 1.4,
    0, 0, 0.3, 56,
    88, 280, 28, 0.48,
    ARRAY['fish'], ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.93, false),

('Sardinha Fresca', 'ingredient', 'Fresh sardines',
    100, 'g', 'unidade (50g)', 50,
    208, 24.6, 0, 11.5,
    0, 0, 3.3, 142,
    505, 397, 382, 2.92,
    ARRAY['fish'], ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.94, false),

('Merluza', 'ingredient', 'Hake fish',
    100, 'g', 'filé (120g)', 120,
    90, 18.4, 0, 1.8,
    0, 0, 0.4, 58,
    86, 285, 30, 0.52,
    ARRAY['fish'], ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.93, false),

('Bacalhau Fresco', 'ingredient', 'Fresh cod',
    100, 'g', 'pedaço (120g)', 120,
    82, 17.8, 0, 0.7,
    0, 0, 0.1, 43,
    54, 413, 16, 0.38,
    ARRAY['fish'], ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.94, false),

('Bacalhau Salgado (dessalgado)', 'ingredient', 'Desalted salt cod',
    100, 'g', 'pedaço (100g)', 100,
    290, 62.8, 0, 2.4,
    0, 0, 0.6, 160,
    7027, 950, 160, 2.5,
    ARRAY['fish'], ARRAY['gluten-free', 'keto'], 'user', 0.92, false),

-- FRUTOS DO MAR (SEAFOOD)
('Camarão', 'ingredient', 'Shrimp',
    100, 'g', 'porção (85g)', 85,
    99, 24, 0.2, 0.3,
    0, 0, 0.1, 189,
    111, 259, 70, 0.51,
    ARRAY['shellfish'], ARRAY['gluten-free', 'keto', 'paleo'], 'user', 0.95, false),

('Lula', 'ingredient', 'Squid',
    100, 'g', 'porção (85g)', 85,
    92, 15.6, 3.1, 1.4,
    0, 0, 0.4, 233,
    44, 246, 32, 0.68,
    ARRAY['shellfish'], ARRAY['gluten-free', 'keto'], 'user', 0.93, false),

('Polvo', 'ingredient', 'Octopus',
    100, 'g', 'pedaço (100g)', 100,
    82, 14.9, 2.2, 1,
    0, 0, 0.3, 48,
    230, 350, 53, 5.3,
    ARRAY['shellfish'], ARRAY['gluten-free', 'keto'], 'user', 0.92, false),

-- EMBUTIDOS (COLD CUTS)
('Presunto Cozido', 'ingredient', 'Cooked ham',
    100, 'g', 'fatia (28g)', 28,
    145, 18.6, 1.5, 6.3,
    0, 1.3, 2.1, 53,
    1203, 287, 7, 0.91,
    ARRAY['soy'], ARRAY['gluten-free'], 'user', 0.94, false),

('Presunto Parma', 'ingredient', 'Parma ham',
    100, 'g', 'fatia (28g)', 28,
    250, 24, 0, 16,
    0, 0, 5.5, 65,
    2340, 340, 10, 1.2,
    NULL, ARRAY['gluten-free', 'keto'], 'user', 0.93, false),

('Mortadela', 'ingredient', 'Bologna',
    100, 'g', 'fatia (28g)', 28,
    311, 11.7, 3.9, 28.5,
    0, 0.8, 10.5, 62,
    1329, 180, 62, 1.5,
    ARRAY['soy'], NULL, 'user', 0.93, false),

('Salame', 'ingredient', 'Salami',
    100, 'g', 'fatia (28g)', 28,
    407, 23.8, 2, 33.7,
    0, 0.3, 11.9, 79,
    2260, 378, 13, 1.78,
    NULL, ARRAY['gluten-free', 'keto'], 'user', 0.94, false),

('Peito de Peru Defumado', 'ingredient', 'Smoked turkey breast',
    100, 'g', 'fatia (28g)', 28,
    104, 17.5, 3.5, 2,
    0, 2, 0.5, 40,
    1050, 302, 12, 1.2,
    ARRAY['soy'], ARRAY['gluten-free'], 'user', 0.93, false),

('Blanquet de Peru', 'ingredient', 'Turkey blanquet',
    100, 'g', 'fatia (28g)', 28,
    112, 16.8, 3.2, 3.5,
    0, 2.5, 1, 38,
    980, 285, 11, 1.1,
    ARRAY['soy'], NULL, 'user', 0.92, false),

('Apresuntado', 'ingredient', 'Pressed ham loaf',
    100, 'g', 'fatia (28g)', 28,
    168, 15.4, 5.6, 9.8,
    0, 3.2, 3.5, 48,
    1156, 260, 18, 1.3,
    ARRAY['soy'], NULL, 'user', 0.91, false),

-- OVOS (EGGS)
('Ovo de Galinha (Inteiro)', 'ingredient', 'Whole chicken egg',
    100, 'g', 'ovo (50g)', 50,
    143, 12.6, 0.7, 9.5,
    0, 0.4, 3.1, 372,
    124, 126, 50, 1.75,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free', 'keto', 'paleo'], 'user', 0.96, false),

('Clara de Ovo', 'ingredient', 'Egg white',
    100, 'g', 'clara (33g)', 33,
    52, 10.9, 0.7, 0.2,
    0, 0.7, 0, 0,
    166, 163, 7, 0.08,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free', 'keto', 'paleo'], 'user', 0.96, false),

('Gema de Ovo', 'ingredient', 'Egg yolk',
    100, 'g', 'gema (17g)', 17,
    322, 15.9, 3.6, 26.5,
    0, 0.6, 9.6, 1085,
    48, 109, 129, 2.73,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free', 'keto'], 'user', 0.96, false),

('Ovo de Codorna', 'ingredient', 'Quail egg',
    100, 'g', '5 ovos (50g)', 50,
    158, 13.1, 0.4, 11.1,
    0, 0.4, 3.6, 844,
    141, 132, 64, 3.65,
    ARRAY['eggs'], ARRAY['vegetarian', 'gluten-free', 'keto', 'paleo'], 'user', 0.94, false);

COMMIT;

SELECT '✅ BRAZILIAN PROTEINS SEEDED!' as status, COUNT(*) as total_items
FROM foods WHERE name IN ('Picanha', 'Peito de Frango (sem pele)', 'Tilápia', 'Presunto Cozido');
