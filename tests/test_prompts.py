from translation_service.prompts import (
    build_translation_prompt,
)


def test_build_translation_prompt():
    prompt = build_translation_prompt(
        "Hei maailma",
    )

    assert prompt == (
        "Translate the following Finnish text to Swedish.\n\n"
        "Finnish:\n"
        "Hei maailma\n\n"
        "Swedish:"
    )


def test_build_translation_prompt_for_empty_text():
    prompt = build_translation_prompt("")

    assert prompt == (
        "Translate the following Finnish text to Swedish.\n\nFinnish:\n\n\nSwedish:"
    )
