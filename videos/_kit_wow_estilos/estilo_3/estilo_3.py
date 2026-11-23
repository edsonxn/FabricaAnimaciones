# -*- coding: utf-8 -*-
"""
ESTILO 3 · HOLOGRAMA ARCANO — propuesta de kit visual para Crónicas de Warcraft (22-nov-2026).

Uso:
  python estilo_3.py                    -> estilo_3_holograma.mp4 (30 s) + hoja.jpg
  python estilo_3.py --cuadros 3,8.5    -> _prev_03.00.jpg ... (sin video, para revisar cuadros sueltos)
  python estilo_3.py --hoja             -> solo rehace hoja.jpg a partir del mp4

Piezas reutilizables (cada una es un objeto con .dibujar(ctx, t_local)):
  mapa_ruta(mapa, puntos, zona, ...)  mapa proyectado azul-violeta, rejilla, círculo rúnico, marcadores = anillos que
                                       pulsan, ruta = haz de energía con partículas, foto del destino en ficha de cristal
  ficha(titulo, iconos, ...)          ficha de cristal translúcido con borde de neón, íconos en hexágonos y contador
  tarjeta(foto, titulo, sub, ...)     tarjeta de jefe con proyección holográfica de la foto y barra de vida por fases
  rotulo(texto, sello, ...)           rótulo inferior con sello rúnico que se estampa
Todo se dibuja en capas: 0 fondo · 1 mapa · 2 vidrio · 3 fotos · neón (luz + bloom) · 5 textos; luego posproceso
(líneas de escaneo, viñeta, glitch de transición) y la marca de la esquina.
"""
import math
import os
import random
import subprocess
import sys

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

cv2.setNumThreads(4)
AQUI = os.path.dirname(os.path.abspath(__file__))
SRC = r"C:\FabricaAnimaciones\videos\wow_errores_60"
FF = r"C:\ffmpeg\bin\ffmpeg.exe"
SALIDA = os.path.join(AQUI, "estilo_3_holograma.mp4")
W, H, FPS, DUR = 1920, 1080, 30, 30.0
NF = int(round(DUR * FPS))

# ---------------------------------------------------------------- paleta
CIAN = (90, 225, 255)
VIOLETA = (160, 110, 255)
MAGENTA = (255, 90, 210)
BLANCO = (236, 250, 255)
NOCHE = (5, 7, 24)
VIDRIO = (10, 20, 54)


def c(rgb):
    return np.array(rgb, np.float32) / 255.0


def cl(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def eo(u):
    u = cl(u)
    return 1 - (1 - u) ** 3


def eio(u):
    u = cl(u)
    return u * u * u * (u * (6 * u - 15) + 10)


def eback(u, s=1.8):
    u = cl(u) - 1
    return 1 + u * u * ((s + 1) * u + s)


def seg(t, a, b):
    return cl((t - a) / (b - a)) if b > a else float(t >= a)


def lerp(a, b, u):
    return a + (b - a) * u


def ruido(t, f=7.0, s=0):
    """Parpadeo suave determinista en [-1, 1]."""
    return math.sin(t * f * 6.283 + s) * 0.6 + math.sin(t * f * 2.71 * 6.283 + s * 1.7) * 0.4


def lut(stops):
    xs = np.linspace(0, 1, 256)
    out = np.zeros((256, 3), np.float32)
    for ch in range(3):
        out[:, ch] = np.interp(xs, [s[0] for s in stops], [s[1][ch] / 255 for s in stops])
    return out


LUT_MAPA = lut([(0, (3, 5, 20)), (.30, (28, 22, 92)), (.55, (62, 76, 198)), (.78, (92, 188, 255)), (1, (225, 248, 255))])
LUT_GP = lut([(0, (2, 3, 12)), (.40, (30, 24, 88)), (.70, (60, 118, 220)), (1, (175, 236, 255))])

# ---------------------------------------------------------------- texto
_F = {}


def fuente(tam, var="Bold", mono=False):
    k = (tam, var, mono)
    if k not in _F:
        if mono:
            f = ImageFont.truetype("C:/Windows/Fonts/consolab.ttf", tam)
        else:
            f = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", tam)
            f.set_variation_by_name(var)
        _F[k] = f
    return _F[k]


class Spr:
    """Sprite premultiplicado: rgb (h,w,3) ya multiplicado por alfa (puede pasarse de alfa = luz aditiva)."""

    def __init__(s, rgb, a, ox=0, oy=0, w=None, h=None):
        s.rgb, s.a, s.ox, s.oy = rgb, a, ox, oy
        s.w = a.shape[1] if w is None else w
        s.h = a.shape[0] if h is None else h


_T = {}


def texto(s, tam, color=BLANCO, var="Bold", glow=CIAN, gk=0.9, mono=False, track=0, gr=None):
    key = (s, tam, color, var, glow, gk, mono, track, gr)
    if key in _T:
        return _T[key]
    f = fuente(tam, var, mono)
    gr = gr if gr is not None else max(3, tam // 7)
    pad = int(gr * 3) + 2
    asc, desc = f.getmetrics()
    if track:
        ws = [f.getlength(ch) for ch in s]
        wt = int(sum(ws) + track * max(0, len(s) - 1)) + 2
    else:
        wt = int(f.getlength(s)) + 2
    ht = asc + desc
    im = Image.new("L", (wt + 2 * pad, ht + 2 * pad), 0)
    d = ImageDraw.Draw(im)
    if track:
        x = pad
        for ch, wc in zip(s, ws):
            d.text((x, pad), ch, font=f, fill=255)
            x += wc + track
    else:
        d.text((pad, pad), s, font=f, fill=255)
    m = np.asarray(im, np.float32) / 255.0
    rgb = m[..., None] * c(color)
    a = m.copy()
    if glow:
        g = cv2.GaussianBlur(m, (0, 0), gr)
        rgb = rgb + g[..., None] * c(glow) * gk * (1 - m[..., None])
        a = np.clip(m + g * 0.30, 0, 1)
    sp = Spr(rgb.astype(np.float32), a.astype(np.float32), pad, pad, wt, ht)
    if len(_T) > 900:
        _T.clear()
    _T[key] = sp
    return sp


GLIFOS = "#$%&*+=<>/\\|0123456789ABCDEFGHJKLMNPQRSTUVWXYZ"


def decodificar(s, u, seed=0):
    """Texto que se 'descifra': lo revelado, 4 glifos al azar delante y el resto vacío."""
    if u >= 1:
        return s
    n = len(s)
    k = u * (n + 4)
    rng = random.Random(seed)
    out = []
    for i, ch in enumerate(s):
        if ch == " ":
            out.append(" ")
        elif i < k - 4:
            out.append(ch)
        elif i < k:
            out.append(rng.choice(GLIFOS))
        else:
            out.append(" ")
    return "".join(out)


# ---------------------------------------------------------------- composición
def pegar(F, sp, x, y, op=1.0):
    if sp is None or op <= 0.003:
        return
    x = int(round(x - sp.ox))
    y = int(round(y - sp.oy))
    h, w = sp.a.shape
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x0 >= x1 or y0 >= y1:
        return
    a = sp.a[y0 - y:y1 - y, x0 - x:x1 - x] * op
    r = sp.rgb[y0 - y:y1 - y, x0 - x:x1 - x] * op
    d = F[y0:y1, x0:x1]
    d *= (1 - a)[..., None]
    d += r


def sumar(luz, m, x, y, color, alpha):
    if alpha <= 0.003:
        return
    x = int(round(x))
    y = int(round(y))
    h, w = m.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x0 >= x1 or y0 >= y1:
        return
    sub = m[y0 - y:y1 - y, x0 - x:x1 - x]
    if sub.ndim == 2:
        luz[y0:y1, x0:x1] += sub[..., None] * (c(color) * alpha)
    else:
        luz[y0:y1, x0:x1] += sub * alpha


def de_pil(im):
    a = np.asarray(im.convert("RGBA"), np.float32) / 255.0
    return Spr((a[..., :3] * a[..., 3:4]).astype(np.float32), a[..., 3].copy())


def glitch_spr(sp, k, seed):
    """Glitch suave de entrada: franjas desplazadas + separación RGB."""
    if sp is None or k <= 0.02:
        return sp
    rng = np.random.default_rng(seed)
    rgb = sp.rgb.copy()
    a = sp.a.copy()
    h = a.shape[0]
    for _ in range(int(2 + 7 * k)):
        y0 = int(rng.integers(0, h))
        hh = int(rng.integers(3, max(5, h // 6)))
        dx = int(rng.normal(0, 1) * 34 * k)
        rgb[y0:y0 + hh] = np.roll(rgb[y0:y0 + hh], dx, axis=1)
        a[y0:y0 + hh] = np.roll(a[y0:y0 + hh], dx, axis=1)
    sh = int(round(9 * k))
    if sh:
        rgb[..., 0] = np.roll(rgb[..., 0], -sh, axis=1)
        rgb[..., 2] = np.roll(rgb[..., 2], sh, axis=1)
    return Spr(rgb, a, sp.ox, sp.oy, sp.w, sp.h)


def linea(ctx, pts, color, grosor=2, alpha=1.0, cerrado=False):
    if alpha <= 0.003 or len(pts) < 2:
        return
    p = np.round(np.asarray(pts, np.float64) * 16).astype(np.int32).reshape(-1, 1, 2)
    col = tuple(float(v * cl(alpha)) for v in color)
    cv2.polylines(ctx.Lu, [p], cerrado, col, int(grosor), cv2.LINE_AA, shift=4)


def circulo(ctx, x, y, r, color, grosor=2, alpha=1.0, relleno=False):
    if alpha <= 0.003 or r <= 0.3:
        return
    col = tuple(float(v * cl(alpha)) for v in color)
    cv2.circle(ctx.Lu, (int(round(x * 16)), int(round(y * 16))), int(round(r * 16)), col,
               -1 if relleno else int(grosor), cv2.LINE_AA, shift=4)


def parcial(pts, p):
    pts = np.asarray(pts, np.float64)
    if p >= 1:
        return pts
    if p <= 0:
        return pts[:1]
    d = np.r_[0, np.cumsum(np.linalg.norm(np.diff(pts, axis=0), axis=1))]
    L = d[-1] * p
    k = int(np.searchsorted(d, L))
    k = max(1, min(k, len(pts) - 1))
    a = (L - d[k - 1]) / max(d[k] - d[k - 1], 1e-6)
    q = pts[k - 1] + (pts[k] - pts[k - 1]) * a
    return np.vstack([pts[:k], q])


def tramo(pts, p0, p1):
    """Sub-curva entre las fracciones p0..p1 de su longitud."""
    a = parcial(pts, p1)
    if p0 <= 0:
        return a
    b = parcial(pts, p0)
    return np.vstack([b[-1:], a[len(b) - 1:]])


_M = {}


def mascara_chaflan(w, h, ch, pluma=0):
    key = (w, h, ch, pluma)
    if key in _M:
        return _M[key]
    ch = int(min(ch, h / 2, w / 2))
    im = Image.new("L", (w * 2, h * 2), 0)
    ImageDraw.Draw(im).polygon([(ch * 2, 0), (w * 2, 0), (w * 2, (h - ch) * 2), ((w - ch) * 2, h * 2), (0, h * 2),
                                (0, ch * 2)], fill=255)
    m = np.asarray(im.resize((w, h), Image.LANCZOS), np.float32) / 255.0
    if pluma:
        m = cv2.GaussianBlur(m, (0, 0), pluma) * np.clip(m * 1.0, 0, 1)
    if len(_M) > 80:
        _M.clear()
    _M[key] = m
    return m


def contorno(x, y, w, h, ch):
    ch = min(ch, h / 2, w / 2)
    return [(x + ch, y), (x + w, y), (x + w, y + h - ch), (x + w - ch, y + h), (x, y + h), (x, y + ch), (x + ch, y)]


def vidrio(F, x, y, w, h, ch, op, tinte=VIDRIO):
    """Cristal translúcido: desenfoca lo de atrás, lo tiñe de azul noche y le pone un brillo vertical."""
    x, y, w, h = int(round(x)), int(round(y)), int(round(w)), int(round(h))
    if w < 2 or h < 2 or op <= 0.003:
        return
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, W), min(y + h, H)
    if x0 >= x1 or y0 >= y1:
        return
    roi = F[y0:y1, x0:x1]
    sm = cv2.resize(roi, (max(1, (x1 - x0) // 6), max(1, (y1 - y0) // 6)), interpolation=cv2.INTER_AREA)
    sm = cv2.GaussianBlur(sm, (0, 0), 1.6)
    bl = cv2.resize(sm, (x1 - x0, y1 - y0), interpolation=cv2.INTER_LINEAR)
    m = mascara_chaflan(w, h, ch)[y0 - y:y1 - y, x0 - x:x1 - x] * op
    gy = np.linspace(1, 0, h, dtype=np.float32)[y0 - y:y1 - y]
    val = bl * 0.30 + c(tinte)[None, None, :] * 0.80 + (gy[:, None, None] ** 2 * 0.07) * c(CIAN)
    roi *= (1 - m)[..., None]
    roi += val * m[..., None]


_RC = {}


def circulo_runico(R, seed=1, estilo=0):
    """Círculo rúnico original: anillos, banda de glifos inventados (trazos en retícula 3x3), marcas, estrella interior."""
    key = (R, seed, estilo)
    if key in _RC:
        return _RC[key]
    ss = 2
    S = int(2 * R + 8) * ss
    C = S / 2
    Rs = R * ss
    im = Image.new("L", (S, S), 0)
    d = ImageDraw.Draw(im)
    lw = max(1, int(round(ss * R / 120)))

    def ring(r, w, fill=255):
        d.ellipse([C - r, C - r, C + r, C + r], outline=fill, width=w)

    ring(Rs, lw * 2)
    ring(Rs * 0.95, lw)
    rng = random.Random(seed)
    n = max(12, int(R / 4.5))
    rg = Rs * 0.875
    gs = Rs * 0.060
    vec = ((1, 0), (0, 1), (1, 1), (1, -1), (0, 2), (2, 0))
    for i in range(n):
        ang = 2 * math.pi * i / n
        ca, sa = math.cos(ang), math.sin(ang)
        cx, cy = C + rg * ca, C + rg * sa
        for _ in range(rng.randint(2, 4)):
            p = (rng.randint(0, 2), rng.randint(0, 2))
            ops = [(p[0] + dx, p[1] + dy) for dx, dy in vec if 0 <= p[0] + dx <= 2 and 0 <= p[1] + dy <= 2]
            if not ops:
                continue
            q = rng.choice(ops)
            pts = []
            for (u, v) in (p, q):
                lx = (u - 1) * gs * 0.55
                ly = (v - 1) * gs * 0.62
                pts.append((cx + lx * (-sa) + ly * ca, cy + lx * ca + ly * sa))
            d.line(pts, fill=255, width=lw)
    ring(Rs * 0.80, lw)
    for i in range(72):
        ang = 2 * math.pi * i / 72
        l1 = Rs * (0.70 if i % 6 == 0 else 0.745)
        d.line([(C + l1 * math.cos(ang), C + l1 * math.sin(ang)),
                (C + Rs * 0.78 * math.cos(ang), C + Rs * 0.78 * math.sin(ang))], fill=210, width=lw)
    rr = Rs * 0.645
    for i in range(48):
        ang = 2 * math.pi * i / 48
        x, y = C + rr * math.cos(ang), C + rr * math.sin(ang)
        r = lw * 1.3
        d.ellipse([x - r, y - r, x + r, y + r], fill=255)
    k = 6 if estilo == 0 else 8
    step = 2 if k == 6 else 3
    rp = Rs * 0.58
    pts = [(C + rp * math.cos(2 * math.pi * i / k - math.pi / 2), C + rp * math.sin(2 * math.pi * i / k - math.pi / 2))
           for i in range(k)]
    for i in range(k):
        d.line([pts[i], pts[(i + step) % k]], fill=170, width=lw)
    ring(Rs * 0.30, lw)
    ring(Rs * 0.26, lw, 120)
    m = np.asarray(im.resize((S // ss, S // ss), Image.LANCZOS), np.float32) / 255.0
    _RC[key] = m
    return m


def runa(luz, R, cx, cy, ang, color, alpha, seed=1, estilo=0, esc=1.0, aplanar=1.0):
    if alpha <= 0.004 or esc <= 0.02:
        return
    m = circulo_runico(R, seed, estilo)
    S = m.shape[0]
    out = max(4, int(S * esc) + 2)
    a = math.radians(ang)
    ca, sa = math.cos(a) * esc, math.sin(a) * esc
    A = np.array([[ca, -sa], [sa * aplanar, ca * aplanar]])
    t = np.array([out / 2, out / 2]) - A @ np.array([S / 2, S / 2])
    M = np.hstack([A, t[:, None]]).astype(np.float32)
    r = cv2.warpAffine(m, M, (out, out), flags=cv2.INTER_LINEAR)
    sumar(luz, r, cx - out / 2, cy - out / 2, color, alpha)


_BL = {}


def destello(luz, x, y, r, color, alpha):
    """Mancha de luz gaussiana (flash)."""
    r = max(2, int(r))
    if r not in _BL:
        S = r * 6
        yy, xx = np.mgrid[0:S, 0:S].astype(np.float32) - S / 2
        _BL[r] = np.exp(-(xx ** 2 + yy ** 2) / (2 * r * r))
    m = _BL[r]
    sumar(luz, m, x - m.shape[1] / 2, y - m.shape[0] / 2, color, alpha)


def hexagono(cx, cy, r, rot=-90):
    return [(cx + r * math.cos(math.radians(rot + 60 * i)), cy + r * math.sin(math.radians(rot + 60 * i))) for i in range(6)]


def foto_holo(ruta, w, h, mezcla=0.28, bordes=0.22, recorte=True):
    """Foto real con tratamiento holográfico ligero (se reconoce lo que es)."""
    im = Image.open(ruta).convert("RGBA")
    if recorte:
        r = max(w / im.width, h / im.height)
        im = im.resize((max(w, int(im.width * r + .5)), max(h, int(im.height * r + .5))), Image.LANCZOS)
        L = (im.width - w) // 2
        T = (im.height - h) // 2
        im = im.crop((L, T, L + w, T + h))
    else:
        im = im.resize((w, h), Image.LANCZOS)
    a = np.asarray(im, np.float32) / 255.0
    rgb = a[..., :3]
    g = cv2.cvtColor((rgb * 255).astype(np.uint8), cv2.COLOR_RGB2GRAY)
    duo = LUT_MAPA[g]
    gx = cv2.Sobel(g.astype(np.float32), cv2.CV_32F, 1, 0)
    gy = cv2.Sobel(g.astype(np.float32), cv2.CV_32F, 0, 1)
    e = np.sqrt(gx * gx + gy * gy)
    e = np.clip(e / (np.percentile(e, 99) + 1e-3), 0, 1) ** 1.6
    out = rgb * (1 - mezcla) * np.array([0.92, 1.0, 1.08], np.float32) + duo * mezcla + e[..., None] * c(CIAN) * bordes
    al = a[..., 3]
    lum = out.mean(-1)[al > 0.5]
    if lum.size:
        out = out * cl(0.92 / (np.percentile(lum, 98) + 1e-3), 1.0, 2.2)
    out = np.clip(out, 0, 1)
    return Spr((out * al[..., None]).astype(np.float32), al.astype(np.float32))


# ---------------------------------------------------------------- contexto de cuadro
class Ctx:
    def __init__(s, t):
        s.t = t
        s.F = np.zeros((H, W, 3), np.float32)
        s.luz = np.zeros((H, W, 3), np.float32)
        s.Lu = np.zeros((H, W, 3), np.uint8)
        s.capas = {k: [] for k in range(6)}

    def en(s, k, fn):
        s.capas[k].append(fn)

    def componer(s):
        for k in (0, 1, 2, 3):
            for fn in s.capas[k]:
                fn(s.F)
        T = s.luz + s.Lu.astype(np.float32) / 255.0
        sm = cv2.resize(T, (W // 4, H // 4), interpolation=cv2.INTER_AREA)
        b = cv2.GaussianBlur(sm, (0, 0), 2.2) * 1.25 + cv2.GaussianBlur(sm, (0, 0), 8.0) * 0.95
        s.F += T + cv2.resize(b, (W, H), interpolation=cv2.INTER_LINEAR)
        for fn in s.capas[5]:
            fn(s.F)
        return s.F


# ---------------------------------------------------------------- panel de cristal
class Panel:
    """Ficha de cristal translúcido: se abre como proyección (línea -> apertura vertical), borde de neón con chaflán."""

    def __init__(s, x, y, w, h, ch=28, color=CIAN, color2=VIOLETA):
        s.x, s.y, s.w, s.h, s.ch = x, y, w, h, ch
        s.color, s.color2 = color, color2

    @staticmethod
    def fases(tl, t_in, t_out=None):
        if tl < t_in:
            return None
        u = tl - t_in
        wf = eo(u / 0.20)
        ap = eio((u - 0.16) / 0.30)
        cont = eo((u - 0.36) / 0.30)
        k = cl(1 - u / 0.65)
        if t_out is not None and tl > t_out:
            v = tl - t_out
            if v > 0.55:
                return None
            cont = min(cont, 1 - eo(v / 0.16))
            ap = min(ap, 1 - eio((v - 0.10) / 0.26))
            wf = min(wf, 1 - eo((v - 0.38) / 0.15))
            k = max(k, cl(v / 0.25))
        return wf, ap, k, cont

    def dibujar(s, ctx, f, seed=0):
        wf, ap, k, cont = f
        x, y, w, h = s.x, s.y, s.w, s.h
        cy = y + h / 2
        fl = 1 - 0.05 * abs(ruido(ctx.t, 5.3, seed))
        if ap > 0.01:
            hh = max(3.0, h * ap)
            yy = cy - hh / 2
            chh = s.ch if hh > 2.2 * s.ch else 0
            ctx.en(2, lambda F, yy=yy, hh=hh, chh=chh: vidrio(F, x, yy, w, hh, chh, 0.93 * fl))
            linea(ctx, contorno(x, yy, w, hh, chh), s.color, 2, 0.95 * fl, True)
            if hh > 40:
                linea(ctx, contorno(x + 8, yy + 8, w - 16, hh - 16, max(0, chh - 4)), s.color2, 1, 0.50 * fl, True)
            # acentos: escuadras blancas en las esquinas rectas y muescas violetas junto a los chaflanes
            L = min(46, hh / 2)
            linea(ctx, [(x + w - L, yy - 6), (x + w + 6, yy - 6), (x + w + 6, yy + L)], BLANCO, 2, 0.9 * fl)
            linea(ctx, [(x - 6, yy + hh - L), (x - 6, yy + hh + 6), (x + L, yy + hh + 6)], BLANCO, 2, 0.9 * fl)
            if chh:
                o = 9
                linea(ctx, [(x - o * .7, yy + chh + o * .7 - 2), (x + chh + o * .7 - 2, yy - o * .7)], s.color2, 3, 0.85 * fl)
                linea(ctx, [(x + w - chh - o * .7 + 2, yy + hh + o * .7), (x + w + o * .7, yy + hh - chh - o * .7 + 2)],
                      s.color2, 3, 0.85 * fl)
            # barrido de brillo diagonal al abrir
            if 0.0 < cont < 1.0 or (k > 0 and ap >= 1):
                pass
        if wf > 0 and ap < 0.98:
            ww = w * wf
            linea(ctx, [(x + w / 2 - ww / 2, cy), (x + w / 2 + ww / 2, cy)], BLANCO, 2, 1.0)
            destello(ctx.luz, x + w / 2 - ww / 2, cy, 10, CIAN, 0.8)
            destello(ctx.luz, x + w / 2 + ww / 2, cy, 10, CIAN, 0.8)
        return cont, k

    def barrido(s, ctx, u):
        """Brillo diagonal que cruza el cristal (u 0..1)."""
        if u <= 0 or u >= 1:
            return
        w, h = int(s.w), int(s.h)
        xs = np.arange(w, dtype=np.float32)[None, :]
        ys = np.arange(h, dtype=np.float32)[:, None]
        pos = lerp(-0.3 * h, w + 0.3 * h, u)
        band = np.exp(-(((xs + ys * 0.45) - pos) / 38.0) ** 2) * mascara_chaflan(w, h, s.ch)
        sumar(ctx.luz, band, s.x, s.y, BLANCO, 0.10)


# ---------------------------------------------------------------- 1 · MAPA CON RUTA
class mapa_ruta:
    """Mapa proyectado con ruta de energía.

    puntos: lista de dict(x=%, y=%, nombre, sub, foto, lado) en % de la imagen; el primero es el origen y el último el
    destino (marcador que «cae» con su foto). Tiempos en segundos locales.
    """

    def __init__(s, mapa, puntos, zona, zona_sub=None, vista=(160, 110, 1600, 890), cam_fin=None, zoom_fin=2.75,
                 t_zoom=(1.3, 4.0), t_ruta=(4.6, 7.2), t_origen=3.3, t_tag=3.8, t_destino=7.2, t_salida=10.62,
                 curva=-0.18, rotulo_final=None, seed=3):
        s.puntos = puntos
        s.zona, s.zona_sub = zona, zona_sub
        s.vx, s.vy, s.vw, s.vh = vista
        s.t_zoom, s.t_ruta = t_zoom, t_ruta
        s.t_origen, s.t_tag, s.t_destino, s.t_salida = t_origen, t_tag, t_destino, t_salida
        s.rotulo_final = rotulo_final
        s.seed = seed
        im = cv2.imread(mapa)[..., ::-1]
        s.H0, s.W0 = im.shape[:2]
        s._textura(im)
        s.P = [(p["x"] * s.W0 / 100.0, p["y"] * s.H0 / 100.0) for p in puntos]
        if cam_fin is None:
            xs = [p[0] for p in s.P]
            ys = [p[1] for p in s.P]
            cam_fin = ((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2)
        s.cam0 = (1.0, s.W0 / 2, s.vh / 2)
        s.cam1 = (zoom_fin, cam_fin[0], cam_fin[1])
        # curva de la ruta por todos los puntos (bezier cuadrática por tramo)
        curv = []
        for a, b in zip(s.P[:-1], s.P[1:]):
            a = np.array(a, float)
            b = np.array(b, float)
            m = (a + b) / 2
            d = b - a
            ctrl = m + np.array([-d[1], d[0]]) * curva
            tt = np.linspace(0, 1, 160)[:, None]
            curv.append((1 - tt) ** 2 * a + 2 * (1 - tt) * tt * ctrl + tt ** 2 * b)
        s.curva = np.vstack(curv)
        s.pluma = mascara_chaflan(s.vw, s.vh, 44, pluma=14)
        # partículas del haz
        rng = random.Random(seed)
        s.part = []
        d0, d1 = t_ruta
        for i in range(320):
            p = rng.random()
            nac = d0 + eio_inv(p) * (d1 - d0) + rng.uniform(0, 0.08)
            s.part.append(s._p(rng, p, nac))
        for i in range(230):
            s.part.append(s._p(rng, rng.random(), rng.uniform(d1, t_salida)))
        s.fotos = {}
        s.tags = {}
        for i, p in enumerate(puntos):
            if p.get("foto"):
                ultimo = i == len(puntos) - 1
                s.fotos[i] = foto_holo(p["foto"], 500 if ultimo else 150, 281 if ultimo else 112)

    @staticmethod
    def _p(rng, p, nac):
        ang = rng.uniform(0, 2 * math.pi)
        return dict(p=p, nac=nac, vx=math.cos(ang) * rng.uniform(12, 70), vy=math.sin(ang) * rng.uniform(12, 70) - 14,
                    vida=rng.uniform(0.5, 1.4), r=rng.choice((1.2, 1.6, 2.2, 3.0)),
                    col=rng.choice((CIAN, CIAN, BLANCO, VIOLETA, MAGENTA)), fase=rng.uniform(0, 6.28))

    def _textura(s, im):
        big = cv2.resize(im, (s.W0 * 2, s.H0 * 2), interpolation=cv2.INTER_CUBIC)
        g = cv2.cvtColor(big, cv2.COLOR_RGB2GRAY)
        lo, hi = np.percentile(g, (1, 99.5))
        g = np.clip((g.astype(np.float32) - lo) / (hi - lo) * 255, 0, 255).astype(np.uint8)
        duo = LUT_MAPA[g]
        gb = cv2.GaussianBlur(g, (0, 0), 1.6).astype(np.float32)
        gx = cv2.Sobel(gb, cv2.CV_32F, 1, 0)
        gy = cv2.Sobel(gb, cv2.CV_32F, 0, 1)
        e = np.sqrt(gx * gx + gy * gy)
        e = np.clip(e / (np.percentile(e, 99) + 1e-3), 0, 1) ** 1.5
        orig = big.astype(np.float32) / 255.0
        tex = (duo * 0.62 + orig * np.array([0.40, 0.52, 0.80], np.float32) * 0.34 + e[..., None] * c(CIAN) * 0.20) * 0.84
        s.tex = (np.clip(tex, 0, 1) * 255).astype(np.uint8)

    def cam(s, t):
        u = eio(seg(t, *s.t_zoom))
        s0, x0, y0 = s.cam0
        s1, x1, y1 = s.cam1
        sc = math.exp(lerp(math.log(s0), math.log(s1), u))
        # el centro sigue al zoom de forma que el punto de destino se acerque sin vaivén
        w = (sc - s0) / (s1 - s0) if s1 != s0 else u
        cx, cy = lerp(x0, x1, w), lerp(y0, y1, w)
        sc *= 1 + 0.045 * eio(seg(t, s.t_zoom[1], s.t_salida))
        return sc, cx, cy

    def a_pantalla(s, t, pts):
        sc, cx, cy = s.cam(t)
        pts = np.asarray(pts, np.float64)
        X = s.vx + s.vw / 2 + (pts[..., 0] - cx) * sc
        Y = s.vy + s.vh / 2 + (pts[..., 1] - cy) * sc
        return np.stack([X, Y], -1)

    # -------- dibujo
    def dibujar(s, ctx, t):
        vx, vy, vw, vh = s.vx, s.vy, s.vw, s.vh
        rev = eo(seg(t, 0.15, 1.25))
        cierre = eio(seg(t, s.t_salida, s.t_salida + 0.32))
        fl = 1 - 0.04 * abs(ruido(t, 3.1, 1))
        # fondo: degradado + círculo rúnico grande
        ctx.en(0, lambda F: F.__iadd__(FONDO))
        runa(ctx.luz, 560, W / 2, H / 2, t * 3.0, VIOLETA, 0.09 * eo(seg(t, 0, 1.5)), seed=11, estilo=1)
        runa(ctx.luz, 430, W / 2, H / 2, -t * 5.0, CIAN, 0.04 * eo(seg(t, 0.3, 1.8)), seed=12)

        sc, cx, cy = s.cam(t)

        def capa_mapa(F):
            M = np.float32([[sc / 2, 0, vw / 2 - cx * sc], [0, sc / 2, vh / 2 - cy * sc]])
            v = cv2.warpAffine(s.tex, M, (vw, vh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT,
                               borderValue=(3, 5, 20)).astype(np.float32) * (1 / 255.0)
            # barra de refresco que recorre el holograma
            yy = np.arange(vh, dtype=np.float32)
            bp = ((t * 0.33) % 1.3) * vh * 1.3 - 0.15 * vh
            v *= (0.92 + 0.10 * np.exp(-((yy - bp) / 60.0) ** 2))[:, None, None]
            m = s.pluma.copy()
            if rev < 1:
                ry = rev * (vh + 80) - 40
                m *= np.clip((ry - yy) / 40.0, 0, 1)[:, None]
                k = 1 - rev
                rng = np.random.default_rng(int(t * 30))
                for _ in range(int(10 * k) + 1):
                    y0 = int(rng.integers(0, vh))
                    hh = int(rng.integers(4, 40))
                    v[y0:y0 + hh] = np.roll(v[y0:y0 + hh], int(rng.normal() * 60 * k), axis=1)
            if cierre > 0:
                bh = max(2.0, vh * (1 - cierre))
                m *= np.clip((bh / 2 - np.abs(yy - vh / 2)) / 8.0, 0, 1)[:, None]
            m *= fl
            roi = F[vy:vy + vh, vx:vx + vw]
            roi *= (1 - m)[..., None]
            roi += v * m[..., None]

        ctx.en(1, capa_mapa)
        vis = rev * (1 - cierre)
        if vis <= 0.01:
            return
        # rejilla que se mueve con la cámara (cada 2,5 % / 10 % de la imagen)
        ga = 0.20 * rev * (1 - cierre)
        for i in range(0, 41):
            xm = i * s.W0 / 40.0
            X = vx + vw / 2 + (xm - cx) * sc
            if vx + 2 < X < vx + vw - 2:
                linea(ctx, [(X, vy + 4), (X, vy + vh - 4)], CIAN, 1, ga * (1.0 if i % 4 == 0 else 0.42))
                L = 14 if i % 4 == 0 else 7
                linea(ctx, [(X, vy - 2), (X, vy + L)], CIAN, 1, 0.7 * vis)
                linea(ctx, [(X, vy + vh - L), (X, vy + vh + 2)], CIAN, 1, 0.7 * vis)
            ym = i * s.H0 / 40.0
            Y = vy + vh / 2 + (ym - cy) * sc
            if vy + 2 < Y < vy + vh - 2:
                linea(ctx, [(vx + 4, Y), (vx + vw - 4, Y)], CIAN, 1, ga * (1.0 if i % 4 == 0 else 0.42))
                L = 14 if i % 4 == 0 else 7
                linea(ctx, [(vx - 2, Y), (vx + L, Y)], CIAN, 1, 0.7 * vis)
                linea(ctx, [(vx + vw - L, Y), (vx + vw + 2, Y)], CIAN, 1, 0.7 * vis)
        # marco del proyector (se traza al entrar)
        tr = eo(seg(t, 0.0, 1.1))
        hh = vh * (1 - cierre)
        yy0 = vy + vh / 2 - hh / 2
        marco = contorno(vx, yy0, vw, hh, 44 if hh > 100 else 0)
        linea(ctx, parcial(marco, tr), CIAN, 2, 0.95 * fl)
        if hh > 60:
            linea(ctx, parcial(contorno(vx + 10, yy0 + 10, vw - 20, hh - 20, 36), tr), VIOLETA, 1, 0.55)
        L = 70
        a = 0.95 * tr
        linea(ctx, [(vx + vw - L, yy0 - 8), (vx + vw + 8, yy0 - 8), (vx + vw + 8, yy0 + L)], BLANCO, 3, a)
        linea(ctx, [(vx - 8, yy0 + hh - L), (vx - 8, yy0 + hh + 8), (vx + L, yy0 + hh + 8)], BLANCO, 3, a)
        if cierre > 0:
            linea(ctx, [(vx, yy0), (vx + vw, yy0)], BLANCO, 2, cierre)
            linea(ctx, [(vx, yy0 + hh), (vx + vw, yy0 + hh)], BLANCO, 2, cierre)
        if rev < 1:
            ry = vy + rev * (vh + 80) - 40
            if vy < ry < vy + vh:
                linea(ctx, [(vx, ry), (vx + vw, ry)], BLANCO, 2, 0.9)
                destello(ctx.luz, vx + vw / 2, ry, 30, CIAN, 0.35)

        # rótulo de zona
        s._zona(ctx, t, vis)
        # ruta
        s._ruta(ctx, t, vis)
        # marcadores
        n = len(s.P)
        scr = s.a_pantalla(t, s.P)
        for i in range(n):
            X, Y = scr[i]
            if i < n - 1:
                tl = t - (s.t_origen if i == 0 else lerp(s.t_ruta[0], s.t_ruta[1], i / (n - 1)))
                s._anillo(ctx, X, Y, tl, CIAN, vis)
            else:
                s._cae(ctx, X, Y, t - s.t_destino, vis)
        # etiquetas
        s._tag_origen(ctx, t, scr[0])
        s._panel_destino(ctx, t, scr[-1])

    def _zona(s, ctx, t, vis):
        u = seg(t, 1.6, 2.5)
        if u <= 0:
            return
        x, y = s.vx + 44, s.vy + 30
        op = vis * eo(u * 3)
        if s.zona_sub:
            sub = texto(decodificar(s.zona_sub, eo(seg(t, 1.5, 2.1)), int(t * 20)), 28, (150, 235, 255), mono=True,
                        glow=CIAN, gk=.7, track=4)
            ctx.en(5, lambda F: pegar(F, sub, x + 4, y, op))
        tit = texto(decodificar(s.zona, u, int(t * 24) + 7), 76, BLANCO, "Bold", glow=CIAN, gk=1.0, track=3)
        if u < 1:
            tit = glitch_spr(tit, (1 - u) * 0.8, int(t * 30))
        ctx.en(5, lambda F: pegar(F, tit, x, y + 34, op))
        wfin = texto(s.zona, 76, BLANCO, "Bold", glow=CIAN, gk=1.0, track=3).w
        lu = eo(seg(t, 1.9, 2.7))
        yl = y + 132
        linea(ctx, [(x, yl), (x + wfin * lu, yl)], CIAN, 2, 0.9 * vis)
        linea(ctx, [(x + wfin * lu, yl), (x + wfin * lu + 26 * lu, yl - 14 * lu)], CIAN, 2, 0.9 * vis)
        runa(ctx.luz, 16, x + wfin * lu + 56, yl - 14, t * 60, VIOLETA, 0.9 * vis * lu, seed=4, esc=1.0)

    def _anillo(s, ctx, X, Y, tl, color, vis, esc=1.0):
        if tl < 0:
            return
        t = ctx.t
        pop = eback(tl / 0.45) * esc
        runa(ctx.luz, 58, X, Y, t * 40, color, 0.85 * vis * cl(tl / 0.3), seed=21, esc=pop)
        runa(ctx.luz, 30, X, Y, -t * 70, VIOLETA, 0.8 * vis * cl(tl / 0.3), seed=22, estilo=1, esc=pop)
        for k in range(3):
            ph = ((tl * 0.75) + k / 3.0) % 1.0
            if tl * 0.75 < k / 3.0:
                continue
            r = (16 + ph * 92) * esc
            circulo(ctx, X, Y, r, color, 2, vis * (1 - ph) ** 1.6 * 0.95)
        circulo(ctx, X, Y, 15 * pop, BLANCO, 2, vis)
        rd = 8 * pop
        linea(ctx, [(X, Y - rd), (X + rd, Y), (X, Y + rd), (X - rd, Y)], BLANCO, 2, vis, True)
        destello(ctx.luz, X, Y, 9, BLANCO, 0.9 * vis)
        if tl < 0.35:
            destello(ctx.luz, X, Y, 40, color, (1 - tl / 0.35) * 0.9 * vis)

    def _cae(s, ctx, X, Y, tl, vis):
        """Marcador final: haz desde arriba, anillo de fijación que se cierra, impacto con onda."""
        if tl < 0:
            return
        imp = 0.32
        if tl < imp:
            u = tl / imp
            ytop = s.vy + 6
            yb = lerp(ytop, Y, eio(u))
            linea(ctx, [(X, ytop), (X, yb)], BLANCO, 3, 0.9 * vis)
            linea(ctx, [(X, ytop), (X, yb)], MAGENTA, 9, 0.35 * vis)
            r = lerp(250, 20, eio(u))
            circulo(ctx, X, Y, r, MAGENTA, 2, vis * eo(u))
            circulo(ctx, X, Y, r * 1.12, CIAN, 1, vis * eo(u) * .6)
            for q in range(4):
                a = q * math.pi / 2 + u * 1.2
                linea(ctx, [(X + math.cos(a) * r * 1.2, Y + math.sin(a) * r * 1.2),
                            (X + math.cos(a) * r * 1.45, Y + math.sin(a) * r * 1.45)], BLANCO, 2, vis * eo(u))
            return
        v = tl - imp
        if v < 0.8:
            q = v / 0.8
            circulo(ctx, X, Y, 20 + eo(q) * 230, MAGENTA, 3, vis * (1 - q) ** 1.5)
            circulo(ctx, X, Y, 20 + eo(q) * 150, CIAN, 2, vis * (1 - q) ** 1.5)
            destello(ctx.luz, X, Y, 60, BLANCO, vis * (1 - q) ** 2 * 1.2)
        s._anillo(ctx, X, Y, v, MAGENTA, vis, esc=1.15)

    def _ruta(s, ctx, t, vis):
        d0, d1 = s.t_ruta
        u = eio(seg(t, d0, d1))
        if u <= 0:
            return
        pts = s.a_pantalla(t, s.curva)
        dib = parcial(pts, u)
        fl = 1 - 0.08 * abs(ruido(t, 9, 2))
        linea(ctx, dib, VIOLETA, 16, 0.32 * vis * fl)
        linea(ctx, dib, CIAN, 7, 0.75 * vis * fl)
        linea(ctx, dib, BLANCO, 2, 1.0 * vis)
        # pulsos que viajan cuando el haz ya está completo
        if t > d1:
            for k in range(3):
                q = ((t - d1) * 0.55 + k / 3.0) % 1.0
                lin = tramo(pts, max(0, q - 0.09), q)
                linea(ctx, lin, BLANCO, 5, 0.9 * vis * math.sin(math.pi * q))
        # cabeza del haz
        if u < 1:
            hx, hy = dib[-1]
            destello(ctx.luz, hx, hy, 22, CIAN, 1.1 * vis)
            destello(ctx.luz, hx, hy, 6, BLANCO, 1.5 * vis)
            L = 30
            linea(ctx, [(hx - L, hy), (hx + L, hy)], BLANCO, 1, 0.8 * vis)
            linea(ctx, [(hx, hy - L), (hx, hy + L)], BLANCO, 1, 0.8 * vis)
        # partículas
        for p in s.part:
            age = t - p["nac"]
            if age < 0 or age > p["vida"] or p["p"] > u + 1e-3:
                continue
            q = age / p["vida"]
            bx, by = parcial(pts, p["p"])[-1]
            x = bx + p["vx"] * age
            y = by + p["vy"] * age
            a = (1 - q) ** 1.3 * (0.6 + 0.4 * math.sin(t * 20 + p["fase"])) * vis
            circulo(ctx, x, y, p["r"], p["col"], 1, a, relleno=True)

    def _tag_origen(s, ctx, t, scr):
        p = s.puntos[0]
        f = Panel.fases(t, s.t_tag, s.t_salida - 0.25)
        if f is None:
            return
        X, Y = scr
        foto = s.fotos.get(0)
        tn = texto(p["nombre"], 38, BLANCO, "Bold", glow=CIAN, gk=.8, track=1)
        ts = texto(p.get("sub", ""), 22, CIAN, mono=True, glow=CIAN, gk=.5, track=2) if p.get("sub") else None
        fw = foto.a.shape[1] if foto else 0
        w = 22 + fw + 22 + max(tn.w, ts.w if ts else 0) + 30
        h = 140
        x = cl(X - w / 2, s.vx + 30, s.vx + s.vw - 30 - w)
        y = Y + 96
        pn = Panel(x, y, w, h, ch=20)
        cont, k = pn.dibujar(ctx, f, seed=5)
        lu = eo(seg(t, s.t_tag, s.t_tag + 0.35))
        linea(ctx, [(X, Y + 20), (X, Y + 20 + (y - 6 - Y - 20) * lu)], CIAN, 2, 0.9 * (1 - (1 - cont) * 0.5 * (t > s.t_tag + 1)))
        circulo(ctx, X, y - 6, 3.5, BLANCO, 1, lu, relleno=True)
        if cont > 0:
            fx, fy = x + 22, y + (h - (foto.a.shape[0] if foto else 0)) / 2
            g = int(t * 30)
            ctx.en(5, lambda F: (pegar(F, glitch_spr(foto, k, g), fx, fy, cont) if foto else None,
                                 linea_marco(F, fx, fy, fw, foto.a.shape[0] if foto else 0, cont)))
            tx = x + 22 + fw + 22
            nombre = texto(decodificar(p["nombre"], seg(t, s.t_tag + 0.4, s.t_tag + 1.1), g), 38, BLANCO, "Bold",
                           glow=CIAN, gk=.8, track=1)
            ctx.en(5, lambda F: pegar(F, glitch_spr(nombre, k, g + 1), tx, y + 26, cont))
            if ts:
                ctx.en(5, lambda F: pegar(F, glitch_spr(ts, k, g + 2), tx + 2, y + 84, cont))
            pn.barrido(ctx, seg(t, s.t_tag + 0.45, s.t_tag + 1.2))

    def _panel_destino(s, ctx, t, scr):
        p = s.puntos[-1]
        t_in = s.t_destino + 0.55
        f = Panel.fases(t, t_in, s.t_salida - 0.3)
        if f is None:
            return
        X, Y = scr
        foto = s.fotos.get(len(s.puntos) - 1)
        rot = s.rotulo_final or p["nombre"]
        tr = texto(rot, 36, BLANCO, "Bold", glow=MAGENTA, gk=.8, track=1)
        fw, fh = (foto.a.shape[1], foto.a.shape[0]) if foto else (0, 0)
        w = max(fw, tr.w) + 60
        h = 22 + fh + 18 + 48 + 18
        x = min(X + 110, s.vx + s.vw - 26 - w)
        y = cl(Y - h / 2, s.vy + 24, s.vy + s.vh - 24 - h)
        pn = Panel(x, y, w, h, ch=26, color=CIAN, color2=MAGENTA)
        cont, k = pn.dibujar(ctx, f, seed=9)
        # guía del marcador al panel
        lu = eo(seg(t, t_in - 0.1, t_in + 0.3))
        ex = X + 26 + (x - 8 - X - 26) * lu
        linea(ctx, [(X + 26, Y), (ex, Y)], MAGENTA, 2, 0.95)
        circulo(ctx, x - 8, Y, 4, BLANCO, 1, lu, relleno=True)
        if cont > 0:
            g = int(t * 30)
            fx, fy = x + (w - fw) / 2, y + 22
            rev = eo(seg(t, t_in + 0.35, t_in + 0.95))
            ctx.en(5, lambda F: (pegar(F, glitch_spr(recorte_v(foto, rev), k, g), fx, fy, cont),
                                 linea_marco(F, fx, fy, fw, fh, cont)))
            if rev < 1:
                linea(ctx, [(fx, fy + fh * rev), (fx + fw, fy + fh * rev)], BLANCO, 2, 0.9)
            rr = texto(decodificar(rot, seg(t, t_in + 0.6, t_in + 1.3), g), 36, BLANCO, "Bold", glow=MAGENTA, gk=.8,
                       track=1)
            ctx.en(5, lambda F: pegar(F, glitch_spr(rr, k, g + 3), x + (w - tr.w) / 2, fy + fh + 18, cont))
            pn.barrido(ctx, seg(t, t_in + 0.5, t_in + 1.3))


def eio_inv(p):
    """Inverso aproximado de eio (para que las partículas nazcan donde pasa la cabeza del haz)."""
    lo, hi = 0.0, 1.0
    for _ in range(20):
        m = (lo + hi) / 2
        if eio(m) < p:
            lo = m
        else:
            hi = m
    return (lo + hi) / 2


def recorte_v(sp, u):
    """Revela un sprite de arriba hacia abajo (u 0..1)."""
    if sp is None or u >= 1:
        return sp
    h = sp.a.shape[0]
    k = int(h * cl(u))
    a = sp.a.copy()
    rgb = sp.rgb.copy()
    a[k:] = 0
    rgb[k:] = 0
    return Spr(rgb, a, sp.ox, sp.oy, sp.w, sp.h)


def linea_marco(F, x, y, w, h, op):
    """Filo fino cian alrededor de una foto (dibujado encima, sin bloom)."""
    if w <= 0 or op <= 0:
        return
    x, y, w, h = int(x), int(y), int(w), int(h)
    col = c(CIAN) * op
    for (a, b, cc, d) in ((y, y + 2, x, x + w), (y + h - 2, y + h, x, x + w)):
        F[max(a, 0):min(b, H), max(cc, 0):min(d, W)] = F[max(a, 0):min(b, H), max(cc, 0):min(d, W)] * (1 - op) + col
    for (a, b, cc, d) in ((y, y + h, x, x + 2), (y, y + h, x + w - 2, x + w)):
        F[max(a, 0):min(b, H), max(cc, 0):min(d, W)] = F[max(a, 0):min(b, H), max(cc, 0):min(d, W)] * (1 - op) + col


# ---------------------------------------------------------------- 2 · FICHA
_HX = {}


def mascara_hex(S, r):
    key = (S, r)
    if key not in _HX:
        im = Image.new("L", (S * 2, S * 2), 0)
        ImageDraw.Draw(im).polygon(hexagono(S, S, r * 2), fill=255)
        _HX[key] = np.asarray(im.resize((S, S), Image.LANCZOS), np.float32) / 255.0
    return _HX[key]


class ficha:
    """Ficha de cristal con título, íconos (ruta_png, texto, color, valor) en hexágonos y contador acumulado."""

    def __init__(s, titulo, iconos, x=340, y=230, w=1240, h=620, t_in=0.55, t_iconos=1.9, paso=1.0, t_out=9.35,
                 prefijo="= "):
        s.titulo, s.iconos = titulo, iconos
        s.pn = Panel(x, y, w, h, ch=34)
        s.x, s.y, s.w, s.h = x, y, w, h
        s.t_in, s.t_ic, s.paso, s.t_out = t_in, t_iconos, paso, t_out
        s.prefijo = prefijo
        s.R = 92
        S = 2 * s.R
        s.hexm = mascara_hex(S, s.R - 6)
        s.spr = []
        for (ruta, _, _, _) in iconos:
            im = Image.open(ruta).convert("RGBA").resize((S, S), Image.LANCZOS)
            sp = de_pil(im)
            sp.rgb *= s.hexm[..., None]
            sp.a *= s.hexm
            sp.ox = sp.oy = s.R
            s.spr.append(sp)
        s.total = sum(v for (_, _, _, v) in iconos)

    def centro(s, i):
        n = len(s.iconos)
        return s.x + s.w / 2 + (i - (n - 1) / 2) * 250, s.y + 268

    def valor(s, t):
        v = 0.0
        for i, (_, _, _, val) in enumerate(s.iconos):
            ti = s.t_ic + i * s.paso
            v += val * eo(seg(t, ti + 0.25, ti + 0.6))
        return int(round(v))

    def dibujar(s, ctx, t):
        f = Panel.fases(t, s.t_in, s.t_out)
        if f is None:
            return
        cont, k = s.pn.dibujar(ctx, f, seed=13)
        if cont <= 0:
            return
        g = int(ctx.t * 30)
        x, y, w = s.x, s.y, s.w
        # título
        u = seg(t, s.t_in + 0.4, s.t_in + 1.2)
        tf = texto(s.titulo, 66, BLANCO, "Bold", glow=CIAN, gk=.9, track=2)
        tt = texto(decodificar(s.titulo, u, g), 66, BLANCO, "Bold", glow=CIAN, gk=.9, track=2)
        tx = x + (w - tf.w) / 2
        ctx.en(5, lambda F: pegar(F, glitch_spr(tt, max(k, (1 - u) * .5), g), tx, y + 40, cont))
        lu = eo(seg(t, s.t_in + 0.6, s.t_in + 1.3))
        yl = y + 136
        linea(ctx, [(x + w / 2 - (w / 2 - 70) * lu, yl), (x + w / 2 + (w / 2 - 70) * lu, yl)], CIAN, 2, 0.8 * cont)
        for sx in (-1, 1):
            xx = x + w / 2 + sx * (w / 2 - 70) * lu
            linea(ctx, [(xx, yl - 6), (xx + sx * 8, yl), (xx, yl + 6)], BLANCO, 2, 0.9 * cont * lu)
        pn_barr = seg(t, s.t_in + 0.5, s.t_in + 1.4)
        s.pn.barrido(ctx, pn_barr)
        # íconos
        for i, ((_, txt, col, val), sp) in enumerate(zip(s.iconos, s.spr)):
            ti = s.t_ic + i * s.paso
            dt = t - ti
            cx, cy = s.centro(i)
            # zócalo apagado mientras no llega
            hx = hexagono(cx, cy, s.R)
            if dt < 0:
                linea(ctx, hx, CIAN, 1, 0.28 * cont, True)
                continue
            tr = eo(dt / 0.35)
            linea(ctx, parcial(hx + [hx[0]], tr), col, 3, 0.95 * cont)
            linea(ctx, hexagono(cx, cy, s.R + 10), CIAN, 1, 0.45 * cont * tr, True)
            runa(ctx.luz, 118, cx, cy, ctx.t * 22 * (1 if i % 2 else -1), col, 0.33 * cont * tr, seed=30 + i, esc=1.0)
            rev = eo(seg(dt, 0.08, 0.5))
            if rev > 0:
                esc = lerp(1.3, 1.0, eback(seg(dt, 0.08, 0.55), 1.2))
                spi = sp
                if abs(esc - 1) > 0.01:
                    S = int(2 * s.R * esc)
                    spi = Spr(cv2.resize(sp.rgb, (S, S)), cv2.resize(sp.a, (S, S)), S / 2, S / 2)
                if rev < 1:
                    hh = spi.a.shape[0]
                    k2 = int(hh * (1 - rev))
                    a = spi.a.copy()
                    rgb = spi.rgb.copy()
                    a[:k2] = 0
                    rgb[:k2] = 0
                    spi = glitch_spr(Spr(rgb, a, spi.ox, spi.oy), (1 - rev), g + i)
                    if k2 < hh:
                        yy = cy - hh / 2 + k2
                        linea(ctx, [(cx - hh / 2, yy), (cx + hh / 2, yy)], BLANCO, 2, 0.9)
                ctx.en(5, lambda F, spi=spi, cx=cx, cy=cy: pegar(F, spi, cx, cy, cont))
            if dt < 0.7:
                q = seg(dt, 0.4, 0.8)
                if q > 0:
                    circulo(ctx, cx, cy, s.R + q * 90, col, 3, cont * (1 - q) ** 1.5)
                    destello(ctx.luz, cx, cy, 70, col, cont * (1 - q) ** 2 * 0.8)
            destello(ctx.luz, cx, cy, 60, col, 0.10 * cont * tr * (1 + 0.3 * math.sin(ctx.t * 3 + i)))
            # ×15
            uq = seg(dt, 0.3, 0.7)
            if uq > 0:
                tq = texto(decodificar(txt, uq, g + 5 * i), 54, BLANCO, "Bold", glow=col, gk=1.1, track=2)
                tqf = texto(txt, 54, BLANCO, "Bold", glow=col, gk=1.1, track=2)
                ctx.en(5, lambda F, tq=tq, cx=cx, cy=cy, w_=tqf.w: pegar(F, tq, cx - w_ / 2, cy + s.R + 18, cont))
        # contador
        if t >= s.t_ic + 0.25:
            v = s.valor(t)
            t_fin = s.t_ic + (len(s.iconos) - 1) * s.paso + 0.6
            pulso = eback(seg(t, t_fin, t_fin + 0.4), 2.5) if t >= t_fin else 0
            esc = 1 + 0.22 * (1 - pulso) * (t >= t_fin) if t < t_fin + 0.4 else 1
            col = MAGENTA if t >= t_fin else CIAN
            tam = int(round(118 * esc))
            tc = texto(f"{s.prefijo}{v}", tam, BLANCO, "Bold", glow=col, gk=1.15, track=3)
            tw = texto(f"{s.prefijo}{s.total}", tam, BLANCO, "Bold", glow=col, gk=1.15, track=3).w
            cxc, cyc = x + w / 2, y + 468 + 56
            op = cont * eo(seg(t, s.t_ic + 0.25, s.t_ic + 0.5))
            ctx.en(5, lambda F: pegar(F, glitch_spr(tc, k, g + 77), cxc - tw / 2, cyc - tc.h / 2 - 6, op))
            if t >= t_fin:
                q = seg(t, t_fin, t_fin + 0.9)
                circulo(ctx, cxc, cyc, 60 + eo(q) * 300, MAGENTA, 3, cont * (1 - q) ** 1.4)
                destello(ctx.luz, cxc, cyc, 90, MAGENTA, cont * (1 - q) ** 2 * 1.0)
                lu = eo(seg(t, t_fin, t_fin + 0.5))
                yl = cyc + 76
                linea(ctx, [(cxc - 200 * lu, yl), (cxc + 200 * lu, yl)], MAGENTA, 3, cont)
                runa(ctx.luz, 26, cxc - 200 * lu - 34, yl, ctx.t * 50, MAGENTA, cont * lu, seed=41, estilo=1)
                runa(ctx.luz, 26, cxc + 200 * lu + 34, yl, -ctx.t * 50, MAGENTA, cont * lu, seed=42, estilo=1)


# ---------------------------------------------------------------- 3 · TARJETA DE JEFE + RÓTULO
class tarjeta:
    """Tarjeta de jefe: proyección holográfica de la foto, nombre, dato y barra de vida por fases."""

    def __init__(s, foto, titulo, sub, pie_foto=None, fases=4, x=150, y=140, w=720, h=716, t_in=0.3,
                 t_barra=(2.6, 7.6), t_out=7.95, colores=(CIAN, VIOLETA, MAGENTA, (90, 255, 190))):
        s.titulo, s.sub, s.pie = titulo, sub, pie_foto
        s.x, s.y, s.w, s.h = x, y, w, h
        s.pn = Panel(x, y, w, h, ch=36, color=CIAN, color2=VIOLETA)
        s.t_in, s.t_barra, s.t_out = t_in, t_barra, t_out
        s.fases_n, s.colores = fases, colores
        s.fw, s.fh = w - 80, int((w - 80) * 9 / 16)
        s.foto = foto_holo(foto, s.fw, s.fh, mezcla=0.22, bordes=0.18)

    def dibujar(s, ctx, t):
        f = Panel.fases(t, s.t_in, s.t_out)
        if f is None:
            return
        cont, k = s.pn.dibujar(ctx, f, seed=17)
        if cont <= 0:
            return
        g = int(ctx.t * 30)
        x, y, w = s.x, s.y, s.w
        fx, fy = x + 40, y + 40
        rev = eo(seg(t, s.t_in + 0.45, s.t_in + 1.25))
        foto = recorte_v(s.foto, rev)
        fl = 1 - 0.06 * abs(ruido(ctx.t, 4, 3))
        ctx.en(5, lambda F: (pegar(F, glitch_spr(foto, k, g), fx, fy, cont * fl), linea_marco(F, fx, fy, s.fw, s.fh, cont)))
        if rev < 1:
            linea(ctx, [(fx - 10, fy + s.fh * rev), (fx + s.fw + 10, fy + s.fh * rev)], BLANCO, 2, cont)
            destello(ctx.luz, fx + s.fw / 2, fy + s.fh * rev, 26, CIAN, 0.5 * cont)
        # emisor: círculo rúnico en la esquina de la foto
        runa(ctx.luz, 46, fx + s.fw - 6, fy + 6, ctx.t * 35, CIAN, 0.9 * cont * rev, seed=51)
        runa(ctx.luz, 24, fx + s.fw - 6, fy + 6, -ctx.t * 70, VIOLETA, 0.9 * cont * rev, seed=52, estilo=1)
        yy = fy + s.fh + 14
        if s.pie:
            tp = texto(s.pie, 22, CIAN, mono=True, glow=CIAN, gk=.5, track=3)
            ctx.en(5, lambda F, yy=yy: pegar(F, tp, fx, yy, cont * rev))
            yy += 44
        u = seg(t, s.t_in + 0.9, s.t_in + 1.6)
        tt = texto(decodificar(s.titulo, u, g), 62, BLANCO, "Bold", glow=CIAN, gk=.95, track=2)
        ctx.en(5, lambda F, yy=yy: pegar(F, glitch_spr(tt, max(k, (1 - u) * .5), g + 1), fx - 2, yy, cont))
        yy += 80
        u2 = seg(t, s.t_in + 1.3, s.t_in + 2.0)
        ts = texto(decodificar(s.sub, u2, g + 9), 40, (200, 240, 255), "SemiBold", glow=VIOLETA, gk=.7, track=1)
        ctx.en(5, lambda F, yy=yy: pegar(F, ts, fx, yy, cont))
        yy += 70
        s._barra(ctx, t, fx, yy, s.fw, cont, g)

    def _barra(s, ctx, t, x, y, w, cont, g):
        op = cont * eo(seg(t, s.t_in + 1.7, s.t_in + 2.1))
        if op <= 0:
            return
        n = s.fases_n
        vida = 1 - eio(seg(t, *s.t_barra)) * 0.97
        fase = min(n - 1, int((1 - vida) * n))
        col = s.colores[fase % len(s.colores)]
        bh = 26
        yb = y + 40
        # cabecera de la barra
        th = texto(f"FASE {fase + 1}/{n}", 24, col, mono=True, glow=col, gk=.7, track=3)
        tv = texto(f"VIDA {int(round(vida * 100)):3d} %", 24, BLANCO, mono=True, glow=CIAN, gk=.4, track=2)
        ctx.en(5, lambda F: (pegar(F, th, x, y, op), pegar(F, tv, x + w - tv.w, y, op)))
        # segmentos
        gap = 8
        sw = (w - gap * (n - 1)) / n
        for i in range(n):
            # el segmento 0 es el último 25 % de vida (derecha a izquierda = vida que se pierde)
            sx = x + i * (sw + gap)
            lo, hi = i / n, (i + 1) / n
            lleno = cl((vida - lo) / (hi - lo))
            linea(ctx, contorno(sx, yb, sw, bh, 8), CIAN, 1, 0.55 * op, True)
            if lleno > 0:
                ww = sw * lleno
                ctx.en(2, lambda F, sx=sx, ww=ww: relleno(F, sx + 3, yb + 3, ww - 6, bh - 6, col, 0.85 * op))
            tl = texto(f"{int(hi * 100)}%", 18, (170, 220, 255), mono=True, glow=None)
            if i < n - 1:
                ctx.en(5, lambda F, sx=sx, tl=tl: pegar(F, tl, sx + sw + gap / 2 - tl.w / 2, yb + bh + 6, op * 0.8))
        # destello en cada cambio de fase
        for j in range(1, n):
            tc = s.t_barra[0] + eio_inv(min(1, j / n / 0.97)) * (s.t_barra[1] - s.t_barra[0])
            q = seg(t, tc, tc + 0.6)
            if 0 < q < 1:
                xc = x + (n - j) * (sw + gap) - gap / 2
                circulo(ctx, xc, yb + bh / 2, 10 + eo(q) * 60, s.colores[j % len(s.colores)], 2, op * (1 - q) ** 1.4)
                destello(ctx.luz, xc, yb + bh / 2, 18, s.colores[j % len(s.colores)], 0.6 * op * (1 - q) ** 2)
        xe = x + vida * w
        destello(ctx.luz, xe, yb + bh / 2, 7, BLANCO, op * 0.6)


def relleno(F, x, y, w, h, col, op):
    x, y, w, h = int(x), int(y), int(w), int(h)
    if w <= 0 or h <= 0:
        return
    roi = F[y:y + h, x:x + w]
    gy = np.linspace(1.15, 0.7, h, dtype=np.float32)[:, None, None]
    roi[:] = roi * (1 - op) + c(col) * gy * op


class rotulo:
    """Rótulo inferior: sello rúnico que se estampa (con un número o signo) + barra de cristal con texto."""

    def __init__(s, texto_, sello="5", x=150, y=884, h=100, t_in=2.2, t_out=7.75, color=MAGENTA):
        s.txt, s.sello = texto_, sello
        s.x, s.y, s.h = x, y, h
        s.t_in, s.t_out, s.color = t_in, t_out, color
        s.tf = texto(texto_, 52, BLANCO, "Bold", glow=color, gk=.8, track=1)
        s.R = 60
        s.bx = x + 2 * s.R + 24
        s.bw = s.tf.w + 70

    def dibujar(s, ctx, t):
        tl = t - s.t_in
        if tl < 0:
            return
        out = seg(t, s.t_out, s.t_out + 0.5)
        if out >= 1:
            return
        g = int(ctx.t * 30)
        cx, cy = s.x + s.R, s.y + s.h / 2
        # sello: cae grande y se aplasta con onda
        u = seg(tl, 0, 0.32)
        esc = lerp(2.2, 1.0, eio(u)) * (1 - eio(seg(t, s.t_out + 0.25, s.t_out + 0.5)))
        op = eo(u * 1.5) * (1 - seg(t, s.t_out + 0.3, s.t_out + 0.5))
        runa(ctx.luz, s.R, cx, cy, ctx.t * 30 + (1 - u) * 90, s.color, 1.0 * op, seed=61, estilo=1, esc=esc)
        runa(ctx.luz, int(s.R * 0.72), cx, cy, -ctx.t * 45, CIAN, 0.7 * op, seed=62, esc=esc)
        circulo(ctx, cx, cy, s.R * 0.5 * esc, BLANCO, 2, op)
        ctx.en(5, lambda F: disco(F, cx, cy, s.R * 0.46 * esc, (34, 8, 46), 0.92 * op))
        num = texto(s.sello, int(70 * max(esc, 0.05)), BLANCO, "Bold", glow=s.color, gk=1.3)
        ctx.en(5, lambda F: pegar(F, num, cx - num.w / 2, cy - num.h / 2 - 3 * esc, op))
        q = seg(tl, 0.32, 1.0)
        if 0 < q < 1:
            circulo(ctx, cx, cy, s.R + eo(q) * 160, s.color, 3, (1 - q) ** 1.5)
            destello(ctx.luz, cx, cy, 70, s.color, (1 - q) ** 2 * 1.1)
        # barra de cristal que se despliega desde el sello
        wu = eio(seg(tl, 0.35, 0.8)) * (1 - eio(seg(t, s.t_out, s.t_out + 0.3)))
        if wu > 0.01:
            bw = s.bw * wu
            bx, by, bh = s.bx, s.y + 8, s.h - 16
            ctx.en(2, lambda F: vidrio(F, bx, by, bw, bh, 18 if bw > 40 else 0, 0.92))
            linea(ctx, contorno(bx, by, bw, bh, 18 if bw > 40 else 0), CIAN, 2, 0.9, True)
            linea(ctx, [(cx + s.R + 4, cy), (bx, cy)], s.color, 2, 0.9)
            linea(ctx, [(bx + 6, by + 14), (bx + 6, by + bh - 14)], s.color, 5, 0.95)
            linea(ctx, [(bx + bw - 60, by + bh + 8), (bx + bw + 8, by + bh + 8)], BLANCO, 2, 0.8)
            destello(ctx.luz, bx + bw, by + bh / 2, 18, CIAN, 0.6 * (1 - wu) + 0.15)
            ut = seg(tl, 0.6, 1.3)
            k = (1 - ut) * 0.6 + seg(t, s.t_out - 0.05, s.t_out + 0.2) * 0.8
            tt = texto(decodificar(s.txt, ut, g), 52, BLANCO, "Bold", glow=s.color, gk=.8, track=1)
            tt = glitch_spr(tt, k, g)
            ctx.en(5, lambda F: pegar(F, recorte_h(tt, bw - 30), bx + 34, by + (bh - s.tf.h) / 2 - 2, 1.0))


def recorte_h(sp, wmax):
    if sp.w + sp.ox <= wmax:
        return sp
    k = int(max(0, wmax + sp.ox))
    a = sp.a.copy()
    rgb = sp.rgb.copy()
    a[:, k:] = 0
    rgb[:, k:] = 0
    return Spr(rgb, a, sp.ox, sp.oy, sp.w, sp.h)


def disco(F, cx, cy, r, col, op):
    r = int(r)
    if r < 2:
        return
    m = np.zeros((2 * r + 2, 2 * r + 2), np.float32)
    cv2.circle(m, (r + 1, r + 1), r, 1.0, -1, cv2.LINE_AA)
    x0, y0 = int(cx) - r - 1, int(cy) - r - 1
    roi = F[y0:y0 + m.shape[0], x0:x0 + m.shape[1]]
    mm = m[:roi.shape[0], :roi.shape[1]][..., None] * op
    roi *= 1 - mm
    roi += c(col) * mm


# ---------------------------------------------------------------- gameplay de fondo
class Clip:
    def __init__(s, ruta, inicio, zoom=1.12):
        s.ruta, s.inicio = ruta, inicio
        s.zw = int(round(W * zoom / 2)) * 2
        s.zh = int(round(H * zoom / 2)) * 2
        s.p = None
        s.sig = -1
        s.ult = np.zeros((H, W, 3), np.uint8)

    def _abrir(s, i):
        if s.p:
            s.p.kill()
        cmd = [FF, "-v", "error", "-ss", f"{s.inicio + i / FPS:.3f}", "-i", s.ruta, "-vf",
               f"scale={s.zw}:{s.zh},crop={W}:{H}", "-f", "rawvideo", "-pix_fmt", "rgb24", "-threads", "2", "-"]
        s.p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, bufsize=W * H * 3 * 2)
        s.sig = i

    def cuadro(s, i):
        if s.p is None or i != s.sig:
            s._abrir(i)
        b = s.p.stdout.read(W * H * 3)
        s.sig += 1
        if len(b) == W * H * 3:
            s.ult = np.frombuffer(b, np.uint8).reshape(H, W, 3)
        return s.ult

    def cerrar(s):
        if s.p:
            s.p.kill()
            s.p = None


def tratar(fr, osc=0.92):
    """Gameplay como transmisión holográfica: mitad color real enfriado, mitad duotono, más oscuro."""
    g = cv2.cvtColor(fr, cv2.COLOR_RGB2GRAY)
    duo = LUT_GP[g]
    o = fr.astype(np.float32) * (1 / 255.0)
    return (o * np.array([0.50, 0.56, 0.66], np.float32) + duo * 0.50) * osc


# ---------------------------------------------------------------- posproceso
def _post():
    yy = np.arange(H)
    sl = np.where(yy % 3 == 2, 0.84, 1.0).astype(np.float32)
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xs - W / 2) / (W / 2)) ** 2 + ((ys - H / 2) / (H / 2)) ** 2)
    vig = np.clip(1.04 - 0.24 * d ** 2.4, 0.62, 1.0).astype(np.float32)
    return (sl[:, None] * vig)[..., None]


def _fondo():
    ys, xs = np.mgrid[0:H, 0:W].astype(np.float32)
    d = np.sqrt(((xs - W / 2) / W) ** 2 + ((ys - H / 2) / H) ** 2)
    base = c(NOCHE)[None, None, :] + (np.clip(1 - d * 1.6, 0, 1) ** 2)[..., None] * c((26, 18, 70))
    # puntos de rejilla finos
    dots = ((xs % 32 < 1.5) & (ys % 32 < 1.5)).astype(np.float32)[..., None] * c((40, 70, 120)) * 0.6
    return (base + dots).astype(np.float32)


POST = _post()
FONDO = _fondo()


def glitch_cuadro(F, k, seed):
    if k <= 0.01:
        return
    rng = np.random.default_rng(seed)
    for _ in range(int(3 + 14 * k)):
        y0 = int(rng.integers(0, H))
        hh = int(rng.integers(5, 24 + int(80 * k)))
        F[y0:y0 + hh] = np.roll(F[y0:y0 + hh], int(rng.normal() * 70 * k), axis=1)
    sh = int(round(12 * k))
    if sh:
        F[..., 0] = np.roll(F[..., 0], -sh, 1)
        F[..., 2] = np.roll(F[..., 2], sh, 1)
    for _ in range(int(6 * k)):
        y = int(rng.integers(0, H))
        F[y:y + 2] += 0.3 * k * c(CIAN)


def banda(F, u):
    """Proyector que se enciende/apaga: solo se ve una franja central de alto H*u."""
    if u >= 1:
        return
    yy = np.arange(H, dtype=np.float32)
    bh = max(2.0, H * u)
    m = np.clip((bh / 2 - np.abs(yy - H / 2)) / 6.0, 0, 1)[:, None, None]
    F *= m
    y0, y1 = int(H / 2 - bh / 2), int(H / 2 + bh / 2)
    for y in (y0, y1 - 2):
        F[max(0, y):max(0, y) + 2] += c(BLANCO) * 0.9


def marca_esquina(n=3, nombre="HOLOGRAMA ARCANO"):
    txt = f"ESTILO {n} · {nombre}"
    f = fuente(24, "SemiBold")
    tw = int(sum(f.getlength(ch) for ch in txt) + 3 * (len(txt) - 1))
    w, h = tw + 74, 44
    im = Image.new("RGBA", (w + 8, h + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([4, 4, 4 + w, 4 + h], radius=8, fill=(4, 8, 26, 130), outline=(90, 225, 255, 110), width=1)
    cx, cy = 4 + 26, 4 + h / 2
    d.polygon(hexagono(cx, cy, 11), outline=(90, 225, 255, 230))
    d.polygon(hexagono(cx, cy, 5, rot=0), fill=(200, 160, 255, 230))
    x = 4 + 50
    for ch in txt:
        d.text((x, 4 + 9), ch, font=f, fill=(185, 238, 255, 225))
        x += f.getlength(ch) + 3
    return de_pil(im)


# ---------------------------------------------------------------- guion de 30 s
P = lambda n: os.path.join(SRC, "pegatinas", n)


class Video:
    def __init__(s):
        s.mapa = mapa_ruta(
            os.path.join(SRC, "mapas", "ungoro_norte.jpg"),
            [dict(x=43.6, y=23.0, nombre="REFUGIO DE LOS MARISCALES", sub="GRYFE · PUNTO DE VUELO",
                  foto=P("refugio_mariscales.png")),
             dict(x=47.3, y=10.8, nombre="BANCAL DEL CREADOR", foto=P("bancal_creador.png"))],
            zona="CRÁTER DE UN'GORO", zona_sub="ZONA · KALIMDOR", cam_fin=(712, 230), zoom_fin=2.75,
            rotulo_final="BANCAL DEL CREADOR · 58-60")
        s.ficha = ficha("N.º 15 · SIN LOS 60 CRISTALES",
                        [(P("o_cristal_rojo.png"), "×15", (255, 95, 95), 15),
                         (P("o_cristal_amarillo.png"), "×15", (255, 214, 80), 15),
                         (P("o_cristal_azul.png"), "×15", (120, 150, 255), 15),
                         (P("o_cristal_verde.png"), "×15", (110, 255, 120), 15)])
        s.tarjeta = tarjeta(P("bancal_creador.png"), "JEFA FINAL: NANAYA", "cambia de elemento cada 25 %",
                            pie_foto="BANCAL DEL CREADOR")
        s.rotulo = rotulo("Sin cristales: solo 5 jefes", sello="5")
        med = os.path.join(SRC, "medios")
        s.cA = Clip(os.path.join(med, "scene-089.mp4"), 0.4)
        s.cB = Clip(os.path.join(med, "scene-091.mp4"), 1.2)
        s.cC = Clip(os.path.join(med, "scene-093.mp4"), 0.5)
        s.marca = marca_esquina()

    def fondo_gp(s, ctx, t):
        if t < 16.5:
            fr = s.cA.cuadro(int(round((t - 11.0) * FPS)))
        elif t < 21.0:
            fr = s.cB.cuadro(int(round((t - 16.5) * FPS)))
        else:
            fr = s.cC.cuadro(int(round((t - 21.0) * FPS)))
        img = tratar(fr)
        ctx.en(0, lambda F: F.__iadd__(img))
        # retícula HUD tenue + círculo rúnico lento en la esquina inferior derecha
        runa(ctx.luz, 300, W - 150, H - 120, t * 6, VIOLETA, 0.10, seed=71, estilo=1)

    def cuadro(s, t):
        ctx = Ctx(t)
        if t < 11.0:
            s.mapa.dibujar(ctx, t)
        else:
            s.fondo_gp(ctx, t)
            if t < 21.0:
                s.ficha.dibujar(ctx, t - 11.0)
            else:
                s.tarjeta.dibujar(ctx, t - 21.0)
                s.rotulo.dibujar(ctx, t - 21.0)
        F = ctx.componer()
        F *= POST
        # transiciones
        if 10.62 <= t < 11.0:
            banda(F, 1 - eio(seg(t, 10.8, 11.0)))
        if 11.0 <= t < 11.3:
            banda(F, eio(seg(t, 11.0, 11.28)))
        k = 0.0
        for (tc, dur, kk) in ((11.0, 0.35, 1.0), (16.5, 0.18, 0.55), (21.0, 0.35, 0.9)):
            if abs(t - tc) < dur:
                k = max(k, kk * (1 - abs(t - tc) / dur))
        for tm in (2.9, 6.1, 9.4, 13.8, 18.4, 24.6, 27.2):
            if 0 <= t - tm < 0.1:
                k = max(k, 0.22)
        if t > 29.35:
            k = max(k, seg(t, 29.35, 29.8))
        glitch_cuadro(F, k, int(t * 1000))
        if t > 21.0:
            pass
        F *= eo(seg(t, 0, 0.35)) * (1 - eio(seg(t, 29.55, 30.0)))
        pegar(F, s.marca, 26, 22, 1.0 * (1 - seg(t, 29.7, 30.0)))
        return (np.clip(F, 0, 1) * 255 + 0.5).astype(np.uint8)

    def cerrar(s):
        for cc in (s.cA, s.cB, s.cC):
            cc.cerrar()


# ---------------------------------------------------------------- salida
def render():
    v = Video()
    cmd = [FF, "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
           "-ss", "0", "-t", f"{DUR}", "-i", os.path.join(SRC, "audio", "wow", "nlXOcybLHxc.wav"),
           "-filter_complex", "[1:a]volume=-18dB,afade=t=in:st=0:d=1.5,afade=t=out:st=27.3:d=2.7[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p",
           "-threads", "4", "-c:a", "aac", "-b:a", "192k", "-t", f"{DUR}", "-movflags", "+faststart", SALIDA]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    import time
    t0 = time.time()
    for i in range(NF):
        p.stdin.write(v.cuadro(i / FPS).tobytes())
        if i % 60 == 0:
            print(f"cuadro {i}/{NF}  {time.time() - t0:.0f}s", flush=True)
    p.stdin.close()
    p.wait()
    v.cerrar()
    print("listo:", SALIDA)


def hoja():
    tiempos = [1.25 + 2.5 * i for i in range(12)]
    tw, th = 640, 360
    lienzo = Image.new("RGB", (tw * 4, th * 3), (0, 0, 0))
    d = ImageDraw.Draw(lienzo)
    for n, t in enumerate(tiempos):
        b = subprocess.run([FF, "-v", "error", "-ss", f"{t:.3f}", "-i", SALIDA, "-frames:v", "1", "-vf", f"scale={tw}:{th}",
                            "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True).stdout
        im = Image.frombytes("RGB", (tw, th), b)
        x, y = (n % 4) * tw, (n // 4) * th
        lienzo.paste(im, (x, y))
        d.rectangle([x, y + th - 26, x + 74, y + th], fill=(0, 0, 0))
        d.text((x + 6, y + th - 24), f"{t:5.2f}s", font=fuente(18, "SemiBold"), fill=(255, 255, 255))
    lienzo.save(os.path.join(AQUI, "hoja.jpg"), quality=88)
    print("hoja:", os.path.join(AQUI, "hoja.jpg"))


if __name__ == "__main__":
    if "--cuadros" in sys.argv:
        ts = [float(x) for x in sys.argv[sys.argv.index("--cuadros") + 1].split(",")]
        v = Video()
        for t in ts:
            Image.fromarray(v.cuadro(t)).save(os.path.join(AQUI, f"_prev_{t:05.2f}.jpg"), quality=90)
        v.cerrar()
    elif "--hoja" in sys.argv:
        hoja()
    else:
        render()
        hoja()
