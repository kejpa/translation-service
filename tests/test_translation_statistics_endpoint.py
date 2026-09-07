from fastapi.testclient import TestClient

from tests.helpers import add_translation, create_docx
from translation_service.main import app

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
