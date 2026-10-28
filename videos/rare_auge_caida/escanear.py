# -*- coding: utf-8 -*-
"""Hojas de contacto de los videos fuente de rare_auge_caida (28-oct-2026). Receta de oot_remake_cambios/escanear.py, pero
SIN bajar los longplays enteros (algunos duran 6 h): ffmpeg salta por HTTP al segundo pedido sobre la URL de 360p y saca un
cuadro; N cuadros repartidos entre el 6 % y el 94 % del video, con el segundo impreso, en previews/_scan/<NOMBRE>_k.jpg.
También anota la altura máxima disponible (el motor exige >= 720p) en previews/_scan/_alturas.txt.
    python escanear.py            todos
    python escanear.py DKC GE     solo esos
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(AQUI, "previews", "_scan")
COLS = 6
FF = r"C:\ffmpeg\bin\ffmpeg.exe"

# nombre: (id de YouTube, cuadros)
FUENTES = {
    "JETPAC": ("gT2KFXtg4nU", 24),     # theALFEST: Jetpac 4K (ZX Spectrum, 1983)
    "KNIGHT": ("ei6UsWr0XrU", 24),     # Knight Lore (ZX Spectrum, 1984)
    "BTOADS": ("aiaXMktO0jQ", 30),     # Kawaii Games: Battletoads NES 4K60
    "DKC": ("d4EUEsEM328", 48),        # Nintendo Longplays: Donkey Kong Country
    "KI": ("pC2OXcOx67I", 30),         # RetroGameUp: Killer Instinct SNES
    "GE": ("rxWkLdgdcPA", 48),         # Graslu00: GoldenEye 007 4K60 no damage
    "GENSO": ("iwoE9sXGd_U", 24),      # Nintendo of America: GoldenEye 007 NSO
    "BK": ("0G7V7aJHWk4", 48),         # Kawaii Games: Banjo-Kazooie 4K60
    "BKNSO": ("RWrWuXE6RHw", 24),      # Nintendo of America: Banjo-Kazooie NSO
    "PD": ("vcqbMXllyb0", 48),         # Graslu00: Perfect Dark sin HUD 4K60
    "CONKER": ("TlkMXV1Eagw", 48),     # Game Master TV: Conker's Bad Fur Day 1080p60
    "DK64": ("agg2K8K2qc0", 48),       # Ninbanyan: Donkey Kong 64
    "DKR": ("3gPXyMK4Lls", 36),        # World of Longplays: Diddy Kong Racing
    "JFG": ("MIgQ9NFJtzU", 24),        # Nintendo of America: NSO diciembre 2023 (Jet Force Gemini)
    "SFA": ("I-6XzVNLKDY", 48),        # Loopy Longplays: Star Fox Adventures
    "GHOUL": ("JrKO4Ky-k2o", 36),      # WishingTikal: Grabbed by the Ghoulies
    "KAMEO": ("U3mPs0WmTYs", 18),      # IGN: Kameo E3 trailer
    "PDZ": ("7lM5kZKnnzM", 18),        # IGN: Perfect Dark Zero cinematic trailer
    "VIVA": ("7_WtivSGCJA", 18),       # Viva Piñata trailer HD
    "NB": ("QLWLdO9GLWM", 18),         # IGN: Nuts & Bolts first trailer
    "KINECT": ("n8wM1aTsl7s", 18),     # XBOX: Kinect Sports Experience
    "REPLAY": ("AaieVt3M72c", 24),     # XBOX: Rare Replay E3 announce trailer
    "OPENING": ("iYbU1uKPaGU", 24),    # Rare Ltd: Rare Replay Opening Number
    "SOT": ("gl3UiHp0sz0", 24),        # Rare Ltd: Sea of Thieves E3 2016 cinematic
    "SOTL": ("r5JIBaasuE8", 24),       # Sea of Thieves: launch gameplay trailer
    "SOTPS5": ("xKLpWOEEUxc", 24),     # PlayStation: Sea of Thieves PS5 launch trailer
    "EVER": ("jWpcUH-tKEU", 24),       # XBOX: Everwild X019 announce trailer
    "EVER2": ("WSWnnQMSPjc", 24),      # XBOX: Everwild Eternals trailer
    "YOOKA": ("oqmF8IgxtJ0", 24),      # Playtonic: Yooka-Laylee Gamescom 2016
    "TS2": ("oJwvhPUbRuA", 30),        # TimeSplitters 2 no commentary
    "NBL": ("zA2uitj9w-E", 24),       # LongplayArchive: Nuts & Bolts
    # segunda tanda (lo que faltaba para el guion)
    "ATIC": ("Z8M4HJTRWqY", 18),       # RetroSpect: Atic Atac
    "SABRE": ("lt4FqqLW8LI", 18),      # Sabre Wulf 100 %
    "RCPRO": ("EA-430ZNqZg", 18),      # NintendoComplete: R.C. Pro-Am
    "SNAKE": ("r1aFoGEWHFA", 18),      # World of Longplays: Snake Rattle 'n Roll
    "DKC2": ("VgTt5fceVTE", 24),       # Nintendo Longplays: DKC 2
    "DKC3": ("HlI65icA8CM", 18),       # Nintendo Longplays: DKC 3
    "BLAST": ("9icL00n7i2U", 18),      # WishingTikal: Blast Corps 4K
    "JFGL": ("vak_weTcVNo", 30),       # LongplayArchive: Jet Force Gemini HD
    "VIVAG": ("ExxSfoXMUAA", 24),      # Viva Piñata gameplay
    "AVATAR": ("HCnTvcrQhwU", 18),     # IGN: creando avatares en la NXE
    "BT": ("Vjxl_yCvc1o", 36),         # Ninbanyan: Banjo-Tooie NSO
    "SGI": ("ZDxLa6P6exc", 24),        # LGR: SGI Indigo2 (máquina)
    "SGI2": ("Bo3lUw9GUJA", 24),       # Dodoid: SGI Onyx de 1993
    "REPLAY2": ("F5y_fcMOvZM", 24),    # Rare Ltd: tráiler de Rare Replay E3 2015
    "DREAM": ("w72kj20YNA0", 30),      # Rare Ltd: Rare Revealed, Dream
    "PDMK": ("7CxpdspOV5I", 30),       # Rare Ltd: Rare Revealed, Perfect Dark
    "NBREV": ("_R2sCzlT5Uc", 30),      # Rare Ltd: Rare Revealed, Nuts & Bolts
    "VIVAREV": ("Sk4b4L8Da10", 24),    # Rare Ltd: Rare Revealed, Viva Piñata
    "KINECT2": ("1xdUV3kbXWw", 24),    # Rare Ltd: Kinect Sports E3 2010
    "KAMEOL": ("fAuDjRjIlB8", 30),     # Loopy Longplays: Kameo 720p
    "SFA2": ("GHYIxHYxNOU", 36),       # LongPlaySonic: Star Fox Adventures 1440p
    "DKCDOC": ("TwWHzilbQ34", 36),     # Boundary Break: documental de DKC (25 años)
}


def info(vid):
    r = subprocess.run(["yt-dlp", "-j", "--no-warnings", f"https://youtu.be/{vid}"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    j = json.loads(r.stdout)
    alt = max((f.get("height") or 0) for f in j["formats"] if f.get("vcodec") not in (None, "none"))
    url = None
    for f in sorted(j["formats"], key=lambda f: (f.get("height") or 0)):
        if f.get("vcodec") not in (None, "none") and (f.get("height") or 0) >= 340 and f.get("protocol", "").startswith("http"):
            url = f["url"]
            break
    return j["duration"], alt, url, j.get("title", "")


def cuadro(url, t):
    r = subprocess.run([FF, "-v", "error", "-ss", str(t), "-i", url, "-frames:v", "1", "-vf", "scale=320:180",
                        "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, timeout=90)
    if len(r.stdout) >= 320 * 180 * 3:
        return np.frombuffer(r.stdout[:320 * 180 * 3], np.uint8).reshape(180, 320, 3).copy()
    return np.zeros((180, 320, 3), np.uint8)


def hoja(nombre, vid, n):
    dur, alt, url, tit = info(vid)
    with open(os.path.join(SCAN, "_alturas.txt"), "a", encoding="utf-8") as fh:
        fh.write(f"{nombre}\t{vid}\t{alt}p\t{dur:.0f} s\t{tit}\n")
    tiempos = [int(dur * (.06 + .88 * k / max(1, n - 1))) for k in range(n)]
    with ThreadPoolExecutor(6) as ex:
        cs = list(ex.map(lambda t: cuadro(url, t), tiempos))
    for f, t in zip(cs, tiempos):
        cv2.putText(f, str(t), (6, 24), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 0), 4)
        cv2.putText(f, str(t), (6, 24), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)
    while len(cs) % COLS:
        cs.append(np.zeros((180, 320, 3), np.uint8))
    filas = [np.hstack(cs[i:i + COLS]) for i in range(0, len(cs), COLS)]
    por = 6                                             # 6 filas por hoja
    for k in range(0, len(filas), por):
        cv2.imwrite(os.path.join(SCAN, f"{nombre}_{k // por + 1}.jpg"), np.vstack(filas[k:k + por]),
                    [cv2.IMWRITE_JPEG_QUALITY, 80])
    print(f"{nombre}: {alt}p, {dur:.0f} s, {n} cuadros  {tit[:60]}", flush=True)


if __name__ == "__main__":
    os.makedirs(SCAN, exist_ok=True)
    for nom in (sys.argv[1:] or list(FUENTES)):
        vid, n = FUENTES[nom]
        try:
            hoja(nom, vid, n)
        except Exception as e:                          # noqa: BLE001
            print(f"{nom}: ERROR {e}", flush=True)
