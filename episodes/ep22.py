"""FRIDGE KINGDOM — Episode 22: "Two Ducks". 40.0s, 1080x1920 @ 30fps.

Variant B (cold open): the first frame is mid-action; the title shows as a banner across the top for the first 2s.

Continues straight from Ep 21: on the dark top shelf, cracks race across the ice block, CRACK! CRACK!, and it bursts.
A pale rubber duck (Squeak) sits in the meltwater, eyes shut, shivering. It shakes off like a wet dog; its bottle-cap
crown flips to tilt the OTHER way (ping). Its eyes snap open (icy glint) and it hops: SQUEAK SQUEAK SQUEAK!
Bottom shelf: Dill (sitting beside the Duck on his throne), Crumb with Peep, and Chip all look up. Dill double-takes.
Chip goes see-through (eep). Squeak hops off the top shelf, BOINGs off the jello and PLONKs onto Dill's head, then hops
over the Duck and lands beside it: two Ducks. Peep's eyes turn to hearts. Dill points at the Duck: nothing (cricket).
Squeak hops onto the Duck's head and pecks Dill's finger (boop; ?!), then hops onto Dill's head and bounces
(SQUEAK x5); Peep copies on Crumb's head. THMP... THMP... THMP: footsteps outside; everyone freezes. Squeaking brings
the Hand! Crumb flings his scarf over Squeak (mmf); Dill pulls the bundle off his head and sits on it: SQUEEEEEAK!
He's launched into the air. Squeak pops out and sits beside the Duck, perfectly still. The door opens (choir); everyone
dives behind the jello. The Hand hovers over the two Ducks: left... right... (tick, tock). The Duck's one motion: it
slides its eyes toward Squeak. The Hand scoops up the Duck (turban and all) and carries it away. The door closes.
Squeak, alone on the throne in the dark, looks at the camera and winks (squeak). DUN DUN DUNNN.
"""
import os
import math, random, subprocess, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import cairo
from animate import heart
from ep1 import (crown, ellipse, rrect, star, text, iris, hexc, seg, ease, ease_out, lerp, back_out, dark_overlay,
                 INK, GOLD, FLOOR, TOP, W, H, FPS, S)
from ep2 import end_card, jello
from ep5 import cap_crown, cricket
from ep6 import fridge6, drawer_front
from ep7 import god_rays, sq_rings
from ep9 import fat_peep, crumb_bitten
from ep10 import ceiling_vent, frost, hand_cuffed
from ep12 import word, hop
from ep13 import ceiling
from ep14 import clean_duck
from ep15 import drop, chip, CHIP_F
from ep16 import keyed, butter_rink, glazed, DISH
from ep17 import NAP_B
from ep18 import draw_dill, rot_at, CHS
from ep17 import cape, cape_tie
from ep20 import BS
from ep21 import block21, mist, splats, jello_glob, scarf_cloth, crumb_arms, COLD_X, JX

DUR = 40.0
END_T = 38.5
DIM = 0.18
FAT = 1.5
ICE_B = hexc("#74C0FC")
ICE_D = hexc("#1971C2")
RED = (1, 0.35, 0.35)
SQ_Y = hexc("#FFF3BF")        # Squeak: frost-bleached butter-cream
SQ_W = hexc("#FFE8A3")
BEAK = hexc("#FF922B")
FROST_RIM = hexc("#A5D8FF")

# ---------------- places ----------------
BLOCK_X = 880                  # ice block on the top shelf (Ep 21)
DUCK_X = DISH                  # the Duck on Dill's throne (420)
DUCK_S = 1.2
SQ_S = 1.05
SQ_HOME = 225                  # Squeak's spot beside the Duck
DI_X = 590                     # Dill (sitting beside the Duck)
CH_X = COLD_X                  # Chip at the cold spot (760)
CR_X = 875                     # Crumb (Peep on his head)
DILL_HEAD = 300                # Dill's feet -> top of his hood
DUCK_HEAD = 1.2 * 158          # the Duck's feet -> top of its cap crown
SIT_LIFT = 70                  # Dill sitting on the scarf bundle

# ---------------- timing ----------------
T_CR1, T_CR2 = 0.45, 1.15
T_SHATTER = 1.85
T_SHAKE = 3.3
T_FLIP = 4.05
T_EYES = 4.7
SQUEAKS_TOP = (5.25, 5.75, 6.25, 6.75)
T_LOOK = 7.2                   # cut to the bottom shelf: everyone looks up
DTAKE = (8.0, 8.4, 8.8, 9.2)   # Dill's double take
T_SEE = 7.9                    # Chip goes see-through
T_JUMP = 9.9
T_BOING = 10.6
T_PLONK = 11.3
T_OFF = 12.0
T_BESIDE = 12.65
T_LOVE = 13.1
T_STAND = 13.9
T_POINT = 14.3
T_CHIRP = 14.7
T_ONDUCK = 15.6                # Squeak hops onto the Duck's head
T_DUCKLAND = 16.05
T_BOOP = 16.35
T_HUH = 16.7
T_TODILL = 17.3
T_DILLLAND = 17.8
BOUNCES = (18.15, 18.75, 19.35, 19.95, 20.55)
STEPS = (21.5, 22.1, 22.7)
T_THROW = 23.3
T_COVER = 23.9
T_GRABB = 25.0
T_SETB = 25.35
T_SIT = 25.6
T_BIGSQ = 26.0
T_POPOUT = 26.15
T_SQHOME = 26.85
T_DLAND2 = 27.0
T_OPEN = 27.7
T_DIVE = 28.0
T_HID = 28.8
T_HDOWN = 28.9
T_HSET = 29.9
TICKS = (30.6, 31.6, 32.6, 33.6)
T_GAZE = 32.3
T_REACH = 34.5
T_GRIP = 35.0
T_LIFT = 35.3
T_GONE = 36.4
T_CLOSE = 36.55
T_GLINT = 36.8
T_WINK = 37.0
DUNS = (37.3, 37.7, 38.1)


def light_at(t):
    if t < T_OPEN:
        return DIM
    if t < T_CLOSE:
        return lerp(DIM, 1.0, ease(seg(t, T_OPEN, T_OPEN + 0.35)))
    return lerp(1.0, DIM, ease(seg(t, T_CLOSE, T_CLOSE + 0.3)))


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
    text(c, "Ep. 22:  Two Ducks", W / 2, 182, 48, (1, 1, 1), olw=8)
    c.restore()


# ---------------- new character: Squeak ----------------
def squeak_duck(c, x, y, s=SQ_S, look=(0, 0), eyes="open", beak=0.0, sq=1.0, rot=0.0, wet=0.0, glint=0.0,
                cap_rot=-0.38, tilt=0.0, t=0.0, shiver=0.0):
    """Squeak, the second rubber duck: frost-bleached butter-cream, chipped beak tip, frost rim on its tail,
    icy-blue glinting eyes, bottle-cap crown tilted to the LEFT. Front-facing; (x, y) = bottom centre.
    eyes: open / shut / wink / wide. beak 0..1 opens it (squeaking). sq squashes about the feet."""
    jx = shiver * math.sin(t * 70) * 4
    c.save(); c.translate(x + jx, y); c.rotate(rot); c.scale(S(s) / S(sq) ** 0.5, S(s) * S(sq))
    # body
    ellipse(c, 0, -58, 92, 58, SQ_Y, lw=7)
    c.move_to(-80, -80); c.line_to(-120, -112); c.line_to(-84, -46); c.close_path()
    c.set_source_rgb(*SQ_Y); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    # frost rim on the tail tip
    c.move_to(-106, -103); c.line_to(-120, -112); c.line_to(-110, -88)
    c.set_source_rgb(*FROST_RIM); c.set_line_width(7); c.stroke()
    ellipse(c, -6, -60, 46, 26, SQ_W, stroke=False)
    # head
    c.save(); c.translate(4, -142); c.rotate(tilt)
    ellipse(c, 0, 0, 54, 52, SQ_Y, lw=7)
    ellipse(c, -26, -24, 11, 6, (1, 1, 1), stroke=False)
    # beak (with a chipped notch on its right tip)
    bo = beak
    if bo > 0.02:
        ellipse(c, 0, 24 + 10 * bo, 34, 12 + 4 * bo, BEAK, lw=5)            # lower beak
        ellipse(c, 0, 22 + 6 * bo, 22, 8 * bo + 2, hexc("#C92A2A"), stroke=False)
    ellipse(c, 0, 18 - 4 * bo, 36, 13, BEAK, lw=5)
    c.move_to(30, 10 - 4 * bo); c.line_to(38, 18 - 4 * bo); c.line_to(31, 24 - 4 * bo); c.close_path()
    c.set_source_rgb(*SQ_Y); c.fill_preserve(); c.set_source_rgb(*INK); c.set_line_width(3.5); c.stroke()
    # eyes
    lx, ly = look
    for i, ex in enumerate((-20, 20)):
        mode = eyes
        if eyes == "wink" and i == 1:
            mode = "shut"
        elif eyes == "wink":
            mode = "open"
        if mode == "shut":
            c.move_to(ex - 12, -10); c.curve_to(ex - 6, -2, ex + 6, -2, ex + 12, -10)
            c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
            continue
        r = 1.35 if mode == "wide" else 1.0
        ellipse(c, ex, -9, 15 * r, 17 * r, (1, 1, 1), lw=4)
        ellipse(c, ex + lx * 5, -8 + ly * 5, 9, 10, ICE_D, stroke=False)
        ellipse(c, ex + lx * 5, -8 + ly * 5, 5.5, 6.5, INK, stroke=False)
        ellipse(c, ex + lx * 5 + 3, -12 + ly * 5, 2.6, 2.6, (1, 1, 1), stroke=False)
    cap_crown(c, -4, -44, cap_rot, 0.95)
    c.restore()
    # wet sheen
    if wet > 0.01:
        for (dx, dy) in ((-50, -96), (40, -40), (-20, -180), (30, -150)):
            c.move_to(dx, dy - 12); c.curve_to(dx - 6, dy, dx - 6, dy + 6, dx, dy + 6)
            c.curve_to(dx + 6, dy + 6, dx + 6, dy, dx, dy - 12)
            c.set_source_rgba(*ICE_B, 0.9 * wet); c.fill()
    c.restore()
    if glint > 0.01:
        gx = x + jx + (-20 + 4) * s
        gy = y - 151 * s
        star(c, gx + 18 * s, gy - 18 * s, 26 * glint * s, t * 3, (0.85, 0.95, 1.0))


# ---------------- props ----------------
CRACKS = [[(-150, -300), (-200, -200), (-170, -110), (-190, -20)],
          [(100, -300), (150, -230), (120, -150), (175, -60)],
          [(-20, -280), (10, -200), (-40, -120), (0, -40)],
          [(-100, -390), (-60, -330), (-120, -270)],
          [(140, -400), (60, -350), (90, -300)]]


def more_cracks(c, x, y, k):
    if k <= 0:
        return
    c.save(); c.translate(x, y); c.scale(BS, BS)
    n = len(CRACKS)
    for i, pts in enumerate(CRACKS):
        f = max(0.0, min(1.0, k * n - i))
        if f <= 0:
            continue
        c.move_to(*pts[0])
        m = f * (len(pts) - 1)
        for j in range(1, len(pts)):
            if j <= m:
                c.line_to(*pts[j])
            else:
                q = m - (j - 1)
                c.line_to(lerp(pts[j - 1][0], pts[j][0], q), lerp(pts[j - 1][1], pts[j][1], q)); break
        c.set_source_rgb(1, 1, 1); c.set_line_width(9); c.stroke_preserve()
        c.set_source_rgb(*ICE_D); c.set_line_width(4); c.stroke()
    c.restore()


def shards(c, t, t0, x, y):
    """Ice shards bursting out of the block and skittering on the shelf."""
    if t < t0:
        return
    q = t - t0
    rnd = random.Random(22)
    for j in range(16):
        a = rnd.uniform(-math.pi * 0.95, -math.pi * 0.05)
        v = rnd.uniform(380, 900)
        sx0, sy0 = x + rnd.uniform(-140, 140), y - rnd.uniform(60, 300)
        vx, vy = math.cos(a) * v, math.sin(a) * v
        px = sx0 + vx * min(q, 0.8)
        py = sy0 + vy * q + 1500 * q * q
        if py > y - 6:
            py = y - 6
            px = sx0 + vx * min(q, 0.8) * 0.7
        sz = rnd.uniform(18, 40)
        rr = a * 3 + q * rnd.uniform(-8, 8) * (1 if py < y - 6 else 0)
        c.save(); c.translate(px, py); c.rotate(rr)
        c.move_to(-sz, sz * 0.4); c.line_to(0, -sz); c.line_to(sz * 0.7, sz * 0.5); c.close_path()
        c.set_source_rgba(0.82, 0.93, 1.0, 0.9); c.fill_preserve()
        c.set_source_rgb(*ICE_D); c.set_line_width(4); c.stroke()
        c.restore()


def spray(c, t, t0, t1, x, y):
    """Water flung off in all directions (wet-dog shake)."""
    if not (t0 <= t < t1 + 0.4):
        return
    for j in range(14):
        a = j * 2 * math.pi / 14 + (t * 7 if t < t1 else 0)
        q = ((t - t0) * 2.2 + j * 0.13) % 1
        r = 130 + 220 * q
        drop(c, x + math.cos(a) * r, y - 140 + math.sin(a) * r * 0.7, 1.1 * (1 - q * 0.6))


def scarf_bundle(c, x, y, wob=0.0, s=1.0):
    """Crumb's blue-striped scarf thrown over Squeak: a lumpy little tent. (x, y) = bottom centre."""
    c.save(); c.translate(x, y); c.scale(s, s)
    w, h = 125, 230
    c.move_to(-w, 0)
    c.curve_to(-w + 8, -h * 0.6, -w * 0.5, -h - wob * 14, 0, -h - wob * 8)
    c.curve_to(w * 0.5, -h + wob * 10, w - 8, -h * 0.6, w, 0)
    for k in range(4):
        x0 = w - k * (2 * w / 4)
        c.curve_to(x0 - 15, 12, x0 - 45, -8, x0 - 2 * w / 4, 0)
    c.close_path()
    c.set_source_rgb(1, 1, 1); c.fill_preserve()
    c.save(); c.clip()
    for k in range(-5, 6):
        c.move_to(k * 34 - 30, 10); c.line_to(k * 34 + 30, -h - 20)
        c.set_source_rgb(*NAP_B); c.set_line_width(9); c.stroke()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(6); c.stroke()
    # the beak bump pokes out
    ellipse(c, 6, -h * 0.55, 30, 12, (1, 1, 1), lw=5)
    c.restore()


def scarf_flat(c, x, y):
    c.save(); c.translate(x, y)
    rrect(c, -110, -24, 220, 24, 10); c.set_source_rgb(1, 1, 1); c.fill_preserve()
    c.save(); c.clip()
    for k in range(-6, 7):
        c.move_to(k * 30 - 6, 0); c.line_to(k * 30 + 6, -24); c.set_source_rgb(*NAP_B); c.set_line_width(7); c.stroke()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.restore()


def scarf_flying(c, x, y, p, t):
    """The scarf spinning through the air, opening up."""
    c.save(); c.translate(x, y); c.rotate(t * 9)
    w = lerp(60, 130, p); h = lerp(30, 90, p)
    rrect(c, -w, -h / 2, 2 * w, h, 16); c.set_source_rgb(1, 1, 1); c.fill_preserve()
    c.save(); c.clip()
    for k in range(-5, 6):
        c.move_to(k * 26 - 6, h); c.line_to(k * 26 + 6, -h); c.set_source_rgb(*NAP_B); c.set_line_width(7); c.stroke()
    c.restore()
    c.set_source_rgb(*INK); c.set_line_width(5); c.stroke()
    c.restore()


# ---------------- states ----------------
def dill_state(t):
    """(x, y, kw, mode, sq). mode: sit / stand / fly / hide."""
    if t < T_LOOK:
        return DI_X, FLOOR, dict(mood="sheepish", look=(-1, -0.5)), "sit", 1.0
    if t < T_STAND:
        look = (0, -1)
        mood = "shocked"
        for i, d in enumerate(DTAKE):
            if t >= d:
                look = (-1, 0.5) if i % 2 == 0 else (0, -1)
        if T_JUMP <= t < T_PLONK:
            p = seg(t, T_JUMP, T_PLONK)
            look = (1, -1) if p < 0.5 else (0.3, -1)
        sq = 1.0
        if t >= T_PLONK:
            q = t - T_PLONK
            sq = 1 - 0.2 * math.exp(-q * 6) * math.cos(q * 25)
            look = (0, -1)
            if t >= T_OFF:
                look = (-1, -0.3)
        return DI_X, FLOOR, dict(mood=mood, look=look), "sit", sq
    if t < T_THROW:
        mood, look, arm = "angry", (-1, 0), "down"
        if T_POINT <= t < T_TODILL:
            arm = "point_l"
            look = (-1, 0) if t < T_ONDUCK else (-1, -0.6)
        if T_HUH <= t < T_TODILL:
            mood = "shocked"
        sq = 1.0
        if t >= T_DILLLAND:
            mood, look, arm = "shocked", (0, -1), "flail"
            sq = 1.0
            for b in (T_DILLLAND,) + BOUNCES:
                if b <= t < b + 0.35:
                    sq = 1 - 0.18 * math.sin(math.pi * seg(t, b, b + 0.35))
            if t >= STEPS[0]:
                mood, arm, look = "shocked", "down", (1, 0)
        x = DI_X
        if T_HUH <= t < T_HUH + 0.3:
            x = DI_X + 14 * math.sin(math.pi * seg(t, T_HUH, T_HUH + 0.3))
        return x, FLOOR, dict(mood=mood, look=look, arm=arm), "stand", sq
    if t < T_GRABB:
        return DI_X, FLOOR, dict(mood="shocked", look=(0, -1), arm="reach" if t >= T_COVER + 0.4 else "down"), "stand", 1.0
    if t < T_SIT:
        return DI_X - 20 * ease(seg(t, T_GRABB, T_SETB)), FLOOR, dict(mood="angry", look=(-1, 0.6), arm="down"), "stand", 1.0
    if t < T_BIGSQ:
        return DI_X - 20, FLOOR - SIT_LIFT, dict(mood="smug", look=(1, 0)), "sit", 1.0
    if t < T_DLAND2:
        p = seg(t, T_BIGSQ, T_DLAND2)
        x, y = hop((DI_X - 20, FLOOR - SIT_LIFT), (650, FLOOR), p, 520)
        return x, y, dict(mood="shocked", look=(0, 1), arm="flail"), "fly", 1.0
    if t < T_DIVE:
        q = t - T_DLAND2
        return 650, FLOOR, dict(mood="dizzy" if q < 0.6 else "shocked", look=(1, -1)), "stand", 1 - 0.2 * math.exp(-q * 7)
    if t < T_HID:
        p = ease(seg(t, T_DIVE, T_HID))
        return lerp(650, 975, p), FLOOR - abs(math.sin(t * 13)) * 20, dict(mood="scared", look=(1, 0), arm="flail"), "stand", 1.0
    look = (-1, -0.2)
    mood = "scared"
    if t >= T_LIFT:
        look = (-0.5, -1)
        mood = "shocked"
    if t >= T_CLOSE:
        look = (-1, 0.3)
    return 975, FLOOR, dict(mood=mood, look=look), "hide", 1.0


def crumb_state(t):
    """(x, y, kw, has_scarf)."""
    if t < T_LOOK:
        return CR_X, FLOOR, dict(mood="worried", look=(-1, 0), arm="none"), True
    if t < T_THROW:
        kw = dict(mood="scared", look=(-0.5, -1), arm="none")
        if t >= T_BESIDE:
            kw = dict(mood="worried", look=(-1, 0), arm="none")
        if t >= STEPS[0]:
            kw = dict(mood="scared", look=(1, -0.3), arm="none")
        return CR_X, FLOOR, kw, True
    if t < T_DIVE:
        arm = "wave" if t < T_COVER + 0.3 else "down"
        mood = "worried" if t < T_BIGSQ else "scared"
        return CR_X, FLOOR, dict(mood=mood, look=(-1, -0.6), arm=arm), False
    if t < T_HID:
        p = ease(seg(t, T_DIVE, T_HID))
        return lerp(CR_X, 1050, p), FLOOR - abs(math.sin(t * 13 + 1)) * 18, dict(mood="scared", look=(1, 0), arm="wave"), False
    look = (-1, -0.3) if t < T_LIFT else (-0.5, -1)
    return 1050, FLOOR, dict(mood="scared", look=look, arm="down"), False


def chip_state(t):
    """(x, y, kw, alpha)."""
    if t < T_LOOK:
        return CH_X, FLOOR, dict(mood="shy", look=(1, 0)), 1.0
    if t < T_DIVE:
        a = lerp(1.0, 0.28, ease(seg(t, T_SEE, T_SEE + 0.4)))
        mood = "eep" if t < T_SEE + 1.0 else "scared"
        return CH_X, FLOOR, dict(mood=mood, look=(-0.5, -1) if t < T_OFF else (-1, 0), arms="cover" if t < T_SEE + 1.0 else "down"), a
    if t < T_HID:
        p = ease(seg(t, T_DIVE, T_HID))
        return lerp(CH_X, 1000, p), FLOOR - abs(math.sin(t * 13 + 2)) * 18, dict(mood="eep", look=(1, 0), arms="up"), 0.28
    return 1000, FLOOR, dict(mood="scared", look=(-1, -0.3)), 0.28


def peep_kw(t):
    """Peep, on Crumb's head: (mood, wings, look, extra_y)."""
    if t < T_LOOK:
        return "blink", "down", (-1, 0), 0.0
    if t < T_LOVE:
        return "shock", "down", (-0.5, -1), 0.0
    if t < STEPS[0] - 0.4:
        dy = 0.0
        for b in BOUNCES:
            b2 = b + 0.3
            if b2 <= t < b2 + 0.45:
                dy = -120 * math.sin(math.pi * seg(t, b2, b2 + 0.45))
        mood = "love" if t < T_STAND + 0.4 else "happy"
        wings = "flap" if dy < 0 else "down"
        return mood, wings, (-1, 0), dy
    if t < T_HID:
        return "shock", "flap" if t >= T_DIVE else "down", (1, 0), 0.0
    return "shock", "down", (-1, -0.3) if t < T_LIFT else (-0.5, -1), 0.0


def squeak_state(t):
    """(x, y, kw)."""
    if t < T_SHATTER:
        return None
    if t < T_LOOK + 0.01 or t < T_JUMP:
        kw = dict(eyes="shut", wet=1.0, shiver=1.0 if t < T_SHAKE else 0.0, cap_rot=0.38)
        x, y = BLOCK_X, TOP
        if T_SHAKE <= t < T_FLIP + 0.3:
            kw["rot"] = 0.22 * math.sin((t - T_SHAKE) * 38)
            kw["wet"] = 1 - seg(t, T_SHAKE, T_FLIP + 0.3)
        if t >= T_FLIP:
            p = back_out(seg(t, T_FLIP, T_FLIP + 0.25))
            kw["cap_rot"] = lerp(0.38, -0.38, p)
            kw["wet"] = 0.0
        if t >= T_EYES:
            kw["eyes"] = "wide" if t < T_EYES + 0.4 else "open"
            kw["glint"] = math.sin(math.pi * seg(t, T_EYES, T_EYES + 0.5))
        for s0 in SQUEAKS_TOP:
            if s0 <= t < s0 + 0.45:
                p = seg(t, s0, s0 + 0.45)
                y = TOP - 110 * math.sin(math.pi * p)
                kw["beak"] = math.sin(math.pi * p)
                kw["sq"] = 1.12 if p < 0.5 else 1 - 0.25 * math.sin(math.pi * seg(p, 0.8, 1.0))
        if t >= T_LOOK:
            # keeps hopping up there while the camera is below
            ph = (t - T_LOOK) % 0.6
            if ph < 0.4:
                y = TOP - 90 * math.sin(math.pi * ph / 0.4)
                kw["beak"] = math.sin(math.pi * ph / 0.4)
        return x, y, kw
    if t < T_BOING:
        p = seg(t, T_JUMP, T_BOING)
        x, y = hop((BLOCK_X, TOP), (JX, FLOOR - 150), p, 260)
        return x, y, dict(beak=0.6, rot=-1.4 * p, eyes="wide")
    if t < T_PLONK:
        p = seg(t, T_BOING, T_PLONK)
        x, y = hop((JX, FLOOR - 150), (DI_X, FLOOR - DILL_HEAD * 0.8 + 20), p, 380)
        return x, y, dict(beak=0.8, rot=-1.4 + 1.4 * p - 2 * math.pi * p, eyes="wide")
    if t < T_OFF:
        q = t - T_PLONK
        return DI_X, FLOOR - DILL_HEAD * 0.8 + 20, dict(look=(0.5, 1), sq=1 - 0.2 * math.exp(-q * 7), beak=0.5 if q < 0.3 else 0.0)
    if t < T_BESIDE:
        p = seg(t, T_OFF, T_BESIDE)
        x, y = hop((DI_X, FLOOR - DILL_HEAD * 0.8 + 20), (SQ_HOME, FLOOR), p, 330)
        return x, y, dict(rot=-0.8 * math.sin(math.pi * p), beak=0.3)
    if t < T_ONDUCK:
        q = t - T_BESIDE
        lk = (1, 0) if t < T_POINT else (1, -0.3)
        return SQ_HOME, FLOOR, dict(look=lk, sq=1 - 0.2 * math.exp(-q * 7))
    if t < T_DUCKLAND:
        p = seg(t, T_ONDUCK, T_DUCKLAND)
        x, y = hop((SQ_HOME, FLOOR), (DUCK_X + 4, FLOOR - DUCK_HEAD), p, 220)
        return x, y, dict(beak=0.4, look=(1, -1))
    if t < T_TODILL:
        kw = dict(look=(1, 0.3))
        rot = 0.0
        if T_BOOP - 0.15 <= t < T_BOOP + 0.3:
            rot = 0.35 * math.sin(math.pi * seg(t, T_BOOP - 0.15, T_BOOP + 0.3))
            kw["beak"] = 0.8 if t >= T_BOOP else 0.0
        kw["rot"] = rot
        return DUCK_X + 4, FLOOR - DUCK_HEAD, kw
    if t < T_DILLLAND:
        p = seg(t, T_TODILL, T_DILLLAND)
        x, y = hop((DUCK_X + 4, FLOOR - DUCK_HEAD), (DI_X, FLOOR - DILL_HEAD), p, 200)
        return x, y, dict(beak=0.4, look=(1, 0))
    if t < T_THROW + 0.2:
        y = FLOOR - DILL_HEAD
        kw = dict(look=(0, 1))
        for b in BOUNCES:
            if b <= t < b + 0.5:
                p = seg(t, b, b + 0.5)
                y = FLOOR - DILL_HEAD - 130 * math.sin(math.pi * p)
                kw["beak"] = math.sin(math.pi * p)
                kw["sq"] = 1.1 if p < 0.5 else 1.0
        if t >= STEPS[0]:
            kw = dict(eyes="wide", look=(1, 0))
        return DI_X, y, kw
    if t < T_POPOUT:
        return "bundle"
    if t < T_SQHOME:
        p = seg(t, T_POPOUT, T_SQHOME)
        x, y = hop((DI_X - 20, FLOOR - SIT_LIFT + 30), (SQ_HOME, FLOOR), p, 420)
        return x, y, dict(beak=1.0 if p < 0.4 else 0.2, rot=-2 * math.pi * p, eyes="wide")
    q = t - T_SQHOME
    kw = dict(sq=1 - 0.2 * math.exp(-q * 7))     # sits perfectly still, copying the Duck
    if t >= T_HSET:
        kw["look"] = (0.3, -1)
    if t >= T_LIFT:
        kw["look"] = (1, -1)
    if t >= T_GONE:
        kw["look"] = (0, 0)
    if t >= T_GLINT:
        kw["glint"] = math.sin(math.pi * seg(t, T_GLINT, T_GLINT + 0.5))
    if t >= T_WINK:
        kw["eyes"] = "wink" if t < T_WINK + 0.55 else "open"
        kw["beak"] = 0.7 * math.sin(math.pi * seg(t, T_WINK, T_WINK + 0.35))
        kw["tilt"] = -0.15 * ease(seg(t, T_WINK, T_WINK + 0.3))
    return SQ_HOME, FLOOR, kw


def hand_state(t):
    """(x, tip_y, grip) or None."""
    if t < T_HDOWN or t >= T_GONE:
        return None
    if t < T_HSET:
        return 310, lerp(-700, FLOOR - 340, ease_out(seg(t, T_HDOWN, T_HSET))), 0.0
    if t < T_REACH:
        q = t - T_HSET
        x = 310 + 115 * math.sin(q * math.pi / 1.0 - math.pi / 2) * min(1, q * 2)
        return x, FLOOR - 340 + 10 * math.sin(q * 6), 0.0
    tip = FLOOR - 175
    if t < T_GRIP:
        p = ease(seg(t, T_REACH, T_GRIP))
        x0 = 310 + 115 * math.sin((T_REACH - T_HSET) * math.pi / 1.0 - math.pi / 2)
        return lerp(x0, DUCK_X + 12, p), lerp(FLOOR - 340, tip, p), 0.0
    if t < T_LIFT:
        return DUCK_X + 12, tip, 0.6 * ease(seg(t, T_GRIP, T_LIFT))
    return DUCK_X + 12, tip - 1700 * ease(seg(t, T_LIFT, T_GONE)) ** 1.4, 0.6


def duck_place(t):
    """(x, y, gaze) of the Duck or None (gone)."""
    hs = hand_state(t)
    gaze = -1.4 * ease(seg(t, T_GAZE, T_GAZE + 0.6))
    if t >= T_LIFT and hs is not None:
        return DUCK_X, FLOOR + (hs[1] - (FLOOR - 175)), gaze
    if t >= T_LIFT:
        return None
    return DUCK_X, FLOOR, gaze


# ---------------- camera ----------------
KEYS = [(0.0, 880, 520, 2.15), (T_SHATTER, 880, 540, 2.15), (T_SHAKE, 885, 560, 2.35), (T_LOOK - 0.02, 885, 560, 2.35),
        (T_LOOK, 640, 1215, 1.4), (DTAKE[-1] + 0.3, 640, 1215, 1.4), (T_JUMP - 0.05, 640, 1215, 1.4),
        (T_JUMP + 0.25, 680, 1040, 0.98), (T_PLONK, 640, 1080, 1.05), (T_OFF, 520, 1180, 1.3),
        (T_BESIDE + 0.2, 420, 1255, 1.65), (T_LOVE - 0.1, 420, 1255, 1.65), (T_LOVE + 0.3, 560, 1215, 1.3),
        (T_STAND, 560, 1215, 1.3), (T_POINT + 0.2, 430, 1240, 1.6), (T_HUH + 0.4, 430, 1240, 1.6),
        (T_DILLLAND + 0.1, 700, 1170, 1.3), (STEPS[0], 700, 1170, 1.3), (STEPS[-1] + 0.3, 690, 1150, 1.25),
        (T_COVER, 640, 1200, 1.4), (T_BIGSQ - 0.1, 520, 1240, 1.55), (T_BIGSQ + 0.3, 560, 1150, 1.3), (T_SQHOME, 530, 1180, 1.3),
        (T_OPEN, 590, 1170, 1.2), (T_HSET, 600, 1160, 1.13), (T_REACH, 600, 1160, 1.13), (T_LIFT, 540, 1120, 1.15),
        (T_GONE, 420, 1200, 1.3), (T_GLINT, 250, 1290, 2.3), (END_T, 230, 1290, 2.6)]


def camera(t):
    cx, cy, z = keyed(KEYS, t)
    shakes = [(T_CR1, 10, 0.2), (T_CR2, 12, 0.25), (T_SHATTER, 22, 0.4), (T_PLONK, 10, 0.25), (T_BIGSQ, 18, 0.4),
              (T_OPEN, 6, 0.2), (T_CLOSE, 6, 0.2)] + [(s, 9, 0.25) for s in STEPS]
    for (t0, q0, d) in shakes:
        if t0 <= t < t0 + d:
            q = q0 * (1 - seg(t, t0, t0 + d)); cx += random.uniform(-q, q); cy += random.uniform(-q, q)
    return cx, cy, z


# ---------------- the scene ----------------
def draw_chip(c, t, x, y, kw, alpha):
    def d():
        cape(c, x, y, CHS, sway=0.5 * math.sin(t * 3))
        chip(c, x, y, CHS, t=t, **kw)
        cape_tie(c, x, y - 6, CHS)
    if alpha < 0.999:
        glazed(c, d, 0.0, alpha)
        for ex in (-19, 19):
            ellipse(c, x + ex * CHS, y - 64 * CHS, 7, 8, INK, stroke=False)
    else:
        d()


def draw_squeak(c, t, st):
    if st is None or st == "bundle":
        return
    x, y, kw = st
    squeak_duck(c, x, y, t=t, **kw)


def scene(c, t):
    L = light_at(t)
    fridge6(c, L, 1, lid=False)
    frost(c, t, 1.0)
    ceiling(c, L)
    ceiling_vent(c, L)
    god_rays(c, L)
    butter_rink(c, 1.0)
    splats(c, 30.0)
    wob = 0.0
    if T_BOING <= t < T_BOING + 1.2:
        q = t - T_BOING
        wob = 1.6 * math.exp(-q * 4) * math.cos(q * 22)
    mist(c, t, 0.35)
    if t < T_HID:
        jello(c, JX, FLOOR, wob)

    # the Duck on the throne
    dp = duck_place(t)
    if dp is not None and t < T_LIFT:
        dx_, dy_, gz = dp
        clean_duck(c, dx_, dy_, tilt=0.35, gaze=2.0 + gz, frosty=0.4, s=DUCK_S)

    # Chip
    chx, chy, ckw, calpha = chip_state(t)
    c.save()
    if t >= T_HID:
        c.rectangle(-500, -500, 2500, FLOOR + 500); c.clip(); c.translate(0, 75)
    draw_chip(c, t, chx, chy, ckw, calpha)
    c.restore()

    # Crumb + Peep
    crx, cry, ckw2, has_scarf = crumb_state(t)
    hiding = t >= T_HID
    c.save()
    if hiding:
        c.rectangle(-500, -500, 2500, FLOOR + 500); c.clip(); c.translate(0, 75)
    crumb_bitten(c, crx, cry, 1.0, **ckw2)
    pm, pw, pl, pdy = peep_kw(t)
    fat_peep(c, crx, cry - 296 + pdy, FAT, mood=pm, wings=pw, look=pl, flap_t=t, face=-0.5)
    if has_scarf:
        crumb_arms(c, t, crx, cry, 0.0, "rest")
        scarf_cloth(c, crx + 105, FLOOR - 70, w=70, h=40, rot=1.4, wet=0.3)
    c.restore()
    if T_LOVE <= t < T_STAND + 0.4:
        for j in range(3):
            q = ((t - T_LOVE) * 0.9 + j / 3) % 1
            heart(c, crx - 60 + 50 * j, cry - 470 - 140 * q, 1.3, 1 - q)

    # the scarf: in flight / bundle / flat on the shelf
    if T_THROW <= t < T_COVER:
        p = seg(t, T_THROW, T_COVER)
        sx, sy = hop((crx + 60, FLOOR - 300), (DI_X, FLOOR - DILL_HEAD - 120), p, 260)
        scarf_flying(c, sx, sy, p, t)

    # Dill
    dx, dy, dkw, dmode, dsq = dill_state(t)
    if dmode != "hide":
        c.save()
        if dmode == "sit":
            sq = 0.8 * dsq
            c.translate(dx, dy); c.scale(1 / sq ** 0.4, sq); c.translate(-dx, -dy)
        elif dsq != 1.0:
            c.translate(dx, dy); c.scale(1 / dsq ** 0.4, dsq); c.translate(-dx, -dy)
        if dmode == "fly":
            rot_at(c, dx, dy - 150, -2 * math.pi * seg(t, T_BIGSQ, T_DLAND2))
        draw_dill(c, t, dx, dy, dkw)
        jello_glob(c, dx + 6, dy - 300, 1.1)
        c.restore()
    head_y = FLOOR - DILL_HEAD * (0.8 * dsq if dmode == "sit" else dsq)

    # the bundle (on Dill's head, then under him)
    if T_COVER <= t < T_BIGSQ:
        if t < T_GRABB:
            wob_b = math.sin((t - T_COVER) * 14) if t >= T_COVER + 0.3 else 0.0
            hop_b = abs(math.sin((t - T_COVER) * 7)) * 30 if t >= T_COVER + 0.4 else 0.0
            scarf_bundle(c, DI_X, head_y - hop_b + 6, wob_b, 0.75)
        elif t < T_SIT:
            p = ease(seg(t, T_GRABB, T_SETB))
            scarf_bundle(c, lerp(DI_X, DI_X - 20, p), lerp(head_y, FLOOR, p) + 6, 0.0, 0.75)
        else:
            k = 0.42
            c.save(); c.translate(DI_X - 20, FLOOR); c.scale(1 + 0.3 * (1 - k), k); c.translate(-(DI_X - 20), -FLOOR)
            scarf_bundle(c, DI_X - 20, FLOOR + 4, 0.0, 0.75)
            c.restore()
    if t >= T_BIGSQ:
        scarf_flat(c, DI_X - 10, FLOOR + 2)
    if dmode == "sit" and T_SIT <= t < T_BIGSQ:
        # Dill drawn again on top of the bundle (smug)
        c.save(); sq = 0.8; c.translate(dx, dy); c.scale(1 / sq ** 0.4, sq); c.translate(-dx, -dy)
        draw_dill(c, t, dx, dy, dkw); jello_glob(c, dx + 6, dy - 300, 1.1)
        c.restore()

    # Squeak
    sst = squeak_state(t)
    if sst is not None and sst != "bundle" and t >= T_JUMP:
        draw_squeak(c, t, sst)

    # hiding behind the jello: characters crouched, the jello in front of them
    if dmode == "hide":
        c.save(); c.rectangle(-500, -500, 2500, FLOOR + 500); c.clip(); c.translate(0, 75)
        draw_dill(c, t, dx, dy, dkw); jello_glob(c, dx + 6, dy - 300, 1.1)
        c.restore()
    if t >= T_HID:
        jello(c, JX, FLOOR, wob)

    # the Hand (+ the Duck in its grip)
    hs = hand_state(t)
    if hs is not None:
        hx, htip, grip = hs
        if t >= T_LIFT and dp is not None:
            clean_duck(c, dp[0], dp[1], tilt=0.35, gaze=2.0 + dp[2], frosty=0.4, s=DUCK_S)
        hand_cuffed(c, hx, htip, grip, duck_turn=0.0)

    drawer_front(c)
    dark_overlay(c, L)

    # ice block + shards (top shelf, in the dark: drawn after the overlay with its own glow)
    if t < T_SHATTER:
        crack = 1.0
        block21(c, t, BLOCK_X, TOP, glow=0.45, crack=crack, wet=1.0)
        more_cracks(c, BLOCK_X, TOP, ease_out(seg(t, T_CR1 - 0.1, T_CR2 + 0.3)))
    ellipse(c, BLOCK_X + 40, TOP + 2, 200, 12, (0.72, 0.88, 1.0), lw=3)
    shards(c, t, T_SHATTER, BLOCK_X, TOP)
    if T_SHATTER <= t < T_SHATTER + 0.35:
        q = seg(t, T_SHATTER, T_SHATTER + 0.35)
        c.save(); c.translate(BLOCK_X, TOP - 180); c.arc(0, 0, 60 + 400 * q, 0, 2 * math.pi); c.restore()
        c.set_source_rgba(0.9, 0.97, 1.0, 0.7 * (1 - q)); c.set_line_width(26 * (1 - q) + 2); c.stroke()
    if sst is not None and sst != "bundle" and t < T_JUMP:
        # Squeak on the top shelf: drawn after the overlay with a faint icy glow so it reads in the dark
        x, y, kw = sst
        rg = cairo.RadialGradient(x, y - 120, 20, x, y - 120, 300)
        rg.add_color_stop_rgba(0, 0.85, 0.95, 1, 0.35); rg.add_color_stop_rgba(1, 0.85, 0.95, 1, 0)
        c.rectangle(x - 320, y - 440, 640, 480); c.set_source(rg); c.fill()
        draw_squeak(c, t, sst)
        spray(c, t, T_SHAKE, T_FLIP + 0.2, x, y)
        if t < T_SHAKE:
            for j in range(2):
                q = ((t - T_SHATTER) * 1.4 + j * 0.5) % 1
                drop(c, x - 70 + 140 * j, y - 200 + 160 * q, 1.0)

    # the Duck squeaky clean eyes shift: little glint in the dark
    if dmode == "hide" and T_LIFT <= t < T_GONE:
        pass

    # words
    word(c, t, "CRACK!", 850, 300, 90, (1, 1, 1), T_CR1, T_CR1 + 0.55, -0.1)
    word(c, t, "CRACK!", 930, 860, 100, (1, 1, 1), T_CR2, T_CR2 + 0.6, 0.1)
    word(c, t, "KSSSH!", BLOCK_X, 300, 120, (0.85, 0.95, 1.0), T_SHATTER, T_SHATTER + 0.8, -0.05)
    word(c, t, "brrrrr...", BLOCK_X + 60, 480, 64, ICE_B, T_SHATTER + 0.8, T_SHAKE, 0.05)
    word(c, t, "shake shake!", BLOCK_X, 300, 64, (1, 1, 1), T_SHAKE + 0.1, T_FLIP + 0.3, -0.05)
    word(c, t, "ping!", BLOCK_X - 160, 420, 50, GOLD, T_FLIP, T_FLIP + 0.5, -0.1)
    for i, s0 in enumerate(SQUEAKS_TOP):
        word(c, t, "SQUEAK!", BLOCK_X + (-120 if i % 2 else 120), 300 + 30 * i, 74, GOLD, s0, s0 + 0.45, 0.1 if i % 2 else -0.1)
    word(c, t, "SQUEAK! SQUEAK!", 640, 820, 70, GOLD, T_LOOK, T_JUMP, 0.04)
    word(c, t, "!!", 760, 1000, 110, RED, T_LOOK + 0.15, T_LOOK + 0.8, 0.08)
    for i, d in enumerate(DTAKE):
        word(c, t, "boing", 470 + 40 * (i % 2), 1070 - 20 * i, 44, (1, 1, 1), d, d + 0.35, -0.1 if i % 2 else 0.1)
    word(c, t, "eep!", CH_X + 70, FLOOR - 300, 54, (1, 1, 1), T_SEE, T_SEE + 0.8, 0.1)
    word(c, t, "WHEEE!", 900, 900, 80, (1, 1, 1), T_JUMP + 0.1, T_BOING, 0.06)
    word(c, t, "BOING!", JX + 20, FLOOR - 330, 90, hexc("#FF8FB3"), T_BOING, T_BOING + 0.5, -0.08)
    word(c, t, "PLONK!", DI_X + 40, FLOOR - 560, 84, (1, 1, 1), T_PLONK, T_PLONK + 0.6, 0.08)
    word(c, t, "plink", SQ_HOME - 10, FLOOR - 300, 48, (1, 1, 1), T_BESIDE, T_BESIDE + 0.5, -0.1)
    word(c, t, "?!", 540, FLOOR - 340, 84, (1, 1, 1), T_BESIDE + 0.15, T_LOVE + 0.3, 0.08)
    word(c, t, "chirp...", 300, FLOOR - 420, 50, (1, 1, 1), T_CHIRP, T_ONDUCK - 0.1, -0.05)
    word(c, t, "boop", DUCK_X + 150, FLOOR - 430, 54, (1, 1, 1), T_BOOP, T_BOOP + 0.5, 0.1)
    word(c, t, "?!", DI_X + 80, FLOOR - 400, 90, RED, T_HUH, T_TODILL, 0.08)
    for i, b in enumerate(BOUNCES):
        word(c, t, "SQUEAK!", DI_X + (-150 if i % 2 else 150), FLOOR - 560 - 20 * (i % 3), 66, GOLD, b + 0.05, b + 0.45,
             0.1 if i % 2 else -0.1)
        word(c, t, "peep!", CR_X + 120, FLOOR - 560, 44, (1, 1, 1), b + 0.35, b + 0.7, 0.08)
    for i, s0 in enumerate(STEPS):
        word(c, t, "THMP", 1000 - 90 * i, 980 + 30 * i, 80 + 10 * i, (1, 1, 1), s0, s0 + 0.5, 0.06 if i % 2 else -0.06)
    word(c, t, "!!", DI_X, FLOOR - 520, 90, RED, STEPS[-1] + 0.2, T_THROW, 0.05)
    word(c, t, "mmf! mmf!", DI_X + 30, FLOOR - 560, 58, (1, 1, 1), T_COVER + 0.2, T_GRABB, -0.05)
    word(c, t, "SQUEEEEEEAK!!", 560, FLOOR - 480, 96, GOLD, T_BIGSQ, T_BIGSQ + 0.9, -0.06)
    word(c, t, "AAAH!", 900, FLOOR - 420, 70, (1, 1, 1), T_DIVE, T_HID, 0.06)
    for i, tk in enumerate(TICKS):
        word(c, t, "tick..." if i % 2 == 0 else "tock...", 330 + (-60 if i % 2 == 0 else 60), FLOOR - 820, 60, (1, 1, 1), tk, tk + 0.8,
             -0.06 if i % 2 == 0 else 0.06)
    word(c, t, "THUD", 540, 900, 80, (1, 1, 1), T_CLOSE, T_CLOSE + 0.45, -0.05)
    word(c, t, "squeak!", SQ_HOME + 170, FLOOR - 370, 54, GOLD, T_WINK, T_WINK + 0.7, 0.1)


def frame(c, t):
    if t >= END_T:
        end_card(c, t, END_T); return
    random.seed(int(t * 30))
    cx, cy, Z = camera(t)
    c.save(); c.translate(W / 2, H / 2); c.scale(Z, Z); c.translate(-cx, -cy)
    scene(c, t)
    c.restore()
    if T_SHATTER <= t < T_SHATTER + 0.1:
        c.rectangle(0, 0, W, H); c.set_source_rgba(0.85, 0.95, 1, 0.4); c.fill()
    if T_OPEN <= t < T_OPEN + 0.1:
        c.rectangle(0, 0, W, H); c.set_source_rgba(1, 1, 1, 0.35); c.fill()
    for d in DUNS:
        if d <= t < d + 0.12:
            c.rectangle(0, 0, W, H); c.set_source_rgba(0.1, 0.4, 0.8, 0.14); c.fill()
    if t >= END_T - 0.4:
        ex = W / 2 + (SQ_HOME + 4 - cx) * Z
        ey = H / 2 + (FLOOR - 150 * SQ_S - cy) * Z
        iris(c, ex, ey, lerp(900, 0, ease(seg(t, END_T - 0.4, END_T))))
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
