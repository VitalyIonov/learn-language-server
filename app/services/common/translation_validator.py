from lingua import Language, LanguageDetectorBuilder

LANG_CODE_TO_LINGUA: dict[str, Language] = {
    "EN": Language.ENGLISH,
    "ES": Language.SPANISH,
    "RU": Language.RUSSIAN,
}


class TranslationValidatorService:
    _detector = LanguageDetectorBuilder.from_languages(Language.ENGLISH, Language.SPANISH, Language.RUSSIAN).build()

    def is_valid(self, text: str, translated_text: str, lang_to: str) -> bool:
        if translated_text.strip().lower() == text.strip().lower():
            return False

        expected = LANG_CODE_TO_LINGUA.get(lang_to)
        if expected is None:
            return True

        detected = self._detector.detect_language_of(translated_text)
        return detected == expected
