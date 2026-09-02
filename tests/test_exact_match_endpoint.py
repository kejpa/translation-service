from fastapi.testclient import TestClient

from translation_service.main import app
from translation_service.models import (
    DocumentPair,
    TranslationUnit,
)

client = TestClient(app)


def test_exact_match_endpoint_returns_translation(db):
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
            "source_text": "Hei maailma",
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "source_text": "Hei maailma",
        "target_text": "Hej världen",
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
        "target_text": None,
    }
