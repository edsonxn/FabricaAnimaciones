# -*- coding: utf-8 -*-
"""Efectos de «Llamada de domingo» (generado por flow/_efectos_gen.py, sesión 2): ambiente continuo por lugar
para que los cortes entre clips no salten de sonido; el bolero y el canario donde el guion los nombra."""
CAMARA = {}
FUNDIDO = {}
FX = [dict(tipo="abre", en=0, dur=1.2)]
ROTULOS = []
SFX = {
    'taller': ('Room tone of an old watch repair workshop: dozens of antique wall clocks ticking softly out of sync, a faint street outside, no music, no voices', 22),
    'oficina': ('Quiet glass office high above a city at night: low air conditioning hum, distant muffled traffic far below, no music, no voices', 22),
    'depto': ('Modern apartment at night: soft steady rain against a window, a faint refrigerator hum, no music, no voices', 22),
    'plaza': ('Small Mexican neighborhood plaza on a Sunday afternoon: birds in big trees, distant children, a far street vendor bell, soft breeze, no music', 22),
    'cocina': ('Old small kitchen at night: a round wall clock ticking, a faint old refrigerator hum, crickets outside, no music, no voices', 22),
    'porche': ('Porch of an old house at dusk: crickets, a distant dog, a soft breeze in potted plants, a metal rocking chair creaking softly, no music', 20),
    'auto_lucia': ('Inside a parked small car in the evening, windows closed: muffled street traffic passing outside, no music, no voices', 20),
    'taxi': ('Back seat of a taxi driving in a city at night in the rain: engine hum, tires on wet asphalt, rain on the roof, no music', 20),
    'pasillo': ('Hospital corridor at night: fluorescent light hum, distant soft monitor beeps, far footsteps, no music, no voices', 22),
    'hospital': ('Hospital room at night: a slow steady heart monitor beep, an oxygen concentrator hiss, faint corridor hum, no music', 22),
    'carretera': ('Inside a modern car on a highway: steady smooth road noise, soft wind, no music, no voices', 20),
    'puerta': ('Quiet old Mexican street at dusk in December: distant firecrackers far away, a dog barking far, soft wind, no music', 20),
    'puerta_dia': ('Old Mexican street on a sunny Sunday morning: birds, a distant church bell, a car passing far away, no music', 20),
    'hospital_ext': ('City street outside a hospital at night: wet asphalt, a distant ambulance siren fading, light traffic, no music', 12),
    'radio_bolero': ('An old wooden AM radio playing a soft romantic Mexican bolero with a guitar trio, lo-fi warm radio sound with faint static, instrumental', 22),
    'radio_perilla': ('Turning the knob of an old wooden radio: static sweeping, then a faint bolero tuning in, lo-fi', 6),
    'canario': ('A single canary singing a long sweet melodic song indoors, close, no other sounds', 12),
}
PISTAS = [
    dict(sfx='puerta_dia', de=0.0, a=5.0, vol=.20),
    dict(sfx='taller', de=5.0, a=57.0, vol=.20),
    dict(sfx='oficina', de=57.0, a=65.0, vol=.20),
    dict(sfx='depto', de=172.0, a=190.0, vol=.20),
    dict(sfx='depto', de=200.0, a=208.0, vol=.20),
    dict(sfx='depto', de=213.0, a=221.0, vol=.20),
    dict(sfx='depto', de=228.0, a=238.0, vol=.20),
    dict(sfx='depto', de=254.0, a=259.0, vol=.20),
    dict(sfx='plaza', de=303.0, a=340.0, vol=.20),
    dict(sfx='puerta_dia', de=340.0, a=344.0, vol=.20),
    dict(sfx='taller', de=344.0, a=372.0, vol=.20),
    dict(sfx='auto_lucia', de=372.0, a=382.0, vol=.20),
    dict(sfx='oficina', de=382.0, a=392.0, vol=.20),
    dict(sfx='auto_lucia', de=399.0, a=409.0, vol=.20),
    dict(sfx='oficina', de=409.0, a=417.0, vol=.20),
    dict(sfx='cocina', de=417.0, a=462.0, vol=.20),
    dict(sfx='plaza', de=462.0, a=490.0, vol=.20),
    dict(sfx='porche', de=490.0, a=500.0, vol=.20),
    dict(sfx='taller', de=500.0, a=531.0, vol=.20),
    dict(sfx='pasillo', de=549.0, a=559.0, vol=.20),
    dict(sfx='taxi', de=559.0, a=569.0, vol=.20),
    dict(sfx='pasillo', de=569.0, a=577.0, vol=.20),
    dict(sfx='hospital_ext', de=587.0, a=591.0, vol=.20),
    dict(sfx='hospital', de=591.0, a=617.0, vol=.20),
    dict(sfx='hospital', de=627.0, a=633.0, vol=.20),
    dict(sfx='carretera', de=645.0, a=655.0, vol=.20),
    dict(sfx='puerta', de=655.0, a=688.0, vol=.20),
    dict(sfx='puerta', de=702.0, a=717.0, vol=.20),
    dict(sfx='puerta', de=733.0, a=759.0, vol=.20),
    dict(sfx='taller', de=759.0, a=775.0, vol=.20),
    dict(sfx="radio_perilla", en=51.8, vol=.35),          # Ramón gira la perilla
    dict(sfx="radio_bolero", de=767.5, a=775.0, vol=.45),   # Daniel prende el radio
    dict(sfx="canario", de=769.5, a=775.0, vol=.40),        # y el canario canta
]
