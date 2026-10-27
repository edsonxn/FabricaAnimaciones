# -*- coding: utf-8 -*-
"""Hojas de contacto propias de los videos fuente (oot_remake_cambios, 26-oct-2026; receta de majora_mask/escanear.py):
baja cada video a 360p en previews/_scan/ y escribe previews/_scan/<NOMBRE>_k.jpg con un cuadro cada PASO s y el segundo
impreso, para el plan de clips por beat.
    python escanear.py            todos los de FUENTES
    python escanear.py DEMO OVR   solo esos
"""
import os
import subprocess
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
SCAN = os.path.join(AQUI, "previews", "_scan")
COLS, FILAS = 6, 6

# nombre: (id de YouTube, paso en s)
FUENTES = {
    "DEMO": ("PQvD3p2yGwc", 6),   # Nintendo of America: Mr. Aonuma Gameplay Demonstration (15:10, 4K)
    "OVR": ("8v8eDMh1o3g", 3),    # Nintendo of America: Overview Trailer (4:44)
    "DIR": ("wuFfiTEr2yc", 3),    # Nintendo of America: tráiler del 40th Anniversary Direct 9.8.2026 (3:26)
    "JUN": ("r8eMoxo4ipE", 3),    # Nintendo of America: anuncio del Nintendo Direct 6.9.2026 (1:38)
    "NLIFE": ("w6tbCJLj8eE", 10),  # Nintendo Life: BRAND NEW Ocarina of Time Switch 2 Gameplay (22:40)
}


def bajar(nombre, vid):
    out = os.path.join(SCAN, f"{nombre}.mp4")
    if not os.path.exists(out):
        subprocess.run(["yt-dlp", "-q", "-f", "bv*[height<=360][ext=mp4]/bv*[height<=360]", "-o", out,
                        f"https://youtu.be/{vid}"], check=False)
    return out


def hoja(nombre, ruta, paso):
    cap = cv2.VideoCapture(ruta)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    total = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    tiempos = list(range(1, int(total), paso))
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
        cv2.imwrite(os.path.join(SCAN, f"{nombre}_{k // por + 1}.jpg"), np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 80])
    print(f"{nombre}: {total:.0f} s, {len(tiempos)} cuadros", flush=True)


if __name__ == "__main__":
    os.makedirs(SCAN, exist_ok=True)
    for n in (sys.argv[1:] or list(FUENTES)):
        vid, paso = FUENTES[n]
        hoja(n, bajar(n, vid), paso)
