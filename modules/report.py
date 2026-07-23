"""
Creates a human-readable duplicate report.
"""

from __future__ import annotations

from pathlib import Path

from modules.models import DuplicateGroup


def write_report(
    groups: list[DuplicateGroup],
    output: Path,
):

    with output.open(
        "w",
        encoding="utf-8",
    ) as f:

        f.write("=" * 70 + "\n")
        f.write("Wallpaper Deduplication Report\n")
        f.write("=" * 70 + "\n\n")

        total_move = 0

        for index, group in enumerate(groups, start=1):

            total_move += len(group.move)

            f.write("=" * 70 + "\n")
            f.write(f"GROUP {index}\n")
            f.write("=" * 70 + "\n\n")

            keep = group.keep

            f.write("KEEP\n")
            f.write("----\n")

            f.write(f"Name       : {keep.path.name}\n")
            f.write(
                f"Resolution : {keep.width} × {keep.height}\n"
            )
            f.write(
                f"Megapixels : {keep.megapixels:.2f} MP\n"
            )
            f.write(
                f"Extension  : {keep.extension}\n"
            )
            f.write(
                f"Filesize   : {keep.filesize:,} bytes\n"
            )
            f.write(
                f"Lossless   : {keep.lossless}\n\n"
            )

            f.write("MOVE\n")
            f.write("----\n")

            for img in group.move:

                f.write(
                    f"{img.path.name}"
                    f" ({img.width}x{img.height}) "
                    f"[{img.extension}] "
                    f"{img.filesize:,} bytes\n"
                )

            f.write("\nReasons\n")
            f.write("-------\n")

            for reason in group.reasons:
                f.write(f"• {reason}\n")

            f.write("\n")

        f.write("=" * 70 + "\n")
        f.write(f"Duplicate Groups : {len(groups)}\n")
        f.write(f"Files To Move    : {total_move}\n")
        f.write("=" * 70 + "\n")
