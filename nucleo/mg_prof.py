# -*- coding: utf-8 -*-
"""MOTION GRAPHICS de PROFESIONES con la interfaz de WoW (panel azul noche y borde dorado de mg_wow), hechos para
«La RUTA de PROFESIONES del 1 al 300 en WoW Forever» (wow_ruta_profesiones, 25-nov-2026). Sirven a cualquier guía de
profesiones de WoW. CERO cifras inventadas: solo números que el guion dice. Uso en efectos.py igual que mg_wow
(fn(dt, dur, marcas) -> BGRA); imágenes = nombre de ícono de Wowhead o ruta de una pegatina PNG/JPG.
  habilidad(n, nombre, ico, tramos, nota)        tarjeta de capítulo «PARADA n»: barra de habilidad 1-300 con los 4 rangos
                                                 (aprendiz/oficial/experto/artesano); marca 0 = barra; marca k = tramo k
                                                 [(a, b, «texto»)] que se enciende con su rótulo (filas alternas); len+1 = nota
  rangos(titulo, rangos, total, niveles)         los 4 rangos con su coste en monedas (cobre/plata/oro) uno por marca, el
                                                 total y luego el nivel que pide cada uno; marcas: 4 costes, total, 3 niveles
  barras(titulo, ico, minimo, maximo, unidad, nota)  montón de barras que crece: el contador llega a `minimo` (marca 0, verde),
                                                 sigue hasta `maximo` (marca 1, rojo) y la franja entre los dos = nota (marca 2)
  telar(titulo, ico, pide, solo, salidas)        la trampa circular: «las recetas 285-300 piden TELAR» ⇄ «el TELAR solo con
                                                 300» con un candado; marca 0 = receta, 1 = telar y bucle, 2.. = salidas
  campamento(titulo, hogueras, objetos, nota)    hoguera con llama y anillo de casillas; marca 0 = hoguera; marca k = hoguera
                                                 k (3/5/10 casillas) y los objetos que se suman; len+1 = nota
  legado(titulo, profs, hitos, total, ceros)     6 profesiones × 3 hitos (150/225/300): cada columna en su marca y el contador
                                                 hasta `total`; marca 4 = fila de las que no dan (0)
  flujo(titulo, nodos, aristas, remate)          árbol de materiales: nodos [(col, fila, img, texto)] que se encienden en su
                                                 marca y flechas desde sus padres; remate en la última marca
  traspaso(titulo, img, de, a, nota)             un objeto que se muda de profesión: estaba en `de`, vuela a `a` y `de` se tacha
                                                 (marca 0 = los dos, 1 = vuelo, 2 = nota)
  bolsas(titulo, bolsas, nota)                   bolsas con su rejilla de casillas (6/8/12/14…) una por marca; nota al final
Prueba: python nucleo/mg_prof.py [i …] → %TEMP%/_mg_prof_pruebaN.jpg (cuadro final de cada uno; MÍRALOS).
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter

from mg_wow import (BLANCO, GRIS, ORO, ORO_T, VERDE, _base, _eo, _mk, _pegar, _pop, _salida, _sello, _texto, fuente,
                    icono)
from mg_wow60 import _img, _marca_ok

ROJO = (235, 60, 50)
AZUL = (70, 140, 255)
COBRE, PLATA = (200, 120, 60), (200, 205, 215)
RANGOS = (("APRENDIZ", 1, 75), ("OFICIAL", 75, 150), ("EXPERTO", 150, 225), ("ARTESANO", 225, 300))


def _encaja(d, s, nombre, tam, ancho):
    while tam > 14 and d.textlength(s, font=fuente(nombre, tam)) > ancho:
        tam -= 2
    return fuente(nombre, tam)


def _capa(im):
    return Image.new("RGBA", im.size, (0, 0, 0, 0))


def _brillo(im, caja, color, r=10, ancho=8, blur=6, alfa=200):
    """Halo difuso alrededor de una caja (capa aparte: ImageDraw no mezcla el alfa)."""
    g = _capa(im)
    ImageDraw.Draw(g).rounded_rectangle(caja, r, outline=tuple(color) + (alfa,), width=ancho)
    im.alpha_composite(g.filter(ImageFilter.GaussianBlur(blur)))


def _flecha(d, a, b, q, color, w=6, punta=16):
    """Flecha de a a b dibujada hasta la fracción q."""
    if q <= 0:
        return
    x = a[0] + (b[0] - a[0]) * q
    y = a[1] + (b[1] - a[1]) * q
    d.line([a, (x, y)], fill=tuple(color) + (255,), width=w)
    if q >= .99:
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        p1 = (b[0] - punta * math.cos(ang - .45), b[1] - punta * math.sin(ang - .45))
        p2 = (b[0] - punta * math.cos(ang + .45), b[1] - punta * math.sin(ang + .45))
        d.polygon([b, p1, p2], fill=tuple(color) + (255,))


def _moneda(d, cx, cy, r, color, a=255):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=tuple(color) + (int(a),), outline=(40, 30, 10, int(a)), width=2)
    d.ellipse((cx - r * .55, cy - r * .55, cx + r * .1, cy + r * .1), fill=(255, 255, 255, int(a * .35)))


# ------------------------------------------------------------------ tarjeta de capítulo: barra de habilidad 1-300
def habilidad(n, nombre, ico, tramos, nota=None, ancho=1560):
    """tramos = [(a, b, texto), ...] (≤ 6); rótulos en dos filas alternas para que no se pisen."""
    h = 470 + (54 if nota else 0)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, f"PARADA {n}")
        d = ImageDraw.Draw(im)
        cx = M + ancho / 2
        a0 = _eo(dt / .35)
        f = _encaja(d, nombre, "negra", 58, ancho - 400)
        tw = d.textlength(nombre, font=f)
        _pegar(im, _img(ico, 70), cx - tw / 2 - 52, M + 104, _pop(dt, .4))
        d = ImageDraw.Draw(im)
        _texto(d, (cx - tw / 2 + 0, M + 104), nombre, f, BLANCO, "lm", 255 * a0)
        x0, x1, yb = M + 90, M + ancho - 90, M + 300
        X = lambda v: x0 + (x1 - x0) * (v - 1) / 299
        d.rounded_rectangle((x0, yb - 16, x1, yb + 16), 14, fill=(6, 8, 22, 240), outline=ORO + (200,), width=2)
        for k, (rn, ra, rb) in enumerate(RANGOS):       # los 4 rangos debajo de la barra
            xa, xb = X(ra), X(rb)
            if k:
                d.line([(xa, yb - 22), (xa, yb + 22)], fill=ORO_T + (230,), width=3)
            _texto(d, ((xa + xb) / 2, yb + 44), rn, fuente("sans", 24), GRIS, "mm", 230 * a0)
        for v in (1, 75, 150, 225, 300):
            _texto(d, (X(v), yb + 76), str(v), fuente("serif", 24), ORO_T, "mm", 220 * a0)
        t0 = _mk(marcas, 0, .4)
        for k, (a, b, s) in enumerate(tramos):
            tk = _mk(marcas, 1 + k, t0 + .8 + k * .9)
            if dt < tk:
                continue
            u = dt - tk
            q = _eo(u / .6)
            xa, xb = X(a), X(b)
            col = ORO_T if k % 2 == 0 else (240, 170, 40)
            d.rounded_rectangle((xa + 1, yb - 13, xa + max(8, (xb - xa) * q) - 1, yb + 13), 11, fill=col + (255,))
            fila = k % 2
            yt = yb - 50 - fila * 44
            w_max = max(150, (xb - xa) * 2.0)
            ft = _encaja(d, s, "negra", 28, w_max)
            xm = min(max((xa + xb) / 2, x0 + d.textlength(s, font=ft) / 2), x1 - d.textlength(s, font=ft) / 2)
            d.line([((xa + xb) / 2, yb - 16), ((xa + xb) / 2, yt + 16)], fill=col + (int(200 * q),), width=2)
            _texto(d, (xm, yt), s, ft, BLANCO if k == len(tramos) - 1 or dt < _mk(marcas, 2 + k, 1e9) else (200, 200, 210),
                   "mm", 255 * q)
            _texto(d, ((xa + xb) / 2, yb), f"{a}-{b}", fuente("negra", 18), (30, 22, 8), "mm", 255 * _eo((u - .4) / .3))
        tn = _mk(marcas, 1 + len(tramos), 1e9)
        if nota and dt >= tn:
            _texto(d, (cx, M + h - 44), nota, _encaja(d, nota, "serif", 34, ancho - 120), VERDE, "mm", 255 * _eo((dt - tn) / .3))
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ los 4 rangos: coste y nivel
def rangos(titulo, costes, total=None, niveles=None, ancho=1600):
    """costes = [(cantidad, «cobre»|«plata»|«oro»), ...] × 4 · total = texto · niveles = [None, 10, 20, 35]."""
    h = 480
    col = dict(cobre=COBRE, plata=PLATA, oro=ORO_T)
    abre = dict(cobre="c", plata="p", oro="o")

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        w = (ancho - 80 - 3 * 30) / 4
        for k, (rn, ra, rb) in enumerate(RANGOS):
            x = M + 40 + k * (w + 30)
            y = M + 96
            tk = _mk(marcas, k, .4 + k * .8)
            on = dt >= tk
            d.rounded_rectangle((x, y, x + w, y + 210), 14, fill=(4, 6, 18, 235),
                                outline=(ORO if on else (80, 70, 40)) + (255,), width=3 if on else 2)
            _texto(d, (x + w / 2, y + 34), rn, fuente("negra", 32), ORO_T if on else GRIS, "mm", 255)
            _texto(d, (x + w / 2, y + 72), f"{ra}-{rb}", fuente("serif", 26), BLANCO if on else GRIS, "mm", 230)
            if on:
                u = dt - tk
                cant, met = costes[k]
                s = _pop(u, .35)
                r = 26 * s
                _moneda(d, x + w / 2 - 64, y + 140, r, col[met], 255 * _eo(u / .2))
                _texto(d, (x + w / 2 - 26, y + 140), f"{cant} {abre[met]}", fuente("negra", int(max(8, 48 * min(1.0, s)))),
                       col[met], "lm", 255 * _eo(u / .25))
            if niveles and niveles[k]:
                tl = _mk(marcas, 5 + sum(1 for v in niveles[:k] if v), 1e9)
                if dt >= tl:
                    u = dt - tl
                    _texto(d, (x + w / 2, y + 250), f"pide nivel {niveles[k]}", fuente("sans", 30), AZUL, "mm", 255 * _eo(u / .3))
                    _brillo(im, (x, y, x + w, y + 210), AZUL, 14, 6, 5, int(160 * max(0.0, 1 - u / 1.2)))
                    d = ImageDraw.Draw(im)
        tt = _mk(marcas, 4, 1e9)
        if total and dt >= tt:
            u = dt - tt
            _texto(d, (M + ancho / 2, M + h - 40), total, fuente("negra", int(max(8, 40 * _pop(u, .35)))), VERDE, "mm")
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ las barras que se come el último tramo
def barras(titulo, ico, minimo, maximo, unidad="barras", nota=None, ancho=1500, por_ico=25):
    n_tot = int(math.ceil(maximo / por_ico))
    cols = 16
    T = int((ancho - 120) / cols) - 6
    h = 100 + int(math.ceil(n_tot / cols)) * (T + 6) + 150

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        t0, t1 = _mk(marcas, 0, .4), _mk(marcas, 1, 2.6)
        u0 = _eo((dt - t0) / 1.4)
        u1 = _eo((dt - t1) / 1.4) if dt >= t1 else 0.0
        v = minimo * u0 + (maximo - minimo) * u1
        k_on = int(v / por_ico + .5)
        ic = _img(ico, T)
        filas = int(math.ceil(n_tot / cols))
        y0 = M + 100
        for i in range(n_tot):
            fx, fy = i % cols, i // cols
            x = M + 60 + fx * (T + 6)
            y = y0 + (filas - 1 - fy) * (T + 6)
            if i < k_on:
                extra = i * por_ico >= minimo
                im.alpha_composite(ic, (int(x), int(y)))
                if extra:
                    d.rectangle((x, y, x + T - 1, y + T - 1), outline=ROJO + (255,), width=2)
            else:
                d.rectangle((x, y, x + T - 1, y + T - 1), outline=(60, 55, 40, 200), width=1)
        yb = y0 + filas * (T + 6) + 36
        x0, x1 = M + 60, M + ancho - 60
        d.rounded_rectangle((x0, yb - 10, x1, yb + 10), 9, fill=(6, 8, 22, 240), outline=ORO + (200,), width=2)
        xm = x0 + (x1 - x0) * minimo / maximo
        xv = x0 + (x1 - x0) * v / maximo
        if v > 0:
            d.rounded_rectangle((x0 + 2, yb - 8, max(x0 + 10, min(xv, xm)), yb + 8), 8, fill=VERDE + (255,))
        if v > minimo:
            d.rounded_rectangle((xm, yb - 8, max(xm + 6, xv), yb + 8), 8, fill=ROJO + (255,))
        if dt >= t0:
            _texto(d, (xm, yb + 36), f"{minimo}", fuente("negra", 30), VERDE, "mm", 255 * u0)
        if dt >= t1:
            _texto(d, (x1, yb + 36), f"{maximo}", fuente("negra", 30), ROJO, "rm", 255 * _eo((dt - t1) / .3))
        col = ROJO if v > minimo + 1 else (VERDE if dt >= t0 + 1.4 else BLANCO)
        _texto(d, (x0, yb + 80), f"{int(round(v))} {unidad}", fuente("negra", 44), col, "lm", 255 * _eo(dt / .3))
        tn = _mk(marcas, 2, 1e9)
        if nota and dt >= tn:
            u = dt - tn
            _texto(d, ((xm + x1) / 2, yb + 80), nota, _encaja(d, nota, "serif", 34, (x1 - xm) * .9), ORO_T, "mm", 255 * _eo(u / .3))
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ la trampa del telar: 300 ⇄ 300
def telar(titulo, ico, pide, solo, salidas=(), ancho=1560):
    """pide = («LAS RECETAS 285-300», «PIDEN UN TELAR») · solo = («EL TELAR», «SOLO LO FABRICA QUIEN TIENE 300») ·
    salidas = [texto, ...] (las salidas verdes, una por marca 2..)."""
    h = 470 + (70 if salidas else 0)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        cy = M + 250
        xa, xb = M + 330, M + ancho - 330
        t0, t1 = _mk(marcas, 0, .4), _mk(marcas, 1, 2.0)
        for k, (cx, (l1, l2), tk) in enumerate(((xa, pide, t0), (xb, solo, t1))):
            if dt < tk:
                continue
            u = dt - tk
            q = _pop(u, .35)
            w, hh = 470 * q, 220 * q
            d.rounded_rectangle((cx - w / 2, cy - hh / 2, cx + w / 2, cy + hh / 2), 16, fill=(4, 6, 18, 240),
                                outline=ORO + (255,), width=3)
            if q > .9:
                _pegar(im, _img(ico, 92), cx, cy - 46, 1.0, _eo(u / .3))
                d = ImageDraw.Draw(im)
                _texto(d, (cx, cy + 32), l1, _encaja(d, l1, "negra", 34, 440), BLANCO, "mm", 255 * _eo(u / .3))
                _texto(d, (cx, cy + 74), l2, _encaja(d, l2, "sans", 26, 440), ORO_T, "mm", 255 * _eo(u / .3))
        if dt >= t1 + .3:                               # el bucle: dos arcos que giran sin fin y el candado
            u = dt - t1 - .3
            q = _eo(u / .6)
            r = (xb - xa) / 2 - 250
            mx = (xa + xb) / 2
            capa = _capa(im)
            dc = ImageDraw.Draw(capa)
            for s, ang0 in ((-1, 0), (1, 180)):
                for j in range(5):
                    a = ang0 + 200 + j * 28 + (u * 90) % 28
                    a0, a1 = a, a + 16
                    dc.arc((mx - r, cy - r * .7, mx + r, cy + r * .7), a0, a1, fill=ROJO + (int(255 * q),), width=8)
            im.alpha_composite(capa)
            d = ImageDraw.Draw(im)
            # candado
            pulso = 1 + .06 * math.sin(u * 6)
            lw, lh = 64 * pulso, 54 * pulso
            d.arc((mx - lw * .34, cy - lh * 1.05, mx + lw * .34, cy - lh * .1), 180, 360, fill=ROJO + (int(255 * q),), width=9)
            d.rounded_rectangle((mx - lw / 2, cy - lh / 2, mx + lw / 2, cy + lh / 2), 8, fill=ROJO + (int(255 * q),))
            d.ellipse((mx - 7, cy - 9, mx + 7, cy + 5), fill=(30, 10, 10, int(255 * q)))
            f3 = fuente("negra", 34)                    # «300 ⇄ 300» con flechas dibujadas (la fuente no trae ⇄)
            _texto(d, (mx - 60, cy + 64), "300", f3, ROJO, "rm", 255 * q)
            _texto(d, (mx + 60, cy + 64), "300", f3, ROJO, "lm", 255 * q)
            _flecha(d, (mx - 44, cy + 56), (mx + 44, cy + 56), q, ROJO, 4, 12)
            _flecha(d, (mx + 44, cy + 74), (mx - 44, cy + 74), q, ROJO, 4, 12)
        for k, s in enumerate(salidas):
            tk = _mk(marcas, 2 + k, 1e9)
            if dt < tk:
                continue
            u = dt - tk
            x = M + ancho * (.30 if k == 0 else .70) if len(salidas) > 1 else M + ancho / 2
            yy = M + h - 70
            _flecha(d, ((M + ancho / 2), cy + 96), (x, yy - 34), _eo(u / .4), VERDE, 5, 16)
            _texto(d, (x, yy), s, _encaja(d, s, "negra", 32, ancho * .4), VERDE, "mm", 255 * _eo((u - .2) / .3))
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ el campamento: hoguera y objetos (3/5/10)
def campamento(titulo, hogueras, objetos, nota=None, ancho=1500):
    """hogueras = [(«BÁSICA», 3), («DE OFICIAL», 5), («DE EXPERTO», 10)] · objetos = íconos/pegatinas (≥ el máximo)."""
    h = 560
    nmax = max(nn for _, nn in hogueras)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        cx, cy = M + ancho * .36, M + 300
        t0 = _mk(marcas, 0, .4)
        if dt >= t0:                                  # la hoguera: leños y llama que baila (capa aparte)
            u = dt - t0
            q = _eo(u / .4)
            for s in (-1, 1):
                d.line([(cx - 60 * s, cy + 52), (cx + 60 * s, cy + 22)], fill=(110, 70, 35, int(255 * q)), width=16)
            fl = _capa(im)
            df = ImageDraw.Draw(fl)
            for j, (cc, esc) in enumerate((((255, 120, 20), 1.0), ((255, 190, 40), .72), ((255, 245, 170), .42))):
                hh = 120 * esc * (1 + .08 * math.sin(u * 9 + j)) * q
                ww = 70 * esc
                df.polygon([(cx - ww, cy + 30), (cx - ww * .5, cy - hh * .45), (cx + 4 * math.sin(u * 7 + j), cy - hh),
                            (cx + ww * .5, cy - hh * .4), (cx + ww, cy + 30)], fill=cc + (235,))
            im.alpha_composite(fl.filter(ImageFilter.GaussianBlur(3)))
            gl = _capa(im)
            ImageDraw.Draw(gl).ellipse((cx - 170, cy - 150, cx + 170, cy + 120), fill=(255, 140, 30, int(55 * q)))
            im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(40)))
            d = ImageDraw.Draw(im)
        # hoguera activa = la de la última marca alcanzada
        act, t_act = -1, None
        for k in range(len(hogueras)):
            tk = _mk(marcas, 1 + k, t0 + 1.0 + k * 1.4)
            if dt >= tk:
                act, t_act = k, tk
        R = 205
        T = 74
        if act >= 0:
            nn = hogueras[act][1]
            u = dt - t_act
            prev = hogueras[act - 1][1] if act > 0 else 0
            for i in range(nn):
                ang = -math.pi / 2 + 2 * math.pi * i / nn
                x, y = cx + R * math.cos(ang), cy - 10 + R * .78 * math.sin(ang)
                ui = u - max(0, i - prev) * .12 if i >= prev else 9
                s = _pop(ui, .3) if ui > 0 else 0
                d.rounded_rectangle((x - T / 2, y - T / 2, x + T / 2, y + T / 2), 9, fill=(4, 6, 18, 235), outline=ORO + (255,), width=2)
                if s > .02:
                    _pegar(im, _img(objetos[i % len(objetos)], T - 10), x, y, s)
                    d = ImageDraw.Draw(im)
        # lista de hogueras a la derecha
        xl = M + ancho * .70
        for k, (nom, nn) in enumerate(hogueras):
            tk = _mk(marcas, 1 + k, t0 + 1.0 + k * 1.4)
            yk = M + 150 + k * 100
            on = dt >= tk
            ak = 255 * _eo((dt - tk) / .3) if on else 90
            _texto(d, (xl, yk), f"HOGUERA {nom}", _encaja(d, f"HOGUERA {nom}", "negra", 30, ancho * .28), ORO_T if k == act else GRIS, "lm", ak)
            _texto(d, (xl, yk + 40), f"{nn} objetos", fuente("serif", 30), BLANCO if k == act else GRIS, "lm", ak)
            if k == act:
                d.polygon([(xl - 34, yk + 4), (xl - 16, yk + 18), (xl - 34, yk + 32)], fill=ORO_T + (255,))
        tn = _mk(marcas, 1 + len(hogueras), 1e9)
        if nota and dt >= tn:
            _texto(d, (M + ancho / 2, M + h - 40), nota, _encaja(d, nota, "negra", 36, ancho - 120), VERDE, "mm", 255 * _eo((dt - tn) / .3))
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ Legado: 6 profesiones × 3 hitos = 18 puntos
def legado(titulo, profs, hitos=(150, 225, 300), total=18, ceros=None, ancho=1500):
    """profs = [(img, nombre), ...] × 6 · ceros = [img, ...] (recolección y secundarias: 0 puntos) en la marca 4."""
    n = len(profs)
    FH = 66
    h = 140 + n * FH + (120 if ceros else 30)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        xn, xc0 = M + 140, M + 600
        wc = 190
        for j, ht in enumerate(hitos):
            _texto(d, (xc0 + j * wc, M + 104), str(ht), fuente("serif", 32), ORO_T, "mm", 255 * _eo(dt / .3))
        puntos = 0.0
        for i, (img, nom) in enumerate(profs):
            y = M + 150 + i * FH
            ai = _eo((dt - .1 - i * .06) / .3)
            _pegar(im, _img(img, 52), M + 90, y, 1.0, ai)
            d = ImageDraw.Draw(im)
            _texto(d, (xn, y), nom, fuente("sans", 30), BLANCO, "lm", 255 * ai)
            for j in range(len(hitos)):
                x = xc0 + j * wc
                tk = _mk(marcas, j, .6 + j * 1.0)
                u = dt - tk - i * .07
                d.ellipse((x - 20, y - 20, x + 20, y + 20), outline=(95, 82, 45, 255), width=3, fill=(4, 6, 18, 235))
                if u > 0:
                    s = _pop(u, .3)
                    r = 15 * s
                    d.ellipse((x - r, y - r, x + r, y + r), fill=ORO_T + (255,))
                    puntos += _eo(u / .3)
        tt = _mk(marcas, 3, 1e9)
        col = VERDE if dt >= tt else BLANCO
        ft = fuente("negra", int(64 * (1 + .25 * max(0.0, 1 - (dt - tt) / .4))) if dt >= tt else 64)
        _texto(d, (M + ancho - 90, M + 150 + (n - 1) * FH / 2), f"{int(round(min(total, puntos)))}", ft, col, "mm", 255)
        _texto(d, (M + ancho - 90, M + 150 + (n - 1) * FH / 2 + 56), "puntos", fuente("sans", 26), GRIS, "mm", 230)
        tz = _mk(marcas, 4, 1e9)
        if ceros and dt >= tz:
            u = dt - tz
            y = M + h - 70
            for k, img in enumerate(ceros):
                x = M + 120 + k * 76
                uk = u - k * .08
                if uk > 0:
                    _pegar(im, _img(img, 56, apagado=True), x, y, _pop(uk, .3))
            d = ImageDraw.Draw(im)
            x = M + 120 + len(ceros) * 76
            _texto(d, (x, y), "= 0 puntos", fuente("negra", 36), ROJO, "lm", 255 * _eo(u / .3))
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ árbol de materiales
def flujo(titulo, nodos, aristas, remate=None, ancho=1600, cols=None, filas=None):
    """nodos = [(col, fila, img, texto), ...] (nodo k en la marca k) · aristas = [(i, j), ...] (flecha de i a j cuando
    entra j) · remate = (texto, i_marca)."""
    nc = cols or (max(c for c, _, _, _ in nodos) + 1)
    nf = filas or (max(f for _, f, _, _ in nodos) + 1)
    FH = 150
    h = 110 + nf * FH + (96 if remate else 10)
    R = 46

    def pos(M, c, f):
        return M + 90 + (ancho - 180) * (c + .5) / nc, M + 110 + FH * (f + .4)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        tk = [_mk(marcas, k, .4 + k * .8) for k in range(len(nodos))]
        for i, j in aristas:
            if dt < tk[j]:
                continue
            (x0, y0), (x1, y1) = pos(M, *nodos[i][:2]), pos(M, *nodos[j][:2])
            ang = math.atan2(y1 - y0, x1 - x0)
            a = (x0 + (R + 10) * math.cos(ang), y0 + (R + 10) * math.sin(ang))
            b = (x1 - (R + 14) * math.cos(ang), y1 - (R + 14) * math.sin(ang))
            _flecha(d, a, b, _eo((dt - tk[j]) / .4), ORO_T, 5, 16)
        for k, (c, f, img, txt) in enumerate(nodos):
            if dt < tk[k]:
                continue
            u = dt - tk[k] - (.3 if any(j == k for _, j in aristas) else 0)
            if u <= 0:
                continue
            x, y = pos(M, c, f)
            s = _pop(u, .3)
            d.ellipse((x - R - 6, y - R - 6, x + R + 6, y + R + 6), fill=(4, 6, 18, 240), outline=ORO + (255,), width=3)
            _pegar(im, _img(img, 2 * R - 8), x, y, s)
            d = ImageDraw.Draw(im)
            _texto(d, (x, y + R + 28), txt, _encaja(d, txt, "sans", 26, (ancho - 180) / nc - 10), BLANCO, "mm", 255 * _eo(u / .3))
        if remate and dt >= _mk(marcas, remate[1], 1e9):
            u = dt - marcas[remate[1]]
            _texto(d, (M + ancho / 2, M + h - 36), remate[0], _encaja(d, remate[0], "negra", 34, ancho - 120), VERDE, "mm",
                   255 * _eo(u / .3))
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ un objeto que se muda de profesión
def traspaso(titulo, img, de, a, nota=None, ancho=1500):
    """de / a = (img_profesión, «NOMBRE»): el objeto está en `de`, vuela a `a` (marca 1) y `de` se tacha; nota en la marca 2."""
    h = 420

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        cy = M + 200
        xa, xb = M + ancho * .22, M + ancho * .78
        t0, t1, t2 = _mk(marcas, 0, .3), _mk(marcas, 1, 1.6), _mk(marcas, 2, 1e9)
        for k, ((pimg, nom), x) in enumerate(((de, xa), (a, xb))):
            u = dt - t0 - k * .15
            if u <= 0:
                continue
            s = _pop(u, .35)
            tachado = k == 0 and dt >= t1 + .7
            d.rounded_rectangle((x - 170, cy - 110, x + 170, cy + 130), 16, fill=(4, 6, 18, 240),
                                outline=(ROJO if tachado else (VERDE if k == 1 and dt >= t1 + .7 else ORO)) + (255,), width=3)
            _pegar(im, _img(pimg, 92, apagado=tachado), x, cy - 30, s)
            d = ImageDraw.Draw(im)
            _texto(d, (x, cy + 70), nom, _encaja(d, nom, "negra", 32, 320), GRIS if tachado else BLANCO, "mm", 255 * _eo(u / .3))
            if tachado:
                q = _eo((dt - t1 - .7) / .3)
                d.line([(x - 150, cy - 95), (x - 150 + 300 * q, cy - 95 + 210 * q)], fill=ROJO + (255,), width=9)
        # el objeto: sobre `de` hasta t1, vuela en arco, se asienta junto a `a`
        if dt >= t0:
            u = dt - t1
            q = _eo(u / .9) if u > 0 else 0.0
            x = xa + 120 + (xb - xa - 20) * q
            y = cy - 110 - 120 * math.sin(math.pi * q)
            _pegar(im, _img(img, 84), x, y, _pop(dt - t0, .35) * (1 + .3 * math.sin(math.pi * q)))
            d = ImageDraw.Draw(im)
            if 0 < q < 1:
                _flecha(d, (xa + 120, cy - 110), (x - 30, y), 1.0, ORO_T, 4, 0)
        if nota and dt >= t2:
            _texto(d, (M + ancho / 2, M + h - 36), nota, _encaja(d, nota, "negra", 34, ancho - 120), VERDE, "mm", 255 * _eo((dt - t2) / .3))
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ bolsas con su rejilla de casillas
def bolsas(titulo, lista, nota=None, ancho=1560):
    """lista = [(img, «Lino», casillas), ...]: la bolsa k y su rejilla en la marca k; nota en la marca len."""
    n = len(lista)
    T = 30
    h = 470 + (50 if nota else 0)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        w = (ancho - 80) / n
        for k, (img, nom, nn) in enumerate(lista):
            tk = _mk(marcas, k, .4 + k * .8)
            if dt < tk:
                continue
            u = dt - tk
            cx = M + 40 + w * (k + .5)
            _pegar(im, _img(img, 96), cx, M + 150, _pop(u, .35))
            d = ImageDraw.Draw(im)
            _texto(d, (cx, M + 224), nom, _encaja(d, nom, "sans", 28, w - 20), BLANCO, "mm", 255 * _eo(u / .3))
            cols = 4 if nn <= 8 else 7 if nn > 12 else 6
            fil = int(math.ceil(nn / cols))
            gx0 = cx - (cols * (T + 6) - 6) / 2
            for i in range(nn):
                ui = u - .2 - i * .05
                if ui <= 0:
                    break
                x = gx0 + (i % cols) * (T + 6)
                y = M + 262 + (i // cols) * (T + 6)
                d.rounded_rectangle((x, y, x + T, y + T), 5, fill=(4, 6, 18, 235), outline=ORO + (int(255 * _eo(ui / .2)),), width=2)
            _texto(d, (cx, M + 262 + fil * (T + 6) + 34), f"{nn} casillas", fuente("negra", 30), ORO_T, "mm",
                   255 * _eo((u - .2 - nn * .05) / .3))
        tn = _mk(marcas, n, 1e9)
        if nota and dt >= tn:
            _texto(d, (M + ancho / 2, M + h - 40), nota, _encaja(d, nota, "negra", 32, ancho - 120), VERDE, "mm", 255 * _eo((dt - tn) / .3))
        return _salida(im, dt)
    return fn


if __name__ == "__main__":
    import sys
    import tempfile

    PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "videos", "wow_ruta_profesiones", "pegatinas")
    P = lambda s: os.path.join(PEG, s + ".png")
    fondo = Image.new("RGB", (1920, 1080), (40, 70, 50))
    pruebas = [
        (habilidad(1, "MINERÍA", P("o_prof_mineria"), [(1, 65, "cobre"), (65, 125, "estaño y plata"), (125, 175, "hierro y oro"),
                                                     (175, 245, "mitril y veraplata"), (245, 300, "torio")], "alimenta a herrería e ingeniería"),
         [.3, 1, 1.6, 2.2, 2.8, 3.4, 4.0], 5),
        (rangos("ENTRENAR CADA RANGO", [(10, "cobre"), (5, "plata"), (50, "plata"), (5, "oro")], "≈ 5 de oro y media por profesión",
                [None, 10, 20, 35]), [.3, .8, 1.3, 1.8, 2.4, 3.0, 3.5, 4.0], 5),
        (barras("HERRERÍA · DEL 270 AL 300", P("o_barra_torio"), 500, 1200, "barras de torio", "un par de planos"), [.3, 2.0, 3.6], 5),
        (telar("LA TRAMPA DEL TELAR", P("o_telar"), ("LAS RECETAS 285-300", "PIDEN UN TELAR"), ("EL TELAR", "SOLO LO FABRICA QUIEN TIENE 300"),
               ["el telar de otro sastre", "otro camino"]), [.3, 1.3, 2.6, 3.2], 4.5),
        (campamento("EL CAMPAMENTO", [("BÁSICA", 3), ("DE OFICIAL", 5), ("DE EXPERTO", 10)],
                    [P(s) for s in ("o_rueda_afilar", "o_vela_incienso", "o_pozo_mana", "o_silla_campamento", "o_tienda_campamento",
                                    "o_estandarte_faccion", "o_laud_encantado", "o_magnetita", "o_cuenco_pescado", "o_equipo_primeros_auxilios")],
                    "28 millones de objetos en la primera semana"), [.3, 1.0, 2.0, 3.0, 4.0], 5.5),
        (legado("LEGADO DE PROFESIONES", [(P("o_prof_herreria"), "Herrería"), (P("o_prof_ingenieria"), "Ingeniería"),
                                         (P("o_prof_alquimia"), "Alquimia"), (P("o_prof_peleteria"), "Peletería"),
                                         (P("o_prof_sastreria"), "Sastrería"), (P("o_prof_encantamiento"), "Encantamiento")],
                ceros=[P(s) for s in ("o_prof_mineria", "o_prof_herboristeria", "o_prof_desuello", "o_prof_cocina", "o_prof_pesca",
                                      "o_prof_primeros_auxilios")]), [.3, 1.0, 1.7, 2.6, 3.4], 4.5),
        (flujo("DE LA HIERBA A LA TELA", [(0, 0, P("o_prof_herboristeria"), "Herboristería"), (1, 0, P("o_prof_alquimia"), "Alquimia"),
                                          (2, 0, P("o_tinte_ceruleo"), "Tintes"), (3, 0, P("o_prof_sastreria"), "Sastrería"),
                                          (3, 1, P("o_prof_peleteria"), "Peletería")], [(0, 1), (1, 2), (2, 3), (2, 4)],
               ("el alquimista tiene clientes nuevos", 5)), [.3, .9, 1.5, 2.1, 2.5, 3.2], 4),
        (traspaso("LAS POCIONES DE SANACIÓN", P("o_pocion_sanacion"), (P("o_prof_alquimia"), "ALQUIMIA"),
                  (P("o_prof_primeros_auxilios"), "PRIMEROS AUXILIOS"), "ahora las puede hacer cualquiera"), [.3, 1.2, 2.6], 4),
        (bolsas("BOLSAS DE COMPONENTES", [(P("o_bolsa_componentes_lino"), "Lino", 6), (P("o_pano_lino"), "Lana", 8),
                                          (P("o_tejido_magico"), "Grande", 12), (P("o_pano_runico"), "Grande", 14)], "las de 12 y 14, con Favor"),
         [.3, .9, 1.5, 2.1, 3.0], 4.5),
    ]
    sel = [int(a) for a in sys.argv[1:]] or range(len(pruebas))
    for i in sel:
        fn, marcas, t = pruebas[i]
        a = fn(t, 8, marcas)
        im = Image.fromarray(a[..., [2, 1, 0, 3]])
        f = fondo.copy()
        f.paste(im, ((1920 - im.width) // 2, (1080 - im.height) // 2), im)
        r = os.path.join(tempfile.gettempdir(), f"_mg_prof_prueba{i}.jpg")
        f.resize((960, 540)).save(r, quality=85)
        print(r, im.size)
