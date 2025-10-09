from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import date, datetime

from app.services.program_service import ProgramService
from app.services.supabase_service import get_service_client
from app.api.middleware.auth import get_current_user
from app.api.middleware.rate_limit import program_generation_rate_limit

router = APIRouter(prefix="/programs", tags=["AI Programs"])


# Request/Response Models
class StartProgramGenerationRequest(BaseModel):
    """Request to start program generation"""
    pass


class ProgramQuestion(BaseModel):
    """A question with button options"""
    question: str
    options: List[str]


class StartProgramGenerationResponse(BaseModel):
    """Response with generated questions"""
    session_id: str
    questions: List[ProgramQuestion]


class QuestionAnswer(BaseModel):
    """User's answer to a question"""
    question: str
    answer: str


class CompleteProgramGenerationRequest(BaseModel):
    """Request to complete program generation with answers"""
    session_id: str
    answers: List[QuestionAnswer]
    event_id: Optional[str] = Field(None, description="Optional event ID to periodize program around")


class CompleteProgramGenerationResponse(BaseModel):
    """Response after program generation"""
    program_id: str
    message: str
    total_days: int
    start_date: str


class MealInfo(BaseModel):
    """Meal information"""
    id: str
    meal_type: str
    meal_name: str
    foods: List[Dict[str, Any]]
    calories: Optional[float]
    protein: Optional[float]
    carbs: Optional[float]
    fats: Optional[float]
    instructions: Optional[str]
    prep_time_minutes: Optional[int]
    is_completed: bool


class WorkoutInfo(BaseModel):
    """Workout information"""
    id: str
    workout_type: str
    workout_name: str
    exercises: List[Dict[str, Any]]
    duration_minutes: Optional[int]
    intensity: Optional[str]
    notes: Optional[str]
    is_completed: bool


class DayInfo(BaseModel):
    """Single day information"""
    day_number: int
    day_date: date
    day_name: str
    notes: Optional[str]
    is_completed: bool
    meals: List[MealInfo]
    workouts: List[WorkoutInfo]


class ActiveProgramResponse(BaseModel):
    """Active program response"""
    program_id: str
    current_day: int
    total_days: int
    start_date: date
    end_date: date
    duration_weeks: int
    generation_context: Optional[Dict[str, Any]]


class CalendarDayInfo(BaseModel):
    """Calendar day information"""
    day_number: int
    day_date: date
    day_name: str
    is_completed: bool
    meal_count: int
    workout_count: int
    completed_meals: int
    completed_workouts: int


class CalendarResponse(BaseModel):
    """Calendar view response"""
    program_id: str
    days: List[CalendarDayInfo]


class MarkCompletedRequest(BaseModel):
    """Request to mark item as completed"""
    is_completed: bool


# Endpoints
@router.post("/generate/start", response_model=StartProgramGenerationResponse)
@program_generation_rate_limit()
async def start_program_generation(
    request: StartProgramGenerationRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Start program generation process.
    Returns personalized questions for the user to answer.

    REQUIRES: User must have completed consultation first.
    """
    try:
        user_id = current_user.get("user_id") or current_user.get("id")

        # CONSULTATION REQUIREMENT CHECK
        from app.services.consultation_service import get_consultation_service
        consultation_service = get_consultation_service()

        has_completed_consultation = await consultation_service.has_completed_consultation(user_id)

        if not has_completed_consultation:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail={
                    "error": "consultation_required",
                    "message": "Complete a consultation before generating your personalized program. This helps us understand your goals, equipment, injuries, and preferences.",
                    "action": "redirect_to_consultation",
                    "consultation_url": "/consultation"
                }
            )

        supabase = get_service_client()
        program_service = ProgramService(supabase)
        result = await program_service.generate_program_questions(
            user_id=user_id
        )

        if not result or "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Failed to generate questions")
            )

        # Format questions
        questions = [
            ProgramQuestion(
                question=q["question"],
                options=q["options"]
            )
            for q in result["questions"]
        ]

        return StartProgramGenerationResponse(
            session_id=result["session_id"],
            questions=questions
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error starting program generation: {str(e)}"
        )


@router.post("/generate/complete", response_model=CompleteProgramGenerationResponse)
@program_generation_rate_limit()
async def complete_program_generation(
    request: CompleteProgramGenerationRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Complete program generation with user's answers.
    Generates full 12-week program and saves to database.

    Optionally provide event_id to generate an event-specific program
    that periodizes training to peak at the event date.
    """
    try:
        supabase = get_service_client()
        program_service = ProgramService(supabase)

        # Convert answers to dict format
        answers = [
            {
                "question": ans.question,
                "answer": ans.answer
            }
            for ans in request.answers
        ]

        result = await program_service.generate_full_program(
            user_id=current_user["id"],
            session_id=request.session_id,
            answers=answers,
            event_id=request.event_id  # Pass optional event_id
        )

        if not result or "error" in result:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=result.get("error", "Failed to generate program")
            )

        return CompleteProgramGenerationResponse(
            program_id=result["program_id"],
            message="Program generated successfully",
            total_days=result["total_days"],
            start_date=result["start_date"]
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error completing program generation: {str(e)}"
        )


@router.get("/active", response_model=Optional[ActiveProgramResponse])
async def get_active_program(
    current_user: dict = Depends(get_current_user)
):
    """
    Get user's currently active program.
    Returns None if no active program.
    """
    try:
        supabase = get_service_client()
        program_service = ProgramService(supabase)

        # Query active program
        result = await program_service.supabase.table("user_active_programs")\
            .select("*, ai_generated_programs(*)")\
            .eq("user_id", current_user["id"])\
            .eq("is_active", True)\
            .single()\
            .execute()

        if not result.data:
            return None

        program = result.data["ai_generated_programs"]
        active = result.data

        return ActiveProgramResponse(
            program_id=program["id"],
            current_day=active["current_day"],
            total_days=program["total_days"],
            start_date=program["start_date"],
            end_date=program["end_date"],
            duration_weeks=program["duration_weeks"],
            generation_context=program.get("generation_context")
        )

    except Exception:
        # Return None if no active program found
        return None


@router.get("/{program_id}/day/{day_number}", response_model=DayInfo)
async def get_program_day(
    program_id: str,
    day_number: int,
    current_user: dict = Depends(get_current_user)
):
    """
    Get specific day's meals and workouts.
    """
    try:
        supabase = get_service_client()
        program_service = ProgramService(supabase)

        # Verify program belongs to user
        program_result = await program_service.supabase.table("ai_generated_programs")\
            .select("id")\
            .eq("id", program_id)\
            .eq("user_id", current_user["id"])\
            .single()\
            .execute()

        if not program_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Program not found"
            )

        # Get day
        day_result = await program_service.supabase.table("ai_program_days")\
            .select("*")\
            .eq("program_id", program_id)\
            .eq("day_number", day_number)\
            .single()\
            .execute()

        if not day_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Day not found"
            )

        day = day_result.data

        # Get meals for this day
        meals_result = await program_service.supabase.table("ai_program_meals")\
            .select("*")\
            .eq("day_id", day["id"])\
            .order("meal_type")\
            .execute()

        # Get workouts for this day
        workouts_result = await program_service.supabase.table("ai_program_workouts")\
            .select("*")\
            .eq("day_id", day["id"])\
            .order("workout_type")\
            .execute()

        # Format meals
        meals = [
            MealInfo(
                id=meal["id"],
                meal_type=meal["meal_type"],
                meal_name=meal["meal_name"],
                foods=meal["foods"],
                calories=meal.get("total_calories"),
                protein=meal.get("total_protein"),
                carbs=meal.get("total_carbs"),
                fats=meal.get("total_fats"),
                instructions=meal.get("instructions"),
                prep_time_minutes=meal.get("prep_time_minutes"),
                is_completed=meal.get("is_completed", False)
            )
            for meal in meals_result.data or []
        ]

        # Format workouts
        workouts = [
            WorkoutInfo(
                id=workout["id"],
                workout_type=workout["workout_type"],
                workout_name=workout["workout_name"],
                exercises=workout["exercises"],
                duration_minutes=workout.get("duration_minutes"),
                intensity=workout.get("intensity"),
                notes=workout.get("notes"),
                is_completed=workout.get("is_completed", False)
            )
            for workout in workouts_result.data or []
        ]

        return DayInfo(
            day_number=day["day_number"],
            day_date=day["day_date"],
            day_name=day["day_name"],
            notes=day.get("notes"),
            is_completed=day.get("is_completed", False),
            meals=meals,
            workouts=workouts
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching program day: {str(e)}"
        )


@router.get("/{program_id}/calendar", response_model=CalendarResponse)
async def get_program_calendar(
    program_id: str,
    start_day: Optional[int] = 1,
    end_day: Optional[int] = 84,
    current_user: dict = Depends(get_current_user)
):
    """
    Get calendar data for program.
    Optionally filter by day range for weekly/monthly views.
    """
    try:
        supabase = get_service_client()
        program_service = ProgramService(supabase)

        # Verify program belongs to user
        program_result = await program_service.supabase.table("ai_generated_programs")\
            .select("id")\
            .eq("id", program_id)\
            .eq("user_id", current_user["id"])\
            .single()\
            .execute()

        if not program_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Program not found"
            )

        # Get days with meal and workout counts
        days_result = await program_service.supabase.rpc(
            "get_program_calendar_data",
            {
                "p_program_id": program_id,
                "p_start_day": start_day,
                "p_end_day": end_day
            }
        ).execute()

        # If RPC function doesn't exist, fall back to manual query
        if not days_result.data or "error" in (days_result.data or {}):
            # Get days
            days_result = await program_service.supabase.table("ai_program_days")\
                .select("*")\
                .eq("program_id", program_id)\
                .gte("day_number", start_day)\
                .lte("day_number", end_day)\
                .order("day_number")\
                .execute()

            days = []
            for day in days_result.data or []:
                # Get meal counts
                meals_result = await program_service.supabase.table("ai_program_meals")\
                    .select("id, is_completed", count="exact")\
                    .eq("day_id", day["id"])\
                    .execute()

                # Get workout counts
                workouts_result = await program_service.supabase.table("ai_program_workouts")\
                    .select("id, is_completed", count="exact")\
                    .eq("day_id", day["id"])\
                    .execute()

                meal_count = len(meals_result.data or [])
                workout_count = len(workouts_result.data or [])
                completed_meals = sum(1 for m in (meals_result.data or []) if m.get("is_completed"))
                completed_workouts = sum(1 for w in (workouts_result.data or []) if w.get("is_completed"))

                days.append(CalendarDayInfo(
                    day_number=day["day_number"],
                    day_date=day["day_date"],
                    day_name=day["day_name"],
                    is_completed=day.get("is_completed", False),
                    meal_count=meal_count,
                    workout_count=workout_count,
                    completed_meals=completed_meals,
                    completed_workouts=completed_workouts
                ))
        else:
            # Format RPC results
            days = [
                CalendarDayInfo(
                    day_number=d["day_number"],
                    day_date=d["day_date"],
                    day_name=d["day_name"],
                    is_completed=d["is_completed"],
                    meal_count=d["meal_count"],
                    workout_count=d["workout_count"],
                    completed_meals=d["completed_meals"],
                    completed_workouts=d["completed_workouts"]
                )
                for d in days_result.data or []
            ]

        return CalendarResponse(
            program_id=program_id,
            days=days
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error fetching calendar: {str(e)}"
        )


@router.patch("/meals/{meal_id}/complete")
async def mark_meal_completed(
    meal_id: str,
    request: MarkCompletedRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Mark a meal as completed/uncompleted.
    """
    try:
        supabase = get_service_client()
        program_service = ProgramService(supabase)

        # Verify meal belongs to user's program
        meal_result = await program_service.supabase.table("ai_program_meals")\
            .select("*, ai_program_days(*, ai_generated_programs(user_id))")\
            .eq("id", meal_id)\
            .single()\
            .execute()

        if not meal_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Meal not found"
            )

        if meal_result.data["ai_program_days"]["ai_generated_programs"]["user_id"] != current_user["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        # Update meal
        update_result = await program_service.supabase.table("ai_program_meals")\
            .update({
                "is_completed": request.is_completed,
                "completed_at": datetime.utcnow().isoformat() if request.is_completed else None
            })\
            .eq("id", meal_id)\
            .execute()

        return {"message": "Meal updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating meal: {str(e)}"
        )


@router.patch("/workouts/{workout_id}/complete")
async def mark_workout_completed(
    workout_id: str,
    request: MarkCompletedRequest,
    current_user: dict = Depends(get_current_user)
):
    """
    Mark a workout as completed/uncompleted.
    """
    try:
        supabase = get_service_client()
        program_service = ProgramService(supabase)

        # Verify workout belongs to user's program
        workout_result = await program_service.supabase.table("ai_program_workouts")\
            .select("*, ai_program_days(*, ai_generated_programs(user_id))")\
            .eq("id", workout_id)\
            .single()\
            .execute()

        if not workout_result.data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Workout not found"
            )

        if workout_result.data["ai_program_days"]["ai_generated_programs"]["user_id"] != current_user["id"]:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied"
            )

        # Update workout
        update_result = await program_service.supabase.table("ai_program_workouts")\
            .update({
                "is_completed": request.is_completed,
                "completed_at": datetime.utcnow().isoformat() if request.is_completed else None
            })\
            .eq("id", workout_id)\
            .execute()

        return {"message": "Workout updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error updating workout: {str(e)}"
        )
