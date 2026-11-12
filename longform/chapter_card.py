"""Render a 1920x1080 card PNG for the long-form film.

Usage: chapter_card.py OUT.png KIND [LINE1] [LINE2] [LINE3]
KIND: intro | chapter | end
"""
import math
import sys

import cairo

W, H = 1920, 1080
GOLD = (1.0, 0.79, 0.24)
WHITE = (1, 1, 1)
INK = (0.08, 0.07, 0.12)


def text(c, s, x, y, size, color, olw=14):
    c.select_font_face("Sans", cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    c.set_font_size(size)
    ext = c.text_extents(s)
    px, py = x - ext.width / 2 - ext.x_bearing, y + ext.height / 2
    c.move_to(px, py)
    c.text_path(s)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.set_source_rgb(*INK)
    c.set_line_width(olw)
    c.stroke_preserve()
    c.set_source_rgb(*color)
    c.fill()


def background(c):
    g = cairo.RadialGradient(W / 2, H / 2, 40, W / 2, H / 2, 1250)
    g.add_color_stop_rgb(0, 0.34, 0.58, 0.82)
    g.add_color_stop_rgb(0.45, 0.17, 0.34, 0.58)
    g.add_color_stop_rgb(1, 0.06, 0.09, 0.2)
    c.rectangle(0, 0, W, H)
    c.set_source(g)
    c.fill()
    # frosty corner flakes
    for i in range(22):
        x = (i * 211) % W
        y = (i * 137) % H
        r = 4 + (i % 4) * 3
        c.arc(x, y, r, 0, 2 * math.pi)
        c.set_source_rgba(1, 1, 1, 0.14 + 0.03 * (i % 3))
        c.fill()


def crown(c, x, y, s):
    c.save()
    c.translate(x, y)
    c.scale(s, s)
    c.move_to(-60, 40)
    c.line_to(-70, -30)
    c.line_to(-30, 0)
    c.line_to(0, -45)
    c.line_to(30, 0)
    c.line_to(70, -30)
    c.line_to(60, 40)
    c.close_path()
    c.set_source_rgb(*GOLD)
    c.fill_preserve()
    c.set_source_rgb(*INK)
    c.set_line_width(8)
    c.stroke()
    for gx, col in [(-30, (0.9, 0.2, 0.3)), (0, (0.2, 0.7, 0.9)), (30, (0.3, 0.8, 0.4))]:
        c.arc(gx, 18, 9, 0, 2 * math.pi)
        c.set_source_rgb(*col)
        c.fill()
    c.restore()


def main():
    out, kind = sys.argv[1], sys.argv[2]
    lines = sys.argv[3:]
    surf = cairo.ImageSurface(cairo.FORMAT_RGB24, W, H)
    c = cairo.Context(surf)
    background(c)
    if kind == "intro":
        crown(c, W / 2, 130, 2.6)
        text(c, "FRIDGE", W / 2, 360, 230, WHITE)
        text(c, "KINGDOM", W / 2, 580, 230, GOLD)
        if lines:
            text(c, lines[0], W / 2, 800, 84, WHITE, olw=12)
        if len(lines) > 1:
            text(c, lines[1], W / 2, 910, 56, (0.78, 0.9, 1.0), olw=10)
    elif kind == "chapter":
        text(c, lines[0], W / 2, 420, 90, (0.78, 0.9, 1.0), olw=12)
        text(c, lines[1], W / 2, 580, 170 if len(lines[1]) < 22 else 140, GOLD)
    elif kind == "end":
        text(c, "TO BE CONTINUED...", W / 2, 400, 170, GOLD)
        for i, ln in enumerate(lines):
            text(c, ln, W / 2, 660 + i * 110, 72, WHITE, olw=12)
    surf.write_to_png(out)


if __name__ == "__main__":
    main()
