# -*- coding: utf-8 -*-
"""Objetos de los Qing al presente (boceto)."""
import math
from functools import lru_cache

import numpy as np

from obj_a import colocar
from obj_b import caballo
from obj_base import *  # noqa: F401,F403
from obj_base import _rotar

# ------------------------------------------------------------------ Qing
@lru_cache(maxsize=None)
def jinete_manchu(pose=0):
    h = caballo(pose)
    r = persona(AZUL_OSC, PIEL, "manchu", "enojo", (40, 140), pose, traje="corta", trenza=True, acc_d="espada")
    return Dib(list(h.ops) + colocar(list(r.ops), 6, -150, 0.56))


@lru_cache(maxsize=None)
def puerta_ciudad():
    """Puerta de la muralla de Pekín con torre."""
    ops = forma(rect(-150, -120, 150, 0, 4), (186, 170, 150), 5.6, peso=0.6, sp=10)
    ops += forma(pol((-150, -120), (-150, -130), (150, -130), (150, -120)), (170, 154, 136), 4, sp=6)
    ops += forma(rect(-120, -210, 120, -130, 4), ROJO_CH, 5, peso=0.5, sp=9)
    ops += forma(pol((-150, -200), (-96, -262), (96, -262), (150, -200)), (72, 100, 110), 5.4, peso=0.5, sp=8)
    ops += forma(rect(-40, -100, 40, 0, 36), NEGRO, 4.6, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def canon(f=0.0):
    ops = forma(elip(0, -62, 100, 34, -0.12, 1.0, 26), GRIS_OSC, 5.6, peso=0.6, sp=9)
    ops += forma(circ(-50, -28, 38, n=22), MADERA, 5, peso=0.5, sp=9) + [T(circ(-50, -28, 12, n=12), 3.6, peso=0.05)]
    ops += forma(rect(82, -86, 118, -40, 6), GRIS_OSC, 4.6, sp=7)
    return Dib(ops)


@lru_cache(maxsize=None)
def vapor(f=0):
    """Buque de vapor europeo con chimeneas y humo."""
    ops = forma(pol((-190, -80), (-150, -8), (150, -8), (210, -90)), (70, 80, 110), 5.8, peso=0.8, sp=10)
    ops += forma(rect(-140, -150, 120, -80, 6), CREMA, 5, peso=0.5, sp=9)
    ops += [R(rect(-110 + 44 * k, -130, -86 + 44 * k, -104, 4), CELESTE, peso=0.03, sp=4) for k in range(5)]
    ops += [T(rect(-110 + 44 * k, -130, -86 + 44 * k, -104, 4), 3.4, peso=0.03) for k in range(5)]
    for x in (-40, 50):
        ops += forma(rect(x - 20, -240, x + 20, -150, 4), (60, 60, 70), 5, peso=0.3, sp=8) + forma(rect(x - 22, -250, x + 22, -232, 3), ROJO_CH, 4, sp=6)
        ph = (f * 0.37 + x * 0.013) % 1.0
        ops += [T(circ(x + 12 * ph + 6, -270 - 70 * ph, 18 + 26 * ph, n=16), 4 * (1 - 0.4 * ph), peso=0.06)]
    ops += [T(ondas(-170, 190, -4, 5, 52, f * 0.9), 4.4, peso=0.12)]
    ops += [T(linea((-190, -80), (-230, -150)), 4.4, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def caja_te():
    ops = forma(rect(-70, -96, 70, 0, 4), (170, 110, 70), 5.4, peso=0.5, sp=9)
    ops += [T(linea((-70, -56), (70, -56)), 3.4, peso=0.04), T(linea((0, -96), (0, -56)), 3.4, peso=0.03)]
    ops += forma(circ(0, -28, 20, n=16), (104, 170, 100), 4, sp=5) + [T(linea((-8, -28), (8, -28)), 3.4, peso=0.02), T(linea((0, -38), (0, -18)), 3.4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def caja_opio():
    ops = forma(rect(-76, -100, 76, 0, 4), (90, 70, 80), 5.6, peso=0.5, sp=9)
    ops += [T(linea((-76, -60), (76, -60)), 3.4, peso=0.04)]
    # amapola
    ops += [T(linea((0, -100), (0, -150)), 4, peso=0.04)]
    for k in range(4):
        a = k * math.pi / 2 + 0.4
        ops += forma(elip(14 * math.cos(a), -168 + 14 * math.sin(a), 18, 12, a, 1.0, 12), ROJO_CH, 3.6, sp=4)
    ops += [R(circ(0, -168, 7, n=10), NEGRO, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def funcionario_opio(pose=0):
    return persona(AZUL_IMP, PIEL, "funcionario", "enojo", (150, 150), pose, traje="tunica", faja=ORO)


@lru_cache(maxsize=None)
def ingles(pose=0):
    return persona(ROJO_CH, PIEL_ROSA, "bombin", "serio", (30, 60), pose, traje="corta", bigote=True, acc_d="saco", faja=NEGRO)


@lru_cache(maxsize=None)
def isla_trozo(r=60):
    """Trozo de mapa que una mano arranca (Hong Kong)."""
    P = mano_poli(np.array([(-r, 0), (-r * 0.6, -r * 0.7), (0, -r), (r * 0.7, -r * 0.5), (r, 0), (r * 0.5, r * 0.6), (-r * 0.2, r * 0.8), (-r, 0)]), 3, seed=4)
    return Dib(forma(P, (96, 134, 184), 5.2, peso=0.4, sp=8))


@lru_cache(maxsize=None)
def nino_emperador(pose=0):
    d = persona(ORO, PIEL, None, "lloron" if pose else "asombro", (60, 60), pose, traje="tunica", faja=ROJO_CH, alto=0.6)
    corona = forma(rect(-70, -110, 70, -76, 6), NEGRO, 5, sp=7) + forma(rect(-40, -76, 40, -36, 6), NEGRO, 5, sp=7)
    corona += [R(elip(-60 + 24 * k, -28, 6, 9, n=8), ROJO_CH, peso=0.02, sp=3) for k in range(6)]
    return Dib(list(d.ops))


@lru_cache(maxsize=None)
def corona_grande():
    ops = forma(rect(-80, -60, 80, -28, 6), NEGRO, 5.4, peso=0.5, sp=8) + forma(rect(-46, -28, 46, 20, 6), NEGRO, 5.4, peso=0.5, sp=8)
    ops += [R(elip(-66 + 22 * k, 34, 6, 10, n=8), ROJO_CH, peso=0.02, sp=3) for k in range(7)] + [rayita(-66 + 22 * k, 10, -66 + 22 * k, 26, 2.6) for k in range(7)]
    return Dib(ops)


# ------------------------------------------------------------------ siglo XX
@lru_cache(maxsize=None)
def soldado_fusil(pose=0, ropa=(108, 122, 100), gorra=True):
    return persona(ropa, PIEL, "gorra" if gorra else "casco", "enojo", (10, 120 + 10 * (pose % 2)), pose, traje="corta", acc_d="lanza")


@lru_cache(maxsize=None)
def avion():
    ops = forma(elip(0, 0, 120, 26, 0, 1.0, 26), (196, 196, 204), 5.4, peso=0.5, sp=8)
    ops += forma(pol((-20, -2), (40, -2), (10, -90), (-30, -90)), GRIS_CL, 4.6, sp=7) + forma(pol((-20, 4), (40, 4), (10, 80), (-30, 80)), GRIS_CL, 4.6, sp=7)
    ops += forma(pol((-110, -4), (-80, -4), (-96, -50), (-120, -50)), GRIS_CL, 4.4, sp=6)
    ops += [R(circ(70, -6, 16, n=12), CELESTE, peso=0.02, sp=4), R(circ(0, 0, 10, n=10), ROJO_CH, peso=0.02, sp=4)]
    ops += [T(linea((124, -24), (124, 24)), 6, peso=0.03)]
    return Dib(ops)


@lru_cache(maxsize=None)
def lider(pose=0, cara="feliz"):
    return persona((100, 112, 110), PIEL, "gorra", cara, (20, 160 if pose % 2 == 0 else 130), pose, traje="corta", faja=None, cuello=(84, 96, 96))


@lru_cache(maxsize=None)
def lider_nuevo(pose=0):
    return persona(NEGRO, PIEL_OSC, "calvo", "guiño", (20, 60), pose, traje="corta", faja=None, cuello=BLANCO, alto=0.85)


@lru_cache(maxsize=None)
def tribuna():
    """Puerta roja con balcón (desde donde se proclama la república)."""
    ops = forma(rect(-220, -60, 220, 0, 3), (176, 72, 62), 5.6, peso=0.6, sp=9)
    ops += forma(rect(-180, -150, 180, -60, 3), ROJO_CH, 5, peso=0.5, sp=9)
    ops += forma(pol((-210, -150), (-140, -206), (140, -206), (210, -150)), ORO, 5.4, peso=0.5, sp=8)
    ops += [R(rect(-60 + 36 * k, -130, -36 + 36 * k, -84, 18), (120, 40, 40), peso=0.02, sp=4) for k in range(4)]
    ops += [T(rect(-60 + 36 * k, -130, -36 + 36 * k, -84, 18), 3.4, peso=0.03) for k in range(4)]
    return Dib(ops)


@lru_cache(maxsize=None)
def bandera():
    ops = [T(linea((0, 20), (0, -260)), 6, peso=0.2)] + forma(rect(0, -260, 200, -140, 3), ROJO_CH, 5, peso=0.5, sp=8)
    ops += [R(circ(40, -224, 10, n=10), AMARILLO, peso=0.02, sp=3)]
    for k in range(4):
        ops += [R(circ(84 + 22 * (k % 2), -240 + 20 * k, 4.5, n=8), AMARILLO, peso=0.02, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def horno_patio():
    ops = forma(curva([(-70, 0), (-66, -100), (-30, -150), (30, -150), (66, -100), (70, 0)], 6), (190, 120, 96), 5.6, peso=0.7, sp=9)
    ops += forma(rect(-22, -60, 22, 0, 12), NEGRO, 4, sp=5) + [R(pol((-14, 0), (0, -36), (14, 0)), NARANJA, peso=0.02, sp=4)]
    ops += forma(rect(-16, -200, 16, -150, 3), (170, 100, 80), 4.6, sp=7)
    return Dib(ops)


@lru_cache(maxsize=None)
def humo(f=0, n=4):
    ops = []
    for k in range(n):
        ph = (f * 0.3 + k / n) % 1.0
        ops.append(T(circ(10 * math.sin(ph * 6 + k) , -90 * ph, 14 + 34 * ph, n=16), 4.2 * (1 - 0.5 * ph), peso=0.05))
    return Dib(ops)


@lru_cache(maxsize=None)
def cuenco_vacio():
    ops = forma(arco_(0, -40, 60, 0, 180, 16).tolist() + [(-60, -40)], CREMA, 5.2, peso=0.5, sp=8)
    ops += [T(linea((-56, -40), (56, -40)), 4.4, peso=0.04), T(linea((-20, -4), (20, -4)), 4, peso=0.02)]
    ops += [T(linea((40, -10), (120, -70)), 5, peso=0.05), T(linea((52, -4), (130, -58)), 5, peso=0.05)]
    return Dib(ops)


@lru_cache(maxsize=None)
def trigo(marchito=0.0):
    ops = []
    for k in range(5):
        x = -60 + 30 * k
        h = 150 * (1 - 0.55 * marchito)
        curv = 26 * marchito * (1 if k % 2 else -1)
        ops += [T(curva([(x, 0), (x + curv * 0.3, -h * 0.5), (x + curv, -h)], 5), 4.4, peso=0.06)]
        for j in range(4):
            ops.append(R(elip(x + curv * (1 - 0.1 * j), -h + 14 * j * (1 - 0.4 * marchito), 6, 11, math.radians(20 * (1 if j % 2 else -1)), 1.0, 8),
                         (226, 190, 92) if marchito < 0.5 else (170, 140, 90), peso=0.02, sp=3))
    return Dib(ops)


@lru_cache(maxsize=None)
def gato(color="blanco", pose=0):
    col = {"blanco": (250, 248, 242), "negro": (64, 58, 66)}[color]
    tinta_ = NEGRO if color == "blanco" else (20, 20, 24)
    ops = forma(elip(0, -60, 76, 36, 0, 1.0, 26), col, 5.2, peso=0.5, sp=8)
    ops += forma(circ(84, -80, 30, n=22), col, 5, peso=0.3, sp=7)
    ops += forma(pol((66, -100), (72, -134), (90, -104)), col, 4, sp=4) + forma(pol((94, -102), (110, -130), (112, -92)), col, 4, sp=4)
    ops += [punto(90, -86, 7), punto(108, -86, 7), T(linea((98, -74), (98, -70)), 4, peso=0.02), T(linea((112, -76), (126, -80)), 3, peso=0.02), T(linea((112, -72), (126, -68)), 3, peso=0.02)]
    p = pose % 2
    for x, d in ((-50, 10 if p else -10), (-20, -10 if p else 10), (36, 10 if p else -10), (60, -10 if p else 10)):
        ops += forma(pol((x - 8, -36), (x + 8, -36), (x + d + 6, 0), (x + d - 8, 0)), col, 4, sp=5)
    ops += [T(curva([(-74, -70), (-110, -90), (-112, -140), (-90, -150)], 6), 7, peso=0.15)]
    return Dib(ops)


@lru_cache(maxsize=None)
def raton(pose=0):
    ops = forma(elip(0, -24, 40, 22, 0, 1.0, 20), GRIS, 4.6, peso=0.3, sp=6) + forma(elip(40, -28, 18, 14, 0.2, 1.0, 14), GRIS, 4.4, sp=5)
    ops += forma(circ(36, -44, 10, n=10), ROSA, 3.6, sp=4) + [punto(48, -32, 6), T(curva([(-38, -24), (-70, -36), (-84, -16), (-96, -40)], 5), 3.4, peso=0.1)]
    return Dib(ops)


@lru_cache(maxsize=None)
def vela(llama_=1.0):
    ops = forma(rect(-22, -110, 22, 0, 4), CREMA, 5, peso=0.4, sp=7) + [T(linea((0, -110), (0, -126)), 4, peso=0.02)]
    if llama_ > 0.05:
        s = llama_
        ops += forma(pol((-12 * s, -126), (0, -190 * s - 0), (12 * s, -126)), NARANJA, 4.4, sp=5)
    return Dib(ops)


@lru_cache(maxsize=None)
def rascacielos(h=300, w=90, c=(120, 150, 190)):
    ops = forma(rect(-w / 2, -h, w / 2, 0, 3), c, 5.4, peso=0.6, sp=9)
    filas = int(h / 36)
    for j in range(filas):
        for i in range(3):
            x = -w / 2 + 14 + i * (w - 28) / 2.0
            ops.append(R(rect(x - 6, -h + 16 + 36 * j, x + 6, -h + 28 + 36 * j, 1), (236, 226, 160) if (i + j) % 3 else (150, 190, 226), peso=0.01, sp=3))
    return Dib(ops)


@lru_cache(maxsize=None)
def fabrica():
    ops = forma(rect(-150, -100, 150, 0, 4), (196, 120, 100), 5.6, peso=0.6, sp=9)
    ops += forma(pol((-150, -100), (-150, -150), (-90, -100), (-90, -150), (-30, -100)), (176, 100, 84), 4.6, sp=7)
    for x in (70, 112):
        ops += forma(rect(x - 14, -230, x + 14, -100, 3), (160, 90, 76), 4.6, peso=0.3, sp=8)
    ops += [R(rect(-120 + 52 * k, -70, -92 + 52 * k, -40, 2), (236, 226, 160), peso=0.02, sp=4) for k in range(5)]
    return Dib(ops)


@lru_cache(maxsize=None)
def podio():
    ops = forma(rect(-180, -70, -60, 0, 3), (196, 196, 204), 5, peso=0.4, sp=8) + forma(rect(-60, -110, 60, 0, 3), ORO, 5.4, peso=0.5, sp=8) + forma(rect(60, -50, 180, 0, 3), (196, 140, 100), 5, peso=0.4, sp=8)
    ops += [T(linea((-130, -44), (-110, -44)), 4, peso=0.02)]
    return Dib(ops)


@lru_cache(maxsize=None)
def tren_bala():
    ops = forma(pol((-230, -20), (-230, -92), (-130, -130), (160, -130), (240, -80), (250, -20)), BLANCO, 5.6, peso=0.9, sp=10)
    ops += [R(rect(-200 + 56 * k, -112, -160 + 56 * k, -82, 6), CELESTE, peso=0.02, sp=4) for k in range(5)]
    ops += forma(pol((160, -130), (240, -80), (250, -20), (200, -20), (190, -60)), ROJO_CH, 4.4, sp=7)
    ops += [T(linea((-230, -46), (250, -46)), 4.4, peso=0.1)]
    ops += [T(linea((-200 - 26 * k, -90 + 20 * k), (-260 - 34 * k, -90 + 20 * k)), 4, peso=0.03) for k in range(3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def cronometro(aguja=0.0):
    ops = forma(circ(0, 0, 100, n=42), CREMA, 6.4, peso=0.8, sp=11) + forma(rect(-18, -128, 18, -100, 4), GRIS_CL, 5, sp=6) + [T(linea((58, -84), (84, -108)), 7, peso=0.03)]
    for i in range(12):
        a = i * math.pi / 6
        ops.append(rayita(84 * math.cos(a), 84 * math.sin(a), 94 * math.cos(a), 94 * math.sin(a), 4.2))
    ops += [T(_rotar(linea((0, 0), (0, -70)), aguja, 0, 0), 6, peso=0.02), R(circ(0, 0, 8, n=10), ROJO_CH, peso=0.01, sp=3)]
    return Dib(ops)


@lru_cache(maxsize=None)
def globo_dialogo():
    P = np.vstack([arco_(104, -64, 26, -90, 0, 6), arco_(104, -6, 26, 0, 90, 6), [(-20, 20), (-52, 68), (-58, 20)],
                   arco_(-104, -6, 26, 90, 180, 6), arco_(-104, -64, 26, 180, 270, 6)])
    return Dib(forma(P, BLANCO, 5.4, peso=0.6, sp=9))


@lru_cache(maxsize=None)
def boton_suscribir():
    ops = forma(rect(-190, -56, 190, 56, 26), ROJO_CH, 6, peso=0.7, sp=9)
    return Dib(ops)


@lru_cache(maxsize=None)
def campana():
    ops = forma(curva([(-50, 0), (-42, -80), (0, -116), (42, -80), (50, 0)], 6), ORO, 5.4, peso=0.5, sp=8) + [T(linea((-60, 0), (60, 0)), 6, peso=0.05)]
    ops += forma(circ(0, 20, 12, n=10), ORO_OSC, 4, sp=4) + [T(linea((0, -116), (0, -134)), 5, peso=0.02)]
    return Dib(ops)
