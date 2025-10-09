-- Migration 020: Nutrition Base Schema (Idempotent)
-- Ensures base nutrition tables exist with required columns
-- Safe to run multiple times
-- Created: 2025-10-09

-- Check if foods_enhanced exists, if not create minimal table
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'foods_enhanced') THEN
        CREATE TABLE public.foods_enhanced (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            name TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
    END IF;
END $$;

-- Add missing columns to foods_enhanced
ALTER TABLE public.foods_enhanced
    ADD COLUMN IF NOT EXISTS brand TEXT,
    ADD COLUMN IF NOT EXISTS barcode TEXT,
    ADD COLUMN IF NOT EXISTS serving_size NUMERIC DEFAULT 100,
    ADD COLUMN IF NOT EXISTS serving_unit TEXT DEFAULT 'g',
    ADD COLUMN IF NOT EXISTS calories NUMERIC DEFAULT 0,
    ADD COLUMN IF NOT EXISTS protein_g NUMERIC DEFAULT 0,
    ADD COLUMN IF NOT EXISTS total_carbs_g NUMERIC DEFAULT 0,
    ADD COLUMN IF NOT EXISTS total_fat_g NUMERIC DEFAULT 0,
    ADD COLUMN IF NOT EXISTS dietary_fiber_g NUMERIC DEFAULT 0,
    ADD COLUMN IF NOT EXISTS total_sugars_g NUMERIC DEFAULT 0,
    ADD COLUMN IF NOT EXISTS sodium_mg NUMERIC DEFAULT 0,
    ADD COLUMN IF NOT EXISTS created_by UUID REFERENCES auth.users(id),
    ADD COLUMN IF NOT EXISTS is_verified BOOLEAN DEFAULT FALSE,
    ADD COLUMN IF NOT EXISTS is_public BOOLEAN DEFAULT FALSE;

-- Enable RLS if not already enabled
ALTER TABLE public.foods_enhanced ENABLE ROW LEVEL SECURITY;

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_foods_enhanced_name ON public.foods_enhanced(name);
CREATE INDEX IF NOT EXISTS idx_foods_enhanced_created_by ON public.foods_enhanced(created_by) WHERE created_by IS NOT NULL;

-- RLS policies
DROP POLICY IF EXISTS "Users can view public foods" ON public.foods_enhanced;
CREATE POLICY "Users can view public foods" ON public.foods_enhanced FOR SELECT
USING (is_public = TRUE OR created_by = auth.uid());

DROP POLICY IF EXISTS "Users can create own foods" ON public.foods_enhanced;
CREATE POLICY "Users can create own foods" ON public.foods_enhanced FOR INSERT
WITH CHECK (created_by = auth.uid());

-- Meal logs table
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'meal_logs') THEN
        CREATE TABLE public.meal_logs (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
            name TEXT,
            category TEXT NOT NULL DEFAULT 'other',
            logged_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
            notes TEXT,
            total_calories NUMERIC DEFAULT 0,
            total_protein_g NUMERIC DEFAULT 0,
            total_carbs_g NUMERIC DEFAULT 0,
            total_fat_g NUMERIC DEFAULT 0,
            total_fiber_g NUMERIC DEFAULT 0,
            source TEXT DEFAULT 'manual',
            estimated BOOLEAN DEFAULT FALSE,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
    END IF;
END $$;

ALTER TABLE public.meal_logs ENABLE ROW LEVEL SECURITY;
CREATE INDEX IF NOT EXISTS idx_meal_logs_user_id ON public.meal_logs(user_id);

DROP POLICY IF EXISTS "Users can view own meal logs" ON public.meal_logs;
CREATE POLICY "Users can view own meal logs" ON public.meal_logs FOR SELECT USING (user_id = auth.uid());

-- Meal foods table
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'meal_foods') THEN
        CREATE TABLE public.meal_foods (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            meal_log_id UUID NOT NULL REFERENCES public.meal_logs(id) ON DELETE CASCADE,
            food_id UUID NOT NULL REFERENCES public.foods_enhanced(id) ON DELETE CASCADE,
            quantity NUMERIC NOT NULL,
            unit TEXT NOT NULL,
            calories NUMERIC DEFAULT 0,
            protein_g NUMERIC DEFAULT 0,
            carbs_g NUMERIC DEFAULT 0,
            fat_g NUMERIC DEFAULT 0,
            fiber_g NUMERIC DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    END IF;
END $$;

ALTER TABLE public.meal_foods ENABLE ROW LEVEL SECURITY;
CREATE INDEX IF NOT EXISTS idx_meal_foods_meal_log_id ON public.meal_foods(meal_log_id);

-- Meal templates table
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'meal_templates') THEN
        CREATE TABLE public.meal_templates (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
            name TEXT NOT NULL,
            category TEXT NOT NULL DEFAULT 'other',
            description TEXT,
            total_calories NUMERIC DEFAULT 0,
            total_protein_g NUMERIC DEFAULT 0,
            total_carbs_g NUMERIC DEFAULT 0,
            total_fat_g NUMERIC DEFAULT 0,
            total_fiber_g NUMERIC DEFAULT 0,
            created_at TIMESTAMPTZ DEFAULT NOW(),
            updated_at TIMESTAMPTZ DEFAULT NOW()
        );
    END IF;
END $$;

ALTER TABLE public.meal_templates ENABLE ROW LEVEL SECURITY;
CREATE INDEX IF NOT EXISTS idx_meal_templates_user_id ON public.meal_templates(user_id);

DROP POLICY IF EXISTS "Users can view own templates" ON public.meal_templates;
CREATE POLICY "Users can view own templates" ON public.meal_templates FOR SELECT USING (user_id = auth.uid());

-- Meal template foods table
DO $$ 
BEGIN
    IF NOT EXISTS (SELECT FROM pg_tables WHERE schemaname = 'public' AND tablename = 'meal_template_foods') THEN
        CREATE TABLE public.meal_template_foods (
            id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
            meal_template_id UUID NOT NULL REFERENCES public.meal_templates(id) ON DELETE CASCADE,
            food_id UUID NOT NULL REFERENCES public.foods_enhanced(id) ON DELETE CASCADE,
            quantity NUMERIC NOT NULL,
            unit TEXT NOT NULL,
            created_at TIMESTAMPTZ DEFAULT NOW()
        );
    END IF;
END $$;

ALTER TABLE public.meal_template_foods ENABLE ROW LEVEL SECURITY;
CREATE INDEX IF NOT EXISTS idx_meal_template_foods_template_id ON public.meal_template_foods(meal_template_id);

-- Unit conversion function
CREATE OR REPLACE FUNCTION convert_to_base_unit(quantity NUMERIC, from_unit TEXT, to_unit TEXT)
RETURNS NUMERIC AS $$
BEGIN
    IF from_unit = to_unit THEN RETURN quantity; END IF;
    CASE from_unit
        WHEN 'oz' THEN quantity := quantity * 28.35;
        WHEN 'lb' THEN quantity := quantity * 453.592;
        WHEN 'cup' THEN quantity := quantity * 240;
        WHEN 'tbsp' THEN quantity := quantity * 15;
        WHEN 'tsp' THEN quantity := quantity * 5;
        ELSE quantity := quantity;
    END CASE;
    CASE to_unit
        WHEN 'g' THEN RETURN quantity;
        WHEN 'oz' THEN RETURN quantity / 28.35;
        ELSE RETURN quantity;
    END CASE;
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Migration complete
COMMENT ON TABLE foods_enhanced IS 'Enhanced food database with nutrition';
COMMENT ON TABLE meal_logs IS 'User meal logs';
COMMENT ON TABLE meal_templates IS 'Reusable meal templates';
