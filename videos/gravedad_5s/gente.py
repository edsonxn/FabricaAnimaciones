# -*- coding: utf-8 -*-
"""Personajes del paisaje de «gravedad 5 s»:
  - Persona quieta dentro de la casa en corte (X = -1250): solo flota a ras del piso (~28 u).
  - Protagonista en el parque (X = -590): da un salto en intro, camina y sube hasta la copa del árbol de 5 m en version_a,
    se tapa los oídos y deriva de lado en viento_mar, cae de golpe en caida_a, y sonríe en el cierre.
  - Kuri (mascota de Kuriox): acompaña a la protagonista en cada zona del paisaje.
  - Perro del parque y peatones de la avenida que flotan y caen al segundo 5.
"""
import math

import numpy as np

import plano as P
import kz_pers2d as K2
from motor import prog, clamp01, e_in, e_out, e_inout, circulo, elipse, rect_red
from mundo_comun import kf, pop, ventana, campana
from anclas import A, Z4
import ui_base as UB
import mundo_paisaje as MP

X_PROTA = -590.0
S_PERS = 28.0


def _base(X):
    return float(MP.suelo_h(X)) - 5.0


def perro_parque(lz, x, y, s=1.0, t=0.0, flotando=0.0):
    """Perrito estilo Kurzgesagt (origen en las patas) que mueve la cola y flota en cámara lenta."""
    col = (218, 152, 92)
    osc = (178, 116, 66)
    mancha = (246, 232, 210)
    with lz.grupo(x, y, s):
        # Cola que se mueve
        ang_c = 0.4 + 0.35 * math.sin(t * 7.5)
        with lz.grupo(-34, -36, 1.0, ang_c):
            lz.relleno(rect_red(-18, -5, 20, 9, 4), osc)
        # Patas traseras y delanteras
        p_ang = 0.25 * math.sin(t * 4.2) * flotando
        for px, c in ((-24, osc), (18, osc), (-16, col), (26, col)):
            with lz.grupo(px, -18, 1.0, p_ang if px > 0 else -p_ang):
                lz.relleno(rect_red(-5, 0, 10, 20, 4), c)
        # Cuerpo y pecho claro
        lz.relleno(rect_red(-36, -42, 68, 28, 14), col)
        lz.relleno(elipse(18, -28, 16, 12, 0, 20), mancha)
        # Cabeza, oreja y hocico
        with lz.grupo(30, -48, 1.0, 0.08 * math.sin(t * 2.5)):
            lz.relleno(circulo(0, 0, 18, 24), col)
            lz.relleno(rect_red(8, -6, 18, 13, 6), col)
            lz.relleno(circulo(24, -4, 4.5, 12), (40, 34, 58))
            lz.relleno(circulo(6, -5, 3.2, 12), (40, 34, 58))
            lz.relleno(elipse(-6, 2, 7, 13, 0.25, 18), osc)


def persona_casa(lz, t, S, est):
    """Persona quieta dentro de la casa (X_CASA): en Segundo 0 solo flota a ras del piso."""
    Xc = MP.X_CASA - 8.0
    if not S.vis(Xc - 150, Xc + 150, -20, 320):
        return
    base = float(MP.suelo_h(MP.X_CASA)) + 32.0
    alt = est.get("alt_casa", 0.0) * 28.0 + 4.0 * math.sin(t * 2.3) * est.get("alt_casa", 0.0)
    lean = 0.08 * math.sin(t * 1.6) * est.get("alt_casa", 0.0)
    emo = "sorpresa" if est.get("alt_casa", 0.0) > 0.2 else "neutro"
    brazos = "arriba" if est.get("alt_casa", 0.0) > 0.35 else "idle"
    with S.en(lz, Xc, base + alt, 1.0):
        K2.cuerpo(lz, 0, 0, S_PERS * 0.86, "hombre", t, piernas="idle", brazos=brazos, mirar=1,
                  vista="frente", emocion=emo, seed=3, lean=lean)


def protagonista(lz, t, S, est):
    der = est.get("deriva", 0.0) * 115.0
    camina_u = clamp01(prog(t, A.caminando - 0.2, A.impulso + 0.3))
    X = X_PROTA + 65.0 * camina_u + der
    if t >= Z4[0]:
        X = -475.0
    if not S.vis(X - 180, X + 180, -60, 560):
        return
    base = _base(X)
    salto_i = est.get("salto_intro", 0.0) * 78.0
    alt_p = est.get("alt_parque", 0.0) * 275.0 + (8.0 * math.sin(t * 2.0) if est.get("alt_parque", 0.0) > 0.1 else 0.0)
    H_pos = base + salto_i + alt_p

    piernas, brazos, emo = "idle", "idle", "neutro"
    lean = 0.0
    if t < A.imagina:
        emo = "alegre"
        if salto_i > 8.0:
            brazos = "arriba"
    elif t < A.caminando - 0.2:
        emo = "neutro"
    elif t < A.impulso + 0.15:
        piernas = "camina"
        brazos = "balanceo"
        emo = "alegre"
    elif t < A.dos_v - 0.2:
        emo = "sorpresa" if t < A.divertido else "alegre"
        brazos = "arriba" if alt_p > 60 else "balanceo"
        lean = -0.14 * clamp01(alt_p / 220.0) + 0.06 * math.sin(t * 1.8)
    elif t < A.cinco_ca - 0.1:
        if A.oidos - 0.2 < t < A.viento + 0.4:
            emo = "dolor"
            brazos = "defensa"
        else:
            emo = "sorpresa"
            brazos = "arriba"
        lean = 0.22 * est.get("viento", 0.0) + 0.08 * math.sin(t * 3.0)
    elif t < A.humanidad - 0.2:
        emo = "dolor" if est.get("impacto_a", 0.0) > 0.2 else "sorpresa"
        brazos = "defensa"
        lean = 0.12 * math.sin(t * 12.0) * est.get("impacto_a", 0.0)
    elif t < Z4[0]:
        emo = "alegre"
        brazos = "pecho"
    else:
        emo = "alegre"
        brazos = "saluda" if t > A.unidos else "idle"

    with S.en(lz, X, H_pos, 1.0):
        K2.cuerpo(lz, 0, 0, S_PERS, "mujer", t, piernas=piernas, brazos=brazos, mirar=1,
                  vista="frente" if (t < A.caminando or t >= Z4[0]) else "perfil",
                  emocion=emo, seed=1, lean=lean)


# Claves de posición X de Kuri en el paisaje
_KURI_X = [
    (0.0, -490.0),
    (A.casa - 0.4, -1020.0),
    (A.caminando - 0.3, -480.0),
    (A.dos_v - 0.2, -360.0),
    (A.coches_v - 0.3, 260.0),
    (A.cinco_ca - 0.2, 320.0),
    (Z4[0], -330.0),
    (A.fin, -330.0),
]


def kuri_paisaje(lz, t, S, est):
    X0 = float(kf(t, _KURI_X))
    der = est.get("deriva", 0.0) * 95.0
    X = X0 + der
    if not S.vis(X - 140, X + 140, -50, 520):
        return
    base = _base(X)
    salto_i = est.get("salto_intro", 0.0) * 92.0
    alt_k = est.get("alt_parque", 0.0) * 245.0 + (12.0 * math.cos(t * 2.4) if est.get("alt_parque", 0.0) > 0.05 else 0.0)
    H_pos = base + salto_i + alt_k
    rot_k = 0.25 * math.sin(t * 1.9) * est.get("alt_parque", 0.0) + 0.22 * est.get("viento", 0.0)

    mirar = (-0.5, -0.2)
    aleteo = 0.0
    tirit = 0.0
    feliz = 0.0
    boca = 0.0
    if salto_i > 5.0:
        feliz = 1.0
        aleteo = 0.8
    elif A.cero_a < t < A.dos_v:
        feliz = 0.8 if t > A.divertido - 0.3 else 0.0
        boca = 0.7 if t < A.divertido - 0.3 else 0.0
        aleteo = 0.6
        mirar = (-0.6, -0.4)
    elif A.dos_v <= t < A.cinco_ca:
        aleteo = 1.0
        tirit = 0.55
        boca = 1.0
        mirar = (0.7, -0.3)
    elif A.cinco_ca <= t < A.sobreviviria:
        tirit = 0.4 * est.get("impacto_a", 0.0)
        mirar = (-0.4, 0.2)
    else:
        feliz = 1.0
        aleteo = 0.5 * campana(t, A.tiron, A.fin)

    with S.en(lz, X, H_pos, 0.96, rot_k):
        P.kuri(lz, 0, 0, 1.0, t, mirar=mirar, aleteo=aleteo, tiritar=tirit, feliz=feliz, boca=boca)


def gente(lz, t, S, est):
    persona_casa(lz, t, S, est)

    # Perrito del parque que sube en cámara lenta junto con la bici y la taza
    alt_c = est.get("alt_cosas", 0.0)
    der = est.get("deriva", 0.0)
    xp = -335.0 + der * 105.0
    hp = _base(xp) + alt_c * 190.0 + 9.0 * math.sin(t * 2.3) * alt_c
    rot_p = 0.18 * math.sin(t * 1.7) * alt_c
    if S.vis(xp - 100, xp + 100, -20, 420):
        with S.en(lz, xp, hp, 0.92, rot_p):
            perro_parque(lz, 0, 0, 1.0, t, flotando=alt_c)

    # Peatones en la avenida urbana (flotan y caen en caida_a)
    imp = est.get("impacto_a", 0.0)
    ok = ventana(t, A.humanidad - 0.2, A.total - 0.3, 0.2, 0.4) if not est.get("normal") else 0.0
    for idx, (x0, tipo, f_h) in enumerate(((165.0, "hombre", 0.85), (610.0, "mujer", 1.05))):
        xe = x0 + der * 125.0 * (0.9 + 0.15 * idx)
        he = _base(x0) + est.get("alt_parque", 0.0) * 230.0 * f_h
        if not S.vis(xe - 120, xe + 120, -40, 480):
            continue
        lean_e = 0.22 * math.sin(t * 1.8 + idx) * clamp01(est.get("alt_parque", 0.0))
        emo_e = "alegre" if ok > 0.3 else ("sorpresa" if he > 25 or imp > 0.2 else "neutro")
        brazos_e = "arriba" if he > 30 else ("saluda" if ok > 0.3 else "idle")
        with S.en(lz, xe, he, 0.95):
            K2.cuerpo(lz, 0, 0, S_PERS * 0.94, K2.variar(tipo, 10 + idx), t,
                      piernas="idle", brazos=brazos_e, mirar=1 if idx == 0 else -1,
                      vista="perfil", emocion=emo_e, seed=10 + idx, lean=lean_e)
        if ok > 0.02:
            x_, y_ = S.pt(xe, he + 250)
            kk = pop(t, A.sobreviviria + 0.1 * idx) * S.k * 1.15
            with lz.capa(2):
                lz.relleno(circulo(x_, y_, 32 * kk, 24), (72, 198, 124), alfa=ok)
                UB.check(lz, x_, y_ + 2 * kk, 15 * kk, (255, 255, 255), ok)

    protagonista(lz, t, S, est)
    kuri_paisaje(lz, t, S, est)
