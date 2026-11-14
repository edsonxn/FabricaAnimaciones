# -*- coding: utf-8 -*-
"""Piezas comunes del vuelo 15 de Starship (kit LÍNEA 3D): anclas a la voz, reloj de misión, HUD con los 33 + 6 motores,
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


# ------------------------------------------------------------------ reloj de misión (video -> segundos de misión)
def _reloj():
    r = [(T0("presenta") + 0.5, -1200.0), (T1("presenta"), -40.0),
         (T0("despegue"), -12.0), (ww("despegue", 0, "encienden"), -3.0), (ww("despegue", 1, "despega"), 0.0),
         (T1("despegue"), 30.0),
         (T0("maxq"), 40.0), (ww("maxq", 0, "potencia"), 58.0), (T1("maxq"), 110.0),
         (T0("separa"), 125.0), (ww("separa", 0, "apaga"), 139.0), (ww("separa", 1, "enciende"), 141.0),
         (F1("separa", 3), 143.0), (T1("separa"), 144.0),
         (ww("propulsor", 1, "enciende"), 146.0), (F1("propulsor", 2), 156.0), (ww("propulsor", 3, "cae"), 182.0),
         (ww("propulsor", 4, "enciende"), 370.0), (ww("propulsor", 6, "decide"), 380.0),
         (ww("propulsor", 7, "desvia"), 388.0), (ww("propulsor", 9, "desintegra"), 400.0), (T1("propulsor"), 404.0),
         (T0("orbita"), 420.0), (ww("orbita", 1, "apaga"), 489.0), (F1("orbita", 2), 498.0),
         (ww("orbita", 3, "veintiseis"), 1570.0), (F1("orbita", 3), 1590.0), (T1("orbita"), 1700.0),
         (T0("starlink"), 2060.0), (ww("starlink", 0, "abre"), 2101.0), (ww("starlink", 2, "cuarenta"), 4000.0),
         (F1("starlink", 2), 4660.0), (T1("starlink"), 4900.0),
         (T0("vueltas"), 5000.0), (ww("vueltas", 3, "hawai"), 5266.0), (ww("vueltas", 3, "chile"), 26135.0),
         (ww("vueltas", 3, "otra"), 74515.0), (T1("vueltas"), 77600.0),
         (ww("reentrada", 0, "enciende"), 77757.0), (F1("reentrada", 0), 77767.0), (ww("reentrada", 2, "toca"), 79846.0),
         (T1("reentrada"), 80700.0),
         (T0("llegada"), 80940.0), (ww("llegada", 0, "baja"), 81013.0), (ww("llegada", 2, "enciende"), 81136.0),
         (ww("llegada", 3, "gira"), 81137.0), (F1("llegada", 3), 81139.0), (ww("llegada", 4, "tres"), 81140.0),
         (ww("llegada", 4, "dos"), 81142.0), (ww("llegada", 4, "uno"), 81146.0), (F1("llegada", 5), 81148.0),
         (T1("llegada"), 81150.0)]
    ta = np.array([a for a, b in r])
    for i in range(1, len(ta)):              # T1 de una escena = T0 de la siguiente: separa los dos anclajes
        if ta[i] <= ta[i - 1]:
            ta[i] = ta[i - 1] + 0.04
    return ta, np.array([b for a, b in r])


_RT, _RM = _reloj()
assert np.all(np.diff(_RT) > 0) and np.all(np.diff(_RM) > 0), "RELOJ no monótono"


def mision(t):
    return float(np.interp(t, _RT, _RM))


EVENTOS = [(58, "MAX-Q"), (139, "MECO"), (370, "ATERRIZAJE B22"), (489, "SECO"), (1570, "INSERCIÓN"),
           (2101, "STARLINK"), (5266, "CONTROL HAWÁI"), (26135, "CONTROL CHILE"), (74515, "CONTROL HAWÁI"),
           (77757, "SALIDA DE ÓRBITA"), (79846, "ENTRADA"), (81136, "ATERRIZAJE"), (81148, "CAPTURA")]


def fmt_t(m):
    signo = "T+" if m >= 0 else "T-"
    s = int(round(abs(m))) if m < 0 else int(abs(m))
    return f"{signo} {s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


# ------------------------------------------------------------------ motores
SH_ANILLO = [k for k, *_ in S.motores_sh()]          # 0 = 3 centrales, 1 = 10 interiores, 2 = 20 exteriores
FALLA = 21                                           # motor que no reencendió en la quema de regreso (de los 33)


def motores_sh(m):
    if -3 <= m < 139:
        return list(range(33))
    if 139 <= m < 141.5:
        return [0, 1, 2]
    if 146 <= m < 182:
        return [i for i in range(33) if i != FALLA]
    if 370 <= m < 395:
        return [0, 1, 2]
    return []


def motores_nave(m):
    if 141 <= m < 489:
        return list(range(6))
    if 1570 <= m < 1590 or 77757 <= m < 77767:
        return [0]
    if 81136 <= m < 81141:
        return [0, 1, 2]
    if 81141 <= m < 81147:
        return [0, 1]
    if 81147 <= m < 81148.5:
        return [0]
    return []


def estado_sh(m):
    if m < -3:
        return "EN PLATAFORMA"
    for a, b, txt in ((-3, 139, "33 RAPTOR"), (139, 141.5, "MECO"), (141.5, 146, "MEDIA VUELTA"), (146, 182, "QUEMA DE REGRESO"),
                      (182, 370, "CAÍDA DE COLA"), (370, 380, "QUEMA DE ATERRIZAJE"), (380, 400, "ABORTO · AL MAR")):
        if a <= m < b:
            return txt
    return "PERDIDO EN EL GOLFO"


def estado_nave(m):
    for a, b, txt in ((-1e9, 141, "EN ESPERA"), (141, 489, "6 RAPTOR"), (489, 1570, "SECO"), (1570, 1590, "QUEMA DE INSERCIÓN"),
                      (1590, 2101, "EN ÓRBITA"), (2101, 4660, "DESPLIEGUE STARLINK"), (4660, 77757, "EN ÓRBITA"),
                      (77757, 77767, "SALIDA DE ÓRBITA"), (77767, 79846, "CAYENDO"), (79846, 80974, "REENTRADA"),
                      (80974, 81136, "PLANEO DE PANZA"), (81136, 81148, "QUEMA DE ATERRIZAJE")):
        if a <= m < b:
            return txt
    return "ATRAPADA"


# ------------------------------------------------------------------ HUD
def hud_reloj(lz, m, op=1.0):
    if op <= 0.01:
        return
    cx, cy, Rr = W / 2, 952 + 1500, 1500.0
    k = 0.0196

    def ang(mm):
        d = mm - m
        return math.copysign(k * abs(d) ** 0.42, d)
    A = np.linspace(-0.62, 0.62, 160)
    pts = np.stack([cx + Rr * np.sin(A), cy - Rr * np.cos(A)], 1)
    mid = len(A) // 2
    lz.l2(pts[:mid + 1], op * 0.85, 1.4)
    lz.l2(pts[mid:], op * 0.3, 1.0)
    vis = [(mm, nom) for mm, nom in EVENTOS if abs(ang(mm)) <= 0.6]
    for ie, (mm, nom) in enumerate(vis):
        a = ang(mm)
        x, y = cx + Rr * math.sin(a), cy - Rr * math.cos(a)
        fade = op * clamp((0.6 - abs(a)) / 0.12)
        pasado = mm <= m
        lz.c2(x, y, 6.5, fade * (1.0 if pasado else 0.5), w=1.2, lleno=pasado)
        alto = 20 if ie % 2 == 0 else 44
        if ie % 2:
            lz.l2([(x, y - 9), (x, y - alto + 4)], fade * 0.35, 0.8)
        lz.texto(nom, x, y - alto, 16, "SemiBold Condensed", fade * (0.95 if pasado else 0.55), "mb", esp=0.14)
    lz.l2([(cx, cy - Rr - 12), (cx, cy - Rr + 12)], op, 1.6)
    lz.texto(fmt_t(m), cx, 1016, 40, "SemiBold Condensed", op, "mm", esp=0.08, fondo=True)


def panel_sh(lz, x, y, m, op=1.0):
    """33 motores en sus 3 anillos (vista desde abajo), encendidos llenos; el que falló, con una X."""
    if op <= 0.01:
        return
    enc = set(motores_sh(m))
    lz.texto("SUPER HEAVY · B22", x, y - 70, 19, "SemiBold Condensed", op * 0.8, "lm", esp=0.2)
    lz.texto(estado_sh(m), x, y + 70, 21, "SemiBold Condensed", op, "lm", esp=0.1)
    cx = x + 52
    lz.c2(cx, y, 50, op * 0.5, w=1.0)
    for i, (k, mx, my, rt) in enumerate(S.motores_sh()):
        px, py = cx + mx * 11.0, y + my * 11.0
        on = i in enc
        lz.c2(px, py, 4.2, op * (1.0 if on else 0.4), w=1.0, lleno=on)
        if i == FALLA and 146 <= m < 400:
            lz.l2([(px - 6, py - 6), (px + 6, py + 6)], op, 1.4)
            lz.l2([(px - 6, py + 6), (px + 6, py - 6)], op, 1.4)
    if m >= 400:
        lz.l2([(cx - 56, y - 56), (cx + 56, y + 56)], op * 0.7, 1.2)


def panel_nave(lz, x, y, m, op=1.0):
    if op <= 0.01:
        return
    enc = set(motores_nave(m))
    lz.texto("NAVE · S42", x, y - 70, 19, "SemiBold Condensed", op * 0.8, "rm", esp=0.2)
    lz.texto(estado_nave(m), x, y + 70, 21, "SemiBold Condensed", op, "rm", esp=0.1)
    cx = x - 52
    lz.c2(cx, y, 50, op * 0.5, w=1.0)
    for i in range(6):
        if i < 3:
            a = 2 * math.pi * i / 3 - math.pi / 2
            px, py, r = cx + math.cos(a) * 13, y + math.sin(a) * 13, 6.0
        else:
            a = 2 * math.pi * (i - 3) / 3 + math.pi / 3 - math.pi / 2
            px, py, r = cx + math.cos(a) * 33, y + math.sin(a) * 33, 11.0
        on = i in enc
        lz.c2(px, py, r, op * (1.0 if on else 0.4), w=1.0, lleno=on)


def hud_mision(lz, op=1.0):
    if op <= 0.01:
        return
    lz.texto("STARSHIP  ·  VUELO 15", 64, 62, 30, "SemiBold Condensed", op, "lm", esp=0.16)
    lz.texto("13 NOV 2026  ·  STARBASE, TEXAS", 64, 96, 19, "Light Condensed", op * 0.85, "lm", esp=0.16)


def hud(lz, t, reloj=1.0, sh=1.0, nave=1.0, mis=1.0):
    m = mision(t)
    hud_mision(lz, mis)
    hud_reloj(lz, m, reloj)
    panel_sh(lz, 64, 960, m, sh * reloj)
    panel_nave(lz, W - 64, 960, m, nave * reloj)


# ------------------------------------------------------------------ video real (retransmisión de SpaceX)
CLIPS = {"lanz": "clips/lanz_a.mp4", "reg": "clips/regreso_full.mp4", "o1150": "clips/orb_1150.mp4",
         "o4395": "clips/orb_4395.mp4", "o5790": "clips/orb_5790.mp4"}
_CAP = {}


def frame_clip(nombre, seg):
    """Cuadro RGB float32 0..1 a 1920x1080 del clip en el segundo `seg` (lectura secuencial con caché)."""
    if nombre not in _CAP:
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
        lz.texto("VIDEO: SPACEX", W - 70, 66, 18, "SemiBold Condensed", 0.8, "rm", esp=0.2)
    if tmision is not None:
        lz.texto("RETRANSMISIÓN  ·  " + fmt_t(tmision), 70, 66, 18, "SemiBold Condensed", 0.85, "lm", esp=0.16)
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


def mapa_sb(lz, op=1.0):
    lz.lineas(COSTA_SB, op * 0.9, 1.2)


# ------------------------------------------------------------------ trayectorias esquemáticas (s km de recorrido, h km)
ASC = curva_suave([(0, 0, 0), (10, 0, 0.2), (20, 0.05, 1.0), (30, 0.3, 2.6), (45, 1.3, 6.5), (58, 3.0, 11), (80, 7, 20),
                   (110, 18, 38), (139, 35, 65), (160, 52, 85), (200, 100, 120), (260, 210, 150), (330, 430, 170),
                   (420, 900, 185), (489, 1400, 190), (600, 2250, 195), (1500, 9000, 200), (1590, 9700, 275)], paso=0.25, suav=10)
BOO = curva_suave([(0, 0, 0), (10, 0, 0.2), (20, 0.05, 1.0), (30, 0.3, 2.6), (45, 1.3, 6.5), (58, 3.0, 11), (80, 7, 20),
                   (110, 18, 38), (139, 35, 65), (146, 40, 70), (160, 47, 80), (182, 50, 92), (220, 46, 102), (260, 38, 100),
                   (300, 28, 84), (340, 17, 55), (370, 9, 22), (380, 6.5, 10), (390, 6.8, 3.5), (400, 8.0, 0.4),
                   (900, 8.0, 0.0)], paso=0.25, suav=6)


def p_asc(m):
    s, h = ASC(min(max(m, 0.0), 1590.0))
    return SB.gran_circulo(AZ, s, h)


def p_boo(m):
    if m < 0:
        return SB.P.copy()
    s, h = BOO(min(m, 900.0))
    return SB.gran_circulo(AZ, s, h)


def prog(f, m, dm=0.5):
    return nrm(f(m + dm) - f(m - dm))


def marco(p):
    u = nrm(p)
    e = nrm(np.cross([0, 0, 1.0], u))
    return e, np.cross(u, e), u


def trayecto(lz, f, m0, m1, op=1.0, w=1.4, guion=None, n=240):
    if m1 <= m0:
        return
    P = np.array([f(x) for x in np.linspace(m0, m1, n)])
    lz.linea(P, op, w, guion=guion)


def slerp(a, b, u):
    a, b = nrm(a), nrm(b)
    d = clamp(float(a @ b), -1, 1)
    om = math.acos(d)
    if om < 1e-5:
        return a
    return nrm((math.sin((1 - u) * om) * a + math.sin(u * om) * b) / math.sin(om))


def oculto_tierra(c, P):
    d = P - c
    L2 = np.sum(d * d, -1)
    s = np.clip(-(d @ c) / np.maximum(L2, 1e-9), 0, 1)
    q = c + d * s[:, None]
    return ((np.linalg.norm(q, axis=-1) < R_T - 1) & (s < 0.999)).astype(float)


# ------------------------------------------------------------------ órbita (inclinación 30,5°, ~277 km, periodo ~90 min)
INC = math.radians(30.5)
R_ORB = R_T + 277.0
PERIODO = 5403.0
W_T = 2 * math.pi / 86164.0
U0 = math.pi - math.asin(math.sin(math.radians(SB.lat if hasattr(SB, "lat") else 25.997)) / math.sin(INC))


def orbita_eci(m, raan=None):
    """Posición en un marco fijo a la Tierra (km). La Tierra gira debajo: ground track que se corre al oeste."""
    raan = math.radians(-97.16) - math.atan2(math.cos(INC) * math.sin(U0), math.cos(U0)) if raan is None else raan
    u = U0 + 2 * math.pi * (m - 600.0) / PERIODO
    x, y, z = math.cos(u), math.sin(u) * math.cos(INC), math.sin(u) * math.sin(INC)
    lon = raan - W_T * (m - 600.0)
    c, s = math.cos(lon), math.sin(lon)
    return np.array([x * c - y * s, x * s + y * c, z]) * R_ORB
