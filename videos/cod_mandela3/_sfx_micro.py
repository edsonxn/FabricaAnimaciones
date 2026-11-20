# -*- coding: utf-8 -*-
"""SFX del intruso (19-nov-2026): micrófono arrebatado con feedback, y el micro devuelto. ElevenLabs sound-generation (cuenta con saldo).
Uso (desde la carpeta del video): python _sfx_micro.py"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "nucleo"))
import tts_eleven as T  # noqa: E402

SFX = {
    "micro_arrebatado": ("A microphone being snatched out of someone's hand: rough handling thumps and fabric rustle on the mic, "
                         "a short sharp audio feedback squeal, close and dry", 1.8),
    "micro_devuelto": ("A microphone handed back roughly: two handling thumps and a small tap on the mic grille, close and dry", 1.0),
}
for nombre, (prompt, seg) in SFX.items():
    for v in (1, 2):
        out = f"sfx/{nombre}{'' if v == 1 else '_2'}.mp3"
        if os.path.exists(out):
            continue
        r = T.post("sound-generation", json=dict(text=prompt, duration_seconds=seg, prompt_influence=0.6), timeout=120)
        if r.status_code != 200:
            raise SystemExit(f"{nombre}: {r.status_code} {r.text[:300]}")
        open(out, "wb").write(r.content)
        print(out, len(r.content) // 1024, "KB")
