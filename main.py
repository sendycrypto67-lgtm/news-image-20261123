#!/usr/bin/env python3
"""Validate the bundled entry.png and copy it byte-for-byte to the output dir.

Reads entry.png sitting next to this script, checks that it is a well-formed
PNG within the entry limits, then copies the exact bytes to
$MAKEFUN_OUTPUT_DIR/entry.png. Exits 1 on any validation failure.
Standard library only. No network access.
"""

import os
import struct
import sys
import zlib

MAX_FILE_SIZE = 1048576
MAX_DIMENSION = 1024
PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
OUTPUT_NAME = "entry.png"
SOURCE_NAME = "entry.png"


def fail(message):
    print("error: " + message, file=sys.stderr)
    return 1


def parse_chunks(data):
    """Walk PNG chunks. Return (width, height) from IHDR, or raise ValueError."""
    if len(data) < 8 + 25:
        raise ValueError("file too short to hold a PNG header")
    if data[:8] != PNG_MAGIC:
        raise ValueError("not a PNG file (bad magic bytes)")
    pos = 8
    width = None
    height = None
    saw_iend = False
    first = True
    while pos + 8 <= len(data):
        length = struct.unpack(">I", data[pos:pos + 4])[0]
        chunk_type = data[pos + 4:pos + 8]
        if first and chunk_type != b"IHDR":
            raise ValueError("first chunk is not IHDR")
        first = False
        end = pos + 8 + length + 4
        if end > len(data):
            raise ValueError("truncated chunk: " + chunk_type.decode("ascii", "replace"))
        if chunk_type in (b"IHDR", b"IEND"):
            stored_crc = struct.unpack(">I", data[end - 4:end])[0]
            actual_crc = zlib.crc32(data[pos + 4:end - 4]) & 0xFFFFFFFF
            if stored_crc != actual_crc:
                raise ValueError(
                    "bad CRC in chunk: " + chunk_type.decode("ascii", "replace")
                )
        if chunk_type == b"IHDR":
            if length != 13:
                raise ValueError("IHDR has wrong length")
            width, height = struct.unpack(">II", data[pos + 8:pos + 16])
        if chunk_type == b"IEND":
            if length != 0:
                raise ValueError("IEND has wrong length")
            if end != len(data):
                raise ValueError("trailing bytes after IEND")
            saw_iend = True
            break
        pos = end
    if width is None or height is None:
        raise ValueError("missing IHDR chunk")
    if not saw_iend:
        raise ValueError("missing IEND chunk")
    return width, height


def main(argv):
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if not out_dir:
        return fail("MAKEFUN_OUTPUT_DIR is not set")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(script_dir, SOURCE_NAME)
    if not os.path.isfile(source):
        source = os.path.join(os.getcwd(), SOURCE_NAME)
    if not os.path.isfile(source):
        return fail("entry.png not found next to main.py or in the working directory")

    try:
        with open(source, "rb") as handle:
            data = handle.read()
    except OSError as exc:
        return fail("cannot read entry.png: " + str(exc))

    if len(data) > MAX_FILE_SIZE:
        return fail(
            "entry.png is %d bytes, over the %d byte limit" % (len(data), MAX_FILE_SIZE)
        )

    try:
        width, height = parse_chunks(data)
    except ValueError as exc:
        return fail("invalid PNG: " + str(exc))

    if width <= 0 or height <= 0:
        return fail("invalid PNG dimensions: %dx%d" % (width, height))
    if width > MAX_DIMENSION or height > MAX_DIMENSION:
        return fail(
            "dimensions %dx%d exceed the %d pixel limit" % (width, height, MAX_DIMENSION)
        )

    try:
        os.makedirs(out_dir, exist_ok=True)
        out_path = os.path.join(out_dir, OUTPUT_NAME)
        with open(out_path, "wb") as handle:
            handle.write(data)
    except OSError as exc:
        return fail("cannot write output: " + str(exc))

    print("wrote %s (%dx%d, %d bytes)" % (out_path, width, height, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
