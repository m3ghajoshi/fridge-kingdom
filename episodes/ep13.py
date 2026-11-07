"""FRIDGE KINGDOM — Episode 13: "Knock From Above". 40.0s, 1080x1920 @ 30fps.

Variant A (title card first): 2s "FRIDGE KINGDOM" title card, then the story.

On the frosty top shelf, crownless Dill points his toothpick sword at the ceiling vent and declares war
(thought bubble: sword vs. snowflake). Peep, perched on Crumb's head, copies his salute. The tapping
answers... faster and faster. Dill whistles up the Jar pickles: they leap out of the jar one by one and
stack into a pickle pyramid under the vent; Dill climbs to the top and pokes the grille (TINK). Silence.
Peep copies him, flies up and lands on Dill's head. Too heavy: the pyramid wobbles and CRASHES. Dill lands
on Crumb, Peep lands on Dill, a pickle lands in the jar. Grandma Gherkin (still wearing Dill's crown)
sighs, hobbles over, springs straight up and jams her cane into the grille, dangling, cool as anything.
tok tok tok. ...tik tik tik. She raps a long pattern; the vent raps a pattern back; she nods solemnly.
She floats down on her shawl. Dill marches up to declare war again: BONK. Grandma "explains" with a
thought bubble: the freezer is a whole icy kingdom with a crowned shadow king. Everyone shivers.
Frost creeps down the back wall in the shape of a giant Hand... it becomes the Duck (which turns its head
to the camera)... then a giant snowflake. Push in on the vent: one icy-blue eye opens behind the slats,
and blinks.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crown, dark_overlay, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp,
                 back_out, bubble, INK, GOLD, TOP, W, H, FPS, S)
from ep2 import end_card
from ep6 import grandma, fridge6, lid_piece, pickle_kid, PICKLE_STYLES, JAR_X
from ep8 import shell_half
from ep9 import fat_peep, crumb_bitten, GRAN_HEAD
from ep10 import ceiling_vent, frost, VENT_X
from ep12 import vent_glow, squash_at, word, hop
from animate import heart

DUR = 40.0
END_T = 38.5
DIM = 0.18
FAT = 1.5
GSC = 1.35          # Grandma scale (readability)
PS = 1.2            # Jar pickle scale (readability)
EGG_X = 900
ICE = hexc("#D0EBFF")
ICE_B = hexc("#74C0FC")

# ---------------- timing ----------------
T_START = 2.0
T_BUB = 2.5          # war bubble
T_SALUTE = 3.4       # Peep copies
T_FAST = 4.6         # tapping speeds up
T_WHISTLE = 6.4      # Dill whistles up the pickles
T_STEP = 6.8         # Dill steps aside
LEAP_T = [7.0, 7.4, 7.8, 8.3, 8.7]
LEAP_D = 0.5
CLIMB_T = [9.4, 9.8, 10.2]
T_POKE = 10.65       # TINK
T_PEEP_UP = 11.3
T_PEEP_ON = 11.85
T_WOB = 11.9
T_FALL = 12.6
T_CRASH = 13.15
T_ROLL = 13.7
T_SIGH = 13.9
T_HOBBLE = 14.3
T_CROUCH = 15.2
T_SPRING = 15.5
T_HOOK = 16.05
TOKS = (17.0, 17.4, 17.8)
TIKS1 = (18.6, 18.9, 19.2)
TOKS2 = (19.8, 20.0, 20.4, 20.9, 21.3, 21.5)
TIKS2 = (22.0, 22.2, 22.6, 22.8, 23.3, 23.5)
T_NOD = 23.9
T_UNHOOK = 24.6
T_LAND = 26.0
T_MARCH = 26.1
T_BONK = 27.0
T_EXPLAIN = 27.7
T_SHIVER = 30.2
T_FROST = 31.0       # hand-shaped frost grows
T_DUCKF = 32.5       # turns into the Duck
T_DTURN = 33.0
T_FLAKE = 33.7       # turns into a snowflake
T_PUSH = 35.0        # push in on the vent
T_EYE = 36.1
T_BLINK = 37.0
T_STING = 36.3
DUNS = (37.55, 37.85, 38.15)

# ---------------- layout ----------------
DX0 = 560            # Dill under the vent
DX1 = 720            # Dill steps aside
CRX = 820            # Crumb (Peep perched on his head)
GRX = 330            # Grandma's spot
GR_LAND = 660
PYR = [(470, 0), (560, 0), (650, 0), (515, 1), (605, 1)]   # (x, row)
PYR_K = [4, 2, 0, 1, 3]                                    # which pickle in each slot
DILL_TOP_X = 560
LAND = {4: (380, 1.45), 2: (300 + 340, -1.5), 0: (1000, 1.5), 1: (250, -1.45), 3: (JAR_X, 0.0)}   # k -> (x, rot)


def ph(k):
    """Pickle height (feet to top of head) at scale PS."""
    return (14 + 2 * PICKLE_STYLES[k]["ry"]) * PS


def slot_y(i):
    x, row = PYR[i]
    if row == 0:
        return TOP
    # sits on the two below
    below = [j for j in range(3) if abs(PYR[j][0] - x) < 60]
    return TOP - min(ph(PYR_K[j]) for j in below) + 12


DILL_TOP_Y = min(slot_y(i) - ph(PYR_K[i]) for i in (3, 4)) + 12


# ---------------- helpers ----------------
def gran_offset(cane="up"):
    """Offset from Grandma's feet to the tip of her raised cane (with her hunch and GSC applied)."""
    cy = -66
    px, py = -40, cy - 175
    py2 = py + 10
    a = -0.22
    x2 = px * math.cos(a) - py2 * math.sin(a)
    y2 = px * math.sin(a) + py2 * math.cos(a) - 10
    return x2 * GSC, y2 * GSC


HOOK = (VENT_X - 70, 96)    # where the cane tip jams into the grille


def bubble_r(c, x, y, s, draw_icon):
    """Thought bubble with its tail on the lower right (for a speaker to the right)."""
    if s <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(S(s), S(s))
    ellipse(c, 0, 0, 120, 92, (1, 1, 1), lw=6)
    c.move_to(30, 80); c.line_to(70, 140); c.line_to(-10, 88); c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    ellipse(c, 20, 86, 30, 8, (1, 1, 1), stroke=False)
    draw_icon(c)
    c.restore()


def flash_words(c, t, items, size, col):
    for (s, x, y, t0, rot) in items:
        word(c, t, s, x, y, size, col, t0, t0 + 0.45, rot)


# ---------------- new props ----------------
def war_icon(c):
    """Thought-bubble icon: Dill's sword striking a snowflake with eyes."""
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    # snowflake
    c.save(); c.translate(30, -6)
    c.set_source_rgb(*ICE_B); c.set_line_width(9)
    for j in range(6):
        a = j * math.pi / 3
        c.move_to(0, 0); c.line_to(52 * math.cos(a), 52 * math.sin(a))
        c.move_to(30 * math.cos(a), 30 * math.sin(a)); c.line_to(42 * math.cos(a + 0.4), 42 * math.sin(a + 0.4))
    c.stroke()
    ellipse(c, -9, -4, 7, 8, (1, 1, 1), lw=3); ellipse(c, 9, -4, 7, 8, (1, 1, 1), lw=3)
    ellipse(c, -8, -2, 3, 3, INK, stroke=False); ellipse(c, 10, -2, 3, 3, INK, stroke=False)
    c.restore()
    # sword
    c.set_source_rgb(*INK); c.set_line_width(14); c.move_to(-80, 60); c.line_to(0, -40); c.stroke()
    c.set_source_rgb(*hexc("#E9C98B")); c.set_line_width(8); c.move_to(-80, 60); c.line_to(0, -40); c.stroke()
    c.set_source_rgb(*hexc("#FF4D6D")); c.move_to(-50, 22); c.line_to(-30, 50); c.line_to(-22, 10); c.close_path(); c.fill()
    # impact burst
    for j in range(6):
        a = j * math.pi / 3 + 0.3
        c.move_to(4 + 20 * math.cos(a), -44 + 20 * math.sin(a)); c.line_to(4 + 34 * math.cos(a), -44 + 34 * math.sin(a))
    c.set_source_rgb(*GOLD); c.set_line_width(5); c.stroke()


def kingdom_icon(c):
    """Grandma's picture: the freezer is a whole icy kingdom with a crowned shadow king."""
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    # fridge outline with the freezer on top
    rrect(c, -64, -10, 128, 80, 8); c.set_source_rgb(*hexc("#E9ECEF")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    rrect(c, -64, -72, 128, 62, 8); c.set_source_rgb(*hexc("#A5D8FF")); c.fill_preserve()
    c.set_source_rgb(*INK); c.stroke()
    # tiny us, down in the fridge
    for i, (x, col) in enumerate([(-30, hexc("#7BC043")), (-8, hexc("#F6D9A3")), (14, hexc("#FFF3A6")), (34, hexc("#558B2F"))]):
        ellipse(c, x, 50, 7, 11, col, lw=2)
    # ice castle rising out of the freezer
    for x, hgt in [(-46, 52), (-22, 74), (0, 96), (22, 74), (46, 52)]:
        c.move_to(x - 11, -40); c.line_to(x - 11, -40 - hgt + 16); c.line_to(x, -40 - hgt); c.line_to(x + 11, -40 - hgt + 16)
        c.line_to(x + 11, -40); c.close_path()
        c.set_source_rgb(*hexc("#E7F5FF")); c.fill_preserve(); c.set_source_rgb(*hexc("#1971C2")); c.set_line_width(3.5); c.stroke()
    # crowned shadow king in the gate
    ellipse(c, 0, -52, 14, 20, hexc("#1C2541"), lw=3)
    c.move_to(-13, -68); c.line_to(-15, -84); c.line_to(-6, -74); c.line_to(0, -90); c.line_to(6, -74); c.line_to(15, -84)
    c.line_to(13, -68); c.close_path(); c.set_source_rgb(*ICE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.5); c.stroke()
    ellipse(c, -5, -56, 3, 2.4, hexc("#9AF0FF"), stroke=False); ellipse(c, 5, -56, 3, 2.4, hexc("#9AF0FF"), stroke=False)
    # snowflakes
    for sx, sy in [(-90, -60), (88, -30), (-84, 30), (92, 50)]:
        c.set_source_rgb(*ICE_B); c.set_line_width(3)
        for j in range(3):
            a = j * math.pi / 3
            c.move_to(sx - 9 * math.cos(a), sy - 9 * math.sin(a)); c.line_to(sx + 9 * math.cos(a), sy + 9 * math.sin(a))
        c.stroke()


def frost_shape(c, shapes, alpha, details=None):
    """Frosty silhouette on the back wall: union of filled shapes with a glowing icy outline."""
    if alpha <= 0.01:
        return
    c.push_group()
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, col in [(40, ICE_B), (22, (1, 1, 1))]:
        for sh in shapes:
            sh(c); c.set_source_rgb(*col); c.set_line_width(lw); c.stroke()
    for sh in shapes:
        sh(c); c.set_source_rgb(*hexc("#DDF1FF")); c.fill()
    if details:
        details(c)
    c.pop_group_to_source(); c.paint_with_alpha(alpha * 0.92)


FX, FY = 510, 330     # frost figures' center on the back wall


def _ell(x, y, rx, ry):
    def f(c):
        c.new_path(); c.save(); c.translate(x, y); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    return f


def _cap(x0, y0, x1, y1, r):
    def f(c):
        c.new_path()
        a = math.atan2(y1 - y0, x1 - x0)
        c.arc(x1, y1, r, a - math.pi / 2, a + math.pi / 2)
        c.arc(x0, y0, r, a + math.pi / 2, a + 3 * math.pi / 2)
        c.close_path()
    return f


def _poly(pts):
    def f(c):
        c.new_path(); c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        c.close_path()
    return f


def hand_shapes():
    """A giant Hand reaching down from the vent: palm, four fingers, thumb."""
    palm = _ell(FX, FY - 40, 120, 110)
    cuff = _poly([(FX - 110, FY - 250), (FX + 110, FY - 250), (FX + 105, FY - 110), (FX - 105, FY - 110)])
    fingers = [_cap(FX - 92, FY + 10, FX - 118, FY + 150, 23), _cap(FX - 34, FY + 40, FX - 44, FY + 215, 24),
               _cap(FX + 28, FY + 40, FX + 34, FY + 210, 24), _cap(FX + 86, FY + 10, FX + 112, FY + 160, 22)]
    thumb = _cap(FX + 100, FY - 50, FX + 190, FY + 40, 30)
    return [cuff, palm, thumb] + fingers


def duck_shapes(turn):
    hx = lerp(FX + 80, FX + 40, turn)
    shapes = [_ell(FX - 10, FY + 70, 150, 95), _poly([(FX - 140, FY + 40), (FX - 215, FY - 10), (FX - 160, FY + 100)]),
              _ell(hx, FY - 70, 70, 66)]
    if turn < 0.5:
        shapes.append(_poly([(hx + 60, FY - 80), (hx + 125, FY - 60), (hx + 60, FY - 40)]))
    else:
        shapes.append(_ell(hx, FY - 34, 34, 16))
    shapes.append(_poly([(hx - 44, FY - 120), (hx - 46, FY - 168), (hx - 24, FY - 146), (hx - 6, FY - 182), (hx + 10, FY - 150),
                         (hx + 30, FY - 176), (hx + 38, FY - 140), (hx + 48, FY - 122)]))

    def details(c):
        col = hexc("#1971C2")
        if turn < 0.5:
            ellipse(c, hx + 26, FY - 86, 11, 11, col, stroke=False)
        else:
            for ex in (-24, 24):
                ellipse(c, hx + ex, FY - 84, 11, 11, col, stroke=False)
        c.set_source_rgb(*col); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(FX - 90, FY + 50); c.curve_to(FX - 40, FY + 10, FX + 40, FY + 40, FX + 20, FY + 100); c.stroke()
    return shapes, details


def flake_draw(c, rot, r, alpha):
    if alpha <= 0.01:
        return
    c.push_group()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, col in [(38, ICE_B), (18, (1, 1, 1))]:
        c.new_path()
        for j in range(6):
            a = rot + j * math.pi / 3
            ca, sa = math.cos(a), math.sin(a)
            c.move_to(FX, FY); c.line_to(FX + r * ca, FY + r * sa)
            for d, bl in [(0.45, 0.3), (0.72, 0.22)]:
                bx, by = FX + r * d * ca, FY + r * d * sa
                for s in (-1, 1):
                    c.move_to(bx, by); c.line_to(bx + r * bl * math.cos(a + s * 0.7), by + r * bl * math.sin(a + s * 0.7))
        c.set_source_rgb(*col); c.set_line_width(lw); c.stroke()
    ellipse(c, FX, FY, r * 0.18, r * 0.18, hexc("#DDF1FF"), lw=10)
    c.pop_group_to_source(); c.paint_with_alpha(alpha * 0.92)


def frost_figures(c, t):
    if t < T_FROST or t >= T_PUSH + 0.8:
        return
    fade_all = 1 - seg(t, T_PUSH, T_PUSH + 0.8)
    if t < T_DUCKF + 0.3:   # hand: frost creeps down from the vent
        a = (1 - seg(t, T_DUCKF - 0.1, T_DUCKF + 0.3)) * fade_all
        reveal = ease(seg(t, T_FROST, T_FROST + 1.1))
        c.save(); c.rectangle(-400, -400, W + 800, (FY - 280 + 560 * reveal) + 400); c.clip()
        frost_shape(c, hand_shapes(), a)
        c.restore()
    if T_DUCKF - 0.1 <= t < T_FLAKE + 0.3:
        a = seg(t, T_DUCKF - 0.1, T_DUCKF + 0.3) * (1 - seg(t, T_FLAKE - 0.1, T_FLAKE + 0.3)) * fade_all
        shapes, det = duck_shapes(ease(seg(t, T_DTURN, T_DTURN + 0.3)))
        frost_shape(c, shapes, a, det)
    if t >= T_FLAKE - 0.1:
        a = seg(t, T_FLAKE - 0.1, T_FLAKE + 0.3) * fade_all
        k = back_out(seg(t, T_FLAKE - 0.1, T_FLAKE + 0.5))
        flake_draw(c, 0.15 * (t - T_FLAKE), 240 * max(0.05, k), a)
    for t0 in (T_DUCKF, T_FLAKE):   # transformation sparkles
        if t0 - 0.2 <= t < t0 + 0.5:
            q = seg(t, t0 - 0.2, t0 + 0.5)
            for j in range(10):
                ang = j * 0.63 + t0
                star(c, FX + math.cos(ang) * 220 * q, FY + math.sin(ang) * 170 * q, 20 * math.sin(math.pi * q), t * 4, (1, 1, 1))


def ceiling(c, light):
    """The fridge's ceiling panel above the back wall."""
    c.rectangle(-400, -800, W + 800, 812)
    c.set_source_rgb(*[v * lerp(0.6, 1.0, light) for v in hexc("#8FA6C4")]); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.rectangle(-400, 0, W + 800, 6); c.set_source_rgba(1, 1, 1, 0.35); c.fill()


def vent_eye(c, t):
    """Drawn after the dark overlay so it glows: one icy-blue eye behind the vent grille; opens, blinks."""
    if t < T_EYE:
        return
    op = ease_out(seg(t, T_EYE, T_EYE + 0.5))
    if T_BLINK <= t < T_BLINK + 0.3:
        op *= abs(math.cos(math.pi * seg(t, T_BLINK, T_BLINK + 0.3)))
    ex, ey = VENT_X, 30 + 48
    gl = ease_out(seg(t, T_EYE, T_EYE + 0.5))
    g = cairo.RadialGradient(ex, ey, 10, ex, ey, 300)
    g.add_color_stop_rgba(0, 0.55, 0.85, 1, 0.5 * gl); g.add_color_stop_rgba(1, 0.55, 0.85, 1, 0)
    c.rectangle(ex - 320, ey - 300, 640, 600); c.set_source(g); c.fill()
    # grille opening, dark inside
    rrect(c, VENT_X - 150, 32, 300, 92, 10); c.set_source_rgb(0.02, 0.04, 0.09); c.fill()
    h = 52 * op
    if h > 0.5:
        c.save(); rrect(c, VENT_X - 150, 32, 300, 92, 10); c.clip()
        c.move_to(ex - 135, ey); c.curve_to(ex - 60, ey - h * 1.35, ex + 60, ey - h * 1.35, ex + 135, ey)
        c.curve_to(ex + 60, ey + h * 1.35, ex - 60, ey + h * 1.35, ex - 135, ey); c.close_path()
        c.set_source_rgb(*hexc("#E7F5FF")); c.fill_preserve()
        c.save(); c.clip()
        ellipse(c, ex + 8, ey, 48, 48, hexc("#4DABF7"), stroke=False)
        ellipse(c, ex + 8, ey, 33, 33, hexc("#A5E8FF"), stroke=False)
        ellipse(c, ex + 8, ey, 9, 38, hexc("#0B1B33"), stroke=False)
        ellipse(c, ex - 8, ey - 16, 9, 9, (1, 1, 1), stroke=False)
        c.restore(); c.restore()
    # thin grille bars over it
    for k in range(4):
        c.rectangle(VENT_X - 150, 32 + 18 + k * 20, 300, 5); c.set_source_rgb(*hexc("#5C6670")); c.fill()
    rrect(c, VENT_X - 170, 20, 340, 110, 18); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    rrect(c, VENT_X - 150, 32, 300, 92, 10); c.set_source_rgb(*hexc("#5C6670")); c.set_line_width(6); c.stroke()


# ---------------- title card (variant A) ----------------
def title_card(c, t):
    g = cairo.RadialGradient(W / 2, 820, 50, W / 2, 820, 1300)
    g.add_color_stop_rgb(0, *hexc("#E7F5FF")); g.add_color_stop_rgb(0.35, *hexc("#74C0FC")); g.add_color_stop_rgb(1, *hexc("#1C2541"))
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    for i, wd in enumerate(["FRIDGE", "KINGDOM"]):
        p = back_out(seg(t, 0.1 + i * 0.25, 0.55 + i * 0.25))
        c.save(); c.translate(W / 2, 640 + i * 170 + 8 * math.sin(t * 6 + i)); c.rotate(0.04 * (1 if i else -1))
        c.scale(S(p), S(p)); text(c, wd, 0, 0, 170, GOLD if i else (1, 1, 1), olw=22); c.restore()
    crown(c, W / 2 + 190, 500, 1.6 * back_out(seg(t, 0.6, 1.0)), 0.25)
    q = ease_out(seg(t, 0.9, 1.3))
    if q > 0:
        c.save(); c.translate(W / 2, 1000 + (1 - q) * 50)
        text(c, "Episode 13:", 0, 0, 60, (1, 1, 1), olw=10)
        text(c, "Knock From Above", 0, 90, 80, GOLD, olw=12)
        c.restore()
    # three knocks from the top of the card
    for i, t0 in enumerate((0.5, 0.9, 1.3)):
        if t >= t0:
            k = back_out(seg(t, t0, t0 + 0.15))
            c.save(); c.translate(300 + 240 * i, 230 + 20 * (i % 2)); c.rotate((-0.1, 0.05, 0.12)[i]); c.scale(S(k), S(k))
            text(c, "tik", 0, 0, 90, ICE, olw=12); c.restore()
    dill(c, 300, 1700 - abs(math.sin(t * 6)) * 30, "angry", crown_on=False, arm="up", shake=3, look=(0.3, -1))
    c.save(); c.translate(720, 1700); c.scale(GSC, GSC); c.translate(-720, -1700)
    grandma(c, 720, 1700, look=(0, -1), cane="up", mood="stern")
    c.restore()
    crown(c, 720 + GRAN_HEAD[0], 1700 + GRAN_HEAD[1], 0.72, -0.2)
    fat_peep(c, 900, 1700 - abs(math.sin(t * 7 + 1)) * 26, FAT, mood="shock", face=0, look=(0, -1), wings="flap", flap_t=t)


# ---------------- character states ----------------
def tik_times():
    """All the tiks from the vent: three slow ones, then faster and faster."""
    out = [2.3, 3.0, 3.7]
    tt, gap = T_FAST, 0.32
    while tt < T_WHISTLE - 0.1:
        out.append(tt); tt += gap; gap = max(0.09, gap * 0.82)
    return out


TIK_RUN = tik_times()


def tik_jolt(t):
    for tt in TIK_RUN:
        if tt <= t < tt + 0.12:
            return 1
    return 0


def pickle_state(k, t):
    """(x, y, kw) or None (still inside the jar)."""
    i = PYR_K.index(k)
    sx, sy = PYR[i][0], slot_y(i)
    t0 = LEAP_T[i]
    if t < t0:
        return None
    if t < t0 + LEAP_D:
        p = seg(t, t0, t0 + LEAP_D)
        x, y = hop((JAR_X, TOP - 300), (sx, sy), p, 260)
        return x, y, dict(look=(1, -1), rot=2 * math.pi * p, arms="up", mood="calm")
    if t < T_FALL:
        strain = 1.5 if t > T_PEEP_ON else 0
        mood = "shock" if T_POKE <= t < T_POKE + 0.5 or t > T_WOB else "calm"
        squish = 1.0
        if PYR[i][1] == 0 and any(ct <= t < ct + 0.2 for ct in CLIMB_T):
            squish = 0.95
        return sx, sy, dict(look=(0, -1), arms="up", mood=mood, shake=strain, sq=squish)
    lx, lr = LAND[k]
    if t < T_CRASH:
        p = seg(t, T_FALL + 0.05 * i, T_CRASH)
        x, y = hop((sx, sy), (lx, TOP if k != 3 else TOP - 120), p, 220 + 40 * i)
        return x, y, dict(look=(0, 0), arms="up", mood="shock", rot=lerp(0, lr + (2 * math.pi if k in (0, 4) else 0), p))
    if k == 3:     # landed in the jar; peeks out later
        if t < T_EXPLAIN:
            return None
        q = back_out(seg(t, T_EXPLAIN, T_EXPLAIN + 0.4))
        return JAR_X, TOP - 170 - 120 * q, dict(look=(1, -1), mood="calm", inside=True)
    if t < 16.4:   # lying dizzy
        return lx, TOP, dict(look=(0, 0), mood="closed", rot=lr)
    if t < 16.8:
        p = ease(seg(t, 16.4, 16.8))
        return lx, TOP, dict(look=(0, -1), mood="calm", rot=lerp(lr, 0, p))
    look = (0.4, -1) if t < T_UNHOOK else (1 if lx < GR_LAND else -1, -0.3)
    mood = "shock" if (T_FROST <= t < T_FROST + 1.4) or t >= T_SHIVER - 0.1 and t < T_SHIVER + 0.8 else "calm"
    sh = 2.5 if T_SHIVER <= t < T_SHIVER + 1.2 or T_FLAKE <= t < T_PUSH else 0
    return lx, TOP, dict(look=look, mood=mood, shake=sh)


def pyramid_wobble(t):
    if t < T_WOB:
        return 0.0
    if t < T_FALL:
        a = 0.02 + 0.12 * seg(t, T_WOB, T_FALL)
        return a * math.sin((t - T_WOB) * 14)
    return 0.0


def dill_state(t):
    """(x, y, kw)."""
    if t < T_STEP:
        mood = "angry"
        if T_FAST <= t < T_FAST + 0.9:
            mood = "shocked"
        arm = "up" if t < T_WHISTLE else "point_l"
        sh = 3 if t < T_FAST else (1.5 + 3 * tik_jolt(t))
        look = (0.4, -1) if t < T_WHISTLE else (-1, -0.3)
        return DX0, TOP, dict(mood=mood, arm=arm, shake=sh, look=look)
    if t < CLIMB_T[0]:
        p = ease(seg(t, T_STEP, T_STEP + 0.4))
        return lerp(DX0, DX1, p), TOP - 30 * math.sin(math.pi * p), dict(mood="smug" if t < 8.9 else "proud", look=(-1, -0.4), arm="point_l" if t < 8.9 else "down")
    # climbing
    steps = [(DX1, TOP), (590, slot_y(2) - ph(PYR_K[2]) + 10), (560, slot_y(4) - ph(PYR_K[4]) + 10), (DILL_TOP_X, DILL_TOP_Y)]
    for j, ct in enumerate(CLIMB_T):
        if t < ct + 0.35:
            if t < ct:
                return steps[j][0], steps[j][1], dict(mood="proud", look=(0, -1), arm="reach")
            x, y = hop(steps[j], steps[j + 1], seg(t, ct, ct + 0.35), 90)
            return x, y, dict(mood="proud", look=(0, -1), arm="reach")
    if t < T_FALL:
        mood = "proud"
        arm = "up"
        if T_POKE - 0.15 <= t < T_POKE + 0.5:
            mood = "angry"
        if T_POKE + 0.5 <= t < T_PEEP_UP:
            mood = "smug"
        if t >= T_PEEP_ON:
            mood = "shocked"
        sq = lerp(0.85, 1, ease(seg(t, T_PEEP_ON, T_PEEP_ON + 0.3))) if t >= T_PEEP_ON else 1.0
        return DILL_TOP_X, DILL_TOP_Y, dict(mood=mood, arm=arm, look=(0, -1) if t < T_PEEP_UP else (0, -1), sq=sq,
                                             rot=-0.12 if T_POKE - 0.2 <= t < T_POKE + 0.4 else 0)
    if t < T_CRASH:
        p = seg(t, T_FALL, T_CRASH)
        x, y = hop((DILL_TOP_X, DILL_TOP_Y), (CRX, TOP - crumb_top(T_CRASH + 0.01)), p, 150)
        return x, y, dict(mood="shocked", arm="reach", rot=1.2 * p, look=(0, 1))
    if t < T_ROLL:
        return CRX, TOP - crumb_top(t), dict(mood="frozen", rot=0.15, sq=0.9, look=(0.4 * math.sin(t * 8), 0.4 * math.cos(t * 8)))
    if t < T_ROLL + 0.5:
        p = ease(seg(t, T_ROLL, T_ROLL + 0.5))
        x, y = hop((CRX, TOP - crumb_top(t)), (620, TOP), p, 70)
        return x, y, dict(mood="frozen", rot=lerp(0.15, -0.2, p))
    if t < T_HOOK:
        return lerp(620, 740, ease(seg(t, T_HOBBLE, T_HOBBLE + 0.5))), TOP, dict(mood="frozen" if t < T_HOBBLE else "shocked", look=(-1, -0.5))
    if t < T_UNHOOK:
        # watching the conversation
        lk = (-0.4, -1)
        mood = "shocked" if (T_HOOK <= t < T_HOOK + 0.8) else "frozen"
        if TIKS1[0] <= t < TIKS1[0] + 0.6 or TIKS2[0] <= t < TIKS2[0] + 0.5:
            mood = "shocked"
        if T_NOD <= t:
            mood = "smug"
        return 740, TOP, dict(mood=mood, look=lk)
    if t < T_MARCH:
        return lerp(740, 500, ease(seg(t, T_UNHOOK + 0.2, T_UNHOOK + 0.9))), TOP, dict(mood="frozen", look=(1, -0.6))
    if t < T_BONK:   # marches up to Grandma, sword up, war again
        p = ease(seg(t, T_MARCH, T_MARCH + 0.4))
        x = lerp(500, 520, p)
        return x, TOP - abs(math.sin((t - T_MARCH) * 12)) * 14, dict(mood="angry", arm="up", look=(0.5, -1), shake=2)
    if t < T_EXPLAIN:
        q = seg(t, T_BONK, T_BONK + 0.08)
        sq = lerp(1, 0.62, ease_out(q))
        if t > T_BONK + 0.5:
            sq = lerp(0.62, 1.0, back_out(seg(t, T_BONK + 0.5, T_BONK + 0.75)))
        return 520, TOP, dict(mood="frozen", sq=sq, look=(0.4 * math.sin(t * 8), 0.4 * math.cos(t * 8)))
    mood, look, sh = "shocked", (1, -0.6), 0
    if t >= T_SHIVER:
        sh = 3
    if T_FROST <= t:
        look = (0.3, -1)
    if T_FLAKE <= t:
        sh = 2.5
    return 520, TOP, dict(mood=mood, look=look, shake=sh)


CRUMB_HITS = [(T_CRASH, 0.42, T_ROLL, 0.35)]


def crumb_sq(t):
    for t0, low, t1, rec in CRUMB_HITS:
        if t0 <= t < t1 + rec:
            down = lerp(1, low, ease_out(seg(t, t0, t0 + 0.08)))
            if t >= t1:
                return lerp(low, 1.0, back_out(seg(t, t1, t1 + rec)))
            return down
    return 1.0


def crumb_top(t):
    return 300 * crumb_sq(t) - 6


def crumb_state(t):
    sq = crumb_sq(t)
    if t < T_FAST:
        return dict(mood="worried", look=(-1, -0.4)), sq
    if t < T_WHISTLE:
        return dict(mood="scared", look=(-0.5, -1), shake=1 + 2 * tik_jolt(t)), sq
    if t < T_FALL:
        return dict(mood="worried", look=(-1, -0.6) if t < T_PEEP_UP else (-1, -1)), sq
    if t < T_CRASH:
        return dict(mood="scared", look=(-1, -1), arm="wave"), sq
    if t < T_ROLL + 0.4:
        return dict(mood="dizzy"), sq
    if t < T_UNHOOK:
        return dict(mood="worried", look=(-1, -1), shake=1.5 if any(tt <= t < tt + 0.15 for tt in TIKS1 + TIKS2) else 0), sq
    if t < T_FROST:
        return dict(mood="worried" if t < T_EXPLAIN else "sheepish", look=(-1, -0.6), shake=2 if t >= T_SHIVER else 0), sq
    return dict(mood="scared", look=(-1, -1), shake=2 if t >= T_FLAKE else 0), sq


def peep_state(t):
    """(x, y, kw)."""
    perch = lambda tt: (CRX, TOP - crumb_top(tt) + 8)
    if t < T_PEEP_UP:
        x, y = perch(t)
        kw = dict(mood="happy", face=-0.3, look=(-1, -0.3))
        if T_SALUTE <= t < T_FAST:
            kw = dict(mood="proud", face=-0.3, look=(-1, -0.3), wings="salute")
        elif T_FAST <= t < T_WHISTLE:
            kw = dict(mood="shock", face=0, look=(-0.5, -1), shake=2 + 2 * tik_jolt(t))
        elif T_WHISTLE <= t:
            kw = dict(mood="happy" if t < 10.6 else "proud", face=-0.4, look=(-1, -1))
        return x, y, kw
    top = (DILL_TOP_X, DILL_TOP_Y - 296)
    if t < T_PEEP_ON:
        p = seg(t, T_PEEP_UP, T_PEEP_ON)
        x0, y0 = perch(T_PEEP_UP)
        x, y = hop((x0, y0), top, p, 160)
        return x, y, dict(mood="blink", face=-0.4, wings="flap", flap_t=t * 1.6)
    if t < T_FALL:
        w = pyramid_wobble(t)
        return top[0], top[1], dict(mood="proud", face=0, look=(0, 0), wings="salute", sq=lerp(0.8, 1, ease(seg(t, T_PEEP_ON, T_PEEP_ON + 0.25))))
    land = lambda tt: (CRX + 10, TOP - crumb_top(tt) - 300 + 40)
    if t < T_CRASH + 0.15:
        p = seg(t, T_FALL, T_CRASH + 0.15)
        x, y = hop(top, land(T_CRASH + 0.2), p, 120)
        return x, y, dict(mood="shock", face=0, wings="flap", flap_t=t * 1.6, rot=-2 * math.pi * p)
    if t < T_ROLL:
        x, y = land(t)
        return x, y, dict(mood="proud", face=-0.3, look=(-1, 0))
    if t < T_ROLL + 0.45:   # back onto Crumb's head
        p = seg(t, T_ROLL, T_ROLL + 0.45)
        x, y = hop(land(T_ROLL), perch(t), p, 60)
        return x, y, dict(mood="happy", face=-0.3)
    x, y = perch(t)
    look, mood, kw = (-1, -1), "happy", {}
    if T_HOOK <= t < T_UNHOOK:
        mood = "shock" if any(tt <= t < tt + 0.3 for tt in TIKS1 + TIKS2) else "happy"
        # Peep copies the knocking: bobs its head on each tok
        if any(tt <= t < tt + 0.12 for tt in TOKS + TOKS2):
            kw = dict(sq=0.88)
    if t >= T_EXPLAIN:
        mood, look = "happy", (-1, -0.8)
    if t >= T_SHIVER:
        mood = "shock"
    if T_FROST <= t:
        look = (-0.6, -1)
    sh = 2.5 if t >= T_SHIVER else 0
    return x, y, dict(mood=mood, face=-0.3, look=look, shake=sh, **kw)


def gran_state(t):
    """(x, y, kw, pend) — pend is the dangling angle around the cane tip (or None)."""
    ox, oy = gran_offset()
    hang_feet = (HOOK[0] - ox, HOOK[1] - oy)
    if t < T_SIGH:
        return GRX, TOP, dict(look=(1, -0.6), cane="down", mood="stern"), None
    if t < T_HOBBLE:
        return GRX, TOP, dict(look=(1, 0), cane="down", mood="closed"), None
    if t < T_CROUCH:
        p = seg(t, T_HOBBLE, T_CROUCH)
        x = lerp(GRX, hang_feet[0], ease(p))
        return x, TOP - abs(math.sin(p * math.pi * 6)) * 10, dict(look=(1, -0.3), cane="down", mood="stern", step=p * 6), None
    if t < T_SPRING:
        return hang_feet[0], TOP, dict(look=(0, -1), cane="up", mood="stern", sq=lerp(1, 0.75, seg(t, T_CROUCH, T_SPRING))), None
    if t < T_HOOK:
        p = ease_out(seg(t, T_SPRING, T_HOOK))
        return hang_feet[0], lerp(TOP, hang_feet[1], p), dict(look=(0, -1), cane="up", mood="stern"), None
    if t < T_UNHOOK:
        dt = t - T_HOOK
        pend = 0.25 * math.exp(-dt * 2.2) * math.sin(dt * 7)
        jolt = 0
        for tt in TOKS + TOKS2:
            if tt <= t < tt + 0.12:
                jolt = 10 * (1 - seg(t, tt, tt + 0.12))
        mood = "closed"
        look = (0, -1)
        if TIKS1[0] <= t < TOKS2[0] or TIKS2[0] <= t < T_NOD:
            mood = "stern"
        bow = 0.0
        if T_NOD <= t < T_NOD + 0.6:
            bow = -0.2 * math.sin(math.pi * seg(t, T_NOD, T_NOD + 0.6) * 2) ** 2
        return hang_feet[0], hang_feet[1] - jolt, dict(look=look, cane="up", mood=mood, bow=bow), pend
    if t < T_LAND:   # floats down on her shawl
        p = seg(t, T_UNHOOK, T_LAND)
        x = lerp(hang_feet[0], GR_LAND, ease(p)) + 20 * math.sin(p * 6)
        y = lerp(hang_feet[1] + 60, TOP, ease(p))
        return x, y, dict(look=(-1, -0.4), cane="down", mood="closed", chute=min(1, seg(t, T_UNHOOK, T_UNHOOK + 0.3))), None
    if t < T_BONK - 0.35:
        return GR_LAND, TOP, dict(look=(-1, -0.2), cane="down", mood="stern" if t < T_MARCH + 0.4 else "angry"), None
    if t < T_BONK + 0.4:   # springs up and BONKs
        q = seg(t, T_BONK - 0.35, T_BONK + 0.4)
        x = lerp(GR_LAND, 640, ease(seg(t, T_BONK - 0.35, T_BONK)))
        return x, TOP, dict(look=(-1, -0.4), cane="up", mood="angry", hop=70 * math.sin(math.pi * q)), None
    if t < T_EXPLAIN + 0.2:
        x = lerp(640, GR_LAND, ease(seg(t, T_BONK + 0.4, T_EXPLAIN)))
        return x, TOP, dict(look=(-1, 0), cane="down", mood="stern"), None
    mood = "stern"
    return GR_LAND, TOP, dict(look=(1, -0.6) if t < T_FROST else (-0.3, -1), cane="up" if t < T_SHIVER else "down", mood=mood,
                              shake=0), None


# ---------------- camera ----------------
KEYS = [(T_START, 600, 450, 1.7), (T_SALUTE - 0.3, 600, 450, 1.7), (T_SALUTE + 0.2, 660, 410, 1.45), (T_FAST, 660, 400, 1.45),
        (T_WHISTLE, 640, 400, 1.42), (T_WHISTLE + 0.6, 630, 390, 1.38), (CLIMB_T[0], 630, 390, 1.38),
        (T_POKE, 620, 330, 1.42), (T_PEEP_UP, 630, 340, 1.38), (T_FALL, 640, 390, 1.38), (T_CRASH + 0.3, 660, 430, 1.42),
        (T_SIGH, 620, 430, 1.45), (T_HOBBLE, 580, 430, 1.45), (T_CROUCH, 600, 420, 1.42), (T_HOOK, 620, 330, 1.42),
        (TOKS[0] - 0.3, 620, 320, 1.62), (TIKS1[-1] + 0.3, 620, 320, 1.62), (T_NOD, 630, 320, 1.6),
        (T_UNHOOK, 640, 380, 1.42), (T_LAND, 640, 420, 1.45), (T_BONK - 0.3, 600, 470, 1.7), (T_BONK + 0.5, 600, 470, 1.7),
        (T_EXPLAIN, 660, 380, 1.42), (T_SHIVER, 660, 390, 1.42), (T_FROST, 620, 420, 1.3), (T_PUSH, 620, 420, 1.3),
        (T_EYE - 0.1, VENT_X, 110, 3.0), (END_T, VENT_X, 95, 3.3)]


def keycam(keys, t):
    if t <= keys[0][0]:
        return keys[0][1:]
    for a, b in zip(keys, keys[1:]):
        if t < b[0]:
            p = ease(seg(t, a[0], b[0]))
            return tuple(lerp(a[i], b[i], p) for i in (1, 2, 3))
    return keys[-1][1:]


def camera(t):
    cx, cy, z = keycam(KEYS, t)
    shakes = [(T_POKE, 6), (T_CRASH, 16), (T_HOOK, 6), (T_BONK, 12), (T_LAND, 4)]
    for t0, s in shakes:
        if t0 <= t < t0 + 0.25:
            q = s * (1 - seg(t, t0, t0 + 0.25)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    if T_FAST <= t < T_WHISTLE and tik_jolt(t):
        cx += random.uniform(-3, 3); cy += random.uniform(-3, 3)
    for d in DUNS:
        if d <= t < d + 0.12:
            z += 0.12 * (1 - seg(t, d, d + 0.12))
    return cx, cy, z


# ---------------- scene ----------------
def draw_pickle(c, k, t):
    st = pickle_state(k, t)
    if st is None:
        return
    x, y, kw = st
    inside = kw.pop("inside", False)
    sq = kw.pop("sq", 1.0)
    sh = kw.pop("shake", 0)
    c.save()
    c.translate(x + sh * random.uniform(-1, 1), y); c.scale(PS, PS * sq); c.translate(-x, -y)
    pickle_kid(c, x, y, k, **kw)
    c.restore()


def draw_gran(c, t):
    x, y, kw, pend = gran_state(t)
    sq = kw.pop("sq", 1.0)
    kw.pop("shake", None)
    hopv = kw.get("hop", 0)
    c.save()
    if pend is not None:
        c.translate(*HOOK); c.rotate(pend); c.translate(-HOOK[0], -HOOK[1])
    c.translate(x, y); c.scale(GSC, GSC * sq); c.translate(-x, -y)
    grandma(c, x, y, **kw)
    c.restore()
    # Dill's crown on her bun (follows her)
    c.save()
    if pend is not None:
        c.translate(*HOOK); c.rotate(pend); c.translate(-HOOK[0], -HOOK[1])
    if kw.get("chute", 0) > 0.05:
        cx, cy = x + GRAN_HEAD[0] + 46 * GSC - 4, y + GRAN_HEAD[1] * sq
    else:
        cx, cy = x + GRAN_HEAD[0], y + GRAN_HEAD[1] * sq
    bowk = kw.get("bow", 0)
    crown(c, cx - 60 * bowk, cy - hopv * GSC + 30 * abs(bowk), 0.72, -0.2 + bowk)
    c.restore()


def draw_dill(c, t):
    x, y, kw = dill_state(t)
    dill(c, x, y, crown_on=False, **kw)


def draw_crumb(c, t):
    kw, sq = crumb_state(t)
    c.save(); squash_at(c, CRX, TOP, sq)
    crumb_bitten(c, CRX, TOP, 1.0, **kw)
    c.restore()


def draw_peep(c, t):
    x, y, kw = peep_state(t)
    fat_peep(c, x, y, FAT, **kw)


def scene(c, t):
    L = DIM
    n_in = sum(1 for tt in LEAP_T if t < tt)
    fridge6(c, L, n_in, lid=False)
    glow = sum(0.35 * max(0, math.sin(math.pi * seg(t, tt, tt + 0.3))) for tt in TIK_RUN + list(TIKS1) + list(TIKS2))
    frost(c, t, 1.0)
    ceiling(c, L)
    ceiling_vent(c, L)
    vent_glow(c, min(1, glow))
    frost_figures(c, t)
    lid_piece(c, 760, TOP - 25, 0.0)
    shell_half(c, EGG_X, TOP - 70, 0.0, top=False)
    ellipse(c, 300, TOP + 4, 70, 10, (0.75, 0.9, 1.0), lw=3)     # meltwater puddle (Ep 11)

    # pyramid layer (wobbles as one)
    w = pyramid_wobble(t)
    c.save(); c.translate(560, TOP); c.rotate(w); c.translate(-560, -TOP)
    on_stack = T_WHISTLE < t < T_FALL
    for i, k in enumerate(PYR_K):
        st = pickle_state(k, t)
        if st and on_stack and t >= LEAP_T[i] + LEAP_D:
            draw_pickle(c, k, t)
    if CLIMB_T[0] <= t < T_FALL:
        draw_dill(c, t)
    if T_PEEP_ON <= t < T_FALL:
        draw_peep(c, t)
    c.restore()
    # leaping / fallen pickles
    for i, k in enumerate(PYR_K):
        st = pickle_state(k, t)
        if st and not (on_stack and t >= LEAP_T[i] + LEAP_D):
            if k == 3 and t >= T_CRASH:
                continue
            draw_pickle(c, k, t)
    # sprout pickle peeking out of the jar (drawn behind the jar glass front)
    if t >= T_EXPLAIN:
        x, y, kw = pickle_state(3, t)
        kw.pop("inside", None)
        c.save(); c.rectangle(JAR_X - 120, -400, 240, TOP - 330 + 400 + 6); c.clip()
        c.translate(x, y); c.scale(PS, PS); c.translate(-x, -y)
        pickle_kid(c, x, y, 3, **kw)
        c.restore()
    if t >= T_CRASH and t < T_EXPLAIN:
        q = seg(t, T_CRASH, T_CRASH + 0.5)
        if q < 1:
            ellipse(c, JAR_X, TOP - 330, 70 * q, 16 * q, (0.75, 0.9, 1.0), lw=3)

    bonking = T_BONK - 0.4 <= t < T_EXPLAIN
    if not bonking:
        draw_gran(c, t)
    if not (CLIMB_T[0] <= t < T_FALL):
        draw_dill(c, t)
    if bonking:
        draw_gran(c, t)
    draw_crumb(c, t)
    if not (T_PEEP_ON <= t < T_FALL):
        draw_peep(c, t)

    # ---------------- effects ----------------
    # war bubble
    if T_BUB <= t < T_FAST:
        s = back_out(seg(t, T_BUB, T_BUB + 0.3))
        if t > T_FAST - 0.25:
            s = 1 - ease(seg(t, T_FAST - 0.25, T_FAST))
        bubble_r(c, DX0 - 150, TOP - 470, 1.15 * s, war_icon)
    if T_START <= t < T_BUB + 0.4:
        for j in range(3):
            q = ((t - T_START) * 2 + j / 3) % 1
            c.move_to(DX0 + 70 + 60 * j * 0.5, TOP - 300 - 40 * j); c.line_to(DX0 + 110 + 50 * j, TOP - 330 - 50 * j - 20 * q)
            c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(6); c.stroke()
    word(c, t, "?!", DX0 + 110, TOP - 420, 80, (1, 0.35, 0.35), T_FAST + 0.1, T_FAST + 1.0, 0.1)
    # whistle
    if T_WHISTLE <= t < T_WHISTLE + 0.5:
        for j in range(3):
            q = seg(t, T_WHISTLE + 0.1 * j, T_WHISTLE + 0.1 * j + 0.3)
            ellipse(c, DX0 - 80 - 60 * q, TOP - 250 - 30 * j, 8 * (1 - q) + 2, 8 * (1 - q) + 2, (1, 1, 1), stroke=False)
        word(c, t, "fweet!", DX0 - 170, TOP - 330, 46, (1, 1, 1), T_WHISTLE, T_WHISTLE + 0.6, -0.1)
    for i, t0 in enumerate(LEAP_T):
        word(c, t, "boing", PYR[i][0] + (60 if i % 2 else -60), slot_y(i) - 240, 36, (1, 1, 1), t0 + LEAP_D - 0.05, t0 + LEAP_D + 0.4, 0.12 * (-1) ** i)
    word(c, t, "TINK!", 760, 140, 60, (1, 1, 1), T_POKE, T_POKE + 0.6, 0.1)
    if T_POKE <= t < T_POKE + 0.5:
        star(c, 640, 120, 24 * math.sin(math.pi * seg(t, T_POKE, T_POKE + 0.5)), t * 6, (1, 1, 1))
    if T_POKE + 0.5 <= t < T_PEEP_UP:
        word(c, t, "...", 760, 200, 70, (1, 1, 1), T_POKE + 0.5, T_PEEP_UP)
    word(c, t, "creak", 380, DILL_TOP_Y - 30, 44, (1, 1, 1), T_WOB + 0.1, T_FALL, -0.12)
    word(c, t, "creeeak", 760, DILL_TOP_Y + 40, 44, (1, 1, 1), T_WOB + 0.35, T_FALL, 0.12)
    word(c, t, "CRASH!", 600, TOP - 470, 96, (1, 1, 1), T_CRASH, T_CRASH + 0.8, -0.08)
    if T_CRASH <= t < T_CRASH + 0.6:
        q = seg(t, T_CRASH, T_CRASH + 0.6)
        for j in range(8):
            a = math.pi * (1 + j / 7)
            ellipse(c, 640 + math.cos(a) * 380 * q, TOP - 10 + math.sin(a) * 120 * q, 26 * (1 - q) + 4, 14 * (1 - q) + 3, (1, 1, 1), stroke=False)
    word(c, t, "plop", JAR_X + 30, TOP - 420, 44, (1, 1, 1), T_CRASH, T_CRASH + 0.6, 0.1)
    if T_CRASH <= t < T_ROLL + 0.3:   # stars over Dill
        for j in range(3):
            a = t * 6 + j * 2.1
            star(c, CRX + 90 * math.cos(a), TOP - crumb_top(t) - 330 + 22 * math.sin(a), 16, t * 4, GOLD)
    # Grandma
    word(c, t, "sigh...", GRX + 30, TOP - 330, 46, (1, 1, 1), T_SIGH, T_HOBBLE + 0.3, -0.06)
    word(c, t, "BOING!", 340, 380, 64, hexc("#FFE680"), T_SPRING, T_SPRING + 0.6, -0.1)
    if T_SPRING <= t < T_HOOK:
        gx, gy, _, _ = gran_state(t)
        for j in range(3):
            c.move_to(gx - 60 + 60 * j, gy + 20); c.line_to(gx - 60 + 60 * j, gy + 140)
            c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(7); c.stroke()
    word(c, t, "chk!", HOOK[0] - 130, HOOK[1] + 70, 46, (1, 1, 1), T_HOOK, T_HOOK + 0.5, -0.1)
    if T_HOOK + 0.2 <= t < TOKS[0]:
        for i, (xx, dl) in enumerate([(DX1 + 10, 0), (CRX, 0.1), (380, 0.2), (640, 0.25)]):
            word(c, t, "!", xx, TOP - 420, 80, (1, 0.9, 0.4), T_HOOK + 0.2 + dl, TOKS[0])
    gx, gy, gkw, pend = gran_state(t)
    tok_xy = (HOOK[0] - 100, HOOK[1] + 190)
    flash_words(c, t, [("tok", tok_xy[0] - 40 * (i % 2), tok_xy[1] + 50 * i, tt, -0.1) for i, tt in enumerate(TOKS)], 54, hexc("#E9C98B"))
    flash_words(c, t, [("tik", VENT_X + 200, 180 + 50 * i, tt, 0.1) for i, tt in enumerate(TIKS1)], 54, ICE)
    flash_words(c, t, [("tok", tok_xy[0] - 30 * (i % 3), tok_xy[1] - 10 + 42 * i, tt, -0.1) for i, tt in enumerate(TOKS2)], 46, hexc("#E9C98B"))
    flash_words(c, t, [("tik", VENT_X + 210 - 20 * (i % 2), 160 + 42 * i, tt, 0.1) for i, tt in enumerate(TIKS2)], 46, ICE)
    if T_NOD <= t < T_UNHOOK:
        word(c, t, "hm.", tok_xy[0] - 20, tok_xy[1] + 40, 54, (1, 1, 1), T_NOD + 0.1, T_UNHOOK)
    # bonk
    word(c, t, "BONK!", 480, TOP - 500, 90, (1, 1, 1), T_BONK, T_BONK + 0.8, 0.1)
    if T_BONK <= t < T_EXPLAIN + 0.6:
        for j in range(3):
            a = t * 6 + j * 2.1
            star(c, 520 + 90 * math.cos(a), TOP - 260 + 20 * math.sin(a), 16, t * 4, GOLD)
    # Grandma's explanation bubble
    if T_EXPLAIN <= t < T_FROST:
        s = back_out(seg(t, T_EXPLAIN, T_EXPLAIN + 0.35))
        if t > T_FROST - 0.3:
            s = 1 - ease(seg(t, T_FROST - 0.3, T_FROST))
        bubble(c, GR_LAND + 120, TOP - 520, 1.7 * s, kingdom_icon)
        word(c, t, "ooooh", 330, TOP - 360, 46, (1, 1, 1), T_EXPLAIN + 0.8, T_SHIVER, -0.08)
    word(c, t, "brrr", 330, TOP - 360, 50, ICE, T_SHIVER, T_FROST, -0.08)
    word(c, t, "brrr", CRX + 40, TOP - 520, 50, ICE, T_SHIVER + 0.15, T_FROST, 0.08)
    # frost figures reactions
    word(c, t, "GASP!", 340, TOP - 280, 60, (1, 1, 1), T_FROST + 0.8, T_DUCKF, -0.08)
    word(c, t, "?", FX + 270, FY - 160, 90, hexc("#FFE680"), T_DTURN + 0.2, T_FLAKE)
    word(c, t, "crrrk", FX - 300, FY - 200, 44, ICE, T_FROST + 0.1, T_FROST + 1.0, -0.1)
    word(c, t, "brrr", 330, TOP - 360, 50, ICE, T_FLAKE + 0.4, T_PUSH, -0.08)
    dark_overlay(c, L)
    vent_eye(c, t)


def frame(c, t):
    if t < T_START:
        title_card(c, t)
        if t > 1.7:
            iris(c, W / 2, H / 2, lerp(1200, 0, ease(seg(t, 1.7, 2.0))))
        return
    if t >= END_T:
        end_card(c, t, END_T); return
    random.seed(int(t * 30))
    cx, cy, Z = camera(t)
    c.save()
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    scene(c, t)
    c.restore()
    if t < T_START + 0.3:
        iris(c, W / 2, H / 2, lerp(0, 1300, ease(seg(t, T_START, T_START + 0.3))))
    # tiks from inside the vent (screen space, top of frame) during the opening
    for i, tt in enumerate(TIK_RUN):
        if tt <= t < tt + (0.6 if i < 3 else 0.35) and t < T_WHISTLE:
            k = back_out(seg(t, tt, tt + 0.12))
            sz = 90 if i < 3 else 70 + 6 * min(i, 10)
            c.save(); c.translate(180 + (i * 233) % 720, 200 + 70 * (i % 3)); c.rotate(0.12 * math.sin(i * 1.7)); c.scale(S(k), S(k))
            text(c, "tik", 0, 0, sz, ICE, olw=12); c.restore()
    if t >= T_STING:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.3, 0.6, 1.0, 0.14 * ease(seg(t, T_STING, T_STING + 0.4))); c.fill()
    if t >= END_T - 0.4:
        iris(c, W / 2, H / 2 + 60, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))


def main(out, preview=None):
    surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, W, H)
    if preview is not None:
        c = cairo.Context(surf); c.set_source_rgb(0, 0, 0); c.paint(); frame(c, preview); surf.write_to_png(out); return
    proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                             "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                             "-crf", "20", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
    for i in range(int(DUR * FPS)):
        c = cairo.Context(surf); c.set_source_rgb(0, 0, 0); c.paint()
        frame(c, i / FPS); surf.flush(); proc.stdin.write(bytes(surf.get_data()))
    proc.stdin.close(); proc.wait()


if __name__ == "__main__":
    main(sys.argv[1], float(sys.argv[2]) if len(sys.argv) > 2 else None)
