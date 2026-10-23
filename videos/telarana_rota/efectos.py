# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA para telarana_rota: fotos REALES como pegatinas, imágenes vivas, rótulos y SFX.
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
    peg("Many orb weaving spiders rebuild their web", "arana", "Furrow orb weaver", x=.80, y=.55),
    peg("Spiders build next to your porch light", "arana2", "Bridge orb weaver at a light", x=.78, y=.62, tam=460),
    dict(tipo="temblor", en="You grab the broom and wipe out", amp=20),
    # --- imágenes vivas (hojas revisadas el 22-oct-2026). Fuera: 003, 009, 015, 024, 030, 042, 045, 054 y 058 (la capa
    #     arrastra la puerta, la tela, el barandal, el banco o media escena).
    dict(tipo="vivo", beat="scene-028", anim="baile", capa=0),      # la araña y su carrete de seda
    dict(tipo="vivo", beat="scene-036", anim="baile", capa=0),      # el investigador con su tabla
    dict(tipo="vivo", beat="scene-047", anim="baile", capa=0),      # la araña y las pelusas
]
ROTULOS = [
    dict(texto="65 FT", en="sixty-five feet of silk", tam=170, color="amarillo", x=.50, y=.14, dur=2.6),
    dict(texto="~50%", en="about half of all the", tam=170, color="amarillo", x=.50, y=.14, dur=2.6),
]
SFX = {
    "escoba_tel": ("Fast broom swoosh through the air snapping thin threads, comic", 2),
    "cae_tel": ("Quick descending cartoon zip of a tiny spider dropping on a silk line", 1),
    "sorbe_tel": ("Small cartoon slurp of someone eating spaghetti noodles", 2),
}
PISTAS = [
    dict(sfx="escoba_tel", en="You grab the broom and wipe out", vol=.55),
    dict(sfx="cae_tel", en="The spider drops out of sight", vol=.5),
    dict(sfx="sorbe_tel", en="Spiders eat their old webs", vol=.5),
]
