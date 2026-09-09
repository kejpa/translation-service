from translation_service.ollama_service import generate_text
from translation_service.prompts import build_translation_prompt


def translate_text(
    source_text: str,
) -> str:
    prompt = build_translation_prompt(
        source_text,
    )

    return generate_text(
        prompt,
    )
