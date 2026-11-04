"""Sound for FRIDGE KINGDOM Ep7 "The Truth About the Duck" (variant A: title card + fanfare)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
from ep3_audio import big_thump, tick
from ep4_audio import cello, chord, trombone, clonk, crack
from ep5_audio import violin_tremolo, drone
import ep6_audio as A6
from ep6_audio import wind, shhhk, snare
from audio import SR, tarr, midi, place, plink, sweep, whoosh, bonk, thud, pop, marimba, boing, ding, lowpass, pluck, sting
import ep7 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A6.N = N
rng = np.random.default_rng(77)


def spy(start, end, mix, gain=0.3):
    """Sneaky spy bassline: staccato minor plucks with a snare tick."""
    bass = [45, 45, 52, 45, 48, 45, 51, 50]
    at, i = start, 0
    while at < end:
        place(mix, pluck(midi(bass[i % 8]), 0.18, 0.25), at, gain)
        if i % 2 == 1:
            place(mix, snare(), at, gain * 0.25)
        i += 1; at += 0.22


def gasp():
    t = tarr(0.45)
    n = rng.standard_normal(len(t)); n = n - lowpass(n, 0.2)
    env = np.minimum(1, t / 0.25) * np.exp(-np.maximum(0, t - 0.3) * 20)
    return n * env * 0.5


def running_water(start, end):
    out = np.zeros(N)
    d = end - start
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.25) * 1.5
    env = np.minimum(1, t / 0.4) * np.minimum(1, (d - t) / 0.4)
    place(out, n * env * 0.12, start, 1.0)
    at = start
    while at < end - 0.2:        # bubbly plinks
        place(out, plink(midi(int(rng.integers(84, 100)))), at, 0.08)
        at += float(rng.uniform(0.08, 0.2))
    return out


def echo(snd, delays=(0.18, 0.36, 0.54, 0.72), decay=0.5):
    out = np.zeros(len(snd) + int(SR * (delays[-1] + 0.1)))
    place(out, snd, 0, 1.0)
    g = 1.0
    for d in delays:
        g *= decay
        place(out, snd, d, g)
    return out


def peep():
    t = tarr(0.12)
    f = 2400 + 900 * np.sin(np.pi * t / 0.12)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.sin(np.pi * t / 0.12) * 0.5


def build(path):
    mix = E.hum() * 0.5
    # 0–2: title fanfare
    place(mix, E.fanfare(), 0.1, 1.0)
    place(mix, E.squeak(0.25), 1.15, 0.35)                        # the "?" over the Duck
    # 2–3.6: the drawer. wind, Wilt's springy fling
    mix += wind(2.0, 3.8) * 0.8
    place(mix, sweep(300, 220, 0.4, vdepth=0) * 0.6, 2.5, 0.4)    # leaf creaks down
    place(mix, E.gib(3, 60, spread=3, syl=0.08), 2.1, 0.35)
    place(mix, thud(), 2.95, 0.4)
    place(mix, boing(), V.T_FLING, 0.9)
    place(mix, sweep(400, 1600, 0.4, vdepth=0), V.T_FLING + 0.05, 0.35)
    # 3.6–4.9: flies up, lands behind the jello
    place(mix, whoosh(0.6), 3.6, 0.6)
    place(mix, thud(), V.T_LAND, 0.8); place(mix, boing(), V.T_LAND + 0.02, 0.3)
    place(mix, E.gib(2, 84, spread=2, syl=0.07), V.T_LAND + 0.05, 0.4)   # Crumb's yelp
    # 4.9–8.4: whispered gibberish, acting out the doodle
    for k, t0 in enumerate([5.0, 6.2, 7.3]):
        place(mix, E.gib(6, 62 + 2 * k, spread=5, syl=0.07, bright=0.25), t0, 0.35)
    for i, m in enumerate([76, 79, 84, 83]):                       # dreamy harp for the doodle
        place(mix, marimba(midi(m), 0.6), 5.1 + i * 0.25, 0.2)
    place(mix, plink(midi(96)), 8.2, 0.45); place(mix, plink(midi(100)), 8.3, 0.45)   # "!"
    # 8.4–12: the plan. spy music; gulp; salute ting
    spy(8.5, 17.0, mix, 0.28)
    place(mix, E.gib(5, 58, spread=4, syl=0.08, bright=0.3), 8.6, 0.4)
    place(mix, E.squeak(0.2), 9.1, 0.25)
    place(mix, sweep(500, 180, 0.3, vdepth=0) * 0.7, 9.95, 0.5)   # gulp
    place(mix, ding(), 10.65, 0.5)                                 # salute "ting"
    place(mix, whoosh(0.3), 11.6, 0.3)
    # 12–17: tiptoe plinks, freeze ticks
    for t0 in np.arange(12.05, 16.8, 0.31):
        if not (13.0 <= t0 < 13.7 or 15.0 <= t0 < 15.7):
            place(mix, plink(midi(88 + int((t0 * 3) % 5))), float(t0), 0.22)
    for t0 in (13.0, 15.0):
        place(mix, tick(2600), t0, 0.8); place(mix, tick(2000), t0 + 0.12, 0.6)
        place(mix, violin_tremolo(0.6, 88) * 0.8, t0, 0.3)
    # 17–18.6: thumbs up from the door seal
    place(mix, ding(), 17.3, 0.45)
    place(mix, E.gib(2, 66, spread=2, syl=0.08), 17.5, 0.35)
    # 18.6: the door opens: choir
    place(mix, E.choir(2.2), V.T_OPEN, 0.9)
    place(mix, whoosh(0.8), V.T_OPEN, 0.5)
    place(mix, whoosh(0.4), V.T_JUMP, 0.4)
    # 19.85: HUGE echoing squeak
    place(mix, echo(E.squeak(0.7) * 2.2), V.T_SQUEAK, 1.0)
    place(mix, big_thump(), V.T_SQUEAK, 0.5)
    place(mix, thud(), 21.2, 0.5)                                  # Crumb bumps down
    # 21.3–25: the Hand scoops up the Duck. gentle, a bit loving
    place(mix, chord([65, 69, 72, 76], 3.2), 21.6, 0.9)
    for i, m in enumerate([84, 88, 91, 96]):
        place(mix, marimba(midi(m), 0.5), V.T_LIFT + i * 0.3, 0.25)
    for t0 in (23.2, 23.3, 23.45):
        place(mix, gasp(), t0, 0.6)
    for k, t0 in enumerate([23.6, 24.2, 24.8, 25.5]):              # squeaks fading as it's carried off
        place(mix, E.squeak(0.25), t0, 0.35 * (0.6 ** k))
    # 25–27.7: far away, a bathtub filling
    mix += running_water(25.0, 27.7)
    place(mix, E.squeak(0.3), 26.4, 0.12)
    # 27.6–30.7: butter dish returned; door closes
    place(mix, whoosh(0.5), 27.7, 0.4)
    place(mix, clonk(), V.T_DISH, 1.0); place(mix, thud(), V.T_DISH, 0.6)
    place(mix, sweep(600, 900, 0.3, vdepth=0) * 0.5, V.T_DISH + 0.2, 0.3)
    place(mix, big_thump(), V.T_CLOSE + 0.3, 0.9)
    # 30.8–34.6: the leap, the throne, the fanfare, confetti
    place(mix, whoosh(0.6), V.T_LEAP, 0.6)
    place(mix, E.gib(3, 70, spread=4, syl=0.07), V.T_LEAP + 0.1, 0.4)
    place(mix, thud(), V.T_LEAP + 0.9, 0.7)
    place(mix, E.fanfare(), V.T_SWORD, 1.2)
    place(mix, chord([60, 64, 67, 72], 2.4), V.T_SWORD + 0.5, 1.1)
    for t0 in (V.T_SWORD + 0.05, V.T_SWORD + 0.45, V.T_SWORD + 0.85):
        place(mix, pop(), t0, 0.7); place(mix, pop(), t0 + 0.03, 0.4)
    bounce_end = 34.6
    mix += E.bouncy(V.T_SWORD + 1.0, bounce_end, base=60, gain=0.22)
    place(mix, E.gib(5, 76, spread=4, syl=0.09), 32.3, 0.35)        # Crumb's happy sob
    # 34.6: music stops. silence... the egg
    for k, t0 in enumerate([35.8, 36.1, 36.4]):
        place(mix, tick(1300 + 200 * k), t0, 0.4)
    place(mix, crack(), V.T_CRACK, 1.0)
    place(mix, crack(), V.T_CRACK + 0.6, 1.0)
    place(mix, drone(2.4), V.T_CRACK, 0.5)
    place(mix, peep(), V.T_CRACK + 1.3, 0.7)
    place(mix, sting(), V.T_CRACK + 1.35, 0.6)
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    out = np.tanh(mix * 1.1)
    # hard duck the music for the silence before the crack
    tt = np.arange(N) / SR
    out = out / np.max(np.abs(out)) * 0.9
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
