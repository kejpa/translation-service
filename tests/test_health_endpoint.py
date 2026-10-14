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

    response = client.get("/api/health")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data["status"], str)
    assert isinstance(data["database"], str)
    assert isinstance(data["ollama"], str)
    assert isinstance(data["model"], str)
    assert isinstance(data["model_available"], bool)
    assert isinstance(data["reuse_threshold"], int)
    assert isinstance(data["reference_threshold"], int)
