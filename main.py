#!/usr/bin/env python3
"""Entry for make.fun bounty news-image-20261123 (Python 3.13, stdlib only).

Copies the shipped entry.png from this repository's root to
$MAKEFUN_OUTPUT_DIR/entry.png (else /output/entry.png). Verifies the image
is a 1024x1024 PNG of at most 1 MiB by reading its IHDR, chmods the copy
0644, and prints nothing on success. No network, no wall clock, no PIL.
"""

import hashlib
import os
import shutil
import struct
import sys

MAX_BYTES = 1048576


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    dst = os.path.join(out_dir, "entry.png")

    try:
        with open(src, "rb") as f:
            head = f.read(33)
    except OSError as exc:
        print("error: cannot read entry.png: %s" % exc, file=sys.stderr)
        return 1
    if len(head) < 33 or head[:8] != b"\x89PNG\r\n\x1a\n":
        print("error: entry.png is not a PNG", file=sys.stderr)
        return 1
    # IHDR chunk: length (4), type "IHDR" (4), width (4 BE), height (4 BE).
    if head[12:16] != b"IHDR":
        print("error: entry.png has no IHDR", file=sys.stderr)
        return 1
    width, height = struct.unpack(">II", head[16:24])
    if width != 1024 or height != 1024:
        print("error: entry.png is %dx%d, want 1024x1024" % (width, height),
              file=sys.stderr)
        return 1
    if os.path.getsize(src) > MAX_BYTES:
        print("error: entry.png exceeds 1 MiB", file=sys.stderr)
        return 1
    with open(src, "rb") as f:
        want = hashlib.sha256(f.read()).hexdigest()

    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    os.chmod(dst, 0o644)
    with open(dst, "rb") as f:
        got = hashlib.sha256(f.read()).hexdigest()
    if got != want:
        print("error: read-back sha256 mismatch", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
