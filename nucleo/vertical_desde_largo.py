# -*- coding: utf-8 -*-
"""Short vertical DERIVADO de un video largo de secuencia (21-oct-2026, Shorts de Cuerpo en Neón).

Reencuadra a 1080x1920 las imágenes 16:9 del largo (las originales de Flow, 1376x768) para cada beat del Short:
recorte horizontal centrado en lo que importa + fundido a negro arriba y abajo. Pensado para estilos de fondo negro
(línea blanca + neón), donde la banda de imagen se funde con el negro sin que se note el borde.

Uso desde videos/<short>/medios_del_largo.py:
    MAPA = {"scene-001": ("scene-012", .40, .50), ...}     # beat del Short: (medio del largo, ancho visible, foco x)
    MAPA = {"scene-006": ("scene-018", .26, .50, .55)}     # 4.º valor opcional: foco y (si la imagen llena el alto)
    import vertical_desde_largo as vl; vl.armar("freno_enojo", MAPA)
- ancho visible = qué fracción del ancho del original entra en los 1080 px (.32 llena todo el alto; .45 deja una banda
  de ~1340 px; < .30 amplía más de 2,6x y se nota). foco x/y = 0..1 sobre el original.
- La banda va centrada en `CY` (.56: deja arriba ~1/5 de negro para las palabras clave, por encima de la interfaz de Shorts).
"""
import json
import os
import sys

import cv2
import numpy as np

W, H = 1080, 1920
CY = .56
PLUMA = .16          # fracción de la banda que se funde a negro arriba y abajo


def _medio(carpeta_largo, mid):
    p = os.path.join(carpeta_largo, "medios", mid + ".jpg")
    im = cv2.imread(p)
    if im is None:
        raise SystemExit(f"no existe o no es imagen: {p}")
    return im


def vertical(im, ancho, fx=.5, fy=.5, cy=CY):
    h0, w0 = im.shape[:2]
    s = W / (ancho * w0)
    im = cv2.resize(im, (int(round(w0 * s)), int(round(h0 * s))), interpolation=cv2.INTER_LANCZOS4)
    if s > 1.2:                                          # nitidez tras ampliar (línea fina sobre negro)
        im = cv2.addWeighted(im, 1.45, cv2.GaussianBlur(im, (0, 0), 1.6), -.45, 0)
    h2, w2 = im.shape[:2]
    x0 = int(np.clip(fx * w2 - W / 2, 0, w2 - W))
    im = im[:, x0:x0 + W]
    if h2 >= H:
        y0 = int(np.clip(fy * h2 - H / 2, 0, h2 - H))
        return im[y0:y0 + H]
    k = np.ones(h2, np.float32)
    n = max(1, int(h2 * PLUMA))
    r = np.linspace(0, 1, n, dtype=np.float32)
    r = r * r * (3 - 2 * r)
    k[:n], k[-n:] = r, r[::-1]
    lienzo = np.zeros((H, W, 3), np.uint8)
    y = int(np.clip(cy * H - h2 / 2, 0, H - h2))
    lienzo[y:y + h2] = (im.astype(np.float32) * k[:, None, None]).astype(np.uint8)
    return lienzo


def armar(largo, mapa, carpeta="."):
    """Escribe medios/<beat>.jpg para cada beat de beats.json según `mapa`; avisa de los beats sin medio."""
    carpeta_largo = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "videos", largo)
    beats = json.load(open(os.path.join(carpeta, "beats.json"), encoding="utf-8"))
    os.makedirs(os.path.join(carpeta, "medios"), exist_ok=True)
    faltan = [b["id"] for b in beats if b["id"] not in mapa]
    for bid, v in mapa.items():
        mid, ancho, fx = v[:3]
        fy = v[3] if len(v) > 3 else .5
        cv2.imwrite(os.path.join(carpeta, "medios", bid + ".jpg"), vertical(_medio(carpeta_largo, mid), ancho, fx, fy),
                    [cv2.IMWRITE_JPEG_QUALITY, 95])
    print(f"{len(mapa)} medios verticales desde {largo}" + (f" · SIN MEDIO: {faltan}" if faltan else ""))


def hoja(carpeta=".", salida="previews/medios_vertical.jpg", cols=7):
    """Hoja de los medios ya armados (cada uno a 216x384, con su número) para revisarlos de un vistazo."""
    ps = sorted(f for f in os.listdir(os.path.join(carpeta, "medios")) if f.endswith(".jpg"))
    cw, ch = 216, 384
    celdas = []
    for f in ps:
        im = cv2.resize(cv2.imread(os.path.join(carpeta, "medios", f)), (cw, ch), interpolation=cv2.INTER_AREA)
        cv2.rectangle(im, (0, 0), (cw - 1, ch - 1), (60, 60, 60), 1)
        cv2.putText(im, f[6:9], (6, 24), cv2.FONT_HERSHEY_SIMPLEX, .7, (0, 0, 255), 2)
        celdas.append(im)
    while len(celdas) % cols:
        celdas.append(np.zeros((ch, cw, 3), np.uint8))
    filas = [np.hstack(celdas[i:i + cols]) for i in range(0, len(celdas), cols)]
    os.makedirs(os.path.dirname(os.path.join(carpeta, salida)), exist_ok=True)
    cv2.imwrite(os.path.join(carpeta, salida), np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 80])
    print("hoja:", salida)


if __name__ == "__main__":
    hoja(*(sys.argv[1:2] or ["."]))
