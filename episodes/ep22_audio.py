"""Sound for FRIDGE KINGDOM Ep22 "Two Ducks" (variant B: cold open)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
import ep5_audio as A5
from ep5_audio import violin_tremolo, drone, cricket_chirp
from ep6_audio import record_scratch
from ep7_audio import gasp, peep, echo
from ep8_audio import shimmer, dun, clink
from ep10_audio import icy, squish
from ep14_audio import crackle
from ep16_audio import slide_whistle
from ep18_audio import footstep, minor_choir, scream
from ep19_audio import shatter
from audio import SR, tarr, midi, place, plink, pluck, marimba, sweep, whoosh, thud, pop, ding, sting, boing, lowpass, bonk
import ep22 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A5.N = N
rng = np.random.default_rng(2222)


def quick_squeak(d=0.22, base=1050, gain=1.0):
    """Squeak's voice: a fast, bright rubber squeak (higher and bouncier than the Duck's)."""
    t = tarr(d)
    f = base + 650 * np.sin(np.pi * t / d) ** 0.8
    f *= 1 + 0.04 * np.sin(2 * np.pi * 23 * t)
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) + 0.45 * np.sin(2 * ph) + 0.25 * np.sign(np.sin(ph))
    env = np.minimum(1, t / 0.02) * np.minimum(1, (d - t) / 0.05)
    return s * env * 0.42 * gain


def muffled(d=0.25):
    return lowpass(quick_squeak(d, 800), 0.05) * 2.5


def shake(d=1.0):
    """Wet-dog shake: rapid flappy noise bursts."""
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.3)
    return n * (0.5 + 0.5 * np.sign(np.sin(2 * np.pi * 14 * t))) * np.exp(-t * 1.2) * 0.6


def crack():
    t = tarr(0.35)
    n = rng.standard_normal(len(t)) * np.exp(-t * 18)
    c = np.sin(2 * np.pi * 2400 * t) * np.exp(-t * 30) * 0.4
    return n * 0.9 + c


def tiptoe_music(start, end, mix, gain=0.22):
    """Sneaky pizzicato while the Hand hovers (tick, tock)."""
    mel = [57, 0, 60, 0, 57, 0, 64, 0, 62, 0, 60, 0, 59, 0, 57, 0]
    at, i = start, 0
    while at < end:
        m = mel[i % 16]
        if m:
            place(mix, pluck(midi(m), 0.25, 0.3), at, gain)
        if i % 4 == 0:
            place(mix, marimba(midi(45), 0.4), at, gain * 0.8)
        at += 0.25; i += 1


def build(path):
    mix = np.zeros(N)
    # cold open: the ice cracks and bursts
    place(mix, drone(V.T_SHATTER), 0.0, 0.3)
    place(mix, crackle(0.5), 0.05, 0.6)
    place(mix, crack(), V.T_CR1, 1.0)
    place(mix, crack(), V.T_CR2, 1.0)
    place(mix, crackle(0.6), V.T_CR2 + 0.1, 0.7)
    place(mix, shatter(), V.T_SHATTER, 1.1)
    place(mix, sting() * 0.5, V.T_SHATTER, 0.4)
    for k in range(6):
        place(mix, plink(midi(96 + (k * 5) % 12)), V.T_SHATTER + 0.25 + 0.12 * k, 0.3)    # shards tinkle
    # shiver, shake, ping, eyes
    place(mix, E.gib(4, 70, spread=2, syl=0.06, gap=0.01, bright=0.4), V.T_SHATTER + 0.8, 0.35)  # brrrr
    place(mix, shake(V.T_FLIP + 0.3 - V.T_SHAKE), V.T_SHAKE, 0.7)
    place(mix, ding(), V.T_FLIP, 0.55)
    place(mix, shimmer(0.6), V.T_EYES, 0.45)
    place(mix, plink(midi(100)), V.T_EYES + 0.05, 0.4)
    for k, s0 in enumerate(V.SQUEAKS_TOP):
        place(mix, quick_squeak(0.24, 1000 + 80 * k), s0 + 0.05, 0.9)
        place(mix, boing() * 0.3, s0 + 0.35, 0.25)
    # bottom shelf: everyone looks up
    for k in range(4):
        place(mix, quick_squeak(0.2, 1150), V.T_LOOK + 0.15 + 0.6 * k, 0.4)            # still squeaking upstairs
    place(mix, gasp(), V.T_LOOK + 0.1, 0.6)
    for d in V.DTAKE:
        place(mix, boing() * 0.4, d, 0.4)
    place(mix, E.gib(1, 82, spread=2, syl=0.07, bright=0.9), V.T_SEE, 0.4)                 # eep
    place(mix, sweep(300, 2000, 0.4, vdepth=0) * 0.2, V.T_SEE, 0.25)
    # the jump
    place(mix, slide_whistle(600, 1500, V.T_BOING - V.T_JUMP) * 0.4, V.T_JUMP, 0.45)
    place(mix, quick_squeak(0.5, 1200), V.T_JUMP + 0.05, 0.6)                              # wheee
    place(mix, boing(), V.T_BOING, 0.8)
    place(mix, E.splat() * 0.4, V.T_BOING, 0.3)
    place(mix, slide_whistle(1400, 500, V.T_PLONK - V.T_BOING) * 0.3, V.T_BOING + 0.05, 0.35)
    place(mix, bonk(), V.T_PLONK, 0.6)
    place(mix, squish(0.2), V.T_PLONK, 0.5)
    place(mix, whoosh(0.5), V.T_OFF, 0.3)
    place(mix, plink(midi(91)), V.T_BESIDE, 0.6)
    place(mix, record_scratch(), V.T_BESIDE + 0.2, 0.5)
    # two Ducks: Peep in love, Dill inspects
    place(mix, shimmer(1.0), V.T_LOVE, 0.4)
    place(mix, peep(), V.T_LOVE + 0.1, 0.6)
    place(mix, peep(), V.T_LOVE + 0.45, 0.5)
    place(mix, E.gib(2, 52, spread=3, syl=0.14, bright=0.5), V.T_POINT, 0.45)            # hmm?
    place(mix, cricket_chirp(), V.T_CHIRP, 0.45)
    place(mix, cricket_chirp(), V.T_CHIRP + 0.45, 0.4)
    place(mix, boing() * 0.4, V.T_ONDUCK, 0.4)
    place(mix, plink(midi(88)), V.T_DUCKLAND, 0.4)
    place(mix, pop() * 0.6, V.T_BOOP, 0.6)
    place(mix, quick_squeak(0.18, 1250), V.T_BOOP + 0.05, 0.7)
    place(mix, E.gib(2, 66, spread=8, syl=0.08, bright=0.9), V.T_HUH, 0.5)               # ?!
    place(mix, boing() * 0.4, V.T_TODILL, 0.4)
    E_b = E.bouncy(V.T_DILLLAND, V.STEPS[0] - 0.2, base=62, gain=0.22)
    mix += E_b
    for k, b in enumerate(V.BOUNCES):
        place(mix, quick_squeak(0.26, 1000 + 60 * (k % 3)), b + 0.05, 0.85)
        place(mix, squish(0.15) * 0.6, b + 0.45, 0.3)
        place(mix, peep(), b + 0.35, 0.4)
    # the footsteps
    for s0 in V.STEPS:
        place(mix, footstep(), s0, 1.2)
        place(mix, thud() * 0.5, s0, 0.6)
    place(mix, violin_tremolo(V.T_THROW - V.STEPS[0], 52), V.STEPS[0], 0.25)
    place(mix, gasp(), V.STEPS[-1] + 0.2, 0.5)
    # the scarf gag
    place(mix, whoosh(0.6), V.T_THROW, 0.5)
    for k in range(3):
        place(mix, muffled(0.2), V.T_COVER + 0.3 + 0.35 * k, 0.7)
    place(mix, E.gib(2, 50, spread=3, syl=0.12, bright=0.5), V.T_GRABB, 0.45)
    place(mix, squish(0.3), V.T_SIT, 0.5)
    place(mix, E.gib(1, 56, spread=2, syl=0.2, bright=0.4), V.T_SIT + 0.1, 0.35)       # smug hm
    place(mix, quick_squeak(0.95, 900, 1.6), V.T_BIGSQ, 1.0)                               # SQUEEEEEAK
    place(mix, boing(), V.T_BIGSQ + 0.05, 0.7)
    place(mix, scream(0.8, 70), V.T_BIGSQ + 0.1, 0.35)
    place(mix, slide_whistle(500, 1600, 0.5) * 0.3, V.T_BIGSQ + 0.1, 0.3)
    place(mix, thud(), V.T_DLAND2, 0.7)
    place(mix, plink(midi(88)), V.T_SQHOME, 0.4)
    # the Hand
    place(mix, E.choir(2.0), V.T_OPEN, 0.55)
    place(mix, whoosh(0.7), V.T_DIVE, 0.4)
    for k in range(3):
        place(mix, E.gib(1, [70, 76, 82][k], spread=2, syl=0.12, bright=0.9), V.T_DIVE + 0.1 * k, 0.35)
    place(mix, sweep(200, 90, 1.0, vdepth=0) * 0.3, V.T_HDOWN, 0.35)
    tiptoe_music(V.T_HSET, V.T_REACH, mix)
    for k, tk in enumerate(V.TICKS):
        place(mix, plink(midi(79 if k % 2 == 0 else 74)), tk, 0.45)
    place(mix, shimmer(0.4), V.T_GAZE, 0.25)
    place(mix, sting() * 0.4, V.T_GRIP, 0.4)
    place(mix, minor_choir(1.3), V.T_LIFT, 0.4)
    place(mix, whoosh(0.8), V.T_LIFT, 0.35)
    place(mix, thud(), V.T_CLOSE, 0.7)
    # the wink
    place(mix, shimmer(0.5), V.T_GLINT, 0.4)
    place(mix, plink(midi(103)), V.T_GLINT + 0.05, 0.35)
    place(mix, quick_squeak(0.22, 1100), V.T_WINK + 0.02, 0.9)
    for k, d in enumerate(V.DUNS):
        place(mix, dun([43, 42, 38][k]), d, 1.1)
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    mix += E.hum() * 0.2
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.82
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
