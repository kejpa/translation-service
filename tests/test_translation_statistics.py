from translation_service.docx_exporter import (
    ParagraphTranslation,
)
from translation_service.translation_statistics import (
    TranslationStatistics,
    calculate_translation_statistics,
)
from translation_service.translation_status import (
    TranslationStatus,
)


def test_calculate_translation_statistics():
    statistics = calculate_translation_statistics(
        [
            ParagraphTranslation(
                source_text="Hei maailma",
                target_text="Hej världen",
                status=TranslationStatus.TRANSLATED,
            ),
            ParagraphTranslation(
                source_text="",
                target_text="",
                status=TranslationStatus.EMPTY,
            ),
            ParagraphTranslation(
                source_text="Tuntematon",
                target_text="Tuntematon",
                status=TranslationStatus.MISSING,
            ),
        ]
    )

    assert statistics == TranslationStatistics(
        total_paragraphs=3,
        translated=1,
        fuzzy_high=0,
        fuzzy_low=0,
        missing=1,
        empty=1,
    )


def test_calculate_translation_statistics_for_empty_list():
    statistics = calculate_translation_statistics([])

    assert statistics == TranslationStatistics(
        total_paragraphs=0,
        translated=0,
        fuzzy_high=0,
        fuzzy_low=0,
        missing=0,
        empty=0,
    )
