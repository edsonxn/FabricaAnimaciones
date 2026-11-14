# -*- coding: utf-8 -*-
"""ESTILO «SCRAPBOOK COQUETTE» (canal de Amaya, 10-nov-2026) — kit por código.
Calco de las plantillas que eligió Amaya (canales/referencias/amaya/): vichy rosa/crema y rayas pastel, letras recortadas de
revista que caen una por una, papel rasgado y recorte de periódico en las esquinas, stickers de productos DIBUJADOS (Flow) con
borde blanco y sombra, sellos de goma «¡SÍ PÍDELO!» / «NI SE TE OCURRA», etiqueta de precio $/$$/$$$, cinta washi con el nombre,
notitas a mano, barras de color de TV como transición, «SUSCRÍBETE» en contorno con cursor y pantalla final.
Todo trabaja sobre float32 HxWx3 en 0..1 (RGB). Las piezas RGBA son float32 HxWx4. Doc: docs/estilo_scrapbook_coquette.md"""
import math
import os
from functools import lru_cache

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1920, 1080
FUENTES = r"C:\Windows\Fonts"
POPPINS = os.path.join(os.path.dirname(__file__), "tactica3d", "fuentes")


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


ROSA = hexrgb("e58fae")
ROSA_FUERTE = hexrgb("d94f86")
MAGENTA = hexrgb("b8336a")
ROSA_CLARO = hexrgb("f8cfdc")
CREMA = hexrgb("fbf1e6")
CIRUELA = hexrgb("5a2a3c")
VERDE = hexrgb("2f9a5c")
ROJO = hexrgb("d6334a")
CAFE = hexrgb("4a2f24")


def clamp(x, a=0.0, b=1.0):
    return a if x < a else b if x > b else x


def pr(t, a, b):
    return clamp((t - a) / max(1e-6, b - a))


def suave(u):
    u = clamp(u)
    return u * u * (3 - 2 * u)


def e_out(u):
    u = clamp(u)
    return 1 - (1 - u) ** 3


def e_back(u, s=1.9):
    u = clamp(u) - 1
    return 1 + u * u * ((s + 1) * u + s)


def rebote(t, t0, d=0.5):
    """0→1 con sobrepaso (pop de sticker)."""
    return e_back(pr(t, t0, t0 + d))


def fuente(nombre, px):
    ruta = os.path.join(POPPINS, nombre) if nombre.startswith("Poppins") else os.path.join(FUENTES, nombre)
    return ImageFont.truetype(ruta, int(px))


# ------------------------------------------------------------------ fondos
@lru_cache(maxsize=4)
def _vichy(celda=48, linea=None, base=CREMA, col=ROSA, alfa=0.62, sem=1):
    linea = linea or celda // 2
    Hh, Ww = H + 4 * celda, W + 4 * celda
    yy, xx = np.mgrid[0:Hh, 0:Ww]
    fila = ((yy // linea) % 2 == 0).astype(np.float32)
    colu = ((xx // linea) % 2 == 0).astype(np.float32)
    a = np.clip(fila * alfa + colu * alfa - fila * colu * alfa * 0.25, 0, 1)[..., None]
    im = np.asarray(base, np.float32) * (1 - a) + np.asarray(col, np.float32) * a
    rg = np.random.default_rng(sem)
    tej = cv2.GaussianBlur(rg.random((Hh, Ww)).astype(np.float32), (0, 0), 0.8)
    im *= (0.95 + 0.07 * tej)[..., None]
    return np.clip(im, 0, 1).astype(np.float32)


@lru_cache(maxsize=4)
def _rayas(ancho=66, c1=hexrgb("f9e3ea"), c2=hexrgb("f4d4de"), sem=2):
    Ww = W + 4 * ancho
    xx = np.arange(Ww)
    m = ((xx // ancho) % 2).astype(np.float32)
    fila = np.asarray(c1, np.float32)[None, :] * (1 - m[:, None]) + np.asarray(c2, np.float32)[None, :] * m[:, None]
    im = np.repeat(fila[None], H, 0)
    rg = np.random.default_rng(sem)
    g = cv2.GaussianBlur(rg.random((H, Ww)).astype(np.float32), (0, 0), 1.2)
    im *= (0.97 + 0.04 * g)[..., None]
    v = np.linspace(0, 1, H, dtype=np.float32)[:, None, None]
    im = im * (1.0 - 0.05 * v)
    return np.clip(im, 0, 1).astype(np.float32)


def fondo(tipo, t, vel=14.0):
    """'vichy' (rosa), 'vichy_amaya', 'vichy_rojo', 'rayas' o 'rayas_gris'; se desliza despacio en diagonal."""
    if tipo.startswith("vichy"):
        if tipo == "vichy_amaya":      # el de los videos de Amaya: rosa-rojo sobre crema amarillenta
            base = _vichy(base=hexrgb("fdf1d8"), col=hexrgb("d9707e"), alfa=0.5)
        else:
            base = _vichy(col=ROJO if tipo == "vichy_rojo" else ROSA, alfa=0.45 if tipo == "vichy_rojo" else 0.62)
        p = 96
        ox = int((t * vel) % p)
        oy = int((t * vel * 0.6) % p)
        return base[oy:oy + H, ox:ox + W].copy()
    gris = tipo == "rayas_gris"
    base = _rayas(c1=hexrgb("ece4e8") if gris else hexrgb("f9e3ea"), c2=hexrgb("dfd4da") if gris else hexrgb("f4d4de"))
    ox = int((t * vel) % 132)
    return base[:, ox:ox + W].copy()


# ------------------------------------------------------------------ composición
def _sombra(rgba, blur=9):
    a = rgba[..., 3]
    s = cv2.GaussianBlur(a, (0, 0), blur)
    return s


def pegar(im, rgba, cx, cy, esc=1.0, rot=0.0, alfa=1.0, sombra=0.28, sx=1.0, sy=1.0, ancla=(0.5, 0.5), som_off=(10, 14),
          tinte=None, gris=0.0):
    """Pega una pieza RGBA centrada (ancla) en (cx, cy) con escala, giro (grados) y sombra suave. Solo trabaja en su recuadro."""
    if alfa <= 0.003 or esc <= 0.01:
        return im
    h, w = rgba.shape[:2]
    ax, ay = ancla[0] * w, ancla[1] * h
    ex, ey = esc * sx, esc * sy
    c, s = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    M = np.array([[c * ex, -s * ey, 0], [s * ex, c * ey, 0]], np.float32)
    esq = np.array([[0, 0], [w, 0], [0, h], [w, h]], np.float32) - [ax, ay]
    p = esq @ M[:, :2].T
    pad = 40 if sombra else 4
    x0, y0 = int(math.floor(cx + p[:, 0].min())) - pad, int(math.floor(cy + p[:, 1].min())) - pad
    x1, y1 = int(math.ceil(cx + p[:, 0].max())) + pad, int(math.ceil(cy + p[:, 1].max())) + pad
    X0, Y0, X1, Y1 = max(0, x0), max(0, y0), min(W, x1), min(H, y1)
    if X1 <= X0 or Y1 <= Y0:
        return im
    M[:, 2] = [cx - x0 - (M[0, 0] * ax + M[0, 1] * ay), cy - y0 - (M[1, 0] * ax + M[1, 1] * ay)]
    bw, bh = x1 - x0, y1 - y0
    pieza = cv2.warpAffine(rgba, M, (bw, bh), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_CONSTANT, borderValue=(0, 0, 0, 0))
    sl = (slice(Y0 - y0, Y1 - y0), slice(X0 - x0, X1 - x0))
    roi = im[Y0:Y1, X0:X1]
    if sombra:
        sa = cv2.GaussianBlur(pieza[..., 3], (0, 0), 7 * max(0.6, esc))
        M2 = np.float32([[1, 0, som_off[0] * esc], [0, 1, som_off[1] * esc]])
        sa = cv2.warpAffine(sa, M2, (bw, bh))[sl] * sombra * alfa
        roi *= (1 - sa[..., None] * np.asarray([0.75, 0.82, 0.85], np.float32))
    col = pieza[..., :3][sl]
    if gris > 0:
        g = col.mean(-1, keepdims=True)
        col = col * (1 - gris) + g * gris
    if tinte is not None:
        col = col * (1 - tinte[1]) + np.asarray(tinte[0], np.float32) * tinte[1]
    a = pieza[..., 3][sl][..., None] * alfa
    im[Y0:Y1, X0:X1] = roi * (1 - a) + col * a
    return im


def a_rgba(pil):
    return (np.asarray(pil.convert("RGBA"), np.float32) / 255.0)


# ------------------------------------------------------------------ stickers de Flow
_STK = {}


def sticker(ruta, alto):
    """PNG RGBA recortado de Flow, a `alto` px (cacheado). Añade el contorno blanco de sticker si la pieza no lo trae."""
    k = (ruta, int(alto))
    if k not in _STK:
        pil = Image.open(ruta).convert("RGBA")
        f = alto / pil.height
        pil = pil.resize((max(1, int(pil.width * f)), int(alto)), Image.LANCZOS)
        a = np.asarray(pil, np.float32) / 255
        borde = cv2.dilate((a[..., 3] > 0.5).astype(np.uint8), cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (9, 9)))
        borde = cv2.GaussianBlur(borde.astype(np.float32), (0, 0), 1.0)
        pad = 8
        out = np.zeros((a.shape[0] + 2 * pad, a.shape[1] + 2 * pad, 4), np.float32)
        bb = np.pad(borde, pad)
        out[..., :3] = 1.0
        out[..., 3] = np.clip(bb, 0, 1)
        sub = out[pad:-pad, pad:-pad]
        al = a[..., 3:4]
        sub[..., :3] = sub[..., :3] * (1 - al) + a[..., :3] * al
        sub[..., 3:4] = np.maximum(sub[..., 3:4], al)
        _STK[k] = out
    return _STK[k]


# ------------------------------------------------------------------ texto
@lru_cache(maxsize=512)
def texto(txt, nombre="Poppins-ExtraBold.ttf", px=60, col=CIRUELA, contorno=0, col_contorno=(1, 1, 1), sombra=False):
    f = fuente(nombre, px)
    bb = f.getbbox(txt, stroke_width=contorno)
    w, h = bb[2] - bb[0] + 8 + contorno * 2, bb[3] - bb[1] + 8 + contorno * 2
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    c8 = tuple(int(v * 255) for v in col) + (255,)
    s8 = tuple(int(v * 255) for v in col_contorno) + (255,)
    d.text((4 - bb[0] + contorno, 4 - bb[1] + contorno), txt, font=f, fill=c8, stroke_width=contorno, stroke_fill=s8)
    return a_rgba(im)


@lru_cache(maxsize=64)
def contorno_texto(txt, nombre="Inkfree.ttf", px=150, col=ROSA_FUERTE, grosor=7):
    """Letras huecas (solo contorno), como el «SUBSCRIBE» de la plantilla."""
    f = fuente(nombre, px)
    bb = f.getbbox(txt, stroke_width=grosor)
    w, h = bb[2] - bb[0] + 20, bb[3] - bb[1] + 20
    a = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(a)
    d.text((10 - bb[0], 10 - bb[1]), txt, font=f, fill=255, stroke_width=grosor, stroke_fill=255)
    b = Image.new("L", (w, h), 0)
    ImageDraw.Draw(b).text((10 - bb[0], 10 - bb[1]), txt, font=f, fill=255)
    m = np.clip(np.asarray(a, np.float32) - np.asarray(b, np.float32) * 0.92, 0, 255) / 255
    out = np.zeros((h, w, 4), np.float32)
    out[..., :3] = col
    out[..., 3] = m
    return out


# ------------------------------------------------------------------ letras recortadas (nota de rescate)
SERIFS = ["georgiab.ttf", "BELLB.TTF", "timesbd.ttf", "cambriab.ttf", "GOUDYSTO.TTF", "BASKVILL.TTF", "BRITANIC.TTF", "ariblk.ttf",
          "georgiaz.ttf", "timesbi.ttf"]
# pastel variados (estilo de Amaya, ref3-5: lila, rosa, menta, amarillo y crema; letra pastel con filete más oscuro)
PAPELES = [("fdf6ec", "b48ad6"), ("fffaf2", "ef86ad"), ("fdf6ec", "6cc4a1"), ("fffaf2", "eab23c"), ("ffffff", "a98bd8"),
           ("f7c6d6", "ffffff"), ("dccbf2", "ffffff"), ("cdeee0", "e2689a"), ("fbeaa5", "9f78cf"), ("ec8db0", "ffffff"),
           ("fdf6ec", "e56f97"), ("e9f6ef", "a17fd3")]


def _osc(hx, k=0.68):
    r, g, b = (int(hx[i:i + 2], 16) for i in (0, 2, 4))
    return (int(r * k), int(g * k), int(b * k), 255)


@lru_cache(maxsize=1024)
def letra_recorte(ch, px, sem):
    rg = np.random.default_rng(sem)
    fondo_, tinta = PAPELES[rg.integers(len(PAPELES))]
    f = fuente(SERIFS[rg.integers(len(SERIFS))], px * rg.uniform(0.82, 1.05))
    sw = max(1, int(px / 30))
    bb = f.getbbox(ch, stroke_width=sw)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    pw, ph = int(tw + px * rg.uniform(0.22, 0.4)), int(max(th, px * 0.6) + px * rg.uniform(0.22, 0.42))
    im = Image.new("RGBA", (pw + 6, ph + 6), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    j = lambda: int(rg.integers(0, max(2, px // 14)))
    poly = [(3 + j(), 3 + j()), (pw + 3 - j(), 3 + j()), (pw + 3 - j(), ph + 3 - j()), (3 + j(), ph + 3 - j())]
    d.polygon(poly, fill="#" + fondo_)
    claro = tinta == "ffffff"
    patron = rg.integers(0, 5)
    if patron == 0 and not claro:      # puntitos
        for yy in range(6, ph, max(8, px // 5)):
            for xx in range(6 + (yy // 7) % 2 * 4, pw, max(8, px // 5)):
                d.ellipse((xx, yy, xx + 3, yy + 3), fill=(255, 255, 255, 70))
    elif patron == 1 and not claro:    # mini vichy
        s = max(5, px // 8)
        for xx in range(3, pw + 3, s * 2):
            d.rectangle((xx, 3, xx + s, ph + 3), fill=(255, 255, 255, 38))
        for yy in range(3, ph + 3, s * 2):
            d.rectangle((3, yy, pw + 3, yy + s), fill=(255, 255, 255, 38))
    filete = _osc(fondo_, 0.62) if claro else _osc(tinta)
    d.text(((pw + 6 - tw) / 2 - bb[0], (ph + 6 - th) / 2 - bb[1]), ch, font=f, fill="#" + tinta, stroke_width=sw,
           stroke_fill=filete)
    return a_rgba(im)


def rotulo_recorte(im, txt, cx, cy, px, t, t0, cada=0.06, sem=0, rot=0.0, salida=None, caer=True, alfa=1.0, esc=1.0):
    """Escribe `txt` con letras recortadas centradas en (cx, cy); cada letra cae y se asienta (como «Welcome to my vlog»)."""
    if t < t0:
        return im
    rg = np.random.default_rng(sem)
    piezas = []
    for i, ch in enumerate(txt):
        if ch == " ":
            piezas.append(None)
            continue
        piezas.append(letra_recorte(ch, int(px * esc), sem * 131 + i * 7 + (ord(ch) % 11)))
    anchos = [(int(px * esc * 0.42) if p is None else p.shape[1] - 4) for p in piezas]
    total = sum(anchos)
    x = cx - total / 2
    cr, sr = math.cos(math.radians(rot)), math.sin(math.radians(rot))
    for i, (p, aw) in enumerate(zip(piezas, anchos)):
        xc = x + aw / 2
        x += aw
        if p is None:
            continue
        ti = t0 + i * cada
        if t < ti:
            continue
        u = pr(t, ti, ti + 0.38)
        dy = (1 - e_out(u)) * -90 if caer else 0
        s = e_back(u, 2.2) if not caer else 1.0
        r = rot + rg.uniform(-9, 9) * (1 + (1 - e_out(u)) * 2)
        dx = xc - cx
        px_, py_ = cx + dx * cr, cy + dx * sr + rg.uniform(-px * esc * 0.08, px * esc * 0.08)
        a = alfa * clamp(u * 3)
        if salida is not None and t > salida:
            v = pr(t, salida + i * 0.02, salida + i * 0.02 + 0.3)
            py_ -= e_out(v) * 140
            a *= 1 - v
        pegar(im, p, px_, py_ + dy, esc=s, rot=r, alfa=a, sombra=0.25, som_off=(5, 7))
    return im


# ------------------------------------------------------------------ papeles
@lru_cache(maxsize=16)
def papel_rasgado(w, h, sem=0, rayado=True):
    rg = np.random.default_rng(sem)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = [(0, 0), (w, 0)]
    n = 40
    for i in range(n + 1):     # borde inferior rasgado
        x = w - i * w / n
        y = h * 0.78 + rg.uniform(-1, 1) * h * 0.08 + math.sin(i * 0.7) * h * 0.04
        pts.append((x, y))
    d.polygon(pts, fill=(250, 250, 247, 255))
    if rayado:
        for y in range(28, h, 26):
            d.line((0, y, w, y), fill=(160, 190, 220, 90), width=2)
        d.line((52, 0, 52, h), fill=(230, 120, 140, 90), width=2)
    pil = im.filter(ImageFilter.GaussianBlur(0.6))
    a = a_rgba(pil)
    # fibras del borde
    a[..., :3] *= 0.97 + 0.03 * rg.random((h, w, 1)).astype(np.float32)
    return a


_PALABRAS = ("moda temporada estilo tendencia nueva colección para los días de invierno con capas suaves y colores cálidos "
             "lana tejido elegante clásico abrigo sastre ciudad noche brillo encaje terciopelo perlas moños cuadros").split()


@lru_cache(maxsize=16)
def periodico(w, h, sem=0):
    rg = np.random.default_rng(sem)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    pts = []
    for i in range(30):
        pts.append((rg.uniform(-4, 4) + (0 if i < 15 else w), i % 15 * h / 14))
    poly = [(0, 0)] + [(w * 0.08 + rg.uniform(-6, 6), h * i / 20) for i in range(21)][::-1]
    poly = [(rg.uniform(0, 8) + w * 0.06 * math.sin(i), h * i / 20) for i in range(21)] + [(w, h), (w, 0)]
    d.polygon(poly, fill=(238, 234, 226, 255))
    f = fuente("times.ttf", 22)
    y = 12
    while y < h - 20:
        linea = " ".join(rg.choice(_PALABRAS, 9))
        d.text((w * 0.1, y), linea, font=f, fill=(40, 36, 34, 235))
        y += 27
    return a_rgba(im.filter(ImageFilter.GaussianBlur(0.4)))


@lru_cache(maxsize=8)
def triangulo(w, h, col=ROSA_FUERTE):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ImageDraw.Draw(im).polygon([(0, 0), (w, h * 0.2), (w * 0.15, h)], fill=tuple(int(c * 255) for c in col) + (255,))
    return a_rgba(im)


def esquinas(im, t, t0=-10, sem=0, lado="tl_br"):
    """Papel rasgado + triángulo rosa arriba a la izquierda y recorte de periódico abajo a la derecha (ref1)."""
    u = e_out(pr(t, t0, t0 + 0.6))
    if u <= 0:
        return im
    pegar(im, triangulo(230, 170), 330 - (1 - u) * 500, 185 - (1 - u) * 300, rot=-18, sombra=0.2)
    pegar(im, papel_rasgado(520, 300, sem), 190 - (1 - u) * 420, 92 - (1 - u) * 260, rot=-14 + math.sin(t * 0.6) * 0.6, sombra=0.22)
    pegar(im, periodico(430, 330, sem + 3), W - 150 + (1 - u) * 420, H - 110 + (1 - u) * 300, rot=-32, sombra=0.22)
    return im


# ------------------------------------------------------------------ sellos, etiqueta, cinta, notas
@lru_cache(maxsize=8)
def sello(tipo="si", px=78):
    txt, col = ("¡SÍ PÍDELO!", VERDE) if tipo == "si" else ("NI SE TE OCURRA", ROJO)
    f = fuente("ariblk.ttf", px)
    bb = f.getbbox(txt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    w, h = tw + 90, th + 80
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((6, 6, w - 6, h - 6), radius=22, outline=255, width=9)
    d.rounded_rectangle((20, 20, w - 20, h - 20), radius=14, outline=255, width=3)
    d.text(((w - tw) / 2 - bb[0], (h - th) / 2 - bb[1]), txt, font=f, fill=255)
    m = np.asarray(im, np.float32) / 255
    rg = np.random.default_rng(5 if tipo == "si" else 6)
    ruido = cv2.GaussianBlur(rg.random(m.shape).astype(np.float32), (0, 0), 2.2)
    m *= np.clip((ruido - 0.36) * 4.5, 0, 1) * 0.9 + 0.1
    out = np.zeros((h, w, 4), np.float32)
    out[..., :3] = col
    out[..., 3] = np.clip(m * 0.95, 0, 1)
    return out


def golpe_sello(im, tipo, cx, cy, t, t0, rot=-12, esc=1.0):
    """El sello cae de golpe (2,3x → 1x en 0,16 s) y deja un temblor de cámara que devuelve en `temblor(t, t0)`."""
    if t < t0:
        return im
    u = pr(t, t0, t0 + 0.16)
    s = esc * (2.3 - 1.3 * e_out(u))
    pegar(im, sello(tipo), cx, cy, esc=s, rot=rot, alfa=clamp(u * 2.5) * 0.93, sombra=0.0)
    return im


def temblor(t, t0, amp=14):
    if t < t0 + 0.14 or t > t0 + 0.5:
        return 0, 0
    k = pr(t, t0 + 0.14, t0 + 0.5)
    a = amp * (1 - k)
    return a * math.sin(t * 90), a * math.cos(t * 77)


@lru_cache(maxsize=8)
def etiqueta(nivel=1, px=70):
    w, h = 300, 150
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.polygon([(46, 8), (w - 8, 8), (w - 8, h - 8), (46, h - 8), (8, h / 2)], fill=(253, 246, 238, 255), outline=(217, 79, 134, 255))
    d.line([(46, 8), (w - 8, 8), (w - 8, h - 8), (46, h - 8), (8, h / 2), (46, 8)], fill=(217, 79, 134, 255), width=6)
    d.ellipse((30, h / 2 - 10, 50, h / 2 + 10), fill=(0, 0, 0, 0), outline=(217, 79, 134, 255), width=4)
    f = fuente("ariblk.ttf", px)
    x = 78
    for i in range(3):
        col = (217, 79, 134, 255) if i < nivel else (224, 205, 212, 255)
        d.text((x, h / 2 - px * 0.62), "$", font=f, fill=col)
        x += px * 0.66
    return a_rgba(im)


def cuelga_etiqueta(im, nivel, cx, cy, t, t0, esc=1.0):
    """Etiqueta de precio que entra columpiándose de un hilo."""
    if t < t0:
        return im
    u = pr(t, t0, t0 + 0.5)
    rot = 18 * math.exp(-(t - t0) * 2.2) * math.cos((t - t0) * 9) - 10
    y = cy - (1 - e_out(u)) * 260
    # hilo
    x0, y0 = int(cx - 40), int(y - 230)
    cv2.line(im, (x0, max(0, y0)), (int(cx - 90 * esc), int(y)), (0.55, 0.38, 0.30), 3, cv2.LINE_AA)
    pegar(im, etiqueta(nivel), cx, y, esc=esc * clamp(u * 3), rot=rot, ancla=(0.05, 0.5), sombra=0.25)
    return im


@lru_cache(maxsize=128)
def cinta(txt, px=54, col_cinta=ROSA_CLARO, col_txt=CIRUELA, sem=0):
    """Cinta washi semitransparente con puntitos y el nombre encima."""
    f = fuente("Poppins-ExtraBold.ttf", px)
    bb = f.getbbox(txt)
    tw, th = bb[2] - bb[0], bb[3] - bb[1]
    w, h = tw + 120, int(th + px * 0.9)
    rg = np.random.default_rng(sem)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    zig = lambda x0, s: [(x0 + s * rg.uniform(0, 14), y) for y in np.linspace(0, h, 9)]
    poly = zig(0, 1) + zig(w, -1)[::-1]
    c = tuple(int(v * 255) for v in col_cinta)
    d.polygon(poly, fill=c + (225,))
    for yy in range(8, h, 18):
        for xx in range(14 + (yy // 18) % 2 * 9, w - 10, 18):
            d.ellipse((xx, yy, xx + 4, yy + 4), fill=(255, 255, 255, 120))
    d.text(((w - tw) / 2 - bb[0], (h - th) / 2 - bb[1]), txt, font=f, fill=tuple(int(v * 255) for v in col_txt) + (255,))
    return a_rgba(im)


@lru_cache(maxsize=256)
def nota(txt, px=44, papel=(255, 248, 200), sem=0):
    """Notita adhesiva escrita a mano (Ink Free)."""
    f = fuente("Inkfree.ttf", px)
    lineas = txt.split("\n")
    bbs = [f.getbbox(l) for l in lineas]
    tw = max(b[2] - b[0] for b in bbs)
    lh = int(px * 1.15)
    w, h = tw + 60, lh * len(lineas) + 50
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rectangle((0, 0, w, h), fill=papel + (255,))
    d.rectangle((0, 0, w, 16), fill=tuple(max(0, c - 22) for c in papel) + (255,))
    for i, (l, b) in enumerate(zip(lineas, bbs)):
        d.text(((w - (b[2] - b[0])) / 2 - b[0], 28 + i * lh - b[1] * 0.2), l, font=f, fill=(70, 40, 50, 255))
    return a_rgba(im)


def pega_nota(im, txt, cx, cy, t, t0, t1=None, rot=None, sem=0, papel=(255, 248, 200), px=44):
    if t < t0 or (t1 is not None and t > t1 + 0.3):
        return im
    rg = np.random.default_rng(sem)
    rot = rg.uniform(-7, 7) if rot is None else rot
    s = rebote(t, t0, 0.4)
    a = 1.0 if t1 is None else 1 - pr(t, t1, t1 + 0.3)
    pegar(im, nota(txt, px, papel, sem), cx, cy, esc=s, rot=rot + math.sin(t * 1.3 + sem) * 1.2, alfa=a, sombra=0.25)
    return im


# ------------------------------------------------------------------ adornos dibujados
@lru_cache(maxsize=16)
def destello(r=40, col=(1, 1, 1)):
    n = 2 * r + 1
    yy, xx = np.mgrid[-r:r + 1, -r:r + 1].astype(np.float32) / r
    m = np.clip(1 - (np.abs(xx) ** 0.5 + np.abs(yy) ** 0.5), 0, 1) ** 1.3
    out = np.zeros((n, n, 4), np.float32)
    out[..., :3] = col
    out[..., 3] = np.clip(m * 2.2, 0, 1)
    return out


def destellos(im, t, pts, s=1.0, col=(1, 1, 1)):
    for i, (x, y) in enumerate(pts):
        k = 0.5 + 0.5 * math.sin(t * 3.1 + i * 1.7)
        pegar(im, destello(36, col), x, y, esc=s * (0.45 + 0.65 * k), rot=t * 30 + i * 20, alfa=0.85 * k, sombra=0)
    return im


@lru_cache(maxsize=8)
def corazon(r=60, col=ROSA_FUERTE):
    n = int(2.4 * r)
    yy, xx = np.mgrid[0:n, 0:n].astype(np.float32)
    x = (xx - n / 2) / r
    y = -(yy - n * 0.45) / r
    m = ((x * x + y * y - 1) ** 3 - x * x * y ** 3 <= 0).astype(np.float32)
    m = cv2.GaussianBlur(m, (0, 0), 1.0)
    out = np.zeros((n, n, 4), np.float32)
    out[..., :3] = col
    out[..., 3] = m
    return out


@lru_cache(maxsize=4)
def cursor(alto=70):
    w = int(alto * 0.72)
    im = Image.new("RGBA", (w + 8, alto + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    p = [(4, 4), (4, alto * 0.82), (alto * 0.25, alto * 0.64), (alto * 0.42, alto), (alto * 0.55, alto * 0.94),
         (alto * 0.39, alto * 0.6), (w, alto * 0.6)]
    d.polygon(p, fill=(255, 255, 255, 255), outline=(20, 20, 20, 255))
    d.line(p + [p[0]], fill=(20, 20, 20, 255), width=3)
    return a_rgba(im)


# ------------------------------------------------------------------ transiciones
@lru_cache(maxsize=1)
def _barras():
    cols = ["e8e2e8", "f0d000", "2ff0c8", "10f010", "b000c0", "a00000", "0010c8"]
    im = np.zeros((H, W, 3), np.float32)
    bw = W / 7
    for i, c in enumerate(cols):
        im[:int(H * 0.66), int(i * bw):int((i + 1) * bw)] = hexrgb(c)
    sub = ["0010c8", "000000", "b000c0", "000000", "2ff0c8", "000000", "e8e2e8"]
    for i, c in enumerate(sub):
        im[int(H * 0.66):int(H * 0.75), int(i * bw):int((i + 1) * bw)] = hexrgb(c)
    im[int(H * 0.75):, :] = 0.02
    im[int(H * 0.75):, int(bw * 0.7):int(bw * 1.7)] = hexrgb("e8e2e8")
    im[int(H * 0.75):, int(bw * 1.7):int(bw * 2.8)] = hexrgb("4a0080")
    return im


def tv(A, B, u, t):
    """Barras de color con glitch entre A y B (ref1). u 0..1."""
    rg = np.random.default_rng(int(t * 60))
    if u < 0.18 or u > 0.82:
        base = A if u < 0.5 else B
        k = 1 - abs(u - (0.09 if u < 0.5 else 0.91)) / 0.09
        out = base.copy()
    else:
        out = _barras().copy()
        k = 1.0
    # glitch: tiras horizontales desplazadas + ruido
    for _ in range(int(6 + 10 * k)):
        y = int(rg.integers(0, H - 40))
        h = int(rg.integers(6, 60))
        out[y:y + h] = np.roll(out[y:y + h], int(rg.integers(-120, 120)), axis=1)
    out += (rg.random((H // 4, W // 4, 1)).astype(np.float32).repeat(4, 0).repeat(4, 1) - 0.5) * 0.25 * k
    return np.clip(out, 0, 1)


_RAS = {}


def rasgado(A, B, u, sem=0, horizontal=True):
    """B entra sobre A como una hoja con el borde rasgado que barre de izquierda a derecha (con sombrita en el borde)."""
    if u <= 0:
        return A
    if u >= 1:
        return B
    if sem not in _RAS:
        rg = np.random.default_rng(sem)
        r = np.cumsum(rg.normal(0, 4.0, H)).astype(np.float32)
        r = r - r.mean()
        r += np.sin(np.arange(H) / 23.0) * 18 + rg.normal(0, 3, H)
        _RAS[sem] = np.clip(r, -70, 70)
    borde = _RAS[sem]
    x = suave(u) * (W + 260) - 130 + borde
    xx = np.arange(W, dtype=np.float32)[None, :]
    m = (xx < x[:, None]).astype(np.float32)
    m = cv2.GaussianBlur(m, (0, 0), 0.8)[..., None]
    sombra = np.exp(-np.clip(xx - x[:, None], 0, None) / 22.0) * (xx >= x[:, None]) * 0.35
    out = A * (1 - sombra[..., None]) * (1 - m) + B * m
    blanco = ((xx < x[:, None]) & (xx > x[:, None] - 7)).astype(np.float32)[..., None]
    return out * (1 - blanco * 0.85) + blanco * 0.85


def acabado(im, t):
    """Grano de papel muy fino + viñeta suave (todas las escenas)."""
    rg = np.random.default_rng(int(t * 30) % 8)
    if not hasattr(acabado, "v"):
        yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
        d = ((xx - W / 2) / W) ** 2 + ((yy - H / 2) / H) ** 2
        acabado.v = (1 - np.clip(d * 0.55, 0, 0.18))[..., None].astype(np.float32)
        acabado.g = [(np.random.default_rng(k).random((H // 2, W // 2, 1)).astype(np.float32) - 0.5).repeat(2, 0).repeat(2, 1)
                     for k in range(8)]
    im = im * acabado.v + acabado.g[int(t * 12) % 8] * 0.022
    return np.clip(im, 0, 1)
