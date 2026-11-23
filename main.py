"""world-news-20261123: copy the generated front-page image to the output dir.

Deterministic, standard library only, no network. The image itself was
generated on Kaggle's free GPU (SDXL) and composited into a newspaper front
page; this program simply delivers the finished file byte for byte.
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")

# Accept a whole PNG or JPEG image, told apart by its first bytes.
MAGIC = (b"\x89PNG", b"\xff\xd8\xff")


def _check_image(path: str) -> int:
    """Return the file size, raising if it is not a whole PNG/JPEG image."""
    with open(path, "rb") as fh:
        head = fh.read(8)
    if not any(head.startswith(m) for m in MAGIC):
        raise ValueError(f"{path}: not a PNG or JPEG image")
    size = os.path.getsize(path)
    if size == 0 or size > 1048576:
        raise ValueError(f"{path}: unexpected size {size} bytes")
    return size


def main() -> int:
    size = _check_image(SRC)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(SRC, dst)
    if _check_image(dst) != size:
        raise ValueError("copied file differs from source")
    digest = hashlib.sha256(open(dst, "rb").read()).hexdigest()
    print(f"wrote {dst} ({size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
