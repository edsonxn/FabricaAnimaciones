# -*- coding: utf-8 -*-
"""Prueba del mapa: python _mapa_test.py  -> previews/mapa_test.jpg"""
import sys
import time

import cv2
import numpy as np

import boceto as B
import mapa as M


def contornos_tinta(h, S, fs, semilla=0, ancho=5.0, minimo=90):
    m = (S[::2, ::2] < 0).astype(np.uint8)
    if m.max() == 0:
        return
    cs, _ = cv2.findContours(m, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
    for k, c in enumerate(cs):
        if len(c) * 2 < minimo:
            continue
        P = cv2.approxPolyDP(c, 1.3, True).reshape(-1, 2).astype(float) * 2
        if len(P) < 4:
            continue
        P = np.vstack([P, P[:1]])
        h.trazo(P, ancho, semilla + k * 13, fs, 1.0, amp=1.6)

M.cargar()
vistas = [
    ("eu", (-3.7, 40.0, 2.3), [("iberos", (214, 140, 80)), ("celtas", (122, 150, 104))]),
    ("eu", (-4.3, 37.6, 6.0), [("castilla_1250", M.COL["castilla"]), ("granada", M.COL["granada"]), ("aragon_1250", M.COL["aragon"]), ("portugal", M.COL["portugal"])]),
    ("am", (-70.0, 5.0, 0.22), [("am_1810", M.COL["imperio"])]),
    ("eu", (-5.0, 43.1, 9.0), [("asturias_722", M.COL["asturias"]), ("andalus_718", M.COL["andalus"])]),
]
out = []
for rej, (lon, lat, z), capas in vistas:
    M.usar(rej)
    cam = M.Cam(lon, lat, z)
    t0 = time.time()
    img, base = M.pintar_base(cam, 0)
    h = B.Hoja()
    h.limpiar()
    for k, (campo, col) in enumerate(capas):
        S = cam.proyectar(M.CAMPOS[campo])
        M.pintar(img, S, col, 1.0, 0, luz=base.luz)
        contornos_tinta(h, S, 0, 3 + k, 4.0)
    M.pintar_rios(img, cam, base)
    if rej == "eu":
        M.rotulo_mapa(img, "OCÉANO ATLÁNTICO", cam, -13.0, 41.5, 40)
        M.rotulo_mapa(img, "MAR MEDITERRÁNEO", cam, 4.5, 38.6, 40)
    h.fondo = img
    o = np.clip(h.componer(), 0, 1)
    print(rej, z, f"{time.time() - t0:.3f}s")
    out.append((o * 255).astype(np.uint8)[..., ::-1])
hoja = np.vstack([np.hstack(out[:2]), np.hstack(out[2:4])])
cv2.imwrite("previews/mapa_test.jpg", cv2.resize(hoja, (1920, 1080)), [cv2.IMWRITE_JPEG_QUALITY, 90])
cv2.imwrite("previews/mapa_test_full.jpg", out[int(sys.argv[1]) if len(sys.argv) > 1 else 0], [cv2.IMWRITE_JPEG_QUALITY, 92])
