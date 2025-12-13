"""
════════════════════════════════════════════════════════════════
Practice Routes - Handle vocabulary practice and validation
════════════════════════════════════════════════════════════════
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from db.database import get_db
from schemas.practice import PracticeSubmit, PracticeResponse
from services.vocab_service import VocabService
from services.ai_service import AIService
from services.practice_service import PracticeService

router = APIRouter(prefix="/api/practice", tags=["practice"])

vocab_service = VocabService()
ai_service = AIService()


@router.get("/word")
async def get_random_word(difficulty: str = None):

    try:
        word = await vocab_service.get_random_word(difficulty)
        if not word:
            raise HTTPException(status_code=404, detail="No words found")
        return word
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch word: {str(e)}")


@router.post("/submit", response_model=PracticeResponse)
async def submit_practice(
    submission: PracticeSubmit,
    db: Session = Depends(get_db)
):
    
    try:
        
        word = await vocab_service.get_word_by_id(submission.word_id)
        if not word:
            raise HTTPException(status_code=404, detail="Word not found")
        
        
        validation_result = await ai_service.validate_sentence(
            word=word["word"],
            definition=word["definition"],
            sentence=submission.user_sentence
        )
        
        
        practice_service = PracticeService(db)
        session = practice_service.save_session(
            word_id=submission.word_id,
            user_sentence=submission.user_sentence,
            score=validation_result["score"],
            cefr_level=validation_result["cefr_level"],
            feedback=validation_result["feedback"],
            corrected_sentence=validation_result.get("corrected_sentence")
        )
        
        return PracticeResponse(
            session_id=session.id,
            word_id=submission.word_id,
            user_sentence=submission.user_sentence,
            score=validation_result["score"],
            cefr_level=validation_result["cefr_level"],
            feedback=validation_result["feedback"],
            corrected_sentence=validation_result.get("corrected_sentence"),
            practiced_at=session.practiced_at.isoformat()
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process submission: {str(e)}")
