# -*- coding: utf-8 -*-
"""¿Qué pasaría si cayeras en arenas movedizas? — Short vertical en ACUARELA PINTADA A MANO POR CÓDIGO (kit acuarela.py).
Un solo plano secuencia: `Mundo` dibuja el cuadro entero en función del tiempo global.
    plano_a.py   0-28 s     orilla, ¡se hunde!, los sesenta, película sepia, ¡MENTIRA!, balanza ×2, corte: cintura y flotas
    plano_b.py   28-48,3 s  la trampa (granos que aprietan, cemento), Kuri tira = un coche, horas y la marea que sube
    plano_c.py   48,3-73 s  no tires, échate atrás (alberca), piernas en círculos con agua, la arena suelta, no entres en pánico"""
import plano_a as A
from escena_base import Escena, TL

try:
    import plano_b as B
except ImportError:                      # mientras se escribe
    B = None
try:
    import plano_c as C
except ImportError:
    C = None


def cuadro(t):
    if C is not None and t >= C.T_INI:
        return C.cuadro(t)
    if B is not None and t >= B.T_INI:
        return B.cuadro(t)
    return A.cuadro(t)


class Mundo(Escena):
    def render(self, lz, t):
        return cuadro(t)


CLASES = {e["id"]: Mundo for e in TL["escenas"]}
