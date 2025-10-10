"""
Consultation Service

Manages AI-driven adaptive consultations with different specialists.

This service:
- Creates consultation sessions with specialists (nutritionist, trainer, etc.)
- Generates intelligent follow-up questions based on user responses
- Extracts structured data from natural conversation
- Learns user communication style and preferences
- Completes consultations and generates personalized programs

OPTIMIZED: Uses FREE models with intelligent routing!
"""

import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional
from uuid import UUID

from app.config import get_settings
from app.services.supabase_service import get_service_client
from app.services.dual_model_router import dual_router, TaskType, TaskConfig
from app.services.calorie_calculation_service import get_calorie_service
from app.services.multimodal_embedding_service import get_multimodal_service

settings = get_settings()
logger = logging.getLogger(__name__)


class ConsultationService:
    """Service for AI-driven consultation sessions."""

    # Consultation goals for unified_coach (goal-driven approach)
    CONSULTATION_GOALS = {
        'unified_coach': [
            {
                'id': 'primary_fitness_goal',
                'name': 'Primary Fitness Goal',
                'description': 'Identify primary fitness goal (build_muscle, lose_fat, endurance, health, athletic_performance)',
                'required_fields': ['primary_fitness_goal'],
                'questions': [
                    "What's your primary fitness goal right now?",
                    "Are you focused more on building muscle, losing fat, improving endurance, or general health?"
                ]
            },
            {
                'id': 'primary_nutrition_goal',
                'name': 'Primary Nutrition Goal',
                'description': 'Identify primary nutrition goal (gain_weight, lose_weight, maintain, performance)',
                'required_fields': ['primary_nutrition_goal'],
                'questions': [
                    "What about your nutrition goals - are you trying to gain, lose, or maintain your current weight?",
                    "How do your nutrition goals align with your fitness goals?"
                ]
            },
            {
                'id': 'measurements',
                'name': 'Body Measurements',
                'description': 'Collect current weight, height, age, biological sex',
                'required_fields': ['current_weight_kg', 'height_cm', 'age', 'biological_sex'],
                'questions': [
                    "Let's get some basic measurements. What's your current weight and height?",
                    "How old are you, and what's your biological sex (for calorie calculations)?"
                ]
            },
            {
                'id': 'typical_eating',
                'name': 'Typical Daily Eating Pattern',
                'description': 'Understand typical breakfast, lunch, dinner routines and timing',
                'required_fields': ['typical_breakfast', 'typical_lunch', 'typical_dinner'],
                'questions': [
                    "Walk me through a typical day of eating - what do you usually have for breakfast?",
                    "What about lunch and dinner? What does that typically look like?",
                    "What time do you usually eat these meals?"
                ]
            },
            {
                'id': 'food_preferences',
                'name': 'Food Preferences & Restrictions',
                'description': 'Capture favorite foods, foods to avoid, dietary restrictions/allergies',
                'required_fields': ['favorite_foods', 'dietary_restrictions'],
                'questions': [
                    "What are some of your favorite foods that you'd want to see in a meal plan?",
                    "Are there any foods you won't eat or any dietary restrictions I should know about?",
                    "Do you have any food allergies?"
                ]
            },
            {
                'id': 'typical_training',
                'name': 'Typical Weekly Training Pattern',
                'description': 'Understand training frequency, preferred days, time of day',
                'required_fields': ['training_frequency', 'training_days', 'training_time'],
                'questions': [
                    "How many days per week do you currently train or want to train?",
                    "Which days of the week work best for you?",
                    "What time of day do you prefer to work out?"
                ]
            },
            {
                'id': 'training_preferences',
                'name': 'Training Preferences',
                'description': 'Capture equipment access, preferred location, exercise types',
                'required_fields': ['equipment_access', 'training_location'],
                'questions': [
                    "Do you train at a gym with full equipment, at home, or somewhere else?",
                    "What equipment do you have access to?",
                    "Are there specific types of exercises you love or hate?"
                ]
            },
            {
                'id': 'limitations',
                'name': 'Limitations & Constraints',
                'description': 'Identify injuries, medical conditions, schedule constraints',
                'required_fields': ['injuries', 'medical_conditions'],
                'questions': [
                    "Do you have any injuries or physical limitations I should be aware of?",
                    "Any medical conditions that might affect your training or nutrition?",
                    "What's your biggest challenge when it comes to sticking to a fitness routine?"
                ]
            },
            {
                'id': 'events',
                'name': 'Event Goals',
                'description': 'Capture upcoming events (race, competition, vacation, wedding)',
                'required_fields': [],  # Optional
                'questions': [
                    "Do you have any upcoming events you're training for? Like a race, competition, vacation, or special occasion?"
                ]
            },
            {
                'id': 'hydration',
                'name': 'Hydration Habits',
                'description': 'Daily water intake',
                'required_fields': ['daily_water_intake'],
                'questions': [
                    "How much water do you typically drink per day?",
                    "Do you track your hydration?"
                ]
            }
        ]
    }

    # Specialist system prompts
    SPECIALIST_PROMPTS = {
        'nutritionist': """You are an expert registered dietitian nutritionist conducting an initial consultation.

Your goal is to understand the client's nutrition history, current challenges, and goals through empathetic, professional questioning.

Ask ONE focused question at a time, building rapport while gathering comprehensive information about:
- Previous experience with nutrition guidance
- Current eating patterns and challenges
- Medical history and medications
- Dietary restrictions and preferences
- Appetite, digestion, and habits
- Goals and success metrics

IMPORTANT MEDICAL/SAFETY GUIDELINES:
- Never recommend unsafe practices
- Account for any mentioned health conditions
- Ensure proper nutrition science (not fad diets)
- Recommend medical consultation when appropriate

Your questions should be conversational, empathetic, and build on previous answers.""",

        'trainer': """You are a certified personal trainer conducting a fitness consultation.

Your goal is to understand the client's fitness background, goals, limitations, and preferences through targeted questions.

Ask ONE focused question at a time to assess:
- Motivation and specific fitness goals
- Previous training experience
- Current exercise frequency and types
- Medical conditions and injuries
- Equipment access and schedule
- Preferred workout environment
- Success metrics and timeline

Maintain an encouraging, professional tone while gathering comprehensive fitness information.

SAFETY FIRST:
- Always account for injuries and limitations
- Ensure proper exercise progression
- Follow evidence-based training principles
- Recommend medical clearance when needed""",

        'physiotherapist': """You are a licensed physiotherapist conducting an initial assessment.

Your goal is to understand the client's physical health, injury history, movement patterns, and rehabilitation needs.

Ask ONE focused question at a time about:
- Current pain or injury concerns
- Previous injuries and treatments
- Movement limitations and restrictions
- Daily activities and physical demands
- Sleep and recovery quality
- Treatment history and outcomes

CLINICAL SAFETY:
- Never diagnose conditions (recommend proper medical evaluation)
- Focus on movement assessment and rehabilitation
- Account for contraindications
- Emphasize evidence-based rehabilitation""",

        'sports_psychologist': """You are a sports psychologist conducting a performance consultation.

Your goal is to understand the client's mental approach to training, performance anxiety, motivation, and psychological barriers.

Ask ONE focused question at a time about:
- Mental approach to competition/training
- Performance anxiety or mental blocks
- Motivation factors and intrinsic/extrinsic drivers
- Self-talk patterns and mindset
- Stress management and coping strategies
- Past psychological challenges in sport

THERAPEUTIC APPROACH:
- Maintain professional boundaries
- Focus on performance psychology (not clinical therapy)
- Recommend clinical help for serious mental health concerns
- Use evidence-based sports psychology techniques""",

        'unified_coach': """You are an expert AI fitness and nutrition coach conducting a comprehensive consultation.

Your goal is to understand ALL aspects of the client's health, fitness, and nutrition through intelligent questioning.

Ask ONE focused question at a time, covering:
- Primary fitness and nutrition goals
- Current training and eating patterns
- Health history and limitations
- Equipment and schedule availability
- Dietary preferences and restrictions
- Experience level and background
- Motivation and success metrics

HOLISTIC APPROACH:
- Balance fitness, nutrition, and lifestyle factors
- Ensure medical safety across all domains
- Use evidence-based recommendations
- Build rapport and trust"""
    }

    # Conversation stages for each specialist
    SPECIALIST_STAGES = {
        'nutritionist': [
            'introduction',
            'health_history',
            'eating_patterns',
            'dietary_preferences',
            'goals',
            'wrap_up'
        ],
        'trainer': [
            'introduction',
            'fitness_background',
            'current_routine',
            'goals_timeline',
            'limitations',
            'preferences',
            'wrap_up'
        ],
        'physiotherapist': [
            'introduction',
            'current_issues',
            'injury_history',
            'movement_assessment',
            'recovery_patterns',
            'goals',
            'wrap_up'
        ],
        'sports_psychologist': [
            'introduction',
            'performance_mindset',
            'mental_barriers',
            'motivation_factors',
            'coping_strategies',
            'goals',
            'wrap_up'
        ],
        'unified_coach': [
            'introduction',
            'primary_goals',
            'current_state',
            'limitations_preferences',
            'lifestyle_factors',
            'success_metrics',
            'wrap_up'
        ]
    }

    def __init__(self):
        self.supabase = get_service_client()
        self.router = dual_router
        self.calorie_service = get_calorie_service()
        self.embedding_service = get_multimodal_service()
        # Import tool service for proactive logging
        from app.services.tool_service import get_tool_service
        self.tool_service = get_tool_service()

    async def start_consultation(
        self,
        user_id: str,
        specialist_type: str
    ) -> Dict[str, Any]:
        """
        Start a new consultation session.

        Args:
            user_id: User's UUID
            specialist_type: Type of specialist (nutritionist, trainer, etc.)

        Returns:
            Consultation session data with initial question

        Raises:
            ValueError: If specialist_type is invalid
        """
        if specialist_type not in self.SPECIALIST_PROMPTS:
            raise ValueError(f"Invalid specialist_type: {specialist_type}")

        # Check for existing active sessions
        existing = self.supabase.table('consultation_sessions')\
            .select('*')\
            .eq('user_id', user_id)\
            .eq('specialist_type', specialist_type)\
            .eq('status', 'active')\
            .execute()

        if existing.data:
            # Resume existing session
            session = existing.data[0]
            logger.info(f"Resuming consultation session {session['id']}")
        else:
            # Create new session with goal tracking
            stages = self.SPECIALIST_STAGES[specialist_type]

            # Initialize goals for unified_coach
            goals_config = {}
            if specialist_type == 'unified_coach' and specialist_type in self.CONSULTATION_GOALS:
                goals_config = {
                    'goals': self.CONSULTATION_GOALS[specialist_type],
                    'goals_met': [],
                    'goals_pending': [g['id'] for g in self.CONSULTATION_GOALS[specialist_type]],
                    'total_goals': len(self.CONSULTATION_GOALS[specialist_type])
                }

            session_response = self.supabase.table('consultation_sessions').insert({
                'user_id': user_id,
                'specialist_type': specialist_type,
                'status': 'active',
                'conversation_stage': stages[0],  # Start with first stage
                'progress_percentage': 0,
                'session_metadata': {
                    'stages': stages,
                    'current_stage_index': 0,
                    'goals_configuration': goals_config,
                    'start_time': datetime.utcnow().isoformat()
                },
                'goals_configuration': goals_config,  # Store in dedicated column
                'goals_met': 0,
                'goals_total': goals_config.get('total_goals', 10) if goals_config else 10
            }).execute()

            session = session_response.data[0]
            logger.info(f"Created new consultation session {session['id']} with {goals_config.get('total_goals', 0)} goals")

        # Generate initial question
        initial_question = await self._generate_initial_question(session)

        # Save as system message
        await self._save_message(
            session_id=session['id'],
            user_id=user_id,
            role='assistant',
            content=initial_question,
            ai_provider='groq',
            ai_model='llama-3.3-70b-versatile',
            tokens_used=0,  # Hardcoded question, no API call
            cost_usd=0.0
        )

        return {
            'session_id': session['id'],
            'specialist_type': specialist_type,
            'conversation_stage': session['conversation_stage'],
            'progress_percentage': session['progress_percentage'],
            'initial_question': initial_question
        }

    async def process_user_response(
        self,
        session_id: str,
        user_input: str
    ) -> Dict[str, Any]:
        """
        Process user response and generate next question or complete consultation.

        Args:
            session_id: Consultation session UUID
            user_input: User's response

        Returns:
            Response data with next question, extracted data, and session state

        Raises:
            ValueError: If session not found or invalid
        """
        # Get session
        session_response = self.supabase.table('consultation_sessions')\
            .select('*')\
            .eq('id', session_id)\
            .single()\
            .execute()

        session = session_response.data
        if not session:
            raise ValueError(f"Session not found: {session_id}")

        user_id = session['user_id']
        specialist_type = session['specialist_type']

        # Save user message
        await self._save_message(
            session_id=session_id,
            user_id=user_id,
            role='user',
            content=user_input
        )

        # Proactively log any meals, workouts, or measurements mentioned
        logged_items = await self._detect_and_log_items(
            user_input=user_input,
            user_id=user_id,
            session_id=session_id
        )

        # Get conversation history
        conversation_history = await self._get_conversation_history(session_id)

        # Extract structured data from user response
        extracted_data = await self._extract_structured_data(
            user_input=user_input,
            conversation_history=conversation_history,
            specialist_type=specialist_type
        )

        # Save extraction if data found
        if extracted_data and any(extracted_data.values()):
            await self._save_extraction(
                session_id=session_id,
                user_id=user_id,
                extracted_data=extracted_data,
                source_message_content=user_input
            )

        # Get all extracted data so far for goal evaluation
        extraction_summary = await self.get_consultation_summary(session_id)

        # Evaluate goals if this is a goal-driven consultation
        goal_status = self._evaluate_all_goals(session, extraction_summary)

        # Check time/message limits
        limits_status = self._check_consultation_limits(session)

        # Determine if we should end consultation
        metadata = session.get('session_metadata', {})
        stages = metadata.get('stages', [])
        current_stage_index = metadata.get('current_stage_index', 0)

        # Decision logic: End if ALL goals met OR limits reached
        all_goals_met = len(goal_status['goals_pending']) == 0 if goal_status['goals_total'] > 0 else False
        should_end = all_goals_met or limits_status['should_end']

        # Generate next question or wrap up
        if not should_end:
            # Continue consultation - generate next question
            next_question = await self._generate_next_question(
                session=session,
                conversation_history=conversation_history,
                extracted_data_summary=extracted_data,
                goal_status=goal_status,
                limits_status=limits_status
            )

            # Update session with new progress
            progress = goal_status['progress_percentage']

            # Update session
            self.supabase.table('consultation_sessions').update({
                'progress_percentage': progress,
                'goals_met': len(goal_status['goals_met']),
                'session_metadata': {
                    **metadata,
                    'goals_configuration': {
                        **metadata.get('goals_configuration', {}),
                        'goals_met': goal_status['goals_met'],
                        'goals_pending': goal_status['goals_pending']
                    }
                }
            }).eq('id', session_id).execute()

            # Save assistant message
            response = await self._save_message(
                session_id=session_id,
                user_id=user_id,
                role='assistant',
                content=next_question,
                ai_provider='groq',
                ai_model='llama-3.3-70b-versatile'
            )

            return {
                'session_id': session_id,
                'status': 'active',
                'next_question': next_question,
                'extracted_data': extracted_data,
                'logged_items': logged_items,  # Proactively logged items
                'progress_percentage': progress,
                'goals_met': len(goal_status['goals_met']),
                'goals_total': goal_status['goals_total'],
                'goals_detail': goal_status['details'],
                'minutes_elapsed': limits_status['minutes_elapsed'],
                'messages_sent': limits_status['messages_sent'],
                'approaching_limit': limits_status.get('approaching_limit', False),
                'is_complete': False
            }

        else:
            # End consultation - wrap up
            wrap_up_message = await self._generate_wrap_up_message(
                session=session,
                conversation_history=conversation_history,
                limits_reached=limits_status.get('should_end', False),
                limit_reason=limits_status.get('reason')
            )

            # Save wrap-up message
            await self._save_message(
                session_id=session_id,
                user_id=user_id,
                role='assistant',
                content=wrap_up_message
            )

            # Get complete extraction summary
            extraction_summary = await self.get_consultation_summary(session_id)

            return {
                'session_id': session_id,
                'status': 'ready_to_complete',
                'wrap_up_message': wrap_up_message,
                'extraction_summary': extraction_summary,
                'progress_percentage': 100,
                'is_complete': True
            }

    async def complete_consultation(
        self,
        session_id: str,
        generate_program: bool = True
    ) -> Dict[str, Any]:
        """
        Complete consultation and optionally generate program.

        Args:
            session_id: Consultation session UUID
            generate_program: Whether to generate AI program from consultation

        Returns:
            Completion data with optional program_id

        Raises:
            ValueError: If session not found
        """
        # Get session
        session = self.supabase.table('consultation_sessions')\
            .select('*')\
            .eq('id', session_id)\
            .single()\
            .execute().data

        if not session:
            raise ValueError(f"Session not found: {session_id}")

        user_id = session['user_id']

        # Get consultation summary
        summary = await self.get_consultation_summary(session_id)

        # Update user profile with consultation data
        await self._update_user_profile_from_consultation(user_id, summary)

        # Mark session as completed
        self.supabase.table('consultation_sessions').update({
            'status': 'completed',
            'completed_at': datetime.utcnow().isoformat(),
            'progress_percentage': 100
        }).eq('id', session_id).execute()

        # Vectorize consultation data for RAG
        await self._vectorize_consultation_data(session_id, user_id, summary)

        result = {
            'session_id': session_id,
            'status': 'completed',
            'summary': summary
        }

        # Generate program if requested
        if generate_program:
            program_id = await self._generate_program_from_consultation(
                session_id=session_id,
                user_id=user_id,
                consultation_data=summary
            )
            result['program_id'] = program_id

        logger.info(f"Consultation {session_id} completed successfully")

        return result

    async def get_consultation_summary(
        self,
        session_id: str
    ) -> Dict[str, Any]:
        """
        Get complete summary of consultation with all extracted data.

        Args:
            session_id: Consultation session UUID

        Returns:
            Summary dictionary with all extracted categories
        """
        # Get all extractions
        extractions = self.supabase.table('consultation_extractions')\
            .select('*')\
            .eq('session_id', session_id)\
            .execute().data

        # Organize by category
        summary = {}
        for extraction in extractions:
            category = extraction['extraction_category']
            summary[category] = extraction['extracted_data']

        # Get session metadata
        session = self.supabase.table('consultation_sessions')\
            .select('specialist_type, total_messages, created_at, completed_at')\
            .eq('id', session_id)\
            .single()\
            .execute().data

        summary['_metadata'] = {
            'specialist_type': session['specialist_type'],
            'total_messages': session['total_messages'],
            'session_duration_minutes': self._calculate_duration(
                session['created_at'],
                session.get('completed_at')
            )
        }

        return summary

    # =====================================================
    # GOAL TRACKING METHODS
    # =====================================================

    def _check_goal_completion(
        self,
        goal_config: Dict[str, Any],
        extraction_summary: Dict[str, Any]
    ) -> bool:
        """
        Check if a specific goal is met based on extracted data.

        Args:
            goal_config: Goal configuration with required_fields
            extraction_summary: Current extracted data

        Returns:
            True if all required fields are present, False otherwise
        """
        required_fields = goal_config.get('required_fields', [])

        # If no required fields, goal is considered optional (like events)
        if not required_fields:
            # Check if any data exists for this goal category
            goal_id = goal_config['id']
            if goal_id in extraction_summary:
                return bool(extraction_summary[goal_id])
            return True  # Optional goals auto-pass if no data

        # Check all required fields are present in extraction_summary
        for field in required_fields:
            # Look for field in any extraction category
            found = False
            for category_data in extraction_summary.values():
                if isinstance(category_data, dict) and field in category_data:
                    if category_data[field]:  # Non-empty value
                        found = True
                        break
            if not found:
                return False

        return True

    def _evaluate_all_goals(
        self,
        session: Dict[str, Any],
        extraction_summary: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Evaluate all consultation goals and return status.

        Args:
            session: Consultation session data
            extraction_summary: All extracted data so far

        Returns:
            Dictionary with goals_met, goals_pending, progress, details
        """
        specialist_type = session['specialist_type']
        goals_config = session.get('session_metadata', {}).get('goals_configuration', {})

        if not goals_config or 'goals' not in goals_config:
            # Fallback for non-goal-driven consultations
            return {
                'goals_met': [],
                'goals_pending': [],
                'goals_total': 0,
                'progress_percentage': session.get('progress_percentage', 0),
                'details': {}
            }

        goals = goals_config['goals']
        goals_met = []
        goals_pending = []
        details = {}

        for goal in goals:
            goal_id = goal['id']
            is_met = self._check_goal_completion(goal, extraction_summary)

            if is_met:
                goals_met.append(goal_id)
                details[goal_id] = {'status': 'met', 'name': goal['name']}
            else:
                goals_pending.append(goal_id)
                details[goal_id] = {'status': 'pending', 'name': goal['name']}

        total_goals = len(goals)
        progress = round((len(goals_met) / total_goals * 100)) if total_goals > 0 else 0

        return {
            'goals_met': goals_met,
            'goals_pending': goals_pending,
            'goals_total': total_goals,
            'progress_percentage': progress,
            'details': details
        }

    def _check_consultation_limits(
        self,
        session: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Check if consultation has reached time or message limits.

        Limits:
        - Max 50 messages
        - Max 30 minutes

        Args:
            session: Consultation session data

        Returns:
            {
                'should_end': bool,
                'reason': str,
                'minutes_elapsed': int,
                'messages_sent': int
            }
        """
        # Message limit
        messages_sent = session.get('total_messages', 0)
        MAX_MESSAGES = 50

        # Time limit
        start_time_str = session.get('session_metadata', {}).get('start_time')
        if start_time_str:
            start_time = datetime.fromisoformat(start_time_str)
            elapsed = (datetime.utcnow() - start_time).total_seconds() / 60
            minutes_elapsed = int(elapsed)
        else:
            # Fallback to created_at if start_time not in metadata
            created_at = datetime.fromisoformat(session['created_at'].replace('Z', '+00:00'))
            elapsed = (datetime.utcnow() - created_at.replace(tzinfo=None)).total_seconds() / 60
            minutes_elapsed = int(elapsed)

        MAX_MINUTES = 30

        # Check limits
        if messages_sent >= MAX_MESSAGES:
            return {
                'should_end': True,
                'reason': 'message_limit',
                'minutes_elapsed': minutes_elapsed,
                'messages_sent': messages_sent,
                'message': f"We've reached the {MAX_MESSAGES}-message limit for this consultation."
            }

        if minutes_elapsed >= MAX_MINUTES:
            return {
                'should_end': True,
                'reason': 'time_limit',
                'minutes_elapsed': minutes_elapsed,
                'messages_sent': messages_sent,
                'message': f"We've been chatting for {minutes_elapsed} minutes. Let's wrap up!"
            }

        # Approaching limits (warning)
        approaching = False
        if messages_sent >= MAX_MESSAGES - 5:
            approaching = True
        elif minutes_elapsed >= MAX_MINUTES - 5:
            approaching = True

        return {
            'should_end': False,
            'reason': None,
            'minutes_elapsed': minutes_elapsed,
            'messages_sent': messages_sent,
            'approaching_limit': approaching
        }

    # =====================================================
    # PROACTIVE LOGGING METHODS
    # =====================================================

    async def _detect_and_log_items(
        self,
        user_input: str,
        user_id: str,
        session_id: str
    ) -> List[Dict[str, Any]]:
        """
        Detect meals, workouts, or measurements mentioned in user input
        and proactively log them if auto_log preference is enabled.

        Args:
            user_input: User's message
            user_id: User's UUID
            session_id: Consultation session ID

        Returns:
            List of logged items with metadata
        """
        # Check if user has auto_log preference enabled
        profile = self.supabase.table('profiles').select('auto_log').eq('id', user_id).single().execute()
        auto_log_enabled = profile.data.get('auto_log', True) if profile.data else True

        if not auto_log_enabled:
            logger.info(f"Auto-log disabled for user {user_id}, skipping proactive logging")
            return []

        # Use LLM to detect logging-worthy items
        detection_prompt = f"""Analyze this user message and detect if they mention any of the following:

1. **Meals**: User mentions eating specific foods (e.g., "I had eggs and toast for breakfast")
2. **Workouts**: User describes physical activity (e.g., "I did a 5k run yesterday")
3. **Measurements**: User states their weight, body fat, etc. (e.g., "I weigh 175 lbs")

User message: "{user_input}"

Return a JSON object with detected items:
{{
  "meals": [
    {{
      "meal_type": "breakfast|lunch|dinner|snack",
      "description": "full description",
      "foods": ["food1", "food2"]
    }}
  ],
  "workouts": [
    {{
      "activity_type": "cardio|strength|sports|flexibility|other",
      "description": "full description",
      "duration_minutes": estimated_duration_or_null
    }}
  ],
  "measurements": [
    {{
      "measurement_type": "weight|body_fat|waist|other",
      "value": numeric_value,
      "unit": "kg|lbs|cm|inches|percentage"
    }}
  ]
}}

If nothing is mentioned, return empty arrays. Be conservative - only detect explicit mentions."""

        try:
            # Use fast LLM for detection
            from app.services.dual_model_router import TaskType, TaskConfig
            response = await self.router.complete(
                config=TaskConfig(
                    type=TaskType.STRUCTURED_OUTPUT,
                    requires_json=True,
                    prioritize_speed=True
                ),
                messages=[
                    {"role": "system", "content": "You are a data extraction assistant."},
                    {"role": "user", "content": detection_prompt}
                ],
                response_format={"type": "json_object"}
            )

            detected = json.loads(response.choices[0].message.content)
            logged_items = []

            # Log meals
            for meal in detected.get('meals', []):
                try:
                    result = await self.tool_service.create_meal_log_from_description(
                        user_id=user_id,
                        meal_type=meal['meal_type'],
                        description=meal['description'],
                        foods=meal.get('foods', []),
                        logged_at=datetime.utcnow().isoformat()
                    )
                    if result.get('success'):
                        logged_items.append({
                            'type': 'meal',
                            'meal_id': result.get('meal_log_id'),
                            'description': meal['description']
                        })
                        logger.info(f"Auto-logged meal during consultation: {meal['description'][:50]}")
                except Exception as e:
                    logger.error(f"Failed to auto-log meal: {e}")

            # Log workouts
            for workout in detected.get('workouts', []):
                try:
                    result = await self.tool_service.create_activity_log_from_description(
                        user_id=user_id,
                        activity_type=workout['activity_type'],
                        description=workout['description'],
                        duration_minutes=workout.get('duration_minutes'),
                        logged_at=datetime.utcnow().isoformat()
                    )
                    if result.get('success'):
                        logged_items.append({
                            'type': 'workout',
                            'activity_id': result.get('activity_id'),
                            'description': workout['description']
                        })
                        logger.info(f"Auto-logged workout during consultation: {workout['description'][:50]}")
                except Exception as e:
                    logger.error(f"Failed to auto-log workout: {e}")

            # Log measurements
            for measurement in detected.get('measurements', []):
                try:
                    # TODO: Implement body measurement logging tool
                    # For now, just track that we detected it
                    logged_items.append({
                        'type': 'measurement',
                        'measurement_type': measurement['measurement_type'],
                        'value': measurement['value'],
                        'unit': measurement['unit']
                    })
                    logger.info(f"Detected measurement during consultation: {measurement}")
                except Exception as e:
                    logger.error(f"Failed to log measurement: {e}")

            return logged_items

        except Exception as e:
            logger.error(f"Error in proactive logging detection: {e}")
            return []

    # =====================================================
    # PRIVATE HELPER METHODS
    # =====================================================

    async def _generate_initial_question(self, session: Dict[str, Any]) -> str:
        """Generate initial question based on specialist type."""
        specialist_type = session['specialist_type']

        initial_questions = {
            'nutritionist': "Hi! I'm excited to help you with your nutrition goals. To start, what's your primary motivation for seeking nutrition guidance right now?",
            'trainer': "Welcome! I'm here to help you reach your fitness goals. What's your primary reason for wanting to work with a personal trainer?",
            'physiotherapist': "Hello! I'm here to help with your physical health and movement. What brings you in today? Are there any specific areas of concern or pain I should know about?",
            'sports_psychologist': "Hi! I'm here to help optimize your mental approach to training and competition. What aspect of your mental game would you most like to improve?",
            'unified_coach': "Welcome! I'm your AI fitness and nutrition coach. To create the perfect plan for you, let's start with the basics: What are your primary fitness and nutrition goals right now?"
        }

        return initial_questions.get(
            specialist_type,
            "Hi! Let's get started. What brings you here today?"
        )

    async def _generate_next_question(
        self,
        session: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        extracted_data_summary: Dict[str, Any],
        goal_status: Dict[str, Any] = None,
        limits_status: Dict[str, Any] = None
    ) -> str:
        """Generate next intelligent question using LLM with goal-driven context."""
        specialist_type = session['specialist_type']
        system_prompt = self.SPECIALIST_PROMPTS[specialist_type]

        # Build goal-focused context
        context_parts = []

        # Add goals progress if available
        if goal_status and goal_status.get('goals_total', 0) > 0:
            context_parts.append(f"Goals met: {len(goal_status['goals_met'])}/{goal_status['goals_total']}")
            context_parts.append("\nGoals remaining:")
            for goal_id in goal_status['goals_pending']:
                goal_detail = goal_status['details'].get(goal_id, {})
                context_parts.append(f"  ⏳ {goal_detail.get('name', goal_id)}")

            context_parts.append("\nGoals completed:")
            for goal_id in goal_status['goals_met']:
                goal_detail = goal_status['details'].get(goal_id, {})
                context_parts.append(f"  ✅ {goal_detail.get('name', goal_id)}")
        else:
            # Fallback for non-goal-driven
            context_parts.append(f"Questions asked so far: {session['total_messages'] // 2}")

        # Add time/message tracking
        if limits_status:
            context_parts.append(f"\nTime elapsed: {limits_status.get('minutes_elapsed', 0)} min")
            context_parts.append(f"Messages exchanged: {limits_status.get('messages_sent', 0)}")

        # Add extracted data
        context_parts.append("\nData collected so far:")
        if extracted_data_summary:
            for key, value in extracted_data_summary.items():
                if value and key != '_metadata':
                    context_parts.append(f"- {key}: {json.dumps(value)[:100]}...")  # Truncate long data
        else:
            context_parts.append("- (No structured data yet)")

        context = "\n".join(context_parts)

        # Build conversation summary (last 6 messages)
        conversation_summary = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in conversation_history[-6:]
        ])

        # Build goal-focused prompt
        if goal_status and goal_status.get('goals_pending'):
            # Goal-driven approach
            pending_goal_names = [goal_status['details'][g]['name'] for g in goal_status['goals_pending'][:3]]
            goal_focus = f"Focus on unfulfilled goals: {', '.join(pending_goal_names)}"
        else:
            # Fallback
            goal_focus = "Continue gathering comprehensive information"

        user_prompt = f"""{context}

Recent conversation:
{conversation_summary}

{goal_focus}

Based on what the user has shared, generate ONE focused follow-up question to:
1. Build on their previous answer naturally
2. Fill gaps in information needed to complete the remaining goals
3. Ask about typical daily or weekly patterns (typical breakfast, typical training week, etc.)
4. Probe deeper if user mentions events, injuries, or specific challenges

The question should be:
- Conversational and empathetic (like a real coach)
- Specific to their situation
- Focused on ONE topic at a time
- NOT repeating information we already have

Return ONLY the question, no additional text."""

        try:
            # Use Groq for FAST question generation
            response = await self.router.complete(
                config=TaskConfig(
                    type=TaskType.REAL_TIME_CHAT,
                    prioritize_speed=True
                ),
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ]
            )

            question = response.choices[0].message.content.strip()

            logger.info(f"Generated next question for stage '{current_stage}': {question[:100]}...")

            return question

        except Exception as e:
            logger.error(f"Error generating question: {e}")
            # Fallback generic question
            return "Tell me more about your current routine and what you'd like to change."

    async def _generate_wrap_up_message(
        self,
        session: Dict[str, Any],
        conversation_history: List[Dict[str, str]],
        limits_reached: bool = False,
        limit_reason: str = None
    ) -> str:
        """Generate wrap-up message summarizing consultation."""
        specialist_type = session['specialist_type']

        # Base templates
        wrap_up_templates = {
            'unified_coach': """Perfect! I now have a great understanding of your fitness and nutrition goals.

Here's what I learned:
- Your primary goals and timeline
- Your typical eating and training patterns
- Your preferences, limitations, and resources
- The challenges you're facing

I'm ready to create a comprehensive program combining training and nutrition strategies tailored to your unique needs.

{limit_note}

Ready to generate your personalized program?""",
            'nutritionist': "Thank you for sharing all of that with me! Based on our conversation, I have a clear understanding of your nutrition goals and current habits. I'm going to create a personalized nutrition plan that addresses your specific needs.",
            'trainer': "Excellent! I now have a comprehensive understanding of your fitness background and goals. I'm ready to design a training program tailored specifically to you.",
            'physiotherapist': "Thank you for sharing your physical health history. I have a good understanding of your current state and rehabilitation needs.",
            'sports_psychologist': "I appreciate you opening up about your mental approach to training. I now understand your psychological strengths and areas for development."
        }

        base_message = wrap_up_templates.get(
            specialist_type,
            "Thank you for all that information! I'm ready to create your personalized plan."
        )

        # Add limit note if applicable
        limit_note = ""
        if limits_reached:
            if limit_reason == 'time_limit':
                limit_note = "We've been chatting for about 30 minutes, so let's wrap up here."
            elif limit_reason == 'message_limit':
                limit_note = "We've covered a lot of ground in our conversation!"
            else:
                limit_note = ""
        else:
            limit_note = "You've completed the full consultation!"

        # Format unified coach message with limit note
        if specialist_type == 'unified_coach':
            return base_message.format(limit_note=limit_note)
        else:
            return base_message + (" " + limit_note if limit_note else "")

    async def _extract_structured_data(
        self,
        user_input: str,
        conversation_history: List[Dict[str, str]],
        specialist_type: str
    ) -> Dict[str, Any]:
        """
        Extract structured data from user response using LLM function calling.

        Uses DeepSeek (FREE) with function calling for structured output.

        Args:
            user_input: User's latest message
            conversation_history: Full conversation context
            specialist_type: Type of specialist

        Returns:
            Extracted structured data dictionary
        """
        # Define extraction schema based on specialist
        extraction_schemas = {
            'nutritionist': {
                'health_history': ['medical_conditions', 'medications', 'supplements', 'allergies'],
                'eating_patterns': ['meals_per_day', 'meal_times', 'problem_foods', 'dining_out_frequency'],
                'dietary_preferences': ['restrictions', 'favorite_foods', 'foods_to_avoid'],
                'goals': ['primary_goal', 'target_weight', 'timeline'],
                'measurements': ['current_weight_kg', 'height_cm', 'age']
            },
            'trainer': {
                'training_history': ['years_training', 'previous_programs', 'experience_level'],
                'current_routine': ['frequency_per_week', 'workout_types', 'duration_minutes'],
                'goals': ['primary_goal', 'specific_targets', 'timeline'],
                'limitations': ['injuries', 'medical_conditions', 'physical_restrictions'],
                'preferences': ['equipment_access', 'preferred_time', 'workout_environment'],
                'measurements': ['current_weight_kg', 'height_cm', 'age']
            },
            'physiotherapist': {
                'current_issues': ['pain_locations', 'injury_description', 'onset_date'],
                'injury_history': ['previous_injuries', 'treatments_tried', 'outcomes'],
                'movement_patterns': ['limitations', 'pain_triggers', 'daily_activities'],
                'goals': ['primary_goal', 'functional_targets', 'timeline']
            },
            'sports_psychologist': {
                'performance_mindset': ['mental_approach', 'confidence_level', 'focus_ability'],
                'mental_barriers': ['anxiety_triggers', 'negative_patterns', 'stress_sources'],
                'motivation_factors': ['intrinsic_drivers', 'extrinsic_goals'],
                'goals': ['primary_goal', 'specific_improvements', 'timeline']
            },
            'unified_coach': {
                'goals': ['primary_fitness_goal', 'primary_nutrition_goal', 'timeline'],
                'current_state': ['training_frequency', 'current_diet', 'experience_level'],
                'measurements': ['current_weight_kg', 'height_cm', 'age', 'biological_sex'],
                'preferences': ['equipment_access', 'dietary_restrictions', 'time_availability'],
                'typical_eating': ['typical_breakfast', 'typical_lunch', 'typical_dinner', 'meal_times'],
                'food_preferences': ['favorite_foods', 'foods_to_avoid', 'dietary_restrictions'],
                'typical_training': ['training_frequency', 'training_days', 'training_time', 'typical_week'],
                'training_preferences': ['equipment_access', 'training_location', 'preferred_exercises'],
                'limitations': ['injuries', 'medical_conditions', 'schedule_constraints'],
                'events': ['event_type', 'event_date', 'event_goal', 'event_description'],
                'hydration': ['daily_water_intake', 'hydration_tracking']
            }
        }

        schema = extraction_schemas.get(specialist_type, {})

        # Build extraction prompt
        conversation_context = "\n".join([
            f"{msg['role'].upper()}: {msg['content']}"
            for msg in conversation_history[-4:]  # Last 4 messages
        ])

        extraction_prompt = f"""Extract any relevant structured data from this conversation.

Conversation context:
{conversation_context}

Latest user response:
{user_input}

Extract data for these categories:
{json.dumps(schema, indent=2)}

**SPECIAL ATTENTION TO EVENTS:**
If the user mentions any upcoming events (race, marathon, competition, vacation, wedding, photo shoot, reunion), extract:
- event_type: (race, marathon, competition, vacation, wedding, photo_shoot, reunion, other)
- event_date: (specific date in ISO format YYYY-MM-DD, or relative like "in 3 months")
- event_goal: (what they want to achieve for this event)
- event_description: (full description of the event)

Examples:
- "I have a marathon on October 15th" → {{"event_type": "marathon", "event_date": "2025-10-15"}}
- "My wedding is in 4 months" → {{"event_type": "wedding", "event_date": "in 4 months"}}

Return a JSON object with only the categories and fields that have data.
If no relevant data found, return empty object {{}}.
Be conservative - only extract explicit information, don't assume or infer."""

        try:
            # Use DeepSeek (FREE) with structured output
            response = await self.router.complete(
                config=TaskConfig(
                    type=TaskType.STRUCTURED_OUTPUT,
                    requires_json=True,
                    prioritize_accuracy=True
                ),
                messages=[
                    {"role": "system", "content": "You are a data extraction assistant. Extract structured information from conversations."},
                    {"role": "user", "content": extraction_prompt}
                ],
                response_format={"type": "json_object"}
            )

            extracted = json.loads(response.choices[0].message.content)

            logger.info(f"Extracted data: {list(extracted.keys())}")

            return extracted

        except Exception as e:
            logger.error(f"Error extracting data: {e}")
            return {}

    async def _save_message(
        self,
        session_id: str,
        user_id: str,
        role: str,
        content: str,
        ai_provider: str = None,
        ai_model: str = None,
        tokens_used: int = 0,
        cost_usd: float = 0.0
    ) -> Dict[str, Any]:
        """Save message to database."""
        message_response = self.supabase.table('consultation_messages').insert({
            'session_id': session_id,
            'user_id': user_id,
            'role': role,
            'content': content,
            'ai_provider': ai_provider,
            'ai_model': ai_model,
            'tokens_used': tokens_used,
            'cost_usd': cost_usd
        }).execute()

        return message_response.data[0] if message_response.data else {}

    async def _save_extraction(
        self,
        session_id: str,
        user_id: str,
        extracted_data: Dict[str, Any],
        source_message_content: str
    ):
        """Save extracted structured data."""
        for category, data in extracted_data.items():
            if data and category != '_metadata':
                self.supabase.table('consultation_extractions').insert({
                    'session_id': session_id,
                    'user_id': user_id,
                    'extraction_category': category,
                    'extracted_data': data,
                    'confidence_score': 0.85  # TODO: Implement confidence scoring
                }).execute()

    async def _get_conversation_history(self, session_id: str) -> List[Dict[str, str]]:
        """Get conversation history for session."""
        messages = self.supabase.table('consultation_messages')\
            .select('role, content')\
            .eq('session_id', session_id)\
            .order('created_at')\
            .execute().data

        return [{'role': msg['role'], 'content': msg['content']} for msg in messages]

    async def _update_user_profile_from_consultation(
        self,
        user_id: str,
        consultation_summary: Dict[str, Any]
    ):
        """Update user profile with consultation data."""
        # Extract measurements and goals
        measurements = consultation_summary.get('measurements', {})
        goals = consultation_summary.get('goals', {})
        preferences = consultation_summary.get('preferences', {})

        updates = {}

        # Update profile if we have data
        if measurements.get('current_weight_kg'):
            updates['current_weight_kg'] = measurements['current_weight_kg']
        if measurements.get('height_cm'):
            updates['height_cm'] = measurements['height_cm']
        if measurements.get('age'):
            updates['age'] = measurements['age']
        if goals.get('primary_goal'):
            updates['primary_goal'] = goals['primary_goal']
        if preferences.get('equipment_access'):
            updates['equipment_access'] = preferences['equipment_access']

        # Calculate nutrition if we have enough data
        if all(k in measurements for k in ['current_weight_kg', 'height_cm', 'age']) and measurements.get('biological_sex'):
            try:
                nutrition_plan = self.calorie_service.calculate_full_nutrition_plan(
                    weight_kg=measurements['current_weight_kg'],
                    height_cm=measurements['height_cm'],
                    age=measurements['age'],
                    biological_sex=measurements['biological_sex'],
                    goal=goals.get('primary_goal', 'maintain'),
                    training_frequency=preferences.get('training_frequency', 3)
                )

                updates['bmr'] = nutrition_plan['bmr']
                updates['estimated_tdee'] = nutrition_plan['tdee']
                updates['daily_calorie_target'] = nutrition_plan['daily_calories']
                updates['daily_protein_target_g'] = nutrition_plan['daily_protein_g']
                updates['daily_carbs_target_g'] = nutrition_plan['daily_carbs_g']
                updates['daily_fat_target_g'] = nutrition_plan['daily_fat_g']

                logger.info(f"Calculated nutrition plan for user {user_id}: {nutrition_plan}")

            except Exception as e:
                logger.error(f"Error calculating nutrition plan: {e}")

        # Mark consultation onboarding as complete
        updates['consultation_onboarding_completed'] = True

        if updates:
            self.supabase.table('profiles').update(updates).eq('id', user_id).execute()
            logger.info(f"Updated profile for user {user_id} with consultation data")

    async def _generate_program_from_consultation(
        self,
        session_id: str,
        user_id: str,
        consultation_data: Dict[str, Any]
    ) -> str:
        """Generate AI program from consultation data."""
        # This would integrate with the existing program generation service
        # For now, just link the consultation to the program
        from app.services.program_service import ProgramService

        program_service = ProgramService(self.supabase)

        # Convert consultation data to program generation format
        program_answers = self._convert_consultation_to_program_answers(consultation_data)

        # Create program generation session (will use consultation data)
        # TODO: Implement full integration
        logger.info(f"Would generate program from consultation {session_id} for user {user_id}")

        # For now, return placeholder
        return "program_id_placeholder"

    def _convert_consultation_to_program_answers(
        self,
        consultation_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Convert consultation extraction to program generation format."""
        # Map consultation data to program questions
        # This bridges the consultation system with existing program generation
        answers = {}

        goals = consultation_data.get('goals', {})
        preferences = consultation_data.get('preferences', {})
        measurements = consultation_data.get('measurements', {})

        if goals.get('primary_goal'):
            answers['primary_focus'] = goals['primary_goal']
        if preferences.get('training_frequency'):
            answers['training_frequency'] = preferences['training_frequency']
        if preferences.get('equipment_access'):
            answers['equipment'] = preferences['equipment_access']

        return answers

    def _calculate_duration(self, start_time: str, end_time: Optional[str]) -> int:
        """Calculate duration in minutes between two timestamps."""
        if not end_time:
            end_time = datetime.utcnow().isoformat()

        start = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        end = datetime.fromisoformat(end_time.replace('Z', '+00:00'))

        duration = (end - start).total_seconds() / 60
        return round(duration)

    async def _vectorize_consultation_data(
        self,
        session_id: str,
        user_id: str,
        summary: Dict[str, Any]
    ) -> None:
        """
        Create embeddings from consultation data and store in multimodal_embeddings.

        This enables RAG to retrieve consultation insights during coach chats.

        Vectorizes:
        - Goals (primary goal, target weight, timeline)
        - Preferences (dietary restrictions, equipment, training frequency)
        - Health history (injuries, medical conditions)
        - Measurements (weight, height, age, sex)
        - Full consultation summary as one embedding
        """
        try:
            # 1. Vectorize individual categories
            categories_to_vectorize = {
                "goals": "User's fitness and nutrition goals from consultation",
                "preferences": "User's dietary and training preferences",
                "health_history": "User's health history and medical information",
                "measurements": "User's physical measurements and stats"
            }

            for category, description in categories_to_vectorize.items():
                if category in summary and summary[category]:
                    # Build semantic text for embedding
                    content_text = f"{description}: {json.dumps(summary[category])}"

                    # Generate embedding
                    embedding = await self.embedding_service.embed_text(content_text)

                    # Store in multimodal_embeddings
                    await self.embedding_service.store_embedding(
                        user_id=user_id,
                        embedding=embedding,
                        data_type="structured",
                        source_type="consultation",
                        source_id=session_id,
                        content_text=content_text,
                        metadata={
                            "consultation_category": category,
                            "specialist_type": summary.get("_metadata", {}).get("specialist_type"),
                            "session_id": session_id
                        },
                        confidence_score=0.95
                    )

            # 2. Vectorize full summary as one comprehensive embedding
            full_summary_text = f"""User consultation summary:
Goals: {summary.get('goals', {})}
Preferences: {summary.get('preferences', {})}
Health: {summary.get('health_history', {})}
Measurements: {summary.get('measurements', {})}
Completed: {summary.get('_metadata', {}).get('session_duration_minutes')} minutes
Specialist: {summary.get('_metadata', {}).get('specialist_type')}"""

            full_embedding = await self.embedding_service.embed_text(full_summary_text)

            await self.embedding_service.store_embedding(
                user_id=user_id,
                embedding=full_embedding,
                data_type="structured",
                source_type="consultation",
                source_id=session_id,
                content_text=full_summary_text,
                metadata={
                    "consultation_category": "full_summary",
                    "specialist_type": summary.get("_metadata", {}).get("specialist_type"),
                    "session_id": session_id,
                    "is_complete_summary": True
                },
                confidence_score=1.0
            )

            logger.info(f"Vectorized consultation {session_id} - created {len(categories_to_vectorize) + 1} embeddings")

        except Exception as e:
            logger.error(f"Failed to vectorize consultation data: {e}")
            # Non-critical - don't fail consultation completion

    # =====================================================
    # STATUS CHECK METHODS FOR FRONTEND
    # =====================================================

    async def has_completed_consultation(self, user_id: str) -> bool:
        """
        Check if user has completed any consultation.

        Used by dashboard to show/hide first-time user banner.

        Args:
            user_id: User's UUID

        Returns:
            True if user has completed at least one consultation, False otherwise
        """
        try:
            result = self.supabase.table('consultation_sessions')\
                .select('id')\
                .eq('user_id', user_id)\
                .eq('status', 'completed')\
                .limit(1)\
                .execute()

            has_completed = len(result.data) > 0
            logger.info(f"User {user_id} consultation status: {'completed' if has_completed else 'not completed'}")
            return has_completed

        except Exception as e:
            logger.error(f"Error checking consultation completion: {e}")
            # Default to False on error (safer to show banner than hide it)
            return False

    async def get_active_session(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Get active consultation session if exists.

        Used by consultation page to prevent duplicate sessions.

        Args:
            user_id: User's UUID

        Returns:
            Active session data if exists, None otherwise
        """
        try:
            result = self.supabase.table('consultation_sessions')\
                .select('*')\
                .eq('user_id', user_id)\
                .eq('status', 'active')\
                .order('created_at', desc=True)\
                .limit(1)\
                .execute()

            active_session = result.data[0] if result.data else None

            if active_session:
                logger.info(f"User {user_id} has active consultation session: {active_session['id']}")
            else:
                logger.info(f"User {user_id} has no active consultation session")

            return active_session

        except Exception as e:
            logger.error(f"Error checking active session: {e}")
            return None

    # =====================================================
    # AI COACH TOOL FUNCTIONS
    # =====================================================

    async def get_user_profile_summary(self, user_id: str) -> Dict[str, Any]:
        """
        Get complete user profile from consultations for AI coach tool use.

        This tool allows the AI coach to access:
        - Nutrition targets (BMR, TDEE, calories, macros)
        - Goals (primary goal, target weight, timeline)
        - Preferences (dietary restrictions, equipment)
        - Measurements (weight, height, age, biological sex)
        - Last consultation date

        Args:
            user_id: User's UUID

        Returns:
            Complete profile dictionary with all consultation data
        """
        try:
            # Get user profile
            profile = self.supabase.table('profiles')\
                .select('*')\
                .eq('id', user_id)\
                .single()\
                .execute().data

            if not profile:
                return {"error": "User profile not found"}

            # Get latest consultation summary
            latest_consultation = self.supabase.table('consultation_sessions')\
                .select('id, specialist_type, completed_at')\
                .eq('user_id', user_id)\
                .eq('status', 'completed')\
                .order('completed_at', desc=True)\
                .limit(1)\
                .execute()

            consultation_data = {}
            if latest_consultation.data:
                session_id = latest_consultation.data[0]['id']
                consultation_data = await self.get_consultation_summary(session_id)

            return {
                "nutrition_targets": {
                    "bmr": profile.get('bmr'),
                    "tdee": profile.get('estimated_tdee'),
                    "daily_calories": profile.get('daily_calorie_target'),
                    "daily_protein_g": profile.get('daily_protein_target_g'),
                    "daily_carbs_g": profile.get('daily_carbs_target_g'),
                    "daily_fat_g": profile.get('daily_fat_target_g')
                },
                "measurements": {
                    "current_weight_kg": profile.get('current_weight_kg'),
                    "height_cm": profile.get('height_cm'),
                    "age": profile.get('age'),
                    "biological_sex": profile.get('biological_sex')
                },
                "goals": consultation_data.get('goals', {
                    "primary_goal": profile.get('primary_goal'),
                    "goal_weight_kg": profile.get('goal_weight_kg')
                }),
                "preferences": consultation_data.get('preferences', {
                    "equipment_access": profile.get('available_equipment'),
                    "dietary_restrictions": profile.get('dietary_restrictions')
                }),
                "last_consultation": latest_consultation.data[0] if latest_consultation.data else None
            }

        except Exception as e:
            logger.error(f"Error getting user profile summary: {e}")
            return {"error": str(e)}

    async def get_user_goals(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's stated goals from consultation for AI coach tool use.

        Returns:
        - Primary goal (lose_weight, build_muscle, etc.)
        - Target weight
        - Timeline
        - Specific targets

        Args:
            user_id: User's UUID

        Returns:
            Goals dictionary from most recent consultation
        """
        try:
            # Get latest completed consultation
            latest_session = self.supabase.table('consultation_sessions')\
                .select('id')\
                .eq('user_id', user_id)\
                .eq('status', 'completed')\
                .order('completed_at', desc=True)\
                .limit(1)\
                .execute()

            if not latest_session.data:
                # Fallback to profile
                profile = self.supabase.table('profiles')\
                    .select('primary_goal, goal_weight_kg')\
                    .eq('id', user_id)\
                    .single()\
                    .execute().data

                return {
                    "primary_goal": profile.get('primary_goal'),
                    "goal_weight_kg": profile.get('goal_weight_kg'),
                    "source": "profile"
                }

            # Get goals from consultation
            summary = await self.get_consultation_summary(latest_session.data[0]['id'])
            goals = summary.get('goals', {})
            goals["source"] = "consultation"

            return goals

        except Exception as e:
            logger.error(f"Error getting user goals: {e}")
            return {"error": str(e)}

    async def get_user_preferences(self, user_id: str) -> Dict[str, Any]:
        """
        Get user's dietary and training preferences for AI coach tool use.

        Returns:
        - Dietary restrictions (allergies, vegetarian, etc.)
        - Equipment access (dumbbells, barbell, etc.)
        - Preferred workout time
        - Training frequency
        - Workout environment (home, gym)

        Args:
            user_id: User's UUID

        Returns:
            Preferences dictionary
        """
        try:
            # Get from consultation
            latest_session = self.supabase.table('consultation_sessions')\
                .select('id')\
                .eq('user_id', user_id)\
                .eq('status', 'completed')\
                .order('completed_at', desc=True)\
                .limit(1)\
                .execute()

            preferences = {}

            if latest_session.data:
                summary = await self.get_consultation_summary(latest_session.data[0]['id'])
                preferences = summary.get('preferences', {})
                preferences.update(summary.get('dietary_preferences', {}))

            # Fallback to profile
            profile = self.supabase.table('profiles')\
                .select('available_equipment, dietary_restrictions, training_frequency')\
                .eq('id', user_id)\
                .single()\
                .execute().data

            if profile:
                if not preferences.get('equipment_access'):
                    preferences['equipment_access'] = profile.get('available_equipment', [])
                if not preferences.get('dietary_restrictions'):
                    preferences['dietary_restrictions'] = profile.get('dietary_restrictions', [])
                if not preferences.get('training_frequency'):
                    preferences['training_frequency'] = profile.get('training_frequency')

            return preferences

        except Exception as e:
            logger.error(f"Error getting user preferences: {e}")
            return {"error": str(e)}

    async def get_nutrition_targets_with_progress(
        self,
        user_id: str,
        date: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Get nutrition targets and current progress for date.

        Returns:
        - Targets (calories, protein, carbs, fat)
        - Current logged (from meal_logs)
        - Remaining (targets - current)
        - Percentage complete

        Args:
            user_id: User's UUID
            date: Date in ISO format (defaults to today)

        Returns:
            Nutrition progress dictionary
        """
        try:
            from datetime import date as date_module

            if not date:
                date = date_module.today().isoformat()

            # Get targets from profile
            profile = self.supabase.table('profiles')\
                .select('daily_calorie_target, daily_protein_target_g, daily_carbs_target_g, daily_fat_target_g')\
                .eq('id', user_id)\
                .single()\
                .execute().data

            targets = {
                "calories": profile.get('daily_calorie_target', 0),
                "protein_g": profile.get('daily_protein_target_g', 0),
                "carbs_g": profile.get('daily_carbs_target_g', 0),
                "fat_g": profile.get('daily_fat_target_g', 0)
            }

            # Get logged meals for date
            meals = self.supabase.table('meals')\
                .select('calories, protein_g, carbs_g, fat_g')\
                .eq('user_id', user_id)\
                .gte('logged_at', f"{date}T00:00:00")\
                .lte('logged_at', f"{date}T23:59:59")\
                .execute().data

            # Calculate totals
            current = {
                "calories": sum(m.get('calories', 0) or 0 for m in meals),
                "protein_g": sum(m.get('protein_g', 0) or 0 for m in meals),
                "carbs_g": sum(m.get('carbs_g', 0) or 0 for m in meals),
                "fat_g": sum(m.get('fat_g', 0) or 0 for m in meals)
            }

            # Calculate remaining
            remaining = {
                "calories": max(0, targets["calories"] - current["calories"]),
                "protein_g": max(0, targets["protein_g"] - current["protein_g"]),
                "carbs_g": max(0, targets["carbs_g"] - current["carbs_g"]),
                "fat_g": max(0, targets["fat_g"] - current["fat_g"])
            }

            # Calculate percentage
            percentage = {
                "calories": round((current["calories"] / targets["calories"] * 100) if targets["calories"] > 0 else 0),
                "protein_g": round((current["protein_g"] / targets["protein_g"] * 100) if targets["protein_g"] > 0 else 0),
                "carbs_g": round((current["carbs_g"] / targets["carbs_g"] * 100) if targets["carbs_g"] > 0 else 0),
                "fat_g": round((current["fat_g"] / targets["fat_g"] * 100) if targets["fat_g"] > 0 else 0)
            }

            return {
                "date": date,
                "targets": targets,
                "current": current,
                "remaining": remaining,
                "percentage": percentage,
                "meals_logged": len(meals)
            }

        except Exception as e:
            logger.error(f"Error getting nutrition targets with progress: {e}")
            return {"error": str(e)}

    async def get_todays_recommendations_for_coach(
        self,
        user_id: str
    ) -> Dict[str, Any]:
        """
        Get today's meal and workout recommendations for AI coach tool use.

        Returns:
        - Pending recommendations (breakfast, lunch, dinner, workout)
        - Accepted recommendations
        - Next recommended action with timing

        Args:
            user_id: User's UUID

        Returns:
            Today's recommendations with next action
        """
        try:
            from app.services.daily_recommendation_service import get_recommendation_service

            recommendation_service = get_recommendation_service()

            # Get today's active recommendations
            from datetime import date as date_module
            today = date_module.today().isoformat()

            recommendations = await recommendation_service.get_active_recommendations(
                user_id=user_id,
                date=today
            )

            # Get next action
            next_action = await recommendation_service.suggest_next_action(user_id=user_id)

            return {
                "date": today,
                "total_recommendations": len(recommendations),
                "recommendations": recommendations,
                "next_action": next_action,
                "summary": {
                    "meals": [r for r in recommendations if r.get('recommendation_type') == 'meal'],
                    "workouts": [r for r in recommendations if r.get('recommendation_type') == 'workout'],
                    "other": [r for r in recommendations if r.get('recommendation_type') not in ['meal', 'workout']]
                }
            }

        except Exception as e:
            logger.error(f"Error getting today's recommendations: {e}")
            return {"error": str(e), "recommendations": []}

    # =====================================================
    # CONSULTATION HISTORY & TEMPORAL TRACKING (Feature 8)
    # =====================================================

    async def get_consultation_history(
        self,
        user_id: str,
        specialist_type: Optional[str] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Get all past completed consultations for a user.

        This enables temporal tracking and goal evolution analysis.
        Returns consultations in reverse chronological order (newest first).

        Args:
            user_id: User's UUID
            specialist_type: Optional filter by specialist type
            limit: Maximum number of consultations to return

        Returns:
            List of consultation summaries with metadata and timestamps
        """
        try:
            # Build query
            query = self.supabase.table('consultation_sessions')\
                .select('id, specialist_type, completed_at, created_at, total_messages, progress_percentage')\
                .eq('user_id', user_id)\
                .eq('status', 'completed')\
                .order('completed_at', desc=True)\
                .limit(limit)

            if specialist_type:
                query = query.eq('specialist_type', specialist_type)

            sessions = query.execute().data

            # Get full summary for each session
            history = []
            for session in sessions:
                summary = await self.get_consultation_summary(session['id'])

                # Add temporal metadata
                history.append({
                    'session_id': session['id'],
                    'specialist_type': session['specialist_type'],
                    'completed_at': session['completed_at'],
                    'created_at': session['created_at'],
                    'duration_minutes': summary['_metadata']['session_duration_minutes'],
                    'total_messages': session['total_messages'],
                    'summary': summary
                })

            logger.info(f"Retrieved {len(history)} consultation(s) for user {user_id}")

            return history

        except Exception as e:
            logger.error(f"Error getting consultation history: {e}")
            return []

    async def compare_consultations(
        self,
        session_id_1: str,
        session_id_2: str
    ) -> Dict[str, Any]:
        """
        Compare two consultations to identify changes.

        Useful for tracking goal evolution, preference changes, and measurement progress.

        Args:
            session_id_1: First consultation session ID (older)
            session_id_2: Second consultation session ID (newer)

        Returns:
            Comparison dictionary with changes, additions, removals
        """
        try:
            # Get both summaries
            summary_1 = await self.get_consultation_summary(session_id_1)
            summary_2 = await self.get_consultation_summary(session_id_2)

            # Get session metadata for temporal context
            session_1 = self.supabase.table('consultation_sessions')\
                .select('completed_at, specialist_type')\
                .eq('id', session_id_1)\
                .single()\
                .execute().data

            session_2 = self.supabase.table('consultation_sessions')\
                .select('completed_at, specialist_type')\
                .eq('id', session_id_2)\
                .single()\
                .execute().data

            # Calculate time between consultations
            time_diff = self._calculate_time_between(
                session_1['completed_at'],
                session_2['completed_at']
            )

            # Compare categories
            changes = {}
            all_categories = set(list(summary_1.keys()) + list(summary_2.keys()))
            all_categories.discard('_metadata')

            for category in all_categories:
                data_1 = summary_1.get(category, {})
                data_2 = summary_2.get(category, {})

                category_changes = self._compare_category(data_1, data_2)

                if category_changes['changed'] or category_changes['added'] or category_changes['removed']:
                    changes[category] = category_changes

            return {
                'session_1': {
                    'id': session_id_1,
                    'completed_at': session_1['completed_at'],
                    'specialist_type': session_1['specialist_type']
                },
                'session_2': {
                    'id': session_id_2,
                    'completed_at': session_2['completed_at'],
                    'specialist_type': session_2['specialist_type']
                },
                'time_between': time_diff,
                'changes': changes,
                'has_changes': len(changes) > 0
            }

        except Exception as e:
            logger.error(f"Error comparing consultations: {e}")
            return {"error": str(e)}

    async def get_goal_evolution(
        self,
        user_id: str,
        category: str = 'goals'
    ) -> Dict[str, Any]:
        """
        Track how specific consultation data evolved over time.

        Shows timeline of changes for a specific category (goals, preferences, measurements, etc.)

        Args:
            user_id: User's UUID
            category: Category to track (goals, preferences, measurements, health_history)

        Returns:
            Timeline of category values across all consultations
        """
        try:
            # Get all consultations
            history = await self.get_consultation_history(user_id, limit=50)

            if not history:
                return {
                    "category": category,
                    "timeline": [],
                    "message": "No completed consultations found"
                }

            # Build timeline
            timeline = []
            for consultation in history:
                summary = consultation['summary']
                category_data = summary.get(category, {})

                if category_data:
                    timeline.append({
                        'session_id': consultation['session_id'],
                        'completed_at': consultation['completed_at'],
                        'specialist_type': consultation['specialist_type'],
                        'data': category_data,
                        'time_ago': self._format_time_ago(consultation['completed_at'])
                    })

            # Identify changes between consecutive consultations
            evolution = []
            for i in range(len(timeline) - 1):
                current = timeline[i]
                previous = timeline[i + 1]

                changes = self._compare_category(previous['data'], current['data'])

                if changes['changed'] or changes['added'] or changes['removed']:
                    evolution.append({
                        'from_session': previous['session_id'],
                        'to_session': current['session_id'],
                        'from_date': previous['completed_at'],
                        'to_date': current['completed_at'],
                        'changes': changes,
                        'time_between': self._calculate_time_between(
                            previous['completed_at'],
                            current['completed_at']
                        )
                    })

            return {
                "category": category,
                "timeline": timeline,
                "evolution": evolution,
                "total_consultations": len(timeline),
                "total_changes": len(evolution)
            }

        except Exception as e:
            logger.error(f"Error getting goal evolution: {e}")
            return {"error": str(e)}

    async def format_consultation_timeline(
        self,
        user_id: str,
        limit: int = 5
    ) -> str:
        """
        Format consultation history as human-readable timeline for coach context.

        This is designed to be injected into the coach's system prompt or tool response.

        Args:
            user_id: User's UUID
            limit: Maximum number of consultations to include

        Returns:
            Formatted string with temporal references
        """
        try:
            history = await self.get_consultation_history(user_id, limit=limit)

            if not history:
                return "No consultation history available."

            # Build formatted timeline
            lines = ["=== CONSULTATION HISTORY ==="]

            for i, consultation in enumerate(history):
                time_ago = self._format_time_ago(consultation['completed_at'])
                specialist = consultation['specialist_type'].replace('_', ' ').title()
                summary = consultation['summary']

                lines.append(f"\n{i + 1}. {specialist} Consultation ({time_ago}):")

                # Goals
                if 'goals' in summary:
                    goals = summary['goals']
                    if isinstance(goals, dict):
                        for key, value in goals.items():
                            lines.append(f"   - {key}: {value}")

                # Key measurements
                if 'measurements' in summary:
                    measurements = summary['measurements']
                    if isinstance(measurements, dict):
                        weight = measurements.get('current_weight_kg')
                        if weight:
                            lines.append(f"   - Weight: {weight} kg")

                # Preferences
                if 'preferences' in summary or 'dietary_preferences' in summary:
                    prefs = summary.get('preferences', summary.get('dietary_preferences', {}))
                    if isinstance(prefs, dict) and prefs:
                        lines.append(f"   - Preferences: {list(prefs.keys())}")

            # Add evolution note if multiple consultations
            if len(history) > 1:
                lines.append(f"\nUser has completed {len(history)} consultations.")
                lines.append("Reference past consultations when relevant.")

            return "\n".join(lines)

        except Exception as e:
            logger.error(f"Error formatting consultation timeline: {e}")
            return "Error retrieving consultation history."

    # Helper methods for temporal comparison

    def _compare_category(self, data_1: Dict[str, Any], data_2: Dict[str, Any]) -> Dict[str, Any]:
        """Compare two category dictionaries and identify changes."""
        changed = {}
        added = {}
        removed = {}

        # Check for changes and removals
        for key in data_1:
            if key not in data_2:
                removed[key] = data_1[key]
            elif data_1[key] != data_2[key]:
                changed[key] = {
                    'from': data_1[key],
                    'to': data_2[key]
                }

        # Check for additions
        for key in data_2:
            if key not in data_1:
                added[key] = data_2[key]

        return {
            'changed': changed,
            'added': added,
            'removed': removed
        }

    def _calculate_time_between(self, time_1: str, time_2: str) -> Dict[str, Any]:
        """Calculate time difference between two timestamps."""
        from datetime import datetime

        t1 = datetime.fromisoformat(time_1.replace('Z', '+00:00'))
        t2 = datetime.fromisoformat(time_2.replace('Z', '+00:00'))

        delta = abs(t2 - t1)

        days = delta.days
        months = days // 30
        weeks = days // 7

        return {
            'days': days,
            'weeks': weeks,
            'months': months,
            'human_readable': self._format_time_delta(days)
        }

    def _format_time_ago(self, timestamp: str) -> str:
        """Format timestamp as 'X days/weeks/months ago'."""
        from datetime import datetime

        past = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
        now = datetime.utcnow()

        delta = now - past.replace(tzinfo=None)
        days = delta.days

        return self._format_time_delta(days) + " ago"

    def _format_time_delta(self, days: int) -> str:
        """Format days into human-readable time span."""
        if days == 0:
            return "today"
        elif days == 1:
            return "1 day"
        elif days < 7:
            return f"{days} days"
        elif days < 30:
            weeks = days // 7
            return f"{weeks} week{'s' if weeks > 1 else ''}"
        elif days < 365:
            months = days // 30
            return f"{months} month{'s' if months > 1 else ''}"
        else:
            years = days // 365
            return f"{years} year{'s' if years > 1 else ''}"


# Global instance
_consultation_service: Optional[ConsultationService] = None


def get_consultation_service() -> ConsultationService:
    """Get the global ConsultationService instance."""
    global _consultation_service
    if _consultation_service is None:
        _consultation_service = ConsultationService()
    return _consultation_service
