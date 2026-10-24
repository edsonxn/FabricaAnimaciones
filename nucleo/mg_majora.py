# -*- coding: utf-8 -*-
"""MOTION GRAPHICS TRANSLÚCIDOS con la interfaz de ZELDA: MAJORA'S MASK (Crónicas del gaming; primer uso `majora_mask`, 23-oct-2026).
Nace de la regla del usuario del 22-oct (al ver las tablillas opacas de zelda_oot): «nada de carteles opacos que tapen el video;
fichas translúcidas como las de Tamriel, pero con la interfaz de CADA juego». Aquí la interfaz es la del propio Majora:
  - el CUADRO DE DIÁLOGO de N64 (negro translúcido, esquinas redondas, texto blanco que se escribe letra a letra, nombres en
    rojo/rosa, triángulo verde de «siguiente» que late);
  - el CARTEL DE «Amanecer del primer día / -Quedan 72 horas-» (letras blancas con serifa, que se abren con tracking) como rótulo
    de cada secreto;
  - el RELOJ DE TRES DÍAS del HUD (arco con el sol/la luna, contador de horas);
  - morado de la máscara + rosa de sus ojos + amarillo de sus púas como acentos finos (nunca relleno opaco).
Todo vive sobre humo negro difuminado (alfa ≤ ~0,7): el gameplay se sigue viendo detrás.
    import mg_majora as M
  ficha(titulo, texto, tipo)          cuadro de diálogo N64; *x* = rojo/rosa como los nombres del juego
  puesto(num, titulo)                 cartel «Amanecer…» con el número del secreto y su título
  reloj(titulo, pasos)                el reloj de 3 días; cada marca = un paso (día, horas que quedan, texto)
  ciclo(pasos, centro)                el bucle de los tres días: Día 1 -> 2 -> 3 -> la luna cae -> Canción del Tiempo
  horario(titulo, dias, filas)        cuaderno de los Bombers: filas de personajes con citas por día; una por marca
  rejilla(titulo, n, remate, icono)   las casillas de máscaras que se llenan; al final, la máscara especial
  almas(titulo, items)                persona -> máscara (retrato real que se funde en su máscara) con su destino; una por marca
  pegatina(ruta, titulo, tam)         imagen REAL con borde blanco; el nombre en una píldora translúcida morada
Probar SIEMPRE con una hoja de cuadros antes de `fx` (texto largo, cifras, títulos largos).
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import mg_gaming as G

BLANCO, CREMA = (250, 250, 248), (236, 228, 210)
ROSA, MORADO, AMARILLO = (255, 92, 150), (120, 50, 160), (250, 206, 60)
VERDE, ROJO, GRIS = (90, 230, 110), (255, 80, 80), (170, 165, 175)
_fc = {}
_eo, _reb, _escala, _bgra = G._eo, G._reb, G._escala, G._bgra
_D = ImageDraw.Draw(Image.new("RGBA", (8, 8)))


def fuente(estilo, tam):
    """«d» diálogo N64 (Arial Rounded), «s» serifa del cartel de los días (Georgia negrita), «si» su cursiva."""
    k = (estilo, int(tam))
    if k not in _fc:
        _fc[k] = ImageFont.truetype({"d": "C:/Windows/Fonts/ARLRDBD.TTF", "s": "C:/Windows/Fonts/georgiab.ttf",
                                     "si": "C:/Windows/Fonts/georgiaz.ttf", "n": "C:/Windows/Fonts/georgia.ttf"}[estilo],
                                    int(tam))
    return _fc[k]


def _limpia(s):
    return s.replace("·", "/")                       # Arial Rounded no trae el punto medio


def _ancho(s, f):
    return _D.textlength(_limpia(s).replace("*", ""), font=f)


def _txt(d, xy, s, f, color, ancla="la", alfa=255, borde=0, track=0):
    s = _limpia(s)
    a = int(max(0, min(255, alfa)))
    if a <= 0:
        return
    if track:
        x = xy[0]
        tot = sum(d.textlength(c, font=f) for c in s) + track * (len(s) - 1)
        if ancla[0] == "m":
            x -= tot / 2
        for c in s:
            _txt(d, (x, xy[1]), c, f, color, "l" + ancla[1], alfa, borde)
            x += d.textlength(c, font=f) + track
        return
    d.text((xy[0] + 2, xy[1] + 3), s, font=f, fill=(0, 0, 0, int(a * .55)), anchor=ancla, stroke_width=borde,
           stroke_fill=(0, 0, 0, int(a * .55)))
    d.text(xy, s, font=f, fill=tuple(color) + (a,), anchor=ancla, stroke_width=borde, stroke_fill=(0, 0, 0, a))


def ajustar(s, estilo, tam, ancho, minimo=14):
    while tam > minimo and _ancho(s, fuente(estilo, tam)) > ancho:
        tam -= 1
    return fuente(estilo, tam)


def _partir(s, f, ancho):
    return G._partir(_D, _limpia(s), f, ancho)


def caja(s, estilo, tam, ancho, alto=10_000, interlinea=1.3, minimo=16, max_lineas=7):
    while True:
        f = fuente(estilo, tam)
        ls = _partir(s, f, ancho)
        lh = tam * interlinea
        if (len(ls) * lh <= alto and len(ls) <= max_lineas and max(_ancho(x, f) for x in ls) <= ancho) or tam <= minimo:
            return f, ls, lh
        tam -= 1


def _humo(w, h, M=46, alfa=.66, radio=34):
    """Cuadro negro translúcido de esquinas redondas con el borde difuminado (como el diálogo de N64)."""
    im = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((M, M, M + w, M + h), radio, fill=int(255 * alfa))
    m = m.filter(ImageFilter.GaussianBlur(7))
    capa = Image.new("RGBA", im.size, (6, 4, 14, 255))
    capa.putalpha(m)
    im.alpha_composite(capa)
    return im, M


def _filete(d, x0, x1, y, alfa=255, color=ROSA):
    """Separador fino: línea que se apaga en los extremos + rombo central amarillo (púas de la máscara)."""
    n = 40
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        k = math.sin(math.pi * (u0 + u1) / 2)
        d.line([(x0 + (x1 - x0) * u0, y), (x0 + (x1 - x0) * u1, y)], fill=color + (int(alfa * .85 * k),), width=2)
    cx = (x0 + x1) / 2
    d.polygon([(cx, y - 8), (cx + 8, y), (cx, y + 8), (cx - 8, y)], fill=AMARILLO + (int(alfa),))


def _flecha(d, x, y, dt, alfa=255):
    """Triángulo verde de «siguiente» del diálogo, que late."""
    k = .55 + .45 * math.sin(dt * 6)
    s = 13
    d.polygon([(x - s, y - s * .6), (x + s, y - s * .6), (x, y + s * .7)], fill=VERDE + (int(alfa * k),))


def _rica(d, x, y, s, f, color, resalte, alfa, ancla="l", hasta=None):
    """Línea con *resaltado*; `hasta` = caracteres visibles (efecto máquina de escribir del diálogo)."""
    trozos = s.split("*")
    tot = sum(d.textlength(t, font=f) for t in trozos)
    if ancla == "m":
        x -= tot / 2
    vis = 10 ** 9 if hasta is None else hasta
    for k, t in enumerate(trozos):
        if vis <= 0:
            break
        t2 = t[:max(0, int(vis))]
        if t2:
            _txt(d, (x, y), t2, f, resalte if k % 2 else color, "lm", alfa)
        x += d.textlength(t, font=f)
        vis -= len(t)


def _salida(im, dt, dur, abre=.3):
    """Entrada como el diálogo de N64: el cuadro se abre en vertical; salida con fundido."""
    u = _eo(dt / abre)
    if u < 1:
        W, H = im.size
        h = max(2, int(H * (.15 + .85 * u)))
        p = im.resize((W, h), Image.BICUBIC)
        out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        out.alpha_composite(p, (0, (H - h) // 2))
        im = out
    return _bgra(im, min(_eo(dt / .2), (dur - dt) / .35))


# ------------------------------------------------------------------ ficha = cuadro de diálogo
def ficha(titulo, texto, tipo=None, ancho=860, vel=55):
    """Cuadro de diálogo de N64: `titulo` arriba en amarillo (como el nombre de un objeto obtenido), `tipo` en gris
    claro cursiva, filete, y el texto que se ESCRIBE letra a letra (vel = letras/s). *x* = rosa (como los nombres)."""
    in_w = ancho - 2 * 46
    ft = ajustar(titulo.upper(), "d", 40, in_w)
    fty = ajustar(tipo, "si", 26, in_w) if tipo else None
    fx, ls, lh = caja(texto, "d", 34, in_w, max_lineas=7)
    h = int(34 + 48 + (34 if tipo else 0) + 26 + lh * len(ls) + 40)
    base, M = _humo(ancho, h)
    letras = [len(x.replace("*", "")) for x in ls]

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        cx = M + ancho / 2
        y = M + 40
        _txt(d, (cx, y), titulo.upper(), ft, AMARILLO, "mm", 255 * _eo((dt - .2) / .3), track=1)
        y += 40
        if tipo:
            _txt(d, (cx, y), tipo, fty, GRIS, "mm", 230 * _eo((dt - .3) / .3))
            y += 34
        _filete(d, M + 70, M + ancho - 70, y, 255 * _eo((dt - .3) / .4))
        y += 26 + lh / 2
        quedan = max(0.0, (dt - .45) * vel)
        for ln, n in zip(ls, letras):
            _rica(d, cx, y, ln, fx, BLANCO, ROSA, 255, "m", hasta=quedan)
            quedan -= n
            y += lh
        if quedan > 0:
            _flecha(d, M + ancho - 40, M + h - 26, dt)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ rótulo de secreto = cartel «Amanecer del primer día»
def puesto(num, titulo, arriba=None):
    """Banda de humo negro con, en serifa blanca, «SECRETO NÚMERO N» que se abre con tracking (como «Amanecer del primer
    día») y debajo el título entre guiones, más pequeño (como «-Quedan 72 horas-»)."""
    arriba = arriba or f"Secreto número {num}"
    w = 1500
    f1 = ajustar(arriba, "s", 76, w - 160)
    f2 = ajustar(f"-{titulo}-", "si", 44, w - 200)
    h = 220

    def fn(dt, dur, marcas):
        im, M = _humo(w, h, alfa=.58, radio=60)
        d = ImageDraw.Draw(im)
        cx = M + w / 2
        u = _eo((dt - .05) / .9)
        _txt(d, (cx, M + 82), arriba, f1, BLANCO, "mm", 255 * u, track=int(26 * (1 - u)) + 2)
        _filete(d, cx - 300 * u, cx + 300 * u, M + 136, 255 * u)
        _txt(d, (cx, M + 176), f"-{titulo}-", f2, CREMA, "mm", 255 * _eo((dt - .55) / .5))
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .5))
    return fn


# ------------------------------------------------------------------ reloj de tres días
def _sol(d, x, y, r, alfa):
    for k in range(12):
        a = k * math.pi / 6
        d.line([(x + math.cos(a) * r * 1.2, y + math.sin(a) * r * 1.2), (x + math.cos(a) * r * 1.65, y + math.sin(a) * r * 1.65)],
               fill=AMARILLO + (int(alfa),), width=4)
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 180, 40, int(alfa)), outline=AMARILLO + (int(alfa),), width=3)


def _luna(d, x, y, r, alfa):
    d.ellipse((x - r, y - r, x + r, y + r), fill=(220, 200, 150, int(alfa)))
    d.ellipse((x - r * .55, y - r * .35, x - r * .2, y - r * .05), fill=(120, 30, 30, int(alfa)))
    d.ellipse((x + r * .2, y - r * .35, x + r * .55, y - r * .05), fill=(120, 30, 30, int(alfa)))
    d.arc((x - r * .5, y + r * .05, x + r * .5, y + r * .6), 200, 340, fill=(80, 20, 20, int(alfa)), width=4)


def reloj(titulo, pasos, w=1100):
    """El reloj del HUD de Majora: arco con 24 marcas, un sol (o la luna, de noche) que lo recorre, el día en grande y las
    horas que quedan. pasos = [(dia, horas_que_quedan, texto)]; marca k = paso k (el contador baja hasta él)."""
    h = 470
    fd, fh, ft = fuente("s", 64), fuente("d", 40), fuente("d", 32)
    ftit = ajustar(titulo.upper(), "d", 34, w - 120)

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        cx, cy, R = M + w / 2, M + 330, 250
        _txt(d, (cx, M + 34), titulo.upper(), ftit, AMARILLO, "mm", 255 * _eo(dt / .4), track=2)
        k = 0
        for i, m in enumerate(marcas or [0]):
            if dt >= m:
                k = i
        k = min(k, len(pasos) - 1)
        m0 = (marcas or [0])[k]
        dia, horas, texto = pasos[k]
        h_prev = pasos[k - 1][1] if k else horas
        u = _eo((dt - m0) / 1.2)
        hv = h_prev + (horas - h_prev) * u
        # arco
        for j in range(25):
            a = math.pi + math.pi * j / 24
            r0, r1 = (R - 18, R) if j % 6 else (R - 34, R)
            d.line([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * r1, cy + math.sin(a) * r1)],
                   fill=CREMA + (200,), width=3 if j % 6 else 5)
        d.arc((cx - R, cy - R, cx + R, cy + R), 180, 360, fill=MORADO + (220,), width=6)
        hora = (6 + (72 - hv)) % 24                      # el ciclo empieza a las 6:00 del primer día
        de_dia = 6 <= hora < 18
        frac = ((hora - 6) if de_dia else ((hora - 18) % 24)) / 12
        a = math.pi + math.pi * frac
        sx, sy = cx + math.cos(a) * (R - 62), cy + math.sin(a) * (R - 62)
        (_sol if de_dia else _luna)(d, sx, sy, 22, 255)
        _txt(d, (cx, cy - 92), dia, fd, BLANCO, "mm", 255)
        col = ROJO if hv <= 6 else BLANCO
        _txt(d, (cx, cy - 26), f"Quedan {int(round(hv))} horas", fh, col, "mm", 255)
        _txt(d, (cx, cy + 30), texto, ajustar(texto, "d", 32, w - 160), CREMA, "mm", 255 * _eo((dt - m0 - .3) / .4))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ el bucle de los tres días
def ciclo(pasos, centro="", titulo=None, w=1500, h=640):
    """pasos = [texto] alrededor de un óvalo (5 típicos: Día 1, Día 2, Día 3, la luna cae, Canción del Tiempo); marca k
    enciende el paso k y la flecha que lo une al anterior; el último vuelve al primero (flecha rosa). `centro` en medio."""
    n = len(pasos)
    fp = fuente("d", 34)
    fc = ajustar(centro, "s", 50, w * .42) if centro else None

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        cx, cy, rx, ry = M + w / 2, M + h / 2 + (16 if titulo else 0), w * .38, h * .33
        if titulo:
            _txt(d, (cx, M + 36), titulo.upper(), ajustar(titulo.upper(), "d", 32, w - 100), AMARILLO, "mm", 255, track=2)
        pos = [(cx + rx * math.cos(-math.pi / 2 + 2 * math.pi * i / n), cy + ry * math.sin(-math.pi / 2 + 2 * math.pi * i / n))
               for i in range(n)]
        mk = list(marcas or [i * .9 for i in range(n)])
        while len(mk) < n:
            mk.append(mk[-1] + .9)
        for i in range(n):                               # primero los caminos, luego las píldoras encima
            u = _eo((dt - mk[i]) / .5)
            if u <= 0:
                continue
            j = (i - 1) % n
            if i or dt >= mk[-1] + .6:                   # la flecha del último al primero sale al final
                uu = u if i else _eo((dt - mk[-1] - .6) / .6)
                a0 = -math.pi / 2 + 2 * math.pi * j / n
                a1 = -math.pi / 2 + 2 * math.pi * (i if i else n) / n
                pts = [(cx + rx * math.cos(a0 + (a1 - a0) * t / 30), cy + ry * math.sin(a0 + (a1 - a0) * t / 30))
                       for t in range(int(30 * uu) + 1)]
                if len(pts) > 1:
                    d.line(pts, fill=(ROSA if i == 0 else CREMA) + (230,), width=5)
        for i in range(n):
            u = _eo((dt - mk[i]) / .5)
            if u <= 0:
                continue
            x, y = pos[i]
            tw = _ancho(pasos[i], fp) + 44
            col = ROJO if "luna" in pasos[i].lower() else (ROSA if i == n - 1 else BLANCO)
            d.rounded_rectangle((x - tw / 2, y - 32, x + tw / 2, y + 32), 28, fill=(16, 6, 26, int(245 * u)),
                                outline=col + (int(255 * u),), width=3)
            _txt(d, (x, y), pasos[i], fp, col, "mm", 255 * u)
        if fc:
            _txt(d, (cx, cy), centro, fc, AMARILLO, "mm", 255 * _eo((dt - mk[-1] - 1.0) / .5))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ cuaderno de los Bombers (horarios)
def horario(titulo, dias, filas, w=1640):
    """dias = ["Día 1", "Día 2", "Día 3"]; filas = [(nombre, [(dia_idx, texto), ...])]; marca k = la cita k (en orden de
    la lista aplanada) cae en su casilla. Columnas del cuaderno de los Bombers con el humo translúcido."""
    citas = [(fi, di, tx) for fi, (_, cs) in enumerate(filas) for di, tx in cs]
    fn_, fd, fx = fuente("d", 34), fuente("s", 38), fuente("d", 26)
    col0 = 260
    cw = (w - 80 - col0) / len(dias)
    rh = 120
    h = 150 + rh * len(filas) + 30

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        _txt(d, (M + w / 2, M + 40), titulo.upper(), ajustar(titulo.upper(), "d", 34, w - 100), AMARILLO, "mm", 255, track=2)
        x0, y0 = M + 40 + col0, M + 92
        for i, dia in enumerate(dias):
            _txt(d, (x0 + cw * i + cw / 2, y0 + 14), dia, fd, BLANCO, "mm", 255 * _eo((dt - .1 * i) / .4))
            d.line([(x0 + cw * i, y0 + 40), (x0 + cw * i, M + h - 30)], fill=CREMA + (90,), width=2)
        for r, (nombre, _) in enumerate(filas):
            y = y0 + 54 + rh * r + rh / 2
            _txt(d, (M + 60, y), nombre, ajustar(nombre, "d", 34, col0 - 30), ROSA, "lm", 255 * _eo((dt - .2) / .4))
            d.line([(M + 40, y + rh / 2), (M + w - 40, y + rh / 2)], fill=CREMA + (60,), width=1)
        mk = list(marcas or [.6 + i * .8 for i in range(len(citas))])
        while len(mk) < len(citas):
            mk.append(mk[-1] + .8)
        for (fi, di, tx), m in zip(citas, mk):
            u = _eo((dt - m) / .4)
            if u <= 0:
                continue
            y = y0 + 54 + rh * fi + rh / 2
            x = x0 + cw * di + cw / 2
            f, ls, lh = caja(tx, "d", 26, cw - 30, rh - 16, max_lineas=3)
            bw = max(_ancho(l_, f) for l_ in ls) + 30
            d.rounded_rectangle((x - bw / 2, y - lh * len(ls) / 2 - 8, x + bw / 2, y + lh * len(ls) / 2 + 8), 14,
                                fill=(MORADO[0], MORADO[1], MORADO[2], int(150 * u)), outline=AMARILLO + (int(200 * u),), width=2)
            for k, l_ in enumerate(ls):
                _txt(d, (x, y - lh * (len(ls) - 1) / 2 + lh * k), l_, f, BLANCO, "mm", 255 * u)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ rejilla de máscaras
def rejilla(titulo, n=24, cols=6, remate=None, icono=None, iconos=(), w=1100):
    """n casillas (la pantalla de máscaras es de 6 x 4) que se llenan en barrido entre la marca 0 y la 1 con un contador
    «k / n» (con `iconos` = rutas de las máscaras REALES, cada casilla enseña la suya; si no, un rombo); en la marca 2,
    `icono` (imagen real) aparece grande en el centro y `remate` debajo."""
    filas_ = math.ceil(n / cols)
    T, G_ = 96, 18
    h = 120 + filas_ * (T + G_) + (90 if remate else 30)
    ic = None
    if icono and os.path.exists(icono):
        ic = Image.open(icono).convert("RGBA")
        ic.thumbnail((380, 380))
    mini = []
    for r in iconos:
        p = Image.open(r).convert("RGBA")
        if p.getbbox():
            p = p.crop(p.getbbox())
        k = (T - 16) / max(p.size)                       # los íconos de 32 px suben con NEAREST (píxel nítido del menú)
        p = p.resize((max(1, int(p.width * k)), max(1, int(p.height * k))), Image.NEAREST if k > 1.5 else Image.LANCZOS)
        mini.append(p)

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        mk = list(marcas or [0, 2.5, 4])
        while len(mk) < 3:
            mk.append(mk[-1] + 1.5)
        _txt(d, (M + w / 2, M + 40), titulo.upper(), ajustar(titulo.upper(), "d", 34, w - 100), AMARILLO, "mm", 255, track=2)
        x0 = M + (w - (cols * T + (cols - 1) * G_)) / 2
        y0 = M + 90
        u = max(0.0, min(1.0, (dt - mk[0]) / max(.5, mk[1] - mk[0])))
        llenas = int(u * n + .001)
        for i in range(n):
            x, y = x0 + (i % cols) * (T + G_), y0 + (i // cols) * (T + G_)
            on = i < llenas
            d.rounded_rectangle((x, y, x + T, y + T), 16, fill=(MORADO + (170,)) if on else (30, 20, 40, 140),
                                outline=(AMARILLO if on else CREMA) + (230 if on else 90,), width=3)
            if on and i < len(mini):
                p = mini[i]
                im.alpha_composite(p, (int(x + (T - p.width) / 2), int(y + (T - p.height) / 2)))
            elif on:
                c = x + T / 2, y + T / 2
                d.polygon([(c[0], c[1] - 26), (c[0] + 26, c[1]), (c[0], c[1] + 26), (c[0] - 26, c[1])], fill=ROSA + (230,))
        _txt(d, (M + w - 60, M + 40), f"{llenas}/{n}", fuente("d", 34), BLANCO, "rm", 255)
        if dt >= mk[2]:
            v = _reb((dt - mk[2]) / .5)
            # velo para que la máscara final destaque sobre la rejilla
            velo = Image.new("RGBA", im.size, (0, 0, 0, 0))
            ImageDraw.Draw(velo).rounded_rectangle((M, M + 70, M + w, M + h - 10), 30, fill=(4, 2, 10, int(150 * min(1, v))))
            im.alpha_composite(velo)
            d = ImageDraw.Draw(im)
            if ic is not None:
                p = ic.resize((max(2, int(ic.width * v)), max(2, int(ic.height * v))), Image.BICUBIC)
                im.alpha_composite(p, (int(M + w / 2 - p.width / 2), int(M + 90 + (filas_ * (T + G_)) / 2 - p.height / 2)))
            if remate:
                _txt(d, (M + w / 2, M + h - 52), remate, ajustar(remate, "s", 46, w - 100), AMARILLO, "mm",
                     255 * _eo((dt - mk[2] - .3) / .4))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ almas: persona -> máscara
def _recorte(ruta, lado):
    im = Image.open(ruta).convert("RGBA")
    im.thumbnail((lado, lado))
    out = Image.new("RGBA", (lado, lado), (0, 0, 0, 0))
    out.alpha_composite(im, ((lado - im.width) // 2, (lado - im.height) // 2))
    return out


def almas(titulo, items, w=1640):
    """items = [(ruta_persona, ruta_mascara, nombre, destino)]; marca k = la columna k: el retrato real aparece, se funde
    en su máscara (destello rosa) y debajo salen el nombre y su destino. Hasta 3-4 columnas."""
    n = len(items)
    L = 300
    h = 120 + L + 150
    caras = [(_recorte(a, L), _recorte(b, L)) for a, b, _, _ in items]
    fnom, fdes = fuente("d", 36), fuente("d", 26)

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        _txt(d, (M + w / 2, M + 40), titulo.upper(), ajustar(titulo.upper(), "d", 34, w - 100), AMARILLO, "mm", 255, track=2)
        mk = list(marcas or [.4 + i * 2.2 for i in range(n)])
        while len(mk) < n:
            mk.append(mk[-1] + 2.2)
        paso = w / n
        for i, ((pa, pb), (_, _, nombre, destino), m) in enumerate(zip(caras, items, mk)):
            if dt < m:
                continue
            cx = M + paso * i + paso / 2
            u = _eo((dt - m) / .4)
            fu = max(0.0, min(1.0, (dt - m - .9) / .7))       # fundido persona -> máscara
            cara = Image.blend(pa, pb, fu)
            if 0 < fu < 1:
                g = Image.new("RGBA", cara.size, ROSA + (int(120 * math.sin(math.pi * fu)),))
                g.putalpha(Image.fromarray((np.array(cara)[..., 3] * .5 * math.sin(math.pi * fu)).astype(np.uint8)))
                cara.alpha_composite(g)
            cara = _escala(cara, .7 + .3 * _reb((dt - m) / .45))
            im.alpha_composite(_alfa(cara, u), (int(cx - L / 2), int(M + 86)))
            d = ImageDraw.Draw(im)
            _txt(d, (cx, M + 86 + L + 36), nombre, ajustar(nombre, "d", 36, paso - 40), ROSA, "mm", 255 * _eo((dt - m - 1.2) / .4))
            f, ls, lh = caja(destino, "d", 26, paso - 50, 90, max_lineas=3)
            for k, l_ in enumerate(ls):
                _txt(d, (cx, M + 86 + L + 78 + lh * k), l_, f, BLANCO, "mm", 255 * _eo((dt - m - 1.4) / .4))
        return _salida(im, dt, dur)
    return fn


def _alfa(p, k):
    if k >= 1:
        return p
    a = np.array(p)
    a[..., 3] = (a[..., 3] * max(0.0, k)).astype(np.uint8)
    return Image.fromarray(a)


# ------------------------------------------------------------------ pegatina
def pegatina(ruta, titulo=None, tam=360, giro=-6.0):
    """Imagen REAL recortada con borde blanco (mg_tes) que entra con rebote, se balancea y flota; el nombre en una píldora
    negra translúcida con filo rosa y letra del diálogo de N64."""
    import mg_tes as T
    base = T._base_pegatina(ruta, tam)
    if titulo:
        tit = _limpia(titulo.upper())
        f = ajustar(tit, "d", 30, max(260, base.width + 40))
        pw, ph = int(_ancho(tit, f) + 56), 62
        pil = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        dp = ImageDraw.Draw(pil)
        dp.rounded_rectangle((0, 0, pw - 1, ph - 1), ph // 2, fill=(10, 4, 20, 190), outline=ROSA + (230,), width=3)
        _txt(dp, (pw / 2, ph / 2 + 1), tit, f, BLANCO, "mm", 255)
        lien = Image.new("RGBA", (max(base.width, pw), base.height + ph // 2), (0, 0, 0, 0))
        lien.alpha_composite(base, ((lien.width - base.width) // 2, 0))
        lien.alpha_composite(pil, ((lien.width - pw) // 2, base.height - ph // 2))
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
