"""Sound for FRIDGE KINGDOM Ep13 "Knock From Above" (variant A: title card first)."""
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
from ep8_audio import shimmer, dun, clink
from ep10_audio import tik, icy, sigh
from ep11_audio import ooh, harp
from ep12_audio import flaps
from ep3_audio import knock
import ep3_audio as A3
from audio import SR, tarr, midi, place, plink, sweep, whoosh, bonk, thud, pop, marimba, boing, ding, lowpass, sting
import ep13 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A2.N = N
A6.N = N
A3.N = N
rng = np.random.default_rng(1313)


def tok():
    """Wooden cane rap on the metal grille."""
    out = knock() * 0.6
    t = tarr(0.15)
    place(out, np.sin(2 * np.pi * 900 * t) * np.exp(-t * 40) * 0.4, 0, 1.0)
    return out


def creak(d=0.6):
    t = tarr(d)
    f = 180 + 60 * np.sin(2 * np.pi * 3 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    saw = (ph / np.pi) % 2 - 1
    return lowpass(saw, 0.2) * np.sin(np.pi * t / d) * 0.6


def tinkle():
    t = tarr(0.6)
    return sum(np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, k in ((2400, 6), (3700, 9), (5200, 12))) * 0.3


def build(path):
    mix = E.hum() * 0.5
    # title card: three tiks
    place(mix, E.fanfare(), 0.1, 0.5)
    for t0 in (0.5, 0.9, 1.3):
        place(mix, tik(), t0, 0.8)
    # 2.0–6.4: Dill declares war; tapping answers, faster and faster
    mix += A2.war_drum(V.T_START, 8, 0.32) * 0.7
    place(mix, E.gib(6, 50, spread=6, syl=0.08, bright=0.8), V.T_START + 0.05, 0.6)
    place(mix, pop(), V.T_BUB, 0.4)
    place(mix, peep(), V.T_SALUTE, 0.6); place(mix, ding(), V.T_SALUTE + 0.1, 0.3)
    for tt in V.TIK_RUN:
        place(mix, tik(), tt, 0.95)
    place(mix, violin_tremolo(V.T_WHISTLE - V.T_FAST, 70) * 0.8, V.T_FAST, 0.25)
    place(mix, E.gib(2, 60, spread=3, syl=0.07, bright=1.0), V.T_FAST + 0.1, 0.45)
    # 6.4–12.6: whistle; pickles leap into a pyramid; Dill climbs; TINK; Peep lands; creak
    for i, m in enumerate([84, 88]):
        place(mix, sweep(midi(m), midi(m) * 1.03, 0.18, vib=7, vdepth=0.01) * 0.3, V.T_WHISTLE + i * 0.2, 0.6)
    A6.march(V.LEAP_T[0] - 0.2, V.CLIMB_T[-1] + 0.4, mix, gain=0.3)
    for t0 in V.LEAP_T:
        place(mix, sweep(400, 1100, 0.3, vdepth=0) * 0.4, t0, 0.35)
        place(mix, boing(), t0 + V.LEAP_D - 0.05, 0.45)
    for t0 in V.CLIMB_T:
        place(mix, marimba(midi(67 + 4 * V.CLIMB_T.index(t0)), 0.3), t0 + 0.3, 0.4)
        place(mix, E.gib(1, 44, spread=2, syl=0.08, bright=0.5), t0, 0.35)
    place(mix, E.fanfare(), V.CLIMB_T[-1] + 0.35, 0.4)
    place(mix, tinkle(), V.T_POKE, 0.8); place(mix, clink(), V.T_POKE, 0.5)
    place(mix, cricket_chirp(), V.T_POKE + 0.5, 0.3)
    flaps(mix, V.T_PEEP_UP, V.T_PEEP_ON, 0.05, 0.5)
    place(mix, peep(), V.T_PEEP_UP + 0.1, 0.5)
    place(mix, thud(), V.T_PEEP_ON, 0.5)
    place(mix, creak(0.5), V.T_WOB + 0.1, 0.6); place(mix, creak(0.4), V.T_WOB + 0.4, 0.6)
    # 12.6–13.9: collapse
    place(mix, sweep(1500, 300, V.T_CRASH - V.T_FALL, vdepth=0) * 0.5, V.T_FALL, 0.5)
    place(mix, E.gib(5, 70, spread=6, syl=0.05, bright=1.0), V.T_FALL + 0.05, 0.4)
    place(mix, E.crash(), V.T_CRASH, 0.9); place(mix, bonk(), V.T_CRASH, 0.6); place(mix, thud(), V.T_CRASH + 0.05, 0.7)
    place(mix, pop(), V.T_CRASH + 0.02, 0.4)
    place(mix, shimmer(0.7), V.T_CRASH + 0.1, 0.3)
    # 13.9–16.05: Grandma sighs, hobbles, springs, hooks the grille
    place(mix, sigh(52), V.T_SIGH, 0.6)
    for k in range(7):
        place(mix, knock() * 0.3, V.T_HOBBLE + 0.13 * k, 0.4)
    place(mix, sweep(300, 220, 0.3, vdepth=0) * 0.4, V.T_CROUCH, 0.3)
    place(mix, boing(), V.T_SPRING, 1.0)
    place(mix, sweep(500, 1600, V.T_HOOK - V.T_SPRING, vdepth=0) * 0.5, V.T_SPRING, 0.45)
    place(mix, A6.clang(), V.T_HOOK, 0.6)
    for k, t0 in enumerate((V.T_HOOK + 0.2, V.T_HOOK + 0.3, V.T_HOOK + 0.4)):
        place(mix, gasp(), t0, 0.35)
    # 16.05–24.6: the conversation (silence around it)
    for tt in V.TOKS + V.TOKS2:
        place(mix, tok(), tt, 1.0)
    for tt in V.TIKS1 + V.TIKS2:
        place(mix, tik(), tt, 1.1)
    tmp = np.zeros(N); place(tmp, icy(6.0), V.TIKS1[0] - 0.2, 0.25); mix += tmp
    place(mix, peep(), V.TIKS1[-1] + 0.4, 0.3)
    place(mix, E.gib(2, 40, spread=2, syl=0.16, bright=0.3), V.T_NOD + 0.1, 0.5)   # "hm."
    place(mix, chord([48, 55, 60], 1.0), V.T_NOD, 0.2)
    # 24.6–27.7: floats down; Dill wants war again; BONK
    place(mix, sweep(900, 1100, 1.2, vib=3, vdepth=0.05) * 0.3, V.T_UNHOOK + 0.1, 0.3)
    place(mix, whoosh(0.4), V.T_UNHOOK, 0.4)
    place(mix, thud(), V.T_LAND, 0.4)
    mix += A2.war_drum(V.T_MARCH, 3, 0.25) * 0.6
    place(mix, E.gib(4, 52, spread=5, syl=0.08, bright=0.8), V.T_MARCH + 0.1, 0.55)
    place(mix, bonk(), V.T_BONK, 1.0)
    place(mix, sweep(1600, 300, 0.6, vdepth=0) * 0.6, V.T_BONK + 0.05, 0.5)   # slide whistle
    place(mix, shimmer(0.8), V.T_BONK + 0.1, 0.4)
    # 27.7–31.0: the frozen kingdom; ooh; brrr
    harp(V.T_EXPLAIN, mix, gain=0.25)
    place(mix, ooh(1.6), V.T_EXPLAIN + 0.7, 0.45)
    place(mix, chord([57, 60, 64, 69], 2.4), V.T_EXPLAIN + 0.2, 0.18)
    for k in range(4):   # brrr: teeth chatter
        place(mix, E.gib(6, 62 + 3 * k, spread=1, syl=0.03, gap=0.01, bright=0.4), V.T_SHIVER + 0.12 * k, 0.25)
    # 31.0–35.0: frost hand -> Duck -> snowflake
    tmp = np.zeros(N); place(tmp, icy(4.2), V.T_FROST - 0.1, 0.45); mix += tmp
    for k in range(10):
        place(mix, tinkle() * 0.5, V.T_FROST + 0.11 * k, 0.4)
    place(mix, gasp(), V.T_FROST + 0.8, 0.5); place(mix, gasp(), V.T_FROST + 0.9, 0.4)
    place(mix, sting(), V.T_FROST + 0.8, 0.35)
    place(mix, shimmer(0.7), V.T_DUCKF - 0.1, 0.5)
    place(mix, E.squeak(0.35), V.T_DTURN, 0.55)
    place(mix, shimmer(0.9), V.T_FLAKE - 0.1, 0.5)
    for i, m in enumerate([84, 88, 91, 96]):
        place(mix, plink(midi(m)), V.T_FLAKE + 0.08 * i, 0.3)
    # 35.0–38.5: push in on the vent... silence... the eye
    place(mix, drone(2.8), V.T_PUSH, 0.4)
    place(mix, sweep(400, 900, 0.5, vdepth=0) * 0.25, V.T_EYE, 0.3)
    place(mix, sting(), V.T_STING, 0.8)
    place(mix, sweep(700, 500, 0.15, vdepth=0) * 0.3, V.T_BLINK, 0.4)   # blink
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
