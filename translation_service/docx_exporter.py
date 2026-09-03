from pathlib import Path

from docx import Document
from sqlalchemy.orm import Session

from translation_service.docx_parser import extract_all_paragraphs
from translation_service.translation_memory import (
    find_exact_matches,
)
from translation_service.translation_candidates import (
    select_translation_candidate,
)


def create_translated_docx(
    paragraphs: list[str],
    output_file: Path,
) -> None:
    document = Document()

    for paragraph in paragraphs:
        document.add_paragraph(paragraph)

    document.save(str(output_file))


def translate_paragraphs(
    source_paragraphs: list[str],
    db: Session,
) -> list[str]:
    translated_paragraphs: list[str] = []

    for paragraph in source_paragraphs:
        matches = find_exact_matches(
            paragraph,
            db,
        )

        candidate = select_translation_candidate(matches)

        if candidate:
            translated_text = candidate.target_text
        else:
            translated_text = paragraph

        translated_paragraphs.append(translated_text)

    return translated_paragraphs


def translate_document(
    source_file: Path,
    output_file: Path,
    db: Session,
) -> None:
    source_paragraphs = extract_all_paragraphs(source_file)

    translated_paragraphs = translate_paragraphs(
        source_paragraphs,
        db,
    )

    create_translated_docx(
        translated_paragraphs,
        output_file,
    )
