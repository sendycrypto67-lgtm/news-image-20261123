#!/usr/bin/env python3
"""Validate and copy the news-image-20261123 v3 entry.

Finds entry.png next to this script, validates it as a well-formed PNG
(magic bytes, file size, IHDR dimensions and parameters, CRC32 of the
IHDR and IEND chunks, at least one IDAT chunk holding image data, a
bit depth valid for the colour type, a well-formed IEND at end of file
with no trailing bytes), then copies it byte-for-byte to
$MAKEFUN_OUTPUT_DIR/entry.png.

Python 3 standard library only, no network. Deterministic: the output
is a byte-for-byte copy of the input. Every failure exits 1 with a
message on stderr.
"""

import os
import struct
import sys
import zlib

MAX_SIZE = 1048576
MAX_DIM = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def fail(message):
    print("error: " + message, file=sys.stderr)
    sys.exit(1)


def read_chunks(data):
    """Yield (type, payload, crc) for each chunk; validate structure."""
    pos = len(PNG_MAGIC)
    chunks = []
    while pos < len(data):
        if pos + 8 > len(data):
            fail("trailing bytes after IEND")
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        ctype = data[pos + 4:pos + 8]
        end = pos + 8 + length + 4
        if end > len(data):
            fail("truncated chunk: " + ctype.decode("latin-1", "replace"))
        payload = data[pos + 8:pos + 8 + length]
        crc = struct.unpack(">I", data[pos + 8 + length:end])[0]
        chunks.append((ctype, payload, crc))
        pos = end
        if ctype == b"IEND":
            if pos != len(data):
                fail("trailing bytes after IEND")
            break
    return chunks


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    try:
        with open(src, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        fail("cannot read entry.png: " + str(exc))

    if len(data) > MAX_SIZE:
        fail("entry.png is %d bytes, over the 1048576 byte limit"
             % len(data))
    if len(data) < len(PNG_MAGIC) or data[:len(PNG_MAGIC)] != PNG_MAGIC:
        fail("entry.png is not a PNG file")

    chunks = read_chunks(data)
    if not chunks or chunks[0][0] != b"IHDR":
        fail("first chunk is not IHDR")
    if chunks[-1][0] != b"IEND":
        fail("last chunk is not IEND")

    ihdr_type, ihdr, ihdr_crc = chunks[0]
    if len(ihdr) != 13:
        fail("IHDR has wrong length")
    if zlib.crc32(ihdr_type + ihdr) & 0xFFFFFFFF != ihdr_crc:
        fail("IHDR CRC32 mismatch")
    width, height, depth, colour = struct.unpack(">IIBB", ihdr[:10])
    if width > MAX_DIM or height > MAX_DIM:
        fail("dimensions %dx%d exceed the 1024 px limit" % (width, height))
    if width == 0 or height == 0:
        fail("dimensions must be positive")
    if depth not in (1, 2, 4, 8, 16):
        fail("invalid bit depth %d" % depth)
    if colour not in (0, 2, 3, 4, 6):
        fail("invalid colour type %d" % colour)
    valid_depths = {0: (1, 2, 4, 8, 16), 2: (8, 16), 3: (1, 2, 4, 8),
                    4: (8, 16), 6: (8, 16)}
    if depth not in valid_depths[colour]:
        fail("bit depth %d is not valid for colour type %d" % (depth, colour))
    if not any(ctype == b"IDAT" for ctype, _, _ in chunks):
        fail("missing IDAT chunk (no image data)")

    iend_type, iend, iend_crc = chunks[-1]
    if len(iend) != 0:
        fail("IEND chunk must be empty")
    if zlib.crc32(iend_type + iend) & 0xFFFFFFFF != iend_crc:
        fail("IEND CRC32 mismatch")

    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        fail("MAKEFUN_OUTPUT_DIR is not set")
    dest = os.path.join(out_dir, "entry.png")
    try:
        with open(dest, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        fail("cannot write output: " + str(exc))


if __name__ == "__main__":
    main()
