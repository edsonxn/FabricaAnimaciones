# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — Short vertical de `hormigas_cocina`. Regla de la tanda (22-oct-2026): cada largo lleva su Short de
30-45 s, publicado ~12 h después, con «Vídeo relacionado» = su largo. Hechos y fuentes: docstring de videos/hormigas_cocina/guion.py.
Escrito por videos/_hacer_shorts_wnd.py (imágenes nuevas de Flow en 9:16, mismas fichas que el largo; voz EnglishComic)."""

TITULO = 'Why Squishing Ants Never Works #Shorts'
ARCHIVO = 'ants_counter_short'
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160
GAP = 0.18
LARGO = dict(video='hormigas_cocina', id='1ytJhwFjptY')
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(video_s=0, clip_s=8, img_s=2.6, rapido_hasta=300, img_s_lento=2.6, fundido=0.15, ambiente=0.0,
                 ambiente_por={}, carpeta_descargas="flow-hormigas_cocina_short")

FICHA = {'estilo': 'Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, vertical nine by sixteen composition with the main subject large in the center', 'personajes': {'ant': 'a cartoon small dark brown house ant with a shiny round head, big round determined eyes, bent antennae, six thin legs, and a tiny orange delivery cap', 'queen': 'a cartoon queen ant, bigger and dark brown, with a long shiny abdomen, big kind eyes and a tiny golden crown', 'human': 'a simple cartoon woman with a round white head, dot eyes, a brown ponytail, a yellow apron and pink rubber gloves'}, 'objeto': 'a bright American kitchen counter with a sugar bowl, a sticky spoon, a few crumbs, a sink and a window', 'epoca': 'present-day American home kitchen in the morning, warm sunlight', 'cierre': 'No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.'}

TRANSICIONES = [("continua", 0.1)] * 6

LYRIA = dict(
    estilo='Busy, clever cartoon nature documentary score about an ant colony behind a kitchen wall: pizzicato strings, marimba, xylophone, bassoon, soft clarinet, felt piano, light brushed percussion and upright bass. Bustling, witty and warm. Instrumental only, never loud under the voice.',
    escenas={},
    tramos=[(['hook', 'trail', 'few', 'cierre'], "Start instantly with a playful hook, keep a light comic pulse under the voice, then a warm resolved "
                     "ending that fades out.")],
)

ESCENAS = [
    {'id': 'hook', 'frases': ['You squish the ants on your counter. By lunch, the line is back. Why?'], 'pre': 0.1},
    {'id': 'trail', 'frases': ['Because they are following an invisible scent trail, like drivers following a map on a delivery app.', 'Squish a few drivers, and the order is still on the screen.']},
    {'id': 'few', 'frases': ['And the ants you see may be only a small slice of the colony. The queens are safe inside your wall.', 'Spray some kinds, and the colony can split into three.']},
    {'id': 'cierre', 'frases': ['Wipe the trail with soapy water, seal the sugar, and use a slow bait. Erase the map.'], 'post': 0.6},
]
