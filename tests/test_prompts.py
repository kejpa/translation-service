from translation_service.prompts import (
    build_translation_prompt,
)


def test_build_translation_prompt_contains_translation_rules():
    prompt = build_translation_prompt(
        "Hei maailma",
    )

    assert "Return only the Swedish translation" in prompt


def test_build_translation_prompt_contains_no_explanation_rule():
    prompt = build_translation_prompt(
        "Hei maailma",
    )

    assert "Do not explain your translation" in prompt
