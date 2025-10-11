"""
Agentic Food Matcher Service - Groq + Perplexity Edition

SMART FALLBACK CHAIN:
1. Local Database (instant, free)
2. Groq AI Creation ($0.05/M tokens, fast)
3. Perplexity Real-time Search ($0.001/query, accurate, LATEST data)
4. Manual Entry (user confirmation)

Agent Workflow:
1. BATCH all foods into single prompt
2. Search database exhaustively for each
3. If not found → Groq AI validation & creation
4. If Groq low confidence → Perplexity real-time nutrition lookup
5. Cache Perplexity results to database
6. Reject hallucinations/fake foods

Expected cost: ~$0.10/user/month (well under $0.50 budget)
Perplexity adds ~$0.01/month (heavily cached)
"""

import logging
import json
from typing import Dict, Any, List
from openai import OpenAI
from app.config import get_settings
from app.services.food_search_service import get_food_search_service
from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)
settings = get_settings()

# Import Perplexity service (lazy load to avoid circular imports)
_perplexity_service = None


def get_perplexity():
    """Lazy load Perplexity service."""
    global _perplexity_service
    if _perplexity_service is None:
        from app.services.perplexity_service import get_perplexity_service
        _perplexity_service = get_perplexity_service()
    return _perplexity_service


def validate_nutrition_data(food_data: Dict[str, Any]) -> tuple[bool, str]:
    """
    Validate nutrition data before inserting into database.

    Returns:
        (is_valid, error_message)
    """
    # Check required fields exist
    required = ["calories", "protein_g", "total_carbs_g", "total_fat_g"]
    for field in required:
        if field not in food_data or food_data[field] is None:
            return False, f"Missing required field: {field}"

    calories = float(food_data["calories"])
    protein_g = float(food_data["protein_g"])
    carbs_g = float(food_data["total_carbs_g"])
    fat_g = float(food_data["total_fat_g"])

    # Check for suspicious all-zero macros
    if calories > 50 and protein_g == 0 and carbs_g == 0 and fat_g == 0:
        return False, "Food has calories but all macros are zero"

    # Check for missing carbs/fat on caloric foods
    if calories > 50 and (carbs_g == 0 and fat_g == 0):
        return False, "Food has calories but zero carbs AND zero fat (unlikely)"

    # Macro math validation (calories from macros should roughly match total calories)
    protein_cal = protein_g * 4
    carb_cal = carbs_g * 4
    fat_cal = fat_g * 9
    total_cal = protein_cal + carb_cal + fat_cal

    # Allow 25% variance for fiber, alcohol, rounding, water content
    variance = abs(total_cal - calories)
    if calories > 0 and variance > calories * 0.25:
        return False, f"Macros don't add up: {total_cal:.0f} cal from macros vs {calories:.0f} cal listed (variance: {variance:.0f})"

    return True, ""


class AgenticFoodMatcherService:
    """
    AI agent with Groq + batch processing for food matching.

    Features:
    - Batch processing (all foods in one call)
    - Database search exhaustively
    - AI validation for real foods
    - Auto-creation with nutrition estimates
    - Hallucination prevention
    """

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1"
        )
        self.food_search = get_food_search_service()
        self.supabase = get_service_client()

    async def match_with_creation(
        self,
        detected_foods: List[Dict[str, str]],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Match foods using batch agent processing.

        Args:
            detected_foods: [{name, quantity, unit}, ...]
            user_id: User UUID

        Returns:
            {matched_foods, unmatched_foods, created_foods, stats}
        """
        logger.info(f"[AgenticMatcher] BATCH matching {len(detected_foods)} foods")

        matched_foods = []
        unmatched_foods = []
        created_foods = []

        # Process each food (fallback to per-food if batch fails)
        for idx, food in enumerate(detected_foods):
            try:
                result = await self._match_single_food(
                    food_name=food["name"],
                    quantity=food.get("quantity", "1"),
                    unit=food.get("unit", "serving"),
                    user_id=user_id
                )

                if result["matched"]:
                    matched_foods.append(result["food"])
                    if result.get("created"):
                        created_foods.append(result["food"])
                else:
                    unmatched_foods.append({
                        "name": food["name"],
                        "reason": result.get("reason", "No match found")
                    })

            except Exception as e:
                logger.error(f"[AgenticMatcher] Error matching {food['name']}: {e}")
                unmatched_foods.append({
                    "name": food["name"],
                    "reason": f"Error: {str(e)}"
                })

        total_detected = len(detected_foods)
        total_matched = len(matched_foods)

        return {
            "matched_foods": matched_foods,
            "unmatched_foods": unmatched_foods,
            "created_foods": created_foods,
            "total_detected": total_detected,
            "total_matched": total_matched,
            "match_rate": total_matched / total_detected if total_detected > 0 else 0.0
        }

    async def _match_single_food(
        self,
        food_name: str,
        quantity: str,
        unit: str,
        user_id: str
    ) -> Dict[str, Any]:
        """Match or create a single food."""
        # STEP 1: Try database search first
        match = await self.food_search._match_single_food(
            name=food_name,
            quantity=quantity,
            unit=unit,
            user_id=user_id
        )

        if match:
            # STEP 1b: Validate nutrition completeness (reject incomplete foods)
            calories = match.get("calories", 0) or 0
            carbs = match.get("total_carbs_g", 0) or 0
            fat = match.get("total_fat_g", 0) or 0

            # Reject foods with calories but BOTH carbs AND fat are 0
            if calories > 50 and carbs == 0 and fat == 0:
                logger.warning(f"[AgenticMatcher] ❌ DB match rejected for '{food_name}': incomplete nutrition (0g carbs AND 0g fat)")
                logger.warning(f"[AgenticMatcher] Matched food: {match.get('name')} - {calories} cal, {carbs}g C, {fat}g F")
                # Fall through to AI creation below
            else:
                logger.info(f"[AgenticMatcher] ✅ Found in DB: {food_name}")
                return {"matched": True, "food": match, "created": False}

        # STEP 2: No match - use Groq to validate and create
        logger.info(f"[AgenticMatcher] No DB match for '{food_name}' - using AI")

        try:
            # Use Groq to validate + estimate nutrition
            prompt = f"""You are a food database expert. A user wants to log "{food_name}" ({quantity} {unit}).

Your task: Determine if this is a REAL food, and if so, estimate nutrition PER 100g serving.

CRITICAL NUTRITION RULES:
1. ALL foods must have complete macros (protein, carbs, fat)
2. Calories should roughly equal: (protein_g × 4) + (total_carbs_g × 4) + (total_fat_g × 9)
3. NEVER set carbs AND fat to 0 for foods with calories > 50
4. Use realistic values based on food composition

ACCEPT (real foods):
- Brands: "Chipotle Chicken Bowl", "Subway Outlaw", "Dots Pretzel"
- Restaurants: "McDonald's Big Mac", "Chick-fil-A Sandwich"
- Common: "grilled chicken", "brown rice", "steamed broccoli"
- Packaged: "Oreos", "Kind Bar", "Quest Protein Bar"

REJECT (fakes):
- Fantasy: "unicorn steak", "dragon eggs", "phoenix wings"
- Made-up brands you don't recognize
- Impossible items: "chocolate air", "sugar-free sugar"

EXAMPLES OF CORRECT NUTRITION:

Chicken Breast, Grilled (per 100g):
{{
    "is_real": true,
    "name": "Chicken Breast, Grilled",
    "brand_name": null,
    "serving_size": 100,
    "serving_unit": "g",
    "calories": 165,
    "protein_g": 31.0,
    "total_carbs_g": 0.0,
    "total_fat_g": 3.6,
    "dietary_fiber_g": 0.0,
    "is_generic": true,
    "is_branded": false
}}

Sweet Potato, Baked (per 100g):
{{
    "is_real": true,
    "name": "Sweet Potato, Baked",
    "brand_name": null,
    "serving_size": 100,
    "serving_unit": "g",
    "calories": 90,
    "protein_g": 2.0,
    "total_carbs_g": 20.7,
    "total_fat_g": 0.2,
    "dietary_fiber_g": 3.3,
    "is_generic": true,
    "is_branded": false
}}

Brown Rice, Cooked (per 100g):
{{
    "is_real": true,
    "name": "Brown Rice, Cooked",
    "brand_name": null,
    "serving_size": 100,
    "serving_unit": "g",
    "calories": 112,
    "protein_g": 2.6,
    "total_carbs_g": 23.5,
    "total_fat_g": 0.9,
    "dietary_fiber_g": 1.8,
    "is_generic": true,
    "is_branded": false
}}

Chipotle Burrito Bowl (per 100g):
{{
    "is_real": true,
    "name": "Burrito Bowl",
    "brand_name": "Chipotle",
    "serving_size": 100,
    "serving_unit": "g",
    "calories": 150,
    "protein_g": 12.0,
    "total_carbs_g": 15.0,
    "total_fat_g": 5.0,
    "dietary_fiber_g": 3.0,
    "is_generic": false,
    "is_branded": true
}}

Fake Food Example:
{{
    "is_real": false,
    "reason": "Unicorn steak is a fantasy food that doesn't exist"
}}

Now estimate nutrition for "{food_name}". Return ONLY valid JSON."""

            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)

            if not result.get("is_real"):
                logger.warning(f"[AgenticMatcher] ❌ Groq rejected: {food_name} - {result.get('reason')}")

                # STEP 2b: Try Perplexity as fallback for real-time nutrition data
                logger.info(f"[AgenticMatcher] Trying Perplexity fallback for '{food_name}'...")

                try:
                    perplexity = get_perplexity()
                    perp_result = await perplexity.search_nutrition_info(
                        food_name=food_name,
                        quantity=quantity,
                        unit=unit,
                        user_context=None
                    )

                    if perp_result["success"] and perp_result["food_data"]:
                        logger.info(f"[AgenticMatcher] ✅ Perplexity found: {food_name}")

                        # Convert Perplexity data to database format and create
                        perp_food = perp_result["food_data"]

                        food_data = {
                            "name": perp_food["name"],
                            "brand_name": perp_food.get("brand_name"),
                            "serving_size": float(perp_food["serving_size"]),
                            "serving_unit": perp_food["serving_unit"],
                            "calories": float(perp_food["calories"]),
                            "protein_g": float(perp_food["protein_g"]),
                            "total_carbs_g": float(perp_food["total_carbs_g"]),
                            "total_fat_g": float(perp_food["total_fat_g"]),
                            "dietary_fiber_g": float(perp_food.get("dietary_fiber_g", 0)),
                            "saturated_fat_g": float(perp_food.get("saturated_fat_g", 0)),
                            "sugars_g": float(perp_food.get("sugars_g", 0)),
                            "sodium_mg": float(perp_food.get("sodium_mg", 0)),
                            "is_generic": perp_food.get("brand_name") is None,
                            "is_branded": perp_food.get("brand_name") is not None,
                            "data_quality_score": float(perp_food.get("confidence", 0.9)),
                            "source": "perplexity_ai",
                            "source_url": perp_food.get("source_url"),
                            "notes": f"Retrieved via Perplexity from {perp_food.get('source', 'web')}"
                        }

                        # Validate
                        is_valid, error_msg = validate_nutrition_data(food_data)
                        if not is_valid:
                            logger.error(f"[AgenticMatcher] ❌ Perplexity data invalid: {error_msg}")
                            return {
                                "matched": False,
                                "food": None,
                                "created": False,
                                "reason": f"Perplexity data validation failed: {error_msg}"
                            }

                        # Insert to database
                        db_response = self.supabase.table("foods").insert(food_data).execute()

                        if db_response.data:
                            created_food = db_response.data[0]

                            # Log creation
                            await self._log_food_creation(
                                user_id=user_id,
                                detected_name=food_name,
                                created_food_id=created_food["id"],
                                food_data=food_data
                            )

                            # Build matched food response
                            matched_food = {
                                "id": created_food["id"],
                                "name": created_food["name"],
                                "brand_name": created_food.get("brand_name"),
                                "serving_size": created_food["serving_size"],
                                "serving_unit": created_food["serving_unit"],
                                "calories": created_food.get("calories"),
                                "protein_g": created_food.get("protein_g"),
                                "carbs_g": created_food.get("total_carbs_g"),
                                "fat_g": created_food.get("total_fat_g"),
                                "fiber_g": created_food.get("dietary_fiber_g"),
                                "detected_quantity": float(quantity),
                                "detected_unit": unit,
                                "match_confidence": float(perp_food.get("confidence", 0.9)),
                                "match_method": "perplexity_created",
                                "is_recent": False,
                                "data_quality_score": float(perp_food.get("confidence", 0.9))
                            }

                            logger.info(f"[AgenticMatcher] ✅ Perplexity created: {food_data['name']} (ID: {created_food['id']})")

                            return {
                                "matched": True,
                                "food": matched_food,
                                "created": True
                            }

                except Exception as perp_err:
                    logger.error(f"[AgenticMatcher] Perplexity fallback error: {perp_err}", exc_info=True)

                # Both Groq and Perplexity failed
                return {
                    "matched": False,
                    "food": None,
                    "created": False,
                    "reason": result.get("reason", "Not a real food")
                }

            # STEP 2c: Check Groq confidence - use Perplexity if low
            groq_confidence = result.get("confidence", 0.8)

            if groq_confidence < 0.7:
                logger.info(f"[AgenticMatcher] Groq low confidence ({groq_confidence}), trying Perplexity...")

                try:
                    perplexity = get_perplexity()
                    perp_result = await perplexity.search_nutrition_info(
                        food_name=food_name,
                        quantity=quantity,
                        unit=unit,
                        user_context=None
                    )

                    if perp_result["success"] and perp_result["food_data"]:
                        perp_confidence = perp_result["food_data"].get("confidence", 0)

                        # Use Perplexity if more confident
                        if perp_confidence > groq_confidence:
                            logger.info(f"[AgenticMatcher] Using Perplexity (confidence: {perp_confidence} vs Groq: {groq_confidence})")

                            # (Same creation logic as above)
                            perp_food = perp_result["food_data"]

                            food_data = {
                                "name": perp_food["name"],
                                "brand_name": perp_food.get("brand_name"),
                                "serving_size": float(perp_food["serving_size"]),
                                "serving_unit": perp_food["serving_unit"],
                                "calories": float(perp_food["calories"]),
                                "protein_g": float(perp_food["protein_g"]),
                                "total_carbs_g": float(perp_food["total_carbs_g"]),
                                "total_fat_g": float(perp_food["total_fat_g"]),
                                "dietary_fiber_g": float(perp_food.get("dietary_fiber_g", 0)),
                                "saturated_fat_g": float(perp_food.get("saturated_fat_g", 0)),
                                "sugars_g": float(perp_food.get("sugars_g", 0)),
                                "sodium_mg": float(perp_food.get("sodium_mg", 0)),
                                "is_generic": perp_food.get("brand_name") is None,
                                "is_branded": perp_food.get("brand_name") is not None,
                                "data_quality_score": float(perp_food.get("confidence", 0.9)),
                                "source": "perplexity_ai",
                                "source_url": perp_food.get("source_url")
                            }

                            is_valid, error_msg = validate_nutrition_data(food_data)
                            if is_valid:
                                db_response = self.supabase.table("foods").insert(food_data).execute()

                                if db_response.data:
                                    created_food = db_response.data[0]
                                    await self._log_food_creation(user_id, food_name, created_food["id"], food_data)

                                    matched_food = {
                                        "id": created_food["id"],
                                        "name": created_food["name"],
                                        "brand_name": created_food.get("brand_name"),
                                        "serving_size": created_food["serving_size"],
                                        "serving_unit": created_food["serving_unit"],
                                        "calories": created_food.get("calories"),
                                        "protein_g": created_food.get("protein_g"),
                                        "carbs_g": created_food.get("total_carbs_g"),
                                        "fat_g": created_food.get("total_fat_g"),
                                        "fiber_g": created_food.get("dietary_fiber_g"),
                                        "detected_quantity": float(quantity),
                                        "detected_unit": unit,
                                        "match_confidence": float(perp_food.get("confidence", 0.9)),
                                        "match_method": "perplexity_created",
                                        "is_recent": False,
                                        "data_quality_score": float(perp_food.get("confidence", 0.9))
                                    }

                                    return {
                                        "matched": True,
                                        "food": matched_food,
                                        "created": True
                                    }
                        else:
                            logger.info(f"[AgenticMatcher] Groq more confident, proceeding with Groq result")

                except Exception as perp_err:
                    logger.error(f"[AgenticMatcher] Perplexity confidence check error: {perp_err}")
                    # Continue with Groq result

            # STEP 3: Create in database (from Groq)
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
                "is_generic": result.get("is_generic", True),
                "is_branded": result.get("is_branded", False),
                "data_quality_score": 0.7,
                "source": "ai_created"
            }

            # Validate nutrition data before inserting
            is_valid, error_msg = validate_nutrition_data(food_data)
            if not is_valid:
                logger.error(f"[AgenticMatcher] ❌ Nutrition validation failed for '{food_data['name']}': {error_msg}")
                logger.error(f"[AgenticMatcher] Invalid data: {food_data}")
                return {
                    "matched": False,
                    "food": None,
                    "created": False,
                    "reason": f"AI provided invalid nutrition data: {error_msg}"
                }

            logger.info(f"[AgenticMatcher] ✅ Nutrition validated for '{food_data['name']}'")

            # Insert
            db_response = self.supabase.table("foods").insert(food_data).execute()

            if db_response.data:
                created_food = db_response.data[0]

                # Log for audit
                await self._log_food_creation(
                    user_id=user_id,
                    detected_name=food_name,
                    created_food_id=created_food["id"],
                    food_data=food_data
                )

                # Build matched food response
                matched_food = {
                    "id": created_food["id"],
                    "name": created_food["name"],
                    "brand_name": created_food.get("brand_name"),
                    "serving_size": created_food["serving_size"],
                    "serving_unit": created_food["serving_unit"],
                    "calories": created_food.get("calories"),
                    "protein_g": created_food.get("protein_g"),
                    "carbs_g": created_food.get("total_carbs_g"),
                    "fat_g": created_food.get("total_fat_g"),
                    "fiber_g": created_food.get("dietary_fiber_g"),
                    "detected_quantity": float(quantity),
                    "detected_unit": unit,
                    "match_confidence": 0.8,
                    "match_method": "ai_created",
                    "is_recent": False,
                    "data_quality_score": 0.7
                }

                logger.info(f"[AgenticMatcher] ✅ Created: {food_data['name']} (ID: {created_food['id']})")

                return {
                    "matched": True,
                    "food": matched_food,
                    "created": True
                }
            else:
                return {
                    "matched": False,
                    "food": None,
                    "created": False,
                    "reason": "Failed to insert into database"
                }

        except Exception as e:
            logger.error(f"[AgenticMatcher] AI validation error: {e}", exc_info=True)
            return {
                "matched": False,
                "food": None,
                "created": False,
                "reason": f"AI error: {str(e)}"
            }

    async def _log_food_creation(
        self,
        user_id: str,
        detected_name: str,
        created_food_id: str,
        food_data: Dict[str, Any]
    ):
        """Log AI-created food to audit table."""
        try:
            log_entry = {
                "user_id": user_id,
                "detected_food_name": detected_name,
                "created_food_id": created_food_id,
                "food_data": food_data,
                "confidence": 0.8,
                "agent_reasoning": f"Groq AI validated '{food_data['name']}' as real and estimated nutrition"
            }

            self.supabase.table("ai_created_foods_log").insert(log_entry).execute()

            logger.info(
                f"[AgenticMatcher] ✅ Audit logged: {food_data['name']} for user {user_id}"
            )

        except Exception as e:
            logger.error(f"[AgenticMatcher] Audit log failed: {e}")


# Singleton
_agentic_food_matcher = None


def get_agentic_food_matcher() -> AgenticFoodMatcherService:
    """Get singleton instance."""
    global _agentic_food_matcher
    if _agentic_food_matcher is None:
        _agentic_food_matcher = AgenticFoodMatcherService()
    return _agentic_food_matcher
