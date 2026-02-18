from __future__ import annotations

import enum


class LanguageCode(str, enum.Enum):
    EN = "EN"
    ES = "ES"

    @property
    def display_name(self) -> str:
        return {LanguageCode.EN: "English", LanguageCode.ES: "Español"}[self]
