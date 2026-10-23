# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA para mariquitas_casa: fotos REALES como pegatinas, imágenes vivas, rótulos y SFX.
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
    # --- fotos reales (3)
    peg("That is an Asian lady beetle", "asiatica", "Asian lady beetle", x=.20),
    peg("A cousin of the ladybug", "nativa", "Native ladybug", x=.80, tam=460),
    peg("There, they pack together in big clusters", "grupo", "Overwintering cluster", x=.20, tam=500),
    dict(tipo="destello", en="Here is the first surprise"),
    # --- imágenes vivas (hojas previews/vivo_NN.jpg revisadas el 22-oct-2026). Fuera: 006, 020, 034, 051, 055 y 066
    #     (la capa arrastra el alféizar, el mapa entero, la pared, la cortina o la ventana).
    dict(tipo="vivo", beat="scene-010", anim="balanceo"),
    dict(tipo="vivo", beat="scene-012", anim="baile"),              # las primas en la fiesta
    dict(tipo="vivo", beat="scene-014", anim="flota", modelo="isnet-anime"),
    dict(tipo="vivo", beat="scene-041", anim="baile"),              # la mariquita que bosteza y su sol
    dict(tipo="vivo", beat="scene-053", anim="respira"),
    dict(tipo="vivo", beat="scene-058", anim="flota", capa=1, modelo="isnet-anime"),   # la mariquita que llega volando
    dict(tipo="vivo", beat="scene-068", anim="balanceo", capa=1),   # la del techo
    dict(tipo="vivo", beat="scene-071", anim="flota", capa=1),      # la del dedo
]
ROTULOS = [
    dict(texto="1988", en="in nineteen eighty-eight", tam=170, color="amarillo", x=.70, y=.16, dur=2.4),
]
SFX = {
    "enjambre_mar": ("Soft buzzing of many small beetles flying around a sunny window, gentle", 5),
    "bostezo_mar": ("Tiny cartoon bug yawn and stretch, cute and short", 2),
    "aspiradora_mar": ("Household vacuum cleaner switching on briefly, then off", 3),
}
PISTAS = [
    dict(sfx="enjambre_mar", en="Hundreds of little orange beetles", vol=.4),
    dict(sfx="bostezo_mar", en="some of them wake up too early", vol=.6),
    dict(sfx="aspiradora_mar", en="Vacuum them up instead", vol=.35),
]
