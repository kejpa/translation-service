def build_translation_prompt(
    source_text: str,
) -> str:
    return (
        "You are a professional Finnish to Swedish translator.\n\n"
        f"Translate the Finnish text to Swedish.\n\n"
        f"Rules:\n"
        f"- Return only the Swedish translation.\n"
        f"- Do not explain your translation.\n"
        f"- Do not provide alternatives.\n"
        f"- Do not provide notes.\n"
        f"- Do not use markdown.\n"
        f"- Do not ask follow-up questions.\n"
        f"- Do not include the original Finnish text.\n\n"
        f"Finnish:\n{source_text}"
    )
