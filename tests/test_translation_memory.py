from translation_service.models import (
    DocumentPair,
    TranslationUnit,
)
from translation_service.translation_memory import (
    find_exact_match,
)


def test_find_exact_match(db):
    document_pair = DocumentPair(
        source_document="source.docx",
        target_document="target.docx",
    )

    db.add(document_pair)
    db.flush()

    db.add(
        TranslationUnit(
            document_pair_id=document_pair.id,
            source_text="Hei maailma",
            target_text="Hej världen",
        )
    )

    db.commit()

    result = find_exact_match(
        "Hei maailma",
        db,
    )

    assert result == "Hej världen"


def test_returns_none_when_no_match_exists(db):
    result = find_exact_match(
        "Text som inte finns",
        db,
    )

    assert result is None


def test_returns_first_match_when_multiple_exist(db):
    document_pair = DocumentPair(
        source_document="source.docx",
        target_document="target.docx",
    )

    db.add(document_pair)
    db.flush()

    db.add(
        TranslationUnit(
            document_pair_id=document_pair.id,
            source_text="Hei maailma",
            target_text="Hej världen",
        )
    )

    db.add(
        TranslationUnit(
            document_pair_id=document_pair.id,
            source_text="Hei maailma",
            target_text="Hej världen version 2",
        )
    )

    db.commit()

    result = find_exact_match(
        "Hei maailma",
        db,
    )

    assert result == "Hej världen"
