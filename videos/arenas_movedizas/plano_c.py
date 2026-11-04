# -*- coding: utf-8 -*-
"""48,3-73 s · CIERRE: «¡NO TIRES!» (tache sobre la cuerda) → se echa atrás (burbuja: flotando en una alberca) → corte:
piernas en círculos lentos y el agua entra entre los granos → la arena lo suelta («¡PLOP!», la bota se queda) → sentado y
embarrado con Kuri: Kuri hunde un rollo de película («mintieron») → «¡NO ENTRES EN PÁNICO!»."""
import math

import numpy as np

from acuarela import (H, W, clamp, curva, e_back, e_in, e_out, elipse, forma, lavado, lerp, linea, pr, rgb, rotulo, suave,
                      terminar)
from comun import FIN, INI, T1, desborde, ww
from fondos_arena import playa
from personajes import AMARILLO, BLANCO, corazon, destello, kuri
from personajes_arena import (AGUA, ARENA_HUM, BOTA, arena_frente, corte_arena, cuerda, explorador, flotador, gaviota,
                              hilos_agua, palmera, tache)
import plano_a as A

C = "cierre"
T_INI = T1("marea")
tPara, tNo, tTires = ww(C, 0, "para"), ww(C, 0, "no"), ww(C, 0, "tires")
tEchate, tAtras, tFlotaras, tAlberca = ww(C, 0, "echate"), ww(C, 0, "atras"), ww(C, 0, "flotaras"), ww(C, 0, "alberca")
tMueve, tDespacio, tCirculos, tEntre = ww(C, 1, "mueve"), ww(C, 1, "despacio"), ww(C, 1, "circulos"), ww(C, 1, "entre")
tPoco, tSuelta = ww(C, 2, "poco"), ww(C, 2, "suelta")
tPelis, tMint, tMenos, tCosa = ww(C, 3, "peliculas"), ww(C, 3, "mintieron"), ww(C, 3, "menos"), ww(C, 3, "cosa")
tNoP, tPanico = ww(C, 3, "no"), ww(C, 3, "panico")
T_CORTE = INI(C, 1) - 0.35
T_SALE = INI(C, 2) - 0.35
T_SENTADO = INI(C, 3) - 0.3
EX, Y_SUP = 540, A.Y_SUP
ROT = 1.15                                   # echado hacia atrás (de espaldas)


def _fondo(t, tarde=0.0, pozo_x=EX, pozo_r=430):
    im = playa(tarde)
    for k in range(2):
        gaviota(im, (300 + 120 * t + k * 420) % (W + 200) - 100, 300 + 80 * k, 0.8, t, seed=2760 + k)
    palmera(im, 70, 1180, 1.25, t)
    lavado(im, elipse(pozo_x, Y_SUP + 60, pozo_r, 150 * pozo_r / 430), ARENA_HUM, 0.8, 77, humedo=16)
    return im


# ------------------------------------------------------------ no tires · échate atrás
def echarse(t):
    im = _fondo(t)
    u = suave(pr(t, tEchate - 0.1, tAtras + 0.6))
    rot = ROT * u
    by = lerp(Y_SUP - 54, Y_SUP - 120, u)
    bx = lerp(EX, EX - 60, u)
    cara = "susto" if t < tEchate else ("normal" if t < tFlotaras else "feliz")
    p = explorador(im, bx, by, A.S_EX, t, rot=rot, cara=cara, boca="o" if t < tEchate else "sonrisa",
                   brazos=(lerp(1.0, 1.9, u), lerp(1.0, 1.9, u)), codos=(0.3, 0.3))
    arena_frente(im, Y_SUP, t, seed=3, x0=EX - 430, x1=EX + 430, onda=5, alto=Y_SUP + 210, cuerpo=EX)
    # Kuri tira… «no» → tache y suelta la cuerda
    suelta = pr(t, tNo + 0.3, tNo + 0.8)
    kx, ky = 820 + 10 * math.sin(t * 1.3), 900 + 16 * math.sin(t * 1.9) - 40 * (1 - suelta) * (0.5 + 0.5 * math.sin(t * 14))
    if suelta < 1:
        cuerda(im, (kx - 30, ky + 30), (EX + 90, Y_SUP + 30), t, tension=1 - suelta)
    kuri(im, kx, ky, 1.1, t, cara="apretados" if t < tNo else ("susto" if t < tEchate else "feliz"),
         brazos=(-0.6, -0.6) if suelta < 0.5 else (0.6, 0.6))
    if t > tNo - 0.1:
        e = pr(t, tNo - 0.1, tTires) * (1 - pr(t, tEchate - 0.3, tEchate))
        if e > 0:
            tache(im, (kx + EX + 90) / 2, (ky + Y_SUP) / 2, 130, t, u=min(1, e * 1.6))
            rotulo(im, "¡NO TIRES!", 540, 380, 160, AMARILLO, t, seed=61, rot=-0.06, esc=e_back(clamp(e * 2)))
    if t > tFlotaras - 0.2:                           # burbuja: flotando en una alberca
        e = e_back(pr(t, tFlotaras - 0.2, tFlotaras + 0.15))
        bx_, by_, r = 330, 460, 250 * e
        for k, (dx, dy, rr) in enumerate(((150, 240, 22), (200, 300, 14))):
            forma(im, elipse(bx_ + dx * e, by_ + dy * e, rr * e, rr * e), BLANCO, t, 6300 + k, tinta=3)
        forma(im, elipse(bx_, by_, r, r * 0.9), rgb("9fd6e6"), t, 6310, tinta=5, luz=(BLANCO, -20, 20, 0.3))
        for k in range(3):
            linea(im, [(bx_ - r * 0.7, by_ - 120 * e + k * 90 * e), (bx_ + r * 0.7, by_ - 110 * e + k * 90 * e)], 3, col=BLANCO,
                  seed=6320 + k, t=t, alfa=0.6, punta=False)
        flotador(im, bx_, by_ + 30 * e + 6 * math.sin(t * 2), 1.1 * e, t)
        explorador(im, bx_ - 10 * e, by_ - 10 * e + 6 * math.sin(t * 2), 0.62 * e + 0.01, t, rot=ROT, cara="feliz",
                   boca="sonrisa", brazos=(1.9, 1.9), seed=140)
    return terminar(im, t)


# ------------------------------------------------------------ corte: piernas en círculos y el agua entra
def circulos(t):
    im = playa()
    yc = A.Y_C
    bx, by = 600, yc - 20
    a = (t - tMueve) * 2.4
    pier = (0.55 + 0.35 * math.sin(a), 0.55 + 0.35 * math.sin(a + 1.6))
    p = explorador(im, bx, by, A.S_EX, t, rot=0.8, cara="normal" if t < tEntre else "feliz", boca="sonrisa",
                   brazos=(1.9, 1.9), codos=(0.3, 0.3), piernas=pier, rodillas=(0.3 + 0.2 * math.cos(a), 0.3 + 0.2 * math.cos(a + 1.6)))
    pies = np.array(p["pies"])
    agua = pr(t, tEntre - 0.2, tEntre + 0.9)
    corte_arena(im, yc, t, seed=5, aprieta=0.6 * (1 - agua), agua=agua, cx=float(pies[:, 0].mean()),
                piernas_y=(yc, float(pies[:, 1].max())), r_aflojar=260 * agua)
    linea(im, [(-20, yc), (W + 20, yc)], 6, seed=5001, t=t, punta=False)
    if t > tCirculos - 0.2:                           # flechas circulares punteadas en cada pie
        e = pr(t, tCirculos - 0.2, tCirculos + 0.4)
        for i, (fx, fy) in enumerate(pies):
            for k in range(int(10 * e)):
                g = k / 10 * 2 * math.pi + t * 2.4
                linea(im, [(fx + 95 * math.cos(g), fy + 65 * math.sin(g)), (fx + 95 * math.cos(g + 0.3), fy + 65 * math.sin(g + 0.3))],
                      11, col=AMARILLO, seed=6400 + 10 * i + k, t=t, punta=False)
    if t > tDespacio - 0.1:
        rotulo(im, "DESPACIO…", 540, 300, 140, AMARILLO, t, seed=62, esc=e_back(pr(t, tDespacio - 0.1, tDespacio + 0.2)))
    if agua > 0:
        hilos_agua(im, float(pies[:, 0].mean()), yc, float(pies[:, 1].max()), suave(agua), t)
        rotulo(im, "+ AGUA", 820, yc + 520, 110, rgb("bfe7f3"), t, seed=63, esc=e_back(pr(t, tEntre, tEntre + 0.3)))
    A._kuri_flota(im, t, x=860, y=620, cara="feliz" if t > tEntre else "normal", brazos=(0.5, 1.6))
    return terminar(im, t)


# ------------------------------------------------------------ la arena lo suelta · sentado con Kuri
PX = 690                                    # pozo de los planos finales (más chico, a la derecha)


def _bota_en_pozo(im, t, hunde=0.0):
    y = Y_SUP - 20 + 90 * hunde
    pts = np.array([(-26, -60), (26, -60), (30, 40), (-30, 40)], np.float32) + [PX + 60, y]
    forma(im, pts, BOTA, t, 6500, tinta=4.5, luz=(BLANCO, -4, 6, 0.15))
    forma(im, elipse(PX + 60, y - 60, 26, 9), rgb("4a2a18"), t, 6501, tinta=3)


def salir(t):
    im = _fondo(t, pozo_x=PX, pozo_r=320)
    u = e_in(pr(t, tPoco - 0.1, tSuelta + 0.1))
    bx = lerp(PX - 20, 300, u)
    by = Y_SUP - 120 - 20 * math.sin(u * math.pi)
    sin_bota = t > tSuelta
    explorador(im, bx, by, A.S_EX, t, rot=ROT, cara="apretados" if t < tSuelta else "feliz", boca="apretada" if t < tSuelta else "sonrisa",
               brazos=(1.9, 1.9), codos=(0.3, 0.3), bota_izq=not sin_bota, barro=0.6)
    arena_frente(im, Y_SUP, t, seed=3, x0=PX - 320, x1=PX + 320, onda=5, alto=Y_SUP + 160, cuerpo=PX)
    if sin_bota:
        _bota_en_pozo(im, t)
        e = pr(t, tSuelta, tSuelta + 0.2) * (1 - pr(t, T_SENTADO - 0.3, T_SENTADO))
        rotulo(im, "¡PLOP!", PX + 60, Y_SUP - 260, 140, AMARILLO, t, seed=64, rot=0.1, esc=e_back(e))
    A._kuri_flota(im, t, x=820, y=820, cara="feliz", brazos=(1.5, 1.5) if t > tSuelta else (0.6, 0.6))
    return terminar(im, t)


def sentado(t):
    im = _fondo(t, tarde=0.35, pozo_x=PX, pozo_r=320)
    dedo = pr(t, tMenos - 0.1, tMenos + 0.2) * (1 - pr(t, tPanico + 0.6, tPanico + 1.0))
    p = explorador(im, 300, 1330, A.S_EX, t, cara="feliz" if t < tMenos or t > tPanico + 0.4 else "normal",
                   boca="sonrisa", brazos=(0.4, lerp(0.5, 2.9, e_out(dedo))), codos=(0.3, lerp(0.4, 0.0, dedo)),
                   piernas=(1.25, 1.25), rodillas=(-0.6, -0.6), bota_izq=False, barro=1.0)
    arena_frente(im, Y_SUP, t, seed=3, x0=PX - 320, x1=PX + 320, onda=5, alto=Y_SUP + 160, cuerpo=None)
    hunde = pr(t, tPanico + 0.8, T1(C) - 0.2)
    _bota_en_pozo(im, t, hunde=hunde)
    if hunde > 0.05:                               # «glub» de la bota
        e = (t * 1.4) % 1
        forma(im, elipse(PX + 50, Y_SUP - 30 - 120 * e, 12, 12), BLANCO, t, 6510, tinta=2.4, alfa=1 - e)
    # Kuri: abrazo, luego hunde un rollo de película en el pozo
    tira_r = pr(t, tPelis - 0.2, tMint + 0.4)
    kx = lerp(470, 640, suave(pr(t, tPelis - 0.3, tPelis + 0.3))) if t < tMenos else lerp(640, 470, suave(pr(t, tMenos, tMenos + 0.5)))
    ky = 1120 + 16 * math.sin(t * 1.9)
    kuri(im, kx, ky, 1.1, t, cara="feliz" if t < tPelis or t > tMint + 0.5 else "apretados",
         brazos=(1.6 + 0.3 * math.sin(t * 8), 1.6 + 0.3 * math.cos(t * 8)) if t > tNoP else (0.9, 0.9))
    if t < tPelis:
        corazon(im, (kx + 300) / 2, 960 + 10 * math.sin(t * 3), 0.8 * e_back(pr(t, T_SENTADO, T_SENTADO + 0.4)), t)
    if tPelis - 0.2 < t < tMenos:                  # el rollo: Kuri lo trae, lo tira y se hunde
        lanza = e_in(pr(t, tMint - 0.1, tMint + 0.4))
        rx = lerp(kx + 60, PX - 40, lanza)
        ry = lerp(ky + 40, Y_SUP + 10, lanza) - 120 * math.sin(lanza * math.pi)
        hund = pr(t, tMint + 0.4, tMenos - 0.2)
        if hund < 1:
            A._rollo(im, rx, ry + 60 * hund, 60 * (1 - 0.6 * hund), t, rgb("d8463a"), 6600)
            arena_frente(im, Y_SUP, t, seed=3, x0=PX - 320, x1=PX + 320, onda=5, alto=Y_SUP + 160) if hund > 0 else None
    if t > tNoP - 0.1:
        e1 = e_back(pr(t, tNoP - 0.1, tNoP + 0.2))
        e2 = e_back(pr(t, tPanico - 0.1, tPanico + 0.2))
        rotulo(im, "¡NO ENTRES", 540, 330, 150, AMARILLO, t, seed=65, rot=-0.05, esc=e1)
        rotulo(im, "EN PÁNICO!", 560, 490, 150, AMARILLO, t, seed=66, rot=-0.03, esc=e2)
        if t > tPanico:
            destello(im, 160, 640, 0.9 * e2, t)
            destello(im, 930, 560, 0.7 * e2, t, seed=1033)
    return terminar(im, t)


def cuadro(t):
    if t < T_INI + 0.6:
        return desborde(A.cuadro(t) if False else __import__("plano_b").cuadro(t), echarse(t), pr(t, T_INI, T_INI + 0.6),
                        cx=540, cy=1200)
    if t < T_CORTE:
        return echarse(t)
    if t < T_CORTE + 0.6:
        return desborde(echarse(t), circulos(t), pr(t, T_CORTE, T_CORTE + 0.6), cx=540, cy=A.Y_C)
    if t < T_SALE:
        return circulos(t)
    if t < T_SALE + 0.6:
        return desborde(circulos(t), salir(t), pr(t, T_SALE, T_SALE + 0.6), cx=540, cy=Y_SUP)
    if t < T_SENTADO:
        return salir(t)
    if t < T_SENTADO + 0.6:
        return desborde(salir(t), sentado(t), pr(t, T_SENTADO, T_SENTADO + 0.6), cx=300, cy=1300)
    return sentado(t)
