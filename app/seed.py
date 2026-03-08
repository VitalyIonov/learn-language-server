import asyncio
from pathlib import Path
from app.scripts.merge_jsons import merge_json_folder
import json
from app.core.db import async_session
from app.db.seed import (
    seed_users,
    seed_categories,
    seed_levels,
    seed_meanings,
    seed_definitions,
)
from app.core.dependencies.service_factories import (
    get_image_service,
    get_storage_r2_service,
)


def run_merge():
    merge_json_folder(
        folder=Path("seed_data/v2/definitions"),
        output_name="all_definitions.json",
        indent=2,
    )
    merge_json_folder(folder=Path("seed_data/v2/categories"), output_name="all_categories.json", indent=2)
    merge_json_folder(folder=Path("seed_data/v2/levels"), output_name="all_levels.json", indent=2)
    merge_json_folder(folder=Path("seed_data/v2/meanings"), output_name="all_meanings.json", indent=2)
    # merge_json_folder(folder=Path("seed_data/v2/users"), output_name="all_users.json", indent=2)


async def main():
    run_merge()

    # with open("seed_data/v2/all_users.json", "r") as f:
    #     users_seed_data = json.load(f)

    with open("seed_data/v2/all_categories.json", "r") as f:
        categories_seed_data = json.load(f)

    with open("seed_data/v2/all_levels.json", "r") as f:
        levels_seed_data = json.load(f)

    with open("seed_data/v2/all_meanings.json", "r") as f:
        meanings_seed_data = json.load(f)

    with open("seed_data/v2/all_definitions.json", "r") as f:
        definitions_seed_data = json.load(f)

    async with async_session() as session:
        storage_service = await get_storage_r2_service()
        image_service = await get_image_service(db=session, svc_storage_r2=storage_service)

        await seed_categories(
            session,
            categories_seed_data,
            image_service,
        )
        await seed_levels(session, levels_seed_data)
        await seed_meanings(session, meanings_seed_data)
        await seed_definitions(
            session,
            definitions_seed_data,
            image_service,
        )
        # await seed_users(session, users_seed_data)


if __name__ == "__main__":
    asyncio.run(main())
