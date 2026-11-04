# -*- coding: utf-8 -*-
"""APRENDER: una pared de perillas que giran al azar (Kuri recién nacido, mareado) → la niña le enseña el gato: «¿TOSTADORA?»
¡MAL! → el error (una bola roja) baja por la torre piso por piso y las perillas giran un poquito → frío o caliente: millones
de perillas pintadas de azul y rojo → «¿PERRO?» (menos mal) → «¿GATO… CREO?» con el medidor de error bajando → millones de
fotos que vuelan y las perillas forman detectores (bordes, bigotes, orejas) → RETROPROPAGACIÓN: la culpa se reparte en
gotitas → el problema: una montaña absurda de fotos."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lerp, linea, pr, rgb, rotulo, rrect,
                      suave, terminar)
from comun import T0, T1, desborde, ww
from fondos_ia import cabeza, papel
from iconos_ia import (bigotes, foto_cosa, marca_x, oreja, palomita, perilla, perro, rejilla_perillas, tostadora, torre, trazo)
from personajes import AMARILLO, BLANCO, OJO_K, destello, gota, kuri, pregunta
from personajes_ia import dibujo_nino, foto_gato, globo, meme_gato, nina, pegar, radiografia

E = "aprender"
T_INI = T0(E)
tPerillas, tAzar, tRecien, tNada = ww(E, 0, "perillas"), ww(E, 0, "azar"), ww(E, 0, "recien"), ww(E, 0, "nada")
tEnsenas, tTost, tMal = ww(E, 1, "ensenas"), ww(E, 1, "tostadora"), ww(E, 1, "mal")
tMide, tError, tAtras, tPiso, tCada, tMenos = (ww(E, 2, "mide"), ww(E, 2, "error"), ww(E, 2, "atras"), ww(E, 2, "piso"),
                                               ww(E, 2, "cada"), ww(E, 2, "menos"))
tFrio, tCaliente, tMillones = ww(E, 3, "frio"), ww(E, 3, "caliente"), ww(E, 3, "millones")
tOtra, tPerro, tMenosMal, tGiran = ww(E, 4, "otra"), ww(E, 4, "perro"), ww(E, 4, "menos"), ww(E, 4, "giran")
tOtra2, tGato, tCreo, tCasi = ww(E, 4, "otra", n=1), ww(E, 4, "gato"), ww(E, 4, "creo"), ww(E, 4, "casi")
tRepite, tFotos, tSolitas = ww(E, 5, "repitelo"), ww(E, 5, "fotos"), ww(E, 5, "solitas")
tDet = [ww(E, 5, "bordes"), ww(E, 5, "bigotes"), ww(E, 5, "orejas")]
tRetro, tCulpa, tAprenden = ww(E, 6, "retropropagacion"), ww(E, 6, "culpa"), ww(E, 6, "aprenden")
tProblema, tAbsurda = ww(E, 7, "problema"), ww(E, 7, "absurda")
T_FIN = T1(E)
ROJO = rgb("e35d4a")
AZUL = rgb("5a9bd8")


def _rnd(i, j, k=0):
    return ((i * 7919 + j * 104729 + k * 1299709) % 1000) / 1000.0


def medidor(im, t, x, y, valor, seed=11000, alfa=1.0):
    """Medidor de error horizontal: barra roja que se llena según `valor` (0..1) y el porcentaje."""
    forma(im, rrect(x, y, 520, 70, 30), BLANCO, t, seed, tinta=4, alfa=alfa)
    w = max(10, 480 * valor)
    forma(im, rrect(x - 240 + w / 2, y, w, 44, 20), lerp(rgb("6aa84f"), ROJO, valor), t, seed + 1, tinta=0, alfa=alfa)
    rotulo(im, "ERROR", x - 340, y, 44, ROJO, t, seed=seed + 2, alfa=alfa)
    rotulo(im, f"{int(round(valor * 100))} %", x + 330, y, 50, TINTA, t, seed=seed + 3, tinta=False, alfa=alfa)


# ------------------------------------------------------------ perillas al azar
def azar(t):
    im = cabeza()
    rejilla_perillas(im, t, 760, 200, 10, 6, 112, 40, lambda i, j: math.sin(t * (1.5 + 3 * _rnd(i, j)) + 6 * _rnd(j, i, 1)),
                     seed=11100)
    if t > tAzar - 0.1:
        rotulo(im, "TODAS AL AZAR", 1265, 940, 70, AMARILLO, t, seed=11050, esc=e_back(pr(t, tAzar - 0.1, tAzar + 0.2)))
    k_ = "mareo" if t > tNada - 0.2 else ("abiertos" if t > tRecien else "normal")
    kuri(im, 330, 560, 1.7, t, cara=k_, rot=0.15 * math.sin(t * 2) if t > tNada else 0)
    if t > tRecien - 0.2:
        rotulo(im, "RECIÉN NACIDA", 330, 260, 46, BLANCO, t, seed=11051, esc=e_back(pr(t, tRecien - 0.2, tRecien + 0.1)))
    if t > tNada - 0.1:
        rotulo(im, "NO SABE NADA", 330, 860, 52, rgb("f08a9a"), t, seed=11052, esc=e_back(pr(t, tNada - 0.1, tNada + 0.2)), rot=0.04)
    return im


# ------------------------------------------------------------ «¿tostadora?» ¡MAL!
def tostadora_mal(t):
    im = papel("calido")
    foto = foto_gato(t)

    p = nina(im, 360, 660, 1.5, t, cara="normal" if t < tMal else "apretados", boca="sonrisa" if t < tMal else "duda",
             brazos=(0.3, 1.5), codos=(0.4, 0.3), mira=1.0)
    mx, my = p["manos"][1]
    pegar(im, foto, mx + 230, my - 60, 0.72, 0.06, t=t, seed=11201, marco=16)
    kuri(im, 1420, 600, 2.0, t, cara="feliz" if t < tMal else "triste")
    if t > tTost - 0.6:
        n = 12 * pr(t, tTost - 0.5, tTost + 0.3)
        globo(im, 1400, 250, 700, 200, "", t, px=50, n=n, lineas=["¿TOSTADORA?"], seed=11210, cola=(-1, 1))
        tostadora(im, 1650, 250, 0.6 * e_back(pr(t, tTost, tTost + 0.3)), t, seed=11220)
    if t > tMal - 0.1:
        e = e_back(pr(t, tMal - 0.1, tMal + 0.2))
        marca_x(im, 1650, 250, 1.2 * e, t, seed=11230)
        rotulo(im, "¡MAL!", W / 2, 950, 130, ROJO, t, seed=11231, esc=e, rot=-0.05)
    return im


# ------------------------------------------------------------ el error baja por la torre
def _perillas_piso(im, t, pisos, k, giro):
    x, y, wk, h = pisos[k]
    for j in range(3):
        v = math.sin(k * 1.7 + j * 2.3) * 0.8 + giro * (0.35 if (k + j) % 2 else -0.35)
        perilla(im, x + wk / 2 + 70 + j * 78, y, 30, t, v, seed=11300 + 10 * k + j)
        if 0 < giro < 1:
            linea(im, curva([(x + wk / 2 + 70 + j * 78 - 34, y - 34), (x + wk / 2 + 70 + j * 78, y - 52),
                             (x + wk / 2 + 70 + j * 78 + 34, y - 34)], 6), 4, col=AMARILLO, seed=11340 + 10 * k + j, t=t)


def error_atras(t):
    im = cabeza()
    pisos = torre(im, t, x=640, y0=1010, w=680, alto_p=190, crece=1.0, activo=(0.4, 0.4, 0.4, 0.4), contenido=True)
    medidor(im, t, 1380, 120, 0.92, alfa=e_back(pr(t, tMide - 0.2, tMide + 0.2)))
    # la bola del error: arriba (sobre el techo) → baja piso por piso
    u = pr(t, tAtras - 0.2, tCada + 0.5)
    yb = lerp(pisos[3][1] - 230, pisos[0][1], e_in(u)) if t > tError - 0.2 else pisos[3][1] - 230
    eb = e_back(pr(t, tError - 0.3, tError))
    if eb > 0.02:
        brillo(im, 640, yb, 120, ROJO, 0.6)
        forma(im, elipse(640, yb, 54 * eb, 54 * eb), ROJO, t, 11350, tinta=4, luz=(BLANCO, -14, 16, 0.4))
        rotulo(im, "ERROR", 640, yb, 30, BLANCO, t, seed=11351, tinta=False, esc=eb)
    if t > tAtras - 0.2:
        rotulo(im, "HACIA ATRÁS ↓", 330, 160, 56, ROJO, t, seed=11352, esc=e_back(pr(t, tAtras - 0.2, tAtras + 0.1)),
               fuente="seguisym.ttf")
    for k in range(4):
        y_k = pisos[k][1]
        llego = 1.0 if yb >= y_k - 10 and t > tAtras else 0.0
        giro = pr(t, tCada + 0.2 * (3 - k), tGirar_aprox(k)) if llego else 0.0
        _perillas_piso(im, t, pisos, k, giro)
    if t > tMenos - 0.3:
        rotulo(im, "UN POQUITO, PARA EQUIVOCARSE MENOS", 1340, 990, 46, AMARILLO, t, seed=11360,
               esc=e_back(pr(t, tMenos - 0.3, tMenos)))
    return im


def tGirar_aprox(k):
    return tCada + 1.4 + 0.2 * (3 - k)


# ------------------------------------------------------------ frío o caliente
def frio_caliente(t):
    im = papel("frio")
    n = 1 if t < tMillones - 0.2 else 1 + int(5 * e_out(pr(t, tMillones - 0.2, tMillones + 0.8)))
    paso = 150 / (1 + 0.5 * (n - 1))
    cols, filas = int(1500 / paso), int(720 / paso)
    r = paso * 0.32

    def tinte(i, j):
        v = _rnd(i, j, 3)
        a = pr(t, tFrio - 0.2 + 0.4 * v, tCaliente + 0.3 * v)
        return lerp(rgb("e8e0d0"), AZUL if v < 0.5 else ROJO, a)
    rejilla_perillas(im, t, 210 + paso / 2, 250 + paso / 2, cols, filas, paso, r,
                     lambda i, j: math.sin(t * 2 + 6 * _rnd(i, j)) * 0.7, tinte=tinte, seed=11400)
    rotulo(im, "¡FRÍO!", 520, 140, 90, AZUL, t, seed=11450, esc=e_back(pr(t, tFrio - 0.1, tFrio + 0.2)), rot=-0.04)
    rotulo(im, "¡CALIENTE!", 1380, 140, 90, ROJO, t, seed=11451, esc=e_back(pr(t, tCaliente - 0.1, tCaliente + 0.2)), rot=0.04)
    if t > tMillones - 0.1:
        rotulo(im, "MILLONES DE JUGADORES A LA VEZ", W / 2, 1000, 56, TINTA, t, seed=11452,
               esc=e_back(pr(t, tMillones - 0.1, tMillones + 0.2)), tinta=False)
    return im


# ------------------------------------------------------------ otra foto: perro… gato, creo
def intentos(t):
    im = papel("calido")
    k = 0 if t < tOtra2 - 0.3 else 1
    foto = foto_gato(t, pose="despierto" if k == 0 else "dormido")
    pegar(im, foto, 420, 470, 0.95, -0.04 + 0.06 * k, t=t, seed=11500 + k, marco=18)
    rotulo(im, ["OTRA FOTO", "OTRA MÁS"][k], 420, 140, 56, TINTA, t, seed=11502 + k, tinta=False,
           esc=e_back(pr(t, [tOtra, tOtra2][k] - 0.2, [tOtra, tOtra2][k] + 0.1)))
    kuri(im, 1500, 620, 1.6, t, cara="normal" if k == 0 else ("feliz" if t > tCasi else "normal"))
    if k == 0 and t > tPerro - 0.4:
        globo(im, 1320, 300, 600, 200, "", t, px=50, n=8 * pr(t, tPerro - 0.4, tPerro + 0.2), lineas=["¿PERRO?"], seed=11510)
        perro(im, 1530, 320, 0.6 * e_back(pr(t, tPerro, tPerro + 0.3)), t, seed=11520, col=rgb("c98a4a"), sx=-1)
    if k == 1 and t > tGato - 0.4:
        globo(im, 1300, 300, 560, 130, "", t, px=46, n=14 * pr(t, tGato - 0.4, tCreo + 0.3), lineas=["¿GATO… CREO?"], seed=11511)
    # medidor de error que baja: 92 → 55 → 18
    v = 0.92
    v = lerp(v, 0.55, suave(pr(t, tPerro, tMenosMal + 0.3)))
    v = lerp(v, 0.18, suave(pr(t, tGato, tCreo + 0.5)))
    medidor(im, t, 1180, 960, v, seed=11530)
    if t > tMenosMal - 0.1 and k == 0:
        rotulo(im, "MAL… PERO MENOS MAL", 1300, 820, 50, rgb("e8933a"), t, seed=11540, esc=e_back(pr(t, tMenosMal - 0.1, tMenosMal + 0.2)))
    # perillas que giran
    for j in range(5):
        g = suave(pr(t, tGiran, tGiran + 0.8)) + suave(pr(t, tOtra2 + 0.6, tOtra2 + 1.2))
        perilla(im, 140 + 120 * j, 930, 40, t, math.sin(j * 1.9) * 0.6 + 0.25 * g * (1 if j % 2 else -1), seed=11550 + j)
    if t > tGiran - 0.1 and t < tOtra2:
        rotulo(im, "GIRAN LAS PERILLAS", 380, 840, 40, AMARILLO, t, seed=11560, esc=e_back(pr(t, tGiran - 0.1, tGiran + 0.2)))
    if t > tCasi - 0.1:
        palomita(im, 1530, 300, 0.9 * e_back(pr(t, tCasi - 0.1, tCasi + 0.2)), t, seed=11570)
        rotulo(im, "¡YA CASI!", 1500, 820, 80, rgb("2e8b4a"), t, seed=11571, esc=e_back(pr(t, tCasi - 0.1, tCasi + 0.2)), rot=-0.04)
    return im


# ------------------------------------------------------------ millones de veces
def _tarjetas(t):
    return [foto_gato(t), foto_cosa("perro", t), foto_cosa("tostadora", t), dibujo_nino(t), foto_cosa("volcan", t),
            foto_gato(t, "despierto"), foto_cosa("bici", t), meme_gato(t)]


def millones(t):
    im = cabeza()
    # una corriente de fotos que pasa volando hacia la torre
    cards = _tarjetas(t)
    vel = 1.0 + 3.0 * pr(t, tRepite, tFotos + 1.0)
    for k in range(10):
        ph = ((t - tRepite) * 0.35 * vel + k / 10) % 1
        x = lerp(-200, 980, ph)
        y = 520 + 300 * math.sin(k * 2.1) + 60 * math.sin(t + k)
        pegar(im, cards[k % len(cards)], x, y, 0.36, 0.2 * math.sin(k + t), t=t, seed=11600 + k, marco=8, alfa=math.sin(math.pi * ph))
    rotulo(im, "× MILLONES", 420, 140, 90, AMARILLO, t, seed=11610, esc=e_back(pr(t, tRepite - 0.1, tRepite + 0.2)), rot=-0.05)
    # la rejilla de perillas que se acomoda sola
    asienta = suave(pr(t, tSolitas - 0.5, tSolitas + 0.8))
    rejilla_perillas(im, t, 1080, 160, 7, 3, 100, 34,
                     lambda i, j: lerp(math.sin(t * (2 + 3 * _rnd(i, j)) + 6 * _rnd(j, i)), [0.9, 0.0, -0.9][i % 3], asienta),
                     seed=11620)
    if t > tSolitas - 0.2:
        rotulo(im, "SOLITAS", 1380, 460, 50, BLANCO, t, seed=11630, esc=e_back(pr(t, tSolitas - 0.2, tSolitas + 0.1)))
    for k, (ti, nom) in enumerate(zip(tDet, ("BORDES", "BIGOTES", "OREJAS"))):
        e = e_back(pr(t, ti - 0.15, ti + 0.2))
        if e <= 0.02:
            continue
        x, y = 1080 + 270 * k, 720
        forma(im, elipse(x, y, 110 * e, 110 * e), rgb("fbf3df"), t, 11640 + k, tinta=5)
        if k == 0:
            for j in range(3):
                trazo(im, x - 40 + 40 * j, y, 1.1 * e, t, math.pi / 2, rgb("e8a33a"), seed=11650 + j)
        elif k == 1:
            bigotes(im, x, y, 1.0 * e, t, seed=11660)
        else:
            oreja(im, x, y + 6, 1.2 * e, t, seed=11670)
        rotulo(im, nom, x, y + 150, 42, AMARILLO, t, seed=11680 + k, esc=e)
    if t > tDet[0] - 0.2:
        rotulo(im, "DETECTORES:", 1350, 560, 46, BLANCO, t, seed=11690, esc=e_back(pr(t, tDet[0] - 0.2, tDet[0] + 0.1)))
    return im


# ------------------------------------------------------------ retropropagación: la culpa repartida
def retro(t):
    im = cabeza()
    rotulo(im, "RETROPROPAGACIÓN", W / 2, 130, 110, AMARILLO, t, seed=11700, esc=e_back(pr(t, tRetro - 0.1, tRetro + 0.3)))
    cols, filas, paso = 12, 4, 120
    x0, y0 = W / 2 - (cols - 1) * paso / 2, 600
    rejilla_perillas(im, t, x0, y0, cols, filas, paso, 38, lambda i, j: math.sin(i * 1.3 + j * 2.1 + t * 0.6) * 0.6, seed=11710)
    # la bola del error se parte en gotitas, una para cada perilla
    eb = e_back(pr(t, tRetro, tRetro + 0.3))
    parte = pr(t, tCulpa - 0.2, tCulpa + 1.2)
    if parte < 0.15:
        brillo(im, W / 2, 330, 140, ROJO, 0.6 * eb)
        forma(im, elipse(W / 2, 330, 70 * eb, 70 * eb), ROJO, t, 11720, tinta=4)
        rotulo(im, "ERROR", W / 2, 330, 36, BLANCO, t, seed=11721, tinta=False, esc=eb)
    else:
        for j in range(filas):
            for i in range(cols):
                tx, ty = x0 + i * paso, y0 + j * paso - 50
                u = e_in(clamp((parte - 0.15) * 1.3 - 0.02 * (i + j)))
                if u >= 1:
                    continue
                gota(im, lerp(W / 2, tx, u), lerp(330, ty, u), 0.7, t, seed=11730 + i + cols * j, alfa=0.9)
    if t > tCulpa - 0.1:
        rotulo(im, "LA CULPA, REPARTIDA", W / 2, 1010, 56, rgb("f08a9a"), t, seed=11790, esc=e_back(pr(t, tCulpa - 0.1, tCulpa + 0.2)))
    if t > tAprenden - 0.2:
        kuri(im, 1760, 330, 1.2, t, cara="feliz")
        rotulo(im, "ASÍ APRENDEN CASI TODAS", 1500, 470, 40, BLANCO, t, seed=11791, esc=e_back(pr(t, tAprenden - 0.2, tAprenden + 0.1)))
    return im


# ------------------------------------------------------------ el problema: una montaña de fotos
def montana(t):
    im = papel("calido")
    cards = _tarjetas(t)
    n = int(34 * e_out(pr(t, tProblema - 0.2, tAbsurda + 1.0)))
    for k in range(n):
        r = _rnd(k, 3)
        fila = int(math.sqrt(k))
        x = W / 2 + (r - 0.5) * (900 - 200 * fila * 0.7)
        y = 980 - 80 * fila - 30 * _rnd(k, 5)
        pegar(im, cards[k % len(cards)], x, y, 0.32, (r - 0.5) * 0.8, t=t, seed=11800 + k, marco=8)
    kuri(im, 300, 520, 1.6, t, cara="susto" if t > tAbsurda else "abiertos")
    if t > tAbsurda - 0.2:
        rotulo(im, "UNA CANTIDAD ABSURDA DE FOTOS", W / 2 + 120, 130, 70, ROJO, t, seed=11850,
               esc=e_back(pr(t, tAbsurda - 0.2, tAbsurda + 0.1)), rot=-0.03)
    elif t > tProblema - 0.1:
        rotulo(im, "SOLO UN PROBLEMA…", W / 2 + 120, 130, 70, TINTA, t, seed=11851, esc=e_back(pr(t, tProblema - 0.1, tProblema + 0.2)))
    return im


TRAMOS = [(azar, T_INI), (tostadora_mal, tEnsenas - 0.5), (error_atras, tMide - 0.4), (frio_caliente, tFrio - 0.4),
          (intentos, tOtra - 0.4), (millones, tRepite - 0.4), (retro, tRetro - 0.4), (montana, tProblema - 0.4)]


def cuadro_crudo(t):
    k = 0
    for i, (_, ti) in enumerate(TRAMOS):
        if t >= ti:
            k = i
    f, ti = TRAMOS[k]
    im = f(t)
    if t < ti + 0.6:
        if k > 0:
            im = desborde(TRAMOS[k - 1][0](t), im, pr(t, ti, ti + 0.6), W * (0.25 + 0.08 * k), H * 0.5)
        else:
            import plano_e
            im = desborde(plano_e.cuadro_crudo(t), im, pr(t, ti, ti + 0.6), W * 0.5, H * 0.5)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
