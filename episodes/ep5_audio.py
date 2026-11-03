"""Sound for FRIDGE KINGDOM Ep5 "The Usurper" (variant A: title card first)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
from ep3_audio import big_thump
from ep4_audio import scream, cello, chord, trombone
from audio import SR, tarr, midi, place, plink, sweep, whoosh, bonk, thud, pop, marimba, boing, ding, lowpass, munch, pluck

DUR = 39.4
N = int(SR * DUR)
E.N = N
rng = np.random.default_rng(55)


def minor_fanfare():
    out = np.zeros(int(SR * 1.6))
    for at, ms, d in [(0, (62, 65, 69), 0.18), (0.2, (62, 65, 69), 0.18), (0.42, (58, 62, 65), 0.25), (0.7, (57, 61, 64), 0.8)]:
        for m in ms:
            t = tarr(d)
            ph = 2 * np.pi * midi(m) * t
            s = sum(np.sin(k * ph) / k for k in range(1, 7)) * np.minimum(1, t / 0.02) * np.exp(-t * 2)
            place(out, s, at, 0.18)
    return out


def violin_tremolo(d, m):
    t = tarr(d)
    f = midi(m) * (1 + 0.01 * np.sin(2 * np.pi * 6 * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = sum(np.sin(k * ph) / k for k in range(1, 8))
    trem = 0.6 + 0.4 * np.sin(2 * np.pi * 14 * t)
    env = np.minimum(1, t / 0.3) * np.minimum(1, (d - t) / 0.1)
    return lowpass(s * trem * env, 0.2) * 0.4


def cricket_chirp():
    t = tarr(0.25)
    s = np.sin(2 * np.pi * 4300 * t) * (np.sin(2 * np.pi * 30 * t) > 0)
    return s * np.sin(np.pi * t / 0.25) * 0.25


def funk(start, end, gain=0.3):
    out = np.zeros(N)
    bass = [40, 40, 52, 40, 43, 45, 43, 38]
    at, i = start, 0
    while at < end:
        place(out, pluck(midi(bass[i % 8]), 0.2, 0.8) * 1.5, at, gain)
        if i % 2 == 1:   # snare-ish
            tt = tarr(0.1)
            place(out, rng.standard_normal(len(tt)) * np.exp(-tt * 40) * 0.5, at, gain)
        if i % 4 == 0:
            place(out, thud(), at, gain * 0.8)
        i += 1; at += 0.24
    return out


def click():
    t = tarr(0.06)
    return (np.sin(2 * np.pi * 2100 * t) + 0.6 * rng.standard_normal(len(t))) * np.exp(-t * 90) * 0.8


def drone(d):
    t = tarr(d)
    s = np.sin(2 * np.pi * 55 * t) + 0.5 * np.sin(2 * np.pi * 58.3 * t) + 0.3 * np.sin(2 * np.pi * 110 * t)
    return s * np.minimum(1, t / 0.8) * np.minimum(1, (d - t) / 0.3) * 0.35


def build(path):
    mix = E.hum() * 0.6
    place(mix, minor_fanfare(), 0.05, 0.9)
    # 2–6: the usurper. steam hiss, furious gibberish
    place(mix, sweep(400, 250, 0.4), 2.2, 0.3)
    place(mix, E.hiss(1.2), 2.8, 0.6); place(mix, E.hiss(1.0), 4.4, 0.5)
    place(mix, E.gib(10, 58, spread=6, syl=0.08), 2.7, 0.55)
    place(mix, E.gib(8, 56, spread=6, syl=0.07), 4.3, 0.55)
    place(mix, pop(), 3.2, 0.4)
    # 6–10: staring contest
    place(mix, violin_tremolo(3.9, 76), 6.0, 0.7)
    place(mix, violin_tremolo(3.9, 77), 6.0, 0.4)
    place(mix, plink(midi(96)), 7.7, 0.3); place(mix, plink(midi(96)), 7.95, 0.3); place(mix, plink(midi(96)), 9.25, 0.3)
    place(mix, sweep(1200, 1000, 0.08, vdepth=0), 9.72, 0.5)            # blink
    place(mix, sweep(800, 200, 0.45, vdepth=0), 10.0, 0.3)             # topple
    place(mix, big_thump(), 10.45, 0.8)
    # 11–15: dance-off
    place(mix, boing(), 11.05, 0.5)
    mix += funk(11.4, 15.0, 0.35)
    place(mix, sweep(500, 900, 0.25, vdepth=0), 12.4, 0.35)            # "hoo!"
    place(mix, sweep(520, 950, 0.25, vdepth=0), 13.9, 0.35)
    place(mix, E.gib(3, 70, spread=4, syl=0.08), 14.5, 0.4)
    for k in range(4):                                                  # ...crickets
        place(mix, cricket_chirp(), 15.05 + k * 0.32, 0.6)
    # 16–21: the charge
    place(mix, E.gib(4, 55, spread=3, syl=0.1), 16.0, 0.5)
    for k in range(8):
        place(mix, pluck(midi(48 + (k % 2) * 2), 0.08, 0.9), 16.6 + k * 0.1, 0.4)
    place(mix, sweep(400, 1000, 0.3), 17.4, 0.3)
    place(mix, boing(), 17.72, 1.0)
    place(mix, sweep(500, 1600, 0.9, vib=10), 17.95, 0.35)              # wheee
    place(mix, E.crash(), 19.0, 0.9); place(mix, big_thump(), 19.0, 0.9)
    place(mix, sweep(900, 200, 0.8, vdepth=0), 19.2, 0.3)              # slide down
    place(mix, E.splat(), 19.25, 0.4)                                   # milk
    for k, m in enumerate([84, 88, 91]):
        place(mix, marimba(midi(m), 0.4), 19.95 + k * 0.25, 0.3)        # dizzy tweets
    # 21–26: Crumb's gift
    place(mix, E.gib(4, 80, spread=2, syl=0.07), 21.2, 0.4)
    place(mix, munch(), 22.75, 1.0); place(mix, munch(), 22.85, 0.8); place(mix, munch(), 22.95, 0.6)
    place(mix, sweep(1500, 1300, 0.15, vdepth=0), 23.05, 0.35)         # tiny "ow"
    place(mix, E.gib(2, 84, spread=1, syl=0.1), 23.6, 0.3)
    place(mix, ding(), 24.5, 0.5)
    place(mix, chord([67, 71, 74, 79], 1.6), 24.7, 0.8)                 # hopeful chime
    # 26–29: silence... SQUEAK
    place(mix, E.squeak(0.32) * 1.6, 27.3, 1.0)
    place(mix, plink(midi(91)), 27.6, 0.25)                            # the crown tilts
    # 29–33: screaming circles, dive behind the jello
    scream(27.55, mix, 0.7)
    for k in range(4):
        scream(29.0 + k * 0.55, mix, 0.5)
    mix += E.bouncy(29.0, 31.2, base=67, gain=0.18)
    place(mix, whoosh(0.6), 31.2, 0.6)
    place(mix, boing(), 31.85, 0.9)
    place(mix, E.gib(6, 78, spread=2, syl=0.05, bright=0.4), 32.2, 0.3)  # trembling
    # 33–37: the jar lid turns by itself
    place(mix, drone(4.4), 33.0, 0.8)
    for t0 in [34.3, 34.9, 35.5, 36.1, 36.7]:
        place(mix, click(), t0, 0.9)
    place(mix, cello(2.4, 37), 34.9, 0.4)
    place(mix, E.squeak(0.35), 38.35, 0.5)
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.9
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
