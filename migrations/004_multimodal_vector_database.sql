-- Migration: Multimodal Vector Database
-- Description: Revolutionary multimodal vector storage for text, images, audio, and more
-- Phase 1: Enhanced Vector Storage Foundation

-- ============================================================================
-- PART 1: ENABLE PGVECTOR EXTENSION
-- ============================================================================

CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================================
-- PART 2: MULTIMODAL EMBEDDINGS TABLE
-- ============================================================================

CREATE TABLE IF NOT EXISTS multimodal_embeddings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,

  -- Content Classification
  data_type TEXT NOT NULL CHECK (data_type IN ('text', 'image', 'audio', 'video', 'pdf', 'structured', 'mixed')),
  content_text TEXT, -- For text content or OCR/transcription results

  -- Vector Storage (pgvector) - Using 384 dimensions for sentence-transformers all-MiniLM-L6-v2
  embedding VECTOR(384) NOT NULL,

  -- Metadata (JSONB for flexible filtering)
  metadata JSONB DEFAULT '{}',

  -- Source Tracking
  source_type TEXT NOT NULL CHECK (source_type IN (
    'meal', 'meal_log', 'meal_photo',
    'workout', 'workout_log', 'workout_photo', 'workout_video',
    'activity', 'activity_photo', 'activity_gpx',
    'goal', 'user_goal',
    'profile', 'user_profile',
    'coach_message', 'conversation',
    'program', 'ai_program',
    'voice_note', 'quick_entry',
    'food_label', 'nutrition_label',
    'body_photo', 'progress_photo',
    'other'
  )),
  source_id UUID, -- Reference to source table record

  -- File References (Supabase Storage)
  storage_url TEXT,
  storage_bucket TEXT CHECK (storage_bucket IN ('user-images', 'user-audio', 'user-videos', 'user-documents', 'user-photos')),
  file_name TEXT,
  file_size_bytes BIGINT,
  mime_type TEXT,

  -- Model Info
  embedding_model TEXT NOT NULL DEFAULT 'all-MiniLM-L6-v2',
  embedding_dimensions INTEGER NOT NULL DEFAULT 384,

  -- Quality & Confidence
  confidence_score NUMERIC CHECK (confidence_score >= 0 AND confidence_score <= 1),
  processing_status TEXT DEFAULT 'completed' CHECK (processing_status IN ('pending', 'processing', 'completed', 'failed')),
  processing_error TEXT,

  -- Timestamps
  created_at TIMESTAMPTZ DEFAULT NOW(),
  updated_at TIMESTAMPTZ DEFAULT NOW(),

  -- Constraints
  CONSTRAINT multimodal_embeddings_content_check
    CHECK (content_text IS NOT NULL OR storage_url IS NOT NULL),
  CONSTRAINT multimodal_embeddings_user_source_unique
    UNIQUE (user_id, source_type, source_id, data_type)
);

-- ============================================================================
-- PART 3: INDEXES FOR FAST RETRIEVAL
-- ============================================================================

-- User + data type filtering (most common query pattern)
CREATE INDEX idx_multimodal_user_type
  ON multimodal_embeddings(user_id, data_type);

-- Source tracking
CREATE INDEX idx_multimodal_source
  ON multimodal_embeddings(source_type, source_id);

-- Source type for filtering
CREATE INDEX idx_multimodal_source_type
  ON multimodal_embeddings(user_id, source_type);

-- Metadata filtering (GIN index for JSONB)
CREATE INDEX idx_multimodal_metadata
  ON multimodal_embeddings USING GIN (metadata);

-- Timestamp filtering for recency-based queries
CREATE INDEX idx_multimodal_created_at
  ON multimodal_embeddings(user_id, created_at DESC);

-- Vector similarity search (IVFFlat index for fast approximate nearest neighbor)
-- Using 100 lists for datasets with thousands of vectors
CREATE INDEX idx_multimodal_embedding_ivfflat
  ON multimodal_embeddings
  USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);

-- Processing status for background workers
CREATE INDEX idx_multimodal_processing
  ON multimodal_embeddings(processing_status)
  WHERE processing_status IN ('pending', 'processing');

-- ============================================================================
-- PART 4: ROW LEVEL SECURITY POLICIES
-- ============================================================================

ALTER TABLE multimodal_embeddings ENABLE ROW LEVEL SECURITY;

-- Users can view their own embeddings
CREATE POLICY "Users can view their own embeddings"
  ON multimodal_embeddings FOR SELECT
  USING (auth.uid() = user_id);

-- Users can insert their own embeddings
CREATE POLICY "Users can insert their own embeddings"
  ON multimodal_embeddings FOR INSERT
  WITH CHECK (auth.uid() = user_id);

-- Users can update their own embeddings
CREATE POLICY "Users can update their own embeddings"
  ON multimodal_embeddings FOR UPDATE
  USING (auth.uid() = user_id);

-- Users can delete their own embeddings
CREATE POLICY "Users can delete their own embeddings"
  ON multimodal_embeddings FOR DELETE
  USING (auth.uid() = user_id);

-- Service role can manage all embeddings (for background workers)
CREATE POLICY "Service role can manage all embeddings"
  ON multimodal_embeddings FOR ALL
  USING (auth.jwt()->>'role' = 'service_role');

-- ============================================================================
-- PART 5: ENHANCED VECTOR SEARCH FUNCTION
-- ============================================================================

CREATE OR REPLACE FUNCTION match_multimodal_embeddings(
  query_embedding VECTOR(384),
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
    -- User filter
    (filter_user_id IS NULL OR e.user_id = filter_user_id)

    -- Data type filter (text, image, audio, etc.)
    AND (filter_data_types IS NULL OR e.data_type = ANY(filter_data_types))

    -- Source type filter (meal, workout, activity, etc.)
    AND (filter_source_types IS NULL OR e.source_type = ANY(filter_source_types))

    -- Metadata filter (contains all specified key-value pairs)
    AND (filter_metadata IS NULL OR e.metadata @> filter_metadata)

    -- Date range filter
    AND (filter_date_from IS NULL OR e.created_at >= filter_date_from)
    AND (filter_date_to IS NULL OR e.created_at <= filter_date_to)

    -- Similarity threshold
    AND (1 - (e.embedding <=> query_embedding)) > match_threshold

    -- Only completed embeddings
    AND e.processing_status = 'completed'

  ORDER BY e.embedding <=> query_embedding
  LIMIT match_count;
END;
$$;

-- ============================================================================
-- PART 6: HELPER FUNCTIONS
-- ============================================================================

-- Function to get user's embedding statistics
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

-- Function to mark pending embeddings for processing
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
    ARRAY[]::VECTOR(384), -- Placeholder empty vector
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
-- PART 7: TRIGGERS
-- ============================================================================

-- Trigger to update updated_at timestamp
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
-- PART 8: STORAGE BUCKETS (Run via Supabase Dashboard or API)
-- ============================================================================

-- Note: These storage buckets should be created via Supabase Dashboard or API:
-- - user-images (public: false, file size limit: 10MB)
-- - user-audio (public: false, file size limit: 50MB)
-- - user-videos (public: false, file size limit: 100MB)
-- - user-documents (public: false, file size limit: 20MB)
-- - user-photos (public: false, file size limit: 10MB)

-- ============================================================================
-- PART 9: GRANT PERMISSIONS
-- ============================================================================

-- Grant permissions to authenticated users
GRANT SELECT, INSERT, UPDATE, DELETE ON multimodal_embeddings TO authenticated;

-- Grant execute on functions
GRANT EXECUTE ON FUNCTION match_multimodal_embeddings TO authenticated;
GRANT EXECUTE ON FUNCTION get_user_embedding_stats TO authenticated;
GRANT EXECUTE ON FUNCTION queue_embedding_processing TO authenticated;

-- ============================================================================
-- MIGRATION COMPLETE
-- ============================================================================

DO $$
BEGIN
  RAISE NOTICE '============================================';
  RAISE NOTICE 'MULTIMODAL VECTOR DATABASE MIGRATION COMPLETE';
  RAISE NOTICE '============================================';
  RAISE NOTICE 'Created: multimodal_embeddings table';
  RAISE NOTICE 'Created: 7 indexes (including IVFFlat vector index)';
  RAISE NOTICE 'Created: 5 RLS policies';
  RAISE NOTICE 'Created: 3 helper functions';
  RAISE NOTICE 'Ready for: Text, Image, Audio, Video, PDF embeddings';
  RAISE NOTICE 'Next Step: Create Supabase Storage buckets';
  RAISE NOTICE '============================================';
END $$;
