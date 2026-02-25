from app.constants.definition_group import DefinitionGroup

BASE_SCORE = 6

DEFINITION_GROUP_SCORES: dict[DefinitionGroup, int] = {
    DefinitionGroup.VERB: 1,
    DefinitionGroup.NOUN: 1,
    DefinitionGroup.DESCRIPTION: 3,
    DefinitionGroup.PHRASE: 3,
    DefinitionGroup.ILLUSTRATION: 2,
}
