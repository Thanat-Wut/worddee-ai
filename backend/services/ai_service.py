"""
════════════════════════════════════════════════════════════════
AI Service - Sentence validation via n8n webhook
════════════════════════════════════════════════════════════════
"""
import os
import httpx
from typing import Dict


class AIService:
    """
    Service for validating sentences using n8n workflow with Gemini AI.
    """
    
    def __init__(self):
        self.webhook_url = os.getenv(
            "N8N_WEBHOOK_URL",
            "http://n8n:5678/webhook/validate-sentence"
        )
    
    async def validate_sentence(
        self,
        word: str,
        definition: str,
        sentence: str
    ) -> Dict:
        """
        Validate a practice sentence using AI.
        
        Args:
            word: The vocabulary word being practiced
            definition: Word definition
            sentence: User's sentence
        
        Returns:
            Dict with score, cefr_level, feedback, corrected_sentence
        """
        try:
            payload = {
                "word": word,
                "definition": definition,
                "sentence": sentence
            }
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload
                )
                response.raise_for_status()
                return response.json()
        
        except Exception as e:
            print(f"Error validating sentence: {e}")
            # Return mock result if n8n is not available
            return self._get_mock_validation(sentence)
    
    def _get_mock_validation(self, sentence: str) -> Dict:
        """
        Generate mock validation result (fallback when n8n is unavailable).
        
        Args:
            sentence: User's sentence
        
        Returns:
            Mock validation result
        """
        return {
            "score": 7.0,
            "cefr_level": "B1",
            "is_correct": True,
            "feedback": "Good attempt! Your sentence demonstrates understanding of the word. (Note: This is a mock result - n8n workflow not configured yet)",
            "corrected_sentence": sentence
        }
