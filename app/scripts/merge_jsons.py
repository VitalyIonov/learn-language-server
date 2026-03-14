from pathlib import Path
import json
import argparse


def merge_json_folder(folder: Path | str, output_name: str, indent: int = 2) -> Path:
    """Рекурсивно собирает все *.json из folder в один файл на уровне родителя folder.
    Возвращает путь к созданному файлу."""
    folder = Path(folder).resolve()
    if not folder.is_dir():
        raise FileNotFoundError(f"Папка не найдена: {folder}")

    out_path = folder.parent / output_name
    collected = []

    for p in sorted(
        folder.rglob("*.json"), key=lambda x: x.relative_to(folder).as_posix()
    ):
        if p.resolve() == out_path:
            continue
        try:
            with p.open(encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"[WARN] Пропускаю '{p}': некорректный JSON ({e})")
            continue
        except Exception as e:
            print(f"[WARN] Пропускаю '{p}': {e}")
            continue
        if isinstance(data, list):
            collected.extend(data)
        else:
            collected.append(data)

    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", encoding="utf-8") as f:
        json.dump(collected, f, ensure_ascii=False, indent=indent)
    return out_path


LEVEL_ORDER = [
    "A0", "A1.1", "A1.2", "A1.3",
    "A2.1", "A2.2", "A2.3",
    "B1.1", "B1.2", "B1.3",
    "B2.1", "B2.2", "B2.3",
    "C1", "C2",
]
_LEVEL_RANK = {level: index for index, level in enumerate(LEVEL_ORDER)}


def deduplicate_definitions(file_path: Path | str) -> None:
    file_path = Path(file_path)

    with file_path.open(encoding="utf-8") as f:
        definitions = json.load(f)

    seen: dict[tuple[str, str, str, str], dict] = {}
    duplicates_count = 0

    for definition in definitions:
        key = (
            definition.get("text", ""),
            definition.get("category", ""),
            definition.get("group", ""),
            definition.get("language", ""),
        )

        if key in seen:
            existing = seen[key]
            for meaning in definition.get("meanings", []):
                if meaning not in existing["meanings"]:
                    existing["meanings"].append(meaning)

            existing_rank = _LEVEL_RANK.get(existing.get("level", ""), 999)
            new_rank = _LEVEL_RANK.get(definition.get("level", ""), 999)
            if new_rank < existing_rank:
                existing["level"] = definition["level"]

            duplicates_count += 1
        else:
            seen[key] = definition

    if duplicates_count > 0:
        deduplicated = list(seen.values())
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(deduplicated, f, ensure_ascii=False, indent=2)
        print(f"[DEDUP] {file_path.name}: {duplicates_count} дублей объединено, осталось {len(deduplicated)}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("folder", type=Path)
    ap.add_argument("output_name")
    ap.add_argument("--indent", type=int, default=2)
    args = ap.parse_args()
    out = merge_json_folder(args.folder, args.output_name, args.indent)
    print(f"Готово: {out} (элементов: см. файл)")


if __name__ == "__main__":
    main()
