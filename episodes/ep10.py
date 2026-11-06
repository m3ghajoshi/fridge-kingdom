"""FRIDGE KINGDOM — Episode 10: "Hide the Chick". 39.6s, 1080x1920 @ 30fps.

Variant B (cold open): no title card; a small title banner sits across the top for the first 2s.

The door bursts open (choir): everybody runs in circles. Crumb boosts Peep into the milk carton's spout
(squish)... the carton bulges and Peep POPs right back out, dripping milk. The Hand descends. Dill grabs
the napkin and flings it over Peep. The Hand pinches the napkin and lifts it: nothing there! Whip pan:
Peep is sitting on Dill's bare head, eyes shut, posing as his crown. The Hand hovers over them (tick tick);
on its cuff, a rubber-duck cufflink turns its head. The Hand takes Dill's licked-clean butter dish
instead, and returns with a FRESH butter block. Dill is overjoyed. Door closes; everyone collapses (even
the jello sighs). Then a frosty cloud drifts down from a vent in the fridge ceiling and frost creeps
across the back wall. Everyone shivers. Three taps from above: tik... tik... tik. Everyone looks up.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, duck, crown, butter_dish, dark_overlay, ellipse, rrect, star, text, hand,
                 iris, hexc, seg, ease, ease_out, lerp, back_out, INK, GOLD, FLOOR, TOP, W, H, FPS, S)
from ep2 import end_card, jello
from ep5 import JELLO_X
from ep6 import grandma, fridge6, lid_piece
from ep7 import god_rays
from ep8 import shell_half
from ep9 import fat_peep, crumb_bitten, butter_dish_left, GRAN_HEAD
from animate import heart

DUR = 39.6
END_T = 38.0
DIM = 0.18
FAT = 1.5
GSC = 1.35
EGG_X = 900
DISH_X = 420
CARTON_X = 110
NAP_X = 760
NAP_HOME = 900      # folded napkin lying in front of the jello
CR_X = 580          # Crumb's "innocent" spot
DI_X = 1020         # Dill's hiding spot (off-frame during the napkin close-up)
CR2 = 650           # Crumb after stepping aside
PE2 = 830           # Peep after bouncing off Dill
GR_X = 250          # Grandma by the carton
VENT_X = 560

# ---------------- timing ----------------
T_SKID = 3.8
T_BOOST = 4.6
T_IN = 5.2
T_HIDDEN = 5.6
T_POP = 6.6
T_LAND = 7.4
T_FLING = 8.0
T_DRAPE = 8.5
T_H1 = 9.4           # hand comes down for the napkin
T_PINCH = 10.6
T_LIFT = 10.9
T_EMPTY = 11.9       # napkin up: nothing there
T_WHIP = 13.0        # whip pan to Dill
T_HOVER = 14.8
T_CUFF = 16.0        # the cufflink Duck turns its head
T_PEEK = 16.8
T_AWAY = 18.2
T_DGRIP = 19.4
T_DLIFT = 19.7
T_BACK = 21.6
T_SET = 22.6
T_JOY = 23.0
T_CLOSE = 24.6
T_SIGHS = [25.2, 25.6, 26.0, 26.4, 26.9]
T_UP = 27.8          # camera tilts up to the ceiling vent
T_PUFF = 28.6
T_DOWN = 31.4
T_SNEEZE = 33.4
T_TAPS = (34.8, 35.4, 36.0)
T_STING = 36.4


def light_at(t):
    if t < T_CLOSE:
        return lerp(DIM, 1.0, ease(seg(t, 0.0, 0.35)))
    return lerp(1.0, DIM, ease(seg(t, T_CLOSE, T_CLOSE + 0.35)))


def hop(a, b, p, height=200):
    return lerp(a[0], b[0], p), lerp(a[1], b[1], p) - height * math.sin(math.pi * p)


def tremble(t):
    return 4 if seg(t, T_DOWN + 0.6, T_DOWN + 1.0) > 0 and t < T_TAPS[0] else 0


# ---------------- new props ----------------
def carton(c, bulge=0.0, spout_open=0.0):
    """Milk carton (front copy so things can hide behind it); bulge 0..1 puffs it out."""
    c.save(); c.translate(CARTON_X, FLOOR); c.scale(1 + 0.08 * bulge, 1 + 0.04 * bulge)
    c.rectangle(-82, -422, 164, 422); c.set_source_rgb(0.95, 0.95, 1); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.move_to(-82, -422); c.line_to(0, -502); c.line_to(82, -422); c.close_path()
    c.set_source_rgb(*hexc("#4DABF7")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.rectangle(-80, -300, 160, 110); c.set_source_rgb(*hexc("#4DABF7")); c.fill()
    # little milk drop logo
    c.move_to(0, -282); c.curve_to(22, -250, 26, -226, 0, -212); c.curve_to(-26, -226, -22, -250, 0, -282)
    c.set_source_rgb(1, 1, 1); c.fill()
    # spout on the gable peak
    c.save(); c.translate(0, -502)
    rrect(c, -26, -26 - 8 * spout_open, 52, 30 + 8 * spout_open, 6); c.set_source_rgb(*hexc("#E7F5FF")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    ellipse(c, 0, -26 - 8 * spout_open, 20 + 8 * spout_open, 6 + 2 * spout_open, hexc("#1C2541"), lw=4)
    c.restore()
    c.restore()


def napkin_tent(c, x, y, unroll=1.0, wob=0.0):
    """A white napkin draped over something round (a lump with folds)."""
    if unroll <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(S(unroll), S(0.3 + 0.7 * unroll))
    w, h = 150, 300
    c.move_to(-w, 0)
    c.curve_to(-w + 10, -h * 0.55, -w * 0.55, -h + wob * 10, 0, -h)
    c.curve_to(w * 0.55, -h - wob * 10, w - 10, -h * 0.55, w, 0)
    for k in range(5):   # wavy hem
        x0 = w - k * (2 * w / 5)
        c.curve_to(x0 - 20, 14, x0 - 50, -10, x0 - 2 * w / 5, 0)
    c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.set_source_rgba(*hexc("#A5D8FF"), 0.8); c.set_line_width(5)
    for fx in (-90, -20, 60):
        c.move_to(fx, -30); c.curve_to(fx + 10, -110, fx + 20, -170, fx * 0.4, -h + 30); c.stroke()
    # blue checker border stripe
    c.set_source_rgba(*hexc("#4DABF7"), 0.9); c.set_line_width(8)
    c.move_to(-w + 14, -24); c.curve_to(-w * 0.4, -14, w * 0.4, -14, w - 14, -24); c.stroke()
    c.restore()


def napkin_hanging(c, x, top_y, sway=0.0):
    """The napkin pinched at the top, hanging from the Hand's fingertips."""
    c.save(); c.translate(x, top_y); c.rotate(sway)
    c.move_to(-14, 0); c.curve_to(-60, 80, -150, 200, -150, 300)
    for k in range(5):
        x0 = -150 + k * 60
        c.curve_to(x0 + 15, 320, x0 + 45, 290, x0 + 60, 310 if k % 2 == 0 else 300)
    c.curve_to(150, 200, 60, 80, 14, 0); c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.set_source_rgba(*hexc("#A5D8FF"), 0.8); c.set_line_width(5)
    for fx in (-70, 0, 70):
        c.move_to(fx * 0.15, 30); c.curve_to(fx * 0.5, 120, fx, 220, fx * 1.1, 290); c.stroke()
    c.set_source_rgba(*hexc("#4DABF7"), 0.9); c.set_line_width(8)
    c.move_to(-138, 280); c.curve_to(-60, 292, 60, 292, 138, 280); c.stroke()
    c.restore()


def napkin_folded(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(S(s), S(s))
    rrect(c, -70, -26, 140, 26, 6); c.set_source_rgb(1, 1, 1); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.set_source_rgba(*hexc("#4DABF7"), 0.9); c.set_line_width(6); c.move_to(-60, -10); c.line_to(60, -10); c.stroke()
    c.restore()


def napkin_flying(c, x, y, p):
    """Napkin unfurling mid-air (p 0..1)."""
    c.save(); c.translate(x, y); c.rotate(-0.6 + 0.6 * p)
    w = lerp(70, 180, p); h = lerp(26, 120, p)
    c.move_to(-w, 0)
    for k in range(4):
        c.curve_to(-w + (k + 0.3) * w / 2, -h * 0.4 * (1 if k % 2 else -1), -w + (k + 0.7) * w / 2, 0, -w + (k + 1) * w / 2, 0)
    c.line_to(w, -h); c.line_to(-w, -h); c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.restore()


def hand_cuffed(c, x, tip_y, grip=0.0, duck_turn=0.0):
    """The Hand, now with a shirt cuff printed with little rubber ducks and a big Duck cufflink."""
    hand(c, x, tip_y, grip)
    c.save(); c.translate(x, tip_y)
    rrect(c, -128, -425, 256, 110, 26); c.set_source_rgb(*hexc("#F8F0E3")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.set_source_rgba(*hexc("#74C0FC"), 0.6); c.set_line_width(5)
    c.move_to(-120, -407); c.line_to(120, -407); c.move_to(-120, -333); c.line_to(120, -333); c.stroke()
    for dx in (-86, 86):   # printed ducks (profile)
        c.save(); c.translate(dx, -339); c.scale(0.22, 0.22); duck(c, 0, 0, turn=0.0); c.restore()
    # the cufflink: a gold ring with the Duck inside
    ellipse(c, 0, -371, 50, 50, GOLD, lw=6)
    ellipse(c, 0, -371, 40, 40, hexc("#D0EBFF"), stroke=False)
    c.save(); c.rectangle(-40, -411, 80, 80); c.clip()
    c.save(); c.translate(0, -339); c.scale(0.3, 0.3); duck(c, 0, 0, turn=duck_turn); c.restore()
    c.restore()
    c.restore()


def ceiling_vent(c, light):
    """Grille in the fridge ceiling, top of the back wall."""
    c.save(); c.translate(VENT_X, 30)
    rrect(c, -170, -10, 340, 110, 18); c.set_source_rgb(*hexc("#ADB5BD")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    for k in range(5):
        rrect(c, -140, 6 + k * 18, 280, 9, 4); c.set_source_rgb(*hexc("#212529")); c.fill()
    for sx in (-150, 150):
        ellipse(c, sx, 45, 8, 8, hexc("#868E96"), lw=3)
    c.restore()


def frost(c, t, k):
    """Frost creeping across the back wall from the vent (k 0..1 growth)."""
    if k <= 0:
        return
    rnd = random.Random(11)
    R = 1300 * k
    c.save()
    c.rectangle(-400, -100, W + 800, TOP - 10 + 100); c.clip()
    g = cairo.RadialGradient(VENT_X, 40, 0, VENT_X, 40, max(R, 1))
    g.add_color_stop_rgba(0, 0.92, 0.98, 1, 0.75); g.add_color_stop_rgba(0.8, 0.85, 0.95, 1, 0.4); g.add_color_stop_rgba(1, 0.85, 0.95, 1, 0)
    c.rectangle(-400, -100, W + 800, TOP + 100); c.set_source(g); c.fill()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for i in range(46):
        a = rnd.uniform(0.05, math.pi - 0.05); d = rnd.uniform(80, 1200)
        if d > R:
            continue
        fx, fy = VENT_X + math.cos(a) * d * 1.1, 40 + math.sin(a) * d * 0.62
        sz = rnd.uniform(16, 34) * min(1, (R - d) / 120)
        c.save(); c.translate(fx, fy); c.rotate(rnd.uniform(0, 1))
        c.set_source_rgba(1, 1, 1, 1.0); c.set_line_width(6)
        for j in range(6):
            aa = j * math.pi / 3
            c.move_to(0, 0); c.line_to(math.cos(aa) * sz, math.sin(aa) * sz)
            c.move_to(math.cos(aa) * sz * 0.55, math.sin(aa) * sz * 0.55)
            c.line_to(math.cos(aa + 0.5) * sz * 0.8, math.sin(aa + 0.5) * sz * 0.8)
        c.stroke(); c.restore()
    c.restore()
    # frosty rim along the top shelf edge
    if k > 0.6:
        q = (k - 0.6) / 0.4
        for i in range(int(22 * q)):
            x = 30 + i * 48
            c.move_to(x - 14, TOP + 34); c.line_to(x, TOP + 34 + 22 + 10 * (i % 3)); c.line_to(x + 14, TOP + 34); c.close_path()
            c.set_source_rgba(0.9, 0.97, 1, 0.9); c.fill_preserve(); c.set_source_rgba(*INK, 0.6); c.set_line_width(3); c.stroke()


def frost_cloud(c, x, y, s, alpha):
    if alpha <= 0 or s <= 0.02:
        return
    c.push_group()
    for dx, dy, r in [(-90, 10, 70), (-30, -30, 90), (50, -10, 80), (110, 20, 60), (10, 40, 70)]:
        ellipse(c, x + dx * s, y + dy * s, r * s, r * s * 0.8, (0.88, 0.96, 1.0), stroke=False)
    c.save(); c.translate(x, y)
    for dx, dy in [(-60, -20), (40, 20), (90, -30)]:
        star(c, dx * s, dy * s, 10 * s, 0.3, (1, 1, 1))
    c.restore()
    c.pop_group_to_source(); c.paint_with_alpha(0.9 * alpha)


def cloud_pos(t):
    """Frosty cloud (x, y, scale, alpha) or None."""
    if t < T_PUFF:
        return None
    if t < T_DOWN:
        p = seg(t, T_PUFF, T_DOWN)
        return VENT_X + 30 * math.sin(t * 2), lerp(150, 560, ease_out(p)), lerp(0.4, 1.4, ease_out(p)), 1.0
    p = seg(t, T_DOWN, T_DOWN + 2.0)
    return VENT_X + 40 * math.sin(t * 2), lerp(560, FLOOR - 620, ease(p)), lerp(1.4, 2.0, p), 1 - 0.6 * p


def fresh_butter(c, x, y):
    butter_dish(c, x, y)
    c.save(); c.translate(x, y)
    star(c, 60, -112, 16, 0.2, (1, 1, 1))
    c.restore()


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
    text(c, "Ep. 10:  Hide the Chick", W / 2, 182, 46, (1, 1, 1), olw=8)
    c.restore()


# ---------------- character states ----------------
CIRC_C, CIRC_R = 570, 280
PH = {"dill": 0.0, "crumb": math.pi * 0.5, "peep": math.pi, "gran": math.pi * 1.5}


def circle(name, t):
    a = 4.2 * t + PH[name]
    x = CIRC_C + CIRC_R * math.cos(a)
    d = math.sin(a)            # >0: front
    face = -1 if math.sin(a) > 0 else 1   # moving direction (d/dt cos = -sin)
    return x, FLOOR + 30 * d - abs(math.sin(t * 14 + PH[name])) * 24, face, d


def skid(name, t, target):
    x0, y0, _, _ = circle(name, T_SKID)
    p = ease_out(seg(t, T_SKID, T_SKID + 0.5))
    return lerp(x0, target, p), lerp(y0, FLOOR, p)


def dill_state(t):
    """(x, y, kw, depth)"""
    if t < T_SKID:
        x, y, f, d = circle("dill", t)
        return x, y, dict(mood="shocked", look=(f, 0), arm="reach"), d
    if t < 7.4:
        x, y = skid("dill", t, 640)
        mood = "shocked" if t < T_POP else "frozen"
        return x, y, dict(mood=mood, look=(-1, -0.4 if T_BOOST <= t < T_POP else 0), shake=2), 0
    if t < 7.9:      # dashes right to the napkin
        p = ease(seg(t, 7.4, 7.9))
        return lerp(640, NAP_HOME, p), FLOOR - abs(math.sin(p * math.pi * 3)) * 20, dict(mood="shocked", look=(1, 0)), 0
    if t < T_DRAPE:  # flings the napkin
        return NAP_HOME, FLOOR, dict(mood="angry", look=(-1, -0.3), arm="reach"), 0
    if t < 9.0:      # sidesteps out of sight
        p = ease(seg(t, T_DRAPE, 9.0))
        return lerp(NAP_HOME, DI_X, p), FLOOR - abs(math.sin(p * math.pi * 2)) * 14, dict(mood="smug", look=(-1, 0)), 0
    if t < T_WHIP:   # offscreen (whistling innocently)
        return DI_X, FLOOR, dict(mood="smug", look=(-1, 0)), 0
    if t < T_AWAY:   # posing royally with Peep as his "crown"
        sweat = t >= T_PEEK
        return DI_X, FLOOR, dict(mood="proud" if t < T_HOVER else "frozen", look=(0, -1) if T_HOVER <= t < T_AWAY else (-1, 0),
                                 arm="up", shake=1.5 if sweat else 0), 0
    if t < T_DLIFT:
        return DI_X, FLOOR, dict(mood="frozen", look=(-1, 0.2), arm="up"), 0
    if t < T_SET:    # NOOO, my throne
        return DI_X, FLOOR, dict(mood="sad" if t > 20.4 else "shocked", look=(-1, -0.2), arm="reach" if t < 20.4 else "down", shake=3), 0
    if t < T_JOY:
        return DI_X, FLOOR, dict(mood="shocked", look=(-1, 0.3)), 0
    if t < 23.5:     # overjoyed: leaps
        return DI_X, FLOOR - 60 * math.sin(math.pi * seg(t, T_JOY, 23.5)), dict(mood="proud", look=(-1, 0), arm="reach"), 0
    if t < 24.1:     # hop onto the fresh butter throne
        x, y = hop((DI_X, FLOOR), (DISH_X, FLOOR - 110), ease(seg(t, 23.5, 24.1)), 260)
        return x, y, dict(mood="proud", look=(-1, 0), arm="reach"), 0
    if t < T_SIGHS[0]:
        return DISH_X, FLOOR - 110, dict(mood="proud", look=(0, 0), arm="up"), 0
    if t < T_DOWN + 0.6:    # collapses, blissful, on the butter
        return DISH_X, FLOOR - 110, dict(mood="smug", look=(0, 0.3), sq=lerp(1, 0.82, ease(seg(t, T_SIGHS[0], T_SIGHS[0] + 0.3))), rot=0.12), 0
    if t < T_TAPS[0]:       # shivering
        return DISH_X, FLOOR - 110, dict(mood="frozen", look=(0, -0.3), shake=4), 0
    lk = (0, -1) if t >= T_TAPS[0] + 0.15 else (0, 0)
    return DISH_X, FLOOR - 110, dict(mood="shocked", look=lk, shake=1.5 if t < T_STING else 0), 0


def crumb_state(t):
    if t < T_SKID:
        x, y, f, d = circle("crumb", t)
        return x, y, dict(mood="scared", look=(f, 0)), d
    if t < T_BOOST:
        x, y = skid("crumb", t, 270)
        return x, y, dict(mood="worried", look=(1, 0) if t < 4.2 else (-1, -0.5), arm="wave" if t > 4.3 else "down"), 0
    if t < T_HIDDEN:   # boosts Peep up to the spout
        return 270, FLOOR - 20 * math.sin(math.pi * seg(t, T_BOOST, T_BOOST + 0.3)), dict(mood="worried", look=(-1, -1), arm="wave"), 0
    if t < T_POP:      # phew
        return 270, FLOOR, dict(mood="sheepish", look=(-1, -0.6)), 0
    if t < 7.6:        # it pops right back out
        return 270, FLOOR - 30 * math.sin(math.pi * seg(t, T_POP, T_POP + 0.3)), dict(mood="scared", look=(1, -0.6) if t > 6.9 else (-1, -1), shake=4), 0
    if t < 8.4:        # shuffles to his innocent spot
        p = ease(seg(t, 7.6, 8.4))
        return lerp(270, CR_X, p), FLOOR - abs(math.sin(p * math.pi * 3)) * 14, dict(mood="scared", look=(1, 0)), 0
    if t < T_EMPTY:    # innocently looking up at the Hand
        return CR_X, FLOOR, dict(mood="sheepish" if t < T_H1 else "worried", look=(0.6, -1) if t > T_H1 else (1, 0)), 0
    if t < T_WHIP:     # it's empty!
        return CR_X, FLOOR - 26 * math.sin(math.pi * seg(t, T_EMPTY, T_EMPTY + 0.35)), dict(mood="scared", look=(1, 0.4)), 0
    if t < T_SIGHS[1]:
        if t < T_JOY:
            return CR_X, FLOOR, dict(mood="worried", look=(1, -0.5) if t < T_AWAY else (-1, -0.3)), 0
        p = ease(seg(t, T_JOY, T_JOY + 0.5))   # steps aside for Dill's leap
        return lerp(CR_X, CR2, p), FLOOR - 20 * math.sin(math.pi * p), dict(mood="sheepish", look=(-1, -0.3)), 0
    if t < T_DOWN + 0.6:   # flops back, exhausted
        p = ease(seg(t, T_SIGHS[1], T_SIGHS[1] + 0.35))
        return CR2, FLOOR, dict(mood="sheepish", look=(0, -1), rot=0.3 * p), 0
    if t < T_TAPS[0]:
        return CR2, FLOOR, dict(mood="worried", look=(0, -0.3), shake=4), 0
    lk = (0, -1) if t >= T_TAPS[0] + 0.25 else (0, 0)
    return CR2, FLOOR, dict(mood="scared", look=lk, shake=1.5 if t < T_STING else 0), 0


def peep_state(t):
    """(x, y, kw, depth, squeeze_x, squeeze_y, behind_carton)"""
    if t < T_SKID:
        x, y, f, d = circle("peep", t)
        return x, y, dict(mood="happy", face=f, wings="flap", flap_t=t), d, 1, 1, False
    if t < T_BOOST:
        x, y = skid("peep", t, 380)
        return x, y, dict(mood="happy", face=-0.5, look=(-1, 0)), 0, 1, 1, False
    if t < T_IN:       # boosted up onto the spout
        x, y = hop((380, FLOOR), (CARTON_X, FLOOR - 520), ease(seg(t, T_BOOST, T_IN)), 160)
        return x, y, dict(mood="happy", wings="flap", flap_t=t), 0, 1, 1, False
    if t < T_POP:      # squished down into the carton
        p = ease(seg(t, T_IN, T_HIDDEN))
        k = int(t * 12) % 2
        return CARTON_X, lerp(FLOOR - 520, FLOOR - 180, p), dict(mood="shock" if p < 1 else "blink", sq=1.0), 0, lerp(1, 0.5, p), lerp(1, 1.1, p), True
    if t < T_LAND:     # POP: shoots out and lands
        x, y = hop((CARTON_X, FLOOR - 520), (NAP_X, FLOOR), seg(t, T_POP, T_LAND), 380)
        return x, y, dict(mood="chirp", wings="flap", flap_t=t, rot=(t - T_POP) * 8), 0, lerp(0.6, 1, seg(t, T_POP, T_POP + 0.2)), 1, t < T_POP + 0.15
    if t < T_DRAPE:
        return NAP_X, FLOOR, dict(mood="happy" if t > T_LAND + 0.25 else "chirp", face=0.4, look=(0, 0),
                                  sq=lerp(0.8, 1, seg(t, T_LAND, T_LAND + 0.25))), 0, 1, 1, False
    if t < T_WHIP:     # under the napkin (hidden)
        return None
    if t < T_JOY:      # perched on Dill's head, posing as his crown
        mood = "blink" if t < T_PEEK or t > 17.3 else "proud"
        return DI_X, FLOOR - 296, dict(mood=mood, face=0, look=(-1, 0)), 0, 0.82, 0.82, False
    if t < 23.6:       # bounced off by Dill's leap
        x, y = hop((DI_X, FLOOR - 296), (PE2, FLOOR), seg(t, T_JOY, 23.6), 200)
        return x, y, dict(mood="happy", wings="flap", flap_t=t), 0, 1, 1, False
    if t < T_SIGHS[3]:
        return PE2, FLOOR, dict(mood="happy", face=-0.5, look=(-1, 0)), 0, 1, 1, False
    if t < T_DOWN + 0.6:   # flops onto its back
        p = ease(seg(t, T_SIGHS[3], T_SIGHS[3] + 0.3))
        return PE2, FLOOR, dict(mood="blink", face=0, rot=0.45 * p), 0, 1, 1, False
    if t < T_SNEEZE:
        return PE2, FLOOR, dict(mood="blink", face=0, shake=4), 0, 1, 1, False
    if t < T_SNEEZE + 0.6:
        return PE2, FLOOR, dict(mood="sneeze", face=-0.4, rot=-0.15, shake=3), 0, 1, 1, False
    if t < T_TAPS[0]:
        return PE2, FLOOR, dict(mood="blink" if int(t * 3) % 2 else "happy", face=0, shake=2), 0, 1, 1, False
    lk = (0, -1) if t >= T_TAPS[0] + 0.3 else (0, 0)
    return PE2, FLOOR, dict(mood="shock" if t < T_STING + 0.6 else "happy", face=0, look=lk), 0, 1, 1, False


def gran_state(t):
    """(x, y, kw, depth)"""
    if t < T_SKID:
        x, y, f, d = circle("gran", t)
        return x, y, dict(look=(f, 0), cane="up", mood="shock", step=t * 3), d
    if t < 7.6:
        x, y = skid("gran", t, 470)
        return x, y, dict(look=(-1, -0.4), cane="down", mood="shock" if T_POP <= t < 7.4 else "stern"), 0
    if t < 8.6:      # hobbles quickly to her innocent spot
        p = ease(seg(t, 7.6, 8.6))
        return lerp(470, GR_X, p), FLOOR, dict(look=(-1, 0), cane="down", mood="stern", step=t * 4), 0
    if t < T_SIGHS[2]:
        return GR_X, FLOOR, dict(look=(1, -0.3), cane="down", mood="stern"), 0
    if t < T_DOWN + 0.6:   # sits down hard, eyes shut
        return GR_X, FLOOR, dict(look=(1, 0), cane="down", mood="closed", bow=0.25 * ease(seg(t, T_SIGHS[2], T_SIGHS[2] + 0.3))), 0
    if t < T_TAPS[0]:
        return GR_X, FLOOR, dict(look=(1, -0.3), cane="down", mood="stern"), 0
    return GR_X, FLOOR, dict(look=(1, -1) if t >= T_TAPS[0] + 0.2 else (1, 0), cane="up" if t >= T_STING else "down",
                             mood="shock" if t >= T_TAPS[0] else "stern"), 0


def hand_state(t):
    """(x, tip_y, grip, carry) or None.  carry in (None, 'napkin', 'dish', 'fresh')."""
    if 7.6 <= t < T_H1:          # descending, high up
        return NAP_X + 40, lerp(-700, FLOOR - 820, ease_out(seg(t, 7.6, T_H1))), 0.0, None
    if T_H1 <= t < T_PINCH:      # down to the napkin
        return NAP_X + 20 * (1 - seg(t, T_H1, T_PINCH)), lerp(FLOOR - 820, FLOOR - 300, ease(seg(t, T_H1, T_PINCH))), 0.0, None
    if T_PINCH <= t < T_LIFT:
        return NAP_X, FLOOR - 300, ease(seg(t, T_PINCH, T_LIFT)), None
    if T_LIFT <= t < T_WHIP:     # lifts it: nothing! then searches side to side
        y = lerp(FLOOR - 300, FLOOR - 720, ease(seg(t, T_LIFT, T_EMPTY)))
        x = NAP_X + 60 * math.sin((t - T_EMPTY) * 5) * seg(t, T_EMPTY + 0.2, T_EMPTY + 0.5)
        return x, y, 1.0, "napkin"
    if T_WHIP <= t < T_HOVER:    # drops the napkin, drifts over to Dill
        p = ease(seg(t, T_WHIP + 0.4, T_HOVER))
        return lerp(NAP_X, DI_X, p), lerp(FLOOR - 720, FLOOR - 620, p), 1.0 - ease(seg(t, T_WHIP, T_WHIP + 0.3)), None
    if T_HOVER <= t < T_AWAY:    # hovers over Peep; finger lowers... tick, tick
        dip = 50 * ease(seg(t, 17.2, 17.8))
        return DI_X + 6 * math.sin(t * 3), FLOOR - 620 + dip, 0.0, None
    if T_AWAY <= t < T_DGRIP:    # swerves to the empty butter dish
        p = ease(seg(t, T_AWAY, T_DGRIP))
        return lerp(DI_X, DISH_X, p), lerp(FLOOR - 570, FLOOR - 120, p) - 200 * math.sin(math.pi * p), 0.0, None
    if T_DGRIP <= t < T_DLIFT:
        return DISH_X, FLOOR - 120, ease(seg(t, T_DGRIP, T_DLIFT)), "dish"
    if T_DLIFT <= t < 20.8:
        return DISH_X, lerp(FLOOR - 120, -700, ease(seg(t, T_DLIFT, 20.8))), 1.0, "dish"
    if T_BACK <= t < T_SET:      # returns with a fresh butter block
        return DISH_X, lerp(-700, FLOOR - 120, ease(seg(t, T_BACK, T_SET))), 1.0, "fresh"
    if T_SET <= t < T_SET + 0.3:
        return DISH_X, FLOOR - 120, 1 - ease(seg(t, T_SET, T_SET + 0.3)), None
    if T_SET + 0.3 <= t < T_CLOSE:
        return DISH_X, lerp(FLOOR - 120, -800, ease(seg(t, T_SET + 0.3, T_CLOSE))), 0.0, None
    return None


def napkin_state(t):
    """('folded'|'flying'|'tent'|'hang'|None, x, y, p)"""
    if t < 7.9:
        return "folded", NAP_HOME, FLOOR, 0
    if t < T_FLING:
        return "folded", NAP_HOME - 30 * seg(t, 7.9, T_FLING), FLOOR - 140 * seg(t, 7.9, T_FLING), 0
    if t < T_DRAPE:
        p = seg(t, T_FLING, T_DRAPE)
        x, y = hop((NAP_HOME - 30, FLOOR - 140), (NAP_X, FLOOR - 200), p, 260)
        return "flying", x, y, p
    if t < T_LIFT:
        return "tent", NAP_X, FLOOR, back_out(seg(t, T_DRAPE, T_DRAPE + 0.25))
    if t < T_WHIP:
        return None   # in the Hand (drawn with it)
    if t < T_WHIP + 0.8:   # dropped: flutters down
        p = seg(t, T_WHIP, T_WHIP + 0.8)
        return "flying", NAP_X - 30 + 40 * math.sin(p * 6), lerp(FLOOR - 450, FLOOR - 20, ease(p)), 1 - p * 0.6
    return "flat", NAP_X - 30, FLOOR, 0


# ---------------- camera ----------------
def camera(t):
    cx, cy, z = 560, FLOOR - 330, 1.3
    # carton close-up
    k = ease(seg(t, T_SKID, T_SKID + 0.6)) * (1 - ease(seg(t, T_POP + 0.2, T_LAND)))
    cx, cy, z = lerp(cx, 230, k), lerp(cy, FLOOR - 400, k), lerp(z, 1.75, k)
    # napkin close-up (Dill is just out of frame on the right)
    k2 = ease(seg(t, T_DRAPE - 0.1, T_DRAPE + 0.5)) * (1 - ease(seg(t, T_WHIP, T_WHIP + 0.35)))
    cx, cy, z = lerp(cx, 700, k2), lerp(cy, FLOOR - 400, k2), lerp(z, 2.0, k2)
    # whip pan to Dill with Peep on his head
    k3 = ease(seg(t, T_WHIP, T_WHIP + 0.35)) * (1 - ease(seg(t, T_AWAY, T_AWAY + 0.6)))
    cx, cy, z = lerp(cx, 880, k3), lerp(cy, FLOOR - 540, k3), lerp(z, 1.7, k3)
    # wide for the dish swap (everyone in frame)
    kw = ease(seg(t, T_AWAY, T_AWAY + 0.6))
    cx, cy, z = lerp(cx, 700, kw), lerp(cy, FLOOR - 360, kw), lerp(z, 1.3, kw)
    # then frame the throne
    k4 = ease(seg(t, T_JOY + 0.3, T_JOY + 1.2))
    cx, cy, z = lerp(cx, 600, k4), lerp(cy, FLOOR - 320, k4), lerp(z, 1.32, k4)
    # tilt up to the ceiling vent, then follow the cloud down
    k5 = ease(seg(t, T_UP, T_UP + 0.9)) * (1 - ease(seg(t, T_DOWN, T_DOWN + 1.4)))
    cx, cy, z = lerp(cx, VENT_X, k5), lerp(cy, 400, k5), lerp(z, 1.5, k5)
    if t >= T_TAPS[0]:   # push in on the faces looking up
        k6 = ease(seg(t, T_TAPS[0], END_T))
        cx, cy, z = lerp(cx, 540, k6), lerp(cy, FLOOR - 420, k6), lerp(z, 1.55, k6)
    if T_POP <= t < T_POP + 0.3:
        s = 12 * (1 - seg(t, T_POP, T_POP + 0.3)); cx += random.uniform(-s, s); cy += random.uniform(-s, s)
    if T_SET <= t < T_SET + 0.25:
        s = 10 * (1 - seg(t, T_SET, T_SET + 0.25)); cy += random.uniform(-s, s)
    if T_CLOSE <= t < T_CLOSE + 0.3:
        s = 14 * (1 - seg(t, T_CLOSE, T_CLOSE + 0.3)); cx += random.uniform(-s, s); cy += random.uniform(-s, s)
    for tt in T_TAPS:
        if tt <= t < tt + 0.2:
            cy += random.uniform(-6, 6)
    return cx, cy, z


# ---------------- scene ----------------
def word(c, t, s, x, y, size, col, t0, t1, rot=0.0):
    if t0 <= t < t1:
        k = back_out(seg(t, t0, t0 + 0.2))
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(k), S(k)); text(c, s, 0, 0, size, col, olw=10); c.restore()


def draw_peep(c, ps):
    x, y, kw, _, sx, sy, _ = ps
    c.save(); c.translate(x, y); c.scale(S(sx), S(sy)); c.translate(-x, -y)
    fat_peep(c, x, y, FAT, **kw)
    c.restore()


def draw_gran(c, gs, t):
    x, y, kw, _ = gs
    c.save(); c.translate(x, y); c.scale(GSC, GSC); c.translate(-x, -y)
    grandma(c, x, y, **kw)
    c.restore()
    bob = 0.0 if t >= T_SKID else 0
    crown(c, x + GRAN_HEAD[0] + (14 if kw.get("bow", 0) > 0.1 else 0), y + GRAN_HEAD[1] + bob + (12 if kw.get("bow", 0) > 0.1 else 0), 0.72, -0.2)


def scene(c, t):
    L = light_at(t)
    fridge6(c, L, 0, lid=False)
    god_rays(c, L)
    lid_piece(c, 760, TOP - 25, 0.0)
    shell_half(c, EGG_X, TOP - 70, 0.0, top=False)
    ceiling_vent(c, L)
    fk = ease(seg(t, T_PUFF + 0.3, T_DOWN + 1.5)) if t >= T_PUFF else 0
    frost(c, t, fk)

    sigh_wob = 0.1 * math.sin((t - T_SIGHS[4]) * 14) * (1 - seg(t, T_SIGHS[4], T_SIGHS[4] + 0.8)) if t >= T_SIGHS[4] else 0
    jello(c, JELLO_X, FLOOR, sigh_wob if t >= T_SIGHS[4] else (0.06 * math.sin(t * 22) if t < T_SKID else 0))

    # butter dish (empty -> taken -> fresh)
    if t < T_DGRIP:
        butter_dish_left(c, DISH_X, FLOOR, 0.0)
    elif t >= T_SET:
        fresh_butter(c, DISH_X, FLOOR)

    ns = napkin_state(t)
    if ns and ns[0] == "folded":
        napkin_folded(c, ns[1], ns[2])
    elif ns and ns[0] == "flying" and t >= T_WHIP:
        napkin_flying(c, ns[1], ns[2], ns[3])
    elif ns and ns[0] == "flat":
        c.save(); c.translate(ns[1], ns[2]); c.scale(2.2, 0.8); napkin_folded(c, 0, 0); c.restore()

    ds, cs, ps, gs = dill_state(t), crumb_state(t), peep_state(t), gran_state(t)
    hs = hand_state(t)

    def draw_dill():
        x, y, kw, _ = ds
        dill(c, x, y, crown_on=False, **kw)

    def draw_crumb():
        crumb_bitten(c, cs[0], cs[1], 1.0, **cs[2])

    items = [(ds[3], draw_dill), (cs[3], draw_crumb), (gs[3], lambda: draw_gran(c, gs, t))]
    peep_behind = ps is not None and ps[6]
    peep_on_head = ps is not None and T_WHIP <= t < T_JOY
    if ps is not None and not peep_behind and not peep_on_head:
        items.append((ps[3] + 0.001, lambda: draw_peep(c, ps)))
    if peep_behind:
        draw_peep(c, ps)
    carton(c, bulge=max(0, math.sin(math.pi * seg(t, 5.9, 6.2))) + max(0, math.sin(math.pi * seg(t, 6.25, 6.6))) * 1.4 +
           (0.6 * math.sin(math.pi * seg(t, T_IN, T_HIDDEN))), spout_open=1.0 if T_IN <= t < T_POP + 0.3 else 0.0)

    # hand behind the characters while lowering the napkin search; carried items in front of the hand
    if hs:
        hx, tip, grip, carry = hs
        hand_cuffed(c, hx, tip, grip, duck_turn=ease(seg(t, T_CUFF, T_CUFF + 0.4)) * (1 - ease(seg(t, T_AWAY, T_AWAY + 0.4))))
        if carry == "napkin":
            napkin_hanging(c, hx - 30, tip - 10, 0.08 * math.sin(t * 4))
        elif carry == "dish":
            butter_dish_left(c, DISH_X, tip + 120, 0.0)
        elif carry == "fresh":
            fresh_butter(c, DISH_X, tip + 120)

    for _, fn in sorted(items, key=lambda it: it[0]):
        fn()
    if peep_on_head:
        draw_peep(c, ps)

    if ns and ns[0] == "flying" and t < T_WHIP:
        napkin_flying(c, ns[1], ns[2], ns[3])
    elif ns and ns[0] == "tent":
        napkin_tent(c, ns[1], ns[2], ns[3], wob=math.sin(t * 6) * (1 if t < T_H1 else 0))

    # ---- effects ----
    if t < T_SKID:   # panic dust + screams
        for j in range(5):
            q = (t * 2 + j / 5) % 1
            ellipse(c, CIRC_C - 300 + j * 150, FLOOR - 10 - q * 40, 30 * (1 - q) + 6, 16 * (1 - q) + 4, (1, 1, 1), stroke=False)
        word(c, t, "AAAH!", 330, FLOOR - 520, 56, (1, 1, 1), 0.3, 1.4, -0.1)
        word(c, t, "EEEK!", 800, FLOOR - 560, 52, hexc("#FFE680"), 1.6, 2.8, 0.1)
        word(c, t, "peep!", 560, FLOOR - 470, 38, hexc("#FFE680"), 2.9, 3.6, -0.05)
    word(c, t, "SQUISH", 110, FLOOR - 700, 50, (1, 1, 1), T_IN + 0.05, T_HIDDEN + 0.4, -0.1)
    if T_HIDDEN + 0.2 <= t < T_POP:   # phew
        word(c, t, "phew", 290, FLOOR - 430, 34, (1, 1, 1), T_HIDDEN + 0.2, T_POP, 0.1)
    if T_POP <= t < T_POP + 0.6:     # milk splash from the spout
        q = seg(t, T_POP, T_POP + 0.6)
        for i in range(8):
            a = -math.pi * (0.1 + 0.8 * i / 7)
            ellipse(c, CARTON_X + math.cos(a) * 160 * q, FLOOR - 540 + math.sin(a) * 160 * q + 260 * q * q, 12, 15, (1, 1, 1), lw=3)
        word(c, t, "POP!", 230, FLOOR - 720, 66, (1, 1, 1), T_POP, T_POP + 0.6, 0.12)
    if T_LAND <= t < T_DRAPE + 2:    # milk drips off Peep's helmet
        q = (t * 1.6) % 1
        if t < T_DRAPE:
            ellipse(c, NAP_X - 40, FLOOR - 250 + q * 60, 7, 10, (1, 1, 1), lw=3)
        word(c, t, "peep!", NAP_X + 80, FLOOR - 340, 38, hexc("#FFE680"), T_LAND + 0.1, T_LAND + 0.6, 0.1)
    word(c, t, "WHOOSH", NAP_X + 80, FLOOR - 420, 44, (1, 1, 1), T_FLING, T_DRAPE + 0.3, -0.08)
    if 8.6 <= t < T_H1:   # innocent whistle notes from Crumb
        for j in range(2):
            q = ((t - 8.6) * 1.2 + j / 2) % 1
            text(c, "~", CR_X - 40 + 40 * q, FLOOR - 330 - 80 * q, 40, (1, 1, 1), olw=6)
    if T_EMPTY <= t < T_WHIP:   # GASP / ?
        word(c, t, "GASP!", CR_X, FLOOR - 430, 50, (1, 1, 1), T_EMPTY, T_EMPTY + 0.7, -0.1)
        k = back_out(seg(t, T_EMPTY + 0.4, T_EMPTY + 0.6))
        if t >= T_EMPTY + 0.4:
            c.save(); c.translate(NAP_X, FLOOR - 130); c.scale(S(k), S(k)); text(c, "?", 0, 0, 110, hexc("#FFE680"), olw=12); c.restore()
    if T_WHIP + 0.35 <= t < T_HOVER:   # the "jewel" sparkle
        star(c, DI_X + 60, FLOOR - 520, 28 * math.sin(math.pi * seg(t, T_WHIP + 0.35, T_WHIP + 0.9)), t * 5, (1, 1, 1))
    if T_HOVER <= t < T_AWAY:          # tick-tick
        for i, t0 in enumerate([15.0, 15.6, 16.2, 16.8, 17.4]):
            word(c, t, "tick" if i % 2 == 0 else "tock", DI_X - 230 + 60 * (i % 2), FLOOR - 360 - 50 * (i % 2), 32, (1, 1, 1), t0, t0 + 0.45, 0.1 * (-1) ** i)
        if t >= T_PEEK:   # sweat drops
            q = (t * 2) % 1
            ellipse(c, DI_X - 80, FLOOR - 250 + q * 50, 9, 13, hexc("#74C0FC"), lw=3)
            ellipse(c, DI_X + 80, FLOOR - 220 + ((q + 0.5) % 1) * 50, 9, 13, hexc("#74C0FC"), lw=3)
    if T_CUFF <= t < T_CUFF + 0.6 and hs:   # tiny sparkle as the cufflink Duck turns
        star(c, hs[0] + 60, hs[1] - 425, 16 * math.sin(math.pi * seg(t, T_CUFF, T_CUFF + 0.6)), t * 4, (1, 1, 1))
    word(c, t, "NOOO!", DI_X - 230, FLOOR - 600, 50, hexc("#FF8787"), T_DLIFT + 0.2, 21.0, -0.1)
    word(c, t, "CLUNK", DISH_X, FLOOR - 300, 48, (1, 1, 1), T_SET, T_SET + 0.6, 0.1)
    if T_JOY <= t < T_CLOSE:   # joy: hearts + sparkles
        for j in range(4):
            q = ((t - T_JOY) * 1.2 + j / 4) % 1
            heart(c, (DISH_X if t > 24.1 else DI_X) + 80 * math.sin(j * 2 + q * 4), FLOOR - 330 - q * 180, 1.1, 1 - q)
        if t >= 24.1:
            star(c, DISH_X - 140, FLOOR - 330, 22 * abs(math.sin(t * 6)), t * 3, GOLD)
            star(c, DISH_X + 140, FLOOR - 380, 18 * abs(math.sin(t * 6 + 1)), -t * 3, GOLD)
    for i, ts in enumerate(T_SIGHS):   # five sighs (the fifth is the jello's)
        if ts <= t < ts + 0.9:
            q = seg(t, ts, ts + 0.9)
            sx = [DISH_X, CR2, GR_X, PE2, JELLO_X][i]
            sy = [FLOOR - 400, FLOOR - 180, FLOOR - 300, FLOOR - 180, FLOOR - 220][i]
            ellipse(c, sx + 30 * q, sy - 60 * q, 26 + 20 * q, 18 + 12 * q, (1, 1, 1), stroke=False)
            word(c, t, "sigh", sx + 50, sy - 90, 30, (1, 1, 1), ts, ts + 0.9, 0.08 * (-1) ** i)
    cp = cloud_pos(t)
    if cp:
        frost_cloud(c, cp[0], cp[1], cp[2], cp[3])
    if t >= T_PUFF and t < T_DOWN:
        word(c, t, "fssshh", VENT_X + 220, 200, 36, hexc("#D0EBFF"), T_PUFF, T_PUFF + 1.2, 0.1)
    if T_DOWN + 0.6 <= t < T_TAPS[0]:   # cold breath puffs + chattering
        for j, (bx, by) in enumerate([(DISH_X + 60, FLOOR - 330), (CR2 + 40, FLOOR - 230), (GR_X + 30, FLOOR - 250)]):
            q = ((t * 1.3) + j / 3) % 1
            ellipse(c, bx + 40 * q, by - 30 * q, 14 + 14 * q, 10 + 8 * q, (0.9, 0.97, 1), stroke=False)
        word(c, t, "brrr", CR2 + 60, FLOOR - 420, 36, hexc("#D0EBFF"), T_DOWN + 0.8, T_SNEEZE, -0.1)
    word(c, t, "A-CHOO!", PE2 + 40, FLOOR - 360, 46, hexc("#FFE680"), T_SNEEZE, T_SNEEZE + 0.7, 0.12)
    for i, tt in enumerate(T_TAPS):    # frost dust shaken down from the ceiling
        if tt <= t < tt + 0.8:
            q = seg(t, tt, tt + 0.8)
            for j in range(6):
                ellipse(c, 300 + j * 90 + 20 * i, 600 + q * 500 + 30 * (j % 2), 5, 5, (0.95, 0.98, 1), stroke=False)
    dark_overlay(c, L)


def frame(c, t):
    if t >= END_T:
        end_card(c, t, END_T); return
    random.seed(int(t * 30))
    cx, cy, Z = camera(t)
    c.save()
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    scene(c, t)
    c.restore()
    if t < 0.12:   # hook flash: the door bursts open
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.7 * (1 - seg(t, 0, 0.12))); c.fill()
    if T_WHIP <= t < T_WHIP + 0.35:   # whip-pan streaks
        a = math.sin(math.pi * seg(t, T_WHIP, T_WHIP + 0.35))
        for i in range(8):
            c.rectangle(0, 200 + i * 210, W, 18); c.set_source_rgba(1, 1, 1, 0.35 * a); c.fill()
    if T_CLOSE <= t < T_CLOSE + 0.12:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0, 0, 0, 0.5 * (1 - seg(t, T_CLOSE, T_CLOSE + 0.12))); c.fill()
    word(c, t, "THUD", W / 2, 520, 110, (1, 1, 1), T_CLOSE, T_CLOSE + 0.6, -0.06)
    for i, tt in enumerate(T_TAPS):   # tik tik tik from above
        if tt <= t < END_T:
            k = back_out(seg(t, tt, tt + 0.15))
            c.save(); c.translate([300, 560, 800][i], 300 + 30 * (i % 2)); c.rotate([-0.12, 0.05, 0.14][i]); c.scale(S(k), S(k))
            text(c, "tik", 0, 0, 96, hexc("#D0EBFF"), olw=12); c.restore()
    if t >= T_STING:   # ominous blue tint
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.3, 0.6, 1.0, 0.12 * ease(seg(t, T_STING, T_STING + 0.3))); c.fill()
    if t >= END_T - 0.4:
        iris(c, W / 2, H * 0.55, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))
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
