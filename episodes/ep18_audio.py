"""Sound for FRIDGE KINGDOM Ep18 "The Squeak Strategy" (variant B: cold open)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
import ep5_audio as A5
from ep5_audio import cricket_chirp, violin_tremolo, drone, minor_fanfare
from ep7_audio import gasp, peep, echo
from ep8_audio import shimmer, dun
from ep10_audio import icy, sigh
from ep13_audio import tok
from ep15_audio import chatter
from audio import SR, tarr, midi, place, plink, pluck, sweep, whoosh, thud, pop, ding, sting, boing, bonk, lowpass
import ep18 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A5.N = N
rng = np.random.default_rng(1818)


def scratch():
    t = tarr(0.45)
    f = 900 * np.exp(-t * 4) + 200
    ph = 2 * np.pi * np.cumsum(f) / SR
    n = rng.standard_normal(len(t))
    return (np.sign(np.sin(ph)) * 0.5 + n * 0.5) * np.exp(-t * 5) * 0.6


def footstep():
    t = tarr(0.5)
    s = np.sin(2 * np.pi * (45 + 30 * np.exp(-t * 10)) * t) * np.exp(-t * 7)
    s += lowpass(rng.standard_normal(len(t)), 0.05) * np.exp(-t * 14) * 1.5
    return s


def wind(d):
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.03) * 3.0
    howl = np.sin(2 * np.pi * np.cumsum(500 + 250 * np.sin(2 * np.pi * 0.7 * t)) / SR) * 0.25
    env = np.minimum(1, t / 0.4) * np.minimum(1, (d - t) / 0.5)
    return (n + howl * (0.5 + 0.5 * np.sin(2 * np.pi * 0.5 * t))) * env * 0.4


def minor_choir(d=2.0):
    t = tarr(d)
    s = np.zeros_like(t)
    for m in (57, 60, 64, 69, 72):           # A minor
        f = midi(m) * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * t + m))
        ph = 2 * np.pi * np.cumsum(f) / SR
        s += sum(np.sin(k * ph) / k for k in range(1, 6))
    env = np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.6)
    return lowpass(s * env, 0.2) * 0.35


def scream(d, base):
    t = tarr(d)
    f = midi(base) * (1 + 0.08 * np.sin(2 * np.pi * 7 * t)) * (1 + 0.15 * t / d)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sign(np.sin(ph))
    return s * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.2) * 0.3


def build(path):
    mix = E.hum() * 0.5
    # 0–2.5: Crumb lands on the Duck. Nothing.
    place(mix, whoosh(0.4), 0.0, 0.35)
    place(mix, E.gib(2, 64, spread=6, syl=0.08, bright=0.8), 0.0, 0.4)
    place(mix, thud(), V.T_CLAND, 0.9)
    place(mix, boing() * 0.4, V.T_CLAND + 0.05, 0.3)                 # jello wobble
    for k in range(3):
        place(mix, cricket_chirp(), 1.2 + 0.3 * k, 0.6)
    place(mix, E.gib(2, 62, spread=2, syl=0.1, bright=0.4), 1.6, 0.35)
    place(mix, sweep(900, 300, 0.45, vdepth=0) * 0.3, V.T_CSLIDE, 0.4)   # shhk slide
    # 2.6–5.5: Peep bounces x3
    place(mix, peep(), V.T_PHOP, 0.5)
    for i, b in enumerate(V.P_BOUNCE):
        place(mix, boing(), b + 0.02, 0.5 + 0.1 * i)
        place(mix, peep(), b + 0.25, 0.35)
    for k in range(2):
        place(mix, cricket_chirp(), 4.65 + 0.3 * k, 0.6)
    place(mix, peep() * 0.7, V.T_PHOPOFF, 0.35)
    # 6–9: the pickle pile
    for k, j in enumerate(V.PK_JUMP):
        place(mix, whoosh(0.3), j, 0.25)
        place(mix, thud(), j + V.PK_FALL, 0.7)
        place(mix, E.gib(1, 66 + 2 * k, spread=2, syl=0.08, bright=0.6), j + 0.05, 0.3)
    place(mix, E.gib(3, 60, spread=8, syl=0.1, bright=0.7), 7.95, 0.4)       # whoa-
    for k in range(5):
        place(mix, boing(), V.T_TOPPLE + 0.4 + 0.08 * k, 0.35)
    # 9–10.5: Grandma's cane
    for p in V.GPOKES:
        place(mix, tok(), p, 0.6)
    place(mix, cricket_chirp(), 10.3, 0.5)
    place(mix, E.gib(1, 46, spread=1, syl=0.2, bright=0.3), V.T_HMPH, 0.5)
    # 10.9–13: Dill's dance (Ep 5 callback): funky bass, record scratch
    mix += A5.funk(V.T_DANCE, V.T_SCRATCH, gain=0.35)
    place(mix, scratch(), V.T_SCRATCH, 0.8)
    place(mix, cricket_chirp(), V.T_SCRATCH + 0.3, 0.6)
    # 13.5: everyone gives up
    for k, x in enumerate((0, 0.1, 0.18, 0.25, 0.32)):
        place(mix, thud() * 0.5, V.T_FLOP + 0.3 + x, 0.35)
    place(mix, sigh(52), V.T_FLOP + 0.3, 0.5)
    # deliberate silence ... then the squeak
    place(mix, E.squeak(0.7), V.T_SQUEAK, 1.0)
    place(mix, sting(), V.T_SQUEAK + 0.25, 0.45)
    place(mix, gasp(), V.T_UP, 0.6)
    # footsteps
    for s in V.STEPS:
        place(mix, footstep(), s, 1.0)
    place(mix, violin_tremolo(V.T_OPEN - V.STEPS[0], 70), V.STEPS[0], 0.35)
    # the door opens: choir in a minor key, the Hand
    place(mix, minor_choir(2.2), V.T_OPEN, 0.55)
    place(mix, whoosh(0.8), V.T_HDOWN, 0.35)
    place(mix, E.fanfare(), V.T_CHARGE, 0.35)
    place(mix, E.gib(3, 58, spread=8, syl=0.12, bright=1.0), V.T_CHARGE + 0.05, 0.6)   # HYAAA
    place(mix, E.squeak(0.25), V.T_BOOP, 0.6)
    for k, d in enumerate((0, 0.1, 0.18, 0.28)):
        place(mix, whoosh(0.3), V.T_LEAP + d, 0.25)
        place(mix, pop() * 0.5, V.T_GRAB + d, 0.3)
    place(mix, whoosh(0.7), V.T_LIFT, 0.5)
    # outside: the freezer
    place(mix, thud() * 0.6, V.T_MCLOSE, 0.5)
    place(mix, sweep(250, 600, 0.9, vdepth=0) * 0.2, V.T_RISE, 0.3)
    place(mix, sweep(200, 120, 0.5, vdepth=0) * 0.3, V.T_FOPEN, 0.4)           # seal pop / creak
    place(mix, pop(), V.T_FOPEN, 0.5)
    place(mix, wind(V.T_EXT2 - V.T_FOPEN), V.T_FOPEN, 0.9)
    place(mix, minor_choir(2.0), V.T_FOPEN + 0.1, 0.4)
    place(mix, icy(3.0), V.T_FOPEN + 0.2, 0.5)
    # close-up: screams, slip, fall
    place(mix, scream(1.6, 72), V.T_CU + 0.2, 0.35)
    place(mix, scream(1.4, 64), V.T_CU + 0.3, 0.3)
    place(mix, chatter(1.5), V.T_CU + 0.4, 0.3)
    place(mix, sweep(1200, 1500, 0.3, vdepth=0) * 0.25, V.T_SLIP - 0.4, 0.3)
    place(mix, pop(), V.T_SLIP + 0.25, 0.7)
    place(mix, gasp(), V.T_SLIP + 0.35, 0.5)
    place(mix, scream(1.5, 70), V.T_FALL + 0.05, 0.4)
    place(mix, sweep(1500, 300, 1.4, vdepth=0.02) * 0.4, V.T_FALL + 0.1, 0.4)
    place(mix, peep(), V.T_FALL + 0.5, 0.35)
    # the SLAM
    place(mix, whoosh(0.3), V.T_SLAM - 0.3, 0.4)
    place(mix, bonk() * 0.5, V.T_SLAM, 0.5)
    place(mix, thud(), V.T_SLAM, 1.0)
    place(mix, footstep(), V.T_SLAM, 0.9)
    # total white: soft wind, echoing peeps, the eye
    place(mix, icy(V.END_T - V.T_WHITE), V.T_WHITE, 0.35)
    for i, p in enumerate(V.PEEPS):
        place(mix, echo(peep(), delays=(0.25, 0.5, 0.75), decay=0.45), p, 0.5 * (0.75 ** i))
    place(mix, plink(midi(96)), V.T_EYES + 0.5, 0.3)
    place(mix, drone(V.END_T - V.T_BIGEYE), V.T_BIGEYE, 0.5)
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
