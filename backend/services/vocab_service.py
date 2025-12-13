
import os
import httpx
from typing import Optional, Dict


class VocabService:
    
    
    def __init__(self):
        self.api_url = os.getenv("VOCAB_API_URL", "http://worddee_api:8001")
        self.api_key = os.getenv("VOCAB_API_KEY", "")
    
    async def get_random_word(self, difficulty: Optional[str] = None) -> Optional[Dict]:
       
        try:
            params = {}
            if difficulty:
                params["difficulty"] = difficulty
            
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.api_url}/api/random",
                    params=params
                )
                response.raise_for_status()
                return response.json()
        
        except Exception as e:
            print(f"Error fetching random word: {e}")
            return None
    
    async def get_word_by_id(self, word_id: int) -> Optional[Dict]:
    
        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                response = await client.get(
                    f"{self.api_url}/api/words/{word_id}"
                )
                response.raise_for_status()
                return response.json()
        
        except Exception as e:
            print(f"Error fetching word {word_id}: {e}")
            return None
