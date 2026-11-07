"""FRIDGE KINGDOM — Episode 12: "Peep Learns to Fly". 40.0s, 1080x1920 @ 30fps.

Variant B (cold open): no title card; a small title banner sits across the top for the first 2s.

Cold open on the frosty top shelf: Peep flaps its stubby wings as hard as it can. Nothing. It holds up a
lettuce-scrap drawing of a flying Duck (Wilt's style); the drawn Duck turns its head to the camera. Dill
scoffs, marches to the shelf edge, poses, and jumps to show how it's done... BONK, straight onto Crumb on
the bottom shelf. Peep copies and lands on Crumb too. Training montage: a spoon catapult on the butter
block (Dill stomps the handle), a jello trampoline, a napkin parachute that flips inside out. Crumb is the
landing pad every time. Then Peep scrunches up, flaps like mad... and hovers! Everyone cheers. Peep keeps
rising, all the way up to the ceiling vent. tik... tik... tik. Peep head-butts the grille once: TONK.
Silence. Then one tik answers. Peep's wings stop. It drops like a stone into Crumb's arms, eyes huge.
Everyone looks up. tik. DUN DUN DUNNN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crown, dark_overlay, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp,
                 back_out, INK, GOLD, FLOOR, TOP, W, H, FPS, S)
from ep2 import end_card, jello, grape
from ep5 import JELLO_X
from ep6 import grandma, fridge6, lid_piece
from ep7 import confetti
from ep8 import shell_half
from ep9 import fat_peep, crumb_bitten, GRAN_HEAD
from ep10 import ceiling_vent, frost, fresh_butter, napkin_folded, napkin_tent, VENT_X
from animate import heart

DUR = 40.0
END_T = 38.5
DIM = 0.18
FAT = 1.5
GSC = 1.35
EGG_X = 900
DISH_X = 420
PIV = (470, FLOOR - 118)     # spoon lever pivot, resting on the butter block
SPOON_REST = 0.445           # bowl end down
SPOON_STOMP = -0.445         # handle end down
LETTUCE, LETTUCE_D = hexc("#C5D86D"), hexc("#94A84A")
SCR = (0.98, 1.0, 0.95)

# ---------------- timing ----------------
T_DROOP = 2.0
T_CARD = 2.4
T_DTURN = 3.6         # the drawn Duck turns its head
T_CARD_DOWN = 4.5
T_PFFT = 4.2
T_DWALK = 4.9
T_DPOSE = 5.7
T_DJUMP = 6.3
T_BONK = 7.15
T_ROLL = 8.3
T_PJUMP = 8.9
T_PLAND = 9.6
T_M1 = 11.0           # montage: spoon catapult
T_STOMP = 11.9
T_M1_LAND = 12.95
T_M2 = 13.4           # jello trampoline
T_BOING = 13.75
T_M2_LAND = 15.1
T_M3 = 15.8           # napkin parachute
T_FLIP = 16.9
T_M3_LAND = 17.35
T_HOV = 18.2          # hover attempt
T_FLAPS = 18.6
T_LIFT = 19.3
T_CHEER = 21.2
T_RISE = 22.8
T_ARRIVE = 28.3
T_TIKS = (29.6, 30.1, 30.6)
T_BUTT = 31.8
T_REPLY = 33.3
T_FREEZE = 33.9
T_DROP = 34.4
T_CATCH = 35.55
T_LOOK = 36.3
T_LASTTIK = 36.7
DUNS = (37.05, 37.5, 37.95)

P_TOP = 600           # Peep on the top shelf
D_TOP = 380           # Dill on the top shelf
EDGE_X = 860          # where Dill jumps
CR_X = 760            # Crumb on the bottom shelf (first catches)
GR_X = 150
GR_X2 = 300          # Grandma's spot from the parachute gag on
HV_PEEP, HV_DILL, HV_CRUMB = 640, 440, 840
VENT_FEET = 330       # Peep's feet when hovering under the vent


# ---------------- helpers ----------------
def hop(a, b, p, height=200):
    return lerp(a[0], b[0], p), lerp(a[1], b[1], p) - height * math.sin(math.pi * p)


def word(c, t, s, x, y, size, col, t0, t1, rot=0.0):
    if t0 <= t < t1:
        k = back_out(seg(t, t0, t0 + 0.2))
        c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(k), S(k)); text(c, s, 0, 0, size, col, olw=10); c.restore()


def squash_at(c, x, y, sq):
    c.translate(x, y); c.scale(S(1 + (1 - sq) * 0.7), S(sq)); c.translate(-x, -y)


def wing_up_t():
    return (math.pi / 2) / 40     # flap_t that freezes Peep's wings fully raised


# ---------------- new props ----------------
def spoon_lever(c, ang):
    """A teaspoon balanced on the butter block: bowl on the right, handle on the left."""
    c.save(); c.translate(*PIV); c.rotate(ang)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_source_rgb(*INK); c.set_line_width(30); c.move_to(-210, 0); c.line_to(110, 0); c.stroke()
    c.set_source_rgb(*hexc("#CED4DA")); c.set_line_width(20); c.move_to(-210, 0); c.line_to(110, 0); c.stroke()
    ellipse(c, 185, -10, 86, 34, hexc("#CED4DA"), lw=7)
    ellipse(c, 185, -18, 60, 18, hexc("#E9ECEF"), stroke=False)
    c.restore()


def spoon_bowl(ang):
    return PIV[0] + 185 * math.cos(ang) + 10 * math.sin(ang), PIV[1] + 185 * math.sin(ang) - 22 * math.cos(ang)


def spoon_handle_end(ang):
    return PIV[0] - 190 * math.cos(ang), PIV[1] - 190 * math.sin(ang) - 14


def spoon_ang(t):
    if t < T_STOMP:
        return SPOON_REST
    return lerp(SPOON_REST, SPOON_STOMP, ease_out(seg(t, T_STOMP, T_STOMP + 0.12)))


def duck_card(c, x, y, turn=0.0, s=1.0, rot=0.0):
    """A torn lettuce scrap with a scratched drawing of the Duck flying (wings out, motion lines)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(s), S(s))
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    rnd = random.Random(12)
    pts = []
    for i in range(24):
        a = 2 * math.pi * i / 24
        r = 1 + rnd.uniform(-0.06, 0.06)
        pts.append((150 * r * math.cos(a) * (1.05 if abs(math.cos(a)) > 0.7 else 1), 112 * r * math.sin(a)))
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.close_path()
    c.set_source_rgb(*LETTUCE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.set_source_rgba(*LETTUCE_D, 0.8); c.set_line_width(5)
    c.move_to(-130, 70); c.curve_to(-60, 40, 40, 70, 130, 40); c.stroke()

    def sl(ps, w=7):
        c.move_to(*ps[0])
        for p in ps[1:]:
            c.line_to(*p)
        c.set_source_rgba(*SCR, 0.95); c.set_line_width(w); c.stroke()
    # body
    c.save(); c.translate(-6, 18); c.scale(62, 34); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*SCR, 0.95); c.set_line_width(7); c.stroke()
    # big flapping wings
    sl([(-20, 4), (-60, -60), (-30, -50), (-10, -82), (10, -40), (14, 0)])
    sl([(-50, 22), (-70, 20), (-60, 30)], 6)  # tail
    # head (turns to camera)
    hx = lerp(46, 26, turn)
    c.save(); c.translate(hx, -18); c.scale(28, 26); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
    c.set_source_rgb(*LETTUCE); c.fill_preserve(); c.set_source_rgba(*SCR, 0.95); c.set_line_width(7); c.stroke()
    if turn < 0.5:
        sl([(hx + 24, -18), (hx + 50, -10), (hx + 24, -2)], 6)
        c.arc(hx + 8, -26, 4.5, 0, 2 * math.pi); c.set_source_rgba(*SCR, 1); c.fill()
    else:
        sl([(hx - 10, -6), (hx + 10, -6), (hx, 6), (hx - 10, -6)], 5)
        for ex in (-10, 10):
            c.arc(hx + ex, -24, 5, 0, 2 * math.pi); c.set_source_rgba(*SCR, 1); c.fill()
    # cap crown
    sl([(hx - 16, -42), (hx - 14, -58), (hx - 6, -48), (hx, -62), (hx + 6, -48), (hx + 14, -58), (hx + 16, -42)], 5)
    # motion lines
    for i, yy in enumerate((-30, 0, 30)):
        sl([(-140 + 10 * i, yy + 10), (-95 + 10 * i, yy + 10)], 5)
    c.restore()


def napkin_chute(c, x, y, flip=0.0, sway=0.0):
    """The blue-striped napkin held overhead as a parachute; flip 0..1 turns it inside out."""
    c.save(); c.translate(x, y); c.rotate(sway)
    dome = lerp(-1.0, 0.9, ease(flip))     # -1 normal dome; positive: inverted
    w = 190
    top = -340
    c.move_to(-w, top + 60)
    c.curve_to(-w * 0.6, top + 60 + 160 * dome, w * 0.6, top + 60 + 160 * dome, w, top + 60)
    for k in range(4):
        x0 = w - k * (2 * w / 4)
        c.curve_to(x0 - 15, top + 80, x0 - 35, top + 50, x0 - 2 * w / 4, top + 60)
    c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.set_source_rgba(*hexc("#4DABF7"), 0.9); c.set_line_width(8)
    c.move_to(-w + 20, top + 50); c.curve_to(-w * 0.4, top + 50 + 120 * dome, w * 0.4, top + 50 + 120 * dome, w - 20, top + 50); c.stroke()
    # strings to Peep's wings
    c.set_source_rgb(*INK); c.set_line_width(3)
    for sx in (-w, -w / 2, w / 2, w):
        c.move_to(sx, top + 62); c.line_to(sx * 0.25, -150); c.stroke()
    c.restore()


def vent_glow(c, k):
    """Faint icy light leaking out between the vent slats."""
    if k <= 0:
        return
    for i in range(5):
        rrect(c, VENT_X - 140, 36 + i * 18, 280, 9, 4)
        c.set_source_rgba(0.6, 0.85, 1.0, 0.7 * k); c.fill()


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
    text(c, "Ep. 12:  Peep Learns to Fly", W / 2, 182, 46, (1, 1, 1), olw=8)
    c.restore()


# ---------------- character states ----------------
def peep_state(t):
    """(x, y, kw) or None."""
    flap = dict(wings="flap", flap_t=t)
    if t < T_DROOP:      # flapping furiously on the top shelf, going nowhere
        lift = 26 * abs(math.sin(t * 9)) if 0.9 < t < 1.5 else 0
        return P_TOP, TOP - lift, dict(mood="blink", face=0, shake=5, sq=0.92 + 0.05 * math.sin(t * 40), **flap)
    if t < T_CARD:       # droops
        return P_TOP, TOP, dict(mood="blink", face=0, rot=0.12 * ease(seg(t, T_DROOP, T_DROOP + 0.3)), sq=0.9)
    if t < T_CARD_DOWN:  # holds up the drawing
        return P_TOP, TOP, dict(mood="happy" if t < T_PFFT else "proud", face=-0.3 if t > T_PFFT else 0, look=(0, -1) if t < T_DTURN else (-1, 0),
                                wings="flap", flap_t=wing_up_t())
    if t < T_PJUMP - 0.6:  # watches Dill, walks to the edge
        x = lerp(P_TOP, EDGE_X - 80, ease(seg(t, T_ROLL - 0.6, T_PJUMP - 0.6)))
        return x, TOP, dict(mood="shock" if T_BONK <= t < T_ROLL else "happy", face=0.6, look=(1, 0.5))
    if t < T_PJUMP:
        return EDGE_X - 80, TOP, dict(mood="proud", face=0.4, sq=lerp(1, 0.8, seg(t, T_PJUMP - 0.4, T_PJUMP)))
    if t < T_PLAND:      # copies Dill's jump
        p = seg(t, T_PJUMP, T_PLAND)
        x, y = hop((EDGE_X - 80, TOP), (CR_X, FLOOR - crumb_top(T_PLAND)), p, 120)
        return x, y, dict(mood="happy", face=0, rot=-0.5 * p, **flap)
    if t < T_M1:         # sitting on squashed Crumb, delighted
        return CR_X, FLOOR - crumb_top(t), dict(mood="proud" if t < 10.2 else "chirp", face=-0.3, look=(-1, 0))
    if t < T_M2:         # spoon catapult
        if t < T_STOMP + 0.05:
            bx, by = spoon_bowl(spoon_ang(t))
            return bx, by + 12, dict(mood="blink" if t > 11.4 else "happy", face=0.2, look=(1, -0.5), wings="flap", flap_t=wing_up_t())
        if t < T_M1_LAND:
            p = seg(t, T_STOMP + 0.05, T_M1_LAND)
            bx, by = spoon_bowl(SPOON_STOMP)
            x = lerp(bx, CR_X + 40, p)
            y = lerp(by, FLOOR - 270, p) - 620 * math.sin(math.pi * p) * (1.0 if p < 0.5 else 1.0)
            return x, y, dict(mood="shock" if p < 0.5 else "chirp", face=0.3, rot=3 * math.pi * p, **flap)
        return CR_X + 40, FLOOR - crumb_top(t, CR_X + 40), dict(mood="proud", face=0, look=(0, 0))
    if t < T_M3:         # jello trampoline
        jt = JELLO_X - 10
        if t < T_BOING:
            return jt, FLOOR - 150 + 12 * ease(seg(t, T_M2, T_BOING)), dict(mood="proud", face=-0.3, sq=lerp(1, 0.7, seg(t, T_M2 + 0.1, T_BOING)))
        if t < T_M2_LAND:
            p = seg(t, T_BOING, T_M2_LAND)
            x = lerp(jt, 800, ease(p))
            y = lerp(FLOOR - 150, FLOOR - 270, p) - 700 * math.sin(math.pi * p)
            return x, y, dict(mood="happy" if p < 0.45 else "shock", face=-0.2, wings="flap", flap_t=t, rot=0.2 * math.sin(t * 12))
        return 800, FLOOR - crumb_top(t, 800), dict(mood="blink", face=0, rot=0.3)
    if t < T_HOV:        # napkin parachute
        if t < T_FLIP:
            p = seg(t, T_M3, T_FLIP)
            return lerp(620, 760, p) + 40 * math.sin(t * 4), lerp(FLOOR - 1050, FLOOR - 650, p), dict(mood="proud", face=0.2, wings="flap", flap_t=wing_up_t())
        if t < T_M3_LAND:
            p = seg(t, T_FLIP, T_M3_LAND)
            return lerp(760 + 40 * math.sin(T_FLIP * 4), 800, p), lerp(FLOOR - 650, FLOOR - 300, p * p), dict(mood="shock", face=0, wings="flap", flap_t=t)
        return None      # under the napkin heap (head pops out, drawn separately)
    if t < T_LIFT:       # scrunches up and flaps like mad
        k = seg(t, T_FLAPS, T_LIFT)
        return HV_PEEP, FLOOR, dict(mood="blink", face=0, shake=3 + 4 * k, sq=lerp(1, 0.85, seg(t, T_HOV, T_FLAPS)),
                                    wings="flap" if t >= T_FLAPS else "down", flap_t=t * 1.6)
    if t < T_RISE:       # HOVERS
        h = 120 * ease(seg(t, T_LIFT, T_LIFT + 1.0)) + 10 * math.sin(t * 6)
        mood = "blink" if t < T_LIFT + 0.8 else ("proud" if t < T_CHEER else "happy")
        return HV_PEEP, FLOOR - h, dict(mood=mood, face=0, look=(0, 0), wings="flap", flap_t=t * 1.6)
    if t < T_ARRIVE:     # higher and higher
        p = ease(seg(t, T_RISE, T_ARRIVE))
        y = lerp(FLOOR - 120, VENT_FEET, p) + 10 * math.sin(t * 6)
        return lerp(HV_PEEP, VENT_X, p), y, dict(mood="happy", face=0, look=(0, -1) if p > 0.6 else (0, 0), wings="flap", flap_t=t * 1.6)
    if t < T_FREEZE:     # at the vent
        y = VENT_FEET + 8 * math.sin(t * 6)
        mood, look = "happy", (0, -1)
        jolt = 0
        for tt in T_TIKS:
            if tt <= t < tt + 0.25:
                jolt = 1
        if t >= T_TIKS[0]:
            mood = "shock" if jolt else "happy"
        if t >= T_TIKS[2] + 0.4:
            mood = "blink" if T_TIKS[2] + 0.6 < t < T_TIKS[2] + 0.8 else "happy"
        if T_BUTT - 0.3 <= t < T_BUTT + 0.4:    # head-butt the grille
            q = seg(t, T_BUTT - 0.3, T_BUTT + 0.4)
            y -= 70 * math.sin(math.pi * q) if q < 0.45 else 70 * math.sin(math.pi * 0.45) * (1 - (q - 0.45) / 0.55)
            mood = "proud" if q < 0.5 else "happy"
        if t >= T_REPLY:
            mood = "shock"
        return VENT_X, y, dict(mood=mood, face=0, look=look, wings="flap", flap_t=t * 1.6, shake=4 if jolt else 0)
    if t < T_DROP:       # wings stop
        return VENT_X, VENT_FEET - 10 * ease(seg(t, T_FREEZE, T_DROP)), dict(mood="shock", face=0, look=(0, 0), wings="flap", flap_t=wing_up_t(), shake=2)
    if t < T_CATCH:      # drops like a stone
        p = seg(t, T_DROP, T_CATCH)
        return lerp(VENT_X, HV_PEEP, p), lerp(VENT_FEET - 10, FLOOR - 300, p * p), dict(mood="shock", face=0, wings="flap", flap_t=wing_up_t())
    lk = (0, -1) if t >= T_LOOK else (0, 0)
    return HV_PEEP, FLOOR - crumb_top(t, HV_PEEP), dict(mood="shock", face=0, look=lk, shake=3 if t < DUNS[0] else 1.5,
                                                        wings="flap", flap_t=wing_up_t() if t < T_LOOK else 0.0)


def crumb_sq(t):
    """Crumb's squash (1 = normal)."""
    hits = [(T_BONK, 0.42, T_ROLL, 0.35), (T_PLAND, 0.6, 10.3, 0.3), (T_M1_LAND, 0.55, 13.3, 0.3),
            (T_M2_LAND, 0.5, 15.7, 0.3), (T_CATCH, 0.55, DUR, 0.3)]
    for t0, low, t1, rec in hits:
        if t0 <= t < t1 + rec:
            down = lerp(1, low, ease_out(seg(t, t0, t0 + 0.08)))
            if t0 == T_PLAND and t >= T_ROLL:
                pass
            if t >= t1:
                return lerp(down, 1.0, back_out(seg(t, t1, t1 + rec)))
            if t0 == T_CATCH:
                return lerp(low, 0.8, ease(seg(t, t0 + 0.2, t0 + 0.8)))
            return down
    return 1.0


def crumb_pos(t):
    if t < T_M1:
        return CR_X
    if t < T_M2:
        return CR_X + 40
    if t < T_M2 + 0.4:
        return lerp(CR_X + 40, 800, ease(seg(t, T_M2, T_M2 + 0.4)))
    if t < T_HOV:
        return 800
    if t < T_RISE:
        return lerp(800, HV_CRUMB, ease(seg(t, T_HOV, T_HOV + 0.5)))
    if t < T_DROP:
        return lerp(HV_CRUMB, HV_PEEP, ease(seg(t, T_RISE + 1.0, T_RISE + 2.5)))
    return HV_PEEP


def crumb_top(t, x=None):
    return 300 * crumb_sq(t) - 6


def crumb_state(t):
    x = crumb_pos(t)
    sq = crumb_sq(t)
    if t < T_DJUMP:
        return x, dict(mood="worried", look=(-1, -1)), sq
    if t < T_BONK:
        return x, dict(mood="scared", look=(0.5, -1), arm="wave"), sq
    if t < T_PJUMP:
        return x, dict(mood="dizzy"), sq
    if t < T_PLAND:
        return x, dict(mood="scared", look=(0.3, -1), arm="wave"), sq
    if t < T_M1:
        return x, dict(mood="dizzy" if t < 10.2 else "sheepish", look=(0, -1)), sq
    if t < T_M2:
        if t < T_M1_LAND:
            return x, dict(mood="scared", look=(-0.6, -1), arm="wave"), sq
        return x, dict(mood="dizzy"), sq
    if t < T_M3:
        if t < T_M2_LAND:
            return x, dict(mood="worried" if t < T_BOING else "scared", look=(1, -1), arm="wave" if t > 14.3 else "down"), sq
        return x, dict(mood="dizzy"), sq
    if t < T_HOV:
        if t < T_M3_LAND:
            return x, dict(mood="worried", look=(-0.4, -1), arm="wave" if t > T_FLIP else "down"), sq
        return x, dict(mood="dizzy"), sq
    if t < T_LIFT:
        return x, dict(mood="worried", look=(-1, 0)), sq
    if t < T_CHEER:
        return x, dict(mood="scared", look=(-1, -0.5)), sq
    if t < T_RISE + 1.0:
        hopy = 40 * abs(math.sin((t - T_CHEER) * 7)) if t < T_RISE else 0
        return x, dict(mood="sheepish", look=(-1, -1), arm="wave"), sq, hopy
    if t < T_DROP:
        return x, dict(mood="worried", look=(0, -1)), sq
    if t < T_CATCH:
        return x, dict(mood="scared", look=(0, -1), arm="wave"), sq
    return x, dict(mood="scared", look=(0, -1) if t >= T_LOOK else (0, -0.5), shake=1.5), sq


def dill_state(t):
    """(x, y, kw) or None when off-screen and irrelevant."""
    if t < T_PFFT:
        return D_TOP, TOP, dict(mood="smug" if t < T_CARD else ("proud" if t < T_DTURN else "shocked"), look=(1, 0) if t < T_DTURN else (1, -0.4))
    if t < T_DWALK:     # pfft
        return D_TOP, TOP, dict(mood="smug", look=(1, 0), arm="point")
    if t < T_DPOSE:
        p = ease(seg(t, T_DWALK, T_DPOSE))
        return lerp(D_TOP, EDGE_X, p), TOP - abs(math.sin(p * math.pi * 4)) * 16, dict(mood="proud", look=(1, 0))
    if t < T_DJUMP:
        return EDGE_X, TOP, dict(mood="proud", look=(0, 0), arm="up", sq=lerp(1, 0.82, seg(t, T_DJUMP - 0.25, T_DJUMP)))
    if t < T_BONK:       # the "flying lesson"
        p = seg(t, T_DJUMP, T_BONK)
        x, y = hop((EDGE_X, TOP), (CR_X, FLOOR - 120), p, 160)
        return x, y + 0 * p, dict(mood="proud" if p < 0.35 else "shocked", look=(0, 1) if p > 0.35 else (0, -0.5), arm="reach", rot=0.5 * p)
    if t < T_ROLL:       # sitting on flattened Crumb, seeing stars
        return CR_X, FLOOR - 120, dict(mood="frozen", look=(0.4 * math.sin(t * 8), 0.4 * math.cos(t * 8)), rot=0.15, sq=0.9)
    if t < T_ROLL + 0.6:
        p = ease(seg(t, T_ROLL, T_ROLL + 0.6))
        x, y = hop((CR_X, FLOOR - 120), (560, FLOOR), p, 80)
        return x, y, dict(mood="frozen", look=(-1, 0), rot=lerp(0.15, -0.3, p))
    if t < T_M1:
        return 560, FLOOR, dict(mood="angry" if t > 9.7 else "frozen", look=(1, -0.3), rot=-0.1 if t < 9.7 else 0, shake=1.5 if t > 9.7 else 0)
    if t < T_M2:         # catapult: hop onto the handle and stomp
        h0 = (230, FLOOR)
        if t < 11.5:
            return h0[0], h0[1], dict(mood="smug", look=(1, -0.3), sq=lerp(1, 0.85, seg(t, 11.2, 11.5)))
        if t < T_STOMP:
            hx, hy = spoon_handle_end(SPOON_REST)
            x, y = hop(h0, (hx, hy), seg(t, 11.5, T_STOMP), 240)
            return x, y, dict(mood="angry", look=(1, 1), arm="reach")
        hx, hy = spoon_handle_end(spoon_ang(t))
        return hx, hy, dict(mood="proud" if t > 12.2 else "angry", look=(1, -1), arm="reach" if t < 12.2 else "down",
                            sq=lerp(0.8, 1, back_out(seg(t, T_STOMP, T_STOMP + 0.3))))
    if t < T_HOV:
        return 560, FLOOR, dict(mood="shocked" if T_M2_LAND <= t < T_M2_LAND + 0.5 else "smug", look=(1, -0.6))
    if t < T_LIFT:
        return HV_DILL, FLOOR, dict(mood="smug", look=(1, 0))
    if t < T_CHEER:
        return HV_DILL, FLOOR, dict(mood="shocked", look=(1, -0.6))
    if t < T_RISE + 1.6:
        hy = 50 * abs(math.sin((t - T_CHEER) * 6)) if t < T_RISE + 0.6 else 0
        return HV_DILL, FLOOR - hy, dict(mood="proud", look=(1, -1), arm="reach")
    if t < T_CATCH:
        return HV_DILL, FLOOR, dict(mood="shocked" if t >= T_DROP else "proud", look=(0.6, -1))
    lk = (0.6, -1) if t >= T_LOOK else (1, 0)
    return lerp(HV_DILL, 410, ease(seg(t, T_CATCH, T_CATCH + 0.5))), FLOOR, dict(mood="shocked", look=lk, shake=1.5 if t >= T_LASTTIK else 0)


def gran_state(t):
    x, y, kw = _gran_state(t)
    return (GR_X2 if t >= T_M3 else GR_X), y, kw


def _gran_state(t):
    if t < T_LIFT:
        mood = "stern"
        if T_M3 <= t < T_FLIP:
            mood = "stern"
        return GR_X, FLOOR, dict(look=(1, -0.4), cane="down", mood=mood)
    if t < T_CHEER:
        return GR_X, FLOOR, dict(look=(1, -0.5), cane="down", mood="shock")
    if t < T_RISE + 1.6:
        hy = 30 * abs(math.sin((t - T_CHEER) * 6)) if t < T_RISE + 0.6 else 0
        return GR_X, FLOOR, dict(look=(1, -1), cane="up", mood="stern", hop=hy)
    lk = (1, -1) if t >= T_LOOK else (1, -0.3)
    return GR_X, FLOOR, dict(look=lk, cane="up" if t >= DUNS[0] else "down", mood="shock" if t >= T_LASTTIK else "stern")


# ---------------- camera ----------------
KEYS = [(0.0, 600, TOP - 260, 1.6), (T_PFFT, 560, TOP - 240, 1.5), (T_DWALK, 560, TOP - 240, 1.5),
        (T_DPOSE, 700, TOP - 240, 1.45), (T_DJUMP, 700, TOP - 240, 1.45), (T_DJUMP + 0.5, 660, 1080, 1.0),
        (T_BONK, 680, 1180, 1.05), (T_BONK + 0.35, 700, FLOOR - 330, 1.45), (T_PJUMP, 700, FLOOR - 400, 1.35),
        (T_M1 - 0.01, 700, FLOOR - 400, 1.35),
        (T_M1, 560, FLOOR - 430, 1.35), (T_M2 - 0.01, 600, FLOOR - 430, 1.35),
        (T_M2, 760, FLOOR - 440, 1.3), (T_M3 - 0.01, 760, FLOOR - 440, 1.3),
        (T_M3, 680, FLOOR - 480, 1.25), (T_HOV - 0.01, 700, FLOOR - 420, 1.32),
        (T_HOV, 570, FLOOR - 330, 1.45), (T_CHEER, 570, FLOOR - 360, 1.4), (T_RISE, 570, FLOOR - 380, 1.4)]


def keycam(keys, t):
    if t <= keys[0][0]:
        return keys[0][1:]
    for a, b in zip(keys, keys[1:]):
        if t < b[0]:
            if b[0] - a[0] < 0.02:
                return b[1:]
            p = ease(seg(t, a[0], b[0]))
            return tuple(lerp(a[i], b[i], p) for i in (1, 2, 3))
    return keys[-1][1:]


def camera(t):
    if t < T_RISE:
        cx, cy, z = keycam(KEYS, t)
    elif t < T_ARRIVE + 0.6:      # follow Peep up
        ps = peep_state(t)
        k = ease(seg(t, T_RISE, T_RISE + 1.2))
        cx = lerp(560, ps[0], k * 0.8)
        cy = lerp(FLOOR - 380, ps[1] - 160, k)
        z = lerp(1.4, 2.0, ease(seg(t, T_RISE + 2.5, T_ARRIVE + 0.6)))
        cy = max(cy, 370)
        cy = lerp(cy, 370, ease(seg(t, T_ARRIVE - 0.8, T_ARRIVE + 0.6)))
        cx = lerp(cx, VENT_X, ease(seg(t, T_ARRIVE - 0.8, T_ARRIVE + 0.6)))
    elif t < T_DROP:
        cx, cy, z = VENT_X, 370, lerp(2.0, 2.1, ease(seg(t, T_ARRIVE + 0.6, T_REPLY)))
    elif t < T_CATCH + 0.2:       # whip down with the falling chick
        ps = peep_state(min(t, T_CATCH - 0.01))
        p = seg(t, T_DROP, T_CATCH)
        cx = lerp(VENT_X, 620, p)
        cy = max(370, min(ps[1] - 120, FLOOR - 360))
        z = lerp(2.1, 1.45, ease(p))
    else:
        cx, cy, z = 600, FLOOR - 360, 1.45
        if t >= T_LOOK:   # push in on the faces
            k = ease(seg(t, T_LOOK, END_T))
            cx, cy, z = lerp(cx, 620, k), lerp(cy, FLOOR - 400, k), lerp(z, 1.75, k)
    shakes = [(T_BONK, 14), (T_PLAND, 8), (T_STOMP, 10), (T_M1_LAND, 8), (T_M2_LAND, 8), (T_M3_LAND, 6), (T_CATCH, 14),
              (T_BUTT, 8), (T_REPLY, 5)]
    for t0, s in shakes:
        if t0 <= t < t0 + 0.25:
            q = s * (1 - seg(t, t0, t0 + 0.25)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    for d in DUNS:
        if d <= t < d + 0.12:
            z += 0.1 * (1 - seg(t, d, d + 0.12))
    return cx, cy, z


# ---------------- scene ----------------
def draw_peep(c, ps):
    if ps is None:
        return
    x, y, kw = ps
    fat_peep(c, x, y, FAT, **kw)


def draw_crumb(c, t):
    st = crumb_state(t)
    x, kw, sq = st[0], st[1], st[2]
    hy = st[3] if len(st) > 3 else 0
    c.save(); squash_at(c, x, FLOOR - hy, sq)
    crumb_bitten(c, x, FLOOR - hy, 1.0, **kw)
    c.restore()


def draw_dill(c, t):
    ds = dill_state(t)
    if ds is None:
        return
    x, y, kw = ds
    dill(c, x, y, crown_on=False, **kw)


def draw_gran(c, t):
    x, y, kw = gran_state(t)
    c.save(); c.translate(x, y); c.scale(GSC, GSC); c.translate(-x, -y)
    grandma(c, x, y, **kw)
    c.restore()
    crown(c, x + GRAN_HEAD[0], y + GRAN_HEAD[1] - kw.get("hop", 0) * GSC, 0.72, -0.2)


def scene(c, t):
    L = DIM
    fridge6(c, L, 0, lid=False)
    lid_piece(c, 760, TOP - 25, 0.0)
    shell_half(c, EGG_X, TOP - 70, 0.0, top=False)
    ceiling_vent(c, L)
    if t >= T_ARRIVE:
        vent_glow(c, 0.5 * max(0, math.sin(math.pi * seg(t, T_REPLY - 0.1, T_REPLY + 0.9))) +
                  sum(0.3 * max(0, math.sin(math.pi * seg(t, tt, tt + 0.4))) for tt in T_TIKS + (T_LASTTIK,)))
    frost(c, t, 1.0)
    # meltwater puddle on the top shelf (from Ep 11's drip)
    ellipse(c, 300, TOP + 4, 70, 10, (0.75, 0.9, 1.0), lw=3)
    wob = 0.0
    if T_BOING - 0.35 <= t < T_BOING + 0.8:
        q = seg(t, T_BOING - 0.35, T_BOING)
        wob = -0.6 * q if t < T_BOING else 0.5 * math.sin((t - T_BOING) * 30) * (1 - seg(t, T_BOING, T_BOING + 0.8))
    jello(c, JELLO_X, FLOOR, wob)
    fresh_butter(c, DISH_X, FLOOR)
    if T_M1 <= t < T_M2:
        spoon_lever(c, spoon_ang(t))
    grape(c, 170, FLOOR - 26, 0.9)   # a stray grape by the carton
    # napkin: flat on the shelf until the parachute gag, then a heap
    if t < T_M3:
        c.save(); c.translate(730, FLOOR); c.scale(2.2, 0.8); napkin_folded(c, 0, 0); c.restore()

    ps = peep_state(t)
    on_top_shelf = t < T_PJUMP
    # top shelf layer
    if on_top_shelf:
        if t < T_CARD_DOWN and t >= T_CARD:
            draw_peep(c, ps)
            k = back_out(seg(t, T_CARD, T_CARD + 0.3))
            if t > T_CARD_DOWN - 0.25:
                k = 1 - ease(seg(t, T_CARD_DOWN - 0.25, T_CARD_DOWN))
            duck_card(c, P_TOP, TOP - 380, ease(seg(t, T_DTURN, T_DTURN + 0.35)), 1.05 * k, 0.05 * math.sin(t * 3))
        else:
            draw_peep(c, ps)
    if t < T_BONK:
        draw_dill(c, t)
    # bottom shelf layer
    draw_gran(c, t)
    if t >= T_BONK:
        draw_dill(c, t)
    draw_crumb(c, t)
    if T_M3_LAND <= t < T_HOV:   # napkin heap over Crumb, Peep's head poking out
        q = back_out(seg(t, T_M3_LAND, T_M3_LAND + 0.2))
        napkin_tent(c, 800, FLOOR, q, wob=math.sin(t * 9) * 0.5)
        if t > T_M3_LAND + 0.4:
            k = back_out(seg(t, T_M3_LAND + 0.4, T_M3_LAND + 0.65))
            fat_peep(c, 800, FLOOR - 300 + 140 * (1 - k), FAT, mood="happy", face=0.3, look=(-1, -0.3))
    if T_HOV <= t:
        napkin_tent(c, 960, FLOOR, 0.0) if False else None
        c.save(); c.translate(900, FLOOR); c.scale(2.0, 0.8); napkin_folded(c, 0, 0); c.rotate(0.1); c.restore()
    if not on_top_shelf:
        draw_peep(c, ps)
    if T_M3 <= t < T_M3_LAND and ps:
        napkin_chute(c, ps[0], ps[1], ease(seg(t, T_FLIP, T_FLIP + 0.25)), 0.15 * math.sin(t * 4) if t < T_FLIP else 0.4 * math.sin(t * 20))

    # ---------------- effects ----------------
    if t < T_DROOP:   # flap flap flap + feather fluff
        for i, t0 in enumerate([0.15, 0.7, 1.25]):
            word(c, t, "flap", P_TOP - 170 + 170 * i, TOP - 340 - 30 * (i % 2), 40, (1, 1, 1), t0, T_DROOP, 0.12 * (-1) ** i)
        for j in range(3):
            q = (t * 1.4 + j / 3) % 1
            ellipse(c, P_TOP - 90 + 90 * j + 30 * math.sin(q * 6), TOP - 200 + 160 * q, 9, 5, hexc("#FFF3A6"), lw=3)
    if T_DROOP + 0.1 <= t < T_CARD:
        word(c, t, "...", P_TOP + 120, TOP - 280, 60, (1, 1, 1), T_DROOP + 0.1, T_CARD)
    if T_DTURN <= t < T_DTURN + 0.6:
        star(c, P_TOP + 90, TOP - 470, 22 * math.sin(math.pi * seg(t, T_DTURN, T_DTURN + 0.6)), t * 5, (1, 1, 1))
    word(c, t, "peep!", P_TOP + 150, TOP - 220, 40, hexc("#FFE680"), T_CARD + 0.1, T_CARD + 0.8, 0.1)
    word(c, t, "pfft!", D_TOP + 40, TOP - 380, 50, (1, 1, 1), T_PFFT, T_DWALK + 0.2, -0.1)
    if T_DPOSE <= t < T_DJUMP:
        star(c, EDGE_X + 70, TOP - 400, 22 * math.sin(math.pi * seg(t, T_DPOSE, T_DJUMP)), t * 5, GOLD)
    word(c, t, "WHOOSH", 900, TOP + 120, 54, (1, 1, 1), T_DJUMP + 0.1, T_BONK, -0.1)
    word(c, t, "BONK!", CR_X, FLOOR - 470, 80, (1, 1, 1), T_BONK, T_BONK + 0.8, 0.1)
    if T_BONK <= t < T_ROLL + 0.5:   # stars circling Dill
        for j in range(3):
            a = t * 6 + j * 2.1
            star(c, CR_X + 90 * math.cos(a), FLOOR - 440 + 22 * math.sin(a), 16, t * 4, GOLD)
    word(c, t, "oof", CR_X - 140, FLOOR - 150, 44, (1, 1, 1), T_PLAND, T_PLAND + 0.6, -0.1)
    word(c, t, "peep peep!", CR_X + 60, FLOOR - 560, 40, hexc("#FFE680"), 10.2, T_M1, 0.08)
    # montage 1
    word(c, t, "STOMP!", 300, FLOOR - 420, 56, (1, 1, 1), T_STOMP, T_STOMP + 0.6, -0.1)
    word(c, t, "WHEEE!", 860, FLOOR - 860, 50, hexc("#FFE680"), T_STOMP + 0.15, 12.6, 0.1)
    word(c, t, "OOF!", 900, FLOOR - 640, 52, (1, 1, 1), T_M1_LAND, T_M1_LAND + 0.5, -0.1)
    # montage 2
    word(c, t, "BOING!", JELLO_X - 40, FLOOR - 300, 60, hexc("#FF8FB3"), T_BOING, T_BOING + 0.6, 0.1)
    word(c, t, "flap flap", 640, FLOOR - 950, 40, (1, 1, 1), 14.1, 14.7, -0.06)
    word(c, t, "SPLAT!", 960, FLOOR - 480, 52, (1, 1, 1), T_M2_LAND, T_M2_LAND + 0.5, -0.1)
    # montage 3
    word(c, t, "floaty~", 920, FLOOR - 900, 40, (1, 1, 1), T_M3 + 0.3, T_FLIP, 0.08)
    word(c, t, "WHOOP!", 560, FLOOR - 860, 52, (1, 1, 1), T_FLIP, T_FLIP + 0.5, 0.12)
    word(c, t, "POOF", 980, FLOOR - 330, 52, (1, 1, 1), T_M3_LAND, T_M3_LAND + 0.6, -0.1)
    if T_M3_LAND <= t < T_M3_LAND + 0.6:
        q = seg(t, T_M3_LAND, T_M3_LAND + 0.6)
        for j in range(6):
            a = math.pi * (1 + j / 5)
            ellipse(c, 800 + math.cos(a) * 220 * q, FLOOR - 40 + math.sin(a) * 80 * q, 30 * (1 - q) + 6, 18 * (1 - q) + 4, (1, 1, 1), stroke=False)
    # hover
    if T_FLAPS <= t < T_CHEER:   # dust whirl under Peep
        for j in range(5):
            q = (t * 2.5 + j / 5) % 1
            ellipse(c, HV_PEEP - 160 + j * 80 + 40 * q * (1 if j % 2 else -1), FLOOR - 10 - 30 * q, 26 * (1 - q) + 6, 12 * (1 - q) + 3, (1, 1, 1), stroke=False)
        for i, t0 in enumerate([18.7, 19.0, 19.3, 19.6]):
            word(c, t, "flap", HV_PEEP - 220 + 150 * i, FLOOR - 560 - 40 * (i % 2), 40, (1, 1, 1), t0, T_LIFT + 0.9, 0.12 * (-1) ** i)
    if T_LIFT + 0.9 <= t < T_CHEER:
        word(c, t, "!", HV_DILL, FLOOR - 400, 90, (1, 0.9, 0.4), T_LIFT + 0.9, T_CHEER)
        word(c, t, "!", HV_CRUMB, FLOOR - 400, 90, (1, 0.9, 0.4), T_LIFT + 1.0, T_CHEER)
        word(c, t, "!", GR_X, FLOOR - 360, 90, (1, 0.9, 0.4), T_LIFT + 1.1, T_CHEER)
    word(c, t, "YAAAY!", 560, FLOOR - 640, 80, GOLD, T_CHEER, T_RISE + 0.5, -0.06)
    confetti(c, t, T_CHEER, 560, FLOOR - 300, n=70, seed=12)
    if T_CHEER <= t < T_RISE + 1.0:
        for j in range(4):
            q = ((t - T_CHEER) * 1.2 + j / 4) % 1
            heart(c, HV_CRUMB + 70 * math.sin(j * 2 + q * 4), FLOOR - 330 - q * 160, 1.0, 1 - q)
    if T_RISE <= t < T_ARRIVE:   # rising sparkle trail
        ps2 = peep_state(t)
        for j in range(4):
            tt = t - j * 0.15
            pj = peep_state(max(T_RISE, tt))
            star(c, pj[0] + 50 * math.sin(tt * 7), pj[1] + 40 + j * 30, 14 - 3 * j, tt * 5, (1, 1, 1))
        word(c, t, "higher...", ps2[0] + 230, ps2[1] - 180, 40, (1, 1, 1), T_RISE + 0.8, T_RISE + 2.6, 0.1)
        word(c, t, "HIGHER!", ps2[0] - 220, ps2[1] - 220, 48, GOLD, T_RISE + 2.8, T_ARRIVE - 0.6, -0.1)
    if T_ARRIVE <= t < T_TIKS[0]:
        word(c, t, "?", VENT_X + 140, VENT_FEET - 300, 80, hexc("#FFE680"), T_ARRIVE + 0.4, T_TIKS[0])
    for i, tt in enumerate(T_TIKS):   # frost dust shaken from the vent
        if tt <= t < tt + 0.8:
            q = seg(t, tt, tt + 0.8)
            for j in range(6):
                ellipse(c, VENT_X - 140 + j * 56 + 10 * i, 150 + q * 260 + 20 * (j % 2), 5, 5, (0.95, 0.98, 1), stroke=False)
    if T_BUTT <= t < T_BUTT + 0.6:
        word(c, t, "TONK!", VENT_X, -25, 64, (1, 1, 1), T_BUTT, T_BUTT + 0.6, 0.12)
        star(c, VENT_X - 90, 160, 20 * math.sin(math.pi * seg(t, T_BUTT, T_BUTT + 0.6)), t * 5, (1, 1, 1))
    if T_REPLY <= t < T_DROP:
        word(c, t, "!", VENT_X + 150, VENT_FEET - 280, 100, (1, 0.35, 0.35), T_REPLY + 0.3, T_DROP)
    if ps and T_DROP <= t < T_CATCH:
        word(c, t, "AAAAA!", ps[0], ps[1] - 490, 56, hexc("#FFE680"), T_DROP + 0.15, T_CATCH, 0.1)
    if T_DROP <= t < T_CATCH and ps:  # speed lines above the falling chick
        for j in range(4):
            c.move_to(ps[0] - 90 + 60 * j, ps[1] - 290 - 30 * (j % 2)); c.line_to(ps[0] - 90 + 60 * j, ps[1] - 400 - 30 * (j % 2))
            c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(7); c.stroke()
    word(c, t, "THUD", HV_PEEP + 220, FLOOR - 260, 64, (1, 1, 1), T_CATCH, T_CATCH + 0.6, -0.1)
    if T_CATCH + 0.3 <= t < END_T:   # Peep trembling: sweat drops
        q = (t * 2) % 1
        ellipse(c, HV_PEEP - 110, FLOOR - 470 + q * 50, 9, 13, hexc("#74C0FC"), lw=3)
        ellipse(c, HV_PEEP + 110, FLOOR - 450 + ((q + 0.5) % 1) * 50, 9, 13, hexc("#74C0FC"), lw=3)
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
    for tm in (T_M1, T_M2, T_M3, T_HOV):   # montage cuts: quick white flash
        if tm <= t < tm + 0.15:
            c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.6 * (1 - seg(t, tm, tm + 0.15))); c.fill()
    # tik tik tik from inside the vent (screen space, top of frame)
    for i, tt in enumerate(T_TIKS):
        if tt <= t < T_BUTT:
            k = back_out(seg(t, tt, tt + 0.15))
            c.save(); c.translate([290, 540, 790][i], 330 + 30 * (i % 2)); c.rotate([-0.12, 0.05, 0.14][i]); c.scale(S(k), S(k))
            text(c, "tik", 0, 0, 96, hexc("#D0EBFF"), olw=12); c.restore()
    if T_REPLY <= t < T_DROP:
        k = back_out(seg(t, T_REPLY, T_REPLY + 0.15))
        c.save(); c.translate(W / 2, 300); c.scale(S(k), S(k)); text(c, "tik.", 0, 0, 130, hexc("#D0EBFF"), olw=14); c.restore()
    if T_LASTTIK <= t < END_T:
        k = back_out(seg(t, T_LASTTIK, T_LASTTIK + 0.15))
        c.save(); c.translate(W / 2, 280); c.rotate(-0.05); c.scale(S(k), S(k)); text(c, "tik.", 0, 0, 120, hexc("#D0EBFF"), olw=14); c.restore()
    if t >= T_REPLY and t < T_DROP:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.3, 0.6, 1.0, 0.10 * ease(seg(t, T_REPLY, T_REPLY + 0.3))); c.fill()
    if t >= DUNS[0]:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.3, 0.6, 1.0, 0.14 * ease(seg(t, DUNS[0], DUNS[0] + 0.3))); c.fill()
    if t >= END_T - 0.4:
        cx, cy, Z = camera(t)
        iris(c, W / 2 + (HV_PEEP - cx) * Z, H / 2 + (FLOOR - 380 - cy) * Z, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))
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
