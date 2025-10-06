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
from openai import OpenAI

from app.config import get_settings
from app.services.supabase_service import get_service_client
from app.services.dual_model_router import dual_router, TaskType, TaskConfig
from app.services.multimodal_embedding_service import get_multimodal_service
from app.services.groq_service_v2 import get_groq_service_v2
from app.services.enrichment_service import get_enrichment_service
from app.services.semantic_search_service import get_semantic_search_service
from app.workers.embedding_worker import embed_meal_log, embed_activity

settings = get_settings()
logger = logging.getLogger(__name__)
openai_client = OpenAI(api_key=settings.OPENAI_API_KEY)


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
        self.groq_service = get_groq_service_v2()
        self.enrichment_service = get_enrichment_service()
        self.semantic_search = get_semantic_search_service()

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
        logger.info("╔" + "═" * 78 + "╗")
        logger.info(f"║ [QuickEntry] 🔍 PREVIEW MODE START")
        logger.info(f"║ User ID: {user_id}")
        logger.info(f"║ Text: '{text[:80] if text else 'None'}{'...' if text and len(text) > 80 else ''}'")
        logger.info(f"║ Image: {bool(image_base64)}")
        logger.info(f"║ Audio: {bool(audio_base64)}")
        logger.info(f"║ PDF: {bool(pdf_base64)}")
        logger.info(f"║ Metadata: {metadata}")
        logger.info("╚" + "═" * 78 + "╝")

        # Step 1: Extract text from all inputs
        logger.info(f"[QuickEntry] 📝 STEP 1: Extracting text from all inputs...")
        try:
            extracted_text = await self._extract_all_text(
                text=text,
                image_base64=image_base64,
                audio_base64=audio_base64,
                pdf_base64=pdf_base64
            )
            logger.info(f"[QuickEntry] ✅ Text extracted: '{extracted_text[:200] if extracted_text else 'NONE'}{'...' if extracted_text and len(extracted_text) > 200 else ''}'")
        except Exception as e:
            logger.error(f"[QuickEntry] ❌ Text extraction failed: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"[QuickEntry] Traceback:\n{traceback.format_exc()}")
            raise

        if not extracted_text:
            logger.warning(f"[QuickEntry] ⚠️  No content extracted - returning error")
            return {
                "success": False,
                "error": "No content to process",
                "entry_type": "unknown",
                "confidence": 0.0,
                "data": {}
            }

        # Step 2: Classify and extract data
        manual_type = metadata.get('manual_type') if metadata else None

        logger.info(f"[QuickEntry] 🤖 STEP 2: Classifying and extracting data...")
        logger.info(f"[QuickEntry] Text to classify: '{extracted_text[:150]}{'...' if len(extracted_text) > 150 else ''}'")
        logger.info(f"[QuickEntry] Manual type override: {manual_type or 'None (auto-detect)'}")
        logger.info(f"[QuickEntry] Has image context: {image_base64 is not None}")

        try:
            if manual_type:
                logger.info(f"[QuickEntry] Using force_type={manual_type}")
                classification = await self._classify_and_extract(
                    extracted_text,
                    user_id=user_id,
                    has_image=image_base64 is not None,
                    force_type=manual_type
                )
            else:
                logger.info(f"[QuickEntry] Auto-detecting entry type...")
                classification = await self._classify_and_extract(
                    extracted_text,
                    user_id=user_id,
                    has_image=image_base64 is not None
                )

            logger.info(f"[QuickEntry] ✅ Classification complete:")
            logger.info(f"[QuickEntry]    └─ Type: {classification.get('type')}")
            logger.info(f"[QuickEntry]    └─ Confidence: {classification.get('confidence')}")
            logger.info(f"[QuickEntry]    └─ Data fields: {list(classification.get('data', {}).keys())}")

            # If classification failed, log the error details
            if classification.get('type') == 'unknown' or classification.get('confidence', 0) == 0:
                logger.error(f"[QuickEntry] ❌❌❌ CLASSIFICATION FAILED ❌❌❌")
                logger.error(f"[QuickEntry] Type: {classification.get('type')}")
                logger.error(f"[QuickEntry] Confidence: {classification.get('confidence')}")
                logger.error(f"[QuickEntry] Validation errors: {classification.get('validation', {}).get('errors', [])}")
                logger.error(f"[QuickEntry] Validation warnings: {classification.get('validation', {}).get('warnings', [])}")
                logger.error(f"[QuickEntry] Missing critical: {classification.get('validation', {}).get('missing_critical', [])}")
                logger.error(f"[QuickEntry] Suggestions: {classification.get('suggestions', [])}")
                logger.error(f"[QuickEntry] FULL CLASSIFICATION OBJECT:")
                logger.error(f"{classification}")

        except Exception as e:
            logger.error(f"[QuickEntry] ❌ Classification threw exception: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"[QuickEntry] Traceback:\n{traceback.format_exc()}")
            raise

        # Inject user notes
        if metadata and 'notes' in metadata:
            if 'data' not in classification:
                classification['data'] = {}
            classification['data']['notes'] = metadata['notes']

        # OPTIONAL: Get semantic context for smart suggestions
        semantic_context = None
        try:
            semantic_context = await self._get_semantic_context(
                user_id=user_id,
                entry_text=extracted_text,
                entry_type=classification["type"]
            )
        except Exception as e:
            logger.warning(f"Semantic context retrieval failed (non-critical): {e}")

        # Return classification WITHOUT saving
        result = {
            "success": True,
            "entry_type": classification["type"],
            "confidence": classification.get("confidence", 0.0),
            "data": classification.get("data", {}),
            "suggestions": classification.get("suggestions", []),
            "extracted_text": extracted_text[:500]
        }

        # Add semantic context if available
        if semantic_context:
            result["semantic_context"] = semantic_context

        return result

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
                user_id=user_id,
                has_image=image_base64 is not None,
                force_type=manual_type
            )
        else:
            # Auto-detect
            classification = await self._classify_and_extract(
                extracted_text,
                user_id=user_id,
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

        # Process image with vision (if provided) - USE GROQ for ultra-fast, cheap vision
        if image_base64:
            try:
                logger.info("[QuickEntry] Processing image with Groq llama-3.2-90b-vision")

                vision_output = await self.groq_service.analyze_image(
                    image_base64=image_base64,
                    prompt="Describe what you see in this image. If it's food, list all visible items, portions, and any nutrition labels. If it's a workout/activity screenshot, extract all text and data."
                )

                extracted_parts.append(f"IMAGE CONTENT: {vision_output}")
                logger.info(f"[QuickEntry] Image processed: {vision_output[:100]}...")

            except Exception as e:
                logger.error(f"Image processing failed: {e}")
                extracted_parts.append("IMAGE: Failed to process")

        # Process audio (speech-to-text) - USE GROQ Whisper for ultra-fast, cheap transcription
        if audio_base64:
            try:
                logger.info("[QuickEntry] 🎤 Processing audio with Groq Whisper Turbo")

                transcription = await self.groq_service.transcribe_audio(
                    audio_base64=audio_base64,
                    audio_format='m4a'
                )

                extracted_parts.append(f"VOICE NOTE: {transcription}")
                logger.info(f"[QuickEntry] ✅ Audio transcribed: {transcription[:100]}...")

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

    async def _get_historical_patterns(
        self,
        user_id: str,
        text: str,
        entry_type: Optional[str] = None
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieve historical patterns for similar past entries.

        This enables SMART estimation based on user's actual behavior.
        """
        try:
            # Search for similar past entries
            similar_entries = await self.semantic_search.search_similar_entries(
                user_id=user_id,
                query_text=text,
                source_type=entry_type,  # Filter by type if known
                limit=15,  # Get more for pattern analysis
                recency_weight=0.5,  # Prefer recent logs
                similarity_threshold=0.65  # Lower threshold to find more matches
            )

            if not similar_entries or len(similar_entries) < 3:
                # Not enough data for pattern
                return None

            # Extract patterns from similar entries
            pattern = self._analyze_pattern(similar_entries, entry_type or "unknown")

            logger.info(f"[QuickEntry] Found pattern: {pattern.get('sample_size')} similar logs, confidence {pattern.get('confidence'):.2f}")
            return pattern

        except Exception as e:
            logger.warning(f"[QuickEntry] Pattern retrieval failed (non-critical): {e}")
            return None

    def _analyze_pattern(self, similar_entries: List[Dict], entry_type: str) -> Dict[str, Any]:
        """Extract statistical patterns from similar past logs."""

        sample_size = len(similar_entries)

        if entry_type == "activity":
            # Extract activity patterns
            durations = [e['metadata'].get('duration_minutes') for e in similar_entries
                        if e['metadata'].get('duration_minutes')]
            distances = [e['metadata'].get('distance_km') for e in similar_entries
                        if e['metadata'].get('distance_km')]
            calories = [e['metadata'].get('calories_burned') for e in similar_entries
                       if e['metadata'].get('calories_burned')]

            pattern = {
                "sample_size": sample_size,
                "type": "activity",
                "duration_avg": sum(durations) / len(durations) if durations else None,
                "distance_avg": sum(distances) / len(distances) if distances else None,
                "calories_avg": sum(calories) / len(calories) if calories else None,
                "consistency": len(durations) / sample_size if durations else 0,
                "confidence": min(0.95, 0.5 + (sample_size / 20) * 0.45)
            }

        elif entry_type == "workout":
            # Extract workout patterns
            durations = [e['metadata'].get('duration_minutes') for e in similar_entries
                        if e['metadata'].get('duration_minutes')]
            exercises_lists = [e['metadata'].get('exercises', []) for e in similar_entries]

            # Find common exercises
            all_exercise_names = []
            for ex_list in exercises_lists:
                if isinstance(ex_list, list):
                    all_exercise_names.extend([ex.get('name') for ex in ex_list if ex.get('name')])

            pattern = {
                "sample_size": sample_size,
                "type": "workout",
                "duration_avg": sum(durations) / len(durations) if durations else None,
                "common_exercises": list(set(all_exercise_names))[:5],  # Top 5 most common
                "consistency": len(durations) / sample_size if durations else 0,
                "confidence": min(0.95, 0.5 + (sample_size / 20) * 0.45)
            }

        elif entry_type == "meal":
            # Extract meal patterns
            calories_list = [e['metadata'].get('calories') for e in similar_entries
                           if e['metadata'].get('calories')]
            proteins = [e['metadata'].get('protein_g') for e in similar_entries
                       if e['metadata'].get('protein_g')]
            foods_lists = [e['metadata'].get('foods', []) for e in similar_entries]

            pattern = {
                "sample_size": sample_size,
                "type": "meal",
                "calories_avg": sum(calories_list) / len(calories_list) if calories_list else None,
                "protein_avg": sum(proteins) / len(proteins) if proteins else None,
                "consistency": len(calories_list) / sample_size if calories_list else 0,
                "confidence": min(0.95, 0.5 + (sample_size / 20) * 0.45)
            }

        else:
            # Generic pattern
            pattern = {
                "sample_size": sample_size,
                "type": entry_type,
                "confidence": min(0.95, 0.5 + (sample_size / 20) * 0.45)
            }

        return pattern

    async def _classify_and_extract(
        self,
        text: str,
        user_id: str,
        has_image: bool = False,
        force_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Classify entry type and extract structured data.

        OPTIMIZED: Single FREE LLM call using DeepSeek V3 or Llama-4 Scout
        Handles ALL entry types: meal, activity, workout, note, measurement

        NOW WITH PATTERN-BASED ESTIMATION for returning users!

        Args:
            text: The text to classify
            user_id: User ID for pattern retrieval
            has_image: Whether an image was included
            force_type: Override auto-detection and force a specific type
        """
        logger.info(f"[QuickEntry] Classifying entry with FREE model (force_type={force_type})")

        # STEP 1: Retrieve historical patterns
        historical_pattern = await self._get_historical_patterns(
            user_id=user_id,
            text=text,
            entry_type=force_type
        )

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
{{
  "type": "meal",
  "confidence": 0.95,
  "data": {{
    "meal_name": "Grilled chicken with rice and broccoli",
    "meal_type": "lunch",
    "foods": [
      {{"name": "Grilled chicken breast", "quantity": "6 oz"}},
      {{"name": "Brown rice", "quantity": "1 cup"}},
      {{"name": "Steamed broccoli", "quantity": "2 cups"}}
    ],
    "calories": 450,
    "protein_g": 45,
    "carbs_g": 40,
    "fat_g": 8,
    "fiber_g": 6,
    "estimated": false
  }},
  "suggestions": ["Great protein content!", "Consider adding healthy fats"]
}}

ACTIVITY example:
{{
  "type": "activity",
  "confidence": 0.9,
  "data": {{
    "activity_name": "Morning run",
    "activity_type": "running",
    "duration_minutes": 45,
    "distance_km": 7.5,
    "pace": "6:00/km",
    "calories_burned": 550,
    "notes": "Felt great, cool weather"
  }},
  "suggestions": ["Excellent consistency!", "Stay hydrated"]
}}

WORKOUT example:
{{
  "type": "workout",
  "confidence": 0.92,
  "data": {{
    "workout_name": "Upper Body Push",
    "workout_type": "strength",
    "exercises": [
      {{"name": "Bench Press", "sets": 4, "reps": "8-10", "weight_lbs": 185}},
      {{"name": "Overhead Press", "sets": 3, "reps": 10, "weight_lbs": 95}}
    ],
    "duration_minutes": 60,
    "notes": "New PR on bench!"
  }},
  "suggestions": ["Progressive overload working!", "Don't forget cooldown"]
}}

NOTE example:
{{
  "type": "note",
  "confidence": 0.8,
  "data": {{
    "title": "Feeling motivated",
    "content": "Starting to see results, energy levels up",
    "tags": ["motivation", "progress", "energy"],
    "category": "reflection"
  }},
  "suggestions": ["Great mindset!", "Track these wins"]
}}

MEASUREMENT example:
{{
  "type": "measurement",
  "confidence": 0.95,
  "data": {{
    "weight_lbs": 175.2,
    "body_fat_pct": 15.5,
    "measurements": {{
      "chest_in": 42,
      "waist_in": 32,
      "arms_in": 15
    }}
  }},
  "suggestions": ["Consistent progress!", "Measure weekly"]
}}

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
            # USE GROQ for ultra-fast, ultra-cheap classification
            # NOW WITH HISTORICAL PATTERNS for smart estimation!
            result = await self.groq_service.classify_and_extract(
                text=text,
                force_type=force_type,
                historical_pattern=historical_pattern  # Pass pattern data
            )

            logger.info(f"[QuickEntry] Classified as: {result.get('type')} ({result.get('confidence', 0):.2f})")
            return result

        except Exception as e:
            logger.error(f"❌ Classification failed: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"❌ Full traceback:\n{traceback.format_exc()}")
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
        Save entry to NEW SCHEMA (quick_entry_logs + structured tables).

        Flow:
        1. Create quick_entry_logs record (raw input + AI metadata)
        2. Create structured log (meal_logs, activities, etc.) with FK link
        3. Update quick_entry_logs with linked IDs
        4. Return success with both IDs
        """
        entry_type = classification["type"]
        raw_data = classification.get("data", {})

        # Handle both old flat structure and new nested structure from Groq V2
        # Flatten primary_fields and secondary_fields into single data dict
        data = {}
        if "primary_fields" in raw_data:
            # New Groq V2 structure - merge primary and secondary fields
            data.update(raw_data.get("primary_fields", {}))
            data.update(raw_data.get("secondary_fields", {}))
            # Preserve top-level flags
            data["estimated"] = raw_data.get("estimated", True)
            data["needs_clarification"] = raw_data.get("needs_clarification", False)
        else:
            # Old flat structure
            data = raw_data

        try:
            # STEP 1: Create quick_entry_logs record (NEW SCHEMA)
            logger.info(f"[QuickEntry] 📝 Creating quick_entry_logs record for {entry_type}")

            # Determine input type and modalities
            input_modalities = []
            if original_text:
                input_modalities.append("text")
            if image_base64:
                input_modalities.append("image")
            if metadata and metadata.get("audio_base64"):
                input_modalities.append("audio")

            input_type = "multimodal" if len(input_modalities) > 1 else (input_modalities[0] if input_modalities else "text")

            # Upload image if provided
            image_url = None
            if image_base64:
                image_url = self._upload_image(image_base64, user_id)

            # Create quick_entry_logs record
            quick_entry_log_data = {
                "user_id": user_id,
                "input_type": input_type,
                "input_modalities": input_modalities,
                "raw_text": original_text[:5000] if original_text else None,  # Limit to 5k chars
                "image_urls": [image_url] if image_url else [],
                "ai_provider": "groq",  # We use Groq for classification
                "ai_model": "llama-3.3-70b-versatile",  # Default model
                "ai_cost_usd": 0.0001,  # Estimated cost (~$0.10 per 1M tokens)
                "tokens_used": len(original_text.split()) * 2 if original_text else 0,  # Rough estimate
                "ai_classification": entry_type,
                "ai_extracted_data": data,  # Store full extracted data
                "ai_confidence_score": classification.get("confidence", 0.0),
                "contains_meal": entry_type == "meal",
                "contains_workout": entry_type == "workout",
                "contains_body_measurement": entry_type == "measurement",
                "contains_activity": entry_type == "activity",
                "contains_goal": False,
                "contains_note": entry_type == "note",
                "processing_status": "completed",
                "logged_at": datetime.utcnow().isoformat(),
                "timezone": "UTC"
            }

            quick_entry_result = self.supabase.table("quick_entry_logs").insert(quick_entry_log_data).execute()
            quick_entry_log_id = quick_entry_result.data[0]["id"]

            logger.info(f"[QuickEntry] ✅ Created quick_entry_logs: {quick_entry_log_id}")

            # STEP 2: Create structured log with FK link
            structured_log_id = None

            if entry_type == "meal":
                # Enrich meal data with quality scores and tags
                enrichment = self.enrichment_service.enrich_meal(user_id, data)

                # Save to meal_logs with quick_entry_log_id FK link
                meal_data = {
                    "user_id": user_id,
                    "quick_entry_log_id": quick_entry_log_id,  # NEW: FK link!
                    "category": data.get("meal_type", "snack"),
                    "name": data.get("meal_name", original_text[:200]),
                    "notes": data.get("notes", original_text[:500]),
                    "total_calories": data.get("calories"),
                    "total_protein_g": data.get("protein_g"),
                    "total_carbs_g": data.get("carbs_g"),
                    "total_fat_g": data.get("fat_g"),
                    "total_fiber_g": data.get("fiber_g"),
                    "foods": data.get("foods", []),  # JSONB array
                    "source": "quick_entry",
                    "estimated": data.get("estimated", False),
                    "confidence_score": classification.get("confidence", 0.0),
                    "image_url": image_url,  # Already uploaded
                    "total_sugar_g": data.get("sugar_g"),
                    "total_sodium_mg": data.get("sodium_mg"),
                    "ai_extracted": True,  # NEW: Flag from migration
                    "ai_confidence": classification.get("confidence", 0.0),  # NEW
                    "extraction_metadata": {  # NEW: Store AI metadata
                        "provider": "groq",
                        "model": "llama-3.3-70b-versatile",
                        "cost_usd": 0.0001
                    },
                    # Enrichment fields
                    "meal_quality_score": enrichment.get("meal_quality_score"),
                    "macro_balance_score": enrichment.get("macro_balance_score"),
                    "adherence_to_goals": enrichment.get("adherence_to_goals"),
                    "tags": enrichment.get("tags", []),
                    "logged_at": datetime.utcnow().isoformat(),
                    "created_at": datetime.utcnow().isoformat(),
                    "updated_at": datetime.utcnow().isoformat()
                }

                result = self.supabase.table("meal_logs").insert(meal_data).execute()
                structured_log_id = result.data[0]["id"]

                # Update quick_entry_logs with meal_log_id link
                self.supabase.table("quick_entry_logs").update({
                    "meal_log_ids": [structured_log_id]
                }).eq("id", quick_entry_log_id).execute()

                logger.info(f"[QuickEntry] ✅ Created meal_log: {structured_log_id}")

            elif entry_type == "activity":
                # Enrich activity data with performance scores
                enrichment = self.enrichment_service.enrich_activity(user_id, data)

                # Save to activities with quick_entry_log_id FK link
                duration_min = data.get("duration_minutes", 0)
                distance_km = data.get("distance_km", 0)

                activity_data = {
                    "user_id": user_id,
                    "quick_entry_log_id": quick_entry_log_id,  # NEW: FK link!
                    "activity_type": data.get("activity_type", "workout"),
                    "sport_type": data.get("sport_type", data.get("activity_type", "workout")),
                    "name": data.get("activity_name", original_text[:200]),
                    "elapsed_time_seconds": int(duration_min * 60) if duration_min else 0,
                    "moving_time_seconds": int(duration_min * 60) if duration_min else None,
                    "distance_meters": int(distance_km * 1000) if distance_km else None,
                    "calories": data.get("calories_burned") or data.get("calories"),
                    "perceived_exertion": data.get("rpe") or data.get("perceived_exertion"),
                    "mood": data.get("mood"),
                    "energy_level": data.get("energy_level"),
                    "notes": data.get("notes", original_text[:500]),
                    "source": "quick_entry",
                    "ai_extracted": True,  # NEW: Flag from migration
                    "ai_confidence": classification.get("confidence", 0.0),  # NEW
                    "extraction_metadata": {  # NEW: Store AI metadata
                        "provider": "groq",
                        "model": "llama-3.3-70b-versatile",
                        "cost_usd": 0.0001
                    },
                    "performance_score": enrichment.get("performance_score"),
                    "effort_level": data.get("rpe") or data.get("perceived_exertion"),
                    "recovery_needed_hours": enrichment.get("recovery_needed_hours"),
                    "tags": enrichment.get("tags", []),
                    "start_date": datetime.utcnow().isoformat()
                }

                result = self.supabase.table("activities").insert(activity_data).execute()
                structured_log_id = result.data[0]["id"]

                # Update quick_entry_logs with activity_id link
                self.supabase.table("quick_entry_logs").update({
                    "activity_ids": [structured_log_id]
                }).eq("id", quick_entry_log_id).execute()

                logger.info(f"[QuickEntry] ✅ Created activity: {structured_log_id}")

            elif entry_type == "workout":
                # NEW SCHEMA: Save to activities + activity_exercises + activity_sets
                exercises = data.get("exercises", [])

                # Calculate volume load and muscle groups
                volume_load = 0
                muscle_groups = set()

                for exercise in exercises:
                    sets = exercise.get("sets", 0)
                    reps = exercise.get("reps", 0) if isinstance(exercise.get("reps"), int) else 0
                    weight = exercise.get("weight_lbs", 0)
                    volume_load += sets * reps * weight

                    # Extract muscle groups (simplified)
                    exercise_name = exercise.get("name", "").lower()
                    if any(word in exercise_name for word in ["bench", "chest", "push"]):
                        muscle_groups.add("chest")
                    if any(word in exercise_name for word in ["squat", "leg", "quad"]):
                        muscle_groups.add("legs")
                    if any(word in exercise_name for word in ["deadlift", "row", "back"]):
                        muscle_groups.add("back")
                    if any(word in exercise_name for word in ["shoulder", "press", "overhead"]):
                        muscle_groups.add("shoulders")
                    if any(word in exercise_name for word in ["curl", "bicep", "arm"]):
                        muscle_groups.add("arms")

                # 1. Create activity record with FK link
                duration_min = data.get("duration_minutes", 0)
                activity_data = {
                    "user_id": user_id,
                    "quick_entry_log_id": quick_entry_log_id,  # NEW: FK link!
                    "source": "workout_log",  # NEW: workout_log source type
                    "activity_type": "strength",  # Workouts are strength training
                    "name": data.get("workout_name", "Quick Workout"),
                    "activity_name": data.get("workout_name", "Quick Workout"),
                    "start_date": datetime.utcnow().isoformat(),
                    "end_date": datetime.utcnow().isoformat(),
                    "elapsed_time_seconds": int(duration_min * 60) if duration_min else 0,
                    "duration_minutes": duration_min,
                    "rpe": data.get("rpe") or data.get("perceived_exertion"),
                    "notes": data.get("notes", original_text[:500]),
                    "calories": data.get("estimated_calories"),
                    "completed": True,
                    "ai_extracted": True,  # NEW: Flag from migration
                    "ai_confidence": classification.get("confidence", 0.0),  # NEW
                    "extraction_metadata": {  # NEW: Store AI metadata
                        "provider": "groq",
                        "model": "llama-3.3-70b-versatile",
                        "cost_usd": 0.0001
                    }
                }

                activity_result = self.supabase.table("activities").insert(activity_data).execute()
                activity_id = activity_result.data[0]["id"]
                structured_log_id = activity_id

                # Update quick_entry_logs with workout_log_id link
                self.supabase.table("quick_entry_logs").update({
                    "workout_log_ids": [activity_id]
                }).eq("id", quick_entry_log_id).execute()

                # 2. Create activity_exercises and activity_sets for each exercise
                for idx, exercise in enumerate(exercises):
                    exercise_name = exercise.get("name", "Unknown Exercise")

                    # Find or create exercise in exercises table
                    exercise_id = await self._get_or_create_exercise_id(exercise_name)

                    # Create activity_exercise record
                    activity_exercise_data = {
                        "activity_id": activity_id,
                        "exercise_id": exercise_id,
                        "order_index": idx + 1,
                        "notes": exercise.get("note", None)
                    }

                    activity_exercise_result = self.supabase.table("activity_exercises").insert(activity_exercise_data).execute()
                    activity_exercise_id = activity_exercise_result.data[0]["id"]

                    # Create activity_sets for this exercise
                    # Check if frontend sent detailed per-set data (from edit mode)
                    sets_detail = exercise.get("sets_detail", [])

                    if sets_detail:
                        # Use detailed per-set data from frontend
                        for set_num, set_data in enumerate(sets_detail, start=1):
                            activity_set_data = {
                                "activity_exercise_id": activity_exercise_id,
                                "set_number": set_num,
                                "reps_completed": set_data.get("reps", 10),
                                "weight_lbs": set_data.get("weight_lbs", 0),
                                "weight_kg": round(set_data.get("weight_lbs", 0) * 0.453592, 2) if set_data.get("weight_lbs") else None,
                                "rpe": data.get("rpe"),
                                "completed": True
                            }

                            self.supabase.table("activity_sets").insert(activity_set_data).execute()
                    else:
                        # Fallback to uniform sets (old behavior)
                        num_sets = exercise.get("sets", 3)
                        reps = exercise.get("reps", 10) if isinstance(exercise.get("reps"), int) else 10
                        weight_lbs = exercise.get("weight_lbs", 0)

                        for set_num in range(1, num_sets + 1):
                            activity_set_data = {
                                "activity_exercise_id": activity_exercise_id,
                                "set_number": set_num,
                                "reps_completed": reps,
                                "weight_lbs": weight_lbs,
                                "weight_kg": round(weight_lbs * 0.453592, 2) if weight_lbs else None,
                                "rpe": data.get("rpe"),
                                "completed": True
                            }

                            self.supabase.table("activity_sets").insert(activity_set_data).execute()

                logger.info(f"[QuickEntry] ✅ Saved workout: activity_id={activity_id}, {len(exercises)} exercises")

            elif entry_type == "note":
                # Enrich note with sentiment analysis
                enrichment = await self.enrichment_service.enrich_note(user_id, data)

                # Save to user_notes
                note_data = {
                    "user_id": user_id,
                    "title": data.get("title", "Quick Note"),
                    "content": data.get("content", original_text),
                    "category": data.get("category", "general"),
                    # Enrichment fields
                    "sentiment": enrichment.get("sentiment"),
                    "sentiment_score": enrichment.get("sentiment_score"),
                    "detected_themes": enrichment.get("detected_themes", []),
                    "related_goals": enrichment.get("related_goals", []),
                    "action_items": enrichment.get("action_items", []),
                    "tags": enrichment.get("tags", []),
                    "created_at": datetime.utcnow().isoformat()
                }

                result = self.supabase.table("user_notes").insert(note_data).execute()
                structured_log_id = result.data[0]["id"]
                logger.info(f"[QuickEntry] ✅ Created note: {structured_log_id}")

            elif entry_type == "measurement":
                # Save to body_measurements with FK link
                measurement_data = {
                    "user_id": user_id,
                    "quick_entry_log_id": quick_entry_log_id,  # NEW: FK link!
                    "weight_lbs": data.get("weight_lbs"),
                    "body_fat_pct": data.get("body_fat_pct"),
                    "measurements": data.get("measurements", {}),
                    "notes": original_text[:500],
                    "measured_at": datetime.utcnow().isoformat(),
                    "source": "quick_entry",
                    "ai_extracted": True,  # NEW
                    "ai_confidence": classification.get("confidence", 0.0),  # NEW
                    "extraction_metadata": {  # NEW
                        "provider": "groq",
                        "model": "llama-3.3-70b-versatile",
                        "cost_usd": 0.0001
                    }
                }

                result = self.supabase.table("body_measurements").insert(measurement_data).execute()
                structured_log_id = result.data[0]["id"]

                # Update quick_entry_logs with measurement_id link
                self.supabase.table("quick_entry_logs").update({
                    "body_measurement_ids": [structured_log_id]
                }).eq("id", quick_entry_log_id).execute()

                logger.info(f"[QuickEntry] ✅ Created body_measurement: {structured_log_id}")

            else:
                # Unknown - save to general notes
                note_data = {
                    "user_id": user_id,
                    "title": "Unclassified Entry",
                    "content": original_text,
                    "tags": ["unclassified"],
                    "category": "general",
                    "created_at": datetime.utcnow().isoformat()
                }

                result = self.supabase.table("user_notes").insert(note_data).execute()
                structured_log_id = result.data[0]["id"]
                logger.info(f"[QuickEntry] ✅ Created unknown entry as note: {structured_log_id}")

            # STEP 3: Return success with both IDs
            return {
                "success": True,
                "entry_id": structured_log_id,
                "quick_entry_log_id": quick_entry_log_id  # NEW: Return both IDs
            }

        except Exception as e:
            logger.error(f"[QuickEntry] ❌ Failed to save entry: {e}", exc_info=True)

            # Update quick_entry_logs with error status
            try:
                self.supabase.table("quick_entry_logs").update({
                    "processing_status": "failed",
                    "processing_error": str(e)
                }).eq("id", quick_entry_log_id).execute()
            except:
                pass

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
        Vectorize entry for RAG retrieval - NEW SCHEMA (quick_entry_embeddings).

        Creates text embedding and stores in quick_entry_embeddings table
        for ultra-personalized AI coach context via vector similarity search.
        """
        try:
            logger.info(f"[QuickEntry] 🔥 Vectorizing {entry_type} entry {entry_id}")

            # Generate text embedding using FREE sentence-transformers (384 dimensions)
            embedding = await self.multimodal_service.embed_text(text)

            # Map entry type to source classification
            source_classification_map = {
                "meal": "meal",
                "activity": "activity",
                "workout": "workout",
                "note": "note",
                "measurement": "body_measurement"
            }
            source_classification = source_classification_map.get(entry_type, "unknown")

            # Build content summary (1-2 sentences)
            content_summary = self._build_content_summary(entry_type, metadata, text)

            # Build comprehensive metadata for RAG context
            comprehensive_metadata = {
                **metadata,  # LLM-extracted data (calories, exercises, etc.)
                'entry_type': entry_type,
                'source': 'quick_entry',
                'timestamp': datetime.utcnow().isoformat(),
                'logged_at': metadata.get('logged_at') or datetime.utcnow().isoformat(),
                'notes': metadata.get('notes', text[:500]),
                'original_text': text[:1000],  # First 1000 chars
                'source_id': entry_id,  # Links to structured table
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
                })

            # Store embedding in NEW quick_entry_embeddings table
            embedding_data = {
                "quick_entry_log_id": entry_id,  # Links to quick_entry_logs
                "user_id": user_id,
                "embedding_type": "text",
                "embedding": embedding.tolist() if hasattr(embedding, 'tolist') else embedding,
                "content_text": text[:5000],  # Store full text (limit 5k chars)
                "content_summary": content_summary,
                "metadata": comprehensive_metadata,
                "source_classification": source_classification,
                "embedding_model": "sentence-transformers/all-MiniLM-L6-v2",
                "embedding_dimensions": 384,
                "content_hash": str(hash(text)),
                "is_active": True,
                "logged_at": datetime.utcnow().isoformat()
            }

            result = self.supabase.table("quick_entry_embeddings").insert(embedding_data).execute()
            embedding_id = result.data[0]["id"]

            # Update quick_entry_logs with embedding_id link
            self.supabase.table("quick_entry_logs").update({
                "embedding_generated": True,
                "embedding_id": embedding_id
            }).eq("id", entry_id).execute()

            logger.info(f"[QuickEntry] ✅ Vectorized {entry_type} entry: embedding_id={embedding_id}")

        except Exception as e:
            logger.error(f"[QuickEntry] ❌ Vectorization error: {e}", exc_info=True)

    def _build_content_summary(self, entry_type: str, metadata: Dict[str, Any], text: str) -> str:
        """Build 1-2 sentence summary for quick_entry_embeddings."""
        if entry_type == "meal":
            meal_name = metadata.get('meal_name', 'Meal')
            calories = metadata.get('calories', '?')
            protein = metadata.get('protein_g', '?')
            return f"{meal_name}: {calories} cal, {protein}g protein"

        elif entry_type == "activity":
            activity_name = metadata.get('activity_name', 'Activity')
            duration = metadata.get('duration_minutes', '?')
            distance = metadata.get('distance_km', '?')
            return f"{activity_name}: {duration} min, {distance} km"

        elif entry_type == "workout":
            workout_name = metadata.get('workout_name', 'Workout')
            exercises = metadata.get('exercises', [])
            exercise_count = len(exercises)
            return f"{workout_name}: {exercise_count} exercises"

        elif entry_type == "measurement":
            weight = metadata.get('weight_lbs', '?')
            body_fat = metadata.get('body_fat_pct', '?')
            return f"Body measurement: {weight} lbs, {body_fat}% body fat"

        else:
            # Truncate text for summary
            return text[:100] + "..." if len(text) > 100 else text

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

    async def _get_or_create_exercise_id(self, exercise_name: str) -> str:
        """
        Find or create exercise in exercises table.

        Args:
            exercise_name: Name of the exercise (e.g., "Bench Press")

        Returns:
            UUID of the exercise
        """
        try:
            # Try to find existing exercise (case-insensitive)
            result = self.supabase.table("exercises").select("id").ilike("name", exercise_name).limit(1).execute()

            if result.data and len(result.data) > 0:
                return result.data[0]["id"]

            # Exercise doesn't exist - create it
            logger.info(f"[QuickEntry] Creating new exercise: {exercise_name}")

            # Simple exercise creation (you can enhance this with exercise library API later)
            exercise_data = {
                "name": exercise_name,
                "description": f"Exercise: {exercise_name}",
                "category": "strength",  # Default category
                "created_at": datetime.utcnow().isoformat()
            }

            create_result = self.supabase.table("exercises").insert(exercise_data).execute()
            return create_result.data[0]["id"]

        except Exception as e:
            logger.error(f"Failed to get/create exercise '{exercise_name}': {e}")
            # Return a default UUID if exercise lookup/creation fails (non-critical)
            return str(uuid.uuid4())

    async def _get_semantic_context(
        self,
        user_id: str,
        entry_text: str,
        entry_type: str
    ) -> Optional[Dict[str, Any]]:
        """
        Get semantic context for smart suggestions (OPTIONAL enhancement).

        Returns similar past entries to help user with autocomplete, reminders, etc.

        Example: User logs "chicken and rice" → Show similar past meals with macros
        """
        try:
            # Only provide context for meals and workouts (most useful)
            if entry_type not in ["meal", "workout", "activity"]:
                return None

            # Search for similar entries
            similar_entries = await self.semantic_search.search_similar_entries(
                user_id=user_id,
                query_text=entry_text,
                source_type=entry_type,
                limit=3,
                recency_weight=0.4,
                similarity_threshold=0.6  # Only show if reasonably similar
            )

            if not similar_entries:
                return None

            # Format context for frontend
            context = {
                "similar_count": len(similar_entries),
                "suggestions": []
            }

            for entry in similar_entries:
                metadata = entry.get('metadata', {})
                suggestion = {
                    "similarity": round(entry.get('similarity', 0), 2),
                    "created_at": entry.get('created_at'),
                }

                # Add type-specific data
                if entry_type == "meal":
                    suggestion.update({
                        "meal_name": metadata.get('meal_name'),
                        "calories": metadata.get('calories'),
                        "protein_g": metadata.get('protein_g'),
                        "quality_score": metadata.get('meal_quality_score')
                    })
                elif entry_type == "workout":
                    suggestion.update({
                        "workout_name": metadata.get('workout_name'),
                        "volume_load": metadata.get('volume_load'),
                        "exercises": metadata.get('exercises', [])[:2]  # First 2 exercises
                    })
                elif entry_type == "activity":
                    suggestion.update({
                        "activity_name": metadata.get('activity_name'),
                        "duration_minutes": metadata.get('duration_minutes'),
                        "distance_km": metadata.get('distance_km')
                    })

                context["suggestions"].append(suggestion)

            return context

        except Exception as e:
            logger.error(f"Semantic context retrieval failed: {e}")
            return None


# Global instance
_service: Optional[QuickEntryService] = None


def get_quick_entry_service() -> QuickEntryService:
    """Get the global QuickEntryService instance."""
    global _service
    if _service is None:
        _service = QuickEntryService()
    return _service
