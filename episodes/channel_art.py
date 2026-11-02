"""Channel art: profile picture (800x800) and YouTube banner (2560x1440, logo inside the 1546x423 safe area)."""
import os
import math, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cairo
from ep1 import dill, crumb, duck, crown, text, ellipse, rrect, hexc, GOLD, INK


def glow_bg(c, w, h, cx, cy):
    g = cairo.RadialGradient(cx, cy, 30, cx, cy, max(w, h) * 0.75)
    g.add_color_stop_rgb(0, *hexc("#E7F5FF")); g.add_color_stop_rgb(0.3, *hexc("#74C0FC"))
    g.add_color_stop_rgb(0.75, *hexc("#3D5285")); g.add_color_stop_rgb(1, *hexc("#1C2541"))
    c.rectangle(0, 0, w, h); c.set_source(g); c.fill()
    c.save(); c.translate(cx, cy)
    for i in range(18):
        a = i * 2 * math.pi / 18
        c.move_to(0, 0); c.arc(0, 0, max(w, h) * 1.2, a, a + math.pi / 18); c.close_path()
        c.set_source_rgba(1, 1, 1, 0.07); c.fill()
    c.restore()


def profile(path):
    S = 800
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, S, S); c = cairo.Context(surf)
    glow_bg(c, S, S, S / 2, S * 0.42)
    # Dill, big and centered, framed for a circle crop
    c.save(); c.translate(S / 2 - 10, S * 0.98); c.scale(2.15, 2.15)
    dill(c, 0, 0, "proud", look=(0.2, 0), arm="up", crown_on=True)
    c.restore()
    surf.write_to_png(path)


def banner(path):
    W, H = 2560, 1440
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H); c = cairo.Context(surf)
    glow_bg(c, W, H, W / 2, H / 2)
    # shelves across the full width (decorative, outside safe area is fine)
    for sy in (H / 2 + 205,):
        c.rectangle(0, sy, W, 30); c.set_source_rgba(0.8, 0.92, 1, 0.8); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    # title inside the safe area (1546x423 centered)
    crown(c, W / 2 + 260, H / 2 - 92, 1.1, 0.25)
    text(c, "FRIDGE KINGDOM", W / 2, H / 2 + 35, 132, GOLD, olw=20)
    text(c, "New episode every day", W / 2, H / 2 + 118, 50, (1, 1, 1), olw=9)
    # characters standing on the shelf, flanking the title
    sy = H / 2 + 205
    c.save(); c.translate(W / 2 - 680, sy); c.scale(0.74, 0.74); dill(c, 0, 0, "proud", look=(0.6, 0), arm="up"); c.restore()
    c.save(); c.translate(W / 2 + 690, sy); c.scale(0.74, 0.74); crumb(c, 0, 0, "worried", look=(-1, 0)); c.restore()
    # the Duck, off to the side, watching (visible on TV/desktop widths)
    c.save(); c.translate(W / 2 + 1000, sy); c.scale(0.8, 0.8); duck(c, 0, 0, turn=1.0); c.restore()
    surf.write_to_png(path)


if __name__ == "__main__":
    profile(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art", "fridge_kingdom_profile.png"))
    banner(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art", "fridge_kingdom_banner.png"))
