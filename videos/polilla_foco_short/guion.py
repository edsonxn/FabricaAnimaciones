# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — Short vertical de `polilla_foco`. Regla de la tanda (22-oct-2026): cada largo lleva su Short de
30-45 s, publicado ~12 h después, con «Vídeo relacionado» = su largo. Hechos y fuentes: docstring de videos/polilla_foco/guion.py.
Escrito por videos/_hacer_shorts_wnd.py (imágenes nuevas de Flow en 9:16, mismas fichas que el largo; voz EnglishComic)."""

TITULO = "Moths Aren't Attracted to Light. They're Trapped #Shorts"
ARCHIVO = 'moth_porch_light_short'
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160
GAP = 0.18
LARGO = dict(video='polilla_foco', id='G22Fo2UVhXo')
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(video_s=0, clip_s=8, img_s=2.6, rapido_hasta=300, img_s_lento=2.6, fundido=0.15, ambiente=0.0,
                 ambiente_por={}, carpeta_descargas="flow-polilla_foco_short")

FICHA = {'estilo': 'Hand-drawn cartoon illustration, bold black ink outlines with slightly wobbly lines, flat bright colors, simple shapes, full-bleed scene that fills the entire frame edge to edge, no border, no frame, no vignette, vertical nine by sixteen composition with the main subject large in the center', 'personajes': {'moth': 'a cartoon fluffy tan moth with soft brown patterned wings, feathery antennae, big round dizzy eyes, a fuzzy body, and a tiny pair of aviator goggles pushed up on its head', 'human': 'a simple cartoon woman with a round white head, dot eyes, curly red hair, glasses and a cozy green sweater', 'bat': 'a small cartoon brown bat with big ears, tiny fangs and a mischievous grin'}, 'objeto': 'a bright white glowing porch light in a glass lantern on a wooden house wall, with a halo of light', 'epoca': 'present-day American front porch on a warm summer night, dark blue sky, a garden with white night flowers', 'cierre': 'No text, no letters, no words, no numbers, no logos, no watermark, no speech bubbles, no sound effect words.'}

TRANSICIONES = [("continua", 0.1)] * 6

LYRIA = dict(
    estilo='Dreamy, curious cartoon nature documentary score about moths circling a porch light at night: celesta, vibraphone, pizzicato strings, soft clarinet, felt piano, light brushed percussion and upright bass. Nocturnal, gently comic and a little bittersweet. Instrumental only, never loud under the voice.',
    escenas={},
    tramos=[(['hook', 'trap', 'night', 'cierre'], "Start instantly with a playful hook, keep a light comic pulse under the voice, then a warm resolved "
                     "ending that fades out.")],
)

ESCENAS = [
    {'id': 'hook', 'frases': ['Moths circling your porch light are not in love with it. They are trapped.'], 'pre': 0.1},
    {'id': 'trap', 'frases': ['For millions of years, the brightest thing at night was the sky. So insects keep their backs toward the light to stay level.', 'Put a bulb next to a moth, and it tilts toward it, and ends up flying in circles. It can even flip upside down.']},
    {'id': 'night', 'frases': ['By morning, it is exhausted, stuck on your wall, and the birds know exactly where to look.']},
    {'id': 'cierre', 'frases': ['Use a warm yellow bulb, point it down, or just flip the switch.'], 'post': 0.6},
]
