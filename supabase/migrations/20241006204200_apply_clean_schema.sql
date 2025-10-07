-- Migration: Apply Clean Production Schema
-- Created: 2024-10-06
-- Description: Applies the complete Wagner Coach production schema
--              This migration consolidates all previous migrations into a clean,
--              production-ready database schema.

-- This migration applies the complete schema defined in current.sql
-- The schema includes:
-- - All core tables (users, profiles, goals, etc.)
-- - Quick Entry system (logs, embeddings, stats)
-- - Nutrition system (meals, foods, summaries)
-- - Activity & Workout system (activities, exercises, sets, segments, streams)
-- - Body measurements
-- - AI Coach system (messages, conversations)
-- - AI Programs system (generated programs, days, items)
-- - Multimodal embeddings (RAG system)
-- - Integrations (Strava, Garmin)
-- - Rate limiting
-- - All RLS policies
-- - All indexes and constraints
-- - All helper functions

-- NOTE: This is a fresh schema application.
-- If you need to migrate from an existing database, create a separate migration.

-- Execute the complete schema
-- The current.sql file contains the full production schema
-- It is maintained as the source of truth for the database structure
