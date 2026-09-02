from io import BytesIO

from docx import Document
from fastapi.testclient import TestClient

from translation_service.main import app
from translation_service.models import DocumentPair, TranslationUnit

client = TestClient(app)


def create_docx(*paragraphs: str) -> bytes:
    document = Document()

    for paragraph in paragraphs:
        document.add_paragraph(paragraph)

    stream = BytesIO()
    document.save(stream)

    return stream.getvalue()


def test_import_document_pair(db):
    source_docx = create_docx(
        "Hei maailma",
        "Miten voit?",
    )

    target_docx = create_docx(
        "Hej världen",
        "Hur mår du?",
    )

    response = client.post(
        "/document-pairs/import",
        files={
            "source_file": (
                "source.docx",
                source_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
            "target_file": (
                "target.docx",
                target_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    assert response.status_code == 200

    payload = response.json()

    assert payload["source_document"] == "source.docx"
    assert payload["target_document"] == "target.docx"
    assert payload["imported_segments"] == 2

    document_pairs = db.query(DocumentPair).all()
    units = db.query(TranslationUnit).all()

    assert len(document_pairs) == 1
    assert len(units) == 2

    assert document_pairs[0].source_document == "source.docx"
    assert document_pairs[0].target_document == "target.docx"

    assert units[0].source_text == "Hei maailma"
    assert units[0].target_text == "Hej världen"

    assert units[1].source_text == "Miten voit?"
    assert units[1].target_text == "Hur mår du?"


def test_import_rejects_non_docx_source():
    target_docx = create_docx(
        "Hej världen",
    )

    response = client.post(
        "/document-pairs/import",
        files={
            "source_file": (
                "source.txt",
                b"not a docx",
                "text/plain",
            ),
            "target_file": (
                "target.docx",
                target_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    assert response.status_code == 400

    assert response.json() == {"detail": "Source file must be a DOCX document"}


def test_import_rejects_non_docx_target():
    source_docx = create_docx(
        "Hei maailma",
    )

    response = client.post(
        "/document-pairs/import",
        files={
            "source_file": (
                "source.docx",
                source_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
            "target_file": (
                "target.txt",
                b"not a docx",
                "text/plain",
            ),
        },
    )

    assert response.status_code == 400

    assert response.json() == {"detail": "Target file must be a DOCX document"}


def test_import_rejects_corrupt_source_docx():
    target_docx = create_docx(
        "Hej världen",
    )

    response = client.post(
        "/document-pairs/import",
        files={
            "source_file": (
                "source.docx",
                b"this is not a valid docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
            "target_file": (
                "target.docx",
                target_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    assert response.status_code == 422


def test_import_rejects_corrupt_target_docx():
    source_docx = create_docx(
        "Hei maailma",
    )

    response = client.post(
        "/document-pairs/import",
        files={
            "source_file": (
                "source.docx",
                source_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
            "target_file": (
                "target.docx",
                b"this is not a valid docx",
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    assert response.status_code == 422


def test_import_rejects_different_number_of_segments():
    source_docx = create_docx(
        "Hei maailma",
        "Miten voit?",
    )

    target_docx = create_docx(
        "Hej världen",
    )

    response = client.post(
        "/document-pairs/import",
        files={
            "source_file": (
                "source.docx",
                source_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
            "target_file": (
                "target.docx",
                target_docx,
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            ),
        },
    )

    assert response.status_code == 422

    assert response.json() == {
        "detail": (
            "Source and target documents contain different numbers of paragraphs"
        )
    }
