# -*- coding: utf-8 -*-
"""Sonido original SIN el narrador (oot_remake_cambios, 26-oct-2026): la demo de Aonuma y el tráiler general traen una voz en
inglés encima del juego. Para los beats donde queremos oír el juego (regla del usuario del 26-oct: música, gritos, SFX), Demucs
(htdemucs --two-stems vocals) separa la voz y el clip se queda con `no_vocals` (música + efectos). Whisper lo comprueba después.
    python quitar_narrador.py 23 24 51 ...     (números de beat)
"""
import os
import shutil
import subprocess
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
TMP = os.path.join(AQUI, "audio", "_demucs")


def uno(n):
    clip = os.path.join(AQUI, "medios", f"scene-{n:03d}.mp4")
    base = f"s{n:03d}"
    wav = os.path.join(TMP, base + ".wav")
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", clip, "-vn", "-ac", "2", "-ar", "44100", wav], check=True)
    subprocess.run([sys.executable, "-m", "demucs", "--two-stems", "vocals", "-n", "htdemucs", "-o", TMP, wav], check=True,
                   capture_output=True)
    limpio = os.path.join(TMP, "htdemucs", base, "no_vocals.wav")
    nuevo = clip[:-4] + "_sv.mp4"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-i", clip, "-i", limpio, "-map", "0:v", "-map", "1:a", "-c:v", "copy",
                    "-c:a", "aac", "-b:a", "160k", "-ar", "48000", "-shortest", nuevo], check=True)
    os.replace(nuevo, clip)
    print(f"scene-{n:03d}: narrador separado", flush=True)


if __name__ == "__main__":
    os.makedirs(TMP, exist_ok=True)
    for a in sys.argv[1:]:
        uno(int(a))
    shutil.rmtree(TMP, ignore_errors=True)
