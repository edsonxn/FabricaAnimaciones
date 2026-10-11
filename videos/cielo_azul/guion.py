# -*- coding: utf-8 -*-
"""¿Por qué el cielo es azul? — Short vertical de ~1 min, boceto + guache (motor compartido nucleo/sh_*.py; ejemplo: videos/primer_foton/).
Fuentes: dispersión de Rayleigh (∝ 1/λ⁴); el Sol emite menos violeta, la alta atmósfera lo absorbe y el ojo es menos sensible a él (NASA, Britannica); atardeceres rojos por mayor trayecto atmosférico; cielo de Marte: rojizo de día y azulado al atardecer (NASA/Mars rovers).
"""

TITULO = '¿Por qué el cielo es azul?'
ARCHIVO = 'cielo_azul_short'
ESTILO_VISUAL = "boceto"
FORMATO = "vertical"
DURACION = None
BPM = 110
GAP = 0.2
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.75, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.0)
ALIAS_QA = {}
SUBTITULOS = False
TRANSICIONES = [("continua", 0.1)] * 10
MUSICA = {}
LYRIA = {'estilo': 'Playful, curious and wonder-filled score for a one-minute animated science short: warm glockenspiel, celesta, pizzicato strings, soft '
           'marimba, a light ticking pulse, tiny synth sparkles and a gentle bass; a cut-paper, hand-made feel. Keeps moving, with short stingers at '
           'scene changes. Melodies low and sparse so a narrator can speak over it. Instrumental only.',
 'escenas': {'gancho': ('Hook: a sparkly mysterious rise and a surprised stinger.', 6),
             'blanca': ('Bright prism-like glockenspiel arpeggios.', 5),
             'dispersion': ('Bouncing pinball marimba, scattering sparkles.', 6),
             'violeta': ('A little courtroom-debate pizzicato rhythm, then a bright resolution chime.', 5),
             'atardecer': ('Warm sunset pad with soft celesta and a gentle slow beat.', 4),
             'marte': ('Dusty curious desert plucks, a playful twist.', 5),
             'cierre': ('Warm glowing final chord, a magical fade.', 5)}}
ESCENAS = [{'id': 'gancho', 'pre': 0.35, 'frases': ['El cielo no es azul.', 'En realidad, deberías verlo violeta.']},
 {'id': 'blanca', 'frases': ['La luz del Sol parece blanca, pero lleva todos los colores mezclados.']},
 {'id': 'dispersion',
  'frases': ['Al chocar con el aire, los colores de onda corta, como el azul y el violeta, se dispersan por todo el cielo.',
             'El rojo casi pasa de largo.']},
 {'id': 'violeta',
  'frases': ['El violeta se dispersa aún más, pero el Sol emite menos violeta, parte se absorbe arriba, y nuestros ojos lo ven peor.',
             'Por eso gana el azul.']},
 {'id': 'atardecer',
  'frases': ['Al atardecer, la luz atraviesa mucho más aire, y el azul se pierde por el camino.', 'Solo llegan el naranja y el rojo.']},
 {'id': 'marte', 'frases': ['En Marte pasa al revés: el cielo es rojizo de día y azul al atardecer.']},
 {'id': 'cierre', 'post': 2.5, 'frases': ['Cada atardecer rojo es el azul que se quedó atrás.']}]
