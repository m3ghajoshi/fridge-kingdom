"""FRIDGE KINGDOM — Episode 24: "Duck vs Duck". 40.0s, 1080x1920 @ 30fps.

Variant B (cold open): the first frame is mid-action; the title shows as a banner across the top for the first 2s.

Continues from Ep 23: the two Ducks sit nose to nose on Dill's throne. Everyone gathers round. Dill rings in a staring
contest (callback to Ep 5): the Duck, of course, doesn't move. Squeak twitches, wobbles, then holds its breath, cheeks
puffing up redder and redder. Dill referees, waving his toothpick sword like a flag; Peep (on Dill's head) cheers for
Squeak, Crumb cheers for the Duck. Squeak can't hold it: PFFFT, it bursts and ricochets around the shelf. The Duck wins
without moving (DING DING, confetti). Sore loser: Squeak throws a squeaking tantrum, louder and louder; everyone covers
up. Then its loudest squeak ever: the jello wobbles, the milk carton tips over, icicles drop and shatter, the Duck's
bath bubbles pop, and the Duck still doesn't budge. Silence. Then, from the ceiling vent, one squeak answers: deep and
icy. Everyone slowly looks up. The Duck's one motion: it turns its head toward the vent. DUN DUN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (crown, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp, back_out, dark_overlay,
                 INK, GOLD, FLOOR, TOP, W, H, FPS, S)
from ep2 import end_card, jello
from ep6 import jar_pickles, drawer_back, drawer_front, JAR_X
from ep7 import god_rays, sq_rings, confetti
from ep9 import fat_peep, crumb_bitten
from ep10 import ceiling_vent, frost, frost_cloud, VENT_X
from ep12 import word, hop
from ep13 import ceiling
from ep14 import clean_duck
from ep15 import drop
from ep16 import keyed, butter_rink
from ep21 import mist, splats, JX
from ep22 import squeak_duck, scarf_flat, SQ_S
from ep23 import draw_chip, draw_dill_full, soap_bubble_small, DILL_HEAD

DUR = 40.0
END_T = 38.5
DIM = 0.22
FAT = 1.5
DUCK_S = 1.2
RED = (1, 0.35, 0.35)
ICY = hexc("#A5D8FF")
SQ_Y = hexc("#FFF3BF")

# ---------------- places ----------------
CR_X = 175                     # Crumb (cheers for the Duck)
DUCK_X = 320                   # the Duck, on the left of the throne
SQ_X = 500                     # Squeak, nose to nose with it (drawn mirrored: facing left)
DI_X = 735                     # Dill, referee (Peep on his head, cheering Squeak)
CH_X = 885                     # Chip
ICICLES = [(255, 0), (430, 1), (640, 2), (815, 3), (1010, 4)]

# ---------------- timing ----------------
ARRIVE = (0.3, 2.6)
T_BELL = 3.3                   # Dill rings in the contest
TWITCH = (4.4, 5.3)
WOBBLE = (5.6, 6.8)
T_BREATH = 7.1                 # Squeak sucks in a breath and holds it
T_CHEER = 10.0
T_BURST = 16.2
BOUNCE = [(16.2, (SQ_X, FLOOR), (650, FLOOR), 260), (16.6, (650, FLOOR), (215, FLOOR), 430),
          (17.15, (215, FLOOR), (590, FLOOR), 320), (17.6, (590, FLOOR), (SQ_X, FLOOR), 150), (17.95, None, None, 0)]
T_FLAT = 17.95
T_WIN = 18.6
T_UP = 21.6                    # Squeak gets up, furious
TANTRUM = [22.1, 22.75, 23.35, 23.9, 24.4, 24.85, 25.3, 25.7, 26.1, 26.45]
T_INHALE = 26.9
T_BIG = 27.9
T_BIG_END = 30.2
T_CARTON = (28.4, 29.2)
DROPS = [28.6, 28.85, 29.05, 29.3, 29.5]
T_FALL = 0.55
POPS = (28.25, 28.5)
T_PANT = 30.4
T_SILENT = 33.3
T_ANSWER = 34.4
T_LOOKUP = (35.0, 36.4)
DUNS = (37.0, 37.5)
T_PUFF = 34.35


def light_at(t):
    return DIM


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
    text(c, "Ep. 24:  Duck vs Duck", W / 2, 182, 48, (1, 1, 1), olw=8)
    c.restore()


# ---------------- set: the fridge with a tippable milk carton ----------------
def milk_carton(c, rot, dim):
    c.save(); c.translate(30, FLOOR); c.rotate(rot); c.translate(80, 0)
    c.rectangle(-80, -420, 160, 420); c.set_source_rgb(*[v * dim for v in (0.95, 0.95, 1)]); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.move_to(-80, -420); c.line_to(0, -500); c.line_to(80, -420); c.close_path()
    c.set_source_rgb(*[v * dim for v in hexc("#4DABF7")]); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.rectangle(-80, -300, 160, 110); c.set_source_rgb(*[v * dim for v in hexc("#4DABF7")]); c.fill()
    c.restore()


def carton_rot(t):
    if t < T_CARTON[0]:
        return 0.0
    p = seg(t, *T_CARTON)
    if p < 0.35:   # rocks back and forth
        return -0.12 * math.sin(p / 0.35 * 2 * math.pi) * 1.0
    q = (p - 0.35) / 0.65
    a = -math.pi / 2 * min(1, q * q * 1.4)
    if q >= 1:
        a = -math.pi / 2 + 0.05 * math.exp(-(t - T_CARTON[1]) * 8) * math.cos((t - T_CARTON[1]) * 30)
    return a


def fridge24(c, light, t):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc("#3D5285")); g.add_color_stop_rgb(1, *hexc("#24325A"))
    c.rectangle(-400, -400, W + 800, H + 1200); c.set_source(g); c.fill()
    dim = lerp(0.6, 1.0, light)
    c.set_source_rgba(1, 1, 1, 0.06 + 0.1 * light); c.set_line_width(8)
    for i in range(6):
        c.move_to(150, 140 + i * 40); c.line_to(930, 140 + i * 40); c.stroke()
    c.save(); c.translate(JAR_X, TOP)
    rrect(c, -95, -330, 190, 330, 30); c.set_source_rgba(0.8, 0.95, 0.85, 0.35 + 0.25 * light); c.fill_preserve()
    c.set_source_rgba(*INK, 1); c.set_line_width(6); c.stroke()
    jar_pickles(c, 0, light)
    ellipse(c, 0, -330, 92, 14, (0.85, 0.95, 0.9), lw=5)
    c.restore()
    for sy in (TOP, FLOOR):
        c.rectangle(-400, sy, W + 800, 34); c.set_source_rgba(0.75, 0.9, 1.0, 0.55 + 0.3 * light); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        c.rectangle(-400, sy + 6, W + 800, 6); c.set_source_rgba(1, 1, 1, 0.6); c.fill()
    drawer_back(c)
    milk_carton(c, carton_rot(t), dim)


def icicle(c, x, y, k, rot=0.0):
    """A hanging icicle (top at (x, y))."""
    L = 110 + 30 * (k % 3)
    c.save(); c.translate(x, y); c.rotate(rot)
    c.move_to(-20, 0); c.line_to(20, 0); c.line_to(2, L); c.line_to(-2, L); c.close_path()
    c.set_source_rgba(0.82, 0.93, 1.0, 0.95); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.move_to(-8, 8); c.line_to(-2, L * 0.6); c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(4); c.stroke()
    c.restore()


def icicles(c, t):
    for (x, k) in ICICLES:
        t0 = DROPS[k]
        if t < t0:
            sh = 4 * math.sin(t * 60 + k) if t >= T_BIG else 0.0
            icicle(c, x + sh, TOP + 34, k)
        elif t < t0 + T_FALL:
            p = seg(t, t0, t0 + T_FALL)
            L = 110 + 30 * (k % 3)
            y = lerp(TOP + 34, FLOOR - L, p * p)
            icicle(c, x, y, k, 0.15 * p * (1 if k % 2 else -1))
        else:
            q = t - t0 - T_FALL
            rnd = random.Random(40 + k)
            for j in range(7):
                a = rnd.uniform(-math.pi * 0.95, -math.pi * 0.05)
                v = rnd.uniform(250, 520)
                px = x + math.cos(a) * v * q
                py = min(FLOOR - 6, FLOOR - 6 + math.sin(a) * v * q + 900 * q * q)
                c.save(); c.translate(px, py); c.rotate(j + q * 6)
                c.move_to(-12, 0); c.line_to(0, -16); c.line_to(12, 0); c.close_path()
                c.set_source_rgba(0.82, 0.93, 1.0, 0.95); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
                c.restore()


# ---------------- Squeak ----------------
def squeak_state(t):
    """-> (x, y, kw, puff, red, sq, rot)."""
    kw = dict(look=(1, 0), eyes="open", beak=0.0)
    puff, red, rot, sq = 0.0, 0.0, 0.0, 1.0
    x, y = SQ_X, FLOOR
    if t < T_BELL:
        ph = (t % 0.5) / 0.5
        y = FLOOR - 14 * abs(math.sin(math.pi * ph))   # can't sit still
        if t >= ARRIVE[1]:
            kw["look"] = (0.4, -0.4)
        return x, y, kw, puff, red, sq, 0.03 * math.sin(t * 9)
    if t < T_BURST:
        if TWITCH[0] <= t < TWITCH[1]:
            ph = seg(t, *TWITCH)
            kw["eyes"] = "wide" if int(ph * 8) % 2 else "open"
            rot = 0.05 * math.sin(t * 60)
        if WOBBLE[0] <= t < WOBBLE[1]:
            rot = 0.22 * math.sin((t - WOBBLE[0]) * 9) * math.sin(math.pi * seg(t, *WOBBLE))
        if t >= T_BREATH - 0.3:
            # gulp, then hold it
            p = seg(t, T_BREATH - 0.3, T_BREATH)
            kw["beak"] = 0.8 * math.sin(math.pi * p) if t < T_BREATH else 0.0
            hold = seg(t, T_BREATH, T_BURST - 0.1)
            puff = ease_out(min(1.0, hold * 2.2)) * 0.75 + 0.35 * hold
            red = hold
            sq = 1 + 0.06 * puff
            rot = 0.02 * math.sin(t * (20 + 40 * hold)) * (0.5 + hold * 2)
            kw["eyes"] = "wide" if hold > 0.55 else "open"
        return x, y, kw, puff, red, sq, rot
    if t < T_FLAT:
        for i in range(len(BOUNCE) - 1):
            t0, a, b, h = BOUNCE[i]
            t1 = BOUNCE[i + 1][0]
            if t < t1:
                p = seg(t, t0, t1)
                x, y = hop(a, b, p, h)
                kw = dict(look=(1, 0), eyes="wide", beak=1.0)
                return x, y, kw, 0.6 * (1 - seg(t, T_BURST, T_BURST + 0.6)), 0.0, 1.0, (-1 if i % 2 else 1) * 2 * math.pi * p
    if t < T_UP:
        # flat, dizzy
        q = t - T_FLAT
        sq = 0.55 + 0.1 * math.exp(-q * 5) * math.cos(q * 25)
        if t >= T_UP - 0.4:
            sq = lerp(sq, 1.0, ease(seg(t, T_UP - 0.4, T_UP)))
        kw = dict(look=(math.cos(t * 8), math.sin(t * 8)), eyes="open", beak=0.0)
        if t >= T_WIN + 1.2:
            kw = dict(look=(1, 0), eyes="open", beak=0.0)
        return x, y, kw, 0.0, 0.0, sq, 0.0
    if t < T_INHALE:
        # tantrum: stomp-hop, squeak louder each time
        kw = dict(look=(1, 0), eyes="wide", beak=0.0)
        red = 0.5
        for i, s0 in enumerate(TANTRUM):
            if s0 - 0.12 <= t < s0 + 0.35:
                p = seg(t, s0 - 0.12, s0 + 0.35)
                y = FLOOR - (50 + 6 * i) * math.sin(math.pi * p)
                kw["beak"] = math.sin(math.pi * p)
                sq = 1 + 0.15 * math.sin(math.pi * p)
                rot = 0.12 * (1 if i % 2 else -1) * math.sin(math.pi * p)
        return x, y, kw, 0.0, red, sq, rot
    if t < T_BIG:
        p = seg(t, T_INHALE, T_BIG)
        kw = dict(look=(1, -0.3), eyes="shut", beak=0.0)
        return x, y, kw, ease(p) * 0.9, 0.6 + 0.4 * p, 1 + 0.1 * p, -0.15 * ease(p)
    if t < T_BIG_END:
        kw = dict(look=(1, 0), eyes="shut", beak=1.0)
        return x + 4 * math.sin(t * 70), y, kw, 0.0, 1.0 - 0.4 * seg(t, T_BIG, T_BIG_END), 1.12, 0.12
    # pants, then pleased with itself
    q = t - T_BIG_END
    kw = dict(look=(1, 0), eyes="shut", beak=0.3 * abs(math.sin(q * 9)) if q < 1.6 else 0.0)
    sq = 1 - 0.05 * abs(math.sin(q * 9)) if q < 1.6 else 1.0
    if t >= T_ANSWER:
        kw = dict(look=(0, -1), eyes="wide", beak=0.0)
        if t >= T_LOOKUP[0]:
            kw["look"] = (-0.5, -1)
    return x, y, kw, 0.0, 0.0, sq, 0.0


def draw_squeak(c, t, st):
    x, y, kw, puff, red, sq, rot = st
    s = SQ_S
    c.save(); c.translate(x, y); c.scale(-1, 1); c.translate(-x, -y)      # mirrored: faces left, at the Duck
    squeak_duck(c, x, y, s, sq=sq, rot=rot, t=t, cap_rot=0.38, **kw)
    c.restore()
    if red > 0.02:
        c.save(); c.translate(x, y); c.scale(-1, 1); c.rotate(rot)
        c.scale(S(s) / S(sq) ** 0.5, S(s) * S(sq)); c.translate(4, -142)
        c.arc(0, 0, 50, 0, 2 * math.pi); c.set_source_rgba(1, 0.25, 0.25, 0.38 * red); c.fill()
        c.restore()
    if puff > 0.02:
        c.save(); c.translate(x, y); c.scale(-1, 1); c.rotate(rot)
        c.scale(S(s) / S(sq) ** 0.5, S(s) * S(sq)); c.translate(4, -142)
        r = 14 + 26 * puff
        for cx_ in (-50, 50):
            ellipse(c, cx_ * (1 + 0.25 * puff), 20, r, r * 0.9, SQ_Y, lw=5)
            ellipse(c, cx_ * (1 + 0.25 * puff), 24, r * 0.6, r * 0.4, (1, 0.55, 0.6), stroke=False)
        c.restore()


# ---------------- the others ----------------
def dill_state(t):
    """(x, y, kw, sq)."""
    if t < ARRIVE[1]:
        p = ease(seg(t, ARRIVE[0], ARRIVE[1]))
        return lerp(1250, DI_X, p), FLOOR - abs(math.sin(t * 11)) * 14 * (p < 1), dict(mood="proud", look=(-1, 0), arm="up"), 1.0
    kw = dict(mood="proud", look=(-1, 0.3), arm="up")
    rot = 0.0
    if T_BELL - 0.3 <= t < T_BELL + 0.5:
        kw = dict(mood="smug", look=(-1, 0), arm="up")
        rot = -0.08 * math.sin(math.pi * seg(t, T_BELL - 0.3, T_BELL + 0.5))
    if T_BELL + 0.5 <= t < T_CHEER:
        kw = dict(mood="frozen", look=(-1, 0.3), arm="down")      # holds his breath too
        if t >= T_BREATH:
            kw["mood"] = "shocked"
    if T_CHEER <= t < T_BURST:
        kw = dict(mood="proud", look=(-1, 0.3), arm="up")
        rot = 0.1 * math.sin((t - T_CHEER) * 7)                    # waves the sword like a flag
        if t >= T_BURST - 1.0:
            kw = dict(mood="shocked", look=(-1, 0.3), arm="up")
            rot = 0.0
    if T_BURST <= t < T_WIN:
        kw = dict(mood="shocked", look=(-1, 0), arm="up")
    if T_WIN <= t < T_UP:
        kw = dict(mood="proud", look=(-1, 0.2), arm="point_l")
        rot = 0.0
    if T_UP <= t < T_INHALE:
        kw = dict(mood="angry", look=(-1, 0), arm="reach")
        rot = 0.04 * math.sin(t * 30)
    if T_INHALE <= t < T_BIG:
        kw = dict(mood="shocked", look=(-1, 0), arm="reach")
    if T_BIG <= t < T_BIG_END:
        kw = dict(mood="shocked", look=(-1, 0), arm="reach")
        rot = 0.2 * ease(seg(t, T_BIG, T_BIG + 0.3)) + 0.03 * math.sin(t * 50)
        return DI_X + 30 * ease(seg(t, T_BIG, T_BIG + 0.4)), FLOOR, dict(kw, rot=rot), 1.0
    if t >= T_BIG_END:
        x = DI_X + 30 * (1 - ease(seg(t, T_BIG_END, T_BIG_END + 0.6)))
        kw = dict(mood="frozen", look=(-1, 0), arm="down")
        if t >= T_ANSWER:
            kw = dict(mood="shocked", look=(0, -1), arm="down")
        return x, FLOOR, kw, 1.0
    kw["rot"] = rot
    return DI_X, FLOOR, kw, 1.0


def crumb_state(t):
    """(x, y, kw, ears)."""
    if t < ARRIVE[1] + 0.2:
        p = ease(seg(t, ARRIVE[0] + 0.2, ARRIVE[1] + 0.2))
        return lerp(-200, CR_X, p), FLOOR - abs(math.sin(t * 11)) * 14 * (p < 1), dict(mood="worried", look=(1, 0), arm="down"), False
    kw = dict(mood="worried", look=(1, 0.2), arm="down")
    y = FLOOR
    if T_CHEER <= t < T_BURST - 0.8:
        k = int((t - T_CHEER) / 0.4) % 2
        kw = dict(mood="sheepish", look=(1, 0), arm="wave" if k else "wave_l")
        y = FLOOR - 30 * abs(math.sin((t - T_CHEER) * math.pi / 0.4))
    if T_BURST - 0.8 <= t < T_WIN:
        kw = dict(mood="scared", look=(1, 0), arm="down")
    if T_WIN <= t < T_UP:
        ph = (t - T_WIN) / 0.45
        kw = dict(mood="sheepish", look=(1, -0.3), arm="wave" if int(ph) % 2 else "wave_l")
        y = FLOOR - 60 * abs(math.sin(math.pi * ph))
        if t >= T_UP - 0.6:
            kw = dict(mood="worried", look=(1, 0), arm="down"); y = FLOOR
    if T_UP <= t < T_BIG_END:
        kw = dict(mood="scared", look=(1, 0), arm="none")
        if t >= T_BIG:
            kw["rot"] = -0.18 * ease(seg(t, T_BIG, T_BIG + 0.3)) + 0.03 * math.sin(t * 50)
        return CR_X - (25 * ease(seg(t, T_BIG, T_BIG + 0.4)) if t >= T_BIG else 0), y, kw, True
    if t >= T_BIG_END:
        kw = dict(mood="dizzy", look=(1, 0), arm="down")
        if t >= T_SILENT:
            kw = dict(mood="worried", look=(1, 0), arm="down")
        if t >= T_ANSWER:
            kw = dict(mood="scared", look=(0.3, -1), arm="down")
        return CR_X - 25 * (1 - ease(seg(t, T_BIG_END, T_BIG_END + 0.6))), FLOOR, kw, False
    return CR_X, y, kw, False


def peep_kw(t):
    kw = dict(mood="happy", wings="down", look=(-1, 0), face=-0.5)
    dy, rot = 0.0, 0.0
    if T_BELL + 0.5 <= t < T_CHEER:
        kw["mood"] = "shock"
    if T_CHEER <= t < T_BURST:
        ph = ((t - T_CHEER) % 0.5) / 0.5
        dy = -60 * math.sin(math.pi * ph)
        kw.update(mood="chirp", wings="flap")
    if T_BURST <= t < T_WIN:
        kw.update(mood="shock")
    if T_WIN <= t < T_UP:
        kw.update(mood="blink", wings="down", look=(-1, 0.5))
    if T_UP <= t < T_BIG_END:
        kw.update(mood="blink", wings="hug")
        if t >= T_BIG:
            rot = 0.35 * ease(seg(t, T_BIG, T_BIG + 0.3)) + 0.05 * math.sin(t * 40)
            kw["helmet_rot"] = -0.22 + 2.5 * ease(seg(t, T_BIG, T_BIG + 0.5))
    if t >= T_BIG_END:
        kw.update(mood="shock", wings="down", helmet_rot=-0.22 + 2.5 * (1 - ease(seg(t, T_BIG_END + 0.6, T_BIG_END + 1.2))))
        if t >= T_ANSWER:
            kw["look"] = (0, -1)
    kw["rot"] = rot
    return dy, kw


def chip_state(t):
    if t < ARRIVE[1] + 0.4:
        p = ease(seg(t, ARRIVE[0] + 0.5, ARRIVE[1] + 0.4))
        return lerp(1250, CH_X, p), FLOOR, dict(mood="shy", look=(-1, 0))
    kw = dict(mood="shy", look=(-1, 0.3))
    x = CH_X
    if T_BREATH <= t < T_BURST:
        kw = dict(mood="scared", look=(-1, 0), shiver=0.5)
    if T_BURST <= t < T_WIN:
        kw = dict(mood="eep", look=(-1, 0), arms="cover")
    if T_WIN <= t < T_UP:
        kw = dict(mood="happy", look=(-1, 0), arms="up")
    if T_UP <= t < T_BIG_END:
        kw = dict(mood="eep", look=(-1, 0), arms="cover")
        if t >= T_BIG:
            x = CH_X + 60 * ease(seg(t, T_BIG, T_BIG + 0.5))
            kw["rot"] = 0.15 + 0.03 * math.sin(t * 50)
    if t >= T_BIG_END:
        x = CH_X + 60 * (1 - ease(seg(t, T_BIG_END + 0.3, T_BIG_END + 1.0)))
        kw = dict(mood="scared", look=(-1, 0))
        if t >= T_ANSWER:
            kw = dict(mood="scared", look=(-0.3, -1), shiver=1.0)
    return x, FLOOR, kw


# ---------------- camera ----------------
KEYS = [(0.0, 410, 1220, 2.05), (1.0, 410, 1220, 2.05), (2.5, 540, 1110, 1.22), (T_BELL + 0.4, 540, 1110, 1.22),
        (T_BELL + 1.0, 410, 1220, 2.1), (T_BREATH + 0.5, 410, 1220, 2.2), (T_CHEER - 0.2, 430, 1210, 2.45),
        (T_CHEER + 0.5, 540, 1110, 1.22), (T_BURST - 1.4, 540, 1110, 1.22), (T_BURST - 0.6, 430, 1220, 2.2),
        (T_BURST + 0.2, 470, 1180, 1.45), (T_FLAT, 470, 1180, 1.35), (T_WIN + 0.3, 520, 1120, 1.22),
        (T_UP - 0.3, 520, 1120, 1.22), (T_UP + 0.4, 500, 1190, 1.6), (TANTRUM[-1], 500, 1190, 1.8),
        (T_BIG - 0.1, 500, 1200, 2.0), (T_BIG + 0.35, 540, 1060, 1.0), (T_BIG_END, 540, 1060, 1.0),
        (T_BIG_END + 0.8, 520, 1120, 1.25), (T_ANSWER, 520, 1120, 1.25), (T_LOOKUP[1], 540, 870, 1.05),
        (END_T, 560, 760, 1.15)]


def camera(t):
    cx, cy, z = keyed(KEYS, t)
    shakes = [(T_BELL, 6, 0.2), (T_BURST, 8, 0.3), (T_FLAT, 6, 0.2), (T_CARTON[1], 16, 0.4)]
    shakes += [(s0, 2 + i, 0.2) for i, s0 in enumerate(TANTRUM)]
    shakes += [(d + T_FALL, 8, 0.2) for d in DROPS]
    for (t0, q0, d) in shakes:
        if t0 <= t < t0 + d:
            q = q0 * (1 - seg(t, t0, t0 + d)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    if T_BIG <= t < T_BIG_END:
        q = 14; cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    return cx, cy, z


# ---------------- the scene ----------------
def jello_wob(t):
    w = 0.0
    if T_BIG <= t < T_BIG_END + 1.5:
        q = t - T_BIG
        w += (1.4 if t < T_BIG_END else 1.4 * math.exp(-(t - T_BIG_END) * 3)) * math.sin(q * 26)
    for d in (T_BURST + 0.4,):
        if d <= t < d + 1:
            w += 0.8 * math.exp(-(t - d) * 4) * math.cos((t - d) * 22)
    return w


def scene(c, t):
    L = light_at(t)
    fridge24(c, L, t)
    frost(c, t, 1.0)
    ceiling(c, L)
    ceiling_vent(c, L)
    butter_rink(c, 1.0)
    splats(c, 30.0)
    mist(c, t, 0.35)
    scarf_flat(c, 610, FLOOR + 2)
    ellipse(c, 880 + 40, TOP + 2, 200, 12, (0.72, 0.88, 1.0), lw=3)

    jello(c, JX, FLOOR, jello_wob(t))

    # --- Chip ---
    chx, chy, chkw = chip_state(t)
    draw_chip(c, t, chx, chy, chkw, 1.0)

    # --- Dill + Peep on his head ---
    dx, dy, dkw, dsq = dill_state(t)
    draw_dill_full(c, t, dx, dy, dkw, "stand", dsq)
    pdy, pkw = peep_kw(t)
    rot = dkw.get("rot", 0.0)
    hx = dx + math.sin(rot) * (DILL_HEAD - 18)
    hy = dy - math.cos(rot) * (DILL_HEAD - 18)
    fat_peep(c, hx, hy + pdy, FAT, flap_t=t, **pkw)

    # --- Crumb ---
    crx, cry, ckw, ears = crumb_state(t)
    crumb_bitten(c, crx, cry, 1.0, **ckw)
    if ears:
        # hands clamped to the sides of his head
        c.save(); c.translate(crx, cry); c.rotate(ckw.get("rot", 0.0))
        c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for sgn in (-1, 1):
            c.move_to(sgn * 70, -120); c.line_to(sgn * 112, -150); c.line_to(sgn * 96, -190)
        c.stroke()
        c.restore()

    # --- the Duck (never moves) ---
    gaze = 1.8
    tilt = 0.35
    if t >= T_LOOKUP[0]:
        k = ease(seg(t, T_LOOKUP[0] + 0.3, T_LOOKUP[1] + 0.3))
        tilt = lerp(0.35, 0.75, k)          # the Duck's one motion: it turns its head toward the vent
    clean_duck(c, DUCK_X, FLOOR, tilt=tilt, gaze=gaze, s=DUCK_S, sparkle_t=t if T_WIN <= t < T_WIN + 1.5 else None)
    if t < POPS[0]:
        soap_bubble_small(c, DUCK_X + 18, FLOOR - 300 * DUCK_S + 10, 34, t)
    if t < POPS[1]:
        soap_bubble_small(c, DUCK_X + 70, FLOOR - 290 * DUCK_S + 30, 16, t + 1)

    # --- Squeak ---
    st = squeak_state(t)
    draw_squeak(c, t, st)
    if T_BREATH + 2 <= t < T_BURST:
        k = int((t - T_BREATH) / 0.9)
        q = ((t - T_BREATH) % 0.9) / 0.9
        drop(c, SQ_X + 80 - 20 * (k % 2), FLOOR - 230 + 60 * q, 1.0)
    # sound rings
    for i, s0 in enumerate(TANTRUM):
        sq_rings(c, st[0] - 40, FLOOR - 170, t, s0, 0.7, (1, 0.95, 0.6))
    if T_BIG <= t < T_BIG_END:
        for j in range(4):
            q = ((t - T_BIG) * 1.6 + j / 4) % 1.0
            c.save(); c.translate(SQ_X - 50, FLOOR - 170); c.scale(lerp(80, 900, q), lerp(60, 680, q))
            c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(1, 0.95, 0.6, 0.8 * (1 - q)); c.set_line_width(14); c.stroke()

    icicles(c, t)
    if t >= T_WIN:
        confetti(c, t, T_WIN, DUCK_X, FLOOR - 380, n=50, seed=24)

    # --- the vent answers ---
    if t >= T_PUFF:
        p = seg(t, T_PUFF, T_PUFF + 1.2)
        frost_cloud(c, VENT_X, 120 + 140 * ease(p), 0.6 + 0.5 * p, 1.0 - 0.3 * seg(t, T_PUFF + 2.5, END_T))
        for j in range(10):
            rnd = random.Random(90 + j)
            q = ((t - T_PUFF) * rnd.uniform(0.15, 0.3) + rnd.random()) % 1.0
            star(c, VENT_X + rnd.uniform(-300, 300) + 20 * math.sin(t + j), 120 + q * 1200, 9, t + j, (0.9, 0.97, 1.0))

    drawer_front(c)
    dark_overlay(c, L)

    # --- words ---
    word(c, t, "hmm...", SQ_X + 40, FLOOR - 470, 46, (1, 1, 1), 0.2, 1.1, 0.06)
    word(c, t, "DING!", DI_X + 30, FLOOR - 560, 80, GOLD, T_BELL, T_BELL + 0.6, -0.08)
    for i in range(9):
        t0 = T_BELL + 0.9 + 0.6 * i
        if t0 > T_CHEER - 0.3:
            break
        word(c, t, "tick" if i % 2 == 0 else "tock", 410 + (-90 if i % 2 else 90), FLOOR - 470, 40, (1, 1, 1), t0, t0 + 0.35,
             0.08 if i % 2 else -0.08)
    word(c, t, "twitch", SQ_X + 20, FLOOR - 420, 40, (1, 1, 1), TWITCH[0], TWITCH[1], 0.1)
    word(c, t, "creak...", SQ_X + 10, FLOOR - 380, 40, (1, 1, 1), WOBBLE[0] + 0.2, WOBBLE[1], -0.06)
    word(c, t, "GULP!", SQ_X + 20, FLOOR - 400, 54, (1, 1, 1), T_BREATH - 0.3, T_BREATH + 0.4, 0.06)
    word(c, t, "mmmmm!", SQ_X + 10, FLOOR - 420, 40, RED, T_BREATH + 1.6, T_CHEER - 0.2, -0.05)
    for i in range(6):
        t0 = T_CHEER + 0.3 + 0.9 * i
        if t0 > T_BURST - 2.0:
            break
        word(c, t, "peep! peep!", DI_X + 40, FLOOR - 700, 44, hexc("#FFE066"), t0, t0 + 0.45, -0.06)
        word(c, t, "hup! hup!", CR_X + 40, FLOOR - 470, 44, (1, 1, 1), t0 + 0.45, t0 + 0.9, 0.06)
    word(c, t, "mmmMMMM!!", SQ_X - 40, FLOOR - 460, 52, RED, T_BURST - 1.0, T_BURST, 0.05)
    word(c, t, "PFFFFT!", SQ_X + 40, FLOOR - 520, 96, (1, 1, 1), T_BURST, T_BURST + 0.6, -0.08)
    word(c, t, "boing!", 650, FLOOR - 330, 54, (1, 1, 1), 16.55, 16.9, 0.1)
    word(c, t, "boing!", 215, FLOOR - 360, 54, (1, 1, 1), 17.1, 17.45, -0.1)
    word(c, t, "splat", SQ_X, FLOOR - 200, 54, (1, 1, 1), T_FLAT, T_FLAT + 0.5, 0.06)
    word(c, t, "DING DING DING!", 540, FLOOR - 640, 66, GOLD, T_WIN, T_WIN + 1.3, -0.04)
    word(c, t, "YAAAY!", CR_X + 130, FLOOR - 470, 70, (1, 1, 1), T_WIN + 0.3, T_WIN + 1.6, 0.06)
    word(c, t, "...", DUCK_X, FLOOR - 470, 70, (1, 1, 1), T_WIN + 1.6, T_UP - 0.3, 0.0)
    for i, s0 in enumerate(TANTRUM):
        size = 36 + 7 * i
        word(c, t, "SQUEAK!" if i > 3 else "squeak!", SQ_X + (-20 if i % 2 else 60), FLOOR - 430 - 18 * i, size,
             hexc("#FFE066"), s0, s0 + 0.4, 0.1 if i % 2 else -0.1)
    word(c, t, "HHHHHH...", SQ_X + 40, FLOOR - 480, 54, (1, 1, 1), T_INHALE, T_BIG, 0.05)
    word(c, t, "SQUEEEEEEEAK!!!", 540, 560, 110, hexc("#FFE066"), T_BIG + 0.05, T_BIG_END, -0.06)
    word(c, t, "pop!", DUCK_X + 30, FLOOR - 420, 50, (1, 1, 1), POPS[0], POPS[0] + 0.35, -0.1)
    word(c, t, "pop!", DUCK_X + 90, FLOOR - 380, 40, (1, 1, 1), POPS[1], POPS[1] + 0.35, 0.1)
    word(c, t, "KLONK!", 120, FLOOR - 200, 80, (1, 1, 1), T_CARTON[1], T_CARTON[1] + 0.6, -0.1)
    for k, d in enumerate(DROPS):
        x = ICICLES[k][0]
        word(c, t, "TINK!", x, FLOOR - 120 - 40 * (k % 2), 52, ICY, d + T_FALL, d + T_FALL + 0.35, 0.1 if k % 2 else -0.1)
    word(c, t, "pant pant", SQ_X + 30, FLOOR - 400, 40, (1, 1, 1), T_PANT, T_PANT + 1.4, 0.05)
    word(c, t, "squeak.", SQ_X + 30, FLOOR - 400, 44, hexc("#FFE066"), T_PANT + 1.6, T_SILENT - 0.1, -0.05)
    word(c, t, "squeak.", VENT_X, 500, 120, ICY, T_ANSWER, T_ANSWER + 1.6, 0.04)
    word(c, t, "!!", 540, FLOOR - 700, 100, RED, T_ANSWER + 0.6, T_ANSWER + 1.4, 0.05)


def frame(c, t):
    if t >= END_T:
        end_card(c, t, END_T); return
    random.seed(int(t * 30))
    cx, cy, Z = camera(t)
    c.save(); c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    scene(c, t)
    c.restore()
    if T_BIG <= t < T_BIG + 0.1:
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 0.8, 0.35); c.fill()
    for d in DUNS:
        if d <= t < d + 0.12:
            c.rectangle(0, 0, W, H); c.set_source_rgba(0.1, 0.4, 0.8, 0.14); c.fill()
    if t >= END_T - 0.45:
        ex = W / 2 + (VENT_X - cx) * Z
        ey = H / 2 + (60 - cy) * Z
        iris(c, ex, ey, lerp(1100, 0, ease(seg(t, END_T - 0.45, END_T))))
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
