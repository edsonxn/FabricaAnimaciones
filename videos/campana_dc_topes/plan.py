# -*- coding: utf-8 -*-
"""Plan de tiempos de campana_dc_topes, compartido por la escena (Blender) y el post (rótulos y sonidos).
Todo sale de voz/tiempos.json (palabra por palabra), así los golpes caen justo en cada «tope». Solo librería estándar."""
import json
import os

AQUI = os.path.dirname(os.path.abspath(__file__))
FPS = 15
VOZ_OFF = 1.0
RX, RY = 270, 480
_T = json.load(open(os.path.join(AQUI, "voz", "tiempos.json"), encoding="utf-8"))
FRASES = [(a + VOZ_OFF, b + VOZ_OFF) for a, b in _T["frases"]]
PALABRAS = [(f, w, a + VOZ_OFF, b + VOZ_OFF) for f, w, a, b in _T["palabras"]]
VOZ_FIN = _T["total"] + VOZ_OFF
SEG = round(VOZ_FIN + 2.2, 2)

DX = -1.0                                           # Daniel parado en la calle, carril izquierdo
CARRIL = 1.15                                       # los carros, carril derecho
TOPES_Y = [-0.7, 2.5, 5.5, 8.5, 11.5, 14.5, 17.5, 20.5, 23.5]
GROSERIAS = {"cabrón", "pinche", "pinches", "mamen", "cagas", "verga", "putos"}


def W(frase, palabra, k=0):
    """Inicio (s, en el video) de la k-ésima `palabra` de la frase `frase` (1-8)."""
    c = [a for f, w, a, _ in PALABRAS if f == frase and w == palabra]
    return c[k]


def W1(frase, palabra, k=0):
    c = [b for f, w, _, b in PALABRAS if f == frase and w == palabra]
    return c[k]


# ---------------------------------------------------------------- momentos clave
T_CHOQUE_A = 0.86                                   # el vocho rojo pega en el tope junto a Daniel y sale volando
TOPES_L3 = [W(3, "tope", k) for k in range(5)]      # «tope · tope · tope, tope, tope»: el carro verde rebota
T_MOFLE = W(4, "mofle") - 0.05                      # pega en el último tope y se le cae el mofle
T_SUSP = W(4, "suspensión") + 0.15                  # se le zafa la llanta y se hunde
T_SUSTO = W(4, "cagas") - 0.1
T_VERGA5 = W(5, "verga")
T_PATADA = W(5, "putos") - 0.05
T_PIE = W(5, "topes")
T_TIRAR = W(7, "tirar")
T_PISOTON = W(7, "todos") + 0.05
T_VUELAN = [T_PISOTON + 0.12 + 0.16 * k for k in range(len(TOPES_Y))]
T_BAILE = W(8, "a")
T_SOY = W(8, "soy")
T_CIERRE = VOZ_FIN + 0.1

# carro verde (B): de dónde a dónde en cada tope de la frase 3, luego el del frente
_B = [(FRASES[2][0] - 1.6, 29.0)] + list(zip(TOPES_L3, [20.5, 14.5, 8.5, 5.5, 2.5])) + \
     [(T_MOFLE, -0.7), (T_SUSP, -2.6), (T_SUSP + 0.55, -3.4)]


def carro_b_y(t):
    if t <= _B[0][0]:
        return _B[0][1]
    for (t0, y0), (t1, y1) in zip(_B, _B[1:]):
        if t <= t1:
            return y0 + (y1 - y0) * (t - t0) / (t1 - t0)
    return _B[-1][1]


# golpes del carro verde: (t, altura) — la barra «SUSPENSIÓN» baja en cada uno
GOLPES_B = [(t, .55) for t in TOPES_L3] + [(T_MOFLE, .8)]
FPS_ = FPS
