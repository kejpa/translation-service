from sqlalchemy.orm import Session

from translation_service.models import TranslationUnit


def find_exact_match(
    source_text: str,
    db: Session,
) -> str | None:
    result = (
        db.query(TranslationUnit)
        .filter(TranslationUnit.source_text == source_text)
        .first()
    )

    if result is None:
        return None

    return result.target_text
