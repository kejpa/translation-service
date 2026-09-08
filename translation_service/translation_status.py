from enum import StrEnum


class TranslationStatus(StrEnum):
    TRANSLATED = "translated"
    FUZZY_HIGH = "fuzzy_high"
    FUZZY_LOW = "fuzzy_low"
    MISSING = "missing"
    EMPTY = "empty"
