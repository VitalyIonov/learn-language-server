import asyncio
from pathlib import Path
from app.scripts.merge_jsons import merge_json_folder
import json
from app.core.db import async_session
from app.db.seed import seed_issue_statuses


def run_merge():
    merge_json_folder(
        folder=Path("seed_data/issue_statuses"),
        output_name="all_issue_statuses.json",
        indent=2,
    )


async def main():
    run_merge()

    with open("seed_data/all_issue_statuses.json", "r") as f:
        question_types_seed_data = json.load(f)

    async with async_session() as session:
        await seed_issue_statuses(session, question_types_seed_data)


if __name__ == "__main__":
    asyncio.run(main())
