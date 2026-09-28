# -*- coding: utf-8 -*-
"""Control de calidad final: (1) Whisper frase por frase sobre audio/final.wav (CER con el guion),
(2) duración y desfase audio/video del MASTER, (3) hoja de 12 cuadros decodificados del MASTER.
Uso: python fab.py <video> verificar"""
import glob
import json
import os
import subprocess

import cv2
import librosa
import numpy as np
import soundfile as sf

import config
from qa import cer

TL = json.load(open("timeline.json", encoding="utf-8"))
os.makedirs("previews", exist_ok=True)

# (1) inteligibilidad sobre la mezcla final
from faster_whisper import WhisperModel

y, sr = sf.read("audio/final.wav")
m16 = librosa.resample(y.mean(1).astype(np.float32), orig_sr=sr, target_sr=16000)
wm = WhisperModel("large-v3", device="cuda", compute_type="float16")
malas, cs = [], []
for e in TL["escenas"]:
    for f in e["frases"]:
        a, b = int((f["t0"] - 0.15) * 16000), int((f["t1"] + 0.15) * 16000)
        prompt = "Número uno: el pan." if f["texto"].startswith("Número") else None
        segs, _ = wm.transcribe(m16[a:b], language=config.VOZ["idioma"], beam_size=5, initial_prompt=prompt)
        hyp = " ".join(s.text for s in segs).strip()
        c = cer(f["texto"], hyp)
        cs.append(c)
        if c > 0.02:
            malas.append((f["key"], round(c, 3), hyp))
print(f"Inteligibilidad (Whisper sobre la mezcla final): CER medio {np.mean(cs):.4f}, frases con CER>2%: {len(malas)}")
for m in malas:
    print("   ", m)

# (2) y (3) sobre el MASTER
masters = glob.glob("salida/*_MASTER.mp4")
if not masters:
    print("Sin MASTER todavía: se omiten duración, desfase y cuadros.")
    raise SystemExit
M = masters[0]
info = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "stream=codec_type,duration,width,height,r_frame_rate",
                       "-of", "compact", M], capture_output=True, text=True).stdout.strip()
print("MASTER:", M, "\n", info)
tmp = "previews/_audio_master.wav"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", M, "-vn", "-ac", "1", "-ar", "48000", tmp], check=True)
a, _ = sf.read("audio/final.wav")
b, _ = sf.read(tmp)
a = a.mean(1)
seg = slice(int(20 * 48000), int(30 * 48000))
from scipy.signal import correlate
c = correlate(b[seg], a[seg], mode="full", method="fft")
lag = int(np.argmax(c) - (len(a[seg]) - 1))
print(f"Desfase audio MP4 vs master: {lag} muestras ({lag / 48:.2f} ms)")
os.remove(tmp)
tiles = []
for t in np.linspace(2.0, TL["total"] - 1.5, 12):
    out = f"previews/_f_{t:07.2f}.png"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", M, "-frames:v", "1", "-vf", "scale=640:360", out], check=True)
    im = cv2.imread(out)
    cv2.putText(im, f"{t:.1f}s", (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 3, cv2.LINE_AA)
    cv2.putText(im, f"{t:.1f}s", (8, 350), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
    tiles.append(im)
    os.remove(out)
cv2.imwrite("previews/final_hoja.jpg", np.vstack([np.hstack(tiles[i:i + 3]) for i in range(0, 12, 3)]),
            [cv2.IMWRITE_JPEG_QUALITY, 88])
print("previews/final_hoja.jpg")
