"""
Chooses the best image inside every duplicate group.
"""

from __future__ import annotations

from modules.models import (
    DuplicateGroup,
    ImageInfo,
)


def image_score(image: ImageInfo):
    """
    Higher tuple = better image.
    """

    return (
        image.width * image.height,
        image.lossless,
        image.filesize,
        -image.path.stat().st_mtime,
    )


def build_reasons(best: ImageInfo) -> list[str]:
    """
    Build a human-readable explanation.
    """

    reasons = []

    reasons.append("Highest Resolution")

    if best.lossless:
        reasons.append("Lossless Format")

    reasons.append("Largest File Size")

    return reasons


def analyze_groups(
    groups,
    images,
) -> list[DuplicateGroup]:

    result: list[DuplicateGroup] = []

    for group in groups:

        infos = [
            images[path]
            for path in group
        ]

        infos.sort(
            key=image_score,
            reverse=True,
        )

        keep = infos[0]

        move = infos[1:]

        result.append(
            DuplicateGroup(
                keep=keep,
                move=move,
                reasons=build_reasons(keep),
            )
        )

    return result
