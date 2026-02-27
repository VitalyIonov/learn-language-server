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

FALSE_DEFINITIONS_COUNT: dict[DefinitionGroup, int] = {
    DefinitionGroup.ILLUSTRATION: 3,
    DefinitionGroup.VERB: 2,
    DefinitionGroup.NOUN: 2,
    DefinitionGroup.DESCRIPTION: 2,
    DefinitionGroup.PHRASE: 2,
}
