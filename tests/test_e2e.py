from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_e2e_rag_flow():
    response = client.post("/query", json={"query": "What are the maintenance fees?"})
    assert response.status_code == 200
    assert "X-Process-Time" in response.headers
    data = response.json()
    assert "PKR 12,000" in data["answer"]

def test_e2e_agent_flow():
    response = client.post("/agent/query", json={"query": "What is the maintenance fee for a Penthouse for 3 months?"})
    assert response.status_code == 200
    assert "X-Process-Time" in response.headers
    data = response.json()
    assert data["tool_used"] == "calculate_maintenance_fee"
    assert "90,000" in data["response"]