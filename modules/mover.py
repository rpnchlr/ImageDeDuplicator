"""
Moves duplicate images into the duplicates directory.

This module never decides WHAT to move.
It only executes the plan produced by analyzer.py.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from modules.config import (
    DUPLICATE_DIR,
    LOG_FILE,
    WALLPAPER_DIR,
)
from modules.models import DuplicateGroup


def _unique_destination(path: Path) -> Path:
    """
    Prevent overwriting existing files.

    image.png
    image (1).png
    image (2).png
    """

    if not path.exists():
        return path

    stem = path.stem
    suffix = path.suffix

    counter = 1

    while True:

        candidate = path.with_name(
            f"{stem} ({counter}){suffix}"
        )

        if not candidate.exists():
            return candidate

        counter += 1


def move_duplicates(
    groups: list[DuplicateGroup],
) -> tuple[int, int]:
    """
    Move duplicate files.

    Returns
    -------
    (moved_files, moved_bytes)
    """

    DUPLICATE_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    moved_files = 0
    moved_bytes = 0

    with LOG_FILE.open(
        "w",
        encoding="utf-8",
    ) as log:

        for group in groups:

            for image in group.move:

                try:

                    relative = image.path.relative_to(
                        WALLPAPER_DIR
                    )

                except ValueError:

                    relative = Path(image.path.name)

                destination = DUPLICATE_DIR / relative

                destination.parent.mkdir(
                    parents=True,
                    exist_ok=True,
                )

                destination = _unique_destination(
                    destination
                )

                shutil.move(
                    str(image.path),
                    str(destination),
                )

                moved_files += 1
                moved_bytes += image.filesize

                log.write(
                    f"{image.path}|{destination}\n"
                )

    return (
        moved_files,
        moved_bytes,
    )
