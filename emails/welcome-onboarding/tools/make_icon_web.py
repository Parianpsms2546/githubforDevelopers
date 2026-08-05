#!/usr/bin/env python3
"""Render images/icon-web.png — the globe icon for the "Website" button.

The Apple and Android icons beside it in the same button row are 72x72 RGBA
PNGs inked in #383842, and both are solid glyphs, so this one is solid too: a
filled disc with the equator, two latitudes and one meridian knocked back out
of it. An outline globe was tried first and read noticeably lighter than its
neighbours — it carried 1899 units of ink against Android's 2156, where this
one carries 2187.

Supersampled 4x for anti-aliasing. Pure stdlib — no imaging library is
available in the build environment.
"""

import struct
import zlib
from math import hypot

SIZE = 72          # canvas, matches icon-apple.png / icon-android.png
INK = (56, 56, 66)  # #383842, sampled from the sibling icons
SS = 4             # supersampling factor per axis

C = SIZE / 2.0     # centre
R = 32.0           # disc radius, leaves 4px of padding on each side
CUT = 3.4          # width of the knocked-out grid lines (~0.85px at 18px)
LAT = 15.0         # latitude lines at y = C +/- LAT
MERIDIAN_A = 13.5  # semi-minor axis of the meridian ellipse

# No straight vertical centre line: the meridian ellipse already reads as one,
# and adding it made the glyph noisy at the 18px it is displayed at.


def covered(x, y):
    """True when (x, y) is inked — inside the disc and off every grid line."""
    dx, dy = x - C, y - C

    if hypot(dx, dy) > R:
        return False

    # Equator + two latitude lines
    for off in (0.0, LAT, -LAT):
        if abs(dy - off) <= CUT / 2:
            return False

    # Meridian: ellipse (dx/a)^2 + (dy/R)^2 = 1, distance approximated by
    # the implicit value over the gradient magnitude.
    f = (dx / MERIDIAN_A) ** 2 + (dy / R) ** 2 - 1.0
    gx = 2 * dx / (MERIDIAN_A ** 2)
    gy = 2 * dy / (R ** 2)
    g = hypot(gx, gy)
    if g > 1e-9 and abs(f) / g <= CUT / 2:
        return False

    return True


def render():
    rows = []
    step = 1.0 / SS
    offs = [(i + 0.5) * step for i in range(SS)]
    for py in range(SIZE):
        row = bytearray()
        for px in range(SIZE):
            hits = 0
            for oy in offs:
                for ox in offs:
                    if covered(px + ox, py + oy):
                        hits += 1
            a = round(255 * hits / (SS * SS))
            row += bytes((INK[0], INK[1], INK[2], a))
        rows.append(bytes(row))
    return rows


def write_png(path, rows):
    raw = b''.join(b'\x00' + r for r in rows)

    def chunk(typ, data):
        body = typ + data
        return struct.pack('>I', len(data)) + body + struct.pack('>I', zlib.crc32(body) & 0xFFFFFFFF)

    ihdr = struct.pack('>IIBBBBB', SIZE, SIZE, 8, 6, 0, 0, 0)
    png = (b'\x89PNG\r\n\x1a\n'
           + chunk(b'IHDR', ihdr)
           + chunk(b'IDAT', zlib.compress(raw, 9))
           + chunk(b'IEND', b''))
    with open(path, 'wb') as fh:
        fh.write(png)


if __name__ == '__main__':
    import os
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                       '..', 'images', 'icon-web.png')
    write_png(os.path.normpath(out), render())
    print('wrote', os.path.normpath(out))
