# -*- coding: utf-8 -*-
"""MOTION GRAPHICS TRANSLÚCIDOS con la estética de RARE (Crónicas del gaming; primer uso `rare_auge_caida`, 28-oct-2026).
Video de un ESTUDIO, no de un juego: la interfaz de referencia es la del propio Rare — el oro del logo de Rareware de los
cartuchos de N64 y el teatro de Rare Replay (2015: telón, oro, luces de escenario) — sobre humo azul noche difuminado (regla
del 22-oct: nada de carteles opacos que tapen el video).
    import mg_rare as R
  ficha(titulo, texto, tipo)          humo azul noche + título en Copperplate oro + texto que se escribe; *x* = oro claro
  puesto(num, titulo, años)           cartel de CAPÍTULO: «CAPÍTULO N» con tracking, filete oro y «-título-» + los años
  pegatina(ruta, titulo, tam)         imagen REAL con borde blanco; nombre en píldora azul con filo oro
  eras(hitos)                         línea de tiempo del estudio: un hito por marca con su imagen real (logo, consola, juego)
  acciones(pasos)                     de quién es Rare: rejilla de 100 casillas que cambian de dueño (Stamper / Nintendo /
                                      Microsoft) con su logo, el % y, al final, el precio en un sello
  reparto(izq, der, centro)           el «divorcio» de 2002: medallones de personajes en fila que, uno por marca, se van al lado
                                      de su dueño (Nintendo / Rare-Microsoft)
  exodo(centro, destinos)             la fuga de talento: el medallón de Rare al centro y, una por marca, flechas que salen a los
                                      estudios nuevos (con su juego); el medallón se va apagando
  torres(items, unidad)               ventas: torres de cartuchos que crecen con el contador; la más alta se corona en oro
  apuesta(titulo, lado_a, lado_b)     balanza: lo que arriesgaron contra lo que ganaron (cada lado entra con una marca)
Probar SIEMPRE con una hoja de cuadros con marcas simuladas antes de `fx` (`python nucleo/mg_rare.py prueba`).
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

import mg_gaming as G

BLANCO, CREMA = (250, 250, 246), (232, 226, 210)
ORO, ORO_CLARO, ORO_OSC = (232, 186, 70), (255, 226, 140), (150, 108, 30)
AZUL, ROJO, VERDE = (110, 165, 255), (235, 40, 45), (95, 205, 90)
GRIS = (165, 170, 185)
NOCHE = (6, 10, 30)
_eo, _reb, _escala, _bgra = G._eo, G._reb, G._escala, G._bgra
_fc = {}
_D = ImageDraw.Draw(Image.new("RGBA", (8, 8)))
_FUENTES = {"c": "C:/Windows/Fonts/COPRGTB.TTF",      # Copperplate Gothic Bold: títulos grabados en oro
            "cl": "C:/Windows/Fonts/COPRGTL.TTF",
            "t": "C:/Windows/Fonts/segoeuib.ttf",     # texto
            "tn": "C:/Windows/Fonts/segoeui.ttf",
            "ti": "C:/Windows/Fonts/segoeuii.ttf",
            "n": "C:/Windows/Fonts/ROCKEB.TTF"}       # cifras grandes (Rockwell Extra Bold)


def fuente(estilo, tam):
    k = (estilo, int(tam))
    if k not in _fc:
        _fc[k] = ImageFont.truetype(_FUENTES[estilo], int(tam))
    return _fc[k]


def _vacio():
    return np.zeros((2, 2, 4), np.uint8)


def _ancho(s, f):
    return _D.textlength(s.replace("*", ""), font=f)


def _txt(d, xy, s, f, color, ancla="la", alfa=255, borde=0, track=0):
    a = int(max(0, min(255, alfa)))
    if a <= 0:
        return
    if track:
        x = xy[0]
        tot = sum(d.textlength(c, font=f) for c in s) + track * (len(s) - 1)
        if ancla[0] == "m":
            x -= tot / 2
        elif ancla[0] == "r":
            x -= tot
        for c in s:
            _txt(d, (x, xy[1]), c, f, color, "l" + ancla[1], alfa, borde)
            x += d.textlength(c, font=f) + track
        return
    d.text((xy[0] + 2, xy[1] + 3), s, font=f, fill=(0, 0, 0, int(a * .6)), anchor=ancla, stroke_width=borde,
           stroke_fill=(0, 0, 0, int(a * .6)))
    d.text(xy, s, font=f, fill=tuple(color) + (a,), anchor=ancla, stroke_width=borde, stroke_fill=(0, 0, 0, a))


def ajustar(s, estilo, tam, ancho, minimo=14):
    while tam > minimo and _ancho(s, fuente(estilo, tam)) > ancho:
        tam -= 1
    return fuente(estilo, tam)


def _partir(s, f, ancho):
    return G._partir(_D, s, f, ancho)


def caja(s, estilo, tam, ancho, interlinea=1.3, minimo=16, max_lineas=7):
    while True:
        f = fuente(estilo, tam)
        ls = _partir(s, f, ancho)
        if (len(ls) <= max_lineas and max(_ancho(x, f) for x in ls) <= ancho) or tam <= minimo:
            return f, ls, tam * interlinea
        tam -= 1


def _alfa(p, k):
    if k >= 1:
        return p
    a = np.array(p)
    a[..., 3] = (a[..., 3] * max(0.0, k)).astype(np.uint8)
    return Image.fromarray(a)


def _humo(w, h, M=46, alfa=.64, radio=30):
    """Panel azul noche translúcido, borde difuminado, con un brillo de foco de escenario arriba (capa aparte)."""
    im = Image.new("RGBA", (w + 2 * M, h + 2 * M), (0, 0, 0, 0))
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle((M, M, M + w, M + h), radio, fill=int(255 * alfa))
    m = m.filter(ImageFilter.GaussianBlur(8))
    capa = Image.new("RGBA", im.size, NOCHE + (255,))
    capa.putalpha(m)
    im.alpha_composite(capa)
    foco = Image.new("L", im.size, 0)
    ImageDraw.Draw(foco).ellipse((M + w * .2, M - h * .25, M + w * .8, M + h * .35), fill=38)
    foco = foco.filter(ImageFilter.GaussianBlur(40))
    luz = Image.new("RGBA", im.size, ORO_CLARO + (255,))
    luz.putalpha(Image.fromarray(np.minimum(np.array(foco), np.array(m))))
    im.alpha_composite(luz)
    return im, M


def _filete(d, x0, x1, y, alfa=255, color=ORO):
    """Línea oro que se apaga en los extremos + rombo central (como el adorno del logo de Rareware)."""
    n = 40
    for i in range(n):
        u0, u1 = i / n, (i + 1) / n
        k = math.sin(math.pi * (u0 + u1) / 2)
        d.line([(x0 + (x1 - x0) * u0, y), (x0 + (x1 - x0) * u1, y)], fill=color + (int(alfa * .9 * k),), width=2)
    cx = (x0 + x1) / 2
    d.polygon([(cx, y - 9), (cx + 9, y), (cx, y + 9), (cx - 9, y)], fill=ORO_CLARO + (int(alfa),))
    d.polygon([(cx, y - 4), (cx + 4, y), (cx, y + 4), (cx - 4, y)], fill=ORO_OSC + (int(alfa),))


def _texto_oro(s, f, track=0, borde=2):
    """Texto en oro degradado con contorno oscuro, como las letras del logo."""
    w = int(sum(_D.textlength(c, font=f) for c in s) + track * max(0, len(s) - 1) + 20)
    asc, desc = f.getmetrics()
    h = asc + desc + 16
    capa = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    d = ImageDraw.Draw(capa)
    x = 10
    for c in s:
        d.text((x, 8), c, font=f, fill=(255, 255, 255, 255), stroke_width=borde, stroke_fill=(40, 26, 0, 255))
        x += d.textlength(c, font=f) + track
    a = np.array(capa).astype(np.float32)
    yy = np.arange(h)[:, None]
    t = np.clip((yy - 8) / max(1, asc), 0, 1)
    top, mid, bot = np.array(ORO_CLARO), np.array(ORO), np.array(ORO_OSC)
    col = np.where(t[..., None] < .5, top + (mid - top) * (t[..., None] / .5), mid + (bot - mid) * ((t[..., None] - .5) / .5))
    claro = a[..., :3].mean(axis=2, keepdims=True) / 255.0      # el contorno (oscuro) se queda oscuro
    a[..., :3] = col * claro + np.array([40, 26, 0]) * (1 - claro)
    sombra = Image.new("RGBA", capa.size, (0, 0, 0, 0))
    sm = capa.split()[3].filter(ImageFilter.GaussianBlur(4))
    sombra.putalpha(Image.fromarray((np.array(sm) * .6).astype(np.uint8)))
    out = Image.new("RGBA", (w + 6, h + 6), (0, 0, 0, 0))
    out.alpha_composite(sombra, (4, 5))
    out.alpha_composite(Image.fromarray(a.astype(np.uint8)), (0, 0))
    return out


def _rica(d, x, y, s, f, color, resalte, alfa, ancla="l", hasta=None):
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


def _salida(im, dt, dur, abre=.32):
    """Entra como un telón que se abre en horizontal desde el centro; sale con fundido."""
    u = _eo(dt / abre)
    if u < 1:
        W, H = im.size
        w = max(2, int(W * (.2 + .8 * u)))
        p = im.resize((w, H), Image.BICUBIC)
        out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        out.alpha_composite(p, ((W - w) // 2, 0))
        im = out
    return _bgra(im, min(_eo(dt / .2), (dur - dt) / .35))


def _medallon(ruta, r, borde=ORO, gris=0.0):
    """Imagen real recortada en círculo con aro oro (y sombra). gris 0..1 = se apaga."""
    s = 2 * r
    lien = Image.new("RGBA", (s + 24, s + 24), (0, 0, 0, 0))
    if ruta and os.path.exists(ruta):
        x = Image.open(ruta).convert("RGBA")
        # fondo azul noche bajo PNG con transparencia
        fondo = Image.new("RGBA", x.size, (20, 28, 60, 255))
        fondo.alpha_composite(x)
        x = fondo
        lado = min(x.size)
        x = x.crop(((x.width - lado) // 2, (x.height - lado) // 4 if x.height > x.width else 0,
                    (x.width - lado) // 2 + lado, ((x.height - lado) // 4 if x.height > x.width else 0) + lado))
        x = x.resize((s, s), Image.LANCZOS)
    else:
        x = Image.new("RGBA", (s, s), (20, 28, 60, 255))
    if gris > 0:
        a = np.array(x).astype(np.float32)
        g = a[..., :3].mean(axis=2, keepdims=True)
        a[..., :3] = a[..., :3] * (1 - gris) + g * gris * .7
        x = Image.fromarray(a.astype(np.uint8))
    m = Image.new("L", (s, s), 0)
    ImageDraw.Draw(m).ellipse((0, 0, s - 1, s - 1), fill=255)
    x.putalpha(m)
    sh = Image.new("L", lien.size, 0)
    ImageDraw.Draw(sh).ellipse((10, 14, s + 14, s + 18), fill=150)
    sh = sh.filter(ImageFilter.GaussianBlur(6))
    sombra = Image.new("RGBA", lien.size, (0, 0, 0, 255))
    sombra.putalpha(sh)
    lien.alpha_composite(sombra)
    lien.alpha_composite(x, (12, 12))
    d = ImageDraw.Draw(lien)
    col = tuple(int(c * (1 - gris) + 120 * gris) for c in borde)
    d.ellipse((10, 10, s + 13, s + 13), outline=col + (255,), width=5)
    d.ellipse((15, 15, s + 8, s + 8), outline=(255, 240, 190, 90), width=1)
    return lien


def _img(ruta, caja_):
    if not ruta or not os.path.exists(ruta):
        return None
    x = Image.open(ruta).convert("RGBA")
    x.thumbnail(caja_, Image.LANCZOS)
    return x


# ------------------------------------------------------------------ ficha
def ficha(titulo, texto, tipo=None, ancho=880, vel=55):
    in_w = ancho - 2 * 50
    ft = ajustar(titulo.upper(), "c", 40, in_w)
    fty = ajustar(tipo, "ti", 27, in_w) if tipo else None
    fx, ls, lh = caja(texto, "t", 34, in_w)
    h = int(36 + 46 + (36 if tipo else 0) + 26 + lh * len(ls) + 36)
    base, M = _humo(ancho, h)
    tit = _texto_oro(titulo.upper(), ft, track=2)
    letras = [len(x.replace("*", "")) for x in ls]

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        cx = M + ancho / 2
        y = M + 42
        a = _eo((dt - .18) / .3)
        if a > 0:
            im.alpha_composite(_alfa(tit, a), (int(cx - tit.width / 2), int(y - tit.height / 2)))
        y += 42
        if tipo:
            _txt(d, (cx, y), tipo, fty, GRIS, "mm", 235 * _eo((dt - .3) / .3))
            y += 36
        _filete(d, M + 70, M + ancho - 70, y, 255 * _eo((dt - .3) / .4))
        y += 26 + lh / 2
        quedan = max(0.0, (dt - .45) * vel)
        for ln, n in zip(ls, letras):
            _rica(d, cx, y, ln, fx, BLANCO, ORO_CLARO, 255, "m", hasta=quedan)
            quedan -= n
            y += lh
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ capítulo
def puesto(num, titulo, años=None, arriba=None):
    """Cartel de capítulo: «CAPÍTULO N» en oro con tracking que se cierra, filete, «-título-» y los años en gris."""
    arriba = arriba or f"Capítulo {num}"
    w, h = 1500, 270 if años else 220
    f1 = ajustar(arriba.upper(), "c", 78, w - 200)
    f2 = ajustar(f"-{titulo}-", "t", 44, w - 220)
    f3 = fuente("cl", 30)
    base, M = _humo(w, h, alfa=.56, radio=60)
    cache = {}

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        cx = M + w / 2
        u = _eo((dt - .05) / .9)
        tr = int(26 * (1 - u)) + 4
        if tr not in cache:
            cache[tr] = _texto_oro(arriba.upper(), f1, track=tr, borde=2)
        t = cache[tr]
        im.alpha_composite(_alfa(t, u), (int(cx - t.width / 2), int(M + 84 - t.height / 2)))
        _filete(d, cx - 320 * u, cx + 320 * u, M + 140, 255 * u)
        _txt(d, (cx, M + 180), f"-{titulo}-", f2, CREMA, "mm", 255 * _eo((dt - .55) / .5))
        if años:
            _txt(d, (cx, M + 234), años, f3, GRIS, "mm", 230 * _eo((dt - .75) / .5), track=6)
        # destello que barre el oro
        g = (dt - .9) / .7
        if 0 < g < 1:
            capa = Image.new("RGBA", im.size, (0, 0, 0, 0))
            dc = ImageDraw.Draw(capa)
            x = M + w * (.15 + .7 * g)
            dc.polygon([(x - 70, M + 40), (x + 30, M + 40), (x - 30, M + 130), (x - 130, M + 130)], fill=(255, 250, 220, 34))
            capa = capa.filter(ImageFilter.GaussianBlur(22))
            im.alpha_composite(capa)
        return _bgra(im, min(_eo(dt / .35), (dur - dt) / .5))
    return fn


# ------------------------------------------------------------------ pegatina
def pegatina(ruta, titulo=None, tam=360, giro=-6.0):
    import mg_tes as T
    base = T._base_pegatina(ruta, tam)
    if titulo:
        tit = titulo.upper()
        f = ajustar(tit, "t", 30, max(260, base.width + 40))
        pw, ph = int(_ancho(tit, f) + 56), 62
        pil = Image.new("RGBA", (pw, ph), (0, 0, 0, 0))
        dp = ImageDraw.Draw(pil)
        dp.rounded_rectangle((0, 0, pw - 1, ph - 1), ph // 2, fill=NOCHE + (200,), outline=ORO + (240,), width=3)
        _txt(dp, (pw / 2, ph / 2 + 1), tit, f, BLANCO, "mm", 255)
        lien = Image.new("RGBA", (max(base.width, pw), base.height + ph // 2), (0, 0, 0, 0))
        lien.alpha_composite(base, ((lien.width - base.width) // 2, 0))
        lien.alpha_composite(pil, ((lien.width - pw) // 2, base.height - ph // 2))
        base = lien

    def fn(dt, dur, marcas):
        s = T._pop(dt, .42)
        if s <= 0.02:
            return _vacio()
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


# ------------------------------------------------------------------ línea de tiempo del estudio
def eras(hitos, titulo="Rare", w=1680):
    """hitos = [(año, texto, ruta_imagen o None)]; marca k = aparece el hito k. La línea se dibuja en oro y el último
    hito late. Si hay más de 6, la línea se desplaza para que el último quede a la vista."""
    n = len(hitos)
    h = 400
    base, Mg = _humo(w, h, alfa=.56)
    ims = [_img(r, (200, 120)) for _, _, r in hitos]
    fa, ftx = fuente("n", 44), fuente("t", 25)
    tit = _texto_oro(titulo.upper(), fuente("c", 34), track=3)
    vis = min(n, 6)
    paso = (w - 220) / max(1, vis - 1)

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        im.alpha_composite(_alfa(tit, _eo(dt / .3)), (int(Mg + w / 2 - tit.width / 2), Mg + 14))
        y = Mg + 215
        mk = list(marcas) + [dur + 1] * (n - len(marcas))
        ult = max([k for k in range(n) if dt >= mk[k] - .05] or [-1])
        # desplazamiento suave para que el último hito quede dentro
        objetivo = max(0, ult - (vis - 1))
        desde = max(0, ult - 1 - (vis - 1))
        off = desde + (objetivo - desde) * _eo((dt - (mk[ult] if ult >= 0 else 0)) / .6)
        x0 = Mg + 110 - off * paso
        xf = x0 + paso * max(0, ult) * (_eo((dt - (mk[ult] if ult >= 0 else 0)) / .5) if ult > 0 else 1)
        if ult >= 0:
            d.line([(max(Mg + 60, x0), y), (min(Mg + w - 60, xf), y)], fill=ORO + (210,), width=4)
        for k, (año, texto, _) in enumerate(hitos):
            u = (dt - mk[k]) / .45
            if u <= 0:
                continue
            x = x0 + paso * k
            if x < Mg + 40 or x > Mg + w - 40:
                continue
            borde_a = min(1.0, (x - Mg - 40) / 80, (Mg + w - 40 - x) / 80)
            s = _reb(u)
            r = 13 * s * (1 + (.25 * math.sin(dt * 5) if k == ult else 0))
            a = 255 * _eo(u) * borde_a
            d.ellipse((x - r, y - r, x + r, y + r), fill=ORO + (int(a),), outline=BLANCO + (int(a),), width=3)
            _txt(d, (x, y + 50), año, fa, BLANCO, "mm", a)
            for j, ln in enumerate(_partir(texto, ftx, paso - 20)[:2]):
                _txt(d, (x, y + 94 + j * 30), ln, ftx, CREMA, "mm", a)
            if ims[k] is not None:
                ic = ims[k]
                k2 = max(.05, s)
                ic2 = ic.resize((max(2, int(ic.width * k2)), max(2, int(ic.height * k2))), Image.BICUBIC)
                im.alpha_composite(_alfa(ic2, _eo(u) * borde_a), (int(x - ic2.width / 2), int(y - 28 - ic2.height)))
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ de quién es Rare
def acciones(pasos, titulo="¿De quién es Rare?", precio=None, w=1300):
    """Rejilla de 10×10 = 100 % de Rare. pasos = [(dueño, %, color, ruta_logo)] acumulados por marca: en la marca k, las
    primeras `%` casillas pasan al color de ese dueño (en cascada) y su logo/porcentaje entra a la derecha. `precio` =
    (texto, sub) estampado como sello en la última marca."""
    h = 640
    base, Mg = _humo(w, h, alfa=.6)
    tit = _texto_oro(titulo.upper(), fuente("c", 38), track=2)
    logos = [_img(r, (170, 80)) for *_, r in pasos]
    fp, fs = fuente("n", 64), fuente("t", 28)
    lado, gap = 44, 6
    gx, gy = Mg + 80, Mg + 110

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        im.alpha_composite(_alfa(tit, _eo(dt / .3)), (int(Mg + w / 2 - tit.width / 2), Mg + 18))
        mk = list(marcas) + [dur + 1] * (len(pasos) + 1 - len(marcas))
        # color de cada casilla: el último paso que la alcanzó
        for i in range(100):
            fila, col = divmod(i, 10)
            x, y = gx + col * (lado + gap), gy + fila * (lado + gap)
            c, a = (60, 80, 140), 150
            for k, (_, pct, color, _) in enumerate(pasos):
                u = (dt - mk[k] - i * .012) / .25
                if i < pct and u > 0:
                    c = tuple(int(c[j] + (color[j] - c[j]) * min(1, u)) for j in range(3))
                    a = 235
            d.rounded_rectangle((x, y, x + lado, y + lado), 7, fill=c + (a,))
        # leyenda a la derecha
        lx = gx + 10 * (lado + gap) + 70
        for k, (dueño, pct, color, _) in enumerate(pasos):
            u = (dt - mk[k]) / .4
            if u <= 0:
                continue
            a = 255 * _eo(u)
            # el paso vigente brilla, los anteriores bajan
            vig = all(dt < mk[j] for j in range(k + 1, len(pasos)))
            a2 = a if vig else a * .45
            yy = gy + 30 + k * 120
            if logos[k] is not None:
                im.alpha_composite(_alfa(logos[k], _eo(u) * (1 if vig else .45)), (int(lx), int(yy)))
                tx = lx + logos[k].width + 22
            else:
                tx = lx
            _txt(d, (tx, yy + 24), f"{pct} %", fp, color, "lm", a2, borde=2)
            _txt(d, (tx, yy + 78), dueño, fs, CREMA, "lm", a2)
        if precio and len(marcas) > len(pasos):
            u = (dt - mk[len(pasos)]) / .35
            if u > 0:
                s = 1.8 - .8 * _eo(u)
                sello = Image.new("RGBA", (520, 200), (0, 0, 0, 0))
                ds = ImageDraw.Draw(sello)
                ds.rounded_rectangle((8, 8, 512, 192), 22, fill=NOCHE + (225,), outline=VERDE + (255,), width=8)
                _txt(ds, (260, 82), precio[0], fuente("n", 70), VERDE, "mm", 255, borde=2)
                _txt(ds, (260, 150), precio[1], fuente("t", 30), BLANCO, "mm", 255)
                sello = sello.rotate(-8, resample=Image.BICUBIC, expand=True)
                sello = sello.resize((int(sello.width * s), int(sello.height * s)), Image.BICUBIC)
                im.alpha_composite(_alfa(sello, _eo(u)), (int(gx + 5 * (lado + gap) - sello.width / 2), int(gy + 5 * (lado + gap) - sello.height / 2)))
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ el reparto de 2002
def reparto(izq, der, items, titulo="El reparto", w=1720):
    """izq/der = (nombre, ruta_logo, color). items = [(nombre, ruta_imagen, lado 'i'|'d')]. Al empezar los medallones están en
    fila al centro; en la marca k el item k se va con un arco a su lado y su nombre se escribe debajo. Una raya vertical
    parte el panel en dos (se abre con la marca 0)."""
    n = len(items)
    h = 640
    base, Mg = _humo(w, h, alfa=.6)
    tit = _texto_oro(titulo.upper(), fuente("c", 38), track=2)
    meds = [_medallon(r, 62) for _, r, _ in items]
    lg = [_img(izq[1], (220, 90)), _img(der[1], (220, 90))]
    fn_, fl = fuente("t", 24), fuente("c", 30)
    destinos = {"i": [], "d": []}
    for k, (_, _, lado) in enumerate(items):
        destinos[lado].append(k)

    def pos_final(k):
        lado = items[k][2]
        j = destinos[lado].index(k)
        m = len(destinos[lado])
        cols = min(3, m)
        fila, col = divmod(j, cols)
        cx = Mg + (w * .25 if lado == "i" else w * .75)
        x = cx + (col - (cols - 1) / 2) * 175
        y = Mg + 270 + fila * 180
        return x, y

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        im.alpha_composite(_alfa(tit, _eo(dt / .3)), (int(Mg + w / 2 - tit.width / 2), Mg + 14))
        t0 = marcas[0] if marcas else .6
        u0 = _eo((dt - t0 + .4) / .6)
        for k, (nom, ruta, color) in enumerate((izq, der)):
            cx = Mg + (w * .25 if k == 0 else w * .75)
            a = 255 * u0
            if lg[k] is not None:
                im.alpha_composite(_alfa(lg[k], u0), (int(cx - lg[k].width / 2), Mg + 82))
                _txt(d, (cx, Mg + 192), nom.upper(), fl, color, "mm", a, track=2)
            else:
                _txt(d, (cx, Mg + 130), nom.upper(), fl, color, "mm", a, track=2)
        d.line([(Mg + w / 2, Mg + 90), (Mg + w / 2, Mg + 90 + (h - 130) * u0)], fill=ORO + (int(170 * u0),), width=3)
        mk = list(marcas) + [dur + 1] * (n - len(marcas))
        for k in range(n):
            # posición inicial: fila al centro, abajo
            x0 = Mg + w / 2 + (k - (n - 1) / 2) * min(150, (w - 200) / max(1, n))
            y0 = Mg + h - 110
            xf, yf = pos_final(k)
            u = _eo((dt - mk[k]) / .8)
            x = x0 + (xf - x0) * u
            y = y0 + (yf - y0) * u - math.sin(math.pi * u) * 120
            ent = _reb(dt / .5 - k * .06)
            if ent <= .02:
                continue
            m = meds[k]
            s = (.62 + .38 * u) * ent
            m2 = m.resize((max(2, int(m.width * s)), max(2, int(m.height * s))), Image.BICUBIC)
            im.alpha_composite(m2, (int(x - m2.width / 2), int(y - m2.height / 2)))
            if u > .6:
                _txt(d, (x, y + 80), items[k][0], fn_, BLANCO, "mm", 255 * _eo((u - .6) / .4))
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ la fuga de talento
def exodo(centro, destinos, titulo="La fuga de talento", w=1720):
    """centro = (nombre, ruta_logo). destinos = [(estudio, año, ruta_imagen, texto)]: en la marca k sale una flecha oro desde
    el medallón central hasta el destino k (repartidos en abanico arriba), entra su medallón y su texto. El medallón central
    se apaga un poco con cada salida."""
    n = len(destinos)
    h = 700
    base, Mg = _humo(w, h, alfa=.6)
    tit = _texto_oro(titulo.upper(), fuente("c", 38), track=2)
    meds = [_medallon(r, 64) for _, _, r, _ in destinos]
    fe, fa, ft = fuente("t", 28), fuente("n", 30), fuente("tn", 24)
    cx, cy = Mg + w / 2, Mg + h - 150
    cache_c = {}

    def pos(k):
        ang = math.pi * (.12 + .76 * (k / max(1, n - 1))) if n > 1 else math.pi / 2
        return cx - math.cos(ang) * w * .40, cy - math.sin(ang) * (h * .50)

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        im.alpha_composite(_alfa(tit, _eo(dt / .3)), (int(Mg + w / 2 - tit.width / 2), Mg + 14))
        mk = list(marcas) + [dur + 1] * (n - len(marcas))
        salidos = sum(1 for k in range(n) if dt >= mk[k])
        gris = min(.75, salidos / max(1, n) * .75)
        g = round(gris, 2)
        if g not in cache_c:
            cache_c[g] = _medallon(centro[1], 92, gris=g)
        c = cache_c[g]
        s = _reb(dt / .5)
        if s > .02:
            c2 = c.resize((max(2, int(c.width * s)), max(2, int(c.height * s))), Image.BICUBIC)
            im.alpha_composite(c2, (int(cx - c2.width / 2), int(cy - c2.height / 2)))
            _txt(d, (cx, cy + 118), centro[0].upper(), fuente("c", 30), ORO, "mm", 255 * _eo(dt / .4), track=2)
        for k, (estudio, año, _, texto) in enumerate(destinos):
            u = (dt - mk[k]) / .7
            if u <= 0:
                continue
            x1, y1 = pos(k)
            p = _eo(u)
            xa, ya = cx + (x1 - cx) * .22, cy + (y1 - cy) * .22
            xb, yb = xa + (x1 - xa) * p * .78, ya + (y1 - ya) * p * .78
            d.line([(xa, ya), (xb, yb)], fill=ORO + (220,), width=5)
            ang = math.atan2(yb - ya, xb - xa)
            for sgn in (-1, 1):
                d.line([(xb, yb), (xb - 22 * math.cos(ang + sgn * .5), yb - 22 * math.sin(ang + sgn * .5))],
                       fill=ORO + (220,), width=5)
            e = _reb((u - .6) / .6)
            if e > .02:
                m = meds[k].resize((max(2, int(meds[k].width * e)), max(2, int(meds[k].height * e))), Image.BICUBIC)
                im.alpha_composite(m, (int(x1 - m.width / 2), int(y1 - m.height / 2)))
                a = 255 * _eo((u - .8) / .4)
                _txt(d, (x1, y1 + 88), estudio, fe, BLANCO, "mm", a)
                _txt(d, (x1, y1 + 122), año, fa, ORO_CLARO, "mm", a)
                for j, ln in enumerate(_partir(texto, ft, 300)[:2]):
                    _txt(d, (x1, y1 + 156 + j * 28), ln, ft, CREMA, "mm", a)
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ torres de ventas
def torres(items, titulo="Copias vendidas", unidad="millones", w=1560):
    """items = [(juego, cifra, ruta_imagen)]. Marca k = crece la torre k (bloques como cartuchos apilados) con su contador;
    tras la última marca la más alta se corona en oro y late."""
    n = len(items)
    h = 640
    base, Mg = _humo(w, h, alfa=.6)
    tit = _texto_oro(titulo.upper(), fuente("c", 38), track=2)
    ims = [_img(r, (150, 110)) for *_, r in items]
    tope = max(c for _, c, _ in items)
    fn_, fj, fu = fuente("n", 46), fuente("t", 24), fuente("tn", 24)
    ancho_t = min(170, (w - 200) / n - 40)
    alto_max = h - 330
    imax = max(range(n), key=lambda k: items[k][1])

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        im.alpha_composite(_alfa(tit, _eo(dt / .3)), (int(Mg + w / 2 - tit.width / 2), Mg + 14))
        mk = list(marcas) + [dur + 1] * (n - len(marcas))
        suelo = Mg + h - 120
        d.line([(Mg + 60, suelo), (Mg + w - 60, suelo)], fill=ORO + (150,), width=2)
        fin = all(dt >= m for m in mk[:n]) and dt >= mk[n - 1] + 1.2
        for k, (juego, cifra, _) in enumerate(items):
            x = Mg + 100 + (k + .5) * (w - 200) / n
            u = _eo((dt - mk[k]) / 1.1)
            if dt < mk[k] - .3:
                continue
            alto = alto_max * cifra / tope * u
            bloque = 34
            nb = int(alto // bloque)
            corona = fin and k == imax
            col = ORO if corona else (90, 130, 230)
            for b in range(nb):
                y1 = suelo - b * bloque - 3
                d.rounded_rectangle((x - ancho_t / 2, y1 - bloque + 5, x + ancho_t / 2, y1), 6,
                                    fill=col + (215,), outline=(255, 255, 255, 70), width=1)
                d.rectangle((x - ancho_t / 2 + 14, y1 - bloque + 12, x + ancho_t / 2 - 14, y1 - 8), fill=(255, 255, 255, 40))
            resto = alto - nb * bloque
            if resto > 2:
                y1 = suelo - nb * bloque - 3
                d.rounded_rectangle((x - ancho_t / 2, y1 - resto, x + ancho_t / 2, y1), 6, fill=col + (215,))
            ytop = suelo - alto - 10
            val = cifra * u
            s = f"{val:.1f}".replace(".", ",")
            puls = 1 + (.08 * math.sin(dt * 6) if corona else 0)
            ftam = fuente("n", int(46 * puls))
            _txt(d, (x, ytop - 30), s, ftam, ORO_CLARO if corona else BLANCO, "mm", 255 * _eo((dt - mk[k]) / .3), borde=2)
            a = 255 * _eo((dt - mk[k] + .3) / .4)
            if ims[k] is not None:
                ic = ims[k]
                im.alpha_composite(_alfa(ic, a / 255), (int(x - ic.width / 2), int(suelo + 8)))
            for j, ln in enumerate(_partir(juego, fj, ancho_t + 40)[:2]):
                _txt(d, (x, suelo + (124 if ims[k] is not None else 24) + j * 28), ln, fj, CREMA, "mm", a)
        _txt(d, (Mg + w - 70, Mg + 50), unidad, fu, GRIS, "rm", 230 * _eo(dt / .4))
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .4))
    return fn


# ------------------------------------------------------------------ la apuesta
def apuesta(titulo, lado_a, lado_b, w=1400):
    """Balanza: lado_a = (título, texto, ruta) entra en la marca 0 y hunde su platillo; lado_b en la marca 1 y la balanza
    se inclina a su favor (lo que ganaron pesa más)."""
    h = 600
    base, Mg = _humo(w, h, alfa=.6)
    tit = _texto_oro(titulo.upper(), fuente("c", 38), track=2)
    ia, ib = _img(lado_a[2], (230, 170)), _img(lado_b[2], (230, 170))
    ft, fx = fuente("c", 30), fuente("t", 26)

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        im.alpha_composite(_alfa(tit, _eo(dt / .3)), (int(Mg + w / 2 - tit.width / 2), Mg + 14))
        t0 = marcas[0] if marcas else .5
        t1 = marcas[1] if len(marcas) > 1 else dur * .6
        ang = 0.0
        ang += -.13 * _reb((dt - t0) / .8) if dt > t0 else 0
        ang += .26 * _reb((dt - t1) / .9) if dt > t1 else 0
        ang += .015 * math.sin(dt * 2.2)
        cx, cy = Mg + w / 2, Mg + 170
        L = w * .32
        d.polygon([(cx - 30, Mg + h - 60), (cx + 30, Mg + h - 60), (cx + 6, cy), (cx - 6, cy)], fill=ORO_OSC + (230,))
        xa, ya = cx - L * math.cos(ang), cy - L * math.sin(ang) * -1
        xb, yb = cx + L * math.cos(ang), cy + L * math.sin(ang) * -1
        ya, yb = cy + L * math.sin(-ang), cy - L * math.sin(-ang)
        d.line([(xa, ya), (xb, yb)], fill=ORO + (255,), width=8)
        d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), fill=ORO_CLARO + (255,))
        for k, (x, y, lado, ic, tm) in enumerate(((xa, ya, lado_a, ia, t0), (xb, yb, lado_b, ib, t1))):
            py = y + 150
            d.line([(x, y), (x - 110, py)], fill=ORO + (200,), width=3)
            d.line([(x, y), (x + 110, py)], fill=ORO + (200,), width=3)
            d.arc((x - 130, py - 40, x + 130, py + 40), 0, 180, fill=ORO + (255,), width=6)
            u = (dt - tm) / .5
            if u > 0:
                a = _eo(u)
                if ic is not None:
                    im.alpha_composite(_alfa(ic, a), (int(x - ic.width / 2), int(py - ic.height + 10 - 30 * (1 - a))))
                _txt(d, (x, py + 70), lado[0].upper(), ft, ROJO if k == 0 else VERDE, "mm", 255 * a, track=2)
                for j, ln in enumerate(_partir(lado[1], fx, 420)[:2]):
                    _txt(d, (x, py + 110 + j * 32), ln, fx, CREMA, "mm", 255 * a)
        return _bgra(im, min(_eo(dt / .25), (dur - dt) / .4))
    return fn


if __name__ == "__main__":
    import sys
    if sys.argv[1:] == ["prueba"]:
        fondo = np.full((1080, 1920, 3), (60, 90, 70), np.uint8)
        pruebas = [
            ("ficha", ficha("Donkey Kong Country", "Vendió *9,3 millones* de copias en Super Nintendo.", tipo="1994"), [], 3.0),
            ("puesto", puesto(3, "La apuesta de las estaciones", "1993 - 1996"), [], 2.5),
            ("eras", eras([("1982", "Ultimate Play the Game", None), ("1985", "Rare y la NES", None),
                           ("1994", "Donkey Kong Country", None), ("1997", "GoldenEye 007", None),
                           ("2002", "Microsoft", None), ("2010", "Kinect Sports", None), ("2018", "Sea of Thieves", None)]),
             [.5, 1, 1.5, 2, 2.5, 3, 3.5], 5.0),
            ("acciones", acciones([("Hermanos Stamper", 100, AZUL, None), ("Nintendo", 49, ROJO, None),
                                   ("Microsoft", 100, VERDE, None)], precio=("375 M US$", "septiembre de 2002")),
             [.3, 1.5, 3, 4], 5.5),
            ("reparto", reparto(("Nintendo", None, ROJO), ("Rare / Microsoft", None, VERDE),
                                [("Donkey Kong", None, "i"), ("Banjo", None, "d"), ("Conker", None, "d"), ("Fox McCloud", None, "i"),
                                 ("Joanna Dark", None, "d")]), [.5, 1.2, 1.9, 2.6, 3.3], 5.0),
            ("exodo", exodo(("Rare", None), [("Free Radical", "1999", None, "TimeSplitters"),
                                            ("Playtonic", "2014", None, "Yooka-Laylee"), ("Otro", "2005", None, "x")]),
             [.6, 1.4, 2.2], 4.0),
            ("torres", torres([("Donkey Kong Country", 9.3, None), ("GoldenEye 007", 8.1, None), ("Banjo-Kazooie", 3.6, None)]),
             [.3, 1, 1.7], 4.5),
            ("apuesta", apuesta("La apuesta", ("Lo que arriesgaron", "Estaciones Silicon Graphics", None),
                                ("Lo que ganaron", "9,3 millones de copias", None)), [.5, 1.8], 3.5),
        ]
        os.makedirs("previews", exist_ok=True)
        for nom, f, mk, dur in pruebas:
            celdas = []
            for t in np.linspace(.2, dur - .3, 6):
                a = f(float(t), dur, mk)
                lien = fondo.copy()
                if a.shape[0] > 2:
                    hh, ww = min(1080, a.shape[0]), min(1920, a.shape[1])
                    a = a[:hh, :ww]
                    y0, x0 = (1080 - hh) // 2, (1920 - ww) // 2
                    al = a[..., 3:4] / 255.0
                    zona = lien[y0:y0 + hh, x0:x0 + ww].astype(np.float32)
                    lien[y0:y0 + hh, x0:x0 + ww] = (zona * (1 - al) + a[..., [2, 1, 0]] * al).astype(np.uint8)
                celdas.append(Image.fromarray(lien).resize((640, 360)))
            hoja = Image.new("RGB", (1920, 720))
            for i, c in enumerate(celdas):
                hoja.paste(c, ((i % 3) * 640, (i // 3) * 360))
            hoja.save(f"previews/mg_rare_{nom}.jpg", quality=82)
            print("previews/mg_rare_" + nom + ".jpg")
