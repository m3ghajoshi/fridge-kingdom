"""FRIDGE KINGDOM — Episode 17: "The Expedition Plan". 40.0s, 1080x1920 @ 30fps.

Variant A (title card first): 2s "FRIDGE KINGDOM" title card, then the story.

War room on the bottom shelf: Dill's map of the fridge (arrow UP to the freezer) hangs from the icicles under the
top shelf. Dill hops and smacks it (TAP TAP TAP); Crumb nods at everything, Peep nods bigger. Chip shakes his
head no; Dill glares; Chip nods very fast (eep). Dill raises his sword: CHARGE!
Costume montage (cha-ching x4): Crumb gets a blue-striped napkin scarf; Peep's eggshell helmet is polished to a
shine; Wilt's floppy top pokes up from the crisper drawer and flicks a lettuce-leaf cape onto Chip (Chip blushes,
one drip); Dill gets a purple grape-skin parka with a hood and poses.
Grandma Gherkin (still wearing Dill's crown) parachutes down on her shawl and inspects the troops: Peep salutes,
she tugs Crumb's scarf tight (gk), pokes Chip's cape. Then she zips over to Dill, who puffs out his chest... she
springs up and BONKs his hood down over his eyes. Dill stumbles blind and walks into the hanging map (thunk).
Problem: Chip's thought bubble: the freezer door won't budge when a little cube pushes it (X); only the Hand can
open it. Everyone thinks (tick... tock...), Dill paces, question marks.
Lightbulb (DING): Dill remembers Ep 7 (bubble: the Duck squeaks, the Hand comes). He slowly turns... to the Duck,
which is sitting on top of the jello (towel turban and cap crown, still frosty). Everyone follows his gaze.
The Duck's one motion: it slowly tilts its head down toward Dill and shifts its eyes. A long stare. Dill sweats,
gulps. The Duck's eye glints. DUN DUN DUNNN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crown, hand, dark_overlay, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp,
                 back_out, bubble, INK, GOLD, TOP, FLOOR, W, H, FPS, S)
from ep2 import end_card, jello
from ep6 import grandma, fridge6, wilt
from ep7 import plan_icon
from ep8 import shell_half
from ep9 import fat_peep, crumb_bitten, GRAN_HEAD
from ep10 import ceiling_vent, frost, carton, CARTON_X
from ep12 import squash_at, word, hop
from ep13 import ceiling, bubble_r
from ep14 import clean_duck
from ep15 import chip, drop, frost_drawing
from ep16 import scroll_map, butter_rink, plate, keyed, MAP_W, MAP_H, DISH
from animate import heart

DUR = 40.0
T_START = 2.0
END_T = 38.5
DIM = 0.18
FAT = 1.5
GSC = 1.35
CHS = 1.3
ICE = hexc("#D0EBFF")
ICE_B = hexc("#74C0FC")
GRAPE = hexc("#862E9C")
GRAPE_L = hexc("#B65FCF")
GRAPE_D = hexc("#5F1F70")
LETTUCE = hexc("#A9E34B")
LETTUCE_D = hexc("#5C940D")
NAP_B = hexc("#4DABF7")

# ---------------- timing ----------------
TAPS = (2.35, 3.0, 3.65)        # Dill smacks the map
T_NO = 4.35                     # Chip shakes his head no
T_GLARE = 5.1                   # Dill glares
T_YES = 5.6                     # Chip nods very fast
T_CHARGE = 6.4                  # Dill raises his sword
T_C1 = 7.5                      # cha-ching 1: Crumb's napkin scarf
T_C2 = 9.3                      # cha-ching 2: Peep's polished helmet
T_WUP = 11.0                    # Wilt pokes up
T_C3 = 11.6                     # cha-ching 3: lettuce cape on Chip
T_WDOWN = 12.4
T_C4 = 13.3                     # cha-ching 4: Dill's grape-skin parka
T_GSTEP = 15.1                  # Grandma steps off the top shelf
T_GLAND = 16.4
T_INS1 = 16.6                   # Peep
T_INS2 = 17.3                   # Crumb (scarf tug)
T_INS3 = 18.0                   # Chip
T_ZIP = 18.6                    # zips over to Dill
T_ZIPEND = 18.9
T_PUFF = 19.0                   # Dill puffs out his chest
T_BONK = 19.75                  # BONK: hood over his eyes
T_THUNK = 20.9                  # Dill walks into the map
T_HOODUP = 21.5
T_PROB = 21.9                   # Chip's bubble: the freezer door
T_HAND = 23.4                   # only the Hand opens it
T_THINK = 25.0                  # everyone thinks
T_BULB = 28.5                   # DING
T_FLASH = 28.9                  # Dill's bubble: squeak the Duck -> the Hand comes
T_TURN = 31.3                   # Dill slowly turns to the Duck
T_FOLLOW = 31.9                 # everyone follows his gaze
T_DUCK = 33.0                   # the Duck's one motion
T_SWEAT = 35.0
T_GULP = 35.7
T_GLINT = 36.4
DUNS = (37.0, 37.4, 37.8)

# ---------------- layout ----------------
CHX, CRX, PEX, DIX = 160, 330, 520, 790     # Chip, Crumb, Peep, Dill on the bottom shelf
MAPX, MAPY, MAPS = 655, 905, 0.8            # hanging map: top centre, scale
JX = 985                                    # jello (the Duck sits on top)
DUCK_S = 0.78
GR0 = (990, TOP)                            # Grandma on the top shelf
GLAND = 640
WX = 250                                    # Wilt peeks up behind Chip


# ---------------- new props / costumes ----------------
def poof(c, x, y, t, t0, s=1.0):
    """Montage puff cloud."""
    if not (t0 <= t < t0 + 0.45):
        return
    q = seg(t, t0, t0 + 0.45)
    for j in range(7):
        a = j * 2 * math.pi / 7 + 0.3
        r = (40 + 90 * q) * s
        ellipse(c, x + math.cos(a) * r, y + math.sin(a) * r * 0.8, (46 - 30 * q) * s, (40 - 26 * q) * s,
                (1, 1, 1), stroke=False)
    c.save(); c.set_source_rgba(1, 1, 1, 0.9 * (1 - q)); c.arc(x, y, 80 * s * (1 - q) + 1, 0, 2 * math.pi); c.fill(); c.restore()


def scarf(c, x, y, tight=0.0, flap=0.0):
    """Blue-striped napkin scarf on Crumb. tight 0..1 squeezes it in (Grandma's tug)."""
    c.save(); c.translate(x, y)
    hw = 80 - 10 * tight
    yt, yb = -96 + 4 * tight, -62 - 4 * tight
    # tail hanging down the right side
    c.move_to(30, yb - 4); c.line_to(62 + 8 * flap, -8); c.line_to(32 + 8 * flap, -2); c.line_to(14, yb - 2); c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    for k in range(3):
        f = 0.3 + 0.25 * k
        c.move_to(lerp(26, 52 + 8 * flap, f) - 6, lerp(yb, -6, f)); c.line_to(lerp(20, 42 + 8 * flap, f) + 8, lerp(yb, -4, f) + 4)
        c.set_source_rgb(*NAP_B); c.set_line_width(6); c.stroke()
    # band
    rrect(c, -hw, yt, 2 * hw, yb - yt, 14); c.set_source_rgb(1, 1, 1); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.save(); rrect(c, -hw, yt, 2 * hw, yb - yt, 14); c.clip()
    for k in range(-5, 6):
        c.move_to(k * 22 - 6, yt); c.line_to(k * 22 + 6, yb)
        c.set_source_rgb(*NAP_B); c.set_line_width(7); c.stroke()
    c.restore()
    ellipse(c, 22, (yt + yb) / 2, 14, 12, (1, 1, 1), lw=4)     # knot
    c.restore()


def cape(c, x, y, s=CHS, sway=0.0):
    """Wilt's lettuce leaf, worn by Chip as a cape (drawn behind him)."""
    c.save(); c.translate(x, y); c.scale(s, s)
    c.move_to(-50, -104)
    c.curve_to(-80, -70, -96 - 6 * sway, -30, -104 - 8 * sway, -6)
    for k in range(9):
        px = lerp(-104 - 8 * sway, 104 + 8 * sway, (k + 1) / 9)
        c.line_to(px, -6 + (8 if k % 2 == 0 else -2))
    c.curve_to(96 + 6 * sway, -30, 80, -70, 50, -104); c.close_path()
    c.set_source_rgb(*LETTUCE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.set_source_rgb(*LETTUCE_D); c.set_line_width(3)
    for k in (-1, 0, 1):
        c.move_to(28 * k, -100); c.line_to(76 * k, -14); c.stroke()
    c.restore()


def cape_tie(c, x, y, s=CHS):
    c.save(); c.translate(x, y); c.scale(s, s)
    ellipse(c, -40, -100, 14, 9, LETTUCE, lw=4); ellipse(c, 40, -100, 14, 9, LETTUCE, lw=4)
    c.restore()


def parka(c, x, y, hood, rot=0.0, t=0.0):
    """Dill's grape-skin parka, drawn over him. hood 0 = sits on top of his head, 1 = pulled down over his eyes."""
    c.save(); c.translate(x, y); c.rotate(rot)

    def body_clip(ex=0):
        c.save(); c.translate(0, -155); c.scale(74 + ex, 132 + ex); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    # coat: lower half of the body
    c.save(); body_clip(4); c.clip()
    c.rectangle(-100, -150, 200, 160); c.set_source_rgb(*GRAPE); c.fill()
    ellipse(c, -34, -110, 12, 34, GRAPE_L, stroke=False)
    c.move_to(-100, -150); c.line_to(100, -150); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.restore()
    body_clip(4); c.set_source_rgb(*INK); c.set_line_width(6)
    c.save(); c.rectangle(-100, -150, 200, 160); c.clip(); body_clip(4); c.stroke(); c.restore()
    # fluffy trim at the collar + toggles
    for k in range(7):
        ellipse(c, -66 + 22 * k, -150, 13, 10, (1, 1, 1), lw=3)
    for by in (-112, -78, -46):
        rrect(c, -8, by - 5, 16, 10, 5); c.set_source_rgb(*hexc("#F3D9A4")); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
    # hood
    rim = lerp(-262, -168, hood)
    c.save(); body_clip(10); c.clip()
    c.rectangle(-100, -320, 200, rim + 320); c.set_source_rgb(*GRAPE); c.fill()
    ellipse(c, -30, lerp(-282, -240, hood), 20, 10, GRAPE_L, stroke=False)
    c.restore()
    c.save(); c.rectangle(-100, -320, 200, rim + 320); c.clip(); body_clip(10)
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke(); c.restore()
    hw = math.sqrt(max(0.0, 1 - ((rim + 155) / 142) ** 2)) * 84
    for k in range(9):
        ex = lerp(-hw + 8, hw - 8, k / 8)
        ellipse(c, ex, rim, 14, 11, (1, 1, 1), lw=3)
    # little stem on top of the hood (it IS a grape)
    c.set_source_rgb(*hexc("#5C940D")); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.move_to(0, -286); c.line_to(10, -318); c.stroke()
    c.restore()


def lightbulb(c, x, y, s, glow=1.0):
    if s <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(S(s), S(s))
    for i in range(8):
        a = -math.pi / 2 + (i - 3.5) * 0.4
        c.move_to(math.cos(a) * 58, math.sin(a) * 58 - 10); c.line_to(math.cos(a) * (78 + 10 * glow), math.sin(a) * (78 + 10 * glow) - 10)
    c.set_source_rgb(*GOLD); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    ellipse(c, 0, -10, 40, 42, hexc("#FFF3BF"), lw=6)
    ellipse(c, -12, -22, 10, 12, (1, 1, 1), stroke=False)
    rrect(c, -18, 26, 36, 26, 6); c.set_source_rgb(*hexc("#ADB5BD")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.move_to(-18, 36); c.line_to(18, 36); c.move_to(-18, 44); c.line_to(18, 44); c.stroke()
    c.restore()


def freezer_icon(t):
    """Chip's bubble: a little cube can't push the freezer door open; the Hand can."""
    def f(c):
        c.save(); rrect(c, -108, -78, 216, 156, 60); c.clip()
        c.rectangle(-120, -90, 240, 180); c.set_source_rgb(*hexc("#E7F5FF")); c.fill()
        open_k = ease(seg(t, T_HAND + 0.6, T_HAND + 1.1))
        # inside of the freezer (seen when open): white light + flakes
        rrect(c, -50, -62, 100, 120, 8); c.set_source_rgb(*hexc("#A5D8FF")); c.fill()
        if open_k > 0:
            c.set_source_rgba(1, 1, 1, 0.9 * open_k); rrect(c, -46, -58, 92, 112, 8); c.fill()
            for j in range(5):
                fx, fy = -30 + 15 * j, -40 + 22 * (j % 3)
                c.set_source_rgba(*ICE_B, open_k); c.set_line_width(3)
                for a in (0, 1.05, 2.1):
                    c.move_to(fx - 7 * math.cos(a), fy - 7 * math.sin(a)); c.line_to(fx + 7 * math.cos(a), fy + 7 * math.sin(a))
                c.stroke()
        # the door (hinged on the left)
        c.save(); c.translate(-50, 0); c.scale(S(1 - 0.85 * open_k), 1)
        rrect(c, 0, -62, 100, 120, 8); c.set_source_rgb(*hexc("#D0EBFF")); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        rrect(c, 80, -30, 9, 52, 4); c.set_source_rgb(*hexc("#868E96")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
        c.restore()
        if t < T_HAND:
            # tiny cube pushing
            bump = abs(math.sin((t - T_PROB) * 7)) * 8
            bx = -84 + bump
            rrect(c, bx - 16, 26, 32, 30, 8); c.set_source_rgba(0.78, 0.92, 1.0, 1); c.fill_preserve()
            c.set_source_rgb(*INK); c.set_line_width(3); c.stroke()
            ellipse(c, bx - 4, 38, 2.5, 3, INK, stroke=False); ellipse(c, bx + 6, 38, 2.5, 3, INK, stroke=False)
            if t > T_PROB + 0.8:
                k = back_out(seg(t, T_PROB + 0.8, T_PROB + 1.0))
                c.save(); c.translate(0, 0); c.scale(S(k), S(k))
                c.set_source_rgb(*INK); c.set_line_width(20); c.set_line_cap(cairo.LINE_CAP_ROUND)
                c.move_to(-42, -42); c.line_to(42, 42); c.move_to(42, -42); c.line_to(-42, 42); c.stroke()
                c.set_source_rgb(*hexc("#E03131")); c.set_line_width(12)
                c.move_to(-42, -42); c.line_to(42, 42); c.move_to(42, -42); c.line_to(-42, 42); c.stroke()
                c.restore()
        else:
            # the Hand comes down and swings it open
            d = ease(seg(t, T_HAND, T_HAND + 0.6))
            hx = lerp(80, 40, open_k)
            c.save(); c.translate(hx, lerp(-150, 30, d)); c.scale(0.22, 0.22); hand(c, 0, 0, 0.5); c.restore()
            if open_k > 0.3:
                for i in range(5):
                    a = -0.9 + 0.45 * i
                    c.move_to(0, 0); c.line_to(math.cos(a) * 150, math.sin(a) * 150)
                c.set_source_rgba(1, 1, 0.8, 0.4 * open_k); c.set_line_width(10); c.stroke()
        c.restore()
    return f


# ---------------- title card (variant A) ----------------
def title_card(c, t):
    g = cairo.RadialGradient(W / 2, 820, 50, W / 2, 820, 1300)
    g.add_color_stop_rgb(0, *hexc("#E7F5FF")); g.add_color_stop_rgb(0.35, *hexc("#74C0FC")); g.add_color_stop_rgb(1, *hexc("#1C2541"))
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    for i, wd in enumerate(["FRIDGE", "KINGDOM"]):
        p = back_out(seg(t, 0.1 + i * 0.25, 0.55 + i * 0.25))
        c.save(); c.translate(W / 2, 640 + i * 170 + 8 * math.sin(t * 6 + i)); c.rotate(0.04 * (1 if i else -1))
        c.scale(S(p), S(p)); text(c, wd, 0, 0, 170, GOLD if i else (1, 1, 1), olw=22); c.restore()
    crown(c, W / 2 + 190, 500, 1.6 * back_out(seg(t, 0.6, 1.0)), 0.25)
    q = ease_out(seg(t, 0.9, 1.3))
    if q > 0:
        c.save(); c.translate(W / 2, 1000 + (1 - q) * 50)
        text(c, "Episode 17:", 0, 0, 60, (1, 1, 1), olw=10)
        text(c, "The Expedition Plan", 0, 90, 76, GOLD, olw=12)
        c.restore()
    # the map with its big red arrow UP, bobbing in at the bottom
    k = back_out(seg(t, 0.4, 0.9))
    c.save(); c.translate(W / 2, 1270 + 10 * math.sin(t * 4)); c.rotate(-0.05); c.scale(S(0.95 * k), S(0.95 * k))
    scroll_map(c, 0, 0, 1.0, ease(seg(t, 0.8, 1.4)), 0.0)
    c.restore()


# ---------------- states ----------------
def tap_k(t):
    """0..1 pulse for each map smack."""
    for tp in TAPS:
        if tp - 0.2 <= t < tp + 0.25:
            return math.sin(math.pi * seg(t, tp - 0.2, tp + 0.25))
    return 0.0


def nod(t, delay=0.12, amp=0.12):
    for tp in TAPS:
        if tp + delay <= t < tp + delay + 0.35:
            return amp * math.sin(math.pi * seg(t, tp + delay, tp + delay + 0.35))
    return 0.0


def hood_k(t):
    if t < T_BONK:
        return 0.0
    if t < T_HOODUP:
        return ease(seg(t, T_BONK, T_BONK + 0.12))
    return 1 - ease(seg(t, T_HOODUP, T_HOODUP + 0.3))


def dill_state(t):
    """(x, y, kw, rot)"""
    if t < T_GLARE:
        k = tap_k(t)
        mood = "angry" if k > 0.5 else "proud"
        return DIX - 40 * k, FLOOR - 60 * k, dict(mood=mood, look=(-1, -0.5), arm="point_l"), 0.0
    if t < T_CHARGE:
        mood = "angry" if t < T_YES + 0.3 else "smug"
        return DIX, FLOOR, dict(mood=mood, look=(-1, 0.3), shake=3 if t < T_YES else 0), 0.0
    if t < T_C1:
        return DIX, FLOOR - 30 * math.sin(math.pi * seg(t, T_CHARGE, T_CHARGE + 0.4)), dict(mood="proud", look=(-1, -0.3), arm="up"), 0.0
    if t < T_C4:
        return DIX, FLOOR, dict(mood="proud", look=(-1, 0)), 0.0
    if t < T_GSTEP:
        k = back_out(seg(t, T_C4 + 0.2, T_C4 + 0.5))
        return DIX, FLOOR, dict(mood="proud", look=(1, -0.4), arm="up" if t > T_C4 + 0.2 else "down"), -0.06 * k
    if t < T_PUFF:
        look = (-1, -1) if t < T_GLAND else (-1, 0)
        return DIX, FLOOR, dict(mood="smug", look=look, arm="cross"), 0.0
    if t < T_BONK:
        return DIX, FLOOR, dict(mood="proud", look=(-1, 0.6), sq=1.0 + 0.06 * ease(seg(t, T_PUFF, T_PUFF + 0.3))), 0.0
    if t < T_THUNK:
        p = seg(t, T_BONK + 0.2, T_THUNK)
        x = DIX - 70 * ease(p) + 20 * math.sin(p * 9)
        return x, FLOOR - 12 * abs(math.sin(t * 9)), dict(mood="shocked", arm="reach" if int(t * 5) % 2 else "flail"), 0.12 * math.sin(t * 8)
    if t < T_HOODUP:
        q = seg(t, T_THUNK, T_THUNK + 0.25)
        return DIX - 70 + 40 * ease(q), FLOOR, dict(mood="frozen", arm="down"), -0.25 * math.sin(math.pi * q)
    if t < T_PROB:
        return DIX - 30, FLOOR, dict(mood="angry", look=(-1, 0), arm="reach"), 0.0
    if t < T_THINK:
        return DIX - 30, FLOOR, dict(mood="proud", look=(-1, -1), arm="point_l"), 0.0
    if t < T_BULB:
        # pacing, hand on chin
        p = (t - T_THINK) / (T_BULB - T_THINK)
        x = DIX - 40 + 50 * math.sin(p * 2 * math.pi * 1.5)
        lk = (1 if math.cos(p * 2 * math.pi * 1.5) > 0 else -1, -0.3)
        return x, FLOOR - 6 * abs(math.sin(t * 7)), dict(mood="smug", look=lk, arm="cross"), 0.0
    x_end = DIX - 40
    if t < T_TURN:
        return x_end, FLOOR, dict(mood="shocked" if t < T_FLASH else "proud", look=(0, -1)), 0.0
    if t < T_SWEAT:
        lx = lerp(0, 1, ease(seg(t, T_TURN, T_TURN + 1.2)))
        return x_end, FLOOR, dict(mood="smug" if t < T_DUCK else "frozen", look=(lx, -0.6 * lx - 0.4 * (1 - lx))), 0.0
    return x_end, FLOOR, dict(mood="frozen", look=(1, -0.6), shake=1.5 if t >= T_GULP else 0), 0.0


def crumb_state(t):
    """(x, y, kw, rot)"""
    if t < T_C1:
        n = nod(t, 0.12, 0.10)
        mood = "sheepish" if t < T_NO else "worried"
        return CRX, FLOOR, dict(mood=mood, look=(1, -0.6), bow=n), 0.0
    if t < T_C2:
        k = back_out(seg(t, T_C1 + 0.25, T_C1 + 0.6))
        return CRX, FLOOR - 20 * math.sin(math.pi * seg(t, T_C1 + 0.2, T_C1 + 0.6)), \
            dict(mood="sheepish", look=(1, 0), arm="wave_l" if t > T_C1 + 0.3 else "down"), 0.0
    if t < T_INS2:
        return CRX, FLOOR, dict(mood="sheepish", look=(1, 0) if t < T_GLAND else (1, 0.5)), 0.0
    if t < T_INS3:
        return CRX, FLOOR, dict(mood="scared", look=(0, 0.6), shake=3 if t < T_INS2 + 0.5 else 0), 0.0
    if t < T_BONK:
        return CRX, FLOOR, dict(mood="worried", look=(1, 0)), 0.0
    if t < T_PROB:
        return CRX, FLOOR, dict(mood="scared", look=(1, 0)), 0.0
    if t < T_THINK:
        return CRX, FLOOR, dict(mood="worried", look=(-1, -0.5)), 0.0
    if t < T_BULB:
        return CRX, FLOOR, dict(mood="worried", look=(0, -1), arm="wave_l"), 0.0
    if t < T_FOLLOW:
        return CRX, FLOOR, dict(mood="worried", look=(1, -0.3)), 0.0
    return CRX, FLOOR, dict(mood="scared" if t >= T_DUCK + 0.5 else "worried", look=(1, -0.8)), 0.0


def peep_state(t):
    """(x, y, kw)"""
    if t < T_C1:
        n = nod(t, 0.25, 1.0)
        return PEX, FLOOR - 30 * n, dict(mood="happy" if n < 0.3 else "proud", face=-0.4, look=(1, -1), rot=0.25 * n)
    if t < T_C2:
        return PEX, FLOOR, dict(mood="happy", face=-0.5, look=(-1, 0))
    if t < T_GLAND:
        hop_ = 25 * math.sin(math.pi * seg(t, T_C2 + 0.2, T_C2 + 0.5))
        return PEX, FLOOR - hop_, dict(mood="proud", face=0.3, wings="salute" if t > T_C2 + 0.3 else "down")
    if t < T_INS2:
        return PEX, FLOOR, dict(mood="proud", face=-0.3, wings="salute")
    if t < T_BONK:
        return PEX, FLOOR, dict(mood="happy", face=0.4, look=(1, 0))
    if t < T_PROB:
        return PEX, FLOOR, dict(mood="shock", face=0.4, look=(1, 0))
    if t < T_THINK:
        return PEX, FLOOR, dict(mood="happy", face=-0.4, look=(-1, -0.5))
    if t < T_BULB:     # copies Crumb's head-scratch / thinking: tilts side to side
        return PEX, FLOOR, dict(mood="blink" if int(t * 2) % 3 == 0 else "happy", face=0.0, look=(0, -1),
                                rot=0.15 * math.sin(t * 3), wings="salute")
    if t < T_FOLLOW + 0.2:
        return PEX, FLOOR, dict(mood="happy", face=0.3, look=(1, -0.3))
    return PEX, FLOOR, dict(mood="shock" if t >= T_DUCK + 0.4 else "happy", face=0.6, look=(1, -1))


def chip_state(t):
    """(x, y, kw)"""
    base = dict(t=t)
    if t < T_NO:
        n = nod(t, 0.2, 1.0)
        return CHX, FLOOR, dict(base, mood="shy", look=(1, -0.6), shiver=0.3)
    if t < T_GLARE + 0.2:
        sh = math.sin((t - T_NO) * 22)
        return CHX, FLOOR, dict(base, mood="scared", look=(sh, 0), arms="out", shiver=0.6)
    if t < T_YES:
        return CHX, FLOOR, dict(base, mood="eep", look=(1, 0), arms="cover", shiver=1.0)
    if t < T_C3:
        bob = 14 * abs(math.sin((t - T_YES) * 18)) if t < T_C1 else 0
        return CHX, FLOOR - bob, dict(base, mood="eep" if t < T_C1 else "shy", look=(1, 0))
    if t < T_INS3:
        bl = 1.0 if t > T_C3 + 0.4 else 0.0
        return CHX, FLOOR, dict(base, mood="happy", blush=bl, arms="up" if t < T_C3 + 1.2 else "down",
                                melt=0.08 * ease(seg(t, T_C3 + 0.6, T_C3 + 1.0)))
    if t < T_BONK:
        return CHX, FLOOR, dict(base, mood="scared" if t < T_ZIP else "shy", look=(1, 0), shiver=1.0 if t < T_ZIP else 0.0)
    if t < T_PROB:
        return CHX, FLOOR, dict(base, mood="eep", look=(1, 0))
    if t < T_THINK:
        return CHX, FLOOR, dict(base, mood="shy", look=(1, -1), arms="draw")
    if t < T_FOLLOW:
        return CHX, FLOOR, dict(base, mood="shy", look=(1, -0.5), arms="cover" if t < T_BULB else "down")
    return CHX, FLOOR, dict(base, mood="scared" if t >= T_DUCK + 0.3 else "shy", look=(1, -1), shiver=1.0 if t >= T_DUCK + 0.3 else 0)


def grandma_state(t):
    """(x, y, kw)"""
    if t < T_GSTEP:
        return GR0[0], GR0[1], dict(look=(-1, 0.5), mood="stern")
    if t < T_GLAND:
        p = seg(t, T_GSTEP, T_GLAND)
        x = lerp(GR0[0] - 60, GLAND, ease(p)) + 30 * math.sin(p * 9)
        y = lerp(TOP - 40, FLOOR, ease_out(p) if p > 0.15 else p * 0.2)
        if p < 0.15:
            x, y = hop(GR0, (GR0[0] - 60, TOP - 40), p / 0.15, 60)
        return x, y, dict(look=(-1, 1), mood="stern", chute=min(1.0, p * 4), cane="down")
    if t < T_INS1 + 0.3:
        return lerp(GLAND, PEX + 80, ease(seg(t, T_GLAND, T_INS1 + 0.3))), FLOOR, dict(look=(-1, -0.6), step=t * 3)
    if t < T_INS2:
        return PEX + 80, FLOOR, dict(look=(-1, -1), mood="stern", bow=-0.1)
    if t < T_INS2 + 0.6:
        x = lerp(PEX + 80, CRX + 105, ease(seg(t, T_INS2, T_INS2 + 0.25)))
        return x, FLOOR, dict(look=(-1, -1), cane="up" if t > T_INS2 + 0.25 else "down", step=t * 3)
    if t < T_INS3 + 0.5:
        x = lerp(CRX + 105, CHX + 110, ease(seg(t, T_INS2 + 0.6, T_INS3)))
        return x, FLOOR, dict(look=(-1, -0.5), cane="up" if T_INS3 + 0.1 <= t < T_INS3 + 0.4 else "down", step=t * 3)
    if t < T_ZIP:
        return CHX + 110, FLOOR, dict(look=(1, 0), mood="stern")
    if t < T_ZIPEND:
        x = lerp(CHX + 110, DIX - 130, ease(seg(t, T_ZIP, T_ZIPEND)))
        return x, FLOOR, dict(look=(1, 0), step=t * 8)
    if t < T_BONK - 0.25:
        return DIX - 130, FLOOR, dict(look=(1, -1), mood="stern")
    if t < T_BONK + 0.35:
        h = 190 * math.sin(math.pi * seg(t, T_BONK - 0.25, T_BONK + 0.35))
        return DIX - 130 + 60 * math.sin(math.pi * seg(t, T_BONK - 0.25, T_BONK + 0.35)), FLOOR, \
            dict(look=(1, -1), mood="angry", cane="up", hop=h)
    if t < T_PROB:
        return DIX - 130, FLOOR, dict(look=(1, -0.3), mood="stern")
    x = DIX - 160
    if t < T_THINK:
        return x, FLOOR, dict(look=(-1, -0.5), mood="stern")
    if t < T_FOLLOW + 0.3:
        return x, FLOOR, dict(look=(1, -0.5), mood="stern", cane="up" if int(t * 2.5) % 2 and t < T_BULB else "down")
    return x, FLOOR, dict(look=(1, -1), mood="shock" if t >= T_DUCK + 0.5 else "stern")


def map_swing(t):
    if t < T_THUNK:
        k = tap_k(t)
        return -0.06 * k
    q = t - T_THUNK
    return -0.25 * math.sin(q * 7) * math.exp(-q * 2.2)


def duck_motion(t):
    k = ease(seg(t, T_DUCK, T_DUCK + 1.4))
    return -0.45 * k, -2.0 * k     # tilt (toward Dill, left), gaze left


# ---------------- camera ----------------
KEYS = [(T_START, 600, 1150, 1.55), (TAPS[2], 620, 1150, 1.55), (T_NO, 400, 1200, 1.8), (T_GLARE, 480, 1200, 1.55),
        (T_YES, 300, 1250, 2.1), (T_CHARGE, 660, 1180, 1.6), (T_C1 - 0.15, 660, 1180, 1.6),
        (T_C1, CRX, 1260, 2.3), (T_C2 - 0.15, CRX, 1260, 2.3), (T_C2, PEX, 1290, 2.4), (T_WUP - 0.15, PEX, 1290, 2.4),
        (T_WUP, CHX + 60, 1290, 2.3), (T_C4 - 0.15, CHX + 60, 1290, 2.3), (T_C4, DIX - 30, 1240, 2.15),
        (T_GSTEP - 0.2, DIX - 30, 1240, 2.15), (T_GSTEP + 0.4, 760, 1020, 1.35), (T_GLAND, 560, 1200, 1.5),
        (T_INS1 + 0.3, 520, 1270, 2.0), (T_INS2 + 0.3, 420, 1280, 2.1), (T_INS3 + 0.2, 280, 1290, 2.1),
        (T_ZIPEND, 700, 1260, 1.9), (T_BONK + 0.2, 720, 1250, 2.1), (T_THUNK - 0.3, 700, 1200, 1.7),
        (T_HOODUP + 0.3, 650, 1170, 1.55), (T_PROB + 0.2, 380, 1150, 1.5), (T_THINK - 0.2, 380, 1150, 1.5),
        (T_THINK + 0.4, 560, 1190, 1.4), (T_BULB - 0.3, 560, 1190, 1.4), (T_BULB + 0.2, 780, 1180, 1.75),
        (T_FLASH + 1.8, 780, 1170, 1.75), (T_TURN + 1.0, 860, 1210, 1.7), (T_DUCK, 880, 1220, 1.85),
        (T_DUCK + 1.4, 900, 1230, 2.05), (T_SWEAT, 860, 1200, 2.1), (DUNS[0], 900, 1180, 2.2), (END_T, 960, 1160, 2.7)]


def camera(t):
    cx, cy, z = keyed(KEYS, t)
    cy += 40
    hw = 540 / z
    cx = min(max(cx, hw), W - hw)
    for t0, s in [(TAPS[0], 4), (TAPS[1], 4), (TAPS[2], 4), (T_BONK, 9), (T_THUNK, 6), (T_BULB, 3)]:
        if t0 <= t < t0 + 0.25:
            q = s * (1 - seg(t, t0, t0 + 0.25)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    for d in DUNS:
        if d <= t < d + 0.12:
            z += 0.12 * (1 - seg(t, d, d + 0.12))
    return cx, cy, z


# ---------------- scene ----------------
def hanging_map(c, t):
    rot = map_swing(t)
    c.save(); c.translate(MAPX, TOP + 34); c.rotate(rot); c.translate(-MAPX, -(TOP + 34))
    c.set_source_rgb(*INK); c.set_line_width(4)
    for sx in (-1, 1):
        c.move_to(MAPX + sx * 70, TOP + 40); c.line_to(MAPX + sx * 100, MAPY); c.stroke()
    c.save(); c.translate(MAPX, MAPY); c.scale(MAPS, MAPS)
    scroll_map(c, 0, 0, 1.0, 1.0, 0.0)
    c.restore()
    c.restore()


def scene(c, t):
    L = DIM
    fridge6(c, L, 1, lid=False)
    frost(c, t, 1.0)
    frost_drawing(c, 40.0)
    ceiling(c, L)
    ceiling_vent(c, L)

    # ---- top shelf: Grandma before she jumps ----
    gx, gy, gk = grandma_state(t)
    if t < T_GSTEP:
        draw_grandma(c, gx, gy, gk)

    # ---- bottom shelf set ----
    jello(c, JX, FLOOR, 0.0)
    tl, gz = duck_motion(t)
    clean_duck(c, JX, FLOOR - 146, tilt=tl, gaze=gz, frosty=0.7, s=DUCK_S)
    carton(c)
    plate(c, DISH)
    butter_rink(c, 1.0)
    hanging_map(c, t)

    # Chip (+ cape behind him)
    chx, chy, chk = chip_state(t)
    has_cape = t >= T_C3 + 0.05
    if has_cape:
        cape(c, chx, chy, CHS, sway=0.5 * math.sin(t * 3))
    chip(c, chx, chy, CHS, **chk)
    if has_cape:
        cape_tie(c, chx, chy - 6, CHS)

    # Crumb (+ scarf)
    crx, cry, ckw, crot = crumb_state(t)
    bow = ckw.pop("bow", 0.0)
    c.save(); c.translate(crx, cry); c.rotate(bow); c.translate(-crx, -cry)
    crumb_bitten(c, crx, cry, 1.0, rot=crot, **ckw)
    if t >= T_C1 + 0.05:
        tight = math.sin(math.pi * seg(t, T_INS2 + 0.2, T_INS2 + 0.6)) if T_INS2 + 0.2 <= t < T_INS2 + 0.6 else 0.0
        scarf(c, crx, cry, tight, flap=math.sin(t * 4))
    c.restore()

    # Peep (polished helmet sparkles)
    px, py, pkw = peep_state(t)
    fat_peep(c, px, py, FAT, **pkw)
    if t >= T_C2 + 0.05:
        for j, (dx, dy) in enumerate([(-34, -200), (30, -228), (52, -176)]):
            ph_ = (t * 1.4 + j * 0.33) % 1
            star(c, px + dx, py + dy, (22 if t < T_C2 + 1.2 else 12) * math.sin(math.pi * ph_), t * 3 + j, (1, 1, 1))

    # Wilt peeks up from the crisper drawer (behind the shelf lip), flicks the cape
    if T_WUP <= t < T_WDOWN + 0.6:
        up = ease(seg(t, T_WUP, T_WUP + 0.4)) * (1 - ease(seg(t, T_WDOWN, T_WDOWN + 0.5)))
        c.save(); c.rectangle(-400, -400, W + 800, FLOOR + 6 + 400); c.clip()
        flick = math.sin(math.pi * seg(t, T_C3 - 0.25, T_C3 + 0.2)) if T_C3 - 0.25 <= t < T_C3 + 0.2 else 0.0
        wilt(c, WX, FLOOR + 300 - 190 * up, droop=0.4 + 0.6 * flick, look=(-1, 0))
        c.restore()

    # Dill (+ parka)
    dx, dy, dkw, drot = dill_state(t)
    dill(c, dx, dy, crown_on=False, rot=drot, **dkw)
    if t >= T_C4 + 0.05:
        parka(c, dx, dy, hood_k(t), drot, t)

    # Grandma on the bottom shelf
    if t >= T_GSTEP:
        draw_grandma(c, gx, gy, gk)

    effects(c, t, dx, dy)
    dark_overlay(c, L)
    # the Duck's glint: light, after the overlay
    if T_GLINT <= t < T_GLINT + 0.6:
        star(c, JX - 20, FLOOR - 146 - 142 * DUCK_S - 10, 26 * math.sin(math.pi * seg(t, T_GLINT, T_GLINT + 0.6)), t * 4, (1, 1, 1))


def draw_grandma(c, x, y, kw):
    hop_ = kw.get("hop", 0.0)
    c.save(); c.translate(x, y); c.scale(GSC, GSC); c.translate(-x, -y)
    grandma(c, x, y, **kw)
    c.restore()
    if kw.get("chute", 0) < 0.05:
        crown(c, x + GRAN_HEAD[0], y + GRAN_HEAD[1] - hop_ * GSC, 0.72, -0.2)


def effects(c, t, dx, dy):
    for i, tp in enumerate(TAPS):
        word(c, t, "TAP!", MAPX - 40 + 60 * i, MAPY - 30, 56, (1, 1, 1), tp, tp + 0.4, -0.1 + 0.1 * i)
    for i, tp in enumerate(TAPS):
        word(c, t, "mm-hm!", CRX - 20, FLOOR - 360, 40, (1, 1, 1), tp + 0.15, tp + 0.5, -0.1)
    word(c, t, "mm-mm!", CHX + 70, FLOOR - 270, 44, ICE, T_NO + 0.1, T_GLARE + 0.2, 0.06)
    word(c, t, "!!", DIX - 40, FLOOR - 380, 70, (1, 0.35, 0.35), T_GLARE, T_YES + 0.2)
    word(c, t, "mm-hm!", CHX + 80, FLOOR - 280, 42, ICE, T_YES, T_C1, -0.06)
    word(c, t, "HYAAA!", DIX + 40, FLOOR - 520, 66, GOLD, T_CHARGE, T_C1 - 0.1, -0.06)
    # montage
    poof(c, CRX, FLOOR - 90, t, T_C1, 0.9)
    poof(c, PEX, FLOOR - 190, t, T_C2, 0.8)
    poof(c, CHX, FLOOR - 110, t, T_C3, 0.8)
    poof(c, DIX, FLOOR - 170, t, T_C4, 1.1)
    for tc, x, y in [(T_C1, CRX + 100, FLOOR - 380), (T_C2, PEX + 60, FLOOR - 360), (T_C3, CHX + 100, FLOOR - 300),
                     (T_C4, DIX - 110, FLOOR - 420)]:
        word(c, t, "cha-ching!", x, y, 54, GOLD, tc + 0.1, tc + 1.0, 0.08)
        if tc + 0.3 <= t < tc + 1.1:
            q = seg(t, tc + 0.3, tc + 1.1)
            for j in range(4):
                a = j * math.pi / 2 + q * 2
                star(c, x - 60 + 160 * math.cos(a) * q, y + 100 + 90 * math.sin(a) * q, 16 * (1 - q), t * 5, GOLD)
    word(c, t, "ting!", PEX - 60, FLOOR - 300, 46, (1, 1, 1), T_C2 + 0.4, T_C2 + 1.3, -0.1)
    word(c, t, "sigh...", WX + 120, FLOOR - 340, 44, hexc("#C5D86D"), T_WUP + 0.3, T_C3 + 0.1, 0.06)
    word(c, t, "drip", CHX - 90, FLOOR - 60, 40, ICE, T_C3 + 0.7, T_C3 + 1.3, -0.1)
    if T_C3 + 0.5 <= t < T_INS1:
        for j in range(2):
            q = ((t - T_C3 - 0.5) * 0.8 + j / 2) % 1
            heart(c, CHX - 30 + 60 * j, FLOOR - 230 - 100 * q, 1.0, 1 - q)
    word(c, t, "ta-daaa!", DIX + 40, FLOOR - 470, 52, (1, 1, 1), T_C4 + 0.6, T_GSTEP - 0.1, -0.08)
    # Grandma inspection
    word(c, t, "hm.", PEX + 140, FLOOR - 260, 44, (1, 1, 1), T_INS1 + 0.3, T_INS2 - 0.05, 0.08)
    word(c, t, "GK!", CRX + 10, FLOOR - 380, 56, (1, 0.35, 0.35), T_INS2 + 0.3, T_INS2 + 0.8, -0.1)
    word(c, t, "boop", CHX + 90, FLOOR - 250, 42, (1, 1, 1), T_INS3 + 0.1, T_INS3 + 0.5, 0.1)
    if T_ZIP <= t < T_ZIPEND + 0.2:
        for j in range(4):
            yy = FLOOR - 40 - 40 * j
            gx = grandma_state(min(t, T_ZIPEND))[0]
            c.move_to(gx - 60 - 30 * j, yy); c.line_to(gx - 200 - 30 * j, yy)
            c.set_source_rgba(1, 1, 1, 0.8); c.set_line_width(6); c.stroke()
    word(c, t, "zip!", DIX - 300, FLOOR - 220, 46, (1, 1, 1), T_ZIP, T_ZIPEND + 0.3, -0.1)
    word(c, t, "BONK!", DIX - 60, FLOOR - 480, 80, (1, 0.9, 0.4), T_BONK, T_BONK + 0.6, -0.1)
    if T_BONK <= t < T_HOODUP:
        for j in range(4):
            a = (t - T_BONK) * 5 + j * math.pi / 2
            star(c, dx + 75 * math.cos(a), dy - 330 + 16 * math.sin(a), 14, t * 5, GOLD)
    word(c, t, "?!", dx + 70, FLOOR - 380, 58, (1, 1, 1), T_BONK + 0.4, T_THUNK)
    word(c, t, "THUNK", MAPX + 40, MAPY + 300, 58, (1, 1, 1), T_THUNK, T_THUNK + 0.5, 0.1)
    word(c, t, "hmph", DIX + 60, FLOOR - 370, 46, (1, 1, 1), T_HOODUP, T_PROB + 0.3, 0.1)
    # problem: the freezer door
    if T_PROB <= t < T_THINK:
        s = 1.45 * back_out(seg(t, T_PROB, T_PROB + 0.3))
        if t >= T_THINK - 0.25:
            s *= 1 - seg(t, T_THINK - 0.25, T_THINK)
        bubble(c, CHX + 130, FLOOR - 520, s, freezer_icon(t))
    word(c, t, "tump tump", CHX + 280, FLOOR - 640, 44, (1, 0.35, 0.35), T_PROB + 0.8, T_HAND, 0.08)
    word(c, t, "ooh...", CHX + 300, FLOOR - 640, 44, (1, 1, 1), T_HAND + 0.8, T_THINK, 0.08)
    # thinking
    if T_THINK <= t < T_BULB:
        for i, (x, y) in enumerate([(CHX + 20, FLOOR - 260), (CRX, FLOOR - 380), (PEX, FLOOR - 320), (DIX - 150, FLOOR - 250)]):
            q = ((t - T_THINK) * 0.7 + i * 0.27) % 1
            word(c, t, "?", x + 20 * math.sin(q * 6), y - 60 * q, 54, (1, 1, 1), T_THINK + 0.2 * i, T_BULB, 0.1 * math.sin(q * 5))
        for k in range(4):
            t0 = T_THINK + 0.3 + 0.8 * k
            word(c, t, "tick..." if k % 2 == 0 else "tock...", 560 + (90 if k % 2 else -90), FLOOR - 560, 46, (1, 1, 1), t0, t0 + 0.7, 0.08 * (1 if k % 2 else -1))
        word(c, t, "hmmm", dx + 60, FLOOR - 370, 44, (1, 1, 1), T_THINK + 0.6, T_THINK + 1.6, 0.1)
        word(c, t, "tok tok", DIX - 150, FLOOR - 230, 38, (1, 1, 1), T_THINK + 1.8, T_THINK + 2.6, -0.1)
    # lightbulb + flashback
    if T_BULB <= t < T_TURN:
        s = back_out(seg(t, T_BULB, T_BULB + 0.25))
        if t >= T_TURN - 0.3:
            s *= 1 - seg(t, T_TURN - 0.3, T_TURN)
        lightbulb(c, dx, dy - 390, 1.0 * s, glow=0.5 + 0.5 * math.sin(t * 12))
    word(c, t, "DING!", dx + 130, FLOOR - 420, 54, GOLD, T_BULB, T_BULB + 0.5, 0.1)
    if T_FLASH <= t < T_TURN:
        s = 1.15 * back_out(seg(t, T_FLASH, T_FLASH + 0.3))
        if t >= T_TURN - 0.25:
            s *= 1 - seg(t, T_TURN - 0.25, T_TURN)
        bubble_r(c, dx - 100, FLOOR - 600, s, plan_icon)
    word(c, t, "ooooh", dx - 40, FLOOR - 340, 46, GOLD, T_FLASH + 0.8, T_TURN, 0.1)
    # the stare
    if T_SWEAT <= t < END_T:
        k = seg(t, T_SWEAT, T_SWEAT + 1.0)
        drop(c, dx + 80, dy - 270 + 50 * k, 1.6)
    word(c, t, "gulp", dx - 120, FLOOR - 330, 46, (1, 1, 1), T_GULP, T_GULP + 0.7, -0.1)
    word(c, t, "...", JX - 10, FLOOR - 420, 60, (1, 1, 1), T_DUCK + 1.4, T_SWEAT + 0.5, 0.05)


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
    c.save()
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    scene(c, t)
    c.restore()
    if t < T_START + 0.3:
        iris(c, W / 2, H / 2, lerp(0, 1300, ease(seg(t, T_START, T_START + 0.3))))
    if t >= T_DUCK:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.35, 0.25, 0.5, 0.12 * ease(seg(t, T_DUCK, T_DUCK + 1.0))); c.fill()
    if t >= END_T - 0.4:
        dyy = FLOOR - 146 - 142 * DUCK_S
        iris(c, W / 2 + (JX - cx) * Z, H / 2 + (dyy - cy) * Z, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))


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
