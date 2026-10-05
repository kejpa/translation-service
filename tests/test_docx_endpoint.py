from io import BytesIO
from pathlib import Path
from zipfile import ZipFile

from docx import Document
from fastapi.testclient import TestClient

from tests.helpers import add_translation
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


def create_docx_with_paragraphs(
    *paragraphs: str,
) -> bytes:
    document = Document()

    for paragraph in paragraphs:
        document.add_paragraph(paragraph)

    stream = BytesIO()

    document.save(stream)

    return stream.getvalue()


def test_parse_valid_docx():
    response = client.post(
        "/api/docx/parse",
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
        "/api/docx/parse",
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
        "/api/docx/parse",
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
                normalized_source_text="Hei maailma",
                normalized_target_text="Hej världen",
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
                normalized_source_text="Hei maailma",
                normalized_target_text="Hej världen",
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
                normalized_source_text="Hei maailma",
                normalized_target_text="Hej världen",
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


def test_llm_translation_document(
    db,
    monkeypatch,
):
    monkeypatch.setattr(
        "translation_service.docx_exporter.translate_text",
        lambda text: ("Tejpning av fler än två fingrar eller tår"),
    )

    source_docx = create_docx_with_paragraphs(
        "SW 27.8\tUseamman kuin kahden sormen teippaus",
    )

    generated_dir = Path.cwd() / "generated"
    generated_dir.mkdir(exist_ok=True)

    source_path = generated_dir / "llm-source.docx"
    translated_path = generated_dir / "llm-translated.docx"

    source_path.write_bytes(source_docx)

    response = client.post(
        "/api/docx/translate",
        files={
            "file": (
                "source.docx",
                source_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    download_url = response.json()["download_url"]

    translated_docx = client.get(
        download_url,
    ).content

    translated_path.write_bytes(
        translated_docx,
    )

    document = Document(
        BytesIO(translated_docx),
    )

    paragraphs = [paragraph.text for paragraph in document.paragraphs]

    assert paragraphs == [
        "SW 27.8\tTejpning av fler än två fingrar eller tår",
    ]


def test_exact_match_same_rule_number_document(
    db,
):
    add_translation(
        db,
        "SW 14.4\tUseamman kuin kahden sormen teippaus",
        "Useamman kuin kahden sormen teippaus",
        "SW 14.4\tTejpning av fler än två fingrar eller tår",
        "Tejpning av fler än två fingrar eller tår",
    )

    source_docx = create_docx_with_paragraphs(
        "SW 14.4\tUseamman kuin kahden sormen teippaus",
    )
    generated_dir = Path.cwd() / "generated"
    generated_dir.mkdir(exist_ok=True)

    source_path = generated_dir / "exact-source.docx"
    translated_path = generated_dir / "exact-translated.docx"

    source_path.write_bytes(source_docx)

    response = client.post(
        "/api/docx/translate",
        files={
            "file": (
                "source.docx",
                source_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    translated_docx = client.get(
        response.json()["download_url"],
    ).content

    translated_path.write_bytes(
        translated_docx,
    )

    document = Document(
        BytesIO(translated_docx),
    )

    paragraphs = [p.text for p in document.paragraphs]

    assert paragraphs == [
        "SW 14.4\tTejpning av fler än två fingrar eller tår",
    ]


def test_exact_match_new_rule_number_document(
    db,
):
    add_translation(
        db,
        "SW 14.4\tUseamman kuin kahden sormen teippaus",
        "Useamman kuin kahden sormen teippaus",
        "SW 14.4\tTejpning av fler än två fingrar eller tår",
        "Tejpning av fler än två fingrar eller tår",
    )

    source_docx = create_docx_with_paragraphs(
        "SW 27.8\tUseamman kuin kahden sormen teippaus",
    )
    generated_dir = Path.cwd() / "generated"
    generated_dir.mkdir(exist_ok=True)

    source_path = generated_dir / "new_number-source.docx"
    translated_path = generated_dir / "new_number-translated.docx"

    source_path.write_bytes(source_docx)

    response = client.post(
        "/api/docx/translate",
        files={
            "file": (
                "source.docx",
                source_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    translated_docx = client.get(
        response.json()["download_url"],
    ).content

    translated_path.write_bytes(
        translated_docx,
    )

    document = Document(
        BytesIO(translated_docx),
    )

    paragraphs = [p.text for p in document.paragraphs]

    assert paragraphs == [
        "SW 27.8\tTejpning av fler än två fingrar eller tår",
    ]
