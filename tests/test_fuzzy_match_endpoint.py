from starlette.testclient import TestClient

from translation_service.main import app
from translation_service.models import DocumentPair, TranslationUnit

client = TestClient(app)


def test_fuzzy_match_endpoint_returns_matches_sorted_by_score(
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

    response = client.get(
        "/translations/fuzzy",
        params={
            "source_text": "Hei maailma",
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["source_text"] == "Hei maailma"

    scores = [match["score"] for match in payload["matches"]]

    assert scores == sorted(
        scores,
        reverse=True,
    )


def test_fuzzy_match_endpoint_returns_empty_list_when_no_matches(
    db,
):
    response = client.get(
        "/translations/fuzzy",
        params={
            "source_text": "Hei maailma",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "source_text": "Hei maailma",
        "matches": [],
    }
