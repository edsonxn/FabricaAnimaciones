# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA para polilla_foco: fotos REALES como pegatinas, imágenes vivas, rótulos y SFX.
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
    peg("Moths. Dozens of them", "polilla", "Banded tussock moth", x=.20, y=.58, tam=460),
    peg("Moths are the night shift of pollination", "polilla2", "Fall webworm moth", x=.80, y=.58, tam=480),
    dict(tipo="temblor", en="bumping into the glass", amp=14),
    # --- imágenes vivas (hojas revisadas el 22-oct-2026). Fuera: 003, 049 y 051 (la capa arrastra el halo, el laboratorio
    #     o el cono de luz).
    dict(tipo="vivo", beat="scene-007", anim="baile", capa=1),      # la vecina en pijama
    dict(tipo="vivo", beat="scene-010", anim="baile", capa=0),      # la polilla dice que no
    dict(tipo="vivo", beat="scene-012", anim="flota", capa=1),      # vuela bajo la luna
    dict(tipo="vivo", beat="scene-020", anim="flota", capa=0),      # vuela con el lomo al cielo
    dict(tipo="vivo", beat="scene-024", anim="baile", capa=0),      # ladeada junto al foco
    dict(tipo="vivo", beat="scene-026", anim="flota", capa=1),      # en órbita
    dict(tipo="vivo", beat="scene-029", anim="baile", capa=1),      # polilla, libélula y escarabajo
    dict(tipo="vivo", beat="scene-039", anim="baile", capa=1),      # el murciélago
    dict(tipo="vivo", beat="scene-043", anim="baile", capa=0),      # turno de noche
    dict(tipo="vivo", beat="scene-061", anim="baile", capa=0),      # corazón roto
]
ROTULOS = [
    dict(texto="2024", en="In twenty twenty-four, scientists finally filmed", tam=170, color="amarillo", x=.50, y=.14, dur=2.6),
    dict(texto="-62%", en="sixty-two percent fewer", tam=170, color="amarillo", x=.50, y=.14, dur=2.6),
    dict(texto="-13%", en="thirteen percent less fruit", tam=170, color="amarillo", x=.50, y=.14, dur=2.4),
]
SFX = {
    "clic_pol": ("Single crisp click of an old porch light switch with a soft electric hum starting", 2),
    "aleteo_pol": ("Soft papery fluttering of several moths circling a lamp, light taps on glass", 4),
    "murcielago_pol": ("Quick swoosh of a small bat swooping past with a tiny high squeak", 2),
}
PISTAS = [
    dict(sfx="clic_pol", en="You flip on the porch light", vol=.55),
    dict(sfx="aleteo_pol", en="Spinning around the bulb", vol=.4),
    dict(sfx="murcielago_pol", en="Bats swoop in", vol=.5),
]
