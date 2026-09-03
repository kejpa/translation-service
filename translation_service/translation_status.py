from enum import StrEnum


class TranslationStatus(StrEnum):
    TRANSLATED = "translated"
    MISSING = "missing"
    EMPTY = "empty"
