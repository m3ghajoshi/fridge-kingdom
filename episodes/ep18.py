"""FRIDGE KINGDOM — Episode 18: "The Squeak Strategy". 40.0s, 1080x1920 @ 30fps.

Variant B (cold open): the first frame is mid-action; a small title banner sits across the top for the first 2s.

The plan from Ep 17: squeak the Duck, the Hand comes, ride the Hand to the freezer. The Duck sits on top of the jello.
Crumb leaps onto it: THUD, nothing (crickets). Peep bounces on it three times: nothing. The five Jar pickles jump
down from the top shelf and pile onto it: nothing, and the pile topples. Grandma Gherkin pokes it with her cane
(tok tok tok): nothing. Dill does his Ep 5 dance at it: nothing; record scratch.
Everyone gives up and flops down. Silence... Then the Duck squeaks all by itself (its one motion: a squash).
Footsteps. The door opens (choir in a minor key); the Hand reaches in and boops the Duck. HYAAA: Dill, Crumb,
Chip and Peep leap onto the Hand's cuff; it lifts them away.
Outside: the Hand opens the TOP door instead: the freezer. A blizzard of cold light. Close-up on the cuff in the
wind: Crumb hangs on by one corner, slips, and they all tumble off into the white. The freezer door SLAMS.
Total white. A small "peep?" echoes. Two tiny eyes blink in the snow... and behind them, a huge icy eye opens.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crown, dark_overlay, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp,
                 back_out, INK, GOLD, TOP, FLOOR, W, H, FPS, S)
from ep2 import end_card, jello
from ep6 import grandma, fridge6, pickle_kid
from ep7 import god_rays, sq_rings
from ep5 import music_note
from ep9 import fat_peep, crumb_bitten, GRAN_HEAD
from ep10 import ceiling_vent, frost, carton, hand_cuffed
from ep12 import word, hop
from ep13 import ceiling
from ep14 import clean_duck
from ep15 import chip, drop, frost_drawing
from ep16 import butter_rink, plate, keyed, DISH
from ep17 import scarf, cape, cape_tie, parka

DUR = 40.0
END_T = 38.5
DIM = 0.18
FAT = 1.5
GSC = 1.35
CHS = 1.3
PKS = 1.2
ICE = hexc("#D0EBFF")
ICE_B = hexc("#74C0FC")
SNOW = hexc("#F8FCFF")
RED = (1, 0.35, 0.35)

# ---------------- timing ----------------
T_CLAND = 0.45                    # Crumb lands on the Duck
T_CSLIDE = 2.0                    # slides off
T_CBACK = 2.5
T_PHOP = 2.6                      # Peep hops up
T_PLAND = 3.1
P_BOUNCE = (3.1, 3.6, 4.1)        # boing x3
T_PHOPOFF = 5.0
T_PBACK = 5.5
PK_JUMP = [6.0, 6.3, 6.6, 6.9, 7.2]
PK_FALL = 0.35
T_TOPPLE = 8.3                    # the pile topples
GPOKES = (9.3, 9.7, 10.1)
T_HMPH = 10.45
T_DANCE = 10.9
T_SCRATCH = 12.95
T_FLOP = 13.5                     # everyone gives up and lies down
T_SQUEAK = 16.8                   # the Duck squeaks all by itself
T_UP = 17.05
STEPS = (17.9, 18.5, 19.1)
T_OPEN = 19.6
T_HDOWN = 20.0
T_HSET = 20.8
T_CHARGE = 20.45
T_BOOP = 21.0
T_LEAP = 21.05
T_GRAB = 21.65
T_LIFT = 22.0
T_EXT = 22.6                      # cut outside
T_MCLOSE = 23.1
T_RISE = 23.2
T_GRIP = 24.15
T_FOPEN = 24.35
T_FOPENED = 25.0
T_REACH = 25.3
T_CU = 26.0                       # close-up on the cuff in the blizzard
T_SLIP = 28.3
T_FALL = 28.75
T_EXT2 = 30.5
T_SLAM = 31.3
T_WHITE = 32.3
PEEPS = (33.4, 34.3, 35.1)
T_EYES = 35.8
T_BIGEYE = 36.5
DUNS = (37.0, 37.4, 37.8)

# ---------------- layout ----------------
JX = 985                          # jello; the Duck sits on top
DUCK_S = 0.78
DY = FLOOR - 146                  # the Duck's base
DTOP = DY - 100                   # feet height standing on the Duck's head
CHX, PEX, CRX, DIX, GRX = 230, 405, 580, 745, 880
PK_TOP = [880, 925, 970, 1015, 1058]                       # Jar pickles on the top shelf
PK_PILE = [(935, DTOP + 18), (1035, DTOP + 18), (985, DTOP - 10), (955, DTOP - 190), (1020, DTOP - 196)]
PK_FLOOR = [(905, 0.0), (1050, 0.0), (780, 0.0), (840, 0.0), (1010, 0.0)]
HX = 820                          # the Hand inside the fridge
HTIP = FLOOR - 330

# exterior fridge
FX0, FX1 = 170, 910
FTOP, FZB = 300, 790              # freezer door
MTOP, MBOT = 815, 1760            # main door
KFLOOR = 1790


def rot_at(c, x, y, a):
    c.translate(x, y); c.rotate(a); c.translate(-x, -y)


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
    text(c, "Ep. 18:  The Squeak Strategy", W / 2, 182, 46, (1, 1, 1), olw=8)
    c.restore()


# ---------------- light ----------------
def light_at(t):
    if t < T_OPEN:
        return DIM
    return lerp(DIM, 1.0, ease(seg(t, T_OPEN, T_OPEN + 0.4)))


def hand_pos(t):
    """Inside the fridge: (x, tip_y, grip)."""
    if t < T_HDOWN:
        return HX, -700, 0.0
    if t < T_LIFT:
        y = lerp(-700, HTIP, ease_out(seg(t, T_HDOWN, T_HSET)))
        boop = 22 * math.sin(math.pi * seg(t, T_BOOP - 0.15, T_BOOP + 0.15)) if T_BOOP - 0.15 <= t < T_BOOP + 0.15 else 0
        return HX + 0.4 * boop, y + boop, 0.3
    return HX, HTIP - 1900 * ease(seg(t, T_LIFT, T_EXT)) ** 1.5, 0.3


# ---------------- team on the Hand ----------------
# feet positions relative to the fingertip (hand-space, scale 1)
ON_HAND = {"dill": (-30, -425), "peep": (85, -425), "chip": (178, -150), "crumb_pivot": (-150, -215)}


def team_on_hand(c, t, hx, tip, s, wind=0.0, falling=None):
    """Dill hugs the top of the cuff, Peep sits beside him, Chip hugs the thumb, Crumb hangs by one corner off the
    side of the palm. falling: dict name -> (dx, dy, rot) extra offsets (screen units, already scaled)."""
    falling = falling or {}
    sh = wind
    c.save(); c.translate(hx, tip); c.scale(s, s)
    # Crumb, hanging by his top-right corner
    if "crumb" not in falling:
        px, py = ON_HAND["crumb_pivot"]
        sw = 0.25 * math.sin(t * 5.0) + 0.3 * sh * math.sin(t * 13)
        c.save(); c.translate(px, py); c.rotate(0.15 + sw)
        draw_crumb(c, t, -85, 270, dict(mood="scared", look=(1, -1), shake=2 * sh, arm="wave"))
        c.restore()
    if "dill" not in falling:
        x, y = ON_HAND["dill"]
        c.save(); rot_at(c, x, y, -0.12 + 0.05 * math.sin(t * 9) * sh)
        draw_dill(c, t, x, y, dict(mood="shocked", look=(0, 1), arm="reach", shake=2 * sh))
        c.restore()
    if "peep" not in falling:
        x, y = ON_HAND["peep"]
        fat_peep(c, x, y + 4, FAT, mood="shock" if sh > 0.3 else "happy", face=0.4, look=(1, 1), wings="flap", flap_t=t,
                 rot=0.1 * math.sin(t * 11) * sh)
    if "chip" not in falling:
        x, y = ON_HAND["chip"]
        cape(c, x, y, CHS, sway=0.5 + 0.8 * sh * math.sin(t * 12))
        chip(c, x, y, CHS, mood="eep", look=(-1, -0.5), arms="up", shiver=0.6 + sh, t=t)
        cape_tie(c, x, y - 6, CHS)
    c.restore()


# ---------------- character draw helpers (with costumes) ----------------
def draw_dill(c, t, x, y, kw, hood=0.0):
    kw = dict(kw)
    dill(c, x, y, crown_on=False, **kw)
    parka(c, x, y, hood, kw.get("rot", 0.0), t)


def draw_crumb(c, t, x, y, kw):
    crumb_bitten(c, x, y, 1.0, **kw)
    scarf(c, x, y, 0.0, flap=math.sin(t * 4))


def draw_chip(c, t, x, y, kw):
    cape(c, x, y, CHS, sway=0.5 * math.sin(t * 3))
    chip(c, x, y, CHS, t=t, **kw)
    cape_tie(c, x, y - 6, CHS)


def draw_grandma(c, x, y, kw):
    hop_ = kw.get("hop", 0.0)
    c.save(); c.translate(x, y); c.scale(GSC, GSC); c.translate(-x, -y)
    grandma(c, x, y, **kw)
    c.restore()
    crown(c, x + GRAN_HEAD[0], y + GRAN_HEAD[1] - hop_ * GSC, 0.72, -0.2)


# ---------------- flop / pop-up helpers ----------------
def flop_k(t):
    """0 = standing, 1 = lying flat."""
    if t < T_FLOP:
        return 0.0
    if t < T_SQUEAK + 0.2:
        return ease(seg(t, T_FLOP, T_FLOP + 0.4))
    return 1 - back_out(seg(t, T_SQUEAK + 0.2, T_UP + 0.15))


def lie(c, x, y, k, side, thick):
    """Rotate a character about its feet so it lies on the floor (side -1 = falls to the left)."""
    a = side * 1.45 * k
    c.translate(x, y - thick * abs(math.sin(a))); c.rotate(a); c.translate(-x, -y)


def look_right(t):
    return t >= STEPS[0] - 0.1


# ---------------- states ----------------
def crumb_state(t):
    """(x, y, kw, squash)"""
    if t < T_CLAND:
        p = seg(t, -0.25, T_CLAND)
        x = lerp(760, JX, p)
        y = lerp(DTOP - 60, DTOP, p) - 140 * math.sin(math.pi * p)
        return x, y, dict(mood="scared", look=(1, 1), arm="wave", rot=0.25 * (1 - p)), 1.0
    if t < T_CSLIDE:
        sq = 1 - 0.25 * math.sin(math.pi * seg(t, T_CLAND, T_CLAND + 0.25)) if t < T_CLAND + 0.25 else 1.0
        bob = 10 * math.sin(math.pi * seg(t, 1.2, 1.5)) if 1.2 <= t < 1.5 else 0
        return JX, DTOP - bob, dict(mood="worried", look=(0, 1) if t < 1.6 else (-1, 0), arm="wave_l" if 1.15 < t < 1.6 else "down"), sq
    if t < T_CBACK:
        p = seg(t, T_CSLIDE, T_CBACK)
        return lerp(JX, 860, p), lerp(DTOP, FLOOR, ease(p)), dict(mood="sheepish", look=(-1, 0), rot=-0.35 * math.sin(math.pi * p)), 1.0
    if t < 3.3:
        p = ease(seg(t, T_CBACK, 3.3))
        return lerp(860, CRX, p), FLOOR - 14 * abs(math.sin(p * 9)), dict(mood="sheepish", look=(-1, 0)), 1.0
    return CRX, FLOOR, common_kw(t, "crumb"), 1.0


def common_kw(t, who):
    """Shared reactions for whoever is standing around."""
    if T_UP <= t < STEPS[0]:
        return dict(crumb=dict(mood="scared", look=(1, -1)), peep=dict(mood="shock", face=0.5, look=(1, -1)),
                    chip=dict(mood="eep", look=(1, -1), arms="out"), dill=dict(mood="shocked", look=(1, -0.5)))[who]
    if look_right(t) and t < T_CHARGE:
        sc = 2 if any(s <= t < s + 0.25 for s in STEPS) else 0
        return dict(crumb=dict(mood="scared", look=(1, -0.6), shake=sc), peep=dict(mood="shock", face=0.7, look=(1, -1)),
                    chip=dict(mood="scared", look=(1, -1), shiver=1.0, arms="cover"),
                    dill=dict(mood="frozen", look=(1, -0.6), shake=sc))[who]
    if t >= T_CHARGE:
        return dict(crumb=dict(mood="scared", look=(1, -1)), peep=dict(mood="proud", face=0.6, look=(1, -1)),
                    chip=dict(mood="eep", look=(1, -1)), dill=dict(mood="angry", look=(1, -1), arm="up"))[who]
    if T_FLOP <= t:
        return dict(crumb=dict(mood="sheepish", look=(0, -1)), peep=dict(mood="blink" if int(t * 1.5) % 4 == 0 else "happy", face=0.0, look=(0, -1)),
                    chip=dict(mood="shy", look=(0, -1)), dill=dict(mood="sad", look=(0, -1)))[who]
    return None


def crumb_kw_mid(t):
    kw = common_kw(t, "crumb")
    if kw is not None:
        return kw
    if t < 5.6:
        return dict(mood="worried", look=(1, -0.6))
    if t < 9.0:
        return dict(mood="scared" if T_TOPPLE <= t < T_TOPPLE + 0.6 else "worried", look=(1, -1))
    if t < T_DANCE:
        return dict(mood="worried", look=(1, -0.5))
    return dict(mood="sheepish", look=(1, 0))


def peep_state(t):
    """(x, y, kw)"""
    if t < T_PHOP:
        return PEX, FLOOR, dict(mood="happy", face=0.6, look=(1, -1))
    if t < T_PLAND:
        p = seg(t, T_PHOP, T_PLAND)
        x, y = hop((PEX, FLOOR), (JX, DTOP), p, 280)
        return x, y, dict(mood="proud", face=0.6, wings="flap", flap_t=t)
    if t < T_PHOPOFF:
        for i, b in enumerate(P_BOUNCE):
            if b <= t < b + 0.5:
                h = (90 + 50 * i) * math.sin(math.pi * seg(t, b, b + 0.5))
                return JX, DTOP - h, dict(mood="happy" if h > 30 else "blink", face=0.0, wings="flap" if h > 20 else "down", flap_t=t)
        return JX, DTOP, dict(mood="blink" if 4.9 < t < 5.0 else "happy", face=-0.3, look=(0, 1))
    if t < T_PBACK:
        x, y = hop((JX, DTOP), (PEX, FLOOR), seg(t, T_PHOPOFF, T_PBACK), 160)
        return x, y, dict(mood="happy", face=-0.6, wings="flap", flap_t=t)
    kw = common_kw(t, "peep")
    if kw is not None:
        return PEX, FLOOR, kw
    if t < T_DANCE:
        return PEX, FLOOR, dict(mood="happy", face=0.5, look=(1, -1))
    # copies Dill's dance, in miniature
    b = (t - T_DANCE) / 0.24
    if t < T_SCRATCH:
        return PEX, FLOOR - 12 * abs(math.sin(b * math.pi)), dict(mood="proud", face=0.3, wings="flap" if int(b) % 2 else "salute",
                                                                   flap_t=t, rot=0.15 * math.sin(b * math.pi))
    return PEX, FLOOR, dict(mood="shock", face=0.3, look=(1, 0))


def chip_kw(t):
    kw = common_kw(t, "chip")
    if kw is not None:
        return kw
    if T_TOPPLE <= t < T_TOPPLE + 0.7:
        return dict(mood="eep", look=(1, -1), arms="cover", shiver=1.0)
    if T_DANCE <= t < T_SCRATCH:
        return dict(mood="giggle", look=(1, 0), arms="up" if int((t - T_DANCE) / 0.48) % 2 else "down")
    return dict(mood="shy", look=(1, -0.6), shiver=0.2)


def dill_state(t):
    """(x, y, kw)"""
    if t < T_DANCE - 0.3:
        mood = "smug" if t < 5.6 else ("angry" if t < 9.0 else "smug")
        if T_TOPPLE <= t < T_TOPPLE + 0.6:
            return DIX, FLOOR, dict(mood="shocked", look=(1, -1))
        if T_HMPH - 0.2 <= t < T_HMPH + 0.4:
            return DIX, FLOOR, dict(mood="smug", look=(1, -0.6), arm="point_l")
        return DIX, FLOOR, dict(mood=mood, look=(1, -0.8), arm="cross")
    if t < T_DANCE:
        p = ease(seg(t, T_DANCE - 0.3, T_DANCE))
        return DIX + 20 * p, FLOOR, dict(mood="proud", look=(1, -0.5))
    if t < T_SCRATCH:
        b = (t - T_DANCE) / 0.24
        arm = ["flail", "reach", "flail", "pound"][int(b) % 4]
        return DIX + 20 + 22 * math.sin(b * math.pi / 2), FLOOR - 18 * abs(math.sin(b * math.pi)), \
            dict(mood="proud" if int(b) % 3 else "smug", look=(1, -0.4), arm=arm, rot=0.14 * math.sin(b * math.pi / 2),
                 sq=1 + 0.06 * math.sin(b * math.pi))
    if t < T_FLOP:
        return DIX + 20, FLOOR, dict(mood="frozen", look=(1, -0.6), arm="flail")
    kw = common_kw(t, "dill")
    return DIX + 20, FLOOR, kw


def gran_state(t):
    """(x, y, kw)"""
    for i, p in enumerate(GPOKES):
        if p - 0.15 <= t < p + 0.25:
            h = 50 * math.sin(math.pi * seg(t, p - 0.15, p + 0.25))
            return GRX + 20, FLOOR, dict(look=(1, -1), mood="angry", cane="up", hop=h)
    if 9.0 <= t < GPOKES[0]:
        return lerp(GRX, GRX + 20, ease(seg(t, 9.0, 9.15))), FLOOR, dict(look=(1, -1), mood="stern", step=t * 3)
    if GPOKES[0] <= t < T_DANCE - 0.3:
        return GRX + 20, FLOOR, dict(look=(1, -1) if t < T_HMPH else (-1, 0), mood="stern")
    if T_UP <= t < STEPS[0]:
        return GRX, FLOOR, dict(look=(1, -1), mood="shock")
    if t >= STEPS[0] - 0.1:
        wave = t >= T_LIFT
        return GRX, FLOOR, dict(look=(1, -1), mood="shock" if t < T_OPEN else "stern",
                                cane="up" if (wave and int(t * 4) % 2) else "down")
    if T_FLOP <= t:
        return GRX, FLOOR, dict(look=(0, -1), mood="stern")
    return GRX, FLOOR, dict(look=(1, -0.8), mood="stern")


def pickle_state(k, t):
    """(x, y, rot, kw)"""
    j = PK_JUMP[k]
    px, py = PK_PILE[k]
    if t < j:
        lk = (0, 1) if t > 5.5 else (-1, 0.5)
        return PK_TOP[k], TOP, 0.0, dict(look=lk, mood="calm", arms="down")
    if t < j + PK_FALL:
        p = seg(t, j, j + PK_FALL)
        x, y = hop((PK_TOP[k], TOP), (px, py), p, 60)
        return x, y, 0.3 * p, dict(look=(0, 1), mood="shock", arms="up")
    if t < T_TOPPLE:
        wob = 0.0
        if t > 7.9:
            wob = 0.12 * math.sin((t - 7.9) * 25) * seg(t, 7.9, T_TOPPLE)
        sq = 0
        return px + wob * 40, py, wob, dict(look=(0, 1), mood="calm", arms="up" if k >= 3 else "down")
    t0 = T_TOPPLE + 0.08 * k
    side = (1 if k % 2 else -1)
    jx = JX + (-50, 50, 0, -25, 25)[k]
    if t < t0 + 0.4:      # tumble down onto the jello
        p = seg(t, t0, t0 + 0.4)
        x, y = hop((px, py), (jx, FLOOR - 150), p, 60)
        return x, y, side * 1.2 * p, dict(look=(0, 1), mood="shock", arms="up")
    if t < t0 + 1.0:      # BOING off the jello, back up onto the top shelf
        p = seg(t, t0 + 0.4, t0 + 1.0)
        x, y = hop((jx, FLOOR - 150), (PK_TOP[k], TOP), p, 330)
        return x, y, side * (1.2 + 3.0 * p), dict(look=(0, 1), mood="shock", arms="up")
    lying = side * 1.45
    if T_UP <= t:
        up = back_out(seg(t, T_UP, T_UP + 0.3))
        return PK_TOP[k], TOP, lying * (1 - up), dict(look=(0, 1), mood="shock")
    return PK_TOP[k], TOP, lying, dict(look=(0, 0), mood="closed")


def duck_squash(t):
    if T_SQUEAK <= t < T_SQUEAK + 0.5:
        q = seg(t, T_SQUEAK, T_SQUEAK + 0.5)
        return 1 + 0.16 * math.sin(math.pi * q), 1 - 0.2 * math.sin(math.pi * q)
    if T_CLAND <= t < T_CLAND + 0.25:
        return 1.06, 0.92
    if T_BOOP <= t < T_BOOP + 0.3:
        q = seg(t, T_BOOP, T_BOOP + 0.3)
        return 1 + 0.08 * math.sin(math.pi * q), 1 - 0.1 * math.sin(math.pi * q)
    return 1.0, 1.0


def leap_pos(name, t, home):
    """Leap from home (x, FLOOR) to the Hand. Returns (x, y, p) in world coords, p = progress."""
    hx, tip, _ = hand_pos(t)
    if name == "crumb":
        tx, ty = hx + ON_HAND["crumb_pivot"][0] - 85, tip + ON_HAND["crumb_pivot"][1] + 270
    else:
        tx, ty = hx + ON_HAND[name][0], tip + ON_HAND[name][1]
    delay = dict(dill=0.0, chip=0.1, peep=0.18, crumb=0.28)[name]
    p = seg(t, T_LEAP + delay, T_GRAB + delay)
    x, y = hop(home, (tx, ty), ease(p), 120)
    return x, y, p


# ---------------- camera (inside) ----------------
KEYS = [(0.0, 880, 1050, 1.55), (0.6, 880, 1130, 1.65), (2.3, 880, 1170, 1.7), (2.7, 700, 1120, 1.3), (5.6, 700, 1120, 1.3),
        (5.95, 760, 1030, 1.22), (9.0, 760, 1030, 1.22), (9.25, 900, 1200, 1.75), (10.5, 900, 1200, 1.75),
        (10.85, 760, 1170, 1.5), (13.0, 760, 1170, 1.5), (13.4, 640, 1120, 1.2), (15.2, 640, 1120, 1.2),
        (16.75, 900, 1190, 2.3), (16.95, 900, 1190, 2.3), (17.25, 640, 1120, 1.2), (19.3, 650, 1100, 1.2),
        (20.1, 720, 1000, 1.15), (21.9, 720, 1000, 1.15), (22.6, 720, 740, 1.15)]


def camera(t):
    cx, cy, z = keyed(KEYS, t)
    cy += 30
    hw = 540 / z
    cx = min(max(cx, hw), W - hw)
    shakes = [(T_CLAND, 6), (T_TOPPLE + 0.4, 5)] + [(j + PK_FALL, 4) for j in PK_JUMP] + [(s, 12) for s in STEPS] + [(T_SQUEAK, 4)]
    for t0, s in shakes:
        if t0 <= t < t0 + 0.25:
            q = s * (1 - seg(t, t0, t0 + 0.25)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    return cx, cy, z


# ---------------- inside scene ----------------
def inside(c, t):
    L = light_at(t)
    fridge6(c, L, 1, lid=False)
    frost(c, t, 1.0)
    frost_drawing(c, 40.0)
    ceiling(c, L)
    ceiling_vent(c, L)
    god_rays(c, L)

    # Jar pickles (top shelf, before they jump) are drawn with the rest below
    # bottom shelf set
    jello(c, JX, FLOOR, 0.15 * math.sin((t - T_CLAND) * 18) * math.exp(-(t - T_CLAND) * 4) if t > T_CLAND else 0.0)
    sx, sy = duck_squash(t)
    c.save(); c.translate(JX, DY); c.scale(sx, sy); c.translate(-JX, -DY)
    clean_duck(c, JX, DY, tilt=-0.45, gaze=-2.0, frosty=0.7, s=DUCK_S)
    c.restore()
    # Jar pickles
    for k in range(5):
        x, y, r, kw = pickle_state(k, t)
        if y <= TOP + 1:
            y -= 36 * abs(math.sin(r))
        c.save(); c.translate(x, y); c.scale(PKS, PKS); c.translate(-x, -y)
        pickle_kid(c, x, y, k, rot=r, **kw)
        c.restore()
    carton(c)
    plate(c, DISH)
    butter_rink(c, 1.0)

    fk = flop_k(t)
    leaping = t >= T_LEAP

    # Chip
    if not leaping:
        c.save(); lie(c, CHX, FLOOR, fk, 1, 80)
        draw_chip(c, t, CHX, FLOOR, chip_kw(t))
        c.restore()

    # Grandma
    gx, gy, gk = gran_state(t)
    c.save(); lie(c, gx, gy, fk, 1, 55)
    draw_grandma(c, gx, gy, gk)
    c.restore()

    # Crumb
    if not leaping:
        crx, cry, ckw, csq = crumb_state(t)
        if t >= 3.3:
            ckw = crumb_kw_mid(t)
        c.save()
        if csq != 1.0:
            c.translate(crx, cry); c.scale(S(1 + (1 - csq) * 0.7), S(csq)); c.translate(-crx, -cry)
        lie(c, crx, cry, fk, 1, 70)
        draw_crumb(c, t, crx, cry, ckw)
        c.restore()

    # Peep
    if not leaping:
        px, py, pkw = peep_state(t)
        c.save(); lie(c, px, py, fk, 1, 60)
        fat_peep(c, px, py, FAT, **pkw)
        c.restore()

    # Dill
    if not leaping:
        dx, dy, dkw = dill_state(t)
        c.save(); lie(c, dx, dy, fk, 1, 76)
        draw_dill(c, t, dx, dy, dkw)
        c.restore()


    # the Hand + the team leaping onto it
    hx, tip, grip = hand_pos(t)
    if t >= T_HDOWN:
        hand_cuffed(c, hx, tip, grip)
    if leaping:
        homes = dict(dill=(DIX + 20, FLOOR), chip=(CHX, FLOOR), peep=(PEX, FLOOR), crumb=(CRX, FLOOR))
        on = {}
        for name in ("crumb", "dill", "peep", "chip"):
            x, y, p = leap_pos(name, t, homes[name])
            if p < 1:
                on[name] = True
                if name == "dill":
                    draw_dill(c, t, x, y, dict(mood="angry", look=(1, -1), arm="up" if p < 0.5 else "reach"))
                elif name == "chip":
                    draw_chip(c, t, x, y, dict(mood="eep", look=(1, -1), arms="up"))
                elif name == "peep":
                    fat_peep(c, x, y, FAT, mood="proud", face=0.5, wings="flap", flap_t=t)
                else:
                    c.save(); rot_at(c, x, y, 0.5 * p)
                    draw_crumb(c, t, x, y, dict(mood="scared", look=(1, -1), arm="wave"))
                    c.restore()
        team_on_hand(c, t, hx, tip, 1.0, wind=0.3, falling=on)

    effects_in(c, t)
    dark_overlay(c, L)


def effects_in(c, t):
    word(c, t, "THUD!", JX - 60, DTOP - 330, 70, (1, 0.9, 0.4), T_CLAND, T_CLAND + 0.6, -0.1)
    word(c, t, "...", JX + 20, DTOP - 340, 64, (1, 1, 1), 0.9, 1.6, 0.05)
    word(c, t, "chirp chirp", JX - 230, DTOP - 120, 44, (1, 1, 1), 1.2, 2.0, -0.06)
    word(c, t, "shhk", JX - 80, FLOOR - 120, 46, (1, 1, 1), T_CSLIDE, T_CBACK + 0.1, 0.1)
    for i, b in enumerate(P_BOUNCE):
        word(c, t, "boing!", JX - 160 + 40 * i, DTOP - 160 - 60 * i, 48 + 6 * i, GOLD, b + 0.05, b + 0.45, -0.1 + 0.1 * i)
    word(c, t, "...", JX, DTOP - 300, 64, (1, 1, 1), 4.6, 5.0, 0.05)
    word(c, t, "chirp", JX - 220, DTOP - 60, 44, (1, 1, 1), 4.65, 5.1, 0.06)
    for k, j in enumerate(PK_JUMP):
        px, py = PK_PILE[k]
        word(c, t, "THUD", px + (60 if k % 2 else -80), py - 200, 44, (1, 0.9, 0.4), j + PK_FALL, j + PK_FALL + 0.35, 0.1 * (1 if k % 2 else -1))
    word(c, t, "...", JX + 10, DTOP - 520, 64, (1, 1, 1), 7.6, 8.25, 0.05)
    word(c, t, "WHOA-", 850, DTOP - 480, 50, (1, 1, 1), 7.95, T_TOPPLE + 0.2, -0.08)
    word(c, t, "CRASH!", 900, FLOOR - 330, 72, RED, T_TOPPLE + 0.45, T_TOPPLE + 1.1, 0.08)
    for i, p in enumerate(GPOKES):
        word(c, t, "tok", JX - 120 + 30 * i, DTOP - 200 - 40 * i, 44, (1, 1, 1), p, p + 0.35, -0.1 + 0.1 * i)
    word(c, t, "...", JX + 10, DTOP - 300, 64, (1, 1, 1), 10.3, 10.85, 0.05)
    word(c, t, "hmph.", GRX - 30, FLOOR - 340, 44, (1, 1, 1), T_HMPH, T_DANCE - 0.2, -0.08)
    if T_DANCE <= t < T_SCRATCH:
        for j in range(3):
            q = ((t - T_DANCE) * 0.9 + j / 3) % 1
            x0 = DIX - 120 + 140 * j
            music_note(c, x0 + 20 * math.sin(q * 7), FLOOR - 380 - 160 * q, 1.2, 1 - q)
    word(c, t, "SKRRTCH!", DIX - 40, FLOOR - 470, 60, RED, T_SCRATCH, T_SCRATCH + 0.5, -0.08)
    word(c, t, "...", JX + 10, DTOP - 300, 64, (1, 1, 1), T_SCRATCH + 0.15, T_FLOP, 0.05)
    word(c, t, "sigh...", 520, FLOOR - 260, 48, (1, 1, 1), T_FLOP + 0.3, T_FLOP + 1.4, -0.06)
    word(c, t, "SQUEAK!", JX - 130, DTOP - 300, 84, GOLD, T_SQUEAK, T_SQUEAK + 0.9, -0.1)
    sq_rings(c, JX, DY - 120, t, T_SQUEAK, 1.0)
    for x in (CHX, PEX, CRX, DIX + 20):
        word(c, t, "!!", x + 10, FLOOR - 330, 64, RED, T_UP, T_UP + 0.6, 0.05)
    for i, s in enumerate(STEPS):
        word(c, t, "THMP", 900 - 60 * i, 640 + 70 * i, 62 + 6 * i, (1, 1, 1), s, s + 0.4, 0.08 * (1 if i % 2 else -1))
    word(c, t, "HYAAA!", DIX - 40, FLOOR - 470, 66, GOLD, T_CHARGE, T_LEAP + 0.3, -0.06)
    word(c, t, "boop", HX + 170, HTIP - 40, 44, (1, 1, 1), T_BOOP, T_BOOP + 0.45, 0.1)
    if T_LIFT <= t < T_EXT:
        for j in range(5):
            x = HX - 180 + 90 * j
            c.move_to(x, 900 - 200 * j % 300); c.line_to(x, 1400 - 200 * j % 300)
            c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(6); c.stroke()


# ---------------- exterior (kitchen) ----------------
def kitchen_bg(c):
    c.rectangle(-200, -200, W + 400, KFLOOR + 200); c.set_source_rgb(*hexc("#FFF1D6")); c.fill()
    c.set_source_rgba(*hexc("#E9C99A"), 0.6); c.set_line_width(3)
    for gx in range(-200, W + 200, 90):
        c.move_to(gx, -200); c.line_to(gx, 1100); c.stroke()
    for gy in range(-200, 1100, 90):
        c.move_to(-200, gy); c.line_to(W + 200, gy); c.stroke()
    # counter on the right
    c.rectangle(930, 1100, 400, 40); c.set_source_rgb(*hexc("#C48A4A")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.rectangle(940, 1140, 400, KFLOOR - 1140); c.set_source_rgb(*hexc("#3BA5A0")); c.fill_preserve(); c.stroke()
    # floor
    for i in range(-3, 16):
        for j in range(0, 4):
            c.rectangle(i * 90, KFLOOR + j * 90, 90, 90)
            c.set_source_rgb(*(hexc("#4D7CC7") if (i + j) % 2 else (0.96, 0.97, 1.0))); c.fill()
    c.move_to(-200, KFLOOR); c.line_to(W + 200, KFLOOR); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()


def door(c, x0, x1, y0, y1, th, inside_draw=None):
    """A door hinged on the right edge (x1); th = swing angle (0 closed). Draws the gap contents first."""
    xl = x1 - (x1 - x0) * math.cos(th)
    if xl > x0 + 2 and inside_draw:
        c.save(); c.rectangle(x0 + 8, y0 + 8, xl - x0 - 8, y1 - y0 - 16); c.clip(); inside_draw(c, x0, xl, y0, y1); c.restore()
    e = 90 * math.sin(th)
    c.move_to(xl, y0 - e); c.line_to(x1, y0); c.line_to(x1, y1); c.line_to(xl, y1 + e); c.close_path()
    c.set_source_rgb(*hexc("#F1F5F9")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    # handle near the free edge
    u = 0.07
    hx = lerp(xl, x1, u)
    hy0, hy1 = y0 + 0.25 * (y1 - y0), y0 + 0.75 * (y1 - y0)
    hy0 -= (1 - u) * e * 0.5; hy1 += (1 - u) * e * 0.5
    rrect(c, hx - 16, hy0, 32, hy1 - hy0, 16); c.set_source_rgb(*hexc("#ADB5BD")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    return xl, hx, (hy0 + hy1) / 2


def blizzard_inside(t):
    def f(c, x0, x1, y0, y1):
        g = cairo.LinearGradient(0, y0, 0, y1)
        g.add_color_stop_rgb(0, *SNOW); g.add_color_stop_rgb(1, *ICE)
        c.rectangle(x0, y0, x1 - x0, y1 - y0); c.set_source(g); c.fill()
        rnd = random.Random(5)
        for j in range(40):
            fx = x0 + ((rnd.random() * 900 - t * 500 * (0.6 + rnd.random())) % (x1 - x0 + 1))
            fy = y0 + rnd.random() * (y1 - y0)
            ellipse(c, fx, fy, 5, 5, (1, 1, 1), stroke=False)
    return f


def freezer_theta(t):
    if t < T_FOPEN:
        return 0.0
    if t < T_SLAM - 0.3:
        return 1.25 * back_out(seg(t, T_FOPEN, T_FOPENED))
    return 1.25 * (1 - ease(seg(t, T_SLAM - 0.3, T_SLAM)) ** 2)


def ext_hand(t):
    """Exterior: (x, tip_y, s, with_team)."""
    s = 0.42
    if t < T_EXT2:
        if t < T_RISE:
            p = ease_out(seg(t, T_EXT, T_RISE))
            return 520, lerp(1650, 1320, p), s, True
        if t < T_GRIP:
            p = ease(seg(t, T_RISE, T_GRIP))
            return lerp(520, 225, p), lerp(1320, 640, p), s, True
        th = freezer_theta(t)
        xl = FX1 - (FX1 - FX0) * math.cos(th)
        hx = lerp(xl, FX1, 0.07)
        if t < T_REACH:
            return hx + 10, 640, s, True
        p = ease(seg(t, T_REACH, T_CU))
        return lerp(hx + 10, 470, p), lerp(640, 700, p), s, True
    p = ease(seg(t, T_EXT2, T_EXT2 + 0.5))
    return lerp(470, 560, p), lerp(700, -500, p), s, False


def exterior(c, t):
    kitchen_bg(c)
    # body
    c.rectangle(FX0 - 10, FTOP - 20, FX1 - FX0 + 20, KFLOOR - FTOP + 20); c.set_source_rgb(*hexc("#DDE7EE")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    c.rectangle(FX0 + 10, KFLOOR - 25, FX1 - FX0 - 20, 20); c.set_source_rgb(*hexc("#868E96")); c.fill()
    # main door: a lit seam while it's still ajar
    if t < T_MCLOSE:
        k = 1 - ease(seg(t, T_EXT, T_MCLOSE))
        door(c, FX0, FX1, MTOP, MBOT, 0.35 * k, lambda cc, a, b, y0, y1: (cc.set_source_rgb(*hexc("#F3FAFF")), cc.paint()))
    else:
        door(c, FX0, FX1, MTOP, MBOT, 0.0)
    # magnets on the main door (banana, star, pizza)
    if t >= T_MCLOSE:
        c.move_to(330, 1180); c.curve_to(350, 1230, 420, 1230, 445, 1170); c.curve_to(410, 1205, 360, 1205, 330, 1180)
        c.set_source_rgb(*hexc("#FFE066")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        star(c, 620, 1050, 46, 0.1, hexc("#FF922B"))
        c.move_to(700, 1660); c.line_to(780, 1660); c.line_to(740, 1740); c.close_path()
        c.set_source_rgb(*hexc("#FFC078")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    # freezer door
    th = freezer_theta(t)
    xl, _, _ = door(c, FX0, FX1, FTOP, FZB, th, blizzard_inside(t))
    # frost seam
    c.move_to(FX0, FZB + 12); c.line_to(FX1, FZB + 12); c.set_source_rgba(*ICE_B, 0.8); c.set_line_width(6); c.stroke()
    open_k = min(1.0, th / 1.0)
    if open_k > 0.05:
        # cold light pouring out
        for i in range(6):
            a0 = 1.9 + 0.35 * i
            c.move_to((FX0 + xl) / 2, (FTOP + FZB) / 2)
            c.line_to((FX0 + xl) / 2 + 2000 * math.cos(a0), (FTOP + FZB) / 2 + 2000 * math.sin(a0) * 0.6 + 400)
            c.line_to((FX0 + xl) / 2 + 2000 * math.cos(a0 + 0.12), (FTOP + FZB) / 2 + 2000 * math.sin(a0 + 0.12) * 0.6 + 400)
            c.close_path(); c.set_source_rgba(0.9, 0.97, 1.0, 0.18 * open_k); c.fill()
        rnd = random.Random(11)
        for j in range(60):
            sp = 0.5 + rnd.random()
            q = (t * sp * 0.8 + rnd.random()) % 1
            fx = lerp((FX0 + xl) / 2, -200 + rnd.random() * (W + 400), q)
            fy = lerp(FTOP + rnd.random() * (FZB - FTOP), FTOP - 300 + rnd.random() * 1800, q)
            ellipse(c, fx, fy, 4 + 8 * q, 4 + 8 * q, (1, 1, 1), lw=2)
    # the Hand (+ team)
    hx, tip, s, team = ext_hand(t)
    if tip < 2000:
        c.save(); c.translate(hx, tip); c.scale(s, s)
        hand_cuffed(c, 0, 0, 0.6 if T_GRIP <= t < T_FOPENED else 0.3)
        c.restore()
        if team:
            team_on_hand(c, t, hx, tip, s, wind=0.6 if t > T_FOPEN else 0.2)
    # SLAM puff
    if T_SLAM <= t < T_SLAM + 0.8:
        q = seg(t, T_SLAM, T_SLAM + 0.8)
        for j in range(10):
            x = lerp(FX0, FX1, j / 9)
            ellipse(c, x, FZB + 10 - 60 * q, 30 + 40 * q, 22 + 20 * q, (1, 1, 1), stroke=False)
        c.set_source_rgba(1, 1, 1, 0.6 * (1 - q)); c.rectangle(-200, -200, W + 400, KFLOOR + 600); c.fill()
    word(c, t, "THUNK", 640, 1500, 54, (1, 1, 1), T_MCLOSE, T_MCLOSE + 0.5, 0.08)
    word(c, t, "WHOOOOSH!", 430, 300, 66, ICE_B, T_FOPEN + 0.2, T_CU, -0.06)
    word(c, t, "THUD!", 560, 560, 120, (1, 0.9, 0.4), T_SLAM, T_SLAM + 0.8, -0.08)


def ext_camera(t):
    if t < T_EXT2:
        cx, cy, z = keyed([(T_EXT, 540, 1250, 1.3), (T_RISE, 520, 1150, 1.35), (T_GRIP, 330, 640, 1.6),
                           (T_FOPENED, 420, 600, 1.5), (T_CU, 450, 560, 1.9)], t)
        if T_FOPEN + 0.2 <= t < T_CU:
            q = 6; cx += random.uniform(-q, q); cy += random.uniform(-q, q)
        return cx, cy, z
    cx, cy, z = keyed([(T_EXT2, 540, 900, 1.15), (T_SLAM, 540, 900, 1.15), (T_SLAM + 0.3, 540, 700, 1.3), (T_WHITE, 540, 560, 2.6)], t)
    if T_SLAM <= t < T_SLAM + 0.35:
        q = 20 * (1 - seg(t, T_SLAM, T_SLAM + 0.35)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    return cx, cy, z


# ---------------- close-up on the cuff in the blizzard ----------------
def closeup(c, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *ICE); g.add_color_stop_rgb(0.6, *SNOW); g.add_color_stop_rgb(1, 1, 1, 1)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    rnd = random.Random(3)
    # wind streaks
    for j in range(26):
        sp = 900 + 900 * rnd.random()
        y = rnd.random() * H
        x = (rnd.random() * 2400 - (t - T_CU) * sp) % 2400 - 600
        c.move_to(x, y); c.line_to(x + 160 + 120 * rnd.random(), y - 20)
        c.set_source_rgba(*ICE_B, 0.35); c.set_line_width(5); c.stroke()
    for j in range(70):
        sp = 600 + 900 * rnd.random()
        y = (rnd.random() * H + (t - T_CU) * 120) % H
        x = (rnd.random() * 1600 - (t - T_CU) * sp) % 1600 - 260
        r = 4 + 9 * rnd.random()
        ellipse(c, x, y, r, r, (1, 1, 1), lw=2)
    s = 1.45
    hx = 540 + 25 * math.sin((t - T_CU) * 2.2)
    tip = lerp(1380, 1500, ease(seg(t, T_CU, T_SLIP)))
    if t >= T_FALL + 0.8:
        tip -= 2200 * ease(seg(t, T_FALL + 0.8, T_EXT2)) ** 2
    c.save(); c.translate(hx, tip); c.scale(s, s); hand_cuffed(c, 0, 0, 0.3); c.restore()
    # falling: Crumb slips first, the rest go with him
    falling = {}
    order = [("crumb", T_SLIP + 0.25), ("dill", T_FALL), ("chip", T_FALL + 0.12), ("peep", T_FALL + 0.35)]
    for name, t0 in order:
        if t >= t0:
            falling[name] = t0
    team_on_hand(c, t, hx, tip, s, wind=1.0, falling={k: 0 for k in falling})
    for name, t0 in order:
        if name not in falling:
            continue
        q = t - t0
        if name == "crumb":
            px, py = ON_HAND["crumb_pivot"]
            x0, y0 = hx + (px - 85) * s, tip + (py + 270) * s
        else:
            x0, y0 = hx + ON_HAND[name][0] * s, tip + ON_HAND[name][1] * s
        drift = dict(crumb=-120, dill=-40, chip=160, peep=60)[name]
        x = x0 + drift * q - 60 * q * q
        y = y0 + 900 * q * q + 150 * q
        sc = max(0.25, 1 - 0.35 * q)
        rot = dict(crumb=-4, dill=3, chip=-5, peep=6)[name] * q
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * sc, s * sc)
        if name == "crumb":
            draw_crumb(c, t, 0, 0, dict(mood="scared", look=(0, -1), arm="wave"))
        elif name == "dill":
            draw_dill(c, t, 0, 0, dict(mood="shocked", look=(0, -1), arm="reach"))
        elif name == "chip":
            draw_chip(c, t, 0, 0, dict(mood="eep", look=(0, -1), arms="up"))
        else:
            fat_peep(c, 0, 0, FAT, mood="shock", wings="flap", flap_t=t * 2, face=0.0)
        c.restore()
    # white fog swallowing the bottom
    fogk = ease(seg(t, T_FALL, T_EXT2))
    if fogk > 0.01:
        g2 = cairo.LinearGradient(0, H * (1 - 0.9 * fogk), 0, H)
        g2.add_color_stop_rgba(0, 1, 1, 1, 0); g2.add_color_stop_rgba(0.6, 1, 1, 1, 0.9); g2.add_color_stop_rgba(1, 1, 1, 1, 1)
        c.rectangle(0, 0, W, H); c.set_source(g2); c.fill()
    word(c, t, "AAAAAH!", 540, 300, 96, ICE_B, T_CU + 0.2, T_SLIP - 0.2, -0.05)
    if T_CU + 1.2 <= t < T_SLIP + 0.25:
        drop(c, hx + (ON_HAND["crumb_pivot"][0] - 40) * s, tip + (ON_HAND["crumb_pivot"][1] + 40) * s + 40 * ((t * 1.5) % 1), 1.8)
    word(c, t, "slip...", 230, tip - 500, 56, (0.3, 0.4, 0.6), T_SLIP - 0.4, T_SLIP + 0.3, -0.1)
    word(c, t, "pop!", 220, tip - 330, 64, RED, T_SLIP + 0.25, T_SLIP + 0.7, 0.1)
    word(c, t, "!!", 500, tip - 760, 90, RED, T_SLIP + 0.3, T_FALL, 0.05)
    word(c, t, "WAAAAAA!", 540, 1500, 84, ICE_B, T_FALL + 0.1, T_FALL + 1.2, 0.05)


# ---------------- total white ----------------
def white(c, t):
    c.rectangle(0, 0, W, H); c.set_source_rgb(*SNOW); c.fill()
    rnd = random.Random(9)
    for j in range(50):
        sp = 60 + 120 * rnd.random()
        x = (rnd.random() * 1400 - (t - T_WHITE) * sp) % 1400 - 160
        y = (rnd.random() * H + (t - T_WHITE) * 50) % H
        r = 3 + 6 * rnd.random()
        ellipse(c, x, y, r, r, ICE, stroke=False)
    # pale vignette
    g = cairo.RadialGradient(W / 2, H / 2, 300, W / 2, H / 2, 1200)
    g.add_color_stop_rgba(0, 1, 1, 1, 0); g.add_color_stop_rgba(1, *ICE, 0.7)
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    grey = (0.62, 0.72, 0.85)
    for i, (p, x, y, sz) in enumerate(zip(PEEPS, (540, 330, 760), (1120, 1000, 1220), (84, 62, 46))):
        if p <= t:
            a = max(0.0, 1 - (t - p) / 2.4)
            if a > 0:
                c.save(); c.push_group()
                k = back_out(seg(t, p, p + 0.2))
                c.translate(x, y); c.scale(S(k), S(k)); text(c, "peep?", 0, 0, sz, grey, olw=6)
                c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()
    # the huge icy eye opening behind (drawn before Peep's eyes so they sit in front)
    if t >= T_BIGEYE:
        o = ease(seg(t, T_BIGEYE, T_BIGEYE + 0.7))
        ex, ey = 640, 820
        c.save(); c.translate(ex, ey)
        c.save(); c.scale(300, S(150 * o)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(*hexc("#A5D8FF"), 0.85); c.fill()
        c.save(); c.scale(300, S(150 * o)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(*hexc("#1864AB"), 0.7); c.set_line_width(8); c.stroke()
        c.save(); c.scale(300, S(150 * o)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.clip()
        ellipse(c, 0, 0, 110, 110, hexc("#4DABF7"), stroke=False)
        ellipse(c, 0, 0, 22, 100, hexc("#0B2A4A"), stroke=False)
        ellipse(c, -40, -40, 22, 16, (1, 1, 1), stroke=False)
        c.restore()
    # Peep's tiny eyes in the snow
    if t >= T_EYES:
        bl = 0.12 if (T_EYES + 0.5 <= t < T_EYES + 0.62) else 1.0
        k = back_out(seg(t, T_EYES, T_EYES + 0.25))
        for ex in (510, 570):
            ellipse(c, ex, 1340, S(16 * k), S(20 * k * bl), INK, stroke=False)
            if bl > 0.5:
                ellipse(c, ex - 5, 1333, S(5 * k), S(5 * k), (1, 1, 1), stroke=False)
        # the tip of the eggshell helmet poking out of the drift
        c.move_to(500, 1300); c.line_to(515, 1280); c.line_to(530, 1296); c.line_to(545, 1276); c.line_to(560, 1296)
        c.line_to(575, 1280); c.line_to(590, 1300)
        c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        if t >= T_BIGEYE + 0.2:
            for ex in (510, 570):
                ellipse(c, ex, 1340, 22, 26, (1, 1, 1), lw=4)
                ellipse(c, ex, 1342, 8, 9, INK, stroke=False)
    # snow drift in front
    c.move_to(-50, 1400)
    for k in range(9):
        c.curve_to(k * 140 + 20, 1360, k * 140 + 100, 1360, k * 140 + 140, 1400)
    c.line_to(W + 50, H + 50); c.line_to(-50, H + 50); c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgba(*ICE_B, 0.5); c.set_line_width(5); c.stroke()
    for i, d in enumerate(DUNS):
        if d <= t < d + 0.15:
            c.rectangle(0, 0, W, H); c.set_source_rgba(*hexc("#1864AB"), 0.08); c.fill()


# ---------------- frame ----------------
def frame(c, t):
    if t >= END_T:
        end_card(c, t, END_T); return
    random.seed(int(t * 30))
    if t < T_EXT:
        cx, cy, Z = camera(t)
        c.save(); c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
        inside(c, t)
        c.restore()
        if T_SQUEAK <= t < T_SQUEAK + 0.12:
            c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 0.8, 0.35); c.fill()
    elif t < T_CU or T_EXT2 <= t < T_WHITE:
        cx, cy, Z = ext_camera(t)
        c.save(); c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
        exterior(c, t)
        c.restore()
        if t >= T_WHITE - 0.3:
            c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, ease(seg(t, T_WHITE - 0.3, T_WHITE))); c.fill()
        if T_CU - 0.15 <= t < T_CU:
            c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, seg(t, T_CU - 0.15, T_CU)); c.fill()
    elif t < T_EXT2:
        closeup(c, t)
    else:
        white(c, t)
        if t >= END_T - 0.4:
            iris(c, 640, 820, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))
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
