# -*- coding: utf-8 -*-
"""Baja la BANDA SONORA OFICIAL de Elden Ring a audio/ost/ (regla del 23-oct-2026: nada de Lyria en Runa Caída).
Copia lo ya bajado en Mohg/Morgott y baja lo nuevo de los canales «- Topic» por id (comprobados el 11-nov-2026).
    python bajar_ost.py   (desde la carpeta del video)
"""
import os
import shutil
import subprocess
import sys

OST = os.path.join("audio", "ost")
MH = "../er_mohg_atrocidades/audio/ost/"
COPIAR = {"tema": MH + "tema.wav", "mesa": MH + "mesa.wav", "omen": MH + "omen.wav", "frenesi": MH + "frenesi.wav"}
FIJOS = {"godrick": "Lr8EPMRN0rg",    # Godrick the Grafted (Shoi Miyazawa - Topic)
         "velo": "tfVTw66YYeU",       # Stormveil Castle (Tai Tomisawa - Topic)
         "limgrave": "jZbBRLkRmSU",   # Limgrave (Tsukasa Saitoh - Topic)
         "margit": "qrE-HvIM1Pg"}     # Margit, the Fell Omen (Tsukasa Saitoh - Topic)


def bajar(nombre, url):
    if os.path.isfile(os.path.join(OST, nombre + ".wav")):
        return
    subprocess.run([sys.executable, "-m", "yt_dlp", "-x", "--audio-format", "wav", "--no-playlist", "--max-downloads", "1",
                    "--print", "after_move:%(channel)s | %(title)s | %(id)s | %(duration)s",
                    "-o", os.path.join(OST, nombre + ".%(ext)s"), url], check=False)


os.makedirs(OST, exist_ok=True)
for n, r in COPIAR.items():
    if not os.path.isfile(os.path.join(OST, n + ".wav")) and os.path.isfile(r):
        shutil.copy(r, os.path.join(OST, n + ".wav"))
for n, i in FIJOS.items():
    bajar(n, f"https://www.youtube.com/watch?v={i}")
print(sorted(os.listdir(OST)))
