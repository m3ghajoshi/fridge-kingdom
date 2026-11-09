"""Sound for FRIDGE KINGDOM Ep16 "The Ice Cube" (variant B: cold open)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
import ep2_audio as A2
from ep4_audio import chord
from ep5_audio import drone
import ep6_audio as A6
from ep7_audio import gasp, peep
from ep8_audio import shimmer, dun
from ep10_audio import icy, squish, whistle
from ep11_audio import harp, ooh, plip
from ep12_audio import flaps
from ep13_audio import tinkle
from ep15_audio import chatter, sniff
from audio import SR, tarr, midi, place, plink, pluck, sweep, whoosh, thud, pop, marimba, ding, sting, boing
import ep16 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A2.N = N
A6.N = N
rng = np.random.default_rng(1616)


def waltz(start, end, mix, gain=0.28):
    """Little ice-rink waltz: oom-pah-pah with a twinkly tune."""
    prog = [(48, [64, 67]), (43, [62, 65]), (43, [62, 65]), (48, [64, 67]),
            (45, [64, 69]), (41, [65, 69]), (43, [62, 67]), (48, [64, 67])]
    tune = [76, 79, 84, 83, 79, 76, 74, 77, 83, 81, 77, 74, 72, 76, 81, 79, 76, 72, 71, 74, 79, 72, 76, 79]
    beat = 0.36
    at, i = start, 0
    while at < end:
        bar, b = divmod(i, 3)
        root, ch = prog[bar % len(prog)]
        if b == 0:
            place(mix, marimba(midi(root), 0.4), at, gain * 1.3)
        else:
            for m in ch:
                place(mix, pluck(midi(m), 0.18, 0.4), at, gain * 0.5)
        place(mix, plink(midi(tune[i % len(tune)])) * 0.6, at, gain * 0.9)
        i += 1; at += beat


def skate(d=0.5):
    """Swish of a skate blade."""
    t = tarr(d)
    n = rng.standard_normal(len(t))
    env = np.sin(np.pi * t / d) ** 2
    return (n - np.concatenate([[0], n[:-1]])) * env * 0.35


def slide_whistle(f0, f1, d):
    return sweep(f0, f1, d, vdepth=0.01)


def build(path):
    mix = E.hum() * 0.5
    # 0–3.2: cold open: searchlight, eep, sploosh, sniffs, it gives up
    tmp = np.zeros(N); place(tmp, icy(3.6), 0.0, 0.45); mix += tmp
    place(mix, drone(3.4), 0.0, 0.3)
    place(mix, chatter(V.T_DIVE), 0.0, 0.5)
    place(mix, sweep(1800, 2600, 0.18, vdepth=0) * 0.5, V.T_EEP, 0.5)
    place(mix, whoosh(0.4), V.T_DIVE, 0.35)
    place(mix, squish(0.4), V.T_SPLOOSH, 0.6)
    for k in range(3):
        place(mix, plip(), V.T_SPLOOSH + 0.05 + 0.1 * k, 0.4)
    place(mix, sweep(900, 400, 0.4, vdepth=0) * 0.2, V.T_SPLOOSH + 0.1, 0.25)     # going see-through
    for s in V.SNIFFS:
        place(mix, sniff(0.55), s, 0.8)
    place(mix, E.gib(2, 38, spread=2, syl=0.25, bright=0.3), V.T_GIVEUP - 0.1, 0.6)   # hmm...
    place(mix, sweep(500, 250, 0.6, vdepth=0) * 0.25, V.T_GIVEUP, 0.3)
    # 3.9–8.4: PAH, phew, idea, helmet clanks and slides
    place(mix, pop(), V.T_PAH, 0.6)
    place(mix, E.gib(1, 76, spread=2, syl=0.12, bright=0.9), V.T_PAH + 0.02, 0.5)
    for k, b in enumerate((60, 52, 70)):
        place(mix, E.gib(1, b, spread=1, syl=0.22, bright=0.3), V.T_PHEW + 0.05 * k, 0.3)
    place(mix, ding(), V.T_IDEA, 0.5)
    place(mix, shimmer(0.6), V.T_IDEA, 0.3)
    place(mix, E.gib(3, 56, spread=6, syl=0.08, bright=0.9), V.T_IDEA + 0.15, 0.5)
    place(mix, whoosh(0.4), V.T_FETCH + 0.4, 0.3)
    place(mix, A6.clang(), V.T_PUT1, 0.6)
    place(mix, E.fanfare()[:int(SR * 0.6)], V.T_PUT1 + 0.1, 0.25)
    place(mix, A6.shhhk(0.35), V.T_SLIP1 + 0.05, 0.5)
    place(mix, slide_whistle(900, 400, 0.4), V.T_SLIP1 + 0.05, 0.3)
    place(mix, A6.clang(), V.T_SLIP1 + 0.5, 0.4)
    place(mix, A6.clang(), V.T_PUT2, 0.5)
    place(mix, A6.shhhk(0.35), V.T_SLIP2 + 0.05, 0.5)
    place(mix, slide_whistle(900, 350, 0.4), V.T_SLIP2 + 0.05, 0.3)
    place(mix, A6.clang(), V.T_SLIP2 + 0.5, 0.4)
    place(mix, E.hiss(0.6), V.T_STEAM, 0.5)
    place(mix, E.gib(4, 50, spread=7, syl=0.07, bright=1.0), V.T_STEAM + 0.05, 0.55)
    # 9–13: drill practice; Chip skates away
    whistle(V.T_WHISTLE, mix)
    for k in range(4):
        place(mix, boing() * 0.5, V.T_WHISTLE + 0.1 + 0.12 * k + 0.5, 0.25)
    A6.march(V.T_MARCH, V.T_EDGE, mix, gain=0.32)
    for k in range(3):
        place(mix, E.gib(1, 55, spread=1, syl=0.1, bright=0.7), V.T_MARCH + k, 0.4)       # hup
    place(mix, sweep(1500, 2400, 0.15, vdepth=0) * 0.4, V.T_CSLIP, 0.45)
    at = V.T_CSLIP + 0.25
    while at < V.T_EDGE:
        place(mix, skate(0.35), at, 0.6); at += 0.38
    place(mix, whoosh(0.7), V.T_EDGE, 0.5)
    place(mix, slide_whistle(1400, 300, 0.9), V.T_EDGE + 0.05, 0.35)
    place(mix, E.gib(3, 70, spread=6, syl=0.06, bright=1.0), V.T_EDGE - 0.2, 0.5)   # Crumb panics
    place(mix, whoosh(0.6), V.T_CDIVE, 0.45)
    # 14: SQUISH x2
    place(mix, squish(0.45), V.T_SQUISH, 0.9)
    place(mix, thud(), V.T_SQUISH, 0.4)
    place(mix, squish(0.45), V.T_SQUISH2, 0.8)
    # 15.2–22: skating waltz; Peep copies; Dill slips into the jello
    waltz(V.T_GLIDE - 0.3, V.T_MELT + 0.4, mix)
    at = V.T_GLIDE
    while at < V.T_BLUSH:
        place(mix, skate(0.5), at, 0.45); at += 0.72
    place(mix, shimmer(0.8), 16.2, 0.3)                       # pirouette
    place(mix, E.gib(2, 66, spread=4, syl=0.07, bright=0.7), V.T_HANDS + 0.1, 0.4)
    harp(V.T_HANDS + 1.0, mix, gain=0.2)
    flaps(mix, V.T_PEEP, V.T_PEEP + 0.7, 0.06, 0.4)
    place(mix, peep(), V.T_PEEP + 0.8, 0.45)
    place(mix, shimmer(0.9), V.T_PEEP + 0.8, 0.25)
    place(mix, whoosh(0.4), V.T_DFALL, 0.4)
    place(mix, E.gib(3, 52, spread=6, syl=0.07, bright=1.0), V.T_DFALL + 0.05, 0.5)
    place(mix, slide_whistle(500, 1300, 0.3), V.T_DLAND, 0.35)
    place(mix, skate(0.4), V.T_DLAND + 0.05, 0.6)
    place(mix, boing(), V.T_THUD, 0.6)
    place(mix, thud(), V.T_THUD, 0.5)
    for k in range(4):
        place(mix, plink(midi(88 + 3 * (k % 2))) * 0.6, V.T_THUD + 0.2 + 0.18 * k, 0.25)
    # 22–25.4: blush, melt, panic, scoop, toss, plop
    place(mix, ooh(1.0), V.T_BLUSH, 0.3)
    for k in range(6):
        place(mix, plip(), V.T_MELT + 0.3 + 0.2 * k, 0.4)
    place(mix, sweep(700, 300, 1.0, vdepth=0.02) * 0.25, V.T_MELT + 0.3, 0.3)
    place(mix, E.gib(4, 70, spread=6, syl=0.06, bright=1.0), V.T_PANIC, 0.55)
    at = V.T_SCOOP
    while at < V.T_TOSS:
        place(mix, A2.war_drum(0, 1, 0.1)[:int(SR * 0.1)] * 0.3 if False else thud() * 0.25, at, 0.4); at += 0.13
    place(mix, whoosh(0.5), V.T_TOSS, 0.45)
    place(mix, slide_whistle(400, 1200, 0.5), V.T_TOSS + 0.02, 0.3)
    place(mix, pop(), V.T_PLOP, 0.6)
    flaps(mix, V.T_TOSS + 0.2, V.T_TOSS + 0.8, 0.06, 0.35)
    # 25.4–27.1: carton frosts; the Duck turns; DING; Chip pops out
    tmp = np.zeros(N); place(tmp, icy(1.2), V.T_FROST, 0.45); mix += tmp
    for k in range(5):
        place(mix, tinkle() * 0.6, V.T_FROST + 0.1 * k, 0.3)
    place(mix, E.squeak(0.5), V.T_DUCK + 0.1, 0.7)
    place(mix, ding(), V.T_DING, 0.6)
    place(mix, pop(), V.T_POP, 0.6)
    for i, m in enumerate([72, 76, 79, 84]):
        place(mix, marimba(midi(m), 0.4), V.T_POP + 0.08 * i, 0.4)
    place(mix, whoosh(0.4), V.T_POP + 0.1, 0.3)
    place(mix, boing(), V.T_LANDC, 0.3)
    # 27.5–31.6: the freezer mime: peas, blizzard, the shadow king
    for k in range(6):
        place(mix, marimba(midi(79 + (k % 3) * 2), 0.2), V.T_MIME + 0.15 + 0.22 * k, 0.25)
    place(mix, E.gib(4, 74, spread=5, syl=0.07, bright=0.6), V.T_MIME + 0.1, 0.35)
    tmp = np.zeros(N); place(tmp, icy(V.T_KING - V.T_BLIZ), V.T_BLIZ, 0.6); mix += tmp
    place(mix, whoosh(1.2), V.T_BLIZ, 0.4)
    for k in range(4):
        place(mix, E.gib(2, 58 + 5 * k, spread=3, syl=0.06, bright=0.5), V.T_BLIZ + 0.3 + 0.2 * k, 0.25)
    place(mix, chatter(V.T_KING - V.T_BLIZ), V.T_BLIZ, 0.35)
    place(mix, drone(V.T_DIDEA - V.T_KING), V.T_KING, 0.4)
    place(mix, chord([50, 53, 56, 59], 1.2), V.T_KING, 0.25)
    for k in range(4):
        place(mix, gasp(), V.T_GASP + 0.06 * k, 0.45)
    place(mix, sting(), V.T_GASP, 0.4)
    # 31.6–35: Dill's idea; the map; arrow UP
    place(mix, ding(), V.T_DIDEA, 0.5)
    place(mix, shimmer(0.8), V.T_DIDEA, 0.35)
    place(mix, E.fanfare(), V.T_DIDEA + 0.3, 0.35)
    place(mix, ooh(1.0), V.T_DIDEA + 0.5, 0.3)
    place(mix, pop(), V.T_MAP, 0.5)
    place(mix, sweep(300, 900, 0.45, vdepth=0) * 0.3, V.T_UNROLL, 0.35)     # map unfurl
    place(mix, whoosh(0.45), V.T_UNROLL, 0.4)
    mix += A2.war_drum(V.T_ARROW - 0.4, 3, 0.25) * 0.5
    place(mix, thud(), V.T_ARROW, 0.8)
    place(mix, chord([55, 59, 62, 67], 1.0), V.T_ARROW, 0.3)
    place(mix, E.gib(4, 54, spread=6, syl=0.08, bright=1.0), V.T_ARROW + 0.3, 0.5)
    place(mix, E.fanfare(), V.T_SWORD, 0.4)
    # 35.4–38.5: Chip goes see-through; push in; DUNs
    place(mix, sweep(1800, 2600, 0.18, vdepth=0) * 0.5, V.T_SEE, 0.5)
    place(mix, sweep(900, 400, 0.5, vdepth=0) * 0.2, V.T_SEE + 0.3, 0.3)
    place(mix, E.gib(1, 48, spread=1, syl=0.2, bright=0.3), V.T_SEE + 0.3, 0.4)     # gulp
    tmp = np.zeros(N); place(tmp, icy(2.0), V.T_PUSH, 0.4); mix += tmp
    for k in range(4):
        place(mix, tinkle() * 0.5, V.T_PUSH + 0.6 + 0.08 * k, 0.3)
    for k, d in enumerate(V.DUNS):
        place(mix, dun([43, 42, 38][k]), d, 1.1)
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.9
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
