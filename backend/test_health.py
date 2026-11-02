import pytest
from httpx import AsyncClient
from main import app


@pytest.mark.asyncio
async def test_health_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "ok"
        assert data["service"] == "tensor-lab-145"


@pytest.mark.asyncio
async def test_analyze_endpoint():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/api/analyze", json={"source_path": "/tmp/test", "language": "python"})
        assert response.status_code == 200
        data = response.json()
        assert "functions" in data
        assert "commands" in data
        assert "entry_points" in data
