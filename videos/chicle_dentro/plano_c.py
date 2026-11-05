# -*- coding: utf-8 -*-
"""BAJADA: corte lateral de la cabeza → la lengua empuja la bolita (con Kuri encima) → la EPIGLOTIS se cierra sobre la
tráquea («PULMONES» tachado) → cae al esófago → regla de 25 cm → anillos de músculo que bajan apretando (peristalsis) +
recuadro del tubo de pasta de dientes → recuadro de la niña DE CABEZA tragando → el chicle llega abajo."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb, rotulo,
                      rrect, suave, terminar)
from comun import T0, desborde, ww
from fondos_chicle import perfil
from iconos_ia import marca_x
from personajes import AMARILLO, BLANCO, kuri
from personajes_ia import nina
from piezas_chicle import ROJO, chicle

T_INI = T0("bajada")
B = "bajada"
tViaje = ww(B, 0, "viaje")
tLengua, tAtras, tEpi, tPulmones, tCae = (ww(B, 1, "lengua"), ww(B, 1, "atras"), ww(B, 1, "epiglotis"), ww(B, 1, "pulmones"),
                                          ww(B, 1, "esofago"))
tTubo, tCm, tGrav, tOndas, tPasta = (ww(B, 2, "tubo"), ww(B, 2, "centimetros"), ww(B, 2, "gravedad"), ww(B, 2, "ondas"),
                                     ww(B, 2, "pasta"))
tCabeza, tSegundos, tEstom = ww(B, 3, "cabeza"), ww(B, 3, "segundos"), ww(B, 3, "estomago")

RUTA = np.array([(1250, 478), (1150, 470), (1050, 478), (975, 530), (945, 620), (940, 760), (940, 900), (940, 1040), (940, 1130)],
                np.float32)


def _pos(u):
    """Punto a lo largo de RUTA (u 0..1, por longitud)."""
    d = np.sqrt(((RUTA[1:] - RUTA[:-1]) ** 2).sum(1))
    s = np.concatenate([[0], np.cumsum(d)]) / d.sum()
    return np.interp(u, s, RUTA[:, 0]), np.interp(u, s, RUTA[:, 1])


def _u(t):
    a = 0.30 * e_out(pr(t, tLengua - 0.2, tAtras + 0.4))                    # por la lengua hasta la faringe
    b = 0.10 * e_in(pr(t, tCae - 0.3, tCae + 0.3))                           # cae al esófago
    c = 0.45 * suave(pr(t, tOndas - 0.2, tCabeza - 0.5))                     # baja empujado por las ondas
    d = 0.20 * e_in(pr(t, tSegundos - 0.4, tEstom + 0.2))                    # llega abajo
    return a + b + c + d


def recuadro(im, cx, cy, w, h, t, seed, e):
    forma(im, rrect(cx, cy, w * e + 2, h * e + 2, 24), rgb("fbf3df"), t, seed, tinta=4.4, sombra=(rgb("d8cfb8"), 10, 10, 0.55))


def pasta(im, cx, cy, t, e, aprieta):
    """Tubo de pasta de dientes que se aprieta por la mitad y la pasta sale."""
    w = 300 * e
    k = 1 - 0.45 * aprieta
    pts = [(cx - w * 0.6, cy - 50 * e), (cx, cy - 50 * e * k), (cx + w * 0.45, cy - 40 * e), (cx + w * 0.55, cy - 22 * e),
           (cx + w * 0.55, cy + 22 * e), (cx + w * 0.45, cy + 40 * e), (cx, cy + 50 * e * k), (cx - w * 0.6, cy + 50 * e)]
    forma(im, curva(pts, 5, True), rgb("4f86c6"), t, 9500, tinta=3.6, luz=(BLANCO, 0, -10, 0.3))
    forma(im, rrect(cx + w * 0.6, cy, 30 * e + 1, 40 * e + 1, 6), BLANCO, t, 9501, tinta=3)
    sale = 120 * e * aprieta
    if sale > 4:
        forma(im, rrect(cx + w * 0.62 + sale / 2 + 14 * e, cy, sale, 26 * e, 12 * e), rgb("e9f4f6"), t, 9502, tinta=2.6)
    for d in (-1, 1):                                                             # dedos que aprietan
        forma(im, elipse(cx, cy + d * (50 * e * k + 26 * e), 36 * e + 1, 24 * e + 1), rgb("f4cfae"), t, 9503 + d, tinta=3)


def cuadro_crudo(t):
    im = perfil()
    if t > tViaje - 0.3 and t < tLengua:
        rotulo(im, "¡EMPIEZA EL VIAJE!", 420, 150, 84, AMARILLO, t, seed=9400, rot=-0.05, esc=e_back(pr(t, tViaje - 0.3, tViaje)))
    # la epiglotis: tapita que se cierra sobre la tráquea
    cierra = e_out(pr(t, tEpi, tEpi + 0.4)) * (1 - pr(t, tTubo, tTubo + 0.5))
    ang = lerp(-1.3, 0.05, cierra)
    ex, ey = 1062, 640
    forma(im, np.array([(ex, ey), (ex - 70 * math.cos(ang), ey + 70 * math.sin(ang) - 8), (ex - 72 * math.cos(ang), ey + 70 * math.sin(ang) + 8)],
                       np.float32), rgb("f2a0a8"), t, 9410, tinta=3)
    if tEpi - 0.2 < t < tTubo:
        e = e_back(pr(t, tEpi - 0.2, tEpi + 0.1))
        linea(im, [(1080, 640), (1380, 720)], 3, seed=9411, t=t, alfa=0.6 * e, punta=False)
        rotulo(im, "EPIGLOTIS", 1540, 730, 64, ROJO, t, seed=9412, esc=e)
    if tPulmones - 0.2 < t < tTubo:
        e = e_back(pr(t, tPulmones - 0.2, tPulmones + 0.1))
        rotulo(im, "A LOS PULMONES", 1350, 960, 54, rgb("2f4f86"), t, seed=9413, esc=e)
        marca_x(im, 1030, 960, 0.7 * e, t, seed=9414)
    if tCae - 0.2 < t < tOndas:
        rotulo(im, "ESÓFAGO", 700, 760, 72, rgb("2f4f86"), t, seed=9420, esc=e_back(pr(t, tCae - 0.2, tCae + 0.1)))
    # regla de 25 cm
    if tCm - 0.4 < t < tOndas + 0.3:
        e = e_back(pr(t, tCm - 0.4, tCm)) * (1 - pr(t, tOndas, tOndas + 0.3))
        forma(im, rrect(840, 880, 40, 500 * e + 2, 6), rgb("f2d36a"), t, 9430, tinta=3)
        for k in range(11):
            y = 880 - 240 * e + k * 48 * e
            linea(im, [(820, y), (840, y)], 2.4, seed=9431 + k, t=t, punta=False)
        rotulo(im, "25 cm", 690, 880, 70, ROJO, t, seed=9440, esc=e)
    if tGrav - 0.2 < t < tPasta:
        rotulo(im, "NO ES GRAVEDAD", 520, 160, 70, ROJO, t, seed=9445, esc=e_back(pr(t, tGrav - 0.2, tGrav + 0.1)))
    # ondas de músculo (peristalsis) que bajan detrás de la bolita
    u = _u(t)
    gx, gy = _pos(u)
    if tOndas - 0.4 < t < tEstom + 0.3:
        for k in range(2):
            yy = gy - 70 - k * 170
            if 640 < yy < 1120:
                for d in (-1, 1):
                    linea(im, curva([(940 + d * 42, yy - 40), (940 + d * 18, yy), (940 + d * 42, yy + 40)], 5), 10, col=rgb("7a2a34"),
                          seed=9450 + k * 3 + d, t=t)
        if t < tCabeza:
            rotulo(im, "ONDAS DE MÚSCULO", 560, 1000, 60, BLANCO, t, seed=9460, esc=e_back(pr(t, tOndas - 0.2, tOndas + 0.1)))
    # la bolita con Kuri montado
    if u < 0.995:
        chicle(im, gx, gy, 34, t, seed=9470)
        kuri(im, gx + 6, gy - 46, 0.32, t, cara="feliz" if u < 0.35 else "susto", aura=False)
    # recuadros: pasta de dientes, niña de cabeza
    if tPasta - 0.6 < t < tCabeza - 0.1:
        e = e_back(pr(t, tPasta - 0.6, tPasta - 0.3)) * (1 - pr(t, tCabeza - 0.4, tCabeza - 0.1))
        recuadro(im, 1560, 300, 560, 360, t, 9480, e)
        pasta(im, 1530, 300, t, e, suave(pr(t, tPasta, tPasta + 0.7)))
    if t > tCabeza - 0.3:
        e = e_back(pr(t, tCabeza - 0.3, tCabeza))
        if e > 0.02:
            recuadro(im, 1560, 330, 520, 520, t, 9490, e)
            nina(im, 1560, 300, 0.95 * e, t, rot=math.pi, cara="feliz", boca="o", brazos=(0.4, 0.4))
            yb = 300 + 60 * e - 160 * e * pr(t, tCabeza, tSegundos)
            chicle(im, 1560, yb, 16 * e + 1, t, seed=9491, dientes=False)
            rotulo(im, "¡DE CABEZA!", 1560, 640, 60, AMARILLO, t, seed=9492, esc=e)
    if t > tEstom - 0.4:                                                          # sigue: el estómago
        e = e_back(pr(t, tEstom - 0.4, tEstom))
        rotulo(im, "AL ESTÓMAGO", 1250, 960, 72, ROJO, t, seed=9493, rot=-0.04, esc=e)
        linea(im, [(1100, 990), (990, 1060)], 6 * e + 1, seed=9494, t=t)
    lupa(im, t, u, gx, gy)
    return im


def lupa(im, t, u, gx, gy):
    """Los viajeros en grande (Kuri sentado en la bolita) dentro de una lupa con su hilo hasta la bolita diminuta."""
    e = e_back(pr(t, T_INI + 0.2, T_INI + 0.6))
    if e < 0.02:
        return
    lx, ly, lr = 300, 470, 205 * e
    if u < 0.995:
        linea(im, [(lx + lr * 0.95, ly + lr * 0.2), (gx - 30, gy)], 3, seed=9600, t=t, alfa=0.4, punta=False)
    dentro = u > 0.3
    forma(im, elipse(lx, ly, lr, lr), rgb("e8a39a") if dentro else rgb("f3b8b0"), t, 9601, tinta=6,
          sombra=(rgb("c9a29a"), 8, 12, 0.5))
    baja = tOndas - 0.4 < t < tEstom + 0.6
    if baja:                                                                      # paredes que aprietan y rayitas de velocidad
        apr = 0.5 + 0.5 * math.sin(t * 6)
        for d in (-1, 1):
            linea(im, curva([(lx + d * lr * 0.85, ly - lr * 0.75), (lx + d * lr * (0.45 - 0.12 * apr), ly - lr * 0.35),
                             (lx + d * lr * 0.85, ly + lr * 0.05)], 5), 12 * e, col=rgb("7a2a34"), seed=9602 + d, t=t)
        for k in range(4):
            yk = ly - lr * 0.55 + ((t * 300 + k * 70) % 280) * e
            linea(im, [(lx - lr * 0.35 + k * lr * 0.22, yk), (lx - lr * 0.35 + k * lr * 0.22, yk + 40 * e)], 3, seed=9606 + k,
                  t=t, alfa=0.5, punta=False)
    bote = 8 * math.sin(t * 5)
    chicle(im, lx, ly + 70 * e + bote * 0.3, 88 * e, t, seed=9610, cara="feliz" if u < 0.3 else "susto")
    kuri(im, lx, ly - 66 * e + bote, 0.9 * e, t, cara="feliz" if u < 0.3 else ("susto" if baja else "normal"), aura=False,
         brazos=(2.1, 2.1) if baja else (0.6, 0.6))
    linea(im, [(lx + lr * 0.7, ly + lr * 0.7), (lx + lr * 1.05, ly + lr * 1.05)], 16 * e + 1, col=rgb("6b4a2e"), seed=9612,
          t=t, punta=False)


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
