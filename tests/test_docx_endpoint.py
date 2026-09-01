from io import BytesIO

from docx import Document
from fastapi.testclient import TestClient

from translation_service.main import app

client = TestClient(app)


def create_docx() -> bytes:
    document = Document()
    document.add_paragraph("Första stycket")

    stream = BytesIO()
    document.save(stream)

    return stream.getvalue()


def test_parse_valid_docx():
    response = client.post(
        "/docx/parse",
        files={
            "file": (
                "test.docx",
                create_docx(),
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["paragraph_count"] == 1
    assert payload["paragraphs"] == ["Första stycket"]


def test_parse_rejects_non_docx():
    response = client.post(
        "/docx/parse",
        files={
            "file": (
                "test.txt",
                b"hello world",
                "text/plain",
            )
        },
    )

    assert response.status_code == 400
    assert response.json() == {"detail": "Only DOCX files are supported"}


def test_parse_rejects_corrupt_docx():
    response = client.post(
        "/docx/parse",
        files={
            "file": (
                "broken.docx",
                b"this is not a real docx file",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            )
        },
    )

    assert response.status_code == 422
    assert response.json() == {"detail": "Invalid DOCX file"}
