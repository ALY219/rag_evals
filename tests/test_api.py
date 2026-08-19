from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_query_endpoint_success():
    response = client.post("/query", json={"question": "What are the maintenance fees?"})
    assert response.status_code == 200