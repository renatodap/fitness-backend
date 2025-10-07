"""
Pydantic schemas for Unified Coach API (ChatGPT-like interface)

This replaces the old AI Chat + Quick Entry with a single unified "Coach" interface.
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime
from enum import Enum


# =====================================================
# Enums
# =====================================================

class MessageRole(str, Enum):
    """Message role in conversation"""
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"


class MessageType(str, Enum):
    """Message type for routing"""
    CHAT = "chat"
    LOG_PREVIEW = "log_preview"
    LOG_CONFIRMED = "log_confirmed"
    SYSTEM = "system"


class LogType(str, Enum):
    """Type of detected log"""
    MEAL = "meal"
    WORKOUT = "workout"
    ACTIVITY = "activity"
    MEASUREMENT = "measurement"


# =====================================================
# Request Models
# =====================================================

class UnifiedMessageRequest(BaseModel):
    """
    Request to send message to unified Coach.

    Can be:
    - Chat message (question, comment)
    - Log message (meal, workout, measurement)

    LLM automatically detects type and routes accordingly.
    """
    message: str = Field(
        ...,
        min_length=1,
        max_length=5000,
        description="User's message (text, or transcribed from voice)"
    )

    conversation_id: Optional[str] = Field(
        None,
        description="Optional conversation ID to continue existing chat. If None, creates new conversation."
    )

    # Optional multimodal inputs
    has_image: bool = Field(
        False,
        description="Whether user uploaded an image (meal photo, workout photo)"
    )

    has_audio: bool = Field(
        False,
        description="Whether message was transcribed from voice"
    )

    image_urls: List[str] = Field(
        default_factory=list,
        description="Optional image URLs for multimodal processing"
    )

    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError("Message cannot be empty or whitespace only")
        return v.strip()

    class Config:
        json_schema_extra = {
            "example": {
                "message": "I just ate 3 eggs, oatmeal, and a banana for breakfast",
                "conversation_id": None,
                "has_image": False,
                "has_audio": False
            }
        }


class ConfirmLogRequest(BaseModel):
    """
    Request to confirm a detected log.

    User reviews the log preview and confirms to save it.
    """
    conversation_id: str = Field(
        ...,
        description="Conversation ID where log was detected"
    )

    log_data: Dict[str, Any] = Field(
        ...,
        description="The log data to save (meal, workout, measurement)"
    )

    log_type: LogType = Field(
        ...,
        description="Type of log being confirmed"
    )

    user_message_id: str = Field(
        ...,
        description="ID of the user message that triggered log detection"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                "log_type": "meal",
                "user_message_id": "456e7890-e89b-12d3-a456-426614174000",
                "log_data": {
                    "meal_type": "breakfast",
                    "calories": 450,
                    "protein": 35,
                    "carbs": 40,
                    "fats": 15,
                    "foods": ["eggs", "oatmeal", "banana"]
                }
            }
        }


# =====================================================
# Response Models
# =====================================================

class LogPreview(BaseModel):
    """
    Preview of detected log for user confirmation.

    Shows parsed data before saving to database.
    """
    log_type: LogType = Field(..., description="Type of log detected")
    confidence: float = Field(..., ge=0.0, le=1.0, description="AI confidence in detection")

    # Structured data varies by log_type
    data: Dict[str, Any] = Field(
        ...,
        description="Parsed structured data (varies by log_type)"
    )

    # AI reasoning
    reasoning: str = Field(
        ...,
        description="Brief explanation of why this was classified as a log"
    )

    # User-friendly summary
    summary: str = Field(
        ...,
        description="Human-readable summary (e.g., '450 calories, 35g protein')"
    )

    # Validation feedback
    validation: Optional[Dict[str, List[str]]] = Field(
        None,
        description="Validation errors, warnings, and missing critical fields"
    )

    # AI suggestions
    suggestions: List[str] = Field(
        default_factory=list,
        description="Helpful suggestions from AI (e.g., 'Add portion sizes for accuracy')"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "log_type": "meal",
                "confidence": 0.95,
                "data": {
                    "meal_type": "breakfast",
                    "calories": 450,
                    "protein": 35,
                    "carbs": 40,
                    "fats": 15,
                    "foods": ["eggs", "oatmeal", "banana"]
                },
                "reasoning": "Past tense eating with specific foods and implicit quantities",
                "summary": "Breakfast: 450 calories, 35g protein, 40g carbs, 15g fats",
                "validation": {
                    "errors": [],
                    "warnings": ["Some portions were estimated"],
                    "missing_critical": []
                },
                "suggestions": ["Add specific portion sizes for better tracking"]
            }
        }


class RAGContext(BaseModel):
    """Information about RAG context used to generate response"""
    sources_count: int = Field(0, description="Total number of context sources retrieved")
    coach_messages_count: int = Field(0, description="Previous coach messages used")
    quick_entries_count: int = Field(0, description="Quick entry logs used (meals, workouts)")
    similarity_threshold: float = Field(0.7, description="Minimum similarity score used")


class UnifiedMessageResponse(BaseModel):
    """
    Response from unified Coach.

    Can be:
    - Chat response (AI answer to question/comment)
    - Log preview (asking user to confirm detected log)
    """
    success: bool = Field(..., description="Whether request was successful")

    conversation_id: str = Field(..., description="Conversation ID (created if new)")

    message_id: str = Field(..., description="ID of the AI's message")

    # Response type indicator
    is_log_preview: bool = Field(
        False,
        description="If true, this is a log preview requiring confirmation"
    )

    # Chat response (if is_log_preview=False)
    message: Optional[str] = Field(
        None,
        description="AI's chat response (if not a log preview)"
    )

    # Log preview (if is_log_preview=True)
    log_preview: Optional[LogPreview] = Field(
        None,
        description="Log preview data (if is_log_preview=True)"
    )

    # Optional context info
    rag_context: Optional[RAGContext] = Field(
        None,
        description="Information about RAG context used"
    )

    # Cost tracking
    tokens_used: Optional[int] = Field(None, description="Tokens used in generation")
    cost_usd: Optional[float] = Field(None, description="Estimated cost in USD")

    # Error handling
    error: Optional[str] = Field(None, description="Error message if success=False")

    class Config:
        json_schema_extra = {
            "examples": [
                {
                    "success": True,
                    "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                    "message_id": "456e7890-e89b-12d3-a456-426614174000",
                    "is_log_preview": False,
                    "message": "Based on your recent meals, you're hitting your protein target well! Your breakfast this morning had 35g protein, which is perfect for post-workout. Keep it up!",
                    "rag_context": {
                        "sources_count": 15,
                        "coach_messages_count": 5,
                        "quick_entries_count": 10
                    },
                    "tokens_used": 450,
                    "cost_usd": 0.00135
                },
                {
                    "success": True,
                    "conversation_id": "123e4567-e89b-12d3-a456-426614174000",
                    "message_id": "789e0123-e89b-12d3-a456-426614174000",
                    "is_log_preview": True,
                    "log_preview": {
                        "log_type": "meal",
                        "confidence": 0.95,
                        "data": {
                            "meal_type": "breakfast",
                            "calories": 450,
                            "protein": 35,
                            "carbs": 40,
                            "fats": 15,
                            "foods": ["eggs", "oatmeal", "banana"]
                        },
                        "reasoning": "Past tense eating with specific foods",
                        "summary": "Breakfast: 450 cal, 35g protein"
                    }
                }
            ]
        }


class ConfirmLogResponse(BaseModel):
    """Response after confirming a log"""
    success: bool = Field(..., description="Whether log was saved successfully")

    log_id: Optional[str] = Field(None, description="ID of the created log")

    quick_entry_log_id: Optional[str] = Field(
        None,
        description="ID of the quick_entry_logs record (audit trail)"
    )

    system_message_id: str = Field(
        ...,
        description="ID of the system message added to conversation"
    )

    system_message: str = Field(
        ...,
        description="Success message shown in chat (e.g., '✅ Meal logged!')"
    )

    error: Optional[str] = Field(None, description="Error message if success=False")


# =====================================================
# Conversation History Models
# =====================================================

class MessageSummary(BaseModel):
    """Summary of a single message in conversation"""
    id: str = Field(..., description="Message ID")
    role: MessageRole = Field(..., description="Message role")
    content: str = Field(..., description="Message content")
    message_type: MessageType = Field(..., description="Message type")
    created_at: datetime = Field(..., description="When message was created")

    # Optional metadata
    quick_entry_log_id: Optional[str] = Field(
        None,
        description="Link to structured log (if this was a confirmed log)"
    )

    is_vectorized: bool = Field(False, description="Whether this message is vectorized for RAG")


class ConversationSummary(BaseModel):
    """Summary of a conversation for list view"""
    id: str = Field(..., description="Conversation ID")
    title: Optional[str] = Field(None, description="Conversation title (from first message)")
    message_count: int = Field(0, description="Number of messages in conversation")
    last_message_at: datetime = Field(..., description="When last message was sent")
    created_at: datetime = Field(..., description="When conversation was created")
    archived: bool = Field(False, description="Whether conversation is archived")

    # Preview of last message
    last_message_preview: Optional[str] = Field(
        None,
        max_length=100,
        description="Preview of last message (truncated)"
    )


class ConversationListResponse(BaseModel):
    """Response for GET /conversations"""
    success: bool = Field(..., description="Whether request was successful")
    conversations: List[ConversationSummary] = Field(
        default_factory=list,
        description="List of conversations"
    )
    total_count: int = Field(0, description="Total number of conversations")
    has_more: bool = Field(False, description="Whether there are more conversations to load")


class MessageListResponse(BaseModel):
    """Response for GET /conversations/{id}/messages"""
    success: bool = Field(..., description="Whether request was successful")
    conversation_id: str = Field(..., description="Conversation ID")
    messages: List[MessageSummary] = Field(
        default_factory=list,
        description="List of messages in conversation"
    )
    total_count: int = Field(0, description="Total number of messages in conversation")
    has_more: bool = Field(False, description="Whether there are more messages to load")
