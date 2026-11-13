# -*- coding: utf-8 -*-
"""Frases con nombres de comentaristas o palabras extranjeras: Whisper con idioma AUTOMÁTICO por ventanas de 3 s (paso 1,5 s)
sobre voz/final/<key>.wav. Marca toda ventana cuya p(es) < 0,8 (el 12-nov `idioma_voz` dejó pasar «Yorsh…» leído en inglés).
    python _check_nombres.py"""
import os
import re
import sys

import numpy as np
import soundfile as sf
from faster_whisper import WhisperModel

os.chdir(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ".")
import guion  # noqa: E402

NOMBRES = r"Alberto|Arnold|Marcos|Fetixe|Yorsh|Pablo|Alexander|Sevilla|Sargento|add-on|CurseForge|PNJ|Questie|Hogger|Mankrik|VanCleef|Mor'Ladim|Stalvan|Sayge|Mulgore|Forever|Classic|Retail|Overgear|Brogan|Edwin|Defias|Elwynn|Durotar|Teldrassil|Darnassus|Orgrimmar|Menethil|Theramore|Auberdine|Nesingwary|Loch Modan|Dun Morogh"
keys = [(f"{e['id']}_{i}", f) for e in guion.ESCENAS for i, f in enumerate(e["frases"])]   # TODAS (12-nov: también oraciones cortas)
wm = WhisperModel("large-v3", device="cuda", compute_type="float16")
malas = []
for k, f in keys:
    y, sr = sf.read(f"voz/final/{k}.wav", always_2d=True)
    y = y.mean(1).astype(np.float32)
    if sr != 16000:
        import librosa
        y = librosa.resample(y, orig_sr=sr, target_sr=16000)
    n, w, h = len(y), 3 * 16000, int(1.5 * 16000)
    for a in range(0, max(1, n - w // 2), h):
        seg = y[a:a + w]
        if len(seg) < 16000:
            continue
        _, info = wm.transcribe(seg, language=None, beam_size=1)
        pes = dict(info.all_language_probs or []).get("es", 0.0)
        if pes < 0.8:
            txt = " ".join(s.text for s in wm.transcribe(seg, language=None, beam_size=1)[0]).strip()
            malas.append((k, a / 16000, round(pes, 2), info.language, txt))
print(f"{len(keys)} frases revisadas por ventanas de 3 s")
for m in malas:
    print("  X", m)
