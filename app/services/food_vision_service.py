"""
Food Vision Service - Isolated Image Analysis for Meal Detection

Analyzes food images using specialized APIs with intelligent fallbacks:
1. FatSecret Platform API (free tier, specialized for food)
2. OpenAI Vision API (gpt-4o-vision, fast and accurate)
3. Claude Vision API (fallback, already integrated)

Returns structured nutritional data + natural language description.
"""

import logging
import json
import base64
from typing import Dict, Any, Optional, Tuple
import httpx
from openai import AsyncOpenAI
from anthropic import AsyncAnthropic

from app.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class FoodVisionService:
    """
    Isolated service for analyzing food images.

    Architecture:
    1. User uploads image
    2. This service analyzes it (specialized API → OpenAI → Claude)
    3. Returns structured data + description
    4. Unified coach uses description in context
    """

    def __init__(self):
        self.openai_client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY) if hasattr(settings, 'OPENAI_API_KEY') else None
        self.anthropic_client = AsyncAnthropic(api_key=settings.ANTHROPIC_API_KEY)
        # FatSecret API credentials (if available)
        self.fatsecret_consumer_key = getattr(settings, 'FATSECRET_CONSUMER_KEY', None)
        self.fatsecret_consumer_secret = getattr(settings, 'FATSECRET_CONSUMER_SECRET', None)

    async def analyze_food_image(
        self,
        image_base64: str,
        user_message: str = ""
    ) -> Dict[str, Any]:
        """
        Analyze food image and return structured nutritional data.

        Args:
            image_base64: Base64 encoded image
            user_message: Optional text from user

        Returns:
            {
                "success": bool,
                "is_food": bool,
                "description": str,  # Natural language description for coach
                "food_items": [...],  # List of detected foods
                "nutrition": {
                    "calories": int,
                    "protein_g": float,
                    "carbs_g": float,
                    "fats_g": float
                },
                "meal_type": str,  # breakfast, lunch, dinner, snack
                "confidence": float,
                "api_used": str
            }
        """
        logger.info(f"[FoodVision] Starting food image analysis")

        # Try APIs in order of preference (cost + accuracy)

        # OPTION 1: FatSecret Platform API (if configured)
        if self.fatsecret_consumer_key and self.fatsecret_consumer_secret:
            logger.info(f"[FoodVision] Trying FatSecret API...")
            result = await self._analyze_with_fatsecret(image_base64, user_message)
            if result and result.get("success"):
                logger.info(f"[FoodVision] FatSecret analysis successful")
                return result

        # OPTION 2: OpenAI Vision API (fast, accurate, $0.01/1K tokens)
        if self.openai_client:
            logger.info(f"[FoodVision] Trying OpenAI Vision API...")
            result = await self._analyze_with_openai_vision(image_base64, user_message)
            if result and result.get("success"):
                logger.info(f"[FoodVision] OpenAI Vision analysis successful")
                return result

        # OPTION 3: Claude Vision API (fallback, already integrated)
        logger.info(f"[FoodVision] Falling back to Claude Vision API...")
        result = await self._analyze_with_claude_vision(image_base64, user_message)
        if result and result.get("success"):
            logger.info(f"[FoodVision] Claude Vision analysis successful")
            return result

        # All APIs failed
        logger.error(f"[FoodVision] All vision APIs failed")
        return {
            "success": False,
            "is_food": False,
            "description": "Unable to analyze image at this time.",
            "error": "All vision APIs failed",
            "api_used": "none"
        }

    async def _analyze_with_fatsecret(
        self,
        image_base64: str,
        user_message: str
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze with FatSecret Platform API.

        Note: FatSecret image recognition requires OAuth 2.0 authentication.
        This is a placeholder for the full implementation.
        """
        try:
            # TODO: Implement FatSecret OAuth 2.0 flow and image recognition
            # For now, skip to next API
            logger.warning(f"[FoodVision] FatSecret API not fully implemented yet")
            return None
        except Exception as e:
            logger.error(f"[FoodVision] FatSecret API failed: {e}")
            return None

    async def _analyze_with_openai_vision(
        self,
        image_base64: str,
        user_message: str
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze with OpenAI Vision API (gpt-4o-vision).

        Cost: ~$0.01/1K tokens (very affordable)
        Accuracy: High (85%+ based on benchmarks)
        """
        try:
            system_prompt = """You are a food recognition AI for a fitness app.

Analyze the image and determine:
1. Is this image showing food/meals? (yes/no)
2. If yes, identify all food items visible
3. Estimate portion sizes
4. Calculate approximate nutritional content (calories, protein, carbs, fats)
5. Determine meal type (breakfast, lunch, dinner, snack)

Return ONLY valid JSON (no markdown, no explanation):
{
    "is_food": true/false,
    "food_items": [
        {"name": "food name", "quantity": "amount", "unit": "g/oz/cups"}
    ],
    "nutrition": {
        "calories": estimated_total_calories,
        "protein_g": estimated_protein_grams,
        "carbs_g": estimated_carbs_grams,
        "fats_g": estimated_fats_grams
    },
    "meal_type": "breakfast/lunch/dinner/snack",
    "description": "Natural language description of the meal for coach context",
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation of analysis"
}

If NOT food, return:
{
    "is_food": false,
    "description": "Brief description of what the image shows",
    "confidence": 1.0
}"""

            user_prompt = f"Analyze this food image."
            if user_message:
                user_prompt += f"\n\nUser's message: {user_message}"

            response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Using mini for cost efficiency
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:image/jpeg;base64,{image_base64}"
                                }
                            },
                            {"type": "text", "text": user_prompt}
                        ]
                    }
                ],
                max_tokens=500,
                temperature=0.1  # Low temp for consistent analysis
            )

            # Parse JSON response
            response_text = response.choices[0].message.content.strip()

            # Clean markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()

            analysis = json.loads(response_text)

            # Add metadata
            analysis["success"] = True
            analysis["api_used"] = "openai_vision"

            logger.info(f"[FoodVision] OpenAI Vision: is_food={analysis.get('is_food')}, confidence={analysis.get('confidence')}")

            return analysis

        except Exception as e:
            logger.error(f"[FoodVision] OpenAI Vision failed: {e}", exc_info=True)
            return None

    async def _analyze_with_claude_vision(
        self,
        image_base64: str,
        user_message: str
    ) -> Optional[Dict[str, Any]]:
        """
        Analyze with Claude Vision API (claude-3-5-sonnet).

        Cost: $3/M input tokens, $15/M output tokens
        Accuracy: Very high (best for complex meals)
        """
        try:
            system_prompt = """You are a food recognition AI for a fitness app.

Analyze the image and determine:
1. Is this image showing food/meals? (yes/no)
2. If yes, identify all food items visible
3. Estimate portion sizes
4. Calculate approximate nutritional content (calories, protein, carbs, fats)
5. Determine meal type (breakfast, lunch, dinner, snack)

Return ONLY valid JSON (no markdown, no explanation):
{
    "is_food": true/false,
    "food_items": [
        {"name": "food name", "quantity": "amount", "unit": "g/oz/cups"}
    ],
    "nutrition": {
        "calories": estimated_total_calories,
        "protein_g": estimated_protein_grams,
        "carbs_g": estimated_carbs_grams,
        "fats_g": estimated_fats_grams
    },
    "meal_type": "breakfast/lunch/dinner/snack",
    "description": "Natural language description of the meal for coach context",
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation of analysis"
}

If NOT food, return:
{
    "is_food": false,
    "description": "Brief description of what the image shows",
    "confidence": 1.0
}"""

            user_prompt = "Analyze this food image."
            if user_message:
                user_prompt += f"\n\nUser's message: {user_message}"

            response = await self.anthropic_client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=800,
                temperature=0.1,
                system=system_prompt,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/jpeg",
                                    "data": image_base64
                                }
                            },
                            {"type": "text", "text": user_prompt}
                        ]
                    }
                ]
            )

            # Parse JSON response
            response_text = response.content[0].text.strip()

            # Clean markdown code blocks if present
            if response_text.startswith("```json"):
                response_text = response_text.replace("```json", "").replace("```", "").strip()
            elif response_text.startswith("```"):
                response_text = response_text.replace("```", "").strip()

            analysis = json.loads(response_text)

            # Add metadata
            analysis["success"] = True
            analysis["api_used"] = "claude_vision"

            logger.info(f"[FoodVision] Claude Vision: is_food={analysis.get('is_food')}, confidence={analysis.get('confidence')}")

            return analysis

        except Exception as e:
            logger.error(f"[FoodVision] Claude Vision failed: {e}", exc_info=True)
            return None


# Global instance
_food_vision_service: Optional[FoodVisionService] = None


def get_food_vision_service() -> FoodVisionService:
    """Get the global FoodVisionService instance."""
    global _food_vision_service
    if _food_vision_service is None:
        _food_vision_service = FoodVisionService()
    return _food_vision_service
