"""
Global configuration for Wallpaper Deduplicator.
"""

from pathlib import Path

# --------------------------------------------------
# Directories
# --------------------------------------------------

SCRIPT_DIR = Path(__file__).resolve().parent.parent

# walls/
WALLPAPER_DIR = SCRIPT_DIR.parent

# walls/duplicates/
DUPLICATE_DIR = WALLPAPER_DIR / "duplicates"

# Ignore while scanning
IGNORE_DIRS = {
    "wall_dedupe",
    "duplicates",
}

# --------------------------------------------------
# Files
# --------------------------------------------------

CACHE_FILE = SCRIPT_DIR / "hash_cache.json"

REPORT_FILE = SCRIPT_DIR / "duplicates.txt"

LOG_FILE = SCRIPT_DIR / "duplicates.log"

# --------------------------------------------------
# Image extensions
# --------------------------------------------------

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".gif",
    ".tif",
    ".tiff",
    ".heic",
}

# --------------------------------------------------
# Perceptual hashing
# --------------------------------------------------

HASH_SIZE = 16

# Maximum Hamming distance
SIMILARITY_THRESHOLD = 4

# --------------------------------------------------
# Preview
# --------------------------------------------------

ENABLE_PREVIEW = True

IMV_COMMAND = "imv"

# Number of duplicate groups to preview
#
# 0    -> preview none
# None -> preview all
# N    -> preview first N groups
#
PREVIEW_FIRST_N = 20

# Pause after each preview and wait for Enter.
WAIT_AFTER_PREVIEW = True

# --------------------------------------------------
# Dry run
# --------------------------------------------------

DRY_RUN = False
