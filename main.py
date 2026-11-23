#!/usr/bin/env python3
"""Validate entry.png and deliver it to the output directory.

The repository holds a single 1024x1024 newspaper front page,
entry.png, next to this file. This program makes sure the file is a
complete PNG that fits the competition limits, then copies it
byte-for-byte into $MAKEFUN_OUTPUT_DIR (falling back to /output),
and re-checks the copy against the original.

Only the Python standard library is used. There is no network
access and no randomness, so repeated runs produce identical bytes.
"""

import hashlib
import os
import shutil
import struct
import sys
import zlib

SIZE_LIMIT = 1048576
SIDE_LIMIT = 1024
MAGIC = b"\x89PNG\r\n\x1a\n"


def abort(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def inspect_png(blob, label):
    """Verify magic, IHDR and IEND; return (width, height)."""
    if len(blob) < 8 or blob[:8] != MAGIC:
        abort(label + " is not a PNG file (bad magic bytes)")
    if len(blob) < 33:
        abort(label + " is too short for a PNG header")
    if struct.unpack(">I", blob[8:12])[0] != 13:
        abort(label + " has an IHDR chunk of unexpected length")
    if blob[12:16] != b"IHDR":
        abort(label + " has no IHDR chunk in the expected position")
    wanted = zlib.crc32(b"IHDR" + blob[16:29]) & 0xFFFFFFFF
    if struct.unpack(">I", blob[29:33])[0] != wanted:
        abort(label + " has an IHDR chunk with a bad CRC32")
    width, height = struct.unpack(">II", blob[16:24])
    depth = blob[24]
    if depth not in (1, 2, 4, 8, 16):
        abort("%s has an invalid bit depth %d" % (label, depth))
    if blob[25] not in (0, 2, 3, 4, 6):
        abort("%s has an invalid colour type %d" % (label, blob[25]))
    if width == 0 or height == 0:
        abort(label + " has a zero dimension")
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        abort("%s is %dx%d, over the %dx%d limit"
              % (label, width, height, SIDE_LIMIT, SIDE_LIMIT))
    if len(blob) < 12 or blob[-12:-8] != b"\x00\x00\x00\x00" \
            or blob[-8:-4] != b"IEND":
        abort(label + " has no well-formed IEND chunk at the end")
    iend_crc = zlib.crc32(b"IEND") & 0xFFFFFFFF
    if struct.unpack(">I", blob[-4:])[0] != iend_crc:
        abort(label + " has an IEND chunk with a bad CRC32")
    return width, height


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(base, "entry.png")
    try:
        with open(source, "rb") as handle:
            blob = handle.read()
    except OSError as exc:
        abort("cannot read " + source + ": " + str(exc))
    if len(blob) > SIZE_LIMIT:
        abort("%s is %d bytes, over the %d byte limit"
              % (source, len(blob), SIZE_LIMIT))
    width, height = inspect_png(blob, source)
    digest = hashlib.sha256(blob).hexdigest()

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    try:
        shutil.copyfile(source, target)
    except OSError as exc:
        abort("cannot write " + target + ": " + str(exc))
    try:
        with open(target, "rb") as handle:
            copy = handle.read()
    except OSError as exc:
        abort("cannot re-read " + target + ": " + str(exc))
    if hashlib.sha256(copy).hexdigest() != digest:
        abort(target + " sha256 differs from " + source)
    if len(copy) != len(blob):
        abort(target + " size differs from " + source)
    if inspect_png(copy, target) != (width, height):
        abort(target + " dimensions differ from " + source)

    print("source: " + source)
    print("dimensions: %dx%d" % (width, height))
    print("size: %d bytes" % len(blob))
    print("sha256: " + digest)
    print("destination: " + target)


if __name__ == "__main__":
    main()
