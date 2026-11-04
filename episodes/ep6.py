"""FRIDGE KINGDOM — Episode 6: "The Jar Opens". 40s, 1080x1920 @ 30fps.

Variant B (cold open): no title card; a small title banner sits across the top for the first 2s.

The Pickle Jar lid POPS. Five little pickles hop out and march off the top shelf, BOINGing off
the jello; last comes ancient Grandma Gherkin, parachuting down on her shawl. Dill bursts out to
greet his family with open arms... they walk right past him and bow to the Duck. Dill makes a
rallying speech; Grandma bonks him with her cane. The pickles carry him off like a parade float
and dump him in the crisper drawer. In the dim drawer a wilted lettuce leaf pats his back, and
Dill finds a doodle scratched into the wall: the Hand holding the Duck, with hearts.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crumb, duck, crown, bubble, dark_overlay, ellipse, rrect, star, text,
                 iris, hexc, seg, ease, ease_out, lerp, back_out, INK, GOLD, FLOOR, TOP, W, H, FPS, S, BREAD, CRUST,
                 GREEN, GREEN_D, GREEN_L)
from ep2 import end_card, jello
from ep5 import cap_crown, gift_piece, crumb_notched, DUCK_X, JELLO_X, GIFT_X
from animate import heart

DUR = 40.0
END_T = 38.4
LIGHT = 0.18                 # door closed: dim fridge
JAR_X = 170
FRONT = FLOOR + 22           # front lip of the bottom shelf (nearer the camera)
LAVENDER, LAVENDER_D = hexc("#B197FC"), hexc("#7950F2")
OLIVE, OLIVE_D = hexc("#7F9A3A"), hexc("#5C7026")
CANE = hexc("#8D5A2B")
TEAR = hexc("#74C0FC")

# ---------------- timing ----------------
T_POP = 0.15
OUT_T = [0.55 + 0.32 * k for k in range(5)]          # pickles hop out of the jar
JAR_SLOT = [(-25, -260), (40, -265), (5, -170), (-45, -150), (50, -140)]   # where each sat in the jar
LAND_X = [578 - 62 * k for k in range(5)]              # landing spots on the top shelf
MARCH0 = 2.8
SPEED_TOP = 280
EDGE = 1020
FRONT_X = [860 + 50 * k for k in range(5)]             # where each lands on the front lip
LINE_X = [540 + 55 * k for k in range(5)]              # final bowing line
G_LINE_X = 830
BOW_T = [11.6 + 0.3 * k for k in range(5)]
G_BOW_T = 13.1
DILL_X = 700
SPEECH_X = 640
BONK_T = 18.35
LIFT_T = 20.0
TOSS_T = 23.0
THUNK_T = 23.65


def edge_t(k):
    return MARCH0 + (EDGE - LAND_X[k]) / SPEED_TOP


# ---------------- new characters ----------------
PICKLE_STYLES = [
    dict(ry=72, acc="none"), dict(ry=66, acc="mustache"), dict(ry=80, acc="bowtie"),
    dict(ry=60, acc="sprout"), dict(ry=70, acc="freckles"),
]


def pickle_kid(c, x, y, k, look=(-1, 0), bow=0.0, step=0.0, arms="down", rot=0.0, mood="calm"):
    """One of the five little Jar pickles. Feet at (x, y). bow<0 leans left. step = walk phase."""
    st = PICKLE_STYLES[k]
    ry = st["ry"]
    c.save(); c.translate(x, y); c.rotate(rot)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    sw = math.sin(step * 2 * math.pi)
    c.set_source_rgb(*INK); c.set_line_width(7)
    c.move_to(-12, -14); c.line_to(-14 - 8 * sw, 0); c.move_to(12, -14); c.line_to(14 + 8 * sw, 0); c.stroke()
    ellipse(c, -18 - 8 * sw, -2, 11, 6, INK, stroke=False); ellipse(c, 18 + 8 * sw, -2, 11, 6, INK, stroke=False)
    c.translate(0, -14); c.rotate(bow); c.translate(0, 14)
    cy = -14 - ry
    ellipse(c, 0, cy, 31, ry, GREEN_D, lw=5)
    ellipse(c, -12, cy - 10, 7, ry * 0.5, hexc("#6FA03A"), stroke=False)
    for bx, by in [(14, 0.4), (-16, -0.2), (10, -0.6), (-6, 0.7)]:
        ellipse(c, bx, cy + by * ry, 4, 5, hexc("#3E5F1E"), stroke=False)
    ey = cy - ry * 0.45
    lx, ly = look
    big = 1.35 if mood == "shock" else 1.0
    for ex in (-11, 11):
        ellipse(c, ex, ey, 9 * big, 10 * big, (1, 1, 1), lw=3)
        if mood == "closed":
            c.set_source_rgb(*INK); c.set_line_width(3); c.move_to(ex - 7, ey); c.line_to(ex + 7, ey); c.stroke()
        else:
            ellipse(c, ex + lx * 4, ey + ly * 4, 4, 4.5, INK, stroke=False)
    c.set_source_rgb(*INK); c.set_line_width(3)
    if mood == "shock":
        ellipse(c, 0, ey + 26, 6, 8, hexc("#7A1F2B"), lw=3)
    else:
        c.move_to(-7, ey + 24); c.line_to(7, ey + 24); c.stroke()
    acc = st["acc"]
    if acc == "mustache":
        c.set_source_rgb(*INK)
        c.move_to(0, ey + 17); c.curve_to(-10, ey + 10, -20, ey + 22, -24, ey + 14)
        c.curve_to(-18, ey + 26, -6, ey + 24, 0, ey + 19)
        c.curve_to(6, ey + 24, 18, ey + 26, 24, ey + 14); c.curve_to(20, ey + 22, 10, ey + 10, 0, ey + 17); c.fill()
    elif acc == "bowtie":
        by = cy + ry * 0.35
        c.move_to(0, by); c.line_to(-16, by - 9); c.line_to(-16, by + 9); c.close_path()
        c.move_to(0, by); c.line_to(16, by - 9); c.line_to(16, by + 9); c.close_path()
        c.set_source_rgb(*hexc("#E03131")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(2.5); c.stroke()
    elif acc == "sprout":
        c.set_source_rgb(*hexc("#2B8A3E")); c.set_line_width(4)
        c.move_to(0, cy - ry); c.curve_to(2, cy - ry - 14, 12, cy - ry - 20, 18, cy - ry - 18); c.stroke()
        ellipse(c, 18, cy - ry - 20, 8, 5, hexc("#69DB7C"), lw=2.5)
    elif acc == "freckles":
        for fx, fy in [(-16, 12), (-12, 17), (16, 12), (12, 17)]:
            ellipse(c, fx, ey + fy, 2.2, 2.2, hexc("#3E5F1E"), stroke=False)
    # arms
    c.set_source_rgb(*INK); c.set_line_width(6)
    if arms == "up":
        c.move_to(-26, cy - 10); c.line_to(-30, cy - ry - 30); c.move_to(26, cy - 10); c.line_to(30, cy - ry - 30)
    elif arms == "march":
        c.move_to(-28, cy + 6); c.line_to(-44 + 6 * sw, cy + 30); c.move_to(28, cy + 6); c.line_to(44 - 6 * sw, cy + 30)
    else:
        c.move_to(-28, cy + 6); c.line_to(-40, cy + 34); c.move_to(28, cy + 6); c.line_to(40, cy + 34)
    c.stroke()
    c.restore()


def grandma(c, x, y, look=(-1, 0), bow=0.0, cane="down", chute=0.0, step=0.0, mood="stern", hop=0.0):
    """Grandma Gherkin: tiny, ancient, hunched olive pickle; round spectacles, white garlic-clove bun,
    lavender shawl, wooden cane. chute 0..1 opens the shawl overhead as a parachute."""
    c.save(); c.translate(x, y - hop)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    sw = math.sin(step * 2 * math.pi)
    c.set_source_rgb(*INK); c.set_line_width(6)
    c.move_to(-9, -10); c.line_to(-11 - 5 * sw, 0); c.move_to(9, -10); c.line_to(11 + 5 * sw, 0); c.stroke()
    ellipse(c, -15 - 5 * sw, -2, 9, 5, INK, stroke=False); ellipse(c, 15 + 5 * sw, -2, 9, 5, INK, stroke=False)
    c.translate(0, -10); c.rotate(-0.22 + bow); c.translate(0, 10)   # always a little hunched forward (left)
    cy = -66
    # cane (behind arm)
    if cane == "down":
        cx0, cy0, cx1, cy1 = -34, cy + 18, -44, 10
    elif cane == "up":
        cx0, cy0, cx1, cy1 = -16, cy - 40, -40, cy - 175
    else:   # "drum": held high like a drum major's baton
        cx0, cy0, cx1, cy1 = -20, cy - 30, -10, cy - 150
    c.set_source_rgb(*INK); c.set_line_width(12); c.move_to(cx0, cy0); c.line_to(cx1, cy1); c.stroke()
    c.set_source_rgb(*CANE); c.set_line_width(7); c.move_to(cx0, cy0); c.line_to(cx1, cy1); c.stroke()
    ang = math.atan2(cy0 - cy1, cx0 - cx1)
    hx, hy = cx0, cy0
    c.save(); c.translate(hx, hy); c.rotate(ang)
    c.set_source_rgb(*INK); c.set_line_width(12); c.arc(12, 0, 12, math.pi, 2 * math.pi * 0.999); c.stroke()
    c.set_source_rgb(*CANE); c.set_line_width(7); c.arc(12, 0, 12, math.pi, 2 * math.pi * 0.999); c.stroke()
    c.restore()
    # body
    ellipse(c, 0, cy, 28, 56, OLIVE, lw=5)
    c.set_source_rgb(*OLIVE_D); c.set_line_width(3)
    for wy in (-14, 2, 18):    # wrinkles
        c.move_to(-14, cy + wy + 20); c.curve_to(-6, cy + wy + 16, 4, cy + wy + 24, 14, cy + wy + 19); c.stroke()
    # shawl
    if chute < 0.05:
        c.move_to(-30, cy - 14); c.curve_to(-10, cy + 4, 10, cy + 4, 30, cy - 14); c.line_to(4, cy + 34); c.close_path()
        c.set_source_rgb(*LAVENDER); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        for i in range(4):
            ellipse(c, -16 + i * 11, cy + 2 + i * 7, 3, 3, (1, 1, 1), stroke=False)
    # face
    ey = cy - 24
    lx, ly = look
    for ex in (-11, 11):
        if mood == "closed":
            c.set_source_rgb(*INK); c.set_line_width(3); c.move_to(ex - 6, ey + 1); c.line_to(ex + 6, ey + 1); c.stroke()
        else:
            ellipse(c, ex, ey, 7, 7, (1, 1, 1), lw=2.5)
            ellipse(c, ex + lx * 3, ey + ly * 3, 3, 3, INK, stroke=False)
        c.save(); c.translate(ex, ey); c.scale(11, 11); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.set_source_rgb(*hexc("#C9A227")); c.set_line_width(3); c.stroke()
    c.set_source_rgb(*hexc("#C9A227")); c.set_line_width(3); c.move_to(-1, ey); c.line_to(1, ey); c.stroke()
    c.set_source_rgb(*(1, 1, 1)); c.set_line_width(4)      # bushy white brows
    if mood == "angry":
        c.move_to(-22, ey - 20); c.line_to(-4, ey - 12); c.move_to(22, ey - 20); c.line_to(4, ey - 12)
    else:
        c.move_to(-22, ey - 14); c.line_to(-4, ey - 16); c.move_to(22, ey - 14); c.line_to(4, ey - 16)
    c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(3)
    c.move_to(-8, ey + 22); c.curve_to(-3, ey + 18, 3, ey + 18, 8, ey + 22); c.stroke()   # pursed frown
    # garlic-clove bun
    c.move_to(0, cy - 56 - 30); c.curve_to(14, cy - 70, 18, cy - 56, 0, cy - 52)
    c.curve_to(-18, cy - 56, -14, cy - 70, 0, cy - 86)
    c.set_source_rgb(*hexc("#F8F9FA")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3.5); c.stroke()
    c.set_source_rgb(*hexc("#DEE2E6")); c.set_line_width(2); c.move_to(0, cy - 82); c.line_to(0, cy - 56); c.stroke()
    # arm holding the cane
    c.set_source_rgb(*INK); c.set_line_width(5)
    c.move_to(-20, cy + 2); c.line_to(cx0 + (2 if cane == "down" else 0), cy0 + (2 if cane == "down" else 8)); c.stroke()
    if chute >= 0.05:   # shawl held overhead as a parachute
        k = chute
        c.set_line_width(4)
        c.move_to(20, cy - 6); c.line_to(54 * k, cy - 150 * k); c.move_to(-12, cy - 6); c.line_to(-54 * k, cy - 150 * k); c.stroke()
        c.save(); c.translate(0, cy - 150 * k); c.scale(S(k), S(k))
        c.move_to(-80, 10); c.curve_to(-80, -70, 80, -70, 80, 10)
        for i in range(4):
            c.curve_to(80 - 40 * i - 10, -2, 80 - 40 * i - 30, -2, 80 - 40 * (i + 1), 10)
        c.close_path(); c.set_source_rgb(*LAVENDER); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        for i in range(5):
            ellipse(c, -56 + i * 28, -12 - 8 * math.sin(i * 0.8), 4, 4, (1, 1, 1), stroke=False)
        c.restore()
    c.restore()


def wilt(c, x, y, droop=0.0, pat=0.0, look=(-1, 0)):
    """Wilt, the wilted lettuce leaf: pale crinkly leaf, top flopped over, half-lidded sad eyes.
    droop 0..1 bends the top further over to the left (to pat someone); pat adds a little tap."""
    c.save(); c.translate(x, y)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_source_rgb(*INK); c.set_line_width(7)
    c.move_to(-10, -16); c.line_to(-14, 0); c.move_to(10, -16); c.line_to(14, 0); c.stroke()
    ellipse(c, -20, -2, 12, 6, INK, stroke=False); ellipse(c, 20, -2, 12, 6, INK, stroke=False)
    PALE, PALE_D, BROWN = hexc("#C5D86D"), hexc("#94A84A"), hexc("#A08445")
    # lower body: wavy-edged leaf
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
    # rib
    c.set_source_rgb(*hexc("#F1F3C2")); c.set_line_width(10); c.move_to(0, -20); c.curve_to(0, -100, -4, -170, -10, -230); c.stroke()
    c.set_source_rgb(*PALE_D); c.set_line_width(3)
    for vy in (-60, -100, -140, -180):
        c.move_to(-2, vy); c.line_to(-46, vy - 22); c.move_to(2, vy); c.line_to(46, vy - 22); c.stroke()
    # floppy top, hanging over to the left
    a0 = lerp(0.5, 2.81 - 2 * math.pi, ease(droop)) - 0.3 * pat
    c.save(); c.translate(-10, -226); c.rotate(a0)
    c.move_to(0, -30)
    c.curve_to(60, -46, 130, -36, 170, 0)
    c.curve_to(150, 14, 160, 26, 140, 30); c.curve_to(120, 44, 100, 30, 80, 42); c.curve_to(50, 46, 30, 30, 0, 30)
    c.close_path(); c.set_source_rgb(*PALE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.set_source_rgb(*BROWN); c.set_line_width(5); c.move_to(150, 4); c.curve_to(158, 14, 150, 22, 140, 26); c.stroke()
    c.set_source_rgb(*hexc("#F1F3C2")); c.set_line_width(6); c.move_to(0, 0); c.curve_to(60, -8, 110, -6, 160, 2); c.stroke()
    c.restore()
    # brown wilted edges
    c.set_source_rgb(*BROWN); c.set_line_width(5)
    c.move_to(-70, -120); c.curve_to(-76, -100, -70, -80, -62, -64); c.stroke()
    c.move_to(68, -110); c.curve_to(74, -92, 70, -76, 60, -60); c.stroke()
    # sad, half-lidded eyes
    lx, ly = look
    for ex in (-22, 22):
        ellipse(c, ex, -150, 14, 15, (1, 1, 1), lw=4)
        ellipse(c, ex + lx * 5, -146 + ly * 4, 6, 6, INK, stroke=False)
        c.save(); c.translate(ex, -150); c.scale(14, 15); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
        c.save(); c.clip(); c.rectangle(ex - 16, -168, 32, 16); c.set_source_rgb(*PALE_D); c.fill(); c.restore()
        c.set_source_rgb(*INK); c.set_line_width(4); c.move_to(ex - 14, -152); c.line_to(ex + 14, -152); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(4)
    c.move_to(-14, -112); c.curve_to(-6, -122, 6, -122, 14, -112); c.stroke()
    c.restore()


# ---------------- set ----------------
def jar_pickles(c, n_inside, light):
    """Jar contents, drawn over our own empty jar (the jar from fridge_bg with only n pickles left)."""
    dim = lerp(0.6, 1.0, light)
    slots = [(-45, -150, 0.1), (5, -170, -0.1), (50, -140, 0.15), (-25, -260, 0.2), (40, -265, -0.1)]
    order = [3, 4, 1, 0, 2]   # which slot empties first
    left = order[5 - n_inside:] if n_inside < 5 else order
    for idx in left:
        px, py, rot = slots[idx]
        c.save(); c.translate(px, py); c.rotate(rot)
        ellipse(c, 0, 0, 26, 70, [v * dim for v in GREEN_D], lw=4)
        ellipse(c, -6, -20, 6, 7, (1, 1, 1), stroke=False); ellipse(c, 8, -20, 6, 7, (1, 1, 1), stroke=False)
        ellipse(c, -6, -21, 3, 3, INK, stroke=False); ellipse(c, 8, -21, 3, 3, INK, stroke=False)
        c.restore()


def fridge6(c, light, n_inside, lid=True, drawer_shake=0.0):
    """fridge_bg from ep1 with a controllable jar (contents + lid)."""
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc("#3D5285")); g.add_color_stop_rgb(1, *hexc("#24325A"))
    c.rectangle(-400, -400, W + 800, H + 1200); c.set_source(g); c.fill()
    if light > 0:
        g2 = cairo.LinearGradient(0, 0, 0, H)
        g2.add_color_stop_rgb(0, *hexc("#F3FAFF")); g2.add_color_stop_rgb(1, *hexc("#BFE0F5"))
        c.rectangle(-400, -400, W + 800, H + 1200); c.set_source(g2); c.paint_with_alpha(light)
    dim = lerp(0.6, 1.0, light)
    c.set_source_rgba(1, 1, 1, 0.06 + 0.1 * light); c.set_line_width(8)
    for i in range(6):
        c.move_to(150, 140 + i * 40); c.line_to(930, 140 + i * 40); c.stroke()
    c.save(); c.translate(JAR_X, TOP)
    rrect(c, -95, -330, 190, 330, 30); c.set_source_rgba(0.8, 0.95, 0.85, 0.35 + 0.25 * light); c.fill_preserve()
    c.set_source_rgba(*INK, 1); c.set_line_width(6); c.stroke()
    jar_pickles(c, n_inside, light)
    if lid:
        rrect(c, -100, -370, 200, 50, 12); c.set_source_rgb(*[v * dim for v in hexc("#E03131")]); c.fill_preserve()
        c.set_source_rgb(*INK); c.stroke()
    else:   # open rim
        ellipse(c, 0, -330, 92, 14, (0.85, 0.95, 0.9), lw=5)
    c.restore()
    # milk carton
    c.save(); c.translate(110, FLOOR)
    c.rectangle(-80, -420, 160, 420); c.set_source_rgb(*[v * dim for v in (0.95, 0.95, 1)]); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.move_to(-80, -420); c.line_to(0, -500); c.line_to(80, -420); c.close_path()
    c.set_source_rgb(*[v * dim for v in hexc("#4DABF7")]); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.rectangle(-80, -300, 160, 110); c.set_source_rgb(*[v * dim for v in hexc("#4DABF7")]); c.fill()
    c.restore()
    for sy in (TOP, FLOOR):
        c.rectangle(-400, sy, W + 800, 34); c.set_source_rgba(0.75, 0.9, 1.0, 0.55 + 0.3 * light); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        c.rectangle(-400, sy + 6, W + 800, 6); c.set_source_rgba(1, 1, 1, 0.6); c.fill()
    drawer_back(c, drawer_shake)


def drawer_back(c, sh=0.0):
    rrect(c, 40 + sh, FLOOR + 90, 1000, 400, 30); c.set_source_rgba(0.7, 0.85, 1, 0.18); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()


def drawer_front(c, sh=0.0):
    """Frosted front panel, drawn over anything that fell into the drawer."""
    rrect(c, 40 + sh, FLOOR + 160, 1000, 330, 30); c.set_source_rgba(0.62, 0.78, 0.95, 0.72); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    rrect(c, 440 + sh, FLOOR + 200, 200, 36, 18); c.set_source_rgba(1, 1, 1, 0.5); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.35); c.set_line_width(10)
    c.move_to(110 + sh, FLOOR + 220); c.line_to(170 + sh, FLOOR + 420); c.stroke()


def lid_piece(c, x, y, rot, squash=1.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(1, S(squash))
    rrect(c, -100, -25, 200, 50, 12); c.set_source_rgb(*[v * 0.7 for v in hexc("#E03131")]); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.set_source_rgb(*[v * 0.7 for v in hexc("#A61E1E")]); c.set_line_width(5)
    for i in range(7):
        c.move_to(-84 + i * 28, -19); c.line_to(-84 + i * 28, 19); c.stroke()
    c.restore()


def doodle(c, alpha=1.0, wobble=0.0):
    """Scratched into the drawer's frosted wall: the Hand holding the Duck, with hearts."""
    col = (0.92, 0.97, 1.0)
    BG = hexc("#22403D")
    c.save(); c.translate(330, 980); c.scale(1.25, 1.25)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)

    def ln(w=8):
        c.set_source_rgba(*col, alpha); c.set_line_width(w); c.stroke()
    # the Hand's arm coming down from the top, and its palm behind the duck
    c.move_to(-55, -330); c.line_to(-60, -150); c.move_to(55, -330); c.line_to(62, -150); ln()
    c.move_to(-60, -150); c.curve_to(-140, -140, -150, -40, -120, 10); ln()
    c.move_to(62, -150); c.curve_to(140, -140, 150, -40, 124, 10); ln()
    # the duck (scratched), sitting in the hand
    c.save(); c.translate(0, -10)
    c.save(); c.scale(95, 58); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); ln()
    c.move_to(-82, -20); c.line_to(-122, -52); c.line_to(-88, 14); ln(7)              # tail
    c.save(); c.translate(30, -84); c.scale(48, 46); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*BG, 1); c.fill_preserve(); ln()
    c.move_to(72, -86); c.line_to(118, -74); c.line_to(72, -62); ln(7)              # beak
    c.arc(44, -98, 6, 0, 2 * math.pi); c.set_source_rgba(*col, alpha); c.fill()      # eye
    c.move_to(4, -124); c.line_to(8, -150); c.line_to(20, -134); c.line_to(30, -156); c.line_to(40, -134)
    c.line_to(52, -150); c.line_to(56, -124); ln(6)                                  # its bottle-cap crown
    c.restore()
    # four big fingers wrapped around the front of the duck, thumb on the side
    for i, fx in enumerate((-90, -40, 10, 60)):
        c.save(); c.translate(fx + 15, 52 - 6 * (i in (1, 2))); c.rotate(0.12)
        rrect(c, -22, -40, 44, 86, 22); c.set_source_rgba(*BG, 1); c.fill_preserve(); ln(7)
        c.restore()
    c.save(); c.translate(124, -10); c.rotate(-0.5)
    rrect(c, -20, -50, 40, 92, 20); c.set_source_rgba(*BG, 1); c.fill_preserve(); ln(7)
    c.restore()
    c.restore()
    for (hx, hy, hs) in [(120, 640, 2.6), (560, 700, 2.0), (610, 930, 2.2), (90, 1180, 2.0), (330, 560, 1.6)]:
        s2 = hs * (1 + 0.1 * math.sin(wobble * 6 + hx))
        c.save(); c.translate(hx, hy); c.scale(s2, s2)
        c.move_to(0, 12); c.curve_to(-30, -10, -18, -34, 0, -18); c.curve_to(18, -34, 30, -10, 0, 12); c.close_path()
        c.set_source_rgba(*col, alpha); c.set_line_width(8 / s2); c.stroke()
        c.restore()


def drawer_inside_bg(c, t):
    g = cairo.LinearGradient(0, 300, 0, 1900)
    g.add_color_stop_rgb(0, *hexc("#24423F")); g.add_color_stop_rgb(1, *hexc("#122523"))
    c.rectangle(-400, -400, W + 800, H + 800); c.set_source(g); c.fill()
    # frosted ridges on the back wall
    c.set_source_rgba(1, 1, 1, 0.05); c.set_line_width(26)
    for i in range(-4, 16):
        x = i * 90 + 20
        c.move_to(x, 300); c.line_to(x, 1550); c.stroke()
    # cold glow from above (light leaking through the shelf)
    rg = cairo.RadialGradient(640, 280, 40, 640, 280, 1100)
    rg.add_color_stop_rgba(0, 0.75, 0.95, 1.0, 0.30); rg.add_color_stop_rgba(1, 0.75, 0.95, 1.0, 0.0)
    c.rectangle(-400, -400, W + 800, H + 800); c.set_source(rg); c.fill()
    doodle(c, 0.5, t)
    # floor of the drawer
    c.rectangle(-400, 1550, W + 800, 500); c.set_source_rgb(*hexc("#1B3532")); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(6); c.move_to(-400, 1550); c.line_to(W + 400, 1550); c.stroke()
    # a few sad leftovers
    ellipse(c, 120, 1560, 70, 14, hexc("#2F4F2A"), lw=4)           # a flat old leaf
    c.save(); c.translate(1010, 1550); c.rotate(-0.3)
    c.move_to(-12, 0); c.line_to(12, 0); c.line_to(4, -70); c.line_to(-4, -70); c.close_path()   # a carrot nub
    c.set_source_rgb(*hexc("#B85C1E")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    c.restore()


# ---------------- title banner (variant B cold open) ----------------
def banner(c, t):
    if t >= 2.3:
        return
    off = -260 * ease(seg(t, 2.0, 2.3))
    c.save(); c.translate(0, off)
    rrect(c, 40, 34, W - 80, 176, 40); c.set_source_rgba(*hexc("#1C2541"), 0.88); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(8); c.stroke()
    text(c, "FRIDGE KINGDOM", W / 2 + 30, 112, 66, GOLD, olw=10)
    crown(c, 150, 120, 0.7, -0.2)
    text(c, "Ep. 6:  The Jar Opens", W / 2, 182, 46, (1, 1, 1), olw=8)
    c.restore()


# ---------------- motion ----------------
def hop(a, b, p, height=200):
    return lerp(a[0], b[0], p), lerp(a[1], b[1], p) - height * math.sin(math.pi * p)


def pickle_state(k, t):
    """Return (x, y, kwargs) for pickle k, or None if still in the jar."""
    if t < OUT_T[k]:
        return None
    sx, sy = JAR_SLOT[k]
    start = (JAR_X + sx, TOP + sy + 70)
    if t < OUT_T[k] + 0.45:      # hop out of the jar
        p = seg(t, OUT_T[k], OUT_T[k] + 0.45)
        x, y = hop(start, (LAND_X[k], TOP), p, 330)
        return x, y, dict(look=(1, -0.5), arms="up", mood="calm")
    te = edge_t(k)
    if t < MARCH0:               # waiting in line
        return LAND_X[k], TOP, dict(look=(-1, 0) if t < OUT_T[k] + 0.7 else (1, 0), mood="calm")
    if t < te:                   # march right along the top shelf
        x = LAND_X[k] + SPEED_TOP * (t - MARCH0)
        return x, TOP - abs(math.sin((t - MARCH0) * 9)) * 10, dict(look=(1, 0), step=(t - MARCH0) * 2.2, arms="march")
    if t < te + 0.38:            # step off the edge and drop onto the jello
        p = seg(t, te, te + 0.38)
        x = lerp(EDGE, JELLO_X - 40 + 25 * k, p)
        y = TOP + (FLOOR - 270 - TOP) * p * p - 60 * math.sin(math.pi * p)
        return x, y, dict(look=(0, 1), arms="up", mood="shock")
    if t < te + 0.48:            # BOING (squash on the jello)
        return JELLO_X - 40 + 25 * k, FLOOR - 270, dict(look=(0, 1), arms="up", mood="closed")
    if t < te + 0.95:            # bounce down to the front lip
        p = seg(t, te + 0.48, te + 0.95)
        x, y = hop((JELLO_X - 40 + 25 * k, FLOOR - 270), (FRONT_X[k], FRONT), p, 180)
        y = lerp(FLOOR - 270, FRONT, p * p) - 180 * math.sin(math.pi * p)
        return x, y, dict(look=(-1, 0), arms="up", mood="calm", rot=-p * 2 * math.pi)
    if t < 9.4:                  # stand, waiting for Grandma
        return FRONT_X[k], FRONT, dict(look=(-1, 0) if k % 2 else (1, -0.3), mood="calm")
    if t < 11.3:                 # march left past Dill to the Duck
        p = seg(t, 9.4, 11.3)
        x = lerp(FRONT_X[k], LINE_X[k], p)
        return x, FRONT - abs(math.sin((t - 9.4) * 9)) * 8, dict(look=(-1, 0), step=(t - 9.4) * 2.2, arms="march")
    if t < 15.3:                 # bow to the Duck
        b = ease(seg(t, BOW_T[k], BOW_T[k] + 0.25)) * (1 - ease(seg(t, 15.0, 15.3)))
        return LINE_X[k], FRONT, dict(look=(-1, 0.6), bow=-0.6 * b, mood="closed" if b > 0.6 else "calm")
    if t < LIFT_T:               # turn to watch Dill's speech
        return LINE_X[k], FRONT, dict(look=(1, -0.6), mood="calm")
    if t < TOSS_T + 0.5:         # parade float
        cx, _ = float_pos(t)
        px = cx + (k - 2) * 62
        if t < LIFT_T + 0.5:
            p = ease(seg(t, LIFT_T, LIFT_T + 0.5))
            px = lerp(LINE_X[k], SPEECH_X + (k - 2) * 62, p)
        return px, FRONT - abs(math.sin((t - LIFT_T) * 6 + k)) * 6, dict(look=(-1, -1), arms="up", step=(t - LIFT_T) * 1.2, mood="calm")
    return None


def float_pos(t):
    """Centre of Dill's body while he's carried (lying flat, head left)."""
    if t < LIFT_T + 0.5:
        p = ease(seg(t, LIFT_T, LIFT_T + 0.5))
        return SPEECH_X, lerp(FRONT + 18 - 155, FRONT - 230, p)
    p = seg(t, LIFT_T + 0.5, TOSS_T)
    return lerp(SPEECH_X, 470, ease(p)), FRONT - 230 - 8 * abs(math.sin(t * 6))


def grandma_state(t):
    if t < 2.3:
        return None
    if t < 2.9:   # climbs over the rim
        p = ease(seg(t, 2.3, 2.9))
        return JAR_X + 30, TOP - 300 - 60 * p, dict(look=(1, -0.3), cane="up" if p < 0.5 else "down", hop=0)
    if t < 3.25:  # hops down beside the jar
        p = seg(t, 2.9, 3.25)
        x, y = hop((JAR_X + 30, TOP - 360), (300, TOP), p, 80)
        y = lerp(TOP - 360, TOP, p * p) - 80 * math.sin(math.pi * p)
        return x, y, dict(look=(1, 0), cane="down")
    if t < 5.6:   # hobbles (surprisingly fast)
        x = min(EDGE, 300 + 330 * (t - 3.25))
        return x, TOP - abs(math.sin(t * 14)) * 6, dict(look=(1, 0), step=(t - 3.25) * 3, cane="down")
    if t < 6.9:   # parachute down on her shawl
        p = seg(t, 5.6, 6.9)
        ch = back_out(seg(t, 5.6, 5.85))
        x = lerp(EDGE, JELLO_X + 60, p) + 30 * math.sin(p * 9)
        y = lerp(TOP, FLOOR - 270, p)
        return x, y, dict(look=(0, 1), chute=ch, cane="down", mood="stern")
    if t < 7.4:   # on the jello, then a dignified step down
        if t < 7.1:
            return JELLO_X + 60, FLOOR - 270, dict(look=(-1, 0), chute=1 - seg(t, 6.9, 7.05))
        p = seg(t, 7.1, 7.4)
        x, y = hop((JELLO_X + 60, FLOOR - 270), (1070, FRONT), p, 40)
        y = lerp(FLOOR - 270, FRONT, p) - 40 * math.sin(math.pi * p)
        return x, y, dict(look=(-1, 0))
    if t < 9.4:
        return 1070, FRONT, dict(look=(-1, 0))
    if t < 11.0:
        p = seg(t, 9.4, 11.0)
        return lerp(1070, G_LINE_X, p), FRONT - abs(math.sin(t * 12)) * 4, dict(look=(-1, 0), step=(t - 9.4) * 2.5)
    if t < 15.3:
        b = ease(seg(t, G_BOW_T, G_BOW_T + 0.6)) * (1 - ease(seg(t, 15.0, 15.3)))
        return G_LINE_X, FRONT, dict(look=(-1, 0.6), bow=-0.6 * b, mood="closed" if b > 0.5 else "stern")
    if t < 17.0:  # hobbles toward Dill during his speech, unimpressed
        p = seg(t, 15.8, 17.0)
        return lerp(G_LINE_X, 860, p), FRONT, dict(look=(-1, -1), step=p * 3)
    if t < BONK_T - 0.3:
        return 860, FRONT, dict(look=(-1, -1), mood="angry")
    if t < BONK_T + 0.5:   # springs up: BONK
        p = seg(t, BONK_T - 0.3, BONK_T + 0.3)
        hp = 120 * math.sin(math.pi * min(1, p))
        return 860, FRONT, dict(look=(-1, -1), mood="angry", cane="up", hop=hp)
    if t < LIFT_T:
        return 860, FRONT, dict(look=(-1, -0.5), mood="stern")
    if t < TOSS_T + 0.6:   # leads the parade like a drum major
        cx, _ = float_pos(t)
        x = cx - 230 if t >= LIFT_T + 0.5 else lerp(860, SPEECH_X - 230, ease(seg(t, LIFT_T, LIFT_T + 0.5)))
        return x, FRONT - abs(math.sin(t * 7)) * 6, dict(look=(-1, 0), cane="drum", step=(t - LIFT_T) * 1.2)
    return None


def dill_state(t):
    """Bottom-shelf Dill: (x, y, kwargs) or None."""
    if t < 3.7:   # peeking over the jello (as Ep 5 ended), trembling
        return JELLO_X - 60, FLOOR - 125 - 4 * math.sin(t * 40), dict(mood="shocked", look=(-1, -1), shake=2)
    if t < 4.0:   # sees his family: lights up
        return JELLO_X - 60, FLOOR - 140, dict(mood="proud", look=(-1, -1))
    if t < 4.5:   # leaps out
        p = seg(t, 4.0, 4.5)
        x = lerp(JELLO_X - 60, DILL_X, p)
        y = lerp(FLOOR - 140, FLOOR, p) - 220 * math.sin(math.pi * p)
        return x, y, dict(mood="proud", look=(1, -1), arm="reach", rot=-0.3 * math.sin(math.pi * p))
    if t < 10.3:  # arms wide, beaming, waiting for the bow
        sh = 6 * math.sin(t * 8) if 7.4 <= t < 9.4 else 0
        return DILL_X, FLOOR, dict(mood="proud", look=(1, -1) if t < 7.4 else (1, 0.3), arm="reach", rot=0.04 * math.sin(t * 4) + sh * 0.004)
    if t < 11.5:  # ...they walk right past
        return DILL_X, FLOOR, dict(mood="proud" if t < 10.4 else "frozen", look=(-1, 0.4), arm="reach")
    if t < 15.3:
        return DILL_X, FLOOR, dict(mood="shocked", look=(-1, 0.4), arm="down",
                                   shake=3 if 13.6 <= t < 14.4 else 0)
    if t < 15.7:  # hops to the front for his speech
        p = seg(t, 15.3, 15.7)
        x = lerp(DILL_X, SPEECH_X, p); y = lerp(FLOOR, FRONT + 18, p) - 140 * math.sin(math.pi * p)
        return x, y, dict(mood="angry", look=(0, 0), arm="up")
    if t < 17.5:  # rallying speech
        beat = int((t - 15.7) / 0.45)
        arm = ["up", "point", "up", "pound", "up"][beat % 5]
        mood = ["angry", "proud", "angry", "proud", "angry"][beat % 5]
        return SPEECH_X, FRONT + 18 - abs(math.sin((t - 15.7) * 7)) * 14, dict(mood=mood, look=(0, 0), arm=arm)
    if t < BONK_T:   # leans down toward Grandma, smug
        p = ease(seg(t, 17.5, 17.95))
        return SPEECH_X, FRONT + 18, dict(mood="smug", look=(1, 1), arm="down", rot=0.42 * p)
    if t < LIFT_T:   # BONK: slide whistle down
        p = ease(seg(t, BONK_T + 0.1, BONK_T + 1.0))
        rot = 0.42 * (1 - ease(seg(t, BONK_T, BONK_T + 0.4)))
        return SPEECH_X, FRONT + 18, dict(mood="frozen", look=(0, 0), arm="down", rot=rot, sq=lerp(1.0, 0.72, p))
    if t < TOSS_T:   # carried, flat, head-first
        cx, cy = float_pos(t)
        p = ease(seg(t, LIFT_T, LIFT_T + 0.5))
        rot = lerp(0, -math.pi / 2, p)
        # keep the body centre on (cx, cy): feet = centre - rotated (0, -155)
        fx = cx - 155 * math.sin(rot); fy = cy + 155 * math.cos(rot)
        return fx, fy, dict(mood="frozen" if t < 21.5 else "shocked", look=(0, -1), arm="down", rot=rot,
                            sq=lerp(0.72, 1.0, seg(t, LIFT_T, LIFT_T + 0.5)))
    if t < THUNK_T + 0.1:   # tossed down into the crisper drawer
        p = seg(t, TOSS_T, THUNK_T)
        cx = lerp(470, 500, p); cy = lerp(FRONT - 230, FLOOR + 330, p * p) - 160 * math.sin(math.pi * p)
        rot = -math.pi / 2 - p * 1.8 * math.pi
        fx = cx - 155 * math.sin(rot); fy = cy + 155 * math.cos(rot)
        return fx, fy, dict(mood="shocked", look=(0, 1), arm="reach", rot=rot)
    return None


# ---------------- camera ----------------
SHOT_B, SHOT_C, SHOT_D, SHOT_E, SHOT_F = 3.3, 7.4, 9.4, 15.2, 20.0
SHOT_CRUMB, SHOT_G, SHOT_H, SHOT_I = 23.9, 25.8, 31.0, 35.8


def camera(t):
    if t < SHOT_B:   # the jar
        k = ease(seg(t, 0.0, SHOT_B))
        return lerp(300, 400, k), lerp(TOP - 250, TOP - 200, k), lerp(2.0, 1.75, k)
    if t < SHOT_C:   # wide: top shelf to jello
        k = ease(seg(t, SHOT_B, SHOT_C))
        return lerp(700, 760, k), lerp(1040, 1110, k), lerp(1.3, 1.36, k)
    if t < SHOT_D:   # Dill beaming
        k = seg(t, SHOT_C, SHOT_D)
        return DILL_X + 10, FLOOR - 215, lerp(2.7, 3.0, k)
    if t < SHOT_E:   # the walk-past and the bow
        k = ease(seg(t, SHOT_D, 11.4))
        k2 = ease(seg(t, 13.4, 14.0)) * (1 - ease(seg(t, 14.5, 14.9)))   # push in on the Duck's nod
        x = lerp(lerp(860, 645, k), DUCK_X + 40, k2)
        y = lerp(FLOOR - 165, FLOOR - 170, k2)
        return x, y, lerp(2.0, 3.0, k2)
    if t < SHOT_F:   # speech + bonk
        k = ease(seg(t, 17.4, 18.0))
        return lerp(680, 730, k), lerp(FLOOR - 200, FLOOR - 190, k), lerp(2.0, 2.3, k)
    if t < SHOT_CRUMB:   # parade, toss into drawer
        k = ease(seg(t, TOSS_T - 0.1, THUNK_T))
        return lerp(lerp(620, 520, seg(t, SHOT_F, TOSS_T)), 520, k), lerp(FLOOR - 170, FLOOR + 150, k), lerp(1.65, 1.5, k)
    if t < SHOT_G:   # Crumb waves goodbye
        k = seg(t, SHOT_CRUMB, SHOT_G)
        return JELLO_X + 50, FLOOR - 250, lerp(2.6, 2.8, k)
    if t < SHOT_H:   # inside the drawer
        k = ease(seg(t, SHOT_G, 29.5))
        return lerp(755, 770, k), lerp(1400, 1410, k), lerp(2.3, 2.45, k)
    if t < SHOT_I:   # the doodle
        k = ease(seg(t, SHOT_H, 32.2))
        k2 = ease(seg(t, 32.2, SHOT_I))
        return lerp(lerp(770, 420, k), 360, k2), lerp(1410, 1040, k), lerp(2.45, lerp(1.85, 2.15, k2), k)
    # Dill's face, DUN DUN DUNNN punches
    z = 2.1
    for i, tp in enumerate((35.85, 36.55, 37.25)):
        if t >= tp:
            z = 2.1 + 0.45 * (i + 1) * ease_out(seg(t, tp, tp + 0.12))
    return 560, 1550 - 230, z


# ---------------- scenes ----------------
def shelf_scene(c, t):
    cx, cy, Z = camera(t)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    random.seed(int(t * 30))
    sh = 0.0
    if THUNK_T <= t < THUNK_T + 0.5:
        sh = 14 * math.sin((t - THUNK_T) * 50) * (1 - seg(t, THUNK_T, THUNK_T + 0.5))
    n_in = 5 - sum(1 for k in range(5) if t >= OUT_T[k] + 0.05)
    fridge6(c, LIGHT, n_in, lid=False, drawer_shake=sh)

    # the lid: lifted, POP, flies off, clatters onto the top shelf to the right
    if t < T_POP:
        lift = 25 + 60 * seg(t, 0, T_POP)
        lid_piece(c, JAR_X, TOP - 345 - lift, 0.0)
    elif t < 1.5:
        p = seg(t, T_POP, 1.5)
        x = lerp(JAR_X, 760, p); y = TOP - 430 - 900 * math.sin(math.pi * p * 0.9) + 420 * p * p + 0 * p
        y = lerp(TOP - 430, TOP - 25, p * p) - 700 * math.sin(math.pi * p)
        lid_piece(c, x, y, p * 7.5)
    else:   # spinning like a coin, settling
        q = seg(t, 1.5, 2.6)
        spin = math.cos((t - 1.5) * 30 * (1 - q * 0.8))
        lid_piece(c, 760, TOP - 25 + 20 * (1 - q) * abs(spin) * 0, 0.0, lerp(abs(spin), 1.0, q) if q < 1 else 1.0)

    # jello (pickles land on it)
    wob = 0.0
    for k in range(5):
        te = edge_t(k) + 0.38
        if te <= t < te + 0.8:
            wob += math.sin((t - te) * 22) * (1 - seg(t, te, te + 0.8))
    if 6.9 <= t < 7.6:
        wob += 0.5 * math.sin((t - 6.9) * 16) * (1 - seg(t, 6.9, 7.6))

    # Dill and Crumb behind the jello at first
    ds = dill_state(t)
    behind = t < 4.25
    if ds and behind:
        x, y, kw = ds; dill(c, x, y, crown_on=True, **kw)
    cr_y = FLOOR - 185 - 4 * math.sin(t * 40)
    if t < 4.6:
        pass
    elif t < 7.2:
        cr_y = FLOOR - 120     # ducks down when the pickles start landing
    else:
        cr_y = FLOOR - 185 + 0 * t
    if t < SHOT_CRUMB:
        crumb_notched(c, JELLO_X + 55, cr_y, True, mood="scared" if t < 9 else "worried", look=(-1, 0),
                      shake=3 if t < 4.6 else 0)
    else:   # waving goodbye
        crumb_notched(c, JELLO_X + 55, FLOOR - 185, True, mood="worried", look=(-1, 0.5), arm="wave")
    c.save(); c.translate(JELLO_X, FLOOR); c.scale(1.8, 1.8); c.translate(-JELLO_X, -FLOOR)
    jello(c, JELLO_X, FLOOR, max(-1, min(1, wob))); c.restore()

    # the Duck on Dill's throne spot (crown still tilted from Ep 5); its one motion: a slow nod
    nod = 0.0
    if 13.6 <= t < 14.6:
        nod = math.sin(math.pi * seg(t, 13.6, 14.6))
    c.save(); c.translate(DUCK_X, FLOOR - 40); c.rotate(-0.12 * nod); c.translate(-DUCK_X, -(FLOOR - 40))
    duck(c, DUCK_X, FLOOR, turn=1.0)
    cap_crown(c, DUCK_X + 6, FLOOR - 186, 0.38)
    c.restore()
    if t < 20.0:
        gift_piece(c, GIFT_X, FLOOR - 22, 0.0)

    # Dill (in front of the jello, behind the pickle line), unless he's at the front
    front_dill = 15.5 <= t
    if ds and not behind and not front_dill:
        x, y, kw = ds; dill(c, x, y, crown_on=True, **kw)

    # pickles + Grandma, sorted by x for a tidy overlap
    bodies = []
    for k in range(5):
        st = pickle_state(k, t)
        if st:
            bodies.append((st[0], "p", k, st))
    g = grandma_state(t)
    if g:
        bodies.append((g[0], "g", 0, g))
    on_top = []
    for _, kind, k, st in sorted(bodies, key=lambda b: -b[0]):
        x, y, kw = st
        if kind == "p":
            pickle_kid(c, x, y, k, **kw)
        else:
            grandma(c, x, y, **kw)

    if ds and front_dill:
        x, y, kw = ds
        if t >= TOSS_T + 0.25:   # falling into the drawer: behind its front panel
            dill(c, x, y, crown_on=True, **kw)
        else:
            dill(c, x, y, crown_on=True, **kw)
    if t >= TOSS_T + 0.25:
        drawer_front(c, sh)

    # ---- effects ----
    def word(s, x, y, size, col, t0, t1, rot=0.0):
        if t0 <= t < t1:
            k = back_out(seg(t, t0, t0 + 0.2))
            c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(k), S(k)); text(c, s, 0, 0, size, col, olw=12); c.restore()
    word("POP!", JAR_X + 150, TOP - 520, 110, (1, 1, 1), T_POP, 0.9, -0.12)
    word("CLANG", 760, TOP - 130, 54, (1, 1, 1), 1.5, 2.2, 0.1)
    for k in range(5):
        te = edge_t(k) + 0.38
        word("BOING!" if k % 2 == 0 else "BOING!", JELLO_X - 80 + 40 * k, FLOOR - 380 - 18 * k, 50, hexc("#FF8FB3"), te, te + 0.5, 0.12 * (1 if k % 2 else -1))
    if 3.75 <= t < 4.3:   # Dill's delighted "!"
        s = back_out(seg(t, 3.75, 3.9))
        c.save(); c.translate(JELLO_X - 60, FLOOR - 520); c.scale(S(s), S(s)); text(c, "!", 0, 0, 120, GOLD, olw=12); c.restore()
    if SHOT_C <= t < SHOT_D:   # sparkles around Dill's beaming face
        for j in range(5):
            a = t * 2.2 + j * 1.26
            star(c, DILL_X + 10 + 190 * math.cos(a), FLOOR - 230 + 170 * math.sin(a), 16 + 6 * math.sin(t * 9 + j), t * 2 + j, GOLD)
        for j in range(3):
            q = ((t - SHOT_C) * 0.9 + j / 3) % 1
            heart(c, DILL_X - 120 + j * 120, FLOOR - 400 - q * 120, 1.6, 1 - q)
    if 10.4 <= t < 11.1:    # record scratch mark over Dill
        s = back_out(seg(t, 10.4, 10.55))
        c.save(); c.translate(DILL_X + 20, FLOOR - 440); c.scale(S(s), S(s)); text(c, "?!", 0, 0, 110, (1, 0.35, 0.35), olw=12); c.restore()
    if 15.9 <= t < 17.5:    # speech bubble: crown + pickle army
        def icon(cc):
            crown(cc, 0, -18, 1.1, 0.0)
            for i in range(3):
                cc.save(); cc.translate(-50 + i * 50, 66); cc.scale(0.38, 0.38); pickle_kid(cc, 0, 0, i, look=(0, -1), arms="up"); cc.restore()
        bubble(c, SPEECH_X - 70, FRONT - 600, back_out(seg(t, 15.9, 16.2)) * (1 - seg(t, 17.2, 17.5)), icon)
    word("BONK!", 820, FRONT - 400, 96, (1, 1, 1), BONK_T, BONK_T + 0.8, 0.1)
    if BONK_T + 0.3 <= t < LIFT_T + 0.4:   # dizzy stars
        for k in range(3):
            a = t * 5 + k * 2.1
            star(c, SPEECH_X + 100 * math.cos(a), FRONT - 320 + 20 * math.sin(a), 20, t * 3)
    word("SHHHK", 560, FLOOR + 120, 64, (1, 1, 1), TOSS_T + 0.35, THUNK_T + 0.1, -0.08)
    word("THUNK!", 640, FLOOR + 50, 96, (1, 1, 1), THUNK_T, THUNK_T + 0.7, 0.1)
    if t >= SHOT_CRUMB:     # Crumb's tiny goodbye wave lines + a falling tear
        q = ((t - SHOT_CRUMB) * 1.2) % 1
        ellipse(c, JELLO_X + 55 + 78, FLOOR - 185 - 204 + q * 120, 6, 9, TEAR, lw=2)
    dark_overlay(c, LIGHT)


def drawer_scene(c, t):
    cx, cy, Z = camera(t)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    random.seed(int(t * 30))
    drawer_inside_bg(c, t)
    if t >= SHOT_H:   # the doodle "lights up" as Dill notices it
        a = ease(seg(t, SHOT_H + 0.2, SHOT_H + 1.2))
        doodle(c, 0.5 * a, t)
        if 31.3 <= t < 32.3:
            q = seg(t, 31.3, 32.3)
            c.save(); c.translate(330, 960); c.scale(lerp(0.6, 1.6, q), lerp(0.6, 1.6, q))
            c.arc(0, 0, 260, 0, 2 * math.pi); c.set_source_rgba(1, 1, 1, 0.25 * (1 - q)); c.set_line_width(10); c.stroke(); c.restore()
    FL = 1550
    # Dill
    if t < 29.8:   # slumped, sad
        sniff = 0.02 * math.sin(t * 3)
        dill(c, 640, FL, mood="sad", look=(0, 1), arm="down", crown_on=True, rot=sniff, sq=0.86)
        q = ((t - SHOT_G) * 0.8) % 1
        ellipse(c, 640 - 28, FL - 0.86 * 205 + 30 + q * 90, 7, 10, TEAR, lw=2)
    elif t < SHOT_H:   # notices something
        dill(c, 640, FL, mood="frozen", look=(-1, -0.5), arm="down", crown_on=True, sq=lerp(0.86, 1.0, seg(t, 29.8, 30.2)))
    elif t < SHOT_I:   # walks to the wall, staring
        p = ease(seg(t, SHOT_H, 32.0))
        x = lerp(640, 560, p)
        dill(c, x, FL - abs(math.sin(p * math.pi * 3)) * 10, mood="frozen" if t < 34.0 else "shocked", look=(-1, -0.6),
             arm="down", crown_on=True)
    else:   # eyes wide, gripping the wall
        dill(c, 560, FL, mood="shocked", look=(-1, -0.4), arm="reach", crown_on=True, shake=4 + 4 * seg(t, 35.8, 38.0))
    # Wilt
    droop, pat = 0.0, 0.0
    if 27.2 <= t < 29.6:
        droop = ease(seg(t, 27.2, 27.7)) * (1 - ease(seg(t, 29.2, 29.6)))
        pat = max(0.0, math.sin((t - 27.7) * 2 * math.pi / 0.45)) if 27.7 <= t < 29.1 else 0.0
    wilt(c, 880, FL, droop=droop, pat=pat, look=(-1, 0.4) if t < SHOT_H else (-1, -0.4))
    if 27.7 <= t < 29.1:   # "pat" ticks
        for k in range(3):
            tp = 27.7 + 0.45 * k + 0.1
            if tp <= t < tp + 0.25:
                text(c, "pat", 700, FL - 330, 40, (1, 1, 1), olw=8)
    # wind wisps
    for j in range(3):
        q = ((t - SHOT_G) * 0.35 + j / 3) % 1
        c.set_source_rgba(1, 1, 1, 0.12 * math.sin(math.pi * q)); c.set_line_width(6)
        x0 = lerp(1100, -100, q); y0 = 900 + j * 160
        c.move_to(x0, y0); c.curve_to(x0 - 60, y0 - 20, x0 - 120, y0 + 20, x0 - 180, y0); c.stroke()
    if 29.8 <= t < 30.6:
        s = back_out(seg(t, 29.8, 29.95))
        c.save(); c.translate(640, FL - 430); c.scale(S(s), S(s)); text(c, "!", 0, 0, 110, (1, 1, 1), olw=12); c.restore()
    c.rectangle(-400, -400, W + 800, H + 800); c.set_source_rgba(0.02, 0.06, 0.08, 0.12); c.fill()


def frame(c, t):
    if t >= END_T:
        end_card(c, t, END_T); return
    c.save()
    if t < SHOT_G:
        shelf_scene(c, t)
    else:
        drawer_scene(c, t)
    c.restore()
    if t < 0.12:   # hard pop-in flash on the very first frames (hook)
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.5 * (1 - seg(t, 0, 0.12))); c.fill()
    if SHOT_G <= t < SHOT_G + 0.35:   # fade in from black inside the drawer
        c.rectangle(0, 0, W, H); c.set_source_rgba(0, 0, 0, 1 - seg(t, SHOT_G, SHOT_G + 0.35)); c.fill()
    if t >= END_T - 0.4:
        iris(c, W / 2, H * 0.47, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))
    if SHOT_I <= t < END_T:   # DUN DUN DUNNN
        for i, tp in enumerate((35.85, 36.55, 37.25)):
            if tp <= t:
                sc = back_out(seg(t, tp, tp + 0.15))
                c.save(); c.translate([250, 830, 540][i], [330, 330, 520][i]); c.rotate([-0.12, 0.12, 0.0][i]); c.scale(S(sc), S(sc))
                text(c, "DUNNN!" if i == 2 else "DUN", 0, 0, [110, 110, 150][i], (1, 0.3, 0.3), olw=14); c.restore()
    banner(c, t)


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
