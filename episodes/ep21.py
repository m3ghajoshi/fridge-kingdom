"""FRIDGE KINGDOM — Episode 21: "Thaw". 40.0s, 1080x1920 @ 30fps.

Variant A (title card first): 2s "FRIDGE KINGDOM" title card, then the story.

Continues straight from Ep 20: the ice-block sled drops out of the light into the fridge and SPLOOSHes into the jello.
The block BOINGs off and lands with a CLONK on the top shelf (everyone glances up: ?). Dill is stuck head-first in the
jello, legs kicking; Crumb is flat on his back with Peep sitting on him; Chip lands on his feet... already sweating.
The door slams; it's dim. In the warm fridge Chip melts all the way into a puddle with two sad eyes. Crumb pulls off
his napkin scarf to mop him up and wring him back together: it's just water. Crumb cries (sad violin); Peep pats him.
Wilt pops up from the crisper drawer, sighs and pats Crumb with its floppy top... then a lightbulb: it looks up at
the ceiling vent, where freezing mist pours down into one cold spot on the bottom shelf. Crumb and Dill slide the
scarf under the puddle and carry it like a stretcher (hup, hup) to the cold spot and tip him in.
Mist swirls, CRACKLE: Chip refreezes into a cube, POP, with a tiny new bubble freckle (ding). YAAAY: Crumb hugs him,
Chip blushes and melts a little again (drip drip) and Crumb mops him; everyone laughs.
Dill marches to reclaim his butter throne: the Duck is sitting on it. He pushes (HNNNG): it doesn't budge. Glare.
Sigh. He plops down beside it. The Duck's one motion: it tilts its head toward him (squeak).
Up on the top shelf, in the dark, the ice block glows faintly. Drip... drip... drip. Silence.
Inside the ice, the frozen Duck's eyes blink. A crack zips across the ice. DUN DUN DUNNN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from animate import heart
from ep1 import (crown, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp, back_out, dark_overlay,
                 INK, GOLD, FLOOR, TOP, W, H, FPS, S)
from ep2 import end_card, jello
from ep6 import fridge6, wilt, drawer_front
from ep7 import god_rays, confetti, sq_rings
from ep9 import fat_peep, crumb_bitten
from ep10 import ceiling_vent, frost, VENT_X
from ep12 import word, hop
from ep13 import ceiling
from ep14 import clean_duck, crumb_tears
from ep15 import drop, CHIP_F, CHIP_L
from ep16 import keyed, butter_rink, plate, DISH
from ep17 import LETTUCE, LETTUCE_D, NAP_B, lightbulb
from ep18 import draw_dill, draw_crumb, draw_chip, rot_at, lie, CHS
from ep19 import flakes, icicle
from ep20 import block, sled_riders, BS, BWS, BHS

DUR = 40.0
T_START = 2.0
END_T = 38.5
DIM = 0.18
FAT = 1.5
ICE_B = hexc("#74C0FC")
ICE_D = hexc("#1971C2")
PINK = hexc("#FF6B9A")
PINK_L = hexc("#FF8FB3")
RED = (1, 0.35, 0.35)
DUCK_Y = hexc("#FFD43B")

# ---------------- places ----------------
JX = 985                 # jello (bottom shelf)
COLD_X = 760             # the cold spot under the vent's mist
WILT_X = 600             # Wilt, in the crisper drawer
CH0, CR0, DI0 = 860, 720, 1030
BLOCK_TOP = (880, TOP)   # where the ice block ends up (top shelf)

# ---------------- timing ----------------
T_SPLOOSH = 2.6
T_DSTUCK = 2.95
T_CRLAND = 3.45
T_PLAND = 3.55
T_CHLAND = 3.55
T_CLONK = 4.2
T_LOOKUP = 4.3
T_CRUP = 4.75
T_PHEAD = 4.9
T_DPOP = 4.95
T_DLAND = 5.35
T_DOOR = 5.75
T_SLUMP = 6.2
T_PUDDLE = 7.4
T_NO = 6.6
T_SCARF = 7.9
T_DAB = 8.3
T_WRING = 9.1
T_CRY = 9.8
T_WILT = 12.0
T_WLAND = 12.45
T_PAT = 12.9
T_BULB = 13.8
T_TILT = 14.1
T_LIFT = 15.8
T_MARCH = 16.1
T_ARRIVE = 17.5
T_TIP = 17.6
T_SPLASH = 17.85
T_BACK = 18.0
T_SWIRL = 18.4
T_GROW = 19.5
T_POP = 19.85
T_NEWF = 20.3
T_YAY = 21.2
T_HUG = 21.6
T_MELT2 = 22.3
T_MOP = 23.2
T_LAUGH = 23.6
T_E = 25.0
T_STOP = 26.2
T_PUSH = 26.6
T_GLARE = 27.8
T_SIGH = 28.5
T_SIT = 29.0
T_LEAN = 30.0
T_F = 31.0
DRIPS = (31.9, 32.6, 33.3, 34.0, 34.8, 35.6)
T_BLINK = 36.4
T_ICECRACK = 37.2
DUNS = (37.2, 37.6, 38.0)


def light_at(t):
    return lerp(1.0, DIM, ease(seg(t, T_DOOR, T_DOOR + 0.3)))


# ---------------- title card (variant A) ----------------
def title_card(c, t):
    g = cairo.RadialGradient(W / 2, 820, 50, W / 2, 820, 1300)
    g.add_color_stop_rgb(0, *hexc("#FFF4E6")); g.add_color_stop_rgb(0.4, *hexc("#A5D8FF")); g.add_color_stop_rgb(1, *hexc("#1C2541"))
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    for i, wd in enumerate(["FRIDGE", "KINGDOM"]):
        p = back_out(seg(t, 0.1 + i * 0.25, 0.55 + i * 0.25))
        c.save(); c.translate(W / 2, 640 + i * 170 + 8 * math.sin(t * 6 + i)); c.rotate(0.04 * (1 if i else -1))
        c.scale(S(p), S(p)); text(c, wd, 0, 0, 170, GOLD if i else (1, 1, 1), olw=22); c.restore()
    crown(c, W / 2 + 190, 500, 1.6 * back_out(seg(t, 0.6, 1.0)), 0.25)
    # drips running off KINGDOM (it's thawing)
    for i, x in enumerate((300, 450, 620, 770)):
        q = (t * 0.9 + i * 0.27) % 1
        if t > 0.7:
            drop(c, x, 900 + 160 * q * q, 1.3)
    q = ease_out(seg(t, 0.9, 1.3))
    if q > 0:
        c.save(); c.translate(W / 2, 1060 + (1 - q) * 50)
        text(c, "Episode 21:", 0, 0, 60, (1, 1, 1), olw=10)
        text(c, "Thaw", 0, 100, 110, hexc("#D0EBFF"), outline=INK, olw=14)
        c.restore()
    k = back_out(seg(t, 0.3, 0.8))
    c.save(); c.translate(W / 2, 1660); c.scale(S(0.62 * k), S(0.62 * k))
    draw_crumb(c, t, -260, 140, dict(mood="worried", look=(1, 0)))
    draw_dill(c, t, -40, 140, dict(mood="shocked", look=(1, 0)))
    fat_peep(c, 180, 140, FAT, mood="shock", face=0.3, look=(1, 0))
    draw_chip(c, t, 360, 140, dict(mood="eep", look=(-1, -1), melt=0.45, arms="out"))
    c.restore()


# ---------------- new props ----------------
def chip_puddle(c, x, y, t, rx=150, frosty=0.0, look=(0, -1), mood="sad", alpha=1.0, wave=0.0):
    """Chip, melted all the way into a puddle: two eyes floating on the water, his air-bubble freckle,
    and Wilt's lettuce cape lying soaked in it. frosty 0..1 freezes the surface white."""
    if rx < 2:
        return
    c.push_group()
    ry = max(6, rx * 0.2)
    ellipse(c, x, y, rx, ry, CHIP_F, lw=5)
    ellipse(c, x - rx * 0.25, y - ry * 0.35, rx * 0.35, ry * 0.25, (1, 1, 1), stroke=False)
    # the soggy lettuce cape
    c.save(); c.translate(x - rx * 0.6, y + ry * 0.1); c.rotate(-0.15)
    ellipse(c, 0, 0, 30 * rx / 150, 9 * rx / 150 + 2, LETTUCE, lw=3)
    c.restore()
    # air-bubble freckle
    ellipse(c, x + rx * 0.5, y - 2, 8, 8, (0.9, 0.97, 1.0), lw=3)
    if frosty > 0.01:
        ellipse(c, x, y, rx, ry, (1, 1, 1), stroke=False)
        c.set_source_rgba(0.95, 0.99, 1, 0)
        c.save(); c.translate(x, y); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(0.93, 0.98, 1.0, 0.9 * frosty); c.fill()
        rnd = random.Random(5)
        for j in range(int(9 * frosty) + 1):
            star(c, x + rnd.uniform(-0.8, 0.8) * rx, y + rnd.uniform(-0.5, 0.5) * ry, 10 + 6 * frosty, j, (1, 1, 1))
    # eyes, floating on the surface
    lx, ly = look
    sc = min(1.0, rx / 120)
    for ex in (-22, 22):
        ex *= sc
        ellipse(c, x + ex, y - 14 * sc, 14 * sc, 16 * sc, (1, 1, 1), lw=4)
        ellipse(c, x + ex + lx * 4 * sc, y - 13 * sc + ly * 4 * sc, 6 * sc, 7 * sc, INK, stroke=False)
        if mood == "sad":   # droopy lids
            c.save(); c.translate(x + ex, y - 14 * sc); c.scale(14 * sc, 16 * sc); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.save(); c.clip(); c.rectangle(x + ex - 16 * sc, y - 32 * sc, 32 * sc, 12 * sc); c.set_source_rgb(*CHIP_F); c.fill(); c.restore()
            c.set_source_rgb(*INK); c.set_line_width(3.5)
            c.move_to(x + ex - 14 * sc, y - 20 * sc); c.line_to(x + ex + 14 * sc, y - 20 * sc + (3 if ex < 0 else -3) * -1); c.stroke()
    # tiny wobbly mouth
    c.set_source_rgb(*INK); c.set_line_width(3.5)
    c.move_to(x - 10 * sc, y + 8 * sc)
    for i in range(1, 6):
        c.line_to(x - 10 * sc + i * 4 * sc, y + 8 * sc + (2.5 if i % 2 else -2) * sc)
    c.stroke()
    # a tiny wave of a drip-hand
    if wave > 0:
        c.move_to(x + rx * 0.75, y - 4); c.line_to(x + rx * 0.75 + 16, y - 26 - 10 * math.sin(t * 14))
        c.set_source_rgb(*INK); c.set_line_width(12); c.stroke()
        c.move_to(x + rx * 0.75, y - 4); c.line_to(x + rx * 0.75 + 16, y - 26 - 10 * math.sin(t * 14))
        c.set_source_rgb(*CHIP_F); c.set_line_width(6); c.stroke()
    c.pop_group_to_source(); c.paint_with_alpha(alpha)


def scarf_cloth(c, x, y, w=120, h=46, rot=0.0, wet=0.0, twist=0.0):
    """Crumb's blue-striped napkin scarf held in a hand (centre x, y)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(1 - 0.5 * twist, 1 + 0.6 * twist)
    rrect(c, -w / 2, -h / 2, w, h, 12); c.set_source_rgb(*[lerp(1, v, 0.5 * wet) for v in (0.75, 0.9, 1.0)]); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.save(); rrect(c, -w / 2, -h / 2, w, h, 12); c.clip()
    for k in range(-4, 5):
        c.move_to(k * 22 - 6 + 20 * twist, -h / 2); c.line_to(k * 22 + 6 - 20 * twist, h / 2)
        c.set_source_rgb(*NAP_B); c.set_line_width(7); c.stroke()
    c.restore(); c.restore()


def stretcher(c, xl, xr, y, t, tilt=0.0, slosh=0.0, with_chip=True):
    """The scarf held between two hands as a stretcher, sagging, with puddle-Chip sloshing inside."""
    c.save(); rot_at(c, (xl + xr) / 2, y, tilt)
    d = 70
    xm = (xl + xr) / 2
    if with_chip:
        chip_puddle(c, xm + 14 * slosh, y + d - 30, t, rx=(xr - xl) * 0.42, look=(math.sin(t * 3), -1), mood="worried")
    c.move_to(xl, y)
    c.curve_to(xl + 30, y + d, xr - 30, y + d, xr, y)
    c.line_to(xr, y + 26)
    c.curve_to(xr - 30, y + d + 30, xl + 30, y + d + 30, xl, y + 26)
    c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    for k in range(1, 7):
        f = k / 7
        xx = lerp(xl, xr, f)
        sag = d * 4 * f * (1 - f) * 0.75
        c.move_to(xx - 5, y + sag + 4); c.line_to(xx + 5, y + sag + 30)
        c.set_source_rgb(*NAP_B); c.set_line_width(7); c.stroke()
    c.restore()


def mist(c, t, k):
    """Freezing mist pouring from the ceiling vent down to one cold spot on the bottom shelf."""
    if k <= 0.01:
        return
    top_y = 140
    c.save()
    # the falling column
    c.move_to(VENT_X - 120, top_y)
    for i in range(11):
        s = i / 10
        c.line_to(lerp(VENT_X - 120, COLD_X - 150, s) + 16 * math.sin(t * 2.2 + s * 9), lerp(top_y, FLOOR, s))
    for i in range(10, -1, -1):
        s = i / 10
        c.line_to(lerp(VENT_X + 120, COLD_X + 150, s) + 16 * math.sin(t * 2.0 + s * 8 + 1), lerp(top_y, FLOOR, s))
    c.close_path()
    g = cairo.LinearGradient(0, top_y, 0, FLOOR)
    g.add_color_stop_rgba(0, 0.85, 0.95, 1, 0.38 * k); g.add_color_stop_rgba(1, 0.9, 0.97, 1, 0.22 * k)
    c.set_source(g); c.fill()
    # snow drifting down inside it
    for j in range(36):
        s = (t * 0.22 + j / 36) % 1
        off = ((j * 37) % 23) / 11.5 - 1
        x = lerp(VENT_X, COLD_X, s) + off * lerp(100, 130, s) + 14 * math.sin(t * 3 + j)
        y = lerp(top_y, FLOOR - 10, s)
        ellipse(c, x, y, 5 + (j % 3) * 2, 5 + (j % 3) * 2, (1, 1, 1), stroke=False)
        c.set_source_rgba(1, 1, 1, 0)
    # frosty patch on the shelf
    c.save(); c.translate(COLD_X, FLOOR + 6); c.scale(170, 20); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(0.9, 0.97, 1.0, min(1, 0.5 + 0.5 * k)); c.fill()
    for j in range(4):
        q = (t * 0.7 + j / 4) % 1
        star(c, COLD_X - 120 + 80 * j, FLOOR + 4, 12 * math.sin(math.pi * q) * min(1, k), j + t, (1, 1, 1))
    c.restore()


def swirl(c, t, x, y, k):
    """Mist swirling down around the cold spot (refreeze)."""
    if k <= 0.01:
        return
    for j in range(14):
        a = t * 5 + j * 2 * math.pi / 14
        r = lerp(220, 80, (t * 0.8 + j / 14) % 1)
        px, py = x + math.cos(a) * r, y - 90 + math.sin(a) * r * 0.45
        ellipse(c, px, py, 18 * k, 12 * k, (1, 1, 1), stroke=False)
        star(c, px, py - 20, 12 * k, a, (1, 1, 1))


def splats(c, t):
    """Jello droplets from the SPLOOSH: they fly out and stay stuck on the shelf."""
    if t < T_SPLOOSH:
        return
    rnd = random.Random(21)
    for j in range(12):
        a = math.pi * (1.05 + 0.9 * j / 11)
        v = rnd.uniform(500, 900)
        vx, vy = math.cos(a) * v * 0.9, math.sin(a) * v * 1.3
        land_x = JX + vx * 1.1
        q = t - T_SPLOOSH
        if q < 0.9:
            x = JX + vx * q / 0.9 * 1.1
            y = FLOOR - 160 + vy * q + 1300 * q * q
            y = min(y, FLOOR - 4) if q > 0.4 else y
            ellipse(c, x, y, 16, 13, PINK, lw=4)
        else:
            ellipse(c, land_x, FLOOR - 2, 24, 7, PINK, lw=3)


def jello_glob(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-40, 0); c.curve_to(-46, -40, -10, -52, 0, -40); c.curve_to(14, -56, 46, -36, 40, 0)
    c.curve_to(30, 10, 28, 26, 20, 22); c.curve_to(14, 18, 10, 8, 0, 6); c.curve_to(-20, 8, -30, 8, -40, 0)
    c.set_source_rgba(*PINK, 0.92); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    ellipse(c, -14, -26, 8, 5, (1, 1, 1), stroke=False)
    c.restore()


def block21(c, t, x, y, s=BS, rot=0.0, glow=0.0, blink=0.0, crack=0.0, wet=0.0):
    """The ice block with the frozen Duck (from Ep 20) + its eyelids blinking + a crack."""
    block(c, x, y, rot, s, glow)
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if blink > 0.01:
        for ex in (-17.25, 26.45):
            ey = -244.8
            rx_, ry_ = 13 * 1.15, 15 * 1.15
            c.save(); c.translate(ex, ey); c.scale(rx_, ry_); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.save(); c.clip()
            c.rectangle(ex - rx_, ey - ry_, 2 * rx_, 2 * ry_ * blink); c.set_source_rgb(0.93, 0.86, 0.45); c.fill()
            c.restore()
            c.move_to(ex - rx_, ey - ry_ + 2 * ry_ * blink); c.line_to(ex + rx_, ey - ry_ + 2 * ry_ * blink)
            c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    if wet > 0:   # meltwater running down the sides
        for j, dx in enumerate((-150, -40, 90, 165)):
            q = (t * 0.6 + j * 0.31) % 1
            yy = lerp(-380, -10, q)
            c.move_to(dx, yy - 22); c.curve_to(dx - 9, yy, dx - 8, yy + 9, dx, yy + 9)
            c.curve_to(dx + 8, yy + 9, dx + 9, yy, dx, yy - 22)
            c.set_source_rgba(*ICE_B, 0.9 * wet); c.fill()
    if crack > 0.01:
        pts = [(-190, -300), (-120, -270), (-90, -310), (-20, -280), (30, -330), (90, -290), (140, -320), (190, -280)]
        n = crack * (len(pts) - 1)
        c.move_to(*pts[0])
        for i in range(1, len(pts)):
            if i <= n:
                c.line_to(*pts[i])
            else:
                f = n - (i - 1)
                if f > 0:
                    c.line_to(lerp(pts[i - 1][0], pts[i][0], f), lerp(pts[i - 1][1], pts[i][1], f))
                break
        c.set_source_rgb(1, 1, 1); c.set_line_width(9); c.stroke_preserve()
        c.set_source_rgb(*ICE_D); c.set_line_width(4); c.stroke()
    c.restore()


# ---------------- states ----------------
def sled_pos(t):
    """Bottom-centre of the falling block before the SPLOOSH."""
    p = seg(t, T_START, T_SPLOOSH)
    return lerp(860, 900, p), lerp(600, FLOOR - 150, p ** 1.6)


def block_pos(t):
    """(x, y bottom, rot, squash) of the ice block after the SPLOOSH."""
    if t < T_SPLOOSH:
        x, y = sled_pos(t)
        return x, y, 0.12 * math.sin(t * 3), 1.0
    if t < T_CLONK:
        p = seg(t, T_SPLOOSH + 0.05, T_CLONK)
        x, y = hop((900, FLOOR - 150), BLOCK_TOP, p, 1600)
        return x, y, 5.0 * p * 2 * math.pi / 5 * 2, 1.0
    q = t - T_CLONK
    return BLOCK_TOP[0], BLOCK_TOP[1], 0.0, 1 - 0.18 * math.exp(-q * 8) * math.cos(q * 30)


def crumb_state(t):
    """x, y, rot, lie_k, kw, scarf_on."""
    kw = dict(mood="worried", look=(1, 0.5))
    scarf_on = t < T_SCARF
    if t < T_CRLAND:
        p = seg(t, T_SPLOOSH, T_CRLAND)
        x, y = hop((975, FLOOR - 150 - BHS), (CR0, FLOOR), p, 260)
        return x, y, 3.0 * p, 0.0, dict(mood="scared", look=(-1, -1), arm="wave"), True
    if t < T_CRUP:
        return CR0, FLOOR, 0.0, 1.0, dict(mood="dizzy"), True
    if t < T_CRUP + 0.3:
        k = 1 - back_out(seg(t, T_CRUP, T_CRUP + 0.3))
        return CR0, FLOOR, 0.0, k, dict(mood="dizzy"), True
    if t < T_LIFT:
        x = CR0
        rot = 0.0
        if t < T_SLUMP:
            kw = dict(mood="worried", look=(1, 0.6) if t > T_LOOKUP + 0.6 else (0, -1))
            if T_LOOKUP <= t < T_LOOKUP + 0.6:
                kw["look"] = (1, -1)
        elif t < T_SCARF:
            kw = dict(mood="scared", look=(1, 0.8), arm="wave" if t > T_NO else "down")
            rot = 0.1
        elif t < T_CRY:
            kw = dict(mood="worried", look=(1, 1), arm="none")
            rot = 0.18 + 0.12 * ease(seg(t, T_DAB, T_DAB + 0.3)) * (1 - ease(seg(t, T_WRING - 0.1, T_WRING + 0.2)))
        else:
            kw = dict(mood="worried", look=(0, 1) if t < T_PAT else (-1, 0.5), arm="none")
            rot = 0.08
            if T_BULB <= t:
                kw["look"] = (-1, -1)
        return x, FLOOR, rot, 0.0, kw, scarf_on
    if t < T_TIP + 0.3:
        cx_ = carry_c(t)
        x = cx_ - 230
        if t < T_MARCH:
            x = lerp(CR0, CH0 - 230, ease(seg(t, T_LIFT - 0.3, T_LIFT)))
        return x, FLOOR - (abs(math.sin(t * 11)) * 12 if T_MARCH <= t < T_ARRIVE else 0), 0.0, 0.0, \
            dict(mood="worried", look=(1, 0.3), arm="none"), False
    if t < T_YAY:
        x = lerp(COLD_X - 230, 900, ease(seg(t, T_BACK, T_BACK + 0.4)))
        return x, FLOOR - (abs(math.sin(t * 11)) * 14 if T_BACK <= t < T_BACK + 0.4 else 0), 0.0, 0.0, \
            dict(mood="scared" if t < T_POP else "worried", look=(-1, 0.3), arm="none"), False
    if t < T_E:
        x = lerp(900, 865, ease(seg(t, T_YAY, T_HUG)))
        mood = "sheepish" if t < T_MOP else "happy"
        return x, FLOOR, 0.0, 0.0, dict(mood=mood, look=(-1, 0.3), arm="none"), False
    return 865, FLOOR, 0.0, 0.0, dict(mood="sheepish" if t < T_SIGH else "worried", look=(-1, 0), arm="down"), False


CARRY_A, CARRY_B = CH0, COLD_X


def carry_c(t):
    return lerp(CARRY_A, CARRY_B, ease(seg(t, T_MARCH, T_ARRIVE)))


def dill_state(t):
    """x, y, rot, kw, mode ('stuck' = head-first in the jello)."""
    if t < T_DSTUCK:
        p = seg(t, T_SPLOOSH, T_DSTUCK)
        x, y = hop((900 + BWS / 2 + 50, FLOOR - 150 - 40), (JX, FLOOR - 30), p, 150)
        return x, y, math.pi * p, dict(mood="shocked", look=(0, 1), arm="reach"), "fly"
    if t < T_DPOP:
        return JX, FLOOR - 330, math.pi, dict(mood="shocked", arm="flail", shake=3), "stuck"
    if t < T_DLAND:
        p = seg(t, T_DPOP, T_DLAND)
        x, y = hop((JX, FLOOR - 30), (DI0, FLOOR), p, 260)
        return x, y, math.pi * (1 - p) + 2 * math.pi * p, dict(mood="dizzy", arm="flail"), "fly"
    if t < T_LIFT - 0.3:
        mood = "dizzy" if t < T_DLAND + 0.6 else ("shocked" if t < T_CRY else "sad")
        look = (-1, 0.8)
        if T_LOOKUP <= t < T_LOOKUP + 0.6:
            look = (-1, -1)
        if t >= T_BULB:
            mood, look = "shocked", (-1, -1)
        return DI0, FLOOR, 0.0, dict(mood=mood, look=look), "stand"
    if t < T_TIP + 0.3:
        x = carry_c(t) + 260
        if t < T_MARCH:
            x = lerp(DI0, CH0 + 260, ease(seg(t, T_LIFT - 0.3, T_LIFT)))
        y = FLOOR - (abs(math.sin(t * 11 + 1.5)) * 12 if T_MARCH <= t < T_ARRIVE else 0)
        return x, y, 0.0, dict(mood="angry", look=(-1, 0.3), arm="point_l"), "stand"
    if t < T_E:
        x = lerp(COLD_X + 260, 1010, ease(seg(t, T_BACK, T_BACK + 0.4)))
        mood, arm = "shocked", "down"
        if t >= T_YAY:
            mood, arm = "proud", "up"
        if t >= T_LAUNGH_END():
            mood, arm = "smug", "down"
        return x, FLOOR, 0.0, dict(mood=mood, look=(-1, 0.3), arm=arm), "stand"
    # E: the throne
    if t < T_STOP:
        x = lerp(1010, 590, ease(seg(t, T_E, T_STOP)))
        return x, FLOOR - abs(math.sin(t * 10)) * 18, 0.0, dict(mood="proud", look=(-1, 0), arm="up"), "stand"
    if t < T_PUSH:
        return 590, FLOOR, 0.0, dict(mood="shocked", look=(-1, 0), arm="up"), "stand"
    if t < T_GLARE:
        return 590 - 12 * ease(seg(t, T_PUSH, T_PUSH + 0.2)), FLOOR, -0.32, dict(mood="angry", look=(-1, 0), arm="point_l", shake=4), "stand"
    if t < T_SIGH:
        return 590, FLOOR, 0.0, dict(mood="angry", look=(-1, 0), arm="cross", shake=2), "stand"
    if t < T_SIT:
        return 590, FLOOR, 0.0, dict(mood="sad", look=(-1, 0.5)), "stand"
    mood, look = "sad", (-1, 0.5)
    if t >= T_LEAN + 0.4:
        mood, look = "sheepish", (-1, -0.5)
    return 590, FLOOR, 0.0, dict(mood=mood, look=look), "sit"


def T_LAUNGH_END():
    return T_MOP


def chip_state(t):
    """mode, x, y, extra.  modes: sled / fly / stand / slump / puddle / carry / freeze / cube"""
    if t < T_SPLOOSH:
        return "sled", 0, 0, {}
    if t < T_CHLAND:
        p = seg(t, T_SPLOOSH, T_CHLAND)
        x, y = hop((815, FLOOR - 150 - BHS), (CH0, FLOOR), p, 300)
        return "fly", x, y, dict(rot=-2 * math.pi * p)
    if t < T_SLUMP:
        m = lerp(0.25, 0.5, seg(t, T_CHLAND, T_SLUMP))
        mood = "eep" if t < T_CHLAND + 0.6 else "shy"
        look = (-1, -1) if T_LOOKUP <= t < T_LOOKUP + 0.6 else (-1, 0)
        return "stand", CH0, FLOOR, dict(melt=m, mood=mood, look=look)
    if t < T_PUDDLE:
        return "slump", CH0, FLOOR, dict(k=ease(seg(t, T_SLUMP, T_PUDDLE)))
    if t < T_LIFT:
        return "puddle", CH0, FLOOR, {}
    if t < T_TIP:
        return "carry", 0, 0, {}
    if t < T_GROW:
        return "freeze", COLD_X, FLOOR, dict(fr=ease(seg(t, T_SWIRL, T_GROW)))
    if t < T_POP:
        return "grow", COLD_X, FLOOR, dict(k=back_out(seg(t, T_GROW, T_POP)))
    return "cube", COLD_X, FLOOR, {}


def peep_pos(t):
    """Peep's feet + kw. Before T_PHEAD it moves on its own; after, it rides on Crumb's head."""
    if t < T_SPLOOSH:
        return None
    if t < T_PLAND:
        p = seg(t, T_SPLOOSH, T_PLAND)
        x, y = hop((975, FLOOR - 150 - BHS - 296), (CR0 + 129, FLOOR - 160), p, 380)
        return x, y, dict(mood="shock", wings="flap", rot=4 * math.pi * p)
    if t < T_PHEAD:
        return CR0 + 129, FLOOR - 160, dict(mood="blink", wings="down", look=(0, -1))
    if t < T_PHEAD + 0.35:
        x, y = hop((CR0 + 129, FLOOR - 160), (CR0, FLOOR - 296), seg(t, T_PHEAD, T_PHEAD + 0.35), 160)
        return x, y, dict(mood="happy", wings="flap")
    return "head"


def peep_head_kw(t):
    if t < T_SLUMP:
        return dict(mood="happy", look=(1, 0.5))
    if t < T_CRY:
        return dict(mood="shock", look=(1, 1))
    if t < T_BULB:
        return dict(mood="blink", wings="hug", look=(0, 1))
    if t < T_LIFT:
        return dict(mood="shock", look=(-1, -1))
    if t < T_TIP + 0.3:
        return dict(mood="proud", wings="salute", look=(-1, 0))
    if t < T_POP:
        return dict(mood="shock", look=(-1, 0.5))
    if t < T_E:
        return dict(mood="love", wings="hug" if T_HUG <= t < T_MOP else "flap", look=(-1, 0.5))
    if t < T_SIGH + 0.4:
        return dict(mood="happy", look=(-1, 0))
    return dict(mood="blink", look=(-1, 0))


def wilt_state(t):
    """(y feet, droop, pat, look, mirrored) — Wilt stands in the crisper drawer below the shelf."""
    if t < T_WILT:
        return None
    if t < T_WLAND:
        p = seg(t, T_WILT, T_WLAND)
        y = lerp(FLOOR + 520, FLOOR + 230, ease_out(p)) - 120 * math.sin(math.pi * p)
        return y, 0.0, 0.0, (1, -1)
    y = FLOOR + 230
    if t < T_PAT:
        return y, 0.2, 0.0, (1, -0.5)
    if t < T_BULB:
        p = seg(t, T_PAT, T_BULB - 0.2)
        return y, 0.75, abs(math.sin(p * 3 * math.pi)), (1, -1)
    if t < T_LIFT:
        return y - 30 * ease_out(seg(t, T_BULB, T_BULB + 0.2)), 0.0, 0.0, (0, -1)
    # job done: it sinks back down into the crisper drawer
    yy = lerp(y - 30, FLOOR + 600, ease(seg(t, T_LIFT, T_LIFT + 0.5)))
    if yy > FLOOR + 590:
        return None
    return yy, 0.0, 0.0, (0, -1)


def duck_pose(t):
    """The Duck on Dill's throne: still looking up-right from Ep 20; its one motion: it tilts toward Dill."""
    q = ease(seg(t, T_LEAN, T_LEAN + 0.6))
    return lerp(0.35, 0.8, q), lerp(2.0, 3.2, q)


# ---------------- camera ----------------
KEYS = [(T_START, 860, 900, 0.95), (T_SPLOOSH, 880, 1120, 1.12), (3.0, 700, 1000, 1.0), (T_CLONK, 700, 960, 1.0),
        (T_LOOKUP + 0.5, 760, 1050, 1.05), (T_DLAND, 860, 1200, 1.45), (T_SLUMP, 860, 1215, 1.65),
        (T_PUDDLE, 850, 1225, 1.7), (T_CRY, 830, 1215, 1.7), (T_WILT, 760, 1240, 1.6), (T_TILT, 740, 1230, 1.6),
        (T_TILT + 0.6, 640, 720, 0.95), (T_TILT + 1.1, 640, 760, 0.95), (T_LIFT, 870, 1200, 1.45), (T_MARCH, 875, 1200, 1.5),
        (T_ARRIVE, 780, 1200, 1.5), (T_SWIRL, 800, 1225, 1.65), (T_POP, 780, 1260, 1.75), (T_NEWF, 750, 1330, 2.4),
        (T_YAY - 0.1, 750, 1330, 2.4), (T_YAY + 0.2, 860, 1215, 1.65), (T_E, 860, 1215, 1.65), (T_STOP, 540, 1225, 1.7),
        (T_LEAN - 0.2, 520, 1235, 1.8), (T_F, 520, 1235, 1.8), (T_F + 0.9, 880, 560, 1.25), (T_BLINK - 0.2, 890, 505, 3.0),
        (END_T, 890, 505, 3.25)]


def camera(t):
    cx, cy, z = keyed(KEYS, t)
    for (t0, q0, d) in ((T_SPLOOSH, 16, 0.35), (T_CLONK, 10, 0.25), (T_DOOR, 6, 0.2), (T_POP, 8, 0.2), (T_SPLASH, 5, 0.2)):
        if t0 <= t < t0 + d:
            q = q0 * (1 - seg(t, t0, t0 + d)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    return cx, cy, z


# ---------------- the scene ----------------
def crumb_arms(c, t, x, y, rot, mode, cloth=None):
    """Arms drawn by the episode for Crumb (arm='none'): mopping, wringing, holding, hugging."""
    c.save(); rot_at(c, x, y, rot)
    c.set_source_rgb(*INK); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND)
    if mode == "rest":
        c.move_to(x - 70, y - 120); c.line_to(x - 100, y - 70); c.move_to(x + 70, y - 120); c.line_to(x + 100, y - 70); c.stroke()
    elif mode == "hold":    # both hands to the stretcher's left end
        c.move_to(x - 70, y - 120); c.line_to(x + 60, y - 160); c.move_to(x + 70, y - 120); c.line_to(x + 110, y - 165); c.stroke()
    elif mode == "hug":     # around Chip (to his left)
        c.move_to(x - 70, y - 130); c.line_to(x - 175, y - 120); c.move_to(x - 70, y - 90); c.line_to(x - 170, y - 70); c.stroke()
    elif mode == "cloth" and cloth is not None:
        hx, hy = cloth
        c.move_to(x + 70, y - 120); c.line_to(hx, hy); c.move_to(x - 70, y - 120); c.line_to(x - 100, y - 70); c.stroke()
    elif mode == "wring" and cloth is not None:
        hx, hy = cloth
        c.move_to(x + 70, y - 120); c.line_to(hx + 40, hy); c.move_to(x - 70, y - 120); c.line_to(hx - 40, hy); c.stroke()
    elif mode == "wipe" and cloth is not None:
        hx, hy = cloth
        c.move_to(x - 70, y - 120); c.line_to(hx, hy); c.move_to(x + 70, y - 120); c.line_to(x + 100, y - 70); c.stroke()
    c.restore()


def cloth_pos(t, x):
    """Where the scarf is while Crumb mops / wrings (world coords)."""
    if t < T_DAB:
        p = ease(seg(t, T_SCARF, T_SCARF + 0.3))
        return lerp(x, x + 100, p), lerp(FLOOR - 80, FLOOR - 160, p), 0.0, 0.0
    if t < T_WRING:
        k = abs(math.sin((t - T_DAB) / (T_WRING - T_DAB) * 2 * math.pi))
        return lerp(x + 110, CH0 - 10, k), lerp(FLOOR - 150, FLOOR - 20, k), 0.3 * k, min(1, (t - T_DAB) * 2)
    if t < T_CRY + 0.4:
        p = ease(seg(t, T_WRING, T_WRING + 0.2))
        return lerp(CH0 - 10, CH0 - 60, p), lerp(FLOOR - 20, FLOOR - 230, p), 1.4, 1.0
    return x + 105, FLOOR - 70, 1.4, 1.0


def scene(c, t):
    L = light_at(t)
    fridge6(c, L, 1, lid=False)
    frost(c, t, 1.0)
    ceiling(c, L)
    ceiling_vent(c, L)
    god_rays(c, L)
    # bottom shelf set
    butter_rink(c, 1.0)
    splats(c, t)
    wob = 0.0
    if t >= T_SPLOOSH:
        q = t - T_SPLOOSH
        wob = 2.2 * math.exp(-q * 3.2) * math.cos(q * 22)
    if T_DSTUCK <= t < T_DPOP:
        wob += 0.12 * math.sin(t * 25)
    if T_DPOP <= t < T_DPOP + 0.6:
        q = t - T_DPOP
        wob += 1.0 * math.exp(-q * 5) * math.cos(q * 25)
    jello(c, JX, FLOOR, wob)
    ty, gz = duck_pose(t)
    clean_duck(c, DISH, FLOOR, tilt=ty, gaze=gz, frosty=0.4, s=1.2)
    if T_LEAN + 0.4 <= t < T_LEAN + 1.4:
        heart(c, DISH + 120, FLOOR - 330 - 60 * seg(t, T_LEAN + 0.4, T_LEAN + 1.4), 1.4, 1 - seg(t, T_LEAN + 0.4, T_LEAN + 1.4))

    # the cold mist from the vent (behind everyone)
    mk = 0.35 + 0.65 * ease(seg(t, T_TILT, T_TILT + 0.5)) * (1 - 0.6 * ease(seg(t, T_E, T_E + 0.6)))
    mk += 0.5 * ease(seg(t, T_SWIRL, T_SWIRL + 0.3)) * (1 - ease(seg(t, T_POP, T_POP + 0.4)))
    mist(c, t, mk)

    # Wilt in the crisper drawer (behind the frosted drawer front)
    ws = wilt_state(t)
    if ws is not None:
        wy, droop, pat, look = ws
        c.save(); c.translate(WILT_X, wy); c.scale(-1.25, 1.25); c.translate(-WILT_X, -wy)
        wilt(c, WILT_X, wy, droop=droop, pat=pat, look=(-look[0], look[1]))
        c.restore()
    drawer_front(c)

    # Chip (on the shelf; when carried he's drawn with the stretcher)
    mode, chx, chy, ex = chip_state(t)
    if mode == "fly":
        c.save(); rot_at(c, chx, chy - 80, ex["rot"])
        draw_chip(c, t, chx, chy, dict(mood="eep", look=(0, -1), arms="up", melt=0.25))
        c.restore()
    elif mode == "stand":
        draw_chip(c, t, chx, chy, dict(mood=ex["mood"], look=ex["look"], arms="out" if ex["mood"] == "eep" else "down",
                                      melt=ex["melt"], blush=0.0))
        for j in range(2):   # sweat
            q = ((t - T_CHLAND) * 1.6 + j * 0.5) % 1
            drop(c, chx - 60 + 120 * j, chy - 190 + 40 * q, 0.9)
    elif mode == "slump":
        k = ex["k"]
        chip_puddle(c, chx, chy, t, rx=lerp(40, 150, k), look=(0, -1), alpha=min(1, k * 2.5))
        c.save(); c.translate(chx, chy); c.scale(1 + 0.5 * k, S(1 - 0.92 * k)); c.translate(-chx, -chy)
        c.push_group()
        draw_chip(c, t, chx, chy, dict(mood="eep", look=(0, -1), arms="out", melt=0.5))
        c.pop_group_to_source(); c.paint_with_alpha(1 - 0.85 * k)
        c.restore()
    elif mode == "puddle":
        lk = (-1, -0.3) if t < T_CRY else (-1, -1)
        if t >= T_BULB:
            lk = (-1, -1)
        chip_puddle(c, chx, chy, t, rx=150, look=lk, wave=1.0 if T_PUDDLE + 0.3 <= t < T_PUDDLE + 1.3 else 0.0)
    elif mode == "freeze":
        rx = 150
        if t < T_SPLASH:
            rx = lerp(60, 150, ease_out(seg(t, T_TIP, T_SPLASH)))
        chip_puddle(c, chx, chy, t, rx=rx, frosty=ex["fr"], look=(0, -1), mood="sad" if ex["fr"] < 0.5 else "worried")
    elif mode == "grow":
        k = ex["k"]
        chip_puddle(c, chx, chy, t, rx=lerp(150, 1, min(1, k)), frosty=1.0, alpha=max(0.0, 1 - k))
        c.save(); c.translate(chx, chy); c.scale(S(lerp(1.6, 1.0, min(k, 1))), S(k)); c.translate(-chx, -chy)
        draw_chip(c, t, chx, chy, dict(mood="happy", arms="down"))
        c.restore()
    elif mode == "cube":
        melt = 0.0
        if t >= T_MELT2:
            melt = 0.2 * ease(seg(t, T_MELT2, T_MELT2 + 0.5)) * (1 - ease(seg(t, T_MOP + 0.8, T_MOP + 1.2)))
        if t < T_NEWF:
            kw = dict(mood="happy", arms="up" if t > T_POP + 0.1 else "down")
        elif t < T_YAY:
            kw = dict(mood="shy", look=(-0.5, 1), arms="draw_l")
        elif t < T_MELT2:
            kw = dict(mood="happy", arms="up")
        elif t < T_MOP:
            kw = dict(mood="shy", look=(1, 0), arms="down", blush=1.0)
        elif t < T_E:
            kw = dict(mood="giggle", arms="down", blush=0.6)
        else:
            kw = dict(mood="shy", look=(-1, 0), arms="down")
        draw_chip(c, t, chx, chy, dict(kw, melt=melt))
        # the tiny new bubble freckle
        sx, sy = 1 + 0.18 * melt, 1 - 0.55 * melt
        fx, fy = chx - 30 * CHS * sx, chy - 26 * CHS * sy
        ellipse(c, fx, fy, 5 * CHS, 5 * CHS, (0.9, 0.97, 1.0), lw=2.5)
        ellipse(c, fx - 1.5, fy - 2, 1.6, 1.6, (1, 1, 1), stroke=False)
        if T_NEWF <= t < T_NEWF + 0.8:
            q = seg(t, T_NEWF, T_NEWF + 0.8)
            star(c, fx - 18, fy - 14, 26 * math.sin(math.pi * q), q * 3, (1, 1, 1))
            c.save(); c.translate(fx, fy); c.arc(0, 0, 18 + 30 * q, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(1, 0.9, 0.4, 0.9 * (1 - q)); c.set_line_width(4); c.stroke()
        if melt > 0.05:
            for j in range(2):
                q = ((t - T_MELT2) * 1.5 + j * 0.5) % 1
                drop(c, chx - 70 + 140 * j, chy - 20 + 30 * q, 0.8)

    # Crumb (+ Peep on his head)
    crx, cry, crot, lk, ckw, scarf_on = crumb_state(t)
    on_sled = t < T_SPLOOSH
    c.save()
    if on_sled:
        c.rectangle(0, 0, 0, 0); c.clip()
    if lk > 0:
        lie(c, crx, cry, lk, 1, 70)
    else:
        rot_at(c, crx, cry, crot)
    if scarf_on:
        draw_crumb(c, t, crx, cry, ckw)
    else:
        crumb_bitten(c, crx, cry, 1.0, **ckw)
    if T_CRY <= t < T_LIFT:
        crumb_tears(c, crx, cry - 160, t, 1.0 if t < T_BULB else max(0.0, 1 - 2 * (t - T_BULB)))
    pp = peep_pos(t)
    if pp == "head":
        pkw = peep_head_kw(t)
        fat_peep(c, crx, cry - 296, FAT, mood=pkw["mood"], wings=pkw.get("wings", "down"), look=pkw.get("look", (0, 0)),
                 flap_t=t, face=-0.5)
    c.restore()
    # Crumb's arms / scarf
    if ckw.get("arm") == "none" and not on_sled:
        if T_SCARF <= t < T_LIFT - 0.3:
            hx, hy, rr, wet = cloth_pos(t, crx)
            wringing = T_WRING <= t < T_CRY + 0.4
            crumb_arms(c, t, crx, cry, 0.0, "wring" if wringing else "cloth", (hx, hy))
            scarf_cloth(c, hx, hy, rot=rr, wet=wet, twist=math.sin((t - T_WRING) * 12) * 0.3 if wringing else 0.0)
            if wringing:
                for j in range(4):
                    q = ((t - T_WRING) * 2.2 + j / 4) % 1
                    drop(c, hx - 15 + 10 * j, hy + 40 + 180 * q, 0.9)
        elif T_LIFT - 0.3 <= t < T_TIP + 0.3:
            crumb_arms(c, t, crx, cry, 0.0, "hold")
        elif T_HUG <= t < T_MOP:
            crumb_arms(c, t, crx, cry, 0.0, "hug")
        elif T_MOP <= t < T_E:
            q = math.sin((t - T_MOP) * 9)
            hx, hy = COLD_X + 60, FLOOR - 90 + 30 * q
            crumb_arms(c, t, crx, cry, 0.0, "wipe", (hx, hy))
            scarf_cloth(c, hx, hy, w=80, h=60, rot=1.4, wet=0.5)
        else:
            crumb_arms(c, t, crx, cry, 0.0, "rest")
            if not scarf_on and t >= T_BACK:
                scarf_cloth(c, crx + 105, FLOOR - 70, w=70, h=40, rot=1.4, wet=0.6)

    # the stretcher
    if T_LIFT - 0.3 <= t < T_TIP + 0.3:
        xl, xr = crx + 110, dill_state(t)[0] - 140
        lift = ease(seg(t, T_LIFT - 0.3, T_LIFT))
        y = lerp(FLOOR - 20, FLOOR - 165, lift)
        tilt = -0.5 * ease(seg(t, T_TIP, T_TIP + 0.2))
        slosh = math.sin(t * 9) if T_MARCH <= t < T_ARRIVE else 0.0
        stretcher(c, xl, xr, y, t, tilt=tilt, slosh=slosh, with_chip=t < T_TIP + 0.1)
        if T_TIP + 0.05 <= t < T_SPLASH:   # pouring
            q = seg(t, T_TIP + 0.05, T_SPLASH)
            for j in range(5):
                ellipse(c, xl + 30 + 10 * j, lerp(y + 40, FLOOR - 10, (q + j * 0.15) % 1), 16, 22, CHIP_F, lw=3)
        if lift < 1 and t < T_LIFT:
            pass
    # Peep flying on its own (before it reaches Crumb's head)
    if pp is not None and pp != "head":
        px, py, pkw = pp
        fat_peep(c, px, py, FAT, mood=pkw["mood"], wings=pkw["wings"], look=pkw.get("look", (0, 0)), flap_t=t,
                 rot=pkw.get("rot", 0.0))

    # Dill
    dx, dy, drot, dkw, dmode = dill_state(t)
    if on_sled:
        pass
    elif dmode == "stuck":
        c.save(); c.translate(dx, dy); c.rotate(math.pi)
        draw_dill(c, t, 0, 0, dkw)
        c.restore()
        # jello over his head
        c.push_group(); jello(c, JX, FLOOR, wob); c.pop_group_to_source(); c.paint_with_alpha(0.75)
    else:
        c.save()
        if dmode == "sit":
            sq = lerp(1.0, 0.8, back_out(seg(t, T_SIT, T_SIT + 0.25)))
            c.translate(dx, dy); c.scale(1 / sq ** 0.4, sq); c.translate(-dx, -dy)
        if dmode == "fly":
            rot_at(c, dx, dy - 150, drot)
        else:
            rot_at(c, dx, dy, drot)
        draw_dill(c, t, dx, dy, dkw)
        if t >= T_DPOP:
            jello_glob(c, dx + 6, dy - 300, 1.1)
        c.restore()

    # Peep in the jello? (no: Peep lands on Crumb) — words / effects
    if t >= T_YAY and t < T_E:
        confetti(c, t, T_YAY, COLD_X + 40, FLOOR - 450, n=50)
    if T_HUG <= t < T_MOP:
        for j in range(3):
            q = ((t - T_HUG) * 0.8 + j / 3) % 1
            heart(c, COLD_X + 40 + 60 * j, FLOOR - 260 - 160 * q, 1.4, 1 - q)
    sq_rings(c, JX, FLOOR - 140, t, T_SPLOOSH, 0.9, PINK_L)
    sq_rings(c, COLD_X, FLOOR - 80, t, T_POP, 0.8, (0.85, 0.95, 1.0))
    if ws is not None and t >= T_BULB:
        lightbulb(c, WILT_X, FLOOR - 160, 1.1 * back_out(seg(t, T_BULB, T_BULB + 0.25)) * (1 - seg(t, T_LIFT - 0.4, T_LIFT - 0.1)))

    dark_overlay(c, L)
    swirl(c, t, COLD_X, FLOOR, ease(seg(t, T_SWIRL, T_SWIRL + 0.3)) * (1 - ease(seg(t, T_GROW, T_POP))))

    # the ice block (glows faintly)
    if t < T_SPLOOSH:
        bx, by = sled_pos(t)
        brot = 0.12 * math.sin(t * 3)
        c.save(); rot_at(c, bx, by, brot)
        block21(c, t, bx, by, glow=0.2)
        sled_riders(c, t, bx, by, mood="scared", flying=True)
        c.restore()
    else:
        bx, by, brot, bsq = block_pos(t)
        c.save(); c.translate(bx, by); c.scale(1 / S(bsq) ** 0.5, bsq); c.translate(-bx, -by)
        blink = 0.0
        if T_BLINK <= t < T_BLINK + 0.4:
            q = seg(t, T_BLINK, T_BLINK + 0.4)
            blink = ease(min(1, q / 0.4)) if q < 0.4 else 1 - ease((q - 0.4) / 0.6)
        if t < T_CLONK:
            rot_at(c, bx, by - BHS / 2, brot)
        block21(c, t, bx, by, glow=0.45 if t > T_CLONK else 0.1, blink=blink,
                crack=ease_out(seg(t, T_ICECRACK, T_ICECRACK + 0.35)), wet=1.0 if t > T_CLONK + 1 else 0.0)
        c.restore()
        if t >= T_CLONK:
            # meltwater puddle on the top shelf + drips off its front edge
            ellipse(c, bx + 40, TOP + 2, 200, 12, (0.72, 0.88, 1.0), lw=3)
            drip_ts = [T_CLONK + 2.0 + 1.6 * k for k in range(5)] + list(DRIPS)
            for d0 in drip_ts:
                q = t - d0
                if 0 <= q < 0.9:
                    drop(c, bx + 150, TOP + 40 + 900 * q * q, 1.6 if d0 in DRIPS else 1.0)
                    if d0 in DRIPS and q < 0.12:
                        ellipse(c, bx + 150, TOP + 38, 12, 16, ICE_B, lw=3)
        if T_BLINK + 0.3 <= t < T_BLINK + 0.9:
            q = seg(t, T_BLINK + 0.3, T_BLINK + 0.9)
            star(c, bx + 26.45 * BS + 20, by - 244.8 * BS - 22, 22 * math.sin(math.pi * q), q * 3, (1, 1, 1))

    # words
    word(c, t, "SPLOOSH!", JX - 120, FLOOR - 520, 110, PINK_L, T_SPLOOSH, T_SPLOOSH + 0.8, -0.08)
    word(c, t, "BOING!", 860, FLOOR - 820, 80, (1, 1, 1), T_SPLOOSH + 0.05, T_SPLOOSH + 0.6, 0.1)
    word(c, t, "CLONK!", BLOCK_TOP[0], TOP - 430, 90, (1, 1, 1), T_CLONK, T_CLONK + 0.6, -0.06)
    word(c, t, "?", 700, FLOOR - 470, 110, (1, 1, 1), T_LOOKUP + 0.1, T_LOOKUP + 0.7, 0.1)
    word(c, t, "SHLORP!", JX, FLOOR - 470, 80, PINK_L, T_DPOP, T_DPOP + 0.6, 0.06)
    word(c, t, "THUD", 540, 900, 80, (1, 1, 1), T_DOOR, T_DOOR + 0.5, -0.05)
    word(c, t, "drip...", CH0 + 30, FLOOR - 330, 54, ICE_B, T_SLUMP + 0.2, T_PUDDLE, 0.08)
    word(c, t, "eep...", CH0 + 140, FLOOR - 120, 46, (1, 1, 1), T_PUDDLE + 0.3, T_PUDDLE + 1.3, -0.1)
    word(c, t, "NOOO!", CR0 - 40, FLOOR - 400, 80, (1, 1, 1), T_NO, T_NO + 0.8, -0.06)
    word(c, t, "dab dab", CH0 - 60, FLOOR - 320, 54, (1, 1, 1), T_DAB + 0.1, T_WRING, 0.06)
    word(c, t, "sniff...", CR0 - 40, FLOOR - 470, 56, (1, 1, 1), T_CRY + 0.5, T_CRY + 1.6, -0.08)
    word(c, t, "sigh...", WILT_X - 120, FLOOR - 40, 52, (1, 1, 1), T_WLAND + 0.1, T_PAT, 0.06)
    word(c, t, "pat pat", WILT_X + 100, FLOOR - 230, 52, (1, 1, 1), T_PAT + 0.1, T_BULB - 0.1, -0.06)
    word(c, t, "!", WILT_X - 120, FLOOR - 220, 110, GOLD, T_BULB, T_BULB + 0.6, 0.1)
    word(c, t, "ooooh...", 820, 520, 64, (1, 1, 1), T_TILT + 0.6, T_TILT + 1.3, -0.05)
    word(c, t, "HUP!", 820, FLOOR - 470, 80, GOLD, T_LIFT, T_LIFT + 0.5, -0.08)
    word(c, t, "hup  hup  hup", 780, FLOOR - 520, 56, (1, 1, 1), T_MARCH + 0.1, T_ARRIVE, 0.04)
    word(c, t, "SPLOSH", COLD_X - 60, FLOOR - 250, 64, CHIP_F, T_SPLASH, T_SPLASH + 0.5, 0.08)
    word(c, t, "CRACKLE", COLD_X, FLOOR - 380, 74, (1, 1, 1), T_SWIRL + 0.5, T_GROW, -0.05)
    word(c, t, "POP!", COLD_X + 40, FLOOR - 330, 92, GOLD, T_POP, T_POP + 0.5, 0.08)
    word(c, t, "ding!", COLD_X - 150, FLOOR - 220, 40, GOLD, T_NEWF + 0.1, T_NEWF + 0.8, -0.1)
    word(c, t, "YAAAAY!", COLD_X + 60, FLOOR - 620, 100, GOLD, T_YAY, T_HUG + 0.6, -0.05)
    word(c, t, "drip drip", COLD_X - 40, FLOOR - 360, 52, ICE_B, T_MELT2 + 0.3, T_MOP, 0.06)
    word(c, t, "ha ha ha!", 900, FLOOR - 620, 66, (1, 1, 1), T_LAUGH, T_E - 0.2, 0.05)
    word(c, t, "HMPH!", 900, FLOOR - 560, 74, (1, 1, 1), T_E + 0.1, T_E + 0.8, -0.06)
    word(c, t, "!!", 640, FLOOR - 520, 96, RED, T_STOP, T_PUSH, 0.08)
    word(c, t, "HNNNG!", 600, FLOOR - 470, 74, (1, 1, 1), T_PUSH + 0.1, T_GLARE, -0.06)
    word(c, t, "sigh...", 660, FLOOR - 430, 60, (1, 1, 1), T_SIGH + 0.1, T_SIT + 0.5, 0.06)
    word(c, t, "plop", 660, FLOOR - 120, 50, (1, 1, 1), T_SIT + 0.05, T_SIT + 0.5, -0.06)
    word(c, t, "squeak", DISH + 10, FLOOR - 400, 48, GOLD, T_LEAN + 0.1, T_LEAN + 0.8, 0.08)
    for d in DRIPS:
        word(c, t, "drip", BLOCK_TOP[0] + 230, TOP + 120, 44, ICE_B, d + 0.15, d + 0.6, 0.06)


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
    if T_DOOR <= t < T_DOOR + 0.1:
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.35); c.fill()
    if T_POP <= t < T_POP + 0.1:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.85, 0.95, 1, 0.35); c.fill()
    if T_BLINK <= t < T_BLINK + 0.08:
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.2); c.fill()
    for d in DUNS:
        if d <= t < d + 0.12:
            c.rectangle(0, 0, W, H); c.set_source_rgba(0.1, 0.4, 0.8, 0.14); c.fill()
    if t >= END_T - 0.4:
        bx, by = BLOCK_TOP
        ex, ey = bx + 4.6 * BS, by - 244.8 * BS
        iris(c, W / 2 + (ex - cx) * Z, H / 2 + (ey - cy) * Z, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))


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
