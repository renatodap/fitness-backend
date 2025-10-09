-- Migration 021: Recursive Meal Templates System
-- Enables templates to contain other templates and be used in logged meals
-- Depends on: 020_nutrition_base_schema.sql
-- Created: 2025-10-09

-- ============================================================================
-- PART 1: UPDATE meal_template_foods TO SUPPORT NESTED TEMPLATES
-- ============================================================================

-- Make food_id nullable (since items can be templates instead of foods)
ALTER TABLE public.meal_template_foods
  ALTER COLUMN food_id DROP NOT NULL;

-- Add columns for nested template support
ALTER TABLE public.meal_template_foods
  ADD COLUMN IF NOT EXISTS child_template_id UUID REFERENCES public.meal_templates(id) ON DELETE CASCADE,
  ADD COLUMN IF NOT EXISTS item_type TEXT NOT NULL DEFAULT 'food',
  ADD COLUMN IF NOT EXISTS order_index INTEGER DEFAULT 0;

-- Add check constraint for item_type
ALTER TABLE public.meal_template_foods
  DROP CONSTRAINT IF EXISTS meal_template_foods_item_type_check,
  ADD CONSTRAINT meal_template_foods_item_type_check
    CHECK (item_type IN ('food', 'template'));

-- Add constraint: must have either food_id OR child_template_id, not both
ALTER TABLE public.meal_template_foods
  DROP CONSTRAINT IF EXISTS meal_template_foods_item_check,
  ADD CONSTRAINT meal_template_foods_item_check CHECK (
    (item_type = 'food' AND food_id IS NOT NULL AND child_template_id IS NULL) OR
    (item_type = 'template' AND child_template_id IS NOT NULL AND food_id IS NULL)
  );

-- ============================================================================
-- PART 2: UPDATE meal_foods TO SUPPORT TEMPLATES IN LOGGED MEALS
-- ============================================================================

-- Make food_id nullable (since items can be templates)
ALTER TABLE public.meal_foods
  ALTER COLUMN food_id DROP NOT NULL;

-- Add columns for template support
ALTER TABLE public.meal_foods
  ADD COLUMN IF NOT EXISTS template_id UUID REFERENCES public.meal_templates(id),
  ADD COLUMN IF NOT EXISTS item_type TEXT DEFAULT 'food',
  ADD COLUMN IF NOT EXISTS order_index INTEGER DEFAULT 0;

-- Add check constraint for item_type
ALTER TABLE public.meal_foods
  DROP CONSTRAINT IF EXISTS meal_foods_item_type_check,
  ADD CONSTRAINT meal_foods_item_type_check
    CHECK (item_type IN ('food', 'template'));

-- Add constraint: must have either food_id OR template_id, not both
ALTER TABLE public.meal_foods
  DROP CONSTRAINT IF EXISTS meal_foods_item_check,
  ADD CONSTRAINT meal_foods_item_check CHECK (
    (item_type = 'food' AND food_id IS NOT NULL AND template_id IS NULL) OR
    (item_type = 'template' AND template_id IS NOT NULL AND food_id IS NULL)
  );

-- ============================================================================
-- PART 3: ENHANCE meal_templates WITH TRACKING & FAVORITES
-- ============================================================================

-- Add tracking columns
ALTER TABLE public.meal_templates
  ADD COLUMN IF NOT EXISTS is_favorite BOOLEAN DEFAULT false,
  ADD COLUMN IF NOT EXISTS use_count INTEGER DEFAULT 0,
  ADD COLUMN IF NOT EXISTS last_used_at TIMESTAMPTZ,
  ADD COLUMN IF NOT EXISTS tags TEXT[] DEFAULT ARRAY[]::text[];

-- ============================================================================
-- PART 4: ADD TEMPLATE TRACKING TO meal_logs
-- ============================================================================

-- Track which template was used to create a logged meal
ALTER TABLE public.meal_logs
  ADD COLUMN IF NOT EXISTS template_id UUID REFERENCES public.meal_templates(id),
  ADD COLUMN IF NOT EXISTS created_from_template BOOLEAN DEFAULT false;

-- ============================================================================
-- PART 5: CIRCULAR REFERENCE PREVENTION FUNCTION
-- ============================================================================

-- Function to check if adding a template would create a circular reference
CREATE OR REPLACE FUNCTION public.check_template_circular_reference(
    p_parent_template_id UUID,
    p_child_template_id UUID
)
RETURNS BOOLEAN AS $$
DECLARE
    v_visited UUID[];
    v_current UUID;
    v_children UUID[];
    v_child UUID;
BEGIN
    -- Can't reference self
    IF p_parent_template_id = p_child_template_id THEN
        RETURN TRUE;
    END IF;

    -- Initialize with the child we want to add
    v_visited := ARRAY[p_child_template_id];
    v_children := ARRAY[p_child_template_id];

    -- Traverse the tree depth-first
    WHILE array_length(v_children, 1) > 0 LOOP
        v_current := v_children[1];
        v_children := v_children[2:array_length(v_children, 1)];

        -- Get all child templates of current template
        FOR v_child IN
            SELECT child_template_id
            FROM public.meal_template_foods
            WHERE meal_template_id = v_current
            AND item_type = 'template'
            AND child_template_id IS NOT NULL
        LOOP
            -- If we find the parent in the children, it's circular
            IF v_child = p_parent_template_id THEN
                RETURN TRUE;
            END IF;

            -- If not visited, add to queue
            IF NOT (v_child = ANY(v_visited)) THEN
                v_visited := array_append(v_visited, v_child);
                v_children := array_append(v_children, v_child);
            END IF;
        END LOOP;
    END LOOP;

    RETURN FALSE;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- ============================================================================
-- PART 6: RECURSIVE NUTRITION CALCULATION FUNCTION
-- ============================================================================

-- Function to calculate total nutrition for a template (including nested templates)
CREATE OR REPLACE FUNCTION public.calculate_template_nutrition(
    p_template_id UUID
)
RETURNS JSONB AS $$
DECLARE
    v_result JSONB;
    v_total_calories NUMERIC := 0;
    v_total_protein NUMERIC := 0;
    v_total_carbs NUMERIC := 0;
    v_total_fat NUMERIC := 0;
    v_total_fiber NUMERIC := 0;
    v_total_sugar NUMERIC := 0;
    v_total_sodium NUMERIC := 0;
    v_item RECORD;
    v_food RECORD;
    v_child_nutrition JSONB;
    v_multiplier NUMERIC;
BEGIN
    -- Loop through all items in the template
    FOR v_item IN
        SELECT
            item_type,
            food_id,
            child_template_id,
            quantity,
            unit
        FROM public.meal_template_foods
        WHERE meal_template_id = p_template_id
    LOOP
        IF v_item.item_type = 'food' THEN
            -- Calculate nutrition from food
            SELECT
                calories,
                protein_g,
                carbs_g,
                fat_g,
                fiber_g,
                sugar_g,
                sodium_mg,
                serving_size,
                serving_unit
            INTO v_food
            FROM public.foods_enhanced
            WHERE id = v_item.food_id;

            IF v_food IS NOT NULL THEN
                -- Calculate multiplier based on quantity and serving size
                v_multiplier := v_item.quantity / NULLIF(v_food.serving_size, 0);

                v_total_calories := v_total_calories + (COALESCE(v_food.calories, 0) * v_multiplier);
                v_total_protein := v_total_protein + (COALESCE(v_food.protein_g, 0) * v_multiplier);
                v_total_carbs := v_total_carbs + (COALESCE(v_food.carbs_g, 0) * v_multiplier);
                v_total_fat := v_total_fat + (COALESCE(v_food.fat_g, 0) * v_multiplier);
                v_total_fiber := v_total_fiber + (COALESCE(v_food.fiber_g, 0) * v_multiplier);
                v_total_sugar := v_total_sugar + (COALESCE(v_food.sugar_g, 0) * v_multiplier);
                v_total_sodium := v_total_sodium + (COALESCE(v_food.sodium_mg, 0) * v_multiplier);
            END IF;

        ELSIF v_item.item_type = 'template' THEN
            -- Recursively calculate nutrition from child template
            v_child_nutrition := public.calculate_template_nutrition(v_item.child_template_id);

            -- Add child template's nutrition (multiplied by quantity if needed)
            v_total_calories := v_total_calories + (v_child_nutrition->>'total_calories')::NUMERIC;
            v_total_protein := v_total_protein + (v_child_nutrition->>'total_protein_g')::NUMERIC;
            v_total_carbs := v_total_carbs + (v_child_nutrition->>'total_carbs_g')::NUMERIC;
            v_total_fat := v_total_fat + (v_child_nutrition->>'total_fat_g')::NUMERIC;
            v_total_fiber := v_total_fiber + (v_child_nutrition->>'total_fiber_g')::NUMERIC;
            v_total_sugar := v_total_sugar + (v_child_nutrition->>'total_sugar_g')::NUMERIC;
            v_total_sodium := v_total_sodium + (v_child_nutrition->>'total_sodium_mg')::NUMERIC;
        END IF;
    END LOOP;

    -- Return as JSONB
    v_result := jsonb_build_object(
        'total_calories', ROUND(v_total_calories, 2),
        'total_protein_g', ROUND(v_total_protein, 2),
        'total_carbs_g', ROUND(v_total_carbs, 2),
        'total_fat_g', ROUND(v_total_fat, 2),
        'total_fiber_g', ROUND(v_total_fiber, 2),
        'total_sugar_g', ROUND(v_total_sugar, 2),
        'total_sodium_mg', ROUND(v_total_sodium, 2)
    );

    RETURN v_result;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- ============================================================================
-- PART 7: FLATTEN TEMPLATE FUNCTION (EXPAND ALL NESTED TEMPLATES)
-- ============================================================================

-- Function to flatten a template into individual foods (resolving all nesting)
CREATE OR REPLACE FUNCTION public.flatten_template(
    p_template_id UUID
)
RETURNS TABLE (
    food_id UUID,
    quantity NUMERIC,
    unit TEXT,
    calories NUMERIC,
    protein_g NUMERIC,
    carbs_g NUMERIC,
    fat_g NUMERIC,
    fiber_g NUMERIC
) AS $$
DECLARE
    v_item RECORD;
    v_child_food RECORD;
BEGIN
    -- Loop through all items in the template
    FOR v_item IN
        SELECT
            mtf.item_type,
            mtf.food_id,
            mtf.child_template_id,
            mtf.quantity,
            mtf.unit
        FROM public.meal_template_foods mtf
        WHERE mtf.meal_template_id = p_template_id
    LOOP
        IF v_item.item_type = 'food' THEN
            -- Return food directly
            RETURN QUERY
            SELECT
                v_item.food_id,
                v_item.quantity,
                v_item.unit::TEXT,
                (v_item.quantity / NULLIF(f.serving_size, 0)) * COALESCE(f.calories, 0),
                (v_item.quantity / NULLIF(f.serving_size, 0)) * COALESCE(f.protein_g, 0),
                (v_item.quantity / NULLIF(f.serving_size, 0)) * COALESCE(f.total_carbs_g, 0),
                (v_item.quantity / NULLIF(f.serving_size, 0)) * COALESCE(f.total_fat_g, 0),
                (v_item.quantity / NULLIF(f.serving_size, 0)) * COALESCE(f.dietary_fiber_g, 0)
            FROM public.foods_enhanced f
            WHERE f.id = v_item.food_id;

        ELSIF v_item.item_type = 'template' THEN
            -- Recursively flatten child template
            RETURN QUERY
            SELECT * FROM public.flatten_template(v_item.child_template_id);
        END IF;
    END LOOP;

    RETURN;
END;
$$ LANGUAGE plpgsql STABLE SECURITY DEFINER;

-- ============================================================================
-- PART 8: CREATE MEAL FROM TEMPLATE FUNCTION
-- ============================================================================

-- Function to create a meal_log from a template
CREATE OR REPLACE FUNCTION public.create_meal_from_template(
    p_user_id UUID,
    p_template_id UUID,
    p_logged_at TIMESTAMPTZ DEFAULT NOW()
)
RETURNS UUID AS $$
DECLARE
    v_meal_log_id UUID;
    v_template RECORD;
    v_nutrition JSONB;
    v_item RECORD;
BEGIN
    -- Get template details
    SELECT
        name,
        category
    INTO v_template
    FROM public.meal_templates
    WHERE id = p_template_id
    AND user_id = p_user_id;

    IF v_template IS NULL THEN
        RAISE EXCEPTION 'Template not found or does not belong to user';
    END IF;

    -- Calculate nutrition
    v_nutrition := public.calculate_template_nutrition(p_template_id);

    -- Create meal_log
    INSERT INTO public.meal_logs (
        user_id,
        name,
        category,
        logged_at,
        template_id,
        created_from_template,
        total_calories,
        total_protein_g,
        total_carbs_g,
        total_fat_g,
        total_fiber_g,
        total_sugar_g,
        total_sodium_mg
    ) VALUES (
        p_user_id,
        v_template.name,
        v_template.category,
        p_logged_at,
        p_template_id,
        true,
        (v_nutrition->>'total_calories')::NUMERIC,
        (v_nutrition->>'total_protein_g')::NUMERIC,
        (v_nutrition->>'total_carbs_g')::NUMERIC,
        (v_nutrition->>'total_fat_g')::NUMERIC,
        (v_nutrition->>'total_fiber_g')::NUMERIC,
        (v_nutrition->>'total_sugar_g')::NUMERIC,
        (v_nutrition->>'total_sodium_mg')::NUMERIC
    )
    RETURNING id INTO v_meal_log_id;

    -- Copy all items from template to meal_foods (flattened)
    FOR v_item IN
        SELECT * FROM public.flatten_template(p_template_id)
    LOOP
        INSERT INTO public.meal_foods (
            meal_log_id,
            food_id,
            item_type,
            quantity,
            unit,
            calories,
            protein_g,
            carbs_g,
            fat_g,
            fiber_g
        ) VALUES (
            v_meal_log_id,
            v_item.food_id,
            'food',
            v_item.quantity,
            v_item.unit,
            v_item.calories,
            v_item.protein_g,
            v_item.carbs_g,
            v_item.fat_g,
            v_item.fiber_g
        );
    END LOOP;

    -- Update template usage stats
    UPDATE public.meal_templates
    SET
        use_count = use_count + 1,
        last_used_at = NOW()
    WHERE id = p_template_id;

    RETURN v_meal_log_id;
END;
$$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;

-- ============================================================================
-- PART 9: TRIGGER TO AUTO-UPDATE TEMPLATE NUTRITION
-- ============================================================================

-- Function to update template nutrition totals when items change
CREATE OR REPLACE FUNCTION public.update_template_nutrition()
RETURNS TRIGGER AS $$
DECLARE
    v_nutrition JSONB;
    v_template_id UUID;
BEGIN
    -- Get template_id from the row
    IF TG_OP = 'DELETE' THEN
        v_template_id := OLD.meal_template_id;
    ELSE
        v_template_id := NEW.meal_template_id;
    END IF;

    -- Recalculate nutrition
    v_nutrition := public.calculate_template_nutrition(v_template_id);

    -- Update template
    UPDATE public.meal_templates
    SET
        total_calories = (v_nutrition->>'total_calories')::NUMERIC,
        total_protein_g = (v_nutrition->>'total_protein_g')::NUMERIC,
        total_carbs_g = (v_nutrition->>'total_carbs_g')::NUMERIC,
        total_fat_g = (v_nutrition->>'total_fat_g')::NUMERIC,
        total_fiber_g = (v_nutrition->>'total_fiber_g')::NUMERIC,
        total_sugar_g = COALESCE((v_nutrition->>'total_sugar_g')::NUMERIC, 0),
        total_sodium_mg = COALESCE((v_nutrition->>'total_sodium_mg')::NUMERIC, 0),
        updated_at = NOW()
    WHERE id = v_template_id;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql VOLATILE SECURITY DEFINER;

-- Create trigger
DROP TRIGGER IF EXISTS trigger_update_template_nutrition ON public.meal_template_foods;
CREATE TRIGGER trigger_update_template_nutrition
    AFTER INSERT OR UPDATE OR DELETE ON public.meal_template_foods
    FOR EACH ROW
    EXECUTE FUNCTION public.update_template_nutrition();

-- ============================================================================
-- PART 10: ROW LEVEL SECURITY POLICIES
-- ============================================================================

-- Enable RLS on meal_templates
ALTER TABLE public.meal_templates ENABLE ROW LEVEL SECURITY;

-- Users can view their own templates
DROP POLICY IF EXISTS "Users can view own templates" ON public.meal_templates;
CREATE POLICY "Users can view own templates"
ON public.meal_templates FOR SELECT
USING (auth.uid() = user_id);

-- Users can insert their own templates
DROP POLICY IF EXISTS "Users can insert own templates" ON public.meal_templates;
CREATE POLICY "Users can insert own templates"
ON public.meal_templates FOR INSERT
WITH CHECK (auth.uid() = user_id);

-- Users can update their own templates
DROP POLICY IF EXISTS "Users can update own templates" ON public.meal_templates;
CREATE POLICY "Users can update own templates"
ON public.meal_templates FOR UPDATE
USING (auth.uid() = user_id);

-- Users can delete their own templates
DROP POLICY IF EXISTS "Users can delete own templates" ON public.meal_templates;
CREATE POLICY "Users can delete own templates"
ON public.meal_templates FOR DELETE
USING (auth.uid() = user_id);

-- Service role can manage all templates
DROP POLICY IF EXISTS "Service role can manage all templates" ON public.meal_templates;
CREATE POLICY "Service role can manage all templates"
ON public.meal_templates FOR ALL
USING (auth.jwt()->>'role' = 'service_role');

-- Enable RLS on meal_template_foods
ALTER TABLE public.meal_template_foods ENABLE ROW LEVEL SECURITY;

-- Users can view template foods for their templates
DROP POLICY IF EXISTS "Users can view own template foods" ON public.meal_template_foods;
CREATE POLICY "Users can view own template foods"
ON public.meal_template_foods FOR SELECT
USING (
    EXISTS (
        SELECT 1 FROM public.meal_templates
        WHERE id = meal_template_id
        AND user_id = auth.uid()
    )
);

-- Users can insert template foods for their templates
DROP POLICY IF EXISTS "Users can insert own template foods" ON public.meal_template_foods;
CREATE POLICY "Users can insert own template foods"
ON public.meal_template_foods FOR INSERT
WITH CHECK (
    EXISTS (
        SELECT 1 FROM public.meal_templates
        WHERE id = meal_template_id
        AND user_id = auth.uid()
    )
);

-- Users can update template foods for their templates
DROP POLICY IF EXISTS "Users can update own template foods" ON public.meal_template_foods;
CREATE POLICY "Users can update own template foods"
ON public.meal_template_foods FOR UPDATE
USING (
    EXISTS (
        SELECT 1 FROM public.meal_templates
        WHERE id = meal_template_id
        AND user_id = auth.uid()
    )
);

-- Users can delete template foods for their templates
DROP POLICY IF EXISTS "Users can delete own template foods" ON public.meal_template_foods;
CREATE POLICY "Users can delete own template foods"
ON public.meal_template_foods FOR DELETE
USING (
    EXISTS (
        SELECT 1 FROM public.meal_templates
        WHERE id = meal_template_id
        AND user_id = auth.uid()
    )
);

-- Service role can manage all template foods
DROP POLICY IF EXISTS "Service role can manage all template foods" ON public.meal_template_foods;
CREATE POLICY "Service role can manage all template foods"
ON public.meal_template_foods FOR ALL
USING (auth.jwt()->>'role' = 'service_role');

-- ============================================================================
-- PART 11: INDEXES FOR PERFORMANCE
-- ============================================================================

-- Index for template hierarchy queries
CREATE INDEX IF NOT EXISTS idx_meal_template_foods_template
ON public.meal_template_foods(meal_template_id);

CREATE INDEX IF NOT EXISTS idx_meal_template_foods_child_template
ON public.meal_template_foods(child_template_id)
WHERE child_template_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_meal_template_foods_item_type
ON public.meal_template_foods(item_type);

-- Index for meal_foods template references
CREATE INDEX IF NOT EXISTS idx_meal_foods_template
ON public.meal_foods(template_id)
WHERE template_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_meal_foods_item_type
ON public.meal_foods(item_type);

-- Index for meal_logs template tracking
CREATE INDEX IF NOT EXISTS idx_meal_logs_template
ON public.meal_logs(template_id)
WHERE template_id IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_meal_logs_created_from_template
ON public.meal_logs(user_id, created_from_template)
WHERE created_from_template = true;

-- Index for favorite templates
CREATE INDEX IF NOT EXISTS idx_meal_templates_user_favorite
ON public.meal_templates(user_id, is_favorite)
WHERE is_favorite = true;

CREATE INDEX IF NOT EXISTS idx_meal_templates_use_count
ON public.meal_templates(user_id, use_count DESC);

CREATE INDEX IF NOT EXISTS idx_meal_templates_last_used
ON public.meal_templates(user_id, last_used_at DESC);

-- ============================================================================
-- PART 12: COMMENTS FOR DOCUMENTATION
-- ============================================================================

COMMENT ON TABLE public.meal_templates IS 'Reusable meal templates that can contain foods or other templates';
COMMENT ON COLUMN public.meal_templates.is_favorite IS 'User-marked favorite templates for quick access';
COMMENT ON COLUMN public.meal_templates.use_count IS 'Number of times template has been used to create meals';
COMMENT ON COLUMN public.meal_templates.last_used_at IS 'Timestamp of most recent use';

COMMENT ON TABLE public.meal_template_foods IS 'Items in a meal template (can be foods or nested templates)';
COMMENT ON COLUMN public.meal_template_foods.item_type IS 'Type of item: food or template';
COMMENT ON COLUMN public.meal_template_foods.child_template_id IS 'Reference to nested template (if item_type = template)';
COMMENT ON COLUMN public.meal_template_foods.order_index IS 'Display order of items in template';

COMMENT ON COLUMN public.meal_foods.item_type IS 'Type of item: food or template';
COMMENT ON COLUMN public.meal_foods.template_id IS 'Reference to template (if item_type = template)';
COMMENT ON COLUMN public.meal_foods.order_index IS 'Display order of items in meal';

COMMENT ON COLUMN public.meal_logs.template_id IS 'Template used to create this meal (if any)';
COMMENT ON COLUMN public.meal_logs.created_from_template IS 'Whether this meal was created from a template';

COMMENT ON FUNCTION public.check_template_circular_reference IS 'Checks if adding a template would create a circular reference';
COMMENT ON FUNCTION public.calculate_template_nutrition IS 'Recursively calculates total nutrition for a template including nested templates';
COMMENT ON FUNCTION public.flatten_template IS 'Expands a template into individual foods, resolving all nested templates';
COMMENT ON FUNCTION public.create_meal_from_template IS 'Creates a meal_log from a template, copying all items';

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

-- Summary:
-- ✅ Updated meal_template_foods to support nested templates
-- ✅ Updated meal_foods to support templates in logged meals
-- ✅ Added template tracking and favorites to meal_templates
-- ✅ Added template_id to meal_logs for tracking
-- ✅ Created circular reference prevention function
-- ✅ Created recursive nutrition calculation function
-- ✅ Created template flattening function
-- ✅ Created meal-from-template creation function
-- ✅ Added trigger to auto-update template nutrition
-- ✅ Added comprehensive RLS policies
-- ✅ Created performance indexes
-- ✅ Added documentation comments
