"""FRIDGE KINGDOM — Episode 8: "It Hatched". 38.2s, 1080x1920 @ 30fps.

Variant B (cold open): no title card; a small title banner sits across the top for the first 2s.

The top-shelf egg bursts and Peep tumbles out, wearing the top of its shell as a helmet. Dill and Crumb
haul themselves up onto the top shelf. Dill poses for the chick; it looks right past him and falls in love
with Crumb. Peep copies Crumb's every move (step, hop, salute). Jealous Dill poses with his sword; Peep
hops on his head, pecks his crown off and wears it. Dill lunges, crashes into Crumb, and Peep sits on the
pile. A soap bubble drifts in from the door seal with a tiny reflection of the Duck in its bath; it pops on
Peep's beak, Peep sneezes, and the crown flies back onto Dill. Then Peep's tummy rumbles... and it turns
to Dill, beak open. DUN DUN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, duck, crown, dark_overlay, ellipse, rrect, star, text,
                 iris, hexc, seg, ease, ease_out, lerp, back_out, INK, GOLD, FLOOR, TOP, W, H, FPS, S)
from ep2 import end_card
from ep4 import WHITE
from ep5 import cap_crown, crumb_notched
from ep6 import fridge6, lid_piece
from animate import heart

DUR = 38.2
END_T = 36.6
DIM = 0.18
EGG_X = 900
PEEP_C = hexc("#FFF3A6")      # pale lemon fluff (paler than the Duck)
PEEP_S = hexc("#FFE066")      # fluff shading
BEAK = hexc("#FF922B")

# ---------------- timing ----------------
T_C1, T_C2, T_POP = 0.9, 1.7, 2.5
T_HELM = 3.6                  # shell top lands on Peep's head
T_DSTRIDE = 9.0
T_SCRATCH = 10.8
T_RUN = 13.0
T_PECK1, T_PECK2, T_CROWN_OFF = 23.4, 23.65, 23.85
T_LUNGE, T_BONK = 26.0, 26.6
T_UP = 29.6
T_BUB0, T_BPOP = 30.2, 32.7
T_SNEEZE = 32.9
T_CROWN_BACK = 33.6
T_RUMBLE = 34.1
T_CLOSE = 35.0
DUNS = (35.1, 35.55, 36.0)


# ---------------- Peep ----------------
ZIG = [(-70 + 14 * i, -8 if i % 2 else 8) for i in range(11)]


def shell_half(c, x, y, rot=0.0, top=True, s=1.0):
    """Half of Peep's eggshell. (x, y) is the centre of the zig-zag rim."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(s), S(s))
    c.save()
    c.move_to(*ZIG[0])
    for p in ZIG[1:]:
        c.line_to(*p)
    yy = -120 if top else 120
    c.line_to(80, yy); c.line_to(-80, yy); c.close_path(); c.clip()
    ellipse(c, 0, 0, 56, 70, WHITE, lw=6)
    if top:
        ellipse(c, -20, -32, 9, 16, (1, 1, 1), stroke=False)
    else:
        ellipse(c, 0, 30, 40, 18, (0.9, 0.88, 0.82), stroke=False)
    c.restore()
    # rim
    c.save(); c.translate(0, 0)
    pts = [(px, py) for px, py in ZIG if abs(px) <= 56]
    c.move_to(*pts[0])
    for p in pts[1:]:
        c.line_to(*p)
    c.set_source_rgb(*INK); c.set_line_width(5); c.set_line_join(cairo.LINE_JOIN_MITER); c.stroke()
    c.restore()
    c.restore()


def fluff_path(c, cx, cy, r, n=14, bump=7):
    for i in range(n + 1):
        a = i / n * 2 * math.pi
        a2 = (i + 0.5) / n * 2 * math.pi
        if i == 0:
            c.move_to(cx + r * math.cos(a), cy + r * math.sin(a))
        else:
            c.curve_to(cx + (r + bump) * math.cos(a2 - 0.12), cy + (r + bump) * math.sin(a2 - 0.12),
                       cx + (r + bump) * math.cos(a2 + 0.12), cy + (r + bump) * math.sin(a2 + 0.12),
                       cx + r * math.cos(a), cy + r * math.sin(a))
    c.close_path()


def peep(c, x, y, mood="happy", look=(0, 0), wings="down", rot=0.0, helmet=True, helmet_rot=-0.22,
         crowned=False, sq=1.0, shake=0.0, flap_t=0.0, face=0.0):
    """Peep the chick. (x, y) = feet on the floor. face: -1 faces left .. 1 faces right (beak offset)."""
    c.save(); c.translate(x + shake * random.uniform(-1, 1), y); c.rotate(rot); c.scale(1 / S(sq) ** 0.5, S(sq))
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    # feet
    c.set_source_rgb(*BEAK); c.set_line_width(7)
    for fx in (-22, 22):
        c.move_to(fx, -18); c.line_to(fx, -2)
        for dx in (-12, 0, 12):
            c.move_to(fx, -2); c.line_to(fx + dx, 2)
    c.stroke()
    # wings (behind body for "down")
    def wing(side, ang):
        c.save(); c.translate(side * 56, -70); c.rotate(side * ang)
        ellipse(c, side * 14, 0, 22, 34, PEEP_S, lw=5)
        c.restore()
    if wings == "flap":
        a = 0.9 + 0.6 * math.sin(flap_t * 40)
        wing(-1, a); wing(1, a)
    elif wings == "salute":
        wing(-1, 0.3)
    elif wings == "hug":
        pass
    else:
        wing(-1, 0.3); wing(1, 0.3)
    # body
    fluff_path(c, 0, -76, 62)
    c.set_source_rgb(*PEEP_C); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    ellipse(c, 6, -44, 34, 22, (1, 1, 0.85), stroke=False)      # pale tummy
    # tuft (pokes through the helmet)
    c.set_source_rgb(*PEEP_S); c.set_line_width(7)
    for k, a in enumerate((-0.45, 0.0, 0.45)):
        c.save(); c.translate(0, -146 if not helmet else -176); c.rotate(a + helmet_rot * 0.4)
        c.move_to(0, 0); c.curve_to(-6, -14, 8, -22, 2, -34)
        c.set_source_rgb(*INK); c.set_line_width(10); c.stroke_preserve()
        c.set_source_rgb(*PEEP_S); c.set_line_width(5); c.stroke()
        c.restore()
    # eyes
    lx, ly = look
    fo = face * 10
    for ex in (-25, 25):
        exx = ex + fo
        if mood == "love":
            heart(c, exx, -92, 1.35 + 0.12 * math.sin(flap_t * 12), 1.0)
        elif mood in ("proud", "blink"):
            c.set_source_rgb(*INK); c.set_line_width(6)
            if mood == "proud":
                c.arc(exx, -88, 12, math.pi * 1.1, math.pi * 1.9)
            else:
                c.move_to(exx - 13, -90); c.line_to(exx + 13, -90)
            c.stroke()
        elif mood == "sneeze":
            c.set_source_rgb(*INK); c.set_line_width(6)
            d = 1 if ex < 0 else -1
            c.move_to(exx - 12 * d, -100); c.line_to(exx + 10 * d, -90); c.line_to(exx - 12 * d, -80); c.stroke()
        else:
            big = 1.25 if mood in ("shock", "hungry") else 1.0
            ellipse(c, exx + lx * 4, -90 + ly * 4, 16 * big, 20 * big, INK, stroke=False)
            ellipse(c, exx + lx * 4 + 5, -98 + ly * 4, 6 * big, 7 * big, (1, 1, 1), stroke=False)
            ellipse(c, exx + lx * 4 - 5, -82 + ly * 4, 2.5, 2.5, (1, 1, 1), stroke=False)
            if mood == "hungry":   # intense little glints
                star(c, exx + lx * 4 + 5, -98 + ly * 4, 7, flap_t * 4, (1, 1, 1))
    # cheeks
    for ex in (-38, 38):
        ellipse(c, ex + fo, -66, 10, 6, hexc("#FFB3C6"), stroke=False)
    # beak
    bx = fo + face * 6
    if mood in ("hungry", "sneeze", "chirp"):
        op = 26 if mood == "hungry" else 16
        c.move_to(bx - 16, -70); c.line_to(bx + 16, -70); c.line_to(bx, -82); c.close_path()
        c.set_source_rgb(*BEAK); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        c.move_to(bx - 16, -66); c.line_to(bx + 16, -66); c.line_to(bx, -66 + op); c.close_path()
        c.set_source_rgb(*BEAK); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
        ellipse(c, bx, -67, 13, 4 + op * 0.12, hexc("#7A1F2B"), stroke=False)
        if mood == "hungry":   # drool
            dl = 10 + 14 * abs(math.sin(flap_t * 3))
            c.move_to(bx + 10, -56); c.curve_to(bx + 12, -56 + dl, bx + 18, -56 + dl, bx + 18, -56 + dl * 0.6)
            ellipse(c, bx + 15, -56 + dl, 6, 8, hexc("#A5D8FF"), lw=3)
    else:
        c.move_to(bx - 14, -72); c.line_to(bx + 14, -72); c.line_to(bx, -54); c.close_path()
        c.set_source_rgb(*BEAK); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    # front wings
    if wings == "salute":
        c.save(); c.translate(52, -88); c.rotate(-1.9)
        ellipse(c, 20, 0, 22, 32, PEEP_S, lw=5); c.restore()
    if wings == "hug":
        for side in (-1, 1):
            c.save(); c.translate(side * 40, -66); c.rotate(side * -0.9)
            ellipse(c, 0, 10, 20, 32, PEEP_S, lw=5); c.restore()
    if helmet:
        shell_half(c, 0, -118, helmet_rot, True, 1.18)
    if crowned:
        crown(c, -6 + 30 * math.sin(helmet_rot), -192, 0.62, helmet_rot)
    c.restore()


# ---------------- soap bubble with the Duck's reflection ----------------
def soap_bubble(c, x, y, r, t, alpha=1.0):
    c.save()
    c.push_group()
    c.save(); c.translate(x, y); c.arc(0, 0, r, 0, 2 * math.pi); c.restore()
    g = cairo.RadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r)
    g.add_color_stop_rgba(0, 0.9, 0.97, 1, 0.25); g.add_color_stop_rgba(0.75, 0.75, 0.85, 1, 0.35)
    g.add_color_stop_rgba(1, 0.95, 0.75, 1, 0.75)
    c.set_source(g); c.fill_preserve()
    c.save(); c.clip()
    # the reflection: the Duck bobbing in bath foam (curved, tinted)
    bob = 4 * math.sin(t * 5)
    c.save(); c.translate(x, y + r * 0.35 + bob); c.scale(r / 190, r / 190)
    duck(c, 0, 40, turn=1.0)
    cap_crown(c, 6, -146, 0.38)
    c.restore()
    for i in range(5):
        ellipse(c, x - r * 0.75 + i * r * 0.38, y + r * 0.6, r * 0.24, r * 0.14, (1, 1, 1), stroke=False)
    # swirl of rainbow sheen
    for k, col in enumerate(((1, 0.6, 0.85), (0.6, 0.9, 1), (0.8, 1, 0.6))):
        c.save(); c.translate(x, y); c.rotate(t * 0.8 + k * 2.1)
        c.arc(0, 0, r * 0.86, 0.2, 1.3); c.restore()
        c.set_source_rgba(*col, 0.55); c.set_line_width(r * 0.08); c.stroke()
    c.restore()
    c.save(); c.translate(x, y); c.arc(0, 0, r, 0, 2 * math.pi); c.restore()
    c.set_source_rgba(*INK, 0.6); c.set_line_width(5); c.stroke()
    ellipse(c, x - r * 0.42, y - r * 0.45, r * 0.16, r * 0.1, (1, 1, 1), stroke=False)
    ellipse(c, x - r * 0.2, y - r * 0.62, r * 0.06, r * 0.05, (1, 1, 1), stroke=False)
    c.pop_group_to_source(); c.paint_with_alpha(alpha)
    c.restore()


def bubble_pos(t):
    p = ease(seg(t, T_BUB0, T_BPOP))
    x = lerp(1150, 548, p)
    y = lerp(TOP - 560, TOP - 236, p ** 2.2) + 30 * math.sin(p * 7) * (1 - p)
    return x, y


def pop_burst(c, x, y, t, t0):
    q = seg(t, t0, t0 + 0.4)
    if 0 < q < 1:
        for i in range(10):
            a = i / 10 * 2 * math.pi
            r1, r2 = 40 + 120 * q, 60 + 150 * q
            c.move_to(x + r1 * math.cos(a), y + r1 * math.sin(a)); c.line_to(x + r2 * math.cos(a), y + r2 * math.sin(a))
        c.set_source_rgba(0.85, 0.95, 1, 1 - q); c.set_line_width(8); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()


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
    text(c, "Ep. 8:  It Hatched", W / 2, 182, 46, (1, 1, 1), olw=8)
    c.restore()


def hop(a, b, p, height=200):
    return lerp(a[0], b[0], p), lerp(a[1], b[1], p) - height * math.sin(math.pi * p)


# ---------------- character states ----------------
def peep_state(t):
    """(x, y, kwargs) or None (still inside the egg)."""
    if t < T_POP:
        return None
    if t < T_POP + 0.4:      # springs up out of the bottom shell
        p = back_out(seg(t, T_POP, T_POP + 0.4))
        return EGG_X, TOP - 20 - 60 * p + 60, dict(mood="shock", helmet=False, wings="flap", flap_t=t, sq=lerp(0.7, 1.0, min(1, p)))
    if t < T_HELM:
        return EGG_X, TOP - 20, dict(mood="shock", helmet=False, look=(0, -1))
    if t < 4.7:
        sq = lerp(0.8, 1.0, back_out(seg(t, T_HELM, T_HELM + 0.25)))
        mood = "blink" if 3.95 < t < 4.1 or 4.25 < t < 4.4 else ("chirp" if 4.45 <= t < 4.7 else "happy")
        return EGG_X, TOP - 20, dict(mood=mood, sq=sq)
    if t < 5.3:              # hops out of the bottom shell
        x, y = hop((EGG_X, TOP - 20), (830, TOP), seg(t, 4.7, 5.3), 120)
        return x, y, dict(mood="happy", wings="flap", flap_t=t)
    if t < T_DSTRIDE + 0.8:
        lk = (-1, 0.2) if t > 6.0 else (0, 0)
        return 830, TOP, dict(mood="happy", look=lk, face=-0.4 if t > 6.0 else 0)
    if t < T_SCRATCH:        # looks at Dill... then leans to peek past him
        lean = -0.28 * ease(seg(t, 10.2, 10.6))
        return 830, TOP, dict(mood="happy", look=(-1, -0.6), rot=lean, face=-0.6)
    if t < T_RUN:            # sees Crumb: love!
        return 830, TOP, dict(mood="love", rot=-0.28 * (1 - ease(seg(t, 12.5, T_RUN))), flap_t=t, face=-0.6,
                              wings="flap" if t > 11.4 else "down")
    if t < 13.8:             # runs to Crumb
        p = ease(seg(t, T_RUN, 13.8))
        return lerp(830, 640, p), TOP - abs(math.sin(p * math.pi * 4)) * 30, dict(mood="love", wings="flap", flap_t=t, face=-1)
    if t < 16.4:             # hugs his leg
        mood = "chirp" if 14.6 <= t < 14.9 else "love"
        return 640, TOP, dict(mood=mood, wings="hug", face=-0.8, flap_t=t, rot=-0.06 * math.sin(t * 6))
    # copycat
    if t < 17.0:
        p = ease(seg(t, 16.4, 17.0))
        return lerp(640, 560, p), TOP - abs(math.sin(p * math.pi * 2)) * 18, dict(mood="happy", face=-1, look=(-1, 0))
    if t < 17.8:
        return 560, TOP, dict(mood="happy", face=-0.5, look=(-1, -0.3))
    if t < 18.4:             # hops (higher than Crumb)
        x, y = hop((560, TOP), (560, TOP), seg(t, 17.8, 18.4), 170)
        return x, y, dict(mood="happy", wings="flap", flap_t=t, face=-0.5)
    if t < 19.2:
        return 560, TOP, dict(mood="happy", face=-0.5, look=(-1, -0.3))
    if t < 20.3:             # salutes
        return 560, TOP, dict(mood="proud", wings="salute", face=-0.3)
    if t < 22.6:
        return 560, TOP, dict(mood="happy", face=0.6, look=(1, -0.4), rot=0.12 * math.sin(t * 2) if t > 21.6 else 0)
    if t < 23.2:             # hops onto Dill's head
        x, y = hop((560, TOP), (700, TOP - 300), seg(t, 22.6, 23.2), 160)
        return x, y, dict(mood="happy", wings="flap", flap_t=t, face=0.5)
    if t < T_CROWN_OFF + 0.6:
        pk = 0.0
        for tp in (T_PECK1, T_PECK2):
            if tp - 0.08 <= t < tp + 0.12:
                pk = 0.35
        return 700, TOP - 300, dict(mood="happy", rot=pk, face=0.4, crowned=t >= T_CROWN_OFF + 0.55, look=(0, 1))
    if t < 24.9:
        return 700, TOP - 300, dict(mood="proud", crowned=True)
    if t < 25.4:             # hops down, crowned
        x, y = hop((700, TOP - 300), (570, TOP), seg(t, 24.9, 25.4), 110)
        return x, y, dict(mood="proud", crowned=True, wings="flap", flap_t=t)
    if t < T_LUNGE:          # poses like Dill: wing up, chest out
        return 570, TOP, dict(mood="proud", crowned=True, wings="salute", sq=1.06)
    if t < 26.5:             # darts away left
        p = ease(seg(t, T_LUNGE + 0.05, 26.5))
        return lerp(570, 320, p), TOP - abs(math.sin(p * math.pi * 3)) * 20, dict(mood="shock", crowned=True, wings="flap", flap_t=t, face=-1)
    if t < 27.4:
        return 320, TOP, dict(mood="happy", crowned=True, face=0.8, look=(1, 0))
    if t < 28.0:             # hops up onto the pile
        x, y = hop((320, TOP), (470, TOP - 290), seg(t, 27.4, 28.0), 120)
        return x, y, dict(mood="happy", crowned=True, wings="flap", flap_t=t)
    if t < T_UP:
        mood = "chirp" if 28.3 <= t < 28.7 else "proud"
        return 470, TOP - 290, dict(mood=mood, crowned=True, wings="salute" if t > 28.8 else "down", sq=1.04)
    if t < T_UP + 0.5:       # bounced off as they stand up
        x, y = hop((470, TOP - 290), (545, TOP), seg(t, T_UP, T_UP + 0.5), 90)
        return x, y, dict(mood="shock", crowned=True, wings="flap", flap_t=t)
    bx, by = bubble_pos(min(t, T_BPOP))
    if t < T_BPOP:           # watches the bubble come, cross-eyed at the end
        lk = (max(-1, min(1, (bx - 545) / 200)), max(-1, min(1, (by - (TOP - 100)) / 200)))
        return 545, TOP, dict(mood="happy", crowned=True, look=lk, face=0.3)
    if t < T_SNEEZE:
        return 545, TOP, dict(mood="blink", crowned=True, sq=0.95)
    if t < T_SNEEZE + 0.5:
        k = math.sin(math.pi * seg(t, T_SNEEZE, T_SNEEZE + 0.5))
        return 545, TOP, dict(mood="sneeze", crowned=False, rot=-0.25 * k, sq=1 - 0.1 * k)
    if t < T_RUMBLE:
        return 545, TOP, dict(mood="happy", look=(1, -0.5), face=0.2)
    if t < 34.6:             # tummy rumble
        return 545, TOP, dict(mood="shock", look=(0, 1), shake=6, sq=1 + 0.04 * math.sin(t * 40))
    if t < T_CLOSE:          # turns to Dill
        return 545, TOP, dict(mood="happy", look=(1, -0.6), face=0.8)
    return 545, TOP, dict(mood="hungry", look=(1, -0.5), face=0.9, flap_t=t,
                          sq=1 + 0.03 * math.sin(t * 6), rot=0.05 * math.sin(t * 3))


def dill_state(t):
    """(x, y, kwargs, has_crown) or None."""
    if t < 5.8:
        return None
    if t < 7.0:      # hauls himself up over the shelf's front edge
        p = ease_out(seg(t, 5.8, 7.0))
        return 430, lerp(TOP + 360, TOP + 70, p) + 8 * math.sin(t * 25), dict(mood="angry", look=(0, -1), arm="reach"), True
    if t < 7.4:
        x, y = hop((430, TOP + 70), (430, TOP), seg(t, 7.0, 7.4), 140)
        return x, y, dict(mood="shocked", look=(0, -1), arm="reach"), True
    if t < T_DSTRIDE:
        return 430, TOP - abs(math.sin((t - 7.4) * 7)) * 6, dict(mood="frozen" if t < 8.3 else "smug", look=(1, 0)), True
    if t < 9.8:      # strides up to the chick
        p = ease(seg(t, T_DSTRIDE, 9.8))
        return lerp(430, 660, p), TOP - abs(math.sin(p * math.pi * 3)) * 22, dict(mood="smug", look=(1, 0)), True
    if t < T_SCRATCH:   # poses
        return 660, TOP, dict(mood="proud", look=(1, 0), arm="up", sq=1.03), True
    if t < 13.4:
        return 660, TOP, dict(mood="frozen", look=(1, 0), arm="up"), True
    if t < 14.0:     # steps aside, stunned
        p = ease(seg(t, 13.4, 14.0))
        return lerp(660, 840, p), TOP - 30 * math.sin(math.pi * p), dict(mood="shocked", look=(-1, 0)), True
    if t < 21.0:     # sulks, arms down
        mood = "angry" if t > 19.0 else "smug" if t < 15.0 else "frozen"
        return 840, TOP, dict(mood=mood, look=(-1, 0.2), shake=2 if t > 19.5 else 0), True
    if t < 21.6:     # marches back in
        p = ease(seg(t, 21.0, 21.6))
        return lerp(840, 700, p), TOP - abs(math.sin(p * math.pi * 2)) * 20, dict(mood="proud", look=(-1, 0)), True
    if t < 22.9:     # heroic pose for Peep to copy
        return 700, TOP, dict(mood="proud", look=(-1, 0), arm="up", sq=1.04), True
    if t < T_CROWN_OFF:
        k = 0.92 if any(tp <= t < tp + 0.12 for tp in (T_PECK1, T_PECK2)) else 1.0
        return 700, TOP, dict(mood="shocked", look=(0, -1), arm="up", sq=k), True
    if t < T_LUNGE:  # crownless and furious
        return 700, TOP, dict(mood="angry" if t > 24.4 else "shocked", look=(-1, -1) if t < 24.9 else (-1, 0.3),
                              shake=4 if t > 25.0 else 0), False
    if t < T_BONK:   # lunges for the chick
        p = ease(seg(t, T_LUNGE, T_BONK))
        return lerp(700, 540, p), TOP - 80 * math.sin(math.pi * p), dict(mood="angry", look=(-1, 0), arm="reach", rot=-0.6 * p), False
    if t < 27.1:     # topples onto Crumb
        p = ease(seg(t, T_BONK, 27.1))
        return lerp(540, 640, p), lerp(TOP, TOP - 218, p), dict(mood="shocked", look=(-1, 0), rot=lerp(-0.6, -math.pi / 2, p)), False
    if t < T_UP:
        return 640, TOP - 218, dict(mood="frozen", look=(0, -1) if t > 28.0 else (1, 1), rot=-math.pi / 2), False
    if t < T_UP + 0.45:   # springs up
        p = ease(seg(t, T_UP, T_UP + 0.45))
        x, y = hop((640, TOP - 218), (690, TOP), p, 120)
        return x, y, dict(mood="angry", rot=lerp(-math.pi / 2, 0, p)), False
    has = t >= T_CROWN_BACK
    if t < T_BPOP:
        bx, by = bubble_pos(t)
        lk = (max(-1, min(1, (bx - 690) / 200)), max(-1, min(1, (by - (TOP - 210)) / 200)))
        return 690, TOP, dict(mood="frozen", look=lk), False
    if t < T_CROWN_BACK:
        return 690, TOP, dict(mood="shocked", look=(-1, -1)), False
    if t < T_RUMBLE:
        return 690, TOP - abs(math.sin((t - T_CROWN_BACK) * 8)) * 12, dict(mood="proud", look=(-1, 0)), True
    if t < T_CLOSE:
        return 690, TOP, dict(mood="frozen", look=(-1, 0.4)), True
    return 690, TOP, dict(mood="shocked", look=(-1, 0.3), shake=3), has


def crumb_state(t):
    """(x, y, kwargs) or None."""
    if t < 6.6:
        return None
    if t < 7.8:      # climbs up
        p = ease_out(seg(t, 6.6, 7.8))
        return 560, lerp(TOP + 340, TOP + 80, p) + 6 * math.sin(t * 30), dict(mood="scared", look=(0, -1), arm="wave")
    if t < 8.2:
        x, y = hop((560, TOP + 80), (560, TOP), seg(t, 7.8, 8.2), 120)
        return x, y, dict(mood="scared", look=(0, -1), arm="wave")
    if t < 11.4:     # panting
        return 560, TOP + 6 * math.sin(t * 9), dict(mood="worried", look=(1, 0) if t > 9.5 else (0, 0.3))
    if t < 13.8:     # notices he's being stared at
        return 560, TOP, dict(mood="scared" if t > 12.0 else "worried", look=(1, 0))
    if t < 16.0:     # chick on his leg: me??
        return 560, TOP, dict(mood="sheepish" if t > 14.5 else "scared", look=(1, 1))
    if t < 16.6:     # steps left
        p = ease(seg(t, 16.0, 16.6))
        return lerp(560, 430, p), TOP - abs(math.sin(p * math.pi * 2)) * 16, dict(mood="worried", look=(1, 0.6))
    if t < 17.4:
        return 430, TOP, dict(mood="worried", look=(1, 0.8))
    if t < 17.9:     # hops
        x, y = hop((430, TOP), (430, TOP), seg(t, 17.4, 17.9), 90)
        return x, y, dict(mood="scared", look=(1, 0.8))
    if t < 18.8:
        return 430, TOP, dict(mood="sheepish", look=(1, 0.8))
    if t < 19.8:     # salutes
        return 430, TOP, dict(mood="worried", look=(1, 0.5), arm="wave")
    if t < 26.2:
        mood = "sheepish"
        if 23.8 <= t < 25.0:
            mood = "scared"
        return 430, TOP - (abs(math.sin(t * 10)) * 8 if 20.0 <= t < 21.0 or 25.3 <= t < 26.0 else 0), dict(mood=mood, look=(1, 0.2) if t < 21.0 else (1, -0.6))
    if t < T_BONK:
        return 430, TOP, dict(mood="scared", look=(1, 0))
    if t < 27.0:     # knocked flat
        p = ease(seg(t, T_BONK, 27.0))
        return lerp(430, 600, p), lerp(TOP, TOP - 72, p), dict(mood="scared", look=(1, 0), rot=lerp(0, -math.pi / 2, p))
    if t < T_UP:
        return 600, TOP - 72, dict(mood="dizzy", rot=-math.pi / 2)
    if t < T_UP + 0.45:
        p = ease(seg(t, T_UP, T_UP + 0.45))
        x, y = hop((600, TOP - 72), (410, TOP), p, 100)
        return x, y, dict(mood="dizzy" if p < 0.5 else "worried", rot=lerp(-math.pi / 2, 0, p))
    if t < T_BPOP:
        bx, by = bubble_pos(t)
        lk = (max(-1, min(1, (bx - 410) / 200)), max(-1, min(1, (by - (TOP - 160)) / 200)))
        return 410, TOP, dict(mood="worried", look=lk)
    if t < T_CLOSE:
        return 410, TOP, dict(mood="sheepish" if t < T_RUMBLE else "scared", look=(1, 0))
    return 410, TOP, dict(mood="scared", look=(1, 0), shake=2)


def crown_flight(t):
    """Crown position while airborne: (x, y, rot) or None."""
    if T_CROWN_OFF <= t < T_CROWN_OFF + 0.55:   # popped off Dill, flips up, lands on Peep
        p = seg(t, T_CROWN_OFF, T_CROWN_OFF + 0.55)
        return lerp(704, 694, p), lerp(TOP - 280, TOP - 300 - 192, p) - 220 * math.sin(math.pi * p), p * 2 * math.pi
    if T_SNEEZE <= t < T_CROWN_BACK:             # sneezed back onto Dill
        p = seg(t, T_SNEEZE, T_CROWN_BACK)
        return lerp(540, 694, p), lerp(TOP - 192, TOP - 280, p) - 260 * math.sin(math.pi * p), -p * 2 * math.pi + 0.08
    return None


# ---------------- camera ----------------
def camera(t):
    if t < T_POP:            # tight on the egg
        sh = 0.0
        for tp in (T_C1, T_C2):
            if tp <= t < tp + 0.2:
                sh = 10 * (1 - seg(t, tp, tp + 0.2))
        return EGG_X + random.uniform(-sh, sh), TOP - 130 + random.uniform(-sh, sh), 3.0
    if t < 5.6:
        k = ease(seg(t, T_POP, T_POP + 0.5))
        return EGG_X - 10 * k, TOP - 130 - 30 * k, lerp(3.0, 2.6, k)
    if t < T_CLOSE:
        k = ease(seg(t, 5.6, 6.5))
        cx, cy, z = lerp(EGG_X - 10, 640, k), lerp(TOP - 160, TOP - 300, k), lerp(2.6, 1.78, k)
        if 21.0 <= t < 26.0:   # rise a bit to keep Peep on Dill's head in frame
            k2 = ease(seg(t, 21.0, 22.6)) * (1 - ease(seg(t, 25.2, 26.0)))
            cy -= 70 * k2
        if T_BUB0 <= t < T_BPOP + 0.5:
            k3 = ease(seg(t, T_BUB0, T_BUB0 + 0.8)) * (1 - ease(seg(t, T_BPOP, T_BPOP + 0.5)))
            cy -= 60 * k3
        if T_BONK <= t < T_BONK + 0.25:
            s = 12 * (1 - seg(t, T_BONK, T_BONK + 0.25))
            cx += random.uniform(-s, s); cy += random.uniform(-s, s)
        if 26.3 <= t < T_UP + 0.8:
            k4 = ease(seg(t, 26.3, 27.0)) * (1 - ease(seg(t, T_UP, T_UP + 0.8)))
            cx -= 80 * k4
        if T_RUMBLE <= t < 34.6:
            cx += random.uniform(-4, 4)
        return cx, cy, z
    # close-up: Peep and Dill
    z = 2.7
    for tp in DUNS:
        if t >= tp:
            z += 0.18 * ease_out(seg(t, tp, tp + 0.1))
    return 612, TOP - 175, z


# ---------------- scene ----------------
def scene(c, t):
    random.seed(int(t * 30))
    cx, cy, Z = camera(t)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    fridge6(c, DIM, 0, lid=False)
    lid_piece(c, 760, TOP - 25, 0.0)

    # ---- the egg ----
    if t < T_POP:
        rot = 0.1 * math.sin(t * 16) * (0.6 + 0.4 * seg(t, 0, T_POP))
        crack = 0.5 if t < T_C2 else 1.0
        if t < T_C1:
            crack = 0.0
        eggs_rot = rot
        from ep7 import cracking_egg
        cracking_egg(c, EGG_X, TOP, eggs_rot, crack, gap=0.6 if t >= T_C2 else 0.0, eyes=1.0 if t >= T_C2 + 0.2 else 0.0)
    else:
        # bottom shell stays on the shelf
        ps = peep_state(t)
        inside = t < 5.0
        if inside and ps:
            x, y, kw = ps; peep(c, x, y, **kw)
        shell_half(c, EGG_X, TOP - 70, 0.0, top=False)
        # top shell flies up, flips, lands on Peep's head
        if t < T_HELM:
            p = seg(t, T_POP, T_HELM)
            sx = lerp(EGG_X, EGG_X, p) + 40 * math.sin(math.pi * p)
            sy = lerp(TOP - 70, TOP - 20 - 118 * 1.0, p) - 330 * math.sin(math.pi * p)
            shell_half(c, sx, sy, -0.22 + 3 * math.pi * 2 * p * 0.5 * 0 + p * 2 * math.pi * 1.0, True, lerp(1.0, 1.18, p))
        if not inside and ps:
            pass

    ds = dill_state(t)
    cs = crumb_state(t)
    ps = peep_state(t) if t >= 5.0 else None

    def draw_dill():
        if ds:
            x, y, kw, has = ds
            dill(c, x, y, crown_on=has, **kw)

    def draw_crumb():
        if cs:
            x, y, kw = cs
            crumb_notched(c, x, y, True, **kw)

    def draw_peep():
        if ps:
            x, y, kw = ps
            peep(c, x, y, **kw)

    # Peep sits on top of the pile / Dill's head: draw last. Otherwise Peep hugs in front of Crumb.
    draw_crumb(); draw_dill(); draw_peep()

    cf = crown_flight(t)
    if cf:
        crown(c, cf[0], cf[1], 1.0, cf[2])

    # ---- the soap bubble ----
    if T_BUB0 <= t < T_BPOP:
        bx, by = bubble_pos(t)
        soap_bubble(c, bx, by, 120 + 6 * math.sin(t * 4), t, min(1, seg(t, T_BUB0, T_BUB0 + 0.3)))
    pop_burst(c, 548, TOP - 236, t, T_BPOP)

    # ---- effects ----
    def word(s, x, y, size, col, t0, t1, rot=0.0):
        if t0 <= t < t1:
            k = back_out(seg(t, t0, t0 + 0.2))
            c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(k), S(k)); text(c, s, 0, 0, size, col, olw=10); c.restore()
    word("CRACK!", EGG_X - 70, TOP - 240, 40, (1, 1, 1), T_C1, T_C1 + 0.6, -0.15)
    word("CRACK!", EGG_X + 70, TOP - 250, 44, (1, 1, 1), T_C2, T_C2 + 0.6, 0.15)
    word("POP!", EGG_X, TOP - 290, 70, GOLD, T_POP, T_POP + 0.7, -0.05)
    if T_POP <= t < T_POP + 0.5:   # shell crumbs
        q = seg(t, T_POP, T_POP + 0.5)
        for i in range(8):
            a = -math.pi * (0.1 + 0.8 * i / 7)
            ellipse(c, EGG_X + math.cos(a) * 150 * q, TOP - 80 + math.sin(a) * 150 * q + 120 * q * q, 7, 5, WHITE, lw=3)
    word("clink", EGG_X + 90, TOP - 250, 34, (1, 1, 1), T_HELM, T_HELM + 0.5, 0.15)
    word("peep!", EGG_X - 150, TOP - 300, 40, hexc("#FFE680"), 4.45, 5.1, -0.1)
    word("huff", 330, TOP - 360, 34, (1, 1, 1), 7.5, 8.2, -0.1)
    word("huff", 620, TOP - 330, 30, (1, 1, 1), 8.4, 9.0, 0.1)
    if T_SCRATCH <= t < T_RUN:     # hearts float up from Peep
        for j in range(4):
            q = ((t - T_SCRATCH - 0.3) * 0.9 + j / 4) % 1
            if t > T_SCRATCH + 0.3:
                heart(c, 800 + 50 * math.sin(j * 2 + q * 4), TOP - 200 - q * 220, 1.6, 1 - q)
    if 13.8 <= t < 16.2:
        for j in range(3):
            q = ((t - 13.8) * 0.8 + j / 3) % 1
            heart(c, 640 + 40 * math.sin(j * 3 + q * 5), TOP - 190 - q * 200, 1.3, 1 - q)
    if 14.2 <= t < 15.6:            # Crumb: me??
        s = back_out(seg(t, 14.2, 14.4))
        c.save(); c.translate(560, TOP - 360); c.scale(S(s), S(s)); text(c, "?", 0, 0, 90, hexc("#FFE680"), olw=10); c.restore()
    word("peep!", 700, TOP - 260, 34, hexc("#FFE680"), 14.6, 15.2, 0.1)
    if 19.3 <= t < 19.9:
        star(c, 620, TOP - 160, 22 * math.sin(math.pi * seg(t, 19.3, 19.9)), t * 6, (1, 1, 1))
    if 18.8 <= t < 19.4:
        star(c, 520, TOP - 230, 22 * math.sin(math.pi * seg(t, 18.8, 19.4)), t * 6, (1, 1, 1))
    word("PECK!", 820, TOP - 440, 44, (1, 1, 1), T_PECK1, T_PECK1 + 0.35, 0.12)
    word("PECK!", 590, TOP - 460, 48, (1, 1, 1), T_PECK2, T_PECK2 + 0.4, -0.12)
    if 25.0 <= t < T_LUNGE:          # steam from Dill
        for j in range(3):
            q = ((t - 25.0) * 1.6 + j / 3) % 1
            ellipse(c, 700 + (j - 1) * 40, TOP - 330 - q * 120, 18 + 14 * q, 14 + 10 * q, (0.95, 0.95, 1), stroke=False)
    word("BONK!", 520, TOP - 420, 70, (1, 0.35, 0.35), T_BONK, T_BONK + 0.7, -0.1)
    if 27.1 <= t < T_UP:             # dizzy stars over the pile
        for j in range(3):
            a = t * 4 + j * 2.1
            star(c, 600 + 120 * math.cos(a), TOP - 400 + 30 * math.sin(a), 16, t * 3, GOLD)
    word("peep!", 560, TOP - 520, 36, hexc("#FFE680"), 28.3, 28.9, 0.1)
    word("pop", 600, TOP - 380, 44, (1, 1, 1), T_BPOP, T_BPOP + 0.5, 0.1)
    word("A-CHOO!", 430, TOP - 300, 46, hexc("#FFE680"), T_SNEEZE, T_SNEEZE + 0.7, -0.12)
    if T_CROWN_BACK <= t < T_CROWN_BACK + 0.5:
        star(c, 760, TOP - 330, 26 * math.sin(math.pi * seg(t, T_CROWN_BACK, T_CROWN_BACK + 0.5)), t * 5, (1, 1, 1))
    if T_RUMBLE <= t < 34.9:
        k = back_out(seg(t, T_RUMBLE, T_RUMBLE + 0.2))
        c.save(); c.translate(545 + random.uniform(-4, 4), TOP - 280); c.rotate(-0.05); c.scale(S(k), S(k))
        text(c, "RUMBLE", 0, 0, 48, hexc("#FFA94D"), olw=10); c.restore()
    if t >= 35.7:                      # gulp
        word("gulp", 735, TOP - 80, 30, (1, 1, 1), 35.7, END_T, 0.1)
    dark_overlay(c, DIM)


def frame(c, t):
    if t >= END_T:
        end_card(c, t, END_T); return
    c.save(); scene(c, t); c.restore()
    if t < 0.12:   # hook flash
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.5 * (1 - seg(t, 0, 0.12))); c.fill()
    if T_POP <= t < T_POP + 0.15:
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.5 * (1 - seg(t, T_POP, T_POP + 0.15))); c.fill()
    if T_CLOSE <= t < T_CLOSE + 0.12:   # hard cut flash into the close-up
        c.rectangle(0, 0, W, H); c.set_source_rgba(0, 0, 0, 0.6 * (1 - seg(t, T_CLOSE, T_CLOSE + 0.12))); c.fill()
    if T_CLOSE <= t < END_T:   # DUN DUN DUNNN
        for i, tp in enumerate(DUNS):
            if tp <= t:
                sc = back_out(seg(t, tp, tp + 0.15))
                c.save(); c.translate([250, 830, 540][i], [330, 330, 1700][i]); c.rotate([-0.12, 0.12, 0.0][i]); c.scale(S(sc), S(sc))
                text(c, "DUNNN!" if i == 2 else "DUN", 0, 0, [110, 110, 150][i], (1, 0.3, 0.3), olw=14); c.restore()
    if t >= END_T - 0.4:
        iris(c, W / 2, H * 0.5, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))
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
