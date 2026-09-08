from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_vapi_tool_call_latency_and_response():
    payload = {
        "type": "tool-calls",
        "call": {"id": "vapi_call_latency_test"},
        "toolCalls": [
            {
                "id": "call_tool_speed_check",
                "type": "function",
                "function": {
                    "name": "query_real_estate_assistant",
                    "arguments": {"query": "What is the starting price for 3 bed villas?"}
                }
            }
        ]
    }
    
    response = client.post("/api/v1/voice/vapi", json=payload)
    assert response.status_code == 200
    
    # Assert latency header tracking
    assert "X-Voice-Latency-MS" in response.headers
    latency = float(response.headers["X-Voice-Latency-MS"])
    assert latency > 0

    data = response.json()
    assert len(data["results"]) == 1
    assert data["results"][0]["toolCallId"] == "call_tool_speed_check"

def test_vapi_assistant_init_latency():
    payload = {"type": "assistant-request", "call": {"id": "vapi_init_test"}}
    response = client.post("/api/v1/voice/vapi", json=payload)
    assert response.status_code == 200
    assert "X-Voice-Latency-MS" in response.headers