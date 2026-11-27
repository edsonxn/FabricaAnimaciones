# -*- coding: utf-8 -*-
"""Voz de campana_dc_topes (sátira 30 s) con ElevenLabs: Daniel Cervantes CLONADA (cuenta 4, eleven_v4_turbo, sin corchetes).
Pide /with-timestamps para saber cuándo cae cada palabra («tope», groserías). `python voz.py [--semilla N] [--solo 2,5]`
Escribe voz/l<n>.wav, voz/l<n>.json (palabras con tiempo, ya descontado el recorte) y voz/voz.wav + voz/tiempos.json."""
import base64
import io
import json
import os
import subprocess
import sys
import types

import librosa
import numpy as np
import soundfile as sf

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
_c = types.ModuleType("config"); _c.VOZ = {}; sys.modules["config"] = _c
import tts_eleven as t  # noqa: E402

VOZ_ID = "U6S3DHgp2HdE70osCRov"   # Daniel Cervantes (clon, cuenta 4)
t._activa = [i for i, (n, _) in enumerate(t.cuentas()) if n == 4][0]
FRASES = [
    "¡Ay, cabrón! ¡Otro pinche tope!",
    "En Juchipila hay más topes que calles, ¡no mamen!",
    "Vas al centro: tope. Vas por las tortillas: tope. Vas a misa: ¡tope, tope, tope!",
    "Se te sale el mofle, se te truena la suspensión... ¡y te cagas del susto!",
    "¡Ya me tienen hasta la verga estos putos topes!",
    "Por eso, mi primera orden como presidente...",
    "¡Tirar todos los pinches topes de Juchipila!",
    "¡A la verga los topes! Soy Daniel Cervantes.",
]
PAUSA = [0.0, 0.2, 0.2, 0.2, 0.25, 0.3, 0.25, 0.35]   # silencio ANTES de cada frase
ESTAB = 0.45   # más suelta que la sobria (.65): aquí va enojado
FFMPEG = r"C:/ffmpeg/bin/ffmpeg.exe"
TEMPO = 1.1    # se acelera con atempo (mismo tono): ritmo de caricatura y cabe en ~30 s


def palabras(txt, al, recorte):
    """Alineación por carácter → [(palabra, t0, t1)] en segundos dentro del audio YA recortado."""
    ch, t0s, t1s = al["characters"], al["character_start_times_seconds"], al["character_end_times_seconds"]
    out, cur, a = [], "", None
    for c, s, e in zip(ch, t0s, t1s):
        if c.isalnum() or c in "áéíóúñüÁÉÍÓÚÑ":
            if not cur:
                a = s
            cur += c; b = e
        elif cur:
            out.append((cur.lower(), round(a - recorte, 3), round(b - recorte, 3))); cur = ""
    if cur:
        out.append((cur.lower(), round(a - recorte, 3), round(b - recorte, 3)))
    return out


def main():
    a = sys.argv[1:]
    semilla = int(a[a.index("--semilla") + 1]) if "--semilla" in a else 11
    solo = {int(x) for x in a[a.index("--solo") + 1].split(",")} if "--solo" in a else None
    os.makedirs(os.path.join(AQUI, "voz"), exist_ok=True)
    sr = 44100
    for i, txt in enumerate(FRASES, 1):
        p = os.path.join(AQUI, "voz", f"l{i}.wav")
        if os.path.exists(p) and not (solo and i in solo):
            continue
        body = dict(text=txt, model_id="eleven_v4_turbo", seed=semilla, language_code="es",
                    voice_settings=dict(stability=ESTAB, similarity_boost=0.8))
        r = t.post(f"text-to-speech/{VOZ_ID}/with-timestamps?output_format=mp3_44100_128", json=body, timeout=120)
        if r.status_code != 200:
            raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:200]}")
        d = r.json()
        y, _ = librosa.load(io.BytesIO(base64.b64decode(d["audio_base64"])), sr=sr, mono=True)
        y, idx = librosa.effects.trim(y, top_db=38)
        sf.write(p, y, sr)
        pal = palabras(txt, d["alignment"], idx[0] / sr)
        json.dump(pal, open(p[:-4] + ".json", "w", encoding="utf-8"), ensure_ascii=False)
        print(f"l{i}: {len(y) / sr:.2f} s · costo {r.headers.get('character-cost')} · {pal}")
    partes, tiempos, todas, cur = [], [], [], 0.0
    for i in range(1, len(FRASES) + 1):
        src = os.path.join(AQUI, "voz", f"l{i}.wav"); rap = src[:-4] + "_r.wav"
        subprocess.run([FFMPEG, "-y", "-loglevel", "error", "-i", src, "-af", f"atempo={TEMPO}", rap], check=True)
        y, _ = librosa.load(rap, sr=sr)
        pa = np.zeros(int(PAUSA[i - 1] * sr), np.float32)
        partes += [pa, y]
        cur += len(pa) / sr
        tiempos.append([round(cur, 3), round(cur + len(y) / sr, 3)])
        for w, x0, x1 in json.load(open(os.path.join(AQUI, "voz", f"l{i}.json"), encoding="utf-8")):
            todas.append([i, w, round(cur + max(0, x0) / TEMPO, 3), round(cur + x1 / TEMPO, 3)])
        cur += len(y) / sr
    v = np.concatenate(partes)
    sf.write(os.path.join(AQUI, "voz", "voz.wav"), v, sr)
    json.dump(dict(frases=tiempos, palabras=todas, total=round(cur, 3)),
              open(os.path.join(AQUI, "voz", "tiempos.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print("total", round(cur, 2), "s ·", tiempos)


if __name__ == "__main__":
    main()
