# -*- coding: utf-8 -*-
"""Baja la BANDA SONORA OFICIAL de Elden Ring a audio/ost/ (regla del 23-oct-2026: nada de Lyria en Runa Caída).
Copia lo ya bajado en Messmer y busca lo nuevo para Maliketh (27-nov-2026) en canales «- Topic» / subidas «Official Soundtrack».
    python bajar_ost.py   (desde la carpeta del video)
Cada búsqueda imprime canal | título | id | duración: revisar que sea la pista oficial correcta.
"""
import os
import shutil
import subprocess
import sys

OST = os.path.join("audio", "ost")
MS = "../er_messmer_atrocidades/audio/ost/"
COPIAR = {n: MS + n + ".wav" for n in ("tema", "mesa", "mesa_velada", "final", "leyndell", "maliketh", "godfrey", "frenesi",
                                       "messmer", "sombra", "catacumbas", "enir", "umbrio", "bayle")}
FIJOS = {"farum": "DAtqGCKYbYo"}   # Crumbling Farum Azula (Shoi Miyazawa - Topic)
BUSCAR = {
          "placidusax": "Dragonlord Placidusax Elden Ring Original Soundtrack",
          "nokron": "Nokron Eternal City Elden Ring Original Soundtrack",
          "pielesdivinas": "Godskin Duo Elden Ring Original Soundtrack",
          "caelid": "Caelid Elden Ring Original Soundtrack",
          "radahn": "Starscourge Radahn Elden Ring Original Soundtrack",
          "astel": "Astel Naturalborn of the Void Elden Ring Original Soundtrack",
          "dioses_caidos": "Godfrey First Elden Lord Elden Ring Original Soundtrack",
          "morgott": "Morgott the Omen King Elden Ring Original Soundtrack",
          "sangre": "Mohg Lord of Blood Elden Ring Original Soundtrack"}


def bajar(nombre, url):
    if os.path.isfile(os.path.join(OST, nombre + ".wav")):
        return
    subprocess.run([sys.executable, "-m", "yt_dlp", "-x", "--audio-format", "wav", "--no-playlist", "--max-downloads", "1",
                    "--match-filter", "duration < 900",
                    "--print", "after_move:%(channel)s | %(title)s | %(id)s | %(duration)s",
                    "-o", os.path.join(OST, nombre + ".%(ext)s"), url], check=False)


os.makedirs(OST, exist_ok=True)
for n, r in COPIAR.items():
    if not os.path.isfile(os.path.join(OST, n + ".wav")) and os.path.isfile(r):
        shutil.copy(r, os.path.join(OST, n + ".wav"))
for n, i in FIJOS.items():
    bajar(n, "https://www.youtube.com/watch?v=" + i)
for n, q in BUSCAR.items():
    bajar(n, "ytsearch1:" + q)
print(sorted(os.listdir(OST)))
