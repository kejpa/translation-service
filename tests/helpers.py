from io import BytesIO

from docx import Document
from translation_service.models import DocumentPair, TranslationUnit


def create_docx(*paragraphs: str) -> bytes:
    document = Document()

    for paragraph in paragraphs:
        document.add_paragraph(paragraph)

    stream = BytesIO()
    document.save(stream)

    return stream.getvalue()


def add_translation(
    db,
    source_text: str,
    target_text: str,
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
            source_text=source_text,
            target_text=target_text,
        )
    )

    db.commit()
