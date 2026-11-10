"""FRIDGE KINGDOM — Episode 19: "The Frozen North". 40.0s, 1080x1920 @ 30fps.

Variant A (title card first): 2s "FRIDGE KINGDOM" title card, then the story.

Inside the freezer. The huge icy eye from Ep 18 slides shut and is gone. Peep pops out of the snow drift; Dill, Chip
and Crumb pop out of theirs. Dill raises his sword (HYAAA!): an icicle grows on the tip and the weight tips him over.
They march into the blizzard. Rumble: three giant frozen peas roll down an ice slope like boulders; everyone runs
(Dill in front, Crumb at the back), dives behind a snow bank, and the peas bounce clean over them.
Dill strikes a hero pose and freezes stiff (popsicle). Chip hugs him: more ice (eep, sorry). Crumb hugs him and Peep,
on Crumb's head, breathes warm air on his face (HAAAH): CRACK, the ice falls off; brrrr. Chip leads the way.
Through an ice-cube-tray canyon (echoing footsteps). Dill shouts HYAAA: the echo knocks an icicle onto his head (BONK).
Light ahead: a great frozen hall. In the middle, a block of ice with a rubber duck frozen inside, wearing the same
bottle-cap crown. Crumb pictures the Duck back home on the jello (it turns its head), looks at the frozen Duck,
back, and again: two Ducks?! A huge shadow with an icicle crown falls across the hall; two icy eyes glow in it.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (crown, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp,
                 back_out, INK, GOLD, W, H, FPS, S)
from ep2 import end_card, jello
from ep7 import the_duck, sq_rings
from ep9 import fat_peep
from ep12 import word, hop
from ep13 import bubble_r
from ep14 import clean_duck
from ep15 import chip, drop
from ep16 import keyed, glazed
from ep17 import cape, cape_tie
from ep18 import draw_dill, draw_crumb, draw_chip, rot_at, lie

DUR = 40.0
T_START = 2.0
END_T = 38.5
FAT = 1.5
CHS = 1.3
FL = 1450
ICE = hexc("#D0EBFF")
ICE_B = hexc("#74C0FC")
ICE_D = hexc("#1971C2")
SNOW = hexc("#F8FCFF")
RED = (1, 0.35, 0.35)
PEA_G = hexc("#8CE99A")

# ---------------- timing ----------------
# A: the blizzard
T_EYE_SHUT = 2.6
T_PPOP = 3.1
POPS = dict(dill=3.7, chip=4.0, crumb=4.3)
T_HYA = 4.85
T_ICICLE = 5.15
T_TIP = 5.45
T_MARCH = 6.0
T_B = 8.0
# B: the peas
T_RUMBLE = 8.3
T_LOOK = 8.6
T_ROLL = 9.2
PEA_T0 = (9.2, 9.5, 9.8)
PEA_R = (125, 100, 145)
PEA_V = 820
T_RUN = 9.7
T_DIVE = 12.9
T_LAND = 13.15
# C: the popsicle
T_UPC = 14.2
T_POSE = 14.6
T_FREEZE = 15.0
T_GASP2 = 15.55
T_CHIPHUG = 15.9
T_EXTRA = 16.25
T_EEP = 16.6
T_THAW = 17.0
T_BREATH = 17.25
T_CRACK = 18.15
T_BRR = 18.35
T_LEAD = 19.2
T_D = 20.0
# D: the canyon
T_SHOUT = 22.4
T_FALLICE = 23.1
T_BONK = 23.5
T_GLOW = 24.5
T_E = 25.5
# E: the hall
T_PUSH = 26.3
T_STING = 26.95
T_GASP3 = 27.75
T_WALK = 28.3
T_ARRIVE = 29.8
T_TOUCH = 30.2
# F: two Ducks?!
T_LOOKBACK = 31.1
T_BUB = 31.25
T_BDUCK = 31.85              # the Duck's one motion (in Crumb's picture of home)
TURNS = (32.45, 32.95, 33.3, 33.6)
T_Q = 34.0
# G: the shadow
T_SHADOW = 35.0
T_TURN = 35.6
T_EYES = 36.3
T_SEE = 36.75                # Chip goes see-through
DUNS = (36.6, 37.1, 37.6)


# ---------------- small helpers ----------------
def snowcap(c, x, y, w):
    """A little heap of snow sitting on a head (x, y = top of the head)."""
    c.move_to(x - w, y + 6)
    c.curve_to(x - w, y - 22, x - w * 0.4, y - 36, x, y - 30)
    c.curve_to(x + w * 0.5, y - 40, x + w, y - 20, x + w, y + 6)
    c.close_path(); c.set_source_rgb(1, 1, 1); c.fill_preserve()
    c.set_source_rgba(*ICE_B, 0.9); c.set_line_width(4); c.stroke()


def mound(c, x, y, w, h, fill=(1, 1, 1), edge=ICE_B):
    if h <= 1:
        return
    c.move_to(x - w, y + 2)
    c.curve_to(x - w * 0.7, y - h, x + w * 0.7, y - h, x + w, y + 2)
    c.close_path(); c.set_source_rgb(*fill); c.fill_preserve()
    c.set_source_rgba(*edge, 0.8); c.set_line_width(5); c.stroke()


def flakes(c, t, x0, x1, y0, y1, n, seed, wind=400, fall=160, rmin=3, rmax=9, col=(1, 1, 1), alpha=1.0):
    rnd = random.Random(seed)
    wd, ht = x1 - x0, y1 - y0
    for j in range(n):
        sp = 0.6 + 0.8 * rnd.random()
        x = x0 + (rnd.random() * wd - t * wind * sp) % wd
        y = y0 + (rnd.random() * ht + t * fall * sp) % ht
        r = rmin + (rmax - rmin) * rnd.random()
        c.new_sub_path(); c.arc(x, y, r, 0, 2 * math.pi)
    c.set_source_rgba(*col, alpha); c.fill()


def streaks(c, t, x0, x1, y0, y1, n, seed, speed=1500, alpha=0.35):
    rnd = random.Random(seed)
    wd = x1 - x0
    c.set_line_width(5); c.set_source_rgba(*ICE_B, alpha)
    for j in range(n):
        y = y0 + rnd.random() * (y1 - y0)
        x = x0 + (rnd.random() * wd - t * speed * (0.6 + rnd.random())) % wd
        c.move_to(x, y); c.line_to(x + 150 + 120 * rnd.random(), y - 18)
    c.stroke()


def icicle(c, x, y, ln, w=10, rot=0.0):
    """Icicle hanging down from (x, y)."""
    if ln < 2:
        return
    c.save(); c.translate(x, y); c.rotate(rot)
    c.move_to(-w, 0); c.line_to(0, ln); c.line_to(w, 0); c.close_path()
    c.set_source_rgba(*hexc("#E7F5FF"), 0.95); c.fill_preserve()
    c.set_source_rgb(*ICE_D); c.set_line_width(3.5); c.stroke()
    c.move_to(-w * 0.3, 4); c.line_to(-w * 0.05, ln * 0.6); c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(2.5); c.stroke()
    c.restore()


def sword_icicle(c, x, y, rot, k):
    """An icicle growing on the tip of Dill's toothpick sword (Dill's sword arm = 'up'). k 0..1."""
    if k <= 0.01:
        return
    c.save(); c.translate(x, y); c.rotate(rot)
    ellipse(c, 150, -382, 16 * k, 13 * k, hexc("#E7F5FF"), lw=3)
    icicle(c, 150, -376, 95 * k, 13 * k, 0.0)
    c.restore()


def wink_star(c, x, y, r, t0, t, dur=0.6):
    if t0 <= t < t0 + dur:
        q = seg(t, t0, t0 + dur)
        star(c, x, y, r * math.sin(math.pi * q), q * 3, (1, 1, 1))


# ---------------- title card ----------------
def title_card(c, t):
    g = cairo.RadialGradient(W / 2, 820, 50, W / 2, 820, 1300)
    g.add_color_stop_rgb(0, *hexc("#F8FCFF")); g.add_color_stop_rgb(0.4, *hexc("#A5D8FF")); g.add_color_stop_rgb(1, *hexc("#1C2541"))
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    flakes(c, t, -50, W + 50, -50, H + 50, 70, 2, wind=120, fall=220, rmin=4, rmax=10, alpha=0.9)
    for i, wd in enumerate(["FRIDGE", "KINGDOM"]):
        p = back_out(seg(t, 0.1 + i * 0.25, 0.55 + i * 0.25))
        c.save(); c.translate(W / 2, 640 + i * 170 + 8 * math.sin(t * 6 + i)); c.rotate(0.04 * (1 if i else -1))
        c.scale(S(p), S(p)); text(c, wd, 0, 0, 170, GOLD if i else (1, 1, 1), olw=22); c.restore()
    crown(c, W / 2 + 190, 500, 1.6 * back_out(seg(t, 0.6, 1.0)), 0.25)
    # icicles dripping off KINGDOM
    for i, x in enumerate((300, 420, 610, 760)):
        icicle(c, x, 880, 70 * ease_out(seg(t, 0.7 + 0.1 * i, 1.1 + 0.1 * i)), 12)
    q = ease_out(seg(t, 0.9, 1.3))
    if q > 0:
        c.save(); c.translate(W / 2, 1060 + (1 - q) * 50)
        text(c, "Episode 19:", 0, 0, 60, (1, 1, 1), olw=10)
        text(c, "The Frozen North", 0, 90, 80, ICE, outline=INK, olw=12)
        c.restore()
    # the team, shivering in a row at the bottom
    k = back_out(seg(t, 0.3, 0.8))
    c.save(); c.translate(W / 2, 1660); c.scale(S(0.62 * k), S(0.62 * k))
    sh = 2.5
    draw_crumb(c, t, -260, 140, dict(mood="worried", look=(1, -1), shake=sh))
    draw_dill(c, t, -40, 140, dict(mood="frozen", look=(1, -1), shake=sh))
    fat_peep(c, 180, 140, FAT, mood="shock", face=0.3, look=(1, -1), shake=sh)
    draw_chip(c, t, 340, 140, dict(mood="scared", look=(-1, -1), shiver=1.0))
    c.restore()
    mound(c, W / 2, 1800, 620, 120)


# =====================================================================
# A: the blizzard
# =====================================================================
A_HOME = dict(dill=300, crumb=560, peep=800, chip=1000)
MARCH_V = 230


def a_x(name, t):
    x = A_HOME[name]
    if t >= T_MARCH:
        x += MARCH_V * (t - T_MARCH)
    return x


def pop_k(t, t0):
    """0 = buried, 1 = up."""
    return back_out(seg(t, t0, t0 + 0.35))


def a_bg(c, t, cx):
    g = cairo.LinearGradient(0, 300, 0, FL)
    g.add_color_stop_rgb(0, *hexc("#A5C8E8")); g.add_color_stop_rgb(1, *SNOW)
    c.rectangle(-1000, -500, 5000, FL + 600); c.set_source(g); c.fill()
    # distant ice ridges (slow parallax)
    off = cx * 0.5
    c.move_to(-1000 + off, FL - 280)
    for k in range(14):
        x = -1000 + off + k * 300
        c.line_to(x + 150, FL - 520 - 120 * ((k * 37) % 3)); c.line_to(x + 300, FL - 280)
    c.line_to(4000, FL); c.line_to(-1000, FL); c.close_path()
    c.set_source_rgba(*hexc("#D0EBFF"), 0.9); c.fill_preserve(); c.set_source_rgba(*ICE_B, 0.6); c.set_line_width(5); c.stroke()
    # snow ground
    c.rectangle(-1000, FL - 10, 5000, 800); c.set_source_rgb(1, 1, 1); c.fill()
    c.move_to(-1000, FL - 10)
    for k in range(40):
        c.curve_to(-1000 + k * 130 + 40, FL - 40, -1000 + k * 130 + 90, FL - 40, -1000 + (k + 1) * 130, FL - 10)
    c.set_source_rgba(*ICE_B, 0.6); c.set_line_width(5); c.stroke()


def big_eye(c, x, y, o, alpha=1.0):
    if o <= 0.01 or alpha <= 0.01:
        return
    c.save(); c.push_group(); c.translate(x, y)
    c.save(); c.scale(190, S(95 * o)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*hexc("#A5D8FF"), 0.85); c.fill()
    c.save(); c.scale(190, S(95 * o)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*hexc("#1864AB"), 0.7); c.set_line_width(6); c.stroke()
    c.save(); c.scale(190, S(95 * o)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.clip()
    ellipse(c, 0, 0, 70, 70, hexc("#4DABF7"), stroke=False)
    ellipse(c, 0, 0, 14, 64, hexc("#0B2A4A"), stroke=False)
    ellipse(c, -25, -25, 14, 10, (1, 1, 1), stroke=False)
    c.pop_group_to_source(); c.paint_with_alpha(alpha); c.restore()


def a_dill_kw(t):
    if t < T_HYA:
        return dict(mood="frozen" if t < POPS["dill"] + 0.6 else "angry", look=(1, -0.5)), 0.0
    if t < T_TIP:
        return dict(mood="angry", look=(1, -1), arm="up"), 0.0
    if t < T_MARCH:
        q = seg(t, T_TIP, T_TIP + 0.35)
        wob = 0.05 * math.sin((t - T_TIP) * 18) * math.exp(-(t - T_TIP) * 3)
        return dict(mood="shocked" if t < T_TIP + 0.3 else "sad", look=(1, 1), arm="up"), 0.42 * ease(q) + wob
    return dict(mood="angry", look=(1, 0), arm="up"), 0.42


def scene_a(c, t, cx):
    a_bg(c, t, cx)
    # the big eye from Ep 18, sliding shut
    if t < T_EYE_SHUT + 0.6:
        o = 1 - ease(seg(t, T_EYE_SHUT, T_EYE_SHUT + 0.35))
        big_eye(c, 880, 900, o, 1 - seg(t, T_EYE_SHUT + 0.3, T_EYE_SHUT + 0.6))
    if T_EYE_SHUT + 0.2 <= t < T_EYE_SHUT + 1.0:   # a swirl of snow where it was
        q = seg(t, T_EYE_SHUT + 0.2, T_EYE_SHUT + 1.0)
        for j in range(12):
            a = j / 12 * 2 * math.pi + q * 4
            ellipse(c, 880 + (60 + 220 * q) * math.cos(a), 900 + (30 + 110 * q) * math.sin(a), 10, 10, (1, 1, 1), lw=2)
    walking = t >= T_MARCH
    sway = lambda ph: (-abs(math.sin((t - T_MARCH) * 7 + ph)) * 14 if walking else 0.0)
    lean = 0.14 if walking else 0.0
    # each character + its drift
    order = [("crumb", POPS["crumb"]), ("peep", T_PPOP), ("chip", POPS["chip"]), ("dill", POPS["dill"])]
    for name, t0 in order:
        x = a_x(name, t)
        k = pop_k(t, t0) if t >= t0 else 0.0
        y = FL + (1 - k) * 330 + sway(hash(name) % 5)
        if k > 0.02 or name == "peep":
            c.save()
            c.rectangle(x - 300, -2000, 600, FL + 2000 + (40 if k > 0.9 else 0)); c.clip()
            rot = lean
            if name == "dill":
                kw, r2 = a_dill_kw(t)
                rot_at(c, x, y, r2 if not walking else lean)
                draw_dill(c, t, x, y, kw)
                sword_icicle(c, x, y, 0.0, ease_out(seg(t, T_ICICLE, T_ICICLE + 0.3)))
                if t < T_MARCH:
                    snowcap(c, x + 4, y - 288, 48)
            elif name == "crumb":
                mood = "scared" if t < t0 + 0.5 else ("sheepish" if T_TIP < t < T_MARCH else "worried")
                rot_at(c, x, y, rot)
                draw_crumb(c, t, x, y, dict(mood=mood, look=(-1, -0.3) if T_TIP < t < T_MARCH else (1, -0.5),
                                            shake=1.5 if walking else 0))
                if t < T_MARCH:
                    snowcap(c, x - 6, y - 268, 60)
            elif name == "peep":
                if t < T_PPOP:
                    c.restore()
                    continue
                if t < T_PPOP + 0.9:
                    mood, face, lk = "shock", 0.0, (0, 0)
                    if t > T_PPOP + 0.45:
                        face = -0.8 * math.sin(math.pi * seg(t, T_PPOP + 0.45, T_PPOP + 0.9))
                        lk = (1 if face > 0 else -1, 0)
                elif T_HYA < t < T_MARCH:
                    mood, face, lk = ("proud" if t < T_TIP else "happy"), -0.5, (-1, -0.5)
                else:
                    mood, face, lk = "happy", 0.5, (1, -0.5)
                rot_at(c, x, y, rot + (0.35 * ease(seg(t, T_TIP, T_TIP + 0.35)) if T_TIP < t < T_MARCH else 0))
                fat_peep(c, x, y, FAT, mood=mood, face=face, look=lk,
                         wings="salute" if T_HYA < t < T_TIP else ("flap" if walking else "down"), flap_t=t)
                if t < T_MARCH:
                    snowcap(c, x - 10, y - 150, 34)
            else:
                rot_at(c, x, y, rot)
                draw_chip(c, t, x, y, dict(mood="giggle" if T_TIP + 0.2 < t < T_MARCH else "shy", look=(-1, -0.3) if T_TIP < t < T_MARCH else (1, -0.5),
                                           shiver=0.5))
                if t < T_MARCH:
                    snowcap(c, x, y - 150, 40)
            c.restore()
        # the drift (collapses when the character pops out)
        dh = 170 * (1 - ease(seg(t, t0, t0 + 0.3))) + 35
        mound(c, x if t < T_MARCH else A_HOME[name], FL + 4, 170, dh)
        if t0 <= t < t0 + 0.7:
            q = seg(t, t0, t0 + 0.7)
            for j in range(8):
                a = math.pi * (0.1 + 0.8 * j / 7)
                ellipse(c, A_HOME[name] - 200 * q * math.cos(a), FL - 80 - 260 * q * math.sin(a) + 300 * q * q,
                        12 * (1 - q) + 2, 12 * (1 - q) + 2, (1, 1, 1), lw=3)
    # Peep's eyes in the drift before it pops (continuity from Ep 18)
    if t < T_PPOP:
        bl = 0.15 if 2.35 < t < 2.45 else 1.0
        for ex in (775, 825):
            ellipse(c, ex, FL - 175, 13, 16 * bl, INK, stroke=False)
            if bl > 0.5:
                ellipse(c, ex - 4, FL - 181, 4, 4, (1, 1, 1), stroke=False)
    # snow and wind
    flakes(c, t, cx - 900, cx + 900, 0, FL + 400, 60, 4, wind=520 if walking else 300, fall=140, rmin=4, rmax=11)
    streaks(c, t, cx - 900, cx + 900, 300, FL + 100, 14 if walking else 6, 7, 1600)
    # words
    word(c, t, "...", 880, 700, 60, (0.4, 0.5, 0.7), 2.0, T_EYE_SHUT, 0.05)
    word(c, t, "POP!", 800, FL - 420, 70, GOLD, T_PPOP, T_PPOP + 0.5, -0.1)
    word(c, t, "peep?", 940, FL - 330, 50, (1, 1, 1), T_PPOP + 0.45, T_PPOP + 1.0, 0.08)
    for name in ("dill", "chip", "crumb"):
        t0 = POPS[name]
        word(c, t, "pop!", A_HOME[name] + 40, FL - (470 if name != "chip" else 330), 54, GOLD, t0, t0 + 0.45, 0.1)
    word(c, t, "HYAAA!", 330, FL - 560, 70, GOLD, T_HYA, T_ICICLE + 0.2, -0.06)
    word(c, t, "crk!", 520, FL - 470, 50, ICE_D, T_ICICLE, T_ICICLE + 0.4, 0.1)
    word(c, t, "CLINK", 560, FL - 330, 60, (1, 1, 1), T_TIP + 0.25, T_TIP + 0.75, 0.1)
    word(c, t, "hee hee", 1000, FL - 300, 44, (1, 1, 1), T_TIP + 0.3, T_MARCH, -0.06)
    word(c, t, "WHOOOOO", cx + 120, 520, 70, ICE_B, T_MARCH + 0.4, T_B, -0.04)


# =====================================================================
# B + C: the pea avalanche, the popsicle
# =====================================================================
BANK = 2350


def ground(x):
    return FL if x >= 0 else FL + 0.7 * x


def pea_state(i, t):
    """(x, y, rot) of giant frozen pea i, or None."""
    r = PEA_R[i]
    t0 = PEA_T0[i]
    x0 = -850 - 60 * i
    if t < t0:
        wob = 0.08 * math.sin(t * 30 + i) if t > T_ROLL - 0.5 else 0
        return x0, ground(x0) - r, wob
    x = x0 + PEA_V * (t - t0)
    if x < BANK:
        return x, ground(x) - r, (x - x0) / r
    # launched off the bank, arcing over the team
    tb = t0 + (BANK - x0) / PEA_V
    q = (t - tb) / 0.75
    xx = lerp(BANK, BANK + 1300, q)
    yy = FL - r - 120 - 520 * math.sin(math.pi * min(q, 1)) if q < 1 else FL - r - 120 + 900 * (q - 1)
    return xx, yy, (x - x0) / r


def frozen_pea(c, x, y, r, rot):
    c.save(); c.translate(x, y); c.rotate(rot)
    ellipse(c, 0, 0, r, r, PEA_G, lw=7)
    ellipse(c, -r * 0.3, -r * 0.3, r * 0.28, r * 0.22, (1, 1, 1), stroke=False)
    for (a, d, s) in ((0.6, 0.55, 0.16), (2.4, 0.6, 0.12), (4.0, 0.5, 0.2), (5.2, 0.7, 0.1)):   # frost patches
        ellipse(c, r * d * math.cos(a), r * d * math.sin(a), r * s, r * s * 0.8, ICE, stroke=False)
    c.move_to(-r * 0.2, r * 0.75); c.line_to(r * 0.35, r * 0.6)
    c.set_source_rgba(*hexc("#2F9E44"), 0.7); c.set_line_width(5); c.stroke()
    c.restore()


B_OFF = dict(crumb=0, peep=160, chip=290, dill=420)
B_REST = dict(crumb=2600, peep=2730, chip=2850, dill=3020)       # where they lie after the dive / stand in C


def b_x(name, t):
    if t < T_RUN:
        base = 250 + 120 * min(t - T_B, T_RUMBLE - T_B) / (T_RUMBLE - T_B)
        return base + B_OFF[name]
    if t < T_DIVE:
        p = seg(t, T_RUN, T_DIVE)
        base = lerp(370, 2450, p * (0.55 + 0.45 * p) / 1.0)
        return base + B_OFF[name]
    p = ease_out(seg(t, T_DIVE, T_LAND))
    return lerp(2450 + B_OFF[name], B_REST[name], p)


def lie_k(t):
    if t < T_DIVE:
        return 0.0
    if t < T_UPC:
        return ease(seg(t, T_DIVE, T_LAND))
    return 1 - back_out(seg(t, T_UPC, T_UPC + 0.3))


def b_bg(c, t, cx):
    g = cairo.LinearGradient(0, -400, 0, FL)
    g.add_color_stop_rgb(0, *hexc("#8DB8E0")); g.add_color_stop_rgb(1, *SNOW)
    c.rectangle(-2000, -1200, 7000, FL + 1300); c.set_source(g); c.fill()
    off = cx * 0.5
    c.move_to(-2000 + off, FL - 200)
    for k in range(20):
        x = -2000 + off + k * 340
        c.line_to(x + 170, FL - 480 - 140 * ((k * 53) % 3)); c.line_to(x + 340, FL - 200)
    c.line_to(5000, FL); c.line_to(-2000, FL); c.close_path()
    c.set_source_rgba(*ICE, 0.9); c.fill_preserve(); c.set_source_rgba(*ICE_B, 0.5); c.set_line_width(5); c.stroke()
    # the ice slope on the left + flat snow
    c.move_to(-1500, ground(-1500)); c.line_to(0, FL); c.line_to(5000, FL); c.line_to(5000, FL + 900); c.line_to(-1500, FL + 900)
    c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill()
    c.move_to(-1500, ground(-1500)); c.line_to(0, FL)
    c.line_to(0, FL + 900); c.line_to(-1500, FL + 900); c.close_path()
    c.set_source_rgba(*hexc("#BDE0FE"), 0.95); c.fill()
    c.move_to(-1500, ground(-1500)); c.line_to(0, FL); c.line_to(5000, FL)
    c.set_source_rgba(*ICE_B, 0.8); c.set_line_width(6); c.stroke()
    for k in range(6):   # shine lines on the slope
        x = -1400 + 230 * k
        c.move_to(x, ground(x) + 30); c.line_to(x + 120, ground(x + 120) + 30)
        c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(6); c.stroke()


def frost_shell(c, x, y, k, extra, t, crack=0.0):
    """Ice encasing Dill in his hero pose (sword arm up). k 0..1 freeze, extra 0..1 = Chip's hug made it worse."""
    if k <= 0.01 or crack >= 1:
        return
    a = 1 - crack
    c.save(); c.push_group()
    c.translate(x, y)
    rrect(c, -128, -420, 330, 425, 60)
    c.set_source_rgba(*hexc("#A5D8FF"), 0.5 * k); c.fill_preserve()
    c.set_source_rgba(*ICE_D, 0.8 * k); c.set_line_width(6); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.85 * k); c.set_line_width(9)
    c.move_to(-95, -340); c.line_to(-60, -390); c.stroke()
    c.move_to(-100, -280); c.line_to(-30, -390); c.stroke()
    c.move_to(150, -90); c.line_to(180, -140); c.stroke()
    for (ix, ln) in ((-90, 50), (-40, 34), (20, 60), (90, 40), (150, 52)):
        icicle(c, ix, -16, ln * k, 9)
    if extra > 0:
        for (ix, iy, ln) in ((-128, -260, 70), (202, -300, 80), (-128, -150, 50), (202, -180, 60), (40, -420, 0)):
            if ln:
                icicle(c, ix, iy, ln * extra, 11, 0.6 if ix < 0 else -0.6)
        for j in range(6):   # spiky frost crystals on top
            sx = -100 + 55 * j
            c.move_to(sx - 14, -416); c.line_to(sx, -416 - 50 * extra); c.line_to(sx + 14, -416); c.close_path()
            c.set_source_rgba(*hexc("#E7F5FF"), 0.95); c.fill_preserve(); c.set_source_rgb(*ICE_D); c.set_line_width(3); c.stroke()
    if crack > 0:
        c.set_source_rgb(*ICE_D); c.set_line_width(5)
        c.move_to(30, -420); c.line_to(0, -300); c.line_to(50, -200); c.line_to(10, -60); c.stroke()
        c.move_to(-128, -230); c.line_to(-40, -250); c.line_to(0, -300); c.stroke()
    c.pop_group_to_source(); c.paint_with_alpha(a); c.restore()


def shards(c, x, y, t, t0):
    if not (t0 <= t < t0 + 1.0):
        return
    q = t - t0
    rnd = random.Random(19)
    for j in range(16):
        a = rnd.random() * math.pi * 2
        v = 500 + 500 * rnd.random()
        sx = x + 50 + math.cos(a) * v * q
        sy = y - 210 + math.sin(a) * v * q * 0.7 + 1400 * q * q
        s = 22 + 26 * rnd.random()
        c.save(); c.translate(sx, sy); c.rotate(q * 8 + a)
        c.move_to(-s, -s * 0.4); c.line_to(s * 0.7, -s * 0.6); c.line_to(s * 0.2, s * 0.8); c.close_path()
        c.set_source_rgba(*hexc("#D0EBFF"), 0.95 * (1 - q)); c.fill_preserve()
        c.set_source_rgba(*ICE_D, 1 - q); c.set_line_width(3); c.stroke()
        c.restore()


def breath_puffs(c, x0, y0, x1, y1, t, t0, t1):
    if not (t0 <= t < t1):
        return
    for j in range(6):
        q = ((t - t0) * 1.6 + j / 6) % 1
        x = lerp(x0, x1, q); y = lerp(y0, y1, q) - 20 * math.sin(q * 6)
        r = 14 + 40 * q
        c.new_path(); c.arc(x, y, r, 0, 2 * math.pi)
        c.set_source_rgba(1, 0.75, 0.45, 0.55 * (1 - q)); c.fill()


def c_dill_kw(t):
    """(kw, freeze k, extra, crack)"""
    if t < T_POSE:
        return dict(mood="shocked", look=(-1, -0.4)), 0, 0, 0
    if t < T_FREEZE:
        return dict(mood="proud", look=(1, -0.5), arm="up"), 0, 0, 0
    k = ease(seg(t, T_FREEZE, T_FREEZE + 0.4))
    extra = ease_out(seg(t, T_EXTRA, T_EXTRA + 0.35))
    crack = seg(t, T_CRACK, T_CRACK + 0.25)
    if t < T_CRACK:
        return dict(mood="frozen", look=(1, -0.5), arm="up"), k, extra, 0
    if t < T_LEAD:
        sh = 7 if T_BRR <= t < T_BRR + 0.8 else 0
        return dict(mood="shocked" if t < T_BRR else ("sad" if t < T_BRR + 0.8 else "smug"), look=(-1, 0), arm="up" if t < T_BRR else "down", shake=sh), 1, 1, crack
    return dict(mood="angry", look=(1, -0.3), arm="up"), 1, 1, 1


def c_chip_x(t):
    if t < T_CHIPHUG:
        return B_REST["chip"]
    if t < T_EEP:
        return lerp(B_REST["chip"], 3135, ease(seg(t, T_CHIPHUG, T_CHIPHUG + 0.25)))
    if t < T_LEAD:
        return lerp(3135, 3260, ease(seg(t, T_EEP, T_EEP + 0.3)))
    return lerp(3260, 3700, ease(seg(t, T_LEAD + 0.2, T_D + 0.2)))


def c_crumb_x(t):
    if t < T_THAW:
        return B_REST["crumb"]
    if t < T_CRACK + 0.2:
        return lerp(B_REST["crumb"], 2870, ease(seg(t, T_THAW, T_THAW + 0.3)))
    return lerp(2870, 2830, ease(seg(t, T_CRACK + 0.1, T_CRACK + 0.4)))


def c_peep_pos(t, crx):
    """Peep hops onto Crumb's head for the warm breath."""
    home = (B_REST["peep"], FL)
    head = (crx + 5, FL - 262)
    if t < T_THAW + 0.05:
        return home[0], home[1], False
    if t < T_BREATH:
        x, y = hop(home, head, seg(t, T_THAW + 0.05, T_BREATH), 160)
        return x, y, False
    if t < T_CRACK + 0.35:
        return head[0], head[1], True
    if t < T_CRACK + 0.7:
        x, y = hop(head, (crx - 150, FL), seg(t, T_CRACK + 0.35, T_CRACK + 0.7), 120)
        return x, y, False
    return crx - 150, FL, False


def scene_bc(c, t, cx):
    b_bg(c, t, cx)
    mound(c, BANK, FL + 4, 210, 170)
    lk = lie_k(t)
    running = T_RUN <= t < T_DIVE
    in_c = t >= T_UPC
    # --- team ---
    # Crumb
    crx = b_x("crumb", t) if not in_c else c_crumb_x(t)
    bob = (lambda ph: -abs(math.sin(t * 13 + ph)) * 30 if running else 0.0)
    looking_back = T_LOOK <= t < T_RUN
    if not in_c or t < T_THAW:
        kw = dict(mood="scared" if (running or looking_back) else "worried", look=(-1, -1) if looking_back else (1, -0.4),
                  arm="wave" if running else "down")
        if in_c:
            kw = dict(mood="scared" if t >= T_GASP2 else "worried", look=(1, -0.5))
        c.save(); rot_at(c, crx, FL, 0.18 if running else 0.0); lie(c, crx, FL + bob(0), lk, 1, 70)
        draw_crumb(c, t, crx, FL + bob(0), kw)
        c.restore()
    # Peep
    if not in_c:
        px = b_x("peep", t)
        c.save(); lie(c, px, FL + bob(1), lk, 1, 60)
        fat_peep(c, px, FL + bob(1), FAT, mood="shock" if (running or looking_back) else "happy",
                 face=-0.6 if looking_back else 0.6, look=(-1, -1) if looking_back else (1, 0),
                 wings="flap" if running else "down", flap_t=t * 2, rot=0.15 if running else 0)
        c.restore()
    # Chip
    chx = b_x("chip", t) if not in_c else c_chip_x(t)
    if in_c:
        if t < T_CHIPHUG:
            ckw = dict(mood="eep" if t >= T_GASP2 else "shy", look=(1, -0.5), arms="out" if t >= T_GASP2 else "down")
        elif t < T_EEP:
            ckw = dict(mood="happy", look=(-1, 0), arms="out", blush=0.6)
        elif t < T_LEAD:
            ckw = dict(mood="eep" if t < T_CRACK else "giggle", look=(-1, -0.3), arms="cover" if t < T_CRACK else "down",
                       blush=0.8 if t < T_CRACK else 0.0)
        else:
            ckw = dict(mood="happy", look=(1, -0.3), arms="draw" if int(t * 4) % 2 else "up")
    else:
        ckw = dict(mood="scared" if (running or looking_back) else "shy", look=(-1, -1) if looking_back else (1, -0.3),
                   arms="up" if running else "down", shiver=1.0 if looking_back else 0.3)
    if not in_c or t < T_D:
        c.save(); rot_at(c, chx, FL, 0.15 if running else 0.0); lie(c, chx, FL + bob(2), lk, 1, 80)
        draw_chip(c, t, chx, FL + bob(2), ckw)
        c.restore()
    # Dill
    dx = b_x("dill", t) if not in_c else B_REST["dill"]
    if not in_c:
        dkw = dict(mood="shocked" if (running or looking_back) else "angry", look=(-1, -0.8) if looking_back else (1, -0.3),
                   arm="reach" if running else "down")
        c.save(); rot_at(c, dx, FL, 0.2 if running else 0.0); lie(c, dx, FL + bob(3), lk, 1, 76)
        draw_dill(c, t, dx, FL + bob(3), dkw)
        c.restore()
        fk, extra, crack = 0, 0, 0
    else:
        dkw, fk, extra, crack = c_dill_kw(t)
        c.save(); lie(c, dx, FL, lk, 1, 76)
        draw_dill(c, t, dx, FL, dkw)
        c.restore()
        frost_shell(c, dx, FL, fk, extra, t, crack)
        shards(c, dx, FL, t, T_CRACK)
    # in C: Crumb hugging (in front of Dill), Peep on his head
    if in_c and t >= T_THAW:
        hug = t < T_CRACK + 0.2
        kw = dict(mood="worried" if hug else "sheepish", look=(1, -0.5), arm="none" if hug else "down")
        draw_crumb(c, t, crx, FL, kw)
        if hug:
            c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
            c.move_to(crx + 70, FL - 150); c.curve_to(crx + 120, FL - 175, crx + 150, FL - 180, crx + 180, FL - 165); c.stroke()
            c.move_to(crx - 70, FL - 140); c.curve_to(crx - 20, FL - 60, crx + 110, FL - 70, crx + 175, FL - 105); c.stroke()
        ppx, ppy, breathing = c_peep_pos(t, crx)
        fat_peep(c, ppx, ppy, FAT, mood="chirp" if breathing else "happy", face=0.8, look=(1, 0),
                 wings="flap" if breathing else "down", flap_t=t)
        if breathing:
            breath_puffs(c, ppx + 60, ppy - 80, dx + 10, FL - 230, t, T_BREATH, T_CRACK + 0.1)
    elif in_c:
        fat_peep(c, B_REST["peep"], FL, FAT, mood="shock" if t >= T_GASP2 else "happy", face=0.6, look=(1, -0.5))
    # --- peas ---
    for i in range(3):
        x, y, r = pea_state(i, t)
        if -2000 < x < 4200:
            frozen_pea(c, x, y, PEA_R[i], r)
    # snow kicked up at the bank
    for i in range(3):
        tb = PEA_T0[i] + (BANK - (-850 - 60 * i)) / PEA_V
        if tb <= t < tb + 0.6:
            q = seg(t, tb, tb + 0.6)
            for j in range(7):
                ellipse(c, BANK + 60 - 200 * q * math.cos(j), FL - 160 - 200 * q * abs(math.sin(j * 1.3)) + 300 * q * q,
                        14 * (1 - q) + 2, 14 * (1 - q) + 2, (1, 1, 1), lw=3)
    flakes(c, t, cx - 1100, cx + 1100, -600, FL + 400, 45, 8, wind=300, fall=120, rmin=4, rmax=9)
    # --- words ---
    word(c, t, "rumble rumble...", 280, FL - 650, 54, (0.35, 0.45, 0.65), T_RUMBLE, T_LOOK + 0.6, -0.05)
    word(c, t, "?", 400, FL - 400, 70, (1, 1, 1), T_LOOK, T_ROLL, 0.1)
    word(c, t, "RUMBLE!", -700, ground(-700) - 420, 80, PEA_G, T_ROLL, T_ROLL + 0.8, -0.1)
    word(c, t, "AAAAAH!", b_x("crumb", t) + 220, FL - 520, 80, RED, T_RUN, T_RUN + 1.3, -0.06)
    word(c, t, "AAAAAH!", b_x("crumb", t) + 260, FL - 560, 70, RED, 11.4, 12.4, 0.06)
    word(c, t, "dive!", 2650, FL - 420, 58, GOLD, T_DIVE, T_LAND + 0.3, -0.08)
    for i in range(3):
        tb = PEA_T0[i] + (BANK - (-850 - 60 * i)) / PEA_V
        word(c, t, "FWOOMP", 2500 + 180 * i, FL - 760 + 60 * i, 56, PEA_G, tb, tb + 0.5, -0.1 + 0.1 * i)
    word(c, t, "phew...", 2750, FL - 380, 50, (1, 1, 1), T_UPC, T_POSE, 0.05)
    word(c, t, "HMPH!", B_REST["dill"] - 80, FL - 520, 60, GOLD, T_POSE, T_FREEZE + 0.1, -0.06)
    word(c, t, "crackle", B_REST["dill"] + 70, FL - 520, 54, ICE_D, T_FREEZE, T_FREEZE + 0.6, 0.08)
    word(c, t, "GASP!", 2700, FL - 420, 60, RED, T_GASP2, T_CHIPHUG, -0.06)
    word(c, t, "CRACKLE", B_REST["dill"] + 130, FL - 560, 56, ICE_D, T_EXTRA, T_EXTRA + 0.5, 0.06)
    word(c, t, "eep!", 3230, FL - 300, 56, (1, 1, 1), T_EEP, T_THAW + 0.2, 0.1)
    word(c, t, "HAAAAH", 2830, FL - 520, 58, hexc("#FF922B"), T_BREATH + 0.1, T_CRACK, -0.05)
    word(c, t, "CRACK!", B_REST["dill"] + 40, FL - 520, 84, (1, 0.9, 0.4), T_CRACK, T_CRACK + 0.5, 0.08)
    word(c, t, "brrrrrr", B_REST["dill"] + 20, FL - 480, 54, ICE_B, T_BRR, T_BRR + 0.8, -0.05)
    word(c, t, "drip", B_REST["dill"] - 80, FL - 60, 40, (1, 1, 1), T_CRACK + 0.3, T_CRACK + 0.9, 0.1)
    if T_LEAD + 0.2 <= t < T_D:   # Chip points the way: a little arrow, no words
        k = back_out(seg(t, T_LEAD + 0.2, T_LEAD + 0.45))
        ax = c_chip_x(t) + 40; ay = FL - 300
        c.save(); c.translate(ax, ay); c.scale(S(k), S(k))
        c.move_to(-40, -14); c.line_to(20, -14); c.line_to(20, -36); c.line_to(60, 0); c.line_to(20, 36); c.line_to(20, 14)
        c.line_to(-40, 14); c.close_path(); c.set_source_rgb(*GOLD); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        c.restore()


# =====================================================================
# D: the ice-cube-tray canyon
# =====================================================================
D_OFF = dict(chip=0, peep=-140, crumb=-290, dill=-460)
D_V = 230


def d_lead(t):
    """Chip's x."""
    x = 700 + D_V * (t - T_D)
    if t > T_GLOW:
        x = 700 + D_V * (T_GLOW - T_D) + 120 * ease_out(seg(t, T_GLOW, T_GLOW + 0.6))
    return x


def d_bg(c, t, cx):
    g = cairo.LinearGradient(0, 0, 0, FL)
    g.add_color_stop_rgb(0, *hexc("#16325C")); g.add_color_stop_rgb(1, *hexc("#3D78B8"))
    c.rectangle(-1000, -1000, 5000, FL + 1000); c.set_source(g); c.fill()
    # the glow at the canyon's end (the hall)
    gk = 0.35 + 0.65 * ease(seg(t, T_GLOW - 0.5, T_GLOW + 0.5))
    rg = cairo.RadialGradient(2900, FL - 300, 50, 2900, FL - 300, 900)
    rg.add_color_stop_rgba(0, 1, 1, 1, gk); rg.add_color_stop_rgba(1, 0.8, 0.93, 1, 0)
    c.rectangle(-1000, -1000, 5000, FL + 1000); c.set_source(rg); c.fill()
    # tray cells: tall translucent plastic walls with giant faceless ice cubes inside
    for k in range(-1, 8):
        x0 = k * 420
        if x0 > 2500:
            break
        rrect(c, x0 + 30, 380, 360, FL - 380 - 60, 30)
        c.set_source_rgba(*hexc("#A5D8FF"), 0.35); c.fill_preserve()
        c.set_source_rgba(*hexc("#D0EBFF"), 0.9); c.set_line_width(8); c.stroke()
        # the giant cube inside
        rrect(c, x0 + 70, 600, 280, 260, 40)
        c.set_source_rgba(*hexc("#E7F5FF"), 0.75); c.fill_preserve()
        c.set_source_rgba(*ICE_B, 0.9); c.set_line_width(5); c.stroke()
        c.move_to(x0 + 100, 640); c.line_to(x0 + 160, 620); c.set_source_rgba(1, 1, 1, 1); c.set_line_width(8); c.stroke()
        ellipse(c, x0 + 270, 780, 12, 12, (1, 1, 1), lw=2)
        # rim
        rrect(c, x0 + 10, 350, 400, 46, 20); c.set_source_rgb(*hexc("#4DABF7")); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        for ix in (x0 + 70, x0 + 200, x0 + 330):
            icicle(c, ix, 394, 40 + 30 * ((ix // 70) % 3), 10)
    # the arch
    c.move_to(2600, FL); c.line_to(2600, 600); c.curve_to(2600, 380, 3000, 380, 3000, 600); c.line_to(3000, FL)
    c.set_source_rgba(1, 1, 1, 0.8 * gk); c.fill()
    # floor
    c.rectangle(-1000, FL, 5000, 700); c.set_source_rgb(*hexc("#B9DDFB")); c.fill()
    c.move_to(-1000, FL); c.line_to(4000, FL); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    for k in range(-2, 12):
        c.move_to(k * 420, FL + 10); c.line_to(k * 420 - 120, FL + 600)
        c.set_source_rgba(*hexc("#74C0FC"), 0.6); c.set_line_width(5); c.stroke()


def d_icicle_y(t, x):
    """The icicle that falls onto Dill's head."""
    if t < T_FALLICE:
        return 394 + 3 * math.sin(t * 40) * (t > T_SHOUT + 0.3)
    return min(394 + 2400 * (t - T_FALLICE) ** 2 * 2.2, FL)


def scene_d(c, t, cx):
    d_bg(c, t, cx)
    lead = d_lead(t)
    walking = t < T_GLOW
    tip = lambda ph: -abs(math.sin((t - T_D) * 6 + ph)) * 22 if walking else 0.0
    dxp = lead + D_OFF["dill"]
    # the falling icicle, from above Dill's position at the shout
    ice_x = 700 + D_V * (T_FALLICE + 0.4 - T_D) + D_OFF["dill"] + 10
    # Dill
    dmood = "angry"
    arm = "down"
    bonked = T_BONK <= t < T_BONK + 1.0
    if T_SHOUT <= t < T_SHOUT + 0.7:
        dmood, arm = "angry", "up"
    elif T_SHOUT + 0.7 <= t < T_BONK:
        dmood = "shocked"
    elif bonked:
        dmood = "frozen"
    elif t >= T_GLOW:
        dmood = "shocked"
    sq = 1 - 0.25 * math.sin(math.pi * seg(t, T_BONK, T_BONK + 0.3)) if T_BONK <= t < T_BONK + 0.3 else 1.0
    draw_dill(c, t, dxp, FL + tip(0.3), dict(mood=dmood, look=(1, -1) if t > T_SHOUT + 0.7 and t < T_BONK else (1, -0.3), arm=arm,
                                            sq=sq, shake=4 if bonked else 0))
    if bonked:
        for j in range(3):
            a = (t - T_BONK) * 6 + j * 2.1
            star(c, dxp + 90 * math.cos(a), FL - 330 + 25 * math.sin(a), 20, a, GOLD)
    # Crumb
    crx = lead + D_OFF["crumb"]
    draw_crumb(c, t, crx, FL + tip(1.2), dict(mood="worried" if t < T_SHOUT else ("scared" if t < T_BONK + 0.6 else "worried"),
                                             look=(-1, -0.5) if T_SHOUT <= t < T_BONK + 0.8 else (1, -0.3)))
    # Peep copies Chip's tiptoe (bigger)
    pxp = lead + D_OFF["peep"]
    fat_peep(c, pxp, FL + tip(2.0) * 1.6, FAT, mood="proud" if walking else "shock", face=0.6, look=(1, -0.3),
             wings="salute" if walking and int(t * 3) % 2 else "down")
    # Chip leads on tiptoe
    draw_chip(c, t, lead, FL + tip(2.6), dict(mood="shy" if walking else "eep", look=(1, -0.3),
                                             arms="cover" if T_SHOUT <= t < T_BONK else ("out" if walking else "up")))
    # the icicle
    if T_SHOUT <= t < T_BONK + 0.05:
        y = d_icicle_y(t, ice_x)
        icicle(c, ice_x, y - 60 if t >= T_FALLICE else y, 120, 18)
    if T_BONK <= t < T_BONK + 1.4:   # broken bits on the floor
        for j, ox in enumerate((-60, 40, 90)):
            icicle(c, dxp + ox, FL - 8, 30, 8, 1.4 + j)
    # echoing footsteps
    for j, t0 in enumerate((20.3, 21.1, 21.9, 23.9)):
        for e in range(3):
            te = t0 + e * 0.22
            word(c, t, "tap", lead - 100 + 130 * e, FL - 560 - 50 * e - 40 * j % 80, 46 - 8 * e, (0.75, 0.88, 1.0), te, te + 0.35, 0.05)
    # the shout and its echo
    word(c, t, "HYAAA!", dxp + 30, FL - 470, 66, GOLD, T_SHOUT, T_SHOUT + 0.6, -0.06)
    for e in range(3):
        te = T_SHOUT + 0.35 + 0.25 * e
        word(c, t, "...aaa", dxp + 260 + 170 * e, FL - 640 - 70 * e, 50 - 8 * e, (0.75, 0.88, 1.0), te, te + 0.45, 0.05)
    word(c, t, "shhh!", crx - 60, FL - 380, 50, (1, 1, 1), T_SHOUT + 0.5, T_FALLICE + 0.2, 0.08)
    word(c, t, "BONK!", dxp + 40, FL - 440, 80, (1, 0.9, 0.4), T_BONK, T_BONK + 0.6, -0.08)
    word(c, t, "ooooh...", lead - 160, FL - 460, 56, (1, 1, 1), T_GLOW + 0.3, T_E, -0.05)


# =====================================================================
# E/F/G: the great frozen hall
# =====================================================================
BX = 1500
BW, BH = 380, 420
BTOP = FL - 60 - BH
E_HOME = dict(chip=520, peep=680, dill=860, crumb=1040)
E_END = dict(chip=790, peep=915, dill=1040, crumb=1225)


def hall_bg(c, t, dim):
    g = cairo.LinearGradient(0, -200, 0, 1150)
    g.add_color_stop_rgb(0, *hexc("#0F2A4F")); g.add_color_stop_rgb(1, *hexc("#3E7CC0"))
    c.rectangle(-1000, -1000, 5000, 2300); c.set_source(g); c.fill()
    # back wall: an ice castle silhouette
    c.move_to(-500, 1150)
    for k in range(9):
        x = -500 + k * 450
        hgt = 420 + 160 * ((k * 7) % 3)
        c.line_to(x, 1150 - hgt)
        for m in range(4):
            c.line_to(x + 40 + m * 100, 1150 - hgt - (40 if m % 2 == 0 else 0))
            c.line_to(x + 90 + m * 100, 1150 - hgt - (40 if m % 2 == 0 else 0))
        c.line_to(x + 450, 1150 - hgt)
    c.line_to(3800, 1150); c.close_path()
    c.set_source_rgba(*hexc("#74C0FC"), 0.35); c.fill()
    # pillars
    for px in (150, 650, 2350, 2850):
        rrect(c, px - 75, 120, 150, 1040, 20)
        gp = cairo.LinearGradient(px - 75, 0, px + 75, 0)
        gp.add_color_stop_rgba(0, 0.75, 0.9, 1, 0.55); gp.add_color_stop_rgba(0.4, 1, 1, 1, 0.75); gp.add_color_stop_rgba(1, 0.6, 0.8, 1, 0.45)
        c.set_source(gp); c.fill_preserve(); c.set_source_rgba(*ICE_D, 0.8); c.set_line_width(5); c.stroke()
    # chandelier icicles
    for k in range(-4, 30):
        x = k * 120
        icicle(c, x, -60, 140 + 90 * ((k * 5) % 3), 18)
    # floor (shiny ice)
    gf = cairo.LinearGradient(0, 1150, 0, 2200)
    gf.add_color_stop_rgb(0, *hexc("#A5D8FF")); gf.add_color_stop_rgb(1, *hexc("#E7F5FF"))
    c.rectangle(-1000, 1150, 5000, 2000); c.set_source(gf); c.fill()
    c.move_to(-1000, 1150); c.line_to(4000, 1150); c.set_source_rgba(*ICE_D, 0.6); c.set_line_width(5); c.stroke()
    for k in range(-6, 16):
        c.move_to(BX + k * 260, 1150); c.line_to(BX + k * 600, 2200)
        c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(4); c.stroke()
    # the arch on the left (where they came in)
    c.move_to(-200, FL + 40); c.line_to(-200, 760); c.curve_to(-200, 560, 220, 560, 220, 760); c.line_to(220, FL + 40)
    c.set_source_rgba(*hexc("#16325C"), 0.85); c.fill()
    # sparkle in the air
    rnd = random.Random(31)
    for j in range(24):
        x = rnd.random() * 3000; y = rnd.random() * 1100
        tw = 0.5 + 0.5 * math.sin(t * 3 + j)
        star(c, x, y, 8 * tw + 2, j, (1, 1, 1))


def ice_block(c, t):
    """The block of ice with a rubber duck (same bottle-cap crown) frozen inside, on a snow pedestal."""
    mound(c, BX, FL + 4, 280, 80)
    # glow behind
    rg = cairo.RadialGradient(BX, BTOP + BH / 2, 40, BX, BTOP + BH / 2, 420)
    rg.add_color_stop_rgba(0, 0.85, 0.95, 1, 0.55); rg.add_color_stop_rgba(1, 0.85, 0.95, 1, 0)
    c.rectangle(BX - 500, BTOP - 300, 1000, BH + 400); c.set_source(rg); c.fill()
    # the duck inside
    the_duck(c, BX, BTOP + BH - 70, 1.15, 1.15, 0.38)
    # the ice
    rrect(c, BX - BW / 2, BTOP, BW, BH, 34)
    gi = cairo.LinearGradient(BX - BW / 2, BTOP, BX + BW / 2, BTOP + BH)
    gi.add_color_stop_rgba(0, 0.85, 0.95, 1, 0.55); gi.add_color_stop_rgba(0.5, 0.65, 0.85, 1, 0.38); gi.add_color_stop_rgba(1, 0.55, 0.78, 1, 0.55)
    c.set_source(gi); c.fill_preserve()
    c.set_source_rgb(*ICE_D); c.set_line_width(8); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.95); c.set_line_width(12); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(BX - BW / 2 + 40, BTOP + 140); c.line_to(BX - BW / 2 + 110, BTOP + 40); c.stroke()
    c.set_line_width(7)
    c.move_to(BX - BW / 2 + 40, BTOP + 220); c.line_to(BX - BW / 2 + 170, BTOP + 50); c.stroke()
    c.move_to(BX + BW / 2 - 40, BTOP + BH - 60); c.line_to(BX + BW / 2 - 80, BTOP + BH - 20); c.stroke()
    for (bx, by, r) in ((BX + 120, BTOP + 70, 10), (BX + 140, BTOP + 110, 6), (BX - 130, BTOP + 330, 8)):
        ellipse(c, bx, by, r, r, (1, 1, 1), lw=2)
    # frost rim on top
    for j in range(7):
        x = BX - BW / 2 + 40 + j * 50
        icicle(c, x, BTOP + BH - 4, 24 + 14 * (j % 3), 8)


def shadow_k(t):
    return ease(seg(t, T_SHADOW, T_SHADOW + 1.4))


def ice_king_shadow(c, t):
    """The huge crowned shadow falling across the hall from the right."""
    k = shadow_k(t)
    if k <= 0:
        return
    sx = lerp(3300, 1750, k)
    c.save(); c.translate(sx, FL + 300); c.scale(2.2, 2.2)
    c.move_to(-380, 0)
    c.curve_to(-400, -300, -300, -470, -170, -500)      # shoulder
    c.curve_to(-200, -560, -170, -640, -120, -660)
    c.curve_to(-140, -800, 140, -800, 120, -660)        # head
    c.curve_to(170, -640, 200, -560, 170, -500)
    c.curve_to(300, -470, 400, -300, 380, 0)
    c.line_to(380, 900); c.line_to(-380, 900)
    c.close_path()
    c.set_source_rgba(0.04, 0.09, 0.22, 0.62); c.fill()
    # the icicle crown
    c.move_to(-130, -745)
    pts = [(-150, -860), (-95, -775), (-60, -900), (-25, -780), (0, -940), (25, -780), (60, -900), (95, -775), (150, -860), (130, -745)]
    for p in pts:
        c.line_to(*p)
    c.close_path(); c.set_source_rgba(0.04, 0.09, 0.22, 0.62); c.fill()
    # glowing icy eyes
    if t >= T_EYES:
        o = ease(seg(t, T_EYES, T_EYES + 0.4))
        for ex in (-45, 45):
            c.save(); c.translate(ex, -690); c.rotate(0.25 if ex < 0 else -0.25)
            c.scale(30, S(13 * o)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(0.55, 0.88, 1.0, 0.95); c.fill()
            ellipse(c, ex, -690, 4, S(11 * o), hexc("#0B2A4A"), stroke=False)
        rg = cairo.RadialGradient(0, -690, 10, 0, -690, 140)
        rg.add_color_stop_rgba(0, 0.55, 0.88, 1, 0.35 * o); rg.add_color_stop_rgba(1, 0.55, 0.88, 1, 0)
        c.rectangle(-200, -850, 400, 320); c.set_source(rg); c.fill()
    c.restore()


def e_x(name, t):
    if t < T_WALK:
        return E_HOME[name]
    return lerp(E_HOME[name], E_END[name], ease(seg(t, T_WALK + 0.1 * (name == "dill"), T_ARRIVE)))


def crumb_look_f(t):
    """Double take: (look, head-whip shake)."""
    if t < T_LOOKBACK:
        return (1, -0.4), 0
    seq = [(-1, 0.6), (1, -0.4), (-1, 0.6), (1, -0.4)]
    lk = (-1, 0.6)
    for i, tt in enumerate(TURNS):
        if t >= tt:
            lk = seq[(i + 1) % 4]
    sh = 4 if any(tt <= t < tt + 0.15 for tt in TURNS) else 0
    return lk, sh


def home_duck_icon(t):
    def f(c):
        # a little jello block with the Duck on top
        rrect(c, -50, 20, 100, 48, 12); c.set_source_rgb(*hexc("#FF6B6B")); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        ellipse(c, -25, 32, 12, 6, (1, 0.8, 0.8), stroke=False)
        q = ease(seg(t, T_BDUCK, T_BDUCK + 0.3))
        clean_duck(c, 0, 24, tilt=lerp(-0.45, 0.1, q), gaze=lerp(-2.0, 0.0, q), frosty=0.7, s=0.36)
        # a little dotted 'home' arrow pointing down
        c.set_source_rgb(*ICE_D); c.set_line_width(4)
        for j in range(3):
            c.new_path(); c.arc(78, -40 + 22 * j, 4, 0, 2 * math.pi); c.fill()
        c.move_to(66, 26); c.line_to(90, 26); c.line_to(78, 44); c.close_path(); c.fill()
    return f


def scene_hall(c, t, cx):
    dim = 0.0
    hall_bg(c, t, dim)
    ice_block(c, t)
    wink_star(c, BX - 120, BTOP + 60, 50, T_STING, t, 0.7)
    wink_star(c, BX + 140, BTOP + 260, 36, T_STING + 0.2, t, 0.7)
    wink_star(c, BX, BTOP - 20, 60, T_STING + 0.1, t, 0.8)
    sk = shadow_k(t)
    turned = t >= T_TURN
    shiver = 3 if turned else 0
    walking = T_WALK <= t < T_ARRIVE
    bob = (lambda ph: -abs(math.sin(t * 9 + ph)) * 18 if walking else 0.0)
    gasp = T_GASP3 <= t < T_WALK
    # Chip
    chx = e_x("chip", t)
    def ch():
        mood = "eep" if gasp else ("scared" if turned else ("happy" if t < T_GASP3 else "shy"))
        draw_chip(c, t, chx, FL + bob(0), dict(mood=mood, look=(1, -1) if turned else (1, -0.4),
                                               arms="cover" if turned else ("out" if gasp else "down"), shiver=1.0 if turned else 0.2))
    if t >= T_SEE:
        glazed(c, ch, k=0.0, alpha=lerp(1.0, 0.28, ease(seg(t, T_SEE, T_SEE + 0.3))))
        if t >= T_SEE + 0.3:
            for ex in (-14, 14):   # only his eyes show
                ellipse(c, chx + ex * 1.3, FL - 92, 9, 11, INK, stroke=False)
    else:
        ch()
    # Peep (copies Crumb's double take), riding on Dill's head after the walk
    pxx = e_x("peep", t)
    pyy = FL + bob(1)
    if t >= T_WALK + 0.4:
        dhx = e_x("dill", t)
        if t < T_WALK + 0.9:
            pxx, pyy = hop((e_x("peep", T_WALK + 0.4), FL), (dhx, FL - 300 + bob(2)), seg(t, T_WALK + 0.4, T_WALK + 0.9), 150)
        else:
            pxx, pyy = dhx, FL - 300 + bob(2)
    pface, plook = 0.6, (1, -0.5)
    if t >= T_LOOKBACK + 0.2 and t < T_SHADOW:
        lk, _ = crumb_look_f(t - 0.18)
        pface, plook = (0.8 if lk[0] > 0 else -0.8), lk
    pmood = "shock" if (gasp or turned or t >= T_Q) else ("love" if T_STING <= t < T_GASP3 else "happy")
    PEEP_DRAW = (pxx, pyy, pmood, pface, plook)
    # Dill
    dxx = e_x("dill", t)
    if turned:
        dkw = dict(mood="frozen", look=(1, -1), shake=shiver)
    elif gasp:
        dkw = dict(mood="shocked", look=(1, -0.4))
    elif t >= T_Q:
        dkw = dict(mood="shocked", look=(1, -0.2))
    elif t >= T_ARRIVE:
        dkw = dict(mood="smug", look=(1, -0.2), arm="point")
    else:
        dkw = dict(mood="proud" if t > T_STING else "angry", look=(1, -0.4))
    draw_dill(c, t, dxx, FL + bob(2), dkw)
    pxx, pyy, pmood, pface, plook = PEEP_DRAW
    fat_peep(c, pxx, pyy, FAT, mood=pmood, face=pface, look=plook, shake=shiver,
             wings="flap" if T_WALK + 0.4 <= t < T_WALK + 0.9 else "down", flap_t=t)
    # Crumb
    crx = e_x("crumb", t)
    if t < T_LOOKBACK:
        ckw = dict(mood="scared" if gasp else "worried", look=(1, -0.4), arm="wave" if T_TOUCH <= t < T_LOOKBACK else "down")
        hop_y = 0
    else:
        lk, sh = crumb_look_f(t)
        mood = "worried" if t < T_Q else "scared"
        if turned:
            lk, mood, sh = (1, -1), "scared", shiver
        ckw = dict(mood=mood, look=lk, shake=sh)
        hop_y = -30 * math.sin(math.pi * seg(t, T_Q, T_Q + 0.3)) if T_Q <= t < T_Q + 0.3 else 0
    draw_crumb(c, t, crx + (15 if T_TOUCH <= t < T_LOOKBACK else 0), FL + bob(3) + hop_y, ckw)
    # thought bubble: the Duck back home
    if T_BUB <= t < T_SHADOW + 0.3:
        bs = back_out(seg(t, T_BUB, T_BUB + 0.3)) * (1 - seg(t, T_SHADOW, T_SHADOW + 0.3)) * 1.25
        bubble_r(c, crx - 230, FL - 560, bs, home_duck_icon(t))
    # the shadow over everything
    ice_king_shadow(c, t)
    if sk > 0:
        c.rectangle(-1000, -1000, 5000, 4000); c.set_source_rgba(0.02, 0.05, 0.15, 0.3 * sk); c.fill()
    # --- words ---
    word(c, t, "ooooh...", 600, FL - 480, 64, (1, 1, 1), T_E + 0.2, T_PUSH, -0.05)
    word(c, t, "!!", BX + 200, BTOP - 80, 90, RED, T_STING, T_STING + 0.7, 0.08)
    word(c, t, "GASP!", 700, FL - 470, 72, RED, T_GASP3, T_WALK + 0.2, -0.06)
    word(c, t, "tink", BX - 230, BTOP + 180, 48, (1, 1, 1), T_TOUCH + 0.1, T_TOUCH + 0.6, 0.1)
    word(c, t, "squeak", crx - 180, FL - 720, 34, GOLD, T_BDUCK, T_BDUCK + 0.5, 0.1)
    for tt in TURNS:
        word(c, t, "boing!", crx + 90, FL - 330, 44, GOLD, tt, tt + 0.3, 0.1)
    word(c, t, "?!", crx + 10, FL - 380, 110, RED, T_Q, T_SHADOW + 0.2, -0.05)
    word(c, t, "??", dxx - 150, FL - 300, 70, (1, 1, 1), T_Q + 0.25, T_SHADOW, 0.08)
    word(c, t, "?", pxx + 60, pyy - 190, 60, (1, 1, 1), T_Q + 0.4, T_SHADOW, -0.08)
    word(c, t, "gulp", crx - 40, FL - 380, 50, (1, 1, 1), T_TURN + 0.3, T_EYES + 0.4, 0.1)
    word(c, t, "eep!", chx - 20, FL - 250, 50, (1, 1, 1), T_SEE, T_SEE + 0.6, -0.1)


# ---------------- cameras ----------------
A_KEYS = [(2.0, 820, 1130, 1.65), (3.35, 820, 1180, 1.65), (3.65, 650, 1230, 1.12), (4.75, 650, 1230, 1.12),
          (5.0, 460, 1230, 1.45), (5.9, 460, 1230, 1.45), (6.4, 650 + MARCH_V * 0.4, 1230, 1.1)]
B_KEYS = [(8.0, 520, 1200, 1.15), (8.6, 560, 1200, 1.15), (9.1, -350, 1000, 0.85), (9.45, -350, 1000, 0.85),
          (9.75, 600, 1150, 0.85)]
C_KEYS = [(T_DIVE - 0.2, 2600, 1200, 0.95), (T_UPC, 2750, 1220, 1.1), (T_POSE, 2960, 1240, 1.6), (T_GASP2, 2940, 1240, 1.6),
          (T_CHIPHUG, 3030, 1240, 1.65), (T_EEP + 0.3, 3030, 1240, 1.65), (T_THAW + 0.2, 2950, 1220, 1.6),
          (T_LEAD, 2980, 1240, 1.5), (T_D, 3250, 1240, 1.4)]
E_KEYS = [(T_E, 1060, 1130, 0.82), (T_PUSH, 1090, 1130, 0.84), (T_STING - 0.15, BX, 1260, 1.6), (T_GASP3 - 0.05, BX, 1240, 1.65),
          (T_GASP3, 780, 1250, 1.45), (T_WALK, 780, 1250, 1.45), (T_ARRIVE, 1150, 1230, 1.3), (T_TOUCH, 1300, 1240, 1.45),
          (T_LOOKBACK, 1260, 1150, 1.45), (T_Q, 1260, 1150, 1.45), (T_SHADOW, 1230, 1150, 1.4),
          (T_TURN + 0.6, 1400, 1000, 0.85), (DUNS[0], 1400, 1000, 0.85), (END_T, 1150, 1180, 1.3)]


def camera(t):
    if t < T_B:
        if t < 6.4:
            cx, cy, z = keyed(A_KEYS, t)
        else:
            cx, cy, z = 650 + MARCH_V * (t - T_MARCH), 1230, 1.1
    elif t < T_RUN:
        cx, cy, z = keyed(B_KEYS, t)
    elif t < T_DIVE - 0.2:
        cx, cy, z = b_x("crumb", t) + 300, 1150, 0.85
        if t < T_RUN + 0.3:
            p = ease(seg(t, T_RUN, T_RUN + 0.3))
            cx = lerp(600, cx, p)
    elif t < T_D:
        cx, cy, z = keyed(C_KEYS, t)
        if t < T_DIVE + 0.1:
            p = ease(seg(t, T_DIVE - 0.2, T_DIVE + 0.1))
            cx = lerp(b_x("crumb", T_DIVE - 0.2) + 300, 2600, p); z = lerp(0.85, 0.95, p)
    elif t < T_E:
        lead = d_lead(t)
        cx, cy, z = lead - 215, 1240, 1.42
    else:
        cx, cy, z = keyed(E_KEYS, t)
    # shakes
    sh = 0
    if T_RUMBLE <= t < T_RUN + 3.2:
        sh = 5 if t < T_ROLL else 7
    for t0, s in [(T_BONK, 14), (T_CRACK, 12), (T_PPOP, 6)] + [(d, 10) for d in DUNS]:
        if t0 <= t < t0 + 0.25:
            sh = max(sh, s * (1 - seg(t, t0, t0 + 0.25)))
    if sh:
        cx += random.uniform(-sh, sh); cy += random.uniform(-sh, sh)
    return cx, cy, z


# ---------------- frame ----------------
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
    c.save(); c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    if t < T_B:
        scene_a(c, t, cx)
    elif t < T_D:
        scene_bc(c, t, cx)
    elif t < T_E:
        scene_d(c, t, cx)
    else:
        scene_hall(c, t, cx)
    c.restore()
    if t < T_START + 0.3:
        iris(c, W / 2, H / 2, lerp(0, 1300, ease(seg(t, T_START, T_START + 0.3))))
    # white gusts between scenes
    for tc in (T_B, T_D, T_E):
        if tc - 0.25 <= t < tc + 0.25:
            a = 1 - abs(t - tc) / 0.25
            c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, a); c.fill()
    if T_STING <= t < T_STING + 0.1:
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.35); c.fill()
    for d in DUNS:
        if d <= t < d + 0.12:
            c.rectangle(0, 0, W, H); c.set_source_rgba(0.1, 0.4, 0.8, 0.12); c.fill()
    if t >= END_T - 0.4:
        crx = E_END["crumb"]
        iris(c, W / 2 + (crx - cx) * Z, H / 2 + (FL - 170 - cy) * Z, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))


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
