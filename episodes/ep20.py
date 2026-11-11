"""FRIDGE KINGDOM — Episode 20: "The Ice King's Shadow". 40.0s, 1080x1920 @ 30fps.

Variant B (cold open): the first frame is mid-action; a small title banner sits across the top for the first 2s.

Cold open in the great frozen hall: the Ice King's crowned shadow looms behind the frosted castle wall, eyes glowing.
It swells, then ROARS a frosty gale that skids the team backwards. Everyone runs, except Dill, who screeches to a halt,
dashes back for the ice block with the frozen Duck inside, and drags it along (HNNNG).
Chase through the hall: an icicle chandelier crashes (everyone hops the shards), the shadow's icy claw lunges for the
block and Dill YOINKs it away, a second chandelier CRASHes behind them.
The floor CRACKs open ahead of Crumb. He skids, slips, slides on his back over the edge and dangles by one corner (hand).
Chip and Dill reach down: too short; Chip drips on Crumb's face. His grip slips: AAAAA, he falls.
Peep leaps off Dill's head and dives after him, flapping with everything it has, catches Crumb's hand, sinks... then
powers up (golden glow) and flies for real, lifting Crumb all the way out. YAAAY: hugs, hearts, Dill salutes Peep.
Glowing eyes open deep in the crack: run! At the freezer door, light floods in (choir): the Hand reaches in for the
ice tray. Dill whistles: everyone piles onto the ice block and they bobsled toward the light, under the Hand's arm,
the shadow's claw swiping just behind; they launch off the edge into the kitchen (WHEEE).
Outside: the sled sails out of the freezer, spins, and drops toward the open fridge below (slide whistle).
Inside the fridge, the Duck sits on Dill's butter throne. Its one motion: it slowly turns its head up toward them.
They hang in the air above the jello: DUN DUN DUNNN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from animate import heart
from ep1 import (CRUST as CRUST_C, crown, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp,
                 back_out, INK, GOLD, FLOOR, W, H, FPS, S)
from ep2 import end_card, jello
from ep6 import fridge6
from ep7 import the_duck, god_rays, confetti, sq_rings
from ep9 import fat_peep
from ep10 import frost, hand_cuffed
from ep12 import word, hop
from ep14 import clean_duck
from ep16 import keyed, glazed, butter_rink, DISH
from ep18 import draw_dill, draw_crumb, draw_chip, rot_at, kitchen_bg, door, blizzard_inside, FX0, FX1, FTOP, FZB, MTOP, MBOT, KFLOOR
from ep19 import hall_bg, icicle, mound, flakes, streaks, shards, wink_star

DUR = 40.0
END_T = 38.5
FAT = 1.5
FL = 1450
ICE = hexc("#D0EBFF")
ICE_B = hexc("#74C0FC")
ICE_D = hexc("#1971C2")
SNOW = hexc("#F8FCFF")
RED = (1, 0.35, 0.35)
SHADOW = (0.04, 0.09, 0.22)
BS = 0.85                       # ice block scale
BWS, BHS = 380 * BS, 420 * BS

# ---------------- timing ----------------
# A: the roar (hall)
T_INHALE = 0.7
T_ROAR = 1.9
T_ROAR_END = 3.6
T_FLEE = 3.85
T_HALT = 4.3
T_BACK = 4.5
T_GRAB = 5.0
T_DRAG = 5.3
T_B = 6.0
# B: the chase
RUN_V = 560
T_ICE1 = 7.0                    # chandelier icicle falls...
T_ICE1_LAND = 7.3
T_CLAW = 8.4
T_YOINK = 8.95
T_CLAW_SHUT = 9.1
T_ICE2 = 10.0
T_ICE2_LAND = 10.3
T_LOOKB = 11.0
T_C = 12.0
# C: the crack
T_CRACK = 12.35
T_SKID = 12.55
T_SLIP = 12.95
T_OVER = 13.45
T_CATCH = 13.7
T_CHIP_IN = 13.25
T_DILL_IN = 13.6
T_TEETER = 13.95
T_YANK = 14.6
T_REACH = 15.0
T_DRIP = 15.55
T_REACH2 = 15.9
T_SLIPGRIP = 16.6
T_FALL = 17.2
T_PJUMP = 17.45
# D: the rescue (same set)
T_GRABP = 18.4
T_POWER = 19.7
T_RISE = 20.1
T_TOP = 21.9
T_LAND = 22.55
T_CHEER = 22.9
T_HUG = 23.25
T_SALUTE = 23.55
T_EYESD = 24.2
T_RUND = 24.6
T_E = 25.0
# E: the freezer door
T_DOPEN = 25.8
T_HAND = 26.3
T_HGRIP = 27.25
T_WHISTLE = 27.45
T_BOARD = 27.6
T_PUSH = 28.0
T_HOPON = 28.65
T_SWIPE = 29.35
T_LAUNCH = 30.15
T_F = 31.0
# F: outside
T_APEX = 32.5
T_FALLF = 32.7
T_G = 35.8
# G: the fall into the fridge
T_DUCK = 36.45                  # the Duck's one motion
T_FREEZE = 37.2
DUNS = (37.25, 37.7, 38.1)


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
    text(c, "Ep. 20:  The Ice King's Shadow", W / 2, 182, 44, (1, 1, 1), olw=8)
    c.restore()


# ---------------- shared props ----------------
def block(c, x, y, rot=0.0, s=BS, glow=0.0):
    """The ice block with a rubber duck (tilted bottle-cap crown) frozen inside. (x, y) = bottom centre."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    bw, bh = 380, 420
    if glow > 0:
        rg = cairo.RadialGradient(0, -bh / 2, 40, 0, -bh / 2, 380)
        rg.add_color_stop_rgba(0, 0.85, 0.95, 1, 0.5 * glow); rg.add_color_stop_rgba(1, 0.85, 0.95, 1, 0)
        c.rectangle(-450, -bh - 250, 900, bh + 400); c.set_source(rg); c.fill()
    the_duck(c, 0, -70, 1.15, 1.15, 0.38)
    rrect(c, -bw / 2, -bh, bw, bh, 34)
    gi = cairo.LinearGradient(-bw / 2, -bh, bw / 2, 0)
    gi.add_color_stop_rgba(0, 0.85, 0.95, 1, 0.55); gi.add_color_stop_rgba(0.5, 0.65, 0.85, 1, 0.38); gi.add_color_stop_rgba(1, 0.55, 0.78, 1, 0.55)
    c.set_source(gi); c.fill_preserve()
    c.set_source_rgb(*ICE_D); c.set_line_width(8); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.95); c.set_line_width(12); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(-bw / 2 + 40, -bh + 140); c.line_to(-bw / 2 + 110, -bh + 40); c.stroke()
    c.set_line_width(7)
    c.move_to(-bw / 2 + 40, -bh + 220); c.line_to(-bw / 2 + 170, -bh + 50); c.stroke()
    c.move_to(bw / 2 - 40, -60); c.line_to(bw / 2 - 80, -20); c.stroke()
    for (bx, by, r) in ((120, -bh + 70, 10), (140, -bh + 110, 6), (-130, -90, 8)):
        ellipse(c, bx, by, r, r, (1, 1, 1), lw=2)
    c.restore()


def king_shadow(c, t, sx, base, sc, swell=0.0, eyes=1.0, mouth=0.0, alpha=0.62):
    """The Ice King's crowned silhouette (from Ep 19), with glowing eyes and a roaring mouth."""
    c.save(); c.translate(sx, base); c.scale(sc * (1 + 0.06 * swell), sc * (1 + 0.1 * swell))
    c.move_to(-380, 0)
    c.curve_to(-400, -300, -300, -470, -170, -500)
    c.curve_to(-200, -560, -170, -640, -120, -660)
    c.curve_to(-140, -800, 140, -800, 120, -660)
    c.curve_to(170, -640, 200, -560, 170, -500)
    c.curve_to(300, -470, 400, -300, 380, 0)
    c.line_to(380, 900); c.line_to(-380, 900); c.close_path()
    c.set_source_rgba(*SHADOW, alpha); c.fill()
    c.move_to(-130, -745)
    for p in [(-150, -860), (-95, -775), (-60, -900), (-25, -780), (0, -940), (25, -780), (60, -900), (95, -775), (150, -860), (130, -745)]:
        c.line_to(*p)
    c.close_path(); c.set_source_rgba(*SHADOW, alpha); c.fill()
    if eyes > 0:
        for ex in (-45, 45):
            c.save(); c.translate(ex, -690); c.rotate(0.25 if ex < 0 else -0.25)
            c.scale(30, S(13 * eyes)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(0.55, 0.88, 1.0, 0.95); c.fill()
            ellipse(c, ex, -690, 4, S(11 * eyes), hexc("#0B2A4A"), stroke=False)
        rg = cairo.RadialGradient(0, -690, 10, 0, -690, 160)
        rg.add_color_stop_rgba(0, 0.55, 0.88, 1, 0.4 * eyes); rg.add_color_stop_rgba(1, 0.55, 0.88, 1, 0)
        c.rectangle(-220, -870, 440, 360); c.set_source(rg); c.fill()
    if mouth > 0.01:   # jagged icy roar
        c.move_to(-60, -630)
        n = 7
        for i in range(n + 1):
            c.line_to(-60 + 120 * i / n, -630 + (10 if i % 2 else 0))
        for i in range(n, -1, -1):
            c.line_to(-60 + 120 * i / n, -615 + 70 * mouth - (12 if i % 2 else 0))
        c.close_path(); c.set_source_rgba(0.7, 0.93, 1.0, 0.95); c.fill()
    c.restore()


def claw(c, x, y, s, grip=0.0, alpha=0.72):
    """The shadow's icy claw sliding along the floor; (x, y) = fingertips' reach on the floor; arm off to the right."""
    c.save(); c.translate(x, y); c.scale(s, s)
    col = (*SHADOW, alpha)
    c.push_group()
    # arm
    c.move_to(480, -330); c.curve_to(1200, -380, 2000, -470, 2800, -520); c.line_to(2800, -40); c.line_to(480, -60); c.close_path()
    c.set_source_rgb(*SHADOW); c.fill()
    # palm
    rrect(c, 230, -360, 330, 320, 90); c.fill()
    # thumb (up-left)
    c.save(); c.translate(330, -330); c.rotate(-2.2 + 0.6 * grip)
    rrect(c, 0, -30, 170, 60, 30); c.fill(); c.restore()
    # four long fingers with icicle claws
    for i in range(4):
        fy = -300 + 80 * i
        a2 = 0.05 * (i - 1.5) + grip * (0.7 + 0.1 * i)
        c.save(); c.translate(270, fy); c.rotate(math.pi - a2)
        ln = 250 - 15 * abs(i - 1.5) - 90 * grip
        rrect(c, -20, -30, ln + 20, 60, 30); c.set_source_rgb(*SHADOW); c.fill()
        c.move_to(ln - 6, -22); c.line_to(ln + 70, 0); c.line_to(ln - 6, 22); c.close_path()
        c.set_source_rgb(0.72, 0.93, 1.0); c.fill()
        c.restore()
    c.pop_group_to_source(); c.paint_with_alpha(alpha)
    for i in range(3):
        star(c, 360 + 50 * i, -300 + 40 * i, 10, i, (0.75, 0.95, 1.0))
    c.restore()


def rotd(c, x, y, a, fn):
    c.save(); rot_at(c, x, y, a); fn(); c.restore()


def run_bob(t, ph, on=True, amp=22, f=11):
    return -abs(math.sin(t * f + ph)) * amp if on else 0.0


def peep_on(c, t, x, y, mood="happy", look=(0, 0), wings="down", face=0.0, shake=0.0, rot=0.0):
    fat_peep(c, x, y, FAT, mood=mood, look=look, wings=wings, flap_t=t, face=face, shake=shake, rot=rot)


# ================= A: the roar =================
A_TEAM0 = dict(chip=600, dill=830, crumb=1040)
SHX, SHB, SHS = 1330, FL + 300, 1.9
BXA = 1330


def roar_k(t):
    return ease(seg(t, T_ROAR, T_ROAR + 0.25)) * (1 - ease(seg(t, T_ROAR_END - 0.3, T_ROAR_END)))


def blown(t):
    """How far the gale has pushed everyone left."""
    return -230 * ease_out(seg(t, T_ROAR + 0.1, T_ROAR_END))


def a_x(name, t):
    x = A_TEAM0[name] + blown(t)
    if name in ("chip", "crumb"):
        if t >= T_FLEE:
            x -= RUN_V * 1.1 * (t - T_FLEE) * ease(seg(t, T_FLEE, T_FLEE + 0.2))
        return x
    # Dill: a few steps away, halt, dash back to the block, then drag it
    if t < T_FLEE:
        return x
    x0 = x
    if t < T_HALT:
        return x0 - 320 * ease(seg(t, T_FLEE, T_HALT))
    if t < T_BACK:
        return x0 - 320 - 20 * ease_out(seg(t, T_HALT, T_HALT + 0.1))
    grab_x = BXA - BWS / 2 - 140
    if t < T_GRAB:
        return lerp(x0 - 340, grab_x, ease(seg(t, T_BACK, T_GRAB)))
    if t < T_DRAG:
        return grab_x
    return grab_x - 330 * (t - T_DRAG) ** 1.3


def a_block_x(t):
    if t < T_DRAG:
        return BXA
    return a_x("dill", t) + 140 + BWS / 2


def scene_a(c, t):
    hall_bg(c, t, 0.0)
    rk = roar_k(t)
    sw = ease(seg(t, T_INHALE, T_ROAR)) * (1 - ease(seg(t, T_ROAR, T_ROAR + 0.4)))
    c.save(); c.rectangle(-1000, -1000, 5000, FL - 290 + 1000); c.clip()
    king_shadow(c, t, SHX, SHB, SHS, swell=sw, eyes=1.0, mouth=rk)
    c.restore()
    # frosted castle pane in front of the shadow
    rrect(c, 820, -200, 1100, FL - 290 + 200, 40); c.set_source_rgba(0.85, 0.95, 1.0, 0.16); c.fill()
    c.set_source_rgba(1, 1, 1, 0.3); c.set_line_width(10)
    for k in range(5):
        c.move_to(860 + 220 * k, FL - 320); c.line_to(1010 + 220 * k, -100); c.stroke()
    # pedestal + block
    mound(c, BXA, FL + 4, 240, 70)
    bx = a_block_x(t)
    wob = 0.04 * math.sin(t * 30) if T_GRAB <= t < T_DRAG + 0.3 else 0.0
    block(c, bx, FL, wob, glow=0.6)
    # the gale
    if rk > 0:
        streaks(c, t, 0, 1700, 500, 1500, 30, 4, speed=-2200, alpha=0.6 * rk)
        flakes(c, t, 0, 1700, 400, 1500, 70, 9, wind=-1500, fall=60, alpha=rk)
    lean = 0.22 * rk
    ph_run = t >= T_FLEE
    # Chip (see-through at first, still scared from Ep 19)
    chx = a_x("chip", t)
    def ch():
        if t >= T_FLEE:
            kw = dict(mood="scared", look=(-1, 0), arms="out", shiver=0.3)
        else:
            kw = dict(mood="scared", look=(1, -1), arms="cover", shiver=1.0)
        draw_chip(c, t, chx, FL + run_bob(t, 0.3, ph_run), kw)
    alpha = lerp(0.3, 1.0, ease(seg(t, T_ROAR_END - 0.2, T_FLEE)))
    rotd(c, chx, FL, lean, lambda: glazed(c, ch, k=0.0, alpha=alpha))
    if alpha < 0.6:
        for ex in (-14, 14):
            ellipse(c, chx + ex * 1.3, FL - 92, 9, 11, INK, stroke=False)
    # Dill (+ Peep on his head)
    dx = a_x("dill", t)
    running = T_FLEE <= t < T_HALT or T_BACK <= t < T_GRAB or t >= T_DRAG
    dy = FL + run_bob(t, 1.0, running)
    if t < T_FLEE:
        dkw = dict(mood="frozen" if rk < 0.1 else "shocked", look=(1, -1), shake=3)
        drot = lean
    elif t < T_HALT:
        dkw = dict(mood="shocked", look=(-1, 0)); drot = -0.12
    elif t < T_BACK:
        dkw = dict(mood="shocked", look=(1, -0.2), arm="point"); drot = 0.1
    elif t < T_GRAB:
        dkw = dict(mood="angry", look=(1, 0), arm="point"); drot = 0.12
    elif t < T_DRAG:
        dkw = dict(mood="angry", look=(-1, 0), arm="point", shake=4); drot = -0.2
    else:
        dkw = dict(mood="angry", look=(-1, 0), arm="point", shake=2); drot = -0.22
    rotd(c, dx, FL, drot, lambda: draw_dill(c, t, dx, dy, dkw))
    hx_ = dx + 300 * math.sin(drot) * 0.0
    pmood = "shock" if t < T_GRAB else "blink"
    rotd(c, dx, FL, drot, lambda: peep_on(c, t, dx, dy - 300, mood=pmood, look=dkw["look"],
                                           wings="flap" if rk > 0.2 else "down", face=-0.6 if t >= T_FLEE else 0.6,
                                           shake=3 if t < T_FLEE else 0))
    # Crumb
    crx = a_x("crumb", t)
    if t >= T_FLEE:
        ckw = dict(mood="scared", look=(-1, 0), arm="wave"); crot = -0.12
    else:
        ckw = dict(mood="scared", look=(1, -1), shake=3); crot = lean
    rotd(c, crx, FL, crot, lambda: draw_crumb(c, t, crx, FL + run_bob(t, 2.0, ph_run), ckw))
    # words
    word(c, t, "RRROOAAARRR!", 880, 560, 92, ICE_B, T_ROAR + 0.1, T_ROAR_END, -0.06)
    word(c, t, "!!", dx + 40, FL - 560, 90, RED, T_HALT, T_BACK + 0.2, 0.08)
    word(c, t, "HNNNG!", dx + 120, FL - 520, 66, (1, 1, 1), T_GRAB, T_DRAG + 0.6, -0.08)
    word(c, t, "eep!", chx, FL - 260, 50, (1, 1, 1), 0.0, 0.9, -0.1)


def cam_a(t):
    keys = [(0.0, 980, 1000, 1.05), (T_INHALE, 1030, 960, 1.08), (T_ROAR, 960, 1000, 0.98),
            (T_ROAR_END, 860, 1080, 1.05), (T_FLEE, 800, 1120, 1.08), (T_HALT, 560, 1150, 1.1), (T_BACK, 600, 1150, 1.1),
            (T_GRAB, 1000, 1150, 1.15), (T_DRAG, 1000, 1150, 1.15), (T_B, 820, 1150, 1.1)]
    cx, cy, z = keyed(keys, t)
    if T_ROAR <= t < T_ROAR_END:
        q = 9; cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    return cx, cy, z


# ================= B: the chase =================
def gx(t):
    return -RUN_V * (t - T_B)


B_OFF = dict(crumb=-340, chip=-175, dill=0)
XI1 = None


def b_pos(name, t):
    return gx(t) + B_OFF[name]


def obstacle_hop(x, xo, h=130, wdt=95):
    if xo - wdt < x < xo + wdt:
        p = (xo + wdt - x) / (2 * wdt)
        return -h * math.sin(math.pi * p)
    return 0.0


XI1 = gx(T_ICE1_LAND) - 175 - 110          # just ahead of Chip when it lands
XI2 = gx(T_ICE2_LAND) + 140 + BWS + 120   # just behind the block


def yoink(t):
    if t < T_YOINK:
        return 0.0
    return -130 * math.exp(-(t - T_YOINK) * 2.5) * ease(seg(t, T_YOINK, T_YOINK + 0.08))


def b_block_x(t):
    return b_pos("dill", t) + 140 + BWS / 2 + yoink(t)


def claw_state(t):
    """(x of fingertips, grip)."""
    base = gx(t) + 900
    if t < T_CLAW:
        return base + 300 * (1 - seg(t, T_B, T_CLAW)), 0.0
    if t < T_CLAW_SHUT:
        p = ease(seg(t, T_CLAW, T_YOINK - 0.05))
        return lerp(base, b_block_x(T_YOINK - 0.05) + BWS / 2 - 40, p), ease(seg(t, T_YOINK - 0.05, T_CLAW_SHUT))
    return lerp(b_block_x(T_YOINK - 0.05) + BWS / 2 - 40, base + 200, ease(seg(t, T_CLAW_SHUT + 0.2, T_CLAW_SHUT + 0.9))), 1.0 - 0.6 * seg(t, T_CLAW_SHUT + 0.4, T_CLAW_SHUT + 0.9)


def corridor_bg(c, t, cx):
    g = cairo.LinearGradient(0, -200, 0, 1150)
    g.add_color_stop_rgb(0, *hexc("#0F2A4F")); g.add_color_stop_rgb(1, *hexc("#3E7CC0"))
    c.rectangle(cx - 1500, -1000, 3000, 2300); c.set_source(g); c.fill()
    # castle silhouette (parallax)
    off = cx * 0.4
    c.move_to(cx - 1500, 1150)
    k0 = int((cx - off - 1500) // 450) - 1
    for k in range(k0, k0 + 9):
        x = k * 450 + off
        hgt = 420 + 160 * ((k * 7) % 3)
        c.line_to(x, 1150 - hgt)
        for m in range(4):
            c.line_to(x + 40 + m * 100, 1150 - hgt - (40 if m % 2 == 0 else 0))
            c.line_to(x + 90 + m * 100, 1150 - hgt - (40 if m % 2 == 0 else 0))
        c.line_to(x + 450, 1150 - hgt)
    c.line_to(cx + 1500, 1150); c.close_path()
    c.set_source_rgba(*ICE_B, 0.35); c.fill()
    # pillars
    p0 = int((cx - 1300) // 700)
    for k in range(p0, p0 + 5):
        px = k * 700 + 120
        rrect(c, px - 75, 120, 150, 1040, 20)
        gp = cairo.LinearGradient(px - 75, 0, px + 75, 0)
        gp.add_color_stop_rgba(0, 0.75, 0.9, 1, 0.55); gp.add_color_stop_rgba(0.4, 1, 1, 1, 0.75); gp.add_color_stop_rgba(1, 0.6, 0.8, 1, 0.45)
        c.set_source(gp); c.fill_preserve(); c.set_source_rgba(*ICE_D, 0.8); c.set_line_width(5); c.stroke()
    i0 = int((cx - 1200) // 120)
    for k in range(i0, i0 + 22):
        icicle(c, k * 120, 380, 120 + 80 * ((k * 5) % 3), 16)
    gf = cairo.LinearGradient(0, 1150, 0, 2200)
    gf.add_color_stop_rgb(0, *hexc("#A5D8FF")); gf.add_color_stop_rgb(1, *hexc("#E7F5FF"))
    c.rectangle(cx - 1500, 1150, 3000, 2200); c.set_source(gf); c.fill()
    c.move_to(cx - 1500, 1150); c.line_to(cx + 1500, 1150); c.set_source_rgba(*ICE_D, 0.6); c.set_line_width(5); c.stroke()
    l0 = int((cx - 1500) // 260)
    for k in range(l0, l0 + 13):
        x = k * 260
        c.move_to(x, 1150); c.line_to(x + (x - cx) * 1.3, 2300)
        c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(4); c.stroke()


def falling_icicle(c, t, x, t0, t1, big=1.0):
    """A chandelier icicle dropping from the ceiling at x, smashing at t1."""
    if t < t0 or t > t1 + 1.2:
        return
    if t < t1:
        p = seg(t, t0, t1) ** 2
        y = lerp(380, FL - 260 * big, p)
        icicle(c, x, y, 260 * big, 44 * big)
    else:
        shards(c, x, FL - 10, t, t1)
        mound(c, x, FL + 4, 120 * big, 26 * big * (1 - 0.3 * seg(t, t1, t1 + 1.2)), fill=ICE, edge=ICE_B)


def scene_b(c, t, cx):
    corridor_bg(c, t, cx)
    falling_icicle(c, t, XI1, T_ICE1, T_ICE1_LAND, 0.9)
    falling_icicle(c, t, XI2, T_ICE2, T_ICE2_LAND, 1.4)
    # block
    bx = b_block_x(t)
    bh = obstacle_hop(bx, XI1, 90) if t > T_ICE1_LAND else 0.0
    block(c, bx, FL + bh, 0.05 * math.sin(t * 25), glow=0.4)
    # the claw (in front of the block)
    kx, kg = claw_state(t)
    claw(c, kx, FL + 30, 1.25, kg, alpha=0.8)
    # Dill dragging
    dx = b_pos("dill", t)
    dh = obstacle_hop(dx, XI1) if t > T_ICE1_LAND else 0.0
    dy = FL + run_bob(t, 1.0) + dh
    looking_back = T_LOOKB <= t < T_C or T_CLAW <= t < T_CLAW_SHUT + 0.4
    dkw = dict(mood="shocked" if looking_back else "angry", look=(1, 0) if looking_back else (-1, 0), arm="point", shake=2)
    rotd(c, dx, FL, -0.2, lambda: draw_dill(c, t, dx, dy, dkw))
    rotd(c, dx, FL, -0.2, lambda: peep_on(c, t, dx, dy - 300, mood="shock" if looking_back else "happy",
                                           look=(1, 0) if looking_back else (-1, 0), face=-0.6))
    # Chip
    chx = b_pos("chip", t)
    chh = obstacle_hop(chx, XI1, 150) if t > T_ICE1_LAND - 0.05 else 0.0
    rotd(c, chx, FL, -0.15, lambda: draw_chip(c, t, chx, FL + run_bob(t, 0.2) + chh,
                                               dict(mood="eep" if chh < -20 else "scared", look=(-1, 0), arms="out", shiver=0.3)))
    # Crumb (in front)
    crx = b_pos("crumb", t)
    rotd(c, crx, FL, -0.15, lambda: draw_crumb(c, t, crx, FL + run_bob(t, 2.2),
                                                dict(mood="scared", look=(1, 0) if T_LOOKB <= t else (-1, 0), arm="wave")))
    # speed streaks
    streaks(c, t, cx - 700, cx + 700, 900, 1500, 14, 8, speed=1600, alpha=0.3)
    word(c, t, "CRASH!", XI1, FL - 420, 80, (1, 1, 1), T_ICE1_LAND, T_ICE1_LAND + 0.6, -0.08)
    word(c, t, "YOINK!", dx + 120, FL - 600, 84, GOLD, T_YOINK, T_YOINK + 0.7, 0.08)
    word(c, t, "CRAAASH!", XI2 - 60, FL - 520, 100, (1, 1, 1), T_ICE2_LAND, T_ICE2_LAND + 0.7, 0.06)
    word(c, t, "AAAAAH!", crx + 120, FL - 420, 70, (1, 1, 1), T_B + 0.2, T_ICE1, -0.06)
    word(c, t, "!!", dx + 40, FL - 580, 80, RED, T_LOOKB, T_LOOKB + 0.6, 0.06)


def cam_b(t):
    cl = ease(seg(t, T_CLAW - 0.4, T_CLAW)) * (1 - ease(seg(t, T_CLAW_SHUT + 0.4, T_CLAW_SHUT + 0.9)))
    cx = gx(t) + 50 + 200 * cl
    cy, z = 1210, lerp(1.13, 0.95, cl)
    if t < T_B + 0.4:
        p = ease(seg(t, T_B, T_B + 0.4))
        z = lerp(1.0, 1.13, p)
    if T_ICE2_LAND <= t < T_ICE2_LAND + 0.3:
        q = 14 * (1 - seg(t, T_ICE2_LAND, T_ICE2_LAND + 0.3)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    if T_ICE1_LAND <= t < T_ICE1_LAND + 0.25:
        q = 8; cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    return cx, cy, z


# ================= C + D: the crack =================
FLC = 1250
XM = 760
CW = 270
XR = XM + CW / 2


def crack_w(t):
    return CW * ease_out(seg(t, T_CRACK + 0.12, T_CRACK + 0.45))


def crack_bg(c, t, cx, cy):
    g = cairo.LinearGradient(0, -400, 0, FLC)
    g.add_color_stop_rgb(0, *hexc("#0F2A4F")); g.add_color_stop_rgb(1, *hexc("#3E7CC0"))
    c.rectangle(-800, -800, 3200, FLC + 800); c.set_source(g); c.fill()
    for px in (-60, 1500):
        rrect(c, px - 75, -100, 150, FLC + 100, 20)
        c.set_source_rgba(0.85, 0.95, 1, 0.55); c.fill_preserve(); c.set_source_rgba(*ICE_D, 0.8); c.set_line_width(5); c.stroke()
    for k in range(-6, 22):
        icicle(c, k * 120, -40, 120 + 80 * ((k * 5) % 3), 16)
    rnd = random.Random(31)
    for j in range(18):
        x = -300 + rnd.random() * 2200; y = -300 + rnd.random() * (FLC + 200)
        star(c, x, y, 6 + 4 * math.sin(t * 3 + j), j, (1, 1, 1))
    w = crack_w(t)
    xl, xr = XM - w / 2, XM + w / 2
    # the ice cliffs (cut-away below the floor)
    for (a, b) in ((-900, xl), (xr, 2600)):
        if b - a < 1:
            continue
        gi = cairo.LinearGradient(0, FLC, 0, FLC + 2600)
        gi.add_color_stop_rgb(0, *hexc("#A5D8FF")); gi.add_color_stop_rgb(1, *hexc("#3E7CC0"))
        c.rectangle(a, FLC, b - a, 2800); c.set_source(gi); c.fill()
    # gap
    if w > 1:
        gg = cairo.LinearGradient(0, FLC, 0, FLC + 2000)
        gg.add_color_stop_rgb(0, *hexc("#1C3E6E")); gg.add_color_stop_rgb(1, *hexc("#050D1F"))
        c.move_to(xl, FLC)
        for i in range(1, 15):
            y = FLC + i * 180
            c.line_to(xl + (18 if i % 2 else -10) * (w / CW), y)
        c.line_to(xl, FLC + 2800); c.line_to(xr, FLC + 2800)
        for i in range(14, 0, -1):
            y = FLC + i * 180
            c.line_to(xr + (-16 if i % 2 else 12) * (w / CW), y)
        c.line_to(xr, FLC); c.close_path()
        c.set_source(gg); c.fill_preserve(); c.set_source_rgb(*ICE_D); c.set_line_width(6); c.stroke()
    # facets on the cliffs
    c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(5)
    for k in range(-4, 12):
        x = k * 200 + 40
        if xl - 40 < x < xr + 40:
            continue
        c.move_to(x, FLC + 120); c.line_to(x + 60, FLC + 600 + 80 * (k % 3)); c.stroke()
    # floor top edge
    c.move_to(-900, FLC); c.line_to(xl, FLC); c.move_to(xr, FLC); c.line_to(2600, FLC)
    c.set_source_rgb(*ICE_D); c.set_line_width(8); c.stroke()
    # the crack line before it opens
    if T_CRACK <= t < T_CRACK + 0.5:
        p = ease_out(seg(t, T_CRACK, T_CRACK + 0.15))
        c.set_source_rgb(*ICE_D); c.set_line_width(6)
        c.move_to(XM, FLC - 4)
        for i in range(1, 7):
            c.line_to(XM + (12 if i % 2 else -12), FLC - 4 + i * 40 * p)
        c.stroke()


GRIP = (XR - 10, FLC + 5)          # where Crumb hangs on
HANG = 330                         # grip point -> feet
LAND_X = XR + 470
BLOCK_C = XR + 700


def draw_crumb_hanging(c, t, gx_, gy_, kw, sway=0.0, flail=1.0):
    """Crumb hanging by one hand from the point (gx_, gy_): right arm straight up, left arm flailing."""
    c.save(); rot_at(c, gx_, gy_, sway)
    fx, fy = gx_ - 40, gy_ + HANG
    draw_crumb(c, t, fx, fy, dict(kw, arm="none"))
    c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(fx + 70, fy - 130); c.line_to(gx_, gy_ + 6); c.stroke()
    ellipse(c, gx_, gy_ + 4, 13, 11, CRUST_C, lw=4)
    a = math.sin(t * 14) * flail
    c.move_to(fx - 70, fy - 120); c.line_to(fx - 120, fy - 60 - 50 * a); c.stroke()
    c.restore()


def c_crumb(t):
    """Crumb until the catch: (x, y feet, rot, kw, mode)."""
    if t < T_SKID:
        return 1560 - RUN_V * (t - T_C), FLC, -0.15, dict(mood="scared", look=(-1, 0), arm="wave"), "run"
    if t < T_SLIP:
        x0 = 1560 - RUN_V * (T_SKID - T_C)
        p = seg(t, T_SKID, T_SLIP)
        return x0 - 260 * p * (1 - 0.3 * p), FLC, 0.28, dict(mood="scared", look=(-1, 0), arm="wave_l"), "skid"
    x1 = 1560 - RUN_V * (T_SKID - T_C) - 260 * 0.7
    if t < T_OVER:
        p = seg(t, T_SLIP, T_OVER)
        return lerp(x1, XR + 60, p), FLC - 40, 1.35 * ease_out(seg(t, T_SLIP, T_SLIP + 0.2)), dict(mood="scared", look=(-1, -1), arm="wave"), "slide"
    if t < T_CATCH:
        p = seg(t, T_OVER, T_CATCH)
        return lerp(XR + 60, GRIP[0], p), lerp(FLC - 40, GRIP[1], p), lerp(1.35, 0.0, p), dict(mood="scared", look=(0, -1)), "drop"
    if t < T_FALL:
        slip = 0.0
        if t >= T_SLIPGRIP:
            slip = 8 * ease(seg(t, T_SLIPGRIP, T_SLIPGRIP + 0.4))
        sway = 0.12 * math.sin((t - T_CATCH) * 3.0) * math.exp(-(t - T_CATCH) * 0.5)
        return GRIP[0], GRIP[1] + slip, sway, dict(mood="scared", look=(0, -1), shake=2 if t >= T_SLIPGRIP else 0), "hang"
    q = t - T_FALL
    return GRIP[0] - 30 * q, GRIP[1] + 10 + 450 * q * q, 0.5 * q, dict(mood="scared", look=(0, -1)), "fall"


def grip_at_catch():
    q = T_GRABP - T_FALL
    return GRIP[0] - 30 * q, GRIP[1] + 10 + 450 * q * q


def peep_carry(t):
    """(px, py) Peep's feet = Crumb's grip point while carrying him."""
    gx0, gy0 = grip_at_catch()
    if t < T_POWER:
        p = seg(t, T_GRABP, T_POWER)
        return gx0, gy0 + 130 * ease_out(p) + 8 * math.sin(t * 30)
    if t < T_RISE:
        return gx0, gy0 + 130 + 6 * math.sin(t * 40)
    if t < T_TOP:
        p = ease(seg(t, T_RISE, T_TOP))
        return lerp(gx0, XM + 60, p), lerp(gy0 + 130, FLC - 520, p)
    p = ease(seg(t, T_TOP, T_LAND))
    return lerp(XM + 60, LAND_X + 40, p), lerp(FLC - 520, FLC - HANG, p) - 100 * math.sin(math.pi * p)


def d_c_pos(t):
    """Dill's feet: he runs in, skids to the lip and teeters, Chip yanks him back; later he kneels to reach."""
    xs = 1560 + 560 - RUN_V * (t - T_C)
    lip = XR + 90
    if t < T_DILL_IN:
        return max(xs, lip + 100), FLC
    if t < T_YANK:
        return lerp(lip + 100, lip, ease_out(seg(t, T_DILL_IN, T_DILL_IN + 0.3))), FLC
    if t < T_CHEER:
        return lerp(lip, XR + 270, ease(seg(t, T_YANK, T_YANK + 0.3))), FLC
    return lerp(XR + 270, XR + 300, ease(seg(t, T_CHEER, T_CHEER + 0.3))), FLC


def c_block(t):
    xs = 1560 + 560 + 140 + BWS / 2 - RUN_V * (t - T_C)
    return max(xs, BLOCK_C), FLC, 0.0


def chip_c(t):
    xs = 1560 + 170 - RUN_V * (t - T_C)
    if t < T_YANK:
        return max(xs, XR + 330), FLC
    if t < T_REACH:
        return XR + 330, FLC
    if t < T_CHEER:
        return lerp(XR + 330, XR + 75, ease(seg(t, T_REACH, T_REACH + 0.35))), FLC
    return lerp(XR + 75, XR + 130, ease(seg(t, T_CHEER, T_CHEER + 0.3))), FLC


def peep_dive(t):
    """Peep from leaving Dill's head to the catch: (x, y, mood, wings, rot)."""
    dx, dy = d_c_pos(T_PJUMP)
    gx0, gy0 = grip_at_catch()
    if t < T_PJUMP + 0.3:
        x, y = hop((dx, dy - 300), (XR - 40, FLC - 100), seg(t, T_PJUMP, T_PJUMP + 0.3), 120)
        return x, y, "shock", "flap", 0.0
    p = seg(t, T_PJUMP + 0.3, T_GRABP)
    return lerp(XR - 40, gx0, p), lerp(FLC - 100, gy0, p ** 1.4), "blink", "flap", 0.4 * (1 - p)


def scene_cd(c, t, cx, cy):
    crack_bg(c, t, cx, cy)
    # glowing eyes deep in the crack (end of D)
    if t >= T_EYESD:
        o = ease(seg(t, T_EYESD, T_EYESD + 0.3))
        for ex in (-45, 45):
            c.save(); c.translate(XM + ex, FLC + 800); c.rotate(0.25 if ex < 0 else -0.25)
            c.scale(36, S(15 * o)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(0.55, 0.88, 1.0, 0.95); c.fill()
            ellipse(c, XM + ex, FLC + 800, 5, S(13 * o), hexc("#0B2A4A"), stroke=False)
    run_off = (lambda: RUN_V * 1.3 * (t - T_RUND)) if t >= T_RUND else (lambda: 0.0)
    # block
    bx, by, _ = c_block(t)
    block(c, bx + run_off() * 0, by, 0.0, glow=0.4)
    # Dill
    dx, dy = d_c_pos(t)
    walking = t < T_DILL_IN
    dkw = dict(mood="angry", look=(-1, 0), arm="point"); drot = -0.2 if walking else 0.0
    if T_DILL_IN <= t < T_TEETER:
        dkw = dict(mood="shocked", look=(-1, 0.6), arm="reach"); drot = -0.15
    elif T_TEETER <= t < T_YANK:
        dkw = dict(mood="shocked", look=(-1, 1), arm="reach", shake=2)
        drot = -0.2 + 0.28 * math.sin((t - T_TEETER) * 16)
    elif T_YANK <= t < T_REACH2:
        dkw = dict(mood="shocked", look=(-1, 0.6)); drot = 0.15 * (1 - seg(t, T_YANK, T_YANK + 0.4))
    elif T_REACH2 <= t < T_FALL:
        dkw = dict(mood="angry", look=(-1, 1), arm="point_l", shake=3); drot = -0.45 * ease(seg(t, T_REACH2, T_REACH2 + 0.3))
    elif T_FALL <= t < T_LAND:
        dkw = dict(mood="shocked", look=(-1, 1)); drot = -0.45 * (1 - ease(seg(t, T_FALL + 0.6, T_FALL + 1.0)))
    elif T_LAND <= t < T_SALUTE:
        dkw = dict(mood="shocked", look=(1, -0.3))
    elif T_SALUTE <= t < T_EYESD:
        dkw = dict(mood="proud", look=(1, -0.3), arm="up")
    else:
        dkw = dict(mood="shocked", look=(-1, 1), shake=3)
    if t >= T_RUND:
        dx += run_off(); dkw = dict(mood="shocked", look=(1, 0), arm="point"); drot = 0.15
    dyy = dy + run_bob(t, 1.0, walking or t >= T_RUND)
    rotd(c, dx, FLC, drot, lambda: draw_dill(c, t, dx, dyy, dkw))
    if t < T_PJUMP:
        pm = "happy" if t < T_CRACK else "shock"
        rotd(c, dx, FLC, drot, lambda: peep_on(c, t, dx, dyy - 300, mood=pm, look=(-1, 0.6), face=-0.6))
    # Chip
    chx, chy = chip_c(t)
    chmood, charms, chrot = "scared", "out", 0.0
    if t < T_CHIP_IN:
        chrot = -0.15
    if T_TEETER <= t < T_YANK + 0.3:
        chmood, charms = "eep", "out"
    if T_REACH <= t < T_FALL:
        chmood, charms, chrot = "eep", "out", -0.35 * ease(seg(t, T_REACH, T_REACH + 0.3))
    if T_FALL <= t < T_CHEER:
        chmood, charms = "scared", "cover"
    if T_CHEER <= t < T_EYESD:
        chmood, charms, chrot = "happy", "up", 0.0
    if t >= T_EYESD:
        chmood, charms = "eep", "cover"
    if t >= T_RUND:
        chx += run_off(); chmood, charms, chrot = "scared", "out", 0.15
    melt = 0.18 * ease(seg(t, T_HUG + 0.4, T_HUG + 1.0)) if t >= T_HUG + 0.4 else 0.0
    rotd(c, chx, FLC, chrot, lambda: draw_chip(c, t, chx, chy + run_bob(t, 0.3, t < T_CHIP_IN or t >= T_RUND),
                                                dict(mood=chmood, look=(-1, 0.6), arms=charms, shiver=0.4, melt=melt,
                                                     blush=0.6 if T_CHEER <= t < T_EYESD else 0.0)))
    if t >= T_HUG + 0.6 and t < T_RUND:
        for j in range(2):
            q = ((t - T_HUG - 0.6) * 1.5 + j * 0.5) % 1
            ellipse(c, chx - 50 + 100 * j, FLC - 10 + 40 * q, 7, 10, ICE_B, lw=2)
    # the drip from Chip onto Crumb's face
    if T_DRIP <= t < T_DRIP + 0.45:
        p = seg(t, T_DRIP, T_DRIP + 0.45)
        ellipse(c, lerp(XR + 10, GRIP[0] - 40, p), lerp(FLC - 120, FLC + HANG - 170, p * p), 10, 14, ICE_B, lw=3)
    # Crumb
    if t < T_GRABP:
        x, y, rot, kw, mode = c_crumb(t)
        if mode in ("hang", "fall"):
            draw_crumb_hanging(c, t, x, y, kw, sway=rot, flail=1.0 if mode == "fall" else 0.5)
        elif mode == "drop":
            rotd(c, x, y, rot, lambda: draw_crumb_hanging(c, t, x, y, kw, flail=1.0))
        else:
            rotd(c, x, y, rot, lambda: draw_crumb(c, t, x, y + (run_bob(t, 2.2) if mode == "run" else 0), kw))
        if mode == "skid":
            for j in range(6):
                q = (t * 6 + j / 6) % 1
                ellipse(c, x - 40 + 60 * q, y - 20 - 70 * q, 10 * (1 - q) + 2, 10 * (1 - q) + 2, (1, 1, 1), lw=2)
    elif t < T_LAND:
        px, py = peep_carry(t)
        draw_crumb_hanging(c, t, px, py, dict(mood="scared" if t < T_RISE else "worried", look=(0, -1)),
                           sway=0.12 * math.sin(t * 4), flail=0.6)
    else:
        crx, cry = LAND_X, FLC
        hugging = T_HUG <= t < T_EYESD
        if t >= T_RUND:
            crx += run_off()
            ckw = dict(mood="scared", look=(1, 0), arm="wave")
        else:
            ckw = dict(mood="sheepish" if hugging else ("scared" if t >= T_EYESD else "worried"),
                       look=(0, -1) if hugging else (-1, 0), arm="none" if hugging else "down")
        draw_crumb(c, t, crx, cry + run_bob(t, 2.0, t >= T_RUND), ckw)
        if hugging:
            c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
            c.move_to(crx - 70, cry - 120); c.line_to(crx - 45, cry - 280)
            c.move_to(crx + 70, cry - 120); c.line_to(crx + 45, cry - 280); c.stroke()
    # Peep
    if T_PJUMP <= t < T_GRABP:
        px, py, pm, pw, pr = peep_dive(t)
        peep_on(c, t, px, py, mood=pm, wings=pw, look=(0, 1), rot=pr)
    elif T_GRABP <= t < T_LAND:
        px, py = peep_carry(t)
        pm = "blink" if t < T_POWER else ("proud" if t < T_TOP else "happy")
        if T_POWER <= t < T_TOP + 0.3:
            k = ease(seg(t, T_POWER, T_POWER + 0.3)) * (1 - seg(t, T_TOP, T_TOP + 0.3))
            rg = cairo.RadialGradient(px, py - 90, 20, px, py - 90, 300)
            rg.add_color_stop_rgba(0, 1, 0.9, 0.4, 0.6 * k); rg.add_color_stop_rgba(1, 1, 0.9, 0.4, 0)
            c.rectangle(px - 320, py - 420, 640, 640); c.set_source(rg); c.fill()
        peep_on(c, t, px, py, mood=pm, wings="flap", look=(0, -1), shake=3 if t < T_POWER else 0)
        if t >= T_POWER:
            for j in range(4):
                star(c, px + 130 * math.cos(t * 5 + j * 1.6), py - 90 + 130 * math.sin(t * 5 + j * 1.6), 16, t * 3 + j, GOLD)
            if t < T_TOP:
                for j in range(5):
                    q = (t * 3 + j / 5) % 1
                    c.move_to(px - 120 + 60 * j, py + 380 + 200 * q); c.line_to(px - 120 + 60 * j, py + 520 + 200 * q)
                    c.set_source_rgba(1, 1, 1, 0.6 * (1 - q)); c.set_line_width(6); c.stroke()
    elif t >= T_LAND:
        hugging = T_HUG <= t < T_EYESD
        crx = LAND_X + (run_off() if t >= T_RUND else 0)
        pm = "love" if hugging else ("shock" if t >= T_EYESD else "proud")
        yy = FLC - 270 + run_bob(t, 2.0, t >= T_RUND)
        if t < T_LAND + 0.3:
            _, py = peep_carry(T_LAND)
            yy = lerp(py, yy, ease(seg(t, T_LAND, T_LAND + 0.3)))
        peep_on(c, t, crx, yy, mood=pm, wings="hug" if hugging else ("salute" if T_CHEER <= t < T_HUG else "down"))
        if hugging:
            for j in range(3):
                q = ((t - T_HUG) * 0.8 + j / 3) % 1
                heart(c, crx - 70 + 70 * j, yy - 230 - 160 * q, 1.5, 1 - q)
    if T_CHEER <= t:
        confetti(c, t, T_CHEER, LAND_X - 150, FLC - 450, n=50)
    # words
    word(c, t, "CRACK!", XM, FLC - 330, 100, (1, 1, 1), T_CRACK, T_CRACK + 0.6, -0.06)
    word(c, t, "whoa-", 1300, FLC - 380, 60, (1, 1, 1), T_SKID, T_SLIP + 0.2, 0.1)
    word(c, t, "whoa-whoa-", XR + 120, FLC - 560, 58, (1, 1, 1), T_TEETER, T_YANK, 0.08)
    word(c, t, "nnngh!", XR + 470, FLC - 330, 60, (1, 1, 1), T_REACH2, T_SLIPGRIP, -0.08)
    word(c, t, "plip", GRIP[0] - 170, FLC + 150, 46, ICE_B, T_DRIP + 0.4, T_DRIP + 0.9, 0.1)
    word(c, t, "slip...", GRIP[0] - 170, FLC + 60, 56, (1, 1, 1), T_SLIPGRIP, T_FALL, -0.1)
    word(c, t, "AAAAAA!", XM - 40, FLC + 260, 74, (1, 1, 1), T_FALL + 0.1, T_PJUMP + 0.3, 0.06)
    word(c, t, "PEEP!!", XR + 150, FLC - 520, 80, GOLD, T_PJUMP, T_PJUMP + 0.7, -0.06)
    gx0, gy0 = grip_at_catch()
    word(c, t, "flap flap flap", XM, gy0 + 560, 56, (1, 1, 1), T_GRABP + 0.1, T_POWER, 0.05)
    word(c, t, "YAAAAY!", LAND_X - 160, FLC - 640, 96, GOLD, T_CHEER, T_EYESD, -0.05)
    word(c, t, "awww", LAND_X + 160, FLC - 380, 56, (1, 0.7, 0.8), T_HUG + 0.3, T_EYESD, 0.08)
    word(c, t, "!!", XM, FLC + 650, 100, RED, T_EYESD + 0.15, T_E, 0.06)


def cam_cd(t):
    gx0, gy0 = grip_at_catch()
    keys = [(T_C, 1150, 1050, 1.0), (T_CRACK, 1050, 1080, 1.0), (T_SLIP, 1000, 1150, 1.05), (T_CATCH, 1000, 1200, 1.1),
            (T_TEETER, 1050, 1150, 1.15), (T_REACH, 1000, 1200, 1.15), (T_SLIPGRIP, 950, 1250, 1.25), (T_FALL, 950, 1300, 1.25),
            (T_GRABP, 880, gy0 + 50, 1.1), (T_POWER, 860, gy0 + 120, 1.25), (T_RISE, 860, gy0 + 100, 1.2),
            (T_TOP, 950, 1000, 1.0), (T_LAND, 1250, 1000, 1.1), (T_CHEER, 1250, 1000, 1.1), (T_HUG + 0.3, 1300, 1020, 1.25),
            (T_EYESD, 1100, 1300, 0.9), (T_E, 1250, 1250, 0.9)]
    cx, cy, z = keyed(keys, t)
    if T_CRACK <= t < T_CRACK + 0.3:
        q = 12 * (1 - seg(t, T_CRACK, T_CRACK + 0.3)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    return cx, cy, z


# ================= E: the freezer door =================
FLE = 1400
EDGE = 300
EX0 = 1240                     # where the block sits before the push


def light_w(t):
    return lerp(0, 420, ease(seg(t, T_DOPEN, T_DOPEN + 0.6)))


def e_bg(c, t):
    g = cairo.LinearGradient(0, -200, 0, FLE)
    g.add_color_stop_rgb(0, *hexc("#16325C")); g.add_color_stop_rgb(1, *hexc("#3E7CC0"))
    c.rectangle(-600, -800, 2800, FLE + 800); c.set_source(g); c.fill()
    # frosty back wall
    for k in range(10):
        c.move_to(-200 + k * 220, -300); c.line_to(-100 + k * 220, FLE)
        c.set_source_rgba(1, 1, 1, 0.12); c.set_line_width(26); c.stroke()
    # wire shelf with the ice-cube tray, upper right
    sy = FLE - 900
    c.set_source_rgb(*hexc("#CED4DA")); c.set_line_width(10)
    c.move_to(1150, sy); c.line_to(2400, sy); c.stroke()
    for k in range(12):
        c.move_to(1170 + k * 100, sy); c.line_to(1020 + k * 100, sy + 30); c.stroke()
    rrect(c, 1330, sy - 90, 460, 90, 14); c.set_source_rgb(*hexc("#4DABF7")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    for k in range(5):
        rrect(c, 1350 + k * 88, sy - 120, 76, 70, 14); c.set_source_rgba(0.9, 0.97, 1, 0.9); c.fill_preserve()
        c.set_source_rgb(*ICE_D); c.set_line_width(4); c.stroke()
    # icicles from the ceiling
    for k in range(-3, 16):
        icicle(c, k * 130, -60, 100 + 70 * ((k * 3) % 3), 16)
    # ice floor (the freezer shelf)
    gf = cairo.LinearGradient(0, FLE, 0, FLE + 600)
    gf.add_color_stop_rgb(0, *hexc("#A5D8FF")); gf.add_color_stop_rgb(1, *hexc("#E7F5FF"))
    c.rectangle(EDGE, FLE, 2400, 900); c.set_source(gf); c.fill()
    c.move_to(EDGE, FLE); c.line_to(2400, FLE); c.set_source_rgb(*ICE_D); c.set_line_width(7); c.stroke()
    c.move_to(EDGE, FLE); c.line_to(EDGE, FLE + 900); c.stroke()
    # the door / the light beyond
    lw = light_w(t)
    c.rectangle(-600, -800, EDGE + 600 + 0, FLE + 2000); c.set_source_rgb(*hexc("#1C3E6E")); c.fill()
    if lw > 0:
        k = lw / 420
        gl = cairo.LinearGradient(-600, 0, EDGE + 300, 0)
        gl.add_color_stop_rgb(0, *hexc("#FFF4D6")); gl.add_color_stop_rgb(1, *hexc("#FFE8A3"))
        c.save(); c.rectangle(-600, -800, EDGE + 600, FLE + 2000); c.clip(); c.set_source(gl); c.paint_with_alpha(k); c.restore()
        for i in range(7):
            a = -0.5 + 0.17 * i + 0.03 * math.sin(t * 2 + i)
            c.move_to(EDGE - 20, FLE - 900 + 110 * i)
            c.line_to(EDGE + 3000 * math.cos(a), FLE - 900 + 110 * i + 3000 * math.sin(a))
            c.line_to(EDGE + 3000 * math.cos(a + 0.05), FLE - 900 + 110 * i + 3000 * math.sin(a + 0.05))
            c.close_path(); c.set_source_rgba(1, 0.95, 0.75, 0.16 * k); c.fill()
    # door slab swinging away (inner panel + rubber gasket)
    dw = lerp(EDGE + 600, 0, ease(seg(t, T_DOPEN, T_DOPEN + 0.6)))
    if dw > 2:
        c.rectangle(EDGE - dw, -800, dw, FLE + 2000); c.set_source_rgb(*hexc("#E9EEF2")); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
        c.rectangle(EDGE - 40, -800, 40, FLE + 2000); c.set_source_rgb(*hexc("#868E96")); c.fill()
    if lw > 0:
        c.rectangle(EDGE, -800, 2600, FLE + 2000); c.set_source_rgba(1, 0.9, 0.6, 0.18 * lw / 420); c.fill()


def e_hand(t):
    """(fingertips x, y, grip)."""
    if t < T_HAND:
        return -900, FLE - 1060, 0.0
    p = ease(seg(t, T_HAND, T_HGRIP))
    x = lerp(-900, 1570, p)
    return x, FLE - 1060, 0.6 * ease(seg(t, T_HGRIP, T_HGRIP + 0.2))


SLED_A = (EX0 - EDGE - 60) / (T_LAUNCH - T_PUSH) ** 2
SLED_V = 2 * SLED_A * (T_LAUNCH - T_PUSH)


def sled_x(t):
    """Bottom-centre x of the block (sled) in scene E."""
    x0 = EX0
    if t < T_PUSH:
        return x0
    q = t - T_PUSH
    return x0 - SLED_A * q * q


def sled_riders(c, t, x, y, mood="scared", wind=0.0, flying=False):
    """Chip and Crumb (with Peep on his head) sitting on top of the block, Dill clinging at the back.
    (x, y) = block bottom centre in the current transform."""
    top = y - BHS
    lean = -0.12 * wind
    rotd(c, x - 80, top, lean, lambda: draw_chip(c, t, x - 85, top + 6, dict(mood="eep" if flying else "scared", look=(-1, 0), arms="up" if flying else "out", shiver=0.3)))
    rotd(c, x + 75, top, lean, lambda: draw_crumb(c, t, x + 75, top + 4, dict(mood=mood, look=(-1, 0), arm="wave_l" if flying else "wave")))
    rotd(c, x + 75, top, lean, lambda: peep_on(c, t, x + 75, top - 296, mood="shock" if flying else "proud", look=(-1, 0), wings="flap" if flying else "salute", face=-0.6))
    rotd(c, x + BWS / 2 + 50, y - 40, -0.35, lambda: draw_dill(c, t, x + BWS / 2 + 50, y - 40, dict(mood="shocked" if flying else "angry", look=(-1, 0), arm="reach")))


def scene_e(c, t, cx):
    e_bg(c, t)
    # the shadow claw from the right
    if t >= T_SWIPE - 0.6:
        p = seg(t, T_SWIPE - 0.6, T_SWIPE)
        kx = lerp(2200, sled_x(T_SWIPE) + BWS / 2 + 100, ease(p))
        kg = ease(seg(t, T_SWIPE, T_SWIPE + 0.2))
        if t > T_SWIPE + 0.3:
            kx = lerp(kx, 2400, ease(seg(t, T_SWIPE + 0.3, T_SWIPE + 0.9)))
        claw(c, kx, FLE + 20, 0.9, kg)
    boarded = t >= T_HOPON
    sx = sled_x(t)
    sy = FLE
    srot = 0.0
    if t >= T_LAUNCH:
        q = t - T_LAUNCH
        sx = sled_x(T_LAUNCH) - SLED_V * q
        sy = FLE - 300 * q + 600 * q * q
        srot = -0.3 * q
    # the block
    rotd(c, sx, sy, srot, lambda: block(c, sx, sy, 0.0, glow=0.3))
    # sparks of ice spray behind the sled
    if T_PUSH <= t < T_LAUNCH:
        for j in range(8):
            q = (t * 5 + j / 8) % 1
            ellipse(c, sx + BWS / 2 + 30 + 160 * q, FLE - 10 - 120 * q * (1 - q) * 4, 9 * (1 - q) + 2, 9 * (1 - q) + 2, (1, 1, 1), lw=2)
    if boarded:
        c.save(); rot_at(c, sx, sy, srot)
        sled_riders(c, t, sx, sy, mood="scared", wind=1.0 if t < T_LAUNCH else 0.0, flying=t >= T_LAUNCH)
        c.restore()
    else:
        # boarding: Chip and Crumb hop on, Dill pushes
        top = FLE - BHS
        chx0, crx0 = EX0 - 400, EX0 - 590
        a0 = ease(seg(t, T_E, T_E + 0.7))
        chx = lerp(1900, chx0, a0); crx = lerp(2100, crx0, a0)
        dxx = lerp(2300, EX0 + BWS / 2 + 120, a0)
        running = t < T_E + 0.7
        dazzled = T_DOPEN <= t < T_WHISTLE
        # Chip
        if t < T_BOARD:
            draw_chip(c, t, chx, FLE + run_bob(t, 0.3, running), dict(mood="happy" if dazzled else "scared", look=(-1, -0.5), arms="out", shiver=0.3))
        else:
            px, py = hop((chx0, FLE), (sx - 85, top + 6), seg(t, T_BOARD, T_BOARD + 0.3), 200)
            draw_chip(c, t, px, py, dict(mood="eep", look=(-1, 0), arms="up", shiver=0.3))
        # Crumb + Peep
        if t < T_BOARD + 0.15:
            ckw = dict(mood="worried" if dazzled else "scared", look=(-1, -0.5), arm="wave_l" if dazzled else "wave")
            draw_crumb(c, t, crx, FLE + run_bob(t, 2.0, running), ckw)
            peep_on(c, t, crx, FLE - 296 + run_bob(t, 2.0, running), mood="love" if dazzled else "shock", look=(-1, -0.5), face=-0.6)
        else:
            px, py = hop((crx0, FLE), (sx + 75, top + 4), seg(t, T_BOARD + 0.15, T_BOARD + 0.5), 220)
            draw_crumb(c, t, px, py, dict(mood="scared", look=(-1, 0), arm="wave"))
            peep_on(c, t, px, py - 296, mood="shock", look=(-1, 0), face=-0.6)
        # Dill: whistles, then pushes the block
        if t < T_PUSH:
            dkw = dict(mood="proud" if T_WHISTLE <= t else "shocked", look=(-1, -0.5), arm="up" if T_WHISTLE <= t < T_PUSH else "down")
            dxp = dxx
        else:
            dxp = sx + BWS / 2 + 110
            dkw = dict(mood="angry", look=(-1, 0), arm="point_l", shake=2)
        rotd(c, dxp, FLE, -0.3 if t >= T_PUSH else 0.0,
             lambda: draw_dill(c, t, dxp, FLE + run_bob(t, 1.0, running or t >= T_PUSH), dkw))
    # the Hand (drawn on top: reaching in overhead)
    hx, hy, hg = e_hand(t)
    if hx > -880:
        c.save(); c.translate(hx, hy); c.rotate(-math.pi / 2); c.scale(0.75, 0.75)
        hand_cuffed(c, 0, 0, hg)
        c.restore()
    word(c, t, "fweet!", 1250, FLE - 520, 64, (1, 1, 1), T_WHISTLE, T_WHISTLE + 0.5, -0.08)
    word(c, t, "ooooh...", 700, FLE - 520, 60, (1, 0.95, 0.7), T_DOPEN + 0.3, T_HAND + 0.6, 0.05)
    word(c, t, "SWIPE!", 1350, FLE - 420, 80, ICE_B, T_SWIPE, T_SWIPE + 0.6, 0.08)
    word(c, t, "WHEEEE!", 420, FLE - 900, 90, GOLD, T_LAUNCH, T_F, -0.06)


def cam_e(t):
    keys = [(T_E, 1100, 1080, 0.88), (T_DOPEN, 820, 1050, 0.85), (T_HAND + 0.5, 800, 900, 0.78), (T_WHISTLE, 950, 1050, 0.92),
            (T_PUSH, 950, 1050, 0.95)]
    cx, cy, z = keyed(keys, t)
    if t >= T_PUSH:
        cx = min(cx, sled_x(t) + 200) if t < T_LAUNCH else sled_x(T_LAUNCH) + 200 - 400 * ease(seg(t, T_LAUNCH, T_F))
        cx = max(cx, 500)
    return cx, cy, z


# ================= F: outside =================
def fridge_open_inside(c, x0, x1, y0, y1):
    g = cairo.LinearGradient(0, y0, 0, y1)
    g.add_color_stop_rgb(0, *hexc("#F3FAFF")); g.add_color_stop_rgb(1, *hexc("#BFE0F5"))
    c.rectangle(x0, y0, x1 - x0, y1 - y0); c.set_source(g); c.fill()
    for sy in (y0 + 0.33 * (y1 - y0), y0 + 0.7 * (y1 - y0)):
        c.rectangle(x0, sy, x1 - x0, 14); c.set_source_rgb(*hexc("#A5D8FF")); c.fill()
    # jello on the lower shelf
    jy = y0 + 0.7 * (y1 - y0)
    rrect(c, x1 - 170, jy - 70, 110, 70, 14); c.set_source_rgb(*hexc("#FF6B6B")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()


def sled_f(t):
    """(x, y, s, rot) of the sled in the exterior shot."""
    x0, y0 = 470, 600
    if t < T_APEX:
        p = seg(t, T_F, T_APEX)
        x = lerp(x0, 600, p)
        y = lerp(y0, 330, ease_out(p))
        return x, y, lerp(0.42, 0.6, p), -0.3 - 4.0 * p
    p = seg(t, T_APEX, T_G)
    x = lerp(600, 430, p)
    y = lerp(330, 1450, p * p)
    return x, y, lerp(0.6, 0.75, p), -0.3 - 4.0 - 1.5 * p


def scene_f(c, t):
    c.rectangle(-1000, -1500, 3000, 1400); c.set_source_rgb(*hexc("#FFF1D6")); c.fill()
    kitchen_bg(c)
    c.rectangle(FX0 - 10, FTOP - 20, FX1 - FX0 + 20, KFLOOR - FTOP + 20); c.set_source_rgb(*hexc("#DDE7EE")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(9); c.stroke()
    c.rectangle(FX0 + 10, KFLOOR - 25, FX1 - FX0 - 20, 20); c.set_source_rgb(*hexc("#868E96")); c.fill()
    door(c, FX0, FX1, MTOP, MBOT, 1.15, fridge_open_inside)
    door(c, FX0, FX1, FTOP, FZB, 1.2, blizzard_inside(t))
    # glow from the open main door
    rg = cairo.RadialGradient(400, 1300, 50, 400, 1300, 700)
    rg.add_color_stop_rgba(0, 1, 1, 0.9, 0.35); rg.add_color_stop_rgba(1, 1, 1, 0.9, 0)
    c.rectangle(-300, 500, 1500, 1500); c.set_source(rg); c.fill()
    # the Hand in the freezer, fingers splayed in surprise
    c.save(); c.translate(600, lerp(560, -500, ease(seg(t, T_F, T_F + 0.9)))); c.scale(0.42, 0.42)
    hand_cuffed(c, 0, 0, 0.0)
    c.restore()
    # the sled
    x, y, s, rot = sled_f(t)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    block(c, 0, BHS / 2, 0.0, glow=0.0)
    sled_riders(c, t, 0, BHS / 2, mood="scared", flying=True)
    c.restore()
    # motion trail
    for j in range(1, 6):
        tt = t - 0.05 * j
        if tt < T_F:
            break
        xx, yy, ss, _ = sled_f(tt)
        ellipse(c, xx, yy, 60 * ss * (1 - j / 6), 60 * ss * (1 - j / 6), (1, 1, 1), lw=2)
    word(c, t, "WHEEEE!", 720, 160, 90, GOLD, T_F, T_APEX + 0.1, -0.06)
    word(c, t, "?!", 700, 420, 90, (1, 1, 1), T_F + 0.3, T_APEX, 0.1)
    word(c, t, "AAAAAAAA!", 520, y - 260, 84, (1, 1, 1), T_FALLF, T_G, 0.04)


def cam_f(t):
    x, y, s, _ = sled_f(t)
    cy = lerp(700, 1200, ease(seg(t, T_APEX, T_G)))
    if t < T_APEX:
        cy = lerp(800, 650, ease(seg(t, T_F, T_APEX)))
    return lerp(560, x + 60, 0.5), cy, lerp(1.0, 1.15, ease(seg(t, T_F, T_G)))


# ================= G: into the fridge =================
JX = 985
DX = DISH


def g_sled(t):
    p = seg(t, T_G, T_FREEZE)
    y = lerp(-300, FLOOR - 330, 1 - (1 - p) ** 2.2)
    return JX - 170, y, 0.12 * math.sin(t * 3)


def scene_g(c, t):
    fridge6(c, 1.0, 1, lid=False)
    frost(c, t, 1.0)
    god_rays(c, 1.0)
    butter_rink(c, 1.0)
    jello(c, JX, FLOOR, 0.08 * math.sin(t * 8))
    # the Duck on Dill's throne: its one motion — it slowly turns its head up toward them
    q = ease(seg(t, T_DUCK, T_DUCK + 0.6))
    clean_duck(c, DX, FLOOR, tilt=lerp(-0.45, 0.35, q), gaze=lerp(-2.0, 2.0, q), frosty=0.4, s=1.2)
    wink_star(c, DX + 70, FLOOR - 290, 44, T_DUCK + 0.6, t, 0.7)
    # the sled falling in
    x, y, rot = g_sled(t)
    c.save(); rot_at(c, x, y, rot)
    block(c, x, y, 0.0, glow=0.2)
    sled_riders(c, t, x, y, mood="scared", flying=True)
    c.restore()
    # speed lines
    if t < T_FREEZE:
        rnd = random.Random(int(t * 12))
        for j in range(10):
            lx = x - 350 + rnd.random() * 700
            ly = y - 900 - rnd.random() * 600
            c.move_to(lx, ly); c.line_to(lx, ly + 260)
            c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(6); c.stroke()
    word(c, t, "squeak", DX - 60, FLOOR - 400, 44, GOLD, T_DUCK + 0.2, T_DUCK + 0.9, 0.1)
    word(c, t, "AAAAAA!", x, y - 1000, 90, (1, 1, 1), T_G, T_FREEZE, 0.04)


def cam_g(t):
    return keyed([(T_G, 700, 800, 1.1), (T_DUCK - 0.1, 690, 920, 1.22), (T_FREEZE, 690, 900, 1.25), (END_T, 700, 880, 1.3)], t)


# ---------------- frame ----------------
def frame(c, t):
    if t >= END_T:
        end_card(c, t, END_T); return
    random.seed(int(t * 30))
    if t < T_B:
        cx, cy, Z = cam_a(t)
    elif t < T_C:
        cx, cy, Z = cam_b(t)
    elif t < T_E:
        cx, cy, Z = cam_cd(t)
    elif t < T_F:
        cx, cy, Z = cam_e(t)
    elif t < T_G:
        cx, cy, Z = cam_f(t)
    else:
        cx, cy, Z = cam_g(t)
    c.save(); c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    if t < T_B:
        scene_a(c, t)
    elif t < T_C:
        scene_b(c, t, cx)
    elif t < T_E:
        scene_cd(c, t, cx, cy)
    elif t < T_F:
        scene_e(c, t, cx)
    elif t < T_G:
        scene_f(c, t)
    else:
        scene_g(c, t)
    c.restore()
    # gusts / flashes between scenes
    for tc in (T_B, T_C, T_E):
        if tc - 0.2 <= t < tc + 0.2:
            a = 1 - abs(t - tc) / 0.2
            c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, a); c.fill()
    for tc in (T_F, T_G):
        if tc - 0.25 <= t < tc + 0.2:
            a = 1 - abs(t - tc) / 0.25
            c.rectangle(0, 0, W, H); c.set_source_rgba(1, 0.97, 0.85, max(0, a)); c.fill()
    if T_POWER <= t < T_POWER + 0.12:
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 0.95, 0.6, 0.35); c.fill()
    for d in DUNS:
        if d <= t < d + 0.12:
            c.rectangle(0, 0, W, H); c.set_source_rgba(0.1, 0.4, 0.8, 0.14); c.fill()
    if t >= END_T - 0.4:
        x, y, _ = g_sled(t)
        iris(c, W / 2 + (x - cx) * Z, H / 2 + (y - 250 - cy) * Z, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))
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
