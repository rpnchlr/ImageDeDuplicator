"""
Finds every supported image inside the wallpaper folder.
"""

from pathlib import Path

from rich.console import Console

from modules.config import (
    IGNORE_DIRS,
    SUPPORTED_EXTENSIONS,
)

console = Console()


def scan_images(root: Path) -> list[Path]:
    """
    Recursively scans the wallpaper directory.

    Returns
    -------
    list[Path]
    """

    images = []

    for path in root.rglob("*"):

        if not path.is_file():
            continue

        # Ignore directories
        if any(
            part in IGNORE_DIRS
            for part in path.parts
        ):
            continue

        if path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        images.append(path)

    images.sort()

    console.print(
        f"[green]Found {len(images)} images[/green]"
    )

    return images
