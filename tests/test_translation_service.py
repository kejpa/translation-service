from tests.helpers import add_translation
from translation_service.docx_exporter import translate_paragraphs
from translation_service.translation_memory import find_exact_matches
from translation_service.translation_service import translate_text
from translation_service.translation_status import TranslationStatus


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
        "You are a professional Finnish to Swedish translator.\n\n"
        "Translate the Finnish text to Swedish.\n\n"
        "Rules:\n"
        "- Return only the Swedish translation.\n"
        "- Do not explain your translation.\n"
        "- Do not provide alternatives.\n"
        "- Do not provide notes.\n"
        "- Do not use markdown.\n"
        "- Do not ask follow-up questions.\n"
        "- Do not include the original Finnish text.\n\n"
        "Finnish:\nHei maailma"
    )


def test_rule_number_can_change_and_still_match(
    db,
):
    add_translation(
        db,
        "SW 14.4\tUseamman kuin kahden sormen teippaus",
        "Useamman kuin kahden sormen teippaus",
        "SW 14.4\tTejpning av fler än två fingrar eller tår",
        "Tejpning av fler än två fingrar eller tår",
    )

    matches = find_exact_matches(
        "SW 27.8\tUseamman kuin kahden sormen teippaus",
        db,
    )

    assert len(matches) == 1

    assert matches[0].target_text == (
        "SW 14.4\tTejpning av fler än två fingrar eller tår"
    )


def test_fuzzy_high_match_uses_new_rule_number(
    db,
):
    add_translation(
        db,
        "SW 14.4\tUseamman kuin kahden sormen teippaus",
        "Useamman kuin kahden sormen teippaus",
        "SW 14.4\tTejpning av fler än två fingrar eller tår",
        "Tejpning av fler än två fingrar eller tår",
    )

    result = translate_paragraphs(
        [
            "SW 27.8\tUseamman kuin kahden sormen teippaukset",
        ],
        db,
    )

    assert result[0].status == (TranslationStatus.FUZZY_HIGH)

    assert result[0].target_text == (
        "SW 27.8\tTejpning av fler än två fingrar eller tår"
    )


def test_fuzzy_low_match_uses_new_rule_number(
    db,
    monkeypatch,
):
    monkeypatch.setattr(
        "translation_service.docx_exporter.get_reuse_threshold",
        lambda: 100,
    )
    add_translation(
        db,
        "SW 14.4\tUseamman kuin kahden sormen teippaus",
        "Useamman kuin kahden sormen teippaus",
        "SW 14.4\tTejpning av fler än två fingrar eller tår",
        "Tejpning av fler än två fingrar eller tår",
    )

    result = translate_paragraphs(
        [
            "SW 27.8\tUseamman kuin kahden sormen",
        ],
        db,
    )

    assert result[0].status == (TranslationStatus.FUZZY_LOW)

    assert result[0].target_text == (
        "SW 27.8\tTejpning av fler än två fingrar eller tår"
    )


def test_llm_translation_uses_new_rule_number(
    db,
    monkeypatch,
):
    monkeypatch.setattr(
        "translation_service.docx_exporter.translate_text",
        lambda text: ("Tejpning av fler än två fingrar eller tår"),
    )

    result = translate_paragraphs(
        [
            "SW 27.8\tUseamman kuin kahden sormen teippaus",
        ],
        db,
    )

    assert result[0].status == (TranslationStatus.LLM)

    assert result[0].target_text == (
        "SW 27.8\tTejpning av fler än två fingrar eller tår"
    )
