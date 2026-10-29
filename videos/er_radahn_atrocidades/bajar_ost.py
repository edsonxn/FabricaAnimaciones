# -*- coding: utf-8 -*-
"""Baja la BANDA SONORA OFICIAL de Elden Ring a audio/ost/ (regla del 23-oct-2026: nada de Lyria en Runa Caída).
Ids fijos de los canales «- Topic» ya usados en Malenia/Melina; los demás se buscan y se imprime canal + título para comprobarlos.
    python bajar_ost.py
"""
import os
import shutil
import subprocess
import sys

OST = os.path.join("audio", "ost")
FIJOS = {
    "radahn": "Z1ts4FP1WWM",       # Starscourge Radahn (Shoi Miyazawa - Topic)
    "malenia": "W3SWV8tvu18",      # Malenia, Blade of Miquella (Yuka Kitamura)
    "consorte": "OK5ObZ_vXsU",     # The Promised Consort (Shoi Miyazawa - Topic)
    "rennala": "mKOpTUezXeM",      # Rennala, Queen of the Full Moon (Yuka Kitamura)
    "mohg": "nt4wKlQ6FLM",         # Mohg, Lord of Blood (Shoi Miyazawa - Topic)
}
BUSCAR = {}                        # 28-oct: «Caelid» devolvió un ambiente de fans (tarnVHSed), no la OST: ids fijos
COPIAR = {"tema": "../er_melina_atrocidades/audio/ost/tema.wav", "mesa": "../er_melina_atrocidades/audio/ost/mesa.wav"}


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
