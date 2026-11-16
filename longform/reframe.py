"""Render an episode straight into a 1920x1080 frame that follows a camera path.

Usage: python3 longform/reframe.py N START END CAMERA.txt OUT.mp4
Draws the episode's own vector frames zoomed 16/9x (so the full 1080 width fills 1920),
cropped to the camera window, so the zoom stays sharp. Video only; the film adds the sound.
"""
import importlib, os, subprocess, sys
import cairo
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "episodes"), os.path.join(ROOT, "engine")]
n, start, end, cam, out = sys.argv[1], float(sys.argv[2]), float(sys.argv[3]), sys.argv[4], sys.argv[5]
ep = importlib.import_module(f"ep{n}")
OW, OH = 1920, 1080
K = OW / ep.W                      # 16/9 zoom
cy = np.loadtxt(cam)
surf = cairo.ImageSurface(cairo.FORMAT_ARGB32, OW, OH)
proc = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgra",
                         "-s", f"{OW}x{OH}", "-r", str(ep.FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                         "-crf", "20", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
for i in range(int(round(start * ep.FPS)), int(round(end * ep.FPS))):
    y = cy[min(i, len(cy) - 1)]
    c = cairo.Context(surf); c.set_source_rgb(0, 0, 0); c.paint()
    c.translate(0, -(y * K - OH / 2)); c.scale(K, K)
    ep.frame(c, i / ep.FPS); surf.flush(); proc.stdin.write(bytes(surf.get_data()))
proc.stdin.close(); proc.wait()
