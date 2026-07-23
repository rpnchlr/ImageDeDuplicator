"""
Preview duplicate groups using imv.
"""

from pathlib import Path
import subprocess

from modules.config import (
    ENABLE_PREVIEW,
    IMV_COMMAND,
)


def preview_group(paths: list[Path]):

    if not ENABLE_PREVIEW:
        return

    command = [
        IMV_COMMAND,
        *map(str, paths),
    ]

    subprocess.run(
        command,
        check=False,
    )
