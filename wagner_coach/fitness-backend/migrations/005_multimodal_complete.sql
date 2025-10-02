-- ============================================================================
-- MULTIMODAL VECTOR DATABASE - COMPLETE & SAFE MIGRATION
-- Can be run multiple times safely (idempotent)
-- ============================================================================

-- Enable pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================================
-- INDEXES (Create if not exists)
-- ============================================================================

-- User + data type filtering (most common query pattern)
CREATE INDEX IF NOT EXISTS idx_multimodal_user_type
  ON multimodal_embeddings(user_id, data_type);

-- Source tracking
CREATE INDEX IF NOT EXISTS idx_multimodal_source
  ON multimodal_embeddings(source_type, source_id);

-- Source type for filtering
CREATE INDEX IF NOT EXISTS idx_multimodal_source_type
  ON multimodal_embeddings(user_id, source_type);

-- Metadata filtering (GIN index for JSONB)
CREATE INDEX IF NOT EXISTS idx_multimodal_metadata
  ON multimodal_embeddings USING GIN (metadata);

-- Timestamp filtering for recency-based queries
CREATE INDEX IF NOT EXISTS idx_multimodal_created_at
  ON multimodal_embeddings(user_id, created_at DESC);

-- Vector similarity search (IVFFlat index for fast approximate nearest neighbor)
CREATE INDEX IF NOT EXISTS idx_multimodal_embedding_ivfflat
  ON multimodal_embeddings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Processing status for background workers
CREATE INDEX IF NOT EXISTS idx_multimodal_processing
  ON multimodal_embeddings(processing_status)
  WHERE processing_status IN ('pending', 'processing');

-- ============================================================================
-- ROW LEVEL SECURITY POLICIES
-- ============================================================================

-- Drop existing policies first (safe if they don't exist)
DROP POLICY IF EXISTS "Users can view their own embeddings" ON multimodal_embeddings;
DROP POLICY IF EXISTS "Users can insert their own embeddings" ON multimodal_embeddings;
DROP POLICY IF EXISTS "Users can update their own embeddings" ON multimodal_embeddings;
DROP POLICY IF EXISTS "Users can delete their own embeddings" ON multimodal_embeddings;
DROP POLICY IF EXISTS "Service role can manage all embeddings" ON multimodal_embeddings;

-- Enable RLS
ALTER TABLE multimodal_embeddings ENABLE ROW LEVEL SECURITY;

-- Create policies
CREATE POLICY "Users can view their own embeddings"
  ON multimodal_embeddings FOR SELECT
  USING (auth.uid() = user_id);

CREATE POLICY "Users can insert their own embeddings"
  ON multimodal_embeddings FOR INSERT
  WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update their own embeddings"
  ON multimodal_embeddings FOR UPDATE
  USING (auth.uid() = user_id);

CREATE POLICY "Users can delete their own embeddings"
  ON multimodal_embeddings FOR DELETE
  USING (auth.uid() = user_id);

CREATE POLICY "Service role can manage all embeddings"
  ON multimodal_embeddings FOR ALL
  USING (auth.jwt()->>'role' = 'service_role');

-- ============================================================================
-- SEARCH FUNCTION
-- ============================================================================

CREATE OR REPLACE FUNCTION match_multimodal_embeddings(
  query_embedding vector(384),
  match_threshold FLOAT DEFAULT 0.5,
  match_count INT DEFAULT 10,
  filter_user_id UUID DEFAULT NULL,
  filter_data_types TEXT[] DEFAULT NULL,
  filter_source_types TEXT[] DEFAULT NULL,
  filter_metadata JSONB DEFAULT NULL,
  filter_date_from TIMESTAMPTZ DEFAULT NULL,
  filter_date_to TIMESTAMPTZ DEFAULT NULL
)
RETURNS TABLE (
  id UUID,
  user_id UUID,
  data_type TEXT,
  content_text TEXT,
  metadata JSONB,
  source_type TEXT,
  source_id UUID,
  storage_url TEXT,
  storage_bucket TEXT,
  file_name TEXT,
  mime_type TEXT,
  embedding_model TEXT,
  confidence_score NUMERIC,
  created_at TIMESTAMPTZ,
  similarity FLOAT
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    e.id,
    e.user_id,
    e.data_type,
    e.content_text,
    e.metadata,
    e.source_type,
    e.source_id,
    e.storage_url,
    e.storage_bucket,
    e.file_name,
    e.mime_type,
    e.embedding_model,
    e.confidence_score,
    e.created_at,
    (1 - (e.embedding <=> query_embedding))::FLOAT AS similarity
  FROM multimodal_embeddings e
  WHERE
    (filter_user_id IS NULL OR e.user_id = filter_user_id)
    AND (filter_data_types IS NULL OR e.data_type = ANY(filter_data_types))
    AND (filter_source_types IS NULL OR e.source_type = ANY(filter_source_types))
    AND (filter_metadata IS NULL OR e.metadata @> filter_metadata)
    AND (filter_date_from IS NULL OR e.created_at >= filter_date_from)
    AND (filter_date_to IS NULL OR e.created_at <= filter_date_to)
    AND (1 - (e.embedding <=> query_embedding)) > match_threshold
    AND e.processing_status = 'completed'
  ORDER BY e.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

CREATE OR REPLACE FUNCTION get_user_embedding_stats(p_user_id UUID)
RETURNS TABLE (
  total_embeddings BIGINT,
  text_count BIGINT,
  image_count BIGINT,
  audio_count BIGINT,
  video_count BIGINT,
  pdf_count BIGINT,
  total_storage_bytes BIGINT,
  oldest_embedding TIMESTAMPTZ,
  newest_embedding TIMESTAMPTZ,
  data_type_breakdown JSONB
)
LANGUAGE plpgsql
AS $$
BEGIN
  RETURN QUERY
  SELECT
    COUNT(*)::BIGINT AS total_embeddings,
    COUNT(*) FILTER (WHERE data_type = 'text')::BIGINT AS text_count,
    COUNT(*) FILTER (WHERE data_type = 'image')::BIGINT AS image_count,
    COUNT(*) FILTER (WHERE data_type = 'audio')::BIGINT AS audio_count,
    COUNT(*) FILTER (WHERE data_type = 'video')::BIGINT AS video_count,
    COUNT(*) FILTER (WHERE data_type = 'pdf')::BIGINT AS pdf_count,
    COALESCE(SUM(file_size_bytes), 0)::BIGINT AS total_storage_bytes,
    MIN(created_at) AS oldest_embedding,
    MAX(created_at) AS newest_embedding,
    jsonb_object_agg(
      data_type,
      count
    ) AS data_type_breakdown
  FROM (
    SELECT
      data_type,
      COUNT(*)::BIGINT AS count
    FROM multimodal_embeddings
    WHERE user_id = p_user_id
    GROUP BY data_type
  ) counts
  GROUP BY ();
END;
$$;

CREATE OR REPLACE FUNCTION queue_embedding_processing(
  p_user_id UUID,
  p_data_type TEXT,
  p_source_type TEXT,
  p_source_id UUID,
  p_content_text TEXT DEFAULT NULL,
  p_storage_url TEXT DEFAULT NULL,
  p_metadata JSONB DEFAULT '{}'
)
RETURNS UUID
LANGUAGE plpgsql
AS $$
DECLARE
  v_embedding_id UUID;
BEGIN
  INSERT INTO multimodal_embeddings (
    user_id,
    data_type,
    source_type,
    source_id,
    content_text,
    storage_url,
    metadata,
    processing_status,
    embedding,
    embedding_model,
    embedding_dimensions
  ) VALUES (
    p_user_id,
    p_data_type,
    p_source_type,
    p_source_id,
    p_content_text,
    p_storage_url,
    p_metadata,
    'pending',
    ARRAY_FILL(0, ARRAY[384])::vector(384), -- Placeholder zero vector
    'pending',
    384
  )
  ON CONFLICT (user_id, source_type, source_id, data_type)
  DO UPDATE SET
    processing_status = 'pending',
    updated_at = NOW()
  RETURNING id INTO v_embedding_id;

  RETURN v_embedding_id;
END;
$$;

-- ============================================================================
-- TRIGGERS
-- ============================================================================

CREATE OR REPLACE FUNCTION update_multimodal_embeddings_updated_at()
RETURNS TRIGGER AS $$
BEGIN
  NEW.updated_at = NOW();
  RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trigger_update_multimodal_embeddings_updated_at
  ON multimodal_embeddings;

CREATE TRIGGER trigger_update_multimodal_embeddings_updated_at
  BEFORE UPDATE ON multimodal_embeddings
  FOR EACH ROW
  EXECUTE FUNCTION update_multimodal_embeddings_updated_at();

-- ============================================================================
-- GRANT PERMISSIONS
-- ============================================================================

GRANT SELECT, INSERT, UPDATE, DELETE ON multimodal_embeddings TO authenticated;
GRANT EXECUTE ON FUNCTION match_multimodal_embeddings TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_embedding_stats TO authenticated;
GRANT EXECUTE ON FUNCTION queue_embedding_processing TO authenticated;

-- ============================================================================
-- SUCCESS MESSAGE
-- ============================================================================

DO $$
BEGIN
  RAISE NOTICE '============================================';
  RAISE NOTICE 'MULTIMODAL VECTOR DATABASE READY!';
  RAISE NOTICE '============================================';
  RAISE NOTICE '✅ Indexes created/verified';
  RAISE NOTICE '✅ RLS policies configured';
  RAISE NOTICE '✅ Search functions ready';
  RAISE NOTICE '✅ Helper functions ready';
  RAISE NOTICE 'Next: Install Python dependencies & create Storage buckets';
  RAISE NOTICE '============================================';
END $$;
