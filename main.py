#!/usr/bin/env python3
"""Put the day's page where the grader reads it.

The picture beside this file is already composed and committed; this program
hands it over byte for byte. It draws nothing, reads no clock, takes no random
number, and writes exactly one file, so the grader's two runs write identical
output and the gate sees the same bytes twice.

It will not hand over a file it has not checked. The PNG signature, every
chunk's declared length and CRC, a closing IEND, and the competition's size
caps are verified first: a repository broken by a bad merge fails here, in the
log, instead of being graded as a corrupt image.

Python 3 standard library only, as the rules require.
"""

import binascii
import os
import struct
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
PAGE = os.path.join(HERE, "entry.png")

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
JPEG_MAGIC = b"\xff\xd8\xff"
CAP_BYTES = 1024 * 1024      # the gate's file cap
CAP_SIDE = 1024              # the gate's pixel cap
FLOOR_SIDE = 256             # below this the judge cannot read the page


def out_dir():
    """The directory the grader names, or MAKEFUN_OUTPUT_DIR outside it."""
    return os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"


def walk(data):
    """Check the chunk chain and return [(kind, body)], or raise ValueError.

    Every chunk is length-prefixed and CRC'd, so a file can be well formed at
    the start and broken later; this walks the whole chain rather than
    trusting the header. It stops at IEND and treats a missing IEND as
    failure, because a truncated PNG still opens in many viewers, which is
    exactly why it must never be shipped silently.
    """
    if data.startswith(JPEG_MAGIC):
        raise ValueError("the file is a JPEG; this entry ships a PNG")
    if not data.startswith(PNG_MAGIC):
        raise ValueError("no PNG signature: %r" % data[:8])

    parts = []
    at = len(PNG_MAGIC)
    while at + 8 <= len(data):
        (length,) = struct.unpack(">I", data[at:at + 4])
        kind = data[at + 4:at + 8]
        body = data[at + 8:at + 8 + length]
        if len(body) != length:
            raise ValueError("%r says %d bytes, only %d remain"
                             % (kind, length, len(body)))
        crc_at = at + 8 + length
        if crc_at + 4 > len(data):
            raise ValueError("%r has no CRC" % kind)
        (stored,) = struct.unpack(">I", data[crc_at:crc_at + 4])
        computed = binascii.crc32(kind + body) & 0xFFFFFFFF
        if stored != computed:
            raise ValueError("%r fails its CRC: %08x not %08x"
                             % (kind, stored, computed))
        parts.append((kind, body))
        at = crc_at + 4
        if kind == b"IEND":
            break
    return parts


def measure(data):
    """The page's width and height, once the chain has been validated."""
    parts = walk(data)
    if not parts or parts[0][0] != b"IHDR":
        raise ValueError("the first chunk is not IHDR")
    if parts[-1][0] != b"IEND":
        raise ValueError("no IEND: the image is truncated")
    head = parts[0][1]
    if len(head) < 8:
        raise ValueError("IHDR is %d bytes, too short for a size" % len(head))
    width, height = struct.unpack(">II", head[:8])
    return width, height


def gate(width, height, size):
    """Refuse anything the competition's gate would refuse."""
    if size > CAP_BYTES:
        raise ValueError("%d bytes is over the %d cap" % (size, CAP_BYTES))
    if width > CAP_SIDE or height > CAP_SIDE:
        raise ValueError("%dx%d is over the %d cap"
                         % (width, height, CAP_SIDE))
    if width < FLOOR_SIDE or height < FLOOR_SIDE:
        raise ValueError("%dx%d is under the readable floor of %d"
                         % (width, height, FLOOR_SIDE))
    if width != height:
        raise ValueError("%dx%d is not square; the gate wants a square"
                         % (width, height))


def main():
    with open(PAGE, "rb") as handle:
        data = handle.read()

    width, height = measure(data)
    gate(width, height, len(data))

    target = os.path.join(out_dir(), "entry.png")
    os.makedirs(os.path.dirname(target) or ".", exist_ok=True)
    with open(target, "wb") as handle:
        handle.write(data)

    if os.path.getsize(target) != len(data):
        raise SystemExit("short write: %d of %d bytes"
                         % (os.path.getsize(target), len(data)))

    print("wrote %s: %dx%d, %d bytes" % (target, width, height, len(data)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
