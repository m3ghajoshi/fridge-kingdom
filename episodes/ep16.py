"""FRIDGE KINGDOM — Episode 16: "The Ice Cube". 40.0s, 1080x1920 @ 30fps.

Variant B (cold open): the first frame is mid-action; a small title banner sits across the top for 2s.

Cold open, straight from Ep 15: the icy searchlight from the vent is locked on Chip. "eep!" Chip hops into the
meltwater puddle under the vent and holds his breath: he turns see-through (ice in water). The beam sniffs
right over him... and gives up (hmm...). Chip pops up gasping (PAH!). Dill's eyes light up: what a soldier!
He fetches a green bottle cap and plonks it on Chip's head as a helmet (CLANK). It slides right off his
slippery head (shhk). Again. Shhk, clank. Dill steams.
Drill practice: Dill whistles (fweet), the pickles fall in, Crumb marches with Peep marching on his head
(Peep copies, with a wing salute). Chip, at the back, takes one step, slips and starts to skate and spin,
helplessly, straight off the shelf's front edge (WHOOSH). Crumb dives after him. Whip-pan down: SQUISH,
they both land in Dill's fresh butter block.
Butter-glazed Chip glides like a champion: pirouettes and sparkles. He takes Crumb's hands and teaches him
to skate (waltz); Crumb wobbles, then glides; hearts. Peep flutters down and copies, spinning even faster.
Dill drops down to complain, lands on the butter rink, his feet fly up: THUD (stars).
Chip is so happy he melts (drip drip). Crumb panics, scoops him up, runs to the milk carton and tosses him
into the spout: the carton frosts over (DING). On the carton's picture panel, the Duck (with its cap crown)
turns its head to the camera (squeak). Chip pops out of the spout, refrozen and sparkling (ta-da!).
Chip mimes the freezer in a thought bubble: frozen peas rolling, a blizzard (everyone shivers), and the
crowned shadow with glinting eyes (GASP). Dill's eyes light up: his bubble shows himself, crowned, on top of
an ice castle. He whips out a rolled-up map and unfurls it: the fridge, a dot for "us" on the bottom shelf,
and a big red arrow pointing UP to the freezer (drum hit). Dill raises his sword to the ceiling.
Chip, horrified, turns see-through again. Push in on the map's freezer: the little shadow's eyes glint.
DUN DUN DUNNN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crown, duck, dark_overlay, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp,
                 back_out, bubble, INK, GOLD, TOP, FLOOR, W, H, FPS, S)
from ep2 import end_card, jello
from ep5 import cap_crown
from ep6 import grandma, fridge6, pickle_kid, PICKLE_STYLES, JAR_X
from ep8 import shell_half
from ep9 import fat_peep, crumb_bitten, GRAN_HEAD
from ep10 import ceiling_vent, frost, carton, fresh_butter, VENT_X, CARTON_X
from ep12 import vent_glow, squash_at, word, hop
from ep13 import ceiling, bubble_r
from ep15 import chip, puddle, lid_standing, frost_drawing, drop
from animate import heart

DUR = 40.0
END_T = 38.5
DIM = 0.18
FAT = 1.5
GSC = 1.35
PS = 1.2
CHS = 1.3
ICE = hexc("#D0EBFF")
ICE_B = hexc("#74C0FC")
ICE_D = hexc("#1864AB")
BUTTER = hexc("#FFE680")
CAP_G = hexc("#40C057")
CAP_GD = hexc("#2B8A3E")
PAPER = hexc("#F4E4C1")
RED = hexc("#E03131")

# ---------------- timing ----------------
T_EEP = 0.3
T_DIVE = 0.55            # Chip hops into the puddle
T_SPLOOSH = 1.05
T_CLEAR = 1.4            # fully see-through
SNIFFS = (1.7, 2.5)
T_GIVEUP = 3.2           # the beam leaves
T_PAH = 3.9              # Chip pops up gasping
T_PHEW = 4.4
T_IDEA = 4.9             # Dill's eyes light up
T_FETCH = 5.3            # Dill grabs the bottle cap
T_PUT1 = 6.1             # CLANK: helmet on
T_SLIP1 = 6.8
T_PUT2 = 7.5
T_SLIP2 = 8.0
T_STEAM = 8.4
T_WHISTLE = 9.0          # fweet: fall in!
T_LINE = 9.6             # pickles in line
T_MARCH = 9.9
T_CSLIP = 11.4           # Chip's foot slips
T_EDGE = 13.0            # Chip goes off the edge
T_CDIVE = 13.3           # Crumb dives
T_SQUISH = 14.0          # Chip lands in the butter
T_SQUISH2 = 14.35        # Crumb lands
T_GLIDE = 15.2           # Chip glides
T_HANDS = 17.4           # takes Crumb's hands
T_PEEP = 19.0            # Peep flutters down
T_DFALL = 20.6           # Dill drops down
T_DLAND = 21.0
T_THUD = 21.4
T_BLUSH = 22.0
T_MELT = 22.4
T_PANIC = 23.5
T_SCOOP = 23.8
T_TOSS = 24.7
T_PLOP = 25.25
T_FROST = 25.4
T_DUCK = 25.6            # the Duck's one motion (picture on the carton)
T_DING = 26.2
T_POP = 26.5
T_LANDC = 27.1
T_MIME = 27.5            # thought bubble: peas
T_BLIZ = 28.9
T_KING = 30.2
T_GASP = 30.6
T_DIDEA = 31.6           # Dill's eyes light up
T_MAP = 33.0             # pulls out the map
T_UNROLL = 33.3
T_ARROW = 34.0           # drum hit: arrow pointing UP
T_SWORD = 35.1
T_SEE = 35.45            # Chip turns see-through again
T_PUSH = 36.6
DUNS = (37.0, 37.4, 37.8)

# ---------------- layout ----------------
PUD_X = 590              # meltwater puddle under the vent
D0, C0, CH0 = 420, 700, 830
CAP0 = 300               # spare green bottle cap lying on the top shelf
PK_X0 = {0: 35, 1: 100, 4: 165, 2: 230}
PK_LINE = {0: 460, 1: 405, 4: 350, 2: 295}
GR_X = 990
DM, CM = 700, 560        # Dill / Crumb in the marching line
CHM = 215                # Chip at the back of the line
DISH = 420               # butter-dish throne (bottom shelf)
RINK = (420, 230)        # butter rink: centre x, half-width
CHB, CRB, PEB, DIB = 230, 380, 520, 690   # bottom-shelf spots for the mime
MAP_W, MAP_H = 280, 360


def ph(k):
    return (14 + 2 * PICKLE_STYLES[k]["ry"]) * PS


def keyed(keys, t):
    """keys: [(t, v...)] -> eased interpolation of the values."""
    if t <= keys[0][0]:
        return keys[0][1:]
    for a, b in zip(keys, keys[1:]):
        if t < b[0]:
            p = ease(seg(t, a[0], b[0]))
            return tuple(lerp(a[i], b[i], p) for i in range(1, len(a)))
    return keys[-1][1:]


# ---------------- new props ----------------
def bottle_cap(c, x, y, rot=0.0, s=1.0):
    """A spare green crimped bottle cap (Dill's 'helmet'); bottom centre at (x, y), upside-up like a hat."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(s), S(s))
    c.move_to(-50, 0)
    n = 14
    for i in range(n + 1):
        px = -50 + 100 * i / n
        c.line_to(px * (1 - 0.1 * (i % 2)), -6 if i % 2 else 0)
    c.line_to(44, -30); c.line_to(-44, -30); c.close_path()
    c.set_source_rgb(*CAP_G); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.set_source_rgb(*CAP_GD); c.set_line_width(3)
    for i in range(1, n, 2):
        px = -46 + 92 * i / n
        c.move_to(px, -4); c.line_to(px * 0.95, -26); c.stroke()
    ellipse(c, 0, -30, 44, 9, hexc("#8CE99A"), lw=4)
    ellipse(c, -16, -31, 10, 3, (1, 1, 1), stroke=False)
    c.restore()


def butter_rink(c, k):
    """Dill's butter block squashed into a shiny rink on the bottom shelf. k 0..1 spreads it."""
    if k <= 0.01:
        return
    cx, hw = RINK
    w = hw * (0.45 + 0.55 * k)
    c.save()
    c.move_to(cx - w, FLOOR + 10)
    for i in range(13):
        a = math.pi + math.pi * i / 12
        c.line_to(cx + w * math.cos(a), FLOOR + 10 + 22 * math.sin(a) + (5 if i % 2 else 0))
    c.line_to(cx + w, FLOOR + 22); c.line_to(cx - w, FLOOR + 22); c.close_path()
    c.set_source_rgb(*BUTTER); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    for i in range(3):
        rrect(c, cx - w * 0.7 + i * w * 0.5, FLOOR - 4, w * 0.25, 6, 3); c.set_source_rgba(1, 1, 1, 0.8); c.fill()
    c.restore()


def plate(c, x):
    ellipse(c, x, FLOOR - 10, 150, 26, (0.97, 0.97, 1), lw=6)


def glazed(c, draw, k=0.32, alpha=1.0):
    """Draw something butter-glazed (yellow tint) and/or see-through."""
    c.push_group()
    draw()
    if k > 0:
        c.set_operator(cairo.OPERATOR_ATOP)
        c.set_source_rgba(1.0, 0.86, 0.25, k); c.paint()
        c.set_operator(cairo.OPERATOR_OVER)
    c.pop_group_to_source(); c.paint_with_alpha(alpha)


def carton_frost(c, k, t):
    if k <= 0.01:
        return
    c.save(); c.translate(CARTON_X, FLOOR)
    c.rectangle(-82, -422, 164, 422); c.set_source_rgba(0.85, 0.95, 1.0, 0.45 * k); c.fill()
    rnd = random.Random(16)
    for i in range(14):
        x, y = rnd.uniform(-70, 70), rnd.uniform(-410, -20)
        c.set_source_rgba(1, 1, 1, 0.9 * k); c.set_line_width(3)
        for j in range(3):
            a = j * math.pi / 3
            c.move_to(x - 9 * math.cos(a), y - 9 * math.sin(a)); c.line_to(x + 9 * math.cos(a), y + 9 * math.sin(a))
        c.stroke()
    for i in range(7):                       # icicles along the gable eave
        x0 = -76 + i * 25
        ln = (18 + 10 * (i % 3)) * k
        c.move_to(x0 - 7, -422); c.line_to(x0, -422 + ln); c.line_to(x0 + 7, -422); c.close_path()
        c.set_source_rgba(*ICE, 0.95); c.fill()
    c.restore()


def duck_panel(c, turn, glow=0.0):
    """The picture on the milk carton's blue panel: the Duck with its cap crown."""
    c.save(); c.translate(CARTON_X, FLOOR - 245)
    rrect(c, -58, -48, 116, 96, 12); c.set_source_rgb(1, 1, 1); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    c.save(); rrect(c, -58, -48, 116, 96, 12); c.clip()
    duck(c, -6, 58, turn=turn, s=0.42)
    hx = lerp(40, 4, ease(turn)) * 0.42 - 6
    cap_crown(c, hx - 4, 58 - 142 * 0.42 - 18, -0.3 + 0.2 * turn, 0.32)
    c.restore()
    if glow > 0:
        star(c, 40, -36, 14 * glow, glow * 3, (1, 1, 1))
    c.restore()


def scroll_map(c, x, y, unroll, arrow, glint=0.0):
    """Dill's map. (x, y) = top centre (the rolled bar). unroll 0..1; arrow 0..1 draws the UP arrow."""
    w, h = MAP_W, MAP_H * max(0.0, unroll)
    c.save(); c.translate(x, y)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    if h > 4:
        c.rectangle(-w / 2, 0, w, h); c.set_source_rgb(*PAPER); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        c.save(); c.rectangle(-w / 2, 0, w, h); c.clip()
        # the fridge
        rrect(c, -100, 26, 200, 300, 16); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        rrect(c, -100, 26, 200, 80, 16); c.set_source_rgb(*hexc("#A5D8FF")); c.fill_preserve()   # freezer
        c.set_source_rgb(*INK); c.stroke()
        for yy in (170, 250):
            c.move_to(-100, yy); c.line_to(100, yy); c.stroke()
        rrect(c, -80, 128, 30, 42, 6); c.set_source_rgb(*INK); c.set_line_width(3.5); c.stroke()     # jar
        # the freezer: ice castle + crowned shadow with eyes
        for tx, th in [(-50, 30), (-25, 44), (25, 44), (50, 30)]:
            c.move_to(tx - 9, 100); c.line_to(tx - 9, 100 - th + 10); c.line_to(tx, 100 - th); c.line_to(tx + 9, 100 - th + 10)
            c.line_to(tx + 9, 100); c.close_path(); c.set_source_rgb(*hexc("#E7F5FF")); c.fill_preserve()
            c.set_source_rgb(*hexc("#1971C2")); c.set_line_width(3); c.stroke()
        ellipse(c, 0, 82, 15, 20, hexc("#1C2541"), lw=3)
        c.move_to(-13, 66); c.line_to(-15, 50); c.line_to(-6, 60); c.line_to(0, 44); c.line_to(6, 60); c.line_to(15, 50)
        c.line_to(13, 66); c.close_path(); c.set_source_rgb(*ICE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.5); c.stroke()
        for ex in (-6, 6):
            ellipse(c, ex, 78, 3.5 + 3 * glint, 2.6 + 1.5 * glint, hexc("#9AF0FF"), stroke=False)
        # "us": a dot with a tiny crowned pickle on the bottom shelf
        ellipse(c, -40, 300, 12, 12, RED, lw=3)
        ellipse(c, 10, 290, 9, 15, hexc("#7BC043"), lw=3)
        c.move_to(2, 276); c.line_to(2, 268); c.line_to(7, 273); c.line_to(10, 265); c.line_to(13, 273); c.line_to(18, 268)
        c.line_to(18, 276); c.close_path(); c.set_source_rgb(*GOLD); c.fill()
        # the big red arrow pointing UP
        if arrow > 0:
            y0, y1 = 300, 120
            ye = lerp(y0, y1, arrow)
            c.move_to(-40, y0 - 16); c.line_to(-40, ye + 20)
            c.set_source_rgb(*INK); c.set_line_width(20); c.stroke()
            c.move_to(-40, y0 - 16); c.line_to(-40, ye + 20)
            c.set_source_rgb(*RED); c.set_line_width(12); c.stroke()
            c.move_to(-66, ye + 30); c.line_to(-40, ye - 4); c.line_to(-14, ye + 30); c.close_path()
            c.set_source_rgb(*RED); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        c.restore()
    # rolled bars
    for yy in ([0, h] if h > 4 else [0]):
        rrect(c, -w / 2 - 14, yy - 13, w + 28, 26, 13); c.set_source_rgb(*hexc("#D9B77E")); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.restore()


# ---------------- thought-bubble icons ----------------
def peas_icon(t):
    def f(c):
        c.save(); rrect(c, -108, -78, 216, 156, 60); c.clip()
        rrect(c, -108, 30, 216, 60, 0); c.set_source_rgb(*hexc("#D0EBFF")); c.fill()
        for i in range(3):
            x = -130 + ((t - T_MIME) * 140 + i * 80) % 260
            ellipse(c, x, 6, 24, 24, hexc("#69DB7C"), lw=4)
            c.save(); c.translate(x, 6); c.rotate((t - T_MIME) * 6 + i)
            ellipse(c, -8, -8, 6, 4, (1, 1, 1), stroke=False); c.restore()
            ellipse(c, x - 5, -2, 3, 3, INK, stroke=False); ellipse(c, x + 6, -2, 3, 3, INK, stroke=False)
            c.set_source_rgb(*INK); c.set_line_width(2.5); c.move_to(x - 6, 14); c.line_to(x + 6, 14); c.stroke()
        c.restore()
    return f


def blizzard_icon(t):
    def f(c):
        c.save(); rrect(c, -108, -78, 216, 156, 60); c.clip()
        c.rectangle(-120, -90, 240, 180); c.set_source_rgb(*hexc("#A5D8FF")); c.fill()
        rnd = random.Random(3)
        for i in range(16):
            x0, y0 = rnd.uniform(-130, 130), rnd.uniform(-90, 90)
            q = (t - T_BLIZ) * 1.6
            x = (x0 + q * 260 + 130) % 260 - 130
            y = (y0 + q * 90 + 90) % 180 - 90
            c.set_source_rgb(1, 1, 1); c.set_line_width(3.5)
            for j in range(3):
                a = j * math.pi / 3 + q
                c.move_to(x - 10 * math.cos(a), y - 10 * math.sin(a)); c.line_to(x + 10 * math.cos(a), y + 10 * math.sin(a))
            c.stroke()
        for i in range(4):     # wind streaks
            yy = -50 + 34 * i
            xx = ((t - T_BLIZ) * 400 + i * 70) % 300 - 150
            c.move_to(xx, yy); c.line_to(xx + 60, yy); c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(4); c.stroke()
        c.restore()
    return f


def king_icon(t):
    def f(c):
        c.save(); rrect(c, -108, -78, 216, 156, 60); c.clip()
        c.rectangle(-120, -90, 240, 180); c.set_source_rgb(*hexc("#D0EBFF")); c.fill()
        c.translate(0, 70); c.scale(0.36, 0.36)
        c.move_to(-150, 40); c.curve_to(-140, -60, -100, -120, -60, -140)
        c.line_to(-210, -170); c.line_to(-220, -150); c.line_to(-70, -110)
        c.curve_to(-80, -170, -60, -220, 0, -225); c.curve_to(60, -220, 80, -170, 70, -110)
        c.line_to(220, -150); c.line_to(210, -170); c.line_to(60, -140)
        c.curve_to(100, -120, 140, -60, 150, 40); c.close_path()
        c.set_source_rgb(*hexc("#0B1A22")); c.fill_preserve(); c.set_source_rgb(*ICE_B); c.set_line_width(8); c.stroke()
        pts = [(-62, -205), (-70, -290), (-38, -240), (-20, -315), (0, -250), (20, -315), (38, -240), (70, -290), (62, -205)]
        c.move_to(*pts[0])
        for p in pts[1:]:
            c.line_to(*p)
        c.close_path(); c.set_source_rgb(*hexc("#0B1A22")); c.fill_preserve(); c.set_source_rgb(*ICE_B); c.set_line_width(7); c.stroke()
        k = ease(seg(t, T_KING + 0.3, T_KING + 0.5))
        for ex in (-24, 24):
            ellipse(c, ex, -170, 6 + 10 * k, 4 + 5 * k, hexc("#9AF0FF"), stroke=False)
        c.restore()
    return f


def castle_icon(c):
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    for x, hgt in [(-56, 60), (-28, 86), (0, 110), (28, 86), (56, 60)]:
        c.move_to(x - 13, 62); c.line_to(x - 13, 62 - hgt + 18); c.line_to(x, 62 - hgt); c.line_to(x + 13, 62 - hgt + 18)
        c.line_to(x + 13, 62); c.close_path()
        c.set_source_rgb(*hexc("#E7F5FF")); c.fill_preserve(); c.set_source_rgb(*hexc("#1971C2")); c.set_line_width(4); c.stroke()
    # Dill on top of the middle tower, crowned, sword up
    ellipse(c, 0, -62, 13, 20, hexc("#7BC043"), lw=3)
    ellipse(c, 4, -68, 4, 4, (1, 1, 1), lw=1.5)
    crown(c, 0, -86, 0.32, 0.05)
    c.set_source_rgb(*INK); c.set_line_width(3); c.move_to(12, -66); c.line_to(26, -92); c.stroke()
    c.set_source_rgb(*hexc("#FF4D6D")); c.move_to(24, -86); c.line_to(36, -90); c.line_to(26, -96); c.close_path(); c.fill()
    for i in range(5):
        a = -math.pi / 2 + (i - 2) * 0.5
        c.move_to(math.cos(a) * 34, -66 + math.sin(a) * 34); c.line_to(math.cos(a) * 48, -66 + math.sin(a) * 48)
    c.set_source_rgb(*GOLD); c.set_line_width(4); c.stroke()


# ---------------- banner (variant B) ----------------
def banner(c, t):
    if t >= 2.3:
        return
    off = -260 * ease(seg(t, 2.0, 2.3))
    c.save(); c.translate(0, off)
    rrect(c, 40, 34, W - 80, 176, 40); c.set_source_rgba(*hexc("#1C2541"), 0.88); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    text(c, "FRIDGE KINGDOM", W / 2 + 30, 112, 66, GOLD, olw=10)
    crown(c, 150, 120, 0.7, -0.2)
    text(c, "Ep. 16:  The Ice Cube", W / 2, 182, 46, (1, 1, 1), olw=8)
    c.restore()


# ---------------- states ----------------
def chip_state(t):
    """(x, y, kwargs, alpha, spin, glaze, carried)"""
    base = dict(t=t)
    if t < T_DIVE:
        return CH0, TOP, dict(base, mood="eep" if t >= T_EEP else "scared", look=(0, -1), shiver=1.0,
                              arms="out" if t >= T_EEP else "cover"), 1.0, 0.0, 0.0
    if t < T_SPLOOSH:
        x, y = hop((CH0, TOP), (PUD_X, TOP + 8), ease(seg(t, T_DIVE, T_SPLOOSH)), 170)
        return x, y, dict(base, mood="eep", arms="up"), 1.0, 0.0, 0.0
    if t < T_PAH:
        a = lerp(1.0, 0.16, ease(seg(t, T_SPLOOSH, T_CLEAR)))
        blink = "happy" if (t * 1.3) % 1 < 0.08 else "shy"
        return PUD_X, TOP + 8, dict(base, mood=blink, look=(0, -1), arms="cover", melt=0.12, breath=False), a, 0.0, 0.0
    if t < T_IDEA:
        a = lerp(0.16, 1.0, ease(seg(t, T_PAH, T_PAH + 0.2)))
        y = TOP - 40 * math.sin(math.pi * seg(t, T_PAH, T_PAH + 0.4))
        return PUD_X, y, dict(base, mood="eep" if t < T_PHEW else "shy", arms="up" if t < T_PHEW else "down",
                              look=(-1, 0)), a, 0.0, 0.0
    if t < T_WHISTLE:
        mood = "shy"
        if T_PUT1 <= t < T_PUT1 + 0.3 or T_PUT2 <= t < T_PUT2 + 0.3:
            mood = "eep"
        return PUD_X, TOP, dict(base, mood=mood, look=(-1, -0.6)), 1.0, 0.0, 0.0
    if t < T_LINE:
        x, y = hop((PUD_X, TOP), (CHM, TOP), ease(seg(t, T_WHISTLE + 0.1, T_LINE)), 120)
        return x, y, dict(base, mood="shy", look=(-1, 0)), 1.0, 0.0, 0.0
    if t < T_CSLIP:
        return CHM, TOP - 10 * abs(math.sin((t - T_MARCH) * 6)) if t > T_MARCH else TOP, \
            dict(base, mood="happy", arms="draw_l" if t > T_MARCH else "down"), 1.0, 0.0, 0.0
    if t < T_EDGE:
        p = seg(t, T_CSLIP, T_EDGE)
        x = lerp(CHM, 330, ease(p))
        spin = (t - T_CSLIP) * 9
        return x, TOP, dict(base, mood="eep", arms="out"), 1.0, spin, 0.0
    if t < T_SQUISH:
        p = seg(t, T_EDGE, T_SQUISH)
        x = lerp(330, 380, p)
        y = TOP + (FLOOR - TOP) * p * p - 60 * math.sin(math.pi * min(1, p * 2)) * (1 - p)
        return x, y, dict(base, mood="eep", arms="up"), 1.0, (t - T_CSLIP) * 9, 0.0
    if t < T_GLIDE:
        sq = lerp(0.6, 1.0, back_out(seg(t, T_SQUISH, T_SQUISH + 0.4)))
        return 380, FLOOR, dict(base, mood="eep" if t < T_SQUISH + 0.5 else "shy", look=(1, 0), squash=sq), 1.0, 0.0, 0.4
    if t < T_HANDS:
        q = t - T_GLIDE
        x = RINK[0] - 40 + 150 * math.sin(q * 1.6)
        spin = 0.0
        if 16.2 <= t < 17.0:
            spin = (t - 16.2) / 0.8 * 2 * math.pi
        return x, FLOOR, dict(base, mood="happy", arms="up" if spin else "out"), 1.0, spin, 0.4
    if t < T_MELT:
        cx = pair_x(t)
        return cx - 70, FLOOR, dict(base, mood="happy", arms="none", blush=1.0 if t > T_BLUSH else 0.0), 1.0, 0.0, 0.4
    if t < T_SCOOP:
        cx = pair_x(t)
        m = 0.45 * ease(seg(t, T_MELT, T_MELT + 1.0))
        return cx - 70, FLOOR, dict(base, mood="happy", blush=1.0, melt=m), 1.0, 0.0, 0.4
    if t < T_TOSS:
        x = crumb_bot_x(t)
        return x + 10, FLOOR - 300 - 10 * abs(math.sin(t * 16)), dict(base, mood="happy", blush=1.0, melt=0.45), 1.0, 0.0, 0.4
    if t < T_PLOP:
        x, y = hop((crumb_bot_x(T_TOSS) + 10, FLOOR - 300), (CARTON_X, FLOOR - 520), ease(seg(t, T_TOSS, T_PLOP)), 260)
        return x, y, dict(base, mood="happy", blush=1.0, melt=0.45, arms="up"), 1.0, (t - T_TOSS) * 8, 0.4
    if t < T_POP:
        return None
    if t < T_LANDC:
        x, y = hop((CARTON_X, FLOOR - 528), (CHB, FLOOR), ease(seg(t, T_POP, T_LANDC)), 220)
        return x, y, dict(base, mood="happy", arms="up"), 1.0, 0.0, 0.0
    if t < T_MIME:
        return CHB, FLOOR, dict(base, mood="happy", arms="up"), 1.0, 0.0, 0.0
    if t < T_BLIZ:
        return CHB, FLOOR, dict(base, mood="shy", arms="out", look=(1, -1)), 1.0, 0.0, 0.0
    if t < T_KING:
        return CHB, FLOOR, dict(base, mood="scared", shiver=1.0, arms="cover"), 1.0, 0.0, 0.0
    if t < T_DIDEA:
        return CHB, FLOOR, dict(base, mood="scared", shiver=1.0, arms="cover", look=(1, -1)), 1.0, 0.0, 0.0
    if t < T_SEE:
        return CHB, FLOOR, dict(base, mood="shy", look=(1, -0.5)), 1.0, 0.0, 0.0
    a = lerp(1.0, 0.18, ease(seg(t, T_SEE + 0.3, T_SEE + 0.8)))
    return CHB, FLOOR, dict(base, mood="eep", look=(1, -0.5), shiver=1.0, arms="cover"), a, 0.0, 0.0


def pair_x(t):
    """Centre of Chip + Crumb skating together."""
    if t < T_HANDS:
        return 0
    q = t - T_HANDS
    amp = 120 * min(1, q / 0.8)
    x = RINK[0] + 70 + amp * math.sin(q * 1.4)
    if t >= T_BLUSH:
        x0 = RINK[0] + 70 + 120 * math.sin((T_BLUSH - T_HANDS) * 1.4)
        return x0
    return x


def crumb_bot_x(t):
    if t < T_SCOOP:
        return pair_x(t) + 70
    if t < T_TOSS:
        return lerp(pair_x(T_SCOOP) + 70, 400, ease(seg(t, T_SCOOP, T_TOSS - 0.1)))
    if t < T_MIME - 0.6:
        return 400
    return lerp(400, CRB, ease(seg(t, T_MIME - 0.6, T_MIME)))


def crumb_state(t):
    """(x, y, kw, rot, sq, glaze, peep_on)"""
    if t < T_MARCH - 0.3:
        if t < T_GIVEUP:
            mood = "scared"
        elif t < T_PHEW:
            mood = "worried"
        else:
            mood = "sheepish"
        x = C0 if t < T_WHISTLE else lerp(C0, CM, ease(seg(t, T_WHISTLE, T_LINE)))
        return x, TOP, dict(mood=mood, look=(-1, 0)), 0.0, 1.0, 0.0, True
    if t < T_CDIVE:
        bob = (t - T_MARCH) * 6
        look = (-1, 0.3) if t >= T_EDGE - 0.4 else (1, 0)
        mood = "scared" if t >= T_CSLIP + 0.4 else "worried"
        return CM, TOP - 8 * abs(math.sin(bob)) if t > T_MARCH else TOP, dict(mood=mood, look=look,
                                                                                arm="wave_l" if t < T_CSLIP else "down"), 0.0, 1.0, 0.0, True
    if t < T_SQUISH2:
        p = seg(t, T_CDIVE, T_SQUISH2)
        x = lerp(CM, 520, ease(p))
        y = lerp(TOP, FLOOR, p * p) - 120 * math.sin(math.pi * p)
        return x, y, dict(mood="scared", arm="none"), -1.2 * math.sin(math.pi * min(1, p * 1.4)), 1.0, 0.0, False
    if t < T_GLIDE + 0.6:
        sq = lerp(0.65, 1.0, back_out(seg(t, T_SQUISH2, T_SQUISH2 + 0.4)))
        return 520, FLOOR, dict(mood="dizzy"), 0.0, sq, 0.4, False
    if t < T_HANDS:
        return 520, FLOOR, dict(mood="worried", look=(-1, 0)), 0.06 * math.sin(t * 9), 1.0, 0.4, False
    if t < T_PANIC:
        q = t - T_HANDS
        wob = 0.22 * math.sin(q * 11) * max(0.15, 1 - q / 1.8)
        mood = "scared" if q < 0.9 else "sheepish"
        if t >= T_MELT + 0.4:
            mood = "worried"
        return pair_x(t) + 70, FLOOR, dict(mood=mood, look=(-1, 0), arm="none"), wob, 1.0, 0.4, False
    if t < T_MIME:
        x = crumb_bot_x(t)
        run = T_SCOOP <= t < T_TOSS
        bob = 10 * abs(math.sin(t * 16)) if run else 0
        mood = "scared" if t < T_DING else "sheepish"
        return x, FLOOR - bob, dict(mood=mood, look=(-1, -0.6) if t > T_TOSS else (-1, 0),
                                    arm="none" if t < T_TOSS + 0.3 else ("wave_l" if t > T_POP else "down")), \
            0.0, 1.0, 0.4, False
    x = crumb_bot_x(t)
    mood = "worried"
    look = (-1, -1)
    if T_BLIZ <= t < T_DIDEA:
        mood = "scared"
    if t >= T_DIDEA:
        look = (1, 0)
    if t >= T_SWORD:
        mood, look = "scared", (0, -1)
    return x, FLOOR, dict(mood=mood, look=look, shake=2 if T_BLIZ <= t < T_KING else 0), 0.0, 1.0, 0.4, False


def peep_state(t, crumb_top):
    """(x, y, kw)"""
    if t < T_CDIVE:
        x, y = crumb_top
        if t < T_GIVEUP:
            return x, y, dict(mood="shock", face=0, look=(1, -1))
        if t < T_MARCH:
            return x, y, dict(mood="happy", face=0, look=(-1, 0))
        if t < T_CSLIP:
            return x, y - 8 * abs(math.sin((t - T_MARCH) * 6)), dict(mood="proud", face=0.6, wings="salute")
        return x, y, dict(mood="shock", face=-0.4, wings="flap", flap_t=t * 2)
    if t < T_PEEP:      # left behind on the top shelf: peeks over the edge
        return 560, TOP, dict(mood="shock", face=0, look=(0, 1), wings="flap" if t < T_CDIVE + 0.5 else "down", flap_t=t * 2)
    if t < T_PEEP + 0.7:
        p = seg(t, T_PEEP, T_PEEP + 0.7)
        return lerp(560, 230, p), lerp(TOP, FLOOR, ease(p)), dict(mood="happy", face=0, wings="flap", flap_t=t * 3)
    if t < T_DLAND:
        q = t - T_PEEP - 0.7
        return 230 + 30 * math.sin(q * 3), FLOOR, dict(mood="proud", face=0.5, wings="flap", flap_t=t)
    if t < T_MIME:
        if T_TOSS + 0.2 <= t < T_TOSS + 0.8:
            x, y = hop((230, FLOOR), (560, FLOOR), ease(seg(t, T_TOSS + 0.2, T_TOSS + 0.8)), 380)
            return x, y, dict(mood="happy", face=0.4, wings="flap", flap_t=t * 3)
        x = 230 if t < T_TOSS + 0.2 else 560
        return x, FLOOR, dict(mood="shock" if t < T_THUD + 0.6 else "happy", face=0.4, look=(1, 0))
    x = lerp(560, PEB, ease(seg(t, T_MIME - 0.6, T_MIME)))
    if T_BLIZ <= t < T_KING:
        return x, FLOOR, dict(mood="shock", face=0, shake=4, wings="flap", flap_t=t * 4)
    if T_KING <= t < T_DIDEA:
        return x, FLOOR, dict(mood="shock", face=-0.4, look=(-1, -1))
    if t >= T_SWORD:
        return x, FLOOR, dict(mood="proud", face=0.4, wings="salute")
    return x, FLOOR, dict(mood="happy", face=-0.3, look=(-1, -0.5))


def peep_spin(t):
    if T_PEEP + 0.7 <= t < T_DLAND:
        return (t - T_PEEP - 0.7) * 14
    return 0.0


def dill_state(t):
    """(x, y, kw, rot, glaze)"""
    if t < T_PHEW:
        return D0, TOP, dict(mood="shocked", look=(1, -1) if t < T_GIVEUP else (1, 0.3)), 0.0, 0.0
    if t < T_IDEA:
        return D0, TOP, dict(mood="smug", look=(1, 0.3)), 0.0, 0.0
    if t < T_FETCH:
        return D0, TOP, dict(mood="proud", look=(1, 0.2), arm="point"), 0.0, 0.0
    if t < T_PUT1:
        p = seg(t, T_FETCH, T_PUT1)
        x = lerp(D0, CAP0 + 40, ease(p * 2)) if p < 0.5 else lerp(CAP0 + 40, PUD_X - 150, ease(p * 2 - 1))
        return x, TOP, dict(mood="smug", look=(-1 if p < 0.5 else 1, 0.3), arm="reach" if p > 0.45 else "down"), 0.0, 0.0
    if t < T_STEAM:
        arm = "reach" if (T_SLIP1 - 0.1 <= t < T_PUT2 + 0.1) else "point"
        mood = "proud"
        if T_SLIP1 <= t < T_PUT2 - 0.2 or t >= T_SLIP2:
            mood = "frozen"
        return PUD_X - 150, TOP, dict(mood=mood, look=(1, -0.3), arm=arm), 0.0, 0.0
    if t < T_WHISTLE:
        return PUD_X - 150, TOP, dict(mood="angry", look=(1, -0.3), shake=3), 0.0, 0.0
    if t < T_LINE:
        x = lerp(PUD_X - 150, DM, ease(seg(t, T_WHISTLE, T_LINE)))
        return x, TOP, dict(mood="proud", look=(-1, 0), arm="point_l"), 0.0, 0.0
    if t < T_DFALL:
        if t < T_EDGE + 0.3:
            bob = (t - T_MARCH) * 6
            mood = "proud" if t < T_CSLIP + 0.5 else "shocked"
            return DM, TOP - (8 * abs(math.sin(bob)) if t > T_MARCH else 0), \
                dict(mood=mood, look=(-1, 0) if t > T_CSLIP else (1, 0), arm="up"), 0.0, 0.0
        return DM, TOP, dict(mood="shocked", look=(-1, 1), arm="down"), 0.0, 0.0
    if t < T_DLAND:
        p = seg(t, T_DFALL, T_DLAND)
        return lerp(720, 660, p), lerp(TOP - 200, FLOOR, p * p), dict(mood="angry", arm="up", look=(0, 1)), 0.0, 0.0
    if t < T_THUD:
        p = seg(t, T_DLAND, T_THUD)
        r = -1.5 * ease(p)
        return 660 + 290 * p, FLOOR - 90 * math.sin(math.pi * p) - 70 * math.sin(-r), dict(mood="shocked", arm="reach"), r, 0.0
    if t < T_MIME - 0.3:
        return 950, FLOOR - 70, dict(mood="frozen", look=(0, -1), arm="down"), -1.5, 0.35
    if t < T_MIME + 0.2:
        p = seg(t, T_MIME - 0.3, T_MIME + 0.2)
        r = -1.5 * (1 - ease(p))
        return lerp(950, DIB, p), FLOOR - 70 * math.sin(-r), dict(mood="angry", look=(-1, 0)), r, 0.35
    if t < T_BLIZ:
        return DIB, FLOOR, dict(mood="smug", look=(-1, -1), arm="cross"), 0.0, 0.35
    if t < T_KING:
        return DIB, FLOOR, dict(mood="frozen", look=(-1, -1), arm="cross", shake=3), 0.0, 0.35
    if t < T_DIDEA:
        return DIB, FLOOR, dict(mood="shocked", look=(-1, -1)), 0.0, 0.35
    if t < T_MAP:
        return DIB, FLOOR, dict(mood="proud", look=(-1, -1)), 0.0, 0.35
    if t < T_SWORD:
        return DIB, FLOOR, dict(mood="proud", look=(1, 0), arm="point"), 0.0, 0.35
    return DIB, FLOOR, dict(mood="proud", look=(0.5, -1), arm="up"), 0.0, 0.35


def cap_state(t):
    """(x, y, rot) of the green bottle cap (or None)."""
    if t < T_FETCH + 0.4:
        return CAP0, TOP, 0.0
    if t < T_PUT1:
        p = ease(seg(t, T_FETCH + 0.4, T_PUT1))
        x, y = hop((CAP0 + 40, TOP - 300), (PUD_X, TOP - 140 * CHS), p, 80)
        return x, y, 0.0
    head = TOP - 140 * CHS + 4

    def slide(t0, d):
        p = seg(t, t0, t0 + 0.5)
        if p < 0.5:
            return PUD_X + d * 50 * ease(p * 2), head + 10 * p, d * 0.8 * ease(p * 2)
        q = (p - 0.5) * 2
        return PUD_X + d * (50 + 70 * q), lerp(head + 5, TOP, q * q), d * lerp(0.8, 1.4, q)
    if t < T_SLIP1:
        return PUD_X, head, 0.08 * math.sin((t - T_PUT1) * 30) * max(0, 1 - (t - T_PUT1) * 3)
    if t < T_PUT2 - 0.35:
        return slide(T_SLIP1, 1)
    if t < T_PUT2:
        p = ease(seg(t, T_PUT2 - 0.35, T_PUT2))
        return lerp(PUD_X + 120, PUD_X, p), lerp(TOP, head, p) - 60 * math.sin(math.pi * p), lerp(1.4, 0, p)
    if t < T_SLIP2:
        return PUD_X, head, 0.0
    if t < T_WHISTLE:
        return slide(T_SLIP2, -1)
    if t < T_WHISTLE + 0.5:     # Dill grabs it and plonks it on his own head
        p = ease(seg(t, T_WHISTLE, T_WHISTLE + 0.5))
        x, y = hop((PUD_X - 120, TOP), (dill_state(t)[0] + 4, TOP - 278), p, 120)
        return x, y, lerp(-1.4, 0.12, p)
    if t < T_DFALL:
        x, y, _, _, _ = dill_state(t)
        return x + 4, y - 278, 0.12
    return None


def pickle_pos(k, t):
    if t < T_WHISTLE + 0.1 + 0.12 * k:
        return PK_X0[k], TOP, 0.0
    t0 = T_WHISTLE + 0.1 + 0.12 * k
    p = seg(t, t0, t0 + 0.5)
    if p < 1:
        x, y = hop((PK_X0[k], TOP), (PK_LINE[k], TOP), ease(p), 90)
        return x, y, 0.0
    step = (t - T_MARCH) * 1.5 if t > T_MARCH else 0
    return PK_LINE[k], TOP, step


def vent_on(t):
    if t < T_GIVEUP:
        return 0.8 + 0.2 * math.sin(t * 9)
    return max(0.0, 1 - seg(t, T_GIVEUP, T_GIVEUP + 0.5))


def beam_x(t):
    keys = [(0.0, CH0, 1.0), (T_DIVE + 0.2, CH0, 1.0), (T_SPLOOSH + 0.2, PUD_X + 60, 1.0), (SNIFFS[0], PUD_X - 20, 1.0),
            (SNIFFS[1], PUD_X + 30, 1.0), (T_GIVEUP, PUD_X + 10, 1.0), (T_GIVEUP + 0.6, 960, 0.0)]
    return keyed(keys, t)


def duck_turn(t):
    return ease(seg(t, T_DUCK, T_DUCK + 0.6))


# ---------------- camera ----------------
KEYS = [(0.0, 760, 470, 2.0), (T_DIVE, 760, 470, 2.0), (T_SPLOOSH, 640, 480, 1.9), (T_GIVEUP, 640, 470, 1.8),
        (T_PAH, 600, 520, 2.1), (T_IDEA, 520, 500, 2.0), (T_FETCH + 0.4, 420, 500, 1.9), (T_PUT1, 520, 520, 2.15),
        (T_STEAM, 520, 520, 2.15), (T_WHISTLE + 0.2, 480, 500, 1.5), (T_MARCH, 490, 500, 1.45), (T_CSLIP, 470, 500, 1.5),
        (T_EDGE, 380, 520, 1.85), (T_EDGE + 0.4, 420, 900, 1.8), (T_SQUISH, 430, 1290, 1.9), (T_SQUISH2 + 0.4, 440, 1300, 1.95),
        (T_GLIDE, 450, 1290, 2.0), (T_HANDS, 470, 1290, 1.95), (T_PEEP, 440, 1280, 1.7), (T_DFALL - 0.3, 600, 1250, 1.5),
        (T_THUD, 640, 1280, 1.5), (T_BLUSH + 0.2, 470, 1300, 1.95), (T_MELT + 0.6, 480, 1300, 2.1), (T_PANIC, 470, 1280, 1.8),
        (T_TOSS, 300, 1210, 1.7), (T_DUCK, 190, 1230, 2.4), (T_DING, 190, 1230, 2.4), (T_POP, 280, 1170, 1.8),
        (T_MIME, 440, 1180, 1.55), (T_KING + 0.4, 440, 1180, 1.55), (T_GASP + 0.4, 450, 1200, 1.65),
        (T_DIDEA, 600, 1200, 1.6), (T_MAP, 700, 1200, 1.6), (T_ARROW, 760, 1200, 1.65), (T_SWORD, 600, 1180, 1.45),
        (T_SEE, 500, 1200, 1.5), (T_PUSH, 480, 1220, 1.6), (T_PUSH + 0.8, 910, FLOOR - 330, 2.9), (END_T, 910, FLOOR - 320, 3.4)]


def camera(t):
    cx, cy, z = keyed(KEYS, t)
    hw = 540 / z
    cx = min(max(cx, hw), W - hw)
    for t0, s in [(T_PUT1, 5), (T_SQUISH, 8), (T_SQUISH2, 6), (T_THUD, 9), (T_ARROW, 6)]:
        if t0 <= t < t0 + 0.25:
            q = s * (1 - seg(t, t0, t0 + 0.25)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    for d in DUNS:
        if d <= t < d + 0.12:
            z += 0.12 * (1 - seg(t, d, d + 0.12))
    return cx, cy, z


# ---------------- scene ----------------
def map_pos(t):
    return DIB + 220, FLOOR - 400


def draw_chip(c, t):
    st = chip_state(t)
    if st is None:
        return
    x, y, kw, alpha, spin, glaze = st
    sq = kw.pop("squash", 1.0)
    arms = kw.get("arms", "down")
    if arms == "none":
        kw["arms"] = "out"

    def d():
        c.save()
        c.translate(x, y); c.scale(S(math.cos(spin)) if spin else 1.0, 1.0)
        if sq != 1.0:
            squash_at(c, 0, 0, sq)
        c.translate(-x, -y)
        chip(c, x, y, CHS, **kw)
        c.restore()
    if alpha < 0.999 or glaze > 0:
        glazed(c, d, glaze, alpha)
        if alpha < 0.5:     # only his eyes still show
            for ex in (-19, 19):
                ellipse(c, x + ex * CHS, y - 64 * CHS, 6, 7, INK, stroke=False)
    else:
        d()
    if glaze > 0 and int(t * 4) % 2 == 0:
        star(c, x + 50, y - 160, 12, t * 5, (1, 1, 1))


def scene(c, t):
    L = DIM
    fridge6(c, L, 1, lid=False)
    frost(c, t, 1.0)
    frost_drawing(c, 40.0)
    ceiling(c, L)
    ceiling_vent(c, L)
    vent_glow(c, vent_on(t) if t < T_GIVEUP + 0.5 else 0.0)

    # ---- top shelf ----
    shell_half(c, 1035, TOP - 70, 0.0, top=False)
    lid_standing(c, 950, math.pi / 2)
    puddle(c, PUD_X, TOP, 85)
    if T_SPLOOSH <= t < T_SPLOOSH + 0.4:
        q = seg(t, T_SPLOOSH, T_SPLOOSH + 0.4)
        for j in range(6):
            a = math.pi * (1.05 + 0.18 * j)
            ellipse(c, PUD_X + math.cos(a) * 110 * q, TOP - 20 + math.sin(a) * 90 * q + 60 * q * q, 8, 8, ICE_B, lw=2)
    gk = dict(look=(-1, 0), mood="stern", cane="down")
    if T_EDGE <= t < T_SQUISH:
        gk = dict(look=(-1, 1), mood="stern", cane="up")
    c.save(); c.translate(GR_X, TOP); c.scale(GSC, GSC); c.translate(-GR_X, -TOP)
    grandma(c, GR_X, TOP, **gk)
    c.restore()
    crown(c, GR_X + GRAN_HEAD[0], TOP + GRAN_HEAD[1], 0.72, -0.2)
    for k in (0, 1, 4, 2):
        x, y, step = pickle_pos(k, t)
        c.save(); c.translate(x, y); c.scale(PS, PS); c.translate(-x, -y)
        mood = "shock" if (t < T_GIVEUP or T_EDGE - 0.3 <= t < T_EDGE + 1.0) else "calm"
        pickle_kid(c, x, y - (6 * abs(math.sin(step * math.pi)) if step else 0), k, look=(1, 0) if t > T_WHISTLE else (1, -0.5),
                   step=step, arms="march" if step else "down", mood=mood)
        c.restore()
    cs = cap_state(t)
    cap_under = cs is not None and t < T_PUT1 - 0.4

    if cap_under:
        bottle_cap(c, cs[0], cs[1], cs[2], 1.0)

    # Dill (top shelf part / falling)
    dx, dy, dkw, drot, dgl = dill_state(t)
    top_phase = t < T_DFALL
    if top_phase:
        dill(c, dx, dy, crown_on=False, rot=drot, **dkw)

    # Crumb + Peep
    crx, cry, ckw, crot, csq, cgl, peep_on = crumb_state(t)
    arm = ckw.get("arm", "down")

    def dc():
        c.save(); squash_at(c, crx, cry, csq)
        crumb_bitten(c, crx, cry, 1.0, rot=crot, **ckw)
        c.restore()
    top_phase_c = t < T_SQUISH2
    if top_phase_c and t < T_CDIVE:
        dc()
    if t < T_SQUISH or t >= T_POP:
        if t < T_SQUISH:
            draw_chip(c, t)
    if top_phase_c and t >= T_CDIVE:
        dc()
    h = 300 * csq - 14
    ctop = (crx + math.sin(crot) * h, cry - math.cos(crot) * h)
    px, py, pkw = peep_state(t, ctop)
    if t < T_PEEP:
        fat_peep(c, px, py, FAT, **pkw)

    if cs is not None and not cap_under:
        bottle_cap(c, cs[0], cs[1], cs[2], 1.0)

    # ---- bottom shelf ----
    jw = 0.6 * math.sin((t - T_THUD) * 18) * max(0, 1 - (t - T_THUD) * 1.5) if t >= T_THUD else 0.0
    jello(c, 985, FLOOR, jw)
    carton(c, bulge=0.25 * math.sin(math.pi * seg(t, T_PLOP, T_PLOP + 0.3)) if T_PLOP <= t < T_PLOP + 0.3 else
           (0.3 * math.sin(math.pi * seg(t, T_POP - 0.2, T_POP + 0.1)) if T_POP - 0.2 <= t < T_POP + 0.1 else 0.0),
           spout_open=1.0 if (T_PLOP - 0.3 <= t < T_PLOP + 0.2 or T_POP - 0.2 <= t < T_POP + 0.3) else 0.0)
    duck_panel(c, duck_turn(t), glow=math.sin(math.pi * seg(t, T_DUCK + 0.6, T_DUCK + 1.0)) if T_DUCK + 0.6 <= t < T_DUCK + 1.0 else 0)
    carton_frost(c, ease(seg(t, T_FROST, T_FROST + 0.6)) * (1 - 0.5 * ease(seg(t, T_POP + 1.0, T_POP + 2.5))), t)
    if t < T_SQUISH:
        fresh_butter(c, DISH, FLOOR)
    else:
        plate(c, DISH)
        butter_rink(c, ease(seg(t, T_SQUISH, T_SQUISH + 0.35)))
        if T_SQUISH <= t < T_SQUISH + 0.5:
            q = seg(t, T_SQUISH, T_SQUISH + 0.5)
            for j in range(8):
                a = math.pi * (1.0 + j / 7)
                ellipse(c, DISH + math.cos(a) * 200 * q, FLOOR - 40 + math.sin(a) * 140 * q + 80 * q * q,
                        12 * (1 - q) + 2, 10 * (1 - q) + 2, BUTTER, lw=3)
    # skate trail sparkles on the rink
    if T_GLIDE <= t < T_BLUSH:
        for j in range(5):
            q = ((t - T_GLIDE) * 0.9 + j / 5) % 1
            star(c, RINK[0] - 200 + 400 * q, FLOOR + 4, 9 * math.sin(math.pi * q), t * 4 + j, (1, 1, 1))
    if not top_phase:
        def dd():
            dill(c, dx, dy, crown_on=False, rot=drot, **dkw)
        if dgl > 0:
            glazed(c, dd, dgl)
        else:
            dd()
        if T_MAP <= t:
            mx, my = map_pos(t)
            if t < T_UNROLL:   # pops into his hand, rolled up
                s = back_out(seg(t, T_MAP, T_MAP + 0.25))
                c.save(); c.translate(mx - 60, my + 120); c.rotate(-0.4); c.scale(S(s), S(s))
                rrect(c, -150, -14, 300, 28, 14); c.set_source_rgb(*hexc("#D9B77E")); c.fill_preserve()
                c.set_source_rgb(*INK); c.set_line_width(5); c.stroke(); c.restore()
            else:
                gl = ease(seg(t, T_PUSH + 0.6, T_PUSH + 0.9))
                scroll_map(c, mx, my, ease(seg(t, T_UNROLL, T_UNROLL + 0.5)), ease(seg(t, T_ARROW - 0.35, T_ARROW)), gl)
    if not top_phase_c:
        if cgl > 0:
            glazed(c, dc, cgl)
        else:
            dc()
        if arm == "none":
            draw_crumb_arms(c, t, crx, crot)
    if T_SQUISH <= t < T_POP or t >= T_POP:
        if t >= T_SQUISH:
            draw_chip(c, t)
    if T_HANDS <= t < T_SCOOP:      # holding hands
        cx_ = pair_x(t)
        c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(cx_ - 70 + 60, FLOOR - 90); c.line_to(cx_ + 70 - 70 * math.cos(crot), FLOOR - 120); c.stroke()
    if t >= T_PEEP:
        rot = 0.0
        sp = peep_spin(t)
        c.save()
        if sp:
            c.translate(px, py); c.scale(S(math.cos(sp)), 1.0); c.translate(-px, -py)
        fat_peep(c, px, py, FAT, **pkw)
        c.restore()

    # ---- effects ----
    effects(c, t, dx, dy)
    dark_overlay(c, L)
    # searchlight (light: after the dark overlay)
    if t < T_GIVEUP + 0.6:
        bx, k = beam_x(t)
        if k > 0.01:
            c.move_to(VENT_X - 70, 125); c.line_to(VENT_X + 70, 125); c.line_to(bx + 120, TOP + 20); c.line_to(bx - 120, TOP + 20)
            c.close_path(); c.set_source_rgba(0.62, 0.88, 1.0, 0.26 * k); c.fill()
            c.save(); c.translate(bx, TOP + 12); c.scale(125, 22); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(0.8, 0.95, 1.0, 0.45 * k); c.fill()
    for i, s in enumerate(SNIFFS):
        word(c, t, "sniff...", VENT_X + (200 if i else -200), 230 + 40 * i, 56, ICE, s, s + 0.7, 0.1 if i else -0.1)
    word(c, t, "hmm...", VENT_X + 200, 250, 52, ICE, T_GIVEUP - 0.1, T_GIVEUP + 0.7, 0.08)
    if t >= T_SEE and t < END_T:
        c.rectangle(-400, -400, W + 800, H + 800); c.set_source_rgba(0.3, 0.6, 1.0, 0.1 * ease(seg(t, T_SEE, T_SEE + 0.5))); c.fill()


def draw_crumb_arms(c, t, x, rot):
    """Crumb's arms for the dive / skating / carrying beats."""
    c.save(); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_source_rgb(*INK); c.set_line_width(9)
    _, y, _, _, _, _, _ = crumb_state(t)

    def sh(side):
        sx, sy = side * 70, -120
        ca, sa = math.cos(rot), math.sin(rot)
        return x + sx * ca - sy * sa, y + sx * sa + sy * ca
    if t < T_SQUISH2:                         # diving, arms out ahead
        ca, sa = math.cos(rot), math.sin(rot)
        for side in (-1, 1):
            s = sh(side)
            c.move_to(*s); c.line_to(s[0] + 120 * sa - 30 * side * ca, s[1] - 120 * ca - 30 * side * sa)
    elif t < T_SCOOP:                         # left hand to Chip, right arm out for balance
        s = sh(-1); c.move_to(*s); c.line_to(x - 120, FLOOR - 120)
        s = sh(1); c.move_to(*s); c.line_to(x + 110 + 20 * math.sin(t * 8), FLOOR - 230)
    else:                                     # carrying Chip in front
        for side in (-1, 1):
            s = sh(side); c.move_to(*s); c.line_to(x + 10 + side * 60, y - 300)
    c.stroke(); c.restore()


def effects(c, t, dx, dy):
    word(c, t, "eep!", CH0 + 30, TOP - 260, 60, ICE, T_EEP, T_DIVE + 0.3, 0.12)
    word(c, t, "SPLOOSH", PUD_X, TOP - 250, 58, ICE_B, T_SPLOOSH, T_SPLOOSH + 0.5, -0.08)
    word(c, t, "PAH!", PUD_X + 40, TOP - 260, 64, (1, 1, 1), T_PAH, T_PAH + 0.6, 0.1)
    word(c, t, "phew", 700, TOP - 400, 48, (1, 1, 1), T_PHEW, T_PHEW + 0.7, -0.08)
    if T_IDEA <= t < T_FETCH + 0.2:
        q = seg(t, T_IDEA, T_FETCH + 0.2)
        for ex, ey in ((-28, -205), (30, -212)):
            star(c, D0 + ex + 6, TOP + ey, 22 * math.sin(math.pi * q), t * 6, GOLD)
        word(c, t, "!", D0 + 30, TOP - 380, 90, GOLD, T_IDEA, T_FETCH + 0.2)
    word(c, t, "CLANK!", PUD_X + 30, TOP - 320, 60, (1, 0.9, 0.4), T_PUT1, T_PUT1 + 0.5, 0.1)
    word(c, t, "shhk", PUD_X + 140, TOP - 200, 46, (1, 1, 1), T_SLIP1 + 0.1, T_SLIP1 + 0.6, 0.1)
    word(c, t, "CLANK!", PUD_X + 10, TOP - 330, 56, (1, 0.9, 0.4), T_PUT2, T_PUT2 + 0.4, -0.1)
    word(c, t, "shhk", PUD_X - 160, TOP - 200, 46, (1, 1, 1), T_SLIP2 + 0.1, T_SLIP2 + 0.6, -0.1)
    if T_STEAM <= t < T_WHISTLE:
        for j in range(3):
            q = ((t - T_STEAM) * 1.6 + j / 3) % 1
            ellipse(c, PUD_X - 150 + (j - 1) * 40, TOP - 300 - 100 * q, 16 + 14 * q, 12 + 10 * q, (1, 1, 1), stroke=False)
            c.set_source_rgba(0, 0, 0, 0)
    word(c, t, "fweet!", DM - 60 if False else 540, TOP - 400, 56, (1, 1, 1), T_WHISTLE, T_WHISTLE + 0.6, -0.1)
    if T_MARCH <= t < T_EDGE:
        for j, (dt, s_) in enumerate([(0, "hup"), (1.0, "hup"), (2.0, "hup")]):
            word(c, t, s_, DM + 90, TOP - 400 + 20 * j, 44, GOLD, T_MARCH + dt, T_MARCH + dt + 0.5, 0.1)
    word(c, t, "?!", CHM + 40, TOP - 240, 60, ICE, T_CSLIP, T_CSLIP + 0.6, 0.1)
    if T_CSLIP + 0.3 <= t < T_EDGE:
        x = lerp(CHM, 330, ease(seg(t, T_CSLIP, T_EDGE)))
        word(c, t, "swish", x - 40, TOP + 80, 44, ICE, T_CSLIP + 0.3, T_EDGE, -0.08)
    word(c, t, "WHOOSH", 360, TOP + 150, 60, (1, 1, 1), T_EDGE, T_EDGE + 0.6, 0.1)
    word(c, t, "!!", CM + 60, TOP - 380, 80, (1, 0.35, 0.35), T_EDGE - 0.3, T_CDIVE + 0.2)
    word(c, t, "SQUISH!", DISH, FLOOR - 330, 72, BUTTER, T_SQUISH, T_SQUISH + 0.6, -0.08)
    word(c, t, "SQUISH!", DISH + 140, FLOOR - 400, 60, BUTTER, T_SQUISH2, T_SQUISH2 + 0.5, 0.1)
    if T_GLIDE + 0.3 <= t < T_HANDS:
        word(c, t, "~ ~ ~", RINK[0], FLOOR + 80, 44, (1, 1, 1), T_GLIDE + 0.3, T_HANDS)
    if T_HANDS + 1.0 <= t < T_BLUSH:
        for j in range(4):
            q = ((t - T_HANDS) * 0.7 + j / 4) % 1
            heart(c, pair_x(t) - 80 + 50 * j, FLOOR - 330 - 140 * q, 1.2, 1 - q)
    word(c, t, "wheee!", 260, FLOOR - 330, 46, (1, 1, 1), T_PEEP + 0.8, T_PEEP + 1.6, 0.1)
    word(c, t, "BOING!", 900, FLOOR - 280, 70, (1, 0.9, 0.4), T_THUD, T_THUD + 0.6, -0.08)
    if T_THUD <= t < T_MIME - 0.3:
        for j in range(4):
            a = (t - T_THUD) * 4 + j * math.pi / 2
            star(c, 750 + 70 * math.cos(a), FLOOR - 170 + 18 * math.sin(a), 14, t * 5, GOLD)
    if T_BLUSH <= t < T_PANIC:
        for j in range(3):
            q = ((t - T_BLUSH) * 0.8 + j / 3) % 1
            heart(c, pair_x(t) - 110 + 50 * j, FLOOR - 240 - 120 * q, 1.0, 1 - q)
    word(c, t, "drip", pair_x(T_BLUSH) - 160, FLOOR - 120, 42, ICE, T_MELT + 0.3, T_MELT + 0.9, -0.1)
    word(c, t, "drip", pair_x(T_BLUSH), FLOOR - 200, 42, ICE, T_MELT + 0.8, T_MELT + 1.4, 0.1)
    if T_MELT + 0.3 <= t < T_TOSS:
        r = 70 * ease(seg(t, T_MELT + 0.3, T_MELT + 1.1))
        if t >= T_SCOOP:
            r *= 1 - seg(t, T_SCOOP, T_SCOOP + 0.3)
        puddle(c, pair_x(T_BLUSH) - 70, FLOOR, r)
    word(c, t, "!!", pair_x(T_BLUSH) + 90, FLOOR - 400, 80, (1, 0.35, 0.35), T_PANIC, T_SCOOP + 0.4)
    word(c, t, "plop", CARTON_X + 90, FLOOR - 560, 50, (1, 1, 1), T_PLOP, T_PLOP + 0.6, 0.1)
    word(c, t, "squeak", CARTON_X + 130, FLOOR - 300, 40, (1, 1, 1), T_DUCK + 0.1, T_DUCK + 0.9, 0.1)
    word(c, t, "DING!", CARTON_X + 110, FLOOR - 470, 56, GOLD, T_DING, T_DING + 0.5, -0.1)
    word(c, t, "ta-da!", CARTON_X + 160, FLOOR - 600, 56, GOLD, T_POP, T_POP + 0.8, 0.1)
    if T_POP <= t < T_POP + 0.6:
        q = seg(t, T_POP, T_POP + 0.6)
        for j in range(6):
            a = -math.pi * j / 5
            star(c, CARTON_X + math.cos(a) * 140 * q, FLOOR - 540 + math.sin(a) * 140 * q, 18 * (1 - q), t * 6, (1, 1, 1))
    # Chip's thought bubble
    if T_MIME <= t < T_DIDEA:
        s = 1.35 * back_out(seg(t, T_MIME, T_MIME + 0.3))
        if t >= T_DIDEA - 0.25:
            s *= 1 - seg(t, T_DIDEA - 0.25, T_DIDEA)
        icon = peas_icon(t) if t < T_BLIZ else blizzard_icon(t) if t < T_KING else king_icon(t)
        bubble(c, CHB + 120, FLOOR - 470, s, icon)
    word(c, t, "brrr", 470, FLOOR - 350, 50, ICE, T_BLIZ + 0.3, T_KING, -0.1)
    word(c, t, "brrr", 760, FLOOR - 380, 50, ICE, T_BLIZ + 0.6, T_KING, 0.1)
    word(c, t, "GASP!", 560, FLOOR - 640, 62, (1, 1, 1), T_GASP, T_GASP + 0.8, -0.08)
    if T_DIDEA <= t < T_DIDEA + 0.8:
        q = seg(t, T_DIDEA, T_DIDEA + 0.8)
        for ex, ey in ((-28, -205), (30, -212)):
            star(c, DIB + ex - 6, FLOOR + ey - 4, 24 * math.sin(math.pi * q), t * 6, GOLD)
    if T_DIDEA + 0.2 <= t < T_MAP:
        s = 1.25 * back_out(seg(t, T_DIDEA + 0.2, T_DIDEA + 0.5))
        bubble_r(c, DIB - 170, FLOOR - 520, s, castle_icon)
    word(c, t, "ooooh", DIB + 120, FLOOR - 420, 46, GOLD, T_DIDEA + 0.5, T_MAP, 0.1)
    word(c, t, "!", DIB + 80, FLOOR - 380, 90, GOLD, T_MAP, T_UNROLL + 0.2, 0.1)
    word(c, t, "BOOM", map_pos(t)[0] + 150, FLOOR - 470, 56, (1, 0.35, 0.35), T_ARROW, T_ARROW + 0.5, 0.12)
    word(c, t, "eep!", CHB + 40, FLOOR - 280, 60, ICE, T_SEE, T_SEE + 0.8, 0.12)
    word(c, t, "gulp", CRB + 70, FLOOR - 340, 46, (1, 1, 1), T_SEE + 0.3, T_SEE + 1.0, -0.1)


def frame(c, t):
    if t >= END_T:
        end_card(c, t, END_T); return
    random.seed(int(t * 30))
    cx, cy, Z = camera(t)
    c.save()
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    scene(c, t)
    c.restore()
    if t >= END_T - 0.4:
        mx, my = map_pos(t)
        iris(c, W / 2 + (mx - cx) * Z, H / 2 + (my + 80 - cy) * Z, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))
    banner(c, t)


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
