"""
Calorie and Macro Calculation Service

Calculates BMR, TDEE, and macronutrient targets based on user metrics and goals.

Uses evidence-based formulas:
- BMR: Mifflin-St Jeor equation
- TDEE: BMR × activity multiplier
- Macros: Goal-specific protein/carb/fat ratios
"""

import logging
from typing import Dict, Optional
from enum import Enum

logger = logging.getLogger(__name__)


class ActivityLevel(str, Enum):
    """Activity level categories with corresponding multipliers."""
    SEDENTARY = "sedentary"  # 1.2 - Little to no exercise
    LIGHTLY_ACTIVE = "lightly_active"  # 1.375 - Light exercise 1-3 days/week
    MODERATELY_ACTIVE = "moderately_active"  # 1.55 - Moderate exercise 3-5 days/week
    VERY_ACTIVE = "very_active"  # 1.725 - Heavy exercise 6-7 days/week
    EXTREMELY_ACTIVE = "extremely_active"  # 1.9 - Very heavy exercise, physical job


class GoalType(str, Enum):
    """Goal types for macro calculations."""
    CUT = "cut"
    LOSE_FAT = "lose_fat"
    FAT_LOSS = "fat_loss"
    BULK = "bulk"
    BUILD_MUSCLE = "build_muscle"
    MUSCLE_GAIN = "muscle_gain"
    MAINTAIN = "maintain"
    MAINTENANCE = "maintenance"
    RECOMP = "recomp"
    PERFORMANCE = "performance"


class CalorieCalculationService:
    """Service for calculating calorie and macronutrient targets."""

    # Activity multipliers for TDEE calculation
    ACTIVITY_MULTIPLIERS = {
        ActivityLevel.SEDENTARY: 1.2,
        ActivityLevel.LIGHTLY_ACTIVE: 1.375,
        ActivityLevel.MODERATELY_ACTIVE: 1.55,
        ActivityLevel.VERY_ACTIVE: 1.725,
        ActivityLevel.EXTREMELY_ACTIVE: 1.9,
    }

    def calculate_bmr(
        self,
        weight_kg: float,
        height_cm: float,
        age: int,
        biological_sex: str
    ) -> int:
        """
        Calculate Basal Metabolic Rate (BMR) using Mifflin-St Jeor equation.

        This is the most accurate BMR formula for modern populations.

        Formula:
        - Men: (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) + 5
        - Women: (10 × weight in kg) + (6.25 × height in cm) - (5 × age in years) - 161

        Args:
            weight_kg: Body weight in kilograms
            height_cm: Height in centimeters
            age: Age in years
            biological_sex: 'male' or 'female'

        Returns:
            BMR in calories per day (integer)

        Raises:
            ValueError: If inputs are invalid
        """
        # Validation
        if weight_kg <= 0 or weight_kg > 500:
            raise ValueError(f"Invalid weight: {weight_kg}kg. Must be between 0 and 500kg.")
        if height_cm <= 0 or height_cm > 300:
            raise ValueError(f"Invalid height: {height_cm}cm. Must be between 0 and 300cm.")
        if age < 13 or age > 120:
            raise ValueError(f"Invalid age: {age}. Must be between 13 and 120.")
        if biological_sex.lower() not in ['male', 'female']:
            raise ValueError(f"Invalid biological_sex: {biological_sex}. Must be 'male' or 'female'.")

        # Calculate BMR
        if biological_sex.lower() == 'male':
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) + 5
        else:  # female
            bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age) - 161

        logger.info(
            f"Calculated BMR: {round(bmr)} cal/day "
            f"(weight={weight_kg}kg, height={height_cm}cm, age={age}, sex={biological_sex})"
        )

        return round(bmr)

    def determine_activity_level(
        self,
        activity_level: Optional[str] = None,
        training_frequency: Optional[int] = None
    ) -> ActivityLevel:
        """
        Determine activity level from either explicit level or training frequency.

        Args:
            activity_level: Explicit activity level string
            training_frequency: Training days per week (0-7)

        Returns:
            ActivityLevel enum value

        Raises:
            ValueError: If both inputs are None
        """
        if activity_level:
            # Map string to enum
            level_map = {
                'sedentary': ActivityLevel.SEDENTARY,
                'lightly_active': ActivityLevel.LIGHTLY_ACTIVE,
                'moderately_active': ActivityLevel.MODERATELY_ACTIVE,
                'very_active': ActivityLevel.VERY_ACTIVE,
                'extremely_active': ActivityLevel.EXTREMELY_ACTIVE,
            }
            return level_map.get(activity_level.lower(), ActivityLevel.MODERATELY_ACTIVE)

        elif training_frequency is not None:
            # Infer from training frequency
            if training_frequency >= 6:
                return ActivityLevel.VERY_ACTIVE
            elif training_frequency >= 4:
                return ActivityLevel.MODERATELY_ACTIVE
            elif training_frequency >= 2:
                return ActivityLevel.LIGHTLY_ACTIVE
            else:
                return ActivityLevel.SEDENTARY

        else:
            raise ValueError("Must provide either activity_level or training_frequency")

    def calculate_tdee(
        self,
        bmr: int,
        activity_level: Optional[str] = None,
        training_frequency: Optional[int] = None
    ) -> int:
        """
        Calculate Total Daily Energy Expenditure (TDEE).

        TDEE = BMR × activity multiplier

        Args:
            bmr: Basal Metabolic Rate (calories/day)
            activity_level: Activity level string (e.g., 'moderately_active')
            training_frequency: Training days per week (alternative to activity_level)

        Returns:
            TDEE in calories per day (integer)

        Raises:
            ValueError: If neither activity_level nor training_frequency provided
        """
        # Determine activity level
        activity_enum = self.determine_activity_level(activity_level, training_frequency)

        # Get multiplier
        multiplier = self.ACTIVITY_MULTIPLIERS[activity_enum]

        # Calculate TDEE
        tdee = bmr * multiplier

        logger.info(
            f"Calculated TDEE: {round(tdee)} cal/day "
            f"(BMR={bmr}, activity={activity_enum.value}, multiplier={multiplier})"
        )

        return round(tdee)

    def adjust_calories_for_goal(
        self,
        tdee: int,
        goal: str
    ) -> int:
        """
        Adjust TDEE based on goal (cut, bulk, maintain).

        Adjustments:
        - Cut/Fat Loss: -20% (0.8x TDEE)
        - Bulk/Muscle Gain: +10% (1.1x TDEE)
        - Maintain/Recomp: No change (1.0x TDEE)

        Args:
            tdee: Total Daily Energy Expenditure
            goal: Goal type string

        Returns:
            Adjusted daily calorie target (integer)
        """
        goal_lower = goal.lower()

        if goal_lower in [GoalType.CUT.value, GoalType.LOSE_FAT.value, GoalType.FAT_LOSS.value]:
            # 20% deficit for fat loss
            adjusted = round(tdee * 0.8)
            logger.info(f"Cut goal: {tdee} → {adjusted} (-20%)")
            return adjusted

        elif goal_lower in [GoalType.BULK.value, GoalType.BUILD_MUSCLE.value, GoalType.MUSCLE_GAIN.value]:
            # 10% surplus for muscle gain
            adjusted = round(tdee * 1.1)
            logger.info(f"Bulk goal: {tdee} → {adjusted} (+10%)")
            return adjusted

        elif goal_lower in [GoalType.MAINTAIN.value, GoalType.MAINTENANCE.value, GoalType.RECOMP.value]:
            # No change for maintenance
            logger.info(f"Maintenance goal: {tdee} (no change)")
            return tdee

        else:
            # Default to maintenance for unknown goals
            logger.warning(f"Unknown goal '{goal}', defaulting to maintenance")
            return tdee

    def calculate_protein_target(
        self,
        body_weight_kg: float,
        goal: str
    ) -> int:
        """
        Calculate daily protein target based on goal.

        Protein recommendations:
        - Cut/Fat Loss: 2.2 g/kg (high for muscle preservation)
        - Bulk/Muscle Gain: 2.0 g/kg (high for muscle building)
        - Maintain/Recomp: 1.8 g/kg (moderate-high)
        - General: 1.6 g/kg (minimum for active individuals)

        Args:
            body_weight_kg: Body weight in kilograms
            goal: Goal type string

        Returns:
            Daily protein target in grams (integer)
        """
        goal_lower = goal.lower()

        if goal_lower in [GoalType.CUT.value, GoalType.LOSE_FAT.value, GoalType.FAT_LOSS.value]:
            protein_per_kg = 2.2
        elif goal_lower in [GoalType.BULK.value, GoalType.BUILD_MUSCLE.value, GoalType.MUSCLE_GAIN.value]:
            protein_per_kg = 2.0
        elif goal_lower in [GoalType.MAINTAIN.value, GoalType.MAINTENANCE.value, GoalType.RECOMP.value]:
            protein_per_kg = 1.8
        else:
            protein_per_kg = 1.6  # General fitness

        protein_g = round(body_weight_kg * protein_per_kg)

        logger.info(f"Protein target: {protein_g}g ({protein_per_kg}g/kg)")

        return protein_g

    def calculate_macros(
        self,
        daily_calories: int,
        body_weight_kg: float,
        goal: str
    ) -> Dict[str, int]:
        """
        Calculate macronutrient targets (protein, carbs, fats).

        Strategy:
        1. Set protein based on goal (see calculate_protein_target)
        2. Set fat at 25-30% of calories (0.28 average)
        3. Fill remaining calories with carbs

        Args:
            daily_calories: Daily calorie target
            body_weight_kg: Body weight in kilograms
            goal: Goal type string

        Returns:
            Dictionary with macro targets:
            {
                'daily_calories': int,
                'daily_protein_g': int,
                'daily_carbs_g': int,
                'daily_fat_g': int,
                'protein_percentage': int,
                'carbs_percentage': int,
                'fat_percentage': int
            }
        """
        # Calculate protein target
        protein_g = self.calculate_protein_target(body_weight_kg, goal)

        # Calculate fat (28% of calories, 9 cal/g)
        fat_calories = daily_calories * 0.28
        fat_g = round(fat_calories / 9)

        # Calculate carbs from remaining calories (4 cal/g)
        protein_calories = protein_g * 4  # 4 cal/g protein
        fat_calories_actual = fat_g * 9  # 9 cal/g fat
        remaining_calories = daily_calories - protein_calories - fat_calories_actual
        carbs_g = round(remaining_calories / 4)  # 4 cal/g carbs

        # Ensure non-negative carbs
        carbs_g = max(carbs_g, 0)

        # Calculate percentages
        protein_pct = round((protein_calories / daily_calories) * 100) if daily_calories > 0 else 0
        fat_pct = round((fat_g * 9 / daily_calories) * 100) if daily_calories > 0 else 0
        carbs_pct = round((carbs_g * 4 / daily_calories) * 100) if daily_calories > 0 else 0

        macros = {
            'daily_calories': daily_calories,
            'daily_protein_g': protein_g,
            'daily_carbs_g': carbs_g,
            'daily_fat_g': fat_g,
            'protein_percentage': protein_pct,
            'carbs_percentage': carbs_pct,
            'fat_percentage': fat_pct
        }

        logger.info(
            f"Macros calculated: "
            f"Protein {protein_g}g ({protein_pct}%), "
            f"Carbs {carbs_g}g ({carbs_pct}%), "
            f"Fat {fat_g}g ({fat_pct}%)"
        )

        return macros

    def calculate_full_nutrition_plan(
        self,
        weight_kg: float,
        height_cm: float,
        age: int,
        biological_sex: str,
        goal: str,
        activity_level: Optional[str] = None,
        training_frequency: Optional[int] = None
    ) -> Dict[str, any]:
        """
        Calculate complete nutrition plan (BMR, TDEE, calories, macros).

        This is the main entry point for getting a full nutrition plan.

        Args:
            weight_kg: Body weight in kilograms
            height_cm: Height in centimeters
            age: Age in years
            biological_sex: 'male' or 'female'
            goal: Goal type (cut, bulk, maintain, etc.)
            activity_level: Activity level string (optional)
            training_frequency: Training days per week (optional)

        Returns:
            Complete nutrition plan dictionary:
            {
                'bmr': int,
                'tdee': int,
                'daily_calories': int,
                'daily_protein_g': int,
                'daily_carbs_g': int,
                'daily_fat_g': int,
                'protein_percentage': int,
                'carbs_percentage': int,
                'fat_percentage': int,
                'activity_level': str,
                'goal': str
            }

        Raises:
            ValueError: If inputs are invalid
        """
        # Step 1: Calculate BMR
        bmr = self.calculate_bmr(weight_kg, height_cm, age, biological_sex)

        # Step 2: Calculate TDEE
        tdee = self.calculate_tdee(bmr, activity_level, training_frequency)

        # Step 3: Adjust calories for goal
        daily_calories = self.adjust_calories_for_goal(tdee, goal)

        # Step 4: Calculate macros
        macros = self.calculate_macros(daily_calories, weight_kg, goal)

        # Step 5: Build complete plan
        activity_enum = self.determine_activity_level(activity_level, training_frequency)

        plan = {
            'bmr': bmr,
            'tdee': tdee,
            'activity_level': activity_enum.value,
            'activity_multiplier': self.ACTIVITY_MULTIPLIERS[activity_enum],
            'goal': goal,
            **macros
        }

        logger.info(f"Complete nutrition plan calculated: {plan}")

        return plan


# Global instance
_calorie_service: Optional[CalorieCalculationService] = None


def get_calorie_service() -> CalorieCalculationService:
    """Get the global CalorieCalculationService instance."""
    global _calorie_service
    if _calorie_service is None:
        _calorie_service = CalorieCalculationService()
    return _calorie_service
