# -*- coding: utf-8 -*-
"""Baja la BANDA SONORA OFICIAL de Elden Ring a audio/ost/ (regla del 23-oct-2026: nada de Lyria en Runa Caída).
Copia lo ya bajado en Godrick/Mohg y baja lo nuevo por id (canales «- Topic» / compositor, comprobados el 16-nov-2026).
    python bajar_ost.py   (desde la carpeta del video)
"""
import os
import shutil
import subprocess
import sys

OST = os.path.join("audio", "ost")
GD = "../er_godrick_atrocidades/audio/ost/"
COPIAR = {"tema": GD + "tema.wav", "mesa": GD + "mesa.wav", "frenesi": GD + "frenesi.wav", "omen": GD + "omen.wav",
          "limgrave": GD + "limgrave.wav", "godrick": GD + "godrick.wav"}
FIJOS = {"rennala": "mKOpTUezXeM",    # Rennala, Queen of the Full Moon (Yuka Kitamura)
         "radahn": "Z1ts4FP1WWM",     # Starscourge Radahn (Shoi Miyazawa - Topic)
         "volcan": "SOyzVrM28M4",     # Volcano Manor (Yoshimi Kudo - Topic)
         "rykard": "otyGVdWf5Mc",     # God-Devouring Serpent (Yoshimi Kudo - Topic)
         "liurnia": "_43OlSUHtLo",    # Liurnia of the Lakes (Yoshimi Kudo - Topic)
         "academia": "hEaRJ5geIY8",   # Academy of Raya Lucaria (Yuka Kitamura)
         "gigante": "r2NZHaO6NUc",    # Fire Giant (Yuka Kitamura)
         "maliketh": "CNK12YsQFr4",   # Beast Clergyman / Maliketh (Shoi Miyazawa - Topic)
         "leyndell": "qQGD67_mLkc",   # Leyndell, Royal Capital (Yuka Kitamura)
         "godfrey": "lHqZZkDvW-o",    # Godfrey, First Elden Lord (Tai Tomisawa - Topic)
         "final": "R3R-hzDPi1A",      # The Final Battle (Tsukasa Saitoh - Topic)
         "mesa_velada": "rJKXX6bDFF4"}  # The Shrouded Roundtable Hold (Shoi Miyazawa - Topic)


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
