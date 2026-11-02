"""Sound for FRIDGE KINGDOM Ep1 — all synthesized."""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import audio as A
from audio import SR, tarr, midi, place, pluck, marimba, plink, sweep, whoosh, bonk, thud, pop, lowpass

DUR = 31.0
N = int(SR * DUR)
rng = np.random.default_rng(3)


def gib(n, base, spread=5, syl=0.09, gap=0.03, bright=0.6):
    """Wordless gibberish 'voice': pitched syllables with a vowel-ish wobble."""
    out = np.zeros(int(SR * n * (syl + gap) + SR * 0.2))
    for i in range(n):
        f = midi(base + rng.integers(-spread, spread + 1))
        t = tarr(syl)
        ff = f * (1 + 0.08 * np.sin(2 * np.pi * 18 * t))
        ph = 2 * np.pi * np.cumsum(ff) / SR
        s = bright * np.sign(np.sin(ph)) * 0.35 + (1 - bright) * np.sin(ph) + 0.4 * np.sin(2 * ph)
        env = np.sin(np.pi * t / syl) ** 0.7
        place(out, lowpass(s * env, 0.35), i * (syl + gap), 0.8)
    return out


def choir(d=1.8):
    t = tarr(d)
    s = np.zeros_like(t)
    for m in (57, 64, 69, 73, 76):  # A major, heavenly
        f = midi(m) * (1 + 0.006 * np.sin(2 * np.pi * 5.5 * t + m))
        ph = 2 * np.pi * np.cumsum(f) / SR
        s += sum(np.sin(k * ph) / k for k in range(1, 6))
    env = np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.5)
    return lowpass(s * env, 0.2) * 0.35


def hum():
    t = np.arange(N) / SR
    s = 0.5 * np.sin(2 * np.pi * 58 * t) + 0.3 * np.sin(2 * np.pi * 116 * t)
    s += lowpass(rng.standard_normal(N), 0.02) * 0.6
    return s * 0.12


def drumroll(d):
    out = np.zeros(int(SR * (d + 0.2)))
    k, at = 0, 0.0
    while at < d:
        tt = tarr(0.05)
        hit = rng.standard_normal(len(tt)) * np.exp(-tt * 70) + np.sin(2 * np.pi * 190 * tt) * np.exp(-tt * 40)
        place(out, hit, at, 0.25 + 0.75 * at / d)
        at += 0.045
    return out * 0.6


def crash():
    t = tarr(1.4)
    n = rng.standard_normal(len(t))
    n = n - lowpass(n, 0.3)
    return n * np.exp(-t * 3) * 0.7


def hiss(d=0.4):
    t = tarr(d)
    n = rng.standard_normal(len(t)); n = n - lowpass(n, 0.5)
    return n * np.sin(np.pi * t / d) * 0.35


def twang():
    t = tarr(0.6)
    f = 260 * np.exp(-t * 2.5) + 80
    ph = 2 * np.pi * np.cumsum(f * (1 + 0.05 * np.sin(2 * np.pi * 22 * t))) / SR
    return np.sign(np.sin(ph)) * 0.3 * np.exp(-t * 5) + np.sin(ph) * 0.4 * np.exp(-t * 5)


def splat():
    t = tarr(0.35)
    n = lowpass(rng.standard_normal(len(t)), 0.15) * 2.5
    out = n * np.exp(-t * 14)
    th = thud(); out[: len(th)] += 0.6 * th
    return out


def squeak(d=0.9):
    """Slow, unsettling rubber-duck squeak."""
    t = tarr(d)
    f = 700 + 500 * np.sin(np.pi * t / d) ** 1.5
    f *= 1 + 0.03 * np.sin(2 * np.pi * 9 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sign(np.sin(ph))
    env = np.minimum(1, t / 0.1) * np.minimum(1, (d - t) / 0.2)
    return s * env * 0.4


def fanfare():
    out = np.zeros(int(SR * 1.2))
    for i, (ms, d) in enumerate([((65, 69, 72), 0.18), ((65, 69, 72), 0.18), ((70, 74, 77), 0.6)]):
        at = [0, 0.2, 0.42][i]
        for m in ms:
            t = tarr(d)
            ph = 2 * np.pi * midi(m) * t
            s = sum(np.sin(k * ph) / k for k in range(1, 7)) * np.minimum(1, t / 0.02) * np.exp(-t * 2)
            place(out, s, at, 0.18)
    return out


def bouncy(start, end, base=60, gain=0.3):
    out = np.zeros(N)
    mel = [0, 4, 7, 4, 9, 7, 4, 2, 0, 4, 7, 12, 11, 7, 5, 2]
    e = 0.15
    i = 0
    at = start
    while at < end:
        place(out, pluck(midi(base + 12 + mel[i % 16]), 0.2, 0.5), at, gain)
        if i % 2 == 0:
            place(out, marimba(midi(base - 12 + [0, 0, 5, 7][(i // 4) % 4]), 0.3), at, gain * 1.2)
        i += 1; at += e
    return out


def eerie(start):
    out = np.zeros(N)
    for i, m in enumerate([81, 84, 88, 87, 81, 80]):
        place(out, marimba(midi(m), 1.2), start + i * 0.45, 0.28)
    return out


def build(path):
    mix = hum()
    # royal march (2.4–7)
    mix += bouncy(2.6, 6.95, base=65, gain=0.22)
    place(mix, fanfare(), 2.45, 0.9)
    place(mix, gib(9, 62, syl=0.1), 3.0, 0.7)            # Dill proclaims
    place(mix, gib(4, 74, spread=3, syl=0.07), 4.65, 0.5)  # Crumb: "?"
    place(mix, gib(7, 60, syl=0.11), 5.6, 0.7)            # Dill: "ME!"
    # THE LIGHT
    place(mix, choir(2.0), 7.0, 1.0)
    place(mix, whoosh(1.5), 8.2, 0.5)
    place(mix, pop(), 9.8, 0.8)
    place(mix, whoosh(1.0), 10.1, 0.5)
    place(mix, thud(), 11.0, 0.8)                         # door shuts
    # hover silence... then fall
    place(mix, sweep(1300, 200, 0.4, vdepth=0.02), 11.8, 0.4)
    place(mix, bonk(), 12.15, 1.0)
    place(mix, sweep(500, 1400, 0.75, vib=8), 12.2, 0.25)   # crown flying
    place(mix, plink(midi(96)), 12.95, 0.7)
    place(mix, gib(3, 72, spread=2, syl=0.08), 13.4, 0.4)  # Crumb: uh oh
    # RAGE
    place(mix, gib(12, 54, spread=6, syl=0.08, bright=0.9), 14.3, 0.8)
    for k in range(5):
        place(mix, hiss(0.35), 14.6 + k * 0.6, 0.6)
    place(mix, drumroll(3.0), 14.6, 0.9)
    place(mix, crash(), 17.6, 0.9)
    # catapult
    mix += bouncy(18.0, 22.0, base=60, gain=0.2)
    place(mix, gib(5, 58, syl=0.08), 18.2, 0.6)
    place(mix, gib(6, 76, spread=4, syl=0.06), 18.9, 0.5)   # Crumb protests
    place(mix, sweep(400, 1200, 0.6), 19.6, 0.25)          # Dill jumps
    place(mix, twang(), 20.25, 1.0)
    place(mix, sweep(300, 2200, 1.6, vib=7), 20.3, 0.4)     # Crumb flies
    place(mix, plink(midi(98)), 21.2, 0.6)                 # crown lands on Dill
    place(mix, splat(), 22.0, 1.0)
    for k in range(6):
        place(mix, plink(midi([96, 100, 103][k % 3])), 23.0 + 0.13 * k, 0.3)
    place(mix, gib(3, 76, spread=2, syl=0.08), 24.25, 0.45)  # "hi?"
    # silence... the duck turns
    mix += eerie(26.5)
    place(mix, squeak(1.1), 27.7, 0.9)
    place(mix, sweep(200, 120, 1.6, vib=3, vdepth=0.05), 29.2, 0.5)
    for m in (57, 60, 63, 66):  # diminished sting
        place(mix, marimba(midi(m), 1.8), 29.2, 0.35)
    place(mix, squeak(0.35), 30.15, 0.5)
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.9
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
