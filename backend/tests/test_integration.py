"""Integration tests for worddee-ai system"""

import pytest
import requests
import time


VOCAB_API_URL = "http://localhost:8001"
BACKEND_URL = "http://localhost:8000"
FRONTEND_URL = "http://localhost:3000"
N8N_URL = "http://localhost:5678"


class TestServiceAvailability:
    

    def test_vocab_api_available(self):
        
        try:
            response = requests.get(f"{VOCAB_API_URL}/health", timeout=5)
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("Vocab API not running")

    def test_backend_available(self):
        
        try:
            response = requests.get(f"{BACKEND_URL}/health", timeout=5)
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("Backend not running")

    def test_frontend_available(self):
        
        try:
            response = requests.get(FRONTEND_URL, timeout=5)
            assert response.status_code == 200
        except requests.exceptions.ConnectionError:
            pytest.skip("Frontend not running")


class TestEndToEndFlow:
    

    def test_complete_practice_flow(self):
        
        
        response = requests.get(f"{BACKEND_URL}/api/practice/word")
        assert response.status_code == 200
        word_data = response.json()
        word_id = word_data["id"]
        
        
        payload = {
            "word_id": word_id,
            "user_sentence": "This is a test sentence for integration testing."
        }
        response = requests.post(f"{BACKEND_URL}/api/practice/submit", json=payload)
        assert response.status_code == 200
        result = response.json()
        
        
        assert "session_id" in result
        assert "score" in result
        assert "cefr_level" in result
        assert "feedback" in result
        
        
        time.sleep(1)  
        response = requests.get(f"{BACKEND_URL}/api/dashboard/stats")
        assert response.status_code == 200
        stats = response.json()
        assert stats["total_sessions"] > 0

    def test_vocab_api_integration(self):
        
        
        response = requests.get(f"{VOCAB_API_URL}/api/random")
        assert response.status_code == 200
        vocab_word = response.json()
        
        
        response = requests.get(f"{BACKEND_URL}/api/practice/word")
        assert response.status_code == 200
        backend_word = response.json()
        
        
        assert set(vocab_word.keys()) == set(backend_word.keys())


class TestDataPersistence:
    

    def test_practice_session_saved(self):
        
        
        payload = {
            "word_id": 1,
            "user_sentence": "Test sentence for data persistence."
        }
        response = requests.post(f"{BACKEND_URL}/api/practice/submit", json=payload)
        assert response.status_code == 200
        session_id = response.json()["session_id"]
        
        
        time.sleep(1)
        response = requests.get(f"{BACKEND_URL}/api/dashboard/stats")
        stats = response.json()
        recent_sessions = stats["recent_sessions"]
        
        
        session_ids = [s["session_id"] for s in recent_sessions]
        assert session_id in session_ids


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
