# -*- coding: utf-8 -*-
"""LEUCOCITOS + LINFOCITOS (dentro de la sangre, con glóbulos rojos que pasan flotando).
muralla: un virus brinca la muralla del castillo → salen los SOLDADOS: GLÓBULOS BLANCOS (células del sistema inmunitario).
nombre: GLÓBULOS BLANCOS = LEUCOCITOS; LEUCO = BLANCO (brochazo blanco).
tipos: GRANULOCITOS · MONOCITOS · LINFOCITOS → TRUCO: les salen orejas de gato, orejas de mono y melena de león.
gato: los granitos se llenan y sueltan ENZIMAS que marean a un virus. mono: crece → MACRÓFAGO y se come una bacteria (¡ÑAM!);
MACRÓFAGO = COME MUCHO.
leones: LINFOCITOS = LOS MÁS LISTOS (birrete); T destruye una célula infectada; B fabrica ANTICUERPOS y CÉLULAS B DE MEMORIA.
antigeno: ¿QUÉ ES UN ANTÍGENO? = LO QUE VIENE DE FUERA: toxinas, bacterias, virus, pedacitos; ANTÍGENO rima con AJENO.
anticuerpo: los anticuerpos se pegan al virus + calcomanía «¡ESTE ES!» → lo destruyen; ANTI-CUERPO: lo fabrica tu cuerpo."""
import math

import numpy as np

from acuarela import H, W, TINTA, brillo, curva, degradado, e_back, e_out, elipse, forma, lavado, linea, mancha_pts, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, T0, ww
from comun_ci import cartel, titulo
from fondos_amaya import papel, _manchas
from iconos_ia import marca_x, palomita
from personajes import AMARILLO, destello, exclama, mareo, pregunta
from kit_amaya import AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, entra, letrero, papa, tarjeta
from piezas_es import ROSA_M
from piezas_fj import base, montanas
from piezas_ci import BLANCO, MOCO, ROSA, anticuerpo, bacteria, calcomania, castillo, celula, virus
from utileria import calavera

T_INI = T0("leucocitos")
L, Y = "leucocitos", "linfocitos"
tBrinca, tSalen, tSold, tGlob, tCel = ww(L, 0, "brinca"), ww(L, 0, "salen"), ww(L, 0, "soldados"), ww(L, 0, "globulos"), ww(L, 0, "celulas")
T_NOM = ww(L, 1, "su") - 0.3
tLeuco, tLeuco2, tBlanco = ww(L, 1, "leucocitos"), ww(L, 1, "leuco", 1), ww(L, 1, "blanco")
T_TIP = ww(L, 2, "hay") - 0.3
tTres, tGran, tMono, tLinf, tTruco = ww(L, 2, "tres"), ww(L, 2, "granulocitos"), ww(L, 2, "monocitos"), ww(L, 2, "linfocitos"), ww(L, 2, "truco")
tGatos, tMonos, tLeones = ww(L, 2, "gatos"), ww(L, 2, "monos"), ww(L, 2, "leones")
T_GATO = ww(L, 3, "los") - 0.3
tGranitos, tPart, tSueltan, tEnz, tAtacar = (ww(L, 3, "granitos"), ww(L, 3, "particulas"), ww(L, 3, "sueltan"), ww(L, 3, "enzimas"),
                                             ww(L, 3, "atacar"))
T_MONO = ww(L, 4, "los") - 0.3
tCrecen, tMacro, tComen, tMicro, tMacro2, tCome = (ww(L, 4, "crecen"), ww(L, 4, "macrofagos"), ww(L, 4, "comen"), ww(L, 4, "microbios"),
                                                   ww(L, 4, "macrofago", 1), ww(L, 4, "come", 1))
T_LEON = T0(Y)
tListos, tDos, tT, tDestr, tInfect = ww(Y, 0, "listos"), ww(Y, 0, "dos"), ww(Y, 0, "linfocitos t"), ww(Y, 0, "destruir"), ww(Y, 0, "infectadas")
T_B = ww(Y, 1, "y") - 0.3
tB, tFabr, tAnti, tMem, tRecu = ww(Y, 1, "b"), ww(Y, 1, "fabrican"), ww(Y, 1, "anticuerpos"), ww(Y, 1, "memoria"), ww(Y, 1, "recuerdan")
T_ANT = ww(Y, 2, "y") - 0.3
tQue, tFuera, tTox, tBac, tVir, tPed, tTruco2, tAnti2, tAjeno = (ww(Y, 2, "antigeno"), ww(Y, 2, "fuera"), ww(Y, 2, "toxinas"),
                                                                ww(Y, 2, "bacterias"), ww(Y, 2, "virus"), ww(Y, 2, "pedacitos"),
                                                                ww(Y, 2, "truco"), ww(Y, 2, "antigeno", 1), ww(Y, 2, "ajeno"))
T_AC = ww(Y, 3, "y") - 0.3
tPega, tCalco, tEste, tDestr2, tFij, tAC2, tCuerpo, tFabr2 = (ww(Y, 3, "pega"), ww(Y, 3, "calcomania"), ww(Y, 3, "este"),
                                                              ww(Y, 3, "destruir"), ww(Y, 3, "fijense"), ww(Y, 3, "anticuerpo", 1),
                                                              ww(Y, 3, "cuerpo"), ww(Y, 3, "fabrica"))
SANGRE = rgb("e07a78")


# ------------------------------------------------------------ fondo: dentro de la sangre
def _sangre():
    im = np.zeros((H, W, 3), np.float32)
    degradado(im, rgb("f6c8bc"), rgb("e9a196"))
    _manchas(im, rgb("d97a76"), 9, 26001, r=(240, 420), alfa=0.25)
    lavado(im, rrect(W / 2, 40, W, 120, 0), rgb("c9605e"), 0.35, 26002)
    lavado(im, rrect(W / 2, H - 30, W, 120, 0), rgb("c9605e"), 0.35, 26003)
    return im


def rojos(im, t, seed, n=9, alfa=0.85):
    """Glóbulos rojos (donitas) que pasan flotando de izquierda a derecha."""
    rg = np.random.default_rng(seed)
    for k in range(n):
        y0, v, fase, r = rg.uniform(120, 980), rg.uniform(40, 90), rg.uniform(0, 2400), rg.uniform(38, 58)
        x = (fase + v * t) % 2300 - 190
        y = y0 + 18 * math.sin(t * 0.8 + k)
        a = 0.35 * math.sin(t * 0.6 + k)
        forma(im, elipse(x, y, r, r * 0.72, a), SANGRE, t, seed + k, tinta=3, alfa=alfa, luz=(rgb("ffffff"), -r * 0.3, -r * 0.3, 0.3))
        lavado(im, elipse(x, y, r * 0.4, r * 0.26, a), rgb("b84a4c"), 0.45 * alfa, seed + 50 + k)


def fondo(t, seed=26010, n=9):
    im = cache("f_sangre", _sangre).copy()
    rojos(im, t, seed, n)
    return im


# ------------------------------------------------------------ muralla
def _fondo_cas():
    im = papel("calido")
    lavado(im, rrect(W / 2, 260, W, 520, 0), rgb("bfe0f0"), 0.5, 26101)
    montanas(im, 0, seed=26102, y0=820)
    lavado(im, rrect(W / 2, 1000, W, 220, 0), rgb("8fc06a"), 0.55, 26103)
    return im


def muralla(t):
    im = cache("f_cas", _fondo_cas).copy()
    castillo(im, 560, 960, 0.7, t, seed=26110)
    # el virus brinca la muralla en arco
    u = pr(t, tBrinca - 0.6, tBrinca + 0.6)
    vx = 1250 - 690 * u
    vy = 700 - 520 * math.sin(u * math.pi) + 120 * u
    virus(im, vx, vy, 0.8, t, seed=26120, cara="enojo")
    if tBrinca - 0.3 < t < tSalen + 0.4:
        rotulo(im, "¡SE BRINCÓ LA MURALLA!", 960, 120, 58, ROJO, t, seed=26125, esc=entra(t, tBrinca - 0.3))
    # salen los soldados: tres glóbulos blancos con casco que marchan
    for k in range(3):
        e = entra(t, tSalen + 0.25 * k)
        if e <= 0.01:
            continue
        x = 560 + (k - 1) * 170 + 30 * math.sin(t * 6 + k) * 0.3
        yy = 860 - 12 * abs(math.sin(t * 7 + k))
        celula(im, x, yy, 0.75 * e, t, seed=26130 + k * 10, tipo="", cara="enojo")
        forma(im, elipse(x, yy - 58 * e, 60 * e, 30 * e), rgb("6f8a4a"), t, 26135 + k * 10, tinta=3)        # casco
    if t > tSold - 0.3:
        rotulo(im, "¡LOS SOLDADOS!", 1180, 330, 70, MORADO, t, seed=26150, esc=entra(t, tSold - 0.3), rot=-0.03)
    if t > tGlob - 0.3:
        letrero(im, "GLÓBULOS BLANCOS", 1180, 470, 56, t, col=CREMA, txt=AZUL, seed=26155, esc=entra(t, tGlob - 0.3), rot=0.03)
    if t > tCel - 0.3:
        letrero(im, "CÉLULAS DEL SISTEMA INMUNITARIO", 1100, 600, 38, t, col=AMARILLO, seed=26160, esc=entra(t, tCel - 0.3), rot=-0.02)
    return im


# ------------------------------------------------------------ nombre
def nombre(t):
    im = fondo(t, 26200)
    celula(im, 480, 580, 1.8 * entra(t, T_NOM), t, seed=26210, tipo="", cara="feliz")
    if t > tLeuco - 0.3:
        letrero(im, "GLÓBULOS BLANCOS", 1100, 230, 52, t, col=CREMA, txt=AZUL, seed=26220, esc=entra(t, tLeuco - 0.6), rot=-0.02)
        rotulo(im, "=", 1100, 330, 70, TINTA, t, seed=26221, tinta=False, esc=entra(t, tLeuco - 0.3))
        letrero(im, "LEUCOCITOS", 1100, 440, 76, t, col=MORADO, txt=CREMA, seed=26225, esc=entra(t, tLeuco - 0.3), rot=0.02)
    if t > tLeuco2 - 0.3:
        e = entra(t, tLeuco2 - 0.3)
        tarjeta(im, 1050, 700, 620 * e, 170 * e, t, CREMA, 26230, rot=-0.02)
        rotulo(im, "LEUCO", 900, 704, 70 * e + 1, MORADO, t, seed=26231, tinta=False)
        if t > tBlanco - 0.3:
            u = pr(t, tBlanco - 0.3, tBlanco + 0.3)
            rotulo(im, "= BLANCO", 1170, 704, 62 * entra(t, tBlanco - 0.3) + 1, AZUL, t, seed=26232, tinta=False)
            lavado(im, mancha_pts(1180, 820, 160 * u + 1, 26233, 0.3, ry=40 * u + 1), BLANCO, 0.9, 26234)
            chispas(im, 1180, 800, 160, t, tBlanco, seed=26235, col=AMARILLO)
    return im


# ------------------------------------------------------------ tipos
TIPOS = [("GRANULOCITOS", "GATOS", "gato", 340), ("MONOCITOS", "MONOS", "mono", 760), ("LINFOCITOS", "LEONES", "leon", 1180)]


def tipos(t):
    im = fondo(t, 26300, n=6)
    if t > tTres - 0.3:
        letrero(im, "3 TIPOS", 760, 110, 64, t, col=MORADO, txt=CREMA, seed=26310, esc=entra(t, tTres - 0.3), rot=-0.03)
    t_ap = (tGran, tMono, tLinf)
    t_tr = (tGatos, tMonos, tLeones)
    for k, ((nom, truco, tipo, x) , ta, tt) in enumerate(zip(TIPOS, t_ap, t_tr)):
        if t <= ta - 0.4:
            continue
        e = entra(t, ta - 0.4)
        ya = t > tt - 0.1
        celula(im, x, 470, 1.25 * e, t, seed=26320 + k * 20, tipo=tipo if ya else "", cara="feliz", granos=1.0 if (ya and k == 0) else 0)
        if ya:
            destello(im, x + 120, 330, entra(t, tt - 0.1), t, seed=26325 + k * 20)
        letrero(im, nom, x, 690, 40, t, col=CREMA, txt=TINTA, seed=26330 + k * 20, esc=e, rot=(k - 1) * 0.03)
        if ya:
            rotulo(im, f"= {truco}", x, 790, 60, [ROJO, rgb("a0662f"), rgb("d08a1a")][k], t, seed=26340 + k * 20, esc=entra(t, tt - 0.1))
    if t > tTruco - 0.3:
        letrero(im, "TRUCO:", 1560, 110, 52, t, col=AMARILLO, seed=26390, esc=entra(t, tTruco - 0.3), rot=0.05)
    return im


# ------------------------------------------------------------ gato
def gato_t(t):
    im = fondo(t, 26400)
    letrero(im, "GRANULOCITO = GATO", 560, 110, 52, t, col=CREMA, txt=ROJO, seed=26405, esc=entra(t, T_GATO + 0.2), rot=-0.03)
    gr = pr(t, tGranitos - 0.4, tGranitos + 0.6)
    celula(im, 520, 560, 1.6, t, seed=26410, tipo="gato", cara="enojo" if t > tSueltan else "feliz", granos=0.2 + 0.8 * gr)
    if t > tGranitos - 0.3:
        letrero(im, "GRANITOS", 520, 860, 50, t, col=rgb("e05a8a"), txt=CREMA, seed=26420, esc=entra(t, tGranitos - 0.3), rot=0.03)
    # el virus enemigo; las enzimas lo marean y se encoge
    golpe = pr(t, tEnz + 0.4, tAtacar + 0.5)
    vs = 1.3 * (1 - 0.55 * golpe)
    virus(im, 1200, 540 + 10 * math.sin(t * 3), vs, t, seed=26430, cara="susto" if golpe > 0.1 else "enojo",
          flojo=golpe)
    if golpe > 0.3:
        mareo(im, 1200, 420, 0.8, t, seed=26435)
    if t > tSueltan - 0.1:
        for j in range(10):
            c = ((t - tSueltan) * 1.2 + j / 10) % 1
            x = 680 + 440 * c
            y = 540 + 90 * math.sin(j * 2.1) * c + 20 * math.sin(t * 5 + j)
            forma(im, elipse(x, y, 10, 10), rgb("e05a8a"), t, 26440 + j, tinta=1.5, alfa=1 - 0.6 * c)
    if t > tEnz - 0.3:
        letrero(im, "ENZIMAS", 940, 330, 56, t, col=AMARILLO, seed=26460, esc=entra(t, tEnz - 0.3), rot=-0.04)
    if t > tAtacar - 0.2:
        rotulo(im, "¡PARA ATACAR!", 1200, 820, 54, ROJO, t, seed=26465, esc=entra(t, tAtacar - 0.2))
    return im


# ------------------------------------------------------------ mono
def mono_t(t):
    im = fondo(t, 26500)
    letrero(im, "MONOCITO = MONO", 520, 110, 52, t, col=CREMA, txt=rgb("a0662f"), seed=26505, esc=entra(t, T_MONO + 0.2), rot=-0.03)
    crece = e_back(pr(t, tCrecen - 0.2, tCrecen + 0.6))
    s = 1.0 + 0.6 * crece
    # la bacteria se acerca y se la come
    ab = pr(t, tComen - 0.6, tComen + 0.2)
    come = pr(t, tComen - 0.5, tComen) * (1 - pr(t, tComen + 0.6, tComen + 1.0))
    celula(im, 560, 560, s, t, seed=26510, tipo="mono", cara="feliz", come=come)
    if t < tComen + 0.3:
        bx = 1260 - 560 * e_out(ab)
        bs = 1.0 * (1 - pr(t, tComen + 0.05, tComen + 0.3))
        if bs > 0.05:
            bacteria(im, bx, 560 + 20 * math.sin(t * 3), bs, t, seed=26520, cara="susto" if ab > 0.3 else "enojo", rot=math.pi)
    if t > tComen + 0.2:
        rotulo(im, "¡ÑAM!", 820, 360, 90, ROJO, t, seed=26525, esc=entra(t, tComen + 0.2), rot=0.12)
        chispas(im, 600, 560, 220, t, tComen + 0.2, seed=26527, col=AMARILLO)
    if t > tCrecen - 0.3:
        rotulo(im, "CRECE...", 300, 300, 56, MORADO, t, seed=26530, esc=entra(t, tCrecen - 0.3), rot=-0.06)
    if t > tMacro - 0.3:
        letrero(im, "MACRÓFAGO", 1200, 260, 66, t, col=MORADO, txt=CREMA, seed=26535, esc=entra(t, tMacro - 0.3), rot=0.03)
    if t > tMacro2 - 0.3:
        e = entra(t, tMacro2 - 0.3)
        tarjeta(im, 1120, 820, 660 * e, 150 * e, t, CREMA, 26540, rot=-0.02)
        rotulo(im, "MACRÓFAGO = COME MUCHO", 1120, 824, 46 * e + 1, ROJO, t, seed=26541, tinta=False, rot=-0.02)
    return im


# ------------------------------------------------------------ leones
def birrete(im, x, y, s, t, seed):
    forma(im, np.array([(x - 70 * s, y), (x, y - 26 * s), (x + 70 * s, y), (x, y + 26 * s)], np.float32), TINTA, t, seed, tinta=0)
    forma(im, rrect(x, y + 20 * s, 70 * s, 26 * s, 4 * s), TINTA, t, seed + 1, tinta=0)
    linea(im, [(x + 50 * s, y), (x + 62 * s, y + 46 * s + 4 * s * math.sin(t * 4))], 3 * s, AMARILLO, seed=seed + 2, t=t)


def celula_infectada(im, x, y, s, t, seed, rompe=0.0):
    if rompe >= 1:
        return
    k = 1 - 0.7 * rompe
    forma(im, mancha_pts(x, y, 80 * s * k, seed, 0.15), rgb("c8c890"), t, seed + 1, tinta=4 * s)
    for j in range(4):
        a = j * 1.6 + 0.4
        virus(im, x + 40 * s * k * math.cos(a), y + 40 * s * k * math.sin(a), 0.22 * s * k, t, seed=seed + 10 + j * 60)
    if rompe > 0:
        for j in range(8):
            a = j * 0.8
            d = 90 * s + 120 * rompe
            forma(im, elipse(x + d * math.cos(a), y + d * math.sin(a), 12 * (1 - rompe) + 1, 12 * (1 - rompe) + 1), rgb("c8c890"), t,
                  seed + 40 + j, tinta=1.5)


def leones(t):
    im = fondo(t, 26600)
    letrero(im, "LINFOCITOS = LEONES", 560, 110, 52, t, col=CREMA, txt=rgb("d08a1a"), seed=26605, esc=entra(t, T_LEON + 0.2), rot=-0.03)
    if t > tListos - 0.3:
        rotulo(im, "¡LOS MÁS LISTOS!", 560, 220, 56, MORADO, t, seed=26610, esc=entra(t, tListos - 0.3))
    ataca = pr(t, tDestr - 0.4, tDestr + 0.2)
    lx = 420 + 300 * suave(ataca) - 120 * pr(t, tDestr + 0.3, tDestr + 1.0)
    celula(im, lx, 560, 1.3, t, seed=26620, tipo="leon", cara="enojo" if ataca > 0.2 else "feliz", letra="T")
    if t > tListos - 0.3:
        birrete(im, lx, 560 - 150, 1.0 * entra(t, tListos - 0.3), t, 26625)
    if t > tDos - 0.3:
        letrero(im, "2 TIPOS: T y B", 1160, 220, 50, t, col=AMARILLO, seed=26630, esc=entra(t, tDos - 0.3), rot=0.03)
    rompe = pr(t, tDestr + 0.1, tDestr + 0.9)
    if t > tT - 1.0:
        celula_infectada(im, 1000, 560, 1.4 * entra(t, tT - 1.0), t, 26640, rompe=rompe)
        if 0 < rompe < 1:
            destello(im, 1000, 560, 1.6, t, seed=26650)
    if t > tT - 0.3:
        letrero(im, "LINFOCITO T", 420, 820, 48, t, col=AZUL, txt=CREMA, seed=26660, esc=entra(t, tT - 0.3), rot=-0.02)
    if t > tInfect - 0.3:
        letrero(im, "DESTRUYE CÉLULAS INFECTADAS", 1000, 860, 40, t, col=CREMA, txt=ROJO, seed=26665, esc=entra(t, tInfect - 0.3),
                rot=0.02)
    return im


def linf_b(t):
    im = fondo(t, 26700)
    celula(im, 360, 520, 1.3, t, seed=26710, tipo="leon", cara="feliz", letra="B")
    if t > tB - 0.3:
        letrero(im, "LINFOCITO B", 360, 820, 48, t, col=ROJO, txt=CREMA, seed=26715, esc=entra(t, tB - 0.3), rot=-0.02)
    # fábrica de anticuerpos: salen Y en abanico
    if t > tFabr - 0.2:
        for j in range(7):
            c = ((t - tFabr + 0.2) * 0.55 + j / 7) % 1
            if t - tFabr + 0.2 < j * 0.25:
                continue
            a = -0.6 + 1.2 * (j / 6)
            x = 500 + 600 * c * math.cos(a)
            y = 520 + 400 * c * math.sin(a)
            anticuerpo(im, x, y, 0.7, t, seed=26720 + j * 5, rot=a + math.pi / 2 + t * 0.8)
    if t > tAnti - 0.3:
        letrero(im, "ANTICUERPOS", 900, 200, 60, t, col=AMARILLO, seed=26760, esc=entra(t, tAnti - 0.3), rot=0.03)
    if t > tMem - 0.6:
        e = entra(t, tMem - 0.6)
        tarjeta(im, 1200, 560, 520 * e, 360 * e, t, CREMA, 26770, rot=0.03)
        for j in range(2):
            celula(im, 1110 + 180 * j, 540, 0.55 * e, t, seed=26775 + j * 30, tipo="leon", cara="feliz", letra="B")
            forma(im, rrect(1110 + 180 * j + 40, 600, 50 * e, 64 * e, 6, 0.2), rgb("f4e6c8"), t, 26790 + j, tinta=2.5)   # libretita
        rotulo(im, "CÉLULAS B DE MEMORIA", 1200, 420, 38 * e + 1, ROJO, t, seed=26795, tinta=False, rot=0.03)
        if t > tRecu - 0.3:
            rotulo(im, "«¡A ESE YA LO CONOZCO!»", 1200, 700, 34 * entra(t, tRecu - 0.3) + 1, MORADO, t, seed=26797, tinta=False, rot=0.03)
            virus(im, 1420, 380, 0.35, t, seed=26798, cara="susto")
    return im


# ------------------------------------------------------------ antígeno
def antigeno(t):
    im = cache("f_ant", lambda: papel("frio")).copy()
    titulo(im, "¿QUÉ ES UN ANTÍGENO?", t, tQue, 26800, col=MORADO, x=700, y=100, px=70)
    if t < tTox - 0.3:
        pregunta(im, 700, 560, 2.2 * entra(t, tQue - 0.2), t, seed=26801)
        virus(im, 1050, 600, 0.9 * entra(t, tQue), t, seed=26802, cara="susto")
    if t > tFuera - 0.3:
        letrero(im, "LO QUE VIENE DE FUERA", 700, 230, 52, t, col=ROJO, txt=CREMA, seed=26805, esc=entra(t, tFuera - 0.3), rot=0.02)
    cosas = [("TOXINAS", tTox), ("BACTERIAS", tBac), ("VIRUS", tVir), ("PEDACITOS", tPed)]
    if t < tTruco2 - 0.3:
        for k, (txt, tk) in enumerate(cosas):
            if t <= tk - 0.3:
                continue
            e = entra(t, tk - 0.3)
            x = 250 + 330 * k
            tarjeta(im, x, 560, 290 * e, 330 * e, t, CREMA, 26810 + k * 9, rot=(k % 2 - 0.5) * 0.05)
            if e > 0.5:
                if k == 0:
                    calavera(im, x, 520, 1.0, t, seed=26812)
                elif k == 1:
                    bacteria(im, x + 20, 520, 0.6, t, seed=26813)
                elif k == 2:
                    virus(im, x, 520, 0.8, t, seed=26814)
                else:
                    for j in range(5):
                        a = j * 1.3
                        forma(im, mancha_pts(x + 50 * math.cos(a), 520 + 40 * math.sin(a), 18, 26815 + j, 0.4), rgb("8fc85a"), t,
                              26820 + j, tinta=2)
                        forma(im, elipse(x + 70 * math.cos(a + 0.4), 520 + 60 * math.sin(a + 0.4), 7, 7), rgb("e05a8a"), t, 26830 + j,
                              tinta=1.2)
            rotulo(im, txt, x, 680, 36 * e + 1, ROJO, t, seed=26840 + k, tinta=False)
    else:
        e1, e2 = entra(t, tAnti2 - 0.3), entra(t, tAjeno - 0.3)
        letrero(im, "TRUCO:", 260, 380, 50, t, col=AMARILLO, seed=26850, esc=entra(t, tTruco2 - 0.3), rot=-0.05)
        if e1 > 0.01:
            tarjeta(im, 735, 520, 560 * e1, 160 * e1, t, CREMA, 26855, rot=-0.02)
            rotulo(im, "ANTÍ", 642, 524, 70 * e1 + 1, MORADO, t, seed=26856, tinta=False)
            rotulo(im, "GENO", 800, 524, 70 * e1 + 1, ROJO, t, seed=26857, tinta=False)
        if e2 > 0.01:
            tarjeta(im, 735, 760, 560 * e2, 160 * e2, t, CREMA, 26860, rot=0.02)
            rotulo(im, "A", 702, 764, 70 * e2 + 1, MORADO, t, seed=26861, tinta=False)
            rotulo(im, "JENO", 800, 764, 70 * e2 + 1, ROJO, t, seed=26862, tinta=False)
            rotulo(im, "(AJENO = DE OTRO)", 720, 900, 40 * e2 + 1, AZUL, t, seed=26863, tinta=False)
            linea(im, curva([(1030, 520), (1120, 640), (1030, 760)], 8), 7, ROJO, seed=26865, t=t)
            rotulo(im, "¡RIMA!", 1220, 640, 60, ROJO, t, seed=26866, esc=e2, rot=0.1)
            chispas(im, 720, 640, 330, t, tAjeno, seed=26867, col=AMARILLO)
    return im


# ------------------------------------------------------------ anticuerpo
def anticuerpo_t(t):
    if t < tFij - 0.3:
        im = fondo(t, 26900, n=6)
        dest = pr(t, tDestr2 - 0.1, tDestr2 + 0.6)
        vx, vy = 760, 540 + 10 * math.sin(t * 2)
        if dest < 1:
            virus(im, vx, vy, 1.8 * (1 - 0.8 * dest), t, seed=26910, cara="susto" if t > tPega else "enojo")
        # anticuerpos que llegan y se pegan alrededor
        for j in range(6):
            a = j * math.pi / 3 + 0.3
            u = e_out(pr(t, tPega - 0.6 + 0.12 * j, tPega + 0.1 + 0.12 * j))
            d = 520 - 360 * u
            if dest > 0.5:
                d += 400 * (dest - 0.5)
            anticuerpo(im, vx + d * math.cos(a), vy + d * math.sin(a), 0.9, t, seed=26920 + j * 5, rot=a - math.pi / 2)
        if t > tCalco - 0.3 and dest < 0.6:
            calcomania(im, vx + 10, vy - 210, 1.3 * entra(t, tCalco - 0.3), t, texto="¡ESTE ES!", seed=26960, rot=-0.08)
        if dest > 0:
            destello(im, vx, vy, 2.0 * suave(dest), t, seed=26965)
            if dest > 0.4:
                rotulo(im, "¡DESTRUIDO!", vx, vy, 80, ROJO, t, seed=26967, esc=entra(t, tDestr2 + 0.2), rot=-0.06)
        if t > tPega - 0.3:
            letrero(im, "SE PEGA AL INVASOR", 760, 900, 48, t, col=CREMA, txt=MORADO, seed=26970, esc=entra(t, tPega - 0.3), rot=0.02)
        return im
    im = cache("f_ac", lambda: papel("calido")).copy()
    e = entra(t, tAC2 - 0.3)
    tarjeta(im, 760, 420, 900 * e, 220 * e, t, CREMA, 26980, rot=-0.02)
    rotulo(im, "ANTI", 520, 424, 100 * e + 1, MORADO, t, seed=26981, tinta=False)
    rotulo(im, "-", 650, 424, 100 * e + 1, TINTA, t, seed=26982, tinta=False)
    gr = 1 + 0.25 * entra(t, tCuerpo - 0.2) * (1 + 0.1 * math.sin(t * 6))
    rotulo(im, "CUERPO", 845, 424, 100 * e * gr + 1, ROJO, t, seed=26983, tinta=False)
    if t > tCuerpo - 0.2:
        linea(im, elipse(845, 424, 260 * gr, 90 * gr), 7, ROSA_M, seed=26984, t=t, cerrado=True)
    for j in range(3):
        anticuerpo(im, 380 + 380 * j, 700, 1.0 * entra(t, tFij + 0.2 * j), t, seed=26990 + j * 5, rot=0.2 * math.sin(t * 2 + j))
    if t > tFabr2 - 0.3:
        letrero(im, "LO FABRICA TU CUERPO", 760, 900, 54, t, col=VERDE, txt=CREMA, seed=26995, esc=entra(t, tFabr2 - 0.3), rot=0.02)
    return im


TRAMOS = [(T_INI, muralla), (T_NOM, nombre), (T_TIP, tipos), (T_GATO, gato_t), (T_MONO, mono_t), (T_LEON, leones), (T_B, linf_b),
          (T_ANT, antigeno), (T_AC, anticuerpo_t), (tFij - 0.3, anticuerpo_t)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
