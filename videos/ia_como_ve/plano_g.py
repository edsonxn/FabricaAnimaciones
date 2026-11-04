# -*- coding: utf-8 -*-
"""IMAGENET: Fei-Fei Li (retrato real en camafeo) + «2009» → la pared de fotos con su etiqueta escrita a mano y
«14 000 000» → la multitud de 49 000 personas de 167 países etiquetando (gato, volcán, tostadora) → el concurso anual
(trofeo y tres computadoras en el podio) → 2012: AlexNet, una red PROFUNDA (losas en perspectiva) entrenada en dos tarjetas
gráficas y 60 millones de perillas → barras de error 15 % vs 26 %: ¡LOS APLASTÓ! → la gráfica real del concurso 2010-2015
(error top-5) que cruza la línea de una persona entrenada (5,1 %)."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lerp, linea, pr, rgb, rotulo, rrect,
                      suave, terminar)
from comun import T0, T1, desborde, ww
from fondos_ia import cabeza, papel
from iconos_ia import foto_cosa, gpu, perilla, personita, tostadora, trofeo
from personajes import AMARILLO, BLANCO, OJO_K, destello, kuri
from personajes_ia import camafeo, dibujo_nino, foto_gato, globo, meme_gato, pegar, retrato

E = "imagenet"
T_INI = T0(E)
tNueve, tFei, tImageNet, tCatorce, tEtiq = (ww(E, 0, "nueve"), ww(E, 0, "fei"), ww(E, 0, "imagenet"), ww(E, 0, "catorce"),
                                            ww(E, 0, "etiquetada"))
tContrato, tCuarenta, tCiento, tAnos = ww(E, 1, "contrato"), ww(E, 1, "cuarenta"), ww(E, 1, "ciento"), ww(E, 1, "anos")
tGato, tVolcan, tTost = ww(E, 1, "gato"), ww(E, 1, "volcan"), ww(E, 1, "tostadora")
tConcurso, tPrograma = ww(E, 2, "concurso"), ww(E, 2, "programa")
tDoce, tAlex, tProfunda, tTarjetas, tSesenta = (ww(E, 3, "doce"), ww(E, 3, "alexnet"), ww(E, 3, "profunda"), ww(E, 3, "tarjetas"),
                                                ww(E, 3, "sesenta"))
tQuince, tSegundo, tVeinti, tAplasto = ww(E, 4, "quince"), ww(E, 4, "segundo"), ww(E, 4, "veintiseis"), ww(E, 4, "aplasto")
tCambio, tTres, tPersona = ww(E, 5, "cambio"), ww(E, 5, "tres"), ww(E, 5, "persona")
T_FIN = T1(E)
ROJO = rgb("e35d4a")
VERDE = rgb("4f9a5a")
ETIQ = ["GATO", "VOLCÁN", "TOSTADORA", "PERRO", "BICI", "GATO", "DIBUJO", "MEME", "PERRO", "VOLCÁN", "GATO", "BICI"]


def _cards(t):
    return [foto_gato(t), foto_cosa("volcan", t), foto_cosa("tostadora", t), foto_cosa("perro", t), foto_cosa("bici", t),
            foto_gato(t, "despierto"), dibujo_nino(t), meme_gato(t), foto_cosa("perro", t), foto_cosa("volcan", t),
            foto_gato(t, "espalda"), foto_cosa("bici", t)]


# ------------------------------------------------------------ Fei-Fei Li y la pared de fotos
def feifei(t):
    im = papel("calido")
    e = e_back(pr(t, tNueve + 0.2, tNueve + 0.6))
    camafeo(im, retrato("feifei_li", 240, 300), 300, 470, 1.1 * e, t, nombre="FEI-FEI LI", seed=12000)
    rotulo(im, "2009", 300, 130, 90, rgb("b8443a"), t, seed=12010, esc=e_back(pr(t, tNueve - 0.2, tNueve + 0.1)))
    cards = _cards(t)
    n = int(12 * e_out(pr(t, tFei + 0.6, tCatorce + 0.5)))
    for k in range(n):
        i, j = k % 4, k // 4
        x, y = 820 + 300 * i, 300 + 250 * j
        pegar(im, cards[k], x, y, 0.55, 0.05 * math.sin(k * 2.3), t=t, seed=12020 + k, marco=10)
        if t > tEtiq - 0.2 + 0.08 * k:                              # su etiqueta escrita a mano
            a = e_back(pr(t, tEtiq - 0.2 + 0.08 * k, tEtiq + 0.1 + 0.08 * k))
            forma(im, rrect(x + 80, y + 100, 150 * a, 44 * a, 6, -0.08), rgb("fff6c8"), t, 12060 + k, tinta=2.6)
            rotulo(im, ETIQ[k], x + 80, y + 100, int(26 * a) + 2, rgb("2b3f8a"), t, seed=12080 + k, rot=-0.08, tinta=False,
                   fuente="segoesc.ttf")
    if t > tImageNet - 0.15:
        rotulo(im, "IMAGENET", 1270, 110, 110, rgb("3f78c8"), t, seed=12100, esc=e_back(pr(t, tImageNet - 0.15, tImageNet + 0.2)))
    if t > tCatorce - 0.1:
        rotulo(im, "14 000 000 IMÁGENES", 300, 900, 56, ROJO, t, seed=12101, esc=e_back(pr(t, tCatorce - 0.1, tCatorce + 0.2)),
               rot=-0.03)
    if t > tEtiq - 0.2:
        rotulo(im, "CADA UNA, A MANO", 300, 990, 44, TINTA, t, seed=12102, tinta=False, esc=e_back(pr(t, tEtiq - 0.2, tEtiq + 0.1)))
    return im


# ------------------------------------------------------------ 49 000 personas
def multitud(t):
    im = papel("frio")
    n = int(48 * e_out(pr(t, tContrato - 0.2, tCuarenta + 0.8)))
    for k in range(n):
        i, j = k % 12, k // 12
        x = 220 + 135 * i + (35 if j % 2 else 0)
        y = 520 + 120 * j
        personita(im, x, y, 1.15 + 0.1 * j, t, seed=k * 7 + 3)
    if t > tCuarenta - 0.1:
        rotulo(im, "49 000 PERSONAS", 560, 150, 84, ROJO, t, seed=12200, esc=e_back(pr(t, tCuarenta - 0.1, tCuarenta + 0.2)))
    if t > tCiento - 0.1:
        rotulo(im, "167 PAÍSES", 1400, 150, 84, rgb("3f78c8"), t, seed=12201, esc=e_back(pr(t, tCiento - 0.1, tCiento + 0.2)))
    if t > tAnos - 0.2:
        rotulo(im, "AÑOS ETIQUETANDO", 1000, 1020, 46, TINTA, t, seed=12202, tinta=False, esc=e_back(pr(t, tAnos - 0.2, tAnos + 0.1)))
    for k, (ti, txt, img) in enumerate(((tGato, "¡ES UN GATO!", foto_gato(t)), (tVolcan, "¡UN VOLCÁN!", foto_cosa("volcan", t)),
                                        (tTost, "¡TOSTADORA!", foto_cosa("tostadora", t)))):
        if t > ti - 0.3:
            a = e_back(pr(t, ti - 0.3, ti))
            x = 420 + 540 * k
            globo(im, x, 400, 400, 110, "", t, px=40, n=14 * pr(t, ti - 0.3, ti + 0.3), lineas=[txt], seed=12210 + k, cola=(-1, 1))
            pegar(im, img, x + 120, 300, 0.32 * a, 0.08, t=t, seed=12220 + k, marco=8)
    return im


# ------------------------------------------------------------ el concurso
def _compu(im, x, y, s, t, cara, seed):
    forma(im, rrect(x, y, 220 * s, 160 * s, 16 * s), rgb("cfd6de"), t, seed, tinta=4.4 * s)
    forma(im, rrect(x, y - 6 * s, 180 * s, 116 * s, 10 * s), rgb("1d2a36"), t, seed + 1, tinta=3 * s)
    forma(im, rrect(x, y + 104 * s, 60 * s, 40 * s, 6 * s), rgb("9aa4ae"), t, seed + 2, tinta=3 * s)
    for d in (-1, 1):
        if cara == "feliz":
            linea(im, curva([(x + d * 34 * s - 12 * s, y - 4 * s), (x + d * 34 * s, y - 16 * s), (x + d * 34 * s + 12 * s, y - 4 * s)], 5),
                  4 * s, col=OJO_K, seed=seed + 3 + (d > 0), t=t)
        else:
            forma(im, elipse(x + d * 34 * s, y - 8 * s, 9 * s, 13 * s), OJO_K, t, seed + 3 + (d > 0), tinta=0)


def concurso(t):
    im = papel("calido")
    e = e_back(pr(t, tConcurso - 0.3, tConcurso + 0.1))
    trofeo(im, W / 2, 330, 1.4 * e, t, seed=12300)
    rotulo(im, "EL CONCURSO DE CADA AÑO", W / 2, 90, 70, rgb("b8443a"), t, seed=12310, esc=e)
    for k, (x, h) in enumerate(((W / 2, 230), (W / 2 - 360, 170), (W / 2 + 360, 120))):
        forma(im, rrect(x, 1080 - h / 2, 320, h, 8), rgb(["e9b949", "c9cfd6", "d9955a"][k]), t, 12320 + k, tinta=4.4)
        rotulo(im, str(k + 1), x, 1080 - h / 2, 70, BLANCO, t, seed=12330 + k)
        _compu(im, x, 1080 - h - 110 + 8 * math.sin(t * 3 + k), 0.95, t, "feliz" if k == 0 else "normal", 12340 + 10 * k)
    if t > tPrograma - 0.2:
        rotulo(im, "¿QUÉ PROGRAMA RECONOCE MEJOR LAS FOTOS?", W / 2, 520, 50, TINTA, t, seed=12380, tinta=False,
               esc=e_back(pr(t, tPrograma - 0.2, tPrograma + 0.1)))
    return im


# ------------------------------------------------------------ 2012: AlexNet
def alexnet(t):
    im = cabeza()
    rotulo(im, "2012", 240, 120, 90, rgb("f08a9a"), t, seed=12400, esc=e_back(pr(t, tDoce - 0.2, tDoce + 0.1)))
    if t > tAlex - 0.2:
        rotulo(im, "ALEXNET", 760, 120, 110, AMARILLO, t, seed=12401, esc=e_back(pr(t, tAlex - 0.2, tAlex + 0.1)))
    # la red PROFUNDA: losas en perspectiva, una tras otra
    n = int(8 * e_out(pr(t, tDoce - 0.1, tAlex + 0.6)))
    for k in range(n):
        x, y = 260 + 120 * k, 470 - 6 * k
        s = 1 - 0.04 * k
        pts = np.array([(x - 40 * s, y - 170 * s), (x + 40 * s, y - 210 * s), (x + 40 * s, y + 170 * s), (x - 40 * s, y + 210 * s)],
                       np.float32)
        forma(im, pts, lerp(rgb("cfe8ea"), rgb("f3cfd6"), k / 7), t, 12410 + k, tinta=4, alfa=0.92)
        if k:
            for j in range(3):
                brillo(im, x - 60, y - 120 + 120 * j, 14, AMARILLO, 0.6 * (0.5 + 0.5 * math.sin(t * 4 - k + j)))
    if t > tProfunda - 0.2:
        rotulo(im, "UNA RED PROFUNDA: MUCHOS PISOS", 680, 760, 46, BLANCO, t, seed=12420, esc=e_back(pr(t, tProfunda - 0.2, tProfunda + 0.1)))
    for k in range(2):
        eg = e_back(pr(t, tTarjetas - 0.3 + 0.25 * k, tTarjetas + 0.25 * k))
        if eg > 0.02:
            gpu(im, 1520, 380 + 250 * k, 0.85 * eg, t, seed=12430 + 20 * k)
    if t > tTarjetas:
        rotulo(im, "2 TARJETAS DE VIDEOJUEGOS", 1520, 150, 46, rgb("6ccf6a"), t, seed=12470, esc=e_back(pr(t, tTarjetas, tTarjetas + 0.3)))
    if t > tSesenta - 0.2:
        e = e_back(pr(t, tSesenta - 0.2, tSesenta + 0.2))
        rotulo(im, "60 000 000 DE PERILLAS", W / 2, 960, 80, AMARILLO, t, seed=12480, esc=e, rot=-0.02)
        for k in range(14):
            perilla(im, 140 + 130 * k, 860 - 20 * math.sin(k + t * 2), 28 * e, t, math.sin(k * 1.7 + t), seed=12490 + k)
    return im


# ------------------------------------------------------------ 15 % vs 26 %: los aplastó
def podio(t):
    im = papel("calido")
    rotulo(im, "SE EQUIVOCÓ EN…", W / 2, 110, 66, TINTA, t, seed=12500, tinta=False)
    base = 900
    aplasta = e_out(pr(t, tAplasto - 0.2, tAplasto + 0.25))
    for k, (nom, v, ti, col) in enumerate((("ALEXNET", 15.3, tQuince, VERDE), ("2.º LUGAR", 26.2, tVeinti, ROJO))):
        u = e_out(pr(t, ti - 0.4, ti + 0.4))
        if u <= 0:
            continue
        x = 680 + 560 * k
        h = 22 * v * u
        if k == 1:
            h *= 1 - 0.55 * aplasta                                 # el segundo lugar, aplastado
        forma(im, rrect(x, base - h / 2, 300, max(h, 6), 12), col, t, 12510 + k, tinta=4.6, luz=(BLANCO, -20, 20, 0.3))
        rotulo(im, f"{int(round(v)) if k else 15} %", x, base - h - 60, 80, col, t, seed=12520 + k, esc=e_back(pr(t, ti - 0.1, ti + 0.2)))
        rotulo(im, nom, x, base + 60, 48, TINTA, t, seed=12530 + k, tinta=False)
    if t > tAplasto - 0.2:
        rotulo(im, "¡LOS APLASTÓ!", W / 2, 260, 120, AMARILLO, t, seed=12540, esc=e_back(pr(t, tAplasto - 0.2, tAplasto + 0.1)), rot=-0.05)
        for k in range(3):
            destello(im, 1240 + 120 * (k - 1), 900 - 280 - 40 * k, 0.8 * aplasta, t, seed=1050 + k)
    kuri(im, 1700, 560, 1.5, t, cara="feliz" if t > tAplasto else "abiertos")
    return im


# ------------------------------------------------------------ la gráfica 2010-2015 (error top-5 del concurso ILSVRC)
DATOS = [(2010, 28.2), (2011, 25.8), (2012, 15.3), (2013, 11.7), (2014, 6.7), (2015, 3.6)]
HUMANO = 5.1


def grafica(t):
    im = papel("frio")
    x0, x1, y0, y1 = 300, 1500, 900, 220
    X = lambda a: lerp(x0, x1, (a - 2010) / 5)                       # noqa: E731
    Y = lambda v: lerp(y0, y1, v / 30)                               # noqa: E731
    linea(im, [(x0, y1 - 30), (x0, y0), (x1 + 60, y0)], 5, seed=12600, t=t, punta=False)
    for a, _ in DATOS:
        rotulo(im, str(a), X(a), y0 + 44, 34, TINTA, t, seed=12610 + a % 10, tinta=False)
    rotulo(im, "ERROR", x0, y1 - 70, 40, TINTA, t, seed=12620, tinta=False)
    # la línea de una persona entrenada
    linea(im, [(x0, Y(HUMANO)), (x1 + 60, Y(HUMANO))], 6, col=rgb("3f78c8"), seed=12621, t=t, punta=False, alfa=0.85)
    rotulo(im, "PERSONA ENTRENADA 5 %", x1 + 120, Y(HUMANO) - 50, 34, rgb("3f78c8"), t, seed=12622, tinta=False)
    u = pr(t, tCambio - 0.3, tPersona + 0.3)
    n = 1 + u * (len(DATOS) - 1)
    pts = []
    for k in range(int(n) + 1):
        if k >= len(DATOS):
            break
        a, v = DATOS[k]
        if k < int(n):
            pts.append((X(a), Y(v)))
        else:
            fr = n - int(n)
            a0, v0 = DATOS[k - 1]
            pts.append((lerp(X(a0), X(a), fr), lerp(Y(v0), Y(v), fr)))
    if len(pts) > 1:
        linea(im, pts, 8, col=ROJO, seed=12630, t=t, punta=False)
    for k, (a, v) in enumerate(DATOS[:int(n) + (1 if n % 1 > 0.95 else 0)]):
        forma(im, elipse(X(a), Y(v), 14, 14), ROJO if k != 2 else VERDE, t, 12640 + k, tinta=3)
        rotulo(im, f"{v:.1f} %".replace(".", ","), X(a) + 70, Y(v) - 30, 30, TINTA, t, seed=12650 + k, tinta=False)
    if t > tCambio - 0.1:
        rotulo(im, "ESE DÍA CAMBIÓ TODO", X(2012), Y(15.3) - 120, 46, VERDE, t, seed=12660, esc=e_back(pr(t, tCambio - 0.1, tCambio + 0.2)))
    if t > tPersona - 0.2:
        e = e_back(pr(t, tPersona - 0.2, tPersona + 0.2))
        brillo(im, X(2015), Y(3.6), 90, AMARILLO, 0.6 * e)
        destello(im, X(2015) + 40, Y(3.6) - 60, 0.9 * e, t, seed=1060)
        rotulo(im, "¡MENOS QUE UNA PERSONA!", 1150, 150, 70, AMARILLO, t, seed=12670, esc=e, rot=-0.03)
    rotulo(im, "Concurso ImageNet (ILSVRC), error top-5", 1640, 1030, 26, TINTA * 1.5, t, seed=12680, tinta=False, alfa=0.7)
    return im


TRAMOS = [(feifei, T_INI), (multitud, tContrato - 0.4), (concurso, tConcurso - 0.5), (alexnet, tDoce - 0.4),
          (podio, tQuince - 0.6), (grafica, tCambio - 0.5)]


def cuadro_crudo(t):
    k = 0
    for i, (_, ti) in enumerate(TRAMOS):
        if t >= ti:
            k = i
    f, ti = TRAMOS[k]
    im = f(t)
    if t < ti + 0.6:
        if k > 0:
            im = desborde(TRAMOS[k - 1][0](t), im, pr(t, ti, ti + 0.6), W * (0.25 + 0.1 * k), H * 0.5)
        else:
            import plano_f
            im = desborde(plano_f.cuadro_crudo(t), im, pr(t, ti, ti + 0.6), W * 0.5, H * 0.5)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
