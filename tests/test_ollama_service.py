from unittest.mock import Mock

import pytest

from translation_service.ollama_service import (
    OllamaError,
    generate_text,
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
