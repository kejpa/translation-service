from pathlib import Path

from docx import Document


def extract_paragraphs(file_path: Path) -> list[str]:
    """
    Extract non-empty paragraphs from a DOCX file
    while preserving the document"""
    document = Document(str(file_path))

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if not text:
            continue

        num_pr = paragraph._element.find(
            ".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numPr"
        )

        if num_pr is None:
            continue

        ilvl = num_pr.find(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}ilvl"
        )

        num_id = num_pr.find(
            "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}numId"
        )

        print()
        print("TEXT:")
        print(repr(text))

        print(
            "ILVL:",
            ilvl.get(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"
            )
            if ilvl is not None
            else None,
        )

        print(
            "NUM_ID:",
            num_id.get(
                "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}val"
            )
            if num_id is not None
            else None,
        )

        print()
        print("NUM_PR XML:")
        print(num_pr.xml)

    return [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]


def extract_all_paragraphs(
    file_path: Path,
) -> list[str]:
    document = Document(str(file_path))

    return [paragraph.text for paragraph in document.paragraphs]
