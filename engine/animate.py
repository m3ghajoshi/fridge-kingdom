"""Nib & Bun: The Cupcake Caper — 20s wordless cartoon, 1080x1920 @ 30fps, drawn with cairo."""
import math, random, subprocess, sys
import cairo

W, H, FPS, DUR = 1080, 1920, 30, 20.0
FLOOR = 1420
INK = (0.23, 0.16, 0.16)


def hexc(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


def clamp(v, a=0.0, b=1.0):
    return max(a, min(b, v))


def seg(t, a, b):
    return clamp((t - a) / (b - a))


def ease(p):
    return p * p * (3 - 2 * p)


def ease_out(p):
    return 1 - (1 - p) ** 3


def lerp(a, b, p):
    return a + (b - a) * p


def back_out(p):
    c = 1.9
    return 1 + (c + 1) * (p - 1) ** 3 + c * (p - 1) ** 2


# ---------- drawing primitives ----------
def ellipse(c, x, y, rx, ry, fill, lw=6, stroke=True):
    c.save(); c.translate(x, y); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*fill)
    if stroke:
        c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(lw); c.stroke()
    else:
        c.fill()


def rrect(c, x, y, w, h, r):
    c.new_sub_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0)
    c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi)
    c.arc(x + r, y + r, r, math.pi, 3 * math.pi / 2)
    c.close_path()


def star(c, x, y, r, rot, fill=hexc("#FFD43B")):
    if r < 0.5: return
    c.save(); c.translate(x, y); c.rotate(rot)
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        (c.move_to if i == 0 else c.line_to)(rr * math.cos(a), rr * math.sin(a))
    c.close_path(); c.set_source_rgb(*fill); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(4); c.stroke(); c.restore()


def heart(c, x, y, s, alpha):
    s = max(s, 1e-3)
    c.save(); c.translate(x, y); c.scale(max(s, 1e-3), max(s, 1e-3))
    c.move_to(0, 12)
    c.curve_to(-30, -10, -18, -34, 0, -18)
    c.curve_to(18, -34, 30, -10, 0, 12)
    c.close_path(); c.set_source_rgba(*hexc("#FF5C8A"), alpha); c.fill_preserve()
    c.set_source_rgba(*INK, alpha); c.set_line_width(3 / s); c.stroke(); c.restore()


def text(c, s, x, y, size, fill, outline=INK, olw=10, font="Poppins", weight=cairo.FONT_WEIGHT_BOLD):
    c.select_font_face(font, cairo.FONT_SLANT_NORMAL, weight)
    c.set_font_size(size)
    ext = c.text_extents(s)
    c.move_to(x - ext.width / 2 - ext.x_bearing, y)
    c.text_path(s)
    c.set_source_rgb(*outline); c.set_line_width(olw); c.set_line_join(cairo.LINE_JOIN_ROUND)
    c.stroke_preserve(); c.set_source_rgb(*fill); c.fill()


# ---------- props ----------
def cupcake(c, x, y, s=1.0, half=None, bite=0.0):
    """x,y = bottom center of wrapper."""
    c.save(); c.translate(x, y); c.scale(max(s, 1e-3), max(s, 1e-3))
    if half:
        c.rectangle(-200 if half == "L" else 0, -300, 200, 400); c.clip()
        if half == "L":
            c.translate(-6, 0)
        else:
            c.translate(6, 0)
    # wrapper
    c.move_to(-42, -60); c.line_to(42, -60); c.line_to(32, 0); c.line_to(-32, 0); c.close_path()
    c.set_source_rgb(*hexc("#F78FB3")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.set_line_width(3)
    for k in (-24, -8, 8, 24):
        c.move_to(k, -58); c.line_to(k * 0.78, -2); c.stroke()
    # frosting
    for (fx, fy, r) in [(-30, -72, 26), (30, -72, 26), (0, -80, 32), (-14, -104, 24), (14, -104, 24), (0, -122, 20)]:
        ellipse(c, fx, fy, r, r * 0.9, hexc("#FFF4F8"), lw=5)
    for (fx, fy, r) in [(-30, -72, 23), (30, -72, 23), (0, -80, 29), (-14, -104, 21), (14, -104, 21), (0, -122, 17)]:
        ellipse(c, fx, fy, r, r * 0.9, hexc("#FFF4F8"), stroke=False)
    for (sx, sy, col) in [(-28, -80, "#4DABF7"), (6, -96, "#FFD43B"), (24, -78, "#69DB7C"), (-8, -118, "#FF6B6B"), (-16, -92, "#B197FC")]:
        c.save(); c.translate(sx, sy); c.rotate(sx * 0.1); rrect(c, -7, -2.5, 14, 5, 2.5)
        c.set_source_rgb(*hexc(col)); c.fill(); c.restore()
    ellipse(c, 0, -146, 13, 13, hexc("#E03131"), lw=4)
    c.restore()
    if bite > 0:
        pass


# ---------- characters ----------
GRAY, GRAY_L, PINK = hexc("#A7A9BE"), hexc("#D6D7E3"), hexc("#FFA8C5")


def nib(c, x, y, facing=1, hop=0.0, arms_up=False, offer=False, look="normal", blink=False):
    c.save(); c.translate(x, y - hop); c.scale(facing, 1)
    # tail
    c.move_to(-50, -35); c.curve_to(-110, -20, -130, -90, -95, -100)
    c.curve_to(-70, -108, -70, -70, -90, -72)
    c.set_source_rgb(*INK); c.set_line_width(13); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke_preserve()
    c.set_source_rgb(*PINK); c.set_line_width(6); c.stroke()
    # feet
    ellipse(c, -22, -6, 18, 9, PINK, lw=5); ellipse(c, 26, -6, 18, 9, PINK, lw=5)
    # body
    ellipse(c, 0, -52, 58, 48, GRAY)
    ellipse(c, 14, -42, 32, 28, GRAY_L, stroke=False)
    # ears (behind head)
    for ex, ey in [(28, -142), (80, -146)]:
        ellipse(c, ex, ey, 30, 30, GRAY); ellipse(c, ex, ey, 17, 17, PINK, stroke=False)
    # head
    ellipse(c, 58, -98, 46, 42, GRAY)
    ellipse(c, 70, -86, 26, 18, GRAY_L, stroke=False)
    # eye
    if blink:
        c.move_to(62, -104); c.curve_to(68, -96, 80, -96, 86, -104)
        c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    else:
        ellipse(c, 74, -106, 13, 15, (1, 1, 1), lw=4)
        ellipse(c, 77 if look != "back" else 69, -104, 8, 9, INK, stroke=False)
        ellipse(c, 80 if look != "back" else 72, -108, 3, 3, (1, 1, 1), stroke=False)
    # cheek + nose + smile
    ellipse(c, 64, -82, 9, 6, hexc("#FFB3C7"), stroke=False)
    ellipse(c, 104, -90, 9, 8, hexc("#FF7AA8"), lw=4)
    c.move_to(84, -76); c.curve_to(90, -70, 96, -70, 100, -76)
    c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    c.set_line_width(2.5)
    for dy in (-6, 4):
        c.move_to(108, -88 + dy * 0.3); c.line_to(138, -92 + dy); c.stroke()
    # arms
    c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if arms_up:
        c.move_to(20, -80); c.line_to(30, -150); c.move_to(55, -70); c.line_to(70, -150)
    elif offer:
        c.move_to(30, -60); c.line_to(88, -78)
    else:
        c.move_to(28, -55); c.line_to(48, -30)
    c.stroke()
    c.restore()


ORANGE, ORANGE_D, CREAM = hexc("#F7A440"), hexc("#D97A1E"), hexc("#FFF3DE")


def bun(c, x, y, facing=1, sx=1.0, sy=1.0, eyes="normal", crouch=0.0, tail_wag=0.0):
    """x,y = feet center. facing=+1 looks right."""
    c.save(); c.translate(x, y); c.scale(facing * sx, sy)
    # tail
    w = tail_wag
    c.move_to(-150, -120); c.curve_to(-250, -140, -240 + 30 * w, -300, -190 + 40 * w, -330)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_source_rgb(*INK); c.set_line_width(46); c.stroke_preserve()
    c.set_source_rgb(*ORANGE); c.set_line_width(34); c.stroke()
    # back legs
    ellipse(c, -95, -22, 46, 28, ORANGE); ellipse(c, 70, -22, 42, 26, ORANGE)
    # body
    ellipse(c, -10, -120 + crouch * 20, 168, 110 - crouch * 15, ORANGE)
    ellipse(c, 40, -95 + crouch * 20, 90, 60, CREAM, stroke=False)
    c.set_source_rgb(*ORANGE_D); c.set_line_width(14); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in (-90, -40, 10):
        c.move_to(k - 15, -222 + crouch * 30); c.curve_to(k, -195, k, -175, k + 10, -160); c.stroke()
    # front paws
    ellipse(c, 90, -12, 38, 22, CREAM); ellipse(c, 150, -12, 38, 22, CREAM)
    hx, hy = 150, -232 + crouch * 60
    # ears
    for ex in (-58, 58):
        c.save(); c.translate(hx + ex, hy - 70); c.rotate(ex * 0.006)
        c.move_to(-36, 20); c.line_to(0, -56); c.line_to(36, 20); c.close_path()
        c.set_source_rgb(*ORANGE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        c.move_to(-18, 10); c.line_to(0, -30); c.line_to(18, 10); c.close_path()
        c.set_source_rgb(*hexc("#FFB3C7")); c.fill(); c.restore()
    # head
    ellipse(c, hx, hy, 104, 96, ORANGE)
    c.set_source_rgb(*ORANGE_D); c.set_line_width(12)
    for k in (-26, 0, 26):
        c.move_to(hx + k, hy - 92); c.line_to(hx + k * 0.8, hy - 62); c.stroke()
    ellipse(c, hx + 22, hy + 38, 66, 44, CREAM, stroke=False)
    # eyes
    ex1, ex2, ey = hx - 10, hx + 54, hy - 12
    c.set_source_rgb(*INK); c.set_line_width(7)
    if eyes == "happy":
        for ex in (ex1, ex2):
            c.move_to(ex - 20, ey + 6); c.curve_to(ex - 10, ey - 14, ex + 10, ey - 14, ex + 20, ey + 6); c.stroke()
    elif eyes == "dizzy":
        for ex in (ex1, ex2):
            c.save(); c.translate(ex, ey)
            c.move_to(0, 0)
            for i in range(60):
                a = i * 0.35; r = i * 0.38
                c.line_to(r * math.cos(a), r * math.sin(a))
            c.set_line_width(5); c.stroke(); c.restore()
    elif eyes == "squish":
        for ex in (ex1, ex2):
            c.move_to(ex - 18, ey - 12); c.line_to(ex + 18, ey + 4); c.move_to(ex - 18, ey + 4); c.line_to(ex + 18, ey - 12); c.stroke()
    else:
        big = 1.25 if eyes == "surprised" else 1.0
        for ex in (ex1, ex2):
            ellipse(c, ex, ey, 22 * big, 27 * big, (1, 1, 1), lw=5)
            pr = 9 if eyes == "surprised" else 14
            ellipse(c, ex + 6, ey + 2, pr * 0.85, pr, INK, stroke=False)
            ellipse(c, ex + 10, ey - 5, 4, 4, (1, 1, 1), stroke=False)
    # nose + mouth
    nx, ny = hx + 30, hy + 24
    c.move_to(nx - 12, ny - 6); c.line_to(nx + 12, ny - 6); c.line_to(nx, ny + 7); c.close_path()
    c.set_source_rgb(*hexc("#FF7AA8")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    c.set_line_width(5)
    if eyes in ("happy",):
        c.move_to(nx - 26, ny + 16); c.curve_to(nx - 10, ny + 40, nx + 10, ny + 40, nx + 26, ny + 16); c.stroke()
    elif eyes == "surprised":
        ellipse(c, nx, ny + 30, 11, 14, hexc("#8B2E3C"), lw=4)
    else:
        c.move_to(nx - 24, ny + 18); c.curve_to(nx - 12, ny + 30, nx, ny + 24, nx, ny + 8)
        c.curve_to(nx, ny + 24, nx + 12, ny + 30, nx + 24, ny + 18); c.stroke()
    # whiskers
    c.set_line_width(3)
    for d in (-1, 1):
        for k in (-8, 6):
            c.move_to(nx + d * 40, ny + 10 + k * 0.4); c.line_to(nx + d * 100, ny + k + 2 * d); c.stroke()
    c.restore()
    return  # head world pos is computed by callers


# ---------- scenes ----------
def background(c):
    g = cairo.LinearGradient(0, 0, 0, FLOOR)
    g.add_color_stop_rgb(0, *hexc("#FFF4D6")); g.add_color_stop_rgb(1, *hexc("#FFE3A3"))
    c.rectangle(0, 0, W, FLOOR); c.set_source(g); c.fill()
    # wallpaper dots
    c.set_source_rgba(*hexc("#F5C56B"), 0.45)
    for row in range(14):
        for col in range(9):
            xx = col * 130 + (65 if row % 2 else 0)
            c.arc(xx, 80 + row * 100, 9, 0, 2 * math.pi); c.fill()
    # window
    rrect(c, 560, 380, 380, 330, 26); c.set_source_rgb(*INK); c.fill()
    rrect(c, 574, 394, 352, 302, 18)
    sky = cairo.LinearGradient(0, 394, 0, 696)
    sky.add_color_stop_rgb(0, *hexc("#74C0FC")); sky.add_color_stop_rgb(1, *hexc("#D0EBFF"))
    c.set_source(sky); c.fill()
    for (cx, cy, s) in [(660, 480, 1.0), (830, 560, 0.75)]:
        for (dx, dy, r) in [(-30, 0, 30), (0, -16, 38), (34, 0, 30)]:
            c.arc(cx + dx * s, cy + dy * s, r * s, 0, 2 * math.pi); c.set_source_rgb(1, 1, 1); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(12)
    c.move_to(750, 394); c.line_to(750, 696); c.move_to(574, 545); c.line_to(926, 545); c.stroke()
    rrect(c, 540, 700, 420, 30, 10); c.set_source_rgb(*hexc("#E8F7EE")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    # potted plant on sill
    c.move_to(880, 700); c.line_to(870, 640); c.line_to(940, 640); c.line_to(930, 700); c.close_path()
    c.set_source_rgb(*hexc("#E8590C")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    for a in (-0.6, 0, 0.6):
        c.save(); c.translate(905, 640); c.rotate(a); ellipse(c, 0, -34, 14, 34, hexc("#51CF66"), lw=4); c.restore()
    # floor
    c.rectangle(0, FLOOR, W, H - FLOOR); c.set_source_rgb(*hexc("#C98A55")); c.fill()
    c.set_source_rgb(*hexc("#B3743F")); c.set_line_width(4)
    for i in range(1, 8):
        yy = FLOOR + i * 70
        c.move_to(0, yy); c.line_to(W, yy); c.stroke()
        for k in range(4):
            xx = (k * 290 + i * 137) % W
            c.move_to(xx, yy - 70); c.line_to(xx, yy); c.stroke()
    c.rectangle(0, FLOOR - 28, W, 28); c.set_source_rgb(*hexc("#FFFFFF")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    # rug
    ellipse(c, 640, FLOOR + 90, 360, 60, hexc("#9775FA"), lw=6)
    ellipse(c, 640, FLOOR + 90, 300, 42, hexc("#B197FC"), stroke=False)


def fridge(c, dent=0.0):
    rrect(c, 40, 640, 300, FLOOR - 640 + 6, 34); c.set_source_rgb(*hexc("#D0EBFF")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    c.move_to(44, 930); c.line_to(336, 930); c.stroke()
    rrect(c, 280, 720, 22, 150, 10); c.set_source_rgb(*hexc("#868E96")); c.fill()
    rrect(c, 280, 990, 22, 220, 10); c.fill()
    # magnets / drawings
    c.save(); c.translate(120, 760); c.rotate(-0.08)
    c.rectangle(0, 0, 110, 90); c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    c.arc(55, 48, 24, 0, 2 * math.pi); c.set_source_rgb(*hexc("#FFD43B")); c.fill()
    c.restore()
    ellipse(c, 175, 752, 12, 12, hexc("#FF6B6B"), lw=4)


def iris(c, cx, cy, r):
    c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.rectangle(-50, -50, W + 100, H + 100)
    c.arc(cx, cy, max(r, 0.1), 0, 2 * math.pi)
    c.set_source_rgb(0.08, 0.05, 0.1); c.fill()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)


def title_card(c, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc("#B197FC")); g.add_color_stop_rgb(1, *hexc("#FF8FB1"))
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    # rotating sunburst
    c.save(); c.translate(W / 2, 820); c.rotate(t * 0.4)
    for i in range(16):
        a = i * 2 * math.pi / 16
        c.move_to(0, 0); c.arc(0, 0, 1500, a, a + math.pi / 16); c.close_path()
        c.set_source_rgba(1, 1, 1, 0.12); c.fill()
    c.restore()
    for i, ch in enumerate("Nib & Bun"):
        p = back_out(seg(t, 0.1 + i * 0.07, 0.5 + i * 0.07))
        if p <= 0:
            continue
        x = 190 + i * 88
        y = 800 - 30 * math.sin(t * 5 + i * 0.7) * (1 - seg(t, 1.6, 2.2) * 0.6)
        c.save(); c.translate(x, y); c.scale(max(p, 1e-3), max(p, 1e-3))
        cols = ["#FFD43B", "#FFFFFF", "#FFD43B"]
        text(c, ch, 0, 0, 170, hexc(cols[i % 3]), olw=18)
        c.restore()
    p = ease_out(seg(t, 0.9, 1.4))
    if p > 0:
        c.save(); c.translate(W / 2, 960 + (1 - p) * 60); c.set_source_rgba(1, 1, 1, p)
        text(c, "The Cupcake Caper", 0, 0, 80, (1, 1, 1), olw=12); c.restore()
    cupcake(c, W / 2, 1380 + 10 * math.sin(t * 6), 1.6)
    nib(c, 250, 1640, 1, hop=abs(math.sin(t * 7)) * 20)
    c.save(); c.translate(820, 1680); c.scale(0.55, 0.55); bun(c, 0, 0, -1, eyes="happy", tail_wag=math.sin(t * 6)); c.restore()


def scene(c, t):
    shake = 0
    if 11.2 <= t < 11.6:
        k = 1 - seg(t, 11.2, 11.6)
        random.seed(int(t * 60))
        c.translate(W / 2, H / 2); c.scale(1.06, 1.06); c.translate(-W / 2, -H / 2)
        c.translate(random.uniform(-26, 26) * k, random.uniform(-26, 26) * k)
    background(c)
    fridge(c)

    # ----- Bun -----
    if t < 7.6:
        pass  # off screen
    elif t < 10.0:
        # peek in from the right edge
        p = ease_out(seg(t, 7.6, 8.2))
        bx = lerp(1420, 1210, p)
        crouch = ease(seg(t, 9.5, 10.0))
        eyes = "surprised" if 8.5 <= t < 9.4 else "normal"
        bun(c, bx, FLOOR, -1, eyes=eyes, crouch=crouch, tail_wag=math.sin(t * 8))
        if 8.5 <= t < 9.6:
            s = back_out(seg(t, 8.5, 8.75)) * (1 - seg(t, 9.35, 9.6))
            c.save(); c.translate(1010, 1010); c.scale(max(s, 1e-3), max(s, 1e-3)); c.rotate(0.1 * math.sin(t * 30))
            text(c, "!", 0, 0, 220, hexc("#FF4757"), olw=16); c.restore()
    elif t < 11.2:
        p = seg(t, 10.0, 11.2)
        bx = lerp(1210, 480 + 250 * 0.6 - 250 * 0.6 * 0 + 0, ease(p) * 0 + p)  # linear travel
        bx = lerp(1210, 585, p)
        by = FLOOR - 430 * math.sin(math.pi * 0.72 * p)
        bun(c, bx, by, -1, sx=1.18, sy=0.86, eyes="normal", tail_wag=-1)
        # speed lines
        c.set_source_rgba(*INK, 0.5); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for k in range(4):
            yy = by - 80 - k * 55
            c.move_to(bx + 220 + k * 20, yy); c.line_to(bx + 360 + k * 30, yy); c.stroke()
    elif t < 13.0:
        # squashed on fridge, then sliding down
        slide = ease(seg(t, 11.6, 13.0)) if t >= 11.6 else 0
        sxv = lerp(0.55, 0.75, seg(t, 11.2, 11.35))
        sxv = 0.55 + 0.04 * math.sin(t * 40) * (1 - seg(t, 11.2, 11.6))
        X = 340 + 254 * sxv
        Y = lerp(1180, FLOOR, slide)
        bun(c, X, Y, -1, sx=sxv, sy=1.12, eyes="squish")
        if t < 12.0:
            s = back_out(seg(t, 11.2, 11.4)) * (1 - seg(t, 11.8, 12.0))
            c.save(); c.translate(560, 820); c.rotate(-0.15); c.scale(max(s, 1e-3), max(s, 1e-3))
            for i in range(12):
                a = i * math.pi / 6
                r = 190 if i % 2 == 0 else 120
                (c.move_to if i == 0 else c.line_to)(r * math.cos(a), r * 0.7 * math.sin(a))
            c.close_path(); c.set_source_rgb(*hexc("#FFE066")); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
            text(c, "BONK!", 0, 30, 96, hexc("#FF4757"), olw=12)
            c.restore()
    else:
        # flips around and sits dizzy, then happy
        flip = ease(seg(t, 13.0, 13.35))
        f = lerp(-1, 1, flip)
        X = lerp(340 + 254, 335, flip)
        bounce = abs(math.sin(seg(t, 13.0, 13.5) * math.pi)) * 40 * (1 - seg(t, 13.0, 13.5))
        if t < 17.2:
            eyes = "dizzy"
        else:
            eyes = "happy"
        wag = math.sin(t * 7) if t >= 17.2 else 0
        bun(c, X, FLOOR - bounce, 1 if f >= 0 else -1, sx=max(abs(f), 0.05), eyes=eyes, tail_wag=wag)
        hx, hy = X + 150, FLOOR - 232
        if 13.3 <= t < 17.3:
            fade = 1 - seg(t, 16.9, 17.3)
            for k in range(3):
                a = t * 4 + k * 2 * math.pi / 3
                star(c, hx + 120 * math.cos(a), hy - 110 + 30 * math.sin(a), 30 * fade, t * 3 + k)

    # ----- Nib -----
    holding = 6.0 <= t < 16.9
    if t < 6.0:
        p = seg(t, 2.5, 6.0)
        nx = lerp(-120, 440, p)
        hop = abs(math.sin(p * 8 * math.pi)) * 34
        nib(c, nx, FLOOR + 40, 1, hop=hop)
    elif t < 10.88:
        nx = 440
        lift = ease_out(seg(t, 6.0, 6.5))
        look = "back" if 8.6 <= t < 10.6 else "normal"
        face = -1 if 9.0 <= t < 10.5 else 1
        nib(c, nx, FLOOR + 40, face, arms_up=True, look="normal" if face == -1 else look,
            blink=(7.1 < t < 7.25))
    elif t < 15.5:
        p = ease_out(seg(t, 10.88, 11.08))
        nx = lerp(440, 820, p)
        nib(c, nx, FLOOR + 40, 1 if t < 13.4 else -1, arms_up=True, blink=(14.0 < t < 14.15))
        if t < 11.5:
            a = 1 - seg(t, 11.08, 11.5)
            c.set_source_rgba(*INK, 0.5 * a); c.set_line_width(6)
            for k in range(3):
                c.move_to(nx - 90 - k * 10, FLOOR - 20 - k * 40); c.line_to(nx - 220 - k * 30, FLOOR - 20 - k * 40); c.stroke()
    else:
        p = seg(t, 15.5, 16.7)
        nx = lerp(820, 690, p)
        hop = abs(math.sin(p * 4 * math.pi)) * 24
        arms = t < 16.7
        nib(c, nx, FLOOR + 40, -1, hop=hop, arms_up=arms, offer=not arms, blink=(18.6 < t < 18.75))

    # ----- cupcake -----
    if t < 6.0:
        cupcake(c, 590, FLOOR + 30, 1.0)
        if 4.5 < t < 6.0:  # sparkle to draw the eye
            s = 0.6 + 0.4 * math.sin(t * 12)
            star(c, 650, FLOOR - 140, 18 * s, t * 4, fill=(1, 1, 1))
    elif t < 16.9:
        # held overhead
        if t < 10.88:
            cx = 440 + (60 if not (9.0 <= t < 10.5) else -60)
        elif t < 15.5:
            cx = lerp(440, 820, ease_out(seg(t, 10.88, 11.08))) + (60 if t < 13.4 else -60)
        else:
            cx = lerp(820, 690, seg(t, 15.5, 16.7)) - 60
        lift = ease_out(seg(t, 6.0, 6.5))
        cy = lerp(FLOOR + 30, FLOOR - 135, lift)
        cupcake(c, cx, cy, 0.9)
        if 6.2 < t < 6.9:
            for k in range(5):
                a = k * 2 * math.pi / 5 + t * 2
                rr = 110 * ease_out(seg(t, 6.2, 6.9))
                star(c, cx + rr * math.cos(a), cy - 70 + rr * math.sin(a), 16 * (1 - seg(t, 6.6, 6.9)), t * 5, fill=(1, 1, 1))
    else:
        # split: one half to Bun, one stays with Nib
        p = ease_out(seg(t, 16.9, 17.3))
        nx = 690
        bite = seg(t, 17.6, 19.4)
        s_half = 0.9 * (1 - 0.6 * bite)
        lx = lerp(630, 560, p); ly = lerp(FLOOR - 25, FLOOR - 115, p)
        cupcake(c, lx, ly, s_half, half="L")
        cupcake(c, lerp(630, 610, p), lerp(FLOOR - 25, FLOOR + 10, p), s_half * 0.85, half="R")
        if 16.9 < t < 17.3:
            s = 1 - seg(t, 16.9, 17.3)
            for k in range(6):
                a = k * math.pi / 3
                c.set_source_rgb(*hexc("#FFF4F8")); c.arc(630 + 70 * (1 - s) * math.cos(a), FLOOR - 90 + 70 * (1 - s) * math.sin(a), 9 * s, 0, 2 * math.pi); c.fill()

    # ----- hearts -----
    if t >= 17.3:
        for k in range(5):
            st = 17.3 + k * 0.35
            if t < st:
                continue
            q = seg(t, st, st + 1.6)
            if q >= 1:
                continue
            hx = 560 + 70 * math.sin(k * 2.1) + 25 * math.sin(t * 4 + k)
            hy = FLOOR - 330 - q * 300
            heart(c, hx, hy, 1.4 + 0.4 * math.sin(k), 1 - q)


def frame(c, t):
    if t < 2.5:
        title_card(c, t)
        if t > 2.2:
            iris(c, W / 2, H / 2, lerp(1200, 0, ease(seg(t, 2.2, 2.5))))
        return
    c.save(); scene(c, t); c.restore()
    if t < 2.9:
        iris(c, 540, 1300, lerp(0, 1300, ease(seg(t, 2.5, 2.9))))
    if t >= 18.8:
        iris(c, 560, 1250, lerp(1400, 0, ease(seg(t, 18.8, 19.4))))
    if t >= 19.4:
        p = back_out(seg(t, 19.4, 19.75))
        c.save(); c.translate(W / 2, H / 2); c.scale(max(p, 1e-3), max(p, 1e-3))
        text(c, "The End", 0, 0, 150, hexc("#FFD43B"), olw=14)
        c.restore()
        heart(c, W / 2, H / 2 + 160, 2.2 * p, 1)


def main(out_path, preview=None):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    if preview is not None:
        c = cairo.Context(surf); frame(c, preview); surf.write_to_png(out_path); return
    proc = subprocess.Popen(
        ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra", "-s", f"{W}x{H}",
         "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
         "-pix_fmt", "yuv420p", out_path], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        c = cairo.Context(surf)
        c.set_source_rgb(0, 0, 0); c.paint()
        frame(c, i / FPS)
        surf.flush()
        proc.stdin.write(bytes(surf.get_data()))
    proc.stdin.close(); proc.wait()


if __name__ == "__main__":
    if len(sys.argv) > 2:
        main(sys.argv[1], float(sys.argv[2]))
    else:
        main(sys.argv[1])
