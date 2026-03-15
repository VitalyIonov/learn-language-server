import argparse
import asyncio
import json
import logging
from pathlib import Path

from app.services.common import TranslateService

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

SEED_DATA_DIR = Path("seed_data/v2")
DEFINITIONS_DIR = SEED_DATA_DIR / "definitions"
MEANINGS_DIR = SEED_DATA_DIR / "meanings"


def load_meanings(category: str, language: str) -> list[str]:
    path = MEANINGS_DIR / category / language.upper() / "meanings.json"
    with open(path, encoding="utf-8") as file:
        return [item["name"] for item in json.load(file)]


def build_meaning_map(category: str, lang_from: str, lang_to: str) -> dict[str, str]:
    source_meanings = load_meanings(category=category, language=lang_from)
    target_meanings = load_meanings(category=category, language=lang_to)

    if len(source_meanings) != len(target_meanings):
        raise ValueError(f"Meaning count mismatch: {lang_from} has {len(source_meanings)}, " f"{lang_to} has {len(target_meanings)}")

    return dict(zip(source_meanings, target_meanings))


def load_source_definitions(category: str, lang_from: str, group: str) -> dict[str, list[dict]]:
    source_dir = DEFINITIONS_DIR / category / lang_from.upper() / group
    if not source_dir.exists():
        raise FileNotFoundError(f"Source directory not found: {source_dir}")

    definitions_by_file: dict[str, list[dict]] = {}
    for json_file in sorted(source_dir.glob("*.json")):
        with open(json_file, encoding="utf-8") as file:
            definitions_by_file[json_file.name] = json.load(file)

    return definitions_by_file


async def translate_definitions(
    category: str,
    group: str,
    lang_from: str,
    lang_to: str,
) -> None:
    svc_translate = TranslateService()
    meaning_map = build_meaning_map(category=category, lang_from=lang_from, lang_to=lang_to)
    definitions_by_file = load_source_definitions(category=category, lang_from=lang_from, group=group)

    target_dir = DEFINITIONS_DIR / category / lang_to.upper() / group
    target_dir.mkdir(parents=True, exist_ok=True)

    for filename, definitions in definitions_by_file.items():
        translated_definitions = []

        for definition in definitions:
            context = f"{', '.join(definition.get('meanings', []))} - {definition.get('category', '')}"

            translated_text = await svc_translate.translate_by_open_ai(
                text=definition["text"],
                lang_from=lang_from,
                lang_to=lang_to,
                context=context,
                group=group.upper(),
            )

            translated_meanings = [meaning_map[meaning] for meaning in definition.get("meanings", []) if meaning in meaning_map]

            translated_definition = {
                "text": translated_text,
                "level": definition["level"],
                "category": definition["category"],
                "meanings": translated_meanings,
                "type": definition["type"],
                "group": definition["group"],
                "language": lang_to.upper(),
            }
            translated_definitions.append(translated_definition)

            logger.info("%s → %s (%s)", definition["text"], translated_text, lang_to.upper())

        output_path = target_dir / filename
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(translated_definitions, file, ensure_ascii=False, indent=2)
            file.write("\n")

        logger.info("Записан %s (%d definitions)", output_path, len(translated_definitions))


async def main() -> None:
    parser = argparse.ArgumentParser(description="Translate seed definition files")
    parser.add_argument("--category", required=True, help="Category folder name (e.g. rooms_in_a_house)")
    parser.add_argument("--group", required=True, help="Definition group (e.g. verb, noun, phrase, descriptions)")
    parser.add_argument("--lang-from", default="ru", help="Source language code (default: ru)")
    parser.add_argument("--lang-to", nargs="+", required=True, help="Target language codes (e.g. en es)")
    args = parser.parse_args()

    for lang_to in args.lang_to:
        logger.info("=== Перевод %s → %s ===", args.lang_from.upper(), lang_to.upper())
        await translate_definitions(
            category=args.category,
            group=args.group,
            lang_from=args.lang_from,
            lang_to=lang_to,
        )

    logger.info("Готово!")


if __name__ == "__main__":
    asyncio.run(main())
