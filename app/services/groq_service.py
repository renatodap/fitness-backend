"""
Groq API Service for Ultra-Fast, Ultra-Cheap LLM Operations

Cost optimization using Groq's blazing-fast inference:
- llama-3.1-8b-instant: $0.05/1M tokens (classification)
- llama-3.2-90b-vision-preview: $0.90/1M tokens (image analysis)
- whisper-large-v3-turbo: $0.04/min (audio transcription)

Total cost per quick entry:
- Text only: $0.00013
- With image: $0.00026
- With audio: ~$0.0002

Compare to GPT-4: ~$0.015/entry (50x more expensive!)
"""

import logging
import base64
import json
import tempfile
import os
from typing import Any, Dict, List, Optional
from openai import OpenAI

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


class GroqService:
    """
    Groq API client for ultra-fast, ultra-cheap LLM inference.

    Uses Groq's OpenAI-compatible API with their lightning-fast LPU architecture.
    """

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )

    async def classify_and_extract(
        self,
        text: str,
        force_type: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Classify entry type and extract structured data using Groq llama-3.1-8b-instant.

        Cost: ~$0.00013 per classification (assuming ~2.5k tokens)
        Speed: ~840 tokens/sec (3x faster than GPT-4!)

        Args:
            text: The text to classify and extract data from
            force_type: Override auto-detection and force a specific type

        Returns:
            Classification result with type, confidence, data, suggestions
        """
        logger.info(f"[Groq] Classifying with llama-3.1-8b-instant (force_type={force_type})")

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
    // Type-specific fields
  }},
  "suggestions": ["helpful tips"]
}}

MEAL example:
{{
  "type": "meal",
  "confidence": 0.95,
  "data": {{
    "meal_name": "Grilled chicken with rice",
    "meal_type": "lunch",
    "foods": [
      {{"name": "Grilled chicken breast", "quantity": "6 oz", "calories": 250, "protein_g": 45, "carbs_g": 0, "fat_g": 6}},
      {{"name": "Brown rice", "quantity": "1 cup", "calories": 200, "protein_g": 5, "carbs_g": 40, "fat_g": 2}}
    ],
    "calories": 450,
    "protein_g": 50,
    "carbs_g": 40,
    "fat_g": 8,
    "fiber_g": 6,
    "sugar_g": 2,
    "sodium_mg": 400,
    "estimated": true,
    "tags": ["high-protein", "balanced"]
  }},
  "suggestions": ["Great protein content!", "Consider adding veggies"]
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
    "rpe": 7,
    "mood": "good",
    "energy_level": 4,
    "tags": ["cardio", "morning"],
    "notes": "Felt great, cool weather"
  }},
  "suggestions": ["Excellent consistency!"]
}}

WORKOUT example:
{{
  "type": "workout",
  "confidence": 0.92,
  "data": {{
    "workout_name": "Upper Body Push",
    "workout_type": "strength",
    "exercises": [
      {{"name": "Bench Press", "sets": 4, "reps": 8, "weight_lbs": 185, "rest_seconds": 120}},
      {{"name": "Overhead Press", "sets": 3, "reps": 10, "weight_lbs": 95, "rest_seconds": 90}}
    ],
    "duration_minutes": 60,
    "rpe": 8,
    "mood": "motivated",
    "energy_level": 4,
    "estimated_calories": 350,
    "tags": ["push", "chest", "shoulders"],
    "notes": "New PR on bench!"
  }},
  "suggestions": ["Progressive overload working!"]
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
      "hips_in": 38,
      "arms_in": 15
    }},
    "tags": ["weekly-checkin", "progress"]
  }},
  "suggestions": ["Consistent progress!"]
}}

NOTE example:
{{
  "type": "note",
  "confidence": 0.8,
  "data": {{
    "title": "Feeling motivated",
    "content": "Starting to see results, energy levels up",
    "category": "reflection",
    "tags": ["motivation", "progress", "energy"]
  }},
  "suggestions": ["Great mindset!"]
}}

IMPORTANT:
- Be intelligent about nutrition estimation
- Extract ALL numbers and details
- Add smart tags for categorization
- If foods are listed, structure them properly in the "foods" array
- Always return valid JSON
"""

        user_prompt = f"""Analyze this entry and extract structured data:

{text}

Return JSON classification and data extraction."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                response_format={"type": "json_object"},
                temperature=0.1,
                max_tokens=2048
            )

            result = json.loads(response.choices[0].message.content)

            # Override type if force_type is set
            if force_type:
                result['type'] = force_type
                result['confidence'] = 1.0

            logger.info(f"[Groq] ✅ Classified as: {result.get('type')} ({result.get('confidence', 0):.2f})")
            return result

        except Exception as e:
            logger.error(f"[Groq] ❌ Classification failed: {e}")
            return {
                "type": "unknown",
                "confidence": 0.0,
                "data": {},
                "suggestions": ["Try being more specific"]
            }

    async def analyze_image(
        self,
        image_base64: str,
        prompt: str = "Describe what you see in this image. If it's food, list all visible items, portions, and any nutrition labels. If it's a workout/activity screenshot, extract all text and data."
    ) -> str:
        """
        Analyze image using Groq llama-3.2-90b-vision-preview.

        Cost: ~$0.00090 per image (assuming ~1k tokens)
        Speed: Ultra-fast multimodal inference

        Args:
            image_base64: Base64-encoded image
            prompt: Custom prompt for image analysis

        Returns:
            Text description of image contents
        """
        logger.info("[Groq] Analyzing image with llama-3.2-90b-vision-preview")

        try:
            response = self.client.chat.completions.create(
                model="llama-3.2-90b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": prompt
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            }
                        ]
                    }
                ],
                temperature=0.1,
                max_tokens=1024
            )

            result = response.choices[0].message.content
            logger.info(f"[Groq] ✅ Image analyzed: {result[:100]}...")
            return result

        except Exception as e:
            logger.error(f"[Groq] ❌ Image analysis failed: {e}")
            return "Failed to analyze image"

    async def transcribe_audio(
        self,
        audio_base64: str,
        audio_format: str = "m4a"
    ) -> str:
        """
        Transcribe audio using Groq whisper-large-v3-turbo.

        Cost: $0.04/minute (extremely cheap!)
        Speed: Ultra-fast transcription (20x faster than OpenAI Whisper)

        Args:
            audio_base64: Base64-encoded audio
            audio_format: Audio file format (m4a, mp3, wav, etc.)

        Returns:
            Transcribed text
        """
        logger.info("[Groq] Transcribing audio with whisper-large-v3-turbo")

        try:
            # Decode audio
            audio_bytes = base64.b64decode(audio_base64)

            # Save to temp file (Groq API needs file object)
            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{audio_format}') as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name

            try:
                # Transcribe using Groq Whisper API
                with open(temp_audio_path, 'rb') as audio_file:
                    transcription_response = self.client.audio.transcriptions.create(
                        model="whisper-large-v3-turbo",
                        file=audio_file,
                        response_format="text"
                    )

                transcription = transcription_response if isinstance(transcription_response, str) else transcription_response.text
                logger.info(f"[Groq] ✅ Audio transcribed: {transcription[:100]}...")
                return transcription

            finally:
                # Clean up temp file
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)

        except Exception as e:
            logger.error(f"[Groq] ❌ Audio transcription failed: {e}")
            return "Failed to transcribe audio"


# Global instance
_groq_service: Optional[GroqService] = None


def get_groq_service() -> GroqService:
    """Get the global GroqService instance."""
    global _groq_service
    if _groq_service is None:
        _groq_service = GroqService()
    return _groq_service
