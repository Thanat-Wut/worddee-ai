from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime



class PracticeSubmit(BaseModel):
    
    word_id: int = Field(..., description="ID of the word being practiced")
    user_sentence: str = Field(..., min_length=1, description="User's sentence")
    session_duration_ms: Optional[int] = Field(None, description="Time taken in milliseconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "word_id": 1,
                "user_sentence": "I eat an apple every morning for breakfast.",
                "session_duration_ms": 45000
            }
        }



class ValidationResult(BaseModel):
    
    score: float = Field(..., ge=0, le=10, description="Score from 0-10")
    cefr_level: str = Field(..., description="CEFR level (A1, A2, B1, B2, C1, C2)")
    feedback: str = Field(..., description="Detailed feedback")
    corrected_sentence: Optional[str] = Field(None, description="Corrected version if needed")
    
    class Config:
        json_schema_extra = {
            "example": {
                "score": 8.5,
                "cefr_level": "B1",
                "feedback": "Good sentence structure. Minor grammar improvement needed.",
                "corrected_sentence": "I eat an apple every morning."
            }
        }

class PracticeResponse(BaseModel):
    
    session_id: int
    word_id: int
    user_sentence: str
    score: float
    cefr_level: str
    feedback: str
    corrected_sentence: Optional[str]
    practiced_at: datetime
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "session_id": 123,
                "word_id": 1,
                "user_sentence": "I eat an apple.",
                "score": 8.5,
                "cefr_level": "B1",
                "feedback": "Good sentence!",
                "corrected_sentence": None,
                "practiced_at": "2025-12-12T10:00:00Z"
            }
        }

class DashboardStats(BaseModel):
    
    total_sessions: int
    average_score: float
    most_common_level: str
    recent_sessions: list[PracticeResponse]
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_sessions": 150,
                "average_score": 7.8,
                "most_common_level": "B1",
                "recent_sessions": []
            }
        }