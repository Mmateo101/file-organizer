import argparse
import shutil
import time
from pathlib import Path

DOWNLOADS = Path(r"C:\Users\mateo\Downloads")
RECENT_FOLDER = "Recent Downloads (this week)"
RECENT_DAYS = 5

CATEGORIES = {
    "Images":     {".jpg", ".jpeg", ".png", ".gif", ".webp"},
    "Documents":  {".pdf"},
    "Work":       {".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx"},
    "Videos":     {".mp4", ".mov", ".avi"},
    "Audio":      {".mp3", ".wav"},
    "Compressed": {".zip", ".rar"},
    "Code":       {".py", ".r", ".rmd", ".cpp", ".h", ".m"},
}

# Subfolders to scan for mis-categorized files. Excludes RECENT_FOLDER and any
# folders that should never be touched (e.g. Trash).
SKIP_RESCAN = {RECENT_FOLDER, "Trash"}


def is_recent(file: Path) -> bool:
    age_seconds = time.time() - file.stat().st_ctime
    return age_seconds < RECENT_DAYS * 86400


def categorize(file: Path) -> str:
    ext = file.suffix.lower()
    for folder, extensions in CATEGORIES.items():
        if ext in extensions:
            return folder
    return "Other"


def build_plan(rescan_subfolders: bool = True) -> list[tuple[Path, Path]]:
    """Return a list of (source, destination) pairs for all files to move.

    rescan_subfolders=True  — also checks already-sorted folders for
                              mis-categorized files (interactive mode).
    rescan_subfolders=False — only processes loose files in the Downloads root
                              and graduates aged-out files from Recent
                              (silent/startup mode).
    """
    plan = []

    # Files sitting directly in Downloads root
    for entry in DOWNLOADS.iterdir():
        if entry.is_file():
            dest_folder = DOWNLOADS / (RECENT_FOLDER if is_recent(entry) else categorize(entry))
            if entry.parent != dest_folder:
                plan.append((entry, dest_folder / entry.name))

    # Files in Recent that have aged out — graduate them to their type folder
    recent_dir = DOWNLOADS / RECENT_FOLDER
    if recent_dir.is_dir():
        for entry in recent_dir.iterdir():
            if entry.is_file() and not is_recent(entry):
                dest_folder = DOWNLOADS / categorize(entry)
                plan.append((entry, dest_folder / entry.name))

    # Interactive only: re-scan existing subfolders so mis-categorized files
    # get corrected when new categories are added.
    if rescan_subfolders:
        for subfolder in DOWNLOADS.iterdir():
            if not subfolder.is_dir() or subfolder.name in SKIP_RESCAN:
                continue
            for entry in subfolder.iterdir():
                if entry.is_file():
                    dest_folder = DOWNLOADS / categorize(entry)
                    if entry.parent != dest_folder:
                        plan.append((entry, dest_folder / entry.name))

    return sorted(plan, key=lambda t: (t[1].parent.name, t[0].name))


def preview(plan: list[tuple[Path, Path]]) -> None:
    current_folder = None
    for src, dest in plan:
        folder = dest.parent.name
        if folder != current_folder:
            graduating = src.parent.name == RECENT_FOLDER
            label = f"{folder}  ← graduating from Recent" if graduating else folder
            print(f"\n  [{label}]")
            current_folder = folder
        print(f"    {src.name}")
    print()


def resolve_dest(dest: Path) -> Path:
    """Append a counter to dest if it already exists."""
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    counter = 1
    candidate = dest
    while candidate.exists():
        candidate = dest.parent / f"{stem} ({counter}){suffix}"
        counter += 1
    return candidate


def execute(plan: list[tuple[Path, Path]]) -> None:
    moved = 0
    for src, dest in plan:
        dest.parent.mkdir(exist_ok=True)
        shutil.move(str(src), str(resolve_dest(dest)))
        moved += 1
    print(f"Done. Moved {moved} file(s).")


def main() -> None:
    parser = argparse.ArgumentParser(description="Organize the Downloads folder by file type.")
    parser.add_argument(
        "--silent",
        action="store_true",
        help="Skip preview and confirmation — organize immediately.",
    )
    args = parser.parse_args()

    if not args.silent:
        print(f"Scanning: {DOWNLOADS}\n")

    plan = build_plan(rescan_subfolders=not args.silent)

    if not plan:
        if not args.silent:
            print("Nothing to organize — Downloads folder is already tidy.")
        return

    if args.silent:
        execute(plan)
    else:
        print(f"Found {len(plan)} file(s) to move:\n")
        preview(plan)
        answer = input("Proceed? [y/N] ").strip().lower()
        if answer == "y":
            execute(plan)
        else:
            print("Aborted — no files were moved.")


if __name__ == "__main__":
    main()
