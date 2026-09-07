from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_vapi_voice_webhook_tool_call():
    payload = {
        "type": "tool-calls",
        "call": {"id": "vapi_call_999"},
        "toolCalls": [
            {
                "id": "call_tool_abc123",
                "type": "function",
                "function": {
                    "name": "query_real_estate_assistant",
                    "arguments": {
                        "query": "What is the maintenance fee for a 2 Bed apartment?"
                    }
                }
            }
        ]
    }

    response = client.post("/api/v1/voice/vapi", json=payload)
    assert response.status_code == 200
    
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 1
    assert data["results"][0]["toolCallId"] == "call_tool_abc123"
    assert len(data["results"][0]["result"]) > 0