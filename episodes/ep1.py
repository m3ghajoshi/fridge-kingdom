"""FRIDGE KINGDOM — Episode 1: "The Hand". 31s wordless cartoon, 1080x1920 @ 30fps."""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from animate import ellipse, rrect, star, text, iris, hexc, clamp, seg, ease, ease_out, lerp, back_out, INK

W, H, FPS, DUR = 1080, 1920, 30, 31.0
FLOOR = 1450      # bottom shelf surface
TOP = 720         # top shelf surface
GREEN, GREEN_L, GREEN_D = hexc("#7BC043"), hexc("#A8DC70"), hexc("#558B2F")
CRUST, BREAD = hexc("#C27C3E"), hexc("#F6D9A3")
GOLD = hexc("#FFC933")


def S(v):
    return v if abs(v) > 1e-3 else (1e-3 if v >= 0 else -1e-3)


# ---------------- characters ----------------
def crown(c, x, y, s=1.0, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(S(s), S(s))
    c.move_to(-48, 0); c.line_to(-52, -52); c.line_to(-26, -24); c.line_to(0, -64)
    c.line_to(26, -24); c.line_to(52, -52); c.line_to(48, 0); c.close_path()
    c.set_source_rgb(*GOLD); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    for gx, col in [(-24, "#FF4D6D"), (0, "#4DABF7"), (24, "#69DB7C")]:
        ellipse(c, gx, -12, 7, 7, hexc(col), lw=3)
    c.restore()


def dill(c, x, y, mood="proud", look=(0, 0), arm="down", crown_on=True, rot=0.0, shake=0.0, sq=1.0):
    c.save(); c.translate(x + shake * random.uniform(-1, 1), y); c.rotate(rot); c.scale(1 / S(sq) ** 0.5, sq)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    # legs
    c.set_source_rgb(*INK); c.set_line_width(10)
    c.move_to(-26, -30); c.line_to(-32, -2); c.move_to(26, -30); c.line_to(32, -2); c.stroke()
    ellipse(c, -40, -4, 20, 9, INK, stroke=False); ellipse(c, 40, -4, 20, 9, INK, stroke=False)
    # body
    ellipse(c, 0, -155, 74, 132, GREEN, lw=7)
    ellipse(c, -30, -175, 16, 72, GREEN_L, stroke=False)
    for bx, by in [(40, -90), (-44, -110), (30, -250), (50, -170), (-10, -60), (-50, -200), (12, -128)]:
        ellipse(c, bx, by, 7, 9, GREEN_D, stroke=False)
    # angry red flush
    if mood == "angry":
        c.save(); c.translate(0, -155); c.scale(74, 132); c.arc(0, 0, 0.95, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(1, 0.2, 0.15, 0.25 + 0.1 * math.sin(shake * 50)); c.fill()
    # eyes (mismatched on purpose)
    lx, ly = look
    for ex, ey, r in [(-28, -205, 24), (30, -212, 34)]:
        big = 1.25 if mood in ("frozen", "shocked") else 1.0
        ellipse(c, ex, ey, r * big, r * big, (1, 1, 1), lw=5)
        pr = r * (0.22 if mood in ("frozen", "shocked") else 0.45 if mood != "angry" else 0.3)
        ellipse(c, ex + lx * r * 0.4, ey + ly * r * 0.4, pr, pr, INK, stroke=False)
        if mood == "angry":
            c.set_source_rgb(0.85, 0.1, 0.1); c.set_line_width(2.5)
            for a in (0.3, 2.6, 4.1):
                c.move_to(ex + r * 0.9 * math.cos(a), ey + r * 0.9 * math.sin(a))
                c.line_to(ex + r * 0.5 * math.cos(a + 0.3), ey + r * 0.5 * math.sin(a + 0.3)); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(8)
    if mood == "angry":
        c.move_to(-54, -244); c.line_to(-6, -226); c.move_to(70, -258); c.line_to(10, -232); c.stroke()
    elif mood == "proud":
        c.move_to(-50, -240); c.line_to(-8, -246); c.move_to(4, -258); c.line_to(62, -262); c.stroke()
    elif mood == "sad":   # Ep 6: brows tilted up in the middle
        c.move_to(-54, -226); c.line_to(-12, -244); c.move_to(70, -240); c.line_to(14, -262); c.stroke()
    # mouth
    c.set_line_width(6)
    if mood == "proud":
        c.move_to(-36, -150); c.curve_to(-20, -112, 30, -110, 48, -152); c.close_path()
        c.set_source_rgb(*hexc("#7A1F2B")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
        c.rectangle(-8, -146, 18, 14); c.set_source_rgb(1, 1, 1); c.fill()
    elif mood == "frozen":
        c.move_to(-26, -138); c.line_to(34, -138); c.stroke()
    elif mood == "shocked":
        ellipse(c, 4, -130, 18, 24, hexc("#7A1F2B"), lw=5)
    elif mood == "angry":
        c.move_to(-36, -128); c.line_to(44, -128); c.line_to(44, -146); c.line_to(-36, -146); c.close_path()
        c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
        for tx in (-16, 4, 24):
            c.move_to(tx, -146); c.line_to(tx, -128); c.stroke()
    elif mood == "smug":
        c.move_to(-30, -140); c.curve_to(-10, -124, 20, -126, 46, -148); c.stroke()
    elif mood == "sad":
        c.move_to(-28, -122); c.curve_to(-10, -146, 22, -146, 40, -120); c.stroke()
    # arms
    c.set_source_rgb(*INK); c.set_line_width(10)
    if arm == "reach":   # both arms straight up, empty-handed (climbing / hanging)
        c.move_to(-60, -170); c.line_to(-96, -290)
    elif arm in ("point_l", "flail"):   # left arm pointing left (Ep 5); "flail": left up, right out
        if arm == "point_l":
            c.move_to(-70, -160); c.line_to(-140, -175)
        else:
            c.move_to(-60, -170); c.line_to(-110, -270)
    else:
        c.move_to(-70, -150); c.line_to(-112, -100)
    if arm == "reach":
        c.move_to(60, -170); c.line_to(96, -290)
    elif arm == "pound":  # fist thrust forward (knocking)
        c.move_to(70, -160); c.line_to(150, -190)
    elif arm == "up":
        c.move_to(70, -160); c.line_to(118, -250)
    elif arm in ("point", "flail"):
        c.move_to(70, -160); c.line_to(140, -175)
    else:
        c.move_to(70, -150); c.line_to(112, -100)
    c.stroke()
    if arm == "pound":
        ellipse(c, 156, -192, 16, 16, GREEN, lw=4)
    if arm == "up":  # toothpick sword
        c.set_source_rgb(*hexc("#E9C98B")); c.set_line_width(9)
        c.move_to(110, -230); c.line_to(150, -380); c.stroke()
        c.set_source_rgb(*hexc("#FF4D6D")); c.move_to(132, -312); c.line_to(178, -330); c.line_to(144, -350); c.close_path(); c.fill()
    if crown_on:
        crown(c, 4, -280, 1.0, 0.08)
    c.restore()


def crumb(c, x, y, mood="worried", look=(0, 0), arm="down", rot=0.0, shake=0.0, crown_on=False, bow=0.0):
    c.save(); c.translate(x + shake * random.uniform(-1, 1), y); c.rotate(rot)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_source_rgb(*INK); c.set_line_width(9)
    c.move_to(-28, -20); c.line_to(-32, -2); c.move_to(28, -20); c.line_to(32, -2); c.stroke()
    ellipse(c, -40, -4, 17, 8, INK, stroke=False); ellipse(c, 40, -4, 17, 8, INK, stroke=False)
    c.translate(0, -20); c.rotate(bow); c.translate(0, 20)

    def toast_path(k):
        c.save(); c.translate(0, -130); c.scale(k, k); c.translate(0, 130)
        c.move_to(-72, -20); c.line_to(-72, -175)
        c.curve_to(-118, -200, -100, -290, -34, -276)
        c.curve_to(-14, -306, 14, -306, 34, -276)
        c.curve_to(100, -290, 118, -200, 72, -175)
        c.line_to(72, -20); c.close_path(); c.restore()
    toast_path(1.0); c.set_source_rgb(*CRUST); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(7); c.stroke()
    toast_path(0.8); c.set_source_rgb(*BREAD); c.fill()
    ellipse(c, 38, -70, 20, 13, hexc("#E64980"), stroke=False)   # jelly smudge
    ellipse(c, 30, -78, 6, 4, hexc("#FF8FB8"), stroke=False)
    lx, ly = look
    if mood == "dizzy":
        for ex in (-26, 26):
            c.save(); c.translate(ex, -160); c.move_to(0, 0)
            for i in range(50):
                a = i * 0.4; r = i * 0.36; c.line_to(r * math.cos(a), r * math.sin(a))
            c.set_source_rgb(*INK); c.set_line_width(4); c.stroke(); c.restore()
    else:
        big = 1.4 if mood == "scared" else 1.0
        for ex in (-26, 26):
            ellipse(c, ex, -160, 17 * big, 19 * big, (1, 1, 1), lw=4)
            ellipse(c, ex + lx * 7, -158 + ly * 8, 7, 8, INK, stroke=False)
        c.set_source_rgb(*INK); c.set_line_width(5)
        c.move_to(-44, -196); c.line_to(-12, -186); c.move_to(44, -196); c.line_to(12, -186); c.stroke()
    c.set_source_rgb(*INK); c.set_line_width(5)
    if mood in ("scared", "worried"):
        c.move_to(-24, -112)
        for i in range(1, 7):
            c.line_to(-24 + i * 8, -112 + (6 if i % 2 else -2))
        c.stroke()
    elif mood == "sheepish":
        c.move_to(-20, -116); c.curve_to(-6, -104, 10, -104, 24, -118); c.stroke()
    else:
        c.move_to(-14, -110); c.line_to(16, -110); c.stroke()
    if mood in ("scared", "worried", "sheepish"):
        c.move_to(78, -232); c.curve_to(70, -214, 74, -204, 82, -204); c.curve_to(90, -204, 92, -214, 78, -232)
        c.set_source_rgb(*hexc("#74C0FC")); c.fill()
    c.set_source_rgb(*INK); c.set_line_width(9)
    c.move_to(-70, -120); c.line_to(-104, -76)
    if arm == "wave":
        k = math.sin(random.random() * 0) + 0
        c.move_to(70, -130); c.line_to(112, -210)
    else:
        c.move_to(70, -120); c.line_to(104, -76)
    c.stroke()
    if crown_on:
        crown(c, -6, -292, 0.9, -0.15)
    c.restore()


def duck(c, x, y, turn=0.0, s=1.0):
    c.save(); c.translate(x, y); c.scale(S(s), S(s))
    ellipse(c, 0, -58, 92, 58, hexc("#FFD43B"), lw=7)
    c.move_to(-80, -80); c.line_to(-120, -112); c.line_to(-84, -46); c.close_path()
    c.set_source_rgb(*hexc("#FFD43B")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    ellipse(c, -6, -60, 46, 26, hexc("#FCC419"), stroke=False)
    hx = lerp(40, 4, ease(turn))
    c.save(); c.translate(hx, -142)
    sqx = max(abs(math.cos(math.pi * turn)), 0.55)
    c.scale(1, 1)
    ellipse(c, 0, 0, 54, 52, hexc("#FFD43B"), lw=7)
    if turn < 0.5:
        c.save(); c.scale(sqx, 1)
        c.move_to(40, 8); c.line_to(92, 20); c.line_to(40, 32); c.close_path()
        c.set_source_rgb(*hexc("#FF922B")); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
        ellipse(c, 22, -14, 8, 9, INK, stroke=False)
        c.restore()
    else:
        ellipse(c, 0, 22, 30 * sqx + 6, 14, hexc("#FF922B"), lw=5)
        for ex in (-19, 19):
            ellipse(c, ex * sqx, -10, 11, 13, INK, stroke=False)
            ellipse(c, ex * sqx + 3, -14, 3, 3, (1, 1, 1), stroke=False)
    c.restore(); c.restore()


def hand(c, x, tip_y, grip=0.0, alpha=1.0):
    col = hexc("#3B2F45")
    c.save(); c.translate(x, tip_y)
    rrect(c, -110, -1400, 220, 1180, 70); c.set_source_rgba(*col, alpha); c.fill()
    rrect(c, -150, -300, 300, 220, 90); c.fill()
    for i, fx in enumerate((-120, -60, 0, 60)):
        ln = lerp(170, 90, grip)
        rrect(c, fx - 4, -110, 56, ln, 28); c.fill()
    rrect(c, 120, -260, 60, lerp(170, 110, grip), 30); c.fill()
    c.restore()


def butter_dish(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(S(s), S(s))
    ellipse(c, 0, -10, 150, 26, (0.97, 0.97, 1), lw=6)
    rrect(c, -95, -110, 190, 96, 18); c.set_source_rgb(*hexc("#FFE680")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.set_source_rgba(1, 1, 1, 0.7); rrect(c, -80, -100, 60, 14, 7); c.fill()
    c.restore()


def spoon(c, px, py, ang):
    c.save(); c.translate(px, py); c.rotate(ang)
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    c.set_source_rgb(*INK); c.set_line_width(30); c.move_to(-120, 0); c.line_to(220, 0); c.stroke()
    c.set_source_rgb(*hexc("#CED4DA")); c.set_line_width(20); c.move_to(-120, 0); c.line_to(220, 0); c.stroke()
    ellipse(c, -190, -10, 90, 36, hexc("#CED4DA"), lw=7)
    ellipse(c, -190, -18, 64, 20, hexc("#E9ECEF"), stroke=False)
    c.restore()


def bubble(c, x, y, s, draw_icon):
    if s <= 0.01:
        return
    c.save(); c.translate(x, y); c.scale(S(s), S(s))
    ellipse(c, 0, 0, 120, 92, (1, 1, 1), lw=6)
    c.move_to(-30, 80); c.line_to(-70, 140); c.line_to(10, 88); c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    ellipse(c, -20, 86, 30, 8, (1, 1, 1), stroke=False)
    draw_icon(c)
    c.restore()


# ---------------- set ----------------
def fridge_bg(c, light):
    g = cairo.LinearGradient(0, 0, 0, H)
    g.add_color_stop_rgb(0, *hexc("#3D5285")); g.add_color_stop_rgb(1, *hexc("#24325A"))
    c.rectangle(-100, -100, W + 200, H + 200); c.set_source(g); c.fill()
    if light > 0:
        g2 = cairo.LinearGradient(0, 0, 0, H)
        g2.add_color_stop_rgb(0, *hexc("#F3FAFF")); g2.add_color_stop_rgb(1, *hexc("#BFE0F5"))
        c.rectangle(-100, -100, W + 200, H + 200); c.set_source(g2); c.paint_with_alpha(light)
    dim = lerp(0.6, 1.0, light)
    # back wall vents
    c.set_source_rgba(1, 1, 1, 0.06 + 0.1 * light); c.set_line_width(8)
    for i in range(6):
        c.move_to(150, 140 + i * 40); c.line_to(930, 140 + i * 40); c.stroke()
    # pickle jar on top shelf (the relatives, watching)
    c.save(); c.translate(170, TOP)
    rrect(c, -95, -330, 190, 330, 30); c.set_source_rgba(0.8, 0.95, 0.85, 0.35 + 0.25 * light); c.fill_preserve()
    c.set_source_rgba(*INK, 1); c.set_line_width(6); c.stroke()
    rrect(c, -100, -370, 200, 50, 12); c.set_source_rgb(*[v * dim for v in hexc("#E03131")]); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    for (px, py, rot) in [(-45, -150, 0.1), (5, -170, -0.1), (50, -140, 0.15), (-25, -260, 0.2), (40, -265, -0.1)]:
        c.save(); c.translate(px, py); c.rotate(rot)
        ellipse(c, 0, 0, 26, 70, [v * dim for v in GREEN_D], lw=4)
        ellipse(c, -6, -20, 6, 7, (1, 1, 1), stroke=False); ellipse(c, 8, -20, 6, 7, (1, 1, 1), stroke=False)
        ellipse(c, -6, -19, 3, 3, INK, stroke=False); ellipse(c, 8, -19, 3, 3, INK, stroke=False)
        c.restore()
    c.restore()
    # milk carton bottom-left
    c.save(); c.translate(110, FLOOR)
    c.rectangle(-80, -420, 160, 420); c.set_source_rgb(*[v * dim for v in (0.95, 0.95, 1)]); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.move_to(-80, -420); c.line_to(0, -500); c.line_to(80, -420); c.close_path()
    c.set_source_rgb(*[v * dim for v in hexc("#4DABF7")]); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.rectangle(-80, -300, 160, 110); c.set_source_rgb(*[v * dim for v in hexc("#4DABF7")]); c.fill()
    c.restore()
    # shelves
    for sy in (TOP, FLOOR):
        c.rectangle(-50, sy, W + 100, 34); c.set_source_rgba(0.75, 0.9, 1.0, 0.55 + 0.3 * light); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        c.rectangle(-50, sy + 6, W + 100, 6); c.set_source_rgba(1, 1, 1, 0.6); c.fill()
    # crisper drawer
    rrect(c, 40, FLOOR + 90, 1000, 400, 30); c.set_source_rgba(0.7, 0.85, 1, 0.18 + 0.25 * light); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    if light > 0:  # god rays
        c.save()
        for i in range(5):
            a = -0.5 + i * 0.22
            c.move_to(-100, -200)
            c.line_to(-100 + 2600 * math.cos(a + 0.6), -200 + 2600 * math.sin(a + 0.6))
            c.line_to(-100 + 2600 * math.cos(a + 0.68), -200 + 2600 * math.sin(a + 0.68))
            c.close_path(); c.set_source_rgba(1, 1, 1, 0.13 * light); c.fill()
        c.restore()


def dark_overlay(c, light):
    """Characters also get dim when the fridge is dark."""
    if light < 1:
        c.rectangle(-100, -100, W + 200, H + 200); c.set_source_rgba(0.05, 0.08, 0.2, 0.22 * (1 - light)); c.fill()


def light_at(t):
    if t < 7.0:
        return 0.0
    if t < 11.0:
        return ease(seg(t, 7.0, 7.35))
    return 1 - ease(seg(t, 11.0, 11.25))


# ---------------- title / end cards ----------------
def title_card(c, t):
    g = cairo.RadialGradient(W / 2, 820, 50, W / 2, 820, 1300)
    g.add_color_stop_rgb(0, *hexc("#E7F5FF")); g.add_color_stop_rgb(0.35, *hexc("#74C0FC")); g.add_color_stop_rgb(1, *hexc("#1C2541"))
    c.rectangle(0, 0, W, H); c.set_source(g); c.fill()
    for i, word in enumerate(["FRIDGE", "KINGDOM"]):
        p = back_out(seg(t, 0.1 + i * 0.25, 0.55 + i * 0.25))
        c.save(); c.translate(W / 2, 700 + i * 170 + 8 * math.sin(t * 6 + i)); c.rotate(0.04 * (1 if i else -1))
        c.scale(S(p), S(p)); text(c, word, 0, 0, 170, GOLD if i else (1, 1, 1), olw=22); c.restore()
    crown(c, W / 2 + 190, 560, 1.6 * back_out(seg(t, 0.6, 1.0)), 0.25)
    q = ease_out(seg(t, 1.0, 1.4))
    if q > 0:
        c.save(); c.translate(W / 2, 1050 + (1 - q) * 50)
        text(c, "Episode 1:  The Hand", 0, 0, 64, (1, 1, 1), olw=10); c.restore()
    dill(c, 360, 1640 - abs(math.sin(t * 5)) * 30, "proud", crown_on=True)
    crumb(c, 720, 1640, "worried", look=(-1, 0), shake=3)


def scene(c, t):
    L = light_at(t)
    # camera: zoom on the duck at the end
    z = ease(seg(t, 26.4, 28.8))
    cx, cy, Z = lerp(560, 860, z), lerp(1040, TOP - 150, z), lerp(1.32, 2.7, z)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    if 12.15 <= t < 12.5:  # thud shake
        k = 1 - seg(t, 12.15, 12.5); random.seed(int(t * 90))
        c.translate(random.uniform(-20, 20) * k, random.uniform(-20, 20) * k)
    fridge_bg(c, L)

    # ---- the Duck: always there, never moving (until it does) ----
    duck(c, 860, TOP, turn=ease(seg(t, 26.6, 28.3)))

    random.seed(int(t * 30))
    DX = 420
    # ---- butter dish throne ----
    if t < 9.8:
        butter_dish(c, DX, FLOOR)
    # ---- hand ----
    if 8.1 <= t < 11.2:
        if t < 9.8:
            tip = lerp(-300, FLOOR - 120, ease(seg(t, 8.1, 9.7)))
            grip = 0
        else:
            tip = lerp(FLOOR - 120, -500, ease(seg(t, 10.1, 11.1)))
            grip = ease(seg(t, 9.8, 10.0))
        hand(c, DX + 20, tip, grip)
        if t >= 9.8:
            butter_dish(c, DX, tip + 120 + 40 * grip)

    # ---- Dill ----
    if t < 2.4:
        pass
    elif t < 7.0:
        wav = math.sin(t * 6)
        dill(c, DX, FLOOR - 110, "proud", look=(0.6, -0.2), arm="up" if (t % 1.6) < 1.1 else "down", rot=0.05 * wav)
    elif t < 11.4:
        dill(c, DX, FLOOR - 110, "frozen", arm="up")
    elif t < 11.8:
        dill(c, DX, FLOOR - 110, "shocked", look=(0, 1), arm="up")
    elif t < 13.3:
        p = seg(t, 11.8, 12.15)
        y = lerp(FLOOR - 110, FLOOR, p * p)
        flat = p >= 1
        dill(c, DX if not flat else DX - 20, y if not flat else FLOOR - 4, "shocked" if not flat else "frozen",
             arm="up" if not flat else "down", crown_on=False, rot=0 if not flat else -math.pi / 2,
             sq=1 if not flat else 1.0)
    elif t < 14.2:
        p = ease(seg(t, 13.3, 13.8))
        dill(c, DX, FLOOR, "frozen", look=(1, 0), crown_on=False, rot=lerp(-math.pi / 2, 0, p))
    elif t < 18.0:
        sh = 6 + 6 * seg(t, 14.2, 17.6)
        dill(c, DX, FLOOR, "angry", arm="up" if t > 14.6 else "down", crown_on=False, shake=sh)
        if t > 14.5:  # steam
            for k in range(3):
                q = ((t - 14.5) * 1.6 + k / 3) % 1
                ellipse(c, DX - 50 + k * 50 + 20 * math.sin(q * 6), FLOOR - 300 - q * 220, 26 + 30 * q, 22 + 24 * q,
                        (1, 1, 1), stroke=False)
        def war_icon(cc):
            cc.save(); cc.scale(120, 92); cc.arc(0, 0, 0.9, 0, 2 * math.pi); cc.restore(); cc.clip()
            cc.save(); cc.scale(0.32, 0.32); cc.translate(0, 230); hand(cc, 0, 0, 0.0); cc.restore()
            cc.set_source_rgb(0.9, 0.1, 0.15); cc.set_line_width(16); cc.set_line_cap(cairo.LINE_CAP_ROUND)
            cc.move_to(-60, -50); cc.line_to(60, 50); cc.move_to(60, -50); cc.line_to(-60, 50); cc.stroke()
        bubble(c, DX + 230, FLOOR - 560, back_out(seg(t, 15.2, 15.5)) * (1 - seg(t, 17.3, 17.6)), war_icon)

    # ---- Crumb ----
    CX = 760
    if 2.4 <= t < 7.0:
        bow = 0.35 * max(0, math.sin((t - 2.4) * 4.2))
        crumb(c, CX, FLOOR, "worried", look=(-1, 0), bow=-bow)
        bubble(c, CX + 60, FLOOR - 470, back_out(seg(t, 4.6, 4.9)) * (1 - seg(t, 6.3, 6.6)),
               lambda cc: text(cc, "?", 0, 40, 130, hexc("#4DABF7"), olw=10))
    elif t < 12.2:
        crumb(c, CX, FLOOR, "scared", bow=-0.3 if t < 11.4 else 0)
    elif t < 18.0:
        crown_on = t >= 12.95
        if t < 13.0:
            mood, look = "scared", (-1, -1)
        elif t < 14.2:
            mood, look = "sheepish", ((0, -1) if t < 13.6 else (-1, 0))
        else:
            mood, look = "scared", (-1, 0)
        crumb(c, CX, FLOOR, mood, look=look, crown_on=crown_on, shake=4 if t > 14.2 else 0)
        if t < 12.95:  # crown flies from Dill to Crumb
            p = seg(t, 12.15, 12.95)
            x = lerp(DX - 60, CX - 6, p); y = lerp(FLOOR - 120, FLOOR - 292, p) - 380 * math.sin(math.pi * p)
            crown(c, x, y, 0.95, p * 12)

    # ---- catapult act ----
    if t >= 18.0:
        PX, PY = 600, FLOOR - 55
        # fulcrum: little matchbox
        rrect(c, PX - 55, PY - 5, 110, 60, 8); c.set_source_rgb(*hexc("#FF6B6B")); c.fill_preserve()
        c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
        launch = ease_out(seg(t, 20.25, 20.45))
        ang = lerp(-0.32, 0.42, launch)
        spoon(c, PX, PY - 10, ang)
        # Dill: walks to end of spoon, jumps on it
        if t < 19.6:
            dill(c, lerp(900, 860, seg(t, 18.0, 19.0)), FLOOR, "angry", arm="point", crown_on=False, shake=3)
        elif t < 20.25:
            p = seg(t, 19.6, 20.25)
            dill(c, lerp(860, 800, p), FLOOR - 260 * math.sin(math.pi * p * 0.9) - 40 * p, "angry", crown_on=False)
        else:
            has_crown = t >= 21.2
            dill(c, 800, FLOOR - 55 - 80, "smug" if t > 21.3 else "angry", crown_on=has_crown, arm="up" if t > 21.4 else "down")
            if t < 21.2:  # crown flies back to Dill
                p = seg(t, 20.4, 21.2)
                x = lerp(PX - 190, 804, p); y = lerp(FLOOR - 380, FLOOR - 415, p) - 500 * math.sin(math.pi * p)
                crown(c, x, y, 0.95, -p * 14)
        # Crumb in the spoon -> flies to top shelf
        bx = PX - 190 * math.cos(-0.32); by = PY - 10 - 190 * math.sin(0.32) - 20
        if t < 20.3:
            crumb(c, bx, by + 30, "scared", look=(1, 0), crown_on=True, shake=5)
        elif t < 22.0:
            p = seg(t, 20.3, 22.0)
            x = lerp(bx, 640, p); y = lerp(by, TOP, p) - 900 * math.sin(math.pi * p) * (1 - 0.35 * p)
            crumb(c, x, y, "scared", rot=p * 4 * math.pi, crown_on=False)
            if p < 0.4:
                c.set_source_rgba(1, 1, 1, 0.6); c.set_line_width(6)
                for k in range(3):
                    c.move_to(x - 40 + k * 40, y + 60); c.line_to(x - 80 + k * 40, y + 180); c.stroke()

    if t >= 22.0:
        if t < 23.0:
            rot = lerp(math.pi / 2, 0, ease(seg(t, 22.4, 23.0)))
            crumb(c, 640, TOP, "dizzy", rot=rot)
            if t < 22.4:
                s = 1 - seg(t, 22.0, 22.4)
                for k in range(8):
                    a = k * math.pi / 4
                    ellipse(c, 640 + 130 * (1 - s) * math.cos(a), TOP - 40 + 50 * (1 - s) * math.sin(a), 12 * s + 1, 8 * s + 1, BREAD, stroke=False)
        elif t < 23.8:
            crumb(c, 640, TOP, "dizzy")
            for k in range(3):
                a = t * 5 + k * 2.1
                star(c, 640 + 100 * math.cos(a), TOP - 330 + 24 * math.sin(a), 22, t * 3)
        elif t < 25.5:
            crumb(c, 640, TOP, "worried" if t < 24.2 else "neutral", look=(1, 0),
                  arm="wave" if 24.2 <= t < 25.2 and int(t * 6) % 2 == 0 else "down")
        elif t < 26.5:
            crumb(c, 640, TOP, "scared", look=(0, 0.3))
        else:
            crumb(c, 640, TOP, "scared", look=(1, 0), shake=3)

    dark_overlay(c, L)


def end_card(c, t):
    c.rectangle(0, 0, W, H); c.set_source_rgb(0.06, 0.05, 0.1); c.fill()
    p = back_out(seg(t, 29.25, 29.6))
    c.save(); c.translate(W / 2, H / 2 - 40); c.scale(S(p), S(p)); c.rotate(0.02 * math.sin(t * 20))
    text(c, "TO BE", 0, -70, 130, GOLD, olw=14)
    text(c, "CONTINUED...", 0, 80, 120, GOLD, olw=14)
    c.restore()
    if t > 30.1:
        duck(c, W / 2, H / 2 + 420, turn=1.0, s=0.7 * back_out(seg(t, 30.1, 30.35)))


def frame(c, t):
    if t < 2.4:
        title_card(c, t)
        if t > 2.1:
            iris(c, W / 2, H / 2, lerp(1200, 0, ease(seg(t, 2.1, 2.4))))
        return
    if t >= 29.2:
        end_card(c, t); return
    c.save(); scene(c, t); c.restore()
    if t < 2.8:
        iris(c, 560, 1250, lerp(0, 1400, ease(seg(t, 2.4, 2.8))))
    if t >= 28.8:
        iris(c, W / 2, H / 2, lerp(900, 0, ease(seg(t, 28.8, 29.2))))


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
