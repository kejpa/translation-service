from translation_service.translation_service import translate_text


def test_translate_text_returns_translation(
    monkeypatch,
):
    monkeypatch.setattr(
        "translation_service.translation_service.generate_text",
        lambda prompt: "Hej världen",
    )

    result = translate_text(
        "Hei maailma",
    )

    assert result == "Hej världen"


def test_translate_text_uses_translation_prompt(
    monkeypatch,
):
    captured_prompt = str | None

    def fake_generate_text(
        prompt: str,
    ):
        nonlocal captured_prompt
        captured_prompt = prompt

        return "Hej världen"

    monkeypatch.setattr(
        "translation_service.translation_service.generate_text",
        fake_generate_text,
    )

    translate_text(
        "Hei maailma",
    )

    assert captured_prompt is not None
    assert "Hei maailma" in captured_prompt


def test_translate_text_passes_prompt_to_generate_text(
    monkeypatch,
):
    captured_prompt = None

    def fake_generate_text(
        prompt: str,
    ):
        nonlocal captured_prompt
        captured_prompt = prompt

        return "Hej världen"

    monkeypatch.setattr(
        "translation_service.translation_service.generate_text",
        fake_generate_text,
    )

    translate_text(
        "Hei maailma",
    )

    assert captured_prompt == (
        "Translate the following Finnish text to Swedish.\n\n"
        "Finnish:\n"
        "Hei maailma\n\n"
        "Swedish:"
    )
