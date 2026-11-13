#!/usr/bin/env python3
"""Generate dark-mode PWA icons as PNGs (stdlib only)."""
from __future__ import annotations

import math
import struct
import zlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def write_png(path: Path, w: int, h: int, rgba: bytearray) -> None:
    raw = bytearray()
    stride = w * 4
    for y in range(h):
        raw.append(0)
        raw.extend(rgba[y * stride : (y + 1) * stride])

    def chunk(tag: bytes, data: bytes) -> bytes:
        crc = zlib.crc32(tag + data) & 0xFFFFFFFF
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", crc)

    ihdr = struct.pack(">IIBBBBB", w, h, 8, 6, 0, 0, 0)
    png = (
        b"\x89PNG\r\n\x1a\n"
        + chunk(b"IHDR", ihdr)
        + chunk(b"IDAT", zlib.compress(bytes(raw), 9))
        + chunk(b"IEND", b"")
    )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(png)


def mix(a, b, t: float):
    t = 0 if t < 0 else 1 if t > 1 else t
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(4))


def setp(img, w, h, x, y, color):
    if 0 <= x < w and 0 <= y < h:
        i = (y * w + x) * 4
        img[i : i + 4] = bytes(color)


def stamp(img, w, h, x, y, color, cover: float):
    if cover <= 0:
        return
    if cover >= 1:
        setp(img, w, h, x, y, color)
        return
    if not (0 <= x < w and 0 <= y < h):
        return
    i = (y * w + x) * 4
    dst = tuple(img[i : i + 4])
    setp(img, w, h, x, y, mix(dst, color, cover))


def fill_rect(img, w, h, x0, y0, x1, y1, color):
    for y in range(max(0, int(y0)), min(h, int(y1) + 1)):
        for x in range(max(0, int(x0)), min(w, int(x1) + 1)):
            setp(img, w, h, x, y, color)


def fill_round_rect(img, w, h, cx, cy, hw, hh, r, color):
    r = min(r, hw, hh)
    for y in range(max(0, int(cy - hh - 1)), min(h, int(cy + hh + 2))):
        for x in range(max(0, int(cx - hw - 1)), min(w, int(cx + hw + 2))):
            dx = abs(x + 0.5 - cx)
            dy = abs(y + 0.5 - cy)
            ox = dx - (hw - r)
            oy = dy - (hh - r)
            if dx <= hw - r and dy <= hh:
                d = -1
            elif dy <= hh - r and dx <= hw:
                d = -1
            else:
                d = math.hypot(max(ox, 0), max(oy, 0)) - r
            cover = 0 if d >= 1 else 1 if d <= 0 else 1 - d
            stamp(img, w, h, x, y, color, cover)


def fill_circle(img, w, h, cx, cy, r, color):
    for y in range(max(0, int(cy - r - 1)), min(h, int(cy + r + 2))):
        for x in range(max(0, int(cx - r - 1)), min(w, int(cx + r + 2))):
            d = math.hypot(x + 0.5 - cx, y + 0.5 - cy) - r
            cover = 0 if d >= 1 else 1 if d <= 0 else 1 - d
            stamp(img, w, h, x, y, color, cover)


def fill_pin(img, w, h, cx, cy, s, color):
    # Teardrop pin: circle + triangle, then inner hole.
    fill_circle(img, w, h, cx, cy - s * 0.18, s * 0.42, color)
    for y in range(int(cy - s * 0.1), int(cy + s * 0.62)):
        t = (y - (cy - s * 0.1)) / (s * 0.72)
        half = (1 - t) * s * 0.38
        for x in range(int(cx - half - 1), int(cx + half + 2)):
            if abs(x + 0.5 - cx) <= half:
                setp(img, w, h, x, y, color)
    fill_circle(img, w, h, cx, cy - s * 0.20, s * 0.16, (16, 20, 28, 255))


def draw_icon(size: int) -> bytearray:
    img = bytearray([12, 16, 22, 255] * (size * size))
    c = size / 2
    fill_round_rect(
        img, size, size, c, c, size * 0.46, size * 0.46, size * 0.22, (22, 28, 38, 255)
    )
    fill_round_rect(
        img, size, size, c, c, size * 0.42, size * 0.42, size * 0.18, (16, 20, 28, 255)
    )
    amber = (255, 176, 32, 255)
    cream = (244, 241, 234, 255)
    fill_pin(img, size, size, c - size * 0.08, c - size * 0.02, size * 0.55, amber)
    # Three log bars (data) on the right.
    bx = c + size * 0.16
    for i, width in enumerate((0.22, 0.16, 0.12)):
        y = c + size * (0.02 + i * 0.12)
        fill_round_rect(
            img, size, size, bx, y, size * width, size * 0.035, size * 0.03, cream
        )
    return img


def main() -> None:
    master = draw_icon(512)
    write_png(ROOT / "icons" / "icon-512.png", 512, 512, master)

    def downscale(src: bytearray, src_s: int, dst_s: int) -> bytearray:
        out = bytearray(dst_s * dst_s * 4)
        factor = src_s / dst_s
        for y in range(dst_s):
            for x in range(dst_s):
                # Box average.
                x0 = int(x * factor)
                y0 = int(y * factor)
                x1 = int((x + 1) * factor)
                y1 = int((y + 1) * factor)
                rs = gs = bs = ac = n = 0
                for yy in range(y0, max(y0 + 1, y1)):
                    for xx in range(x0, max(x0 + 1, x1)):
                        i = (yy * src_s + xx) * 4
                        rs += src[i]
                        gs += src[i + 1]
                        bs += src[i + 2]
                        ac += src[i + 3]
                        n += 1
                j = (y * dst_s + x) * 4
                out[j : j + 4] = bytes((rs // n, gs // n, bs // n, ac // n))
        return out

    write_png(ROOT / "icons" / "icon-192.png", 192, 192, downscale(master, 512, 192))
    write_png(ROOT / "apple-touch-icon.png", 180, 180, downscale(master, 512, 180))
    print("wrote icons")


if __name__ == "__main__":
    main()
