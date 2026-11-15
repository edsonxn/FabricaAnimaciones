# -*- coding: utf-8 -*-
"""Piezas comunes de «Starship sin patas» (kit LÍNEA 3D): anclas a la voz, reloj de misión, HUD con los 33 + 6 motores,
lector de clips de la retransmisión de SpaceX con capas encima, geografía de Starbase (OSM) y trayectorias ESQUEMÁTICAS.
Mundo en KM con el centro de la Tierra en el origen; los cohetes en metros × M."""
import json
import math
import os
import re
import sys

import cv2
import numpy as np

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(AQUI, "..", "..", "nucleo"))

import linea3d_starship as S  # noqa: E402,F401
from linea3d import (L3, R_T, TINTE, Cam, Sitio, base_de, chorro, circulo3d, clamp, cuerpo_revolucion, curva_suave,  # noqa: E402,F401
                     e_inout, e_out, etiqueta3d, globo, latlon_xyz, lerp, nrm, pr, rejilla_suelo, rnd, smooth, ancho_texto)
from motor import H, W  # noqa: E402

TL = json.load(open(os.path.join(AQUI, "timeline.json"), encoding="utf-8"))
TOTAL = TL["total"]
ESC = {e["id"]: e for e in TL["escenas"]}
M = 0.001


def _norm(s):
    s = s.lower()
    for a, b in zip("áéíóúü", "aeiouu"):
        s = s.replace(a, b)
    return re.sub(r"[^a-zñ0-9]", "", s)


def ww(esc, frase, palabra, n=0, fin=False):
    obj = [_norm(x) for x in palabra.split()]
    ws = ESC[esc]["frases"][frase]["words"]
    nw = [_norm(x["w"]) for x in ws]
    hits = [ws[i + len(obj) - 1]["e"] if fin else ws[i]["s"]
            for i in range(len(ws) - len(obj) + 1) if all(nw[i + j].startswith(obj[j]) for j in range(len(obj)))]
    if len(hits) <= n:
        raise KeyError(f"[{esc}:{frase}] no está '{palabra}' en {[x['w'] for x in ws]}")
    return hits[n]


def T0(esc):
    return ESC[esc]["t0"]


def T1(esc):
    return ESC[esc]["t1"]


def F0(esc, i):
    return ESC[esc]["frases"][i]["words"][0]["s"]


def F1(esc, i):
    return ESC[esc]["frases"][i]["words"][-1]["e"]


def ap(t, a, d=0.35):
    """Aparece en a (fundido de d s)."""
    return smooth(pr(t, a, a + d))


def vent(t, a, b, d=0.35):
    """Visible entre a y b con fundidos."""
    return smooth(pr(t, a, a + d)) * (1 - smooth(pr(t, b - d, b)))


# ------------------------------------------------------------------ video real (retransmisión de SpaceX)
CLIPS = {k: f"clips/{k}.mp4" for k in ("f5", "f6", "f7", "f8", "f11", "nolanding", "f9landed", "crs8", "orbcomm", "sn10", "sn10b", "sn15", "cnn")}
CLIPS["reg"] = "../starship_vuelo15/clips/regreso_full.mp4"
CLIPS["lanz"] = "../starship_vuelo15/clips/lanz_a.mp4"
CREDITO = {"f5": "SPACEX", "f6": "SPACEX", "f7": "SPACEX", "f8": "SPACEX VÍA VIDEOFROMSPACE", "f11": "SPACEX VÍA VIDEOFROMSPACE",
           "nolanding": "SPACEX", "f9landed": "SPACEX", "crs8": "SPACEX", "orbcomm": "SPACEX", "sn10": "SPACEX",
           "sn10b": "SPACE.COM / SPADRE", "sn15": "SPACEX", "cnn": "CNN · SPACEX", "reg": "SPACEX VÍA VIDEOFROMSPACE",
           "lanz": "SPACEX VÍA VIDEOFROMSPACE"}
_CAP = {}


def frame_clip(nombre, seg):
    """Cuadro RGB float32 0..1 a 1920x1080 del clip en el segundo `seg` (lectura secuencial con caché)."""
    if nombre not in _CAP:
        while len(_CAP) >= 2:                       # máx. 2 lectores abiertos por proceso (memoria)
            viejo = next(iter(_CAP))
            _CAP.pop(viejo)[0].release()
        cap = cv2.VideoCapture(os.path.join(AQUI, CLIPS[nombre]))
        _CAP[nombre] = [cap, cap.get(cv2.CAP_PROP_FPS) or 30.0, -10, None]
    c = _CAP[nombre]
    idx = max(0, int(round(seg * c[1])))
    if idx != c[2]:
        if not (c[2] < idx <= c[2] + 8):
            c[0].set(cv2.CAP_PROP_POS_FRAMES, idx)
            c[2] = idx - 1
        im = None
        while c[2] < idx:
            ok, im = c[0].read()
            c[2] += 1
            if not ok:
                break
        if im is not None:
            c[3] = im
    im = c[3] if c[3] is not None else np.zeros((1080, 1920, 3), np.uint8)
    if im.shape[1] != 1920:
        im = cv2.resize(im, (1920, 1080), interpolation=cv2.INTER_AREA)
    return im[..., ::-1].astype(np.float32) / 255.0


def real(t, nombre, seg, lz=None, zoom=1.2, cy=0.42, cx=0.5, sat=0.75, credito=True, rotulo=None, sub=None, tmision=None):
    """Clip a pantalla completa, recortado (fuera el HUD de la retransmisión), un poco desaturado, con marco de
    transmisión y capas de `lz` (líneas y rótulos blancos) encima."""
    im = frame_clip(nombre, seg)
    hh, wc = int(1080 / zoom), int(1920 / zoom)
    y0 = int(clamp(cy * 1080 - hh / 2, 0, 1080 - hh))
    x0 = int(clamp(cx * 1920 - wc / 2, 0, 1920 - wc))
    im = cv2.resize(im[y0:y0 + hh, x0:x0 + wc], (W, H), interpolation=cv2.INTER_CUBIC)
    g = im.mean(-1, keepdims=True)
    im = g + (im - g) * sat
    im = im * 0.92
    banda = np.clip((np.arange(H, dtype=np.float32) - 105) / 90.0, 0, 1)[:, None, None]   # arriba oscuro: tapa rótulos de la retransmisión
    im = im * (0.04 + 0.96 * banda)
    if lz is None:
        lz = L3(Cam((0, -10, 0), (0, 0, 0)))
    # marco de transmisión
    for (x, y, dx, dy) in ((40, 40, 1, 1), (W - 40, 40, -1, 1), (40, H - 40, 1, -1), (W - 40, H - 40, -1, -1)):
        lz.l2([(x + dx * 46, y), (x, y), (x, y + dy * 46)], 0.85, 1.6)
    if credito:
        lz.texto("VIDEO: " + CREDITO.get(nombre, "SPACEX"), W - 70, 66, 18, "SemiBold Condensed", 0.8, "rm", esp=0.2)
    if tmision is not None:
        lz.texto(tmision, 70, 66, 18, "SemiBold Condensed", 0.85, "lm", esp=0.16)
    if rotulo:
        lz.texto(rotulo, 70, H - 120, 46, "Bold Condensed", 1.0, "lm", esp=0.06)
        if sub:
            lz.texto(sub, 72, H - 76, 22, "SemiBold Condensed", 0.9, "lm", esp=0.16)
    ov = lz.final(t, brillo=0.6, grano=0.0)
    a = ov.mean(-1, keepdims=True)
    sombra = cv2.GaussianBlur(a, (0, 0), 6)[..., None] if a.ndim == 3 else a
    sombra = np.clip(sombra.reshape(H, W, 1) * 2.2, 0, 1)
    out = im * (1 - 0.7 * sombra) + ov
    return _Img(np.clip(out, 0, 1))


class _Img:
    """Envoltura para que un cuadro ya compuesto se trate como un L3 en el montaje."""

    def __init__(self, img):
        self.img = img

    def final(self, t=0.0):
        return self.img


# ------------------------------------------------------------------ geografía de Starbase (OSM)
SB = Sitio(25.99705, -97.15807)              # torre de la plataforma orbital 2 (OSM «Starbase Integration Tower 2»)
AZ = 97.0                                    # rumbo esquemático del ascenso (este-sureste, sobre el golfo)
SA, CA = math.sin(math.radians(AZ)), math.cos(math.radians(AZ))
DH = nrm(SA * SB.E + CA * SB.N)              # dirección horizontal del ascenso


def _costa():
    d = json.load(open(os.path.join(AQUI, "datos", "osm_costa.json"), encoding="utf-8"))
    out = []
    for e in d["elements"]:
        g = e.get("geometry")
        if g and len(g) >= 3:
            ll = np.array([[p["lat"], p["lon"]] for p in g])
            out.append(SB.a_mundo(*SB.latlon_a_en(ll[:, 0], ll[:, 1]), 0.0))
    return out


COSTA_SB = _costa()


# ------------------------------------------------------------------ fotos reales como pegatinas en marco de alambre
_FOTOS = {}


def _img_foto(nombre):
    if nombre not in _FOTOS:
        im = cv2.imread(os.path.join(AQUI, "imagenes", nombre + ".jpg"))
        f = 1400.0 / max(im.shape[:2])
        if f < 1:
            im = cv2.resize(im, (int(im.shape[1] * f), int(im.shape[0] * f)), interpolation=cv2.INTER_AREA)
        _FOTOS[nombre] = im[..., ::-1].astype(np.float32) / 255.0
    return _FOTOS[nombre]


def a_img(x, t):
    if isinstance(x, np.ndarray):
        return x
    return np.asarray(x.final(t), np.float32)


def foto(base, t, nombre, cx, cy, ancho, t0, t1, rotulo=None, sub=None, estilo=0, asp=None, foco=(0.5, 0.5), ancla=None, sat=0.8):
    """Pega la foto `imagenes/<nombre>.jpg` centrada en (cx, cy), `ancho` px, visible entre t0 y t1, con marco de alambre,
    rótulo y una entrada distinta por `estilo` (0 barrido de arriba abajo, 1 zoom desde el ancla, 2 deslizar, 3 apertura
    desde el centro con mira). `asp` = ancho/alto del recorte (None = el de la foto); `foco` = centro del recorte (0..1)."""
    img = a_img(base, t)
    if t < t0 - 0.01 or t > t1 + 0.01:
        return img
    src = _img_foto(nombre)
    hs, ws = src.shape[:2]
    asp = asp or ws / hs
    # recorte con el aspecto pedido y deriva lenta (zoom 1 → 1,06)
    z = 1.0 + 0.06 * pr(t, t0, t1)
    if ws / hs > asp:
        ch, cw = hs / z, hs * asp / z
    else:
        cw, ch = ws / z, ws / asp / z
    x0 = int(clamp(foco[0] * ws - cw / 2, 0, ws - cw))
    y0 = int(clamp(foco[1] * hs - ch / 2, 0, hs - ch))
    w = int(ancho)
    h = int(ancho / asp)
    sub_im = cv2.resize(src[y0:y0 + int(ch), x0:x0 + int(cw)], (w, h), interpolation=cv2.INTER_AREA)
    g = sub_im.mean(-1, keepdims=True)
    sub_im = (g + (sub_im - g) * sat) * 0.95
    k_in = e_out(pr(t, t0, t0 + 0.55))
    k_out = 1 - smooth(pr(t, t1 - 0.35, t1))
    dx = dy = 0.0
    esc = 1.0
    if estilo == 1:
        esc = lerp(0.55, 1.0, k_in)
        if ancla is not None:
            dx, dy = (ancla[0] - cx) * (1 - k_in), (ancla[1] - cy) * (1 - k_in)
    elif estilo == 2:
        dx = 160 * (1 - k_in)
    if esc != 1.0:
        sub_im = cv2.resize(sub_im, (max(2, int(w * esc)), max(2, int(h * esc))), interpolation=cv2.INTER_AREA)
    hh, ww_ = sub_im.shape[:2]
    X0, Y0 = int(cx + dx - ww_ / 2), int(cy + dy - hh / 2)
    mask = np.ones((hh, ww_, 1), np.float32)
    if estilo == 0:                                     # barrido de arriba abajo
        lim = k_in * (hh + 20)
        mask *= np.clip((lim - np.arange(hh, dtype=np.float32)) / 20.0, 0, 1)[:, None, None]
    elif estilo == 3:                                   # se abre desde el centro
        half = k_in * (ww_ / 2 + 20)
        dd = np.abs(np.arange(ww_, dtype=np.float32) - ww_ / 2)
        mask *= np.clip((half - dd) / 20.0, 0, 1)[None, :, None]
    else:
        mask *= k_in
    mask *= k_out
    xa, ya, xb, yb = max(0, X0), max(0, Y0), min(W, X0 + ww_), min(H, Y0 + hh)
    if xb > xa and yb > ya:
        m = mask[ya - Y0:yb - Y0, xa - X0:xb - X0]
        p = sub_im[ya - Y0:yb - Y0, xa - X0:xb - X0]
        img = img.copy()
        img[ya:yb, xa:xb] = img[ya:yb, xa:xb] * (1 - m * 0.97) + p * m
    # marco, rótulo y guía (líneas blancas)
    lz = L3(Cam((0, -10, 0), (0, 0, 0)))
    op = min(k_in * 1.4, 1.0) * k_out
    xL, yT, xR, yB = X0 - 6, Y0 - 6, X0 + ww_ + 6, Y0 + hh + 6
    L = 34
    if estilo in (0, 2):
        for (x, y, sx, sy) in ((xL, yT, 1, 1), (xR, yT, -1, 1), (xL, yB, 1, -1), (xR, yB, -1, -1)):
            lz.l2([(x + sx * L, y), (x, y), (x, y + sy * L)], op, 1.8)
        lz.l2([(xL, yT), (xR, yT), (xR, yB), (xL, yB)], op * 0.3, 0.8, cerrada=True)
    elif estilo == 1:
        lz.l2([(xL, yT), (xR, yT), (xR, yB), (xL, yB)], op * 0.9, 1.4, cerrada=True)
        lz.l2([(xL, yT), (xL, yT - 22), (xL + 150, yT - 22), (xL + 164, yT)], op * 0.9, 1.4)
    else:
        lz.l2([(xL, yT), (xR, yT), (xR, yB), (xL, yB)], op * 0.5, 1.0, cerrada=True)
        mx, my = (xL + xR) / 2, (yT + yB) / 2
        for (a1, b1, a2, b2) in ((xL - 18, my, xL + 14, my), (xR - 14, my, xR + 18, my), (mx, yT - 18, mx, yT + 14), (mx, yB - 14, mx, yB + 18)):
            lz.l2([(a1, b1), (a2, b2)], op, 1.6)
    if estilo == 0 and k_in < 1:                        # línea de barrido
        ys = Y0 + k_in * hh
        lz.l2([(xL - 10, ys), (xR + 10, ys)], op * (1 - k_in) * 1.5, 2.0)
    if rotulo:
        ty = yB + 34
        lz.texto(rotulo, xL, ty, 34, "Bold Condensed", op, "lm", esp=0.06, fondo=True)
        if sub:
            lz.texto(sub, xL + 2, ty + 32, 18, "SemiBold Condensed", op * 0.9, "lm", esp=0.16, fondo=True)
    if ancla is not None:
        ax, ay = ancla
        bx = xL if ax < xL else (xR if ax > xR else ax)
        by = yT if ay < yT else (yB if ay > yB else ay)
        lz.l2([(bx, by), (ax, ay)], op * 0.7, 1.0)
        lz.c2(ax, ay, 6, op, w=1.4)
    ov = lz.final(t, brillo=0.6, grano=0.0)
    a = ov.mean(-1, keepdims=True)
    sombra = np.clip(cv2.GaussianBlur(a, (0, 0), 5).reshape(H, W, 1) * 2.0, 0, 1)
    return np.clip(img * (1 - 0.6 * sombra) + ov, 0, 1)


def vacio():
    return L3(Cam((0, -10, 0), (0, 0, 0)))


def bloque(lz, x, y, titulo, sub, op, px=64, anchor="lm"):
    if op <= 0.01:
        return
    lz.texto(titulo, x, y, px, "Bold Condensed", op, anchor, esp=0.05)
    if sub:
        lz.texto(sub, x + (4 if anchor[0] == "l" else 0), y + px * 0.62 + 6, 24, "SemiBold Condensed", op * 0.9, anchor, esp=0.14)


def cabecera(lz, txt, op=0.85):
    lz.texto("T MENOS CERO", 64, 62, 26, "SemiBold Condensed", op, "lm", esp=0.2)
    lz.texto(txt, 64, 94, 19, "Light Condensed", op * 0.85, "lm", esp=0.16)
