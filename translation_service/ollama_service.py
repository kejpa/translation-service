import ollama

from translation_service.config import (
    get_ollama_base_url,
    get_ollama_model,
    get_temperature,
)


class OllamaError(Exception):
    pass


def generate_text(
    prompt: str,
    client=None,
) -> str:
    if client is None:
        client = ollama.Client(
            host=get_ollama_base_url(),
        )

    try:
        response = client.generate(
            model=get_ollama_model(),
            prompt=prompt,
            options={
                "temperature": get_temperature(),
            },
        )

        return response["response"]

    except Exception as error:
        raise OllamaError(
            "Failed to communicate with Ollama",
        ) from error


def check_connection(
    client=None,
) -> bool:
    if client is None:
        client = ollama.Client(
            host=get_ollama_base_url(),
        )

    try:
        client.list()

        return True

    except Exception:
        return False


def model_exists(
    client=None,
) -> bool:
    if client is None:
        client = ollama.Client(
            host=get_ollama_base_url(),
        )

    models = client.list()

    configured_model = get_ollama_model()

    return any(model["model"] == configured_model for model in models["models"])
