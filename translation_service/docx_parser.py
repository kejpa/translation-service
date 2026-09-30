from pathlib import Path

from docx import Document
from docx.oxml.ns import qn


def extract_paragraphs(file_path: Path) -> list[str]:
    """
    Extract non-empty paragraphs from a DOCX file
    while preserving the document"""
    document = Document(str(file_path))
    paragraphs = []

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if not text:
            continue

        prefix = get_visible_prefix(
            paragraph,
            document,
        )

        if prefix:
            text = f"{prefix} {text}"

        paragraphs.append(text)

    return paragraphs


def extract_all_paragraphs(
    file_path: Path,
) -> list[str]:
    document = Document(str(file_path))

    return [paragraph.text for paragraph in document.paragraphs]


def get_visible_prefix(
    paragraph,
    document,
) -> str | None:
    _, _, lvl_text = get_visible_prefix_info(
        paragraph,
        document,
    )

    if lvl_text is None:
        return None

    if "%" in lvl_text:
        return None

    return lvl_text


def get_paragraph_metadata(
    paragraph,
    document,
) -> dict[str, str | None]:
    num_id, ilvl, lvl_text = get_visible_prefix_info(
        paragraph,
        document,
    )

    return {
        "text": paragraph.text.strip(),
        "num_id": num_id,
        "ilvl": ilvl,
        "lvl_text": lvl_text,
    }


def get_visible_prefix_info(
    paragraph,
    document,
) -> tuple[str | None, str | None, str | None]:
    ppr = paragraph._element.find(qn("w:pPr"))

    if ppr is None:
        return None, None, None

    num_pr = ppr.find(qn("w:numPr"))

    if num_pr is None:
        return None, None, None

    ilvl_element = num_pr.find(qn("w:ilvl"))
    numid_element = num_pr.find(qn("w:numId"))

    if ilvl_element is None or numid_element is None:
        return None, None, None

    ilvl = ilvl_element.get(qn("w:val"))
    num_id = numid_element.get(qn("w:val"))

    numbering = document.part.numbering_part.element

    abstract_num_id = None

    for num in numbering.findall(qn("w:num")):
        if num.get(qn("w:numId")) == num_id:
            abstract_element = num.find(qn("w:abstractNumId"))

            if abstract_element is not None:
                abstract_num_id = abstract_element.get(
                    qn("w:val"),
                )

            break

    if abstract_num_id is None:
        return num_id, ilvl, None

    for abstract_num in numbering.findall(
        qn("w:abstractNum"),
    ):
        if (
            abstract_num.get(
                qn("w:abstractNumId"),
            )
            != abstract_num_id
        ):
            continue

        for lvl in abstract_num.findall(
            qn("w:lvl"),
        ):
            if lvl.get(qn("w:ilvl")) != ilvl:
                continue

            lvl_text_element = lvl.find(
                qn("w:lvlText"),
            )

            if lvl_text_element is None:
                return num_id, ilvl, None

            return (
                num_id,
                ilvl,
                lvl_text_element.get(
                    qn("w:val"),
                ),
            )

    return num_id, ilvl, None
