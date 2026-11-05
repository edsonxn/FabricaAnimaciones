# -*- coding: utf-8 -*-
import os, glob, numpy as np, librosa
AQUI = os.path.dirname(os.path.abspath(__file__))
try:
    from faster_whisper import WhisperModel
    W = WhisperModel("small", device="cpu", compute_type="int8")
except Exception as e:
    W = None; print("sin whisper", e)
for f in sorted(glob.glob(os.path.join(AQUI, "*.mp3"))):
    y, sr = librosa.load(f, sr=22050)
    f0, vo, _ = librosa.pyin(y, fmin=50, fmax=300, sr=sr)
    f0 = f0[~np.isnan(f0)]
    txt = ""
    if W:
        segs, _ = W.transcribe(f, language="es")
        txt = " ".join(s.text for s in segs)
    print(f"{os.path.basename(f):14s} dur {len(y)/sr:5.1f}s  F0 med {np.median(f0):5.0f} Hz  p10 {np.percentile(f0,10):4.0f}  | {txt}")
