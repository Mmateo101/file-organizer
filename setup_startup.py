"""
setup_startup.py — Run this once to register organizer.py in Windows Task Scheduler.

It creates a task called "FileOrganizerStartup" that runs organizer.py --silent
every time the current user logs in.

Usage:
    python setup_startup.py            # register the task
    python setup_startup.py --remove   # remove the task
"""

import argparse
import subprocess
import sys
from pathlib import Path

TASK_NAME = "FileOrganizerStartup"
ORGANIZER = Path(__file__).parent / "organizer.py"


def python_exe() -> str:
    return sys.executable


def register() -> None:
    python = python_exe()
    script = str(ORGANIZER.resolve())

    # Build the schtasks command:
    #   /SC ONLOGON   — trigger: at user logon
    #   /RL HIGHEST   — run with highest available privileges (avoids UAC prompt)
    #   /F            — force-overwrite if task already exists
    cmd = [
        "schtasks", "/Create",
        "/TN", TASK_NAME,
        "/TR", f'"{python}" "{script}" --silent',
        "/SC", "ONLOGON",
        "/RL", "HIGHEST",
        "/F",
    ]

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f'Task "{TASK_NAME}" registered successfully.')
        print(f"  Python : {python}")
        print(f"  Script : {script}")
        print(f"  Trigger: at every logon")
        print(f"  Flag   : --silent")
    else:
        print("Failed to register task.")
        print(result.stderr.strip())
        sys.exit(1)


def remove() -> None:
    cmd = ["schtasks", "/Delete", "/TN", TASK_NAME, "/F"]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        print(f'Task "{TASK_NAME}" removed.')
    else:
        print("Failed to remove task (does it exist?).")
        print(result.stderr.strip())
        sys.exit(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Register or remove the startup task for organizer.py.")
    parser.add_argument("--remove", action="store_true", help="Remove the scheduled task instead of creating it.")
    args = parser.parse_args()

    if args.remove:
        remove()
    else:
        register()


if __name__ == "__main__":
    main()
