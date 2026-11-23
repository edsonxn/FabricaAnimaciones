# -*- coding: utf-8 -*-
"""ESTILO 5 · CUADERNO DE EXPLORADOR (acuarela y lápiz) — propuesta de kit para Crónicas de Warcraft (22-nov-2026).

Todo por código (numpy / PIL / opencv + ffmpeg), cuadro a cuadro.
Piezas reutilizables (pensadas para pasarlas al kit si se elige este estilo):
  - MapaRuta  / mapa_ruta(...)  -> mapa en acuarela con bordes de mancha, ruta = doble trazo de lápiz + aguada, X pintada,
                                    recortes con cinta para los rótulos y polaroid de lo nombrado.
  - Ficha     / ficha(...)      -> hoja de cuaderno con clip, título manuscrito, íconos recortados y pegados con cinta, contador.
  - Tarjeta   / tarjeta(...)    -> polaroid de la foto + hoja con clip (título, subtítulo, gráfico de cuartos en acuarela).
  - Rotulo    / rotulo(...)     -> tira de papel rasgado con aguada y sello de tinta roja (lower third).
  - acuarelar(frame)            -> trata el gameplay como acuarela + lápiz sobre papel.
  - transicion_aguada(...)      -> cortinilla de mancha de acuarela.

Uso:
  python estilo_5.py                 # render completo (video + hoja)
  python estilo_5.py --cuadro 9.5 salida.png
  python estilo_5.py --hoja          # solo la hoja de revisión desde el mp4
"""
import os
import sys
import math
import functools
import subprocess

import numpy as np
import cv2
from PIL import Image, ImageDraw, ImageFont

cv2.setNumThreads(4)

AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = r'C:\FabricaAnimaciones\videos\wow_errores_60'
FFMPEG = r'C:\ffmpeg\bin\ffmpeg.exe'
CAVEAT = os.path.join(AQUI, 'fuentes', 'Caveat.ttf')
W, H, FPS, DUR = 1920, 1080, 30, 30.0
SALIDA = os.path.join(AQUI, 'estilo_5_cuaderno.mp4')
HOJA = os.path.join(AQUI, 'hoja.jpg')

# Paleta (tinta y pigmentos, 0..1 salvo las tintas de texto que van 0..255)
TINTA = (38, 32, 30)
LAPIZ = (52, 49, 48)
PLUMA = (32, 52, 112)
ROJO = np.array([0.80, 0.20, 0.18], np.float32)
AZUL = np.array([0.32, 0.52, 0.82], np.float32)
OCRE = np.array([0.93, 0.70, 0.36], np.float32)
VERDE = np.array([0.42, 0.68, 0.36], np.float32)
AMARILLO = np.array([0.98, 0.82, 0.30], np.float32)
SIENA = np.array([0.80, 0.42, 0.26], np.float32)


# ───────────────────────────── utilidades ─────────────────────────────
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def prog(t, a, b):
    return clamp((t - a) / (b - a)) if b > a else float(t >= a)


def e_out(x):
    return 1 - (1 - x) ** 3


def e_in(x):
    return x ** 3


def e_inout(x):
    return 4 * x ** 3 if x < 0.5 else 1 - (-2 * x + 2) ** 3 / 2


def e_back(x, s=1.6):
    x -= 1
    return 1 + x * x * ((s + 1) * x + s)


def smooth(e0, e1, x):
    t = np.clip((x - e0) / (e1 - e0), 0, 1)
    return t * t * (3 - 2 * t)


@functools.lru_cache(None)
def fbm(h, w, seed, base=6, octavas=4):
    """Ruido suave (≈ -1..1). Cacheado: no mutar el resultado."""
    rng = np.random.default_rng(seed)
    acc = np.zeros((h, w), np.float32)
    amp, tot = 1.0, 0.0
    for o in range(octavas):
        n = base * 2 ** o
        gx = n + 3
        gy = max(3, int(round(n * h / max(w, 1))) + 3)
        g = rng.random((gy, gx)).astype(np.float32)
        acc += amp * cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= 0.5
    acc /= tot
    acc = (acc - acc.mean()) / (acc.std() + 1e-6) * 0.33
    return acc


def _papel_global():
    rng = np.random.default_rng(11)
    manchas = fbm(H, W, 3, 3, 3)
    fibra = fbm(H, W, 4, 60, 2)
    grano = cv2.GaussianBlur(rng.normal(0, 1, (H, W)).astype(np.float32), (0, 0), 0.7)
    lum = 1 + 0.035 * manchas + 0.02 * grano + 0.02 * fibra
    gran = np.clip(1 + 0.10 * fbm(H, W, 9, 90, 2) + 0.05 * grano, 0.7, 1.2)   # granulado del pigmento
    return lum.astype(np.float32), gran.astype(np.float32)


LUM, GRAN = _papel_global()
CREMA = np.array([0.955, 0.930, 0.872], np.float32)
PAPEL = np.clip(CREMA[None, None, :] * LUM[..., None], 0, 1)


def lum_crop(h, w, x=0, y=0):
    x, y = x % max(1, W - w), y % max(1, H - h)
    return LUM[y:y + h, x:x + w]


# ─────────────────── capas (RGBA float premultiplicado) ───────────────────
def pil_a_capa(im):
    a = np.asarray(im.convert('RGBA')).astype(np.float32) / 255.0
    a[..., :3] *= a[..., 3:4]
    return a


def over(dst, capa, x, y, op=1.0):
    """Compone capa premultiplicada sobre dst RGB float (in place)."""
    if capa is None:
        return
    h, w = capa.shape[:2]
    Hh, Ww = dst.shape[:2]
    x, y = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(0, x), max(0, y), min(Ww, x + w), min(Hh, y + h)
    if x1 <= x0 or y1 <= y0 or op <= 0:
        return
    s = capa[y0 - y:y1 - y, x0 - x:x1 - x]
    a = s[..., 3:4] * op
    d = dst[y0:y1, x0:x1]
    d *= (1 - a)
    d += s[..., :3] * op


def over_capa(dst, capa, x, y, op=1.0):
    """Compone capa premultiplicada sobre otra capa premultiplicada (in place)."""
    h, w = capa.shape[:2]
    Hh, Ww = dst.shape[:2]
    x, y = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(0, x), max(0, y), min(Ww, x + w), min(Hh, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    s = capa[y0 - y:y1 - y, x0 - x:x1 - x] * op
    a = s[..., 3:4]
    d = dst[y0:y1, x0:x1]
    d *= (1 - a)
    d += s


def pinta(dst, alfa, color, x, y):
    """Pigmento en modo multiplicar (acuarela / tinta de sello). dst RGB o RGBA premultiplicada opaca."""
    h, w = alfa.shape[:2]
    Hh, Ww = dst.shape[:2]
    x, y = int(round(x)), int(round(y))
    x0, y0, x1, y1 = max(0, x), max(0, y), min(Ww, x + w), min(Hh, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    a = alfa[y0 - y:y1 - y, x0 - x:x1 - x, None]
    d = dst[y0:y1, x0:x1, :3]
    d *= 1 - a * (1 - np.asarray(color, np.float32))


def transformar(capa, ang=0.0, esc=1.0):
    if abs(ang) < 0.02 and abs(esc - 1) < 0.002:
        return capa
    h, w = capa.shape[:2]
    r = math.radians(ang)
    nw = int(abs(w * math.cos(r) * esc) + abs(h * math.sin(r) * esc)) + 4
    nh = int(abs(w * math.sin(r) * esc) + abs(h * math.cos(r) * esc)) + 4
    M = cv2.getRotationMatrix2D((w / 2, h / 2), ang, esc)
    M[0, 2] += nw / 2 - w / 2
    M[1, 2] += nh / 2 - h / 2
    return cv2.warpAffine(capa, M, (nw, nh), flags=cv2.INTER_LINEAR,
                          borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))


def pegar_centro(dst, capa, cx, cy, ang=0.0, esc=1.0, op=1.0):
    c = transformar(capa, ang, esc)
    h, w = c.shape[:2]
    over(dst, c, cx - w / 2, cy - h / 2, op)


def sombra_alfa(alfa, blur=10, op=0.32):
    return np.clip(cv2.GaussianBlur(alfa, (0, 0), blur) * op, 0, 1)


def con_sombra(capa, sombra, dx=8, dy=12):
    """sombra = alfa ya difuminada (mismo tamaño que capa). Devuelve capa con margen (centro conservado)."""
    h, w = capa.shape[:2]
    m = 36
    out = np.zeros((h + 2 * m, w + 2 * m, 4), np.float32)
    out[m + dy:m + dy + h, m + dx:m + dx + w, 3] = sombra
    over_capa(out, capa, m, m)
    return out


# ───────────────────────────── texto a mano ─────────────────────────────
@functools.lru_cache(None)
def fuente(tam, peso=700):
    f = ImageFont.truetype(CAVEAT, tam)
    try:
        f.set_variation_by_axes([peso])
    except Exception:
        pass
    return f


def tam_que_cabe(texto, tam, maxw, peso=700):
    while tam > 20 and fuente(tam, peso).getlength(texto) > maxw:
        tam -= 2
    return tam


class Texto:
    """Texto manuscrito (Caveat) como capa; .escrito(p) lo revela de izquierda a derecha como si se escribiera."""

    def __init__(self, texto, tam, peso=700, color=TINTA, pad=10, seed=0):
        f = fuente(tam, peso)
        self.texto, self.f = texto, f
        asc, desc = f.getmetrics()
        w = int(f.getlength(texto)) + 2 * pad + 8
        h = asc + desc + 2 * pad
        im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
        ImageDraw.Draw(im).text((pad, pad), texto, font=f, fill=tuple(color) + (255,))
        c = pil_a_capa(im)
        tex = np.clip(0.86 + 0.5 * fbm(h, w, 100 + seed, 20, 2), 0.7, 1.0)    # tinta no uniforme
        c *= tex[..., None]
        self.capa, self.w, self.h, self.pad, self.asc = c, w, h, pad, asc
        self.x_ini = np.arange(w, dtype=np.float32)

    def x_de(self, sub):
        i = self.texto.find(sub)
        return self.pad + self.f.getlength(self.texto[:i]), self.f.getlength(sub)

    def escrito(self, p, suave=36):
        if p >= 1:
            return self.capa
        borde = p * (self.w + suave)
        m = np.clip((borde - self.x_ini) / suave, 0, 1)
        return self.capa * m[None, :, None]


# ───────────────────────────── trazos de lápiz ─────────────────────────────
def remuestrear(pts, paso=2.0):
    pts = np.asarray(pts, np.float64)
    seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
    L = np.concatenate([[0], np.cumsum(seg)])
    n = max(2, int(L[-1] / paso))
    s = np.linspace(0, L[-1], n)
    return np.stack([np.interp(s, L, pts[:, 0]), np.interp(s, L, pts[:, 1])], 1)


def bezier(p0, c, p1, n=240):
    t = np.linspace(0, 1, n)[:, None]
    p0, c, p1 = map(lambda v: np.asarray(v, float), (p0, c, p1))
    return (1 - t) ** 2 * p0 + 2 * (1 - t) * t * c + t ** 2 * p1


def temblor(pts, amp=1.5, seed=0, frec=0.025):
    pts = remuestrear(pts)
    n = len(pts)
    rng = np.random.default_rng(seed)
    k = max(4, int(n * frec))
    g = rng.normal(0, 1, k)
    wv = np.interp(np.linspace(0, k - 1, n), np.arange(k), g)
    d = np.gradient(pts, axis=0)
    nr = np.stack([-d[:, 1], d[:, 0]], 1)
    nr /= np.linalg.norm(nr, axis=1, keepdims=True) + 1e-9
    return pts + nr * (wv * amp)[:, None]


def parcial(pts, f):
    k = int(round(clamp(f) * (len(pts) - 1)))
    return pts[:k + 1]


def circulo_mano(cx, cy, rx, ry, vueltas=1.12, a0=-110, seed=0):
    rng = np.random.default_rng(seed)
    ph = rng.random() * 6.28
    a = np.radians(a0) + np.linspace(0, 2 * np.pi * vueltas, 260)
    k = np.linspace(0, 1, len(a))
    r = 1 + 0.035 * np.sin(3 * a + ph) + 0.07 * k
    return np.stack([cx + rx * r * np.cos(a), cy + ry * r * np.sin(a)], 1)


def flecha_mano(p0, p1, curva=0.22, punta=24, seed=0):
    p0, p1 = np.asarray(p0, float), np.asarray(p1, float)
    d = p1 - p0
    nrm = np.array([-d[1], d[0]]) / (np.linalg.norm(d) + 1e-9)
    c = (p0 + p1) / 2 + nrm * np.linalg.norm(d) * curva
    cuerpo = temblor(bezier(p0, c, p1), 1.0, seed)
    v = cuerpo[-1] - cuerpo[-6]
    v /= np.linalg.norm(v) + 1e-9
    puntas = []
    for s in (1, -1):
        ang = math.radians(152 * s)
        r = np.array([v[0] * math.cos(ang) - v[1] * math.sin(ang), v[0] * math.sin(ang) + v[1] * math.cos(ang)])
        puntas.append(temblor([cuerpo[-1], cuerpo[-1] + r * punta], 0.5, seed + 7 + s))
    return cuerpo, puntas


class Trazo:
    """Línea de lápiz con 2 pasadas temblorosas; .dibujar(draw, f) dibuja la fracción f."""

    def __init__(self, pts, color=LAPIZ, ancho=3, alfa=210, pasadas=2, seed=0, amp=0.9):
        base = remuestrear(pts)
        self.vars = [temblor(base, amp, seed + 31 * k) for k in range(pasadas)]
        self.color, self.ancho, self.alfa = tuple(color), ancho, alfa

    def dibujar(self, d, f, ox=0, oy=0):
        if f <= 0:
            return
        for k, v in enumerate(self.vars):
            p = parcial(v, f)
            if len(p) < 2:
                continue
            al = int(self.alfa * (1 if k == 0 else 0.5))
            d.line([(x - ox, y - oy) for x, y in p], fill=self.color + (al,),
                   width=self.ancho if k == 0 else max(1, self.ancho - 1), joint='curve')


def capa_trazos(w, h, dibujos, gx=0, gy=0):
    """dibujos = lista de (Trazo, f). Devuelve capa premultiplicada con textura de grafito."""
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    alguno = False
    for tr, f in dibujos:
        if f > 0:
            tr.dibujar(d, f)
            alguno = True
    if not alguno:
        return None
    c = pil_a_capa(im)
    g = np.clip(0.78 + 0.45 * (GRAN[gy % (H - h + 1):gy % (H - h + 1) + h, gx % (W - w + 1):gx % (W - w + 1) + w] - 0.8) / 0.4, 0.78, 1)
    c *= g[..., None]
    return c


# ───────────────────────────── acuarela ─────────────────────────────
@functools.lru_cache(None)
def campo_mancha(w, h, seed, rug=0.32, forma='circulo'):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    xx = (xx + 0.5) / w * 2 - 1
    yy = (yy + 0.5) / h * 2 - 1
    if forma == 'caja':
        d = (np.abs(xx) ** 7 + np.abs(yy) ** 7) ** (1 / 7)
    else:
        d = np.sqrt(xx ** 2 + yy ** 2)
    return (d + rug * fbm(h, w, seed, 4, 4)).astype(np.float32)


def acuarela_alfa(campo, p, dens=0.55, borde=0.5, ancho=0.05):
    """Mancha que se extiende: p 0..1. Borde más oscuro (pigmento acumulado)."""
    r = p * 0.98
    dentro = smooth(r + 0.012, r - 0.012, campo)
    filo = np.exp(-((campo - (r - 0.025)) / ancho) ** 2) * dentro
    return np.clip(dentro * (dens + borde * filo), 0, 1)


class Mancha:
    def __init__(self, w, h, color, seed=0, rug=0.32, dens=0.55, borde=0.5, forma='circulo'):
        self.w, self.h, self.color = w, h, color
        self.campo = campo_mancha(w, h, seed, rug, forma)
        self.dens, self.borde = dens, borde
        self.gran = GRAN[(seed * 37) % (H - h):(seed * 37) % (H - h) + h, (seed * 53) % (W - w):(seed * 53) % (W - w) + w]

    def alfa(self, p):
        return acuarela_alfa(self.campo, p, self.dens, self.borde) * self.gran

    def pintar(self, dst, p, cx, cy, op=1.0):
        if p <= 0:
            return
        pinta(dst, self.alfa(p) * op, self.color, cx - self.w / 2, cy - self.h / 2)


class Pincelada:
    """Banda de aguada horizontal que avanza de izquierda a derecha (subrayados, resaltados)."""

    def __init__(self, w, h, color, seed=0, dens=0.5, borde=0.45):
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        n = fbm(h, w, seed, 5, 3)
        self.fx = xx / w + 0.06 * n
        banda = np.abs((yy + 0.5) / h * 2 - 1) + 0.35 * fbm(h, w, seed + 1, 8, 3)
        self.dentro = smooth(0.92, 0.80, banda)
        self.filo = np.exp(-((banda - 0.80) / 0.09) ** 2)
        self.w, self.h, self.color, self.dens, self.borde = w, h, color, dens, borde
        self.gran = GRAN[seed % 400:seed % 400 + h, seed % 900:seed % 900 + w]

    def alfa(self, p):
        av = smooth(p * 1.08 + 0.01, p * 1.08 - 0.03, self.fx)
        frente = np.exp(-((self.fx - (p * 1.08 - 0.03)) / 0.02) ** 2) * (p < 1)
        a = self.dentro * av * (self.dens + self.borde * np.maximum(self.filo, frente))
        return np.clip(a * self.gran, 0, 1)


# ───────────────────────────── papeles ─────────────────────────────
def recorte_papel(w, h, seed=0, tono=(0.975, 0.962, 0.925), amp=5.0):
    """Trozo de papel rasgado (capa premultiplicada)."""
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    d = np.minimum(np.minimum(xx, w - 1 - xx), np.minimum(yy, h - 1 - yy))
    v = d + amp * fbm(h, w, seed, 14, 3) * 2.2
    a = smooth(amp - 0.8, amp + 0.8, v)
    fibra = smooth(amp + 4.5, amp + 0.8, v) * a           # filo blanco de fibra rasgada
    rgb = np.array(tono, np.float32)[None, None, :] * lum_crop(h, w, seed * 13, seed * 7)[..., None]
    rgb = rgb + (1 - rgb) * 0.65 * fibra[..., None]
    c = np.zeros((h, w, 4), np.float32)
    c[..., :3] = rgb * a[..., None]
    c[..., 3] = a
    return c


def hoja_cuaderno(w, h, seed=0, renglon=46, margen=96, y0=None, rasgado_arriba=True):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
    rgb = np.array([0.988, 0.980, 0.955], np.float32)[None, None, :] * lum_crop(h, w, seed * 5, seed * 11)[..., None]
    y0 = renglon * 2 if y0 is None else y0
    for y in range(y0, h - 10, renglon):
        rgb[y:y + 2, :] *= np.array([0.80, 0.87, 0.97], np.float32)
    rgb[:, margen:margen + 2] *= np.array([0.97, 0.66, 0.66], np.float32)
    if rasgado_arriba:
        borde = 9 + 6 * fbm(1, w, seed + 3, 30, 3)[0] * 2.5 + 3 * np.sin(np.arange(w) * 0.9)
        a = smooth(borde - 0.8, borde + 0.8, yy)
        fibra = smooth(borde + 5, borde + 0.8, yy)
        rgb = rgb + (1 - rgb) * 0.7 * fibra[..., None]
    else:
        a = np.ones((h, w), np.float32)
    lado = np.minimum(np.minimum(xx, w - 1 - xx), h - 1 - yy)
    a = a * smooth(0, 1.5, lado)
    c = np.zeros((h, w, 4), np.float32)
    c[..., :3] = rgb * a[..., None]
    c[..., 3] = a
    return c


def cinta(w=150, h=42, seed=0):
    """Trozo de cinta de papel semitransparente con extremos dentados."""
    rng = np.random.default_rng(seed)
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    izq = [(rng.uniform(0, 7), y) for y in np.linspace(0, h, 7)]
    der = [(w - rng.uniform(0, 7), y) for y in np.linspace(h, 0, 7)]
    d.polygon(izq + der, fill=(236, 226, 190, 175))
    for k in range(3):
        y = rng.uniform(4, h - 4)
        d.line([(6, y), (w - 6, y)], fill=(255, 250, 230, 40), width=2)
    return pil_a_capa(im)


def clip_metal(seed=0):
    """Sujetapapeles dibujado (capa premultiplicada, 74x190)."""
    w, h = 74, 190
    im = Image.new('RGBA', (w * 3, h * 3), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    s = 3
    # tres "U" anidadas como un clip real
    def u(x0, y0, x1, y1, r, col, ww):
        d.arc([x0 * s, y0 * s, x1 * s, (y0 + 2 * r) * s], 180, 360, fill=col, width=ww * s)
        d.line([(x0 * s, (y0 + r) * s), (x0 * s, y1 * s)], fill=col, width=ww * s)
        d.line([(x1 * s, (y0 + r) * s), (x1 * s, y1 * s)], fill=col, width=ww * s)
    col, hi = (120, 124, 130, 255), (215, 220, 228, 255)
    u(8, 4, 66, 150, 29, col, 5)
    d.arc([8 * s, 120 * s, 54 * s, 184 * s], 0, 180, fill=col, width=5 * s)
    u(20, 22, 54, 160, 17, col, 5)
    d.line([(20 * s, 150 * s), (20 * s, 120 * s)], fill=col, width=5 * s)
    u(9, 5, 65, 150, 28, hi, 1)
    u(21, 23, 53, 160, 16, hi, 1)
    im = im.resize((w, h), Image.LANCZOS)
    return pil_a_capa(im)


def recorte_foto(ruta, ancho, borde=10, ang=0.0, cinta_seed=None):
    """Imagen impresa y recortada con borde blanco (para íconos y fotos pequeñas)."""
    im = Image.open(ruta).convert('RGBA')
    k = ancho / im.width
    im = im.resize((ancho, max(1, int(im.height * k))), Image.LANCZOS)
    w, h = im.width + 2 * borde, im.height + 2 * borde
    base = recorte_papel(w, h, seed=hash(ruta) % 97, tono=(0.99, 0.985, 0.97), amp=2.5)
    over_capa(base, pil_a_capa(im), borde, borde)
    return base


def polaroid(ruta, ancho_foto=520, pie=None, seed=0):
    im = Image.open(ruta).convert('RGB')
    k = ancho_foto / im.width
    im = im.resize((ancho_foto, int(im.height * k)), Image.LANCZOS)
    foto = np.asarray(im).astype(np.float32) / 255
    foto = np.clip(foto * 1.05 + 0.02, 0, 1) * (0.96 + 0.04 * lum_crop(foto.shape[0], foto.shape[1])[..., None])
    b, bb = 20, 92 if pie else 26
    w, h = ancho_foto + 2 * b, foto.shape[0] + b + bb
    c = recorte_papel(w, h, seed=seed, tono=(0.985, 0.978, 0.960), amp=1.6)
    c[b:b + foto.shape[0], b:b + ancho_foto, :3] = foto
    if pie:
        t = Texto(pie, tam_que_cabe(pie, 52, ancho_foto - 20, 600), peso=600, color=LAPIZ, seed=seed)
        over_capa(c, t.capa, (w - t.w) / 2, b + foto.shape[0] + (bb - t.h) / 2 + 2)
    # cinta arriba
    m = 30
    out = np.zeros((h + m, w, 4), np.float32)
    over_capa(out, c, 0, m)
    ct = transformar(cinta(170, 46, seed + 5), -4)
    over_capa(out, ct, w / 2 - ct.shape[1] / 2, m - ct.shape[0] / 2 + 4)
    return out


class Nota:
    """Recorte de papel rasgado con cinta, con líneas manuscritas que se escriben una tras otra."""

    def __init__(self, lineas, seed=0, ang=-2.0, padx=34, pady=18, subrayar=None, color_sub=OCRE, vel=0.024):
        self.txt = [Texto(l['texto'], l['tam'], l.get('peso', 700), l.get('color', TINTA), seed=seed + i)
                    for i, l in enumerate(lineas)]
        w = int(max(t.w for t in self.txt) + 2 * padx)
        h = int(sum(t.h for t in self.txt) - 10 * (len(self.txt) - 1) + 2 * pady)
        self.m = 30
        self.W, self.H = w, h + self.m
        base = np.zeros((self.H, self.W, 4), np.float32)
        over_capa(base, recorte_papel(w, h, seed), 0, self.m)
        self.sombra_ref = base[..., 3].copy()
        ct = transformar(cinta(130, 40, seed + 9), 3 if seed % 2 else -5)
        over_capa(base, ct, w * 0.5 - ct.shape[1] / 2, self.m - ct.shape[0] / 2 + 6)
        self.base = base
        self.sombra = sombra_alfa(self.sombra_ref, 9, 0.30)
        self.pos, y = [], self.m + pady
        self.t0 = []
        tt = 0.25
        for t in self.txt:
            self.pos.append((padx + (w - 2 * padx - t.w) / 2, y))
            dur = 0.2 + vel * len(t.texto)
            self.t0.append((tt, tt + dur))
            tt += dur + 0.08
            y += t.h - 10
        self.fin_escritura = tt
        self.ang = ang
        self.sub = None
        if subrayar:
            i, s = subrayar
            x, sw = self.txt[i].x_de(s)
            px, py = self.pos[i]
            hh = int(self.txt[i].h * 0.42)
            self.sub = (Pincelada(int(sw + 24), hh, color_sub, seed + 3, 0.55, 0.5),
                        px + x - 12, py + self.txt[i].h * 0.52)

    def capa(self, t):
        c = self.base.copy()
        if self.sub:
            p = prog(t, self.fin_escritura - 0.1, self.fin_escritura + 0.45)
            if p > 0:
                pc, x, y = self.sub
                pinta(c, pc.alfa(p), pc.color, x, y)
        for t_, (x, y), (a, b) in zip(self.txt, self.pos, self.t0):
            p = prog(t, a, b)
            if p > 0:
                over_capa(c, t_.escrito(p), x, y)
        return con_sombra(c, self.sombra, 6, 9)

    def dibujar(self, dst, t, cx, cy, salida=None):
        a = prog(t, 0, 0.45)
        if a <= 0:
            return
        e = e_back(a)
        esc = 0.86 + 0.14 * e
        ang = self.ang + (1 - e) * 9
        dy = -(1 - e_out(a)) * 34
        op = min(1.0, a * 2.5)
        if salida is not None and t > salida:
            q = e_in(prog(t, salida, salida + 0.45))
            op *= 1 - q
            dy += q * 50
            ang += q * 6
        if op <= 0:
            return
        pegar_centro(dst, self.capa(t), cx, cy + dy, ang, esc, op)


# ───────────────────────────── gameplay en acuarela ─────────────────────────────
class Clip:
    def __init__(self, ruta, inicio=0.0):
        self.ruta, self.inicio = ruta, inicio
        self.cap = cv2.VideoCapture(ruta)
        self.n = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.cur, self.ult = -1, None

    def cuadro(self, t):
        i = min(self.n - 1, max(0, int((t + self.inicio) * FPS)))
        if i < self.cur or i > self.cur + 45 or self.ult is None:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, i)
            self.cur = i - 1
        while self.cur < i:
            ok, f = self.cap.read()
            if not ok:
                break
            self.ult, self.cur = f, self.cur + 1
        return self.ult


@functools.lru_cache(None)
def _marco_pagina(margen=34, seed=21):
    """Máscara del gameplay 'pintado' dentro de la página: borde irregular de acuarela."""
    c = campo_mancha(W // 4, H // 4, seed, 0.10, 'caja')
    c = cv2.resize(c, (W, H), interpolation=cv2.INTER_CUBIC)
    lim = 1 - margen / (H / 2)
    a = smooth(lim + 0.006, lim - 0.006, c)
    filo = np.exp(-((c - (lim - 0.01)) / 0.012) ** 2) * a
    return a.astype(np.float32), filo.astype(np.float32)


def acuarelar(bgr):
    """Gameplay -> acuarela + lápiz sobre papel (RGB float 1080p)."""
    small = cv2.resize(bgr, (480, 270), interpolation=cv2.INTER_AREA)
    for _ in range(2):
        small = cv2.bilateralFilter(small, 7, 40, 6)
    up = cv2.resize(small, (W, H), interpolation=cv2.INTER_CUBIC).astype(np.float32) / 255
    rgb = up[..., ::-1]
    rgb = np.power(np.clip(rgb, 0, 1), 0.72)                         # aclarar (la acuarela es luminosa)
    gris = rgb.mean(axis=2, keepdims=True)
    rgb = gris + (rgb - gris) * 1.12
    rgb = 0.1 + 0.88 * rgb
    mid = cv2.resize(bgr, (960, 540), interpolation=cv2.INTER_AREA)
    g = cv2.cvtColor(mid, cv2.COLOR_BGR2GRAY).astype(np.float32)
    bl = cv2.GaussianBlur(255 - g, (0, 0), 5)
    sk = np.clip(g * 255 / (256 - bl), 0, 255) / 255                 # boceto a lápiz (color dodge)
    sk = cv2.resize(sk, (W, H), interpolation=cv2.INTER_LINEAR)
    sk = 0.45 + 0.55 * np.power(sk, 2.2)
    out = np.clip(rgb, 0, 1) * sk[..., None] * (0.9 + 0.1 * LUM[..., None]) * (0.94 + 0.06 * GRAN[..., None])
    a, filo = _marco_pagina()
    out = out * (1 - 0.30 * filo[..., None])
    return PAPEL * (1 - a[..., None]) + out * a[..., None] * PAPEL


def transicion_aguada(A, B, p, seed=5, color=SIENA):
    """Cortinilla de acuarela de A a B (p 0..1) con frente de pigmento."""
    c = campo_mancha(W // 4, H // 4, seed, 0.0, 'circulo')
    yy, xx = np.mgrid[0:H // 4, 0:W // 4].astype(np.float32)
    f = (xx / (W // 4)) * 0.75 + (1 - yy / (H // 4)) * 0.25 + 0.16 * fbm(H // 4, W // 4, seed, 5, 4)
    f = cv2.resize(f, (W, H), interpolation=cv2.INTER_CUBIC)
    thr = -0.15 + p * 1.35
    m = smooth(thr + 0.015, thr - 0.015, f)[..., None]
    banda = np.exp(-((f - thr) / 0.035) ** 2)[..., None] * (0 < p < 1)
    out = A * (1 - m) + B * m
    out *= 1 - 0.55 * banda * (1 - color) * GRAN[..., None]
    return out


# ───────────────────────────── piezas del kit ─────────────────────────────
class MapaRuta:
    """Mapa en acuarela + ruta de lápiz. Coordenadas de puntos en % de la imagen del mapa."""

    def __init__(self, mapa, recorte, destino, origen, final, zona, curva=0.30, seed=1,
                 nota_origen=(500, 812), nota_zona=(560, 196), polaroid_xy=(1395, 318), nota_final=(1405, 622),
                 zoom=0.07):
        img = cv2.imread(mapa)
        self.ih, self.iw = img.shape[:2]
        x0, y0, x1, y1 = recorte
        dx0, dy0, dx1, dy1 = destino
        self.rec, self.dst = recorte, destino
        self.k = (dx1 - dx0) / (x1 - x0)
        dw, dh = dx1 - dx0, dy1 - dy0
        crop = cv2.resize(img[y0:y1, x0:x1], (dw, dh), interpolation=cv2.INTER_CUBIC)
        self.mapa = self._acuarelar_mapa(crop)
        self.campo = campo_mancha(dw // 2, dh // 2, seed, 0.30, 'caja')
        self.campo = cv2.resize(self.campo, (dw, dh), interpolation=cv2.INTER_CUBIC)
        self.zoom = zoom
        self.A = self.a_pantalla(origen['xy'])
        self.B = self.a_pantalla(final['xy'])
        A, B = np.array(self.A), np.array(self.B)
        d = B - A
        nr = np.array([-d[1], d[0]]) / np.linalg.norm(d)
        if nr[0] < 0:
            nr = -nr
        C = (A + B) / 2 + nr * np.linalg.norm(d) * curva
        self.foco = (A + B) / 2
        centro = bezier(A, C, B, 300)
        centro = temblor(centro, 2.0, seed + 4, 0.012)
        # contorno de la ruta = dos trazos de lápiz paralelos + aguada entre ellos
        dd = np.gradient(centro, axis=0)
        nn = np.stack([-dd[:, 1], dd[:, 0]], 1)
        nn /= np.linalg.norm(nn, axis=1, keepdims=True)
        corte = int(len(centro) * 0.93)
        self.centro = centro
        self.bordes = [Trazo(centro[:corte] + nn[:corte] * s * 15, LAPIZ, 5, 255, 2, seed + 10 + i, 0.7)
                       for i, s in enumerate((1, -1))]
        # punta de flecha a mano
        v = centro[-1] - centro[-12]
        v /= np.linalg.norm(v)
        self.puntas = []
        for s in (1, -1):
            a = math.radians(150 * s)
            r = np.array([v[0] * math.cos(a) - v[1] * math.sin(a), v[0] * math.sin(a) + v[1] * math.cos(a)])
            self.puntas.append(Trazo([centro[-1] - v * 6, centro[-1] - v * 6 + r * 40], LAPIZ, 5, 250, 2, seed + 20 + s))
        # trazos auxiliares
        self.circ_A = Trazo(circulo_mano(A[0], A[1], 50, 46, seed=seed), LAPIZ, 4, 250, 2, seed + 30)
        self.mancha_A = Mancha(150, 140, AZUL, seed + 2, 0.35, 0.75, 0.6)
        self.mancha_B = Mancha(190, 170, ROJO, seed + 3, 0.40, 0.42, 0.6)
        self.x_B = self._x_pintada(seed)
        self.gotas = self._gotas(seed)
        # notas, foto y flechas
        self.nota_zona = Nota([{'texto': zona, 'tam': 92}], seed + 40, -2.5, subrayar=(0, zona), color_sub=OCRE)
        self.nota_A = Nota([{'texto': origen['nombre'].upper(), 'tam': 54},
                            {'texto': origen.get('sub', ''), 'tam': 42, 'peso': 500, 'color': PLUMA}], seed + 41, 1.8)
        self.nota_B = Nota([{'texto': final['rotulo'], 'tam': 58}], seed + 42, -1.5,
                           subrayar=(0, final['rotulo'].split('·')[-1].strip()), color_sub=ROJO)
        self.pol = polaroid(final['foto'], 470, None, seed + 43)
        self.pol_sombra = sombra_alfa(self.pol[..., 3], 11, 0.35)
        self.xy_nota_zona, self.xy_nota_A = nota_zona, nota_origen
        self.xy_pol, self.xy_nota_B = polaroid_xy, nota_final
        self.fl_A = flecha_mano((nota_origen[0] + 250, nota_origen[1] - 50), (A[0] - 40, A[1] + 16), -0.25, 22, seed + 50)
        self.fl_B = flecha_mano((polaroid_xy[0] - 250, polaroid_xy[1] + 40), (B[0] + 40, B[1] + 6), 0.25, 22, seed + 51)
        self.tr_fl = [Trazo(p, PLUMA, 4, 250, 2, seed + 60 + i, 0.5) for i, p in
                      enumerate([self.fl_A[0], *self.fl_A[1], self.fl_B[0], *self.fl_B[1]])]
        # tiempos
        self.T = dict(mapa=(0.0, 1.7), zona=0.9, A=2.1, notaA=2.7, ruta=(4.3, 7.2), aguada=(4.8, 7.8),
                      X=7.4, pol=7.8, notaB=8.4)

    def a_pantalla(self, pct):
        x0, y0, _, _ = self.rec
        dx0, dy0, _, _ = self.dst
        px, py = pct[0] / 100 * self.iw, pct[1] / 100 * self.ih
        return (dx0 + (px - x0) * self.k, dy0 + (py - y0) * self.k)

    @staticmethod
    def _acuarelar_mapa(bgr):
        h, w = bgr.shape[:2]
        s = cv2.resize(bgr, (w // 3, h // 3), interpolation=cv2.INTER_AREA)
        for _ in range(4):
            s = cv2.bilateralFilter(s, 9, 38, 9)
        up = cv2.resize(s, (w, h), interpolation=cv2.INTER_CUBIC).astype(np.float32) / 255
        rgb = np.power(up[..., ::-1], 0.8)
        gris = rgb.mean(axis=2, keepdims=True)
        rgb = gris + (rgb - gris) * 0.95
        rgb = 1 - (1 - rgb) * 0.52                                     # aguada clara
        g = cv2.GaussianBlur(cv2.cvtColor(bgr, cv2.COLOR_BGR2GRAY).astype(np.float32), (0, 0), 2.2)
        bl = cv2.GaussianBlur(255 - g, (0, 0), 7)
        sk = np.clip(g * 255 / (256 - bl), 0, 255) / 255
        sk = 0.62 + 0.38 * np.power(sk, 2.5)
        return np.clip(rgb * sk[..., None], 0, 1).astype(np.float32)

    def _x_pintada(self, seed):
        n = 150
        trazos = []
        for k, (a, b) in enumerate((((-40, -44), (42, 40)), ((40, -42), (-38, 44)))):
            m = Image.new('L', (n, n), 0)
            ImageDraw.Draw(m).line([(n / 2 + a[0], n / 2 + a[1]), (n / 2 + b[0], n / 2 + b[1])], fill=255, width=21)
            al = np.asarray(m).astype(np.float32) / 255
            al = cv2.GaussianBlur(al, (0, 0), 2.2)
            al = smooth(0.35, 0.6, al + 0.25 * fbm(n, n, seed + 70 + k, 10, 3))
            filo = np.clip(al - cv2.GaussianBlur(al, (0, 0), 3), 0, 1) * 2
            # dirección del trazo para revelarlo como pincelada
            yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
            v = np.array(b, float) - np.array(a, float)
            v /= np.linalg.norm(v)
            pr = ((xx - n / 2 - a[0]) * v[0] + (yy - n / 2 - a[1]) * v[1]) / np.linalg.norm(np.subtract(b, a))
            trazos.append((np.clip(al * 0.85 + filo * 0.5, 0, 1), pr))
        return trazos

    def _gotas(self, seed):
        rng = np.random.default_rng(seed + 80)
        n = 260
        m = Image.new('L', (n, n), 0)
        d = ImageDraw.Draw(m)
        for _ in range(14):
            ang, r = rng.uniform(0, 6.28), rng.uniform(70, 120)
            s = rng.uniform(2.5, 7)
            x, y = n / 2 + r * math.cos(ang), n / 2 + r * math.sin(ang)
            d.ellipse([x - s, y - s, x + s, y + s], fill=255)
        return np.asarray(m).astype(np.float32) / 255 * 0.7

    def render(self, t):
        T = self.T
        c = PAPEL.copy()
        dx0, dy0, dx1, dy1 = self.dst
        # 1) el mapa se extiende como una mancha de acuarela
        p = e_out(prog(t, *T['mapa']))
        if p > 0:
            a = acuarela_alfa(self.campo, p * 0.91, 1.0, 0.0) * smooth(0, 0.4, p)
            filo = np.exp(-((self.campo - (p * 0.91 * 0.98 - 0.02)) / 0.025) ** 2) * (a > 0)
            reg = c[dy0:dy1, dx0:dx1]
            mapa = self.mapa * reg * (1 - 0.35 * filo[..., None])
            c[dy0:dy1, dx0:dx1] = reg * (1 - a[..., None]) + mapa * a[..., None]
        # 2) marcador de origen: mancha azul + círculo de lápiz
        A, B = self.A, self.B
        self.mancha_A.pintar(c, e_out(prog(t, T['A'], T['A'] + 0.8)), A[0], A[1])
        # 3) aguada de la ruta (sigue al lápiz)
        pa = prog(t, *T['aguada'])
        if pa > 0:
            self._aguada_ruta(c, e_inout(pa))
        # 4) X roja que cae + salpicadura
        tx = t - T['X']
        if tx > 0:
            self.mancha_B.pintar(c, e_out(prog(tx, 0.18, 0.9)), B[0], B[1], 0.75)
            g = self.gotas * smooth(0.15, 0.35, tx)
            pinta(c, g * GRAN[:g.shape[0], :g.shape[1]], ROJO, B[0] - g.shape[0] / 2, B[1] - g.shape[1] / 2)
            esc = 1 + 0.9 * (1 - e_out(prog(tx, 0, 0.3)))
            for k, (al, pr) in enumerate(self.x_B):
                q = prog(tx, 0.0 + 0.12 * k, 0.16 + 0.12 * k)
                if q <= 0:
                    continue
                m = al * smooth(q * 1.1 + 0.02, q * 1.1 - 0.06, pr)
                if esc != 1:
                    m = cv2.resize(m, None, fx=esc, fy=esc, interpolation=cv2.INTER_LINEAR)
                pinta(c, m * 0.95, ROJO * 0.85, B[0] - m.shape[1] / 2, B[1] - m.shape[0] / 2)
        # 5) lápiz: círculo de origen, contorno de la ruta, punta, flechas
        dib = [(self.circ_A, e_inout(prog(t, T['A'] + 0.3, T['A'] + 1.0)))]
        pr_ = prog(t, *T['ruta'])
        for b in self.bordes:
            dib.append((b, e_inout(pr_)))
        for s in self.puntas:
            dib.append((s, prog(t, T['ruta'][1] - 0.05, T['ruta'][1] + 0.25)))
        fA = prog(t, T['notaA'] + 0.9, T['notaA'] + 1.5)
        fB = prog(t, T['pol'] + 0.6, T['pol'] + 1.1)
        fls = [fA, prog(fA, 0.75, 1), prog(fA, 0.75, 1), fB, prog(fB, 0.75, 1), prog(fB, 0.75, 1)]
        for tr, f in zip(self.tr_fl, fls):
            dib.append((tr, min(1.0, f / 0.8) if tr in (self.tr_fl[0], self.tr_fl[3]) else f))
        ct = capa_trazos(W, H, dib)
        if ct is not None:
            over(c, ct, 0, 0)
        # 6) recortes pegados: zona, origen, polaroid, rótulo final
        self.nota_zona.dibujar(c, t - T['zona'], *self.xy_nota_zona)
        self.nota_A.dibujar(c, t - T['notaA'], *self.xy_nota_A)
        tp = t - T['pol']
        if tp > 0:
            a = prog(tp, 0, 0.5)
            e = e_back(a, 1.3)
            capa = con_sombra(self.pol, self.pol_sombra, 8, 12)
            pegar_centro(c, capa, self.xy_pol[0], self.xy_pol[1] - (1 - e_out(a)) * 120, 3 + (1 - e) * 10,
                         0.9 + 0.1 * e, min(1, a * 3))
        self.nota_B.dibujar(c, t - T['notaB'], *self.xy_nota_B)
        # 7) cámara: acercamiento lento hacia la ruta
        z = 1 + self.zoom * e_inout(prog(t, 0, 10.8))
        if z > 1.0005:
            fx, fy = self.foco
            M = np.float32([[z, 0, fx * (1 - z)], [0, z, fy * (1 - z)]])
            c = cv2.warpAffine(c, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
        return c

    def _aguada_ruta(self, c, f):
        pts = parcial(self.centro, f)
        if len(pts) < 2:
            return
        x0, y0 = pts.min(axis=0) - 30
        x1, y1 = pts.max(axis=0) + 30
        x0, y0 = int(max(0, x0)), int(max(0, y0))
        w, h = int(x1 - x0), int(y1 - y0)
        m = Image.new('L', (w, h), 0)
        ImageDraw.Draw(m).line([(x - x0, y - y0) for x, y in pts], fill=255, width=20, joint='curve')
        al = cv2.GaussianBlur(np.asarray(m).astype(np.float32) / 255, (0, 0), 2.5)
        al = smooth(0.3, 0.55, al + 0.3 * fbm(h, w, 77, 8, 3))
        filo = np.clip(al - cv2.GaussianBlur(al, (0, 0), 3), 0, 1) * 1.8
        pinta(c, np.clip(al * 0.62 + filo * 0.5, 0, 1) * GRAN[y0:y0 + h, x0:x0 + w], SIENA, x0, y0)


def mapa_ruta(**kw):
    return MapaRuta(**kw)


class Ficha:
    """Hoja de cuaderno con clip: título, íconos recortados que se pegan uno a uno con su etiqueta y un contador."""

    def __init__(self, titulo, iconos, etiqueta='×15', total=60, tam=(1200, 690), seed=7, salida=8.7):
        w, h = tam
        self.w, self.h, self.pad = w, h, 90
        hoja = hoja_cuaderno(w, h, seed)
        self.base = np.zeros((h + self.pad, w, 4), np.float32)
        over_capa(self.base, hoja, 0, self.pad)
        self.sombra = sombra_alfa(self.base[..., 3], 14, 0.38)
        clip = clip_metal()
        over_capa(self.base, transformar(clip, 4), 150, self.pad - 76)
        tt = tam_que_cabe(titulo, 80, w - 200)
        self.titulo = Texto(titulo, tt, seed=seed)
        self.tit_xy = (124, self.pad + 26)
        uy = self.pad + 26 + self.titulo.h - 18
        self.subr = Trazo(temblor([(130, uy), (130 + self.titulo.w - 30, uy + 4)], 2.5, seed, 0.05), LAPIZ, 4, 200, 2, seed)
        n = len(iconos)
        sep = (w - 200) / n
        self.slots = [100 + sep * (i + 0.5) for i in range(n)]
        self.y_ico = self.pad + 270
        rng = np.random.default_rng(seed)
        self.ico = []
        for i, r in enumerate(iconos):
            rc = recorte_foto(r, 168, 9)
            m = 26
            capa = np.zeros((rc.shape[0] + 2 * m, rc.shape[1] + 2 * m, 4), np.float32)
            sh = sombra_alfa(np.pad(rc[..., 3], m), 5, 0.35)
            capa[..., 3] = np.roll(np.roll(sh, 4, 0), 3, 1)
            over_capa(capa, rc, m, m)
            ct = transformar(cinta(110, 34, seed + i), rng.uniform(-25, 25))
            over_capa(capa, ct, capa.shape[1] / 2 - ct.shape[1] / 2 + rng.uniform(-20, 20), m - ct.shape[0] / 2 + 6)
            self.ico.append((capa, rng.uniform(-6, 6)))
        self.mas = Texto('+', 70, color=LAPIZ, seed=seed + 5)
        self.etq = [Texto(etiqueta, 66, color=PLUMA, seed=seed + 10 + i) for i in range(n)]
        self.total, self.salida = total, salida
        self.circ = Trazo(circulo_mano(w / 2 + 40, self.pad + 578, 150, 68, 1.15, -160, seed + 2), (178, 40, 36), 6, 225, 2, seed + 3)
        self.linea = Trazo(temblor([(w / 2 - 300, self.pad + 492), (w / 2 + 300, self.pad + 494)], 1.5, seed + 9), LAPIZ, 3, 190, 2, seed + 9)
        self.T = dict(entra=(0, 0.8), titulo=(0.75, 1.9), subr=(1.8, 2.3), ico0=2.3, paso=0.9, cuenta=(5.9, 7.1), circ=(7.1, 7.7))

    @functools.lru_cache(None)
    def _num(self, n):
        return Texto(f'= {n}', 132, color=TINTA, seed=n % 7)

    def capa(self, t):
        T = self.T
        c = self.base.copy()
        p = prog(t, *T['titulo'])
        if p > 0:
            over_capa(c, self.titulo.escrito(p), *self.tit_xy)
        dib = [(self.subr, e_inout(prog(t, *T['subr'])))]
        for i, (cx, (ic, ang)) in enumerate(zip(self.slots, self.ico)):
            ti = t - (T['ico0'] + i * T['paso'])
            if ti <= 0:
                continue
            a = prog(ti, 0, 0.42)
            e = e_back(a, 2.0)
            cap = transformar(ic, ang + (1 - e) * 14, 1.35 - 0.35 * e)
            over_capa(c, cap, cx - cap.shape[1] / 2, self.y_ico - cap.shape[0] / 2, min(1, a * 3))
            pe = prog(ti, 0.35, 0.8)
            if pe > 0:
                et = self.etq[i]
                over_capa(c, et.escrito(pe), cx - et.w / 2, self.y_ico + 100)
            if i > 0:
                pm = prog(ti, 0.0, 0.25)
                if pm > 0:
                    mx = (cx + self.slots[i - 1]) / 2
                    over_capa(c, self.mas.escrito(pm), mx - self.mas.w / 2, self.y_ico - self.mas.h / 2 - 6)
        tl = t - (T['ico0'] + len(self.ico) * T['paso'])
        dib.append((self.linea, e_inout(prog(tl, 0.0, 0.5))))
        pc = prog(t, *T['cuenta'])
        if pc > 0:
            n = int(round(self.total * e_inout(pc)))
            nt = self._num(n)
            k = prog(pc, 0, 0.12)
            over_capa(c, nt.escrito(1.0), self.w / 2 + 40 - nt.w / 2, self.pad + 578 - nt.h / 2 - 8, k)
        dib.append((self.circ, e_inout(prog(t, *T['circ']))))
        ct = capa_trazos(self.w, self.h + self.pad, dib)
        if ct is not None:
            over_capa(c, ct, 0, 0)
        return con_sombra(c, self.sombra, 10, 16)

    def dibujar(self, dst, t, cx, cy):
        if t <= 0:
            return
        a = prog(t, *self.T['entra'])
        e = e_back(a, 1.2)
        dy = (1 - e_out(a)) * 760
        ang = -1.5 - (1 - e) * 10
        op = 1.0
        if t > self.salida:
            q = e_in(prog(t, self.salida, self.salida + 0.65))
            dy += q * 1000
            ang += q * 9
        if dy > 1300:
            return
        pegar_centro(dst, self.capa(t), cx, cy + dy, ang, 1.0, op)


def ficha(**kw):
    return Ficha(**kw)


class Tarjeta:
    """Tarjeta de jefe: polaroid de la foto + hoja con clip (título, nombre resaltado, subtítulo, cuartos en acuarela)."""

    def __init__(self, foto, linea1, nombre, sub, pie=None, tam=(860, 450), seed=9, salida=7.7,
                 colores=(ROJO, AMARILLO, AZUL, VERDE)):
        self.pol = polaroid(foto, 600, pie, seed)
        self.pol_sombra = sombra_alfa(self.pol[..., 3], 12, 0.38)
        w, h = tam
        self.w, self.h, self.pad = w, h, 70
        hoja = hoja_cuaderno(w, h, seed + 1, renglon=48, margen=70)
        self.base = np.zeros((h + self.pad, w, 4), np.float32)
        over_capa(self.base, hoja, 0, self.pad)
        self.sombra = sombra_alfa(self.base[..., 3], 13, 0.36)
        over_capa(self.base, transformar(clip_metal(), -6), w // 2 + 40, self.pad - 74)
        self.l1 = Texto(linea1, 64, seed=seed)
        self.nom = Texto(nombre, 118, seed=seed + 1)
        self.sub = Texto(sub, tam_que_cabe(sub, 56, w - 140, 600), peso=600, color=PLUMA, seed=seed + 2)
        self.xy1 = (96, self.pad + 28)
        self.xyn = (92, self.pad + 86)
        self.xys = (96, self.pad + 300)
        self.res = Pincelada(int(self.nom.w + 10), int(self.nom.h * 0.45), ROJO, seed + 4, 0.42, 0.5)
        self.xyres = (self.xyn[0] - 4, self.xyn[1] + self.nom.h * 0.50)
        self.pc = (w - 150, self.pad + 175)
        r = 92
        self.r = r
        self.circ = Trazo(circulo_mano(self.pc[0], self.pc[1], r, r, 1.06, -95, seed), LAPIZ, 3, 220, 2, seed + 5)
        self.cruz = [Trazo(temblor([(self.pc[0], self.pc[1] - r), (self.pc[0], self.pc[1] + r)], 1, seed + 6), LAPIZ, 2, 190, 1, seed + 6),
                     Trazo(temblor([(self.pc[0] - r, self.pc[1]), (self.pc[0] + r, self.pc[1])], 1, seed + 7), LAPIZ, 2, 190, 1, seed + 7)]
        # cuartos: máscaras de acuarela por cuadrante
        s = 2 * r + 20
        yy, xx = np.mgrid[0:s, 0:s].astype(np.float32) - s / 2
        ang = (np.degrees(np.arctan2(yy, xx)) + 90) % 360
        rad = np.sqrt(xx ** 2 + yy ** 2) / r + 0.10 * fbm(s, s, seed + 8, 6, 3)
        self.cuartos = []
        for q in range(4):
            dentro = ((ang >= q * 90) & (ang < (q + 1) * 90)).astype(np.float32)
            dentro = cv2.GaussianBlur(dentro, (0, 0), 1.5)
            self.cuartos.append((dentro, rad, colores[q]))
        self.salida = salida
        self.T = dict(pol=(0.1, 0.7), hoja=(0.6, 1.3), l1=(1.3, 1.9), nom=(1.9, 2.6), res=(2.6, 3.1),
                      sub=(3.1, 4.2), circ=(3.6, 4.2), cuarto0=4.2, paso=0.35)

    def capa_hoja(self, t):
        T = self.T
        c = self.base.copy()
        p = prog(t, *T['res'])
        if p > 0:
            pinta(c, self.res.alfa(p), self.res.color, *self.xyres)
        for tx, xy, key in ((self.l1, self.xy1, 'l1'), (self.nom, self.xyn, 'nom'), (self.sub, self.xys, 'sub')):
            p = prog(t, *T[key])
            if p > 0:
                over_capa(c, tx.escrito(p), *xy)
        for q, (dentro, rad, col) in enumerate(self.cuartos):
            pq = e_out(prog(t, T['cuarto0'] + q * T['paso'], T['cuarto0'] + q * T['paso'] + 0.5))
            if pq <= 0:
                continue
            a = acuarela_alfa(rad, pq * 0.97, 0.5, 0.5) * dentro
            s = dentro.shape[0]
            pinta(c, a, col, self.pc[0] - s / 2, self.pc[1] - s / 2)
        dib = [(self.circ, e_inout(prog(t, *T['circ'])))]
        for i, cz in enumerate(self.cruz):
            dib.append((cz, prog(t, T['circ'][1] - 0.1 + 0.15 * i, T['circ'][1] + 0.2 + 0.15 * i)))
        ct = capa_trazos(self.w, self.h + self.pad, dib)
        if ct is not None:
            over_capa(c, ct, 0, 0)
        return con_sombra(c, self.sombra, 10, 15)

    def dibujar(self, dst, t, pol_xy=(520, 430), hoja_xy=(1265, 420)):
        if t <= 0:
            return
        T = self.T
        q = e_in(prog(t, self.salida, self.salida + 0.7)) if t > self.salida else 0.0
        a = prog(t, *T['pol'])
        if a > 0:
            e = e_back(a, 1.4)
            capa = con_sombra(self.pol, self.pol_sombra, 9, 14)
            pegar_centro(dst, capa, pol_xy[0] - q * 1100, pol_xy[1] - (1 - e_out(a)) * 140 + q * 120,
                         -4 + (1 - e) * 12 + q * 14, 0.9 + 0.1 * e, min(1, a * 3))
        a = prog(t, *T['hoja'])
        if a > 0:
            e = e_back(a, 1.2)
            pegar_centro(dst, self.capa_hoja(t), hoja_xy[0] + (1 - e_out(a)) * 900 + q * 1100,
                         hoja_xy[1] + q * 160, 2 + (1 - e) * 8 - q * 10, 1.0, min(1, a * 4))


def tarjeta(**kw):
    return Tarjeta(**kw)


class Rotulo:
    """Lower third: tira de papel rasgado con cinta, aguada detrás del texto y sello de tinta roja."""

    def __init__(self, texto, sello='5', sello_sub='JEFES', seed=13, salida=3.2, color=OCRE):
        self.txt = Texto(texto, 76, seed=seed)
        self.ws = 190                                   # hueco del sello en la punta de la tira
        w, h = int(self.txt.w + 90 + self.ws), 170
        self.w, self.h = w, h
        self.m = 24
        self.base = np.zeros((h + 2 * self.m, w + 2 * self.m, 4), np.float32)
        over_capa(self.base, recorte_papel(w, h, seed, amp=6), self.m, self.m)
        self.sombra = sombra_alfa(self.base[..., 3], 9, 0.34)
        self.ct = transformar(cinta(120, 40, seed + 2), 80)
        self.agua = Pincelada(w - 40 - self.ws, int(h * 0.55), color, seed + 3, 0.5, 0.45)
        self.campo_tira = (np.arange(w + 2 * self.m, dtype=np.float32) / (w + 2 * self.m))
        # sello
        n = 230
        m = Image.new('L', (n, n), 0)
        d = ImageDraw.Draw(m)
        d.ellipse([18, 18, n - 18, n - 18], outline=255, width=12)
        d.ellipse([36, 36, n - 36, n - 36], outline=255, width=4)
        f = fuente(118, 700)
        d.text((n / 2, n / 2 - 14), sello, font=f, fill=255, anchor='mm')
        f2 = fuente(36, 700)
        d.text((n / 2, n / 2 + 54), sello_sub, font=f2, fill=255, anchor='mm')
        al = np.asarray(m).astype(np.float32) / 255
        al = cv2.GaussianBlur(al, (0, 0), 0.8)
        ruido = fbm(n, n, seed + 5, 18, 3)
        self.sello = np.clip(al * (0.78 + 0.6 * ruido) * smooth(-0.25, 0.1, ruido), 0, 1)
        self.salida = salida

    def dibujar(self, dst, t, x=110, cy=930):
        if t <= 0:
            return
        q = e_in(prog(t, self.salida, self.salida + 0.55)) if t > self.salida else 0.0
        c = self.base.copy()
        p = prog(t, 0.0, 0.45)
        rev = smooth(p * 1.1 + 0.02, p * 1.1 - 0.05, self.campo_tira)       # la tira se desenrolla
        pa = prog(t, 0.3, 0.9)
        if pa > 0:
            pinta(c, self.agua.alfa(pa), self.agua.color, self.m + 20, self.m + self.h * 0.32)
        pt = prog(t, 0.55, 1.55)
        if pt > 0:
            over_capa(c, self.txt.escrito(pt), self.m + 45, self.m + (self.h - self.txt.h) / 2 + 2)
        # sello de tinta impreso en la punta de la tira: cae, se aplasta y deja la marca
        ts = t - 1.65
        if ts > 0:
            a = prog(ts, 0, 0.32)
            esc = 0.68 * (1.7 - 0.8 * e_out(prog(ts, 0, 0.22)) + 0.1 * e_out(prog(ts, 0.22, 0.32)))
            al = transformar(np.dstack([self.sello] * 4), -14, esc)[..., 0]
            k = min(1, a * 2.2)
            sx, sy = self.m + self.w - self.ws / 2 - 10, self.m + self.h / 2
            pinta(c, al * 0.95 * k, ROJO * 0.92, sx - al.shape[1] / 2, sy - al.shape[0] / 2)
        over_capa(c, self.ct, self.m - self.ct.shape[1] / 2 + 6, self.m + self.h / 2 - self.ct.shape[0] / 2)
        c = con_sombra(c, self.sombra, 6, 9)
        c *= np.pad(rev, (36, 36), mode='edge')[None, :, None]
        pegar_centro(dst, c, x + c.shape[1] / 2 - 60 - q * 1800, cy, -1.0, 1.0, 1.0)


def rotulo(**kw):
    return Rotulo(**kw)


def etiqueta_esquina(texto='ESTILO 5 · CUADERNO DE EXPLORADOR'):
    t = Texto(texto, 34, seed=3)
    w, h = t.w + 40, t.h + 6
    c = np.zeros((h + 20, w + 20, 4), np.float32)
    ct = cinta(w, h, 77)
    over_capa(c, ct, 10, 10)
    over_capa(c, t.capa, 30, 13)
    return transformar(c, 1.2)


# ───────────────────────────── el video ─────────────────────────────
class Video:
    def __init__(self):
        P = lambda *a: os.path.join(SRC, *a)
        self.mapa = MapaRuta(
            mapa=P('mapas', 'ungoro_norte.jpg'), recorte=(330, 0, 1130, 450), destino=(200, 110, 1720, 965),
            origen={'xy': (43.6, 23.0), 'nombre': 'Refugio de los Mariscales', 'sub': '+ Gryfe (vuelo) al lado'},
            final={'xy': (47.3, 10.8), 'rotulo': 'BANCAL DEL CREADOR · 58-60', 'foto': P('pegatinas', 'bancal_creador.png')},
            zona="CRÁTER DE UN'GORO")
        self.ficha = Ficha(titulo='N.º 15 · SIN LOS 60 CRISTALES',
                           iconos=[P('pegatinas', f'o_cristal_{c}.png') for c in ('rojo', 'amarillo', 'azul', 'verde')])
        self.tarjeta = Tarjeta(foto=P('pegatinas', 'bancal_creador.png'), linea1='JEFA FINAL:', nombre='NANAYA',
                               sub='cambia de elemento cada 25 %', pie='bancal del creador')
        self.rotulo = Rotulo('Sin cristales: solo 5 jefes', '5', 'JEFES')
        self.c89 = Clip(P('medios', 'scene-089.mp4'))
        self.c91 = Clip(P('medios', 'scene-091.mp4'), 0.5)
        self.c93 = Clip(P('medios', 'scene-093.mp4'), 0.3)
        self.esq = etiqueta_esquina()

    def esc1(self, t):
        return self.mapa.render(t)

    def esc2(self, t):
        if t < 16.2:
            fondo = acuarelar(self.c89.cuadro(t - 10.6))
        elif t < 16.9:
            fondo = transicion_aguada(acuarelar(self.c89.cuadro(t - 10.6)), acuarelar(self.c91.cuadro(t - 16.2)),
                                      prog(t, 16.2, 16.9), 8, VERDE)
        else:
            fondo = acuarelar(self.c91.cuadro(t - 16.2))
        self.ficha.dibujar(fondo, t - 11.25, 960, 560)
        return fondo

    def esc3(self, t):
        fondo = acuarelar(self.c93.cuadro(t - 20.6))
        self.tarjeta.dibujar(fondo, t - 21.3)
        self.rotulo.dibujar(fondo, t - 25.8)
        return fondo

    def cuadro(self, t):
        if t < 10.4:
            c = self.esc1(t)
        elif t < 11.2:
            c = transicion_aguada(self.esc1(t), self.esc2(t), prog(t, 10.4, 11.2), 5, SIENA)
        elif t < 20.5:
            c = self.esc2(t)
        elif t < 21.3:
            c = transicion_aguada(self.esc2(t), self.esc3(t), prog(t, 20.5, 21.3), 6, AZUL)
        elif t < 29.3:
            c = self.esc3(t)
        else:
            c = transicion_aguada(self.esc3(t), PAPEL.copy(), prog(t, 29.3, 29.95), 7, OCRE)
        op = min(1, t / 0.6) * (1 - prog(t, 29.4, 29.95))
        over(c, self.esq, 18, 14, 0.92 * op)
        return c


def a_uint8(c):
    return (np.clip(c, 0, 1) * 255 + 0.5).astype(np.uint8)


def render():
    v = Video()
    n = int(DUR * FPS)
    audio = os.path.join(SRC, 'audio', 'wow', 'nlXOcybLHxc.wav')
    cmd = [FFMPEG, '-y', '-loglevel', 'error', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', f'{W}x{H}', '-r', str(FPS),
           '-i', '-', '-ss', '2', '-t', f'{DUR}', '-i', audio,
           '-filter:a', f'volume=-18dB,afade=t=in:st=0:d=1.5,afade=t=out:st={DUR - 2.5}:d=2.5',
           '-map', '0:v', '-map', '1:a', '-c:v', 'libx264', '-preset', 'medium', '-crf', '20', '-pix_fmt', 'yuv420p',
           '-threads', '4', '-c:a', 'aac', '-b:a', '192k', '-t', f'{DUR}', '-movflags', '+faststart', SALIDA]
    pr = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    import time
    t0 = time.time()
    for i in range(n):
        t = i / FPS
        pr.stdin.write(a_uint8(v.cuadro(t)).tobytes())
        if i % 60 == 0:
            print(f'{t:5.1f} s  ({time.time() - t0:.0f} s)', flush=True)
    pr.stdin.close()
    pr.wait()
    print('listo:', SALIDA)


def hoja():
    cap = cv2.VideoCapture(SALIDA)
    tiles = []
    for k in range(12):
        t = 1.25 + 2.5 * k
        cap.set(cv2.CAP_PROP_POS_MSEC, t * 1000)
        ok, f = cap.read()
        f = cv2.resize(f, (640, 360), interpolation=cv2.INTER_AREA)
        cv2.rectangle(f, (548, 330), (640, 360), (0, 0, 0), -1)
        cv2.putText(f, f'{t:.2f}s', (554, 352), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
        tiles.append(f)
    filas = [np.hstack(tiles[r * 4:(r + 1) * 4]) for r in range(3)]
    cv2.imwrite(HOJA, np.vstack(filas), [cv2.IMWRITE_JPEG_QUALITY, 90])
    print('hoja:', HOJA)


if __name__ == '__main__':
    if '--cuadro' in sys.argv:
        i = sys.argv.index('--cuadro')
        t = float(sys.argv[i + 1])
        out = sys.argv[i + 2]
        v = Video()
        Image.fromarray(a_uint8(v.cuadro(t))).save(out)
        print(out)
    elif '--hoja' in sys.argv:
        hoja()
    else:
        render()
        hoja()
