# -*- coding: utf-8 -*-
"""MOTION GRAPHICS TRANSLÚCIDOS de la CONSOLA Nintendo 64 (Crónicas del gaming; primer uso `n64_secretos`, 31-oct-2026).
Regla del usuario del 22-oct: fichas translúcidas, con la interfaz de CADA juego. Este video es de TODA la consola, así que la
interfaz es la del hardware: grafito de la carcasa, los cuatro colores del logo, el cartucho gris y letras plateadas de caja.
    import mg_n64 as N
  ficha(titulo, texto, tipo)      grafito translúcido con la tira de 4 colores; el texto se escribe; *x* = amarillo
  puesto(num, titulo, juego)      un cartucho entra con el número en la etiqueta + «SECRETO N.º N» + título + juego
  hud(n, total)                   contador de esquina: cubo que gira + «N/30»
  pegatina(ruta, titulo, tam)     imagen REAL con borde blanco y pestaña
  contador(titulo, pasos)         cifra grande que sube; un paso por marca
  linea_tiempo(hitos, titulo)     cronología; un hito por marca; el último late
  lista(items, titulo)            renglones que entran con su cuadro de color; un renglón por marca
  (los MG propios del guion van más abajo, cada uno con su docstring)
Probar SIEMPRE con una hoja de cuadros antes de `fx` (python nucleo/mg_n64.py prueba).
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import mg_majora as MJ

BLANCO, CREMA, GRIS = (250, 250, 248), (226, 228, 232), (168, 174, 186)
ROJO, VERDE, AZUL, AMARILLO = (226, 38, 48), (0, 170, 82), (40, 104, 226), (250, 200, 24)
LOGO = [ROJO, AMARILLO, VERDE, AZUL]
GRAFITO, CARCASA = (24, 26, 32), (146, 148, 154)
PLATA_CLARA, PLATA, PLATA_OSC = (255, 255, 255), (206, 212, 224), (104, 112, 132)
_eo, _reb, _bgra, _txt, _salida, _rica = MJ._eo, MJ._reb, MJ._bgra, MJ._txt, MJ._salida, MJ._rica
_fc = {}


def fuente(estilo, tam):
    """«t» Arial Black (títulos de caja de los 90), «b» Bahnschrift SemiBold (texto), «c» Bahnschrift condensada (notas)."""
    k = (estilo, int(tam))
    if k not in _fc:
        if estilo == "t":
            _fc[k] = ImageFont.truetype("C:/Windows/Fonts/ariblk.ttf", int(tam))
        else:
            f = ImageFont.truetype("C:/Windows/Fonts/bahnschrift.ttf", int(tam))
            f.set_variation_by_name("SemiBold" if estilo == "b" else "SemiBold Condensed")
            _fc[k] = f
    return _fc[k]


def ajustar(s, estilo, tam, ancho, minimo=14):
    while tam > minimo and MJ._ancho(s, fuente(estilo, tam)) > ancho:
        tam -= 1
    return fuente(estilo, tam)


def caja(s, estilo, tam, ancho, alto=10_000, interlinea=1.28, minimo=16, max_lineas=7):
    while True:
        f = fuente(estilo, tam)
        ls = MJ._partir(s, f, ancho)
        lh = tam * interlinea
        if (len(ls) * lh <= alto and len(ls) <= max_lineas and max(MJ._ancho(x, f) for x in ls) <= ancho) or tam <= minimo:
            return f, ls, lh
        tam -= 1


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
def tira(d, x0, x1, y, g=6, alfa=255):
    """La tira de los cuatro colores del logo, partida en cuatro tramos."""
    a = (x1 - x0) / 4
    if a < 1:                                   # la tira aún no empieza a dibujarse (u ≈ 0)
        return
    for i, c in enumerate(LOGO):
        xa = x0 + a * i
        d.rectangle((xa, y, max(xa, x0 + a * (i + 1) - (2 if i < 3 else 0)), y + g), fill=c + (int(alfa),))


def pizarra(w, h, M=46, alfa=.42, radio=20, colores=True):
    """Grafito translúcido de bordes difuminados, con la tira de colores arriba. Nunca una caja opaca: el video se ve detrás."""
    im = _capa(w + 2 * M, h + 2 * M)
    s = Image.new("L", im.size, 0)
    ImageDraw.Draw(s).rounded_rectangle((M, M + 6, M + w, M + h + 6), radio, fill=110)
    sombra = Image.new("RGBA", im.size, (0, 0, 0, 255))
    sombra.putalpha(s.filter(ImageFilter.GaussianBlur(14)))
    im.alpha_composite(sombra)
    capa = _capa(*im.size)
    ImageDraw.Draw(capa).rounded_rectangle((M, M, M + w, M + h), radio, fill=GRAFITO + (int(255 * alfa),))
    capa.putalpha(capa.getchannel("A").filter(ImageFilter.GaussianBlur(7)))
    im.alpha_composite(capa)
    if colores:
        tira(ImageDraw.Draw(im), M + radio, M + w - radio, M + 1, 5)
    return im, M


def pestana(d, x, y, s, f, alfa=255, color=AMARILLO):
    """Pestaña con el nombre: grafito con un cuadro del color a la izquierda."""
    s = MJ._limpia(s)
    w, h = d.textlength(s, font=f) + 54, f.size * 1.55
    d.rounded_rectangle((x, y - h / 2, x + w, y + h / 2), 6, fill=(14, 15, 20, int(alfa * .88)))
    d.rectangle((x + 12, y - h * .24, x + 12 + h * .48, y + h * .24), fill=color + (int(alfa),))
    _txt(d, (x + 22 + h * .48, y + 1), s, f, BLANCO, "lm", alfa)


def letras_plata(im, xy, s, f, alfa=255, ancla="m", fase=None):
    """Letras plateadas con relieve, como el rótulo de una caja de N64. `fase` = segundos desde la entrada: cada letra cae en su sitio."""
    s = MJ._limpia(s)
    a = int(max(0, min(255, alfa)))
    if a <= 0:
        return
    tot = ImageDraw.Draw(im).textlength(s, font=f)
    alto, pad = int(f.size * 1.5), 14
    cap = _capa(tot + 2 * pad, alto + 2 * pad)
    m = Image.new("L", cap.size, 0)
    dm, dc = ImageDraw.Draw(m), ImageDraw.Draw(cap)
    x, y = pad, pad + alto / 2
    for i, c in enumerate(s):
        w = dm.textlength(c, font=f)
        dy = 0
        if fase is not None:
            u = _reb((fase - i * .03) / .4)
            if u <= .01:
                x += w
                continue
            dy = -20 * (1 - min(1.0, u))
        dc.text((x, y + dy), c, font=f, fill=(8, 9, 14, 255), anchor="lm", stroke_width=max(3, f.size // 16), stroke_fill=(8, 9, 14, 255))
        dm.text((x, y + dy), c, font=f, fill=255, anchor="lm")
        x += w
    grad = np.zeros((cap.height, cap.width, 4), np.uint8)
    for yy in range(cap.height):
        u = max(0.0, min(1.0, (yy - pad) / max(1, alto)))
        p0, p1, k = (PLATA_CLARA, PLATA, u / .5) if u < .5 else (PLATA, PLATA_OSC, (u - .5) / .5)
        grad[yy, :, :3] = [p0[j] + (p1[j] - p0[j]) * k for j in range(3)]
    grad[..., 3] = np.array(m)
    cap.alpha_composite(Image.fromarray(grad, "RGBA"))
    if a < 255:
        cap.putalpha(cap.getchannel("A").point(lambda v: int(v * a / 255)))
    px = int(xy[0] - (tot / 2 if ancla == "m" else (tot if ancla == "r" else 0))) - pad
    im.alpha_composite(cap, (max(0, px), max(0, int(xy[1] - alto / 2) - pad)))


def cubo(tam, ang=0.0, inclina=.48):
    """Cubo de cuatro colores que gira sobre su eje (cuatro caras laterales con los colores del logo). Dibujado, no es el logo."""
    S = int(max(8, tam))
    im = _capa(S * 2, S * 2)
    d = ImageDraw.Draw(im)
    c, R = S, S * .62
    vs = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]

    def rot(p):
        x, y, z = p
        x, z = x * math.cos(ang) - z * math.sin(ang), x * math.sin(ang) + z * math.cos(ang)
        y, z = y * math.cos(inclina) - z * math.sin(inclina), y * math.sin(inclina) + z * math.cos(inclina)
        return x, y, z
    rv = [rot(v) for v in vs]
    caras = [((0, 1, 3, 2), ROJO), ((4, 5, 7, 6), VERDE), ((0, 2, 6, 4), AZUL), ((1, 3, 7, 5), AMARILLO), ((0, 1, 5, 4), (208, 212, 220)), ((2, 3, 7, 6), (70, 74, 84))]
    for idx, col in caras:
        if sum(rv[i][2] for i in idx) < 0:              # cámara en -z: solo las caras que la miran (el cubo es convexo)
            d.polygon([(c + rv[i][0] * R, c + rv[i][1] * R) for i in idx], fill=col + (255,), outline=(10, 10, 14, 255))
    return im.crop(im.getbbox() or (0, 0, 2, 2))


def cartucho(tam, texto=None, color=ROJO, img=None):
    """Cartucho gris de N64 visto de frente: hombros, estrías a los lados y etiqueta. `texto` = cifra grande; `img` = ruta de etiqueta real."""
    W, H = int(tam * .92), int(tam)
    im = _capa(W, H)
    d = ImageDraw.Draw(im)
    d.rounded_rectangle((0, H * .05, W - 1, H - 1), int(W * .06), fill=CARCASA + (255,), outline=(70, 72, 80, 255), width=2)
    d.rounded_rectangle((W * .10, 0, W * .90, H * .16), int(W * .05), fill=(164, 166, 172, 255), outline=(70, 72, 80, 255), width=2)
    for i in range(6):                                  # estrías laterales
        y = H * (.2 + i * .1)
        for x0, x1 in ((W * .03, W * .10), (W * .90, W * .97)):
            d.line([(x0, y), (x1, y)], fill=(104, 106, 114, 255), width=max(2, int(H * .012)))
    x0, y0, x1, y1 = W * .15, H * .13, W * .85, H * .86
    d.rounded_rectangle((x0, y0, x1, y1), 6, fill=color + (255,), outline=(240, 240, 244, 255), width=max(2, int(H * .01)))
    if img:
        fo = Image.open(img).convert("RGB")
        k = max((x1 - x0) / fo.width, (y1 - y0) / fo.height)
        fo = fo.resize((int(fo.width * k) + 1, int(fo.height * k) + 1), Image.LANCZOS).crop((0, 0, int(x1 - x0), int(y1 - y0)))
        im.alpha_composite(fo.convert("RGBA"), (int(x0), int(y0)))
    if texto is not None:
        f = ajustar(str(texto), "t", int(H * .4), (x1 - x0) * .9)
        d.text(((x0 + x1) / 2, (y0 + y1) / 2), str(texto), font=f, fill=(255, 255, 255, 255), anchor="mm",
               stroke_width=max(2, f.size // 14), stroke_fill=(10, 10, 14, 255))
    return im


# ------------------------------------------------------------------ ficha
def ficha(titulo, texto, tipo=None, ancho=900, vel=55):
    """Ficha translúcida: `titulo` en la pestaña, `tipo` en gris (el juego y el año) y el texto que se ESCRIBE letra a letra.
    *x* = amarillo. Al terminar gira un cubo pequeño."""
    in_w = ancho - 2 * 44
    fp = ajustar(titulo, "b", 32, in_w - 70)
    fty = ajustar(tipo, "c", 26, in_w) if tipo else None
    fx, ls, lh = caja(texto, "b", 34, in_w, max_lineas=7)
    h = int(44 + (36 if tipo else 0) + lh * len(ls) + 40)
    base, M = pizarra(ancho, h)
    lien = _capa(base.width, base.height + 34)
    lien.alpha_composite(base, (0, 34))
    letras = [len(x.replace("*", "")) for x in ls]

    def fn(dt, dur, marcas):
        im = lien.copy()
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 32, titulo, fp, 255 * _eo((dt - .1) / .3))
        y = M + 34 + 42
        if tipo:
            _txt(d, (M + 44, y + 6), tipo, fty, GRIS, "lm", 235 * _eo((dt - .3) / .3))
            y += 36
        y += lh / 2
        quedan = max(0.0, (dt - .4) * vel)
        for ln, n in zip(ls, letras):
            _rica(d, M + 44, y, ln, fx, BLANCO, AMARILLO, 255, "l", hasta=quedan)
            quedan -= n
            y += lh
        if quedan > 0:
            g = cubo(30, dt * 2.6)
            im.alpha_composite(g, (int(M + ancho - 40 - g.width / 2), int(M + 34 + h - 34 - g.height / 2)))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ rótulo de secreto
def puesto(num, titulo, juego=None, arriba=None):
    """Banda translúcida: un cartucho con el número en la etiqueta baja y encaja con rebote; «SECRETO N.º N» plateado letra a letra,
    el título debajo y el juego en la pestaña. La etiqueta cambia de color con el número."""
    arriba = arriba or f"Secreto n.º {num}"
    w, h = 1540, 226
    f1 = ajustar(arriba.upper(), "t", 66, w - 420)
    f2 = ajustar(titulo, "b", 44, w - 420)
    fj = ajustar(juego, "c", 28, 520) if juego else None
    car = cartucho(198, num, LOGO[int(num) % 4])

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h, alfa=.46, radio=24)
        d = ImageDraw.Draw(im)
        u = _reb((dt - .05) / .5)
        if u > .02:
            y = M + 16 - (1 - min(1.0, u)) * 150
            c2 = car.copy()
            c2.putalpha(c2.getchannel("A").point(lambda v: int(v * min(1.0, u * 2))))
            im.alpha_composite(c2, (M + 42, max(0, int(y))))
        tx = M + 240 + (w - 240) / 2 - 30
        letras_plata(im, (tx, M + 80), arriba.upper(), f1, 255, fase=dt - .15)
        d = ImageDraw.Draw(im)
        a = _eo((dt - .3) / .5)
        tira(d, tx - 330 * a, tx + 330 * a, M + 134, 4, 255 * a)
        _txt(d, (tx, M + 178), titulo, f2, AMARILLO, "mm", 255 * _eo((dt - .55) / .5))
        if juego:
            pestana(d, M + w - MJ._ancho(juego, fj) - 92, M + 14, juego, fj, 255 * _eo((dt - .7) / .4), LOGO[int(num) % 4])
        return _bgra(im, min(_eo(dt / .3), (dur - dt) / .5))
    return fn


# ------------------------------------------------------------------ pegatina
def pegatina(ruta, titulo=None, tam=360, giro=-5.0):
    """Imagen REAL recortada con borde blanco (mg_tes) con rebote y balanceo; el nombre en una pestaña grafito."""
    import mg_tes as T
    base = T._base_pegatina(ruta, tam)
    if titulo:
        tit = MJ._limpia(titulo)
        f = ajustar(tit, "b", 30, max(260, base.width + 40))
        pw, ph = int(MJ._ancho(tit, f) + 66), 56
        pil = _capa(pw, ph)
        pestana(ImageDraw.Draw(pil), 0, ph / 2, tit, f, 255)
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
    """Contador de esquina: un cubo que gira y las cifras plateadas que caen al entrar."""
    s = f"{n}/{total}"
    f = fuente("t", 42)

    def fn(dt, dur, marcas):
        im = _capa(w, h)
        g = cubo(58, dt * 1.6)
        im.alpha_composite(g, (int(46 - g.width / 2), int(h / 2 - g.height / 2)))
        letras_plata(im, (98, h / 2), s, f, 255, ancla="l", fase=dt)
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .35))
    return fn


def contador(titulo, pasos, w=1160, h=340):
    """Cifra grande que SUBE hasta el valor de cada paso. pasos = [(valor, texto[, «formateado»])]; marca k = paso k."""
    fp = ajustar(titulo, "b", 32, w - 120)
    fn_ = fuente("t", 96)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 8, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, len(pasos), .3, 1.8)
        k = _actual(mk, dt, len(pasos))
        v0 = pasos[k - 1][0] if k else 0
        v1, texto = pasos[k][0], pasos[k][1]
        u = _eo((dt - mk[k]) / 1.1)
        v = v0 + (v1 - v0) * u
        s = pasos[k][2] if len(pasos[k]) > 2 and u >= 1 else f"{int(round(v)):,}".replace(",", " ")
        letras_plata(im, (M + w / 2, M + 136), s, fn_, 255)
        d = ImageDraw.Draw(im)
        _txt(d, (M + w / 2, M + h - 58), texto, ajustar(texto, "b", 34, w - 110), AMARILLO, "mm", 255 * _eo((dt - mk[k] - .3) / .4))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ cronología
def linea_tiempo(hitos, titulo="Así fue", w=1720, h=410):
    """Línea de cuatro colores que se dibuja; marca k = hito k: un cubo cae en su sitio, el año plateado y el texto. El último late."""
    n = len(hitos)
    fp = ajustar(titulo, "b", 32, w - 120)
    fa = fuente("t", 42)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 8, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, n, .4, 1.4)
        x0, x1 = M + 110, M + w - 110
        paso = (x1 - x0) / max(1, n - 1)
        yl = M + 196
        u = _eo((dt - mk[0] + .2) / max(.6, mk[-1] - mk[0] + .4))
        tira(d, x0 - 30, x0 - 30 + (x1 - x0 + 60) * u, yl - 3, 7)
        for i, (ano, txt) in enumerate(hitos):
            r = _reb((dt - mk[i]) / .45)
            if r <= .02:
                continue
            x = x0 + paso * i
            late = 1 + (.12 * math.sin(dt * 6) if i == n - 1 and dt > mk[i] + .5 else 0)
            g = cubo(54 * min(1.1, r) * late, dt * 1.4 + i)
            im.alpha_composite(g, (int(x - g.width / 2), int(yl - g.height / 2)))
            letras_plata(im, (x, yl - 74), ano, fa, 255 * min(1.0, r))
            d = ImageDraw.Draw(im)
            fx, ls, lh = caja(txt, "b", 30, paso * .94 if n > 1 else w * .6, max_lineas=3)
            y = yl + 66
            for ln in ls:
                _txt(d, (x, y), ln, fx, BLANCO, "mm", 255 * _eo((dt - mk[i] - .15) / .3))
                y += lh
        return _salida(im, dt, dur)
    return fn


def lista(items, titulo, w=1160, renglon=74):
    """Lista: cada renglón entra con su cuadro de color. *x* = amarillo. Marca k = renglón k."""
    n = len(items)
    h = 80 + n * renglon + 22
    fp = ajustar(titulo, "b", 32, w - 120)
    fx = ajustar(max((i.replace("*", "") for i in items), key=len), "b", 38, w - 160)

    def fn(dt, dur, marcas):
        im, M = pizarra(w, h)
        d = ImageDraw.Draw(im)
        pestana(d, M + 26, M + 8, titulo, fp, 255 * _eo(dt / .3))
        mk = _marcas(marcas, n, .4, 1.2)
        for i, s in enumerate(items):
            u = _eo((dt - mk[i]) / .35)
            if u <= 0:
                continue
            y = M + 78 + renglon * (i + .5)
            x = M + 44 - 40 * (1 - u)
            d.rectangle((x, y - 15, x + 30, y + 15), fill=LOGO[i % 4] + (int(255 * u),))
            _rica(d, x + 54, y, s, fx, BLANCO, AMARILLO, 255 * u, "l")
        return _salida(im, dt, dur)
    return fn


# ================================================================== MG PROPIOS de n64_secretos (31-oct-2026)
def _base(w, h, titulo, dt):
    im, M = pizarra(w, h)
    d = ImageDraw.Draw(im)
    if titulo:
        pestana(d, M + 26, M + 8, titulo, ajustar(titulo, "b", 32, w - 120), 255 * _eo(dt / .3))
    return im, M, d


def barras(titulo, items, w=1160, renglon=96):
    """Barras horizontales que CRECEN, una por marca, a escala de la mayor. items = [(valor, etiqueta[, «texto del valor»])].
    La barra lleva el color del logo; el valor plateado sigue a la punta."""
    n = len(items)
    h = 76 + n * renglon + 20
    vmax = max(v for v, *_ in items)
    fe = ajustar(max((it[1] for it in items), key=len), "b", 30, 300)
    fv = fuente("t", 40)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, titulo, dt)
        mk = _marcas(marcas, n, .4, 1.4)
        x0, x1 = M + 340, M + w - 190
        for i, it in enumerate(items):
            u = _eo((dt - mk[i]) / 1.0)
            if dt < mk[i] - .05:
                continue
            y = M + 76 + renglon * (i + .5)
            _txt(d, (x0 - 22, y), it[1], fe, BLANCO, "rm", 255 * min(1, u * 3))
            L = (x1 - x0) * it[0] / vmax * u
            d.rounded_rectangle((x0, y - 22, x0 + max(8, L), y + 22), 8, fill=LOGO[i % 4] + (235,))
            s = it[2] if len(it) > 2 and u >= 1 else f"{it[0] * u:,.0f}".replace(",", " ")
            letras_plata(im, (x0 + max(8, L) + 16, y), s, fv, 255 * min(1, u * 3), ancla="l")
            d = ImageDraw.Draw(im)
        return _salida(im, dt, dur)
    return fn


def pantalla4(titulo="Cuatro mandos, cuatro pantallas", w=1000, h=640):
    """Una tele que se parte en cuatro: marca k enciende el cuadrante k (P1..P4) y el puerto k de la consola debajo."""
    fP = fuente("t", 54)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, titulo, dt)
        mk = _marcas(marcas, 4, .5, .7)
        tx0, ty0, tx1, ty1 = M + 150, M + 70, M + w - 150, M + h - 160
        d.rounded_rectangle((tx0 - 16, ty0 - 16, tx1 + 16, ty1 + 16), 26, fill=(12, 13, 18, 230), outline=CARCASA + (255,), width=4)
        cx, cy = (tx0 + tx1) / 2, (ty0 + ty1) / 2
        u = _eo((dt - mk[0] + .3) / .4)
        d.line([(cx, ty0), (cx, ty0 + (ty1 - ty0) * u)], fill=BLANCO + (220,), width=4)
        d.line([(tx0, cy), (tx0 + (tx1 - tx0) * u, cy)], fill=BLANCO + (220,), width=4)
        cuad = [(tx0, ty0, cx, cy), (cx, ty0, tx1, cy), (tx0, cy, cx, ty1), (cx, cy, tx1, ty1)]
        for i, (a0, b0, a1, b1) in enumerate(cuad):
            r = _reb((dt - mk[i]) / .45)
            if r <= .02:
                continue
            d.rectangle((a0 + 6, b0 + 6, a1 - 6, b1 - 6), fill=LOGO[i] + (int(120 * min(1, r)),))
            _txt(d, ((a0 + a1) / 2, (b0 + b1) / 2), f"P{i + 1}", fP, BLANCO, "mm", 255 * min(1, r))
            px = M + 240 + i * (w - 480) / 3
            d.rounded_rectangle((px - 46, ty1 + 52, px + 46, ty1 + 108), 10, fill=(30, 32, 38, 255), outline=LOGO[i] + (255,), width=5)
            d.ellipse((px - 12, ty1 + 68, px + 12, ty1 + 92), fill=LOGO[i] + (255,))
        for i in range(4):
            if dt < mk[i]:
                px = M + 240 + i * (w - 480) / 3
                d.rounded_rectangle((px - 46, ty1 + 52, px + 46, ty1 + 108), 10, fill=(30, 32, 38, 200), outline=(90, 92, 100, 200), width=3)
        return _salida(im, dt, dur)
    return fn


def stick_optico(w=1160, h=560):
    """Cómo funciona el stick: una rueda RANURADA gira, un haz de luz la atraviesa y un sensor CUENTA los cortes (como un ratón de bola).
    Marca 0 = gira y cuenta; marca 1 = al encender, «el centro es 0»; marca 2 = L + R + START lo vuelve a centrar."""
    fs, fc, fb = fuente("t", 64), fuente("b", 30), fuente("t", 34)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, "Dentro del stick", dt)
        mk = _marcas(marcas, 3, .4, 2.5)
        cx, cy, R = M + 300, M + 280, 170
        ang = dt * 2.2 if dt < mk[1] or dt > mk[2] + 1.2 else 0
        d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(60, 62, 70, 230), outline=PLATA + (255,), width=5)
        for k in range(24):
            a = ang + k * math.tau / 24
            xa, ya = cx + math.cos(a) * (R - 34), cy + math.sin(a) * (R - 34)
            d.ellipse((xa - 11, ya - 11, xa + 11, ya + 11), fill=(10, 10, 14, 255))
        d.ellipse((cx - 36, cy - 36, cx + 36, cy + 36), fill=CARCASA + (255,))
        luz = any(abs(((ang + k * math.tau / 24) % math.tau) - math.pi * 1.5) < .09 for k in range(24))
        d.rectangle((cx - 24, cy - R - 70, cx + 24, cy - R - 40), fill=(80, 80, 90, 255))
        d.line([(cx, cy - R - 40), (cx, cy - R + 60)], fill=AMARILLO + (255 if luz else 70,), width=10)
        d.rectangle((cx - 24, cy - R + 60, cx + 24, cy - R + 84), fill=(VERDE if luz else (60, 60, 66)) + (255,))
        _txt(d, (cx + 40, cy - R - 55), "LED", fc, GRIS, "lm", 230)
        _txt(d, (cx + 40, cy - R + 72), "sensor", fc, GRIS, "lm", 230)
        n = int(dt * 2.2 * 24 / math.tau) if dt < mk[1] else 0
        if dt > mk[2] + 1.2:
            n = int((dt - mk[2] - 1.2) * 2.2 * 24 / math.tau)
        tx = M + 760
        _txt(d, (tx, M + 110), "Cortes contados", fc, GRIS, "mm", 235)
        letras_plata(im, (tx, M + 190), str(n), fs, 255)
        d = ImageDraw.Draw(im)
        if dt >= mk[1]:
            _rica(d, tx - 210, M + 290, "Al encender: *aquí = centro*", fc, BLANCO, AMARILLO, 255 * _eo((dt - mk[1]) / .4), "l")
        if dt >= mk[2]:
            for i, b in enumerate(("L", "R", "START")):
                r = _reb((dt - mk[2] - i * .25) / .4)
                if r > .02:
                    bw = 74 if b != "START" else 150
                    bx = tx - 230 + [0, 110, 220][i]
                    d.rounded_rectangle((bx, M + 360, bx + bw, M + 360 + 64 * min(1, r)), 14, fill=[GRIS, GRIS, ROJO][i] + (255,))
                    _txt(d, (bx + bw / 2, M + 392), b, fb, GRAFITO if i < 2 else BLANCO, "mm", 255 * min(1, r))
            _txt(d, (tx, M + 470), "= vuelve a centrar", fc, AMARILLO, "mm", 255 * _eo((dt - mk[2] - .8) / .4))
        return _salida(im, dt, dur)
    return fn


def bits(w=1000, h=560):
    """64 casillas que se encienden («64 bits»); marca 1 = la mitad se APAGA (lo que se usaba: 32); marca 2 = palanca en «2.ª»."""
    f, fc, fg = fuente("t", 46), fuente("b", 32), fuente("t", 70)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, "El procesador", dt)
        mk = _marcas(marcas, 3, .3, 2.2)
        lado, gx, gy = 40, M + 70, M + 110
        for i in range(64):
            r, c = divmod(i, 8)
            u = _eo((dt - mk[0] - i * .018) / .2)
            if u <= 0:
                continue
            apag = dt > mk[1] + c * .06 and c >= 4
            col = (70, 72, 80) if apag else LOGO[(r + c) % 4]
            x, y = gx + c * (lado + 8), gy + r * (lado + 8)
            d.rectangle((x, y, x + lado, y + lado), fill=col + (int(235 * u),))
        txt = "32" if dt > mk[1] + .5 else "64"
        letras_plata(im, (M + 720, M + 190), txt + " bits", f, 255)
        d = ImageDraw.Draw(im)
        if dt > mk[1]:
            _txt(d, (M + 720, M + 260), "lo que de verdad se usaba", fc, AMARILLO, "mm", 255 * _eo((dt - mk[1]) / .4))
        if dt > mk[2]:
            r = _reb((dt - mk[2]) / .5)
            cx, cy = M + 720, M + 400
            d.ellipse((cx - 60 * r, cy - 60 * r, cx + 60 * r, cy + 60 * r), fill=(14, 15, 20, 240), outline=PLATA + (255,), width=4)
            _txt(d, (cx, cy + 2), "2.ª", fg if r > .9 else fuente("t", max(10, int(70 * r))), BLANCO, "mm", 255)
        return _salida(im, dt, dur)
    return fn


def textura(w=1160, h=560):
    """La memoria de texturas: un bloque de 4 KB (barra) con una textura nítida; marca 1 = con filtrado se queda en 2 KB;
    marca 2 = la textura se ESTIRA sobre un muro y se emborrona («vaselina»)."""
    rng = np.random.default_rng(64)
    tex = np.zeros((16, 16, 3), np.uint8)
    for y in range(16):
        for x in range(16):
            b = ((x + (y // 4 % 2) * 4) % 8 == 0) or y % 4 == 0
            tex[y, x] = (96, 64, 52) if b else (178 + rng.integers(-20, 20), 96 + rng.integers(-14, 14), 70)
    nitida = Image.fromarray(tex).resize((300, 300), Image.NEAREST).convert("RGBA")
    borrosa = Image.fromarray(tex).resize((40, 40), Image.BILINEAR).resize((520, 300), Image.BICUBIC).filter(ImageFilter.GaussianBlur(5)).convert("RGBA")
    fc, fv = fuente("b", 32), fuente("t", 48)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, "Memoria para texturas", dt)
        mk = _marcas(marcas, 3, .3, 2.4)
        bx0, bx1, by = M + 60, M + w - 60, M + 90
        k = 1 - .5 * _eo((dt - mk[1]) / .8) if dt > mk[1] else 1
        d.rounded_rectangle((bx0, by, bx1, by + 40), 8, outline=PLATA + (255,), width=3)
        d.rounded_rectangle((bx0 + 4, by + 4, bx0 + 4 + (bx1 - bx0 - 8) * k * _eo((dt - mk[0]) / .6), by + 36), 6, fill=AMARILLO + (230,))
        letras_plata(im, (bx1 - 10, by + 80), "4 KB" if k > .99 else "2 KB con filtrado", fv, 255, ancla="r")
        d = ImageDraw.Draw(im)
        if dt < mk[2]:
            im.alpha_composite(nitida, (int(M + 80), int(M + 180)))
            _txt(d, (M + 420, M + 330), "Una textura de 16 × 16", fc, BLANCO, "lm", 240)
        else:
            u = _eo((dt - mk[2]) / .7)
            t = nitida.resize((int(300 + 220 * u), 300), Image.NEAREST)
            t = Image.blend(t, borrosa.resize(t.size), u)
            im.alpha_composite(t, (int(M + 80), int(M + 180)))
            _rica(d, M + 640, M + 330, "Estirada: *vaselina*", fc, BLANCO, AMARILLO, 255 * u, "l")
        return _salida(im, dt, dur)
    return fn


def posicion(w=560, h=420):
    """El indicador de posición de Mario Kart: el puesto salta 1.º, 4.º, 2.º… y se queda en «?» (marca 1)."""
    f, fq, fc = fuente("t", 150), fuente("t", 210), fuente("b", 30)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, "Tu posición", dt)
        mk = _marcas(marcas, 1, 1.6)
        if dt < mk[0]:
            s = ["1.º", "4.º", "2.º", "7.º", "3.º", "5.º"][int(dt * 6) % 6]
            letras_plata(im, (M + w / 2, M + h / 2 + 10), s, f, 255)
        else:
            r = _reb((dt - mk[0]) / .5)
            letras_plata(im, (M + w / 2, M + h / 2 + 10 - 30 * (1 - min(1, r))), "?", fq, 255)
            d = ImageDraw.Draw(im)
            _txt(d, (M + w / 2, M + h - 34), "Hasta cruzar la meta", fc, AMARILLO, "mm", 255 * _eo((dt - mk[0] - .4) / .4))
        return _salida(im, dt, dur)
    return fn


def velocidad(niveles, titulo="Velocidad de juego", w=1000, h=520):
    """Un velocímetro: marca k = nivel k (aguja y «×N»). niveles = [(multiplicador, texto, ruta_imagen|None)]."""
    n = len(niveles)
    fx, fc = fuente("t", 92), fuente("b", 32)
    fotos = [Image.open(p).convert("RGBA") if p else None for *_, p in niveles]
    fotos = [f.resize((int(f.width * 210 / max(f.size)), int(f.height * 210 / max(f.size))), Image.LANCZOS) if f else None for f in fotos]

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, titulo, dt)
        mk = _marcas(marcas, n, .4, 1.8)
        k = _actual(mk, dt, n)
        v0 = niveles[k - 1][0] if k else 0
        v = v0 + (niveles[k][0] - v0) * _reb((dt - mk[k]) / .7)
        cx, cy, R = M + 300, M + 370, 220
        for i in range(31):
            a = math.pi + math.pi * i / 30
            r0 = R - (26 if i % 10 == 0 else 12)
            d.line([(cx + math.cos(a) * r0, cy + math.sin(a) * r0), (cx + math.cos(a) * R, cy + math.sin(a) * R)], fill=PLATA + (255,), width=4)
        d.arc((cx - R, cy - R, cx + R, cy + R), 180, 360, fill=PLATA + (200,), width=3)
        a = math.pi + math.pi * min(3, v) / 3
        d.line([(cx, cy), (cx + math.cos(a) * (R - 30), cy + math.sin(a) * (R - 30))], fill=ROJO + (255,), width=9)
        d.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill=BLANCO + (255,))
        letras_plata(im, (M + 720, M + 170), f"×{niveles[k][0]:g}", fx, 255)
        d = ImageDraw.Draw(im)
        _txt(d, (M + 720, M + 260), niveles[k][1], ajustar(niveles[k][1], "b", 34, 380), AMARILLO, "mm", 255 * _eo((dt - mk[k]) / .4))
        if fotos[k] is not None:
            s = min(1.0, _reb((dt - mk[k]) / .45))
            if s > .05:
                f2 = fotos[k].resize((max(2, int(fotos[k].width * s)), max(2, int(fotos[k].height * s))))
                im.alpha_composite(f2, (int(M + 720 - f2.width / 2), int(M + 300)))
        return _salida(im, dt, dur)
    return fn


def tachones(pasos, titulo, w=900, renglon=86):
    """Lo que iba a ser y lo que fue: cada marca añade un renglón y TACHA el anterior; el último queda en amarillo con el cubo."""
    n = len(pasos)
    h = 76 + n * renglon + 24
    f = ajustar(max(pasos, key=len), "b", 40, w - 160)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, titulo, dt)
        mk = _marcas(marcas, n, .4, 1.4)
        for i, s in enumerate(pasos):
            u = _eo((dt - mk[i]) / .35)
            if u <= 0:
                continue
            y = M + 76 + renglon * (i + .5)
            ult = i == n - 1
            _txt(d, (M + 90, y), s, f, AMARILLO if ult else BLANCO, "lm", 255 * u * (1 if ult or dt < (mk[i + 1] if i + 1 < n else 1e9) else .55))
            if not ult and i + 1 < n and dt > mk[i + 1]:
                t = _eo((dt - mk[i + 1]) / .3)
                d.line([(M + 80, y + 2), (M + 80 + (MJ._ancho(s, f) + 30) * t, y + 2)], fill=ROJO + (255,), width=6)
            if ult:
                g = cubo(34, dt * 2.4)
                im.alpha_composite(g, (int(M + 44 - g.width / 2), int(y - g.height / 2)))
            else:
                d.rectangle((M + 34, y - 12, M + 58, y + 12), fill=LOGO[i % 4] + (int(255 * u),))
        return _salida(im, dt, dur)
    return fn


def mito(dicen, verdad, titulo="Lo que se cuenta", w=1100):
    """«SE DICE» (marca 0) con una X roja que lo sella (marca 1) y «LA VERDAD» con ✓ verde (marca 2)."""
    f1, ls1, lh1 = caja(dicen, "b", 36, w - 260, max_lineas=3)
    f2, ls2, lh2 = caja(verdad, "b", 36, w - 260, max_lineas=3)
    h = int(70 + 50 + lh1 * len(ls1) + 40 + 50 + lh2 * len(ls2) + 30)
    fe, fx = fuente("t", 30), fuente("t", 120)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, titulo, dt)
        mk = _marcas(marcas, 3, .3, 1.8)
        y = M + 76
        _txt(d, (M + 50, y + 18), "SE DICE", fe, GRIS, "lm", 255 * _eo((dt - mk[0]) / .3))
        y += 50
        for ln in ls1:
            _rica(d, M + 50, y + lh1 / 2, ln, f1, BLANCO, AMARILLO, 255 * _eo((dt - mk[0]) / .4), "l")
            y += lh1
        if dt > mk[1]:                                      # la fuente no trae ✗ ni ✓: se dibujan
            r = min(1.2, _reb((dt - mk[1]) / .4)) * 44
            cx, cy = M + w - 110, M + 76 + 50 + lh1 * len(ls1) / 2
            d.line([(cx - r, cy - r), (cx + r, cy + r)], fill=ROJO + (255,), width=16)
            d.line([(cx - r, cy + r), (cx + r, cy - r)], fill=ROJO + (255,), width=16)
        y += 40
        if dt > mk[2]:
            u = _eo((dt - mk[2]) / .4)
            _txt(d, (M + 50, y + 18), "LA VERDAD", fe, VERDE, "lm", 255 * u)
            yy = y + 50
            for ln in ls2:
                _rica(d, M + 50, yy + lh2 / 2, ln, f2, BLANCO, AMARILLO, 255 * u, "l")
                yy += lh2
            r = min(1.2, _reb((dt - mk[2] - .3) / .4)) * 44
            if r > 1:
                cx, cy = M + w - 110, y + 50 + lh2 * len(ls2) / 2
                d.line([(cx - r, cy), (cx - r * .25, cy + r * .7), (cx + r, cy - r * .8)], fill=VERDE + (255,), width=16, joint="curve")
        return _salida(im, dt, dur)
    return fn


def factura(lineas, total, titulo="Cargo a la habitación", w=640):
    """Ticket de hotel que se IMPRIME renglón a renglón (uno por marca) y el total al final con un sello. lineas = [(concepto, importe)]."""
    n = len(lineas)
    h = 120 + n * 64 + 230
    fl, ft, fs = fuente("c", 32), fuente("t", 40), fuente("t", 46)

    def fn(dt, dur, marcas):
        im = _capa(w + 60, h + 60)
        mk = _marcas(marcas, n + 1, .4, 1.0)
        alto = min(h, 120 + 64 * sum(dt > m for m in mk[:n]) + (230 if dt > mk[n] else 0))
        d = ImageDraw.Draw(im)
        d.rectangle((30, 30, 30 + w, 30 + alto), fill=(246, 244, 236, 228))
        for x in range(30, 30 + w, 24):                     # borde dentado abajo
            d.polygon([(x, 30 + alto), (x + 12, 30 + alto + 12), (x + 24, 30 + alto)], fill=(246, 244, 236, 228))
        _txt(d, (30 + w / 2, 80), titulo.upper(), ajustar(titulo.upper(), "t", 34, w - 60), GRAFITO, "mm", 255)
        tira(d, 60, 30 + w - 30, 110, 4)
        for i, (c, v) in enumerate(lineas):
            if dt > mk[i]:
                y = 160 + i * 64
                _txt(d, (60, y), c, fl, GRAFITO, "lm", 255)
                _txt(d, (w, y), v, fl, GRAFITO, "rm", 255)
        if dt > mk[n]:
            y = 160 + n * 64 + 30
            d.line([(60, y - 34), (w, y - 34)], fill=GRAFITO + (255,), width=2)
            _txt(d, (60, y), "TOTAL", ft, GRAFITO, "lm", 255)
            _txt(d, (w, y), total, ft, ROJO, "rm", 255)
            r = _reb((dt - mk[n] - .4) / .4)
            if r > .02:
                sello = _capa(360, 120)
                ds = ImageDraw.Draw(sello)
                ds.rounded_rectangle((6, 6, 354, 114), 12, outline=ROJO + (220,), width=6)
                _txt(ds, (180, 60), "¿REUNIÓN?", fs, ROJO, "mm", 220)
                sello = sello.rotate(-14, expand=True, resample=Image.BICUBIC)
                sello = sello.resize((max(2, int(sello.width * min(1.2, r))), max(2, int(sello.height * min(1.2, r)))))
                im.alpha_composite(sello, (int(30 + w / 2 - sello.width / 2), int(y + 110 - sello.height / 2)))
        return _salida(im, dt, dur)
    return fn


def dos_versiones(titulo, a, b, w=1400, h=440):
    """Dos versiones de la misma historia: a = (quién, qué dice) entra en la marca 0, b en la marca 1, y en la 2 cae «SIN CERRAR»."""
    fn_, fsel = fuente("t", 40), fuente("t", 42)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, titulo, dt)
        mk = _marcas(marcas, 3, .4, 2.0)
        col = (w - 200) / 2
        for i, (quien, que) in enumerate((a, b)):
            u = _eo((dt - mk[i]) / .45)
            if u <= 0:
                continue
            x = M + 60 + i * (col + 80) + (1 - u) * (-60 if i == 0 else 60)
            d.rectangle((x, M + 84, x + 10, M + h - 40), fill=LOGO[i * 2] + (int(255 * u),))
            _txt(d, (x + 34, M + 112), quien, ajustar(quien, "t", 40, col - 40), AMARILLO, "lm", 255 * u)
            fx, ls, lh = caja(que, "b", 34, col - 50, alto=h - 200, max_lineas=6)
            y = M + 176
            for ln in ls:
                _rica(d, x + 34, y, ln, fx, BLANCO, AMARILLO, 255 * u, "l")
                y += lh
        if dt > mk[1]:
            g = cubo(56, dt * 2)
            im.alpha_composite(g, (int(M + w / 2 - g.width / 2), int(M + h / 2 - g.height / 2)))
        if dt > mk[2]:
            r = _reb((dt - mk[2]) / .45)
            s = _capa(440, 110)
            ds = ImageDraw.Draw(s)
            ds.rounded_rectangle((6, 6, 434, 104), 12, fill=(14, 15, 20, 200), outline=AMARILLO + (255,), width=5)
            _txt(ds, (220, 56), "SIN CERRAR", fsel, AMARILLO, "mm", 255)
            s = s.rotate(6, expand=True, resample=Image.BICUBIC)
            s = s.resize((max(2, int(s.width * min(1.15, r))), max(2, int(s.height * min(1.15, r)))))
            im.alpha_composite(s, (int(M + w / 2 - s.width / 2), int(M + h - 40 - s.height)))
        return _salida(im, dt, dur)
    return fn


def cadena(eslabones, titulo, w=1600, h=470):
    """Cómo una cosa llevó a otra: nodos redondos con su imagen REAL (o el cubo) unidos por la tira de colores; uno por marca.
    eslabones = [(texto, año|None, ruta|None)]; el último late."""
    n = len(eslabones)
    D = 190
    imgs = []
    for _, _, ruta in eslabones:
        if ruta:
            fo = Image.open(ruta).convert("RGBA")
            lado = min(fo.size)
            fo = fo.crop(((fo.width - lado) // 2, (fo.height - lado) // 2, (fo.width + lado) // 2, (fo.height + lado) // 2)).resize((D, D), Image.LANCZOS)
            m = Image.new("L", (D, D), 0)
            ImageDraw.Draw(m).ellipse((0, 0, D - 1, D - 1), fill=255)
            fo.putalpha(Image.fromarray(np.minimum(np.array(fo.getchannel("A")), np.array(m))))
            imgs.append(fo)
        else:
            imgs.append(None)
    fa = fuente("t", 34)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, titulo, dt)
        mk = _marcas(marcas, n, .4, 1.6)
        x0, x1, y = M + 150, M + w - 150, M + 210
        paso = (x1 - x0) / max(1, n - 1)
        for i, (txt, ano, _) in enumerate(eslabones):
            r = _reb((dt - mk[i]) / .45)
            if r <= .02:
                continue
            x = x0 + paso * i
            if i:
                u = _eo((dt - mk[i]) / .4)
                tira(d, x - paso + D / 2 + 10, x - paso + D / 2 + 10 + (paso - D - 20) * u, y - 3, 7)
            late = 1 + (.06 * math.sin(dt * 6) if i == n - 1 and dt > mk[i] + .5 else 0)
            s = min(1.0, r) * late
            dd = int(D * s)
            d.ellipse((x - dd / 2 - 7, y - dd / 2 - 7, x + dd / 2 + 7, y + dd / 2 + 7), fill=LOGO[i % 4] + (255,))
            if imgs[i] is not None:
                ii = imgs[i].resize((max(2, dd), max(2, dd)))
                im.alpha_composite(ii, (int(x - dd / 2), int(y - dd / 2)))
            else:
                d.ellipse((x - dd / 2, y - dd / 2, x + dd / 2, y + dd / 2), fill=GRAFITO + (255,))
                g = cubo(dd * .3, dt * 1.6)
                im.alpha_composite(g, (int(x - g.width / 2), int(y - g.height / 2)))
            d = ImageDraw.Draw(im)
            if ano:
                letras_plata(im, (x, y - D / 2 - 40), ano, fa, 255 * min(1, r))
                d = ImageDraw.Draw(im)
            fx, ls, lh = caja(txt, "b", 32, paso * .92 if n > 1 else 500, max_lineas=2)
            yy = y + D / 2 + 40
            for ln in ls:
                _txt(d, (x, yy), ln, fx, BLANCO, "mm", 255 * _eo((dt - mk[i] - .15) / .3))
                yy += lh
        return _salida(im, dt, dur)
    return fn


def pulso(w=1160, h=540):
    """Bio Tetris: electrocardiograma que corre, pulsaciones plateadas y piezas que caen; marca 1 = el pulso SUBE (más piezas, en rojo);
    marca 2 = el pulso baja («demasiado tranquilo») y también castiga."""
    fb, fc = fuente("t", 80), fuente("b", 32)
    piezas = [((0, 0), (1, 0), (2, 0), (3, 0)), ((0, 0), (1, 0), (0, 1), (1, 1)), ((0, 0), (1, 0), (2, 0), (1, 1)), ((0, 0), (0, 1), (1, 1), (2, 1))]

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, "Bio Tetris", dt)
        mk = _marcas(marcas, 3, .3, 2.6)
        if dt < mk[1]:
            bpm = 72
        elif dt < mk[2]:
            bpm = 72 + 46 * _eo((dt - mk[1]) / 1.2)
        else:
            bpm = 118 - 64 * _eo((dt - mk[2]) / 1.2)
        alerta = bpm > 100 or bpm < 60
        x0, x1, yb = M + 40, M + 640, M + 300
        T = 60 / bpm
        pts = []
        for px in range(int(x0), int(x1), 4):
            t = dt - (x1 - px) / 300
            f = (t % T) / T
            v = 0
            if .30 < f < .34:
                v = -110 * math.sin((f - .30) / .04 * math.pi)
            elif .34 < f < .37:
                v = 40 * math.sin((f - .34) / .03 * math.pi)
            pts.append((px, yb + v))
        d.line(pts, fill=(ROJO if alerta else VERDE) + (255,), width=5, joint="curve")
        letras_plata(im, (M + 340, M + 440), f"{int(bpm)} ppm", fb, 255)
        d = ImageDraw.Draw(im)
        gx0, gw, cel = M + 760, 300, 30
        d.rectangle((gx0, M + 80, gx0 + gw, M + h - 30), outline=PLATA + (200,), width=3)
        vel = 120 + 4 * (bpm - 72) if bpm >= 72 else 120 + 5 * (72 - bpm)
        for k in range(5):
            fase = (dt * vel / 100 + k * .37) % 1
            y = M + 80 + fase * (h - 140)
            pz = piezas[(k + int(dt * vel / 100 + k * .37)) % 4]
            x = gx0 + 20 + (k * 53) % (gw - 120)
            col = ROJO if alerta and k % 2 == 0 else LOGO[k % 4]
            for cx, cy in pz:
                d.rectangle((x + cx * cel, y + cy * cel, x + cx * cel + cel - 3, y + cy * cel + cel - 3), fill=col + (235,))
        if dt > mk[2]:
            _txt(d, (M + 340, M + 120), "Demasiado tranquilo: castigo", fc, AMARILLO, "mm", 255 * _eo((dt - mk[2] - .6) / .4))
        elif dt > mk[1]:
            _txt(d, (M + 340, M + 120), "Pulso alto: piezas difíciles", fc, AMARILLO, "mm", 255 * _eo((dt - mk[1] - .6) / .4))
        return _salida(im, dt, dur)
    return fn


def progreso(pct, titulo, sello="CANCELADO", w=1160, h=330):
    """Barra de desarrollo que se llena hasta `pct` (marca 0) y se queda ahí; en la marca 1 cae el sello."""
    fv, fs = fuente("t", 64), fuente("t", 74)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, titulo, dt)
        mk = _marcas(marcas, 2, .3, 2.6)
        u = _eo((dt - mk[0]) / 1.8)
        x0, x1, y = M + 60, M + w - 60, M + 170
        d.rounded_rectangle((x0, y - 34, x1, y + 34), 12, outline=PLATA + (255,), width=4)
        L = (x1 - x0 - 12) * pct / 100 * u
        for i in range(4):
            d.rectangle((x0 + 6 + L * i / 4, y - 28, x0 + 6 + L * (i + 1) / 4, y + 28), fill=LOGO[i] + (235,))
        letras_plata(im, (x0 + 6 + L + 70, y + 84), f"{int(round(pct * u))} %", fv, 255)
        if dt > mk[1]:
            r = _reb((dt - mk[1]) / .45)
            s = _capa(620, 150)
            ds = ImageDraw.Draw(s)
            ds.rounded_rectangle((8, 8, 612, 142), 16, outline=ROJO + (235,), width=9)
            _txt(ds, (310, 76), sello, fs, ROJO, "mm", 235)
            s = s.rotate(-9, expand=True, resample=Image.BICUBIC)
            k = 1 + 1.2 * (1 - min(1, r))
            s = s.resize((max(2, int(s.width * k)), max(2, int(s.height * k))))
            s.putalpha(s.getchannel("A").point(lambda v: int(v * min(1, r * 2))))
            im.alpha_composite(s, (int(M + w / 2 - s.width / 2), int(y - s.height / 2)))
        return _salida(im, dt, dur)
    return fn


def postits(notas, titulo="Ideas en secreto", w=1300, h=520):
    """Notas Post-it de los cuatro colores que se PEGAN de golpe en la pizarra, una por marca, cada una con su giro."""
    f = fuente("c", 34)
    n = len(notas)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, titulo, dt)
        mk = _marcas(marcas, n, .3, .9)
        for i, s in enumerate(notas):
            r = _reb((dt - mk[i]) / .35)
            if r <= .02:
                continue
            lado = 250
            nota = _capa(lado + 20, lado + 20)
            dn = ImageDraw.Draw(nota)
            dn.rectangle((14, 16, lado + 14, lado + 16), fill=(0, 0, 0, 90))
            dn.rectangle((8, 8, lado + 8, lado + 8), fill=[(255, 236, 110), (255, 160, 190), (150, 230, 160), (140, 200, 255)][i % 4] + (250,))
            fx, ls, lh = caja(s, "c", 36, lado - 40, alto=lado - 40, max_lineas=5)
            y = 8 + lado / 2 - lh * (len(ls) - 1) / 2
            for ln in ls:
                _txt(dn, (8 + lado / 2, y), ln, fx, GRAFITO, "mm", 255)
                y += lh
            k = 1 + .5 * (1 - min(1, r))
            nota = nota.rotate([-7, 5, -3, 8, -6][i % 5], expand=True, resample=Image.BICUBIC)
            nota = nota.resize((max(2, int(nota.width * k)), max(2, int(nota.height * k))))
            cx = M + 70 + (w - 140) * (i + .5) / n
            cy = M + 90 + (h - 120) / 2 + (-22 if i % 2 else 22)
            im.alpha_composite(nota, (int(cx - nota.width / 2), int(cy - nota.height / 2)))
        return _salida(im, dt, dur)
    return fn


def sin_cara(fotos, titulo="El prototipo", w=1500, h=520, revela=True):
    """Cuatro muñecos grises SIN CARA (marca 0); desde la marca 1, cada uno se convierte en la imagen REAL del personaje (una por marca).
    fotos = [(ruta, nombre)] (4). `revela=False` = solo los muñecos (para el gancho)."""
    D = 230
    reales = []
    for ruta, _ in fotos:
        fo = Image.open(ruta).convert("RGBA")
        fo.thumbnail((D, int(D * 1.35)), Image.LANCZOS)
        reales.append(fo)
    fn_ = fuente("b", 32)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, titulo, dt)
        mk = _marcas(marcas, 5, .3, 1.0)
        for i in range(4):
            cx, base_y = M + 140 + (w - 280) * i / 3, M + h - 70
            u = _eo((dt - mk[0] - i * .12) / .35)
            t = _eo((dt - mk[i + 1]) / .45) if revela and dt > mk[i + 1] else 0
            if u > 0 and t < 1:
                a = int(235 * u * (1 - t))
                d.ellipse((cx - 50, base_y - 330, cx + 50, base_y - 230), fill=(176, 180, 190, a))
                d.rounded_rectangle((cx - 70, base_y - 220, cx + 70, base_y - 40), 30, fill=(150, 154, 164, a))
                d.rectangle((cx - 60, base_y - 40, cx - 18, base_y), fill=(150, 154, 164, a))
                d.rectangle((cx + 18, base_y - 40, cx + 60, base_y), fill=(150, 154, 164, a))
            if t > 0:
                r = reales[i].copy()
                r.putalpha(r.getchannel("A").point(lambda v: int(v * t)))
                im.alpha_composite(r, (int(cx - r.width / 2), int(base_y - r.height)))
                d = ImageDraw.Draw(im)
                pestana(d, cx - MJ._ancho(fotos[i][1], fn_) / 2 - 40, base_y + 26, fotos[i][1], fn_, 255 * t, LOGO[i])
        return _salida(im, dt, dur)
    return fn


def cita(lineas, autor, w=1500):
    """Una cita en renglones que entran uno por marca (*x* = amarillo); el autor en la pestaña y comillas plateadas grandes."""
    fx = ajustar(max((s.replace("*", "") for s in lineas), key=len), "b", 52, w - 260)
    n = len(lineas)
    h = 90 + n * 92 + 40
    fq = fuente("t", 150)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, autor, dt)
        mk = _marcas(marcas, n, .4, 1.8)
        letras_plata(im, (M + 70, M + 120), "“", fq, 255 * _eo(dt / .4))
        d = ImageDraw.Draw(im)
        for i, s in enumerate(lineas):
            u = _eo((dt - mk[i]) / .5)
            if u > 0:
                _rica(d, M + 150 + 20 * (1 - u), M + 110 + 92 * i, s, fx, BLANCO, AMARILLO, 255 * u, "l")
        return _salida(im, dt, dur)
    return fn


def calor(w=1100, h=500):
    """Mario Party: un stick que gira cada vez más rápido y un termómetro que sube (marca 0); marca 1 = «AMPOLLAS»; marca 2 = 90 quejas;
    marca 3 = guantes, hasta 4 por familia."""
    fv, fc, fs = fuente("t", 64), fuente("b", 32), fuente("t", 52)

    def fn(dt, dur, marcas):
        im, M, d = _base(w, h, "Girar el stick con la palma", dt)
        mk = _marcas(marcas, 4, .3, 1.8)
        cx, cy, R = M + 220, M + 270, 130
        vel = 2 + 10 * min(1, max(0, dt - mk[0]) / 2.5)
        a = dt * vel
        d.ellipse((cx - R, cy - R, cx + R, cy + R), outline=PLATA + (200,), width=4)
        d.ellipse((cx - 60, cy - 60, cx + 60, cy + 60), fill=(60, 62, 70, 255), outline=(20, 20, 24, 255), width=3)
        kx, ky = cx + math.cos(a) * 70, cy + math.sin(a) * 70
        d.ellipse((kx - 40, ky - 40, kx + 40, ky + 40), fill=GRIS + (255,), outline=(30, 30, 36, 255), width=3)
        for k in range(1, 6):
            aa = a - k * .28
            d.arc((cx - R + 14, cy - R + 14, cx + R - 14, cy + R - 14), math.degrees(aa) - 6, math.degrees(aa) + 6, fill=ROJO + (int(220 - k * 36),), width=8)
        tx, ty0, ty1 = M + 470, M + 90, M + h - 60
        q = min(1, max(0, dt - mk[0]) / 3.0)
        d.rounded_rectangle((tx, ty0, tx + 50, ty1), 24, outline=PLATA + (255,), width=4)
        yq = min(ty1 - 44, ty1 - (ty1 - ty0 - 20) * q)          # nunca más bajo que el radio: con q≈0 PIL exige y1 >= y0
        col = tuple(int(VERDE[j] + (ROJO[j] - VERDE[j]) * q) for j in range(3))
        d.rounded_rectangle((tx + 8, yq, tx + 42, ty1 - 8), 18, fill=col + (255,))
        x2 = M + 800
        if dt > mk[1]:
            r = _reb((dt - mk[1]) / .4)
            _txt(d, (x2, M + 130), "¡AMPOLLAS!", fuente("t", max(10, int(52 * min(1.15, r)))), ROJO, "mm", 255)
        if dt > mk[2]:
            u = _eo((dt - mk[2]) / 1.0)
            letras_plata(im, (x2, M + 250), f"{int(90 * u)} quejas", fv, 255)
            d = ImageDraw.Draw(im)
        if dt > mk[3]:
            _rica(d, x2 - 230, M + 370, "*Guantes*: hasta 4 por familia", fc, BLANCO, AMARILLO, 255 * _eo((dt - mk[3]) / .4), "l")
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ prueba
def _hoja(fn, dur, marcas, ruta, n=6, fondo=None):
    W, H = 640, 360
    hoja = Image.new("RGB", (W * 3, H * ((n + 2) // 3)), (40, 40, 40))
    for i in range(n):
        dt = dur * (i + .7) / n
        c = Image.new("RGB", (1920, 1080), (70, 96, 120)) if fondo is None else fondo.copy()
        a = fn(dt, dur, marcas)
        if a.shape[0] > 2:
            g = Image.fromarray(a[..., [2, 1, 0, 3]], "RGBA")
            c.paste(g, ((1920 - g.width) // 2, (1080 - g.height) // 2), g)
        hoja.paste(c.resize((W, H)), (W * (i % 3), H * (i // 3)))
    hoja.save(ruta, quality=80)


if __name__ == "__main__":
    import sys
    if "prueba" in sys.argv:
        d = os.environ.get("TMP_HOJAS", ".")
        _hoja(ficha("Mario Party", "Girar el *stick* con la palma te dejaba la mano *hecha polvo*.", "Mario Party / 1998"), 6, [], os.path.join(d, "n64_ficha.jpg"))
        _hoja(puesto(12, "La demanda de los guantes", "Mario Party"), 3.6, [], os.path.join(d, "n64_puesto.jpg"))
        _hoja(hud(7), 4, [], os.path.join(d, "n64_hud.jpg"), n=3)
        _hoja(linea_tiempo([("1993", "Project Reality"), ("1995", "Space World"), ("1996", "Sale en Japón")], "Así nació"), 6, [.4, 1.6, 3], os.path.join(d, "n64_linea.jpg"))
        _hoja(contador("Cartucho contra CD", [(64, "Megabytes en el cartucho más grande"), (650, "Megabytes en un CD")]), 6, [.3, 2.8], os.path.join(d, "n64_cont.jpg"))
        _hoja(lista(["Un *cartucho* gris", "Cuatro *puertos*", "Un *stick* analógico"], "La consola"), 5, [.4, 1.4, 2.4], os.path.join(d, "n64_lista.jpg"))
