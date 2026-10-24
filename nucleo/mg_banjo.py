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
  (pegatinas: mg_tes.pegatina · pantallas: mg_wow.pantalla · mapas: mg_mapa tema «banjo»)
"""
import math

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


def puesto(num, titulo, jiggy, ancho=None, etiqueta="JIGGY NÚMERO"):
    """El Jiggy REAL gira sobre su eje vertical (se estrecha y se ensancha, como el que flota en el juego) con el número en
    Cooper encima; a su derecha, sobre humo, «JIGGY NÚMERO N» y el título que se escribe de izquierda a derecha."""
    h, J = 320, 250
    fnum, ftit, fsup = fuente("t", 128), fuente("t", 70), fuente("r", 32)
    tw = ImageDraw.Draw(Image.new("RGBA", (10, 10))).textlength(titulo.upper(), font=ftit)
    if ancho is None:
        ancho = int(max(1000, 60 + J + 60 + tw + 80))

    def fn(dt, dur, marcas):
        im, M = humo(ancho, h)
        W, H = im.size
        capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
        d = ImageDraw.Draw(capa)
        x0 = M + 60 + J + 40
        cy = M + h / 2
        _texto(d, (x0, cy - 48), etiqueta + " " + str(num), fsup, AZUL_CLARO, "lm", 255 * _eo((dt - .3) / .35))
        _texto(d, (x0, cy + 20), titulo.upper(), ftit, CREMA, "lm", 255, borde=4)
        u = _eo((dt - .4) / .6)                                  # el título se descubre de izquierda a derecha
        m = np.zeros((H, W), np.uint8)
        m[:, :int(x0 + (tw + 20) * u)] = 255
        a = np.array(capa)
        a[..., 3] = np.minimum(a[..., 3], m)
        im.alpha_composite(Image.fromarray(a))
        d = ImageDraw.Draw(im)
        filete(d, x0 + tw / 2, cy + 74, min(tw / 2, 260), 255 * u)
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
            _pegar(im, _icono(ruta, 180, redondo=True), cx, cy, _reb((dt - tf) / .4) * (1 + .06 * math.sin(dt * 8)))
            _texto(d, (cx, cy + 130), txt, fuente("t", 44), ROJO, "mm", 255 * _eo((dt - tf) / .3), borde=3, color_borde=CREMA)
        return _bgra(_escala(im, _reb(dt / .45)), min(1.0, (dur - dt) / .35))
    return fn
