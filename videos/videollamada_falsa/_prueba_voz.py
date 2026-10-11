# -*- coding: utf-8 -*-
"""Prueba suelta de la voz con eleven_v3 y etiquetas entre corchetes (no toca voz/). Uso: python _prueba_voz.py [stability]
Escribe previews/prueba_voz_<n>.mp3 e imprime costo, duración y palabras/s."""
import io
import os
import re
import sys

import librosa
import requests

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.abspath(os.path.join(AQUI, "..", ".."))
K = open(os.path.join(RAIZ, "canales", "tokens", "elevenlabs_api_key.txt"), encoding="utf-8").read().strip()
VOZ = "0hh7H4ZVAtaGpm1VZyEN"
MODELO = sys.argv[1] if len(sys.argv) > 1 else "eleven_v3"
ST = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
FRASES = [
    "[thoughtful] En esta ciudad, la gente ya no desconfía de los extraños. [short pause] Desconfía de las caras conocidas.",
    "[sighs] Quince transferencias. Cinco cuentas. Doscientos millones de dólares de Hong Kong.",
    "[whispers] Y en aquella sala, nadie era real. [short pause] Nadie, excepto él.",
]
for n, f in enumerate(FRASES):
    body = dict(text=f, model_id=MODELO, seed=1, language_code="es", voice_settings=dict(stability=ST))
    r = requests.post(f"https://api.elevenlabs.io/v1/text-to-speech/{VOZ}?output_format=mp3_44100_128", json=body,
                      headers={"xi-api-key": K}, timeout=180)
    if r.status_code != 200:
        print(r.status_code, r.text[:400])
        break
    p = os.path.join(AQUI, "previews", f"prueba_{MODELO}_{n}.mp3")
    open(p, "wb").write(r.content)
    y, sr = librosa.load(io.BytesIO(r.content), sr=None, mono=True)
    pal = len(re.sub(r"\[[^\]]*\]", " ", f).split())
    print(n, "costo", r.headers.get("character-cost"), "chars", len(f), f"dur {len(y) / sr:.2f}s", f"{pal / (len(y) / sr):.2f} pal/s")
