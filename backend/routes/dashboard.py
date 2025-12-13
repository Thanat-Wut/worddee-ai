
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.practice import DashboardStats, PracticeResponse
from services.practice_service import PracticeService

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats(db: Session = Depends(get_db)):

    practice_service = PracticeService(db)
    
    
    stats = practice_service.get_statistics()
    
    
    recent_sessions = practice_service.get_recent_sessions(limit=10)
    
    
    recent_sessions_data = [
        PracticeResponse(
            session_id=session.id,
            word_id=session.word_id,
            user_sentence=session.user_sentence,
            score=session.score,
            cefr_level=session.cefr_level,
            feedback=session.feedback,
            corrected_sentence=session.corrected_sentence,
            practiced_at=session.practiced_at.isoformat()
        )
        for session in recent_sessions
    ]
    
    return DashboardStats(
        total_sessions=stats["total_sessions"],
        average_score=stats["average_score"],
        most_common_level=stats["most_common_level"],
        recent_sessions=recent_sessions_data
    )
