"""Sound for FRIDGE KINGDOM Ep15 "Something Is Melting" (variant A: title card first)."""
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
from ep7_audio import gasp, peep, spy
from ep8_audio import shimmer, dun
from ep10_audio import icy, sigh
from ep11_audio import harp, ooh, scratch, plip
from ep12_audio import flaps
from ep13_audio import tinkle, creak
from audio import SR, tarr, midi, place, plink, sweep, whoosh, thud, pop, marimba, ding, lowpass, sting, boing
import ep15 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A2.N = N
A6.N = N
rng = np.random.default_rng(1515)


def chatter(d):
    """Tiny teeth chattering: fast clicks."""
    out = np.zeros(int(SR * d) + SR)
    at = 0.0
    while at < d:
        t = tarr(0.02)
        place(out, np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 300) + rng.standard_normal(len(t)) * np.exp(-t * 250) * 0.4, at, 0.5)
        at += 0.045
    return out[:int(SR * d)]


def rattle(d):
    out = np.zeros(int(SR * d) + SR)
    at = 0.0
    while at < d:
        t = tarr(0.05)
        s = sum(np.sin(2 * np.pi * f * t) for f in (310, 790, 1460)) * np.exp(-t * 70)
        place(out, s * 0.3 + rng.standard_normal(len(t)) * np.exp(-t * 90) * 0.4, at, float(rng.uniform(0.5, 1.0)))
        at += float(rng.uniform(0.03, 0.06))
    return out[:int(SR * d)]


def sniff(d=0.55):
    """A huge, low, breathy sniff from inside the vent."""
    t = tarr(d)
    n = rng.standard_normal(len(t))
    band = lowpass(n, 0.06) - lowpass(n, 0.01)
    env = np.minimum(1, t / 0.12) * np.minimum(1, (d - t) / 0.08)
    return band * env * 3.0 + np.sin(2 * np.pi * 70 * t) * env * 0.2


def squeaky(d=0.18):
    """Napkin-on-ice squeak."""
    t = tarr(d)
    f = 1500 + 400 * np.sin(np.pi * t / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sign(np.sin(ph)) * 0.25 * np.sin(np.pi * t / d)


def build(path):
    mix = E.hum() * 0.5
    # 0–2: title card; drips
    for t0 in (0.2, 0.6, 1.0, 1.35):
        place(mix, plip(), t0 + 0.4, 0.35)
    place(mix, chord([62, 66, 69, 74], 1.6), 0.2, 0.15)
    # 2–6.2: drips on Dill
    place(mix, chord([55, 59, 62, 67], 0.8), V.T_START + 0.1, 0.2)        # proud guard
    for i, d in enumerate(V.DRIPS):
        place(mix, plip(), d, 0.8)
        place(mix, sweep(1200, 900, 0.08, vdepth=0) * 0.2, d - 0.3, 0.2)
    place(mix, E.gib(2, 58, spread=5, syl=0.08, bright=0.8), V.DRIPS[1] + 0.15, 0.45)
    place(mix, E.gib(3, 54, spread=6, syl=0.07, bright=1.0), V.DRIPS[2] + 0.15, 0.55)
    mix += A2.war_drum(V.T_FIST, 3, 0.25) * 0.5
    place(mix, E.gib(5, 50, spread=7, syl=0.07, bright=1.0), V.T_FIST + 0.1, 0.6)   # GRRR
    # 6.2–11.6: footprints; detective tiptoe
    place(mix, ding(), V.T_SPOT, 0.4)
    place(mix, E.gib(2, 68, spread=4, syl=0.08, bright=0.7), V.T_SPOT + 0.1, 0.45)
    place(mix, shimmer(0.9), V.T_SPOT + 0.1, 0.25)
    spy(V.T_FOLLOW, V.T_ARRIVE, mix, gain=0.32)
    at = V.T_FOLLOW + 0.1
    while at < V.T_ARRIVE:
        place(mix, plink(midi(91)) * 0.25, at, 0.25); at += 0.44
    # 11.8–14.2: the lid chatters; Crumb is plonked in front; CLANG
    place(mix, chatter(V.T_TIP - V.T_CHATTER), V.T_CHATTER, 0.6)
    place(mix, E.gib(3, 66, spread=5, syl=0.06, bright=0.9), V.T_GRAB, 0.4)
    place(mix, whoosh(0.6), V.T_GRAB, 0.45)
    place(mix, thud(), V.T_PLONK, 0.6)
    place(mix, creak(0.35), V.T_TIP, 0.35)
    place(mix, A6.clang(), V.T_CLANG, 0.7)
    for k in range(3):
        place(mix, gasp(), V.T_GASP + 0.25 + 0.07 * k, 0.45)
    place(mix, sting(), V.T_GASP + 0.25, 0.4)
    place(mix, sweep(1800, 2600, 0.18, vdepth=0) * 0.5, V.T_GASP + 0.3, 0.5)      # eep!
    place(mix, chatter(V.T_SOFT - V.T_COWER), V.T_COWER, 0.5)
    # 16–22: hug, melt, mop, wring, ta-da
    harp(V.T_HUG, mix, gain=0.3)
    place(mix, chord([60, 64, 67, 72], 1.6), V.T_HUG + 0.1, 0.22)
    place(mix, ooh(1.0), V.T_HUG + 0.2, 0.35)
    for k in range(6):
        place(mix, plip(), V.T_MELT + 0.3 + 0.25 * k, 0.4)
    place(mix, sweep(700, 300, 1.0, vdepth=0.02) * 0.25, V.T_MELT + 0.4, 0.3)     # melting slide-down
    place(mix, E.gib(3, 70, spread=6, syl=0.06, bright=1.0), V.T_PANIC, 0.55)    # panic
    place(mix, whoosh(0.3), V.T_NAPKIN, 0.4)
    for k in range(4):
        place(mix, squeaky(), V.T_MOP + 0.45 * k + 0.1, 0.6)
    for k in range(5):
        place(mix, plip(), V.T_WRING + 0.35 + 0.12 * k, 0.35)
    place(mix, sweep(300, 900, 0.6, vdepth=0) * 0.3, V.T_WRING + 0.4, 0.3)       # filling back up
    place(mix, boing(), V.T_TADA - 0.05, 0.4)
    for i, m in enumerate([72, 76, 79, 84]):
        place(mix, marimba(midi(m), 0.4), V.T_TADA + 0.08 * i, 0.4)
    # 22.5–27.5: Peep copies the shiver; Dill sulks
    flaps(mix, V.T_PDOWN, V.T_PDOWN + 0.5, 0.06, 0.4)
    place(mix, peep(), V.T_PDOWN + 0.5, 0.45)
    place(mix, chatter(V.T_PCOPY - V.T_SHIV), V.T_SHIV, 0.5)
    place(mix, E.gib(2, 76, spread=3, syl=0.05, bright=0.6), V.T_SHIV + 0.2, 0.3)   # tiny brrr
    flaps(mix, V.T_PCOPY, V.T_GIGGLE + 0.3, 0.04, 0.5)
    place(mix, chatter(V.T_GIGGLE + 0.3 - V.T_PCOPY) * 1.8, V.T_PCOPY, 0.6)
    place(mix, E.gib(4, 80, spread=4, syl=0.07, bright=1.0), V.T_PCOPY + 0.1, 0.5)   # BRRRR (peep-voiced)
    for k in range(4):
        place(mix, E.gib(1, 82 + (k % 2) * 3, spread=2, syl=0.07, bright=0.6), V.T_GIGGLE + 0.18 * k, 0.35)   # hee hee
    place(mix, sweep(400, 250, 0.3, vdepth=0) * 0.4, V.T_CROSS + 0.2, 0.4)        # hmph
    place(mix, E.gib(1, 48, spread=2, syl=0.15, bright=0.5), V.T_CROSS + 0.25, 0.5)
    flaps(mix, V.T_PUP, V.T_PUP + 0.5, 0.06, 0.35)
    # 27.6–31: the frost drawing
    tmp = np.zeros(N); place(tmp, drone(V.T_RATTLE - V.T_DRAW), V.T_DRAW, 0.3); mix += tmp
    at = V.T_DRAW
    while at < V.T_DRAW_END:
        place(mix, scratch(0.12), at, 0.6); at += 0.18
    # 31.2: the Duck's one motion
    place(mix, E.squeak(0.5), V.T_DUCK + 0.2, 0.7)
    # 32.6: the drawing's eyes glint; brrr
    for i, m in enumerate([84, 88, 91, 96]):
        place(mix, plink(midi(m)), V.T_GLINT + 0.06 * i, 0.35)
    place(mix, chord([50, 53, 56, 59], 1.0), V.T_GLINT, 0.2)
    for k in range(3):
        place(mix, E.gib(2, 60 + 4 * k, spread=3, syl=0.06, bright=0.5), V.T_GLINT + 0.3 + 0.12 * k, 0.25)
    # 33.6–38.5: the vent rattles; searchlight; sniffs; found
    place(mix, rattle(V.T_FIND + 0.5 - V.T_RATTLE), V.T_RATTLE, 0.55)
    for k in range(3):
        place(mix, gasp(), V.T_RATTLE + 0.1 + 0.06 * k, 0.4)
    tmp = np.zeros(N); place(tmp, icy(4.8), V.T_BEAM, 0.45); mix += tmp
    place(mix, sweep(300, 600, 0.9, vdepth=0) * 0.25, V.T_BEAM, 0.3)
    place(mix, whoosh(0.4), V.T_HIDE, 0.4)
    for s in V.SNIFFS:
        place(mix, sniff(0.55), s, 0.8)
    place(mix, sting(), V.T_FIND, 0.6)
    for k in range(6):
        place(mix, tinkle() * 0.5, V.T_FIND + 0.08 * k, 0.3)
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
