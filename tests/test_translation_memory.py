from translation_service.models import (
    DocumentPair,
    TranslationUnit,
)
from translation_service.translation_memory import (
    find_exact_matches,
)


def test_find_exact_matches(db):
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

    result = find_exact_matches(
        "Hei maailma",
        db,
    )

    assert len(result) == 1

    assert result[0].source_text == "Hei maailma"
    assert result[0].target_text == "Hej världen"


def test_returns_none_when_no_match_exists(db):
    result = find_exact_matches(
        "Text som inte finns",
        db,
    )

    assert result == []


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

    result = find_exact_matches(
        "Hei maailma",
        db,
    )

    assert len(result) == 2

    assert result[0].source_text == "Hei maailma"
    assert result[0].target_text == "Hej världen"

    assert result[1].source_text == "Hei maailma"
    assert result[1].target_text == "Hej världen version 2"


def test_find_exact_matches_is_case_insensitive(db):
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

    result = find_exact_matches(
        "HEI MAAILMA",
        db,
    )

    assert len(result) == 1

    assert result[0].source_text == "Hei maailma"
    assert result[0].target_text == "Hej världen"
