# -*- coding: utf-8 -*-
"""ESTILO «pergamino» (cartógrafo de pergamino) del kit de Crónicas de Warcraft — motor. API: nucleo/mg_wow_estilos.py.
Adaptado de videos/_kit_wow_estilos/estilo_1/estilo_1.py (22-nov-2026): pergamino quemado, tinta sepia, letra caligráfica
(Monotype Corsiva), sellos de lacre que caen y se aplastan, ruta de pluma punteada que se entinta, fotos pegadas.
Las piezas devuelven fn(dt, dur, marcas) -> BGRA (lienzo local con alfa; el mapa, cuadro entero opaco)."""
import math
import os

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

from . import comun as C

W, H = 1920, 1080
FUENTES = r'C:\Windows\Fonts'

# ----------------------------------------------------------------------------- utilidades (copiadas de la demo)
# Paleta (RGB 0-255)
TINTA = (44, 28, 17)
TINTA_HUM = (96, 60, 30)
TINTA_ROJA = (158, 32, 24)
LACRE = (146, 22, 24)
PAPEL_CL = (238, 221, 182)
PAPEL_OS = (200, 168, 116)
HALO = (241, 226, 190)
BRASA = np.array([1.0, 0.55, 0.12], np.float32)
CARBON = np.array([0.10, 0.06, 0.03], np.float32)
CALI = 'MTCORSVA.TTF'      # Monotype Corsiva = letra caligráfica
LETRA_SELLO = 'BOOKOSB.TTF'


# ----------------------------------------------------------------------------- utilidades
def cl(u):
    return 0.0 if u < 0 else 1.0 if u > 1 else float(u)


def seg(t, a, b):
    return cl((t - a) / (b - a))


def eo(u):
    u = cl(u); return 1 - (1 - u) ** 3


def eio(u):
    u = cl(u); return u * u * (3 - 2 * u)


def eback(u, s=1.6):
    u = cl(u) - 1; return 1 + (s + 1) * u ** 3 + s * u ** 2


def lerp(a, b, u):
    return a + (b - a) * u


_FC = {}


def fuente(nombre, tam):
    k = (nombre, tam)
    if k not in _FC:
        _FC[k] = ImageFont.truetype(os.path.join(FUENTES, nombre), tam)
    return _FC[k]


def ruido(h, w, escala, seed, octavas=4):
    """Ruido fractal 0..1 (rejillas aleatorias reescaladas)."""
    rng = np.random.default_rng(seed)
    out = np.zeros((h, w), np.float32); amp = 1.0; tot = 0.0; e = float(escala)
    for _ in range(octavas):
        gh = max(2, int(h / e) + 2); gw = max(2, int(w / e) + 2)
        g = rng.random((gh, gw)).astype(np.float32)
        out += amp * cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC)
        tot += amp; amp *= 0.5; e = max(1.5, e / 2)
    out /= tot
    return (out - out.min()) / (out.max() - out.min() + 1e-6)


def premul(rgb, a):
    return np.dstack([rgb * a[..., None], a]).astype(np.float32)


def spr_pil(im):
    a = np.asarray(im.convert('RGBA'), np.float32) / 255.0
    a[..., :3] *= a[..., 3:4]
    return a


def pegar(dst, s, x, y, alfa=1.0):
    """Compone el sprite premultiplicado s (h,w,4) con su esquina en (x,y). dst = RGB (h,w,3) o RGBA premult (h,w,4)."""
    if s is None or alfa <= 0.002:
        return
    x = int(round(x)); y = int(round(y)); h, w = s.shape[:2]
    x0, y0 = max(0, x), max(0, y); x1, y1 = min(dst.shape[1], x + w), min(dst.shape[0], y + h)
    if x1 <= x0 or y1 <= y0:
        return
    ss = s[y0 - y:y1 - y, x0 - x:x1 - x]
    if alfa < 1:
        ss = ss * alfa
    d = dst[y0:y1, x0:x1]
    if dst.shape[2] == 4:
        d *= (1 - ss[..., 3:4]); d += ss
    else:
        d *= (1 - ss[..., 3:4]); d += ss[..., :3]


def pegar_c(dst, s, cx, cy, alfa=1.0):
    pegar(dst, s, cx - s.shape[1] / 2, cy - s.shape[0] / 2, alfa)


def transformar(s, ang=0.0, sx=1.0, sy=None):
    """Gira (grados, + = antihorario) y escala un sprite premultiplicado. Devuelve (sprite, M 2x3)."""
    sy = sx if sy is None else sy
    h, w = s.shape[:2]
    a = math.radians(ang); ca, sa = math.cos(a), math.sin(a)
    A = np.array([[ca * sx, sa * sy], [-sa * sx, ca * sy]], np.float64)
    co = np.array([[0, 0], [w, 0], [0, h], [w, h]], np.float64) - [w / 2, h / 2]
    tc = co @ A.T
    nw = int(math.ceil(tc[:, 0].max() - tc[:, 0].min())) + 2
    nh = int(math.ceil(tc[:, 1].max() - tc[:, 1].min())) + 2
    t = np.array([nw / 2, nh / 2]) - A @ np.array([w / 2, h / 2])
    M = np.hstack([A, t[:, None]])
    out = cv2.warpAffine(s, M, (nw, nh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return out, M


def sombra(s, blur=8, op=0.55):
    a = cv2.GaussianBlur(s[..., 3], (0, 0), blur) * op
    return np.dstack([np.zeros(a.shape + (3,), np.float32), a])


def lut_grad(paradas):
    x = np.linspace(0, 1, 256)
    ps = [p for p, _ in paradas]
    out = np.zeros((256, 3), np.float32)
    for c in range(3):
        out[:, c] = np.interp(x, ps, [col[c] / 255.0 for _, col in paradas])
    return out


SEPIA = lut_grad([(0, (52, 34, 20)), (0.45, (150, 108, 62)), (1, (240, 222, 182))])
SEPIA_JUEGO = lut_grad([(0, (26, 16, 9)), (0.5, (140, 98, 56)), (1, (238, 212, 162))])


def disco(r):
    return cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * r + 1, 2 * r + 1))


# ----------------------------------------------------------------------------- papel, quemado, tinta
def papel(h, w, seed, claro=PAPEL_CL, oscuro=PAPEL_OS):
    n1 = ruido(h, w, max(h, w) / 3, seed, 3)
    n2 = ruido(h, w, 80, seed + 1, 3)
    n3 = ruido(h, w, 9, seed + 2, 2)
    t = np.clip((0.5 * n1 + 0.35 * n2 + 0.15 * n3 - 0.18) / 0.7, 0, 1)
    a = np.array(oscuro, np.float32) / 255; b = np.array(claro, np.float32) / 255
    img = a + (b - a) * t[..., None]
    sp = ruido(h, w, 45, seed + 4, 3)
    man = np.clip((sp - 0.74) / 0.12, 0, 1) * 0.12
    img *= (1 - man[..., None] * np.array([0.5, 0.85, 1.3], np.float32))
    fib = np.zeros((h, w), np.float32)
    rng = np.random.default_rng(seed + 5)
    for _ in range(int(h * w / 7000)):
        x, y = rng.uniform(0, w), rng.uniform(0, h); L = rng.uniform(8, 36); an = rng.uniform(0, math.pi)
        cv2.line(fib, (int(x), int(y)), (int(x + L * math.cos(an)), int(y + L * math.sin(an))), 1.0, 1)
    fib = cv2.GaussianBlur(fib, (0, 0), 0.7)
    img *= (1 - 0.06 * fib[..., None])
    return np.clip(img, 0, 1).astype(np.float32)


def quemar_bordes(img, seed, ancho=36, carbon=14, chamusca=90):
    """Bordes quemados irregulares: devuelve sprite premultiplicado (h,w,4)."""
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
    nz = 0.75 * ruido(h, w, 80, seed, 4) + 0.25 * ruido(h, w, 12, seed + 9, 2)
    dd = d - nz * ancho - 2
    alfa = np.clip(dd / 1.4, 0, 1)
    ch = np.clip(1 - dd / carbon, 0, 1) ** 0.8
    sc = np.clip(1 - dd / chamusca, 0, 1) ** 1.7
    img = img * (1 - 0.55 * sc[..., None] * np.array([0.45, 0.72, 1.0], np.float32))
    img = img * (1 - ch[..., None]) + CARBON * ch[..., None]
    return premul(img, alfa)


def borde_rasgado(img, seed, ancho=10):
    """Bordes de papel rasgado (sin quemar), un poco oscurecidos."""
    h, w = img.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
    nz = 0.6 * ruido(h, w, 30, seed, 3) + 0.4 * ruido(h, w, 5, seed + 3, 2)
    dd = d - nz * ancho - 1
    alfa = np.clip(dd / 1.2, 0, 1)
    sc = np.clip(1 - dd / 40, 0, 1) ** 1.5
    img = img * (1 - 0.35 * sc[..., None] * np.array([0.5, 0.75, 1.0], np.float32))
    return premul(img, alfa)


def campo_mancha(h, w, seed, cx=0.5, cy=0.5, mezcla=0.38, escala=None):
    """Campo 0..1 para manchas/quemaduras que crecen desde (cx, cy) con borde irregular."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    r = np.hypot((xx - cx * w) / max(w, h), (yy - cy * h) / max(w, h))
    r = r / r.max()
    nz = ruido(h, w, escala or max(h, w) / 5, seed, 4)
    return ((1 - mezcla) * r + mezcla * nz).astype(np.float32)


def revelar(campo, p, suave=0.06):
    return np.clip((p * (1 + suave + 0.02) - campo) / suave, 0, 1)


def quemar_spr(s, campo, p):
    """Salida: el sprite se quema (borde de brasa que avanza) según p 0..1."""
    if p <= 0:
        return s
    th = p * 1.18 - 0.08
    d = campo - th
    keep = np.clip(d / 0.006, 0, 1)
    ch = np.clip(1 - d / 0.08, 0, 1) ** 1.5 * keep
    a0 = s[..., 3]
    glow = np.exp(-(np.maximum(d, 0) / 0.008) ** 2) * np.clip(1 + d / 0.005, 0, 1) * (a0 > 0.05) * 0.9
    out = s * keep[..., None]
    out[..., :3] = out[..., :3] * (1 - 0.88 * ch[..., None]) + CARBON * (0.88 * ch * out[..., 3])[..., None]
    g = glow * a0
    out[..., :3] += BRASA * g[..., None]
    out[..., 3] = np.maximum(out[..., 3], g)
    out[..., :3] = np.minimum(out[..., :3], out[..., 3:4])
    return out


# ----------------------------------------------------------------------------- texto caligráfico
def texto(txt, tam, fnt=CALI, color=TINTA, halo=None, halo_r=9, halo_a=0.82, seed=0):
    """Sprite de texto en tinta. ' · ' se dibuja como rombo de tinta. halo = color de papel detrás (para leer sobre el mapa)."""
    F = fuente(fnt, tam)
    txt = txt.replace("'", "’")                    # Corsiva: el apóstrofo recto casi no se ve
    partes = [p.strip() for p in txt.split('·')]
    tmp = ImageDraw.Draw(Image.new('L', (4, 4)))
    gap = int(tam * 0.8)
    anchos = [tmp.textlength(p, font=F) for p in partes]
    total = sum(anchos) + gap * (len(partes) - 1)
    asc, desc = F.getmetrics()
    pad = int(tam * 0.35) + halo_r
    Wc = int(total + 2 * pad); Hc = int(asc + desc + 2 * pad)
    m = Image.new('L', (Wc, Hc), 0); d = ImageDraw.Draw(m)
    ref = 'H' if sum(c.isupper() for c in txt) > sum(c.islower() for c in txt) else 'x'
    bb = d.textbbox((0, pad), ref, font=F); cy = (bb[1] + bb[3]) / 2
    x = pad
    for i, p in enumerate(partes):
        d.text((x, pad), p, font=F, fill=255); x += anchos[i]
        if i < len(partes) - 1:
            cx = x + gap * 0.56; rr = max(3, tam * 0.09)
            d.polygon([(cx, cy - rr * 1.35), (cx + rr, cy), (cx, cy + rr * 1.35), (cx - rr, cy)], fill=255)
            x += gap
    a = np.asarray(m, np.float32) / 255
    a = cv2.GaussianBlur(a, (0, 0), 0.45)
    a = a * (0.84 + 0.16 * ruido(Hc, Wc, 7, seed + 77, 2))
    col = np.array(color, np.float32) / 255
    out = premul(np.broadcast_to(col, a.shape + (3,)).copy(), a)
    if halo is not None:
        ha = cv2.dilate((a > 0.08).astype(np.float32), disco(max(1, halo_r // 2)))
        ha = np.clip(cv2.GaussianBlur(ha, (0, 0), halo_r * 0.7) * 1.3, 0, 1) * halo_a
        base = premul(np.broadcast_to(np.array(halo, np.float32) / 255, ha.shape + (3,)).copy(), ha)
        out = out + base * (1 - out[..., 3:4])
    return out.astype(np.float32)


def escribir(s, p, suave=34):
    """Revela el sprite de izquierda a derecha como si se escribiera; el frente queda más claro (tinta húmeda)."""
    if p >= 1:
        return s
    if p <= 0:
        return None
    w = s.shape[1]
    x = np.arange(w, dtype=np.float32)
    edge = p * (w + suave)
    m = np.clip((edge - x) / suave, 0, 1)
    out = s * m[None, :, None]
    hum = np.clip(1 - (edge - x) / (suave * 2.5), 0, 1) * (m > 0)
    col = np.array(TINTA_HUM, np.float32) / 255 - np.array(TINTA, np.float32) / 255
    out[..., :3] += (col[None, None, :] * (hum[None, :, None] * out[..., 3:4])) * 0.8
    return np.clip(out, 0, 1)


# ----------------------------------------------------------------------------- lacre, pluma, rosa, cinta
def sello(r, letra=None, seed=0, base=LACRE):
    """Sello de lacre con relieve (mapa de alturas + luz). Devuelve sprite premultiplicado."""
    S = int(r * 2.9); c = S / 2
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
    dx, dy = xx - c, yy - c
    dist = np.hypot(dx, dy); ang = np.arctan2(dy, dx)
    rng = np.random.default_rng(seed)
    rr = np.full_like(dist, r)
    for k in range(2, 10):
        rr += r * rng.uniform(0.008, 0.03) * 2.0 / k * np.sin(k * ang + rng.uniform(0, 6.28))
    for _ in range(3):
        a0 = rng.uniform(0, 6.28); wd = rng.uniform(0.12, 0.3); hh = rng.uniform(0.07, 0.17) * r
        da = np.angle(np.exp(1j * (ang - a0)))
        rr += hh * np.exp(-(da / wd) ** 2)
    blob = np.clip(rr - dist + 0.5, 0, 1)
    dt = np.clip((rr - dist) / (0.30 * r), 0, 1)
    hgt = np.sqrt(dt)
    if letra is not None:
        rin = 0.66 * r
        rim = np.exp(-((dist - rin) / (0.075 * r)) ** 2)
        inner = np.clip((rin - dist) / (0.04 * r), 0, 1)
        hgt = hgt * 0.85 + 0.38 * rim - 0.22 * inner
        # cuentas alrededor del disco
        cu = np.zeros_like(dist)
        for k in range(20):
            a = k / 20 * 2 * math.pi
            cu += np.exp(-(((xx - c - 0.82 * r * math.cos(a)) ** 2 + (yy - c - 0.82 * r * math.sin(a)) ** 2) / (0.045 * r) ** 2))
        hgt += 0.12 * cu
        if letra:
            m = Image.new('L', (S, S), 0); d = ImageDraw.Draw(m)
            F = fuente(LETRA_SELLO, int(r * 1.0))
            bb = d.textbbox((0, 0), letra, font=F)
            d.text((c - (bb[0] + bb[2]) / 2, c - (bb[1] + bb[3]) / 2), letra, font=F, fill=255)
            em = cv2.GaussianBlur(np.asarray(m, np.float32) / 255, (0, 0), max(0.6, r * 0.02))
            hgt += 0.34 * em * inner
    hgt = cv2.GaussianBlur(hgt.astype(np.float32), (0, 0), max(0.7, r * 0.018))
    gx = cv2.Sobel(hgt, cv2.CV_32F, 1, 0, ksize=3) * r * 0.10
    gy = cv2.Sobel(hgt, cv2.CV_32F, 0, 1, ksize=3) * r * 0.10
    n = np.dstack([-gx, -gy, np.ones_like(gx)]); n /= np.linalg.norm(n, axis=2, keepdims=True)
    L = np.array([-0.5, -0.6, 0.62]); L /= np.linalg.norm(L)
    Hh = L + np.array([0, 0, 1.0]); Hh /= np.linalg.norm(Hh)
    diff = np.clip((n * L).sum(-1), 0, 1)
    spec = np.clip((n * Hh).sum(-1), 0, 1) ** 36
    col = np.array(base, np.float32) / 255 * (0.28 + 0.95 * diff)[..., None] + spec[..., None] * np.array([1, 0.86, 0.8]) * 0.6
    col *= (0.9 + 0.2 * ruido(S, S, max(3, r * 0.4), seed + 1, 2))[..., None]
    return premul(np.clip(col, 0, 1).astype(np.float32), blob)


def pluma():
    """Pluma de ave dibujada (sprite vertical, punta abajo). Devuelve (sprite, punta_xy, cima_xy) a escala final."""
    k = 3; w, h = 130 * k, 430 * k
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx = w / 2
    izq, der = [], []
    for i in range(60):
        u = i / 59; y = (30 + 300 * u) * k
        wv = math.sin(math.pi * u) ** 0.75
        izq.append((cx - (40 * wv + 2) * k - 6 * k * u, y)); der.append((cx + (26 * wv + 2) * k - 4 * k * u, y))
    d.polygon(izq + der[::-1], fill=(236, 228, 210, 255))
    d.polygon([(cx, 30 * k)] + izq[1:] + [(cx - 6 * k, 330 * k)], fill=(214, 204, 184, 255))
    for i in range(4, 58, 2):
        u = i / 59; y = (30 + 300 * u) * k; wv = math.sin(math.pi * u) ** 0.75
        d.line([(cx - 2 * k * u, y), (cx - (40 * wv) * k - 6 * k * u, y - 26 * k)], fill=(150, 140, 122, 255), width=k)
        d.line([(cx - 2 * k * u, y), (cx + (26 * wv) * k - 4 * k * u, y - 20 * k)], fill=(170, 160, 142, 255), width=k)
    d.line([(cx, 18 * k), (cx - 6 * k, 340 * k), (cx - 7 * k, 400 * k)], fill=(248, 244, 232, 255), width=4 * k)
    d.polygon([(cx - 10 * k, 360 * k), (cx - 4 * k, 360 * k), (cx - 7 * k, 422 * k)], fill=(40, 26, 16, 255))
    im = im.resize((w // k, h // k), Image.LANCZOS)
    return spr_pil(im), np.array([cx / k - 7, 421.0]), np.array([cx / k, 18.0])


def rosa_vientos(R=115):
    k = 2; S = int(R * 2.5) * k; c = S / 2; r = R * k
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    ink = TINTA + (255,); claro = (236, 220, 182, 235)
    d.ellipse([c - r * 0.98, c - r * 0.98, c + r * 0.98, c + r * 0.98], outline=ink, width=3 * k)
    d.ellipse([c - r * 0.9, c - r * 0.9, c + r * 0.9, c + r * 0.9], outline=ink, width=k)
    for i in range(72):
        a = i / 72 * 2 * math.pi; l = 0.08 if i % 9 == 0 else 0.04
        d.line([(c + r * 0.9 * math.cos(a), c + r * 0.9 * math.sin(a)),
                (c + r * (0.9 - l) * math.cos(a), c + r * (0.9 - l) * math.sin(a))], fill=ink, width=k)
    def punta(a, L, wd, rojo=False):
        tip = (c + r * L * math.cos(a), c + r * L * math.sin(a))
        p1 = (c + r * wd * math.cos(a + math.pi / 2), c + r * wd * math.sin(a + math.pi / 2))
        p2 = (c + r * wd * math.cos(a - math.pi / 2), c + r * wd * math.sin(a - math.pi / 2))
        d.polygon([(c, c), tip, p1], fill=claro, outline=ink)
        d.polygon([(c, c), tip, p2], fill=(TINTA_ROJA + (255,)) if rojo else ink, outline=ink)
    for i in range(4):
        punta(math.pi / 4 + i * math.pi / 2, 0.58, 0.10)
    for i in range(4):
        punta(-math.pi / 2 + i * math.pi / 2, 0.86, 0.13, rojo=(i == 0))
    d.ellipse([c - 6 * k, c - 6 * k, c + 6 * k, c + 6 * k], fill=ink)
    F = fuente('BOOKOSB.TTF', int(R * 0.30) * k)
    bb = d.textbbox((0, 0), 'N', font=F)
    d.text((c - (bb[0] + bb[2]) / 2, c - r * 1.02 - (bb[3] - bb[1]) - bb[1] - 4 * k), 'N', font=F, fill=ink)
    im = im.resize((S // k, S // k), Image.LANCZOS)
    return spr_pil(im)


def cinta(ancho, alto=104, seed=3):
    """Cinta/filacteria de pergamino con colas plegadas (sin texto)."""
    k = 2; Wc, Hc = (ancho + 160) * k, (alto + 50) * k
    pap = papel(Hc, Wc, seed)
    pap_os = pap * np.array([0.78, 0.72, 0.62], np.float32)
    def mascara(poly):
        m = Image.new('L', (Wc, Hc), 0); ImageDraw.Draw(m).polygon([(x * k, y * k) for x, y in poly], fill=255)
        return np.asarray(m, np.float32) / 255
    a0, a1 = 80, 80 + ancho; t0, t1 = 8, 8 + alto
    cola_i = [(0, 30), (a0 + 22, 30), (a0 + 22, t1 + 34), (0, t1 + 34), (30, (30 + t1 + 34) / 2)]
    cola_d = [(a1 + 160, 30), (a1 - 22, 30), (a1 - 22, t1 + 34), (a1 + 160, t1 + 34), (a1 + 130, (30 + t1 + 34) / 2)]
    pli_i = [(a0, t1), (a0 + 22, t1 + 34), (a0 + 22, t1)]
    pli_d = [(a1, t1), (a1 - 22, t1 + 34), (a1 - 22, t1)]
    banda = []
    for i in range(41):
        u = i / 40; banda.append((a0 + u * ancho, t0 + 10 * math.sin(math.pi * u) * -1 + 10))
    for i in range(41):
        u = 1 - i / 40; banda.append((a0 + u * ancho, t1 + 10 * math.sin(math.pi * u) * -1 + 0))
    out = np.zeros((Hc, Wc, 4), np.float32)
    for poly, col in [(cola_i, pap_os), (cola_d, pap_os), (pli_i, pap_os * 0.7), (pli_d, pap_os * 0.7), (banda, pap)]:
        m = mascara(poly)
        out = premul(col, m) + out * (1 - m[..., None])
    # contornos de tinta
    lin = Image.new('L', (Wc, Hc), 0); dl = ImageDraw.Draw(lin)
    for poly in (cola_i, cola_d, banda):
        dl.line([(x * k, y * k) for x, y in poly] + [(poly[0][0] * k, poly[0][1] * k)], fill=255, width=3 * k)
    la = cv2.GaussianBlur(np.asarray(lin, np.float32) / 255, (0, 0), 0.8)
    ink = premul(np.broadcast_to(np.array(TINTA, np.float32) / 255, la.shape + (3,)).copy(), la)
    out = ink + out * (1 - la[..., None])
    out = cv2.resize(out, (Wc // k, Hc // k), interpolation=cv2.INTER_AREA)
    return out, (a0 + ancho / 2, t0 + alto / 2 + 5)


def trazo_cv(canvas, pts, grosor, color, alfa=1.0):
    """Traza una polilínea con grosor variable (lista) sobre un canvas uint8 RGBA (premult implícito con LINE_AA)."""
    col = tuple(int(c) for c in color) + (int(255 * alfa),)
    for i in range(len(pts) - 1):
        g = max(1, int(round(grosor[i])))
        p1 = (int(pts[i][0] * 16), int(pts[i][1] * 16)); p2 = (int(pts[i + 1][0] * 16), int(pts[i + 1][1] * 16))
        cv2.line(canvas, p1, p2, col, g, cv2.LINE_AA, 4)


def rubrica(L=480, A=16):
    """Puntos y grosores de una rúbrica caligráfica (línea ondulada con remates)."""
    pts, gr = [], []
    n = 140
    for i in range(n):
        s = i / (n - 1)
        x = L * (s - 0.5)
        y = A * math.sin(2 * math.pi * s * 1.5) * math.sin(math.pi * s)
        pts.append((x, y))
        gr.append(1.2 + 4.2 * math.sin(math.pi * s) ** 0.8)
    return np.array(pts), np.array(gr)


def circulo_mano(rx, ry, seed=1):
    rng = np.random.default_rng(seed)
    f = rng.uniform(0, 6.28); n = 160; pts = []; gr = []
    a0 = -2.4
    for i in range(n):
        s = i / (n - 1); a = a0 + s * 2 * math.pi * 1.1
        k = 1 + 0.035 * math.sin(3 * a + f) + 0.07 * s
        pts.append((rx * k * math.cos(a), ry * k * math.sin(a)))
        gr.append(2.0 + 4.5 * math.sin(math.pi * min(1, s * 1.05)) ** 0.6)
    return np.array(pts), np.array(gr)


def dibujar_trazo(dst, pts, gr, p, ox, oy, color=TINTA, alfa=1.0):
    """Dibuja la fracción p de un trazo (pts relativos a ox,oy) sobre dst (RGB o RGBA premult)."""
    if p <= 0:
        return
    n = max(2, int(len(pts) * cl(p)))
    P = pts[:n] + [ox, oy]
    x0, y0 = np.floor(P.min(0) - 12).astype(int); x1, y1 = np.ceil(P.max(0) + 12).astype(int)
    cv = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
    trazo_cv(cv, P - [x0, y0], gr[:n], color, alfa)
    pegar(dst, cv.astype(np.float32) / 255, x0, y0)


def foto_pegada(ruta, ancho, ang=0.0, tono=0.5, margen=14, seed=0, arco=False):
    """Foto real recortada sobre papel con bordes rasgados, viraje sepia parcial; girada."""
    im = Image.open(ruta).convert('RGB')
    h = int(ancho * im.height / im.width)
    f = np.asarray(im.resize((ancho, h), Image.LANCZOS), np.float32) / 255
    g = cv2.cvtColor((f * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    f = f * (1 - tono) + SEPIA[g] * tono
    f = f * (0.92 + 0.08 * ruido(h, ancho, 40, seed, 2))[..., None]
    Wp, Hp = ancho + 2 * margen, h + 2 * margen
    base = papel(Hp, Wp, seed + 30)
    base[margen:margen + h, margen:margen + ancho] = f
    # filete de tinta alrededor de la foto
    cv2.rectangle(base, (margen - 3, margen - 3), (margen + ancho + 2, margen + h + 2), tuple(np.array(TINTA) / 255.0), 2, cv2.LINE_AA)
    s = borde_rasgado(base, seed + 31, ancho=8)
    return transformar(s, ang)[0]


# ----------------------------------------------------------------------------- caída de sellos
class Caida:
    """Sello de lacre que cae, se aplasta y suelta gotas."""
    def __init__(self, r, letra, seed, t0, dur=0.26, gotas=7):
        self.spr = sello(r, letra, seed)
        self.sh = sombra(self.spr, blur=max(3, r * 0.12), op=0.6)
        self.t0, self.dur, self.r = t0, dur, r
        rng = np.random.default_rng(seed + 100)
        self.gotas = []
        for i in range(gotas):
            a = rng.uniform(0, 2 * math.pi); dd = r * rng.uniform(1.05, 1.6); rg = max(3, r * rng.uniform(0.07, 0.15))
            self.gotas.append((a, dd, sello(rg, None, seed + 200 + i)))

    def impacto(self, t):
        return t - self.t0 - self.dur

    def dibuja(self, dst, X, Y, t):
        dt = t - self.t0
        if dt < 0:
            return
        if dt < self.dur:
            u = dt / self.dur; e = u * u
            esc = 2.3 - 1.3 * e; alfa = min(1.0, u * 3); off = (1 - e) * 46 + 5; sx = sy = esc
        else:
            v = dt - self.dur
            q = 0.22 * math.exp(-v * 9) * math.cos(v * 30)
            sx, sy = 1 + q, 1 - q; esc = 1.0; alfa = 1.0; off = 5
            for a, dd, g in self.gotas:
                k = eo(min(1.0, v / 0.16))
                pegar_c(dst, g, X + math.cos(a) * dd * k, Y + math.sin(a) * dd * k * 0.92)
        sh, _ = transformar(self.sh, 0, sx * esc * 1.05, sy * esc * 1.05)
        pegar_c(dst, sh, X + off * 0.6, Y + off, alfa * 0.9)
        sp, _ = transformar(self.spr, 0, sx, sy) if (sx != 1 or sy != 1) else (self.spr, None)
        pegar_c(dst, sp, X, Y, alfa)


def sacudida(t, impactos, A=5.0):
    dx = dy = 0.0
    for ti in impactos:
        v = t - ti
        if 0 <= v < 0.35:
            k = A * math.exp(-v * 14)
            dx += k * math.sin(v * 90); dy += k * math.cos(v * 70)
    return dx, dy

# ----------------------------------------------------------------------------- 2) FICHA (pergamino enrollado)
def rodillo(alto_papel, r=27):
    hh = alto_papel + 40; Wc = 2 * r + 30; Hc = hh + 2 * 34
    out = np.zeros((Hc, Wc, 4), np.float32)
    x = np.arange(Wc, dtype=np.float32) - Wc / 2
    prof = np.clip(1 - (x / r) ** 2, 0, 1)
    cuerpo = (np.abs(x) <= r).astype(np.float32)
    pap = np.array(PAPEL_CL, np.float32) / 255
    col = pap * (0.45 + 0.6 * np.sqrt(prof))[:, None]
    col = col * (0.95 + 0.1 * ruido(1, Wc, 6, 4, 1)[0])[:, None]
    body = np.broadcast_to(col, (hh, Wc, 3)).copy()
    for k in range(5):  # capas del rollo
        yk = 4 + k * 3
        body[yk:yk + 1] *= 0.75; body[hh - yk - 1:hh - yk] *= 0.75
    out[34:34 + hh] = premul(body, np.broadcast_to(cuerpo, (hh, Wc)).copy())
    # pomos de madera
    yy, xx = np.mgrid[0:40, 0:Wc].astype(np.float32)
    for cy0 in (16, Hc - 24):
        pm = np.zeros((Hc, Wc), np.float32)
        d = np.hypot((xx - Wc / 2) / (r * 0.72), (yy - 20) / 17)
        a = np.clip((1 - d) * 12, 0, 1)
        lum = np.clip(1 - np.hypot((xx - Wc / 2 + r * 0.25) / (r * 0.6), (yy - 13) / 12), 0, 1)
        col = np.array([70, 40, 20], np.float32) / 255 * (0.55 + 0.9 * lum)[..., None] + (lum ** 6)[..., None] * 0.35
        y0 = cy0 - 20
        pegar(out, premul(np.clip(col, 0, 1), a), 0, y0)
    return out


# ============================================================================= piezas del kit (generalizadas)
def _plano(fuente_img, fondo=PAPEL_CL):
    """Imagen RGB sin transparencia (lo transparente queda en color papel)."""
    im = C.rgba(fuente_img)
    bg = Image.new('RGBA', im.size, tuple(fondo) + (255,))
    bg.alpha_composite(im)
    return bg.convert('RGB')


def _foto_pegada(fuente_img, ancho, ang=0.0, tono=0.4, margen=14, seed=0):
    """foto_pegada de la demo para rutas, «ico:» e íconos de objeto (estos, más chicos: no se ven borrosos)."""
    im = _plano(fuente_img)
    if C.es_icono(fuente_img):
        ancho = min(ancho, 230)
    h = int(ancho * im.height / im.width)
    if h > ancho * 1.3:                                   # retrato muy alto: recorte 4:5 desde arriba (caras)
        h = int(ancho * 1.25)
        e = ancho / im.width
        im = im.resize((ancho, int(im.height * e)), Image.LANCZOS).crop((0, 0, ancho, h))
    else:
        im = im.resize((ancho, h), Image.LANCZOS)
    f = np.asarray(im, np.float32) / 255
    g = cv2.cvtColor((f * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    f = f * (1 - tono) + SEPIA[g] * tono
    f = f * (0.92 + 0.08 * ruido(h, ancho, 40, seed, 2))[..., None]
    Wp, Hp = ancho + 2 * margen, h + 2 * margen
    base = papel(Hp, Wp, seed + 30)
    base[margen:margen + h, margen:margen + ancho] = f
    cv2.rectangle(base, (margen - 3, margen - 3), (margen + ancho + 2, margen + h + 2), tuple(np.array(TINTA) / 255.0), 2, cv2.LINE_AA)
    s = borde_rasgado(base, seed + 31, ancho=8)
    return transformar(s, ang)[0]


def _texto_cabe(txt, tam, ancho_max, minimo=30, **kw):
    s = texto(txt, tam, **kw)
    while s.shape[1] > ancho_max and tam > minimo:
        tam -= 4
        s = texto(txt, tam, **kw)
    return s


def _bloque(sprs, gap=-6, dx=(0, 10)):
    """Apila sprites premultiplicados (alineados a la izquierda, el segundo un poco a la derecha)."""
    sprs = [s for s in sprs if s is not None]
    w = max(s.shape[1] + dx[min(i, len(dx) - 1)] for i, s in enumerate(sprs))
    h = sum(s.shape[0] for s in sprs) + gap * (len(sprs) - 1)
    out = np.zeros((h, w, 4), np.float32)
    y = 0
    for i, s in enumerate(sprs):
        pegar(out, s, dx[min(i, len(dx) - 1)], y)
        y += s.shape[0] + gap
    return out


# ----------------------------------------------------------------------------- FICHA (pergamino entre rodillos)
class Ficha:
    """Pergamino entre dos rodillos que se despliega: título escrito, rúbrica, íconos con mancha de tinta y su etiqueta a
    pluma, contador que rueda con el acumulado y círculo de tinta roja al total. Ícono k en la marca k."""
    MX, MY = 90, 130

    def __init__(self, titulo, iconos, etiquetas, valores, total=None, alto=600, seed=21):
        n = len(iconos)
        self.n = n
        self.titulo = _texto_cabe(titulo, 80, 1480, 50, seed=11)
        base = 660 + 200 * (n - 1)
        ancho = int(max(base, self.titulo.shape[1] + 110))
        self.w, self.h = ancho, alto
        off = (ancho - base) / 2
        self.lay_ix = [off + 165 + 200 * i for i in range(n)]
        pap = papel(alto, ancho, seed)
        yy = np.arange(alto, dtype=np.float32)
        osc = 1 - 0.18 * (np.clip(1 - yy / 40, 0, 1) ** 2 + np.clip(1 - (alto - yy) / 40, 0, 1) ** 2)
        pap *= osc[:, None, None]
        self.papel = borde_rasgado(pap, seed + 1, ancho=6)
        self.rod = rodillo(alto)
        self.rod_sh = sombra(self.rod, 6, 0.5)
        self.rub = rubrica(min(520, ancho - 220), 14)
        self.etqs = [texto(e, 58, seed=12 + i) if e else None for i, e in enumerate(etiquetas)]
        self.igual = texto('=', 110, seed=13)
        cum = [0]
        for v in valores:
            cum.append(cum[-1] + v)
        if total is not None:
            cum[-1] = total
        self.cum = cum
        self.nums = {v: texto(str(v), 132, seed=14 + (v % 50)) for v in cum}
        self.gx = self.lay_ix[-1] + 170
        self.nx = self.gx + 145
        nw = max(s.shape[1] for s in self.nums.values())
        x0c, x1c = self.gx - 50, self.nx + nw / 2 + 10
        self.circ = circulo_mano((x1c - x0c) / 2, 92, seed + 5)
        self.circ_cx = (x0c + x1c) / 2
        self.iconos = []
        R = 74
        for i, ruta in enumerate(iconos):
            im = np.asarray(_plano(ruta, (40, 30, 22)).resize((2 * R, 2 * R), Image.LANCZOS), np.float32) / 255
            g = cv2.cvtColor((im * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
            im = im * 0.85 + SEPIA[g] * 0.15
            S = 2 * R + 40
            c = S / 2
            yy, xx = np.mgrid[0:S, 0:S].astype(np.float32)
            dist = np.hypot(xx - c + 0.5, yy - c + 0.5)
            canvas = np.zeros((S, S, 3), np.float32)
            canvas[20:20 + 2 * R, 20:20 + 2 * R] = im
            spr = premul(canvas, np.clip(R - dist + 0.5, 0, 1))
            ink = np.array(TINTA, np.float32) / 255
            for (rr, g_) in [(R + 1.5, 2.6), (R + 9, 1.4)]:
                ar = np.clip(g_ / 2 - np.abs(dist - rr) + 0.5, 0, 1)
                spr = premul(np.broadcast_to(ink, ar.shape + (3,)).copy(), ar) + spr * (1 - ar[..., None])
            self.iconos.append((spr, campo_mancha(S, S, seed + 40 + i, 0.5, 0.5, 0.30, escala=S / 4)))
        self.mancha_col = np.array([70, 44, 24], np.float32) / 255
        rng = np.random.default_rng(seed + 9)
        self.gotas = [[(rng.uniform(0, 6.28), rng.uniform(95, 125), rng.uniform(2, 4.5)) for _ in range(6)] for _ in iconos]
        self.cw, self.ch = ancho + 2 * self.MX, alto + 2 * self.MY
        self._sh = {}

    def tiempos(self, dur, marcas):
        ic = C.tiempos(marcas, self.n, ini=1.6, paso=.7, minimo=1.0)[:self.n]
        return dict(cae=(0.0, 0.3), abre=(0.3, 1.1), titulo=(0.8, 1.7), rub=(1.5, 2.0), cont=max(1.0, ic[0] - .3),
                    iconos=ic, circ=(ic[-1] + .85, ic[-1] + 1.55), cierra=(dur - .75, dur - .25), fuera=(dur - .3, dur))

    def _contenido(self, t):
        T = self.T
        cv = self.papel.copy()
        pt = seg(t, *T['titulo'])
        if pt > 0:
            pegar(cv, escribir(self.titulo, pt), self.w / 2 - self.titulo.shape[1] / 2, 92 - self.titulo.shape[0] / 2)
        dibujar_trazo(cv, self.rub[0], self.rub[1], eio(seg(t, *T['rub'])), self.w / 2, 158)
        n = 0
        for i, (spr, man) in enumerate(self.iconos):
            ti = T['iconos'][i]
            X, Y = self.lay_ix[i], 300
            dt = t - ti
            if dt < 0:
                continue
            pm = eo(seg(dt, 0, 0.22))
            mm = revelar(man, pm * 0.50, 0.05) * 0.20
            pegar_c(cv, premul(np.broadcast_to(self.mancha_col, mm.shape + (3,)).copy(), mm), X, Y)
            u = seg(dt, 0.05, 0.42)
            if u > 0:
                k = 1.35 - 0.35 * eback(u, 2.2)
                sp = transformar(spr, 0, k)[0] if abs(k - 1) > 1e-3 else spr
                pegar_c(cv, sombra(sp, 5, 0.4), X + 5, Y + 7, min(1, u * 2.5))
                pegar_c(cv, sp, X, Y, min(1, u * 2.5))
            if dt > 0.3:
                for (a, dd, rr) in self.gotas[i]:
                    k = eo(seg(dt, 0.3, 0.45))
                    cvv = np.zeros((14, 14, 4), np.uint8)
                    cv2.circle(cvv, (7 * 16, 7 * 16), int(rr * 16), TINTA + (230,), -1, cv2.LINE_AA, 4)
                    pegar_c(cv, cvv.astype(np.float32) / 255, X + math.cos(a) * dd * (0.8 + 0.2 * k), Y + math.sin(a) * dd * 0.95)
            pe = seg(dt, 0.35, 0.75)
            if pe > 0 and self.etqs[i] is not None:
                e = self.etqs[i]
                pegar(cv, escribir(e, pe), X - e.shape[1] / 2, 435 - e.shape[0] / 2)
            if dt >= 0.3:
                n += 1
        if t >= T['cont']:
            al = cl((t - T['cont']) / 0.3)
            gx, nx = self.gx, self.nx
            pegar(cv, self.igual, gx - self.igual.shape[1] / 2, 300 - self.igual.shape[0] / 2, al)
            t_ult = T['iconos'][n - 1] + 0.3 if n > 0 else -9
            u = cl((t - t_ult) / 0.28)
            new = self.nums[self.cum[n]]
            if n > 0 and u < 1:
                old = self.nums[self.cum[n - 1]]
                pegar(cv, old, nx - old.shape[1] / 2, 296 - old.shape[0] / 2 - 40 * eo(u), (1 - u) * al)
                pegar(cv, new, nx - new.shape[1] / 2, 296 - new.shape[0] / 2 + 40 * (1 - eo(u)), u * al)
            else:
                pegar(cv, new, nx - new.shape[1] / 2, 296 - new.shape[0] / 2, al)
            dibujar_trazo(cv, self.circ[0], self.circ[1], eio(seg(t, *T['circ'])), self.circ_cx, 300, TINTA_ROJA, 0.92)
        return cv

    def dibuja(self, frame, t):
        T = self.T
        if t < T['cae'][0] or t > T['fuera'][1]:
            return
        ab = eio(seg(t, *T['abre'])) if t < T['cierra'][0] else 1 - eio(seg(t, *T['cierra']))
        wv = int(40 + (self.w - 40) * ab)
        al = eo(seg(t, *T['cae'])) * (1 - seg(t, *T['fuera']))
        dy = -50 * (1 - eo(seg(t, *T['cae']))) + 30 * seg(t, *T['fuera'])
        cx, cy = self.cw / 2, self.ch / 2 + dy
        cv = self._contenido(t) if ab > 0.02 else self.papel
        xo = (self.w - wv) // 2
        sub = cv[:, xo:xo + wv]
        if wv not in self._sh:
            if len(self._sh) > 40:
                self._sh.clear()
            self._sh[wv] = sombra(sub, 14, 0.55)
        pegar(frame, self._sh[wv], cx - wv / 2 + 14, cy - self.h / 2 + 18, al)
        pegar(frame, sub, cx - wv / 2, cy - self.h / 2, al)
        rw, rh = self.rod.shape[1], self.rod.shape[0]
        for sx in (-1, 1):
            X = cx + sx * wv / 2
            pegar(frame, self.rod_sh, X - rw / 2 + 8, cy - rh / 2 + 12, al)
            pegar(frame, self.rod, X - rw / 2, cy - rh / 2, al)

    def fn(self):
        def fn(dt, dur, marcas):
            self.T = self.tiempos(dur, marcas)
            cv = np.zeros((self.ch, self.cw, 4), np.float32)
            self.dibuja(cv, dt)
            return C.bgra_premul(cv)
        return fn


# ----------------------------------------------------------------------------- TARJETA (pergamino quemado con arco)
class Tarjeta:
    """Tarjeta de pergamino que cae girando: foto en ventana de arco, título a pluma, rúbrica, líneas, sello de lacre;
    sale quemándose."""

    def __init__(self, foto, titulo, sub=None, letra=None, ancho=600, ang=-3.0, seed=51):
        self.ang = ang
        self.mg = mg = 70
        fw, fh = ancho - 110, int((ancho - 110) * .6)
        self.titulos = []
        t1 = _texto_cabe(titulo, 56, ancho - 70, 40, seed=21)
        if t1.shape[1] > ancho - 70:
            fnt = fuente(CALI, 46)
            self.titulos = [texto(l, 46, seed=21 + i) for i, l in enumerate(C.partir(titulo, ancho - 80, fnt.getlength))]
        else:
            self.titulos = [t1]
        fnt = fuente(CALI, 44)
        self.lineas = [texto(l, 44, seed=31 + i) for i, l in enumerate(C.partir(sub, ancho - 90, fnt.getlength))] if sub else []
        fx, fy = mg + 55, mg + 52
        self.ty = [fy + fh + 54 + 58 * i for i in range(len(self.titulos))]
        self.ry = self.ty[-1] + 46
        self.ly = [self.ry + 54 + 50 * i for i in range(len(self.lineas))]
        alto = int((self.ly[-1] if self.lineas else self.ry) + 46 - mg)
        self.w, self.h = ancho, alto
        base = quemar_bordes(papel(alto, ancho, seed), seed + 1, ancho=24, carbon=10, chamusca=70)
        self.base = np.zeros((alto + 2 * mg, ancho + 2 * mg, 4), np.float32)
        pegar(self.base, base, mg, mg)
        if C.es_icono(foto):
            fondo = Image.new('RGB', (fw, fh), (52, 38, 26))
            ic = _plano(foto, (52, 38, 26))
            e = fh * .8 / ic.height
            ic = ic.resize((max(2, int(ic.width * e)), max(2, int(ic.height * e))), Image.LANCZOS)
            fondo.paste(ic, ((fw - ic.width) // 2, (fh - ic.height) // 2 + 20))
            im = fondo
        else:
            im = _plano(foto)
        sc = max(fw / im.width, fh / im.height)
        im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
        ox, oy = (im.width - fw) // 2, (im.height - fh) // 4
        f = np.asarray(im, np.float32)[oy:oy + fh, ox:ox + fw] / 255
        g = cv2.cvtColor((f * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        f = f * 0.62 + SEPIA[g] * 0.38
        m = Image.new('L', (fw, fh), 0)
        dm = ImageDraw.Draw(m)
        dm.rectangle([0, fw // 2 - 40, fw, fh], fill=255)
        dm.ellipse([0, 0, fw, fw - 60], fill=255)
        ma = cv2.GaussianBlur(np.asarray(m, np.float32) / 255, (0, 0), 0.7)
        self.foto = premul(f, ma)
        self.foto_xy = (fx, fy)
        self.f_foto = campo_mancha(fh, fw, seed + 3, 0.5, 0.45, 0.42)
        big = np.zeros((fh + 40, fw + 40), np.uint8)
        big[20:-20, 20:-20] = (ma > 0.5)
        dist = cv2.distanceTransform((1 - big).astype(np.uint8), cv2.DIST_L2, 5)
        ring = np.clip(1.6 - np.abs(dist - 3.5), 0, 1) + np.clip(0.9 - np.abs(dist - 11), 0, 1)
        ink = np.array(TINTA, np.float32) / 255
        self.filete = premul(np.broadcast_to(ink, ring.shape + (3,)).copy(), np.clip(ring, 0, 1))
        self.rub = rubrica(min(380, ancho - 160), 10)
        letra = letra if letra is not None else next((ch for ch in titulo if ch.isalnum()), 'N').upper()
        self.sello = Caida(48, letra, seed + 5, 1.9, gotas=5)
        Hc, Wc = self.base.shape[:2]
        self.f_quema = campo_mancha(Hc, Wc, seed + 7, 0.85, 0.95, 0.45)
        a = math.radians(16)
        self.cw = int((Wc * math.cos(a) + Hc * math.sin(a)) * 1.16) + 60
        self.ch = int((Wc * math.sin(a) + Hc * math.cos(a)) * 1.16) + 80

    def _canvas(self, t):
        cv = self.base.copy()
        pf = seg(t, .45, 1.2)
        if pf > 0:
            fx, fy = self.foto_xy
            pegar(cv, self.filete * min(1, pf * 2), fx - 20, fy - 20)
            pegar(cv, self.foto * revelar(self.f_foto, eo(pf), 0.08)[..., None], fx, fy)
        cxl = self.mg + self.w / 2
        for i, s in enumerate(self.titulos):
            pt = seg(t, .9 + .5 * i, 1.7 + .5 * i)
            if pt > 0:
                pegar(cv, escribir(s, pt), cxl - s.shape[1] / 2, self.ty[i] - s.shape[0] / 2)
        dibujar_trazo(cv, self.rub[0], self.rub[1], eio(seg(t, 1.6, 2.1)), cxl, self.ry)
        for i, s in enumerate(self.lineas):
            pl = seg(t, 1.9 + .55 * i, 2.6 + .55 * i)
            if pl > 0:
                pegar(cv, escribir(s, pl), cxl - s.shape[1] / 2, self.ly[i] - s.shape[0] / 2)
        self.sello.dibuja(cv, self.mg + self.w - 70, self.mg + 58, t)
        return cv

    def fn(self):
        def fn(dt, dur, marcas):
            u = seg(dt, 0, .6)
            if u <= 0:
                return C.VACIO
            e = eback(u, 1.3)
            cv = self._canvas(dt)
            q = seg(dt, dur - .7, dur - .02)
            if q > 0:
                cv = quemar_spr(cv, self.f_quema, q)
            sp, _ = transformar(cv, lerp(14, self.ang, e), lerp(1.15, 1.0, eo(u)))
            out = np.zeros((self.ch, self.cw, 4), np.float32)
            a = min(1, u * 3)
            cx, cy = self.cw / 2, self.ch / 2 - 30 * (1 - eo(u))
            pegar_c(out, sombra(sp, 12, 0.6), cx + 16, cy + 22, a)
            pegar_c(out, sp, cx, cy, a)
            return C.bgra_premul(out)
        return fn


# ----------------------------------------------------------------------------- RÓTULO (tira de papel con lacre)
class Rotulo:
    """Tira de papel rasgado que se desenrolla, sello de lacre con su letra/cifra y texto escrito a pluma; sale quemándose."""
    MG = 100

    def __init__(self, txt, letra=None, alto=118, seed=61):
        self.txt = _texto_cabe(txt, 66, 1400, 40, seed=31)
        self.xt = 128 if letra else 44
        ancho = self.xt + self.txt.shape[1] + 46
        self.w, self.h = ancho, alto
        self.tira = borde_rasgado(papel(alto, ancho, seed), seed + 1, ancho=9)
        ink = np.array(TINTA, np.float32) / 255
        x0 = self.xt - 8
        for yy_ in (16, alto - 18):
            t_ = self.tira[yy_:yy_ + 2, x0:ancho - 30]
            t_[..., :3] = t_[..., :3] * 0.3 + ink * 0.7 * t_[..., 3:4]
        self.sello = Caida(56, str(letra)[:2], seed + 2, 0.55, gotas=6) if letra else None
        mg = self.MG
        self.f_quema = campo_mancha(alto + 2 * mg, ancho + 2 * mg, seed + 3, 0.1, 0.5, 0.45)

    def fn(self):
        def fn(dt, dur, marcas):
            mg = self.MG
            pa = eo(seg(dt, 0.0, 0.6))
            wv = max(2, int(self.w * pa))
            cv = np.zeros((self.h + 2 * mg, self.w + 2 * mg, 4), np.float32)
            dx = -30 * (1 - pa)
            tira = np.zeros_like(cv)
            pegar(tira, self.tira[:, :wv], mg + dx, mg)
            pt = seg(dt, 0.95, 2.1)
            if pt > 0:
                pegar(tira, escribir(self.txt, pt), mg + self.xt + dx, mg + self.h / 2 - self.txt.shape[0] / 2 - 2)
            if self.sello is not None:
                self.sello.dibuja(tira, mg + 52 + dx, mg + self.h / 2, dt)
            q = seg(dt, dur - .68, dur - .02)
            if q > 0:
                tira = quemar_spr(tira, self.f_quema, q)
            pegar(cv, sombra(tira, 10, 0.6), 10, 14)
            pegar(cv, tira, 0, 0)
            return C.bgra_premul(cv)
        return fn


# ----------------------------------------------------------------------------- PEGATINA (foto pegada con lacre)
class Pegatina:
    """Foto pegada en pergamino rasgado que se revela como tinta, sello de lacre que la clava y su nombre a pluma."""
    MG = 60

    def __init__(self, fuente_img, titulo=None, tam=380, seed=0):
        rng = np.random.default_rng(seed)
        ang = float(rng.choice([-1, 1]) * rng.uniform(2.0, 4.0))
        self.foto = _foto_pegada(fuente_img, int(tam), ang, tono=.35, seed=seed)
        self.sh = sombra(self.foto, 8, .55)
        fh, fw = self.foto.shape[:2]
        self.campo = campo_mancha(fh, fw, seed + 1, .5, .5, .4)
        self.lacre = Caida(max(16, int(min(fw, 380) * .075)), None, seed + 2, .5, gotas=4)
        self.tit = _texto_cabe(titulo, 50, max(fw * 1.25, 320), 30, halo=HALO, seed=seed + 3) if titulo else None
        th = self.tit.shape[0] if self.tit is not None else 0
        tw = self.tit.shape[1] if self.tit is not None else 0
        mg = self.MG
        self.cw = int(max(fw, tw) + 2 * mg)
        self.ch = int(fh + th + 2 * mg - (14 if th else 0))
        self.fx, self.fy = self.cw / 2, mg + fh / 2
        self.ty = mg + fh - 14
        self.f_q = campo_mancha(self.ch, self.cw, seed + 5, .2, .9, .45)

    def fn(self):
        def fn(dt, dur, marcas):
            p = seg(dt, 0, .6)
            if p <= 0:
                return C.VACIO
            cv = np.zeros((self.ch, self.cw, 4), np.float32)
            m = revelar(self.campo, eo(p), .08)[..., None]
            k = 1.08 - .08 * eo(p)
            fy = self.fy + 2 * math.sin(dt * 1.3)
            sp, sh = self.foto * m, self.sh * m
            if abs(k - 1) > 1e-3:
                sp, sh = transformar(sp, 0, k)[0], transformar(sh, 0, k)[0]
            pegar_c(cv, sh, self.fx + 7, fy + 10)
            pegar_c(cv, sp, self.fx, fy)
            self.lacre.dibuja(cv, self.fx - 4, fy - self.foto.shape[0] / 2 + 22, dt)
            if self.tit is not None:
                pt = seg(dt, .75, 1.5)
                if pt > 0:
                    pegar(cv, escribir(self.tit, pt), self.cw / 2 - self.tit.shape[1] / 2, self.ty)
            q = seg(dt, dur - .68, dur - .02)
            if q > 0:
                cv = quemar_spr(cv, self.f_q, q)
            return C.bgra_premul(cv)
        return fn


# ----------------------------------------------------------------------------- MAPA (cuadro entero)
class Mapa:
    """Pergamino quemado sobre la mesa con el mapa en sepia: cinta con la zona, rosa de los vientos, un sello de lacre
    numerado por paso (cae en su marca), ruta de pluma punteada del paso anterior al nuevo (se entinta con la pluma),
    rótulo caligráfico y la foto pegada de lo que se nombra (se va cuando entra el paso siguiente; la del último queda).
    La cámara encuadra los pasos vistos, como mg_wow.ruta."""
    SX0, SY0, SX1, SY1 = 46, 30, 1874, 1050
    VX0, VY0, VX1, VY1 = 120, 100, 1800, 980

    def __init__(self, mapa, puntos, titulo=None, sub=None, zmin=1.0, zmax=1.6, objeto=None, curva=.16, seed=11):
        rng = np.random.default_rng(seed)
        self.zmin, self.zmax = zmin, zmax
        img = cv2.cvtColor(cv2.imread(mapa), cv2.COLOR_BGR2RGB)
        self.mw, self.mh = img.shape[1], img.shape[0]
        hi = cv2.resize(img, (self.mw * 2, self.mh * 2), interpolation=cv2.INTER_CUBIC)
        hi = cv2.GaussianBlur(hi, (0, 0), 1.4)
        Lf = cv2.cvtColor(hi, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
        lo, up = np.percentile(Lf, 2), np.percentile(Lf, 99)
        Lf = np.clip((Lf - lo) / (up - lo), 0, 1)
        Lf = 0.24 + 0.76 * Lf ** 0.9
        L = (Lf * 255).astype(np.uint8)
        Lb = cv2.GaussianBlur(Lf, (0, 0), 3.0)
        e = np.hypot(cv2.Sobel(Lb, cv2.CV_32F, 1, 0), cv2.Sobel(Lb, cv2.CV_32F, 0, 1))
        e = np.clip(e / (np.percentile(e, 98) + 1e-6), 0, 1)
        sep = SEPIA[L] * 0.85 + hi.astype(np.float32) / 255 * 0.15
        sep *= (1 - 0.30 * e)[..., None]
        self.mhi = np.clip(sep / np.array([0.94, 0.87, 0.71], np.float32), 0, 1.08).astype(np.float32)
        g = cv2.resize(rng.random((70, 7)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
        g = 0.65 * g + 0.35 * ruido(H, W, 30, seed + 1, 3)
        oscuro = np.array([30, 18, 11], np.float32) / 255
        claro = np.array([78, 50, 30], np.float32) / 255
        mesa = oscuro + (claro - oscuro) * g[..., None]
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        luz = np.exp(-(((xx - 500) / 1300) ** 2 + ((yy - 200) / 900) ** 2))
        self.mesa = (mesa * (0.45 + 0.75 * luz)[..., None]).astype(np.float32)
        sw, sh = self.SX1 - self.SX0, self.SY1 - self.SY0
        hoja = quemar_bordes(papel(sh, sw, seed + 2), seed + 3, ancho=34, carbon=13, chamusca=110)
        self.hoja = np.zeros((H, W, 4), np.float32)
        self.hoja[self.SY0:self.SY1, self.SX0:self.SX1] = hoja
        self.hoja_sh = sombra(self.hoja, blur=18, op=0.75)
        a = np.maximum(self.hoja[..., 3:4], 1e-4)
        self.hoja_rgb = self.hoja[..., :3] / a
        VW, VH = self.VX1 - self.VX0, self.VY1 - self.VY0
        self.VW, self.VH = VW, VH
        self.pap_vp = self.hoja_rgb[self.VY0:self.VY1, self.VX0:self.VX1].copy()
        yv, xv = np.mgrid[0:VH, 0:VW].astype(np.float32)
        dv = np.minimum(np.minimum(xv, VW - 1 - xv), np.minimum(yv, VH - 1 - yv))
        self.feather = np.clip((dv - 4 - ruido(VH, VW, 40, seed + 4, 3) * 22) / 9, 0, 1)
        self.f_emp = campo_mancha(VH, VW, seed + 5, 0.47, 0.42, 0.42)
        bo = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        d = ImageDraw.Draw(bo)
        ink = TINTA + (255,)
        x0, y0, x1, y1 = self.VX0 - 12, self.VY0 - 12, self.VX1 + 12, self.VY1 + 12
        d.rectangle([x0, y0, x1, y1], outline=ink, width=5)
        d.rectangle([self.VX0 - 2, self.VY0 - 2, self.VX1 + 2, self.VY1 + 2], outline=ink, width=2)
        for (cx, cy) in [(x0, y0), (x1, y0), (x0, y1), (x1, y1)]:
            d.polygon([(cx, cy - 16), (cx + 11, cy), (cx, cy + 16), (cx - 11, cy)], fill=ink)
            d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=(236, 220, 182, 255))
        self.borde = spr_pil(bo)
        per = 2 * ((x1 - x0) + (y1 - y0))
        dx0, dx1, dy0, dy1 = np.abs(xx - x0), np.abs(xx - x1), np.abs(yy - y0), np.abs(yy - y1)
        m = np.argmin(np.stack([dy0, dx1, dy1, dx0]), axis=0)
        par = np.where(m == 0, xx - x0, np.where(m == 1, (x1 - x0) + yy - y0,
                       np.where(m == 2, (x1 - x0) + (y1 - y0) + (x1 - xx), 2 * (x1 - x0) + (y1 - y0) + (y1 - yy))))
        self.par = (par / per).astype(np.float32)
        hb = self.hoja_rgb.copy()
        pegar(hb, self.borde, 0, 0)
        self.hoja_rgb_borde = hb
        self.rosa = rosa_vientos(104)
        # cinta con la zona y subtítulo
        self.zona = _texto_cabe(titulo, 66, 1100, 44, seed=1) if titulo else None
        self.cinta = None
        fijas = [(self.VX1 - 270, self.VY1 - 270, self.VX1 - 30, self.VY1 - 30)]
        if self.zona is not None:
            self.cinta, self.cinta_c = cinta(int(max(640, self.zona.shape[1] + 150)), 100, seed + 6)
            cwid = self.cinta.shape[1]
            fijas.append((W / 2 - cwid / 2, self.VY0 - 60, W / 2 + cwid / 2, self.VY0 + 70))
        self.sub = texto(sub, 36, color=TINTA_HUM, halo=HALO, seed=3) if sub else None
        if self.sub is not None:
            fijas.append((W / 2 - self.sub.shape[1] / 2, self.VY0 + 60, W / 2 + self.sub.shape[1] / 2, self.VY0 + 70 + self.sub.shape[0]))
        # puntos
        n = len(puntos)
        self.n = n
        self.P = [(p[0] / 100 * self.mw, p[1] / 100 * self.mh) for p in puntos]
        ult = n - 1 if n > 1 else -1
        self.r_sello = [54 if i == ult else 42 for i in range(n)]
        self.sellos = [Caida(self.r_sello[i], str(i + 1), seed + 7 + i, 0.0) for i in range(n)]
        self.rot = []
        for i, p in enumerate(puntos):
            nom = texto(p[2], 50 if i == ult else 46, halo=HALO, seed=20 + i) if len(p) > 2 and p[2] else None
            sb = texto(p[3], 34, color=TINTA_HUM, halo=HALO, seed=40 + i) if len(p) > 3 and p[3] else None
            self.rot.append(_bloque([nom, sb]) if (nom is not None or sb is not None) else None)
        fotos = [p[4] if len(p) > 4 and p[4] else None for p in puntos]
        if objeto and n and fotos[-1] is None:
            fotos[-1] = "ico:" + objeto
        self.fotos = []
        for i, f in enumerate(fotos):
            if f is None:
                self.fotos.append(None)
                continue
            s = _foto_pegada(f, 330 if i == ult else 250, (-3.5 if i % 2 else 3.5), seed=60 + 7 * i)
            self.fotos.append((s, sombra(s, 7, .55), campo_mancha(s.shape[0], s.shape[1], 61 + i, .5, .5, .4),
                               Caida(15, None, 62 + i, 0.0, gotas=0)))
        self.pluma, self.punta, _ = pluma()
        self.tramos = []
        for k in range(1, n):
            A, B = np.array(self.P[k - 1]), np.array(self.P[k])
            dv_ = B - A
            Ld = max(np.linalg.norm(dv_), 1e-6)
            perp = np.array([dv_[1], -dv_[0]]) / Ld * (1 if k % 2 else -1)
            Cc = (A + B) / 2 + perp * Ld * curva
            u = np.linspace(0, 1, 160)[:, None]
            Pq = (1 - u) ** 2 * A + 2 * (1 - u) * u * Cc + u ** 2 * B
            self.tramos.append((Pq, [(f, rng.uniform(-9, 9), rng.uniform(1.6, 3.4)) for f in rng.uniform(0.1, 0.9, 4)]))
        lim = (self.VX0 + 8, self.VY0 + 8, self.VX1 - 8, self.VY1 - 8)
        self.lim = lim
        tam_rot = [(r.shape[1], r.shape[0]) if r is not None else None for r in self.rot]
        tam_foto = [(f[0].shape[1], f[0].shape[0]) if f is not None else None for f in self.fotos]
        self.lado_rot, self.lado_foto = C.colocador(self.P, None, self.mw, self.mh, VW, VH, zmin, zmax, self.VX0, self.VY0,
                                                    fijas, tam_rot, tam_foto, lambda j: self.r_sello[j] + 14,
                                                    lambda j: self.r_sello[j] + 10, lambda j: self.r_sello[j] + 40, lim)

    def _pant(self, p, cx, cy, s):
        return self.VX0 + self.VW / 2 + (p[0] - cx) * s, self.VY0 + self.VH / 2 + (p[1] - cy) * s

    def cuadro(self, t, dur, tk):
        cx, cy, s, vistos = C.camara_en(self.P, tk, t, dur, self.mw, self.mh, self.VW, self.VH, self.zmin, self.zmax)
        pant = lambda p: self._pant(p, cx, cy, s)
        bb = (.15, 1.0)
        hoja = (self.hoja_rgb_borde if t >= bb[1] else self.hoja_rgb).copy()
        pe = seg(t, .25, 1.3)
        if pe > 0:
            M = np.float32([[s / 2, 0, self.VW / 2 - cx * s], [0, s / 2, self.VH / 2 - cy * s]])
            mp = cv2.warpAffine(self.mhi, M, (self.VW, self.VH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            rv = revelar(self.f_emp, eio(pe), 0.07) * self.feather
            if pe < 1:
                frente = np.exp(-((eio(pe) * 1.09 - self.f_emp - 0.035) / 0.03) ** 2) * self.feather
                vp = self.pap_vp * (1 - rv[..., None] + mp * rv[..., None])
                vp *= (1 - frente[..., None] * np.array([0.22, 0.34, 0.5], np.float32) * rv[..., None] ** 0.5)
            else:
                vp = self.pap_vp * (1 - rv[..., None] + mp * rv[..., None])
            hoja[self.VY0:self.VY1, self.VX0:self.VX1] = vp
        sl = (slice(self.VY0 - 14, self.VY1 + 14), slice(self.VX0 - 14, self.VX1 + 14))
        if t < bb[1]:
            pb = eio(seg(t, *bb))
            mm = np.clip((pb * 1.02 - self.par) / 0.02, 0, 1)
            pegar(hoja, self.borde * mm[..., None], 0, 0)
        elif pe > 0:
            pegar(hoja[sl], self.borde[sl], 0, 0)
        pr = seg(t, 1.0, 1.8)
        if pr > 0:
            rs, _ = transformar(self.rosa, -120 * (1 - eo(pr)), 0.6 + 0.4 * eback(pr))
            pegar_c(hoja, rs, self.VX1 - 150, self.VY1 - 150, min(1, pr * 2) * 0.9)
        n = self.n
        # fotos pegadas (la del paso nuevo; se van cuando entra el siguiente)
        for i in vistos:
            if self.fotos[i] is None:
                continue
            sp, sh, fc, pin = self.fotos[i]
            p = seg(t, tk[i] + .45, tk[i] + 1.2)
            if p <= 0:
                continue
            a = 1.0
            if i + 1 < n and t > tk[i + 1]:
                a = 1 - eo((t - tk[i + 1]) / .4)
            if a <= 0:
                continue
            x, y = pant(self.P[i])
            fw, fh = sp.shape[1], sp.shape[0]
            rx, ry = C.caja_en(x, y, fw, fh, self.r_sello[i] + 40, self.lado_foto.get(i, 0), self.lim)
            X, Y = rx + fw / 2, ry + fh / 2
            m = revelar(fc, eo(p), 0.08)[..., None]
            k = 1.06 - 0.06 * eo(p)
            spp, shh = sp * m, sh * m
            if k != 1:
                spp, shh = transformar(spp, 0, k)[0], transformar(shh, 0, k)[0]
            pegar_c(hoja, shh, X + 7, Y + 10, a)
            pegar_c(hoja, spp, X, Y, a)
            if a >= 1:
                pin.dibuja(hoja, X - 4, Y - fh / 2 + 18, t - tk[i] - 1.15)
        # ruta de pluma: tramo k (del paso k-1 al k) en el 1,3 s que sigue a su marca
        DTR = 1.3
        pluma_en = None
        for k, (Pq, salp) in enumerate(self.tramos, 1):
            if t < tk[k]:
                continue
            q = np.array([pant(p) for p in Pq])
            Lc = np.r_[0, np.cumsum(np.hypot(*np.diff(q, axis=0).T))]
            ini, fin = self.r_sello[k - 1] + 6, Lc[-1] - self.r_sello[k] - 8
            if fin <= ini:
                continue
            prg = eio(seg(t, tk[k], tk[k] + DTR))
            cab = ini + prg * (fin - ini)
            x0, y0 = int(max(0, q[:, 0].min() - 20)), int(max(0, q[:, 1].min() - 20))
            x1, y1 = int(min(W, q[:, 0].max() + 20)), int(min(H, q[:, 1].max() + 20))
            if x1 <= x0 or y1 <= y0:
                continue
            cvs = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
            seco = 1.0 - cl((t - tk[k] - DTR) / 0.7)
            s0 = ini
            while s0 < cab:
                s1 = min(s0 + 13, cab)
                qa = (np.interp(s0, Lc, q[:, 0]) - x0, np.interp(s0, Lc, q[:, 1]) - y0)
                qb = (np.interp(s1, Lc, q[:, 0]) - x0, np.interp(s1, Lc, q[:, 1]) - y0)
                hum = cl(1 - (cab - s1) / 70) * seco
                col = np.array(TINTA) * (1 - hum) + np.array(TINTA_HUM) * hum
                cv2.line(cvs, (int(qa[0] * 16), int(qa[1] * 16)), (int(qb[0] * 16), int(qb[1] * 16)),
                         tuple(int(v) for v in col) + (255,), int(round(7 + 3 * hum)), cv2.LINE_AA, 4)
                s0 += 26
            for (f, off, rr) in salp:
                ls = ini + f * (fin - ini)
                if ls < cab:
                    qq = (np.interp(ls, Lc, q[:, 0]) - x0 + off * 1.3, np.interp(ls, Lc, q[:, 1]) - y0 - off)
                    cv2.circle(cvs, (int(qq[0] * 16), int(qq[1] * 16)), int(rr * 16), TINTA + (235,), -1, cv2.LINE_AA, 4)
            pegar(hoja, cvs.astype(np.float32) / 255, x0, y0)
            if tk[k] - .25 < t < tk[k] + DTR + .45:
                if t <= tk[k] + DTR:
                    Pp = (np.interp(cab, Lc, q[:, 0]), np.interp(cab, Lc, q[:, 1]))
                    al, lift = cl((t - tk[k] + .25) / .25), 0
                else:
                    Pp = (np.interp(fin, Lc, q[:, 0]), np.interp(fin, Lc, q[:, 1]))
                    u = (t - tk[k] - DTR) / .45
                    al, lift = 1 - u, eo(u) * 70
                pluma_en = (Pp, al, lift)
        # sellos (encima de la ruta) y rótulos caligráficos (quedan los 2 últimos y el del paso final)
        for i in vistos:
            x, y = pant(self.P[i])
            self.sellos[i].dibuja(hoja, x, y, t - tk[i])
        for i in vistos:
            r = self.rot[i]
            if r is None:
                continue
            pa = seg(t, tk[i] + .35, tk[i] + 1.25)
            if pa <= 0:
                continue
            a = 1.0
            if i != n - 1 and i + 2 < n and t > tk[i + 2]:
                a = 1 - eo((t - tk[i + 2]) / .4)
            if a <= 0:
                continue
            x, y = pant(self.P[i])
            rx, ry = C.caja_en(x, y, r.shape[1], r.shape[0], self.r_sello[i] + 10, self.lado_rot.get(i, 0), self.lim)
            pegar(hoja, escribir(r, pa), rx, ry, a)
        if self.cinta is not None:
            pc = seg(t, .6, 1.2)
            if pc > 0:
                wfull = self.cinta.shape[1]
                wv = max(2, int(wfull * eo(pc)))
                xo = (wfull - wv) // 2
                sub = self.cinta[:, xo:xo + wv]
                ccx, ccy = W / 2, self.VY0 - 8
                pegar(hoja, sombra(sub, 6, 0.5), ccx - wv / 2 + 5, ccy - self.cinta_c[1] + 8)
                pegar(hoja, sub, ccx - wv / 2, ccy - self.cinta_c[1])
                pz = seg(t, .9, 1.7)
                if pz > 0:
                    pegar(hoja, escribir(self.zona, pz), ccx - self.zona.shape[1] / 2, ccy - self.zona.shape[0] / 2 + 2)
        if self.sub is not None:
            ps = seg(t, 1.4, 2.1)
            if ps > 0:
                pegar(hoja, escribir(self.sub, ps), W / 2 - self.sub.shape[1] / 2, self.VY0 + 62)
        if pluma_en is not None:
            Pp, al, lift = pluma_en
            pl, M = transformar(self.pluma, -38 + 4 * math.sin(t * 9))
            tip = M[:, :2] @ self.punta + M[:, 2]
            pegar(hoja, sombra(pl, 5, 0.35), Pp[0] - tip[0] + 14 + lift * 0.4, Pp[1] - tip[1] + 18 + lift * 0.6, al)
            pegar(hoja, pl, Pp[0] - tip[0] + lift * 0.5, Pp[1] - tip[1] - lift, al)
        pe_h = eo(seg(t, 0, 0.75))
        dx, dy = sacudida(t, [tk[i] + .26 for i in range(n)], A=4.0)
        k = 1.05 - 0.05 * pe_h
        ddy = -40 * (1 - pe_h) + dy
        hp = premul(hoja, self.hoja[..., 3])
        frame = self.mesa.copy()
        if abs(k - 1) > 1e-4 or abs(dx) > 0.05 or abs(ddy) > 0.05:
            M = np.float32([[k, 0, (1 - k) * W / 2 + dx], [0, k, (1 - k) * H / 2 + ddy]])
            hp = cv2.warpAffine(hp, M, (W, H), flags=cv2.INTER_LINEAR)
            shp = cv2.warpAffine(self.hoja_sh, M, (W, H), flags=cv2.INTER_LINEAR)
        else:
            shp = self.hoja_sh
        frame *= (1 - shp[..., 3:4] * pe_h)
        frame = frame * (1 - hp[..., 3:4] * pe_h) + hp[..., :3] * pe_h
        return frame

    def fn(self):
        def fn(dt, dur, marcas):
            tk = C.tiempos(marcas, self.n, ini=1.3, paso=2.2, minimo=1.0)
            return C.bgra_opaco(self.cuadro(dt, dur, tk))
        return fn
