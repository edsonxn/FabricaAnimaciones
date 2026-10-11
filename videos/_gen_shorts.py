# -*- coding: utf-8 -*-
"""Genera guion.py de los 5 Shorts de ciencia (boceto + guache vertical) del 5-oct-2026."""
import os
import pprint

CAB = '''# -*- coding: utf-8 -*-
"""{titulo} — Short vertical de ~1 min, boceto + guache (motor compartido nucleo/sh_*.py; ejemplo: videos/primer_foton/).
{fuentes}
"""

TITULO = {titulo!r}
ARCHIVO = {archivo!r}
ESTILO_VISUAL = "boceto"
FORMATO = "vertical"
DURACION = {duracion}
BPM = 110
GAP = 0.2
VOZ = dict(referencia="C:/chatterbox_voices/Dan.mp3", idioma="es",
           exaggeration=0.75, cfg_weight=0.3, temperature=0.8)
MEZCLA = dict(musica=-21.5, sfx=-23.0)
ALIAS_QA = {alias!r}
SUBTITULOS = False
MUSICA = {{}}
LYRIA = {lyria}
ESCENAS = {escenas}
'''

ESTILO_LYRIA = ("Playful, curious and wonder-filled score for a one-minute animated science short: warm glockenspiel, celesta, pizzicato strings, "
                "soft marimba, a light ticking pulse, tiny synth sparkles and a gentle bass; a cut-paper, hand-made feel. Keeps moving, with short "
                "stingers at scene changes. Melodies low and sparse so a narrator can speak over it. Instrumental only.")

V = {}

V["platano_radiactivo"] = dict(
    titulo="Tu plátano es radiactivo",
    archivo="platano_radiactivo_short",
    duracion=58.0,
    fuentes="Fuentes: K-40 = 0,0117 % del potasio natural; un plátano (~420 mg de K) ≈ 15 Bq (Health Physics Society; Oak Ridge/ORAU); 'dosis equivalente de plátano' ≈ 0,1 µSv; "
            "radiografía dental ≈ 5 µSv (≈ 50 plátanos); cuerpo humano adulto ≈ 4 000 Bq de K-40 (HPS).",
    alias={},
    escenas=[
        {"id": "gancho", "pre": 0.35, "frases": ["Hay algo radiactivo en tu cocina, y seguro lo has comido.", "Un plátano."]},
        {"id": "potasio", "frases": ["Los plátanos son ricos en potasio, un mineral que tu corazón y tus músculos necesitan.",
                                     "Y una pequeñísima parte de ese potasio es radiactiva."]},
        {"id": "atomos", "frases": ["Dentro de un solo plátano, unos quince átomos se desintegran cada segundo.",
                                    "Cada uno suelta un poquito de radiación."]},
        {"id": "dosis", "frases": ["Pero tranquilo, la dosis es diminuta.",
                                  "Una radiografía dental equivale a comer unos cincuenta plátanos.",
                                  "Un detector de radiación muy sensible los nota al instante."]},
        {"id": "cuerpo", "frases": ["Y tú tampoco eres inocente: tu cuerpo también tiene potasio.",
                                   "Por eso tú mismo sueltas unas cuatro mil desintegraciones por segundo."]},
        {"id": "cierre", "post": 1.0, "frases": ["Para que un plátano te hiciera daño, tendrías que comer millones de golpe.",
                                                 "Así que tranquilo, el plátano es inocente.", "Pero ahora lo mirarás distinto."]},
    ],
    lyria={"gancho": ("Hook: a suspicious spy-movie pluck, a ticking pulse and a cheeky sting at the end.", 6),
           "potasio": ("Light curious marimba and pizzicato, a friendly science vibe.", 5),
           "atomos": ("Tiny sparkling ticks multiplying, a nervous little rhythm.", 6),
           "dosis": ("Comic balance: a see-saw bassoon-like bass and bright bells, then a quick detector blip rhythm.", 6),
           "cuerpo": ("Warm surprised swell, a wink of glockenspiel.", 5),
           "cierre": ("Relieved bouncy resolution, a final playful stinger.", 6)},
)

V["luna_se_aleja"] = dict(
    titulo="La Luna se está yendo",
    archivo="luna_se_aleja_short",
    duracion=58.0,
    fuentes="Fuentes: recesión lunar ≈ 3,8 cm/año (láser a los retrorreflectores de Apolo, NASA/LLR); alargamiento del día ≈ 1,7 ms por siglo; "
            "hace ~400 millones de años el día duraba ~22 h (ritmitas y corales fósiles); eclipses totales terminarán en ~600 millones de años (Britannica/NASA).",
    alias={},
    escenas=[
        {"id": "gancho", "pre": 0.35, "frases": ["La Luna se está yendo.", "Cada año está un poco más lejos de la Tierra."]},
        {"id": "unas", "frases": ["Se aleja unos cuatro centímetros por año, lo mismo que crecen tus uñas."]},
        {"id": "espejos", "frases": ["Lo sabemos porque los astronautas dejaron espejos en su superficie.",
                                    "Desde la Tierra les disparamos láseres y medimos cuánto tarda en volver la luz."]},
        {"id": "dias", "frases": ["Las mareas empujan a la Luna hacia afuera, y a cambio frenan un poco a la Tierra.",
                                 "Por eso los días se alargan, unos milisegundos por siglo."]},
        {"id": "pasado", "frases": ["Hace cuatrocientos millones de años, un día duraba unas veintidós horas."]},
        {"id": "futuro", "frases": ["Y dentro de unos seiscientos millones de años, la Luna se verá tan pequeña que ya no habrá eclipses totales de Sol."]},
        {"id": "cierre", "post": 1.0, "frases": ["Tenemos suerte de vivir justo ahora, cuando la Luna encaja perfecta delante del Sol."]},
    ],
    lyria={"gancho": ("Hook: a mysterious soft rise with celesta and a low moon-like pad, curiosity.", 5),
           "unas": ("Light playful pizzicato, a tiny growth motif.", 4),
           "espejos": ("Techy ticking pulse, a laser zap sparkle rhythm, curious.", 6),
           "dias": ("Slow heavy pendulum bass with a gentle see-saw feel.", 5),
           "pasado": ("Nostalgic warm glockenspiel, rewinding feel.", 4),
           "futuro": ("Wonder-filled spacey pad slowly dimming, then a hopeful note.", 5),
           "cierre": ("Warm triumphant bell chords and a magical sparkle ending.", 6)},
)

V["peso_nube"] = dict(
    titulo="¿Cuánto pesa una nube?",
    archivo="peso_nube_short",
    duracion=58.0,
    fuentes="Fuentes: un cúmulo típico ≈ 500 toneladas de agua (M. LeMone, NCAR); gotas de nube ~0,02 mm que caen ~1 cm/s (velocidad terminal); "
            "corrientes ascendentes (térmicas) sostienen las gotas; un elefante africano ≈ 6 t.",
    alias={},
    escenas=[
        {"id": "gancho", "pre": 0.35, "frases": ["Una nube pesa lo mismo que ochenta elefantes.", "Y aun así, flota."]},
        {"id": "peso", "frases": ["Una nube normal de verano contiene unas quinientas toneladas de agua.",
                                 "Medio millón de litros, suspendidos sobre tu cabeza."]},
        {"id": "gotas", "frases": ["Pero ese agua está repartida en miles de millones de gotitas diminutas.",
                                  "Tan pequeñas que caen a menos de un centímetro por segundo."]},
        {"id": "aire", "frases": ["Además, el aire caliente que sube desde el suelo las empuja hacia arriba.",
                                 "Es como una corriente invisible que las sostiene."]},
        {"id": "lluvia", "frases": ["Pero cuando las gotas se juntan y se hacen más grandes, pesan demasiado.",
                                   "Ya no hay corriente que las aguante, y entonces llueve."]},
        {"id": "cierre", "post": 1.0, "frases": ["Así que cuando mires una nube, recuerda:", "son ochenta elefantes flotando sobre tu cabeza."]},
    ],
    lyria={"gancho": ("Hook: a fluffy bouncy pluck with a surprised cartoon sting.", 6),
           "peso": ("Heavy comic tuba-like bass steps, playful marimba on top.", 5),
           "gotas": ("Tiny delicate raindrop glockenspiel, floating and light.", 4),
           "aire": ("Airy rising pad and gentle flute-like whistles, lifting feel.", 4),
           "lluvia": ("Marimba raindrops building to a soft rain patter and a release.", 6),
           "cierre": ("Cheerful floating resolution, a wink of celesta.", 5)},
)

V["dedos_arrugados"] = dict(
    titulo="¿Por qué se arrugan los dedos en el agua?",
    archivo="dedos_arrugados_short",
    duracion=58.0,
    fuentes="Fuentes: arrugas por vasoconstricción regulada por el sistema nervioso simpático (Wilder-Smith 2004; Changizi 2011); "
            "mejor agarre de objetos mojados con dedos arrugados, sin diferencia en secos (Kareklas, Nettle y Smulders 2013, Biology Letters). Aparecen tras ~5 min en el agua.",
    alias={},
    escenas=[
        {"id": "gancho", "pre": 0.35, "frases": ["Tus dedos se arrugan en el agua, y no es porque se empapen."]},
        {"id": "falso", "frases": ["Si fuera por absorber agua, también se arrugaría el resto de tu piel.",
                                 "Pero no: lo ordena tu sistema nervioso."]},
        {"id": "vasos", "frases": ["Después de unos cinco minutos en el agua, hace que los vasos sanguíneos de tus dedos se contraigan, y la piel se pliega."]},
        {"id": "neumatico", "frases": ["Y las arrugas funcionan como las ranuras de un neumático.", "Canalizan el agua y mejoran el agarre."]},
        {"id": "prueba", "frases": ["En experimentos, la gente con dedos arrugados levantaba objetos mojados más rápido.",
                                   "Con objetos secos no había ninguna diferencia."]},
        {"id": "cierre", "post": 1.0, "frases": ["Quizá es un truco heredado de nuestros ancestros, para agarrar piedras y peces resbalosos.",
                                                 "Tus dedos tienen un sistema antideslizante integrado."]},
    ],
    lyria={"gancho": ("Hook: a squelchy curious pluck and a cheeky sting.", 6),
           "falso": ("Detective-style pizzicato, a little 'wrong answer' buzz then a reveal.", 5),
           "vasos": ("Quiet ticking clock and soft bubbling marimba, scientific.", 4),
           "neumatico": ("Bouncy rolling rhythm like a tire, bright bells.", 6),
           "prueba": ("Playful experiment montage, fast marimba and claps.", 6),
           "cierre": ("Warm clever resolution, a final wink with celesta.", 5)},
)

V["cielo_azul"] = dict(
    titulo="¿Por qué el cielo es azul?",
    archivo="cielo_azul_short",
    duracion=58.0,
    fuentes="Fuentes: dispersión de Rayleigh (∝ 1/λ⁴); el Sol emite menos violeta, la alta atmósfera lo absorbe y el ojo es menos sensible a él (NASA, Britannica); "
            "atardeceres rojos por mayor trayecto atmosférico; cielo de Marte: rojizo de día y azulado al atardecer (NASA/Mars rovers).",
    alias={},
    escenas=[
        {"id": "gancho", "pre": 0.35, "frases": ["El cielo no es azul.", "En realidad, deberías verlo violeta."]},
        {"id": "blanca", "frases": ["La luz del Sol parece blanca, pero lleva todos los colores mezclados."]},
        {"id": "dispersion", "frases": ["Al chocar con el aire, los colores de onda corta, como el azul y el violeta, se dispersan por todo el cielo.",
                                       "El rojo casi pasa de largo."]},
        {"id": "violeta", "frases": ["El violeta se dispersa aún más, pero el Sol emite menos violeta, parte se absorbe arriba, y nuestros ojos lo ven peor.",
                                    "Por eso gana el azul."]},
        {"id": "atardecer", "frases": ["Al atardecer, la luz atraviesa mucho más aire, y el azul se pierde por el camino.",
                                      "Solo llegan el naranja y el rojo."]},
        {"id": "marte", "frases": ["En Marte pasa al revés: el cielo es rojizo de día y azul al atardecer."]},
        {"id": "cierre", "post": 1.0, "frases": ["Cada atardecer rojo es el azul que se quedó atrás."]},
    ],
    lyria={"gancho": ("Hook: a sparkly mysterious rise and a surprised stinger.", 6),
           "blanca": ("Bright prism-like glockenspiel arpeggios.", 5),
           "dispersion": ("Bouncing pinball marimba, scattering sparkles.", 6),
           "violeta": ("A little courtroom-debate pizzicato rhythm, then a bright resolution chime.", 5),
           "atardecer": ("Warm sunset pad with soft celesta and a gentle slow beat.", 4),
           "marte": ("Dusty curious desert plucks, a playful twist.", 5),
           "cierre": ("Warm glowing final chord, a magical fade.", 5)},
)

for nombre, d in V.items():
    lyria = dict(estilo=ESTILO_LYRIA, escenas=d.pop("lyria"))
    txt = CAB.format(titulo=d["titulo"], archivo=d["archivo"], duracion=d["duracion"], fuentes=d["fuentes"], alias=d["alias"],
                     lyria=pprint.pformat(lyria, width=150, sort_dicts=False), escenas=pprint.pformat(d["escenas"], width=150, sort_dicts=False))
    p = os.path.join(os.path.dirname(os.path.abspath(__file__)), nombre, "guion.py")
    open(p, "w", encoding="utf-8").write(txt)
    pal = sum(len(f.split()) for e in d["escenas"] for f in e["frases"])
    print(nombre, "palabras:", pal)
