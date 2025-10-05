"""
Groq API Service V2 - Ultra-Accurate Extraction with UI-Optimized Output

Improvements over V1:
1. Conservative estimation - only estimate when confident
2. UI-friendly field structure - no JSON in frontend
3. Field visibility logic - show relevant fields first
4. Validation and confidence scoring
5. Better prompts with real-world examples
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


# Standard nutrition data for common foods (conservative estimates)
COMMON_FOODS = {
    "chicken breast": {"calories_per_oz": 47, "protein_per_oz": 8.8, "carbs_per_oz": 0, "fat_per_oz": 1},
    "ground beef (90/10)": {"calories_per_oz": 51, "protein_per_oz": 7.5, "carbs_per_oz": 0, "fat_per_oz": 2.8},
    "salmon": {"calories_per_oz": 58, "protein_per_oz": 8, "carbs_per_oz": 0, "fat_per_oz": 2.6},
    "eggs (large)": {"calories_each": 72, "protein_each": 6, "carbs_each": 0.4, "fat_each": 5},
    "white rice (cooked)": {"calories_per_cup": 205, "protein_per_cup": 4, "carbs_per_cup": 45, "fat_per_cup": 0.4},
    "brown rice (cooked)": {"calories_per_cup": 218, "protein_per_cup": 5, "carbs_per_cup": 46, "fat_per_cup": 1.6},
    "oatmeal (cooked)": {"calories_per_cup": 166, "protein_per_cup": 6, "carbs_per_cup": 28, "fat_per_cup": 3.6},
    "broccoli (cooked)": {"calories_per_cup": 55, "protein_per_cup": 4, "carbs_per_cup": 11, "fat_per_cup": 0.6},
    "sweet potato": {"calories_per_medium": 112, "protein_per_medium": 2, "carbs_per_medium": 26, "fat_per_medium": 0.1},
    "banana": {"calories_per_medium": 105, "protein_per_medium": 1.3, "carbs_per_medium": 27, "fat_per_medium": 0.4},
    "protein powder (whey)": {"calories_per_scoop": 120, "protein_per_scoop": 24, "carbs_per_scoop": 3, "fat_per_scoop": 1.5},
}


class GroqServiceV2:
    """
    Ultra-accurate Groq API client with UI-optimized output.
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
        Ultra-accurate classification and extraction with UI-friendly output.

        Returns structured data optimized for frontend display:
        - primary_fields: Show by default
        - secondary_fields: Show in "expand" section
        - validation: Errors and warnings
        - ui_hints: How to display fields
        """
        logger.info(f"[GroqV2] Classifying with ultra-accurate extraction")

        if force_type:
            classification_instruction = f"""This is a **{force_type}** entry. Extract all relevant {force_type} data."""
        else:
            classification_instruction = """Classify into ONE type:
- **meal**: Food/drink consumption
- **activity**: Cardio (running, cycling, swimming, sports)
- **workout**: Strength training (lifting, calisthenics)
- **measurement**: Body measurements (weight, body fat %, circumferences)
- **note**: Thoughts, feelings, goals, reflections
- **unknown**: Cannot determine"""

        system_prompt = f"""You are an ULTRA-PRECISE fitness data extraction assistant.

{classification_instruction}

ACCURACY RULES:
1. NEVER guess nutrition data without portion sizes
2. If portions missing, extract foods but set macros to null
3. Break down combo foods (e.g., "burger" → bun, patty, cheese, etc.)
4. Use standard units: oz, lbs, cups, grams, km, miles
5. Set confidence based on data quality (vague input = low confidence)
6. Provide helpful suggestions for improving data quality

Return ONLY valid JSON:
{{
  "type": "meal|activity|workout|measurement|note|unknown",
  "confidence": 0.0-1.0,
  "data": {{
    "primary_fields": {{
      // Fields to show BY DEFAULT in UI
    }},
    "secondary_fields": {{
      // Fields to show in EXPAND section
    }},
    "estimated": boolean,
    "needs_clarification": boolean
  }},
  "validation": {{
    "errors": [],
    "warnings": [],
    "missing_critical": []
  }},
  "suggestions": []
}}

MEAL EXAMPLES:

INPUT: "6oz grilled chicken, 1 cup brown rice, broccoli"
OUTPUT:
{{
  "type": "meal",
  "confidence": 0.9,
  "data": {{
    "primary_fields": {{
      "meal_name": "Grilled chicken with brown rice and broccoli",
      "meal_type": "lunch",
      "calories": 558,
      "protein_g": 63,
      "foods": [
        {{"name": "Grilled chicken breast", "quantity": "6 oz"}},
        {{"name": "Brown rice, cooked", "quantity": "1 cup"}},
        {{"name": "Broccoli", "quantity": "1 cup (estimated)"}}
      ]
    }},
    "secondary_fields": {{
      "carbs_g": 57,
      "fat_g": 8.6,
      "fiber_g": 9,
      "sugar_g": 3,
      "sodium_mg": 150,
      "foods_detailed": [
        {{
          "name": "Grilled chicken breast",
          "quantity": "6 oz",
          "calories": 280,
          "protein_g": 53,
          "carbs_g": 0,
          "fat_g": 6
        }},
        {{
          "name": "Brown rice, cooked",
          "quantity": "1 cup",
          "calories": 218,
          "protein_g": 5,
          "carbs_g": 46,
          "fat_g": 1.6
        }},
        {{
          "name": "Broccoli, steamed",
          "quantity": "1 cup",
          "calories": 55,
          "protein_g": 4,
          "carbs_g": 11,
          "fat_g": 0.6
        }}
      ],
      "tags": ["high-protein", "high-fiber", "balanced"]
    }},
    "estimated": true,
    "needs_clarification": false
  }},
  "validation": {{
    "errors": [],
    "warnings": ["Broccoli quantity estimated - specify portion for accuracy"],
    "missing_critical": []
  }},
  "suggestions": [
    "Great macro balance!",
    "For exact tracking, add broccoli portion (e.g., '2 cups')"
  ]
}}

INPUT: "chicken and rice"
OUTPUT:
{{
  "type": "meal",
  "confidence": 0.6,
  "data": {{
    "primary_fields": {{
      "meal_name": "Chicken and rice",
      "meal_type": "lunch",
      "calories": null,
      "protein_g": null,
      "foods": [
        {{"name": "Chicken", "quantity": "not specified"}},
        {{"name": "Rice", "quantity": "not specified"}}
      ]
    }},
    "secondary_fields": {{
      "carbs_g": null,
      "fat_g": null,
      "fiber_g": null,
      "tags": ["needs-portions"]
    }},
    "estimated": true,
    "needs_clarification": true
  }},
  "validation": {{
    "errors": [],
    "warnings": [],
    "missing_critical": ["portion_sizes", "nutrition_data"]
  }},
  "suggestions": [
    "Add portions for accurate tracking",
    "Example: '6oz chicken, 1 cup rice'",
    "Quick estimate: ~450 calories, ~50g protein (4-6oz chicken + 1 cup rice)"
  ]
}}

WORKOUT EXAMPLE:

INPUT: "bench press 4x8 @ 185lbs, incline db press 3x10 @ 70lbs"
OUTPUT:
{{
  "type": "workout",
  "confidence": 0.95,
  "data": {{
    "primary_fields": {{
      "workout_name": "Chest Press Workout",
      "duration_minutes": 45,
      "exercises": [
        {{
          "name": "Bench Press",
          "sets": 4,
          "reps": 8,
          "weight_lbs": 185,
          "weight_per_side": 67.5
        }},
        {{
          "name": "Incline Dumbbell Press",
          "sets": 3,
          "reps": 10,
          "weight_lbs": 70,
          "note": "70lbs per dumbbell"
        }}
      ]
    }},
    "secondary_fields": {{
      "volume_load": 8020,
      "muscle_groups": ["chest", "triceps", "shoulders"],
      "estimated_calories": 250,
      "rpe": null,
      "tags": ["push", "upper-body"]
    }},
    "estimated": false,
    "needs_clarification": false
  }},
  "validation": {{
    "errors": [],
    "warnings": [],
    "missing_critical": []
  }},
  "suggestions": [
    "Solid volume! 8,020 lbs total",
    "Add RPE (effort 1-10) for better tracking"
  ]
}}

ACTIVITY EXAMPLE:

INPUT: "ran 5 miles in 40 minutes"
OUTPUT:
{{
  "type": "activity",
  "confidence": 0.95,
  "data": {{
    "primary_fields": {{
      "activity_name": "Morning Run",
      "activity_type": "running",
      "distance_miles": 5,
      "distance_km": 8.05,
      "duration_minutes": 40,
      "pace": "8:00/mile (4:58/km)"
    }},
    "secondary_fields": {{
      "calories_burned": 550,
      "avg_heart_rate": null,
      "rpe": null,
      "tags": ["cardio", "running"]
    }},
    "estimated": true,
    "needs_clarification": false
  }},
  "validation": {{
    "errors": [],
    "warnings": ["Calories estimated based on average runner"],
    "missing_critical": []
  }},
  "suggestions": [
    "Great pace! 8:00/mile",
    "Add heart rate or RPE for better tracking"
  ]
}}

IMPORTANT:
- primary_fields = show by default
- secondary_fields = show in "More details" section
- Use null for unknown values (NEVER guess wildly)
- Set needs_clarification=true if critical data missing
- Provide actionable suggestions
"""

        user_prompt = f"""Extract fitness data from this entry:

"{text}"

Return structured JSON with primary_fields (show by default) and secondary_fields (expandable)."""

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

            # Override type if forced
            if force_type:
                result['type'] = force_type
                result['confidence'] = 1.0

            logger.info(f"[GroqV2] ✅ Classified: {result.get('type')} (confidence: {result.get('confidence', 0):.2f})")
            return result

        except Exception as e:
            logger.error(f"[GroqV2] ❌ Classification failed: {e}")
            return {
                "type": "unknown",
                "confidence": 0.0,
                "data": {
                    "primary_fields": {},
                    "secondary_fields": {},
                    "estimated": True,
                    "needs_clarification": True
                },
                "validation": {
                    "errors": [str(e)],
                    "warnings": [],
                    "missing_critical": ["all_data"]
                },
                "suggestions": ["Try being more specific", "Include details like amounts, duration, etc."]
            }

    async def analyze_image(
        self,
        image_base64: str,
        prompt: str = "Describe what you see in detail. If it's food, list ALL visible items with estimated portions. If it's a workout screenshot, extract ALL text and data."
    ) -> str:
        """Analyze image using Groq vision."""
        logger.info("[GroqV2] Analyzing image with llama-3.2-90b-vision")

        try:
            response = self.client.chat.completions.create(
                model="llama-3.2-90b-vision-preview",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {"type": "text", "text": prompt},
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
            logger.info(f"[GroqV2] ✅ Image analyzed")
            return result

        except Exception as e:
            logger.error(f"[GroqV2] ❌ Image analysis failed: {e}")
            return "Failed to analyze image"

    async def transcribe_audio(
        self,
        audio_base64: str,
        audio_format: str = "m4a"
    ) -> str:
        """Transcribe audio using Groq Whisper."""
        logger.info("[GroqV2] Transcribing audio with whisper-large-v3-turbo")

        try:
            audio_bytes = base64.b64decode(audio_base64)

            with tempfile.NamedTemporaryFile(delete=False, suffix=f'.{audio_format}') as temp_audio:
                temp_audio.write(audio_bytes)
                temp_audio_path = temp_audio.name

            try:
                with open(temp_audio_path, 'rb') as audio_file:
                    transcription_response = self.client.audio.transcriptions.create(
                        model="whisper-large-v3-turbo",
                        file=audio_file,
                        response_format="text"
                    )

                transcription = transcription_response if isinstance(transcription_response, str) else transcription_response.text
                logger.info(f"[GroqV2] ✅ Audio transcribed")
                return transcription

            finally:
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)

        except Exception as e:
            logger.error(f"[GroqV2] ❌ Audio transcription failed: {e}")
            return "Failed to transcribe audio"


# Global instance
_groq_service_v2: Optional[GroqServiceV2] = None


def get_groq_service_v2() -> GroqServiceV2:
    """Get the global GroqServiceV2 instance."""
    global _groq_service_v2
    if _groq_service_v2 is None:
        _groq_service_v2 = GroqServiceV2()
    return _groq_service_v2
