"""FRIDGE KINGDOM — Episode 5: "The Usurper". ~39.4s, 1080x1920 @ 30fps.

Variant A (title card first).

The Duck sits in Dill's throne spot wearing a bottle-cap crown. Dill (still yolky) tries
everything: a staring contest (he blinks first and topples), a dance-off (crickets), a full
charge (he bounces off the Duck like a trampoline into the milk carton). Crumb snaps off a
corner of himself as a gift and bows. The Duck squeaks. Once. Dill and Crumb scream, run in
circles and dive behind the jello... and up on the top shelf, the Pickle Jar lid starts to
turn by itself.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crumb, duck, crown, bubble, fridge_bg, dark_overlay, ellipse, rrect, star, text,
                 iris, hexc, seg, ease, ease_out, lerp, back_out, INK, GOLD, FLOOR, TOP, W, H, FPS, S, BREAD, CRUST,
                 GREEN)
from ep2 import title_card, end_card, jello
from ep4 import goo

DUR = 39.4
END_T = 37.4
LIGHT = 0.18          # door closed: dim fridge
DUCK_X = 420          # Dill's throne spot
DILL_X = 720
JELLO_X = 975
GIFT_X = 535
SQUEAK_T = 27.3
CAP_RED, CAP_RED_D = hexc("#E8590C"), hexc("#B8420A")
TEAR = hexc("#74C0FC")
LID_CLICKS = [34.3, 34.9, 35.5, 36.1, 36.7]


# ---------------- new props ----------------
def cap_crown(c, x, y, rot=0.0, s=1.0):
    """Bottle-cap crown: crimped orange-red cap sitting on its rim, bottom centre at (x, y)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(s), S(s))
    c.move_to(-50, 0)
    n = 14
    for i in range(n + 1):           # crimped skirt
        px = -50 + 100 * i / n
        c.line_to(px * (1 - 0.1 * (i % 2)), -6 if i % 2 else 0)
    c.line_to(44, -30); c.line_to(-44, -30); c.close_path()
    c.set_source_rgb(*CAP_RED); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.set_source_rgb(*CAP_RED_D); c.set_line_width(3)
    for i in range(1, n, 2):
        px = -46 + 92 * i / n
        c.move_to(px, -4); c.line_to(px * 0.95, -26); c.stroke()
    ellipse(c, 0, -30, 44, 9, hexc("#FF8A3D"), lw=4)       # top face
    ellipse(c, -16, -31, 10, 3, (1, 1, 1), stroke=False)    # shine
    c.restore()


def the_duck(c, t, sx=1.0, sy=1.0, cap_rot=0.0):
    """The Duck on the throne spot, facing camera, wearing the cap crown. Optional squash about its base."""
    c.save(); c.translate(DUCK_X, FLOOR); c.scale(S(sx), S(sy)); c.translate(-DUCK_X, -FLOOR)
    duck(c, DUCK_X, FLOOR, turn=1.0)
    cap_crown(c, DUCK_X + 6, FLOOR - 186, cap_rot)
    c.restore()


def gift_piece(c, x, y, rot=0.0, s=1.0):
    """The corner Crumb snapped off himself."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(s), S(s))
    c.move_to(-30, 20); c.line_to(-26, -24); c.curve_to(-6, -40, 24, -36, 34, -18); c.line_to(18, -4)
    c.line_to(26, 6); c.line_to(8, 12); c.line_to(14, 22); c.close_path()
    c.set_source_rgb(*CRUST); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    c.move_to(-20, 12); c.line_to(-18, -14); c.curve_to(-4, -26, 14, -24, 22, -14); c.line_to(8, 4); c.close_path()
    c.set_source_rgb(*BREAD); c.fill()
    c.restore()


def crumb_notched(c, x, y, notched, **kw):
    """Crumb, optionally with his top-right corner snapped off (clip follows his bow)."""
    if not notched:
        crumb(c, x, y, **kw); return
    c.save()
    m = c.get_matrix()
    c.translate(x, y); c.rotate(kw.get("rot", 0.0))
    c.translate(0, -20); c.rotate(kw.get("bow", 0.0)); c.translate(0, 20)
    c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.rectangle(-400, -600, 800, 800)
    c.move_to(48, -330); c.line_to(140, -330); c.line_to(140, -200); c.line_to(108, -214)
    c.line_to(96, -238); c.line_to(76, -244); c.line_to(70, -270); c.line_to(52, -280); c.close_path()
    c.clip()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    c.set_matrix(m)
    crumb(c, x, y, **kw)
    c.restore()
    # crumbly broken edge
    c.save(); c.translate(x, y); c.rotate(kw.get("rot", 0.0))
    c.translate(0, -20); c.rotate(kw.get("bow", 0.0)); c.translate(0, 20)
    c.move_to(108, -214); c.line_to(96, -238); c.line_to(76, -244); c.line_to(70, -270); c.line_to(52, -280)
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.restore()


def dill_lids(c, x, y, k_small, k_big, big=1.0):
    """Eyelids over Dill's eyes (assumes rot=0, sq=1, no shake). k = 0 open .. 1 closed."""
    for (ex, ey, r), k in [((-28, -205, 24), k_small), ((30, -212, 34), k_big)]:
        if k <= 0.01:
            continue
        r = r * big
        c.save()
        c.translate(x + ex, y + ey); c.scale(r, r); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.save(); c.clip()
        c.rectangle(x + ex - r - 4, y + ey - r - 4, 2 * r + 8, (2 * r + 4) * k + 4)
        c.set_source_rgb(*GREEN); c.fill()
        c.restore()
        ly = y + ey - r + 2 * r * k
        c.set_source_rgb(*INK); c.set_line_width(5)
        hw = r * math.sqrt(max(0.0, 1 - ((ly - (y + ey)) / r) ** 2))
        c.move_to(x + ex - hw, ly); c.line_to(x + ex + hw, ly); c.stroke()
        ellipse_outline(c, x + ex, y + ey, r)


def ellipse_outline(c, x, y, r):
    c.save(); c.translate(x, y); c.scale(r, r); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()


def tears(c, x, y, t, amt, big=1.0):
    """Watering eyes: drops welling and streaming down."""
    if amt <= 0.01:
        return
    for ex, ey, r in [(-28, -205, 24), (30, -212, 34)]:
        r *= big
        ellipse(c, x + ex, y + ey + r * 0.75, r * 0.85 * amt, r * 0.28 * amt, TEAR, lw=3)
        for j in range(2):
            q = (t * 1.3 + j * 0.5 + ex * 0.01) % 1
            dy = r + q * 120 * amt
            ellipse(c, x + ex + (j * 2 - 1) * r * 0.5, y + ey + dy, 8 * amt, 12 * amt, TEAR, lw=3)


def music_note(c, x, y, s, alpha):
    c.save(); c.translate(x, y); c.scale(S(s), S(s))
    c.set_source_rgba(*INK, alpha); c.set_line_width(6)
    c.move_to(14, 0); c.line_to(14, -60); c.line_to(40, -50); c.stroke()
    c.save(); c.translate(0, 0); c.scale(16, 12); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*hexc("#FFD43B"), alpha); c.fill_preserve(); c.set_source_rgba(*INK, alpha); c.set_line_width(4); c.stroke()
    c.restore()


def cricket(c, x, y, t):
    c.save(); c.translate(x, y)
    ellipse(c, 0, 0, 26, 12, hexc("#2B8A3E"), lw=3)
    ellipse(c, 22, -4, 9, 9, hexc("#2B8A3E"), lw=3)
    c.set_source_rgb(*INK); c.set_line_width(3)
    a = 0.3 * math.sin(t * 40)
    c.move_to(26, -10); c.line_to(48, -36 + 6 * a); c.move_to(22, -12); c.line_to(36, -40 - 6 * a)
    c.move_to(-10, 6); c.line_to(-30, 22); c.move_to(4, 8); c.line_to(-6, 24); c.stroke()
    c.restore()


def jar_lid(c, t):
    """The Pickle Jar lid turning by itself, one click at a time (drawn over fridge_bg's lid)."""
    clicks = sum(ease(seg(t, k, k + 0.12)) for k in LID_CLICKS)
    lift = 5 * clicks
    c.save(); c.translate(170, TOP)
    rrect(c, -100, -370 - lift, 200, 50, 12); c.set_source_rgb(*hexc("#E03131")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    # ridges sliding sideways as it turns
    c.save(); rrect(c, -100, -370 - lift, 200, 50, 12); c.clip()
    off = (clicks * 22) % 28
    c.set_source_rgb(*hexc("#A61E1E")); c.set_line_width(5)
    for i in range(-1, 9):
        px = -100 + i * 28 + off
        c.move_to(px, -364 - lift); c.line_to(px, -326 - lift); c.stroke()
    c.restore()
    # gap of light under the lid
    if lift > 1:
        c.rectangle(-92, -320 - lift, 184, lift); c.set_source_rgb(*hexc("#B2F2BB")); c.fill()
    c.restore()


# ---------------- staging ----------------
def camera(t):
    wide = (590, FLOOR - 230, 1.85)
    if t < 6.0:
        k = ease(seg(t, 2.0, 6.0))
        return 590, FLOOR - 240, lerp(1.75, 1.9, k)
    if t < 7.0:
        k = ease(seg(t, 6.0, 6.9))
        return lerp(590, 575, k), lerp(FLOOR - 240, FLOOR - 225, k), lerp(1.9, 2.2, k)
    if t < 8.4:
        k = seg(t, 7.0, 8.4)
        return DILL_X + 4, FLOOR - 212, lerp(3.4, 3.7, k)                   # Dill's eyes
    if t < 9.2:
        k = seg(t, 8.4, 9.2)
        return DUCK_X + 4, FLOOR - 165, lerp(3.4, 3.6, k)                   # the Duck's blank stare
    if t < 10.0:
        k = seg(t, 9.2, 10.0)
        return DILL_X + 4, FLOOR - 212, lerp(3.7, 4.0, k)
    if t < 11.6:
        k = ease(seg(t, 10.0, 10.4)) * (1 - ease(seg(t, 11.0, 11.6)))
        return lerp(590, 740, k), FLOOR - 230, 1.85
    if t < 17.8:
        return wide
    if t < 21.0:
        k = ease(seg(t, 17.6, 18.3))
        b = ease(seg(t, 19.6, 21.0))
        return lerp(lerp(590, 470, k), 450, b), lerp(lerp(FLOOR - 230, FLOOR - 470, k), FLOOR - 250, b), lerp(lerp(1.85, 1.2, k), 1.8, b)
    if t < 26.0:
        return 450, FLOOR - 250, 1.8
    if t < 29.0:
        k = ease(seg(t, 26.0, 28.9))
        return lerp(450, 435, k), lerp(FLOOR - 250, FLOOR - 220, k), lerp(1.8, 2.15, k)
    if t < 33.0:
        k = ease(seg(t, 29.0, 29.6))
        k2 = ease(seg(t, 31.0, 32.0))
        return lerp(lerp(435, 630, k), 790, k2), lerp(FLOOR - 220, FLOOR - 250, k), lerp(2.15, 1.55, k)
    k = ease(seg(t, 33.0, 34.1))
    return lerp(790, 230, k), lerp(FLOOR - 250, TOP - 230, k), lerp(1.55, 2.1, k)


def dill_state(t):
    """Return (x, y, kwargs, lids, tears, goo?) for Dill, or None."""
    if t < 6.0:   # trembling, pointing at the usurper
        sh = 3 + 5 * seg(t, 2.0, 6.0)
        return dict(x=DILL_X, y=FLOOR, mood="angry", look=(-1, 0), arm="point_l" if t > 2.6 else "down", shake=sh), True
    if t < 10.0:  # staring contest
        jit = 0
        if t >= 7.6:
            jit = 4 * math.sin(t * 70)
        return dict(x=DILL_X + jit, y=FLOOR, mood="frozen", look=(-1, 0), arm="down"), True
    if t < 11.0:  # topples backwards
        p = seg(t, 10.0, 10.45)
        rot = (math.pi / 2) * p * p
        if t >= 10.45:
            rot = math.pi / 2 - 0.08 * math.sin((t - 10.45) * 20) * (1 - seg(t, 10.45, 10.9))
        return dict(x=DILL_X, y=FLOOR, mood="frozen" if t < 10.3 else "shocked", look=(0, -1), rot=rot), False
    if t < 11.4:  # springs back up
        p = back_out(seg(t, 11.0, 11.35))
        return dict(x=DILL_X, y=FLOOR, mood="angry", look=(-1, 0), rot=(math.pi / 2) * (1 - p)), False
    if t < 15.0:  # dance-off: wild flailing
        beat = int((t - 11.4) / 0.24)
        arms = ["reach", "flail", "up", "point_l", "pound", "flail", "reach", "point"]
        hop = abs(math.sin((t - 11.4) * math.pi / 0.48)) * 60
        x = DILL_X + 60 * math.sin((t - 11.4) * 2.2)
        mood = "proud" if beat % 4 != 3 else "smug"
        return dict(x=x, y=FLOOR - hop, mood=mood, look=(-1, -0.2), arm=arms[beat % len(arms)],
                    rot=0.28 * math.sin((t - 11.4) * math.pi / 0.48)), hop < 8
    if t < 16.0:  # final pose... crickets
        x = DILL_X + 60 * math.sin(3.6 * 2.2)
        return dict(x=x, y=FLOOR, mood="smug" if t < 15.5 else "frozen", look=(-1, 0), arm="up", rot=-0.15), True
    if t < 16.6:  # backs up, sword raised
        x0 = DILL_X + 60 * math.sin(3.6 * 2.2)
        x = lerp(x0, 850, ease(seg(t, 16.0, 16.5)))
        return dict(x=x, y=FLOOR, mood="angry", look=(-1, 0), arm="up", shake=3), True
    if t < 17.4:  # CHARGE
        p = seg(t, 16.6, 17.4)
        x = lerp(850, 575, p)
        return dict(x=x, y=FLOOR - abs(math.sin(p * math.pi * 5)) * 30, mood="angry", look=(-1, 0), arm="up", rot=-0.25), False
    if t < 17.7:  # leap onto the Duck
        p = seg(t, 17.4, 17.7)
        x = lerp(575, DUCK_X + 10, p); y = lerp(FLOOR, FLOOR - 200, p) - 160 * math.sin(math.pi * p)
        return dict(x=x, y=y, mood="angry", look=(-1, 0.5), arm="reach", rot=-0.2), False
    if t < 17.95:  # squash on the Duck
        p = math.sin(math.pi * seg(t, 17.7, 17.95))
        return dict(x=DUCK_X + 10, y=FLOOR - 200 + 55 * p, mood="shocked", look=(0, 1), arm="reach", sq=1 - 0.3 * p), False
    if t < 19.0:  # launched up and over into the milk carton
        p = seg(t, 17.95, 19.0)
        x = lerp(DUCK_X + 10, 240, p); y = lerp(FLOOR - 200, FLOOR - 120, p) - 720 * math.sin(math.pi * p)
        return dict(x=x, y=y, mood="shocked", look=(-1, 0), arm="reach", rot=-p * 2 * math.pi), False
    if t < 19.9:  # flat against the carton, sliding down
        p = ease(seg(t, 19.15, 19.9))
        return dict(x=240, y=lerp(FLOOR - 120, FLOOR, p), mood="frozen", look=(0, 0), sq=lerp(0.8, 1.0, p)), False
    if t < 22.6:  # dazed
        return dict(x=240, y=FLOOR, mood="shocked" if t < 21.4 else "frozen", look=(1, 0),
                    rot=0.12 * math.sin(t * 5) * (1 - seg(t, 21.4, 22.2))), False
    if t < SQUEAK_T + 0.1:  # watches Crumb's offering
        return dict(x=240, y=FLOOR, mood="frozen" if t < 25.0 else "smug", look=(1, 0)), True
    if t < 29.0:  # the squeak
        return dict(x=240, y=FLOOR, mood="shocked", look=(1, 0), arm="reach", shake=5), True
    return None


def crumb_state(t):
    if t < 21.0:
        return None
    if t < 22.0:
        p = ease(seg(t, 21.0, 22.0))
        return dict(x=lerp(940, 640, p), y=FLOOR - abs(math.sin(p * math.pi * 4)) * 20, mood="worried", look=(-1, 0)), False
    if t < 22.75:
        return dict(x=640, y=FLOOR, mood="worried", look=(1, -1) if t > 22.3 else (-1, 0), arm="wave" if t > 22.3 else "down"), False
    if t < 23.6:   # CRUNCH. ow.
        return dict(x=640, y=FLOOR, mood="scared", look=(0, 0), shake=6), True
    if t < 24.6:   # steps up and sets the gift down
        p = ease(seg(t, 23.6, 24.4))
        return dict(x=lerp(640, 610, p), y=FLOOR, mood="sheepish", look=(-1, 0.5), bow=-0.35 * math.sin(math.pi * p)), True
    if t < SQUEAK_T + 0.1:   # deep bow
        b = ease(seg(t, 24.6, 25.2))
        return dict(x=610, y=FLOOR, mood="sheepish", look=(-1, 0.6), bow=-0.45 * b), True
    if t < 29.0:
        return dict(x=610, y=FLOOR, mood="scared", look=(-1, 0), shake=5), True
    return None


RUN_C, RUN_R = 640, 190


def run_pos(t, phase):
    """Screaming circles: an ellipse seen from the side; returns x, y-offset, depth."""
    a = (t - 29.0) * 2 * math.pi / 1.1 + phase
    return RUN_C + RUN_R * math.cos(a), -18 * math.sin(a), math.sin(a)


def scene(c, t):
    cx, cy, Z = camera(t)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    random.seed(int(t * 30))
    if 18.95 <= t < 19.35:   # carton crash shake
        k = 1 - seg(t, 18.95, 19.35)
        c.translate(random.uniform(-22, 22) * k, random.uniform(-22, 22) * k)
    fridge_bg(c, LIGHT)
    if t >= 33.0:
        jar_lid(c, t)

    # jello at the right (hiding place later)
    wob = 0.0
    if 31.9 <= t < 33.0:
        wob = math.sin((t - 31.9) * 18) * (1 - seg(t, 31.9, 33.0))
    jello_front = t >= 31.8

    def draw_jello():
        c.save(); c.translate(JELLO_X, FLOOR); c.scale(1.8, 1.8); c.translate(-JELLO_X, -FLOOR)
        jello(c, JELLO_X, FLOOR, wob); c.restore()
    if not jello_front:
        draw_jello()

    # ---- the Duck ----
    sx = sy = 1.0
    if 17.7 <= t < 18.2:     # trampoline squash
        p = math.sin(math.pi * seg(t, 17.7, 18.2)) * (1 - 0.3 * seg(t, 17.95, 18.2))
        sy = 1 - 0.3 * p; sx = 1 + 0.18 * p
    if SQUEAK_T <= t < SQUEAK_T + 0.35:   # the squeak (its one tiny motion follows: the crown tilts)
        p = math.sin(math.pi * seg(t, SQUEAK_T, SQUEAK_T + 0.35))
        sy = 1 - 0.1 * p; sx = 1 + 0.06 * p
    cap = 0.0
    if t >= SQUEAK_T + 0.25:
        cap = 0.38 * back_out(seg(t, SQUEAK_T + 0.25, SQUEAK_T + 0.6))
    the_duck(c, t, sx, sy, cap)

    # ---- the gift ----
    if 23.6 <= t < 24.4:     # carried
        p = ease(seg(t, 23.6, 24.4))
        gift_piece(c, lerp(560, GIFT_X, p), lerp(FLOOR - 140, FLOOR - 22, p), lerp(0.3, 0, p))
    elif t >= 24.4 and t < 33.0:
        gift_piece(c, GIFT_X, FLOOR - 22, 0.0)

    # ---- Dill ----
    st = dill_state(t)
    if st is not None:
        kw, upright = st
        x, y = kw.pop("x"), kw.pop("y")
        dill(c, x, y, crown_on=True, **kw)
        if upright and t < 21.0:
            goo(c, x, y, t, 7, h=115, n=4, top=292)
        if 2.0 <= t < 6.0 and t > 2.8:   # steam
            for k in range(3):
                q = ((t - 2.8) * 1.6 + k / 3) % 1
                ellipse(c, x - 50 + k * 50 + 20 * math.sin(q * 6), y - 360 - q * 200, 24 + 26 * q, 20 + 22 * q,
                        (1, 1, 1), stroke=False)
        if 6.0 <= t < 10.0:   # staring contest: tears, twitch, blink
            amt = ease(seg(t, 7.1, 8.2))
            tears(c, x, y, t, amt, big=1.25)
            k_big = 0.0
            if 7.7 <= t < 8.4 or 9.2 <= t < 9.5:
                k_big = 0.35 * max(0, math.sin(t * 55))          # twitch
            k_small = 0.0
            if t >= 9.5:   # lids creep... then BLINK
                creep = 0.25 * seg(t, 9.5, 9.72)
                blink = math.sin(math.pi * seg(t, 9.72, 9.95)) if t < 9.95 else 0.0
                k_small = max(creep, blink); k_big = max(k_big, creep, blink)
            dill_lids(c, x, y, k_small, k_big, big=1.25)
            if 7.7 <= t < 8.4:   # twitch marks
                c.set_source_rgb(*INK); c.set_line_width(4)
                for j in range(3):
                    a = -0.9 + j * 0.45
                    c.move_to(x + 30 + 52 * math.cos(a), y - 212 + 52 * math.sin(a))
                    c.line_to(x + 30 + 66 * math.cos(a), y - 212 + 66 * math.sin(a)); c.stroke()
        if 19.9 <= t < 21.6:   # dizzy stars
            for k in range(3):
                a = t * 5 + k * 2.1
                star(c, x + 100 * math.cos(a), y - 380 + 22 * math.sin(a), 22, t * 3)

    # ---- Crumb ----
    cs = crumb_state(t)
    if cs is not None:
        kw, notched = cs
        x, y = kw.pop("x"), kw.pop("y")
        crumb_notched(c, x, y, notched, **kw)
        if 22.3 <= t < 22.75:   # gripping the corner
            gift_piece(c, x + 92, y - 262, 0.0, 1.0)
        if 22.75 <= t < 23.6:   # holds the piece, crumbs fly
            gift_piece(c, x + 115, y - 140, 0.3)
            q = seg(t, 22.75, 23.3)
            for j in range(7):
                a = -math.pi * (0.1 + 0.8 * j / 6)
                ellipse(c, x + 100 + math.cos(a) * 140 * q, y - 260 + math.sin(a) * 110 * q + 260 * q * q,
                        7, 6, BREAD, lw=2)
            if t < 23.4:   # tiny "ow" star
                s = back_out(seg(t, 22.8, 23.0)) * (1 - seg(t, 23.2, 23.4))
                star(c, x + 110, y - 300, 30 * s, 0.3, hexc("#FFE066"))

    # ---- screaming circles, then the dive behind the jello ----
    if 29.0 <= t < 33.0:
        bodies = []
        for who, phase in (("dill", 0.0), ("crumb", math.pi)):
            if t < 31.2:
                x, dy, depth = run_pos(t, phase)
                y = FLOOR + dy
            elif t < 31.8:
                x0, dy0, _ = run_pos(31.2, phase)
                tx = JELLO_X - 60 if who == "dill" else JELLO_X + 55
                p = seg(t, 31.2, 31.8)
                x = lerp(x0, tx, p); y = FLOOR - 220 * math.sin(math.pi * p) + dy0 * (1 - p); depth = -1
            else:   # peeking over the jello, trembling
                x = JELLO_X - 60 if who == "dill" else JELLO_X + 55
                y = FLOOR - (125 if who == "dill" else 185) - 4 * math.sin(t * 40); depth = -1
            bodies.append((depth, who, x, y))
        for depth, who, x, y in sorted(bodies):
            if who == "dill":
                dill(c, x, y, "shocked", look=(-1, 0), arm="reach" if t < 31.8 else "down", crown_on=True,
                     rot=0.15 * math.sin(t * 25) if t < 31.2 else 0.0, shake=3 if t >= 31.8 else 0)
            else:
                crumb(c, x, y, "scared", look=(-1, 0), arm="wave" if t < 31.8 else "down",
                      rot=-0.15 * math.sin(t * 25) if t < 31.2 else 0.0, shake=3 if t >= 31.8 else 0)
                # (the snapped corner is too small to read at this distance; keep the shape simple)
    if jello_front:
        draw_jello()

    # ---- crickets during the dance-off silence ----
    if 15.0 <= t < 16.2:
        cricket(c, 560, FLOOR - 8, t)
    # music notes during the dance
    if 11.4 <= t < 15.0:
        for j in range(4):
            q = ((t - 11.4) * 0.8 + j / 4) % 1
            music_note(c, DILL_X - 160 + j * 110 + 30 * math.sin(q * 6 + j), FLOOR - 420 - q * 280, 1.1, 1 - q)
    if 2.0 <= t < 5.8:   # furious bubble: Dill's throne... with a duck on it, crossed out
        def icon(cc):
            cc.save(); cc.scale(0.55, 0.55); cc.translate(0, 80); duck(cc, 0, 0, turn=1.0); cc.restore()
            cc.set_source_rgb(0.9, 0.1, 0.15); cc.set_line_width(14); cc.set_line_cap(cairo.LINE_CAP_ROUND)
            cc.move_to(-55, -50); cc.line_to(55, 50); cc.move_to(55, -50); cc.line_to(-55, 50); cc.stroke()
        bubble(c, DILL_X + 10, FLOOR - 610, back_out(seg(t, 3.2, 3.5)) * (1 - seg(t, 5.4, 5.8)), icon)

    # ---- sound-effect words ----
    def word(s, x, y, size, col, t0, t1, rot=0.0):
        if t0 <= t < t1:
            k = back_out(seg(t, t0, t0 + 0.2))
            c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(k), S(k)); text(c, s, 0, 0, size, col, olw=12); c.restore()
    word("BLINK", DILL_X + 10, FLOOR - 300, 46, (1, 1, 1), 9.72, 10.0, -0.08)
    word("THUD!", DILL_X + 150, FLOOR - 160, 100, (1, 1, 1), 10.45, 11.1, 0.1)
    word("BOING!", DUCK_X + 40, FLOOR - 470, 110, hexc("#FFD43B"), 17.75, 18.6, -0.1)
    word("CRASH!", 300, FLOOR - 600, 120, (1, 1, 1), 19.0, 19.9, 0.12)
    word("CRUNCH", 560, FLOOR - 430, 72, BREAD, 22.75, 23.5, -0.1)
    word("SQUEAK.", DUCK_X + 10, FLOOR - 330, 64, hexc("#FFD43B"), SQUEAK_T, SQUEAK_T + 1.2)
    word("BOING!", JELLO_X - 60, FLOOR - 420, 90, hexc("#FF8FB3"), 31.85, 32.5, 0.1)
    for i, k in enumerate(LID_CLICKS):
        word("click", 330 + (i % 2) * 30, TOP - 420 - i * 12, 46, (1, 1, 1), k, k + 0.45, 0.15 * (1 if i % 2 else -1))
    if 19.0 <= t < 19.9:   # milk splashes out of the carton top
        q = seg(t, 19.0, 19.9)
        for j in range(6):
            a = -math.pi * (0.25 + 0.5 * j / 5)
            ellipse(c, 110 + math.cos(a) * 200 * q, FLOOR - 500 + math.sin(a) * 260 * q + 500 * q * q, 14, 18, (1, 1, 1), lw=3)
    if t >= SQUEAK_T + 0.15 and t < 29.0:   # "!!" over both
        s = back_out(seg(t, SQUEAK_T + 0.15, SQUEAK_T + 0.35))
        for x0 in (240, 610):
            c.save(); c.translate(x0, FLOOR - 470); c.scale(S(s), S(s)); text(c, "!!", 0, 0, 120, (1, 0.3, 0.3), olw=12); c.restore()
    dark_overlay(c, LIGHT)


def frame(c, t):
    if t < 2.0:
        title_card(c, t, 5, "The Usurper")
        if t > 1.7:
            iris(c, W / 2, H / 2, lerp(1200, 0, ease(seg(t, 1.7, 2.0))))
        return
    if t >= END_T:
        end_card(c, t, END_T); return
    c.save(); scene(c, t); c.restore()
    if t < 2.4:
        iris(c, W / 2, H / 2, lerp(0, 1400, ease(seg(t, 2.0, 2.4))))
    if t >= END_T - 0.4:
        iris(c, W / 2, H * 0.42, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))


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
