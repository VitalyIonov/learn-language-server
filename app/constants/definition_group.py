from __future__ import annotations

import enum


class DefinitionGroup(str, enum.Enum):
    VERB = "VERB"
    NOUN = "NOUN"
    DESCRIPTION = "DESCRIPTION"
    PHRASE = "PHRASE"
