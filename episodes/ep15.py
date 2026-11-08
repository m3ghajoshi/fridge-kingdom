"""FRIDGE KINGDOM — Episode 15: "Something Is Melting". 40.0s, 1080x1920 @ 30fps.

Variant A (title card first): 2s FRIDGE KINGDOM title card, then the story.

Night on the frosty top shelf. Crownless Dill stands guard under the ceiling vent, sword raised... plip. A drop of
meltwater hits his head. Plip. Plip, right in his big eye. He shakes his sword at the vent (GRRR).
Crumb (Peep riding on his head) points down: a trail of tiny wet SQUARE footprints leads away from the puddle
under the vent. Detective music: Dill and Crumb tiptoe along the trail (Peep copies the tiptoe), even circling
the crust bit where the prints loop around it, to the old Jar lid, which now stands propped up on its rim.
The lid chatters. Dill grabs Crumb and plonks him in front (bait, as usual). Crumb tips the lid over: CLANG.
Behind it: a small shivering ice cube. GASP; "eep!". This is Chip. Crumb softens and hugs him; Chip blushes
and melts (drip, drip, puddle). Panic! Crumb whips out a napkin, mops the puddle (squeak squeak) and wrings it
back over Chip, who pops back to full size (ta-da). Peep hops down and copies Chip's shiver, ten times bigger
(brrr! BRRRR!); Chip giggles. Dill crosses his arms and turns away (hmph).
Chip hops up and scratches a picture into the frost on the back wall: a huge crowned shadow reaching for a
tiny cube running away. Up on the Jar, the Duck (towel turban still frosty) makes its one motion: it slowly
turns its head and slides its eyes toward the drawing (squeak). The drawn shadow's eyes glint; everyone shivers.
Then the vent RATTLES. Icy searchlight beams sweep the shelf; Chip dives behind Crumb. SNIFF... SNIFF...
The beam slides across everyone and stops on Chip peeking out from behind Crumb. DUN DUN DUNNN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crown, dark_overlay, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp,
                 back_out, INK, GOLD, TOP, W, H, FPS, S)
from ep2 import end_card
from ep6 import grandma, fridge6, pickle_kid, PICKLE_STYLES, JAR_X
from ep8 import shell_half
from ep9 import fat_peep, crumb_bitten, bread_bit, GRAN_HEAD
from ep10 import ceiling_vent, frost, napkin_folded, VENT_X
from ep12 import vent_glow, squash_at, word, hop
from ep13 import ceiling
from ep14 import clean_duck
from animate import heart

DUR = 40.0
T_START = 2.0
END_T = 38.5
DIM = 0.18
FAT = 1.5
GSC = 1.35
PS = 1.2
ICE = hexc("#D0EBFF")
ICE_B = hexc("#74C0FC")
ICE_D = hexc("#1864AB")
TEAR = hexc("#74C0FC")
CHIP_F = (0.78, 0.92, 1.0)
CHIP_L = (0.92, 0.98, 1.0)
CHIP_E = hexc("#4DABF7")

# ---------------- timing ----------------
DRIPS = (2.9, 3.7, 4.5)       # drop impacts on Dill
T_FIST = 5.1                  # Dill shakes his sword at the vent
T_SPOT = 6.2                  # Crumb spots the footprints
T_FOLLOW = 7.2
T_ARRIVE = 11.6
T_CHATTER = 11.8              # the lid chatters
T_GRAB = 12.5                 # Dill swings Crumb in front of him
T_PLONK = 13.1
T_TIP = 13.7                  # Crumb tips the lid over
T_CLANG = 14.05
T_GASP = 14.2
T_COWER = 14.9
T_SOFT = 16.0
T_HUG = 16.7
T_MELT = 17.3
T_PANIC = 18.8
T_NAPKIN = 19.2
T_MOP = 19.6
T_WRING = 21.0
T_TADA = 22.0
T_BACK = 22.2                 # Crumb steps back
T_PDOWN = 22.5                # Peep hops down
T_SHIV = 23.1                 # Chip shivers
T_PCOPY = 23.8                # Peep copies, hugely
T_GIGGLE = 25.0
T_CROSS = 25.7                # Dill crosses his arms
T_PUP = 27.1                  # Peep hops back onto Crumb
T_DRAW = 27.6
T_DRAW_END = 31.0
T_DUCK = 31.2                 # the Duck's one motion
T_DUCK_END = 32.4
T_GLINT = 32.6
T_RATTLE = 33.6
T_BEAM = 34.1
T_HIDE = 34.4
SNIFFS = (35.0, 35.8)
T_FIND = 36.5
DUNS = (37.0, 37.4, 37.8)

# ---------------- layout ----------------
CHIP_X = 950
LID_X = 950
PK_X = {0: 35, 1: 100, 4: 165, 2: 230}
GRX = 295
DIX0 = 560
CRX0 = 395
CHS = 1.3                    # Chip's scale


def ph(k):
    return (14 + 2 * PICKLE_STYLES[k]["ry"]) * PS


# ---------------- new character: Chip ----------------
def chip(c, x, y, s=1.0, mood="shy", look=(0, 0), melt=0.0, shiver=0.0, t=0.0, blush=0.0, arms="down", rot=0.0,
         breath=True):
    """Chip the ice cube. (x, y) = feet on the floor. melt 0..0.5 slumps him; shiver jitters him."""
    jx = shiver * math.sin(t * 70) * 5
    sy = 1 - 0.55 * melt
    sx = 1 + 0.18 * melt
    c.save(); c.translate(x + jx, y); c.rotate(rot); c.scale(S(s), S(s))
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    # feet
    for fx in (-26, 26):
        ellipse(c, fx, -4, 15, 8, CHIP_F, lw=4)
    c.save(); c.scale(sx, S(sy))
    # arms (behind the body edge)
    pts = {"down": [(-54, -52, -78, -30), (54, -52, 78, -30)],
           "up": [(-52, -62, -76, -102), (52, -62, 76, -102)],
           "draw": [(-54, -52, -78, -30), (52, -64, 84, -108)],
           "draw_l": [(-52, -64, -84, -108), (54, -52, 78, -30)],
           "out": [(-54, -58, -90, -66), (54, -58, 90, -66)],
           "cover": [(-50, -56, -22, -70), (50, -56, 22, -70)]}[arms]
    for (ax, ay, bx, by) in pts:
        c.move_to(ax, ay); c.line_to(bx, by); c.set_source_rgb(*INK); c.set_line_width(17); c.stroke()
        c.move_to(ax, ay); c.line_to(bx, by); c.set_source_rgb(*CHIP_F); c.set_line_width(9); c.stroke()
    # body: translucent rounded cube
    rrect(c, -58, -116, 116, 112, 26); c.set_source_rgba(*CHIP_F, 0.93); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    rrect(c, -46, -110, 92, 18, 9); c.set_source_rgba(*CHIP_L, 0.95); c.fill()           # top bevel
    c.save(); c.translate(-36, -76); c.rotate(0.25)                                        # frost streak
    rrect(c, -7, -24, 14, 46, 7); c.set_source_rgba(1, 1, 1, 0.95); c.fill(); c.restore()
    ellipse(c, -38, -36, 5, 5, (1, 1, 1), stroke=False)
    ellipse(c, 32, -28, 8, 8, (0.9, 0.97, 1.0), lw=3)                                       # air-bubble freckle
    ellipse(c, 29, -31, 2.5, 2.5, (1, 1, 1), stroke=False)
    # face
    lx, ly = look
    if mood in ("happy", "giggle"):
        c.set_source_rgb(*INK); c.set_line_width(5)
        for ex in (-19, 19):
            c.move_to(ex - 10, -60); c.curve_to(ex - 5, -72, ex + 5, -72, ex + 10, -60); c.stroke()
    elif mood in ("scared", "eep"):
        for ex in (-20, 20):
            ellipse(c, ex, -64, 14, 16, (1, 1, 1), lw=4)
            ellipse(c, ex + lx * 4, -63 + ly * 4, 5, 6, INK, stroke=False)
    else:
        for ex in (-19, 19):
            ellipse(c, ex + lx * 4, -64 + ly * 3, 7, 9, INK, stroke=False)
            ellipse(c, ex + lx * 4 + 2, -68 + ly * 3, 2.5, 2.5, (1, 1, 1), stroke=False)
    if blush > 0.01:
        for bx in (-36, 36):
            ellipse(c, bx, -46, 11, 6, (1.0, 0.55, 0.7), stroke=False)
            c.set_source_rgba(1.0, 0.55, 0.7, 0)
    c.set_source_rgb(*INK); c.set_line_width(4.5)
    if mood == "eep":
        ellipse(c, 0, -38, 8, 10, hexc("#7A1F2B"), lw=4)
    elif mood == "scared":    # chattering teeth
        op = 4 + 4 * abs(math.sin(t * 40))
        rrect(c, -16, -44, 32, op + 4, 3); c.set_source_rgb(1, 1, 1); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(3.5); c.stroke()
        for tx in (-6, 6):
            c.move_to(tx, -44); c.line_to(tx, -40 + op); c.stroke()
    elif mood == "giggle":
        c.move_to(-14, -44); c.curve_to(-6, -30, 6, -30, 14, -44); c.close_path()
        c.set_source_rgb(*hexc("#7A1F2B")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    elif mood == "happy":
        c.move_to(-12, -42); c.curve_to(-4, -34, 4, -34, 12, -42); c.stroke()
    else:   # wobbly little mouth
        c.move_to(-12, -40)
        for i in range(1, 7):
            c.line_to(-12 + i * 4, -40 + (3 if i % 2 else -2))
        c.stroke()
    c.restore()
    # melt drips running down the sides
    if melt > 0.02:
        for j, dx in enumerate((-50, 8, 44)):
            q = (t * 1.2 + j * 0.37) % 1
            yy = lerp(-100 * sy, -6, q)
            c.move_to(dx * sx, yy - 14); c.curve_to(dx * sx - 7, yy, dx * sx - 6, yy + 7, dx * sx, yy + 7)
            c.curve_to(dx * sx + 6, yy + 7, dx * sx + 7, yy, dx * sx, yy - 14)
            c.set_source_rgba(*ICE_B, 0.95); c.fill()
    c.restore()
    # frosty breath puff
    if breath:
        q = (t * 0.8) % 1
        if q < 0.55:
            k = q / 0.55
            ellipse(c, x + jx + (18 + 40 * k) * s, y - (40 * sy + 20 * k) * s, (8 + 14 * k) * s, (6 + 10 * k) * s,
                    (1, 1, 1), stroke=False)
            c.set_source_rgba(1, 1, 1, 0)


def puddle(c, x, y, rx):
    if rx < 2:
        return
    ellipse(c, x, y + 4, rx, max(4, rx * 0.14), (0.72, 0.88, 1.0), lw=3)
    ellipse(c, x - rx * 0.3, y + 2, rx * 0.25, 2.5, (1, 1, 1), stroke=False)


# ---------------- new props ----------------
def lid_standing(c, x, ang):
    """The Jar lid propped up on its rim (ang 0 = standing, pi/2 = fallen flat, tipped away from us)."""
    r = 88
    k = max(0.12, math.cos(ang))
    cy = TOP - r * k
    c.save()
    # rim thickness below the face when leaning back
    ellipse(c, x, cy + 6 * (1 - k), r, max(8, r * k), [v * 0.55 for v in hexc("#E03131")], lw=6)
    ellipse(c, x, cy, r, max(8, r * k), [v * 0.75 for v in hexc("#E03131")], lw=6)
    ellipse(c, x, cy, r * 0.74, max(5, r * 0.74 * k), [v * 0.85 for v in hexc("#E03131")], lw=4)
    c.set_source_rgb(*[v * 0.5 for v in hexc("#A61E1E")]); c.set_line_width(5)
    for i in range(16):
        a = i * math.pi / 8
        c.move_to(x + r * 0.82 * math.cos(a), cy + r * 0.82 * math.sin(a) * k)
        c.line_to(x + r * 0.96 * math.cos(a), cy + r * 0.96 * math.sin(a) * k)
    c.stroke()
    ellipse(c, x - 30, cy - 34 * k, 16, max(3, 9 * k), (1, 0.75, 0.75), stroke=False)
    c.restore()


def _prints():
    pts = []
    x = 615
    i = 0
    while x < 900:
        if 650 < x < 730 and not any(p[3] for p in pts):     # loop once around the crust bit
            for j in range(7):
                a = math.pi + j * 2 * math.pi / 7
                pts.append((690 + 58 * math.cos(a), TOP + 17 + 8 * math.sin(a), a, True))
            x = 760
            continue
        pts.append((x + (6 if i % 2 else -6), TOP + (10 if i % 2 else 24), 0.0, False))
        x += 44; i += 1
    return pts


PRINTS = _prints()


def footprints(c, t, alpha=1.0):
    for i, (x, y, a, _) in enumerate(PRINTS):
        c.save(); c.translate(x, y); c.rotate(0.15 * math.sin(a))
        rrect(c, -10, -8, 20, 16, 4); c.set_source_rgba(*hexc("#339AF0"), 0.95 * alpha); c.fill_preserve()
        c.set_source_rgba(*INK, 0.8 * alpha); c.set_line_width(2.5); c.stroke()
        ellipse(c, -5, -3, 4, 2, (1, 1, 1), stroke=False)
        if (t * 1.3 + i * 0.13) % 1 < 0.12:
            star(c, 0, -2, 8, t, (1, 1, 1))
        c.restore()


def drop(c, x, y, s=1.0):
    c.move_to(x, y - 16 * s); c.curve_to(x - 10 * s, y, x - 9 * s, y + 10 * s, x, y + 10 * s)
    c.curve_to(x + 9 * s, y + 10 * s, x + 10 * s, y, x, y - 16 * s)
    c.set_source_rgb(*ICE_B); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    ellipse(c, x - 3 * s, y + 1 * s, 2.5 * s, 3.5 * s, (1, 1, 1), stroke=False)


def splash(c, x, y, q):
    for j in range(5):
        a = math.pi * (1.1 + 0.2 * j)
        ellipse(c, x + math.cos(a) * 40 * q, y + math.sin(a) * 40 * q + 30 * q * q, 6 * (1 - q) + 1, 6 * (1 - q) + 1, ICE_B, lw=2)


# ---------------- the frost drawing ----------------
DX0, DY0, DSC = 930, 535, 0.7


def _king_outline():
    raw = [(-150, 40), (-140, -60), (-100, -120), (-60, -140), (-210, -170), (-220, -150), (-70, -110),
           (-80, -170), (-60, -220), (0, -225), (60, -220), (80, -170), (70, -110), (220, -150), (210, -170),
           (60, -140), (100, -120), (140, -60), (150, 40)]
    return [(DX0 + px * DSC, DY0 + py * DSC) for px, py in raw]


def _king_crown():
    raw = [(-62, -205), (-70, -290), (-38, -240), (-20, -315), (0, -250), (20, -315), (38, -240), (70, -290), (62, -205)]
    return [(DX0 + px * DSC, DY0 + py * DSC) for px, py in raw]


CUBE = (742, 545, 46)     # running cube: x, y(bottom), size


def _cube_lines():
    x, y, s = CUBE
    return [[(x - s / 2, y), (x - s / 2, y - s), (x + s / 2, y - s), (x + s / 2, y), (x - s / 2, y)],
            [(x + s / 2 + 12, y - 30), (x + s / 2 + 52, y - 30)],
            [(x + s / 2 + 16, y - 16), (x + s / 2 + 62, y - 16)],
            [(x + s / 2 + 10, y - 4), (x + s / 2 + 40, y - 4)]]


STROKES = [_king_outline(), _king_crown()] + _cube_lines()


def _plen(pl):
    return sum(math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(pl, pl[1:]))


TOTAL_LEN = sum(_plen(p) for p in STROKES)


def draw_progress(t):
    return ease(seg(t, T_DRAW, T_DRAW_END)) if t < T_DRAW_END else 1.0


def pen_point(p):
    """Where the 'pen' is at progress p."""
    L = p * TOTAL_LEN
    for pl in STROKES:
        for a, b in zip(pl, pl[1:]):
            d = math.hypot(b[0] - a[0], b[1] - a[1])
            if L <= d:
                q = L / max(d, 1e-6)
                return lerp(a[0], b[0], q), lerp(a[1], b[1], q)
            L -= d
    return STROKES[-1][-1]


def frost_drawing(c, t):
    p = draw_progress(t) if t >= T_DRAW else 0.0
    if p <= 0:
        return
    L = p * TOTAL_LEN
    c.save(); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    if p >= 1:     # shadow fill once the outline is done
        a = ease(seg(t, T_DRAW_END - 0.1, T_DRAW_END + 0.5))
        for pl in STROKES[:2]:
            c.move_to(*pl[0])
            for q in pl[1:]:
                c.line_to(*q)
            c.close_path(); c.set_source_rgba(0.04, 0.1, 0.2, 0.55 * a); c.fill()
    for lw, col in [(14, (1, 1, 1, 0.8)), (7, (*ICE_D, 1))]:
        rem = L
        for pl in STROKES:
            if rem <= 0:
                break
            c.move_to(*pl[0])
            for a_, b_ in zip(pl, pl[1:]):
                d = math.hypot(b_[0] - a_[0], b_[1] - a_[1])
                if rem <= d:
                    q = rem / max(d, 1e-6)
                    c.line_to(lerp(a_[0], b_[0], q), lerp(a_[1], b_[1], q)); rem = 0; break
                c.line_to(*b_); rem -= d
            c.set_source_rgba(*col); c.set_line_width(lw); c.stroke()
    # the shadow's eyes glint
    if t >= T_GLINT:
        k = ease(seg(t, T_GLINT, T_GLINT + 0.3))
        for ex in (-22, 22):
            x, y = DX0 + ex * DSC, DY0 - 175 * DSC
            g = cairo.RadialGradient(x, y, 1, x, y, 30)
            g.add_color_stop_rgba(0, 0.7, 0.92, 1, 0.9 * k); g.add_color_stop_rgba(1, 0.7, 0.92, 1, 0)
            c.rectangle(x - 30, y - 30, 60, 60); c.set_source(g); c.fill()
            ellipse(c, x, y, 9 * k + 0.5, 4 * k + 0.5, ICE, stroke=False)
        if T_GLINT <= t < T_GLINT + 0.6:
            star(c, DX0 + 22 * DSC, DY0 - 175 * DSC, 22 * math.sin(math.pi * seg(t, T_GLINT, T_GLINT + 0.6)), t * 4, (1, 1, 1))
    c.restore()


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
        text(c, "Episode 15:", 0, 0, 60, (1, 1, 1), olw=10)
        text(c, "Something Is Melting", 0, 90, 76, GOLD, olw=12)
        c.restore()
    # drips falling down the card
    for i, (dx, t0) in enumerate([(250, 0.2), (820, 0.6), (520, 1.0), (360, 1.35)]):
        q = (t - t0) % 1.1
        if t >= t0:
            drop(c, dx, 150 + q * 1700, 2.2)
    # wet square footprints along the bottom
    for i in range(9):
        if t > 0.3 + i * 0.12:
            rrect(c, 120 + i * 95, 1820 - (14 if i % 2 else 0), 34, 24, 6)
            c.set_source_rgba(0.62, 0.85, 1.0, 0.95); c.fill_preserve(); c.set_source_rgb(*ICE_D); c.set_line_width(3); c.stroke()
    dill(c, 300, 1720, "angry", crown_on=False, arm="up", shake=2, look=(0.3, -1))
    c.save(); squash_at(c, 720, 1720, 1.0)
    crumb_bitten(c, 720, 1720, 1.0, mood="scared", look=(0, -1))
    c.restore()
    fat_peep(c, 720, 1720 - 292, FAT, mood="shock", face=0, look=(0, -1), wings="flap", flap_t=t)


# ---------------- character states ----------------
def light_at(t):
    return DIM


def drop_y(t, hit):
    """y of a falling drop that hits Dill's head at time hit (falls for 0.45s), or None."""
    if hit - 0.45 <= t < hit:
        q = seg(t, hit - 0.45, hit)
        return lerp(140, TOP - 290, q * q)
    return None


def dill_x(t):
    if t < T_FOLLOW:
        return DIX0
    if t < T_ARRIVE:
        p = seg(t, T_FOLLOW, T_ARRIVE)
        if p < 0.45:
            return lerp(DIX0, 728, ease(p / 0.45))
        if p < 0.62:
            return lerp(728, 652, ease((p - 0.45) / 0.17))
        return lerp(652, 815, ease((p - 0.62) / 0.38))
    if t < T_GRAB:
        return 815
    if t < T_PLONK + 0.3:
        return lerp(815, 700, ease(seg(t, T_GRAB, T_PLONK + 0.3)))
    if t < T_BACK:
        return 700
    if t < T_BACK + 0.6:
        return lerp(700, 455, ease(seg(t, T_BACK, T_BACK + 0.6)))
    return 455


def tiptoe(t):
    return T_FOLLOW <= t < T_ARRIVE


def dill_state(t):
    x = dill_x(t)
    sq = 1.0
    for d in DRIPS:
        if d <= t < d + 0.25:
            sq = lerp(0.9, 1.0, back_out(seg(t, d, d + 0.25)))
    if t < DRIPS[0]:
        return x, dict(mood="proud", look=(0.5, 0), arm="up", sq=sq)
    if t < DRIPS[1]:
        return x, dict(mood="frozen", look=(0, -1), arm="up", sq=sq)
    if t < DRIPS[2]:
        return x, dict(mood="angry", look=(0, -1), arm="up", sq=sq)
    if t < T_SPOT:
        return x, dict(mood="angry", look=(0, -1), arm="up", shake=4 if t >= T_FIST else 1, sq=sq,
                       rot=0.06 * math.sin(t * 22) if t >= T_FIST else 0)
    if t < T_FOLLOW:
        return x, dict(mood="smug", look=(1, 0.8), arm="down")
    if tiptoe(t):
        bob = math.sin((t - T_FOLLOW) * 7)
        p = seg(t, T_FOLLOW, T_ARRIVE)
        back = 0.45 <= p < 0.62
        return x, dict(mood="smug", look=(-1 if back else 1, 1), arm="down", sq=0.9 + 0.03 * bob, rot=0.05 * bob)
    if t < T_GRAB:
        return x, dict(mood="shocked", look=(1, 0.4), arm="down", shake=2 if t >= T_CHATTER else 0)
    if t < T_PLONK:
        return x, dict(mood="shocked", look=(-1, -1), arm="reach")
    if t < T_GASP:
        return x, dict(mood="smug", look=(1, 0.3), arm="down")
    if t < T_SOFT:
        return x, dict(mood="shocked", look=(1, 0.6), arm="down", shake=2 if t < T_GASP + 0.6 else 0)
    if t < T_CROSS:
        mood = "smug" if t < T_PANIC else "frozen"
        if T_TADA <= t < T_CROSS:
            mood = "smug"
        return x, dict(mood=mood, look=(1, 0.4), arm="down")
    if t < T_DRAW + 0.8:
        p = seg(t, T_CROSS, T_CROSS + 0.4)
        return x, dict(mood="smug", look=(-1, -0.4) if t < T_DRAW else (1, -0.3), arm="cross", rot=-0.05 * ease(p))
    if t < T_GLINT:
        return x, dict(mood="frozen", look=(1, -0.6), arm="cross")
    if t < T_RATTLE:
        return x, dict(mood="shocked", look=(1, -0.6), arm="down", shake=2)
    return x, dict(mood="shocked", look=(-0.2, -1), arm="reach" if t < T_HIDE + 0.6 else "down", shake=3)


def crumb_x(t):
    if t < T_FOLLOW + 0.5:
        return CRX0
    if t < T_ARRIVE + 0.4:
        return max(CRX0, dill_x(t - 0.5) - 150)
    if t < T_GRAB:
        return dill_x(T_ARRIVE - 0.1) - 150
    if t < T_PLONK:
        return lerp(665, 800, ease(seg(t, T_GRAB, T_PLONK)))
    if t < T_SOFT:
        return 800
    if t < T_HUG:
        return lerp(800, 830, ease(seg(t, T_SOFT, T_HUG)))
    if t < T_PANIC:
        return 830
    if t < T_PANIC + 0.3:
        return lerp(830, 790, ease(seg(t, T_PANIC, T_PANIC + 0.3)))
    if t < T_BACK:
        return 790
    if t < T_BACK + 0.6:
        return lerp(790, 585, ease(seg(t, T_BACK, T_BACK + 0.6)))
    return 585


def crumb_lift(t):
    """Height of Crumb above the shelf while Dill swings him over."""
    if T_GRAB <= t < T_PLONK:
        return 330 * math.sin(math.pi * ease(seg(t, T_GRAB, T_PLONK)))
    return 0.0


def crumb_sq(t):
    if T_PLONK <= t < T_PLONK + 0.3:
        return lerp(0.8, 1.0, back_out(seg(t, T_PLONK, T_PLONK + 0.3)))
    if T_MOP - 0.2 <= t < T_WRING:
        return lerp(1.0, 0.82, ease(seg(t, T_MOP - 0.2, T_MOP)))
    if T_WRING <= t < T_WRING + 0.3:
        return lerp(0.82, 1.0, ease(seg(t, T_WRING, T_WRING + 0.3)))
    if tiptoe(t):
        return 0.92 + 0.03 * math.sin((t - T_FOLLOW) * 7 + 1)
    return 1.0


def crumb_rot(t):
    if T_GRAB <= t < T_PLONK:
        return -1.2 * math.sin(math.pi * seg(t, T_GRAB, T_PLONK))
    if T_HUG - 0.2 <= t < T_PANIC:
        return 0.2 * ease(seg(t, T_HUG - 0.2, T_HUG + 0.2))
    if T_PANIC <= t < T_PANIC + 0.3:
        return 0.2 * (1 - ease(seg(t, T_PANIC, T_PANIC + 0.3)))
    if tiptoe(t):
        return 0.05 * math.sin((t - T_FOLLOW) * 7 + 1)
    return 0.0


def crumb_state(t):
    """kw for crumb_bitten (arm 'none' when the episode draws his arms)."""
    if t < DRIPS[2]:
        return dict(mood="worried", look=(1, -0.6))
    if t < T_SPOT:
        return dict(mood="scared", look=(1, -1))
    if t < T_FOLLOW:
        return dict(mood="worried", look=(1, 1), arm="none")
    if tiptoe(t):
        return dict(mood="worried", look=(1, 1))
    if t < T_GRAB:
        return dict(mood="scared", look=(1, 0.3), shake=2 if t >= T_CHATTER else 0)
    if t < T_TIP:
        return dict(mood="scared", look=(1, 0.5))
    if t < T_GASP:
        return dict(mood="scared", look=(1, 0.6), arm="none")
    if t < T_SOFT:
        return dict(mood="scared", look=(1, 0.8), shake=1.5 if t < T_GASP + 0.6 else 0)
    if t < T_HUG:
        return dict(mood="sheepish", look=(1, 0.8), arm="none")
    if t < T_MELT:
        return dict(mood="sheepish", look=(1, 0.8), arm="none")
    if t < T_PANIC:
        return dict(mood="sheepish" if t < T_MELT + 0.5 else "worried", look=(1, 0.9), arm="none")
    if t < T_TADA:
        return dict(mood="scared" if t < T_NAPKIN else "worried", look=(1, 1), arm="none")
    if t < T_DRAW:
        return dict(mood="sheepish", look=(1, 0.6) if t < T_CROSS else (1, -0.2))
    if t < T_GLINT:
        return dict(mood="worried", look=(1, -0.6))
    if t < T_RATTLE:
        return dict(mood="scared", look=(1, -0.8), shake=1.5)
    return dict(mood="scared", look=(-0.3, -1), shake=2)


def crumb_arms(t, x, sq, rot):
    """Hand targets for the custom-arm beats: list of (shoulder, hand)."""
    def shoulder(side):
        sx, sy = side * 70, -120 * sq
        ca, sa = math.cos(rot), math.sin(rot)
        return x + sx * ca - sy * sa, TOP + sx * sa + sy * ca
    if T_SPOT <= t < T_FOLLOW:      # points down at the prints
        return [(shoulder(-1), (x - 104, TOP - 76)), (shoulder(1), (x + 140, TOP - 40))]
    if T_TIP <= t < T_GASP:         # reaches for the top of the lid
        a = lid_ang(t)
        return [(shoulder(-1), (x - 104, TOP - 76)), (shoulder(1), (LID_X - 60 + 40 * math.sin(a), TOP - 170 * max(0.3, math.cos(a))))]
    if T_SOFT <= t < T_HUG:         # opens arms
        return [(shoulder(-1), (x - 130, TOP - 210)), (shoulder(1), (x + 130, TOP - 210))]
    if T_HUG <= t < T_PANIC:        # hug around Chip
        return [(shoulder(-1), (CHIP_X - 10, TOP - 70)), (shoulder(1), (CHIP_X + 58, TOP - 90))]
    if T_PANIC <= t < T_NAPKIN:     # hands up, panic
        return [(shoulder(-1), (x - 110, TOP - 240)), (shoulder(1), (x + 110, TOP - 240))]
    if T_NAPKIN <= t < T_TADA:
        return [(shoulder(-1), (x - 104, TOP - 76 * sq)), (shoulder(1), napkin_pos(t))]
    return []


def napkin_pos(t):
    if t < T_MOP:
        p = ease(seg(t, T_NAPKIN, T_MOP))
        return lerp(790 + 104, CHIP_X - 80, p), lerp(TOP - 76, TOP - 10, p)
    if t < T_WRING:
        q = (t - T_MOP) * 2.6
        return CHIP_X + 70 * math.sin(q * math.pi) - 10, TOP - 12
    p = ease(seg(t, T_WRING, T_WRING + 0.35))
    return lerp(CHIP_X - 10, CHIP_X - 10, p), lerp(TOP - 12, TOP - 250, p)


def chip_melt(t):
    m = 0.0
    if t >= T_MELT:
        m = 0.42 * ease(seg(t, T_MELT, T_MELT + 1.3))
    if t >= T_WRING + 0.35:
        m = lerp(0.42, 0.0, ease(seg(t, T_WRING + 0.35, T_TADA)))
    return m


def puddle_rx(t):
    r = 0.0
    if t >= T_MELT:
        r = 110 * ease(seg(t, T_MELT, T_MELT + 1.4))
    if t >= T_MOP:
        r = lerp(110, 10, ease(seg(t, T_MOP, T_WRING)))
    if t >= T_WRING:
        r = 0.0
    return r


def chip_pos(t):
    """(x, y) feet of Chip."""
    if t < T_DRAW:
        if T_COWER <= t < T_COWER + 0.4:
            return CHIP_X + 25 * ease(seg(t, T_COWER, T_COWER + 0.4)), TOP
        if t < T_COWER:
            return CHIP_X, TOP
        if t < T_SOFT:
            return CHIP_X + 25, TOP
        return lerp(CHIP_X + 25, CHIP_X, ease(seg(t, T_SOFT, T_SOFT + 0.4))), TOP
    if t < T_DRAW_END + 0.4:
        p = draw_progress(t)
        px, py = pen_point(p)
        x = min(max(px + 95, 820), 1005)
        reach = max(0, TOP - 140 * CHS - py)
        tt = t - T_DRAW
        y = TOP - reach * abs(math.sin(tt * 5.0)) if reach > 10 else TOP
        if t >= T_DRAW_END:
            q = ease(seg(t, T_DRAW_END, T_DRAW_END + 0.4))
            x = lerp(x, CHIP_X, q); y = TOP
        return x, y
    if t < T_HIDE:
        return CHIP_X, TOP
    if t < T_HIDE + 0.5:
        p = seg(t, T_HIDE, T_HIDE + 0.5)
        return hop((CHIP_X, TOP), (610, TOP), ease(p), 90)
    if t < T_FIND - 0.4:
        return 610, TOP
    return lerp(610, 715, ease(seg(t, T_FIND - 0.4, T_FIND))), TOP


def chip_state(t):
    melt = chip_melt(t)
    base = dict(melt=melt, t=t)
    if t < T_GASP:
        return dict(base, mood="scared", look=(-1, 0), shiver=1.0)
    if t < T_COWER:
        return dict(base, mood="eep", look=(-1, 0), arms="out", shiver=0.6)
    if t < T_SOFT:
        return dict(base, mood="scared", look=(-1, 0), arms="cover", shiver=1.0)
    if t < T_HUG:
        return dict(base, mood="scared", look=(-1, -0.4), shiver=0.5)
    if t < T_PANIC:
        bl = ease(seg(t, T_HUG + 0.2, T_MELT))
        return dict(base, mood="happy", blush=bl)
    if t < T_WRING + 0.35:
        return dict(base, mood="happy", blush=1.0)
    if t < T_TADA + 0.6:
        return dict(base, mood="happy", arms="up", blush=0.6)
    if t < T_SHIV:
        return dict(base, mood="shy", look=(-1, 0))
    if t < T_GIGGLE:
        return dict(base, mood="scared" if t < T_PCOPY + 0.4 else "shy", look=(-1, 0), shiver=1.0)
    if t < T_DRAW:
        return dict(base, mood="giggle", arms="cover" if t < T_GIGGLE + 1.0 else "down")
    if t < T_DRAW_END:
        px = pen_point(draw_progress(t))[0]
        return dict(base, mood="shy", look=(-0.5, -1), arms="draw" if px > chip_pos(t)[0] else "draw_l")
    if t < T_RATTLE:
        return dict(base, mood="scared", look=(-1, -0.3), shiver=0.6)
    if t < T_FIND - 0.4:
        return dict(base, mood="scared", look=(0, -1), shiver=1.0, arms="cover")
    return dict(base, mood="scared", look=(-0.6, -1), shiver=1.0)


def perch(t):
    """Top of Crumb's head (where Peep rides)."""
    x = crumb_x(t)
    sq = crumb_sq(t)
    rot = crumb_rot(t)
    h = 300 * sq - 14
    return x + math.sin(rot) * h, TOP - crumb_lift(t) - math.cos(rot) * h


def peep_state(t):
    if t < T_PDOWN:
        x, y = perch(t)
        if t < DRIPS[2]:
            return x, y, dict(mood="happy", face=0, look=(1, -0.5))
        if t < T_SPOT:
            return x, y, dict(mood="shock", face=0, look=(0, -1), wings="flap", flap_t=t)
        if tiptoe(t):
            return x, y, dict(mood="blink" if (t * 2) % 1 < 0.1 else "happy", face=0.5, look=(1, 1),
                              rot=0.08 * math.sin((t - T_FOLLOW) * 7 + 1))
        if T_GRAB <= t < T_PLONK + 0.3:
            return x, y, dict(mood="shock", face=0, wings="flap", flap_t=t * 2)
        if T_GASP <= t < T_COWER + 0.5:
            return x, y - 20 * math.sin(math.pi * seg(t, T_GASP, T_GASP + 0.3)), dict(mood="shock", face=0.5, look=(1, 1))
        if T_HUG <= t < T_PANIC:
            return x, y, dict(mood="love", face=0.4, flap_t=t)
        return x, y, dict(mood="happy", face=0.5, look=(1, 0.8))
    spot = (735, TOP)
    if t < T_PDOWN + 0.5:
        x, y = hop(perch(T_PDOWN), spot, ease(seg(t, T_PDOWN, T_PDOWN + 0.5)), 120)
        return x, y, dict(mood="happy", face=0.5, wings="flap", flap_t=t * 2)
    if t < T_PCOPY:
        return spot[0], spot[1], dict(mood="happy", face=0.6, look=(1, 0))
    if t < T_GIGGLE + 0.3:
        return spot[0], spot[1], dict(mood="shock", face=0.3, look=(1, -0.3), shake=12, wings="flap", flap_t=t * 4)
    if t < T_PUP:
        return spot[0], spot[1], dict(mood="proud" if t < T_GIGGLE + 1.0 else "happy", face=0.4, look=(1, 0))
    if t < T_PUP + 0.5:
        x, y = hop(spot, perch(T_PUP + 0.5), ease(seg(t, T_PUP, T_PUP + 0.5)), 140)
        return x, y, dict(mood="happy", face=-0.3, wings="flap", flap_t=t * 2)
    x, y = perch(t)
    if t < T_GLINT:
        return x, y, dict(mood="happy", face=0.5, look=(1, -0.6))
    return x, y, dict(mood="shock", face=0.3, look=(0.5, -1), shake=3)


def lid_ang(t):
    if t < T_TIP:
        return 0.0
    p = seg(t, T_TIP, T_CLANG)
    a = (math.pi / 2) * p * p
    if t >= T_CLANG:
        a = math.pi / 2 - 0.12 * abs(math.sin((t - T_CLANG) * 18)) * max(0, 1 - (t - T_CLANG) * 3)
    return a


def lid_shake(t):
    if T_CHATTER <= t < T_TIP:
        return 5 * math.sin(t * 60)
    return 0.0


def pickle_kw(k, t):
    look, mood = (1, -0.3), "calm"
    if t >= T_GASP and t < T_GASP + 1.4:
        mood = "shock"
    if t >= T_GLINT:
        mood = "shock"
        look = (0.5, -1) if t >= T_RATTLE else (1, -0.3)
    if T_FOLLOW <= t < T_GASP:
        mood = "closed"
    return dict(look=look, mood=mood)


def gran_kw(t):
    if T_FOLLOW <= t < T_GASP:
        return dict(look=(1, 0), mood="closed", cane="down")
    if t >= T_RATTLE:
        return dict(look=(0.6, -1), mood="stern", cane="up")
    return dict(look=(1, -0.3), mood="stern", cane="down")


def duck_tilt(t):
    return lerp(0.36, -0.12, ease(seg(t, T_DUCK + 0.15, T_DUCK + 0.85)))


def duck_gaze(t):
    return ease(seg(t, T_DUCK + 0.5, T_DUCK + 1.0))


def beam_x(t):
    if t < T_BEAM:
        return None
    keys = [(T_BEAM, 120), (T_BEAM + 0.9, 980), (T_BEAM + 1.7, 300), (T_FIND - 0.3, 780), (T_FIND, 715)]
    for a, b in zip(keys, keys[1:]):
        if t < b[0]:
            return lerp(a[1], b[1], ease(seg(t, a[0], b[0])))
    return 715 + 6 * math.sin(t * 3)


# ---------------- camera ----------------
KEYS = [(T_START, 590, 430, 2.2), (DRIPS[1], 590, 430, 2.2), (DRIPS[2], 580, 450, 2.35), (T_FIST + 0.4, 560, 460, 2.0),
        (T_SPOT + 0.3, 600, 500, 1.75), (T_FOLLOW, 640, 500, 1.8),
        (T_FOLLOW + 2.0, 700, 480, 1.85), (T_ARRIVE, 800, 470, 1.85), (T_GRAB, 800, 440, 1.6), (T_PLONK, 820, 440, 1.6),
        (T_TIP, 860, 480, 1.9), (T_GASP + 0.2, 890, 500, 2.2), (T_SOFT, 890, 500, 2.2), (T_HUG + 0.4, 880, 510, 2.35),
        (T_PANIC, 880, 500, 2.25), (T_MOP, 900, 530, 2.3), (T_WRING, 900, 500, 2.2), (T_TADA + 0.2, 880, 490, 2.1),
        (T_PDOWN + 0.6, 840, 500, 2.0), (T_PCOPY, 850, 510, 2.15), (T_GIGGLE + 0.5, 850, 510, 2.1),
        (T_CROSS + 0.3, 540, 470, 2.0), (T_PUP, 560, 470, 1.95), (T_DRAW + 0.3, 820, 440, 1.6), (T_DRAW_END, 820, 440, 1.6),
        (T_DUCK, 820, 440, 1.6), (T_DUCK + 0.3, JAR_X + 40, TOP - 420, 2.5), (T_DUCK_END - 0.25, JAR_X + 40, TOP - 420, 2.5),
        (T_DUCK_END, 800, 450, 1.65), (T_GLINT + 0.6, 800, 450, 1.65), (T_RATTLE, 800, 460, 1.65),
        (T_RATTLE + 0.5, 640, 520, 1.6), (T_FIND - 0.3, 640, 520, 1.6), (T_FIND + 0.3, 690, 560, 2.4), (END_T, 700, 570, 2.7)]


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
    hw = 540 / z
    cx = min(max(cx, hw), W - hw)
    for t0, s in [(T_CLANG, 7), (T_RATTLE, 6), (T_RATTLE + 0.5, 4), (T_PLONK, 5)]:
        if t0 <= t < t0 + 0.25:
            q = s * (1 - seg(t, t0, t0 + 0.25)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    for d in DUNS:
        if d <= t < d + 0.12:
            z += 0.12 * (1 - seg(t, d, d + 0.12))
    return cx, cy, z


# ---------------- scene ----------------
def vent_shake(t):
    if T_RATTLE <= t < T_FIND + 0.5:
        return 6 * math.sin(t * 55), 3 * math.sin(t * 41)
    return 0, 0


def draw_gran(c, t):
    kw = gran_kw(t)
    c.save(); c.translate(GRX, TOP); c.scale(GSC, GSC); c.translate(-GRX, -TOP)
    grandma(c, GRX, TOP, **kw)
    c.restore()
    crown(c, GRX + GRAN_HEAD[0], TOP + GRAN_HEAD[1] + 10 * GSC - 10 * GSC, 0.72, -0.2)


def draw_crumb(c, t):
    x = crumb_x(t)
    sq = crumb_sq(t)
    rot = crumb_rot(t)
    lift = crumb_lift(t)
    kw = crumb_state(t)
    arm = kw.get("arm", "down")
    c.save(); c.translate(0, -lift)
    c.save(); squash_at(c, x, TOP, sq)
    crumb_bitten(c, x, TOP, 1.0, rot=rot, **kw)
    c.restore()
    c.restore()
    return x, sq, rot, arm


def draw_crumb_arms(c, t, x, sq, rot):
    c.save(); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_source_rgb(*INK); c.set_line_width(9)
    for (s, h) in crumb_arms(t, x, sq, rot):
        c.move_to(*s); c.line_to(*h); c.stroke()
    c.restore()


def scene(c, t):
    L = light_at(t)
    fridge6(c, L, 1, lid=False)
    frost(c, t, 1.0)
    frost_drawing(c, t)
    ceiling(c, L)
    vx, vy = vent_shake(t)
    c.save(); c.translate(vx, vy)
    ceiling_vent(c, L)
    glow = 0.0
    if t >= T_RATTLE - 0.3:
        glow = min(1, seg(t, T_RATTLE - 0.3, T_RATTLE)) * (0.75 + 0.25 * math.sin(t * 9))
    vent_glow(c, glow)
    c.restore()

    shell_half(c, 1035, TOP - 70, 0.0, top=False)
    puddle(c, VENT_X + 30, TOP, 70)                                  # meltwater under the vent
    bread_bit(c, 690, TOP - 8, 2.6)
    footprints(c, t)

    # the Duck sits in the mouth of the open Jar
    clean_duck(c, JAR_X, TOP - 322, tilt=duck_tilt(t), gaze=duck_gaze(t), frosty=1.0, s=0.78)
    for k in (0, 1, 4, 2):
        x = PK_X[k]
        c.save(); c.translate(x, TOP); c.scale(PS, PS); c.translate(-x, -TOP)
        kw = pickle_kw(k, t)
        sh = 3 * math.sin(t * 50 + k) if t >= T_GLINT else 0
        pickle_kid(c, x + sh, TOP, k, **kw)
        c.restore()
    draw_gran(c, t)

    # the lid (Chip hides behind it until it tips)
    a = lid_ang(t)
    standing = a < 0.6
    cx_, cy_ = chip_pos(t)
    ckw = chip_state(t)
    hidden_behind_crumb = T_HIDE + 0.25 <= t
    if standing:
        if t >= T_CHATTER - 0.6:
            chip(c, cx_, cy_, CHS, **ckw)
        lid_standing(c, LID_X + lid_shake(t), a)
    else:
        lid_standing(c, LID_X, a)
        puddle(c, cx_, TOP, puddle_rx(t))
        if hidden_behind_crumb:
            chip(c, cx_, cy_, CHS, **ckw)

    # Dill / Crumb (Dill is behind Crumb while swinging him over)
    dx, dkw = dill_state(t)
    swinging = T_GRAB <= t < T_PLONK
    if not swinging:
        dill(c, dx, TOP, crown_on=False, **dkw)
    x, sq, rot, arm = draw_crumb(c, t)
    if swinging:
        dill(c, dx, TOP, crown_on=False, **dkw)
    if not standing and not hidden_behind_crumb:
        chip(c, cx_, cy_, CHS, **ckw)
    if arm == "none":
        draw_crumb_arms(c, t, x, sq, rot)
    # napkin
    if T_NAPKIN <= t < T_TADA:
        nx, ny = napkin_pos(t)
        if t < T_WRING:
            napkin_folded(c, nx, ny + 10, 0.75)
        else:
            c.save(); c.translate(nx, ny); c.rotate(math.pi / 2 + 0.3 * math.sin(t * 20))
            napkin_folded(c, 0, 14, 0.7); c.restore()
            for j in range(4):           # wrung-out drops falling back onto Chip
                q = ((t - T_WRING - 0.3) * 2.2 + j * 0.25) % 1
                if t > T_WRING + 0.3:
                    drop(c, nx + (j - 1.5) * 10, lerp(ny + 50, TOP - 120 * CHS * (1 - chip_melt(t) * 0.55), q), 1.0)
    # Peep
    px, py, pkw = peep_state(t)
    fat_peep(c, px, py, FAT, **pkw)

    # ---------------- effects ----------------
    for d in DRIPS:
        y = drop_y(t, d)
        if y is not None:
            drop(c, DIX0 + 10, y, 1.3)
        if d <= t < d + 0.35:
            splash(c, DIX0 + 10, TOP - 290, seg(t, d, d + 0.35))
        word(c, t, "plip", DIX0 + 150 + 30 * DRIPS.index(d), TOP - 300 - 40 * DRIPS.index(d), 50, ICE, d, d + 0.6, 0.1)
    word(c, t, "!?", DIX0 - 10, TOP - 360, 70, (1, 0.35, 0.35), DRIPS[1] + 0.15, DRIPS[2] - 0.1)
    word(c, t, "GRRR", DIX0 + 170, TOP - 330, 64, (1, 0.35, 0.35), T_FIST, T_SPOT, 0.08)
    word(c, t, "!", CRX0 + 130, TOP - 400, 90, (1, 0.9, 0.4), T_SPOT, T_FOLLOW)
    if T_SPOT <= t < T_FOLLOW:     # sparkle along the trail
        q = seg(t, T_SPOT, T_FOLLOW)
        i = int(q * len(PRINTS))
        if i < len(PRINTS):
            star(c, PRINTS[i][0], PRINTS[i][1] - 4, 16, t * 5, (1, 1, 1))
    if tiptoe(t):
        for j in range(3):
            q = ((t - T_FOLLOW) * 0.7 + j / 3) % 1
            word(c, t, "?", dill_x(t) + 60 + 30 * j, TOP - 360 - 60 * q, 46, (1, 1, 1), T_FOLLOW + 0.3, T_ARRIVE, 0.1 * j - 0.1)
            break
        word(c, t, "tip", dill_x(t) - 60, TOP + 90, 40, (1, 1, 1), T_FOLLOW + 0.4, T_FOLLOW + 1.0, -0.1)
        word(c, t, "toe", dill_x(t) + 20, TOP + 90, 40, (1, 1, 1), T_FOLLOW + 1.1, T_FOLLOW + 1.7, 0.1)
        word(c, t, "tip", dill_x(t) - 60, TOP + 90, 40, (1, 1, 1), T_FOLLOW + 2.6, T_FOLLOW + 3.2, -0.1)
        word(c, t, "toe", dill_x(t) + 20, TOP + 90, 40, (1, 1, 1), T_FOLLOW + 3.3, T_FOLLOW + 3.9, 0.1)
    word(c, t, "chk chk chk", LID_X - 10, TOP - 230, 40, ICE, T_CHATTER, T_TIP, 0.06)
    word(c, t, "CLANG!", LID_X + 10, TOP - 200, 66, (1, 0.9, 0.4), T_CLANG, T_CLANG + 0.4, 0.1)
    word(c, t, "GASP!", 700, TOP - 470, 62, (1, 1, 1), T_GASP + 0.25, T_GASP + 1.0, -0.08)
    word(c, t, "eep!", CHIP_X + 50, TOP - 250, 56, ICE, T_GASP + 0.3, T_COWER + 0.4, 0.12)
    word(c, t, "brrr", CHIP_X + 60, TOP - 230, 40, ICE, T_COWER + 0.4, T_SOFT, 0.1)
    if T_HUG + 0.2 <= t < T_PANIC:
        for j in range(4):
            q = ((t - T_HUG) * 0.8 + j / 4) % 1
            heart(c, CHIP_X - 60 + 40 * j, TOP - 200 - 160 * q, 1.2, 1 - q)
    word(c, t, "drip", CHIP_X + 90, TOP - 150, 40, ICE, T_MELT + 0.3, T_MELT + 0.9, 0.1)
    word(c, t, "drip", CHIP_X - 120, TOP - 120, 40, ICE, T_MELT + 0.9, T_MELT + 1.5, -0.1)
    word(c, t, "!!", 860, TOP - 420, 80, (1, 0.35, 0.35), T_PANIC, T_NAPKIN + 0.3)
    for j in range(3):
        word(c, t, "squeak", CHIP_X - 110 + 120 * (j % 2), TOP - 200 - 30 * (j % 2), 40, (1, 1, 1),
             T_MOP + 0.45 * j, T_MOP + 0.45 * j + 0.4, -0.1 + 0.1 * (j % 2))
    word(c, t, "ta-da!", CHIP_X + 20, TOP - 260, 54, GOLD, T_TADA, T_TADA + 0.8, 0.08)
    if T_TADA <= t < T_TADA + 0.6:
        q = seg(t, T_TADA, T_TADA + 0.6)
        for j in range(6):
            a_ = -math.pi * j / 5
            star(c, CHIP_X + math.cos(a_) * 120 * q, TOP - 70 + math.sin(a_) * 120 * q, 18 * (1 - q), t * 6, (1, 1, 1))
    word(c, t, "brrr", CHIP_X + 70, TOP - 220, 40, ICE, T_SHIV, T_PCOPY, 0.1)
    word(c, t, "BRRRR!", 735, TOP - 300, 62, ICE, T_PCOPY + 0.1, T_PCOPY + 0.7, -0.1)
    word(c, t, "BRRRRR!", 735, TOP - 320, 70, ICE, T_PCOPY + 0.7, T_GIGGLE + 0.3, 0.08)
    if T_PCOPY <= t < T_GIGGLE + 0.3:      # fluff flying off
        for j in range(5):
            q = ((t - T_PCOPY) * 1.6 + j / 5) % 1
            ellipse(c, 735 + (j - 2) * 50 * q * 2, TOP - 150 - 120 * q, 9, 7, (1, 0.96, 0.7), lw=2)
    word(c, t, "hee hee", CHIP_X + 50, TOP - 240, 40, (1, 1, 1), T_GIGGLE, T_GIGGLE + 1.0, 0.1)
    word(c, t, "hmph!", 470 + 40, TOP - 390, 56, (1, 1, 1), T_CROSS + 0.2, T_CROSS + 1.2, -0.1)
    for j in range(3):
        word(c, t, "scritch", 980 - 80 * (j % 2), 300 + 50 * j, 38, (1, 1, 1), T_DRAW + 0.2 + 1.0 * j, T_DRAW + 0.8 + 1.0 * j, 0.1)
    word(c, t, "squeak", JAR_X + 150, TOP - 520, 44, (1, 1, 1), T_DUCK + 0.2, T_DUCK + 1.0, 0.1)
    word(c, t, "brrr", 700, TOP - 450, 50, ICE, T_GLINT + 0.3, T_RATTLE, -0.08)
    if t >= T_RATTLE:
        word(c, t, "RATTLE", VENT_X - 300, 230, 56, (1, 0.9, 0.4), T_RATTLE, T_RATTLE + 0.6, -0.12)
        word(c, t, "RATTLE", VENT_X + 300, 250, 56, (1, 0.9, 0.4), T_RATTLE + 0.3, T_RATTLE + 0.9, 0.12)
        for j in range(10):     # frost dust shaken down
            q = ((t - T_RATTLE) * 0.9 + j / 10) % 1
            ellipse(c, VENT_X - 140 + 30 * j, 140 + 500 * q, 5, 5, (1, 1, 1), stroke=False)
    dark_overlay(c, L)
    # searchlight from the vent (drawn after the dark overlay: it's light)
    bx = beam_x(t)
    if bx is not None:
        k = ease(seg(t, T_BEAM, T_BEAM + 0.3))
        c.move_to(VENT_X - 70 + vx, 125); c.line_to(VENT_X + 70 + vx, 125); c.line_to(bx + 120, TOP + 20); c.line_to(bx - 120, TOP + 20)
        c.close_path(); c.set_source_rgba(0.62, 0.88, 1.0, 0.26 * k); c.fill()
        c.save(); c.translate(bx, TOP + 12); c.scale(125, 22); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(0.8, 0.95, 1.0, 0.45 * k); c.fill()
    for i, s in enumerate(SNIFFS):
        word(c, t, "sniff...", VENT_X + (170 if i else -170), 230 + 40 * i, 60, ICE, s, s + 0.8, 0.1 if i else -0.1)


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
    if t >= T_FIND:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.3, 0.6, 1.0, 0.12 * ease(seg(t, T_FIND, T_FIND + 0.5))); c.fill()
    if t >= END_T - 0.4:
        cx, cy, Z = camera(t)
        iris(c, W / 2 + (715 - cx) * Z, H / 2 + (TOP - 80 - cy) * Z, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))


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
