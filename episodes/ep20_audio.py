"""Sound for FRIDGE KINGDOM Ep20 "The Ice King's Shadow" (variant B: cold open)."""
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
from ep10_audio import icy, sigh, whistle
from ep12_audio import flaps, flute
from ep14_audio import crackle
from ep15_audio import chatter
from ep16_audio import slide_whistle
from ep18_audio import wind, scream, footstep
from ep19_audio import shatter, warm_breath
from audio import SR, tarr, midi, place, plink, pluck, marimba, sweep, whoosh, thud, pop, ding, sting, boing, bonk, lowpass
import ep20 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A5.N = N
rng = np.random.default_rng(2020)


def roar(d):
    """Huge frosty roar: low growl + roaring wind noise."""
    t = tarr(d)
    f = 70 + 25 * np.sin(2 * np.pi * 2.5 * t) + rng.standard_normal(len(t)).cumsum() * 0.0
    g = np.sin(2 * np.pi * np.cumsum(f) / SR)
    g = np.sign(g) * np.abs(g) ** 0.5
    n = lowpass(rng.standard_normal(len(t)), 0.12) * 2.5
    env = np.minimum(1, t / 0.15) * np.minimum(1, (d - t) / 0.4)
    return (g * 0.6 + n * 0.5) * env


def inhale(d):
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.05) * 3
    return n * (t / d) ** 2 * 0.6


def skid(d=0.5):
    t = tarr(d)
    n = rng.standard_normal(len(t)) * 0.4
    s = np.sin(2 * np.pi * (2600 - 800 * t / d) * t) * 0.2
    return lowpass(n, 0.5) * np.exp(-t * 3) + s * np.exp(-t * 4)


def heroic(start, mix, gain=0.32):
    """A rising heroic swell: brass-ish triads climbing, then a held major chord."""
    seq = [(60, 64, 67), (62, 65, 69), (64, 67, 71), (65, 69, 72), (67, 71, 74), (72, 76, 79)]
    for i, ch in enumerate(seq):
        d = 0.32 if i < len(seq) - 1 else 1.4
        for m in ch:
            place(mix, sweep(midi(m), midi(m), d, vib=5, vdepth=0.006, shape="saw") * 0.18, start + i * 0.3, gain)


def chase(start, end, mix, gain=0.26):
    """Minor-key chase ostinato."""
    mel = [0, 3, 7, 3, 0, 3, 8, 7, 0, 3, 7, 10, 8, 7, 3, 2]
    at, i = start, 0
    while at < end:
        place(mix, pluck(midi(69 + mel[i % 16]), 0.18, 0.6), at, gain)
        if i % 2 == 0:
            place(mix, marimba(midi(45 + [0, 0, -4, -2][(i // 4) % 4]), 0.3), at, gain * 1.3)
        i += 1; at += 0.13


def build(path):
    mix = np.zeros(N)
    # A: the roar (cold open)
    place(mix, drone(V.T_B), 0.0, 0.45)
    place(mix, wind(V.T_B + 0.3), 0.0, 0.35)
    place(mix, chatter(1.2), 0.1, 0.3)                                        # teeth chattering
    place(mix, violin_tremolo(1.2, 52), 0.0, 0.25)
    place(mix, inhale(V.T_ROAR - V.T_INHALE), V.T_INHALE, 0.7)
    place(mix, roar(V.T_ROAR_END - V.T_ROAR), V.T_ROAR, 0.95)
    place(mix, wind(V.T_ROAR_END - V.T_ROAR), V.T_ROAR, 0.6)
    place(mix, scream(1.0, 70), V.T_ROAR + 0.3, 0.25)
    place(mix, skid(0.9), V.T_ROAR + 0.2, 0.3)
    place(mix, E.gib(2, 66, spread=8, syl=0.08, bright=0.9), V.T_FLEE, 0.4)  # run!
    place(mix, skid(0.35), V.T_HALT, 0.5)
    place(mix, sting() * 0.5, V.T_HALT + 0.05, 0.4)
    place(mix, whoosh(0.4), V.T_BACK, 0.4)
    place(mix, thud(), V.T_GRAB, 0.5)
    place(mix, E.gib(3, 50, spread=2, syl=0.12, bright=0.4), V.T_GRAB + 0.05, 0.5)   # HNNNG
    for k in range(3):
        place(mix, footstep() * 0.4, V.T_DRAG + 0.22 * k, 0.3)
    # B: the chase
    place(mix, whoosh(0.4), V.T_B - 0.2, 0.5)
    chase(V.T_B, V.T_C, mix)
    for k in range(int((V.T_C - V.T_B) / 0.18)):
        place(mix, footstep() * 0.25, V.T_B + 0.18 * k, 0.2)
    place(mix, scream(1.2, 74), V.T_B + 0.2, 0.3)
    place(mix, sweep(1800, 500, 0.3, vdepth=0) * 0.25, V.T_ICE1, 0.35)
    place(mix, shatter(), V.T_ICE1_LAND, 0.8)
    place(mix, E.gib(1, 78, spread=2, syl=0.08, bright=0.7), V.T_ICE1_LAND + 0.1, 0.35)  # eep
    place(mix, violin_tremolo(1.0, 58), V.T_CLAW - 0.3, 0.35)
    place(mix, whoosh(0.5), V.T_CLAW, 0.5)
    place(mix, pop(), V.T_YOINK, 0.7)
    place(mix, sweep(400, 1600, 0.2, vdepth=0) * 0.3, V.T_YOINK, 0.4)            # yoink
    place(mix, clink(), V.T_CLAW_SHUT, 0.6)
    place(mix, sweep(2000, 500, 0.3, vdepth=0) * 0.25, V.T_ICE2, 0.35)
    place(mix, shatter(), V.T_ICE2_LAND, 1.0)
    place(mix, thud(), V.T_ICE2_LAND, 0.7)
    place(mix, gasp(), V.T_LOOKB, 0.5)
    # C: the crack
    place(mix, whoosh(0.4), V.T_C - 0.2, 0.4)
    place(mix, crackle(0.5), V.T_CRACK, 1.0)
    place(mix, bonk() * 0.5, V.T_CRACK, 0.5)
    place(mix, rumble(0.6), V.T_CRACK + 0.05, 0.5)
    place(mix, skid(0.45), V.T_SKID, 0.6)
    place(mix, E.gib(2, 62, spread=4, syl=0.1, bright=0.5), V.T_SKID + 0.1, 0.35)  # whoa
    place(mix, sweep(900, 300, 0.4, vdepth=0) * 0.3, V.T_SLIP, 0.4)
    place(mix, thud() * 0.6, V.T_SLIP + 0.15, 0.4)
    place(mix, E.gib(3, 70, spread=10, syl=0.08, bright=0.9), V.T_OVER, 0.5)    # yelp
    place(mix, pluck(midi(40), 0.3, 0.3), V.T_CATCH, 0.5)
    place(mix, violin_tremolo(V.T_FALL - V.T_CATCH, 60), V.T_CATCH, 0.3)
    place(mix, skid(0.4), V.T_DILL_IN, 0.4)
    place(mix, E.gib(4, 56, spread=6, syl=0.09, bright=0.5), V.T_TEETER, 0.4)   # whoa-whoa
    place(mix, sweep(500, 300, 0.3, vdepth=0) * 0.3, V.T_YANK, 0.4)
    place(mix, E.gib(2, 52, spread=2, syl=0.18, bright=0.3), V.T_REACH2, 0.4)   # nnngh
    place(mix, plink(midi(88)), V.T_DRIP + 0.42, 0.5)                           # plip
    place(mix, E.gib(1, 64, spread=1, syl=0.12, bright=0.4), V.T_DRIP + 0.6, 0.3)
    place(mix, sweep(700, 600, 0.5, vdepth=0) * 0.25, V.T_SLIPGRIP, 0.35)
    place(mix, scream(1.3, 76), V.T_FALL, 0.5)
    place(mix, slide_whistle(1400, 400, 1.0) * 0.4, V.T_FALL, 0.4)
    place(mix, gasp(), V.T_FALL + 0.05, 0.5)
    # D: Peep's flight
    place(mix, peep(), V.T_PJUMP, 0.9)
    place(mix, peep(), V.T_PJUMP + 0.15, 0.8)
    place(mix, whoosh(0.6), V.T_PJUMP + 0.3, 0.5)
    flaps(mix, V.T_PJUMP + 0.2, V.T_LAND, rate=0.07, gain=0.45)
    place(mix, thud() * 0.5, V.T_GRABP, 0.5)
    place(mix, violin_tremolo(V.T_POWER - V.T_GRABP, 64), V.T_GRABP, 0.35)
    place(mix, E.gib(3, 82, spread=3, syl=0.1, bright=0.8), V.T_GRABP + 0.3, 0.3)   # strain
    place(mix, shimmer(1.2), V.T_POWER, 0.6)
    place(mix, ding(), V.T_POWER, 0.4)
    heroic(V.T_POWER + 0.1, mix, 0.4)
    flute(V.T_RISE, V.T_TOP, mix, gain=0.25)
    place(mix, thud() * 0.5, V.T_LAND, 0.5)
    place(mix, E.fanfare(), V.T_CHEER, 0.45)
    place(mix, E.gib(4, 64, spread=10, syl=0.09, bright=1.0), V.T_CHEER + 0.05, 0.45)   # YAAAY
    place(mix, E.gib(3, 72, spread=6, syl=0.08, bright=0.8), V.T_CHEER + 0.1, 0.35)
    place(mix, peep(), V.T_HUG, 0.7)
    place(mix, E.gib(2, 58, spread=3, syl=0.22, bright=0.4), V.T_HUG + 0.3, 0.35)   # awww
    for k in range(3):
        place(mix, plink(midi(84 - 3 * k)), V.T_HUG + 0.6 + 0.25 * k, 0.25)          # Chip drips
    place(mix, rumble(0.7), V.T_EYESD, 0.7)
    place(mix, sting(), V.T_EYESD + 0.1, 0.5)
    place(mix, E.gib(2, 70, spread=8, syl=0.08, bright=0.9), V.T_RUND, 0.4)
    # E: the freezer door
    place(mix, whoosh(0.4), V.T_E - 0.2, 0.4)
    for k in range(4):
        place(mix, footstep() * 0.3, V.T_E + 0.18 * k, 0.25)
    place(mix, sweep(200, 120, 0.4, vdepth=0) * 0.3, V.T_DOPEN - 0.1, 0.5)   # door suction
    place(mix, E.choir(2.2), V.T_DOPEN, 0.6)
    place(mix, E.gib(2, 60, spread=3, syl=0.25, bright=0.4), V.T_DOPEN + 0.3, 0.3)   # ooooh
    place(mix, whoosh(0.9), V.T_HAND, 0.5)
    place(mix, clink(), V.T_HGRIP, 0.5)
    whistle(V.T_WHISTLE, mix)
    for k, d in enumerate((0.0, 0.15, 0.35)):
        place(mix, boing(), V.T_BOARD + d, 0.35)
    place(mix, E.gib(2, 50, spread=3, syl=0.12, bright=0.6), V.T_PUSH, 0.4)
    place(mix, skid(V.T_LAUNCH - V.T_PUSH) * 0.6, V.T_PUSH, 0.4)
    mix += E.bouncy(V.T_PUSH, V.T_LAUNCH, base=64, gain=0.25)
    place(mix, whoosh(0.5), V.T_SWIPE - 0.2, 0.5)
    place(mix, clink(), V.T_SWIPE + 0.15, 0.5)
    place(mix, whoosh(0.9), V.T_LAUNCH, 0.7)
    place(mix, E.gib(4, 72, spread=8, syl=0.09, bright=1.0), V.T_LAUNCH + 0.05, 0.5)   # WHEEE
    # F: outside
    place(mix, E.choir(1.2), V.T_F, 0.35)
    place(mix, sweep(600, 1400, V.T_APEX - V.T_F, vdepth=0.01) * 0.35, V.T_F, 0.35)
    place(mix, slide_whistle(1500, 250, V.T_G - V.T_FALLF + 0.5) * 0.5, V.T_FALLF, 0.5)
    place(mix, scream(V.T_G - V.T_FALLF, 74), V.T_FALLF, 0.4)
    place(mix, scream(V.T_G - V.T_FALLF - 0.2, 66), V.T_FALLF + 0.1, 0.35)
    # G: into the fridge
    place(mix, whoosh(0.8), V.T_G - 0.1, 0.5)
    place(mix, scream(V.T_FREEZE - V.T_G, 78), V.T_G, 0.35)
    place(mix, E.squeak(0.35), V.T_DUCK, 0.6)
    place(mix, plink(midi(100)), V.T_DUCK + 0.6, 0.35)
    place(mix, drone(V.END_T - V.T_FREEZE), V.T_FREEZE, 0.5)
    for k, d in enumerate(V.DUNS):
        place(mix, dun([43, 42, 38][k]), d, 1.1)
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    mix += E.hum() * 0.2
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.9
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
