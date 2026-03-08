from __future__ import annotations

import enum


class TargetLanguageCode(str, enum.Enum):
    EN = "EN"
    ES = "ES"
    RU = "RU"

    @property
    def display_name(self) -> str:
        return {TargetLanguageCode.EN: "English", TargetLanguageCode.ES: "Español", TargetLanguageCode.RU: "Русский"}[self]
