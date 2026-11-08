"""FRIDGE KINGDOM — Episode 14: "The Duck Is Back". 40.0s, 1080x1920 @ 30fps.

Variant B (cold open): the first frame is mid-action; a small title banner sits across the top for 2s.

Cold open on the ceiling vent: the icy eye is still glaring out of the grille when the door bursts open
(choir, blinding light) and the eye squints and vanishes. The Hand descends and sets the Duck back down on
the top shelf: squeaky clean, sparkling, with a pink-striped towel turban under its tilted bottle-cap crown.
Door closes. The Jar pickles turn and bow to it, one by one; the sprout pickle bows from inside the jar;
Grandma Gherkin bows too (still wearing Dill's crown). Record scratch: Dill's jaw drops; he steams and
raises his sword at the Duck... Grandma's spectacles glint at him and he deflates.
Peep, perched on Crumb's head, sees the Duck: a big yellow bird like itself! Its eyes turn to hearts.
It hops down and waddles over to sit beside the Duck, then copies it: perfectly still. Very still.
Crumb waves (nothing; a cricket chirps). Crumb holds up a crust bit, Peep's favourite (nothing!).
He drops it and sits down alone, crying. Dill shuffles over, looks away, and awkwardly pats his back three
times (a callback to Wilt's pat); Crumb leans on him; Dill freezes.
The Duck's one motion: it slowly tilts its head toward Crumb (squeak). Peep copies the tilt, follows its gaze,
sees Crumb crying, and its eyes turn to hearts again; it races back and leaps into a hug on Crumb's head.
Then the vent's slats glow icy blue and a crackling frost tendril creeps down the back wall straight to the
Duck. Above the Duck's cap crown, a spiky crown of ice grows out of thin air, and frost spreads over the
Duck's towel turban. Everyone gasps. Push in on the Duck under its ice crown; DUN DUN DUNNN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crown, dark_overlay, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp,
                 back_out, INK, GOLD, TOP, W, H, FPS, S)
from ep2 import end_card
from ep5 import cap_crown, cricket
from ep6 import grandma, fridge6, lid_piece, pickle_kid, PICKLE_STYLES, JAR_X
from ep7 import god_rays
from ep8 import shell_half
from ep9 import fat_peep, crumb_bitten, bread_bit, GRAN_HEAD
from ep10 import ceiling_vent, frost, hand_cuffed, VENT_X
from ep12 import vent_glow, squash_at, word, hop
from ep13 import ceiling
from animate import heart

DUR = 40.0
END_T = 38.5
DIM = 0.18
FAT = 1.5
GSC = 1.35
PS = 1.2
DUCK_Y = hexc("#FFD43B")
DUCK_D = hexc("#FCC419")
BEAK = hexc("#FF922B")
ICE = hexc("#D0EBFF")
ICE_B = hexc("#74C0FC")
TOWEL = hexc("#FFF5F7")
TOWEL_S = hexc("#F783AC")
TEAR = hexc("#74C0FC")

# ---------------- timing ----------------
T_OPEN = 0.45         # door bursts open
T_PULL = 0.95         # camera pulls back to the shelf
T_SET = 3.4           # the Duck touches down
T_CLOSE = 5.2
BOW_T = [5.6, 5.85, 6.1, 6.35]
T_SPROUT = 6.6
T_GBOW = 6.9
T_SCRATCH = 7.6       # Dill's jaw drops
T_STEAM = 8.1
T_SWORD = 8.5
T_GLINT = 9.0
T_DEFLATE = 9.4
T_NOTICE = 10.0       # Peep sees the Duck
T_LOVE = 10.5
T_HOPOFF = 11.6
T_WADDLE = 12.1
T_SIT = 13.4
T_STILL = 14.2        # copies the Duck: perfectly still
T_WAVE = 15.2
T_BREAD = 16.9
T_DROP = 18.6
T_SITDOWN = 19.3
T_SHUFFLE = 20.4
PATS = (21.6, 22.2, 22.8)
T_LEAN = 23.4
T_DTILT = 25.4        # the Duck's one motion
T_PTILT = 26.5        # Peep copies the tilt
T_GAZE = 27.3         # Peep follows the gaze to Crumb
T_LOVE2 = 27.9
T_RUN = 28.4
T_HUG = 29.2
T_WIPE = 30.0
T_GLOW = 31.0         # vent glows
T_CREEP = 31.6        # frost tendril creeps down
T_REACH = 33.6        # tendril reaches the Duck
T_ICROWN = 33.8       # ice crown grows
T_GASP = 34.7
T_FROSTCAP = 35.0     # frost over the turban
T_PUSH = 35.2
T_SHINE = 36.5
DUNS = (37.0, 37.4, 37.8)

# ---------------- layout ----------------
DUCK_X = 530
PEEP_SPOT = 705
CRX = 850
DIX = 990
GRX = 380
PK_X = {0: 45, 1: 125, 4: 205, 2: 285}     # pickle k -> x (the sprout pickle, k=3, is in the jar)


def ph(k):
    return (14 + 2 * PICKLE_STYLES[k]["ry"]) * PS


# ---------------- new props ----------------
def towel_turban(c, frosty=0.0):
    """Pink-striped towel wrapped around the Duck's head (head-local coords, head centre at 0,0)."""
    c.save()
    # wrapped band around the top of the head
    c.move_to(-58, -14); c.curve_to(-64, -64, -20, -86, 8, -84); c.curve_to(46, -82, 66, -52, 58, -12)
    c.curve_to(30, -30, -30, -30, -58, -14); c.close_path()
    c.set_source_rgb(*TOWEL); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    # stripes
    c.save()
    c.move_to(-58, -14); c.curve_to(-64, -64, -20, -86, 8, -84); c.curve_to(46, -82, 66, -52, 58, -12)
    c.curve_to(30, -30, -30, -30, -58, -14); c.close_path(); c.clip()
    c.set_source_rgb(*TOWEL_S); c.set_line_width(7)
    for k in range(4):
        c.move_to(-70, -26 - k * 17); c.curve_to(-20, -46 - k * 17, 20, -46 - k * 17, 70, -24 - k * 17); c.stroke()
    c.restore()
    # twisted knot puff on top-right
    c.save(); c.translate(36, -74); c.rotate(0.5)
    ellipse(c, 0, 0, 22, 15, TOWEL, lw=5)
    c.set_source_rgb(*TOWEL_S); c.set_line_width(4); c.move_to(-12, -4); c.curve_to(-2, 6, 6, -8, 14, 2); c.stroke()
    c.restore()
    if frosty > 0.01:
        c.save()
        c.move_to(-58, -14); c.curve_to(-64, -64, -20, -86, 8, -84); c.curve_to(46, -82, 66, -52, 58, -12)
        c.curve_to(30, -30, -30, -30, -58, -14); c.close_path()
        c.set_source_rgba(0.85, 0.95, 1.0, 0.75 * frosty); c.fill()
        for (fx, fy) in [(-34, -40), (-4, -64), (30, -46), (44, -26)]:
            c.set_source_rgba(1, 1, 1, frosty); c.set_line_width(3.5)
            for j in range(3):
                a = j * math.pi / 3
                c.move_to(fx - 9 * math.cos(a), fy - 9 * math.sin(a)); c.line_to(fx + 9 * math.cos(a), fy + 9 * math.sin(a))
            c.stroke()
        c.restore()
    c.restore()


def clean_duck(c, x, y, tilt=0.0, gaze=0.0, sparkle_t=None, frosty=0.0, s=1.0):
    """The Duck, front-facing, back from its bath: towel turban under the bottle-cap crown.
    tilt rotates the head (positive = toward the right); gaze shifts its eyes right."""
    c.save(); c.translate(x, y); c.scale(S(s), S(s))
    ellipse(c, 0, -58, 92, 58, DUCK_Y, lw=7)
    c.move_to(-80, -80); c.line_to(-120, -112); c.line_to(-84, -46); c.close_path()
    c.set_source_rgb(*DUCK_Y); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    ellipse(c, -6, -60, 46, 26, DUCK_D, stroke=False)
    ellipse(c, -40, -82, 22, 9, (1, 1, 1), stroke=False)            # squeaky-clean shine on the body
    # head
    c.save(); c.translate(4, -142); c.rotate(tilt)
    ellipse(c, 0, 0, 54, 52, DUCK_Y, lw=7)
    ellipse(c, -24, -26, 12, 7, (1, 1, 1), stroke=False)             # head shine
    ellipse(c, 0, 22, 36, 14, BEAK, lw=5)
    for ex in (-19, 19):
        gx = ex + 6 * gaze
        ellipse(c, gx, -8, 11, 13, INK, stroke=False)
        ellipse(c, gx + 3, -12, 3, 3, (1, 1, 1), stroke=False)
    towel_turban(c, frosty)
    cap_crown(c, 4, -80, 0.32, 0.95)
    if frosty > 0.01:   # rime on the cap crown
        c.save(); c.translate(4, -80); c.rotate(0.32); c.scale(0.95, 0.95)
        ellipse(c, 0, -30, 44, 9, (0.9, 0.97, 1.0), stroke=False)
        c.set_source_rgba(0.9, 0.97, 1, 0.6 * frosty); c.rectangle(-48, -28, 96, 26); c.fill()
        c.restore()
    c.restore()
    c.restore()
    if sparkle_t is not None:      # sparkly-clean twinkles
        for j, (dx, dy) in enumerate([(-110, -230), (100, -260), (130, -120), (-140, -60), (20, -320)]):
            ph_ = (sparkle_t * 1.3 + j * 0.37) % 1
            star(c, x + dx * s, y + dy * s, 18 * s * math.sin(math.pi * ph_), sparkle_t * 2 + j, (1, 1, 1))


def ice_crown(c, x, y, k, glint=0.0):
    """A spiky crown made of ice, floating above the Duck. k grows it 0..1; (x, y) = its base centre."""
    if k <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(S(k), S(k))
    g = cairo.RadialGradient(0, -40, 5, 0, -40, 160)
    g.add_color_stop_rgba(0, 0.6, 0.88, 1, 0.55); g.add_color_stop_rgba(1, 0.6, 0.88, 1, 0)
    c.rectangle(-170, -200, 340, 260); c.set_source(g); c.fill()
    pts = [(-70, 0), (-80, -70), (-50, -38), (-30, -108), (-10, -46), (0, -128), (10, -46), (30, -108), (50, -38), (80, -70), (70, 0)]
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path()
    c.set_source_rgba(*hexc("#E7F5FF"), 0.92); c.fill_preserve()
    c.set_source_rgb(*hexc("#1971C2")); c.set_line_width(6); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(4)          # facets
    for (a, b) in [((-30, -96), (-26, -20)), ((0, -114), (0, -24)), ((30, -96), (26, -20))]:
        c.move_to(*a); c.line_to(*b); c.stroke()
    rrect(c, -72, -16, 144, 18, 8); c.set_source_rgb(*ICE_B); c.fill_preserve()
    c.set_source_rgb(*hexc("#1971C2")); c.set_line_width(4); c.stroke()
    for gx in (-40, 0, 40):    # icicle drips under the band
        c.move_to(gx - 8, 2); c.line_to(gx, 20); c.line_to(gx + 8, 2); c.close_path()
        c.set_source_rgba(*hexc("#E7F5FF"), 0.95); c.fill_preserve(); c.set_source_rgb(*hexc("#1971C2")); c.set_line_width(3); c.stroke()
    if glint > 0:
        star(c, 0, -128, 34 * glint, glint * 3, (1, 1, 1))
    c.restore()


TEND = [(VENT_X - 20, 130), (VENT_X - 40, 200), (VENT_X - 10, 260), (VENT_X - 50, 320), (DUCK_X + 30, 370), (DUCK_X + 10, 410)]


def frost_tendril(c, p):
    """A crackling frost line creeping down the back wall from the vent to the Duck. p 0..1."""
    if p <= 0.01:
        return
    n = len(TEND) - 1
    L = p * n
    pts = [TEND[0]]
    for i in range(n):
        if L <= i:
            break
        q = min(1, L - i)
        a, b = TEND[i], TEND[i + 1]
        pts.append((lerp(a[0], b[0], q), lerp(a[1], b[1], q)))
    c.save(); c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    for lw, col in [(26, (*ICE_B, 0.7)), (12, (1, 1, 1, 0.95))]:
        c.move_to(*pts[0])
        for pp in pts[1:]:
            c.line_to(*pp)
        c.set_source_rgba(*col); c.set_line_width(lw); c.stroke()
    # little branches
    for i, (bx, by) in enumerate(pts[1:]):
        for s in (-1, 1):
            c.move_to(bx, by); c.line_to(bx + s * 34, by - 22 - 6 * (i % 2))
        c.set_source_rgba(1, 1, 1, 0.9); c.set_line_width(6); c.stroke()
    tx, ty = pts[-1]
    if p < 1:
        star(c, tx, ty, 20, p * 20, (1, 1, 1))
    c.restore()


def steam(c, x, y, t, t0, t1):
    if not (t0 <= t < t1):
        return
    for j in range(4):
        q = ((t - t0) * 1.8 + j * 0.25) % 1
        ellipse(c, x + (j % 2 * 2 - 1) * (40 + 30 * q), y - 120 * q, 18 + 20 * q, 14 + 14 * q, (1, 1, 1), stroke=False)


def crumb_tears(c, x, top, t, amt):
    """Crumb's eyes at (+-26, -160) from his feet, scaled by his squash (top = feet y)."""
    if amt <= 0.01:
        return
    for ex in (-26, 26):
        for j in range(2):
            q = (t * 1.4 + j * 0.5 + ex * 0.01) % 1
            ellipse(c, x + ex + (j * 2 - 1) * 8, top + q * 110 * amt, 7 * amt, 11 * amt, TEAR, lw=3)


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
    text(c, "Ep. 14:  The Duck Is Back", W / 2, 182, 46, (1, 1, 1), olw=8)
    c.restore()


# ---------------- states ----------------
def light_at(t):
    if t < T_OPEN:
        return DIM
    if t < T_CLOSE:
        return lerp(DIM, 1.0, ease(seg(t, T_OPEN, T_OPEN + 0.25)))
    return lerp(1.0, DIM, ease(seg(t, T_CLOSE, T_CLOSE + 0.35)))


def duck_pos(t):
    """(x, feet_y) of the Duck."""
    if t >= T_SET:
        return DUCK_X, TOP
    p = ease_out(seg(t, 1.1, T_SET))
    return DUCK_X, lerp(-500, TOP, p)


def hand_state(t):
    """(x, tip_y, grip) or None."""
    if t < 1.1 or t >= T_CLOSE:
        return None
    dx, dy = duck_pos(t)
    if t < T_SET + 0.1:
        return dx + 10, dy - 256, 0.6
    if t < T_SET + 0.45:
        return dx + 10, TOP - 256 - 30 * ease(seg(t, T_SET + 0.1, T_SET + 0.45)), lerp(0.6, 0.0, ease(seg(t, T_SET + 0.1, T_SET + 0.45)))
    return dx + 10, lerp(TOP - 286, -900, ease(seg(t, T_SET + 0.45, T_CLOSE))), 0.0


def duck_tilt(t):
    return 0.36 * ease(seg(t, T_DTILT, T_DTILT + 1.0))


def duck_gaze(t):
    return ease(seg(t, T_DTILT + 0.3, T_DTILT + 1.0))


def pickle_kw(k, t):
    """(x, kw) for the four pickles on the shelf."""
    x = PK_X[k]
    i = [0, 1, 4, 2].index(k)
    look, mood, bow = (1, -1), "calm", 0.0
    if t < T_PULL + 0.4:
        look, mood = (0.3, -1), "shock"
    elif t < T_SET:
        look, mood = (1, -1), "shock"
    if t >= BOW_T[i]:
        bow = 0.55 * ease(seg(t, BOW_T[i], BOW_T[i] + 0.35))
        look = (1, 0.6)
        if T_CREEP + 0.5 <= t:
            bow = lerp(0.55, 0.0, ease(seg(t, T_CREEP + 0.5, T_CREEP + 0.9)))
            look, mood = (1, -1), "calm"
        if t >= T_GASP:
            mood = "shock"
    if T_STILL + 0.6 <= t < T_RUN and t >= BOW_T[i] + 1:
        mood = "closed"
    return x, dict(look=look, mood=mood, bow=bow)


def gran_kw(t):
    look, mood, bow, cane = (1, -0.6), "stern", 0.0, "down"
    if t < T_SET:
        look, mood = (0.5, -1), "closed" if t < T_PULL + 0.5 else "stern"
    if t >= T_GBOW:
        bow = 0.5 * ease(seg(t, T_GBOW, T_GBOW + 0.4))
        mood = "closed"
    if T_GLINT - 0.3 <= t < T_DEFLATE + 0.6:      # side-eyes Dill
        bow = lerp(0.5, 0.15, ease(seg(t, T_GLINT - 0.3, T_GLINT)))
        look, mood = (1, -0.4), "stern"
    elif t >= T_DEFLATE + 0.6:
        bow = 0.5
        mood = "closed"
    if t >= T_CREEP + 0.5:
        bow = lerp(0.5, 0.0, ease(seg(t, T_CREEP + 0.5, T_CREEP + 0.9)))
        look, mood = (0.6, -1), "stern"
    return dict(look=look, mood=mood, bow=bow, cane=cane)


def dill_state(t):
    """(x, kw)."""
    if t < T_SET:
        return DIX, dict(mood="shocked", look=(-0.6, -1), arm="reach" if t < T_PULL + 0.6 else "down")
    if t < T_SCRATCH:
        return DIX, dict(mood="smug", look=(-1, 0), arm="down")
    if t < T_STEAM:
        return DIX, dict(mood="shocked", look=(-1, 0.3), arm="down", sq=1.06)
    if t < T_SWORD:
        return DIX, dict(mood="angry", look=(-1, 0.3), arm="down", shake=3)
    if t < T_DEFLATE:
        return DIX - 30 * ease(seg(t, T_SWORD, T_SWORD + 0.3)), dict(mood="angry", look=(-1, 0.2), arm="point_l", shake=2)
    if t < T_SHUFFLE:
        x = DIX - 30 * (1 - ease(seg(t, T_DEFLATE, T_DEFLATE + 0.4)))
        mood = "sad" if t < T_STILL else "frozen"
        look = (-1, 0.4)
        if T_STILL <= t:
            look = (-1, 0.2)
        return x, dict(mood=mood, look=look, arm="down", sq=lerp(0.92, 1, ease(seg(t, T_DEFLATE + 0.6, T_DEFLATE + 1.2))))
    if t < PATS[0] - 0.3:      # shuffles closer, looking away
        p = ease(seg(t, T_SHUFFLE, PATS[0] - 0.5))
        return lerp(DIX, CRX + 125, p), dict(mood="frozen", look=(1, -0.4), arm="down", sq=1 - 0.03 * abs(math.sin(p * 9)))
    if t < T_HUG:
        rot = 0.0
        for pt in PATS:
            if pt - 0.15 <= t < pt + 0.25:
                rot = -0.09 * math.sin(math.pi * seg(t, pt - 0.15, pt + 0.25))
        mood = "frozen"
        look = (1, -0.4)
        if t >= T_LEAN:
            mood, look = "shocked", (-0.6, 0.4)
            rot = 0.04
        return CRX + 125, dict(mood=mood, look=look, arm="point_l", rot=rot)
    if t < T_GLOW:
        mood = "smug" if t < T_WIPE else "sad"
        return CRX + 125 + 30 * ease(seg(t, T_HUG, T_HUG + 0.4)), dict(mood=mood, look=(1, -0.2), arm="down")
    look = (-0.6, -1)
    mood = "shocked" if t >= T_CREEP + 0.4 else "sad"
    return CRX + 155, dict(mood=mood, look=look, arm="down", shake=2 if t >= T_GASP else 0)


def crumb_sq(t):
    if t < T_SITDOWN:
        return 1.0
    if t < T_HUG:
        return lerp(1.0, 0.84, ease(seg(t, T_SITDOWN, T_SITDOWN + 0.35)))
    return lerp(0.84, 1.0, back_out(seg(t, T_HUG, T_HUG + 0.4)))


def crumb_top(t):
    return 300 * crumb_sq(t) - 6


def crumb_state(t):
    """(rot, kw, tears)."""
    if t < T_SET:
        return 0, dict(mood="scared", look=(-0.6, -1)), 0
    if t < T_NOTICE:
        return 0, dict(mood="worried", look=(-1, 0)), 0
    if t < T_HOPOFF:
        return 0, dict(mood="worried", look=(-0.6, -1)), 0
    if t < T_STILL:
        return 0, dict(mood="worried", look=(-1, 0)), 0
    if t < T_BREAD:
        wav = T_WAVE <= t < T_BREAD - 0.2
        return 0, dict(mood="sheepish" if wav else "worried", look=(-1, 0), arm="wave_l" if wav else "down"), 0
    if t < T_DROP:
        return 0, dict(mood="sheepish", look=(-1, 0), arm="wave_l"), 0
    if t < T_HUG:
        rot = 0.0
        if t >= T_LEAN:
            rot = 0.14 * ease(seg(t, T_LEAN, T_LEAN + 0.4))
        return rot, dict(mood="worried", look=(-1, 0.6) if t < T_LEAN else (1, 0.5)), min(1, seg(t, T_SITDOWN, T_SITDOWN + 0.6))
    rot = 0.14 * (1 - ease(seg(t, T_HUG, T_HUG + 0.3)))
    if t < T_GLOW:
        return rot, dict(mood="sheepish", look=(-0.3, -1)), 0.7 * (1 - seg(t, T_HUG + 0.8, T_GLOW))
    return 0, dict(mood="scared", look=(-1, -0.8), shake=1.5 if t >= T_GASP else 0), 0


def perch(t):
    return CRX, TOP - crumb_top(t) + 8


def peep_state(t):
    """(x, y, kw)."""
    if t < T_HOPOFF:
        x, y = perch(t)
        if t < T_SET:
            return x, y, dict(mood="shock", face=0, look=(-0.5, -1), wings="flap", flap_t=t)
        if t < T_NOTICE:
            return x, y, dict(mood="happy", face=-0.3, look=(-1, 0))
        if t < T_LOVE:
            return x, y - 30 * math.sin(math.pi * seg(t, T_NOTICE, T_NOTICE + 0.3)), dict(mood="shock", face=-0.5, look=(-1, 0))
        return x, y, dict(mood="love", face=-0.5, flap_t=t)
    if t < T_WADDLE:
        p = seg(t, T_HOPOFF, T_WADDLE)
        x, y = hop(perch(T_HOPOFF), (CRX - 120, TOP), p, 120)
        return x, y, dict(mood="love", face=-0.5, wings="flap", flap_t=t * 1.5)
    if t < T_SIT:
        p = seg(t, T_WADDLE, T_SIT)
        x = lerp(CRX - 120, PEEP_SPOT, ease(p))
        return x, TOP - abs(math.sin(p * math.pi * 5)) * 14, dict(mood="love", face=-0.6, rot=0.08 * math.sin(p * math.pi * 5), flap_t=t)
    if t < T_STILL:
        return PEEP_SPOT, TOP, dict(mood="love", face=-0.6, flap_t=t, sq=lerp(0.9, 1, ease(seg(t, T_SIT, T_SIT + 0.3))))
    if t < T_PTILT:
        # copies the Duck: front-facing, dead still (not even its trademark wobble)
        return PEEP_SPOT, TOP, dict(mood="happy", face=0, look=(0, 0), sq=lerp(1.05, 1.0, ease(seg(t, T_STILL, T_STILL + 0.2))))
    if t < T_GAZE:
        return PEEP_SPOT, TOP, dict(mood="happy", face=0, look=(0.4, 0), rot=0.28 * ease(seg(t, T_PTILT, T_PTILT + 0.4)))
    if t < T_RUN:
        rot = 0.28 * (1 - ease(seg(t, T_GAZE, T_GAZE + 0.3)))
        mood = "shock" if t < T_LOVE2 else "love"
        return PEEP_SPOT, TOP, dict(mood=mood, face=0.6, look=(1, 0), rot=rot, flap_t=t)
    if t < T_HUG:
        p = seg(t, T_RUN, T_HUG)
        x, y = hop((PEEP_SPOT, TOP), perch(T_HUG), p, 180)
        return x, y, dict(mood="love", face=0.5, wings="flap", flap_t=t * 1.5, rot=-0.4 * math.sin(math.pi * p))
    x, y = perch(t)
    if t < T_GLOW:
        return x, y, dict(mood="love", face=0, wings="hug", flap_t=t, sq=lerp(0.8, 1, back_out(seg(t, T_HUG, T_HUG + 0.3))))
    mood = "shock" if t >= T_CREEP + 0.3 else "happy"
    return x, y, dict(mood=mood, face=-0.4, look=(-1, -1), wings="hug", shake=2 if t >= T_GASP else 0)


def bread_state(t):
    """(x, y) of the crust bit Crumb offers, or None."""
    if t < T_BREAD or t >= T_HUG:
        return None
    sq = crumb_sq(t)
    if t < T_DROP:
        wig = 10 * math.sin((t - T_BREAD) * 9)
        return CRX - 102 + wig, TOP - 300
    p = seg(t, T_DROP, T_DROP + 0.4)
    return CRX - 102 - 40 * p, lerp(TOP - 300, TOP - 8, p * p)


# ---------------- camera ----------------
KEYS = [(0.0, VENT_X, 95, 3.2), (T_OPEN, VENT_X, 95, 3.2), (T_PULL, VENT_X, 95, 3.0), (T_PULL + 0.6, 560, 380, 1.25),
        (T_SET, 560, 470, 1.3), (BOW_T[0], 300, 520, 1.6), (T_GBOW + 0.4, 330, 520, 1.6),
        (T_SCRATCH, 900, 500, 1.75), (T_DEFLATE + 0.6, 860, 500, 1.65),
        (T_NOTICE - 0.3, 860, 440, 1.7), (T_LOVE + 0.6, 890, 380, 2.0), (T_HOPOFF, 880, 420, 1.7),
        (T_SIT, 680, 500, 1.6), (T_STILL, 680, 500, 1.6), (T_STILL + 0.8, 660, 520, 1.85), (T_WAVE, 740, 510, 1.6),
        (T_DROP, 740, 510, 1.6), (T_SITDOWN + 0.5, 940, 560, 1.9), (T_LEAN + 0.8, 950, 560, 2.0),
        (T_DTILT - 0.3, 640, 540, 1.9), (T_GAZE, 660, 540, 1.75), (T_LOVE2 + 0.2, 760, 520, 1.5), (T_HUG + 0.3, 860, 480, 1.6),
        (T_WIPE + 0.6, 880, 480, 1.6), (T_GLOW + 0.2, 570, 400, 1.35), (T_REACH, 570, 420, 1.35),
        (T_GASP + 0.3, 600, 440, 1.4), (T_PUSH, 580, 440, 1.4), (DUNS[0], DUCK_X, 520, 2.5), (END_T, DUCK_X, 530, 2.7)]


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
    if z < 2.6:
        cx = min(max(cx, hw), W - hw)
    for t0, s in [(T_SET, 6), (T_SCRATCH, 8), (T_CLOSE, 5), (T_GASP, 6)]:
        if t0 <= t < t0 + 0.25:
            q = s * (1 - seg(t, t0, t0 + 0.25)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    for d in DUNS:
        if d <= t < d + 0.12:
            z += 0.12 * (1 - seg(t, d, d + 0.12))
    return cx, cy, z


# ---------------- scene ----------------
def draw_gran(c, t):
    kw = gran_kw(t)
    c.save(); c.translate(GRX, TOP); c.scale(GSC, GSC); c.translate(-GRX, -TOP)
    grandma(c, GRX, TOP, **kw)
    c.restore()
    bowk = kw.get("bow", 0)
    # Dill's crown rides on her bun as she bows (rotate the bun point about her hip)
    hx, hy = GRX, TOP - 10 * GSC
    bx, by = GRAN_HEAD[0], GRAN_HEAD[1] + 10 * GSC
    ca, sa = math.cos(bowk), math.sin(bowk)
    cx, cy = hx + bx * ca - by * sa, hy + bx * sa + by * ca
    crown(c, cx, cy, 0.72, -0.2 + bowk)
    if T_GLINT <= t < T_GLINT + 0.5:     # spectacle glint
        star(c, cx + 10, cy + 55, 26 * math.sin(math.pi * seg(t, T_GLINT, T_GLINT + 0.5)), t * 4, (1, 1, 1))


def scene(c, t):
    L = light_at(t)
    fridge6(c, L, 1, lid=False)
    frost(c, t, 1.0)
    ceiling(c, L)
    ceiling_vent(c, L)
    glow = 0.0
    if t >= T_GLOW:
        glow = min(1, seg(t, T_GLOW, T_GLOW + 0.5)) * (0.75 + 0.25 * math.sin(t * 6))
    vent_glow(c, glow)
    god_rays(c, L)
    frost_tendril(c, seg(t, T_CREEP, T_REACH))
    lid_piece(c, 700, TOP - 25, 0.0)
    shell_half(c, 940, TOP - 70, 0.0, top=False)
    ellipse(c, 640, TOP + 4, 60, 9, (0.75, 0.9, 1.0), lw=3)     # meltwater puddle

    # sprout pickle in the jar
    if t >= T_SPROUT - 0.3:
        q = back_out(seg(t, T_SPROUT - 0.3, T_SPROUT))
        bowk = 0.5 * ease(seg(t, T_SPROUT, T_SPROUT + 0.35)) if t < T_CREEP + 0.5 else 0.0
        x, y = JAR_X, TOP - 170 - 120 * q
        c.save(); c.rectangle(JAR_X - 120, -400, 240, TOP - 330 + 400 + 6); c.clip()
        c.translate(x, y); c.scale(PS, PS); c.translate(-x, -y)
        pickle_kid(c, x, y, 3, look=(1, 0.5 if bowk > 0.2 else -1), mood="shock" if t >= T_GASP else "calm", bow=bowk)
        c.restore()

    for k in (0, 1, 4, 2):
        x, kw = pickle_kw(k, t)
        c.save(); c.translate(x, TOP); c.scale(PS, PS); c.translate(-x, -TOP)
        pickle_kid(c, x, TOP, k, **kw)
        c.restore()
    draw_gran(c, t)

    # the Duck (and the Hand carrying it)
    dx, dy = duck_pos(t)
    if t >= 1.1:
        land = 1.0
        if T_SET <= t < T_SET + 0.25:
            land = lerp(0.9, 1.0, back_out(seg(t, T_SET, T_SET + 0.25)))
        c.save(); c.translate(dx, dy); c.scale(1 / land ** 0.5, land); c.translate(-dx, -dy)
        clean_duck(c, dx, dy, tilt=duck_tilt(t), gaze=duck_gaze(t), sparkle_t=t if t < T_GLOW else None,
                   frosty=ease(seg(t, T_FROSTCAP, T_FROSTCAP + 0.8)))
        c.restore()
    hs = hand_state(t)
    if hs:
        hand_cuffed(c, hs[0], hs[1], hs[2])

    dxx, dkw = dill_state(t)
    behind = T_STILL <= t < T_HUG      # arm reaches behind Crumb
    if behind:
        dill(c, dxx, TOP, crown_on=False, **dkw)
    # Crumb
    rot, ckw, tr = crumb_state(t)
    sq = crumb_sq(t)
    c.save(); squash_at(c, CRX, TOP, sq)
    crumb_bitten(c, CRX, TOP, 1.0, rot=rot, **ckw)
    c.restore()
    crumb_tears(c, CRX + 20 * rot, TOP - 160 * sq, t, tr)
    if not behind:
        dill(c, dxx, TOP, crown_on=False, **dkw)
    b = bread_state(t)
    if b:
        bread_bit(c, b[0], b[1], 2.6)
    # Peep
    px, py, pkw = peep_state(t)
    fat_peep(c, px, py, FAT, **pkw)

    # ---------------- effects ----------------
    if T_OPEN <= t < T_SET:
        word(c, t, "!", 280, TOP - 330, 90, (1, 0.9, 0.4), T_PULL + 0.4, T_SET)
        word(c, t, "!", 990, TOP - 400, 90, (1, 0.9, 0.4), T_PULL + 0.5, T_SET)
    word(c, t, "plink!", DUCK_X - 150, TOP - 300, 52, (1, 1, 1), T_SET, T_SET + 0.7, -0.1)
    if T_SET <= t < T_SET + 0.6:
        q = seg(t, T_SET, T_SET + 0.6)
        for j in range(8):
            a = math.pi * (1 + j / 7)
            star(c, DUCK_X + math.cos(a) * 200 * q, TOP - 10 + math.sin(a) * 90 * q, 22 * (1 - q), t * 5, (1, 1, 1))
    for i, k in enumerate((0, 1, 4, 2)):
        if BOW_T[i] <= t < BOW_T[i] + 0.45:
            word(c, t, "fwip", PK_X[k] + 10, TOP - 260 - 30 * (i % 2), 34, (1, 1, 1), BOW_T[i], BOW_T[i] + 0.45, -0.1)
    # Dill
    word(c, t, "?!", DIX + 10, TOP - 360, 90, (1, 0.35, 0.35), T_SCRATCH, T_STEAM + 0.2, 0.1)
    steam(c, DIX, TOP - 340, t, T_STEAM, T_DEFLATE)
    word(c, t, "...", DIX - 10, TOP - 380, 70, (1, 1, 1), T_DEFLATE + 0.2, T_NOTICE - 0.2)
    # Peep falls for the Duck
    word(c, t, "!", CRX + 60, perch(t)[1] - 300, 90, (1, 0.9, 0.4), T_NOTICE, T_LOVE)
    if T_LOVE <= t < T_SIT + 0.6:
        x0, y0 = peep_state(t)[:2]
        for j in range(5):
            q = ((t - T_LOVE) * 0.9 + j * 0.2) % 1
            heart(c, x0 - 60 + 30 * j + 20 * math.sin(t * 3 + j), y0 - 280 - 160 * q, 1.4, 1 - q)
    # still... very still
    if T_STILL + 0.5 <= t < T_DTILT:
        cricket(c, 655, TOP + 30, t)
        word(c, t, "chirp", 655, TOP + 110, 40, (1, 1, 1), T_STILL + 0.6, T_STILL + 1.4, 0.1)
        word(c, t, "chirp", 655, TOP + 110, 40, (1, 1, 1), T_WAVE + 1.0, T_WAVE + 1.6, 0.1)
        word(c, t, "chirp", 655, TOP + 110, 40, (1, 1, 1), T_DROP - 0.4, T_DROP + 0.3, 0.1)
    word(c, t, "?", CRX - 20, TOP - 380, 80, (1, 0.9, 0.4), T_WAVE + 0.6, T_BREAD)
    word(c, t, "??", CRX - 20, TOP - 380, 80, (1, 0.9, 0.4), T_BREAD + 0.8, T_DROP)
    word(c, t, "plop", CRX - 200, TOP - 60, 40, (1, 1, 1), T_DROP + 0.4, T_DROP + 1.0, 0.1)
    word(c, t, "sniff", CRX - 120, TOP - 330, 44, (1, 1, 1), T_SITDOWN + 0.6, T_SITDOWN + 1.4, -0.1)
    for i, pt in enumerate(PATS):
        word(c, t, "pat", CRX + 20 + 50 * i, TOP - 330 - 30 * i, 46, (1, 1, 1), pt, pt + 0.5, -0.08 + 0.08 * i)
    word(c, t, "...", CRX + 150, TOP - 400, 70, (1, 1, 1), T_LEAN + 0.5, T_DTILT - 0.2)
    if T_LEAN + 0.2 <= t < T_DTILT:      # Dill sweats
        q = (t * 1.5) % 1
        ellipse(c, CRX + 125 + 80, TOP - 280 + 50 * q, 9, 13, TEAR, lw=3)
    # the Duck's motion
    word(c, t, "squeak", DUCK_X - 210, TOP - 330, 44, (1, 1, 1), T_DTILT + 0.2, T_DTILT + 1.0, -0.1)
    word(c, t, "!", PEEP_SPOT + 40, TOP - 330, 90, (1, 0.9, 0.4), T_GAZE + 0.1, T_LOVE2 + 0.3)
    word(c, t, "peep!", PEEP_SPOT + 120, TOP - 380, 54, (1, 1, 1), T_LOVE2 + 0.2, T_RUN + 0.4, 0.1)
    if T_HUG <= t < T_GLOW:
        for j in range(7):
            q = ((t - T_HUG) * 0.8 + j / 7) % 1
            heart(c, CRX - 140 + 45 * j + 15 * math.sin(t * 2 + j), TOP - 300 - 260 * q, 1.5, (1 - q) * min(1, (T_GLOW - t) * 3))
    word(c, t, "awww", 600, TOP - 400, 50, (1, 1, 1), T_HUG + 0.3, T_GLOW - 0.2, -0.08)
    if T_WIPE <= t < T_GLOW:      # Dill secretly wipes a tear
        ellipse(c, CRX + 155 + 30, TOP - 220, 9, 13, TEAR, lw=3)
    # cliffhanger
    word(c, t, "crrrk", VENT_X + 140, 230, 44, ICE, T_CREEP + 0.1, T_CREEP + 0.9, 0.1)
    word(c, t, "crrrk", VENT_X - 260, 330, 44, ICE, T_CREEP + 1.0, T_CREEP + 1.8, -0.1)
    ice_crown(c, DUCK_X + 18, TOP - 300, back_out(seg(t, T_ICROWN, T_ICROWN + 0.6)),
              glint=math.sin(math.pi * seg(t, T_SHINE, T_SHINE + 0.5)) if T_SHINE <= t < T_SHINE + 0.5 else 0)
    word(c, t, "GASP!", 240, TOP - 360, 64, (1, 1, 1), T_GASP, T_GASP + 0.9, -0.08)
    dark_overlay(c, L)


def frame(c, t):
    if t >= END_T:
        end_card(c, t, END_T); return
    random.seed(int(t * 30))
    cx, cy, Z = camera(t)
    c.save()
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    scene(c, t)
    if t < T_OPEN + 0.5:
        vent_eye14(c, t)
    c.restore()
    # blinding flash as the door opens
    if T_OPEN <= t < T_OPEN + 0.5:
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.85 * (1 - seg(t, T_OPEN, T_OPEN + 0.5))); c.fill()
    if t >= T_GASP:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.3, 0.6, 1.0, 0.12 * ease(seg(t, T_GASP, T_GASP + 0.5))); c.fill()
    if t >= END_T - 0.4:
        cx, cy, Z = camera(t)
        iris(c, W / 2 + (DUCK_X - cx) * Z, H / 2 + (TOP - 200 - cy) * Z, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))
    banner(c, t)


def vent_eye14(c, t):
    """The icy eye from Ep 13, still glaring, then squinting shut and vanishing when the light floods in."""
    op = 1.0 - ease(seg(t, T_OPEN, T_OPEN + 0.4))
    if op <= 0.01:
        return
    ex, ey = VENT_X, 78
    g = cairo.RadialGradient(ex, ey, 10, ex, ey, 300)
    g.add_color_stop_rgba(0, 0.55, 0.85, 1, 0.5 * op); g.add_color_stop_rgba(1, 0.55, 0.85, 1, 0)
    c.rectangle(ex - 320, ey - 300, 640, 600); c.set_source(g); c.fill()
    rrect(c, VENT_X - 150, 32, 300, 92, 10); c.set_source_rgba(0.02, 0.04, 0.09, op); c.fill()
    h = 52 * op
    look = 18 * math.sin(t * 7) if t < T_OPEN else 0
    if h > 0.5:
        c.save(); rrect(c, VENT_X - 150, 32, 300, 92, 10); c.clip()
        c.move_to(ex - 135, ey); c.curve_to(ex - 60, ey - h * 1.35, ex + 60, ey - h * 1.35, ex + 135, ey)
        c.curve_to(ex + 60, ey + h * 1.35, ex - 60, ey + h * 1.35, ex - 135, ey); c.close_path()
        c.set_source_rgb(*hexc("#E7F5FF")); c.fill_preserve()
        c.save(); c.clip()
        ellipse(c, ex + look, ey + 10, 48, 48, hexc("#4DABF7"), stroke=False)
        ellipse(c, ex + look, ey + 10, 33, 33, hexc("#A5E8FF"), stroke=False)
        ellipse(c, ex + look, ey + 10, 9, 38, hexc("#0B1B33"), stroke=False)
        ellipse(c, ex + look - 16, ey - 6, 9, 9, (1, 1, 1), stroke=False)
        c.restore(); c.restore()
    for k in range(4):
        c.rectangle(VENT_X - 150, 32 + 18 + k * 20, 300, 5); c.set_source_rgb(*hexc("#5C6670")); c.fill()
    rrect(c, VENT_X - 170, 20, 340, 110, 18); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()


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
