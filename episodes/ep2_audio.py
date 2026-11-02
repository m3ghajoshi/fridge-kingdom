"""Sound for FRIDGE KINGDOM Ep2 "Operation Butter"."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
from audio import SR, midi, place, plink, sweep, whoosh, bonk, thud, pop, marimba, boing

DUR = 38.0
N = int(SR * DUR)
E.N = N  # resize shared helpers' buffers (hum, bouncy, eerie)


def war_drum(start, beats, gap=0.4):
    out = np.zeros(N)
    for k in range(beats):
        place(out, thud(), start + k * gap, 0.9 if k % 2 == 0 else 0.6)
    return out


def build(path):
    mix = E.hum()
    place(mix, E.fanfare(), 0.1, 0.9)
    # Crumb sidesteps away from the Duck; tiny squeak each time it turns
    for i in range(10):
        place(mix, plink(midi(86 if i % 2 else 89)), 2.3 + i * 0.37, 0.45)
    for g in (3.0, 4.2, 5.3):
        place(mix, E.squeak(0.25), g, 0.45)
        place(mix, E.gib(2, 76, spread=2, syl=0.06), g + 0.05, 0.35)
    # leap + jello bounces
    place(mix, sweep(500, 1300, 0.9, vib=7), 6.0, 0.3)
    for k in range(3):
        place(mix, boing(), 7.0 + k * 0.47, 0.6 - k * 0.12)
    place(mix, E.splat(), 8.85, 0.8)
    # the battle plan
    place(mix, whoosh(0.6), 9.15, 0.4)
    mix += war_drum(9.4, 12)
    place(mix, E.gib(14, 58, spread=6, syl=0.09, bright=0.8), 9.5, 0.75)
    place(mix, E.gib(3, 74, spread=2, syl=0.07), 12.4, 0.45)
    # building the decoy
    mix += E.bouncy(14.0, 18.9, base=62, gain=0.2)
    place(mix, pop(), 14.35, 0.8)
    for k in range(6):
        place(mix, plink(midi(79 + (k % 3) * 2)), 14.8 + k * 0.2, 0.4)   # squeaky hammering
    place(mix, pop(), 16.05, 0.7)
    place(mix, E.gib(5, 78, spread=3, syl=0.06), 17.2, 0.55)             # Crumb protests
    place(mix, plink(midi(91)), 17.7, 0.6)
    # Dill hides... silence
    place(mix, E.gib(3, 60, syl=0.08), 19.2, 0.4)
    # THE LIGHT
    place(mix, E.choir(2.0), 21.0, 1.0)
    place(mix, whoosh(1.5), 21.6, 0.5)
    place(mix, plink(midi(72)), 22.45, 0.4)                               # "?"
    place(mix, sweep(1500, 150, 0.3, vib=2, vdepth=0.0), 23.6, 0.35)     # record scratch-ish
    place(mix, whoosh(0.8), 23.7, 0.5)
    place(mix, pop(), 24.85, 0.9)
    place(mix, E.gib(22, 66, spread=8, syl=0.07, bright=0.9), 24.95, 0.8)  # Dill screams, fading
    place(mix, plink(midi(96)), 25.9, 0.7)                                # crown clink
    place(mix, thud(), 31.5, 0.8)                                         # door shuts
    # in the dark
    place(mix, sweep(400, 900, 0.6), 33.0, 0.25)
    place(mix, plink(midi(98)), 34.2, 0.5)
    place(mix, E.squeak(1.1), 34.6, 0.85)
    for m in (57, 60, 63, 66):
        place(mix, marimba(midi(m), 1.8), 36.0, 0.35)
    place(mix, E.squeak(0.35), 36.95, 0.5)
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.9
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
