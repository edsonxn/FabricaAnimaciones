# -*- coding: utf-8 -*-
"""blte_j2.mp4 se bajó con el audio cortado (43 de 108 s): baja solo el audio del VOD (2600 + 108 s) y lo remuxa sin tocar el video."""
import os
import shutil
import subprocess

import numpy as np

FF =r"C:\ffmpeg\bin\ffmpeg.exe"
D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
mp4 = os.path.join(D, "medios", "_fuente", "blte_j2.mp4")
url = [u for u in subprocess.run(["yt-dlp", "-g", "-f", "bestaudio[language^=es]", "https://youtu.be/omVu-XL2Hr4"], capture_output=True,
                                 text=True).stdout.split() if u.startswith("http")][0]      # el VOD trae doblajes automáticos: el español, a mano
tmp, nuevo = mp4 + ".audio.m4a", mp4 + ".nuevo.mp4"
subprocess.run([FF, "-loglevel", "error", "-y", "-ss", "2600", "-i", url, "-t", "108", "-vn", "-c:a", "aac", "-b:a", "192k", tmp], check=True)


def pcm(ruta):
    b = subprocess.run([FF, "-v", "error", "-i", ruta, "-t", "40", "-vn", "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(b, np.float32)


# misma narración y alineada con el audio que ya tenía: si no, sería otro doblaje o un desfase
a, b = pcm(mp4), pcm(tmp)
n = min(len(a), len(b))
c = np.fft.irfft(np.fft.rfft(a[:n], 2 * n) * np.conj(np.fft.rfft(b[:n], 2 * n)))
k = int(np.argmax(c))
print(f"desfase {(k if k < n else k - 2 * n) / 8000:+.3f} s · correlación {c[k] / (np.linalg.norm(a[:n]) * np.linalg.norm(b[:n])):.2f}")
assert c[k] / (np.linalg.norm(a[:n]) * np.linalg.norm(b[:n])) > .5
assert abs(k if k < n else k - 2 * n) < 800
subprocess.run([FF, "-loglevel", "error", "-y", "-i", mp4, "-i", tmp, "-map", "0:v:0", "-map", "1:a:0", "-c", "copy", nuevo], check=True)
d = subprocess.run([r"C:\ffmpeg\bin\ffprobe.exe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=duration", "-of", "csv=p=0", nuevo],
                   capture_output=True, text=True).stdout.strip()
print("audio nuevo:", d, "s")
assert float(d) > 100
shutil.move(nuevo, mp4)
os.remove(tmp)
