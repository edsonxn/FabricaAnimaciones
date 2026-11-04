# -*- coding: utf-8 -*-
"""MOTION GRAPHICS TRANSLÚCIDOS de Banjo-Tooie (Crónicas del gaming; primer uso `bt_jiggies_crueles`, 23-oct-2026).
Regla del usuario (22-oct-2026, tras `zelda_oot`): FICHAS TRANSLÚCIDAS como las de Tamriel (humo difuminado, separadores finos,
tipografía de la interfaz) pero con la interfaz de CADA juego; nunca carteles opacos que tapen el video. Aquí: humo chocolate
de bordes difuminados (no caja), filetes miel que se desvanecen con un panal hexagonal al centro, Cooper Black miel con
contorno (los rótulos de Rare) y Arial Rounded crema; los contadores son PANALES como la barra de vida del juego. Todo entra
con rebote y nada queda quieto. CERO cifras ni nombres inventados: solo lo que el guion dice.

    import mg_banjo as B
  ficha(titulo, texto, sub=None)            ficha translúcida; *asteriscos* = miel; el texto entra línea a línea
  puesto(num, titulo, jiggy)                Jiggy REAL que gira sobre su eje (como en el juego) con el número + título en humo
  crueldad(nivel, total=5)                  «CRUELDAD»: panales que se llenan uno a uno (rojo en el máximo)
  bt_jiggies_crueles (23-oct-2026), animados por las marcas de la voz:
  marcador(titulo, metas, total, segundos, iconos, pasos)   barra de puntos con dos metas (página de Cheato / Jiggy) + reloj
  contrarreloj(titulo, n, segundos, icono, remate, gas, hasta)   n objetivos que caen con reloj; remate BOOM o gas tóxico
  carrera(banjo, mary)                      Canary Mary contra Banjo: botón A, acelera si te pegas, acelerón final, el truco
  recados(titulo, madre, hijos, premio)     problema -> solución de cada hijo, ✓, Jiggy de premio y sello «NO»
  cadena(titulo, pasos, final)              requisitos encadenados hasta el jefe (en rojo)
  bt_mundos_ranking (30-oct-2026): egg(num, titulo), cuatro_listas(titulo, filas, media), ruleta(), codigos(filas),
  conexiones(nodos, enlaces), ficha_mundo(items)
  bt_50_secretos (3-nov-2026; marcas de la voz o, si faltan, fracciones fijas de la duración):
  secreto(num, titulo, total) rótulo grande (~4 s)  ·  contador(num, total) HUD «N/50» de esquina todo el secreto
  versus(izq, der, titulo, marca) N64 <-> Xbox 360/Japón  ·  concurso(pregunta, opciones, correcta, trampa)
  antipirata(n) cartucho + 0 -> 268 + «NO CONTROLLER»  ·  huesos(n, quitar) pez abisal  ·  cronometro(filas)
  fechas(hitos) sellos por región  ·  jinjos_color(n)  ·  rotulos(lineas) subtítulos de jefe  ·  memoria(lleno, pak)
  compas(bpm, compases) 6/8 al tempo
  (pegatinas: mg_tes.pegatina · pantallas: mg_wow.pantalla · mapas: mg_mapa tema «gaming»)
"""
import math
import os
import re

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

from mg_gaming import (MIEL, MIEL_OSC, CREMA, CHOCO, ROJO, fuente, _eo, _reb, _texto, _escala, _partir)

AZUL_CLARO = (150, 196, 255)
_bc = {}


def _bgra(im, alfa=1.0):
    a = np.array(im)
    if alfa < 1:
        a[..., 3] = (a[..., 3] * max(0.0, alfa)).astype(np.uint8)
    return a[..., [2, 1, 0, 3]].copy()


def _hex(cx, cy, r, giro=0.0):
    return [(cx + r * math.cos(math.radians(60 * k + 30 + giro)), cy + r * math.sin(math.radians(60 * k + 30 + giro)))
            for k in range(6)]


def filete(d, cx, y, medio, alfa=255, color=MIEL):
    """Línea miel fina que se desvanece hacia los extremos, con un panal hexagonal al centro."""
    a = alfa / 255
    for i in range(60):
        u0, u1 = i / 60, (i + 1) / 60
        k = (1 - u0) ** 1.5
        for s in (-1, 1):
            d.line([(cx + s * (12 + u0 * medio), y), (cx + s * (12 + u1 * medio), y)], fill=color + (int(235 * k * a),), width=3)
    d.polygon(_hex(cx, y, 11), fill=CHOCO + (int(200 * a),), outline=color + (int(255 * a),))
    d.polygon(_hex(cx, y, 5), fill=color + (int(255 * a),))


def humo(w, h):
    """Humo chocolate oscuro con bordes muy difuminados (deja ver el juego alrededor); se calcula una vez por tamaño."""
    k = (w, h)
    if k not in _bc:
        M = 60
        im = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
        m = Image.new("L", im.size, 0)
        ImageDraw.Draw(m).rounded_rectangle((M + 12, M + 12, M + w - 12, M + h - 12), 46, fill=196)
        m = m.filter(ImageFilter.GaussianBlur(28))
        capa = Image.new("RGBA", im.size, (22, 12, 6, 255))
        capa.putalpha(m)
        im.alpha_composite(capa)
        _bc[k] = (im, M)
    im, M = _bc[k]
    return im.copy(), M


def _linea_rica(d, cx, y, s, f, alfa):
    """Línea centrada: *tramos* en miel, el resto en crema."""
    trozos = s.split("*")
    total = sum(d.textlength(t, font=f) for t in trozos)
    x = cx - total / 2
    for i, t in enumerate(trozos):
        if t:
            _texto(d, (x, y), t, f, MIEL if i % 2 else CREMA, "lm", alfa)
            x += d.textlength(t, font=f)


# ------------------------------------------------------------------ ficha translúcida
def ficha(titulo, texto, sub=None, ancho=960):
    """Título Cooper miel con contorno chocolate, `sub` (mundo, personaje) chico espaciado en azul claro, filete con panal y
    el texto centrado que entra línea a línea. Sin caja: humo difuminado."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    ft, fs, fx = fuente("t", 62), fuente("r", 29), fuente("r", 41)
    tits = _partir(tmp, titulo, ft, ancho - 120)
    lineas = _partir(tmp, texto, fx, ancho - 110)
    h = 40 + (40 if sub else 0) + 72 * len(tits) + 44 + 56 * len(lineas) + 34

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        cx, y = M + ancho / 2, M + 34
        if sub:
            _texto(d, (cx, y + 10), " ".join(sub.upper()), fs, AZUL_CLARO, "mm", 255 * _eo(dt / .3))
            y += 40
        for k, ln in enumerate(tits):
            _texto(d, (cx, y + 34 + 72 * k), ln, ft, MIEL, "mm", 255, borde=4)
        y += 72 * len(tits) + 12
        filete(d, cx, y, min(ancho * .40, 120 + 14 * len(titulo)), 255 * _eo((dt - .15) / .35))
        y += 40
        for i, ln in enumerate(lineas):
            _linea_rica(d, cx, y + 56 * i, ln, fx, 255 * _eo((dt - .35 - .26 * i) / .35))
        s = _reb(dt / .45) * (1 + .005 * math.sin(dt * 2.6))
        return _bgra(_escala(im, s), min(1.0, (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ rótulo de puesto con el Jiggy real
_jc = {}


def _jiggy(ruta, tam):
    k = (ruta, tam)
    if k not in _jc:
        im = Image.open(ruta).convert("RGBA")
        bb = im.getbbox()
        if bb:
            im = im.crop(bb)
        e = tam / max(im.size)
        _jc[k] = im.resize((max(2, int(im.width * e)), max(2, int(im.height * e))), Image.LANCZOS)
    return _jc[k]


def puesto(num, titulo, jiggy, ancho=None, etiqueta="JIGGY NÚMERO", sufijo="", max_ancho=None):
    """El Jiggy REAL gira sobre su eje vertical (se estrecha y se ensancha, como el que flota en el juego) con el número en
    Cooper encima; a su derecha, sobre humo, «JIGGY NÚMERO N» y el título que se escribe de izquierda a derecha.
    `max_ancho` (bt_50_secretos): el título se encoge y, si aún no cabe, se parte en dos líneas; `sufijo` va tras el número."""
    h, J = 320, 250
    fnum, fsup = fuente("t", 128), fuente("r", 32)
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    T, tam = titulo.upper(), 70
    tits = [T]
    if max_ancho:
        libre = max_ancho - (60 + J + 60 + 80)
        while tam > 52 and tmp.textlength(T, font=fuente("t", tam)) > libre:
            tam -= 2
        if tmp.textlength(T, font=fuente("t", tam)) > libre:
            tam = 62
            while True:
                tits = _partir(tmp, T, fuente("t", tam), libre)
                if tam <= 40 or (len(tits) <= 2 and max(tmp.textlength(x, font=fuente("t", tam)) for x in tits) <= libre):
                    break
                tam -= 2
    ftit = fuente("t", tam)
    tw = max(tmp.textlength(x, font=ftit) for x in tits)
    if ancho is None:
        ancho = int(max(1000, 60 + J + 60 + tw + 80))
    if len(tits) == 1:
        ys, ye, yf = [20], -48, 74
    else:
        paso = tam * 1.22
        ys = [14 - paso * (len(tits) - 1) / 2 + paso * i for i in range(len(tits))]
        ye, yf = ys[0] - tam * .5 - 32, ys[-1] + tam * .5 + 24

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        W, H = im.size
        capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(capa)
        x0 = M + 60 + J + 40
        cy = M + h / 2
        _texto(d, (x0, cy + ye), etiqueta + " " + str(num) + sufijo, fsup, AZUL_CLARO, "lm", 255 * _eo((dt - .3) / .35))
        for i, ln in enumerate(tits):
            _texto(d, (x0, cy + ys[i]), ln, ftit, CREMA, "lm", 255, borde=4)
        u = _eo((dt - .4) / .6)                                  # el título se descubre de izquierda a derecha
        m = np.zeros((H, W), np.uint8)
        m[:, :int(x0 + (tw + 20) * u)] = 255
        a = np.array(capa)
        a[..., 3] = np.minimum(a[..., 3], m)
        im.alpha_composite(Image.fromarray(a))
        d = ImageDraw.Draw(im)
        filete(d, x0 + tw / 2, cy + yf, min(tw / 2, 260), 255 * u)
        # Jiggy que gira: ancho = |cos| (nunca 0), con un destello cuando queda de frente
        jg = _jiggy(jiggy, J)
        ang = dt * 2.6 + .6
        sx = max(.10, abs(math.cos(ang)))
        k = _reb(dt / .5)
        j2 = jg.resize((max(2, int(jg.width * sx * k)), max(2, int(jg.height * k))), Image.BICUBIC)
        if math.cos(ang) < 0:                                   # la cara de atrás, un poco más oscura
            arr = np.array(j2)
            arr[..., :3] = (arr[..., :3] * .78).astype(np.uint8)
            j2 = Image.fromarray(arr)
        jx, jy = M + 60 + J / 2, cy + 8 * math.sin(dt * 2.0)
        im.alpha_composite(j2, (int(jx - j2.width / 2), int(jy - j2.height / 2)))
        if sx > .55:
            dd = ImageDraw.Draw(im)
            _texto(dd, (jx, jy + 8), str(num), fnum, CREMA, "mm", 255 * min(1.0, (sx - .55) / .25) * _eo(dt / .4),
                   borde=7, color_borde=CHOCO)
        return _bgra(im, min(1.0, (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ medidor de crueldad (panales)
def crueldad(nivel, total=5, titulo="CRUELDAD"):
    """Fila de panales como la barra de vida del juego: entran vacíos y se llenan de miel uno a uno; si `nivel` == `total`
    el último se llena en rojo y late."""
    R = 40
    ancho = 70 + total * (2 * R + 14) + 40
    h = 150
    ft = fuente("t", 40)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        luz = Image.new("RGBA", im.size, (0, 0, 0, 0))       # brillos aparte: ImageDraw no mezcla el alfa
        dl = ImageDraw.Draw(luz)
        _texto(d, (M + ancho / 2, M + 30), " ".join(titulo), ft, MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        y = M + 96
        for k in range(total):
            cx = M + 55 + R + k * (2 * R + 14)
            e = _reb((dt - .1 - .08 * k) / .4)
            if e <= 0:
                continue
            r = R * e
            d.polygon(_hex(cx, y, r), fill=(40, 24, 12, 200), outline=MIEL_OSC + (255,))
            u = _eo((dt - .5 - .22 * k) / .3) if k < nivel else 0
            if u > 0:
                rojo = nivel == total and k == total - 1
                lat = 1 + (.08 * math.sin(dt * 9) if rojo else 0)
                col = ROJO if rojo else MIEL
                d.polygon(_hex(cx, y, (r - 7) * u * lat), fill=col + (255,))
                dl.polygon(_hex(cx - 7, y - 9, (r - 7) * u * .32), fill=(255, 250, 225, 120))
        im.alpha_composite(luz)
        return _bgra(im, min(1.0, (dur - dt) / .35))
    return fn


# ======================================================================= MG de `bt_jiggies_crueles` (23-oct-2026)
VERDE_OK = (110, 230, 110)
_ic = {}


def _icono(ruta, tam, redondo=False):
    """Imagen real recortada a `tam` (lado mayor); `redondo` = medallón circular con aro miel."""
    k = (ruta, tam, redondo)
    if k not in _ic:
        im = Image.open(ruta).convert("RGBA")
        a = np.array(im)[..., 3]
        if (a < 10).mean() > .12:
            im = im.crop(im.getbbox())
        if redondo:
            s = min(im.size)
            im = im.crop(((im.width - s) // 2, 0, (im.width - s) // 2 + s, s)).resize((tam, tam), Image.LANCZOS)
            m = Image.new("L", (tam, tam), 0)
            ImageDraw.Draw(m).ellipse((0, 0, tam - 1, tam - 1), fill=255)
            fondo = Image.new("RGBA", (tam, tam), (60, 40, 24, 255))
            fondo.alpha_composite(im)
            fondo.putalpha(m)
            out = Image.new("RGBA", (tam + 12, tam + 12), (0, 0, 0, 0))
            ImageDraw.Draw(out).ellipse((0, 0, tam + 11, tam + 11), fill=MIEL + (255,))
            out.alpha_composite(fondo, (6, 6))
            im = out
        else:
            e = tam / max(im.size)
            im = im.resize((max(2, int(im.width * e)), max(2, int(im.height * e))), Image.LANCZOS)
        _ic[k] = im
    return _ic[k]


def _gris(ic, k=.5):
    a = np.array(ic)
    a[..., :3] = (a[..., :3].mean(axis=2, keepdims=True) * k).astype(np.uint8)
    return Image.fromarray(a)


def _pegar(im, ic, cx, cy, s=1.0, alfa=1.0):
    if s <= .02 or alfa <= .02:
        return
    if abs(s - 1) > .01:
        ic = ic.resize((max(2, int(ic.width * s)), max(2, int(ic.height * s))), Image.BICUBIC)
    if alfa < 1:
        a = np.array(ic)
        a[..., 3] = (a[..., 3] * alfa).astype(np.uint8)
        ic = Image.fromarray(a)
    im.alpha_composite(ic, (int(cx - ic.width / 2), int(cy - ic.height / 2)))


def _t(marcas, i, defecto=None):
    return marcas[i] if i < len(marcas) else defecto


def _reloj(d, cx, cy, r, frac, texto, rojo=False):
    """Esfera de reloj: anillo que se vacía (frac 1 -> 0) con los segundos en el centro."""
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(30, 16, 8, 210), outline=MIEL_OSC + (255,), width=4)
    if frac > 0:
        d.arc((cx - r + 8, cy - r + 8, cx + r - 8, cy + r - 8), -90, -90 + 360 * frac, fill=(ROJO if rojo else MIEL) + (255,),
              width=12)
    _texto(d, (cx, cy + 2), texto, fuente("t", int(r * .62)), ROJO if rojo else CREMA, "mm", 255, borde=3)


# ------------------------------------------------------------------ marcador con dos metas (Zubbas / olla de oro)
def marcador(titulo, metas, total, segundos, iconos=None, pasos=None, ancho=1300):
    """Barra de 0 a `total` con metas [(valor, etiqueta, ruta_icono)] que se encienden al alcanzarlas y un reloj de `segundos`
    que corre desde la marca 0 hasta el final. `pasos` = [(i_marca, valor)]: en esa marca la barra sube a `valor`.
    `iconos` = [(ruta, etiqueta)] en fila (Zubbas rojo/verde/azul con «1», «2», «3»), entran desde la marca 0."""
    h = (350 if iconos else 250) + 44 * max(0, len(metas) - 1)
    ft, fe, fn_ = fuente("t", 50), fuente("r", 33), fuente("t", 56)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        cx = M + ancho / 2
        _texto(d, (cx, M + 34), titulo, ft, MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        y = M + 70
        t0 = _t(marcas, 0, .4)
        if iconos:
            for k, (ruta, et) in enumerate(iconos):
                x = cx + (k - (len(iconos) - 1) / 2) * 240
                s = _reb((dt - t0 - .25 * k) / .4)
                if isinstance(ruta, tuple):                    # sin imagen real: panal del color (Zubbas)
                    r = 34 * max(0.0, s)
                    d.polygon(_hex(x - 40, y + 44 + 4 * math.sin(dt * 3 + k), r), fill=ruta + (255,), outline=CREMA + (255,))
                else:
                    _pegar(im, _icono(ruta, 76), x - 40, y + 44 + 4 * math.sin(dt * 3 + k), s)
                _texto(d, (x + 22, y + 46), et, fn_, CREMA, "lm", 255 * _eo((dt - t0 - .25 * k) / .3), borde=3)
            y += 104
        v = 0.0
        for i, val in (pasos or []):
            ti = _t(marcas, i)
            if ti is None or dt < ti:
                continue
            v = v + (val - v) * _eo((dt - ti) / 1.2)
        x0, x1, yb = M + 70, M + ancho - 200, y + 80
        d.rounded_rectangle((x0, yb - 22, x1, yb + 22), 22, fill=(30, 16, 8, 210), outline=MIEL_OSC + (255,), width=3)
        xv = x0 + (x1 - x0) * min(1.0, v / total)
        if xv > x0 + 10:
            d.rounded_rectangle((x0 + 4, yb - 18, xv, yb + 18), 18, fill=MIEL + (255,))
        for j, (val, et, ruta) in enumerate(metas):
            xm = x0 + (x1 - x0) * val / total
            ok = v >= val - .5
            col = VERDE_OK if ok else CREMA
            d.line([(xm, yb - 30), (xm, yb + 30 + 44 * j)], fill=col + (255,), width=5)
            _texto(d, (xm - 12, yb + 58 + 44 * j), f"{val} = {et}", fe, col, "rm", 255)   # escalonadas: no se enciman
            if ruta:
                s = (1.0 + .12 * math.sin(dt * 7)) if ok else .8
                ic = _icono(ruta, 64)
                _pegar(im, ic if ok else _gris(ic, .7), xm, yb - 72, s)
        _texto(d, (min(max(xv, x0 + 40), x1 - 40), yb + 2), str(int(round(v))), fuente("t", 34), CHOCO if xv > x0 + 60 else CREMA,
               "mm", 255 * _eo((dt - t0) / .3))
        rest = segundos if dt < t0 else max(0.0, segundos - (dt - t0) * segundos / max(1.0, dur - t0))
        _reloj(d, M + ancho - 95, yb, 64, rest / segundos, str(int(math.ceil(rest))), rojo=rest < segundos * .2)
        return _bgra(_escala(im, _reb(dt / .45)), min(1.0, (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ contrarreloj (dinamita / Clinkers)
def _tnt(d, cx, cy, s, apagado):
    w, h = 26 * s, 64 * s
    col = (120, 110, 100) if apagado else (205, 40, 32)
    d.rounded_rectangle((cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2), int(6 * s), fill=col + (255,), outline=(40, 20, 10, 255),
                        width=2)
    d.rectangle((cx - w / 2, cy - 6 * s, cx + w / 2, cy + 6 * s), fill=(160, 150, 140, 255) if apagado else (240, 220, 170, 255))
    if not apagado:
        d.line([(cx, cy - h / 2), (cx + 6 * s, cy - h / 2 - 14 * s)], fill=(60, 40, 20, 255), width=3)
        d.ellipse((cx + 3 * s, cy - h / 2 - 20 * s, cx + 12 * s, cy - h / 2 - 11 * s), fill=(255, 200, 40, 255))


def contrarreloj(titulo, n, segundos, icono=None, remate=None, gas=False, hasta=1.0, ancho=1240):
    """`n` objetivos (dinamita dibujada o `icono` real) en rejilla + reloj de `segundos`. Marca 0: arranca el reloj y entre
    la marca 0 y la 1 los objetivos caen uno a uno (gris + ✓ verde; `hasta` = fracción que cae, < 1 = no te da tiempo);
    marca 2: `remate` en rojo con destello (dinamita) o, con `gas`, una niebla verde tóxica que sube."""
    cols = 8 if n <= 16 else 10
    filas = math.ceil(n / cols)
    celda = 124
    h = 130 + filas * celda + (90 if remate else 30)
    ft = fuente("t", 50)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + 60, M + 56), titulo, ft, MIEL, "lm", 255 * _eo(dt / .3), borde=3)
        t0, t1, t2 = _t(marcas, 0, .5), _t(marcas, 1, dur * .7), _t(marcas, 2)
        hechos = 0 if dt < t0 else int(n * hasta * min(1.0, (dt - t0) / max(.5, t1 - t0)))   # hasta < 1: no llegas
        gx0 = M + 60 + (ancho - 120 - cols * celda) / 2
        for k in range(n):
            r, c = divmod(k, cols)
            cx, cy = gx0 + c * celda + celda / 2, M + 130 + r * celda + celda / 2
            s = _reb((dt - .15 - .03 * k) / .35)
            if s <= 0:
                continue
            apag = k < hechos
            if icono:
                ic = _icono(icono, 100)
                _pegar(im, _gris(ic) if apag else ic, cx, cy + 3 * math.sin(dt * 4 + k), s)
            else:
                _tnt(d, cx, cy + 2 * math.sin(dt * 5 + k), s * 1.45, apag)
            if apag:
                d.line([(cx - 30, cy + 4), (cx - 8, cy + 26), (cx + 32, cy - 26)], fill=VERDE_OK + (255,), width=7)
        rest = segundos if dt < t0 else max(0.0, segundos - (dt - t0) * segundos * .85 / max(1.0, dur - t0))
        _reloj(d, M + ancho - 110, M + 66, 58, rest / segundos, str(int(math.ceil(rest))), rojo=rest < segundos * .3)
        _texto(d, (M + ancho - 200, M + 66), f"{hechos}/{n}", fuente("t", 44), CREMA, "rm", 255 * _eo((dt - t0) / .3), borde=3)
        if t2 is not None and dt >= t2:
            u = dt - t2
            if gas:
                capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
                alto = int(im.size[1] * min(1.0, u / 2.0))
                dc = ImageDraw.Draw(capa)
                for j in range(10):
                    yy = im.size[1] - alto + (j % 3) * 30 + 12 * math.sin(dt * 2 + j)
                    xx = M + j * ancho / 9
                    dc.ellipse((xx - 150, yy, xx + 150, yy + 190), fill=(90, 200, 60, 80))
                im.alpha_composite(capa.filter(ImageFilter.GaussianBlur(16)))
            elif u < .6:                                     # destello redondo y difuminado, no un rectángulo
                fl = Image.new("RGBA", im.size, (0, 0, 0, 0))
                rr = 120 + 700 * u
                cx_, cy_ = im.size[0] / 2, im.size[1] / 2
                ImageDraw.Draw(fl).ellipse((cx_ - rr, cy_ - rr * .6, cx_ + rr, cy_ + rr * .6),
                                           fill=(255, 210, 110, int(190 * (1 - u / .6))))
                im.alpha_composite(fl.filter(ImageFilter.GaussianBlur(40)))
            if remate:
                _texto(ImageDraw.Draw(im), (M + ancho / 2, M + h - 52), remate, fuente("t", max(8, int(52 * _reb(u / .4)))), ROJO,
                       "mm", 255, borde=4, color_borde=CREMA)
        return _bgra(_escala(im, _reb(dt / .45)), min(1.0, (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ la carrera contra Canary Mary
def carrera(banjo, mary, ancho=1640):
    """Pista con Canary Mary (arriba) y Banjo (abajo) y el botón A que late con un contador de pulsaciones.
    Marca 0: arranca (Banjo gana terreno); marca 1: Banjo se le pega y Mary ACELERA (líneas de velocidad, «¡+!» rojo);
    marca 2: acelerón final de Mary pase lo que pase (gana ella); marca 3: el truco: se reinicia, Banjo se queda detrás y en
    la recta final machaca, la adelanta y llega primero («¡META!»)."""
    h = 470
    ib, imr = _icono(banjo, 140, redondo=True), _icono(mary, 140, redondo=True)

    def pos(dt, marcas):
        t0, t1, t2, t3 = (_t(marcas, i) for i in range(4))
        t0 = .5 if t0 is None else t0
        pb = pm = 0.0
        if dt >= t0:
            pm = .055 * (dt - t0)
            pb = pm * 1.15
        if t1 is not None and dt >= t1:
            base = .055 * (t1 - t0)
            pb = base * 1.15 + .045 * (dt - t1)
            pm = base + .085 * (dt - t1)
        if t2 is not None and dt >= t2:
            pb = min(.78, pb)
            pm = min(.97, pm + .3 * _eo((dt - t2) / .8))
        if t3 is not None and dt >= t3:
            u = dt - t3
            pm = .08 + .45 * min(1.0, u / 2.4) + .40 * _eo((u - 2.4) / 1.4)
            pb = .04 + .44 * min(1.0, u / 2.4) + .49 * _eo((u - 2.4) / 1.1)
        return min(.97, pb), min(.97, pm)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + ancho / 2, M + 40), "Canary Mary contra Banjo", fuente("t", 56), MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        x0, x1 = M + 200, M + ancho - 170
        t0 = _t(marcas, 0, .5)
        pb, pm = pos(dt, marcas)
        t1, t3 = _t(marcas, 1), _t(marcas, 3)
        for k, (y, p, ic) in enumerate(((M + 170, pm, imr), (M + 330, pb, ib))):
            d.rounded_rectangle((x0 - 20, y - 30, x1 + 20, y + 30), 30, fill=(30, 16, 8, 190), outline=MIEL_OSC + (200,), width=3)
            for j in range(12):
                xx = x0 + ((j * 110 - (dt - t0) * 160 * (dt > t0)) % (x1 - x0))
                d.line([(xx, y), (xx + 40, y)], fill=MIEL_OSC + (130,), width=3)
            x = x0 + (x1 - x0) * p
            if k == 0 and t1 is not None and dt >= t1 and (t3 is None or dt < t3):
                for j in range(4):
                    d.line([(x - 70 - j * 12, y - 24 + j * 16), (x - 150 - j * 12, y - 24 + j * 16)], fill=ROJO + (220,), width=4)
                _texto(d, (x + 72, y - 50), "¡+!", fuente("t", 44), ROJO, "mm", 255, borde=3, color_borde=CREMA)
            _pegar(im, ic, x, y - 6 * abs(math.sin(dt * 9 + k)) * (dt > t0), 1.0)
        d.rectangle((x1 + 30, M + 110, x1 + 50, M + 390), fill=CREMA + (255,))
        for j in range(10):
            d.rectangle((x1 + 30 + (j % 2) * 10, M + 110 + j * 28, x1 + 40 + (j % 2) * 10, M + 124 + j * 28), fill=CHOCO + (255,))
        golpe = abs(math.sin(dt * 22)) if dt >= t0 else 0
        r = 66 - 10 * golpe
        d.ellipse((M + 80 - r, M + 250 - r, M + 80 + r, M + 250 + r), fill=(60, 110, 230, 255), outline=CREMA + (255,), width=5)
        _texto(d, (M + 80, M + 252), "A", fuente("t", int(70 - 8 * golpe)), CREMA, "mm", 255, borde=2)
        n = 0 if dt < t0 else int((dt - t0) * 9)
        _texto(d, (M + 80, M + 360), f"x{n}", fuente("r", 40), MIEL, "mm", 255 * _eo((dt - t0) / .3))
        if t3 is not None and dt > t3 + 3.8:
            _texto(d, (M + ancho / 2, M + h - 34), "¡META!", fuente("t", max(8, int(64 * _reb((dt - t3 - 3.8) / .4)))), VERDE_OK,
                   "mm", 255, borde=4)
        return _bgra(_escala(im, _reb(dt / .45)), min(1.0, (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ recados (Scrotty) y cadena de requisitos (Weldar)
def recados(titulo, madre, hijos, premio, ancho=1640):
    """La madre a la izquierda; `hijos` = [(ruta, nombre, problema, solucion)]: en la marca k entra el hijo k con su problema
    (rojo) y una flecha hacia la solución; en la marca n+k se marca con ✓. Marca 2n: el Jiggy de premio vuela al centro;
    marca 2n+1: «¿OTRO?» y un sello rojo «NO»."""
    n = len(hijos)
    h = 170 + n * 150
    im_m = _icono(madre, 240)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + ancho / 2, M + 40), titulo, fuente("t", 50), MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        _pegar(im, im_m, M + 150, M + h / 2 + 30 + 5 * math.sin(dt * 2), _reb(dt / .5))
        fr, fs = fuente("t", 40), fuente("r", 30)
        tj = _t(marcas, 2 * n)
        dim = 1.0 - .78 * _eo((dt - tj) / .5) if tj is not None and dt >= tj else 1.0   # el premio pasa al frente
        filas = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(filas)
        for k, (ruta, nom, prob, sol) in enumerate(hijos):
            tk = _t(marcas, k)
            if tk is None or dt < tk:
                continue
            y = M + 140 + k * 150
            _pegar(filas, _icono(ruta, 110, redondo=True), M + 390, y + 4 * math.sin(dt * 3 + k), _reb((dt - tk) / .4))
            a = 255 * _eo((dt - tk - .2) / .3)
            _texto(d, (M + 470, y - 24), nom, fr, CREMA, "lm", a, borde=3)
            _texto(d, (M + 470, y + 24), prob, fs, (255, 150, 130), "lm", a)
            u = _eo((dt - tk - .5) / .6)
            if u > 0:
                xa = M + 920
                xb = xa + 150 * u
                d.line([(xa, y), (xb, y)], fill=MIEL + (255,), width=6)
                if u > .9:
                    d.polygon([(xb, y - 14), (xb + 22, y), (xb, y + 14)], fill=MIEL + (255,))
                    _texto(d, (M + 1110, y), sol, fs, CREMA, "lm", 255 * _eo((dt - tk - 1.0) / .3))
            tc = _t(marcas, n + k)
            if tc is not None and dt >= tc:
                s2 = _reb((dt - tc) / .35)
                d.line([(M + 300, y + 6), (M + 324, y + 6 + 30 * s2), (M + 324 + 44 * s2, y + 6 - 40 * s2)], fill=VERDE_OK + (255,),
                       width=10)
        if dim < 1:
            a = np.array(filas)
            a[..., 3] = (a[..., 3] * dim).astype(np.uint8)
            filas = Image.fromarray(a)
        im.alpha_composite(filas)
        d = ImageDraw.Draw(im)
        if tj is not None and dt >= tj:
            u = _eo((dt - tj) / .8)
            _pegar(im, _jiggy(premio, 150), M + 150 + (ancho - 480) * u, M + h / 2 + 30 - 120 * math.sin(u * math.pi), .6 + .4 * u)
        tn = _t(marcas, 2 * n + 1)
        if tn is not None and dt >= tn:
            _texto(d, (M + ancho - 300, M + h / 2 - 80), "¿OTRO?", fuente("t", 46), CREMA, "mm", 255 * _eo((dt - tn) / .3), borde=3)
            if dt - tn > .5:
                sello = Image.new("RGBA", (260, 140), (0, 0, 0, 0))
                ds = ImageDraw.Draw(sello)
                ds.rounded_rectangle((6, 6, 254, 134), 18, outline=ROJO + (255,), width=10)
                _texto(ds, (130, 72), "NO", fuente("t", 90), ROJO, "mm", 255)
                sello = sello.rotate(-14, expand=True, resample=Image.BICUBIC)
                _pegar(im, sello, M + ancho - 300, M + h / 2 + 40, max(.05, 2.2 - 1.2 * _eo((dt - tn - .5) / .25)))
        return _bgra(_escala(im, _reb(dt / .45)), min(1.0, (dur - dt) / .35))
    return fn


def cadena(titulo, pasos, final, ancho=1720):
    """Pasos [(ruta o None, texto)] en fila unidos por flechas: en la marca k se enciende el paso k (los demás esperan
    grises); en la marca len(pasos) aparece `final` = (ruta, texto) en rojo, latiendo."""
    n = len(pasos)
    h = 440
    paso_x = (ancho - 340) / max(1, n)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + ancho / 2, M + 40), titulo, fuente("t", 48), MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        fs = fuente("r", 33)
        for k, (ruta, txt) in enumerate(pasos):
            cx, cy = M + 100 + k * paso_x, M + 180
            tk = _t(marcas, k, .4 + .5 * k)
            on = dt >= tk
            s = _reb((dt - tk) / .4) if on else .85
            if k < n - 1:
                d.line([(cx + 66, cy), (cx + paso_x - 66, cy)], fill=(90, 70, 50, 220), width=4)
                u = _eo((dt - tk) / .4) if on else 0
                if u > 0:
                    d.line([(cx + 66, cy), (cx + 66 + (paso_x - 132) * u, cy)], fill=MIEL + (255,), width=7)
            elif _t(marcas, n) is not None:
                d.line([(cx + 66, cy), (M + ancho - 210, cy)], fill=(90, 70, 50, 220), width=4)
            if ruta:
                ic = _icono(ruta, 140, redondo=True)
                _pegar(im, ic if on else _gris(ic), cx, cy + (3 * math.sin(dt * 3 + k) if on else 0), s)
            else:
                d.polygon(_hex(cx, cy, 66 * s), fill=(MIEL if on else (90, 70, 50)) + (255,))
            for j, ln in enumerate(_partir(d, txt, fs, paso_x - 14)):
                _texto(d, (cx, cy + 106 + 36 * j), ln, fs, CREMA if on else (150, 130, 110), "mm", 255)
        tf = _t(marcas, n)
        if tf is not None and dt >= tf:
            ruta, txt = final
            cx, cy = M + ancho - 140, M + 180
            k = _reb((dt - tf) / .4) * (1 + .06 * math.sin(dt * 8))
            if ruta:
                _pegar(im, _icono(ruta, 180, redondo=True), cx, cy, k)
            else:                       # final sin imagen (bt_50_secretos): panal rojo que late
                d.polygon(_hex(cx, cy, 80 * k), fill=ROJO + (255,))
            ff = fuente("t", 44 if len(txt) <= 14 else 34)
            for j, ln in enumerate(_partir(d, txt, ff, 300)):     # el final se parte: nunca se sale por la derecha
                _texto(d, (cx, cy + 124 + 40 * j), ln, ff, ROJO, "mm", 255 * _eo((dt - tf) / .3), borde=3, color_borde=CREMA)
        return _bgra(_escala(im, _reb(dt / .45)), min(1.0, (dur - dt) / .35))
    return fn


# ======================================================================= MG de `bt_mundos_ranking` (30-oct-2026)
def egg(num, titulo):
    """Contador de Easter eggs del video: huevo azul moteado (los de Kazooie) que rebota con el número y, a su derecha,
    «EASTER EGG» + título. Pequeño, para una esquina: no tapa el juego."""
    ftit, fsup, fnum = fuente("t", 44), fuente("r", 26), fuente("t", 50)
    tw = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textlength(titulo, font=ftit)
    ancho, h = int(max(430, 190 + tw + 50)), 134

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        cx, cy = M + 82, M + h / 2 + 2 * math.sin(dt * 3)
        e = _reb(dt / .45)
        rx, ry = 44 * e, 56 * e
        d.ellipse((cx - rx, cy - ry, cx + rx, cy + ry), fill=(70, 132, 220, 255), outline=CREMA + (255,), width=3)
        for a, r, s in ((.7, .55, 7), (2.3, .62, 6), (3.9, .5, 8), (5.2, .68, 5)):
            px, py = cx + rx * r * math.cos(a), cy + ry * r * math.sin(a)
            d.ellipse((px - s * e, py - s * e, px + s * e, py + s * e), fill=MIEL + (255,))
        _texto(d, (cx, cy + 2), str(num), fnum, CREMA, "mm", 255 * _eo((dt - .15) / .25), borde=4, color_borde=CHOCO)
        x0 = M + 150
        _texto(d, (x0, M + 44), "EASTER EGG", fsup, AZUL_CLARO, "lm", 255 * _eo((dt - .2) / .3))
        _texto(d, (x0, M + 88), titulo, ftit, MIEL, "lm", 255 * _eo((dt - .3) / .3), borde=3)
        return _bgra(im, min(1.0, (dur - dt) / .35))
    return fn


def cuatro_listas(titulo, filas, media, ancho=1180):
    """Dónde pone cada lista a este mundo. filas = [(nombre, celdas, indice_encendido)], p. ej. ("MrDrBoi", list("12345678"), 7)
    o ("Super Joe Bros", list("SABCDE"), 4). Cada fila se enciende en su marca; `media` sale tras la última fila."""
    n = len(filas)
    fila_h = 92
    h = 128 + n * fila_h + 96
    fn_nom, fcel, fmed = fuente("r", 33), fuente("t", 34), fuente("t", 50)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + ancho / 2, M + 50), titulo, fuente("t", 50), MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        filete(d, M + ancho / 2, M + 96, 300, 255 * _eo((dt - .1) / .3))
        for k, (nom, celdas, on) in enumerate(filas):
            y = M + 158 + k * fila_h
            tk = _t(marcas, k, .5 + .55 * k)
            _texto(d, (M + 60, y), nom, fn_nom, CREMA, "lm", 255 * _eo((dt - .2 - .1 * k) / .3))
            paso = 62
            for j, c in enumerate(celdas):
                cx = M + 372 + j * paso + (8 - len(celdas)) * paso / 2
                lit = j == on and dt >= tk
                r = 28 * _reb((dt - .3 - .03 * j) / .35) * (1 + (.16 * math.sin(dt * 7) if lit else 0))
                if r <= 0:
                    continue
                col = (ROJO if on >= len(celdas) - 2 else MIEL) if lit else (60, 38, 22)
                d.polygon(_hex(cx, y, r), fill=col + (255 if lit else 190,), outline=MIEL_OSC + (255,))
                _texto(d, (cx, y + 1), c, fcel, CHOCO if lit else (150, 124, 96), "mm", 255)
        tm = _t(marcas, n, .6 + .55 * n)
        if dt >= tm:
            _texto(d, (M + ancho / 2, M + h - 58), media, fmed, CREMA, "mm", 255 * _eo((dt - tm) / .3), borde=4)
        return _bgra(_escala(im, _reb(dt / .45)), min(1.0, (dur - dt) / .35))
    return fn


def ruleta(n=1000, cols=50, ancho=1320):
    """1000 casillas iguales que se apagan una tras otra; en la marca 0 queda UNA encendida (dorada, latiendo)."""
    filas = n // cols
    c = (ancho - 120) // cols
    h = 150 + filas * c + 110
    gano = cols * (filas // 2) + cols * 2 // 3          # la que queda: nunca en el borde
    orden = np.random.RandomState(7).permutation(n)     # las demás se apagan en un orden fijo

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + ancho / 2, M + 56), "UNA PUERTA, MIL INTENTOS", fuente("t", 50), MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        tm = _t(marcas, 0, 1.6)
        u = min(1.0, max(0.0, dt - .3) / max(.4, tm - .3))
        apagada = np.zeros(n, bool)
        apagada[orden[:int(u * (n - 1))]] = True
        x0, y0 = M + 60, M + 112
        for i in range(n):
            if i == gano:
                continue
            px, py = x0 + (i % cols) * c, y0 + (i // cols) * c
            d.rectangle((px + 2, py + 2, px + c - 3, py + c - 3), fill=(46, 30, 18, 200) if apagada[i] else (120, 92, 60, 255))
        px, py = x0 + (gano % cols) * c, y0 + (gano // cols) * c
        lat = 1 + .3 * math.sin(dt * 8)
        r = c / 2 + (12 * _reb((dt - tm) / .4) * lat if dt >= tm else 0)
        d.rectangle((px + c / 2 - r, py + c / 2 - r, px + c / 2 + r, py + c / 2 + r), fill=MIEL + (255,), outline=CREMA + (255,))
        if dt >= tm:
            _texto(d, (M + ancho / 2, M + h - 58), "1 de cada 1000", fuente("t", 56), CREMA, "mm", 255 * _eo((dt - tm) / .3), borde=4)
        return _bgra(_escala(im, _reb(dt / .45)), min(1.0, (dur - dt) / .35))
    return fn


def codigos(filas, ancho=1500):
    """La Cámara de Códigos: filas = [(escrito, al_derecho, efecto)]. En la marca k un huevo golpea las letras de la fila k una a
    una (tejas de piedra que se encienden) y luego salen la palabra al derecho y lo que hace."""
    n = len(filas)
    fila_h = 128
    h = 124 + n * fila_h + 26
    fl, fd, fe = fuente("t", 56), fuente("t", 52), fuente("r", 34)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + ancho / 2, M + 50), "CÁMARA DE CÓDIGOS", fuente("t", 50), MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        filete(d, M + ancho / 2, M + 96, 300, 255 * _eo((dt - .1) / .3))
        for k, (esc, der, ef) in enumerate(filas):
            y = M + 180 + k * fila_h
            tk = _t(marcas, k, .5 + 1.4 * k)
            x0 = M + 70
            for j, c in enumerate(esc):
                cx = x0 + j * 80
                tj = tk + .16 * j
                on = dt >= tj
                r = 36 * ((1 + .25 * max(0.0, 1 - (dt - tj) / .2)) if on else 1)
                d.rounded_rectangle((cx - r, y - r, cx + r, y + r), 10, fill=(MIEL if on else (82, 70, 58)) + (255,),
                                    outline=(CREMA if on else (120, 104, 86)) + (255,), width=3)
                _texto(d, (cx, y), c, fl, CHOCO if on else CREMA, "mm", 255)
            tr = tk + .16 * len(esc) + .15
            if dt >= tr:
                xf = x0 + len(esc) * 80 + 14
                _texto(d, (xf, y), "=", fd, CREMA, "lm", 255 * _eo((dt - tr) / .25))
                _texto(d, (xf + 70, y - 22), der, fd, MIEL, "lm", 255 * _eo((dt - tr - .1) / .25), borde=3)
                _texto(d, (xf + 70, y + 32), ef, fe, CREMA, "lm", 255 * _eo((dt - tr - .2) / .25))
        return _bgra(_escala(im, _reb(dt / .45)), min(1.0, (dur - dt) / .35))
    return fn


def conexiones(nodos, enlaces, ancho=1760, alto=900):
    """Los mundos conectados: nodos = {clave: (ruta_img, x, y)} (fracciones) y enlaces = [(a, b, rótulo)]; cada enlace se traza
    en su marca, de a hacia b, con bolitas miel que corren por él."""
    def fn(dt, dur, marcas):
        im, M = humo(ancho, alto)
        d = ImageDraw.Draw(im)
        pos = lambda k: (M + nodos[k][1] * ancho, M + nodos[k][2] * alto)
        fr = fuente("r", 30)
        for i, (a, b, txt) in enumerate(enlaces):
            tk = _t(marcas, i, .6 + 1.1 * i)
            ax, ay = pos(a)
            bx, by = pos(b)
            d.line([(ax, ay), (bx, by)], fill=(90, 70, 50, 180), width=4)
            u = _eo((dt - tk) / .7) if dt >= tk else 0
            if u > 0:
                d.line([(ax, ay), (ax + (bx - ax) * u, ay + (by - ay) * u)], fill=MIEL + (255,), width=8)
                for q in range(3):
                    v = ((dt * .5 + q / 3) % 1) * u
                    x, y = ax + (bx - ax) * v, ay + (by - ay) * v
                    d.ellipse((x - 9, y - 9, x + 9, y + 9), fill=CREMA + (255,))
                _texto(d, ((ax + bx) / 2, (ay + by) / 2 - 24), txt, fr, CREMA, "mm", 255 * _eo((dt - tk - .3) / .3), borde=3,
                       color_borde=CHOCO)
        for j, (k, (ruta, _x, _y)) in enumerate(nodos.items()):
            cx, cy = pos(k)
            ic = _jiggy(ruta, 350)
            e = _reb((dt - .05 * j) / .4)
            if e > 0:
                aw, ah = (ic.width / 2 + 26) * e, (ic.height / 2 + 22) * e
                d.rounded_rectangle((cx - aw, cy - ah, cx + aw, cy + ah), 22, fill=(30, 16, 8, 235), outline=MIEL + (255,), width=3)
            _pegar(im, ic, cx, cy, e * (1 + .02 * math.sin(dt * 2.4 + j)))
        return _bgra(_escala(im, _reb(dt / .45)), min(1.0, (dur - dt) / .35))
    return fn


def ficha_mundo(items, ancho=None):
    """Tira baja al presentar un mundo: items = [(ruta, etiqueta, nombre)] (JEFE / TRANSFORMACIÓN…), uno tras otro con rebote."""
    n = len(items)
    ancho = ancho or 90 + n * 430
    h = 190
    fe, fnom = fuente("r", 24), fuente("t", 38)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        for k, (ruta, et, nom) in enumerate(items):
            x = M + 50 + k * 430
            tk = .15 + .3 * k
            _pegar(im, _icono(ruta, 136, redondo=True), x + 70, M + h / 2 + 3 * math.sin(dt * 2.6 + k), _reb((dt - tk) / .4))
            _texto(d, (x + 152, M + h / 2 - 28), " ".join(et.upper()), fe, AZUL_CLARO, "lm", 255 * _eo((dt - tk) / .3))
            _texto(d, (x + 152, M + h / 2 + 18), nom, fnom, MIEL, "lm", 255 * _eo((dt - tk - .1) / .3), borde=3)
        return _bgra(im, min(1.0, (dur - dt) / .35))
    return fn


# ======================================================================= MG de `bt_50_secretos` (3-nov-2026)
# Todas aceptan las marcas de la voz (s desde el inicio del MG); si faltan, usan fracciones fijas `q` de la duración.
_RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _jiggy_def():
    for v in ("bt_50_secretos", "bt_mundos_ranking", "bt_jiggies_crueles"):
        p = os.path.join(_RAIZ, "videos", v, "pegatinas", "jiggy.png")
        if os.path.exists(p):
            return p
    raise FileNotFoundError("falta pegatinas/jiggy.png: pasa `jiggy=` con la ruta del Jiggy real")


def _mq(marcas, i, dur, q):
    """Marca i de la voz (s) o, si no viene, la fracción q de la duración del MG."""
    return marcas[i] if marcas and i < len(marcas) else q * dur


def _ajustar(s, estilo, tam, ancho, minimo=34):
    tmp = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    while tam > minimo and tmp.textlength(s, font=fuente(estilo, tam)) > ancho:
        tam -= 2
    return fuente(estilo, tam)


def _vacia(im):
    return Image.new("RGBA", im.size, (0, 0, 0, 0))


def _encajar(ruta, wmax, hmax):
    """Imagen real recortada que cabe en wmax x hmax sin deformarse (las fotos anchas no se quedan diminutas)."""
    k = ("enc", ruta, wmax, hmax)
    if k not in _ic:
        im = _icono(ruta, max(wmax, hmax) * 2)
        e = min(wmax / im.width, hmax / im.height)
        _ic[k] = im.resize((max(2, int(im.width * e)), max(2, int(im.height * e))), Image.LANCZOS)
    return _ic[k]


def _salida(im, dt, dur):
    return _bgra(_escala(im, _reb(dt / .45)), min(1.0, (dur - dt) / .35))


def _tacha(d, cx, cy, r, u, ancho=9, color=ROJO):
    """X roja que se traza (u 0 -> 1): primero un trazo y luego el otro."""
    a, b = min(1.0, u * 2), max(0.0, u * 2 - 1)
    if a > 0:
        d.line([(cx - r, cy - r), (cx - r + 2 * r * a, cy - r + 2 * r * a)], fill=color + (255,), width=ancho)
    if b > 0:
        d.line([(cx + r, cy - r), (cx + r - 2 * r * b, cy - r + 2 * r * b)], fill=color + (255,), width=ancho)


# ------------------------------------------------------------------ 1. rótulo de secreto + contador de esquina
def secreto(num, titulo, total=50, jiggy=None):
    """Rótulo grande de cada secreto (~4 s): el Jiggy real gira con el número, «SECRETO N DE 50» y el título, que se encoge
    o se parte en dos líneas para no pasar de 1500 px. El contador de esquina va aparte: `contador(num, total)`."""
    return puesto(num, titulo, jiggy or _jiggy_def(), etiqueta="SECRETO", sufijo=f" DE {total}", max_ancho=1500)


def contador(num, total=50, jiggy=None):
    """HUD de esquina que dura TODO el secreto: Jiggy real pequeño que gira despacio + «N/50» en Cooper miel (las cifras caen
    al entrar). Da ritmo en un video largo sin tapar el juego."""
    ruta = jiggy or _jiggy_def()
    s = f"{num}/{total}"
    fnum = fuente("t", 58)
    tw = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textlength(s, font=fnum)
    ancho, h = int(122 + tw + 36), 112

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        jg = _jiggy(ruta, 86)
        ang = dt * 1.4 + .4
        sx = max(.14, abs(math.cos(ang)))
        k = _reb(dt / .45)
        j2 = jg.resize((max(2, int(jg.width * sx * k)), max(2, int(jg.height * k))), Image.BICUBIC)
        if math.cos(ang) < 0:
            arr = np.array(j2)
            arr[..., :3] = (arr[..., :3] * .78).astype(np.uint8)
            j2 = Image.fromarray(arr)
        _pegar(im, j2, M + 62, M + h / 2 + 3 * math.sin(dt * 2))
        d = ImageDraw.Draw(im)
        u = _eo((dt - .12) / .35)
        _texto(d, (M + 118, M + h / 2 + 4 - 34 * (1 - u)), s, fnum, MIEL, "lm", 255 * u, borde=4)
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ 2. comparativa N64 <-> XBOX 360 / JAPÓN
def versus(izq, der, titulo=None, marca="CAMBIÓ", col_w=530):
    """Dos columnas translúcidas: izq/der = dict(etiqueta, texto, icono=None). Marca 0: entra la izquierda; marca 1: la
    derecha (antes, un hueco con «?»); marca 2: flecha entre ellas y sello rojo `marca` («CAMBIÓ»; None = solo flecha)."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    fx = fuente("r", 36)
    hueco = 280
    ancho = 2 * col_w + hueco + 60
    lados = []
    for s in (izq, der):
        fe = _ajustar(s["etiqueta"].upper(), "t", 46, col_w - 50)
        lados.append((s, fe, _partir(tmp, s.get("texto", ""), fx, col_w - 60)))
    con_ic = any(s.get("icono") for s in (izq, der))
    IC = 190
    nl = max(len(l[2]) for l in lados)
    alto = 104 + (IC + 24 if con_ic else 0) + 48 * nl + 24
    top = 86 if titulo else 22
    h = top + alto + 26
    fts = _ajustar(titulo, "t", 50, ancho - 100) if titulo else None
    fsel = fuente("t", 44)

    def columna(k, dt, tk):
        s, fe, lin = lados[k]
        c = Image.new("RGBA", (col_w + 20, alto + 20), (0, 0, 0, 0))
        d = ImageDraw.Draw(c)
        d.rounded_rectangle((10, 10, col_w + 10, alto + 10), 30, fill=(58, 34, 16, 92),
                            outline=(MIEL if k else MIEL_OSC) + (230,), width=3)
        cx = 10 + col_w / 2
        _texto(d, (cx, 56), s["etiqueta"].upper(), fe, MIEL if k else CREMA, "mm", 255, borde=3)
        filete(d, cx, 98, col_w * .30, 255 * _eo((dt - tk - .15) / .3))
        y = 118
        if con_ic:
            if s.get("icono"):
                _pegar(c, _encajar(s["icono"], col_w - 80, IC), cx, y + IC / 2 + 4 * math.sin(dt * 2.4 + k))
            y += IC + 24
        d = ImageDraw.Draw(c)
        for i, ln in enumerate(lin):
            _linea_rica(d, cx, y + 20 + 48 * i, ln, fx, 255 * _eo((dt - tk - .3 - .18 * i) / .3))
        return c

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        if titulo:
            _texto(d, (M + ancho / 2, M + 48), titulo, fts, MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        t0, t1 = _mq(marcas, 0, dur, .04), _mq(marcas, 1, dur, .40)
        t2 = _mq(marcas, 2, dur, min(.9, t1 / max(dur, .01) + .14))
        yc = M + top + alto / 2 + 10
        xs = (M + 30 + col_w / 2, M + ancho - 30 - col_w / 2)
        for k, tk in ((0, t0), (1, t1)):
            if dt < tk:
                if k == 1:                                     # hueco que espera a la otra versión
                    cap = _vacia(im)
                    dc = ImageDraw.Draw(cap)
                    x0, y0 = xs[1] - col_w / 2, yc - alto / 2
                    for j in range(0, int(col_w), 36):
                        dc.line([(x0 + j, y0), (x0 + j + 18, y0)], fill=MIEL_OSC + (150,), width=3)
                        dc.line([(x0 + j, y0 + alto), (x0 + j + 18, y0 + alto)], fill=MIEL_OSC + (150,), width=3)
                    for j in range(0, int(alto), 36):
                        dc.line([(x0, y0 + j), (x0, y0 + j + 18)], fill=MIEL_OSC + (150,), width=3)
                        dc.line([(x0 + col_w, y0 + j), (x0 + col_w, y0 + j + 18)], fill=MIEL_OSC + (150,), width=3)
                    _texto(dc, (xs[1], yc), "?", fuente("t", int(120 + 8 * math.sin(dt * 4))), MIEL_OSC, "mm", 170, borde=3)
                    im.alpha_composite(cap)
                continue
            u = (dt - tk) / .45
            off = (1 - _eo(u)) * (130 if k else -130)
            _pegar(im, columna(k, dt, tk), xs[k] + off, yc, max(.05, _reb(u)), min(1.0, _eo(u / .5)))
        if dt >= t2:
            d = ImageDraw.Draw(im)
            u = _eo((dt - t2) / .4)
            xa, xb = M + 40 + col_w + 28, M + ancho - 40 - col_w - 28
            xe = xa + (xb - xa - 26) * u
            d.line([(xa, yc), (xe, yc)], fill=MIEL + (255,), width=11)
            d.polygon([(xe, yc - 22), (xe + 30, yc), (xe, yc + 22)], fill=MIEL + (255,))
            if marca and dt >= t2 + .25:
                tw = d.textlength(marca, font=fsel)
                sello = Image.new("RGBA", (int(tw + 44), 84), (0, 0, 0, 0))
                ds = ImageDraw.Draw(sello)
                ds.rounded_rectangle((4, 4, sello.width - 4, 80), 14, fill=(40, 14, 8, 150), outline=ROJO + (255,), width=6)
                _texto(ds, (sello.width / 2, 44), marca, fsel, ROJO, "mm", 255, borde=2, color_borde=CREMA)
                sello = sello.rotate(8, expand=True, resample=Image.BICUBIC)
                s = max(.05, 2.2 - 1.2 * _eo((dt - t2 - .25) / .25)) * (1 + .04 * math.sin(dt * 7))
                _pegar(im, sello, (xa + xb) / 2, yc - 84, s)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ 3. el concurso de Tower of Tragedy
def concurso(pregunta, opciones, correcta, trampa=None, titulo="TOWER OF TRAGEDY", ancho=1300):
    """Tarjeta del concurso: pregunta arriba y las opciones que CAEN una a una (marca k = opción k); marca n: la correcta
    se enciende en miel con ✓ y, poco después, la `trampa` (índice) se tacha en rojo."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    fq, fl, fsup = fuente("t", 48), fuente("t", 40), fuente("r", 34)
    ql = _partir(tmp, pregunta, fq, ancho - 130)
    n = len(opciones)
    OP = 94
    top = 92 + 58 * len(ql) + 30
    h = top + n * OP + 24
    fos = [_ajustar(o, "r", 40, ancho - 290) for o in opciones]

    def opcion(k, dt, tr):
        w, oh = ancho - 120, 80
        c = Image.new("RGBA", (w + 16, oh + 16), (0, 0, 0, 0))
        d = ImageDraw.Draw(c)
        lit = dt >= tr and k == correcta
        trap = trampa is not None and k == trampa and dt >= tr + .3
        otra = dt >= tr and not lit and not trap
        if lit:
            fill, borde, ctxt = MIEL + (235,), CREMA, CHOCO
        elif trap:
            fill, borde, ctxt = (70, 18, 10, 170), ROJO, (255, 160, 140)
        else:
            fill, borde, ctxt = (52, 30, 14, 150 if not otra else 110), MIEL_OSC, CREMA if not otra else (190, 170, 150)
        d.rounded_rectangle((8, 8, w + 8, oh + 8), 40, fill=fill, outline=borde + (255,), width=3)
        cy = 8 + oh / 2
        d.polygon(_hex(58, cy, 30), fill=(CHOCO if lit else MIEL) + (255,))
        _texto(d, (58, cy + 2), "ABCDEFG"[k], fl, MIEL if lit else CHOCO, "mm", 255)
        _texto(d, (104, cy), opciones[k], fos[k], ctxt, "lm", 255, borde=(2 if lit else 0), color_borde=MIEL)
        if lit:
            u = _reb((dt - tr) / .35)
            d.line([(w - 62, cy + 2), (w - 46, cy + 2 + 18 * u), (w - 46 + 30 * u, cy + 2 - 26 * u)], fill=CHOCO + (255,), width=8)
        if trap:
            u = _eo((dt - tr - .3) / .35)
            tw = d.textlength(opciones[k], font=fos[k])
            d.line([(96, cy + 2), (96 + (tw + 20) * u, cy + 2)], fill=ROJO + (255,), width=8)
            _tacha(d, w - 46, cy, 18, _eo((dt - tr - .5) / .3), 8)
        return c

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        cx = M + ancho / 2
        _texto(d, (cx, M + 40), " ".join(titulo.upper()), fsup, AZUL_CLARO, "mm", 255 * _eo(dt / .3))
        for i, ln in enumerate(ql):
            _texto(d, (cx, M + 96 + 58 * i), ln, fq, MIEL, "mm", 255 * _eo((dt - .1) / .3), borde=3)
        filete(d, cx, M + top - 22, 260, 255 * _eo((dt - .2) / .3))
        tr = _mq(marcas, n, dur, .62)
        for k in range(n):
            tk = _mq(marcas, k, dur, .14 + .13 * k)
            if dt < tk:
                continue
            u = (dt - tk) / .5
            y = M + top + k * OP + OP / 2 - 240 * (1 - _reb(u))
            lat = 1 + .025 * math.sin(dt * 8) if (dt >= tr and k == correcta) else 1.0
            _pegar(im, opcion(k, dt, tr), cx, y, lat, min(1.0, _eo(u / .4)))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ 4. las comprobaciones antipiratería
def _cartucho_chip(d, cx, cy, s, luz, alarma):
    """Cartucho de N64 esquemático (parte alta ancha con agarres, parte baja que se estrecha) con una ventana a la placa y
    su chip (patas plateadas) y un led que parpadea; asoman los contactos dorados."""
    w, hh = 250 * s, 230 * s
    x0, y0, x1, y1 = cx - w / 2, cy - hh / 2, cx + w / 2, cy + hh / 2
    ym = y0 + hh * .70
    d.rectangle((cx - w * .36, y1 - 4 * s, cx + w * .36, y1 + 12 * s), fill=(40, 100, 60, 255))
    for k in range(13):                                       # contactos dorados que asoman
        x = cx - w * .33 + k * w * .66 / 12
        d.rectangle((x - 3 * s, y1 - 2 * s, x + 3 * s, y1 + 11 * s), fill=(214, 172, 66, 255))
    gris, osc = (96, 96, 106, 255), (20, 20, 24, 255)
    d.rounded_rectangle((x0, y0, x1, ym + 10 * s), int(22 * s), fill=gris, outline=osc, width=3)
    d.polygon([(x0, ym), (x1, ym), (x1 - w * .08, y1), (x0 + w * .08, y1)], fill=gris, outline=osc)
    d.line([(x0 + 2, ym), (x1 - 2, ym)], fill=gris, width=4)
    for k in range(7):                                        # agarres estriados a los lados
        y = y0 + 34 * s + k * 13 * s
        for xa in (x0 + 8 * s, x1 - 26 * s):
            d.line([(xa, y), (xa + 18 * s, y)], fill=(62, 62, 70, 255), width=3)
    wx0, wy0, wx1, wy1 = x0 + 40 * s, y0 + 26 * s, x1 - 40 * s, ym - 8 * s
    d.rounded_rectangle((wx0, wy0, wx1, wy1), int(10 * s), fill=(34, 92, 58, 255), outline=osc, width=3)
    for k in range(4):                                        # pistas de la placa
        y = wy0 + 18 * s + k * 22 * s
        d.line([(wx0 + 10 * s, y), (wx0 + 40 * s, y), (wx0 + 50 * s, y + 8 * s)], fill=(90, 170, 110, 255), width=2)
    cw, ch = 92 * s, 60 * s
    qx, qy = (wx0 + wx1) / 2 + 18 * s - cw / 2, (wy0 + wy1) / 2 - ch / 2
    for k in range(6):
        x = qx + 8 * s + k * 15 * s
        d.line([(x, qy - 8 * s), (x, qy)], fill=(200, 200, 210, 255), width=3)
        d.line([(x, qy + ch), (x, qy + ch + 8 * s)], fill=(200, 200, 210, 255), width=3)
    d.rectangle((qx, qy, qx + cw, qy + ch), fill=(16, 16, 18, 255), outline=(80, 80, 90, 255), width=2)
    d.line([(qx + 8 * s, qy + 10 * s), (qx + cw * .5, qy + 10 * s)], fill=(70, 70, 80, 255), width=2)
    col = ROJO if alarma else MIEL
    r = 7 * s * (1 + .4 * luz)
    lx, ly = qx + cw - 16 * s, qy + ch - 15 * s
    d.ellipse((lx - r, ly - r, lx + r, ly + r), fill=col + (int(120 + 135 * luz),))
    return qx + cw / 2, qy + ch / 2


def antipirata(n=268, titulo="ANTIPIRATERÍA", rotulo="COMPROBACIONES", letrero="NO CONTROLLER", ancho=1240):
    """Cartucho de N64 con su chip que emite pulsos; a la derecha el contador rueda de 0 a `n` (marca 0 -> marca 1) con su
    barra; marca 2: el letrero `letrero` parpadea en rojo debajo y el led del chip pasa a rojo."""
    h = 500
    fnum = fuente("t", 140)
    frot = fuente("r", 38)
    flet = _ajustar(letrero, "t", 78, ancho - 140)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + ancho / 2, M + 46), titulo, fuente("t", 50), MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        t0, t1, t2 = _mq(marcas, 0, dur, .10), _mq(marcas, 1, dur, .55), _mq(marcas, 2, dur, .66)
        u = 0.0 if dt < t0 else min(1.0, (dt - t0) / max(.3, t1 - t0))
        v = int(round(n * (1 - (1 - u) ** 1.6)))
        alarma = dt >= t2
        rodando = t0 <= dt < t1
        cap = _vacia(im)
        dc = ImageDraw.Draw(cap)
        temb = 4 * math.sin(dt * 60) * max(0.0, 1 - (dt - t2) / .5) if alarma else 0
        chx, chy = _cartucho_chip(dc, M + 215 + temb, M + 236, 1.08, abs(math.sin(dt * (14 if rodando else 3))), alarma)
        glow = _vacia(im)
        dg = ImageDraw.Draw(glow)
        if rodando or alarma:
            for j in range(3):                                 # pulsos que salen del chip
                f = ((dt * (1.6 if rodando else .8)) + j / 3) % 1
                r = 70 + 150 * f
                dg.ellipse((chx - r, chy - r * .8, chx + r, chy + r * .8), outline=(ROJO if alarma else MIEL) + (int(200 * (1 - f)),),
                           width=4)
        im.alpha_composite(glow)
        im.alpha_composite(cap)
        d = ImageDraw.Draw(im)
        xr = M + 440
        pop = 1 + .10 * max(0.0, 1 - (dt - t1) / .3) if dt >= t1 else 1
        _texto(d, (xr, M + 196), str(v), fuente("t", int(140 * pop)) if pop > 1.001 else fnum, CREMA if v < n else MIEL, "lm",
               255 * _eo((dt - .1) / .3), borde=5)
        _texto(d, (xr + 4, M + 290), rotulo, frot, AZUL_CLARO, "lm", 255 * _eo((dt - .2) / .3))
        x1 = M + ancho - 70
        d.rounded_rectangle((xr, M + 326, x1, M + 352), 13, fill=(30, 16, 8, 200), outline=MIEL_OSC + (255,), width=2)
        if v > 0:
            d.rounded_rectangle((xr + 3, M + 329, xr + 3 + (x1 - xr - 6) * v / n, M + 349), 10,
                                fill=(ROJO if alarma else MIEL) + (255,))
        if alarma:
            w = dt - t2
            on = (w % .7) < .46
            s = _reb(w / .35)
            _texto(d, (M + ancho / 2, M + 438), letrero, fuente("t", max(10, int(flet.size * s))), ROJO, "mm", 255 if on else 70,
                   borde=4, color_borde=CREMA)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ 5. el pez abisal sin huesos
def _cabeza_abisal(d, hx, cy, dt, a):
    A = int(255 * a)
    col = CREMA + (A,)
    d.line([(hx + 110, cy - 58), (hx + 20, cy - 96), (hx - 78, cy - 62), (hx - 122, cy - 8)], fill=col, width=6, joint="curve")
    d.line([(hx - 122, cy + 4), (hx - 74, cy + 70), (hx + 56, cy + 78), (hx + 112, cy + 46)], fill=col, width=6, joint="curve")
    d.line([(hx + 110, cy - 58), (hx + 112, cy + 46)], fill=col, width=6)
    pts = []
    for k in range(9):                                        # dientes
        x = hx - 118 + k * 13
        pts += [(x, cy - 6 + (k % 2) * 4), (x + 6, cy + (14 if k % 2 else -18))]
    d.line(pts, fill=col, width=3)
    d.ellipse((hx - 34, cy - 66, hx + 10, cy - 22), outline=col, width=5)
    d.ellipse((hx - 18, cy - 50, hx - 4, cy - 36), fill=col)
    lure = [(hx + 20, cy - 96), (hx - 10, cy - 150), (hx - 70, cy - 168), (hx - 116, cy - 140)]
    d.line(lure, fill=col, width=4, joint="curve")
    return lure[-1]


def huesos(n=12, quitar=4, titulo="MÁXIMO DE ARTICULACIONES", ancho=1440):
    """Esqueleto esquemático de pez abisal (cráneo con señuelo que brilla, espina con `n` articulaciones-círculo y costillas).
    Las articulaciones entran de la cabeza a la cola; marca 0: las últimas `quitar` se tachan en rojo; marca 1: caen y la cola
    se recoge hasta la última que queda; abajo «n -> n-quitar»."""
    h = 470
    ft = _ajustar(titulo, "t", 50, ancho - 100)
    fnum = fuente("t", 60)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + ancho / 2, M + 44), titulo, ft, MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        tq, tf = _mq(marcas, 0, dur, .42), _mq(marcas, 1, dur, .60)
        cy, hx = M + 262, M + 182
        x0, x1 = M + 312, M + ancho - 210
        paso = (x1 - x0) / max(1, n - 1)
        xs = [x0 + j * paso for j in range(n)]
        quedan = max(1, n - quitar)
        cortados = set(range(quedan, n))
        glow = _vacia(im)
        cap = _vacia(im)
        dc = ImageDraw.Draw(cap)
        bx, by = _cabeza_abisal(dc, hx, cy, dt, _eo(dt / .35))
        lat = .5 + .5 * math.sin(dt * 4)
        dg = ImageDraw.Draw(glow)
        rr = 26 + 10 * lat
        dg.ellipse((bx - rr, by - rr, bx + rr, by + rr), fill=MIEL + (int(120 + 80 * lat),))
        im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(10)))
        dc.ellipse((bx - 11, by - 11, bx + 11, by + 11), fill=(255, 236, 150, 255))
        for j in range(n):
            tin = (.04 + .30 * j / max(1, n - 1)) * dur
            if dt < tin:
                continue
            e = _reb((dt - tin) / .35)
            px, py, a = xs[j], cy, 1.0
            if j in cortados and dt >= tf:
                tt = dt - tf - .07 * (j - quedan)
                if tt > 0:
                    px += 70 * tt * (1 + .3 * (j % 2))
                    py += 520 * tt * tt + 30 * tt
                    a = max(0.0, 1 - tt / 1.0)
                if a <= 0:
                    continue
            A = int(255 * a)
            prev = (hx + 112 if j == 0 else px - paso)
            dc.line([(prev, py), (px, py)], fill=CREMA + (A,), width=7)
            L = (112 - 52 * j / max(1, n - 1)) * min(1.0, e)
            for sg in (-1, 1):
                dc.line([(px, py), (px - 12, py + sg * L * .55), (px - 30, py + sg * L)], fill=CREMA + (int(A * .85),), width=5,
                        joint="curve")
            r = 16 * e
            marcado = j in cortados and dt >= tq + .18 * (j - quedan)
            dc.ellipse((px - r, py - r, px + r, py + r), fill=(ROJO if marcado else MIEL) + (A,), outline=CHOCO + (A,), width=3)
            if marcado:
                _tacha(dc, px, py - 46, 18, _eo((dt - tq - .18 * (j - quedan)) / .3), 7)
        def aleta(x, y, e, A):
            if e <= .02 or A <= 0:
                return
            dc.line([(x, y), (x + 108 * e, y - 72 * e), (x + 80 * e, y), (x + 108 * e, y + 72 * e), (x, y)], fill=CREMA + (A,),
                    width=6, joint="curve")
            for k in (-1, 0, 1):
                dc.line([(x + 10 * e, y), (x + 92 * e, y + k * 44 * e)], fill=CREMA + (int(A * .7),), width=3)
        if dt >= (.04 + .30) * dur:                         # aleta de la cola: cae con la última vértebra y brota otra
            if dt < tf:
                aleta(xs[-1], cy, 1.0, 255)
            else:
                tt = dt - tf - .07 * (n - 1 - quedan)
                aleta(xs[-1] + 90 * max(0.0, tt), cy + 520 * max(0.0, tt) ** 2, 1.0, int(255 * max(0.0, 1 - max(0.0, tt) / 1.0)))
                aleta(xs[quedan - 1], cy, _reb((dt - tf - .45) / .45), 255)
        im.alpha_composite(cap)
        d = ImageDraw.Draw(im)
        cxn, yn = M + ancho / 2, M + h - 46
        a0 = 255 * _eo((dt - .3 * dur) / .4)
        if dt < tf + .7:
            _texto(d, (cxn, yn), str(n), fnum, CREMA, "mm", a0, borde=4)
        else:
            u = _eo((dt - tf - .7) / .35)
            _texto(d, (cxn - 90, yn), str(n), fnum, CREMA, "mm", 255, borde=4)
            d.line([(cxn - 40, yn), (cxn - 40 + 70 * u, yn)], fill=MIEL + (255,), width=8)
            if u > .8:
                d.polygon([(cxn + 30, yn - 16), (cxn + 52, yn), (cxn + 30, yn + 16)], fill=MIEL + (255,))
            _texto(d, (cxn + 110, yn), str(quedan), fuente("t", max(10, int(60 * _reb(u)))), ROJO, "mm", 255 * u, borde=4,
                   color_borde=CREMA)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ 6. tabla de tiempos que ruedan
def _a_seg(s):
    s = s.strip()
    if re.fullmatch(r"\d+(:\d{1,2})+", s):
        v = 0
        for p in s.split(":"):
            v = v * 60 + int(p)
        return v, s.count(":") + 1
    return None, 0


def _fmt_t(v, campos):
    v, out = int(v), []
    for _ in range(campos - 1):
        out.append(v % 60)
        v //= 60
    out.append(v)
    out = out[::-1]
    return str(out[0]) + "".join(f":{p:02d}" for p in out[1:])


def cronometro(filas, titulo=None, ancho=None):
    """filas = [(etiqueta, "4:10:46"), (etiqueta, "25:49"), ("Tú", "decenas de horas")]: en la marca k entra la fila k con su
    cronómetro y la cifra RUEDA hasta su valor (formato h:mm:ss o m:ss); un valor de texto se baraja y queda en rojo."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    fl, ftm = fuente("r", 42), fuente("t", 64)
    lw = max(tmp.textlength(e, font=fl) for e, _ in filas)
    tw = max(tmp.textlength(v, font=ftm) for _, v in filas)
    ancho = ancho or int(min(1500, max(1000, 170 + lw + 90 + tw + 70)))
    FH = 108
    top = 92 if titulo else 26
    h = top + len(filas) * FH + 22
    fts = _ajustar(titulo, "t", 50, ancho - 100) if titulo else None
    datos = [(_ajustar(e, "r", 42, ancho - 330 - tw), *_a_seg(v)) for e, v in filas]
    ftxt = [_ajustar(v, "t", 64, ancho - 260 - lw) for _, v in filas]

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        if titulo:
            _texto(d, (M + ancho / 2, M + 48), titulo, fts, MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        cap = _vacia(im)
        dc = ImageDraw.Draw(cap)
        for k, (fe, seg, campos) in enumerate(datos):
            e, v = filas[k]
            tk = _mq(marcas, k, dur, .06 + .22 * k)
            if dt < tk:
                continue
            u = _eo((dt - tk) / .35)
            y = M + top + k * FH + FH / 2
            dx = -50 * (1 - u)
            A = int(255 * u)
            if k:
                for i in range(40):
                    kk = 1 - abs(i - 20) / 20
                    dc.line([(M + 60 + i * (ancho - 120) / 40, y - FH / 2), (M + 60 + (i + 1) * (ancho - 120) / 40, y - FH / 2)],
                            fill=MIEL_OSC + (int(140 * kk * u),), width=2)
            rr = min(1.0, (dt - tk) / 1.6)
            cxr, cyr, r = M + 96 + dx, y + 4, 32
            dc.rectangle((cxr - 7, cyr - r - 14, cxr + 7, cyr - r - 4), fill=CREMA + (A,))
            dc.ellipse((cxr - r, cyr - r, cxr + r, cyr + r), fill=(30, 16, 8, int(200 * u)), outline=CREMA + (A,), width=4)
            ang = (dt - tk) * 9 if rr < 1 else 1.6 * 9
            dc.line([(cxr, cyr), (cxr + (r - 8) * math.sin(ang), cyr - (r - 8) * math.cos(ang))], fill=MIEL + (A,), width=4)
            _texto(dc, (M + 160 + dx, y), e, fe, CREMA, "lm", A)
            xr = M + ancho - 60 + dx
            if seg is not None:
                s = _fmt_t(seg * (1 - (1 - rr) ** 2.4), campos) if rr < 1 else v
                pop = 1 + .14 * max(0.0, 1 - (dt - tk - 1.6) / .3) if rr >= 1 else 1
                _texto(dc, (xr, y), s, fuente("t", int(ftxt[k].size * pop)), MIEL, "rm", A, borde=4)
            else:
                if rr < 1:
                    rs = np.random.RandomState(int(dt * 20) + k)
                    s = "%d:%02d:%02d" % (rs.randint(10, 99), rs.randint(0, 59), rs.randint(0, 59))
                    _texto(dc, (xr, y), s, ftm, MIEL, "rm", A, borde=4)
                else:
                    tam = int(ftxt[k].size * _reb((dt - tk - 1.6) / .35))
                    _texto(dc, (xr, y + 2 * math.sin(dt * 6)), v, fuente("t", max(10, tam)), ROJO, "rm", A, borde=4,
                           color_borde=CREMA)
        im.alpha_composite(cap)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ 7. sellos de fecha por región
def _bandera(cod, w, h):
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    if cod == "jp":
        d.rectangle((0, 0, w - 1, h - 1), fill=(245, 245, 245, 255))
        r = h * .3
        d.ellipse((w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r), fill=(200, 16, 46, 255))
    elif cod in ("na", "us"):
        for k in range(7):
            d.rectangle((0, k * h / 7, w - 1, (k + 1) * h / 7), fill=((178, 34, 52) if k % 2 == 0 else (245, 245, 245)) + (255,))
        d.rectangle((0, 0, w * .44, h * 4 / 7), fill=(40, 52, 120, 255))
        for i in range(4):
            for j in range(3):
                x, y = w * .06 + i * w * .1, h * .1 + j * h * .15
                d.ellipse((x - 2, y - 2, x + 2, y + 2), fill=(245, 245, 245, 255))
    elif cod == "eu":
        d.rectangle((0, 0, w - 1, h - 1), fill=(0, 51, 153, 255))
        for k in range(12):
            a = math.radians(30 * k)
            x, y = w / 2 + h * .32 * math.cos(a), h / 2 + h * .32 * math.sin(a)
            d.regular_polygon((x, y, 4), 5, rotation=-90, fill=(255, 204, 0, 255))
    elif cod and os.path.exists(cod):
        ic = _icono(cod, max(w, h))
        im.alpha_composite(ic.resize((w, h), Image.LANCZOS))
    else:
        return None
    ImageDraw.Draw(im).rectangle((0, 0, w - 1, h - 1), outline=CREMA + (255,), width=2)
    return im


def fechas(hitos, titulo=None, ancho=None):
    """hitos = [(region, fecha, bandera, nota=None)], bandera = "na"/"jp"/"eu" (dibujada) o ruta a una imagen o None.
    Cada sello CAE (marca k = sello k) sobre una línea que avanza; el último late. `nota` (opcional) va bajo la línea."""
    n = len(hitos)
    SW, SH = 400, 180
    ancho = ancho or n * 460 + 60
    top = 88 if titulo else 22
    hay_nota = any(len(x) > 3 and x[3] for x in hitos)
    h = top + 300 + (60 if hay_nota else 0)
    fts = _ajustar(titulo, "t", 50, ancho - 100) if titulo else None
    tmp = ImageDraw.Draw(Image.new("RGBA", (4, 4)))
    tope = ancho / n - 34                                    # el sello más ancho que cabe en su hueco sin tocar al vecino
    sellos = []
    for k, hi in enumerate(hitos):
        reg, fec, ban = hi[0].upper(), hi[1], hi[2] if len(hi) > 2 else None
        b = _bandera(ban, 80, 54) if ban else None
        izq = 124 if b is not None else 40
        fr = _ajustar(reg, "r", 36, tope - izq - 30)
        sw = int(min(tope, max(SW, izq + tmp.textlength(reg, font=fr) + 30)))
        ff = _ajustar(fec, "t", 54, sw - 50)
        sellos.append((reg, fec, b, fr, ff, (-4, 3, -2, 4)[k % 4], sw))
    fno = fuente("r", 34)

    def sello(k, borde):
        reg, fec, b, fr, ff, giro, sw = sellos[k]
        c = Image.new("RGBA", (sw, SH), (0, 0, 0, 0))
        d = ImageDraw.Draw(c)
        d.rounded_rectangle((6, 6, sw - 6, SH - 6), 22, fill=(52, 30, 14, 140), outline=borde + (255,), width=5)
        d.rounded_rectangle((16, 16, sw - 16, SH - 16), 16, outline=borde + (140,), width=2)
        if b is not None:
            c.alpha_composite(b, (30, 31))
            _texto(d, (124, 58), reg, fr, AZUL_CLARO, "lm", 255)
        else:
            _texto(d, (sw / 2, 58), reg, fr, AZUL_CLARO, "mm", 255)
        _texto(d, (sw / 2, 128), fec, ff, MIEL, "mm", 255, borde=3)
        return c.rotate(giro, expand=True, resample=Image.BICUBIC)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        if titulo:
            _texto(d, (M + ancho / 2, M + 48), titulo, fts, MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        yl = M + top + 256
        xs = [M + ancho * (k + .5) / n for k in range(n)]
        ts = [_mq(marcas, k, dur, .10 + .24 * k) for k in range(n)]
        llegados = [k for k in range(n) if dt >= ts[k]]
        xf = M + 50
        if llegados:
            j = llegados[-1]
            ant = xs[j - 1] if j else M + 50
            xf = ant + (xs[j] - ant) * _eo((dt - ts[j]) / .5)
            if j == n - 1 and dt - ts[j] > .5:
                xf = xs[j] + (M + ancho - 50 - xs[j]) * _eo((dt - ts[j] - .5) / .5)
        d.line([(M + 50, yl), (M + ancho - 50, yl)], fill=(90, 70, 50, 200), width=4)
        d.line([(M + 50, yl), (xf, yl)], fill=MIEL + (255,), width=7)
        for k in range(n):
            on = dt >= ts[k]
            d.polygon(_hex(xs[k], yl, 13), fill=(MIEL if on else (90, 70, 50)) + (255,), outline=CHOCO + (255,))
        for k in llegados:
            w = dt - ts[k]
            ultimo = k == n - 1
            lat = 1 + .05 * math.sin(dt * 7) if ultimo and w > .4 else 1
            borde = MIEL if ultimo else MIEL_OSC
            s = max(.05, 2.2 - 1.2 * _eo(w / .28)) * lat
            sy = 6 * math.sin(w * 30) * max(0.0, 1 - w / .4)       # golpe del sello
            _pegar(im, sello(k, borde), xs[k], yl - 122 + sy, s, min(1.0, _eo(w / .15)))
            if len(hitos[k]) > 3 and hitos[k][3]:
                _texto(ImageDraw.Draw(im), (xs[k], yl + 44), hitos[k][3], fno, CREMA, "mm", 255 * _eo((w - .3) / .3))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ 8. el color de los Jinjos se sortea
def jinjos_color(n=9, titulo="FAMILIAS JINJO", remate="EL COLOR SE SORTEA EN CADA PARTIDA", ancho=1460):
    """`n` Jinjos (dibujados con el kit) que saltan y cambian de color cada vez más despacio, como una ruleta; en la marca 0
    se detienen con un destello y sale `remate`."""
    from mg_gaming import JINJO, _jinjo
    h = 380
    ft = _ajustar(titulo, "t", 50, ancho - 100)
    fr = _ajustar(remate, "t", 46, ancho - 120)
    paso = (ancho - 200) / max(1, n - 1)
    R = min(56, paso / 2.95)                                  # con los bracitos abiertos no se tocan
    cols = [c for _, c in JINJO]

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + ancho / 2, M + 44), titulo, ft, MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        t0, ts = .35, _mq(marcas, 0, dur, .62)
        u = min(1.0, max(0.0, (dt - t0) / max(.3, ts - t0)))
        S = 22 * (1 - (1 - u) ** 2.2)                          # pasos de la ruleta: rápido -> lento
        paso_i = int(S)
        perm = np.random.RandomState(11 + paso_i).permutation(len(cols))
        salto = abs(math.sin(math.pi * (S - paso_i))) if u < 1 else 0
        cap = _vacia(im)
        dc = ImageDraw.Draw(cap)
        cy = M + 206
        for i in range(n):
            e = _reb((dt - .08 * i) / .4)
            if e <= 0:
                continue
            cx = M + 100 + i * paso
            by = cy - 26 * salto * (1 if (i + paso_i) % 2 else .6)
            _jinjo(dc, cx, by, R * e, cols[perm[i % len(cols)]], 255, dt + i)
            if u < 1 and dt > t0:
                _texto(dc, (cx, cy - R - 50 - 6 * math.sin(dt * 6 + i)), "?", fuente("t", 40), CREMA, "mm", 200, borde=3)
        if dt >= ts:
            w = dt - ts
            for i in range(n):
                cx = M + 100 + i * paso
                f = min(1.0, w / .5)
                r = R + 6 + 40 * f
                dc.ellipse((cx - r, cy - r, cx + r, cy + r), outline=MIEL + (int(220 * (1 - f)),), width=4)
            _texto(dc, (M + ancho / 2, M + h - 52), remate, fuente("t", max(10, int(fr.size * _reb(w / .4)))), CREMA, "mm",
                   255 * _eo(w / .25), borde=4)
        im.alpha_composite(cap)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ 9. subtítulos de jefe que se sustituyen
def rotulos(lineas, ancho=None):
    """Rótulo de jefe del juego: nombre grande + subtítulo. lineas = [(nombre, subtitulo, traduccion=None)]; en la marca k
    el subtítulo anterior se tacha y cae, y el nuevo baja con rebote (la traducción debajo, en azul)."""
    tmp = ImageDraw.Draw(Image.new("RGBA", (10, 10)))
    n = len(lineas)
    fnm, fsb, ftr = fuente("t", 92), fuente("t", 56), fuente("r", 38)
    anchos = [max(tmp.textlength(x[0].upper(), font=fnm), tmp.textlength(x[1], font=fsb),
                  tmp.textlength("«" + x[2] + "»" if len(x) > 2 and x[2] else "", font=ftr)) for x in lineas]
    ancho = ancho or int(min(1500, max(980, max(anchos) + 180)))
    h = 380
    L = [(_ajustar(x[0].upper(), "t", 92, ancho - 140), _ajustar(x[1], "t", 56, ancho - 140),
          _ajustar("«" + x[2] + "»", "r", 38, ancho - 140) if len(x) > 2 and x[2] else None) for x in lineas]
    fc = fuente("r", 34)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        cx = M + ancho / 2
        ts = [_mq(marcas, k, dur, .03 + .9 * k / n) for k in range(n)]
        k = max([i for i in range(n) if dt >= ts[i]] or [0])
        w = dt - ts[k]
        nom = lineas[k][0].upper()
        cap = _vacia(im)
        dc = ImageDraw.Draw(cap)
        cambia_nom = k > 0 and lineas[k - 1][0].upper() != nom
        pul = 1 + .06 * max(0.0, 1 - w / .3) if k > 0 else 1
        an = 255 * (_eo(w / .3) if (k == 0 or cambia_nom) else 1)
        _texto(dc, (cx, M + 92), nom, fuente("t", int(L[k][0].size * pul)), MIEL, "mm", an, borde=5)
        filete(dc, cx, M + 162, min(ancho * .36, 320), 255 * _eo((dt - .2) / .35))
        _texto(dc, (M + ancho - 50, M + 40), f"{k + 1}/{n}", fc, AZUL_CLARO, "rm", 255 * _eo((dt - .3) / .3))
        if k > 0 and w < .75:                               # el anterior: se tacha y cae
            sb_old = lineas[k - 1][1]
            fo = L[k - 1][1]
            tw = dc.textlength(sb_old, font=fo)
            caida = max(0.0, w - .3)
            yo = M + 232 + 420 * caida * caida + 60 * caida
            ao = 255 * max(0.0, 1 - caida / .28)
            _texto(dc, (cx, yo), sb_old, fo, (200, 180, 160), "mm", ao, borde=3)
            ul = _eo(w / .28)
            dc.line([(cx - tw / 2 - 10, yo), (cx - tw / 2 - 10 + (tw + 20) * ul, yo)], fill=ROJO + (int(ao),), width=8)
        tn = ts[k] + (.58 if k > 0 else .25)
        if dt >= tn:
            v = (dt - tn) / .45
            yn = M + 232 - 70 * (1 - _reb(v))
            _texto(dc, (cx, yn), lineas[k][1], L[k][1], CREMA, "mm", 255 * _eo(v / .4), borde=4)
            if L[k][2]:
                _texto(dc, (cx, M + 306), "«" + lineas[k][2] + "»", L[k][2], AZUL_CLARO, "mm", 255 * _eo((dt - tn - .3) / .35))
        im.alpha_composite(cap)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ 10. la memoria del N64 y la cara de atrás
def _cubo(d, cx, cy, r, ang, atras):
    """Cubo de alambre que gira: caras delanteras con relleno miel suave; las de atrás (discontinuas, rojas) con alfa `atras`."""
    v = []
    for x in (-1, 1):
        for y in (-1, 1):
            for z in (-1, 1):
                x1, z1 = x * math.cos(ang) - z * math.sin(ang), x * math.sin(ang) + z * math.cos(ang)
                y1, z2 = y * math.cos(.45) - z1 * math.sin(.45), y * math.sin(.45) + z1 * math.cos(.45)
                v.append((cx + r * x1, cy + r * y1, z2))
    caras = [(0, 1, 3, 2), (4, 6, 7, 5), (0, 4, 5, 1), (2, 3, 7, 6), (0, 2, 6, 4), (1, 5, 7, 3)]
    detras = [c for c in caras if sum(v[i][2] for i in c) / 4 >= 0]
    delante = [c for c in caras if sum(v[i][2] for i in c) / 4 < 0]
    for c in delante:                                         # relleno primero: ImageDraw pisa el alfa de lo de debajo
        d.polygon([(v[i][0], v[i][1]) for i in c], fill=MIEL + (70,))
    if atras > .02:
        for c in detras:
            p = [(v[i][0], v[i][1]) for i in c]
            for a, b in zip(p, p[1:] + [p[0]]):
                for t in range(0, 10, 2):                  # discontinua
                    d.line([(a[0] + (b[0] - a[0]) * t / 10, a[1] + (b[1] - a[1]) * t / 10),
                            (a[0] + (b[0] - a[0]) * (t + 1) / 10, a[1] + (b[1] - a[1]) * (t + 1) / 10)],
                           fill=ROJO + (int(255 * atras),), width=3)
    for c in delante:
        p = [(v[i][0], v[i][1]) for i in c]
        d.line(p + [p[0]], fill=MIEL + (255,), width=4)


def _pak(d, cx, cy, s=1.0):
    """Expansion Pak esquemático: cuerpo gris oscuro con la tapa roja y las ranuras."""
    w, hh = 120 * s, 150 * s
    d.rounded_rectangle((cx - w / 2, cy - hh / 2 + 34 * s, cx + w / 2, cy + hh / 2), int(10 * s), fill=(54, 54, 60, 255),
                        outline=(20, 20, 24, 255), width=2)
    d.rounded_rectangle((cx - w / 2, cy - hh / 2, cx + w / 2, cy - hh / 2 + 44 * s), int(10 * s), fill=(196, 40, 36, 255),
                        outline=(20, 20, 24, 255), width=2)
    for k in range(4):
        y = cy - hh / 2 + 60 * s + k * 18 * s
        d.line([(cx - w / 2 + 16 * s, y), (cx + w / 2 - 16 * s, y)], fill=(90, 90, 100, 255), width=3)


def memoria(lleno=1.0, titulo="MEMORIA DEL N64", pak=None, nota="NO HACE FALTA", frase="La cara de atrás se borra",
            ancho=1400):
    """Barra de memoria por bloques que se llena hasta `lleno` (marca 0 -> marca 1; lleno = los últimos bloques laten en
    rojo); a la derecha el Expansion Pak (`pak` = ruta o dibujado) que se tacha con `nota` en la marca 1; marca 2: un cubo
    que gira pierde sus caras de atrás y sale `frase`."""
    h = 450
    NB = 16
    fno = _ajustar(nota, "t", 42, 310)
    ffr = _ajustar(frase, "t", 56, ancho - 340)

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + 60, M + 50), titulo, fuente("t", 50), MIEL, "lm", 255 * _eo(dt / .3), borde=3)
        t0, t1, t2 = _mq(marcas, 0, dur, .08), _mq(marcas, 1, dur, .42), _mq(marcas, 2, dur, .62)
        u = 0.0 if dt < t0 else _eo((dt - t0) / max(.3, (t1 - t0) * .9))
        x0, x1, yb = M + 60, M + ancho - 330, M + 150
        bw = (x1 - x0) / NB
        cap = _vacia(im)
        dc = ImageDraw.Draw(cap)
        llenos = lleno * NB * u
        for b in range(NB):
            bx = x0 + b * bw
            dc.rounded_rectangle((bx + 3, yb - 34, bx + bw - 3, yb + 34), 8, fill=(30, 16, 8, 200), outline=MIEL_OSC + (255,), width=2)
            f = max(0.0, min(1.0, llenos - b))
            if f > 0:
                rojo = lleno >= .999 and b >= NB - 3 and u >= .999
                lat = .5 + .5 * math.sin(dt * 8) if rojo else 1
                col = ROJO if rojo else MIEL
                dc.rounded_rectangle((bx + 7, yb + 30 - 60 * f, bx + bw - 7, yb + 30), 6,
                                     fill=col + (int(200 + 55 * lat),))
        _texto(dc, (x0, yb + 64), "0%", fuente("r", 34), CREMA, "lm", 255 * _eo((dt - .2) / .3))
        _texto(dc, (x1, yb + 64), f"{int(round(100 * lleno * u))}%", fuente("r", 34), CREMA, "rm", 255 * _eo((dt - .2) / .3))
        px, py = M + ancho - 178, M + 146
        e = _reb((dt - .25) / .45)
        if pak:
            _pegar(cap, _encajar(pak, 250, 160), px, py + 3 * math.sin(dt * 2), max(.05, e))
            dc = ImageDraw.Draw(cap)
        elif e > .05:
            _pak(dc, px, py + 3 * math.sin(dt * 2), 1.15 * e)
        if dt >= t1:
            w = dt - t1
            _tacha(dc, px, py, 84, _eo(w / .4), 13)
            _texto(dc, (px, py + 130), nota, fno, ROJO, "mm", 255 * _eo((w - .3) / .3), borde=3, color_borde=CREMA)
        im.alpha_composite(cap)
        if dt >= t2 - .2:
            w = dt - t2
            cap = _vacia(im)
            dc = ImageDraw.Draw(cap)
            a = _eo((w + .2) / .3)
            _cubo(dc, M + 140, M + 356, 60 * max(.05, _reb((w + .2) / .4)), dt * 1.1, max(0.0, 1 - _eo((w - .7) / .9)) * a)
            im.alpha_composite(cap)
            d = ImageDraw.Draw(im)
            _texto(d, (M + 260, M + 356), frase, ffr, CREMA, "lm", 255 * _eo((w - .2) / .35), borde=4)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ 11. el compás de 6/8
def compas(bpm=100, compases=2, titulo="ESCUCHA EL COMPÁS", desfase=None, ancho=1340):
    """«6/8» grande y seis pulsos en dos grupos de tres que laten al tempo (`bpm` = corcheas por minuto; si el tempo de la
    música va en negra con puntillo, pásalo x3). Empieza en la marca 0 (o `desfase` s); una bolita de miel salta de pulso en
    pulso; el 1 y el 4 llevan el acento. Tras `compases` sigue latiendo suave."""
    h = 390
    ft = _ajustar(titulo, "t", 50, ancho - 100)
    f68 = fuente("t", 150)
    fnum = fuente("r", 36)
    xs = [x * (ancho - 60) / 1280 for x in (430, 560, 690, 890, 1020, 1150)]

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        d = ImageDraw.Draw(im)
        _texto(d, (M + ancho / 2, M + 44), titulo, ft, MIEL, "mm", 255 * _eo(dt / .3), borde=3)
        t0 = desfase if desfase is not None else _mq(marcas, 0, dur, .10)
        per = 60.0 / bpm
        p = (dt - t0) / per
        pi = int(math.floor(p)) if p >= 0 else -1
        fr = p - pi if p >= 0 else 0
        actual = pi % 6 if pi >= 0 else -1
        medida = pi // 6 + 1 if pi >= 0 else 0
        suave = medida > compases
        cy = M + 222
        lat68 = 1 + (.06 * (1 - fr) ** 2 if actual in (0, 3) and not suave else 0)
        _texto(d, (M + 170, cy - 10), "6/8", fuente("t", int(150 * lat68)) if lat68 > 1.001 else f68, MIEL, "mm",
               255 * _eo((dt - .1) / .3), borde=5)
        cap = _vacia(im)
        dc = ImageDraw.Draw(cap)
        for g in (0, 1):                                    # llave de cada grupo de tres
            a, b = M + xs[3 * g] - 40, M + xs[3 * g + 2] + 40
            dc.line([(a, cy + 98), (a, cy + 110), (b, cy + 110), (b, cy + 98)], fill=MIEL_OSC + (220,), width=4)
        for k in range(6):
            cx = M + xs[k]
            acento = k in (0, 3)
            R = 54 if acento else 42
            e = _reb((dt - .15 - .06 * k) / .4)
            if e <= 0:
                continue
            on = k == actual
            fuerza = (1 - fr) ** 2 * (.5 if suave else 1) if on else 0
            r = R * e * (1 + .32 * fuerza)
            if on:
                dc.ellipse((cx - r - 16, cy - r - 16, cx + r + 16, cy + r + 16), outline=MIEL + (int(200 * fuerza),), width=5)
            dc.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(MIEL + (int(150 + 105 * fuerza),)) if on else (60, 38, 22, 200),
                       outline=(CREMA if acento else MIEL_OSC) + (255,), width=4 if acento else 3)
            _texto(dc, (cx, cy + 2), str(k + 1), fuente("t", 56 if acento else 46), CHOCO if on else CREMA, "mm", 255, borde=2,
                   color_borde=MIEL if on else CHOCO)
        if 0 <= actual:                                       # bolita que salta al siguiente pulso
            sig = (actual + 1) % 6
            xa, xb = M + xs[actual], M + xs[sig]
            bx = xa + (xb - xa) * fr
            by = cy - 72 - (40 if sig else 70) * math.sin(math.pi * fr)
            dc.ellipse((bx - 13, by - 13, bx + 13, by + 13), fill=MIEL + (255,), outline=CHOCO + (255,), width=2)
        if medida:
            _texto(dc, (M + 170, cy + 96), f"compás {min(medida, compases)}/{compases}", fnum, AZUL_CLARO, "mm",
                   255 * _eo((dt - t0) / .3))
        im.alpha_composite(cap)
        return _salida(im, dt, dur)
    return fn
