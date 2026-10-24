# -*- coding: utf-8 -*-
"""Hojas de contacto propias de las partes de ZeldaCentral (majora_mask, 23-oct-2026): baja cada parte a 360p en
previews/_scan/ y escribe previews/_scan/PNN_k.jpg con un cuadro cada PASO s y el segundo impreso (para el plan de clips).
    python escanear.py 1 2 3 10        (números de parte de mapa_clips.md)
"""
import os
import re
import subprocess
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(AQUI, "previews", "_scan")
PASO = 15
COLS, FILAS = 6, 6


def partes():
    txt = open(os.path.join(AQUI, "mapa_clips.md"), encoding="utf-8").read()
    return {int(n): i for n, i in re.findall(r"P(\d\d) (\S{11}) ", txt)}


def bajar(n, vid):
    out = os.path.join(SCAN, f"P{n:02d}.mp4")
    if not os.path.exists(out):
        subprocess.run(["yt-dlp", "-q", "-f", "bv*[height<=360][ext=mp4]/bv*[height<=360]", "-o", out,
                        f"https://youtu.be/{vid}"], check=False)
    return out


def hoja(n, ruta):
    cap = cv2.VideoCapture(ruta)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    tiempos = list(range(3, int(total), PASO))
    por = COLS * FILAS
    for k in range(0, len(tiempos), por):
        celdas = []
        for t in tiempos[k:k + por]:
            cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
            ok, f = cap.read()
            f = cv2.resize(f if ok else np.zeros((360, 640, 3), np.uint8), (320, 180))
            cv2.putText(f, str(t), (6, 24), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 0, 0), 4)
            cv2.putText(f, str(t), (6, 24), cv2.FONT_HERSHEY_SIMPLEX, .8, (0, 255, 255), 2)
            celdas.append(f)
        while len(celdas) % COLS:
            celdas.append(np.zeros((180, 320, 3), np.uint8))
        filas = [np.hstack(celdas[i:i + COLS]) for i in range(0, len(celdas), COLS)]
        cv2.imwrite(os.path.join(SCAN, f"P{n:02d}_{k // por + 1}.jpg"), np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 80])
    print(f"P{n:02d}: {total:.0f} s, {len(tiempos)} cuadros")


if __name__ == "__main__":
    os.makedirs(SCAN, exist_ok=True)
    P = partes()
    for a in sys.argv[1:]:
        n = int(a)
        hoja(n, bajar(n, P[n]))
