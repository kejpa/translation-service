from docx import Document


def extract_paragraphs(file_path: str) -> list[str]:
    """
    Extract non-empty paragraphs from a DOCX file
    while preserving document"""
    document = Document(file_path)

    return [
        paragraph.text.strip()
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]
