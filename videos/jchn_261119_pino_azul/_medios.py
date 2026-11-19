# -*- coding: utf-8 -*-
"""Arma medios/scene-XXX.jpg (1080x1920) recortando las fotos reales de Commons (fuente/fotos/). Recorte = (cx, cy, zoom):
centro del recorte 9:16 en fracción de la foto y cuánto se acerca (1 = el 9:16 más grande que cabe). «ventana» = la foto
entera sobre ella misma desenfocada (para no perder una vista ancha)."""
import os, sys
import cv2
import numpy as np
sys.path.insert(0, "../../nucleo")
import secuencia as S

F = "fuente/fotos/"
S2 = F + "Pinus_maximartinezii_Sierra_de_Morones_Juchipila_Zacatecas_2.jpg"
S1 = F + "Pinus_maximartinezii_Sierra_de_Morones_Juchipila_Zacatecas_1.jpg"
S3 = F + "Pinus_maximartinezii_Sierra_de_Morones_Juchipila_Zacatecas_3.jpg"
AZUL = F + "Pinus_maximartinezii.jpg"
CONO1 = F + "Pinus_maximartinezii_cone_Huazamota_Durango_Mexico_1.jpg"
CONO2 = F + "Pinus_maximartinezii_cone_Huazamota_Durango_Mexico_2.jpg"
PLAN = {
    "scene-001": (S2, (.72, .5, 1.0)),
    "scene-002": (S1, (.42, .5, 1.0)),
    "scene-003": (AZUL, (.5, .45, 1.15)),
    "scene-004": (S2, (.5, .5, 1.0)),
    "scene-005": (S3, (.48, .45, 1.0)),
    "scene-006": (S2, (.25, .55, 1.0)),
    "scene-007": (S3, (.8, .5, 1.0)),
    "scene-008": (CONO2, (.5, .5, 1.0)),
    "scene-009": (S2, (.45, .55, 1.05)),
    "scene-010": (S1, (.6, .35, 1.2)),
    "scene-011": (S1, (.3, .6, 1.25)),
    "scene-012": (S2, (.5, .5, 1.0)),
    "scene-013": (S2, (.62, .45, 1.1)),
    "scene-014": (S1, (.5, .5, 1.0)),
    "scene-015": (S1, (.5, .5, 1.0)),
    "scene-016": (S1, (.5, .5, 1.0)),
}
W, H = 1080, 1920


def recorte(im, cx, cy, z):
    ih, iw = im.shape[:2]
    if iw * H > ih * W:
        h = ih / z
        w = h * W / H
    else:
        w = iw / z
        h = w * H / W
    x0 = min(max(cx * iw - w / 2, 0), iw - w)
    y0 = min(max(cy * ih - h / 2, 0), ih - h)
    c = im[int(y0):int(y0 + h), int(x0):int(x0 + w)]
    return cv2.resize(c, (W, H), interpolation=cv2.INTER_LANCZOS4)


def ventana(im):
    fondo = cv2.GaussianBlur(recorte(im, .5, .5, 1.0), (0, 0), 28)
    fondo = (fondo * .55).astype(np.uint8)
    ih, iw = im.shape[:2]
    w = W - 60
    h = int(ih * w / iw)
    f = cv2.resize(im, (w, h), interpolation=cv2.INTER_AREA)
    y = (H - h) // 2 - 80
    fondo[y:y + h, 30:30 + w] = f
    cv2.rectangle(fondo, (28, y - 2), (30 + w + 1, y + h + 1), (230, 240, 241), 4)
    return fondo


S.dir_medios()
for b, (ruta, r) in PLAN.items():
    im = cv2.imdecode(np.fromfile(ruta, np.uint8), cv2.IMREAD_COLOR)
    out = ventana(im) if r == "ventana" else recorte(im, *r)
    cv2.imencode(".jpg", out, [cv2.IMWRITE_JPEG_QUALITY, 93])[1].tofile(os.path.join("medios", b + ".jpg"))
    print(b, os.path.basename(ruta), r)
