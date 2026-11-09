"""Sound for FRIDGE KINGDOM Ep17 "The Expedition Plan" (variant A: title card first)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
import ep2_audio as A2
from ep4_audio import chord
from ep5_audio import drone, violin_tremolo
import ep6_audio as A6
from ep7_audio import gasp, peep
from ep8_audio import shimmer, dun
from ep10_audio import icy, sigh
from ep11_audio import harp, ooh, plip
from ep12_audio import flaps
from ep13_audio import tok, creak
from ep15_audio import chatter
from audio import SR, tarr, midi, place, plink, pluck, sweep, whoosh, thud, pop, marimba, ding, sting, boing, bonk
import ep17 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A2.N = N
A6.N = N
rng = np.random.default_rng(1717)


def cha_ching():
    out = np.zeros(int(SR * 0.7))
    t = tarr(0.08)
    place(out, rng.standard_normal(len(t)) * np.exp(-t * 60) * 0.5, 0, 1.0)
    for i, m in enumerate([88, 91, 96]):
        place(out, plink(midi(m)), 0.06 + 0.05 * i, 0.6)
    place(out, ding() * 0.6, 0.14, 0.8)
    return out


def tick():
    t = tarr(0.06)
    return np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 90) * 0.5


def hum_think(d):
    """Thinking hum: a wobbly low gibberish 'hmmm'."""
    t = tarr(d)
    f = midi(50) * (1 + 0.02 * np.sin(2 * np.pi * 4 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.4 * np.sin(2 * ph) + 0.2 * np.sin(3 * ph)
    return s * np.minimum(1, t / 0.2) * np.minimum(1, (d - t) / 0.2) * 0.3


def build(path):
    mix = E.hum() * 0.5
    # 0–2: title card
    place(mix, E.fanfare(), 0.1, 0.45)
    mix += A2.war_drum(0.9, 3, 0.3) * 0.35
    place(mix, sweep(300, 900, 0.4, vdepth=0) * 0.3, 0.8, 0.3)       # map unfurl
    # 2–7.4: war room: map smacks, nods, Chip says no, CHARGE
    mix += A2.war_drum(V.T_START, 13, 0.4) * 0.35
    for tp in V.TAPS:
        place(mix, A6.clang() * 0.3, tp, 0.25)
        place(mix, thud(), tp, 0.45)
        place(mix, E.gib(2, 52, spread=6, syl=0.08, bright=1.0), tp - 0.15, 0.5)
        place(mix, E.gib(2, 64, spread=2, syl=0.08, bright=0.4), tp + 0.15, 0.35)     # Crumb mm-hm
        place(mix, peep(), tp + 0.3, 0.25)
    place(mix, E.gib(4, 70, spread=3, syl=0.07, bright=0.5), V.T_NO + 0.1, 0.4)        # Chip mm-mm
    place(mix, chatter(0.7), V.T_NO, 0.3)
    place(mix, sting(), V.T_GLARE, 0.35)
    place(mix, E.gib(3, 48, spread=4, syl=0.1, bright=1.0), V.T_GLARE + 0.05, 0.5)
    place(mix, sweep(1800, 2600, 0.15, vdepth=0) * 0.4, V.T_YES - 0.1, 0.4)
    place(mix, E.gib(6, 74, spread=2, syl=0.05, bright=0.6), V.T_YES, 0.4)
    place(mix, E.fanfare(), V.T_CHARGE, 0.4)
    place(mix, E.gib(3, 58, spread=8, syl=0.12, bright=1.0), V.T_CHARGE + 0.05, 0.6)  # HYAAA
    # 7.5–15: costume montage, cha-ching x4, bouncy music
    E_b = E.bouncy(V.T_C1 - 0.2, V.T_GSTEP, base=62, gain=0.22)
    mix += E_b[:N] if len(E_b) >= N else np.pad(E_b, (0, N - len(E_b)))
    for tc in (V.T_C1, V.T_C2, V.T_C3, V.T_C4):
        place(mix, pop(), tc, 0.5)
        place(mix, whoosh(0.3), tc - 0.1, 0.3)
        place(mix, cha_ching(), tc + 0.1, 0.7)
    place(mix, E.gib(2, 66, spread=3, syl=0.08, bright=0.5), V.T_C1 + 0.4, 0.4)
    place(mix, shimmer(0.7), V.T_C2 + 0.3, 0.4)
    place(mix, peep(), V.T_C2 + 0.35, 0.4)
    place(mix, sigh(52), V.T_WUP + 0.2, 0.5)
    place(mix, whoosh(0.3), V.T_C3 - 0.25, 0.35)
    place(mix, ooh(0.8), V.T_C3 + 0.4, 0.25)
    place(mix, plip(), V.T_C3 + 0.75, 0.45)
    place(mix, E.fanfare(), V.T_C4 + 0.5, 0.45)
    place(mix, E.gib(4, 56, spread=6, syl=0.09, bright=0.9), V.T_C4 + 0.6, 0.45)
    # 15–21.5: Grandma's inspection, BONK, stumble, THUNK
    place(mix, sweep(1200, 500, 1.2, vdepth=0.03) * 0.25, V.T_GSTEP, 0.35)            # floating down
    place(mix, whoosh(1.2), V.T_GSTEP + 0.1, 0.25)
    place(mix, thud() * 0.5, V.T_GLAND, 0.35)
    A6.march(V.T_GLAND, V.T_ZIP, mix, gain=0.22)
    place(mix, E.gib(1, 44, spread=1, syl=0.2, bright=0.3), V.T_INS1 + 0.3, 0.45)       # hm.
    place(mix, peep(), V.T_INS1 + 0.1, 0.35)
    place(mix, sweep(400, 1600, 0.2, vdepth=0) * 0.4, V.T_INS2 + 0.3, 0.4)              # GK
    place(mix, E.gib(1, 76, spread=1, syl=0.1, bright=1.0), V.T_INS2 + 0.32, 0.4)
    place(mix, pop() * 0.6, V.T_INS3 + 0.15, 0.4)                                       # boop
    place(mix, whoosh(0.35), V.T_ZIP, 0.5)
    place(mix, sweep(600, 2000, 0.3, vdepth=0) * 0.3, V.T_ZIP, 0.35)
    place(mix, E.gib(3, 50, spread=4, syl=0.1, bright=0.8), V.T_PUFF + 0.05, 0.45)
    place(mix, sweep(400, 1200, 0.3, vdepth=0) * 0.25, V.T_BONK - 0.25, 0.3)
    place(mix, bonk(), V.T_BONK, 0.9)
    for k in range(4):
        place(mix, plink(midi(88 + 3 * (k % 2))) * 0.6, V.T_BONK + 0.2 + 0.15 * k, 0.25)
    place(mix, E.gib(5, 54, spread=8, syl=0.08, bright=1.0), V.T_BONK + 0.3, 0.45)
    at = V.T_BONK + 0.3
    while at < V.T_THUNK:
        place(mix, thud() * 0.3, at, 0.3); at += 0.18
    place(mix, thud(), V.T_THUNK, 0.8)
    place(mix, creak(0.6), V.T_THUNK + 0.05, 0.3)
    place(mix, E.gib(2, 46, spread=3, syl=0.12, bright=0.6), V.T_HOODUP, 0.45)          # hmph
    # 21.9–25: the freezer door problem
    place(mix, E.gib(4, 70, spread=4, syl=0.08, bright=0.5), V.T_PROB + 0.1, 0.35)
    for k in range(3):
        place(mix, thud() * 0.35, V.T_PROB + 0.25 + 0.45 * k, 0.35)                    # tump tump
    place(mix, sweep(500, 200, 0.4, vdepth=0) * 0.3, V.T_PROB + 0.8, 0.35)               # X buzz
    place(mix, E.choir(1.4), V.T_HAND + 0.4, 0.3)
    place(mix, sweep(200, 500, 0.5, vdepth=0) * 0.2, V.T_HAND + 0.6, 0.3)                # door swing
    place(mix, ooh(0.8), V.T_HAND + 0.8, 0.25)
    # 25–28.5: everyone thinks
    place(mix, hum_think(V.T_BULB - V.T_THINK), V.T_THINK, 0.5)
    for k in range(8):
        place(mix, tick(), V.T_THINK + 0.3 + 0.4 * k, 0.5 if k % 2 == 0 else 0.35)
    for k in range(2):
        place(mix, tok(), V.T_THINK + 1.8 + 0.25 * k, 0.4)
    # 28.5–31.3: lightbulb, the Ep 7 memory
    place(mix, ding(), V.T_BULB, 0.7)
    place(mix, shimmer(0.8), V.T_BULB, 0.35)
    harp(V.T_FLASH, mix, gain=0.2)
    place(mix, E.squeak(0.4), V.T_FLASH + 0.5, 0.3)        # remembered squeak (soft, in the bubble)
    place(mix, E.choir(1.0), V.T_FLASH + 1.0, 0.18)
    place(mix, ooh(1.0), V.T_FLASH + 0.8, 0.3)
    # 31.3–37: the slow turn and the stare
    place(mix, drone(V.DUNS[0] - V.T_TURN), V.T_TURN, 0.35)
    place(mix, violin_tremolo(V.DUNS[0] - V.T_TURN, 76), V.T_TURN, 0.55)
    place(mix, violin_tremolo(V.DUNS[0] - V.T_DUCK, 77), V.T_DUCK, 0.4)
    place(mix, creak(1.2), V.T_DUCK, 0.35)
    place(mix, E.gib(1, 48, spread=1, syl=0.2, bright=0.3), V.T_GULP, 0.5)
    place(mix, plink(midi(100)), V.T_GLINT, 0.4)
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
