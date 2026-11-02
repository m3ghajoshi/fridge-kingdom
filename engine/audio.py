"""Synthesized music + sound effects for 'Nib & Bun: The Cupcake Caper'. All sounds made from scratch."""
import numpy as np
from scipy.io import wavfile

SR = 44100
DUR = 20.0
N = int(SR * DUR)
rng = np.random.default_rng(7)


def tarr(d):
    return np.arange(int(SR * d)) / SR


def midi(m):
    return 440.0 * 2 ** ((m - 69) / 12)


def place(buf, snd, at, gain=1.0):
    i = int(at * SR)
    j = min(len(buf), i + len(snd))
    if i < len(buf):
        buf[i:j] += snd[: j - i] * gain


def lowpass(x, a=0.15):
    y = np.zeros_like(x)
    acc = 0.0
    for i, v in enumerate(x):
        acc += a * (v - acc)
        y[i] = acc
    return y


# ---------- instruments ----------
def pluck(freq, d=0.35, bright=0.5):
    t = tarr(d)
    env = np.exp(-t * 9)
    tri = 2 * np.abs(2 * ((t * freq) % 1) - 1) - 1
    sine = np.sin(2 * np.pi * freq * t)
    attack = np.minimum(1, t / 0.004)
    return (bright * tri + (1 - bright) * sine) * env * attack


def marimba(freq, d=0.5):
    t = tarr(d)
    s = np.sin(2 * np.pi * freq * t) * np.exp(-t * 7)
    s += 0.3 * np.sin(2 * np.pi * freq * 4 * t) * np.exp(-t * 25)
    return s * np.minimum(1, t / 0.003)


# ---------- sound effects ----------
def plink(freq):
    t = tarr(0.18)
    return np.sin(2 * np.pi * freq * t) * np.exp(-t * 30) * 0.8


def ding():
    t = tarr(1.2)
    s = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k)
            for f, a, k in [(1568, 1, 3), (2352, .5, 5), (3136, .3, 7), (4704, .15, 9)])
    return s * 0.5


def boing():
    t = tarr(0.7)
    f = 220 + 160 * np.exp(-t * 3) + 40 * np.sin(2 * np.pi * 14 * t) * np.exp(-t * 2)
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 4) * 0.9


def sweep(f0, f1, d, vib=6, vdepth=0.03, shape="sine"):
    t = tarr(d)
    f = f0 * (f1 / f0) ** (t / d)
    f = f * (1 + vdepth * np.sin(2 * np.pi * vib * t))
    ph = 2 * np.pi * np.cumsum(f) / SR
    s = np.sin(ph) if shape == "sine" else np.sign(np.sin(ph)) * 0.5
    env = np.minimum(1, t / 0.03) * np.minimum(1, (d - t) / 0.08)
    return s * env


def whoosh(d=0.9):
    t = tarr(d)
    n = rng.standard_normal(len(t))
    n = lowpass(n, 0.08) * 3
    env = np.sin(np.pi * t / d) ** 2
    return n * env * 0.6


def zip_sfx():
    t = tarr(0.22)
    f = 600 * (8 ** (t / 0.22))
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sign(np.sin(ph)) * 0.25 * np.exp(-t * 6)


def bonk():
    t = tarr(0.6)
    f = 140 * np.exp(-t * 4) + 60
    ph = 2 * np.pi * np.cumsum(f) / SR
    body = np.sin(ph) * np.exp(-t * 7) * 1.2
    click_t = tarr(0.05)
    click = np.sin(2 * np.pi * 900 * click_t) * np.exp(-click_t * 80)
    wood = np.zeros_like(t)
    wood[: len(click)] = click
    noise = rng.standard_normal(len(t)) * np.exp(-t * 40) * 0.4
    return body + wood * 0.8 + noise


def thud():
    t = tarr(0.3)
    f = 90 * np.exp(-t * 5) + 45
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 12) * 0.9


def pop():
    t = tarr(0.12)
    f = 900 * np.exp(-t * 25) + 300
    ph = 2 * np.pi * np.cumsum(f) / SR
    return np.sin(ph) * np.exp(-t * 30) * 0.8


def chirp():
    out = np.zeros(int(SR * 0.6))
    for i, m in enumerate([84, 88, 91, 96]):
        place(out, plink(midi(m)), i * 0.08, 0.7)
    return out


def munch():
    t = tarr(0.16)
    n = lowpass(rng.standard_normal(len(t)), 0.25) * 2
    return n * np.exp(-t * 25) * 0.7


def sting():
    out = np.zeros(int(SR * 1.5))
    for m in [60, 64, 67, 72]:
        place(out, marimba(midi(m), 1.5), 0, 0.5)
    return out


# ---------- music ----------
def music():
    buf = np.zeros(N)
    eighth = 0.25
    melody = [72, 76, 79, 76, 77, None, 74, None,
              71, 74, 77, 74, 72, None, 67, None,
              72, 76, 79, 84, 83, 79, 77, 74,
              76, 72, 74, 71, 72, None, None, None]
    bass = [48, 48, 53, 53, 55, 55, 48, 48]  # per half-bar (1s)
    loop = len(melody) * eighth  # 8 s
    t0 = 0.0
    while t0 < DUR:
        for i, m in enumerate(melody):
            at = t0 + i * eighth
            if m is not None and at < DUR:
                place(buf, pluck(midi(m), 0.3, 0.4), at, 0.32)
        for i, m in enumerate(bass):
            for k in range(2):
                at = t0 + i * 1.0 + k * 0.5
                if at < DUR:
                    place(buf, marimba(midi(m), 0.45), at, 0.45)
        t0 += loop
    # duck during the big gag, fade out at end
    tt = np.arange(N) / SR
    duck = 1 - 0.55 * np.clip((tt - 9.8) / 0.3, 0, 1) * np.clip((13.4 - tt) / 0.4, 0, 1)
    fade = np.clip((19.6 - tt) / 0.5, 0, 1)
    return buf * duck * fade


def build(path):
    mix = music() * 0.9
    sfx = np.zeros(N)
    # Nib tiptoes in
    for i in range(8):
        place(sfx, plink(midi(88 if i % 2 else 91)), 2.5 + 0.4375 * (i + 1), 0.6)
    place(sfx, ding(), 6.2, 0.7)                 # lifts the cupcake
    place(sfx, boing(), 8.5, 0.8)                # Bun spots Nib "!"
    place(sfx, whoosh(1.1), 10.0, 0.9)           # pounce
    place(sfx, sweep(380, 1500, 1.15), 10.0, 0.45)  # slide whistle up
    place(sfx, zip_sfx(), 10.88, 0.8)            # Nib dodges
    place(sfx, bonk(), 11.2, 1.0)                # BONK into fridge
    place(sfx, sweep(1400, 260, 1.5, vib=5, vdepth=0.04), 11.5, 0.45)  # slides down
    place(sfx, thud(), 13.0, 0.9)
    for k in range(8):                           # dizzy twinkles
        place(sfx, plink(midi([96, 100, 103, 100][k % 4])), 13.4 + 0.25 * k, 0.35)
    for i in range(4):                           # Nib walks over
        place(sfx, plink(midi(86 if i % 2 else 89)), 15.6 + 0.3 * i, 0.5)
    place(sfx, pop(), 16.9, 0.9)                 # cupcake split
    place(sfx, chirp(), 17.3, 0.6)               # Bun happy
    for k in range(5):
        place(sfx, munch(), 17.7 + 0.35 * k, 0.8)
    place(sfx, sting(), 19.4, 0.9)
    out = mix + sfx
    out = np.tanh(out * 1.1)
    out = out / np.max(np.abs(out)) * 0.9
    wavfile.write(path, SR, (out * 32767).astype(np.int16))


if __name__ == "__main__":
    import sys
    build(sys.argv[1])
