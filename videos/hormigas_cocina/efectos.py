# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA para hormigas_cocina: fotos REALES como pegatinas, imágenes vivas, rótulos y SFX.
Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py."""

import os
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))


def peg(en, slug, titulo, x=.20, y=.58, tam=520, dur=4.6):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_AQUI, "pegatinas", slug + ".jpg"), "REAL LIFE: " + titulo, tam),
                en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


CAMARA = {}
FUNDIDO = {}
VIVO_AUTO = 12

FX = [
    peg("the odorous house ant, one of the most common", "hormiga", "Odorous house ant", x=.78, y=.55),
    peg("A perfect line of tiny ants", "hormiga_suelo", "Odorous house ant", x=.80, y=.60, tam=440, dur=3.6),
    dict(tipo="temblor", en="You squish them. All of them", amp=18),
    dict(tipo="temblor", en="blast the line with bug spray", amp=22),
    # --- imágenes vivas (hojas revisadas el 22-oct-2026). Fuera: 027, 031, 038, 043, 048, 060 y 067 (la capa arrastra
    #     el fregadero, la nube, el piso o media cocina).
    dict(tipo="vivo", beat="scene-005", anim="baile", capa=0),      # aplasta la fila
    dict(tipo="vivo", beat="scene-007", anim="baile", capa=0),      # manos en la cintura
    dict(tipo="vivo", beat="scene-009", anim="baile", capa=0),      # se rasca la cabeza
    dict(tipo="vivo", beat="scene-017", anim="baile", capa=0),      # el teléfono con la ruta
    dict(tipo="vivo", beat="scene-023", anim="balanceo"),           # el pastel de hormigas
    dict(tipo="vivo", beat="scene-065", anim="balanceo", capa=0),   # la señora y los repartidores
]
ROTULOS = [
    dict(texto="7-15%", en="they are only seven to fifteen percent", tam=170, color="amarillo", x=.50, y=.14, dur=2.8),
    dict(texto="x3", en="can quietly turn into three", tam=170, color="amarillo", x=.50, y=.14, dur=2.6),
]
SFX = {
    "aplasta_hor": ("Quick cartoon thumb squish on a kitchen counter, a soft squeak and a paper towel rub", 2),
    "ding_hor": ("Bright short food delivery app notification chime from a phone", 1),
    "spray_hor": ("Long hissing aerosol bug spray can blast, comic", 3),
}
PISTAS = [
    dict(sfx="aplasta_hor", en="Thumb, paper towel", vol=.55),
    dict(sfx="ding_hor", en="Think of it like a food delivery app", vol=.45),
    dict(sfx="spray_hor", en="blast the line with bug spray", vol=.5),
]
