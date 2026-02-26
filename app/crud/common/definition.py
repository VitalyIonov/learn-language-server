from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Definition
from app.models.common.associations import DefinitionsMeanings
from app.schemas.common import DefinitionStatRow


async def get_definition_stats(db: AsyncSession, category_id: int) -> list[DefinitionStatRow]:
    statement = (
        select(
            Definition.level_id,
            Definition.group,
            DefinitionsMeanings.meaning_id,
            func.count(Definition.id).label("def_count"),
        )
        .join(DefinitionsMeanings, DefinitionsMeanings.definition_id == Definition.id)
        .where(
            Definition.category_id == category_id,
        )
        .group_by(Definition.level_id, Definition.group, DefinitionsMeanings.meaning_id)
    )

    result = await db.execute(statement)
    return [DefinitionStatRow(*row) for row in result.all()]
