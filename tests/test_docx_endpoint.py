from io import BytesIO
from zipfile import ZipFile

from docx import Document
from fastapi.testclient import TestClient

from translation_service.docx_exporter import (
    ParagraphTranslation,
    build_translated_document,
)
from translation_service.main import app
from translation_service.translation_status import (
    TranslationStatus,
)

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


def test_build_translated_document_applies_fuzzy_high_indicator():
    document = build_translated_document(
        [
            ParagraphTranslation(
                source_text="Hei maailma",
                target_text="Hej världen",
                status=TranslationStatus.FUZZY_HIGH,
            ),
        ]
    )

    buffer = BytesIO()
    document.save(buffer)

    with ZipFile(
        BytesIO(buffer.getvalue()),
    ) as docx:
        xml = docx.read(
            "word/document.xml",
        ).decode(
            "utf-8",
        )

    assert "00FF00" in xml


def test_build_translated_document_applies_llm_indicator():
    document = build_translated_document(
        [
            ParagraphTranslation(
                source_text="Hei maailma",
                target_text="Hej världen",
                status=TranslationStatus.LLM,
            ),
        ]
    )

    buffer = BytesIO()
    document.save(buffer)

    with ZipFile(
        BytesIO(buffer.getvalue()),
    ) as docx:
        xml = docx.read(
            "word/document.xml",
        ).decode(
            "utf-8",
        )

    assert "FF0000" in xml


def test_build_translated_document_does_not_apply_indicator_for_translated():
    document = build_translated_document(
        [
            ParagraphTranslation(
                source_text="Hei maailma",
                target_text="Hej världen",
                status=TranslationStatus.TRANSLATED,
            ),
        ]
    )

    buffer = BytesIO()
    document.save(buffer)

    with ZipFile(
        BytesIO(buffer.getvalue()),
    ) as docx:
        xml = docx.read(
            "word/document.xml",
        ).decode(
            "utf-8",
        )

    assert "00FF00" not in xml
    assert "FFFF00" not in xml
    assert "FF0000" not in xml
