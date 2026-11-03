"""Sound for FRIDGE KINGDOM Ep4 "Knock Knock" (variant B: cold open, no title fanfare)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
from ep3_audio import knock, big_thump, tick
from audio import SR, tarr, midi, place, plink, sweep, whoosh, zip_sfx, bonk, thud, pop, marimba, boing, ding, lowpass, munch, pluck

DUR = 39.6
N = int(SR * DUR)
E.N = N
rng = np.random.default_rng(44)


def scream(at, mix, gain=0.5):
    place(mix, sweep(900, 1500, 0.35, vib=18, vdepth=0.06, shape="square"), at, gain * 0.5)
    place(mix, E.gib(2, 86, spread=2, syl=0.1, bright=0.9), at, gain * 0.6)


def clonk():
    t = tarr(0.15)
    return (np.sin(2 * np.pi * 520 * t) + 0.5 * np.sin(2 * np.pi * 1310 * t)) * np.exp(-t * 35) * 0.7


def crack():
    t = tarr(0.25)
    n = rng.standard_normal(len(t)); n = n - lowpass(n, 0.5)
    out = n * np.exp(-t * 30) * 1.2
    place(out, clonk(), 0, 0.3)
    return out


def trombone(at, mix):
    for i, (m, d) in enumerate([(55, 0.35), (54, 0.35), (53, 0.35), (52, 1.0)]):
        s = sweep(midi(m), midi(m) * 0.995, d, vib=6 if i == 3 else 0.01, vdepth=0.03 if i == 3 else 0.0, shape="square")
        place(mix, lowpass(s, 0.15) * 2.2, at + i * 0.37, 0.4)


def cello(d=3.0, m=36):
    t = tarr(d)
    f = midi(m) * (1 + 0.006 * np.sin(2 * np.pi * 5 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = sum(np.sin(k * ph) / k for k in range(1, 8))
    env = np.minimum(1, t / 0.4) * np.minimum(1, (d - t) / 0.6)
    return lowpass(s * env, 0.08) * 0.8


def chord(ms, d=2.0):
    out = np.zeros(int(SR * d))
    for m in ms:
        t = tarr(d)
        f = midi(m) * (1 + 0.004 * np.sin(2 * np.pi * 5 * t + m))
        ph = 2 * np.pi * np.cumsum(f) / SR
        s = sum(np.sin(k * ph) / k ** 1.5 for k in range(1, 5))
        place(out, s * np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.6), 0, 0.12)
    return out


def drip():
    return plink(midi(84 + rng.integers(-3, 4))) * 0.6


def build(path):
    mix = E.hum() * 0.6
    # 0–5: split screen. knock, scream, knock, scream (the first frame is mid-scream)
    for t0 in [-0.25, 0.75, 1.75, 2.75, 3.55, 4.3]:
        if t0 >= 0:
            place(mix, knock(), t0, 1.0); place(mix, bonk(), t0, 0.25)
        scream(max(0, t0 + 0.1), mix, 0.55)
    place(mix, E.gib(5, 60, spread=5, syl=0.08), 1.1, 0.5)      # Dill, furious
    place(mix, E.gib(6, 58, spread=6, syl=0.07), 3.0, 0.5)
    # 5–11: egg wall
    for t0 in (5.3, 7.4, 9.55, 10.45):
        place(mix, knock(), t0, 0.7)
    place(mix, E.gib(3, 82, spread=2, syl=0.07), 5.35, 0.45)
    mix += E.bouncy(5.55, 9.6, base=64, gain=0.14)
    for i in range(6):
        place(mix, clonk(), 5.55 + i * 0.68 + 0.68, 0.8)
    place(mix, E.gib(8, 78, spread=3, syl=0.06, bright=0.4), 9.6, 0.4)   # nervous mumbling
    place(mix, E.squeak(0.25), 10.4, 0.25)                                 # (the Duck, unnoticed)
    # 11–17.7: the climb
    place(mix, E.gib(4, 58, spread=4, syl=0.1), 11.1, 0.5)
    for t0 in (12.3, 13.1, 13.8):
        place(mix, E.gib(1, 62, spread=2, syl=0.12), t0 - 0.4, 0.45)       # grunt
        place(mix, thud(), t0, 0.5)
    place(mix, E.fanfare(), 13.85, 0.35)                                   # tiny victory
    place(mix, sweep(500, 300, 1.4, vib=5, vdepth=0.02), 14.1, 0.25)     # magnet slides
    place(mix, big_thump(), 15.5, 0.8)                                     # magnet thunk
    trombone(15.55, mix)
    place(mix, E.drumroll(1.6), 16.0, 0.6)
    place(mix, sweep(400, 1200, 0.5), 17.1, 0.3)                           # leap
    place(mix, pop(), 17.6, 0.7)
    # 17.7–22: straining on the handle. creak. nothing.
    place(mix, E.gib(14, 52, spread=2, syl=0.16, bright=0.8), 18.0, 0.45)
    for t0 in (18.6, 19.9, 21.1):
        place(mix, sweep(160, 120, 0.8, vdepth=0.0), t0, 0.25)
    # 21.6–24.7: the Hand. choir. whoosh. flung inside.
    place(mix, E.choir(3.4), 21.7, 0.8)
    place(mix, whoosh(1.4), 22.4, 0.7)
    place(mix, sweep(600, 1600, 0.6, vib=10), 24.0, 0.35)                  # wheee
    place(mix, whoosh(0.7), 24.6, 0.6)
    # 25.15: wrecking ball through the egg wall
    for k in range(3):
        place(mix, crack(), 25.15 + k * 0.12, 1.0)
    place(mix, big_thump(), 25.15, 0.9)
    place(mix, E.splat(), 25.6, 1.0); place(mix, E.splat(), 25.8, 0.7)
    for k in range(6):
        place(mix, munch(), 25.3 + k * 0.1, 0.3)                           # shell bits
    place(mix, E.gib(3, 64, spread=3, syl=0.1), 26.7, 0.4)                 # dazed
    # 28.6–32.8: hug, crown, dignity
    place(mix, chord([60, 64, 67, 72], 2.4), 28.6, 1.0)
    place(mix, chord([65, 69, 72, 77], 2.2), 30.8, 1.0)
    for k in range(10):
        place(mix, drip(), 27.2 + k * 0.55, 0.5)
    for k, m in enumerate([72, 76, 79, 84]):
        place(mix, plink(midi(m)), 32.0 + k * 0.1, 0.4)
    place(mix, E.gib(2, 60, spread=1, syl=0.2), 32.2, 0.3)                 # "ahem"
    # 32.9: door closes. silence. low cello. the Duck.
    place(mix, thud(), 32.95, 0.6)
    place(mix, cello(4.0, 36), 33.8, 0.9)
    place(mix, cello(3.0, 37), 34.6, 0.5)
    place(mix, sweep(1200, 300, 0.25, vdepth=0.0), 34.6, 0.3)              # gasp
    place(mix, marimba(midi(57), 1.5), 36.4, 0.35)
    place(mix, E.squeak(0.35), 38.95, 0.5)
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.9
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
