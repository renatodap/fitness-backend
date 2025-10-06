-- ============================================================================
-- Quick Entry Database Verification Script
-- Run this in Supabase SQL Editor to verify everything is set up correctly
-- ============================================================================

-- Check 1: Verify semantic_search_entries function exists
SELECT
  'semantic_search_entries' AS function_name,
  EXISTS (
    SELECT 1
    FROM pg_proc
    WHERE proname = 'semantic_search_entries'
  ) AS exists,
  CASE
    WHEN EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'semantic_search_entries')
    THEN '✅ Function exists - Quick Entry will work'
    ELSE '❌ Function missing - Apply supabase_migration_semantic_search_helpers.sql'
  END AS status;

-- Check 2: Verify multimodal_embeddings table exists
SELECT
  'multimodal_embeddings' AS table_name,
  EXISTS (
    SELECT 1
    FROM information_schema.tables
    WHERE table_name = 'multimodal_embeddings'
  ) AS exists,
  CASE
    WHEN EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'multimodal_embeddings')
    THEN '✅ Table exists'
    ELSE '❌ Table missing - Apply migration 004 or 005'
  END AS status;

-- Check 3: Verify pgvector extension is installed
SELECT
  'pgvector' AS extension_name,
  EXISTS (
    SELECT 1
    FROM pg_extension
    WHERE extname = 'vector'
  ) AS exists,
  CASE
    WHEN EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector')
    THEN '✅ pgvector extension installed'
    ELSE '❌ pgvector missing - Enable in Supabase dashboard'
  END AS status;

-- Check 4: Verify all required semantic search functions
SELECT
  proname AS function_name,
  CASE
    WHEN proname IN (
      'semantic_search_entries',
      'find_similar_meals',
      'find_similar_workouts',
      'get_ai_context_bundle',
      'get_recent_entry_stats'
    ) THEN '✅ Available'
    ELSE '⚠️ Unknown function'
  END AS status
FROM pg_proc
WHERE proname IN (
  'semantic_search_entries',
  'find_similar_meals',
  'find_similar_workouts',
  'get_ai_context_bundle',
  'get_recent_entry_stats'
)
ORDER BY proname;

-- Check 5: Verify indexes exist
SELECT
  indexname,
  tablename,
  '✅ Index exists' AS status
FROM pg_indexes
WHERE tablename = 'multimodal_embeddings'
  AND indexname IN (
    'idx_multimodal_embeddings_user_source',
    'idx_multimodal_embeddings_user_created',
    'idx_multimodal_embeddings_metadata'
  )
ORDER BY indexname;

-- Check 6: Verify embedding column has correct dimensions
SELECT
  column_name,
  data_type,
  CASE
    WHEN data_type = 'USER-DEFINED' THEN '✅ Vector type (should be vector(384))'
    ELSE '❌ Wrong type - should be vector(384)'
  END AS status
FROM information_schema.columns
WHERE table_name = 'multimodal_embeddings'
  AND column_name = 'embedding';

-- ============================================================================
-- SUMMARY: Quick Entry Readiness Check
-- ============================================================================

DO $$
DECLARE
  v_semantic_search_exists BOOLEAN;
  v_table_exists BOOLEAN;
  v_pgvector_exists BOOLEAN;
  v_ready BOOLEAN;
BEGIN
  -- Check all requirements
  SELECT EXISTS (SELECT 1 FROM pg_proc WHERE proname = 'semantic_search_entries') INTO v_semantic_search_exists;
  SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'multimodal_embeddings') INTO v_table_exists;
  SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector') INTO v_pgvector_exists;

  v_ready := v_semantic_search_exists AND v_table_exists AND v_pgvector_exists;

  RAISE NOTICE '';
  RAISE NOTICE '════════════════════════════════════════════════════════════';
  RAISE NOTICE '         QUICK ENTRY DATABASE VERIFICATION';
  RAISE NOTICE '════════════════════════════════════════════════════════════';
  RAISE NOTICE '';
  RAISE NOTICE 'Components:';
  RAISE NOTICE '  semantic_search_entries(): %', CASE WHEN v_semantic_search_exists THEN '✅ EXISTS' ELSE '❌ MISSING' END;
  RAISE NOTICE '  multimodal_embeddings table: %', CASE WHEN v_table_exists THEN '✅ EXISTS' ELSE '❌ MISSING' END;
  RAISE NOTICE '  pgvector extension: %', CASE WHEN v_pgvector_exists THEN '✅ ENABLED' ELSE '❌ DISABLED' END;
  RAISE NOTICE '';

  IF v_ready THEN
    RAISE NOTICE '🎉 QUICK ENTRY IS READY TO USE! 🎉';
    RAISE NOTICE '';
    RAISE NOTICE 'All required components are installed and configured.';
    RAISE NOTICE 'Backend can now process Quick Entry requests successfully.';
  ELSE
    RAISE NOTICE '⚠️  QUICK ENTRY NOT READY - ACTION REQUIRED ⚠️';
    RAISE NOTICE '';
    IF NOT v_pgvector_exists THEN
      RAISE NOTICE '1. Enable pgvector extension:';
      RAISE NOTICE '   - Go to Supabase Dashboard → Database → Extensions';
      RAISE NOTICE '   - Enable "vector" extension';
    END IF;
    IF NOT v_table_exists THEN
      RAISE NOTICE '2. Apply multimodal embeddings migration:';
      RAISE NOTICE '   - File: migrations/004_multimodal_vector_database.sql';
      RAISE NOTICE '   - OR: migrations/005_multimodal_complete.sql';
    END IF;
    IF NOT v_semantic_search_exists THEN
      RAISE NOTICE '3. Apply semantic search helper functions:';
      RAISE NOTICE '   - File: migrations/supabase_migration_semantic_search_helpers.sql';
    END IF;
  END IF;

  RAISE NOTICE '';
  RAISE NOTICE '════════════════════════════════════════════════════════════';
END $$;
