"""
Groups visually similar images using perceptual hashes.

Uses Union-Find (Disjoint Set Union) to merge duplicate chains into
single groups.
"""

from __future__ import annotations

from collections import defaultdict
from pathlib import Path

from modules.config import SIMILARITY_THRESHOLD
from modules.models import ImageInfo


class UnionFind:
    def __init__(self):
        self.parent: dict[Path, Path] = {}

    def find(self, x: Path) -> Path:
        if x not in self.parent:
            self.parent[x] = x

        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]

        return x

    def union(self, a: Path, b: Path) -> None:
        pa = self.find(a)
        pb = self.find(b)

        if pa != pb:
            self.parent[pb] = pa


def group_duplicates(
    images: dict[Path, ImageInfo],
) -> list[list[Path]]:
    """
    Group visually similar images.

    Returns:
        [
            [Path(...), Path(...), ...],
            [Path(...), Path(...)]
        ]
    """

    uf = UnionFind()

    paths = list(images.keys())
    total = len(paths)

    for i in range(total):
        img1 = images[paths[i]]

        for j in range(i + 1, total):
            img2 = images[paths[j]]

            distance = img1.phash - img2.phash

            if distance <= SIMILARITY_THRESHOLD:
                print(
                    f"[MATCH] {distance:2d} | "
                    f"{paths[i].name} <--> {paths[j].name}"
                )

                uf.union(paths[i], paths[j])

    groups: dict[Path, list[Path]] = defaultdict(list)

    for path in paths:
        groups[uf.find(path)].append(path)

    return [
        group
        for group in groups.values()
        if len(group) > 1
    ]
