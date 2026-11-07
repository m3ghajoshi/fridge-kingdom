"""Sound for FRIDGE KINGDOM Ep12 "Peep Learns to Fly" (variant B: cold open)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
from ep4_audio import chord
from ep5_audio import violin_tremolo, drone, cricket_chirp
import ep6_audio as A6
from ep7_audio import gasp, peep
from ep8_audio import shimmer, dun, clink
from ep10_audio import tik, icy
import ep3_audio as A3
from audio import SR, tarr, midi, place, plink, sweep, whoosh, bonk, thud, pop, marimba, boing, ding, lowpass, sting
import ep12 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A6.N = N
A3.N = N
rng = np.random.default_rng(1212)


def flap(d=0.05):
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.35)
    return n * np.sin(np.pi * t / d) * 0.6


def flaps(mix, start, end, rate=0.09, gain=0.5):
    at = start
    while at < end:
        place(mix, flap(), at, gain * float(rng.uniform(0.7, 1.0)))
        at += rate


def flute(start, end, mix, notes=(72, 74, 76, 79, 81, 84, 86, 88, 91, 93), gain=0.22):
    step = (end - start) / len(notes)
    for i, m in enumerate(notes):
        place(mix, sweep(midi(m), midi(m), step * 1.1, vib=6, vdepth=0.008) * 0.5, start + i * step, gain)


def tonk():
    t = tarr(0.5)
    s = sum(np.sin(2 * np.pi * f * t) * a * np.exp(-t * k) for f, a, k in ((420, 1, 7), (1130, 0.5, 10), (1870, 0.3, 14)))
    return s * 0.6


def build(path):
    mix = E.hum() * 0.5
    # 0–2.4: cold open: furious flapping, nothing happens
    flaps(mix, 0.0, V.T_DROOP, 0.07, 0.6)
    place(mix, E.gib(4, 74, spread=3, syl=0.06, bright=0.9), 0.2, 0.35)
    place(mix, thud(), 1.25, 0.25)
    place(mix, sweep(600, 300, 0.4, vdepth=0) * 0.4, V.T_DROOP, 0.4)     # deflate
    place(mix, cricket_chirp(), V.T_DROOP + 0.2, 0.4)
    # 2.4–4.9: the drawing of a flying Duck; it turns; Dill scoffs
    place(mix, ding(), V.T_CARD, 0.45)
    place(mix, peep(), V.T_CARD + 0.1, 0.6)
    for i, m in enumerate([72, 76, 79, 84]):
        place(mix, marimba(midi(m), 0.5), V.T_CARD + 0.25 + i * 0.12, 0.25)
    place(mix, E.squeak(0.35), V.T_DTURN, 0.5)
    place(mix, E.gib(3, 54, spread=2, syl=0.1, bright=0.9), V.T_PFFT, 0.5)
    # 4.9–7.15: Dill's flying lesson
    for k, t0 in enumerate(np.arange(V.T_DWALK, V.T_DPOSE, 0.2)):
        place(mix, marimba(midi([60, 64, 67, 64][k % 4]), 0.25), float(t0), 0.25)
    place(mix, E.fanfare(), V.T_DPOSE, 0.45)
    place(mix, whoosh(0.8), V.T_DJUMP, 0.5)
    place(mix, sweep(900, 250, 0.8, vdepth=0) * 0.6, V.T_DJUMP + 0.05, 0.45)
    place(mix, bonk(), V.T_BONK, 1.0); place(mix, thud(), V.T_BONK, 0.7)
    place(mix, shimmer(0.9), V.T_BONK + 0.1, 0.4)
    place(mix, E.gib(3, 50, spread=3, syl=0.12, bright=0.2), V.T_BONK + 0.3, 0.4)   # muffled Crumb
    # 8.3–11: Peep copies
    place(mix, sweep(400, 1600, 0.4, vdepth=0) * 0.5, V.T_PJUMP, 0.4)
    place(mix, peep(), V.T_PJUMP + 0.1, 0.5)
    place(mix, thud(), V.T_PLAND, 0.6)
    place(mix, E.gib(2, 52, spread=2, syl=0.1, bright=0.2), V.T_PLAND + 0.05, 0.4)
    place(mix, peep(), 10.2, 0.6); place(mix, peep(), 10.45, 0.6)
    # 11–18.2: training montage (bouncy music)
    mix += E.bouncy(V.T_M1, V.T_HOV, base=62, gain=0.22)
    for tm in (V.T_M1, V.T_M2, V.T_M3):
        place(mix, whoosh(0.3), tm, 0.3)
    place(mix, sweep(300, 700, 0.35, vdepth=0) * 0.5, 11.5, 0.3)
    place(mix, thud(), V.T_STOMP, 0.8); place(mix, A6.clang(), V.T_STOMP, 0.5)
    place(mix, sweep(500, 2000, 0.5, vdepth=0) * 0.6, V.T_STOMP + 0.05, 0.5)
    place(mix, peep(), V.T_STOMP + 0.3, 0.5)
    place(mix, thud(), V.T_M1_LAND, 0.7); place(mix, E.gib(2, 50, spread=2, syl=0.1, bright=0.2), V.T_M1_LAND, 0.4)
    place(mix, boing(), V.T_BOING, 0.9)
    flaps(mix, 14.1, 14.7, 0.07, 0.45)
    place(mix, E.splat(), V.T_M2_LAND, 0.7); place(mix, E.gib(2, 50, spread=2, syl=0.1, bright=0.2), V.T_M2_LAND + 0.05, 0.4)
    place(mix, sweep(900, 1100, 1.0, vib=3, vdepth=0.05) * 0.3, V.T_M3 + 0.3, 0.3)   # floaty
    place(mix, whoosh(0.4), V.T_FLIP, 0.5); place(mix, sweep(1400, 300, 0.45, vdepth=0) * 0.5, V.T_FLIP, 0.5)
    place(mix, pop(), V.T_M3_LAND, 0.6); place(mix, thud(), V.T_M3_LAND, 0.5)
    place(mix, peep(), V.T_M3_LAND + 0.45, 0.5)
    # 18.2–22.8: the hover!
    place(mix, violin_tremolo(V.T_LIFT - V.T_HOV + 0.4, 76) * 0.8, V.T_HOV, 0.3)
    flaps(mix, V.T_FLAPS, V.T_RISE, 0.045, 0.55)
    place(mix, sweep(600, 1200, 1.0, vdepth=0) * 0.3, V.T_LIFT, 0.3)
    for k, t0 in enumerate((V.T_LIFT + 0.9, V.T_LIFT + 1.0, V.T_LIFT + 1.1)):
        place(mix, gasp(), t0, 0.4)
    place(mix, E.fanfare(), V.T_CHEER, 0.8)
    place(mix, E.gib(8, 66, spread=8, syl=0.07, bright=0.9), V.T_CHEER + 0.1, 0.5)
    place(mix, E.gib(6, 58, spread=6, syl=0.08, bright=0.7), V.T_CHEER + 0.2, 0.4)
    place(mix, pop(), V.T_CHEER, 0.5)
    place(mix, peep(), V.T_CHEER + 0.6, 0.6)
    # 22.8–28.3: higher and higher (rising flute)
    flaps(mix, V.T_RISE, V.T_FREEZE, 0.06, 0.3)
    flute(V.T_RISE + 0.2, V.T_ARRIVE, mix)
    place(mix, chord([60, 64, 67, 72], 5.0), V.T_RISE + 0.2, 0.25)
    # 28.3–33.9: the vent. tik tik tik, TONK, ... tik.
    tmp = np.zeros(N); place(tmp, icy(5.5), V.T_ARRIVE, 0.35); mix += tmp
    place(mix, plink(midi(88)), V.T_ARRIVE + 0.4, 0.3)
    for tt in V.T_TIKS:
        place(mix, tik(), tt, 1.0)
    place(mix, peep(), V.T_TIKS[2] + 0.6, 0.35)
    place(mix, tonk(), V.T_BUTT, 0.9); place(mix, clink(), V.T_BUTT, 0.5)
    place(mix, tik(), V.T_REPLY, 1.3)
    place(mix, sting(), V.T_REPLY + 0.05, 0.6)
    place(mix, drone(1.2), V.T_REPLY, 0.6)
    # 33.9–36.3: wings stop. drop. THUD.
    place(mix, E.gib(5, 80, spread=4, syl=0.05, bright=1.0), V.T_DROP + 0.1, 0.4)    # AAAAA
    place(mix, sweep(1800, 250, V.T_CATCH - V.T_DROP, vdepth=0) * 0.6, V.T_DROP, 0.55)  # slide whistle
    place(mix, thud(), V.T_CATCH, 1.0); place(mix, bonk(), V.T_CATCH, 0.4)
    place(mix, E.gib(2, 50, spread=2, syl=0.1, bright=0.2), V.T_CATCH + 0.05, 0.4)
    place(mix, violin_tremolo(1.4, 64) * 0.8, V.T_CATCH + 0.3, 0.3)
    # 36.3–38.5: everyone looks up. tik. DUN DUN DUNNN
    place(mix, tik(), V.T_LASTTIK, 1.2)
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
