from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import RGBColor

from translation_service.translation_status import (
    TranslationStatus,
)

GREEN = "00FF00"
YELLOW = "FFFF00"
RED = "FF0000"


def get_border_color(
    status: TranslationStatus,
) -> str | None:
    match status:
        case TranslationStatus.TRANSLATED:
            return None

        case TranslationStatus.EMPTY:
            return None

        case TranslationStatus.FUZZY_HIGH:
            return GREEN

        case TranslationStatus.FUZZY_LOW:
            return YELLOW

        case TranslationStatus.LLM:
            return RED

        case TranslationStatus.MISSING:
            return RED


def get_text_color(
    status: TranslationStatus,
) -> str | None:
    match status:
        case TranslationStatus.TRANSLATED:
            return None

        case TranslationStatus.EMPTY:
            return None

        case TranslationStatus.FUZZY_HIGH:
            return None

        case TranslationStatus.FUZZY_LOW:
            return None

        case TranslationStatus.LLM:
            return None

        case TranslationStatus.MISSING:
            return RED


def apply_status_indicator(
    paragraph,
    status,
):
    border_color = get_border_color(
        status,
    )

    if border_color is not None:
        apply_left_border(
            paragraph,
            border_color,
        )

    text_color = get_text_color(status)
    if text_color is not None:
        apply_text_color(
            paragraph,
            text_color,
        )


def apply_left_border(
    paragraph,
    color: str,
) -> None:
    paragraph_properties = paragraph._p.get_or_add_pPr()

    paragraph_border = OxmlElement(
        "w:pBdr",
    )

    left_border = OxmlElement(
        "w:left",
    )

    left_border.set(
        qn("w:val"),
        "single",
    )

    left_border.set(
        qn("w:sz"),
        "12",
    )

    left_border.set(
        qn("w:space"),
        "4",
    )

    left_border.set(
        qn("w:color"),
        color,
    )

    paragraph_border.append(
        left_border,
    )

    paragraph_properties.append(
        paragraph_border,
    )


def apply_text_color(
    paragraph,
    color: str,
) -> None:
    for run in paragraph.runs:
        run.font.color.rgb = RGBColor.from_string(
            color,
        )
