from app.constants.definition import DefinitionGroup

DEFINITION_GROUP_SCORES: dict[DefinitionGroup, int] = {
    DefinitionGroup.VERB: 1,
    DefinitionGroup.NOUN: 1,
    DefinitionGroup.DESCRIPTION: 3,
    DefinitionGroup.PHRASE: 3,
    DefinitionGroup.ILLUSTRATION: 2,
}
