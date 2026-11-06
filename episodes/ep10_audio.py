"""Sound for FRIDGE KINGDOM Ep10 "Hide the Chick" (variant B: cold open)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
from ep3_audio import tick, knock, run_music
from ep4_audio import chord
from ep5_audio import violin_tremolo, drone
import ep6_audio as A6
from ep7_audio import gasp, peep
from ep8_audio import shimmer, dun
from ep9_audio import footstep
from audio import SR, tarr, midi, place, plink, sweep, whoosh, bonk, thud, pop, marimba, boing, ding, lowpass, sting
import ep10 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A6.N = N
import ep3_audio as A3
A3.N = N
rng = np.random.default_rng(1010)


def squish(d=0.4):
    t = tarr(d)
    f = 500 - 350 * t / d
    ph = 2 * np.pi * np.cumsum(f) / SR
    n = lowpass(rng.standard_normal(len(t)), 0.25)
    return (np.sin(ph) * 0.4 + n * 0.6) * np.sin(np.pi * t / d) * 0.8


def cork_pop():
    out = np.zeros(int(SR * 0.3))
    place(out, pop(), 0, 1.2)
    place(out, sweep(400, 1600, 0.18, vdepth=0) * np.exp(-tarr(0.18) * 8)[:len(sweep(400, 1600, 0.18, vdepth=0))], 0, 0.5)
    return out


def sigh(base=55):
    t = tarr(0.8)
    f = midi(base) * (1.1 - 0.25 * t / 0.8)
    ph = 2 * np.pi * np.cumsum(f) / SR
    n = lowpass(rng.standard_normal(len(t)), 0.2)
    voice = (np.sin(ph) * 0.35 + 0.15 * np.sin(2 * ph)) * np.sin(np.pi * t / 0.8)
    return (voice + n * 0.35 * np.sin(np.pi * t / 0.8)) * 0.8


def icy(d):
    """Cold wind + glassy shimmer."""
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.04) * 2.0
    env = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)
    out = n * env * 0.25
    sh = shimmer(d)[:len(t)]
    out[:len(sh)] += sh * 0.8
    return out


def tik():
    out = knock() * 0.25
    place(out, tick(3200), 0, 1.2)
    return out


def whistle(start, mix):
    for i, m in enumerate([79, 83, 81, 86]):
        place(mix, sweep(midi(m), midi(m) * 1.02, 0.18, vib=7, vdepth=0.01) * 0.25, start + i * 0.2, 0.6)


def build(path):
    mix = E.hum() * 0.5
    # 0–3.8: door bursts open, choir, panic
    place(mix, E.choir(3.2), 0.0, 0.6)
    mix += run_music(0.2, 3.9, base=60, gain=0.24)
    place(mix, E.gib(6, 72, spread=6, syl=0.07), 0.3, 0.5)           # Dill AAAH
    place(mix, E.gib(5, 80, spread=4, syl=0.06), 1.6, 0.45)          # Crumb EEEK
    place(mix, peep(), 2.9, 0.6); place(mix, peep(), 3.1, 0.5)
    for t0 in np.arange(0.4, 3.8, 0.35):
        place(mix, thud(), t0, 0.12)
    place(mix, sweep(900, 300, 0.4, vdepth=0) * 0.4, V.T_SKID, 0.5)  # skid
    # 4.6–6.6: into the carton
    place(mix, boing(), V.T_BOOST, 0.5)
    place(mix, squish(0.45), V.T_IN, 0.9)
    place(mix, sweep(300, 220, 0.4, vdepth=0) * 0.3, 5.95, 0.4)
    place(mix, sweep(300, 200, 0.4, vdepth=0) * 0.4, 6.3, 0.5)
    place(mix, E.gib(2, 70, spread=2, syl=0.14, bright=0.3), V.T_HIDDEN + 0.25, 0.4)   # phew
    place(mix, cork_pop(), V.T_POP, 1.0)
    place(mix, E.splat(), V.T_POP + 0.05, 0.4)
    place(mix, sweep(600, 1500, 0.5, vdepth=0) * 0.35, V.T_POP + 0.05, 0.4)
    place(mix, thud(), V.T_LAND, 0.4); place(mix, peep(), V.T_LAND + 0.15, 0.6)
    # 7.6–9.4: the Hand comes; napkin
    place(mix, E.choir(4.0), 7.6, 0.45)
    place(mix, E.gib(3, 64, spread=5, syl=0.06), 7.45, 0.4)
    place(mix, whoosh(0.5), V.T_FLING, 0.9)
    place(mix, sweep(1200, 500, 0.3, vdepth=0) * 0.3, V.T_DRAPE, 0.4)
    whistle(8.7, mix)
    # 10.6–13: pinch, lift, nothing
    place(mix, violin_tremolo(V.T_EMPTY - V.T_H1, 74), V.T_H1, 0.5)
    place(mix, plink(midi(88)), V.T_PINCH, 0.3)
    place(mix, sweep(400, 900, 1.0, vdepth=0) * 0.25, V.T_LIFT, 0.4)
    place(mix, gasp(), V.T_EMPTY, 1.0); place(mix, gasp(), V.T_EMPTY + 0.04, 0.6)
    place(mix, plink(midi(76)), V.T_EMPTY + 0.4, 0.4); place(mix, plink(midi(71)), V.T_EMPTY + 0.6, 0.4)
    # 13: whip pan; jewel ting
    place(mix, whoosh(0.35), V.T_WHIP - 0.05, 0.9)
    place(mix, ding(), V.T_WHIP + 0.4, 0.6)
    # 14.8–18.2: tense hover, tick-tock
    place(mix, drone(V.T_AWAY - V.T_HOVER + 0.2), V.T_HOVER - 0.2, 0.6)
    for i, t0 in enumerate([15.0, 15.6, 16.2, 16.8, 17.4]):
        place(mix, tick(2400 if i % 2 == 0 else 1800), t0, 0.9)
    place(mix, E.squeak(0.2), V.T_CUFF, 0.2)                         # the cufflink Duck turns
    place(mix, sweep(700, 500, 0.6, vdepth=0) * 0.2, 17.2, 0.4)       # finger lowers
    # 18.2–22.6: takes the dish, brings fresh butter
    place(mix, whoosh(0.5), V.T_AWAY, 0.6)
    place(mix, A6.clang(), V.T_DGRIP, 0.4)
    place(mix, E.gib(4, 60, spread=3, syl=0.14, bright=0.4), V.T_DLIFT + 0.2, 0.5)   # NOOO
    place(mix, sweep(900, 400, 0.6, vdepth=0) * 0.3, V.T_BACK, 0.3)
    place(mix, E.choir(1.2), V.T_BACK, 0.5)
    place(mix, thud(), V.T_SET, 0.8); place(mix, knock(), V.T_SET, 0.5)   # CLUNK
    # 23: joy, fanfare
    place(mix, E.fanfare(), V.T_JOY + 0.1, 0.9)
    place(mix, boing(), 23.5, 0.4)
    place(mix, E.gib(5, 74, spread=5, syl=0.07), V.T_JOY, 0.4)
    # 24.6: door closes; sighs
    place(mix, footstep(), V.T_CLOSE, 1.0)
    for i, ts in enumerate(V.T_SIGHS):
        place(mix, sigh([55, 64, 50, 72, 45][i]), ts, 0.8)
    place(mix, boing(), V.T_SIGHS[4] + 0.1, 0.25)                     # jello wobble
    # 27.8–34: frost
    place(mix, icy(V.T_TAPS[0] - V.T_PUFF), V.T_PUFF, 1.0)
    place(mix, sweep(2000, 900, 1.0, vdepth=0) * 0.2, V.T_PUFF, 0.5)
    for i, m in enumerate([76, 79, 83, 86, 88]):
        place(mix, plink(midi(m)), V.T_UP + 0.9 + i * 0.25, 0.25)
    for t0 in np.arange(V.T_DOWN + 0.8, V.T_TAPS[0] - 0.2, 0.09):    # teeth chattering
        place(mix, tick(1500), t0, 0.25)
    place(mix, E.gib(3, 86, spread=2, syl=0.06), V.T_SNEEZE - 0.15, 0.4)
    place(mix, peep(), V.T_SNEEZE + 0.05, 0.9); place(mix, pop(), V.T_SNEEZE + 0.05, 0.3)
    # 34.8: tik tik tik from above, then sting
    for tt in V.T_TAPS:
        place(mix, tik(), tt, 1.0)
    place(mix, sting(), V.T_STING, 0.8)
    place(mix, dun(38), V.T_STING, 0.6)
    place(mix, chord([50, 53, 56], 1.4), V.T_STING + 0.1, 0.4)
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    out = np.tanh(mix * 1.1)
    tt = np.arange(N) / SR
    # hush right before the taps
    out *= 1 - 0.7 * np.clip((tt - (V.T_TAPS[0] - 0.4)) / 0.1, 0, 1) * np.clip((V.T_TAPS[0] - tt) / 0.02, 0, 1)
    out = out / np.max(np.abs(out)) * 0.9
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
