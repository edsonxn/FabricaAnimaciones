# -*- coding: utf-8 -*-
"""Hojas de verificación de los clips ya hechos: 3 cuadros por beat (20, 50 y 80 % del beat) a 160x90, 4 beats por fila, 11 filas por hoja
(44 beats) con el número de beat impreso. Salen en medios/_escaneo/_hojas/H<k>.jpg. También mide barras negras laterales y propone el recorte
(fracción por lado que usa recorte_por: iguala x e y y luego cubre 16:9).
    python hoja_clips.py              todos los clips que existan
    python hoja_clips.py 1-44         un rango
    python hoja_clips.py --barras     solo imprime el recorte propuesto por clip
"""
import json
import os
import sys

import cv2
import numpy as np

AQ = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(AQ, "medios", "_escaneo", "_hojas")
bs = json.load(open(os.path.join(AQ, "beats.json"), encoding="utf-8"))
W, H = 160, 90


def cuadros(f, L):
    cap = cv2.VideoCapture(f)
    fps = cap.get(cv2.CAP_PROP_FPS) or 30
    dur = cap.get(cv2.CAP_PROP_FRAME_COUNT) / fps
    res = []
    for p in (.2, .5, .8):
        cap.set(cv2.CAP_PROP_POS_MSEC, min(dur - .1, L * p) * 1000)
        ok, fr = cap.read()
        res.append(fr if ok else None)
    cap.release()
    return res, dur


def barras(fr_list):
    fr = [f for f in fr_list if f is not None]
    if not fr:
        return 0
    g = np.mean([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) for f in fr], 0)
    sd = np.std([cv2.cvtColor(f, cv2.COLOR_BGR2GRAY).astype(np.float32) for f in fr], 0)
    h, w = g.shape
    col = (g.mean(0) < 10) & (sd.mean(0) < 4)
    izq = 0
    while izq < w // 3 and col[izq]:
        izq += 1
    der = 0
    while der < w // 3 and col[w - 1 - der]:
        der += 1
    return min(izq, der) / w


def main():
    solo_barras = "--barras" in sys.argv
    rng = [a for a in sys.argv[1:] if not a.startswith("--")]
    lo, hi = 1, len(bs)
    if rng:
        lo, hi = [int(x) for x in rng[0].split("-")] if "-" in rng[0] else (int(rng[0]), int(rng[0]))
    os.makedirs(OUT, exist_ok=True)
    tiles = {}
    for b in bs:
        n = int(b["id"].split("-")[1])
        if not lo <= n <= hi:
            continue
        f = os.path.join(AQ, "medios", b["id"] + ".mp4")
        if not os.path.exists(f):
            tiles[n] = [np.zeros((H, W, 3), np.uint8)] * 3
            continue
        L = b["t1"] - b["t0"]
        cs, dur = cuadros(f, L)
        bar = barras(cs)
        if solo_barras or bar > .02:
            print(f"scene-{n:03d} barras {bar:.3f}" + (" CORTO" if dur < L - .05 else ""))
        tiles[n] = [cv2.resize(c, (W, H)) if c is not None else np.zeros((H, W, 3), np.uint8) for c in cs]
    if solo_barras:
        return
    ns = sorted(tiles)
    for k in range(0, len(ns), 44):
        grupo = ns[k:k + 44]
        filas = []
        for i in range(0, len(grupo), 4):
            fila = []
            for n in grupo[i:i + 4]:
                t = np.hstack(tiles[n])
                cv2.putText(t, str(n), (3, 14), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 0, 0), 3)
                cv2.putText(t, str(n), (3, 14), cv2.FONT_HERSHEY_SIMPLEX, .5, (0, 255, 255), 1)
                fila.append(np.pad(t, ((0, 0), (0, 3), (0, 0)), constant_values=255))
            while len(fila) < 4:
                fila.append(np.zeros((H, W * 3 + 3, 3), np.uint8))
            filas.append(np.vstack([np.hstack(fila), np.full((2, W * 12 + 12, 3), 255, np.uint8)]))
        cv2.imwrite(os.path.join(OUT, f"H{grupo[0]:03d}.jpg"), np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 80])
        print("hoja", grupo[0], "-", grupo[-1])


if __name__ == "__main__":
    main()
