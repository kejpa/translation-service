from dataclasses import dataclass

from translation_service.models import TranslationUnit


@dataclass
class FuzzyMatch:
    translation_unit: TranslationUnit
    score: float
