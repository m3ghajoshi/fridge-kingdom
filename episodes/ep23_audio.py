"""Sound for FRIDGE KINGDOM Ep23 "The New Duck" (variant A: title card first)."""
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "engine"))
import numpy as np
from scipy.io import wavfile
import ep1_audio as E
import ep5_audio as A5
from ep5_audio import cricket_chirp
from ep6_audio import record_scratch, sad_violin
from ep7_audio import gasp, peep
from ep8_audio import shimmer, dun
from ep10_audio import squish
from ep14_audio import pat
from ep16_audio import slide_whistle
from ep18_audio import footstep, minor_choir
from ep22_audio import quick_squeak
from audio import SR, tarr, midi, place, plink, pluck, marimba, sweep, whoosh, thud, pop, ding, sting, boing, lowpass, bonk
import ep23 as V

DUR = V.DUR
N = int(SR * DUR)
E.N = N
A5.N = N
rng = np.random.default_rng(2323)


def fwip(d=0.18):
    t = tarr(d)
    n = lowpass(rng.standard_normal(len(t)), 0.35)
    return n * np.sin(np.pi * t / d) ** 2 * 0.7


def conga_hit(f=110, d=0.25):
    t = tarr(d)
    s = np.sin(2 * np.pi * (f + 60 * np.exp(-t * 30)) * t) * np.exp(-t * 14)
    s += lowpass(rng.standard_normal(len(t)), 0.2) * np.exp(-t * 40) * 0.3
    return s


def conga(start, end, mix, gain=0.5):
    """Conga line beat: 1-2-3-KICK, with a little horn stab on the kick."""
    at, i = start, 0
    beat = 0.3
    while at < end:
        k = i % 4
        place(mix, conga_hit(140 if k < 3 else 95), at, gain * (1.0 if k == 3 else 0.7))
        if k == 3:
            for m in (62, 66, 69):
                place(mix, pluck(midi(m), 0.25, 0.7), at, gain * 0.35)
        else:
            place(mix, marimba(midi([74, 76, 74][k]), 0.2), at, gain * 0.25)
        at += beat; i += 1


def build(path):
    mix = np.zeros(N)
    place(mix, E.fanfare(), 0.15, 0.9)
    # Grandma's parachute + the pickles hopping down
    place(mix, fwip(0.3), V.T_JUMPG + 0.3, 0.8)
    place(mix, sweep(900, 500, 1.2, vdepth=0.05) * 0.15, V.T_JUMPG + 0.4, 0.3)
    for k in range(5):
        place(mix, fwip(), V.KID_JUMP[k] + 0.1, 0.7)
        place(mix, plink(midi(76 + 2 * k)), V.KID_JUMP[k] + 0.6, 0.35)
    place(mix, thud() * 0.4, V.T_LANDG, 0.4)
    # the bow
    for m in range(6):
        place(mix, fwip(0.12), V.T_BOW + 0.05 * m, 0.4)
    place(mix, E.choir(1.0) * 0.5, V.T_BOW, 0.25)
    place(mix, quick_squeak(0.22, 1150), V.T_SQ_HAPPY + 0.05, 0.8)
    place(mix, quick_squeak(0.2, 1250), V.T_SQ_HAPPY + 0.35, 0.7)
    # head-hops: boop x6, BOING on the jello
    for i in range(6):
        place(mix, pop() * 0.6, V.T_HEADHOP + V.HH * (i + 1), 0.5)
        place(mix, quick_squeak(0.1, 1100 + 60 * i), V.T_HEADHOP + V.HH * (i + 1), 0.4)
    place(mix, boing(), V.T_ONJELLO, 0.8)
    place(mix, E.splat() * 0.3, V.T_ONJELLO, 0.3)
    for k in range(3):
        place(mix, quick_squeak(0.18, 1100), V.T_ONJELLO + 0.1 + 0.4 * k, 0.5)
    for k in range(6):
        place(mix, E.gib(1, 70 + 2 * k, spread=2, syl=0.06, bright=0.8), V.T_TURN + 0.1 * k, 0.15)   # shuffle mutters
    # the leap + the whip-round
    place(mix, slide_whistle(600, 1600, V.T_LEAPLAND - V.T_LEAP) * 0.4, V.T_LEAP, 0.45)
    place(mix, quick_squeak(0.5, 1200), V.T_LEAP + 0.05, 0.6)
    place(mix, record_scratch(), V.T_REVERSE, 0.5)
    place(mix, whoosh(0.4), V.T_REVERSE + 0.05, 0.4)
    # conga!
    conga(V.T_CONGA, V.crash_t(5) + 0.1, mix, 0.5)
    place(mix, boing(), V.T_CARTON - 0.05, 0.6)
    for k in range(5):
        place(mix, quick_squeak(0.16, 1250), V.T_CARTON + 0.25 + 0.5 * k, 0.45)
    for m in range(6):
        place(mix, bonk(), V.crash_t(m), 0.55 + 0.05 * m)
        place(mix, E.gib(1, 64 + 3 * m, spread=2, syl=0.08, bright=0.6), V.crash_t(m) + 0.08, 0.25)
    place(mix, A5.cricket_chirp() if hasattr(A5, "cricket_chirp") else cricket_chirp(), V.crash_t(5) + 0.4, 0.3)
    # Dill's chance
    place(mix, E.gib(2, 58, spread=3, syl=0.12, bright=0.5), V.DILL_UP + 0.2, 0.45)     # ha!
    place(mix, whoosh(0.5), V.DILL_WALK[0], 0.3)
    place(mix, quick_squeak(0.3, 1000), V.T_OFFCARTON + 0.05, 0.6)
    place(mix, pop(), V.T_CATCH, 0.6)
    place(mix, quick_squeak(0.2, 900), V.T_CATCH + 0.05, 0.5)
    place(mix, E.fanfare(), V.T_PLONK, 0.7)                                              # TA-DA
    place(mix, plink(midi(88)), V.T_PLONK, 0.4)
    place(mix, E.gib(2, 50, spread=2, syl=0.16, bright=0.4), V.T_SIT + 0.1, 0.4)          # ahem
    # pyramid + bows
    place(mix, pop(), V.T_PYR, 0.7)
    place(mix, sweep(400, 1200, 0.3, vdepth=0) * 0.3, V.T_PYR, 0.3)
    for m in range(6):
        place(mix, fwip(0.12), V.T_PBOW + 0.08 * m, 0.45)
    place(mix, shimmer(0.6), V.T_PBOW + 0.3, 0.3)
    place(mix, boing() * 0.5, V.T_ONHEAD, 0.5)
    place(mix, squish(0.2), V.T_HEADLAND, 0.5)
    place(mix, E.gib(1, 48, spread=2, syl=0.2, bright=0.3), V.T_HEADLAND + 0.2, 0.45)     # hmph
    # copy-loop
    for k, (mv, t0, who) in enumerate(V.COPY):
        if who == "S":
            place(mix, quick_squeak(0.2, 1050 + 40 * k), t0 + 0.02, 0.7)
        else:
            place(mix, peep(), t0 + 0.02, 0.6)
        if mv == "spin":
            place(mix, sweep(500, 1500, 0.3, vdepth=0) * 0.2, t0, 0.3)
        elif mv == "hop":
            place(mix, boing() * 0.4, t0, 0.3)
        else:
            place(mix, slide_whistle(800, 1000, 0.3) * 0.2, t0, 0.3)
    E_b = E.bouncy(V.COPY[0][1], V.T_FRENZY[1], base=64, gain=0.2)
    mix += E_b
    at = V.T_FRENZY[0]
    k = 0
    while at < V.T_FRENZY[1]:
        if k % 2 == 0:
            place(mix, quick_squeak(0.12, 1100 + 30 * (k % 6)), at, 0.55)
        else:
            place(mix, peep(), at, 0.45)
        at += 0.11; k += 1
    place(mix, slide_whistle(500, 1400, 0.45) * 0.4, V.T_PEEPJUMP[0], 0.45)
    place(mix, plink(midi(91)), V.T_PEEPJUMP[1], 0.5)
    # Crumb, left out
    place(mix, E.gib(2, 66, spread=4, syl=0.1, bright=0.6), V.T_OFFER + 0.4, 0.4)       # hm? hm?
    place(mix, E.gib(2, 68, spread=4, syl=0.1, bright=0.6), V.T_OFFER + 1.2, 0.35)
    place(mix, cricket_chirp(), V.T_OFFER_END - 0.4, 0.35)
    sad_violin(V.T_WALKAWAY[0], mix)
    place(mix, E.gib(1, 55, spread=2, syl=0.35, bright=0.2), V.T_SITCR + 0.25, 0.35)     # sigh
    for p0 in V.PATS:
        place(mix, pat(), p0, 0.7)
        place(mix, plink(midi(96)), p0 + 0.45, 0.35)                                     # drip
    place(mix, shimmer(0.5), V.T_SMILE, 0.3)
    # Squeak at the door
    place(mix, boing() * 0.4, V.T_TOTHRONE[0], 0.4)
    place(mix, whoosh(0.3), V.T_FWD[0], 0.35)
    for k, s0 in enumerate(V.SQUEAKS):
        place(mix, quick_squeak(0.3, 1050 + 50 * k, 1.3), s0 + 0.02, 1.0)
    for s0 in V.STEPS:
        place(mix, footstep(), s0, 1.2)
        place(mix, thud() * 0.5, s0, 0.6)
    place(mix, gasp(), V.STEPS[0] + 0.2, 0.5)
    place(mix, whoosh(0.6), V.T_FLEE[0] + 0.2, 0.35)
    for k in range(6):
        place(mix, E.gib(1, [72, 76, 80][k % 3], spread=2, syl=0.06, bright=0.9), V.T_FLEE[0] + 0.1 * k, 0.2)
    # the Hand returns the Duck
    place(mix, E.choir(2.0), V.T_OPEN, 0.55)
    place(mix, sweep(200, 90, 0.9, vdepth=0) * 0.3, V.T_HDOWN, 0.35)
    place(mix, plink(midi(91)), V.T_HSET, 0.55)
    place(mix, shimmer(0.8), V.T_HSET, 0.35)
    place(mix, E.squeak(0.3), V.T_HSET + 0.1, 0.35)
    place(mix, minor_choir(1.0), V.T_TURNFACE[0], 0.3)
    for k, d in enumerate(V.DUNS):
        place(mix, dun([43, 42][k]), d, 1.1)
    place(mix, E.squeak(0.35), V.END_T + 0.9, 0.5)
    mix += E.hum() * 0.2
    out = np.tanh(mix * 1.1)
    out = out / np.max(np.abs(out)) * 0.82
    tt = np.arange(N) / SR
    out *= np.clip((DUR - tt) / 0.4, 0, 1)
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    build(sys.argv[1])
