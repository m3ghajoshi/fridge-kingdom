"""Sound for FRIDGE KINGDOM Ep24 "Duck vs Duck" (variant B: cold open)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
import ep5_audio as A5
from ep5_audio import cricket_chirp, violin_tremolo
from ep6_audio import record_scratch
from ep7_audio import gasp, peep
from ep8_audio import shimmer, dun
from ep10_audio import squish
from ep16_audio import slide_whistle
from ep18_audio import minor_choir
from ep22_audio import quick_squeak, crack
from audio import SR, tarr, midi, place, plink, pluck, marimba, sweep, whoosh, thud, pop, ding, sting, boing, lowpass, bonk
import ep24 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A5.N = N
rng = np.random.default_rng(2424)


def tick(f=1500):
    t = tarr(0.06)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 80) * 0.6


def bell():
    t = tarr(1.2)
    s = sum(np.sin(2 * np.pi * 880 * k * t) * np.exp(-t * (2 + k)) / k for k in (1, 2.7, 5.4))
    return s * 0.5


def pfft(d=0.6):
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.25)
    f = 300 + 500 * np.exp(-t * 4)
    buzz = np.sign(np.sin(2 * np.pi * np.cumsum(f) / SR)) * 0.3
    return (n * 0.8 + lowpass(buzz, 0.2)) * np.exp(-t * 3)


def inhale(d):
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.08)
    return n * (t / d) ** 1.5 * 1.2


def big_squeak(d):
    """Squeak's loudest ever: long, wobbling, distorted."""
    t = tarr(d)
    f = 1150 + 500 * np.sin(np.pi * np.minimum(t / 0.4, 1) * 0.5) + 60 * np.sin(2 * np.pi * 7 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.6 * np.sin(2 * ph) + 0.4 * np.sign(np.sin(ph))
    env = np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.2)
    return np.tanh(s * 1.5) * env * 0.5


def icy_squeak(d=1.4):
    """The answer from the vent: one deep, slow, echoing squeak."""
    t = tarr(d)
    f = 260 + 140 * np.sin(np.pi * t / d) ** 0.8
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.2 * np.sign(np.sin(ph))
    env = np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.3)
    dry = s * env * 0.5
    out = dry.copy()
    for k, dl in enumerate((0.18, 0.37, 0.6)):
        sh = int(dl * SR)
        out[sh:] += dry[:-sh] * (0.45 / (k + 1))
    return out


def tinkle():
    out = np.zeros(int(SR * 0.5))
    for k in range(5):
        p = plink(midi(98 + (k * 3) % 9))
        at = int(k * 0.05 * SR)
        out[at:at + len(p)] += p[:len(out) - at] * 0.6
    return out


def build(path):
    mix = np.zeros(N)
    # cold open: tense violin standoff
    place(mix, violin_tremolo(3.3, 57), 0.0, 0.5)
    place(mix, violin_tremolo(3.3, 60), 0.0, 0.35)
    for k in range(6):
        place(mix, quick_squeak(0.08, 1300), 0.15 + 0.5 * k, 0.25)          # can't sit still
    place(mix, E.gib(2, 58, spread=2, syl=0.15, bright=0.4), 0.25, 0.3)       # hmm
    for k in range(8):
        place(mix, E.gib(1, 66 + (k % 3) * 3, spread=2, syl=0.07, bright=0.6), 0.5 + 0.3 * k, 0.15)   # footsteps arriving
    # DING: the contest begins
    place(mix, bell(), V.T_BELL, 0.8)
    t = V.T_BELL + 0.9
    i = 0
    while t < V.T_CHEER - 0.2:
        place(mix, tick(1600 if i % 2 == 0 else 1100), t, 0.6)
        t += 0.6; i += 1
    place(mix, violin_tremolo(V.T_CHEER - V.T_BELL - 0.3, 62), V.T_BELL + 0.3, 0.3)
    for k in range(6):
        place(mix, sweep(2000, 2400, 0.05, vdepth=0) * 0.2, V.TWITCH[0] + 0.12 * k, 0.3)            # twitch
    place(mix, sweep(220, 180, V.WOBBLE[1] - V.WOBBLE[0], vib=5, vdepth=0.1) * 0.3, V.WOBBLE[0], 0.35)   # creak
    place(mix, E.gib(1, 50, spread=1, syl=0.18, bright=0.3), V.T_BREATH - 0.3, 0.5)            # GULP
    place(mix, sweep(300, 900, V.T_BURST - V.T_BREATH, vib=8, vdepth=0.02) * 0.12, V.T_BREATH, 0.4)   # strain
    # the cheering section
    t = V.T_CHEER + 0.3
    while t < V.T_BURST - 1.2:
        place(mix, peep(), t, 0.55)
        place(mix, peep(), t + 0.2, 0.45)
        place(mix, E.gib(2, 62, spread=3, syl=0.09, bright=0.6), t + 0.45, 0.35)       # hup hup
        t += 0.9
    mix_b = E.bouncy(V.T_CHEER, V.T_BURST - 0.8, base=62, gain=0.18)
    mix += mix_b
    place(mix, sweep(400, 1600, 0.9, vib=12, vdepth=0.05) * 0.2, V.T_BURST - 1.0, 0.4)
    # PFFFT + ricochet
    place(mix, pfft(0.7), V.T_BURST, 1.0)
    place(mix, slide_whistle(1600, 500, 1.7) * 0.35, V.T_BURST + 0.05, 0.4)
    for b in V.BOUNCE[1:-1]:
        place(mix, boing(), b[0], 0.6)
    place(mix, squish(0.25), V.T_FLAT, 0.7)
    place(mix, quick_squeak(0.35, 700), V.T_FLAT + 0.1, 0.4)
    # winner
    for k in range(3):
        place(mix, bell(), V.T_WIN + 0.3 * k, 0.6)
    place(mix, E.fanfare(), V.T_WIN + 0.1, 0.55)
    place(mix, E.gib(3, 70, spread=4, syl=0.1, bright=0.8), V.T_WIN + 0.3, 0.45)     # yaaay
    place(mix, shimmer(0.8), V.T_WIN, 0.3)
    place(mix, cricket_chirp(), V.T_WIN + 1.8, 0.35)
    # tantrum: louder and louder
    place(mix, record_scratch(), V.T_UP, 0.4)
    for i, s0 in enumerate(V.TANTRUM):
        place(mix, quick_squeak(0.3, 1000 + 25 * i, 1.0 + 0.12 * i), s0, 0.35 + 0.07 * i)
        place(mix, thud() * 0.3, s0 - 0.1, 0.25 + 0.03 * i)
    place(mix, E.gib(2, 52, spread=2, syl=0.12, bright=0.3), V.TANTRUM[2], 0.3)   # ugh
    # the big one
    place(mix, inhale(V.T_BIG - V.T_INHALE), V.T_INHALE, 0.6)
    place(mix, big_squeak(V.T_BIG_END - V.T_BIG), V.T_BIG, 1.0)
    place(mix, sting() * 0.5, V.T_BIG, 0.3)
    for p0 in V.POPS:
        place(mix, pop(), p0, 0.6)
    place(mix, bonk(), V.T_CARTON[1], 0.9)
    place(mix, thud(), V.T_CARTON[1], 0.9)
    for d in V.DROPS:
        place(mix, tinkle(), d + V.T_FALL, 0.55)
        place(mix, crack() * 0.5, d + V.T_FALL, 0.4)
    # after
    for k in range(4):
        place(mix, E.gib(1, 60, spread=1, syl=0.12, bright=0.2), V.T_PANT + 0.35 * k, 0.25)     # pant
    place(mix, quick_squeak(0.15, 1100), V.T_PANT + 1.65, 0.4)
    # silence... then the answer
    place(mix, icy_squeak(1.5), V.T_ANSWER, 1.0)
    place(mix, sweep(900, 400, 1.6, vdepth=0) * 0.15, V.T_PUFF, 0.3)                 # frosty breath
    place(mix, gasp(), V.T_ANSWER + 0.7, 0.5)
    place(mix, minor_choir(1.6), V.T_LOOKUP[0], 0.3)
    place(mix, E.squeak(0.25), V.T_LOOKUP[0] + 0.5, 0.25)                          # the Duck turns
    for k, d in enumerate(V.DUNS):
        place(mix, dun([43, 42][k]), d, 1.1)
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    mix += E.hum() * 0.2
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.82
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
