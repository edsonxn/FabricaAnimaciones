# -*- coding: utf-8 -*-
"""Base de spyro2 (30-oct-2026): OST oficial del juego por pistas y SFX del propio juego.
    python preparar_base.py ost        audio/ost/<NN>_<pista>.wav (ripeo de 44 pistas de GnC Films, cortado por sus marcas)
    python preparar_base.py sfx        sfx/sp_*.mp3 recortados de videos de un solo sonido (canal Myles Moss)
"""
import os
import re
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
OST_ID = "mFtiP6YwxYQ"
MARCAS = """00:00:00 Gateway To Glimmer|00:03:28 Summer Forest|00:06:05 Idol Springs|00:09:45 Hula Girl Rescue|00:10:06 Colossus|00:13:50 Hockey
00:15:53 Hurricos|00:19:08 Sunny Beach|00:21:54 Aquaria Towers|00:24:41 Ocean Speedway|00:26:52 Crush's Dungeon|00:29:02 Autumn Plains
00:31:39 Skelos Badlands|00:34:07 Lava Lizards I|00:34:44 Lava Lizards II|00:35:33 Dem Bones|00:36:02 Ice Wizards|00:37:24 Crystal Glacier
00:40:52 Breeze Harbor|00:44:06 Gear Grab|00:47:04 Zephyr|00:50:53 Scorch|00:54:21 Bronze Flute|00:54:34 Magma Cone|00:58:06 Crystal Geysers
00:59:27 Shady Oasis|01:03:28 Metro Speedway|01:06:02 Icy Speedway|01:08:26 Gulp's Overlook|01:11:19 Winter Tundra|01:13:55 Mystic Marsh
01:17:46 Cloud Temples|01:20:57 Agent Zero's Secret Hideout|01:22:59 Robotica Farms|01:26:48 Metropolis|01:30:29 Canyon Speedway
01:33:29 Ripto's Arena|01:35:46 Dragon Shores|01:39:40 End Credits|01:43:52 Sunny Beach (demo)|01:45:42 Skelos Badlands (demo)
01:47:33 Bronze Flute (alternate)|01:47:50 Ripto's Arena (alternate)|01:50:07 Demo Cue"""
SFX = {"sp_menu": "OMt7xWuWhK4", "sp_logo": "tsVXto5HRvE", "sp_8piezas": "GDySE_dz-MA", "sp_tiempo_mas": "GZMpBnBel_U", "sp_tiempo_fin": "tBS0qyDfKww",
       "sp_portal": "wVRtEbYVc8w", "sp_portal_activo": "-ATWeDwv6YI", "sp_carga": "mzYS1bunhGU", "sp_buceo": "E4FqyiTlB3w", "sp_lava": "9F0DrMgKJEY",
       "sp_ahogo": "s45MXEW3BMw", "sp_moneybags": "56nLG7qSIFE", "sp_muro": "om2O2JRJYW8", "sp_vasija": "6tXG3ay7pCs", "sp_lamparas": "6U14Zn889hk",
       "sp_agente0": "tgeG80ke5D0", "sp_ripto": "Z231q9FgK3g", "sp_crush": "00AX7KE1vUw", "sp_crush_mazo": "5fw--PvPGcI", "sp_gulp": "GSCkbH-0u2U",
       "sp_gulp_trago": "si0zyNNniC8", "sp_estatua": "K1rHeL2bOhs", "sp_templo": "UhKOIJJ5k3M", "sp_puno": "bWqCRt5WdJI", "sp_ladron": "HIQKDKMFHuA",
       "sp_oveja": "XfbS-rDwuUA", "sp_yeti": "XgQJTQWq-DY", "sp_cowlek": "eI6PQUfuSFI", "sp_camello": "USrgdxnrWU0", "sp_elefante": "tMlT576FTQA",
       "sp_vagoneta": "IJecTI_IuBg", "sp_rocas": "girzljDv_qE", "sp_publico": "e1qcNrt8nuQ", "sp_pterodactilo": "yDK6S2nJ-Cg", "sp_arcos": "Z1mGVYsCksQ"}


def bajar(i, base):
    subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "--no-warnings", "-x", "--audio-format", "wav", "-o", base + ".%(ext)s",
                    "https://youtu.be/" + i], capture_output=True, text=True)
    time.sleep(3)


def seg(h):
    a, b, c = h.split(":")
    return int(a) * 3600 + int(b) * 60 + int(c)


def ost():
    d = os.path.join(AQUI, "audio", "ost")
    os.makedirs(d, exist_ok=True)
    todo = os.path.join(d, "_completa.wav")
    if not os.path.exists(todo):
        bajar(OST_ID, os.path.join(d, "_completa"))
    marcas = [m.strip().split(" ", 1) for m in re.split(r"[|\n]", MARCAS) if m.strip()]
    for n, (h, nombre) in enumerate(marcas):
        fin = ["-to", str(seg(marcas[n + 1][0]))] if n + 1 < len(marcas) else []
        limpio = re.sub(r"[^a-z0-9]+", "_", nombre.lower()).strip("_")
        sal = os.path.join(d, f"{n + 1:02d}_{limpio}.wav")
        if not os.path.exists(sal):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", todo, "-ss", str(seg(h)), *fin, "-c", "copy", sal])
        print(os.path.basename(sal), os.path.exists(sal), flush=True)


def sfx():
    s, b = os.path.join(AQUI, "sfx"), os.path.join(AQUI, "sfx", "_bruto")
    os.makedirs(b, exist_ok=True)
    corte = "silenceremove=start_periods=1:start_threshold=-48dB,areverse,silenceremove=start_periods=1:start_threshold=-48dB,areverse"
    for n, i in SFX.items():
        wav, mp3 = os.path.join(b, n + ".wav"), os.path.join(s, n + ".mp3")
        if not os.path.exists(wav):
            bajar(i, os.path.join(b, n))
        if os.path.exists(wav):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", corte, "-q:a", "2", mp3])
        print(n, os.path.exists(mp3), flush=True)


if __name__ == "__main__":
    {"ost": ost, "sfx": sfx}[sys.argv[1]]()
