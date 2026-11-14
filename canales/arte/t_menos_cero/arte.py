# -*- coding: utf-8 -*-
"""Arte del canal «T Menos Cero» (14-nov-2026), dibujado con el kit LÍNEA 3D (mismo estilo que los videos):
  BANNER_2560x1440.jpg  (zona visible en escritorio = franja central de 423 px; texto dentro de 1546x423)
  LOGO_800.jpg
  _banner_zona_segura.jpg (banner con las zonas marcadas, para revisar)
python canales/arte/t_menos_cero/arte.py
"""
import math
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "..", "nucleo"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402

import linea3d as L  # noqa: E402

STARBASE = (25.997, -97.157)


def lienzo(w, h):
    L.W, L.H = w, h
    L._vineta.cache_clear()


def guardar(lz, ruta, grano=0.0):
    im = (np.clip(lz.final(0.4, grano=grano), 0, 1) * 255).astype(np.uint8)[..., ::-1]
    cv2.imwrite(ruta, im, [cv2.IMWRITE_JPEG_QUALITY, 95])
    return im


def trayectoria(sitio):
    """Ascenso esquemático hacia el este: de la plataforma a una órbita baja (~ 200 km)."""
    s = np.linspace(0, 2600, 260)
    h = 210 * (1 - np.exp(-(s / 520) ** 1.25))
    return sitio.gran_circulo(96.0, s, h), s, h


# ------------------------------------------------------------------ banner
def banner():
    lienzo(2560, 1440)
    W, H = 2560, 1440
    sitio = L.Sitio(*STARBASE)
    # vista de costado: la cámara al sur, sobre la tangente del punto medio del ascenso, mira al norte -> la trayectoria
    # corre de izquierda a derecha sobre el limbo (alturas exageradas x3, esquema)
    T = sitio.gran_circulo(96.0, 1300, 0.0)
    Tu = L.nrm(T)
    e_t = L.nrm(sitio.gran_circulo(96.0, 1310, 0.0) - T)
    n_t = np.cross(Tu, e_t)
    pos = T - n_t * 5200 + Tu * 700
    cam = L.Cam(pos, T + Tu * 260, Tu, 34, 1.0, centro=(W / 2, H / 2 + 34))
    lz = L.L3(cam)
    L.globo(lz, np.zeros(3), L.R_T, op=1.0, paso=10, op_rej=0.15, op_costa=0.6, w=1.2, tol=0.01)
    # trayectoria con eventos
    P, s, h = trayectoria(sitio)
    P = sitio.gran_circulo(96.0, s, h * 1.3)
    lz.linea(P, 0.95, 2.0)
    lz.linea(sitio.gran_circulo(96.0, np.linspace(2600, 5200, 200), np.full(200, 273.0)), 0.5, 1.4, guion=4)
    eventos = [(280, "MAX-Q"), (720, "MECO"), (1500, "SECO")]
    for sk, nombre in eventos:
        i = int(np.argmin(abs(s - sk)))
        x, y = cam.px(P[i])
        lz.c2(x, y, 6, 1.0, lleno=True)
        lz.c2(x, y, 14, 0.55, w=1.2)
        arriba = nombre != "SECO"
        lz.texto(nombre, x, y - 30 if arriba else y + 30, 22, "SemiBold Condensed", 0.85, "mb" if arriba else "mt", esp=0.18)
    xs, ys = cam.px(sitio.P)
    lz.c2(xs, ys, 5, 1.0, lleno=True)
    lz.c2(xs, ys, 11, 0.6, w=1.0)
    lz.texto("STARBASE", xs - 26, ys - 4, 20, "Light Condensed", 0.85, "rm", esp=0.25)
    # título en la zona segura (centro 1546 x 423)
    cx, cy = W / 2, H / 2
    lz.texto("T MENOS CERO", cx, cy - 100, 132, "Bold Condensed", 1.0, "mm", esp=0.12, fondo=False)
    lz.texto("COHETES Y EXPLORACIÓN ESPACIAL  ·  EXPLICADOS EN 3D", cx, cy - 18, 34, "Light Condensed", 0.9, "mm", esp=0.28)
    # reloj de misión a los lados (dentro de la franja de escritorio)
    lz.texto("T+ 00:00:00", cx - 700, cy - 172, 26, "SemiBold Condensed", 0.75, "lm", esp=0.2)
    lz.texto("ALT 0 KM   VEL 0 KM/H", cx + 700, cy - 172, 26, "SemiBold Condensed", 0.75, "rm", esp=0.2)
    lz.l2([(cx - 700, cy - 150), (cx - 520, cy - 150)], 0.5, 1)
    lz.l2([(cx + 520, cy - 150), (cx + 700, cy - 150)], 0.5, 1)
    im = guardar(lz, os.path.join(AQUI, "BANNER_2560x1440.jpg"))
    z = im.copy()
    cv2.rectangle(z, (0, (1440 - 423) // 2), (2559, (1440 + 423) // 2), (0, 160, 255), 3)      # escritorio
    cv2.rectangle(z, ((2560 - 1546) // 2, (1440 - 423) // 2), ((2560 + 1546) // 2, (1440 + 423) // 2), (0, 255, 0), 3)
    cv2.imwrite(os.path.join(AQUI, "_banner_zona_segura.jpg"), cv2.resize(z, (1280, 720)), [cv2.IMWRITE_JPEG_QUALITY, 88])


# ------------------------------------------------------------------ logo
def logo():
    lienzo(1600, 1600)
    S = 1600
    c = S / 2
    cam = L.Cam(np.array([0, -10.0, 2.6]), np.zeros(3), (0, 0, 1), 40, 0.01)
    lz = L.L3(cam)
    # órbita inclinada (anillo 3D): mitad trasera tenue, se tapa con el texto
    eje = L.nrm(np.array([0.22, -0.35, 1.0]))
    orb = L.circulo3d(np.zeros(3), eje, 3.15, 240)
    fr = (orb @ L.nrm(cam.pos)) > 0
    lz.linea(orb, np.where(fr, 0.0, 0.45), 5.0)
    # texto T−0 (con relleno negro detrás para cortar la órbita trasera)
    lz.texto("T-0", c, c + 10, 500, "Bold Condensed", 1.0, "mm", esp=0.04, fondo=False)
    lz.linea(orb, np.where(fr, 1.0, 0.0), 7.0)
    # nave sobre la órbita (punto con halo) y estela
    k = 40
    x, y = cam.px(orb[k])
    lz.c2(x, y, 16, 1.0, lleno=True)
    lz.c2(x, y, 34, 0.5, w=2.2)
    est = orb[k - 30:k]
    lz.linea(est, np.linspace(0.0, 1.0, len(est)), 7.0)
    im = guardar(lz, os.path.join(AQUI, "_logo_1600.jpg"))
    cv2.imwrite(os.path.join(AQUI, "LOGO_800.jpg"), cv2.resize(im, (800, 800), interpolation=cv2.INTER_AREA),
                [cv2.IMWRITE_JPEG_QUALITY, 95])
    m = cv2.resize(im, (160, 160), interpolation=cv2.INTER_AREA)               # vista chica en círculo
    mask = np.zeros((160, 160), np.uint8)
    cv2.circle(mask, (80, 80), 79, 255, -1)
    prev = np.full((200, 400, 3), 40, np.uint8)
    prev[20:180, 20:180] = np.where(mask[..., None] > 0, m, 40)
    m2 = cv2.resize(im, (48, 48), interpolation=cv2.INTER_AREA)
    prev[76:124, 230:278] = m2
    cv2.imwrite(os.path.join(AQUI, "_logo_chico.jpg"), prev)
    os.remove(os.path.join(AQUI, "_logo_1600.jpg"))


if __name__ == "__main__":
    banner()
    logo()
    print("ok")
