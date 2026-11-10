# -*- coding: utf-8 -*-
"""Baja la BANDA SONORA OFICIAL de Elden Ring a audio/ost/ (regla del 23-oct-2026: nada de Lyria en Runa Caída).
Copia lo ya bajado en Morgott/Radahn y baja lo nuevo de los canales «- Topic» por id (comprobados el 10-nov-2026).
    python bajar_ost.py
"""
import os
import shutil
import subprocess
import sys

OST = os.path.join("audio", "ost")
MO = "../er_morgott_atrocidades/audio/ost/"
RA = "../er_radahn_atrocidades/audio/ost/"
COPIAR = {"tema": MO + "tema.wav", "mesa": MO + "mesa.wav", "mohg": MO + "mohg.wav", "frenesi": MO + "frenesi.wav",
          "malenia": RA + "malenia.wav"}
FIJOS = {"omen": "yvMQYoCZ9hA",       # Omen Illusion (Shoi Miyazawa - Topic) = Mohg, el Augurio
         "godskin": "YCauPz3hyfM",    # Godskin Apostles (Tai Tomisawa - Topic)
         "astel": "pFrbhWZpJaM"}      # Astel, Naturalborn of the Void (Tai Tomisawa - Topic): el dios exterior


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
