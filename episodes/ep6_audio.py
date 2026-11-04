"""Sound for FRIDGE KINGDOM Ep6 "The Jar Opens" (variant B: cold open, no title fanfare)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
from ep3_audio import big_thump, tick
from ep4_audio import cello, chord, trombone
from ep5_audio import violin_tremolo, drone
from audio import SR, tarr, midi, place, plink, sweep, whoosh, bonk, thud, pop, marimba, boing, ding, lowpass, pluck, sting
import ep6 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
rng = np.random.default_rng(66)


def clang():
    t = tarr(1.0)
    s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k)
            for f, a, k in [(520, 1, 4), (1370, 0.6, 6), (2290, 0.4, 9), (3410, 0.25, 12)])
    return s * 0.5


def coin_wobble(start, end, mix):
    """Lid spinning down like a coin: rattles getting faster, then a final clack."""
    at, gap = start, 0.16
    while at < end:
        place(mix, tick(1800 + rng.integers(-200, 200)), at, 0.5)
        at += gap; gap = max(0.03, gap * 0.82)
    place(mix, thud(), end, 0.5)


def snare():
    t = tarr(0.12)
    return rng.standard_normal(len(t)) * np.exp(-t * 35) * 0.5


def march(start, end, mix, gain=0.35, base=50):
    """Tiny pickle marching drum + fife."""
    fife = [7, 7, 9, 7, 12, 11, 7, 4]
    at, i = start, 0
    while at < end:
        place(mix, snare(), at, gain * (1.0 if i % 2 == 0 else 0.6))
        if i % 4 == 0:
            place(mix, thud(), at, gain * 1.3)
        if i % 2 == 0:
            place(mix, pluck(midi(base + 24 + fife[(i // 2) % 8]), 0.16, 0.3), at, gain * 0.6)
        i += 1; at += 0.2


def organ(ms, d):
    out = np.zeros(int(SR * d))
    for m in ms:
        t = tarr(d)
        ph = 2 * np.pi * midi(m) * t
        s = np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph) + 0.2 * np.sin(4 * ph)
        place(out, s * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.4), 0, 0.1)
    return out


def record_scratch():
    t = tarr(0.35)
    n = rng.standard_normal(len(t))
    f = 1200 * np.exp(-t * 6) + 200
    ph = 2 * np.pi * np.cumsum(f) / SR
    return (lowpass(n, 0.3) * 1.5 * np.sign(np.sin(ph)) + 0.4 * np.sin(ph)) * np.exp(-t * 5) * 0.6


def shhhk(d=0.35):
    t = tarr(d)
    n = rng.standard_normal(len(t)); n = n - lowpass(n, 0.3)
    return n * np.minimum(1, t / 0.03) * np.exp(-t * 4) * 0.5


def wind(start, end):
    out = np.zeros(N)
    d = end - start
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.02) * 4
    sw = 0.5 + 0.5 * np.sin(2 * np.pi * 0.35 * t) ** 2
    env = np.minimum(1, t / 0.8) * np.minimum(1, (d - t) / 0.8)
    place(out, n * sw * env * 0.35, start, 1.0)
    return out


def sad_violin(start, mix):
    mel = [(76, 0.8), (74, 0.4), (72, 0.8), (71, 0.6), (69, 1.4)]
    at = start
    for m, d in mel:
        place(mix, violin_tremolo(d + 0.1, m) * 0.9, at, 0.55)
        at += d


def build(path):
    mix = E.hum() * 0.6
    # 0–3.3: the jar. organ hold, POP, lid clatters
    place(mix, organ([38, 45, 50, 53], 2.8), 0.0, 0.8)
    place(mix, pop() * 1.6, V.T_POP, 1.0); place(mix, pop(), V.T_POP + 0.02, 0.6)
    place(mix, sweep(500, 1400, 0.5, vdepth=0), V.T_POP + 0.05, 0.25)          # lid flies up
    place(mix, clang(), 1.5, 0.7)
    coin_wobble(1.6, 2.6, mix)
    for k, t0 in enumerate(V.OUT_T):                                             # pickles hop out
        place(mix, pop(), t0, 0.35)
        place(mix, E.gib(2, 82 + k, spread=2, syl=0.06), t0 + 0.05, 0.3)
        place(mix, plink(midi(79 + 2 * k)), t0 + 0.45, 0.3)
    for t0 in (2.35, 2.6, 2.85, 3.25):                                           # Grandma's cane on the rim
        place(mix, tick(1500), t0, 0.7)
    # 2.8–5.6: tiny march along the top shelf
    march(2.8, 5.3, mix, 0.3)
    at = 3.25
    while at < 5.6:                                                              # cane taps, hobbling fast
        place(mix, tick(1400), at, 0.45); at += 0.18
    place(mix, plink(midi(96)), 3.75, 0.4); place(mix, plink(midi(100)), 3.85, 0.4)   # Dill: "!"
    place(mix, E.gib(4, 66, spread=4, syl=0.07), 3.8, 0.45)
    place(mix, whoosh(0.4), 4.0, 0.5); place(mix, thud(), 4.5, 0.7)
    for k in range(5):
        te = V.edge_t(k)
        place(mix, sweep(900, 1500, 0.3, vdepth=0), te, 0.18)                    # "wheee"
        place(mix, boing(), te + 0.38, 0.6)
        place(mix, plink(midi(84 + k)), te + 0.95, 0.3)
    # Grandma's shawl parachute: music-box float
    for i, m in enumerate([84, 88, 91, 88, 86, 83]):
        place(mix, marimba(midi(m), 0.4), 5.65 + i * 0.2, 0.25)
    place(mix, boing(), 6.9, 0.3)
    place(mix, tick(1400), 7.4, 0.5)
    # 7.4–9.4: Dill beams. triumphant swell
    place(mix, chord([60, 64, 67, 72, 76], 2.2), 7.35, 1.6)
    place(mix, E.choir(2.0), 7.4, 0.6)
    place(mix, E.gib(6, 64, spread=5, syl=0.09), 7.8, 0.5)
    # 9.4–11.3: the pickles march... right past him
    march(9.4, 11.3, mix, 0.3)
    place(mix, record_scratch(), 10.4, 1.0)
    for t0 in V.BOW_T:
        place(mix, whoosh(0.35), t0, 0.5)
    place(mix, whoosh(0.7), V.G_BOW_T, 0.5)
    place(mix, chord([62, 65, 69], 1.6), 11.7, 0.6)                              # reverent pad
    place(mix, sweep(300, 260, 0.6, vdepth=0) * 0.5, 13.65, 0.4)                 # the Duck's slow nod (creak)
    place(mix, E.gib(3, 58, spread=2, syl=0.12), 14.5, 0.35)                     # Dill: "...huh?"
    # 15.3–20: the speech, the bonk
    place(mix, sweep(400, 900, 0.3, vdepth=0), 15.3, 0.3)
    for k in range(4):
        place(mix, thud(), 15.7 + k * 0.45, 0.6)
    place(mix, E.gib(14, 60, spread=7, syl=0.08), 15.75, 0.6)
    place(mix, E.gib(3, 64, spread=2, syl=0.1), 17.55, 0.4)                      # smug "heh heh"
    place(mix, bonk() * 0.8, V.BONK_T, 0.9); place(mix, tick(2600), V.BONK_T, 0.6)
    place(mix, sweep(1400, 260, 1.0, vib=5, vdepth=0.01), V.BONK_T + 0.1, 0.35)   # slide whistle down
    for k, m in enumerate([84, 88, 91]):
        place(mix, marimba(midi(m), 0.4), V.BONK_T + 0.6 + k * 0.25, 0.3)
    # 20–23.65: the parade float, into the drawer
    place(mix, E.gib(3, 80, spread=3, syl=0.06), V.LIFT_T, 0.35)
    sad = [57, 60, 64, 62, 60, 59, 57, 55]
    for i in range(int((V.TOSS_T - V.LIFT_T - 0.4) / 0.32)):
        at = V.LIFT_T + 0.4 + i * 0.32
        place(mix, thud(), at, 0.5 if i % 2 == 0 else 0.3)
        place(mix, pluck(midi(sad[i % 8]), 0.3, 0.4), at, 0.35)
    place(mix, whoosh(0.5), V.TOSS_T, 0.6)
    place(mix, sweep(900, 300, 0.5, vdepth=0), V.TOSS_T + 0.1, 0.25)
    place(mix, shhhk(), V.TOSS_T + 0.35, 0.8)
    place(mix, big_thump(), V.THUNK_T, 1.0)
    # 23.9–25.8: Crumb's tiny goodbye
    place(mix, E.gib(2, 86, spread=1, syl=0.12, bright=0.3), 24.1, 0.35)
    trombone(24.4, mix)
    # 25.8–31: the drawer. wind, sad violin, pats
    mix += wind(25.8, 31.5)
    sad_violin(26.0, mix)
    for k in range(3):
        place(mix, thud(), 27.8 + 0.45 * k, 0.25)
    for t0 in (26.6, 28.9):   # sniffles
        tt = tarr(0.18); place(mix, lowpass(rng.standard_normal(len(tt)), 0.2) * np.sin(np.pi * tt / 0.18) * 0.8, t0, 0.4)
    place(mix, plink(midi(91)), 29.8, 0.4)
    # 31–35.8: the doodle
    place(mix, sting(), 31.3, 0.8)
    place(mix, drone(4.6), 31.2, 0.7)
    for k in range(6):
        place(mix, marimba(midi([81, 84, 88, 87, 84, 80][k]), 0.8), 32.0 + k * 0.55, 0.18)
    # 35.8: DUN DUN DUNNN
    for i, tp in enumerate((35.85, 36.55, 37.25)):
        ms = [[36, 43, 48], [35, 42, 47], [34, 41, 46, 49]][i]
        place(mix, chord([m + 12 for m in ms], 0.65 if i < 2 else 1.3), tp, 2.0)
        place(mix, cello(0.65 if i < 2 else 1.3, ms[0]), tp, 0.9)
        place(mix, big_thump(), tp, 0.8)
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.9
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
