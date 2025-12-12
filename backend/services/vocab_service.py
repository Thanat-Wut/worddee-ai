import httpx
import os
from typing import Optional, Dict, Any
from fastapi import HTTPException, status

class VocabService:
    """Service to interact with worddee-api"""
    
    def __init__(self):
        self.base_url = os.getenv("VOCAB_API_URL", "http://worddee_api:8001")
        self.api_key = os.getenv("VOCAB_API_KEY", "")
    
    async def get_random_word(self, difficulty: Optional[str] = None) -> Dict[str, Any]:
        """Get random word from vocab API"""
        url = f"{self.base_url}/api/random"
        params = {"difficulty": difficulty} if difficulty else {}
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, params=params, timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Vocab API error: {str(e)}"
                )
    
    async def get_word_by_id(self, word_id: int) -> Dict[str, Any]:
        """Get specific word by ID"""
        url = f"{self.base_url}/api/words/{word_id}"
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(url, timeout=10.0)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                if e.response.status_code == 404:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Word with ID {word_id} not found"
                    )
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Vocab API error: {str(e)}"
                )
            except httpx.HTTPError as e:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail=f"Vocab API error: {str(e)}"
                )

vocab_service = VocabService()