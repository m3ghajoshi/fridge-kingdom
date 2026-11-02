"""FRIDGE KINGDOM — Episode 3: "The Outside". 40s, 1080x1920 @ 30fps.

Dill is dropped onto a plate in the giant kitchen, nearly becomes a sandwich topping,
escapes down a spoon, over a sugar bowl and off the counter, races the closing fridge
door... and gets locked out. Inside, Crumb wears the crown. Three knocks.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crumb, duck, hand, crown, fridge_bg, dark_overlay, ellipse, rrect, star, text,
                 iris, hexc, seg, ease, ease_out, lerp, back_out, INK, GOLD, FLOOR, TOP, W, H, FPS, S, BREAD, CRUST)
from ep2 import title_card, end_card

DUR = 40.0
END_T = 38.3          # TO BE CONTINUED card starts

# ---- kitchen world coordinates ----
CY = 1350             # counter surface
FY = 2550             # kitchen floor
EDGE = 2000           # counter's right edge
PY = CY - 110         # plate surface (plate sits on a cutting board)
STACK_X = 300         # sandwich stack centre
DILL_PLATE_X = 640
SP0 = (830, PY - 30)  # spoon bowl (top of the slide)
SP1 = (1480, CY - 14) # spoon handle end (bottom)
BOWL_X = 1660         # sugar bowl
FX0, FX1 = 3200, 4500 # fridge left/right


# ---------------- kitchen props ----------------
def kitchen_bg(c):
    c.rectangle(-3000, -3000, 12000, 9000); c.set_source_rgb(*hexc("#FFF1D6")); c.fill()
    # wall tiles
    c.set_source_rgba(*hexc("#E8C99A"), 0.8); c.set_line_width(5)
    for i in range(-10, 60):
        c.move_to(i * 160, -800); c.line_to(i * 160, FY); c.stroke()
    for j in range(-6, 20):
        c.move_to(-1000, j * 160); c.line_to(6000, j * 160); c.stroke()
    # window with sky
    rrect(c, 260, -300, 1200, 980, 30); c.set_source_rgb(*hexc("#A5D8FF")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(14); c.stroke()
    ellipse(c, 600, 300, 160, 60, (1, 1, 1), stroke=False); ellipse(c, 720, 260, 120, 70, (1, 1, 1), stroke=False)
    c.set_source_rgb(*hexc("#F8F9FA")); c.set_line_width(26)
    c.move_to(860, -300); c.line_to(860, 680); c.move_to(260, 200); c.line_to(1460, 200); c.stroke()
    # floor (checker)
    c.rectangle(-3000, FY, 12000, 2000); c.set_source_rgb(*hexc("#F1F3F5")); c.fill()
    for i in range(-20, 60):
        for j in range(0, 6):
            if (i + j) % 2 == 0:
                c.rectangle(i * 200, FY + j * 200, 200, 200); c.set_source_rgb(*hexc("#4C6EF5")); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(8); c.move_to(-3000, FY); c.line_to(9000, FY); c.stroke()
    # counter: cabinets + top
    c.rectangle(-3000, CY + 60, 3000 + EDGE, FY - CY - 60); c.set_source_rgb(*hexc("#3E7C87")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    for k in range(-6, 4):
        x0 = 60 + k * 480
        if x0 + 440 > EDGE: break
        rrect(c, x0, CY + 120, 420, FY - CY - 180, 24); c.set_source_rgb(*hexc("#4E96A2")); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        ellipse(c, x0 + 370, CY + 420, 18, 18, GOLD, lw=5)
    rrect(c, -3000, CY, 3000 + EDGE + 30, 64, 10); c.set_source_rgb(*hexc("#D9A066")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.35); c.rectangle(-3000, CY + 8, 3000 + EDGE, 8); c.fill()


def cutting_board(c):
    rrect(c, 0, CY - 84, 860, 84, 16); c.set_source_rgb(*hexc("#E3B474")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.set_source_rgba(*hexc("#B9844A"), 0.7); c.set_line_width(4)
    for k in range(3):
        c.move_to(40, CY - 60 + k * 20); c.line_to(820, CY - 60 + k * 20); c.stroke()


def plate(c):
    ellipse(c, 420, PY + 16, 400, 40, hexc("#DEE2E6"), lw=7)
    ellipse(c, 420, PY, 400, 34, (1, 1, 1), lw=7)
    ellipse(c, 420, PY + 2, 290, 20, hexc("#F1F3F5"), stroke=False)
    c.set_source_rgb(*hexc("#74C0FC")); c.set_line_width(5)
    c.save(); c.translate(420, PY); c.scale(370, 28); c.arc(0, 0, 1, 0.15, math.pi - 0.15); c.restore(); c.stroke()


def bread_slab(c, x, yb, w=420, h=80, rot=0.0):
    c.save(); c.translate(x, yb); c.rotate(rot)
    rrect(c, -w / 2, -h, w, h, 26); c.set_source_rgb(*CRUST); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    rrect(c, -w / 2 + 16, -h + 14, w - 32, h - 28, 16); c.set_source_rgb(*BREAD); c.fill()
    for k in range(7):
        ellipse(c, -w / 2 + 50 + k * (w - 100) / 6, -h / 2 + (6 if k % 2 else -5), 6, 4, hexc("#E0B97A"), stroke=False)
    c.restore()


def lettuce(c, x, yb, w=460):
    c.save(); c.translate(x, yb)
    c.move_to(-w / 2, 0)
    n = 12
    for i in range(n + 1):
        px = -w / 2 + w * i / n
        c.line_to(px, -38 - (14 if i % 2 else 0))
    c.line_to(w / 2, 0); c.close_path()
    c.set_source_rgb(*hexc("#8CE99A")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.set_source_rgb(*hexc("#40C057")); c.set_line_width(4)
    for i in range(1, n, 2):
        px = -w / 2 + w * i / n
        c.move_to(px, -6); c.line_to(px + 8, -36); c.stroke()
    c.restore()


def tomato(c, x, yb, w=380):
    c.save(); c.translate(x, yb)
    for k, dx in enumerate((-w / 4, w / 4)):
        rrect(c, dx - w / 4 - 6, -42, w / 2 + 12, 42, 18); c.set_source_rgb(*hexc("#FA5252")); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        for s in (-50, -15, 20, 55):
            ellipse(c, dx + s * w / 380, -21, 7, 10, hexc("#FFE066"), stroke=False)
    c.restore()


def big_spoon(c):
    (x0, y0), (x1, y1) = SP0, SP1
    ang = math.atan2(y1 - y0, x1 - x0)
    L = math.hypot(x1 - x0, y1 - y0)
    c.save(); c.translate(x0, y0); c.rotate(ang)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_source_rgb(*INK); c.set_line_width(46); c.move_to(60, 0); c.line_to(L, 0); c.stroke()
    c.set_source_rgb(*hexc("#CED4DA")); c.set_line_width(32); c.move_to(60, 0); c.line_to(L, 0); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(8); c.move_to(120, -6); c.line_to(L - 40, -6); c.stroke()
    ellipse(c, 0, 0, 120, 52, hexc("#CED4DA"), lw=8)
    ellipse(c, -6, -8, 86, 30, hexc("#E9ECEF"), stroke=False)
    c.restore()


def spoon_point(p):
    (x0, y0), (x1, y1) = SP0, SP1
    return lerp(x0, x1, p), lerp(y0, y1, p) - 18


def mug(c, x):
    rrect(c, x - 150, CY - 380, 300, 380, 30); c.set_source_rgb(*hexc("#E8590C")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    c.set_line_width(36); c.set_source_rgb(*INK)
    c.save(); c.translate(x + 150, CY - 200); c.scale(90, 110); c.arc(0, 0, 1, -math.pi / 2, math.pi / 2); c.restore(); c.stroke()
    c.set_line_width(22); c.set_source_rgb(*hexc("#E8590C"))
    c.save(); c.translate(x + 150, CY - 200); c.scale(90, 110); c.arc(0, 0, 1, -math.pi / 2, math.pi / 2); c.restore(); c.stroke()
    ellipse(c, x - 40, CY - 220, 50, 50, hexc("#FFD8A8"), stroke=False)   # a plain dot pattern
    ellipse(c, x + 60, CY - 120, 34, 34, hexc("#FFD8A8"), stroke=False)


def sugar_bowl(c, squash=0.0):
    c.save(); c.translate(BOWL_X, CY); c.scale(1 + 0.08 * squash, 1 - 0.08 * squash)
    # sugar heap
    c.move_to(-170, -250); c.curve_to(-120, -330, 120, -330, 170, -250); c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    for k in range(9):
        ellipse(c, -110 + k * 27, -268 - (k % 3) * 10, 4, 4, hexc("#DEE2E6"), stroke=False)
    # bowl
    c.move_to(-190, -260); c.line_to(190, -260); c.curve_to(190, -80, 120, 0, 0, 0); c.curve_to(-120, 0, -190, -80, -190, -260)
    c.close_path(); c.set_source_rgb(*hexc("#E7F5FF")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    c.set_source_rgb(*hexc("#4DABF7")); c.set_line_width(14)
    c.move_to(-184, -200); c.line_to(184, -200); c.stroke()
    c.move_to(-168, -150); c.line_to(168, -150); c.stroke()
    c.restore()


SPRINKLES = []
_r = random.Random(7)
for _ in range(70):
    SPRINKLES.append((_r.uniform(1860, EDGE - 20), CY - _r.uniform(4, 14), _r.uniform(0, math.pi),
                      _r.choice(["#FF6B6B", "#4DABF7", "#FFD43B", "#69DB7C", "#B197FC", "#FF8FB3"])))


def sprinkles(c, kick=None):
    for (x, y, a, col) in SPRINKLES:
        dx = dy = 0
        if kick is not None:
            k = kick(x)
            dx, dy = k * 40, -k * 120
        c.save(); c.translate(x + dx, y + dy); c.rotate(a + (dx * 0.05)); rrect(c, -14, -5, 28, 10, 5)
        c.set_source_rgb(*hexc(col)); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2); c.stroke(); c.restore()


def door_theta(t):
    """Fridge door angle (radians, 0 = shut)."""
    if t < 23.0:
        return 0.80
    return 0.80 * (1 - ease(seg(t, 23.0, 30.3)) ** 1.15)


def fridge_front(c, t):
    th = door_theta(t)
    top, bot = FY - 2700, FY - 130
    # body & base
    c.rectangle(FX0, top, FX1 - FX0, FY - top); c.set_source_rgb(*hexc("#DDE7EE")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(10); c.stroke()
    c.rectangle(FX0 + 20, FY - 120, FX1 - FX0 - 40, 110); c.set_source_rgb(*hexc("#868E96")); c.fill()
    for k in range(10):
        c.rectangle(FX0 + 60 + k * 120, FY - 95, 60, 14); c.set_source_rgb(*hexc("#495057")); c.fill()
    # interior (bright) visible in the gap
    xl = FX1 - (FX1 - FX0) * math.cos(th)
    if xl > FX0 + 2:
        c.save(); c.rectangle(FX0 + 10, top + 10, xl - FX0 - 10, bot - top - 10); c.clip()
        g = cairo.LinearGradient(FX0, 0, xl, 0)
        g.add_color_stop_rgb(0, *hexc("#F3FAFF")); g.add_color_stop_rgb(1, *hexc("#BFE0F5"))
        c.set_source(g); c.paint()
        for sy in (bot - 700, bot - 1450):
            c.rectangle(FX0, sy, 3000, 26); c.set_source_rgba(*hexc("#74C0FC"), 0.8); c.fill()
        # a tiny silhouette of the Pickle Jar on the top shelf, glimpsed through the gap
        rrect(c, FX0 + 60, bot - 1450 - 200, 110, 200, 20); c.set_source_rgba(*hexc("#2F9E44"), 0.6); c.fill()
        rrect(c, FX0 + 54, bot - 1450 - 228, 122, 34, 8); c.set_source_rgba(*hexc("#E03131"), 0.8); c.fill()
        c.restore()
        # light spilling onto the floor
        c.move_to(FX0, FY); c.line_to(xl, FY); c.line_to(xl - 200, FY + 300); c.line_to(FX0 - 500, FY + 300); c.close_path()
        c.set_source_rgba(1, 1, 0.85, 0.35 * min(1, (xl - FX0) / 200)); c.fill()
    # the door: hinged on the right, its free edge swings toward us
    e = 160 * math.sin(th)
    c.move_to(xl, top - e); c.line_to(FX1, top); c.line_to(FX1, bot); c.line_to(xl, bot + e); c.close_path()
    c.set_source_rgb(*hexc("#F1F5F9")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(10); c.stroke()
    # handle + magnets ride on the door
    def at(u, y):
        x = lerp(xl, FX1, u)
        yy = y + (1 - u) * e * ((y - (top + bot) / 2) / ((bot - top) / 2))
        return x, yy
    hx, hy0 = at(0.06, FY - 1500); _, hy1 = at(0.06, FY - 700)
    rrect(c, hx - 22, hy0, 44, hy1 - hy0, 22); c.set_source_rgb(*hexc("#ADB5BD")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    sx = max(math.cos(th), 0.2)
    for (u, y, kind) in [(0.25, FY - 900, "banana"), (0.33, FY - 1350, "star"), (0.22, FY - 1800, "pizza")]:
        x, yy = at(u, y)
        c.save(); c.translate(x, yy); c.scale(sx, 1)
        if kind == "banana":
            c.move_to(-70, -20); c.curve_to(-40, 50, 50, 50, 80, -30); c.curve_to(40, 20, -30, 20, -70, -20)
            c.set_source_rgb(*hexc("#FFE066")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        elif kind == "star":
            c.restore(); c.save(); c.translate(x, yy); star(c, 0, 0, 70, 0.1, hexc("#FF922B"))
        else:
            c.move_to(-60, -50); c.line_to(60, -50); c.line_to(0, 70); c.close_path()
            c.set_source_rgb(*hexc("#FFC078")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
            c.rectangle(-66, -62, 132, 18); c.set_source_rgb(*hexc("#D9480F")); c.fill()
            for px, py in [(-20, -20), (18, -10), (0, 20)]:
                ellipse(c, px, py, 11, 11, hexc("#E03131"), stroke=False)
        c.restore()


# ---------------- Dill's path through the kitchen ----------------
def stack_top(t):
    """Height of the sandwich stack above the plate."""
    h = 0
    if t >= 6.4: h = 80
    if t >= 7.9: h = 118
    if t >= 9.2: h = 160
    return h


def drop_y(t, t0, target):
    """Something falling from above and landing at `target` at time t0."""
    p = seg(t, t0 - 0.45, t0)
    return lerp(target - 1400, target, p * p)


def dill_state(t):
    """Returns dict with x, y, mood, look, arm, rot, sq (or None)."""
    d = dict(mood="shocked", look=(0, 0), arm="down", rot=0.0, sq=1.0, shake=0.0)
    if t < 3.7:      # carried by the Hand
        p = ease(seg(t, 2.0, 3.4))
        tip = lerp(PY - 1500, PY - 175, p)
        d.update(x=DILL_PLATE_X, y=tip + 170, rot=math.sin(t * 20) * 0.22, look=(0, 1))
    elif t < 4.1:    # dropped
        p = seg(t, 3.7, 4.0)
        d.update(x=DILL_PLATE_X, y=lerp(PY - 5, PY, p), sq=lerp(1, 0.75, p))
    elif t < 6.4:    # awe: looking around the enormous kitchen
        b = back_out(seg(t, 4.0, 4.4))
        d.update(x=DILL_PLATE_X, y=PY, sq=lerp(0.75, 1.0, min(b, 1.2)), mood="shocked" if t < 5.0 else "frozen",
                 look=(-1, -1) if t < 5.0 else (1, -1) if t < 5.8 else (-1, 0))
    elif t < 10.0:   # the sandwich gets built next to him
        d.update(x=DILL_PLATE_X, y=PY, mood="frozen" if t < 9.4 else "shocked", look=(-1, 0.3), shake=2 if t > 9.2 else 0)
    elif t < 11.0:   # the Hand pinches him onto the tomato
        p = ease(seg(t, 10.2, 10.9))
        x = lerp(DILL_PLATE_X, STACK_X, p); y = lerp(PY, PY - 160, p) - 260 * math.sin(math.pi * p)
        d.update(x=x, y=y, rot=math.sin(t * 22) * 0.2, look=(0, 1))
    elif t < 13.6:   # the top slice lowers like a ceiling
        crouch = ease(seg(t, 12.2, 13.5))
        d.update(x=STACK_X, y=PY - 160, mood="shocked", look=(0, -1), sq=lerp(1, 0.78, crouch), shake=3 * crouch)
    elif t < 14.4:   # dives off the stack, rolls along the plate
        p = seg(t, 13.6, 14.4)
        x = lerp(STACK_X, SP0[0] - 40, ease_out(p)); y = lerp(PY - 160, PY, p) - 180 * math.sin(math.pi * min(1, p * 1.4))
        d.update(x=x, y=y, rot=p * 2 * math.pi, mood="shocked")
    elif t < 17.5:   # zips down the spoon
        p = seg(t, 14.4, 17.5) ** 1.6
        x, y = spoon_point(p)
        ang = math.atan2(SP1[1] - SP0[1], SP1[0] - SP0[0])
        d.update(x=x, y=y, rot=ang, mood="shocked" if t < 15.6 else "proud", arm="up" if t >= 15.6 else "down", look=(1, 0))
    elif t < 18.3:   # skids along the counter into the sugar bowl
        p = seg(t, 17.5, 18.0)
        d.update(x=lerp(SP1[0], BOWL_X - 230, p), y=CY, mood="shocked", look=(1, 0), rot=-0.25)
        if t >= 18.0:
            d.update(x=BOWL_X - 230, sq=0.8)
    elif t < 19.3:   # PING! bounces off and over the bowl
        p = seg(t, 18.3, 19.3)
        d.update(x=lerp(BOWL_X - 230, 1830, p), y=CY - 560 * math.sin(math.pi * p) - (0 if p < 1 else 0),
                 rot=p * -2 * math.pi, mood="shocked")
    elif t < 20.6:   # skids through the sprinkles
        p = seg(t, 19.3, 20.6)
        d.update(x=lerp(1830, EDGE - 40, ease_out(p)), y=CY, rot=-0.35, mood="smug", look=(1, 0), arm="up")
    elif t < 22.1:   # off the edge: somersaults down to the floor
        p = seg(t, 20.6, 22.1)
        x = lerp(EDGE - 40, 2200, p); y = lerp(CY, FY, p * p) - 260 * math.sin(math.pi * p)
        d.update(x=x, y=y, rot=p * 4 * math.pi, mood="shocked")
    elif t < 23.2:   # heroic landing: ta-da
        b = back_out(seg(t, 22.1, 22.5))
        d.update(x=2200, y=FY, mood="proud", arm="up", sq=lerp(0.7, 1.0, min(b, 1.15)), look=(-1, -0.5))
    elif t < 29.5:   # sees the door closing: RUN
        p = seg(t, 23.4, 29.5)
        x = lerp(2200, FX0 - 160, p)
        hop = abs(math.sin(t * 16)) * 26
        d.update(x=x, y=FY - hop, mood="shocked" if t < 24.2 else "angry", look=(1, 0),
                 rot=0.18, arm="point" if int(t * 8) % 2 else "down", shake=2)
    elif t < 30.3:   # the leap
        p = seg(t, 29.5, 30.3)
        d.update(x=lerp(FX0 - 160, FX0 + 120, p), y=lerp(FY, FY - 160, p) - 260 * math.sin(math.pi * p * 0.8),
                 mood="proud", arm="up", rot=0.35 * (1 - p), look=(1, -1))
    else:
        return None  # drawn flattened against the door separately
    return d


def flat_dill(c, t):
    """Dill splatted on the door, then slowly peeling off."""
    if t < 31.3:
        y = FY - 230; rot = 0.0
    elif t < 33.2:
        p = ease(seg(t, 31.3, 33.2)) ** 1.5
        y = lerp(FY - 230, FY, p); rot = 0.0
    else:
        y = FY; rot = -ease(seg(t, 33.2, 33.7)) * math.pi / 2
    c.save(); c.translate(FX0 + 120, y); c.rotate(rot); c.scale(1.45, 0.82)
    dill(c, 0, 0, "frozen" if t < 31.3 else "shocked", look=(0, 0), crown_on=False)
    c.restore()


def camera(t):
    if t < 13.6:
        cx, cy, Z = 470, 1050, 1.32
        if 4.0 <= t < 6.4:   # pull back a little to show how BIG everything is
            k = math.sin(math.pi * seg(t, 4.0, 6.4))
            cx, cy, Z = lerp(470, 560, k), lerp(1050, 760, k), lerp(1.32, 0.95, k)
        if t >= 12.0:        # creep in on the ceiling coming down
            k = ease(seg(t, 12.0, 13.4))
            cx, cy, Z = lerp(470, 360, k), lerp(1050, 1020, k), lerp(1.32, 1.7, k)
        return cx, cy, Z
    st = dill_state(t)
    if t < 23.2:
        x, y = st["x"], st["y"]
        k = ease(seg(t, 13.6, 14.4))
        cx = lerp(360, x + 120, k); cy = lerp(1020, y - 300, k)
        Z = lerp(1.7, 1.15, k)
        if t >= 20.6:
            cy = lerp(CY - 300, FY - 380, ease(seg(t, 20.6, 22.0)))
        return cx, cy, Z
    if t < 29.5:
        if 25.4 <= t < 26.6:   # close-up on the closing gap
            th = door_theta(t); xl = FX1 - (FX1 - FX0) * math.cos(th)
            return (FX0 + xl) / 2 + 60, FY - 700, 1.05
        x = st["x"]
        k = ease(seg(t, 22.9, 23.8))
        return lerp(2320, lerp(x + 420, FX0 - 100, 0.35), k), lerp(FY - 380, FY - 600, k), lerp(1.15, 0.86, k)
    if t < 30.3:
        k = ease(seg(t, 29.5, 30.3))
        return lerp(FX0 + 134, FX0 + 120, k), lerp(FY - 600, FY - 420, k), lerp(0.86, 1.25, k)
    return FX0 + 120, FY - 420, 1.25


def kitchen(c, t):
    cx, cy, Z = camera(t)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    random.seed(int(t * 30))
    # impact shakes
    for t0, amp in ((6.4, 14), (7.9, 10), (9.2, 10), (13.85, 22), (18.0, 10), (22.1, 16), (30.3, 30)):
        if t0 <= t < t0 + 0.35:
            k = 1 - seg(t, t0, t0 + 0.35)
            c.translate(random.uniform(-amp, amp) * k, random.uniform(-amp, amp) * k)
    kitchen_bg(c)
    mug(c, 1150)
    cutting_board(c)
    plate(c)

    # --- the sandwich assembles ---
    if t >= 5.95:
        bread_slab(c, STACK_X, drop_y(t, 6.4, PY), 420, 80)
    if t >= 7.45:
        lettuce(c, STACK_X, drop_y(t, 7.9, PY - 80), 470)
    if t >= 8.75:
        tomato(c, STACK_X, drop_y(t, 9.2, PY - 118), 390)

    big_spoon(c)
    sq = 0
    if 18.0 <= t < 18.5:
        sq = math.sin(math.pi * seg(t, 18.0, 18.5))
    sugar_bowl(c, sq)
    sprinkles(c, kick=(lambda x: max(0, 1 - abs(x - dill_state(t)["x"]) / 90) * math.sin(math.pi * seg(t, 19.3, 20.6) * 6) ** 2)
              if 19.3 <= t < 20.6 else None)

    fridge_front(c, t)

    # --- Dill ---
    st = dill_state(t)
    if st is not None:
        dill(c, st["x"], st["y"], st["mood"], look=st["look"], arm=st["arm"], crown_on=False,
             rot=st["rot"], shake=st["shake"], sq=st["sq"])
    else:
        flat_dill(c, t)

    # --- the top slice coming down like a ceiling ---
    if 11.0 <= t < 16.0:
        if t < 13.85:
            p = ease(seg(t, 11.0, 13.4))
            yb = lerp(PY - 1500, PY - 160 - 320, p)
            if t >= 13.5:
                yb = lerp(PY - 480, PY - 160, seg(t, 13.5, 13.85) ** 2)
        else:
            yb = PY - 160
        # shadow on Dill
        if t < 13.85:
            c.save(); ellipse_a = 0.25 * ease(seg(t, 11.0, 13.4))
            c.translate(STACK_X, PY - 160); c.scale(220, 26); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(0, 0, 0, ellipse_a); c.fill()
        bread_slab(c, STACK_X, yb, 420, 80)
    if t >= 16.0:
        bread_slab(c, STACK_X, PY - 160, 420, 80)
    # crumbs flying off the slam
    if 13.85 <= t < 14.6:
        p = seg(t, 13.85, 14.6)
        for k in range(8):
            a = -math.pi * (0.1 + 0.8 * k / 7)
            ellipse(c, STACK_X + math.cos(a) * 320 * p, PY - 200 + math.sin(a) * 240 * p + 300 * p * p, 9, 7, CRUST, lw=3)

    # --- the Hand ---
    if 2.0 <= t < 5.0:
        if t < 3.7:
            p = ease(seg(t, 2.0, 3.4)); tip = lerp(PY - 1500, PY - 175, p); grip = 1.0
        else:
            tip = lerp(PY - 175, PY - 1700, ease(seg(t, 3.9, 5.0))); grip = 1 - ease(seg(t, 3.6, 3.8))
        hand(c, DILL_PLATE_X, tip, grip)
    if 5.9 <= t < 9.8:   # the Hand drops each layer in
        for t0, x in ((6.4, STACK_X), (7.9, STACK_X), (9.2, STACK_X)):
            if t0 - 0.55 <= t < t0 + 0.25:
                lift = ease(seg(t, t0 - 0.05, t0 + 0.25))
                hand(c, x + 60, lerp(PY - 700, PY - 1600, lift), 0.0)
    if 9.9 <= t < 11.6:  # pinch Dill onto the stack
        if t < 10.9:
            p = ease(seg(t, 10.2, 10.9))
            x = lerp(DILL_PLATE_X, STACK_X, p) if t >= 10.2 else DILL_PLATE_X
            tip = lerp(PY - 1500, PY - 175, ease(seg(t, 9.9, 10.2))) - (260 * math.sin(math.pi * p) + 160 * p if t >= 10.2 else 0)
            hand(c, x, tip, ease(seg(t, 10.1, 10.25)))
        else:
            hand(c, STACK_X, lerp(PY - 335, PY - 1700, ease(seg(t, 10.9, 11.6))), 1 - ease(seg(t, 10.9, 11.05)))

    # --- sound-effect words ---
    if 18.0 <= t < 18.6:
        s = back_out(seg(t, 18.0, 18.2))
        c.save(); c.translate(BOWL_X - 120, CY - 520); c.rotate(-0.15); c.scale(S(s), S(s))
        text(c, "PING!", 0, 0, 120, hexc("#74C0FC"), olw=12); c.restore()
    if 22.1 <= t < 23.2:
        s = back_out(seg(t, 22.1, 22.3))
        for k in range(5):
            a = -math.pi / 2 + (k - 2) * 0.5
            star(c, 2200 + math.cos(a) * 260 * s, FY - 200 + math.sin(a) * 260 * s, 34 * s, t * 3, GOLD)
    if 30.3 <= t < 31.6:
        s = back_out(seg(t, 30.3, 30.5))
        c.save(); c.translate(FX0 + 150, FY - 680); c.rotate(-0.12); c.scale(S(s * 1.1), S(s * 1.1))
        text(c, "BONK!", 0, 0, 150, hexc("#FF6B6B"), olw=14); c.restore()
        for k in range(4):
            a = t * 5 + k * math.pi / 2
            star(c, FX0 + 120 + math.cos(a) * 170, FY - 470 + math.sin(a) * 40, 28, a, GOLD)
    # ticking clock icon during the race
    if 23.6 <= t < 29.5:
        cx, cy, Z = camera(t)
        c.save(); c.translate(cx + 380 / Z, cy - 760 / Z); c.scale(1 / Z, 1 / Z)
        ellipse(c, 0, 0, 80, 80, (1, 1, 1), lw=8)
        a = t * 2 * math.pi
        c.set_source_rgb(*INK); c.set_line_width(8); c.move_to(0, 0); c.line_to(55 * math.sin(a), -55 * math.cos(a)); c.stroke()
        c.restore()


def inside(c, t):
    """Dark fridge. Crumb wears the crown. Three knocks."""
    z = ease(seg(t, 36.7, 37.6))
    cx, cy, Z = lerp(560, 430, z), lerp(1080, 1280, z), lerp(1.25, 2.05, z)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    random.seed(int(t * 30))
    for t0 in (35.1, 35.7, 36.3):
        if t0 <= t < t0 + 0.22:
            k = 1 - seg(t, t0, t0 + 0.22)
            c.translate(random.uniform(-12, 12) * k, random.uniform(-6, 6) * k)
    fridge_bg(c, 0.0)
    # the Duck: top shelf, right at the front edge. Its one motion: it turns toward the knocking.
    duck(c, 640, TOP + 26, turn=lerp(1.0, 0.0, ease(seg(t, 36.4, 37.1))))
    knocks = sum(1 for t0 in (35.1, 35.7, 36.3) if t >= t0)
    if t < 35.1:
        mood, look, arm = "sheepish", (0, -1), "wave"   # admiring himself in the crown
        bob = abs(math.sin(t * 6)) * 14
    else:
        mood, look, arm = "scared", (1, 0) if knocks < 3 else (0, 0), "down"
        bob = 0
    crumb(c, 430, FLOOR - bob, mood, look=look, arm=arm, crown_on=True, shake=(2 + 2 * knocks) if t >= 35.1 else 0)
    # knock rings on the right edge (the door)
    for t0 in (35.1, 35.7, 36.3):
        if t0 <= t < t0 + 0.45:
            p = seg(t, t0, t0 + 0.45)
            c.save(); c.translate(860, 1180); c.rotate(0.1)
            s = back_out(min(1, p * 2.5))
            c.scale(S(s), S(s))
            text(c, "knock", 0, 0, 70, hexc("#FFD8A8"), olw=8)
            c.restore()
    dark_overlay(c, 0.0)


def frame(c, t):
    if t < 2.0:
        title_card(c, t, 3, "The Outside")
        if t > 1.7:
            iris(c, W / 2, H / 2, lerp(1200, 0, ease(seg(t, 1.7, 2.0))))
        return
    if t >= END_T:
        end_card(c, t, END_T); return
    if t < 34.0:
        c.save(); kitchen(c, t); c.restore()
        if t < 2.4:
            iris(c, W / 2, H / 2, lerp(0, 1400, ease(seg(t, 2.0, 2.4))))
        if t >= 33.6:
            iris(c, W / 2, H / 2 + 300, lerp(1000, 0, ease(seg(t, 33.6, 34.0))))
    else:
        c.save(); inside(c, t); c.restore()
        if t < 34.4:
            iris(c, W / 2, H * 0.62, lerp(0, 1400, ease(seg(t, 34.0, 34.4))))
        if t >= END_T - 0.35:
            iris(c, W / 2, H * 0.55, lerp(900, 0, ease(seg(t, END_T - 0.35, END_T))))


def main(out, preview=None):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    if preview is not None:
        c = cairo.Context(surf); frame(c, preview); surf.write_to_png(out); return
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                             "-crf", "20", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        c = cairo.Context(surf); c.set_source_rgb(0, 0, 0); c.paint()
        frame(c, i / FPS); surf.flush(); proc.stdin.write(bytes(surf.get_data()))
    proc.stdin.close(); proc.wait()


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else None)
