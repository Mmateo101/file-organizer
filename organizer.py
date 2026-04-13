import os
import shutil
from pathlib import Path

DOWNLOADS = Path(r"C:\Users\mateo\Downloads")

CATEGORIES = {
    "Images":    {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "Documents": {".pdf", ".doc", ".docx"},
    "Videos":    {".mp4", ".mov", ".avi"},
    "Audio":     {".mp3", ".wav"},
}


def categorize(file: Path) -> str:
    ext = file.suffix.lower()
    for folder, extensions in CATEGORIES.items():
        if ext in extensions:
            return folder
    return "Other"


def build_plan() -> list[tuple[Path, Path]]:
    """Return a list of (source, destination) pairs for all files to move."""
    plan = []
    for entry in DOWNLOADS.iterdir():
        if entry.is_file():
            dest_folder = DOWNLOADS / categorize(entry)
            dest = dest_folder / entry.name
            # Avoid moving files that are already in the right place
            if entry.parent != dest_folder:
                plan.append((entry, dest))
    return sorted(plan, key=lambda t: (categorize(t[0]), t[0].name))


def preview(plan: list[tuple[Path, Path]]) -> None:
    if not plan:
        print("Nothing to organize — Downloads folder is already tidy.")
        return

    current_folder = None
    for src, dest in plan:
        folder = dest.parent.name
        if folder != current_folder:
            print(f"\n  [{folder}]")
            current_folder = folder
        print(f"    {src.name}")
    print()


def execute(plan: list[tuple[Path, Path]]) -> None:
    moved = 0
    for src, dest in plan:
        dest.parent.mkdir(exist_ok=True)
        # Handle name collisions by appending a counter
        if dest.exists():
            stem, suffix = dest.stem, dest.suffix
            counter = 1
            while dest.exists():
                dest = dest.parent / f"{stem} ({counter}){suffix}"
                counter += 1
        shutil.move(str(src), str(dest))
        moved += 1
    print(f"Done. Moved {moved} file(s).")


def main() -> None:
    print(f"Scanning: {DOWNLOADS}\n")
    plan = build_plan()

    if not plan:
        print("Nothing to organize — Downloads folder is already tidy.")
        return

    print(f"Found {len(plan)} file(s) to move:\n")
    preview(plan)

    answer = input("Proceed? [y/N] ").strip().lower()
    if answer == "y":
        execute(plan)
    else:
        print("Aborted — no files were moved.")


if __name__ == "__main__":
    main()
