from starlette.testclient import TestClient

from translation_service.main import app

client = TestClient(app)


def test_root_endpoint(
    monkeypatch,
):
    monkeypatch.setattr(
        "translation_service.main.check_connection",
        lambda: True,
    )

    monkeypatch.setattr(
        "translation_service.main.check_database_connection",
        lambda db: True,
    )

    response = client.get("/")

    assert response.status_code == 200

    body = response.json()

    assert body["service"] == "translation-service"
    assert body["status"] == "running"
    assert body["database"] == "connected"
    assert body["ollama"] == "connected"


def test_root_endpoint_reports_disconnected_services(
    monkeypatch,
):
    monkeypatch.setattr(
        "translation_service.main.check_connection",
        lambda: False,
    )

    monkeypatch.setattr(
        "translation_service.main.check_database_connection",
        lambda db: False,
    )

    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["database"] == "disconnected"
    assert response.json()["ollama"] == "disconnected"
