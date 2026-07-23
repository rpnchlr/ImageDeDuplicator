"""
Shared dataclasses.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from imagehash import ImageHash


@dataclass(slots=True)
class ImageInfo:
    path: Path

    phash: ImageHash

    width: int
    height: int

    filesize: int

    extension: str

    lossless: bool

    megapixels: float


@dataclass(slots=True)
class DuplicateGroup:
    """
    One duplicate group.

    keep:
        Image that should remain.

    move:
        Images that should be moved.

    reasons:
        Human-readable explanation for why the keep image won.
    """

    keep: ImageInfo

    move: list[ImageInfo]

    reasons: list[str] = field(default_factory=list)
