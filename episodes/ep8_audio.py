"""Sound for FRIDGE KINGDOM Ep8 "It Hatched" (variant B: cold open, no fanfare card)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
from ep3_audio import big_thump, tick
from ep4_audio import chord, trombone, crack
from ep5_audio import drone
import ep6_audio as A6
from ep6_audio import record_scratch
from ep7_audio import peep
from audio import SR, tarr, midi, place, plink, sweep, whoosh, bonk, thud, pop, marimba, boing, ding, lowpass, pluck, sting
import ep8 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A6.N = N
rng = np.random.default_rng(88)


def clink():
    t = tarr(0.35)
    s = sum(np.sin(2 * np.pi * f * t) * a for f, a in ((2100, 0.5), (3350, 0.3), (5200, 0.15)))
    return s * np.exp(-t * 14) * 0.5


def peck():
    t = tarr(0.06)
    n = rng.standard_normal(len(t))
    return (n - lowpass(n, 0.3)) * np.exp(-t * 80) * 0.8 + np.sin(2 * np.pi * 1400 * t) * np.exp(-t * 60) * 0.4


def rumble(d=0.6):
    t = tarr(d)
    f = 55 + 10 * np.sin(2 * np.pi * 7 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sign(np.sin(ph)) * 0.4 + np.sin(ph * 2) * 0.3
    return lowpass(s, 0.08) * np.sin(np.pi * t / d) * 2.0


def shimmer(d):
    out = np.zeros(int(SR * d) + SR)
    at = 0.0
    while at < d:
        place(out, plink(midi(int(rng.integers(88, 104)))), at, 0.12)
        at += float(rng.uniform(0.07, 0.16))
    return out


def peep_hi(gain=1.0):
    return peep() * gain


def dun(m):
    t = tarr(0.7)
    f = midi(m)
    s = sum(np.sin(2 * np.pi * f * k * t) / k for k in range(1, 6))
    return s * np.exp(-t * 3.5) * 0.45


def build(path):
    mix = E.hum() * 0.5
    # 0–2.5: wobbling egg, cracks, POP
    for k, t0 in enumerate([0.05, 0.35, 0.65, 1.2, 1.45, 2.0, 2.2]):
        place(mix, tick(1100 + 90 * k), t0, 0.35)
    mix += 0  # keep hum
    place(mix, crack(), V.T_C1, 1.0)
    place(mix, crack(), V.T_C2, 1.0)
    place(mix, drone(1.0), 0.0, 0.35)
    place(mix, pop(), V.T_POP, 1.0); place(mix, crack(), V.T_POP, 0.6)
    place(mix, whoosh(0.5), V.T_POP + 0.05, 0.4)
    place(mix, sweep(500, 1400, 0.6, vdepth=0) * 0.4, V.T_POP + 0.1, 0.35)   # shell flies up
    # 3.6: clink, blink, peep
    place(mix, clink(), V.T_HELM, 0.9)
    place(mix, plink(midi(96)), 3.95, 0.25); place(mix, plink(midi(96)), 4.25, 0.25)
    place(mix, peep_hi(), 4.45, 0.8)
    place(mix, boing(), 4.7, 0.35)
    # 5.8–9: Dill and Crumb climb up: grunts, huffs
    place(mix, E.gib(3, 52, spread=3, syl=0.12, bright=0.3), 5.9, 0.4)
    place(mix, E.gib(2, 50, spread=2, syl=0.14, bright=0.3), 6.6, 0.4)
    place(mix, thud(), 7.4, 0.5)
    place(mix, E.gib(3, 72, spread=3, syl=0.1), 6.8, 0.35)
    place(mix, thud(), 8.2, 0.4)
    for t0 in (7.5, 8.0, 8.5, 9.0):
        place(mix, sweep(300, 200, 0.18, vdepth=0) * 0.5, t0, 0.25)   # huff
    # 9–10.8: Dill strides, poses: fanfare stub
    mix += E.bouncy(9.0, 9.8, base=55, gain=0.2)
    fan = E.fanfare()
    place(mix, fan[: int(SR * 1.0)] * np.linspace(1, 0, int(SR * 1.0)) ** 0.5, 9.8, 0.8)
    # 10.8: record scratch; harp of love
    place(mix, record_scratch(), V.T_SCRATCH, 0.8)
    for i, m in enumerate([72, 76, 79, 84, 88, 91]):
        place(mix, marimba(midi(m), 0.7), 11.1 + i * 0.18, 0.28)
    place(mix, chord([65, 69, 72, 77], 2.0), 11.2, 0.6)
    # 13–16: runs to Crumb, hugs his leg
    for k in range(6):
        place(mix, plink(midi(90 + (k % 3) * 2)), 13.0 + k * 0.13, 0.25)
    place(mix, E.gib(2, 80, spread=3, syl=0.08), 13.9, 0.4)                    # Crumb's yelp
    place(mix, peep_hi(), 14.6, 0.8)
    for t0 in (14.0, 14.7, 15.3):
        place(mix, pop(), t0, 0.2)                                              # heart pops
    place(mix, sweep(700, 1100, 0.25, vdepth=0) * 0.4, 14.2, 0.3)               # "?"
    # 16–21: copycat. step / step, hop / hop, salute / salute
    mix += E.bouncy(16.0, 21.0, base=64, gain=0.18)
    place(mix, plink(midi(79)), 16.1, 0.3); place(mix, plink(midi(91)), 16.5, 0.3)
    place(mix, boing(), 17.4, 0.4); place(mix, boing(), 17.8, 0.5)
    place(mix, ding(), 18.85, 0.4); place(mix, ding(), 19.3, 0.5)
    place(mix, peep_hi(0.6), 19.4, 0.6)
    place(mix, E.gib(4, 74, spread=4, syl=0.07), 20.1, 0.35)                   # Crumb giggles
    place(mix, E.gib(3, 50, spread=2, syl=0.12, bright=0.3), 19.5, 0.35)       # Dill grumbles
    # 21–26: Dill poses again; Peep hops on his head; PECK PECK; crown pops off
    place(mix, E.gib(3, 60, spread=4, syl=0.09), 21.1, 0.4)
    place(mix, fan[: int(SR * 0.7)] * np.linspace(1, 0, int(SR * 0.7)), 21.7, 0.6)
    place(mix, boing(), 22.6, 0.4); place(mix, thud(), 23.2, 0.3)
    place(mix, peck(), V.T_PECK1, 0.9); place(mix, peck(), V.T_PECK2, 0.9)
    place(mix, pop(), V.T_CROWN_OFF, 0.8)
    place(mix, sweep(900, 1500, 0.3, vdepth=0) * 0.4, V.T_CROWN_OFF, 0.35)
    place(mix, ding(), V.T_CROWN_OFF + 0.55, 0.6)                              # lands on Peep
    place(mix, E.hiss(0.9), 25.0, 0.45)                                        # Dill steams
    place(mix, E.gib(4, 48, spread=4, syl=0.1, bright=0.4), 25.1, 0.45)
    # 26–30: lunge, BONK, pile
    place(mix, whoosh(0.5), V.T_LUNGE, 0.6)
    place(mix, bonk(), V.T_BONK, 1.0); place(mix, thud(), V.T_BONK + 0.4, 0.6)
    place(mix, sweep(1200, 300, 0.6, vdepth=0) * 0.4, V.T_BONK + 0.1, 0.35)    # slide whistle down
    for k in range(4):
        place(mix, plink(midi(96 - k * 3)), 27.2 + k * 0.35, 0.15)             # dizzy twinkles
    place(mix, boing(), 27.5, 0.35)
    place(mix, peep_hi(), 28.3, 0.8)
    place(mix, boing(), V.T_UP, 0.4)
    # 30.2–32.7: the soap bubble drifts in
    place(mix, shimmer(2.5), V.T_BUB0, 1.0)
    place(mix, chord([76, 79, 83, 88], 2.4) * 0.5, V.T_BUB0, 0.5)
    place(mix, E.squeak(0.25), 31.4, 0.12)                                     # faint squeak inside it
    # 32.7: pop, sneeze, crown flies back onto Dill
    place(mix, pop(), V.T_BPOP, 1.0)
    sn = np.concatenate([sweep(900, 1500, 0.25, vdepth=0) * 0.3, peep()])
    place(mix, sn, V.T_SNEEZE - 0.15, 0.8)
    place(mix, whoosh(0.5), V.T_SNEEZE + 0.05, 0.4)
    place(mix, ding(), V.T_CROWN_BACK, 0.7)
    place(mix, E.gib(2, 66, spread=2, syl=0.09), V.T_CROWN_BACK + 0.1, 0.35)
    # 34.1: tummy RUMBLE. silence. Peep turns.
    place(mix, rumble(0.7), V.T_RUMBLE, 1.0)
    # 35: close-up: DUN DUN DUNNN + gulp
    for tp, m in zip(V.DUNS, (43, 42, 37)):
        place(mix, dun(m), tp, 1.0 if m != 37 else 1.3)
    place(mix, big_thump(), V.DUNS[2], 0.6)
    place(mix, sweep(500, 180, 0.3, vdepth=0) * 0.7, 35.75, 0.5)              # gulp
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    out = np.tanh(mix * 1.1)
    tt = np.arange(N) / SR
    # quiet hold before the rumble
    out *= 1 - 0.7 * np.clip((tt - 33.9) / 0.15, 0, 1) * np.clip((V.T_RUMBLE + 0.05 - tt) / 0.05, 0, 1)
    out = out / np.max(np.abs(out)) * 0.9
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
