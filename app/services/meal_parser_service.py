"""
Meal Parser Service

Intelligent meal parsing using FREE AI models for natural language food logging.

OPTIMIZED: Using 100% FREE models with intelligent routing!
"""

import logging
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel
import json

from app.services.supabase_service import get_service_client
from app.services.dual_model_router import dual_router, TaskType, TaskConfig
from app.services.food_search_service import get_food_search_service

logger = logging.getLogger(__name__)


class ParsedFoodItem(BaseModel):
    """Parsed food item."""
    name: str
    brand: Optional[str] = None
    quantity: float
    unit: str
    food_id: Optional[str] = None
    nutrition: Dict[str, float]
    confidence: Literal["high", "medium", "low"]
    source: Literal["database", "openai", "estimate"]
    needs_confirmation: bool = False


class ParsedMeal(BaseModel):
    """Parsed meal with all food items."""
    meal_name: str
    category: Literal["breakfast", "lunch", "dinner", "snack"]
    logged_at: str
    foods: List[ParsedFoodItem]
    total_calories: float
    total_protein_g: float
    total_carbs_g: float
    total_fat_g: float
    confidence: Literal["high", "medium", "low"]
    warnings: List[str] = []
    requires_confirmation: bool = False


class MealParserService:
    """
    Service for parsing meal descriptions using AI.

    Uses OpenAI to extract structured food items from natural language
    and matches against food database for nutrition information.
    """

    def __init__(self):
        """Initialize with dual model router, Supabase clients, and food search service."""
        self.router = dual_router
        self.supabase = get_service_client()
        self.food_search = get_food_search_service()

    async def parse(
        self,
        description: str,
        user_id: Optional[str] = None
    ) -> ParsedMeal:
        """
        Parse natural language meal description.

        Args:
            description: Natural language meal description
            user_id: Optional user ID for personalized matching

        Returns:
            ParsedMeal with structured food items

        Raises:
            ValueError: If description is empty
        """
        if not description or not description.strip():
            raise ValueError("Description cannot be empty")

        # Step 1: Extract structured food items using LLM
        extracted = await self._extract_food_items(description)

        # Step 2: Match ALL foods against database in one batch (OPTIMIZED!)
        # Uses FoodSearchService's sophisticated 4-tier matching strategy
        parsed_foods = []
        warnings = []

        if user_id and extracted["foods"]:
            # Batch match all detected foods using sophisticated matching
            match_result = await self.food_search.match_detected_foods(
                detected_foods=extracted["foods"],
                user_id=user_id
            )

            # Convert matched foods to ParsedFoodItem format
            for matched in match_result["matched_foods"]:
                try:
                    parsed = self._convert_matched_to_parsed(matched)
                    parsed_foods.append(parsed)
                except Exception as e:
                    logger.error(f"Error converting matched food: {e}")
                    warnings.append(f"Could not parse: {matched.get('name', 'unknown')}")

            # Handle unmatched foods with AI estimation
            for unmatched in match_result["unmatched_foods"]:
                try:
                    # Find original detected food item
                    original_item = next(
                        (item for item in extracted["foods"] if item["name"] == unmatched["name"]),
                        None
                    )
                    if original_item:
                        parsed = await self._parse_food_item_fallback(original_item, warnings)
                        parsed_foods.append(parsed)
                        warnings.append(f"Using AI estimate for: {unmatched['name']} (not in database)")
                except Exception as e:
                    logger.error(f"Error estimating food item: {e}")
                    warnings.append(f"Could not estimate: {unmatched['name']}")
        else:
            # Fallback to old method if no user_id (shouldn't happen)
            for item in extracted["foods"]:
                try:
                    parsed = await self._parse_food_item_fallback(item, warnings)
                    parsed_foods.append(parsed)
                except Exception as e:
                    logger.error(f"Error parsing food item: {e}")
                    warnings.append(f"Could not parse: {item.get('name', 'unknown')}")

        # Step 3: Calculate totals
        totals = self._calculate_totals(parsed_foods)

        # Step 4: Determine overall confidence
        confidence = self._calculate_confidence(parsed_foods)
        requires_confirmation = any(f.needs_confirmation for f in parsed_foods)

        return ParsedMeal(
            meal_name=extracted.get("meal_name", "Meal"),
            category=extracted.get("category", "snack"),
            logged_at=extracted.get("logged_at", ""),
            foods=parsed_foods,
            total_calories=totals["calories"],
            total_protein_g=totals["protein"],
            total_carbs_g=totals["carbs"],
            total_fat_g=totals["fat"],
            confidence=confidence,
            warnings=warnings,
            requires_confirmation=requires_confirmation
        )

    async def _extract_food_items(self, description: str) -> Dict[str, Any]:
        """
        Extract structured food items from description using OpenAI.

        Args:
            description: Raw meal description

        Returns:
            Dict with meal_name, category, foods list
        """
        prompt = f"""Parse this meal description into structured data.
Extract each food item with quantity and unit.

Meal: {description}

Return JSON with:
- meal_name: descriptive name
- category: breakfast, lunch, dinner, or snack
- logged_at: ISO timestamp (use current time)
- foods: list of {{name, quantity, unit}}

Example output:
{{
  "meal_name": "Chicken and Rice",
  "category": "lunch",
  "logged_at": "2025-09-30T12:00:00Z",
  "foods": [
    {{"name": "grilled chicken breast", "quantity": 6, "unit": "oz"}},
    {{"name": "brown rice", "quantity": 1, "unit": "cup"}}
  ]
}}"""

        try:
            # OPTIMIZED: Use Groq for ULTRA FAST extraction with dual router
            response = await self.router.complete(
                config=TaskConfig(
                    type=TaskType.QUICK_CATEGORIZATION,
                    requires_json=True,
                    prioritize_speed=True  # Need instant meal parsing
                ),
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            logger.error(f"Error extracting food items: {e}")
            # Fallback
            return {
                "meal_name": "Meal",
                "category": "snack",
                "logged_at": "",
                "foods": [{"name": description, "quantity": 1, "unit": "serving"}]
            }

    def _convert_matched_to_parsed(
        self,
        matched: Dict[str, Any]
    ) -> ParsedFoodItem:
        """
        Convert FoodSearchService matched food to ParsedFoodItem format.

        Args:
            matched: Matched food from FoodSearchService (with detected_quantity, etc.)

        Returns:
            ParsedFoodItem with database nutrition
        """
        # Scale nutrition based on detected quantity
        serving_size = matched.get("serving_size", 1)
        detected_quantity = matched.get("detected_quantity", 1)
        detected_unit = matched.get("detected_unit", "serving")

        # Calculate multiplier (simplified - assumes units match)
        # In production, would need unit conversion
        multiplier = detected_quantity / serving_size if serving_size > 0 else detected_quantity

        nutrition = {
            "calories": (matched.get("calories", 0) or 0) * multiplier,
            "protein_g": (matched.get("protein_g", 0) or 0) * multiplier,
            "carbs_g": (matched.get("total_carbs_g", 0) or 0) * multiplier,
            "fat_g": (matched.get("total_fat_g", 0) or 0) * multiplier,
        }

        # Determine confidence based on match method and confidence score
        match_confidence = matched.get("match_confidence", 0.5)
        if match_confidence >= 0.9:
            confidence = "high"
        elif match_confidence >= 0.6:
            confidence = "medium"
        else:
            confidence = "low"

        return ParsedFoodItem(
            name=matched.get("name", "Unknown"),
            brand=matched.get("brand_name"),
            quantity=detected_quantity,
            unit=detected_unit,
            food_id=matched.get("id"),
            nutrition=nutrition,
            confidence=confidence,
            source="database",
            needs_confirmation=confidence != "high"  # Only high confidence doesn't need confirmation
        )

    async def _parse_food_item_fallback(
        self,
        item: Dict[str, Any],
        warnings: List[str]
    ) -> ParsedFoodItem:
        """
        Fallback food item parsing using AI estimation (when database match fails).

        Args:
            item: Extracted food item dict
            warnings: List to append warnings to

        Returns:
            ParsedFoodItem with AI-estimated nutrition
        """
        # Estimate nutrition with AI
        nutrition = await self._estimate_nutrition(item)

        return ParsedFoodItem(
            name=item["name"],
            quantity=item["quantity"],
            unit=item["unit"],
            nutrition=nutrition,
            confidence="medium",
            source="openai",
            needs_confirmation=True
        )

    async def _estimate_nutrition(self, item: Dict[str, Any]) -> Dict[str, float]:
        """
        Estimate nutrition using OpenAI.

        Args:
            item: Food item dict

        Returns:
            Dict with nutrition estimates
        """
        prompt = f"""Estimate nutrition for: {item['quantity']} {item['unit']} of {item['name']}

Return JSON with calories, protein_g, carbs_g, fat_g"""

        try:
            # OPTIMIZED: Use Groq for ULTRA FAST nutrition estimation with dual router
            response = await self.router.complete(
                config=TaskConfig(
                    type=TaskType.QUICK_CATEGORIZATION,
                    requires_json=True,
                    prioritize_speed=True  # Need instant nutrition estimates
                ),
                messages=[{"role": "user", "content": prompt}],
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            return json.loads(content)

        except Exception as e:
            logger.error(f"Error estimating nutrition: {e}")
            # Fallback estimates
            return {
                "calories": 200,
                "protein_g": 10,
                "carbs_g": 20,
                "fat_g": 8
            }

    def _scale_nutrition(
        self,
        base_nutrition: Dict[str, float],
        quantity: float,
        unit: str
    ) -> Dict[str, float]:
        """Scale nutrition based on quantity and unit."""
        # Simplified scaling (would need unit conversion in production)
        scale = quantity

        return {
            "calories": base_nutrition.get("calories", 0) * scale,
            "protein_g": base_nutrition.get("protein_g", 0) * scale,
            "carbs_g": base_nutrition.get("carbs_g", 0) * scale,
            "fat_g": base_nutrition.get("fat_g", 0) * scale,
        }

    def _calculate_totals(self, foods: List[ParsedFoodItem]) -> Dict[str, float]:
        """Calculate total nutrition."""
        return {
            "calories": sum(f.nutrition.get("calories", 0) for f in foods),
            "protein": sum(f.nutrition.get("protein_g", 0) for f in foods),
            "carbs": sum(f.nutrition.get("carbs_g", 0) for f in foods),
            "fat": sum(f.nutrition.get("fat_g", 0) for f in foods),
        }

    def _calculate_confidence(self, foods: List[ParsedFoodItem]) -> Literal["high", "medium", "low"]:
        """Calculate overall confidence level."""
        if not foods:
            return "low"

        confidences = [f.confidence for f in foods]

        if all(c == "high" for c in confidences):
            return "high"
        elif all(c in ["high", "medium"] for c in confidences):
            return "medium"
        else:
            return "low"
