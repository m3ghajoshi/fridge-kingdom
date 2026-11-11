"""Sound for FRIDGE KINGDOM Ep21 "Thaw" (variant A: title card first)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
import ep5_audio as A5
from ep5_audio import violin_tremolo, drone
from ep4_audio import clonk
from ep3_audio import big_thump
from ep6_audio import sad_violin, march
from ep7_audio import gasp, peep, echo
from ep8_audio import shimmer, dun, rumble, clink
from ep10_audio import icy, sigh, squish, cork_pop
from ep14_audio import crackle, pat
from ep15_audio import sniff
from ep16_audio import slide_whistle
from ep18_audio import scream, footstep
from audio import SR, tarr, midi, place, plink, pluck, marimba, sweep, whoosh, thud, pop, ding, sting, boing, lowpass
import ep21 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A5.N = N
rng = np.random.default_rng(2121)


def splash(d=0.6):
    """Wet jello SPLOOSH: noisy burst + low wobble."""
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.25) * np.exp(-t * 7) * 1.4
    w = np.sin(2 * np.pi * (120 + 60 * np.sin(2 * np.pi * 9 * t)) * t) * np.exp(-t * 4) * 0.8
    return n + w


def wobble(d=1.2, f=8):
    t = tarr(d)
    return np.sin(2 * np.pi * (90 + 40 * np.sin(2 * np.pi * f * t)) * t) * np.exp(-t * 2.5) * 0.6


def cheerful(start, end, mix, gain=0.22):
    """Light happy ostinato for the refreeze celebration."""
    mel = [0, 4, 7, 12, 7, 4, 9, 7, 0, 4, 7, 12, 14, 12, 7, 4]
    at, i = start, 0
    while at < end:
        place(mix, marimba(midi(72 + mel[i % 16]), 0.25), at, gain)
        if i % 4 == 0:
            place(mix, pluck(midi(48 + [0, 5, 7, 5][(i // 4) % 4]), 0.4, 0.3), at, gain * 1.2)
        i += 1; at += 0.16


def build(path):
    mix = np.zeros(N)
    # title card
    place(mix, E.fanfare(), 0.2, 0.35)
    for k in range(4):
        place(mix, plink(midi(84 - 2 * k)), 0.8 + 0.3 * k, 0.25)
    # A: the crash
    place(mix, slide_whistle(1500, 300, V.T_SPLOOSH - V.T_START + 0.1) * 0.5, V.T_START, 0.5)
    place(mix, scream(V.T_SPLOOSH - V.T_START, 76), V.T_START, 0.35)
    place(mix, scream(V.T_SPLOOSH - V.T_START, 66), V.T_START + 0.05, 0.3)
    place(mix, splash(0.7), V.T_SPLOOSH, 1.0)
    place(mix, E.splat(), V.T_SPLOOSH, 0.8)
    place(mix, wobble(1.4), V.T_SPLOOSH + 0.05, 0.6)
    place(mix, boing(), V.T_SPLOOSH + 0.05, 0.6)
    place(mix, sweep(400, 1400, 0.6, vdepth=0) * 0.3, V.T_SPLOOSH + 0.1, 0.4)     # block flies up
    place(mix, E.gib(3, 70, spread=8, syl=0.08, bright=0.9), V.T_SPLOOSH + 0.1, 0.4)
    place(mix, squish(0.4), V.T_DSTUCK, 0.7)
    place(mix, lowpass(E.gib(5, 50, spread=4, syl=0.09, bright=0.4), 0.08) * 2, V.T_DSTUCK + 0.3, 0.45)  # muffled yelling
    place(mix, thud(), V.T_CRLAND, 0.6)
    place(mix, peep(), V.T_PLAND, 0.6)
    place(mix, pop(), V.T_CHLAND, 0.5)
    place(mix, sweep(1400, 300, V.T_CLONK - V.T_SPLOOSH - 0.6, vdepth=0) * 0.2, V.T_SPLOOSH + 0.7, 0.3)
    place(mix, clonk(), V.T_CLONK, 0.9)
    place(mix, clink(), V.T_CLONK + 0.05, 0.6)
    place(mix, E.gib(1, 64, spread=6, syl=0.14, bright=0.6), V.T_LOOKUP + 0.15, 0.35)      # ?
    place(mix, cork_pop(), V.T_DPOP, 0.8)
    place(mix, squish(0.4), V.T_DPOP, 0.5)
    place(mix, thud(), V.T_DLAND, 0.5)
    place(mix, peep(), V.T_PHEAD + 0.3, 0.5)
    place(mix, big_thump(), V.T_DOOR, 0.9)
    place(mix, sweep(300, 90, 0.4, vdepth=0) * 0.4, V.T_DOOR, 0.4)
    # B: Chip melts
    place(mix, drone(V.T_WILT - V.T_DOOR), V.T_DOOR + 0.2, 0.3)
    for k in range(6):
        place(mix, plink(midi(88 - 3 * k)), V.T_SLUMP + 0.2 * k, 0.35)
    place(mix, sweep(700, 200, V.T_PUDDLE - V.T_SLUMP, vdepth=0.02) * 0.3, V.T_SLUMP, 0.35)
    place(mix, E.gib(3, 72, spread=10, syl=0.12, bright=0.8), V.T_NO, 0.55)              # NOOO
    place(mix, gasp(), V.T_SLUMP + 0.1, 0.4)
    place(mix, E.gib(1, 82, spread=2, syl=0.1, bright=0.6), V.T_PUDDLE + 0.3, 0.3)         # eep...
    place(mix, whoosh(0.3), V.T_SCARF, 0.35)
    for k in range(2):
        place(mix, squish(0.25), V.T_DAB + 0.2 + 0.4 * k, 0.45)
    place(mix, squish(0.45), V.T_WRING, 0.5)
    for k in range(5):
        place(mix, plink(midi(80 + (k % 3) * 3)), V.T_WRING + 0.1 + 0.09 * k, 0.3)
    sad_violin(V.T_CRY - 0.2, mix)
    place(mix, sniff(0.55), V.T_CRY + 0.4, 0.5)
    place(mix, sniff(0.55), V.T_CRY + 1.4, 0.45)
    place(mix, E.gib(2, 60, spread=3, syl=0.2, bright=0.3), V.T_CRY + 0.9, 0.3)          # sob
    # C: Wilt's idea
    place(mix, boing(), V.T_WILT, 0.5)
    place(mix, sigh(46), V.T_WLAND + 0.1, 0.5)
    for k in range(3):
        place(mix, pat(), V.T_PAT + 0.15 + 0.28 * k, 0.6)
    place(mix, ding(), V.T_BULB, 0.6)
    place(mix, sting() * 0.4, V.T_BULB, 0.3)
    place(mix, icy(1.6), V.T_TILT + 0.2, 0.45)
    place(mix, shimmer(1.3), V.T_TILT + 0.4, 0.4)
    place(mix, E.gib(2, 58, spread=3, syl=0.25, bright=0.4), V.T_TILT + 0.7, 0.3)        # ooooh
    place(mix, E.gib(1, 60, spread=2, syl=0.12, bright=0.7), V.T_LIFT, 0.45)             # HUP
    march(V.T_MARCH, V.T_ARRIVE, mix, gain=0.3)
    for k in range(int((V.T_ARRIVE - V.T_MARCH) / 0.3)):
        place(mix, E.gib(1, 56 + 4 * (k % 2), spread=1, syl=0.08, bright=0.6), V.T_MARCH + 0.3 * k, 0.22)
        place(mix, squish(0.15) * 0.4, V.T_MARCH + 0.15 + 0.3 * k, 0.25)                 # slosh
    place(mix, sweep(600, 300, 0.25, vdepth=0) * 0.3, V.T_TIP, 0.35)
    place(mix, splash(0.4) * 0.6, V.T_SPLASH, 0.6)
    # D: refreeze
    place(mix, icy(V.T_POP - V.T_SWIRL), V.T_SWIRL, 0.55)
    place(mix, violin_tremolo(V.T_GROW - V.T_SWIRL, 64), V.T_SWIRL, 0.25)
    place(mix, crackle(V.T_GROW - V.T_SWIRL - 0.3), V.T_SWIRL + 0.4, 0.9)
    place(mix, sweep(300, 1200, V.T_POP - V.T_GROW, vdepth=0) * 0.35, V.T_GROW, 0.4)
    place(mix, pop(), V.T_POP, 0.9)
    place(mix, ding(), V.T_POP + 0.02, 0.45)
    place(mix, shimmer(1.0), V.T_POP, 0.45)
    place(mix, plink(midi(100)), V.T_NEWF + 0.05, 0.5)
    place(mix, plink(midi(103)), V.T_NEWF + 0.2, 0.35)
    place(mix, E.gib(2, 80, spread=2, syl=0.08, bright=0.7), V.T_NEWF + 0.4, 0.3)        # Chip giggles
    place(mix, E.fanfare(), V.T_YAY, 0.45)
    place(mix, E.gib(4, 64, spread=10, syl=0.09, bright=1.0), V.T_YAY + 0.05, 0.45)       # YAAAY
    place(mix, E.gib(3, 72, spread=6, syl=0.08, bright=0.8), V.T_YAY + 0.1, 0.35)
    cheerful(V.T_YAY + 0.6, V.T_E, mix)
    place(mix, peep(), V.T_HUG, 0.6)
    place(mix, E.gib(2, 58, spread=3, syl=0.22, bright=0.4), V.T_HUG + 0.3, 0.35)        # awww
    for k in range(3):
        place(mix, plink(midi(84 - 3 * k)), V.T_MELT2 + 0.3 + 0.3 * k, 0.3)
    for k in range(4):
        place(mix, squish(0.12) * 0.6, V.T_MOP + 0.35 * k, 0.3)
    for k in range(5):   # everyone laughs
        place(mix, E.gib(1, [60, 66, 74, 82, 70][k], spread=2, syl=0.07, bright=0.9), V.T_LAUGH + 0.12 * k, 0.3)
        place(mix, E.gib(1, [62, 68, 76, 84, 72][k], spread=2, syl=0.07, bright=0.9), V.T_LAUGH + 0.6 + 0.12 * k, 0.25)
    # E: the throne
    march(V.T_E, V.T_STOP, mix, gain=0.32, base=45)
    place(mix, E.gib(1, 50, spread=2, syl=0.18, bright=0.5), V.T_E + 0.1, 0.45)          # HMPH
    place(mix, sting() * 0.6, V.T_STOP, 0.4)
    place(mix, E.gib(3, 50, spread=2, syl=0.14, bright=0.4), V.T_PUSH + 0.1, 0.5)        # HNNNG
    place(mix, violin_tremolo(V.T_GLARE - V.T_PUSH, 55), V.T_PUSH, 0.25)
    place(mix, footstep() * 0.5, V.T_PUSH + 0.3, 0.3)
    place(mix, footstep() * 0.5, V.T_PUSH + 0.7, 0.3)
    place(mix, rumble(0.5), V.T_GLARE, 0.35)
    place(mix, sigh(44), V.T_SIGH + 0.05, 0.55)
    place(mix, thud() * 0.5, V.T_SIT + 0.05, 0.45)
    place(mix, squish(0.2), V.T_SIT + 0.05, 0.4)
    place(mix, E.squeak(0.35), V.T_LEAN, 0.65)
    place(mix, plink(midi(96)), V.T_LEAN + 0.5, 0.3)
    # F: the block upstairs
    place(mix, whoosh(0.8), V.T_F, 0.35)
    place(mix, drone(V.T_BLINK - V.T_F - 0.6), V.T_F + 0.3, 0.35)
    mix += E.eerie(V.T_F + 0.6) * 0.6
    for d in V.DRIPS:
        place(mix, echo(plink(midi(86))), d + 0.12, 0.5)
    # G: the blink (after a beat of near-silence)
    place(mix, sting(), V.T_BLINK, 0.7)
    place(mix, plink(midi(102)), V.T_BLINK + 0.45, 0.35)
    place(mix, crackle(0.4), V.T_ICECRACK, 0.9)
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
