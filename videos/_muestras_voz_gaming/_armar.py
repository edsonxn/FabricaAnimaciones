# -*- coding: utf-8 -*-
"""Une las muestras en un mp4 con una cartela por opción (para la tele y el chat)."""
import glob
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
FUENTE = "C\\:/Windows/Fonts/arialbd.ttf"
ROT = {
    "00_hope_actual": ("ACTUAL", "Hope (la de siempre)"),
    "00_profeta_ref": ("REFERENCIA", "el Profeta (Runa y Tamriel)"),
    "01_salvatore": ("OPCION 1", "Salvatore - epica y mistica"),
    "02_miguel": ("OPCION 2", "Miguel - voz de trailer"),
    "03_ludovico": ("OPCION 3", "Ludovico - bajo retumbante"),
    "04_santiago": ("OPCION 4", "Santiago - rasposa, de mando"),
    "05_carlos_aguilar": ("OPCION 5", "Carlos Aguilar - potente"),
    "06_david_misterio": ("OPCION 6", "David - misterio y terror"),
    "07_francis": ("OPCION 7", "Francis - profunda y calida"),
    "08_arconte": ("OPCION 8", "Arconte - elegante (Espana)"),
}
partes = []
for mp3 in sorted(glob.glob(os.path.join(AQUI, "0*.mp3"))):
    n = os.path.splitext(os.path.basename(mp3))[0]
    a, b = ROT[n]
    out = os.path.join(AQUI, f"_seg_{n}.mp4")
    vf = (f"drawtext=fontfile='{FUENTE}':text='{a}':fontsize=110:fontcolor=0xF2C14E:x=(w-tw)/2:y=h/2-150,"
          f"drawtext=fontfile='{FUENTE}':text='{b}':fontsize=64:fontcolor=white:x=(w-tw)/2:y=h/2+20")
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=0x14161c:s=1920x1080:r=30",
                    "-i", mp3, "-af", "apad=pad_dur=0.9", "-vf", vf, "-shortest",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "44100", "-ac", "2", out], check=True)
    partes.append(out)
lista = os.path.join(AQUI, "_lista.txt")
open(lista, "w").write("".join(f"file '{p}'\n" for p in partes))
final = os.path.join(AQUI, "voces_gaming_muestras.mp4")
subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", final], check=True)
for p in partes:
    os.remove(p)
os.remove(lista)
print(final)
