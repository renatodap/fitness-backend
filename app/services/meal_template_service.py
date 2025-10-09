"""
Meal Template Service

Handles CRUD operations for meal templates with support for:
- Recursive templates (templates containing other templates)
- Template usage tracking (use_count, last_used_at)
- Template favorites
- Creating meals from templates
"""

import logging
from typing import Optional, List, Dict, Any
from datetime import datetime

from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


class MealTemplateService:
    """Service for managing meal templates."""

    def __init__(self):
        """Initialize template service with Supabase client."""
        self.supabase = get_service_client()

    async def create_template(
        self,
        user_id: str,
        name: str,
        category: str,
        description: Optional[str] = None,
        tags: Optional[List[str]] = None,
        food_items: List[Dict[str, Any]] = None
    ) -> dict:
        """
        Create a new meal template.

        Args:
            user_id: User's UUID
            name: Template name
            category: Meal category (breakfast, lunch, dinner, snack)
            description: Optional description
            tags: Optional list of tags for categorization
            food_items: List of food/template items with structure:
                {
                    "item_type": "food" | "template",
                    "food_id": UUID (if item_type='food'),
                    "template_id": UUID (if item_type='template'),
                    "quantity": float,
                    "unit": string
                }

        Returns:
            Created template with calculated nutrition

        Raises:
            ValueError: If validation fails
            Exception: If database operation fails
        """
        try:
            # Validate input
            if not name or not name.strip():
                raise ValueError("Template name is required")

            if category not in ["breakfast", "lunch", "dinner", "snack", "pre_workout", "post_workout", "other"]:
                raise ValueError(f"Invalid category: {category}")

            if not food_items or len(food_items) == 0:
                raise ValueError("At least one food or template item is required")

            # Create template record
            template_data = {
                "user_id": user_id,
                "name": name.strip(),
                "category": category,
                "description": description.strip() if description else None,
                "tags": tags if tags else [],
                "is_favorite": False,
                "use_count": 0,
                "last_used_at": None,
                # Totals will be calculated by triggers
                "total_calories": 0,
                "total_protein_g": 0,
                "total_carbs_g": 0,
                "total_fat_g": 0,
                "total_fiber_g": 0
            }

            response = await self.supabase.table("meal_templates").insert(template_data).execute()

            if not response.data or len(response.data) == 0:
                raise Exception("Failed to create template")

            template = response.data[0]
            template_id = template["id"]

            # Add template items (foods or other templates)
            if food_items:
                template_items = []
                for idx, item in enumerate(food_items):
                    item_type = item.get("item_type", "food")

                    if item_type == "food":
                        if not item.get("food_id"):
                            raise ValueError(f"food_id required for item {idx}")

                        template_items.append({
                            "meal_template_id": template_id,
                            "item_type": "food",
                            "food_id": item["food_id"],
                            "child_template_id": None,
                            "quantity": item["quantity"],
                            "unit": item["unit"],
                            "order_index": idx
                        })

                    elif item_type == "template":
                        if not item.get("template_id") and not item.get("child_template_id"):
                            raise ValueError(f"template_id required for item {idx}")

                        # Check for circular references
                        child_template_id = item.get("template_id") or item.get("child_template_id")
                        await self._check_circular_reference(template_id, child_template_id)

                        template_items.append({
                            "meal_template_id": template_id,
                            "item_type": "template",
                            "food_id": None,
                            "child_template_id": child_template_id,
                            "quantity": item["quantity"],
                            "unit": item["unit"],
                            "order_index": idx
                        })
                    else:
                        raise ValueError(f"Invalid item_type: {item_type}")

                # Insert all template items
                items_response = await self.supabase.table("meal_template_foods").insert(template_items).execute()

                if not items_response.data:
                    raise Exception("Failed to add items to template")

            # Fetch complete template with calculated nutrition
            return await self.get_template_by_id(template_id, user_id)

        except ValueError as e:
            logger.warning(f"Template validation error: {e}")
            raise
        except Exception as e:
            logger.error(f"Failed to create template: {e}", exc_info=True)
            raise Exception(f"Failed to create template: {str(e)}")

    async def get_template_by_id(
        self,
        template_id: str,
        user_id: str
    ) -> dict:
        """
        Get template by ID with all items and nutrition.

        Args:
            template_id: Template UUID
            user_id: User UUID (for security)

        Returns:
            Template with items and calculated nutrition

        Raises:
            ValueError: If template not found or unauthorized
        """
        try:
            response = await self.supabase.table("meal_templates").select(
                "*, items:meal_template_foods(*, food:foods_enhanced(*))"
            ).eq("id", template_id).eq("user_id", user_id).execute()

            if not response.data or len(response.data) == 0:
                raise ValueError(f"Template {template_id} not found")

            return response.data[0]

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to fetch template: {e}", exc_info=True)
            raise Exception(f"Failed to fetch template: {str(e)}")

    async def get_user_templates(
        self,
        user_id: str,
        category: Optional[str] = None,
        favorites_only: bool = False,
        tags: Optional[List[str]] = None,
        limit: int = 50,
        offset: int = 0
    ) -> dict:
        """
        Get user's templates with filtering.

        Args:
            user_id: User UUID
            category: Optional category filter
            favorites_only: Only return favorited templates
            tags: Optional tag filter (any match)
            limit: Max results
            offset: Pagination offset

        Returns:
            Dict with templates list and pagination info
        """
        try:
            # Build query
            query = self.supabase.table("meal_templates").select(
                "*, items:meal_template_foods(count)",
                count="exact"
            ).eq("user_id", user_id)

            # Apply filters
            if category:
                query = query.eq("category", category)

            if favorites_only:
                query = query.eq("is_favorite", True)

            if tags and len(tags) > 0:
                # Filter by any matching tag (contains operator)
                query = query.contains("tags", tags)

            # Order and paginate
            query = query.order("last_used_at", desc=True, nullslast=True).order("created_at", desc=True).limit(limit).offset(offset)

            response = await query.execute()

            return {
                "templates": response.data or [],
                "total": response.count or 0,
                "limit": limit,
                "offset": offset
            }

        except Exception as e:
            logger.error(f"Failed to fetch templates: {e}", exc_info=True)
            raise Exception(f"Failed to fetch templates: {str(e)}")

    async def update_template(
        self,
        template_id: str,
        user_id: str,
        updates: dict
    ) -> dict:
        """
        Update template fields.

        Args:
            template_id: Template UUID
            user_id: User UUID (for security)
            updates: Dict of fields to update

        Returns:
            Updated template

        Raises:
            ValueError: If template not found or validation fails
        """
        try:
            # Verify template exists and belongs to user
            existing = await self.get_template_by_id(template_id, user_id)

            # Build update dict (only allowed fields)
            allowed_fields = ["name", "description", "category", "tags", "is_favorite"]
            update_data = {}

            for field in allowed_fields:
                if field in updates:
                    update_data[field] = updates[field]

            if not update_data:
                raise ValueError("No valid fields to update")

            # Update template
            response = await self.supabase.table("meal_templates").update(update_data).eq("id", template_id).eq("user_id", user_id).execute()

            if not response.data:
                raise ValueError(f"Template {template_id} not found")

            return await self.get_template_by_id(template_id, user_id)

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to update template: {e}", exc_info=True)
            raise Exception(f"Failed to update template: {str(e)}")

    async def delete_template(
        self,
        template_id: str,
        user_id: str
    ) -> None:
        """
        Delete a template.

        Args:
            template_id: Template UUID
            user_id: User UUID (for security)

        Raises:
            ValueError: If template not found
        """
        try:
            # Verify template exists
            await self.get_template_by_id(template_id, user_id)

            # Delete template (CASCADE will delete template_foods)
            response = await self.supabase.table("meal_templates").delete().eq("id", template_id).eq("user_id", user_id).execute()

            if not response.data:
                raise ValueError(f"Template {template_id} not found")

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to delete template: {e}", exc_info=True)
            raise Exception(f"Failed to delete template: {str(e)}")

    async def create_meal_from_template(
        self,
        template_id: str,
        user_id: str,
        logged_at: Optional[str] = None,
        notes: Optional[str] = None
    ) -> dict:
        """
        Create a meal log from a template.

        Uses database function to properly flatten recursive templates.

        Args:
            template_id: Template UUID
            user_id: User UUID
            logged_at: Optional timestamp (defaults to now)
            notes: Optional notes for the meal

        Returns:
            Created meal log

        Raises:
            ValueError: If template not found
        """
        try:
            # Call database function to create meal from template
            response = await self.supabase.rpc(
                "create_meal_from_template",
                {
                    "p_user_id": user_id,
                    "p_template_id": template_id,
                    "p_logged_at": logged_at or datetime.utcnow().isoformat(),
                    "p_notes": notes
                }
            ).execute()

            if not response.data or len(response.data) == 0:
                raise ValueError(f"Failed to create meal from template {template_id}")

            meal_id = response.data[0]["meal_id"]

            # Update template usage stats
            await self._increment_template_usage(template_id)

            # Fetch created meal
            meal_response = await self.supabase.table("meal_logs").select(
                "*, foods:meal_foods(*, food:foods_enhanced(*))"
            ).eq("id", meal_id).execute()

            if not meal_response.data:
                raise ValueError("Failed to fetch created meal")

            return meal_response.data[0]

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to create meal from template: {e}", exc_info=True)
            raise Exception(f"Failed to create meal from template: {str(e)}")

    async def _check_circular_reference(
        self,
        parent_template_id: str,
        child_template_id: str
    ) -> None:
        """
        Check for circular template references.

        Args:
            parent_template_id: Parent template UUID
            child_template_id: Child template UUID

        Raises:
            ValueError: If circular reference detected
        """
        try:
            response = await self.supabase.rpc(
                "check_template_circular_reference",
                {
                    "p_parent_template_id": parent_template_id,
                    "p_child_template_id": child_template_id
                }
            ).execute()

            if response.data and len(response.data) > 0 and response.data[0].get("has_circular_reference"):
                raise ValueError(f"Circular reference detected: template {child_template_id} cannot contain template {parent_template_id}")

        except ValueError:
            raise
        except Exception as e:
            logger.error(f"Failed to check circular reference: {e}", exc_info=True)
            # Don't fail the entire operation on this check
            pass

    async def _increment_template_usage(
        self,
        template_id: str
    ) -> None:
        """
        Increment template usage count and update last_used_at.

        Args:
            template_id: Template UUID
        """
        try:
            await self.supabase.table("meal_templates").update({
                "use_count": self.supabase.rpc("increment", {"col": "use_count"}),
                "last_used_at": datetime.utcnow().isoformat()
            }).eq("id", template_id).execute()

        except Exception as e:
            logger.error(f"Failed to increment template usage: {e}", exc_info=True)
            # Don't fail the entire operation on this
            pass


# Singleton instance
_template_service = None


def get_meal_template_service() -> MealTemplateService:
    """Get or create singleton template service instance."""
    global _template_service
    if _template_service is None:
        _template_service = MealTemplateService()
    return _template_service
