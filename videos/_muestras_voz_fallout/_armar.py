# -*- coding: utf-8 -*-
"""Radio Yermo (17-nov-2026). Une las muestras en un mp4 con una cartela por opción (para la tele y el chat)."""
import glob
import os
import subprocess

AQUI = os.path.dirname(os.path.abspath(__file__))
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
FUENTE = "C\\:/Windows/Fonts/arialbd.ttf"
ROT = {
    "00_profeta_ref": ("REFERENCIA", "el Profeta (Tamriel y Runa)"),
    "01_jose": ("OPCION 1", "Jose - locutor grave (Mexico)"),
    "02_zabra": ("OPCION 2", "Zabra - locutor de radio con energia (Mexico)"),
    "03_juan_pablo": ("OPCION 3", "Juan Pablo - locutor nortenio"),
    "04_brian": ("OPCION 4", "Brian C - calido y limpio"),
    "05_bardo": ("OPCION 5", "Bardo Limon - sonoro y sincero"),
    "06_carlos_pro": ("OPCION 6", "Carlos Pro - radio y documental (Argentina)"),
}
partes = []
for mp3 in sorted(glob.glob(os.path.join(AQUI, "0*.mp3"))):
    n = os.path.splitext(os.path.basename(mp3))[0]
    a, b = ROT[n]
    out = os.path.join(AQUI, f"_seg_{n}.mp4")
    vf = (f"drawtext=fontfile='{FUENTE}':text='{a}':fontsize=110:fontcolor=0x3CFF8C:x=(w-tw)/2:y=h/2-150,"
          f"drawtext=fontfile='{FUENTE}':text='{b}':fontsize=64:fontcolor=white:x=(w-tw)/2:y=h/2+20")
    subprocess.run([FF, "-y", "-loglevel", "error", "-f", "lavfi", "-i", "color=c=0x04100a:s=1920x1080:r=30",
                    "-i", mp3, "-af", "apad=pad_dur=0.9", "-vf", vf, "-shortest",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-ar", "44100", "-ac", "2", out], check=True)
    partes.append(out)
lista = os.path.join(AQUI, "_lista.txt")
open(lista, "w").write("".join(f"file '{p}'\n" for p in partes))
final = os.path.join(AQUI, "voces_radio_yermo_muestras.mp4")
subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-c", "copy", final], check=True)
for p in partes:
    os.remove(p)
os.remove(lista)
print(final)
