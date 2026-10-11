# -*- coding: utf-8 -*-
"""Post-efectos de cámara ("tomas raras") y transiciones entre escenas.
Todas las funciones reciben/devuelven float32 HxWx3 en [0,1]."""
import math

import cv2
import numpy as np

from motor import W, H, h01, ruido1, e_in, e_out, e_inout, smooth, clamp01

_yy, _xx = np.mgrid[0:H, 0:W].astype(np.float32)
CX, CY = W / 2.0, H / 2.0
_DX, _DY = _xx - CX, _yy - CY
_R = np.sqrt(_DX ** 2 + _DY ** 2)
_A = np.arctan2(_DY, _DX)
RMAX = math.hypot(CX, CY)
NEGRO_F = np.array([20, 16, 24], np.float32) / 255
BLANCO_F = np.array([255, 252, 244], np.float32) / 255


def _remap(img, mx, my, borde=cv2.BORDER_REFLECT):
    return cv2.remap(img, mx.astype(np.float32), my.astype(np.float32), cv2.INTER_LINEAR, borderMode=borde)


# ---------------------------------------------------------------- post-efectos
def ojo_pez(img, k):
    if abs(k) < 1e-3:
        return img
    rn = _R / (CY * 1.25)
    f = 1 - k + k * rn * rn
    return _remap(img, CX + _DX * f, CY + _DY * f)


def ondular(img, t, amp=14.0, lon=90.0):
    if amp < 0.3:
        return img
    mx = _xx + amp * np.sin(_yy / lon + t * 3.1)
    my = _yy + amp * 0.8 * np.sin(_xx / (lon * 1.4) + t * 2.3)
    return _remap(img, mx, my)


def caleido(img, n=6, rot=0.0, mezcla=1.0, zoom=1.0):
    if mezcla < 0.003:
        return img
    seg = 2 * np.pi / n
    a = np.abs(((_A + rot) % seg) - seg / 2) - rot * 0.3
    r = _R / zoom
    out = _remap(img, CX + r * np.cos(a), CY + r * np.sin(a))
    return out if mezcla >= 0.997 else img * (1 - mezcla) + out * mezcla


def planeta(img, rot=0.0, mezcla=1.0):
    """Mini-planeta: el suelo de la imagen se enrolla en un círculo."""
    rp = CY * 1.08
    mx = ((_A + rot + np.pi / 2) % (2 * np.pi)) / (2 * np.pi) * W
    my = H - np.clip(_R / rp, 0, 1.5) * H * 0.92
    out = _remap(img, mx, my, cv2.BORDER_REPLICATE)
    return out if mezcla >= 0.997 else img * (1 - mezcla) + out * mezcla


def tono(img, grados):
    if abs(grados) < 0.5:
        return img
    u8 = np.clip(img * 255, 0, 255).astype(np.uint8)
    hsv = cv2.cvtColor(u8, cv2.COLOR_RGB2HSV)
    hsv[..., 0] = ((hsv[..., 0].astype(np.int32) + int(grados / 2)) % 180).astype(np.uint8)
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2RGB).astype(np.float32) / 255


def warhol(img, t=0.0, mezcla=1.0):
    peq = cv2.resize(img, (W // 2, H // 2), interpolation=cv2.INTER_AREA)
    tiles = [tono(peq, 0 + t * 40), tono(peq, 90 + t * 40), tono(peq, 180 + t * 40), tono(peq, 270 + t * 40)]
    out = np.vstack([np.hstack(tiles[:2]), np.hstack(tiles[2:])])
    # líneas de separación tipo cómic
    out[H // 2 - 4:H // 2 + 4] = NEGRO_F
    out[:, W // 2 - 4:W // 2 + 4] = NEGRO_F
    return out if mezcla >= 0.997 else img * (1 - mezcla) + out * mezcla


def droste(img, niveles=4, k=0.55, rot=0.12, fase=0.0):
    """Imagen dentro de sí misma, con marco blanco (efecto infinito)."""
    out = img.copy()
    cur = img
    for i in range(niveles):
        s = k ** (i + 1 - fase)
        w, h = int(W * s), int(H * s)
        if w < 8:
            break
        M = cv2.getRotationMatrix2D((W / 2, H / 2), math.degrees(rot * (i + 1 - fase)), s)
        capa = cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT)
        uno = cv2.warpAffine(np.ones((H, W), np.float32), M, (W, H), flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_CONSTANT)
        marco = cv2.dilate(uno, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (17, 17)))[..., None]
        mask = uno[..., None]
        out = out * (1 - marco) + BLANCO_F * marco
        out = out * (1 - mask) + np.clip(capa, 0, 1) * mask
    return out


def rgb_split(img, px, ang=0.0):
    if px < 0.4:
        return img
    dx, dy = px * math.cos(ang), px * math.sin(ang)
    r = cv2.warpAffine(np.ascontiguousarray(img[..., 0]), np.float32([[1, 0, dx], [0, 1, dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    b = cv2.warpAffine(np.ascontiguousarray(img[..., 2]), np.float32([[1, 0, -dx], [0, 1, -dy]]), (W, H), borderMode=cv2.BORDER_REFLECT)
    return np.stack([r, img[..., 1], b], -1)


def sacudir(img, dx, dy, rot=0.0, zoom=1.0):
    if abs(dx) < 0.2 and abs(dy) < 0.2 and abs(rot) < 1e-4 and abs(zoom - 1) < 1e-4:
        return img
    M = cv2.getRotationMatrix2D((CX, CY), math.degrees(rot), zoom)
    M[:, 2] += (dx, dy)
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def pixelar(img, bloque):
    if bloque <= 1.5:
        return img
    w, h = max(1, int(W / bloque)), max(1, int(H / bloque))
    peq = cv2.resize(img, (w, h), interpolation=cv2.INTER_AREA)
    return cv2.resize(peq, (W, H), interpolation=cv2.INTER_NEAREST)


def glitch(img, t, amt, seed=0):
    if amt < 0.01:
        return img
    out = img.copy()
    fr = int(t * 15)
    y = 0
    i = 0
    while y < H:
        hh = int(12 + 90 * h01(seed, fr, i))
        if h01(seed + 1, fr, i) < 0.45 * amt + 0.1:
            dx = int((h01(seed + 2, fr, i) - 0.5) * 260 * amt)
            out[y:y + hh] = np.roll(img[y:y + hh], dx, axis=1)
            if h01(seed + 3, fr, i) < 0.3:
                out[y:y + hh] = out[y:y + hh][..., [2, 0, 1]]
        y += hh
        i += 1
    return rgb_split(out, 10 * amt, 0.0)


def espejo(img, vertical=False):
    out = img.copy()
    if vertical:
        out[H // 2:] = img[:H // 2][::-1]
    else:
        out[:, W // 2:] = img[:, :W // 2][:, ::-1]
    return out


def destello(img, a, color=BLANCO_F):
    if a <= 0.003:
        return img
    return img * (1 - a) + color * a


# grano de papel y viñeta (precalculados)
def _grano(seed):
    rng = np.random.default_rng(seed)
    g = rng.normal(0, 1, (H // 2, W // 2)).astype(np.float32)
    g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
    return g


_GRANOS = [_grano(s) for s in range(4)]
_fib = np.random.default_rng(77).normal(0, 1, (H, W)).astype(np.float32)
_FIBRA = cv2.GaussianBlur(_fib, (0, 0), sigmaX=6, sigmaY=0.8) * 3.0
_VIG = (1 - 0.28 * np.clip(_R / RMAX, 0, 1) ** 2.2).astype(np.float32)[..., None]
_VIG2 = np.ascontiguousarray(_VIG[..., 0])
_UNO = np.ones((H, W), np.float32)

try:                                    # grano + fibra + viñeta de `acabado` en un paso con numba (FAB_SIN_NUMBA=1 la apaga)
    import os as _os
    if _os.environ.get("FAB_SIN_NUMBA"):
        raise ImportError
    from numba import njit as _njit, prange as _prange

    @_njit(parallel=True, cache=True)
    def _grano_nb(img, gr, fib, grano, vig, out):
        uno, medio = np.float32(1.0), np.float32(0.5)
        for y in _prange(img.shape[0]):
            for x in range(img.shape[1]):
                f = uno + (gr[y, x] * grano + fib[y, x] * grano * medio)
                v = vig[y, x]
                for ch in range(3):
                    out[y, x, ch] = img[y, x, ch] * f * v
except Exception:
    _grano_nb = None


def bloom(img, fuerza, umbral=0.62):
    """Resplandor de lo luminoso Y saturado (soles, lava, luces de color; no cielos claros ni texto blanco).
    Se calcula a 1/4 de resolución."""
    if fuerza <= 0:
        return img
    peq = cv2.resize(img, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
    mx, mn = peq.max(-1, keepdims=True), peq.min(-1, keepdims=True)
    lum = peq @ np.array([0.3, 0.59, 0.11], np.float32)
    sat = np.clip((mx - mn) / (mx + 1e-4), 0, 1)
    fuente = peq * np.clip((lum[..., None] - umbral) / (1 - umbral), 0, 1) * np.sqrt(sat)
    g = cv2.GaussianBlur(fuente, (0, 0), 9) * 0.65 + cv2.GaussianBlur(fuente, (0, 0), 2.5) * 0.45
    return img + fuerza * cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)


def _papel_tex():
    """Textura de papel para gouache: manchas suaves de pigmento + fibras + pequeñas motas (precalculada)."""
    rng = np.random.default_rng(2026)
    tot = np.zeros((H, W), np.float32)
    for sg, am in ((70, 0.5), (28, 0.35), (9, 0.25)):
        n = rng.normal(0, 1, (H // 4, W // 4)).astype(np.float32)
        n = cv2.resize(n, (W, H), interpolation=cv2.INTER_CUBIC)
        n = cv2.GaussianBlur(n, (0, 0), sg / 4)
        tot += n / (n.std() + 1e-6) * am
    fib = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), sigmaX=1.2, sigmaY=5.0)
    tot += fib / (fib.std() + 1e-6) * 0.35
    mota = (rng.random((H, W)) > 0.9993).astype(np.float32)
    mota = cv2.GaussianBlur(mota, (0, 0), 1.3) * 26
    return (tot * 0.020 - mota * 0.05).astype(np.float32)[..., None]


_PAPEL = None


def acabado(img, boil, grano=None, vineta=None):
    import estilos
    global _PAPEL
    pap = estilos.ACTUAL.get("papel", 0.0)
    if pap > 0:                      # gouache: la textura del papel se ve más en los tonos claros
        if _PAPEL is None:
            _PAPEL = _papel_tex()
        lum = img @ np.array([0.3, 0.59, 0.11], np.float32)
        img = img * (1 + _PAPEL * pap * (0.55 + 0.45 * lum[..., None]))
        img = img * np.array([1.0, 0.985, 0.955], np.float32) + np.array([0.008, 0.004, 0.0], np.float32)
    img = bloom(img, estilos.ACTUAL.get("bloom", 0.0))
    grano = estilos.ACTUAL["grano"] if grano is None else grano
    vineta = estilos.ACTUAL["vineta"] if vineta is None else vineta
    if grano <= 0:
        return img * _VIG if vineta else img
    if _grano_nb is not None and img.dtype == np.float32 and img.shape == (H, W, 3):
        out = np.empty((H, W, 3), np.float32)
        _grano_nb(img, _GRANOS[boil % 4], _FIBRA, np.float32(grano), _VIG2 if vineta else _UNO, out)
        return out
    g = _GRANOS[boil % 4] * grano + _FIBRA * grano * 0.5
    img = img * (1 + g[..., None])
    if vineta:
        img = img * _VIG
    return img


# ---------------------------------------------------------------- transiciones
def _mezcla(A, B, m):
    m = m[..., None] if m.ndim == 2 else m
    return A * (1 - m) + B * m


def _anillo(img, dist, grosor=10.0, color=NEGRO_F):
    m = np.clip(1 - np.abs(dist) / grosor, 0, 1)
    return _mezcla(img, np.broadcast_to(color, img.shape), m)


def tr_iris(A, B, p, seed=0, cx=CX, cy=CY):
    r_all = math.hypot(max(cx, W - cx), max(cy, H - cy)) * 1.05
    dx, dy = _xx - cx, _yy - cy
    rr = np.sqrt(dx * dx + dy * dy)
    aa = np.arctan2(dy, dx)
    if p < 0.5:
        q = e_in(p / 0.5)
        r = (1 - q) * r_all
        src = A
    else:
        q = e_out((p - 0.5) / 0.5)
        r = q * r_all
        src = B
    reff = r * (1 + 0.035 * np.sin(aa * 7 + p * 9))
    d = reff - rr
    m = np.clip(d / 2 + 0.5, 0, 1)
    out = _mezcla(np.broadcast_to(NEGRO_F, A.shape).copy(), src, m)
    return _anillo(out, d, 9, BLANCO_F) if r > 2 else out


def tr_mancha(A, B, p, seed=0):
    q = e_in(p) * 1.25
    r = q * RMAX
    n = np.zeros_like(_A)
    for k, amp in ((3, 0.12), (5, 0.1), (8, 0.07), (13, 0.05), (21, 0.04)):
        n += amp * np.sin(_A * k + 6.28 * h01(seed, k))
    # goterones
    n += 0.35 * np.clip(np.sin(_A * 9 + 6.28 * h01(seed, 99)), 0, 1) ** 12
    d = r * (1 + n) - _R
    m = np.clip(d / 2 + 0.5, 0, 1)
    out = _mezcla(A, B, m)
    return _anillo(out, d, 7, NEGRO_F)


def tr_espiral(A, B, p, seed=0):
    v = (_A / (2 * np.pi) + 0.5) + (_R / RMAX) * 1.6
    f = p * 2.75
    d = (f - v) * 60
    m = np.clip(d, 0, 1)
    out = _mezcla(A, B, m)
    return _anillo(out, d * 3, 8, BLANCO_F)


def tr_glitch(A, B, p, seed=0):
    fr = int(p * 24)
    out = np.empty_like(A)
    y = 0
    i = 0
    s = math.sin(math.pi * p)
    while y < H:
        hh = int(10 + 70 * h01(seed, i, 3))
        ts = 0.25 + 0.5 * h01(seed, i, 5)
        src = B if p > ts else A
        dx = int((h01(seed, i, fr) - 0.5) * 420 * s)
        out[y:y + hh] = np.roll(src[y:y + hh], dx, axis=1)
        if h01(seed + 7, i, fr) < 0.18 * s:
            out[y:y + hh] = out[y:y + hh][..., [1, 2, 0]]
        y += hh
        i += 1
    return rgb_split(out, 24 * s, 0.3)


def _escalar(img, s, rot=0.0, cx=CX, cy=CY):
    M = cv2.getRotationMatrix2D((cx, cy), math.degrees(rot), s)
    return cv2.warpAffine(img, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


def tr_zoom(A, B, p, seed=0, cx=CX, cy=CY):
    qa = e_in(min(1.0, p / 0.62))
    Az = _escalar(A, 1 + 6.5 * qa, 0.7 * qa, cx, cy)
    if qa > 0.1:  # desenfoque radial barato
        Az = (Az + _escalar(A, 1 + 6.5 * qa * 0.93, 0.7 * qa * 0.95, cx, cy)
              + _escalar(A, 1 + 6.5 * qa * 0.86, 0.7 * qa * 0.9, cx, cy)) / 3
    qb = e_out(clamp01((p - 0.38) / 0.62))
    Bz = _escalar(B, 0.22 + 0.78 * qb, -0.6 * (1 - qb))
    w = smooth((p - 0.38) / 0.3)
    return Az * (1 - w) + Bz * w


def tr_persianas(A, B, p, seed=0, periodo=150.0):
    th = 0.6
    u = (_xx * math.cos(th) + _yy * math.sin(th)) / periodo
    loc = u - np.floor(u)
    stagger = (_xx + _yy) / (W + H)
    pp = np.clip((p * 1.6 - stagger * 0.6), 0, 1)
    d = (pp - loc) * periodo
    m = np.clip(d / 1.5 + 0.5, 0, 1)
    out = _mezcla(A, B, m)
    return _anillo(out, d, 3, NEGRO_F)


def tr_derretir(A, B, p, seed=0):
    xs = np.arange(W, dtype=np.float32)
    n = ruido1(xs / 55.0, seed, 1) * 0.35 + ruido1(xs / 13.0, seed, 2) * 0.12
    gotas = np.clip(ruido1(xs / 31.0, seed, 3), 0, 1) ** 3 * 0.9
    off = (e_in(p) * H * (1.25 + n + gotas)).astype(np.float32)
    my = _yy - off[None, :]
    visibleA = my >= 0
    Ashift = cv2.remap(A, _xx, np.maximum(my, 0).astype(np.float32), cv2.INTER_LINEAR, borderMode=cv2.BORDER_REPLICATE)
    d = my
    m = np.clip(0.5 - d / 2, 0, 1)
    out = _mezcla(Ashift, B, m)
    return _anillo(out, d, 6, NEGRO_F)


def tr_ola(A, B, p, seed=0):
    xf = (p * 1.4 - 0.2) * W + 70 * np.sin(_yy / 75 + p * 11) + 25 * np.sin(_yy / 21 - p * 23)
    d = xf - _xx
    m = np.clip(d / 2 + 0.5, 0, 1)
    out = _mezcla(A, B, m)
    espuma = np.clip(1 - np.abs(d - 14) / 14, 0, 1)
    out = _mezcla(out, np.broadcast_to(BLANCO_F, out.shape), espuma)
    return _anillo(out, d + 30, 5, np.array([0.1, 0.45, 0.85], np.float32))


def tr_burbujas(A, B, p, seed=0, n=70):
    mask = np.zeros((H, W), np.uint8)
    ring = np.zeros((H, W), np.uint8)
    for i in range(n):
        cx = int(h01(seed, i, 1) * W)
        cy = int(h01(seed, i, 2) * H)
        d0 = 0.5 * h01(seed, i, 3)
        R0 = 160 + 300 * h01(seed, i, 4)
        q = e_out(clamp01((p - d0) / 0.45))
        r = int(q * R0)
        if r > 0:
            cv2.circle(mask, (cx, cy), r, 255, -1, cv2.LINE_AA)
            cv2.circle(ring, (cx, cy), r, 255, 6, cv2.LINE_AA)
    m = mask.astype(np.float32) / 255
    out = _mezcla(A, B, m)
    rg = ring.astype(np.float32) / 255 * (1 - m * 0.7)
    return _mezcla(out, np.broadcast_to(BLANCO_F, out.shape), rg * 0.9)


def tr_caleido(A, B, p, seed=0):
    s = math.sin(math.pi * p)
    rot = p * 2.4
    z = 1 + 0.5 * s
    ka = caleido(A, 6, rot, mezcla=clamp01(p / 0.45) ** 0.7, zoom=z) if p < 0.58 else None
    kb = caleido(B, 6, rot, mezcla=clamp01((1 - p) / 0.45) ** 0.7, zoom=z) if p > 0.42 else None
    if ka is None:
        src = kb
    elif kb is None:
        src = ka
    else:
        w = smooth((p - 0.42) / 0.16)
        src = ka * (1 - w) + kb * w
    return tono(src, 140 * s)


def tr_pixeles(A, B, p, seed=0):
    s = math.sin(math.pi * p)
    bloque = 1 + 80 * s ** 2
    w = smooth((p - 0.42) / 0.16)
    img = A * (1 - w) + B * w
    return pixelar(img, bloque)


def tr_garabato(A, B, p, seed=0):
    """Rayones de marcador que tapan A y destapan B."""
    mask = np.zeros((H // 2, W // 2), np.uint8)
    filas = 9
    total = filas * 2
    avance = e_inout(p) * total
    pts = []
    for i in range(total + 1):
        fila = i // 2
        x = 40 if i % 2 == 0 else W // 2 - 40
        if fila % 2 == 1:
            x = W // 2 - x
        y = int((fila + 0.5 + 0.3 * (i % 2)) * (H // 2) / filas)
        pts.append((x + int(20 * (h01(seed, i) - 0.5)), y))
    pts = np.array(pts, np.float32)
    k = int(avance)
    fr = avance - k
    seg = list(pts[:k + 1])
    if k + 1 < len(pts):
        seg.append(pts[k] + (pts[k + 1] - pts[k]) * fr)
    if len(seg) >= 2:
        cv2.polylines(mask, [np.array(seg, np.int32)], False, 255, int(H / 2 / filas * 1.35), cv2.LINE_AA)
    m = cv2.resize(mask, (W, H), interpolation=cv2.INTER_LINEAR).astype(np.float32) / 255
    borde = np.clip(cv2.Laplacian(m, cv2.CV_32F, ksize=3) * -4, 0, 1)
    out = _mezcla(A, B, m)
    return _mezcla(out, np.broadcast_to(NEGRO_F, out.shape), borde)


def tr_fundido(A, B, p, seed=0):
    """Fundido cruzado suave con un leve acercamiento (documental)."""
    u = smooth(p)
    Az = _escalar(A, 1 + 0.04 * u) if u > 0.02 else A
    Bz = _escalar(B, 1.04 - 0.04 * u) if u < 0.98 else B
    return Az * (1 - u) + Bz * u


def tr_zoom_suave(A, B, p, seed=0, cx=CX, cy=CY):
    """Acercamiento hacia el centro de A que se funde con B saliendo de lejos (sin desenfoque radial)."""
    Az = _escalar(A, 1 + 2.2 * e_in(min(1.0, p / 0.7)), 0.0, cx, cy)
    Bz = _escalar(B, 0.7 + 0.3 * e_out(clamp01((p - 0.3) / 0.7)), 0.0, cx, cy)
    w = smooth((p - 0.3) / 0.45)
    return Az * (1 - w) + Bz * w


def tr_bajada(A, B, p, seed=0):
    """Paneo vertical: la cámara baja (A sale por arriba, B entra desde abajo)."""
    u = e_inout(p)
    off = int(round(u * H))
    out = np.empty_like(A)
    out[:H - off] = A[off:]
    out[H - off:] = B[:off]
    return out


def tr_paneo(A, B, p, seed=0):
    """Paneo horizontal de cámara: A sale por la izquierda y B entra por la derecha, con un leve alejamiento
    en el medio (la cámara viaja) y desenfoque de movimiento suave."""
    u = e_inout(p)
    off = int(round(u * W))
    out = np.empty_like(A)
    out[:, :W - off] = A[:, off:]
    out[:, W - off:] = B[:, :off]
    v = abs(math.sin(math.pi * p))          # 0 en los extremos, 1 en el punto de mayor velocidad
    k = int(v * 22) * 2 + 1
    if k > 3:
        out = cv2.blur(out, (k, 1))
    z = 1.0 - 0.05 * v
    return _escalar(out, z) if z < 0.998 else out


TRANSICIONES = dict(iris=tr_iris, mancha=tr_mancha, espiral=tr_espiral, glitch=tr_glitch, zoom=tr_zoom,
                    persianas=tr_persianas, derretir=tr_derretir, ola=tr_ola, burbujas=tr_burbujas,
                    caleido=tr_caleido, pixeles=tr_pixeles, garabato=tr_garabato,
                    fundido=tr_fundido, zoom_suave=tr_zoom_suave, bajada=tr_bajada, paneo=tr_paneo,
                    continua=lambda A, B, p, seed=0: B)   # plano secuencia (render.py la salta)
