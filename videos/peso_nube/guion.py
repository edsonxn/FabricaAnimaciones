# -*- coding: utf-8 -*-
"""¿Cuánto pesa una nube? — Short vertical de ~1 min, boceto + guache (motor compartido nucleo/sh_*.py; ejemplo: videos/primer_foton/).
Fuentes: un cúmulo típico ≈ 500 toneladas de agua (M. LeMone, NCAR); gotas de nube ~0,02 mm que caen ~1 cm/s (velocidad terminal); corrientes ascendentes (térmicas) sostienen las gotas; un elefante africano ≈ 6 t.
"""

TITULO = '¿Cuánto pesa una nube?'
ARCHIVO = 'peso_nube_short'
ESTILO_VISUAL = "boceto"
FORMATO = "vertical"
DURACION = None
BPM = 110
GAP = 0.2
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.75, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.0)
ALIAS_QA = {"quinientos": "quinientas", "500": "quinientas"}
SUBTITULOS = False
TRANSICIONES = [("continua", 0.1)] * 10
MUSICA = {}
LYRIA = {'estilo': 'Playful, curious and wonder-filled score for a one-minute animated science short: warm glockenspiel, celesta, pizzicato strings, soft '
           'marimba, a light ticking pulse, tiny synth sparkles and a gentle bass; a cut-paper, hand-made feel. Keeps moving, with short stingers at '
           'scene changes. Melodies low and sparse so a narrator can speak over it. Instrumental only.',
 'escenas': {'gancho': ('Hook: a fluffy bouncy pluck with a surprised cartoon sting.', 6),
             'peso': ('Heavy comic tuba-like bass steps, playful marimba on top.', 5),
             'gotas': ('Tiny delicate raindrop glockenspiel, floating and light.', 4),
             'aire': ('Airy rising pad and gentle flute-like whistles, lifting feel.', 4),
             'lluvia': ('Marimba raindrops building to a soft rain patter and a release.', 6),
             'cierre': ('Cheerful floating resolution, a wink of celesta.', 5)}}
ESCENAS = [{'id': 'gancho', 'pre': 0.35, 'frases': ['Una nube pesa lo mismo que ochenta elefantes.', 'Y aun así, flota.']},
 {'id': 'peso',
  'frases': ['Una nube normal de verano pesa unas quinientas toneladas.', 'Medio millón de litros, suspendidos sobre tu cabeza.']},
 {'id': 'gotas',
  'frases': ['Pero ese agua está repartida en miles de millones de gotitas diminutas.',
             'Tan pequeñas que caen a menos de un centímetro por segundo.']},
 {'id': 'aire',
  'frases': ['Además, el aire caliente que sube desde el suelo las empuja hacia arriba.', 'Es como una corriente invisible que las mantiene arriba.']},
 {'id': 'lluvia',
  'frases': ['Pero cuando las gotas se juntan y se hacen más grandes, pesan demasiado.', 'Ya no hay corriente que las aguante, y entonces llueve.']},
 {'id': 'cierre', 'post': 2.5, 'frases': ['Así que cuando mires una nube, recuerda:', 'son ochenta elefantes flotando sobre tu cabeza.']}]
