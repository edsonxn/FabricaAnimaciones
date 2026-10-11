# -*- coding: utf-8 -*-
"""Tu plátano es radiactivo — Short vertical de ~1 min, boceto + guache (motor compartido nucleo/sh_*.py; ejemplo: videos/primer_foton/).
Fuentes: K-40 = 0,0117 % del potasio natural; un plátano (~420 mg de K) ≈ 15 Bq (Health Physics Society; Oak Ridge/ORAU); 'dosis equivalente de plátano' ≈ 0,1 µSv; radiografía dental ≈ 5 µSv (≈ 50 plátanos); cuerpo humano adulto ≈ 4 000 Bq de K-40 (HPS).
"""

TITULO = 'Tu plátano es radiactivo'
ARCHIVO = 'platano_radiactivo_short'
ESTILO_VISUAL = "boceto"
FORMATO = "vertical"
DURACION = 58.0
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
 'escenas': {'gancho': ('Hook: a suspicious spy-movie pluck, a ticking pulse and a cheeky sting at the end.', 6),
             'potasio': ('Light curious marimba and pizzicato, a friendly science vibe.', 5),
             'atomos': ('Tiny sparkling ticks multiplying, a nervous little rhythm.', 6),
             'dosis': ('Comic balance: a see-saw bassoon-like bass and bright bells, then a quick detector blip rhythm.', 6),
             'cuerpo': ('Warm surprised swell, a wink of glockenspiel.', 5),
             'cierre': ('Relieved bouncy resolution, a final playful stinger.', 6)}}
ESCENAS = [{'id': 'gancho', 'pre': 0.35, 'frases': ['Hay algo radiactivo en tu cocina, y seguro lo has comido.', 'Un plátano.']},
 {'id': 'potasio',
  'frases': ['Los plátanos son ricos en potasio, un mineral que tu corazón y tus músculos necesitan.',
             'Y una pequeñísima parte de ese potasio es radiactiva.']},
 {'id': 'atomos',
  'frases': ['Dentro de un solo plátano, unos quince átomos se desintegran cada segundo.', 'Cada uno suelta un poquito de radiación.']},
 {'id': 'dosis',
  'frases': ['Pero tranquilo, la dosis es diminuta.',
             'Una radiografía dental equivale a comer unos cincuenta plátanos.',
             'Un detector de radiación muy sensible los nota al instante.']},
 {'id': 'cuerpo',
  'frases': ['Y tú tampoco eres inocente: tu cuerpo también tiene potasio.',
             'Por eso tú mismo sueltas unas cuatro mil desintegraciones por segundo.']},
 {'id': 'cierre',
  'post': 1.0,
  'frases': ['Para que un plátano te hiciera daño, tendrías que comer millones de golpe.',
             'Así que tranquilo, el plátano es inocente.',
             'Pero ahora lo mirarás distinto.']}]
