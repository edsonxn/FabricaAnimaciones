# -*- coding: utf-8 -*-
"""CIERRE: de vuelta al cuarto (la niña, Kuri y la foto): «recuerda el viaje» → el camino que sube por dentro de Kuri con sus
paradas: píxeles, filtros, pisos (formas, partes, objetos), perillas, el mapa de estrellas → la foto se disuelve en su patrón
y le cuelga la etiqueta «GATO» → la torre crece hacia arriba sin fin, botón de suscribirse pintado y Kuri feliz."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lerp, linea, pr, rgb, rotulo, rrect,
                      suave, terminar)
from comun import T0, T1, TOTAL, desborde, ww
from fondos_ia import cabeza, cuarto, papel
from iconos_ia import PISOS_COL, estrella, perilla, torre, trazo
from personajes import AMARILLO, BLANCO, OJO_K, destello, kuri
from personajes_ia import celda, foto_gato, nina, pegar

E = "cierre"
T_INI = T0(E)
tProxima, tViaje = ww(E, 0, "proxima"), ww(E, 0, "viaje")
tPix, tFiltros, tPisos, tObjetos = ww(E, 1, "pixeles"), ww(E, 1, "filtros"), ww(E, 1, "pisos"), ww(E, 1, "objetos")
tPerillas, tMapa, tJuntas = ww(E, 2, "perillas"), ww(E, 2, "mapa"), ww(E, 2, "juntas")
tNoVio, tPatron, tLlamo = ww(E, 3, "vio"), ww(E, 3, "patron"), ww(E, 3, "llamo")
tCabeza, tSuscribete, tKuri, tPisosK = ww(E, 4, "cabeza"), ww(E, 4, "suscribete"), ww(E, 4, "kuri"), ww(E, 4, "pisos")
T_FIN = TOTAL
ROJO = rgb("e35d4a")


def viaje(t):
    im = cuarto()
    foto = foto_gato(t)

    def sostiene(im_, manos):
        pegar(im_, foto, manos[1][0] + 200, manos[1][1] - 60, 0.6, 0.06, t=t, seed=16001, marco=14)
    p = nina(im, 520, 600, 1.55, t, cara="normal", boca="sonrisa", brazos=(0.3, 1.5), codos=(0.4, 0.3), mira=1.0)
    sostiene(im, p["manos"])
    kuri(im, 1440, 470, 2.4, t, cara="feliz")
    if t > tViaje - 0.3:
        rotulo(im, "RECUERDA EL VIAJE", W / 2, 120, 90, AMARILLO, t, seed=16010, esc=e_back(pr(t, tViaje - 0.3, tViaje)), rot=-0.03)
    return im


PARADAS = [("PÍXELES", "pix"), ("FILTROS", "fil"), ("PISOS", "pis"), ("PERILLAS", "per"), ("EL MAPA", "map")]


def _icono(im, cual, x, y, e, t):
    import plano_d
    if cual == "pix":
        for j in range(3):
            for i in range(3):
                celda(im, x + (i - 1) * 46 * e, y + (j - 1) * 46 * e, 42 * e, rgb(["e8a33a", "c87428", "f2c27a"][(i + j) % 3]), t,
                      seed=16100 + i + 3 * j, numeros=False)
    elif cual == "fil":
        pegar(im, plano_d._mapa("vertical"), x, y, 0.3 * e, 0, t=t, seed=16110, marco=6, marco_col=rgb("2b3648"))
    elif cual == "pis":
        for k in range(4):
            forma(im, rrect(x, y + 50 * e - 34 * k * e, (150 - 24 * k) * e, 30 * e, 6), PISOS_COL[k], t, 16120 + k, tinta=2.6)
    elif cual == "per":
        for k in range(3):
            perilla(im, x + (k - 1) * 60 * e, y, 24 * e, t, math.sin(t * 2 + k), seed=16130 + k)
    else:
        for k in range(6):
            estrella(im, x + 60 * e * math.cos(k * 1.1), y + 40 * e * math.sin(k * 1.7), 6 * e, t, rgb("ffe9a8"), 1.0, seed=16140 + k)


def camino(t):
    im = cabeza()
    tiempos = [tPix, tFiltros, tPisos, tPerillas, tMapa]
    pts = [(260 + 350 * k, 900 - 165 * k) for k in range(5)]
    linea(im, curva(pts, 12), 8, col=OJO_K * 0.7, seed=16200, t=t, alfa=0.6, punta=False)
    act = -1
    for k, ((nom, cual), (x, y), ti) in enumerate(zip(PARADAS, pts, tiempos)):
        e = e_back(pr(t, ti - 0.3, ti + 0.1))
        forma(im, elipse(x, y, 120, 120), rgb("16323c") * 1.4, t, 16210 + k, tinta=4, alfa=0.9)
        if e > 0.02:
            act = k
            brillo(im, x, y, 150, AMARILLO, 0.35 * e)
            _icono(im, cual, x, y, e, t)
            rotulo(im, nom, x, y + 160, 44, AMARILLO, t, seed=16230 + k, esc=e)
    if act >= 0 and t > tPisos:                                     # «formas, partes y objetos» bajo los pisos
        x, y = pts[2]
        rotulo(im, "FORMAS · PARTES · OBJETOS", x + 40, y + 215, 30, BLANCO, t, seed=16240,
               esc=e_back(pr(t, tPisos + 0.3, tPisos + 0.6)), alfa=1 - pr(t, tPerillas - 0.4, tPerillas))
    if t > tPerillas + 0.6:
        x, y = pts[3]
        rotulo(im, "NADIE LAS GIRÓ A MANO", x + 40, y + 215, 30, BLANCO, t, seed=16241, esc=e_back(pr(t, tPerillas + 0.6, tPerillas + 0.9)),
               alfa=1 - pr(t, tMapa - 0.4, tMapa))
    if t > tJuntas - 0.3:
        x, y = pts[4]
        rotulo(im, "IMÁGENES Y PALABRAS, JUNTAS", x - 120, y + 215, 30, BLANCO, t, seed=16242, esc=e_back(pr(t, tJuntas - 0.3, tJuntas)))
    # Kuri sube por el camino hasta la parada actual
    if act >= 0:
        ti = tiempos[act]
        k0 = max(0, act - 1)
        u = e_out(pr(t, ti - 0.3, ti + 0.5))
        kx = lerp(pts[k0][0], pts[act][0], u) if act else pts[0][0]
        ky = lerp(pts[k0][1], pts[act][1], u) if act else pts[0][1]
        kuri(im, kx + 40, ky - 190 + 10 * math.sin(t * 3), 1.0, t, cara="feliz")
    return im


def patron(t):
    im = papel("calido")
    import plano_d
    u = suave(pr(t, tPatron - 0.3, tPatron + 1.0))
    f = foto_gato(t)
    m = plano_d._mapa("vertical")
    mix = f * (1 - u) + m * u
    pegar(im, mix, W / 2 - 160, 520, 1.25, -0.02, t=t, seed=16300, marco=16)
    rotulo(im, "NO VIO UN GATO", W / 2 - 160, 110, 80, TINTA, t, seed=16301, esc=e_back(pr(t, tNoVio - 0.3, tNoVio)), tinta=False)
    if t > tPatron - 0.2:
        rotulo(im, "ENCONTRÓ EL PATRÓN", 1560, 340, 56, AMARILLO * 0.85, t, seed=16302, esc=e_back(pr(t, tPatron - 0.2, tPatron + 0.1)))
    if t > tLlamo - 0.6:                                             # la etiqueta que le cuelga
        a = e_back(pr(t, tLlamo - 0.6, tLlamo - 0.2))
        linea(im, [(W / 2 + 160, 320), (1560, 560)], 4, seed=16310, t=t, alfa=a)
        forma(im, rrect(1600, 620, 300 * a, 120 * a, 18, 0.08), rgb("fff6c8"), t, 16311, tinta=4)
        rotulo(im, "«GATO»", 1600, 620, int(64 * a) + 2, rgb("2b3f8a"), t, seed=16312, tinta=False, rot=0.08)
        rotulo(im, "EN MILLONES DE EJEMPLOS", 1560, 800, 40, TINTA, t, seed=16313, tinta=False, esc=a)
    return im


def suscribete(t):
    im = cabeza()
    sube = e_in(pr(t, tPisosK - 0.4, tPisosK + 2.0))
    y0 = 1010 + 900 * sube
    torre(im, t, x=640, y0=y0, w=640, alto_p=170, crece=1.0, activo=(0.6, 0.6, 0.6, 0.6))
    for k in range(5, 12 if sube > 0.02 else 5):                    # pisos nuevos que siguen apareciendo arriba
        y = y0 - 170 * k - 85 - 140
        if y < -100:
            break
        forma(im, rrect(640, y, 640 - 30 * k, 150, 14), PISOS_COL[k % 4] * 0.9, t, 16400 + k, tinta=4.4)
        rotulo(im, "?", 640, y, 70, TINTA, t, seed=16420 + k, tinta=False)
    kuri(im, 1450, 520, 2.6, t, cara="feliz", brazos=(0.5, 1.8))
    if t > tSuscribete - 0.3:
        e = e_back(pr(t, tSuscribete - 0.3, tSuscribete + 0.1))
        click = 1 - 0.08 * math.sin(math.pi * pr(t, tSuscribete + 0.4, tSuscribete + 0.7))
        forma(im, rrect(1450, 900, 560 * e * click, 120 * e * click, 30), ROJO, t, 16430, tinta=5, luz=(BLANCO, -20, 20, 0.35))
        rotulo(im, "SUSCRÍBETE", 1450, 900, int(60 * e) + 2, BLANCO, t, seed=16431)
        destello(im, 1760, 820, 0.9 * pr(t, tSuscribete + 0.4, tSuscribete + 0.8), t, seed=1070)
    if t > tCabeza - 0.3:
        rotulo(im, "¿QUÉ PASA DENTRO DE OTRA CABEZA?", W / 2, 90, 60, BLANCO, t, seed=16440, esc=e_back(pr(t, tCabeza - 0.3, tCabeza)),
               alfa=1 - pr(t, tPisosK - 0.3, tPisosK))
    if t > tPisosK - 0.2:
        rotulo(im, "¡MUCHOS PISOS POR ENSEÑARTE!", W / 2, 90, 70, AMARILLO, t, seed=16441, esc=e_back(pr(t, tPisosK - 0.2, tPisosK + 0.1)))
    return im


TRAMOS = [(viaje, T_INI), (camino, tPix - 0.4), (patron, tNoVio - 0.8), (suscribete, tCabeza - 0.6)]


def cuadro_crudo(t):
    k = 0
    for i, (_, ti) in enumerate(TRAMOS):
        if t >= ti:
            k = i
    f, ti = TRAMOS[k]
    im = f(t)
    if t < ti + 0.6:
        if k > 0:
            im = desborde(TRAMOS[k - 1][0](t), im, pr(t, ti, ti + 0.6), W * (0.3 + 0.12 * k), H * 0.5)
        else:
            import plano_j
            im = desborde(plano_j.cuadro_crudo(t), im, pr(t, ti, ti + 0.6), W * 0.5, H * 0.5)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
