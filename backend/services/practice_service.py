
from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models import PracticeSession
from typing import Dict, List, Optional
from datetime import datetime


class PracticeService:
    
    
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
    
        return (
            self.db.query(PracticeSession)
            .order_by(PracticeSession.practiced_at.desc())
            .limit(limit)
            .all()
        )
    
    def get_statistics(self) -> Dict:
    
    
        total_sessions = self.db.query(func.count(PracticeSession.id)).scalar() or 0
        
        
        avg_score = self.db.query(func.avg(PracticeSession.score)).scalar() or 0.0
        
        
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
