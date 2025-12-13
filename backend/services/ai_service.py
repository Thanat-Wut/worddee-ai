
import os
import httpx
import logging
from typing import Dict

logger = logging.getLogger(__name__)

class AIService:
    
    
    def __init__(self):
        self.webhook_url = os.getenv(
            "N8N_WEBHOOK_URL",
            "http://n8n:5678/webhook/validate-sentence"
        )
        self.timeout = 60.0
    
    async def validate_sentence(
        self,
        word: str,
        definition: str,
        sentence: str
    ) -> Dict:
        
        payload = {
            "word": word,
            "definition": definition,
            "sentence": sentence
        }
        
        logger.info(f"Sending to n8n: {payload}")
        
        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    self.webhook_url,
                    json=payload
                )
                
                logger.info(f"n8n response status: {response.status_code}")
                response.raise_for_status()
                data = response.json()
                logger.info(f"n8n response data: {data}")
                
                if isinstance(data, list) and len(data) > 0:
                    result = data[0]
                else:
                    result = data
                
                return {
                    "score": float(result.get("score", 7.0)),
                    "cefr_level": str(result.get("cefr_level", "B1")).strip(),
                    "is_correct": bool(result.get("is_correct", True)),
                    "feedback": str(result.get("feedback", "Good attempt!")),
                    "corrected_sentence": result.get("corrected_sentence") or sentence
                }
        
        except httpx.TimeoutException as e:
            logger.error(f"n8n timeout: {e}")
            return self._get_mock_validation(sentence, "timeout")
        
        except httpx.HTTPStatusError as e:
            logger.error(f"n8n HTTP error: {e.response.status_code}")
            return self._get_mock_validation(sentence, f"error {e.response.status_code}")
        
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return self._get_mock_validation(sentence, "system error")
    
    def _get_mock_validation(self, sentence: str, error_msg: str = None) -> Dict:
        
        feedback = "Good attempt! Your sentence demonstrates understanding."
        if error_msg:
            feedback = f"[Mock - {error_msg}] {feedback}"
        
        return {
            "score": 7.0,
            "cefr_level": "B1",
            "is_correct": True,
            "feedback": feedback,
            "corrected_sentence": sentence
        }

ai_service = AIService()