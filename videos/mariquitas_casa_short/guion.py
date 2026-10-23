# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — Short vertical de `mariquitas_casa`. Regla de la tanda (22-oct-2026): cada largo lleva su Short de
30-45 s, publicado ~12 h después, con «Vídeo relacionado» = su largo. Hechos y fuentes: docstring de videos/mariquitas_casa/guion.py.
Escrito por videos/_hacer_shorts_wnd.py (imágenes nuevas de Flow en 9:16, mismas fichas que el largo; voz EnglishComic)."""

TITULO = 'Where Do the Ladybugs in Your House Go? #Shorts'
ARCHIVO = 'ladybugs_winter_short'
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160
GAP = 0.18
LARGO = dict(video='mariquitas_casa', id='zEq5GKLUNMo')
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(video_s=0, clip_s=8, img_s=2.6, rapido_hasta=300, img_s_lento=2.6, fundido=0.15, ambiente=0.0,
                 ambiente_por={}, carpeta_descargas="flow-mariquitas_casa_short")

FICHA = {'estilo': 'Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, vertical nine by sixteen composition with the main subject large in the center', 'personajes': {'beetle': 'a cartoon Asian lady beetle with a shiny round orange shell with black spots, a white head with a small black M-shaped mark, big round cheerful eyes, short black legs, and a tiny red and white knitted winter scarf', 'native': 'a cartoon native ladybug with a bright red shell, seven black spots, a black head with two white cheek spots, big round eyes, and no scarf', 'human': 'a simple cartoon woman with a round white head, dot eyes, round glasses, short gray hair and a lavender cardigan'}, 'objeto': 'a light-colored two-story wooden house with dark green shutters, next to a wooded field', 'epoca': 'present-day American countryside home in autumn, orange and yellow trees, late afternoon sun', 'cierre': 'No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.'}

TRANSICIONES = [("continua", 0.1)] * 6

LYRIA = dict(
    estilo='Cozy, curious cartoon nature documentary score about ladybugs moving into a house for the winter: pizzicato strings, marimba, glockenspiel, soft clarinet, felt piano, light brushed percussion and upright bass. Warm, autumnal and a little mischievous. Instrumental only, never loud under the voice.',
    escenas={},
    tramos=[(['hook', 'who', 'wake', 'cierre'], "Start instantly with a playful hook, keep a light comic pulse under the voice, then a warm resolved "
                     "ending that fades out.")],
)

ESCENAS = [
    {'id': 'hook', 'frases': ['Hundreds of ladybugs on your house in October. A week later, they are gone.', 'So where did they go? Into your walls. For the whole winter.'], 'pre': 0.1},
    {'id': 'who', 'frases': ['And they are probably not ladybugs. See the little M on the head? That is an Asian lady beetle.', 'To them, your sunny wall looks like a cliff back home in Asia. So they move in, every single year.']},
    {'id': 'wake', 'frases': ['They sleep all winter without eating. But a warm day fools them, and out they come, onto your windows.', 'Do not squish them. They bleed a smelly yellow liquid from their knees.']},
    {'id': 'cierre', 'frases': ['Vacuum them up, let them go outside in spring, and seal the gaps before next October.'], 'post': 0.6},
]
