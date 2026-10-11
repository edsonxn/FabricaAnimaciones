# -*- coding: utf-8 -*-
"""Transcribe con Whisper los mp3 de prueba (previews/prueba_*.mp3) para ver si algún modelo LEE las etiquetas en voz alta."""
import glob
import os

from faster_whisper import WhisperModel

AQUI = os.path.dirname(os.path.abspath(__file__))
wm = WhisperModel("large-v3", device="cuda", compute_type="float16")
for p in sorted(glob.glob(os.path.join(AQUI, "previews", "prueba_*.mp3"))):
    segs, _ = wm.transcribe(p, language="es", beam_size=5, vad_filter=False)
    print(os.path.basename(p), "|", " ".join(s.text for s in segs).strip())
