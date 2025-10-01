"""
Service for AI-generated personalized fitness and nutrition programs.
"""
import json
from datetime import date, datetime, timedelta
from typing import Dict, List, Optional, Any
from uuid import UUID
import openai
from app.config import settings
from app.services.context_builder import ContextBuilder

openai.api_key = settings.OPENAI_API_KEY


class ProgramService:
    """Service for generating personalized 3-month programs with AI."""

    def __init__(self, supabase_client):
        self.supabase = supabase_client
        self.context_builder = ContextBuilder(supabase_client)

    async def get_user_profile_for_generation(self, user_id: str) -> Dict[str, Any]:
        """
        Fetch comprehensive user data for program generation.

        Returns complete user context including:
        - Profile information
        - Goals
        - Recent workout history
        - Recent nutrition data
        - Preferences and limitations
        """
        # Get profile
        profile_response = self.supabase.table('profiles').select('*').eq('id', user_id).single().execute()
        profile = profile_response.data if profile_response.data else {}

        # Get active goals
        goals_response = self.supabase.table('user_goals').select('*').eq('user_id', user_id).eq('is_active', True).execute()
        goals = goals_response.data if goals_response.data else []

        # Get recent workouts (last 30 days)
        thirty_days_ago = (datetime.now() - timedelta(days=30)).isoformat()
        workouts_response = self.supabase.table('workout_completions')\
            .select('*')\
            .eq('user_id', user_id)\
            .gte('completed_at', thirty_days_ago)\
            .order('completed_at', desc=True)\
            .limit(20)\
            .execute()
        recent_workouts = workouts_response.data if workouts_response.data else []

        # Get recent meals (last 14 days)
        fourteen_days_ago = (datetime.now() - timedelta(days=14)).isoformat()
        meals_response = self.supabase.table('meal_logs')\
            .select('*')\
            .eq('user_id', user_id)\
            .gte('logged_at', fourteen_days_ago)\
            .order('logged_at', desc=True)\
            .limit(30)\
            .execute()
        recent_meals = meals_response.data if meals_response.data else []

        # Get activities (Strava/Garmin data)
        activities_response = self.supabase.table('activities')\
            .select('*')\
            .eq('user_id', user_id)\
            .gte('start_date', thirty_days_ago)\
            .order('start_date', desc=True)\
            .limit(20)\
            .execute()
        recent_activities = activities_response.data if activities_response.data else []

        return {
            'profile': profile,
            'goals': goals,
            'recent_workouts': recent_workouts,
            'recent_meals': recent_meals,
            'recent_activities': recent_activities,
            'fetched_at': datetime.now().isoformat()
        }

    async def generate_program_questions(self, user_id: str, session_id: Optional[str] = None) -> Dict[str, Any]:
        """
        Generate 2-3 personalized questions for the user based on their profile.

        The AI analyzes the user's data and creates relevant questions with
        2-3 button options each to refine the program generation.
        """
        # Get user data
        user_data = await self.get_user_profile_for_generation(user_id)

        # Create or update generation session
        if not session_id:
            session_response = self.supabase.table('program_generation_sessions').insert({
                'user_id': user_id,
                'status': 'in_progress',
                'user_profile_snapshot': user_data
            }).execute()
            session_id = session_response.data[0]['id']

        # Build context summary for AI
        context_summary = self._build_context_summary(user_data)

        # Generate questions using OpenAI
        system_prompt = """You are an expert fitness and nutrition coach creating a personalized 3-month program.

Your task is to generate 2-3 targeted questions to understand the user's preferences for their program.
Each question should have 2-3 clear button options.

Consider:
- User's current fitness level and experience
- Their goals and timeline
- Available equipment and time
- Dietary preferences and restrictions
- Past workout patterns

Generate questions that will help you create the PERFECT program for them.

IMPORTANT MEDICAL/SAFETY GUIDELINES:
- Never recommend unsafe practices
- Account for any mentioned injuries or health conditions
- Ensure proper progression and recovery
- Follow evidence-based fitness and nutrition science
- Recommend medical consultation when appropriate

Return ONLY a JSON object with this structure:
{
  "questions": [
    {
      "id": "q1",
      "question": "What's your primary focus for the next 3 months?",
      "options": [
        {"value": "strength", "label": "Build Strength"},
        {"value": "endurance", "label": "Improve Endurance"},
        {"value": "body_comp", "label": "Transform Body Composition"}
      ]
    }
  ]
}"""

        user_prompt = f"""Based on this user's data, generate 2-3 personalized questions:

{context_summary}

Generate questions that will help create the best possible program for THIS specific user."""

        try:
            response = openai.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            questions_data = json.loads(response.choices[0].message.content)

            # Update session with questions
            self.supabase.table('program_generation_sessions').update({
                'questions': questions_data.get('questions', []),
                'total_steps': len(questions_data.get('questions', [])),
                'updated_at': datetime.now().isoformat()
            }).eq('id', session_id).execute()

            return {
                'session_id': session_id,
                'questions': questions_data.get('questions', []),
                'user_context_summary': context_summary
            }

        except Exception as e:
            print(f"Error generating questions: {e}")
            # Return default questions if AI fails
            return {
                'session_id': session_id,
                'questions': self._get_default_questions(),
                'user_context_summary': context_summary
            }

    async def generate_full_program(
        self,
        user_id: str,
        session_id: str,
        answers: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """
        Generate complete 3-month program based on user data and answers.

        Creates:
        - 84 days of programming (12 weeks)
        - Daily meal plans (breakfast, lunch, dinner, snacks, pre/post workout)
        - Daily workout schedules (strength, cardio, sports, flexibility, rest)
        - Proper periodization and progression
        - Medical safety and nutrition guidelines followed
        """
        # Get session and user data
        session_response = self.supabase.table('program_generation_sessions')\
            .select('*')\
            .eq('id', session_id)\
            .single()\
            .execute()
        session = session_response.data

        user_data = session.get('user_profile_snapshot', {})

        # Build comprehensive prompt
        context_summary = self._build_context_summary(user_data)
        answers_summary = self._build_answers_summary(session.get('questions', []), answers)

        system_prompt = """You are an expert fitness coach and nutritionist creating a comprehensive 3-month personalized program.

You must create a complete, day-by-day program including:
1. **Workouts**: Strength training, cardio, sports, flexibility, active recovery
2. **Meal Plans**: Breakfast, lunch, dinner, snacks, pre/post-workout meals
3. **Proper Periodization**: Progressive overload, deload weeks, recovery
4. **Nutrition Strategy**: Calorie and macro targets based on goals

CRITICAL REQUIREMENTS:
- Follow medical safety guidelines
- Evidence-based fitness programming
- Proper nutrition science (not fad diets)
- Account for injuries/limitations
- Ensure adequate recovery
- Progressive overload with proper progression
- Realistic and sustainable

Return a JSON object with this structure:
{
  "program": {
    "name": "12-Week Transformation Program",
    "description": "Comprehensive program tailored to your goals",
    "duration_weeks": 12,
    "difficulty_level": "intermediate",
    "primary_focus": ["strength", "muscle_gain"],
    "dietary_approach": "high_protein_balanced"
  },
  "weeks": [
    {
      "week_number": 1,
      "focus": "Foundation & Assessment",
      "days": [
        {
          "day_number": 1,
          "day_of_week": "monday",
          "day_name": "Upper Body Strength",
          "day_focus": "strength",
          "meals": [
            {
              "meal_type": "breakfast",
              "meal_time": "07:00",
              "name": "High Protein Oatmeal Bowl",
              "description": "Oats with protein powder, berries, almonds",
              "recipe_instructions": "1. Cook oats...",
              "preparation_time_minutes": 10,
              "foods": [
                {"food_name": "Rolled oats", "quantity": 80, "unit": "g"},
                {"food_name": "Whey protein", "quantity": 30, "unit": "g"}
              ],
              "total_calories": 450,
              "total_protein_g": 35,
              "total_carbs_g": 55,
              "total_fat_g": 10,
              "meal_tags": ["quick", "high_protein"],
              "notes": "Great pre-workout meal"
            }
          ],
          "workouts": [
            {
              "workout_type": "strength",
              "workout_subtype": "lifting",
              "name": "Upper Body Push Focus",
              "description": "Chest, shoulders, triceps",
              "duration_minutes": 60,
              "intensity": "moderate",
              "target_rpe": 7,
              "exercises": [
                {
                  "exercise_name": "Barbell Bench Press",
                  "sets": 4,
                  "reps": "8-10",
                  "rest_seconds": 90,
                  "notes": "Focus on control"
                }
              ],
              "equipment_needed": ["barbell", "bench"],
              "warmup_notes": "5 min cardio, dynamic stretches",
              "cooldown_notes": "5 min stretching"
            }
          ]
        }
      ]
    }
  ]
}

Generate ALL 12 weeks with ALL 84 days. Be comprehensive and detailed."""

        user_prompt = f"""Create a complete 3-month program for this user:

USER DATA:
{context_summary}

USER ANSWERS:
{answers_summary}

Generate the COMPLETE program with all 84 days of meals and workouts."""

        try:
            # This is a large generation, may need to split or use larger context
            response = openai.chat.completions.create(
                model="gpt-4o",  # Use more capable model for this
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                temperature=0.7,
                response_format={"type": "json_object"}
            )

            program_data = json.loads(response.choices[0].message.content)

            # Save program to database
            program_id = await self._save_program_to_database(
                user_id=user_id,
                program_data=program_data,
                generation_context=user_data,
                questions_answers=answers
            )

            # Update session
            self.supabase.table('program_generation_sessions').update({
                'status': 'completed',
                'generated_program_id': program_id,
                'answers': answers,
                'completed_at': datetime.now().isoformat()
            }).eq('id', session_id).execute()

            return {
                'success': True,
                'program_id': program_id,
                'program_summary': program_data.get('program', {})
            }

        except Exception as e:
            print(f"Error generating program: {e}")
            raise Exception(f"Failed to generate program: {str(e)}")

    async def _save_program_to_database(
        self,
        user_id: str,
        program_data: Dict[str, Any],
        generation_context: Dict[str, Any],
        questions_answers: List[Dict[str, str]]
    ) -> str:
        """Save generated program to database."""
        program_info = program_data.get('program', {})
        weeks = program_data.get('weeks', [])

        # Calculate dates
        start_date = date.today()
        end_date = start_date + timedelta(weeks=program_info.get('duration_weeks', 12))

        # Create program
        program_response = self.supabase.table('ai_generated_programs').insert({
            'user_id': user_id,
            'name': program_info.get('name', '12-Week Custom Program'),
            'description': program_info.get('description', ''),
            'duration_weeks': program_info.get('duration_weeks', 12),
            'total_days': program_info.get('duration_weeks', 12) * 7,
            'start_date': start_date.isoformat(),
            'end_date': end_date.isoformat(),
            'difficulty_level': program_info.get('difficulty_level', 'intermediate'),
            'primary_focus': program_info.get('primary_focus', []),
            'equipment_needed': program_info.get('equipment_needed', []),
            'dietary_approach': program_info.get('dietary_approach', 'balanced'),
            'generation_context': generation_context,
            'questions_answers': questions_answers,
            'is_active': True,
            'status': 'active'
        }).execute()

        program_id = program_response.data[0]['id']

        # Save all days, meals, and workouts
        day_counter = 1
        for week in weeks:
            for day_data in week.get('days', []):
                # Create day
                day_response = self.supabase.table('ai_program_days').insert({
                    'program_id': program_id,
                    'day_number': day_counter,
                    'day_date': (start_date + timedelta(days=day_counter - 1)).isoformat(),
                    'day_of_week': day_data.get('day_of_week'),
                    'day_name': day_data.get('day_name'),
                    'day_focus': day_data.get('day_focus')
                }).execute()

                day_id = day_response.data[0]['id']

                # Save meals
                for meal_data in day_data.get('meals', []):
                    self.supabase.table('ai_program_meals').insert({
                        'program_day_id': day_id,
                        'program_id': program_id,
                        'meal_type': meal_data.get('meal_type'),
                        'meal_time': meal_data.get('meal_time'),
                        'name': meal_data.get('name'),
                        'description': meal_data.get('description'),
                        'recipe_instructions': meal_data.get('recipe_instructions'),
                        'preparation_time_minutes': meal_data.get('preparation_time_minutes'),
                        'foods': meal_data.get('foods', []),
                        'total_calories': meal_data.get('total_calories'),
                        'total_protein_g': meal_data.get('total_protein_g'),
                        'total_carbs_g': meal_data.get('total_carbs_g'),
                        'total_fat_g': meal_data.get('total_fat_g'),
                        'meal_tags': meal_data.get('meal_tags', []),
                        'notes': meal_data.get('notes')
                    }).execute()

                # Save workouts
                for workout_data in day_data.get('workouts', []):
                    self.supabase.table('ai_program_workouts').insert({
                        'program_day_id': day_id,
                        'program_id': program_id,
                        'workout_type': workout_data.get('workout_type'),
                        'workout_subtype': workout_data.get('workout_subtype'),
                        'name': workout_data.get('name'),
                        'description': workout_data.get('description'),
                        'duration_minutes': workout_data.get('duration_minutes'),
                        'intensity': workout_data.get('intensity'),
                        'target_rpe': workout_data.get('target_rpe'),
                        'exercises': workout_data.get('exercises', []),
                        'workout_details': workout_data.get('workout_details', {}),
                        'equipment_needed': workout_data.get('equipment_needed', []),
                        'warmup_notes': workout_data.get('warmup_notes'),
                        'cooldown_notes': workout_data.get('cooldown_notes'),
                        'notes': workout_data.get('notes')
                    }).execute()

                day_counter += 1

        # Set as user's active program
        self.supabase.table('user_active_programs').insert({
            'user_id': user_id,
            'program_id': program_id,
            'current_day': 1
        }, upsert=True).execute()

        return program_id

    def _build_context_summary(self, user_data: Dict[str, Any]) -> str:
        """Build readable summary of user data."""
        profile = user_data.get('profile', {})
        goals = user_data.get('goals', [])

        summary = f"""PROFILE:
- Name: {profile.get('full_name', 'Not provided')}
- Age: {profile.get('age', 'Not provided')}
- Experience Level: {profile.get('experience_level', 'beginner')}
- Primary Goal: {profile.get('primary_goal', 'Not specified')}
- Weekly Hours Available: {profile.get('weekly_hours', 'Not specified')}
- Equipment Access: {profile.get('equipment_access', 'Not specified')}
- Dietary Preferences: {profile.get('dietary_preferences', 'Not specified')}
- Health Conditions: {profile.get('health_conditions', 'None specified')}

ACTIVE GOALS:
{chr(10).join([f"- {g.get('goal_description')} (Target: {g.get('target_date', 'No deadline')})" for g in goals]) if goals else '- No active goals'}

RECENT ACTIVITY:
- Workouts in last 30 days: {len(user_data.get('recent_workouts', []))}
- Meals logged in last 14 days: {len(user_data.get('recent_meals', []))}
- Connected device activities: {len(user_data.get('recent_activities', []))}
"""
        return summary

    def _build_answers_summary(self, questions: List[Dict], answers: List[Dict]) -> str:
        """Build readable summary of Q&A."""
        summary = []
        for i, (question, answer) in enumerate(zip(questions, answers)):
            q_text = question.get('question', '')
            a_value = answer.get('value', '')
            a_label = next((opt['label'] for opt in question.get('options', []) if opt['value'] == a_value), a_value)
            summary.append(f"Q{i+1}: {q_text}\nA{i+1}: {a_label}\n")
        return '\n'.join(summary)

    def _get_default_questions(self) -> List[Dict]:
        """Default fallback questions if AI generation fails."""
        return [
            {
                "id": "q1",
                "question": "What's your primary focus for the next 3 months?",
                "options": [
                    {"value": "strength", "label": "Build Strength"},
                    {"value": "muscle_gain", "label": "Gain Muscle"},
                    {"value": "fat_loss", "label": "Lose Fat"}
                ]
            },
            {
                "id": "q2",
                "question": "How many days per week can you train?",
                "options": [
                    {"value": "3_days", "label": "3 Days"},
                    {"value": "4_days", "label": "4 Days"},
                    {"value": "5_days", "label": "5-6 Days"}
                ]
            },
            {
                "id": "q3",
                "question": "What's your meal prep preference?",
                "options": [
                    {"value": "simple_quick", "label": "Simple & Quick"},
                    {"value": "meal_prep", "label": "Batch Meal Prep"},
                    {"value": "variety", "label": "Maximum Variety"}
                ]
            }
        ]
