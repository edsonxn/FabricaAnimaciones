# -*- coding: utf-8 -*-
"""La Luna se está yendo — Short vertical de ~1 min, boceto + guache (motor compartido nucleo/sh_*.py; ejemplo: videos/primer_foton/).
Fuentes: recesión lunar ≈ 3,8 cm/año (láser a los retrorreflectores de Apolo, NASA/LLR); alargamiento del día ≈ 1,7 ms por siglo; hace ~400 millones de años el día duraba ~22 h (ritmitas y corales fósiles); eclipses totales terminarán en ~600 millones de años (Britannica/NASA).
"""

TITULO = 'La Luna se está yendo'
ARCHIVO = 'luna_se_aleja_short'
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
 'escenas': {'gancho': ('Hook: a mysterious soft rise with celesta and a low moon-like pad, curiosity.', 5),
             'unas': ('Light playful pizzicato, a tiny growth motif.', 4),
             'espejos': ('Techy ticking pulse, a laser zap sparkle rhythm, curious.', 6),
             'dias': ('Slow heavy pendulum bass with a gentle see-saw feel.', 5),
             'pasado': ('Nostalgic warm glockenspiel, rewinding feel.', 4),
             'futuro': ('Wonder-filled spacey pad slowly dimming, then a hopeful note.', 5),
             'cierre': ('Warm triumphant bell chords and a magical sparkle ending.', 6)}}
ESCENAS = [{'id': 'gancho', 'pre': 0.35, 'frases': ['La Luna se está yendo.', 'Cada año está un poco más lejos de la Tierra.']},
 {'id': 'unas', 'frases': ['Se aleja unos cuatro centímetros por año, lo mismo que crecen tus uñas.']},
 {'id': 'espejos',
  'frases': ['Lo sabemos porque los astronautas dejaron espejos en su superficie.',
             'Desde la Tierra les disparamos láseres y medimos cuánto tarda en volver la luz.']},
 {'id': 'dias',
  'frases': ['Las mareas empujan a la Luna hacia afuera, y a cambio frenan un poco a la Tierra.',
             'Por eso los días se alargan, unos milisegundos por siglo.']},
 {'id': 'pasado', 'frases': ['Hace cuatrocientos millones de años, un día duraba unas veintidós horas.']},
 {'id': 'futuro', 'frases': ['Y dentro de unos seiscientos millones de años, la Luna se verá tan pequeña que ya no habrá eclipses totales de Sol.']},
 {'id': 'cierre', 'post': 2.5, 'frases': ['Tenemos suerte de vivir justo ahora, cuando la Luna encaja perfecta delante del Sol.']}]
