from enum import StrEnum


class TranslationStatus(StrEnum):
    TRANSLATED = "translated"
    FUZZY_HIGH = "fuzzy_high"
    MISSING = "missing"
    EMPTY = "empty"
