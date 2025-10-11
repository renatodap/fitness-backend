"""
Text Meal Parser Service

Parses natural language meal descriptions into structured food items.
Uses LLM to extract food names, quantities, and meal context.

This service is used when the coach detects meal logging intent from user's message.
It provides the first step in the text-based meal logging flow.
"""

import logging
import json
from typing import Dict, Any, List, Optional
from groq import AsyncGroq

from app.config import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)


# System prompt for meal parsing
MEAL_PARSING_SYSTEM_PROMPT = """You are a meal parsing AI. Extract structured food information from natural language meal descriptions.

CRITICAL RULES:
- Extract each food item separately
- Include cooking method if mentioned (grilled, fried, baked, steamed, etc.)
- If user specifies quantity, use their exact quantity and unit
- If NO quantity specified, use "1" and "serving" as defaults
- DO NOT add quantities if user didn't mention them - let "serving" indicate this
- Use database-friendly food names (e.g., "Chicken Breast, Grilled" not "grilled chicken")
- Detect meal type from context (breakfast, lunch, dinner, snack) or time of day

QUANTITY RULES:
✅ User says "6 oz of chicken" → quantity: "6", unit: "oz"
✅ User says "two cups of rice" → quantity: "2", unit: "cup"
✅ User says "a banana" → quantity: "1", unit: "serving"
✅ User says "chicken and rice" → quantity: "1", unit: "serving" (for each)

NAMING RULES:
- Use standard USDA-style names
- Include cooking method when mentioned
- "Chicken Breast, Grilled" NOT "grilled chicken breast"
- "Rice, White, Cooked" NOT "white rice"
- "Eggs, Scrambled" NOT "scrambled eggs"

Output ONLY valid JSON (no markdown):
{
  "food_items": [
    {
      "name": "database-friendly food name with cooking method",
      "quantity": "number as string",
      "unit": "oz|g|cup|piece|serving|tbsp|tsp|slice",
      "grams": null
    }
  ],
  "meal_type": "breakfast|lunch|dinner|snack",
  "description": "brief natural language summary of what was eaten"
}

Examples:

Input: "I had 6 oz of grilled chicken breast and a cup of brown rice for lunch"
Output:
{
  "food_items": [
    {"name": "Chicken Breast, Grilled", "quantity": "6", "unit": "oz", "grams": null},
    {"name": "Rice, Brown, Cooked", "quantity": "1", "unit": "cup", "grams": null}
  ],
  "meal_type": "lunch",
  "description": "grilled chicken breast and brown rice"
}

Input: "ate chicken and vegetables"
Output:
{
  "food_items": [
    {"name": "Chicken Breast, Cooked", "quantity": "1", "unit": "serving", "grams": null},
    {"name": "Vegetables, Mixed, Cooked", "quantity": "1", "unit": "serving", "grams": null}
  ],
  "meal_type": "lunch",
  "description": "chicken and vegetables"
}

Input: "breakfast: 3 eggs, 2 slices of toast, and a banana"
Output:
{
  "food_items": [
    {"name": "Eggs, Whole, Cooked", "quantity": "3", "unit": "piece", "grams": null},
    {"name": "Bread, White, Toast", "quantity": "2", "unit": "slice", "grams": null},
    {"name": "Banana, Raw", "quantity": "1", "unit": "piece", "grams": null}
  ],
  "meal_type": "breakfast",
  "description": "eggs, toast, and banana"
}

IMPORTANT:
- If quantity not specified, use "1" and "serving"
- The backend will use the food's standard serving size from database
- Focus on accurate food identification, the database provides nutrition
"""


class TextMealParserService:
    """Service for parsing natural language meal descriptions."""

    def __init__(self):
        self.groq_client = AsyncGroq(api_key=settings.GROQ_API_KEY)

    async def parse_meal_text(
        self,
        user_message: str,
        user_context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Parse natural language meal description into structured food items.

        Args:
            user_message: Natural language meal description from user
            user_context: Optional context (time of day, user preferences, etc.)

        Returns:
            Dict with parsed meal data:
            {
                "food_items": [
                    {
                        "name": str,
                        "quantity": str,
                        "unit": str,
                        "grams": None
                    }
                ],
                "meal_type": str,
                "description": str
            }

        Raises:
            ValueError: If parsing fails or returns invalid data
        """
        try:
            logger.info(f"Parsing meal text: {user_message[:100]}...")

            # Build user prompt
            user_prompt = user_message

            # Add context if provided
            if user_context:
                context_parts = []
                if "time_of_day" in user_context:
                    context_parts.append(f"Time: {user_context['time_of_day']}")
                if "recent_meals" in user_context:
                    context_parts.append(f"Recent meals: {user_context['recent_meals']}")

                if context_parts:
                    user_prompt = f"Context: {', '.join(context_parts)}\n\nUser message: {user_message}"

            # Call Groq with Llama 3.3 70B (cheap, fast, good at structured output)
            logger.info("Calling Groq API for meal parsing...")

            response = await self.groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",  # Fast and cheap
                messages=[
                    {
                        "role": "system",
                        "content": MEAL_PARSING_SYSTEM_PROMPT
                    },
                    {
                        "role": "user",
                        "content": user_prompt
                    }
                ],
                max_tokens=500,
                temperature=0.1  # Low temp for consistent parsing
            )

            # Extract response
            raw_response = response.choices[0].message.content
            logger.info(f"Groq response: {raw_response[:200]}...")

            # Clean markdown code blocks if present
            response_text = raw_response.strip()
            if response_text.startswith('```json'):
                response_text = response_text.replace('```json\n', '').replace('```', '').strip()
            elif response_text.startswith('```'):
                response_text = response_text.replace('```\n', '').replace('```', '').strip()

            # Parse JSON
            try:
                parsed_result = json.loads(response_text)
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse JSON: {e}")
                logger.error(f"Raw response: {response_text}")
                raise ValueError(f"LLM returned invalid JSON: {response_text[:100]}")

            # Validate response structure
            if "food_items" not in parsed_result:
                raise ValueError("Missing 'food_items' in parsed response")

            if not isinstance(parsed_result["food_items"], list):
                raise ValueError("'food_items' must be a list")

            if len(parsed_result["food_items"]) == 0:
                raise ValueError("No foods detected in message")

            # Validate each food item
            for idx, item in enumerate(parsed_result["food_items"]):
                if "name" not in item or "quantity" not in item or "unit" not in item:
                    logger.warning(f"Food item {idx} missing required fields: {item}")
                    continue

                # Ensure quantity is string
                if "quantity" in item:
                    item["quantity"] = str(item["quantity"])

                # Set grams to None if not present
                if "grams" not in item:
                    item["grams"] = None

            # Set defaults
            result = {
                "food_items": parsed_result["food_items"],
                "meal_type": parsed_result.get("meal_type", "lunch"),
                "description": parsed_result.get("description", user_message[:100]),
                "tokens_used": response.usage.total_tokens,
                "model": "llama-3.3-70b-versatile"
            }

            logger.info(
                f"✅ Meal parsing complete: {len(result['food_items'])} foods detected, "
                f"tokens={result['tokens_used']}"
            )

            return result

        except Exception as e:
            logger.error(f"Meal text parsing failed: {e}", exc_info=True)
            raise


# Global instance
_service: Optional[TextMealParserService] = None


def get_text_meal_parser_service() -> TextMealParserService:
    """Get the global TextMealParserService instance."""
    global _service
    if _service is None:
        _service = TextMealParserService()
    return _service
