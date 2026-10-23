# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — Short vertical de `chinche_invierno`. Regla de la tanda (22-oct-2026): cada largo lleva su Short de
30-45 s, publicado ~12 h después, con «Vídeo relacionado» = su largo. Hechos y fuentes: docstring de videos/chinche_invierno/guion.py.
Escrito por videos/_hacer_shorts_wnd.py (imágenes nuevas de Flow en 9:16, mismas fichas que el largo; voz EnglishComic)."""

TITULO = 'What If You Let a Stink Bug Stay All Winter? #Shorts'
ARCHIVO = 'stinkbug_winter_short'
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160
GAP = 0.18
LARGO = dict(video='chinche_invierno', id='ScnMG05QH6s')
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(video_s=0, clip_s=8, img_s=2.6, rapido_hasta=300, img_s_lento=2.6, fundido=0.15, ambiente=0.0,
                 ambiente_por={}, carpeta_descargas="flow-chinche_invierno_short")

FICHA = {'estilo': 'Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, vertical nine by sixteen composition with the main subject large in the center', 'personajes': {'bug': 'a cartoon brown marmorated stink bug with a mottled brown shield-shaped body, small white bands on its antennae and legs, big round sleepy eyes, and a tiny gray knitted beanie hat', 'human': 'a simple cartoon man with a round white head, dot eyes, a short gray beard, glasses and a plaid flannel shirt', 'wasp': 'a tiny cartoon samurai wasp, shiny black, with a small white headband and big determined eyes'}, 'objeto': 'a cozy American living room in winter with a reading lamp, a sofa, a window with frost, and a warm radiator', 'epoca': 'present-day American suburban home in late autumn and winter', 'cierre': 'No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.'}

TRANSICIONES = [("continua", 0.1)] * 6

LYRIA = dict(
    estilo='Cozy, wry cartoon nature documentary score about a clumsy stink bug spending the winter in a house: pizzicato strings, bassoon, tuba, marimba, felt piano, soft clarinet, light brushed percussion. Comic, warm, a little grumpy. Instrumental only, never loud under the voice.',
    escenas={},
    tramos=[(['hook', 'winter', 'smell', 'cierre'], "Start instantly with a playful hook, keep a light comic pulse under the voice, then a warm resolved "
                     "ending that fades out.")],
)

ESCENAS = [
    {'id': 'hook', 'frases': ['A stink bug lands on your sleeve in November. What if you just let it live there all winter?'], 'pre': 0.1},
    {'id': 'winter', 'frases': ['It would sleep. In your walls, for months. No eating, no eggs, no damage.', 'One man in Maryland counted more than twenty-six thousand of them in his house in one season.']},
    {'id': 'smell', 'frases': ['Squeeze one, and it sprays a chemical that is also found in cilantro.', 'So if cilantro tastes like soap to you, this bug is your nightmare.']},
    {'id': 'cierre', 'frases': ['In spring it leaves, to eat apples and peaches. So skip the squish. Drop it in a jar of soapy water.'], 'post': 0.6},
]
