"""
════════════════════════════════════════════════════════════════
Practice Routes - Handle vocabulary practice and validation
════════════════════════════════════════════════════════════════
"""
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from backend.db.database import get_db
from backend.schemas.practice import PracticeSubmit, PracticeResponse
from backend.services.vocab_service import VocabService
from backend.services.ai_service import AIService
from backend.services.practice_service import PracticeService

router = APIRouter(prefix="/api/practice", tags=["practice"])

vocab_service = VocabService()
ai_service = AIService()


@router.get("/word")
async def get_random_word(difficulty: str = None):
    """
    Get a random vocabulary word for practice.
    
    Args:
        difficulty: Optional filter (Beginner, Intermediate, Advanced)
    
    Returns:
        Word object with id, word, definition, difficulty_level, created_at
    """
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
    """
    Submit a practice sentence for AI validation.
    
    Args:
        submission: PracticeSubmit with word_id and user_sentence
        db: Database session
    
    Returns:
        PracticeResponse with score, cefr_level, feedback, etc.
    """
    try:
        # Get word details
        word = await vocab_service.get_word_by_id(submission.word_id)
        if not word:
            raise HTTPException(status_code=404, detail="Word not found")
        
        # Validate sentence with AI
        validation_result = await ai_service.validate_sentence(
            word=word["word"],
            definition=word["definition"],
            sentence=submission.user_sentence
        )
        
        # Save practice session to database
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
