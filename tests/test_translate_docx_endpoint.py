from fastapi.testclient import TestClient

from tests.helpers import add_translation, create_docx
from translation_service.main import app

client = TestClient(app)


def test_translate_docx_rejects_non_docx_file(
    db,
):
    response = client.post(
        "/docx/translate",
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


def test_translate_docx_rejects_invalid_docx(
    db,
):
    response = client.post(
        "/docx/translate",
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


def test_translate_docx_returns_translation_job_result(
    db,
):
    add_translation(
        db,
        "Hei maailma",
        "Hei maailma",
        "Hej världen",
        "Hej världen",
    )
    db.flush()

    response = client.post(
        "/docx/translate",
        files={
            "file": (
                "source.docx",
                create_docx("Hei maailma"),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    assert response.status_code == 200

    body = response.json()

    assert body["download_url"] == "/downloads/translated.docx"
    assert body["statistics"] == {
        "total_paragraphs": 1,
        "translated": 1,
        "fuzzy_high": 0,
        "fuzzy_low": 0,
        "llm": 0,
        "missing": 0,
        "empty": 0,
    }
