# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA para arana_escusado: fotos REALES como pegatinas e imágenes vivas.
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
    # --- fotos reales (4)
    peg("A spider, sitting on the rim of the toilet", "casa", "Common house spider", x=.20),
    peg("the diving bell spider, lives its whole life underwater", "campana", "Diving bell spider", x=.80),
    peg("dunked marsh wolf spiders underwater", "marisma", "Marsh wolf spider", x=.20),
    peg("Many house spiders spend their entire lives indoors", "casa", "Common house spider", x=.80, tam=480),
]
FX += [
    # --- imágenes vivas (python fab.py arana_escusado vivo; hojas previews/vivo_NN.jpg revisadas el 22-oct-2026).
    #     Fuera: 002, 017, 048, 056, 061 y 063 (la capa arrastra la puerta, la tubería, la mesa o el escusado entero).
    dict(tipo="vivo", beat="scene-009", anim="baile"),              # el experto y su caballete
    dict(tipo="vivo", beat="scene-011", anim="baile"),              # reloj de arena, reloj y araña
    dict(tipo="vivo", beat="scene-013", anim="balanceo", capa=1),   # la araña con visor (la capa 0 es el remolino)
    dict(tipo="vivo", beat="scene-027", anim="flota"),              # la burbuja de la araña de campana
    dict(tipo="vivo", beat="scene-035", anim="baile"),
    dict(tipo="vivo", beat="scene-040", anim="respira"),
    dict(tipo="vivo", beat="scene-065", anim="respira"),
    dict(tipo="vivo", beat="scene-068", anim="balanceo", capa=2),   # la araña de la esquina
    dict(tipo="vivo", beat="scene-071", anim="flota", capa=0),      # la nube de pensamiento
    dict(tipo="temblor", en="and you flush", amp=22),
    dict(tipo="destello", en="they started twitching"),
]
ROTULOS = [
    dict(texto="40 HOURS", en="A few lasted around forty", tam=150, color="amarillo", y=.18, dur=2.6),
    dict(texto="1.6 GALLONS", en="a gallon and a half", tam=140, color="amarillo", x=.66, y=.16, dur=2.6),   # x=.66: sin pisar la cisterna
]
SFX = {
    "flush_esc": ("Modern toilet flushing, strong whoosh of water and a gurgling swirl draining away", 4),
    "tobogan_esc": ("Cartoon water slide rush, fast swirling water tunnel with a comic whoosh", 3),
    "goteo_esc": ("Echoing water drips and a slow stream in a dark brick sewer tunnel, ambient", 8),
    "burbujas_esc": ("Gentle cartoon underwater bubbles rising, soft bloops", 2),
    "despierta_esc": ("Tiny cartoon twitch with a soft magical sparkle chime", 2),
}
PISTAS = [
    dict(sfx="flush_esc", en="and you flush", vol=.7),
    dict(sfx="tobogan_esc", en="it is the biggest water slide on Earth", vol=.55),
    dict(sfx="burbujas_esc", en="breathing from its own private bubble", vol=.5),
    dict(sfx="goteo_esc", de="Now it is in the sewer", a="back from the dead|fin", vol=.35),
    dict(sfx="despierta_esc", en="they started twitching", vol=.55),
    dict(sfx="flush_esc", en="And to send it away", vol=.45),
]
