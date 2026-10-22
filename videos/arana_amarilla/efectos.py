# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA para arana_amarilla: fotos REALES como pegatinas e imágenes vivas.
Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera SFX + audio/fx.wav)    python fab.py <v> fx hoja
"""

import os
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))

# FOTO REAL como pegatina al presentar cada animal (regla del canal, 18-oct-2026; docs/manual_wild_next_door.md
# § «FOTO REAL»): ~1/3 del alto, en la esquina donde el dibujo deja aire, alternando lados. Créditos en pegatinas/CREDITOS.md.


def peg(en, slug, titulo, x=.20, y=.58, tam=520, dur=4.6):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_AQUI, "pegatinas", slug + ".jpg"), "REAL LIFE: " + titulo, tam),
                en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


CAMARA = {}
FUNDIDO = {}
VIVO_AUTO = 12          # parallax suave en todas las imágenes sin FX vivo

FX = [
    # --- fotos reales (6)
    peg("This is the yellow garden spider", "garden", "Yellow garden spider", x=.80),
    peg("The males? Tiny", "male", "Male garden spider", x=.20, tam=480),
    peg("Scientists call it a stabilimentum", "zigzag", "The zigzag", x=.52, y=.40, tam=460),   # entre la araña y el científico
    peg("She weaves a round, brown, papery egg sac", "eggsac", "Egg sac", x=.20),
    peg("The Joro spider, a newcomer from Asia", "joro", "Joro spider", x=.20),          # la Joro dibujada va a la derecha
    peg("Here is the quick check", "check", "Yellow garden spider", x=.20),

    # --- imágenes vivas (python fab.py arana_amarilla vivo; hojas previews/vivo_NN.jpg revisadas el 22-oct-2026).
    #     Fuera: 030, 037, 052, 059, 073, 076, 081 y 097 (la capa arrastra media telaraña o el arbusto).
    dict(tipo="vivo", beat="scene-017", anim="balanceo", capa=1),   # el hombre que pasa (la capa 0 lleva tela)
    dict(tipo="vivo", beat="scene-021", anim="balanceo", capa=1),   # la araña junto a la rueda
    dict(tipo="vivo", beat="scene-027", anim="balanceo"),
    dict(tipo="vivo", beat="scene-032", anim="balanceo"),
    dict(tipo="vivo", beat="scene-040", anim="baile"),              # araña frente al saltamontes
    dict(tipo="vivo", beat="scene-050", anim="baile"),              # abuela y niños
    dict(tipo="vivo", beat="scene-069", anim="flota", capa=1),      # el pájaro (la capa 0 es la tela)
    dict(tipo="vivo", beat="scene-078", anim="respira", capa=0),
    dict(tipo="vivo", beat="scene-083", anim="respira"),
    dict(tipo="vivo", beat="scene-086", anim="balanceo"),
    dict(tipo="vivo", beat="scene-091", anim="baile"),
    dict(tipo="vivo", beat="scene-099", anim="balanceo"),
    dict(tipo="vivo", beat="scene-103", anim="baile"),
]
ROTULOS = []
SFX = {}
PISTAS = []
