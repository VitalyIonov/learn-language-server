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
