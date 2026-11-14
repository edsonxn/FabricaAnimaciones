# -*- coding: utf-8 -*-
"""Escenas del video. Por defecto TODAS usan las escenas genéricas (IntroGenerica, ItemGenerico,
EscenaLibre, OutroGenerico) según su posición y campos en guion.py: el video sale completo sin
programar nada. Para una coreografía a medida, crea una clase y regístrala en PROPIAS.

Ejemplo de escena a medida (heredar de Item: título -> antes(fase A) -> hoy(fase B)):

class Uno(Item):
    PAL = "acido"
    def escena(self):                       # anclas y efectos de sonido
        self.t_x = self.w("apagones")       # tiempo en que se dice la palabra
        self.ev(self.t_x, "pop", 0.6)
    def antes(self, lz, t):                 # fase A
        dibujar_icono(lz, "ojo", 960, 560, pop(t, self.B + 0.1), t)
    def hoy(self, lz, t):                   # fase B
        D.cerebro(lz, 960, 540, 1.3 * pop(t, self.t_x), t, brillo=0.5)

Ejemplos completos y más elaborados: videos/40mil_anos/escenas.py
"""
from escena_base import *  # noqa: F401,F403

PROPIAS = {
    # "uno": Uno,
}

CLASES = clases_automaticas(PROPIAS)
