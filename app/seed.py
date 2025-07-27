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
        await seed_users(session, users_seed_data["users"])
        await seed_categories(session, categories_seed_data["categories"])
        await seed_levels(session, levels_seed_data["levels"])
        await seed_meanings(session, meanings_seed_data["meanings"])
        await seed_definitions(session, definitions_seed_data["definitions"])


if __name__ == "__main__":
    asyncio.run(main())
