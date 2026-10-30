# -*- coding: utf-8 -*-
"""MOTION GRAPHICS TRANSLÚCIDOS con la interfaz de SUPER MARIO 64 (Crónicas del gaming; primer uso `mario64_secretos`, 29-oct-2026).
Regla del usuario del 22-oct: fichas translúcidas como las de Tamriel, pero con la interfaz de CADA juego. Aquí la de Mario 64:
  - el CUADRO DE DIÁLOGO del juego (los letreros y Toad): caja negra translúcida, texto blanco que se escribe letra a letra y el
    triángulo rojo de «siguiente» que late;
  - la PANTALLA DE SELECCIÓN DE ESTRELLA como rótulo de cada secreto: la Estrella de poder dorada (con sus ojos) que gira sobre
    su eje, «SECRETO N.º N» en las letras de colores del logo (rojo, amarillo, verde, azul con contorno) y el título debajo;
  - el HUD: «★ × N», monedas y el medidor de energía en forma de tarta de 8 gajos.
Todo sobre humo negro difuminado (alfa ≤ ~0,7): el gameplay se sigue viendo detrás.
    import mg_mario64 as M
  ficha(titulo, texto, tipo)          cuadro de diálogo; *x* = amarillo moneda
  puesto(num, titulo)                 selección de estrella: estrella que gira + «SECRETO N.º N» + -título-
  pegatina(ruta, titulo, tam)         imagen REAL con borde blanco; nombre en píldora negra con filo dorado
  estrellas(titulo, total, pasos)     contador del HUD «★ × N» que sube por tramos; un paso por marca (valor, texto)
  linea_tiempo(hitos, titulo)         cronología del desarrollo; un hito por marca; el último late
  (los MG propios del guion van más abajo, cada uno con su docstring)
Probar SIEMPRE con una hoja de cuadros antes de `fx` (python nucleo/mg_mario64.py prueba).
"""
import math
import os

import numpy as np
from PIL import Image, ImageDraw, ImageFilter

import mg_majora as MJ
from mg_majora import ajustar, caja, fuente

BLANCO, CREMA, GRIS = (250, 250, 248), (236, 230, 214), (175, 175, 182)
ORO, ORO_CLARO, ORO_OSC = (255, 206, 30), (255, 240, 150), (214, 128, 10)
ROJO, AZUL, VERDE, AMARILLO = (232, 40, 40), (46, 98, 232), (40, 176, 70), (255, 214, 0)
LOGO = [ROJO, AMARILLO, VERDE, AZUL]                 # colores de las letras del logo de Super Mario 64
_eo, _reb, _bgra, _txt, _humo, _salida, _rica = MJ._eo, MJ._reb, MJ._bgra, MJ._txt, MJ._humo, MJ._salida, MJ._rica
_D = ImageDraw.Draw(Image.new("RGBA", (8, 8)))


def _capa(w, h):
    return Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0))


# ------------------------------------------------------------------ piezas
def letras_logo(d, xy, s, f, alfa=255, ancla="m", fase=0.0, salto=0.0):
    """Texto con las letras alternando los colores del logo de Super Mario 64, contorno negro grueso y brillo blanco arriba.
    `salto` > 0 = cada letra rebota un poco (ola), como el logo de la pantalla de título."""
    s = MJ._limpia(s)
    tot = sum(d.textlength(c, font=f) for c in s)
    x = xy[0] - (tot / 2 if ancla == "m" else 0)
    a = int(max(0, min(255, alfa)))
    k = 0
    for i, c in enumerate(s):
        w = d.textlength(c, font=f)
        if c.strip():
            col = LOGO[k % 4]
            k += 1
            y = xy[1] - salto * max(0.0, math.sin(fase * 5 - i * .55))
            d.text((x + 3, y + 5), c, font=f, fill=(0, 0, 0, int(a * .6)), anchor="lm", stroke_width=6,
                   stroke_fill=(0, 0, 0, int(a * .6)))
            d.text((x, y), c, font=f, fill=col + (a,), anchor="lm", stroke_width=5, stroke_fill=(16, 10, 6, a))
        x += w


def estrella(tam, giro=0.0, ojos=True, brillo=1.0):
    """La Estrella de poder: 5 puntas doradas con estrella interior clara, contorno naranja y dos ojos negros alargados.
    `giro` en radianes: el ancho = |cos| (gira sobre su eje vertical); de espaldas no se ven los ojos."""
    S = int(tam)
    im = _capa(S, S)
    d = ImageDraw.Draw(im)
    c = S / 2

    def pts(R, r):
        out = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5
            rr = R if k % 2 == 0 else r
            out.append((c + math.cos(a) * rr, c + math.sin(a) * rr * 1.0 + S * .03))
        return out
    d.polygon(pts(S * .48, S * .22), fill=ORO_OSC + (255,))
    d.polygon(pts(S * .44, S * .2), fill=ORO + (255,))
    cl = tuple(int(o + (c_ - o) * brillo) for o, c_ in zip(ORO, ORO_CLARO))     # ImageDraw no mezcla alfa: color sólido
    d.polygon(pts(S * .30, S * .14), fill=cl + (255,))
    vis = math.cos(giro)
    if ojos and vis > 0:
        for sx in (-1, 1):
            ex = c + sx * S * .075
            d.ellipse((ex - S * .028, c - S * .06, ex + S * .028, c + S * .07), fill=(14, 10, 6, 255))
    k = max(.06, abs(vis))
    return im.resize((max(2, int(S * k)), S), Image.BICUBIC)


def _destellos(d, cx, cy, r, dt, n=6, alfa=255):
    for i in range(n):
        a = dt * 1.3 + i * 2 * math.pi / n
        u = .5 + .5 * math.sin(dt * 4 + i * 1.7)
        x, y = cx + math.cos(a) * r, cy + math.sin(a) * r * .8
        s = 6 + 8 * u
        col = (255, 250, 200, int(alfa * u))
        d.line([(x - s, y), (x + s, y)], fill=col, width=3)
        d.line([(x, y - s), (x, y + s)], fill=col, width=3)


def _flecha_roja(d, x, y, dt, alfa=255):
    """El triángulo rojo de «siguiente» de los diálogos de Mario 64, que sube y baja."""
    k = .6 + .4 * math.sin(dt * 6)
    yy = y + 3 * math.sin(dt * 6)
    s = 13
    d.polygon([(x - s, yy - s * .6), (x + s, yy - s * .6), (x, yy + s * .7)], fill=(255, 70, 60, int(alfa * k)))


# ------------------------------------------------------------------ ficha = cuadro de diálogo
def ficha(titulo, texto, tipo=None, ancho=880, vel=55):
    """Cuadro de diálogo de Mario 64: `titulo` en letras del logo, `tipo` en gris cursiva, filete dorado y el texto que se
    ESCRIBE letra a letra (vel = letras/s). *x* = amarillo moneda. Al terminar, el triángulo rojo late."""
    in_w = ancho - 2 * 46
    ft = ajustar(titulo.upper(), "d", 42, in_w)
    fty = ajustar(tipo, "si", 26, in_w) if tipo else None
    fx, ls, lh = caja(texto, "d", 34, in_w, max_lineas=7)
    h = int(34 + 52 + (34 if tipo else 0) + 26 + lh * len(ls) + 40)
    base, M = _humo(ancho, h, alfa=.64, radio=22)
    letras = [len(x.replace("*", "")) for x in ls]

    def fn(dt, dur, marcas):
        im = base.copy()
        d = ImageDraw.Draw(im)
        cx = M + ancho / 2
        y = M + 44
        letras_logo(d, (cx, y), titulo.upper(), ft, 255 * _eo((dt - .15) / .3), fase=dt, salto=0)
        y += 44
        if tipo:
            _txt(d, (cx, y), tipo, fty, GRIS, "mm", 230 * _eo((dt - .3) / .3))
            y += 34
        MJ._filete(d, M + 70, M + ancho - 70, y, 255 * _eo((dt - .3) / .4), color=ORO)
        y += 26 + lh / 2
        quedan = max(0.0, (dt - .45) * vel)
        for ln, n in zip(ls, letras):
            _rica(d, cx, y, ln, fx, BLANCO, AMARILLO, 255, "m", hasta=quedan)
            quedan -= n
            y += lh
        if quedan > 0:
            _flecha_roja(d, M + ancho - 40, M + h - 26, dt)
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ rótulo de secreto = selección de estrella
def puesto(num, titulo, arriba=None):
    """Banda de humo negro: a la izquierda la Estrella de poder que entra con rebote y gira; «SECRETO N.º N» con las letras
    del logo (que hacen la ola) y debajo el título entre guiones, como el nombre del curso en la selección de estrella."""
    arriba = arriba or f"Secreto n.º {num}"
    w, h = 1560, 236
    f1 = ajustar(arriba.upper(), "d", 78, w - 420)
    f2 = ajustar(f"-{titulo}-", "si", 44, w - 420)

    def fn(dt, dur, marcas):
        im, M = _humo(w, h, alfa=.58, radio=60)
        d = ImageDraw.Draw(im)
        # estrella
        s = _reb((dt - .05) / .5)
        if s > .02:
            st = estrella(190 * s, giro=dt * 2.4)
            im.alpha_composite(st, (int(M + 150 - st.width / 2), int(M + h / 2 - st.height / 2)))
            _destellos(d, M + 150, M + h / 2, 120, dt, alfa=220 * min(1, s))
        tx = M + 270 + (w - 270) / 2 - 40
        u = _eo((dt - .2) / .6)
        letras_logo(d, (tx, M + 88), arriba.upper(), f1, 255 * u, fase=dt, salto=7 * (1 - min(1, (dt - .2) / 1.2)))
        MJ._filete(d, tx - 330 * u, tx + 330 * u, M + 146, 255 * u, color=ORO)
        _txt(d, (tx, M + 190), f"-{titulo}-", f2, BLANCO, "mm", 255 * _eo((dt - .6) / .5))
        return _bgra(im, min(_eo(dt / .3), (dur - dt) / .5))
    return fn


# ------------------------------------------------------------------ pegatina
def pegatina(ruta, titulo=None, tam=360, giro=-6.0):
    """Imagen REAL recortada con borde blanco (mg_tes) con rebote y balanceo; el nombre en píldora negra con filo dorado."""
    import mg_tes as T
    base = T._base_pegatina(ruta, tam)
    if titulo:
        tit = MJ._limpia(titulo.upper())
        f = ajustar(tit, "d", 30, max(260, base.width + 40))
        pw, ph = int(MJ._ancho(tit, f) + 56), 62
        pil = _capa(pw, ph)
        dp = ImageDraw.Draw(pil)
        dp.rounded_rectangle((0, 0, pw - 1, ph - 1), ph // 2, fill=(8, 6, 12, 195), outline=ORO + (235,), width=3)
        _txt(dp, (pw / 2, ph / 2 + 1), tit, f, BLANCO, "mm", 255)
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


# ------------------------------------------------------------------ HUD: contador de estrellas
def _hud_num(d, xy, s, tam, alfa=255, color=BLANCO, ancla="lm"):
    f = fuente("d", tam)
    _txt(d, xy, s, f, color, ancla, alfa, borde=4)


def estrellas(titulo, pasos, w=1100, h=330):
    """El contador del HUD «★ × N» en grande: la estrella late y el número SUBE (rueda) hasta el valor de cada paso; debajo
    el texto del paso. pasos = [(valor, texto)]; marca k = paso k. Remate: si el valor final es 120, destellos dorados."""
    ft = ajustar(titulo.upper(), "d", 34, w - 100)

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        letras_logo(d, (M + w / 2, M + 40), titulo.upper(), ft, 255 * _eo(dt / .4))
        mk = list(marcas or [.3 + 1.6 * i for i in range(len(pasos))])
        while len(mk) < len(pasos):
            mk.append(mk[-1] + 1.6)
        k = 0
        for i, m in enumerate(mk[:len(pasos)]):
            if dt >= m:
                k = i
        v0 = pasos[k - 1][0] if k else 0
        v1, texto = pasos[k]
        u = _eo((dt - mk[k]) / 1.1)
        v = v0 + (v1 - v0) * u
        cy = M + 150
        st = estrella(150 * (1 + .06 * math.sin(dt * 5)), giro=.25 * math.sin(dt * 1.5))
        im.alpha_composite(st, (int(M + w / 2 - 230 - st.width / 2), int(cy - st.height / 2)))
        _hud_num(d, (M + w / 2 - 130, cy + 4), "×", 70)
        _hud_num(d, (M + w / 2 - 60, cy + 4), f"{int(round(v))}", 110, color=AMARILLO if u >= 1 else BLANCO)
        if v1 >= 120 and u >= 1:
            _destellos(d, M + w / 2 - 230, cy, 110, dt)
        _txt(d, (M + w / 2, M + h - 52), texto, ajustar(texto, "d", 34, w - 120), CREMA, "mm",
             255 * _eo((dt - mk[k] - .3) / .4))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ cronología
def linea_tiempo(hitos, titulo="Así se hizo", w=1720, h=420):
    """Línea dorada que se dibuja de izquierda a derecha; marca k = hito k: una estrella pequeña cae en su sitio con rebote,
    el año en letras del logo y el texto debajo. El último hito late. hitos = [(año, texto)]."""
    n = len(hitos)
    ft = ajustar(titulo.upper(), "d", 34, w - 100)
    fa = fuente("d", 46)

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        letras_logo(d, (M + w / 2, M + 40), titulo.upper(), ft, 255 * _eo(dt / .4))
        mk = list(marcas or [.4 + 1.4 * i for i in range(n)])
        while len(mk) < n:
            mk.append(mk[-1] + 1.4)
        x0, x1, y = M + 110, M + w - 110, M + 190
        paso = (x1 - x0) / max(1, n - 1)
        lx = x0 + (x1 - x0) * min(1.0, max(0.0, (dt - mk[0] + .3) / max(.5, mk[n - 1] - mk[0] + .3)))
        d.line([(x0, y), (lx, y)], fill=ORO + (230,), width=6)
        for i, ((anio, texto), m) in enumerate(zip(hitos, mk)):
            if dt < m:
                continue
            cx = x0 + paso * i
            s = _reb((dt - m) / .45)
            late = 1 + (.12 * math.sin(dt * 6) if i == n - 1 else 0)
            st = estrella(64 * s * late, giro=0)
            im.alpha_composite(st, (int(cx - st.width / 2), int(y - st.height / 2)))
            d = ImageDraw.Draw(im)
            letras_logo(d, (cx, y - 70), str(anio), fa, 255 * _eo((dt - m) / .3))
            f, ls, lh = caja(texto, "d", 26, paso - 24 if n > 1 else w - 200, 130, max_lineas=4)
            for j, l_ in enumerate(ls):
                _txt(d, (cx, y + 62 + lh * j), l_, f, BLANCO, "mm", 255 * _eo((dt - m - .2) / .4))
        return _salida(im, dt, dur)
    return fn


# ================================================================== MG PROPIOS DEL GUION (mario64_secretos, 29-oct-2026)
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


def mando(titulo="Cruceta contra stick", w=1500, h=560):
    """La cruceta frente al stick: a la izquierda una cruz cuyas 8 flechas se encienden una a una (marca 0, «8 direcciones»);
    a la derecha el stick analógico: un capuchón que da vueltas y deja estela (marca 1, «360 grados»); marca 2 = la
    inclinación cambia el radio: «De puntillas / Trotar / Correr»."""
    ft = ajustar(titulo.upper(), "d", 34, w - 100)
    f1 = fuente("d", 40)

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        letras_logo(d, (M + w / 2, M + 40), titulo.upper(), ft, 255 * _eo(dt / .4))
        mk = _marcas(marcas, 3, paso=2.0)
        cx, cy, R = M + w * .27, M + 280, 120
        u0 = _eo((dt - mk[0]) / .4)
        if u0 > 0:
            g = 46
            gris = (52, 52, 60, int(240 * u0))
            d.rectangle((cx - g / 2, cy - R * .78, cx + g / 2, cy + R * .78), fill=gris)
            d.rectangle((cx - R * .78, cy - g / 2, cx + R * .78, cy + g / 2), fill=gris)
            n_on = int(max(0, min(8, (dt - mk[0]) / .2)))
            for k in range(8):
                a = -math.pi / 2 + k * math.pi / 4
                x, y = cx + math.cos(a) * (R + 30), cy + math.sin(a) * (R + 30)
                col = AMARILLO if k < n_on else (90, 90, 96)
                p = [(x + math.cos(a) * 18, y + math.sin(a) * 18), (x + math.cos(a + 2.4) * 14, y + math.sin(a + 2.4) * 14),
                     (x + math.cos(a - 2.4) * 14, y + math.sin(a - 2.4) * 14)]
                d.polygon(p, fill=col + (int(255 * u0),))
            _txt(d, (cx, M + h - 56), "Cruceta: 8 direcciones", f1, BLANCO, "mm", 255 * u0)
        sx, sy = M + w * .73, M + 280
        u1 = _eo((dt - mk[1]) / .4)
        if u1 > 0:
            d.ellipse((sx - R, sy - R, sx + R, sy + R), outline=(200, 200, 210, int(220 * u1)), width=6)
            ang = (dt - mk[1]) * 2.6
            fase = int((dt - mk[2]) / 1.1) % 3 if dt >= mk[2] else None
            tilt = [.3, .65, 1.0][fase] if fase is not None else 1.0
            capa = _capa(im.width, im.height)
            dc = ImageDraw.Draw(capa)
            for j in range(26):
                a = ang - j * .07
                k = 1 - j / 26
                x, y = sx + math.cos(a) * R * .72 * tilt, sy + math.sin(a) * R * .72 * tilt
                dc.ellipse((x - 7 * k, y - 7 * k, x + 7 * k, y + 7 * k), fill=AMARILLO + (int(200 * k * u1),))
            im.alpha_composite(capa)
            d = ImageDraw.Draw(im)
            x, y = sx + math.cos(ang) * R * .72 * tilt, sy + math.sin(ang) * R * .72 * tilt
            d.ellipse((x - 38, y - 38, x + 38, y + 38), fill=(70, 70, 80, 255), outline=(20, 20, 24, 255), width=4)
            d.ellipse((x - 24, y - 24, x + 24, y + 24), fill=(110, 110, 120, 255))
            lab = ["De puntillas", "Trotar", "Correr"][fase] if fase is not None else "Stick: 360 grados"
            _txt(d, (sx, M + h - 56), lab, f1, AMARILLO if fase is not None else BLANCO, "mm", 255 * u1)
        return _salida(im, dt, dur)
    return fn


def _engranaje(d, cx, cy, r, ang):
    n = 12
    pts = []
    for k in range(n * 2):
        a = ang + k * math.pi / n
        rr = r if k % 2 == 0 else r * .8
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=(196, 156, 64, 255), outline=(90, 60, 20, 255))
    d.ellipse((cx - r * .3, cy - r * .3, cx + r * .3, cy + r * .3), fill=(90, 60, 20, 255))


def reloj_ttc(pasos, titulo="Tick Tock Clock: mira el minutero", w=1240, h=600):
    """El reloj del castillo: esfera crema con números; en cada marca el minutero gira hasta su minuto y a la derecha dos
    engranajes giran a esa velocidad con su nombre. pasos = [(minuto, nombre, vueltas/s o None = al azar)]."""
    ft = ajustar(titulo.upper(), "d", 34, w - 100)
    f1, fnum = fuente("d", 46), fuente("s", 40)

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        letras_logo(d, (M + w / 2, M + 40), titulo.upper(), ft, 255 * _eo(dt / .4))
        mk = _marcas(marcas, len(pasos))
        k = _actual(mk, dt, len(pasos))
        cx, cy, R = M + w * .30, M + 330, 200
        d.ellipse((cx - R - 14, cy - R - 14, cx + R + 14, cy + R + 14), fill=(120, 80, 30, 255))
        d.ellipse((cx - R, cy - R, cx + R, cy + R), fill=(246, 234, 200, 255))
        for hnum in range(1, 13):
            a = -math.pi / 2 + hnum * math.pi / 6
            _txt(d, (cx + math.cos(a) * R * .8, cy + math.sin(a) * R * .8), str(hnum), fnum, (60, 40, 20), "mm", 255)
        m0 = pasos[k - 1][0] if k else pasos[0][0]
        m1, nombre, vel = pasos[k]
        if m1 < m0:
            m1 += 60
        u = _eo((dt - mk[k]) / .8)
        a = -math.pi / 2 + (m0 + (m1 - m0) * u) / 60 * 2 * math.pi
        d.line([(cx, cy), (cx + math.cos(a) * R * .72, cy + math.sin(a) * R * .72)], fill=(232, 40, 40, 255), width=12)
        d.ellipse((cx - 16, cy - 16, cx + 16, cy + 16), fill=(30, 20, 10, 255))
        gx, gy = M + w * .72, M + 290
        t = max(0.0, dt - mk[k])
        ang = (1.6 * math.sin(t * 2.3) + .9 * math.sin(t * 5.1)) if vel is None else t * vel * 2 * math.pi
        _engranaje(d, gx, gy, 120, ang)
        _engranaje(d, gx + 150, gy + 110, 70, -ang * 1.7 + .2)
        if dt >= mk[0]:
            _txt(d, (gx + 40, M + h - 60), nombre, f1, AMARILLO, "mm", 255 * _eo((dt - mk[k] - .5) / .4))
        return _salida(im, dt, dur)
    return fn


def agua(cuadro, titulo="Wet-Dry World: el salto decide el agua", w=1300, h=640):
    """El cuadro REAL del nivel con sus 3 franjas horizontales; marca k = la estrella (Mario) salta a la franja k (0 arriba,
    2 abajo) y a la derecha un depósito cuyo nivel de agua sube o baja a esa altura, con olas."""
    ft = ajustar(titulo.upper(), "d", 34, w - 100)
    f1 = fuente("d", 34)
    img = Image.open(cuadro).convert("RGBA").resize((360, 360), Image.LANCZOS)
    niveles = [.85, .5, .15]
    textos = ["Saltas arriba: agua alta", "En medio: a media altura", "Saltas abajo: casi seco"]

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        letras_logo(d, (M + w / 2, M + 40), titulo.upper(), ft, 255 * _eo(dt / .4))
        mk = _marcas(marcas, 3)
        x0, y0 = int(M + 110), int(M + 120)
        im.alpha_composite(img, (x0, y0))
        d = ImageDraw.Draw(im)
        zona = _actual(mk, dt, 3) if dt >= mk[0] else None
        for z in range(3):
            on = zona == z
            d.rectangle((x0, y0 + z * 120, x0 + 360, y0 + z * 120 + 120), outline=(AMARILLO if on else BLANCO) + (255 if on else 120,),
                        width=5 if on else 2)
        lv, u = .5, 0.0
        if zona is not None:
            u = _eo((dt - mk[zona]) / 1.0)
            prev = niveles[zona - 1] if zona else .5
            lv = prev + (niveles[zona] - prev) * u
            st = estrella(70, giro=dt * 3)
            sy = y0 + zona * 120 + 60 - 70 * math.sin(min(1.0, (dt - mk[zona]) / .5) * math.pi)
            im.alpha_composite(st, (int(x0 + 360 + 40), int(sy - st.height / 2)))
        tx0, ty0, tx1, ty1 = M + w * .62, M + 120, M + w * .62 + 300, M + 480
        capa = _capa(im.width, im.height)
        dc = ImageDraw.Draw(capa)
        wy = ty1 - (ty1 - ty0) * lv
        for xx in range(int(tx0) + 4, int(tx1) - 3, 6):
            yy = wy + 6 * math.sin(xx * .05 + dt * 4)
            dc.line([(xx, yy), (xx, ty1 - 4)], fill=(60, 140, 255, 170), width=6)
        im.alpha_composite(capa)
        d = ImageDraw.Draw(im)
        d.rectangle((tx0, ty0, tx1, ty1), outline=BLANCO + (220,), width=4)
        if zona is not None:
            _txt(d, (M + w / 2, M + h - 50), textos[zona], f1, BLANCO, "mm", 255 * u)
        return _salida(im, dt, dur)
    return fn


def boton_a(pasos, titulo="El reto del botón A", w=1100, h=520):
    """El botón A azul del mando de N64 y el contador «A ×». pasos = [(valor_texto, pulsado 0..1, texto)]; marca k = paso k:
    el botón se hunde hasta `pulsado` (0,5 = a medio camino, con flecha «medio») y el contador cambia con rebote."""
    ft = ajustar(titulo.upper(), "d", 34, w - 100)
    f1 = fuente("d", 34)

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        letras_logo(d, (M + w / 2, M + 40), titulo.upper(), ft, 255 * _eo(dt / .4))
        mk = _marcas(marcas, len(pasos))
        k = _actual(mk, dt, len(pasos))
        val, pul, texto = pasos[k]
        u = _eo((dt - mk[k]) / .5)
        p0 = pasos[k - 1][1] if k else 0
        pv = p0 + (pul - p0) * u
        bx, by, R = M + w * .30, M + 250, 110
        hund = 34 * pv
        d.ellipse((bx - R, by - R + 40, bx + R, by + R + 40), fill=(10, 30, 90, 255))
        d.ellipse((bx - R, by - R + hund, bx + R, by + R + hund), fill=(40, 90, 230, 255), outline=(20, 50, 160, 255), width=6)
        _txt(d, (bx, by + hund), "A", fuente("d", 120), BLANCO, "mm", 255)
        if 0 < pul < 1 and u >= 1:
            ax = bx - R - 24                               # flecha a la IZQUIERDA del botón (el contador va a la derecha)
            d.polygon([(ax, by + hund), (ax - 40, by + hund - 24), (ax - 40, by + hund + 24)], fill=AMARILLO + (255,))
            _txt(d, (ax - 50, by + hund), "medio", f1, AMARILLO, "rm", 255)
        sx = M + w * .70
        _hud_num(d, (sx - 40, M + 250), "A ×", 70, ancla="rm")
        _hud_num(d, (sx, M + 250), val, int(110 * (.8 + .2 * _reb((dt - mk[k]) / .4))), color=AMARILLO)
        _txt(d, (M + w / 2, M + h - 50), texto, ajustar(texto, "d", 34, w - 120), CREMA, "mm", 255 * _eo((dt - mk[k] - .3) / .4))
        return _salida(im, dt, dur)
    return fn


def bit(titulo="Un solo bit", w=1500, h=600, n=16, cual=7):
    """La altura de Mario como fila de n bits; marca 0 = la fila se escribe; marca 1 = un rayo cae sobre el bit `cual`, que
    cambia y se pone rojo; marca 2 = a la derecha la estrella (Mario) sube de golpe por la barra de altura."""
    import random
    rnd = random.Random(64)
    bits = [rnd.randint(0, 1) for _ in range(n)]
    ft = ajustar(titulo.upper(), "d", 34, w - 100)
    fb, f1 = fuente("d", 44), fuente("d", 32)

    def fn(dt, dur, marcas):
        im, M = _humo(w, h)
        d = ImageDraw.Draw(im)
        letras_logo(d, (M + w / 2, M + 40), titulo.upper(), ft, 255 * _eo(dt / .4))
        mk = _marcas(marcas, 3, paso=1.4)
        T, G_ = 62, 10
        x0, y0 = M + 60, M + 300
        vis = int(max(0, min(n, (dt - mk[0]) / .06)))
        _txt(d, (x0, M + 230), "La altura de Mario, en la memoria:", f1, CREMA, "lm", 255 * _eo((dt - mk[0]) / .3))
        for i in range(vis):
            x = x0 + i * (T + G_)
            rojo = i == cual and dt >= mk[1]
            b = (1 - bits[i]) if rojo else bits[i]
            d.rounded_rectangle((x, y0, x + T, y0 + T + 10), 10, fill=((140, 20, 20, 230) if rojo else (20, 26, 40, 200)),
                                outline=((255, 80, 80) if rojo else (120, 140, 170)) + (255,), width=3)
            _txt(d, (x + T / 2, y0 + T / 2 + 5), str(b), fb, (255, 230, 230) if rojo else BLANCO, "mm", 255)
        if mk[1] <= dt < mk[1] + .7:
            x = x0 + cual * (T + G_) + T / 2
            k = 1 - (dt - mk[1]) / .7
            pts = [(x - 10, M + 70), (x + 18, M + 150), (x - 8, M + 190), (x + 12, y0 - 4)]
            d.line(pts, fill=(255, 255, 210, int(255 * k)), width=9)
        if dt >= mk[1]:
            _txt(d, (x0 + cual * (T + G_) + T / 2, y0 + T + 50), "cambió", f1, (255, 120, 120), "mm", 255 * _eo((dt - mk[1]) / .3))
        bx = M + w - 110
        d.line([(bx, M + 120), (bx, M + h - 70)], fill=(200, 200, 210, 200), width=6)
        alto = .2 + (.7 * _reb((dt - mk[2]) / .5) if dt >= mk[2] else 0)
        y = M + h - 70 - (h - 190) * alto
        st = estrella(64, giro=dt * 3)
        im.alpha_composite(st, (int(bx - st.width / 2), int(y - st.height / 2)))
        return _salida(im, dt, dur)
    return fn


# ------------------------------------------------------------------ prueba
def _hoja(fn, dur, marcas, ruta, n=6, fondo=None):
    cols = []
    for k in range(n):
        dt = dur * (k + .5) / n
        a = fn(dt, dur, marcas)
        bg = np.zeros((1080, 1920, 3), np.uint8) + np.array([60, 140, 60], np.uint8) if fondo is None else fondo.copy()
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
        _hoja(puesto(7, "El rayo cósmico"), 4.0, [], "previews/m64_puesto.jpg")
        _hoja(ficha("Ventas", "Unos *11,9 millones* de copias en Nintendo 64.", tipo="Según Nintendo"), 6.0, [],
              "previews/m64_ficha.jpg")
        _hoja(estrellas("Estrellas de poder", [(70, "Para el final"), (120, "Al 100 %")]), 5.0, [.3, 2.4],
              "previews/m64_estrellas.jpg")
        _hoja(linea_tiempo([("1994", "Empieza"), ("1995", "Shoshinkai"), ("1996", "Japón"), ("1997", "Shindou")]), 7.0,
              [.4, 1.8, 3.2, 4.6], "previews/m64_linea.jpg")
        _hoja(mando(), 7.0, [.4, 2.4, 4.4], "previews/m64_mando.jpg")
        _hoja(reloj_ttc([(0, "Detenido", 0), (15, "Lento", .15), (30, "Al azar", None), (45, "Rápido", 1.2)]), 8.0,
              [.4, 2.2, 4.0, 5.8], "previews/m64_reloj.jpg")
        _hoja(agua(os.path.join("..", "videos", "mario64_secretos", "pegatinas", "cuadro_wdw.png")), 7.0, [.6, 2.6, 4.6],
              "previews/m64_agua.jpg")
        _hoja(boton_a([("1", 1.0, "Lo normal"), ("0,5", .5, "Medio pulsado"), ("0", 0, "En 2023: cero")]), 7.0,
              [.4, 2.4, 4.6], "previews/m64_botona.jpg")
        _hoja(bit(), 6.0, [.4, 2.4, 3.6], "previews/m64_bit.jpg")
        print("previews/m64_*.jpg")
