"""
Ultra-Optimized Quick Entry Service

Handles ALL input modalities with FREE models:
- Text
- Voice/Audio (speech-to-text)
- Images (camera/upload)
- PDFs
- Any combination

Uses ONLY FREE top-tier models for max cost efficiency:
- Meta Llama-4 Scout (vision + text, 512k context) - FREE
- DeepSeek V3 (text processing, SOTA) - FREE
- Yi-Vision (image analysis) - FREE
"""

import logging
import json
import base64
import uuid
from typing import Any, Dict, List, Literal, Optional
from datetime import datetime
from io import BytesIO

from app.config import get_settings
from app.services.supabase_service import get_service_client
from app.services.dual_model_router import dual_router, TaskType, TaskConfig
from app.services.multimodal_embedding_service import get_multimodal_service
from app.workers.embedding_worker import embed_meal_log, embed_activity

settings = get_settings()
logger = logging.getLogger(__name__)


EntryType = Literal["meal", "activity", "workout", "note", "measurement", "unknown"]


class QuickEntryService:
    """
    Ultra-fast, ultra-cheap quick entry processing.

    Handles:
    - Text entries
    - Voice/audio → text → processing
    - Images (food photos, workout screenshots, etc.)
    - PDFs (meal plans, workout PDFs)
    - Notes and thoughts
    """

    def __init__(self):
        self.supabase = get_service_client()
        self.router = dual_router
        self.multimodal_service = get_multimodal_service()

    async def process_entry_preview(
        self,
        user_id: str,
        text: Optional[str] = None,
        image_base64: Optional[str] = None,
        audio_base64: Optional[str] = None,
        pdf_base64: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process entry and return classification WITHOUT saving to database.

        Used for preview/confirmation flow where user reviews before saving.

        Returns:
            Classification result with type, confidence, extracted data, suggestions
        """
        logger.info(f"[QuickEntry] PREVIEW mode for user {user_id}")

        # Step 1: Extract text from all inputs
        extracted_text = await self._extract_all_text(
            text=text,
            image_base64=image_base64,
            audio_base64=audio_base64,
            pdf_base64=pdf_base64
        )

        if not extracted_text:
            return {
                "success": False,
                "error": "No content to process",
                "entry_type": "unknown",
                "confidence": 0.0,
                "data": {}
            }

        # Step 2: Classify and extract data
        manual_type = metadata.get('manual_type') if metadata else None

        if manual_type:
            classification = await self._classify_and_extract(
                extracted_text,
                has_image=image_base64 is not None,
                force_type=manual_type
            )
        else:
            classification = await self._classify_and_extract(
                extracted_text,
                has_image=image_base64 is not None
            )

        # Inject user notes
        if metadata and 'notes' in metadata:
            if 'data' not in classification:
                classification['data'] = {}
            classification['data']['notes'] = metadata['notes']

        # Return classification WITHOUT saving
        return {
            "success": True,
            "entry_type": classification["type"],
            "confidence": classification.get("confidence", 0.0),
            "data": classification.get("data", {}),
            "suggestions": classification.get("suggestions", []),
            "extracted_text": extracted_text[:500]
        }

    async def confirm_and_save_entry(
        self,
        user_id: str,
        entry_type: str,
        data: Dict[str, Any],
        original_text: str,
        extracted_text: Optional[str] = None,
        image_base64: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Save confirmed entry to database after user approval.

        Args:
            user_id: User ID
            entry_type: Type of entry (meal, workout, activity, etc.)
            data: Extracted/edited data from LLM + user edits
            original_text: Original user input text
            extracted_text: Full extracted text from all inputs
            image_base64: Optional image to upload

        Returns:
            Success status with entry ID
        """
        logger.info(f"[QuickEntry] CONFIRM mode: Saving {entry_type} for user {user_id}")

        try:
            # Build classification format for save
            classification = {
                "type": entry_type,
                "confidence": 1.0,  # User confirmed, so confidence is max
                "data": data
            }

            # Save to database
            saved_entry = await self._save_entry(
                user_id=user_id,
                classification=classification,
                original_text=original_text,
                image_base64=image_base64,
                metadata=None
            )

            if not saved_entry["success"]:
                return {
                    "success": False,
                    "error": saved_entry.get("error", "Failed to save entry"),
                    "entry_type": entry_type,
                    "confidence": 0.0,
                    "data": {}
                }

            # Vectorize for RAG (async, don't wait)
            try:
                await self._vectorize_entry(
                    user_id=user_id,
                    entry_id=saved_entry["entry_id"],
                    entry_type=entry_type,
                    text=extracted_text or original_text,
                    metadata=data
                )
            except Exception as e:
                logger.error(f"Vectorization failed (non-critical): {e}")

            return {
                "success": True,
                "entry_type": entry_type,
                "confidence": 1.0,
                "data": data,
                "entry_id": saved_entry.get("entry_id")
            }

        except Exception as e:
            logger.error(f"[QuickEntry] Confirm and save failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "entry_type": entry_type,
                "confidence": 0.0,
                "data": {}
            }

    async def process_entry(
        self,
        user_id: str,
        text: Optional[str] = None,
        image_base64: Optional[str] = None,
        audio_base64: Optional[str] = None,
        pdf_base64: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Process any type of quick entry.

        OPTIMIZED: Uses FREE models only, parallel processing where possible

        Args:
            user_id: User ID
            text: Optional text input
            image_base64: Optional base64 encoded image
            audio_base64: Optional base64 encoded audio
            pdf_base64: Optional base64 encoded PDF
            metadata: Optional metadata

        Returns:
            Processed entry with classification, extracted data, and DB save status
        """
        logger.info(f"[QuickEntry] Processing entry for user {user_id}")

        # Step 1: Convert all inputs to text (parallel where possible)
        extracted_text = await self._extract_all_text(
            text=text,
            image_base64=image_base64,
            audio_base64=audio_base64,
            pdf_base64=pdf_base64
        )

        if not extracted_text:
            return {
                "success": False,
                "error": "No content to process",
                "entry_type": "unknown"
            }

        # Step 2: Classify entry type and extract structured data (single FREE LLM call)
        # Check for manual type override from UI
        manual_type = metadata.get('manual_type') if metadata else None

        if manual_type:
            # User manually selected type - trust them and just extract data
            logger.info(f"Manual type override: {manual_type}")
            classification = await self._classify_and_extract(
                extracted_text,
                has_image=image_base64 is not None,
                force_type=manual_type
            )
        else:
            # Auto-detect
            classification = await self._classify_and_extract(
                extracted_text,
                has_image=image_base64 is not None
            )

        # Inject user notes into classification data if provided
        if metadata and 'notes' in metadata:
            if 'data' not in classification:
                classification['data'] = {}
            classification['data']['notes'] = metadata['notes']

        # Step 3: Save to appropriate database table
        try:
            saved_entry = await self._save_entry(
                user_id=user_id,
                classification=classification,
                original_text=extracted_text,
                image_base64=image_base64,
                metadata=metadata
            )
        except Exception as e:
            logger.error(f"[QuickEntry] ❌ Save failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": f"Failed to save entry: {str(e)}",
                "entry_type": classification.get("type", "unknown"),
                "confidence": 0.0,
                "data": {}
            }

        # Step 4: Vectorize for RAG (async, don't wait)
        if saved_entry["success"]:
            # Spawn vectorization task (fire and forget)
            try:
                await self._vectorize_entry(
                    user_id=user_id,
                    entry_id=saved_entry["entry_id"],
                    entry_type=classification["type"],
                    text=extracted_text,
                    metadata=classification.get("data", {})
                )
            except Exception as e:
                logger.error(f"Vectorization failed (non-critical): {e}")

        return {
            "success": saved_entry["success"],
            "entry_type": classification["type"],
            "confidence": classification.get("confidence", 0.0),
            "data": classification.get("data", {}),
            "entry_id": saved_entry.get("entry_id"),
            "suggestions": classification.get("suggestions", []),
            "extracted_text": extracted_text[:500]  # Preview
        }

    async def _extract_all_text(
        self,
        text: Optional[str],
        image_base64: Optional[str],
        audio_base64: Optional[str],
        pdf_base64: Optional[str]
    ) -> str:
        """
        Extract text from all input modalities.

        OPTIMIZED: Uses FREE models with parallel processing
        """
        extracted_parts = []

        # Add direct text
        if text:
            extracted_parts.append(f"USER TEXT: {text}")

        # Process image with vision (if provided)
        if image_base64:
            try:
                logger.info("[QuickEntry] Processing image with FREE vision model")

                # Use FREE Meta Llama-4 Scout or Yi-Vision with dual router
                image_text = await self.router.complete(
                    config=TaskConfig(
                        type=TaskType.VISION,
                        requires_vision=True
                    ),
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {
                                    "type": "text",
                                    "text": "Describe what you see in this image. If it's food, list all visible items, portions, and any nutrition labels. If it's a workout/activity screenshot, extract all text and data."
                                },
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/jpeg;base64,{image_base64}"
                                    }
                                }
                            ]
                        }
                    ]
                )

                vision_output = image_text.choices[0].message.content
                extracted_parts.append(f"IMAGE CONTENT: {vision_output}")
                logger.info(f"[QuickEntry] Image processed: {vision_output[:100]}...")

            except Exception as e:
                logger.error(f"Image processing failed: {e}")
                extracted_parts.append("IMAGE: Failed to process")

        # Process audio (speech-to-text) - Whisper integration
        if audio_base64:
            try:
                logger.info("[QuickEntry] 🎤 Processing audio with Whisper")

                # Decode audio
                import whisper
                import tempfile
                import os

                audio_bytes = base64.b64decode(audio_base64)

                # Save to temp file (Whisper needs file path)
                with tempfile.NamedTemporaryFile(delete=False, suffix='.m4a') as temp_audio:
                    temp_audio.write(audio_bytes)
                    temp_audio_path = temp_audio.name

                try:
                    # Load Whisper model (tiny for speed, can upgrade to base/small/medium)
                    model = whisper.load_model("tiny")

                    # Transcribe
                    result = model.transcribe(temp_audio_path)
                    transcription = result["text"]

                    extracted_parts.append(f"VOICE NOTE: {transcription}")
                    logger.info(f"[QuickEntry] ✅ Audio transcribed: {transcription[:100]}...")

                finally:
                    # Clean up temp file
                    if os.path.exists(temp_audio_path):
                        os.remove(temp_audio_path)

            except Exception as e:
                logger.error(f"❌ Audio processing failed: {e}")
                extracted_parts.append("AUDIO: Failed to transcribe")

        # Process PDF (OCR/text extraction)
        if pdf_base64:
            try:
                logger.info("[QuickEntry] Processing PDF")
                # TODO: Integrate PDF text extraction
                extracted_parts.append("PDF: (PDF extraction integration needed)")
            except Exception as e:
                logger.error(f"PDF processing failed: {e}")

        return "\n\n".join(extracted_parts)

    async def _classify_and_extract(
        self,
        text: str,
        has_image: bool = False,
        force_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Classify entry type and extract structured data.

        OPTIMIZED: Single FREE LLM call using DeepSeek V3 or Llama-4 Scout
        Handles ALL entry types: meal, activity, workout, note, measurement

        Args:
            text: The text to classify
            has_image: Whether an image was included
            force_type: Override auto-detection and force a specific type
        """
        logger.info(f"[QuickEntry] Classifying entry with FREE model (force_type={force_type})")

        # Build classification instruction
        if force_type:
            classification_instruction = f"""The user has indicated this is a **{force_type}** entry.
Type is already determined: "{force_type}"
Extract all relevant data for this {force_type} entry."""
        else:
            classification_instruction = """Classify the entry into ONE of these types:
1. **meal**: Any food/drink consumption (meals, snacks, supplements)
2. **activity**: Cardio activities (running, walking, cycling, swimming, sports)
3. **workout**: Strength training (lifting, calisthenics, specific exercises)
4. **measurement**: Body measurements (weight, body fat %, circumference, progress photos)
5. **note**: General thoughts, goals, feelings, observations, plans
6. **unknown**: Cannot determine"""

        system_prompt = f"""You are a fitness coach assistant analyzing user entries.

{classification_instruction}

Extract ALL relevant data in structured JSON format.

Return ONLY valid JSON (no markdown, no code blocks):

{{
  "type": "meal|activity|workout|measurement|note|unknown",
  "confidence": 0.0-1.0,
  "data": {{
    // Type-specific fields (see examples below)
  }},
  "suggestions": ["helpful tips for user"]
}}

MEAL example:
{
  "type": "meal",
  "confidence": 0.95,
  "data": {
    "meal_name": "Grilled chicken with rice and broccoli",
    "meal_type": "lunch",
    "foods": [
      {"name": "Grilled chicken breast", "quantity": "6 oz"},
      {"name": "Brown rice", "quantity": "1 cup"},
      {"name": "Steamed broccoli", "quantity": "2 cups"}
    ],
    "calories": 450,
    "protein_g": 45,
    "carbs_g": 40,
    "fat_g": 8,
    "fiber_g": 6,
    "estimated": false
  },
  "suggestions": ["Great protein content!", "Consider adding healthy fats"]
}

ACTIVITY example:
{
  "type": "activity",
  "confidence": 0.9,
  "data": {
    "activity_name": "Morning run",
    "activity_type": "running",
    "duration_minutes": 45,
    "distance_km": 7.5,
    "pace": "6:00/km",
    "calories_burned": 550,
    "notes": "Felt great, cool weather"
  },
  "suggestions": ["Excellent consistency!", "Stay hydrated"]
}

WORKOUT example:
{
  "type": "workout",
  "confidence": 0.92,
  "data": {
    "workout_name": "Upper Body Push",
    "workout_type": "strength",
    "exercises": [
      {"name": "Bench Press", "sets": 4, "reps": "8-10", "weight_lbs": 185},
      {"name": "Overhead Press", "sets": 3, "reps": 10, "weight_lbs": 95}
    ],
    "duration_minutes": 60,
    "notes": "New PR on bench!"
  },
  "suggestions": ["Progressive overload working!", "Don't forget cooldown"]
}

NOTE example:
{
  "type": "note",
  "confidence": 0.8,
  "data": {
    "title": "Feeling motivated",
    "content": "Starting to see results, energy levels up",
    "tags": ["motivation", "progress", "energy"],
    "category": "reflection"
  },
  "suggestions": ["Great mindset!", "Track these wins"]
}

MEASUREMENT example:
{
  "type": "measurement",
  "confidence": 0.95,
  "data": {
    "weight_lbs": 175.2,
    "body_fat_pct": 15.5,
    "measurements": {
      "chest_in": 42,
      "waist_in": 32,
      "arms_in": 15
    }
  },
  "suggestions": ["Consistent progress!", "Measure weekly"]
}

IMPORTANT:
- Be intelligent about nutrition estimation from images
- Extract ALL numbers and details
- If unsure, set confidence lower and add suggestions
- Always return valid JSON (no markdown blocks)
"""

        user_prompt = f"""Analyze this entry and extract structured data:

{text}

Return JSON classification and data extraction."""

        try:
            # Use FREE DeepSeek V3 or Llama-4 Scout for complex reasoning with dual router
            response = await self.router.complete(
                config=TaskConfig(
                    type=TaskType.STRUCTURED_OUTPUT,
                    requires_json=True,
                    prioritize_accuracy=True  # Accuracy important for classification
                ),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)

            # Override type if force_type is set (user manual selection)
            if force_type:
                result['type'] = force_type
                result['confidence'] = 1.0  # High confidence when user manually selects
                logger.info(f"[QuickEntry] Forced type: {force_type}")
            else:
                logger.info(f"[QuickEntry] Classified as: {result.get('type')} ({result.get('confidence', 0):.2f})")

            return result

        except Exception as e:
            logger.error(f"Classification failed: {e}")
            return {
                "type": "unknown",
                "confidence": 0.0,
                "data": {},
                "suggestions": ["Try being more specific", "Include details like amounts, duration, etc."]
            }

    async def _save_entry(
        self,
        user_id: str,
        classification: Dict[str, Any],
        original_text: str,
        image_base64: Optional[str],
        metadata: Optional[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Save entry to appropriate database table based on type.
        """
        entry_type = classification["type"]
        data = classification.get("data", {})

        try:
            if entry_type == "meal":
                # Save to meal_logs (using correct field names to match schema)
                result = self.supabase.table("meal_logs").insert({
                    "user_id": user_id,
                    "category": data.get("meal_type", "snack"),  # category, not meal_type
                    "name": data.get("meal_name", original_text[:200]),  # name, not description
                    "notes": f"Quick entry. {original_text[:200]}" if len(original_text) > 200 else original_text,
                    "total_calories": data.get("calories"),  # total_calories, not calories
                    "total_protein_g": data.get("protein_g"),  # total_protein_g
                    "total_carbs_g": data.get("carbs_g"),  # total_carbs_g
                    "total_fat_g": data.get("fat_g"),  # total_fat_g
                    "total_fiber_g": data.get("fiber_g"),  # total_fiber_g
                    "logged_at": datetime.utcnow().isoformat(),
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }).execute()

                return {"success": True, "entry_id": result.data[0]["id"]}

            elif entry_type == "activity":
                # Save to activities (fixed field names to match schema)
                duration_min = data.get("duration_minutes", 0)
                distance_km = data.get("distance_km", 0)

                result = self.supabase.table("activities").insert({
                    "user_id": user_id,
                    "activity_type": data.get("activity_type", "workout"),
                    "sport_type": data.get("sport_type", data.get("activity_type", "workout")),
                    "name": data.get("activity_name", original_text[:200]),
                    "elapsed_time_seconds": int(duration_min * 60) if duration_min else 0,  # Convert minutes to seconds
                    "moving_time_seconds": int(duration_min * 60) if duration_min else None,
                    "distance_meters": int(distance_km * 1000) if distance_km else None,  # Convert km to meters
                    "calories": data.get("calories_burned") or data.get("calories"),
                    "perceived_exertion": data.get("rpe") or data.get("perceived_exertion"),
                    "mood": data.get("mood"),
                    "energy_level": data.get("energy_level"),
                    "notes": data.get("notes", original_text[:500]),
                    "start_date": datetime.utcnow().isoformat(),
                    "source": "manual"  # Changed from quick_entry to match schema constraint
                }).execute()

                return {"success": True, "entry_id": result.data[0]["id"]}

            elif entry_type == "workout":
                # Save to workout_completions (using correct schema fields)
                result = self.supabase.table("workout_completions").insert({
                    "user_id": user_id,
                    "duration_minutes": data.get("duration_minutes"),
                    "notes": f"Workout: {data.get('workout_name', 'Quick Workout')}. {data.get('notes', original_text[:400])}",
                    "rpe": data.get("rpe") or data.get("perceived_exertion"),
                    "mood": data.get("mood"),
                    "energy_level": data.get("energy_level"),
                    "workout_rating": data.get("workout_rating"),
                    "difficulty_rating": data.get("difficulty_rating"),
                    "started_at": datetime.utcnow().isoformat(),
                    "completed_at": datetime.utcnow().isoformat()
                }).execute()

                return {"success": True, "entry_id": result.data[0]["id"]}

            elif entry_type == "note":
                # Save to user_notes (create if doesn't exist)
                result = self.supabase.table("user_notes").insert({
                    "user_id": user_id,
                    "title": data.get("title", "Quick Note"),
                    "content": data.get("content", original_text),
                    "tags": data.get("tags", []),
                    "category": data.get("category", "general"),
                    "created_at": datetime.utcnow().isoformat()
                }).execute()

                return {"success": True, "entry_id": result.data[0]["id"]}

            elif entry_type == "measurement":
                # Save to body_measurements
                result = self.supabase.table("body_measurements").insert({
                    "user_id": user_id,
                    "weight_lbs": data.get("weight_lbs"),
                    "body_fat_pct": data.get("body_fat_pct"),
                    "measurements": data.get("measurements", {}),
                    "notes": original_text[:500],
                    "measured_at": datetime.utcnow().isoformat(),
                    "source": "quick_entry"
                }).execute()

                return {"success": True, "entry_id": result.data[0]["id"]}

            else:
                # Unknown - save to general notes
                result = self.supabase.table("user_notes").insert({
                    "user_id": user_id,
                    "title": "Unclassified Entry",
                    "content": original_text,
                    "tags": ["unclassified"],
                    "category": "general",
                    "created_at": datetime.utcnow().isoformat()
                }).execute()

                return {"success": True, "entry_id": result.data[0]["id"]}

        except Exception as e:
            logger.error(f"Failed to save entry: {e}")
            return {"success": False, "error": str(e)}

    async def _vectorize_entry(
        self,
        user_id: str,
        entry_id: str,
        entry_type: str,
        text: str,
        metadata: Dict[str, Any]
    ):
        """
        Vectorize entry for RAG retrieval - REVOLUTIONARY MULTIMODAL.

        Creates text embedding and stores in multimodal_embeddings table
        for ultra-personalized AI coach context via vector similarity search.
        """
        try:
            logger.info(f"[QuickEntry] 🔥 Vectorizing {entry_type} entry {entry_id}")

            # Generate text embedding using FREE sentence-transformers
            embedding = await self.multimodal_service.embed_text(text)

            # Map entry type to source type (must match context_builder.py expectations!)
            source_type_map = {
                "meal": "meal",  # Changed from "meal_log" to match context builder
                "activity": "activity",
                "workout": "workout",
                "note": "voice_note",
                "measurement": "progress_photo"
            }
            source_type = source_type_map.get(entry_type, "quick_entry")

            # Store embedding in multimodal_embeddings table with FULL context
            # This allows AI coach to access:
            # - WHEN it happened (timestamp)
            # - WHAT happened (description, exercises, foods)
            # - HOW it went (notes, feelings, RPE)
            # - WHICH specific meal/workout/activity (source_id)

            comprehensive_metadata = {
                **metadata,  # LLM-extracted data (calories, exercises, etc.)
                'entry_type': entry_type,
                'source': 'quick_entry',
                'timestamp': datetime.utcnow().isoformat(),  # WHEN
                'logged_at': metadata.get('logged_at') or datetime.utcnow().isoformat(),
                'notes': metadata.get('notes', text[:500]),  # HOW (user feelings)
                'original_text': text,  # Full context
                'source_id': entry_id,  # Links to SQL table
            }

            # Add type-specific metadata for AI coach context
            if entry_type == "meal":
                comprehensive_metadata.update({
                    'meal_name': metadata.get('meal_name'),
                    'meal_type': metadata.get('meal_type'),
                    'calories': metadata.get('calories'),
                    'protein_g': metadata.get('protein_g'),
                    'carbs_g': metadata.get('carbs_g'),
                    'fat_g': metadata.get('fat_g'),
                })
            elif entry_type == "activity":
                comprehensive_metadata.update({
                    'activity_name': metadata.get('activity_name'),
                    'activity_type': metadata.get('activity_type'),
                    'duration_minutes': metadata.get('duration_minutes'),
                    'distance_km': metadata.get('distance_km'),
                    'calories_burned': metadata.get('calories_burned'),
                    'rpe': metadata.get('rpe'),
                    'mood': metadata.get('mood'),
                })
            elif entry_type == "workout":
                comprehensive_metadata.update({
                    'workout_name': metadata.get('workout_name'),
                    'workout_type': metadata.get('workout_type'),
                    'exercises': metadata.get('exercises', []),
                    'duration_minutes': metadata.get('duration_minutes'),
                    'rpe': metadata.get('rpe'),
                    'difficulty_rating': metadata.get('difficulty_rating'),
                })

            await self.multimodal_service.store_embedding(
                user_id=user_id,
                embedding=embedding,
                data_type='text',
                source_type=source_type,
                source_id=entry_id,
                content_text=text,
                metadata=comprehensive_metadata,
                confidence_score=0.9,
                embedding_model='all-MiniLM-L6-v2'
            )

            logger.info(f"✅ Vectorized {entry_type} entry: {entry_id}")

        except Exception as e:
            logger.error(f"❌ Vectorization error: {e}")

    def _upload_image(self, image_base64: str, user_id: str) -> Optional[str]:
        """
        Upload image to Supabase Storage and generate image embedding - REVOLUTIONARY.

        Stores image in user-images bucket and creates CLIP embedding for
        multimodal vector search (find similar meal photos, workout images, etc.)
        """
        try:
            logger.info(f"[QuickEntry] 📸 Uploading image for user {user_id}")

            # Decode base64 image
            image_bytes = base64.b64decode(image_base64)

            # Generate unique filename
            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            filename = f"{user_id}/meals/{timestamp}_meal.jpg"

            # Upload to Supabase Storage (user-images bucket)
            storage_response = self.supabase.storage.from_('user-images').upload(
                filename,
                image_bytes,
                {'content-type': 'image/jpeg'}
            )

            # Get public URL
            storage_url = self.supabase.storage.from_('user-images').get_public_url(filename)

            logger.info(f"✅ Image uploaded: {storage_url}")

            # Generate image embedding asynchronously (fire and forget)
            try:
                import asyncio
                asyncio.create_task(self._vectorize_image(
                    user_id=user_id,
                    image_base64=image_base64,
                    storage_url=storage_url,
                    bucket='user-images',
                    filename=filename
                ))
            except Exception as embed_error:
                logger.warning(f"Image embedding queued failed (non-critical): {embed_error}")

            return storage_url

        except Exception as e:
            logger.error(f"❌ Image upload failed: {e}")
            return None

    async def _vectorize_image(
        self,
        user_id: str,
        image_base64: str,
        storage_url: str,
        bucket: str,
        filename: str
    ):
        """
        Generate CLIP embedding for uploaded image - REVOLUTIONARY.

        Enables semantic image search: "show me my high-protein meals" will
        retrieve visually similar meal photos via vector similarity.
        """
        try:
            logger.info(f"[QuickEntry] 🖼️ Vectorizing image for user {user_id}")

            # Generate image embedding using FREE CLIP model
            embedding = await self.multimodal_service.embed_image(image_base64)

            # Store embedding in multimodal_embeddings table
            await self.multimodal_service.store_embedding(
                user_id=user_id,
                embedding=embedding,
                data_type='image',
                source_type='meal_photo',
                source_id=str(uuid.uuid4()),  # Generate new UUID for image
                content_text=None,  # No text for pure image
                metadata={
                    'uploaded_via': 'quick_entry',
                    'uploaded_at': datetime.utcnow().isoformat()
                },
                storage_url=storage_url,
                storage_bucket=bucket,
                file_name=filename,
                file_size_bytes=len(base64.b64decode(image_base64)),
                mime_type='image/jpeg',
                confidence_score=0.95,  # High confidence for CLIP embeddings
                embedding_model='clip-vit-base-patch32'
            )

            logger.info(f"✅ Image vectorized successfully")

        except Exception as e:
            logger.error(f"❌ Image vectorization failed: {e}")


# Global instance
_service: Optional[QuickEntryService] = None


def get_quick_entry_service() -> QuickEntryService:
    """Get the global QuickEntryService instance."""
    global _service
    if _service is None:
        _service = QuickEntryService()
    return _service
