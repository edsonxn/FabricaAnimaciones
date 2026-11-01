# -*- coding: utf-8 -*-
"""Utilería original para «El caso de la Víbora Roja» (estilo noir en tinta y aguada).
Todas las piezas dibujadas en coordenadas del mundo con Noir.pieza, Noir.trazo, contraluz y tramado.

- lanza_dorniense · espadon_clegane · frasco_veneno · craneo_impacto · antorcha_pared · estrado_piedra
"""
import math
import numpy as np

import noir as N
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from toon import blob, elipse_, suave, tubo


def rot(P, ang, c):
    P = np.asarray(P, float)
    cs, sn = math.cos(ang), math.sin(ang)
    Q = P - c
    return np.stack([c[0] + Q[:, 0] * cs - Q[:, 1] * sn, c[1] + Q[:, 0] * sn + Q[:, 1] * cs], 1)


def lanza_dorniense(h, x, y, ang=0.0, largo=420, s=1.0, veneno=False, sem=0):
    """Lanza dorniense de fresno con punta en forma de hoja y borlas rojas/oscuras."""
    c = np.array([x, y], float)
    # Asta de madera
    asta = np.array([[-4 * s, -largo * 0.7], [4 * s, -largo * 0.7], [3 * s, largo * 0.3], [-3 * s, largo * 0.3]]) + c
    asta = rot(asta, ang, c)
    h.pieza(asta, 65, sem, w=3 * s, luz=(0, -1), d=4 * s, trama=0.25, rim=0.5)

    # Punta metálica (hoja estilizada)
    y_tip = -largo * 0.7
    punta = np.array([[0, y_tip - 80 * s], [14 * s, y_tip - 20 * s], [6 * s, y_tip],
                      [-6 * s, y_tip], [-14 * s, y_tip - 20 * s]]) + c
    punta = rot(punta, ang, c)
    tono_p = 35 if veneno else 180
    h.pieza(punta, tono_p, sem + 1, w=4 * s, luz=(0, -1), d=6 * s, trama=0.2, rim=0.9)

    # Nervio central
    linea = rot(np.array([[0, y_tip - 76 * s], [0, y_tip + 6 * s]]) + c, ang, c)
    h.trazo(linea, 2.5 * s, sem + 2, color=gris(20 if not veneno else 220))

    # Cintas / borla dorniense
    for k in (-1, 1):
        cinta = np.array([[k * 4 * s, y_tip + 4 * s], [k * 18 * s, y_tip + 28 * s], [k * 8 * s, y_tip + 55 * s]]) + c
        h.trazo(rot(cinta, ang, c), 2.5 * s, sem + 3 + k, color=gris(40), jit=0.4)

    if veneno:
        # Gota de veneno cayendo de la punta
        p_tip = rot(np.array([[0, y_tip - 82 * s]]) + c, ang, c)[0]
        h.pieza(np.array(elipse_(p_tip[0], p_tip[1] + 6 * s, 4 * s, 7 * s)), 15, sem + 6, w=2 * s)


def espadon_clegane(h, x, y, ang=0.0, largo=480, s=1.0, tono=90, sem=10):
    """Mandoble pesado de dos manos: hoja ancha con filo mellado y cruz de hierro macizo."""
    c = np.array([x, y], float)
    # Empuñadura y pomo
    emp = np.array([[-5 * s, 40 * s], [5 * s, 40 * s], [4 * s, 110 * s], [-4 * s, 110 * s]]) + c
    h.pieza(rot(emp, ang, c), 45, sem, w=3 * s, trama=0.3)
    pomo = rot(np.array(elipse_(x, y + 120 * s, 12 * s, 12 * s)), ang, c)
    h.pieza(pomo, 70, sem + 1, w=3 * s, rim=0.7)

    # Guardia / cruz
    cruz = np.array([[-55 * s, 26 * s], [55 * s, 26 * s], [52 * s, 42 * s], [-52 * s, 42 * s]]) + c
    h.pieza(rot(cruz, ang, c), 60, sem + 2, w=4 * s, luz=(0, -1), d=6 * s, rim=0.8)

    # Hoja ancha de acero
    y_tip = 26 * s - largo
    hoja = np.array([[0, y_tip - 30 * s], [18 * s, y_tip], [22 * s, 26 * s],
                     [-22 * s, 26 * s], [-18 * s, y_tip]]) + c
    h.pieza(rot(hoja, ang, c), tono, sem + 3, w=5 * s, luz=(-1, -1), d=10 * s, trama=0.35, rim=0.85)

    # Canaladura central
    canal = rot(np.array([[0, y_tip + 40 * s], [0, 20 * s]]) + c, ang, c)
    h.trazo(canal, 3.5 * s, sem + 4, color=gris(25), jit=0.2)


def frasco_veneno(h, x, y, s=1.0, tono_liquido=20, sem=20):
    """Frasco de boticario de mantícora: vidrio oscuro, tapón de corcho y gotas viscosas."""
    cuerpo = np.array([[-35, 60], [35, 60], [42, 20], [22, -20], [12, -40],
                       [-12, -40], [-22, -20], [-42, 20]], float) * s + (x, y)
    h.pieza(cuerpo, 85, sem, w=4 * s, luz=(1, -1), d=8 * s, trama=0.25, rim=0.9)

    # Nivel de veneno interior
    liq = np.array([[-30, 55], [30, 55], [36, 25], [-36, 25]], float) * s + (x, y)
    h.pieza(liq, tono_liquido, sem + 1, w=2 * s, trama=0.5)

    # Cuello y corcho
    corcho = np.array([[-10, -40], [10, -40], [8, -58], [-8, -58]], float) * s + (x, y)
    h.pieza(corcho, 60, sem + 2, w=3 * s, trama=0.3)

    # Sello de cera / símbolo
    h.pieza(np.array(elipse_(x, y + 20 * s, 12 * s, 12 * s)), 35, sem + 3, w=2 * s)
    h.trazo(np.array([[x - 6 * s, y + 20 * s], [x + 6 * s, y + 20 * s]]), 2 * s, sem + 4, color=gris(160))


def craneo_impacto(h, x, y, grietas=0.8, s=1.0, sem=30):
    """Cráneo humano en alto contraste con cuencas profundas y fracturas en tinta."""
    # Bóveda craneal
    boveda = np.array(elipse_(x, y - 20 * s, 68 * s, 64 * s, n=24))
    h.pieza(boveda, 170, sem, w=5 * s, luz=(0, -1), d=14 * s, trama=0.4, rim=0.9)

    # Pómulos y mandíbula
    mand = np.array([[-44 * s, 20 * s], [44 * s, 20 * s], [28 * s, 68 * s], [-28 * s, 68 * s]]) + (x, y)
    h.pieza(mand, 140, sem + 1, w=4 * s, luz=(0, -1), d=10 * s, trama=0.35)

    # Cuencas oculares oscuras
    for sx in (-24 * s, 24 * s):
        ojo = np.array(elipse_(x + sx, y, 16 * s, 20 * s, n=16))
        h.pieza(ojo, 15, sem + 2, w=3 * s)

    # Cavidad nasal
    nariz = np.array([[x, y + 14 * s], [x + 8 * s, y + 32 * s], [x - 8 * s, y + 32 * s]])
    h.pieza(nariz, 15, sem + 3, w=2.5 * s)

    # Dientes / maxilar
    for i in range(-3, 4):
        dx = i * 7 * s
        h.trazo(np.array([[x + dx, y + 54 * s], [x + dx, y + 66 * s]]), 2 * s, sem + 4 + i, color=gris(25))

    # Fisuras / fracturas en tinta
    if grietas > 0:
        f1 = np.array([[x - 30 * s, y - 70 * s], [x - 12 * s, y - 40 * s], [x - 22 * s, y - 10 * s], [x - 8 * s, y + 10 * s]])
        h.trazo(f1, 3.5 * s, sem + 10, color=gris(10), jit=0.5)
        f2 = np.array([[x + 10 * s, y - 65 * s], [x + 28 * s, y - 35 * s], [x + 20 * s, y - 5 * s]])
        h.trazo(f2, 2.8 * s, sem + 11, color=gris(10), jit=0.4)


def antorcha_pared(h, x, y, s=1.0, k_luz=1.0, sem=40):
    """Soporte de hierro medieval en muro con llama emisiva y luz parpadeante."""
    # Soporte de hierro forjado
    h.pieza(np.array([[x - 20 * s, y], [x + 6 * s, y], [x + 6 * s, y + 16 * s], [x - 20 * s, y + 16 * s]]), 30, sem, w=3 * s)
    brazo = np.array([[x, y + 16 * s], [x + 28 * s, y + 40 * s], [x + 32 * s, y + 70 * s]])
    h.trazo(brazo, 5 * s, sem + 1, color=gris(25))

    # Cazoleta
    caz = np.array([[x + 16 * s, y + 66 * s], [x + 48 * s, y + 66 * s], [x + 40 * s, y + 84 * s], [x + 24 * s, y + 84 * s]])
    h.pieza(caz, 35, sem + 2, w=3.5 * s, rim=0.6)

    # Llama
    flama = np.array([[x + 32 * s, y + 18 * s], [x + 46 * s, y + 42 * s], [x + 38 * s, y + 66 * s],
                      [x + 26 * s, y + 66 * s], [x + 18 * s, y + 42 * s]])
    h.pieza(flama, 240, sem + 3, w=2 * s)
    if k_luz > 0:
        h.emitir(flama, 1.4 * k_luz)
        h.luz_radial(x + 32 * s, y + 42 * s, 360 * s, (1.5, 1.35, 1.1), k=0.9 * k_luz)
