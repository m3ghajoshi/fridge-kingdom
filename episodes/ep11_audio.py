"""Sound for FRIDGE KINGDOM Ep11 "Wilt's Secret" (variant A: title card + fanfare)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
from ep3_audio import tick
from ep4_audio import chord, drip
from ep5_audio import violin_tremolo, drone
import ep6_audio as A6
from ep6_audio import shhhk, wind
from ep7_audio import gasp, peep
from ep8_audio import shimmer, dun, peck
from ep10_audio import sigh, icy
from audio import SR, tarr, midi, place, plink, sweep, whoosh, thud, pop, marimba, boing, ding, lowpass, sting
import ep11 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A6.N = N
rng = np.random.default_rng(1111)


def harp(start, mix, notes=(60, 64, 67, 71, 72, 76, 79, 83, 84, 88), step=0.07, gain=0.3):
    for i, m in enumerate(notes):
        place(mix, marimba(midi(m), 0.9), start + i * step, gain)


def ooh(d=1.6):
    """Soft 'ooooh' crowd: a few detuned vowel tones."""
    t = tarr(d)
    out = np.zeros(len(t))
    for m in (60, 64, 67, 72):
        f = midi(m) * (1 + 0.004 * rng.standard_normal())
        ph = 2 * np.pi * f * t + 0.3 * np.sin(2 * np.pi * 5 * t)
        out += np.sin(ph) + 0.3 * np.sin(2 * ph)
    env = np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.5)
    return lowpass(out * env, 0.2) * 0.25


def scratch(d=0.12):
    t = tarr(d)
    n = rng.standard_normal(len(t)); n = n - lowpass(n, 0.4)
    return n * np.sin(np.pi * t / d) * 0.35


def plip():
    t = tarr(0.25)
    f = 900 + 1400 * np.exp(-t * 25)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 18) * 0.7


def build(path):
    mix = E.hum() * 0.5
    # 0–2: title fanfare
    place(mix, E.fanfare(), 0.1, 1.0)
    place(mix, E.gib(4, 64, spread=3, syl=0.07, bright=0.2), 1.0, 0.3)       # Wilt's shy giggle
    # 2–6.3: shelf. heroic leap, Peep copies, falls
    place(mix, sweep(300, 900, 0.5, vdepth=0) * 0.6, V.T_DLEAP, 0.5)
    place(mix, whoosh(0.5), V.T_DLEAP, 0.4)
    place(mix, thud(), V.T_DLAND, 0.7)
    place(mix, E.fanfare(), V.T_DLAND + 0.05, 0.5)
    place(mix, peep(), V.T_PCROUCH, 0.6)
    place(mix, sweep(400, 1800, 0.7, vdepth=0) * 0.6, V.T_PLEAP, 0.5)
    place(mix, peep(), V.T_PLEAP + 0.2, 0.5); place(mix, peep(), V.T_PLEAP + 0.4, 0.5)
    place(mix, thud(), V.T_PLAND, 0.4)
    place(mix, violin_tremolo(0.45, 88) * 0.8, V.T_PLAND, 0.35)
    place(mix, sweep(1400, 300, 0.45, vdepth=0) * 0.6, V.T_PFALL, 0.55)    # falling slide whistle
    place(mix, shhhk(), V.T_SHK, 1.0); place(mix, thud(), V.T_SHK + 0.05, 0.6)
    place(mix, E.gib(3, 70, spread=4, syl=0.07), V.T_SHK + 0.1, 0.45)       # "PEEP?!"
    place(mix, sweep(1500, 400, 0.5, vdepth=0) * 0.6, V.T_CDIVE, 0.5)
    place(mix, sweep(1300, 350, 0.5, vdepth=0) * 0.6, V.T_DDIVE, 0.45)
    # 6.3–9: the drawer. land, sigh, hug
    mix += wind(V.T_CUT, 9.0) * 0.6
    place(mix, thud(), V.T_CLAND, 0.6); place(mix, thud(), V.T_DIL_LAND, 0.9)
    place(mix, sigh(52), 6.9, 0.6)
    place(mix, peep(), 7.4, 0.5)
    for i, m in enumerate([72, 76, 79]):
        place(mix, marimba(midi(m), 0.5), 7.4 + i * 0.2, 0.25)
    # 9–12.2: the doodle. who did this?!
    place(mix, plink(midi(96)), V.T_NOTICE, 0.45); place(mix, plink(midi(100)), V.T_NOTICE + 0.1, 0.45)
    place(mix, sting(), V.T_POINT, 0.7)
    place(mix, E.gib(6, 58, spread=5, syl=0.08, bright=0.8), V.T_POINT + 0.1, 0.5)
    place(mix, E.gib(5, 60, spread=6, syl=0.07, bright=0.8), V.T_WHO, 0.5)
    # 12.2–14.4: Wilt raises the twig, shy
    place(mix, ding(), V.T_TWIG + 0.3, 0.4)
    place(mix, E.gib(5, 66, spread=3, syl=0.09, bright=0.1), V.T_TWIG + 0.6, 0.4)
    for t0 in (V.T_TWIG + 0.3, V.T_TWIG + 0.4, V.T_TWIG + 0.5):
        place(mix, gasp(), t0, 0.35)
    # 14.4–17.2: shuffle over, pull the curtain
    for t0 in np.arange(V.T_WALK, V.T_PULL, 0.3):
        place(mix, plink(midi(76 + int(t0 * 7) % 5)), float(t0), 0.15)
    place(mix, sweep(200, 500, 1.4, vdepth=0) * 0.25, V.T_PULL, 0.4)
    place(mix, whoosh(1.2), V.T_PULL, 0.3)
    # 17.2–23.4: the mural. harp, ooooh, highlights, the Duck turns
    harp(V.T_OPEN - 0.3, mix)
    place(mix, ooh(2.0), V.T_OPEN + 0.4, 1.0)
    place(mix, chord([60, 64, 67, 71], 5.5), V.T_OPEN, 0.5)
    for k, th in enumerate(V.T_HL):
        place(mix, ding(), th, 0.3)
        place(mix, marimba(midi(84 + 3 * k), 0.6), th + 0.1, 0.3)
    place(mix, E.squeak(0.4), V.T_DUCK, 0.5)
    place(mix, E.gib(3, 72, spread=3, syl=0.08), V.T_DUCK + 0.8, 0.3)
    # 23.4–30: Peep scribbles; Crumb melts
    place(mix, peep(), V.T_PEEP_GO, 0.5)
    at = V.T_SCRATCH[0]
    while at < V.T_SCRATCH[1]:
        place(mix, scratch(), at, 0.7); place(mix, peck(), at, 0.3)
        at += 0.22
    place(mix, ding(), V.T_PROUD, 0.5); place(mix, peep(), V.T_PROUD + 0.1, 0.6)
    harp(V.T_MELT, mix, notes=(72, 76, 79, 84, 79, 76, 84), step=0.12, gain=0.25)
    place(mix, E.gib(4, 76, spread=2, syl=0.14, bright=0.1), V.T_MELT + 0.3, 0.4)  # "awww"
    place(mix, chord([65, 69, 72, 76], 2.0), V.T_MELT, 0.5)
    # 30–33.6: the crowned shadow. low drone, glint
    place(mix, drone(3.8), V.T_POINTUP, 0.9)
    place(mix, violin_tremolo(3.2, 52) * 0.8, V.T_POINTUP + 0.4, 0.3)
    place(mix, whoosh(0.8), V.T_POINTUP + 0.4, 0.3)
    place(mix, sting(), V.T_GLINT, 0.7)
    place(mix, shimmer(1.0), V.T_GLINT, 0.6)
    # 33.6–36.4: shivers, pfft, the drip
    tmp = np.zeros(N); place(tmp, icy(2.0), V.T_DOWN, 0.7); mix += tmp
    for t0 in np.arange(V.T_DOWN + 0.3, V.T_PFFT, 0.06):     # teeth chattering
        place(mix, tick(3000 + int(rng.integers(-300, 300))), float(t0), 0.2)
    place(mix, E.gib(3, 56, spread=2, syl=0.1, bright=0.9), V.T_PFFT + 0.1, 0.45)
    place(mix, plip(), V.T_PLIP, 1.0)
    place(mix, drip(), V.T_PLIP + 0.05, 0.6)
    for k, d in enumerate(V.DUNS):
        place(mix, dun([43, 42, 38][k]), d, 1.1)
    for t0 in (V.T_PLIP + 0.9, V.T_PLIP + 1.4, V.T_PLIP + 1.9):
        place(mix, plip(), t0, 0.35)
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.9
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
