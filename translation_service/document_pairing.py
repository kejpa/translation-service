from collections.abc import Sequence

from pathlib import Path

from translation_service.docx_parser import extract_paragraphs
from sqlalchemy.orm import Session
from translation_service.models import DocumentPair, TranslationUnit


def pair_paragraphs(
    source_paragraphs: Sequence[str],
    target_paragraphs: Sequence[str],
) -> list[tuple[str, str]]:
    if len(source_paragraphs) != len(target_paragraphs):
        raise ValueError(
            "Source and target documents contain different numbers of paragraphs"
        )

    return list(zip(source_paragraphs, target_paragraphs, strict=True))


def import_document_pair(
    source_file: str | Path,
    target_file: str | Path,
) -> list[tuple[str, str]]:
    source_paragraphs = extract_paragraphs(source_file)
    target_paragraphs = extract_paragraphs(target_file)

    return pair_paragraphs(
        source_paragraphs,
        target_paragraphs,
    )


def save_document_pairs(
    source_document: str,
    target_document: str,
    pairs: list[tuple[str, str]],
    db: Session,
) -> int:
    document_pair = DocumentPair(
        source_document=source_document,
        target_document=target_document,
    )

    db.add(document_pair)
    db.flush()

    for source_text, target_text in pairs:
        db.add(
            TranslationUnit(
                document_pair_id=document_pair.id,
                source_text=source_text,
                target_text=target_text,
            )
        )

    db.commit()

    return len(pairs)


def import_and_save_document_pair(
    source_path: str | Path,
    target_path: str | Path,
    source_filename: str,
    target_filename: str,
    db: Session,
) -> int:
    pairs = import_document_pair(
        source_path,
        target_path,
    )

    return save_document_pairs(
        source_filename,
        target_filename,
        pairs,
        db,
    )
