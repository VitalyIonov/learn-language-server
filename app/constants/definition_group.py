from __future__ import annotations

import enum
from typing import Literal


class DefinitionGroup(str, enum.Enum):
    VERB = "VERB"
    NOUN = "NOUN"
    DESCRIPTION = "DESCRIPTION"
    PHRASE = "PHRASE"
    ILLUSTRATION = "ILLUSTRATION"


TextDefinitionGroup = Literal[
    DefinitionGroup.VERB,
    DefinitionGroup.NOUN,
    DefinitionGroup.DESCRIPTION,
    DefinitionGroup.PHRASE,
]

ImageDefinitionGroup = Literal[DefinitionGroup.ILLUSTRATION]
