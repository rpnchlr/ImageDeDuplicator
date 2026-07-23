"""
Restore previously moved duplicate images.

Reads duplicates.log and moves every file back to its
original location.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from modules.config import (
    DUPLICATE_DIR,
    LOG_FILE,
)


def _remove_empty_directories(directory: Path) -> None:
    """
    Remove empty directories recursively.

    Example

    duplicates/
        Anime/
            (empty)

    becomes

    duplicates/
    """

    if not directory.exists():
        return

    for child in directory.iterdir():

        if child.is_dir():
            _remove_empty_directories(child)

    try:
        directory.rmdir()
    except OSError:
        pass


def restore_duplicates() -> tuple[int, int]:
    """
    Restore every moved file.

    Returns
    -------
    (restored_files, restored_bytes)
    """

    if not LOG_FILE.exists():
        print("No duplicates.log found.")
        return (0, 0)

    restored_files = 0
    restored_bytes = 0

    with LOG_FILE.open(
        "r",
        encoding="utf-8",
    ) as log:

        for line in log:

            line = line.strip()

            if not line:
                continue

            try:
                original, moved = line.split("|", maxsplit=1)

            except ValueError:
                continue

            original = Path(original)
            moved = Path(moved)

            if not moved.exists():
                continue

            original.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            size = moved.stat().st_size

            shutil.move(
                str(moved),
                str(original),
            )

            restored_files += 1
            restored_bytes += size

    _remove_empty_directories(DUPLICATE_DIR)

    return (
        restored_files,
        restored_bytes,
    )
