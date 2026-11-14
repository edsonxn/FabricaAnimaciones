# -*- coding: utf-8 -*-
"""MATERIA + GAS.
materia: «¿QUÉ ES LA MATERIA?» + foto real de su cuaderno + OCUPA UN LUGAR (caja punteada) / TIENE MASA (pesa) → banca, vaso de
agua y tres alumnos con sello MATERIA → truco de dos preguntas con palomitas → «¿Y EL AIRE?»: globo que se infla y ocupa lugar →
balanza: el globo inflado pesa tantito más → «EL AIRE TAMBIÉN ES MATERIA».
gas: 3 ESTADOS (piedra, vaso, nube de partículas) + «GAS = SIN FORMA NI VOLUMEN DEFINIDO» → piedra con su forma, agua que toma la
forma del vaso, gas que sale de una esquina y se reparte por toda la caja → frasco cerrado y tanque de gas de la casa; al abrir la
válvula, el gas se escapa."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_out, elipse, forma, lavado, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import T0, ww
from comun_ci import cartel, titulo
from fondos_amaya import papel, _manchas
from iconos_ia import palomita
from personajes import AMARILLO, destello, pregunta
from kit_amaya import AZUL, CREMA, GRIS, MORADO, ROJO, VERDE, cache, chispas, entra, gente, letrero, papa, tarjeta
from piezas_es import ROSA_M, TURQ, polaroid
from piezas_fj import base
from piezas_ci import N2, O2, balanza, banca, globo, particulas, piedra, tanque, vaso

T_INI = T0("materia")
M, G = "materia", "gas"
tMat, tCuad, tOcupa, tEsp, tMasa = ww(M, 0, "materia"), ww(M, 0, "cuaderno"), ww(M, 0, "ocupa"), ww(M, 0, "espacio"), ww(M, 0, "masa")
T_EJ = ww(M, 1, "una") - 0.3
tBanca, tAgua, tUst = ww(M, 1, "banca"), ww(M, 1, "agua"), ww(M, 1, "ustedes")
T_TRUCO = ww(M, 1, "truco") - 0.3
tTruco, tQ1, tQ2, tSi, tMat3 = ww(M, 1, "truco"), ww(M, 1, "ocupa"), ww(M, 1, "tiene"), ww(M, 1, "si", 1), ww(M, 1, "materia", 3)
T_AIRE = ww(M, 2, "y") - 0.3
tAire, tInfla, tOcupa2 = ww(M, 2, "aire"), ww(M, 2, "inflan"), ww(M, 2, "ocupa")
T_BAL = ww(M, 2, "globo", 1) - 0.6
tPesa, tTant, tDesinf, tTamb = ww(M, 2, "pesa"), ww(M, 2, "tantito"), ww(M, 2, "desinflado"), ww(M, 2, "tambien")
T_G = T0(G)
tTres, tSol, tLiq, tGaseo = ww(G, 0, "tres"), ww(G, 0, "solido"), ww(G, 0, "liquido"), ww(G, 0, "gaseoso")
tGas, tSin, tForma, tVol = ww(G, 0, "gas"), ww(G, 0, "sin"), ww(G, 0, "forma"), ww(G, 0, "volumen")
T_G2 = ww(G, 1, "una") - 0.3
tPied, tPForma, tAguaG, tVaso, tGas2, tRep, tEspG = (ww(G, 1, "piedra"), ww(G, 1, "forma"), ww(G, 1, "agua"), ww(G, 1, "vaso"),
                                                     ww(G, 1, "gas"), ww(G, 1, "reparte"), ww(G, 1, "espacio"))
T_G3 = ww(G, 2, "por") - 0.3
tGases3, tRecip, tTanque, tSiNo, tEscapan = (ww(G, 2, "gases"), ww(G, 2, "recipiente"), ww(G, 2, "tanque"), ww(G, 2, "si"),
                                             ww(G, 2, "escapan"))


def caja_punteada(im, x, y, w, h, t, seed, col=AZUL, u=1.0):
    n = 18
    pts = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2), (x + w / 2, y + h / 2), (x - w / 2, y + h / 2), (x - w / 2, y - h / 2)]
    for k in range(4):
        (ax, ay), (bx, by) = pts[k], pts[k + 1]
        for j in range(n // 2):
            a0, a1 = 2 * j / n, (2 * j + 1) / n
            if (k + a0) / 4 > u:
                return
            linea(im, [(ax + (bx - ax) * a0, ay + (by - ay) * a0), (ax + (bx - ax) * a1, ay + (by - ay) * a1)], 5, col, seed=seed + k * 20 + j,
                  t=t, punta=False)


def pesa(im, x, y, s, t, seed, texto="MASA"):
    forma(im, np.array([(x - 70 * s, y + 50 * s), (x - 45 * s, y - 40 * s), (x + 45 * s, y - 40 * s), (x + 70 * s, y + 50 * s)],
                       np.float32), rgb("5a5a66"), t, seed, tinta=4 * s, luz=(rgb("ffffff"), -10 * s, -10 * s, 0.3))
    linea(im, elipse(x, y - 58 * s, 22 * s, 18 * s), 7 * s, rgb("5a5a66"), seed=seed + 1, t=t, cerrado=True, punta=False)
    rotulo(im, texto, x, y + 10 * s, 26 * s, CREMA, t, seed=seed + 2, tinta=False)


def sello(im, x, y, t, t0, seed, texto="MATERIA", col=None):
    if t <= t0 - 0.1:
        return
    e = entra(t, t0 - 0.1, 0.25)
    col = VERDE if col is None else col
    linea(im, rrect(x, y, 230 * e + 1, 70 * e + 1, 12, -0.12), 6, col, seed=seed, t=t, cerrado=True, punta=False)
    rotulo(im, texto, x, y + 3, 38 * e + 1, col, t, seed=seed + 1, rot=-0.12, tinta=False)


def def_materia(t):
    im = cache("b_def", lambda: papel("frio")).copy()
    titulo(im, "¿QUÉ ES LA MATERIA?", t, tMat, 20000, col=MORADO, x=760, y=120, px=84)
    if t > tCuad - 0.4:
        e = entra(t, tCuad - 0.4)
        polaroid(im, "materia", 330, 480, 1.0 * e, t, rot=-0.05, seed=20010, alto=440)
        rotulo(im, "SU CUADERNO", 330, 790, 38 * e + 1, ROSA_M, t, seed=20012, rot=-0.05)
    if t > tOcupa - 0.3:
        e = entra(t, tOcupa - 0.3)
        tarjeta(im, 980, 330, 720 * e, 150 * e, t, rgb("b8c7e8"), 20020, rot=0.02)
        rotulo(im, "OCUPA UN LUGAR", 900, 335, 58 * e + 1, TINTA, t, seed=20021, rot=0.02, tinta=False)
        caja_punteada(im, 1260, 330, 110, 110, t, 20030, u=pr(t, tEsp - 0.2, tEsp + 0.6))
        if t > tEsp:
            rotulo(im, "EN EL ESPACIO", 980, 440, 40, AZUL, t, seed=20025, esc=entra(t, tEsp - 0.2))
    if t > tMasa - 0.3:
        e = entra(t, tMasa - 0.3)
        tarjeta(im, 980, 610, 720 * e, 150 * e, t, rgb("f6a6a0"), 20040, rot=-0.02)
        rotulo(im, "Y TIENE MASA", 900, 615, 58 * e + 1, TINTA, t, seed=20041, rot=-0.02, tinta=False)
        pesa(im, 1260, 610, 0.9 * e + 0.01, t, 20045, "1 KG")
    return im


def ejemplos(t):
    im = cache("b_ej", lambda: papel("calido")).copy()
    forma(im, np.array([(0, 820), (W, 800), (W, H), (0, H)], np.float32), rgb("d9c19a"), 0, 20100, tinta=0)
    linea(im, [(0, 820), (W, 800)], 5, seed=20101)
    if t > tBanca - 0.3:
        e = entra(t, tBanca - 0.3)
        banca(im, 300, 800, 1.3 * e + 0.01, t, 20110)
        rotulo(im, "BANCA", 300, 470, 50 * e + 1, rgb("b0703a"), t, seed=20112)
        sello(im, 300, 380, t, tBanca + 0.4, 20115)
    if t > tAgua - 0.3:
        e = entra(t, tAgua - 0.3)
        vaso(im, 720, 790, 1.5 * e + 0.01, t, seed=20120)
        rotulo(im, "AGUA", 720, 470, 50 * e + 1, AZUL, t, seed=20122)
        sello(im, 720, 380, t, tAgua + 0.4, 20125)
    if t > tUst - 0.3:
        e = entra(t, tUst - 0.3)
        for k in range(3):
            gente(im, 1060 + 120 * k, 680 - 20 * (k % 2), 2.6 * e + 0.01, t, seed=20130 + k * 3)
        rotulo(im, "¡USTEDES!", 1180, 470, 50 * e + 1, ROSA_M, t, seed=20140)
        sello(im, 1180, 380, t, tUst + 0.5, 20145)
    return im


def truco(t):
    im = cache("b_tr", lambda: papel("frio")).copy()
    letrero(im, "TRUCO", 260, 140, 60, t, col=AMARILLO, seed=20200, esc=entra(t, tTruco - 0.3), rot=-0.05)
    for k, (txt, tk) in enumerate((("¿OCUPA LUGAR?", tQ1), ("¿TIENE MASA?", tQ2))):
        if t > tk - 0.3:
            e = entra(t, tk - 0.3)
            tarjeta(im, 640, 330 + 190 * k, 760 * e, 150 * e, t, CREMA, 20210 + k * 5, rot=(k - 0.5) * 0.03)
            rotulo(im, txt, 600, 336 + 190 * k, 62 * e + 1, MORADO, t, seed=20211 + k * 5, tinta=False)
            forma(im, rrect(1130, 330 + 190 * k, 110 * e, 110 * e, 14), CREMA, t, 20213 + k * 5, tinta=4)
            if t > tSi - 0.2 + 0.25 * k:
                palomita(im, 1135, 330 + 190 * k, 0.8 * entra(t, tSi - 0.2 + 0.25 * k), t, seed=20215 + k * 5, col=VERDE)
                rotulo(im, "SÍ", 1260, 336 + 190 * k, 60, VERDE, t, seed=20217 + k, esc=entra(t, tSi - 0.2 + 0.25 * k))
    if t > tMat3 - 0.4:
        e = entra(t, tMat3 - 0.4)
        forma(im, rrect(700, 760, 820 * e + 1, 130 * e + 1, 24, -0.02), VERDE, t, 20230, tinta=5)
        rotulo(im, "= ES MATERIA", 700, 766, 76 * e + 1, CREMA, t, seed=20231, rot=-0.02)
        chispas(im, 700, 760, 260, t, tMat3, seed=20235, col=AMARILLO)
    return im


def aire(t):
    im = cache("b_aire", lambda: papel("calido")).copy()
    titulo(im, "¿Y EL AIRE?", t, tAire, 20300, col=AZUL, x=700, y=130, px=96)
    u = suave(pr(t, tInfla, tOcupa2 + 0.6))
    if t > tInfla - 0.6:
        globo(im, 700, 520 - 40 * u, 2.2, t, infla=0.08 + 0.92 * u, col=ROJO, seed=20310)
        if 0 < u < 1:
            for k in range(3):
                a = (t * 2 + k / 3) % 1
                lavado(im, elipse(700 + 30 * math.sin(k * 2), 760 - 160 * a, 18, 14), rgb("cfe4f4"), 0.6 * (1 - a), 20320 + k)
    if t > tAire + 0.3:
        letrero(im, "NO SE VE...", 1180, 330, 46, t, col=CREMA, txt=GRIS, seed=20330, esc=entra(t, tAire + 0.3), rot=0.04)
    if t > tOcupa2 - 0.3:
        letrero(im, "¡PERO OCUPA LUGAR!", 1150, 520, 54, t, col=AMARILLO, txt=TINTA, seed=20335, esc=entra(t, tOcupa2 - 0.3), rot=-0.03)
        caja_punteada(im, 700, 470, 470, 560, t, 20340, col=AZUL, u=pr(t, tOcupa2, tOcupa2 + 0.8))
    return im


def bascula(t):
    im = cache("b_bal", lambda: papel("calido")).copy()
    inc = e_out(pr(t, tPesa - 0.1, tPesa + 0.9)) * (1 + 0.15 * math.sin(max(0, t - tPesa) * 7) * math.exp(-max(0, t - tPesa) * 2))
    balanza(im, 700, 330, 1.25, t, inclina=inc, seed=20400,
            izq=lambda m, x, y: globo(m, x, y - 120, 1.0, t, infla=1.0, col=ROJO, seed=20420),
            der=lambda m, x, y: globo(m, x, y - 40, 1.0, t, infla=0.05, col=ROJO, seed=20430))
    rotulo(im, "INFLADO", 410, 780, 44, ROJO, t, seed=20440, esc=entra(t, T_BAL + 0.3))
    if t > tDesinf - 0.3:
        rotulo(im, "DESINFLADO", 1000, 760, 44, GRIS, t, seed=20441, esc=entra(t, tDesinf - 0.3))
    if t > tTant - 0.2:
        letrero(im, "¡PESA TANTITO MÁS!", 400, 160, 50, t, col=AMARILLO, seed=20445, esc=entra(t, tTant - 0.2), rot=-0.04)
    if t > tTamb - 0.4:
        e = entra(t, tTamb - 0.4)
        forma(im, rrect(1130, 160, 700 * e + 1, 120 * e + 1, 22, 0.03), VERDE, t, 20450, tinta=5)
        rotulo(im, "EL AIRE ES MATERIA", 1130, 166, 54 * e + 1, CREMA, t, seed=20451, rot=0.03)
        chispas(im, 1130, 160, 230, t, tTamb, seed=20455, col=AMARILLO)
    return im


def nube_gas(im, x, y, w, h, t, seed, n=16, alfa=1.0):
    lavado(im, rrect(x, y, w, h, 30), rgb("dceef0"), 0.35 * alfa, seed)
    particulas(im, x - w / 2, y - h / 2, x + w / 2, y + h / 2, n, t, seed + 5, col=[N2, N2, N2, O2], r=12, vel=1.6, alfa=alfa)


def estados(t):
    im = cache("b_est", lambda: papel("frio")).copy()
    titulo(im, "3 ESTADOS DE LA MATERIA", t, tTres, 20500, col=MORADO, x=740, y=100, px=72)
    for k, (txt, tk, col) in enumerate((("SÓLIDO", tSol, rgb("b8a890")), ("LÍQUIDO", tLiq, rgb("8fc3e8")), ("GASEOSO", tGaseo, rgb("dceef0")))):
        if t <= tk - 0.3:
            continue
        e = entra(t, tk - 0.3)
        x = 300 + 440 * k
        tarjeta(im, x, 400, 380 * e, 380 * e, t, CREMA, 20510 + k * 7, rot=(k - 1) * 0.02)
        rotulo(im, txt, x, 250, 52 * e + 1, TINTA, t, seed=20511 + k * 7, tinta=False)
        if e > 0.6:
            if k == 0:
                piedra(im, x, 430, 1.1, t, seed=20520)
            elif k == 1:
                vaso(im, x, 530, 1.1, t, seed=20525)
            else:
                nube_gas(im, x, 430, 300, 220, t, 20530, n=12)
    if t > tGas - 0.3:
        e = entra(t, tGas - 0.3)
        tarjeta(im, 740, 770, 1260 * e, 200 * e, t, rgb("f4d38a"), 20550, rot=-0.01)
        rotulo(im, "GAS: ESTADO DE AGREGACIÓN DE LA MATERIA", 740, 735, 40 * e + 1, TINTA, t, seed=20551, tinta=False)
        for k, (txt, tk) in enumerate((("SIN FORMA", tForma), ("NI VOLUMEN DEFINIDO", tVol))):
            if t > tk - 0.3:
                rotulo(im, txt, 480 + 520 * k, 815, 54, ROJO, t, seed=20555 + k, esc=entra(t, tk - 0.3))
    return im


def formas(t):
    im = cache("b_for", lambda: papel("calido")).copy()
    if t > tPied - 0.3:
        e = entra(t, tPied - 0.3)
        piedra(im, 280, 450, 1.6 * e + 0.01, t, seed=20600)
        if t > tPForma - 0.2:
            letrero(im, "SU PROPIA FORMA", 280, 700, 40, t, seed=20605, esc=entra(t, tPForma - 0.2), rot=-0.03)
    if t > tAguaG - 0.3:
        e = entra(t, tAguaG - 0.3)
        vaso(im, 700, 600, 1.6 * e + 0.01, t, nivel=0.15 + 0.6 * suave(pr(t, tAguaG, tVaso + 0.4)), seed=20610)
        if pr(t, tAguaG - 0.2, tVaso + 0.4) < 1:                                      # chorrito que lo llena
            linea(im, [(700, 160), (700, 560 - 300 * 0.6 * suave(pr(t, tAguaG, tVaso + 0.4)))], 14, rgb("8fc3e8"), seed=20615, t=t,
                  alfa=0.9 * e)
        if t > tVaso - 0.2:
            letrero(im, "LA FORMA DEL VASO", 700, 700, 40, t, seed=20618, esc=entra(t, tVaso - 0.2), rot=0.03)
    if t > tGas2 - 0.3:
        e = entra(t, tGas2 - 0.3)
        tarjeta(im, 1180, 430, 460 * e, 440 * e, t, CREMA, 20620, rot=0.01)
        linea(im, rrect(1180, 430, 400, 380, 10), 5, seed=20621, t=t, cerrado=True, punta=False, alfa=e)
        u = suave(pr(t, tRep - 0.2, tEspG + 0.6))
        x0, y0 = 1180 - 200 + 4, 430 + 190 - 4
        particulas(im, x0, y0 - 100 - 270 * u, x0 + 100 + 290 * u, y0, 18, t, 20625, col=[N2, N2, O2], r=12, vel=1.8)
        if t > tEspG - 0.2:
            letrero(im, "¡SE REPARTE POR TODO!", 1180, 700, 40, t, col=AMARILLO, seed=20630, esc=entra(t, tEspG - 0.2), rot=-0.03)
    return im


def recipiente(t):
    im = cache("b_rec", lambda: papel("frio")).copy()
    forma(im, np.array([(0, 880), (W, 870), (W, H), (0, H)], np.float32), rgb("c9c2b0"), 0, 20700, tinta=0)
    if t > tGases3 - 0.3:                                             # frasco cerrado con gas adentro
        e = entra(t, tGases3 - 0.3)
        frasco = rrect(380, 640, 300 * e + 1, 420 * e + 1, 40)
        lavado(im, frasco, rgb("dfeff7"), 0.55, 20710)
        particulas(im, 380 - 130 * e, 640 - 180 * e, 380 + 130 * e, 640 + 190 * e, 14, t, 20715, col=[N2, N2, O2], r=12, vel=1.8,
                   alfa=min(1, e))
        linea(im, frasco, 5, seed=20712, t=t, cerrado=True, punta=False)
        forma(im, rrect(380, 640 - 220 * e, 320 * e + 1, 50 * e + 1, 10), ROJO, t, 20713, tinta=4)
    if t > tRecip - 0.3:
        letrero(im, "EN UN RECIPIENTE", 380, 200, 52, t, col=AMARILLO, seed=20720, esc=entra(t, tRecip - 0.3), rot=-0.03)
    if t > tTanque - 0.4:
        e = entra(t, tTanque - 0.4)
        ab = suave(pr(t, tSiNo - 0.1, tSiNo + 0.5))
        tanque(im, 1000, 880, 1.25 * e + 0.01, t, abierto=ab, seed=20730)
        if ab > 0.01:                                                  # el gas que sale se ve: partículas que vuelan
            for k in range(10):
                a = (t * 0.7 + k / 10) % 1
                px, py = 1080 + a * (380 + 30 * (k % 3)), 330 - a * (200 + 25 * (k % 4)) + 25 * math.sin(t * 4 + k)
                forma(im, elipse(px, py, 11, 11), [N2, O2][k % 2], t, 20750 + k, tinta=2, alfa=ab * (1 - a * 0.7))
        rotulo(im, "TANQUE DE GAS", 1000, 960, 46 * e + 1, ROJO, t, seed=20740)
        if t > tEscapan - 0.3:
            letrero(im, "¡SE ESCAPAN!", 1300, 260, 62, t, col=ROJO, txt=CREMA, seed=20745, esc=entra(t, tEscapan - 0.3), rot=0.04)
    return im


CAFE_ = TINTA
TRAMOS = [(T_INI, def_materia), (T_EJ, ejemplos), (T_TRUCO, truco), (T_AIRE, aire), (T_BAL, bascula), (T_G, estados),
          (T_G2, formas), (T_G3, recipiente)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
