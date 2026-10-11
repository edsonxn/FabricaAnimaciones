# -*- coding: utf-8 -*-
"""Genera los recortes de retratos reales de nucleo/datos/retratos/ a partir de los candidatos descargados de Wikimedia Commons.
Uso: python preparar_retratos.py   (lee videos/independencia_mx/retratos/_config.py y retratos/cand/*.jpg)"""
import os, sys
import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
V = os.path.join(AQUI, "..", "videos", "independencia_mx", "retratos")
sys.path.insert(0, V)
from _config import R

SAL = os.path.join(AQUI, "datos", "retratos")
os.makedirs(SAL, exist_ok=True)
PW, PH = 448, 560


def recorte(im, cara, alto_rel, ancho_rel, cy_rel, salida, dx=0.0):
    H, W = im.shape[:2]
    x, y, w, h = cara
    cx, cy = x + w / 2 + dx * h, y + h / 2
    ch = h * alto_rel
    cw = ch * ancho_rel
    x0, y0 = cx - cw / 2, cy - cy_rel * ch
    M = np.float32([[salida[0] / cw, 0, -x0 * salida[0] / cw], [0, salida[1] / ch, -y0 * salida[1] / ch]])
    return cv2.warpAffine(im, M, salida, flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


lineas = ["# Créditos de los retratos (dominio público, Wikimedia Commons)\n",
          "Pinturas, grabados y fotografías antiguas (siglos XVIII-XX) de dominio público. Recortados, suavizados y coloreados al estilo del video.\n"]
for k, d in R.items():
    im = cv2.imread(os.path.join(V, "cand", d["f"] + ".jpg"))
    cy_rel = d.get("cy", 0.40)
    cv2.imwrite(os.path.join(SAL, f"{k}.jpg"), recorte(im, d["cara"], d.get("alto", 3.0), 0.8, cy_rel, (PW, PH), d.get("dx", 0.0)), [cv2.IMWRITE_JPEG_QUALITY, 92])
    cv2.imwrite(os.path.join(SAL, f"{k}_m.jpg"), recorte(im, d["cara"], d.get("alto_m", 2.15), 1.0, 0.47, (400, 400), d.get("dx", 0.0)), [cv2.IMWRITE_JPEG_QUALITY, 92])
    lineas.append(f"- {k}: «{d['fuente']}» (https://commons.wikimedia.org/wiki/File:{d['fuente'].replace(' ', '_')})\n")
open(os.path.join(SAL, "CREDITOS.md"), "w", encoding="utf-8").writelines(lineas)
print("listo", len(R))
