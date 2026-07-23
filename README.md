# 🖼️ Wallpaper Deduplicator

A fast and safe Python tool to detect visually similar wallpapers, keep the highest-quality version, and move duplicates to a separate folder instead of deleting them.

## Features

- 🔍 Recursively scans wallpaper directories
- 🧠 Detects visually similar images using perceptual hashing (pHash)
- 📂 Supports:
  - JPG / JPEG
  - PNG
  - WEBP
  - GIF
  - HEIC
- ⭐ Automatically selects the best image based on:
  - Resolution
  - File size
  - Lossless format preference
- 👀 Preview duplicate groups before moving
- 📝 Generates a detailed duplicate report
- 📦 Moves duplicates safely to a `duplicates/` folder
- ♻️ Restore (Undo) moved duplicates
- ⚡ Uses caching for much faster future scans

---

## Project Structure

```
wall_dedupe/
├── dedupe.py
├── modules/
│   ├── analyzer.py
│   ├── cache.py
│   ├── config.py
│   ├── grouping.py
│   ├── hasher.py
│   ├── models.py
│   ├── mover.py
│   ├── preview.py
│   ├── report.py
│   ├── restore.py
│   ├── scanner.py
│   └── utils.py
```

---

## Installation

Clone the repository:

```bash
git clone https://github.com/<your-username>/wallpaper-deduplicator.git
cd wallpaper-deduplicator
```

Install dependencies:

```bash
pip install pillow imagehash pillow-heif
```

---

## Usage

Run duplicate detection:

```bash
python dedupe.py
```

Restore moved duplicates:

```bash
python dedupe.py --undo
```

---

## Configuration

Most behavior can be customized by editing:

```text
modules/config.py
```

### Common Settings

| Setting                      | Description                                                                                     |
| ---------------------------- | ----------------------------------------------------------------------------------------------- |
| `WALLPAPER_DIR`              | Directory to scan for wallpapers.                                                               |
| `SUPPORTED_EXTENSIONS`       | File types to include during scanning.                                                          |
| `HASH_SIZE`                  | Perceptual hash size. Higher values increase accuracy but are slower.                           |
| `HAMMING_DISTANCE_THRESHOLD` | Maximum pHash distance for considering two images as duplicates. Lower values are stricter.     |
| `PREVIEW_FIRST_N`            | Number of duplicate groups to preview. Set to `None` to preview all or `0` to disable previews. |
| `WAIT_AFTER_PREVIEW`         | Pause after each preview until Enter is pressed.                                                |
| `CACHE_FILE`                 | Path to the hash cache file.                                                                    |
| `REPORT_FILE`                | Path to the generated duplicate report.                                                         |
| `DUPLICATES_DIR`             | Directory where duplicate images are moved.                                                     |
| `LOG_FILE`                   | Log file used for restoring moved duplicates.                                                   |

### Example

```python
WALLPAPER_DIR = Path.home() / "Pictures" / "Wallpapers"

HASH_SIZE = 16

HAMMING_DISTANCE_THRESHOLD = 8

PREVIEW_FIRST_N = 20

WAIT_AFTER_PREVIEW = True
```

> **Tip:** Increase `HASH_SIZE` for more accurate matching or decrease `HAMMING_DISTANCE_THRESHOLD` if the tool groups images too aggressively.

## How It Works

1. Scan all supported images.
2. Compute perceptual hashes (pHash).
3. Group visually similar images.
4. Choose the highest-quality image to keep.
5. Preview duplicate groups (optional).
6. Generate a duplicate report.
7. Move duplicate images to `duplicates/`.
8. Restore them anytime using `--undo`.

---

## Quality Ranking

Images are ranked using:

1. Higher resolution
2. Higher megapixels
3. Lossless formats preferred
4. Larger file size

The highest-ranked image is kept.

---

## Output

### Report

```
duplicates.txt
```

Contains every duplicate group, the kept image, moved images, and reasons for the selection.

### Log

```
duplicates.log
```

Stores original and moved paths, enabling restoration.

### Duplicates Folder

```
duplicates/
```

Moved duplicate images are stored here while preserving their directory structure.

---

## Supported Formats

- JPG
- JPEG
- PNG
- WEBP
- GIF
- HEIC

---

## Safety

This tool **never permanently deletes images**.

Duplicates are moved to a separate folder and can be restored at any time.

---

## Future Ideas

- BK-Tree search for faster matching
- Parallel hashing
- Interactive terminal UI
- JSON export
- GUI version
