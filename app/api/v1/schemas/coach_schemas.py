"""
Pydantic schemas for Coach Chat API
Following TDD: These are the interface definitions
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from datetime import datetime


class ChatMessage(BaseModel):
    """Individual message in a conversation"""
    role: str = Field(..., description="Message role: 'user' or 'assistant'")
    content: str = Field(..., description="Message content")
    timestamp: datetime = Field(default_factory=datetime.utcnow)

    @validator('role')
    def validate_role(cls, v):
        if v not in ['user', 'assistant', 'system']:
            raise ValueError("Role must be 'user', 'assistant', or 'system'")
        return v


class ChatRequest(BaseModel):
    """Request payload for chat endpoint"""
    coach_type: str = Field(..., description="Type of coach: 'trainer' or 'nutritionist'")
    message: str = Field(..., min_length=1, max_length=1000, description="User's message")
    conversation_id: Optional[str] = Field(None, description="Optional conversation ID to continue")

    @validator('coach_type')
    def validate_coach_type(cls, v):
        if v not in ['trainer', 'nutritionist']:
            raise ValueError("Coach type must be 'trainer' or 'nutritionist'")
        return v

    @validator('message')
    def validate_message(cls, v):
        if not v.strip():
            raise ValueError("Message cannot be empty or whitespace only")
        return v.strip()


class ContextInfo(BaseModel):
    """Information about context used for response generation"""
    recent_workouts: int = Field(0, description="Number of recent workouts included")
    recent_meals: int = Field(0, description="Number of recent meals included")
    embeddings_retrieved: int = Field(0, description="Number of RAG embeddings retrieved")
    profile_used: bool = Field(True, description="Whether user profile was included")


class ChatResponse(BaseModel):
    """Response payload from chat endpoint"""
    success: bool = Field(..., description="Whether the request was successful")
    conversation_id: str = Field(..., description="UUID of the conversation")
    message: str = Field(..., description="AI coach's response")
    context_used: Optional[ContextInfo] = Field(None, description="Context information")
    error: Optional[str] = Field(None, description="Error message if success=False")


class ConversationHistoryResponse(BaseModel):
    """Response for fetching conversation history"""
    success: bool
    conversation_id: Optional[str]
    messages: List[ChatMessage]
    coach_type: str
    created_at: datetime
    last_message_at: datetime


class UserContext(BaseModel):
    """Complete user context for AI coach"""
    user_id: str
    profile: Optional[Dict[str, Any]] = None
    recent_workouts: List[Dict[str, Any]] = []
    recent_meals: List[Dict[str, Any]] = []
    recent_activities: List[Dict[str, Any]] = []
    goals: List[Dict[str, Any]] = []
    relevant_embeddings: List[Dict[str, Any]] = []


class CoachPersona(BaseModel):
    """Coach persona configuration"""
    id: str
    name: str  # 'trainer' or 'nutritionist'
    display_name: str
    system_prompt: str
    specialty: str
    created_at: datetime
    updated_at: datetime
