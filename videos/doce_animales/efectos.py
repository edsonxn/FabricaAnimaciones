# -*- coding: utf-8 -*-
"""Capa de EFECTOS del motor SECUENCIA para doce_animales: fotos REALES como pegatinas, 3 clips de clímax a cuadro entero e
imágenes vivas. Receta: docs/estilo_secuencia_fx.md · formato y tipos: nucleo/secuencia_fx.py.
  python fab.py <v> fx --seco   (lista tiempos)    python fab.py <v> fx   (genera SFX + audio/fx.wav)    python fab.py <v> fx hoja
"""

import os
import mg_tes as T

_AQUI = os.path.dirname(os.path.abspath(__file__))

# FOTO REAL de cada animal como pegatina al presentarlo (regla del canal, 18-oct-2026; docs/manual_wild_next_door.md
# § «FOTO REAL»): ~1/3 del alto, en la esquina donde el dibujo deja aire, alternando lados. Créditos en pegatinas/CREDITOS.md.


def peg(en, slug, titulo, x=.20, y=.58, tam=520, dur=4.6):
    return dict(tipo="mg", fn=T.pegatina(os.path.join(_AQUI, "pegatinas", slug + ".jpg"), "REAL LIFE: " + titulo, tam),
                en=en, dur=dur, x=x, y=y, sale=.3, nombre="pegatina " + slug, ver=1.0)


def clip(nombre, de, a, recorte=0.0):
    """Clip de clímax de Flow a cuadro entero (su audio no entra en la mezcla: clip_linterna trae una risa)."""
    return dict(tipo="video", ruta=os.path.join(_AQUI, "medios", nombre + ".mp4"), de=de, a=a, recorte=recorte,
                entra=.25, sale=.25, nombre=nombre)


CAMARA = {}
FUNDIDO = {}
VIVO_AUTO = 12          # parallax suave en todas las imágenes sin FX vivo

FX = [
    # --- fotos reales (14)
    peg("The ladybug", "lady", "Ladybug", x=.20),
    peg("The millipede", "milli", "Millipede", x=.20, tam=500),        # sobre el 11: el milpiés va a la derecha
    peg("It is a hover fly", "hover", "Hover fly", x=.42),                # entre la lupa y el hombre
    peg("This is a ground beetle", "beetle", "Ground beetle", x=.80, y=.24, tam=540),   # arriba: abajo está su cabeza
    peg("It is a yellow garden spider", "garden", "Yellow garden spider", x=.20, tam=500),
    peg("The dragonfly", "dragon", "Dragonfly", x=.80),
    peg("The bumblebee", "bumble", "Bumblebee", x=.20),
    peg("The toad", "toad", "American toad", x=.20),                      # sobre el 5
    peg("this is most likely a garter snake", "snake", "Garter snake", x=.20),
    peg("The bat", "bat", "Little brown bat", x=.20, tam=500),            # sobre el 3
    peg("It is the western fence lizard", "lizard", "Western fence lizard", x=.20),
    peg("the Virginia opossum", "possum", "Virginia opossum", x=.80),
    peg("The spotted lanternfly", "lantern", "Spotted lanternfly", x=.20),
    peg("the blacklegged tick", "tick", "Blacklegged tick", x=.80, tam=500),

    # --- scene-002: la transición de Flow «dentro de la boca → cobertizo» pasa ~1 s por negro TOTAL (clip 2,95-3,95 s):
    #     el mismo clip encima, saltándose el negro, y un poco más lento para llenar el beat sin congelarse
    dict(clip("scene-002", ("scene-002", 2.808), "scene-002:fin"), desde=3.95, vel=.90, entra=0, sale=0),

    # --- clips de clímax a cuadro entero (19 puntos de Flow; clips_climax.json)
    clip("clip_desmayo", "scene-142", "scene-143:fin", recorte=.03),
    clip("clip_linterna", "scene-161", "scene-162:fin"),
    clip("clip_cierre", ("scene-193", -2.0), "scene-193:fin"),     # 6 s: «…shovel down. Go back inside…»

    # --- imágenes vivas (python fab.py doce_animales vivo; hojas previews/vivo_NN.jpg revisadas el 19-oct-2026)
    dict(tipo="vivo", beat="scene-016", anim="balanceo", capa=1),      # la mariquita sobre el dedo
    dict(tipo="vivo", beat="scene-019", anim="baile"),                 # 11 + milpiés
    dict(tipo="vivo", beat="scene-022", anim="respira", capa=0),       # milpiés y dedo (la capa 1 es un pedazo suelto)
    dict(tipo="vivo", beat="scene-025", anim="respira", capa=1),       # científico (la capa 0 es el suelo)
    dict(tipo="vivo", beat="scene-029", anim="flota", capa=1),         # mosca sírfida en el aire
    dict(tipo="vivo", beat="scene-032", anim="baile"),                 # lupa + hombre con matamoscas
    dict(tipo="vivo", beat="scene-037", anim="respira"),               # primer plano de la sírfida
    dict(tipo="vivo", beat="scene-064", anim="flota", capa=1),         # la libélula del sueño (no el durmiente)
    dict(tipo="vivo", beat="scene-070", anim="respira"),
    dict(tipo="vivo", beat="scene-083", anim="baile"),                 # 5 + sapo
    dict(tipo="vivo", beat="scene-088", anim="balanceo", capa=0),      # sapo (la mano va troceada)
    dict(tipo="vivo", beat="scene-090", anim="respira"),
    dict(tipo="vivo", beat="scene-092", anim="baile"),                 # perro y sapo frente a frente
    dict(tipo="vivo", beat="scene-117", anim="balanceo", capa=0),      # señal de prohibido (el murciélago arrastra plantas)
    dict(tipo="vivo", beat="scene-123", anim="baile"),                 # 2 + lagartija
    dict(tipo="vivo", beat="scene-135", anim="baile"),                 # 1 + zarigüeya
    dict(tipo="vivo", beat="scene-140", anim="baile"),
    dict(tipo="vivo", beat="scene-145", anim="respira"),
    dict(tipo="vivo", beat="scene-148", anim="baile"),                 # zarigüeya fría y mapache caliente
    dict(tipo="vivo", beat="scene-150", anim="baile"),
    dict(tipo="vivo", beat="scene-155", anim="respira", capa=0),       # zarigüeya (la capa 1 es una cabeza sin cuerpo)
    dict(tipo="vivo", beat="scene-173", anim="flota", amp=.6),
    dict(tipo="vivo", beat="scene-181", anim="respira"),
    # descartadas tras la hoja: 052 y 185 (telaraña/madriguera), 056 (lupa sin mango), 078 (díptico), 085 (cabeza sin
    # cuerpo), 094 108 121 126 130 166 (arrastran arbusto, rama, cama, tocón, piel o multitud), 096 099 103 (suelo), 132 (mapa)
]
ROTULOS = []
SFX = {}
PISTAS = []
