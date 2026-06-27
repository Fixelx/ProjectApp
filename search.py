#!/usr/bin/env python3

from pathlib import Path

ROOT = Path("/opt/projects")
SEARCH = "<a"

EXCLUDE_DIRS = {
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
    "media",
    "staticfiles",
    'base.html',
    'search.py'
}

for path in ROOT.rglob("*"):

    if not path.is_file():
        continue

    if any(part in EXCLUDE_DIRS for part in path.parts):
        continue

    try:
        with path.open("r", encoding="utf-8") as f:

            for number, line in enumerate(f, start=1):

                if SEARCH in line:
                    print(
                        f"{path}:{number}: {line.rstrip()}"
                    )

    except (UnicodeDecodeError, PermissionError):
        pass