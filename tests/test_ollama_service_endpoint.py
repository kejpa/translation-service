from unittest.mock import patch

from starlette.testclient import TestClient

from translation_service.main import app
from translation_service.ollama_service import InstallModelResult, OllamaError

client = TestClient(app)


def test_llm_test_endpoint_returns_response(
    monkeypatch,
):
    monkeypatch.setattr(
        "translation_service.main.generate_text",
        lambda prompt, client=None: "Hello",
    )

    response = client.post(
        "/api/llm/test",
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
        "/api/llm/test",
        json={
            "prompt": "Say hello",
        },
    )

    assert response.status_code == 500


def test_install_model_uses_configured_model_when_request_is_empty():
    with (
        patch(
            "translation_service.main.get_ollama_model",
            return_value="gemma3:4b",
        ),
        patch(
            "translation_service.main.install_model",
        ) as install_model_mock,
    ):
        install_model_mock.return_value = InstallModelResult(
            success=True,
            model="gemma3:4b",
            message="Installed successfully",
        )

        response = client.post(
            "/api/llm/install-model",
            json={},
        )

    assert response.status_code == 200

    install_model_mock.assert_called_once_with(
        "gemma3:4b",
    )


def test_install_model_uses_requested_model():
    with patch(
        "translation_service.main.install_model",
    ) as install_model_mock:
        install_model_mock.return_value = InstallModelResult(
            success=True,
            model="qwen3:4b",
            message="Installed successfully",
        )

        response = client.post(
            "/api/llm/install-model",
            json={
                "model": "qwen3:4b",
            },
        )

    assert response.status_code == 200

    install_model_mock.assert_called_once_with(
        "qwen3:4b",
    )


def test_install_model_returns_success_response():
    with patch(
        "translation_service.main.install_model",
    ) as install_model_mock:
        install_model_mock.return_value = InstallModelResult(
            success=True,
            model="gemma3:4b",
            message="Installed successfully",
        )

        response = client.post(
            "/api/llm/install-model",
            json={},
        )

    assert response.status_code == 200

    assert response.json() == {
        "success": True,
        "model": "gemma3:4b",
        "message": "Installed successfully",
    }


def test_install_model_returns_failure_response():
    with patch(
        "translation_service.main.install_model",
    ) as install_model_mock:
        install_model_mock.return_value = InstallModelResult(
            success=False,
            model="KalleAnka3:29",
            message="Model not found",
        )

        response = client.post(
            "/api/llm/install-model",
            json={
                "model": "KalleAnka3:29",
            },
        )

    assert response.status_code == 200

    assert response.json() == {
        "success": False,
        "model": "KalleAnka3:29",
        "message": "Model not found",
    }
