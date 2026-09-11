from fastapi.testclient import TestClient

from translation_service.main import app

client = TestClient(app)


def test_health_endpoint(
    monkeypatch,
):
    monkeypatch.setattr(
        "translation_service.main.check_connection",
        lambda: True,
    )

    monkeypatch.setattr(
        "translation_service.main.model_exists",
        lambda: True,
    )

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "running",
        "database": "connected",
        "docker": "running",
        "ollama": "connected",
        "model": "gemma3:4b",
        "model_available": True,
        "reuse_threshold": 85,
        "reference_threshold": 30,
    }
