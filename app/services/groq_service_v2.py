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
from typing import Any, Dict, Optional
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
        if not settings.GROQ_API_KEY:
            logger.error("[GroqV2] ❌ GROQ_API_KEY not set in environment!")
            raise ValueError("GROQ_API_KEY environment variable is required")

        logger.info(f"[GroqV2] Initializing with API key: {settings.GROQ_API_KEY[:10]}...")
        self.client = OpenAI(
            api_key=settings.GROQ_API_KEY,
            base_url="https://api.groq.com/openai/v1",
            timeout=30.0  # 30 second timeout
        )

    async def classify_and_extract(
        self,
        text: str,
        force_type: Optional[str] = None,
        historical_pattern: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Ultra-accurate classification and extraction with UI-friendly output.

        NOW WITH PATTERN-BASED ESTIMATION! Uses historical user data to make
        smarter estimates based on actual behavior.

        Returns structured data optimized for frontend display:
        - primary_fields: Show by default
        - secondary_fields: Show in "expand" section
        - validation: Errors and warnings
        - ui_hints: How to display fields
        """
        if historical_pattern:
            logger.info(f"[GroqV2] Using historical pattern: {historical_pattern.get('sample_size')} similar logs")
        else:
            logger.info("[GroqV2] No historical pattern - using baseline estimation")

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

        system_prompt = """You are an ULTRA-PRECISE fitness data extraction assistant.

{classification_instruction}

CRITICAL ESTIMATION RULES - WHERE TO DRAW THE LINE:

1. **TIMESTAMP ESTIMATION** (ALWAYS REQUIRED - EVERY LOG NEEDS TIME):
   - "ate chicken" → Current time (NOW)
   - "had breakfast" → Today 7:30 AM
   - "lunch was a burrito" → Today 12:30 PM
   - "dinner last night" → Yesterday 6:30 PM
   - "morning run" → Today 7:00 AM
   - "after work workout" → Today 5:30 PM
   - "snack earlier" → 2 hours ago
   - If NO time context → use current time
   - Format: ISO 8601 (e.g., "2025-10-05T12:30:00Z")

2. **MEAL LOGS** - Estimate what's calculable, not what's unknowable:

   ✅ ALWAYS ESTIMATE:
   - `logged_at` - timestamp (use rules above)
   - `meal_type` - infer from time: 6-10am=breakfast, 11am-2pm=lunch, 5-9pm=dinner, else=snack
   - `calories`, `protein_g`, `carbs_g`, `fat_g` - IF food is named
   - Food portions - assume typical (chicken 5oz, rice 1 cup, eggs 2-3)
   - Micronutrients when calculable from portion

   ❌ NEVER ESTIMATE/MAKE UP:
   - Foods not mentioned ("chicken" doesn't mean "chicken with rice and broccoli")
   - Cooking methods not mentioned (don't assume grilled vs fried)

   Example: "ate chicken" → estimate 5oz grilled chicken breast, calculate macros from that
   Example: "ate chicken" → DO NOT add rice, vegetables, or other foods

3. **ACTIVITY LOGS** - Only estimate what's reasonable:

   ✅ ALWAYS EXTRACT IF PROVIDED:
   - `distance_miles` / `distance_km` - IF user says it ("ran 4 miles", "10k run")
   - `pace` - IF user says it ("8:30 pace", "6min/km") - extract the number and add /mile or /km
   - `duration_minutes` - IF user says it OR if you have distance+pace (calculate: distance / (pace_per_mile))

   ✅ ALWAYS ESTIMATE:
   - `start_date` - timestamp from context ("this morning"→7am, "after work"→5pm)
   - `activity_type` - extract from text (ran→running, biked→cycling, swam→swimming)
   - `calories_burned` - IF you have duration (use: duration * 10 for running, duration * 8 for cycling)

   ⚠️ CONDITIONALLY ESTIMATE (only if NOT provided):
   - `duration_minutes` - ONLY if typical activity ("morning run" → ~35min reasonable) OR calculate from distance+pace
   - `rpe` - ONLY if effort words present ("easy"→4, "moderate"→6, "hard"→8)
   - `mood` - ONLY if mood words present ("felt great"→good)

   ❌ NEVER ESTIMATE/MAKE UP:
   - `distance` if not mentioned (too variable - could be 1km or 20km)
   - `pace` if neither distance nor pace mentioned
   - `avg_heart_rate` - impossible to know
   - Specific route or location

   Example: "morning run" → timestamp 7am, duration ~35min, calories ~350 (based on duration), NO distance/pace
   Example: "ran 4 miles at 8:30 pace" → distance=4mi, pace=8:30/mile, duration=34min (calculated), calories=340
   Example: "morning run" → distance=null, pace=null (DON'T MAKE UP)

4. **WORKOUT LOGS** - Only log what user actually said:

   ✅ ALWAYS ESTIMATE:
   - `started_at` - timestamp
   - `completed_at` - IF you estimate duration
   - `workout_name` - derive from context ("chest workout", "leg day")

   ⚠️ CONDITIONALLY ESTIMATE:
   - `duration_minutes` - ONLY if typical ("workout" → ~50min reasonable)
   - `estimated_calories` - ONLY if you have duration
   - `rpe` - ONLY if effort words present
   - `muscle_groups` - ONLY if workout type clear ("chest workout"→["chest"])

   ❌ NEVER ESTIMATE/MAKE UP:
   - `exercises` array - DO NOT add exercises user didn't mention
   - `sets`, `reps`, `weight_lbs` - DO NOT make up
   - Specific exercise details not provided

   Example: "did chest workout" → timestamp, duration ~50min, calories ~300, muscle_groups=["chest"]
   Example: "did chest workout" → exercises=[] or null (DON'T ADD bench press, flyes, etc.)
   Example: "bench pressed" → exercises=[{{"name": "Bench Press"}}] with sets/reps/weight ALL null

5. **THE LINE - WHAT'S REASONABLE VS BULLSHIT**:

   REASONABLE (based on standards/norms):
   - Timestamps from context clues
   - Food portions for named foods
   - Macros calculated from portions
   - Typical durations for common activities
   - Calories from duration + activity type

   BULLSHIT (too personal/variable):
   - Distance for runs (too variable)
   - Pace without distance+time
   - Exercises user didn't mention
   - Sets/reps/weights (impossible to know)
   - Foods user didn't mention

6. **CONFIDENCE LEVELS**:
   - High (0.8-1.0): User provided specific data
   - Medium (0.5-0.8): Reasonable portion/duration assumptions
   - Low (0.3-0.5): Very vague, minimal estimates
   - Use null for unknowable data, mark needs_clarification=true

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

INPUT: "ate chicken and rice"  (VAGUE - no time, no portions - STILL ESTIMATE EVERYTHING)
OUTPUT:
{{
  "type": "meal",
  "confidence": 0.5,
  "data": {{
    "primary_fields": {{
      "meal_name": "Chicken and rice",
      "meal_type": "lunch",
      "logged_at": "2025-10-05T14:30:00Z",
      "calories": 450,
      "protein_g": 50,
      "foods": [
        {{"name": "Chicken breast", "quantity": "5 oz (assumed)"}},
        {{"name": "Rice, cooked", "quantity": "1 cup (assumed)"}}
      ]
    }},
    "secondary_fields": {{
      "carbs_g": 45,
      "fat_g": 6,
      "fiber_g": 2,
      "sugar_g": 0,
      "sodium_mg": 200,
      "foods_detailed": [
        {{
          "name": "Chicken breast",
          "quantity": "5 oz (assumed)",
          "calories": 235,
          "protein_g": 44,
          "carbs_g": 0,
          "fat_g": 5
        }},
        {{
          "name": "White rice, cooked",
          "quantity": "1 cup (assumed)",
          "calories": 205,
          "protein_g": 4,
          "carbs_g": 45,
          "fat_g": 0.4
        }}
      ],
      "tags": ["estimated-all", "needs-verification"]
    }},
    "estimated": true,
    "needs_clarification": true
  }},
  "validation": {{
    "errors": [],
    "warnings": ["Time and portions assumed - no specific data provided"],
    "missing_critical": ["exact_portions", "exact_time"]
  }},
  "suggestions": [
    "Estimated ~450 cal, ~50g protein (assumed 5oz chicken + 1 cup rice)",
    "Time assumed to be current - specify if different",
    "For accuracy: 'had 6oz chicken and 1 cup rice for lunch at 12pm'"
  ]
}}

INPUT: "had eggs for breakfast"  (time context + vague portions)
OUTPUT:
{{
  "type": "meal",
  "confidence": 0.6,
  "data": {{
    "primary_fields": {{
      "meal_name": "Eggs",
      "meal_type": "breakfast",
      "logged_at": "2025-10-05T07:30:00Z",
      "calories": 216,
      "protein_g": 18,
      "foods": [
        {{"name": "Eggs (large)", "quantity": "3 eggs (assumed)"}}
      ]
    }},
    "secondary_fields": {{
      "carbs_g": 1.2,
      "fat_g": 15,
      "fiber_g": 0,
      "sugar_g": 0.5,
      "sodium_mg": 210,
      "cholesterol_mg": 558,
      "tags": ["breakfast", "high-protein", "estimated-portions"]
    }},
    "estimated": true,
    "needs_clarification": true
  }},
  "validation": {{
    "errors": [],
    "warnings": ["Egg quantity assumed (3 eggs typical for breakfast)"],
    "missing_critical": ["exact_egg_count"]
  }},
  "suggestions": [
    "Time inferred as 7:30 AM (breakfast time)",
    "Assumed 3 eggs - specify if different: '2 eggs' or '4 eggs'",
    "Great protein choice for breakfast!"
  ]
}}

INPUT: "Chicken Margherita at Olive Garden"  (restaurant meal with known typical serving)
OUTPUT:
{{
  "type": "meal",
  "confidence": 0.85,
  "data": {{
    "primary_fields": {{
      "meal_name": "Chicken Margherita at Olive Garden",
      "meal_type": "dinner",
      "calories": 870,
      "protein_g": 62,
      "foods": [
        {{"name": "Grilled chicken breast", "quantity": "8-10 oz (estimated)"}},
        {{"name": "Tomato bruschetta topping", "quantity": "~1/2 cup"}},
        {{"name": "Mozzarella cheese", "quantity": "~2 oz"}},
        {{"name": "Balsamic glaze", "quantity": "drizzle"}},
        {{"name": "Parmesan-crusted zucchini", "quantity": "side"}}
      ]
    }},
    "secondary_fields": {{
      "carbs_g": 48,
      "fat_g": 38,
      "fiber_g": 5,
      "sugar_g": 12,
      "sodium_mg": 1580,
      "foods_detailed": [
        {{
          "name": "Grilled chicken breast",
          "quantity": "8-10 oz",
          "calories": 400,
          "protein_g": 50,
          "carbs_g": 0,
          "fat_g": 8
        }},
        {{
          "name": "Mozzarella cheese",
          "quantity": "2 oz",
          "calories": 170,
          "protein_g": 12,
          "carbs_g": 2,
          "fat_g": 13
        }},
        {{
          "name": "Parmesan-crusted zucchini",
          "quantity": "side",
          "calories": 300,
          "protein_g": 0,
          "carbs_g": 46,
          "fat_g": 17
        }}
      ],
      "tags": ["restaurant-food", "italian", "high-protein", "estimated"]
    }},
    "estimated": true,
    "needs_clarification": false
  }},
  "validation": {{
    "errors": [],
    "warnings": ["Nutrition estimated from Olive Garden menu data - actual portions may vary"],
    "missing_critical": []
  }},
  "suggestions": [
    "Solid protein choice!",
    "Restaurant portions tend to be larger - estimate ~870 calories",
    "For exact tracking, ask for nutrition info or weigh/measure leftovers"
  ]
}}

WORKOUT EXAMPLES:

INPUT: "bench press 4x8 @ 185lbs, incline db press 3x10 @ 70lbs"  (specific)
OUTPUT:
{{
  "type": "workout",
  "confidence": 0.9,
  "data": {{
    "primary_fields": {{
      "workout_name": "Chest Press Workout",
      "started_at": "2025-10-05T14:30:00Z",
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
      ],
      "estimated_calories": 280
    }},
    "secondary_fields": {{
      "completed_at": "2025-10-05T15:15:00Z",
      "volume_load": 8020,
      "muscle_groups": ["chest", "triceps", "shoulders"],
      "rpe": 7,
      "tags": ["push", "upper-body", "chest-day"]
    }},
    "estimated": true,
    "needs_clarification": false
  }},
  "validation": {{
    "errors": [],
    "warnings": ["Time assumed to be current"],
    "missing_critical": []
  }},
  "suggestions": [
    "Solid volume! 8,020 lbs total",
    "Time assumed current - add if different",
    "RPE estimated at 7 - confirm effort level"
  ]
}}

INPUT: "did chest workout this morning"  (VAGUE - don't make up exercises)
OUTPUT:
{{
  "type": "workout",
  "confidence": 0.5,
  "data": {{
    "primary_fields": {{
      "workout_name": "Chest Workout",
      "started_at": "2025-10-05T07:00:00Z",
      "duration_minutes": 50,
      "estimated_calories": 300
    }},
    "secondary_fields": {{
      "completed_at": "2025-10-05T07:50:00Z",
      "exercises": [],
      "volume_load": null,
      "muscle_groups": ["chest"],
      "rpe": null,
      "tags": ["upper-body", "chest", "morning"]
    }},
    "estimated": true,
    "needs_clarification": true
  }},
  "validation": {{
    "errors": [],
    "warnings": ["No specific exercises mentioned - cannot estimate workout details"],
    "missing_critical": ["exercises", "sets_reps", "weights"]
  }},
  "suggestions": [
    "Time: 7:00 AM (morning) ✓",
    "Duration: ~50min (estimated typical)",
    "Calories: ~300 (based on duration)",
    "Add exercises for tracking: 'chest workout: bench 185x8, incline press 70x10, flyes 30x12'"
  ]
}}

INPUT: "leg day after work, squats felt heavy"  (has ONE exercise mentioned)
OUTPUT:
{{
  "type": "workout",
  "confidence": 0.6,
  "data": {{
    "primary_fields": {{
      "workout_name": "Leg Day",
      "started_at": "2025-10-05T17:30:00Z",
      "duration_minutes": 60,
      "exercises": [
        {{
          "name": "Squats",
          "sets": null,
          "reps": null,
          "weight_lbs": null,
          "note": "Felt heavy"
        }}
      ],
      "estimated_calories": 350
    }},
    "secondary_fields": {{
      "completed_at": "2025-10-05T18:30:00Z",
      "volume_load": null,
      "muscle_groups": ["legs"],
      "rpe": 8,
      "mood": null,
      "tags": ["legs", "lower-body", "after-work", "high-effort"]
    }},
    "estimated": true,
    "needs_clarification": true
  }},
  "validation": {{
    "errors": [],
    "warnings": ["Only squats mentioned - other exercises unknown", "Sets/reps/weight not specified"],
    "missing_critical": ["exercise_details", "other_exercises"]
  }},
  "suggestions": [
    "Time: 5:30 PM (after work) ✓",
    "Squats noted (felt heavy) ✓",
    "RPE: 8 (inferred from 'felt heavy')",
    "Add details: 'leg day: squats 225x5x4, RDL 185x8x3, leg press 450x12x3'"
  ]
}}

ACTIVITY EXAMPLES:

INPUT: "i ran 4 miles this morning at 8:30 pace"  (has distance and pace)
OUTPUT:
{{
  "type": "activity",
  "confidence": 0.9,
  "data": {{
    "primary_fields": {{
      "activity_name": "Morning Run",
      "activity_type": "running",
      "start_date": "2025-10-06T07:00:00Z",
      "distance_miles": 4,
      "distance_km": 6.44,
      "duration_minutes": 34,
      "pace": "8:30/mile (5:17/km)",
      "calories_burned": 400
    }},
    "secondary_fields": {{
      "rpe": null,
      "mood": null,
      "tags": ["cardio", "running", "morning"]
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
    "Great pace! 8:30/mile",
    "Duration calculated from distance and pace",
    "Add RPE (1-10) for effort tracking"
  ]
}}

INPUT: "ran 5 miles in 40 minutes"  (specific data)
OUTPUT:
{{
  "type": "activity",
  "confidence": 0.9,
  "data": {{
    "primary_fields": {{
      "activity_name": "Run",
      "activity_type": "running",
      "start_date": "2025-10-05T14:30:00Z",
      "distance_miles": 5,
      "distance_km": 8.05,
      "duration_minutes": 40,
      "pace": "8:00/mile (4:58/km)",
      "calories_burned": 550
    }},
    "secondary_fields": {{
      "rpe": 6,
      "mood": "good",
      "tags": ["cardio", "running"]
    }},
    "estimated": true,
    "needs_clarification": false
  }},
  "validation": {{
    "errors": [],
    "warnings": ["Time assumed to be current - specify if different"],
    "missing_critical": []
  }},
  "suggestions": [
    "Great pace! 8:00/mile",
    "Add RPE (1-10) for effort tracking"
  ]
}}

INPUT: "went for a run this morning"  (VAGUE - only estimate what's reasonable)
OUTPUT:
{{
  "type": "activity",
  "confidence": 0.5,
  "data": {{
    "primary_fields": {{
      "activity_name": "Morning Run",
      "activity_type": "running",
      "start_date": "2025-10-05T07:00:00Z",
      "duration_minutes": 35,
      "calories_burned": 350
    }},
    "secondary_fields": {{
      "distance_km": null,
      "distance_miles": null,
      "pace": null,
      "rpe": null,
      "mood": null,
      "tags": ["cardio", "running", "morning", "duration-estimated"]
    }},
    "estimated": true,
    "needs_clarification": true
  }},
  "validation": {{
    "errors": [],
    "warnings": ["Duration estimated as typical morning run (~35min)", "Distance not specified - too variable to estimate"],
    "missing_critical": ["distance", "pace"]
  }},
  "suggestions": [
    "Duration estimated ~35min (typical morning run)",
    "Calories estimated ~350 based on duration",
    "Add distance for better tracking: 'ran 5km' or 'ran for 3 miles'"
  ]
}}

INPUT: "easy 10k after work"  (has distance, infer duration)
OUTPUT:
{{
  "type": "activity",
  "confidence": 0.7,
  "data": {{
    "primary_fields": {{
      "activity_name": "Easy 10k Run",
      "activity_type": "running",
      "start_date": "2025-10-05T17:30:00Z",
      "distance_km": 10,
      "distance_miles": 6.2,
      "duration_minutes": 65,
      "calories_burned": 750
    }},
    "secondary_fields": {{
      "pace": "6:30/km (10:29/mile)",
      "rpe": 4,
      "mood": null,
      "tags": ["cardio", "running", "easy-pace", "evening"]
    }},
    "estimated": true,
    "needs_clarification": true
  }},
  "validation": {{
    "errors": [],
    "warnings": ["Duration estimated based on 'easy' pace (~6:30/km)", "Pace calculated from estimated duration"],
    "missing_critical": ["exact_duration"]
  }},
  "suggestions": [
    "Distance: 10km (specified) ✓",
    "Duration estimated ~65min for easy pace",
    "RPE inferred as 4 from 'easy'",
    "For exact pace, add actual time: 'easy 10k in 58 minutes'"
  ]
}}

CRITICAL RULES - NEVER SKIP:
1. **TIMESTAMPS ARE MANDATORY** - Every log MUST have a time
   - Meals: logged_at (infer from meal_type or context)
   - Activities: start_date
   - Workouts: started_at (and completed_at if duration estimated)
   - Measurements: measured_at
   - Use time inference rules (breakfast→7:30am, lunch→12:30pm, "morning"→7am, etc)
   - If NO context, use current time

2. **ESTIMATE ONLY WHAT'S REASONABLE**:
   - ✅ Timestamps, meal portions for named foods, typical durations, calories from duration
   - ⚠️ Only estimate duration/RPE if context supports it
   - ❌ NEVER make up: distances, paces, exercises not mentioned, sets/reps/weights, foods not mentioned

3. **STRUCTURE**:
   - primary_fields = show by default (most important data)
   - secondary_fields = show in "More details" section (extra context)
   - Use null for unknowable fields (distance, pace, specific exercises, etc.)

4. **CONFIDENCE & GUIDANCE**:
   - Set confidence honestly based on what user provided
   - Set needs_clarification=true if critical data missing
   - Provide actionable suggestions for what to add next time
""".format(classification_instruction=classification_instruction)

        # Build user prompt with historical pattern if available
        if historical_pattern and historical_pattern.get('sample_size', 0) >= 3:
            pattern_context = f"""
**HISTORICAL PATTERN DETECTED** ({historical_pattern['sample_size']} similar past logs):
You can use this user's typical behavior to make SMARTER estimates:
"""
            if historical_pattern['type'] == 'activity':
                if historical_pattern.get('duration_avg'):
                    pattern_context += f"\n- Typical duration: {historical_pattern['duration_avg']:.0f} minutes"
                if historical_pattern.get('distance_avg'):
                    pattern_context += f"\n- Typical distance: {historical_pattern['distance_avg']:.1f} km"
                if historical_pattern.get('calories_avg'):
                    pattern_context += f"\n- Typical calories: {historical_pattern['calories_avg']:.0f}"
                pattern_context += f"\n- Pattern confidence: {historical_pattern['confidence']:.2f}"
                pattern_context += f"\n\nUse these values for estimation! User is consistent ({historical_pattern['sample_size']} similar logs)."

            elif historical_pattern['type'] == 'workout':
                if historical_pattern.get('duration_avg'):
                    pattern_context += f"\n- Typical duration: {historical_pattern['duration_avg']:.0f} minutes"
                if historical_pattern.get('common_exercises'):
                    pattern_context += f"\n- Common exercises: {', '.join(historical_pattern['common_exercises'])}"
                pattern_context += f"\n- Pattern confidence: {historical_pattern['confidence']:.2f}"
                pattern_context += "\n\nUse these patterns for estimation! User typically does these exercises."

            elif historical_pattern['type'] == 'meal':
                if historical_pattern.get('calories_avg'):
                    pattern_context += f"\n- Typical calories: {historical_pattern['calories_avg']:.0f}"
                if historical_pattern.get('protein_avg'):
                    pattern_context += f"\n- Typical protein: {historical_pattern['protein_avg']:.0f}g"
                pattern_context += f"\n- Pattern confidence: {historical_pattern['confidence']:.2f}"
                pattern_context += "\n\nUse these values! User typically eats this portion for this meal."

            user_prompt = f"""{pattern_context}

Extract fitness data from this entry:
"{text}"

Return structured JSON using historical patterns above for smarter estimates."""
        else:
            user_prompt = f"""Extract fitness data from this entry:

"{text}"

Return structured JSON with primary_fields (show by default) and secondary_fields (expandable)."""

        try:
            logger.info(f"[GroqV2] Calling Groq API with text: '{text[:100]}...'")

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

            logger.info("[GroqV2] Received response, parsing JSON...")
            raw_content = response.choices[0].message.content
            logger.info(f"[GroqV2] Raw response: {raw_content[:500] if raw_content else 'EMPTY'}")

            # Handle empty or malformed response
            if not raw_content or not raw_content.strip():
                logger.error("[GroqV2] Empty response from Groq API")
                raise ValueError("Empty response from Groq API")

            # Try to parse JSON, with better error handling
            try:
                result = json.loads(raw_content)
            except json.JSONDecodeError as json_err:
                logger.error(f"[GroqV2] ❌ JSON parse error: {json_err}")
                logger.error(f"[GroqV2] ❌ Error position: line {json_err.lineno}, column {json_err.colno}")
                logger.error(f"[GroqV2] ❌ Problematic JSON (full):\n{raw_content}")

                # Try to extract JSON from markdown code blocks if present
                if "```json" in raw_content or "```" in raw_content:
                    logger.info("[GroqV2] 🔧 Attempting to extract JSON from markdown...")
                    json_start = raw_content.find("```json")
                    if json_start != -1:
                        json_start += 7
                    else:
                        json_start = raw_content.find("```") + 3

                    json_end = raw_content.find("```", json_start)
                    if json_end != -1:
                        raw_content = raw_content[json_start:json_end].strip()
                        logger.info(f"[GroqV2] 🔧 Extracted JSON: {raw_content[:200]}...")
                        result = json.loads(raw_content)
                    else:
                        logger.error("[GroqV2] ❌ Could not find closing ``` in markdown")
                        raise
                else:
                    logger.error("[GroqV2] ❌ Not markdown format, raising original error")
                    raise

            # Override type if forced
            if force_type:
                result['type'] = force_type
                result['confidence'] = 1.0

            logger.info(f"[GroqV2] ✅ Classified: {result.get('type')} (confidence: {result.get('confidence', 0):.2f})")
            return result

        except json.JSONDecodeError as e:
            logger.error(f"[GroqV2] ❌ JSON parsing failed: {e}")
            logger.error(f"[GroqV2] Raw response was: {raw_content if 'raw_content' in locals() else 'No response'}")
            error_msg = f"AI response parsing failed: {str(e)}"
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
                    "errors": [error_msg],
                    "warnings": [],
                    "missing_critical": ["all_data"]
                },
                "suggestions": [
                    f"⚠️ System Error: {error_msg}",
                    "Try again or contact support"
                ]
            }
        except Exception as e:
            logger.error(f"[GroqV2] ❌ API call failed: {type(e).__name__}: {e}")
            import traceback
            logger.error(f"[GroqV2] Traceback: {traceback.format_exc()}")

            # Show the actual error to help debug
            error_msg = f"{type(e).__name__}: {str(e)}"

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
                    "errors": [error_msg],
                    "warnings": [],
                    "missing_critical": ["all_data"]
                },
                "suggestions": [
                    f"⚠️ API Error: {error_msg}",
                    "Check backend logs for details",
                    "Verify Groq API key is set in environment"
                ]
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
            logger.info("[GroqV2] ✅ Image analyzed")
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
                logger.info("[GroqV2] ✅ Audio transcribed")
                return transcription

            finally:
                if os.path.exists(temp_audio_path):
                    os.remove(temp_audio_path)

        except Exception as e:
            logger.error(f"[GroqV2] ❌ Audio transcription failed: {e}")
            return "Failed to transcribe audio"

    async def generate_meal_title(
        self,
        description: str,
        foods: List[str],
        meal_type: str
    ) -> str:
        """
        Generate a concise meal title from description and foods.

        Converts long descriptions like "I had 3 eggs, 2 slices of toast with butter,
        and a banana for breakfast" into concise titles like "Eggs, toast, and banana".

        Args:
            description: Natural language meal description
            foods: List of food names
            meal_type: Type of meal (breakfast, lunch, dinner, snack)

        Returns:
            Concise meal title (max 50 characters)
        """
        logger.info(f"[GroqV2] Generating meal title from: '{description[:100]}...'")

        prompt = f"""Generate a short, concise meal title from this description:

Description: "{description}"
Foods: {foods}
Meal type: {meal_type}

RULES:
1. Create a title that's 3-6 words maximum
2. Focus on the main foods, not preparation details
3. Use natural language, not a list
4. Don't include meal type (breakfast/lunch/dinner) unless relevant
5. Don't include quantities or portions

EXAMPLES:

Input: "I had 3 eggs, 2 slices of toast with butter for breakfast"
Foods: ["eggs", "toast", "butter"]
Output: Eggs and toast with butter

Input: "ate 6oz grilled chicken breast with 1 cup brown rice and broccoli for lunch"
Foods: ["chicken breast", "brown rice", "broccoli"]
Output: Chicken, rice, and broccoli

Input: "had a protein shake with banana and oatmeal after my workout"
Foods: ["protein shake", "banana", "oatmeal"]
Output: Protein shake with banana

Input: "dinner was salmon with sweet potato and green beans"
Foods: ["salmon", "sweet potato", "green beans"]
Output: Salmon with sweet potato

Input: "snacked on an apple and peanut butter"
Foods: ["apple", "peanut butter"]
Output: Apple with peanut butter

Input: "Chicken Margherita at Olive Garden"
Foods: ["chicken margherita"]
Output: Chicken Margherita

Input: "big mac meal with fries and coke"
Foods: ["big mac", "fries", "coke"]
Output: Big Mac meal

Return ONLY the title, NO explanation or extra text."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=50
            )

            title = response.choices[0].message.content.strip()

            # Remove any quotes or extra formatting
            title = title.strip('"').strip("'").strip()

            # Truncate if too long
            if len(title) > 50:
                title = title[:47] + "..."

            logger.info(f"[GroqV2] ✅ Generated title: '{title}'")
            return title

        except Exception as e:
            logger.error(f"[GroqV2] ❌ Title generation failed: {e}")
            # Fallback: create simple title from foods
            if len(foods) == 1:
                return foods[0].capitalize()
            elif len(foods) == 2:
                return f"{foods[0].capitalize()} and {foods[1]}"
            elif len(foods) >= 3:
                return f"{foods[0].capitalize()}, {foods[1]}, and more"
            else:
                return meal_type.capitalize()

    async def extract_food_quantities(
        self,
        description: str,
        food_names: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Extract food quantities and units from a description.

        This is critical for accurate macro calculation - we need to parse
        "1.5 cup of oatmeal, 2 scoops of whey, 15g of maple syrup"
        into structured data with correct quantities/units.

        Args:
            description: Natural language description of the meal
            food_names: List of detected food names to match against

        Returns:
            List of dicts with {food, quantity, unit} for each food
        """
        logger.info(f"[GroqV2] Extracting quantities from: '{description}'")
        logger.info(f"[GroqV2] Expected foods: {food_names}")

        prompt = f"""Extract food quantities from this meal description:

"{description}"

Expected foods: {food_names}

Parse each food and extract:
- food: The food name (match to expected foods list)
- quantity: The numeric amount (e.g., 1.5, 2, 15)
- unit: The unit (cup, scoop, g, kg, oz, lb, tbsp, tsp, piece, serving, etc.)

RULES:
1. Match each food in the expected list to its quantity/unit in the description
2. If a food is mentioned but no quantity given, use quantity=1, unit="serving"
3. Keep units exactly as mentioned (don't convert - e.g., "cup" stays "cup", "g" stays "g")
4. For brand names or protein powder, "scoop" is typical unit
5. Don't add foods that aren't in the expected list

EXAMPLES:

Input: "1.5 cup of oatmeal, 2 scoops of whey isolate, 15g of maple syrup"
Expected: ["oatmeal", "whey isolate", "maple syrup"]
Output:
[
  {{"food": "oatmeal", "quantity": 1.5, "unit": "cup"}},
  {{"food": "whey isolate", "quantity": 2, "unit": "scoop"}},
  {{"food": "maple syrup", "quantity": 15, "unit": "g"}}
]

Input: "3 eggs, 2 slices of toast, 1 banana"
Expected: ["eggs", "toast", "banana"]
Output:
[
  {{"food": "eggs", "quantity": 3, "unit": "piece"}},
  {{"food": "toast", "quantity": 2, "unit": "slice"}},
  {{"food": "banana", "quantity": 1, "unit": "piece"}}
]

Input: "chicken breast and brown rice"
Expected: ["chicken breast", "brown rice"]
Output:
[
  {{"food": "chicken breast", "quantity": 1, "unit": "serving"}},
  {{"food": "brown rice", "quantity": 1, "unit": "serving"}}
]

Return ONLY valid JSON array with NO explanation or markdown."""

        try:
            response = self.client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                max_tokens=500,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            logger.info(f"[GroqV2] Raw response: {content}")

            # Parse JSON response
            result = json.loads(content)

            # Handle if response is wrapped in a key
            if "foods" in result:
                parsed_foods = result["foods"]
            elif "data" in result:
                parsed_foods = result["data"]
            elif isinstance(result, list):
                parsed_foods = result
            else:
                # Assume the first array value is our data
                parsed_foods = list(result.values())[0] if result else []

            logger.info(f"[GroqV2] ✅ Extracted {len(parsed_foods)} food quantities:")
            for food in parsed_foods:
                logger.info(f"   - {food.get('food')}: {food.get('quantity')} {food.get('unit')}")

            return parsed_foods

        except json.JSONDecodeError as e:
            logger.error(f"[GroqV2] ❌ JSON decode error: {e}")
            logger.error(f"[GroqV2] Raw content: {content}")
            # Fallback: return default servings
            return [{"food": name, "quantity": 1, "unit": "serving"} for name in food_names]

        except Exception as e:
            logger.error(f"[GroqV2] ❌ Quantity extraction failed: {e}")
            # Fallback: return default servings
            return [{"food": name, "quantity": 1, "unit": "serving"} for name in food_names]


# Global instance
_groq_service_v2: Optional[GroqServiceV2] = None


def get_groq_service_v2() -> GroqServiceV2:
    """Get the global GroqServiceV2 instance."""
    global _groq_service_v2
    if _groq_service_v2 is None:
        _groq_service_v2 = GroqServiceV2()
    return _groq_service_v2
