

import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)


class TestHealthEndpoints:
    

    def test_root_endpoint(self):
        
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "service" in data
        assert data["service"] == "Worddee-AI Backend"

    def test_health_endpoint(self):
        
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"


class TestPracticeEndpoints:
    

    def test_get_random_word_no_difficulty(self):
        
        response = client.get("/api/practice/word")
        assert response.status_code == 200
        data = response.json()
        assert "word" in data
        assert "definition" in data
        assert "difficulty_level" in data

    def test_get_random_word_with_difficulty(self):
        
        response = client.get("/api/practice/word?difficulty=Beginner")
        assert response.status_code == 200
        data = response.json()
        assert data["difficulty_level"] == "Beginner"

    def test_submit_practice_valid(self):
        
        payload = {
            "word_id": 1,
            "user_sentence": "This is a test sentence."
        }
        response = client.post("/api/practice/submit", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "score" in data
        assert "cefr_level" in data
        assert "feedback" in data
        assert 0 <= data["score"] <= 10

    def test_submit_practice_invalid(self):
        
        payload = {
            "word_id": 1
            
        }
        response = client.post("/api/practice/submit", json=payload)
        assert response.status_code == 422  


class TestDashboardEndpoints:
    

    def test_get_dashboard_stats(self):
        
        response = client.get("/api/dashboard/stats")
        assert response.status_code == 200
        data = response.json()
        assert "total_sessions" in data
        assert "average_score" in data
        assert "most_common_level" in data
        assert "recent_sessions" in data
        assert isinstance(data["recent_sessions"], list)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
