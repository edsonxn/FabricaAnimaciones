# -*- coding: utf-8 -*-
"""Baja la BANDA SONORA OFICIAL de Elden Ring / Shadow of the Erdtree a audio/ost/ (regla del 23-oct-2026: nada de Lyria en Runa Caída).
Copia lo ya bajado en Rykard y baja lo nuevo del DLC por id (canales «- Topic»; si no hay Topic, la subida «Official Soundtrack» de Qiuvox;
buscado el 24-nov-2026).
    python bajar_ost.py   (desde la carpeta del video)
"""
import os
import shutil
import subprocess
import sys

OST = os.path.join("audio", "ost")
RK = "../er_rykard_atrocidades/audio/ost/"
COPIAR = {n: RK + n + ".wav" for n in ("tema", "mesa", "mesa_velada", "final", "leyndell", "maliketh", "godfrey", "frenesi")}
FIJOS = {"messmer": "jsOsinZVKqk",     # Messmer, the Impaler (Release - Topic)
         "sombra": "elHD7EHGBkw",      # Shadow Keep (Qiuvox, OST oficial)
         "belurat": "DYViU7PHOq4",     # Belurat, Tower Settlement (Shoi Miyazawa - Topic)
         "enir": "nmr8lo4xOdY",        # Enir-Ilim (Qiuvox, OST oficial)
         "catacumbas": "5_9QTQGStaQ",  # Catacombs of the Shadow Realm (Qiuvox, OST oficial)
         "rauh": "itITwa-DaoA",        # Ancient Ruins of Rauh (Qiuvox, OST oficial)
         "chaman": "RoV-zvZhBM0",      # Shaman Village (OST oficial)
         "consorte": "OK5ObZ_vXsU",    # The Promised Consort (Shoi Miyazawa - Topic)
         "leon": "1Saywp-mXxo",        # Divine Beast Dancing Lion (Shoi Miyazawa - Topic)
         "rellana": "1OlnZqnSDow",     # The Twin Moon Knight (Release - Topic)
         "bayle": "Tz8nN-7MPR8",       # Bayle the Dread (Release - Topic)
         "romina": "zxpKOijOGOo",      # The Saint of the Bud (Release - Topic)
         "umbrio": "KaTQO6tZlRg",      # The Scadutree Avatar (Release - Topic)
         "putrefacto": "zl5eLkeJL0M"}  # The Putrescent Knight (Release - Topic)


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
