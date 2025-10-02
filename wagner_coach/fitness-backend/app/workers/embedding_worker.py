"""
Embedding Worker - Background Processing for Multimodal Embeddings

Celery tasks for generating embeddings for all user data:
- Meals & nutrition logs
- Workouts & activities
- Goals & preferences
- Voice notes & images
- Backfill for existing data
"""

import logging
from typing import Dict, Any, Optional
from datetime import datetime
from celery import shared_task

from app.services.multimodal_embedding_service import get_multimodal_service
from app.services.supabase_service import get_service_client

logger = logging.getLogger(__name__)


# ============================================================================
# MEAL EMBEDDINGS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def embed_meal_log(self, meal_log_id: str):
    """
    Generate embedding for a meal log.

    Args:
        meal_log_id: UUID of meal_logs record
    """
    try:
        service = get_multimodal_service()
        supabase = get_service_client()

        # Fetch meal data
        response = supabase.table("meal_logs").select(
            "*, meal_log_foods(*, foods(*))"
        ).eq("id", meal_log_id).single().execute()

        meal = response.data

        # Format text for embedding
        foods_list = [
            f"{f['foods']['name']} ({f['quantity']}{f['unit']})"
            for f in meal.get('meal_log_foods', [])
        ]
        foods_text = ", ".join(foods_list) if foods_list else "No foods logged"

        content_text = (
            f"Meal Type: {meal['category']}\n"
            f"Foods: {foods_text}\n"
            f"Nutrition: {meal['total_calories']} calories, "
            f"{meal['total_protein_g']}g protein, "
            f"{meal['total_carbs_g']}g carbs, "
            f"{meal['total_fat_g']}g fat\n"
            f"Logged at: {meal['logged_at']}\n"
        )

        if meal.get('notes'):
            content_text += f"Notes: {meal['notes']}"

        # Generate embedding
        embedding = await service.embed_text(content_text)

        # Store embedding
        await service.store_embedding(
            user_id=meal['user_id'],
            embedding=embedding,
            data_type='text',
            source_type='meal_log',
            source_id=meal_log_id,
            content_text=content_text,
            metadata={
                'category': meal['category'],
                'calories': float(meal['total_calories']) if meal['total_calories'] else None,
                'protein_g': float(meal['total_protein_g']) if meal['total_protein_g'] else None,
                'logged_at': meal['logged_at'],
                'foods_count': len(meal.get('meal_log_foods', []))
            },
            confidence_score=1.0
        )

        logger.info(f"✅ Embedded meal log: {meal_log_id}")
        return {"status": "success", "meal_log_id": meal_log_id}

    except Exception as e:
        logger.error(f"❌ Failed to embed meal log {meal_log_id}: {e}")
        raise self.retry(exc=e, countdown=60)


# ============================================================================
# WORKOUT/ACTIVITY EMBEDDINGS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def embed_activity(self, activity_id: str):
    """
    Generate embedding for an activity/workout.

    Args:
        activity_id: UUID of activities record
    """
    try:
        service = get_multimodal_service()
        supabase = get_service_client()

        # Fetch activity data
        response = supabase.table("activities").select("*").eq(
            "id", activity_id
        ).single().execute()

        activity = response.data

        # Format text for embedding
        content_text = (
            f"Activity: {activity['name']}\n"
            f"Type: {activity['activity_type']}\n"
            f"Date: {activity['start_date']}\n"
        )

        if activity.get('distance_meters'):
            content_text += f"Distance: {activity['distance_meters']/1000:.2f} km\n"

        if activity.get('elapsed_time_seconds'):
            content_text += f"Duration: {activity['elapsed_time_seconds']//60} minutes\n"

        if activity.get('average_heartrate'):
            content_text += f"Avg Heart Rate: {activity['average_heartrate']} bpm\n"

        if activity.get('calories'):
            content_text += f"Calories: {activity['calories']}\n"

        if activity.get('notes'):
            content_text += f"Notes: {activity['notes']}\n"

        if activity.get('perceived_exertion'):
            content_text += f"RPE: {activity['perceived_exertion']}/10\n"

        # Generate embedding
        embedding = await service.embed_text(content_text)

        # Store embedding
        await service.store_embedding(
            user_id=activity['user_id'],
            embedding=embedding,
            data_type='text',
            source_type='activity',
            source_id=activity_id,
            content_text=content_text,
            metadata={
                'activity_type': activity['activity_type'],
                'sport_type': activity.get('sport_type'),
                'start_date': activity['start_date'],
                'distance_meters': activity.get('distance_meters'),
                'duration_seconds': activity.get('elapsed_time_seconds'),
                'calories': activity.get('calories'),
                'perceived_exertion': activity.get('perceived_exertion')
            },
            confidence_score=1.0
        )

        logger.info(f"✅ Embedded activity: {activity_id}")
        return {"status": "success", "activity_id": activity_id}

    except Exception as e:
        logger.error(f"❌ Failed to embed activity {activity_id}: {e}")
        raise self.retry(exc=e, countdown=60)


# ============================================================================
# GOAL EMBEDDINGS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def embed_user_goal(self, goal_id: str):
    """
    Generate embedding for a user goal.

    Args:
        goal_id: UUID of user_goals record
    """
    try:
        service = get_multimodal_service()
        supabase = get_service_client()

        # Fetch goal data
        response = supabase.table("user_goals").select("*").eq(
            "id", goal_id
        ).single().execute()

        goal = response.data

        # Format text for embedding
        content_text = (
            f"Goal Type: {goal['goal_type']}\n"
            f"Description: {goal['goal_description']}\n"
        )

        if goal.get('target_value'):
            content_text += f"Target: {goal['target_value']} {goal.get('target_unit', '')}\n"

        if goal.get('target_date'):
            content_text += f"Target Date: {goal['target_date']}\n"

        if goal.get('priority'):
            content_text += f"Priority: {goal['priority']}/5\n"

        if goal.get('progress_notes'):
            content_text += f"Progress Notes: {goal['progress_notes']}\n"

        # Generate embedding
        embedding = await service.embed_text(content_text)

        # Store embedding
        await service.store_embedding(
            user_id=goal['user_id'],
            embedding=embedding,
            data_type='text',
            source_type='user_goal',
            source_id=goal_id,
            content_text=content_text,
            metadata={
                'goal_type': goal['goal_type'],
                'status': goal.get('status'),
                'priority': goal.get('priority'),
                'target_date': goal.get('target_date'),
                'created_at': goal['created_at']
            },
            confidence_score=1.0
        )

        logger.info(f"✅ Embedded user goal: {goal_id}")
        return {"status": "success", "goal_id": goal_id}

    except Exception as e:
        logger.error(f"❌ Failed to embed user goal {goal_id}: {e}")
        raise self.retry(exc=e, countdown=60)


# ============================================================================
# PROFILE EMBEDDINGS
# ============================================================================

@shared_task(bind=True, max_retries=3)
def embed_user_profile(self, user_id: str):
    """
    Generate embedding for user profile.

    Args:
        user_id: UUID of user
    """
    try:
        service = get_multimodal_service()
        supabase = get_service_client()

        # Fetch profile data
        response = supabase.table("profiles").select("*").eq(
            "id", user_id
        ).single().execute()

        profile = response.data

        # Format text for embedding
        content_parts = []

        if profile.get('about_me'):
            content_parts.append(f"About: {profile['about_me']}")

        if profile.get('fitness_goals'):
            content_parts.append(f"Fitness Goals: {profile['fitness_goals']}")

        if profile.get('primary_goal'):
            content_parts.append(f"Primary Goal: {profile['primary_goal']}")

        if profile.get('focus_areas'):
            content_parts.append(f"Focus Areas: {', '.join(profile['focus_areas'])}")

        if profile.get('preferred_activities'):
            content_parts.append(f"Preferred Activities: {', '.join(profile['preferred_activities'])}")

        if profile.get('physical_limitations'):
            content_parts.append(f"Physical Limitations: {', '.join(profile['physical_limitations'])}")

        if profile.get('available_equipment'):
            content_parts.append(f"Available Equipment: {', '.join(profile['available_equipment'])}")

        content_text = "\n".join(content_parts)

        if not content_text:
            logger.info(f"⏭️ Skipping empty profile: {user_id}")
            return {"status": "skipped", "reason": "empty_profile"}

        # Generate embedding
        embedding = await service.embed_text(content_text)

        # Store embedding
        await service.store_embedding(
            user_id=user_id,
            embedding=embedding,
            data_type='text',
            source_type='user_profile',
            source_id=user_id,
            content_text=content_text,
            metadata={
                'experience_level': profile.get('experience_level'),
                'primary_goal': profile.get('primary_goal'),
                'training_frequency': profile.get('training_frequency'),
                'updated_at': profile['updated_at']
            },
            confidence_score=1.0
        )

        logger.info(f"✅ Embedded user profile: {user_id}")
        return {"status": "success", "user_id": user_id}

    except Exception as e:
        logger.error(f"❌ Failed to embed user profile {user_id}: {e}")
        raise self.retry(exc=e, countdown=60)


# ============================================================================
# BACKFILL EMBEDDINGS
# ============================================================================

@shared_task
def backfill_user_embeddings(user_id: str):
    """
    Backfill all embeddings for a user.

    Creates embeddings for:
    - All meal logs
    - All activities
    - All goals
    - User profile

    Args:
        user_id: UUID of user
    """
    try:
        supabase = get_service_client()
        results = {
            "meals": {"total": 0, "queued": 0},
            "activities": {"total": 0, "queued": 0},
            "goals": {"total": 0, "queued": 0},
            "profile": {"queued": 0}
        }

        logger.info(f"🔄 Starting backfill for user: {user_id}")

        # 1. Backfill meals
        meals = supabase.table("meal_logs").select("id").eq("user_id", user_id).execute()
        results["meals"]["total"] = len(meals.data)

        for meal in meals.data:
            # Check if embedding already exists
            existing = supabase.table("multimodal_embeddings").select("id").eq(
                "source_type", "meal_log"
            ).eq("source_id", meal["id"]).execute()

            if not existing.data:
                embed_meal_log.delay(meal["id"])
                results["meals"]["queued"] += 1

        # 2. Backfill activities
        activities = supabase.table("activities").select("id").eq("user_id", user_id).execute()
        results["activities"]["total"] = len(activities.data)

        for activity in activities.data:
            existing = supabase.table("multimodal_embeddings").select("id").eq(
                "source_type", "activity"
            ).eq("source_id", activity["id"]).execute()

            if not existing.data:
                embed_activity.delay(activity["id"])
                results["activities"]["queued"] += 1

        # 3. Backfill goals
        goals = supabase.table("user_goals").select("id").eq("user_id", user_id).execute()
        results["goals"]["total"] = len(goals.data)

        for goal in goals.data:
            existing = supabase.table("multimodal_embeddings").select("id").eq(
                "source_type", "user_goal"
            ).eq("source_id", goal["id"]).execute()

            if not existing.data:
                embed_user_goal.delay(goal["id"])
                results["goals"]["queued"] += 1

        # 4. Backfill profile
        existing_profile = supabase.table("multimodal_embeddings").select("id").eq(
            "source_type", "user_profile"
        ).eq("source_id", user_id).execute()

        if not existing_profile.data:
            embed_user_profile.delay(user_id)
            results["profile"]["queued"] = 1

        logger.info(f"✅ Backfill queued for user {user_id}: {results}")
        return results

    except Exception as e:
        logger.error(f"❌ Backfill failed for user {user_id}: {e}")
        raise


@shared_task
def backfill_all_users():
    """
    Backfill embeddings for ALL users.

    Run this once after deploying the multimodal system.
    """
    try:
        supabase = get_service_client()

        # Get all user IDs
        users = supabase.table("profiles").select("id").execute()

        total_users = len(users.data)
        logger.info(f"🚀 Starting global backfill for {total_users} users")

        for i, user in enumerate(users.data, 1):
            logger.info(f"📊 Backfilling user {i}/{total_users}")
            backfill_user_embeddings.delay(user["id"])

        logger.info(f"✅ Global backfill queued for {total_users} users")
        return {"total_users": total_users, "status": "queued"}

    except Exception as e:
        logger.error(f"❌ Global backfill failed: {e}")
        raise
