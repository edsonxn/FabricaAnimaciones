# -*- coding: utf-8 -*-
"""Hojas de contacto de las fuentes de n64_secretos (31-oct-2026; receta de mario64_secretos/escanear.py, ampliada con rango).
Sin bajar los videos: ffmpeg salta por HTTP sobre la URL de 360p y saca un cuadro por tiempo; los cuadros salen con el segundo
impreso en medios/_escaneo/<NOMBRE>_<k>.jpg (8 columnas x 6 filas de 240x135 = 48 cuadros por hoja). Anota la altura máxima
(el motor exige >= 720p) y la duración en medios/_escaneo/_alturas.txt.
    python escanear.py NOMBRE=ID,n[,t0,t1] [...]      n cuadros entre t0 y t1 (por defecto todo el video)
    python escanear.py --rango NOMBRE=ID,n,t0,t1       igual (sirve para repetir una zona con más densidad: el nombre lleva sufijo)
"""
import json
import os
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(AQUI, "medios", "_escaneo")
COLS, FILAS, W, H = 8, 6, 240, 135
FF = r"C:\ffmpeg\bin\ffmpeg.exe"


def info(vid):
    r = subprocess.run(["yt-dlp", "-j", "--no-warnings", f"https://youtu.be/{vid}"], capture_output=True, text=True,
                       encoding="utf-8", errors="replace")
    j = json.loads(r.stdout)
    vs = [f for f in j["formats"] if f.get("vcodec") not in (None, "none")]
    alt = max((f.get("height") or 0) for f in vs)
    cands = [f["url"] for f in sorted(vs, key=lambda f: ((f.get("height") or 0), f.get("protocol", "") != "https"))
             if (f.get("height") or 0) >= 340 and f.get("protocol", "") in ("https", "http", "m3u8_native")]
    url = None
    for u in cands[:6]:
        if cuadro(u, max(1, int(j["duration"] * .3))).any():
            url = u
            break
    return j["duration"], alt, url or cands[0], j.get("title", "")


def cuadro(url, t):
    r = subprocess.run([FF, "-v", "error", "-ss", str(t), "-i", url, "-frames:v", "1", "-vf", f"scale={W}:{H}",
                        "-f", "rawvideo", "-pix_fmt", "bgr24", "-"], capture_output=True, timeout=120)
    if len(r.stdout) >= W * H * 3:
        return np.frombuffer(r.stdout[:W * H * 3], np.uint8).reshape(H, W, 3).copy()
    return np.zeros((H, W, 3), np.uint8)


def hoja(nombre, vid, n, t0=None, t1=None):
    dur, alt, url, tit = info(vid)
    t0 = 0 if t0 is None else t0
    t1 = dur - 1 if t1 is None else min(t1, dur - 1)
    with open(os.path.join(SCAN, "_alturas.txt"), "a", encoding="utf-8") as fh:
        fh.write(f"{nombre}\t{vid}\t{alt}p\t{dur:.0f} s\t{tit}\n")
    tiempos = [round(t0 + (t1 - t0) * k / max(1, n - 1), 1) for k in range(n)]
    with ThreadPoolExecutor(6) as ex:
        cs = list(ex.map(lambda t: cuadro(url, t), tiempos))
    for f, t in zip(cs, tiempos):
        s = str(int(t)) if t == int(t) else f"{t:.1f}"
        cv2.putText(f, s, (4, 20), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 0, 0), 4)
        cv2.putText(f, s, (4, 20), cv2.FONT_HERSHEY_SIMPLEX, .6, (0, 255, 255), 2)
    while len(cs) % COLS:
        cs.append(np.zeros((H, W, 3), np.uint8))
    filas = [np.hstack(cs[i:i + COLS]) for i in range(0, len(cs), COLS)]
    for k in range(0, len(filas), FILAS):
        cv2.imwrite(os.path.join(SCAN, f"{nombre}_{k // FILAS + 1}.jpg"), np.vstack(filas[k:k + FILAS]),
                    [cv2.IMWRITE_JPEG_QUALITY, 78])
    print(f"{nombre}: {alt}p, {dur:.0f} s, {n} cuadros {t0:.0f}-{t1:.0f}  {tit[:50]}", flush=True)


def una(arg):
    nombre, resto = arg.split("=", 1)
    p = resto.split(",")
    vid, n = p[0], int(p[1])
    t0 = float(p[2]) if len(p) > 2 else None
    t1 = float(p[3]) if len(p) > 3 else None
    try:
        hoja(nombre, vid, n, t0, t1)
    except Exception as e:                              # noqa: BLE001
        print(f"{nombre}: ERROR {e}", flush=True)


if __name__ == "__main__":
    os.makedirs(SCAN, exist_ok=True)
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    with ThreadPoolExecutor(3) as ex:
        list(ex.map(una, args))
