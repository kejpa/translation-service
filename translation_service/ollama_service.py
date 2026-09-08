import ollama

from translation_service.config import (
    get_ollama_model,
    get_temperature,
    get_ollama_base_url,
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
