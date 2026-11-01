# -*- coding: utf-8 -*-
"""Muestra EN MOVIMIENTO del look (cámara que avanza: paralaje entre planos, desenfoque, hervor de líneas):
python _movimiento.py  ->  previews/muestra_look.mp4 (13 s, sin audio). Cuadros en paralelo (10 procesos)."""
import os
import subprocess
import sys
from multiprocessing import Pool

AQUI = os.path.dirname(os.path.abspath(__file__))
os.chdir(AQUI)
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))
sys.path.insert(0, AQUI)

FPS = 30
TOMAS = [  # (lámina, segundos, fotogramas clave de cámara)
    ("cementerio", 5.0, [(0.0, dict(x=-40.0, z=-60.0, guinada=2.0)), (5.0, dict(x=10.0, z=90.0, guinada=-0.5))]),
    ("danza", 4.0, [(0.0, dict(x=60.0, z=-80.0, guinada=-2.0)), (4.0, dict(x=10.0, z=90.0, guinada=0.0))]),
    ("recuerdo", 4.0, [(0.0, dict(x=-330.0, z=-560.0, guinada=15.0)), (4.0, dict(x=-265.0, z=-430.0, guinada=12.5))]),
]


def cuadro(args):
    i, nombre, t, kfs = args
    import cv2
    import numpy as np
    import look
    import grabado_3d as G3
    base = {"cementerio": look.CAM_A, "danza": look.CAM_B, "recuerdo": look.CAM_C}[nombre]
    kf = [(tk, {**base, **d}) for tk, d in kfs]
    cam = G3.kf_camara(t, kf)
    im = look.LAMINAS[nombre](t, cam=cam)
    cv2.imwrite(f"previews/mov/f_{i:04d}.jpg", (np.clip(im, 0, 1) * 255).astype(np.uint8)[..., ::-1],
                [cv2.IMWRITE_JPEG_QUALITY, 93])
    return i


if __name__ == "__main__":
    os.makedirs("previews/mov", exist_ok=True)
    tareas, i = [], 0
    for nombre, dur, kfs in TOMAS:
        for k in range(int(dur * FPS)):
            if len(sys.argv) < 2 or nombre in sys.argv[1:]:
                tareas.append((i, nombre, k / FPS, kfs))
            i += 1
    with Pool(10) as p:
        for n, _ in enumerate(p.imap_unordered(cuadro, tareas, chunksize=4)):
            if n % 60 == 0:
                print(f"{n}/{len(tareas)}", flush=True)
    subprocess.run([r"C:\ffmpeg\bin\ffmpeg.exe", "-v", "error", "-y", "-framerate", str(FPS), "-i", "previews/mov/f_%04d.jpg",
                    "-c:v", "libx264", "-crf", "18", "-pix_fmt", "yuv420p", "previews/muestra_look.mp4"], check=True)
    print("previews/muestra_look.mp4")
