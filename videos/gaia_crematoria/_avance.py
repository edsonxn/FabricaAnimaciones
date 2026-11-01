# -*- coding: utf-8 -*-
"""AVANCE del render mientras corre: une los segmentos ya terminados (seguidos desde el 0) con su tramo de audio/final.wav en
salida/AVANCE.mp4 (copia de video, sin recodificar). Uso (desde la carpeta del video): python _avance.py"""
import json
import os
import subprocess

FF = r"C:\ffmpeg\bin\ffmpeg.exe"
info = json.load(open("segmentos/info.json", encoding="utf-8"))
dur_seg = info["tam"] / info["fps"]
n = 0
while os.path.exists(f"segmentos/seg_{n:04d}.mp4"):
    n += 1
if n == 0:
    raise SystemExit("todavía no hay segmentos terminados")
lista = os.path.abspath("segmentos/_avance.txt")
with open(lista, "w", encoding="utf-8") as f:
    for i in range(n):
        f.write(f"file '{os.path.abspath(f'segmentos/seg_{i:04d}.mp4').replace(os.sep, '/')}'\n")
os.makedirs("salida", exist_ok=True)
subprocess.run([FF, "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lista, "-i", "audio/final.wav", "-map", "0:v",
                "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-t", f"{n * dur_seg:.2f}", "-shortest",
                "salida/AVANCE.mp4"], check=True)
os.remove(lista)
# copia ligera (1280 px, ~10 MB/min) para verla en el navegador de la app (salida/avance.html) o en el teléfono
subprocess.run([FF, "-y", "-loglevel", "error", "-i", "salida/AVANCE.mp4", "-vf", "scale=1280:-2", "-c:v", "libx264", "-preset",
                "veryfast", "-crf", "26", "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", "salida/AVANCE_ligero.mp4"],
               check=True)
print(f"salida/AVANCE.mp4 y AVANCE_ligero.mp4: {n} segmentos = {n * dur_seg / 60:.1f} min")
