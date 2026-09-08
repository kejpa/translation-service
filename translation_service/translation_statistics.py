from dataclasses import dataclass

from translation_service.docx_exporter import ParagraphTranslation
from translation_service.translation_status import TranslationStatus


@dataclass
class TranslationStatistics:
    total_paragraphs: int
    translated: int
    fuzzy_high: int
    fuzzy_low: int
    missing: int
    empty: int


def calculate_translation_statistics(
    paragraphs: list[ParagraphTranslation],
) -> TranslationStatistics:
    translated = 0
    fuzzy_high = 0
    fuzzy_low = 0
    missing = 0
    empty = 0

    for paragraph in paragraphs:
        if paragraph.status == TranslationStatus.TRANSLATED:
            translated += 1
        elif paragraph.status == TranslationStatus.FUZZY_HIGH:
            fuzzy_high += 1
        elif paragraph.status == TranslationStatus.FUZZY_LOW:
            fuzzy_low += 1
        elif paragraph.status == TranslationStatus.MISSING:
            missing += 1
        elif paragraph.status == TranslationStatus.EMPTY:
            empty += 1

    return TranslationStatistics(
        total_paragraphs=len(paragraphs),
        translated=translated,
        fuzzy_high=fuzzy_high,
        fuzzy_low=fuzzy_low,
        missing=missing,
        empty=empty,
    )
