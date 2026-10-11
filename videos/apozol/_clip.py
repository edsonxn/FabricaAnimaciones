# -*- coding: utf-8 -*-
"""Renderiza un clip de prueba (sin audio) en paralelo: python _clip.py t0 t1 salida.mp4 [procs] [fps]   (fps por defecto = motor.FPS)"""
import os
import subprocess
import sys
import time
from multiprocessing import Pool

import cv2
import numpy as np

import render as R
from motor import FPS, W, H

T0, T1, SAL = float(sys.argv[1]), float(sys.argv[2]), sys.argv[3]
PROCS = int(sys.argv[4]) if len(sys.argv) > 4 else 6
FPS_C = int(sys.argv[5]) if len(sys.argv) > 5 else FPS
TAM = 30
TMP = os.path.join("previews", "_clip_tmp")


def tarea(a):
    i0, i1, ruta = a
    tmp = ruta + ".tmp.mp4"
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS_C), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20",
           "-pix_fmt", "yuv420p", "-threads", "2", tmp]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i in range(i0, i1):
        p.stdin.write(R._R.cuadro(i / FPS_C).tobytes())
    p.stdin.close()
    p.wait()
    os.replace(tmp, ruta)
    return ruta


if __name__ == "__main__":
    os.makedirs(TMP, exist_ok=True)
    n0, n1 = int(round(T0 * FPS_C)), int(round(T1 * FPS_C))
    tareas = [(i, min(i + TAM, n1), os.path.join(TMP, f"c_{i:06d}.mp4")) for i in range(n0, n1, TAM)]
    t_ini = time.time()
    with Pool(PROCS, initializer=R._init) as pool:
        for k, r in enumerate(pool.imap(tarea, tareas)):
            print(f"[{k + 1}/{len(tareas)}] {time.time() - t_ini:.0f}s", flush=True)
    with open(os.path.join(TMP, "lista.txt"), "w") as f:
        for _, _, r in tareas:
            f.write(f"file '{os.path.basename(r)}'\n")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(TMP, "lista.txt"), "-c", "copy", SAL], check=True)
    for _, _, r in tareas:
        os.remove(r)
    print("listo", SAL, f"{time.time() - t_ini:.0f}s")
