from sqlalchemy import Column, Integer, String, Text, DateTime, Numeric
from db.database import Base
from datetime import datetime

class PracticeSession(Base):

    __tablename__ = "practice_sessions"
    
    id = Column(Integer, primary_key=True, index=True)
    word_id = Column(Integer, nullable=False, index=True)
    user_sentence = Column(Text, nullable=False)
    score = Column(Numeric(3, 1))
    cefr_level = Column(String(10))
    feedback = Column(Text)
    corrected_sentence = Column(Text)
    practiced_at = Column(DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f"<PracticeSession(id={self.id}, word_id={self.word_id}, score={self.score})>"