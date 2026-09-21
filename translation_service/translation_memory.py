from sqlalchemy import func
from sqlalchemy.orm import Session

from translation_service.models import TranslationUnit
from translation_service.normalization import normalize_text


def find_exact_matches(
    source_text: str,
    db: Session,
) -> list[TranslationUnit]:
    normalized_source_text = normalize_text(
        source_text,
    )

    print(f"Searching for: '{normalized_source_text}'")

    normalized_source_text = normalize_text(
        source_text,
    )

    results = (
        db.query(TranslationUnit)
        .filter(
            func.lower(
                TranslationUnit.normalized_source_text,
            )
            == normalized_source_text.lower(),
        )
        .order_by(TranslationUnit.id)
        .all()
    )
    print(f"Matches: {len(results)}")
    return results
