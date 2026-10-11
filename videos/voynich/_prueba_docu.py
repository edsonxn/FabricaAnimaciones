# -*- coding: utf-8 -*-
"""Banco de pruebas de nucleo/docu.py: genera previews/docu_prueba.jpg con varias piezas."""
import json
import os
import sys

import cv2
import numpy as np

import docu as D
from motor import H, W

os.makedirs("previews", exist_ok=True)
zipf = json.load(open("datos/zipf.json"))


def tablero_demo(t):
    lz = np.zeros((H, W, 3), np.float32)
    cam = D.Cam((1.0, 1700, 1000, 0), (1.25, 1800, 1050, -1.5), 5.0)(t)
    bg = D.tablero()
    sp_bg = D.Sprite(bg, None, sombra=False)
    D.pegar(lz, sp_bg, cam @ D.poner(bg.shape[1], bg.shape[0], 1700, 1000))
    fol = ["f004", "f024", "f110", "f136", "f175"]
    pos = [(1100, 900, -6), (1500, 1120, 4), (1900, 880, -3), (2300, 1100, 5), (2650, 900, -5)]
    pts = []
    for n, (x, y, r) in zip(fol, pos):
        p = D.polaroid(D.cargar(D.ruta_img(n), 900), 430, aspecto=1.15, foco=(0.5, 0.45))
        D.pegar(lz, p, cam @ D.poner(p.w, p.h, x, y, 1.0, r))
        pts.append((x, y - p.h / 2 + 24))
    for a, b in zip(pts[:-1], pts[1:]):
        D.hilo(lz, cam, a, b, 1.0)
    for x, y in pts:
        D.pin(lz, cam, x, y)
    pal = D.bloque_texto([[("Plantas", 0.3), ("Imposibles", 0.6)]], W / 2, H - 200, "serif", 88)
    D.dibujar_bloque(lz, pal, t, "serif", 88)
    D.tag_nombre(lz, "Wilfrid Voynich", 420, 780, t, 0.4)
    D.numero(lz, "240", 1500, 250, 190, t, 0.2, color=D.ROJO, fnt="abril")
    return D.acabado(lz, t)


def foto_demo(t):
    lz = np.zeros((H, W, 3), np.float32)
    D.foto_parallax(lz, "friedman", t, 5.0, 1.08, 1.32, (0.5, 0.42), (0.5, 0.36), par=(70, 20))
    pal = D.bloque_texto([[("William", 0.2), ("Friedman", 0.5)]], W * 0.72, H * 0.5, "serif", 96)
    D.dibujar_bloque(lz, pal, t, "serif", 96)
    D.estampa(lz, "SIN DESCIFRAR", W * 0.7, H * 0.72, t, 1.0, 80)
    return D.acabado(lz, t)


def graf_demo(t):
    lz = np.zeros((H, W, 3), np.float32)
    D.foto_parallax(lz, "f187", t, 8.0, 1.6, 1.9, (0.5, 0.4), (0.5, 0.5), par=(0, 0))
    lz *= 0.45
    D.grafica_zipf(lz, zipf, t, 0.3, W / 2, H / 2)
    return D.acabado(lz, t)


def tiempo_demo(t):
    lz = np.zeros((H, W, 3), np.float32)
    D.foto_parallax(lz, "f008", t, 8.0, 1.6, 1.9, (0.5, 0.3), (0.5, 0.4), par=(0, 0))
    lz *= 0.35
    D.linea_tiempo(lz, t, 0.2, W / 2, H / 2, 1300, 1500, 1404, 1438, marcas=[(1455, "Biblia de Gutenberg")])
    return D.acabado(lz, t)


cuadros = [tablero_demo(1.8), foto_demo(2.4), graf_demo(2.6), tiempo_demo(3.4)]
hoja = np.vstack([np.hstack(cuadros[:2]), np.hstack(cuadros[2:])])
hoja = cv2.resize(hoja, (1920, 1080), interpolation=cv2.INTER_AREA)
cv2.imwrite("previews/docu_prueba.jpg", cv2.cvtColor((hoja * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
for i, c in enumerate(cuadros):
    cv2.imwrite(f"previews/docu_prueba_{i}.jpg", cv2.cvtColor((c * 255).astype(np.uint8), cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 90])
print("ok")
