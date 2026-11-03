# -*- coding: utf-8 -*-
"""MOTION GRAPHICS TRANSLÚCIDOS con la interfaz de POKÉMON ROJO/AZUL en Game Boy (Crónicas del gaming; primer uso
`pokemon_rojo_azul`, 3-nov-2026). Regla del 22-oct: fichas translúcidas con la interfaz de CADA juego, nunca carteles opacos.
Aquí la interfaz es la del Game Boy original:
  - los cuatro VERDES de la pantalla DMG (fondo translúcido verde muy oscuro, letras verde claro);
  - el CUADRO DE TEXTO de Rojo/Azul: doble filete con esquinas de píxel, texto que se escribe letra a letra y la flecha ▼ que late;
  - LETRA DE PÍXEL: Tahoma/Verdana negrita a 10-11 px SIN suavizado, ampliada ×3-×6 con vecino más cercano (como el texto del juego);
  - la Poké Ball de píxel que cae y se AGITA tres veces, como al capturar, en el rótulo de cada secreto.
    import mg_pokemon as P
  ficha(titulo, texto, tipo)       cuadro de texto RB; *x* = amarillo Pikachu
  puesto(num, titulo)              Poké Ball que cae y se agita + «SECRETO No.N» + título
  hud(n, total)                    contador de esquina (Poké Ball + N/20); se llama «aviso …» (no cuenta como MG)
  pegatina(ruta, titulo, tam)      imagen REAL con borde blanco y pestaña de píxel
  contador / linea_tiempo / lista / dos_versiones / mito            genéricos con esta interfaz
  nombres, indice, ranuras, tabla_tipos, foco, uno_de_256, mochila, equipo, ataques, cartas, bytes300, pastel, pistas, sello
                                   MG propios del guion (cada uno con su docstring)
Probar SIEMPRE con una hoja de cuadros antes de `fx` (python nucleo/mg_pokemon.py prueba).
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OSC, MED, CLA, LUZ = (15, 56, 15), (48, 98, 48), (139, 172, 15), (155, 188, 15)
BLANCO, CREMA = (248, 248, 232), (224, 236, 200)
ROJO, AZUL, AMARILLO, GRIS = (232, 56, 48), (72, 120, 232), (248, 208, 48), (150, 170, 140)
_fc, _pc = {}, {}


def _eo(u):
    u = max(0.0, min(1.0, u))
    return 1 - (1 - u) ** 3


def _reb(u):
    if u <= 0:
        return 0.0
    return 1.0 if u >= 1.6 else 1 - math.exp(-6 * u) * math.cos(9 * u)


def _bgra(im, alfa=1.0):
    a = np.array(im.convert("RGBA"))[..., [2, 1, 0, 3]].copy()
    alfa = max(0.0, min(1.0, alfa))
    if alfa < 1:
        a[..., 3] = (a[..., 3] * alfa).astype(np.uint8)
    return a


def _capa(w, h):
    return Image.new("RGBA", (max(2, int(w)), max(2, int(h))), (0, 0, 0, 0))


def _marcas(marcas, n, base=.4, paso=1.6):
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


def _salida(im, dt, dur, abre=.25):
    """Entrada como una ventana del Game Boy (se abre en vertical a saltos de píxel); salida con fundido."""
    u = _eo(dt / abre)
    if u < 1:
        W, H = im.size
        h = max(2, int(H * (.1 + .9 * round(u * 6) / 6)))
        p = im.resize((W, h), Image.NEAREST)
        out = _capa(W, H)
        out.alpha_composite(p, (0, (H - h) // 2))
        im = out
    return _bgra(im, min(_eo(dt / .15), (dur - dt) / .35))


# ------------------------------------------------------------------ letra de píxel
def _fuente(estilo):
    """«t» títulos (Verdana negrita 10 px), «b» texto (Tahoma negrita 11 px), «m» cifras/menús (Lucida Console 11 px)."""
    if estilo not in _fc:
        _fc[estilo] = ImageFont.truetype({"t": "C:/Windows/Fonts/verdanab.ttf", "b": "C:/Windows/Fonts/tahomabd.ttf",
                                          "m": "C:/Windows/Fonts/lucon.ttf"}[estilo], {"t": 10, "b": 11, "m": 11}[estilo])
    return _fc[estilo]


def ancho_pix(s, estilo="b", k=4):
    return int(math.ceil(_fuente(estilo).getlength(s.replace("*", "")))) * k + 2 * k


def pix(s, estilo="b", k=4, color=LUZ, sombra=True):
    """Texto de píxel: sin suavizado a 10-11 px y ampliado ×k con vecino más cercano. Con sombra oscura de 1 píxel (legible
    sobre cualquier clip). Devuelve RGBA."""
    key = (s, estilo, k, color, sombra)
    if key in _pc:
        return _pc[key]
    f = _fuente(estilo)
    w = int(math.ceil(f.getlength(s))) + 3
    m = Image.new("L", (max(2, w), 15), 0)
    d = ImageDraw.Draw(m)
    d.fontmode = "1"
    d.text((1, 1), s, font=f, fill=255)
    m = m.resize((m.width * k, m.height * k), Image.NEAREST)
    im = _capa(m.width + k, m.height + k)
    if sombra:
        sm = Image.new("RGBA", m.size, (6, 22, 6, 235))
        im.paste(sm, (k, k), m)
    col = Image.new("RGBA", m.size, color + (255,))
    im.alpha_composite(Image.composite(col, _capa(*m.size), m))
    if len(_pc) > 4000:
        _pc.clear()
    _pc[key] = im
    return im


def poner(im, xy, s, estilo="b", k=4, color=LUZ, ancla="l", alfa=255):
    """Pega texto de píxel; ancla «l» (izquierda, centrado en vertical), «m» (centro) o «r»."""
    if alfa <= 2 or not s:
        return 0
    t = pix(s, estilo, k, color)
    if alfa < 255:
        t = t.copy()
        t.putalpha(t.getchannel("A").point(lambda v: int(v * alfa / 255)))
    x, y = xy
    x = x - t.width / 2 if ancla == "m" else (x - t.width if ancla == "r" else x)
    im.alpha_composite(t, (int(x), int(y - t.height / 2)))
    return t.width


def rica(im, x, y, s, k=4, color=LUZ, resalte=AMARILLO, alfa=255, hasta=None, estilo="b", ancla="l"):
    """Línea con *resaltado*; `hasta` = letras visibles (máquina de escribir)."""
    trozos = s.split("*")
    if ancla == "m":
        x -= sum(ancho_pix(t, estilo, k) - 2 * k for t in trozos) / 2
    vis = 10 ** 9 if hasta is None else hasta
    for i, t in enumerate(trozos):
        if vis <= 0:
            break
        t2 = t[:max(0, int(vis))]
        if t2:
            poner(im, (x, y), t2, estilo, k, resalte if i % 2 else color, "l", alfa)
        x += ancho_pix(t, estilo, k) - 2 * k
        vis -= len(t)


def partir(s, ancho, k=4, estilo="b"):
    out, ln = [], ""
    for p in s.split():
        prueba = (ln + " " + p).strip()
        if ancho_pix(prueba, estilo, k) <= ancho or not ln:
            ln = prueba
        else:
            out.append(ln)
            ln = p
    if ln:
        out.append(ln)
    return out


# ------------------------------------------------------------------ piezas
def marco(w, h, k=4, alfa=.70, filete=LUZ):
    """Cuadro de texto de Rojo/Azul en versión TRANSLÚCIDA: verde muy oscuro difuminado + doble filete de píxel con las esquinas
    recortadas. Margen M alrededor para la sombra."""
    M = 30
    im = _capa(w + 2 * M, h + 2 * M)
    s = Image.new("L", im.size, 0)
    ImageDraw.Draw(s).rectangle((M - 4, M + 2, M + w + 4, M + h + 8), fill=120)
    sombra = Image.new("RGBA", im.size, (0, 0, 0, 255))
    sombra.putalpha(s.filter(ImageFilter.GaussianBlur(12)))
    im.alpha_composite(sombra)
    d = ImageDraw.Draw(im)
    d.rectangle((M + k, M + k, M + w - k, M + h - k), fill=OSC + (int(255 * alfa),))
    for ins, g in ((0, k), (2 * k, k)):                       # dos filetes; las esquinas se recortan un píxel
        x0, y0, x1, y1 = M + ins, M + ins, M + w - ins, M + h - ins
        c = 2 * k
        d.rectangle((x0 + c, y0, x1 - c, y0 + g - 1), fill=filete + (255,))
        d.rectangle((x0 + c, y1 - g + 1, x1 - c, y1), fill=filete + (255,))
        d.rectangle((x0, y0 + c, x0 + g - 1, y1 - c), fill=filete + (255,))
        d.rectangle((x1 - g + 1, y0 + c, x1, y1 - c), fill=filete + (255,))
        for cx, cy in ((x0 + k, y0 + k), (x1 - 2 * k + 1, y0 + k), (x0 + k, y1 - 2 * k + 1), (x1 - 2 * k + 1, y1 - 2 * k + 1)):
            d.rectangle((cx, cy, cx + k - 1, cy + k - 1), fill=filete + (255,))
    return im, M


def flecha(im, x, y, dt, k=4, color=LUZ):
    """La flecha ▼ del cuadro de texto, que sube y baja a saltos."""
    if int(dt * 2.5) % 2:
        y += k
    d = ImageDraw.Draw(im)
    for i in range(4):
        d.rectangle((x + i * k, y + i * k, x + (7 - i) * k - 1, y + (i + 1) * k - 1), fill=color + (255,))


def cursor(im, x, y, k=4, color=BLANCO):
    """El cursor ▶ de los menús de RB, en píxel (la letra no trae el glifo)."""
    d = ImageDraw.Draw(im)
    for i in range(4):
        d.rectangle((x + i * k, y - (4 - i) * k, x + (i + 1) * k - 1, y + (4 - i) * k - 1), fill=color + (255,))


def palomita(im, x, y, k=4, color=AMARILLO):
    """✓ de píxel centrado en (x, y)."""
    d = ImageDraw.Draw(im)
    for i, (a, b) in enumerate(((-3, 0), (-2, 1), (-1, 2), (0, 1), (1, 0), (2, -1), (3, -2))):
        d.rectangle((x + a * k, y + b * k, x + (a + 1) * k - 1, y + (b + 1) * k - 1), fill=color + (255,))


def pestana(im, x, y, s, k=4, color=AMARILLO):
    """Pestaña del título: bloque verde oscuro con filete claro y el texto de píxel."""
    t = pix(s, "t", k, color)
    w, h = t.width + 8 * k, t.height + 2 * k
    d = ImageDraw.Draw(im)
    d.rectangle((x, y - h / 2, x + w, y + h / 2), fill=OSC + (235,), outline=LUZ + (255,), width=k)
    im.alpha_composite(t, (int(x + 4 * k), int(y - t.height / 2)))
    return w


_BALL = ["......####......", "....##RRRR##....", "...#RRRRRRRR#...", "..#RRRRRRRRRR#..", ".#RRRRRRRRRRRR#.", ".#RRRRRRRRRRRR#.",
         "#RRRRRR##RRRRRR#", "#######WW#######", "#######WW#######", "#WWWWWW##WWWWWW#", ".#WWWWWWWWWWWW#.", ".#WWWWWWWWWWWW#.",
         "..#WWWWWWWWWW#..", "...#WWWWWWWW#...", "....##WWWW##....", "......####......"]


def pokeball(tam=64, gris=False):
    """Poké Ball de píxel (16×16 ampliada)."""
    key = ("ball", tam, gris)
    if key not in _pc:
        im = Image.new("RGBA", (16, 16), (0, 0, 0, 0))
        px = im.load()
        col = {"#": (16, 24, 16, 255), "R": (GRIS if gris else ROJO) + (255,), "W": (BLANCO + (255,))}
        for y, fila in enumerate(_BALL):
            for x, c in enumerate(fila):
                if c in col:
                    px[x, y] = col[c]
        _pc[key] = im.resize((tam, tam), Image.NEAREST)
    return _pc[key]


def sprite(ruta, alto):
    """Imagen real (arte oficial con alfa) a una altura dada; para MG con personajes."""
    alto = max(2, int(alto))          # el rebote de entrada da alturas negativas en los primeros cuadros (fx del 3-nov)
    key = ("spr", ruta, alto)
    if key not in _pc:
        im = Image.open(ruta).convert("RGBA")
        bb = im.getchannel("A").getbbox()
        if bb:
            im = im.crop(bb)
        im = im.resize((max(2, int(im.width * alto / im.height)), alto), Image.NEAREST if im.height < 160 else Image.LANCZOS)
        _pc[key] = im
    return _pc[key]


def _base(w, h, titulo, dt, k=4):
    im, M = marco(w, h, k)
    if titulo:
        pestana(im, M + 26, M + 2, titulo, 4, AMARILLO)
    return im, M


def _lienzo(w, h):
    """Lienzo con 26 px extra arriba para que la pestaña del título no se corte."""
    return w, h


# ------------------------------------------------------------------ ficha
def ficha(titulo, texto, tipo=None, ancho=900, vel=48, k=4):
    """Cuadro de texto de RB translúcido: `titulo` en la pestaña amarilla, `tipo` en verde claro pequeño y el texto que se
    ESCRIBE letra a letra; ▼ al terminar. *x* = amarillo."""
    in_w = ancho - 2 * 46
    ls = partir(texto, in_w, k)
    while len(ls) > 6 and k > 3:
        k -= 1
        ls = partir(texto, in_w, k)
    lh = 15 * k + 4
    h = int(52 + (40 if tipo else 0) + lh * len(ls) + 34)
    letras = [len(x.replace("*", "")) for x in ls]

    def fn(dt, dur, marcas):
        base, M = marco(ancho, h, 4)
        im = _capa(base.width, base.height + 30)
        im.alpha_composite(base, (0, 30))
        pestana(im, M + 26, M + 32, titulo, 4, AMARILLO) if _eo((dt - .05) / .2) > .5 else None
        y = M + 30 + 50
        if tipo:
            poner(im, (M + 46, y), tipo, "m", 3, CLA, "l", 255 * _eo((dt - .2) / .3))
            y += 40
        y += lh / 2 - 6
        quedan = max(0.0, (dt - .3) * vel)
        for ln, n in zip(ls, letras):
            rica(im, M + 46, y, ln, k, BLANCO, AMARILLO, 255, hasta=quedan)
            quedan -= n
            y += lh
        if quedan > 0:
            flecha(im, M + ancho - 70, M + 30 + h - 42, dt)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ rótulo de secreto
def puesto(num, titulo, arriba=None):
    """Banda translúcida: la Poké Ball cae, rebota y se AGITA tres veces (como al capturar) y suelta estrellitas; «SECRETO No.N»
    en letra de píxel grande y el título en amarillo debajo."""
    arriba = arriba or f"SECRETO No.{num}"
    tt = pix(arriba, "t", 7, BLANCO)
    k2 = 5
    while ancho_pix(titulo, "b", k2) > 1180 and k2 > 3:
        k2 -= 1
    tw = ancho_pix(titulo, "b", k2)
    w = max(tt.width, tw) + 300
    h = 230

    def fn(dt, dur, marcas):
        im, M = marco(w, h, 5, alfa=.6)
        u = _reb((dt - .05) / .45)
        if u > .02:
            ag = 0.0
            if 1.0 < dt < 2.4:                              # tres sacudidas
                f = (dt - 1.0) / 1.4
                ag = 24 * math.sin(f * 3 * 2 * math.pi) * (1 - f)
            b = pokeball(128).rotate(ag, resample=Image.NEAREST, expand=True)
            y = M + h / 2 - b.height / 2 - (1 - min(1.0, u)) * 140
            im.alpha_composite(b, (int(M + 70 + 64 - b.width / 2), max(0, int(y))))
            if dt > 2.45:                                   # «¡click!»: estrellitas
                e = _eo((dt - 2.45) / .4)
                dd = ImageDraw.Draw(im)
                for i in range(3):
                    a = -math.pi / 2 + (i - 1) * .8
                    x = M + 134 + math.cos(a) * 90 * e
                    yy = M + h / 2 + math.sin(a) * 90 * e
                    dd.rectangle((x - 6, yy - 6, x + 6, yy + 6), fill=AMARILLO + (int(255 * (1 - e * .6)),))
        tx = M + 240 + (w - 240) / 2
        n = int(max(0, dt - .2) * 30)
        if n:
            poner(im, (tx, M + 78), arriba[:n], "t", 7, BLANCO, "m")
        rica(im, tx, M + 168, titulo, k2, AMARILLO, BLANCO, 255 * _eo((dt - .5) / .3), ancla="m")
        return _bgra(im, min(_eo(dt / .2), (dur - dt) / .45))
    return fn


def hud(n, total=20):
    """Contador de esquina: Poké Ball + «N/20» (nombrarlo «aviso …» en efectos.py: es numeración, no MG)."""
    s = f"{n}/{total}"

    def fn(dt, dur, marcas):
        t = pix(s, "t", 5, BLANCO)
        im = _capa(t.width + 110, 100)
        b = pokeball(64)
        im.alpha_composite(b, (12, 18))
        poner(im, (92, 50), s, "t", 5, BLANCO, "l")
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .35))
    return fn


# ------------------------------------------------------------------ pegatina
def pegatina(ruta, titulo=None, tam=360, giro=-5.0):
    """Imagen REAL recortada con borde blanco (mg_tes) con rebote y balanceo; el nombre en una pestaña de píxel."""
    import mg_tes as T
    base = T._base_pegatina(ruta, tam)
    if titulo:
        t = pix(titulo, "t", 3, AMARILLO)
        pw, ph = t.width + 30, t.height + 14
        pil = _capa(pw, ph)
        ImageDraw.Draw(pil).rectangle((0, 0, pw - 1, ph - 1), fill=OSC + (240,), outline=LUZ + (255,), width=3)
        pil.alpha_composite(t, (15, 7))
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
        kk = s * (1 + .025 * math.sin(dt * 3.0))
        im = im.resize((max(2, int(im.width * kk)), max(2, int(im.height * kk))), Image.BILINEAR)
        a = np.array(im)[..., [2, 1, 0, 3]]
        fl = int(round(7 * math.sin(dt * 1.7)))
        out = np.zeros((a.shape[0] + 16, a.shape[1], 4), np.uint8)
        out[8 + fl:8 + fl + a.shape[0]] = a
        if dur - dt < .3:
            out[..., 3] = (out[..., 3] * max(0.0, (dur - dt) / .3)).astype(np.uint8)
        return out
    return fn


# ------------------------------------------------------------------ genéricos
def contador(titulo, pasos, w=1100, h=330):
    """Cifra grande que SUBE hasta el valor de cada paso. pasos = [(valor, texto[, «formateado»])]; marca k = paso k."""
    def fn(dt, dur, marcas):
        im, M = _base(w, h, titulo, dt)
        mk = _marcas(marcas, len(pasos), .3, 1.8)
        kk = _actual(mk, dt, len(pasos))
        v0 = pasos[kk - 1][0] if kk else 0
        v1, texto = pasos[kk][0], pasos[kk][1]
        u = _eo((dt - mk[kk]) / 1.1)
        v = v0 + (v1 - v0) * u
        s = pasos[kk][2] if len(pasos[kk]) > 2 and u >= 1 else f"{int(round(v)):,}".replace(",", " ")
        poner(im, (M + w / 2, M + 130), s, "t", 10, BLANCO, "m")
        kt = 4
        while ancho_pix(texto, "b", kt) > w - 80 and kt > 3:
            kt -= 1
        rica(im, M + w / 2, M + h - 62, texto, kt, AMARILLO, BLANCO, 255 * _eo((dt - mk[kk] - .3) / .4), ancla="m")
        return _salida(im, dt, dur)
    return fn


def linea_tiempo(hitos, titulo="Así fue", w=1700, h=400):
    """Línea de píxel que se dibuja; marca k = hito k: una Poké Ball cae en su sitio con el año y el texto. El último late."""
    n = len(hitos)

    def fn(dt, dur, marcas):
        im, M = _base(w, h, titulo, dt)
        d = ImageDraw.Draw(im)
        mk = _marcas(marcas, n, .4, 1.4)
        x0, x1 = M + 120, M + w - 120
        paso = (x1 - x0) / max(1, n - 1)
        yl = M + 186
        u = _eo((dt - mk[0] + .2) / max(.6, mk[-1] - mk[0] + .4))
        xa = x0 - 40 + (x1 - x0 + 80) * u
        for xx in range(int(x0 - 40), int(xa), 16):          # trazo a guiones de píxel
            d.rectangle((xx, yl - 4, xx + 9, yl + 4), fill=LUZ + (255,))
        for i, (ano, txt) in enumerate(hitos):
            r = _reb((dt - mk[i]) / .45)
            if r <= .02:
                continue
            x = x0 + paso * i
            late = 1 + (.14 * math.sin(dt * 6) if i == n - 1 and dt > mk[i] + .5 else 0)
            b = pokeball(int(56 * min(1.1, r) * late))
            im.alpha_composite(b, (int(x - b.width / 2), int(yl - b.height / 2)))
            poner(im, (x, yl - 70), ano, "t", 5, BLANCO, "m", 255 * min(1.0, r))
            ls = partir(txt, paso * .95 if n > 1 else w * .6, 3)
            y = yl + 66
            for ln in ls[:3]:
                rica(im, x, y, ln, 3, LUZ, AMARILLO, 255 * _eo((dt - mk[i] - .15) / .3), ancla="m")
                y += 46
        return _salida(im, dt, dur)
    return fn


def lista(items, titulo, w=1100, renglon=70, icono=None):
    """Menú de RB: renglones que entran uno por marca con el cursor ▶ en el último. *x* = amarillo."""
    n = len(items)
    h = 70 + n * renglon + 20

    def fn(dt, dur, marcas):
        im, M = _base(w, h, titulo, dt)
        mk = _marcas(marcas, n, .4, 1.2)
        act = _actual(mk, dt, n)
        for i, s in enumerate(items):
            u = _eo((dt - mk[i]) / .3)
            if u <= 0:
                continue
            y = M + 66 + renglon * (i + .5)
            if i == act:
                cursor(im, M + 44, y)
            rica(im, M + 92, y, s, 4, BLANCO, AMARILLO, 255 * u)
        return _salida(im, dt, dur)
    return fn


def dos_versiones(titulo, a, b, w=1400, h=430, sello_b=None):
    """Dos columnas: a = (etiqueta, imagen o None, texto); b igual. Marca 0 = a, marca 1 = b (+ sello opcional)."""
    def fn(dt, dur, marcas):
        im, M = _base(w, h, titulo, dt)
        mk = _marcas(marcas, 2, .3, 1.8)
        for i, (et, ruta, txt) in enumerate((a, b)):
            u = _reb((dt - mk[i]) / .45)
            if u <= .02:
                continue
            cx = M + w * (.25 if i == 0 else .75)
            poner(im, (cx, M + 60), et, "t", 4, AMARILLO, "m", 255 * min(1, u))
            if ruta:
                s = sprite(ruta, int(220 * min(1.05, u)))
                im.alpha_composite(s, (int(cx - s.width / 2), int(M + 90)))
            ls = partir(txt, w * .44, 3)
            y = M + h - 40 - 44 * (len(ls) - 1)
            for ln in ls[:3]:
                rica(im, cx, y, ln, 3, BLANCO, AMARILLO, 255 * min(1, u), ancla="m")
                y += 44
        d = ImageDraw.Draw(im)
        u = _eo((dt - mk[0]) / .5)
        d.rectangle((M + w / 2 - 3, M + 50, M + w / 2 + 3, M + 50 + (h - 90) * u), fill=LUZ + (200,))
        if sello_b and dt > mk[1] + .7:
            _sello(im, M + w * .75, M + h * .45, sello_b, dt - mk[1] - .7)
        return _salida(im, dt, dur)
    return fn


def _sello(im, x, y, s, t, color=ROJO):
    """Sello de píxel que cae girado (NO, ERROR, MENTIRA…)."""
    r = _reb(t / .35)
    if r <= .02:
        return
    tt = pix(s, "t", 9, color, sombra=False)
    c = _capa(tt.width + 60, tt.height + 40)
    ImageDraw.Draw(c).rectangle((6, 6, c.width - 7, c.height - 7), outline=color + (255,), width=8)
    c.alpha_composite(tt, (30, 20))
    k = 1.6 - .6 * min(1.0, r)
    c = c.resize((int(c.width * k), int(c.height * k)), Image.NEAREST).rotate(-12, resample=Image.NEAREST, expand=True)
    c.putalpha(c.getchannel("A").point(lambda v: int(v * min(1.0, r))))
    im.alpha_composite(c, (int(x - c.width / 2), int(y - c.height / 2)))


def mito(dicen, verdad, titulo="El rumor", sello="FALSO", w=1200, h=360):
    """«Se decía…» (marca 0) y la verdad (marca 1) con el sello encima de lo que se decía."""
    def fn(dt, dur, marcas):
        im, M = _base(w, h, titulo, dt)
        mk = _marcas(marcas, 2, .3, 2.0)
        y = M + 90
        for ln in partir(dicen, w - 100, 4):
            rica(im, M + 50, y, ln, 4, GRIS if dt > mk[1] else BLANCO, AMARILLO, 255 * _eo((dt - mk[0]) / .3))
            y += 62
        if dt > mk[1]:
            _sello(im, M + w * .72, M + 110, sello, dt - mk[1])
            yy = M + h - 70
            rica(im, M + 50, yy, verdad, 4, AMARILLO, BLANCO, 255 * _eo((dt - mk[1] - .4) / .3))
        return _salida(im, dt, dur)
    return fn


# ================================================================== MG PROPIOS de pokemon_rojo_azul (3-nov-2026)
def nombres(w=1300, h=470):
    """Pantalla de nombres de RB japonés: JUGADOR (NUEVO NOMBRE / SATOSHI / …) y RIVAL (… / SHIGERU / …). Marca 0 = el cursor
    baja a SATOSHI, marca 1 = a SHIGERU, marca 2 = «VERDE» y los nombres se CRUZAN de columna."""
    j = ["NUEVO NOMBRE", "SATOSHI", "JACK", "HIROSHI"]
    r = ["NUEVO NOMBRE", "SHIGERU", "JOHN", "TSUNEKAZU"]

    def fn(dt, dur, marcas):
        im, M = _base(w, h, "Pocket Monsters Rojo", dt)
        mk = _marcas(marcas, 3, .4, 1.8)
        cruce = _eo((dt - mk[2]) / .8) if dt > mk[2] else 0
        for col, (et, ops, sel, m) in enumerate((("TU NOMBRE", j, 1, mk[0]), ("RIVAL", r, 1, mk[1]))):
            x = M + 70 + col * w / 2
            poner(im, (x, M + 70), et, "t", 4, AMARILLO, "l")
            for i, s in enumerate(ops):
                y = M + 140 + i * 70
                es = i == sel and dt > m
                xs = x + 50
                if es and cruce > 0:                        # en Verde, SATOSHI y SHIGERU cambian de lado
                    xs += (w / 2) * cruce * (1 if col == 0 else -1)
                poner(im, (xs, y), s, "b", 4, AMARILLO if es else BLANCO, "l")
                if es and cruce == 0:
                    cursor(im, x + 4, y)
        if cruce > 0:
            poner(im, (M + w / 2, M + h - 40), "En VERDE: al revés", "t", 4, (120, 220, 120), "m", 255 * cruce)
        return _salida(im, dt, dur)
    return fn


def indice(ruta_a, ruta_b, w=1300, h=460):
    """Dos fichas de Pokédex: «POKéDEX No.001 BULBASAUR» (marca 0) y «CÓDIGO No.001 RHYDON» (marca 1), que entra girando."""
    def fn(dt, dur, marcas):
        im, M = _base(w, h, "Dos números", dt)
        mk = _marcas(marcas, 2, .3, 1.8)
        for i, (ruta, et, nom) in enumerate(((ruta_a, "POKéDEX", "BULBASAUR"), (ruta_b, "EN EL CÓDIGO", "RHYDON"))):
            u = _reb((dt - mk[i]) / .5)
            if u <= .02:
                continue
            cx = M + w * (.27 if i == 0 else .73)
            poner(im, (cx, M + 64), et, "t", 4, AMARILLO, "m")
            s = sprite(ruta, int(230 * min(1.05, u)))
            if i == 1 and u < 1:
                s = s.resize((max(2, int(s.width * abs(math.cos((1 - u) * math.pi / 2)))), s.height), Image.NEAREST)
            im.alpha_composite(s, (int(cx - s.width / 2), M + 98))
            poner(im, (cx, M + h - 78), "No.001", "t", 6, BLANCO, "m")
            poner(im, (cx, M + h - 30), nom, "b", 4, AMARILLO if i else LUZ, "m")
        return _salida(im, dt, dur)
    return fn


# índices internos que quedaron VACÍOS (MissingNo.) en Rojo/Azul: 39 huecos entre 1 y 190
HUECOS = (31, 32, 50, 52, 56, 61, 62, 63, 67, 68, 69, 79, 80, 81, 86, 87, 94, 95, 115, 121, 122, 127, 134, 135, 137, 140, 146,
          156, 159, 160, 161, 162, 172, 174, 175, 181, 182, 183, 184)


def ranuras(ruta_ultimo=None, w=1500, h=560):
    """La lista interna: 190 casillas (19×10) que se llenan en orden; las 39 vacías parpadean con ruido de MissingNo.
    Marca 0 = empieza a llenarse, marca 1 = se encienden los huecos (contador 39), marca 2 = la 190 late: VICTREEBEL."""
    cols, filas = 19, 10
    cw = (w - 140) / cols
    ch = (h - 200) / filas

    def fn(dt, dur, marcas):
        im, M = _base(w, h, "Lista interna: 190 puestos", dt)
        d = ImageDraw.Draw(im)
        mk = _marcas(marcas, 3, .3, 1.8)
        llen = int(190 * _eo((dt - mk[0]) / 1.4)) if dt > mk[0] else 0
        rng = np.random.default_rng(int(dt * 12))
        for i in range(1, 191):
            c, f = (i - 1) % cols, (i - 1) // cols
            x, y = M + 70 + c * cw, M + 70 + f * ch
            if i > llen:
                d.rectangle((x, y, x + cw - 6, y + ch - 6), outline=MED + (200,), width=2)
                continue
            if i in HUECOS:
                if dt > mk[1]:
                    for _ in range(5):                       # ruido de MissingNo
                        a, b = rng.integers(0, int(cw - 10)), rng.integers(0, int(ch - 10))
                        d.rectangle((x + a, y + b, x + a + 6, y + b + 6), fill=(BLANCO if rng.random() < .5 else (90, 60, 120)) + (255,))
                    d.rectangle((x, y, x + cw - 6, y + ch - 6), outline=ROJO + (255,), width=3)
                else:
                    d.rectangle((x, y, x + cw - 6, y + ch - 6), fill=CLA + (150,))
            else:
                d.rectangle((x, y, x + cw - 6, y + ch - 6), fill=CLA + (150,))
            if i == 190 and dt > mk[2]:
                p = 1 + .5 * abs(math.sin(dt * 5))
                d.rectangle((x - 4 * p, y - 4 * p, x + cw - 6 + 4 * p, y + ch - 6 + 4 * p), outline=AMARILLO + (255,), width=5)
        if dt > mk[1]:
            n = int(39 * _eo((dt - mk[1]) / 1.0))
            poner(im, (M + 70, M + h - 50), f"VACÍOS: {n}", "t", 5, ROJO, "l")
        if dt > mk[2]:
            poner(im, (M + w - 70, M + h - 50), "No.190 VICTREEBEL", "t", 5, AMARILLO, "r", 255 * _eo((dt - mk[2]) / .3))
            if ruta_ultimo:
                s = sprite(ruta_ultimo, int(170 * _reb((dt - mk[2]) / .5) or 2))
                im.alpha_composite(s, (int(M + w - 70 - s.width), int(M + h - 90 - s.height)))
        return _salida(im, dt, dur)
    return fn


def tabla_tipos(w=1320, h=470):
    """FANTASMA → PSÍQUICO. Marca 0 = «Debía: ×2 ¡Es súper eficaz!»; marca 1 = se tacha y sale «En el juego: ×0 No le afecta»
    con el sello ERROR; marca 2 = «Único ataque Fantasma: LENGÜETAZO» (opcional)."""
    def fn(dt, dur, marcas):
        im, M = _base(w, h, "Tabla de tipos", dt)
        d = ImageDraw.Draw(im)
        mk = _marcas(marcas, 3, .3, 1.8)
        poner(im, (M + 60, M + 90), "ATAQUE", "m", 3, CLA, "l")
        poner(im, (M + w - 60, M + 90), "DEFENSA", "m", 3, CLA, "r")
        poner(im, (M + 60, M + 150), "FANTASMA", "t", 6, (190, 140, 240), "l")
        poner(im, (M + w - 60, M + 150), "PSÍQUICO", "t", 6, (255, 120, 170), "r")
        u = _eo((dt - .3) / .6)
        d.rectangle((M + 470, M + 146, M + 470 + (w - 980) * u, M + 154), fill=LUZ + (255,))
        if dt > mk[0]:
            a = 255 * _eo((dt - mk[0]) / .3)
            rica(im, M + 60, M + 250, "Debía: *×2* ¡Es súper eficaz!", 4, BLANCO, AMARILLO, a)
            if dt > mk[1]:
                d = ImageDraw.Draw(im)
                x1 = M + 60 + (ancho_pix("Debía: ×2 ¡Es súper eficaz!", "b", 4)) * _eo((dt - mk[1]) / .4)
                d.rectangle((M + 56, M + 248, x1, M + 256), fill=ROJO + (255,))
        if dt > mk[1]:
            rica(im, M + 60, M + 330, "En el juego: *×0* No le afecta", 4, BLANCO, ROJO, 255 * _eo((dt - mk[1] - .3) / .3))
            _sello(im, M + w - 230, M + 300, "ERROR", dt - mk[1] - .6)
        if marcas and len(marcas) > 2 and dt > mk[2]:
            rica(im, M + 60, M + 410, "Y el único ataque Fantasma: *LENGÜETAZO*", 3, LUZ, AMARILLO, 255 * _eo((dt - mk[2]) / .3))
        return _salida(im, dt, dur)
    return fn


def foco(w=1200, h=430):
    """Probabilidad de crítico. Marca 0 = barra base; marca 1 = «Prometía ×4» crece; marca 2 = «Hacía ÷4» encoge + BUG."""
    def fn(dt, dur, marcas):
        im, M = _base(w, h, "FOCO ENERGÍA", dt)
        d = ImageDraw.Draw(im)
        mk = _marcas(marcas, 3, .3, 1.8)
        filas = [("Normal", 1.0, LUZ, mk[0]), ("Prometía ×4", 4.0, AMARILLO, mk[1]), ("Hacía ÷4", .25, ROJO, mk[2])]
        for i, (et, v, col, m) in enumerate(filas):
            if dt < m:
                continue
            y = M + 100 + i * 100
            poner(im, (M + 50, y), et, "b", 4, col, "l")
            u = _eo((dt - m) / .8)
            largo = (w - 560) * v / 4 * u
            for xx in range(0, int(largo), 14):
                d.rectangle((M + 480 + xx, y - 18, M + 480 + xx + 10, y + 18), fill=col + (255,))
        if dt > mk[2] + .8:
            _sello(im, M + w - 200, M + 330, "BUG", dt - mk[2] - .8)
        return _salida(im, dt, dur)
    return fn


def uno_de_256(w=760, h=560):
    """256 casillas (16×16) verdes = «100 % de precisión»; marca 0 = se llenan, marca 1 = UNA se vuelve roja: FALLÓ."""
    def fn(dt, dur, marcas):
        im, M = _base(w, h, "Precisión: 100 %", dt)
        d = ImageDraw.Draw(im)
        mk = _marcas(marcas, 2, .3, 1.8)
        n = int(256 * _eo((dt - mk[0]) / 1.0)) if dt > mk[0] else 0
        c = (w - 120) / 16
        for i in range(n):
            x, y = M + 60 + (i % 16) * c, M + 60 + (i // 16) * ((h - 160) / 16)
            mala = i == 201 and dt > mk[1]
            col = ROJO if mala and int(dt * 6) % 2 == 0 else (ROJO if mala else CLA)
            d.rectangle((x, y, x + c - 5, y + (h - 160) / 16 - 5), fill=col + (230,))
        if dt > mk[1]:
            poner(im, (M + w / 2, M + h - 52), "1 de 256: ¡FALLÓ!", "t", 5, ROJO, "m", 255 * _eo((dt - mk[1]) / .3))
        return _salida(im, dt, dur)
    return fn


def mochila(objetos, w=900, renglon=64):
    """Menú OBJETO de RB. objetos = [(nombre, cantidad)]. Marca 0 = la lista, marca 1 = el cursor baja al 6.º, marca 2 = su
    cantidad sube +128 (la «duplicación» de MissingNo)."""
    n = len(objetos)
    h = 70 + n * renglon + 30

    def fn(dt, dur, marcas):
        im, M = _base(w, h, "OBJETO", dt)
        mk = _marcas(marcas, 3, .3, 1.6)
        cur = min(5, int(max(0, dt - mk[1]) * 6)) if dt > mk[1] else 0
        for i, (nom, c) in enumerate(objetos):
            u = _eo((dt - mk[0] - .08 * i) / .25)
            y = M + 70 + renglon * (i + .5)
            cant = c
            col = BLANCO
            if i == 5 and dt > mk[2]:
                cant = c + int(128 * _eo((dt - mk[2]) / 1.4))
                col = AMARILLO
            poner(im, (M + 90, y), nom, "b", 4, col, "l", 255 * u)
            poner(im, (M + w - 50, y), f"×{cant}", "m", 4, col, "r", 255 * u)
            if i == cur:
                cursor(im, M + 44, y)
        return _salida(im, dt, dur)
    return fn


def equipo(miembros, titulo="Equipo", w=1100, renglon=96):
    """Pantalla POKéMON de RB: renglón = icono real + NOMBRE + :L66 + barra PS verde. miembros = [(ruta|None, nombre, nivel)];
    un renglón por marca."""
    n = len(miembros)
    h = 70 + n * renglon + 20

    def fn(dt, dur, marcas):
        im, M = _base(w, h, titulo, dt)
        d = ImageDraw.Draw(im)
        mk = _marcas(marcas, n, .4, .9)
        for i, (ruta, nom, nv) in enumerate(miembros):
            u = _reb((dt - mk[i]) / .4)
            if u <= .02:
                continue
            y = M + 70 + renglon * (i + .5)
            if ruta:
                s = sprite(ruta, int(80 * min(1.05, u)))
                im.alpha_composite(s, (int(M + 90 - s.width / 2), int(y - s.height / 2)))
            else:
                b = pokeball(56, gris=True)
                im.alpha_composite(b, (int(M + 62), int(y - 28)))
                nom = nom or "?"
            poner(im, (M + 160, y - 14), nom, "b", 4, BLANCO, "l")
            poner(im, (M + 560, y - 14), f":L{nv}", "m", 4, AMARILLO, "l")
            pw = (w - 820) * _eo((dt - mk[i]) / .6)
            poner(im, (M + 160, y + 26), "PS:", "m", 3, CLA, "l")
            d.rectangle((M + 240, y + 18, M + 240 + 380, y + 34), outline=LUZ + (255,), width=3)
            d.rectangle((M + 244, y + 22, M + 244 + 372 * min(1, pw / max(1, w - 820)), y + 30), fill=(96, 208, 96, 255))
        return _salida(im, dt, dur)
    return fn


def ataques(nombre, ataques_, ilegal, ruta=None, w=1100, h=480):
    """Menú LUCHA de RB con los 4 ataques del Pokémon; marca 0 = la lista, marca 1 = el cursor llega al ilegal y sale
    «✗ no lo puede aprender» + sello TRAMPA."""
    def fn(dt, dur, marcas):
        im, M = _base(w, h, nombre, dt)
        mk = _marcas(marcas, 2, .3, 1.8)
        for i, a in enumerate(ataques_):
            y = M + 90 + i * 72
            mal = a == ilegal and dt > mk[1]
            poner(im, (M + 100, y), a, "b", 5, ROJO if mal else BLANCO, "l", 255 * _eo((dt - mk[0] - .1 * i) / .25))
            if (a == ilegal and dt > mk[1]) or (dt < mk[1] and i == 0):
                cursor(im, M + 50, y, 5)
        if ruta:
            s = sprite(ruta, 300)
            im.alpha_composite(s, (int(M + w - 60 - s.width), int(M + 60)))
        if dt > mk[1]:
            rica(im, M + 60, M + h - 40, f"*{ilegal}*: Dragonite no puede aprenderlo", 3, BLANCO, ROJO, 255 * _eo((dt - mk[1] - .3) / .3))
            _sello(im, M + w - 230, M + h - 150, "TRAMPA", dt - mk[1] - .6)
        return _salida(im, dt, dur)
    return fn


def cartas(ruta_mew=None, total=78000, premios=20, w=1300, h=520):
    """Lluvia de sobres de píxel y contador hasta 78 000 (marca 0); marca 1 = «20 ganadores»: 20 Poké Balls con Mew."""
    rng = np.random.default_rng(7)
    sobres = [(rng.random(), rng.random() * 1.6, rng.integers(-20, 20)) for _ in range(60)]

    def fn(dt, dur, marcas):
        im, M = _base(w, h, "Concurso CoroCoro", dt)
        d = ImageDraw.Draw(im)
        mk = _marcas(marcas, 2, .3, 2.4)
        if dt < mk[1] + .4:
            for x, t0, g in sobres:
                yy = ((dt - mk[0] - t0) * 300) % (h - 120)
                if dt - mk[0] - t0 < 0:
                    continue
                xx = M + 40 + x * (w - 160)
                d.rectangle((xx, M + 60 + yy, xx + 56, M + 60 + yy + 38), fill=CREMA + (220,), outline=OSC + (255,), width=3)
                d.line([(xx, M + 60 + yy), (xx + 28, M + 60 + yy + 20), (xx + 56, M + 60 + yy)], fill=OSC + (255,), width=3)
        n = int(total * _eo((dt - mk[0]) / 2.0)) if dt > mk[0] else 0
        poner(im, (M + w / 2, M + 150), f"{n:,}".replace(",", " ") + " cartas", "t", 9, BLANCO, "m")
        if dt > mk[1]:
            u = _eo((dt - mk[1]) / 1.0)
            for i in range(int(premios * u)):
                x = M + 110 + (i % 10) * ((w - 220) / 9)
                y = M + 270 + (i // 10) * 100
                b = pokeball(64)
                im.alpha_composite(b, (int(x - 32), int(y)))
            poner(im, (M + w / 2, M + h - 40), f"Solo {premios} MEW", "t", 6, AMARILLO, "m", 255 * u)
            if ruta_mew and dt > mk[1] + .6:
                s = sprite(ruta_mew, int(200 * min(1.0, _reb((dt - mk[1] - .6) / .5)) or 2))
                im.alpha_composite(s, (int(M + w - 40 - s.width), int(M + 40)))
        return _salida(im, dt, dur)
    return fn


def bytes300(ruta_mew=None, w=1500, h=420):
    """El cartucho LLENO (bloques de memoria); marca 0 = «se quitan las herramientas de depuración»: se abre un hueco;
    marca 1 = «~300 bytes»; marca 2 = Mew entra en el hueco y lo llena."""
    n = 48

    def fn(dt, dur, marcas):
        im, M = _base(w, h, "Memoria del cartucho", dt)
        d = ImageDraw.Draw(im)
        mk = _marcas(marcas, 3, .3, 1.6)
        bw = (w - 120) / n
        hueco = range(34, 38)
        for i in range(n):
            x = M + 60 + i * bw
            vacio = i in hueco and dt > mk[0]
            if vacio and dt > mk[2] + .5:
                col = (250, 150, 200)
            elif vacio:
                a = _eo((dt - mk[0]) / .5)
                col = tuple(int(CLA[j] * (1 - a) + OSC[j] * a) for j in range(3))
            else:
                col = CLA
            d.rectangle((x, M + 110, x + bw - 4, M + 230), fill=col + (230,))
        poner(im, (M + 60, M + 80), "LLENO", "t", 4, LUZ, "l")
        if dt > mk[0]:
            xh = M + 60 + 34 * bw
            d.rectangle((xh - 4, M + 104, xh + 4 * bw, M + 236), outline=AMARILLO + (255,), width=4)
            if dt > mk[1]:
                poner(im, (xh + 2 * bw, M + 290), "~300 BYTES", "t", 6, AMARILLO, "m", 255 * _eo((dt - mk[1]) / .3))
        if dt > mk[2] and ruta_mew:
            u = _eo((dt - mk[2]) / .7)
            s = sprite(ruta_mew, 150)
            xh = M + 60 + 36 * bw
            im.alpha_composite(s, (int(xh - s.width / 2), int(M + h - 10 - s.height - (1 - u) * 0 + (1 - u) * 160)))
        return _salida(im, dt, dur)
    return fn


def pastel(partes, titulo="Los derechos de Pokémon", w=1100, h=500):
    """Pastel de píxel en tercios: partes = [(etiqueta, color)]; una porción por marca; la última se separa y late."""
    n = len(partes)

    def fn(dt, dur, marcas):
        im, M = _base(w, h, titulo, dt)
        mk = _marcas(marcas, n, .3, 1.0)
        R = 170
        cx, cy = M + 270, M + h / 2 + 20
        pie = Image.new("RGBA", (R * 2 // 6 + 2, R * 2 // 6 + 2), (0, 0, 0, 0))
        pd = ImageDraw.Draw(pie)
        r = R // 6
        for i, (et, col) in enumerate(partes):
            u = _eo((dt - mk[i]) / .5)
            if u <= 0:
                continue
            a0 = -90 + 360 * i / n
            pd.pieslice((1, 1, 2 * r, 2 * r), a0, a0 + 360 / n * u, fill=col + (255,), outline=OSC + (255,))
            y = M + 120 + i * 90
            ImageDraw.Draw(im).rectangle((M + 560, y - 14, M + 588, y + 14), fill=col + (int(255 * u),))
            poner(im, (M + 606, y), et, "b", 4, col, "l", 255 * u)
        p = pie.resize((pie.width * 6, pie.height * 6), Image.NEAREST)
        im.alpha_composite(p, (int(cx - p.width / 2), int(cy - p.height / 2)))
        return _salida(im, dt, dur)
    return fn


def pistas(ruta_a, ruta_b, items, titulo="¿Ditto = Mew fallido?", w=1400, h=500):
    """Dos Pokémon con «=?» en medio y las pistas debajo, una por marca con su casilla ✓."""
    n = len(items)

    def fn(dt, dur, marcas):
        im, M = _base(w, h, titulo, dt)
        mk = _marcas(marcas, n, .5, 1.4)
        for i, ruta in enumerate((ruta_a, ruta_b)):
            s = sprite(ruta, int(200 * min(1.0, _reb((dt - .1 - .2 * i) / .5)) or 2))
            cx = M + 170 + i * 380
            im.alpha_composite(s, (int(cx - s.width / 2), int(M + 70)))
        poner(im, (M + 360, M + 170), "=?", "t", 8, AMARILLO, "m", 255 * _eo((dt - .5) / .3))
        for i, it in enumerate(items):
            if dt < mk[i]:
                continue
            y = M + 110 + i * 100
            ImageDraw.Draw(im).rectangle((M + 690, y - 22, M + 734, y + 22), outline=LUZ + (255,), width=4)
            if dt > mk[i] + .3:
                palomita(im, M + 712, y)
            rica(im, M + 760, y, it, 3, BLANCO, AMARILLO, 255 * _eo((dt - mk[i]) / .3))
        return _salida(im, dt, dur)
    return fn


def sello(texto, color=ROJO):
    """Solo el sello (NO, MENTIRA, TEORÍA…) sobre el clip."""
    def fn(dt, dur, marcas):
        im = _capa(700, 320)
        _sello(im, 350, 160, texto, dt, color)
        return _bgra(im, min(1.0, (dur - dt) / .3))
    return fn


# ------------------------------------------------------------------ MG cortos de relleno (≥ 5 MG por minuto, regla del 3-nov)
def _gameboy(d, x, y, k=6, alfa=255):
    """Game Boy de píxel (gris, pantalla verde) con esquina superior izquierda en (x, y); 20×32 píxeles ×k."""
    d.rectangle((x, y, x + 20 * k, y + 32 * k), fill=(196, 196, 204, alfa), outline=(40, 40, 50, alfa), width=k)
    d.rectangle((x + 3 * k, y + 3 * k, x + 17 * k, y + 15 * k), fill=(90, 90, 110, alfa))
    d.rectangle((x + 5 * k, y + 5 * k, x + 15 * k, y + 13 * k), fill=CLA + (alfa,))
    d.rectangle((x + 3 * k, y + 21 * k, x + 7 * k, y + 22 * k), fill=(40, 40, 50, alfa))
    d.rectangle((x + 4 * k, y + 20 * k, x + 5 * k, y + 23 * k), fill=(40, 40, 50, alfa))
    d.ellipse((x + 13 * k, y + 20 * k, x + 15 * k, y + 22 * k), fill=(160, 30, 80, alfa))
    d.ellipse((x + 16 * k, y + 18 * k, x + 18 * k, y + 20 * k), fill=(160, 30, 80, alfa))


def cable(titulo="Cable link", w=1100, h=420):
    """Dos Game Boy unidos por el cable; una Poké Ball viaja de una pantalla a otra (ida y vuelta)."""
    def fn(dt, dur, marcas):
        im, M = _base(w, h, titulo, dt)
        d = ImageDraw.Draw(im)
        k = 7
        x1, x2, y = M + 90, M + w - 90 - 20 * k, M + 80
        _gameboy(d, x1, y, k)
        _gameboy(d, x2, y, k)
        u = _eo((dt - .2) / .6)
        pts = [(x1 + 10 * k, y), (x1 + 10 * k, y - 30), (x2 + 10 * k, y - 30), (x2 + 10 * k, y)]
        largo = (x2 - x1) * u
        d.line([pts[0], pts[1]], fill=(60, 60, 70, 255), width=10)
        d.line([pts[1], (pts[1][0] + largo, pts[1][1])], fill=(60, 60, 70, 255), width=10)
        if u >= 1:
            d.line([pts[2], pts[3]], fill=(60, 60, 70, 255), width=10)
            f = ((dt - .8) / 1.6) % 2
            f = f if f < 1 else 2 - f
            bx = pts[1][0] + (pts[2][0] - pts[1][0]) * _eo(f) if f < 1 else pts[2][0]
            b = pokeball(56)
            im.alpha_composite(b, (int(bx - 28), int(pts[1][1] - 28)))
        return _salida(im, dt, dur)
    return fn


def vida(nombre, nivel=None, de=1.0, a=0.0, titulo=None, w=760, h=170):
    """Caja de PS del enemigo de RB: NOMBRE, :Lnn y la barra que BAJA de `de` a `a` (verde → amarillo → rojo) durante el MG."""
    def fn(dt, dur, marcas):
        im, M = marco(w, h, 4)
        poner(im, (M + 40, M + 46), nombre, "t", 5, BLANCO, "l")
        if nivel:
            poner(im, (M + w - 40, M + 46), nivel, "m", 4, AMARILLO, "r")
        d = ImageDraw.Draw(im)
        v = de + (a - de) * _eo((dt - .5) / max(.6, dur - 1.4))
        col = (96, 208, 96) if v > .5 else (AMARILLO if v > .2 else ROJO)
        poner(im, (M + 40, M + 112), "PS:", "m", 4, AMARILLO, "l")
        d.rectangle((M + 150, M + 98, M + w - 40, M + 126), outline=LUZ + (255,), width=4)
        d.rectangle((M + 156, M + 104, M + 156 + (w - 202) * max(0.0, v), M + 120), fill=col + (255,))
        if titulo:
            pestana(im, M + 26, M + 2, titulo, 3, AMARILLO)
        return _salida(im, dt, dur)
    return fn


def cartel(texto, sub=None, k=6, color=BLANCO):
    """Cuadro de texto de RB con UNA frase grande que se escribe (y un subtítulo); ▼ al terminar. *x* = amarillo."""
    w = max(ancho_pix(texto, "t", k), ancho_pix(sub, "b", 4) if sub else 0) + 140
    h = 150 + (60 if sub else 0)

    def fn(dt, dur, marcas):
        im, M = marco(w, h, 5)
        n = max(0.0, (dt - .2) * 40)
        rica(im, M + 70, M + 78, texto, k, color, AMARILLO, 255, hasta=n, estilo="t")
        if sub and n > len(texto):
            poner(im, (M + 70, M + 150), sub, "b", 4, LUZ, "l", 255 * _eo((dt - .2 - len(texto) / 40) / .3))
        if n > len(texto.replace("*", "")):
            flecha(im, M + w - 70, M + h - 46, dt)
        return _salida(im, dt, dur)
    return fn


def quien(ruta, texto="¿Quién es ese Pokémon?", revela=False, w=760, h=620):
    """«¿Quién es ese Pokémon?»: la silueta NEGRA del Pokémon con rayos detrás; `revela` = a mitad del MG se ve en color."""
    def fn(dt, dur, marcas):
        im, M = _base(w, h, texto, dt)
        d = ImageDraw.Draw(im)
        cx, cy = M + w / 2, M + h / 2 + 10
        for i in range(16):                                # rayos que giran
            a0 = dt * .6 + i * math.pi / 8
            d.polygon([(cx, cy), (cx + 600 * math.cos(a0), cy + 600 * math.sin(a0)),
                       (cx + 600 * math.cos(a0 + .12), cy + 600 * math.sin(a0 + .12))], fill=(AMARILLO if i % 2 else CLA) + (70,))
        im2 = _capa(*im.size)
        im2.paste(im, (0, 0))
        im = im2
        s = sprite(ruta, int((h - 140) * min(1.0, _reb((dt - .2) / .5)) or 2))
        if not (revela and dt > dur / 2):
            neg = Image.new("RGBA", s.size, (12, 16, 12, 255))
            neg.putalpha(s.getchannel("A"))
            s = neg
        im.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))
        poner(im, (cx, M + h - 40), "?", "t", 9, AMARILLO, "m", 255 * (.6 + .4 * abs(math.sin(dt * 4))))
        im = im.crop((0, 0, w + 2 * M, h + 2 * M))
        return _salida(im, dt, dur)
    return fn


def exclama():
    """El «!» que sale sobre un entrenador cuando te ve (RB), con rebote."""
    def fn(dt, dur, marcas):
        im = _capa(150, 170)
        d = ImageDraw.Draw(im)
        r = _reb(dt / .35)
        k = 10 * min(1.0, r)
        if k > 1:
            d.rectangle((75 - 7 * k, 85 - 8 * k, 75 + 7 * k, 85 + 7 * k), fill=BLANCO + (255,), outline=OSC + (255,), width=4)
            d.rectangle((75 - k, 85 - 6 * k, 75 + k, 85 + 2 * k), fill=OSC + (255,))
            d.rectangle((75 - k, 85 + 3.5 * k, 75 + k, 85 + 5.5 * k), fill=OSC + (255,))
        return _bgra(im, min(1.0, (dur - dt) / .3))
    return fn


# ------------------------------------------------------------------ prueba
def _hoja(fn, dur, marcas, ruta, n=6, fondo=None):
    W, H = 640, 360
    hoja = Image.new("RGB", (W * 3, H * ((n + 2) // 3)), (40, 40, 40))
    for i in range(n):
        dt = dur * (i + .7) / n
        c = Image.new("RGB", (1920, 1080), (200, 200, 190)) if fondo is None else fondo.copy()
        a = fn(dt, dur, marcas)
        if a.shape[0] > 2:
            g = Image.fromarray(a[..., [2, 1, 0, 3]], "RGBA")
            c.paste(g, ((1920 - g.width) // 2, (1080 - g.height) // 2), g)
        hoja.paste(c.resize((W, H)), (W * (i % 3), H * (i // 3)))
    hoja.save(ruta, quality=80)


def _limites(fn, dur, marcas):
    """Llama al MG en sus instantes límite (lección de n64_secretos: un MG debe aguantar q≈0 y q≈1)."""
    for t in (0.0, 1 / 30, dur / 2, dur - 1 / 30, dur):
        fn(t, dur, marcas)


if __name__ == "__main__":
    import sys
    if "prueba" in sys.argv:
        d = os.environ.get("TMP_HOJAS", ".")
        peg = sys.argv[sys.argv.index("prueba") + 1] if len(sys.argv) > sys.argv.index("prueba") + 1 else None
        P = (lambda s: os.path.join(peg, s + ".png")) if peg else (lambda s: None)
        pruebas = [
            ("ficha", ficha("Satoshi Tajiri", "Fundó *Game Freak* como una revista hecha a mano sobre videojuegos, en 1983.", "GAME FREAK / 1983"), 6, []),
            ("puesto", puesto(20, "Te pusiste el nombre del creador"), 4, []),
            ("hud", hud(7), 3, []),
            ("linea", linea_tiempo([("1990", "Se presenta"), ("1996", "Rojo y Verde"), ("1998", "América"), ("1999", "Europa")], "Así nació"), 6, [.4, 1.4, 2.4, 3.4]),
            ("contador", contador("Ventas", [(10_000_000, "copias en Japón", "10 millones"), (31_000_000, "en el mundo", "31 millones")]), 5, [.3, 2.5]),
            ("nombres", nombres(), 6, [.4, 1.8, 3.4]),
            ("ranuras", ranuras(P("victreebel")), 6, [.3, 2.0, 3.6]),
            ("tabla", tabla_tipos(), 6, [.3, 2.0, 4.0]),
            ("foco", foco(), 6, [.3, 1.6, 3.0]),
            ("256", uno_de_256(), 4, [.3, 2.0]),
            ("mochila", mochila([("POCIÓN", 3), ("ANTÍDOTO", 2), ("SUPERBALL", 5), ("REPELENTE", 4), ("CUERDA HUIDA", 1), ("CARAMELORARO", 2)]), 5, [.3, 1.5, 2.6]),
            ("cartas", cartas(P("mew")), 6, [.3, 3.0]),
            ("bytes", bytes300(P("mew")), 6, [.3, 1.8, 3.3]),
            ("pastel", pastel([("Nintendo", AZUL), ("Game Freak", LUZ), ("Creatures", AMARILLO)]), 4, [.3, 1.0, 1.8]),
            ("mito", mito("Si usabas *Fuerza* en el camión, debajo aparecía Mew.", "Debajo no había *nada*.", "El rumor del camión", "MENTIRA"), 5, [.3, 2.4]),
            ("sello", sello("NO"), 2, []),
            ("cable", cable(), 4, []),
            ("vida", vida("TU PARTIDA", ":L99", 1.0, 0.0), 4, []),
            ("cartel", cartel("¡Un *MEW* salvaje!", "Solo con un truco"), 3, []),
            ("exclama", exclama(), 2, []),
        ]
        if peg:
            pruebas += [
                ("quien", quien(P("raichu"), "¿GOROCHU?"), 4, []),
                ("indice", indice(P("bulbasaur"), P("rhydon")), 5, [.3, 2.0]),
                ("equipo", equipo([(P("tauros"), "TAUROS", 66), (P("exeggutor"), "EXEGGUTOR", 67), (P("arcanine"), "ARCANINE", 68),
                                   (None, "INICIAL", 69), (P("gyarados"), "GYARADOS", 70)], "Equipo del Prof. Oak"), 6, [.3, .9, 1.5, 2.1, 2.7]),
                ("ataques", ataques("DRAGONITE de Lance", ["AGILIDAD", "GOLPE", "BARRERA", "HIPERRAYO"], "BARRERA", P("dragonite")), 5, [.3, 2.0]),
                ("pistas", pistas(P("ditto"), P("mew"), ["Mismo color *rosa*", "Los dos usan *Transformación*", "Dittos en la *Cueva Celeste*"]), 6, [.6, 2.0, 3.4]),
                ("dos", dos_versiones("La propuesta de América", ("Más músculo", None, "Pokémon *más fuertes* para EE. UU."),
                                      ("Yamauchi", P("pikachu"), "Pikachu se queda *redondito*"), sello_b="NO"), 5, [.3, 2.0]),
            ]
        for nom, fn, dur, mk in pruebas:
            _limites(fn, dur, mk)
            _hoja(fn, dur, mk, os.path.join(d, f"pk_{nom}.jpg"))
            print("ok", nom)
