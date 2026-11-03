"""FRIDGE KINGDOM — Episode 4: "Knock Knock". ~39.6s, 1080x1920 @ 30fps.

Variant B (cold open): no title card; a small title banner sits across the top for the first 2s.

Outside, Dill pounds on the fridge door; inside, Crumb jumps at every knock and builds an egg
barricade. Dill climbs the magnets (the pizza slides down with him), hangs from the handle,
and is flung inside like a wrecking ball when the Hand opens the door. Egg wall smashed, both
yolky, a hug, the crown returned... and the Duck is sitting in Dill's throne spot.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crumb, duck, hand, crown, fridge_bg, dark_overlay, ellipse, rrect, star, text,
                 iris, hexc, seg, ease, ease_out, lerp, back_out, INK, GOLD, FLOOR, TOP, W, H, FPS, S, BREAD, CRUST)
from ep2 import end_card
from ep3 import kitchen_bg, FY, FX0, FX1
from animate import heart

DUR = 39.6
END_T = 38.0
SPLIT = 960                       # split-screen divider (0–5s)
CUT_IN = 5.0                      # inside: egg wall
CUT_OUT = 11.0                    # outside: the climb
CUT_IN2 = 24.7                    # inside: wrecking ball
YOLK, YOLK_D, WHITE = hexc("#FFB703"), hexc("#F08C00"), hexc("#FFF9EC")
TOOTHPICK = hexc("#E9C98B")

# ---- outside door layout (ep3 world: floor FY, fridge FX0..FX1) ----
D_TOP, D_BOT = FY - 2700, FY - 130
MAGNETS = {"banana": (0.30, FY - 430), "star": (0.19, FY - 820), "pizza": (0.46, FY - 1210)}
HANDLE_U, HANDLE_Y0, HANDLE_Y1 = 0.06, FY - 1750, FY - 1050
KNOCKS_SPLIT = [-0.25, 0.75, 1.75, 2.75, 3.55, 4.3]


# ---------------- props ----------------
def egg(c, x, y, s=1.0, rot=0.0, crack=0.0):
    """Egg standing with its bottom at (x, y)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(s), S(s))
    ellipse(c, 0, -70, 56, 70, WHITE, lw=6)
    ellipse(c, -20, -98, 10, 18, (1, 1, 1), stroke=False)
    if crack > 0:
        c.set_source_rgb(*INK); c.set_line_width(4)
        c.move_to(-50, -60)
        for i in range(1, 9):
            px = -50 + 100 * i / 8 * min(1, crack * 1.2)
            c.line_to(px, -60 + (12 if i % 2 else -10))
        c.stroke()
    c.restore()


def shell(c, x, y, s, rot, top=True):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(s), S(s))
    if top:
        c.move_to(-56, 0); c.curve_to(-56, -80, 56, -80, 56, 0)
    else:
        c.move_to(-56, 0); c.curve_to(-56, 70, 56, 70, 56, 0)
    for i in range(8):
        c.line_to(56 - 112 * (i + 1) / 8, (10 if i % 2 == 0 else -6))
    c.close_path(); c.set_source_rgb(*WHITE); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.restore()


def yolk_blob(c, x, y, r, seed=0):
    rnd = random.Random(seed)
    c.save(); c.translate(x, y)
    c.move_to(r, 0)
    for i in range(1, 13):
        a = i * math.pi / 6
        rr = r * (0.8 + 0.35 * rnd.random())
        c.line_to(rr * math.cos(a), rr * 0.8 * math.sin(a))
    c.close_path(); c.set_source_rgb(*YOLK); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(4); c.stroke()
    ellipse(c, -r * 0.3, -r * 0.3, r * 0.22, r * 0.15, hexc("#FFE08A"), stroke=False)
    c.restore()


def goo(c, x, y, t, seed, h=280, n=5, top=290):
    """Yolk and egg-white splotches on a character standing at (x, y), with drips. Keeps the face clear."""
    rnd = random.Random(seed)
    yolk_blob(c, x - 30, y - top, 24, seed * 7)
    for k in range(n):
        bx = x + rnd.uniform(-55, 55); by = y - rnd.uniform(40, h)
        r = rnd.uniform(18, 32)
        if k % 3 == 2:
            ellipse(c, bx, by, r * 1.2, r, WHITE, lw=3)
        else:
            yolk_blob(c, bx, by, r, seed * 10 + k)
        # drip
        q = (t * 0.9 + rnd.random()) % 1
        ellipse(c, bx + 4, by + r + q * (y - by - r + 10), 6 * (1 - 0.4 * q), 9 * (1 - 0.4 * q), YOLK, lw=3)


def toothpick_spear(c, x0, y0, ang, L=230):
    c.save(); c.translate(x0, y0); c.rotate(ang); c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_source_rgb(*INK); c.set_line_width(15); c.move_to(-40, 0); c.line_to(L, 0); c.stroke()
    c.set_source_rgb(*TOOTHPICK); c.set_line_width(9); c.move_to(-40, 0); c.line_to(L, 0); c.stroke()
    c.restore()


def door_geom(th):
    xl = FX1 - (FX1 - FX0) * math.cos(th)
    e = 160 * math.sin(th)

    def at(u, y):
        x = lerp(xl, FX1, u)
        yy = y + (1 - u) * e * ((y - (D_TOP + D_BOT) / 2) / ((D_BOT - D_TOP) / 2))
        return x, yy
    return xl, e, at


def magnet(c, kind, x, y, sx=1.0):
    c.save(); c.translate(x, y); c.scale(S(sx), 1)
    if kind == "banana":
        c.move_to(-90, -20); c.curve_to(-50, 60, 60, 60, 100, -30); c.curve_to(50, 24, -40, 24, -90, -20)
        c.set_source_rgb(*hexc("#FFE066")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        ellipse(c, 100, -30, 8, 8, hexc("#5C3D2E"), stroke=False)
    elif kind == "star":
        star(c, 0, 0, 85, 0.0, hexc("#FF922B"))
    else:
        c.move_to(-75, -62); c.line_to(75, -62); c.line_to(0, 88); c.close_path()
        c.set_source_rgb(*hexc("#FFC078")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        rrect(c, -82, -76, 164, 22, 8); c.set_source_rgb(*hexc("#D9480F")); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        for px, py in [(-28, -30), (22, -18), (0, 20)]:
            ellipse(c, px, py, 13, 13, hexc("#E03131"), lw=3)
    c.restore()


def magnet_pos(kind, th=0.0, pizza_dy=0.0):
    u, y = MAGNETS[kind]
    if kind == "pizza":
        y += pizza_dy
    return door_geom(th)[2](u, y)


def fridge_door(c, th, pizza_dy=0.0, light=1.0):
    xl, e, at = door_geom(th)
    c.rectangle(FX0, D_TOP, FX1 - FX0, FY - D_TOP); c.set_source_rgb(*hexc("#DDE7EE")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(10); c.stroke()
    c.rectangle(FX0 + 20, FY - 120, FX1 - FX0 - 40, 110); c.set_source_rgb(*hexc("#868E96")); c.fill()
    for k in range(10):
        c.rectangle(FX0 + 60 + k * 120, FY - 95, 60, 14); c.set_source_rgb(*hexc("#495057")); c.fill()
    if xl > FX0 + 2:
        c.save(); c.rectangle(FX0 + 10, D_TOP + 10, xl - FX0 - 10, D_BOT - D_TOP - 10); c.clip()
        g = cairo.LinearGradient(FX0, 0, xl, 0)
        g.add_color_stop_rgb(0, *hexc("#F3FAFF")); g.add_color_stop_rgb(1, *hexc("#BFE0F5"))
        c.set_source(g); c.paint()
        for sy in (D_BOT - 700, D_BOT - 1450):
            c.rectangle(FX0, sy, 3000, 26); c.set_source_rgba(*hexc("#74C0FC"), 0.8); c.fill()
        c.restore()
        c.move_to(FX0, FY); c.line_to(xl, FY); c.line_to(xl - 200, FY + 300); c.line_to(FX0 - 500, FY + 300); c.close_path()
        c.set_source_rgba(1, 1, 0.85, 0.35 * min(1, (xl - FX0) / 200)); c.fill()
    c.move_to(xl, D_TOP - e); c.line_to(FX1, D_TOP); c.line_to(FX1, D_BOT); c.line_to(xl, D_BOT + e); c.close_path()
    c.set_source_rgb(*hexc("#F1F5F9")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(10); c.stroke()
    hx, hy0 = at(HANDLE_U, HANDLE_Y0); _, hy1 = at(HANDLE_U, HANDLE_Y1)
    rrect(c, hx - 24, hy0, 48, hy1 - hy0, 24); c.set_source_rgb(*hexc("#ADB5BD")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    sx = max(math.cos(th), 0.25)
    for kind in ("banana", "star", "pizza"):
        x, y = magnet_pos(kind, th, pizza_dy)
        magnet(c, kind, x, y, sx)


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
    text(c, "Ep. 4:  Knock Knock", W / 2, 182, 46, (1, 1, 1), olw=8)
    c.restore()


# ---------------- split screen (0–5s) ----------------
def knock_pulse(t, times, d=0.35):
    for t0 in times:
        if t0 <= t < t0 + d:
            return 1 - seg(t, t0, t0 + d), t0
    return 0.0, None


def split_outside(c, t):
    cx, cy, Z = 3110, FY - 330, 1.3
    c.translate(W / 2, SPLIT / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    k, t0 = knock_pulse(t, KNOCKS_SPLIT, 0.3)
    random.seed(int(t * 30))
    kitchen_bg(c); fridge_door(c, 0.0)
    pound = k > 0.4
    dill(c, 3040 + 18 * k, FY, "angry", look=(1, 0), arm="pound" if pound else "down", crown_on=False,
         shake=4 + 4 * k, rot=0.12 * k)
    # steam
    for j in range(3):
        q = (t * 1.4 + j / 3) % 1
        ellipse(c, 3010 + j * 40 + 16 * math.sin(q * 6), FY - 320 - q * 160, 20 + 22 * q, 16 + 18 * q, (1, 1, 1), stroke=False)
    if t0 is not None and t0 >= 0:
        s = back_out(min(1, (1 - k) * 3))
        c.save(); c.translate(3330, FY - 420); c.rotate(-0.12); c.scale(S(s), S(s))
        text(c, "KNOCK!", 0, 0, 84, hexc("#FFD43B"), olw=10); c.restore()


def split_inside(c, t):
    cx, cy, Z = 560, FLOOR - 270, 1.3
    c.translate(W / 2, SPLIT + (H - SPLIT) / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    fridge_bg(c, 0.0)
    # Crumb jumps (and screams) right after each knock
    jump = 0.0; scream = False
    for t0 in KNOCKS_SPLIT:
        p = seg(t, t0 + 0.05, t0 + 0.6)
        if 0 < p < 1:
            jump = max(jump, math.sin(math.pi * p)); scream = True
    random.seed(int(t * 30))
    crumb(c, 470, FLOOR - 170 * jump, "scared", look=(1, -0.3), crown_on=True, shake=6 if scream else 2,
          arm="wave" if scream else "down", rot=-0.12 * jump)
    if scream:
        for j in range(3):
            a = -0.9 + j * 0.45
            c.set_source_rgb(*INK); c.set_line_width(6)
            c.move_to(470 + 170 * math.cos(a), FLOOR - 230 - 170 * jump + 170 * math.sin(a))
            c.line_to(470 + 230 * math.cos(a), FLOOR - 230 - 170 * jump + 230 * math.sin(a)); c.stroke()
    k, t0 = knock_pulse(t, KNOCKS_SPLIT, 0.4)
    if k > 0:
        c.save(); c.translate(840, FLOOR - 430); c.rotate(0.1); c.scale(S(back_out(min(1, (1 - k) * 3))), S(back_out(min(1, (1 - k) * 3))))
        text(c, "knock", 0, 0, 64, hexc("#FFD8A8"), olw=8); c.restore()
    dark_overlay(c, 0.0)


def split_screen(c, t):
    c.save(); c.rectangle(0, 0, W, SPLIT); c.clip(); split_outside(c, t); c.restore()
    c.save(); c.rectangle(0, SPLIT, W, H - SPLIT); c.clip(); split_inside(c, t); c.restore()
    c.rectangle(-10, SPLIT - 10, W + 20, 20); c.set_source_rgb(1, 1, 1); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()


# ---------------- inside: the egg wall (5–11s) ----------------
WALL = [(650, 0), (760, 0), (870, 0), (705, 1), (815, 1), (760, 2)]
EGG_T0 = 5.55
EGG_DT = 0.68
KNOCKS_IN = [5.3, 7.4, 9.55, 10.45]


def wall_pos(i):
    x, row = WALL[i]
    return x, FLOOR - row * 128


def egg_wall(c, t, n=6, wob=0.0):
    for i in range(n):
        x, y = wall_pos(i)
        row = WALL[i][1]
        egg(c, x + wob * 10 * (row + 1) * math.sin(t * 9 + i), y, 1.0, wob * 0.06 * (row + 1) * math.sin(t * 9 + i * 2))


def eggs_placed(t):
    return sum(1 for i in range(6) if t >= EGG_T0 + i * EGG_DT + 0.5)


def inside_eggs(c, t):
    z = ease(seg(t, 10.2, 10.9))
    cx, cy, Z = lerp(640, 660, z), lerp(FLOOR - 330, FLOOR - 300, z), lerp(1.62, 1.75, z)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    random.seed(int(t * 30))
    k, _ = knock_pulse(t, KNOCKS_IN, 0.3)
    if k > 0:
        c.translate(random.uniform(-10, 10) * k, random.uniform(-5, 5) * k)
    fridge_bg(c, 0.0)
    # the Duck: perched on top of the finished egg wall for a moment. Nobody notices.
    duck_on = 10.25 <= t < 10.85
    egg_wall(c, t, eggs_placed(t), wob=k + 0.25 * (t > 9.4))
    if duck_on:
        tx, ty = wall_pos(5)
        duck(c, tx, ty - 132, turn=1.0, s=0.62)
    # Crumb shuttles eggs in from off-screen left
    if t < EGG_T0 + 6 * EGG_DT:
        i = min(5, int((t - EGG_T0) / EGG_DT)) if t >= EGG_T0 else -1
        if i < 0:   # first knock: jump, then dash
            p = seg(t, 5.3, 5.55)
            crumb(c, 520, FLOOR - 120 * math.sin(math.pi * p), "scared", look=(1, 0), crown_on=True, shake=5)
        else:
            ph = (t - (EGG_T0 + i * EGG_DT)) / EGG_DT
            tx, ty = wall_pos(i)
            if ph < 0.35:     # dash left (empty-handed)
                x = lerp(tx - 120, 150, ease(ph / 0.35)); carry = False
            elif ph < 0.75:   # dash back with an egg over his head
                x = lerp(150, tx - 120, ease((ph - 0.35) / 0.4)); carry = True
            else:
                x = tx - 120; carry = False
            hop = abs(math.sin(ph * math.pi * 4)) * 26
            crumb(c, x, FLOOR - hop, "worried", look=(1 if ph >= 0.35 else -1, 0), crown_on=True, rot=0.15 if ph >= 0.35 else -0.15)
            # speed lines
            c.set_source_rgba(1, 1, 1, 0.5); c.set_line_width(6)
            for j in range(3):
                d = -1 if ph >= 0.35 else 1
                c.move_to(x + d * 90, FLOOR - 80 - j * 70); c.line_to(x + d * 190, FLOOR - 80 - j * 70); c.stroke()
            if carry:
                egg(c, x, FLOOR - 330 - hop, 0.8)
            elif ph >= 0.75:   # the egg drops into place
                q = seg(ph, 0.75, 1.0)
                egg(c, tx, lerp(ty - 120, ty, q * q), 1.0)
    else:
        # hides, shaking, with a toothpick spear; peeks at the door
        peek = ease(seg(t, 10.1, 10.4)) * (1 - ease(seg(t, 10.85, 11.0)))
        bow = lerp(-0.18, 0.12, peek)
        random.seed(int(t * 30))
        crumb(c, 500, FLOOR, "scared", look=(1, -0.2 * (1 - peek)), crown_on=True, shake=3 + 5 * k, bow=bow)
        toothpick_spear(c, 560, FLOOR - 90 + 0 * peek, -0.35)
        if t < 10.0:
            s = back_out(seg(t, 9.4, 9.6))
            for j in range(3):   # nervous sweat
                q = (t * 2 + j / 3) % 1
                ellipse(c, 420 - j * 30, FLOOR - 260 + q * 80, 9, 13, hexc("#74C0FC"), stroke=False)
    if k > 0:
        c.save(); c.translate(850, FLOOR - 600); c.rotate(0.1); s = back_out(min(1, (1 - k) * 3)); c.scale(S(s), S(s))
        text(c, "knock", 0, 0, 64, hexc("#FFD8A8"), olw=8); c.restore()
    dark_overlay(c, 0.0)


# ---------------- outside: the climb (11–24.7s) ----------------
def stand_on(kind, th=0.0, pizza_dy=0.0):
    x, y = magnet_pos(kind, th, pizza_dy)
    top = {"banana": 14, "star": 40, "pizza": 76}[kind]
    return x, y - top


def pizza_dy(t):
    if t < 14.0:
        return 0.0
    return (FY - 60 - MAGNETS["pizza"][1]) * ease(seg(t, 14.1, 15.5)) ** 1.3


def hop(a, b, p, height=260):
    return lerp(a[0], b[0], p), lerp(a[1], b[1], p) - height * math.sin(math.pi * p)


def door_th(t):
    return 1.15 * ease(seg(t, 22.4, 24.0))


def hang_pose(t):
    """Dill hanging off the handle: hands on the handle, feet braced, leaning back."""
    th = door_th(t)
    _, _, at = door_geom(th)
    hx, hy = at(HANDLE_U, FY - 1330)
    rot = -0.55 + (0.06 * math.sin(t * 22) if t < 22.2 else 0)
    hl = (96, -290)
    dx = hl[0] * math.cos(rot) - hl[1] * math.sin(rot)
    dy = hl[0] * math.sin(rot) + hl[1] * math.cos(rot)
    return hx - dx + 4, hy - dy, rot


def dill_out(t):
    """Dill's pose outside. Returns dict."""
    d = dict(mood="angry", look=(0, 0), arm="down", rot=0.0, sq=1.0, shake=0.0)
    floor = (3360, FY)
    b, s_, p_ = stand_on("banana"), stand_on("star"), stand_on("pizza")
    if t < 11.7:      # glares up at the magnets
        d.update(x=floor[0], y=floor[1], look=(0.4, -1), shake=3, arm="point" if t > 11.3 else "down")
    elif t < 12.4:
        x, y = hop(floor, b, ease_out(seg(t, 11.7, 12.3)), 200)
        d.update(x=x, y=y, arm="reach", mood="angry", look=(0, -1))
    elif t < 13.2:
        x, y = hop(b, s_, ease_out(seg(t, 12.5, 13.1)), 200)
        d.update(x=x, y=y, arm="reach", look=(0, -1))
    elif t < 14.1:
        x, y = hop(s_, p_, ease_out(seg(t, 13.2, 13.8)), 200)
        sq = 1.0
        d.update(x=x, y=y, arm="up" if t > 13.8 else "reach", mood="proud" if t > 13.8 else "angry", look=(1, -0.5))
    elif t < 15.6:    # the pizza slides down with him
        x, y = stand_on("pizza", 0, pizza_dy(t))
        d.update(x=x, y=y, mood="frozen" if t < 14.5 else "shocked", look=(0, 1) if t > 14.5 else (1, 0),
                 arm="up" if t < 14.5 else "down")
    elif t < 16.0:
        x, y = stand_on("pizza", 0, pizza_dy(t))
        d.update(x=x, y=y, mood="frozen", look=(-1, 0.5), arm="down")
    elif t < 16.5:    # off the pizza and again: banana
        x, y = hop(stand_on("pizza", 0, pizza_dy(t)), b, ease_out(seg(t, 16.0, 16.45)), 220)
        d.update(x=x, y=y, arm="reach", look=(0, -1), shake=2)
    elif t < 17.0:
        x, y = hop(b, s_, ease_out(seg(t, 16.55, 16.95)), 200)
        d.update(x=x, y=y, arm="reach", look=(-1, -1), shake=2)
    elif t < 17.7:    # leap for the handle
        hx, hy, rot = hang_pose(t)
        p = ease_out(seg(t, 17.1, 17.6))
        x, y = hop(s_, (hx, hy), p, 160)
        d.update(x=x, y=y, arm="reach", rot=lerp(0, rot, p), look=(-1, -1))
    elif t < 24.0:    # hangs and PULLS. Nothing. Then the door flies open.
        hx, hy, rot = hang_pose(t)
        strain = 6 if t < 22.2 else 2
        mood = "angry" if t < 21.9 else "shocked"
        d.update(x=hx, y=hy, rot=rot, arm="reach", shake=strain, mood=mood, look=(1, -1) if t < 21.9 else (-1, 0))
        if t >= 22.4:   # swinging out with the door
            p = seg(t, 22.4, 24.0)
            d.update(rot=rot - 0.9 * math.sin(math.pi * p) - 0.0, mood="shocked")
    else:             # flung into the fridge, shrinking into the light
        th = door_th(t)
        hx, hy, rot = hang_pose(23.99)
        p = seg(t, 24.0, CUT_IN2)
        x = lerp(hx, FX0 + 360, p); y = lerp(hy, FY - 1150, p) - 300 * math.sin(math.pi * p)
        d.update(x=x, y=y, rot=-p * 3 * math.pi, sq=1.0, mood="shocked", arm="reach", scale=lerp(1, 0.45, p))
    return d


def outside_cam(t, st):
    if t < 11.7:
        k = ease(seg(t, 11.0, 11.7))
        return 3450, lerp(FY - 900, FY - 700, k), lerp(0.82, 0.95, k)
    if t < 17.7:
        cy = clampv(st["y"] - 260, FY - 1550, FY - 560)
        return clampv(st["x"] - 40, 3380, 3640), cy, 1.18
    if t < 21.6:
        k = ease(seg(t, 17.7, 18.4))
        return lerp(3380, 3270, k), lerp(clampv(stand_on("star")[1] - 260, FY - 1550, FY - 560), FY - 1330, k), lerp(1.18, 1.3, k)
    k = ease(seg(t, 21.6, 22.4))
    return lerp(3270, 3420, k), lerp(FY - 1330, FY - 1380, k), lerp(1.3, 0.95, k)


def clampv(v, a, b):
    return max(a, min(b, v))


def outside(c, t):
    st = dill_out(t)
    cx, cy, Z = outside_cam(t, st)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    random.seed(int(t * 30))
    for t0, amp in ((15.5, 16), (24.0, 14)):
        if t0 <= t < t0 + 0.35:
            kk = 1 - seg(t, t0, t0 + 0.35)
            c.translate(random.uniform(-amp, amp) * kk, random.uniform(-amp, amp) * kk)
    kitchen_bg(c)
    th = door_th(t)
    fridge_door(c, th, pizza_dy(t))
    # the Duck? No. Just magnets.
    sc = st.pop("scale", 1.0)
    c.save(); c.translate(st["x"], st["y"]); c.scale(sc, sc)
    dill(c, 0, 0, st["mood"], look=st["look"], arm=st["arm"], crown_on=False, rot=st["rot"], shake=st["shake"], sq=st["sq"])
    c.restore()
    # effort: sweat + straining lines while hanging
    if 18.0 <= t < 22.0:
        for j in range(3):
            q = (t * 2.2 + j / 3) % 1
            ellipse(c, st["x"] - 90 + j * 40, st["y"] - 320 + q * 120, 9, 13, hexc("#74C0FC"), stroke=False)
        if int(t * 3) % 2 == 0:
            c.save(); c.translate(st["x"] - 200, st["y"] - 420); c.rotate(-0.2)
            text(c, "HNNNG", 0, 0, 70, hexc("#FF6B6B"), olw=9); c.restore()
    # sad trombone moment: a little rain cloud of shame
    if 15.5 <= t < 16.0:
        s = back_out(seg(t, 15.5, 15.7))
        c.save(); c.translate(st["x"], st["y"] - 420); c.scale(S(s), S(s))
        ellipse(c, -40, 0, 70, 46, hexc("#ADB5BD"), lw=5); ellipse(c, 40, -6, 70, 52, hexc("#ADB5BD"), lw=5)
        c.restore()
    # the Hand arrives, grabs the door's top edge, and swings it open
    if 21.6 <= t < CUT_IN2:
        _, _, at = door_geom(th)
        gx, gy = at(HANDLE_U, HANDLE_Y0 + 60)
        tip = lerp(gy - 1800, gy + 120, ease(seg(t, 21.6, 22.3)))
        hand(c, gx - 10, tip, ease(seg(t, 22.2, 22.4)))
    if 15.5 <= t < 16.1:
        s = back_out(seg(t, 15.5, 15.7))
        c.save(); c.translate(st["x"] - 260, FY - 200); c.rotate(-0.1); c.scale(S(s), S(s))
        text(c, "clunk.", 0, 0, 80, hexc("#CED4DA"), olw=9); c.restore()


# ---------------- inside: wrecking ball, yolk, hug, the reveal (24.7–38s) ----------------
def light_in(t):
    if t < 32.9:
        return 1.0
    return 1 - ease(seg(t, 32.9, 33.4))


EGG_FLY = []
_r = random.Random(4)
for i in range(6):
    EGG_FLY.append((_r.uniform(-900, 700), _r.uniform(-1200, -500), _r.uniform(-12, 12)))

HIT = 25.15


def inside_end(c, t):
    L = light_in(t)
    # camera
    if t < 28.6:
        cx, cy, Z = 660, FLOOR - 300, 1.6
    elif t < 33.6:
        k = ease(seg(t, 28.6, 29.3))
        cx, cy, Z = 690, lerp(FLOOR - 300, FLOOR - 260, k), lerp(1.6, 1.85, k)
    else:
        k = ease(seg(t, 34.0, 37.3))
        cx, cy, Z = lerp(690, 520, k), lerp(FLOOR - 260, FLOOR - 190, k), lerp(1.85, 1.9, k)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    random.seed(int(t * 30))
    if HIT <= t < HIT + 0.4:
        kk = 1 - seg(t, HIT, HIT + 0.4)
        c.translate(random.uniform(-26, 26) * kk, random.uniform(-26, 26) * kk)
    fridge_bg(c, L)

    # the Duck, in Dill's throne spot (it was not there a moment ago)
    if t >= 33.3:
        duck(c, 420, FLOOR, turn=ease(seg(t, 36.3, 37.0)), s=1.0)

    # egg wall: intact until Dill hits it
    if t < HIT:
        egg_wall(c, t, 6, wob=0.2)
    else:
        p = seg(t, HIT, HIT + 1.2)
        for i, (vx, vy, vr) in enumerate(EGG_FLY):
            x0, y0 = wall_pos(i)
            if p < 1:
                x = x0 + vx * p; y = y0 + vy * p + 1900 * p * p
                shell(c, x - 30, y - 70, 0.9, vr * p, True)
                shell(c, x + 30, y - 40, 0.9, -vr * p, False)
        # yolk puddle
        s = ease_out(seg(t, HIT, HIT + 0.5))
        c.save(); c.translate(720, FLOOR + 4); c.scale(S(s), S(s))
        ellipse(c, 0, 0, 260, 30, WHITE, lw=5)
        for j, (dx, r) in enumerate([(-130, 30), (120, 28)]):
            yolk_blob(c, dx, -6, r, 70 + j)
        c.restore()
        # yolk splats flying
        if t < HIT + 0.9:
            q = seg(t, HIT, HIT + 0.9)
            for j in range(7):
                a = -math.pi * (0.05 + 0.9 * j / 6)
                yolk_blob(c, 760 + math.cos(a) * 420 * q, FLOOR - 250 + math.sin(a) * 300 * q + 500 * q * q, 22 * (1 - 0.4 * q), 90 + j)

    # Crumb (hiding with the spear until the crash)
    DXF, CXF = 790, 600
    if t < HIT + 0.05:
        crumb(c, 500, FLOOR, "scared", look=(1, 0), crown_on=True, shake=3, bow=-0.1)
        toothpick_spear(c, 560, FLOOR - 90, -0.35)
    elif t < 26.6:   # bowled over: flat on his back
        p = ease_out(seg(t, HIT, HIT + 0.4))
        crumb(c, lerp(500, CXF - 40, p), FLOOR, "dizzy", rot=p * math.pi / 2, crown_on=True)
    else:
        if t < 27.1:
            r = math.pi / 2 * (1 - ease(seg(t, 26.6, 27.1))); mood = "dizzy"
        elif t < 28.6:
            r = 0; mood = "dizzy" if t < 27.8 else "sheepish"
        else:
            r = 0.12 * ease(seg(t, 28.6, 29.0)); mood = "sheepish"
        hug = ease(seg(t, 28.6, 29.0)) * (1 - ease(seg(t, 30.4, 30.8)))
        crown_on = t < 30.8
        crumb(c, CXF + 35 * hug, FLOOR, mood, look=(1, 0), rot=r, crown_on=crown_on,
              arm="wave" if 30.8 <= t < 31.9 else "down")
        goo(c, CXF + 35 * hug, FLOOR, t, 3, h=95, n=4, top=285)

    # Dill: flies in from the right like a wrecking ball
    if t < HIT:
        p = seg(t, CUT_IN2, HIT)
        x = lerp(1250, 830, p); y = FLOOR - 330 + 120 * p
        dill(c, x, y, "shocked", look=(-1, 0), arm="reach", crown_on=False, rot=-0.9 - p * 2.5)
        c.set_source_rgba(1, 1, 1, 0.7); c.set_line_width(8)
        for j in range(4):
            c.move_to(x + 120, y - 60 - j * 70); c.line_to(x + 340, y - 40 - j * 70); c.stroke()
    elif t < 26.4:   # tumble to a stop
        p = seg(t, HIT, 26.2)
        x = lerp(700, DXF, ease_out(p)); y = FLOOR - 240 * math.sin(math.pi * min(1, p * 1.3))
        dill(c, x, y if p < 0.77 else FLOOR, "shocked", crown_on=False, rot=-p * 2 * math.pi * 1.0 if p < 0.77 else 0)
    else:
        hug = ease(seg(t, 28.6, 29.0)) * (1 - ease(seg(t, 30.4, 30.8)))
        has_crown = t >= 32.0
        if t < 27.8:
            mood, look, arm = "frozen", (-1, 0), "down"
        elif t < 28.6:
            mood, look, arm = "shocked", (-1, 0.3), "down"
        elif t < 30.8:
            mood, look, arm = "smug", (-1, 0), "down"
        elif t < 32.0:
            mood, look, arm = "proud", (0, -1), "down"
        elif t < 33.6:
            mood, look, arm = "proud", (0.3, -0.6), "up"
        elif t < 34.6:
            mood, look, arm = "proud", lerp(0.3, -1, ease(seg(t, 33.8, 34.3))), "down"
            look = (look, 0)
        else:
            mood, look, arm = "shocked", (-1, 0.2), "down"
        puff = 1.0 + 0.05 * ease(seg(t, 32.0, 32.4))
        rot = -0.12 * hug
        dill(c, DXF - 35 * hug, FLOOR, mood, look=look, arm=arm, crown_on=has_crown, rot=rot, sq=puff,
             shake=3 if t >= 34.6 else 0)
        goo(c, DXF - 35 * hug, FLOOR, t, 7, h=115, n=4, top=292)
        # crown: lifted off Crumb's head and handed up to Dill
        if 30.8 <= t < 32.0:
            p = ease(seg(t, 30.8, 31.9))
            x = lerp(CXF - 6, DXF + 4, p); y = lerp(FLOOR - 292, FLOOR - 280 * puff, p) - 160 * math.sin(math.pi * p)
            crown(c, x, y, lerp(0.9, 1.0, p), lerp(-0.15, 0.08, p))
        if 32.0 <= t < 32.8:   # sparkle of dignity
            s = back_out(seg(t, 32.0, 32.25)) * (1 - seg(t, 32.5, 32.8))
            for j in range(5):
                a = -math.pi / 2 + (j - 2) * 0.45
                star(c, DXF + 4 + math.cos(a) * 140 * s, FLOOR - 350 + math.sin(a) * 110 * s, 22 * s, t * 3, GOLD)
        # hearts during the hug
        if 28.8 <= t < 30.9:
            for j in range(4):
                q = ((t - 28.8) * 0.9 + j / 4) % 1
                heart(c, 695 + 60 * math.sin(j * 2 + q * 5), FLOOR - 380 - q * 260, 1.6, 1 - q)

    # sound-effect words
    if HIT <= t < HIT + 0.9:
        s = back_out(seg(t, HIT, HIT + 0.2))
        c.save(); c.translate(760, FLOOR - 560); c.rotate(-0.12); c.scale(S(s * 1.1), S(s * 1.1))
        text(c, "CRACK!", 0, 0, 120, (1, 1, 1), olw=12); c.restore()
    if HIT + 0.5 <= t < HIT + 1.5:
        s = back_out(seg(t, HIT + 0.5, HIT + 0.7))
        c.save(); c.translate(560, FLOOR - 470); c.rotate(0.1); c.scale(S(s), S(s))
        text(c, "SPLAT!", 0, 0, 110, YOLK, olw=12); c.restore()
    if t >= 34.6:   # "!" over Dill
        s = back_out(seg(t, 34.6, 34.8))
        c.save(); c.translate(DXF - 10, FLOOR - 450); c.scale(S(s), S(s))
        text(c, "!", 0, 0, 150, (1, 0.3, 0.3), olw=12); c.restore()
    dark_overlay(c, L)
    if 24.7 <= t < 25.0:   # white flash as the door light floods in
        c.save(); c.identity_matrix(); c.rectangle(0, 0, W, H)
        c.set_source_rgba(1, 1, 1, 0.8 * (1 - seg(t, 24.7, 25.0))); c.fill(); c.restore()


def frame(c, t):
    if t >= END_T:
        end_card(c, t, END_T); return
    if t < CUT_IN:
        split_screen(c, t)
    elif t < CUT_OUT:
        c.save(); inside_eggs(c, t); c.restore()
    elif t < CUT_IN2:
        c.save(); outside(c, t); c.restore()
        if t >= 24.3:   # light floods the frame as Dill vanishes inside
            c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.9 * seg(t, 24.3, CUT_IN2)); c.fill()
    else:
        c.save(); inside_end(c, t); c.restore()
        if t >= END_T - 0.4:
            iris(c, 360, 1150, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))
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
