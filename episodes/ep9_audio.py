"""Sound for FRIDGE KINGDOM Ep9 "Feeding Time" (variant A: title card + fanfare)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
from ep3_audio import big_thump, run_music
from ep4_audio import chord, trombone, crack
from ep5_audio import violin_tremolo
import ep6_audio as A6
from ep6_audio import record_scratch
from ep7_audio import peep
from ep8_audio import peck, rumble, clink
from audio import SR, tarr, midi, place, plink, sweep, whoosh, bonk, thud, pop, marimba, boing, ding, lowpass, munch
import ep9 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A6.N = N
import ep3_audio as A3
A3.N = N
rng = np.random.default_rng(99)


def snap():
    t = tarr(0.08)
    n = rng.standard_normal(len(t))
    return (n - lowpass(n, 0.2)) * np.exp(-t * 60) * 0.7 + np.sin(2 * np.pi * 900 * t) * np.exp(-t * 50) * 0.4


def gulp():
    return sweep(420, 140, 0.28, vdepth=0) * np.exp(-tarr(0.28) * 4) * 0.9


def slurp(d=1.5):
    t = tarr(d)
    f = 300 + 500 * np.abs(np.sin(2 * np.pi * 3.5 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    n = lowpass(rng.standard_normal(len(t)), 0.3)
    return (np.sin(ph) * 0.4 + n * 0.5) * np.sin(np.pi * t / d) * 0.8


def burp(d=1.0):
    t = tarr(d)
    f = 70 + 25 * np.sin(2 * np.pi * 3 * t) - 20 * t
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sign(np.sin(ph)) * 0.5 + np.sin(ph * 3) * 0.3
    s *= 0.7 + 0.3 * np.sin(2 * np.pi * 31 * t)
    return lowpass(s, 0.12) * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.3) * 2.2


def footstep():
    return big_thump() * 1.0 + lowpass(rng.standard_normal(int(SR * 0.3)), 0.03) * np.exp(-tarr(0.3) * 12) * 3


def long_peep():
    t = tarr(0.9)
    f = 2100 + 500 * np.sin(np.pi * t / 0.9) + 60 * np.sin(2 * np.pi * 9 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.minimum(1, t / 0.04) * np.minimum(1, (0.9 - t) / 0.2) * 0.5


def build(path):
    mix = E.hum() * 0.5
    # 0–2: title fanfare
    place(mix, E.fanfare(), 0.1, 1.0)
    # 2–4: the chase
    mix += run_music(2.0, 4.6, base=57, gain=0.22)
    for t0 in np.arange(2.3, 4.0, 0.29):
        place(mix, snap(), t0, 0.8)
    place(mix, E.gib(5, 70, spread=6, syl=0.07), 2.2, 0.45)          # Dill panics
    place(mix, E.gib(3, 64, spread=4, syl=0.08), 3.5, 0.4)
    place(mix, thud(), 4.0, 0.5)
    # 4–6: Crumb blocks, crunches off a crumb, feeds it
    place(mix, sweep(500, 900, 0.2, vdepth=0) * 0.4, 3.6, 0.4)
    place(mix, E.gib(2, 76, spread=2, syl=0.1), 3.7, 0.4)
    place(mix, crack(), 4.65, 0.5)
    place(mix, whoosh(0.3), 5.75, 0.3)
    for k in range(4):
        place(mix, munch(), 6.05 + k * 0.17, 0.8)
    place(mix, peep(), 6.4, 0.6)
    # 7.35: PECK, ow
    place(mix, peck(), 7.35, 1.0); place(mix, crack(), 7.37, 0.4)
    place(mix, E.gib(1, 86, spread=1, syl=0.12), 7.45, 0.6)
    for k in range(3):
        place(mix, munch(), 7.7 + k * 0.2, 0.6)
    place(mix, E.gib(3, 74, spread=5, syl=0.06), 8.6, 0.5)            # Dill yelps
    place(mix, ding(), 9.05, 0.6)                                       # Crumb's idea
    place(mix, whoosh(0.4), V.T_CUT - 0.2, 0.6)
    # 10–15: feeding montage
    mix += E.bouncy(10.0, 15.0, base=62, gain=0.2)
    for i, (ts, tt, tg) in enumerate(V.T_FOOD):
        place(mix, plink(midi(84)), ts, 0.3)
        place(mix, sweep(600, 1100, 0.3, vdepth=0) * 0.3, tt, 0.4)
        if i == 2:
            place(mix, pop(), tg, 0.9)
        place(mix, gulp(), tg, 0.9)
        place(mix, ding(), tg + 0.2, 0.5 + 0.1 * i)
    place(mix, E.squeak(0.25), 12.4, 0.25)                             # the sticker Duck turns
    place(mix, E.gib(3, 70, spread=3, syl=0.09), 15.0, 0.4)            # Crumb: uh oh
    # 16–21: the butter
    place(mix, E.gib(4, 54, spread=4, syl=0.08, bright=0.3), 16.0, 0.45)
    place(mix, boing(), 16.9, 0.5); place(mix, thud(), V.T_SLURP0, 0.4)
    place(mix, slurp(V.T_SLURP1 - V.T_SLURP0), V.T_SLURP0 + 0.05, 1.0)
    trombone(19.3, mix)
    place(mix, E.gib(5, 50, spread=4, syl=0.14, bright=0.3), 20.4, 0.45)   # Dill sobs
    # 21–26: the jello stand-off
    place(mix, plink(midi(91)), 21.5, 0.4)
    place(mix, boing(), V.T_GLAND - 0.6, 0.45); place(mix, thud(), V.T_GLAND, 0.6)
    place(mix, violin_tremolo(V.T_SWING - V.T_GLAND, 76), V.T_GLAND, 0.8)
    place(mix, violin_tremolo(V.T_SWING - V.T_GLAND, 77), V.T_GLAND, 0.5)
    place(mix, whoosh(0.4), V.T_SWING - 0.05, 0.9)
    place(mix, bonk(), V.T_SWING + 0.15, 0.5)
    place(mix, E.gib(2, 84, spread=3, syl=0.07), V.T_SWING + 0.3, 0.45)
    # 26–30: content Peep, BURP, crown flies
    mix += E.bouncy(26.4, 28.4, base=60, gain=0.14)
    place(mix, E.gib(4, 52, spread=3, syl=0.1, bright=0.4), 27.6, 0.4)  # Dill scolds
    place(mix, sweep(300, 500, 0.5, vdepth=0) * 0.3, V.T_BURP - 0.6, 0.4)
    place(mix, burp(1.0), V.T_BURP, 1.2)
    place(mix, sweep(600, 1800, 0.6, vdepth=0) * 0.4, V.T_BURP + 0.1, 0.45)   # slide whistle up
    place(mix, sweep(1800, 600, 0.5, vdepth=0) * 0.4, V.T_CROWN_DROP - 0.5, 0.4)
    place(mix, clink(), V.T_CROWN_DROP, 0.9); place(mix, ding(), V.T_CROWN_DROP + 0.05, 0.4)
    # 30.8–33.5: pats, sleepy
    for t0 in (30.95, 31.3, 31.65, 32.0):
        place(mix, thud(), t0, 0.18)
    for i, m in enumerate([72, 67, 64, 60]):
        place(mix, marimba(midi(m), 0.8), 31.0 + i * 0.4, 0.25)
    place(mix, sweep(500, 300, 0.5, vdepth=0) * 0.3, 32.7, 0.3)        # yawn
    # 33.5: PEEEEEP
    place(mix, long_peep(), V.T_PEEEP, 1.3)
    place(mix, long_peep(), V.T_PEEEP + 0.05, 0.4)
    # footsteps outside
    for tt in V.T_THUMPS:
        place(mix, footstep(), tt, 1.0)
    # light + choir, then record stop
    place(mix, E.choir(V.T_STOP - V.T_LIGHT + 0.3), V.T_LIGHT, 1.0)
    place(mix, record_scratch(), V.T_STOP, 1.0)
    place(mix, peep(), 38.25, 0.35)
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    out = np.tanh(mix * 1.1)
    tt = np.arange(N) / SR
    # silence before the PEEP, and after the record stop (except the tiny peep + end squeak)
    out *= 1 - 0.75 * np.clip((tt - (V.T_PEEEP - 0.6)) / 0.1, 0, 1) * np.clip((V.T_PEEEP - tt) / 0.02, 0, 1)
    out = out / np.max(np.abs(out)) * 0.9
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
