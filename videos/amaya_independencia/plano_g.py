# -*- coding: utf-8 -*-
"""ETAPA 3 · RESISTENCIA (1815-1820, Guerrero y Victoria): «3 RESISTENCIA» → montañas: quedaban pocos, escondidos → Guerrero y
Guadalupe Victoria se asoman detrás de las montañas («¡ATACAN!») y se esconden («¡A ESCONDERSE!»): guerrillas → chiste: una niña
en su pupitre aguantando el último día antes de vacaciones (reloj, calendario) → dato chido: Guadalupe Victoria con la banda
presidencial, «1.er PRESIDENTE DE MÉXICO»."""
import math

import numpy as np

from acuarela import H, W, TINTA, curva, e_out, elipse, forma, linea, pr, rgb, rotulo, rrect, suave, terminar
from comun import T0, ww
from fondos_amaya import papel, _manchas
from personajes import AMARILLO, destello, exclama, gota
from personajes_ia import nina
from kit_amaya import AZUL, CAFE, CREMA, DORADO, GRIS, ROJO, VERDE, cache, cam, chispas, entra, gente, letrero, papa, tarjeta
from piezas_fj import BLANCO_B, ROJO_B, VERDE_B, base, cabecera, montanas

T_INI = T0("resistencia")
C = "resistencia"
tTres, tRes, tMil, tQued, tPocos, tEsc, tMont = (ww(C, 0, "tres"), ww(C, 0, "resistencia"), ww(C, 0, "mil"),
                                                 ww(C, 0, "quedaban"), ww(C, 0, "pocos"), ww(C, 0, "escondidos"),
                                                 ww(C, 0, "montanas"))
tGue, tVic, tGuerr, tAtac, tEscon, tAguan, tUlt, tVac = (ww(C, 1, "vicente"), ww(C, 1, "guadalupe"), ww(C, 1, "guerrillas"),
                                                        ww(C, 1, "atacaban"), ww(C, 1, "escondian"), ww(C, 1, "aguantaron"),
                                                        ww(C, 1, "ultimo"), ww(C, 1, "vacaciones"))
tDato, tVic2, tPrim, tPres = ww(C, 2, "dato"), ww(C, 2, "guadalupe"), ww(C, 2, "primer"), ww(C, 2, "presidente")
T_MONT = tQued - 0.4
T_CHISTE = tAguan - 0.5
T_DATO = tDato - 0.6
COL = rgb("a8d8b0")


def cab(im, t):
    cabecera(im, t, "3 · RESISTENCIA · 1815-1820", COL, 15000)


def _mascara_frente():
    """Máscara (0..1) de las dos montañas delanteras + el suelo: lo que tapa a quien se esconde detrás."""
    import cv2
    from acuarela import curva as cv_
    m = np.zeros((H, W), np.float32)
    y0 = 900
    for cx, w, h in ((560, 640, 420), (1240, 700, 470)):
        p = cv_([(cx - w / 2, y0), (cx - w * 0.18, y0 - h * 0.8), (cx, y0 - h), (cx + w * 0.2, y0 - h * 0.75), (cx + w / 2, y0)], 8)
        p = np.vstack([p, [(cx + w / 2, H), (cx - w / 2, H)]]).astype(np.int32)
        cv2.fillPoly(m, [p], 1.0, cv2.LINE_AA)
    m[y0 - 12:] = 1
    m = cv2.GaussianBlur(m, (0, 0), 1.5)
    return m[..., None]


def tapa(im):
    bg = cache("g_mont", _fondo_mont)
    m = cache("g_masc", _mascara_frente)
    im *= 1 - m
    im += bg * m


def _fondo_mont():
    im = papel("frio")
    montanas(im, 0, seed=15010)
    return im


def titulo(t):
    im = cache("g_tit", lambda: papel("frio")).copy()
    cab(im, t)
    rotulo(im, "3", 760, 400, 300, COL, t, seed=15020, esc=entra(t, tTres - 0.3))
    rotulo(im, "RESISTENCIA", 760, 660, 130, VERDE, t, seed=15021, esc=entra(t, tRes - 0.2))
    letrero(im, "1815 – 1820", 760, 820, 60, t, col=CREMA, seed=15022, esc=entra(t, tMil - 0.2))
    for k, n in enumerate(("guerrero", "victoria")):
        cam(im, n, 1150 + 230 * k, 430 + 40 * k, 0.55 * entra(t, tRes + 0.2 * k), t, "", seed=74 + k, rot=(k - 0.5) * 0.12)
    return im


def asoma(t, t_sube, t_baja, periodo=None):
    """0 (escondido) .. 1 (arriba): sube en t_sube y baja en t_baja; después sigue asomándose en ciclos."""
    if t < t_sube:
        return 0.0
    if t < t_baja:
        return e_out(pr(t, t_sube, t_sube + 0.35))
    v = 1 - suave(pr(t, t_baja, t_baja + 0.3))
    if periodo and t > t_baja + 0.6:
        f = ((t - t_baja - 0.6) / periodo) % 1
        v = max(v, math.sin(math.pi * pr(f, 0.2, 0.8)) ** 0.5)
    return v


def montes(t):
    im = cache("g_mont", _fondo_mont).copy()
    cab(im, t)
    # quedaban pocos: tres personitas que se agachan tras la montaña
    if t < tGue - 0.3:
        for k in range(3):
            e = entra(t, tPocos - 0.3 + 0.12 * k)
            baja = suave(pr(t, tEsc - 0.1, tEsc + 0.4))
            gente(im, 470 + 90 * k, 540 + 160 * baja, 1.8 * e + 0.01, t, seed=190 + k, col=rgb("6a8a4a"),
                  cara="susto" if baja > 0.5 else "normal")
        tapa(im)   # la montaña delantera los tapa
        letrero(im, "QUEDABAN POCOS", 560, 230, 58, t, col=CREMA, seed=15030, esc=entra(t, tPocos - 0.3))
        if t > tEsc - 0.3:
            letrero(im, "ESCONDIDOS EN LAS MONTAÑAS", 900, 330, 52, t, col=AMARILLO, seed=15035, esc=entra(t, tEsc - 0.3), rot=-0.03)
        return im
    # Guerrero y Victoria se asoman y se esconden (guerrillas)
    for k, (nom, tk, x) in enumerate((("guerrero", tGue, 560), ("victoria", tVic, 1240))):
        v = asoma(t, tk - 0.3, tEscon - 0.1, periodo=1.6 + 0.3 * k) if t > tk - 0.3 else 0.0
        if t < tAtac - 0.2:
            v = entra(t, tk - 0.3) if t > tk - 0.3 else 0.0
        y = 760 - 330 * v
        cam(im, nom, x, y, 0.72, t, "VICENTE GUERRERO" if k == 0 else "GUADALUPE VICTORIA", seed=70 + k)
    tapa(im)
    if t > tGuerr - 0.3:
        letrero(im, "GUERRILLAS", 900, 230, 60, t, col=AMARILLO, seed=15040, esc=entra(t, tGuerr - 0.3))
    if tAtac - 0.2 < t < tEscon - 0.1:
        rotulo(im, "¡ATACAN!", 900, 400, 90, ROJO, t, seed=15045, esc=entra(t, tAtac - 0.2), rot=-0.06)
        exclama(im, 900, 520, 1.4, t, seed=15046)
    if t > tEscon - 0.2:
        rotulo(im, "¡Y SE ESCONDEN!", 900, 400, 80, VERDE, t, seed=15047, esc=entra(t, tEscon - 0.2), rot=0.05)
    return im


def chiste(t):
    im = cache("g_chi", lambda: papel("calido")).copy()
    forma(im, np.array([(0, 860), (W, 850), (W, H), (0, H)], np.float32), rgb("d9c08e"), 0, 15100, tinta=0)
    cab(im, t)
    letrero(im, "AGUANTARON...", 420, 220, 64, t, col=CREMA, txt=VERDE, seed=15105, esc=entra(t, tAguan - 0.3), rot=-0.04)
    # el chiste: la niña en su pupitre, rendida pero aguantando
    if t > tUlt - 0.6:
        e = entra(t, tUlt - 0.6, 0.45)
        cab_ = 0.25 * math.sin(t * 2.2)
        nina(im, 720, 600, 1.35 * e + 0.01, t, cara="apretados", boca="recta", brazos=(0.15, 0.15), seed=15110, rot=cab_ * 0.2)
        forma(im, rrect(720, 800, 520 * e + 1, 190 * e + 1, 10), rgb("8a5a34"), t, 15121, tinta=4)      # frente del pupitre
        forma(im, rrect(720, 700, 600 * e + 1, 50 * e + 1, 10), rgb("b98352"), t, 15120, tinta=4)       # tapa
        forma(im, rrect(560, 676, 150 * e + 1, 18 * e + 1, 4, -0.05), CREMA, t, 15123, tinta=2.5)       # cuaderno
        forma(im, rrect(860, 676, 120 * e + 1, 14 * e + 1, 4, 0.1), rgb("f2c14e"), t, 15124, tinta=2.5)  # lápiz
        gota(im, 830, 420 + 30 * ((t * 1.2) % 1), 0.9, t, seed=15125)
        # reloj que casi no avanza y calendario
        forma(im, elipse(1180, 380, 130 * e + 1, 130 * e + 1), CREMA, t, 15130, tinta=5)
        a = -math.pi / 2 + 0.25 * math.sin(t * 0.7)
        linea(im, [(1180, 380), (1180 + 95 * math.cos(a), 380 + 95 * math.sin(a))], 8, seed=15131, t=t)
        linea(im, [(1180, 380), (1180 + 60 * math.cos(t * 0.05), 380 + 60 * math.sin(t * 0.05))], 10, seed=15132, t=t)
        if t > tVac - 0.4:
            letrero(im, "ÚLTIMO DÍA ANTES DE VACACIONES", 820, 960, 50, t, col=AMARILLO, seed=15140, esc=entra(t, tVac - 0.4))
    return im


def dato(t):
    im = cache("g_dato", lambda: papel("calido")).copy()
    _manchas(im, rgb("a8d8b0"), 0, 1)
    cab(im, t)
    letrero(im, "DATO CHIDO", 420, 220, 66, t, col=AMARILLO, seed=15200, esc=entra(t, tDato - 0.3), rot=-0.05)
    e = entra(t, tVic2 - 0.3, 0.45)
    cam(im, "victoria", 620, 560, 1.15 * e, t, "GUADALUPE VICTORIA", seed=72)
    if t > tPrim - 0.3:
        eb = entra(t, tPrim - 0.3)
        # banda presidencial cruzada sobre el marco
        for k, col in enumerate((VERDE_B, BLANCO_B, ROJO_B)):
            d = (k - 1) * 36
            x1 = 460 + 300 * eb
            y1 = 590 + 150 * eb
            forma(im, np.array([(450, 582 + d), (450, 618 + d), (x1, y1 + 18 + d), (x1, y1 - 18 + d)], np.float32), col, t,
                  15210 + k, tinta=3)
        rotulo(im, "PRIMER", 1180, 410, 110, ROJO, t, seed=15220, esc=eb)
        letrero(im, "PRESIDENTE", 1180, 560, 70, t, col=CREMA, seed=15221, esc=entra(t, tPres - 0.2))
        letrero(im, "DE MÉXICO", 1180, 680, 62, t, col=CREMA, txt=VERDE, seed=15222, esc=entra(t, tPres + 0.2))
        chispas(im, 620, 560, 340, t, tPrim, seed=15230, col=AMARILLO)
    return im


TRAMOS = [(T_INI, titulo), (T_MONT, montes), (T_CHISTE, chiste), (T_DATO, dato)]


def cuadro_crudo(t):
    im = base(TRAMOS, t)
    papa(im, t, 1770, H + 30, alto=330)
    return im


def cuadro(t):
    return terminar(cuadro_crudo(t), t)
