# -*- coding: utf-8 -*-
"""MOTION GRAPHICS TRANSLÚCIDOS con la interfaz de SPYRO 2 (Crónicas del gaming; primer uso `spyro2`, 30-oct-2026).
Regla del usuario del 22-oct: fichas translúcidas como las de Tamriel, pero con la interfaz de CADA juego. Aquí la de Spyro 2:
  - el CUADRO DE DIÁLOGO real: pizarra azul oscura translúcida de esquinas redondas con filo claro fino, pestaña con el NOMBRE
    arriba a la izquierda y texto amarillo que se escribe letra a letra;
  - las GEMAS (roja 1, verde 2, azul 5, dorada 10, magenta 25) que giran sobre su eje: rótulo de cada secreto y HUD;
  - los NÚMEROS dorados con relieve del contador de gemas del HUD.
    import mg_spyro as S
  ficha(titulo, texto, tipo)          cuadro de diálogo; *x* = blanco resaltado
  puesto(num, titulo)                 gema que gira + «SECRETO N.º N» en oro + -título-
  pegatina(ruta, titulo, tam)         imagen REAL con borde blanco; nombre en la pestaña del diálogo
  hud(n, total)                       contador de esquina: gema + «N/30» (da ritmo en un video largo)
  gemas(titulo, pasos)                contador grande que sube por tramos; un paso por marca (valor, texto)
  linea_tiempo(hitos, titulo)         cronología; un hito por marca; el último late
  (los MG propios del guion van más abajo, cada uno con su docstring)
Probar SIEMPRE con una hoja de cuadros antes de `fx` (python nucleo/mg_spyro.py prueba).
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import mg_majora as MJ

BLANCO, CREMA, GRIS = (250, 250, 248), (232, 228, 206), (170, 182, 196)
AMARILLO, ORO, ORO_CLARO, ORO_OSC = (240, 222, 86), (250, 190, 40), (255, 238, 150), (150, 88, 14)
PIZARRA, FILO = (22, 34, 56), (150, 170, 190)
MORADO, NARANJA = (150, 96, 230), (242, 140, 44)
GEMA = {"roja": (232, 30, 52), "verde": (40, 196, 74), "azul": (54, 104, 244), "dorada": (250, 186, 34), "magenta": (226, 54, 208)}
_ORDEN = ["roja", "verde", "azul", "dorada", "magenta"]
_eo, _reb, _bgra, _txt, _salida, _rica = MJ._eo, MJ._reb, MJ._bgra, MJ._txt, MJ._salida, MJ._rica
_fj, _fc = {}, {}


def fuente(estilo, tam):
    """«s» Palatino negrita (cifras alineadas; Georgia las baila), «si» su cursiva, «d» Arial Rounded para los botones."""
    k = (estilo, int(tam))
    if k not in _fc:
        _fc[k] = ImageFont.truetype({"s": "C:/Windows/Fonts/palab.ttf", "si": "C:/Windows/Fonts/palabi.ttf",
                                     "d": "C:/Windows/Fonts/ARLRDBD.TTF"}[estilo], int(tam))
    return _fc[k]


def ajustar(s, estilo, tam, ancho, minimo=14):
    while tam > minimo and MJ._ancho(s, fuente(estilo, tam)) > ancho:
        tam -= 1
    return fuente(estilo, tam)


def caja(s, estilo, tam, ancho, alto=10_000, interlinea=1.3, minimo=16, max_lineas=7):
    while True:
        f = fuente(estilo, tam)
        ls = MJ._partir(s, f, ancho)
        lh = tam * interlinea
        if (len(ls) * lh <= alto and len(ls) <= max_lineas and max(MJ._ancho(x, f) for x in ls) <= ancho) or tam <= minimo:
            return f, ls, lh
        tam -= 1


def fuente_jp(tam):
    if tam not in _fj:
        _fj[tam] = ImageFont.truetype("C:/Windows/Fonts/YuGothB.ttc", int(tam))
    return _fj[tam]


def _capa(w, h):
    return Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))


def _marcas(marcas, n, base=.4, paso=1.8):
    mk = list(marcas or [base + paso * i for i in range(n)])
    while len(mk) < n:
        mk.append(mk[-1] + paso)
    return mk


def _actual(mk, dt, n):
    k = 0
    for i, m in enumerate(mk[:n]):
        if dt >= m:
            k = i
    return k


# ------------------------------------------------------------------ piezas
def pizarra(w, h, M=46, alfa=.46, radio=26, filo=True):
    """El cuadro de diálogo de Spyro 2: pizarra azul translúcida de esquinas redondas con un filo claro fino y sombra suave."""
    im = _capa(w + 2 * M, h + 2 * M)
    s = Image.new("L", im.size, 0)
    ImageDraw.Draw(s).rounded_rectangle((M, M + 6, M + w, M + h + 6), radio, fill=90)
    s = s.filter(ImageFilter.GaussianBlur(12))
    sombra = Image.new("RGBA", im.size, (0, 0, 0, 255))
    sombra.putalpha(s)
    im.alpha_composite(sombra)
    d = ImageDraw.Draw(im)
    capa = _capa(*im.size)
    dc = ImageDraw.Draw(capa)
    dc.rounded_rectangle((M, M, M + w, M + h), radio, fill=PIZARRA + (int(255 * alfa),))
    im.alpha_composite(capa)
    if filo:
        d.rounded_rectangle((M, M, M + w, M + h), radio, outline=FILO + (150,), width=2)
    return im, M


def pestana(d, x, y, s, f, alfa=255):
    """La pestaña con el nombre del que habla, encima del cuadro de diálogo: oscura, filo dorado fino, letras oro."""
    s = MJ._limpia(s)
    w, h = d.textlength(s, font=f) + 40, f.size * 1.5
    d.rounded_rectangle((x, y - h / 2, x + w, y + h / 2), 7, fill=(14, 20, 34, int(alfa * .86)), outline=ORO + (int(alfa * .9),), width=2)
    _txt(d, (x + 20, y + 1), s, f, ORO, "lm", alfa)


def letras_oro(im, xy, s, f, alfa=255, ancla="m", fase=None, sombra=True):
    """Letras/cifras doradas con relieve, como el contador de gemas del juego: degradado claro arriba y oscuro abajo, contorno
    oscuro. `fase` = segundos desde la entrada: cada letra cae en su sitio."""
    s = MJ._limpia(s)
    a = int(max(0, min(255, alfa)))
    if a <= 0:
        return
    d0 = ImageDraw.Draw(im)
    tot = d0.textlength(s, font=f)
    alto = int(f.size * 1.5)
    pad = 12
    cap = _capa(tot + 2 * pad, alto + 2 * pad)
    m = Image.new("L", cap.size, 0)
    dm = ImageDraw.Draw(m)
    dc = ImageDraw.Draw(cap)
    x = pad
    y = pad + alto / 2
    for i, c in enumerate(s):
        w = dm.textlength(c, font=f)
        dy = 0
        if fase is not None:
            u = _reb((fase - i * .035) / .4)
            if u <= .01:
                x += w
                continue
            dy = -22 * (1 - min(1.0, u))
        dc.text((x, y + dy), c, font=f, fill=(30, 12, 2, 255), anchor="lm", stroke_width=max(3, f.size // 15), stroke_fill=(30, 12, 2, 255))
        dm.text((x, y + dy), c, font=f, fill=255, anchor="lm")
        x += w
    grad = np.zeros((cap.height, cap.width, 4), np.uint8)
    for yy in range(cap.height):
        u = max(0.0, min(1.0, (yy - pad) / max(1, alto)))
        if u < .5:
            k = u / .5
            col = [ORO_CLARO[j] + (ORO[j] - ORO_CLARO[j]) * k for j in range(3)]
        else:
            k = (u - .5) / .5
            col = [ORO[j] + (ORO_OSC[j] - ORO[j]) * k for j in range(3)]
        grad[yy, :, :3] = col
    grad[..., 3] = np.array(m)
    cap.alpha_composite(Image.fromarray(grad, "RGBA"))
    if a < 255:
        cap.putalpha(cap.getchannel("A").point(lambda v: int(v * a / 255)))
    px = int(xy[0] - (tot / 2 if ancla == "m" else (tot if ancla == "r" else 0))) - pad
    py = int(xy[1] - alto / 2) - pad
    if sombra:
        so = Image.new("RGBA", cap.size, (0, 0, 0, 255))
        so.putalpha(cap.getchannel("A").point(lambda v: int(v * .5)))
        im.alpha_composite(so, (max(0, px + 3), max(0, py + 5)))
    im.alpha_composite(cap, (max(0, px), max(0, py)))


def gema(tam, color="verde", giro=0.0):
    """Gema facetada de Spyro: octógono tallado con tabla clara, facetas y destello. `giro` en radianes: ancho = |cos|."""
    S = int(max(4, tam))
    base = GEMA.get(color, color)
    cla = tuple(min(255, int(c + (255 - c) * .55)) for c in base)
    osc = tuple(int(c * .52) for c in base)
    im = _capa(S, S)
    d = ImageDraw.Draw(im)
    c = S / 2
    R = S * .47
    ext = [(c + math.cos(math.pi / 8 + k * math.pi / 4) * R, c + math.sin(math.pi / 8 + k * math.pi / 4) * R * .84) for k in range(8)]
    tab = [(c + math.cos(math.pi / 8 + k * math.pi / 4) * R * .52, c - S * .05 + math.sin(math.pi / 8 + k * math.pi / 4) * R * .4) for k in range(8)]
    d.polygon(ext, fill=base + (255,))
    for k in range(8):
        p = [ext[k], ext[(k + 1) % 8], tab[(k + 1) % 8], tab[k]]
        my = sum(q[1] for q in p) / 4
        lado = math.sin(math.pi / 8 + k * math.pi / 4 + math.pi / 8)
        col = cla if lado < -.3 else (osc if lado > .35 else base)
        d.polygon(p, fill=col + (255,))
    d.polygon(tab, fill=cla + (255,))
    d.polygon([tab[4], tab[5], tab[6]], fill=(255, 255, 255, 215))
    k = max(.3, abs(math.cos(giro)))
    return im.resize((max(2, int(S * k)), S), Image.BICUBIC)


def gema_de(num):
    return _ORDEN[int(num) % len(_ORDEN)]


def _chispas(d, cx, cy, r, dt, n=6, alfa=255, col=(255, 250, 210)):
    for i in range(n):
        a = dt * 1.2 + i * 2 * math.pi / n
        u = .5 + .5 * math.sin(dt * 4 + i * 1.7)
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r * .8
        s = 5 + 8 * u
        c = col + (int(alfa * u),)
        d.line([(x - s, y), (x + s, y)], fill=c, width=3)
        d.line([(x, y - s), (x, y + s)], fill=c, width=3)


def _ranura(im, m, dt, x, y, tam=30):
    """Gema pequeña que gira: el «siguiente» del diálogo."""
    g = gema(tam, "verde", dt * 3.2)
    im.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))


# ------------------------------------------------------------------ ficha = cuadro de diálogo
def ficha(titulo, texto, tipo=None, ancho=900, vel=55):
    """Cuadro de diálogo de Spyro 2: `titulo` en la pestaña, `tipo` en gris, y el texto amarillo que se ESCRIBE letra a letra
    (vel = letras/s). *x* = blanco. Al terminar gira una gema pequeña, como el aviso de seguir."""
    in_w = ancho - 2 * 44
    fp = ajustar(titulo, "s", 32, in_w - 60)
    fty = ajustar(tipo, "si", 25, in_w) if tipo else None
    fx, ls, lh = caja(texto, "s", 33, in_w, max_lineas=7)
    h = int(46 + (36 if tipo else 0) + lh * len(ls) + 40)
    M_ = 46
    base, M = pizarra(ancho, h)
    lien = _capa(base.width, base.height + 34)
    lien.alpha_composite(base, (0, 34))
    letras = [len(x.replace("*", "")) for x in ls]

    def fn(dt, dur, marcas):
        im = lien.copy()
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 34, titulo, fp, 255 * _eo((dt - .1) / .3))
        y = M + 34 + 44
        if tipo:
            _txt(d, (M + 44, y + 6), tipo, fty, GRIS, "lm", 230 * _eo((dt - .3) / .3))
            y += 36
        y += lh / 2
        quedan = max(0.0, (dt - .4) * vel)
        for ln, n in zip(ls, letras):
            _rica(d, M + 44, y, ln, fx, AMARILLO, BLANCO, 255, "l", hasta=quedan)
            quedan -= n
            y += lh
        if quedan > 0:
            _ranura(im, M, dt, M + ancho - 36, M + 34 + h - 30)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ rótulo de secreto
def puesto(num, titulo, arriba=None):
    """Banda translúcida: a la izquierda la gema del número (color por número) que entra con rebote y gira; «SECRETO N.º N» en
    oro con relieve, letra a letra; debajo el título en amarillo, como el nombre de un nivel."""
    arriba = arriba or f"Secreto n.º {num}"
    w, h = 1540, 226
    f1 = ajustar(arriba.upper(), "s", 76, w - 400)
    f2 = ajustar(titulo, "si", 44, w - 400)
    col = gema_de(num)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h, alfa=.5, radio=30)
        d = ImageDraw.Draw(im)
        s = _reb((dt - .05) / .5)
        if s > .02:
            g = gema(176 * s, col, dt * 2.2)
            im.alpha_composite(g, (int(M + 136 - g.width / 2), int(M + h / 2 - g.height / 2)))
            _chispas(d, M + 136, M + h / 2, 108, dt, alfa=220 * min(1, s))
        tx = M + 262 + (w - 262) / 2 - 30
        letras_oro(im, (tx, M + 84), arriba.upper(), f1, 255, fase=dt - .15)
        u = _eo((dt - .3) / .5)
        MJ._filete(d, tx - 320 * u, tx + 320 * u, M + 142, 255 * u, color=ORO)
        _txt(d, (tx, M + 182), titulo, f2, AMARILLO, "mm", 255 * _eo((dt - .55) / .5))
        return _bgra(im, min(_eo(dt / .3), (dur - dt) / .5))
    return fn


# ------------------------------------------------------------------ pegatina
def pegatina(ruta, titulo=None, tam=360, giro=-5.0):
    """Imagen REAL recortada con borde blanco (mg_tes) con rebote y balanceo; el nombre en la pestaña del diálogo."""
    import mg_tes as T
    base = T._base_pegatina(ruta, tam)
    if titulo:
        tit = MJ._limpia(titulo)
        f = ajustar(tit, "s", 30, max(260, base.width + 40))
        pw, ph = int(MJ._ancho(tit, f) + 48), 56
        pil = _capa(pw, ph)
        dp = ImageDraw.Draw(pil)
        dp.rounded_rectangle((0, 0, pw - 1, ph - 1), 9, fill=(14, 20, 34, 205), outline=ORO + (235,), width=2)
        _txt(dp, (pw / 2, ph / 2 + 1), tit, f, ORO, "mm", 255)
        lien = _capa(max(base.width, pw), base.height + ph // 2)
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
        if dur - dt < .3:
            out[..., 3] = (out[..., 3] * max(0.0, (dur - dt) / .3)).astype(np.uint8)
        return out
    return fn


# ------------------------------------------------------------------ HUD
def hud(n, total=30, w=250, h=96):
    """Contador de esquina como el de gemas del juego: la gema del número gira y las cifras doradas caen al entrar."""
    col = gema_de(n)
    s = f"{n}/{total}"
    f = fuente("s", 50)

    def fn(dt, dur, marcas):
        im = _capa(w, h)
        g = gema(76, col, dt * 2.0)
        im.alpha_composite(g, (int(46 - g.width / 2), int(h / 2 - g.height / 2)))
        letras_oro(im, (92, h / 2), s, f, 255, ancla="l", fase=dt)
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .35))
    return fn


def gemas(titulo, pasos, w=1160, h=340, color="dorada"):
    """El contador del HUD en grande: la gema late y el número SUBE hasta el valor de cada paso; debajo el texto del paso.
    pasos = [(valor, texto)]; marca k = paso k. Si el valor es texto ya formateado, usa (valor, texto, «9 991»)."""
    fp = ajustar(titulo, "s", 32, w - 120)
    fn_ = fuente("s", 104)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, len(pasos), .3, 1.8)
        k = _actual(mk, dt, len(pasos))
        v0 = pasos[k - 1][0] if k else 0
        v1, texto = pasos[k][0], pasos[k][1]
        u = _eo((dt - mk[k]) / 1.1)
        v = v0 + (v1 - v0) * u
        cy = M + 130
        g = gema(148 * (1 + .05 * math.sin(dt * 5)), color, dt * 1.8)
        im.alpha_composite(g, (int(M + w / 2 - 340 - g.width / 2), int(cy - g.height / 2)))
        s = pasos[k][2] if len(pasos[k]) > 2 and u >= 1 else f"{int(round(v)):,}".replace(",", " ")
        letras_oro(im, (M + w / 2 + 60, cy), s, fn_, 255)
        d = ImageDraw.Draw(im)
        _txt(d, (M + w / 2, M + h - 58), texto, ajustar(texto, "s", 34, w - 110), CREMA, "mm", 255 * _eo((dt - mk[k] - .3) / .4))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ cronología
def linea_tiempo(hitos, titulo="Así se hizo", w=1720, h=410):
    """Línea dorada que se dibuja; marca k = hito k: una gema cae en su sitio, el año en oro y el texto debajo. El último late."""
    n = len(hitos)
    fp = ajustar(titulo, "s", 32, w - 120)
    fa = fuente("s", 48)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, n, .4, 1.4)
        x0, x1, y = M + 120, M + w - 120, M + 186
        paso = (x1 - x0) / max(1, n - 1)
        lx = x0 + (x1 - x0) * min(1.0, max(0.0, (dt - mk[0] + .3) / max(.5, mk[n - 1] - mk[0] + .3)))
        d.line([(x0, y), (lx, y)], fill=ORO + (230,), width=5)
        for i, ((anio, texto), m) in enumerate(zip(hitos, mk)):
            if dt < m:
                continue
            cx = x0 + paso * i
            s = _reb((dt - m) / .45)
            late = 1 + (.12 * math.sin(dt * 6) if i == n - 1 else 0)
            g = gema(66 * s * late, _ORDEN[i % 5], (dt - m) * 2)
            im.alpha_composite(g, (int(cx - g.width / 2), int(y - g.height / 2)))
            letras_oro(im, (cx, y - 70), str(anio), fa, 255 * _eo((dt - m) / .3))
            d = ImageDraw.Draw(im)
            f, ls, lh = caja(texto, "s", 27, paso - 26 if n > 1 else w - 200, 140, max_lineas=4)
            for j, l_ in enumerate(ls):
                _txt(d, (cx, y + 66 + lh * j), l_, f, CREMA, "mm", 255 * _eo((dt - m - .2) / .4))
        return _salida(im, dt, dur)
    return fn


# ================================================================== MG PROPIOS DEL GUION (spyro2, 30-oct-2026)
def _foto(ruta, w, h, radio=16, marco=(240, 240, 235)):
    im = Image.open(ruta).convert("RGB")
    k = max(w / im.width, h / im.height)
    im = im.resize((int(im.width * k + 1), int(im.height * k + 1)), Image.LANCZOS)
    x, y = (im.width - w) // 2, (im.height - h) // 2
    im = im.crop((x, y, x + w, y + h)).convert("RGBA")
    m = Image.new("L", (w, h), 0)
    ImageDraw.Draw(m).rounded_rectangle((0, 0, w - 1, h - 1), radio, fill=255)
    im.putalpha(m)
    out = _capa(w + 8, h + 8)
    ImageDraw.Draw(out).rounded_rectangle((0, 0, w + 7, h + 7), radio + 4, fill=marco + (255,))
    out.alpha_composite(im, (4, 4))
    return out


def nombres(filas, titulo="Un juego, tres nombres", w=1500, h=None):
    """Tabla de regiones: marca k = fila k entra de lado; región en gris a la izquierda y el nombre en oro. filas = [(región, nombre)]."""
    n = len(filas)
    h = h or 110 + 96 * n
    fp = ajustar(titulo, "s", 32, w - 120)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, n, .4, 1.1)
        for i, ((reg, nom), m) in enumerate(zip(filas, mk)):
            if dt < m:
                continue
            u = _eo((dt - m) / .45)
            y = M + 88 + 96 * i
            _txt(d, (M + 60 - 40 * (1 - u), y), reg, fuente("s", 34), GRIS, "lm", 255 * u)
            f = ajustar(nom, "s", 52, w - 370)
            letras_oro(im, (M + 330 + 40 * (1 - u), y), nom, f, 255 * u, ancla="l")
            d = ImageDraw.Draw(im)
            if i < n - 1:
                d.line([(M + 60, y + 48), (M + w - 60, y + 48)], fill=FILO + (int(70 * u),), width=1)
        return _salida(im, dt, dur)
    return fn


def _boton(d, im, x, y, b, r=50, on=0.0):
    """Botón de mando de PlayStation: triángulo verde, círculo rojo, cruz azul, cuadrado rosa; L1/R1/R2 y flecha arriba. on = 0..1 pulsado."""
    PS = {"tri": (64, 210, 170), "cir": (240, 80, 80), "cru": (110, 150, 240), "cua": (240, 130, 200)}
    yy = y + 6 * on
    if b in PS:
        col = PS[b]
        d.ellipse((x - r, y - r + 7, x + r, y + r + 7), fill=(6, 8, 14, 230))
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=(38, 40, 48, 255), outline=(ORO if on > .4 else (90, 92, 104)) + (255,), width=4)
        a = r * .46
        if b == "tri":
            d.polygon([(x, yy - a), (x + a, yy + a * .72), (x - a, yy + a * .72)], outline=col + (255,), width=6)
        elif b == "cir":
            d.ellipse((x - a, yy - a, x + a, yy + a), outline=col + (255,), width=6)
        elif b == "cru":
            d.line([(x - a, yy - a), (x + a, yy + a)], fill=col + (255,), width=7)
            d.line([(x + a, yy - a), (x - a, yy + a)], fill=col + (255,), width=7)
        else:
            d.rectangle((x - a, yy - a, x + a, yy + a), outline=col + (255,), width=6)
    elif b == "arriba":
        d.ellipse((x - r, y - r + 7, x + r, y + r + 7), fill=(6, 8, 14, 230))
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=(38, 40, 48, 255), outline=(ORO if on > .4 else (90, 92, 104)) + (255,), width=4)
        a = r * .5
        d.polygon([(x, yy - a), (x + a * .9, yy + a * .55), (x - a * .9, yy + a * .55)], fill=(226, 226, 232, 255))
    else:
        w_, h_ = r * 1.3, r * .74
        d.rounded_rectangle((x - w_, y - h_ + 7, x + w_, y + h_ + 7), 12, fill=(6, 8, 14, 230))
        d.rounded_rectangle((x - w_, yy - h_, x + w_, yy + h_), 12, fill=(38, 40, 48, 255),
                            outline=(ORO if on > .4 else (90, 92, 104)) + (255,), width=4)
        _txt(d, (x, yy), b, fuente("d", int(r * .72)), BLANCO, "mm", 255)


def codigo(botones, titulo, resultado=None, w=None, h=380):
    """Un truco: fila de botones que se pulsan en orden; cada uno se enciende y queda dorado; al final sale `resultado`.
    botones = lista de 'arriba','cir','cua','tri','cru','L1','R1','R2' y grupos 'x4' como ('arriba', 4). `marcas[0]` = arranca,
    `marcas[1]` = sale el resultado."""
    seq = []
    for b in botones:
        seq.append(b if isinstance(b, tuple) else (b, 1))
    w = w or min(1680, 300 + 230 * len(seq))
    fp = ajustar(titulo, "s", 32, w - 120)
    paso = (w - 200) / max(1, len(seq) - 1) if len(seq) > 1 else 0

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, 2, .5, 3.0)
        t = (dt - mk[0]) / max(.6, (mk[1] - mk[0]) * .9)
        for i, (b, nv) in enumerate(seq):
            x = M + (100 + paso * i if len(seq) > 1 else w / 2)
            cy = M + 150
            ent = _reb((dt - .25 - i * .08) / .4)
            if ent < .03:
                continue
            u = t * len(seq) - i
            on = 1.0 if u >= 1 else (.3 + .7 * abs(math.sin(u * math.pi * max(1, nv))) if 0 <= u < 1 else 0.0)
            _boton(d, im, x, cy, b, int(54 * min(1.1, ent)), on)
            if nv > 1:
                letras_oro(im, (x, cy + 88), f"×{nv}", fuente("s", 40), 255 * ent)
                d = ImageDraw.Draw(im)
        if resultado and dt >= mk[1]:
            _txt(d, (M + w / 2, M + h - 54), resultado, ajustar(resultado, "s", 36, w - 110), AMARILLO, "mm", 255 * _eo((dt - mk[1]) / .4))
        return _salida(im, dt, dur)
    return fn


def pilones(poderes=("Supercarga", "Supercongelación", "Supervuelo"), titulo="Pilones", w=1500, h=400):
    """Los espíritus cargan el par de pilones: dos columnas con chispas que van llenándose (marca 0); marca k+1 = se enciende el poder k."""
    fp = ajustar(titulo, "s", 32, w - 120)
    col = [NARANJA, (250, 230, 90), (120, 210, 255), (200, 150, 255)]

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, 1 + len(poderes), .4, 1.2)
        lleno = min(1.0, max(0.0, (dt - mk[0]) / max(.6, mk[1] - mk[0])))
        for sx in (M + 110, M + 300):
            d.rounded_rectangle((sx - 36, M + 86, sx + 36, M + h - 40), 12, outline=FILO + (200,), width=3)
            y1 = M + h - 46
            y0 = y1 - (h - 132) * lleno
            d.rounded_rectangle((sx - 30, y0, sx + 30, y1), 10, fill=NARANJA + (210,))
        for i in range(10):
            u = ((dt * .9 + i * .1) % 1.0)
            if lleno >= 1:
                break
            x = M + 205 + (-95 if i % 2 else 95) * u
            y = M + 80 + (h - 170) * (1 - abs(u - .5) * 1.6)
            d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=(240, 250, 255, 220))
        ancho = (w - 470) / 2
        for i, nom in enumerate(poderes):
            m = mk[i + 1]
            if dt < m:
                continue
            u = _reb((dt - m) / .4)
            x = M + 410 + ancho * (i % 2) + ancho / 2
            y = M + 138 + 130 * (i // 2)
            c = col[i % 4]
            late = .5 + .5 * math.sin(dt * 5 + i)
            glow = _capa(*im.size)
            ImageDraw.Draw(glow).ellipse((x - 150, y - 56, x + 150, y + 56), fill=c + (int(46 + 34 * late),))
            im.alpha_composite(glow.filter(ImageFilter.GaussianBlur(22)))
            d = ImageDraw.Draw(im)
            f = ajustar(nom, "s", max(16, int(48 * min(1.08, u))), ancho - 30)
            _txt(d, (x, y), nom, f, c, "mm", 255 * min(1, u))
        return _salida(im, dt, dur)
    return fn


def mundos(fotos, nombres_, titulo="Avalar", w=1660, h=430):
    """Los tres mundos de Avalar como portales en fila (esquema, NO un mapa): cada portal es una foto REAL del mundo con arco
    dorado y su nombre; la línea dorada los une. Una marca por mundo."""
    n = len(fotos)
    fp = ajustar(titulo, "s", 32, w - 120)
    pw, ph = int((w - 240) / n) - 40, 250
    tiles = [_foto(p, pw, ph) for p in fotos]

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, n, .4, 1.4)
        paso = (w - 120) / n
        for i in range(n):
            if dt < mk[i]:
                continue
            cx = M + 60 + paso * (i + .5)
            s = _reb((dt - mk[i]) / .45)
            t = tiles[i].resize((max(2, int(tiles[i].width * s)), max(2, int(tiles[i].height * s))), Image.BILINEAR)
            im.alpha_composite(t, (int(cx - t.width / 2), int(M + 200 - t.height / 2)))
            if i:
                u = _eo((dt - mk[i]) / .4)
                x0 = M + 60 + paso * (i - .5) + pw / 2
                x1 = x0 + (paso - pw) * u
                d = ImageDraw.Draw(im)
                d.line([(x0, M + 200), (x1, M + 200)], fill=ORO + (255,), width=6)
            letras_oro(im, (cx, M + h - 44), nombres_[i], ajustar(nombres_[i], "s", 42, pw), 255 * _eo((dt - mk[i] - .15) / .3))
        return _salida(im, dt, dur)
    return fn


def renombres(pares, titulo="Nombres de desarrollo", w=1500, h=None):
    """Lista de nombres viejos: marca k = par k; el viejo sale en gris, una raya lo tacha y el nuevo aparece en oro. pares = [(viejo, nuevo)]."""
    n = len(pares)
    h = h or 104 + 84 * n
    fp = ajustar(titulo, "s", 32, w - 120)
    fv = fuente("s", 38)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, n, .4, 1.0)
        for i, ((vie, nue), m) in enumerate(zip(pares, mk)):
            if dt < m:
                continue
            y = M + 84 + 84 * i
            u = _eo((dt - m) / .3)
            x = M + w * .46
            _txt(d, (x, y), vie, ajustar(vie, "s", 38, w * .4), GRIS, "rm", 255 * u)
            r = _eo((dt - m - .35) / .3)
            if r > 0:
                wv = d.textlength(vie, font=ajustar(vie, "s", 38, w * .4))
                d.line([(x - wv - 6, y + 2), (x - wv - 6 + (wv + 12) * r, y + 2)], fill=(240, 70, 70, 255), width=5)
                d.polygon([(x + 28, y - 12), (x + 52, y), (x + 28, y + 12)], fill=ORO + (int(255 * r),))
                letras_oro(im, (x + 76, y), nue, ajustar(nue, "s", 44, w * .42), 255 * r, ancla="l")
                d = ImageDraw.Draw(im)
        return _salida(im, dt, dur)
    return fn


def katakana(w=1280, h=430):
    """スパイロ en grande (el logo japonés de Spyro); marca 1 = debajo se lee «RIPTO» letra a letra: el nombre del villano sale de
    leer mal el logo. Marca 0 = entra el katakana."""
    fj = fuente_jp(170)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, "El logo japonés de Spyro", fuente("s", 32), 255 * _eo(dt / .3))
        mk = _marcas(marcas, 2, .4, 2.2)
        s = _reb((dt - mk[0]) / .5)
        if s > .02:
            _txt(d, (M + w / 2, M + 170), "スパイロ", fuente_jp(max(10, int(170 * min(1.05, s)))), BLANCO, "mm", 255, borde=3)
        if dt >= mk[1]:
            letras_oro(im, (M + w / 2, M + h - 86), "RIPTO", fuente("s", 118), 255, fase=(dt - mk[1]) * .45)
        return _salida(im, dt, dur)
    return fn


def anagrama(origen="CAROLINE", destino="ELORA", w=1320, h=430, pie=None):
    """Las letras de `origen` en fila (marca 0); las de `destino` se encienden, suben y se ordenan (marca 1). El resto se apaga."""
    fo, fd = fuente("s", 96), fuente("s", 104)
    pos, usadas = [], set()
    for c in destino:
        for i, o in enumerate(origen):
            if o == c and i not in usadas:
                pos.append(i)
                usadas.add(i)
                break
    ao = 112
    x0 = (w - ao * (len(origen) - 1)) / 2
    ad = 124
    xd0 = (w - ad * (len(destino) - 1)) / 2

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, "De dónde salió el nombre", fuente("s", 32), 255 * _eo(dt / .3))
        mk = _marcas(marcas, 2, .4, 2.0)
        if dt < mk[0]:
            return _salida(im, dt, dur)
        u = _eo((dt - mk[1]) / 1.0) if dt >= mk[1] else 0.0
        for i, c in enumerate(origen):
            if i in usadas:
                continue
            _txt(d, (M + x0 + ao * i, M + 300), c, fo, GRIS, "mm", 255 * _eo((dt - mk[0] - i * .05) / .25) * (1 - .55 * u))
        for j, i in enumerate(pos):
            x = x0 + ao * i + (xd0 + ad * j - x0 - ao * i) * u
            y = 300 - 170 * u
            if dt < mk[1]:
                _txt(d, (M + x, M + y), origen[i], fo, CREMA, "mm", 255 * _eo((dt - mk[0] - i * .05) / .25))
            else:
                letras_oro(im, (M + x, M + y), origen[i], fd, 255, sombra=False)
                d = ImageDraw.Draw(im)
        if pie and u >= 1:
            _txt(d, (M + w / 2, M + h - 40), pie, ajustar(pie, "s", 30, w - 120), CREMA, "mm", 255 * _eo((dt - mk[1] - 1) / .4))
        return _salida(im, dt, dur)
    return fn


def rueda(digitos, titulo, pie=None, w=1160, h=390):
    """Cerradura de 5 dígitos: cada rueda gira y se detiene en su número, una tras otra (marca 0); marca 1 = sale `pie`."""
    fp = ajustar(titulo, "s", 32, w - 120)
    n = len(digitos)
    fd = fuente("s", 120)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, 2, .4, 2.4)
        anc = 160
        x0 = M + (w - anc * (n - 1)) / 2
        for i, c in enumerate(digitos):
            fin = mk[0] + .5 + i * .32
            x = x0 + anc * i
            d.rounded_rectangle((x - 66, M + 76, x + 66, M + 256), 14, fill=(10, 14, 24, 170), outline=ORO + (200,), width=3)
            s = c if dt >= fin else str(int(dt * 17 + i * 3) % 10)
            letras_oro(im, (x, M + 166), s, fd, 255 if dt >= fin else 200, sombra=False)
            d = ImageDraw.Draw(im)
        if pie and dt >= mk[1]:
            _txt(d, (M + w / 2, M + h - 58), pie, ajustar(pie, "s", 36, w - 110), AMARILLO, "mm", 255 * _eo((dt - mk[1]) / .4))
        return _salida(im, dt, dur)
    return fn


def _engrane(d, cx, cy, r, ang, col=(204, 196, 176)):
    n = 10
    pts = []
    for k in range(n * 4):
        a = ang + k * math.pi / (2 * n)
        rr = r if k % 4 in (0, 1) else r * .76
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=col + (255,), outline=(70, 60, 50, 255))
    d.ellipse((cx - r * .3, cy - r * .3, cx + r * .3, cy + r * .3), fill=(40, 34, 30, 255))


def vagoneta(titulo="Gear Grab: 50 engranajes", total=50, w=1500, h=380):
    """El reto: el contador de engranajes del HUD sube de 0 a `total` entre la marca 0 y la marca 1 y al llegar late en oro."""
    fp = ajustar(titulo, "s", 32, w - 120)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, 2, .3, 3.0)
        t = min(1.0, max(0.0, (dt - mk[0]) / max(.5, mk[1] - mk[0])))
        n = int(round(total * t))
        cols, tam = 25, 46
        for i in range(total):
            x = M + 90 + (w - 180) / (cols - 1) * (i % cols)
            y = M + 104 + 76 * (i // cols)
            if i < n:
                _engrane(d, x, y, tam / 2 + 2, dt * 2 + i)
            else:
                d.ellipse((x - 7, y - 7, x + 7, y + 7), fill=FILO + (60,))
        late = 1 + (.06 * math.sin(dt * 6) if n >= total else 0)
        letras_oro(im, (M + w / 2, M + 276), f"{n} / {total}", fuente("s", int(72 * late)), 255)
        return _salida(im, dt, dur)
    return fn


def pantallas_negras(fotos, nombres_, titulo="Copia pirata europea", pie="Pantalla en negro", w=1400, h=440):
    """Dos televisores con la foto REAL de cada nivel; marca 1 = la imagen se apaga a negro (franja de TV que se cierra) y sale `pie`.
    Marca 0 = entran."""
    fp = ajustar(titulo, "s", 32, w - 120)
    pw, ph = 560, 300
    tiles = [_foto(p, pw, ph, radio=10) for p in fotos]

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, 2, .3, 2.0)
        for i, t in enumerate(tiles):
            cx = M + w * (.27 + .46 * i)
            x, y = int(cx - t.width / 2), int(M + 62)
            im.alpha_composite(t, (x, y))
            if dt >= mk[1] + i * .5:
                u = _eo((dt - mk[1] - i * .5) / .4)
                neg = _capa(t.width - 8, t.height - 8)
                nd = ImageDraw.Draw(neg)
                hh = neg.height / 2 * u
                nd.rectangle((0, 0, neg.width, hh), fill=(0, 0, 0, 255))
                nd.rectangle((0, neg.height - hh, neg.width, neg.height), fill=(0, 0, 0, 255))
                im.alpha_composite(neg, (x + 4, y + 4))
                d = ImageDraw.Draw(im)
            f = ajustar(nombres_[i], "s", 34, pw)
            _txt(d, (cx, M + h - 44), nombres_[i], f, AMARILLO, "mm", 255)
        if dt >= mk[1] + 1:
            s = _reb((dt - mk[1] - 1) / .4)
            _txt(d, (M + w / 2, M + 212), pie, fuente("s", max(10, int(58 * min(1.05, s)))), (255, 96, 86), "mm", 255, borde=3)
        return _salida(im, dt, dur)
    return fn


def discos(a, b, foto_a, foto_b, titulo="Cada uno dentro del otro", w=1320, h=470):
    """Dos discos con la caja/foto REAL en la etiqueta; marca 0 = entran girando; marca 1 = flecha de A a B; marca 2 = de B a A."""
    fp = ajustar(titulo, "s", 32, w - 120)
    R = 160

    def disco(ruta):
        f = Image.open(ruta).convert("RGB")
        k = max(2 * R / f.width, 2 * R / f.height)
        f = f.resize((int(f.width * k + 1), int(f.height * k + 1)), Image.LANCZOS)
        x, y = (f.width - 2 * R) // 2, (f.height - 2 * R) // 2
        f = f.crop((x, y, x + 2 * R, y + 2 * R)).convert("RGBA")
        m = Image.new("L", (2 * R, 2 * R), 0)
        md = ImageDraw.Draw(m)
        md.ellipse((0, 0, 2 * R - 1, 2 * R - 1), fill=255)
        md.ellipse((R - 26, R - 26, R + 26, R + 26), fill=0)
        f.putalpha(m)
        ImageDraw.Draw(f).ellipse((1, 1, 2 * R - 2, 2 * R - 2), outline=(230, 230, 240, 255), width=4)
        return f
    da, db = disco(foto_a), disco(foto_b)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, 3, .3, 1.8)
        cy = M + 216
        s = _reb((dt - mk[0]) / .5)
        if s < .03:
            return _salida(im, dt, dur)
        ca, cb = M + w * .22, M + w * .78
        for dd, cx, sgn, nom in ((da, ca, 1, a), (db, cb, -1, b)):
            r = dd.rotate(sgn * dt * 40, resample=Image.BICUBIC)
            k = max(.05, min(1.05, s))
            r = r.resize((int(r.width * k), int(r.height * k)), Image.BILINEAR)
            im.alpha_composite(r, (int(cx - r.width / 2), int(cy - r.height / 2)))
            d = ImageDraw.Draw(im)
            _txt(d, (cx, M + h - 42), nom, ajustar(nom, "s", 34, 460), AMARILLO, "mm", 255 * min(1, s))
        x0, x1 = ca + R + 26, cb - R - 26
        for i, (yy, ida) in enumerate(((cy - 42, True), (cy + 42, False))):
            m = mk[i + 1]
            if dt < m:
                continue
            u = _eo((dt - m) / .5)
            a0, a1 = (x0, x1) if ida else (x1, x0)
            xf = a0 + (a1 - a0) * u
            d.line([(a0, yy), (xf, yy)], fill=ORO + (255,), width=8)
            sg = 1 if ida else -1
            d.polygon([(xf + sg * 26, yy), (xf, yy - 18), (xf, yy + 18)], fill=ORO + (255,))
        return _salida(im, dt, dur)
    return fn


def trueque(pasos, titulo="La misión del lápiz", w=1720, h=340):
    """La cadena de trueques: marca k = paso k; cada uno es una imagen REAL (o solo texto) unida al anterior por una flecha.
    pasos = [(texto, ruta o None)]; el último brilla con chispas doradas."""
    n = len(pasos)
    fp = ajustar(titulo, "s", 32, w - 120)
    tiles = []
    for tx, ruta in pasos:
        tiles.append(_foto(ruta, 160, 160) if ruta and os.path.exists(ruta) else None)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, n, .4, 1.1)
        paso = (w - 120) / n
        for i, ((tx, _), m) in enumerate(zip(pasos, mk)):
            if dt < m:
                continue
            cx = M + 60 + paso * (i + .5)
            s = _reb((dt - m) / .4)
            cy = M + 140
            if tiles[i] is not None:
                t = tiles[i].resize((max(2, int(tiles[i].width * s)), max(2, int(tiles[i].height * s))), Image.BILINEAR)
                im.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))
            else:
                g = gema(120 * s, "dorada" if i == n - 1 else _ORDEN[i % 3], dt * 2)
                im.alpha_composite(g, (int(cx - g.width / 2), int(cy - g.height / 2)))
            d = ImageDraw.Draw(im)
            if i == n - 1:
                _chispas(d, cx, cy, 112, dt)
            _txt(d, (cx, M + h - 56), tx, ajustar(tx, "s", 32, paso - 16), AMARILLO if i == n - 1 else CREMA, "mm", 255 * min(1, s))
            if i:
                xa = cx - paso * .5
                d.polygon([(xa - 14, cy - 18), (xa + 16, cy), (xa - 14, cy + 18)], fill=ORO + (int(255 * min(1, s)),))
        return _salida(im, dt, dur)
    return fn


def relacion(centro, ramas, titulo, w=1500, h=470):
    """Un solo nombre en el centro y sus papeles alrededor. centro = (nombre, foto o None); ramas = [(papel, foto)], una marca por rama."""
    n = len(ramas)
    fp = ajustar(titulo, "s", 32, w - 120)
    tc = _foto(centro[1], 210, 210) if centro[1] and os.path.exists(centro[1]) else None
    tiles = [_foto(r[1], 190, 190) if r[1] and os.path.exists(r[1]) else None for r in ramas]

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, n + 1, .3, 1.2)
        cx, cy = M + 260, M + 214
        s = _reb((dt - mk[0]) / .4)
        if tc is not None and s > .03:
            t = tc.resize((max(2, int(tc.width * s)), max(2, int(tc.height * s))), Image.BILINEAR)
            im.alpha_composite(t, (int(cx - t.width / 2), int(cy - t.height / 2)))
        d = ImageDraw.Draw(im)
        letras_oro(im, (cx, M + h - 56), centro[0], ajustar(centro[0], "s", 42, 430), 255 * min(1, s))
        paso = (w - 520) / max(1, n)
        for i, ((nom, _), m) in enumerate(zip(ramas, mk[1:])):
            if dt < m:
                continue
            x = M + 500 + paso * (i + .5)
            u = _eo((dt - m) / .4)
            d = ImageDraw.Draw(im)
            d.line([(cx + 110, cy), (cx + 110 + (x - 100 - cx - 110) * u, cy)], fill=ORO + (220,), width=5)
            if tiles[i] is not None:
                k = _reb((dt - m) / .45)
                t = tiles[i].resize((max(2, int(tiles[i].width * k)), max(2, int(tiles[i].height * k))), Image.BILINEAR)
                im.alpha_composite(t, (int(x - t.width / 2), int(cy - t.height / 2)))
            d = ImageDraw.Draw(im)
            _txt(d, (x, M + h - 56), nom, ajustar(nom, "s", 34, paso - 20), AMARILLO, "mm", 255 * u)
        return _salida(im, dt, dur)
    return fn


def notas(filas, titulo="La crítica", w=1320, h=330):
    """Notas de la prensa: marca k = medio k; la cifra sube en oro. filas = [(medio, valor numérico, texto de la cifra)]."""
    n = len(filas)
    fp = ajustar(titulo, "s", 32, w - 120)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, n, .4, 1.3)
        paso = (w - 120) / n
        for i, ((med, val, tx), m) in enumerate(zip(filas, mk)):
            if dt < m:
                continue
            cx = M + 60 + paso * (i + .5)
            u = _eo((dt - m) / .7)
            s = tx if u >= 1 else f"{val * u:.1f}".replace(".", ",")
            letras_oro(im, (cx, M + 140), s, ajustar("00,0", "s", 96, paso - 30), 255)
            d = ImageDraw.Draw(im)
            _txt(d, (cx, M + 240), med, ajustar(med, "s", 36, paso - 20), CREMA, "mm", 255 * _eo((dt - m) / .4))
        return _salida(im, dt, dur)
    return fn


def libreta(filas, titulo, w=1400, h=None, gema_col="verde"):
    """Lista que se escribe: marca k = fila k entra con una gema de viñeta. *x* = blanco. Sirve para los planes de Moneybags, las
    criaturas de Faunus Mortas o los temas de los prototipos."""
    n = len(filas)
    h = h or 96 + 72 * n
    fp = ajustar(titulo, "s", 32, w - 120)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, n, .4, 1.0)
        for i, (tx, m) in enumerate(zip(filas, mk)):
            if dt < m:
                continue
            u = _eo((dt - m) / .35)
            y = M + 78 + 72 * i
            g = gema(46, gema_col if i % 2 == 0 else "azul", (dt - m) * 2.5)
            im.alpha_composite(g, (int(M + 62 - g.width / 2), int(y - g.height / 2)))
            d = ImageDraw.Draw(im)
            f, ls, _lh = caja(tx, "s", 34, w - 170, max_lineas=1)
            _rica(d, M + 106 - 30 * (1 - u), y, ls[0], f, AMARILLO, BLANCO, 255 * u, "l")
        return _salida(im, dt, dur)
    return fn


def carteles(pares, titulo, w=1400, h=None):
    """Lo que dice el texto frente a lo que dice la voz (o dos versiones): filas [(rótulo, frase)], una marca por fila; la última
    fila entra grande en rojo-naranja."""
    n = len(pares)
    h = h or 90 + 110 * n
    fp = ajustar(titulo, "s", 32, w - 120)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 6, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, n, .4, 1.6)
        for i, ((rot, fr), m) in enumerate(zip(pares, mk)):
            if dt < m:
                continue
            u = _reb((dt - m) / .4)
            y = M + 92 + 110 * i
            _txt(d, (M + 60, y), rot, fuente("s", 32), GRIS, "lm", 255 * min(1, u))
            f = ajustar(fr, "s", 56, w - 360)
            if i == n - 1 and n > 1:
                _txt(d, (M + 300, y), fr, f, (255, 110, 84), "lm", 255 * min(1, u), borde=2)
            else:
                letras_oro(im, (M + 300, y), fr, f, 255 * min(1, u), ancla="l")
                d = ImageDraw.Draw(im)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ prueba
def _hoja(fn, dur, marcas, ruta, n=6, fondo=None):
    cols = []
    for k in range(n):
        dt = dur * (k + .5) / n
        a = fn(dt, dur, marcas)
        bg = np.zeros((1080, 1920, 3), np.uint8) + np.array([190, 110, 150], np.uint8) if fondo is None else fondo.copy()
        h, w = a.shape[:2]
        y0, x0 = max(0, (1080 - h) // 2), max(0, (1920 - w) // 2)
        sub = a[:1080, :1920]
        al = sub[..., 3:4] / 255.0
        zona = bg[y0:y0 + sub.shape[0], x0:x0 + sub.shape[1]]
        bg[y0:y0 + sub.shape[0], x0:x0 + sub.shape[1]] = (zona * (1 - al) + sub[..., :3] * al).astype(np.uint8)
        cols.append(Image.fromarray(bg[..., ::-1]).resize((640, 360)))
    hoja = Image.new("RGB", (640 * 3, 360 * ((n + 2) // 3)))
    for i, c in enumerate(cols):
        hoja.paste(c, ((i % 3) * 640, (i // 3) * 360))
    hoja.save(ruta, quality=85)


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["prueba"]:
        os.makedirs("previews", exist_ok=True)
        _hoja(puesto(30, "Dos niveles, una sola canción"), 4.0, [], "previews/sp_puesto.jpg", n=3)
        _hoja(ficha("Brother Harry", "Texto de prueba con *resaltado* en blanco que se escribe letra a letra en la caja del juego.", tipo="Según el documental"),
              6.0, [], "previews/sp_ficha.jpg", n=3)
        _hoja(gemas("Gemas", [(9991, "Prototipo de agosto de 1999"), (10000, "Juego final")]), 5.0, [.3, 2.4], "previews/sp_gemas.jpg", n=3)
        _hoja(linea_tiempo([("1998", "Spyro the Dragon"), ("E3 1999", "Lo enseñan"), ("Nov. 1999", "Sale en EE. UU."), ("2018", "Reignited")]), 7.0,
              [.4, 1.8, 3.2, 4.6], "previews/sp_linea.jpg", n=3)
        _hoja(nombres([("EE. UU.", "Ripto's Rage"), ("Europa", "Gateway to Glimmer"), ("España", "En busca de los talismanes"),
                       ("Japón", "Spyro × Sparx: Tondemo Tours")]), 6.0, [.4, 1.5, 2.6, 3.7], "previews/sp_nombres.jpg", n=3)
        _hoja(codigo([("arriba", 4), ("R1", 4), "cir"], "Modo cabezón", "Cabezas gigantes"), 6.0, [.5, 4.0], "previews/sp_codigo.jpg", n=3)
        _hoja(pilones(), 7.0, [.4, 2.0, 3.0, 4.0, 5.0], "previews/sp_pilones.jpg", n=3)
        _hoja(renombres([("Sparkle", "Glimmer"), ("Colossus Springs", "Idol Springs"), ("Mystic City", "Cloud Temples")]), 6.0, [.4, 1.6, 2.8],
              "previews/sp_renombres.jpg", n=3)
        _hoja(katakana(), 6.0, [.4, 2.6], "previews/sp_katakana.jpg", n=3)
        _hoja(anagrama(), 6.0, [.4, 2.4], "previews/sp_anagrama.jpg", n=3)
        _hoja(rueda("22475", "Las coordenadas del portal", "Su cumpleaños"), 6.0, [.4, 3.2], "previews/sp_rueda.jpg", n=3)
        _hoja(vagoneta(), 6.0, [.3, 3.6], "previews/sp_vagoneta.jpg", n=3)
        _hoja(trueque([("Huevo", None), ("Semilla", None), ("Patito de goma", None), ("Moneda dorada", None)]), 6.0, [.4, 1.5, 2.6, 3.7],
              "previews/sp_trueque.jpg", n=3)
        _hoja(notas([("IGN", 8.8, "8,8"), ("GameSpot", 8.6, "8,6")]), 5.0, [.4, 1.7], "previews/sp_notas.jpg", n=3)
        _hoja(libreta(["Bombas y barriles sin cobrar", "Un *condominio* en Hurricos", "Una casa en Aquaria Towers"], "Las cuentas de Moneybags"), 6.0,
              [.4, 1.4, 2.4], "previews/sp_libreta.jpg", n=3)
        _hoja(carteles([("Texto", "Torch"), ("Voz", "Kill")], "Lo que dice el monje"), 5.0, [.4, 2.2], "previews/sp_carteles.jpg", n=3)
        print("previews/sp_*.jpg")
