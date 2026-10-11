# -*- coding: utf-8 -*-
"""Pintura a guache procedural para los fondos del Short: capas horneadas (RGBA, con margen para la cámara y paralaje) y efectos
dinámicos que se pintan encima de cada cuadro (discos, halos, rayos, manchas, niebla, estática de tele). Todo uint8 RGB."""
import math

import cv2
import numpy as np

from motor import H, W

MX, MY = 90, 160                 # margen de cada capa (px) para cámara y paralaje
BW, BH = W + 2 * MX, H + 2 * MY
pi = math.pi


# ------------------------------------------------------------------ ruido y texturas
_cache_campo = {}


def campo(seed, esc, octavas=3, shape=(BH, BW)):
    """Ruido suave ~N(0,1) de escala `esc` px (fractal)."""
    k = (seed, esc, octavas, shape)
    if k in _cache_campo:
        return _cache_campo[k]
    r = np.random.default_rng(seed)
    out = np.zeros(shape, np.float32)
    amp = 1.0
    for o in range(octavas):
        s = max(4, esc / (2 ** o))
        gh, gw = int(shape[0] / s) + 4, int(shape[1] / s) + 4
        g = r.normal(0, 1, (gh, gw)).astype(np.float32)
        out += amp * cv2.resize(g, (int(gw * s), int(gh * s)), interpolation=cv2.INTER_CUBIC)[:shape[0], :shape[1]]
        amp *= 0.5
    out = (out - out.mean()) / (out.std() + 1e-6)
    if len(_cache_campo) > 12:
        _cache_campo.clear()
    _cache_campo[k] = out
    return out


def _grano_fino():
    r = np.random.default_rng(5)
    n = r.normal(0, 1, (BH, BW)).astype(np.float32)
    return cv2.GaussianBlur(n, (0, 0), 0.8)


def _vetas():
    r = np.random.default_rng(6)
    n = r.normal(0, 1, (BH, BW)).astype(np.float32)
    v = cv2.filter2D(n, -1, np.eye(41, dtype=np.float32) / 41)
    return v / (v.std() + 1e-6)


_G = {}


def grano():
    if "g" not in _G:
        _G["g"] = _grano_fino()
        _G["v"] = _vetas()
    return _G["g"], _G["v"]


def textura(img, amp_g=0.035, amp_v=0.05):
    """Aspecto de guache: fibra del pincel (vetas diagonales) + grano de papel."""
    g, v = grano()
    f = (1 + amp_g * g + amp_v * v)[..., None]
    img[..., :3] = np.clip(img[..., :3].astype(np.float32) * f, 0, 255).astype(np.uint8)
    return img


def lienzo(c0, c1=None, ang=90.0):
    """RGBA opaco con degradado lineal c0 -> c1 (grados: 90 = de arriba abajo)."""
    c1 = c0 if c1 is None else c1
    yy, xx = np.mgrid[0:BH, 0:BW].astype(np.float32)
    a = math.radians(ang)
    u = (xx / BW * math.cos(a) + yy / BH * math.sin(a))
    u = (u - u.min()) / (u.max() - u.min() + 1e-6)
    out = np.empty((BH, BW, 4), np.uint8)
    for c in range(3):
        out[..., c] = (c0[c] + (c1[c] - c0[c]) * u).astype(np.uint8)
    out[..., 3] = 255
    return out


def vacio():
    return np.zeros((BH, BW, 4), np.uint8)


def banda(img, F, th, col, alfa=1.0, borde=0.07, oscuro=0.0):
    """Mancha pintada: donde F > th se pinta `col`; el borde es de pincel (corto y algo más oscuro si oscuro > 0)."""
    m = np.clip((F - th) / borde, 0, 1)
    if oscuro > 0:
        e = np.clip(1 - np.abs((F - th - borde * 0.5)) / (borde * 0.9), 0, 1) * (m > 0)
        col_b = np.array(col, np.float32) * (1 - oscuro)
        for c in range(3):
            img[..., c] = img[..., c] * (1 - m * alfa) + (col[c] * (1 - e) + col_b[c] * e) * m * alfa
    else:
        for c in range(3):
            img[..., c] = img[..., c] * (1 - m * alfa) + col[c] * m * alfa
    if img.shape[2] == 4:
        img[..., 3] = np.maximum(img[..., 3], (m * alfa * 255)).astype(img.dtype)
    return img


def cosmos(seed, c0, c1, bandas, estrellas=260, brillo=1.0, cols_est=((255, 244, 214), (255, 214, 120), (190, 220, 255))):
    """Fondo espacial pintado: degradado + nubes de color en bandas + estrellas (puntos y destellos de cuatro puntas)."""
    f = lienzo(c0, c1).astype(np.float32)
    for i, (esc, th, col, alfa) in enumerate(bandas):
        F = campo(seed + i * 17, esc, 3)
        banda(f, F, th, col, alfa, 0.09, oscuro=0.12)
    out = textura(np.clip(f, 0, 255).astype(np.uint8))
    out[..., 3] = 255
    r = np.random.default_rng(seed)
    for k in range(estrellas):
        x, y = r.uniform(0, BW), r.uniform(0, BH)
        rad = r.choice([1.2, 1.6, 2.2, 3.0], p=[0.45, 0.3, 0.17, 0.08])
        col = cols_est[r.integers(0, len(cols_est))]
        col = tuple(int(c * brillo) for c in col)
        cv2.circle(out, (int(x * 4), int(y * 4)), int(rad * 4), col + (255,), -1, cv2.LINE_AA, 2)
        if rad > 2.9 and k % 2 == 0:
            L = rad * 5
            P = np.array([(x, y - L), (x + L * .22, y - L * .22), (x + L, y), (x + L * .22, y + L * .22), (x, y + L), (x - L * .22, y + L * .22),
                          (x - L, y), (x - L * .22, y - L * .22)])
            cv2.fillPoly(out, [np.rint(P * 4).astype(np.int32)], col + (255,), cv2.LINE_AA, 2)
    return out


def mancha(img, cx, cy, rx, ry, col, seed=0, rot=0.0, rough=0.10, luz=(-0.5, -0.6), tono=0.72, n=48, alfa=255, brillo=1.12):
    """Forma pintada a guache con la media luna de sombra del estilo (sombra oscura + cuerpo + brillo corrido hacia la luz)."""
    r = np.random.default_rng(seed)
    ph = r.uniform(0, 2 * pi, 4)
    th = np.linspace(0, 2 * pi, n, endpoint=False)
    rad = 1 + rough * (0.6 * np.sin(2 * th + ph[0]) + 0.4 * np.sin(3 * th + ph[1]) + 0.25 * np.sin(5 * th + ph[2]))
    x, y = rx * rad * np.cos(th), ry * rad * np.sin(th)
    c, s = math.cos(rot), math.sin(rot)
    P0 = np.stack([cx + x * c - y * s, cy + x * s + y * c], 1)

    def pintar(P, col_):
        col_ = tuple(int(max(0, min(255, v))) for v in col_)
        cv2.fillPoly(img, [np.rint(P * 4).astype(np.int32)], col_ + (alfa,) if img.shape[2] == 4 else col_, cv2.LINE_AA, 2)
    pintar(P0, [v * tono for v in col])
    d = np.array(luz, float) * min(rx, ry) * 0.16
    C = np.array([cx, cy])
    pintar((P0 - C) * 0.90 + C + d, col)
    pintar((P0 - C) * 0.5 + C + d * 2.2, [v * brillo for v in col])
    return img


def halo_estatico(img, cx, cy, r, col, alfa=0.5, anillos=6):
    """Resplandor pintado en anillos planos concéntricos (no difuminado)."""
    for i in range(anillos):
        k = 1 - i / anillos
        a = alfa * (i + 1) / anillos * 0.55
        ov = img.copy()
        cv2.circle(ov, (int(cx * 4), int(cy * 4)), int(r * k * 4), tuple(int(c) for c in col) + ((255,) if img.shape[2] == 4 else ()), -1,
                   cv2.LINE_AA, 2)
        cv2.addWeighted(ov, a, img, 1 - a, 0, img)
    return img


# ------------------------------------------------------------------ cámara y composición de capas
def vista(capa, z, dx, dy):
    M = np.float32([[z, 0, W / 2 - z * BW / 2 + dx], [0, z, H / 2 - z * BH / 2 + dy]])
    return cv2.warpAffine(capa, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)


def componer(capas, z=1.0, dx=0.0, dy=0.0):
    """capas = [(RGBA, factor_de_paralaje), ...] de lejos a cerca. Devuelve RGB uint8 (H, W, 3)."""
    out = None
    for rgba, f in capas:
        zz = 1 + (z - 1) * f
        v = vista(rgba, zz, dx * f, dy * f)
        if out is None:
            out = np.ascontiguousarray(v[..., :3])
        else:
            a = v[..., 3:4].astype(np.uint16)
            out = ((out.astype(np.uint16) * (255 - a) + v[..., :3].astype(np.uint16) * a) // 255).astype(np.uint8)
    return out


# ------------------------------------------------------------------ efectos dinámicos sobre el cuadro (uint8 RGB)
def _roi(img, x0, y0, x1, y1):
    x0, y0 = max(0, int(x0)), max(0, int(y0))
    x1, y1 = min(W, int(x1)), min(H, int(y1))
    if x1 <= x0 or y1 <= y0:
        return None
    return x0, y0, x1, y1


def disco(img, x, y, r, col, a=1.0):
    q = _roi(img, x - r - 2, y - r - 2, x + r + 2, y + r + 2)
    if q is None or a <= 0.01:
        return
    x0, y0, x1, y1 = q
    roi = img[y0:y1, x0:x1]
    m = np.zeros(roi.shape[:2], np.uint8)
    cv2.circle(m, (int(round((x - x0) * 4)), int(round((y - y0) * 4))), int(max(1, r * 4)), 255, -1, cv2.LINE_AA, 2)
    al = (m.astype(np.float32) * (a / 255.0))[..., None]
    roi[:] = np.clip(roi * (1 - al) + np.array(col, np.float32) * al, 0, 255).astype(np.uint8)


def halo(img, x, y, r, col, a=0.5, anillos=5):
    """Resplandor en anillos planos (guache): cada anillo suma un poco de color hacia el centro."""
    for i in range(anillos):
        k = 1 - i / anillos
        disco(img, x, y, r * k, col, a * 0.42 / anillos * (i + 1) ** 0.8)


def poligono(img, P, col, a=1.0):
    P = np.asarray(P, float)
    q = _roi(img, P[:, 0].min() - 2, P[:, 1].min() - 2, P[:, 0].max() + 2, P[:, 1].max() + 2)
    if q is None or a <= 0.01:
        return
    x0, y0, x1, y1 = q
    roi = img[y0:y1, x0:x1]
    m = np.zeros(roi.shape[:2], np.uint8)
    cv2.fillPoly(m, [np.rint((P - (x0, y0)) * 4).astype(np.int32)], 255, cv2.LINE_AA, 2)
    al = (m.astype(np.float32) * (a / 255.0))[..., None]
    roi[:] = np.clip(roi * (1 - al) + np.array(col, np.float32) * al, 0, 255).astype(np.uint8)


def rayos(img, cx, cy, r0, r1, n, rot, cols, a=1.0, ancho=0.5):
    """Sol de rayos (Big Bang): n triángulos alternando colores, ancho = fracción del sector."""
    for i in range(n):
        a0 = rot + 2 * pi * i / n
        w = pi / n * ancho
        P = [(cx + r0 * math.cos(a0 - w), cy + r0 * math.sin(a0 - w)), (cx + r1 * math.cos(a0), cy + r1 * math.sin(a0)),
             (cx + r0 * math.cos(a0 + w), cy + r0 * math.sin(a0 + w))]
        poligono(img, P, cols[i % len(cols)], a)


def mancha_din(img, cx, cy, rx, ry, col, a=1.0, seed=0, t=0.0, rough=0.12, n=30, rot=0.0):
    """Mancha de pintura que respira (contorno vivo)."""
    th = np.linspace(0, 2 * pi, n, endpoint=False)
    ph = seed * 1.7
    rad = 1 + rough * (np.sin(2 * th + ph + t * 1.3) * 0.6 + np.sin(3 * th - ph * 1.3 + t * 0.9) * 0.4 + 0.2 * np.sin(5 * th + t * 2.1 + ph))
    x, y = rx * rad * np.cos(th), ry * rad * np.sin(th)
    c, s = math.cos(rot), math.sin(rot)
    poligono(img, np.stack([cx + x * c - y * s, cy + x * s + y * c], 1), col, a)


def ruido_tele(img, rect, t, azul=0.06, redondeo=26, brillo=1.0):
    """Estática de tele de tubo dentro de rect=(x0, y0, x1, y1): nieve en bloques de 3x3 px a 12 cuadros/s, esquinas redondeadas."""
    x0, y0, x1, y1 = [int(v) for v in rect]
    w, h = x1 - x0, y1 - y0
    if w < 8 or h < 8:
        return
    r = np.random.default_rng(int(t * 12) * 7919 + 13)
    g = r.random((h // 3 + 1, w // 3 + 1), dtype=np.float32)
    g = cv2.resize(g, (w + 2, h + 2), interpolation=cv2.INTER_NEAREST)[:h, :w]
    band = 0.5 + 0.5 * np.sin((np.arange(h)[:, None] / 38.0) - t * 3.0)
    v = np.clip((0.15 + 0.85 * g) * (0.82 + 0.18 * band) * brillo, 0, 1)
    rgb = np.stack([v * (1 - azul), v, v * (1 + azul)], -1).clip(0, 1)
    m = np.zeros((h, w), np.uint8)
    cv2.rectangle(m, (0, 0), (w - 1, h - 1), 255, -1)
    k = max(3, redondeo)
    m = cv2.GaussianBlur(m, (0, 0), k * 0.35)
    m = (m > 200).astype(np.float32)[..., None]
    cx0, cy0, cx1, cy1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if cx1 <= cx0 or cy1 <= cy0:
        return
    sl = (slice(cy0 - y0, cy1 - y0), slice(cx0 - x0, cx1 - x0))
    roi = img[cy0:cy1, cx0:cx1]
    roi[:] = (roi * (1 - m[sl]) + rgb[sl] * 255 * m[sl]).astype(np.uint8)
