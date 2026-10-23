# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — Short vertical de `arana_crias`. Regla de la tanda (22-oct-2026): cada largo lleva su Short de
30-45 s, publicado ~12 h después, con «Vídeo relacionado» = su largo. Hechos y fuentes: docstring de videos/arana_crias/guion.py.
Escrito por videos/_hacer_shorts_wnd.py (imágenes nuevas de Flow en 9:16, mismas fichas que el largo; voz EnglishComic)."""

TITULO = 'Never Stomp a Spider With a Lumpy Back #Shorts'
ARCHIVO = 'spider_babies_short'
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160
GAP = 0.18
LARGO = dict(video='arana_crias', id='YsNXuTVIzjw')
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(video_s=0, clip_s=8, img_s=2.6, rapido_hasta=300, img_s_lento=2.6, fundido=0.15, ambiente=0.0,
                 ambiente_por={}, carpeta_descargas="flow-arana_crias_short")

FICHA = {'estilo': 'Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, vertical nine by sixteen composition with the main subject large in the center', 'personajes': {'mom': 'a cartoon brown wolf spider mother with a fuzzy striped gray-brown body, eight sturdy hairy legs, a row of big shiny dark eyes, a warm motherly face, and a tiny pink bandana tied around her head', 'babies': "dozens of tiny pale cartoon baby spiders with dot eyes, piled in layers on their mother's back", 'human': 'a simple cartoon man with a round white head, dot eyes, a baseball cap, a gray hoodie and work boots'}, 'objeto': 'a garage floor with a workbench, garden tools, a broom, and a half-open garage door to the backyard', 'epoca': 'present-day American home in early autumn, evening', 'cierre': 'No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.'}

TRANSICIONES = [("continua", 0.1)] * 6

LYRIA = dict(
    estilo='Tender, slightly suspenseful cartoon nature documentary score about a wolf spider mother carrying her babies: pizzicato strings, marimba, celesta, soft clarinet, felt piano, bassoon, light brushed percussion. Warm, surprising and a little funny. Instrumental only, never loud under the voice.',
    escenas={},
    tramos=[(['hook', 'ride', 'squish', 'cierre'], "Start instantly with a playful hook, keep a light comic pulse under the voice, then a warm resolved "
                     "ending that fades out.")],
)

ESCENAS = [
    {'id': 'hook', 'frases': ['You see a big spider in the garage. Its back looks lumpy. Look closer before you stomp.'], 'pre': 0.1},
    {'id': 'ride', 'frases': ['Those lumps are babies. A wolf spider mom carries them on her back, sometimes in layers.', 'They do not even eat on the ride. They live off their yolk.']},
    {'id': 'squish', 'frases': ['Stomp on her, and the babies do not die with her. They run. In every direction.']},
    {'id': 'cierre', 'frases': ['So skip the boot. A bucket and a piece of cardboard, and carry the whole family outside.'], 'post': 0.6},
]
