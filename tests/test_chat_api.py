from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"

def test_chat_api_multi_turn_flow():
    session_id = "api_session_77"
    
    # Turn 1: Qualify lead via REST API
    payload1 = {
        "session_id": session_id,
        "message": "I want to buy a luxury flat with budget 40 million"
    }
    resp1 = client.post("/api/v1/chat", json=payload1)
    assert resp1.status_code == 200
    data1 = resp1.json()
    assert data1["is_safe"] is True
    assert data1["lead_info"]["budget"] == "40 million"

    # Turn 2: Schedule appointment under same session_id
    payload2 = {
        "session_id": session_id,
        "message": "Schedule an appointment for viewing tomorrow"
    }
    resp2 = client.post("/api/v1/chat", json=payload2)
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert data2["is_safe"] is True
    assert data2["lead_info"]["budget"] == "40 million"  # Context retained across HTTP requests