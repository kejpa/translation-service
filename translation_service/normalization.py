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
