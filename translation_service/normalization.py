import re

NORMALIZATION_RULES = [
    re.compile(
        r"^SW\s+\d+(?:\.\d+)*\s+",
        re.IGNORECASE,
    ),
]


def normalize_text(
    text: str,
) -> str:
    normalized = text

    for rule in NORMALIZATION_RULES:
        normalized = rule.sub(
            "",
            normalized,
        )

    return normalized.strip()


def extract_prefix(
    text: str,
) -> tuple[str, str]:
    normalized = normalize_text(text)

    if normalized == text:
        return "", text

    prefix = text.removesuffix(
        normalized,
    ).strip()

    return prefix, normalized


def rebuild_text(
    prefix: str,
    text: str,
) -> str:
    if not prefix:
        return text

    return f"{prefix}\t{text}"
