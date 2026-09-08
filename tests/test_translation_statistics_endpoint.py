from fastapi.testclient import TestClient

from tests.helpers import add_translation, create_docx
from translation_service.main import app
from translation_service.models import DocumentPair, TranslationUnit

client = TestClient(app)


def test_translation_statistics_endpoint(
    db,
):
    add_translation(
        db,
        "Hei maailma",
        "Hej världen",
    )
    response = client.post(
        "/docx/statistics",
        files={
            "file": (
                "source.docx",
                create_docx(
                    "Hei maailma",
                    "",
                    "Tuntematon teksti",
                ),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "total_paragraphs": 3,
        "translated": 1,
        "fuzzy_high": 0,
        "fuzzy_low": 0,
        "missing": 1,
        "empty": 1,
    }


def test_translation_statistics_rejects_non_docx_file(
    db,
):
    response = client.post(
        "/docx/statistics",
        files={
            "file": (
                "source.txt",
                b"not a docx",
                "text/plain",
            ),
        },
    )

    assert response.status_code == 400

    assert response.json() == {
        "detail": "Only DOCX files are supported",
    }


def test_translation_statistics_rejects_invalid_docx(
    db,
):
    response = client.post(
        "/docx/statistics",
        files={
            "file": (
                "source.docx",
                b"this is not a valid docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    assert response.status_code == 422

    assert response.json() == {
        "detail": "Invalid DOCX file",
    }


def test_translation_statistics_for_empty_document(
    db,
):
    response = client.post(
        "/docx/statistics",
        files={
            "file": (
                "source.docx",
                create_docx(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "total_paragraphs": 0,
        "translated": 0,
        "fuzzy_high": 0,
        "fuzzy_low": 0,
        "missing": 0,
        "empty": 0,
    }


def test_translation_statistics_counts_fuzzy_high_matches(
    db,
    monkeypatch,
):
    monkeypatch.setenv(
        "REUSE_THRESHOLD",
        "85",
    )

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

    response = client.post(
        "/docx/statistics",
        files={
            "file": (
                "source.docx",
                create_docx(
                    "Hei maailma!",
                ),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "total_paragraphs": 1,
        "translated": 0,
        "fuzzy_high": 1,
        "fuzzy_low": 0,
        "missing": 0,
        "empty": 0,
    }


def test_translation_statistics_counts_mixed_translation_statuses(
    db,
    monkeypatch,
):
    monkeypatch.setenv(
        "REUSE_THRESHOLD",
        "85",
    )

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
                source_text="Miten voit",
                target_text="Hur mår du",
            ),
        ]
    )

    db.commit()

    response = client.post(
        "/docx/statistics",
        files={
            "file": (
                "source.docx",
                create_docx(
                    "Hei maailma",  # exact
                    "Miten voit?",  # fuzzy_high
                    "xyz123",  # missing
                    "",  # empty
                ),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    assert response.status_code == 200

    assert response.json() == {
        "total_paragraphs": 4,
        "translated": 1,
        "fuzzy_high": 1,
        "fuzzy_low": 0,
        "missing": 1,
        "empty": 1,
    }
