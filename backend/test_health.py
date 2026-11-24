import pytest
from fastapi.testclient import TestClient
from backend.main import app


def test_health_endpoint():
    client = TestClient(app=app)
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["service"] == "tensor-lab-145"


def test_analyze_endpoint():
    client = TestClient(app=app)
    response = client.post("/api/analyze", json={"source_path": "/var/lib/alan-portfolio/workspaces/ryan/tensor-lab-145/backend/main.py", "language": "python"})
    assert response.status_code == 200
    data = response.json()
    assert "functions" in data
    assert "commands" in data
    assert "entry_points" in data
