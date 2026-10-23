# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — Short vertical de `telarana_rota`. Regla de la tanda (22-oct-2026): cada largo lleva su Short de
30-45 s, publicado ~12 h después, con «Vídeo relacionado» = su largo. Hechos y fuentes: docstring de videos/telarana_rota/guion.py.
Escrito por videos/_hacer_shorts_wnd.py (imágenes nuevas de Flow en 9:16, mismas fichas que el largo; voz EnglishComic)."""

TITULO = 'What a Spider Does After You Wreck Its Web #Shorts'
ARCHIVO = 'spider_web_gone_short'
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160
GAP = 0.18
LARGO = dict(video='telarana_rota', id='cS1E3faIDbs')
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(video_s=0, clip_s=8, img_s=2.6, rapido_hasta=300, img_s_lento=2.6, fundido=0.15, ambiente=0.0,
                 ambiente_por={}, carpeta_descargas="flow-telarana_rota_short")

FICHA = {'estilo': 'Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, vertical nine by sixteen composition with the main subject large in the center', 'personajes': {'spider': 'a cartoon gray-brown porch orb weaver spider with a plump round abdomen with a pale leaf-shaped pattern, eight hairy banded legs, big round expressive eyes, and a tiny yellow construction hard hat', 'human': 'a simple cartoon man with a round white head, dot eyes, short black hair, a red flannel shirt and jeans'}, 'objeto': 'a round orb web with neat straight spokes and an even spiral, glistening, strung between a porch post and the porch light', 'epoca': 'present-day American front porch at night, a glowing porch light with moths, a wooden railing and a doormat', 'cierre': 'No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.'}

TRANSICIONES = [("continua", 0.1)] * 6

LYRIA = dict(
    estilo='Warm, clever cartoon nature documentary score about a porch spider rebuilding its web overnight: pizzicato strings, marimba, harp-like plucks, celesta, bassoon, soft clarinet, felt piano, light brushed percussion. Resourceful, a little bittersweet, funny. Instrumental only, never loud under the voice.',
    escenas={},
    tramos=[(['hook', 'drop', 'rebuild', 'cierre'], "Start instantly with a playful hook, keep a light comic pulse under the voice, then a warm resolved "
                     "ending that fades out.")],
)

ESCENAS = [
    {'id': 'hook', 'frases': ['You sweep away a spider web on your porch. The next morning, it is back. Same spot. How?'], 'pre': 0.1},
    {'id': 'drop', 'frases': ['The spider dropped on a safety line of silk, hid, and waited for you to go inside.']},
    {'id': 'rebuild', 'frases': ['Then it rebuilt. Around sixty-five feet of silk, overnight.', 'And it recycles. Spiders eat their old webs, and reuse some of that protein to spin new silk.']},
    {'id': 'cierre', 'frases': ['Sweep it every day, and it will move. Or swap your porch light for a yellow bulb, and fewer bugs means fewer webs.'], 'post': 0.6},
]
