"""Sound for FRIDGE KINGDOM Ep19 "The Frozen North" (variant A: title card first)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
import ep5_audio as A5
from ep5_audio import violin_tremolo, drone
from ep7_audio import gasp, peep, echo
from ep8_audio import shimmer, dun, rumble, clink
from ep10_audio import icy, sigh
from ep14_audio import crackle
from ep15_audio import chatter
from ep18_audio import wind, scream, footstep
from audio import SR, tarr, midi, place, plink, pluck, marimba, sweep, whoosh, thud, pop, ding, sting, boing, bonk, lowpass
import ep19 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A5.N = N
rng = np.random.default_rng(1919)


def roll(d):
    """Big frozen pea rolling: low grinding rumble."""
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.02) * 4
    f = 40 + 8 * np.sin(2 * np.pi * 3 * t)
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * 0.6
    return (n + s) * np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.3) * 0.5


def tap():
    t = tarr(0.12)
    return np.sin(2 * np.pi * 1400 * t) * np.exp(-t * 60) * 0.5 + rng.standard_normal(len(t)) * np.exp(-t * 90) * 0.2


def warm_breath(d):
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.08)
    return n * np.sin(np.pi * t / d) * 1.4


def shatter():
    t = tarr(0.8)
    s = rng.standard_normal(len(t)) * np.exp(-t * 9) * 0.6
    for f in (2300, 3100, 4200, 5600):
        s += np.sin(2 * np.pi * f * t + rng.uniform(0, 6)) * np.exp(-t * (6 + f / 1500)) * 0.2
    return s


def wonder(start, mix, gain=0.3):
    """A slow glassy arpeggio for the frozen hall."""
    for i, m in enumerate([76, 79, 83, 88, 86, 83, 79, 81]):
        place(mix, marimba(midi(m), 1.0), start + i * 0.28, gain)
        place(mix, plink(midi(m + 12)), start + i * 0.28 + 0.02, gain * 0.4)


def build(path):
    mix = np.zeros(N)
    # title card
    place(mix, E.fanfare(), 0.2, 0.35)
    place(mix, icy(1.8), 0.1, 0.3)
    # A: blizzard
    place(mix, wind(V.T_B - V.T_START + 0.3), V.T_START, 0.7)
    place(mix, drone(1.0), V.T_START, 0.3)
    place(mix, sweep(400, 200, 0.4, vdepth=0) * 0.15, V.T_EYE_SHUT, 0.4)
    place(mix, pop(), V.T_PPOP, 0.8)
    place(mix, peep(), V.T_PPOP + 0.45, 0.6)
    for name in ("dill", "chip", "crumb"):
        place(mix, pop(), V.POPS[name], 0.6)
    place(mix, E.gib(2, 50, spread=4, syl=0.1, bright=0.5), V.POPS["dill"] + 0.1, 0.35)
    place(mix, chatter(1.0), V.POPS["chip"] + 0.1, 0.25)
    place(mix, E.gib(3, 58, spread=8, syl=0.12, bright=1.0), V.T_HYA, 0.6)       # HYAAA
    place(mix, crackle(0.3), V.T_ICICLE, 0.5)
    place(mix, sweep(600, 250, 0.35, vdepth=0) * 0.3, V.T_TIP, 0.4)
    place(mix, clink(), V.T_TIP + 0.25, 0.9)
    place(mix, E.gib(2, 64, spread=3, syl=0.08, bright=0.4), V.T_TIP + 0.4, 0.35)  # ow
    place(mix, chatter(0.6), V.T_TIP + 0.3, 0.2)                                 # Chip giggles
    for k in range(7):
        place(mix, footstep() * 0.3, V.T_MARCH + 0.3 * k, 0.25)
    # B: the pea avalanche
    place(mix, whoosh(0.5), V.T_B - 0.25, 0.5)
    place(mix, rumble(0.9), V.T_RUMBLE, 0.7)
    place(mix, E.gib(1, 62, spread=3, syl=0.12, bright=0.5), V.T_LOOK, 0.35)   # ?
    place(mix, violin_tremolo(0.7, 64), V.T_LOOK, 0.3)
    for i, t0 in enumerate(V.PEA_T0):
        tb = t0 + (V.BANK - (-850 - 60 * i)) / V.PEA_V
        place(mix, roll(tb - t0), t0, 0.6)
        place(mix, whoosh(0.6), tb, 0.45)
        place(mix, thud(), tb + 0.75, 0.5)
    place(mix, scream(1.3, 72), V.T_RUN, 0.35)
    place(mix, scream(1.2, 64), V.T_RUN + 0.1, 0.3)
    mix += E.bouncy(V.T_RUN, V.T_DIVE, base=62, gain=0.28)
    place(mix, scream(1.0, 70), 11.4, 0.3)
    place(mix, whoosh(0.3), V.T_DIVE, 0.4)
    for k in range(4):
        place(mix, thud() * 0.6, V.T_LAND - 0.05 + 0.06 * k, 0.4)
    # C: the popsicle
    place(mix, sigh(56), V.T_UPC, 0.4)                                         # phew
    place(mix, E.gib(2, 52, spread=2, syl=0.14, bright=0.6), V.T_POSE, 0.5)     # HMPH
    place(mix, crackle(0.45), V.T_FREEZE, 0.8)
    place(mix, icy(0.8), V.T_FREEZE, 0.4)
    place(mix, ding(), V.T_FREEZE + 0.4, 0.3)
    place(mix, gasp(), V.T_GASP2, 0.6)
    place(mix, E.gib(2, 70, spread=4, syl=0.08, bright=0.5), V.T_CHIPHUG, 0.3)
    place(mix, crackle(0.4), V.T_EXTRA, 1.0)
    place(mix, E.gib(1, 76, spread=2, syl=0.1, bright=0.7), V.T_EEP, 0.4)       # eep
    place(mix, warm_breath(0.9), V.T_BREATH + 0.05, 0.5)
    place(mix, peep(), V.T_BREATH, 0.35)
    place(mix, shatter(), V.T_CRACK, 0.9)
    place(mix, bonk() * 0.4, V.T_CRACK, 0.4)
    place(mix, chatter(0.8), V.T_BRR, 0.4)
    for k in range(3):
        place(mix, plink(midi(84 - 3 * k)), V.T_CRACK + 0.3 + 0.2 * k, 0.25)     # drip
    place(mix, E.gib(2, 72, spread=5, syl=0.09, bright=0.7), V.T_LEAD + 0.2, 0.35)
    # D: the canyon
    place(mix, whoosh(0.5), V.T_D - 0.25, 0.5)
    place(mix, icy(V.T_E - V.T_D), V.T_D, 0.25)
    for t0 in (20.3, 21.1, 21.9, 23.9):
        for e in range(3):
            place(mix, tap(), t0 + 0.22 * e, 0.5 * (0.55 ** e))
    place(mix, echo(E.gib(3, 58, spread=8, syl=0.12, bright=1.0), delays=(0.3, 0.6, 0.9), decay=0.45), V.T_SHOUT, 0.55)
    place(mix, E.gib(1, 60, spread=1, syl=0.18, bright=0.2), V.T_SHOUT + 0.5, 0.3)   # shhh
    place(mix, sweep(1800, 600, 0.4, vdepth=0) * 0.2, V.T_FALLICE, 0.4)
    place(mix, bonk(), V.T_BONK, 0.8)
    place(mix, clink(), V.T_BONK + 0.02, 0.6)
    place(mix, shimmer(1.2), V.T_GLOW, 0.3)
    place(mix, E.gib(2, 60, spread=3, syl=0.25, bright=0.4), V.T_GLOW + 0.3, 0.35)    # ooooh
    # E: the hall
    place(mix, whoosh(0.5), V.T_E - 0.25, 0.4)
    wonder(V.T_E + 0.1, mix, 0.3)
    place(mix, sting(), V.T_STING, 0.6)
    place(mix, shimmer(1.0), V.T_STING, 0.4)
    place(mix, gasp(), V.T_GASP3, 0.7)
    for k in range(5):
        place(mix, footstep() * 0.25, V.T_WALK + 0.3 * k, 0.25)
    place(mix, plink(midi(96)), V.T_TOUCH + 0.1, 0.5)
    place(mix, plink(midi(91)), V.T_TOUCH + 0.25, 0.3)
    # F: two Ducks?!
    place(mix, E.squeak(0.25), V.T_BDUCK, 0.4)
    for i, tt in enumerate(V.TURNS):
        place(mix, boing(), tt, 0.45 + 0.05 * i)
    place(mix, E.gib(2, 66, spread=10, syl=0.08, bright=0.9), V.T_Q, 0.5)      # ?!
    place(mix, sting() * 0.6, V.T_Q, 0.4)
    # G: the shadow
    place(mix, drone(V.END_T - V.T_SHADOW), V.T_SHADOW, 0.6)
    place(mix, wind(V.END_T - V.T_SHADOW), V.T_SHADOW, 0.35)
    place(mix, violin_tremolo(1.2, 52), V.T_TURN, 0.3)
    place(mix, E.gib(1, 50, spread=1, syl=0.15, bright=0.3), V.T_TURN + 0.3, 0.4)   # gulp
    place(mix, plink(midi(100)), V.T_EYES, 0.4)
    place(mix, E.gib(1, 78, spread=2, syl=0.08, bright=0.6), V.T_SEE, 0.3)
    for k, d in enumerate(V.DUNS):
        place(mix, dun([43, 42, 38][k]), d, 1.1)
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    mix += E.hum() * 0.25
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.9
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
