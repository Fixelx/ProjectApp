#!/usr/bin/env python3

import re
from pathlib import Path

ROOT = Path("/opt/projects")

EXCLUDE_DIRS = {
    "venv",
    "__pycache__",
    ".git",
    "node_modules",
    "staticfiles",
    "media",
}

CLASS_RE = re.compile(r'class="([^"]*)"')


for path in ROOT.rglob("*"):

    if not path.is_file():
        continue

    if any(part in EXCLUDE_DIRS for part in path.parts):
        continue

    if path.suffix not in {".html", ".htm"}:
        continue

    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue


    changed = False


    def replace(match):
        classes = match.group(1).split()

        has_btn = "btn" in classes
        has_btn_variant = any(
            c.startswith("btn-")
            for c in classes
        )

        if has_btn_variant and not has_btn:
            classes.insert(0, "btn")
            return f'class="{" ".join(classes)}"'

        return match.group(0)


    new_text = CLASS_RE.sub(replace, text)


    if new_text != text:
        path.write_text(
            new_text,
            encoding="utf-8"
        )

        print(f"✔ geändert: {path}")