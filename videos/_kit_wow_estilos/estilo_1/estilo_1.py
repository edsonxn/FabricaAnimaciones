# -*- coding: utf-8 -*-
"""ESTILO 1 · CARTÓGRAFO DE PERGAMINO — propuesta de kit visual para Crónicas de Warcraft (22-nov-2026).

Todo por código (numpy + PIL + opencv), cuadro a cuadro, y ffmpeg para el MP4.
Piezas reutilizables (cada una devuelve un objeto con .dibuja(...) o .cuadro(t), tiempos LOCALES en segundos):
  mapa_ruta(...)  -> .cuadro(t): pergamino quemado sobre mesa; el mapa se empapa de tinta en sepia, cinta con el nombre de la zona,
                     rosa de los vientos, sellos de lacre que caen y se aplastan (con gotas), ruta de pluma punteada que se entinta
                     (tinta húmeda -> seca) con la pluma dibujando, fotos pegadas que aparecen con mancha de tinta, rótulos caligráficos.
  ficha(...)      -> .dibuja(frame, t): pergamino enrollado entre dos rodillos que se despliega; título escrito, rúbrica, íconos que
                     entran con mancha de tinta, «×15» a pluma, contador que rueda y círculo de tinta roja al total.
  tarjeta(...)    -> .dibuja(frame, t): tarjeta de pergamino lanzada sobre la mesa, foto en ventana de arco, texto a pluma, sello.
  rotulo(...)     -> .dibuja(frame, t): tira de papel rasgado que se desenrolla con sello de lacre y texto escrito.
  Transiciones: quemado(A, B, p) (el papel se quema con borde de brasa) y tinta(A, B, p) (mancha de tinta que cubre y destiñe).
  Salidas: las fichas se queman (quemar_spr).

Uso:  python estilo_1.py                 -> estilo_1_pergamino.mp4 + hoja.jpg
      python estilo_1.py --cuadros 3 9.5 -> _tmp/c_3.00.jpg ... (cuadros sueltos para revisar)
      python estilo_1.py --hoja          -> solo rehace hoja.jpg desde el MP4
"""
import os, sys, math, subprocess, argparse
import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = r'C:\FabricaAnimaciones\videos\wow_errores_60'
FFMPEG = r'C:\ffmpeg\bin\ffmpeg.exe'
FUENTES = r'C:\Windows\Fonts'
W, H, FPS, DUR = 1920, 1080, 30, 30.0
SALIDA = os.path.join(AQUI, 'estilo_1_pergamino.mp4')
TMP = os.path.join(AQUI, '_tmp')
cv2.setNumThreads(4)

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


# ----------------------------------------------------------------------------- 1) MAPA CON RUTA
class mapa_ruta:
    """Pergamino quemado sobre la mesa con el mapa en sepia, ruta de pluma de A a B, sellos, fotos y rótulos."""
    SX0, SY0, SX1, SY1 = 46, 30, 1874, 1050          # hoja de pergamino en pantalla
    VX0, VY0, VX1, VY1 = 120, 100, 1800, 980          # ventana del mapa

    def __init__(self, mapa, a, b, zona, rotulo_a, rotulo_b, sub_a=None, foto_a=None, foto_b=None, foto_zona=None,
                 letra_a='R', letra_b='B', cam=((760, 420, 1.45), (760, 228, 2.30), (765, 224, 2.42)), curva=0.30,
                 t=None, seed=11):
        self.T = dict(hoja=0.0, borde=(0.3, 1.6), empapa=(0.45, 2.2), cam=4.2, cinta=(1.0, 1.8), zona=(1.6, 2.6),
                      rosa=(2.0, 3.0), foto_zona=(2.2, 3.0), sello_a=2.9, rot_a=(3.35, 4.3), sub_a=(4.1, 4.7),
                      foto_a=(3.6, 4.4), ruta=(4.7, 7.5), sello_b=7.6, foto_b=(8.0, 8.8), rot_b=(8.6, 9.8))
        if t:
            self.T.update(t)
        T = self.T
        self.cam = cam
        rng = np.random.default_rng(seed)
        img = cv2.cvtColor(cv2.imread(mapa), cv2.COLOR_BGR2RGB)
        self.mw, self.mh = img.shape[1], img.shape[0]
        self.A = np.array([a[0] / 100 * self.mw, a[1] / 100 * self.mh])
        self.B = np.array([b[0] / 100 * self.mw, b[1] / 100 * self.mh])
        # mapa en sepia de grabado, al doble de resolución
        hi = cv2.resize(img, (self.mw * 2, self.mh * 2), interpolation=cv2.INTER_CUBIC)
        hi = cv2.GaussianBlur(hi, (0, 0), 1.4)
        Lf = cv2.cvtColor(hi, cv2.COLOR_RGB2GRAY).astype(np.float32) / 255
        lo, up = np.percentile(Lf, 2), np.percentile(Lf, 99)
        Lf = np.clip((Lf - lo) / (up - lo), 0, 1)
        Lf = 0.24 + 0.76 * Lf ** 0.9                      # sin negros: tinta de imprenta vieja sobre papel
        L = (Lf * 255).astype(np.uint8)
        Lb = cv2.GaussianBlur(Lf, (0, 0), 3.0)
        e = np.hypot(cv2.Sobel(Lb, cv2.CV_32F, 1, 0), cv2.Sobel(Lb, cv2.CV_32F, 0, 1))
        e = np.clip(e / (np.percentile(e, 98) + 1e-6), 0, 1)
        sep = SEPIA[L] * 0.85 + hi.astype(np.float32) / 255 * 0.15
        sep *= (1 - 0.30 * e)[..., None]
        self.REF = np.array([0.94, 0.87, 0.71], np.float32)
        self.mhi = np.clip(sep / self.REF, 0, 1.08).astype(np.float32)
        # mesa
        g = cv2.resize(rng.random((70, 7)).astype(np.float32), (W, H), interpolation=cv2.INTER_CUBIC)
        g = 0.65 * g + 0.35 * ruido(H, W, 30, seed + 1, 3)
        oscuro = np.array([30, 18, 11], np.float32) / 255; claro = np.array([78, 50, 30], np.float32) / 255
        mesa = oscuro + (claro - oscuro) * g[..., None]
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        luz = np.exp(-(((xx - 500) / 1300) ** 2 + ((yy - 200) / 900) ** 2))
        self.mesa = (mesa * (0.45 + 0.75 * luz)[..., None]).astype(np.float32)
        # hoja de pergamino quemada (pantalla completa, premult)
        sw, sh = self.SX1 - self.SX0, self.SY1 - self.SY0
        hoja = quemar_bordes(papel(sh, sw, seed + 2), seed + 3, ancho=34, carbon=13, chamusca=110)
        self.hoja = np.zeros((H, W, 4), np.float32)
        self.hoja[self.SY0:self.SY1, self.SX0:self.SX1] = hoja
        self.hoja_sh = sombra(self.hoja, blur=18, op=0.75)
        a = np.maximum(self.hoja[..., 3:4], 1e-4)
        self.hoja_rgb = self.hoja[..., :3] / a                      # sin premultiplicar
        VW, VH = self.VX1 - self.VX0, self.VY1 - self.VY0
        self.VW, self.VH = VW, VH
        self.pap_vp = self.hoja_rgb[self.VY0:self.VY1, self.VX0:self.VX1].copy()
        # borde impreso del mapa y campo de empapado
        yv, xv = np.mgrid[0:VH, 0:VW].astype(np.float32)
        dv = np.minimum(np.minimum(xv, VW - 1 - xv), np.minimum(yv, VH - 1 - yv))
        self.feather = np.clip((dv - 4 - ruido(VH, VW, 40, seed + 4, 3) * 22) / 9, 0, 1)
        self.f_emp = campo_mancha(VH, VW, seed + 5, 0.47, 0.42, 0.42)
        # marco de tinta (doble filete + rombos en las esquinas), revelado a lo largo del perímetro
        bo = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(bo)
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
        hb = self.hoja_rgb.copy(); pegar(hb, self.borde, 0, 0)
        self.hoja_rgb_borde = hb
        # piezas
        self.rosa = rosa_vientos(112)
        self.cinta, self.cinta_c = cinta(780, 100, seed + 6)
        self.zona = texto(zona, 66, seed=1)
        self.rot_a = texto(rotulo_a, 50, halo=HALO, seed=2)
        self.sub_a = texto(sub_a, 36, halo=HALO, color=TINTA_HUM, seed=3) if sub_a else None
        self.rot_b = texto(rotulo_b, 54, halo=HALO, seed=4)
        self.sel_a = Caida(44, letra_a, seed + 7, T['sello_a'])
        self.sel_b = Caida(54, letra_b, seed + 8, T['sello_b'])
        self.fotos = []
        for ruta, anc, ang, clave, sd in [(foto_b, 420, -3.0, 'foto_b', 40), (foto_a, 290, 4.0, 'foto_a', 50),
                                          (foto_zona, 280, 3.5, 'foto_zona', 60)]:
            if ruta:
                s = foto_pegada(ruta, anc, ang, seed=sd)
                self.fotos.append((clave, s, sombra(s, 7, 0.55), campo_mancha(s.shape[0], s.shape[1], sd + 1, 0.5, 0.5, 0.4),
                                   Caida(15, None, sd + 2, T[clave][1] - 0.05, gotas=0)))
        self.pluma, self.punta, self.cima = pluma()
        # ruta (curva cuadrática en px del mapa, con comba hacia la izquierda)
        mid = (self.A + self.B) / 2; dv_ = self.B - self.A; Ld = np.linalg.norm(dv_)
        perp = np.array([dv_[1], -dv_[0]]) / Ld
        if perp[0] > 0:
            perp = -perp
        C = mid + perp * Ld * curva
        u = np.linspace(0, 1, 600)[:, None]
        P = (1 - u) ** 2 * self.A + 2 * (1 - u) * u * C + u ** 2 * self.B
        dl = np.r_[0, np.cumsum(np.linalg.norm(np.diff(P, axis=0), axis=1))]
        self.ruta_P, self.ruta_l = P, dl
        self.ruta_L = dl[-1]
        # recorte para que la línea no se meta bajo los sellos
        self.l_ini = 50 / cam[1][2]; self.l_fin = self.ruta_L - 60 / cam[1][2]
        per_ = 12.5; dash = 6.0
        self.dashes = [(s0, min(s0 + dash, self.l_fin)) for s0 in np.arange(self.l_ini, self.l_fin, per_)]
        self.salpic = [(self.l_ini + (self.l_fin - self.l_ini) * f, rng.uniform(-9, 9), rng.uniform(1.6, 3.4))
                       for f in rng.uniform(0.1, 0.95, 5)]

    # -- cámara y coordenadas
    def camara(self, t):
        (c0x, c0y, s0), (c1x, c1y, s1), (c2x, c2y, s2) = self.cam
        if t < self.T['cam']:
            u = eio(seg(t, 0, self.T['cam']))
            return lerp(c0x, c1x, u), lerp(c0y, c1y, u), math.exp(lerp(math.log(s0), math.log(s1), u))
        u = seg(t, self.T['cam'], 11.0)
        return lerp(c1x, c2x, u), lerp(c1y, c2y, u), lerp(s1, s2, u)

    def pant(self, p, c):
        cx, cy, s = c
        return (self.VX0 + self.VW / 2 + (p[0] - cx) * s, self.VY0 + self.VH / 2 + (p[1] - cy) * s)

    def punto_ruta(self, l):
        return np.array([np.interp(l, self.ruta_l, self.ruta_P[:, 0]), np.interp(l, self.ruta_l, self.ruta_P[:, 1])])

    def cuadro(self, t):
        T = self.T
        c = self.camara(t)
        cx, cy, s = c
        hoja = (self.hoja_rgb_borde if t >= T['borde'][1] else self.hoja_rgb).copy()
        if t < T['borde'][1]:
            pb = eio(seg(t, *T['borde']))
            if pb > 0:
                m = np.clip((pb * 1.02 - self.par) / 0.02, 0, 1)
                pegar(hoja, self.borde * m[..., None], 0, 0)
        # mapa empapándose en el pergamino
        pe = seg(t, *T['empapa'])
        if pe > 0:
            M = np.float32([[s / 2, 0, self.VW / 2 - cx * s], [0, s / 2, self.VH / 2 - cy * s]])
            mp = cv2.warpAffine(self.mhi, M, (self.VW, self.VH), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
            rv = revelar(self.f_emp, eio(pe), 0.07) * self.feather
            frente = np.exp(-((eio(pe) * 1.09 - self.f_emp - 0.035) / 0.03) ** 2) * (pe < 1) * self.feather
            vp = self.pap_vp * (1 - rv[..., None] + mp * rv[..., None])
            vp *= (1 - frente[..., None] * np.array([0.22, 0.34, 0.5], np.float32) * rv[..., None] ** 0.5)
            hoja[self.VY0:self.VY1, self.VX0:self.VX1] = vp
            if t < T['borde'][1]:
                pb = eio(seg(t, *T['borde']))
                m = np.clip((pb * 1.02 - self.par) / 0.02, 0, 1)[self.VY0 - 3:self.VY1 + 3, self.VX0 - 3:self.VX1 + 3]
                pegar(hoja[self.VY0 - 3:self.VY1 + 3, self.VX0 - 3:self.VX1 + 3],
                      self.borde[self.VY0 - 3:self.VY1 + 3, self.VX0 - 3:self.VX1 + 3] * m[..., None], 0, 0)
            else:
                pegar(hoja[self.VY0 - 3:self.VY1 + 3, self.VX0 - 3:self.VX1 + 3],
                      self.borde[self.VY0 - 3:self.VY1 + 3, self.VX0 - 3:self.VX1 + 3], 0, 0)
        PA = self.pant(self.A, c); PB = self.pant(self.B, c)
        # rosa de los vientos
        pr = seg(t, *T['rosa'])
        if pr > 0:
            rs, _ = transformar(self.rosa, -120 * (1 - eo(pr)), 0.6 + 0.4 * eback(pr))
            pegar_c(hoja, rs, self.VX1 - 150, self.VY1 - 150, min(1, pr * 2) * 0.9)
        # fotos
        anclas = {'foto_b': (PB[0] + 335, PB[1] - 70), 'foto_a': (PA[0] - 250, PA[1] - 10),
                  'foto_zona': (self.VX0 + 205, self.VY0 + 170)}
        for clave, sp, sh, fc, pin in self.fotos:
            p = seg(t, *T[clave])
            if p <= 0:
                continue
            X, Y = anclas[clave]
            m = revelar(fc, eo(p), 0.08)[..., None]
            k = 1.06 - 0.06 * eo(p)
            spp = sp * m
            if k != 1:
                spp = transformar(spp, 0, k)[0]; shh = transformar(sh * m, 0, k)[0]
            else:
                shh = sh * m
            pegar_c(hoja, shh, X + 7, Y + 10)
            pegar_c(hoja, spp, X, Y)
            pin.dibuja(hoja, X - 4, Y - sp.shape[0] / 2 + 18, t)
        # ruta de pluma punteada
        p0, p1 = T['ruta']
        pr = eio(seg(t, p0, p1))
        cab = self.l_ini + pr * (self.l_fin - self.l_ini)
        if pr > 0:
            pts = [self.pant(self.punto_ruta(l), c) for l in (self.l_ini, self.l_fin)]
            x0 = int(min(PA[0], PB[0]) - 220); x1 = int(max(PA[0], PB[0]) + 120)
            y0 = int(min(PA[1], PB[1]) - 60); y1 = int(max(PA[1], PB[1]) + 60)
            x0, y0 = max(0, x0), max(0, y0)
            cvs = np.zeros((y1 - y0, x1 - x0, 4), np.uint8)
            seco = 1.0 - cl((t - p1) / 0.7) if t > p1 else 1.0
            for (a_, b_) in self.dashes:
                if a_ > cab:
                    break
                bb = min(b_, cab)
                q1 = np.array(self.pant(self.punto_ruta(a_), c)) - [x0, y0]
                q2 = np.array(self.pant(self.punto_ruta(bb), c)) - [x0, y0]
                hum = cl(1 - (cab - b_) / 34) * seco
                col = np.array(TINTA) * (1 - hum) + np.array(TINTA_HUM) * hum
                g = int(round(7 + 3 * hum))
                cv2.line(cvs, (int(q1[0] * 16), int(q1[1] * 16)), (int(q2[0] * 16), int(q2[1] * 16)),
                         tuple(int(v) for v in col) + (255,), g, cv2.LINE_AA, 4)
            for (l, off, rr) in self.salpic:
                if l < cab:
                    q = np.array(self.pant(self.punto_ruta(l), c)) - [x0, y0] + [off * 1.3, -off]
                    cv2.circle(cvs, (int(q[0] * 16), int(q[1] * 16)), int(rr * 16), TINTA + (235,), -1, cv2.LINE_AA, 4)
            pegar(hoja, cvs.astype(np.float32) / 255, x0, y0)
        # sellos y rótulos
        self.sel_a.dibuja(hoja, PA[0], PA[1], t)
        pa = seg(t, *T['rot_a'])
        if pa > 0:
            pegar(hoja, escribir(self.rot_a, pa), PA[0] + 52, PA[1] - self.rot_a.shape[0] / 2 - 18)
        if self.sub_a is not None:
            ps = seg(t, *T['sub_a'])
            if ps > 0:
                pegar(hoja, escribir(self.sub_a, ps), PA[0] + 60, PA[1] + 14)
        self.sel_b.dibuja(hoja, PB[0], PB[1], t)
        pb = seg(t, *T['rot_b'])
        if pb > 0:
            fb = anclas['foto_b']
            pegar(hoja, escribir(self.rot_b, pb), fb[0] - self.rot_b.shape[1] / 2, fb[1] + 150)
        # cinta con el nombre de la zona
        pc = seg(t, *T['cinta'])
        if pc > 0:
            wfull = self.cinta.shape[1]; wv = max(2, int(wfull * eo(pc)))
            xo = (wfull - wv) // 2
            sub = self.cinta[:, xo:xo + wv]
            ccx, ccy = W / 2, self.VY0 - 8
            pegar(hoja, sombra(sub, 6, 0.5), ccx - wv / 2 + 5, ccy - self.cinta_c[1] + 8)
            pegar(hoja, sub, ccx - wv / 2, ccy - self.cinta_c[1])
            pz = seg(t, *T['zona'])
            if pz > 0:
                pegar(hoja, escribir(self.zona, pz), ccx - self.zona.shape[1] / 2,
                      ccy - self.zona.shape[0] / 2 + (self.cinta_c[1] - self.cinta.shape[0] / 2) * 0 + 2)
        # pluma
        if p0 - 0.25 < t < p1 + 0.45:
            if t <= p1:
                P = np.array(self.pant(self.punto_ruta(cab), c)); al = cl((t - p0 + 0.25) / 0.25); lift = 0
            else:
                P = np.array(self.pant(self.punto_ruta(self.l_fin), c)); u = (t - p1) / 0.45; al = 1 - u; lift = eo(u) * 70
            wob = 4 * math.sin(t * 9)
            pl, M = transformar(self.pluma, -38 + wob)
            tip = M[:, :2] @ self.punta + M[:, 2]
            pegar(hoja, sombra(pl, 5, 0.35), P[0] - tip[0] + 14 + lift * 0.4, P[1] - tip[1] + 18 + lift * 0.6, al)
            pegar(hoja, pl, P[0] - tip[0] + lift * 0.5, P[1] - tip[1] - lift, al)
        # hoja sobre la mesa (entrada + sacudidas de los sellos)
        pe_h = eo(seg(t, 0, 0.75))
        dx, dy = sacudida(t, [self.sel_a.t0 + self.sel_a.dur, self.sel_b.t0 + self.sel_b.dur])
        k = 1.05 - 0.05 * pe_h; ddy = -40 * (1 - pe_h) + dy
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


# ----------------------------------------------------------------------------- fondo de gameplay tratado
class Clip:
    def __init__(self, ruta):
        self.cap = cv2.VideoCapture(ruta); self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.idx = -1; self.fr = None

    def get(self, i):
        i = max(0, min(self.n - 1, int(i)))
        if i == self.idx and self.fr is not None:
            return self.fr
        if i < self.idx or i > self.idx + 40 or self.fr is None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, i); self.idx = i - 1
        while self.idx < i:
            ok, f = self.cap.read()
            if not ok:
                break
            self.fr = f; self.idx += 1
        return self.fr


class FondoJuego:
    """Gameplay virado a sepia cálido, suavizado, con viñeta de bordes chamuscados y grano de papel."""
    def __init__(self, seed=31):
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = np.minimum(np.minimum(xx, W - 1 - xx), np.minimum(yy, H - 1 - yy))
        dd = d - ruido(H, W, 90, seed, 4) * 60
        self.carbon = (np.clip(1 - dd / 16, 0, 1) ** 0.8)[..., None]
        sc = np.clip(1 - dd / 230, 0, 1) ** 1.6
        r = np.hypot((xx - W / 2) / W, (yy - H / 2) / H)
        self.mult = ((1 - 0.6 * sc) * (1 - 0.55 * np.clip(r * 1.4 - 0.25, 0, 1)) *
                     (0.94 + 0.08 * ruido(H, W, 4, seed + 1, 2)))[..., None].astype(np.float32)
        self.tinte = (1 - 0.35 * sc[..., None] * np.array([0.3, 0.6, 1.0], np.float32)).astype(np.float32)

    def trata(self, bgr):
        f = cv2.GaussianBlur(bgr, (0, 0), 1.3)
        g = cv2.cvtColor(f, cv2.COLOR_BGR2GRAY)
        rgb = f[..., ::-1].astype(np.float32) / 255
        out = SEPIA_JUEGO[g] * 0.58 + rgb * np.array([1.0, 0.9, 0.7], np.float32) * 0.42
        out = out * self.mult * self.tinte
        out = out * (1 - self.carbon) + CARBON * self.carbon
        return out


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


class ficha:
    """Pergamino entre dos rodillos que se despliega: título, rúbrica, íconos con «×N», contador y círculo rojo."""
    def __init__(self, titulo, iconos, etiqueta='×15', paso=15, cx=960, cy=560, ancho=1260, alto=600, t=None, seed=21):
        self.T = dict(cae=(0.0, 0.3), abre=(0.3, 1.1), titulo=(1.1, 2.1), rub=(2.0, 2.55), cont=2.3,
                      iconos=[2.6, 3.3, 4.0, 4.7], circ=(5.45, 6.15), cierra=(8.7, 9.2), fuera=(9.15, 9.4))
        if t:
            self.T.update(t)
        self.cx, self.cy, self.w, self.h, self.paso = cx, cy, ancho, alto, paso
        pap = papel(alto, ancho, seed)
        yy = np.arange(alto, dtype=np.float32)
        osc = 1 - 0.18 * (np.clip(1 - yy / 40, 0, 1) ** 2 + np.clip(1 - (alto - yy) / 40, 0, 1) ** 2)
        pap *= osc[:, None, None]
        self.papel = borde_rasgado(pap, seed + 1, ancho=6)
        self.rod = rodillo(alto)
        self.rod_sh = sombra(self.rod, 6, 0.5)
        self.titulo = texto(titulo, 80, seed=11)
        self.rub = rubrica(520, 14)
        self.etq = texto(etiqueta, 58, seed=12)
        self.igual = texto('=', 110, seed=13)
        self.nums = {v: texto(str(v), 132, seed=14 + v) for v in range(0, paso * len(iconos) + 1, paso)}
        self.circ = circulo_mano(138, 92, seed + 5)
        self.iconos = []
        R = 74
        for i, ruta in enumerate(iconos):
            im = np.asarray(Image.open(ruta).convert('RGB').resize((2 * R, 2 * R), Image.LANCZOS), np.float32) / 255
            g = cv2.cvtColor((im * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
            im = im * 0.85 + SEPIA[g] * 0.15
            S = 2 * R + 40; c = S / 2
            yy, xx = np.mgrid[0:S, 0:S].astype(np.float32); dist = np.hypot(xx - c + 0.5, yy - c + 0.5)
            canvas = np.zeros((S, S, 3), np.float32); canvas[20:20 + 2 * R, 20:20 + 2 * R] = im
            a_ic = np.clip(R - dist + 0.5, 0, 1)
            spr = premul(canvas, a_ic)
            ink = np.array(TINTA, np.float32) / 255
            for (rr, g_) in [(R + 1.5, 2.6), (R + 9, 1.4)]:
                ar = np.clip(g_ / 2 - np.abs(dist - rr) + 0.5, 0, 1)
                spr = premul(np.broadcast_to(ink, ar.shape + (3,)).copy(), ar) + spr * (1 - ar[..., None])
            mancha = campo_mancha(S, S, seed + 40 + i, 0.5, 0.5, 0.30, escala=S / 4)
            self.iconos.append((spr, mancha))
        self.mancha_col = np.array([70, 44, 24], np.float32) / 255
        rng = np.random.default_rng(seed + 9)
        self.gotas = [[(rng.uniform(0, 6.28), rng.uniform(95, 125), rng.uniform(2, 4.5)) for _ in range(6)] for _ in iconos]
        self.lay_ix = [165 + 200 * i for i in range(len(iconos))]

    def _contenido(self, t):
        T = self.T
        cv = self.papel.copy()
        pt = seg(t, *T['titulo'])
        if pt > 0:
            pegar(cv, escribir(self.titulo, pt), self.w / 2 - self.titulo.shape[1] / 2, 92 - self.titulo.shape[0] / 2)
        dibujar_trazo(cv, self.rub[0], self.rub[1], eio(seg(t, *T['rub'])), self.w / 2, 158)
        n = 0
        for i, (spr, man) in enumerate(self.iconos):
            ti = T['iconos'][i]; X, Y = self.lay_ix[i], 300
            dt = t - ti
            if dt < 0:
                continue
            # mancha de tinta que se esparce bajo el ícono
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
            if pe > 0:
                pegar(cv, escribir(self.etq, pe), X - self.etq.shape[1] / 2, 435 - self.etq.shape[0] / 2)
            if dt >= 0.3:
                n += 1
        # contador
        if t >= T['cont']:
            al = cl((t - T['cont']) / 0.3)
            gx = self.lay_ix[-1] + 170
            pegar(cv, self.igual, gx - self.igual.shape[1] / 2, 300 - self.igual.shape[0] / 2, al)
            nx = gx + 145
            v = n * self.paso
            t_ult = T['iconos'][n - 1] + 0.3 if n > 0 else -9
            u = cl((t - t_ult) / 0.28)
            if n > 0 and u < 1:
                old = self.nums[(n - 1) * self.paso]
                pegar(cv, old, nx - old.shape[1] / 2, 296 - old.shape[0] / 2 - 40 * eo(u), (1 - u) * al)
                new = self.nums[v]
                pegar(cv, new, nx - new.shape[1] / 2, 296 - new.shape[0] / 2 + 40 * (1 - eo(u)), u * al)
            else:
                new = self.nums[v]
                pegar(cv, new, nx - new.shape[1] / 2, 296 - new.shape[0] / 2, al)
            dibujar_trazo(cv, self.circ[0], self.circ[1], eio(seg(t, *T['circ'])), gx + 82, 300, TINTA_ROJA, 0.92)
        return cv

    def dibuja(self, frame, t):
        T = self.T
        if t < T['cae'][0] or t > T['fuera'][1]:
            return
        if t < T['cierra'][0]:
            ab = eio(seg(t, *T['abre']))
        else:
            ab = 1 - eio(seg(t, *T['cierra']))
        wmin = 40
        wv = int(wmin + (self.w - wmin) * ab)
        al = eo(seg(t, *T['cae'])) * (1 - seg(t, *T['fuera']))
        dy = -50 * (1 - eo(seg(t, *T['cae']))) + 30 * seg(t, *T['fuera'])
        cx, cy = self.cx, self.cy + dy
        cv = self._contenido(t) if ab > 0.02 else self.papel
        xo = (self.w - wv) // 2
        sub = cv[:, xo:xo + wv]
        pegar(frame, sombra(sub, 14, 0.55), cx - wv / 2 + 14, cy - self.h / 2 + 18, al)
        pegar(frame, sub, cx - wv / 2, cy - self.h / 2, al)
        rw = self.rod.shape[1]; rh = self.rod.shape[0]
        for sx in (-1, 1):
            X = cx + sx * wv / 2
            pegar(frame, self.rod_sh, X - rw / 2 + 8, cy - rh / 2 + 12, al)
            pegar(frame, self.rod, X - rw / 2, cy - rh / 2, al)


# ----------------------------------------------------------------------------- 3) TARJETA DE JEFE
class tarjeta:
    """Tarjeta de pergamino quemado lanzada sobre la escena: foto en ventana de arco, título, subtítulo, sello de lacre."""
    def __init__(self, foto, titulo, lineas, letra='N', cx=420, cy=540, ancho=660, alto=770, ang=-3.0, t=None, seed=51):
        self.T = dict(entra=(0.0, 0.75), foto=(0.6, 1.4), titulo=(1.2, 2.1), rub=(2.0, 2.5),
                      lineas=[(2.4, 3.15), (3.0, 3.6)], sello=3.45, quema=(6.8, 7.7))
        if t:
            self.T.update(t)
        self.cx, self.cy, self.ang, self.w, self.h = cx, cy, ang, ancho, alto
        self.mg = 70
        base = quemar_bordes(papel(alto, ancho, seed), seed + 1, ancho=24, carbon=10, chamusca=70)
        self.base = np.zeros((alto + 2 * self.mg, ancho + 2 * self.mg, 4), np.float32)
        pegar(self.base, base, self.mg, self.mg)
        # ventana de arco con la foto
        fw, fh = ancho - 110, 330
        fx, fy = self.mg + 55, self.mg + 52
        im = Image.open(foto).convert('RGB')
        sc = max(fw / im.width, fh / im.height)
        im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
        ox, oy = (im.width - fw) // 2, (im.height - fh) // 2
        f = np.asarray(im, np.float32)[oy:oy + fh, ox:ox + fw] / 255
        g = cv2.cvtColor((f * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
        f = f * 0.62 + SEPIA[g] * 0.38
        m = Image.new('L', (fw, fh), 0); dm = ImageDraw.Draw(m)
        dm.rectangle([0, fw // 2 - 40, fw, fh], fill=255); dm.ellipse([0, 0, fw, fw - 60], fill=255)
        ma = np.asarray(m, np.float32) / 255
        ma = cv2.GaussianBlur(ma, (0, 0), 0.7)
        self.foto = premul(f, ma)
        self.foto_xy = (fx, fy)
        self.f_foto = campo_mancha(fh, fw, seed + 3, 0.5, 0.45, 0.42)
        # filetes de tinta siguiendo el arco
        dist = cv2.distanceTransform((ma < 0.5).astype(np.uint8), cv2.DIST_L2, 5)
        big = np.zeros((fh + 40, fw + 40), np.uint8); big[20:-20, 20:-20] = (ma > 0.5)
        dist = cv2.distanceTransform((1 - big).astype(np.uint8), cv2.DIST_L2, 5)
        ring = np.clip(1.6 - np.abs(dist - 3.5), 0, 1) + np.clip(0.9 - np.abs(dist - 11), 0, 1)
        ink = np.array(TINTA, np.float32) / 255
        self.filete = premul(np.broadcast_to(ink, ring.shape + (3,)).copy(), np.clip(ring, 0, 1))
        self.titulo = texto(titulo, 54, seed=21)
        self.lineas = [texto(l, 54, color=TINTA, seed=22 + i) for i, l in enumerate(lineas)]
        self.rub = rubrica(380, 10)
        self.sello = Caida(48, letra, seed + 5, self.T['sello'], gotas=5)
        Hc, Wc = self.base.shape[:2]
        self.f_quema = campo_mancha(Hc, Wc, seed + 7, 0.85, 0.95, 0.45)
        self.ty = self.mg + 52 + fh + 62

    def _canvas(self, t):
        T = self.T
        cv = self.base.copy()
        pf = seg(t, *T['foto'])
        if pf > 0:
            fx, fy = self.foto_xy
            pegar(cv, self.filete * min(1, pf * 2), fx - 20, fy - 20)
            pegar(cv, self.foto * revelar(self.f_foto, eo(pf), 0.08)[..., None], fx, fy)
        cxl = self.mg + self.w / 2
        pt = seg(t, *T['titulo'])
        if pt > 0:
            pegar(cv, escribir(self.titulo, pt), cxl - self.titulo.shape[1] / 2, self.ty - self.titulo.shape[0] / 2)
        dibujar_trazo(cv, self.rub[0], self.rub[1], eio(seg(t, *T['rub'])), cxl, self.ty + 50)
        for i, s in enumerate(self.lineas):
            pl = seg(t, *T['lineas'][i])
            if pl > 0:
                pegar(cv, escribir(s, pl), cxl - s.shape[1] / 2, self.ty + 112 + 58 * i - s.shape[0] / 2)
        self.sello.dibuja(cv, self.mg + self.w - 78, self.mg + 60, t)
        return cv

    def dibuja(self, frame, t):
        T = self.T
        if t < T['entra'][0] or t > T['quema'][1] + 0.05:
            return
        u = seg(t, *T['entra'])
        e = eback(u, 1.3)
        cx = lerp(-420, self.cx, e); cy = lerp(self.cy + 120, self.cy, eo(u)); ang = lerp(16, self.ang, e)
        cv = self._canvas(t)
        q = seg(t, *T['quema'])
        if q > 0:
            cv = quemar_spr(cv, self.f_quema, q)
        sp, _ = transformar(cv, ang)
        pegar_c(frame, sombra(sp, 12, 0.6), cx + 16, cy + 22, min(1, u * 3))
        pegar_c(frame, sp, cx, cy, min(1, u * 3))


# ----------------------------------------------------------------------------- 4) RÓTULO INFERIOR
class rotulo:
    """Tira de papel rasgado que se desenrolla desde la izquierda, sello de lacre con letra y texto escrito a pluma."""
    def __init__(self, txt, letra='V', x=800, y=868, ancho=1010, alto=118, t=None, seed=61):
        self.T = dict(abre=(0.0, 0.6), sello=0.55, texto=(0.95, 2.1), quema=(3.85, 4.7))
        if t:
            self.T.update(t)
        self.x, self.y, self.w, self.h = x, y, ancho, alto
        pap = papel(alto, ancho, seed)
        self.tira = borde_rasgado(pap, seed + 1, ancho=9)
        ink = np.array(TINTA, np.float32) / 255
        for yy_ in (16, alto - 18):
            self.tira[yy_:yy_ + 2, 120:ancho - 30, :3] = self.tira[yy_:yy_ + 2, 120:ancho - 30, :3] * 0.3 + ink * 0.7 * self.tira[yy_:yy_ + 2, 120:ancho - 30, 3:4]
        self.txt = texto(txt, 66, seed=31)
        self.sello = Caida(56, letra, seed + 2, self.T['sello'], gotas=6)
        self.mg = 80
        self.f_quema = campo_mancha(alto + 2 * self.mg, ancho + 2 * self.mg, seed + 3, 0.1, 0.5, 0.45)

    def dibuja(self, frame, t):
        T = self.T
        if t < T['abre'][0] or t > T['quema'][1] + 0.05:
            return
        pa = eo(seg(t, *T['abre']))
        wv = max(2, int(self.w * pa))
        cv = np.zeros((self.h + 2 * self.mg, self.w + 2 * self.mg, 4), np.float32)
        pegar(cv, self.tira[:, :wv], self.mg, self.mg)
        pt = seg(t, *T['texto'])
        if pt > 0:
            pegar(cv, escribir(self.txt, pt), self.mg + 128, self.mg + self.h / 2 - self.txt.shape[0] / 2 - 2)
        self.sello.dibuja(cv, self.mg + 52, self.mg + self.h / 2, t)
        q = seg(t, *T['quema'])
        if q > 0:
            cv = quemar_spr(cv, self.f_quema, q)
        dx = -30 * (1 - pa)
        pegar(frame, sombra(cv, 10, 0.6), self.x - self.mg + 10 + dx, self.y - self.mg + 14)
        pegar(frame, cv, self.x - self.mg + dx, self.y - self.mg)


# ----------------------------------------------------------------------------- transiciones
def quemado(A, B, p, campo):
    """El cuadro A se quema (borde de brasa y carbón) y deja ver B."""
    th = p * 1.2 - 0.1
    d = campo - th
    mB = np.clip(-d / 0.006, 0, 1)[..., None]
    ch = (np.clip(1 - d / 0.075, 0, 1) ** 1.5 * (d > 0))[..., None]
    glow = (np.exp(-(np.maximum(d, 0) / 0.007) ** 2) * np.clip(1 + d / 0.006, 0, 1))[..., None]
    A2 = A * (1 - 0.93 * ch) + CARBON * 0.93 * ch
    out = A2 * (1 - mB) + B * mB
    return np.clip(out + BRASA * glow * 0.85, 0, 1)


class Tinta:
    def __init__(self, seed=71):
        self.f1 = campo_mancha(H, W, seed, 0.62, 0.45, 0.45, escala=260)
        self.f2 = campo_mancha(H, W, seed + 1, 0.5, 0.5, 0.45, escala=260)
        g = ruido(H, W, 120, seed + 2, 3)
        self.col = (np.array([30, 19, 12], np.float32) / 255 * (0.8 + 0.5 * g[..., None])).astype(np.float32)

    def mezcla(self, A, B, p):
        if p < 0.5:
            m = revelar(self.f1, eo(p / 0.5), 0.05)[..., None]
            fr = np.exp(-((eo(p / 0.5) * 1.07 - self.f1 - 0.025) / 0.025) ** 2)[..., None] * 0.5
            return A * (1 - m) + self.col * m + np.array([0.25, 0.15, 0.07], np.float32) * fr * (1 - m)
        m = revelar(self.f2, eo((p - 0.5) / 0.5), 0.07)[..., None]
        return self.col * (1 - m) + B * m


# ----------------------------------------------------------------------------- montaje del video de muestra
class Video:
    def __init__(self):
        P = lambda n: os.path.join(SRC, 'pegatinas', n)
        self.mapa = mapa_ruta(os.path.join(SRC, 'mapas', 'ungoro_norte.jpg'), (43.6, 23.0), (47.3, 10.8),
                              'CRÁTER DE UN’GORO', 'Refugio de los Mariscales', 'BANCAL DEL CREADOR · 58-60',
                              sub_a='vuelo: Gryfe', foto_a=P('refugio_mariscales.png'), foto_b=P('bancal_creador.png'),
                              foto_zona=P('ungoro.png'))
        self.fondo = FondoJuego()
        self.c091 = Clip(os.path.join(SRC, 'medios', 'scene-091.mp4'))
        self.c093 = Clip(os.path.join(SRC, 'medios', 'scene-093.mp4'))
        self.ficha = ficha('N.º 15 · Sin los 60 cristales',
                           [P('o_cristal_rojo.png'), P('o_cristal_amarillo.png'), P('o_cristal_azul.png'), P('o_cristal_verde.png')])
        self.tarjeta = tarjeta(P('bancal_creador.png'), 'JEFA FINAL: NANAYA', ['cambia de elemento', 'cada 25 %'])
        self.rotulo = rotulo('Sin cristales: solo 5 jefes', 'V', ancho=980)
        self.f_q = campo_mancha(H, W, 81, 0.78, 0.30, 0.28, escala=420)
        self.tinta = Tinta()
        tag = texto('ESTILO 1 · CARTÓGRAFO DE PERGAMINO', 22, fnt='BOOKOSB.TTF', seed=91, halo_r=4)
        th, tw = tag.shape[:2]
        tira = borde_rasgado(papel(th + 4, tw + 26, 92), 93, ancho=5)
        pegar(tira, tag, 13, 2)
        self.tag = tira

    def s1(self, t):
        return self.mapa.cuadro(t)

    def s2(self, t):
        f = self.fondo.trata(self.c091.get((t - 10.6) * FPS * 0.9))
        self.ficha.dibuja(f, t - 11.3)
        return f

    def s3(self, t):
        f = self.fondo.trata(self.c093.get((t - 21.0) * FPS))
        self.tarjeta.dibuja(f, t - 21.4)
        self.rotulo.dibuja(f, t - 24.6)
        return f

    def cuadro(self, t):
        if t < 10.6:
            f = self.s1(t)
        elif t < 11.5:
            f = quemado(self.s1(t), self.s2(t), seg(t, 10.6, 11.5), self.f_q)
        elif t < 20.6:
            f = self.s2(t)
        elif t < 21.4:
            p = seg(t, 20.6, 21.4)
            f = self.tinta.mezcla(self.s2(t) if p < 0.5 else None, self.s3(t) if p >= 0.5 else None, p)
        else:
            f = self.s3(t)
        pegar(f, self.tag, 20, 14, 0.93 * eo(seg(t, 0.2, 0.8)))
        f = f * (1 - eio(seg(t, 29.35, 30.0)))
        return np.clip(f, 0, 1)


def a_u8(f):
    return (np.clip(f, 0, 1) * 255 + 0.5).astype(np.uint8)


def render():
    v = Video()
    wav = os.path.join(SRC, 'audio', 'wow', 'nlXOcybLHxc.wav')
    cmd = [FFMPEG, '-y', '-v', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS), '-i', '-',
           '-ss', '4', '-t', str(DUR), '-i', wav,
           '-filter_complex', '[1:a]loudnorm=I=-18:TP=-2:LRA=11,aresample=48000,'
                              'afade=t=in:st=0:d=1.5,afade=t=out:st=27.4:d=2.6[a]',
           '-map', '0:v', '-map', '[a]', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
           '-threads', '4', '-filter_threads', '1', '-c:a', 'aac', '-b:a', '192k', '-t', str(DUR), '-movflags', '+faststart', SALIDA]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        pr.stdin.write(a_u8(v.cuadro(i / FPS)).tobytes())
        if i % 60 == 0:
            print(f'cuadro {i}/{n}', flush=True)
    pr.stdin.close(); pr.wait()
    print('listo', SALIDA)


def hoja():
    os.makedirs(TMP, exist_ok=True)
    tiempos = [1.25 + 2.5 * i for i in range(12)]
    tw, th = 640, 360
    lienzo = Image.new('RGB', (tw * 4, th * 3), (20, 20, 20))
    d = ImageDraw.Draw(lienzo)
    for i, t in enumerate(tiempos):
        p = os.path.join(TMP, f'h_{i}.jpg')
        subprocess.run([FFMPEG, '-y', '-v', 'error', '-ss', f'{t:.3f}', '-i', SALIDA, '-frames:v', '1', '-vf', f'scale={tw}:{th}', p], check=True)
        lienzo.paste(Image.open(p), ((i % 4) * tw, (i // 4) * th))
        d.rectangle([(i % 4) * tw, (i // 4) * th + th - 26, (i % 4) * tw + 70, (i // 4) * th + th], fill=(0, 0, 0))
        d.text(((i % 4) * tw + 6, (i // 4) * th + th - 22), f'{t:.2f}s', fill=(255, 255, 255), font=fuente('arial.ttf', 18))
    lienzo.save(os.path.join(AQUI, 'hoja.jpg'), quality=90)
    print('hoja', os.path.join(AQUI, 'hoja.jpg'))


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--cuadros', nargs='*', type=float)
    ap.add_argument('--hoja', action='store_true')
    a = ap.parse_args()
    if a.cuadros:
        os.makedirs(TMP, exist_ok=True)
        v = Video()
        for t in a.cuadros:
            Image.fromarray(a_u8(v.cuadro(t))).save(os.path.join(TMP, f'c_{t:05.2f}.jpg'), quality=90)
            print('cuadro', t)
    elif a.hoja:
        hoja()
    else:
        render()
        hoja()
