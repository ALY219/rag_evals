from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_endpoint_success():
    response = client.post("/query", json={"query": "What are the maintenance fees?"})
    assert response.status_code == 200
    assert "answer" in response.json()
    assert "sources" in response.json()

def test_agent_endpoint_tool_execution():
    response = client.post("/agent/query", json={"query": "What is the maintenance fee for a 2 Bed?"})
    assert response.status_code == 200
    data = response.json()
    assert data["tool_used"] == "calculate_maintenance_fee"
    assert "12,000" in data["response"]

def test_agent_endpoint_fallback():
    response = client.post("/agent/query", json={"query": "Who is the property manager?"})
    assert response.status_code == 200
    data = response.json()
    assert data["tool_used"] is None
    assert "real estate assistant" in data["response"]