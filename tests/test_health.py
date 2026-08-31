from fastapi.testclient import TestClient

from translation_service.main import app


client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200

    payload = response.json()

    assert payload["status"] == "running"
    assert payload["database"] == "connected"
