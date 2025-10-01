"""
Meal Parser Service

Intelligent meal parsing using OpenAI for natural language food logging.
"""

import logging
from typing import Any, Dict, List, Literal, Optional
from pydantic import BaseModel
from openai import AsyncOpenAI
import json

from app.config import settings
from app.services.supabase_service import get_service_client

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
        """Initialize with OpenAI and Supabase clients."""
        self.openai = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.supabase = get_service_client()

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

        # Step 2: Match each food against database
        parsed_foods = []
        warnings = []

        for item in extracted["foods"]:
            try:
                parsed = await self._parse_food_item(item, warnings, user_id)
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
            response = await self.openai.chat.completions.create(
                model="gpt-4o-mini",
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

    async def _parse_food_item(
        self,
        item: Dict[str, Any],
        warnings: List[str],
        user_id: Optional[str]
    ) -> ParsedFoodItem:
        """
        Parse individual food item.

        Args:
            item: Extracted food item dict
            warnings: List to append warnings to
            user_id: Optional user ID

        Returns:
            ParsedFoodItem with nutrition info
        """
        # Try database match first
        db_match = await self._search_food_database(item["name"])

        if db_match:
            # Use database nutrition
            nutrition = self._scale_nutrition(
                db_match["nutrition"],
                item["quantity"],
                item["unit"]
            )

            return ParsedFoodItem(
                name=db_match["name"],
                brand=db_match.get("brand"),
                quantity=item["quantity"],
                unit=item["unit"],
                food_id=db_match["id"],
                nutrition=nutrition,
                confidence="high",
                source="database",
                needs_confirmation=False
            )

        else:
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

    async def _search_food_database(self, query: str) -> Optional[Dict]:
        """Search food database for match."""
        try:
            response = (
                self.supabase.table("foods")
                .select("*")
                .ilike("name", f"%{query}%")
                .limit(1)
                .execute()
            )

            if response.data:
                return response.data[0]

        except Exception as e:
            logger.error(f"Error searching food database: {e}")

        return None

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
            response = await self.openai.chat.completions.create(
                model="gpt-4o-mini",
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
