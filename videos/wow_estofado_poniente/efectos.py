# -*- coding: utf-8 -*-
"""Capa de efectos de «Estofado de Poniente» (SIN VOZ: anclas en segundos). Clip k = [10(k-1), 10k]; A 0-5 s, B 5-10 s.
Rótulos = PNG de pergamino (`python rotulos.py`). SFX de foley con ElevenLabs (`python fab.py <v> fx`)."""

ROT = [  # (ruta, de, a, y, ancho)
    ("rotulos/rot_0.png", 0.3, 3.0, .50, .56),      # WARCRAFT (1983) · Los Páramos de Poniente
    ("rotulos/rot_1.png", 7.9, 11.6, .78, .62),     # la misión, cuando el pergamino se desenrolla
    ("rotulos/rot_2.png", 69.0, 72.0, .50, .46),    # Continuará…
]

FX = [dict(tipo="imagen", ruta=r, de=de, a=a, x=.5, y=y, ancho=an, anim="fade", entra=.45, sale=.4) for r, de, a, y, an in ROT]
FX += [
    dict(tipo="abre", de=0.0, a=0.8),                               # entra de negro, como el arranque de un rollo
    dict(tipo="temblor", en=24.9, amp=26, dur=.5),                  # embestida del jabalí
    dict(tipo="temblor", en=34.8, amp=18, dur=.4),                  # la ola
    dict(tipo="temblor", en=54.8, amp=22, dur=.35),                 # portazo
    dict(tipo="oscurecer", de=68.6, a=72.0, k=.55, entra=.8),       # baja la luz bajo «Continuará…»
]

SFX = {
    "rafaga": ("Strong gust of wind sweeping through a dry wheat field, rustling stalks", 3),
    "pergamino": ("Old parchment scroll unrolling and dropping on a wooden porch floor", 2),
    "buitre": ("Raspy comic vulture squawk, cartoonish but real bird", 2),
    "aleteo": ("Large ragged bird wings flapping close past the microphone", 2),
    "jabali": ("Angry boar grunts and hooves pawing dry ground, then charging snort", 3),
    "impacto": ("Comic heavy body thud into dry grass with a puff of dust", 2),
    "murloc": ("Wet gurgling bubbly creature chorus, small fish-frog monsters burbling 'mrglglgl'", 3),
    "ola": ("Big ocean wave crashing over rocks, foam hissing as it drains", 3),
    "grillos": ("Quiet farm field at night, crickets and a light breeze, seamless loop", 10),
    "crujido": ("Slow creaking of rusty iron plates and old wooden joints, a scarecrow golem rising", 3),
    "pisadas": ("Heavy stomping metal footsteps chasing through crops, plants being slashed", 5),
    "portazo": ("Heavy wooden farmhouse door slammed shut", 1),
    "fuego": ("Crackling fireplace inside a cosy farmhouse, seamless loop", 10),
    "burbujas": ("Thick stew bubbling in an iron cauldron, seamless loop", 8),
    "glup": ("Comic wet squelchy blink and gloop of a clay creature rising from soup", 2),
}

PISTAS = [
    dict(sfx="rafaga", en=4.3, vol=.55),
    dict(sfx="pergamino", en=7.4, vol=.6),
    dict(sfx="buitre", en=12.3, vol=.5),
    dict(sfx="aleteo", en=14.4, vol=.55),
    dict(sfx="jabali", en=20.6, vol=.55),
    dict(sfx="impacto", en=24.7, vol=.6),
    dict(sfx="murloc", en=30.8, vol=.55),
    dict(sfx="ola", en=34.4, vol=.55),
    dict(sfx="grillos", de=40.0, a=50.0, vol=.35),
    dict(sfx="crujido", en=45.4, vol=.6),
    dict(sfx="pisadas", de=50.0, a=54.6, vol=.5),
    dict(sfx="portazo", en=54.7, vol=.7),
    dict(sfx="fuego", de=55.0, a=70.0, vol=.3),
    dict(sfx="burbujas", de=60.0, a=71.0, vol=.35),
    dict(sfx="glup", en=66.2, vol=.6),
]
