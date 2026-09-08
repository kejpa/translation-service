from starlette.testclient import TestClient

from translation_service.main import app
from translation_service.ollama_service import OllamaError

client = TestClient(app)


def test_llm_test_endpoint_returns_response(
    monkeypatch,
):
    monkeypatch.setattr(
        "translation_service.main.generate_text",
        lambda prompt, client=None: "Hello",
    )

    response = client.post(
        "/llm/test",
        json={
            "prompt": "Say hello",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "response": "Hello",
    }


def test_llm_test_endpoint_returns_500_on_ollama_error(
    monkeypatch,
):
    def fail(*args, **kwargs):
        raise OllamaError(
            "Failed to communicate with Ollama",
        )

    monkeypatch.setattr(
        "translation_service.main.generate_text",
        fail,
    )

    response = client.post(
        "/llm/test",
        json={
            "prompt": "Say hello",
        },
    )

    assert response.status_code == 500
