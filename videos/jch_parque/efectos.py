# -*- coding: utf-8 -*-
"""Capa de efectos del reel «Los jardines y el parque de Juchipila» (vertical 1080x1920). Formato y tipos: nucleo/secuencia_fx.py.
Receta de «Un segundo»: una imagen por frase, cámara dirigida, golpes en la palabra, color como emoción, rótulos solo de énfasis
(años y 2-3 palabras), un boom grave reutilizado en cada año y SFX/ambientes de ElevenLabs. Música: Lyria (aparte).
  python fab.py jch_parque fx --seco | fx | fx hoja
"""

CAMARA = {
    "scene-001": dict(a=(1.0, 0, .35), b=(1.22, 0, -.15)),     # el jardín frente al templo: se empuja hacia la iglesia
    "scene-002": dict(a=(1.22, 0, .2), b=(1.02, 0, 0)),        # se abre sobre el panteón
    "scene-003": dict(a=(1.25, -.3, .3), b=(1.02, 0, 0)),      # de los rosales a la torre
    "scene-004": dict(a=(1.0, 0, .4), b=(1.2, 0, -.2)),        # amanece sobre el cañón
    "scene-005": dict(a=(1.0, 0, 0), b=(1.25, 0, -.15)),       # los dos frailes: se empuja a las caras
    "scene-006": dict(a=(1.2, .3, -.3), b=(1.05, -.2, .3)),    # baja siguiendo la fila
    "scene-007": dict(a=(1.0, 0, .2), b=(1.25, 0, -.2)),       # la cruz y las primeras chozas
    "scene-008": dict(a=(1.2, .3, .1), b=(1.0, 0, 0)),
    "scene-009": dict(a=(1.0, 0, 0), b=(1.3, 0, 0)),           # el reloj de arena
    "scene-010": dict(a=(1.05, 0, -.3), b=(1.25, 0, .2)),
    "scene-011": dict(a=(1.25, -.3, 0), b=(1.05, .2, 0)),
    "scene-012": dict(a=(1.3, .3, .2), b=(1.05, 0, 0)),        # detalle de la banca
    "scene-013": dict(a=(1.3, 0, .1), b=(1.02, 0, 0)),         # el kiosco se revela
    "scene-014": dict(a=(1.05, 0, 0), b=(1.25, 0, .3)),
    "scene-015": dict(a=(1.25, 0, -.2), b=(1.02, 0, 0)),
    "scene-016": dict(a=(1.0, 0, 0), b=(1.25, .1, -.1)),
    "scene-017": dict(a=(1.0, 0, 0), b=(1.3, 0, .1)),          # la piedra
    "scene-018": dict(a=(1.25, .3, 0), b=(1.02, -.1, 0)),
    "scene-019": dict(a=(1.0, 0, -.3), b=(1.3, 0, .3)),        # vista aérea del parque
    "scene-020": dict(a=(1.0, 0, .4), b=(1.25, 0, -.4)),       # de la pista al teatro
    "scene-021": dict(a=(1.3, 0, .3), b=(1.02, 0, 0)),
    "scene-022": dict(a=(1.0, 0, 0), b=(1.3, .2, .1)),
    "scene-023": dict(a=(1.0, 0, 0), b=(1.2, -.1, -.05)),
}

FUNDIDO = {
    "scene-004": 0,        # corte seco a «mil quinientos cuarenta y dos»
    "scene-011": 0,        # corte seco al año 1943
    "scene-017": 0,        # corte seco a la primera piedra
}

FX = [
    dict(tipo="abre", en=0, dur=.6),
    dict(tipo="cierra", en=63.1, dur=.9),
    # gancho: el panteón se siente frío; los rosales, cálidos
    dict(tipo="desaturar", beat="scene-002", k=.55, entra=.5),
    dict(tipo="vineta", beat="scene-002", color="noche", fuerza=.5, entra=.4),
    dict(tipo="temblor", en="primer", amp=14, dur=.4),
    dict(tipo="tinte", beat="scene-003", color=(255, 235, 170), k=.25, entra=.5),
    # 1542
    dict(tipo="zoom", en="mil quinientos", cuanto=.12, entra=.2),
    dict(tipo="destello", en="mil quinientos", fuerza=.35, dur=.2),
    dict(tipo="tinte", beat="scene-004", color=(255, 225, 190), k=.2, entra=.4),
    # la fundación
    dict(tipo="vineta", beat="scene-006", color="noche", fuerza=.3, entra=.5),
    dict(tipo="destello", en="fundó", fuerza=.35, dur=.25),
    dict(tipo="tinte", beat="scene-007", color=(255, 235, 170), k=.25, entra=.4),
    # cuatro siglos: sepia y desaturado como foto antigua
    dict(tipo="desaturar", beat="scene-009", k=.4, entra=.3),
    dict(tipo="tinte", beat="scene-009", color=(255, 224, 176), k=.4, entra=.3),
    # 1943
    dict(tipo="zoom", en="mil novecientos", cuanto=.1, entra=.2),
    dict(tipo="destello", en="mil novecientos", fuerza=.3, dur=.2),
    # 1949 y la primera piedra
    dict(tipo="zoom", en="mil novecientos#2", cuanto=.1, entra=.2),
    dict(tipo="destello", en="mil novecientos#2", fuerza=.3, dur=.2),
    dict(tipo="temblor", en="primera piedra", amp=40, dur=.5),
    dict(tipo="destello", en="primera piedra", fuerza=.5, dur=.22),
    dict(tipo="vineta", beat="scene-017", color="noche", fuerza=.35, entra=.3),
    # hoy: más color
    dict(tipo="tinte", beat="scene-019", color=(255, 240, 200), k=.15, entra=.4),
    # la feria
    dict(tipo="latido", beat="scene-021", bpm=90, zoom=.02, fuerza=.12),
    dict(tipo="destello", en="Cada enero", fuerza=.25, dur=.3, color=(255, 220, 150)),
    # el vacío de datos: archivo y búsqueda
    dict(tipo="desaturar", beat="scene-022", k=.35, entra=.4),
    dict(tipo="vineta", beat="scene-022", color="noche", fuerza=.45, entra=.4),
    # cierre cálido
    dict(tipo="tinte", beat="scene-023", color=(255, 225, 175), k=.25, entra=.6),
]

ROTULOS = [
    dict(texto="JUCHIPILA, ZACATECAS", en=.8, a=3.2, tam=52, color="amarillo", caja="tinta", y=.87),
    dict(texto="Ilustraciones generadas con IA", en=1.0, a=3.4, tam=34, color="crema", caja="tinta", y=.92),
    dict(texto="PRIMER", en="primer", a="scene-002:fin", tam=130, color="crema", y=.13),
    dict(texto="PANTEÓN", en="primer", a="scene-002:fin", tam=130, color="crema", y=.20),
    dict(texto="1542", en="mil quinientos", a="scene-004:fin", tam=220, color="crema", y=.17),
    dict(texto="PLAZUELA", en="Plazuela", a="scene-008:fin", tam=120, color="crema", y=.13),
    dict(texto="SEGOVIA", en="Segovia#2", a="scene-008:fin", tam=120, color="crema", y=.20),
    dict(texto="1943", en="mil novecientos", a="scene-011:fin", tam=220, color="crema", y=.17),
    dict(texto="18 DE MAYO", en="dieciocho", a="scene-015:fin", tam=110, color="crema", y=.12),
    dict(texto="1949", en="mil novecientos#2", a="scene-015:fin", tam=220, color="crema", y=.19),
    dict(texto="PRIMERA", en="primera piedra", a="scene-017:fin", tam=130, color="crema", y=.13),
    dict(texto="PIEDRA", en="primera piedra", a="scene-017:fin", tam=130, color="crema", y=.20),
    dict(texto="2.7", en="dos punto siete", a="scene-019:fin", tam=240, color="crema", y=.15),
    dict(texto="HECTÁREAS", en="hectáreas", a="scene-019:fin", tam=110, color="crema", y=.24),
    dict(texto="¿LA SABES?", en="Si tú la sabes", a="scene-023:fin", tam=130, color="tinta", caja="amarillo", y=.14),
]

SFX = {
    "boom": ("Deep cinematic sub boom hit with a long reverb tail", 3),
    "campana": ("Single distant church bell toll in a quiet small town, natural long reverb, nothing else", 4),
    "piedra": ("Heavy stone block set down onto stone with a dull thud, followed by a short trowel scrape", 2),
    "siglos": ("Soft airy time-lapse whoosh rising with a faint clock ticking sweep, cinematic transition", 2.5),
    "plaza": ("Quiet small town plaza ambience, distant chatter, birds and soft footsteps on stone, a faint far guitar", 6),
    "feria": ("Distant village festival ambience, crowd murmur, a faraway brass band playing, one soft firework pop", 6),
    "hojas": ("Slow page turning of an old heavy book, dry paper rustle, quiet room", 3),
}

PISTAS = [
    dict(sfx="campana", en="templo", vol=.45),
    dict(sfx="boom", en="primer", vol=.5),
    dict(sfx="plaza", de="scene-003", a="scene-003:fin", vol=.28, entra=.6, sale=.8),
    dict(sfx="boom", en="mil quinientos", vol=.45),
    dict(sfx="siglos", en="Pasaron", vol=.5),
    dict(sfx="boom", en="mil novecientos", vol=.45),
    dict(sfx="boom", en="mil novecientos#2", vol=.45),
    dict(sfx="piedra", en="primera piedra", vol=.8),
    dict(sfx="feria", de="scene-021", a="scene-021:fin", vol=.3, entra=.6, sale=.8),
    dict(sfx="hojas", en="De cuándo", vol=.5),
]
