"""FRIDGE KINGDOM — Episode 9: "Feeding Time". 40.5s, 1080x1920 @ 30fps.

Variant A (title card first).

Peep chases Dill across the top shelf, beak snapping. Crumb steps in and feeds it a crumb of his own
crust; Peep gobbles it and pecks a bite out of his bottom corner (ow). On the bottom shelf, Crumb runs a
feeding montage: a grape (gulp), a cheese slice with a Duck sticker on it (the sticker turns its head...
gone), a pea (pop). Peep gets rounder each time and is still hungry. Dill offers his bitten butter throne;
Peep slurps up every last bit; Dill weeps over the empty dish. Peep eyes the jello: Grandma Gherkin springs
in front of it, cane raised; she swings (miss) and Peep backs off. Full at last, Peep burps a huge burp that
blows Dill's crown away; it drops out of the sky onto Grandma's bun. Crumb pats Peep's belly. Sleepy Peep
lets out the loudest PEEEEP yet... THUMP. THUMP. Footsteps outside. Light spills in from the door's edge;
the choir begins; everyone slowly turns to look at Peep. If the Hand sees it... Record stop.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crumb, duck, crown, bubble, dark_overlay, ellipse, rrect, star, text, hand,
                 iris, hexc, seg, ease, ease_out, lerp, back_out, INK, GOLD, FLOOR, TOP, W, H, FPS, S)
from ep2 import end_card, jello, grape
from ep4 import WHITE
from ep5 import cap_crown, crumb_notched, tears, JELLO_X
from ep6 import grandma, fridge6, lid_piece
from ep8 import peep, shell_half
from animate import heart

DUR = 40.5
END_T = 39.0
DIM = 0.18
EGG_X = 900
DISH_X = 420

# ---------------- timing ----------------
T_CUT = 9.8            # whip down to the bottom shelf
T_FOOD = [(10.3, 10.9, 11.25), (11.9, 13.1, 13.45), (14.0, 14.45, 14.75)]   # (show, toss, gulp)
T_SLURP0, T_SLURP1 = 17.6, 19.2
T_GLAND = 22.9         # Grandma lands in front of the jello
T_SWING = 24.9
T_BURP = 29.0
T_CROWN_DROP = 30.3
T_PEEEP = 33.5
T_THUMPS = (34.9, 35.6)
T_LIGHT = 36.2
T_TURN = 36.7
T_STOP = 37.7

FAT = [1.0, 1.12, 1.26, 1.38]   # Peep after each montage gulp; +butter -> 1.52


def fatness(t):
    f = 1.0
    for i, (_, _, tg) in enumerate(T_FOOD):
        f = lerp(f, FAT[i + 1], back_out(seg(t, tg, tg + 0.3)))
    f = lerp(f, 1.52, ease(seg(t, T_SLURP0, T_SLURP1)))
    if T_BURP - 0.6 <= t < T_BURP:      # gulps air, puffs up
        f += 0.08 * ease(seg(t, T_BURP - 0.6, T_BURP))
    elif T_BURP <= t < T_BURP + 0.5:
        f += 0.08 * (1 - ease(seg(t, T_BURP, T_BURP + 0.5)))
    return f


def fat_peep(c, x, y, fat, **kw):
    c.save(); c.translate(x, y); c.scale(S(fat), S(1 + (fat - 1) * 0.4)); c.translate(-x, -y)
    peep(c, x, y, **kw)
    c.restore()


# ---------------- new props ----------------
def pea(c, x, y, s=1.0):
    if s < 0.02:
        return
    ellipse(c, x, y, 24 * s, 24 * s, hexc("#69DB7C"), lw=5)
    ellipse(c, x - 8 * s, y - 8 * s, 7 * s, 6 * s, (1, 1, 1), stroke=False)


def cheese_slice(c, x, y, s=1.0, rot=0.0, duck_turn=0.0, bite=0.0):
    """A square cheese slice with a round sticker of the Duck (with its cap crown) printed on it."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(s), S(s))
    rrect(c, -80, -80, 160, 160, 14); c.set_source_rgb(*hexc("#FFD43B")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    for hx, hy, r in [(-50, -52, 10), (52, -40, 8), (-48, 50, 9), (46, 54, 12), (8, -64, 6)]:
        ellipse(c, hx, hy, r, r * 0.85, hexc("#F59F00"), stroke=False)
    # sticker
    ellipse(c, 2, 4, 52, 52, (1, 1, 1), lw=5)
    ellipse(c, 2, 4, 44, 44, hexc("#D0EBFF"), stroke=False)
    c.save(); c.translate(2, 38); c.scale(0.26, 0.26)
    duck(c, 0, 0, turn=duck_turn)
    cap_crown(c, lerp(40, 4, ease(duck_turn)) + 4, -186, 0.38)
    c.restore()
    c.restore()


def butter_dish_left(c, x, y, amt=1.0):
    """Dill's bitten butter throne with only `amt` (0..1) of the butter left (eaten from the right)."""
    c.save(); c.translate(x, y)
    ellipse(c, 0, -10, 150, 26, (0.97, 0.97, 1), lw=6)
    if amt > 0.01:
        bites = [(70, -112, 34), (32, -118, 26), (96, -76, 22)]
        c.save()
        c.rectangle(-120, -140, 25 + 190 * amt, 140); c.clip()
        c.save()
        c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        c.rectangle(-300, -300, 600, 400)
        for bx, by, r in bites:
            c.new_sub_path(); c.arc(bx, by, r, 0, 2 * math.pi)
        c.clip()
        c.set_fill_rule(cairo.FILL_RULE_WINDING)
        rrect(c, -95, -110, 190, 96, 18); c.set_source_rgb(*hexc("#FFE680")); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        c.set_source_rgba(1, 1, 1, 0.7); rrect(c, -80, -100, 60, 14, 7); c.fill()
        c.restore()
        c.save(); rrect(c, -95, -110, 190, 96, 18); c.clip()
        for bx, by, r in bites:
            c.new_sub_path(); c.arc(bx, by, r, 0, 2 * math.pi)
        c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        c.restore()
        if amt < 0.99:   # licked-clean ragged edge
            ex = -95 + 190 * amt
            c.move_to(ex, -100)
            for k in range(6):
                c.line_to(ex + (6 if k % 2 else -4), -100 + k * 16)
            c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        c.restore()
    else:   # licked clean: shiny plate
        ellipse(c, -40, -18, 40, 6, (1, 1, 1), stroke=False)
    c.restore()


def crumb_bitten(c, x, y, bite=0.0, **kw):
    """Crumb (top-right corner already snapped off) with a new round peck-bite out of his bottom-right corner."""
    if bite < 0.05:
        crumb_notched(c, x, y, True, **kw); return
    r = 24 * bite
    c.save()
    m = c.get_matrix()
    c.translate(x, y); c.rotate(kw.get("rot", 0.0))
    c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
    c.rectangle(-400, -600, 800, 800)
    c.new_sub_path(); c.arc(74, -38, r, 0, 2 * math.pi)
    c.clip()
    c.set_fill_rule(cairo.FILL_RULE_WINDING)
    c.set_matrix(m)
    crumb_notched(c, x, y, True, **kw)
    c.restore()
    c.save(); c.translate(x, y); c.rotate(kw.get("rot", 0.0))
    c.arc(74, -38, r, math.pi * 0.5, math.pi * 1.5)
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.restore()


def bread_bit(c, x, y, s=1.0):
    c.move_to(x - 12 * s, y + 8 * s); c.line_to(x - 8 * s, y - 10 * s); c.line_to(x + 10 * s, y - 8 * s); c.line_to(x + 12 * s, y + 9 * s)
    c.close_path(); c.set_source_rgb(*hexc("#C98A4B")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3.5); c.stroke()


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
        text(c, "Episode 9:", 0, 0, 60, (1, 1, 1), olw=10)
        text(c, "Feeding Time", 0, 90, 80, GOLD, olw=12)
        c.restore()
    dill(c, 280, 1680 - abs(math.sin(t * 7)) * 40, "shocked", crown_on=True, arm="reach", shake=3)
    snap = int(t * 7) % 2
    peep(c, 620, 1680 - abs(math.sin(t * 7 + 1)) * 30, mood="hungry" if snap else "happy", face=-1, look=(-1, -0.4),
         wings="flap", flap_t=t)
    crumb_notched(c, 860, 1680, True, mood="worried", look=(-1, 0), shake=3)


def hop(a, b, p, height=200):
    return lerp(a[0], b[0], p), lerp(a[1], b[1], p) - height * math.sin(math.pi * p)


def snap_mood(t, rate=7):
    return "hungry" if int(t * rate) % 2 == 0 else "happy"


# ---------------- states: TOP SHELF (2.0 – T_CUT) ----------------
def top_dill(t):
    if t < 4.0:      # flees right -> left
        p = seg(t, 2.0, 4.0)
        return lerp(840, 250, ease_out(p)), TOP - abs(math.sin(t * 14)) * 30, dict(mood="shocked", look=(1, 0), arm="reach")
    if t < 8.6:      # cowers behind Crumb, peeking
        return 250, TOP, dict(mood="frozen" if t < 6.0 else "shocked", look=(1, 0), shake=4)
    if t < 9.0:      # Peep looks at him again: yelp
        return 250, TOP - 40 * math.sin(math.pi * seg(t, 8.6, 9.0)), dict(mood="shocked", look=(1, 0), arm="reach")
    return 250, TOP, dict(mood="frozen", look=(1, 0), shake=5)


def top_crumb(t):
    bite = back_out(seg(t, 7.35, 7.5))
    if t < 3.6:
        return 450, TOP, dict(mood="worried", look=(1, 0)), 0
    if t < 4.6:      # throws his arm out: STOP
        return 450, TOP, dict(mood="scared", look=(1, 0.3), arm="wave"), 0
    if t < 5.0:      # breaks off a bit of crust
        return 450, TOP, dict(mood="sheepish", look=(1, 0.5)), 0
    if t < 5.7:      # holds it out
        return 450, TOP, dict(mood="sheepish", look=(1, 0.6), arm="wave"), 0
    if t < 7.35:
        return 450, TOP, dict(mood="sheepish" if t < 6.8 else "worried", look=(1, 0.7)), 0
    if t < 8.4:      # OW
        return 450 - 12 * math.sin(math.pi * seg(t, 7.35, 7.7)), TOP - 30 * math.sin(math.pi * seg(t, 7.35, 7.75)), \
            dict(mood="scared", look=(1, 1)), bite
    if t < 9.0:
        return 450, TOP, dict(mood="worried", look=(1, 0.6)), bite
    # idea!
    return 450, TOP, dict(mood="sheepish", look=(0, -1), arm="wave"), bite


def top_peep(t):
    if t < 4.0:      # chases, snapping
        p = seg(t, 2.2, 4.0)
        return lerp(1060, 660, ease_out(p)), TOP - abs(math.sin(t * 16)) * 26, dict(mood=snap_mood(t), face=-1, look=(-1, -0.3), wings="flap", flap_t=t)
    if t < 4.6:      # skids to a stop at Crumb's arm
        return 660, TOP, dict(mood="shock", face=-0.8, look=(-1, -1), sq=lerp(0.85, 1, seg(t, 4.0, 4.3)))
    if t < 5.75:     # stares up, hungry
        return 660, TOP, dict(mood="hungry", face=-0.8, look=(-1, -1), flap_t=t)
    if t < 6.05:     # catches the crumb
        return 660, TOP, dict(mood="chirp", face=-0.9, look=(-1, -1), rot=-0.08)
    if t < 6.8:      # munch
        k = int(t * 10) % 2
        return 660, TOP, dict(mood="blink" if k else "proud", face=-0.6, sq=1 + 0.05 * k)
    if t < 7.35:     # leans in...
        p = ease(seg(t, 6.8, 7.2))
        return lerp(660, 600, p), TOP, dict(mood="hungry", face=-1, look=(-1, 0.6), rot=-0.45 * p, flap_t=t)
    if t < 7.6:      # PECK
        return 600, TOP, dict(mood="chirp", face=-1, rot=-0.6)
    if t < 8.5:      # chews the corner
        k = int(t * 10) % 2
        return lerp(600, 650, ease(seg(t, 7.6, 7.9))), TOP, dict(mood="blink" if k else "proud", face=-0.3, sq=1 + 0.05 * k)
    # looks past Crumb at Dill: hungry again
    return 650, TOP, dict(mood="hungry", face=-1, look=(-1, -0.2), flap_t=t)


def food_in_hand_top(t):
    """Crust bit position: (x, y) or None."""
    if 5.0 <= t < 5.75:
        return 450 + 112 + 6, TOP - 216
    if 5.75 <= t < 6.05:
        p = seg(t, 5.75, 6.05)
        x, y = hop((568, TOP - 216), (644, TOP - 70), p, 60)
        return x, y
    return None


# ---------------- states: BOTTOM SHELF (T_CUT – END) ----------------
CR_X = 600     # Crumb (feeder)
PE_X = 800     # Peep (eater)


def bot_dill(t):
    """(x, y, kw, crown_on, tears)"""
    has = t < T_BURP + 0.05
    if t < 16.0:     # on his throne, watching nervously
        mood = "frozen" if any(tg <= t < tg + 0.5 for _, _, tg in T_FOOD) else "shocked"
        return DISH_X, FLOOR - 110, dict(mood=mood, look=(1, 0.3), shake=2), has, 0
    if t < 16.5:     # Peep turns to him: gulp; hops off
        p = seg(t, 16.0, 16.5)
        x, y = hop((DISH_X, FLOOR - 110), (285, FLOOR), ease(p), 90)
        return x, y, dict(mood="shocked", look=(1, 0), arm="reach"), has, 0
    if t < T_SLURP0:   # presents the throne with a nervous grin
        return 285, FLOOR, dict(mood="smug", look=(1, 0.2), arm="point", shake=3), has, 0
    if t < T_SLURP1 + 0.2:
        mood = "shocked" if t < 18.2 else "sad"
        return 285, FLOOR, dict(mood=mood, look=(1, 0.4), arm="point" if t < 18.2 else "down"), has, 0
    if t < 19.9:     # rushes to the empty dish
        p = ease(seg(t, T_SLURP1 + 0.2, 19.9))
        return lerp(285, DISH_X - 20, p), FLOOR - 20 * math.sin(math.pi * p), dict(mood="sad", look=(1, 0.5)), has, 0
    if t < 26.6:     # weeps behind the empty dish
        return DISH_X - 20, FLOOR + 4 * math.sin(t * 9), dict(mood="sad", look=(0, 1)), has, min(1, seg(t, 19.9, 20.4))
    if t < 27.5:     # sniffles over to Peep, wagging a finger
        p = ease(seg(t, 26.6, 27.5))
        return lerp(DISH_X - 20, 480, p), FLOOR - abs(math.sin(p * math.pi * 2)) * 16, dict(mood="angry", look=(1, 0)), has, 0
    if t < T_BURP:
        return 480, FLOOR, dict(mood="angry", look=(1, 0.2), arm="point", sq=1.03), has, 0
    if t < T_BURP + 1.2:   # blasted by the burp
        p = seg(t, T_BURP, T_BURP + 0.25)
        return 480 - 22 * ease_out(p), FLOOR, dict(mood="shocked", look=(1, 0), rot=-0.25 * (1 - seg(t, T_BURP + 0.4, T_BURP + 1.2)), shake=6), has, 0
    if t < T_CROWN_DROP + 0.4:   # pats his bare head
        return 460, FLOOR, dict(mood="shocked", look=(0, -1), arm="reach"), False, 0
    if t < T_PEEEP:
        return 460, FLOOR, dict(mood="angry" if t < 31.6 else "frozen", look=(1, -0.2) if t < 31.6 else (1, 0.2)), False, 0
    if t < T_PEEEP + 0.9:
        return 460, FLOOR, dict(mood="shocked", look=(1, 0), shake=8, sq=0.95), False, 0
    if t < T_TURN:   # THUMP: freezes, eyes to the door
        return 460, FLOOR - (12 if any(tt <= t < tt + 0.15 for tt in T_THUMPS) else 0), dict(mood="frozen", look=(1, -0.2)), False, 0
    return 460, FLOOR, dict(mood="frozen", look=(1, 0.5), shake=1.5 if t < T_STOP else 0), False, 0


def bot_crumb(t):
    """(x, y, kw)"""
    if t < 16.0:
        for i, (ts, tt, tg) in enumerate(T_FOOD):
            if ts <= t < tt + 0.1:
                return CR_X, FLOOR, dict(mood="sheepish", look=(1, -0.2 if i == 1 else 0.3), arm="wave")
        if 15.0 <= t < 16.0:   # out of food: shrugs
            return CR_X, FLOOR - 10 * abs(math.sin(t * 8)), dict(mood="scared", look=(1, 0))
        return CR_X, FLOOR, dict(mood="worried", look=(1, 0.3))
    if t < 26.0:
        mood = "scared" if T_GLAND - 0.2 <= t < T_SWING + 0.8 else "worried"
        lk = (-1, 0) if t < 21.0 else (1, 0)
        return CR_X, FLOOR, dict(mood=mood, look=lk)
    if t < 27.0:     # walks round behind Peep to its far side
        p = ease(seg(t, 26.0, 27.0))
        return lerp(CR_X, 800, p), FLOOR - abs(math.sin(p * math.pi * 3)) * 14, dict(mood="worried", look=(-1, 0))
    if t < T_BURP:
        return 800, FLOOR, dict(mood="worried", look=(-1, 0.3))
    if t < 30.8:
        return 800, FLOOR, dict(mood="scared" if t < T_BURP + 0.8 else "sheepish", look=(-1, -0.6) if t > T_CROWN_DROP - 0.5 else (-1, 0))
    if t < 32.6:     # pats Peep's round belly
        k = math.sin((t - 30.8) * 9)
        return 800, FLOOR, dict(mood="sheepish", look=(-1, 0.4), rot=-0.07 - 0.05 * max(0, k))
    if t < T_PEEEP:
        return 800, FLOOR, dict(mood="sheepish", look=(-1, 0.4))
    if t < T_PEEEP + 0.9:
        return 800, FLOOR, dict(mood="scared", look=(-1, 0), shake=8)
    if t < T_TURN:
        return 800, FLOOR - (12 if any(tt <= t < tt + 0.15 for tt in T_THUMPS) else 0), dict(mood="scared", look=(1, -0.3))
    return 800, FLOOR, dict(mood="scared", look=(-1, 0.4), shake=1.5 if t < T_STOP else 0)


def bot_peep(t):
    """(x, y, kw)"""
    if t < T_FOOD[0][2] - 0.3:
        return PE_X, FLOOR, dict(mood="hungry", face=-0.9, look=(-1, -0.6), flap_t=t)
    for i, (ts, tt, tg) in enumerate(T_FOOD):
        if tg - 0.3 <= t < tg:
            return PE_X, FLOOR, dict(mood="hungry", face=-1, look=(-1, -0.6), flap_t=t)
        if tg <= t < tg + 0.45:
            return PE_X, FLOOR, dict(mood="chirp", face=-0.6, look=(0, -1), sq=1.06)
        if tg + 0.45 <= t < (T_FOOD[i + 1][2] - 0.3 if i < 2 else 15.0):
            return PE_X, FLOOR, dict(mood="hungry" if t > tg + 0.8 else "proud", face=-0.9, look=(-1, -0.6), flap_t=t)
    if t < 16.0:     # still hungry: turns to look at Dill
        return PE_X, FLOOR, dict(mood="hungry", face=-1, look=(-1, -0.2), flap_t=t, rot=0.04 * math.sin(t * 5))
    if t < 16.9:
        return PE_X, FLOOR, dict(mood="hungry" if t > 16.4 else "happy", face=-1, look=(-1, 0.2), flap_t=t)
    if t < T_SLURP0:   # big hop over Crumb onto the butter dish rim
        x, y = hop((PE_X, FLOOR), (DISH_X + 140, FLOOR - 16), ease(seg(t, 16.9, T_SLURP0)), 330)
        return x, y, dict(mood="hungry", face=-1, wings="flap", flap_t=t)
    if t < T_SLURP1:   # slurps from right to left
        amt = 1 - ease(seg(t, T_SLURP0, T_SLURP1))
        k = int(t * 12) % 2
        return DISH_X - 95 + 190 * amt + 40, FLOOR - 16, dict(mood="chirp" if k else "hungry", face=-1, rot=-0.15, flap_t=t)
    if t < 19.6:
        return DISH_X - 55, FLOOR - 16, dict(mood="proud", face=0.2)
    if t < 20.2:     # hops down off the dish
        x, y = hop((DISH_X - 55, FLOOR - 16), (720, FLOOR), ease(seg(t, 19.6, 20.2)), 200)
        return x, y, dict(mood="happy", wings="flap", flap_t=t)
    if t < 21.2:
        return 720, FLOOR, dict(mood="happy", face=0.3, look=(0, 0))
    if t < 21.9:     # spots the jello
        return 720, FLOOR, dict(mood="hungry", face=1, look=(1, -0.3), flap_t=t)
    if t < 22.7:     # waddles toward it
        p = ease(seg(t, 21.9, 22.7))
        return lerp(720, 760, p), FLOOR - abs(math.sin(p * math.pi * 3)) * 14, dict(mood="hungry", face=1, look=(1, -0.3), flap_t=t)
    if t < T_GLAND + 0.2:
        return 760, FLOOR, dict(mood="shock", face=1, look=(1, -0.6), sq=0.9)
    if t < T_SWING - 0.2:   # stand-off: inches forward
        return 760 + 20 * ease(seg(t, 23.6, T_SWING - 0.2)), FLOOR, dict(mood="hungry", face=1, look=(1, 0.3), flap_t=t)
    if t < T_SWING + 0.35:  # ducks the swing
        return 780, FLOOR, dict(mood="shock", face=1, look=(1, -1), sq=0.7)
    if t < 26.0:            # backs off
        p = ease(seg(t, T_SWING + 0.35, 26.0))
        return lerp(780, 650, p), FLOOR - abs(math.sin(p * math.pi * 3)) * 12, dict(mood="shock", face=0.6, look=(1, 0), wings="flap", flap_t=t)
    if t < T_BURP - 0.6:    # full now: sits, content
        return 650, FLOOR, dict(mood="proud" if t > 26.6 else "happy", face=-0.2, look=(-1, 0))
    if t < T_BURP:          # cheeks puff
        return 650, FLOOR, dict(mood="blink", face=-0.6, sq=1.05)
    if t < T_BURP + 0.8:    # BURP
        return 650, FLOOR, dict(mood="chirp", face=-1, rot=-0.08, shake=3)
    if t < 30.8:
        return 650, FLOOR, dict(mood="proud", face=-0.3)
    if t < 32.6:            # belly pats: sleepy
        return 650, FLOOR, dict(mood="blink" if int(t * 2) % 3 else "proud", face=0.2, sq=1 + 0.02 * math.sin(t * 9))
    if t < T_PEEEP - 0.5:   # yawns
        return 650, FLOOR, dict(mood="chirp", face=0, look=(0, -1))
    if t < T_PEEEP:         # breathes in
        return 650, FLOOR, dict(mood="blink", sq=lerp(1, 1.12, ease(seg(t, T_PEEEP - 0.5, T_PEEEP))))
    if t < T_PEEEP + 0.9:   # PEEEEEP
        return 650, FLOOR, dict(mood="chirp", face=0, look=(0, -1), sq=1.1, shake=5, wings="flap", flap_t=t)
    if t < T_TURN:          # happily oblivious
        return 650, FLOOR, dict(mood="happy", face=0.6 if t > 35.2 else 0, look=(1, -0.4))
    if t < T_STOP:
        return 650, FLOOR, dict(mood="happy", face=0, look=(0, 0))
    return 650, FLOOR, dict(mood="blink" if 38.2 <= t < 38.35 else "happy", face=0, look=(0, 0))


def bot_grandma(t):
    """(x, y, kw) or None"""
    if t < T_GLAND - 0.6:
        return None
    if t < T_GLAND:   # springs in from the right
        x, y = hop((1180, FLOOR), (935, FLOOR), ease(seg(t, T_GLAND - 0.6, T_GLAND)), 260)
        return x, y, dict(look=(-1, 0), cane="up", mood="angry")
    if t < T_SWING - 0.15:
        return 935, FLOOR, dict(look=(-1, 0.5), cane="up", mood="angry", bow=-0.05 * math.sin(t * 3))
    if t < T_SWING + 0.35:   # the swing
        return 935, FLOOR, dict(look=(-1, 0.5), cane="down" if t >= T_SWING else "drum", mood="angry", bow=0.35 if t >= T_SWING else -0.2)
    if t < 26.4:
        return 935, FLOOR, dict(look=(-1, 0.3), cane="up", mood="angry")
    if t < T_CROWN_DROP:
        return 935, FLOOR, dict(look=(-1, 0), cane="down", mood="stern")
    if t < T_CROWN_DROP + 0.5:   # crown lands on her bun: one stern blink
        return 935, FLOOR, dict(look=(-1, 0), cane="down", mood="closed" if t < T_CROWN_DROP + 0.25 else "stern")
    if t < T_PEEEP + 0.9:
        return 935, FLOOR, dict(look=(-1, 0.2), cane="down", mood="stern" if t < T_PEEEP else "angry")
    if t < T_TURN:
        return 935, FLOOR, dict(look=(1, -0.3), cane="down", mood="stern")
    return 935, FLOOR, dict(look=(-1, 0.4), cane="down", mood="stern")


GRAN_HEAD = (-46, -202)
GSC = 1.35   # where a hat sits on Grandma's bun (relative to her feet)


def crown_pos(t):
    """Dill's crown in flight / on Grandma: (x, y, rot, scale) or None."""
    if T_BURP <= t < T_BURP + 0.9:   # blasted up and off to the left
        p = seg(t, T_BURP, T_BURP + 0.9)
        return lerp(484, 120, p), lerp(FLOOR - 390, FLOOR - 1100, ease_out(p)), -p * 4 * math.pi, 1.0
    if T_CROWN_DROP - 0.5 <= t < T_CROWN_DROP:   # drops out of the sky onto Grandma
        p = ease(seg(t, T_CROWN_DROP - 0.5, T_CROWN_DROP)) ** 1.6
        return lerp(950, 935 + GRAN_HEAD[0], p), lerp(FLOOR - 1100, FLOOR + GRAN_HEAD[1], p), lerp(2.0, -0.2, p), lerp(0.9, 0.72, p)
    if t >= T_CROWN_DROP:
        return 935 + GRAN_HEAD[0], FLOOR + GRAN_HEAD[1] + (6 if t < T_CROWN_DROP + 0.12 else 0), -0.2, 0.72
    return None


def food_bot(t):
    """Montage food item: (kind, x, y, extra) or None."""
    kinds = ["grape", "cheese", "pea"]
    hx, hy = CR_X + 118, FLOOR - 222
    for i, (ts, tt, tg) in enumerate(T_FOOD):
        if ts <= t < tt:
            s = back_out(seg(t, ts, ts + 0.25))
            if i == 1:   # held up high to show it off
                return kinds[i], hx + 10, hy - 40 * ease(seg(t, ts, ts + 0.3)), (s, 1.0 * ease(seg(t, 12.35, 12.75)))
            return kinds[i], hx, hy, (s, 0)
        if tt <= t < tg:
            p = seg(t, tt, tg)
            x, y = hop((hx + (10 if i == 1 else 0), hy - (40 if i == 1 else 0)), (PE_X - 18, FLOOR - 64), p, 120)
            return kinds[i], x, y, (lerp(1, 0.5, p) if i == 1 else 1, 1.0)
    return None


# ---------------- camera ----------------
def camera(t):
    """(cx, cy, zoom) in world coords."""
    if t < T_CUT:
        cx = lerp(700, 455, ease(seg(t, 2.0, 4.4)))
        z = 1.8
        if 5.0 <= t < 6.3:   # push in on the crumb hand-off
            k = ease(seg(t, 5.0, 5.4)) * (1 - ease(seg(t, 6.0, 6.3)))
            z += 0.0 * k
        cy = TOP - 190
        if 7.35 <= t < 7.6:
            s = 8 * (1 - seg(t, 7.35, 7.6))
            cx += random.uniform(-s, s); cy += random.uniform(-s, s)
        return cx, cy, z
    cx, cy, z = 640, FLOOR - 200, 1.62
    # cheese close-up: show off the Duck sticker
    k = ease(seg(t, 12.0, 12.4)) * (1 - ease(seg(t, 12.9, 13.3)))
    cx, cy, z = lerp(cx, CR_X + 128, k), lerp(cy, FLOOR - 300, k), lerp(z, 2.5, k)
    # slurp: slide left to the throne
    k2 = ease(seg(t, 16.0, 16.8)) * (1 - ease(seg(t, 20.0, 20.8)))
    cx = lerp(cx, 520, k2)
    # jello stand-off: slide right
    k3 = ease(seg(t, 21.2, 22.2)) * (1 - ease(seg(t, 26.0, 26.8)))
    cx, cy, z = lerp(cx, 830, k3), lerp(cy, FLOOR - 180, k3), lerp(z, 2.0, k3)
    # final group shot centre
    k4 = ease(seg(t, 26.2, 27.2))
    cx, cy, z = lerp(cx, 690, k4), lerp(cy, FLOOR - 230, k4), lerp(z, 1.8, k4)
    if T_BURP <= t < T_CROWN_DROP + 0.4:   # look up after the crown
        k5 = ease(seg(t, T_BURP + 0.1, T_BURP + 0.6)) * (1 - ease(seg(t, T_CROWN_DROP - 0.3, T_CROWN_DROP + 0.2)))
        cy -= 160 * k5
    if T_BURP <= t < T_BURP + 0.35:
        s = 14 * (1 - seg(t, T_BURP, T_BURP + 0.35))
        cx += random.uniform(-s, s); cy += random.uniform(-s, s)
    if T_PEEEP <= t < T_PEEEP + 0.9:
        s = 16 * (1 - seg(t, T_PEEEP, T_PEEEP + 0.9))
        cx += random.uniform(-s, s); cy += random.uniform(-s, s)
    for tt in T_THUMPS:
        if tt <= t < tt + 0.25:
            s = 12 * (1 - seg(t, tt, tt + 0.25))
            cy += random.uniform(-s, s)
    if t >= T_TURN:   # slow push toward Peep
        k6 = ease(seg(t, T_TURN, END_T))
        cx, cy, z = lerp(cx, 680, k6), lerp(cy, FLOOR - 280, k6), lerp(z, 2.05, k6)
    return cx, cy, z


# ---------------- scenes ----------------
def word(c, t, s, x, y, size, col, t0, t1, rot=0.0):
    if t0 <= t < t1:
        k = back_out(seg(t, t0, t0 + 0.2))
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(k), S(k)); text(c, s, 0, 0, size, col, olw=10); c.restore()


def top_scene(c, t):
    fridge6(c, DIM, 0, lid=False)
    lid_piece(c, 760, TOP - 25, 0.0)
    shell_half(c, EGG_X, TOP - 70, 0.0, top=False)
    x, y, kw = top_dill(t); dill(c, x, y, crown_on=True, **kw)
    x, y, kw, bite = top_crumb(t); crumb_bitten(c, x, y, bite, **kw)
    x, y, kw = top_peep(t); peep(c, x, y, **kw)
    fb = food_in_hand_top(t)
    if fb:
        bread_bit(c, fb[0], fb[1], 1.2)
    word(c, t, "SNAP!", 760, TOP - 330, 46, (1, 1, 1), 2.6, 3.0, -0.12)
    word(c, t, "SNAP!", 560, TOP - 360, 50, (1, 1, 1), 3.3, 3.7, 0.12)
    word(c, t, "crunch", 330, TOP - 380, 34, (1, 1, 1), 4.65, 5.1, -0.1)
    word(c, t, "munch", 760, TOP - 260, 36, (1, 1, 1), 6.1, 6.7, 0.1)
    if 6.05 <= t < 6.7:
        for j in range(2):
            q = ((t - 6.05) * 1.4 + j / 2) % 1
            heart(c, 670 + 30 * math.sin(j * 3 + q * 5), TOP - 200 - q * 120, 1.0, 1 - q)
    word(c, t, "PECK!", 600, TOP - 150, 44, (1, 1, 1), 7.35, 7.75, 0.15)
    word(c, t, "ow", 380, TOP - 360, 30, hexc("#FFE680"), 7.45, 8.1, -0.1)
    if 7.35 <= t < 8.0:   # crumbs fly off the corner
        q = seg(t, 7.35, 8.0)
        for i in range(5):
            a = -math.pi * (0.15 + 0.7 * i / 4)
            bread_bit(c, 525 + math.cos(a) * 110 * q, TOP - 40 + math.sin(a) * 110 * q + 160 * q * q, 0.5)
    if 8.6 <= t < 9.2:    # Dill's yelp
        word(c, t, "!!", 250, TOP - 420, 60, (1, 0.35, 0.35), 8.6, 9.2)
    if t >= 9.0:          # Crumb's idea
        k = math.sin(math.pi * seg(t, 9.0, 9.7))
        star(c, 450, TOP - 380, 30 * k, t * 5, GOLD)
    dark_overlay(c, DIM)


def thought_icon(c):
    """Crumb's worry: the Hand reaching down for Peep."""
    c.save(); c.rectangle(-118, -90, 236, 180); c.clip(); c.translate(0, 0); c.scale(0.26, 0.26)
    hand(c, 30, -40, grip=0.4)
    c.restore()
    c.save(); c.translate(-6, 78); c.scale(0.4, 0.4)
    peep(c, 0, 0, mood="happy")
    c.restore()


def bot_scene(c, t):
    fridge6(c, DIM, 0, lid=False)
    lid_piece(c, 760, TOP - 25, 0.0)
    jello(c, JELLO_X, FLOOR, 0.12 * math.sin(t * 20) * (1 - seg(t, T_SWING, T_SWING + 0.8)) if t >= T_SWING else
          (0.08 * math.sin(t * 25) if any(tt <= t < tt + 0.4 for tt in T_THUMPS) else 0))
    amt = 1 - ease(seg(t, T_SLURP0, T_SLURP1))
    butter_dish_left(c, DISH_X, FLOOR, amt)

    x, y, kw, has, tr = bot_dill(t)
    gs = bot_grandma(t)
    cr = bot_crumb(t)
    ps = bot_peep(t)
    fat = fatness(t)

    # Crumb walks behind Peep (26–27): draw him first then; otherwise Peep hops over him (draw Peep last).
    dill(c, x, y, crown_on=has, **kw)
    if tr > 0:
        tears(c, x, y, t, tr)
    if 16.0 <= t < 17.6:   # sweat drops while presenting the throne
        q = (t * 2) % 1
        ellipse(c, x + 70, y - 260 + q * 40, 8, 12, hexc("#74C0FC"), lw=3)
    crumb_bitten(c, cr[0], cr[1], 1.0, **cr[2])
    if gs:
        c.save(); c.translate(gs[0], gs[1]); c.scale(GSC, GSC); c.translate(-gs[0], -gs[1])
        grandma(c, gs[0], gs[1], **gs[2])
        c.restore()
    fat_peep(c, ps[0], ps[1], fat, **ps[2])

    cp = crown_pos(t)
    if cp:
        crown(c, cp[0], cp[1], cp[3], cp[2])

    f = food_bot(t)
    if f:
        kind, fx, fy, (s, extra) = f
        if kind == "grape":
            grape(c, fx, fy, 1.3 * s)
        elif kind == "cheese":
            cheese_slice(c, fx, fy - 60 * s, 0.9 * s, rot=0.08, duck_turn=extra if t < T_FOOD[1][1] else 1.0)
        else:
            pea(c, fx, fy, 1.2 * s)

    # ---- effects ----
    for i, (ts, tt, tg) in enumerate(T_FOOD):
        word(c, t, ["GULP!", "GONE!", "pop!"][i], PE_X + 40, FLOOR - 330, [52, 56, 44][i], (1, 1, 1), tg, tg + 0.55, 0.1 * (-1) ** i)
        if tg + 0.15 <= t < tg + 0.6:   # ding sparkle: rounder!
            star(c, PE_X + 90, FLOOR - 190, 26 * math.sin(math.pi * seg(t, tg + 0.15, tg + 0.6)), t * 5, GOLD)
    if 12.35 <= t < 12.9:   # the sticker Duck turns its head: a tiny sparkle
        star(c, CR_X + 175, FLOOR - 360, 14 * math.sin(math.pi * seg(t, 12.35, 12.9)), t * 4, (1, 1, 1))
    if 15.0 <= t < 15.9:    # empty-handed
        k = back_out(seg(t, 15.0, 15.2))
        c.save(); c.translate(CR_X, FLOOR - 400); c.scale(S(k), S(k)); text(c, "?", 0, 0, 80, hexc("#FFE680"), olw=10); c.restore()
    word(c, t, "SLURRRP!", DISH_X + 40, FLOOR - 330, 54, hexc("#FFE680"), T_SLURP0 + 0.1, T_SLURP1, -0.08)
    if 20.4 <= t < 21.6:
        word(c, t, "waaah", DISH_X - 60, FLOOR - 420, 40, hexc("#A5D8FF"), 20.4, 21.6, -0.12)
    if 21.4 <= t < 22.6:    # Peep eyes the jello
        k = math.sin(math.pi * seg(t, 21.4, 22.6))
        star(c, 790, FLOOR - 250, 18 * k, t * 6, (1, 1, 1))
    if T_SWING <= t < T_SWING + 0.35:   # swing arc
        q = seg(t, T_SWING, T_SWING + 0.35)
        c.save(); c.translate(915, FLOOR - 140)
        c.arc_negative(0, 0, 150, -math.pi * 0.35, -math.pi * (0.35 + 0.7 * q))
        c.set_source_rgba(1, 1, 1, 0.8 * (1 - q)); c.set_line_width(14); c.stroke(); c.restore()
    word(c, t, "WHIFF!", 820, FLOOR - 340, 50, (1, 1, 1), T_SWING, T_SWING + 0.6, -0.1)
    if T_BURP <= t < T_BURP + 0.8:      # burp shockwave rolls left
        q = seg(t, T_BURP, T_BURP + 0.8)
        for k in range(3):
            r = 60 + 380 * q - k * 70
            if r > 20:
                c.save(); c.translate(630, FLOOR - 120)
                c.arc(0, 0, r, math.pi * 0.62, math.pi * 1.32)
                c.set_source_rgba(0.85, 1, 0.75, 0.75 * (1 - q)); c.set_line_width(16); c.stroke(); c.restore()
    if T_BURP <= t < T_BURP + 1.2:
        k = back_out(seg(t, T_BURP, T_BURP + 0.2))
        c.save(); c.translate(660, FLOOR - 400); c.rotate(-0.08); c.scale(S(k), S(k))
        text(c, "BUUURP!", 0, 0, 84, hexc("#A9E34B"), olw=12); c.restore()
    word(c, t, "clink", 960, FLOOR - 230, 30, (1, 1, 1), T_CROWN_DROP, T_CROWN_DROP + 0.6, 0.12)
    if 30.8 <= t < 32.6:   # pat pat
        word(c, t, "pat", 760, FLOOR - 140, 30, (1, 1, 1), 30.9, 31.5, 0.1)
        word(c, t, "pat", 770, FLOOR - 200, 30, (1, 1, 1), 31.6, 32.2, -0.1)
    if 32.6 <= t < T_PEEEP:  # z's
        for j in range(2):
            q = ((t - 32.6) * 1.2 + j / 2) % 1
            text(c, "z", 700 + 40 * q + j * 20, FLOOR - 250 - 100 * q, 30 + 14 * q, (1, 1, 1), olw=6)
    if T_PEEEP <= t < T_PEEEP + 0.9:    # sound rings
        q = (t - T_PEEEP) * 2 % 1
        for k in range(2):
            r = 120 + 300 * ((q + k * 0.5) % 1)
            c.save(); c.translate(650, FLOOR - 120); c.arc(0, 0, r, 0, 2 * math.pi)
            c.set_source_rgba(1, 0.95, 0.6, 0.6 * (1 - (q + k * 0.5) % 1)); c.set_line_width(10); c.stroke(); c.restore()
    if T_TURN + 0.3 <= t < T_STOP + 1.3:
        s = back_out(seg(t, T_TURN + 0.3, T_TURN + 0.6))
        bubble(c, 610, FLOOR - 560, 0.95 * s, thought_icon)
    dark_overlay(c, DIM)


def light_spill(c, t):
    """Light leaking in at the door's edge (right side of the frame), screen space."""
    k = ease(seg(t, T_LIGHT, T_LIGHT + 1.2))
    if t >= T_STOP:
        k = 1.0
    if k <= 0:
        return
    w = 120 + 300 * k
    g = cairo.LinearGradient(W, 0, W - w, 0)
    g.add_color_stop_rgba(0, 1, 0.98, 0.85, 0.7 * k); g.add_color_stop_rgba(0.35, 1, 0.95, 0.7, 0.35 * k)
    g.add_color_stop_rgba(1, 1, 0.95, 0.7, 0)
    c.rectangle(W - w, 0, w, H); c.set_source(g); c.fill()
    # rays sweeping across
    for i in range(4):
        y0 = 500 + i * 330
        c.move_to(W, y0); c.line_to(W - 900 * k, y0 + 120 - i * 40); c.line_to(W - 900 * k, y0 + 210 - i * 40); c.line_to(W, y0 + 60)
        c.close_path(); c.set_source_rgba(1, 0.97, 0.8, 0.10 * k); c.fill()


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
        top_scene(c, t)
    else:
        bot_scene(c, t)
    c.restore()
    light_spill(c, t)
    if t < 2.4:
        iris(c, W / 2, H / 2, lerp(0, 1400, ease(seg(t, 2.0, 2.4))))
    if T_CUT - 0.12 <= t < T_CUT + 0.18:   # whip down to the bottom shelf
        a = 1 - abs(t - T_CUT) / 0.18
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.6 * max(0, a)); c.fill()
    # PEEEEEP: big word in screen space
    if T_PEEEP <= t < T_PEEEP + 1.0:
        k = back_out(seg(t, T_PEEEP, T_PEEEP + 0.2))
        c.save(); c.translate(W / 2 + random.uniform(-6, 6), 430); c.rotate(-0.05); c.scale(S(k), S(k))
        text(c, "PEEEEEEP!", 0, 0, 150, hexc("#FFE066"), olw=16); c.restore()
    for i, tt in enumerate(T_THUMPS):   # footsteps outside, at the door's edge
        if tt <= t < tt + 0.6:
            k = back_out(seg(t, tt, tt + 0.15))
            c.save(); c.translate(W - 200, 520 + i * 260); c.rotate(0.1 if i else -0.1); c.scale(S(k), S(k))
            text(c, "THUMP", 0, 0, 90, (0.9, 0.85, 1.0), olw=12); c.restore()
    if t >= T_STOP:   # record stop: freeze-frame tint
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.1, 0.05, 0.2, 0.18 * (1 - seg(t, T_STOP, T_STOP + 0.15) * 0.3)); c.fill()
    if t >= END_T - 0.4:
        iris(c, W / 2 + (650 - cx) * Z, H / 2 + (FLOOR - 110 - cy) * Z, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))


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
