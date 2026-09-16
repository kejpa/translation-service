from starlette.testclient import TestClient

from translation_service.main import app
from translation_service.models import TranslationUnit, DocumentPair

client = TestClient(app)


def test_translation_memory_statistics(
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

    db.add(
        TranslationUnit(
            document_pair_id=document_pair.id,
            source_text="Miten voit?",
            target_text="Hur mår du?",
        )
    )

    db.commit()

    response = client.get(
        "/translation-memory/statistics",
    )

    assert response.status_code == 200

    assert response.json() == {
        "document_pairs": 1,
        "translation_units": 2,
    }


def test_translation_memory_statistics_empty_database():
    response = client.get(
        "/translation-memory/statistics",
    )

    assert response.status_code == 200

    assert response.json() == {
        "document_pairs": 0,
        "translation_units": 0,
    }
