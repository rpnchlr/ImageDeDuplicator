"""
Image hashing.
"""

from pathlib import Path
import os

from PIL import Image
import imagehash
from tqdm import tqdm

try:
    from pillow_heif import register_heif_opener

    register_heif_opener()

except Exception:
    pass

from modules.models import ImageInfo
from modules.config import HASH_SIZE


LOSSLESS = {
    ".png",
    ".tif",
    ".tiff",
}


def hash_images(
    image_paths,
    cache,
):

    images = {}

    for path in tqdm(
        image_paths,
        desc="Hashing",
    ):

        stat = os.stat(path)

        key = str(path)

        mtime = stat.st_mtime

        size = stat.st_size

        # ---------------- Cache ---------------- #

        if key in cache:

            c = cache[key]

            if (
                c["mtime"] == mtime
                and c["size"] == size
            ):

                images[path] = ImageInfo(

                    path=path,

                    phash=imagehash.hex_to_hash(
                        c["phash"]
                    ),

                    width=c["width"],

                    height=c["height"],

                    filesize=c["filesize"],

                    extension=c["extension"],

                    lossless=c["lossless"],

                    megapixels=c["megapixels"],
                )

                continue

        # -------------- Compute --------------- #

        try:

            with Image.open(path) as img:

                phash = imagehash.phash(
                    img,
                    hash_size=HASH_SIZE,
                )

                w, h = img.size

        except Exception:

            continue

        mp = (w * h) / 1_000_000

        ext = path.suffix.lower()

        lossless = ext in LOSSLESS

        info = ImageInfo(

            path=path,

            phash=phash,

            width=w,

            height=h,

            filesize=size,

            extension=ext,

            lossless=lossless,

            megapixels=mp,
        )

        images[path] = info

        cache[key] = {

            "mtime": mtime,

            "size": size,

            "phash": str(phash),

            "width": w,

            "height": h,

            "megapixels": mp,

            "extension": ext,

            "lossless": lossless,

            "filesize": size,
        }

    return images
