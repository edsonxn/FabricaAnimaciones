# -*- coding: utf-8 -*-
"""Hoja de objetos del kit: python _objetos.py  -> previews/objetos_N.png (tamaño completo, sin reducir)."""
import sys

import cv2
import numpy as np

import boceto as B
import kit as K
from motor import H, W


def hoja(nombre, items, fondo=(26, 28, 66)):
    h = B.Hoja()
    h.limpiar()
    f = np.empty((H, W, 3), np.float32)
    f[:] = np.array(fondo, np.float32) / 255
    h.fondo = f
    for it in items:
        d, x, y, s = it[:4]
        kw = it[4] if len(it) > 4 else {}
        K.poner(h, d, x, y, s, **kw)
    return h


def guardar(h, ruta, extra=None):
    img = np.clip(h.componer(), 0, 1)
    if extra:
        extra(img)
    cv2.imwrite(ruta, cv2.cvtColor((img * 255).astype(np.uint8), cv2.COLOR_RGB2BGR))


if __name__ == "__main__":
    # hoja 1: personajes
    it = [(K.foti("abiertos", "sonrisa"), 260, 260, 1.6), (K.cola(0.0), 260, 260, 1.6),
          (K.foti("feliz", "abierta"), 760, 260, 1.6), (K.foti("miedo", "grito"), 260, 640, 1.6),
          (K.foti("mareado", "o"), 760, 640, 1.6), (K.foti("enojado", "dientes"), 260, 1000, 1.6),
          (K.foti("guino", "lengua"), 760, 1000, 1.6), (K.foti("dormido", "triste"), 260, 1360, 1.6),
          (K.foti("estrellas", "abierta"), 760, 1360, 1.6),
          (K.electron(), 120, 1640, 1.3), (K.electron("miedo", "grito"), 260, 1640, 1.3), (K.proton(), 420, 1640, 1.3),
          (K.neutron(), 580, 1640, 1.3), (K.quark("rojo"), 700, 1640, 1.3), (K.quark("verde", "esfuerzo", "triste"), 780, 1640, 1.3),
          (K.quark("azul", "enojado", "zigzag"), 860, 1640, 1.3), (K.corazon(), 960, 1640, 1.3),
          (K.chispa(), 960, 1800, 1.0), (K.mancuerna(), 160, 1820, 1.0), (K.pesa_rusa(), 360, 1820, 1.0)]
    guardar(hoja("a", it), "previews/objetos_1.png")
    # hoja 2: props
    it2 = [(K.persona(), 220, 330, 1.0), (K.persona("miedo", "grito", "arriba"), 640, 330, 0.9),
           (K.espalda(), 270, 760, 0.8), (K.tele(), 760, 760, 1.0),
           (K.termometro(0.7), 140, 1270, 0.8), (K.olla(), 500, 1230, 1.0), (K.llama(0.0, 380, 1380, 1.0), 380, 1380, 1.0),
           (K.placa_interruptor(), 840, 1280, 0.9), (K.palanca(1.0), 840, 1280, 0.9),
           (K.tierra(), 150, 1700, 1.2), (K.hoja_calendario(), 340, 1700, 1.0), (K.palanca(-1.0), 560, 1640, 1.0)]
    h2 = hoja("b", it2)
    K.rotulo(h2, "380 000 AÑOS", 540, 1850, 100, rot=-0.04, tira=True)
    K.rotulo(h2, "¿CÓMO NACIÓ?", 540, 1560, 90, rot=0.03, color=(40, 120, 220))
    guardar(h2, "previews/objetos_2.png")
    print("listo")
