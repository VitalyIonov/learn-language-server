from __future__ import annotations

import enum


class InterfaceLanguageCode(str, enum.Enum):
    EN = "EN"
    RU = "RU"
    ES = "ES"
    FR = "FR"
    IT = "IT"

    @property
    def display_name(self) -> str:
        return {
            InterfaceLanguageCode.EN: "English",
            InterfaceLanguageCode.RU: "Русский",
            InterfaceLanguageCode.ES: "Español",
            InterfaceLanguageCode.FR: "Français",
            InterfaceLanguageCode.IT: "Italiano",
        }[self]
