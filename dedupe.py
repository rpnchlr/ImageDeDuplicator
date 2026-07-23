"""
Wallpaper Deduplicator

Main entry point.
"""

from __future__ import annotations

import sys

from modules.scanner import scan_images
from modules.cache import load_cache, save_cache
from modules.hasher import hash_images
from modules.grouping import group_duplicates
from modules.analyzer import analyze_groups
from modules.preview import preview_group
from modules.report import write_report
from modules.mover import move_duplicates
from modules.restore import restore_duplicates

from modules.config import (
    WALLPAPER_DIR,
    CACHE_FILE,
    REPORT_FILE,
    PREVIEW_FIRST_N,
    WAIT_AFTER_PREVIEW,
)


def should_preview(index: int) -> bool:
    if PREVIEW_FIRST_N is None:
        return True

    if PREVIEW_FIRST_N <= 0:
        return False

    return index <= PREVIEW_FIRST_N


def print_image(title, image):
    print(title)
    print("-" * len(title))

    print(f"Name       : {image.path.name}")
    print(f"Resolution : {image.width} × {image.height}")
    print(f"Megapixels : {image.megapixels:.2f} MP")
    print(f"Extension  : {image.extension}")
    print(f"Filesize   : {image.filesize:,} bytes")
    print(f"Lossless   : {image.lossless}")

    print()


def human_size(size: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]

    value = float(size)

    for unit in units:

        if value < 1024:
            return f"{value:.2f} {unit}"

        value /= 1024

    return f"{value:.2f} PB"


def undo():
    print("=" * 60)
    print("Restore Duplicates")
    print("=" * 60)
    print()

    restored_files, restored_bytes = restore_duplicates()

    print()
    print("=" * 60)
    print("Restore Finished")
    print("=" * 60)
    print(f"Restored Files : {restored_files}")
    print(f"Restored Size  : {human_size(restored_bytes)}")
    print("=" * 60)


def main():

    # -----------------------------------------
    # Undo Mode
    # -----------------------------------------

    if "--undo" in sys.argv:
        undo()
        return

    print("=" * 60)
    print("Wallpaper Deduplicator")
    print("=" * 60)
    print()

    image_paths = scan_images(WALLPAPER_DIR)

    if not image_paths:
        print("No supported images found.")
        return

    print(f"Found {len(image_paths)} images.\n")

    cache = load_cache(CACHE_FILE)

    images = hash_images(
        image_paths,
        cache,
    )

    save_cache(
        CACHE_FILE,
        cache,
    )

    print(f"\nHashed {len(images)} images.\n")

    print("Searching for duplicate groups...\n")

    groups = group_duplicates(images)

    print(f"Found {len(groups)} duplicate groups.\n")

    if not groups:
        print("No duplicates found.")
        return

    analysis = analyze_groups(
        groups,
        images,
    )

    write_report(
        analysis,
        REPORT_FILE,
    )

    print(f"Report written to:\n{REPORT_FILE}\n")

    files_to_move = sum(
        len(group.move)
        for group in analysis
    )

    bytes_to_move = sum(
        image.filesize
        for group in analysis
        for image in group.move
    )

    print("=" * 60)
    print("SUMMARY")
    print("=" * 60)
    print(f"Duplicate Groups : {len(analysis)}")
    print(f"Files To Move    : {files_to_move}")
    print(f"Space Recovered  : {human_size(bytes_to_move)}")
    print()

    for index, group in enumerate(analysis, start=1):

        keep = group.keep
        move = group.move

        print("=" * 70)
        print(f"GROUP {index}")
        print("=" * 70)
        print()

        print_image("KEEP", keep)

        print("MOVE")
        print("----")

        if not move:
            print("Nothing\n")

        for image in move:
            print(
                f"{image.path.name}"
                f" ({image.width}×{image.height})"
                f" [{image.extension}]"
            )

        print()

        if should_preview(index):

            preview_group(
                [
                    keep.path,
                    *[img.path for img in move],
                ]
            )

            if WAIT_AFTER_PREVIEW:
                input("Press Enter to continue...")

    print()
    print("=" * 60)

    answer = input(
        "Move duplicate files to 'duplicates/'? [y/N]: "
    ).strip().lower()

    if answer != "y":
        print("\nCancelled.")
        return

    print("\nMoving files...\n")

    moved_files, moved_bytes = move_duplicates(
        analysis,
    )

    print()
    print("=" * 60)
    print("Finished")
    print("=" * 60)
    print(f"Moved Files : {moved_files}")
    print(f"Recovered   : {human_size(moved_bytes)}")
    print("Log written : duplicates.log")
    print("=" * 60)


if __name__ == "__main__":
    main()
