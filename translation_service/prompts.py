def build_translation_prompt(
    source_text: str,
) -> str:
    return (
        "Translate the following Finnish text to Swedish.\n\n"
        f"Finnish:\n{source_text}\n\n"
        "Swedish:"
    )
