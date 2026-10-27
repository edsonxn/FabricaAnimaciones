# -*- coding: utf-8 -*-
"""Prepara el terreno 3D de la Grieta del Invocador para nucleo/tactica3d (27-oct-2026).

Lee el minimapa oficial de Data Dragon (map11.png, 512 px: negro = muros, oliva = caminos, azul = río, gris azulado = bases)
y escribe en nucleo/tactica3d/assets/:
  grieta_altura.png  1024 px, gris: 0 = río, ~30 = camino, ~45 = base, 255 = cima de los muros (suavizado = taludes)
  grieta_color.png   2048 px, textura pintada: arena en los caminos, bosque en los muros, agua, losas en las bases
  arboles.json       [[u, v, escala], ...] árboles sobre los muros (InstancedMesh en el motor)
uso: python nucleo/tactica3d/preparar_grieta.py [mapa.png]   (por defecto videos/lol_worlds_2026/mapas/grieta.png)
"""
import json
import os
import sys

import cv2
import numpy as np

_D = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(_D, "assets")
SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(_D, "..", "..", "videos", "lol_worlds_2026", "mapas", "grieta.png")


def clases(img):
    """máscaras float 0..1: muro, rio, base (el resto es camino)"""
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV).astype(np.float32)
    h, s, v = hsv[..., 0], hsv[..., 1], hsv[..., 2]
    muro = (v < 45).astype(np.float32)
    rio = ((h > 88) & (h < 110) & (s > 110) & (v > 60)).astype(np.float32)
    base = ((s < 95) & (v > 70) & (h > 80) & (h < 125)).astype(np.float32) * (1 - rio)
    return muro, rio, base


def ruido(n, escala, semilla):
    r = np.random.default_rng(semilla)
    k = max(2, n // escala)
    z = r.random((k, k)).astype(np.float32)
    return cv2.resize(z, (n, n), interpolation=cv2.INTER_CUBIC)


def main():
    os.makedirs(OUT, exist_ok=True)
    img = cv2.imread(SRC, cv2.IMREAD_COLOR)
    muro, rio, base = clases(img)
    # muros limpios: sin motas
    muro = cv2.morphologyEx(muro, cv2.MORPH_OPEN, np.ones((2, 2), np.uint8))

    # ---------- altura (1024) ----------
    N = 1024
    m = cv2.resize(muro, (N, N), interpolation=cv2.INTER_LINEAR)
    r = cv2.resize(rio, (N, N), interpolation=cv2.INTER_LINEAR)
    b = cv2.resize(base, (N, N), interpolation=cv2.INTER_LINEAR)
    alt = .12 * (1 - r) + .06 * b
    alt = cv2.GaussianBlur(alt, (0, 0), 3)
    mm = cv2.GaussianBlur(m, (0, 0), 2.2)
    alt = np.maximum(alt, np.clip((mm - .25) / .5, 0, 1) * (.82 + .18 * ruido(N, 40, 3)))
    cv2.imwrite(os.path.join(OUT, "grieta_altura.png"), np.clip(alt * 255, 0, 255).astype(np.uint8))

    # ---------- color (2048) ----------
    M = 2048
    m2 = cv2.GaussianBlur(cv2.resize(muro, (M, M), interpolation=cv2.INTER_LINEAR), (0, 0), 2)
    r2 = cv2.GaussianBlur(cv2.resize(rio, (M, M), interpolation=cv2.INTER_LINEAR), (0, 0), 3)
    b2 = cv2.GaussianBlur(cv2.resize(base, (M, M), interpolation=cv2.INTER_LINEAR), (0, 0), 2)
    n1, n2, n3 = ruido(M, 24, 1), ruido(M, 90, 2), ruido(M, 8, 5)
    camino = np.dstack([0x5e + 0 * n1, 0x8e + 0 * n1, 0x93 + 0 * n1]).astype(np.float32)  # BGR caqui
    camino *= (.86 + .2 * n1 + .08 * n3)[..., None]
    camino[..., 1] += 12 * (n2 - .5)
    bosque = np.dstack([0x2a, 0x4a, 0x24]).astype(np.float32) * (.7 + .5 * n1 + .25 * n3)[..., None]
    agua = np.dstack([0xb4, 0x92, 0x22]).astype(np.float32) * (.85 + .25 * n2)[..., None]
    losa = np.dstack([0xa8, 0x9a, 0x86]).astype(np.float32) * (.88 + .12 * n1)[..., None]
    # juntas de las losas de las bases
    yy, xx = np.mgrid[0:M, 0:M]
    junta = (((xx // 64) + (yy // 64)) % 2).astype(np.float32) * .03
    losa *= (1 - junta)[..., None]
    col = camino * (1 - b2[..., None]) + losa * b2[..., None]
    col = col * (1 - r2[..., None]) + agua * r2[..., None]
    col = col * (1 - m2[..., None]) + bosque * m2[..., None]
    # borde oscuro al pie de los muros (lectura clara de los pasillos)
    borde = np.clip(cv2.GaussianBlur(m2, (0, 0), 5) - m2, 0, 1)
    col *= (1 - .55 * borde)[..., None]
    cv2.imwrite(os.path.join(OUT, "grieta_color.png"), np.clip(col, 0, 255).astype(np.uint8))

    # ---------- árboles ----------
    dist = cv2.distanceTransform((muro > .5).astype(np.uint8), cv2.DIST_L2, 3)
    rng = np.random.default_rng(7)
    arb = []
    paso = 6
    for y in range(2, 510, paso):
        for x in range(2, 510, paso):
            jx, jy = x + rng.uniform(-2.5, 2.5), y + rng.uniform(-2.5, 2.5)
            ix, iy = int(np.clip(jx, 0, 511)), int(np.clip(jy, 0, 511))
            if dist[iy, ix] >= 3:
                arb.append([round(jx / 512, 4), round(jy / 512, 4), round(float(rng.uniform(.75, 1.35)), 2)])
    json.dump(arb, open(os.path.join(OUT, "arboles.json"), "w"))
    print("altura, color y", len(arb), "árboles en", OUT)


if __name__ == "__main__":
    main()
