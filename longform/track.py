"""Camera path for reframing a vertical episode into 16:9.

Usage: python3 longform/track.py build/epN_video.mp4 OUT.txt [WINDOW_H]
Writes one line per frame: the crop window's centre y, in the episode's 1080x1920 coordinates.
The camera aims at where things move and where characters are (dark ink outlines), only moves
when another spot is clearly better (dead zone), and glides between spots (smoothing).
"""
import subprocess, sys
import numpy as np
from scipy.ndimage import gaussian_filter1d

src, out = sys.argv[1], sys.argv[2]
WIN_H = float(sys.argv[3]) if len(sys.argv) > 3 else 1080 * 9 / 16   # full width -> 607.5 tall
w, h = 108, 192
raw = subprocess.run(["ffmpeg", "-v", "error", "-i", src, "-vf", f"scale={w}:{h}",
                      "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
rgb = np.frombuffer(raw, np.uint8).reshape(-1, h, w, 3).astype(np.float32) / 255
mx, mn = rgb.max(axis=3), rgb.min(axis=3)
sat = (mx - mn) / np.maximum(mx, 1e-3)
r, g, bl = rgb[..., 0], rgb[..., 1], rgb[..., 2]
# Characters are the warm/green saturated shapes (Duck, Peep, Crumb, Dill, pickles); the fridge,
# shelves, frost and backgrounds are blue/grey/beige, and the cup is magenta. Those never count.
char = (sat > 0.35) & (mx > 0.3) & ~((bl > r) & (bl > g)) & ~((r > g) & (bl > g))   # no blue, no magenta props
gray = rgb.mean(axis=3)
motion = np.abs(gray - np.concatenate([gray[:15], gray[:-15]]))
s = gaussian_filter1d(char.sum(axis=2) * 1.0 + motion.sum(axis=2) * 0.15, 8, axis=0)
# Faces sit near the top of characters: nudge the window up a little so heads win over feet.
s = np.roll(s, -int(h * 0.015), axis=1)
win = int(round(WIN_H / 1920 * h))
cs = np.cumsum(np.pad(s, ((0, 0), (1, 0))), axis=1)
score = cs[:, win:] - cs[:, :-win]
best = score.argmax(axis=1)
# Hard cuts (the whole picture changes between two frames): the camera cuts too, instead of gliding.
jump = np.abs(np.diff(gray, axis=0)).mean(axis=(1, 2))
cuts = [0] + [i + 1 for i in np.where(jump > 0.08)[0]] + [len(best)]
path = np.zeros(len(best))
for a0, b0 in zip(cuts[:-1], cuts[1:]):
    if b0 <= a0:
        continue
    cur = float(np.median(best[a0:min(b0, a0 + 10)]))
    for i in range(a0, b0):
        c = min(max(int(round(cur)), 0), score.shape[1] - 1)
        if score[i, best[i]] > 1.15 * score[i, c]:
            cur = float(best[i])
        path[i] = cur
    path[a0:b0] = gaussian_filter1d(path[a0:b0], 12, mode="nearest")
cy = np.clip((path + win / 2) / h * 1920, WIN_H / 2, 1920 - WIN_H / 2)
np.savetxt(out, cy, fmt="%.1f")
