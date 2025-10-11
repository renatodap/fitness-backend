"""
Photo Meal Analysis Service

Analyzes meal photos using OpenAI Vision API to detect foods and portions.

IMPORTANT: This service does NOT estimate calories or macronutrients.
It only identifies foods and estimates quantities. All nutrition data
comes from the database via the food matching service.
"""

import logging
import base64
import json
from typing import Dict, Any, Optional, BinaryIO
from openai import AsyncOpenAI

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


# System prompt for OpenAI Vision
FOOD_DETECTION_SYSTEM_PROMPT = """You are a food detection AI. Analyze this meal photo and identify the foods and portions you see.

CRITICAL RULES:
- List each food item separately (don't group similar items)
- Estimate portions in BOTH common units (oz, cups, pieces, servings) AND grams when possible
- Be highly descriptive about the food (e.g., "grilled boneless skinless chicken breast" not just "chicken")
- Detect cooking methods when visible (grilled, fried, raw, baked, steamed, roasted)
- Include food preparation details (peeled, chopped, diced, whole)
- DO NOT estimate calories, protein, carbs, fats, or any macronutrients
- DO NOT provide nutrition advice or recommendations
- Output ONLY valid JSON in the exact format specified below

Output format (valid JSON only):
{
  "food_items": [
    {
      "name": "descriptive food name with cooking method",
      "quantity": "estimated quantity as string number",
      "unit": "common unit (oz, cup, piece, serving, tbsp, tsp, slice, etc.)",
      "grams": "estimated grams as string number (if determinable)"
    }
  ],
  "meal_type": "breakfast" | "lunch" | "dinner" | "snack",
  "description": "brief overall description of the meal"
}

Examples:
- "grilled chicken breast, boneless" not "chicken"
- "steamed broccoli florets" not "broccoli"
- "brown rice, cooked" not "rice"
- "fried egg, whole" not "egg"
"""


class PhotoMealAnalysisService:
    """Service for analyzing meal photos with OpenAI Vision API."""

    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_meal_photo(
        self,
        image_file: BinaryIO,
        filename: str,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Analyze a meal photo to detect foods and portions.

        Args:
            image_file: Image file binary stream
            filename: Original filename
            user_id: User ID for logging

        Returns:
            Dict with detected food items and meal metadata:
            {
                "food_items": [
                    {
                        "name": str,
                        "quantity": str,
                        "unit": str,
                        "grams": str (optional)
                    }
                ],
                "meal_type": str,
                "description": str,
                "raw_response": str (for debugging)
            }

        Raises:
            ValueError: If image analysis fails or returns invalid JSON
        """
        try:
            logger.info(f"Analyzing meal photo: user_id={user_id}, filename={filename}")

            # Read image and encode to base64
            image_data = image_file.read()
            base64_image = base64.b64encode(image_data).decode('utf-8')

            # Detect MIME type from filename extension
            mime_type = self._get_mime_type(filename)

            # Call OpenAI Vision API
            logger.info(f"Calling OpenAI Vision API: model=gpt-4o-mini")

            response = await self.client.chat.completions.create(
                model="gpt-4o-mini",  # Cost-effective vision model
                messages=[
                    {
                        "role": "system",
                        "content": FOOD_DETECTION_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text",
                                "text": "Analyze this meal photo and identify all foods with their quantities."
                            },
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{mime_type};base64,{base64_image}",
                                    "detail": "high"  # High detail for better food detection
                                }
                            }
                        ]
                    }
                ],
                max_tokens=1000,
                temperature=0.1  # Low temperature for consistent results
            )

            # Extract response
            raw_response = response.choices[0].message.content
            logger.info(f"OpenAI Vision response: {raw_response[:200]}...")

            # Parse JSON response
            try:
                parsed_result = json.loads(raw_response)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse OpenAI response as JSON: {e}")
                raise ValueError(f"OpenAI returned invalid JSON: {raw_response[:100]}")

            # Validate response structure
            if "food_items" not in parsed_result:
                raise ValueError("OpenAI response missing 'food_items' field")

            if not isinstance(parsed_result["food_items"], list):
                raise ValueError("'food_items' must be a list")

            # Validate each food item
            for idx, item in enumerate(parsed_result["food_items"]):
                if "name" not in item or "quantity" not in item or "unit" not in item:
                    logger.warning(f"Food item {idx} missing required fields: {item}")
                    continue

                # Ensure quantity and grams are strings
                if "quantity" in item:
                    item["quantity"] = str(item["quantity"])
                if "grams" in item:
                    item["grams"] = str(item["grams"])

            # Add metadata
            result = {
                "food_items": parsed_result["food_items"],
                "meal_type": parsed_result.get("meal_type", "lunch"),
                "description": parsed_result.get("description", "Photo-detected meal"),
                "raw_response": raw_response,
                "tokens_used": response.usage.total_tokens,
                "model": "gpt-4o-mini"
            }

            logger.info(
                f"✅ Photo analysis complete: detected {len(result['food_items'])} foods, "
                f"tokens={result['tokens_used']}"
            )

            return result

        except Exception as e:
            logger.error(f"Photo analysis failed: {e}", exc_info=True)
            raise

    def _get_mime_type(self, filename: str) -> str:
        """
        Determine MIME type from filename extension.

        Args:
            filename: Original filename

        Returns:
            MIME type string
        """
        extension = filename.lower().split('.')[-1]
        mime_types = {
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg',
            'png': 'image/png',
            'gif': 'image/gif',
            'webp': 'image/webp',
            'bmp': 'image/bmp'
        }
        return mime_types.get(extension, 'image/jpeg')


# Global instance
_service: Optional[PhotoMealAnalysisService] = None


def get_photo_meal_analysis_service() -> PhotoMealAnalysisService:
    """Get the global PhotoMealAnalysisService instance."""
    global _service
    if _service is None:
        _service = PhotoMealAnalysisService()
    return _service
