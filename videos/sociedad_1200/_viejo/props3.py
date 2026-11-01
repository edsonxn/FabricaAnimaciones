# -*- coding: utf-8 -*-
"""Utilería noir 3: tablero de corcho con hilos · diana · teatro de sombras del rey Midas · apretón de manos con sombra de diablo ·
brújulas que no se alinean."""
import math

import numpy as np

import noir as N
from motor import H, W, clamp01, e_inout, e_out, smooth
from noir import gris
from props import rect, rot, foto
from toon import blob, elipse_, suave, tubo, eje_curvo


# ---------------------------------------------------------------------- tablero de corcho
def chincheta(h, x, y, sem=0):
    h.pieza(elipse_(x, y, 9, 9, n=12), 210, sem, w=2.5, luz=(0.3, -1), d=3, trama=0, rim=0.9)


def tarjeta(h, x, y, texto, t, t0, ang=0.0, sem=0, s=1.0):
    h.pieza(rot(rect(x - 150 * s, y - 50 * s, 300 * s, 100 * s), ang, np.array([x, y])), 225, sem, w=3, luz=(0.2, -1), d=5,
            trama=0, rim=0)
    N.texto_maquina(h, texto, x, y, 30 * s, t, t0, cps=30, tono=0.06, centro=True)
    chincheta(h, x, y - 40 * s, sem + 1)


def hilo(h, a, b, u=1.0, sem=0):
    """Hilo tenso entre dos chinchetas (se tiende con u 0..1)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    if u <= 0:
        return
    q = a + (b - a) * u
    med = (a + q) / 2 + (0, 14 * (1 - u))
    h.trazo(np.array([a, med, q]), 3.0, sem, color=gris(220), taper=(0.0, 0.0), jit=0.3, ruido=0.0)


# ---------------------------------------------------------------------- diana
def diana(h, cx, cy, r, sem=0):
    for k in range(6):
        rr = r * (1 - k / 6)
        h.pieza(elipse_(cx, cy, rr, rr, n=60), 30 if k % 2 == 0 else 220, sem + k, w=3, luz=(0.2, -1), d=4, trama=0, rim=0,
                sombra=0)
    h.trazo(np.array([[cx - r * 1.1, cy], [cx + r * 1.1, cy]]), 2, sem + 10, alfa=0.5)
    h.trazo(np.array([[cx, cy - r * 1.1], [cx, cy + r * 1.1]]), 2, sem + 11, alfa=0.5)


def dardo(h, x, y, ang, s=1.0, sem=0):
    def T(P):
        return rot(np.asarray(P, float) * s + (x, y), ang, np.array([x, y]))
    h.pieza(T([(0, -4), (180, -6), (180, 6), (0, 4)]), 200, sem, w=3 * s, luz=(0.2, -1), d=3, trama=0, rim=0.8)
    h.pieza(T([(0, -3), (-26, 0), (0, 3)]), 230, sem + 1, w=2 * s, luz=(0.2, -1), d=2, trama=0)
    h.pieza(T([(150, -6), (200, -40), (210, -4)]), 40, sem + 2, w=2 * s, luz=(0.2, -1), d=2, trama=0)
    h.pieza(T([(150, 6), (200, 40), (210, 4)]), 40, sem + 3, w=2 * s, luz=(0.2, -1), d=2, trama=0)


# ---------------------------------------------------------------------- teatro de sombras: el rey Midas
def rey(h, x, y, s=1.0, brazo=0.0, caido=0.0, sem=0):
    """Silueta del rey (corona, barba, manto) en perfil a la derecha. brazo 0..1 extiende la mano; caido 0..1 se desploma."""
    def T(P):
        P = np.asarray(P, float).reshape(-1, 2)
        P = rot(P, 0.9 * caido, np.array([-20.0, 0.0]))
        return P * s + (x, y + 120 * caido * s)
    cuerpo = [(-110, 0), (90, 0), (70, -160), (60, -300), (40, -380), (10, -400), (-40, -396), (-70, -360), (-90, -260), (-120, -120)]
    h.pieza(T(suave(cuerpo, 4)), 10, sem, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False)
    cab = [(-30, -400), (-36, -440), (-24, -470), (8, -478), (30, -462), (40, -440), (52, -426), (40, -420), (44, -404), (30, -380),
           (40, -350), (16, -330), (-6, -350), (-20, -380)]                                    # cabeza con barba puntiaguda
    h.pieza(T(suave(cab, 4)), 10, sem + 1, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False)
    if caido < 0.5:
        cor = [(-30, -466), (-36, -510), (-20, -486), (-8, -520), (4, -486), (18, -520), (26, -486), (40, -506), (34, -462)]
        h.pieza(T(cor), 10, sem + 2, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False)
    hx = 40 + 170 * brazo                                  # estira el brazo hacia adelante y abajo, hasta la mesa
    hy = -300 + 120 * brazo
    h.pieza(T(tubo(np.array([[30, -340], [hx * 0.6 + 12, (hy - 330) / 2 + 6], [hx, hy]]), 40, 26)), 10, sem + 3, w=0, luz=(0, -1), d=1,
            sombra=0, trama=0, rim=0, linea=False)
    h.pieza(T(blob(hx + 14, hy, 16, 12, n=8)), 10, sem + 4, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False)
    return T(np.array([[hx + 26, hy]]))[0]


def objeto_oro(h, tipo, x, y, s, oro, t, sem=0):
    """Rosa, pan o copa: silueta negra (teatro de sombras) que al tocarla se vuelve METAL brillante (blanco con destellos)."""
    if tipo == "rosa":
        P = [(-4, 0), (4, 0), (6, -120), (26, -150), (20, -184), (0, -196), (-22, -184), (-26, -150), (-6, -120)]
    elif tipo == "pan":
        P = [(-80, 0), (80, 0), (90, -30), (70, -64), (20, -78), (-40, -74), (-84, -50), (-94, -22)]
    else:                                               # copa
        P = [(-50, 0), (50, 0), (40, -12), (8, -20), (8, -70), (46, -100), (52, -170), (-52, -170), (-46, -100), (-8, -70), (-8, -20),
             (-40, -12)]
    P = np.array(P, float) * s + (x, y)
    if oro <= 0:
        h.pieza(P, 10, sem, w=0, luz=(0, -1), d=1, sombra=0, trama=0, rim=0, linea=False)
        return
    tono = int(10 + 215 * oro)
    h.pieza(P, tono, sem, w=4 * s * oro, luz=(0.4, -1), d=10 * s, sombra=0.7 * oro, trama=0.4 * oro, rim=oro, rim_tono=255)
    for k in range(3):                                   # destellos metálicos
        r = np.random.default_rng(sem + k)
        q = P[int(r.integers(len(P)))]
        v = oro * (0.5 + 0.5 * math.sin(t * 5 + k * 2))
        L = 26 * s * v
        h.emitir(np.array([[q[0] - L, q[1]], [q[0], q[1] - 3], [q[0] + L, q[1]], [q[0], q[1] + 3]]), 1.2 * v)
        h.emitir(np.array([[q[0], q[1] - L], [q[0] + 3, q[1]], [q[0], q[1] + L], [q[0] - 3, q[1]]]), 1.2 * v)


# ---------------------------------------------------------------------- brújula
def brujula(h, cx, cy, r, ang, sem=0, etiqueta="", t=0.0, t0=-99):
    h.pieza(elipse_(cx, cy, r, r, n=64), 70, sem, w=7, luz=(0.3, -1), d=r * 0.08, trama=0.4, rim=0.95, rim_tono=230)
    h.pieza(elipse_(cx, cy, r * 0.86, r * 0.86, n=64), 215, sem + 1, w=3, luz=(0.3, -1), d=4, trama=0, rim=0)
    for k in range(16):
        a = k * math.pi / 8
        l0 = 0.70 if k % 4 else 0.58
        h.trazo(np.array([[cx + math.cos(a) * r * l0, cy + math.sin(a) * r * l0], [cx + math.cos(a) * r * 0.8, cy + math.sin(a) * r * 0.8]]),
                3 if k % 4 else 5, sem + 10 + k, alfa=0.8)
    for k, c in enumerate("NESO"):
        a = -math.pi / 2 + k * math.pi / 2
        N.texto_maquina(h, c, cx + math.cos(a) * r * 0.45, cy + math.sin(a) * r * 0.45, r * 0.16, t, -99, cps=1e9, tono=0.1,
                        centro=True)
    a = ang - math.pi / 2
    n_ = np.array([math.cos(a), math.sin(a)])
    p_ = np.array([-n_[1], n_[0]])
    c = np.array([cx, cy])
    h.pieza(np.array([c + n_ * r * 0.72, c + p_ * r * 0.07, c - p_ * r * 0.07]), 12, sem + 40, w=3, luz=(0.3, -1), d=3, trama=0,
            rim=0.6)
    h.pieza(np.array([c - n_ * r * 0.72, c + p_ * r * 0.07, c - p_ * r * 0.07]), 170, sem + 41, w=3, luz=(0.3, -1), d=3, trama=0)
    h.pieza(elipse_(cx, cy, r * 0.06, r * 0.06, n=12), 200, sem + 42, w=3, luz=(0.3, -1), d=2, trama=0)
    if etiqueta:
        N.texto_maquina(h, etiqueta, cx, cy + r * 1.14, 36, t, t0, cps=30, tono=0.9, centro=True)
