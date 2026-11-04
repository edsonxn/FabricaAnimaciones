# -*- coding: utf-8 -*-
"""SFX DEL PROPIO JUEGO (regla del 29-oct-2026): sfx/bt_*.mp3 recortados de videos de un solo sonido.
Largos sin recortar en sfx/_bruto (voces de Banjo/Kazooie y «All Sound Effects» de ThumbsUpMaster) para sacar más si hace falta.
    python bajar_sfx.py
"""
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
S = os.path.join(AQUI, "sfx")
B = os.path.join(S, "_bruto")
CORTOS = {"bt_nota": "MYe-NHFO8v4", "bt_panal": "DUIwRc0AXQM", "bt_panal_skill": "QyccTnt74rM", "bt_jinjo": "UVUxKIL9chU",
          "bt_jiggy": "4yW4u0r9pQM", "bt_correcto": "eDoXOgrvYkY", "bt_pluma": "gUsLE35Y9nc", "bt_guhuh": "GD1dpLSvoNU"}
LARGOS = {"sfx_todos": "lUSFTbPooPI", "voces_kazooie": "IbZFoPck_iQ", "voces_banjo": "WyHNcbrtS1g", "voces_set1": "Lf-0ZmvxDtg"}


def bajar(i, base):
    subprocess.run([sys.executable, "-m", "yt_dlp", "-q", "--no-warnings", "-x", "--audio-format", "wav", "-o", base + ".%(ext)s",
                    "https://youtu.be/" + i], capture_output=True, text=True)
    time.sleep(3)


def main():
    os.makedirs(B, exist_ok=True)
    for n, i in LARGOS.items():
        if not os.path.exists(os.path.join(B, n + ".wav")):
            bajar(i, os.path.join(B, n))
            print(n, os.path.exists(os.path.join(B, n + ".wav")), flush=True)
    corte = "silenceremove=start_periods=1:start_threshold=-48dB,areverse,silenceremove=start_periods=1:start_threshold=-48dB,areverse"
    for n, i in CORTOS.items():
        wav, mp3 = os.path.join(B, n + ".wav"), os.path.join(S, n + ".mp3")
        if not os.path.exists(wav):
            bajar(i, os.path.join(B, n))
        if os.path.exists(wav):
            subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-af", corte, "-q:a", "2", mp3])
        print(n, os.path.exists(mp3), flush=True)


if __name__ == "__main__":
    main()
