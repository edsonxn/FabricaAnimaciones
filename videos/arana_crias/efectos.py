# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA para arana_crias: fotos REALES como pegatinas, imágenes vivas, rótulos y SFX.
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
    peg("This is a wolf spider", "mama", "Wolf spider mom with babies", x=.78, y=.55),
    peg("she carries her eggs", "saco", "Wolf spider with egg sac", x=.20, y=.58, tam=480),
    peg("Wolf spiders are outdoor hunters", "mama2", "Wolf spider mom outdoors", x=.80, y=.58, tam=440),
    # --- imágenes vivas (hojas revisadas el 22-oct-2026). Fuera: 003, 015, 017 (rehecha), 034, 053 y 059 (la capa
    #     arrastra el haz de luz, la explosión o el zócalo).
    dict(tipo="vivo", beat="scene-013", anim="respira", capa=0),    # la mamá con sus crías de noche
    dict(tipo="vivo", beat="scene-019", anim="baile", capa=0),      # corre con su bola de huevos
    dict(tipo="vivo", beat="scene-023", anim="baile", capa=0),      # sin carriola
    dict(tipo="vivo", beat="scene-028", anim="baile", capa=0),      # el señor con la bota
    dict(tipo="vivo", beat="scene-047", anim="baile", capa=1),      # el señor que la persigue
    dict(tipo="vivo", beat="scene-049", anim="baile", capa=1),      # la araña que se defiende
    dict(tipo="vivo", beat="scene-055", anim="baile", capa=0),      # libera a la familia
]
ROTULOS = [
    dict(texto="100+", en="a mom carrying a hundred kids", tam=170, color="amarillo", x=.50, y=.14, dur=2.6),
]
SFX = {
    "foco_cri": ("Fluorescent garage light flickering on with a buzz and a click", 2),
    "corren_cri": ("Fast tiny scurrying of many little legs scattering across a concrete floor, comic", 3),
    "cubeta_cri": ("Plastic bowl gently set down on concrete, then cardboard sliding underneath", 2),
}
PISTAS = [
    dict(sfx="foco_cri", en="You flip on the garage light", vol=.5),
    dict(sfx="corren_cri", en="Most of them jump off and run", vol=.45),
    dict(sfx="cubeta_cri", en="set it over her", vol=.5),
]
