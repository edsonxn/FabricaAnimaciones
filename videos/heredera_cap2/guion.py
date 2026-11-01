# -*- coding: utf-8 -*-
"""NOVELA CON IA · «La heredera del rancho», Capítulo 2 «¿Qué le pasó a Carmen?» (~2 min, vertical 9:16).
Página FB «Lágrimas y Venganza». Continúa `videos/heredera_rancho/` (cap. 1): mismo proyecto de Flow y mismos personajes
(https://flow.google.com/project/44a69a63-fd04-4493-9f93-fa2ab6d933d8). Personajes NUEVOS en este capítulo: Doña Chela,
Chuy y Carmen (flashback).

Motor SECUENCIA en modo SIN_VOZ con `dialogo=True` (como el cap. 1): cada clip de Flow trae su diálogo con labios
sincronizados. Consistencia: PERSONAJES de Flow (retrato + cuerpo + voz fija) e imagen del escenario como ingredientes.
Presupuesto: 13 clips en 360p (4 de 8 s = 6 pts, 9 de 10 s = 7 pts) = 87 puntos + repeticiones; descarga «720p mejorada».

BIBLIA DE LA SERIE (para los capítulos siguientes; lo del cap. 1 sigue igual):
- Lupe (Guadalupe Ríos, 24): sirvienta desde niña; su madre Carmen era la cocinera y desapareció cuando Lupe tenía 8.
  Desde la carta del cap. 1 sabe que es hija de Aurelio. En el cap. 2 deja de obedecer: «Ya no soy tu sirvienta».
- Leonor Montalvo (60): la viuda. No puede tocar a Lupe (condición del testamento) → paga a Chuy para que la ASUSTE y se vaya.
- Rodrigo (36): ambicioso, endeudado, se burla de Lupe. Valeria (30): frívola, pero en el cap. 2 ve a su madre pagarle a
  Chuy y empieza a dudar (futura aliada).
- Licenciado Ibarra (58): notario leal a Aurelio; guarda la LLAVE de la capilla que Aurelio dejó para Lupe.
- Emiliano (29): caporal, aliado de Lupe (interés amoroso). Doña Chela (66): cocinera vieja, amiga de Carmen; la vio la
  última noche: «nadie la vio salir». Chuy (40): matón del rancho a sueldo de Leonor.
- Carmen (32 en 2010): la cocinera, igual a Lupe (misma trenza). La noche del 12 de octubre de 2010 dejó la carta y su maleta.
- LA VERDAD (no revelar aún): Carmen está VIVA. Esa noche Leonor mandó a un hombre (Nacho, el hermano mayor de Chuy) a
  sacarla del rancho; forcejearon, Nacho cayó por la escalera de la capilla y murió. Carmen huyó creyendo que lo había matado;
  Leonor enterró a Nacho en la tumba SIN NOMBRE de la capilla y desde entonces chantajea a Carmen (si vuelve, cárcel). Chuy no
  sabe que su hermano está ahí. Carmen vive en Tapalpa con otro nombre.
- Cap. 2 termina: Leonor en la capilla: «Tu madre no está en esa tumba.» Lupe: «¿Entonces quién?»
- Cap. 3: «¿Quién está en la tumba?» (Lupe y Emiliano abren la tumba; Chuy reconoce la hebilla de su hermano.)
"""

TITULO = "La heredera del rancho · Capítulo 2"
ARCHIVO = "la_heredera_del_rancho_cap2"
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
    carpeta_descargas="flow-heredera_cap2",
)

# Ficha visual: se repite PALABRA POR PALABRA en cada prompt donde aparezca (los personajes de Flow van de ingrediente).
# Las fichas de los 7 personajes del cap. 1 son IDÉNTICAS a las de videos/heredera_rancho/guion.py (no cambiarlas).
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
        # NUEVOS en el cap. 2
        "chela": "a 66-year-old short plump Mexican cook with brown wrinkled skin, grey hair in a low bun, small gold "
                 "earrings, a dark-green dress with a checkered red-and-white apron and a grey rebozo shawl",
        "chuy": "a 40-year-old big tough Mexican ranch hand with dark tanned skin, a thick black mustache, a scar across "
                "his left eyebrow, a dirty black cowboy hat, a black leather vest over a sweaty grey shirt",
        "carmen": "a 32-year-old Mexican woman with warm light-brown skin, long black hair in a single thick braid over "
                  "her shoulder, big dark expressive eyes, she looks exactly like an older Lupe, wearing a simple white "
                  "cook's blouse with a red embroidered collar and a long dark skirt",
    },
    nombres={"lupe": "Lupe", "leonor": "Doña Leonor", "rodrigo": "Rodrigo", "valeria": "Valeria",
             "ibarra": "Licenciado Ibarra", "emiliano": "Emiliano", "chela": "Doña Chela", "chuy": "Chuy",
             "carmen": "Carmen"},
    objetos={
        "mandil": "The apron is a white starched maid's apron",
        "sobre": "The envelope is a thick brown paper envelope stuffed with Mexican peso bills",
        "maleta": "The suitcase is an old small brown leather suitcase with brass clasps, covered in dust",
        "llave": "The key is a big old iron key with a ribbon of faded purple silk tied to it",
        "carta": "The letter is a white envelope with handwriting in blue ink, sealed with red wax",
        "linterna": "The lantern is an old kerosene lantern with a warm flickering flame",
    },
    epoca="a traditional hacienda in Los Altos de Jalisco, Mexico, today, the days after the owner's funeral: stone "
          "arches, an inner courtyard with a stone fountain and magenta bougainvillea, terracotta tile floors, heavy "
          "carved wooden furniture, black mourning ribbons still on the doors",
    cierre="No on-screen text, no subtitles, no captions, no logos, no watermark. Only the spoken lines written here, "
           "clear Mexican Spanish accent, no background music.",
)

_ESTUDIO = ("the owner's study of the hacienda: a big dark wooden desk, bookshelves, a mounted longhorn skull, an oil "
            "portrait of an old man with a white mustache, white lilies with a black ribbon, afternoon light through "
            "wooden shutters")
_CUARTO = ("a small humble servant's bedroom of the hacienda at night: whitewashed walls, a narrow iron bed, a Virgin of "
           "Guadalupe image with a votive candle, a small window, warm lamp light")
_COCINA = ("the big old kitchen of the hacienda in the morning: blue-and-white Talavera tiles, a wood-fired stove with "
           "clay pots, hanging copper pans, strings of dried red chiles, a long wooden table, steam and morning sunlight")
_CARMEN = ("a small cook's bedroom closed for sixteen years: thick dust and cobwebs, a white sheet over a narrow bed, a "
           "faded embroidered tablecloth, an old wooden wardrobe, a cracked mirror, dusty light through a small window")
_CAPILLA = ("the small old stone chapel of the hacienda at night: a simple altar with a wooden crucifix, dead flowers, "
            "a few iron crosses in the stone floor, and one plain stone tomb with a plain iron cross and no name, "
            "lit only by a kerosene lantern")

# Un clip por plano. `dialogo` = (personaje, tono, línea) -> «X says in Mexican Spanish, <tono>: "…"».
PLANOS = [
    dict(clip=1, personajes=["valeria", "lupe"], objetos=["mandil"], escenario=_COCINA,
         a="In the kitchen in front of two other servants, Valeria throws the white apron in Lupe's face; Lupe slowly "
           "takes it off her face, folds it calmly and puts it on the table, looking Valeria in the eye; the servants gasp.",
         dialogo=[("valeria", "mocking, loud", "¡Sírveme el desayuno, sirvienta!"),
                  ("lupe", "calm and firm", "Ya no soy tu sirvienta, Valeria.")]),
    dict(clip=2, personajes=["chela", "lupe"], escenario=_COCINA,
         a="Later, alone by the wood-fired stove, old Doña Chela grabs Lupe's arm, looks toward the door to make sure "
           "nobody is listening and whispers to her; Lupe's face changes.",
         dialogo=[("chela", "a frightened whisper", "Tu mamá no se fue, mija. Esa noche nadie la vio salir."),
                  ("lupe", "shocked, softly", "¿Entonces dónde está?")]),
    dict(clip=3, personajes=["leonor", "chuy"], objetos=["sobre"],
         escenario="the dark stables of the hacienda at night: wooden stalls, horses, hay, a single hanging lantern",
         a="In the dark stables, Doña Leonor hands the thick envelope of money to Chuy; he weighs it in his hand and "
           "smiles under his mustache, touching the brim of his hat.",
         dialogo=[("leonor", "cold, quiet", "Que se asuste. Que se vaya sola. Sin un solo rasguño."),
                  ("chuy", "a low rough voice", "Usted manda, patrona.")]),
    dict(clip=4, personajes=["valeria"],
         escenario="an upper stone balcony of the hacienda at night overlooking the courtyard and the lit stable door",
         a="From the dark balcony, Valeria lowers her phone and looks down toward the stables, frowning, troubled, "
           "slowly realizing what her mother is doing.",
         dialogo=[("valeria", "a troubled whisper", "Mamá… ¿qué estás haciendo?")]),
    dict(clip=5, personajes=["lupe", "emiliano"],
         escenario="the end of a dark stone corridor of the hacienda: an old wooden door closed with a rusty padlock "
                   "and a chain, cobwebs, dim light",
         a="Emiliano breaks the rusty padlock with a hammer, the chain falls to the floor; Lupe, holding her breath, "
           "pushes the old wooden door open with a long creak.",
         dialogo=[("emiliano", "low, serious", "Doña Leonor mandó cerrar este cuarto hace dieciséis años.")]),
    dict(clip=6, personajes=["lupe", "emiliano"], objetos=["maleta"], escenario=_CARMEN,
         a="In the dusty room, Lupe kneels and pulls the old dusty suitcase from under the bed; she opens it: it is "
           "full of a woman's folded clothes; she touches them with trembling hands; Emiliano watches from the door.",
         dialogo=[("lupe", "voice breaking", "Su maleta… Está llena. Mi mamá nunca se la llevó."),
                  ("emiliano", "softly", "Nadie se va sin su ropa, Lupe.")]),
    dict(clip=7, personajes=["carmen"], objetos=["carta"], escenario=_CARMEN.replace(
             "closed for sixteen years: thick dust and cobwebs, a white sheet over a narrow bed",
             "sixteen years ago, clean and lived-in: a narrow bed with an embroidered blanket"),
         a="Flashback with warm soft faded tones, at night: Carmen, alone and frightened, writes the letter by candle "
           "light, hides it in a small wooden box, then freezes, hearing heavy footsteps outside the door.",
         dialogo=[("carmen", "a desperate whisper", "Perdóname, mija. Si me pasa algo, que él te diga la verdad.")]),
    dict(clip=8, personajes=["lupe", "chuy"], escenario=_CUARTO,
         a="Night, in Lupe's room the lamp suddenly goes out; the dark silhouette of a man in a cowboy hat appears "
           "behind the small window and knocks on the glass three times; Lupe pulls the blanket to her chest, terrified.",
         dialogo=[("chuy", "a rough menacing whisper through the glass",
                   "Lárgate del rancho… o vas a acabar como tu madre.")]),
    dict(clip=9, personajes=["lupe", "rodrigo"],
         escenario="a dark stone corridor of the hacienda at night, black mourning ribbons on the doors, moonlight",
         a="Lupe runs barefoot out into the dark corridor and crashes into Rodrigo, who is leaning against the wall with "
           "a glass of whisky; he smiles with contempt and blocks her way.",
         dialogo=[("rodrigo", "mocking, slow", "¿Asustada, heredera? Esta casa tiene sus fantasmas."),
                  ("lupe", "breathless but defiant", "Los fantasmas no golpean ventanas, Rodrigo.")]),
    dict(clip=10, personajes=["ibarra", "lupe"], objetos=["llave"], escenario=_ESTUDIO,
         a="Next morning in the study, the notary takes the big old iron key out of his leather folder and places it in "
           "Lupe's open hand; she closes her fingers around it.",
         dialogo=[("ibarra", "solemn, low", "Don Aurelio me pidió darle esto si usted decidía quedarse."),
                  ("lupe", "intrigued", "¿Qué abre, licenciado?"),
                  ("ibarra", "grave", "La capilla.")]),
    dict(clip=11, personajes=["lupe", "emiliano"], objetos=["llave", "linterna"], escenario=_CAPILLA,
         a="At night, Lupe opens the chapel door with the old iron key; she and Emiliano walk in with the lantern and "
           "stop in front of the plain stone tomb with no name; Emiliano crouches and wipes the dust off the stone.",
         dialogo=[("emiliano", "puzzled, low", "Esta tumba no tiene nombre."),
                  ("lupe", "horrified whisper", "Pero tiene la fecha… doce de octubre de dos mil diez. La noche que se "
                                                "fue mi mamá.")]),
    dict(clip=12, personajes=["leonor"], objetos=["linterna"], escenario=_CAPILLA,
         a="Behind them, at the chapel door, Doña Leonor appears holding her own lantern, her face half lit, perfectly "
           "calm and cold, her red nails on the door frame.",
         dialogo=[("leonor", "slow, icy", "Hay cosas que es mejor no desenterrar, Guadalupe.")]),
    dict(clip=13, personajes=["lupe", "leonor"], objetos=["linterna"], escenario=_CAPILLA,
         a="Lupe turns and faces Doña Leonor, tears in her eyes but standing firm; Leonor walks closer and leans to her "
           "ear; slow push-in on Lupe's face as she freezes in shock.",
         dialogo=[("lupe", "furious, voice trembling", "¿Qué le hizo a mi madre?"),
                  ("leonor", "a cold whisper", "Tu madre no está en esa tumba."),
                  ("lupe", "barely a breath", "¿Entonces quién?")]),
]

# Rótulos por código (énfasis, no subtítulos): título y el gancho al capítulo 3 (detalle en efectos.py).
ROTULOS = [
    dict(t=0.3, dur=2.6, texto="LA HEREDERA DEL RANCHO\nCapítulo 2"),
    dict(t=122.0, dur=4.0, texto="Capítulo 3:\n¿Quién está en la tumba?"),
]

LYRIA = dict(
    estilo="Mexican ranchera telenovela dramatic score: lush strings, solo piano, a melancholic requinto guitar and a "
           "soft distant trumpet, slow tempo 80 BPM, cinematic and melodramatic, mixed low under dialogue.",
    escenas={
        "gancho": ("A defiant string hit, then a proud tense motif.", 3),
        "secreto": ("Whispering suspense: low strings, a music-box piano motif and soft pizzicato.", 10),
        "cuarto": ("Mysterious dusty atmosphere, slow harp and cello, a sad flashback theme on requinto guitar.", 10),
        "susto": ("Horror-telenovela tension: string scrapes, deep heartbeat drum, a sudden scare sting.", 6),
        "capilla": ("Sacred and sinister: a soft organ drone, low choir, a slow tolling bell.", 4),
        "revelacion": ("Rising emotional strings and choir building to one huge final cliffhanger sting.", 9),
    },
    tramos=[(["gancho", "secreto", "cuarto", "susto", "capilla", "revelacion"],
             "Keep it as a bed under dialogue; end on the final sting.")],
)

MEZCLA = dict(musica=-25.0)   # cama bajo el diálogo; mezcla.py la agacha 12 dB cuando hablan (novela, 23-oct)
TRANSICIONES = [("corte", 0.0)] * 5
MUSICA = {"gancho": dict(sabor="tension"), "susto": dict(sabor="tension"), "revelacion": dict(sabor="tension")}

ESCENAS = [   # secciones musicales (SIN_VOZ): 42 compases = 126 s
    {"id": "gancho", "compases": 3, "frases": []},      # clip 1: «ya no soy tu sirvienta» (0-8)
    {"id": "secreto", "compases": 10, "frases": []},    # clips 2-4: Chela, el sobre, Valeria (8-36)
    {"id": "cuarto", "compases": 10, "frases": []},     # clips 5-7: candado, maleta, flashback de Carmen (36-66)
    {"id": "susto", "compases": 6, "frases": []},       # clips 8-9: la ventana, Rodrigo (66-84)
    {"id": "capilla", "compases": 4, "frases": []},     # clip 10: la llave (84-94)
    {"id": "revelacion", "compases": 9, "frases": []},  # clips 11-13: la tumba, Leonor, «¿entonces quién?» (94-126)
]
