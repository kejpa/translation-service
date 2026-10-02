from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.text.paragraph import Paragraph


def extract_paragraphs(file_path: Path) -> list[str]:
    """
    Extract non-empty paragraphs from a DOCX file
    while preserving the document"""
    document = Document(str(file_path))

    renderer = NumberingRenderer()
    paragraphs = []

    for paragraph in iter_paragraphs(document):
        text = paragraph.text.strip()

        if not text:
            continue

        prefix = get_visible_prefix(
            paragraph,
            document,
            renderer,
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
    renderer,
) -> str | None:
    num_id, ilvl, lvl_text = get_visible_prefix_info(
        paragraph,
        document,
    )

    if lvl_text is None:
        return None

    # Regelnumrering
    if "%" in lvl_text and num_id is not None and ilvl is not None:
        return renderer.render(
            num_id,
            int(ilvl),
            lvl_text,
        )

    # Punktlistor
    return lvl_text


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


class NumberingRenderer:
    def __init__(self) -> None:
        self._counters: dict[str, dict[int, int]] = {}

    def render(
        self,
        num_id: str,
        ilvl: int,
        lvl_text: str,
    ) -> str:
        counters = self._counters.setdefault(
            num_id,
            {},
        )

        counters[ilvl] = counters.get(ilvl, 0) + 1

        for level in list(counters.keys()):
            if level > ilvl:
                del counters[level]

        result = lvl_text

        for level in range(ilvl + 1):
            placeholder = f"%{level + 1}"

            if placeholder in result:
                result = result.replace(placeholder, str(counters.get(level, 0)))

        return result


def iter_paragraphs(document):
    body = document.element.body

    for child in body:
        tag = child.tag.split("}")[-1]

        if tag == "p":
            yield Paragraph(child, document)

        elif tag == "sdt":
            sdt_content = child.find(
                ".//{http://schemas.openxmlformats.org/wordprocessingml/2006/main}sdtContent"
            )

            if sdt_content is None:
                continue

            for nested in sdt_content:
                nested_tag = nested.tag.split("}")[-1]

                if nested_tag == "p":
                    yield Paragraph(nested, document)
