# -*- coding: utf-8 -*-
"""MOTION GRAPHICS de la COMPARATIVA Ocarina of Time N64 / remake de Switch 2 (Crónicas del gaming; primer uso
`oot_remake_cambios`, 26-oct-2026). Misma regla que mg_majora (22-oct: todo TRANSLÚCIDO con la interfaz del juego, nunca
carteles opacos): reutiliza sus primitivas (el cuadro de diálogo de N64, que es el mismo motor de Ocarina; el humo negro; el
filete) y añade lo propio de un video «antes / ahora»:
    import mg_oot as O
  marco(w, h, año, consola)          marco translúcido para una VENTANA de video del original (FX `video` con ancho): hueco
                                     transparente de w×h, filo con los 4 colores del logo de N64 y la píldora «NINTENDO 64 / 1998»
  etiqueta(texto, sub, color)        píldora pequeña para marcar el cuadro grande («SWITCH 2 / 2026»)
  contador(antes, despues, titulo)   el contador de rupias del HUD: «99» -> en la marca 0 rueda hasta «200» y se pone verde
  linea_tiempo(hitos)                1998 -> 2011 -> 2026: un hito por marca, con su imagen real (consola, logo)
  partitura(notas, titulo)           el pentagrama de la ocarina con los botones A (azul) y C (amarillo), una nota por golpe;
                                     en la marca 1 se apaga y aparece la onda del MICRÓFONO (tararear)
  sticks()                           N64: un stick / Switch 2: dos sticks; el derecho gira 360° alrededor de Link
  balance(si, no)                    lo confirmado (✓ verde) y lo que no (? gris), un renglón por marca
Probar SIEMPRE con una hoja de cuadros (marcas simuladas) antes de `fx`.
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import mg_majora as M

_eo, _reb, _bgra = M._eo, M._reb, M._bgra
fuente, ajustar, _txt, _humo, _filete = M.fuente, M.ajustar, M._txt, M._humo, M._filete
BLANCO, CREMA, AMARILLO, GRIS, VERDE = M.BLANCO, M.CREMA, M.AMARILLO, M.GRIS, M.VERDE
# los cuatro colores del logo de Nintendo 64 y el rojo de Switch
N64 = [(230, 50, 45), (250, 196, 30), (40, 160, 70), (40, 90, 200)]
ROJO_SW, AZUL_A, AMARILLO_C = (230, 0, 18), (70, 110, 240), (250, 200, 40)


def _vacio():
    return np.zeros((2, 2, 4), np.uint8)


def _pildora(texto, sub=None, color=N64, alto=58):
    """Píldora negra translúcida: puntitos de color + TEXTO + /sub."""
    f = fuente("d", 30)
    fs = fuente("d", 24)
    w = int(M._ancho(texto, f) + (M._ancho(" / " + sub, fs) if sub else 0) + 40 + 22 * (len(color) if isinstance(color, list) else 1))
    im = Image.new("RGBA", (w + 8, alto + 8), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((4, 4, w + 4, alto + 4), alto // 2, fill=(8, 6, 16, 200))
    cols = color if isinstance(color, list) else [color]
    x = 26
    for c in cols:
        d.ellipse((x - 7, alto / 2 + 4 - 7, x + 7, alto / 2 + 4 + 7), fill=tuple(c) + (255,))
        x += 20
    x += 8
    _txt(d, (x, alto / 2 + 5), texto, f, BLANCO, "lm")
    if sub:
        _txt(d, (x + M._ancho(texto, f), alto / 2 + 6), " / " + sub, fs, GRIS, "lm")
    return im


# ------------------------------------------------------------------ ventana del original
def marco(w, h, año="1998", consola="NINTENDO 64", color=None):
    """Marco para la ventana del ORIGINAL (FX `video` con ancho=w en px y el mismo x, y): sombra difusa por fuera, filo con los
    cuatro colores de N64 que se dibuja al entrar, esquinas redondas y la píldora «NINTENDO 64 / 1998» encima."""
    color = color or N64
    M_ = 40
    W, H = w + 2 * M_, h + 2 * M_ + 50
    oy = 50                                     # sitio para la píldora
    sombra = Image.new("L", (W, H), 0)
    ImageDraw.Draw(sombra).rounded_rectangle((M_ - 6, oy + M_ - 6, M_ + w + 6, oy + M_ + h + 6), 22, fill=170)
    sombra = sombra.filter(ImageFilter.GaussianBlur(14))
    hueco = Image.new("L", (W, H), 0)
    ImageDraw.Draw(hueco).rounded_rectangle((M_, oy + M_, M_ + w, oy + M_ + h), 16, fill=255)
    base = Image.new("RGBA", (W, H), (0, 0, 0, 255))
    base.putalpha(Image.fromarray(np.clip(np.array(sombra).astype(int) - np.array(hueco).astype(int) * 2, 0, 255).astype(np.uint8)))
    pil = _pildora(consola, año, color if isinstance(color, list) else [color])
    per = 2 * (w + h)

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        u = _eo(dt / .7)
        # filo de colores que recorre el borde (cada lado de un color)
        lados = [((M_, oy + M_), (M_ + w, oy + M_)), ((M_ + w, oy + M_), (M_ + w, oy + M_ + h)),
                 ((M_ + w, oy + M_ + h), (M_, oy + M_ + h)), ((M_, oy + M_ + h), (M_, oy + M_))]
        largo = u * per
        for k, ((x0, y0), (x1, y1)) in enumerate(lados):
            L = abs(x1 - x0) + abs(y1 - y0)
            if largo <= 0:
                break
            p = min(1.0, largo / L)
            d.line([(x0, y0), (x0 + (x1 - x0) * p, y0 + (y1 - y0) * p)], fill=tuple(color[k % len(color)]) + (235,), width=5)
            largo -= L
        a = _eo((dt - .25) / .4)
        if a > 0:
            p2 = M._alfa(pil, a)
            im.alpha_composite(p2, (M_ + 10, max(0, oy + M_ - pil.height // 2 - 26)))
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .35))
    return fn


def etiqueta(texto="SWITCH 2", sub="2026", color=ROJO_SW):
    pil = _pildora(texto, sub, [color])

    def fn(dt, dur, marcas):
        k = _reb(dt / .45)
        im = pil.resize((max(2, int(pil.width * k)), max(2, int(pil.height * k))), Image.BICUBIC)
        return _bgra(im, min(_eo(dt / .2), (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ contador de rupias
def contador(antes=99, despues=200, titulo="Bolsa inicial", rupia=None, sub_antes="Nintendo 64", sub_despues="Switch 2"):
    """El contador del HUD con la rupia verde: muestra `antes` con su consola; en la marca 0 el número rueda hasta `despues`,
    se pone verde (como la bolsa llena del juego) y cambia la consola."""
    w, h = 760, 300
    base, Mg = _humo(w, h, alfa=.6)
    icono = None
    if rupia and os.path.exists(rupia):
        icono = Image.open(rupia).convert("RGBA")
        icono.thumbnail((150, 150))
    fn_num = fuente("d", 128)
    ft, fs = fuente("d", 34), M.fuente("si", 28)

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        cx = Mg + w / 2
        _txt(d, (cx, Mg + 40), titulo.upper(), ft, AMARILLO, "mm", 255 * _eo(dt / .3), track=1)
        _filete(d, Mg + 90, Mg + w - 90, Mg + 74, 255 * _eo(dt / .4))
        t0 = marcas[0] if marcas else dur * .5
        u = _eo((dt - t0) / 1.1)
        n = int(round(antes + (despues - antes) * u))
        col = tuple(int(BLANCO[i] + (VERDE[i] - BLANCO[i]) * u) for i in range(3))
        if icono:
            ang = 8 * math.sin(dt * 2.4)
            ic = icono.rotate(ang, resample=Image.BICUBIC, expand=True)
            im.alpha_composite(ic, (int(Mg + 120 - ic.width / 2), int(Mg + 175 - ic.height / 2)))
        x = Mg + 230
        s = f"{n}"
        if 0 < u < 1:                                # rueda: el número vibra un poco
            x += 3 * math.sin(dt * 60)
        _txt(d, (x, Mg + 172), s, fn_num, col, "lm", 255, borde=3)
        sub = sub_despues if u >= .5 else sub_antes
        _txt(d, (Mg + w - 40, Mg + h - 30), sub, fs, GRIS, "rm", 230)
        k = _reb(dt / .45)
        if k < .999:
            im = M.G._escala(im, k)
        return _bgra(im, min(_eo(dt / .2), (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ línea de tiempo
def linea_tiempo(hitos, titulo="Ocarina of Time", w=1640):
    """hitos = [(año, texto, ruta_imagen o None)]; marca k = aparece el hito k (con rebote). Una línea fina que crece."""
    n = len(hitos)
    h = 380
    base, Mg = _humo(w, h, alfa=.55)
    ims = []
    for _, _, r in hitos:
        if r and os.path.exists(r):
            x = Image.open(r).convert("RGBA")
            x.thumbnail((170, 110))
            ims.append(x)
        else:
            ims.append(None)
    fa, ftx, ft = fuente("s", 46), fuente("d", 26), fuente("d", 30)

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        _txt(d, (Mg + w / 2, Mg + 36), titulo.upper(), ft, AMARILLO, "mm", 255 * _eo(dt / .3), track=2)
        y = Mg + 200
        x0, x1 = Mg + 110, Mg + w - 110
        mk = list(marcas) + [dur] * (n - len(marcas))
        ult = max([k for k in range(n) if dt >= mk[k] - .05] or [-1])
        xf = x0 + (x1 - x0) * (max(0, ult) / max(1, n - 1)) * _eo((dt - (mk[ult] if ult >= 0 else 0)) / .5) if ult >= 0 else x0
        d.line([(x0, y), (max(x0, xf), y)], fill=AMARILLO + (200,), width=4)
        for k, (año, texto, _) in enumerate(hitos):
            u = (dt - mk[k]) / .45
            if u <= 0:
                continue
            x = x0 + (x1 - x0) * k / max(1, n - 1)
            s = _reb(u)
            r = 12 * s
            col = N64[k % 4]
            d.ellipse((x - r, y - r, x + r, y + r), fill=tuple(col) + (255,), outline=BLANCO + (255,), width=3)
            a = 255 * _eo(u)
            _txt(d, (x, y + 52), año, fa, BLANCO, "mm", a)
            for j, ln in enumerate(M._partir(texto, ftx, 300)[:2]):
                _txt(d, (x, y + 98 + j * 30), ln, ftx, CREMA, "mm", a)
            if ims[k] is not None:
                ic = ims[k]
                k2 = max(.05, s)
                ic2 = ic.resize((max(2, int(ic.width * k2)), max(2, int(ic.height * k2))), Image.BICUBIC)
                im.alpha_composite(M._alfa(ic2, _eo(u)), (int(x - ic2.width / 2), int(y - 30 - ic2.height)))
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ partitura de la ocarina
_FLECHA = {"^": 0, ">": 90, "v": 180, "<": 270}


def _boton(d, x, y, n, a):
    """Nota de la ocarina como en N64: A = círculo azul con «A»; C = círculo amarillo con flecha."""
    r = 26
    if n == "A":
        d.ellipse((x - r, y - r, x + r, y + r), fill=AZUL_A + (int(a),), outline=BLANCO + (int(a),), width=3)
        _txt(d, (x, y + 1), "A", fuente("d", 30), BLANCO, "mm", a)
        return
    d.ellipse((x - r, y - r, x + r, y + r), fill=AMARILLO_C + (int(a),), outline=BLANCO + (int(a),), width=3)
    ang = math.radians(_FLECHA[n])
    pts = [(0, -14), (12, 8), (-12, 8)]
    pts = [(x + px * math.cos(ang) - py * math.sin(ang), y + px * math.sin(ang) + py * math.cos(ang)) for px, py in pts]
    d.polygon(pts, fill=(60, 40, 0, int(a)))


def partitura(notas, titulo="Canción de Epona", nota_s=.32, w=1180):
    """Pentagrama translúcido con las notas (A, ^, <, >, v) que aparecen una a una desde la marca 0; en la marca 1 se apaga
    y en su lugar late la ONDA del micrófono (tararear) con «Switch 2: tararea al micrófono»."""
    h = 330
    base, Mg = _humo(w, h, alfa=.58)
    ft, fs = fuente("d", 32), fuente("si", 28)
    alturas = {"A": 4, "v": 3, ">": 2, "<": 1, "^": 0}         # posición en el pentagrama (como en el juego)

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        t0 = marcas[0] if marcas else .4
        t1 = marcas[1] if len(marcas) > 1 else dur
        _txt(d, (Mg + w / 2, Mg + 38), titulo.upper(), ft, AMARILLO, "mm", 255 * _eo(dt / .3), track=1)
        y0, paso = Mg + 110, 34
        apaga = 1 - _eo((dt - t1) / .5)
        for k in range(5):
            d.line([(Mg + 60, y0 + k * paso), (Mg + w - 60, y0 + k * paso)], fill=CREMA + (int(130 * apaga),), width=2)
        for k, n in enumerate(notas):
            u = (dt - t0 - k * nota_s) / .25
            if u <= 0:
                continue
            x = Mg + 140 + k * (w - 260) / max(1, len(notas) - 1)
            y = y0 + alturas[n] * paso
            _boton(d, x, y - 10 * (1 - _eo(u)), n, 255 * _eo(u) * apaga)
        if apaga < 1:                                       # la onda del micrófono
            b = _eo((dt - t1) / .5)
            cx, cy = Mg + w / 2, y0 + 2 * paso
            for i in range(-36, 37):
                amp = (40 + 30 * math.sin(i * .7 + dt * 9)) * math.exp(-(i / 22) ** 2) * (.6 + .4 * math.sin(dt * 5 + i))
                x = cx + i * 13
                d.line([(x, cy - amp), (x, cy + amp)], fill=(120, 200, 255, int(230 * b)), width=7)
            _txt(d, (Mg + w / 2, Mg + h - 34), "Switch 2: tararea al micrófono", fs, CREMA, "mm", 255 * b)
        else:
            _txt(d, (Mg + w / 2, Mg + h - 34), "Nintendo 64: botón A y botones C", fs, GRIS, "mm", 230 * _eo((dt - t0) / .4))
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ sticks
def _stick(d, x, y, r, a, flecha=0.0, col=(200, 200, 205)):
    d.ellipse((x - r, y - r, x + r, y + r), outline=col + (int(a),), width=5)
    d.ellipse((x - r * .55, y - r * .55, x + r * .55, y + r * .55), fill=(70, 70, 78, int(a)), outline=col + (int(a),), width=3)
    if flecha:                                     # arco que gira: la cámara libre
        ang0 = (flecha * 240) % 360
        d.arc((x - r - 26, y - r - 26, x + r + 26, y + r + 26), ang0, ang0 + 300, fill=(120, 200, 255, int(a)), width=6)
        t = math.radians(ang0 + 300)
        px, py = x + (r + 26) * math.cos(t), y + (r + 26) * math.sin(t)
        d.ellipse((px - 9, py - 9, px + 9, py + 9), fill=(120, 200, 255, int(a)))


def sticks(w=1240):
    """Dos paneles: «Nintendo 64: un stick» (mueve a Link; cámara con Z) y, desde la marca 0, «Switch 2: dos sticks» con el
    derecho girando 360° (la cámara libre)."""
    h = 360
    base, Mg = _humo(w, h, alfa=.58)
    ft, fs = fuente("d", 32), fuente("si", 26)

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        t0 = marcas[0] if marcas else dur * .45
        cx1, cx2, cy = Mg + w * .27, Mg + w * .73, Mg + 175
        a1 = 255 * _eo(dt / .4)
        _txt(d, (cx1, Mg + 40), "NINTENDO 64", ft, AMARILLO, "mm", a1, track=1)
        _stick(d, cx1, cy, 62, a1)
        _txt(d, (cx1, Mg + h - 40), "Un stick: mueve a Link / cámara con Z", fs, CREMA, "mm", a1)
        u = _eo((dt - t0) / .45)
        if u > 0:
            a2 = 255 * u
            _txt(d, (cx2, Mg + 40), "SWITCH 2", ft, (255, 90, 90), "mm", a2, track=1)
            _stick(d, cx2 - 85, cy, 52, a2)
            _stick(d, cx2 + 85, cy, 52, a2, flecha=max(.001, dt - t0))
            _txt(d, (cx2, Mg + h - 40), "Dos sticks: la cámara es tuya", fs, CREMA, "mm", a2)
            d.line([(Mg + w / 2, Mg + 80), (Mg + w / 2, Mg + h - 80)], fill=CREMA + (int(90 * u),), width=2)
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ balance final
def balance(si, no, w=1280):
    """Dos columnas: CONFIRMADO (✓ verde) y SIN CONFIRMAR (? gris). Marca k = renglón k (primero los de `si`, luego `no`)."""
    filas = max(len(si), len(no))
    h = 120 + 58 * filas + 40
    base, Mg = _humo(w, h, alfa=.6)
    ft, fr = fuente("d", 34), fuente("d", 30)

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        a0 = 255 * _eo(dt / .3)
        cx1, cx2 = Mg + w * .27, Mg + w * .73
        _txt(d, (cx1, Mg + 44), "SIN CONFIRMAR", ft, GRIS, "mm", a0, track=1)
        _txt(d, (cx2, Mg + 44), "CONFIRMADO", ft, VERDE, "mm", a0, track=1)
        _filete(d, Mg + 60, Mg + w - 60, Mg + 86, a0)
        todos = [(0, t) for t in no] + [(1, t) for t in si]
        mk = list(marcas) + [dur] * (len(todos) - len(marcas))
        cuenta = [0, 0]
        for k, (lado, t) in enumerate(todos):
            u = (dt - mk[k]) / .35
            fila = cuenta[lado]
            cuenta[lado] += 1
            if u <= 0:
                continue
            a = 255 * _eo(u)
            x = (cx1 if lado == 0 else cx2) - w * .21
            y = Mg + 124 + fila * 58 + 12 * (1 - _eo(u))
            if lado:
                d.line([(x, y), (x + 10, y + 12), (x + 30, y - 14)], fill=VERDE + (int(a),), width=6)
            else:
                _txt(d, (x + 14, y), "?", fr, GRIS, "mm", a)
            _txt(d, (x + 48, y), t, fr, BLANCO if lado else CREMA, "lm", a)
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .4))
    return fn
