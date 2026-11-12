# -*- coding: utf-8 -*-
"""Voz ajena en los clips con ambiente_por (7-nov): Demucs separa la voz de cada clip y se mide/transcribe SOLO esa pista.
    python _voz_ajena.py [scene-015 ...]   -> nivel de la pista de voz por segundo + Whisper medium sobre ella
"""
import os, subprocess, sys
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import guion
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
TMP = os.path.join("audio", "_demucs_chk")
ids = sys.argv[1:] or [k for k, v in guion.SECUENCIA["ambiente_por"].items() if v > 0]
os.makedirs(TMP, exist_ok=True)
from faster_whisper import WhisperModel
m = WhisperModel("medium", device="cuda", compute_type="float16")
for k in ids:
    w = os.path.join(TMP, k + ".wav")
    subprocess.run([FF, "-y", "-v", "error", "-i", os.path.join("medios", k + ".mp4"), "-vn", "-ac", "2", "-ar", "44100", w], check=True)
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-n", "htdemucs", "-o", TMP, w], check=True, capture_output=True)
    v, sr = sf.read(os.path.join(TMP, "htdemucs", k, "vocals.wav"))
    t, _ = sf.read(w)
    v = v.mean(1); t = t.mean(1)
    db = lambda x: 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)
    por_s = [db(v[i:i + sr]) for i in range(0, len(v), sr)]
    print(f"{k} voz {db(v):6.1f} dB / total {db(t):6.1f} dB | por s: " + " ".join(f"{x:.0f}" for x in por_s), flush=True)
    segs, info = m.transcribe(os.path.join(TMP, "htdemucs", k, "vocals.wav"), vad_filter=False, condition_on_previous_text=False)
    for s in segs:
        if s.no_speech_prob < 0.6:
            print(f"    {s.start:5.1f}-{s.end:5.1f} [{info.language}] {s.text.strip()[:120]}", flush=True)
