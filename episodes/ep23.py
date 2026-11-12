"""FRIDGE KINGDOM — Episode 23: "The New Duck". 40.0s, 1080x1920 @ 30fps.

Variant A (title card first, 2s).

With the Duck gone (taken by the Hand in Ep 22), Grandma Gherkin parachutes down from the top shelf on her shawl and
the five Jar pickles hop down after her (fwip x5). They line up and bow to the next Duck they see: Squeak, on Dill's
throne. Squeak, delighted, hops away along the tops of their heads (boop x6) onto the jello. The bowing line turns and
shuffles after it, up onto the jello; Squeak leaps back over them all (WHEEE) and the line whips round: a bowing conga
line chases it to the left to a conga drum. Squeak bounces up onto the milk carton; the line can't stop: BONK BONK
BONK, all six pile up against the carton. Dill sees his chance: he catches Squeak, plonks it back on the throne (ta-da)
and sits beside it like a king's advisor. The pile pops up into a pyramid and bows to them. Squeak hops onto Dill's
head. Peep (on Crumb's head) copies Squeak; Squeak copies Peep back; faster and faster, until Peep leaps over onto
Dill's head beside Squeak. Crumb, left out, offers Peep a crust bit: not noticed. He sits alone; Chip pats him (and
drips on him). Squeak hops back to the throne, right up to the door, and squeaks at it three times. THMP... THMP.
Everyone freezes; the pickles flee. The door opens: the Hand sets the Duck back down beside Squeak, squeaky clean, a
bubble-bath bubble on its turban. The two Ducks slowly turn to face each other. DUN DUN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (crown, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp, back_out, dark_overlay,
                 INK, GOLD, FLOOR, TOP, W, H, FPS, S)
from ep2 import end_card, jello
from ep6 import fridge6, drawer_front, grandma, pickle_kid, PICKLE_STYLES
from ep7 import god_rays
from ep9 import fat_peep, crumb_bitten, bread_bit
from ep10 import ceiling_vent, frost, hand_cuffed
from ep12 import word, hop
from ep13 import ceiling
from ep14 import clean_duck, crumb_tears
from ep15 import drop, chip
from ep16 import keyed, butter_rink, DISH
from ep17 import cape, cape_tie
from ep18 import draw_dill, rot_at, CHS
from ep21 import mist, splats, jello_glob, COLD_X, JX
from ep22 import squeak_duck, scarf_flat, SQ_S

DUR = 40.0
T_START = 2.0
END_T = 38.5
DIM = 0.22
FAT = 1.5
GSC = 1.35                     # Grandma scale
PKS = 1.2                      # Jar pickle scale
DUCK_S = 1.2
RED = (1, 0.35, 0.35)
JT = FLOOR - 150               # jello top
DILL_HEAD = 300
SIT = 0.8

# ---------------- places ----------------
SQ0 = 225                      # Squeak on the throne at the start (end of Ep 22)
THRONE = DISH                  # 420
DUCK_SET = 215                 # where the Hand sets the Duck down
DI_SIT = 590                   # Dill sitting beside the throne
CR_X = 790                     # Crumb after coming out
CR_SIT = 880                   # Crumb sitting alone
CH_X = 1045                    # Chip
WALL = 236                     # the milk carton's front edge (where the line crashes)
SPOTS = [480, 560, 630, 700, 770, 840]          # bow spots: Grandma, kids 0..4
OFFS = [s - 840 for s in SPOTS]                  # offsets from the line anchor (kid 4)
PILE_X = 240
PYR = [(140, 0, 0), (220, 0, 2), (300, 0, 4), (180, 1, 1), (260, 1, 3)]   # (x, row, kid)
PYR_G = 220

# ---------------- timing ----------------
T_JUMPG = 2.05                 # Grandma jumps off the top shelf
T_LANDG = 3.7
KID_JUMP = [2.35 + 0.28 * k for k in range(5)]
T_BOW = 4.15
T_BOWED = 4.5
T_SQ_HAPPY = 4.7
T_HEADHOP = 5.3                # Squeak hops along their heads
HH = 0.17                      # per head
T_ONJELLO = T_HEADHOP + 6 * HH + 0.3     # 6.62
T_TURN = 5.75                  # line turns right
T_LEAP = 7.15                  # Squeak leaps back over the line
T_LEAPLAND = 7.75
T_REVERSE = 7.35               # line whips round
T_CONGA = 7.55
V_CONGA = 250.0
T_CARTON0 = 8.05
T_CARTON = 8.65                # Squeak on the carton top
T_OFFCARTON = 11.35
T_CATCH = 11.9
DILL_UP = 10.55
DILL_WALK = (10.75, 11.6)
T_CARRY = (12.05, 12.6)
T_PLONK = 12.85
T_STEP = (13.0, 13.4)
T_SIT = 13.5
CC_OUT = (12.4, 13.7)          # Crumb and Chip come out from behind the jello
T_PYR = 14.3
T_PBOW = 14.65
T_ONHEAD = 15.8
T_HEADLAND = 16.2
COPY = [("hop", 16.7, "S"), ("hop", 17.25, "P"), ("spin", 17.85, "S"), ("spin", 18.4, "P"),
        ("wiggle", 18.95, "S"), ("wiggle", 19.4, "P"), ("hop", 19.85, "S"), ("hop", 20.2, "P"),
        ("spin", 20.55, "S"), ("spin", 20.85, "P"), ("hop", 21.15, "S"), ("hop", 21.4, "P")]
T_FRENZY = (21.7, 22.9)
T_PEEPJUMP = (23.0, 23.45)
T_OFFER = 23.9
T_OFFER_END = 25.9
T_WALKAWAY = (26.05, 26.85)
T_SITCR = 27.0
PATS = (27.9, 28.45, 29.0)
T_SMILE = 29.5
T_TOTHRONE = (30.0, 30.45)
T_FWD = (30.55, 30.85)
SQUEAKS = (31.0, 31.5, 32.0)
T_BACK = (32.35, 32.6)
STEPS = (32.75, 33.35)
T_FLEE = (33.0, 34.3)
T_OPEN = 34.8
T_HDOWN = 35.0
T_HSET = 35.9
T_HREL = 36.15
T_HGONE = 36.9
T_TURNFACE = (36.95, 37.6)
DUNS = (37.65, 38.05)


def light_at(t):
    if t < T_OPEN:
        return DIM
    return lerp(DIM, 1.0, ease(seg(t, T_OPEN, T_OPEN + 0.35)))


# ---------------- title card (variant A) ----------------
def title_card(c, t):
    g = cairo.RadialGradient(W / 2, 820, 50, W / 2, 820, 1300)
    g.add_color_stop_rgb(0, *hexc("#FFF9DB")); g.add_color_stop_rgb(0.4, *hexc("#FFD43B")); g.add_color_stop_rgb(1, *hexc("#1C2541"))
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    for i, wd in enumerate(["FRIDGE", "KINGDOM"]):
        p = back_out(seg(t, 0.1 + i * 0.25, 0.55 + i * 0.25))
        c.save(); c.translate(W / 2, 600 + i * 170 + 8 * math.sin(t * 6 + i)); c.rotate(0.04 * (1 if i else -1))
        c.scale(S(p), S(p)); text(c, wd, 0, 0, 170, GOLD if i else (1, 1, 1), olw=22); c.restore()
    crown(c, W / 2 + 190, 460, 1.6 * back_out(seg(t, 0.6, 1.0)), 0.25)
    q = ease_out(seg(t, 0.9, 1.3))
    if q > 0:
        c.save(); c.translate(W / 2, 1010 + (1 - q) * 50)
        text(c, "Episode 23:", 0, 0, 60, (1, 1, 1), olw=10)
        text(c, "The New Duck", 0, 100, 104, hexc("#FFF3BF"), outline=INK, olw=14)
        c.restore()
    k = back_out(seg(t, 0.3, 0.8))
    c.save(); c.translate(W / 2, 1700); c.scale(S(0.9 * k), S(0.9 * k))
    hb = abs(math.sin(t * 7)) * 50
    squeak_duck(c, 0, -hb, 1.0, look=(0, 0), eyes="open", beak=0.6 * abs(math.sin(t * 7)), t=t)
    for j in range(3):
        pickle_kid(c, -360 + j * 95, 0, j * 2, look=(1, 0), bow=0.45, arms="down")
    draw_grandma(c, 300, 0, dict(look=(-1, 0), bow=-0.35))
    c.restore()


# ---------------- helpers ----------------
def ground(x):
    """Floor height along the bottom shelf, including the jello hump."""
    d = abs(x - JX)
    if d >= 90:
        return FLOOR
    if d <= 66:
        return JT
    return lerp(JT, FLOOR, ease(seg(d, 66, 90)))


def gran_head(x, y, bow, hop_=0.0):
    a = -0.22 + bow
    return (x + GSC * 140 * math.sin(a), y - hop_ * GSC + GSC * (-10 - 140 * math.cos(a))), a


def draw_grandma(c, x, y, kw, crown_on=True):
    kw = dict(kw)
    bow = kw.get("bow", 0.0)
    hop_ = kw.get("hop", 0.0)
    c.save(); c.translate(x, y); c.scale(GSC, GSC); c.translate(-x, -y)
    grandma(c, x, y, **kw)
    c.restore()
    if crown_on and kw.get("chute", 0.0) < 0.05:
        (hx, hy), a = gran_head(x, y, bow, hop_)
        crown(c, hx, hy, 0.72, a)


def draw_kid(c, x, y, k, **kw):
    c.save(); c.translate(x, y); c.scale(PKS, PKS); c.translate(-x, -y)
    pickle_kid(c, x, y, k, **kw)
    c.restore()


def kid_h(k):
    return (14 + 2 * PICKLE_STYLES[k]["ry"]) * PKS


def soap_bubble_small(c, x, y, r, t):
    c.save(); c.translate(x, y + 3 * math.sin(t * 3))
    c.arc(0, 0, r, 0, 2 * math.pi)
    g = cairo.RadialGradient(-r * 0.3, -r * 0.3, 2, 0, 0, r)
    g.add_color_stop_rgba(0, 1, 1, 1, 0.55); g.add_color_stop_rgba(0.7, 0.85, 0.9, 1, 0.25); g.add_color_stop_rgba(1, 0.9, 0.7, 1, 0.55)
    c.set_source(g); c.fill_preserve()
    c.set_source_rgba(*INK, 0.8); c.set_line_width(4); c.stroke()
    ellipse(c, -r * 0.35, -r * 0.4, r * 0.22, r * 0.13, (1, 1, 1), stroke=False)
    c.restore()


# ---------------- the line (Grandma + 5 pickles) ----------------
# member m: 0 = Grandma, 1..5 = kids 0..4
def anchor(t):
    """x of the line's anchor (kid 4) while it walks as a line."""
    if t < T_TURN:
        return 840.0
    if t < T_REVERSE:
        return lerp(840, 1000, ease(seg(t, T_TURN, T_REVERSE - 0.1)))
    if t < T_CONGA:
        return 1000.0
    return 1000.0 - V_CONGA * (t - T_CONGA)


def crash_t(m):
    """When member m hits the carton (moving left)."""
    x_at_conga = 1000 + OFFS[m]
    return T_CONGA + (x_at_conga - WALL) / V_CONGA


def member(t, m):
    """-> dict(kind, x, y, look, bow, step, rot, mood, extra)"""
    kid = m - 1
    spot = SPOTS[m]
    # arriving from the top shelf
    if t < T_LANDG and m == 0:
        p = seg(t, T_JUMPG, T_LANDG)
        x0, y0 = 560, TOP
        if p <= 0:
            return dict(x=x0, y=y0, look=(1, 1), bow=0.0, chute=0.0, mood="stern")
        if p < 0.18:
            q = p / 0.18
            return dict(x=lerp(x0, x0 + 10, q), y=y0 - 90 * math.sin(math.pi * q * 0.5), look=(0, 1), chute=q, mood="stern")
        q = (p - 0.18) / 0.82
        y = lerp(y0 - 90, FLOOR, ease(q) * 0.5 + q * 0.5)
        x = lerp(x0 + 10, spot, ease(q)) + 26 * math.sin(q * 9)
        ch = 1.0 if q < 0.9 else 1 - (q - 0.9) / 0.1
        return dict(x=x, y=y, look=(-0.5, 1), chute=ch, mood="stern")
    if m > 0 and t < KID_JUMP[kid] + 0.6:
        x0 = 640 + 52 * kid
        if t < KID_JUMP[kid]:
            return dict(x=x0, y=TOP, look=(0, 1), bow=0.0, mood="calm")
        p = seg(t, KID_JUMP[kid], KID_JUMP[kid] + 0.6)
        x, y = hop((x0, TOP), (spot, FLOOR), p, 160)
        return dict(x=x, y=y, look=(0, 1), rot=-2 * math.pi * p * (1 if kid % 2 else -1), mood="shock")
    # bowing to Squeak on the throne
    if t < T_TURN:
        bw = -0.55 * ease(seg(t, T_BOW, T_BOWED))
        lk = (-1, 0)
        return dict(x=spot, y=FLOOR, look=lk, bow=bw, mood="calm" if t < T_BOWED else "closed")
    # whole line walking right / then left (conga)
    if t < T_CONGA or t < crash_t(m):
        x = anchor(t) + OFFS[m]
        y = ground(x)
        moving_right = t < T_REVERSE
        step = (t * 3.2) % 1
        bob = abs(math.sin(t * 2 * math.pi * 1.6 + m)) * 14 if (t < T_REVERSE - 0.1 or t >= T_CONGA) else 0
        if T_REVERSE <= t < T_CONGA:
            # whip round
            return dict(x=x, y=y, look=(-1, 0), bow=0.0, mood="shock", spin=seg(t, T_REVERSE, T_CONGA))
        lk = (1, 0) if moving_right else (-1, 0)
        bw = 0.45 if moving_right else -0.45
        return dict(x=x, y=y - bob, look=lk, bow=bw, step=step, mood="closed", conga=not moving_right)
    # crashed: into the pile
    tc = crash_t(m)
    order = m          # Grandma hits first and ends up at the bottom
    py = FLOOR - 64 * order
    if t < T_PYR:
        p = seg(t, tc, tc + 0.3)
        sq = 1 - 0.35 * math.sin(math.pi * seg(t, tc, tc + 0.12))
        x = lerp(WALL, PILE_X + (8 if order % 2 else -8), p)
        y = lerp(FLOOR, py, ease(p))
        return dict(x=x, y=y, pile=ease(p), sq=sq, mood="shock" if t < tc + 0.6 else "closed", dizzy=t >= tc + 0.3)
    # pyramid, bowing to the throne
    if m == 0:
        x, y = PYR_G, None
    else:
        for (px, row, kk) in PYR:
            if kk == kid:
                x = px
                y = FLOOR if row == 0 else FLOOR - min(kid_h(PYR[j][2]) for j in range(3) if abs(PYR[j][0] - px) < 60) + 10
    if m == 0:
        y = FLOOR - min(kid_h(PYR[j][2]) for j in (3, 4)) - max(kid_h(PYR[j][2]) for j in range(3)) + 22
    p = back_out(seg(t, T_PYR, T_PYR + 0.35))
    if t < T_FLEE[0]:
        x0 = PILE_X
        y0 = FLOOR - 64 * order
        xx, yy = lerp(x0, x, p), lerp(y0, y, p)
        bw = 0.0
        lk = (1, 0)
        if t >= T_PBOW:
            bw = 0.5 * ease(seg(t, T_PBOW + 0.08 * m, T_PBOW + 0.08 * m + 0.25))
        if t >= T_ONHEAD:
            lk = (1, -0.6)
        if STEPS[0] - 0.4 <= t:
            bw, lk = 0.0, (1, 0)
        return dict(x=xx, y=yy, look=lk, bow=bw, mood="closed" if bw > 0.3 else "calm")
    # fleeing left
    p = seg(t, T_FLEE[0] + 0.1 * m, T_FLEE[0] + 0.1 * m + 0.8)
    fx = lerp(x, -260, ease(p) ** 1.3)
    fy = lerp(y, FLOOR, ease(min(1, p * 3))) - abs(math.sin(t * 20 + m)) * 22
    return dict(x=fx, y=fy, look=(-1, 0), bow=-0.3, step=(t * 5) % 1, mood="shock", arms="up")


def draw_member(c, t, m, st):
    kid = m - 1
    x, y = st["x"], st["y"]
    look = st.get("look", (-1, 0))
    mood = st.get("mood", "calm")
    if "pile" in st:
        k = st["pile"]
        sq = st.get("sq", 1.0)
        c.save()
        lift = 34 * k
        c.translate(x, y - lift); c.rotate(-math.pi / 2 * k); c.scale(1, S(sq)); c.translate(-x, -y)
        if m == 0:
            draw_grandma(c, x, y, dict(look=(-1, 0), bow=0.22, mood="closed" if st.get("dizzy") else "angry"), crown_on=False)
        else:
            draw_kid(c, x, y, kid, look=(0, 0), mood="shock" if mood == "shock" else "closed", arms="up")
        c.restore()
        if m == 0:
            (hx, hy), a = gran_head(x, y, 0.22)
            # crown knocked askew, it sits on the pile
            crown(c, x - 150 * k + 10, y - 40, 0.72, -1.3 * k)
        if st.get("dizzy") and m == 5:
            for j in range(3):
                a = t * 4 + j * 2.1
                star(c, PILE_X + 60 * math.cos(a), FLOOR - 64 * 5 - 70 + 18 * math.sin(a), 16, t * 3, GOLD)
        return
    rot = 0.0
    if "spin" in st:
        rot = 0.0
    if m == 0:
        draw_grandma(c, x, y, dict(look=look, bow=st.get("bow", 0.0), chute=st.get("chute", 0.0),
                                   step=st.get("step", 0.0), mood=mood if mood in ("stern", "closed", "angry") else "stern",
                                   cane="drum" if st.get("conga") else "down"))
        return
    arms = st.get("arms", "march" if st.get("conga") else "down")
    sx = 1.0
    if "spin" in st:
        sx = math.cos(math.pi * st["spin"])
    c.save(); c.translate(x, y); c.scale(S(sx) if abs(sx) > 0.05 else 0.05, 1); c.translate(-x, -y)
    draw_kid(c, x, y, kid, look=look, bow=st.get("bow", 0.0), step=st.get("step", 0.0), rot=st.get("rot", 0.0),
             mood=mood, arms=arms)
    c.restore()


# ---------------- Squeak ----------------
def squeak_state(t):
    """(x, y, kw, scale)."""
    kw = dict(look=(1, 0))
    if t < T_SQ_HAPPY:
        lk = (1, 0.3) if t >= T_LANDG - 0.5 else (0.6, -1)
        return SQ0, FLOOR, dict(look=lk, eyes="open"), SQ_S
    if t < T_HEADHOP:
        p = seg(t, T_SQ_HAPPY, T_HEADHOP)
        y = FLOOR - 70 * abs(math.sin(math.pi * 2 * p))
        return SQ0, y, dict(look=(1, 0), beak=abs(math.sin(math.pi * 2 * p)), eyes="wide" if p < 0.3 else "open"), SQ_S
    # hop along the heads: Grandma, kid0..kid4, then onto the jello
    heads = []
    for m in range(6):
        x = SPOTS[m]
        if m == 0:
            (hx, hy), _ = gran_head(x, FLOOR, -0.55)
            heads.append((hx, hy + 10))
        else:
            heads.append((x - 30, FLOOR - kid_h(m - 1) * 0.92))
    pts = [(SQ0, FLOOR)] + heads + [(JX, JT)]
    times = [T_HEADHOP + HH * i for i in range(7)] + [T_ONJELLO]
    if t < T_ONJELLO:
        for i in range(len(pts) - 1):
            if t < times[i + 1]:
                p = seg(t, times[i], times[i + 1])
                h = 150 if i == 0 else (130 if i == len(pts) - 2 else 60)
                x, y = hop(pts[i], pts[i + 1], p, h)
                return x, y, dict(look=(1, 0.3), beak=0.8 * math.sin(math.pi * p), eyes="open"), SQ_S
    if t < T_LEAP:
        ph = ((t - T_ONJELLO) % 0.4) / 0.4
        return JX, JT - 90 * math.sin(math.pi * ph), dict(look=(-1, 0.4), beak=math.sin(math.pi * ph)), SQ_S
    if t < T_LEAPLAND:
        p = seg(t, T_LEAP, T_LEAPLAND)
        x, y = hop((JX, JT), (330, FLOOR), p, 420)
        return x, y, dict(look=(-1, 0), beak=0.8, eyes="wide", rot=2 * math.pi * p), SQ_S
    if t < T_CARTON0:
        p = seg(t, T_LEAPLAND, T_CARTON0)
        x, y = hop((330, FLOOR), (285, FLOOR), p, 70)
        return x, y, dict(look=(-1, 0), beak=0.4), SQ_S
    if t < T_CARTON:
        p = seg(t, T_CARTON0, T_CARTON)
        x, y = hop((285, FLOOR), (110, FLOOR - 500), p, 140)
        return x, y, dict(look=(-1, -1), beak=0.6), SQ_S
    if t < T_OFFCARTON:
        ph = ((t - T_CARTON) % 0.5) / 0.5
        hh = 60 * math.sin(math.pi * ph)
        return 110, FLOOR - 500 - hh, dict(look=(0.5, 1), beak=math.sin(math.pi * ph), eyes="open"), SQ_S
    if t < T_CATCH:
        p = seg(t, T_OFFCARTON, T_CATCH)
        x, y = hop((110, FLOOR - 500), (DILL_WALK[1] - 30, FLOOR - 340), p, 120)
        return x, y, dict(look=(1, 0.5), beak=0.5, rot=0.6 * p), SQ_S
    if t < T_PLONK:
        dx = dill_state(t)[0]
        return dx, FLOOR - 345, dict(look=(-1, 0), beak=0.3 * abs(math.sin(t * 9)), eyes="open"), SQ_S
    if t < T_ONHEAD:
        q = t - T_PLONK
        p = ease(min(1, q / 0.2))
        dx = dill_state(t)[0]
        x = lerp(470, THRONE, p) if q < 0.2 else THRONE
        y = lerp(FLOOR - 345, FLOOR, p) if q < 0.2 else FLOOR
        lk = (1, 0) if t < T_PBOW else (-1, 0)
        return x, y, dict(look=lk, sq=1 - 0.2 * math.exp(-q * 8)), SQ_S
    head_y = FLOOR - DILL_HEAD * SIT + 18
    sx_head = DI_SIT - 25
    if t < T_HEADLAND:
        p = seg(t, T_ONHEAD, T_HEADLAND)
        x, y = hop((THRONE, FLOOR), (sx_head, head_y), p, 200)
        return x, y, dict(look=(1, 0), beak=0.6), SQ_S
    if t < T_TOTHRONE[0]:
        x, y = sx_head, head_y
        kw = dict(look=(1, 0))
        rot = 0.0
        for (mv, t0, who) in COPY:
            if who != "S":
                continue
            d = 0.42
            if t0 <= t < t0 + d:
                p = seg(t, t0, t0 + d)
                if mv == "hop":
                    y -= 120 * math.sin(math.pi * p); kw["beak"] = math.sin(math.pi * p)
                elif mv == "spin":
                    rot = 2 * math.pi * ease(p); y -= 60 * math.sin(math.pi * p)
                else:
                    rot = 0.35 * math.sin(p * 6 * math.pi)
        if T_FRENZY[0] <= t < T_FRENZY[1]:
            ph = ((t - T_FRENZY[0]) % 0.22) / 0.22
            y -= 90 * math.sin(math.pi * ph); kw["beak"] = math.sin(math.pi * ph)
        if t >= T_PEEPJUMP[1]:
            ph = ((t - T_PEEPJUMP[1]) % 0.5) / 0.5
            y -= 50 * math.sin(math.pi * ph)
            kw["look"] = (1, 0.4)
            kw["beak"] = 0.5 * math.sin(math.pi * ph)
        kw["rot"] = rot
        return x, y, kw, SQ_S
    if t < T_TOTHRONE[1]:
        p = seg(t, *T_TOTHRONE)
        x, y = hop((sx_head, head_y), (THRONE, FLOOR), p, 160)
        return x, y, dict(look=(-1, 0), beak=0.5), SQ_S
    if t < T_FWD[0]:
        return THRONE, FLOOR, dict(look=(0, 0)), SQ_S
    if t < T_BACK[0]:
        # comes right up to the door (the camera) and squeaks at it
        k = ease(seg(t, *T_FWD))
        s = lerp(SQ_S, 1.45, k)
        y = FLOOR + 40 * k
        kw = dict(look=(0, 0), eyes="open")
        if T_FWD[0] <= t < T_FWD[1]:
            y -= 60 * math.sin(math.pi * seg(t, *T_FWD))
        for s0 in SQUEAKS:
            if s0 <= t < s0 + 0.4:
                p = seg(t, s0, s0 + 0.4)
                kw["beak"] = math.sin(math.pi * p)
                kw["sq"] = 1.12 if p < 0.5 else 0.94
                kw["eyes"] = "shut" if p < 0.6 else "open"
        return THRONE, y, kw, s
    if t < T_BACK[1]:
        k = ease(seg(t, *T_BACK))
        return THRONE, FLOOR + 40 * (1 - k), dict(look=(1, 0), eyes="wide"), lerp(1.45, SQ_S, k)
    kw = dict(look=(1, -0.3), eyes="wide" if t < T_HSET else "open")
    if t >= T_OPEN:
        kw["look"] = (-0.5, -1)
    if t >= T_HSET:
        kw["look"] = (-1, 0)
    if t >= T_TURNFACE[0]:
        k = ease(seg(t, *T_TURNFACE))
        kw["tilt"] = -0.3 * k
        kw["look"] = (-1, 0)
    return THRONE, FLOOR, kw, SQ_S


# ---------------- Dill ----------------
def dill_state(t):
    """(x, y, kw, mode, sq). mode: hide / stand / sit."""
    if t < DILL_UP:
        lk = (-1, -0.3)
        if T_ONJELLO - 0.3 <= t < T_LEAP:
            lk = (0, -1)
        elif T_LEAP <= t:
            lk = (-1, -0.5)
        mood = "shocked" if t >= T_ONJELLO - 0.3 else "sheepish"
        return 975, FLOOR, dict(mood=mood, look=lk), "hide", 1.0
    if t < DILL_WALK[0]:
        return 975, FLOOR + 75 * (1 - ease(seg(t, DILL_UP, DILL_WALK[0]))), dict(mood="smug", look=(-1, -0.6)), "stand", 1.0
    if t < DILL_WALK[1]:
        p = ease(seg(t, *DILL_WALK))
        return lerp(975, 560, p), FLOOR - abs(math.sin(t * 12)) * 16, dict(mood="angry", look=(-1, -1), arm="down"), "stand", 1.0
    if t < T_CATCH:
        return 560, FLOOR, dict(mood="shocked", look=(-1, -1), arm="reach"), "stand", 1.0
    if t < T_PLONK:
        q = t - T_CATCH
        sq = 1 - 0.15 * math.exp(-q * 8)
        x = 560 if t < T_CARRY[0] else lerp(560, 470, ease(seg(t, *T_CARRY)))
        return x, FLOOR - (abs(math.sin(t * 12)) * 12 if T_CARRY[0] <= t < T_CARRY[1] else 0), \
            dict(mood="smug", look=(0, -1), arm="reach"), "stand", sq
    if t < T_STEP[0]:
        return 470, FLOOR, dict(mood="proud", look=(-1, 0), arm="point_l"), "stand", 1.0
    if t < T_SIT:
        p = ease(seg(t, *T_STEP))
        return lerp(470, DI_SIT, p), FLOOR - 30 * math.sin(math.pi * p), dict(mood="smug", look=(-1, 0)), "stand", 1.0
    # sitting beside the throne like a king's advisor
    mood, look, arm = "smug", (-1, 0), "cross"
    if t >= T_PBOW + 0.2:
        mood, look = "proud", (-1, 0)
    sq = 1.0
    if t >= T_HEADLAND:
        mood, look = "angry", (0, -1)
        q = t - T_HEADLAND
        sq = 1 - 0.18 * math.exp(-q * 7) * math.cos(q * 25)
        for (mv, t0, who) in COPY:
            if who == "S" and t0 + 0.3 <= t < t0 + 0.55 and mv == "hop":
                sq = 1 - 0.12 * math.sin(math.pi * seg(t, t0 + 0.3, t0 + 0.55))
        if T_FRENZY[0] <= t < T_FRENZY[1]:
            sq = 1 - 0.08 * abs(math.sin((t - T_FRENZY[0]) * math.pi / 0.22))
            mood = "shocked"
        if T_PEEPJUMP[1] <= t < T_PEEPJUMP[1] + 0.25:
            sq = 1 - 0.15 * math.sin(math.pi * seg(t, T_PEEPJUMP[1], T_PEEPJUMP[1] + 0.25))
        if t >= T_PEEPJUMP[1]:
            mood, look = "angry", (0, -1)
        if t >= T_TOTHRONE[0]:
            look = (-1, 0)
            mood = "shocked" if t < T_TOTHRONE[0] + 0.5 else "angry"
        if t >= STEPS[0]:
            mood, look = "shocked", (1, -0.5)
        if t >= T_OPEN:
            mood, look, arm = "scared", (-1, -1), "down"
        if t >= T_HGONE:
            mood, look = "shocked", (-1, 0)
    return DI_SIT, FLOOR, dict(mood=mood, look=look, arm=arm), "sit", sq


# ---------------- Crumb / Peep / Chip ----------------
def crumb_state(t):
    """(x, y, kw, sitting)."""
    if t < CC_OUT[0]:
        lk = (-1, -0.3)
        if T_ONJELLO - 0.3 <= t < T_LEAP:
            lk = (-0.5, -1)
        return 1050, FLOOR, dict(mood="scared" if t >= T_ONJELLO - 0.3 else "worried", look=lk, arm="none"), "hide"
    if t < CC_OUT[1]:
        p = seg(t, *CC_OUT)
        y = FLOOR + 75 * (1 - ease(min(1, p * 3)))
        x = lerp(1050, CR_X, ease(p))
        return x, y - abs(math.sin(t * 11)) * 12 * (p > 0.3), dict(mood="worried", look=(-1, 0), arm="down"), "stand"
    if t < T_OFFER:
        mood = "sheepish"
        look = (-1, -0.6)
        if t >= T_PEEPJUMP[0]:
            mood, look = "worried", (-1, -0.8)
        return CR_X, FLOOR, dict(mood=mood, look=look, arm="down"), "stand"
    if t < T_WALKAWAY[0]:
        return CR_X, FLOOR, dict(mood="sheepish", look=(-1, -0.8), arm="none"), "offer"
    if t < T_SITCR:
        p = ease(seg(t, *T_WALKAWAY))
        return lerp(CR_X, CR_SIT, p), FLOOR - abs(math.sin(t * 7)) * 8, dict(mood="worried", look=(1, 0.5), arm="down"), "stand"
    mood = "worried"
    look = (0, 0.6)
    if t >= PATS[0]:
        look = (1, -0.2)
    if t >= T_SMILE:
        mood = "sheepish"
    if t >= STEPS[0]:
        mood, look = "scared", (-1, -0.3)
    return CR_SIT, FLOOR, dict(mood=mood, look=look, arm="down"), "sit"


def peep_state(t, crx, cry, crumb_sq):
    """(x, y, kw)."""
    head_cr = cry - 296 * crumb_sq
    if t < T_PEEPJUMP[0]:
        kw = dict(mood="blink", wings="down", look=(-1, 0), face=-0.5)
        dy = 0.0
        rot = 0.0
        if t >= CC_OUT[0]:
            kw["mood"] = "happy"
        if T_LOVE_P <= t:
            kw["mood"] = "happy"
        for (mv, t0, who) in COPY:
            if who != "P":
                continue
            d = 0.42
            if t0 <= t < t0 + d:
                p = seg(t, t0, t0 + d)
                kw["mood"] = "proud"
                if mv == "hop":
                    dy = -120 * math.sin(math.pi * p); kw["wings"] = "flap"
                elif mv == "spin":
                    rot = 2 * math.pi * ease(p); dy = -60 * math.sin(math.pi * p)
                else:
                    rot = 0.35 * math.sin(p * 6 * math.pi)
        if T_FRENZY[0] <= t < T_FRENZY[1]:
            ph = ((t - T_FRENZY[0] + 0.11) % 0.22) / 0.22
            dy = -90 * math.sin(math.pi * ph); kw["wings"] = "flap"; kw["mood"] = "chirp"
        if t < T_ONHEAD:
            kw["look"] = (-1, -0.3)
        kw["rot"] = rot
        return crx, head_cr + dy, kw
    head_y = FLOOR - DILL_HEAD * SIT + 18
    px_head = DI_SIT + 50
    if t < T_PEEPJUMP[1]:
        p = seg(t, *T_PEEPJUMP)
        x, y = hop((crx, head_cr), (px_head, head_y), p, 180)
        return x, y, dict(mood="love", wings="flap", look=(-1, 0), face=-0.5)
    ph = ((t - T_PEEPJUMP[1] + 0.25) % 0.5) / 0.5
    dy = -50 * math.sin(math.pi * ph)
    kw = dict(mood="happy", wings="flap" if dy < -10 else "down", look=(-1, 0), face=-0.5)
    if t >= T_TOTHRONE[0]:
        dy = 0.0
        kw = dict(mood="shock", wings="down", look=(-1, 0.3), face=-0.5)
    if t >= STEPS[0]:
        kw["look"] = (1, -0.3)
    if t >= T_OPEN:
        kw["look"] = (-1, -1)
    if t >= T_HGONE:
        kw["look"] = (-1, 0)
    return px_head, head_y + dy, kw


T_LOVE_P = 99.0


def chip_state(t):
    """(x, y, kw, alpha)."""
    if t < CC_OUT[0] + 0.2:
        return 1000, FLOOR, dict(mood="scared" if t >= T_ONJELLO - 0.3 else "shy", look=(-1, -0.3)), 1.0, "hide"
    if t < CC_OUT[1] + 0.2:
        p = seg(t, CC_OUT[0] + 0.2, CC_OUT[1] + 0.2)
        y = FLOOR + 75 * (1 - ease(min(1, p * 3)))
        return lerp(1000, CH_X, ease(p)), y, dict(mood="shy", look=(-1, 0)), 1.0, "stand"
    kw = dict(mood="shy", look=(-1, -0.4))
    x = CH_X
    if PATS[0] - 0.4 <= t < T_SMILE + 0.5:
        x = lerp(CH_X, 1010, ease(seg(t, PATS[0] - 0.4, PATS[0])))
        kw = dict(mood="happy", look=(-1, 0.3), arms="draw_l")
        for p0 in PATS:
            if p0 <= t < p0 + 0.35:
                kw["rot"] = -0.12 * math.sin(math.pi * seg(t, p0, p0 + 0.35))
        kw["melt"] = 0.12 * ease(seg(t, PATS[0], PATS[-1] + 0.3))
        kw["blush"] = 1.0
    elif t >= T_SMILE + 0.5:
        x = 1010
        kw = dict(mood="happy", look=(-1, 0), melt=0.12)
    if t >= STEPS[0]:
        kw = dict(mood="eep", look=(-1, -0.4), melt=0.12, arms="cover")
    alpha = 1.0
    if t >= STEPS[0] + 0.1:
        alpha = lerp(1.0, 0.3, ease(seg(t, STEPS[0] + 0.1, STEPS[0] + 0.5)))
    return x, FLOOR, kw, alpha, "stand"


# ---------------- the Hand + the Duck ----------------
def hand_state(t):
    if t < T_HDOWN or t >= T_HGONE:
        return None
    tip = FLOOR - 175
    if t < T_HSET:
        return DUCK_SET + 12, lerp(-800, tip, ease_out(seg(t, T_HDOWN, T_HSET))), 0.6
    if t < T_HREL + 0.1:
        return DUCK_SET + 12, tip, 0.6 * (1 - ease(seg(t, T_HREL - 0.15, T_HREL + 0.1)))
    return DUCK_SET + 12, tip - 1800 * ease(seg(t, T_HREL + 0.1, T_HGONE)) ** 1.4, 0.0


def duck_place(t):
    hs = hand_state(t)
    if t < T_HDOWN:
        return None
    if t < T_HSET:
        return DUCK_SET, hs[1] + 175
    return DUCK_SET, FLOOR


# ---------------- camera ----------------
KEYS = [(T_START, 610, 1160, 1.12), (T_LANDG, 620, 1230, 1.25), (T_BOW, 520, 1310, 1.5), (T_HEADHOP, 520, 1310, 1.5),
        (T_ONJELLO, 680, 1280, 1.28), (T_LEAP, 680, 1280, 1.26), (T_LEAPLAND, 560, 1270, 1.2), (T_CARTON, 470, 1230, 1.22),
        (10.4, 470, 1250, 1.24), (DILL_WALK[1], 520, 1270, 1.26), (T_PLONK, 480, 1280, 1.38), (T_SIT, 520, 1280, 1.34),
        (T_PBOW + 0.6, 450, 1230, 1.3), (T_ONHEAD, 520, 1260, 1.4), (T_HEADLAND + 0.2, 690, 1240, 1.75),
        (T_FRENZY[1], 690, 1240, 1.75), (T_PEEPJUMP[1] + 0.2, 680, 1250, 1.62), (T_OFFER_END, 680, 1260, 1.6),
        (T_SITCR + 0.3, 880, 1290, 1.9), (T_SMILE + 0.3, 880, 1290, 1.9), (T_TOTHRONE[0] + 0.2, 520, 1290, 1.5),
        (T_FWD[1], 425, 1220, 2.35), (SQUEAKS[-1] + 0.35, 425, 1220, 2.4), (STEPS[0] - 0.05, 520, 1260, 1.7),
        (STEPS[0] + 0.25, 560, 1270, 1.2), (T_FLEE[1], 560, 1270, 1.2), (T_HSET, 360, 1220, 1.4),
        (T_HGONE, 330, 1300, 1.95), (END_T, 320, 1320, 2.25)]


def camera(t):
    cx, cy, z = keyed(KEYS, t)
    shakes = [(crash_t(m), 6, 0.15) for m in range(6)] + [(s, 12, 0.3) for s in STEPS] + [(T_PLONK, 6, 0.15), (T_OPEN, 6, 0.2)]
    for (t0, q0, d) in shakes:
        if t0 <= t < t0 + d:
            q = q0 * (1 - seg(t, t0, t0 + d)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    return cx, cy, z


# ---------------- the scene ----------------
def draw_chip(c, t, x, y, kw, alpha):
    def d():
        cape(c, x, y, CHS, sway=0.5 * math.sin(t * 3))
        chip(c, x, y, CHS, t=t, **kw)
        cape_tie(c, x, y - 6, CHS)
    if alpha < 0.999:
        from ep16 import glazed
        glazed(c, d, 0.0, alpha)
        for ex in (-19, 19):
            ellipse(c, x + ex * CHS, y - 64 * CHS, 7, 8, INK, stroke=False)
    else:
        d()


def draw_dill_full(c, t, dx, dy, dkw, mode, dsq):
    c.save()
    sq = (SIT if mode == "sit" else 1.0) * dsq
    if sq != 1.0:
        c.translate(dx, dy); c.scale(1 / sq ** 0.4, sq); c.translate(-dx, -dy)
    draw_dill(c, t, dx, dy, dkw)
    jello_glob(c, dx + 6, dy - 300, 1.1)
    c.restore()


def scene(c, t):
    L = light_at(t)
    fridge6(c, L, 0, lid=False)
    frost(c, t, 1.0)
    ceiling(c, L)
    ceiling_vent(c, L)
    god_rays(c, L)
    butter_rink(c, 1.0)
    splats(c, 30.0)
    mist(c, t, 0.35)
    scarf_flat(c, 580, FLOOR + 2)
    # ice-block meltwater + shards on the top shelf (Ep 22)
    ellipse(c, 880 + 40, TOP + 2, 200, 12, (0.72, 0.88, 1.0), lw=3)

    wob = 0.0
    for tt in [T_ONJELLO, T_LEAP] + [T_TURN + (1000 + OFFS[m] - 900) / 160 for m in (4, 5)]:
        if tt <= t < tt + 1.0:
            q = t - tt
            wob += 1.2 * math.exp(-q * 4) * math.cos(q * 22)

    dx, dy, dkw, dmode, dsq = dill_state(t)
    crx, cry, ckw, cmode = crumb_state(t)
    chx, chy, chkw, chalpha, chmode = chip_state(t)
    crumb_sq = 0.85 if cmode == "sit" else 1.0

    # --- hiders behind the jello ---
    def hidden(fn):
        c.save(); c.rectangle(-500, -500, 2500, FLOOR + 500); c.clip(); c.translate(0, 75); fn(); c.restore()
    if dmode == "hide":
        hidden(lambda: draw_dill_full(c, t, dx, dy, dkw, "stand", 1.0))
    if chmode == "hide":
        hidden(lambda: draw_chip(c, t, chx, chy, chkw, 1.0))
    if cmode == "hide":
        def _cr():
            crumb_bitten(c, crx, cry, 1.0, **ckw)
            fat_peep(c, crx, cry - 296, FAT, mood="shock" if t >= T_ONJELLO - 0.3 else "blink", wings="down",
                     look=(-1, -0.5), flap_t=t, face=-0.5)
        hidden(_cr)
    if dmode == "stand" and t < DILL_WALK[0]:
        c.save(); c.rectangle(-500, -500, 2500, FLOOR + 500); c.clip()
        draw_dill_full(c, t, dx, dy, dkw, "stand", 1.0)
        c.restore()
    jello(c, JX, FLOOR, wob)

    # --- the line ---
    states = [member(t, m) for m in range(6)]
    piled = sorted([m for m in range(6) if "pile" in states[m]])
    for m in range(6):
        if m in piled:
            continue
        if t < T_LANDG and m == 0:
            continue
        draw_member(c, t, m, states[m])
    for m in piled:
        draw_member(c, t, m, states[m])
    if t < T_LANDG:
        draw_member(c, t, 0, states[0])

    # --- Chip ---
    if chmode != "hide":
        draw_chip(c, t, chx, chy, chkw, chalpha)

    # --- Crumb + Peep ---
    if cmode != "hide":
        c.save()
        if cmode == "sit":
            c.translate(crx, cry); c.scale(1 / crumb_sq ** 0.4, crumb_sq); c.translate(-crx, -cry)
        crumb_bitten(c, crx, cry, 1.0, **ckw)
        c.restore()
        if cmode == "sit" and T_SITCR + 0.2 <= t < T_SMILE:
            crumb_tears(c, crx, cry - 160 * crumb_sq, t, 0.8)
        # drips from Chip landing on Crumb
        for p0 in PATS:
            if p0 + 0.1 <= t < p0 + 0.6:
                q = seg(t, p0 + 0.1, p0 + 0.6)
                drop(c, crx + 90, cry - 260 + 180 * q * q, 1.2)
        if T_SITCR <= t:
            for j, p0 in enumerate(PATS):
                if t >= p0 + 0.6:
                    ellipse(c, crx + 60 - 22 * j, cry - 160 + 40 * j, 13, 9, (0.65, 0.85, 1.0), lw=3)
    psx, psy, pkw = peep_state(t, crx, cry, crumb_sq)
    if cmode != "hide" and t < T_PEEPJUMP[0]:
        fat_peep(c, psx, psy, FAT, flap_t=t, **pkw)

    # --- Dill ---
    if dmode in ("stand", "sit") and not (dmode == "stand" and t < DILL_WALK[0]):
        draw_dill_full(c, t, dx, dy, dkw, dmode, dsq)

    # --- Peep on Dill's head ---
    if t >= T_PEEPJUMP[0]:
        fat_peep(c, psx, psy, FAT, flap_t=t, **pkw)

    # --- Squeak ---
    sx, sy, skw, ss = squeak_state(t)
    squeak_duck(c, sx, sy, ss, t=t, **skw)

    if cmode == "offer":
        # left arm raised high, holding up a crust bit for Peep
        p = ease(seg(t, T_OFFER, T_OFFER + 0.3))
        lower = ease(seg(t, T_OFFER_END - 0.3, T_OFFER_END))
        wig = 10 * math.sin(t * 9) * (1 - lower)
        hx = crx - 70 - lerp(20, 40, p) * (1 - lower)
        hy = cry - 120 - lerp(0, 330, p) * (1 - lower) + wig
        c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
        c.move_to(crx - 70, cry - 120); c.line_to(hx, hy)
        c.move_to(crx + 70, cry - 120); c.line_to(crx + 100, cry - 70); c.stroke()
        bread_bit(c, hx - 8, hy - 18, 3.0)
        if p > 0.5 and lower < 0.5:
            star(c, hx + 30, hy - 60, 18, t * 4, (1, 1, 1))
    # --- the Duck + the Hand ---
    dp = duck_place(t)
    if dp is not None:
        gaze = 1.0 + 0.8 * ease(seg(t, *T_TURNFACE)) if t >= T_HSET else 0.0
        tilt = 0.35 * ease(seg(t, *T_TURNFACE))
        clean_duck(c, dp[0], dp[1], tilt=tilt, gaze=gaze, s=DUCK_S, sparkle_t=t if t < T_HGONE + 0.6 else None)
        soap_bubble_small(c, dp[0] + 18, dp[1] - 300 * DUCK_S + 10, 34, t)
        soap_bubble_small(c, dp[0] + 70, dp[1] - 290 * DUCK_S + 30, 16, t + 1)
    hs = hand_state(t)
    if hs is not None:
        hand_cuffed(c, hs[0], hs[1], hs[2], duck_turn=0.0)

    drawer_front(c)
    dark_overlay(c, L)

    # --- words ---
    word(c, t, "fwip!", 640, TOP - 120, 60, (1, 1, 1), T_JUMPG + 0.3, T_JUMPG + 0.9, -0.08)
    for k in range(5):
        word(c, t, "fwip!", 700 + 70 * k, TOP + 160 + 30 * (k % 2), 50, (1, 1, 1), KID_JUMP[k] + 0.1, KID_JUMP[k] + 0.55,
             0.1 if k % 2 else -0.1)
    word(c, t, "squeak?", SQ0 + 40, FLOOR - 320, 54, hexc("#FFE066"), T_SQ_HAPPY, T_SQ_HAPPY + 0.6, 0.08)
    for i in range(6):
        t0 = T_HEADHOP + HH * (i + 1)
        word(c, t, "boop", SPOTS[i] + 10, FLOOR - 330 - 20 * (i % 2), 44, (1, 1, 1), t0, t0 + 0.3, 0.1 if i % 2 else -0.1)
    word(c, t, "BOING!", JX - 40, JT - 260, 80, hexc("#FF8FB3"), T_ONJELLO, T_ONJELLO + 0.5, -0.08)
    word(c, t, "WHEEE!", 650, FLOOR - 640, 84, (1, 1, 1), T_LEAP + 0.05, T_LEAPLAND, 0.06)
    word(c, t, "!!", 720, FLOOR - 380, 90, RED, T_REVERSE, T_CONGA + 0.2, 0.06)
    for j in range(4):
        b = T_CONGA + 0.15 + 0.6 * j
        word(c, t, "cha-cha-cha!", 760 - 110 * j, FLOOR - 340 - 25 * (j % 2), 46, (1, 1, 1), b, b + 0.45, -0.06 if j % 2 else 0.06)
    for m in range(6):
        tc = crash_t(m)
        word(c, t, "BONK!", 300 + 15 * m, FLOOR - 130 - 64 * m - 60, 58 + 4 * m, (1, 1, 1), tc, tc + 0.32, 0.1 if m % 2 else -0.1)
    word(c, t, "squeak! squeak!", 230, FLOOR - 700, 54, hexc("#FFE066"), T_CARTON + 0.2, T_CARTON + 1.2, -0.05)
    word(c, t, "ha!", 760, FLOOR - 420, 70, (1, 1, 1), DILL_UP + 0.2, DILL_WALK[0] + 0.4, 0.08)
    word(c, t, "GOTCHA!", 560, FLOOR - 640, 72, (1, 1, 1), T_CATCH, T_CATCH + 0.5, -0.06)
    word(c, t, "TA-DA!", 440, FLOOR - 520, 90, GOLD, T_PLONK, T_PLONK + 0.7, -0.08)
    word(c, t, "ahem.", DI_SIT + 30, FLOOR - 380, 52, (1, 1, 1), T_SIT + 0.1, T_SIT + 0.8, 0.06)
    word(c, t, "POP!", 230, FLOOR - 720, 76, (1, 1, 1), T_PYR, T_PYR + 0.4, 0.08)
    for m in range(6):
        b = T_PBOW + 0.08 * m
        word(c, t, "fwip", 330 + 30 * m, FLOOR - 520 + (30 if m % 2 else 0), 40, (1, 1, 1), b, b + 0.3, 0.1 if m % 2 else -0.1)
    word(c, t, "boing", DI_SIT - 30, FLOOR - 470, 50, (1, 1, 1), T_HEADLAND, T_HEADLAND + 0.4, -0.1)
    word(c, t, "hmph!", DI_SIT + 130, FLOOR - 300, 52, RED, T_HEADLAND + 0.2, T_HEADLAND + 0.9, 0.08)
    for (mv, t0, who) in COPY:
        if who == "S":
            word(c, t, "squeak!", DI_SIT - 70, FLOOR - 560, 42, hexc("#FFE066"), t0, t0 + 0.35, -0.08)
        else:
            word(c, t, "peep!", CR_X + 120, FLOOR - 560, 46, (1, 1, 1), t0, t0 + 0.35, 0.08)
    word(c, t, "squeak! peep! squeak!", 700, FLOOR - 600, 40, (1, 1, 1), T_FRENZY[0], T_FRENZY[1], 0.03)
    word(c, t, "?", CR_X + 60, FLOOR - 400, 80, (1, 1, 1), T_PEEPJUMP[1], T_PEEPJUMP[1] + 0.6, 0.1)
    word(c, t, "hm? hm?", CR_X - 40, FLOOR - 560, 50, (1, 1, 1), T_OFFER + 0.4, T_OFFER_END - 0.4, -0.06)
    word(c, t, "...", CR_X, FLOOR - 400, 70, (1, 1, 1), T_OFFER_END - 0.3, T_WALKAWAY[1], 0.0)
    word(c, t, "sigh...", CR_SIT - 20, FLOOR - 420, 50, (0.8, 0.85, 1.0), T_SITCR + 0.2, PATS[0] - 0.2, -0.05)
    for j, p0 in enumerate(PATS):
        word(c, t, "pat", 1000, FLOOR - 330 - 30 * j, 46, (1, 1, 1), p0, p0 + 0.35, 0.1)
        word(c, t, "drip", CR_SIT + 60, FLOOR - 180, 40, (0.65, 0.85, 1.0), p0 + 0.3, p0 + 0.7, -0.1)
    for i, s0 in enumerate(SQUEAKS):
        word(c, t, "SQUEAK!", THRONE + (-55 if i % 2 else 55), FLOOR - 400 - 20 * i, 42, hexc("#FFE066"), s0, s0 + 0.42,
             0.1 if i % 2 else -0.1)
    for i, s0 in enumerate(STEPS):
        word(c, t, "THMP", 820 - 200 * i, 900 + 40 * i, 96 + 12 * i, (1, 1, 1), s0, s0 + 0.55, 0.06 if i % 2 else -0.06)
    word(c, t, "!!", 640, FLOOR - 640, 100, RED, STEPS[0] + 0.15, STEPS[1] + 0.4, 0.05)
    word(c, t, "zip!", 160, FLOOR - 300, 60, (1, 1, 1), T_FLEE[0] + 0.3, T_FLEE[0] + 0.9, -0.08)
    word(c, t, "plink", DUCK_SET, FLOOR - 400, 50, (1, 1, 1), T_HSET, T_HSET + 0.5, -0.06)


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
    scene(c, t)
    c.restore()
    if t < T_START + 0.3:
        iris(c, W / 2, H / 2, lerp(0, 1300, ease(seg(t, T_START, T_START + 0.3))))
    if T_OPEN <= t < T_OPEN + 0.1:
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.35); c.fill()
    for d in DUNS:
        if d <= t < d + 0.12:
            c.rectangle(0, 0, W, H); c.set_source_rgba(0.1, 0.4, 0.8, 0.14); c.fill()
    if t >= END_T - 0.4:
        mx = (DUCK_SET + THRONE) / 2
        ex = W / 2 + (mx - cx) * Z
        ey = H / 2 + (FLOOR - 170 - cy) * Z
        iris(c, ex, ey, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))


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
