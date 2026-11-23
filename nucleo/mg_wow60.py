# -*- coding: utf-8 -*-
"""MOTION GRAPHICS del SESENTA y las BANDAS con la interfaz de WoW (panel azul noche y borde dorado de mg_wow), hechos para
«Los 25 ERRORES al llegar al nivel 60 en WoW Forever» (wow_errores_60, 22-nov-2026). Sirven a cualquier video de fin de nivel,
bandas o JcJ de Forever. CERO cifras inventadas: solo números que el guion dice. Uso en efectos.py igual que mg_wow
(fn(dt, dur, marcas)); las imágenes pueden ser un nombre de ícono de Wowhead o la ruta de una pegatina PNG/JPG.
  cuenta_atras(titulo, n, unidad, fecha, bandas, nota)   anillo de n segmentos con la cifra grande (los días que faltan) y las
                                                         bandas que entran una por marca (foto, nombre, tamaño); marca 0 = anillo,
                                                         1..len = bandas, len+1 = nota con flecha de reinicio
  aforo(titulo, bandas, grupo, rotulo)                   una fila de casillas de jugador por banda (10/20/40 fijas); marca k = la
                                                         banda k; marca len = «tu grupo» (los primeros `grupo` en verde, los que
                                                         faltan en rojo) y ✔/✘ por banda
  consolas(titulo, consolas, n, final, remate)           consolas de colores con n cristales cada una que se llenan en su marca, el
                                                         total que corre (n × consolas) y, en la marca len, el jefe final
  rangos(titulo, hitos, techos, reinicio, tope)          escalera de rangos JcJ 1..tope: hitos (ícono en su peldaño) uno por marca,
                                                         luego cada techo semanal (línea roja) y al final el reinicio a rango 1
  tope_hora(titulo, antes, ahora, sello)                 reloj de una hora y las entradas a mazmorra: «antes» se encienden, luego
                                                         «ahora» y las que sobran se tachan; sello en la última marca
  entregas(titulo, piezas, vendida, nota, arriba, abajo) dos filas de casillas: el conjunto que tienes arriba y el siguiente abajo;
                                                         la pieza k viaja y sube de nivel en su marca; en la marca len la pieza
                                                         `vendida` se queda vacía en rojo con la `nota`
"""
import math
import os

from PIL import Image, ImageDraw, ImageFilter

from mg_wow import (BLANCO, GRIS, ORO, ORO_T, VERDE, _base, _eo, _mk, _pegar, _pop, _salida, _sello, _texto, fuente,
                    icono)

ROJO = (235, 60, 50)
AZUL_C, MORADO = (0, 112, 221), (163, 53, 238)
_cache = {}


def _encaja(d, s, nombre, tam, ancho):
    while tam > 16 and d.textlength(s, font=fuente(nombre, tam)) > ancho:
        tam -= 2
    return fuente(nombre, tam)


def _img(src, tam, apagado=False):
    """Ícono de Wowhead (nombre) o imagen local (ruta) ajustada a tam×tam, sin deformar."""
    if not (isinstance(src, str) and os.path.exists(src)):
        return icono(src, tam, apagado)
    k = ("img", src, tam, apagado)
    if k not in _cache:
        im = Image.open(src).convert("RGBA")
        im.thumbnail((tam, tam), Image.LANCZOS)
        lien = Image.new("RGBA", (tam, tam), (0, 0, 0, 0))
        lien.alpha_composite(im, ((tam - im.width) // 2, (tam - im.height) // 2))
        if apagado:
            g = lien.convert("LA").convert("RGBA")
            g.putalpha(lien.getchannel("A").point(lambda v: int(v * .45)))
            lien = g
        _cache[k] = lien
    return _cache[k]


def _foto(src, w, h, radio=12):
    """Foto local recortada para CUBRIR w×h (recorte por arriba si es alta: caras), con esquinas redondeadas."""
    k = ("foto", src, w, h)
    if k not in _cache:
        if isinstance(src, str) and os.path.exists(src):
            im = Image.open(src).convert("RGBA")
            s = max(w / im.width, h / im.height)
            im = im.resize((max(w, int(im.width * s + .5)), max(h, int(im.height * s + .5))), Image.LANCZOS)
            x0 = (im.width - w) // 2
            y0 = (im.height - h) // 2 if im.width / im.height >= w / h else int((im.height - h) * .2)
            im = im.crop((x0, y0, x0 + w, y0 + h))
        else:
            im = icono(src, max(w, h)).resize((w, h))
        m = Image.new("L", (w, h), 0)
        ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radio, fill=255)
        im.putalpha(Image.composite(im.getchannel("A"), Image.new("L", (w, h), 0), m))
        _cache[k] = im
    return _cache[k]


def _jugador(d, x, y, t, color, alfa=255, borde=None):
    """Casilla de jugador: cabeza + hombros dentro de un cuadro redondeado."""
    a = int(alfa)
    d.rounded_rectangle((x, y, x + t, y + t), max(3, t // 6), fill=(4, 6, 18, int(a * .9)), outline=(borde or (95, 82, 45)) + (a,), width=2)
    if color is None:
        return
    c = tuple(color) + (a,)
    r = t * .17
    cx = x + t / 2
    d.ellipse((cx - r, y + t * .18, cx + r, y + t * .18 + 2 * r), fill=c)
    d.pieslice((x + t * .2, y + t * .56, x + t * .8, y + t * 1.12), 180, 360, fill=c)


def _marca_ok(d, cx, cy, r, ok, alfa=255):
    """Palomita verde o tache rojo dibujados (las fuentes del kit no traen ✔/✘)."""
    a = int(alfa)
    if ok:
        d.line([(cx - r, cy), (cx - r * .3, cy + r * .7), (cx + r, cy - r * .8)], fill=VERDE + (a,), width=max(4, int(r * .35)), joint="curve")
    else:
        w = max(4, int(r * .35))
        d.line([(cx - r * .8, cy - r * .8), (cx + r * .8, cy + r * .8)], fill=ROJO + (a,), width=w)
        d.line([(cx - r * .8, cy + r * .8), (cx + r * .8, cy - r * .8)], fill=ROJO + (a,), width=w)


# ------------------------------------------------------------------ intro: los días que faltan para las bandas
def cuenta_atras(titulo, n, unidad, fecha, bandas, nota=None, ancho=1560):
    """bandas = [(imagen, nombre, rótulo), ...] (≤ 3)."""
    h = 520

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        cx, cy, R = M + 250, M + 278, 155
        t0 = _mk(marcas, 0, .3)
        if dt >= t0:
            u = dt - t0
            for i in range(n):                     # segmentos del anillo, uno por día, que se encienden en cascada
                q = _eo((u - i * .05) / .25)
                a0 = -90 + i * 360 / n + 2.5
                a1 = -90 + (i + 1) * 360 / n - 2.5
                col = ORO_T if q > 0 else (60, 55, 40)
                d.arc((cx - R, cy - R, cx + R, cy + R), a0, a1, fill=col + (int(80 + 175 * q),), width=22)
            s = 1 + .15 * max(0.0, 1 - u / .35)
            k = min(n, int(n * _eo(u / .9)) if u < .9 else n)
            _texto(d, (cx, cy - 18), str(k), fuente("negra", int(150 * s)), BLANCO, "mm", 255 * _eo(u / .3))
            _texto(d, (cx, cy + 74), unidad, fuente("negra", 34), ORO_T, "mm", 255 * _eo((u - .3) / .3))
            _texto(d, (cx, cy + R + 34), fecha, fuente("serif", 30), GRIS, "mm", 255 * _eo((u - .5) / .3))
        x0 = M + 500
        wc = (ancho - 520 - 2 * 24) / max(1, len(bandas))
        for k, (img, nom, rot) in enumerate(bandas):
            tk = _mk(marcas, 1 + k, t0 + 1 + k * .8)
            if dt < tk:
                continue
            u = dt - tk
            xk = x0 + k * (wc + 24)
            yk = M + 110 + (1 - _eo(u / .4)) * 40
            a = _eo(u / .3)
            ft = _foto(img, int(wc), 220)
            _pegar(im, ft, xk + wc / 2, yk + 110, 1.0, a)
            d = ImageDraw.Draw(im)
            d.rounded_rectangle((xk, yk, xk + wc, yk + 220), 12, outline=ORO + (int(255 * a),), width=3)
            _texto(d, (xk + wc / 2, yk + 256), nom, _encaja(d, nom, "negra", 32, wc - 10), BLANCO, "mm", 255 * a)
            _texto(d, (xk + wc / 2, yk + 300), rot, _encaja(d, rot, "sans", 30, wc - 10), ORO_T, "mm", 255 * a)
        tn = _mk(marcas, 1 + len(bandas), 1e9)
        if nota and dt >= tn:
            u = dt - tn
            yn = M + h - 52
            _texto(d, (x0 + (ancho - 520) / 2 + 30, yn), nota, fuente("serif", 34), VERDE, "mm", 255 * _eo(u / .3))
            # flecha circular de reinicio a la izquierda de la nota
            xa = x0 + (ancho - 520) / 2 + 30 - d.textlength(nota, font=fuente("serif", 34)) / 2 - 40
            ang = 300 * _eo(u / .6)
            d.arc((xa - 18, yn - 18, xa + 18, yn + 18), -60, -60 + ang, fill=VERDE + (255,), width=5)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ c08: las bandas son fijas y tu grupo no cambia
def aforo(titulo, bandas, grupo=None, rotulo=None, ancho=1600):
    """bandas = [(nombre, n, sub), ...] con n = 10/20/40; grupo = jugadores que tienes (None = no sale)."""
    T, G, POR = 30, 6, 20
    lineas = [math.ceil(n / POR) for _, n, _ in bandas]
    h = 120 + sum(l * (T + G) + 54 for l in lineas) + (70 if rotulo else 20)

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        tg = _mk(marcas, len(bandas), 1e9)
        y = M + 112
        for k, (nom, n, sub) in enumerate(bandas):
            tk = _mk(marcas, k, .4 + k * 1.1)
            alto = lineas[k] * (T + G)
            if dt >= tk:
                u = dt - tk
                a = 255 * _eo(u / .3)
                _texto(d, (M + 60, y + 14), nom, _encaja(d, nom, "negra", 34, 440), BLANCO, "lm", a)
                _texto(d, (M + 60, y + 54), sub, _encaja(d, sub, "sans", 26, 440), ORO_T, "lm", a)
                x0 = M + 540
                for i in range(n):
                    ui = u - .2 - i * .025
                    if ui <= 0:
                        continue
                    xi = x0 + (i % POR) * (T + G)
                    yi = y + (i // POR) * (T + G)
                    col, bor = (190, 190, 200), None
                    if grupo is not None and dt >= tg:
                        lleno = i < grupo
                        col, bor = (VERDE, VERDE) if lleno else (None, ROJO)
                    _jugador(d, xi, yi, T, col, 255 * _eo(ui / .2), bor)
                if grupo is not None and dt >= tg:
                    ug = dt - tg
                    ok = grupo >= n
                    xv = x0 + POR * (T + G) + 40
                    _marca_ok(d, xv, y + alto / 2 - 3, 22 * (1 + .3 * max(0, 1 - ug / .3)), ok, 255 * _eo(ug / .25))
            y += alto + 54
        if rotulo and grupo is not None and dt >= tg:
            _texto(d, (M + ancho / 2, M + h - 42), rotulo, fuente("serif", 34), VERDE, "mm", 255 * _eo((dt - tg - .4) / .3))
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ c15: el Bancal del Creador, 4 consolas × 15 cristales
def consolas(titulo, consolas_, n=15, final=None, remate=None, ancho=1640):
    """consolas_ = [(color RGB, rótulo del color, jefe, elemento, imagen del cristal), ...]; final = (imagen, nombre, sub)."""
    nc = len(consolas_)
    h = 680 if final else 580

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        wc = (ancho - 120 - (nc - 1) * 26) / nc
        tot = 0.0
        for k, (col, rot, jefe, elem, img) in enumerate(consolas_):
            tk = _mk(marcas, k, .4 + k * 1.2)
            xk = M + 60 + k * (wc + 26)
            yk = M + 100
            d.rounded_rectangle((xk, yk, xk + wc, yk + 380), 14, fill=(6, 8, 22, 235), outline=(95, 82, 45, 255), width=2)
            if dt < tk:
                _texto(d, (xk + wc / 2, yk + 190), "?", fuente("negra", 80), (70, 70, 90), "mm")
                continue
            u = dt - tk
            q = _eo(u / 1.1)
            d.rounded_rectangle((xk, yk, xk + wc, yk + 380), 14, outline=tuple(col) + (255,), width=4)
            _pegar(im, _img(img, 64), xk + 46, yk + 44, _pop(u))
            d = ImageDraw.Draw(im)
            _texto(d, (xk + 86, yk + 44), rot, _encaja(d, rot, "negra", 30, wc - 100), col, "lm", 255 * _eo(u / .3))
            llenos = int(n * q + 1e-6)
            tot += n * q
            S = min(36, (wc - 60) / 5 - 8)
            for i in range(n):                         # 3 filas de 5 rombos
                cxr = xk + wc / 2 + ((i % 5) - 2) * (S + 8)
                cyr = yk + 106 + (i // 5) * (S + 8)
                pts = [(cxr, cyr - S / 2), (cxr + S / 2.6, cyr), (cxr, cyr + S / 2), (cxr - S / 2.6, cyr)]
                if i < llenos:
                    d.polygon(pts, fill=tuple(col) + (255,), outline=BLANCO + (200,))
                else:
                    d.polygon(pts, fill=(20, 22, 40, 255), outline=(80, 80, 100, 255))
            _texto(d, (xk + wc / 2, yk + 106 + 3 * (S + 8) + 10), f"{llenos} / {n}", fuente("negra", 30), BLANCO, "mm", 255)
            if q >= 1:
                ua = u - 1.1
                _texto(d, (xk + wc / 2, yk + 306), jefe, _encaja(d, jefe, "negra", 36, wc - 20), ORO_T, "mm", 255 * _eo(ua / .3))
                _texto(d, (xk + wc / 2, yk + 344), elem, _encaja(d, elem, "sans", 24, wc - 20), GRIS, "mm", 255 * _eo(ua / .3))
        # total que corre
        yt = M + 524
        _texto(d, (M + ancho / 2, yt), f"{int(round(tot))} / {n * nc} CRISTALES", fuente("negra", 40), VERDE if tot >= n * nc - .01 else BLANCO, "mm",
               255 * _eo((dt - _mk(marcas, 0, .4)) / .3))
        if final:
            tf = _mk(marcas, nc, 1e9)
            if dt >= tf:
                u = dt - tf
                img, nom, sub = final
                s = _pop(u)
                _pegar(im, _img(img, 74), M + ancho / 2 - 440, yt + 82, s)
                d = ImageDraw.Draw(im)
                _texto(d, (M + ancho / 2 - 380, yt + 70), nom, fuente("negra", 40), (255, 128, 0), "lm", 255 * _eo(u / .3))
                _texto(d, (M + ancho / 2 - 380, yt + 108), sub, fuente("sans", 26), BLANCO, "lm", 255 * _eo((u - .2) / .3))
        tr = _mk(marcas, nc + (1 if final else 0), 1e9)
        if remate and dt >= tr:
            _sello(im, remate, M + ancho - 300, yt + 88, dt - tr, ROJO, 32, ang=-5)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ c22/c21: la escalera de rangos JcJ de Forever
def rangos(titulo, hitos=(), techos=(), reinicio=None, tope=14, ancho=1560):
    """hitos = [(rango, imagen, texto), ...]; techos = [(texto, rango), ...]; reinicio = texto (todo vuelve al rango 1)."""
    h = 600

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        x0, x1, yb, hmax = M + 90, M + ancho - 90, M + h - 70, 360
        w = (x1 - x0) / tope
        nh, nt = len(hitos), len(techos)
        # techo vigente: el último que ya entró (con transición)
        techo, utecho = None, 0
        for j, (txt, r) in enumerate(techos):
            tj = _mk(marcas, nh + j, 1e9)
            if dt >= tj:
                techo, utecho, ttxt = r, dt - tj, txt
        tr = _mk(marcas, nh + nt, 1e9)
        caida = _eo((dt - tr) / .8) if reinicio and dt >= tr else 0.0
        for i in range(tope):
            r = i + 1
            u = dt - .15 - i * .045
            if u <= 0:
                continue
            q = _eo(u / .35)
            hh = 50 + (hmax - 50) * i / (tope - 1)
            hh = hh * q * (1 - caida) + (50 if r == 1 else 14) * caida
            bloqueado = techo is not None and r > techo
            col = (40, 44, 70) if bloqueado or (caida > .5 and r > 1) else (70, 120, 210)
            if r == 1 and caida > .5:
                col = (90, 200, 120)
            xa = x0 + i * w + 4
            d.rounded_rectangle((xa, yb - hh, xa + w - 8, yb), 6, fill=col + (240,), outline=ORO + (160,), width=2)
            _texto(d, (xa + (w - 8) / 2, yb + 26), str(r), fuente("negra", 26), GRIS if bloqueado else BLANCO, "mm", 255 * q)
        for k, (r, img, txt) in enumerate(hitos):
            tk = _mk(marcas, k, .8 + k * 1.0)
            if dt < tk or caida > .3:
                continue
            u = dt - tk
            i = r - 1
            hh = 50 + (hmax - 50) * i / (tope - 1)
            xc = x0 + i * w + w / 2
            yc = yb - hh - 44
            _pegar(im, _img(img, 64), xc, yc, _pop(u))
            d = ImageDraw.Draw(im)
            d.rounded_rectangle((x0 + i * w + 4, yb - hh, x0 + i * w + w - 4, yb), 6, outline=ORO_T + (255,), width=4)
            fx = _encaja(d, txt, "sans", 26, 330)
            tw = d.textlength(txt, font=fx)
            xt = min(max(xc, M + 40 + tw / 2), M + ancho - 40 - tw / 2)
            _texto(d, (xt, yc - 52), txt, fx, ORO_T, "mm", 255 * _eo((u - .15) / .3))
        if techo is not None and caida < .3:
            i = techo - 1
            hh = 50 + (hmax - 50) * i / (tope - 1)
            yl = yb - hh - 10
            q = _eo(utecho / .5)
            d.line([(x0, yl), (x0 + (x1 - x0) * q, yl)], fill=ROJO + (255,), width=6)
            fx = fuente("negra", 32)
            tw = d.textlength(ttxt, font=fx)
            xt = min(x0 + techo * w + 20 + tw / 2, x1 - tw / 2 - 10)
            yt = max(M + 104, yl - 40)
            a = _eo(utecho / .3)
            d.rounded_rectangle((xt - tw / 2 - 16, yt - 24, xt + tw / 2 + 16, yt + 24), 10, fill=(10, 8, 20, int(235 * a)),
                                outline=ROJO + (int(255 * a),), width=3)            # píldora: el rótulo no se pierde entre las barras
            _texto(d, (xt, yt), ttxt, fx, ROJO, "mm", 255 * a)
        if reinicio and dt >= tr:
            _sello(im, reinicio, M + ancho / 2, M + 200, dt - tr - .5, ROJO, 40, ang=-6)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ c05: el tope de entradas por hora
def tope_hora(titulo, antes, ahora, sello=None, ico="inv_misc_key_03", ancho=1500):
    """antes/ahora = (rótulo, n). Marca 0: la fila de «antes» · 1: la fila de «ahora» (las que sobran, tachadas) · 2: sello."""
    h = 530
    na, nn = antes[1], ahora[1]

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        cx, cy, R = M + 200, M + 270, 130
        # reloj de una hora: la aguja da la vuelta mientras el MG está en pantalla
        d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(6, 8, 22, 240), outline=ORO + (255,), width=5)
        for i in range(12):
            a = math.radians(i * 30 - 90)
            d.line([(cx + math.cos(a) * (R - 18), cy + math.sin(a) * (R - 18)), (cx + math.cos(a) * (R - 6), cy + math.sin(a) * (R - 6))],
                   fill=ORO_T + (255,), width=4)
        frac = min(1.0, dt / max(1.0, min(dur, 9.0)))
        d.pieslice((cx - R + 12, cy - R + 12, cx + R - 12, cy + R - 12), -90, -90 + 360 * frac, fill=(201, 162, 39, 90))
        a = math.radians(-90 + 360 * frac)
        d.line([(cx, cy), (cx + math.cos(a) * (R - 26), cy + math.sin(a) * (R - 26))], fill=BLANCO + (255,), width=6)
        d.ellipse((cx - 9, cy - 9, cx + 9, cy + 9), fill=ORO_T + (255,))
        _texto(d, (cx, cy + R + 32), "1 HORA", fuente("negra", 30), ORO_T, "mm")
        T, G = 76, 14
        x0 = M + 420
        for fila, (rot, n, i_m) in enumerate(((antes[0], na, 0), (ahora[0], nn, 1))):
            tk = _mk(marcas, i_m, .4 + i_m * 2.0)
            if dt < tk:
                continue
            u = dt - tk
            y = M + 140 + fila * 160
            _texto(d, (x0, y - 20), rot, fuente("negra", 32), BLANCO if fila == 0 else VERDE, "lm", 255 * _eo(u / .3))
            for i in range(na):
                ui = u - .15 - i * .08
                if ui <= 0:
                    continue
                x = x0 + i * (T + G)
                d.rounded_rectangle((x, y + 8, x + T, y + 8 + T), 8, fill=(4, 6, 18, 235), outline=(95, 82, 45, 255), width=2)
                apagada = fila == 1 and i >= nn
                _pegar(im, icono(ico, T - 10, apagada), x + T / 2, y + 8 + T / 2, _pop(ui))
                d = ImageDraw.Draw(im)
                if apagada and ui > .3:
                    q = _eo((ui - .3) / .25)
                    d.line([(x + 6, y + 14), (x + 6 + (T - 12) * q, y + 2 + T - (T - 12) * (1 - q) - 0)], fill=ROJO + (255,), width=6)
        ts = _mk(marcas, 2, 1e9)
        if sello and dt >= ts:
            _sello(im, sello, M + ancho * .64, M + h - 52, dt - ts, ROJO, 34, ang=-3)
        return _salida(im, dt)
    return fn


# ------------------------------------------------------------------ c01: la cadena del conjunto 0.5 se come el conjunto
def entregas(titulo, piezas, vendida=None, nota=None, arriba="CONJUNTO DE MAZMORRA", abajo="CONJUNTO 0.5", ancho=1640):
    """piezas = [(imagen, nombre), ...]; la k viaja en su marca; marca len: la pieza `vendida` (índice) se vacía con `nota`."""
    n = len(piezas)
    T = min(110, int((ancho - 140) / n) - 22)
    G = (ancho - 120 - n * T) / max(1, n - 1)
    h = 620

    def fn(dt, dur, marcas):
        im, M = _base(ancho, h, titulo)
        d = ImageDraw.Draw(im)
        ya, yb = M + 150, M + 370
        _texto(d, (M + 60, ya - 30), arriba, fuente("negra", 28), AZUL_C, "lm")
        _texto(d, (M + 60, yb - 30), abajo, fuente("negra", 28), MORADO, "lm")
        tv = _mk(marcas, n, 1e9)
        for k, (img, nom) in enumerate(piezas):
            x = M + 60 + k * (T + G)
            tk = _mk(marcas, k, .6 + k * .7)
            vend = vendida == k and dt >= tv
            for yy in (ya, yb):
                d.rounded_rectangle((x, yy, x + T, yy + T), 9, fill=(4, 6, 18, 235), outline=(95, 82, 45, 255), width=2)
            u = dt - tk
            if u < 0 and not vend:                     # todavía arriba, en azul
                _pegar(im, _img(img, T - 10), x + T / 2, ya + T / 2)
                d = ImageDraw.Draw(im)
                d.rounded_rectangle((x, ya, x + T, ya + T), 9, outline=AZUL_C + (255,), width=3)
            elif vend:
                d.rounded_rectangle((x, ya, x + T, ya + T), 9, outline=ROJO + (255,), width=4)
                d.rounded_rectangle((x, yb, x + T, yb + T), 9, outline=ROJO + (255,), width=4)
                uu = dt - tv
                _texto(d, (x + T / 2, yb + T / 2), "?", fuente("negra", 60), ROJO, "mm", 255 * _eo(uu / .3))
            else:
                q = _eo(u / .7)
                yy = ya + (yb - ya) * q
                _pegar(im, _img(img, T - 10), x + T / 2, yy + T / 2, 1.0 + .25 * math.sin(math.pi * q))
                d = ImageDraw.Draw(im)
                if q >= 1:
                    gl = Image.new("RGBA", im.size, (0, 0, 0, 0))
                    ImageDraw.Draw(gl).rounded_rectangle((x - 6, yb - 6, x + T + 6, yb + T + 6), 12, outline=MORADO + (220,), width=8)
                    im.alpha_composite(gl.filter(ImageFilter.GaussianBlur(5)))
                    d = ImageDraw.Draw(im)
                    d.rounded_rectangle((x, yb, x + T, yb + T), 9, outline=MORADO + (255,), width=3)
            fn_ = _encaja(d, nom, "sans", 24, T + G - 8)
            _texto(d, (x + T / 2, yb + T + 26), nom, fn_, ROJO if vend else BLANCO, "mm", 255 if (u >= 0 or vend) else 120)
        if nota and dt >= tv:
            u = dt - tv
            _texto(d, (M + ancho / 2, M + h - 40), nota, _encaja(d, nota, "negra", 34, ancho - 120), ROJO, "mm", 255 * _eo(u / .3))
        return _salida(im, dt)
    return fn


if __name__ == "__main__":
    import sys
    import tempfile

    import numpy as np
    PEG = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "videos", "wow_errores_60", "pegatinas")
    P = lambda s: os.path.join(PEG, s + ".png")
    fondo = Image.new("RGB", (1920, 1080), (40, 70, 50))
    pruebas = [
        (cuenta_atras("FALTAN PARA LAS BANDAS", 14, "DÍAS", "9 de diciembre", [(P("cavernas_tumulo"), "Cavernas del Túmulo", "10 jugadores"),
                                                                            (P("cima_hyjal"), "Cima Hyjal", "20 jugadores"),
                                                                            (P("guarida_onyxia"), "Guarida de Onyxia", "40 jugadores")],
                      "reinician cada semana"), [.2, 1.2, 1.8, 2.4, 3.0], 5),
        (aforo("LAS BANDAS SON FIJAS", [("Cavernas del Túmulo", 10, "8 jefes"), ("Cima Hyjal", 20, "13 jefes"), ("Guarida de Onyxia", 40, "1 jefe")],
               14, "Tu hermandad: 14 jugadores"), [.2, 1.0, 2.0, 4.0], 6),
        (consolas("BANCAL DEL CREADOR · 4 CONSOLAS", [((235, 60, 50), "Rojo", "Cinder", "fuego", P("o_cristal_rojo")),
                                                     ((255, 210, 40), "Amarillo", "Bolt", "rayo", P("o_cristal_amarillo")),
                                                     ((70, 140, 255), "Azul", "Snowtalon", "escarcha", P("o_cristal_azul")),
                                                     ((60, 200, 90), "Verde", "Vitrix (probable)", "veneno", P("o_cristal_verde"))], 15,
                  ("inv_misc_gem_crystal_01", "NANAYA", "jefa final · cambia de elemento cada 25 %"), "SIN CRISTALES: 5 JEFES"),
         [.2, 1.0, 1.8, 2.6, 4.2, 5.0], 6.5),
        (rangos("LOS LACRES ENVALENTONADOS", [(8, P("o_lacre_muneca"), "muñeca y cinturón · rango 8"), (11, "ability_mount_charger", "monturas · rango 11"),
                                             (13, P("o_lacre_cabeza"), "cabeza · rango 13")]), [.5, 1.5, 2.5], 4.5),
        (rangos("EL RANGO TIENE TOPE", [], [("SEMANA 1 · TOPE RANGO 3", 3), ("SEMANA 10 · TOPE RANGO 14", 14)], "TEMPORADA NUEVA: RANGO 1"),
         [1.0, 2.5, 4.0], 4.5),
        (rangos("EL RANGO TIENE TOPE", [], [("SEMANA 1 · TOPE RANGO 3", 3), ("SEMANA 10 · TOPE RANGO 14", 14)], "TEMPORADA NUEVA: RANGO 1"),
         [1.0, 2.5, 4.0], 6.0),
        (tope_hora("ENTRADAS A UNA MAZMORRA", ("ANTES: 10 POR HORA", 10), ("DESDE EL 20 DE NOVIEMBRE: 5", 5), "DEMASIADAS ESTANCIAS"),
         [.3, 2.0, 3.5], 5),
        (entregas("LA CADENA DEL CONJUNTO 0.5", [("inv_bracer_14", "Brazales"), ("inv_belt_27", "Cinturón"), ("inv_gauntlets_29", "Guantes"),
                                                ("inv_boots_plate_06", "Botas"), (P("o_quijotes_forjaluz"), "Piernas"), ("inv_shoulder_10", "Hombreras"),
                                                (P("o_yelmo_forjaluz"), "Casco"), (P("o_peto_forjaluz"), "Peto")],
                  6, "¿Vendiste el casco? A matar a Gandling otra vez"), [.3, .8, 1.3, 1.8, 2.3, 2.8, 3.3, 3.8, 5.0], 6),
    ]
    sel = [int(a) for a in sys.argv[1:]] or range(len(pruebas))
    for i in sel:
        fn, marcas, t = pruebas[i]
        a = fn(t, 8, marcas)
        im = Image.fromarray(a[..., [2, 1, 0, 3]])
        f = fondo.copy()
        f.paste(im, ((1920 - im.width) // 2, (1080 - im.height) // 2), im)
        r = os.path.join(tempfile.gettempdir(), f"_mg_wow60_prueba{i}.jpg")
        f.resize((960, 540)).save(r, quality=85)
        print(r, im.size)
