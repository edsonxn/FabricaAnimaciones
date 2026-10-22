# -*- coding: utf-8 -*-
"""MOTION GRAPHICS con PIEL PINTADA EN FLOW (Crónicas del gaming, aventura de fantasía de N64; primer uso `zelda_oot`, 22-oct-2026).
Nace de la crítica del usuario a los paneles dibujados por código de `mg_gaming` («esos cuadros de texto se ven muy poco
trabajados… apóyate de Flow») y, el mismo día, «hay mucho texto que se sale de la caja y elementos que no están del todo
acomodados»: Flow PINTA las piezas y este módulo las escala sin deformar esquinas (9-slice) y coloca TODO dentro del ÁREA
INTERIOR medida de cada pieza (`INTERIOR`, píxeles de la pieza): el texto se ajusta solo (tamaño y saltos) con `caja()`, nunca
pisa el marco; los elementos de un tablero se reparten en el hueco que queda bajo el título, sin montarse.
Tipografía: Engravers MT (títulos grabados) + Book Antiqua negrita (texto). CERO cifras ni nombres inventados.

Piezas: videos/<v>/ui/*.png (prompts en videos/<v>/prompts.json; recorte con nucleo/recortar_ui.py). En efectos.py:
    import mg_zelda as Z
    Z.usar(os.path.join(_AQUI, "ui"))
  puesto(num, titulo)                     medallón con el número + cinta de terciopelo con el título
  ficha(titulo, texto, tipo, piel)        tablilla de piedra (piel="piedra") o pergamino (piel="pergamino"); *x* = resaltado
  linea_tiempo(hitos, titulo)             cuerda dorada sobre el tablero; un hito por marca (medallón pequeño + cifra)
  ocarina(canciones, titulo)              pergamino con pentagrama a tinta; los 5 botones reales; cada marca, una canción
  paradoja(pasos, titulo)                 bucle ovalado con 4 letreros de madera, una nota que gira y el sello de cera «NADIE»
  versiones(cols, filas, titulo)          cartuchos pintados como cabecera; filas que se rellenan; lo que cambió late
  tres_lineas(raiz, ramas, titulo)        cinta raíz y tres ramas doradas con letreros de juegos; la rama `caida` en rojo
Probar SIEMPRE con una hoja de cuadros antes de `fx` (texto largo, cifras de varias cifras, títulos largos).
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import mg_gaming as G

ORO, ORO_OSC, CREMA, TINTA, AZUL_N, ROJO = ((246, 206, 110), (150, 105, 35), (250, 240, 215), (58, 34, 16),
                                            (18, 28, 70), (205, 45, 40))
NEGRO = (8, 10, 22)
UI = {}
_fc = {}
# 9-slice: márgenes (izq, arriba, der, abajo) en píxeles de la pieza = grosor del marco medido (22-oct) + columna central fija
CORTES = {"tablero": ((140, 140, 136, 100), (520, 690)), "tablilla": ((100, 98, 100, 100), (560, 655)),
          "pergamino": ((210, 120, 206, 106), None), "letrero": ((92, 88, 94, 96), None), "cinta": ((245, 0, 242, 0), None)}
# área útil dentro de la pieza SIN estirar (fracciones): para piezas que se usan a escala uniforme
INTERIOR = {"cinta": (245 / 1327, 70 / 316, 1 - 242 / 1327, 1 - 70 / 316),
            "cartucho": (300 / 1124, 160 / 713, 1 - 292 / 1124, 1 - 268 / 713),
            "medallon": (.30, .30, .70, .68), "sello": (.22, .22, .78, .78)}
PAD = 22                                                    # aire entre el marco y el texto


def usar(carpeta):
    """Carga las piezas PNG (tablero, tablilla, pergamino, medallon, cinta, sello, cartucho, letrero, boton_1..5)."""
    for f in os.listdir(carpeta):
        if f.endswith(".png") and not f.startswith("_"):
            UI[f[:-4]] = Image.open(os.path.join(carpeta, f)).convert("RGBA")


def fuente(estilo, tam):
    """«g» grabada (Engravers MT, títulos), «t» texto (Book Antiqua negrita), «i» cursiva."""
    k = (estilo, int(tam))
    if k not in _fc:
        _fc[k] = ImageFont.truetype({"g": "C:/Windows/Fonts/ENGR.TTF", "t": "C:/Windows/Fonts/ANTQUAB.TTF",
                                     "i": "C:/Windows/Fonts/ANTQUABI.TTF"}[estilo], int(tam))
    return _fc[k]


_eo, _reb, _escala, _bgra = G._eo, G._reb, G._escala, G._bgra
_D = ImageDraw.Draw(Image.new("RGBA", (8, 8)))


def _ancho(s, f):
    return _D.textlength(s.replace("*", ""), font=f)


def _txt(d, xy, s, f, color, ancla="la", alfa=255, borde=3, color_borde=NEGRO, sombra=True):
    s = s.replace("·", "/")
    a = int(max(0, min(255, alfa)))
    if a <= 0:
        return
    if sombra:
        d.text((xy[0] + 2, xy[1] + 4), s, font=f, fill=(0, 0, 0, int(a * .5)), anchor=ancla, stroke_width=borde,
               stroke_fill=(0, 0, 0, int(a * .5)))
    d.text(xy, s, font=f, fill=tuple(color) + (a,), anchor=ancla, stroke_width=borde, stroke_fill=tuple(color_borde) + (a,))


def ajustar(s, estilo, tam, ancho, minimo=14):
    """Fuente más grande (≤ tam) con la que `s` cabe en una línea de `ancho`."""
    while tam > minimo and _ancho(s, fuente(estilo, tam)) > ancho:
        tam -= 1
    return fuente(estilo, tam)


def _partir(s, f, ancho):
    return G._partir(_D, s, f, ancho)


def caja(s, estilo, tam, ancho, alto, interlinea=1.28, minimo=14, max_lineas=6):
    """Reparte `s` en líneas que caben en ancho x alto bajando el tamaño si hace falta. -> (fuente, líneas, alto_línea)."""
    while True:
        f = fuente(estilo, tam)
        ls = _partir(s, f, ancho)
        lh = tam * interlinea
        if (len(ls) * lh <= alto and len(ls) <= max_lineas and max(_ancho(x, f) for x in ls) <= ancho) or tam <= minimo:
            return f, ls, lh
        tam -= 1


def _bloque(d, x0, y0, x1, y1, ls, f, lh, color, alfa=255, borde=2, color_borde=NEGRO, resalte=None, entra=None, dt=0):
    """Dibuja las líneas centradas en la caja (x0..x1, y0..y1); *x* en `resalte`; `entra` = (t0, paso) línea a línea."""
    ytop = (y0 + y1) / 2 - lh * len(ls) / 2 + lh / 2
    for i, ln in enumerate(ls):
        a = alfa if entra is None else alfa * _eo((dt - entra[0] - entra[1] * i) / .35)
        x = (x0 + x1) / 2 - _ancho(ln, f) / 2
        for k, t in enumerate(ln.split("*")):
            if not t:
                continue
            _txt(d, (x, ytop + lh * i), t, f, (resalte if (k % 2 and resalte) else color), "lm", a, borde, color_borde)
            x += d.textlength(t, font=f)


def nueve(nombre, w, h, s=.5):
    """Escala la pieza a w x h sin deformar esquinas ni el adorno central (márgenes de CORTES, grosor x s)."""
    im = UI[nombre]
    W, H = im.size
    (l, t, r, b), col = CORTES[nombre]
    if t == 0 and b == 0:                                   # solo horizontal (cinta): alto proporcional
        s = h / H
    dl, dt_, dr, db = [max(1, int(v * s)) if v else 0 for v in (l, t, r, b)]
    w, h = int(w), int(h)
    out = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    xs, xd = [0, l, W - r, W], [0, dl, w - dr, w]
    if col:
        c0, c1 = col
        cw = int((c1 - c0) * s)
        mid = (w - cw) // 2
        xs, xd = [0, l, c0, c1, W - r, W], [0, dl, mid, mid + cw, w - dr, w]
    ys, yd = ([0, t, H - b, H], [0, dt_, h - db, h]) if (t or b) else ([0, H], [0, h])
    for i in range(len(xs) - 1):
        for j in range(len(ys) - 1):
            sx0, sx1, sy0, sy1 = xs[i], xs[i + 1], ys[j], ys[j + 1]
            dx0, dx1, dy0, dy1 = xd[i], xd[i + 1], yd[j], yd[j + 1]
            if sx1 <= sx0 or sy1 <= sy0 or dx1 <= dx0 or dy1 <= dy0:
                continue
            out.alpha_composite(im.crop((sx0, sy0, sx1, sy1)).resize((dx1 - dx0, dy1 - dy0), Image.LANCZOS), (dx0, dy0))
    return out


def interior(nombre, w, h, s=.5, pad=PAD):
    """Rectángulo útil (x0, y0, x1, y1) de una pieza escalada con nueve() o, si no está en CORTES, a escala uniforme."""
    if nombre in CORTES and nombre != "cinta":
        (l, t, r, b), _ = CORTES[nombre]
        return l * s + pad, t * s + pad, w - r * s - pad, h - b * s - pad
    fx0, fy0, fx1, fy1 = INTERIOR[nombre]
    return w * fx0 + pad, h * fy0, w * fx1 - pad, h * fy1


def pieza(nombre, w=None, h=None):
    im = UI[nombre]
    if w and not h:
        h = int(im.size[1] * w / im.size[0])
    if h and not w:
        w = int(im.size[0] * h / im.size[1])
    return im.resize((int(w), int(h)), Image.LANCZOS)


def brillo(im, u, ancho=.10, fuerza=.55):
    """Destello diagonal que barre la pieza de izquierda a derecha (u 0..1); solo donde hay pintura."""
    if not 0 < u < 1:
        return im
    a = np.array(im).astype(np.float32)
    H, W = a.shape[:2]
    yy, xx = np.mgrid[0:H, 0:W]
    pos = (-.3 + 1.6 * u) * (W + H * .5)
    m = np.exp(-(((xx + yy * .5) - pos) / (ancho * W)) ** 2) * fuerza * (a[..., 3] / 255.0)
    for c in range(3):
        a[..., c] = a[..., c] + (255 - a[..., c]) * m
    return Image.fromarray(a.clip(0, 255).astype(np.uint8))


def _sombra(im, dx=10, dy=16, rad=14, op=.55):
    M = rad * 2 + max(dx, dy)
    out = Image.new("RGBA", (im.size[0] + 2 * M, im.size[1] + 2 * M), (0, 0, 0, 0))
    a = np.array(im)[..., 3].astype(np.float32) * op
    s = Image.fromarray(a.astype(np.uint8)).filter(ImageFilter.GaussianBlur(rad))
    neg = Image.new("RGBA", s.size, (0, 0, 0, 255))
    neg.putalpha(s)
    out.alpha_composite(neg, (M + dx, M + dy))
    out.alpha_composite(im, (M, M))
    return out, M


def _alfa(p, k):
    if k >= 1:
        return p
    a = np.array(p)
    a[..., 3] = (a[..., 3] * max(0.0, k)).astype(np.uint8)
    return Image.fromarray(a)


# ------------------------------------------------------------------ rótulo de puesto
def puesto(num, titulo):
    """Medallón (cae girando con rebote, destello) con el número dentro de su disco + cinta de terciopelo que se
    despliega desde detrás; el título se ajusta al hueco azul de la cinta que el medallón no tapa."""
    R, ch = 260, 150
    escala_c = ch / UI["cinta"].size[1]
    fin_izq, fin_der = 245 * escala_c, 242 * escala_c       # colas + broche de la cinta
    tapa = R - 70                                            # lo que el medallón tapa de la cinta
    tit = titulo.upper()
    ft = ajustar(tit, "g", 60, 1100)
    tw = _ancho(tit, ft)
    cw = int(max(620, tapa + 30 + tw + 40 + fin_der))
    x_c = 70                                                 # la cinta nace detrás del medallón
    ancho, alto = x_c + cw + 10, R + 70
    cinta = nueve("cinta", cw, ch)
    tx0, tx1 = tapa + 30 - x_c + x_c, cw - fin_der - 20      # hueco libre en coordenadas de la cinta
    fs = fuente("g", 26)
    med = pieza("medallon", R, R)
    mx0, my0, mx1, my1 = interior("medallon", R, R, pad=0)
    fnum = ajustar(str(num), "t", 130, (mx1 - mx0) * 1.1)

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (ancho, alto), (0, 0, 0, 0))
        fl = 4 * math.sin(dt * 2.2)
        cy = alto / 2 + fl
        u = _eo((dt - .25) / .6)
        if u > 0:
            c = cinta.copy()
            d = ImageDraw.Draw(c)
            a_t = 255 * _eo((dt - .55) / .4)
            _txt(d, ((tx0 + tx1) / 2, ch / 2 - 14), "SECRETO NÚMERO " + str(num), fs, ORO, "mm", a_t, 2, NEGRO)
            _txt(d, ((tx0 + tx1) / 2, ch / 2 + 22), tit, ajustar(tit, "g", 46, tx1 - tx0), CREMA, "mm", a_t, 3, AZUL_N)
            c = brillo(c, (dt - .9) / .9, fuerza=.35)
            m = Image.new("L", c.size, 0)
            ImageDraw.Draw(m).rectangle((0, 0, int(cw * u), ch), fill=255)
            c.putalpha(Image.fromarray(np.minimum(np.array(c)[..., 3], np.array(m))))
            im.alpha_composite(c, (x_c, int(cy - ch / 2)))
        m2 = med.copy()
        _txt(ImageDraw.Draw(m2), ((mx0 + mx1) / 2, (my0 + my1) / 2 + 4), str(num), fnum, (255, 248, 225), "mm", 255, 5,
             (95, 55, 10))
        m2 = brillo(m2, (dt - .6) / .7)
        m2 = _escala(m2, _reb(dt / .55)).rotate(-25 * (1 - _eo(dt / .8)) + 3 * math.sin(dt * 1.6), Image.BICUBIC)
        im.alpha_composite(m2, (0, int(cy - R / 2)))
        return _bgra(im, min(1.0, (dur - dt) / .45))
    return fn


# ------------------------------------------------------------------ ficha
def ficha(titulo, texto, tipo=None, ancho=900, piel="piedra"):
    """Tablilla de piedra con marco de oro (piel="piedra") o pergamino con rodillos (piel="pergamino"). Título grabado,
    `tipo` en cursiva, separador, texto que entra línea a línea; todo ajustado al interior. *x* resaltado."""
    perg = piel == "pergamino"
    nom = "pergamino" if perg else "tablilla"
    s = .55
    (l, t, r, b), _ = CORTES[nom]
    in_w = ancho - (l + r) * s - 2 * PAD - (30 if perg else 0)
    ft = ajustar(titulo.upper(), "g", 42, in_w)
    fty = ajustar(tipo, "i", 28, in_w) if tipo else None
    fx, ls, lh = caja(texto, "t", 38, in_w, 10_000, max_lineas=8)
    cab = 52 + (38 if tipo else 0) + 30                      # título + tipo + separador
    h = int(t * s + PAD + cab + lh * len(ls) + PAD + b * s + 8)
    base = nueve(nom, ancho, h, s=s)
    x0, y0, x1, y1 = interior(nom, ancho, h, s=s)
    col_t, col_x, col_r, cb = ((120, 25, 20), TINTA, (165, 30, 25), (235, 220, 190)) if perg else (ORO, CREMA, ORO, NEGRO)
    bt = 0 if perg else 2

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        cx = ancho / 2
        y = y0 + 22
        _txt(d, (cx, y), titulo.upper(), ft, col_t, "mm", 255 * _eo((dt - .15) / .35), 0 if perg else 3, cb, not perg)
        y += 40
        if tipo:
            _txt(d, (cx, y), tipo, fty, (95, 72, 50) if perg else (175, 205, 255), "mm", 230 * _eo((dt - .25) / .35),
                 0 if perg else 2, cb, not perg)
            y += 38
        a_l = 255 * _eo((dt - .2) / .5)
        d.line([(x0 + 30, y), (x1 - 30, y)], fill=(col_t if perg else ORO_OSC) + (int(a_l * .8),), width=3)
        d.ellipse((cx - 7, y - 7, cx + 7, y + 7), fill=(col_t if perg else ORO) + (int(a_l),))
        _bloque(d, x0, y + 14, x1, y1, ls, fx, lh, col_x, 255, bt, cb, col_r, entra=(.35, .3), dt=dt)
        im = brillo(im, (dt - .1) / .9, fuerza=.4)
        im, _ = _sombra(im)
        return _bgra(_escala(im, _reb(dt / .45) * (1 + .005 * math.sin(dt * 2.6))), min(1.0, (dur - dt) / .35))
    return fn


def _tablero(w, h, titulo, dt, s=.62):
    """Tablero con el título grabado arriba; devuelve (imagen, draw, (x0, y0, x1, y1) del hueco libre bajo el título)."""
    im = nueve("tablero", w, h, s=s)
    x0, y0, x1, y1 = interior("tablero", w, h, s=s)
    d = ImageDraw.Draw(im)
    f = ajustar(titulo.upper(), "g", 44, x1 - x0 - 40)
    _txt(d, (w / 2, y0 + 20), titulo.upper(), f, ORO, "mm", 255 * _eo((dt - .15) / .4), 3, NEGRO)
    d.line([(w / 2 - 220, y0 + 52), (w / 2 + 220, y0 + 52)], fill=ORO_OSC + (int(200 * _eo((dt - .2) / .4)),), width=2)
    return im, d, (x0, y0 + 70, x1, y1)


def _fin(im, dt, dur):
    im = brillo(im, (dt - .05) / 1.0, fuerza=.32)
    im, _ = _sombra(im)
    return _bgra(_escala(im, .94 + .06 * _reb(dt / .5)), min(_eo(dt / .3), (dur - dt) / .4))


# ------------------------------------------------------------------ línea de tiempo / escalera
def linea_tiempo(hitos, titulo="Así se hizo", w=1720, h=520, rojo_ultimo=True):
    """hitos = [(cifra, texto)]; marca 0 = la cuerda dorada se tiende; marca k = el hito k-1 cae (medallón chico con
    rebote, cifra grabada encima, texto debajo). El último late (en rojo con `rojo_ultimo`)."""
    n = len(hitos)
    medc = pieza("medallon", 64, 64)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, d, (X0, Y0, X1, Y1) = _tablero(w, h, titulo, dt)
        paso = (X1 - X0) / n
        y = Y0 + (Y1 - Y0) * .42
        x0, x1 = X0 + paso / 2, X1 - paso / 2
        fa = ajustar(max((str(c) for c, _ in hitos), key=len), "t", 54, paso * .8)
        u = _eo((dt - mk[0]) / .9)
        if u > 0:
            xe = x0 + (x1 - x0) * u
            d.line([(x0, y + 3), (xe, y + 3)], fill=(20, 12, 4, 200), width=10)
            d.line([(x0, y), (xe, y)], fill=ORO + (255,), width=7)
            d.line([(x0, y - 2), (xe, y - 2)], fill=(255, 240, 190, 200), width=2)
        for i, (cifra, txt) in enumerate(hitos):
            x = x0 + paso * i
            v = (dt - mk[1 + i]) / .5
            if v <= 0:
                continue
            ult = i == n - 1
            col = ROJO if (ult and rojo_ultimo) else ORO
            r = 64 * _reb(v) * (1 + (.12 * math.sin(dt * 6) if ult else 0))
            im.alpha_composite(medc.resize((max(2, int(r)), max(2, int(r))), Image.LANCZOS), (int(x - r / 2), int(y - r / 2)))
            d = ImageDraw.Draw(im)
            dy = 22 * (1 - _reb(v))
            a = 255 * _eo(v)
            _txt(d, (x, y - 44 - dy), str(cifra), fa, col, "mb", a, 3, NEGRO)
            fx, ls, lh = caja(txt, "t", 30, paso * .9, (Y1 - y - 50), max_lineas=3)
            _bloque(d, x - paso * .45, y + 44 + dy, x + paso * .45, y + 44 + dy + lh * len(ls), ls, fx, lh, CREMA, a, 2)
        return _fin(im, dt, dur)
    return fn


# ------------------------------------------------------------------ ocarina
BOTON = {"^": "boton_1", "v": "boton_2", "<": "boton_3", ">": "boton_4", "A": "boton_5"}
NOTA_Y = {"A": 0, "v": 1, ">": 2, "<": 3, "^": 4}


def _boton(nombre, r):
    b = pieza(BOTON[nombre], r, r)
    if nombre == "A":
        _txt(ImageDraw.Draw(b), (r / 2, r / 2 + 2), "A", fuente("t", int(r * .5)), CREMA, "mm", 255, max(1, int(r / 30)),
             (10, 30, 90))
    return b


def ocarina(canciones, titulo="La ocarina: cinco notas", w=1640, h=660):
    """Pergamino con pentagrama a tinta; a la izquierda, los 5 botones reales del mando (entran uno a uno y se hunden
    cuando suenan). marca 0 = botones + pentagrama · marca k = la canción k-1 cae nota a nota y su nombre aparece debajo;
    la anterior se va hacia la izquierda. Todo dentro del papel (entre los rodillos)."""
    n = len(canciones)
    s = .7
    X0, Y0, X1, Y1 = interior("pergamino", w, h, s=s, pad=10)
    cache = {}

    def bt(b, r):
        k = (b, int(r))
        if k not in cache:
            cache[k] = _boton(b, max(4, int(r)))
        return cache[k]

    zona_b = (X0, X0 + 300)                                  # mando a la izquierda
    sx0, sx1 = zona_b[1] + 40, X1 - 20                       # pentagrama
    ft = ajustar(titulo.upper(), "g", 42, X1 - X0)
    fnom = ajustar(max((c[0].upper() for c in canciones), key=len), "g", 44, sx1 - sx0)
    fb = ajustar("Solo cinco botones libres", "i", 28, zona_b[1] - zona_b[0])

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im = nueve("pergamino", w, h, s=s)
        d = ImageDraw.Draw(im)
        _txt(d, ((X0 + X1) / 2, Y0 + 18), titulo.upper(), ft, (120, 25, 20), "mm", 255 * _eo((dt - .15) / .4), 0,
             sombra=False)
        bx, by = (zona_b[0] + zona_b[1]) / 2, Y0 + (Y1 - Y0) * .50
        lay = [("A", -88, 92), ("^", 36, -62), ("v", 36, 110), ("<", -36, 24), (">", 108, 24)]
        sonando = None
        for k in range(n):
            j = int((dt - mk[1 + k]) / .32)
            if 0 <= j < len(canciones[k][1]) and (k == n - 1 or dt < mk[2 + k]):
                sonando = canciones[k][1][j]
        for i, (b, ox, oy) in enumerate(lay):
            u = (dt - mk[0] - .14 * i) / .45
            if u <= 0:
                continue
            act = b == sonando
            r = (100 if b != "A" else 110) * _reb(u) * (.9 if act else 1)
            im.alpha_composite(bt(b, r), (int(bx - 20 + ox - r / 2), int(by + oy - r / 2 + (6 if act else 0))))
        d = ImageDraw.Draw(im)
        _txt(d, (bx, Y1 - 14), "Solo cinco botones libres", fb, TINTA, "mm", 230 * _eo((dt - mk[0] - .8) / .4), 0,
             sombra=False)
        paso = 50
        y0 = Y0 + 90
        ap = _eo((dt - mk[0]) / .6)
        for k in range(5):
            yy = y0 + k * paso
            d.line([(sx0, yy), (sx0 + (sx1 - sx0) * _eo((dt - mk[0] - .06 * k) / .8), yy)], fill=TINTA + (int(200 * ap),),
                   width=3)
        for k, (nom, notas) in enumerate(canciones):
            t0 = mk[1 + k]
            if dt < t0:
                continue
            sal = _eo((dt - mk[2 + k]) / .45) if k < n - 1 else 0
            if sal >= 1:
                continue
            dx = -(sx1 - sx0) * .35 * sal
            r = 76
            for j, b in enumerate(notas):
                v = (dt - t0 - .32 * j) / .35
                if v <= 0:
                    continue
                x = sx0 + r / 2 + 10 + j * (sx1 - sx0 - r - 20) / max(1, len(notas) - 1) + dx
                y = y0 + (4 - NOTA_Y[b]) * paso - 46 * (1 - _reb(v))
                im.alpha_composite(_alfa(bt(b, r), min(1, _eo(v)) * (1 - sal)), (int(x - r / 2), int(y - r / 2)))
            d = ImageDraw.Draw(im)
            _txt(d, ((sx0 + sx1) / 2 + dx, min(Y1 - 16, y0 + 4 * paso + 70)), nom.upper(), fnom, (120, 25, 20), "mm",
                 255 * (1 - sal) * _eo((dt - t0 - .2) / .4), 0, sombra=False)
        im = brillo(im, (dt - .05) / 1.0, fuerza=.25)
        im, _ = _sombra(im)
        return _bgra(_escala(im, .94 + .06 * _reb(dt / .5)), min(_eo(dt / .3), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ letrero de madera con texto ajustado
def letrero(txt, ancho=420, alto=150, tam=32, s=.3):
    im = nueve("letrero", ancho, alto, s=s)
    x0, y0, x1, y1 = interior("letrero", ancho, alto, s=s, pad=8)
    f, ls, lh = caja(txt, "t", tam, x1 - x0, y1 - y0, interlinea=1.15, max_lineas=2)
    _bloque(ImageDraw.Draw(im), x0, y0, x1, y1, ls, f, lh, CREMA, 255, 3, (40, 20, 6))
    return im


# ------------------------------------------------------------------ paradoja
def paradoja(pasos, titulo="La canción de la tormenta", w=1640, h=900, pregunta="¿QUIÉN LA COMPUSO?", sello="NADIE"):
    """Bucle ovalado de 4 letreros (arriba, derecha, abajo, izquierda) unidos por un camino dorado, todo dentro del hueco
    bajo el título; marcas 0..3 = entra cada paso; luego una nota brillante gira · marca 4 = la pregunta (centro, arriba) ·
    marca 5 = el sello de cera cae con la palabra (centro, abajo). Pregunta y sello no se tocan entre sí ni con el bucle."""
    LW, LH = 420, 150
    letreros = [letrero(p, LW, LH) for p in pasos]
    SL = 210
    sel = pieza("sello", SL, SL)
    sx0, sy0, sx1, sy1 = interior("sello", SL, SL, pad=0)
    _txt(ImageDraw.Draw(sel), ((sx0 + sx1) / 2, (sy0 + sy1) / 2 + 2), sello, ajustar(sello, "g", 46, sx1 - sx0),
         (255, 228, 210), "mm", 255, 3, (90, 10, 10))
    fnota = ImageFont.truetype("C:/Windows/Fonts/seguisym.ttf", 64)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 8
        im, d, (X0, Y0, X1, Y1) = _tablero(w, h, titulo, dt)
        cx, cy = (X0 + X1) / 2, (Y0 + Y1) / 2
        RX = (X1 - X0) / 2 - LW / 2 - 6
        RY = (Y1 - Y0) / 2 - LH / 2 - 4
        fq = ajustar(pregunta, "g", 40, 2 * RX - LW - 40)
        angs = [-90, 0, 90, 180]
        for i in range(4):
            t_ini = mk[i + 1] if i < 3 else mk[3] + .5
            u = _eo((dt - t_ini) / .8)
            if u <= 0:
                continue
            a0, a1 = angs[i] + 20, angs[i] + 20 + (90 - 40) * u
            d.arc((cx - RX, cy - RY + 4, cx + RX, cy + RY + 4), a0, a1, fill=(10, 6, 2, 200), width=12)
            d.arc((cx - RX, cy - RY, cx + RX, cy + RY), a0, a1, fill=ORO + (255,), width=8)
            if u > .95:
                t = math.radians(a1)
                px, py = cx + RX * math.cos(t), cy + RY * math.sin(t)
                tg = math.atan2(RY * math.cos(t), -RX * math.sin(t))
                d.polygon([(px + 26 * math.cos(tg), py + 26 * math.sin(tg)),
                           (px + 16 * math.cos(tg + 2.2), py + 16 * math.sin(tg + 2.2)),
                           (px + 16 * math.cos(tg - 2.2), py + 16 * math.sin(tg - 2.2))], fill=ORO + (255,))
        if dt > mk[3] + 1.2:
            v = ((dt - mk[3] - 1.2) / 3.2) % 1
            for k in range(8):
                tt = math.radians(-90 + 360 * v - 5 * (k + 1))
                ex, ey = cx + RX * math.cos(tt), cy + RY * math.sin(tt)
                rr = 13 - k
                d.ellipse((ex - rr, ey - rr, ex + rr, ey + rr), fill=(255, 235, 160, int(190 - 22 * k)))
            t = math.radians(-90 + 360 * v)
            _txt(d, (cx + RX * math.cos(t), cy + RY * math.sin(t)), "♪", fnota, (255, 245, 210), "mm", 255, 3, (90, 60, 10))
        for i, lt in enumerate(letreros):
            u = (dt - mk[i]) / .45
            if u <= 0:
                continue
            t = math.radians(angs[i])
            px, py = cx + RX * math.cos(t), cy + RY * math.sin(t)
            p = _escala(lt, _reb(u))
            im.alpha_composite(p, (int(px - p.size[0] / 2), int(py - p.size[1] / 2 + 3 * math.sin(dt * 2 + i))))
        d = ImageDraw.Draw(im)
        hueco_top, hueco_bot = cy - RY + LH / 2 + 14, cy + RY - LH / 2 - 14      # entre el letrero de arriba y el de abajo
        yq = hueco_top + 30
        q = (dt - mk[4]) / .45
        if q > 0:
            _txt(d, (cx, yq), pregunta, fq, CREMA, "mm", 255 * _eo(q), 3, NEGRO)
        s_ = (dt - mk[5]) / .32
        if s_ > 0:
            ys = (yq + 34 + hueco_bot) / 2
            p = sel.rotate(-8, Image.BICUBIC, expand=True)
            esc = min(1.0, (hueco_bot - yq - 40) / p.size[1])
            p = _escala(p, esc * (1.9 - .9 * _eo(s_)) * (1 + .03 * math.sin(dt * 6)))
            im.alpha_composite(p, (int(cx - p.size[0] / 2), int(ys - p.size[1] / 2)))
        return _fin(im, dt, dur)
    return fn


# ------------------------------------------------------------------ versiones del cartucho
def versiones(cols, filas, titulo="El juego que cambió en silencio", w=1700, h=760):
    """cols = ["1.0", ...]; filas = [(nombre, [(texto, color)])], color None/"rojo"/"verde"/"oro". marca 0 = los
    cartuchos pintados caen como cabecera (versión ajustada a su etiqueta) · marca k = la fila k-1 se rellena; lo que
    cambió late con halo. Cada texto se ajusta a su casilla."""
    COL = {None: CREMA, "rojo": (255, 105, 90), "verde": (120, 235, 150), "oro": ORO}
    nf = len(filas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (nf + 2)
        im, d, (X0, Y0, X1, Y1) = _tablero(w, h, titulo, dt)
        col_nom = (X1 - X0) * .30
        xc0 = X0 + col_nom
        cw = (X1 - xc0) / len(cols)
        alto_cab = min(150, (Y1 - Y0) * .36)
        fila_h = (Y1 - Y0 - alto_cab - 10) / nf
        cel_w, cel_h = cw * .86, min(64, fila_h * .7)
        fcel = ajustar(max((t for _, cs in filas for t, _c in cs), key=len), "g", 30, cel_w - 24)
        for j, c in enumerate(cols):
            u = (dt - mk[0] - .12 * j) / .45
            if u <= 0:
                continue
            p = pieza("cartucho", h=int(alto_cab - 6))
            if p.size[0] > cw * .92:
                p = pieza("cartucho", int(cw * .92))
            lx0, ly0, lx1, ly1 = interior("cartucho", *p.size, pad=6)
            _txt(ImageDraw.Draw(p), ((lx0 + lx1) / 2, (ly0 + ly1) / 2), c, ajustar(c, "t", 40, lx1 - lx0, 10), TINTA, "mm",
                 255, 0, sombra=False)
            p = _escala(p, _reb(u))
            im.alpha_composite(p, (int(xc0 + cw * (j + .5) - p.size[0] / 2),
                                   int(Y0 + alto_cab / 2 - p.size[1] / 2 + 3 * math.sin(dt * 2 + j))))
        d = ImageDraw.Draw(im)
        for i, (nom, celdas) in enumerate(filas):
            y = Y0 + alto_cab + 10 + fila_h * (i + .5)
            u = (dt - mk[1 + i]) / .4
            if u <= 0:
                continue
            d.line([(X0, y - fila_h / 2), (X1, y - fila_h / 2)], fill=ORO_OSC + (int(170 * _eo(u)),), width=2)
            fx, ls, lh = caja(nom, "t", 32, col_nom - 20, fila_h - 8, interlinea=1.15, max_lineas=2)
            for k, ln in enumerate(ls):
                _txt(d, (X0, y - lh * (len(ls) - 1) / 2 + lh * k), ln, fx, CREMA, "lm", 255 * _eo(u), 2)
            for j, (txt, col) in enumerate(celdas):
                v = (dt - mk[1 + i] - .3 - .28 * j) / .35
                if v <= 0:
                    continue
                x = xc0 + cw * (j + .5)
                c = COL[col]
                late = (1 + .05 * math.sin(dt * 6 + j)) if col in ("rojo", "verde") else 1
                bw, bh = cel_w * _reb(v) * late, cel_h
                if col in ("rojo", "verde"):
                    halo = Image.new("RGBA", im.size, (0, 0, 0, 0))
                    ImageDraw.Draw(halo).rounded_rectangle((x - bw / 2 - 6, y - bh / 2 - 6, x + bw / 2 + 6, y + bh / 2 + 6),
                                                           20, fill=c + (int(110 * _eo(v) * (.6 + .4 * math.sin(dt * 6))),))
                    im.alpha_composite(halo.filter(ImageFilter.GaussianBlur(10)))
                    d = ImageDraw.Draw(im)
                d.rounded_rectangle((x - bw / 2, y - bh / 2, x + bw / 2, y + bh / 2), 14, fill=(10, 14, 30, int(215 * _eo(v))),
                                    outline=ORO + (int(230 * _eo(v)),), width=3)
                _txt(d, (x, y + 2), txt, fcel, c, "mm", 255 * _eo(v), 2)
        return _fin(im, dt, dur)
    return fn


# ------------------------------------------------------------------ tres líneas temporales
def tres_lineas(raiz, ramas, titulo="Una historia, tres caminos", w=1720, h=820):
    """raiz = texto de la cinta de arriba; ramas = [(etiqueta, [juegos], caida)]. marca 0 = la cinta raíz entra ·
    marca k = nace la rama k-1 (camino dorado que baja y se curva hasta su columna), su etiqueta y sus juegos en
    letreros. `caida` = rama en rojo. Columnas, etiquetas y letreros ajustados al hueco bajo el título."""
    n = len(ramas)
    CH = 112
    cinta = nueve("cinta", 640, CH)
    ix0, iy0, ix1, iy1 = interior("cinta", 640, CH, pad=10)
    _txt(ImageDraw.Draw(cinta), ((ix0 + ix1) / 2, CH / 2 + 2), raiz, ajustar(raiz, "g", 38, ix1 - ix0), CREMA, "mm", 255, 3,
         AZUL_N)
    jue = {}

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, d, (X0, Y0, X1, Y1) = _tablero(w, h, titulo, dt)
        colw = (X1 - X0) / n
        rx, ry = w / 2, Y0 + CH / 2
        ty = ry + CH / 2 + 120
        LW = min(380, colw - 30)
        for k, (eti, juegos, caida) in enumerate(ramas):
            u = _eo((dt - mk[1 + k]) / .9)
            if u <= 0:
                continue
            col = (230, 70, 55) if caida else ORO
            tx = X0 + colw * (k + .5)
            pts = []
            for s in range(41):
                t = s / 40 * u
                pts.append(((1 - t) ** 2 * rx + 2 * (1 - t) * t * rx + t * t * tx,
                            (1 - t) ** 2 * (ry + CH / 2 - 10) + 2 * (1 - t) * t * (ry + CH / 2 + 80) + t * t * ty))
            d.line([(x, y + 4) for x, y in pts], fill=(10, 6, 2, 200), width=13, joint="curve")
            d.line(pts, fill=col + (255,), width=9, joint="curve")
            y_et = ty + 24
            if u > .9:
                d.ellipse((tx - 15, ty - 15, tx + 15, ty + 15), fill=col + (255,), outline=(30, 18, 6, 255), width=4)
                fx, ls, lh = caja(eti, "i", 32, colw - 40, 90, interlinea=1.15, max_lineas=2)
                _bloque(d, tx - colw / 2 + 20, y_et, tx + colw / 2 - 20, y_et + lh * len(ls), ls, fx, lh,
                        col if caida else CREMA, 255 * _eo((dt - mk[1 + k] - .7) / .4), 2)
            for j, jg in enumerate(juegos):
                v = (dt - mk[1 + k] - 1.0 - .35 * j) / .4
                if v <= 0:
                    continue
                if (jg, LW) not in jue:
                    jue[(jg, LW)] = letrero(jg, int(LW), 100, 30, s=.26)
                p = _escala(jue[(jg, LW)], _reb(v))
                yj = y_et + 112 + j * 108
                im.alpha_composite(p, (int(tx - p.size[0] / 2), int(min(Y1 - 46, yj) - p.size[1] / 2)))
                d = ImageDraw.Draw(im)
        u = (dt - mk[0]) / .5
        if u > 0:
            p = brillo(_escala(cinta, _reb(u) * (1 + .015 * math.sin(dt * 3))), (dt - mk[0] - .3) / .8, fuerza=.35)
            im.alpha_composite(p, (int(rx - p.size[0] / 2), int(ry - p.size[1] / 2)))
        return _fin(im, dt, dur)
    return fn


# ------------------------------------------------------------------ pegatina con rótulo de cinta
def pegatina(ruta, titulo=None, tam=360, giro=-6.0):
    """Como mg_tes.pegatina (imagen REAL recortada con borde blanco que entra con rebote, se balancea y flota) pero el
    nombre va en una cinta de terciopelo pintada en Flow, con el texto ajustado al hueco azul (no la píldora negra)."""
    import mg_tes as T
    base = T._base_pegatina(ruta, tam)
    if titulo:
        tit = titulo.upper()
        ch = 74
        fin = 245 * ch / UI["cinta"].size[1]
        cw = int(min(max(base.width + 60, 300), 640))     # nunca más ancha que su hueco en una fila (efectos.fila)
        f = ajustar(tit, "t", 30, cw - 2 * fin - 16)
        c = nueve("cinta", cw, ch)
        _txt(ImageDraw.Draw(c), (cw / 2, ch / 2 + 2), tit, f, CREMA, "mm", 255, 2, AZUL_N)
        lien = Image.new("RGBA", (max(base.width, cw), base.height + ch // 2), (0, 0, 0, 0))
        lien.alpha_composite(base, ((lien.width - base.width) // 2, 0))
        lien.alpha_composite(c, ((lien.width - cw) // 2, base.height - ch // 2))
        base = lien

    def fn(dt, dur, marcas):
        s = T._pop(dt, .42)
        if s <= 0.02:
            return np.zeros((2, 2, 4), np.uint8)
        ang = giro * min(1.0, dt / .5) + (1 - min(1.0, dt / .5)) * -22 + 2.2 * math.sin(dt * 2.1)
        im = base.rotate(ang, resample=Image.BICUBIC, expand=True)
        k = s * (1 + .025 * math.sin(dt * 3.0))
        im = im.resize((max(2, int(im.width * k)), max(2, int(im.height * k))), Image.BILINEAR)
        a = np.array(im)[..., [2, 1, 0, 3]]
        fl = int(round(7 * math.sin(dt * 1.7)))
        out = np.zeros((a.shape[0] + 16, a.shape[1], 4), np.uint8)
        out[8 + fl:8 + fl + a.shape[0]] = a
        return out
    return fn
