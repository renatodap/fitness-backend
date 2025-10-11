"""
Coach Tool Service

Provides focused, on-demand data access tools for the agentic coach.
Instead of retrieving ALL data upfront, Claude calls only the tools it needs.

This enables:
- On-demand data fetching (80% cost reduction for simple queries)
- Multi-step reasoning (chain tools intelligently)
- Adaptive retrieval (request more data if needed)
- Better accuracy (get exactly what's needed)
"""

import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta

from app.services.supabase_service import get_service_client
from app.services.multimodal_embedding_service import get_multimodal_service

logger = logging.getLogger(__name__)


class CoachToolService:
    """
    Provides on-demand data access tools for the agentic coach.

    Each method is a "tool" that Claude can call dynamically.
    Tools are focused, fast, and return only what's needed.
    """

    def __init__(self):
        self.supabase = get_service_client()
        self.embedding_service = get_multimodal_service()

    # ====== PROFILE & GOALS TOOLS ======

    async def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's profile with goals and preferences.

        Returns essential user info:
        - Name, age, biological sex
        - Current weight, goal weight, height
        - Primary goal (lose weight, gain muscle, etc.)
        - Experience level, training frequency
        - Dietary restrictions, available equipment
        - Daily macro targets (calories, protein, carbs, fats)

        Args:
            user_id: User's UUID

        Returns:
            User profile dict with all relevant data
        """
        try:
            logger.info(f"[Tool:get_user_profile] Fetching profile for user {user_id}")

            response = self.supabase.table("profiles")\
                .select("*")\
                .eq("id", user_id)\
                .single()\
                .execute()

            if response.data:
                logger.info("[Tool:get_user_profile] Profile retrieved successfully")
                return {
                    "success": True,
                    "profile": response.data
                }
            else:
                logger.warning("[Tool:get_user_profile] No profile found")
                return {
                    "success": False,
                    "error": "Profile not found"
                }

        except Exception as e:
            logger.error(f"[Tool:get_user_profile] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_active_nutrition_program(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's active nutrition program with macro targets.

        Returns:
        - Program name and goal
        - Daily calorie target
        - Protein, carbs, fat targets in grams
        - Start date and status

        Args:
            user_id: User's UUID

        Returns:
            Nutrition program dict or None if no active program
        """
        try:
            logger.info(f"[Tool:get_active_nutrition_program] Fetching for user {user_id}")

            response = self.supabase.table("nutrition_programs")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("status", "active")\
                .order("created_at", desc=True)\
                .limit(1)\
                .execute()

            if response.data:
                logger.info(f"[Tool:get_active_nutrition_program] Program found: {response.data[0].get('name')}")
                return {
                    "success": True,
                    "program": response.data[0]
                }
            else:
                logger.info("[Tool:get_active_nutrition_program] No active program")
                return {
                    "success": True,
                    "program": None
                }

        except Exception as e:
            logger.error(f"[Tool:get_active_nutrition_program] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_active_workout_program(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's active workout program.

        Returns:
        - Program name and goal
        - Frequency (days per week)
        - Start date and status
        - Description

        Args:
            user_id: User's UUID

        Returns:
            Workout program dict or None if no active program
        """
        try:
            logger.info(f"[Tool:get_active_workout_program] Fetching for user {user_id}")

            response = self.supabase.table("workout_programs")\
                .select("*")\
                .eq("user_id", user_id)\
                .eq("status", "active")\
                .order("created_at", desc=True)\
                .limit(1)\
                .execute()

            if response.data:
                logger.info(f"[Tool:get_active_workout_program] Program found: {response.data[0].get('name')}")
                return {
                    "success": True,
                    "program": response.data[0]
                }
            else:
                logger.info("[Tool:get_active_workout_program] No active program")
                return {
                    "success": True,
                    "program": None
                }

        except Exception as e:
            logger.error(f"[Tool:get_active_workout_program] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    # ====== NUTRITION TOOLS ======

    async def get_daily_nutrition_summary(self, user_id: str, date: str) -> Dict[str, Any]:
        """
        Get nutrition summary for a specific date.

        Calculates totals from all meal logs on that date:
        - Total calories
        - Total protein, carbs, fats
        - Number of meals logged
        - Breakdown by meal type

        Args:
            user_id: User's UUID
            date: Date in YYYY-MM-DD format (e.g., "2025-10-08")

        Returns:
            Daily nutrition summary with totals
        """
        try:
            logger.info(f"[Tool:get_daily_nutrition_summary] Fetching for {date}")

            # Parse date
            date_obj = datetime.strptime(date, "%Y-%m-%d")
            start_of_day = date_obj.replace(hour=0, minute=0, second=0, microsecond=0)
            end_of_day = date_obj.replace(hour=23, minute=59, second=59, microsecond=999999)

            response = self.supabase.table("meals")\
                .select("*")\
                .eq("user_id", user_id)\
                .gte("logged_at", start_of_day.isoformat())\
                .lte("logged_at", end_of_day.isoformat())\
                .execute()

            meals = response.data if response.data else []

            # Calculate totals
            total_calories = 0
            total_protein = 0
            total_carbs = 0
            total_fats = 0

            for meal in meals:
                total_calories += meal.get("calories") or meal.get("total_calories", 0)
                total_protein += meal.get("protein_g") or meal.get("total_protein_g", 0)
                total_carbs += meal.get("carbs_g") or meal.get("total_carbs_g", 0)
                total_fats += meal.get("fat_g") or meal.get("total_fat_g", 0)

            logger.info(f"[Tool:get_daily_nutrition_summary] Found {len(meals)} meals, {total_calories} cal")

            return {
                "success": True,
                "date": date,
                "summary": {
                    "total_calories": round(total_calories, 1),
                    "total_protein_g": round(total_protein, 1),
                    "total_carbs_g": round(total_carbs, 1),
                    "total_fats_g": round(total_fats, 1),
                    "meal_count": len(meals),
                    "meals": meals
                }
            }

        except Exception as e:
            logger.error(f"[Tool:get_daily_nutrition_summary] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_recent_meals(self, user_id: str, days: int = 3) -> Dict[str, Any]:
        """
        Get recent meals (last N days).

        Unlike the old RAG which got 30 days, this is focused and fast.
        Perfect for "what did I eat recently?" type questions.

        Args:
            user_id: User's UUID
            days: Number of days to look back (default 3, max 30)

        Returns:
            List of recent meal logs
        """
        try:
            days = min(days, 30)  # Cap at 30 days
            logger.info(f"[Tool:get_recent_meals] Fetching last {days} days")

            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

            response = self.supabase.table("meals")\
                .select("*")\
                .eq("user_id", user_id)\
                .gte("logged_at", cutoff)\
                .order("logged_at", desc=True)\
                .limit(50)\
                .execute()

            meals = response.data if response.data else []
            logger.info(f"[Tool:get_recent_meals] Found {len(meals)} meals")

            return {
                "success": True,
                "days": days,
                "count": len(meals),
                "meals": meals
            }

        except Exception as e:
            logger.error(f"[Tool:get_recent_meals] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def search_food_database(self, query: str, limit: int = 10) -> Dict[str, Any]:
        """
        Search the food database by name.

        Useful when user asks "how many calories are in X?" or similar.

        Args:
            query: Food name to search for
            limit: Max number of results (default 10)

        Returns:
            List of matching foods with nutrition data
        """
        try:
            logger.info(f"[Tool:search_food_database] Searching for '{query}'")

            response = self.supabase.table("foods")\
                .select("*")\
                .ilike("name", f"%{query}%")\
                .limit(limit)\
                .execute()

            foods = response.data if response.data else []
            logger.info(f"[Tool:search_food_database] Found {len(foods)} foods")

            return {
                "success": True,
                "query": query,
                "count": len(foods),
                "foods": foods
            }

        except Exception as e:
            logger.error(f"[Tool:search_food_database] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    # ====== TRAINING TOOLS ======

    async def get_recent_activities(self, user_id: str, days: int = 3) -> Dict[str, Any]:
        """
        Get recent activities/workouts (last N days).

        Focused and fast, unlike old RAG which got 30 days.

        Args:
            user_id: User's UUID
            days: Number of days to look back (default 3, max 30)

        Returns:
            List of recent activities
        """
        try:
            days = min(days, 30)  # Cap at 30 days
            logger.info(f"[Tool:get_recent_activities] Fetching last {days} days")

            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

            response = self.supabase.table("activities")\
                .select("*")\
                .eq("user_id", user_id)\
                .gte("start_date", cutoff)\
                .order("start_date", desc=True)\
                .limit(50)\
                .execute()

            activities = response.data if response.data else []
            logger.info(f"[Tool:get_recent_activities] Found {len(activities)} activities")

            return {
                "success": True,
                "days": days,
                "count": len(activities),
                "activities": activities
            }

        except Exception as e:
            logger.error(f"[Tool:get_recent_activities] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def get_activity_details(self, user_id: str, activity_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific activity.

        Includes all exercises, sets, reps, weights.

        Args:
            user_id: User's UUID
            activity_id: Activity UUID

        Returns:
            Detailed activity data
        """
        try:
            logger.info(f"[Tool:get_activity_details] Fetching activity {activity_id}")

            response = self.supabase.table("activities")\
                .select("*")\
                .eq("id", activity_id)\
                .eq("user_id", user_id)\
                .single()\
                .execute()

            if response.data:
                logger.info("[Tool:get_activity_details] Activity found")
                return {
                    "success": True,
                    "activity": response.data
                }
            else:
                logger.warning("[Tool:get_activity_details] Activity not found")
                return {
                    "success": False,
                    "error": "Activity not found"
                }

        except Exception as e:
            logger.error(f"[Tool:get_activity_details] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def analyze_training_volume(self, user_id: str, days: int = 7) -> Dict[str, Any]:
        """
        Analyze training volume over the last N days.

        Calculates:
        - Total training time
        - Number of workouts
        - Average duration
        - Activity type breakdown

        Args:
            user_id: User's UUID
            days: Number of days to analyze (default 7)

        Returns:
            Training volume analysis
        """
        try:
            logger.info(f"[Tool:analyze_training_volume] Analyzing last {days} days")

            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

            response = self.supabase.table("activities")\
                .select("*")\
                .eq("user_id", user_id)\
                .gte("start_date", cutoff)\
                .execute()

            activities = response.data if response.data else []

            # Calculate metrics
            total_time = sum(a.get("duration_minutes", 0) for a in activities)
            workout_count = len(activities)
            avg_duration = total_time / workout_count if workout_count > 0 else 0

            # Activity type breakdown
            type_counts = {}
            for activity in activities:
                activity_type = activity.get("activity_type", "Unknown")
                type_counts[activity_type] = type_counts.get(activity_type, 0) + 1

            logger.info(f"[Tool:analyze_training_volume] {workout_count} workouts, {total_time} min total")

            return {
                "success": True,
                "days": days,
                "analysis": {
                    "total_time_minutes": round(total_time, 1),
                    "workout_count": workout_count,
                    "average_duration_minutes": round(avg_duration, 1),
                    "activity_type_breakdown": type_counts
                }
            }

        except Exception as e:
            logger.error(f"[Tool:analyze_training_volume] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    # ====== PROGRESS TOOLS ======

    async def get_body_measurements(self, user_id: str, days: int = 7) -> Dict[str, Any]:
        """
        Get body measurements from the last N days.

        Args:
            user_id: User's UUID
            days: Number of days to look back (default 7)

        Returns:
            List of body measurements
        """
        try:
            logger.info(f"[Tool:get_body_measurements] Fetching last {days} days")

            cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

            response = self.supabase.table("body_measurements")\
                .select("*")\
                .eq("user_id", user_id)\
                .gte("measured_at", cutoff)\
                .order("measured_at", desc=True)\
                .execute()

            measurements = response.data if response.data else []
            logger.info(f"[Tool:get_body_measurements] Found {len(measurements)} measurements")

            return {
                "success": True,
                "days": days,
                "count": len(measurements),
                "measurements": measurements
            }

        except Exception as e:
            logger.error(f"[Tool:get_body_measurements] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def calculate_progress_trend(
        self,
        user_id: str,
        metric: str,
        days: int = 30
    ) -> Dict[str, Any]:
        """
        Calculate progress trend for a specific metric.

        Supported metrics:
        - "weight" - Body weight trend
        - "calories" - Daily calorie average
        - "protein" - Daily protein average
        - "training_volume" - Weekly training time

        Args:
            user_id: User's UUID
            metric: Metric to track
            days: Number of days to analyze (default 30)

        Returns:
            Progress trend analysis with direction and rate of change
        """
        try:
            logger.info(f"[Tool:calculate_progress_trend] Analyzing {metric} over {days} days")

            if metric == "weight":
                # Get weight measurements
                cutoff = (datetime.utcnow() - timedelta(days=days)).isoformat()

                response = self.supabase.table("body_measurements")\
                    .select("weight_kg, weight_lbs, measured_at")\
                    .eq("user_id", user_id)\
                    .gte("measured_at", cutoff)\
                    .order("measured_at", desc=False)\
                    .execute()

                measurements = response.data if response.data else []

                if len(measurements) < 2:
                    return {
                        "success": False,
                        "error": "Not enough data points (need at least 2 measurements)"
                    }

                # Calculate trend
                first_weight = measurements[0].get("weight_kg") or measurements[0].get("weight_lbs", 0)
                last_weight = measurements[-1].get("weight_kg") or measurements[-1].get("weight_lbs", 0)
                change = last_weight - first_weight

                direction = "increasing" if change > 0 else "decreasing" if change < 0 else "stable"

                logger.info(f"[Tool:calculate_progress_trend] Weight {direction} by {abs(change):.1f}")

                return {
                    "success": True,
                    "metric": "weight",
                    "days": days,
                    "trend": {
                        "direction": direction,
                        "change": round(change, 2),
                        "first_value": round(first_weight, 2),
                        "last_value": round(last_weight, 2),
                        "data_points": len(measurements)
                    }
                }

            else:
                return {
                    "success": False,
                    "error": f"Metric '{metric}' not yet supported"
                }

        except Exception as e:
            logger.error(f"[Tool:calculate_progress_trend] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    # ====== PROACTIVE LOGGING TOOLS ======

    async def create_meal_log_from_description(
        self,
        user_id: str,
        meal_type: str,
        description: str,
        foods: List[str],
        estimated_calories: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create a meal log from natural language description.

        Claude calls this when user mentions eating food.

        NEW FLOW (same as photo meal logging):
        1. Parse text with text_meal_parser_service (extract quantities)
        2. Match foods with photo_meal_matcher_service
        3. Construct preview with photo_meal_constructor_service
        4. Return preview for user confirmation

        Args:
            user_id: User's UUID
            meal_type: "breakfast", "lunch", "dinner", "snack"
            description: Natural language description of the meal
            foods: List of food names mentioned
            estimated_calories: Optional calorie estimate (ignored, we use database)

        Returns:
            Meal log preview for user confirmation (same format as photo logging)
        """
        try:
            logger.info(f"[Tool:create_meal_log] Creating meal: {meal_type} - {description}")
            logger.info(f"[Tool:create_meal_log] Foods: {foods}")

            # STEP 1: Parse natural language description with text_meal_parser_service
            from app.services.text_meal_parser_service import get_text_meal_parser_service

            text_parser = get_text_meal_parser_service()

            # Parse the full description to extract quantities and food details
            logger.info("[Tool:create_meal_log] Parsing meal text for quantities...")
            parse_result = await text_parser.parse_meal_text(
                user_message=description,
                user_context={"meal_type": meal_type}
            )

            logger.info(
                f"[Tool:create_meal_log] Parsed {len(parse_result['food_items'])} foods "
                f"(tokens={parse_result.get('tokens_used', 0)})"
            )

            # STEP 2: Match detected foods with database using photo_meal_matcher_service
            from app.services.photo_meal_matcher_service import get_photo_meal_matcher_service

            matcher_service = get_photo_meal_matcher_service()

            logger.info("[Tool:create_meal_log] Matching foods to database...")
            match_result = await matcher_service.match_photo_foods(
                detected_foods=parse_result["food_items"],
                user_id=user_id
            )

            logger.info(
                f"[Tool:create_meal_log] Matched {match_result['total_matched']}/{match_result['total_detected']} foods"
            )

            # STEP 3: Construct meal preview with photo_meal_constructor_service
            from app.services.photo_meal_constructor_service import get_photo_meal_constructor_service

            constructor_service = get_photo_meal_constructor_service()

            logger.info("[Tool:create_meal_log] Constructing meal preview...")
            meal_preview = await constructor_service.construct_meal_preview(
                matched_foods=match_result["matched_foods"],
                meal_metadata={
                    "meal_type": parse_result.get("meal_type", meal_type),
                    "description": parse_result.get("description", description)
                },
                user_id=user_id
            )

            logger.info(
                f"[Tool:create_meal_log] Preview ready: {meal_preview['totals']['calories']} cal, "
                f"{meal_preview['totals']['protein_g']}g protein"
            )

            # STEP 4: Return preview in tool result format
            # This will be handled by unified_coach_service which will show inline preview
            return {
                "success": True,
                "log_type": "meal",
                "requires_confirmation": True,  # Frontend should show inline meal preview
                "meal_data": meal_preview,  # Full preview data (same as photo logging)
                "message": (
                    f"I detected a {meal_preview['meal_type']} with "
                    f"{meal_preview['meta']['total_foods']} foods. "
                    f"Total: {round(meal_preview['totals']['calories'])} cal, "
                    f"{round(meal_preview['totals']['protein_g'])}g protein"
                )
            }

        except Exception as e:
            logger.error(f"[Tool:create_meal_log] Failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "message": f"Failed to parse meal: {str(e)}"
            }

    async def create_activity_log_from_description(
        self,
        user_id: str,
        activity_type: str,
        description: str,
        duration_minutes: Optional[int] = None,
        distance_km: Optional[float] = None,
        calories_burned: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Create an activity log from natural language description.

        Claude calls this when user mentions a workout/exercise.

        Behavior depends on user's auto_log_enabled preference:
        - FALSE (default): Returns preview for user review/confirmation
        - TRUE: Immediately saves to database, user can edit later

        Args:
            user_id: User's UUID
            activity_type: "running", "cycling", "strength_training", "walking", etc.
            description: Natural language description
            duration_minutes: Duration in minutes
            distance_km: Distance in kilometers (for cardio)
            calories_burned: Estimated calories burned

        Returns:
            Activity log preview OR saved confirmation
        """
        try:
            logger.info(f"[Tool:create_activity_log] Creating activity: {activity_type} - {description}")

            # STEP 1: Check user's auto_log preference
            try:
                profile_response = self.supabase.table("profiles")\
                    .select("auto_log_enabled")\
                    .eq("id", user_id)\
                    .single()\
                    .execute()

                auto_log_enabled = profile_response.data.get("auto_log_enabled", False) if profile_response.data else False
                logger.info(f"[Tool:create_activity_log] auto_log_enabled: {auto_log_enabled}")
            except Exception as pref_err:
                logger.warning(f"[Tool:create_activity_log] Failed to fetch preference, defaulting to FALSE: {pref_err}")
                auto_log_enabled = False

            # STEP 2: Estimate duration if not provided (use heuristics)
            if not duration_minutes:
                # Simple heuristics
                if "5k" in description.lower() or "5 k" in description.lower():
                    duration_minutes = 30  # Typical 5K time
                elif "10k" in description.lower():
                    duration_minutes = 60
                elif distance_km:
                    # Assume 6 min/km pace for running
                    duration_minutes = int(distance_km * 6)
                else:
                    duration_minutes = 30  # Default

            # Estimate calories if not provided
            if not calories_burned:
                # Very rough estimate: ~10 cal/min for moderate intensity
                calories_burned = duration_minutes * 10

            # Build activity data
            activity_data = {
                "activity_type": activity_type,
                "description": description,
                "duration_minutes": duration_minutes,
                "calories_burned": calories_burned,
                "start_date": datetime.utcnow().isoformat()
            }

            if distance_km:
                activity_data["distance_km"] = distance_km

            logger.info(f"[Tool:create_activity_log] Activity data: {activity_data}")

            # STEP 3: BRANCH based on auto_log preference
            if auto_log_enabled:
                # AUTO-LOG MODE: Save immediately
                logger.info("[Tool:create_activity_log] AUTO-LOGGING (auto_log=true)")

                # Save to activities table
                try:
                    activity_entry = {
                        "user_id": user_id,
                        "activity_type": activity_type,
                        "description": description,
                        "duration_minutes": duration_minutes,
                        "calories_burned": calories_burned,
                        "start_date": datetime.utcnow().isoformat(),
                        "created_at": datetime.utcnow().isoformat()
                    }

                    if distance_km:
                        activity_entry["distance_km"] = distance_km

                    saved_activity = self.supabase.table("activities")\
                        .insert(activity_entry)\
                        .execute()

                    activity_id = saved_activity.data[0]["id"] if saved_activity.data else None

                    logger.info(f"[Tool:create_activity_log] Auto-saved activity log: {activity_id}")

                    return {
                        "success": True,
                        "log_type": "activity",
                        "auto_logged": True,
                        "activity_id": activity_id,
                        "activity_data": activity_data,
                        "message": f"✅ Auto-logged {activity_type.replace('_', ' ').title()}: {description} ({duration_minutes} min, ~{calories_burned} cal burned)"
                    }

                except Exception as save_err:
                    logger.error(f"[Tool:create_activity_log] Auto-save failed: {save_err}", exc_info=True)
                    # Fall back to preview mode on error
                    return {
                        "success": True,
                        "log_type": "activity",
                        "requires_confirmation": True,
                        "activity_data": activity_data,
                        "message": f"Preview: {activity_type.replace('_', ' ').title()} - {duration_minutes} min (auto-save failed, needs manual confirm)"
                    }

            else:
                # PREVIEW MODE: Return for user confirmation
                logger.info("[Tool:create_activity_log] PREVIEW MODE (auto_log=false)")

                return {
                    "success": True,
                    "log_type": "activity",
                    "requires_confirmation": True,  # Frontend should show review card
                    "activity_data": activity_data,
                    "message": f"Preview: {activity_type.replace('_', ' ').title()} - {duration_minutes} min, ~{calories_burned} cal burned"
                }

        except Exception as e:
            logger.error(f"[Tool:create_activity_log] Failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    async def create_body_measurement_log(
        self,
        user_id: str,
        weight_lbs: Optional[float] = None,
        weight_kg: Optional[float] = None,
        body_fat_percentage: Optional[float] = None,
        notes: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Create a body measurement log.

        Claude calls this when user mentions their weight or measurements.

        Behavior depends on user's auto_log_enabled preference:
        - FALSE (default): Returns preview for user review/confirmation
        - TRUE: Immediately saves to database, user can edit later

        Args:
            user_id: User's UUID
            weight_lbs: Weight in pounds
            weight_kg: Weight in kilograms
            body_fat_percentage: Body fat %
            notes: Additional notes

        Returns:
            Measurement log preview OR saved confirmation
        """
        try:
            logger.info(f"[Tool:create_body_measurement_log] Creating measurement for user {user_id}")

            # STEP 1: Check user's auto_log preference
            try:
                profile_response = self.supabase.table("profiles")\
                    .select("auto_log_enabled")\
                    .eq("id", user_id)\
                    .single()\
                    .execute()

                auto_log_enabled = profile_response.data.get("auto_log_enabled", False) if profile_response.data else False
                logger.info(f"[Tool:create_body_measurement_log] auto_log_enabled: {auto_log_enabled}")
            except Exception as pref_err:
                logger.warning(f"[Tool:create_body_measurement_log] Failed to fetch preference, defaulting to FALSE: {pref_err}")
                auto_log_enabled = False

            # STEP 2: Convert weight if only one unit provided
            if weight_lbs and not weight_kg:
                weight_kg = weight_lbs * 0.453592
            elif weight_kg and not weight_lbs:
                weight_lbs = weight_kg * 2.20462

            measurement_data = {
                "weight_lbs": round(weight_lbs, 1) if weight_lbs else None,
                "weight_kg": round(weight_kg, 1) if weight_kg else None,
                "body_fat_percentage": round(body_fat_percentage, 1) if body_fat_percentage else None,
                "measured_at": datetime.utcnow().isoformat(),
                "notes": notes
            }

            logger.info(f"[Tool:create_body_measurement_log] Measurement data: {measurement_data}")

            # STEP 3: BRANCH based on auto_log preference
            if auto_log_enabled:
                # AUTO-LOG MODE: Save immediately
                logger.info("[Tool:create_body_measurement_log] AUTO-LOGGING (auto_log=true)")

                # Save to body_measurements table
                try:
                    measurement_entry = {
                        "user_id": user_id,
                        "weight_lbs": measurement_data["weight_lbs"],
                        "weight_kg": measurement_data["weight_kg"],
                        "body_fat_percentage": measurement_data["body_fat_percentage"],
                        "measured_at": datetime.utcnow().isoformat(),
                        "notes": notes,
                        "created_at": datetime.utcnow().isoformat()
                    }

                    saved_measurement = self.supabase.table("body_measurements")\
                        .insert(measurement_entry)\
                        .execute()

                    measurement_id = saved_measurement.data[0]["id"] if saved_measurement.data else None

                    logger.info(f"[Tool:create_body_measurement_log] Auto-saved measurement: {measurement_id}")

                    return {
                        "success": True,
                        "log_type": "measurement",
                        "auto_logged": True,
                        "measurement_id": measurement_id,
                        "measurement_data": measurement_data,
                        "message": f"✅ Auto-logged weight: {round(weight_lbs, 1)} lbs ({round(weight_kg, 1)} kg)" + (f", {body_fat_percentage}% BF" if body_fat_percentage else "")
                    }

                except Exception as save_err:
                    logger.error(f"[Tool:create_body_measurement_log] Auto-save failed: {save_err}", exc_info=True)
                    # Fall back to preview mode on error
                    return {
                        "success": True,
                        "log_type": "measurement",
                        "requires_confirmation": True,
                        "measurement_data": measurement_data,
                        "message": f"Preview: Weight {round(weight_lbs, 1)} lbs (auto-save failed, needs manual confirm)"
                    }

            else:
                # PREVIEW MODE: Return for user confirmation
                logger.info("[Tool:create_body_measurement_log] PREVIEW MODE (auto_log=false)")

                return {
                    "success": True,
                    "log_type": "measurement",
                    "requires_confirmation": True,  # Frontend should show review card
                    "measurement_data": measurement_data,
                    "message": f"Preview: Weight {round(weight_lbs, 1)} lbs ({round(weight_kg, 1)} kg)" + (f", {body_fat_percentage}% BF" if body_fat_percentage else "")
                }

        except Exception as e:
            logger.error(f"[Tool:create_body_measurement_log] Failed: {e}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    # ====== PERPLEXITY TOOLS (REAL-TIME INTELLIGENCE) ======

    async def search_latest_nutrition_info(
        self,
        query: str,
        food_name: str,
        user_id: str  # Required for tool injection but not used by Perplexity
    ) -> Dict[str, Any]:
        """
        Search for LATEST real-time nutrition info using Perplexity AI.

        Perfect for:
        - New restaurant items ("2025 Chipotle Chicken Bowl")
        - Seasonal foods ("Current Starbucks PSL nutrition")
        - Regional variations ("UK vs US McDonald's Big Mac")
        - Latest menu changes

        Args:
            query: Search query for nutrition info
            food_name: Specific food name to research
            user_id: User UUID (injected by system)

        Returns:
            Latest nutrition data from Perplexity
        """
        try:
            logger.info(f"[Tool:search_latest_nutrition_info] Query: '{query}'")

            from app.services.perplexity_service import get_perplexity_service
            perplexity = get_perplexity_service()

            result = await perplexity.search_nutrition_info(
                food_name=food_name,
                quantity="100",  # Default to 100g for comparison
                unit="g",
                user_context=query
            )

            if result["success"]:
                food_data = result["food_data"]
                logger.info(f"[Tool:search_latest_nutrition_info] Found: {food_data['name']}")

                return {
                    "success": True,
                    "food": {
                        "name": food_data["name"],
                        "brand": food_data.get("brand_name"),
                        "serving_size": f"{food_data['serving_size']}{food_data['serving_unit']}",
                        "calories": food_data["calories"],
                        "protein_g": food_data["protein_g"],
                        "carbs_g": food_data["total_carbs_g"],
                        "fat_g": food_data["total_fat_g"],
                        "fiber_g": food_data.get("dietary_fiber_g", 0),
                        "source": food_data.get("source", "Perplexity"),
                        "confidence": food_data.get("confidence", 0.9),
                        "last_updated": food_data.get("last_updated")
                    },
                    "sources": result.get("sources", []),
                    "reasoning": result.get("reasoning", "")
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Not found")
                }

        except Exception as e:
            logger.error(f"[Tool:search_latest_nutrition_info] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    async def analyze_food_healthiness(
        self,
        food_name: str,
        user_goal: Optional[str] = None,
        user_id: str = None  # Required for tool injection
    ) -> Dict[str, Any]:
        """
        Analyze if a food is healthy using latest research (Perplexity).

        Perfect for "Is X healthy?" questions.
        Uses real-time web search for current nutrition science.

        Args:
            food_name: Food to analyze
            user_goal: User's fitness goal (weight loss, muscle gain, etc.)
            user_id: User UUID (injected by system)

        Returns:
            Health analysis with pros/cons and recommendations
        """
        try:
            logger.info(f"[Tool:analyze_food_healthiness] Analyzing: {food_name}")

            from app.services.perplexity_service import get_perplexity_service
            perplexity = get_perplexity_service()

            # Get dietary restrictions from user profile if available
            dietary_restrictions = None
            if user_id:
                try:
                    profile = await self.supabase.table("profiles")\
                        .select("dietary_preferences")\
                        .eq("id", user_id)\
                        .single()\
                        .execute()

                    if profile.data:
                        dietary_restrictions = profile.data.get("dietary_preferences", [])
                except:
                    pass

            result = await perplexity.analyze_food_healthiness(
                food_name=food_name,
                user_goal=user_goal,
                dietary_restrictions=dietary_restrictions
            )

            if result["success"]:
                analysis = result["analysis"]
                logger.info(f"[Tool:analyze_food_healthiness] Rating: {analysis['overall_rating']}")

                return {
                    "success": True,
                    "analysis": analysis
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error", "Analysis failed")
                }

        except Exception as e:
            logger.error(f"[Tool:analyze_food_healthiness] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }

    # ====== SEMANTIC SEARCH TOOL (RAG) ======

    async def semantic_search_user_data(
        self,
        user_id: str,
        query: str,
        limit: int = 5
    ) -> Dict[str, Any]:
        """
        Perform semantic search across ALL user data.

        This is the RAG component - searches:
        - Quick entry logs (meals, workouts, measurements)
        - Coach conversation history
        - Multimodal embeddings (text, images, audio)

        Use this when you need to find relevant historical context
        that isn't covered by the focused tools above.

        Args:
            user_id: User's UUID
            query: Search query
            limit: Max results to return (default 5)

        Returns:
            Semantically similar results from user's history
        """
        try:
            logger.info(f"[Tool:semantic_search_user_data] Searching for '{query[:50]}...'")

            # Generate query embedding
            query_embedding = await self.embedding_service.embed_text(query)
            embedding_list = query_embedding.tolist() if hasattr(query_embedding, 'tolist') else query_embedding

            # Search quick_entry_embeddings
            response = self.supabase.rpc(
                "search_quick_entry_embeddings",
                {
                    "query_embedding": embedding_list,
                    "user_id_filter": user_id,
                    "match_threshold": 0.5,
                    "match_count": limit
                }
            ).execute()

            results = response.data if response.data else []
            logger.info(f"[Tool:semantic_search_user_data] Found {len(results)} results")

            return {
                "success": True,
                "query": query,
                "count": len(results),
                "results": results
            }

        except Exception as e:
            logger.error(f"[Tool:semantic_search_user_data] Failed: {e}")
            return {
                "success": False,
                "error": str(e)
            }


# Global instance
_tool_service: Optional[CoachToolService] = None


def get_tool_service() -> CoachToolService:
    """Get the global CoachToolService instance."""
    global _tool_service
    if _tool_service is None:
        _tool_service = CoachToolService()
    return _tool_service


# ====== TOOL DEFINITIONS FOR CLAUDE ======
# These define the schema Claude sees for tool calling

COACH_TOOLS = [
    {
        "name": "get_user_profile",
        "description": "Get the user's profile including goals, preferences, body stats, and daily macro targets. Use this to understand their goals and personalize advice.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's UUID"
                }
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "get_daily_nutrition_summary",
        "description": "Get nutrition totals for a specific date - total calories, protein, carbs, fats, and meal count. Perfect for 'did I hit my goals today?' type questions.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's UUID"
                },
                "date": {
                    "type": "string",
                    "description": "Date in YYYY-MM-DD format (e.g., '2025-10-08')"
                }
            },
            "required": ["user_id", "date"]
        }
    },
    {
        "name": "get_recent_meals",
        "description": "Get the user's recent meals from the last N days (default 3, max 30). Use this to see what they've been eating lately.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's UUID"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to look back (default 3, max 30)",
                    "default": 3
                }
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "get_recent_activities",
        "description": "Get the user's recent workouts/activities from the last N days (default 3, max 30). Use this to see their training recently.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's UUID"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to look back (default 3, max 30)",
                    "default": 3
                }
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "analyze_training_volume",
        "description": "Analyze the user's training volume over the last N days - total time, workout count, average duration, and activity type breakdown.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's UUID"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to analyze (default 7)",
                    "default": 7
                }
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "get_body_measurements",
        "description": "Get the user's body measurements (weight, etc.) from the last N days.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's UUID"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to look back (default 7)",
                    "default": 7
                }
            },
            "required": ["user_id"]
        }
    },
    {
        "name": "calculate_progress_trend",
        "description": "Calculate progress trend for a metric over N days. Supported metrics: 'weight', 'calories', 'protein', 'training_volume'.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's UUID"
                },
                "metric": {
                    "type": "string",
                    "description": "Metric to track: 'weight', 'calories', 'protein', or 'training_volume'"
                },
                "days": {
                    "type": "integer",
                    "description": "Number of days to analyze (default 30)",
                    "default": 30
                }
            },
            "required": ["user_id", "metric"]
        }
    },
    {
        "name": "semantic_search_user_data",
        "description": "Search across ALL user data semantically (RAG). Use this when you need historical context that isn't covered by other tools - finds relevant meals, workouts, conversations, etc. based on meaning.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "The user's UUID"
                },
                "query": {
                    "type": "string",
                    "description": "Search query to find relevant historical data"
                },
                "limit": {
                    "type": "integer",
                    "description": "Max number of results (default 5)",
                    "default": 5
                }
            },
            "required": ["user_id", "query"]
        }
    },
    {
        "name": "search_food_database",
        "description": "Search the food database by name to get nutrition information. Use when user asks 'how many calories are in X?'",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Food name to search for"
                },
                "limit": {
                    "type": "integer",
                    "description": "Max number of results (default 10)",
                    "default": 10
                }
            },
            "required": ["query"]
        }
    },
    {
        "name": "create_meal_log_from_description",
        "description": "PROACTIVELY log a meal when the user mentions eating food in past tense. Examples: 'I had eggs for breakfast', 'ate chicken and rice', 'just finished lunch'. Use this to be helpful and log their meals automatically.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User's UUID (will be injected automatically)"
                },
                "meal_type": {
                    "type": "string",
                    "description": "Type of meal: 'breakfast', 'lunch', 'dinner', or 'snack'",
                    "enum": ["breakfast", "lunch", "dinner", "snack"]
                },
                "description": {
                    "type": "string",
                    "description": "Natural language description of what they ate"
                },
                "foods": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of food names mentioned (e.g., ['eggs', 'toast', 'banana'])"
                },
                "estimated_calories": {
                    "type": "integer",
                    "description": "Optional estimated total calories if you can guess based on foods"
                }
            },
            "required": ["meal_type", "description", "foods"]
        }
    },
    {
        "name": "create_activity_log_from_description",
        "description": "PROACTIVELY log a workout/activity when the user mentions exercise in past tense. Examples: 'did a 5k run', 'just finished my workout', 'went for a bike ride'. Use this to be helpful and log their workouts automatically.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User's UUID (will be injected automatically)"
                },
                "activity_type": {
                    "type": "string",
                    "description": "Type of activity: 'running', 'cycling', 'strength_training', 'walking', 'swimming', 'yoga', etc.",
                    "enum": ["running", "cycling", "strength_training", "walking", "swimming", "yoga", "cardio", "hiit", "other"]
                },
                "description": {
                    "type": "string",
                    "description": "Natural language description of the workout"
                },
                "duration_minutes": {
                    "type": "integer",
                    "description": "Duration in minutes (estimate if not mentioned)"
                },
                "distance_km": {
                    "type": "number",
                    "description": "Distance in kilometers for cardio activities (optional)"
                },
                "calories_burned": {
                    "type": "integer",
                    "description": "Estimated calories burned (optional, will be estimated if not provided)"
                }
            },
            "required": ["activity_type", "description"]
        }
    },
    {
        "name": "create_body_measurement_log",
        "description": "PROACTIVELY log body measurements when the user mentions their weight or body stats. Examples: 'I weigh 175 lbs', 'my weight is 80kg', 'body fat is 15%'. Use this to track their progress automatically.",
        "input_schema": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User's UUID (will be injected automatically)"
                },
                "weight_lbs": {
                    "type": "number",
                    "description": "Weight in pounds"
                },
                "weight_kg": {
                    "type": "number",
                    "description": "Weight in kilograms"
                },
                "body_fat_percentage": {
                    "type": "number",
                    "description": "Body fat percentage (e.g., 15.5)"
                },
                "notes": {
                    "type": "string",
                    "description": "Optional notes about the measurement"
                }
            },
            "required": []
        }
    },
    {
        "name": "search_latest_nutrition_info",
        "description": "Search for LATEST real-time nutrition information using Perplexity AI with web access. Use when user asks about NEW foods, restaurant items (e.g., '2025 Chipotle bowl'), seasonal items (e.g., 'current Starbucks PSL'), or when food not in database. Gets most accurate, up-to-date data from official sources.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query for nutrition info (e.g., 'Chipotle Chicken Bowl 2025 nutrition facts', 'Starbucks Pumpkin Spice Latte current nutrition')"
                },
                "food_name": {
                    "type": "string",
                    "description": "The specific food name to research (e.g., 'Chicken Bowl', 'Pumpkin Spice Latte')"
                }
            },
            "required": ["query", "food_name"]
        }
    },
    {
        "name": "analyze_food_healthiness",
        "description": "Use Perplexity AI with real-time web access to analyze if a food is healthy based on LATEST nutrition research. Perfect for 'is X healthy?' questions. Gets current science from peer-reviewed sources, considers user's specific goal (weight loss, muscle gain, etc.), and provides pros/cons with specific recommendations.",
        "input_schema": {
            "type": "object",
            "properties": {
                "food_name": {
                    "type": "string",
                    "description": "Food to analyze for healthiness (e.g., 'quinoa', 'Diet Coke', 'bacon')"
                },
                "user_goal": {
                    "type": "string",
                    "description": "User's fitness goal to contextualize health advice (e.g., 'weight loss', 'muscle gain', 'endurance')"
                }
            },
            "required": ["food_name"]
        }
    }
]
