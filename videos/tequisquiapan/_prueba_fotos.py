# -*- coding: utf-8 -*-
"""Prueba de FotoPeg: 3 cuadros con 2 fotos sobre un cuadro del mapa -> previews/fotos_prueba_<n>.jpg (1920x1080).
Fondo: el mapa de este video si ya carga; si no, el de historia_jalisco; si tampoco, papel liso. Un rótulo de tinta cruza el
borde de una foto para comprobar el orden de capas (la tinta debe quedar ENCIMA de la foto)."""
import os
import sys

import cv2
import numpy as np

import boceto as B
import foto_peg as FP
from motor import H, W

AQUI = os.path.dirname(os.path.abspath(__file__))
os.makedirs(os.path.join(AQUI, "previews"), exist_ok=True)


def fondo_mapa():
    try:
        import mapa as M
        M.cargar()
        M.usar("mx")
        cam = M.Cam(-102.35, 21.88, 2.6)
        img, base = M.pintar_base(cam, 0)
        if "edo_aguascalientes" in getattr(M, "CAMPOS", {}):
            M.pintar(img, cam.proyectar(M.CAMPOS["edo_aguascalientes"]), M.COL_CELDAS[0], 0.8, 0, luz=base.luz)
        M.pintar_rios(img, cam, base)
        print("fondo: mapa.py de este video")
        return np.ascontiguousarray(np.clip(img, 0, 1).astype(np.float32))
    except Exception as e:                                   # el mapa lo hace otro agente: no bloquear la prueba
        print("mapa no disponible:", repr(e)[:120])
    ruta = os.path.join(AQUI, "..", "historia_jalisco", "previews", "mapa_test.jpg")
    im = cv2.imread(ruta)
    if im is not None:
        print("fondo: cuadro de historia_jalisco/previews/mapa_test.jpg")
        t = im[540:1080, 960:1920] if im.shape[0] >= 1080 else im
        t = cv2.resize(t, (W, H), interpolation=cv2.INTER_CUBIC)
        return np.ascontiguousarray(t[..., ::-1].astype(np.float32) / 255.0)
    print("fondo: papel")
    return None


fondo = fondo_mapa()
hoja = B.Hoja()
s48 = FP.s_para(0.50)
CUADROS = [
    # (nombre, [(clave, x, y, s, u)], rótulo (texto, x, y))
    ("1", [("beso_0", 560, 860, s48, 1.0), ("convencion_9", 1340, 900, FP.s_para(0.46), 1.0)], ("Teatro Morelos", 1000, 330)),
    ("2", [("posada_3", 600, 880, FP.s_para(0.48), 1.0), ("feria_3", 1330, 930, FP.s_para(0.44), 0.55)], ("1852", 860, 250)),
    ("3", [("siglo20_3", 520, 920, FP.s_para(0.55), 1.0), ("convencion_8", 1350, 860, FP.s_para(0.42), 1.0)], ("Cristo Roto", 330, 300)),
]
for n, fotos, rot in CUADROS:
    for fase_ in (0, 1):
        hoja.limpiar()
        hoja.fondo = None if fondo is None else fondo.copy()      # pegflow compone EN el fondo: uno nuevo por cuadro, como en escenas.py
        for k, (clave, x, y, s, u) in enumerate(fotos):
            FP.F(clave).dibujar(hoja, x, y, s=s, u=u, fase_=fase_, semilla=k, tv=0.4 * fase_)
        txt, tx, ty = rot
        m = B.mascara_texto(txt, px=96)
        hoja.pegar_mascara(m, tx, ty)
        out = (np.clip(hoja.componer(), 0, 1)[..., ::-1] * 255).astype(np.uint8)
        if fase_ == 0:
            cv2.imwrite(os.path.join(AQUI, "previews", f"fotos_prueba_{n}.jpg"), out, [cv2.IMWRITE_JPEG_QUALITY, 92])
print("ok", [c[0] for c in CUADROS])
