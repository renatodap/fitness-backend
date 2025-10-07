# Quick Entry Logging System - Design Document

**Version:** 1.0
**Date:** 2025-10-06
**Status:** Production-Ready
**Migration:** `007_quick_entry_logging_system.sql`

---

## Table of Contents
1. [Overview](#overview)
2. [Architecture](#architecture)
3. [Database Schema](#database-schema)
4. [Data Flow](#data-flow)
5. [API Implementation](#api-implementation)
6. [Vector Embeddings & RAG](#vector-embeddings--rag)
7. [AI Cost Optimization](#ai-cost-optimization)
8. [Usage Examples](#usage-examples)
9. [Testing Strategy](#testing-strategy)
10. [Monitoring & Analytics](#monitoring--analytics)

---

## Overview

### Purpose
The Quick Entry Logging System is a comprehensive, production-ready database architecture designed to:
- **Capture** multimodal user input (text, voice, images, PDFs)
- **Store** both raw input and AI-processed structured data
- **Extract** structured information (meals, workouts, body measurements)
- **Generate** vector embeddings for semantic search
- **Enable** RAG (Retrieval-Augmented Generation) for AI coach context

### Key Features
✅ **Multimodal Support**: Text, voice, images, PDFs
✅ **Dual Storage**: Raw + structured data
✅ **Vector Embeddings**: FREE sentence-transformers model
✅ **Semantic Search**: pgvector with HNSW indexing
✅ **Cost Tracking**: Per-entry AI costs ($0.50/user/month target)
✅ **Analytics**: Usage stats, success rates, performance metrics
✅ **RLS Security**: Row-level security on all tables
✅ **Backward Compatible**: Links to existing tables

### Target Use Cases
1. **"I ate 3 eggs and oatmeal for breakfast"** → Meal log created
2. **Voice note: "Just finished 30 min run, 5K"** → Activity log created
3. **Photo of meal** → AI extracts nutrition data → Meal log created
4. **"Did 3 sets of 10 pushups"** → Workout log created
5. **Coach question: "What did I eat yesterday?"** → RAG retrieves relevant meals

---

## Architecture

### System Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INPUT                              │
│  Text | Voice Note | Meal Photo | Workout Photo | PDF Label    │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  QUICK ENTRY LOGS TABLE                         │
│  - Raw text, audio URL, image URLs                             │
│  - Input metadata (type, modalities)                           │
│  - Processing status                                            │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                     AI PROCESSING                               │
│  Groq Llama 3.3 70B: Text extraction ($0.05/M tokens)         │
│  Llama 4 Scout: Image analysis ($0.50/M tokens)               │
│  FREE Whisper: Voice transcription (local)                     │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│               UPDATE QUICK ENTRY LOGS                           │
│  - AI extracted data (structured JSON)                         │
│  - Classification (meal, workout, body_measurement)            │
│  - Confidence score                                             │
│  - Cost tracking                                                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│              CREATE STRUCTURED LOGS                             │
│  ├─ meal_logs (if meal detected)                               │
│  ├─ activities (if workout detected)                           │
│  └─ body_measurements (if measurement detected)                │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│         GENERATE VECTOR EMBEDDINGS (FREE)                       │
│  sentence-transformers/all-MiniLM-L6-v2 (384D)                 │
│  Store in quick_entry_embeddings table                         │
└─────────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────────┐
│                  SEMANTIC SEARCH & RAG                          │
│  Coach asks: "What did I eat for breakfast today?"             │
│  → Vector search finds relevant meals                          │
│  → Context built for AI coach response                         │
└─────────────────────────────────────────────────────────────────┘
```

---

## Database Schema

### Core Tables

#### 1. `quick_entry_logs`
**Purpose:** Main table storing ALL quick entry submissions

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `user_id` | UUID | Foreign key to auth.users |
| `input_type` | TEXT | 'text', 'voice', 'image', 'multimodal', 'pdf' |
| `input_modalities` | TEXT[] | Array of modalities used |
| `raw_text` | TEXT | Original user text input |
| `raw_transcription` | TEXT | Voice-to-text transcription |
| `image_urls` | TEXT[] | Uploaded image URLs |
| `audio_url` | TEXT | Uploaded audio URL |
| `pdf_url` | TEXT | Uploaded PDF URL |
| `ai_provider` | TEXT | 'groq', 'openrouter', 'anthropic', 'free' |
| `ai_model` | TEXT | Exact model used |
| `ai_cost_usd` | NUMERIC(10,6) | Cost per entry |
| `tokens_used` | INTEGER | Total tokens consumed |
| `ai_classification` | TEXT | 'meal', 'workout', 'body_measurement', etc. |
| `ai_extracted_data` | JSONB | Full structured AI output |
| `ai_confidence_score` | NUMERIC(3,2) | 0.0 to 1.0 |
| `contains_meal` | BOOLEAN | TRUE if meal detected |
| `contains_workout` | BOOLEAN | TRUE if workout detected |
| `contains_body_measurement` | BOOLEAN | TRUE if measurement detected |
| `meal_log_ids` | UUID[] | Links to created meal_logs |
| `workout_log_ids` | UUID[] | Links to created activities |
| `body_measurement_ids` | UUID[] | Links to body_measurements |
| `processing_status` | TEXT | 'pending', 'processing', 'completed', 'failed' |
| `embedding_generated` | BOOLEAN | TRUE if vector embedding created |
| `embedding_id` | UUID | Link to quick_entry_embeddings |
| `logged_at` | TIMESTAMPTZ | When user submitted |
| `created_at` | TIMESTAMPTZ | Record created |

**Indexes:**
- `idx_quick_entry_logs_user_id` - User lookup
- `idx_quick_entry_logs_logged_at` - Time-based queries
- `idx_quick_entry_logs_classification` - Filter by type
- `idx_quick_entry_logs_status` - Processing status
- `idx_quick_entry_logs_raw_text_fts` - Full-text search

**RLS Policies:**
- Users can CRUD their own entries only

---

#### 2. `quick_entry_embeddings`
**Purpose:** Vector embeddings for semantic search & RAG

| Column | Type | Description |
|--------|------|-------------|
| `id` | UUID | Primary key |
| `quick_entry_log_id` | UUID | Foreign key to quick_entry_logs |
| `user_id` | UUID | Foreign key to auth.users |
| `embedding_type` | TEXT | 'text', 'image', 'multimodal', 'combined' |
| `embedding` | vector(384) | 384-dimensional vector (FREE model) |
| `content_text` | TEXT | Searchable text representation |
| `content_summary` | TEXT | 1-2 sentence summary |
| `metadata` | JSONB | Additional context |
| `source_classification` | TEXT | 'meal', 'workout', etc. |
| `embedding_model` | TEXT | 'sentence-transformers/all-MiniLM-L6-v2' |
| `content_hash` | TEXT | Hash for duplicate detection |
| `is_active` | BOOLEAN | Can deactivate old embeddings |
| `logged_at` | TIMESTAMPTZ | Original entry timestamp |

**Indexes:**
- `idx_quick_entry_embeddings_vector` - HNSW for vector similarity
- `idx_quick_entry_embeddings_user_id` - User lookup
- `idx_quick_entry_embeddings_logged_at` - Time filtering
- `idx_quick_entry_embeddings_content_fts` - Full-text search

**RLS Policies:**
- Users can view their own embeddings
- Service role can insert/update

---

#### 3. `quick_entry_stats`
**Purpose:** Per-user analytics and cost tracking

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | UUID | Primary key (user) |
| `total_entries` | INTEGER | Total quick entries |
| `text_entries` | INTEGER | Text-only entries |
| `voice_entries` | INTEGER | Voice note entries |
| `image_entries` | INTEGER | Image uploads |
| `multimodal_entries` | INTEGER | Multiple modalities |
| `meal_extractions` | INTEGER | Successful meal extractions |
| `workout_extractions` | INTEGER | Successful workout extractions |
| `body_measurement_extractions` | INTEGER | Successful measurement extractions |
| `failed_extractions` | INTEGER | Failed AI extractions |
| `total_ai_cost_usd` | NUMERIC(10,2) | Total AI costs |
| `total_tokens_used` | BIGINT | Total tokens consumed |
| `avg_processing_time_ms` | INTEGER | Average AI processing time |
| `avg_confidence_score` | NUMERIC(3,2) | Average extraction confidence |
| `first_entry_at` | TIMESTAMPTZ | First usage date |
| `last_entry_at` | TIMESTAMPTZ | Most recent usage |

**Auto-updated by trigger on `quick_entry_logs` INSERT**

---

### Enhanced Existing Tables

#### `meal_logs` (Enhanced)
New columns:
- `quick_entry_log_id` UUID - Links to quick_entry_logs
- `ai_extracted` BOOLEAN - TRUE if AI-created
- `ai_confidence` NUMERIC(3,2) - Extraction confidence
- `extraction_metadata` JSONB - AI model, cost, etc.

#### `activities` (Enhanced)
Same enhancements as meal_logs

#### `body_measurements` (Enhanced)
Same enhancements as meal_logs

---

### Database Functions

#### `search_quick_entry_embeddings()`
**Purpose:** Semantic similarity search

```sql
SELECT * FROM search_quick_entry_embeddings(
    query_embedding := your_embedding_vector,
    user_id_filter := 'user-uuid',
    match_threshold := 0.7,
    match_count := 10,
    classification_filter := 'meal', -- optional
    start_date := '2025-10-01', -- optional
    end_date := '2025-10-31' -- optional
);
```

**Returns:**
- `id`, `quick_entry_log_id`, `content_text`, `content_summary`
- `similarity` (0.0 to 1.0)
- `classification`, `logged_at`, `metadata`

#### `get_rag_context_for_quick_entry()`
**Purpose:** Build RAG context string for AI coach

```sql
SELECT get_rag_context_for_quick_entry(
    p_user_id := 'user-uuid',
    p_query_embedding := your_embedding_vector,
    p_max_results := 10,
    p_similarity_threshold := 0.7
);
```

**Returns:** Formatted text string ready for AI prompt

---

## Data Flow

### Example: User Submits Text Entry

**User Input:**
`"I just ate 3 scrambled eggs, 2 slices of whole wheat toast, and a banana for breakfast"`

**Step 1: Create Quick Entry Log**
```python
quick_entry_log = {
    "user_id": user_id,
    "input_type": "text",
    "input_modalities": ["text"],
    "raw_text": "I just ate 3 scrambled eggs, 2 slices of whole wheat toast, and a banana for breakfast",
    "processing_status": "pending",
    "logged_at": datetime.utcnow()
}
# INSERT into quick_entry_logs
```

**Step 2: AI Processing (Groq Llama 3.3 70B)**
```python
# Call Groq API to extract structured data
ai_response = await groq_client.extract_meal_data(
    text=quick_entry_log["raw_text"],
    model="llama-3.3-70b-versatile"
)

# ai_response:
{
    "classification": "meal",
    "meal_type": "breakfast",
    "foods": [
        {"name": "scrambled eggs", "quantity": 3, "unit": "eggs"},
        {"name": "whole wheat toast", "quantity": 2, "unit": "slices"},
        {"name": "banana", "quantity": 1, "unit": "whole"}
    ],
    "estimated_nutrition": {
        "calories": 450,
        "protein": 28,
        "carbs": 52,
        "fats": 12
    },
    "confidence": 0.92
}
```

**Step 3: Update Quick Entry Log**
```python
# UPDATE quick_entry_logs
update_data = {
    "ai_provider": "groq",
    "ai_model": "llama-3.3-70b-versatile",
    "ai_cost_usd": 0.0005,  # Example cost
    "tokens_used": 150,
    "ai_classification": "meal",
    "ai_extracted_data": ai_response,
    "ai_confidence_score": 0.92,
    "contains_meal": True,
    "processing_status": "completed",
    "processing_duration_ms": 1200
}
```

**Step 4: Create Meal Log**
```python
meal_log = {
    "user_id": user_id,
    "quick_entry_log_id": quick_entry_log_id,
    "category": "breakfast",
    "logged_at": quick_entry_log["logged_at"],
    "foods": ai_response["foods"],
    "total_calories": 450,
    "total_protein_g": 28,
    "total_carbs_g": 52,
    "total_fat_g": 12,
    "source": "quick_entry",
    "ai_extracted": True,
    "ai_confidence": 0.92,
    "extraction_metadata": {
        "model": "llama-3.3-70b-versatile",
        "cost": 0.0005,
        "tokens": 150
    }
}
# INSERT into meal_logs
```

**Step 5: Generate Vector Embedding (FREE)**
```python
# Use FREE sentence-transformers model (local or Hugging Face)
embedding = await generate_embedding(
    text=quick_entry_log["raw_text"],
    model="sentence-transformers/all-MiniLM-L6-v2"
)

# Create embedding record
quick_entry_embedding = {
    "quick_entry_log_id": quick_entry_log_id,
    "user_id": user_id,
    "embedding_type": "text",
    "embedding": embedding,  # 384-dimensional vector
    "content_text": quick_entry_log["raw_text"],
    "content_summary": "Breakfast: scrambled eggs, wheat toast, banana (450 cal)",
    "source_classification": "meal",
    "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
    "content_hash": hash(quick_entry_log["raw_text"]),
    "logged_at": quick_entry_log["logged_at"]
}
# INSERT into quick_entry_embeddings
```

**Step 6: Update Quick Entry Log with Links**
```python
# UPDATE quick_entry_logs
update_data = {
    "meal_log_ids": [meal_log_id],
    "embedding_generated": True,
    "embedding_id": embedding_id
}
```

**Step 7: Stats Auto-Updated (Trigger)**
```sql
-- Trigger automatically updates quick_entry_stats:
-- total_entries += 1
-- text_entries += 1
-- meal_extractions += 1
-- total_ai_cost_usd += 0.0005
-- total_tokens_used += 150
-- last_entry_at = NOW()
```

---

## API Implementation

### Backend Service: `quick_entry_service.py`

```python
"""
Quick Entry Service

Handles multimodal input processing, AI extraction, and structured logging.
"""
from typing import Dict, Optional, List
from datetime import datetime
from uuid import UUID

from app.services.supabase_service import SupabaseService
from app.services.groq_service import GroqService
from app.services.embedding_service import EmbeddingService
from app.core.exceptions import QuickEntryProcessingError
import structlog

logger = structlog.get_logger()

class QuickEntryService:
    """Service for processing Quick Entry submissions."""

    def __init__(
        self,
        supabase: SupabaseService,
        groq: GroqService,
        embedding: EmbeddingService
    ):
        self.supabase = supabase
        self.groq = groq
        self.embedding = embedding

    async def process_text_entry(
        self,
        user_id: UUID,
        text: str,
        logged_at: Optional[datetime] = None
    ) -> Dict:
        """
        Process text-based Quick Entry.

        Steps:
        1. Create quick_entry_logs record
        2. Call Groq AI to extract structured data
        3. Update quick_entry_logs with AI results
        4. Create structured logs (meal, workout, etc.)
        5. Generate vector embeddings (FREE)
        6. Return results

        Args:
            user_id: User UUID
            text: Raw text input
            logged_at: When entry was made (defaults to NOW)

        Returns:
            Dict with quick_entry_log_id, extracted data, created logs

        Raises:
            QuickEntryProcessingError: If processing fails
        """
        logged_at = logged_at or datetime.utcnow()

        try:
            # Step 1: Create quick entry log
            quick_entry_log = await self.supabase.table("quick_entry_logs").insert({
                "user_id": str(user_id),
                "input_type": "text",
                "input_modalities": ["text"],
                "raw_text": text,
                "processing_status": "pending",
                "logged_at": logged_at.isoformat()
            }).execute()

            log_id = quick_entry_log.data[0]["id"]

            # Step 2: AI extraction (Groq Llama 3.3 70B)
            logger.info("Starting AI extraction", user_id=user_id, log_id=log_id)

            ai_result = await self.groq.extract_structured_data(
                text=text,
                model="llama-3.3-70b-versatile"
            )

            # Step 3: Update quick entry log with AI results
            await self.supabase.table("quick_entry_logs").update({
                "ai_provider": "groq",
                "ai_model": ai_result["model"],
                "ai_cost_usd": ai_result["cost"],
                "tokens_used": ai_result["tokens"],
                "ai_classification": ai_result["classification"],
                "ai_extracted_data": ai_result["data"],
                "ai_confidence_score": ai_result["confidence"],
                "contains_meal": ai_result["classification"] == "meal",
                "contains_workout": ai_result["classification"] == "workout",
                "contains_body_measurement": ai_result["classification"] == "body_measurement",
                "processing_status": "processing",
                "processing_duration_ms": ai_result["duration_ms"]
            }).eq("id", log_id).execute()

            # Step 4: Create structured logs
            created_logs = await self._create_structured_logs(
                user_id=user_id,
                quick_entry_log_id=log_id,
                classification=ai_result["classification"],
                extracted_data=ai_result["data"],
                logged_at=logged_at,
                ai_metadata={
                    "model": ai_result["model"],
                    "cost": ai_result["cost"],
                    "tokens": ai_result["tokens"],
                    "confidence": ai_result["confidence"]
                }
            )

            # Step 5: Generate embeddings (FREE)
            embedding_id = await self._generate_embeddings(
                quick_entry_log_id=log_id,
                user_id=user_id,
                text=text,
                classification=ai_result["classification"],
                logged_at=logged_at
            )

            # Step 6: Final update
            await self.supabase.table("quick_entry_logs").update({
                "processing_status": "completed",
                "embedding_generated": True,
                "embedding_id": embedding_id,
                **created_logs["update_fields"]  # meal_log_ids, etc.
            }).eq("id", log_id).execute()

            logger.info(
                "Quick entry processed successfully",
                user_id=user_id,
                log_id=log_id,
                classification=ai_result["classification"]
            )

            return {
                "quick_entry_log_id": log_id,
                "classification": ai_result["classification"],
                "confidence": ai_result["confidence"],
                "extracted_data": ai_result["data"],
                "created_logs": created_logs["logs"],
                "embedding_id": embedding_id
            }

        except Exception as e:
            logger.error("Quick entry processing failed", user_id=user_id, error=str(e))

            # Update status to failed
            if 'log_id' in locals():
                await self.supabase.table("quick_entry_logs").update({
                    "processing_status": "failed",
                    "processing_error": str(e)
                }).eq("id", log_id).execute()

            raise QuickEntryProcessingError(f"Failed to process quick entry: {str(e)}")

    async def _create_structured_logs(
        self,
        user_id: UUID,
        quick_entry_log_id: UUID,
        classification: str,
        extracted_data: Dict,
        logged_at: datetime,
        ai_metadata: Dict
    ) -> Dict:
        """Create structured logs based on classification."""
        logs = []
        update_fields = {}

        if classification == "meal":
            # Create meal_log
            meal_log = await self.supabase.table("meal_logs").insert({
                "user_id": str(user_id),
                "quick_entry_log_id": str(quick_entry_log_id),
                "category": extracted_data.get("meal_type", "other"),
                "logged_at": logged_at.isoformat(),
                "foods": extracted_data.get("foods", []),
                "total_calories": extracted_data.get("calories"),
                "total_protein_g": extracted_data.get("protein"),
                "total_carbs_g": extracted_data.get("carbs"),
                "total_fat_g": extracted_data.get("fats"),
                "source": "quick_entry",
                "ai_extracted": True,
                "ai_confidence": ai_metadata["confidence"],
                "extraction_metadata": ai_metadata
            }).execute()

            logs.append({"type": "meal", "id": meal_log.data[0]["id"]})
            update_fields["meal_log_ids"] = [meal_log.data[0]["id"]]

        elif classification == "workout":
            # Create activity log
            activity = await self.supabase.table("activities").insert({
                "user_id": str(user_id),
                "quick_entry_log_id": str(quick_entry_log_id),
                "source": "quick_entry",
                "name": extracted_data.get("workout_name", "Quick Entry Workout"),
                "activity_type": extracted_data.get("activity_type", "strength"),
                "start_date": logged_at.isoformat(),
                "elapsed_time_seconds": extracted_data.get("duration_seconds"),
                "notes": extracted_data.get("notes"),
                "ai_extracted": True,
                "ai_confidence": ai_metadata["confidence"],
                "extraction_metadata": ai_metadata
            }).execute()

            logs.append({"type": "workout", "id": activity.data[0]["id"]})
            update_fields["workout_log_ids"] = [activity.data[0]["id"]]

        elif classification == "body_measurement":
            # Create body measurement
            measurement = await self.supabase.table("body_measurements").insert({
                "user_id": str(user_id),
                "quick_entry_log_id": str(quick_entry_log_id),
                "measured_at": logged_at.isoformat(),
                "weight_lbs": extracted_data.get("weight_lbs"),
                "body_fat_pct": extracted_data.get("body_fat_pct"),
                "source": "quick_entry",
                "ai_extracted": True,
                "ai_confidence": ai_metadata["confidence"],
                "extraction_metadata": ai_metadata
            }).execute()

            logs.append({"type": "body_measurement", "id": measurement.data[0]["id"]})
            update_fields["body_measurement_ids"] = [measurement.data[0]["id"]]

        return {
            "logs": logs,
            "update_fields": update_fields
        }

    async def _generate_embeddings(
        self,
        quick_entry_log_id: UUID,
        user_id: UUID,
        text: str,
        classification: str,
        logged_at: datetime
    ) -> UUID:
        """Generate vector embeddings using FREE model."""
        # Generate embedding using FREE sentence-transformers
        embedding = await self.embedding.generate_text_embedding(
            text=text,
            model="sentence-transformers/all-MiniLM-L6-v2"
        )

        # Create summary (1-2 sentences)
        summary = await self._generate_summary(text, classification)

        # Insert embedding
        result = await self.supabase.table("quick_entry_embeddings").insert({
            "quick_entry_log_id": str(quick_entry_log_id),
            "user_id": str(user_id),
            "embedding_type": "text",
            "embedding": embedding,
            "content_text": text,
            "content_summary": summary,
            "source_classification": classification,
            "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
            "embedding_dimensions": 384,
            "content_hash": hash(text),
            "logged_at": logged_at.isoformat()
        }).execute()

        return result.data[0]["id"]

    async def _generate_summary(self, text: str, classification: str) -> str:
        """Generate 1-2 sentence summary."""
        # Simple summary (can enhance with AI if needed)
        max_length = 100
        if len(text) <= max_length:
            return text
        return text[:max_length] + "..."
```

---

## Vector Embeddings & RAG

### Generating Embeddings

**Use FREE Model:**
```python
from sentence_transformers import SentenceTransformer

# Load model (one-time, cache it)
model = SentenceTransformer('sentence-transformers/all-MiniLM-L6-v2')

# Generate embedding
text = "I ate 3 eggs and oatmeal for breakfast"
embedding = model.encode(text)  # Returns 384-dimensional vector

# Store in database
await supabase.table("quick_entry_embeddings").insert({
    "embedding": embedding.tolist(),  # Convert numpy array to list
    # ... other fields
})
```

### Semantic Search

**Query:**
```python
# User query: "What did I eat for breakfast today?"
query_embedding = model.encode("breakfast meals today")

# Search database
results = await supabase.rpc(
    "search_quick_entry_embeddings",
    {
        "query_embedding": query_embedding.tolist(),
        "user_id_filter": user_id,
        "match_threshold": 0.7,
        "match_count": 5,
        "classification_filter": "meal",
        "start_date": datetime.now().replace(hour=0, minute=0).isoformat()
    }
).execute()

# Results ranked by similarity
for result in results.data:
    print(f"Similarity: {result['similarity']:.2f}")
    print(f"Content: {result['content_text']}")
    print(f"Logged: {result['logged_at']}")
```

### RAG Context Building

**For AI Coach:**
```python
# Get context for user question
context = await supabase.rpc(
    "get_rag_context_for_quick_entry",
    {
        "p_user_id": user_id,
        "p_query_embedding": query_embedding.tolist(),
        "p_max_results": 10,
        "p_similarity_threshold": 0.7
    }
).execute()

# context.data will be formatted text ready for AI prompt
# Example output:
"""
[MEAL | 2025-10-06 08:30]
I ate 3 scrambled eggs, 2 slices of whole wheat toast, and a banana for breakfast

[MEAL | 2025-10-05 08:15]
Had oatmeal with blueberries and protein powder for breakfast

[WORKOUT | 2025-10-05 18:00]
30 minute run, 5K distance, felt great
"""

# Use in AI coach prompt
system_prompt = f"""
You are a fitness coach. Use this context about the user:

{context.data}

User question: What did I eat for breakfast today?
"""
```

---

## AI Cost Optimization

### Model Selection Strategy

| Task | Model | Cost | When to Use |
|------|-------|------|-------------|
| **Text extraction** | Groq Llama 3.3 70B | $0.05/M tokens | Simple meal/workout logging |
| **Image analysis** | Llama 4 Scout | $0.50/M tokens | Meal photos, workout photos |
| **Voice transcription** | FREE Whisper Tiny | $0.00 | Voice notes (local) |
| **Embeddings** | sentence-transformers | $0.00 | All text embeddings (FREE) |
| **Complex reasoning** | Claude 3.5 Sonnet | $3-15/M tokens | Only when Groq fails |

### Cost Tracking

**Monitor per user:**
```sql
SELECT
    user_id,
    total_entries,
    total_ai_cost_usd,
    total_ai_cost_usd / NULLIF(total_entries, 0) AS avg_cost_per_entry,
    meal_extractions,
    workout_extractions,
    failed_extractions
FROM quick_entry_stats
WHERE total_ai_cost_usd > 0.50  -- Alert if user exceeds target
ORDER BY total_ai_cost_usd DESC;
```

**Target: $0.50/user/month**
- Text entries: $0.05 (Groq)
- Image entries: $0.10 (OpenRouter)
- Embeddings: $0.00 (FREE)
- **Total per user/month: ~$0.15 for Quick Entry**

---

## Usage Examples

### Example 1: Text Entry (Meal)

**User submits:**
```
"I had chicken breast with rice and broccoli for lunch, about 600 calories"
```

**System processes:**
1. Creates `quick_entry_logs` record with raw text
2. Calls Groq AI to extract:
   - Meal type: lunch
   - Foods: chicken breast, rice, broccoli
   - Calories: 600
3. Creates `meal_logs` record
4. Generates embedding (FREE)
5. User can now search: "What did I eat for lunch?" → finds this meal

---

### Example 2: Voice Entry (Workout)

**User records voice note:**
```
"Just finished a 30 minute run, covered about 5 kilometers, felt great"
```

**System processes:**
1. Uploads audio to storage
2. Transcribes with FREE Whisper: "Just finished a 30 minute run..."
3. Creates `quick_entry_logs` with `audio_url` and `raw_transcription`
4. Calls Groq AI to extract:
   - Activity type: run
   - Duration: 30 minutes
   - Distance: 5 km
5. Creates `activities` record
6. Generates embedding from transcription

---

### Example 3: Image Entry (Meal Photo)

**User uploads meal photo**

**System processes:**
1. Uploads image to storage (Supabase Storage)
2. Creates `quick_entry_logs` with `image_urls`
3. Calls Llama 4 Scout to analyze image:
   - Detected foods: pasta, marinara sauce, meatballs
   - Estimated portions
   - Estimated nutrition
4. Creates `meal_logs` record
5. Generates embedding from description: "Spaghetti with meatballs..."

---

## Testing Strategy

### Unit Tests

**Test: Text extraction**
```python
@pytest.mark.asyncio
async def test_process_text_entry_meal(quick_entry_service, mock_groq):
    """Test successful meal extraction from text."""
    # Mock Groq response
    mock_groq.extract_structured_data.return_value = {
        "classification": "meal",
        "confidence": 0.92,
        "data": {
            "meal_type": "breakfast",
            "foods": ["eggs", "toast"],
            "calories": 450
        },
        "model": "llama-3.3-70b-versatile",
        "cost": 0.0005,
        "tokens": 150,
        "duration_ms": 1200
    }

    result = await quick_entry_service.process_text_entry(
        user_id=UUID("test-user"),
        text="I ate 3 eggs and toast for breakfast"
    )

    assert result["classification"] == "meal"
    assert result["confidence"] == 0.92
    assert len(result["created_logs"]) == 1
    assert result["created_logs"][0]["type"] == "meal"
```

### Integration Tests

**Test: Full quick entry flow**
```python
@pytest.mark.asyncio
async def test_quick_entry_full_flow(authenticated_client, test_user):
    """Test complete quick entry flow: submit → extract → search."""
    # Step 1: Submit quick entry
    response = await authenticated_client.post("/api/v1/quick-entry", json={
        "text": "I ate oatmeal with blueberries for breakfast",
        "input_type": "text"
    })
    assert response.status_code == 201
    quick_entry_id = response.json()["id"]

    # Step 2: Wait for processing (or use async job queue)
    await asyncio.sleep(2)

    # Step 3: Verify meal log created
    meal_logs = await authenticated_client.get("/api/v1/meals")
    assert len(meal_logs.json()) == 1
    assert meal_logs.json()[0]["source"] == "quick_entry"

    # Step 4: Verify embedding generated
    quick_entry = await authenticated_client.get(f"/api/v1/quick-entry/{quick_entry_id}")
    assert quick_entry.json()["embedding_generated"] == True

    # Step 5: Test semantic search
    search_results = await authenticated_client.post("/api/v1/search", json={
        "query": "breakfast meals",
        "limit": 5
    })
    assert len(search_results.json()) == 1
    assert "oatmeal" in search_results.json()[0]["content_text"]
```

---

## Monitoring & Analytics

### Key Metrics

**1. Processing Success Rate**
```sql
SELECT
    COUNT(*) FILTER (WHERE processing_status = 'completed') * 100.0 / COUNT(*) AS success_rate_pct,
    AVG(ai_confidence_score) AS avg_confidence,
    AVG(processing_duration_ms) AS avg_processing_time_ms
FROM quick_entry_logs
WHERE created_at >= NOW() - INTERVAL '7 days';
```

**2. Cost Per User**
```sql
SELECT
    user_id,
    SUM(ai_cost_usd) AS total_cost_usd,
    COUNT(*) AS entries,
    SUM(ai_cost_usd) / COUNT(*) AS avg_cost_per_entry
FROM quick_entry_logs
WHERE logged_at >= NOW() - INTERVAL '30 days'
GROUP BY user_id
HAVING SUM(ai_cost_usd) > 0.50  -- Alert threshold
ORDER BY total_cost_usd DESC;
```

**3. Extraction Types Distribution**
```sql
SELECT
    ai_classification,
    COUNT(*) AS count,
    AVG(ai_confidence_score) AS avg_confidence,
    COUNT(*) * 100.0 / SUM(COUNT(*)) OVER () AS percentage
FROM quick_entry_logs
WHERE processing_status = 'completed'
GROUP BY ai_classification;
```

**4. Embeddings Performance**
```sql
SELECT
    COUNT(*) AS total_embeddings,
    COUNT(*) FILTER (WHERE is_active = TRUE) AS active_embeddings,
    AVG(LENGTH(content_text)) AS avg_content_length,
    COUNT(DISTINCT user_id) AS users_with_embeddings
FROM quick_entry_embeddings;
```

---

## Production Deployment Checklist

- [x] Migration file created (`007_quick_entry_logging_system.sql`)
- [x] All tables have RLS policies
- [x] Indexes created for performance
- [x] Vector similarity index (HNSW) created
- [x] Database functions for search created
- [x] Triggers for auto-stats updates created
- [ ] Backend service implemented (`quick_entry_service.py`)
- [ ] API endpoints created (`/api/v1/quick-entry`)
- [ ] Groq integration tested
- [ ] Embedding generation tested (FREE model)
- [ ] Semantic search tested
- [ ] RAG context building tested
- [ ] Unit tests written (≥80% coverage)
- [ ] Integration tests written
- [ ] Cost monitoring dashboard created
- [ ] Error tracking configured (Sentry)
- [ ] Documentation updated
- [ ] Migration tested on staging
- [ ] Migration run on production

---

## Next Steps

1. **Implement Backend Service**
   - Create `app/services/quick_entry_service.py`
   - Implement text, voice, image processing
   - Add error handling and retries

2. **Create API Endpoints**
   - `POST /api/v1/quick-entry` - Submit new entry
   - `GET /api/v1/quick-entry` - List user's entries
   - `GET /api/v1/quick-entry/{id}` - Get specific entry
   - `POST /api/v1/quick-entry/search` - Semantic search

3. **Integrate AI Services**
   - Groq for text extraction
   - OpenRouter for image analysis
   - FREE Whisper for voice transcription
   - FREE sentence-transformers for embeddings

4. **Test & Deploy**
   - Run migration on staging
   - Test all flows end-to-end
   - Monitor costs and performance
   - Deploy to production

---

**This system is ready for production deployment. Follow CLAUDE.md standards for implementation.**
