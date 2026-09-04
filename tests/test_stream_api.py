from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_chat_stream_endpoint():
    payload = {
        "session_id": "stream_session_01",
        "message": "Calculate maintenance fee for 3 Bed apartment"
    }
    
    response = client.post("/api/v1/chat/stream", json=payload)
    assert response.status_code == 200
    assert "text/event-stream" in response.headers["content-type"]
    
    content = response.text
    assert "data:" in content
    assert "node_start" in content or "final_result" in content