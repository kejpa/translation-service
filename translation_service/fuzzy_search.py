from rapidfuzz import fuzz
from sqlalchemy.orm import Session

from translation_service.fuzzy_match import FuzzyMatch
from translation_service.models import TranslationUnit
from translation_service.normalization import normalize_text


def find_fuzzy_matches(
    source_text: str,
    db: Session,
) -> list[FuzzyMatch]:
    translation_units = db.query(TranslationUnit).all()

    normalized_source_text = normalize_text(
        source_text,
    )
    matches: list[FuzzyMatch] = []
    for translation_unit in translation_units:
        score = float(
            fuzz.ratio(
                translation_unit.normalized_source_text,
                normalized_source_text,
            )
        )

        matches.append(
            FuzzyMatch(
                translation_unit=translation_unit,
                score=score,
            )
        )

    matches.sort(
        key=lambda match: match.score,
        reverse=True,
    )

    return matches
