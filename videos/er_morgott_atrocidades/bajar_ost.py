# -*- coding: utf-8 -*-
"""Baja la BANDA SONORA OFICIAL de Elden Ring a audio/ost/ (regla del 23-oct-2026: nada de Lyria en Runa Caída).
Copia lo que ya bajaron Melina/Radahn (morgott, leyndell, mohg...) y busca lo nuevo (Margit, Godfrey); imprime canal + título
para comprobar que es la OST oficial («- Topic» o el compositor).
    python bajar_ost.py
"""
import os
import shutil
import subprocess
import sys

OST = os.path.join("audio", "ost")
M = "../er_melina_atrocidades/audio/ost/"
R = "../er_radahn_atrocidades/audio/ost/"
COPIAR = {"tema": M + "tema.wav", "mesa": M + "mesa.wav", "morgott": M + "morgott.wav", "leyndell": M + "leyndell.wav",
          "frenesi": M + "frenesi.wav", "gigante": M + "gigante.wav", "mohg": R + "mohg.wav", "rennala": R + "rennala.wav"}
FIJOS = {}
BUSCAR = {"margit": "Margit, the Fell Omen Elden Ring Original Soundtrack",
          "godfrey": "Godfrey, First Elden Lord Elden Ring Original Soundtrack"}


def bajar(nombre, url):
    sal = os.path.join(OST, nombre + ".%(ext)s")
    if os.path.isfile(os.path.join(OST, nombre + ".wav")):
        return
    subprocess.run([sys.executable, "-m", "yt_dlp", "-x", "--audio-format", "wav", "--no-playlist", "--max-downloads", "1",
                    "--print", "after_move:%(channel)s | %(title)s | %(id)s | %(duration)s", "-o", sal, url], check=False)


os.makedirs(OST, exist_ok=True)
for n, r in COPIAR.items():
    if not os.path.isfile(os.path.join(OST, n + ".wav")) and os.path.isfile(r):
        shutil.copy(r, os.path.join(OST, n + ".wav"))
for n, i in FIJOS.items():
    bajar(n, f"https://www.youtube.com/watch?v={i}")
for n, q in BUSCAR.items():
    bajar(n, f"ytsearch1:{q}")
print(sorted(os.listdir(OST)))
