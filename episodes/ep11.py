"""FRIDGE KINGDOM — Episode 11: "Wilt's Secret". 40.3s, 1080x1920 @ 30fps.

Variant A (title card first).

On the frosty bottom shelf, crownless Dill shows off a heroic leap off his fresh-butter throne. Peep copies
it, way bigger, flips, teeters on the front edge... and falls into the crisper drawer (SHHHK). Crumb and
Dill dive in after it. Wilt is already cradling Peep under its floppy top. Dill spots the old doodle on the
drawer wall and demands: WHO DID THIS?! Wilt sheepishly raises a twig scratcher. Then Wilt pulls back a
lettuce curtain: a whole secret mural of the fridge's history (the Hand, the Jar, the Duck, a snowflake with
eyes). The scratched Duck turns its head to the camera. Peep copies Wilt and pecks its own drawing: Crumb
with a heart. Crumb melts. Wilt points its twig way up: the last drawing, high above, a crowned shadow with
icicles looming over a fridge. Its eyes glint. Everyone shivers. Plip: a drop of meltwater lands on Dill's
head. He looks up. DUN DUN DUNNN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crown, dark_overlay, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp,
                 back_out, INK, GOLD, FLOOR, TOP, W, H, FPS, S)
from ep2 import end_card, jello
from ep5 import JELLO_X, cap_crown
from ep6 import grandma, fridge6, lid_piece, drawer_front, doodle, TEAR
from ep8 import shell_half, peep
from ep9 import fat_peep, crumb_bitten, GRAN_HEAD
from ep10 import ceiling_vent, frost, fresh_butter, napkin_folded
from animate import heart

DUR = 40.3
END_T = 38.8
DIM = 0.18
FAT = 1.5
GSC = 1.35
EGG_X = 900
DISH_X = 420
GR_X = 250
FL = 1550                # crisper-drawer floor
SCR = (0.92, 0.97, 1.0)  # scratched-line colour
WALL = hexc("#22403D")
PALE, PALE_D, BROWN = hexc("#C5D86D"), hexc("#94A84A"), hexc("#A08445")
TWIG = hexc("#8D5A2B")

# ---------------- timing ----------------
T_DLEAP = 2.35       # Dill's heroic leap
T_DLAND = 3.0
T_PCROUCH = 3.6
T_PLEAP = 3.85       # Peep copies it
T_PLAND = 4.55       # lands on the very front edge
T_PFALL = 5.0
T_SHK = 5.45         # SHHHK into the drawer
T_CDIVE = 5.75
T_DDIVE = 6.0
T_CUT = 6.3          # cut into the drawer
T_CLAND = 6.7
T_DIL_LAND = 7.0
T_NOTICE = 9.0       # Dill notices the doodle
T_POINT = 9.8
T_WHO = 11.0         # "?!" to the group
T_TWIG = 12.2        # Wilt raises the twig
T_WALK = 14.4
T_PULL = 15.7        # curtain starts opening
T_OPEN = 17.2
T_HL = (17.5, 18.5, 19.5)   # hand, jar, snowflake highlights
T_DUCK = 20.8        # mural Duck turns its head
T_PEEP_GO = 23.4
T_SCRATCH = (24.4, 27.0)
T_PROUD = 27.2
T_MELT = 27.9
T_POINTUP = 30.0
T_GLINT = 31.9
T_DOWN = 33.6
T_PFFT = 35.0
T_DRIP = 35.9
T_PLIP = 36.45
DUNS = (36.75, 37.25, 37.75)

# drawer positions
D_X = 1100        # Dill in front of the mural
C_X = 1250
P_X = 1390
CUR_L0, CUR_L1, CUR_R = 1140, 1860, 1990   # lettuce curtain edges
TIP = 157         # Wilt's top-tip reach to the right (angle -0.2)


# ---------------- Wilt (with a controllable top + twig) ----------------
def wilt11(c, x, y, ang=0.5, look=(-1, 0), twig=False, blush=0.0, shake=0.0, sq=1.0, mood="sad"):
    """Wilt from ep6, but the floppy top's angle is set directly (0.5 = resting, -1.57 = straight up,
    -3.47 = hanging over to the left), and it can hold a twig scratcher at the tip."""
    c.save(); c.translate(x + shake * random.uniform(-1, 1), y); c.scale(1 / S(sq) ** 0.5, S(sq))
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_source_rgb(*INK); c.set_line_width(7)
    c.move_to(-10, -16); c.line_to(-14, 0); c.move_to(10, -16); c.line_to(14, 0); c.stroke()
    ellipse(c, -20, -2, 12, 6, INK, stroke=False); ellipse(c, 20, -2, 12, 6, INK, stroke=False)
    c.move_to(0, -16)
    for i in range(9):
        a = math.pi * (0.5 + i / 8.0)
        r = 78 + 10 * (i % 2)
        c.line_to(r * math.cos(a) * 0.9, -150 + r * math.sin(a) * 1.7 * 0.6)
    c.curve_to(-30, -240, 30, -240, 70, -170)
    for i in range(9):
        a = math.pi * (-0.1 + i / 8.0 * 0.6)
        r = 78 + 10 * (i % 2)
        c.line_to(r * math.cos(a) * 0.9, -150 + r * math.sin(a) * 0.8 + 50 * i / 8)
    c.close_path()
    c.set_source_rgb(*PALE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.set_source_rgb(*hexc("#F1F3C2")); c.set_line_width(10); c.move_to(0, -20); c.curve_to(0, -100, -4, -170, -10, -230); c.stroke()
    c.set_source_rgb(*PALE_D); c.set_line_width(3)
    for vy in (-60, -100, -140, -180):
        c.move_to(-2, vy); c.line_to(-46, vy - 22); c.move_to(2, vy); c.line_to(46, vy - 22); c.stroke()
    # floppy top
    c.save(); c.translate(-10, -226); c.rotate(ang)
    c.move_to(0, -30)
    c.curve_to(60, -46, 130, -36, 170, 0)
    c.curve_to(150, 14, 160, 26, 140, 30); c.curve_to(120, 44, 100, 30, 80, 42); c.curve_to(50, 46, 30, 30, 0, 30)
    c.close_path(); c.set_source_rgb(*PALE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.set_source_rgb(*BROWN); c.set_line_width(5); c.move_to(150, 4); c.curve_to(158, 14, 150, 22, 140, 26); c.stroke()
    c.set_source_rgb(*hexc("#F1F3C2")); c.set_line_width(6); c.move_to(0, 0); c.curve_to(60, -8, 110, -6, 160, 2); c.stroke()
    if twig:   # a little twig scratcher held at the tip
        c.save(); c.translate(150, 6)
        for lw, col in ((15, INK), (8, TWIG)):
            c.set_source_rgb(*col); c.set_line_width(lw)
            c.move_to(0, 0); c.line_to(110, -6); c.move_to(62, -4); c.line_to(86, -30); c.stroke()
        c.set_source_rgb(*SCR); c.set_line_width(4); c.move_to(108, -6); c.line_to(118, -7); c.stroke()
        c.restore()
    c.restore()
    c.set_source_rgb(*BROWN); c.set_line_width(5)
    c.move_to(-70, -120); c.curve_to(-76, -100, -70, -80, -62, -64); c.stroke()
    c.move_to(68, -110); c.curve_to(74, -92, 70, -76, 60, -60); c.stroke()
    # eyes
    lx, ly = look
    wide = mood == "shock"
    for ex in (-22, 22):
        ellipse(c, ex, -150, 14 * (1.2 if wide else 1), 15 * (1.2 if wide else 1), (1, 1, 1), lw=4)
        ellipse(c, ex + lx * 5, -146 + ly * 4, 6, 6, INK, stroke=False)
        if not wide:
            c.save(); c.translate(ex, -150); c.scale(14, 15); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.save(); c.clip(); c.rectangle(ex - 16, -168, 32, 16); c.set_source_rgb(*PALE_D); c.fill(); c.restore()
            c.set_source_rgb(*INK); c.set_line_width(4); c.move_to(ex - 14, -152); c.line_to(ex + 14, -152); c.stroke()
    if blush > 0:
        for ex in (-40, 40):
            c.save(); c.translate(ex, -120); c.scale(16, 9); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(1, 0.45, 0.6, 0.75 * blush); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(4)
    if mood == "shy":       # small wobbly smile
        c.move_to(-12, -114); c.curve_to(-4, -106, 4, -106, 12, -114); c.stroke()
    elif mood == "shock":
        ellipse(c, 0, -110, 9, 11, INK, stroke=False)
    else:
        c.move_to(-14, -112); c.curve_to(-6, -122, 6, -122, 14, -112); c.stroke()
    c.restore()


def wilt_tip(x, y, ang):
    """World position of the twig's point."""
    ox, oy = x - 10, y - 226
    lx, ly = 150 + 118, 6 - 7
    return ox + lx * math.cos(ang) - ly * math.sin(ang), oy + lx * math.sin(ang) + ly * math.cos(ang)


# ---------------- drawer set ----------------
def drawer_bg(c, t):
    g = cairo.LinearGradient(0, -700, 0, 1900)
    g.add_color_stop_rgb(0, *hexc("#152B29")); g.add_color_stop_rgb(0.45, *hexc("#24423F")); g.add_color_stop_rgb(1, *hexc("#122523"))
    c.rectangle(-600, -1200, 3200, 3400); c.set_source(g); c.fill()
    c.set_source_rgba(1, 1, 1, 0.05); c.set_line_width(26)
    for i in range(-6, 30):
        x = i * 90 + 20
        c.move_to(x, -900); c.line_to(x, 1550); c.stroke()
    rg = cairo.RadialGradient(640, 280, 40, 640, 280, 1100)
    rg.add_color_stop_rgba(0, 0.75, 0.95, 1.0, 0.30); rg.add_color_stop_rgba(1, 0.75, 0.95, 1.0, 0.0)
    c.rectangle(-600, -1200, 3200, 3400); c.set_source(rg); c.fill()
    doodle(c, 0.5, t)
    c.rectangle(-600, FL, 3200, 700); c.set_source_rgb(*hexc("#1B3532")); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(6); c.move_to(-600, FL); c.line_to(2600, FL); c.stroke()
    ellipse(c, 120, FL + 10, 70, 14, hexc("#2F4F2A"), lw=4)
    c.save(); c.translate(2080, FL); c.rotate(-0.3)
    c.move_to(-12, 0); c.line_to(12, 0); c.line_to(4, -70); c.line_to(-4, -70); c.close_path()
    c.set_source_rgb(*hexc("#B85C1E")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    c.restore()


def sline(c, pts, w=8, a=0.85, col=SCR):
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.set_source_rgba(*col, a); c.set_line_width(w); c.stroke()


def scircle(c, x, y, rx, ry, w=8, a=0.85, fill=None):
    c.save(); c.translate(x, y); c.scale(rx, ry); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    if fill is not None:
        c.set_source_rgb(*fill); c.fill_preserve()
    c.set_source_rgba(*SCR, a); c.set_line_width(w); c.stroke()


def glow_at(c, x, y, r, k):
    if k <= 0:
        return
    rg = cairo.RadialGradient(x, y, 0, x, y, r)
    rg.add_color_stop_rgba(0, 1, 1, 0.85, 0.35 * k); rg.add_color_stop_rgba(1, 1, 1, 0.85, 0)
    c.rectangle(x - r, y - r, 2 * r, 2 * r); c.set_source(rg); c.fill()


def mural(c, t):
    """Wilt's secret wall of scratched drawings: the fridge's whole history."""
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    # sparkle-glow highlights as each drawing is noticed
    for (hx, hy), th in zip([(1310, 640), (1780, 740), (1820, 1110)], T_HL):
        glow_at(c, hx, hy, 230, math.sin(math.pi * seg(t, th, th + 0.9)))
    glow_at(c, 1530, 1030, 240, math.sin(math.pi * seg(t, T_DUCK - 0.2, T_DUCK + 1.0)))
    # tally marks: days and days in the drawer
    for g in range(4):
        bx = 1190 + g * 70
        for i in range(4):
            sline(c, [(bx + i * 12, 1150), (bx + i * 12 + 3, 1215)], 6, 0.7)
        sline(c, [(bx - 6, 1200), (bx + 50, 1162)], 6, 0.7)
    # 1. The Hand descending, light rays all around
    c.save(); c.translate(1310, 640)
    sline(c, [(-50, -170), (-56, 30)]); sline(c, [(50, -170), (56, 30)])
    sline(c, [(-56, 30), (-110, 60), (-112, 140)])
    for i, fx in enumerate((-80, -36, 8, 52)):
        sline(c, [(fx, 40 + 8 * (i in (1, 2))), (fx + 2, 170 + 10 * (i in (1, 2)))], 9)
        c.arc(fx + 16, 170 + 10 * (i in (1, 2)), 16, 0, math.pi); c.set_source_rgba(*SCR, 0.85); c.set_line_width(8); c.stroke()
    sline(c, [(56, 30), (100, 70), (96, 110)])
    for a in (-2.6, -2.2, -0.9, -0.5, 0.1, 3.0):
        sline(c, [(math.cos(a) * 170, 60 + math.sin(a) * 170), (math.cos(a) * 230, 60 + math.sin(a) * 230)], 6, 0.6)
    c.restore()
    # 2. The Jar with its five little pickles
    c.save(); c.translate(1780, 740)
    sline(c, [(-80, -110), (-80, 110), (80, 110), (80, -110)], 8)
    sline(c, [(-95, -110), (95, -110), (95, -150), (-95, -150), (-95, -110)], 8)
    for px, py in [(-40, -50), (20, -60), (-10, 10), (45, 20), (-45, 60)]:
        scircle(c, px, py, 18, 28, 6, 0.8)
        c.arc(px - 6, py - 8, 3.5, 0, 2 * math.pi); c.arc(px + 6, py - 8, 3.5, 0, 2 * math.pi)
        c.set_source_rgba(*SCR, 0.9); c.fill()
    c.restore()
    # 3. A snowflake with eyes (blinks)
    c.save(); c.translate(1820, 1110); c.rotate(0.1 * math.sin(t * 0.8))
    for j in range(6):
        a = j * math.pi / 3
        sline(c, [(math.cos(a) * 40, math.sin(a) * 40), (math.cos(a) * 110, math.sin(a) * 110)], 8)
        mx, my = math.cos(a) * 80, math.sin(a) * 80
        for d in (0.6, -0.6):
            sline(c, [(mx, my), (mx + math.cos(a + d) * 28, my + math.sin(a + d) * 28)], 6)
    scircle(c, 0, 0, 42, 42, 7, 0.85, fill=WALL)
    blink = 1.0
    th = T_HL[2] + 0.5
    if th <= t < th + 0.25 or 25.5 <= t < 25.7:
        blink = 0.15
    for ex in (-15, 15):
        c.save(); c.translate(ex, -4); c.scale(6, S(9 * blink)); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(*SCR, 0.95); c.fill()
    c.restore()
    # 4. The Duck (with its cap crown); turns its head to the camera
    turn = ease(seg(t, T_DUCK, T_DUCK + 0.35))
    c.save(); c.translate(1530, 1060)
    scircle(c, 0, 0, 100, 60, 8)
    sline(c, [(-86, -20), (-126, -54), (-92, 14)], 7)
    hx = lerp(34, 10, turn)
    scircle(c, hx, -86, 50, 48, 8, 0.85, fill=WALL)
    if turn < 0.5:
        sline(c, [(hx + 42, -88), (hx + 88, -76), (hx + 42, -64)], 7)
        c.arc(hx + 16, -100, 6, 0, 2 * math.pi); c.set_source_rgba(*SCR, 0.95); c.fill()
    else:
        sline(c, [(hx - 18, -66), (hx + 18, -66), (hx, -48), (hx - 18, -66)], 7)
        for ex in (-18, 18):
            c.arc(hx + ex, -98, 7, 0, 2 * math.pi); c.set_source_rgba(*SCR, 0.95); c.fill()
    sline(c, [(hx - 28, -128), (hx - 24, -156), (hx - 12, -140), (hx, -162), (hx + 12, -140), (hx + 24, -156), (hx + 28, -128)], 6)
    c.restore()


# Peep's own drawing: Crumb (toast) with a heart. Strokes revealed in order.
PEEP_DRAW_O = (1590, 1480)
PEEP_STROKES = [
    [(-55, 0), (-55, -95), (-78, -120), (-62, -158), (-20, -160), (0, -175), (24, -160), (62, -158), (78, -120), (55, -95), (55, 0), (-55, 0)],
    [(-24, -110), (-22, -96)], [(22, -112), (22, -98)],
    [(-22, -60), (0, -46), (22, -62)],
    [(105, -110), (85, -132), (100, -150), (118, -136), (136, -150), (150, -132), (130, -110), (118, -96), (105, -110)],
]


def peep_drawing(c, r):
    if r <= 0:
        return
    ox, oy = PEEP_DRAW_O
    total = sum(len(s) - 1 for s in PEEP_STROKES)
    n = r * total
    rnd = random.Random(5)
    c.save(); c.translate(ox, oy)
    for s in PEEP_STROKES:
        if n <= 0:
            break
        pts = [(x + rnd.uniform(-3, 3), y + rnd.uniform(-3, 3)) for x, y in s]
        k = min(len(pts) - 1, n)
        full = int(k)
        draw = pts[:full + 1]
        if k > full and full + 1 < len(pts):
            a, b = pts[full], pts[full + 1]
            draw.append((lerp(a[0], b[0], k - full), lerp(a[1], b[1], k - full)))
        if len(draw) >= 2:
            sline(c, draw, 7, 0.9, (1, 0.93, 0.6) if s is PEEP_STROKES[-1] else SCR)
        n -= len(s) - 1
    c.restore()


def ice_king(c, t):
    """High above the curtain: a crowned shadow with icicles, looming over a fridge."""
    c.save(); c.translate(1700, -40)
    # the fridge
    sline(c, [(-110, 0), (110, 0), (110, 300), (-110, 300), (-110, 0)], 8)
    sline(c, [(-110, 90), (110, 90)], 7)
    sline(c, [(80, 30), (80, 70)], 7); sline(c, [(80, 120), (80, 190)], 7)
    # the crowned shadow rising out of the top
    c.move_to(-150, 40)
    c.curve_to(-140, -60, -100, -120, -60, -140)
    c.line_to(-210, -170); c.line_to(-220, -150); c.line_to(-70, -110)    # left arm
    c.curve_to(-80, -170, -60, -220, 0, -225)
    c.curve_to(60, -220, 80, -170, 70, -110)
    c.line_to(220, -150); c.line_to(210, -170); c.line_to(60, -140)      # right arm
    c.curve_to(100, -120, 140, -60, 150, 40)
    c.close_path()
    c.set_source_rgb(*hexc("#0B1A22")); c.fill_preserve()
    c.set_source_rgba(*hexc("#A5D8FF"), 0.9); c.set_line_width(8); c.stroke()
    # spiky crown
    pts = [(-62, -205), (-70, -290), (-38, -240), (-20, -315), (0, -250), (20, -315), (38, -240), (70, -290), (62, -205)]
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path(); c.set_source_rgb(*hexc("#0B1A22")); c.fill_preserve()
    c.set_source_rgba(*hexc("#A5D8FF"), 0.9); c.set_line_width(7); c.stroke()
    # icicles hanging off the arms and crown rim
    for x0, y0, ln in [(-200, -158, 60), (-170, -150, 44), (-140, -142, 70), (-110, -134, 40),
                       (110, -134, 40), (140, -142, 70), (170, -150, 44), (200, -158, 60),
                       (-50, -205, 30), (-15, -205, 40), (20, -205, 34), (52, -205, 26)]:
        c.move_to(x0 - 9, y0); c.line_to(x0, y0 + ln); c.line_to(x0 + 9, y0); c.close_path()
        c.set_source_rgba(*hexc("#D0EBFF"), 0.9); c.fill()
    # eyes: dim, then glint
    g = 0.35 + 0.65 * ease(seg(t, T_GLINT, T_GLINT + 0.25))
    for ex, rot in ((-26, 0.35), (26, -0.35)):
        c.save(); c.translate(ex, -165); c.rotate(rot); c.scale(16, 7); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(0.75, 0.95, 1.0, g); c.fill()
    if t >= T_GLINT:
        for ex in (-26, 26):
            star(c, ex + 6, -170, 26 * math.sin(math.pi * seg(t, T_GLINT, T_GLINT + 0.6)), t * 3, (1, 1, 1))
    c.restore()


def curtain(c, o, sway=0.0):
    """Lettuce curtain on a twig rod; o 0 closed .. 1 bunched up at the right."""
    L = lerp(CUR_L0, CUR_L1, o)
    for lw, col in ((16, INK), (10, TWIG)):
        c.set_source_rgb(*col); c.set_line_width(lw)
        c.move_to(CUR_L0 - 40, 440); c.line_to(CUR_R + 30, 440); c.stroke()
    nf = 7
    wdt = (CUR_R - L) / nf
    for i in range(nf):
        x0 = L + i * wdt
        c.move_to(x0, 440)
        c.line_to(x0 + wdt, 440)
        c.curve_to(x0 + wdt + 10 + sway * 8, 800, x0 + wdt - 10, 1200, x0 + wdt + sway * 12, 1500)
        for k in range(4):
            c.line_to(x0 + wdt - (k + 0.5) * wdt / 4, 1500 + (16 if k % 2 == 0 else -6))
        c.line_to(x0 + sway * 12, 1500)
        c.curve_to(x0 - 10, 1200, x0 + 10 + sway * 8, 800, x0, 440)
        c.close_path()
        c.set_source_rgb(*(PALE if i % 2 == 0 else hexc("#B5CA5E"))); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        c.set_source_rgba(*hexc("#F1F3C2"), 0.8); c.set_line_width(5)
        c.move_to(x0 + wdt / 2, 460); c.curve_to(x0 + wdt / 2 + 8, 900, x0 + wdt / 2 - 8, 1200, x0 + wdt / 2, 1480); c.stroke()
        c.set_source_rgb(*BROWN); c.set_line_width(4)
        c.move_to(x0 + wdt * 0.2, 1490); c.line_to(x0 + wdt * 0.5, 1505); c.stroke()


# ---------------- title card (variant A) ----------------
def title_card(c, t):
    g = cairo.RadialGradient(W / 2, 820, 50, W / 2, 820, 1300)
    g.add_color_stop_rgb(0, *hexc("#E7F5FF")); g.add_color_stop_rgb(0.35, *hexc("#74C0FC")); g.add_color_stop_rgb(1, *hexc("#1C2541"))
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    for i, word in enumerate(["FRIDGE", "KINGDOM"]):
        p = back_out(seg(t, 0.1 + i * 0.25, 0.55 + i * 0.25))
        c.save(); c.translate(W / 2, 640 + i * 170 + 8 * math.sin(t * 6 + i)); c.rotate(0.04 * (1 if i else -1))
        c.scale(S(p), S(p)); text(c, word, 0, 0, 170, GOLD if i else (1, 1, 1), olw=22); c.restore()
    crown(c, W / 2 + 190, 500, 1.6 * back_out(seg(t, 0.6, 1.0)), 0.25)
    q = ease_out(seg(t, 0.9, 1.3))
    if q > 0:
        c.save(); c.translate(W / 2, 1000 + (1 - q) * 50)
        text(c, "Episode 11:", 0, 0, 60, (1, 1, 1), olw=10)
        text(c, "Wilt's Secret", 0, 90, 80, GOLD, olw=12)
        c.restore()
    dill(c, 250, 1700, "angry", look=(1, 0), arm="point", crown_on=False, shake=2)
    wilt11(c, 560, 1700, ang=lerp(0.5, -1.1, ease(seg(t, 0.8, 1.2))), look=(-1, 0.4), twig=True, blush=1.0, mood="shy")
    fat_peep(c, 860, 1700 - abs(math.sin(t * 7)) * 30, 1.3, mood="happy", face=-1, look=(-1, -0.3), wings="flap", flap_t=t)


# ---------------- shelf scene (2.0 – 6.3) ----------------
def shelf_dill(t):
    if t < T_DLEAP:
        return DISH_X, FLOOR - 110, dict(mood="proud", look=(1, 0), arm="down", sq=lerp(1.0, 0.82, seg(t, 2.0, T_DLEAP)))
    if t < T_DLAND:
        p = seg(t, T_DLEAP, T_DLAND)
        return lerp(DISH_X, 520, p), lerp(FLOOR - 110, FLOOR, p) - 260 * math.sin(math.pi * p), dict(mood="proud", look=(1, -0.5), arm="reach", rot=0.25 * math.sin(math.pi * p))
    if t < T_PLEAP:
        return 520, FLOOR, dict(mood="proud", look=(1, 0), arm="up", sq=lerp(0.85, 1.0, back_out(seg(t, T_DLAND, T_DLAND + 0.25))))
    if t < T_PFALL:
        return 520, FLOOR, dict(mood="frozen", look=(1, -0.6), arm="up")
    if t < T_DDIVE:
        p = ease(seg(t, T_PFALL + 0.3, T_DDIVE - 0.1))
        return lerp(520, 800, p), FLOOR - 30 * math.sin(math.pi * p * 3) * (p > 0), dict(mood="shocked", look=(1, 1), arm="reach")
    p = seg(t, T_DDIVE, T_CUT)
    return lerp(860, 940, p), FLOOR - 120 * math.sin(math.pi * min(1, p * 1.4)) + 500 * p * p, dict(mood="frozen", look=(0, 1), arm="reach", rot=0.6 * p)


def shelf_crumb(t):
    X = 680
    if t < T_PFALL:
        mood = "worried" if t < T_PLEAP else "scared"
        return X, FLOOR, dict(mood=mood, look=(1 if t > T_PCROUCH else -1, -0.3))
    if t < T_CDIVE:
        p = ease(seg(t, T_PFALL + 0.2, T_CDIVE))
        return lerp(X, 900, p), FLOOR, dict(mood="scared", look=(1, 1))
    p = seg(t, T_CDIVE, T_CUT)
    return lerp(900, 990, p), FLOOR - 140 * math.sin(math.pi * min(1, p * 1.5)) + 700 * p * p, dict(mood="scared", look=(0, 1), rot=0.5 * p)


def shelf_peep(t):
    X0 = 900
    if t < T_DLAND:
        return X0, FLOOR, dict(mood="happy", look=(-1, -0.3), face=-0.6), 0
    if t < T_PCROUCH:
        return X0, FLOOR, dict(mood="proud", face=-0.3), 0
    if t < T_PLEAP:
        return X0, FLOOR, dict(mood="proud", face=0.4, sq=lerp(1, 0.75, seg(t, T_PCROUCH, T_PLEAP))), 0
    if t < T_PLAND:
        p = seg(t, T_PLEAP, T_PLAND)
        return lerp(X0, 1000, p), FLOOR - 430 * math.sin(math.pi * p), dict(mood="happy", face=0.6, wings="flap", flap_t=t,
                                                                           rot=2 * math.pi * ease(p)), 0
    if t < T_PFALL:   # teetering on the front lip
        w = math.sin((t - T_PLAND) * 22)
        return 1000, FLOOR + 30, dict(mood="shock", face=0.5, wings="flap", flap_t=t, rot=0.3 * w), 1
    p = seg(t, T_PFALL, T_SHK)
    return lerp(1000, 920, p), FLOOR + 30 + 300 * p * p, dict(mood="shock", face=0, wings="flap", flap_t=t, rot=0.4 + 1.5 * p), 1


def shelf_scene(c, t):
    L = DIM
    sh = 10 * math.sin((t - T_SHK) * 40) * (1 - seg(t, T_SHK, T_SHK + 0.5)) if t >= T_SHK else 0
    fridge6(c, L, 0, lid=False, drawer_shake=sh)
    lid_piece(c, 760, TOP - 25, 0.0)
    shell_half(c, EGG_X, TOP - 70, 0.0, top=False)
    ceiling_vent(c, L)
    frost(c, t, 1.0)
    jello(c, JELLO_X, FLOOR, 0.0)
    c.save(); c.translate(730, FLOOR); c.scale(2.2, 0.8); napkin_folded(c, 0, 0); c.restore()
    fresh_butter(c, DISH_X, FLOOR)
    # Grandma (with Dill's crown) watching from the left
    c.save(); c.translate(GR_X, FLOOR); c.scale(GSC, GSC); c.translate(-GR_X, -FLOOR)
    grandma(c, GR_X, FLOOR, look=(1, -0.3), mood="stern")
    c.restore()
    crown(c, GR_X + GRAN_HEAD[0], FLOOR + GRAN_HEAD[1], 0.72, -0.2)
    px, py, pkw, falling = shelf_peep(t)
    if falling and t >= T_PFALL:
        fat_peep(c, px, py, FAT, **pkw)
    x, y, kw = shelf_crumb(t); crumb_bitten(c, x, y, 1.0, **kw)
    x, y, kw = shelf_dill(t); dill(c, x, y, crown_on=False, **kw)
    if not (falling and t >= T_PFALL):
        fat_peep(c, px, py, FAT, **pkw)
    drawer_front(c, sh)
    # effects
    word(c, t, "TA-DA!", 600, FLOOR - 470, 54, GOLD, T_DLAND, T_DLAND + 0.7, -0.08)
    if T_DLAND <= t < T_DLAND + 0.6:
        star(c, 470, FLOOR - 400, 26 * math.sin(math.pi * seg(t, T_DLAND, T_DLAND + 0.6)), t * 5, GOLD)
    word(c, t, "peep!", 900, FLOOR - 330, 40, hexc("#FFE680"), T_PCROUCH, T_PLEAP + 0.2, 0.1)
    word(c, t, "WHEEE!", 960, FLOOR - 600, 52, hexc("#FFE680"), T_PLEAP + 0.1, T_PLAND, 0.12)
    if T_PLAND <= t < T_PFALL:
        word(c, t, "!", 1000, FLOOR - 300, 90, (1, 0.35, 0.35), T_PLAND + 0.1, T_PFALL)
    word(c, t, "SHHHK!", 820, FLOOR + 260, 64, (1, 1, 1), T_SHK, T_SHK + 0.7, -0.08)
    word(c, t, "PEEP?!", 700, FLOOR - 470, 46, (1, 1, 1), T_SHK + 0.1, T_CUT, 0.08)
    dark_overlay(c, L)


# ---------------- drawer scene (6.3 – END) ----------------
def hop(a, b, p, height=200):
    return lerp(a[0], b[0], p), lerp(a[1], b[1], p) - height * math.sin(math.pi * p)


def walk(path, t, bounce=18, rate=3.0):
    """path: [(t, x)]; returns (x, y_lift, moving)."""
    if t <= path[0][0]:
        return path[0][1], 0.0, False
    for (ta, xa), (tb, xb) in zip(path, path[1:]):
        if t < tb:
            p = seg(t, ta, tb)
            if xa == xb:
                return xa, 0.0, False
            return lerp(xa, xb, ease(p) if (tb - ta) > 0.6 else p), abs(math.sin((t - ta) * rate * math.pi)) * bounce, True
    return path[-1][1], 0.0, False


def wilt_state(t):
    """(x, kwargs)"""
    path = [(0, 920), (T_WALK, 920), (T_PULL, 983), (T_OPEN, 1703), (22.4, 1703), (23.2, 1800)]
    x, lift, moving = walk(path, t, 10, 2.6)
    kw = dict(look=(-1, 0.3), mood="sad")
    if t < 8.0:          # top draped over Peep, patting
        kw["ang"] = -3.47 + 0.12 * math.sin(t * 9)
    elif t < 8.5:
        kw["ang"] = lerp(-3.47, 0.5, ease(seg(t, 8.0, 8.5)))
    elif t < T_TWIG:
        kw["ang"] = 0.5
        kw["look"] = (-1, 0) if t < T_WHO else (-1, -0.2)
        if t >= T_WHO + 0.4:
            kw["look"] = (-1, 0.6); kw["mood"] = "sad"
    elif t < T_WALK:     # sheepishly raises the twig
        kw["ang"] = lerp(0.5, -1.1, back_out(seg(t, T_TWIG, T_TWIG + 0.5))) + 0.05 * math.sin(t * 8)
        kw.update(twig=True, blush=ease(seg(t, T_TWIG, T_TWIG + 0.4)), mood="shy", look=(-0.6, 0.6))
    elif t < T_PULL:
        kw.update(ang=lerp(-1.1, -0.2, ease(seg(t, T_WALK, T_WALK + 0.5))), twig=True, blush=0.6, mood="shy", look=(1, 0))
    elif t < T_OPEN + 0.3:
        kw.update(ang=-0.2 + 0.05 * math.sin(t * 10), twig=True, blush=0.4, mood="shy", look=(1, -0.2))
    elif t < T_PEEP_GO:   # presents the mural
        kw.update(ang=lerp(-0.2, -1.2, ease(seg(t, T_OPEN + 0.3, T_OPEN + 0.8))), twig=True, blush=0.5, mood="shy", look=(-1, -0.5))
    elif t < T_POINTUP:
        kw.update(ang=-1.2 + 0.25 * math.sin((t - T_PEEP_GO) * 9) * (t < T_PEEP_GO + 1.0), twig=True, blush=0.3, mood="shy", look=(-1, 0.3))
    elif t < T_DOWN:     # points way up
        kw.update(ang=lerp(-1.2, -1.75, back_out(seg(t, T_POINTUP, T_POINTUP + 0.5))), twig=True, mood="shock", look=(-0.2, -1))
    else:                # shivers
        kw.update(ang=-1.4 + 0.08 * math.sin(t * 50), twig=True, mood="shock", look=(-1, -0.3),
                  shake=7 if t < T_PLIP else 3)
    kw["sq"] = 1.0 - lift / 200
    return x, kw


def peep_d(t):
    """Peep in the drawer: (x, y, kwargs)."""
    if t < 7.3:
        return 765, FL, dict(mood="blink" if int(t * 2) % 3 else "happy", face=0.6, look=(1, -0.5))
    if t < 8.6:
        return 765, FL, dict(mood="love", face=-0.6, wings="hug", flap_t=t)
    path = [(8.6, 765), (9.1, 720), (T_WALK + 0.8, 720), (T_OPEN + 0.2, P_X), (99, P_X)]
    x, lift, moving = walk(path, t, 26, 4.0)
    y = FL - lift
    if t < T_WHO:
        return x, y, dict(mood="happy", face=-0.6, look=(-1, -0.3))
    if t < T_TWIG + 0.4:
        return x, y, dict(mood="happy", face=-0.2, look=(-0.5, -0.5))
    if t < T_WALK + 0.8:
        return x, y, dict(mood="shock", face=0.5, look=(1, -0.5))
    if t < T_OPEN + 0.2:
        return x, y, dict(mood="happy", face=0.6, look=(1, -0.3))
    if t < T_PEEP_GO:
        return x, y, dict(mood="shock" if t < 21.0 else "happy", face=0.3, look=(0.5, -1))
    if t < T_SCRATCH[0]:
        return x, y, dict(mood="proud" if t < T_PEEP_GO + 0.5 else "happy", face=0.8, look=(1, 0))
    if t < T_SCRATCH[1]:   # pecking the wall
        pk = abs(math.sin((t - T_SCRATCH[0]) * 14))
        return x + 14 * pk, y, dict(mood="chirp" if pk > 0.6 else "happy", face=1.0, look=(1, 0), rot=0.2 * pk)
    if t < T_POINTUP:
        return x, y - abs(math.sin((t - T_PROUD) * 6)) * 14 * (t < T_PROUD + 1.2), dict(mood="proud", face=0.2, wings="salute")
    if t < T_DOWN:
        return x, y, dict(mood="shock", face=0.4, look=(0.6, -1))
    return x, y, dict(mood="shock", face=-0.3, look=(-0.6, -0.6), shake=4)


def crumb_d(t):
    """(x, y, kwargs, melt)"""
    if t < T_CLAND:
        p = seg(t, T_CUT, T_CLAND)
        return 560, lerp(700, FL, p * p), dict(mood="scared", look=(0, 1), rot=0.4 * (1 - p)), 0.0
    if t < 7.3:
        return 560, FL, dict(mood="scared", look=(1, 0)), 0.0
    path = [(7.3, 560), (7.9, 620), (8.6, 620), (9.1, 580), (T_WALK + 0.9, 580), (T_OPEN + 0.5, C_X), (99, C_X)]
    x, lift, moving = walk(path, t, 18, 3.4)
    y = FL - lift
    if t < 8.6:
        return x, y, dict(mood="sheepish", look=(1, 0), arm="wave"), 0.0
    if t < T_WHO:
        return x, y, dict(mood="worried", look=(-1, -0.3)), 0.0
    if t < T_TWIG + 0.4:
        return x, y, dict(mood="worried", look=(-1, 0), shake=2), 0.0
    if t < T_WALK + 0.9:
        return x, y, dict(mood="scared", look=(1, 0)), 0.0
    if t < T_PEEP_GO:
        return x, y, dict(mood="sheepish" if t > 18.0 else "worried", look=(0.5, -1)), 0.0
    if t < T_MELT:
        return x, y, dict(mood="worried", look=(1, 0)), 0.0
    if t < T_POINTUP:     # melts with love
        m = ease(seg(t, T_MELT, T_MELT + 0.8))
        return x, y, dict(mood="sheepish", look=(1, 0), arm="wave" if t < T_MELT + 0.6 else "down"), m
    m = 1 - ease(seg(t, T_POINTUP, T_POINTUP + 0.4))
    if t < T_DOWN:
        return x, y, dict(mood="scared", look=(1, -1)), m
    return x, y, dict(mood="scared", look=(-1, -0.6), shake=4), 0.0


def dill_d(t):
    """(x, y, kwargs)"""
    if t < T_CLAND:
        return None
    if t < T_DIL_LAND:
        p = seg(t, T_CLAND, T_DIL_LAND)
        return 420, lerp(600, FL, p * p), dict(mood="frozen", look=(0, 1), arm="reach", rot=-0.6 * (1 - p))
    if t < 8.4:   # face-plant squash, then pops up
        sq = lerp(0.6, 1.0, back_out(seg(t, 7.8, 8.2)))
        return 420, FL, dict(mood="frozen" if t < 7.8 else "angry", look=(1, 0), sq=sq)
    if t < T_NOTICE:
        return 420, FL, dict(mood="smug", look=(1, 0))
    if t < T_POINT:
        p = seg(t, T_NOTICE + 0.3, T_POINT)
        x = lerp(420, 360, ease(p))
        return x, FL - 20 * math.sin(math.pi * p), dict(mood="shocked", look=(-1, -0.6))
    if t < T_WHO:
        return 360, FL, dict(mood="angry", look=(-1, -0.5), arm="point_l", shake=3)
    if t < T_TWIG:
        return 360, FL - 16 * abs(math.sin((t - T_WHO) * 9)), dict(mood="angry", look=(1, 0), arm="pound", shake=2)
    if t < T_WALK + 1.2:
        return 360, FL, dict(mood="shocked", look=(1, -0.3))
    path = [(T_WALK + 1.2, 360), (T_OPEN + 0.6, D_X), (99, D_X)]
    x, lift, moving = walk(path, t, 22, 3.2)
    y = FL - lift
    if t < T_OPEN + 0.6:
        return x, y, dict(mood="smug", look=(1, -0.2))
    if t < T_PEEP_GO:
        return x, y, dict(mood="shocked" if t < 19.5 else "frozen", look=(0.6, -1))
    if t < T_MELT:
        return x, y, dict(mood="smug", look=(1, 0.2))
    if t < T_POINTUP:
        return x, y, dict(mood="smug", look=(1, 0))
    if t < T_DOWN:
        return x, y, dict(mood="frozen", look=(1, -1))
    if t < T_PFFT:
        return x, y, dict(mood="shocked", look=(1, -0.5), shake=5)
    if t < T_PLIP:      # pfft, it's just a drawing
        return x, y, dict(mood="smug", look=(-1, 0), arm="point")
    sq = lerp(0.8, 1.0, back_out(seg(t, T_PLIP, T_PLIP + 0.25)))
    return x, y, dict(mood="shocked", look=(0, -1), arm="reach" if t > T_PLIP + 0.5 else "down", sq=sq, shake=2 if t > DUNS[0] else 0)


def curtain_open(t):
    return ease(seg(t, T_PULL, T_OPEN))


def drawer_scene(c, t):
    drawer_bg(c, t)
    ice_king(c, t)
    mural(c, t)
    peep_drawing(c, seg(t, T_SCRATCH[0], T_SCRATCH[1]))
    o = curtain_open(t)
    curtain(c, o, sway=math.sin(t * 3) * (0.3 if o < 1 else 0.1))

    wx, wkw = wilt_state(t)
    px, py, pkw = peep_d(t)
    ds = dill_d(t)
    cx_, cy_, ckw, melt = crumb_d(t)
    if t < 8.0:   # cradled under Wilt's top
        fat_peep(c, px, py, FAT, **pkw)
        wilt11(c, wx, FL, **wkw)
    else:
        wilt11(c, wx, FL, **wkw)
    if t >= T_OPEN:
        fat_peep(c, px, py, FAT, **pkw)
    # Crumb (melting = squash)
    c.save(); c.translate(cx_, cy_); c.scale(1 + 0.14 * melt, S(1 - 0.22 * melt)); c.translate(-cx_, -cy_)
    crumb_bitten(c, cx_, cy_, 1.0, **ckw)
    c.restore()
    if 8.0 <= t < T_OPEN:
        fat_peep(c, px, py, FAT, **pkw)
    if ds:
        x, y, kw = ds
        dill(c, x, y, crown_on=False, **kw)

    # ---- effects ----
    word(c, t, "THUD", 470, FL - 380, 54, (1, 1, 1), T_DIL_LAND, T_DIL_LAND + 0.6, 0.1)
    if 6.8 <= t < 8.0:
        word(c, t, "sigh", 900, FL - 420, 34, (1, 1, 1), 6.9, 7.9, 0.08)
    if 7.3 <= t < 8.8:
        for j in range(3):
            q = ((t - 7.3) * 1.2 + j / 3) % 1
            heart(c, 700 + 40 * math.sin(j * 2 + q * 5), FL - 280 - q * 160, 1.2, 1 - q)
    if T_NOTICE <= t < T_POINT:
        k = back_out(seg(t, T_NOTICE, T_NOTICE + 0.15))
        c.save(); c.translate(430, FL - 420); c.scale(S(k), S(k)); text(c, "!", 0, 0, 100, GOLD, olw=12); c.restore()
    if T_POINT <= t < T_WHO:
        glow_at(c, 330, 860, 300, 0.6 * math.sin(math.pi * seg(t, T_POINT, T_WHO)))
    word(c, t, "?!", 370, FL - 440, 110, (1, 0.4, 0.4), T_POINT + 0.1, T_TWIG, 0.06)
    if T_TWIG + 0.3 <= t < T_WALK:     # everyone stares: !
        for xx, d in ((360, 0.0), (580, 0.1), (720, 0.2)):
            if t >= T_TWIG + 0.3 + d:
                k = back_out(seg(t, T_TWIG + 0.3 + d, T_TWIG + 0.45 + d))
                c.save(); c.translate(xx, FL - 400 + (60 if xx == 720 else 0)); c.scale(S(k), S(k)); text(c, "!", 0, 0, 70, (1, 1, 1), olw=10); c.restore()
        ttx, tty = wilt_tip(wx, FL, wkw["ang"])
        star(c, ttx, tty, 20 * abs(math.sin(t * 5)), t * 4, (1, 1, 1))
        word(c, t, "...hehe", 1010, FL - 470, 34, hexc("#C5D86D"), T_TWIG + 0.6, T_WALK, -0.06)
    if T_OPEN - 0.3 <= t < T_OPEN + 1.6:
        word(c, t, "ta-daa", 1700, FL - 470, 40, hexc("#C5D86D"), T_OPEN - 0.2, T_OPEN + 1.0, 0.06)
    if T_OPEN + 0.4 <= t < T_PEEP_GO - 0.4:
        word(c, t, "OOOOH", 1300, 1160, 58, (1, 1, 1), T_OPEN + 0.4, T_OPEN + 2.2, -0.05)
    for th in T_HL:
        if th <= t < th + 0.7:
            pos = {T_HL[0]: (1420, 520), T_HL[1]: (1890, 600), T_HL[2]: (1930, 1000)}[th]
            star(c, pos[0], pos[1], 30 * math.sin(math.pi * seg(t, th, th + 0.7)), t * 4, (1, 1, 1))
    if T_DUCK <= t < T_DUCK + 0.8:
        star(c, 1610, 950, 30 * math.sin(math.pi * seg(t, T_DUCK, T_DUCK + 0.8)), t * 4, GOLD)
        word(c, t, "?", 1660, 900, 70, hexc("#FFE680"), T_DUCK + 0.3, T_DUCK + 1.4, 0.1)
    if T_SCRATCH[0] <= t < T_SCRATCH[1]:
        word(c, t, "scritch", 1560, 1250, 38, (1, 1, 1), T_SCRATCH[0] + 0.1, T_SCRATCH[0] + 1.2, -0.08)
        word(c, t, "scratch", 1620, 1200, 38, (1, 1, 1), T_SCRATCH[0] + 1.3, T_SCRATCH[1], 0.08)
        q = (t * 3) % 1
        ellipse(c, 1500 + 20 * q, 1400 - 30 * q, 5, 5, SCR, stroke=False)
    if T_PROUD <= t < T_PROUD + 0.7:
        star(c, 1700, 1300, 26 * math.sin(math.pi * seg(t, T_PROUD, T_PROUD + 0.7)), t * 5, GOLD)
    if T_MELT <= t < T_POINTUP:
        for j in range(5):
            q = ((t - T_MELT) * 0.9 + j / 5) % 1
            heart(c, C_X - 60 + j * 30 + 25 * math.sin(q * 6 + j), FL - 300 - q * 260, 1.6, 1 - q)
        word(c, t, "awww", C_X, FL - 470, 46, hexc("#FF8FB3"), T_MELT + 0.2, T_POINTUP, -0.06)
        for sx in (-26, 26):   # happy tears
            q = ((t - T_MELT) * 1.4 + (0.5 if sx > 0 else 0)) % 1
            ellipse(c, C_X + sx * 1.1 + (-10 if sx < 0 else 10) * q, FL - 140 + q * 70, 7, 10, TEAR, lw=2)
    if T_POINTUP <= t < T_DOWN:   # dotted line from the twig to the drawing
        ttx, tty = wilt_tip(wx, FL, wkw["ang"])
        a = ease(seg(t, T_POINTUP + 0.3, T_POINTUP + 1.2))
        c.set_dash([18, 22]); c.set_source_rgba(1, 1, 1, 0.5 * a); c.set_line_width(6)
        c.move_to(ttx, tty); c.line_to(lerp(ttx, 1700, a), lerp(tty, 330, a)); c.stroke(); c.set_dash([])
    if T_DOWN + 0.3 <= t < T_PLIP:   # brrr
        for j, (bx, by) in enumerate([(D_X + 60, FL - 330), (C_X + 40, FL - 230), (P_X + 20, FL - 200), (1800 - 30, FL - 160)]):
            q = ((t * 1.3) + j / 4) % 1
            ellipse(c, bx + 40 * q, by - 30 * q, 14 + 14 * q, 10 + 8 * q, (0.9, 0.97, 1), stroke=False)
        word(c, t, "brrr", 1560, FL - 460, 44, hexc("#D0EBFF"), T_DOWN + 0.4, T_PFFT, -0.1)
    word(c, t, "pfft", D_X - 120, FL - 420, 40, (1, 1, 1), T_PFFT + 0.1, T_DRIP + 0.3, -0.1)
    # the drip
    if T_DRIP <= t < T_PLIP:
        p = seg(t, T_DRIP, T_PLIP)
        y = lerp(560, FL - 290, p * p)
        c.save(); c.translate(D_X + 20, y)
        c.move_to(0, -26); c.curve_to(14, -4, 16, 14, 0, 16); c.curve_to(-16, 14, -14, -4, 0, -26); c.close_path()
        c.set_source_rgb(*hexc("#A5D8FF")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        c.restore()
    if T_PLIP <= t < T_PLIP + 0.5:
        q = seg(t, T_PLIP, T_PLIP + 0.5)
        for i in range(7):
            a = -math.pi * (0.1 + 0.8 * i / 6)
            ellipse(c, D_X + 20 + math.cos(a) * 90 * q, FL - 290 + math.sin(a) * 70 * q + 120 * q * q, 7, 9, hexc("#A5D8FF"), lw=2)
    word(c, t, "plip", D_X + 140, FL - 380, 50, hexc("#A5D8FF"), T_PLIP, T_PLIP + 0.7, 0.1)
    if t >= T_PLIP + 0.3:   # more drips falling from above
        for j in range(3):
            q = ((t - T_PLIP) * 1.3 + j / 3) % 1
            ellipse(c, D_X - 160 + j * 170, 620 + q * 500, 7, 11, hexc("#A5D8FF"), lw=2)
    c.rectangle(-600, -1200, 3200, 3400); c.set_source_rgba(0.02, 0.06, 0.08, 0.10); c.fill()


def word(c, t, s, x, y, size, col, t0, t1, rot=0.0):
    if t0 <= t < t1:
        k = back_out(seg(t, t0, t0 + 0.2))
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(k), S(k)); text(c, s, 0, 0, size, col, olw=10); c.restore()


# ---------------- camera ----------------
SHELF_KEYS = [(2.0, 660, FLOOR - 280, 1.45), (T_PLEAP, 660, FLOOR - 280, 1.45), (T_PLAND, 760, FLOOR - 200, 1.45),
              (T_SHK, 760, FLOOR - 60, 1.4), (T_CUT, 780, FLOOR - 60, 1.4)]
DRAWER_KEYS = [(T_CUT, 600, 1230, 1.45), (8.6, 600, 1230, 1.45), (9.6, 430, 1170, 1.6), (T_WHO, 430, 1170, 1.6),
               (11.6, 600, 1230, 1.5), (T_TWIG, 600, 1230, 1.5), (12.8, 800, 1290, 1.9), (T_WALK, 800, 1290, 1.9),
               (T_PULL, 1000, 1150, 1.4), (T_OPEN, 1500, 1060, 1.15), (T_PEEP_GO, 1500, 1060, 1.2),
               (24.2, 1440, 1290, 1.72), (T_POINTUP + 0.4, 1440, 1290, 1.72), (31.2, 1700, -30, 1.75),
               (T_DOWN, 1700, -20, 1.95), (34.4, 1440, 1250, 1.4), (T_DRIP, 1440, 1250, 1.4),
               (T_PLIP + 0.1, 1120, 1320, 2.3), (END_T, 1120, 1300, 2.6)]


def keycam(keys, t):
    if t <= keys[0][0]:
        return keys[0][1:]
    for a, b in zip(keys, keys[1:]):
        if t < b[0]:
            p = ease(seg(t, a[0], b[0]))
            return tuple(lerp(a[i], b[i], p) for i in (1, 2, 3))
    return keys[-1][1:]


def camera(t):
    if t < T_CUT:
        cx, cy, z = keycam(SHELF_KEYS, t)
        if T_SHK <= t < T_SHK + 0.3:
            s = 14 * (1 - seg(t, T_SHK, T_SHK + 0.3)); cx += random.uniform(-s, s); cy += random.uniform(-s, s)
        return cx, cy, z
    cx, cy, z = keycam(DRAWER_KEYS, t)
    if T_DIL_LAND <= t < T_DIL_LAND + 0.25:
        cy += random.uniform(-10, 10)
    for d in DUNS:
        if d <= t < d + 0.12:
            z += 0.12 * (1 - seg(t, d, d + 0.12))
    return cx, cy, z


def frame(c, t):
    if t < 2.0:
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
    if t < T_CUT:
        shelf_scene(c, t)
    else:
        drawer_scene(c, t)
    c.restore()
    if t < 2.4:
        iris(c, W / 2, H / 2, lerp(0, 1400, ease(seg(t, 2.0, 2.4))))
    if T_CUT <= t < T_CUT + 0.15:
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.5 * (1 - seg(t, T_CUT, T_CUT + 0.15))); c.fill()
    if t >= T_GLINT and t < T_DOWN:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.3, 0.6, 1.0, 0.10 * ease(seg(t, T_GLINT, T_GLINT + 0.3))); c.fill()
    if t >= DUNS[0]:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.3, 0.6, 1.0, 0.12 * ease(seg(t, DUNS[0], DUNS[0] + 0.3))); c.fill()
    if t >= END_T - 0.4:
        cx, cy, Z = camera(t)
        iris(c, W / 2 + (D_X - cx) * Z, H / 2 + (FL - 200 - cy) * Z, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))


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
