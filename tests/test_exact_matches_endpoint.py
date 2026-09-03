from fastapi.testclient import TestClient

from translation_service.main import app
from translation_service.models import (
    DocumentPair,
    TranslationUnit,
)

client = TestClient(app)


def test_exact_matches_endpoint_is_case_insensitive(db):
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

    response = client.get(
        "/translations/exact",
        params={
            "source_text": "hei maailma",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "source_text": "hei maailma",
        "matches": [
            "Hej världen",
        ],
    }


def test_exact_match_endpoint_is_case_insensitive_uppercase(db):
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

    response = client.get(
        "/translations/exact",
        params={
            "source_text": "HEI MAAILMA",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "source_text": "HEI MAAILMA",
        "matches": ["Hej världen"],
    }


def test_exact_match_endpoint_returns_null_when_not_found(db):
    response = client.get(
        "/translations/exact",
        params={
            "source_text": "Finns inte",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "source_text": "Finns inte",
        "matches": [],
    }
