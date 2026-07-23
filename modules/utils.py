"""
Utility functions used across the project.
"""

from pathlib import Path

from PIL import Image

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()
except Exception:
    pass


def get_resolution(path: Path) -> tuple[int, int]:
    """
    Returns image resolution.

    Example
    -------
    (3840, 2160)
    """

    with Image.open(path) as img:
        return img.width, img.height


def megapixels(path: Path) -> float:
    """
    Returns megapixels.
    """

    w, h = get_resolution(path)
    return (w * h) / 1_000_000


def resolution_score(path: Path) -> int:
    """
    Used when deciding which duplicate to keep.
    """

    w, h = get_resolution(path)
    return w * h


def is_lossless(path: Path) -> bool:
    """
    PNG/TIFF are treated as lossless.
    """

    return path.suffix.lower() in {
        ".png",
        ".tif",
        ".tiff",
    }


def human_size(size: int) -> str:
    """
    Convert bytes into readable string.
    """

    units = [
        "B",
        "KB",
        "MB",
        "GB",
    ]

    value = float(size)

    for unit in units:

        if value < 1024:
            return f"{value:.1f} {unit}"

        value /= 1024

    return f"{value:.1f} TB"
