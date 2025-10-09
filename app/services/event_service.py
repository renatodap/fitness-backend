"""
Event Management Service

Handles user events (races, competitions, shows) and integrates with AI program generation
for event-specific periodization.

This service:
- Creates and manages user events
- Calculates countdowns and training phases
- Generates event-specific AI programs
- Integrates with daily recommendations

OPTIMIZED: Uses FREE models for event analysis and periodization planning
"""

import logging
from datetime import date, timedelta
from typing import List, Dict, Any, Optional
from uuid import UUID

from app.config import get_settings
from app.services.supabase_service import get_service_client
from app.services.dual_model_router import dual_router, TaskType, TaskConfig

settings = get_settings()
logger = logging.getLogger(__name__)


class EventService:
    """Service for managing user events and event-driven training."""

    # Periodization templates for different event types
    EVENT_PERIODIZATION_TEMPLATES = {
        'marathon': {
            'training_weeks': 16,
            'taper_weeks': 2,
            'peak_week_offset': -7,  # days before event
            'phases': [
                {'name': 'Base Building', 'weeks': 4, 'focus': 'Volume, easy pace'},
                {'name': 'Build Phase', 'weeks': 6, 'focus': 'Tempo runs, long runs'},
                {'name': 'Peak Phase', 'weeks': 4, 'focus': 'Race pace, peak mileage'},
                {'name': 'Taper', 'weeks': 2, 'focus': 'Reduced volume, race prep'}
            ],
            'nutrition_strategy': 'carb_loading_protocol'
        },
        'half_marathon': {
            'training_weeks': 12,
            'taper_weeks': 1,
            'peak_week_offset': -7,
            'phases': [
                {'name': 'Base', 'weeks': 4},
                {'name': 'Build', 'weeks': 5},
                {'name': 'Peak', 'weeks': 2},
                {'name': 'Taper', 'weeks': 1}
            ],
            'nutrition_strategy': 'carb_loading_24hr'
        },
        'powerlifting_meet': {
            'training_weeks': 12,
            'taper_weeks': 1,
            'peak_week_offset': -7,
            'phases': [
                {'name': 'Hypertrophy', 'weeks': 4, 'focus': '8-12 reps, volume'},
                {'name': 'Strength', 'weeks': 5, 'focus': '3-6 reps, intensity'},
                {'name': 'Peaking', 'weeks': 2, 'focus': '1-3 reps, specificity'},
                {'name': 'Deload/Taper', 'weeks': 1, 'focus': 'Reduced volume, CNS recovery'}
            ],
            'nutrition_strategy': 'water_cut_protocol'
        },
        'weightlifting_meet': {
            'training_weeks': 12,
            'taper_weeks': 1,
            'peak_week_offset': -7,
            'phases': [
                {'name': 'General Prep', 'weeks': 4},
                {'name': 'Specific Prep', 'weeks': 5},
                {'name': 'Competition Prep', 'weeks': 2},
                {'name': 'Taper', 'weeks': 1}
            ],
            'nutrition_strategy': 'weight_class_protocol'
        },
        'bodybuilding_show': {
            'training_weeks': 16,
            'taper_weeks': 1,
            'peak_week_offset': -7,
            'phases': [
                {'name': 'Mass Building', 'weeks': 8, 'focus': 'Calorie surplus, volume'},
                {'name': 'Cutting Phase', 'weeks': 6, 'focus': 'Calorie deficit, maintain strength'},
                {'name': 'Final Prep', 'weeks': 2, 'focus': 'Peak conditioning, carb depletion/load'}
            ],
            'nutrition_strategy': 'peak_week_protocol'
        },
        'triathlon': {
            'training_weeks': 20,
            'taper_weeks': 2,
            'peak_week_offset': -14,
            'phases': [
                {'name': 'Base', 'weeks': 8},
                {'name': 'Build', 'weeks': 8},
                {'name': 'Peak', 'weeks': 2},
                {'name': 'Taper', 'weeks': 2}
            ],
            'nutrition_strategy': 'endurance_fueling'
        }
    }

    def __init__(self):
        self.supabase = get_service_client()
        self.router = dual_router

    async def create_event(
        self,
        user_id: str,
        event_name: str,
        event_type: str,
        event_date: date,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Create a new user event.

        Args:
            user_id: User UUID
            event_name: Name of event ("Boston Marathon 2026")
            event_type: Type of event (marathon, powerlifting_meet, etc.)
            event_date: Date of event
            **kwargs: Additional event fields (location, goal_performance, etc.)

        Returns:
            Created event data with auto-calculated training dates

        Raises:
            ValueError: If event_type is invalid
        """
        # Validate event_type
        valid_types = [
            'marathon', 'half_marathon', '10k', '5k',
            'triathlon', 'cycling_race', 'swimming_meet',
            'powerlifting_meet', 'weightlifting_meet', 'strongman',
            'bodybuilding_show', 'physique_competition',
            'crossfit_competition', 'obstacle_race',
            'team_sport_game', 'tennis_match', 'golf_tournament',
            'hiking_trip', 'skiing_trip', 'climbing_expedition',
            'fitness_test', 'photo_shoot', 'wedding', 'vacation', 'other'
        ]

        if event_type not in valid_types:
            raise ValueError(f"Invalid event_type: {event_type}. Must be one of {valid_types}")

        # Calculate training start date if not provided
        if 'training_start_date' not in kwargs:
            template = self.EVENT_PERIODIZATION_TEMPLATES.get(event_type, {})
            training_weeks = template.get('training_weeks', 12)
            kwargs['training_start_date'] = (event_date - timedelta(weeks=training_weeks)).isoformat()

        event_data = {
            'user_id': user_id,
            'event_name': event_name,
            'event_type': event_type,
            'event_date': event_date.isoformat(),
            **kwargs
        }

        # Database triggers will auto-calculate taper_start_date and peak_week_date
        response = self.supabase.table('user_events').insert(event_data).execute()
        event = response.data[0] if response.data else {}

        logger.info(f"Created event '{event_name}' for user {user_id} on {event_date}")

        return event

    async def get_upcoming_events(
        self,
        user_id: str,
        days_ahead: int = 365
    ) -> List[Dict[str, Any]]:
        """
        Get upcoming events for user within timeframe.

        Args:
            user_id: User UUID
            days_ahead: Number of days to look ahead (default: 365)

        Returns:
            List of upcoming events ordered by date
        """
        cutoff_date = (date.today() + timedelta(days=days_ahead)).isoformat()

        response = self.supabase.table('user_events')\
            .select('*')\
            .eq('user_id', user_id)\
            .gte('event_date', date.today().isoformat())\
            .lte('event_date', cutoff_date)\
            .in_('status', ['upcoming', 'registered', 'training', 'tapering'])\
            .order('event_date')\
            .execute()

        return response.data if response.data else []

    async def get_primary_event(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get user's primary event (highest priority upcoming event).

        Args:
            user_id: User UUID

        Returns:
            Primary event dict or None if no primary event
        """
        response = self.supabase.table('user_events')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('is_primary_goal', True)\
            .gte('event_date', date.today().isoformat())\
            .single()\
            .execute()

        return response.data if response.data else None

    async def get_event_countdown(self, event_id: str) -> Dict[str, Any]:
        """
        Get countdown information for event.

        Returns:
            - days_until_event
            - weeks_until_event
            - current_training_phase (base/build/peak/taper)
            - training_phase_progress (%)
            - key_milestones
        """
        event = self.supabase.table('user_events')\
            .select('*')\
            .eq('id', event_id)\
            .single()\
            .execute().data

        if not event:
            raise ValueError(f"Event {event_id} not found")

        event_date = date.fromisoformat(event['event_date'])
        today = date.today()

        days_until = (event_date - today).days
        weeks_until = days_until // 7

        # Determine current phase
        taper_date = date.fromisoformat(event['taper_start_date']) if event.get('taper_start_date') else event_date - timedelta(weeks=2)
        peak_date = date.fromisoformat(event['peak_week_date']) if event.get('peak_week_date') else event_date - timedelta(weeks=1)
        training_start = date.fromisoformat(event['training_start_date']) if event.get('training_start_date') else today

        if today >= taper_date:
            current_phase = 'taper'
            phase_start = taper_date
            phase_end = event_date
        elif today >= peak_date:
            current_phase = 'peak'
            phase_start = peak_date
            phase_end = taper_date
        elif today >= training_start:
            current_phase = 'build'
            phase_start = training_start
            phase_end = peak_date
        else:
            current_phase = 'pre_training'
            phase_start = today
            phase_end = training_start

        # Calculate phase progress
        total_phase_days = (phase_end - phase_start).days
        elapsed_phase_days = (today - phase_start).days
        phase_progress = (elapsed_phase_days / total_phase_days * 100) if total_phase_days > 0 else 0

        return {
            'event_id': event_id,
            'event_name': event['event_name'],
            'event_type': event['event_type'],
            'event_date': event['event_date'],
            'days_until_event': days_until,
            'weeks_until_event': weeks_until,
            'current_training_phase': current_phase,
            'phase_progress_percentage': round(phase_progress, 1),
            'is_taper_week': today >= taper_date,
            'is_peak_week': peak_date <= today < taper_date,
            'is_pre_training': today < training_start,
            'milestones': {
                'training_starts': training_start.isoformat(),
                'peak_week_starts': peak_date.isoformat(),
                'taper_starts': taper_date.isoformat(),
                'event_day': event_date.isoformat()
            },
            'countdown_message': self._generate_countdown_message(days_until, current_phase)
        }

    async def generate_event_specific_program(
        self,
        user_id: str,
        event_id: str
    ) -> str:
        """
        Generate AI program periodized for specific event.

        Creates training plan that:
        - Peaks at event date
        - Includes proper taper
        - Adjusts volume/intensity by phase
        - Includes nutrition periodization (carb cycling, peak week protocol)

        Args:
            user_id: User UUID
            event_id: Event UUID

        Returns:
            program_id of generated AI program

        Raises:
            ValueError: If event not found or user doesn't own event
        """
        # Get event
        event_response = self.supabase.table('user_events')\
            .select('*')\
            .eq('id', event_id)\
            .eq('user_id', user_id)\
            .single()\
            .execute()

        if not event_response.data:
            raise ValueError(f"Event {event_id} not found or access denied")

        event = event_response.data

        # Get user profile
        from app.services.program_service import ProgramService
        program_service = ProgramService(self.supabase)
        user_data = await program_service.get_user_profile_for_generation(user_id)

        # Calculate program duration (from now until event)
        event_date = date.fromisoformat(event['event_date'])
        days_until_event = (event_date - date.today()).days
        weeks_until_event = days_until_event // 7

        if weeks_until_event < 4:
            raise ValueError(f"Event is only {weeks_until_event} weeks away. Need at least 4 weeks to generate program.")

        # Get periodization template
        template = self.EVENT_PERIODIZATION_TEMPLATES.get(
            event['event_type'],
            {'training_weeks': min(weeks_until_event, 12), 'phases': []}
        )

        # Build event-specific context for AI
        event_context = self._build_event_context(event, template, user_data)

        # Generate program using program_service with event context
        # Note: This integrates with existing program generation
        answers = [
            {'question': 'Event Type', 'answer': event['event_type']},
            {'question': 'Event Date', 'answer': event['event_date']},
            {'question': 'Event Goal', 'answer': event.get('goal_performance', 'Complete successfully')}
        ]

        # TODO: Modify program_service to accept event_context
        # For now, create program and link to event
        logger.info(f"Generating event-specific program for {event['event_name']}")

        # Placeholder - will integrate with program_service.generate_full_program
        program_id = "event_program_placeholder"

        # Link program to event
        self.supabase.table('user_events')\
            .update({'linked_program_id': program_id})\
            .eq('id', event_id)\
            .execute()

        return program_id

    async def get_all_events(
        self,
        user_id: str,
        include_completed: bool = False
    ) -> List[Dict[str, Any]]:
        """Get all events for user."""
        query = self.supabase.table('user_events')\
            .select('*')\
            .eq('user_id', user_id)\
            .order('event_date', desc=True)

        if not include_completed:
            query = query.in_('status', ['upcoming', 'registered', 'training', 'tapering'])

        response = query.execute()
        return response.data if response.data else []

    async def update_event(
        self,
        event_id: str,
        user_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update event details."""
        response = self.supabase.table('user_events')\
            .update(updates)\
            .eq('id', event_id)\
            .eq('user_id', user_id)\
            .execute()

        return response.data[0] if response.data else {}

    async def delete_event(self, event_id: str, user_id: str):
        """Delete event."""
        self.supabase.table('user_events')\
            .delete()\
            .eq('id', event_id)\
            .eq('user_id', user_id)\
            .execute()

        logger.info(f"Deleted event {event_id} for user {user_id}")

    async def complete_event(
        self,
        event_id: str,
        user_id: str,
        result_notes: Optional[str] = None,
        result_data: Optional[Dict[str, Any]] = None
    ):
        """Mark event as completed with results."""
        updates = {
            'status': 'completed',
            'completed_at': date.today().isoformat()
        }

        if result_notes:
            updates['result_notes'] = result_notes

        if result_data:
            updates['result_data'] = result_data

        return await self.update_event(event_id, user_id, updates)

    # =====================================================
    # PRIVATE HELPER METHODS
    # =====================================================

    def _build_event_context(
        self,
        event: Dict[str, Any],
        template: Dict[str, Any],
        user_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Build comprehensive event context for AI program generation."""
        event_date = date.fromisoformat(event['event_date'])
        days_until = (event_date - date.today()).days

        return {
            'event_details': {
                'name': event['event_name'],
                'type': event['event_type'],
                'subtype': event.get('event_subtype'),
                'date': event['event_date'],
                'days_until_event': days_until,
                'goal_performance': event.get('goal_performance'),
                'location': event.get('location')
            },
            'periodization': {
                'total_weeks': template.get('training_weeks', 12),
                'taper_weeks': template.get('taper_weeks', 1),
                'phases': template.get('phases', []),
                'nutrition_strategy': template.get('nutrition_strategy')
            },
            'user_profile': {
                'experience_level': user_data['profile'].get('experience_level'),
                'equipment': user_data['profile'].get('equipment_access'),
                'training_frequency': user_data['profile'].get('training_frequency')
            }
        }

    def _generate_countdown_message(self, days_until: int, phase: str) -> str:
        """Generate human-readable countdown message."""
        if days_until < 0:
            return "Event has passed"
        elif days_until == 0:
            return "Event is TODAY!"
        elif days_until == 1:
            return "1 day until event!"
        elif days_until < 7:
            return f"{days_until} days until event!"
        elif days_until < 14:
            weeks = days_until // 7
            extra_days = days_until % 7
            if extra_days == 0:
                return f"{weeks} week{'s' if weeks > 1 else ''} until event"
            return f"{weeks} week{'s' if weeks > 1 else ''} and {extra_days} day{'s' if extra_days > 1 else ''} until event"
        else:
            weeks = days_until // 7
            return f"{weeks} weeks until event ({phase} phase)"


# Global instance
_event_service: Optional[EventService] = None


def get_event_service() -> EventService:
    """Get the global EventService instance."""
    global _event_service
    if _event_service is None:
        _event_service = EventService()
    return _event_service
