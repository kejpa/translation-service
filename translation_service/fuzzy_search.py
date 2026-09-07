from rapidfuzz import fuzz
from sqlalchemy.orm import Session

from translation_service.fuzzy_match import FuzzyMatch
from translation_service.models import TranslationUnit


def find_fuzzy_matches(
    source_text: str,
    db: Session,
) -> list[FuzzyMatch]:
    translation_units = db.query(TranslationUnit).all()

    matches: list[FuzzyMatch] = []
    for translation_unit in translation_units:
        score = float(
            fuzz.ratio(
                source_text.lower(),
                translation_unit.source_text.lower(),
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
