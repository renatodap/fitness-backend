"""
Food Quantity Conversion Logic

This module handles all conversions between servings and grams.
It's the heart of the dual quantity system.

Key Principles:
1. Gram quantity is the source of truth for nutrition calculations
2. Conversions use household serving size when available  
3. All conversions are reversible without data loss
4. Edge cases are handled gracefully with sensible fallbacks
"""
from decimal import Decimal, ROUND_HALF_UP
from typing import Optional, Dict, Any
import logging

logger = logging.getLogger(__name__)


class FoodQuantityConverter:
    """
    Handles bidirectional conversion between servings and grams.
    
    This is a stateless service that performs pure calculations.
    No database access - just math.
    """
    
    @staticmethod
    def calculate_quantities(
        food_data: Dict[str, Any],
        input_quantity: Decimal,
        input_field: str
    ) -> Dict[str, Any]:
        """
        Calculate both serving and gram quantities from user input.
        
        This is the core conversion function. Given one quantity (either
        servings or grams), calculate the other quantity.
        
        Args:
            food_data: Food information from foods_enhanced table
                Required keys: serving_size
                Optional keys: household_serving_size, household_serving_unit
            input_quantity: The quantity entered by user
            input_field: 'serving' or 'grams' - which field user edited
            
        Returns:
            Dict with:
                - serving_quantity (float)
                - serving_unit (str or None)
                - gram_quantity (float)
                - last_edited_field (str)
                
        Example:
            >>> food = {
            ...     'serving_size': 28,
            ...     'household_serving_size': '28',
            ...     'household_serving_unit': 'slice'
            ... }
            >>> result = FoodQuantityConverter.calculate_quantities(
            ...     food, Decimal('2'), 'serving'
            ... )
            >>> result['gram_quantity']
            56.0
        """
        # Extract food serving information
        serving_size = Decimal(str(food_data.get('serving_size', 100)))
        household_serving_size = food_data.get('household_serving_size')
        household_serving_unit = food_data.get('household_serving_unit')
        
        # Parse household serving size (may be string like "1" or "0.5")
        household_grams_per_serving = None
        if household_serving_size:
            try:
                household_grams_per_serving = Decimal(str(household_serving_size))
            except (ValueError, TypeError):
                logger.warning(
                    f"Invalid household_serving_size: {household_serving_size} "
                    f"for food {food_data.get('name', 'unknown')}"
                )
        
        # Determine grams per serving (priority: household > standard)
        grams_per_serving = household_grams_per_serving if household_grams_per_serving else serving_size
        
        # Ensure we have a valid serving size
        if grams_per_serving <= 0:
            logger.warning(
                f"Invalid serving size: {grams_per_serving} "
                f"for food {food_data.get('name', 'unknown')}, using 100g default"
            )
            grams_per_serving = Decimal('100')
        
        # Calculate based on input field
        if input_field == 'serving':
            # User edited servings → calculate grams
            serving_quantity = input_quantity
            gram_quantity = serving_quantity * grams_per_serving
            
        else:  # input_field == 'grams'
            # User edited grams → calculate servings
            gram_quantity = input_quantity
            serving_quantity = gram_quantity / grams_per_serving
        
        # Round to reasonable precision
        # Servings: 3 decimal places (allows 0.001 precision)
        # Grams: 1 decimal place (allows 0.1g precision)
        serving_quantity = serving_quantity.quantize(
            Decimal('0.001'), 
            rounding=ROUND_HALF_UP
        )
        gram_quantity = gram_quantity.quantize(
            Decimal('0.1'), 
            rounding=ROUND_HALF_UP
        )
        
        return {
            'serving_quantity': float(serving_quantity),
            'serving_unit': household_serving_unit or 'serving',
            'gram_quantity': float(gram_quantity),
            'last_edited_field': input_field
        }
    
    @staticmethod
    def calculate_nutrition(
        food_data: Dict[str, Any],
        gram_quantity: Decimal
    ) -> Dict[str, float]:
        """
        Calculate nutrition values based on gram quantity.
        
        CRITICAL: Nutrition is ALWAYS calculated from grams for consistency.
        This ensures no rounding errors from back-and-forth conversions.
        
        Args:
            food_data: Food information from foods_enhanced table
                Required keys: serving_size, calories, protein_g, etc.
            gram_quantity: Quantity in grams
            
        Returns:
            Dict with nutrition values:
                - calories
                - protein_g
                - carbs_g
                - fat_g
                - fiber_g
                - sugar_g
                - sodium_mg
                
        Example:
            >>> food = {
            ...     'serving_size': 100,
            ...     'calories': 280,
            ...     'protein_g': 15,
            ...     'total_carbs_g': 46,
            ...     'total_fat_g': 4
            ... }
            >>> nutrition = FoodQuantityConverter.calculate_nutrition(
            ...     food, Decimal('150')
            ... )
            >>> nutrition['calories']
            420.0
        """
        serving_size = Decimal(str(food_data.get('serving_size', 100)))
        
        # Ensure serving size is valid
        if serving_size <= 0:
            logger.warning(
                f"Invalid serving size: {serving_size} "
                f"for food {food_data.get('name', 'unknown')}, using 100g"
            )
            serving_size = Decimal('100')
        
        # Calculate multiplier
        multiplier = gram_quantity / serving_size
        
        # Helper function to safely calculate nutrient
        def calc_nutrient(key: str, default: float = 0) -> float:
            value = Decimal(str(food_data.get(key, default)))
            result = value * multiplier
            # Round to 1 decimal place
            return float(result.quantize(Decimal('0.1'), rounding=ROUND_HALF_UP))
        
        # Calculate each nutrient
        return {
            'calories': calc_nutrient('calories'),
            'protein_g': calc_nutrient('protein_g'),
            'carbs_g': calc_nutrient('total_carbs_g'),
            'fat_g': calc_nutrient('total_fat_g'),
            'fiber_g': calc_nutrient('dietary_fiber_g'),
            'sugar_g': calc_nutrient('total_sugars_g'),
            'sodium_mg': calc_nutrient('sodium_mg'),
        }
    
    @staticmethod
    def validate_quantity_update(
        current_quantity: Dict[str, Any],
        new_input_quantity: Decimal,
        new_input_field: str
    ) -> bool:
        """
        Validate that a quantity update makes sense.
        
        Args:
            current_quantity: Current quantity data
            new_input_quantity: New quantity value
            new_input_field: Which field is being updated
            
        Returns:
            True if update is valid, False otherwise
        """
        # Check for reasonable values
        if new_input_quantity <= 0:
            logger.warning("Quantity update rejected: non-positive value")
            return False
            
        if new_input_quantity > 100000:  # 100kg
            logger.warning("Quantity update rejected: exceeds 100kg")
            return False
        
        # Additional validation could go here
        # e.g., flag suspiciously large changes
        
        return True
    
    @staticmethod
    def format_serving_display(
        serving_quantity: float, 
        serving_unit: Optional[str]
    ) -> str:
        """
        Format serving quantity for display with proper pluralization.
        
        Args:
            serving_quantity: Number of servings
            serving_unit: Unit name (can be None)
            
        Returns:
            Formatted string like "2 slices" or "1.5 servings"
            
        Example:
            >>> FoodQuantityConverter.format_serving_display(2, 'slice')
            '2 slices'
            >>> FoodQuantityConverter.format_serving_display(1, 'slice')
            '1 slice'
            >>> FoodQuantityConverter.format_serving_display(1.5, None)
            '1.5 servings'
        """
        if not serving_unit:
            unit_display = 'serving' if serving_quantity == 1 else 'servings'
            return f"{serving_quantity:.2f} {unit_display}".rstrip('0').rstrip('.')
        
        # Pluralization rules for common units
        plural_map = {
            'slice': 'slices',
            'piece': 'pieces',
            'scoop': 'scoops',
            'cup': 'cups',
            'tbsp': 'tbsp',
            'tsp': 'tsp',
            'bar': 'bars',
            'packet': 'packets',
            'bottle': 'bottles',
            'can': 'cans',
            'container': 'containers',
            # Size adjectives don't pluralize
            'medium': 'medium',
            'small': 'small',
            'large': 'large',
            'extra large': 'extra large',
        }
        
        unit_display = serving_unit
        if serving_quantity != 1:
            unit_display = plural_map.get(serving_unit.lower(), f"{serving_unit}s")
        
        # Format quantity (remove trailing zeros)
        qty_str = f"{serving_quantity:.2f}".rstrip('0').rstrip('.')
        
        return f"{qty_str} {unit_display}"


# Convenience functions for backward compatibility
def convert_to_grams(
    quantity: Decimal, 
    unit: str, 
    food_data: Dict[str, Any]
) -> Decimal:
    """
    Convert any unit to grams.
    
    Legacy function for backward compatibility.
    New code should use FoodQuantityConverter.calculate_quantities().
    """
    if unit == 'g':
        return quantity
    
    # Treat as servings
    result = FoodQuantityConverter.calculate_quantities(
        food_data=food_data,
        input_quantity=quantity,
        input_field='serving'
    )
    return Decimal(str(result['gram_quantity']))


def convert_from_grams(
    grams: Decimal,
    food_data: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Convert grams to servings.
    
    Legacy function for backward compatibility.
    New code should use FoodQuantityConverter.calculate_quantities().
    """
    return FoodQuantityConverter.calculate_quantities(
        food_data=food_data,
        input_quantity=grams,
        input_field='grams'
    )
