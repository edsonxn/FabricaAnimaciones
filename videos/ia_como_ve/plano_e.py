# -*- coding: utf-8 -*-
"""CAPAS: los mapas de filtros se APILAN → la TORRE dentro de la cabeza de Kuri se levanta piso por piso; una ventana redonda
a la derecha enseña en grande lo que arma cada piso (cientos de filtros → esquinas, curvas, rayado del pelo → ojo, oreja,
nariz, bigotes → cara de gato, rueda, letrero de alto), con chispas que suben de piso a piso → la niña con lupa se asoma a
cada piso (bordes, texturas, partes, objetos) → «nadie le programó qué es una oreja»: la regla escrita a mano, tachada →
«¿CÓMO?»."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lerp, linea, pr, rgb, rotulo, rrect,
                      suave, terminar)
from comun import T0, T1, desborde, ww
from fondos_ia import cabeza, papel
from iconos_ia import PIEZAS, PISOS_NOM, cara_gato, marca_x, torre, trazo
from personajes import AMARILLO, BLANCO, OJO_K, destello, kuri, pregunta
from personajes_ia import foto_gato, nina, pegar

E = "capas"
T_INI = T0(E)
tMagia, tApilar = ww(E, 0, "magia"), ww(E, 0, "apilar")
tTorre, tPrimer, tCientos, tFoto = ww(E, 1, "torre"), ww(E, 1, "primer"), ww(E, 1, "cientos"), ww(E, 1, "foto")
tSeg, tMapas, tEsq, tCurv, tRay = ww(E, 2, "segundo"), ww(E, 2, "mapas"), ww(E, 2, "esquinas"), ww(E, 2, "curvas"), ww(E, 2, "rayado")
tTer, tOjo, tOreja, tNariz, tBig = ww(E, 3, "tercer"), ww(E, 3, "ojo"), ww(E, 3, "oreja"), ww(E, 3, "nariz"), ww(E, 3, "bigotes")
tArriba, tCara, tRueda, tLetrero = ww(E, 4, "arriba"), ww(E, 4, "cara"), ww(E, 4, "rueda"), ww(E, 4, "letrero")
tInv = ww(E, 5, "investigadores")
tV = [ww(E, 5, "bordes"), ww(E, 5, "texturas"), ww(E, 5, "partes"), ww(E, 5, "objetos")]
tNadie, tProg, tSola = ww(E, 6, "nadie"), ww(E, 6, "programo"), ww(E, 6, "sola")
tComo = ww(E, 7, "como")
T_FIN = T1(E)
T_PISO = [tPrimer, tSeg, tTer, tArriba]
VX, VY, VR = 1480, 520, 300                                     # la ventana redonda


def _mapas():
    import plano_d
    return [plano_d._mapa(n) for n in ("vertical", "acostado", "diagonal", "color")]


# ------------------------------------------------------------ apilar
def apilar(t):
    im = cabeza()
    for k, m in enumerate(_mapas()):
        ti = T_INI + 0.3 + 0.45 * k
        u = e_out(pr(t, ti, ti + 0.5))
        if u <= 0:
            continue
        y = lerp(-300, 640 - 60 * k, u)
        if t > tApilar:
            y = 640 - 60 * k - 26 * k * e_out(pr(t, tApilar, tApilar + 0.4))
        pegar(im, m, W / 2 + 30 * (k % 2) - 15, y, 0.62, 0.05 * (k - 1.5), t=t, seed=10000 + 10 * k, marco=10, marco_col=rgb("2b3648"))
    rotulo(im, "¡A APILAR!", W / 2, 150, 110, AMARILLO, t, seed=10050, esc=e_back(pr(t, tApilar - 0.1, tApilar + 0.2)), rot=-0.04)
    kuri(im, 330, 700, 2.1, t, cara="feliz")
    if t > tApilar + 0.8:                                         # «imagina la cabeza de la IA…»
        rotulo(im, "DENTRO DE LA CABEZA DE KURI", W / 2, 980, 50, OJO_K, t, seed=10051, esc=e_back(pr(t, tApilar + 0.8, tApilar + 1.1)))
    return im


# ------------------------------------------------------------ la ventana redonda de cada piso
def _ventana(im, t, k, apar):
    e = e_back(apar)
    if e <= 0.02:
        return
    forma(im, elipse(VX, VY, VR * e, VR * e), rgb("fbf3df"), t, 10100, tinta=7, sombra=(rgb("d8c9a6"), 0, 16, 0.5))
    linea(im, [(VX - VR * 0.72 * e, VY + VR * 0.72 * e), (VX - VR * 1.02 * e, VY + VR * 1.02 * e)], 30, col=rgb("7a4a2a"), seed=10101,
          t=t)
    rotulo(im, f"PISO {k + 1}: {PISOS_NOM[k]}", VX, VY - VR - 50, 56, AMARILLO, t, seed=10102 + k, esc=e)
    if k == 0:                                                   # cientos de filtros = rayitas de colores
        n = int(60 * e_out(pr(t, tCientos - 0.2, tCientos + 1.2)))
        rg = np.random.default_rng(3)
        for i in range(n):
            a, r = rg.uniform(0, 2 * math.pi), VR * 0.8 * math.sqrt(rg.uniform(0.02, 1))
            trazo(im, VX + r * math.cos(a), VY + r * math.sin(a), 0.7, t, rg.uniform(0, math.pi),
                  [rgb("e8a33a"), rgb("4fa3c0"), rgb("d0607a"), rgb("6aa84f")][i % 4], seed=10110 + i)
        if t > tCientos - 0.1:
            rotulo(im, "CIENTOS DE FILTROS", VX, VY + VR + 50, 44, BLANCO, t, seed=10108, esc=e_back(pr(t, tCientos, tCientos + 0.3)))
        return
    sets = {1: [("esquina", tEsq), ("curva", tCurv), ("rayado", tRay)],
            2: [("ojo", tOjo), ("oreja", tOreja), ("nariz", tNariz), ("bigotes", tBig)],
            3: [("cara", tCara), ("rueda", tRueda), ("alto", tLetrero)]}[k]
    n = len(sets)
    for i, (nom, ti) in enumerate(sets):
        a = e_back(pr(t, ti - 0.15, ti + 0.2))
        if a <= 0.02:
            continue
        ang = -math.pi / 2 + i / n * 2 * math.pi + (0.3 if n == 4 else 0)
        r = VR * (0.45 if n > 1 else 0)
        PIEZAS[nom](im, VX + r * math.cos(ang), VY + r * math.sin(ang), (1.15 if k < 3 else 0.95) * a, t, seed=10200 + 30 * k + 7 * i)
    if k == 1 and t > tMapas - 0.2:                              # «no mira la foto: mira los mapas del primero»
        pass


def construir(t):
    im = cabeza()
    crece = e_out(pr(t, tTorre - 0.4, tTorre + 0.9))
    act = [suave(pr(t, ti - 0.2, ti + 0.4)) for ti in T_PISO]
    pisos = torre(im, t, x=640, y0=1010, w=720, alto_p=190, crece=crece, activo=act, contenido=True,
                  foco=max([k for k in range(4) if t > T_PISO[k] - 0.2], default=-1))
    # la foto entra al piso 1
    if t > tPrimer - 0.6:
        e = e_back(pr(t, tPrimer - 0.6, tPrimer - 0.2)) * (1 - 0.6 * pr(t, tSeg, tSeg + 0.5))
        pegar(im, foto_gato(t), 150, 960, 0.3 * max(e, 0.01), -0.05, t=t, seed=10300, marco=10)
        if e > 0.5:
            linea(im, curva([(230, 900), (260, 880), (300, 915)], 4), 5, col=AMARILLO, seed=10301, t=t, alfa=0.8)
    # chispas que suben de un piso al siguiente
    for k in range(1, 4):
        if t > T_PISO[k] - 0.2:
            x, y0, y1 = pisos[k][0], pisos[k - 1][1], pisos[k][1]
            for j in range(5):
                ph = ((t - T_PISO[k]) * 0.9 + j / 5) % 1
                px = x - 220 + 110 * j
                py = lerp(y0, y1, ph)
                brillo(im, px, py, 18, AMARILLO, 0.8 * math.sin(math.pi * ph))
    # «mira los mapas del primero»: los mapas del piso 1 suben como hojas al piso 2
    if tMapas - 0.3 < t < tEsq + 0.5:
        u = pr(t, tMapas - 0.3, tEsq + 0.2)
        for k, m in enumerate(_mapas()[:3]):
            y = lerp(pisos[0][1], pisos[1][1], e_in(clamp(u * 1.4 - 0.15 * k)))
            pegar(im, m, 420 + 200 * k, y, 0.22, 0.05 * (k - 1), t=t, seed=10310 + 10 * k, marco=6, marco_col=rgb("2b3648"),
                  alfa=1 - pr(u, 0.85, 1.0))
    k = max([k for k in range(4) if t > T_PISO[k] - 0.3], default=-1)
    if k >= 0:
        _ventana(im, t, k, pr(t, T_PISO[k] - 0.3, T_PISO[k] + 0.1))
        linea(im, curva([(pisos[k][0] + pisos[k][2] / 2 + 10, pisos[k][1]), (1100, pisos[k][1] - 40), (VX - VR - 10, VY)], 8), 4,
              col=AMARILLO, seed=10320 + k, t=t, alfa=0.55, punta=False)
    return im


# ------------------------------------------------------------ la niña con lupa se asoma a cada piso
def asomarse(t):
    im = cabeza()
    kf = max([k for k in range(4) if t > tV[k] - 0.2], default=-1)
    pisos = torre(im, t, x=760, y0=1010, w=720, alto_p=190, crece=1.0, activo=[1.0 if k == kf else 0.35 for k in range(4)],
                  foco=kf)
    for k in range(4):
        if t > tV[k] - 0.2:
            rotulo(im, PISOS_NOM[k], 180, pisos[k][1], 50, AMARILLO, t, seed=10400 + k, esc=e_back(pr(t, tV[k] - 0.2, tV[k] + 0.1)))
    # la investigadora
    yk = pisos[kf][1] if kf >= 0 else pisos[0][1]
    p = nina(im, 1540, 640, 1.45, t, cara="abiertos" if kf >= 0 else "normal", boca="abierta" if kf == 3 else "sonrisa",
             brazos=(0.4, 2.0), codos=(0.3, 0.9), mira=-1.0)
    hx, hy = p["manos"][1] if "manos" in p else (1440, 520)
    lx, ly = hx - 90, hy - 40
    forma(im, elipse(lx, ly, 62, 62), rgb("dff3f6"), t, 10410, tinta=7, alfa=0.55)
    linea(im, [(lx + 44, ly + 44), (hx, hy)], 16, col=rgb("7a4a2a"), seed=10411, t=t)
    if kf >= 0:
        linea(im, [(lx - 50, ly - 20), (pisos[kf][0] + pisos[kf][2] / 2, yk - 60)], 3, col=AMARILLO, seed=10412, t=t, alfa=0.6,
              punta=False)
        linea(im, [(lx - 50, ly + 20), (pisos[kf][0] + pisos[kf][2] / 2, yk + 60)], 3, col=AMARILLO, seed=10413, t=t, alfa=0.6,
              punta=False)
    rotulo(im, "LOS INVESTIGADORES SE ASOMARON", W / 2 + 200, 90, 46, BLANCO, t, seed=10420,
           esc=e_back(pr(t, tInv - 0.1, tInv + 0.3)), alfa=1 - pr(t, tV[0] - 0.4, tV[0]))
    return im


# ------------------------------------------------------------ nadie le programó qué es una oreja
def sola(t):
    im = papel("calido")
    # la hoja de reglas escritas a mano (como en los píxeles) y el tache
    e = e_back(pr(t, tNadie - 0.3, tNadie + 0.1))
    forma(im, rrect(560, 520, 620 * e, 520 * e, 16, -0.03), BLANCO, t, 10500, tinta=4)
    if e > 0.5:
        for k, txt in enumerate(("REGLA:", "SI TIENE PUNTA", "Y ES TRIANGULAR", "Y ESTÁ ARRIBA…", "= OREJA")):
            rotulo(im, txt, 560, 330 + 80 * k, 44, rgb("3f78c8"), t, seed=10510 + k, tinta=False)
        if t > tProg + 0.1:
            marca_x(im, 560, 520, 2.4 * e_back(pr(t, tProg + 0.1, tProg + 0.4)), t, seed=10520)
            rotulo(im, "NADIE LO ESCRIBIÓ", 560, 860, 56, rgb("e35d4a"), t, seed=10521, esc=e_back(pr(t, tProg + 0.2, tProg + 0.5)))
    # la oreja que salió sola del piso 3, brillando
    eo = e_back(pr(t, tNadie + 0.4, tNadie + 0.8))
    if eo > 0.02:
        brillo(im, 1360, 470, 260 * eo, AMARILLO, 0.45)
        cara_gato(im, 1360, 500, 2.1 * eo, t, seed=10530)
        if t > tNadie + 0.9:                                   # la oreja, marcada
            linea(im, elipse(1360 - 82 * 2.1 * eo, 500 - 78 * 2.1 * eo, 80, 95, -0.4), 7, col=AMARILLO, seed=10535, t=t,
                  cerrado=True, punta=False, alfa=pr(t, tNadie + 0.9, tNadie + 1.2))
    if t > tSola - 0.2:
        rotulo(im, "¡LA DESCUBRIÓ SOLA!", 1360, 860, 74, AMARILLO, t, seed=10540, esc=e_back(pr(t, tSola - 0.2, tSola + 0.1)), rot=-0.03)
        destello(im, 1560, 300, 1.0 * pr(t, tSola, tSola + 0.3), t, seed=1040)
        destello(im, 1160, 330, 0.8 * pr(t, tSola + 0.1, tSola + 0.4), t, seed=1041)
    kuri(im, 1760, 260, 1.3, t, cara="feliz" if t > tSola else "normal")
    return im


def como(t):
    im = cabeza()
    torre(im, t, x=W / 2, y0=1030, w=640, alto_p=170, crece=1.0, activo=(0.3, 0.3, 0.3, 0.3), contenido=True)
    e = e_back(pr(t, tComo - 0.15, tComo + 0.2))
    rotulo(im, "¿CÓMO?", W / 2, 150, 150, AMARILLO, t, seed=10600, esc=e, rot=0.03)
    kuri(im, 1600, 560, 1.9, t, cara="abiertos")
    pregunta(im, 1660, 300, 1.3 * e, t, seed=1012)
    pregunta(im, 300, 380, 1.0 * e_back(pr(t, tComo + 0.2, tComo + 0.45)), t, seed=1013)
    return im


TRAMOS = [(apilar, T_INI), (construir, tTorre - 0.5), (asomarse, tInv - 0.4), (sola, tNadie - 0.4), (como, tComo - 0.5)]


def cuadro_crudo(t):
    k = 0
    for i, (_, ti) in enumerate(TRAMOS):
        if t >= ti:
            k = i
    f, ti = TRAMOS[k]
    im = f(t)
    if t < ti + 0.6:
        if k > 0:
            im = desborde(TRAMOS[k - 1][0](t), im, pr(t, ti, ti + 0.6), W * (0.3 + 0.1 * k), H * 0.5)
        else:
            import plano_d
            im = desborde(plano_d.cuadro_crudo(t), im, pr(t, ti, ti + 0.6), W * 0.5, H * 0.5)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
