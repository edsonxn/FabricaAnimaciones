# -*- coding: utf-8 -*-
"""PREGUNTA 3 + RESPUESTA 3 + VACUNAS + AUTOINMUNE + PREGUNTA 4 + RESPUESTA 4.
preg3: ¿QUÉ OTRO NOMBRE TIENEN LOS GLÓBULOS BLANCOS? ¿Y SUS 3 TIPOS? (glóbulo blanco con «?») + cuenta 3-2-1.
resp3: LEUCOCITOS → GRANULOCITOS · MONOCITOS · LINFOCITOS → les salen orejas de gato, de mono y melena de león → ¡MUY BIEN!
vacunas: LAS VACUNAS (frasco y jeringa con aguja) → ACTIVAN EL SISTEMA INMUNITARIO (escudo que se prende) → MEMORIA (célula B con su
libretita) contra VIRUS o BACTERIA → ESTÁN HECHAS DE: VIRUS DEBILITADOS (con curita y ojeras) O PARTES DE ELLOS → la cancha:
PARTIDO DE PRÁCTICA contra un portero virus flojito (¡GOL!) → llega EL DE VERDAD, grandote → ¡YA SE LO SABE! (otro gol).
autoinmune: ENFERMEDADES AUTOINMUNES: el soldado SE CONFUNDE (mareo) y ataca a las células buenas del cuerpo → AUTO = UNO MISMO
(AUTOBIOGRAFÍA = la vida de UNO MISMO) → ¡AUTOGOL! en la cancha → para cuidarlo: COMAN SALUDABLE (plato), HAGAN EJERCICIO
(corredor), DUERMAN BIEN (cama con zzz).
preg4/resp4: ¿DE QUÉ ESTÁN ELABORADAS LAS VACUNAS? → VIRUS DEBILITADOS O PARTES DE ELLOS → PARA QUE EL CUERPO TENGA MEMORIA → ¡ESO!"""
import math

import numpy as np

from acuarela import H, W, TINTA, brillo, curva, e_back, e_out, elipse, forma, lavado, linea, mancha_pts, pr, rgb, rotulo, rrect, suave, terminar
from comun import FIN, T0, ww
from comun_ci import cartel, pantalla_pregunta, titulo
from fondos_amaya import papel
from iconos_ia import marca_x, palomita
from personajes import AMARILLO, destello, exclama, mareo, pregunta
from kit_amaya import AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, entra, letrero, papa, tarjeta
from piezas_es import ROSA_M
from piezas_fj import base, cama, luna, zzz
from piezas_ci import BLANCO, PIEL, ROSA, bacteria, balon, cancha, celula, corredor, plato, porteria, virus
from plano_e import escudo
from plano_f import fondo

T_INI = T0("preg3")
P3, R3, V, A, P4, R4 = "preg3", "resp3", "vacunas", "autoinmune", "preg4", "resp4"
tP3, tOtro, tGlobP, tCuales, tFinP3 = ww(P3, 0, "pausa"), ww(P3, 0, "otro"), ww(P3, 0, "globulos"), ww(P3, 0, "cuales"), FIN(P3)
T_R3 = T0(R3)
tLeuR, tTipR = ww(R3, 0, "leucocitos"), ww(R3, 0, "tipos")
R3_AP = (ww(R3, 0, "granulocitos"), ww(R3, 0, "monocitos"), ww(R3, 0, "linfocitos"))
R3_TR = (ww(R3, 0, "gatos"), ww(R3, 0, "monos"), ww(R3, 0, "leones"))
tMuyBien = ww(R3, 0, "muy")
T_V = T0(V)
tVacunas, tActivar, tMem, tVirusV, tBactV = ww(V, 0, "vacunas"), ww(V, 0, "activar"), ww(V, 0, "memoria"), ww(V, 0, "virus"), ww(V, 0, "bacteria")
T_V2 = ww(V, 1, "estan") - 0.3
tElab, tDebil, tPartes = ww(V, 1, "elaboradas"), ww(V, 1, "debilitados"), ww(V, 1, "partes")
T_V3 = ww(V, 1, "es como") - 0.3
tPartido, tEntrena, tFlojito, tLlega, tVerdad, tSabe = (ww(V, 1, "partido"), ww(V, 1, "entrena"), ww(V, 1, "flojito"), ww(V, 1, "llega"),
                                                        ww(V, 1, "verdad"), ww(V, 1, "ya"))
T_A = T0(A)
tEnf, tConf, tAtaca, tBuenas, tPropio = (ww(A, 0, "enfermedades"), ww(A, 0, "confunde"), ww(A, 0, "ataca"), ww(A, 0, "buenas"),
                                         ww(A, 0, "propio"))
T_A2 = ww(A, 1, "auto") - 0.3
tUno, tAutobio = ww(A, 1, "uno"), ww(A, 1, "autobiografia")
T_A3 = ww(A, 1, "es como") - 0.3
tMeter, tAutogol = ww(A, 1, "meter"), ww(A, 1, "autogol")
T_A4 = ww(A, 2, "y") - 0.3
tMant, tComan, tHagan, tDuerman = ww(A, 2, "mantener"), ww(A, 2, "coman"), ww(A, 2, "hagan"), ww(A, 2, "duerman")
T_P4 = T0(P4)
tP4, tDeQue, tVacP, tFinP4 = ww(P4, 0, "pausa"), ww(P4, 0, "de"), ww(P4, 0, "vacunas"), FIN(P4)
T_R4 = T0(R4)
tDebR, tPartR, tSirven, tMemR, tEso = ww(R4, 0, "virus"), ww(R4, 0, "partes"), ww(R4, 0, "sirven"), ww(R4, 0, "memoria"), ww(R4, 0, "eso")
TIPOS = [("GRANULOCITOS", "GATOS", "gato"), ("MONOCITOS", "MONOS", "mono"), ("LINFOCITOS", "LEONES", "leon")]
COL_TR = [ROJO, rgb("a0662f"), rgb("d08a1a")]


# ------------------------------------------------------------ piezas locales
def vacuna(im, x, y, s, t, seed):
    """Frasquito de vacuna con tapa azul y etiqueta, y una jeringa con aguja al lado."""
    forma(im, rrect(x, y + 20 * s, 120 * s, 170 * s, 18 * s), rgb("eaf4f8"), t, seed, tinta=4 * s, alfa=0.9,
          luz=(rgb("ffffff"), -30 * s, -40 * s, 0.5))
    lavado(im, rrect(x, y + 50 * s, 104 * s, 100 * s, 12 * s), rgb("c8e4f4"), 0.7, seed + 1)
    forma(im, rrect(x, y - 82 * s, 90 * s, 40 * s, 8 * s), AZUL, t, seed + 2, tinta=3 * s)
    forma(im, rrect(x, y + 30 * s, 124 * s, 60 * s, 4 * s), CREMA, t, seed + 3, tinta=2.5 * s)
    rotulo(im, "VACUNA", x, y + 32 * s, 24 * s, AZUL, t, seed=seed + 4, tinta=False)
    jx, jy = x + 250 * s, y + 10 * s
    a = -0.5
    c, sn = math.cos(a), math.sin(a)

    def P(dx, dy):
        return (jx + dx * c - dy * sn, jy + dx * sn + dy * c)
    forma(im, np.array([P(-110 * s, -22 * s), P(70 * s, -22 * s), P(70 * s, 22 * s), P(-110 * s, 22 * s)], np.float32), rgb("eaf4f8"), t,
          seed + 5, tinta=3.5 * s, alfa=0.9)
    forma(im, np.array([P(-60 * s, -18 * s), P(66 * s, -18 * s), P(66 * s, 18 * s), P(-60 * s, 18 * s)], np.float32), rgb("9fd0f0"), t,
          seed + 6, tinta=0, alfa=0.7)
    linea(im, [P(70 * s, 0), P(150 * s, 0)], 3 * s, GRIS, seed=seed + 7, t=t, punta=False)
    linea(im, [P(-110 * s, 0), P(-170 * s, 0)], 9 * s, GRIS, seed=seed + 8, t=t, punta=False)
    forma(im, np.array([P(-170 * s, -30 * s), P(-160 * s, -30 * s), P(-160 * s, 30 * s), P(-170 * s, 30 * s)], np.float32), GRIS, t,
          seed + 9, tinta=2.5 * s)


def libro(im, x, y, s, t, seed, titulo_="AUTOBIOGRAFÍA"):
    forma(im, rrect(x, y, 300 * s, 380 * s, 14 * s, -0.05), rgb("c8754a"), t, seed, tinta=5 * s, sombra=(rgb("6a3a2a"), 14 * s, 14 * s, 0.4))
    forma(im, rrect(x, y - 110 * s, 260 * s, 70 * s, 10 * s, -0.05), CREMA, t, seed + 1, tinta=3 * s)
    rotulo(im, titulo_, x, y - 108 * s, 30 * s, rgb("8a3a2a"), t, seed=seed + 2, tinta=False, rot=-0.05)
    forma(im, elipse(x, y + 50 * s, 70 * s, 70 * s), PIEL, t, seed + 3, tinta=3.5 * s)
    from kit_amaya import cara_p
    cara_p(im, x, y + 50 * s, 2.2 * s, t, seed + 4, cara="normal")
    forma(im, elipse(x, y + 4 * s, 72 * s, 26 * s), rgb("5a3a2a"), t, seed + 5, tinta=0)


def partido(im, t, t_tiro, rival, autogol=False, seed=0):
    """Cancha: un glóbulo blanco patea; rival = 'flojo' | 'fuerte' (portero virus). autogol = patea a su propia portería."""
    cancha(im, 760, 620, 1360, 620, t, seed=seed)
    gx = 230 if autogol else 1290
    porteria(im, gx, 640, 1.0, t, seed=seed + 20)
    if not autogol:
        u = pr(t, t_tiro, t_tiro + 0.6)
        if rival == "flojo":
            virus(im, gx + 20 * math.sin(t * 1.2), 560, 0.7, t, seed=seed + 30, flojo=1.0)
            if t < t_tiro + 0.8:
                rotulo(im, "zzz", gx + 90, 450, 34, GRIS, t, seed=seed + 31)
        else:
            sal = e_out(pr(t, t_tiro - 1.2, t_tiro - 0.6))
            virus(im, gx + 60 * math.sin(t * 5), 560, 0.6 + 0.5 * sal, t, seed=seed + 35, cara="enojo", col=rgb("d04a4a"))
        px = 520
    else:
        u = pr(t, t_tiro, t_tiro + 0.7)
        px = 760
    pateo = pr(t, t_tiro - 0.15, t_tiro + 0.05) * (1 - pr(t, t_tiro + 0.2, t_tiro + 0.5))
    celula(im, px, 650 - 30 * pateo, 0.8, t, seed=seed + 40, tipo="", cara="susto" if (autogol and u > 0.5) else "feliz")
    bx0 = px + (-110 if autogol else 110)
    if not autogol:
        bx = bx0 + (gx - bx0) * e_out(u)
        by = 700 - 140 * math.sin(u * math.pi) * 0.8 - 90 * u
    else:
        bx = bx0 + (gx - bx0) * e_out(u)
        by = 700 - 160 * math.sin(u * math.pi) - 90 * u
    balon(im, bx, by, 34, t, seed=seed + 50, gira=t * 8 * (1 if u < 1 else 0))
    return u


# ------------------------------------------------------------ preg3 / resp3
def preg3(t):
    im = cache("g_p3", lambda: papel("frio")).copy()
    pantalla_pregunta(im, t, tP3, tFinP3, T_R3, 27000, ["¿QUÉ OTRO NOMBRE TIENEN", "LOS GLÓBULOS BLANCOS?", "¿Y CUÁLES SON SUS 3 TIPOS?"],
                      [tOtro, tGlobP, tCuales], y0=400, px=58)
    if t > tGlobP:
        celula(im, 1330, 640, 0.75 * entra(t, tGlobP), t, seed=27040, tipo="", cara="feliz")
        pregunta(im, 1450, 520, 1.1 * entra(t, tGlobP + 0.2), t, seed=27045)
    return im


def resp3(t):
    im = fondo(t, 27100, n=6)
    letrero(im, "RESPUESTA", 260, 110, 56, t, col=VERDE, txt=CREMA, seed=27105, esc=entra(t, T_R3), rot=-0.04)
    if t > tLeuR - 0.3:
        letrero(im, "LEUCOCITOS", 860, 120, 76, t, col=MORADO, txt=CREMA, seed=27110, esc=entra(t, tLeuR - 0.3), rot=0.02)
    for k, ((nom, truco, tipo), ta, tt) in enumerate(zip(TIPOS, R3_AP, R3_TR)):
        if t <= ta - 0.4:
            continue
        x = 340 + 420 * k
        e = entra(t, ta - 0.4)
        ya = t > tt - 0.1
        celula(im, x, 470, 1.1 * e, t, seed=27120 + k * 20, tipo=tipo if ya else "", cara="feliz", granos=1.0 if (ya and k == 0) else 0)
        letrero(im, nom, x, 680, 40, t, col=CREMA, seed=27130 + k * 20, esc=e, rot=(k - 1) * 0.03)
        if ya:
            rotulo(im, truco, x, 780, 58, COL_TR[k], t, seed=27140 + k * 20, esc=entra(t, tt - 0.1))
            destello(im, x + 110, 340, entra(t, tt - 0.1), t, seed=27145 + k * 20)
    if t > tMuyBien - 0.3:
        rotulo(im, "¡MUY BIEN!", 760, 920, 80, VERDE, t, seed=27190, esc=entra(t, tMuyBien - 0.3), rot=-0.04)
        palomita(im, 1130, 900, 1.0 * entra(t, tMuyBien - 0.1), t, seed=27195, col=VERDE)
    return im


# ------------------------------------------------------------ vacunas
def vac1(t):
    im = cache("g_v1", lambda: papel("calido")).copy()
    titulo(im, "LAS VACUNAS", t, tVacunas, 27200, col=AZUL, x=640, y=100, px=86)
    e = entra(t, tVacunas - 0.4)
    if e > 0.01:
        vacuna(im, 330, 460, 1.3 * e, t, 27210)
    if t > tActivar - 0.3:
        u = pr(t, tActivar, tActivar + 0.6)
        brillo(im, 900, 470, 200, rgb("fff3a0"), 0.5 * u * (0.7 + 0.3 * math.sin(t * 6)))
        escudo(im, 900, 470, 0.9 * entra(t, tActivar - 0.3), t, 27220, col=AZUL if u < 0.5 else VERDE)
        letrero(im, "ACTIVAN EL SISTEMA INMUNITARIO", 760, 730, 44, t, col=CREMA, txt=VERDE, seed=27225, esc=entra(t, tActivar - 0.3),
                rot=-0.02)
    if t > tMem - 0.4:
        e2 = entra(t, tMem - 0.4)
        celula(im, 1280, 430, 0.8 * e2, t, seed=27230, tipo="leon", cara="feliz", letra="B")
        forma(im, rrect(1370, 510, 70 * e2, 90 * e2, 8, 0.2), rgb("f4e6c8"), t, 27235, tinta=3)
        letrero(im, "MEMORIA", 1280, 640, 52, t, col=MORADO, txt=CREMA, seed=27240, esc=e2, rot=0.04)
    if t > tVirusV - 0.3:
        rotulo(im, "CONTRA UN", 470, 880, 44, MORADO, t, seed=27245, esc=entra(t, tVirusV - 0.3))
        virus(im, 720, 880, 0.55 * entra(t, tVirusV - 0.3), t, seed=27250)
    if t > tBactV - 0.3:
        rotulo(im, "O", 870, 880, 50, MORADO, t, seed=27255, esc=entra(t, tBactV - 0.3))
        bacteria(im, 1060, 880, 0.55 * entra(t, tBactV - 0.3), t, seed=27260)
    return im


def vac2(t):
    im = cache("g_v2", lambda: papel("frio")).copy()
    titulo(im, "¿DE QUÉ ESTÁN HECHAS?", t, tElab, 27300, col=MORADO, x=700, y=110, px=72)
    if t > tDebil - 0.6:
        e = entra(t, tDebil - 0.6)
        tarjeta(im, 450, 520, 520 * e, 480 * e, t, CREMA, 27310, rot=-0.03)
        if e > 0.5:
            virus(im, 450, 470 + 8 * math.sin(t * 1.5), 1.5, t, seed=27315, flojo=1.0)
            rotulo(im, "zzz", 580, 330, 40, GRIS, t, seed=27318)
        rotulo(im, "VIRUS DEBILITADOS", 450, 700, 40 * e + 1, ROJO, t, seed=27320, tinta=False, rot=-0.03)
    if t > tPartes - 0.6:
        e = entra(t, tPartes - 0.6)
        rotulo(im, "O", 790, 520, 80, MORADO, t, seed=27325, esc=e)
        tarjeta(im, 1130, 520, 520 * e, 480 * e, t, CREMA, 27330, rot=0.03)
        if e > 0.5:
            for j in range(6):
                a = j * 1.05
                d = 90 + 15 * math.sin(t * 2 + j)
                forma(im, mancha_pts(1130 + d * math.cos(a), 470 + d * 0.8 * math.sin(a), 30, 27335 + j, 0.4), rgb("b8d890"), t,
                      27340 + j, tinta=2.5)
                forma(im, elipse(1130 + (d + 40) * math.cos(a + 0.3), 470 + (d + 40) * 0.8 * math.sin(a + 0.3), 10, 10), GRIS, t,
                      27350 + j, tinta=1.5)
        rotulo(im, "PARTES DE ELLOS", 1130, 700, 40 * e + 1, ROJO, t, seed=27360, tinta=False, rot=0.03)
    if t > tPartes + 0.3:
        rotulo(im, "(¡NO TE ENFERMAN, SOLO ENSEÑAN!)", 790, 900, 40, VERDE, t, seed=27365, esc=entra(t, tPartes + 0.3))
    return im


def vac3(t):
    im = cache("g_v3", lambda: papel("calido")).copy()
    titulo(im, "PARTIDO DE PRÁCTICA", t, tPartido, 27400, col=VERDE, x=700, y=100, px=72)
    if t < tLlega - 0.2:
        u = partido(im, t, tFlojito + 0.2, "flojo", seed=27410)
        if t > tFlojito - 0.3:
            letrero(im, "RIVAL FLOJITO", 1290, 330, 44, t, col=CREMA, txt=GRIS, seed=27420, esc=entra(t, tFlojito - 0.3), rot=0.04)
        if t > tEntrena - 0.3:
            letrero(im, "EL CUERPO ENTRENA", 420, 330, 44, t, col=CREMA, txt=AZUL, seed=27425, esc=entra(t, tEntrena - 0.3), rot=-0.04)
        if u >= 1:
            rotulo(im, "¡GOL!", 1080, 470, 90, VERDE, t, seed=27430, esc=entra(t, tFlojito + 0.8), rot=-0.1)
    else:
        u = partido(im, t, tSabe - 0.1, "fuerte", seed=27440)
        letrero(im, "¡EL DE VERDAD!", 1240, 330, 52, t, col=ROJO, txt=CREMA, seed=27450, esc=entra(t, tLlega - 0.2), rot=0.04)
        if t > tSabe - 0.3:
            letrero(im, "¡YA SE LO SABE!", 520, 330, 56, t, col=VERDE, txt=CREMA, seed=27455, esc=entra(t, tSabe - 0.3), rot=-0.04)
        if u >= 1:
            rotulo(im, "¡GOL!", 1080, 470, 90, VERDE, t, seed=27460, esc=entra(t, tSabe + 0.5), rot=-0.1)
            chispas(im, 1290, 560, 200, t, tSabe + 0.5, seed=27465, col=AMARILLO)
    return im


# ------------------------------------------------------------ autoinmune
def auto1(t):
    im = fondo(t, 27500, n=5)
    titulo(im, "ENFERMEDADES AUTOINMUNES", t, tEnf, 27500, col=MORADO, x=700, y=100, px=64)
    conf = pr(t, tConf - 0.2, tConf + 0.3)
    ataca = pr(t, tAtaca - 0.3, tAtaca + 0.4)
    sx = 420 + 280 * suave(ataca)
    celula(im, sx, 520, 1.2, t, seed=27510, tipo="", cara="susto" if conf > 0.5 and ataca < 0.5 else ("enojo" if ataca >= 0.5 else "feliz"))
    if conf > 0:
        mareo(im, sx, 360, 1.0 * conf, t, seed=27515)
    if tConf - 0.3 < t < tAtaca:
        letrero(im, "SE CONFUNDE", sx, 760, 50, t, col=AMARILLO, seed=27520, esc=entra(t, tConf - 0.3), rot=-0.03)
    # células buenas del cuerpo (rosas y felices) que se asustan
    for k in range(3):
        x, y = 1040 + 150 * k, 460 + 110 * (k % 2)
        golpe = pr(t, tAtaca + 0.2 + 0.25 * k, tAtaca + 0.5 + 0.25 * k)
        celula(im, x + 20 * golpe * math.sin(t * 30), y, 0.6, t, seed=27530 + k * 20, tipo="", col=rgb("f8c8d0"),
               cara="susto" if ataca > 0.3 else "feliz")
        if golpe > 0 and golpe < 1:
            destello(im, x, y, 0.9, t, seed=27535 + k * 20)
    if t > tBuenas - 0.3:
        letrero(im, "CÉLULAS BUENAS", 1190, 260, 44, t, col=CREMA, txt=rgb("d06080"), seed=27590, esc=entra(t, tBuenas - 0.3), rot=0.03)
    if t > tPropio - 0.3:
        letrero(im, "¡DE SU PROPIO CUERPO!", 900, 860, 52, t, col=ROJO, txt=CREMA, seed=27595, esc=entra(t, tPropio - 0.3), rot=0.02)
    return im


def auto2(t):
    im = cache("g_a2", lambda: papel("rosa")).copy()
    e = entra(t, T_A2 + 0.2)
    tarjeta(im, 600, 360, 860 * e, 220 * e, t, CREMA, 27600, rot=-0.03)
    rotulo(im, "AUTO =", 360, 364, 80 * e + 1, ROJO, t, seed=27601, tinta=False, rot=-0.03)
    if t > tUno - 0.3:
        rotulo(im, "UNO MISMO", 770, 364, 66 * entra(t, tUno - 0.3) + 1, MORADO, t, seed=27602, tinta=False, rot=-0.03)
    if t > tAutobio - 0.5:
        e2 = entra(t, tAutobio - 0.5)
        libro(im, 1200, 560, 1.0 * e2, t, 27610)
        rotulo(im, "= LA VIDA DE UNO MISMO", 560, 640, 46 * e2 + 1, AZUL, t, seed=27620, tinta=False)
        rotulo(im, "(escrita por uno mismo)", 560, 720, 36 * e2 + 1, GRIS * 0.6, t, seed=27621, tinta=False)
    return im


def auto3(t):
    im = cache("g_a3", lambda: papel("calido")).copy()
    u = partido(im, t, tAutogol - 0.5, "", autogol=True, seed=27700)
    if u >= 1:
        rotulo(im, "¡AUTOGOL!", 760, 320, 120, ROJO, t, seed=27710, esc=entra(t, tAutogol), rot=-0.06)
        marca_x(im, 230, 560, 1.0 * entra(t, tAutogol + 0.1), t, seed=27715, col=ROJO)
    else:
        rotulo(im, "¿A DÓNDE PATEAS?", 760, 200, 56, MORADO, t, seed=27720, esc=entra(t, T_A3 + 0.3))
        flecha = pr(t, tMeter - 0.2, tMeter + 0.4)
        if flecha > 0:
            linea(im, curva([(650, 600), (480, 470), (300, 560)], 8), 8, ROJO, seed=27725, t=t, alfa=0.0)
    return im


def auto4(t):
    im = cache("g_a4", lambda: papel("frio")).copy()
    titulo(im, "PARA CUIDAR TU DEFENSA", t, tMant, 27800, col=VERDE, x=700, y=110, px=70)
    cols = [(320, "COMAN SALUDABLE", tComan, rgb("f4d38a")), (760, "HAGAN EJERCICIO", tHagan, rgb("b8e0c0")),
            (1200, "DUERMAN BIEN", tDuerman, rgb("c8c0ec"))]
    for k, (x, txt, tk, col) in enumerate(cols):
        if t <= tk - 0.4:
            continue
        e = entra(t, tk - 0.4)
        tarjeta(im, x, 540, 400 * e, 520 * e, t, col, 27810 + k * 9, rot=(k - 1) * 0.03)
        rotulo(im, txt, x, 750, 38 * e + 1, TINTA, t, seed=27811 + k * 9, tinta=False)
        if e < 0.6:
            continue
        if k == 0:
            plato(im, x, 520, 1.0, t, seed=27820)
        elif k == 1:
            corredor(im, x, 520, 1.6, t, seed=27830)
        else:
            cama(im, x + 20, 560, 0.55, t, seed=27840)
            luna(im, x - 110, 380, 40, t, seed=27845)
            zzz(im, x + 40, 450, t, s=0.9, seed=27850)
        palomita(im, x + 150, 330, 0.6 * entra(t, tk + 0.3), t, seed=27860 + k, col=VERDE)
    return im


# ------------------------------------------------------------ preg4 / resp4
def preg4(t):
    im = cache("g_p4", lambda: papel("frio")).copy()
    pantalla_pregunta(im, t, tP4, tFinP4, T_R4, 27900, ["¿DE QUÉ ESTÁN ELABORADAS", "LAS VACUNAS?"], [tDeQue, tVacP], y0=430)
    if t > tVacP - 0.2:
        vacuna(im, 640, 800, 0.7 * entra(t, tVacP - 0.2), t, 27940)
        pregunta(im, 1050, 780, 1.4 * entra(t, tVacP), t, seed=27950)
    return im


def resp4(t):
    im = cache("g_r4", lambda: papel("frio")).copy()
    letrero(im, "RESPUESTA", 260, 110, 56, t, col=VERDE, txt=CREMA, seed=28000, esc=entra(t, T_R4), rot=-0.04)
    if t > tDebR - 0.3:
        e = entra(t, tDebR - 0.3)
        virus(im, 360, 420, 1.1 * e + 0.01, t, seed=28010, flojo=1.0)
        cartel(im, "VIRUS DEBILITADOS", 760, 380, 48, t, tDebR, 28020, ok=True, t_ok=tDebR + 0.5)
    if t > tPartR - 0.3:
        cartel(im, "O PARTES DE ELLOS", 760, 520, 48, t, tPartR, 28030, ok=True, t_ok=tPartR + 0.5)
    if t > tSirven - 0.3:
        e = entra(t, tSirven - 0.3)
        forma(im, rrect(760, 720, 1000 * e + 1, 160 * e + 1, 22, -0.02), MORADO, t, 28040, tinta=5)
        rotulo(im, "SIRVEN PARA QUE EL CUERPO", 760, 682, 46 * e + 1, CREMA, t, seed=28041, rot=-0.02)
        if t > tMemR - 0.3:
            rotulo(im, "TENGA MEMORIA", 760, 752, 58 * entra(t, tMemR - 0.3) + 1, AMARILLO, t, seed=28042, rot=-0.02)
    if t > tEso - 0.3:
        rotulo(im, "¡ESO!", 760, 910, 96, VERDE, t, seed=28050, esc=entra(t, tEso - 0.3), rot=-0.05)
        chispas(im, 760, 910, 220, t, tEso, seed=28055, col=AMARILLO)
    return im


TRAMOS = [(T_INI, preg3), (T_R3, resp3), (T_V, vac1), (T_V2, vac2), (T_V3, vac3), (T_A, auto1), (T_A2, auto2), (T_A3, auto3),
          (T_A4, auto4), (T_P4, preg4), (T_R4, resp4)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
