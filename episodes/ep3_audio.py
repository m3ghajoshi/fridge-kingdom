"""Sound for FRIDGE KINGDOM Ep3 "The Outside"."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
from audio import SR, tarr, midi, place, plink, sweep, whoosh, zip_sfx, bonk, thud, pop, marimba, boing, ding, lowpass, munch, pluck

DUR = 40.0
N = int(SR * DUR)
E.N = N  # resize shared helpers' buffers (hum, bouncy, eerie)
rng = np.random.default_rng(33)


def tick(f=2400):
    t = tarr(0.04)
    return np.sin(2 * np.pi * f * t) * np.exp(-t * 120) * 0.6


def knock():
    t = tarr(0.25)
    f = 110 * np.exp(-t * 6) + 70
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 18)
    n = lowpass(rng.standard_normal(len(t)), 0.1) * np.exp(-t * 40) * 1.5
    return (body + n) * 0.9


def big_thump():
    out = thud() * 1.4
    n = lowpass(rng.standard_normal(len(out)), 0.05) * np.exp(-tarr(0.3) * 15) * 1.5
    return out + n


def scrape(d):
    t = tarr(d)
    n = rng.standard_normal(len(t)); n = n - lowpass(n, 0.4)
    ring = np.sin(2 * np.pi * 1800 * t) * 0.15 + np.sin(2 * np.pi * 2650 * t) * 0.08
    return (n * 0.25 + ring) * np.minimum(1, t / 0.05) * np.minimum(1, (d - t) / 0.2)


def tension(start, end):
    out = np.zeros(N)
    at, k = start, 0
    while at < end:
        place(out, thud(), at, 0.5 + 0.5 * (at - start) / (end - start))
        at += max(0.12, 0.35 - 0.02 * k); k += 1
    return out


def run_music(start, end, base=57, gain=0.2):
    """Frantic chase plucks."""
    out = np.zeros(N)
    mel = [0, 3, 7, 3, 10, 7, 3, 0]
    at, i = start, 0
    while at < end:
        place(out, pluck(midi(base + 12 + mel[i % 8]), 0.12, 0.6), at, gain)
        if i % 2 == 0:
            place(out, thud(), at, gain * 1.5)
        i += 1; at += 0.13
    return out


def build(path):
    mix = E.hum() * 0.6
    # title fanfare, slightly off-key (one note bent flat)
    fan = E.fanfare()
    place(mix, fan, 0.1, 0.9)
    place(mix, sweep(midi(77), midi(76), 0.5, vdepth=0.0), 0.55, 0.12)
    # echoey whoosh + awe choir as the Hand lowers Dill into the kitchen
    place(mix, whoosh(1.6), 2.0, 0.6)
    place(mix, E.choir(2.2), 2.1, 0.7)
    place(mix, E.gib(6, 64, spread=6, syl=0.12), 2.4, 0.5)     # Dill flailing
    place(mix, pop(), 3.7, 0.7); place(mix, thud(), 3.98, 0.7)
    place(mix, E.gib(3, 70, spread=2, syl=0.18), 4.4, 0.55)    # "whoaaa"
    for k, m in enumerate([72, 76, 79, 84]):                   # wonder sparkle
        place(mix, plink(midi(m)), 4.6 + k * 0.18, 0.35)
    # thump x3, gasp
    for t0 in (6.4, 7.9, 9.2):
        place(mix, whoosh(0.5), t0 - 0.45, 0.35)
        place(mix, big_thump(), t0, 0.9)
    place(mix, E.gib(2, 68, spread=2, syl=0.08), 6.7, 0.4)
    place(mix, E.gib(2, 70, spread=2, syl=0.08), 8.2, 0.45)
    place(mix, sweep(400, 1500, 0.35, vdepth=0.0), 9.45, 0.4)  # GASP
    place(mix, E.gib(5, 72, spread=4, syl=0.07), 10.2, 0.6)    # protest while pinched
    # the ceiling closes in: rising slide whistle + tension drums
    place(mix, sweep(300, 1600, 2.6, vib=5, vdepth=0.04), 11.0, 0.35)
    mix += tension(11.2, 13.6)
    place(mix, E.gib(4, 76, spread=3, syl=0.06), 12.6, 0.5)
    place(mix, whoosh(0.4), 13.5, 0.5)
    place(mix, big_thump(), 13.85, 1.0)
    # zip + spoon scrape
    place(mix, zip_sfx(), 14.4, 0.8)
    place(mix, scrape(3.0), 14.5, 0.6)
    mix += E.bouncy(14.6, 20.6, base=62, gain=0.18)
    place(mix, E.gib(6, 66, spread=5, syl=0.07, bright=0.8), 15.6, 0.55)   # "wheee"
    # ping, swish, crunch, ta-da
    place(mix, ding(), 18.0, 0.9); place(mix, boing(), 18.02, 0.5)
    place(mix, whoosh(0.6), 19.3, 0.45)
    for k in range(9):
        place(mix, munch(), 19.35 + k * 0.13, 0.35)
    place(mix, sweep(900, 250, 1.4, vib=8), 20.6, 0.35)         # falling
    place(mix, thud(), 22.1, 0.8)
    for k, m in enumerate([67, 72, 76, 79]):                    # ta-da
        place(mix, marimba(midi(m), 0.6), 22.25 + (0 if k < 3 else 0.2), 0.35)
    # race: running blips + ticking clock
    place(mix, sweep(1200, 300, 0.3, vdepth=0.0), 23.3, 0.35)    # "!"
    mix += run_music(23.6, 29.5)
    for k in range(int((29.5 - 23.6) / 0.5)):
        place(mix, tick(2400 if k % 2 else 1900), 23.6 + k * 0.5, 0.9)
    place(mix, sweep(140, 90, 1.0, vdepth=0.0), 25.4, 0.3)      # door creak
    place(mix, E.gib(8, 58, spread=6, syl=0.07, bright=0.9), 27.0, 0.6)
    place(mix, sweep(400, 1300, 0.7), 29.5, 0.35)               # leap
    # BONK, slow peel, slide whistle down
    place(mix, bonk(), 30.3, 1.0); place(mix, big_thump(), 30.3, 0.8)
    place(mix, sweep(1500, 300, 2.0, vib=4, vdepth=0.04), 31.3, 0.4)
    place(mix, thud(), 33.65, 0.6)
    # inside, dark: three muffled knocks
    for t0 in (35.1, 35.7, 36.3):
        place(mix, knock(), t0, 1.0)
    place(mix, E.gib(2, 80, spread=1, syl=0.06), 35.4, 0.35)
    place(mix, E.gib(2, 82, spread=1, syl=0.06), 36.0, 0.4)
    place(mix, E.squeak(0.4), 36.5, 0.5)
    for m in (57, 60, 63, 66):
        place(mix, marimba(midi(m), 1.8), 37.0, 0.35)
    place(mix, E.squeak(0.35), 39.25, 0.5)
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.9
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
