from unittest.mock import Mock

import pytest

from translation_service.ollama_service import (
    OllamaError,
    generate_text,
    check_connection,
)


def test_generate_text_returns_response():
    client = Mock()

    client.generate.return_value = {
        "response": "Hello",
    }

    result = generate_text(
        prompt="Say hello",
        client=client,
    )

    assert result == "Hello"


def test_generate_text_uses_configured_model(
    monkeypatch,
):
    monkeypatch.setenv(
        "OLLAMA_MODEL",
        "gemma3:4b",
    )

    client = Mock()

    client.generate.return_value = {
        "response": "Hello",
    }

    generate_text(
        prompt="Say hello",
        client=client,
    )

    client.generate.assert_called_once_with(
        model="gemma3:4b",
        prompt="Say hello",
        options={
            "temperature": 0,
        },
    )


def test_generate_text_raises_ollama_error_on_failure():
    client = Mock()

    client.generate.side_effect = Exception(
        "Connection failed",
    )

    with pytest.raises(OllamaError):
        generate_text(
            prompt="Say hello",
            client=client,
        )


def test_check_ollama_connection_returns_true(
    monkeypatch,
):
    class FakeClient:
        def list(self):
            return {}

    monkeypatch.setattr(
        "translation_service.ollama_service.ollama.Client",
        lambda host: FakeClient(),
    )

    assert check_connection() is True


def test_check_ollama_connection_returns_false_on_error(
    monkeypatch,
):
    class FakeClient:
        def list(self):
            raise Exception()

    monkeypatch.setattr(
        "translation_service.ollama_service.ollama.Client",
        lambda host: FakeClient(),
    )

    assert check_connection() is False
