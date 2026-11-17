# -*- coding: utf-8 -*-
"""Radio Yermo (17-nov-2026): las mismas muestras con el filtro de radio del juego (nucleo/fx_radio.py), en 3 modos por voz:
A = radio completa · B = combinación (radio en el saludo, luego el narrador se acerca al micrófono) · C = narrador con un toque de radio.
Sin créditos nuevos: reusa los mp3 de _generar.py. Uso: python _radio.py  ->  voces_radio_yermo_filtro.mp4"""
import glob
import os
import re
import subprocess
import sys

import numpy as np
import soundfile as sf

sys.path.insert(0, r"C:\FabricaAnimaciones\nucleo")
import fx_radio as R

AQUI = os.path.dirname(os.path.abspath(__file__))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
FUENTE = "C\:/Windows/Fonts/arialbd.ttf"
SR = 44100
NOM = {"01_jose": "Jose", "02_zabra": "Zabra", "03_juan_pablo": "Juan Pablo", "04_brian": "Brian C",
       "05_bardo": "Bardo Limon", "06_carlos_pro": "Carlos Pro"}
MODOS = {"A": "radio completa", "B": "combinacion radio + narrador", "C": "narrador con toque de radio"}


def leer(mp3):
    raw = subprocess.run([FF, "-loglevel", "error", "-i", mp3, "-ac", "1", "-ar", str(SR), "-f", "f32le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).copy()


def corte(mp3):
    """Mitad del silencio que sigue a «...lo que queda del mundo.» (primer silencio que empieza después de los 5 s)."""
    err = subprocess.run([FF, "-hide_banner", "-i", mp3, "-af", "silencedetect=n=-35dB:d=0.22", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    ini = [float(v) for v in re.findall(r"silence_start: ([\d.]+)", err)]
    fin = [float(v) for v in re.findall(r"silence_end: ([\d.]+)", err)]
    for a, b in zip(ini, fin):
        if a > 5.0:
            return (a + b) / 2
    return 6.3


partes = []
for mp3 in sorted(glob.glob(os.path.join(AQUI, "0[1-9]_*.mp3"))):
    n = os.path.splitext(os.path.basename(mp3))[0]
    x = leer(mp3)
    for k, modo in MODOS.items():
        if k == "A":
            y = np.concatenate([R.sintonia(SR), R.radio(x, SR)])
        elif k == "B":
            y = np.concatenate([R.sintonia(SR), R.mezcla(x, SR, corte(mp3))])
        else:
            y = R.tinte(x, SR)
        wav = os.path.join(AQUI, f"_{n}_{k}.wav")
        sf.write(wav, np.concatenate([y, np.zeros(int(0.8 * SR), np.float32)]), SR)
        num = n[:2].lstrip("0")
        out = os.path.join(AQUI, f"_seg_{n}_{k}.mp4")
        vf = (f"drawtext=fontfile='{FUENTE}':text='OPCION {num}{k}':fontsize=74:fontcolor=0x3CFF8C:x=(w-tw)/2:y=h/2-115,"
              f"drawtext=fontfile='{FUENTE}':text='{NOM[n]}':fontsize=48:fontcolor=white:x=(w-tw)/2:y=h/2-8,"
              f"drawtext=fontfile='{FUENTE}':text='{modo}':fontsize=36:fontcolor=0xA0FFC0:x=(w-tw)/2:y=h/2+60")
        if not os.path.exists(out):
            subprocess.run([FF, "-y", "-loglevel", "error", "-threads", "2", "-f", "lavfi", "-i", "color=c=0x04100a:s=1280x720:r=24", "-i", wav,
                            "-vf", vf, "-shortest", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                            "-ar", "44100", "-ac", "2", out], check=True)
        partes.append(out)
lista = os.path.join(AQUI, "_lista.txt")
open(lista, "w").write("".join(f"file '{p}'\n" for p in partes))
final = os.path.join(AQUI, "voces_radio_yermo_filtro.mp4")
subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", final], check=True)
for p in partes:
    os.remove(p)
os.remove(lista)
print(final)
