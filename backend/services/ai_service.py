import httpx
import os
from fastapi import HTTPException, status
from schemas.practice import ValidationResult

class AIService:
    """Service to validate sentences via n8n + Gemini"""
    
    def __init__(self):
        self.webhook_url = os.getenv("N8N_WEBHOOK_URL", "http://n8n:5678/webhook/validate-sentence")
    
    async def validate_sentence(self, word: str, user_sentence: str) -> ValidationResult:

        payload = {
            "word": word,
            "sentence": user_sentence
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.webhook_url,
                    json=payload,
                    timeout=30.0  # AI might take time
                )
                response.raise_for_status()
                data = response.json()
                
                # Parse n8n response
                return ValidationResult(
                    score=data.get("score", 5.0),
                    cefr_level=data.get("cefr_level", "A2"),
                    feedback=data.get("feedback", "Sentence validated."),
                    corrected_sentence=data.get("corrected_sentence")
                )
                
            except httpx.HTTPError as e:
                # If n8n is not ready, return mock result
                return ValidationResult(
                    score=7.0,
                    cefr_level="B1",
                    feedback=f"[Mock] Good use of '{word}'. (n8n not configured yet)",
                    corrected_sentence=None
                )

ai_service = AIService()