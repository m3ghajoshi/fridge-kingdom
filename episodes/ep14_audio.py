"""Sound for FRIDGE KINGDOM Ep14 "The Duck Is Back" (variant B: cold open)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
import ep2_audio as A2
from ep4_audio import chord
from ep5_audio import violin_tremolo, drone, cricket_chirp
import ep6_audio as A6
from ep7_audio import gasp, peep
from ep8_audio import shimmer, dun
from ep10_audio import icy, sigh
from ep11_audio import harp, ooh
from ep12_audio import flaps
from ep13_audio import tinkle
from audio import SR, tarr, midi, place, plink, sweep, whoosh, thud, pop, marimba, ding, lowpass, sting
import ep14 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A2.N = N
A6.N = N
rng = np.random.default_rng(1414)


def pat():
    t = tarr(0.12)
    n = rng.standard_normal(len(t))
    return lowpass(n, 0.12) * np.exp(-t * 45) * 0.9 + np.sin(2 * np.pi * 180 * t) * np.exp(-t * 40) * 0.4


def sizzle(d):
    t = tarr(d)
    n = rng.standard_normal(len(t))
    return (n - lowpass(n, 0.3)) * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.2) * 0.25


def crackle(d):
    out = np.zeros(int(SR * d) + SR)
    at = 0.0
    while at < d:
        t = tarr(0.03)
        place(out, rng.standard_normal(len(t)) * np.exp(-t * 120), at, float(rng.uniform(0.2, 0.5)))
        at += float(rng.uniform(0.02, 0.07))
    return out


def lullaby(start, end, mix, gain=0.22):
    """Gentle music-box loop while Peep moons over the Duck."""
    notes = [72, 76, 79, 84, 79, 76, 74, 77, 81, 77]
    at, i = start, 0
    while at < end:
        place(mix, plink(midi(notes[i % len(notes)])), at, gain)
        at += 0.28; i += 1


def build(path):
    mix = E.hum() * 0.5
    # 0–1: the eye glares... the door bursts open; the eye squints away
    place(mix, drone(1.0), 0.0, 0.35)
    place(mix, sweep(600, 300, 0.4, vdepth=0) * 0.3, V.T_OPEN, 0.3)
    place(mix, E.choir(4.6), V.T_OPEN - 0.05, 0.9)
    place(mix, whoosh(0.5), V.T_OPEN, 0.4)
    for k in range(4):
        place(mix, gasp(), V.T_PULL + 0.3 + 0.08 * k, 0.3)
    # 1.1–5.2: the Hand sets the clean Duck down; sparkles
    place(mix, shimmer(2.2), 1.2, 0.4)
    place(mix, ding(), V.T_SET, 0.5); place(mix, E.squeak(0.25), V.T_SET + 0.02, 0.4)
    place(mix, shimmer(0.7), V.T_SET, 0.5)
    place(mix, whoosh(0.6), V.T_SET + 0.5, 0.3)
    place(mix, thud(), V.T_CLOSE, 0.6)
    # 5.6–7.6: everyone bows
    for i, t0 in enumerate(V.BOW_T):
        place(mix, whoosh(0.25), t0, 0.35)
        place(mix, marimba(midi([67, 71, 74, 79][i]), 0.4), t0 + 0.1, 0.35)
    place(mix, pop(), V.T_SPROUT - 0.3, 0.4); place(mix, whoosh(0.25), V.T_SPROUT, 0.3)
    place(mix, whoosh(0.3), V.T_GBOW, 0.35); place(mix, chord([55, 59, 62, 67], 1.2), V.T_GBOW + 0.1, 0.18)
    # 7.6–9.9: Dill: record scratch, steam, sword, glint, deflate
    place(mix, A6.record_scratch(), V.T_SCRATCH, 0.9)
    place(mix, E.gib(3, 58, spread=6, syl=0.07, bright=1.0), V.T_SCRATCH + 0.3, 0.5)
    place(mix, sizzle(V.T_DEFLATE - V.T_STEAM), V.T_STEAM, 0.6)
    mix += A2.war_drum(V.T_SWORD, 2, 0.25) * 0.6
    place(mix, E.gib(4, 50, spread=6, syl=0.08, bright=0.9), V.T_SWORD + 0.05, 0.55)
    place(mix, plink(midi(100)), V.T_GLINT, 0.5); place(mix, plink(midi(103)), V.T_GLINT + 0.06, 0.4)
    place(mix, sweep(500, 180, 0.6, vdepth=0) * 0.5, V.T_DEFLATE, 0.5)     # deflating
    place(mix, sigh(46), V.T_DEFLATE + 0.3, 0.4)
    # 10–14.2: Peep falls for the Duck
    place(mix, peep(), V.T_NOTICE, 0.6)
    harp(V.T_LOVE, mix, gain=0.3)
    for k in range(5):
        place(mix, pop(), V.T_LOVE + 0.2 + 0.25 * k, 0.2)
    flaps(mix, V.T_HOPOFF, V.T_WADDLE, 0.06, 0.4)
    for k in range(6):
        place(mix, peep() * 0.6, V.T_WADDLE + 0.22 * k, 0.25)
    lullaby(V.T_LOVE + 0.2, V.T_STILL, mix)
    # 14.2–19.3: very still... cricket; wave; crust; drop
    for t0 in (V.T_STILL + 0.6, V.T_STILL + 1.0, V.T_WAVE + 1.0, V.T_WAVE + 1.3, V.T_DROP - 0.4, V.T_DROP - 0.1):
        place(mix, cricket_chirp(), t0, 0.35)
    place(mix, E.gib(3, 64, spread=4, syl=0.09, bright=0.7), V.T_WAVE, 0.45)        # "hellooo?"
    place(mix, E.gib(4, 66, spread=5, syl=0.08, bright=0.8), V.T_BREAD + 0.1, 0.45)  # "look! food!"
    place(mix, ding(), V.T_BREAD, 0.3)
    place(mix, pop(), V.T_DROP + 0.4, 0.4)
    # 19.3–25.4: Crumb sits alone; Dill pats; sad violin
    A6.sad_violin(V.T_SITDOWN, mix)
    for k in range(3):
        place(mix, E.gib(1, 70, spread=2, syl=0.12, bright=0.3), V.T_SITDOWN + 0.5 + 0.5 * k, 0.3)   # sniffles
    for k in range(4):
        place(mix, A6.snare() * 0.3 if hasattr(A6, "snare") else pat(), V.T_SHUFFLE + 0.25 * k, 0.15)
    for pt in V.PATS:
        place(mix, pat(), pt, 0.8)
    place(mix, chord([60, 63, 67], 1.5), V.T_LEAN, 0.15)
    place(mix, sweep(900, 700, 0.3, vdepth=0) * 0.3, V.T_LEAN + 0.4, 0.3)
    # 25.4–31: the Duck's one motion; Peep runs home
    place(mix, E.squeak(0.5), V.T_DTILT + 0.2, 0.7)
    place(mix, sweep(700, 900, 0.3, vdepth=0) * 0.3, V.T_PTILT, 0.3)
    place(mix, peep(), V.T_GAZE + 0.1, 0.5)
    place(mix, peep(), V.T_LOVE2 + 0.2, 0.8)
    flaps(mix, V.T_RUN, V.T_HUG, 0.05, 0.5)
    place(mix, sweep(500, 1200, V.T_HUG - V.T_RUN, vdepth=0) * 0.3, V.T_RUN, 0.4)
    place(mix, thud(), V.T_HUG, 0.4)
    harp(V.T_HUG, mix, gain=0.3)
    place(mix, chord([60, 64, 67, 72], 1.6), V.T_HUG + 0.1, 0.25)
    place(mix, ooh(1.2), V.T_HUG + 0.3, 0.4)        # "awww"
    for k in range(6):
        place(mix, pop(), V.T_HUG + 0.15 + 0.2 * k, 0.15)
    # 31–38.5: the vent glows; frost creeps to the Duck; ice crown
    tmp = np.zeros(N); place(tmp, icy(7.4), V.T_GLOW - 0.1, 0.5); mix += tmp
    place(mix, drone(7.0), V.T_GLOW, 0.35)
    place(mix, crackle(V.T_REACH - V.T_CREEP), V.T_CREEP, 0.6)
    for k in range(6):
        place(mix, tinkle() * 0.5, V.T_ICROWN + 0.1 * k, 0.4)
    place(mix, sweep(400, 1600, 0.6, vdepth=0) * 0.3, V.T_ICROWN, 0.35)
    for k in range(4):
        place(mix, gasp(), V.T_GASP + 0.06 * k, 0.45)
    place(mix, sting(), V.T_GASP, 0.6)
    place(mix, crackle(0.8), V.T_FROSTCAP, 0.4)
    for i, m in enumerate([84, 88, 91, 96]):
        place(mix, plink(midi(m)), V.T_SHINE + 0.06 * i, 0.35)
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
