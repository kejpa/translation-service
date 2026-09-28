from pathlib import Path

from docx import Document

WORDPROCESSINGML_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


class NumberingState:
    def __init__(self) -> None:
        self.counters: dict[int, int] = {}

    def next(self, level: int) -> str:
        self.counters[level] = self.counters.get(level, 0) + 1

        levels_to_remove = [key for key in self.counters if key > level]

        for key in levels_to_remove:
            del self.counters[key]

        return ".".join(str(self.counters[i]) for i in sorted(self.counters)) + "."


def get_numbering_info(
    paragraph,
) -> tuple[str | None, str | None]:
    num_pr = paragraph._element.find(
        f".//{{{WORDPROCESSINGML_NS}}}numPr",
    )

    if num_pr is None:
        return None, None

    ilvl = num_pr.find(
        f"{{{WORDPROCESSINGML_NS}}}ilvl",
    )

    num_id = num_pr.find(
        f"{{{WORDPROCESSINGML_NS}}}numId",
    )

    return (
        num_id.get(f"{{{WORDPROCESSINGML_NS}}}val") if num_id is not None else None,
        ilvl.get(f"{{{WORDPROCESSINGML_NS}}}val") if ilvl is not None else None,
    )


def extract_paragraphs(
    file_path: Path,
) -> list[str]:
    """
    Extract non-empty paragraphs from a DOCX file
    while preserving the document.
    """
    document = Document(str(file_path))

    paragraphs: list[str] = []
    numbering_state = NumberingState()

    for paragraph in document.paragraphs:
        text = paragraph.text.strip()

        if not text:
            continue

        num_id, ilvl = get_numbering_info(
            paragraph,
        )

        fmt = (
            get_numbering_format(
                document,
                num_id,
            )
            if num_id is not None
            else None
        )

        if fmt is not None:
            prefix = fmt
        elif ilvl is not None:
            prefix = numbering_state.next(
                int(ilvl),
            )
        else:
            prefix = ""

        if prefix:
            text = f"{prefix}\t{text}"

        paragraphs.append(text)

    return paragraphs


def extract_all_paragraphs(
    file_path: Path,
) -> list[str]:
    document = Document(str(file_path))

    return [paragraph.text for paragraph in document.paragraphs]


def get_numbering_format(
    document,
    num_id: str,
) -> str | None:
    numbering = document.part.numbering_part.element

    for num in numbering.findall(f".//{{{WORDPROCESSINGML_NS}}}num"):
        if num.get(f"{{{WORDPROCESSINGML_NS}}}numId") != num_id:
            continue

        abstract_num_id = num.find(f"{{{WORDPROCESSINGML_NS}}}abstractNumId")

        if abstract_num_id is None:
            return None

        abstract_id = abstract_num_id.get(f"{{{WORDPROCESSINGML_NS}}}val")

        for abstract_num in numbering.findall(
            f".//{{{WORDPROCESSINGML_NS}}}abstractNum"
        ):
            if (
                abstract_num.get(f"{{{WORDPROCESSINGML_NS}}}abstractNumId")
                != abstract_id
            ):
                continue

            lvl_text = abstract_num.find(f".//{{{WORDPROCESSINGML_NS}}}lvlText")

            if lvl_text is not None:
                return lvl_text.get(f"{{{WORDPROCESSINGML_NS}}}val")

    return None
