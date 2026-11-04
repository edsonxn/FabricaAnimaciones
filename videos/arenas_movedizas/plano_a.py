# -*- coding: utf-8 -*-
"""0-28 s · GANCHO: paseo por la orilla → el suelo se traga las piernas → «¡ARENAS MOVEDIZAS!»
MITO: los sesenta (35 rollos, uno con arenas) → película sepia: el galán se hunde hasta la cabeza → «¡MENTIRA!» →
balanza (la arena pesa el doble) → corte: te hundes hasta la cintura… y flotas."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb,
                      rotulo, rrect, suave, terminar)
from comun import FIN, INI, T1, desborde, ww
from fondos_arena import Y_SECA, papel, playa, sepia
from personajes import AMARILLO, BLANCO, destello, exclama, gota, kuri, pregunta
from personajes_arena import (ARENA_HUM, ARENA_OSC, arena_frente, balanza, corte_arena, cubeta, explorador, gaviota,
                              heroe_cine, palmera)
from utileria import flecha

G, M = "gancho", "mito"
tPronto, tSuelo, tTraga = ww(G, 0, "pronto"), ww(G, 0, "suelo"), ww(G, 0, "traga")
tCaiste, tArenas, tMoved = ww(G, 1, "caiste"), ww(G, 1, "arenas"), ww(G, 1, "movedizas")
tSesenta, tUna, tPelis = ww(M, 0, "sesenta"), ww(M, 0, "una"), ww(M, 0, "peliculas")
tTenia, tSiempre, tHund, tCabeza = ww(M, 0, "tenia"), ww(M, 0, "siempre"), ww(M, 0, "hundian"), ww(M, 0, "cabeza")
tPero, tMint = ww(M, 1, "pero"), ww(M, 1, "mintieron")
tArena2, tPesa, tDoble = ww(M, 2, "arena"), ww(M, 2, "pesa"), ww(M, 2, "doble")
tHundes, tCintura, tFlotas = ww(M, 2, "hundes"), ww(M, 2, "cintura"), ww(M, 2, "flotas")

T_CINE = T1(G) + 0.1                 # entra la película
T_BAL = FIN(M, 1) + 0.35             # entra la balanza
T_CORTE = tHundes - 0.45             # entra el corte
Y_SUP = 1420                         # superficie de la arena movediza (vista de playa)
Y_C = 1050                           # superficie en el corte
S_EX = 1.6


def _kuri_flota(im, t, x=830, y=760, cara="normal", brazos=(0.5, 0.5), s=1.1):
    kuri(im, x + 18 * math.sin(t * 1.3), y + 22 * math.sin(t * 1.9), s, t, cara=cara, brazos=brazos)
    return x + 18 * math.sin(t * 1.3), y + 22 * math.sin(t * 1.9)


# ------------------------------------------------------------ gancho en la playa
def orilla(t):
    im = playa()
    for k in range(3):
        gaviota(im, (200 + 160 * t + k * 260) % (W + 200) - 100, 260 + 60 * k + 12 * math.sin(t * 2 + k), 0.9, t, seed=2700 + k)
    palmera(im, 70 - 40 * min(t, tPronto), 1180, 1.25, t)
    # la mancha húmeda de la arena movediza aparece bajo los pies
    u = suave(pr(t, tPronto - 0.1, tSuelo + 0.2))
    paseo = 1 - pr(t, tPronto - 0.3, tPronto + 0.2)
    ex = 540
    for k in range(5):                                   # huellas que se quedan atrás
        hx = ex - 120 - k * 150 - 0 * t
        hx -= 150 * ((t * 1.1) % 1) * paseo if t < tPronto else 0
        if hx > -40:
            lavado(im, elipse(hx, Y_SUP + 40 + (k % 2) * 34, 24, 11), rgb("b8925e"), 0.4, 60 + k)
    if u > 0:
        lavado(im, elipse(ex, Y_SUP + 60, 420 * u, 150 * u), ARENA_HUM, 0.8 * u, 77, humedo=16)
    # hundimiento: primero de golpe (traga), luego despacio
    h = 115 * e_out(pr(t, tSuelo, tTraga + 0.6)) + 30 * pr(t, tTraga + 0.6, T1(G))
    susto = t > tSuelo
    cara = "susto" if susto else ("parpadeo" if (t % 3.1) < 0.12 else "normal")
    boca = "grito" if tTraga < t < tTraga + 1.2 else ("o" if susto else "sonrisa")
    bra = (0.35 + 0.15 * math.sin(t * 7), 0.35 - 0.15 * math.sin(t * 7)) if not susto else (2.3 + 0.2 * math.sin(t * 13), 2.3 + 0.2 * math.cos(t * 13))
    sombrero = e_out(pr(t, tTraga, tTraga + 0.2)) * (1 - e_in(pr(t, tTraga + 0.35, tTraga + 0.7)))
    by = 1196 + h - (8 * abs(math.sin(t * 7)) * paseo)
    sx_ = 3 * math.sin(t * 50) * pr(t, tSuelo, tSuelo + 0.2) * (1 - pr(t, tTraga + 0.8, tTraga + 1.2))
    p = explorador(im, ex + sx_, by, S_EX, t, cara=cara, boca=boca, brazos=bra, codos=(0.5, 0.5), anda=paseo, sombrero=sombrero)
    arena_frente(im, Y_SUP, t, seed=3, x0=ex - 430, x1=ex + 430, onda=5 * u, alto=Y_SUP + 210, cuerpo=ex,
                 ondas_r=(t - tSuelo) * 160 if t > tSuelo else 0)
    if t > tTraga:                                       # salpicones de arena
        e = t - tTraga
        for k in range(7):
            a = -math.pi / 2 + (k - 3) * 0.4
            r = 60 + 420 * e
            yy = Y_SUP - 20 + math.sin(a) * r + 900 * e * e
            if e < 0.7:
                lavado(im, elipse(ex + math.cos(a) * r, yy, 16 - 12 * e, 14 - 10 * e), ARENA_HUM, 0.9, 400 + k)
    kc = "susto" if susto else ("feliz" if t < 2 else "normal")
    kx, ky = _kuri_flota(im, t, cara=kc, brazos=(1.5, 1.5) if susto else (0.5, 0.5))
    if t > tSuelo:
        exclama(im, kx, ky - 170, 1.3 * e_back(pr(t, tSuelo, tSuelo + 0.25)), t)
        exclama(im, p["cabeza"][0] - 150, p["cabeza"][1] - 190, 1.1 * e_back(pr(t, tTraga, tTraga + 0.25)), t, seed=1004)
    if t > tTraga + 0.5:
        for k in range(2):
            gota(im, p["cabeza"][0] + 110 + 10 * k, p["cabeza"][1] - 40 + 30 * k, 1.0, t, seed=1050 + k)
    if t > tArenas - 0.05:
        e1 = e_back(pr(t, tArenas - 0.05, tArenas + 0.25))
        rotulo(im, "¡ARENAS", 470, 360, 150, AMARILLO, t, seed=11, rot=-0.07, esc=e1)
    if t > tMoved - 0.05:
        e2 = e_back(pr(t, tMoved - 0.05, tMoved + 0.25))
        rotulo(im, "MOVEDIZAS!", 560, 520, 150, AMARILLO, t, seed=12, rot=-0.04, esc=e2)
    return terminar(im, t)


# ------------------------------------------------------------ los sesenta: 35 rollos y la película
def _rollo(im, x, y, r, t, col, seed):
    forma(im, elipse(x, y, r, r), col, t, seed, tinta=3.4)
    for k in range(5):
        a = k / 5 * 2 * math.pi + 0.3
        forma(im, elipse(x + 0.55 * r * math.cos(a), y + 0.55 * r * math.sin(a), 0.2 * r, 0.2 * r), rgb("2a2220"), t, seed + 1 + k,
              tinta=0)
    forma(im, elipse(x, y, 0.13 * r, 0.13 * r), rgb("2a2220"), t, seed + 9, tinta=0)


CUADRO = (110, 470, 970, 1500)        # recuadro de la película (x0, y0, x1, y1)
ROJO = rgb("d8463a")


def _escena_cine(im, t):
    """Lo que pasa DENTRO de la película: el galán se hunde hasta la cabeza (luego se pasa a sepia)."""
    x0, y0, x1, y1 = CUADRO
    sub = im[y0:y1, x0:x1]
    sub[:] = np.asarray(rgb("cfd8c8"), np.float32)
    ys = 1180
    for k in range(4):                                   # selva de cartón piedra
        forma(im, elipse(x0 + 80 + k * 260, ys - 90, 170, 120), rgb("6e8a5a") * (0.8 + 0.05 * k), t, 3300 + k, tinta=4)
    palmera(im, x0 + 60, ys - 40, 1.0, t, seed=3340)
    palmera(im, x1 - 260, ys - 40, 0.9, t, seed=3350)
    u = suave(pr(t, tSiempre - 0.2, tCabeza + 0.3))
    hy = lerp(ys - 420, ys + 40, u)
    heroe_cine(im, 540, hy, 1.6, t, mano=suave(pr(t, tCabeza - 0.2, tCabeza + 0.4)))
    pol = np.array([(x0 - 10, ys), (x1 + 10, ys), (x1 + 10, y1 + 10), (x0 - 10, y1 + 10)], np.float32)
    forma(im, pol, rgb("b8a07a"), t, 3310, tinta=4, sombra=(rgb("7d6a4a"), 0, -30, 0.4))
    for k in range(3):
        linea(im, elipse(540, ys + 20, 120 + 90 * k + 30 * math.sin(t * 2), 18 + 12 * k), 3, seed=3320 + k, t=t, cerrado=True,
              alfa=0.6, punta=False)
    if t > tCabeza:                                      # burbujas «glub»
        e = (t - tCabeza) % 0.8
        forma(im, elipse(500, ys - 20 - 140 * e, 14, 14), BLANCO, t, 3330, tinta=2.6, alfa=1 - e)


def cine(t):
    im = papel("cine")
    x0, y0, x1, y1 = CUADRO
    t_peli = tTenia - 0.2                             # el rollo marcado crece y se vuelve película
    if t < t_peli + 0.6:
        # «años sesenta»: 35 rollos en 5x7, uno rojo = el que tenía arenas movedizas
        for k in range(35):
            c, f = k % 5, k // 5
            x, y = 180 + c * 180, 520 + f * 160
            ap = e_back(pr(t, tUna + k * 0.035, tUna + k * 0.035 + 0.25))
            if ap <= 0:
                continue
            marcado = k == 17 and t > tPelis + 0.3
            r = 62 * ap * (1 + 0.25 * marcado * (1 + math.sin(t * 9)) * 0.5)
            if marcado and t > t_peli:
                r *= 1 + 6 * e_in(pr(t, t_peli, t_peli + 0.6))
            _rollo(im, x, y, r, t, ROJO if marcado else rgb("d9cdb5"), 3400 + k)
        rotulo(im, "AÑOS 60", 540, 280, 170, rgb("f2d89a"), t, seed=21, esc=e_back(pr(t, tSesenta - 0.2, tSesenta + 0.1)))
        if t > tPelis + 0.3:
            rotulo(im, "1 DE CADA 35", 540, 1700, 120, ROJO * 1.15, t, seed=22, esc=e_back(pr(t, tPelis + 0.3, tPelis + 0.6)))
    if t > t_peli + 0.3:
        u = pr(t, t_peli + 0.3, t_peli + 0.8)
        peli = np.zeros_like(im)
        peli[:] = im
        forma(peli, rrect((x0 + x1) / 2, (y0 + y1) / 2, x1 - x0 + 120, y1 - y0 + 60, 18), rgb("1c1714"), t, 3500, tinta=5)
        for k in range(9):                               # perforaciones
            for xx in (x0 - 35, x1 + 35):
                forma(peli, rrect(xx, y0 + 40 + k * 120, 34, 50, 8), rgb("efe6d2"), t, 3510 + k + (xx > 500) * 20, tinta=2)
        tmp = peli.copy()                                # la escena se recorta al cuadro de la película
        _escena_cine(tmp, t)
        peli[y0:y1, x0:x1] = tmp[y0:y1, x0:x1]
        sepia(peli, x0, y0, x1, y1, t)
        rotulo(peli, "AÑOS 60", 540, 300, 150, rgb("f2d89a"), t, seed=21)
        im = desborde(im, peli, u, cx=540, cy=980, borde=(0.2, 0.15, 0.12))
    if t > tPero:                                        # «¡MENTIRA!»: sello rojo y la película se rasga
        e = pr(t, tMint - 0.05, tMint + 0.18)
        if e > 0:
            rotulo(im, "¡MENTIRA!", 540, 980, 190, ROJO, t, seed=23, rot=-0.2, esc=lerp(2.2, 1.0, e_out(e)), alfa=min(1, e * 3))
        kuri(im, 880, 1660, 1.0, t, cara="apretados", brazos=(1.2 + 0.4 * math.sin(t * 12), 1.2 - 0.4 * math.sin(t * 12)))
    return terminar(im, t, calido=True)


# ------------------------------------------------------------ balanza: la arena pesa el doble
def _balanza(t):
    im = papel("calido")
    incl = 0.32 * e_back(pr(t, tPesa, tDoble + 0.3), 1.3)
    pl = balanza(im, 540, 1000, 1.05, t, incl)
    lx, ly = pl[0]
    ap = e_back(pr(t, T_BAL - 0.1, T_BAL + 0.3))
    explorador(im, lx, ly - 205 * ap, 0.95 * ap + 0.01, t, cara="abiertos" if t > tPesa else "normal",
               boca="o" if t > tDoble else "sonrisa", brazos=(0.6, 0.6))
    rx, ry = pl[1]
    c = e_back(pr(t, tArena2 - 0.1, tArena2 + 0.25))
    if c > 0:
        cubeta(im, rx, ry - 150 * c, 1.3 * c, t)
    if t > tDoble - 0.1:
        e = e_back(pr(t, tDoble - 0.1, tDoble + 0.2))
        rotulo(im, "PESA ×2", 640, 560, 170, AMARILLO, t, seed=31, rot=0.06, esc=e)
    kuri(im, 230, 470 + 20 * math.sin(t * 2), 1.0, t, cara="normal" if t < tDoble else "susto", brazos=(0.6, 1.6))
    if t > tDoble:
        pregunta(im, 230, 300, 1.0 * e_back(pr(t, tDoble, tDoble + 0.3)), t)
    return terminar(im, t)


# ------------------------------------------------------------ corte: hasta la cintura, y flotas
def corte(t, aprieta=0.0, patada=0.0, extra=None):
    """Vista en corte del pozo (la usan también los planos de la trampa)."""
    im = playa()
    flota = 10 * math.sin(t * 2.2) * pr(t, tFlotas - 0.2, tFlotas + 0.3)
    by = Y_C - 54 - (230 * (1 - e_out(pr(t, tHundes - 0.2, tCintura + 0.2)))) + flota
    pat = patada
    piernas = (0.25 * pat * math.sin(t * 15), 0.25 * pat * math.sin(t * 15 + 2)) if pat > 0 else None
    cara = "susto" if t < tFlotas else "feliz"
    boca = "o" if t < tFlotas else "sonrisa"
    if extra:
        cara, boca = extra.get("cara", cara), extra.get("boca", boca)
    bra = extra.get("brazos", (1.9, 1.9)) if extra else (1.9 + 0.2 * math.sin(t * 3), 1.9 + 0.2 * math.cos(t * 3))
    p = explorador(im, 540, by, S_EX, t, cara=cara, boca=boca, brazos=bra, codos=(0.3, 0.3), piernas=piernas,
                   anda=0.0, rodillas=(0.2 * pat, 0.2 * pat))
    corte_arena(im, Y_C, t, seed=5, aprieta=aprieta, cx=540, piernas_y=(by + 40, by + 230))
    linea(im, [(-20, Y_C), (W + 20, Y_C)], 6, seed=5001, t=t, punta=False)
    return im, p, by


def corte_flota(t):
    im, p, by = corte(t)
    if t > tCintura - 0.1:                              # línea de la cintura
        e = pr(t, tCintura - 0.1, tCintura + 0.3)
        for k in range(int(12 * e)):
            linea(im, [(120 + k * 72, Y_C - 4), (150 + k * 72, Y_C - 4)], 6, col=rgb("d8463a"), seed=5100 + k, t=t, punta=False)
        rotulo(im, "CINTURA", 200, Y_C + 70, 80, rgb("d8463a"), t, seed=41, esc=e_back(e))
    if t > tFlotas - 0.2:                               # flechas de empuje hacia arriba
        e = e_back(pr(t, tFlotas - 0.2, tFlotas + 0.2))
        for k, x in enumerate((360, 540, 720)):
            yy = 1640 - 30 * math.sin(t * 4 + k)
            flecha(im, x, yy, x, yy - 260 * e, 46, t, rgb("f2c14e"), seed=5200 + k)
        rotulo(im, "¡FLOTAS!", 540, 300, 150, AMARILLO, t, seed=42, esc=e)
        destello(im, p["cabeza"][0] - 140, p["cabeza"][1] - 120, 0.8 * e, t)
    _kuri_flota(im, t, x=860, y=640, cara="susto" if t < tFlotas else "feliz", brazos=(1.4, 1.4) if t > tFlotas else (0.6, 0.6))
    return terminar(im, t)


T_FIN = T1(M)


def cuadro(t):
    if t < T_CINE:
        return orilla(t)
    if t < T_CINE + 0.6:
        return desborde(orilla(t), cine(t), pr(t, T_CINE, T_CINE + 0.6), cx=540, cy=900, borde=(0.2, 0.15, 0.12))
    if t < T_BAL:
        return cine(t)
    if t < T_BAL + 0.6:
        return desborde(cine(t), _balanza(t), pr(t, T_BAL, T_BAL + 0.6), cx=300, cy=1000)
    if t < T_CORTE:
        return _balanza(t)
    if t < T_CORTE + 0.6:
        return desborde(_balanza(t), corte_flota(t), pr(t, T_CORTE, T_CORTE + 0.6), cx=540, cy=Y_C)
    return corte_flota(t)
