-- Migration: Add Perplexity Nutrition Cache Table
-- Purpose: Store Perplexity API results to minimize API calls and costs
-- Created: 2025-10-10

-- ============================================================================
-- UP MIGRATION
-- ============================================================================

-- Table: Store cached Perplexity nutrition lookups
CREATE TABLE IF NOT EXISTS perplexity_nutrition_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    cache_key TEXT NOT NULL,
    food_name TEXT NOT NULL,
    quantity TEXT,
    unit TEXT,
    nutrition_data JSONB NOT NULL,
    confidence FLOAT,
    source TEXT,
    cached_at TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index: Fast lookups by cache_key (food_name + quantity + unit hash)
CREATE INDEX idx_perplexity_cache_key ON perplexity_nutrition_cache(cache_key);

-- Index: Fast lookups by cached_at for cache expiration
CREATE INDEX idx_perplexity_cached_at ON perplexity_nutrition_cache(cached_at);

-- Index: Cleanup old cache entries (>30 days) - used by cleanup jobs
CREATE INDEX idx_perplexity_cleanup ON perplexity_nutrition_cache(cached_at)
WHERE cached_at < NOW() - INTERVAL '30 days';

-- Index: Search by food_name for debugging/analytics
CREATE INDEX idx_perplexity_food_name ON perplexity_nutrition_cache(food_name);

-- Comment on table
COMMENT ON TABLE perplexity_nutrition_cache IS 'Stores Perplexity AI nutrition lookups to avoid redundant API calls. Cache entries expire after 7 days (configurable).';

-- Comments on columns
COMMENT ON COLUMN perplexity_nutrition_cache.cache_key IS 'Hash of food_name + quantity + unit for fast lookups';
COMMENT ON COLUMN perplexity_nutrition_cache.nutrition_data IS 'Full nutrition data from Perplexity (calories, macros, micros)';
COMMENT ON COLUMN perplexity_nutrition_cache.confidence IS 'Confidence score from Perplexity (0-1)';
COMMENT ON COLUMN perplexity_nutrition_cache.source IS 'Source URL or reference from Perplexity response';

-- ============================================================================
-- DOWN MIGRATION (for rollback)
-- ============================================================================

-- DROP INDEX IF EXISTS idx_perplexity_food_name;
-- DROP INDEX IF EXISTS idx_perplexity_cleanup;
-- DROP INDEX IF EXISTS idx_perplexity_cached_at;
-- DROP INDEX IF EXISTS idx_perplexity_cache_key;
-- DROP TABLE IF EXISTS perplexity_nutrition_cache CASCADE;
