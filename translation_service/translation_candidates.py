from translation_service.models import TranslationUnit


def select_translation_candidate(
    matches: list[TranslationUnit],
) -> TranslationUnit | None:
    if not matches:
        return None

    return matches[0]
