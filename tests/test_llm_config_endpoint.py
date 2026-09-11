from starlette.testclient import TestClient

from translation_service.main import app

client = TestClient(app)


def test_llm_config_endpoint_returns_defaults(
    monkeypatch,
):
    monkeypatch.delenv(
        "OLLAMA_MODEL",
        raising=False,
    )

    monkeypatch.delenv(
        "TEMPERATURE",
        raising=False,
    )

    response = client.get(
        "/llm/config",
    )

    assert response.status_code == 200

    assert response.json() == {
        "model": "gemma3:4b",
        "temperature": 0,
        "reuse_threshold": 85,
        "reference_threshold": 30,
    }


def test_llm_config_endpoint_returns_environment_values(
    monkeypatch,
):
    monkeypatch.setenv(
        "OLLAMA_MODEL",
        "qwen2.5:7b",
    )

    monkeypatch.setenv(
        "TEMPERATURE",
        "0.2",
    )

    monkeypatch.setenv(
        "REUSE_THRESHOLD",
        "95",
    )

    monkeypatch.setenv(
        "REFERENCE_THRESHOLD",
        "60",
    )

    response = client.get(
        "/llm/config",
    )

    assert response.status_code == 200

    assert response.json() == {
        "model": "qwen2.5:7b",
        "temperature": 0.2,
        "reuse_threshold": 95,
        "reference_threshold": 60,
    }
