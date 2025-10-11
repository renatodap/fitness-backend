"""
Perplexity Service - Real-time Nutrition Intelligence

Uses OpenRouter's Perplexity API for:
- Latest nutrition data for new/unknown foods
- Real-time restaurant menu updates
- Food healthiness analysis with current research
- Regional/seasonal food variations

Cost: ~$0.001-0.005 per query (cached aggressively)
Fallback tier: Local DB → Groq AI → Perplexity → Manual entry
"""

import logging
import json
from typing import Dict, Any, Optional
from openai import AsyncOpenAI
from app.config import get_settings
from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)
settings = get_settings()


class PerplexityService:
    """
    Real-time nutrition intelligence using Perplexity AI via OpenRouter.

    Features:
    - Latest nutrition data (restaurant menus, seasonal items)
    - Food healthiness analysis with current research
    - Intelligent caching to minimize API costs
    - Structured JSON output for easy parsing
    """

    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.OPENROUTER_API_KEY,
            base_url="https://openrouter.ai/api/v1"
        )
        self.supabase = get_service_client()
        self.model = "perplexity/llama-3.1-sonar-large-128k-online"  # Real-time web search

        # Cache settings
        self.cache_ttl_days = 7  # Cache nutrition data for 1 week

    async def search_nutrition_info(
        self,
        food_name: str,
        quantity: str = "100",
        unit: str = "g",
        user_context: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Search for real-time nutrition information using Perplexity.

        This is the SMART fallback when:
        - Food not found in local database
        - Groq AI has low confidence
        - User asks for specific restaurant/brand item
        - Need latest nutrition data (e.g., "2025 Chipotle bowl")

        Args:
            food_name: Name of food to research
            quantity: Serving quantity
            unit: Serving unit (g, oz, cup, etc.)
            user_context: Optional context (e.g., "Chipotle restaurant")

        Returns:
            {
                "success": bool,
                "food_data": {
                    "name": str,
                    "brand_name": str | None,
                    "serving_size": float,
                    "serving_unit": str,
                    "calories": float,
                    "protein_g": float,
                    "total_carbs_g": float,
                    "total_fat_g": float,
                    "dietary_fiber_g": float,
                    "source": str,
                    "confidence": float
                },
                "reasoning": str,
                "sources": list[str],  # Perplexity provides sources
                "error": str | None
            }
        """
        try:
            logger.info(f"[Perplexity] Searching nutrition for: {food_name} ({quantity} {unit})")

            # STEP 1: Check cache first (avoid redundant API calls)
            cached_result = await self._check_cache(food_name, quantity, unit)
            if cached_result:
                logger.info(f"[Perplexity] Cache HIT for {food_name}")
                return {
                    "success": True,
                    "food_data": cached_result,
                    "reasoning": "Retrieved from cache",
                    "sources": cached_result.get("sources", []),
                    "error": None
                }

            # STEP 2: Build intelligent search prompt
            search_query = self._build_search_prompt(food_name, quantity, unit, user_context)

            # STEP 3: Query Perplexity with structured output
            logger.info(f"[Perplexity] Calling API for {food_name}...")

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": """You are a nutrition database expert with real-time web access.

Your task: Find the MOST ACCURATE, UP-TO-DATE nutrition information for the given food.

CRITICAL RULES:
1. Search official sources: USDA, brand websites, restaurant nutrition PDFs
2. Prioritize recent data (2024-2025)
3. Verify macros match calories: (protein_g × 4) + (carbs_g × 4) + (fat_g × 9) ≈ calories
4. NEVER guess - if unsure, indicate low confidence
5. For branded/restaurant items, cite the official source

Return ONLY valid JSON with this structure:
{
    "found": true/false,
    "name": "Official food name",
    "brand_name": "Brand or restaurant name (null if generic)",
    "serving_size": 100.0,
    "serving_unit": "g",
    "calories": 165.0,
    "protein_g": 31.0,
    "total_carbs_g": 0.0,
    "total_fat_g": 3.6,
    "dietary_fiber_g": 0.0,
    "saturated_fat_g": 1.0,
    "sugars_g": 0.0,
    "sodium_mg": 74.0,
    "confidence": 0.95,  // 0.0-1.0 based on source quality
    "source": "USDA FoodData Central",
    "source_url": "https://fdc.nal.usda.gov/...",
    "notes": "Additional context if relevant",
    "last_updated": "2025-01"
}

If not found, return:
{
    "found": false,
    "reason": "Could not find reliable nutrition data",
    "confidence": 0.0
}"""
                    },
                    {
                        "role": "user",
                        "content": search_query
                    }
                ],
                temperature=0.1,  # Low temperature for factual accuracy
                max_tokens=1000,
                response_format={"type": "json_object"}
            )

            # STEP 4: Parse response
            result_text = response.choices[0].message.content
            result = json.loads(result_text)

            logger.info(f"[Perplexity] Result: found={result.get('found')}, confidence={result.get('confidence', 0)}")

            if not result.get("found"):
                return {
                    "success": False,
                    "food_data": None,
                    "reasoning": result.get("reason", "Not found"),
                    "sources": [],
                    "error": "Food not found in real-time search"
                }

            # STEP 5: Validate nutrition data
            food_data = {
                "name": result["name"],
                "brand_name": result.get("brand_name"),
                "serving_size": float(result["serving_size"]),
                "serving_unit": result["serving_unit"],
                "calories": float(result["calories"]),
                "protein_g": float(result["protein_g"]),
                "total_carbs_g": float(result["total_carbs_g"]),
                "total_fat_g": float(result["total_fat_g"]),
                "dietary_fiber_g": float(result.get("dietary_fiber_g", 0)),
                "saturated_fat_g": float(result.get("saturated_fat_g", 0)),
                "sugars_g": float(result.get("sugars_g", 0)),
                "sodium_mg": float(result.get("sodium_mg", 0)),
                "confidence": float(result.get("confidence", 0.8)),
                "source": result.get("source", "Perplexity AI"),
                "source_url": result.get("source_url"),
                "notes": result.get("notes"),
                "last_updated": result.get("last_updated"),
                "sources": [result.get("source_url")] if result.get("source_url") else []
            }

            # STEP 6: Cache result for future queries
            await self._cache_result(food_name, quantity, unit, food_data)

            logger.info(f"[Perplexity] ✅ Found: {food_data['name']} - {food_data['calories']} cal")

            return {
                "success": True,
                "food_data": food_data,
                "reasoning": f"Retrieved from {food_data['source']}",
                "sources": food_data["sources"],
                "error": None
            }

        except Exception as e:
            logger.error(f"[Perplexity] Search failed: {e}", exc_info=True)
            return {
                "success": False,
                "food_data": None,
                "reasoning": "Perplexity API error",
                "sources": [],
                "error": str(e)
            }

    async def analyze_food_healthiness(
        self,
        food_name: str,
        user_goal: Optional[str] = None,
        dietary_restrictions: Optional[list[str]] = None
    ) -> Dict[str, Any]:
        """
        Analyze if a food is healthy based on latest research.

        Perfect for "Is X healthy?" questions.
        Uses Perplexity's real-time web search to get current research.

        Args:
            food_name: Food to analyze
            user_goal: User's fitness goal (weight loss, muscle gain, etc.)
            dietary_restrictions: Any dietary restrictions

        Returns:
            {
                "success": bool,
                "analysis": {
                    "overall_rating": "healthy" | "moderate" | "unhealthy",
                    "score": 0-100,
                    "pros": list[str],
                    "cons": list[str],
                    "recommendations": str,
                    "relevant_for_goal": bool,
                    "sources": list[str]
                },
                "error": str | None
            }
        """
        try:
            logger.info(f"[Perplexity] Analyzing healthiness: {food_name}")

            # Build analysis prompt
            context = f"User goal: {user_goal}. " if user_goal else ""
            context += f"Dietary restrictions: {', '.join(dietary_restrictions)}. " if dietary_restrictions else ""

            prompt = f"""Analyze the healthiness of "{food_name}" based on current nutrition science.

{context}

Provide:
1. Overall health rating (healthy/moderate/unhealthy)
2. Health score (0-100)
3. Key benefits (pros)
4. Concerns or drawbacks (cons)
5. Specific recommendations for this user
6. Whether it aligns with their goal

Use latest research from reputable sources (Harvard, Mayo Clinic, peer-reviewed journals).

Return ONLY valid JSON:
{{
    "overall_rating": "healthy",
    "score": 85,
    "pros": ["High protein", "Low in saturated fat", "Rich in vitamins"],
    "cons": ["High sodium if processed"],
    "recommendations": "Great choice for muscle building. Choose grilled over fried.",
    "relevant_for_goal": true,
    "reasoning": "Brief scientific explanation",
    "sources": ["https://..."]
}}"""

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a nutrition science expert with access to latest research."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=1500,
                response_format={"type": "json_object"}
            )

            analysis = json.loads(response.choices[0].message.content)

            logger.info(f"[Perplexity] Analysis: {analysis['overall_rating']} (score: {analysis['score']})")

            return {
                "success": True,
                "analysis": analysis,
                "error": None
            }

        except Exception as e:
            logger.error(f"[Perplexity] Analysis failed: {e}", exc_info=True)
            return {
                "success": False,
                "analysis": None,
                "error": str(e)
            }

    def _build_search_prompt(
        self,
        food_name: str,
        quantity: str,
        unit: str,
        user_context: Optional[str]
    ) -> str:
        """Build intelligent search prompt for Perplexity."""
        base_query = f"Find official nutrition information for: {food_name}"

        # Add context clues
        if user_context:
            base_query += f" ({user_context})"

        # Add serving size request
        base_query += f"\n\nProvide nutrition per {quantity}{unit} serving."

        # Add quality hints
        base_query += "\n\nPrioritize: Official sources (USDA, brand websites, restaurant PDFs)"
        base_query += "\nRequired: Calories, protein, carbs, fats (complete macros)"
        base_query += "\nPrefer: Recent data (2024-2025)"

        return base_query

    async def _check_cache(
        self,
        food_name: str,
        quantity: str,
        unit: str
    ) -> Optional[Dict[str, Any]]:
        """Check if we have cached Perplexity result for this food."""
        try:
            # Normalize search key
            cache_key = f"{food_name.lower()}_{quantity}_{unit}"

            response = self.supabase.table("perplexity_nutrition_cache")\
                .select("*")\
                .eq("cache_key", cache_key)\
                .gte("cached_at", f"NOW() - INTERVAL '{self.cache_ttl_days} days'")\
                .order("cached_at", desc=True)\
                .limit(1)\
                .execute()

            if response.data:
                cached = response.data[0]
                logger.info(f"[Perplexity] Cache hit: {food_name}")
                return cached.get("nutrition_data")

            return None

        except Exception as e:
            logger.warning(f"[Perplexity] Cache check failed: {e}")
            return None

    async def _cache_result(
        self,
        food_name: str,
        quantity: str,
        unit: str,
        food_data: Dict[str, Any]
    ):
        """Cache Perplexity result to avoid redundant API calls."""
        try:
            cache_key = f"{food_name.lower()}_{quantity}_{unit}"

            cache_entry = {
                "cache_key": cache_key,
                "food_name": food_name,
                "quantity": quantity,
                "unit": unit,
                "nutrition_data": food_data,
                "confidence": food_data.get("confidence", 0.8),
                "source": food_data.get("source", "Perplexity"),
                "cached_at": "NOW()"
            }

            self.supabase.table("perplexity_nutrition_cache")\
                .insert(cache_entry)\
                .execute()

            logger.info(f"[Perplexity] Cached: {food_name}")

        except Exception as e:
            logger.warning(f"[Perplexity] Cache save failed: {e}")


# Singleton instance
_perplexity_service: Optional[PerplexityService] = None


def get_perplexity_service() -> PerplexityService:
    """Get the global PerplexityService instance."""
    global _perplexity_service
    if _perplexity_service is None:
        _perplexity_service = PerplexityService()
    return _perplexity_service
