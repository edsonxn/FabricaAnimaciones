# -*- coding: utf-8 -*-
"""Capa de EFECTOS de «La heredera del rancho» cap. 3 (SIN voz: anclas en segundos; los clips traen su propio diálogo).
Beats: s1 0-10 reprise · ESCENA 1 capilla s2-s6 10-60 · s7 60-68 amanecer · ESCENA 2 cocina s8-s13 68-124 ·
s14 124-132 Valeria en el balcón · ESCENA 3 capilla s15-s19 132-182 + «Continuará…» (182-186, el clip 19 congelado).
Receta «novela, no tráiler»: AMBIENTE DE CUARTO continuo por escena (pega los cortes entre clips), pocos golpes, uno al final.
  python fab.py heredera_cap3 fx --seco   ·   python fab.py heredera_cap3 fx   ·   python fab.py heredera_cap3 fx hoja
"""

CAMARA = {}
FUNDIDO = {}
FX = [
    dict(tipo="abre", en=0, dur=.6),
    dict(tipo="desaturar", de=0.0, a=10.0, k=.45, sale=.4),       # «En el capítulo anterior…»: recuerdo, menos color
    dict(tipo="oscurecer", de=181.6, a=186.0, k=.6),             # fondo para el «Continuará…»
]
ROTULOS = [
    dict(texto="En el capítulo anterior…", en=0.4, a=3.4, tam=58, color="crema", caja="tinta", y=.08),
    dict(texto="LA HEREDERA", en=10.2, a=13.2, tam=112, color="crema", caja="tinta", y=.08),
    dict(texto="DEL RANCHO", en=10.2, a=13.2, tam=112, color="crema", caja="tinta", y=.15),
    dict(texto="Capítulo 3", en=10.5, a=13.2, tam=66, color="dorado", y=.22),
    dict(texto="Continuará…", en=182.0, a=186.0, tam=92, color="crema", y=.38),
    dict(texto="Capítulo 4:", en=182.4, a=186.0, tam=76, color="dorado", y=.46),
    dict(texto="¿Dónde está Carmen?", en=182.6, a=186.0, tam=76, color="crema", y=.53),
]
PALETA = {"dorado": (232, 178, 64)}
# Descripciones nuevas (ni las de los caps. 1-2 ni las de novela_altar): la página no debe oír los mismos efectos.
SFX = {
    "capilla_noche": ("Quiet night room tone inside a small old stone chapel: faint crickets outside, a soft cold draft through "
                      "an open wooden door, the gentle hiss of a kerosene lantern flame, no music, no voices", 22),
    "amanecer": ("Countryside dawn on a Mexican ranch: many small birds waking up, a rooster crowing far away, soft breeze over "
                 "the fields, distant cow, no music", 10),
    "cocina": ("Old ranch kitchen room tone at dawn: a wood fire crackling inside a stove, a clay pot simmering softly, birds "
               "outside the window, no music, no voices", 22),
    "patio_noche": ("Night courtyard of an old Mexican hacienda: crickets, two dogs barking far away, wind moving a cypress "
                    "tree, no music", 10),
    "latido": ("A slow deep cinematic heartbeat, low and tense, steady thumps, no music", 10),
    "golpe_final": ("Telenovela cliffhanger hit: a sudden orchestral string stab with a deep taiko boom and a long dark "
                    "reverb tail", 5),
}
PISTAS = [
    dict(sfx="capilla_noche", de=0.0, a=60.0, vol=.22),          # reprise + escena 1: la misma capilla
    dict(sfx="amanecer", de=59.5, a=68.5, vol=.40),               # cortinilla (el clip 7 va mudo: su voz en off era inventada)
    dict(sfx="cocina", de=68.0, a=124.0, vol=.20),                # escena 2
    dict(sfx="patio_noche", de=123.6, a=132.4, vol=.32),          # Valeria en el balcón
    dict(sfx="capilla_noche", de=132.0, a=186.0, vol=.22),        # escena 3
    dict(sfx="latido", de=171.5, a=181.8, vol=.30),               # Chuy levanta la escopeta
    dict(sfx="golpe_final", en=181.6, vol=.70),                   # cliffhanger
]
