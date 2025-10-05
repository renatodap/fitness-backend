-- ============================================================================
-- Semantic Search Helper Functions
-- Created: 2025-01-05
-- Purpose: SQL functions for semantic search using multimodal_embeddings
-- ============================================================================

-- ============================================================================
-- FUNCTION: Semantic Search with Recency Weighting
-- ============================================================================

CREATE OR REPLACE FUNCTION semantic_search_entries(
  p_user_id UUID,
  p_query_embedding vector(384),
  p_source_type TEXT DEFAULT NULL,
  p_limit INTEGER DEFAULT 10,
  p_recency_weight DECIMAL DEFAULT 0.3,
  p_similarity_threshold DECIMAL DEFAULT 0.5
)
RETURNS TABLE (
  id UUID,
  source_type TEXT,
  source_id UUID,
  content_text TEXT,
  metadata JSONB,
  data_type TEXT,
  storage_url TEXT,
  created_at TIMESTAMPTZ,
  similarity DECIMAL,
  recency_score DECIMAL,
  final_score DECIMAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    e.id,
    e.source_type,
    e.source_id,
    e.content_text,
    e.metadata,
    e.data_type,
    e.storage_url,
    e.created_at,
    -- Cosine similarity (1 - cosine distance)
    (1 - (e.embedding <=> p_query_embedding))::DECIMAL AS similarity,
    -- Recency score (exponential decay over 30 days)
    EXP(-EXTRACT(EPOCH FROM (NOW() - e.created_at)) / (86400 * 30))::DECIMAL AS recency_score,
    -- Final score: weighted average of similarity and recency
    ((1 - p_recency_weight) * (1 - (e.embedding <=> p_query_embedding)) +
     p_recency_weight * EXP(-EXTRACT(EPOCH FROM (NOW() - e.created_at)) / (86400 * 30)))::DECIMAL AS final_score
  FROM multimodal_embeddings e
  WHERE e.user_id = p_user_id
    AND (p_source_type IS NULL OR e.source_type = p_source_type)
    AND (1 - (e.embedding <=> p_query_embedding)) >= p_similarity_threshold
  ORDER BY final_score DESC
  LIMIT p_limit;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION semantic_search_entries IS 'Vector similarity search with recency weighting for personalized context retrieval';

-- ============================================================================
-- FUNCTION: Find Similar Meals (Optimized for Nutrition)
-- ============================================================================

CREATE OR REPLACE FUNCTION find_similar_meals(
  p_user_id UUID,
  p_query_embedding vector(384),
  p_limit INTEGER DEFAULT 5,
  p_min_quality_score DECIMAL DEFAULT NULL
)
RETURNS TABLE (
  id UUID,
  source_id UUID,
  content_text TEXT,
  meal_name TEXT,
  calories INTEGER,
  protein_g DECIMAL,
  quality_score DECIMAL,
  similarity DECIMAL,
  created_at TIMESTAMPTZ
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    e.id,
    e.source_id,
    e.content_text,
    (e.metadata->>'meal_name')::TEXT AS meal_name,
    (e.metadata->>'calories')::INTEGER AS calories,
    (e.metadata->>'protein_g')::DECIMAL AS protein_g,
    (e.metadata->>'meal_quality_score')::DECIMAL AS quality_score,
    (1 - (e.embedding <=> p_query_embedding))::DECIMAL AS similarity,
    e.created_at
  FROM multimodal_embeddings e
  WHERE e.user_id = p_user_id
    AND e.source_type = 'meal'
    AND (p_min_quality_score IS NULL OR (e.metadata->>'meal_quality_score')::DECIMAL >= p_min_quality_score)
  ORDER BY (1 - (e.embedding <=> p_query_embedding)) DESC
  LIMIT p_limit;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION find_similar_meals IS 'Find meals similar to query, optionally filtering by quality score';

-- ============================================================================
-- FUNCTION: Find Similar Workouts (Optimized for Progressive Overload)
-- ============================================================================

CREATE OR REPLACE FUNCTION find_similar_workouts(
  p_user_id UUID,
  p_query_embedding vector(384),
  p_limit INTEGER DEFAULT 5,
  p_muscle_groups TEXT[] DEFAULT NULL
)
RETURNS TABLE (
  id UUID,
  source_id UUID,
  content_text TEXT,
  workout_name TEXT,
  volume_load INTEGER,
  exercises JSONB,
  progressive_overload_status TEXT,
  similarity DECIMAL,
  created_at TIMESTAMPTZ
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    e.id,
    e.source_id,
    e.content_text,
    (e.metadata->>'workout_name')::TEXT AS workout_name,
    (e.metadata->>'volume_load')::INTEGER AS volume_load,
    (e.metadata->'exercises')::JSONB AS exercises,
    (e.metadata->>'progressive_overload_status')::TEXT AS progressive_overload_status,
    (1 - (e.embedding <=> p_query_embedding))::DECIMAL AS similarity,
    e.created_at
  FROM multimodal_embeddings e
  WHERE e.user_id = p_user_id
    AND e.source_type = 'workout'
    AND (p_muscle_groups IS NULL OR
         (e.metadata->'muscle_groups')::TEXT[] && p_muscle_groups)
  ORDER BY (1 - (e.embedding <=> p_query_embedding)) DESC
  LIMIT p_limit;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION find_similar_workouts IS 'Find workouts similar to query, optionally filtering by muscle groups';

-- ============================================================================
-- FUNCTION: Get Context Bundle for AI Coach
-- ============================================================================

CREATE OR REPLACE FUNCTION get_ai_context_bundle(
  p_user_id UUID,
  p_query_embedding vector(384),
  p_entry_type TEXT DEFAULT NULL
)
RETURNS JSONB AS $$
DECLARE
  v_similar_entries JSONB;
  v_recent_meals JSONB;
  v_recent_workouts JSONB;
  v_context JSONB;
BEGIN
  -- Get similar entries
  SELECT JSONB_AGG(ROW_TO_JSON(t.*))
  INTO v_similar_entries
  FROM (
    SELECT
      source_type,
      content_text,
      metadata,
      (1 - (embedding <=> p_query_embedding))::DECIMAL AS similarity,
      created_at
    FROM multimodal_embeddings
    WHERE user_id = p_user_id
      AND (p_entry_type IS NULL OR source_type = p_entry_type)
    ORDER BY (1 - (embedding <=> p_query_embedding)) DESC
    LIMIT 3
  ) t;

  -- Get recent meals (last 3 days)
  SELECT JSONB_AGG(ROW_TO_JSON(t.*))
  INTO v_recent_meals
  FROM (
    SELECT
      content_text,
      metadata,
      created_at
    FROM multimodal_embeddings
    WHERE user_id = p_user_id
      AND source_type = 'meal'
      AND created_at >= NOW() - INTERVAL '3 days'
    ORDER BY created_at DESC
    LIMIT 5
  ) t;

  -- Get recent workouts (last 7 days)
  SELECT JSONB_AGG(ROW_TO_JSON(t.*))
  INTO v_recent_workouts
  FROM (
    SELECT
      content_text,
      metadata,
      created_at
    FROM multimodal_embeddings
    WHERE user_id = p_user_id
      AND source_type = 'workout'
      AND created_at >= NOW() - INTERVAL '7 days'
    ORDER BY created_at DESC
    LIMIT 3
  ) t;

  -- Build context bundle
  v_context := JSONB_BUILD_OBJECT(
    'similar_entries', COALESCE(v_similar_entries, '[]'::JSONB),
    'recent_meals', COALESCE(v_recent_meals, '[]'::JSONB),
    'recent_workouts', COALESCE(v_recent_workouts, '[]'::JSONB),
    'timestamp', NOW()
  );

  RETURN v_context;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION get_ai_context_bundle IS 'Get comprehensive context bundle for AI coach recommendations';

-- ============================================================================
-- FUNCTION: Get Recent Entry Stats
-- ============================================================================

CREATE OR REPLACE FUNCTION get_recent_entry_stats(
  p_user_id UUID,
  p_days INTEGER DEFAULT 7
)
RETURNS TABLE (
  source_type TEXT,
  entry_count BIGINT,
  avg_quality_score DECIMAL
) AS $$
BEGIN
  RETURN QUERY
  SELECT
    e.source_type,
    COUNT(*)::BIGINT AS entry_count,
    AVG(
      CASE
        WHEN e.source_type = 'meal' THEN (e.metadata->>'meal_quality_score')::DECIMAL
        WHEN e.source_type = 'activity' THEN (e.metadata->>'performance_score')::DECIMAL
        ELSE NULL
      END
    )::DECIMAL AS avg_quality_score
  FROM multimodal_embeddings e
  WHERE e.user_id = p_user_id
    AND e.created_at >= NOW() - (p_days || ' days')::INTERVAL
  GROUP BY e.source_type
  ORDER BY entry_count DESC;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;

COMMENT ON FUNCTION get_recent_entry_stats IS 'Get statistics on recent entries by type';

-- ============================================================================
-- INDEXES: Optimize semantic search queries
-- ============================================================================

-- Index for user + source_type filtering (if not exists)
CREATE INDEX IF NOT EXISTS idx_multimodal_embeddings_user_source
  ON multimodal_embeddings(user_id, source_type);

-- Index for user + created_at (for recency queries)
CREATE INDEX IF NOT EXISTS idx_multimodal_embeddings_user_created
  ON multimodal_embeddings(user_id, created_at DESC);

-- GIN index for metadata JSONB queries
CREATE INDEX IF NOT EXISTS idx_multimodal_embeddings_metadata
  ON multimodal_embeddings USING GIN(metadata);

-- ============================================================================
-- VERIFICATION
-- ============================================================================

DO $$
DECLARE
  v_function_count INTEGER;
BEGIN
  -- Count created functions
  SELECT COUNT(*)::INTEGER
  INTO v_function_count
  FROM pg_proc
  WHERE proname IN (
    'semantic_search_entries',
    'find_similar_meals',
    'find_similar_workouts',
    'get_ai_context_bundle',
    'get_recent_entry_stats'
  );

  RAISE NOTICE '============================================';
  RAISE NOTICE 'Semantic Search Helper Functions Migration Complete!';
  RAISE NOTICE '============================================';
  RAISE NOTICE 'Functions Created: %', v_function_count;
  RAISE NOTICE '';
  RAISE NOTICE 'Available Functions:';
  RAISE NOTICE '  ✓ semantic_search_entries(user_id, query_embedding, ...)';
  RAISE NOTICE '  ✓ find_similar_meals(user_id, query_embedding, ...)';
  RAISE NOTICE '  ✓ find_similar_workouts(user_id, query_embedding, ...)';
  RAISE NOTICE '  ✓ get_ai_context_bundle(user_id, query_embedding, ...)';
  RAISE NOTICE '  ✓ get_recent_entry_stats(user_id, days)';
  RAISE NOTICE '';
  RAISE NOTICE 'Indexes Created: 3';
  RAISE NOTICE '  ✓ idx_multimodal_embeddings_user_source';
  RAISE NOTICE '  ✓ idx_multimodal_embeddings_user_created';
  RAISE NOTICE '  ✓ idx_multimodal_embeddings_metadata';
  RAISE NOTICE '';
  RAISE NOTICE 'Ready for semantic search! 🚀';
  RAISE NOTICE '============================================';
END $$;
