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
from dataclasses import dataclass

from translation_service.translation_status import TranslationStatus


@dataclass
class ParagraphTranslation:
    source_text: str
    target_text: str
    status: TranslationStatus


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
) -> list[ParagraphTranslation]:
    translated_paragraphs: list[ParagraphTranslation] = []

    for paragraph in source_paragraphs:
        matches = find_exact_matches(
            paragraph,
            db,
        )

        candidate = select_translation_candidate(matches)

        if candidate is not None:
            translated_paragraphs.append(
                ParagraphTranslation(
                    source_text=paragraph,
                    target_text=candidate.target_text,
                    status=TranslationStatus.TRANSLATED,
                )
            )
        else:
            translated_paragraphs.append(
                ParagraphTranslation(
                    source_text=paragraph,
                    target_text=paragraph,
                    status=TranslationStatus.MISSING,
                )
            )

    return translated_paragraphs


def translate_document(
    source_file: Path,
    output_file: Path,
    db: Session,
) -> None:
    source_paragraphs = extract_all_paragraphs(source_file)

    translations = translate_paragraphs(
        source_paragraphs,
        db,
    )

    create_translated_docx(
        [translation.target_text for translation in translations],
        output_file,
    )
