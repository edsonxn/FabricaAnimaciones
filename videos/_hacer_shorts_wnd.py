# -*- coding: utf-8 -*-
"""Escribe el guion.py del Short vertical de cada largo de la tanda de Wild Next Door (22-oct-2026).
Toma FICHA (personajes, objeto, época) del guion del largo y le cambia el formato a 9:16. Plantilla: arana_escusado_short.
Uso: python videos/_hacer_shorts_wnd.py"""
import importlib.util
import os

AQUI = os.path.dirname(os.path.abspath(__file__))

SHORTS = {
    "mariquitas_casa": ("Where Do the Ladybugs in Your House Go? #Shorts", "ladybugs_winter_short", [
        ("hook", ["Hundreds of ladybugs on your house in October. A week later, they are gone.",
                  "So where did they go? Into your walls. For the whole winter."]),
        ("who", ["And they are probably not ladybugs. See the little M on the head? That is an Asian lady beetle.",
                 "To them, your sunny wall looks like a cliff back home in Asia. So they move in, every single year."]),
        ("wake", ["They sleep all winter without eating. But a warm day fools them, and out they come, onto your windows.",
                  "Do not squish them. They bleed a smelly yellow liquid from their knees."]),
        ("cierre", ["Vacuum them up, let them go outside in spring, and seal the gaps before next October."]),
    ]),
    "chinche_invierno": ("What If You Let a Stink Bug Stay All Winter? #Shorts", "stinkbug_winter_short", [
        ("hook", ["A stink bug lands on your sleeve in November. What if you just let it live there all winter?"]),
        ("winter", ["It would sleep. In your walls, for months. No eating, no eggs, no damage.",
                    "One man in Maryland counted more than twenty-six thousand of them in his house in one season."]),
        ("smell", ["Squeeze one, and it sprays a chemical that is also found in cilantro.",
                   "So if cilantro tastes like soap to you, this bug is your nightmare."]),
        ("cierre", ["In spring it leaves, to eat apples and peaches. So skip the squish. Drop it in a jar of soapy water."]),
    ]),
    "hormigas_cocina": ("Why Squishing Ants Never Works #Shorts", "ants_counter_short", [
        ("hook", ["You squish the ants on your counter. By lunch, the line is back. Why?"]),
        ("trail", ["Because they are following an invisible scent trail, like drivers following a map on a delivery app.",
                   "Squish a few drivers, and the order is still on the screen."]),
        ("few", ["And the ants you see may be only a small slice of the colony. The queens are safe inside your wall.",
                 "Spray some kinds, and the colony can split into three."]),
        ("cierre", ["Wipe the trail with soapy water, seal the sugar, and use a slow bait. Erase the map."]),
    ]),
    "telarana_rota": ("What a Spider Does After You Wreck Its Web #Shorts", "spider_web_gone_short", [
        ("hook", ["You sweep away a spider web on your porch. The next morning, it is back. Same spot. How?"]),
        ("drop", ["The spider dropped on a safety line of silk, hid, and waited for you to go inside."]),
        ("rebuild", ["Then it rebuilt. Around sixty-five feet of silk, overnight.",
                     "And it recycles. Spiders eat their old webs, and reuse some of that protein to spin new silk."]),
        ("cierre", ["Sweep it every day, and it will move. Or swap your porch light for a yellow bulb, and fewer bugs means fewer webs."]),
    ]),
    "polilla_foco": ("Moths Aren't Attracted to Light. They're Trapped #Shorts", "moth_porch_light_short", [
        ("hook", ["Moths circling your porch light are not in love with it. They are trapped."]),
        ("trap", ["For millions of years, the brightest thing at night was the sky. So insects keep their backs toward the light to stay level.",
                  "Put a bulb next to a moth, and it tilts toward it, and ends up flying in circles. It can even flip upside down."]),
        ("night", ["By morning, it is exhausted, stuck on your wall, and the birds know exactly where to look."]),
        ("cierre", ["Use a warm yellow bulb, point it down, or just flip the switch."]),
    ]),
    "arana_crias": ("Never Stomp a Spider With a Lumpy Back #Shorts", "spider_babies_short", [
        ("hook", ["You see a big spider in the garage. Its back looks lumpy. Look closer before you stomp."]),
        ("ride", ["Those lumps are babies. A wolf spider mom carries them on her back, sometimes in layers.",
                  "They do not even eat on the ride. They live off their yolk."]),
        ("squish", ["Stomp on her, and the babies do not die with her. They run. In every direction."]),
        ("cierre", ["So skip the boot. A bucket and a piece of cardboard, and carry the whole family outside."]),
    ]),
}

PLANTILLA = '''# -*- coding: utf-8 -*-
"""Wild Next Door (EN INGLÉS) — Short vertical de `{v}`. Regla de la tanda (22-oct-2026): cada largo lleva su Short de
30-45 s, publicado ~12 h después, con «Vídeo relacionado» = su largo. Hechos y fuentes: docstring de videos/{v}/guion.py.
Escrito por videos/_hacer_shorts_wnd.py (imágenes nuevas de Flow en 9:16, mismas fichas que el largo; voz EnglishComic)."""

TITULO = {titulo!r}
ARCHIVO = {archivo!r}
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
DURACION = None
BPM = 160
GAP = 0.18
LARGO = dict(video={v!r}, id=None)
VOZ = dict(referencia="C:/chatterbox_voices/EnglishComic.mp3", idioma="en",
           exaggeration=0.8, cfg_weight=0.3, temperature=0.8)

SECUENCIA = dict(video_s=0, clip_s=8, img_s=2.6, rapido_hasta=300, img_s_lento=2.6, fundido=0.15, ambiente=0.0,
                 ambiente_por={{}}, carpeta_descargas="flow-{v}_short")

FICHA = {ficha!r}

TRANSICIONES = [("continua", 0.1)] * 6

LYRIA = dict(
    estilo={estilo!r},
    escenas={{}},
    tramos=[({ids!r}, "Start instantly with a playful hook, keep a light comic pulse under the voice, then a warm resolved "
                     "ending that fades out.")],
)

ESCENAS = {escenas}
'''


def cargar(v):
    sp = importlib.util.spec_from_file_location("g_" + v, os.path.join(AQUI, v, "guion.py"))
    g = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(g)
    return g


for v, (titulo, archivo, bloques) in SHORTS.items():
    g = cargar(v)
    ficha = dict(g.FICHA)
    ficha["estilo"] = ficha["estilo"].replace("sixteen by nine horizontal",
                                              "vertical nine by sixteen composition with the main subject large in the center")
    escenas = []
    for k, (i, frases) in enumerate(bloques):
        e = {"id": i, "frases": frases}
        if k == 0:
            e["pre"] = 0.1
        if k == len(bloques) - 1:
            e["post"] = 0.6
        escenas.append(e)
    txt = PLANTILLA.format(v=v, titulo=titulo, archivo=archivo, ficha=ficha,
                           estilo=g.LYRIA["estilo"].split(". Never")[0] + ". Instrumental only, never loud under the voice.",
                           ids=[i for i, _ in bloques],
                           escenas="[\n" + "".join(f"    {e!r},\n" for e in escenas) + "]")
    open(os.path.join(AQUI, v + "_short", "guion.py"), "w", encoding="utf-8").write(txt)
    w = sum(len(f.split()) for _, fr in bloques for f in fr)
    print(f"{v}_short: {w} palabras ~ {w / 2.73:.0f} s")
