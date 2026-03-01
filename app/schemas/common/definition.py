from typing import NamedTuple

from app.constants.definition import DefinitionGroup


class DefinitionStatRow(NamedTuple):
    level_id: int
    group: DefinitionGroup
    meaning_id: int
    def_count: int


class CategoryDefinitionStatRow(NamedTuple):
    category_id: int
    level_id: int
    group: DefinitionGroup
    meaning_id: int
    def_count: int
