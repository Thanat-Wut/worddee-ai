"""
════════════════════════════════════════════════════════════════
Practice Service - Session management and statistics
════════════════════════════════════════════════════════════════
"""
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models import PracticeSession
from typing import Dict, List, Optional
from datetime import datetime


class PracticeService:
    """
    Service for managing practice sessions and calculating statistics.
    """
    
    def __init__(self, db: Session):
        self.db = db
    
    def save_session(
        self,
        word_id: int,
        user_sentence: str,
        score: float,
        cefr_level: str,
        feedback: str,
        corrected_sentence: Optional[str] = None
    ) -> PracticeSession:
        """
        Save a practice session to the database.
        
        Args:
            word_id: ID of the practiced word
            user_sentence: User's submitted sentence
            score: AI-generated score (0-10)
            cefr_level: CEFR level (A1-C2)
            feedback: AI feedback
            corrected_sentence: Optional corrected version
        
        Returns:
            Created PracticeSession
        """
        session = PracticeSession(
            word_id=word_id,
            user_sentence=user_sentence,
            score=score,
            cefr_level=cefr_level,
            feedback=feedback,
            corrected_sentence=corrected_sentence,
            practiced_at=datetime.utcnow()
        )
        
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)
        
        return session
    
    def get_recent_sessions(self, limit: int = 10) -> List[PracticeSession]:
        """
        Get recent practice sessions.
        
        Args:
            limit: Maximum number of sessions to return
        
        Returns:
            List of PracticeSession objects
        """
        return (
            self.db.query(PracticeSession)
            .order_by(PracticeSession.practiced_at.desc())
            .limit(limit)
            .all()
        )
    
    def get_statistics(self) -> Dict:
        """
        Calculate user's practice statistics.
        
        Returns:
            Dict with total_sessions, average_score, most_common_level
        """
        # Total sessions
        total_sessions = self.db.query(func.count(PracticeSession.id)).scalar() or 0
        
        # Average score
        avg_score = self.db.query(func.avg(PracticeSession.score)).scalar() or 0.0
        
        # Most common CEFR level
        most_common = (
            self.db.query(
                PracticeSession.cefr_level,
                func.count(PracticeSession.cefr_level).label("count")
            )
            .group_by(PracticeSession.cefr_level)
            .order_by(func.count(PracticeSession.cefr_level).desc())
            .first()
        )
        
        most_common_level = most_common[0] if most_common else "N/A"
        
        return {
            "total_sessions": total_sessions,
            "average_score": float(avg_score),
            "most_common_level": most_common_level
        }
