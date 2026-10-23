# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA para chinche_invierno: fotos REALES como pegatinas, imágenes vivas, rótulos y SFX.
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
    peg("This is the brown marmorated stink bug", "chinche", "Brown marmorated stink bug", x=.22),
    peg("called the samurai wasp", "avispa", "Samurai wasp", x=.80, tam=480),
    dict(tipo="temblor", en="bonks into the lamp", amp=20),
    # --- imágenes vivas (hojas revisadas el 22-oct-2026). Fuera: 002, 011, 014, 034, 041, 048, 060 y 062 (la capa arrastra
    #     la pantalla de la lámpara, la casa, el zócalo, la mesa o el sillón).
    dict(tipo="vivo", beat="scene-009", anim="balanceo", capa=1),   # la chinche junto a la taza
    dict(tipo="vivo", beat="scene-023", anim="baile", capa=0),      # el señor con el frasco
    dict(tipo="vivo", beat="scene-044", anim="respira"),
    dict(tipo="vivo", beat="scene-057", anim="balanceo", capa=1),   # el granjero triste
    dict(tipo="vivo", beat="scene-065", anim="balanceo", capa=1),   # el señor junto a la trampa
    dict(tipo="vivo", beat="scene-069", anim="balanceo", capa=1),   # la chinche confundida en la ventana
]
ROTULOS = [
    dict(texto="26,000+", en="His final count was more than twenty-six thousand", tam=170, color="amarillo", x=.30, y=.16, dur=2.8),
]
SFX = {
    "zumbido_chi": ("Clumsy loud buzzing of a single large beetle flying around a lamp, bumping", 4),
    "bonk_chi": ("Small cartoon bonk of a bug hitting a lampshade", 1),
    "burbujas_chi": ("Soapy water bubbles and a tiny plop of a bug falling into a jar", 2),
}
PISTAS = [
    dict(sfx="zumbido_chi", en="something starts buzzing around the shade", vol=.45),
    dict(sfx="bonk_chi", en="bonks into the lamp", vol=.6),
    dict(sfx="burbujas_chi", en="and nudge the bug in", vol=.5),
]
