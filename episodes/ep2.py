"""FRIDGE KINGDOM — Episode 2: "Operation Butter". 38s, 1080x1920 @ 30fps."""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from ep1 import (dill, crumb, duck, hand, crown, bubble, fridge_bg, dark_overlay, ellipse, rrect, star, text,
                 iris, hexc, seg, ease, ease_out, lerp, back_out, INK, GOLD, FLOOR, TOP, W, H, FPS, S, BREAD)

DUR = 38.0


def jello(c, x, y, wob=0.0):
    c.save(); c.translate(x, y)
    sx, sy = 1 + 0.12 * wob, 1 - 0.12 * wob
    c.scale(sx, sy)
    c.move_to(-90, 0); c.line_to(-70, -150); c.line_to(70, -150); c.line_to(90, 0); c.close_path()
    c.set_source_rgba(*hexc("#FF6B9A"), 0.85); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    ellipse(c, 0, -150, 70, 16, hexc("#FF8FB3"), lw=5)
    c.set_source_rgba(1, 1, 1, 0.5); rrect(c, -55, -125, 16, 90, 8); c.fill()
    c.restore()


def cheese(c, x, y, s=1.0):
    c.save(); c.translate(x, y); c.scale(S(s), S(s))
    rrect(c, -70, -36, 140, 26, 6); c.set_source_rgb(*hexc("#868E96")); c.fill_preserve()  # bottle cap
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    rrect(c, -95, -70, 190, 36, 6); c.set_source_rgb(*hexc("#FFD43B")); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    for hx, hy, r in [(-50, -54, 9), (10, -50, 7), (55, -58, 10)]:
        ellipse(c, hx, hy, r, r * 0.8, hexc("#F59F00"), stroke=False)
    c.restore()


def grape(c, x, y, s=1.0):
    if s < 0.02: return
    ellipse(c, x, y, 26 * s, 28 * s, hexc("#9C36B5"), lw=5)
    ellipse(c, x - 8 * s, y - 10 * s, 6 * s, 5 * s, (1, 1, 1), stroke=False)
    c.set_source_rgb(*hexc("#5C940D")); c.set_line_width(6); c.move_to(x, y - 26 * s); c.line_to(x + 6 * s, y - 42 * s); c.stroke()


def napkin(c, x, y, unroll):
    if unroll <= 0.01:
        return
    w = 420 * unroll
    c.save(); c.translate(x, y); c.rotate(-0.04)
    rrect(c, -w / 2, -150, w, 300, 14); c.set_source_rgb(1, 1, 1); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.rectangle(-w / 2, -150, w, 300); c.clip()
    # crayon battle plan
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(9)
    c.set_source_rgb(*hexc("#5C3B6B"))   # the Hand, stick-figure style
    c.move_to(-150, -130); c.line_to(-150, -40)
    for k in range(4):
        c.move_to(-150, -40); c.line_to(-175 + k * 16, -5)
    c.stroke()
    c.set_source_rgb(*hexc("#F59F00")); rrect(c, -20, 10, 90, 30, 4); c.fill()   # cheese throne
    c.set_source_rgb(*hexc("#E03131")); c.set_line_width(12)   # big X
    c.move_to(-190, -130); c.line_to(-110, -20); c.move_to(-110, -130); c.line_to(-190, -20); c.stroke()
    c.set_source_rgb(*hexc("#2F9E44")); c.set_line_width(8)    # arrow to Dill doodle
    c.move_to(70, 25); c.curve_to(110, -40, 140, -60, 150, -100); c.stroke()
    ellipse(c, 150, -110, 18, 32, hexc("#7BC043"), lw=4)
    c.restore()


def carton_front(c):
    c.save(); c.translate(110, FLOOR)
    c.rectangle(-80, -420, 160, 420); c.set_source_rgb(0.95, 0.95, 1); c.fill_preserve()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    c.move_to(-80, -420); c.line_to(0, -500); c.line_to(80, -420); c.close_path()
    c.set_source_rgb(*hexc("#4DABF7")); c.fill_preserve(); c.set_source_rgb(*INK); c.stroke()
    c.rectangle(-80, -300, 160, 110); c.set_source_rgb(*hexc("#4DABF7")); c.fill()
    c.restore()


def light_at(t):
    if t < 21.0:
        return 0.0
    if t < 31.5:
        return ease(seg(t, 21.0, 21.35))
    return 1 - ease(seg(t, 31.5, 31.75))


DX = 430          # decoy position
CROWN_X = 330     # where Dill's crown lands


def scene(c, t):
    L = light_at(t)
    # camera: start on top shelf, drop to the main shelf, ease back for the hand sequence
    top = 1 - ease(seg(t, 6.0, 7.0))
    cx = lerp(560, 700, top); cy = lerp(1040, TOP - 170, top); Z = lerp(1.32, 1.6, top)
    c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    fridge_bg(c, L)
    random.seed(int(t * 30))

    # --- the Duck: turns a little more each time Crumb glances back ---
    if t < 6:
        glances = sum(1 for g in (3.0, 4.2, 5.3) if t >= g)
        turn = 0.18 * glances
    else:
        turn = 0.55 if t < 33 else 1.0
    duck(c, 860, TOP, turn=turn)

    # --- Crumb: sidestepping on the top shelf, then jumping down onto the jello ---
    jx = 760
    if t < 6.0:
        p = seg(t, 2.2, 6.0)
        x = lerp(690, 500, p)
        glancing = any(g <= t < g + 0.45 for g in (3.0, 4.2, 5.3))
        crumb(c, x, TOP, "scared", look=(1, 0) if glancing else (-1, 0), shake=2)
    elif t < 9.0:
        if t < 7.0:  # leap down from top shelf to the jello
            p = seg(t, 6.0, 7.0)
            x = lerp(500, jx, p); y = lerp(TOP, FLOOR - 150, p) - 260 * math.sin(math.pi * p)
            crumb(c, x, y, "scared", rot=p * 2 * math.pi)
        elif t < 8.4:
            b = seg(t, 7.0, 8.4) * 3
            hop = abs(math.sin(math.pi * b)) * 220 * (1 - b / 3.6)
            crumb(c, jx, FLOOR - 150 - hop, "scared", look=(0, -1))
        else:
            p = ease(seg(t, 8.4, 8.9))
            crumb(c, lerp(jx, jx - 120, p), lerp(FLOOR - 150, FLOOR, p) - 80 * math.sin(math.pi * p),
                  "dizzy", rot=lerp(0, -math.pi / 2, p))
    # jello itself
    wob = 0
    if 7.0 <= t < 8.8:
        wob = math.sin((t - 7.0) * 18) * (1 - seg(t, 7.0, 8.8))
    jello(c, jx, FLOOR, wob)

    # --- Dill + plan ---
    if 6.6 <= t < 9.0:
        dill(c, 300, FLOOR, "proud", look=(1, 0), arm="down")
    if 9.0 <= t < 14.0:
        dill(c, 300, FLOOR, "angry" if t < 11 else "proud", look=(1, 0), arm="point" if int(t * 3) % 2 else "up", shake=2)
        napkin(c, 560, FLOOR - 520, ease_out(seg(t, 9.2, 9.9)))
        crumb(c, jx - 120, FLOOR, "worried", look=(-1, -1),
              rot=lerp(-math.pi / 2, 0, ease(seg(t, 9.0, 9.4))), bow=-0.18 * max(0, math.sin(t * 7)))

    # --- building the decoy ---
    if t >= 14.0:
        cheese(c, DX, FLOOR, back_out(seg(t, 14.3, 14.7)))
    if 14.0 <= t < 19.0:
        dill(c, 250, FLOOR, "proud", look=(1, 0), arm="up" if int(t * 4) % 2 else "down")
        if t < 17.2:
            crumb(c, lerp(jx - 120, 640, seg(t, 14.0, 14.5)), FLOOR, "worried", look=(-1, 0))
        else:  # Crumb is placed on the decoy as bait
            p = ease_out(seg(t, 17.2, 17.7))
            crumb(c, lerp(640, DX, p), lerp(FLOOR, FLOOR - 70, p) - 160 * math.sin(math.pi * p), "scared", shake=4)
        if t >= 16.0:
            grape(c, DX + (0 if t >= 17.7 else 140), (FLOOR - 410 if t >= 17.7 else FLOOR - 40),
                  back_out(seg(t, 16.0, 16.3)))
    if t >= 19.0:
        bait_y = FLOOR - 70
        if t < 33.0:
            crumb(c, DX, bait_y, "scared", look=(-1, -1) if t > 24 else (0, -1), shake=5, arm="down")
        else:
            p = ease(seg(t, 33.0, 34.2))
            x = lerp(DX, CROWN_X, p); y = lerp(bait_y, FLOOR, p) - 120 * math.sin(math.pi * p)
            crumb(c, x, y, "sheepish" if t > 34.4 else "worried", look=(0, -1) if t > 34.2 else (-1, 1),
                  arm="wave" if t > 34.2 else "down")
        if t < 33.0:
            grape(c, DX, bait_y - 340, 1.0)

    # --- Dill hides behind the milk carton, then gets grabbed ---
    if 19.0 <= t < 24.6:
        peek = ease_out(seg(t, 19.0, 19.6))
        dill(c, lerp(110, 210, peek), FLOOR, "shocked" if t >= 21 else "smug", look=(1, -0.2))
    if 24.6 <= t < 31.5:
        p = ease(seg(t, 24.9, 29.5))
        dy = lerp(0, 1400, p)
        kick = math.sin(t * 22) * 0.25
        dill(c, 210, FLOOR - dy, "shocked", look=(0, 1), rot=kick, crown_on=(t < 25.0))
    # crown tumbles to the shelf
    if 25.0 <= t:
        if t < 25.9:
            p = seg(t, 25.0, 25.9)
            x = lerp(214, CROWN_X, p); y = lerp(FLOOR - 280, FLOOR, p) - 90 * math.sin(math.pi * p)
            crown(c, x, y, 0.95, p * 10)
        elif t < 34.2:
            crown(c, CROWN_X, FLOOR, 0.95, 0.0)
    carton_front(c)

    # --- the Hand ---
    if 21.6 <= t < 31.0:
        if t < 23.6:
            hx, tip, grip = DX + 20, lerp(-300, FLOOR - 470, ease(seg(t, 21.6, 23.4))), 0
        elif t < 24.9:
            p = ease(seg(t, 23.6, 24.6))
            hx, tip, grip = lerp(DX + 20, 230, p), lerp(FLOOR - 470, FLOOR - 170, p), 0
        else:
            hx, tip = 230, lerp(FLOOR - 170, FLOOR - 1570, ease(seg(t, 24.9, 29.5)))
            grip = ease(seg(t, 24.6, 24.9))
        hand(c, hx, tip, grip)
        if 22.2 <= t < 24.2:  # hand hovers... "?" over the decoy
            bubble(c, DX + 260, FLOOR - 820, back_out(seg(t, 22.4, 22.7)) * (1 - seg(t, 23.8, 24.1)),
                   lambda cc: text(cc, "?", 0, 40, 130, hexc("#FF922B"), olw=10))

    # --- Crumb picks up the crown in the dark ---
    if t >= 33.0:
        p = seg(t, 33.0, 34.2)
        dill_gone = True
    if t >= 34.2:
        crown(c, CROWN_X, FLOOR - 340 - 10 * math.sin(t * 4), 1.0, 0.05 * math.sin(t * 3))

    dark_overlay(c, L)


def overlay_crumb_moves(c, t):
    pass


def title_card(c, t, ep, name):
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
        text(c, f"Episode {ep}:  {name}", 0, 0, 62, (1, 1, 1), olw=10); c.restore()
    dill(c, 360, 1640 - abs(math.sin(t * 5)) * 30, "angry", crown_on=True, arm="up", shake=3)
    crumb(c, 720, 1640, "worried", look=(-1, 0), shake=3)


def end_card(c, t, t0):
    c.rectangle(0, 0, W, H); c.set_source_rgb(0.06, 0.05, 0.1); c.fill()
    p = back_out(seg(t, t0 + 0.05, t0 + 0.4))
    c.save(); c.translate(W / 2, H / 2 - 40); c.scale(S(p), S(p)); c.rotate(0.02 * math.sin(t * 20))
    text(c, "TO BE", 0, -70, 130, GOLD, olw=14); text(c, "CONTINUED...", 0, 80, 120, GOLD, olw=14)
    c.restore()
    if t > t0 + 0.9:
        duck(c, W / 2, H / 2 + 420, turn=1.0, s=0.7 * back_out(seg(t, t0 + 0.9, t0 + 1.15)))


def frame(c, t):
    if t < 2.0:
        title_card(c, t, 2, "Operation Butter")
        if t > 1.7:
            iris(c, W / 2, H / 2, lerp(1200, 0, ease(seg(t, 1.7, 2.0))))
        return
    if t >= 36.0:
        end_card(c, t, 36.0); return
    c.save(); scene(c, t); c.restore()
    if t < 2.4:
        iris(c, W / 2, H / 2, lerp(0, 1400, ease(seg(t, 2.0, 2.4))))
    if t >= 35.6:
        iris(c, W / 2, H * 0.55, lerp(900, 0, ease(seg(t, 35.6, 36.0))))


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
