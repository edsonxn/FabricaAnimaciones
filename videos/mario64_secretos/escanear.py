# -*- coding: utf-8 -*-
"""Hojas de contacto de los videos fuente de mario64_secretos (29-oct-2026; copia de rare_auge_caida/escanear.py). Receta de oot_remake_cambios, pero
SIN bajar los longplays enteros (algunos duran 6 h): ffmpeg salta por HTTP al segundo pedido sobre la URL de 360p y saca un
cuadro; N cuadros repartidos entre el 6 % y el 94 % del video, con el segundo impreso, en previews/_scan/<NOMBRE>_k.jpg.
También anota la altura máxima disponible (el motor exige >= 720p) en previews/_scan/_alturas.txt.
    python escanear.py            todos
    python escanear.py SM64        solo esos
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
    "SM64": ("CRzjAKE2Zns", 540),      # Ninbanyan: Super Mario 64 Switch Online, 100 % con capítulos por nivel (1080p60)
    "SM3D": ("m9PcTN_vSVo", 60),       # Ninbanyan: Super Mario 64 en 3D All-Stars (Switch)
    # secretos (segunda tanda)
    "SHOSHIN": ("nChnAtz6RGU", 36),    # Ultra64 ARCHIVES: Shoshinkai 1995 demo build
    "SW95": ("GjgaRzI853o", 30),       # Project Space World: B-roll de Space World 1995
    "HALFA": ("X-zAWbM50JM", 30),      # pannenkoek2012: Watch for Rolling Rocks 0.5x A Presses
    "UPWARP": ("X5cwuYFUUAY", 12),     # UncommentatedPannen: TTC upwarp
    "UPW2": ("vj8DzA9y8ls", 30),       # LunaticJ: The Biggest Myth in Speedrunning History
    "BLJ": ("fDz5WfNIbJI", 30),        # Kaze Emanuar: Everything you need to know about BLJs
    "BLJH": ("gKf_bFNXuu8", 30),       # LunaticJ: The History of SM64's BLJ
    "YOSHI": ("KVnhgyZN-wE", 18),      # YTSunny: 120 estrellas, Yoshi en el tejado
    "LUIGI": ("cjJrbygzen0", 18),      # Kaze Emanuar: multijugador beta con el Luigi oficial
    "CMJP": ("FiQpaW4l1OE", 12),       # anuncio japonés 1996
    "N64ADS": ("in4X7qOUxEg", 48),     # NintendoComplete: anuncios de N64 1996-2001
    "DS": ("XAn3NQ4KSC0", 12),         # Super Mario 64 DS E3
    "DSVC": ("xqQU2RZnRjc", 12),       # Super Mario 64 DS Wii U VC launch trailer
    "AS3D": ("CPJcaGWoO2c", 24),       # Nintendo of America: 3D All-Stars announcement
    "TAS": ("9JhYbnx_h0w", 30),        # Games Done Quick: SM64 TAS de Palix, SGDQ 2026
    "WR120": ("Y1a_q2AZ9pk", 30),      # greensuigi 120 estrellas
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
    tiempos = [int(dur * (.004 + .992 * k / max(1, n - 1))) for k in range(n)]
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
