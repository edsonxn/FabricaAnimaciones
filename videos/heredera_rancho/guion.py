# -*- coding: utf-8 -*-
"""NOVELA CON IA · «La heredera del rancho», Capítulo 1 (~2 min, vertical 9:16). Página FB «Lágrimas y Venganza».
Serie de muchos capítulos (pedida por el usuario el 23-oct-2026). Premisa con datos (docs/formato_novela_ia.md): herencia +
familia que la quiere fuera (428×) + revelación de parentesco (169×). Don Aurelio Montalvo muere y deja el rancho El Mezquital
(Los Altos de Jalisco) a Lupe, la sirvienta; la viuda Leonor y sus hijos la quieren fuera. Secreto: Lupe es hija de Aurelio
y de Carmen, la cocinera que «se fue» hace años (Leonor sabe qué le pasó).

Motor SECUENCIA en modo SIN_VOZ con `dialogo=True` (como `videos/novela_altar/`): cada clip de Flow trae su diálogo con
labios sincronizados. Consistencia: PERSONAJES de Flow (retrato + cuerpo + voz fija) e imagen del escenario como ingredientes.
Presupuesto: 13 clips en 360p (4 de 8 s = 6 pts, 9 de 10 s = 7 pts) = 87 puntos + repeticiones; descarga «720p mejorada».

BIBLIA DE LA SERIE (para los capítulos siguientes):
- Lupe (Guadalupe Ríos, 24): sirvienta desde niña en la casa; su madre Carmen era la cocinera y desapareció cuando Lupe tenía 8.
- Leonor Montalvo (60): la viuda, elegante y fría; sabe que Lupe es hija de Aurelio y qué le pasó a Carmen.
- Rodrigo (36): el hijo mayor, ambicioso, endeudado; Valeria (30): la hija consentida, frívola, pero no mala del todo.
- Licenciado Ibarra (58): el notario, leal a Aurelio. Emiliano (29): el caporal, aliado de Lupe (interés amoroso).
- Condición del testamento: si a Lupe le pasa algo, todo va a la beneficencia (por eso no pueden simplemente matarla).
- Cap. 2: «¿Qué le pasó a Carmen?» (Lupe busca en el cuarto de su madre; Leonor contrata a alguien para asustarla).
"""

TITULO = "La heredera del rancho · Capítulo 1"
ARCHIVO = "la_heredera_del_rancho_cap1"
MOTOR = "secuencia"
FORMATO = "vertical"
ESTILO_VISUAL = "secuencia_flow"
SIN_VOZ = True          # sin narrador: el diálogo vive en el audio de cada clip
SUBTITULOS = False
DURACION = 126.0
BPM = 80                # 1 compás = 3 s

SECUENCIA = dict(
    clips_s=[8, 10, 10, 8, 10, 10, 10, 8, 10, 10, 10, 8, 10],  # 122 s
    video_calidad="360p",
    combinar=False,     # un plano y su diálogo por clip: cortar a mitad de frase rompe el lipsync
    dialogo=True,       # NO añadir «sin diálogo»: los personajes hablan
    fundido=0.0,        # cortes secos, como telenovela
    ambiente=1.0,       # el audio del clip ES el diálogo
    ambiente_por={},
    carpeta_descargas="flow-heredera_rancho",
)

# Ficha visual: se repite PALABRA POR PALABRA en cada prompt donde aparezca (los personajes de Flow van de ingrediente).
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
        "rodrigo": "a 36-year-old Mexican man with fair skin, slicked-back brown hair, a thin mustache, black suit with a "
                   "white open-collar shirt and no tie, a gold signet ring, arrogant expression",
        "valeria": "a 30-year-old Mexican woman with fair skin, long glossy chestnut hair, big black sunglasses pushed up "
                   "on her head, a short black designer dress, a smartphone always in her hand",
        "ibarra": "a 58-year-old Mexican notary with grey hair, round wire glasses, a grey three-piece suit and a burgundy "
                  "tie, holding a brown leather folder",
        "emiliano": "a 29-year-old Mexican ranch foreman with tanned skin, short dark hair and stubble, a denim shirt "
                    "with rolled-up sleeves, a leather belt with a big silver buckle, holding a straw cowboy hat",
        "aurelio": "a frail 70-year-old Mexican man with a thick white mustache and grey hair, pale and sick, in white "
                   "cotton pajamas",
    },
    nombres={"lupe": "Lupe", "leonor": "Doña Leonor", "rodrigo": "Rodrigo", "valeria": "Valeria",
             "ibarra": "Licenciado Ibarra", "emiliano": "Emiliano", "aurelio": "Don Aurelio"},
    objetos={
        "bandeja": "The tray is a silver tray with white porcelain coffee cups",
        "testamento": "The will is a few typed pages with official stamps inside the brown leather folder",
        "caja": "The box is a small old carved wooden box with a rosary and faded photographs inside",
        "carta": "The letter is an old yellowed envelope sealed with red wax, with handwriting in blue ink",
    },
    epoca="a traditional hacienda in Los Altos de Jalisco, Mexico, today, during the funeral of the owner: stone arches, "
          "an inner courtyard with a stone fountain and magenta bougainvillea, terracotta tile floors, heavy carved "
          "wooden furniture, black mourning ribbons and white lilies everywhere",
    cierre="No on-screen text, no subtitles, no captions, no logos, no watermark. Only the spoken lines written here, "
           "clear Mexican Spanish accent, no background music.",
)

_ESTUDIO = ("the owner's study of the hacienda: a big dark wooden desk, bookshelves, a mounted longhorn skull, an oil "
            "portrait of an old man with a white mustache, white lilies with a black ribbon, afternoon light through "
            "wooden shutters")
_CUARTO = ("a small humble servant's bedroom of the hacienda at night: whitewashed walls, a narrow iron bed, a Virgin of "
           "Guadalupe image with a votive candle, a small window, warm lamp light")

# Un clip por plano. `dialogo` = (personaje, tono, línea) -> «X says in Mexican Spanish, <tono>: "…"».
PLANOS = [
    dict(clip=1, personajes=["leonor", "lupe"], objetos=["bandeja"],
         a="In the courtyard during the funeral wake, among mourners in black, Doña Leonor slaps Lupe across the face; the "
           "tray falls and the coffee cups shatter on the tiles; mourners gasp; Lupe holds her cheek, eyes full of tears.",
         dialogo=[("leonor", "furious, in front of everyone",
                   "¿Qué haces llorando aquí? ¡Tú no eres de la familia!")]),
    dict(clip=2, personajes=["ibarra", "leonor", "rodrigo", "valeria"], objetos=["testamento"], escenario=_ESTUDIO,
         a="The notary sits at the big desk and opens the leather folder; Doña Leonor sits stiffly in an armchair, "
           "Rodrigo stands behind her with his arms crossed, Valeria scrolls her phone, bored.",
         dialogo=[("ibarra", "formal and slow", "Yo, Aurelio Montalvo, en pleno uso de mis facultades…"),
                  ("rodrigo", "impatient", "Ya, licenciado, vaya al grano.")]),
    dict(clip=3, personajes=["ibarra", "lupe"], objetos=["testamento", "bandeja"], escenario=_ESTUDIO,
         a="The notary lowers his glasses and looks up at Lupe, who is standing by the door holding a tray of coffee; "
           "slow push-in on Lupe; the cup slips from her hand and shatters on the floor.",
         dialogo=[("ibarra", "clear and solemn",
                   "Dejo el rancho El Mezquital, la casa y todo el ganado… a Guadalupe Ríos.")]),
    dict(clip=4, personajes=["valeria", "rodrigo"], escenario=_ESTUDIO,
         a="Valeria bursts into an incredulous laugh and drops her phone on her lap; Rodrigo slams both hands on the "
           "desk, red with rage.",
         dialogo=[("valeria", "laughing in disbelief", "¿A la sirvienta? ¡Mi papá estaba senil!")]),
    dict(clip=5, personajes=["leonor", "lupe"], escenario=_ESTUDIO,
         a="Doña Leonor rises and walks slowly to Lupe, grabs her chin with her red-nailed fingers and forces her to look "
           "up; Lupe trembles, tears running down.",
         dialogo=[("leonor", "quiet and venomous", "¿Con qué lo embrujaste, mosquita muerta?"),
                  ("lupe", "terrified, sobbing", "Yo no sabía nada, señora, se lo juro.")]),
    dict(clip=6, personajes=["rodrigo", "ibarra"], objetos=["testamento"], escenario=_ESTUDIO,
         a="Rodrigo leans over the desk threateningly toward the notary; the notary calmly closes the leather folder "
           "and holds his gaze.",
         dialogo=[("rodrigo", "threatening", "Vamos a impugnar ese testamento."),
                  ("ibarra", "calm, with a hint of warning", "Inténtelo. Pero su padre dejó una condición.")]),
    dict(clip=7, personajes=["ibarra", "leonor", "rodrigo"], escenario=_ESTUDIO,
         a="Close-up of the notary speaking slowly; then Doña Leonor and Rodrigo exchange a long silent look full of "
           "hidden intentions.",
         dialogo=[("ibarra", "slow and serious",
                   "Si a Guadalupe le pasa algo… todo se va a la beneficencia.")]),
    dict(clip=8, personajes=["lupe", "emiliano"], escenario=_CUARTO,
         a="Night: Lupe, crying, throws her few clothes into an old small suitcase on the iron bed; Emiliano stands in "
           "the doorway holding his hat against his chest.",
         dialogo=[("emiliano", "gentle but firm", "¿Te vas a ir así nomás? Don Aurelio te dejó esto por algo."),
                  ("lupe", "crying", "Esta casa nunca va a ser mía.")]),
    dict(clip=9, personajes=["aurelio", "lupe"],
         escenario="the master bedroom of the hacienda some weeks earlier: a big carved wooden bed, a crucifix, medicine "
                   "bottles on the night table, soft morning light",
         a="Flashback with warm soft faded tones: frail Don Aurelio in bed holds Lupe's hand with both hands and looks at "
           "her with deep tenderness; Lupe, sitting at the bedside, is confused.",
         dialogo=[("aurelio", "weak, tender voice", "Prométeme que no te vas a dejar, mija."),
                  ("lupe", "surprised, softly", "¿Mija? Patrón, está delirando.")]),
    dict(clip=10, personajes=["leonor", "rodrigo"],
         escenario="the big living room of the hacienda at night, lit only by a stone fireplace, dark wooden beams",
         a="Doña Leonor stares into the fireplace holding a glass of tequila; Rodrigo paces behind her; she turns to him "
           "with an icy look.",
         dialogo=[("leonor", "cold and controlled", "Si se queda con el rancho, se queda con todo."),
                  ("rodrigo", "nervous", "¿Y qué propones, mamá?"),
                  ("leonor", "a chilling whisper", "Que se vaya… como se fue su madre.")]),
    dict(clip=11, personajes=["lupe"], objetos=["caja", "carta"], escenario=_CUARTO,
         a="Lupe opens her mother's small carved wooden box on the bed; under the rosary she finds the old sealed letter; "
           "she breaks the red wax with trembling fingers and reads, her hand over her mouth.",
         dialogo=[("lupe", "reading aloud, voice breaking", "«Para mi hija… Guadalupe.» ¿Su hija?")]),
    dict(clip=12, personajes=["leonor"],
         escenario="a dark stone corridor of the hacienda at night, a thin line of warm light under a closed wooden door",
         a="In the dark corridor, Doña Leonor stands pressed against the servant's door, listening; her face hardens, "
           "half lit by the light from under the door.",
         dialogo=[("leonor", "a barely audible whisper", "Ya lo sabe.")]),
    dict(clip=13, personajes=["lupe"], objetos=["carta"], escenario=_CUARTO,
         a="Lupe wipes away her tears, holds the letter against her chest, then takes her clothes back out of the "
           "suitcase; slow push-in as she looks at herself in a small mirror, determined for the first time.",
         dialogo=[("lupe", "slow, firm and calm",
                   "Me quedo. Y voy a saber qué le hicieron a mi madre.")]),
]

# Rótulos por código (énfasis, no subtítulos): título y el gancho al capítulo 2 (detalle en efectos.py).
ROTULOS = [
    dict(t=0.3, dur=2.6, texto="LA HEREDERA DEL RANCHO\nCapítulo 1"),
    dict(t=122.0, dur=4.0, texto="Capítulo 2:\n¿Qué le pasó a Carmen?"),
]

LYRIA = dict(
    estilo="Mexican ranchera telenovela dramatic score: lush strings, solo piano, a melancholic requinto guitar and a "
           "soft distant trumpet, slow tempo 80 BPM, cinematic and melodramatic, mixed low under dialogue.",
    escenas={
        "gancho": ("A sudden dramatic string hit, then a tense low drone.", 3),
        "testamento": ("Suspenseful pizzicato strings and a ticking piano ostinato that builds to a shocking reveal "
                       "sting.", 10),
        "humillacion": ("Dark angry strings, menacing cello ostinato, injustice.", 10),
        "despedida": ("Heartbreaking tender theme on requinto guitar and piano, with a warm nostalgic flashback "
                      "feeling.", 6),
        "conspiracion": ("Ominous low strings and a sinister piano motif.", 4),
        "revelacion": ("Rising emotional strings and choir, then a determined heroic theme and one final dramatic "
                       "sting.", 9),
    },
    tramos=[(["gancho", "testamento", "humillacion", "despedida", "conspiracion", "revelacion"],
             "Keep it as a bed under dialogue; end on the final sting.")],
)

MEZCLA = dict(musica=-22.0)   # la música va bajo el diálogo de los clips
TRANSICIONES = [("corte", 0.0)] * 5
MUSICA = {"gancho": dict(sabor="tension"), "testamento": dict(sabor="tension"), "revelacion": dict(sabor="tension")}

ESCENAS = [   # secciones musicales (SIN_VOZ): 42 compases = 126 s
    {"id": "gancho", "compases": 3, "frases": []},        # clip 1: la cachetada en el velorio (0-8)
    {"id": "testamento", "compases": 10, "frases": []},   # clips 2-4: lectura y «a Guadalupe Ríos» (8-36)
    {"id": "humillacion", "compases": 10, "frases": []},  # clips 5-7: Leonor, impugnar, la condición (36-66)
    {"id": "despedida", "compases": 6, "frases": []},     # clips 8-9: la maleta y el flashback (66-84)
    {"id": "conspiracion", "compases": 4, "frases": []},  # clip 10: «como se fue su madre» (84-94)
    {"id": "revelacion", "compases": 9, "frases": []},    # clips 11-13: la carta, «ya lo sabe», «me quedo» (94-126)
]
