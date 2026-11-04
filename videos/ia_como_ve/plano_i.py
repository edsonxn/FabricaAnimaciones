# -*- coding: utf-8 -*-
"""PALABRAS: números → ¿palabras? → 2021: 400 millones de fotos con su texto (columnas que suben) → imanes: la foto se acerca a
su frase y empuja las equivocadas → el MAPA DE SIGNIFICADOS como cielo de estrellas: foto de gato y palabra «gato» vecinas,
el perro cerca, el volcán lejísimos → el traductor convierte los pedazos de la imagen en estrellas de ese mapa → el mensaje con
las «palabras visuales» y la respuesta palabra por palabra con sus probabilidades → dibujo, radiografía y meme: ya vio
muchísimos de cada uno."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lerp, linea, pr, rgb, rotulo, rrect,
                      suave, terminar)
from comun import T0, T1, desborde, ww
from fondos_ia import cabeza, papel
from iconos_ia import estrella, foto_cosa
from personajes import AMARILLO, BLANCO, OJO_K, destello, kuri, pregunta
from personajes_ia import dibujo_nino, foto_gato, meme_gato, pegar, radiografia
from plano_h import NC, NR, _pieza, _poner

E = "palabras"
T_INI = T0(E)
tUltimo, tNumeros, tPalabras = ww(E, 0, "ultimo"), ww(E, 0, "numeros"), ww(E, 0, "palabras")
tVeintiuno, tCuatro, tTexto = ww(E, 1, "veintiuno"), ww(E, 1, "cuatrocientos"), ww(E, 1, "texto")
tAcercar, tAlejarla = ww(E, 2, "acercar"), ww(E, 2, "alejarla")
tMapa, tGato, tGatoP, tPerro, tVolcan = (ww(E, 3, "mapa"), ww(E, 3, "gato"), ww(E, 3, "gato", n=1), ww(E, 3, "perro"),
                                         ww(E, 3, "volcan"))
tLenguaje, tTraductor, tPuntos = ww(E, 4, "lenguaje"), ww(E, 4, "traductor"), ww(E, 4, "puntos")
tLee, tMensaje, tContesta, tProbable = ww(E, 5, "lee"), ww(E, 5, "mensaje"), ww(E, 5, "contesta", n=1), ww(E, 5, "probable")
tDibujo, tRadio, tMeme, tMiles = ww(E, 6, "dibujo"), ww(E, 6, "radiografia"), ww(E, 6, "meme"), ww(E, 6, "miles")
T_FIN = T1(E)
ROJO = rgb("e35d4a")
VERDE = rgb("4f9a5a")
CIELO = rgb("ffe9a8")


# ------------------------------------------------------------ ¿números → palabras?
def numpal(t):
    im = cabeza()
    for k in range(9):
        y = 260 + 70 * k
        rotulo(im, f"{math.sin(k * 1.7 + t * 0.8) * 3:+.2f}", 360, y, 46, OJO_K, t, seed=14000 + k, tinta=False)
    e = e_back(pr(t, tNumeros - 0.2, tNumeros + 0.2))
    linea(im, [(560, 540), (1160, 540)], 14, col=AMARILLO, seed=14010, t=t, alfa=e)
    forma(im, np.array([(1160, 500), (1220, 540), (1160, 580)], np.float32), AMARILLO, t, 14011, tinta=3, alfa=e)
    pregunta(im, 860, 400, 1.4 * e, t, seed=14012)
    if t > tPalabras - 0.2:
        a = e_back(pr(t, tPalabras - 0.2, tPalabras + 0.2))
        forma(im, rrect(1500, 540, 420 * a, 160 * a, 24), BLANCO, t, 14013, tinta=5)
        rotulo(im, "«GATO»", 1500, 540, int(90 * a) + 2, TINTA, t, seed=14014, tinta=False)
    kuri(im, 1600, 820, 1.3, t, cara="abiertos")
    rotulo(im, "LO ÚLTIMO", W / 2, 120, 80, AMARILLO, t, seed=14015, esc=e_back(pr(t, tUltimo - 0.2, tUltimo + 0.1)))
    return im


# ------------------------------------------------------------ 400 millones de fotos con su texto
PARES = [("gato", "un gato durmiendo"), ("perro", "mi perro en el parque"), ("volcan", "volcán en erupción"),
         ("tostadora", "tostadora nueva"), ("bici", "mi bici roja"), ("gato2", "gato curioso"), ("panda", "panda comiendo"),
         ("dibujo", "dibujo de mi hija"), ("meme", "lunes. siempre lunes")]


def _img(nom, t):
    if nom == "gato":
        return foto_gato(t)
    if nom == "gato2":
        return foto_gato(t, "despierto")
    if nom == "dibujo":
        return dibujo_nino(t)
    if nom == "meme":
        return meme_gato(t)
    return foto_cosa(nom, t)


def pares(t):
    im = papel("calido")
    for c in range(3):
        for k in range(4):
            idx = (c * 4 + k) % len(PARES)
            ph = ((t - tVeintiuno) * 0.08 * (1 + 0.2 * c) + k / 4) % 1
            x, y = 520 + 440 * c, lerp(1250, -170, ph)
            nom, txt = PARES[idx]
            pegar(im, _img(nom, t), x, y, 0.5, 0.03 * (c - 1), t=t, seed=14100 + c * 10 + k, marco=8)
            forma(im, rrect(x, y + 140, 300, 50, 8), rgb("fff6c8"), t, 14140 + c * 10 + k, tinta=2.6)
            rotulo(im, txt, x, y + 140, 28, rgb("2b3f8a"), t, seed=14170 + c * 10 + k, tinta=False, fuente="segoesc.ttf")
    forma(im, rrect(W / 2, 90, 1300, 130, 20), rgb("f7ecd4"), t, 14200, tinta=0, alfa=0.85)
    rotulo(im, "2021", 360, 90, 80, rgb("b8443a"), t, seed=14201, esc=e_back(pr(t, tVeintiuno - 0.2, tVeintiuno + 0.1)))
    if t > tCuatro - 0.2:
        rotulo(im, "400 000 000 FOTOS", 1080, 90, 80, rgb("3f78c8"), t, seed=14202, esc=e_back(pr(t, tCuatro - 0.2, tCuatro + 0.1)))
    if t > tTexto - 0.2:
        rotulo(im, "+ SU TEXTO", 1600, 90, 64, rgb("2b3f8a"), t, seed=14203, esc=e_back(pr(t, tTexto - 0.2, tTexto + 0.1)))
    return im


# ------------------------------------------------------------ imanes: acercar y alejar
def imanes(t):
    im = papel("frio")
    pegar(im, foto_gato(t), W / 2, 470, 0.8, 0, t=t, seed=14300, marco=14)
    frases = [("UN GATO DORMIDO", (-1, 1), True), ("UN VOLCÁN", (1, -1), False), ("UNA BICI ROJA", (1, 1), False),
              ("UNA TOSTADORA", (-1, -1), False)]
    ua = e_in(pr(t, tAcercar, tAcercar + 1.4))
    ul = e_out(pr(t, tAlejarla, tAlejarla + 1.2))
    for k, (txt, (dx, dy), buena) in enumerate(frases):
        x0, y0 = W / 2 + dx * 640, 470 + dy * 290
        if buena:
            x, y = lerp(x0, W / 2, 0.75 * ua), lerp(y0, 760, ua)
        else:
            x, y = x0 + dx * 120 * ul, y0 + dy * 50 * ul
        col = VERDE if buena and ua > 0.5 else (ROJO if not buena and ul > 0.1 else TINTA)
        forma(im, rrect(x, y, 30 * len(txt) * 0.62 + 50, 70, 12), BLANCO, t, 14310 + k, tinta=4)
        rotulo(im, txt, x, y, 36, col, t, seed=14320 + k, tinta=False)
        if buena and 0.05 < ua < 1:
            for j in range(3):
                linea(im, [(x + 20 * (j - 1), y - 60), (x + 20 * (j - 1) + (W / 2 - x) * 0.1, y - 100)], 5, col=VERDE, seed=14330 + j, t=t)
        if not buena and ul > 0.05:
            linea(im, [(x - dx * 200, y - dy * 30), (x - dx * 120, y - dy * 18)], 7, col=ROJO, seed=14340 + k, t=t, alfa=ul)
    rotulo(im, "ACERCAR A SU FRASE", 480, 1030, 54, VERDE, t, seed=14350, esc=e_back(pr(t, tAcercar - 0.2, tAcercar + 0.1)))
    if t > tAlejarla - 0.2:
        rotulo(im, "ALEJAR LAS EQUIVOCADAS", 1440, 1030, 54, ROJO, t, seed=14351, esc=e_back(pr(t, tAlejarla - 0.2, tAlejarla + 0.1)))
    return im


# ------------------------------------------------------------ el mapa de significados (cielo de estrellas)
def _cielo(im, t, seed=14400, n=120):
    rg = np.random.default_rng(seed)
    for k in range(n):
        x, y = rg.uniform(0, W), rg.uniform(0, H)
        f = 0.4 + 0.6 * (0.5 + 0.5 * math.sin(t * 2 + k))
        brillo(im, x, y, 6 + 6 * f, CIELO, 0.5 * f)


def mapa(t):
    im = papel("noche")
    _cielo(im, t)
    rotulo(im, "EL MAPA DE SIGNIFICADOS", W / 2, 90, 70, CIELO, t, seed=14450, esc=e_back(pr(t, tMapa - 0.2, tMapa + 0.2)))
    for k, (txt, x, y, nom) in enumerate((("TOSTADORA", 1500, 860, "tostadora"), ("BICI", 1250, 980, "bici"),
                                          ("MEME", 320, 900, "meme"), ("TECLADO", 820, 240, None), ("PANDA", 1620, 620, "panda"))):
        rotulo(im, txt, x, y, 30, CIELO * 0.7, t, seed=14460 + k, tinta=False, alfa=0.6)
        if nom:
            pegar(im, _img(nom, t), x, y - 80, 0.22, 0.05 * (k - 2), t=t, seed=14465 + k, marco=5, alfa=0.55)
        estrella(im, x - 90 - 8 * len(txt), y, 6, t, CIELO, 0.6, seed=14470 + k)
    grupos = [("gato", "GATO", 560, 470, tGato), ("perro", "PERRO", 1000, 700, tPerro), ("volcan", "VOLCÁN", 1650, 300, tVolcan)]
    for k, (nom, pal, x, y, ti) in enumerate(grupos):
        e = e_back(pr(t, ti - 0.3, ti + 0.1))
        if e <= 0.02:
            continue
        estrella(im, x, y, 10, t, CIELO, 1.0, seed=14480 + k)
        pegar(im, _img(nom, t), x - 90, y - 20, 0.36 * e, -0.05, t=t, seed=14490 + k, marco=6)
        tp = tGatoP if k == 0 else ti + 0.2
        if t > tp - 0.2:
            a = e_back(pr(t, tp - 0.2, tp + 0.1))
            forma(im, rrect(x + 120, y + 50, 190 * a, 60 * a, 12), BLANCO, t, 14500 + k, tinta=3)
            rotulo(im, f"«{pal}»", x + 120, y + 50, int(34 * a) + 2, TINTA, t, seed=14510 + k, tinta=False)
    gx, gy = 560, 470
    if t > tGatoP:
        linea(im, elipse(gx + 20, gy + 20, 260, 170), 4, col=AMARILLO, seed=14520, t=t, cerrado=True, punta=False, alfa=0.7)
        rotulo(im, "VECINAS", gx + 20, gy - 190, 40, AMARILLO, t, seed=14521, esc=e_back(pr(t, tGatoP, tGatoP + 0.3)))
    if t > tPerro + 0.3:
        linea(im, [(gx + 120, gy + 90), (900, 690)], 4, col=CIELO, seed=14522, t=t, alfa=0.6, punta=False)
        rotulo(im, "CERCA", 800, 560, 40, CIELO, t, seed=14523, esc=e_back(pr(t, tPerro + 0.3, tPerro + 0.6)))
    if t > tVolcan + 0.3:
        u = e_out(pr(t, tVolcan + 0.3, tVolcan + 1.3))
        linea(im, [(gx + 120, gy - 40), (lerp(gx + 120, 1560, u), lerp(gy - 40, 320, u))], 4, col=rgb("f08a9a"), seed=14524, t=t,
              alfa=0.7, punta=False)
        rotulo(im, "¡LEJÍSIMOS!", 1200, 340, 50, rgb("f08a9a"), t, seed=14525, esc=e_back(pr(t, tVolcan + 0.8, tVolcan + 1.1)), rot=-0.1)
    return im


# ------------------------------------------------------------ el traductor y el mensaje
def mensaje(t):
    im = papel("noche")
    _cielo(im, t, n=70)
    foto = foto_gato(t)
    rotulo(im, "MODELO DE LENGUAJE CON VISIÓN", W / 2, 80, 56, CIELO, t, seed=14600, esc=e_back(pr(t, tLenguaje - 0.3, tLenguaje)))
    # traductor: una caja con engranes donde entran los pedazos
    e = e_back(pr(t, tTraductor - 0.3, tTraductor + 0.1))
    forma(im, rrect(820, 380, 260 * e, 200 * e, 30), rgb("5fb7c0"), t, 14610, tinta=5)
    rotulo(im, "TRADUCTOR", 820, 380, int(38 * e) + 2, BLANCO, t, seed=14611)
    sel = [(3, 2), (5, 1), (5, 2), (2, 4), (4, 2), (1, 3)]
    for k, (i, j) in enumerate(sel):
        ph = clamp((t - tTraductor - 0.3 * k) / 1.6)
        if t < tTraductor:
            ph = 0.0
        x = lerp(260, 820, min(1, ph * 1.6))
        y = lerp(260 + 110 * k - 60, 380, min(1, ph * 1.6))
        if ph < 0.62:
            _poner(im, _pieza(foto, i, j, 1.1), x, y)
        else:                                                    # sale como estrella del mapa
            u = (ph - 0.62) / 0.38
            sx, sy = lerp(950, 1200 + 110 * k, u), lerp(380, 300 + 40 * math.sin(k * 2), u)
            estrella(im, sx, sy, 10, t, AMARILLO, 1.0, seed=14620 + k)
    if t > tTraductor + 3.6:
        pegar(im, foto, 300, 400, 0.45, -0.04, t=t, seed=14625, marco=8, alfa=pr(t, tTraductor + 3.6, tTraductor + 4.2))
    if t > tPuntos - 0.2:
        rotulo(im, "PUNTOS DEL MAPA", 1500, 470, 40, AMARILLO, t, seed=14630, esc=e_back(pr(t, tPuntos - 0.2, tPuntos + 0.1)))
    # el mensaje: fichas visuales + palabras
    if t > tLee - 0.3:
        a = e_back(pr(t, tLee - 0.3, tLee + 0.1))
        forma(im, rrect(W / 2, 700, 1500, 110, 30), rgb("f4f1ea"), t, 14640, tinta=4, alfa=a)
        for k in range(6):
            forma(im, rrect(330 + 80 * k, 700, 60, 60, 8), lerp(AMARILLO, rgb("e8933a"), k / 5), t, 14650 + k, tinta=2.4, alfa=a)
        rotulo(im, "¿qué hay en la foto?", 1150, 700, 46, TINTA, t, seed=14660, tinta=False, fuente="segoesc.ttf", alfa=a)
        if t > tMensaje - 0.2:
            rotulo(im, "TU MENSAJE", 330 + 200, 620, 32, CIELO, t, seed=14661, tinta=False)
    # la respuesta, palabra por palabra, con sus probabilidades
    if t > tContesta - 0.4:
        resp = [("Un", ["Un 71 %", "El 20 %"]), ("gato", ["gato 92 %", "perro 5 %"]), ("naranja", ["naranja 88 %", "café 7 %"]),
                ("dormido", ["dormido 64 %", "acostado 30 %"]), ("sobre…", ["sobre 81 %", "en 12 %"])]
        x = 300
        for k, (pal, op) in enumerate(resp):
            tk = tContesta - 0.2 + 0.55 * k
            a = e_back(pr(t, tk, tk + 0.25))
            if a <= 0.02:
                break
            w = 40 + 34 * len(pal)
            forma(im, rrect(x + w / 2, 900, w * a, 80, 16), rgb("d8ecf0"), t, 14670 + k, tinta=3)
            rotulo(im, pal, x + w / 2, 900, 44, TINTA, t, seed=14680 + k, tinta=False, alfa=a)
            if tk < t < tk + 1.2 or k == len(resp) - 1:
                for j, o in enumerate(op):
                    bw = 180 if j == 0 else 60
                    forma(im, rrect(x + w / 2, 980 + 34 * j, bw, 22, 6), VERDE if j == 0 else rgb("9aa4ae"), t, 14690 + 3 * k + j,
                          tinta=0, alfa=0.8)
                    rotulo(im, o, x + w / 2, 980 + 34 * j, 22, CIELO, t, seed=14700 + 3 * k + j, tinta=False)
            x += w + 30
        if t > tProbable - 0.2:
            rotulo(im, "ELIGE LA MÁS PROBABLE", 1500, 570, 46, AMARILLO, t, seed=14720, esc=e_back(pr(t, tProbable - 0.2, tProbable + 0.1)))
    return im


# ------------------------------------------------------------ ya vio muchísimos
def vio(t):
    im = papel("calido")
    for k, (img_f, ti, txt) in enumerate(((dibujo_nino, tDibujo, "DIBUJOS"), (radiografia, tRadio, "RADIOGRAFÍAS"),
                                          (meme_gato, tMeme, "MEMES"))):
        e = e_back(pr(t, ti - 0.3, ti + 0.1))
        if e <= 0.02:
            continue
        x = 400 + 560 * k
        n = 1 + int(5 * e_out(pr(t, tMiles - 0.2, tMiles + 1.0)))
        for j in range(n - 1, -1, -1):
            pegar(im, img_f(t), x + 16 * j, 520 - 14 * j, 0.62 * e, 0.06 * (j - 2), t=t, seed=14800 + 10 * k + j, marco=10)
        rotulo(im, txt, x, 850, 56, rgb("b8443a"), t, seed=14830 + k, esc=e)
    if t > tMiles - 0.2:
        rotulo(im, "MILES DE MILLONES DE IMÁGENES CON TEXTO", W / 2, 990, 56, rgb("3f78c8"), t, seed=14840,
               esc=e_back(pr(t, tMiles - 0.2, tMiles + 0.1)))
    rotulo(im, "YA VIO MUCHÍSIMOS", W / 2, 110, 76, TINTA, t, seed=14841, tinta=False,
           esc=e_back(pr(t, tMiles + 1.5, tMiles + 1.8)))
    return im


TRAMOS = [(numpal, T_INI), (pares, tVeintiuno - 0.5), (imanes, tAcercar - 0.5), (mapa, tMapa - 0.5), (mensaje, tLenguaje - 0.5),
          (vio, tDibujo - 0.5)]


def cuadro_crudo(t):
    k = 0
    for i, (_, ti) in enumerate(TRAMOS):
        if t >= ti:
            k = i
    f, ti = TRAMOS[k]
    im = f(t)
    if t < ti + 0.6:
        if k > 0:
            im = desborde(TRAMOS[k - 1][0](t), im, pr(t, ti, ti + 0.6), W * (0.3 + 0.08 * k), H * 0.5)
        else:
            import plano_h
            im = desborde(plano_h.cuadro_crudo(t), im, pr(t, ti, ti + 0.6), W * 0.5, H * 0.5)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
