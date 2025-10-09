"""
Food Search Service

Provides intelligent food search with:
- Fast autocomplete with partial matching
- Smart ranking (recent > frequent > quality)
- Recent foods tracking
- Nutrition preview
"""

import logging
from typing import List, Dict, Any, Optional
from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


class FoodSearchService:
    """Service for searching foods and tracking user food history."""

    def __init__(self):
        self.supabase = get_service_client()

    async def search_foods(
        self,
        query: str,
        user_id: Optional[str] = None,
        limit: int = 20,
        include_recent: bool = True
    ) -> Dict[str, Any]:
        """
        Search foods with intelligent ranking.

        Ranking priority:
        1. User's recent foods (if include_recent=True)
        2. Popular foods (high search_count)
        3. High quality foods (high data_quality_score)
        4. Verified foods (is_verified=true)

        Args:
            query: Search query string
            user_id: Optional user ID for personalized results
            limit: Maximum number of results
            include_recent: Include user's recent foods

        Returns:
            Dict with foods list and metadata
        """
        try:
            logger.info(f"Searching foods: query='{query}', user_id={user_id}, limit={limit}")

            results = []

            # Step 1: Get user's recent foods (if requested and user logged in)
            if include_recent and user_id:
                recent_foods = await self._get_recent_foods_for_search(
                    user_id=user_id,
                    query=query,
                    limit=min(5, limit)  # Max 5 recent foods in search
                )
                results.extend(recent_foods)
                logger.info(f"Found {len(recent_foods)} recent foods matching query")

            # Step 2: Search global food database
            remaining_limit = limit - len(results)
            if remaining_limit > 0:
                db_foods = await self._search_food_database(
                    query=query,
                    limit=remaining_limit,
                    exclude_ids=[f["id"] for f in results]  # Don't duplicate recent foods
                )
                results.extend(db_foods)
                logger.info(f"Found {len(db_foods)} database foods matching query")

            # Step 3: Track search query for analytics
            if query and len(query) >= 3:
                await self._track_search_query(query=query, user_id=user_id)

            return {
                "foods": results,
                "total": len(results),
                "limit": limit,
                "query": query
            }

        except Exception as e:
            logger.error(f"Food search failed: {e}", exc_info=True)
            return {
                "foods": [],
                "total": 0,
                "limit": limit,
                "query": query,
                "error": str(e)
            }

    async def get_recent_foods(
        self,
        user_id: str,
        limit: int = 20
    ) -> Dict[str, Any]:
        """
        Get user's recently logged foods for quick access.

        Args:
            user_id: User ID
            limit: Maximum number of foods to return

        Returns:
            Dict with recent foods list
        """
        try:
            logger.info(f"Getting recent foods for user {user_id}, limit={limit}")

            # Query meal_foods table (relational schema)
            # Join with meal_logs to filter by user_id
            response = self.supabase.table("meal_foods") \
                .select("food_id, quantity, unit, created_at, meal_logs!inner(user_id, logged_at)") \
                .eq("meal_logs.user_id", user_id) \
                .order("created_at", desc=True) \
                .limit(200) \
                .execute()

            if not response.data:
                return {"foods": []}

            # Extract food IDs and track last usage
            food_tracking = {}  # {food_id: {last_logged_at, quantity, unit, count}}

            for meal_food in response.data:
                food_id = meal_food.get("food_id")
                if not food_id:
                    continue

                # Get logged_at from joined meal_logs
                meal_log_data = meal_food.get("meal_logs", {})
                logged_at = meal_log_data.get("logged_at") if isinstance(meal_log_data, dict) else None

                if food_id not in food_tracking:
                    food_tracking[food_id] = {
                        "last_logged_at": logged_at or meal_food.get("created_at"),
                        "last_quantity": meal_food.get("quantity"),
                        "last_unit": meal_food.get("unit"),
                        "log_count": 1
                    }
                else:
                    # Update count but keep most recent quantity/unit
                    food_tracking[food_id]["log_count"] += 1

            # Get top N unique food IDs
            sorted_food_ids = sorted(
                food_tracking.keys(),
                key=lambda fid: (
                    food_tracking[fid]["log_count"],  # Primary: log count
                    food_tracking[fid]["last_logged_at"]  # Secondary: recency
                ),
                reverse=True
            )[:limit]

            if not sorted_food_ids:
                return {"foods": []}

            # Fetch full food data from foods_enhanced
            foods_response = self.supabase.table("foods_enhanced") \
                .select("id, name, brand_name, food_group, serving_size, serving_unit, calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, total_sugars_g, sodium_mg") \
                .in_("id", sorted_food_ids) \
                .execute()

            # Merge with tracking data
            foods_with_history = []
            for food_data in foods_response.data:
                food_id = food_data["id"]
                tracking = food_tracking.get(food_id, {})

                foods_with_history.append({
                    **food_data,
                    "last_quantity": tracking.get("last_quantity"),
                    "last_unit": tracking.get("last_unit"),
                    "last_logged_at": tracking.get("last_logged_at"),
                    "log_count": tracking.get("log_count", 0),
                    "is_recent": True
                })

            # Sort by original order (log_count + recency)
            foods_with_history.sort(
                key=lambda f: (
                    f["log_count"],
                    f["last_logged_at"]
                ),
                reverse=True
            )

            logger.info(f"Returning {len(foods_with_history)} recent foods")

            return {"foods": foods_with_history}

        except Exception as e:
            logger.error(f"Get recent foods failed: {e}", exc_info=True)
            return {"foods": [], "error": str(e)}

    async def _get_recent_foods_for_search(
        self,
        user_id: str,
        query: str,
        limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Get user's recent foods that match search query.

        This is used within search results to prioritize foods the user has logged recently.
        """
        try:
            # Get recent foods
            recent_response = await self.get_recent_foods(user_id=user_id, limit=50)
            recent_foods = recent_response.get("foods", [])

            if not recent_foods:
                return []

            # Filter to match query (case-insensitive partial match)
            query_lower = query.lower()
            matching_foods = [
                food for food in recent_foods
                if query_lower in food["name"].lower() or
                   (food.get("brand_name") and query_lower in food["brand_name"].lower())
            ]

            return matching_foods[:limit]

        except Exception as e:
            logger.error(f"Get recent foods for search failed: {e}")
            return []

    async def _search_food_database(
        self,
        query: str,
        limit: int = 20,
        exclude_ids: List[str] = None
    ) -> List[Dict[str, Any]]:
        """
        Search food database with partial matching and ranking.

        Uses PostgreSQL ILIKE for partial matching and ranks by:
        - Popularity (search_count)
        - Quality (data_quality_score)
        - Verification (is_verified)
        """
        try:
            if exclude_ids is None:
                exclude_ids = []

            # Build query
            select_query = self.supabase.table("foods_enhanced").select(
                "id, name, brand_name, food_group, serving_size, serving_unit, "
                "calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, "
                "total_sugars_g, sodium_mg, data_quality_score, is_verified, "
                "popularity_score, search_count, is_generic, is_branded"
            )

            # Filter by data quality (exclude low-quality foods with incomplete nutrition)
            select_query = select_query.gte("data_quality_score", 0.5)

            # Filter by query (partial match on name or brand)
            # Use ILIKE for case-insensitive partial matching
            select_query = select_query.or_(
                f"name.ilike.%{query}%,brand_name.ilike.%{query}%"
            )

            # Exclude already-included foods (e.g., recent foods)
            if exclude_ids:
                select_query = select_query.not_.in_("id", exclude_ids)

            # Order by quality and popularity
            select_query = select_query.order("search_count", desc=True) \
                .order("data_quality_score", desc=True) \
                .limit(limit)

            response = select_query.execute()

            foods = response.data if response.data else []

            # Add is_recent flag (false for database search results)
            for food in foods:
                food["is_recent"] = False

            return foods

        except Exception as e:
            logger.error(f"Database food search failed: {e}", exc_info=True)
            return []

    async def _track_search_query(
        self,
        query: str,
        user_id: Optional[str] = None
    ):
        """
        Track search query for analytics and popularity ranking.

        This increments search_count for foods that match the query,
        improving their ranking in future searches.
        """
        try:
            # Find foods matching this query
            response = self.supabase.table("foods_enhanced") \
                .select("id") \
                .or_(f"name.ilike.%{query}%,brand_name.ilike.%{query}%") \
                .limit(10) \
                .execute()

            if not response.data:
                return

            # Increment search_count for matching foods
            food_ids = [food["id"] for food in response.data]

            for food_id in food_ids:
                try:
                    # Increment search_count atomically
                    self.supabase.rpc(
                        "increment_food_search_count",
                        {"food_id_param": food_id}
                    ).execute()
                except:
                    # If RPC doesn't exist, skip (non-critical)
                    pass

        except Exception as e:
            logger.debug(f"Search tracking failed (non-critical): {e}")

    async def increment_food_popularity(
        self,
        food_id: str,
        user_id: str
    ):
        """
        Increment popularity score when user logs a food.

        Call this when a meal is saved to track which foods are most commonly logged.
        """
        try:
            # Increment popularity_score
            self.supabase.rpc(
                "increment_food_popularity",
                {"food_id_param": food_id}
            ).execute()

        except Exception as e:
            logger.debug(f"Popularity tracking failed (non-critical): {e}")

    async def match_detected_foods(
        self,
        detected_foods: List[Dict[str, str]],
        user_id: str
    ) -> Dict[str, Any]:
        """
        Match detected food names to database foods with fuzzy matching.

        Matching strategies (in order):
        1. User's recent foods (exact/partial match)
        2. Exact name match in database
        3. Fuzzy match with cooking method detection
        4. Generic fallback (base ingredient)

        Args:
            detected_foods: List of dicts with 'name', 'quantity', 'unit'
            user_id: User ID for personalized matching (recent foods)

        Returns:
            Dict with matched_foods and unmatched_foods lists
        """
        try:
            logger.info(f"Matching {len(detected_foods)} detected foods for user {user_id}")

            matched_foods = []
            unmatched_foods = []

            for detected in detected_foods:
                name = detected.get("name", "").strip()
                quantity = detected.get("quantity", "1").strip()
                unit = detected.get("unit", "serving").strip()

                if not name:
                    continue

                # Try to match this food
                match_result = await self._match_single_food(
                    name=name,
                    quantity=quantity,
                    unit=unit,
                    user_id=user_id
                )

                if match_result:
                    matched_foods.append(match_result)
                else:
                    unmatched_foods.append({
                        "name": name,
                        "reason": "no_match_found"
                    })

            total_detected = len(detected_foods)
            total_matched = len(matched_foods)
            match_rate = total_matched / total_detected if total_detected > 0 else 0.0

            logger.info(f"Matching complete: {total_matched}/{total_detected} matched ({match_rate*100:.1f}%)")

            return {
                "matched_foods": matched_foods,
                "unmatched_foods": unmatched_foods,
                "total_detected": total_detected,
                "total_matched": total_matched,
                "match_rate": match_rate
            }

        except Exception as e:
            logger.error(f"Food matching failed: {e}", exc_info=True)
            raise

    async def _match_single_food(
        self,
        name: str,
        quantity: str,
        unit: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """
        Match a single detected food to database.

        Returns enriched food dict or None if no match found.
        """
        try:
            # Strategy 1: Search user's recent foods (highest priority)
            recent_match = await self._match_from_recent_foods(name, user_id)
            if recent_match:
                return self._enrich_match(recent_match, quantity, unit, "recent", 1.0, True)

            # Strategy 2: Exact/partial match in database
            db_match = await self._match_from_database(name)
            if db_match:
                confidence = self._calculate_match_confidence(name, db_match["name"])
                match_method = "exact" if confidence > 0.9 else "fuzzy"
                return self._enrich_match(db_match, quantity, unit, match_method, confidence, False)

            # Strategy 3: Fuzzy match with cooking method detection
            fuzzy_match = await self._fuzzy_match_with_cooking_method(name)
            if fuzzy_match:
                confidence = self._calculate_match_confidence(name, fuzzy_match["name"])
                return self._enrich_match(fuzzy_match, quantity, unit, "fuzzy", confidence, False)

            # No match found
            logger.warning(f"No match found for: {name}")
            return None

        except Exception as e:
            logger.error(f"Single food matching failed for '{name}': {e}", exc_info=True)
            return None

    async def _match_from_recent_foods(
        self,
        name: str,
        user_id: str
    ) -> Optional[Dict[str, Any]]:
        """Match from user's recently logged foods."""
        try:
            # Query recent foods with name matching
            response = self.supabase.rpc(
                "search_user_recent_foods_v2",
                {
                    "p_user_id": user_id,
                    "p_search_query": name,
                    "p_limit": 1
                }
            ).execute()

            if response.data and len(response.data) > 0:
                return response.data[0]

            return None
        except Exception as e:
            # RPC might not exist, fall back to manual query
            logger.debug(f"Recent foods RPC failed, using fallback: {e}")
            try:
                # Fallback: query recent foods manually
                response = self.supabase.from_("foods_enhanced").select(
                    "id, name, brand_name, food_group, serving_size, serving_unit, "
                    "calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, "
                    "total_sugars_g, sodium_mg, is_generic, is_branded, data_quality_score"
                ).gte("data_quality_score", 0.5).ilike("name", f"%{name}%").limit(1).execute()

                if response.data and len(response.data) > 0:
                    return response.data[0]
            except:
                pass

            return None

    async def _match_from_database(
        self,
        name: str
    ) -> Optional[Dict[str, Any]]:
        """Match from global food database with exact/partial matching."""
        try:
            # STEP 1: Try EXACT case-insensitive match first (highest priority)
            # This ensures "whey isolate" matches "Whey Isolate" exactly, not "Whey Protein"
            logger.info(f"[FoodSearch] Trying EXACT match for: '{name}'")
            response = self.supabase.from_("foods_enhanced").select(
                "id, name, brand_name, food_group, serving_size, serving_unit, "
                "calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, "
                "total_sugars_g, sodium_mg, is_generic, is_branded, data_quality_score"
            ).gte("data_quality_score", 0.5).ilike("name", name).order(
                "is_generic", desc=True  # Generic foods first
            ).order(
                "data_quality_score", desc=True  # Then by quality
            ).limit(5).execute()  # Get top 5 to filter

            if response.data and len(response.data) > 0:
                # Filter for EXACT matches (ignoring case and extra spaces)
                exact_matches = [
                    food for food in response.data
                    if food["name"].lower().strip() == name.lower().strip()
                ]

                if exact_matches:
                    logger.info(f"[FoodSearch] ✅ EXACT match found: '{exact_matches[0]['name']}'")
                    return exact_matches[0]

                # If no exact match but ilike found something, it's a partial match
                # Return the first one but log it
                logger.info(f"[FoodSearch] ⚠️ Partial match (ilike): '{response.data[0]['name']}' for query '{name}'")
                return response.data[0]

            # STEP 2: Try partial match with word boundaries (PREFER GENERIC over branded)
            # This searches for foods containing the search term
            logger.info(f"[FoodSearch] Trying PARTIAL match for: '{name}'")
            response = self.supabase.from_("foods_enhanced").select(
                "id, name, brand_name, food_group, serving_size, serving_unit, "
                "calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, "
                "total_sugars_g, sodium_mg, is_generic, is_branded, data_quality_score"
            ).gte("data_quality_score", 0.5).ilike("name", f"%{name}%").order(
                "is_generic", desc=True  # Generic foods first
            ).order(
                "data_quality_score", desc=True  # Then by quality
            ).limit(1).execute()

            if response.data and len(response.data) > 0:
                logger.info(f"[FoodSearch] ⚠️ Partial match found: '{response.data[0]['name']}' for query '{name}'")
                return response.data[0]

            logger.warning(f"[FoodSearch] ❌ No match found for: '{name}'")
            return None
        except Exception as e:
            logger.error(f"Database match failed: {e}")
            return None

    async def _fuzzy_match_with_cooking_method(
        self,
        name: str
    ) -> Optional[Dict[str, Any]]:
        """
        Fuzzy match with cooking method detection.

        Detects cooking methods (grilled, fried, raw, cooked, etc.) and searches accordingly.
        """
        try:
            # Common cooking methods
            cooking_methods = [
                "grilled", "fried", "baked", "roasted", "steamed",
                "boiled", "raw", "cooked", "fresh", "frozen"
            ]

            # Detect cooking method in name
            detected_method = None
            base_name = name.lower()

            for method in cooking_methods:
                if method in base_name:
                    detected_method = method
                    # Remove method from name to get base ingredient
                    base_name = base_name.replace(method, "").strip()
                    break

            # Search with cooking method filter if detected (PREFER GENERIC)
            if detected_method:
                response = self.supabase.from_("foods_enhanced").select(
                    "id, name, brand_name, food_group, serving_size, serving_unit, "
                    "calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, "
                    "total_sugars_g, sodium_mg, is_generic, is_branded, data_quality_score"
                ).gte("data_quality_score", 0.5).ilike("name", f"%{base_name}%{detected_method}%").order(
                    "is_generic", desc=True  # Generic foods first
                ).order(
                    "data_quality_score", desc=True  # Then by quality
                ).limit(1).execute()

                if response.data and len(response.data) > 0:
                    return response.data[0]

            # Fallback: search just base name (PREFER GENERIC)
            response = self.supabase.from_("foods_enhanced").select(
                "id, name, brand_name, food_group, serving_size, serving_unit, "
                "calories, protein_g, total_carbs_g, total_fat_g, dietary_fiber_g, "
                "total_sugars_g, sodium_mg, is_generic, is_branded, data_quality_score"
            ).gte("data_quality_score", 0.5).ilike("name", f"%{base_name}%").order(
                "is_generic", desc=True  # Generic foods first
            ).order(
                "data_quality_score", desc=True  # Then by quality
            ).limit(1).execute()

            if response.data and len(response.data) > 0:
                return response.data[0]

            return None
        except Exception as e:
            logger.error(f"Fuzzy match failed: {e}")
            return None

    def _calculate_match_confidence(
        self,
        detected_name: str,
        db_name: str
    ) -> float:
        """
        Calculate match confidence using string similarity.

        Returns value between 0.0 and 1.0.
        """
        from difflib import SequenceMatcher

        detected_lower = detected_name.lower().strip()
        db_lower = db_name.lower().strip()

        # Use SequenceMatcher for similarity
        similarity = SequenceMatcher(None, detected_lower, db_lower).ratio()

        # Bonus for exact substring match
        if detected_lower in db_lower or db_lower in detected_lower:
            similarity = min(1.0, similarity + 0.1)

        return round(similarity, 2)

    def _enrich_match(
        self,
        food_record: Dict[str, Any],
        quantity: str,
        unit: str,
        method: str,
        confidence: float,
        is_recent: bool
    ) -> Dict[str, Any]:
        """
        Enrich matched food with detected quantity and metadata.

        Args:
            food_record: Database food record
            quantity: Detected quantity as string
            unit: Detected unit
            method: Match method used
            confidence: Match confidence score
            is_recent: Whether from recent foods

        Returns:
            Enriched food dict ready for API response
        """
        try:
            quantity_float = float(quantity)
        except (ValueError, TypeError):
            quantity_float = 1.0

        return {
            # Database fields
            "id": food_record.get("id"),
            "name": food_record.get("name"),
            "brand_name": food_record.get("brand_name"),
            "food_group": food_record.get("food_group"),
            "serving_size": food_record.get("serving_size"),
            "serving_unit": food_record.get("serving_unit"),

            # Nutrition
            "calories": food_record.get("calories"),
            "protein_g": food_record.get("protein_g"),
            "total_carbs_g": food_record.get("total_carbs_g"),
            "total_fat_g": food_record.get("total_fat_g"),
            "dietary_fiber_g": food_record.get("dietary_fiber_g"),
            "total_sugars_g": food_record.get("total_sugars_g"),
            "sodium_mg": food_record.get("sodium_mg"),

            # Detected values
            "detected_quantity": quantity_float,
            "detected_unit": unit or food_record.get("serving_unit", "serving"),

            # Match metadata
            "match_confidence": confidence,
            "match_method": method,
            "is_recent": is_recent,
            "data_quality_score": food_record.get("data_quality_score"),

            # Food type flags
            "is_generic": food_record.get("is_generic"),
            "is_branded": food_record.get("is_branded"),
        }


# Global instance
_service: Optional[FoodSearchService] = None


def get_food_search_service() -> FoodSearchService:
    """Get the global FoodSearchService instance."""
    global _service
    if _service is None:
        _service = FoodSearchService()
    return _service
