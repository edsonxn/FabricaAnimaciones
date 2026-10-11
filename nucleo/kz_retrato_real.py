# -*- coding: utf-8 -*-
"""Retratos REALES (pinturas, grabados y fotos de dominio público, de Wikimedia Commons) integrados en el estilo Kurzgesagt.
En vez de un busto dibujado, se muestra el cuadro histórico dentro de un marco dorado con bisel, sombra y brillo que cruza el cristal: se mezcla con la animación
(mapa de color hacia el morado/crema de la paleta, viñeta, flotación suave) y no parece una foto pegada.
Los recortes ya hechos viven en nucleo/datos/retratos/ (ver CREDITOS.md; se generan con nucleo/preparar_retratos.py).
API compatible con kz_retrato.retrato y kz_mapa_dib.medallon: si `quien` tiene retrato real, esas funciones delegan aquí (el resto de personajes sigue dibujado)."""
import math
import os
from functools import lru_cache

import cv2
import numpy as np

from motor import rect_red

AQUI = os.path.dirname(os.path.abspath(__file__))
DIR = os.path.join(AQUI, "datos", "retratos")

# hacia dónde mira el personaje en el cuadro original: +1 derecha, -1 izquierda, 0 de frente (para voltearlo si la escena pide otra dirección)
MIRA = {"allende": 1, "leona": 1, "odonoju": 1, "napoleon": 1, "morelos": 1, "matamoros": 1, "porfirio": 1}

PW, PH = 448, 560           # lienzo del cuadro (retrato)
MARCO = 24                  # grosor del marco
MARG = 40                   # margen para la sombra
SW, SH = PW + 2 * (MARCO + MARG), PH + 2 * (MARCO + MARG)
FRAME_H = PH + 2 * MARCO    # alto del marco en el sprite
FRAME_W = PW + 2 * MARCO
MD = 400                    # diámetro del medallón en el sprite (sin marco)
RING = 22


def hay(quien):
    return os.path.exists(os.path.join(DIR, f"{quien}.jpg"))


def _grad_map(rgb, mezcla=0.34):
    """Mezcla el cuadro con un mapa de degradado de la paleta del video (sombras moradas, luces cremas) y baja un poco la saturación."""
    f = rgb.astype(np.float32) / 255.0
    L = (0.299 * f[..., 0] + 0.587 * f[..., 1] + 0.114 * f[..., 2])[..., None]
    c0 = np.array([0.15, 0.09, 0.33], np.float32)
    c1 = np.array([0.70, 0.40, 0.48], np.float32)
    c2 = np.array([1.00, 0.93, 0.80], np.float32)
    g = np.where(L < 0.5, c0 + (c1 - c0) * (L / 0.5), c1 + (c2 - c1) * ((L - 0.5) / 0.5))
    sat = L + (f - L) * 0.90
    out = sat * (1 - mezcla) + g * mezcla
    out = (out - 0.5) * 1.06 + 0.5
    return np.clip(out, 0, 1)


def _suavizar(bgr):
    x = cv2.bilateralFilter(bgr, 9, 38, 8)
    x = cv2.bilateralFilter(x, 7, 30, 6)
    return x


def _rr(w, h, r, escala=1):
    m = np.zeros((h * escala, w * escala), np.uint8)
    cv2.rectangle(m, (r * escala, 0), (w * escala - r * escala - 1, h * escala - 1), 255, -1)
    cv2.rectangle(m, (0, r * escala), (w * escala - 1, h * escala - r * escala - 1), 255, -1)
    for cx, cy in ((r, r), (w - r - 1, r), (r, h - r - 1), (w - r - 1, h - r - 1)):
        cv2.circle(m, (cx * escala, cy * escala), r * escala, 255, -1, cv2.LINE_AA)
    return cv2.resize(m, (w, h), interpolation=cv2.INTER_AREA) if escala > 1 else m


def _mezclar(dst, src_rgb, mask01):
    a = mask01[..., None]
    dst[..., :3] = dst[..., :3] * (1 - a) + src_rgb * a
    dst[..., 3:4] = np.maximum(dst[..., 3:4], a)


def _viñeta(h, w, fuerza=0.55):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h * 0.46) / (h / 2)) ** 2)
    v = np.clip((d - 0.55) / 0.75, 0, 1) ** 1.6
    return (1 - fuerza * v)[..., None]


@lru_cache(maxsize=64)
def _cuadro(quien, borde=(250, 206, 90)):
    """Sprite RGBA premultiplicado (uint8) del retrato enmarcado + sombra. Devuelve (sprite, caja_cristal_pts)."""
    ruta = os.path.join(DIR, f"{quien}.jpg")
    img = cv2.imread(ruta)
    img = cv2.resize(img, (PW, PH), interpolation=cv2.INTER_CUBIC)
    img = _suavizar(img)
    rgb = _grad_map(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) * _viñeta(PH, PW)
    S = np.zeros((SH, SW, 4), np.float32)
    ox, oy = MARG, MARG
    fw, fh = FRAME_W, FRAME_H
    marco = _rr(fw, fh, 30, 3)
    mf = np.zeros((SH, SW), np.float32)
    mf[oy:oy + fh, ox:ox + fw] = marco / 255.0
    # sombra
    sh = cv2.GaussianBlur(np.roll(np.roll(mf, 12, 0), 9, 1), (0, 0), 13)
    S[..., :3] = np.array([0.04, 0.025, 0.16], np.float32)
    S[..., 3] = sh * 0.50
    # marco dorado: molduras concéntricas (borde oscuro, banda dorada, filete claro, paspartú) con degradado vertical y bisel
    yy = np.linspace(0, 1, fh, dtype=np.float32)[:, None, None]
    brillo_v = 1.14 - 0.34 * yy
    bc = np.array(borde, np.float32) / 255.0
    oscuro = np.clip(bc * 0.50, 0, 1)
    medio = bc
    claro = np.clip(bc * 1.05 + 0.16, 0, 1)
    cuerpo = np.zeros((fh, fw, 3), np.float32)
    masc = np.zeros((fh, fw), np.float32)
    for inset, rad, col in ((0, 30, oscuro), (4, 27, medio), (13, 21, oscuro * 1.15), (15, 19, claro), (19, 15, np.array([0.09, 0.05, 0.17], np.float32))):
        m = np.zeros((fh, fw), np.float32)
        r = _rr(fw - 2 * inset, fh - 2 * inset, rad, 3) / 255.0
        m[inset:fh - inset, inset:fw - inset] = r
        c = np.clip(col * (brillo_v if inset in (4, 15) else 1.0), 0, 1)
        cuerpo = cuerpo * (1 - m[..., None]) + c * m[..., None]
        masc = np.maximum(masc, m)
    marco = masc * 255.0
    m_in = (marco > 127).astype(np.uint8)
    luz = m_in.astype(bool) & ~np.roll(np.roll(m_in, 3, 0), 3, 1).astype(bool)
    sombra_b = m_in.astype(bool) & ~np.roll(np.roll(m_in, -3, 0), -3, 1).astype(bool)
    cuerpo[luz] = np.clip(cuerpo[luz] * 0.55 + 0.52, 0, 1)
    cuerpo[sombra_b] = cuerpo[sombra_b] * 0.55
    _mezclar(S[oy:oy + fh, ox:ox + fw], cuerpo, masc)
    # el cuadro
    px, py = ox + MARCO, oy + MARCO
    mp = _rr(PW, PH, 10, 2) / 255.0
    sub = S[py:py + PH, px:px + PW]
    sub[..., :3] = sub[..., :3] * (1 - mp[..., None]) + rgb * mp[..., None]
    sub[..., 3] = np.maximum(sub[..., 3], mp)
    # sombra interior suave sobre el cuadro (cristal)
    inner = cv2.GaussianBlur((255 - cv2.erode(_rr(PW, PH, 10), np.ones((9, 9), np.uint8))).astype(np.float32) / 255.0, (0, 0), 6) * mp
    sub[..., :3] *= (1 - 0.35 * inner[..., None])
    # remaches
    for cx, cy in ((ox + 13, oy + 13), (ox + fw - 14, oy + 13), (ox + 13, oy + fh - 14), (ox + fw - 14, oy + fh - 14)):
        col = tuple(float(v) for v in np.clip(bc * 0.6, 0, 1)) + (1.0,)
        cv2.circle(S, (int(cx), int(cy)), 5, col, -1, cv2.LINE_AA)
        cv2.circle(S, (int(cx) - 1, int(cy) - 1), 3, (1.0, 0.95, 0.75, 1.0), -1, cv2.LINE_AA)
    rgb_pm = S[..., :3] * S[..., 3:4]
    spr = np.concatenate([rgb_pm * 255.0, S[..., 3:4] * 255.0], -1).round().astype(np.uint8)
    # contorno del cristal (para el brillo), en coordenadas del sprite centradas
    cristal = _rr_pts(px - SW / 2, py - SH / 2, PW, PH, 10)
    return spr, cristal


def _rr_pts(x, y, w, h, r, n=5):
    pts = []
    for cx, cy, a0 in ((x + w - r, y + r, -90), (x + w - r, y + h - r, 0), (x + r, y + h - r, 90), (x + r, y + r, 180)):
        for a in np.linspace(a0, a0 + 90, n):
            pts.append((cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))))
    return np.array(pts, float)


@lru_cache(maxsize=64)
def _medalla(quien, borde=(250, 206, 90), ring=(60, 40, 110)):
    ruta = os.path.join(DIR, f"{quien}_m.jpg")
    if not os.path.exists(ruta):
        ruta = os.path.join(DIR, f"{quien}.jpg")
    img = cv2.imread(ruta)
    h0, w0 = img.shape[:2]
    if abs(h0 - w0) > 4:                       # recorte cuadrado desde el centro-alto de un retrato 4:5
        lado = w0
        y0 = int(h0 * 0.10)
        img = img[y0:y0 + lado, :]
    img = cv2.resize(img, (MD, MD), interpolation=cv2.INTER_CUBIC)
    img = _suavizar(img)
    rgb = _grad_map(cv2.cvtColor(img, cv2.COLOR_BGR2RGB)) * _viñeta(MD, MD, 0.5)
    D = MD + 2 * RING + 2 * 36
    S = np.zeros((D, D, 4), np.float32)
    c = D // 2
    yy, xx = np.mgrid[0:D, 0:D].astype(np.float32)
    d = np.sqrt((xx - c) ** 2 + (yy - c) ** 2)
    r_in = MD / 2
    r_out = r_in + RING
    disco = np.clip(r_in + 0.8 - d, 0, 1)
    anillo = np.clip(r_out + 0.8 - d, 0, 1)
    # sombra
    sh = cv2.GaussianBlur(np.clip(r_out + 0.8 - np.sqrt((xx - c - 8) ** 2 + (yy - c - 12) ** 2), 0, 1), (0, 0), 11)
    S[..., :3] = np.array([0.04, 0.025, 0.16], np.float32)
    S[..., 3] = sh * 0.45
    # anillo dorado con degradado y bisel
    bc = np.array(borde, np.float32) / 255.0
    t = np.clip((yy - (c - r_out)) / (2 * r_out), 0, 1)[..., None]
    oro = np.clip(bc * 1.04 + 0.04, 0, 1) * (1 - t) + np.clip(bc * 0.70, 0, 1) * t
    luz = np.clip(1 - np.abs(d - (r_out - 3)) / 3.0, 0, 1) * np.clip(-(xx - c) - (yy - c), 0, 60) / 60.0
    oro = np.clip(oro + luz[..., None] * 0.5, 0, 1)
    _mezclar(S, oro, anillo)
    # canal oscuro entre anillo y cuadro
    canal = np.clip(1 - np.abs(d - (r_in + 1.5)) / 4.0, 0, 1)
    S[..., :3] = S[..., :3] * (1 - 0.6 * canal[..., None]) + np.array([0.10, 0.06, 0.20], np.float32) * 0.6 * canal[..., None]
    # cuadro
    big = np.zeros((D, D, 3), np.float32)
    o = (D - MD) // 2
    big[o:o + MD, o:o + MD] = rgb
    S[..., :3] = S[..., :3] * (1 - disco[..., None]) + big * disco[..., None]
    S[..., 3] = np.maximum(S[..., 3], disco)
    inner = np.clip((d - (r_in - 16)) / 16.0, 0, 1) * disco
    S[..., :3] *= (1 - 0.35 * inner[..., None])
    rgb_pm = S[..., :3] * S[..., 3:4]
    spr = np.concatenate([rgb_pm * 255.0, S[..., 3:4] * 255.0], -1).round().astype(np.uint8)
    return spr, D, r_out


def _brillo(lz, t, cx, cy, k, contorno, seed=0, alfa=1.0, periodo=5.5):
    """Franja diagonal de luz que cruza el cristal cada pocos segundos (recortada a la forma del cuadro)."""
    u = ((t + seed * 0.9) % periodo) / periodo
    if u > 0.32:
        return
    v = u / 0.32
    ox = (-1.1 + 2.2 * v) * (PW * 0.5)
    w = PW * 0.20
    a = 0.20 * math.sin(math.pi * v) ** 0.7 * alfa
    tira = np.array([(ox - w, -PH * 0.62), (ox + w * 0.3, -PH * 0.62), (ox + w * 0.3 + PH * 0.32, PH * 0.62), (ox - w + PH * 0.32, PH * 0.62)], float)
    pts = contorno * k + (cx, cy)
    with lz.recorte(pts):
        lz.relleno(tira * k + (cx, cy), (255, 250, 235), alfa=a, temblor=0.0)


def retrato(lz, x, y, s, quien, t=0.0, emocion="neutro", habla=0.0, mirar=0.0, alfa=1.0, flip=1, luz_borde=(255, 220, 90), seed=0, mano=None, borde=(250, 206, 90)):
    """Retrato enmarcado. (x, y, s) con la misma convención que kz_retrato.retrato: s ≈ alto de la cabeza / 2,4; (x, y) = base del cuello. Flota suavemente; si habla, late un poco."""
    if alfa <= 0.01:
        return
    spr, cristal = _cuadro(quien, tuple(borde))
    nat = MIRA.get(quien, 0)
    want = (1 if mirar > 0.15 else (-1 if mirar < -0.15 else 0)) * (1 if flip >= 0 else -1) if mirar else 0
    voltear = (nat != 0 and want != 0 and want != nat) or (flip < 0 and nat == 0 and False)
    if voltear:
        spr = spr[:, ::-1].copy()
        cristal = cristal * [-1, 1]
    alto = 3.45 * s
    cy = y - 3.05 * s + alto / 2
    cy = min(cy, 1080 - 18 - alto / 2) if alto < 1000 else cy
    k = alto / FRAME_H
    cy += 3.5 * math.sin(t * 1.3 + seed) * (s / 150.0)
    rot = 0.010 * math.sin(t * 0.8 + seed * 1.7)
    if habla > 0:
        k *= 1 + 0.014 * habla * (0.5 + 0.5 * math.sin(t * 13.0 + seed))
    if luz_borde is not None:
        lz.halo(x, cy, alto * 0.78, luz_borde, alfa=0.20 * alfa)
    lz.pegar(spr, x, cy, k, rot, (0.5, 0.5), alfa)
    zr = getattr(lz, "zonas_rot", None)
    if zr is not None:                                  # las etiquetas sin cola esquivan el marco
        zr.append((x - FRAME_W * k / 2, cy - FRAME_H * k / 2, x + FRAME_W * k / 2, cy + FRAME_H * k / 2))
    if rot == 0.0:
        _brillo(lz, t, x, cy, k, cristal, seed, alfa)
    else:
        c, sn = math.cos(rot), math.sin(rot)
        cr = np.stack([cristal[:, 0] * c - cristal[:, 1] * sn, cristal[:, 0] * sn + cristal[:, 1] * c], 1)
        _brillo(lz, t, x, cy, k, cr, seed, alfa)


def medallon(lz, x, y, r, quien, t, emocion="neutro", borde=(250, 206, 90), fondo=(60, 40, 110), alfa=1.0, seed=0, habla=0.0, k=1.0):
    """Retrato real en medallón redondo con anillo dorado (para mapas y escenas). r = radio exterior del anillo en px cuando k = 1."""
    if k <= 0.01 or alfa <= 0.01:
        return
    spr, D, r_out = _medalla(quien, tuple(borde))
    kk = (r * k) / r_out
    if habla > 0:
        kk *= 1 + 0.02 * habla * (0.5 + 0.5 * math.sin(t * 13.0 + seed))
    with lz.capa(2):
        lz.pegar(spr, x, y + 2.5 * math.sin(t * 1.4 + seed), kk, 0.0, (0.5, 0.5), alfa)
