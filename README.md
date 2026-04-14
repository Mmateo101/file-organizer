# file-organizer

Automatically sorts your Downloads folder into subfolders by file type.

## Folders

| Folder | Extensions |
|---|---|
| Images/ | `.jpg` `.jpeg` `.png` `.gif` `.webp` |
| Documents/ | `.pdf` |
| Work/ | `.doc` `.docx` `.xls` `.xlsx` `.ppt` `.pptx` |
| Videos/ | `.mp4` `.mov` `.avi` |
| Audio/ | `.mp3` `.wav` |
| Compressed/ | `.zip` `.rar` |
| Code/ | `.py` `.r` `.rmd` `.cpp` `.h` `.m` |
| Other/ | everything else |

## Usage

### Option 1 — Run manually

```
python organizer.py
```

Shows a preview of what will be moved and asks for confirmation before doing anything. Also rescans existing subfolders to fix any mis-categorized files.

### Option 2 — Auto-organize on every startup

Run once to register a Windows startup task:

```
python setup_startup.py
```

This creates a Task Scheduler entry (`FileOrganizerStartup`) that runs `organizer.py --silent` every time you log in — no preview, no prompt, just organizes immediately.

To remove the startup task:

```
python setup_startup.py --remove
```
