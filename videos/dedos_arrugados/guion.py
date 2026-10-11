# -*- coding: utf-8 -*-
"""¿Por qué se arrugan los dedos en el agua? — Short vertical de ~1 min, boceto + guache (motor compartido nucleo/sh_*.py; ejemplo: videos/primer_foton/).
Fuentes: arrugas por vasoconstricción regulada por el sistema nervioso simpático (Wilder-Smith 2004; Changizi 2011); mejor agarre de objetos mojados con dedos arrugados, sin diferencia en secos (Kareklas, Nettle y Smulders 2013, Biology Letters). Aparecen tras ~5 min en el agua.
"""

TITULO = '¿Por qué se arrugan los dedos en el agua?'
ARCHIVO = 'dedos_arrugados_short'
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
 'escenas': {'gancho': ('Hook: a squelchy curious pluck and a cheeky sting.', 6),
             'falso': ("Detective-style pizzicato, a little 'wrong answer' buzz then a reveal.", 5),
             'vasos': ('Quiet ticking clock and soft bubbling marimba, scientific.', 4),
             'neumatico': ('Bouncy rolling rhythm like a tire, bright bells.', 6),
             'prueba': ('Playful experiment montage, fast marimba and claps.', 6),
             'cierre': ('Warm clever resolution, a final wink with celesta.', 5)}}
ESCENAS = [{'id': 'gancho', 'pre': 0.35, 'frases': ['Tus dedos se arrugan en el agua, y no es porque se empapen.']},
 {'id': 'falso', 'frases': ['Si fuera por absorber agua, también se arrugaría el resto de tu piel.', 'Pero no: lo ordena tu sistema nervioso.']},
 {'id': 'vasos',
  'frases': ['Después de unos cinco minutos en el agua, hace que los vasos sanguíneos de tus dedos se contraigan, y la piel se pliega.']},
 {'id': 'neumatico', 'frases': ['Y las arrugas funcionan como las ranuras de un neumático.', 'Canalizan el agua y mejoran el agarre.']},
 {'id': 'prueba',
  'frases': ['En experimentos, la gente con dedos arrugados levantaba objetos mojados más rápido.',
             'Con objetos secos no había ninguna diferencia.']},
 {'id': 'cierre',
  'post': 2.5,
  'frases': ['Quizá es un truco heredado de nuestros ancestros, para agarrar piedras y peces resbalosos.',
             'Tus dedos tienen un sistema antideslizante integrado.']}]
