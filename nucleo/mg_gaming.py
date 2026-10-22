# -*- coding: utf-8 -*-
"""MOTION GRAPHICS «Nintendo 64 / plataformas de Rare» por código (Crónicas del gaming; primer uso `banjo_tooie`, 19-oct-2026).
Hermano de mg_wow.py / mg_tes.py / mg_er.py con la estética de los plataformas 3D de N64: Cooper Black (títulos gordos y
redondos, como los logos de la época), Arial Rounded para el texto, paneles marrón chocolate con borde miel, amarillo miel,
azul Banjo y rojo Kazooie; todo entra con REBOTE (sobreimpulso), nada queda quieto (flota, late o brilla). CERO cifras ni
nombres inventados: solo lo que el guion ya dice.

Uso desde videos/<v>/efectos.py (FX `mg` de nucleo/secuencia_fx.py; acepta de/a o en/dur; `marcas` = anclas de la voz):
    import mg_gaming as G
  puesto(num, titulo)                 medallón miel con el número que rebota + cinta con el título (rótulo de cada secreto)
  ficha(titulo, texto, tipo=None)     cuadro de diálogo chocolate; *entre asteriscos* = miel; el texto entra línea a línea
  linea_tiempo(hitos, titulo)         línea que se dibuja; un hito por marca (año grande + texto); el último late en rojo
  swop(titulo)                        Stop 'n' Swop: cartucho 1 → barra de memoria que se vacía → cartucho 2; marca 3 = la
                                      carta de Nintendo lo tacha; marca 4 = «XBLA 2009» lo enciende en verde
  jinjos(titulo)                      9 casas de colores que se llenan de 1 a 9 Jinjos (una familia por marca) + la 10.ª gris
                                      agrietada con «?» y «SHOULDN'T BE HERE» en la última marca
  concurso(nombres, titulo)           tres atriles con su pesa colgando; marca k = la pesa cae sobre el atril k (aplastado)
  ocarina(canciones, titulo)          (zelda_oot) los 5 botones del mando (A + 4 C) entran; marca k = la canción k cae nota a
                                      nota en el pentagrama con su nombre (la anterior sale por la izquierda)
  paradoja(pasos, titulo)             (zelda_oot) bucle de 4 pasos con una nota que da vueltas; marca 4 = «¿QUIÉN LA COMPUSO?»,
                                      marca 5 = sello rojo «NADIE»
  versiones(cols, filas, titulo)      (zelda_oot) tabla de versiones del cartucho; marca k = la fila k se rellena casilla a
                                      casilla; lo que cambió late en rojo/verde
  tres_lineas(raiz, ramas, titulo)    (zelda_oot) medallón raíz; marca k = nace la rama k (línea que baja y se curva) con sus
                                      juegos; la rama marcada `caida` va en rojo
  (pegatinas: mg_tes.pegatina · pantallas: mg_wow.pantalla)
"""
import math

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

MIEL, MIEL_OSC, CREMA, CHOCO, AZUL, ROJO, VERDE, GRIS = ((255, 196, 38), (196, 128, 20), (255, 241, 210), (46, 27, 14),
                                                         (52, 104, 214), (214, 52, 40), (72, 200, 90), (150, 150, 150))
JINJO = [("Blanca", (240, 240, 240)), ("Naranja", (255, 140, 30)), ("Amarilla", (255, 220, 40)), ("Marrón", (140, 90, 50)),
         ("Verde", (70, 190, 70)), ("Roja", (220, 50, 50)), ("Azul", (60, 110, 230)), ("Morada", (150, 70, 200)),
         ("Negra", (40, 40, 40))]
_fc = {}


def fuente(estilo, tam):
    """estilo: «t» título (Cooper Black), «r» texto (Arial Rounded), «c» condensada (Bahnschrift)."""
    k = (estilo, tam)
    if k not in _fc:
        _fc[k] = ImageFont.truetype({"t": "C:/Windows/Fonts/COOPBL.TTF", "r": "C:/Windows/Fonts/ARLRDBD.TTF",
                                     "c": "C:/Windows/Fonts/bahnschrift.ttf"}[estilo], tam)
    return _fc[k]


def _eo(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def _reb(u):
    """Rebote con sobreimpulso (easeOutBack): pasa de 1 y vuelve."""
    u = max(0.0, min(1.0, u))
    c = 2.2
    return 1 + (c + 1) * (u - 1) ** 3 + c * (u - 1) ** 2


def _texto(d, xy, s, f, color, ancla="la", alfa=255, borde=0, color_borde=CHOCO):
    s = s.replace("·", "/")                       # Arial Rounded no trae el punto medio (salía un cuadro)
    a = int(max(0, min(255, alfa)))
    if a <= 0:
        return
    if borde:
        d.text(xy, s, font=f, fill=tuple(color) + (a,), anchor=ancla, stroke_width=borde,
               stroke_fill=tuple(color_borde) + (a,))
    else:
        d.text((xy[0] + 2, xy[1] + 3), s, font=f, fill=(0, 0, 0, int(a * .6)), anchor=ancla)
        d.text(xy, s, font=f, fill=tuple(color) + (a,), anchor=ancla)


def _bgra(im, alfa=1.0):
    a = np.array(im)
    if alfa < 1:
        a[..., 3] = (a[..., 3] * max(0.0, alfa)).astype(np.uint8)
    return a[..., [2, 1, 0, 3]].copy()


def _panel(w, h, borde=MIEL):
    """Panel chocolate redondeado con borde miel grueso y sombra suave (cuadro de diálogo de plataformas de N64)."""
    M = 40
    im = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
    sm = Image.new("L", im.size, 0)
    ImageDraw.Draw(sm).rounded_rectangle((M + 8, M + 14, M + w + 8, M + h + 14), 36, fill=150)
    som = Image.new("RGBA", im.size, (0, 0, 0, 255))
    som.putalpha(sm.filter(ImageFilter.GaussianBlur(16)))
    im.alpha_composite(som)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((M, M, M + w, M + h), 36, fill=CHOCO + (236,), outline=borde + (255,), width=7)
    d.rounded_rectangle((M + 12, M + 12, M + w - 12, M + h - 12), 28, outline=MIEL_OSC + (120,), width=2)
    return im, M


def _escala(im, s):
    """Escala alrededor del centro (para el rebote de entrada) manteniendo el lienzo."""
    if abs(s - 1) < .01:
        return im
    W, H = im.size
    s = max(.05, s)
    p = im.resize((max(1, int(W * s)), max(1, int(H * s))), Image.BICUBIC)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if s <= 1:
        out.alpha_composite(p, ((W - p.size[0]) // 2, (H - p.size[1]) // 2))
    else:
        x0, y0 = (p.size[0] - W) // 2, (p.size[1] - H) // 2
        out.alpha_composite(p.crop((x0, y0, x0 + W, y0 + H)))
    return out


def _partir(d, s, f, ancho):
    lineas, cur = [], ""
    for w in s.split():
        prueba = (cur + " " + w).strip()
        if d.textlength(prueba.replace("*", ""), font=f) <= ancho or not cur:
            cur = prueba
        else:
            lineas.append(cur)
            cur = w
    return lineas + [cur] if cur else lineas


def _linea_rica(d, x, y, s, f, alfa, ancla_y="m"):
    """Texto con *tramos* en miel; el resto en crema."""
    trozos = s.split("*")
    for i, t in enumerate(trozos):
        if not t:
            continue
        col = MIEL if i % 2 else CREMA
        _texto(d, (x, y), t, f, col, "l" + ancla_y, alfa)
        x += d.textlength(t, font=f)


# ------------------------------------------------------------------ rótulo de puesto
def puesto(num, titulo, ancho=None):
    """Medallón miel con el número (rebota y gira un poco, luego flota) + cinta chocolate con el título que se despliega.
    La cinta se ajusta al título (antes, con ancho fijo, «EL CONCURSO DE LA MUERTE» se cortaba)."""
    h = 300
    fnum, ftit, fsup = fuente("t", 150), fuente("t", 74), fuente("r", 34)
    if ancho is None:
        tw = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textlength(titulo.upper(), font=ftit)
        ancho = int(max(1100, 170 + 118 + 40 + tw + 90))

    def fn(dt, dur, marcas):
        im = Image.new("RGBA", (ancho, h), (0, 0, 0, 0))
        d = ImageDraw.Draw(im)
        cx, cy, R = 170, h / 2 + 6 * math.sin(dt * 2.4), 118
        u = _eo((dt - .25) / .55)
        if u > 0:                                           # cinta del título que se despliega hacia la derecha
            x1 = cx + 60 + (ancho - cx - 100) * u
            d.rounded_rectangle((cx + 40, cy - 66, x1, cy + 66), 30, fill=CHOCO + (235,), outline=MIEL + (255,), width=6)
            capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dc = ImageDraw.Draw(capa)
            _texto(dc, (cx + R + 40, cy - 32), "SECRETO NÚMERO " + str(num), fsup, MIEL, "lm", 255 * _eo((dt - .5) / .4))
            _texto(dc, (cx + R + 40, cy + 18), titulo.upper(), ftit, CREMA, "lm", 255 * _eo((dt - .55) / .4), borde=4)
            m = Image.new("L", im.size, 0)
            ImageDraw.Draw(m).rectangle((0, 0, int(x1 - 10), h), fill=255)
            a = np.array(capa)
            a[..., 3] = (a[..., 3].astype(np.uint16) * (np.array(m) // 255)).astype(np.uint8)
            im.alpha_composite(Image.fromarray(a))
        med = Image.new("RGBA", (2 * R + 40, 2 * R + 40), (0, 0, 0, 0))
        dm = ImageDraw.Draw(med)
        c = R + 20
        som = Image.new("RGBA", med.size, (0, 0, 0, 0))
        ImageDraw.Draw(som).ellipse((c - R, c - R + 10, c + R, c + R + 10), fill=(0, 0, 0, 110))
        med.alpha_composite(som.filter(ImageFilter.GaussianBlur(5)))
        dm.ellipse((c - R, c - R, c + R, c + R), fill=MIEL + (255,), outline=CHOCO + (255,), width=8)
        luz = Image.new("RGBA", med.size, (0, 0, 0, 0))
        ImageDraw.Draw(luz).ellipse((c - R + 22, c - R + 16, c + R - 44, c - 14), fill=(255, 245, 190, 110))
        med.alpha_composite(luz)
        dm = ImageDraw.Draw(med)
        _texto(dm, (c, c + 4), str(num), fnum, CREMA, "mm", 255, borde=7)
        med = _escala(med, _reb(dt / .5)).rotate(-14 * (1 - _eo(dt / .7)) + 4 * math.sin(dt * 1.7), Image.BICUBIC)
        im.alpha_composite(med, (int(cx - c), int(cy - c)))
        return _bgra(im, min(1.0, (dur - dt) / .45))
    return fn


# ------------------------------------------------------------------ ficha (cuadro de diálogo)
def ficha(titulo, texto, tipo=None, ancho=820):
    """Cuadro chocolate con borde miel; título en Cooper con borde, `tipo` chico en azul claro, el texto entra línea a línea
    (*entre asteriscos* = miel). Entra con rebote y respira un poco."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    ft, fty, fx = fuente("t", 54), fuente("r", 28), fuente("r", 38)
    lineas = _partir(tmp, texto, fx, ancho - 90)
    h = 130 + (40 if tipo else 0) + 52 * len(lineas) + 30

    def fn(dt, dur, marcas):
        im, M = _panel(ancho, h)
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(cap)
        y = M + 70
        _texto(d, (M + 45, y), titulo, ft, MIEL, "lm", 255, borde=4)
        y += 46
        if tipo:
            _texto(d, (M + 47, y), tipo.upper(), fty, (150, 190, 255), "lm", 230)
            y += 40
        d.line([(M + 45, y), (M + ancho - 45, y)], fill=MIEL_OSC + (200,), width=3)
        y += 40
        for i, ln in enumerate(lineas):
            a = 255 * _eo((dt - .35 - .28 * i) / .35)
            _linea_rica(d, M + 45, y + 52 * i, ln, fx, a)
        im.alpha_composite(cap)
        s = _reb(dt / .45) * (1 + .006 * math.sin(dt * 3))
        return _bgra(_escala(im, s), min(1.0, (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ línea de tiempo
def linea_tiempo(hitos, titulo="Así se hizo", w=1720, h=430, rojo_ultimo=True):
    """hitos = [(año, texto)]; marca 0 = se dibuja la línea; marca k (1..n) = entra el hito k-1 (cae con rebote). El último
    hito late (en rojo con `rojo_ultimo`)."""
    n = len(hitos)
    fa, fx, ft = fuente("t", 58), fuente("r", 27), fuente("t", 44)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(cap)
        _texto(d, (M + w / 2, M + 58), titulo.upper(), ft, MIEL, "mm", 255 * _eo(dt / .4), borde=3)
        y = M + h * .52
        x0, x1 = M + 200, M + w - 200
        u = _eo((dt - mk[0]) / .9)
        d.line([(x0, y), (x0 + (x1 - x0) * u, y)], fill=CREMA + (230,), width=6)
        for i, (anio, txt) in enumerate(hitos):
            x = x0 + (x1 - x0) * (i / max(1, n - 1))
            v = (dt - mk[1 + i]) / .5
            if v <= 0:
                d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(90, 70, 50, int(200 * u)))
                continue
            ult = i == n - 1
            col = ROJO if (ult and rojo_ultimo) else MIEL
            r = 16 * _reb(v) * (1 + (.18 * math.sin(dt * 6) if ult else 0))
            d.ellipse((x - r, y - r, x + r, y + r), fill=col + (255,), outline=CHOCO + (255,), width=4)
            dy = 30 * (1 - _reb(v))
            a = 255 * _eo(v)
            _texto(d, (x, y - 36 - dy), str(anio), fa, col if ult else CREMA, "mb", a, borde=4)
            for k, ln in enumerate(_partir(d, txt, fx, min(340, (x1 - x0) / max(1, n - 1) * .9))[:3]):
                _texto(d, (x, y + 34 + 32 * k + dy), ln, fx, CREMA, "mt", a)
        im.alpha_composite(cap)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ Stop 'n' Swop
def _cartucho(d, cx, cy, s, etiqueta, col, a):
    """Cartucho de N64 esquemático (cuerpo gris oscuro con hombros, etiqueta de color con el nombre)."""
    if a <= 0:
        return
    A = int(a)
    w, h = 250 * s, 170 * s
    d.polygon([(cx - w / 2, cy - h / 2 + 18 * s), (cx - w / 2 + 18 * s, cy - h / 2), (cx + w / 2 - 18 * s, cy - h / 2),
               (cx + w / 2, cy - h / 2 + 18 * s), (cx + w / 2, cy + h / 2), (cx - w / 2, cy + h / 2)],
              fill=(70, 70, 78, A), outline=(20, 20, 24, A))
    d.rounded_rectangle((cx - w / 2 + 20 * s, cy - h / 2 + 22 * s, cx + w / 2 - 20 * s, cy + h / 2 - 32 * s), 8,
                        fill=col + (A,))
    for k in range(7):
        x = cx - w / 2 + 28 * s + k * 30 * s
        d.line([(x, cy + h / 2 - 16 * s), (x + 12 * s, cy + h / 2 - 16 * s)], fill=(40, 40, 46, A), width=3)
    _texto(d, (cx, cy - 8 * s), etiqueta, fuente("t", max(8, int(30 * s))), CREMA, "mm", a, borde=3)


def _huevo(d, cx, cy, r, col, a):
    if a <= 0:
        return
    d.ellipse((cx - r * .78, cy - r, cx + r * .78, cy + r * .9), fill=col + (int(a),), outline=CHOCO + (int(a),), width=3)
    d.ellipse((cx - r * .4, cy - r * .7, cx - r * .05, cy - r * .25), fill=(255, 255, 255, int(a * .5)))


def swop(titulo="Stop 'n' Swop", w=1500, h=560):
    """marca 0: cartucho 1 con el huevo · marca 1: se apaga, la barra de memoria se vacía y el huevo viaja · marca 2: llega
    al cartucho 2 · marca 3: Nintendo lo tacha (X roja) · marca 4: «XBLA 2009» se enciende en verde y el viaje vuelve."""
    ft, fb, fs = fuente("t", 50), fuente("r", 28), fuente("t", 62)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 6
        im, M = _panel(w, h)
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(cap)
        _texto(d, (M + w / 2, M + 56), titulo.upper(), ft, MIEL, "mm", 255 * _eo(dt / .4), borde=3)
        cy = M + h * .50
        xa, xb = M + w * .18, M + w * .82
        _cartucho(d, xa, cy + 8 * math.sin(dt * 2), max(.05, _reb((dt - mk[0]) / .5)), "Banjo-Kazooie", AZUL,
                  255 * _eo((dt - mk[0]) / .3))
        if dt > mk[1]:
            _cartucho(d, xb, cy + 8 * math.sin(dt * 2 + 1), max(.05, _reb((dt - mk[1]) / .5)), "Banjo-Tooie", ROJO,
                      255 * _eo((dt - mk[1]) / .3))
        bx0, bx1, by = M + w * .33, M + w * .67, M + h * .80   # barra de memoria que se vacía al apagar
        if dt > mk[1] - .1:
            lleno = 1 - _eo((dt - mk[1]) / 2.6)
            d.rounded_rectangle((bx0, by - 16, bx1, by + 16), 14, outline=CREMA + (220,), width=3)
            if lleno > .01:
                d.rounded_rectangle((bx0 + 5, by - 11, bx0 + 5 + (bx1 - bx0 - 10) * lleno, by + 11), 10,
                                    fill=(MIEL if lleno > .3 else ROJO) + (255,))
            _texto(d, ((bx0 + bx1) / 2, by + 30), "MEMORIA AL APAGAR LA CONSOLA", fb, CREMA, "mt", 220)
        hx, hy = xa, cy - 130
        if dt > mk[1]:
            tramo = (mk[2] - mk[1]) if mk[2] < 90 else 2.0
            v = _eo((dt - mk[1]) / max(.6, tramo))
            hx, hy = xa + (xb - xa) * v, cy - 130 - 110 * math.sin(math.pi * v)
        rojo, verde = _eo((dt - mk[3]) / .4), _eo((dt - mk[4]) / .5)
        if dt > mk[4]:                                      # 2009: el viaje vuelve, en bucle
            v = ((dt - mk[4]) / 1.8) % 1
            hx, hy = xa + (xb - xa) * v, cy - 130 - 110 * math.sin(math.pi * v)
        _huevo(d, hx, hy, 34, (255, 120, 190), 255 * _eo((dt - mk[0] - .2) / .4) * (1 - .7 * rojo * (1 - verde)))
        if rojo > 0:
            cx, cyy, r = M + w / 2, cy - 100, 90 * _reb((dt - mk[3]) / .45)
            col = ROJO + (int(255 * rojo * (1 - .7 * verde)),)
            d.line([(cx - r, cyy - r), (cx + r, cyy + r)], fill=col, width=22)
            d.line([(cx - r, cyy + r), (cx + r, cyy - r)], fill=col, width=22)
            _texto(d, (cx, cyy + 108), "NINTENDO PIDE QUITARLO", fb, ROJO, "mt", 255 * rojo * (1 - verde))
        if verde > 0:
            capa = Image.new("RGBA", (380, 140), (0, 0, 0, 0))
            dc = ImageDraw.Draw(capa)
            dc.rounded_rectangle((10, 10, 370, 130), 30, fill=VERDE + (255,), outline=CHOCO + (255,), width=6)
            _texto(dc, (190, 72), "XBLA 2009", fs, CREMA, "mm", 255, borde=4)
            capa = _escala(capa, _reb((dt - mk[4]) / .5))
            im.alpha_composite(capa, (int(M + w / 2 - 190), int(cy + 10)))
        im.alpha_composite(cap)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ familias Jinjo
def _jinjo(d, cx, cy, r, col, a, fase=0.0):
    """Jinjo esquemático: cuerpo redondo, ojos grandes, boca abierta y bracitos que saludan."""
    if a <= 0:
        return
    A = int(a)
    borde = (20, 20, 20, A) if col != (40, 40, 40) else (210, 210, 210, A)
    by = cy + 2 * math.sin(fase * 5)
    d.ellipse((cx - r, by - r, cx + r, by + r), fill=col + (A,), outline=borde, width=2)
    for s in (-1, 1):
        d.line([(cx + s * r * .8, by), (cx + s * r * 1.45, by - r * (.6 + .35 * math.sin(fase * 7 + s)))], fill=borde,
               width=3)
        ex = cx + s * r * .38
        d.ellipse((ex - r * .24, by - r * .5, ex + r * .24, by - r * .02), fill=(255, 255, 255, A), outline=(0, 0, 0, A))
        d.ellipse((ex - r * .1, by - r * .34, ex + r * .1, by - r * .14), fill=(0, 0, 0, A))
    d.ellipse((cx - r * .22, by + r * .15, cx + r * .22, by + r * .55), fill=(90, 20, 20, A))


def jinjos(titulo="Las familias Jinjo", w=1720, h=640):
    """marcas 0..8: la familia k entra con sus k+1 Jinjos (blanca 1 … negra 9; contador que llega a 45) · marca 9: la 10.ª
    casa gris, agrietada, con diez «?» y la etiqueta «SHOULDN'T BE HERE» que tiembla."""
    ft, fn_, fc, fe = fuente("t", 48), fuente("r", 24), fuente("t", 56), fuente("c", 34)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 12
        im, M = _panel(w, h)
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(cap)
        _texto(d, (M + 60, M + 56), titulo.upper(), ft, MIEL, "lm", 255 * _eo(dt / .4), borde=3)
        col_w = (w - 120) / 10
        base = M + h - 70
        total = 0
        for k, (nom, col) in enumerate(JINJO):
            u = (dt - mk[k]) / .45
            if u <= 0:
                continue
            x = M + 60 + col_w * (k + .5)
            a = int(255 * _eo(u))
            d.polygon([(x - 54, base - 42), (x, base - 86), (x + 54, base - 42)], fill=col + (a,), outline=CHOCO + (a,))
            d.rectangle((x - 42, base - 42, x + 42, base), fill=(120, 80, 50, a), outline=CHOCO + (a,))
            d.rectangle((x - 12, base - 26, x + 12, base), fill=CHOCO + (a,))
            _texto(d, (x, base + 10), nom, fn_, CREMA, "mt", a)
            for j in range(k + 1):                         # torre de Jinjos que van cayendo uno a uno
                v = (dt - mk[k] - .06 * j) / .35
                if v <= 0:
                    continue
                yy = base - 110 - j * 40 - 24 * (1 - _reb(v))
                _jinjo(d, x + (9 if j % 2 else -9), yy, 17, col, 255 * _eo(v), dt + k + j)
                total += 1
        if total:
            _texto(d, (M + w - 60, M + 56), f"{total} JINJO" + ("S" if total != 1 else ""), fc, CREMA, "rm", 255, borde=4)
        g = (dt - mk[9]) / .5
        if g > 0:                                           # la familia gris
            x = M + 60 + col_w * 9.5
            a = int(255 * _eo(g))
            tb = 3 * math.sin(dt * 40) * max(0.0, 1 - g / 4)
            d.polygon([(x - 54 + tb, base - 42), (x - 8, base - 74), (x + 6, base - 60), (x + 54, base - 42)],
                      fill=GRIS + (a,), outline=CHOCO + (a,))
            d.rectangle((x - 42, base - 42, x + 42, base), fill=(95, 95, 95, a), outline=CHOCO + (a,))
            d.line([(x - 10, base - 42), (x + 4, base - 24), (x - 6, base - 12), (x + 8, base)], fill=(20, 20, 20, a),
                   width=4)
            _texto(d, (x, base + 10), "Gris", fn_, GRIS, "mt", a)
            for j in range(10):
                yy = base - 108 - j * 36 + 4 * math.sin(dt * 3 + j)
                _texto(d, (x + (9 if j % 2 else -9), yy), "?", fuente("t", 34), GRIS, "mm", a * (.55 + .45 * (j % 2)))
            e = (dt - mk[9] - .8) / .4
            if e > 0:
                capa = Image.new("RGBA", (440, 70), (0, 0, 0, 0))
                dc = ImageDraw.Draw(capa)
                dc.rectangle((4, 4, 436, 66), fill=(250, 240, 120, 255), outline=(20, 20, 20, 255), width=3)
                _texto(dc, (220, 36), "SHOULDN'T BE HERE", fe, (20, 20, 20), "mm", 255)
                capa = _escala(capa.rotate(-8 + 2 * math.sin(dt * 5), Image.BICUBIC, expand=True), _reb(e))
                im.alpha_composite(capa, (int(x - capa.size[0] + 50), int(M + 100)))
        im.alpha_composite(cap)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ el concurso de las pesas
def concurso(nombres=("Banjo y Kazooie", "Mingella", "Blobbelda"), titulo="Tower of Tragedy", w=1500, h=620):
    """Tres atriles con una pesa «1 TON» colgando de su cuerda; marca 0 = entran · marca k (1, 2) = la pesa cae sobre el
    atril k (golpe, polvo, nombre en rojo y tachado). El atril 0 sobrevive y brilla al final."""
    ft, fn_, fp = fuente("t", 50), fuente("t", 40), fuente("t", 30)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 4
        im, M = _panel(w, h)
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(cap)
        _texto(d, (M + w / 2, M + 56), titulo.upper(), ft, MIEL, "mm", 255 * _eo(dt / .4), borde=3)
        piso = M + h - 80
        for i, nom in enumerate(nombres):
            x = M + w * (.2 + .3 * i)
            u = _reb((dt - mk[0] - .15 * i) / .5)
            if u <= 0:
                continue
            a = int(255 * min(1, u))
            caida = _eo((dt - mk[i]) / .28) if i > 0 else 0
            col = (AZUL, (110, 60, 160), (60, 140, 90))[i]
            ya = piso - 150 * (1 - caida * .75)
            d.polygon([(x - 90, piso), (x - 70, ya), (x + 70, ya), (x + 90, piso)], fill=col + (a,), outline=CHOCO + (a,))
            d.rectangle((x - 74, ya - 16, x + 74, ya), fill=MIEL + (a,), outline=CHOCO + (a,))
            _texto(d, (x, piso + 14), nom, fn_, CREMA if caida < .5 else ROJO, "mt", a, borde=3)
            if caida > .5:
                d.line([(x - 120, piso + 36), (x + 120, piso + 36)], fill=ROJO + (230,), width=6)
            yp0 = M + 110 + 6 * math.sin(dt * 2 + i)
            yp = yp0 + (ya - 116 - yp0) * caida
            d.line([(x, M + 90), (x, yp)], fill=CREMA + (int(a * (1 - caida)),), width=3)
            d.polygon([(x - 58, yp + 100), (x - 40, yp), (x + 40, yp), (x + 58, yp + 100)], fill=(60, 60, 66, a),
                      outline=(20, 20, 20, a))
            d.ellipse((x - 16, yp - 22, x + 16, yp + 6), outline=(60, 60, 66, a), width=6)
            _texto(d, (x, yp + 54), "1 TON", fp, CREMA, "mm", a)
            if i > 0:                                       # polvo del golpe
                p = (dt - mk[i] - .28) / .9
                if 0 < p < 1:
                    for k in range(10):
                        ang = math.pi * (k / 9)
                        rr = 40 + 120 * _eo(p)
                        px, py = x + math.cos(ang) * rr * 1.4, piso - 20 - math.sin(ang) * rr * .4
                        d.ellipse((px - 14, py - 14, px + 14, py + 14), fill=(200, 180, 150, int(160 * (1 - p))))
        if dt > mk[2] + .8:                                 # sobrevive el atril 0
            x = M + w * .2
            b = .5 + .5 * math.sin(dt * 5)
            d.ellipse((x - 130, piso - 280, x + 130, piso - 10), outline=MIEL + (int(140 * b),), width=5)
        im.alpha_composite(cap)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ Ocarina of Time (zelda_oot, 22-oct-2026)
NOTA_Y = {"A": 0, "v": 1, ">": 2, "<": 3, "^": 4}          # renglón del pentagrama de cada botón (como en el juego)


def _boton(d, cx, cy, r, b, a):
    """Botón del mando de N64: A = círculo azul con «A»; C = círculo amarillo con flecha."""
    if a <= 0:
        return
    A = int(a)
    col = (60, 110, 230) if b == "A" else (255, 205, 40)
    d.ellipse((cx - r, cy - r + 4, cx + r, cy + r + 4), fill=(0, 0, 0, int(A * .45)))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=col + (A,), outline=CHOCO + (A,), width=max(2, int(r / 9)))
    d.ellipse((cx - r * .6, cy - r * .72, cx + r * .2, cy - r * .2), fill=(255, 255, 255, int(A * .35)))
    if b == "A":
        _texto(d, (cx, cy + 2), "A", fuente("t", max(10, int(r * 1.15))), CREMA, "mm", a, borde=2)
        return
    s = r * .5
    pts = {"^": [(0, -1), (-.9, .6), (.9, .6)], "v": [(0, 1), (-.9, -.6), (.9, -.6)],
           ">": [(1, 0), (-.6, -.9), (-.6, .9)], "<": [(-1, 0), (.6, -.9), (.6, .9)]}[b]
    d.polygon([(cx + px * s, cy + py * s) for px, py in pts], fill=CHOCO + (A,))


def ocarina(canciones, titulo="La ocarina: cinco notas", w=1600, h=560):
    """canciones = [(nombre, "v><v><")] (botones A v > < ^). marca 0 = los 5 botones entran uno a uno (rebote) · marca k
    (1..n) = la canción k-1 cae nota a nota en el pentagrama y su nombre aparece debajo; la anterior se desliza fuera."""
    ft, fn_, fb = fuente("t", 50), fuente("t", 46), fuente("r", 26)
    n = len(canciones)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(cap)
        _texto(d, (M + w / 2, M + 56), titulo.upper(), ft, MIEL, "mm", 255 * _eo(dt / .4), borde=3)
        # mando: A abajo a la izquierda y la cruz de botones C, como en el mando de N64
        bx, by = M + 200, M + h * .56
        lay = [("A", -70, 95), ("^", 40, -45), ("v", 40, 95), ("<", -30, 25), (">", 110, 25)]
        for i, (b, ox, oy) in enumerate(lay):
            u = (dt - mk[0] - .14 * i) / .45
            if u > 0:
                r = 44 * _reb(u)
                act = False
                for k in range(n):                          # se ilumina el botón que suena ahora
                    t0 = mk[1 + k]
                    j = int((dt - t0) / .32)
                    if 0 <= j < len(canciones[k][1]) and canciones[k][1][j] == b and (k == n - 1 or dt < mk[2 + k]):
                        act = True
                _boton(d, bx + ox, by + oy - (8 if act else 0), r * (1.12 if act else 1), b, 255 * min(1, u))
        _texto(d, (bx + 20, M + h - 50), "SOLO 5 BOTONES LIBRES", fb, CREMA, "mm", 220 * _eo((dt - mk[0] - .8) / .4))
        # pentagrama
        x0, x1 = M + 420, M + w - 70
        y0, paso = M + 150, 52
        ap = 255 * _eo((dt - mk[0]) / .5)
        for k in range(5):
            yy = y0 + k * paso
            d.line([(x0, yy), (x0 + (x1 - x0) * _eo((dt - mk[0] - .05 * k) / .7), yy)], fill=CREMA + (int(ap * .55),),
                   width=3)
        for k, (nom, notas) in enumerate(canciones):
            t0 = mk[1 + k]
            if dt < t0:
                continue
            sal = _eo((dt - mk[2 + k]) / .45) if k < n - 1 else 0
            if sal >= 1:
                continue
            dx = -(x1 - x0) * .6 * sal
            a_c = 255 * (1 - sal)
            for j, b in enumerate(notas):
                v = (dt - t0 - .32 * j) / .35
                if v <= 0:
                    continue
                x = x0 + 70 + j * (x1 - x0 - 140) / max(1, len(notas) - 1) + dx
                y = y0 + (4 - NOTA_Y[b]) * paso - 60 * (1 - _reb(v))
                _boton(d, x, y, 36, b, a_c * min(1, _eo(v)))
            _texto(d, ((x0 + x1) / 2 + dx, y0 + 4 * paso + 62), nom.upper(), fn_, MIEL, "mm",
                   a_c * _eo((dt - t0 - .2) / .4), borde=4)
        im.alpha_composite(cap)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def paradoja(pasos, titulo="La canción de la tormenta", w=1560, h=780, pregunta="¿QUIÉN LA COMPUSO?", sello="NADIE"):
    """pasos = 4 textos en el orden del bucle (arriba, derecha, abajo, izquierda). marcas 0..3 = entra cada paso y se dibuja
    la flecha que lo une al siguiente; cuando están todas, una nota da vueltas al bucle sin parar · marca 4 = la pregunta en
    el centro · marca 5 = sello rojo que cae con golpe y queda latiendo."""
    ft, fp, fq, fs = fuente("t", 48), fuente("r", 30), fuente("t", 40), fuente("t", 96)
    fnota = ImageFont.truetype("C:/Windows/Fonts/seguisym.ttf", 64)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * 8
        im, M = _panel(w, h)
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(cap)
        _texto(d, (M + w / 2, M + 56), titulo.upper(), ft, MIEL, "mm", 255 * _eo(dt / .4), borde=3)
        cx, cy = M + w / 2, M + h * .56
        RX, RY = w * .33, h * .30                           # bucle ovalado: deja sitio a la pregunta y al sello
        angs = [-90, 0, 90, 180]
        for i in range(4):                                  # arco de cada paso al siguiente; el último cierra el bucle
            t_ini = mk[i + 1] if i < 3 else mk[3] + .5
            u = _eo((dt - t_ini) / .7)
            if u <= 0:
                continue
            a0, a1 = angs[i] + 18, angs[i] + 18 + (90 - 36) * u
            d.arc((cx - RX, cy - RY, cx + RX, cy + RY), a0, a1, fill=MIEL + (230,), width=8)
            if u > .95:                                     # punta de flecha
                t = math.radians(a1)
                px, py = cx + RX * math.cos(t), cy + RY * math.sin(t)
                tg = math.atan2(RY * math.cos(t), -RX * math.sin(t))
                d.polygon([(px + 22 * math.cos(tg), py + 22 * math.sin(tg)),
                           (px + 14 * math.cos(tg + 2.2), py + 14 * math.sin(tg + 2.2)),
                           (px + 14 * math.cos(tg - 2.2), py + 14 * math.sin(tg - 2.2))], fill=MIEL + (255,))
        if dt > mk[3] + 1.2:                                # la nota que gira por el bucle
            v = ((dt - mk[3] - 1.2) / 3.2) % 1
            for k in range(6):                              # estela
                tt = math.radians(-90 + 360 * v - 6 * (k + 1))
                ex, ey = cx + RX * math.cos(tt), cy + RY * math.sin(tt)
                d.ellipse((ex - 11 + k, ey - 11 + k, ex + 11 - k, ey + 11 - k), fill=MIEL + (int(160 - 25 * k),))
            t = math.radians(-90 + 360 * v)
            _texto(d, (cx + RX * math.cos(t), cy + RY * math.sin(t)), "♪", fnota, CREMA, "mm", 255, borde=3)
        for i, txt in enumerate(pasos):
            u = (dt - mk[i]) / .45
            if u <= 0:
                continue
            t = math.radians(angs[i])
            px, py = cx + RX * math.cos(t), cy + RY * math.sin(t)
            lineas = _partir(d, txt, fp, 270)
            bw, bh = 320, 36 * len(lineas) + 34
            caja = Image.new("RGBA", (bw + 20, bh + 20), (0, 0, 0, 0))
            dc = ImageDraw.Draw(caja)
            dc.rounded_rectangle((10, 10, bw + 10, bh + 10), 22, fill=(70, 42, 22, 250), outline=MIEL + (255,), width=5)
            for k, ln in enumerate(lineas):
                _texto(dc, ((bw + 20) / 2, (bh + 20) / 2 - 18 * (len(lineas) - 1) + 36 * k), ln, fp, CREMA, "mm", 255)
            caja = _escala(caja, _reb(u))
            cap.alpha_composite(caja, (int(px - (bw + 20) / 2), int(py - (bh + 20) / 2 + 4 * math.sin(dt * 2 + i))))
        q = (dt - mk[4]) / .45
        if q > 0:
            _texto(d, (cx, cy - 70), pregunta, fq, CREMA, "mm", 255 * _eo(q), borde=3)
        im.alpha_composite(cap)
        s = (dt - mk[5]) / .35
        if s > 0:
            capa = Image.new("RGBA", (460, 170), (0, 0, 0, 0))
            dc = ImageDraw.Draw(capa)
            dc.rounded_rectangle((10, 10, 450, 160), 26, fill=(255, 241, 210, 40), outline=ROJO + (255,), width=10)
            _texto(dc, (230, 88), sello, fs, ROJO, "mm", 255, borde=4, color_borde=CREMA)
            capa = capa.rotate(-9, Image.BICUBIC, expand=True)
            capa = _escala(capa, (1.9 - .9 * _eo(s)) * (1 + .04 * math.sin(dt * 6)))
            im.alpha_composite(capa, (int(cx - capa.size[0] / 2), int(cy + 50 - capa.size[1] / 2)))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def versiones(cols, filas, titulo="El juego que cambió en silencio", w=1640, h=600):
    """cols = ["1.0", "1.1", ...]; filas = [(nombre, [(texto, color)])], color None = crema, "rojo", "verde" o "miel"; las
    celdas rojas/verdes laten (lo que cambió). marca 0 = cabecera (un cartucho por versión) · marca k (1..n) = la fila k-1
    se rellena casilla a casilla."""
    ft, fr, fc = fuente("t", 48), fuente("r", 30), fuente("t", 34)
    COL = {None: CREMA, "rojo": ROJO, "verde": VERDE, "miel": MIEL}

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (len(filas) + 2)
        im, M = _panel(w, h)
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(cap)
        _texto(d, (M + w / 2, M + 56), titulo.upper(), ft, MIEL, "mm", 255 * _eo(dt / .4), borde=3)
        xn, xc0 = M + 50, M + 560
        cw = (w - 560 - 50) / len(cols)
        yh = M + 160
        for j, c in enumerate(cols):                        # cabecera: un cartucho por versión
            u = (dt - mk[0] - .12 * j) / .45
            if u > 0:
                _cartucho(d, xc0 + cw * (j + .5), yh + 4 * math.sin(dt * 2 + j), .8 * max(.05, _reb(u)), c,
                          AZUL if "Game" not in c else (110, 60, 160), 255 * _eo(u))
        for i, (nom, celdas) in enumerate(filas):
            y = yh + 150 + i * 105
            u = (dt - mk[1 + i]) / .4
            if u <= 0:
                continue
            d.line([(xn, y - 56), (M + w - 50, y - 56)], fill=MIEL_OSC + (int(160 * _eo(u)),), width=2)
            lns = _partir(d, nom, fr, 480)[:2]
            for k, ln in enumerate(lns):
                _texto(d, (xn, y + 34 * k - 17 * (len(lns) - 1)), ln, fr, CREMA, "lm", 255 * _eo(u))
            for j, (txt, col) in enumerate(celdas):
                v = (dt - mk[1 + i] - .3 - .28 * j) / .35
                if v <= 0:
                    continue
                x = xc0 + cw * (j + .5)
                c = COL[col]
                late = (1 + .07 * math.sin(dt * 6 + j)) if col in ("rojo", "verde") else 1
                bw = cw * .86 * _reb(v) * late
                d.rounded_rectangle((x - bw / 2, y - 34, x + bw / 2, y + 34), 18, fill=c + (int(60 * _eo(v)),),
                                    outline=c + (int(255 * _eo(v)),), width=4)
                _texto(d, (x, y), txt, fc, c, "mm", 255 * _eo(v), borde=3)
        im.alpha_composite(cap)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn


def tres_lineas(raiz, ramas, titulo="Una historia, tres caminos", w=1720, h=700):
    """raiz = texto del medallón de arriba; ramas = [(etiqueta, [juegos], caida)]. marca 0 = el medallón entra y late ·
    marca k (1..n) = nace la rama k-1: la línea baja desde la raíz y se curva hacia su columna, la etiqueta aparece y los
    juegos caen uno a uno con rebote. `caida` = rama en rojo (el héroe derrotado)."""
    ft, fr, fe, fj = fuente("t", 46), fuente("t", 44), fuente("r", 32), fuente("t", 36)
    n = len(ramas)

    def fn(dt, dur, marcas):
        mk = list(marcas) + [99] * (n + 2)
        im, M = _panel(w, h)
        cap = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(cap)
        _texto(d, (M + w / 2, M + 52), titulo.upper(), ft, MIEL, "mm", 255 * _eo(dt / .4), borde=3)
        rx, ry = M + w / 2, M + 150
        for k, (eti, juegos, caida) in enumerate(ramas):
            u = _eo((dt - mk[1 + k]) / .9)
            if u <= 0:
                continue
            col = ROJO if caida else MIEL
            tx, ty = M + w * (k + .5) / n, M + 330
            pts = []
            for s in range(31):                             # curva raíz -> columna, dibujada hasta u
                t = s / 30 * u
                pts.append(((1 - t) ** 2 * rx + 2 * (1 - t) * t * rx + t * t * tx,
                            (1 - t) ** 2 * ry + 2 * (1 - t) * t * (ry + 130) + t * t * ty))
            d.line(pts, fill=col + (240,), width=9, joint="curve")
            if u > .9:
                d.ellipse((tx - 14, ty - 14, tx + 14, ty + 14), fill=col + (255,), outline=CHOCO + (255,), width=4)
                for j, ln in enumerate(_partir(d, eti, fe, w / n - 70)[:2]):
                    _texto(d, (tx, ty + 30 + 32 * j), ln, fe, col if caida else CREMA, "mt",
                           255 * _eo((dt - mk[1 + k] - .7) / .4))
            for j, jg in enumerate(juegos):
                v = (dt - mk[1 + k] - 1.0 - .35 * j) / .4
                if v <= 0:
                    continue
                y = ty + 130 + j * 66 - 30 * (1 - _reb(v))
                bw = d.textlength(jg, font=fj) + 50
                d.rounded_rectangle((tx - bw / 2, y - 26, tx + bw / 2, y + 26), 22, fill=(70, 42, 22, int(250 * _eo(v))),
                                    outline=col + (int(255 * _eo(v)),), width=4)
                _texto(d, (tx, y), jg, fj, CREMA, "mm", 255 * _eo(v), borde=2)
        u = (dt - mk[0]) / .5                               # la raíz va encima de las líneas
        if u > 0:
            capa = Image.new("RGBA", (620, 120), (0, 0, 0, 0))
            dc = ImageDraw.Draw(capa)
            dc.rounded_rectangle((10, 10, 610, 110), 50, fill=VERDE + (255,), outline=CHOCO + (255,), width=7)
            _texto(dc, (310, 62), raiz, fr, CREMA, "mm", 255, borde=4)
            capa = _escala(capa, _reb(u) * (1 + .02 * math.sin(dt * 3)))
            cap.alpha_composite(capa, (int(rx - 310), int(ry - 60)))
        im.alpha_composite(cap)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .4))
    return fn
