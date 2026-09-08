from translation_service.fuzzy_search import find_fuzzy_matches
from translation_service.models import DocumentPair, TranslationUnit


def test_fuzzy_match_returns_exact_match_with_highest_score(
    db,
):
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

    matches = find_fuzzy_matches(
        "Hei maailma",
        db,
    )

    assert len(matches) == 1

    assert matches[0].translation_unit.target_text == "Hej världen"
    assert matches[0].score == 100.0


def test_fuzzy_match_returns_empty_list_for_empty_tm(
    db,
):
    matches = find_fuzzy_matches(
        "Hei maailma",
        db,
    )

    assert matches == []


def test_fuzzy_matches_are_sorted_by_score(
    db,
):
    document_pair = DocumentPair(
        source_document="source.docx",
        target_document="target.docx",
    )

    db.add(document_pair)
    db.flush()

    db.add_all(
        [
            TranslationUnit(
                document_pair_id=document_pair.id,
                source_text="Hei maailma",
                target_text="Hej världen",
            ),
            TranslationUnit(
                document_pair_id=document_pair.id,
                source_text="Hei maailmaa",
                target_text="Hej världen!",
            ),
            TranslationUnit(
                document_pair_id=document_pair.id,
                source_text="Terve maailma",
                target_text="God dag världen",
            ),
        ]
    )

    db.commit()

    matches = find_fuzzy_matches(
        "Hei maailma",
        db,
    )

    scores = [match.score for match in matches]

    assert scores == sorted(
        scores,
        reverse=True,
    )
