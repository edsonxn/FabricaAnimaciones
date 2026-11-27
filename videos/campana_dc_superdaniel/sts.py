# -*- coding: utf-8 -*-
"""Voz de Daniel sobre los clips de Flow: `python sts.py c1 [c2 ...]`.
1) Demucs separa clips/<c>_360.mp4 en voz (lo que dijo el actor de Flow, con lipsync) y resto (SFX/ambiente del clip).
2) ElevenLabs speech-to-speech (cuenta 4, clon de Daniel U6S3DHgp2HdE70osCRov) convierte esa voz: conserva tiempos y
   entonación, así los labios siguen sincronizados.
3) Remezcla voz de Daniel + resto -> audio/<c>_daniel.wav (48 kHz)."""
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

VOZ_ID = "U6S3DHgp2HdE70osCRov"   # Daniel Cervantes (clon, cuenta 4; con su permiso, solo campaña)
t._activa = [i for i, (n, _) in enumerate(t.cuentas()) if n == 4][0]
SR = 48000


def separa(c):
    sep = os.path.join(AQUI, "audio", "sep")
    os.makedirs(sep, exist_ok=True)
    wav = os.path.join(AQUI, "audio", f"{c}_orig.wav")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", os.path.join(AQUI, "clips", f"{c}_360.mp4"), "-vn", "-ac", "2",
                    "-ar", "44100", wav], check=True)
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-n", "htdemucs", "-o", sep, wav], check=True)
    d = os.path.join(sep, "htdemucs", f"{c}_orig")
    return os.path.join(d, "vocals.wav"), os.path.join(d, "no_vocals.wav")


def convierte(voc, c):
    with open(voc, "rb") as f:
        r = t.post(f"speech-to-speech/{VOZ_ID}?output_format=mp3_44100_128",
                   files={"audio": ("voz.wav", f, "audio/wav")},
                   data={"model_id": "eleven_multilingual_sts_v2", "remove_background_noise": "true",
                         "voice_settings": json.dumps(dict(stability=0.65, similarity_boost=0.8))},
                   timeout=180)
    if r.status_code != 200:
        raise SystemExit(f"ElevenLabs {r.status_code}: {r.text[:300]}")
    y, _ = librosa.load(io.BytesIO(r.content), sr=SR, mono=True)
    sf.write(os.path.join(AQUI, "audio", f"{c}_voz_daniel.wav"), y, SR)
    return y


def main():
    for c in sys.argv[1:]:
        voc, resto = separa(c)
        v = convierte(voc, c)
        r, _ = librosa.load(resto, sr=SR, mono=True)
        n = max(len(v), len(r))
        mezcla = np.pad(v, (0, n - len(v))) * 1.0 + np.pad(r, (0, n - len(r))) * 0.8
        mezcla /= max(1.0, np.abs(mezcla).max() / 0.95)
        sf.write(os.path.join(AQUI, "audio", f"{c}_daniel.wav"), mezcla.astype(np.float32), SR)
        print(f"{c}: voz Daniel {len(v) / SR:.2f} s -> audio/{c}_daniel.wav")


if __name__ == "__main__":
    main()
