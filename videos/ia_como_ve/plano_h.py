# -*- coding: utf-8 -*-
"""PARCHES Y ATENCIÓN: el celular donde una IA describe la foto → la foto se corta en un ROMPECABEZAS de 7×5 pedazos
(«16 × 16 píxeles») → un pedazo sale con su lista de números y se vuelve una «palabra visual»; etiquetas en los pedazos
(pelo naranja, tecla, pedazo de oreja) → ATENCIÓN: el pedazo de pelo lanza hilos a todos («¿quién me ayuda a entender lo que
soy?») → hilos gruesos pelo ↔ oreja ↔ bigote: «¡SOMOS UN GATO!» → tecla ↔ gato: la escena completa → la hoja del artículo:
«An image is worth 16×16 words» (2020)."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lerp, linea, pr, rgb, rotulo, rrect,
                      suave, terminar)
from comun import T0, T1, desborde, ww
from fondos_ia import papel
from personajes import AMARILLO, BLANCO, OJO_K, destello, kuri
from personajes_ia import foto_gato, globo, nina, pegar

E = "parches"
T_INI = T0(E)
tPlaticas, tDescriben, tPaso = ww(E, 0, "platicas"), ww(E, 0, "describen"), ww(E, 0, "paso")
tCortan, tRompe, tPedazos, tDieci = ww(E, 1, "cortan"), ww(E, 1, "rompecabezas"), ww(E, 1, "pedazos"), ww(E, 1, "dieciseis")
tLista, tPelo, tTecla, tOreja, tPalabra = (ww(E, 2, "lista"), ww(E, 2, "pelo"), ww(E, 2, "tecla"), ww(E, 2, "oreja"),
                                           ww(E, 2, "palabra"))
tAtencion, tMira, tQuien = ww(E, 3, "atencion"), ww(E, 3, "mira"), ww(E, 3, "quien")
tPelo4, tOreja4, tBigote, tSomos = ww(E, 4, "pelo"), ww(E, 4, "oreja"), ww(E, 4, "bigote"), ww(E, 4, "somos")
tTecla5, tGato5, tEscena = ww(E, 5, "tecla"), ww(E, 5, "gato"), ww(E, 5, "escena")
tTitulo, tVale = ww(E, 6, "titulo"), ww(E, 6, "vale")
T_FIN = T1(E)

NC, NR = 7, 5
FW, FH = 560, 420
PW, PH = FW // NC, FH // NR                                      # 80 × 84
ESC = 1.55
CX, CY = 720, 560
PELO, OREJA, BIGOTE, TECLA, CUERPO = (3, 2), (5, 1), (5, 2), (2, 4), (4, 2)
ETQ = {PELO: ("PELO NARANJA", tPelo), TECLA: ("TECLA", tTecla), OREJA: ("PEDAZO DE OREJA", tOreja)}


def _pieza(foto, i, j, esc):
    import cv2
    pz = foto[j * PH:(j + 1) * PH, i * PW:(i + 1) * PW]
    return cv2.resize(pz, (int(PW * esc), int(PH * esc)), interpolation=cv2.INTER_LINEAR)


def _poner(im, pz, x, y, sombra=True):
    """Pegado rápido por recorte (sin giro): sombra suave + pieza + contorno fino."""
    h, w = pz.shape[:2]
    x0, y0 = int(x - w / 2), int(y - h / 2)
    if sombra:
        sx, sy = x0 + 8, y0 + 10
        im[max(0, sy):sy + h, max(0, sx):sx + w] *= 0.82
    xa, ya = max(0, x0), max(0, y0)
    xb, yb = min(W, x0 + w), min(H, y0 + h)
    if xb > xa and yb > ya:
        im[ya:yb, xa:xb] = pz[ya - y0:yb - y0, xa - x0:xb - x0]
        im[ya:yb, [xa, xb - 1]] *= 0.55
        im[[ya, yb - 1], xa:xb] *= 0.55


def _centro(i, j, t):
    sep = 22 * e_out(pr(t, tCortan - 0.1, tRompe + 0.3))
    x = CX + (i - (NC - 1) / 2) * (PW * ESC + sep)
    y = CY + (j - (NR - 1) / 2) * (PH * ESC + sep)
    if tCortan < t < tLista:                                        # se mecen como piezas sueltas
        x += 4 * math.sin(t * 3 + i * 1.3 + j)
        y += 4 * math.cos(t * 2.6 + j * 1.7 + i)
    return x, y


# ------------------------------------------------------------ el celular
def chat(t):
    im = papel("calido")
    p = nina(im, 380, 650, 1.45, t, cara="normal", boca="sonrisa", brazos=(0.3, 1.2), codos=(0.4, 0.6), mira=1.0)
    x, y = 960, 540
    forma(im, rrect(x, y, 470, 840, 50), rgb("2b2f38"), t, 13000, tinta=5)
    forma(im, rrect(x, y, 420, 760, 30), rgb("f4f1ea"), t, 13001, tinta=2)
    pegar(im, foto_gato(t), x + 60, y - 200, 0.55, 0, t=t, seed=13002, marco=8)
    if t > tDescriben - 0.6:
        n = 44 * pr(t, tDescriben - 0.6, tPaso)
        globo(im, x - 20, y + 140, 360, 210, "", t, px=34, n=n, lineas=["UN GATO NARANJA", "DORMIDO SOBRE", "UN TECLADO"],
              seed=13010, cola=(-1, 1), col=rgb("d8ecf0"))
    kuri(im, 1480, 520, 1.7, t, cara="feliz" if t > tDescriben else "normal")
    if t > tPaso - 0.2:
        rotulo(im, "UN PASO MÁS", 1480, 880, 70, rgb("b8443a"), t, seed=13020, esc=e_back(pr(t, tPaso - 0.2, tPaso + 0.1)), rot=-0.04)
    return im


# ------------------------------------------------------------ el rompecabezas
def _hilo(im, a, b, ancho, col, alfa, seed, t=0.0):
    (x0, y0), (x1, y1) = a, b
    mx, my = (x0 + x1) / 2, min(y0, y1) - 60 - 0.15 * abs(x1 - x0)
    linea(im, curva([(x0, y0), (mx, my), (x1, y1)], 10), ancho, col=col, seed=seed, t=t, alfa=alfa, punta=False)


def rompecabezas(t):
    im = papel("frio")
    foto = foto_gato(t)
    fuera = None
    for j in range(NR):
        for i in range(NC):
            x, y = _centro(i, j, t)
            sale = (i, j) == PELO and tLista - 0.3 < t < tPelo + 0.6
            if sale:
                fuera = (x, y)
                u = e_out(pr(t, tLista - 0.3, tLista + 0.3)) * (1 - e_in(pr(t, tPelo, tPelo + 0.6)))
                x, y = lerp(x, 1620, u), lerp(y, 330, u)
                esc = ESC * (1 + 1.2 * u)
            else:
                esc = ESC
            _poner(im, _pieza(foto, i, j, esc), x, y, sombra=t > tCortan)
            if sale and u > 0.3:                                    # su lista de números
                for k, v in enumerate(("0.81", "-1.2", "3.07", "0.44", "…")):
                    rotulo(im, v, 1470 + 110 * (k % 3), 530 + 60 * (k // 3), 44, rgb("3f78c8"), t, seed=13150 + k, tinta=False,
                           alfa=u)
    if t > tDieci - 0.2 and t < tLista:
        e = e_back(pr(t, tDieci - 0.2, tDieci + 0.1))
        rotulo(im, "16 × 16 PÍXELES", 1600, 320, 64, rgb("b8443a"), t, seed=13200, esc=e, fuente="seguisym.ttf")
        rotulo(im, "CADA PEDAZO", 1600, 400, 48, rgb("b8443a"), t, seed=13202, esc=e)
    if tRompe - 0.2 < t < tLista:
        rotulo(im, "UN ROMPECABEZAS", 1600, 180, 62, rgb("3f78c8"), t, seed=13201, esc=e_back(pr(t, tRompe - 0.2, tRompe + 0.1)))
    # etiquetas: palabras visuales
    for (cel, (txt, ti)) in ETQ.items():
        if tLista < t and t > ti - 0.2 and t < tAtencion + 0.4:
            x, y = _centro(*cel, t)
            a = e_back(pr(t, ti - 0.2, ti + 0.1)) * (1 - pr(t, tAtencion, tAtencion + 0.4))
            forma(im, rrect(x, y - 95, 34 * len(txt) * 0.62 + 30, 52, 10), rgb("fff6c8"), t, 13210 + cel[0], tinta=3, alfa=a)
            rotulo(im, txt, x, y - 95, 30, rgb("2b3f8a"), t, seed=13220 + cel[0], tinta=False, alfa=a)
    if t > tPalabra - 0.2 and t < tAtencion:
        rotulo(im, "= UNA PALABRA VISUAL", 1620, 650, 46, AMARILLO * 0.85, t, seed=13230, esc=e_back(pr(t, tPalabra - 0.2, tPalabra + 0.1)))
    # ATENCIÓN: el pedazo de pelo lanza hilos a todos
    if t > tAtencion - 0.2:
        rotulo(im, "ATENCIÓN", 1580, 140, 96, AMARILLO * 0.9, t, seed=13240, esc=e_back(pr(t, tAtencion - 0.2, tAtencion + 0.1)))
        pa = _centro(*PELO, t)
        u = e_out(pr(t, tMira - 0.2, tMira + 0.8)) * (1 - 0.7 * pr(t, tPelo4 - 0.3, tPelo4 + 0.3))
        for j in range(NR):
            for i in range(NC):
                if (i, j) != PELO and u > 0.02:
                    _hilo(im, pa, _centro(i, j, t), 2.2, rgb("3f78c8"), 0.5 * u, 13300 + i + NC * j, t)
        if t > tQuien - 0.3 and t < tPelo4:
            globo(im, 1560, 470, 560, 170, "", t, px=34, n=60 * pr(t, tQuien - 0.3, tQuien + 1.5),
                  lineas=["¿QUIÉN DE USTEDES", "ME AYUDA A ENTENDER", "LO QUE SOY?"], seed=13350, cola=(-1, 1))
    # pelo ↔ oreja ↔ bigote
    for k, (cel, ti) in enumerate(((OREJA, tOreja4), (BIGOTE, tBigote))):
        if t > ti - 0.2 and t < tTecla5 + 0.3:
            a = e_out(pr(t, ti - 0.2, ti + 0.3)) * (1 - pr(t, tTecla5, tTecla5 + 0.3))
            pa, pb = _centro(*PELO, t), _centro(*cel, t)
            brillo(im, pb[0], pb[1], 70, AMARILLO, 0.5 * a)
            _hilo(im, pa, pb, 9 * a, AMARILLO * 0.9, 0.95 * a, 13400 + k, t)
    if t > tPelo4 - 0.2 and t < tTecla5:
        pa = _centro(*PELO, t)
        brillo(im, pa[0], pa[1], 70, AMARILLO, 0.5)
    if t > tSomos - 0.2 and t < tTecla5 + 0.2:
        rotulo(im, "¡SOMOS UN GATO!", 1600, 520, 72, rgb("e8933a"), t, seed=13410, esc=e_back(pr(t, tSomos - 0.2, tSomos + 0.1)), rot=-0.04)
    # tecla ↔ gato: la escena completa
    if t > tTecla5 - 0.2:
        a = e_out(pr(t, tGato5 - 0.3, tGato5 + 0.3))
        pa = _centro(*TECLA, t)
        brillo(im, pa[0], pa[1], 70, rgb("7fd3e8"), 0.6)
        for k, cel in enumerate((CUERPO, PELO, BIGOTE)):
            _hilo(im, pa, _centro(*cel, t), 8 * a, rgb("7fd3e8"), 0.9 * a, 13420 + k, t)
        if t > tEscena - 0.2:
            forma(im, rrect(CX, 1010, 980, 80, 16), BLANCO, t, 13430, tinta=4, alfa=e_back(pr(t, tEscena - 0.2, tEscena + 0.1)))
            rotulo(im, "UN GATO ACOSTADO SOBRE UN TECLADO", CX, 1010, 46, TINTA, t, seed=13431, tinta=False,
                   esc=e_back(pr(t, tEscena - 0.2, tEscena + 0.1)))
    return im


# ------------------------------------------------------------ el título del artículo
def titulo(t):
    im = papel("calido")
    e = e_back(pr(t, tTitulo - 0.3, tTitulo + 0.2))
    forma(im, rrect(820, 540, 1040 * e, 760 * e, 10, -0.02), BLANCO, t, 13500, tinta=4, sombra=(rgb("d8c9a6"), 14, 18, 0.5))
    if e > 0.6:
        rotulo(im, "AN IMAGE IS WORTH", 820, 300, 70, TINTA, t, seed=13510, tinta=False)
        rotulo(im, "16×16 WORDS", 820, 400, 96, rgb("b8443a"), t, seed=13511, fuente="seguisym.ttf")
        rotulo(im, "Dosovitskiy y otros · 2020", 820, 480, 32, TINTA * 1.4, t, seed=13512, tinta=False)
        for k in range(7):
            linea(im, [(420, 560 + 50 * k), (1220 - 120 * (k % 3), 560 + 50 * k)], 4, col=rgb("b9b2a6"), seed=13520 + k, t=t,
                  punta=False)
        pegar(im, foto_gato(t)[:, :], 1060, 760, 0.35, 0.04, t=t, seed=13530, marco=6)
    if t > tVale - 0.2:
        rotulo(im, "UNA IMAGEN VALE 16 × 16 PALABRAS", W / 2, 1000, 64, AMARILLO, t, seed=13540,
               esc=e_back(pr(t, tVale - 0.2, tVale + 0.1)), fuente="seguisym.ttf")
    kuri(im, 1620, 470, 1.7, t, cara="feliz")
    return im


TRAMOS = [(chat, T_INI), (rompecabezas, tCortan - 0.5), (titulo, tTitulo - 0.5)]


def cuadro_crudo(t):
    k = 0
    for i, (_, ti) in enumerate(TRAMOS):
        if t >= ti:
            k = i
    f, ti = TRAMOS[k]
    im = f(t)
    if t < ti + 0.6:
        if k > 0:
            im = desborde(TRAMOS[k - 1][0](t), im, pr(t, ti, ti + 0.6), W * (0.35 + 0.15 * k), H * 0.5)
        else:
            import plano_g
            im = desborde(plano_g.cuadro_crudo(t), im, pr(t, ti, ti + 0.6), W * 0.5, H * 0.5)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
