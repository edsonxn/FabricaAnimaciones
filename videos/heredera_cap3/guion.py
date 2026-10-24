# -*- coding: utf-8 -*-
"""NOVELA CON IA · «La heredera del rancho», Capítulo 3 «¿Quién está en la tumba?» (~3 min 6 s, vertical 9:16).
Página FB «Lágrimas y Venganza». Continúa `videos/heredera_cap2/`: mismo proyecto de Flow y mismos personajes
(https://flow.google.com/project/44a69a63-fd04-4493-9f93-fa2ab6d933d8). Sin personajes nuevos.

PRIMER CAPÍTULO CON LA RECETA «NOVELA, NO TRÁILER» (docs/formato_novela_ia.md, crítica del usuario 23-oct-2026):
reprise «En el capítulo anterior…» + 3 ESCENAS largas (un lugar, un momento, una conversación que avanza) separadas por
planos de establecimiento mudos; dentro de cada escena plano/contraplano, una reacción muda y la MISMA luz y vestuario;
una línea por clip con silencios; un solo cliffhanger al final; música por momentos (`MEZCLA["musica_curva"]`).

Clip 1 = REPRISE: NO se genera en Flow; se copia videos/heredera_cap2/medios/scene-013.mp4 → medios/scene-001.mp4.
Presupuesto: 18 clips nuevos en 360p (4 de 8 s = 6 pts, 14 de 10 s = 7 pts) = 122 puntos + repeticiones. Más largo que el
cap. 2 (126 s) a propósito: escenas de 50-56 s con una línea por clip y silencios, como pide la receta.
Continuidad entre clips de una escena: `_PUESTAn` (puesta en escena fija, palabra por palabra) + `_MISMA` + la misma imagen de
escenario; cada escena termina en la decisión que provoca la siguiente.

BIBLIA DE LA SERIE (lo de los caps. 1-2 sigue igual; ver el docstring de videos/heredera_cap2/guion.py):
- LA VERDAD (sigue sin revelarse entera): Carmen está VIVA en Tapalpa con otro nombre. La noche del 12-oct-2010 Leonor mandó a
  Nacho (hermano mayor de Chuy) a sacarla del rancho; forcejearon y Nacho cayó por la escalera de la capilla y murió. Carmen huyó
  creyendo que lo había matado; Leonor enterró a Nacho en la tumba sin nombre y desde entonces chantajea a Carmen.
- Cap. 3 revela: (1) Leonor deja ver que Carmen vive («tu madre lo va a pagar»); (2) Doña Chela: esa noche también desapareció
  Nacho, y la patrona dijo que «se fue al norte»; (3) Valeria se pasa al lado de Lupe (vio a su madre pagarle a Chuy);
  (4) en la tumba hay un hombre: la hebilla de plata con cabeza de caballo es de Nacho; Chuy la reconoce.
- Cap. 3 termina: Chuy, con la escopeta, cree que Carmen mató a su hermano: «Esa noche mi hermano fue por tu madre.»
- Cap. 4: «¿Dónde está Carmen?» (Chuy quiere venganza contra Carmen; Leonor lo usa; Lupe y Valeria buscan a Carmen; una
  pista lleva a Tapalpa).
"""

TITULO = "La heredera del rancho · Capítulo 3"
ARCHIVO = "la_heredera_del_rancho_cap3"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
SIN_VOZ = True          # sin narrador: el diálogo vive en el audio de cada clip
SUBTITULOS = False
DURACION = 186.0
BPM = 80                # 1 compás = 3 s

SECUENCIA = dict(
    clips_s=[10, 10, 10, 10, 10, 10, 8, 8, 10, 10, 10, 10, 8, 8, 10, 10, 10, 10, 10],  # 182 s (clip 1 = reprise del cap. 2)
    video_calidad="360p",
    combinar=False,     # un plano y su diálogo por clip: cortar a mitad de frase rompe el lipsync
    dialogo=True,       # NO añadir «sin diálogo»: los personajes hablan
    fundido=0.0,        # cortes secos, como telenovela
    ambiente=1.0,       # el audio del clip ES el diálogo
    ambiente_por={},
    carpeta_descargas="flow-heredera_cap3",
)

# Fichas IDÉNTICAS a las de videos/heredera_cap2/guion.py (no cambiarlas: los personajes de Flow van de ingrediente).
# OJO (novela_altar): NO poner «shot on ARRI Alexa»: Flow quema el texto «ARRI ALEXA» en el video.
FICHA = dict(
    estilo="Vertical nine by sixteen shot from a modern prestige Mexican telenovela, photorealistic live action, cinematic "
           "35mm lens look, shallow depth of field, warm golden natural light with deep shadows, earthy colors of a Jalisco "
           "hacienda, natural skin texture, subtle film grain, dramatic soap opera acting",
    personajes={
        "lupe": "a 24-year-old Mexican woman with warm light-brown skin, long black hair in a single thick braid over her "
                "shoulder, big dark expressive eyes, no makeup, wearing a light-blue maid uniform dress with a white apron, "
                "a small silver cross necklace",
        "leonor": "an elegant 60-year-old Mexican woman with fair skin, short silver-blonde hair in a perfect bob, pearl "
                  "earrings and a pearl necklace, a black tailored mourning dress, red nail polish, cold arrogant gaze",
        "valeria": "a 30-year-old Mexican woman with fair skin, long glossy chestnut hair, big black sunglasses pushed up "
                   "on her head, a short black designer dress, a smartphone always in her hand",
        "emiliano": "a 29-year-old Mexican ranch foreman with tanned skin, short dark hair and stubble, a denim shirt "
                    "with rolled-up sleeves, a leather belt with a big silver buckle, holding a straw cowboy hat",
        "chela": "a 66-year-old short plump Mexican cook with brown wrinkled skin, grey hair in a low bun, small gold "
                 "earrings, a dark-green dress with a checkered red-and-white apron and a grey rebozo shawl",
        "chuy": "a 40-year-old big tough Mexican ranch hand with dark tanned skin, a thick black mustache, a scar across "
                "his left eyebrow, a dirty black cowboy hat, a black leather vest over a sweaty grey shirt",
    },
    nombres={"lupe": "Lupe", "leonor": "Doña Leonor", "valeria": "Valeria", "emiliano": "Emiliano",
             "chela": "Doña Chela", "chuy": "Chuy"},
    objetos={
        "linterna": "The lantern is an old kerosene lantern with a warm flickering flame",
        "hebilla": "The buckle is an old tarnished silver belt buckle shaped like a horse head, on a rotten leather belt",
        "escopeta": "The shotgun is an old double-barrel hunting shotgun with a worn wooden stock",
        "barreta": "The crowbar is a long rusty iron crowbar",
    },
    epoca="a traditional hacienda in Los Altos de Jalisco, Mexico, today, the days after the owner's funeral: stone "
          "arches, an inner courtyard with a stone fountain and magenta bougainvillea, terracotta tile floors, heavy "
          "carved wooden furniture, black mourning ribbons still on the doors",
    cierre="No on-screen text, no subtitles, no captions, no logos, no watermark. Only the spoken lines written here, "
           "clear Mexican Spanish accent, no background music.",
)

# Escenarios: la MISMA imagen de Flow en todos los clips de una escena (capilla = la del cap. 2; cocina = la del cap. 2).
_CAPILLA = ("the small old stone chapel of the hacienda at night: a simple altar with a wooden crucifix, dead flowers, "
            "a few iron crosses in the stone floor, and one plain stone tomb with a plain iron cross and no name, "
            "lit only by a kerosene lantern")
_COCINA = ("the big old kitchen of the hacienda at dawn: blue-and-white Talavera tiles, a wood-fired stove with "
           "clay pots, a clay comal with tortillas, hanging copper pans, strings of dried red chiles, a long wooden table, "
           "steam and the first pale-blue light through the window")
_MISMA = ("Continuing the same conversation from the previous shot, same moment, same lighting, same clothes, the "
          "characters stay exactly where they were.")

# PUESTA EN ESCENA FIJA por escena (cap. 3, contra el efecto tráiler): se repite PALABRA POR PALABRA en cada clip de la escena
# para que Flow deje a cada personaje en su sitio, con la misma luz y los mismos objetos, de un clip al siguiente.
_PUESTA1 = ("Fixed blocking of this scene: Lupe stands in front of the nameless tomb on the LEFT of the frame holding a "
            "lantern; Doña Leonor stands on the RIGHT, near the open chapel door, holding her own lantern; Emiliano stands "
            "behind Lupe, near the altar. Night; the only light comes from the two lanterns.")
_PUESTA1B = _PUESTA1.replace("Doña Leonor stands on the RIGHT, near the open chapel door, holding her own lantern",
                              "on the RIGHT the open chapel door is now empty and dark (Doña Leonor has left)").replace(
                              "the two lanterns", "Lupe's lantern")
_PUESTA2 = ("Fixed blocking of this scene: Doña Chela stands at the wood-fired stove on the RIGHT, patting tortillas on the "
            "clay comal; Lupe stands beside her on the LEFT, in her light-blue uniform, with dark circles under her eyes; the "
            "open kitchen door is in the background between them. Pale-blue dawn light from the window and warm firelight.")
_PUESTA3 = ("Fixed blocking of this scene: Emiliano kneels at the head of the nameless tomb holding the crowbar; Lupe stands "
            "on the LEFT side of the tomb holding the lantern high; the wooden chapel door is in the background behind them. "
            "Night; the only light is Lupe's lantern.")

# Un clip por plano. `dialogo` = (personaje, tono, línea) -> «X says in Mexican Spanish, <tono>: "…"».
# Cada escena es UNA conversación que avanza: cada línea responde a la anterior, una línea por clip con la reacción de quien
# escucha y silencios; cada escena termina en la decisión que lleva a la siguiente (causa → efecto, no momentos sueltos).
PLANOS = [
    # ── 0-10 s · «EN EL CAPÍTULO ANTERIOR…» (reprise: medios/scene-001.mp4 = heredera_cap2/medios/scene-013.mp4) ──
    dict(clip=1, reprise="../heredera_cap2/medios/scene-013.mp4", personajes=["lupe", "leonor"], objetos=["linterna"],
         escenario=_CAPILLA, a="REPRISE: no se genera en Flow (es el último clip del capítulo 2).",
         dialogo=[]),

    # ── ESCENA 1 · LA CAPILLA, LA MISMA NOCHE (10-60 s): sigue la plática del cap. 2; Leonor deja ver que Carmen vive ──
    # termina en: «nos está mirando» → la tumba se abrirá otro día (escena 3)
    dict(clip=2, personajes=["leonor", "lupe", "emiliano"], objetos=["linterna"], escenario=_CAPILLA,
         a=f"{_PUESTA1} {_MISMA} Right after Lupe asked who is in the tomb. Close-up of Doña Leonor's face, half lit by her "
           "lantern: she glances at the nameless tomb, a thin cold smile, and answers slowly. Then a silent reverse close-up "
           "of Lupe listening, jaw tight, eyes wet.",
         dialogo=[("leonor", "slow, contemptuous", "Alguien que nadie va a extrañar.")]),
    dict(clip=3, personajes=["lupe", "leonor", "emiliano"], objetos=["linterna"], escenario=_CAPILLA,
         a=f"{_PUESTA1} {_MISMA} Close-up of Lupe, voice shaking but holding Leonor's gaze; then a silent reverse shot of "
           "Doña Leonor tilting her head, unimpressed, her red nails tapping her lantern.",
         dialogo=[("lupe", "trembling, accusing", "Usted sabe dónde está mi madre.")]),
    dict(clip=4, personajes=["leonor", "lupe", "emiliano"], objetos=["linterna"], escenario=_CAPILLA,
         a=f"{_PUESTA1} {_MISMA} Doña Leonor takes two slow steps toward Lupe until the two lanterns almost touch; tight "
           "over-the-shoulder shot from behind Lupe; Leonor lowers her voice to an icy whisper.",
         dialogo=[("leonor", "an icy whisper", "Lo que sé es que, si abres esa tumba, tu madre lo va a pagar.")]),
    dict(clip=5, personajes=["lupe", "leonor", "emiliano"], objetos=["linterna"], escenario=_CAPILLA,
         a=f"{_PUESTA1} {_MISMA} Silent reaction shot: very slow push-in on Lupe's face for three seconds as she understands, "
           "hope and fear at once; she whispers. Doña Leonor does not answer: she turns her back and walks out through the "
           "chapel door; the door creaks.",
         dialogo=[("lupe", "barely a breath, stunned", "¿Lo va a pagar…? Entonces está viva.")]),
    dict(clip=6, personajes=["lupe", "emiliano"], objetos=["linterna"], escenario=_CAPILLA,
         a=f"{_PUESTA1B} {_MISMA} Doña Leonor is gone. Two-shot: Emiliano steps beside Lupe; a long silence, a tear runs down "
           "her cheek; she wipes it, determined, and looks at the tomb; Emiliano glances at the dark doorway and stops her.",
         dialogo=[("lupe", "quiet, determined", "Entonces vamos a abrirla."),
                  ("emiliano", "low, worried", "Hoy no, Lupe. Nos está mirando.")]),

    # ── CORTINILLA (60-68 s): plano de establecimiento mudo, el amanecer siguiente ──
    dict(clip=7, personajes=[],
         escenario="the whole hacienda seen from the hill at dawn: stone walls, a bell tower, the small chapel, low mist "
                   "over the fields, magenta bougainvillea, smoke rising from the kitchen chimney, the sky turning orange",
         a="Slow wide establishing shot drifting toward the hacienda at dawn, the morning after; mist moves over the fields; "
           "a rooster flaps its wings on the wall; smoke rises from the kitchen chimney. No people. Nobody speaks.",
         dialogo=[]),

    # ── ESCENA 2 · LA COCINA AL AMANECER (68-124 s): Nacho desapareció la misma noche; Valeria se voltea ──
    # termina en: «mañana la tapan con cemento» → «Entonces es esta noche» (escena 3)
    dict(clip=8, personajes=["lupe", "chela"], escenario=_COCINA,
         a=f"{_PUESTA2} Two-shot: Lupe, who has not slept, comes close to old Doña Chela and speaks low; Doña Chela's hands "
           "freeze on the tortilla; silence.",
         dialogo=[("lupe", "low, urgent", "Doña Chela, en la tumba de la capilla hay alguien.")]),
    dict(clip=9, personajes=["chela", "lupe"], escenario=_COCINA,
         a=f"{_PUESTA2} {_MISMA} Close-up of Doña Chela: she slowly takes her hands off the comal, crosses herself, looks "
           "toward the open door to make sure nobody is there, and whispers; Lupe in soft focus in the foreground.",
         dialogo=[("chela", "a frightened whisper", "Esa misma noche también desapareció Nacho… el hermano de Chuy.")]),
    dict(clip=10, personajes=["lupe", "chela"], escenario=_COCINA,
         a=f"{_PUESTA2} {_MISMA} Reverse close-up of Lupe asking, shocked; then Doña Chela answers, bitter, pulling her grey "
           "rebozo tight around her shoulders.",
         dialogo=[("lupe", "shocked, softly", "¿Y nadie lo buscó?"),
                  ("chela", "bitter, low", "La patrona dijo que se fue al norte. Y Chuy le creyó.")]),
    dict(clip=11, personajes=["valeria", "lupe", "chela"], escenario=_COCINA,
         a=f"{_PUESTA2} {_MISMA} A noise at the open kitchen door behind them: Lupe and Doña Chela turn, frightened. Valeria "
           "is standing in the doorway, phone lowered, no makeup, she heard everything; a silent beat as the three women look "
           "at each other; then Valeria speaks, ashamed but firm. Exactly the same woman as the Valeria character reference.",
         dialogo=[("valeria", "ashamed but firm", "Mi mamá le pagó a Chuy anoche. Yo la vi.")]),
    dict(clip=12, personajes=["lupe", "valeria", "chela"], escenario=_COCINA,
         a=f"{_PUESTA2} {_MISMA} Valeria has stepped into the kitchen. Close-up of Lupe, distrustful, arms crossed; then "
           "reverse close-up of Valeria answering, nervous, glancing back at the door.",
         dialogo=[("lupe", "distrustful, cold", "¿Y por qué me lo dices a mí?"),
                  ("valeria", "nervous, quick", "Porque mañana mi mamá manda tapar esa tumba con cemento.")]),
    dict(clip=13, personajes=["lupe", "chela", "valeria"], escenario=_COCINA,
         a=f"{_PUESTA2} {_MISMA} Silent reaction: Valeria waits by the door; Lupe and Doña Chela look at each other for three seconds; the tortilla burns "
           "on the comal and smokes; then Lupe speaks, decided.",
         dialogo=[("lupe", "quiet, decided", "Entonces es esta noche.")]),

    # ── CORTINILLA (124-132 s): esa noche; Valeria vigila desde el balcón (ata la escena 2 con la 3) ──
    dict(clip=14, personajes=["valeria"], objetos=["linterna"],
         escenario="an upper stone balcony of the hacienda at night overlooking the dark courtyard, and beyond it the small "
                   "stone chapel under a starry sky, a cypress tree moving in the wind",
         a="That night. From the dark balcony, Valeria watches, nervous, phone in her hand; far below, a single lantern crosses "
           "the courtyard toward the chapel, carried by two small figures. Dogs bark in the distance. Valeria says nothing at all: her lips stay closed "
           "the whole time, completely silent, only night ambience.",
         dialogo=[]),

    # ── ESCENA 3 · LA CAPILLA, ESA NOCHE (132-182 s): abren la tumba; Chuy reconoce la hebilla ──
    dict(clip=15, personajes=["lupe", "emiliano"], objetos=["linterna", "barreta"], escenario=_CAPILLA,
         a=f"{_PUESTA3} Emiliano pushes the crowbar under the heavy stone lid of the nameless tomb and strains; the stone "
           "grinds and slides a few inches; dust falls into the lantern light.",
         dialogo=[("emiliano", "straining, low", "Alúmbrame aquí, Lupe.")]),
    dict(clip=16, personajes=["lupe", "emiliano"], objetos=["linterna", "hebilla"], escenario=_CAPILLA,
         a=f"{_PUESTA3} {_MISMA} The lid is half open. Close-up of Lupe leaning over the tomb, the lantern light on her face; "
           "inside only an old rotten grey blanket and the buckle; she slowly picks up the buckle, blows the dust off it and "
           "turns it in the light; Emiliano watches her. Nothing gory.",
         dialogo=[("lupe", "a trembling whisper, relieved and horrified", "No es mi mamá… Es un hombre.")]),
    dict(clip=17, personajes=["chuy", "lupe", "emiliano"], objetos=["linterna", "hebilla", "escopeta"], escenario=_CAPILLA,
         a=f"{_PUESTA3} {_MISMA} The chapel door behind them bangs open: Chuy stands in the doorway pointing the shotgun at "
           "them; Lupe and Emiliano turn; Chuy shouts, then sees the silver buckle in Lupe's hand and stops.",
         dialogo=[("chuy", "a rough angry shout", "¿Qué tienes en la mano?")]),
    dict(clip=18, personajes=["chuy", "lupe", "emiliano"], objetos=["linterna", "hebilla", "escopeta"], escenario=_CAPILLA,
         a=f"{_PUESTA3} {_MISMA} Chuy walks in slowly, the shotgun lowered and pointed at the floor, staring at the buckle; "
           "his face falls and his "
           "voice breaks; silent reverse close-up of Lupe holding the buckle out in her trembling hand.",
         dialogo=[("chuy", "a broken rough voice", "Esa hebilla… era de mi hermano Nacho.")]),
    dict(clip=19, personajes=["chuy", "lupe", "emiliano"], objetos=["linterna", "escopeta"], escenario=_CAPILLA,
         a=f"{_PUESTA3} {_MISMA} Chuy's eyes fill with tears and anger; he grips the shotgun across his chest, NOT aiming "
           "it at anyone, and steps closer to Lupe, glaring at her. Then a slow push-in on Lupe's face as she freezes in shock, the lantern shaking in her hand.",
         dialogo=[("chuy", "a low furious whisper", "Esa noche, mi hermano fue por tu madre.")]),
]

# Rótulos por código (énfasis, no subtítulos): reprise, título y el gancho al capítulo 4 (detalle en efectos.py).
ROTULOS = [
    dict(t=0.3, dur=3.0, texto="En el capítulo anterior…"),
    dict(t=10.2, dur=2.8, texto="LA HEREDERA DEL RANCHO\nCapítulo 3"),
    dict(t=182.0, dur=4.0, texto="Continuará…\nCapítulo 4: ¿Dónde está Carmen?"),
]

LYRIA = dict(   # la música sale de Flow Music (doc § «Música de telenovela»); esto es su estructura por segundos
    estilo="Mexican ranchera telenovela dramatic score: lush strings, solo piano, a melancholic requinto guitar and a "
           "soft distant trumpet, slow tempo 80 BPM, cinematic and melodramatic, sparse, lots of silence for dialogue.",
    escenas={
        "reprise": ("Dark reprise of last episode's cliffhanger sting, decaying.", 3),
        "capilla1": ("Almost silent: a very low organ drone, one sustained cello note; a sad swell at the twist.", 17),
        "cortinilla1": ("Telenovela bumper: a short lyrical requinto guitar and strings phrase at dawn.", 3),
        "cocina": ("Almost silent under dialogue: soft pizzicato and a music-box piano; a tense string swell at the end.", 18),
        "cortinilla2": ("Short sinister bumper: low strings and a distant bell.", 3),
        "tumba": ("Slow-building suspense: heartbeat drum and tremolo strings, rising to one huge final cliffhanger sting.", 18),
    },
    tramos=[(["reprise", "capilla1", "cortinilla1", "cocina", "cortinilla2", "tumba"],
             "Mostly silence under the conversations; music rises only at scene twists, bumpers and the final sting.")],
)

# Música POR MOMENTOS (receta «novela, no tráiler»): casi muda bajo la plática, sube en giros, cortinillas y el cliffhanger.
MEZCLA = dict(musica=-25.0, musica_curva=[
    (0, 0), (9, 0), (11, -12),                  # reprise con su golpe → casi fuera bajo la escena 1
    (40, -12), (43, -6), (50, -6), (52, -12),   # giro «Entonces está viva» y vuelve a bajar
    (58, -12), (60, 0), (67, 0), (70, -14),     # cortinilla del amanecer → escena 2 casi muda
    (97, -14), (99, -7), (108, -7), (110, -12), # entra Valeria
    (121, -12), (123, -4), (124, 0), (131, 0), (134, -12),   # «Entonces es esta noche» → cortinilla del balcón → escena 3
    (151, -12), (153, -5), (172, -3), (182, 0), (186, 0),    # Chuy entra → sube hasta el golpe final
])
TRANSICIONES = [("corte", 0.0)] * 5
MUSICA = {"reprise": dict(sabor="tension"), "tumba": dict(sabor="tension")}

ESCENAS = [   # secciones musicales (SIN_VOZ): 62 compases = 186 s
    {"id": "reprise", "compases": 3, "frases": []},      # clip 1: reprise del cap. 2 (0-10)
    {"id": "capilla1", "compases": 17, "frases": []},    # clips 2-6: Leonor «tu madre lo va a pagar» (10-60)
    {"id": "cortinilla1", "compases": 3, "frases": []},  # clip 7: la hacienda al amanecer (60-68)
    {"id": "cocina", "compases": 18, "frases": []},      # clips 8-13: Chela, Nacho, Valeria, «es esta noche» (68-124)
    {"id": "cortinilla2", "compases": 3, "frases": []},  # clip 14: Valeria en el balcón (124-132)
    {"id": "tumba", "compases": 18, "frases": []},       # clips 15-19: la tumba, la hebilla, Chuy (132-186)
]
