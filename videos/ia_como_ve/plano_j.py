# -*- coding: utf-8 -*-
"""TRUCOS: «tú ves» la foto, «la IA ve» patrones (mapa de bordes) → el experimento tramposo: lobos siempre en la nieve,
huskies en el pasto → un husky en la nieve: «¿LOBO?» y el foco de atención cae en la nieve, no en el animal → el panda + unas
manchitas que no notas = «GIBÓN 99 %» (Goodfellow y otros, 2014: panda 57,7 % → gibón 99,3 %) → los científicos siguen
asomándose a sus pisos."""
import math

import numpy as np

from acuarela import (H, W, TINTA, brillo, clamp, curva, e_back, e_in, e_out, elipse, forma, lerp, linea, pr, rgb, rotulo, rrect,
                      suave, terminar)
from comun import T0, T1, desborde, ww
from fondos_ia import cabeza, papel
from iconos_ia import foto_cosa, marca_x, torre
from personajes import AMARILLO, BLANCO, OJO_K, destello, gota, kuri, pregunta
from personajes_ia import foto_gato, nina, pegar

E = "trucos"
T_INI = T0(E)
tOjo, tPatrones, tEquiv = ww(E, 0, "ojo"), ww(E, 0, "patrones"), ww(E, 0, "equivocados")
tExper, tTramposas, tLobos, tHusky, tNieve, tAnimal = (ww(E, 1, "experimento"), ww(E, 1, "tramposas"), ww(E, 1, "lobos"),
                                                       ww(E, 1, "husky"), ww(E, 1, "nieve"), ww(E, 1, "animal"))
tPanda, tManchitas, tJuro, tNoventa, tGibon = (ww(E, 2, "panda"), ww(E, 2, "manchitas"), ww(E, 2, "juro"), ww(E, 2, "noventa"),
                                               ww(E, 2, "gibon"))
tCient, tVerdad = ww(E, 3, "cientificos"), ww(E, 3, "verdad")
T_FIN = T1(E)
ROJO = rgb("e35d4a")
VERDE = rgb("4f9a5a")


def patrones(t):
    im = papel("calido")
    import plano_d
    pegar(im, foto_gato(t), 520, 500, 0.95, -0.03, t=t, seed=15000, marco=14)
    rotulo(im, "TÚ VES", 520, 150, 70, rgb("3f78c8"), t, seed=15001)
    e = e_back(pr(t, tOjo + 0.3, tOjo + 0.7))
    pegar(im, plano_d._mapa("vertical"), 1400, 500, 0.95 * e, 0.03, t=t, seed=15002, marco=14, marco_col=rgb("2b3648"))
    rotulo(im, "LA IA VE", 1400, 150, 70, rgb("b8443a"), t, seed=15003, esc=e)
    if t > tPatrones - 0.2:
        rotulo(im, "PATRONES", 1400, 880, 80, AMARILLO, t, seed=15004, esc=e_back(pr(t, tPatrones - 0.2, tPatrones + 0.1)), rot=-0.04)
    if t > tEquiv - 0.2:
        rotulo(im, "…A VECES, LOS EQUIVOCADOS", W / 2, 1010, 54, ROJO, t, seed=15005, esc=e_back(pr(t, tEquiv - 0.2, tEquiv + 0.1)))
    return im


def husky(t):
    im = papel("frio")
    rotulo(im, "FOTOS TRAMPOSAS", 470, 90, 60, ROJO, t, seed=15100, esc=e_back(pr(t, tTramposas - 0.2, tTramposas + 0.1)))
    for k in range(4):                                              # entrenamiento: lobos en nieve, huskies en pasto
        lobo = k < 2
        ti = tExper + 0.6 + 0.5 * k
        e = e_back(pr(t, ti, ti + 0.35))
        x, y = 270 + 400 * (k % 2), 330 + 380 * (k // 2)
        pegar(im, foto_cosa("lobo" if lobo else "husky", t), x, y, 0.85 * e, 0.04 * (k - 1.5), t=t, seed=15110 + k, marco=10)
        if e > 0.5:
            rotulo(im, "LOBO" if lobo else "HUSKY", x, y + 175, 40, TINTA, t, seed=15120 + k, tinta=False)
    linea(im, [(900, 160), (900, 980)], 4, col=rgb("9aa4ae"), seed=15130, t=t, punta=False, alfa=0.6)
    if t > tHusky + 0.6:                                            # la prueba: un husky en la nieve
        e = e_back(pr(t, tHusky + 0.6, tHusky + 1.0))
        pegar(im, foto_cosa("husky_nieve", t), 1400, 480, 1.35 * e, 0, t=t, seed=15140, marco=14)
        rotulo(im, "LA PRUEBA", 1400, 120, 56, rgb("3f78c8"), t, seed=15141, esc=e)
        if t > tNieve - 0.4:
            a = e_out(pr(t, tNieve - 0.4, tNieve + 0.2))
            for k in range(6):                                      # el foco de atención cae en la nieve
                brillo(im, 1180 + 90 * k, 650 + 20 * math.sin(k + t * 2), 90, rgb("ffcf6a"), 0.55 * a)
            rotulo(im, "¿LOBO?", 1650, 280, 70, ROJO, t, seed=15142, esc=e_back(pr(t, tNieve - 0.4, tNieve - 0.1)), rot=0.05)
            rotulo(im, "MIRÓ LA NIEVE", 1400, 860, 60, AMARILLO * 0.85, t, seed=15143, esc=a)
        if t > tAnimal - 0.2:
            marca_x(im, 1360, 470, 0.8 * e_back(pr(t, tAnimal - 0.2, tAnimal + 0.1)), t, seed=15144)
            rotulo(im, "NO EL ANIMAL", 1400, 960, 50, ROJO, t, seed=15145, esc=e_back(pr(t, tAnimal - 0.2, tAnimal + 0.1)))
    return im


def _ruido_img():
    rg = np.random.default_rng(7)
    n = rg.random((270 // 9, 360 // 9, 3)).astype(np.float32)
    import cv2
    return cv2.resize(n, (360, 270), interpolation=cv2.INTER_NEAREST)


def panda(t):
    im = papel("calido")
    p = foto_cosa("panda", t)
    pegar(im, p, 330, 470, 0.95, -0.03, t=t, seed=15200, marco=14)
    rotulo(im, "PANDA 58 %", 330, 760, 50, VERDE, t, seed=15201, esc=e_back(pr(t, tPanda - 0.2, tPanda + 0.1)))
    em = e_back(pr(t, tManchitas - 0.3, tManchitas + 0.1))
    if em > 0.02:
        rotulo(im, "+", 640, 470, 120, TINTA, t, seed=15202, tinta=False, esc=em)
        pegar(im, _ruido_img(), 920, 470, 0.85 * em, 0.02, t=t, seed=15203, marco=10)
        rotulo(im, "MANCHITAS (× 0,007)", 920, 760, 40, TINTA, t, seed=15204, tinta=False, esc=em)
        rotulo(im, "=", 1210, 470, 120, TINTA, t, seed=15205, tinta=False, esc=em)
        mix = np.clip(p + (_ruido_img() - 0.5) * 0.04, 0, 1)
        pegar(im, mix, 1530, 470, 0.95 * em, 0.03, t=t, seed=15206, marco=14)
        rotulo(im, "¿LA MISMA FOTO?", 1530, 140, 46, TINTA, t, seed=15207, tinta=False, esc=em)
    if t > tJuro - 0.2:
        a = e_back(pr(t, tJuro - 0.2, tJuro + 0.1))
        forma(im, rrect(1530, 800, 420 * a, 120 * a, 20), ROJO, t, 15210, tinta=5)
        txt = "GIBÓN 99 %" if t > tNoventa else "GIBÓN"
        rotulo(im, txt, 1530, 800, int(64 * a) + 2, BLANCO, t, seed=15211)
        kuri(im, 1820, 300, 1.1, t, cara="feliz")
    if t > tGibon - 0.2:
        rotulo(im, "¡JURADO!", 1530, 960, 54, ROJO, t, seed=15212, esc=e_back(pr(t, tGibon - 0.2, tGibon + 0.1)), rot=-0.05)
    return im


def asomarse(t):
    im = cabeza()
    torre(im, t, x=760, y0=1010, w=720, alto_p=190, crece=1.0, activo=[0.35 + 0.65 * (int(t * 0.8) % 4 == k) for k in range(4)],
          foco=int(t * 0.8) % 4)
    p = nina(im, 1540, 640, 1.45, t, cara="abiertos", boca="o", brazos=(0.4, 2.0), codos=(0.3, 0.9), mira=-1.0)
    hx, hy = p["manos"][1]
    forma(im, elipse(hx - 90, hy - 40, 62, 62), rgb("dff3f6"), t, 15300, tinta=7, alfa=0.55)
    linea(im, [(hx - 46, hy + 4), (hx, hy)], 16, col=rgb("7a4a2a"), seed=15301, t=t)
    if t > tVerdad - 0.3:
        rotulo(im, "¿QUÉ ESTÁ MIRANDO DE VERDAD?", W / 2, 90, 66, AMARILLO, t, seed=15310, esc=e_back(pr(t, tVerdad - 0.3, tVerdad)))
    else:
        rotulo(im, "LOS CIENTÍFICOS SIGUEN ASOMÁNDOSE", W / 2, 90, 56, BLANCO, t, seed=15311, esc=e_back(pr(t, tCient - 0.2, tCient + 0.1)))
    return im


TRAMOS = [(patrones, T_INI), (husky, tExper - 0.4), (panda, tPanda - 0.5), (asomarse, tCient - 0.6)]


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
            import plano_i
            im = desborde(plano_i.cuadro_crudo(t), im, pr(t, ti, ti + 0.6), W * 0.5, H * 0.5)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
