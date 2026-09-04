from sqlalchemy.orm import Session
from sqlalchemy import func

from translation_service.models import TranslationUnit


def find_exact_matches(
    source_text: str,
    db: Session,
) -> list[TranslationUnit]:
    results = (
        db.query(TranslationUnit)
        .filter(func.lower(TranslationUnit.source_text) == source_text.lower())
        .order_by(TranslationUnit.id)
        .all()
    )

    return results
