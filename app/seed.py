import asyncio
import json
from app.core.db import async_session
from app.db.seed import (
    seed_users,
    seed_categories,
    seed_levels,
    seed_meanings,
    seed_definitions,
)
from app.core.dependencies.admin import get_image_service, get_storage_r2_service


from app.core.config import settings

print(settings.database_uri)


async def main():
    with open("seed_data/users.json", "r") as f:
        users_seed_data = json.load(f)

    with open("seed_data/categories.json", "r") as f:
        categories_seed_data = json.load(f)

    with open("seed_data/levels.json", "r") as f:
        levels_seed_data = json.load(f)

    with open("seed_data/meanings.json", "r") as f:
        meanings_seed_data = json.load(f)

    with open("seed_data/definitions.json", "r") as f:
        definitions_seed_data = json.load(f)

    async with async_session() as session:
        storage_service = await get_storage_r2_service()
        image_service = await get_image_service(
            db=session, svc_storage_r2=storage_service
        )

        await seed_users(session, users_seed_data["users"])
        await seed_categories(
            session,
            categories_seed_data["categories"],
            storage_service,
            image_service,
        )
        await seed_levels(session, levels_seed_data["levels"])
        await seed_meanings(session, meanings_seed_data["meanings"])
        await seed_definitions(session, definitions_seed_data["definitions"])


if __name__ == "__main__":
    asyncio.run(main())
