"""
Handles loading and saving the hash cache.
"""

from __future__ import annotations

import json
from pathlib import Path


def load_cache(cache_file: Path) -> dict:
    """
    Load hash cache.

    Returns an empty dict if cache doesn't exist.
    """

    if not cache_file.exists():
        return {}

    try:
        with cache_file.open("r", encoding="utf-8") as f:
            return json.load(f)

    except Exception:
        return {}


def save_cache(cache_file: Path, cache: dict) -> None:
    """
    Save cache to disk.
    """

    with cache_file.open("w", encoding="utf-8") as f:
        json.dump(
            cache,
            f,
            indent=4,
            sort_keys=True,
        )
