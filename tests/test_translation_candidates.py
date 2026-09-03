from translation_service.models import TranslationUnit
from translation_service.translation_candidates import (
    select_translation_candidate,
)


def test_returns_none_when_no_matches_exist():
    candidate = select_translation_candidate([])

    assert candidate is None


def test_returns_first_match():
    first = TranslationUnit(
        source_text="Hei maailma",
        target_text="Första översättningen",
    )

    second = TranslationUnit(
        source_text="Hei maailma",
        target_text="Andra översättningen",
    )

    candidate = select_translation_candidate(
        [first, second],
    )

    assert candidate is first
