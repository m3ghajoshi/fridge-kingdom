"""FRIDGE KINGDOM — Episode 7: "The Truth About the Duck". 40s, 1080x1920 @ 30fps.

Variant A (title card first).

In the crisper drawer, Wilt flings Dill back up to the shelf with its floppy top. Behind the jello Dill
acts out the doodle for Crumb (the Hand + the Duck + hearts) and hatches a plan: squeak the Duck when
the door opens. Crumb gulps, salutes, and tiptoes past the bowing pickles, freezing whenever one looks.
Dill gives a thumbs-up from the door seal; the door opens; Crumb jumps on the Duck: SQUEEEAK! The Hand
gently scoops the Duck up (hearts) and carries it off; far away, a bathtub steams with a little duck
silhouette bobbing. The Hand returns Dill's (half-eaten) butter-dish throne. Door closes. Dill leaps onto
his throne, sword raised; the pickles and Grandma bow; confetti; Crumb cries happy tears. In the dark the
camera drifts up to the top shelf: a single egg wobbles... CRACK. Two tiny eyes peek out.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, duck, crown, bubble, dark_overlay, ellipse, rrect, star, text, hand,
                 iris, hexc, seg, ease, ease_out, lerp, back_out, INK, GOLD, FLOOR, TOP, W, H, FPS, S)
from ep2 import end_card, jello
from ep4 import WHITE
from ep5 import cap_crown, crumb_notched, DUCK_X, JELLO_X
from ep6 import (pickle_kid, grandma, wilt, fridge6, drawer_inside_bg, lid_piece, LINE_X, G_LINE_X, FRONT, TEAR)
from animate import heart

DUR = 40.3
END_T = 38.8
DIM = 0.18
SEAL_X = 1110          # Dill's hiding spot at the door seal
EGG_X = 900
CRUMB_SIT = 245
HUD_X = JELLO_X - 110     # Dill's spot in the jello huddle

# ---------------- timing ----------------
T_FLING = 3.2          # Wilt flings Dill up
T_LAND = 4.3           # Dill lands behind the jello
T_OPEN = 18.6          # door opens
T_JUMP = 19.35         # Crumb leaps onto the Duck
T_SQUEAK = 19.85
T_GRIP = 22.6
T_LIFT = 23.0
T_DISH = 29.0          # butter dish set down
T_CLOSE = 30.3
T_LEAP = 30.8          # Dill leaps onto his throne
T_SWORD = 31.75
T_CRACK = 36.8


def light_at(t):
    if t < T_OPEN:
        return DIM
    if t < T_CLOSE:
        return lerp(DIM, 1.0, ease(seg(t, T_OPEN, T_OPEN + 0.4)))
    return lerp(1.0, DIM, ease(seg(t, T_CLOSE, T_CLOSE + 0.35)))


# ---------------- new props ----------------
def god_rays(c, light):
    if light <= DIM + 0.01:
        return
    k = (light - DIM) / (1 - DIM)
    for i in range(5):
        a = -0.5 + i * 0.22
        c.move_to(-100, -200)
        c.line_to(-100 + 2600 * math.cos(a + 0.6), -200 + 2600 * math.sin(a + 0.6))
        c.line_to(-100 + 2600 * math.cos(a + 0.68), -200 + 2600 * math.sin(a + 0.68))
        c.close_path(); c.set_source_rgba(1, 1, 1, 0.13 * k); c.fill()


def door_seal(c, x):
    """The rubbery door gasket: a thick grey ribbed strip down the right edge of the fridge."""
    rrect(c, x, -400, 260, 2600, 40); c.set_source_rgb(*hexc("#6C7A89")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.18); c.set_line_width(10)
    for dx in (28, 70, 112):
        c.move_to(x + dx, -380); c.line_to(x + dx, 2180); c.stroke()
    c.set_source_rgba(0, 0, 0, 0.25); c.set_line_width(6)
    for dx in (48, 90):
        c.move_to(x + dx, -380); c.line_to(x + dx, 2180); c.stroke()


def butter_dish_bitten(c, x, y, s=1.0):
    """Dill's butter-dish throne, back from The Outside with a big bite out of the butter."""
    c.save(); c.translate(x, y); c.scale(S(s), S(s))
    ellipse(c, 0, -10, 150, 26, (0.97, 0.97, 1), lw=6)
    bites = [(70, -112, 34), (32, -118, 26), (96, -76, 22)]
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
    c.restore()


def the_duck(c, x, y, sx=1.0, sy=1.0, cap_rot=0.38):
    c.save(); c.translate(x, y); c.scale(S(sx), S(sy)); c.translate(-x, -y)
    duck(c, x, y, turn=1.0)
    cap_crown(c, x + 6, y - 186, cap_rot)
    c.restore()


def cracking_egg(c, x, y, rot=0.0, crack=0.0, gap=0.0, eyes=0.0):
    """Egg (bottom at x, y). crack 0..1 draws the zig-zag; gap opens it to a dark slit; eyes peek through."""
    c.save(); c.translate(x, y); c.rotate(rot)
    ellipse(c, 0, -70, 56, 70, WHITE, lw=6)
    ellipse(c, -20, -98, 10, 18, (1, 1, 1), stroke=False)
    pts = [(-52, -64), (-38, -50), (-26, -72), (-12, -52), (2, -74), (16, -54), (30, -74), (42, -52), (54, -66)]
    n = max(1, int(round(len(pts) * min(1, crack))))
    if crack > 0:
        if gap > 0:
            c.move_to(*pts[0])
            for px, py in pts[1:]:
                c.line_to(px, py - 20 * gap)
            for px, py in reversed(pts):
                c.line_to(px, py + 18 * gap)
            c.close_path(); c.set_source_rgb(*hexc("#1A1424")); c.fill()
            if eyes > 0:
                for ex in (-14, 14):
                    ellipse(c, ex, -64, 10 * S(eyes), 9 * S(eyes), (1, 1, 1), stroke=False)
                    ellipse(c, ex + 2, -63, 5 * S(eyes), 5 * S(eyes), INK, stroke=False)
        c.set_source_rgb(*INK); c.set_line_width(4.5); c.set_line_join(cairo.LINE_JOIN_MITER)
        c.move_to(*pts[0])
        for px, py in pts[1:n]:
            c.line_to(px, py)
        c.stroke()
    c.restore()


def thumbs_up(c, x, y, s=1.0):
    """A little green fist with the thumb up (drawn at the end of Dill's pointing arm)."""
    c.save(); c.translate(x, y); c.scale(S(s), S(s))
    rrect(c, -8, -46, 18, 40, 9); c.set_source_rgb(*hexc("#7BC043")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    ellipse(c, 0, 0, 22, 18, hexc("#7BC043"), lw=4)
    c.set_source_rgb(*INK); c.set_line_width(3)
    for fy in (-6, 2, 10):
        c.move_to(-18, fy); c.line_to(-4, fy); c.stroke()
    c.restore()


CONF_COLS = [hexc("#FF4D6D"), hexc("#4DABF7"), hexc("#69DB7C"), hexc("#FFC933"), hexc("#B197FC")]


def confetti(c, t, t0, cx, cy, n=60, seed=7):
    if t < t0:
        return
    rnd = random.Random(seed)
    for i in range(n):
        a = rnd.uniform(-math.pi * 0.95, -math.pi * 0.05)
        v = rnd.uniform(500, 1100)
        dt = t - t0 - rnd.uniform(0, 0.25)
        if dt < 0:
            continue
        x = cx + math.cos(a) * v * dt * 0.8 + 30 * math.sin(dt * 5 + i)
        y = cy + math.sin(a) * v * dt + 520 * dt * dt
        y = min(y, FLOOR + 20 - (i % 5) * 3)
        c.save(); c.translate(x, y); c.rotate(dt * rnd.uniform(4, 9) + i)
        c.scale(1, S(abs(math.cos(dt * 8 + i)) * 0.9 + 0.1))
        c.rectangle(-9, -5, 18, 10); c.set_source_rgb(*CONF_COLS[i % 5]); c.fill()
        c.restore()


def sq_rings(c, x, y, t, t0, dur=1.0, col=(1, 1, 1)):
    if not (t0 <= t < t0 + dur):
        return
    for j in range(3):
        q = seg(t, t0 + j * 0.15, t0 + j * 0.15 + 0.6)
        if 0 < q < 1:
            c.save(); c.translate(x, y); c.scale(lerp(80, 420, q), lerp(60, 300, q))
            c.arc(0, 0, 1, 0, 2 * math.pi); c.restore()
            c.set_source_rgba(*col, 0.8 * (1 - q)); c.set_line_width(10); c.stroke()


# ---------------- title card (two-line name) ----------------
def title_card(c, t):
    from ep1 import crumb
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
        text(c, "Episode 7:", 0, 0, 60, (1, 1, 1), olw=10)
        text(c, "The Truth About the Duck", 0, 90, 70, GOLD, olw=12)
        c.restore()
    dill(c, 300, 1680 - abs(math.sin(t * 5)) * 30, "angry", crown_on=True, arm="up", shake=3)
    crumb(c, 560, 1680, "worried", look=(1, 0), shake=3)
    the_duck(c, 860, 1680)
    # a single "?" over the Duck
    s = back_out(seg(t, 1.1, 1.35))
    c.save(); c.translate(860, 1400); c.scale(S(s), S(s)); text(c, "?", 0, 0, 120, hexc("#FF8FB3"), olw=12); c.restore()


# ---------------- character states ----------------
def crumb_state(t):
    """(x, y, kwargs) for Crumb on the bottom shelf."""
    PEEK = (JELLO_X + 75, FLOOR - 185)
    if t < T_LAND:
        return PEEK[0], PEEK[1] - 4 * math.sin(t * 30), dict(mood="worried", look=(-1, 0))
    if t < T_LAND + 0.5:   # startled jump when Dill lands
        p = seg(t, T_LAND, T_LAND + 0.5)
        return PEEK[0], PEEK[1] - 120 * math.sin(math.pi * p), dict(mood="scared", look=(-1, 0), shake=3)
    if t < 8.2:
        return PEEK[0], PEEK[1], dict(mood="worried", look=(-1, -0.3))
    if t < 9.6:            # "!" he gets it
        return PEEK[0], PEEK[1] - 10 * math.sin(min(1, seg(t, 8.2, 8.5)) * math.pi), dict(mood="sheepish", look=(-1, -0.5))
    if t < 10.5:           # ...but HE has to do it? gulp
        sq = 1 - 0.06 * math.sin(math.pi * seg(t, 9.9, 10.3))
        return PEEK[0], PEEK[1] + 8 * (1 - sq) * 10, dict(mood="scared", look=(0, 0), shake=2)
    if t < 11.6:           # salute
        return PEEK[0], PEEK[1], dict(mood="worried", look=(0, 0), arm="wave")
    if t < 12.0:           # slips out from behind the jello
        p = ease(seg(t, 11.6, 12.0))
        return lerp(PEEK[0], 1030, p), lerp(PEEK[1], FLOOR, p) - 60 * math.sin(math.pi * p), dict(mood="worried", look=(-1, 0))
    # tiptoe along the back of the shelf, freezing whenever someone looks
    path = [(12.0, 1030), (13.0, 905), (13.7, 905), (15.0, 700), (15.7, 700), (16.8, 565), (T_JUMP, 565)]
    if t < T_JUMP:
        for (ta, xa), (tb, xb) in zip(path, path[1:]):
            if t < tb:
                p = seg(t, ta, tb)
                moving = xa != xb
                x = lerp(xa, xb, p)
                if moving:
                    ph = (t - ta) * 3.2
                    lift = abs(math.sin(ph * math.pi)) * 26
                    return x, FLOOR - lift, dict(mood="worried", look=(-1, 0), rot=0.08 * math.sin(ph * math.pi))
                # frozen mid-tiptoe
                return x, FLOOR - 20, dict(mood="scared", look=(1, 0.3), rot=0.1)
        if t < T_OPEN:
            return 565, FLOOR, dict(mood="worried", look=(-1, 0.2))
        return 565, FLOOR, dict(mood="scared", look=(-1, -1), shake=2)
    if t < T_SQUEAK:       # leap onto the Duck
        p = seg(t, T_JUMP, T_SQUEAK)
        x = lerp(565, DUCK_X + 10, p)
        y = lerp(FLOOR, FLOOR - 96, p) - 260 * math.sin(math.pi * p)
        return x, y, dict(mood="scared", look=(-1, 1), rot=-0.3 * math.sin(math.pi * p))
    if t < 20.7:           # standing on the squashed Duck
        return DUCK_X + 10, FLOOR - 96 + 18 * math.sin(math.pi * seg(t, T_SQUEAK, T_SQUEAK + 0.25)), dict(mood="scared", look=(0, -1), shake=3)
    if t < 21.2:           # tumbles off backwards
        p = seg(t, 20.7, 21.2)
        x = lerp(DUCK_X + 10, CRUMB_SIT, p)
        y = lerp(FLOOR - 96, FRONT + 30, p * p) - 160 * math.sin(math.pi * p)
        return x, y, dict(mood="scared", look=(1, -1), rot=-0.5 * p)
    if t < T_LEAP:         # sitting, stunned, watching
        return CRUMB_SIT, FRONT + 30, dict(mood="scared" if t < 26.0 else "worried", look=(1, -1), rot=-0.5 * (1 - ease(seg(t, 24.2, 24.6))))
    if t < 32.0:
        return CRUMB_SIT, FRONT + 30, dict(mood="worried", look=(1, -0.6))
    return CRUMB_SIT, FRONT + 30 - abs(math.sin((t - 32.0) * 6)) * 8 * (1 - seg(t, 34.4, 35.0)), dict(mood="sheepish", look=(1, -0.6))


def dill_state(t):
    """Dill on the bottom shelf / door seal: (x, y, kwargs) or None."""
    if t < 3.6:
        return None   # (in the drawer)
    if t < T_LAND:   # flies up out of the drawer and lands behind the jello
        p = seg(t, 3.6, T_LAND)
        x = lerp(760, HUD_X, p)
        y = lerp(FLOOR + 420, FLOOR - 125, p) - 520 * math.sin(math.pi * p)
        return x, y, dict(mood="shocked", look=(0, -1), arm="reach", rot=-p * 2 * math.pi)
    if t < 4.9:
        return HUD_X, FLOOR - 125, dict(mood="frozen", look=(1, 0), sq=lerp(0.8, 1.0, seg(t, T_LAND, T_LAND + 0.2)))
    if t < 8.4:      # acts out the doodle: big arms, cradling, swooning
        beat = int((t - 4.9) / 0.6)
        arm = ["reach", "down", "reach", "point_l", "reach", "down"][beat % 6]
        mood = ["proud", "smug", "proud", "angry", "proud", "smug"][beat % 6]
        return HUD_X, FLOOR - 125 - abs(math.sin((t - 4.9) * 5)) * 10, dict(mood=mood, look=(1, -0.3), arm=arm,
                                                                                  rot=0.08 * math.sin((t - 4.9) * 4))
    if t < 11.7:     # the plan
        arm = "point_l" if t < 9.8 else "pound"
        return HUD_X, FLOOR - 125, dict(mood="smug" if t < 9.8 else "proud", look=(1, 0) if t < 9.8 else (1, -0.3), arm=arm)
    if t < 12.0:     # sneaks off to the right (to the door seal)
        p = seg(t, 11.7, 12.0)
        return lerp(HUD_X, 1180, p), FLOOR - 125 - 80 * math.sin(math.pi * p), dict(mood="smug", look=(1, 0))
    if t < 17.0:
        return None
    if t < T_LEAP:   # at the door seal
        if t < 17.25:
            return SEAL_X, FLOOR, dict(mood="smug", look=(-1, 0), arm="down")
        if t < T_OPEN:
            return SEAL_X, FLOOR, dict(mood="proud", look=(-1, 0), arm="point_l", thumb=True)
        return SEAL_X, FLOOR, dict(mood="shocked", look=(-1, -1), arm="down")
    if t < T_LEAP + 0.9:   # leaps over everyone onto the butter dish
        p = seg(t, T_LEAP, T_LEAP + 0.9)
        x = lerp(SEAL_X, DUCK_X, ease(p))
        y = lerp(FLOOR, FLOOR - 110, p) - 620 * math.sin(math.pi * p)
        return x, y, dict(mood="proud", look=(-1, -1), arm="reach", rot=-0.25 * math.sin(math.pi * p))
    if t < T_SWORD:
        return DUCK_X, FLOOR - 110, dict(mood="proud", look=(0, 0), arm="down", sq=lerp(0.85, 1.0, seg(t, T_LEAP + 0.9, T_LEAP + 1.05)))
    return DUCK_X, FLOOR - 110 - abs(math.sin((t - T_SWORD) * 4)) * 10 * (1 - seg(t, 34.4, 35.0)), \
        dict(mood="proud", look=(0, 0), arm="up", rot=0.04 * math.sin(t * 4))


def pickle_pose(k, t):
    """The five pickles bowing to the Duck's spot (left)."""
    x = LINE_X[k]
    bow = -0.6
    kw = dict(look=(-1, 0.6), mood="closed", arms="down")
    if k == 2 and 15.0 <= t < 15.75:       # the bowtie pickle peeks at Crumb
        b = 1 - ease(seg(t, 15.0, 15.2)) * (1 - ease(seg(t, 15.5, 15.75)))
        bow = -0.6 * b
        kw = dict(look=(1, -0.6), mood="calm", arms="down")
    if T_OPEN <= t < 23.2:                  # the door! straighten up and look
        bow = -0.6 * (1 - ease(seg(t, T_OPEN, T_OPEN + 0.3)))
        kw = dict(look=(-1, -1), mood="calm" if t < T_SQUEAK else "shock", arms="down")
    elif 23.2 <= t < T_DISH + 0.4:          # gasp as the Duck is carried away
        bow = 0.0
        kw = dict(look=(-0.5, -1), mood="shock", arms="up")
    elif T_DISH + 0.4 <= t < 32.0:
        bow = 0.0
        kw = dict(look=(-1, -0.6), mood="calm", arms="down")
    elif t >= 32.0:                         # bow to Dill
        b = ease(seg(t, 32.0 + 0.12 * k, 32.35 + 0.12 * k))
        bow = -0.6 * b
        kw = dict(look=(-1, -0.6), mood="closed" if b > 0.6 else "calm", arms="down")
    return x, FRONT, bow, kw


def grandma_pose(t):
    bow = -0.6
    kw = dict(look=(-1, 0.6), mood="closed")
    if 13.0 <= t < 13.75:                   # Grandma peeks at Crumb, spectacles glinting
        b = 1 - ease(seg(t, 13.0, 13.2)) * (1 - ease(seg(t, 13.5, 13.75)))
        bow = -0.6 * b
        kw = dict(look=(1, -0.4), mood="stern")
    if T_OPEN <= t < 32.0:
        bow = -0.6 * (1 - ease(seg(t, T_OPEN, T_OPEN + 0.3)))
        kw = dict(look=(-1, -1), mood="stern" if t < 23.2 or t > T_DISH else "angry")
    elif t >= 32.0:
        b = ease(seg(t, 32.7, 33.1)) * (1 - ease(seg(t, 33.8, 34.1)))
        bow = -0.6 * b
        kw = dict(look=(-1, -0.6), mood="closed" if b > 0.5 else "stern", cane="up" if t >= 33.9 else "down")
    return G_LINE_X, FRONT, bow, kw


def hand_state(t):
    """(x, tip_y, grip, carrying) or None."""
    X = DUCK_X + 20
    if T_OPEN + 0.3 <= t < T_SQUEAK:
        return X, lerp(-400, FLOOR - 650, ease_out(seg(t, T_OPEN + 0.3, T_SQUEAK))), 0.0, None
    if T_SQUEAK <= t < 21.3:     # freezes mid-air at the squeak
        return X, FLOOR - 650 + 10 * math.sin((t - T_SQUEAK) * 30) * (1 - seg(t, T_SQUEAK, T_SQUEAK + 0.5)), 0.0, None
    if 21.3 <= t < T_GRIP:       # gently comes down
        return X, lerp(FLOOR - 650, FLOOR - 120, ease(seg(t, 21.3, T_GRIP))), 0.0, None
    if T_GRIP <= t < T_LIFT:
        return X, FLOOR - 120, ease(seg(t, T_GRIP, T_LIFT)), "duck"
    if T_LIFT <= t < 25.0:       # lifts it away, slowly, lovingly
        return X, lerp(FLOOR - 120, -700, ease(seg(t, T_LIFT, 25.0))), 1.0, "duck"
    if 27.6 <= t < T_DISH:       # brings back the butter dish
        return X, lerp(-600, FLOOR - 120, ease(seg(t, 27.6, T_DISH))), 1.0, "dish"
    if T_DISH <= t < T_DISH + 0.3:
        return X, FLOOR - 120, 1 - ease(seg(t, T_DISH, T_DISH + 0.3)), None
    if T_DISH + 0.3 <= t < T_CLOSE:
        return X, lerp(FLOOR - 120, -600, ease(seg(t, T_DISH + 0.3, T_CLOSE))), 0.0, None
    return None


# ---------------- camera ----------------
def camera(t):
    if t < 3.6:      # inside the drawer
        k = ease(seg(t, 2.0, 3.6))
        return lerp(760, 750, k), lerp(1400, 1360, k), lerp(2.3, 2.15, k)
    if t < 4.6:      # shelf: watch Dill fly up and land
        return 900, FLOOR - 250, 1.75
    if t < 12.0:     # huddle behind the jello
        k = ease(seg(t, 4.6, 5.2))
        return lerp(900, 955, k), lerp(FLOOR - 250, FLOOR - 300, k), lerp(1.75, 2.3, k)
    if t < 17.0:     # follow Crumb's tiptoe
        cs = crumb_state(t)
        k = ease(seg(t, 12.0, 12.6))
        x = min(900, max(620, cs[0] - 40))
        return lerp(975, x, k), lerp(FLOOR - 300, FLOOR - 210, k), lerp(2.3, 2.0, k)
    if t < T_OPEN:   # the door seal
        return SEAL_X + 20, FLOOR - 230, 2.6
    if t < 21.3:     # wide: door open, the Hand, SQUEAK
        z = 1.45
        if T_SQUEAK <= t:
            z += 0.18 * ease_out(seg(t, T_SQUEAK, T_SQUEAK + 0.12)) * (1 - ease(seg(t, 20.4, 21.2)))
        return 500, FLOOR - 430, z
    if t < 25.0:     # pick-up
        k = ease(seg(t, T_LIFT, 24.6))
        return 500, lerp(FLOOR - 430, FLOOR - 560, k), 1.45
    if t < 27.6:     # everybody stares up (vignette above)
        return 500, FLOOR - 560, 1.45
    if t < T_LEAP:   # butter dish returns
        k = ease(seg(t, 27.6, 28.4))
        return 500, lerp(FLOOR - 560, FLOOR - 400, k), 1.45
    if t < 32.0:     # the leap
        return 560, FLOOR - 400, 1.5
    if t < 34.6:     # push in on the celebration
        k = ease(seg(t, 32.0, 34.4))
        return lerp(560, 450, k), lerp(FLOOR - 400, FLOOR - 300, k), lerp(1.5, 1.8, k)
    # drift up to the top shelf: the egg
    k = ease(seg(t, 34.6, 35.9))
    zp = 0.0
    for tp in (T_CRACK, T_CRACK + 0.6):
        if t >= tp:
            zp += 0.25 * ease_out(seg(t, tp, tp + 0.1))
    return lerp(450, EGG_X - 10, k), lerp(FLOOR - 300, TOP - 120, k), lerp(1.8, 3.3, k) + zp


# ---------------- scenes ----------------
def drawer_scene(c, t):
    cx, cy, Z = camera(t)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    random.seed(int(t * 30))
    drawer_inside_bg(c, t)
    FL = 1550
    # Wilt bends its floppy top down for Dill, then springs it back up
    if t < 2.5:
        droop = 0.0
    elif t < 2.9:
        droop = ease(seg(t, 2.5, 2.9))
    elif t < T_FLING:
        droop = 1.0 + 0.06 * math.sin((t - 2.9) * 40)
    else:
        droop = max(0.0, 1 - ease_out(seg(t, T_FLING, T_FLING + 0.18)) * 1.25)
    wilt(c, 880, FL, droop=min(1.0, droop), look=(-1, 0.3) if t < T_FLING else (-0.5, -1))
    # Dill
    if t < 2.6:
        dill(c, 640, FL, mood="sad", look=(1, 0), arm="down", crown_on=True, sq=0.9)
    elif t < 2.95:      # hops onto the leaf tip
        p = seg(t, 2.6, 2.95)
        dill(c, lerp(640, 712, p), lerp(FL, 1420, p) - 120 * math.sin(math.pi * p), mood="frozen", look=(1, 0), arm="reach")
    elif t < T_FLING:
        dill(c, 712, 1420 + 8 * math.sin((t - 2.95) * 40), mood="frozen", look=(0, -1), arm="reach", sq=0.92)
    else:               # FLUNG
        p = seg(t, T_FLING, 3.6)
        dill(c, lerp(712, 760, p), lerp(1420, 600, ease_out(p)), mood="shocked", look=(0, -1), arm="reach", rot=-p * 3)
    if t >= T_FLING:
        s = back_out(seg(t, T_FLING, T_FLING + 0.15))
        c.save(); c.translate(820, 1100); c.rotate(-0.12); c.scale(S(s), S(s)); text(c, "SPROING!", 0, 0, 80, hexc("#C5D86D"), olw=12); c.restore()
    c.rectangle(-400, -400, W + 800, H + 800); c.set_source_rgba(0.02, 0.06, 0.08, 0.12); c.fill()


def doodle_icon(cc):
    cc.save(); cc.scale(120, 92); cc.arc(0, 0, 0.92, 0, 2 * math.pi); cc.restore(); cc.clip()
    cc.save(); cc.translate(-6, 0); cc.scale(0.28, 0.28); hand(cc, 0, 160, 0.4); cc.restore()
    cc.save(); cc.translate(-10, 80); cc.scale(0.45, 0.45); duck(cc, 0, 0, turn=1.0); cap_crown(cc, 6, -186, 0.38); cc.restore()
    heart(cc, 70, -40, 1.6, 1.0); heart(cc, -78, -10, 1.2, 1.0); heart(cc, 74, 30, 1.0, 1.0)


def plan_icon(cc):
    cc.save(); cc.scale(120, 92); cc.arc(0, 0, 0.92, 0, 2 * math.pi); cc.restore(); cc.clip()
    # light from the door (left), the Duck squeaking, the Hand coming
    cc.save(); cc.translate(-46, 74); cc.scale(0.42, 0.42); duck(cc, 0, 0, turn=1.0); cc.restore()
    cc.set_source_rgb(*hexc("#FF922B")); cc.set_line_width(6); cc.set_line_cap(cairo.LINE_CAP_ROUND)
    for r in (28, 46):
        cc.arc(-46, 10, r + 20, -2.5, -0.7); cc.stroke()
    cc.save(); cc.translate(60, -10); cc.scale(0.26, 0.26); hand(cc, 0, 120, 0.0); cc.restore()
    cc.set_source_rgb(*INK); cc.set_line_width(7)
    cc.move_to(8, -42); cc.line_to(30, -60); cc.move_to(8, -42); cc.line_to(18, -18); cc.stroke()   # arrow tip pointing at duck
    cc.move_to(8, -42); cc.curve_to(30, -70, 40, -70, 46, -60); cc.stroke()


def vignette(c, t):
    """Far away, the Duck's true home: a steaming bathtub. Drawn in screen space."""
    a = ease(seg(t, 25.0, 25.5)) * (1 - ease(seg(t, 27.3, 27.7)))
    if a <= 0.01:
        return
    cx, cy, R = W / 2, 520, 360
    c.save()
    c.push_group()
    c.save(); c.translate(cx, cy)
    c.move_to(R, 0)
    for i in range(1, 25):
        ang = i / 24 * 2 * math.pi
        rr = R + 24 * (i % 2)
        c.line_to(rr * math.cos(ang), rr * math.sin(ang) * 0.8)
    c.close_path(); c.restore()
    c.set_source_rgb(*hexc("#F1E8FF")); c.fill_preserve(); c.save(); c.clip()
    # tiles
    c.set_source_rgba(0.6, 0.55, 0.8, 0.35); c.set_line_width(4)
    for i in range(-6, 7):
        c.move_to(cx + i * 70, cy - 400); c.line_to(cx + i * 70, cy + 400); c.stroke()
        c.move_to(cx - 400, cy + i * 70); c.line_to(cx + 400, cy + i * 70); c.stroke()
    # tub
    rrect(c, cx - 300, cy + 40, 600, 300, 80); c.set_source_rgb(1, 1, 1); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    # water + bobbing duck silhouette
    bob = 8 * math.sin(t * 5)
    c.save(); c.translate(cx + 20 * math.sin(t * 1.5), cy + 60 + bob); c.scale(0.8, 0.8)
    c.set_source_rgba(*hexc("#3B2F45"), 0.85)
    c.save(); c.translate(0, -58); c.scale(92, 58); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    c.save(); c.translate(4, -142); c.scale(54, 52); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); c.fill()
    c.move_to(-80, -80); c.line_to(-120, -112); c.line_to(-84, -46); c.close_path(); c.fill()
    c.move_to(-44, -196); c.line_to(52, -196); c.line_to(48, -216); c.line_to(-40, -216); c.close_path(); c.fill()   # its little cap
    c.restore()
    c.rectangle(cx - 296, cy + 70, 592, 30); c.set_source_rgb(*hexc("#A5D8FF")); c.fill()
    for i in range(6):
        ellipse(c, cx - 250 + i * 100, cy + 70, 40, 14, hexc("#E7F5FF"), lw=4)
    # steam
    for j in range(5):
        q = ((t - 25.0) * 0.45 + j / 5) % 1
        ellipse(c, cx - 220 + j * 110 + 30 * math.sin(q * 6 + j), cy - 20 - q * 300, 40 + 30 * q, 30 + 20 * q,
                (1, 1, 1), stroke=False)
    # hearts drifting up
    for j in range(3):
        q = ((t - 25.0) * 0.6 + j / 3) % 1
        heart(c, cx + 150 - j * 120, cy - 40 - q * 220, 1.8, 1 - q)
    c.restore()
    c.save(); c.translate(cx, cy)
    c.move_to(R, 0)
    for i in range(1, 25):
        ang = i / 24 * 2 * math.pi
        rr = R + 24 * (i % 2)
        c.line_to(rr * math.cos(ang), rr * math.sin(ang) * 0.8)
    c.close_path(); c.restore()
    c.set_source_rgb(*INK); c.set_line_width(10); c.stroke()
    # little thought-puffs leading down to the pickles
    for i, (px, py, r) in enumerate([(560, 960, 34), (590, 1050, 24), (615, 1120, 16)]):
        ellipse(c, px, py, r, r * 0.8, hexc("#F1E8FF"), lw=6)
    c.pop_group_to_source(); c.paint_with_alpha(a)
    c.restore()


def shelf_scene(c, t):
    cx, cy, Z = camera(t)
    L = light_at(t)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    random.seed(int(t * 30))
    if T_DISH <= t < T_DISH + 0.3 or T_CLOSE + 0.3 <= t < T_CLOSE + 0.6:
        k = 1 - seg(t, T_DISH, T_DISH + 0.3) if t < T_CLOSE else 1 - seg(t, T_CLOSE + 0.3, T_CLOSE + 0.6)
        c.translate(random.uniform(-14, 14) * k, random.uniform(-14, 14) * k)
    fridge6(c, L, 0, lid=False)
    god_rays(c, L)
    lid_piece(c, 760, TOP - 25, 0.0)

    # the egg on the top shelf
    rot, crack, gap, eyes = 0.0, 0.0, 0.0, 0.0
    if 35.8 <= t < T_CRACK:
        rot = 0.12 * math.sin((t - 35.8) * 14) * seg(t, 35.8, 36.2)
    if t >= T_CRACK:
        crack = lerp(0.55, 1.0, seg(t, T_CRACK + 0.6, T_CRACK + 0.7))
        gap = ease(seg(t, T_CRACK + 0.8, T_CRACK + 1.05))
        eyes = back_out(seg(t, T_CRACK + 1.05, T_CRACK + 1.25))
        rot = 0.05 * math.sin((t - T_CRACK) * 30) * (1 - seg(t, T_CRACK, T_CRACK + 0.4))
    cracking_egg(c, EGG_X, TOP, rot, crack, gap, eyes)

    # jello
    c.save(); c.translate(JELLO_X, FLOOR); c.scale(1.8, 1.8); c.translate(-JELLO_X, -FLOOR)
    wob = math.sin((t - T_LAND) * 20) * (1 - seg(t, T_LAND, T_LAND + 0.7)) if T_LAND <= t < T_LAND + 0.7 else 0.0
    jello_args = (JELLO_X, FLOOR, wob)
    c.restore()

    ds = dill_state(t)
    cs = crumb_state(t)
    behind_jello = t < 12.0
    # Dill + Crumb behind the jello first
    if behind_jello:
        if ds:
            x, y, kw = ds; th = kw.pop("thumb", False); dill(c, x, y, crown_on=True, **kw)
        x, y, kw = cs; crumb_notched(c, x, y, True, **kw)
    c.save(); c.translate(JELLO_X, FLOOR); c.scale(1.8, 1.8); c.translate(-JELLO_X, -FLOOR)
    jello(c, *jello_args); c.restore()

    # the Duck (on the throne spot, then in the Hand), or the butter dish
    hs = hand_state(t)
    duck_sq = 1.0
    if T_SQUEAK <= t < 20.7:
        duck_sq = 0.72 + 0.06 * math.sin((t - T_SQUEAK) * 30) * (1 - seg(t, T_SQUEAK, 20.3))
    elif 20.7 <= t < 21.1:
        duck_sq = lerp(0.72, 1.0, back_out(seg(t, 20.7, 21.1)))
    if hs:
        hx, tip, grip, carry = hs
        hand(c, hx, tip, grip)
        if carry == "duck":
            the_duck(c, DUCK_X, tip + 120 + 0 * grip)
        elif carry == "dish":
            butter_dish_bitten(c, DUCK_X, tip + 120)
    if t < T_GRIP:
        the_duck(c, DUCK_X, FLOOR, 1 / duck_sq ** 0.4, duck_sq)
    if t >= T_DISH:
        butter_dish_bitten(c, DUCK_X, FLOOR)

    # Crumb (after leaving the jello) walks behind the pickle line
    if not behind_jello:
        x, y, kw = cs; crumb_notched(c, x, y, True, **kw)

    # pickles + Grandma
    bodies = [(pickle_pose(k, t), "p", k) for k in range(5)] + [(grandma_pose(t), "g", 0)]
    for (x, y, bow, kw), kind, k in sorted(bodies, key=lambda b: -b[0][0]):
        if kind == "p":
            pickle_kid(c, x, y, k, bow=bow, **kw)
        else:
            grandma(c, x, y, bow=bow, **kw)
    if 13.05 <= t < 13.6:   # spectacle glint
        star(c, G_LINE_X + 20, FRONT - 120, 16 * math.sin(math.pi * seg(t, 13.05, 13.6)), t * 4, (1, 1, 1))

    # Dill (front) after the jello huddle
    if ds and not behind_jello:
        x, y, kw = ds
        th = kw.pop("thumb", False)
        dill(c, x, y, crown_on=True, **kw)
        if th:
            s = back_out(seg(t, 17.25, 17.45))
            thumbs_up(c, x - 152, y - 178, 1.4 * s)
    door_seal(c, SEAL_X + 55)
    if 17.3 <= t < 18.0:
        star(c, SEAL_X - 170, FLOOR - 260, 30 * math.sin(math.pi * seg(t, 17.3, 18.0)), t * 5, (1, 1, 1))

    # ---- effects ----
    def word(s, x, y, size, col, t0, t1, rot=0.0):
        if t0 <= t < t1:
            k = back_out(seg(t, t0, t0 + 0.2))
            c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(k), S(k)); text(c, s, 0, 0, size, col, olw=12); c.restore()
    word("THUMP", 900, FLOOR - 470, 60, (1, 1, 1), T_LAND, T_LAND + 0.6, 0.1)
    bubble(c, 935, FLOOR - 590, back_out(seg(t, 5.0, 5.3)) * (1 - seg(t, 8.0, 8.3)), doodle_icon)
    bubble(c, 935, FLOOR - 590, back_out(seg(t, 8.5, 8.8)) * (1 - seg(t, 9.7, 10.0)), plan_icon)
    if 8.2 <= t < 9.0:
        s = back_out(seg(t, 8.2, 8.35))
        c.save(); c.translate(1080, FLOOR - 470); c.scale(S(s), S(s)); text(c, "!", 0, 0, 100, GOLD, olw=12); c.restore()
    if 9.9 <= t < 10.5:
        word("gulp", 1090, FLOOR - 450, 44, (1, 1, 1), 9.9, 10.5, 0.1)
    if 10.6 <= t < 11.3:   # salute "ting"
        star(c, JELLO_X + 75 + 115, FLOOR - 185 - 215, 26 * math.sin(math.pi * seg(t, 10.6, 11.3)), t * 6, (1, 1, 1))
    for t0 in (13.0, 15.0):   # freeze!
        if t0 <= t < t0 + 0.7:
            x = crumb_state(t)[0]
            s = back_out(seg(t, t0, t0 + 0.12))
            c.save(); c.translate(x, FLOOR - 400); c.scale(S(s), S(s)); text(c, "!", 0, 0, 90, (1, 0.35, 0.35), olw=10); c.restore()
    word("SQUEEEAK!", 560, FLOOR - 470, 92, hexc("#FFD43B"), T_SQUEAK, T_SQUEAK + 1.1, -0.08)
    sq_rings(c, DUCK_X, FLOOR - 110, t, T_SQUEAK, 1.2, hexc("#FFD43B"))
    if 23.0 <= t < 25.2:   # the Hand's hearts as it lifts the Duck
        hs2 = hand_state(min(t, 24.99))
        tip = hs2[1] if hs2 else -700
        for j in range(4):
            q = ((t - 23.0) * 0.9 + j / 4) % 1
            heart(c, DUCK_X - 160 + j * 100, tip + 60 - q * 260, 2.4, 1 - q)
    if 23.2 <= t < 24.2:
        word("GASP!", 760, FRONT - 330, 70, (1, 1, 1), 23.2, 24.2, 0.08)
    word("CLUNK", 300, FLOOR - 240, 64, (1, 1, 1), T_DISH, T_DISH + 0.7, -0.1)
    word("THUD", 900, FLOOR - 700, 70, (1, 1, 1), T_CLOSE + 0.3, T_CLOSE + 0.9, 0.08)
    if T_SWORD <= t:
        confetti(c, t, T_SWORD + 0.05, DUCK_X + 80, FLOOR - 350, 70, 7)
        confetti(c, t, T_SWORD + 0.45, 760, FLOOR - 250, 50, 11)
        confetti(c, t, T_SWORD + 0.85, 300, FLOOR - 300, 40, 3)
    if t >= 32.2:          # Crumb's happy tears
        for j in range(2):
            q = ((t - 32.2) * 1.4 + j * 0.5) % 1
            for sx in (-26, 26):
                ellipse(c, CRUMB_SIT + sx + (-12 if sx < 0 else 12) * q, FRONT + 30 - 150 + q * 90, 7, 10, TEAR, lw=2)
    word("CRACK!", EGG_X - 30, TOP - 230, 46, (1, 1, 1), T_CRACK, T_CRACK + 0.5, -0.1)
    word("CRACK!", EGG_X + 10, TOP - 200, 54, (1, 1, 1), T_CRACK + 0.6, T_CRACK + 1.1, 0.1)
    if t >= T_CRACK + 1.3:
        word("peep", EGG_X + 70, TOP - 165, 34, hexc("#FFE680"), T_CRACK + 1.3, END_T, 0.15)
    dark_overlay(c, L)


def frame(c, t):
    if t < 2.0:
        title_card(c, t)
        if t > 1.7:
            iris(c, W / 2, H / 2, lerp(1200, 0, ease(seg(t, 1.7, 2.0))))
        return
    if t >= END_T:
        end_card(c, t, END_T); return
    c.save()
    if t < 3.6:
        drawer_scene(c, t)
    else:
        shelf_scene(c, t)
    c.restore()
    if 25.0 <= t < 27.7:
        vignette(c, t)
    if t < 2.4:
        iris(c, W / 2, H / 2, lerp(0, 1400, ease(seg(t, 2.0, 2.4))))
    if 3.6 <= t < 3.75:   # whip cut up to the shelf
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.5 * (1 - seg(t, 3.6, 3.75))); c.fill()
    if T_OPEN <= t < T_OPEN + 0.25:   # door-open flash
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.7 * (1 - seg(t, T_OPEN, T_OPEN + 0.25))); c.fill()
    if t >= END_T - 0.4:
        cx, cy, Z = camera(t)
        iris(c, W / 2 + (EGG_X - cx) * Z, H / 2 + (TOP - 70 - cy) * Z, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))


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
