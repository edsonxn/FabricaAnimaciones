# -*- coding: utf-8 -*-
"""LogIA presenta · «LLAMADA DE DOMINGO» — episodio de antología de ciencia ficción de futuro próximo (~15 min, 16:9).
Idea del usuario (6-nov-2026): una empresa crea una app con la que los hijos se clonan para hablar con sus papás y hacerlos
sentir bien; casi ningún papá se da cuenta, algunos sí. Formato de CAPÍTULO DE SERIE: personajes con personalidad y voz
propia, sin narrador. Estilo elegido por Claude (el noir B/N de LogIA no le funciona al público): DRAMA DE ANTOLOGÍA REALISTA
= clips de Flow con diálogo actuado y lipsync (personajes de Flow con voz fija, receta de docs/formato_novela_ia.md
«NOVELA, NO TRÁILER») + interfaz de la app PRESENTE, presentación de la empresa, noticiero y anuncios dibujados por código
(ui.py, voces de ElevenLabs para los personajes que nunca se ven de cerca: la directora, la asistente, el locutor).

BIBLIA
- PRESENTE (empresa mexicana, directora Valeria Roca): «Tres horas de entrevista, tus fotos, audios y chats, y tu Presente
  llama por ti, con tu cara y tu voz». «Modo discreto»: el familiar nunca recibe aviso (Ley de Compañía Digital). El 94 % de los
  padres nunca lo nota. Los RESÚMENES que recibe el cliente están optimizados para que EL CLIENTE esté tranquilo (la trampa).
- Don Ramón Ortega (71), relojero jubilado en Guadalajara, viudo; su canario Paco dejó de cantar cuando murió su esposa.
  Arregla el reloj de bolsillo del abuelo para el nieto que viene. Le dice «Chato» a su hijo. NUNCA se da cuenta.
- Daniel Ortega (37), director en una startup de la CDMX, esposa Inés embarazada. No llegó a la muerte de su mamá (culpa).
  Contrata PRESENTE en modo discreto; después mete también a su hermana.
- Lucía Ortega (42), enfermera en Guadalajara, la hija que SÍ va cada domingo y a la que su papá no ve.
- Doña Carmen (69), vecina de dominó: SÍ se da cuenta (el perro que nunca tuvieron) y elige que la sigan engañando.
- Don Chuy (74), el compadre del dominó: feliz con su hija-app, nunca lo sabe.
- Mariana (38), hija de Carmen, solo aparece como su Presente en videollamada.
- FINAL: Ramón muere en el hospital esperando al hijo que su Presente le prometió («Ya voy, papá. Aguántame»); el resumen le
  dijo a Daniel «revisión de rutina». Al llegar en Navidad se entera por Lucía. Le llama «Papá»: PRESENTE Legado, armado con
  las propias llamadas. «¿Perdonarte de qué, Chato? Si tú nunca faltaste». Epílogo: seis meses después Daniel desliza la
  notificación como al principio; las dos voces artificiales siguen platicando cada domingo.

Tipos de beat (`tipo` en PLANOS): "clip" = video de Flow con diálogo · "llamada" = video de Flow del Presente hablando a la
cámara (ui.py le pone la interfaz de videollamada) · "img" = imagen de Flow con cámara lenta · "ui" = pieza por código (ui.py).
"""

TITULO = "Llamada de domingo"
ARCHIVO = "llamada_de_domingo"
MOTOR = "secuencia"
FORMATO = "horizontal"
ESTILO_VISUAL = "secuencia_flow"
SIN_VOZ = True          # sin narrador: el diálogo vive en el audio de cada clip (y en el de cada pieza de ui.py)
SUBTITULOS = False
BPM = 60                # 1 compás = 4 s

# ───────────────────────────── fichas (palabra por palabra en cada prompt) ─────────────────────────────
FICHA = dict(
    estilo="Cinematic 16:9 frame from a prestige near-future anthology TV drama, photorealistic live action, anamorphic "
           "40mm lens look, shallow depth of field, muted cool teal-grey color grade with soft natural light, Mexico a few "
           "years in the future with sleek discreet technology, natural skin texture, subtle film grain, restrained "
           "naturalistic acting",
    personajes={
        "ramon": "a 71-year-old Mexican man with brown weathered skin, thick white hair combed back, a neat white "
                 "mustache, reading glasses hanging on a cord around his neck, a beige knitted cardigan over a light-blue "
                 "checked shirt",
        "daniel": "a 37-year-old Mexican man with light-brown skin, short black hair with a fade, a short trimmed black "
                  "beard, tired eyes, a slim navy suit with a white shirt and no tie",
        "lucia": "a 42-year-old Mexican woman with brown skin, shoulder-length wavy black hair with a few grey strands "
                 "tied in a low ponytail, no makeup, tired kind eyes, teal nurse scrubs under an open grey cardigan",
        "ines": "a 34-year-old Mexican woman with fair olive skin, long straight dark-brown hair, seven months pregnant, "
                "an oversized beige knit sweater",
        "carmen": "a 69-year-old Mexican woman with short permed grey hair, round gold-rimmed glasses, a lilac blouse "
                  "under a cream cardigan, a small gold medal necklace",
        "chuy": "a 74-year-old stout Mexican man, bald with a white horseshoe of hair, a thick grey-and-black mustache, a "
                "white guayabera shirt",
        "mariana": "a 38-year-old Mexican woman with fair skin, a sleek chestnut bob haircut, small pearl earrings, a "
                   "white silk blouse",
    },
    nombres={"ramon": "Don Ramón", "daniel": "Daniel", "lucia": "Lucía", "ines": "Inés", "carmen": "Doña Carmen",
             "chuy": "Don Chuy", "mariana": "Mariana"},
    objetos={
        "reloj": "The pocket watch is an old gold pocket watch with an open engraved lid",
        "canario": "The birdcage is a small white wire birdcage with a yellow canary inside",
        "telefono": "The phone is a thin frameless glass smartphone",
    },
    epoca="Guadalajara and Mexico City, Mexico, a few years in the future",
    cierre="No on-screen text, no subtitles, no captions, no logos, no watermark. Only the spoken lines written here, "
           "natural Mexican Spanish accent, no background music.",
)

# Escenarios (una imagen de Flow por lugar = ingrediente de todos los clips de ese lugar)
ESC = dict(
    taller="Don Ramón's small watch-repair workshop in an old house in Guadalajara on a Sunday morning: a wooden "
           "workbench with tiny tools, a magnifying lamp and open watch movements, dozens of antique wall clocks ticking "
           "on a green wall, a white wire birdcage with a yellow canary by the window, an old wooden radio on a shelf, "
           "a framed photo of a smiling older woman, warm tungsten light mixed with soft daylight",
    oficina="a sleek glass-walled startup office on a high floor in Mexico City at night: the city lights through "
            "floor-to-ceiling windows, a long white table with laptops, a whiteboard full of graphs, cold blue LED light",
    depto="a modern minimalist apartment in Mexico City at night: grey sofa, a big TV on the wall, a laptop on the coffee "
          "table, rain on the window, dim cold light from the screens, a framed photo of an older couple on a shelf",
    plaza="a small shaded plaza in a Guadalajara neighborhood on a Sunday afternoon: a folding table with dominoes under "
          "big laurel trees, a white kiosk, colorful old houses, dappled warm sunlight",
    cocina="Doña Carmen's small old kitchen at night: a single hanging lamp over a table with an embroidered tablecloth, "
           "a sugar bowl, a clay jar, a round wall clock, saint pictures, dark window",
    porche="the porch of Doña Carmen's colorful old house at dusk: potted geraniums, a metal rocking chair, a warm porch "
           "light",
    auto_lucia="inside an old small hatchback car parked on a Guadalajara street in the evening: dashboard, a hospital "
               "badge hanging from the mirror, streetlights through the windshield",
    taxi="the back seat of a taxi at night in Mexico City: passing city lights and rain on the window",
    pasillo="a hospital corridor at night in Guadalajara: pale green walls, fluorescent lights, a stretcher, a nurses' "
            "station",
    hospital="a public hospital room at night in Guadalajara: a single bed, a heart monitor, an oxygen tube, a curtain, "
             "a window with the dark city",
    carretera="inside a modern car driving on a highway to Guadalajara at sunset in December: the golden light, an "
              "infant car seat in the back",
    puerta="the front door of Don Ramón's watch-repair shop in Guadalajara at dusk in December: the metal shutter half "
           "down, a black mourning bow on the door, dry flowers on the step, neighbors' Christmas lights",
    taller_perfecto="an idealized spotless version of an old watch-repair workshop: every antique clock perfectly "
                    "aligned on a green wall, a tidy wooden workbench, soft golden perfect light, no dust at all, slightly "
                    "too perfect, like a catalog",
    puerta_dia="the front door of Don Ramón's watch-repair shop in an old Guadalajara street on a sunny Sunday: a painted "
               "sign, the metal shutter open, potted plants",
    hospital_ext="the facade of a big public hospital in Guadalajara at night: an emergency entrance sign glowing red, "
                 "an ambulance, wet asphalt",
    perfecto="an immaculate bright minimalist living room in soft perfect daylight: a white sofa, a green plant, white "
             "walls, everything clean and slightly too perfect, like a catalog",
)
_MISMA = ("Continuing the same conversation from the previous shot, same moment, same lighting, same clothes, the "
          "characters stay exactly where they were.")
_LLAMADA = ("Framed as the front camera of a video call: medium close-up, the person looks straight into the lens and "
            "talks to the viewer as if to a loved one, perfectly lit, a warm flawless smile, eyes slightly too steady.")


def C(d, quien, esc, a, dialogo, objetos=(), **kw):
    """Clip de Flow con diálogo (d = 8 o 10 s)."""
    return dict(tipo="clip", d=d, personajes=list(quien), escenario=ESC[esc], esc=esc, a=a, dialogo=list(dialogo),
                objetos=list(objetos), **kw)


def L(d, quien, a, dialogo, esc="perfecto"):
    """El Presente (clon) hablando a la cámara en videollamada: ui.py le pone la interfaz."""
    return dict(tipo="llamada", d=d, personajes=[quien], escenario=ESC[esc], esc=esc, a=f"{_LLAMADA} {a}",
                dialogo=list(dialogo), objetos=[])


def I(d, img, a, quien=(), esc=None):
    """Imagen de Flow con movimiento lento de cámara."""
    return dict(tipo="img", d=d, img=img, a=a, personajes=list(quien), esc=esc)


def U(d, ui, a):
    """Pieza dibujada por código (ui.py)."""
    return dict(tipo="ui", d=d, ui=ui, a=a)


PLANOS = [
    # ═══════════ APERTURA (0:00) — el domingo perfecto, y quién lo hace en realidad ═══════════
    I(5, "ext_relojeria", "Fachada de la relojería un domingo por la mañana."),
    C(8, ["ramon"], "taller",
      "Don Ramón sits at his workbench with a jeweler's loupe in one eye, working on the open pocket watch; the clocks "
      "tick; the phone on the bench lights up and buzzes; he lifts the loupe and grins like a child.",
      [("ramon", "delighted, to himself", "¡Ándale! Ya sabía yo que no me ibas a fallar.")], ["reloj", "telefono"]),
    C(10, ["ramon"], "taller",
      f"{_MISMA} Medium close-up: Don Ramón holds the phone up in front of his face for a video call, beaming, and shows "
      "the open gold pocket watch to the camera.",
      [("ramon", "warm, teasing", "¿Qué pasó, Chato? Pensé que hoy no ibas a poder. Mira, te estoy arreglando el reloj "
                                  "del abuelo. Para el niño.")], ["reloj", "telefono"]),
    L(8, "daniel", "Daniel, freshly shaved and groomed, wearing a soft cream knit sweater instead of a suit, smiles warmly.",
      [("daniel", "warm, loving", "¿Cómo no, papá? Es domingo. ¿Y esa rodilla?")]),
    C(10, ["ramon"], "taller",
      f"{_MISMA} Don Ramón rubs his knee and laughs, then his smile fades as he looks at the silent yellow canary in its "
      "cage by the window.",
      [("ramon", "laughing, then softer and sad", "Terca, como yo. Oye, el Paco ya no canta. Desde que se fue tu mamá, "
                                                  "ya no canta.")], ["canario", "telefono"]),
    L(10, "daniel", "Daniel, in the soft cream knit sweater, tilts his head tenderly.",
      [("daniel", "gentle, reassuring", "Ponle la estación de boleros, la que ponía mamá en las mañanas. Vas a ver que "
                                        "canta.")]),
    I(6, "ramon_radio", "Ramón gira la perilla del radio viejo mirando la jaula del canario.", ["ramon"], "taller"),
    C(8, ["daniel"], "oficina",
      "Night. Daniel, exhausted, tie-less, sits at the long table in a meeting; his phone vibrates face up on the table; "
      "he glances at it without picking it up, flips it face down and speaks to a colleague off-screen.",
      [("daniel", "tired, impatient", "No, sigue, sigue. ¿Cómo vamos con los inversionistas?")], ["telefono"]),
    U(7, "notif_1", "Notificación: llamada con Papá completada, ánimo 92 %, resumen; la desliza sin leer."),
    U(9, "titulo", "LogIA presenta · LLAMADA DE DOMINGO."),

    # ═══════════ ACTO 1 (1:21) — PRESENTE ═══════════
    I(5, "ext_auditorio", "Auditorio moderno en la CDMX de noche: el lanzamiento de PRESENTE."),
    U(56, "keynote_1", "Valeria Roca presenta PRESENTE en el escenario (voz ElevenLabs, diapositivas por código)."),
    U(30, "anuncio", "Anuncio de PRESENTE en la tele del departamento de Daniel."),
    C(10, ["ines", "daniel"], "depto",
      "Inés sits on the grey sofa with a hand on her pregnant belly, the TV glowing; Daniel works on the laptop at the "
      "other end of the sofa without looking up. She speaks first, he answers without lifting his eyes.",
      [("ines", "tired, a little sad", "¿Otra vez no le llamaste a tu papá?"),
       ("daniel", "distracted", "Le llamo el domingo.")]),
    C(8, ["ines", "daniel"], "depto",
      f"{_MISMA} Close-up of Inés looking at him; then a silent reverse shot of Daniel stopping typing, guilty.",
      [("ines", "quiet, disappointed", "Eso dijiste hace tres domingos, Dani.")]),
    U(10, "onboard_1", "La app en la laptop: «Vamos a conocer a tu papá». ¿Cómo te dice cuando está contento?"),
    C(8, ["daniel"], "depto",
      "Late night, Inés is gone. Close-up of Daniel lit by the laptop screen; he smiles despite himself.",
      [("daniel", "softly amused", "Chato. Me dice Chato.")]),
    U(5, "onboard_2", "¿Y cuando está enojado?"),
    C(8, ["daniel"], "depto",
      f"{_MISMA} Daniel laughs quietly and shakes his head, lit by the laptop.",
      [("daniel", "laughing quietly", "Daniel Alejandro Ortega. Completo.")]),
    U(7, "onboard_3", "Última pregunta: ¿qué es lo que más le duele a tu papá?"),
    C(10, ["daniel"], "depto",
      f"{_MISMA} Daniel's smile fades; a long silence; he looks at the framed photo of his parents on the shelf, then "
      "answers very quietly, his eyes wet.",
      [("daniel", "very quiet, ashamed", "Que mi mamá se murió… y yo no llegué.")]),
    U(16, "onboard_4", "Entrevista completada; se arma su cara; «Modo discreto» y el dedo que lo activa."),
    I(5, "daniel_laptop", "Daniel iluminado por la laptop; Inés dormida al fondo.", ["daniel", "ines"], "depto"),

    # ═══════════ ACTO 2 (4:21) — EL MILAGRO ═══════════
    U(4, "carta_4meses", "CUATRO MESES DESPUÉS."),
    U(40, "montaje", "Montaje: Ramón feliz con el teléfono día tras día; el contador de llamadas sube."),
    I(4, "plaza", "La plaza del dominó.", (), "plaza"),
    C(10, ["chuy", "carmen", "ramon"], "plaza",
      "Fixed blocking: Don Chuy on the LEFT, Doña Carmen in the CENTER, Don Ramón on the RIGHT, around the dominoes table. "
      "Don Chuy slams a domino tile on the table, proud and loud; Doña Carmen nods.",
      [("chuy", "loud, proud", "¡Mi hija me habla diario, compadre! ¡Diario! Antes ni en mi cumpleaños.")]),
    C(8, ["carmen", "chuy", "ramon"], "plaza",
      f"{_MISMA} Fixed blocking: Don Chuy on the LEFT, Doña Carmen in the CENTER, Don Ramón on the RIGHT. Doña Carmen "
      "smiles, proud, adjusting her glasses.",
      [("carmen", "proud, sweet", "La mía también. Hasta se acuerda de mis pastillas.")]),
    C(10, ["ramon", "chuy", "carmen"], "plaza",
      f"{_MISMA} Fixed blocking: Don Chuy on the LEFT, Doña Carmen in the CENTER, Don Ramón on the RIGHT. Don Ramón places a "
      "tile with a flourish, beaming; the others laugh.",
      [("ramon", "beaming, proud", "El Chato me cuenta todo. Como si viviera aquí a la vuelta.")]),
    I(5, "carmen_duda", "Carmen mira su teléfono; la sonrisa se le va un poco.", ["carmen"], "plaza"),
    I(4, "lucia_llega", "Lucía llega con bolsas del súper y un pastillero.", ["lucia"], "puerta_dia"),
    C(10, ["lucia", "ramon"], "taller",
      "Lucía, in her nurse scrubs, comes into the workshop holding grocery bags and a weekly pill organizer; Don Ramón, on a "
      "video call, covers the phone with his hand and answers without looking at her.",
      [("lucia", "cheerful, tired", "Papá, te traje tus pastillas de la semana."),
       ("ramon", "distracted, happy", "Ahorita, mija. Estoy con tu hermano.")], ["telefono"]),
    C(8, ["lucia", "ramon"], "taller",
      f"{_MISMA} Close-up of Lucía putting the bags down slowly, hurt.",
      [("lucia", "hurt, quiet", "Yo vengo cada domingo, papá. Cada domingo.")]),
    C(10, ["ramon", "lucia"], "taller",
      f"{_MISMA} Don Ramón answers kindly, without malice, smiling at the phone; then a silent close-up of Lucía swallowing "
      "her tears.",
      [("ramon", "kind, oblivious", "Ya sé, mija. Pero tu hermano sí me escucha.")], ["telefono"]),
    C(10, ["lucia"], "auto_lucia",
      "Evening. Lucía sits in her parked car with the phone at her ear, annoyed, rubbing her forehead.",
      [("lucia", "annoyed, suspicious", "¿Desde cuándo le hablas diario a papá?")], ["telefono"]),
    C(10, ["daniel"], "oficina",
      "Daniel walks in the glass office with the phone at his ear, confused; he stops, looks at the screen, then puts it "
      "back to his ear.",
      [("daniel", "confused, then covering", "¿Diario? … Ah. Sí. Sí, le hablo.")], ["telefono"]),
    U(7, "dashboard", "El tablero de PRESENTE: 121 llamadas con Papá, ánimo 94 %."),
    C(10, ["lucia"], "auto_lucia",
      f"{_MISMA} Lucía softens, leaning her head back on the seat, smiling sadly.",
      [("lucia", "softer, sincere", "Qué bueno, Dani. Te extraña mucho. Vente en Navidad, ¿sí?")], ["telefono"]),
    C(8, ["daniel"], "oficina",
      f"{_MISMA} Daniel looks at the city through the glass, guilty, the phone at his ear.",
      [("daniel", "hesitant", "Sí… Sí voy.")], ["telefono"]),

    # ═══════════ ACTO 3 (6:55) — LA QUE SE DIO CUENTA ═══════════
    I(4, "cocina", "La cocina de Carmen de noche.", (), "cocina"),
    C(10, ["carmen"], "cocina",
      "Doña Carmen sits at her kitchen table on a video call, the phone propped against the sugar bowl; she speaks sweetly "
      "but her eyes are watchful, testing.",
      [("carmen", "sweet, testing", "Mija, ¿te acuerdas del perro que teníamos en Tepic? El Firulais.")], ["telefono"]),
    L(10, "mariana", "Mariana laughs, delighted, nodding.",
      [("mariana", "delighted, warm", "¡Ay, el Firulais! ¡Cómo no, mamá! Si dormía conmigo.")]),
    C(8, ["carmen"], "cocina",
      f"{_MISMA} Very slow push-in on Doña Carmen's face as it freezes; she takes off her glasses.",
      [("carmen", "barely a breath", "Nunca tuvimos perro, Mariana.")], ["telefono"]),
    L(8, "mariana", "Mariana keeps exactly the same warm smile, unbothered.",
      [("mariana", "smooth, sweet", "Ay, mamá, qué cosas dices. ¿Ya te tomaste tu pastilla?")]),
    I(5, "carmen_sola", "Carmen sola, el teléfono boca abajo, el reloj de la pared.", ["carmen"], "cocina"),
    C(10, ["carmen", "ramon"], "plaza",
      "Next morning, the plaza is empty; Doña Carmen sits next to Don Ramón on a park bench and talks low, holding his arm.",
      [("carmen", "low, urgent", "Ramón, no son ellos. Es una aplicación. Mi hija ya me lo confesó.")]),
    C(8, ["ramon", "carmen"], "plaza",
      f"{_MISMA} Don Ramón laughs it off, patting her hand.",
      [("ramon", "amused, dismissive", "Ay, Carmen. El Chato se acuerda de todo.")]),
    C(10, ["carmen", "ramon"], "plaza",
      f"{_MISMA} Doña Carmen looks him in the eye; Don Ramón's smile slowly disappears.",
      [("carmen", "serious, gentle", "¿Y ya le preguntaste algo que no le haya contado a nadie?")]),
    C(10, ["carmen"], "porche",
      "Dusk. Doña Carmen in her rocking chair on the porch, the phone at her ear; she listens, closes her eyes, and answers "
      "with a sad, tender resignation.",
      [("carmen", "tender, resigned", "No, mija. No lo canceles. Que me siga hablando.")], ["telefono"]),
    I(5, "ramon_duda", "Ramón de noche en el taller, con el teléfono en la mano, dudando.", ["ramon"], "taller"),
    C(8, ["ramon"], "taller",
      "Night, only the magnifying lamp is on. Don Ramón on a video call, serious for the first time, looking into the phone.",
      [("ramon", "serious, slow", "Chato… ¿dónde estabas tú cuando se murió tu mamá?")], ["telefono"]),
    L(10, "daniel", "Daniel, in the soft cream knit sweater, lowers his eyes for a second, then looks back into the lens "
                    "with perfect sorrow.",
      [("daniel", "sorrowful, sincere", "En el aeropuerto, papá. No alcancé el vuelo. Y nunca te pedí perdón.")]),
    C(8, ["ramon"], "taller",
      f"{_MISMA} Don Ramón's eyes fill with tears; relieved, he nods slowly.",
      [("ramon", "moved, relieved", "Ya, mijo. Ya pasó.")], ["telefono"]),

    # ═══════════ ACTO 4 (8:58) — EL ALGORITMO ═══════════
    U(18, "noticiero", "Noticiero: 40 millones de usuarios y la Ley de Compañía Digital."),
    C(10, ["lucia"], "pasillo",
      "Lucía, in her nurse scrubs, walks fast down the hospital corridor with the phone at her ear, furious.",
      [("lucia", "furious", "¡Es una aplicación, Daniel! Carmen me contó todo. ¡Papá habla con un robot!")], ["telefono"]),
    C(10, ["daniel"], "taxi",
      "Daniel in the back of a taxi at night, phone at his ear, defensive, the city lights passing over his face.",
      [("daniel", "defensive, tired", "¿Y qué querías? ¿Que no le hablara nadie? Está feliz, Lucía.")], ["telefono"]),
    C(8, ["lucia"], "pasillo",
      f"{_MISMA} Lucía stops in the corridor, closes her eyes, and says it quietly before hanging up.",
      [("lucia", "quiet, crushing", "Está feliz con alguien que no existe.")], ["telefono"]),
    U(10, "agregar_lucia", "Daniel agrega a Lucía a PRESENTE en modo discreto."),
    I(4, "ext_hospital", "Hospital público de Guadalajara de noche.", (), "hospital_ext"),
    C(10, ["ramon"], "hospital",
      "Night. Don Ramón lies in the hospital bed in a gown with an oxygen tube; weak, he holds the phone above his face on "
      "a video call.",
      [("ramon", "weak, hopeful", "Chato… estoy en el hospital. Me duele el pecho. ¿Vienes?")], ["telefono"]),
    L(8, "daniel", "Daniel, in the soft cream knit sweater, worried and tender.",
      [("daniel", "tender, urgent", "Ya voy, papá. Aguántame. Tomo el primer vuelo.")]),
    C(8, ["ramon"], "hospital",
      f"{_MISMA} Don Ramón lowers the phone to his chest and smiles with relief, looking at a nurse off-screen.",
      [("ramon", "weak, happy", "Ya viene mi hijo.")]),
    U(10, "notif_rutina", "Daniel en una fiesta de oficina: «Papá tuvo una revisión médica de rutina. Todo en orden»."),
    I(6, "cama_vacia", "La cama vacía al amanecer; el reloj de Ramón detenido en el buró.", (), "hospital"),
    U(8, "notif_lucia", "«Llamada de Lucía atendida por tu Presente. Lucía está alterada: dale espacio»."),

    # ═══════════ ACTO 5 (10:46) — NAVIDAD ═══════════
    U(4, "carta_3semanas", "TRES SEMANAS DESPUÉS."),
    C(10, ["daniel", "ines"], "carretera",
      "Daniel drives, happy for the first time, wearing a dark jacket; Inés, no longer pregnant, sits in the back next to a "
      "newborn baby in the infant car seat and smiles at him in the mirror.",
      [("daniel", "excited", "Va a ser la sorpresa de su vida. Ni le dije que veníamos.")]),
    I(5, "puerta", "La relojería al anochecer: cortina a medio bajar, moño negro, flores secas.", (), "puerta"),
    C(10, ["lucia", "daniel"], "puerta",
      "Lucía, dressed in black, opens the shop door; cardboard boxes behind her; Daniel stands outside holding the baby "
      "carrier, smiling uncertainly. She speaks first; he answers.",
      [("lucia", "cold, tired", "¿Ahora sí vienes?"),
       ("daniel", "confused, smiling", "¿Dónde está papá?")]),
    C(10, ["lucia", "daniel"], "puerta",
      f"{_MISMA} Close-up of Lucía, dressed in black, eyes red, very calm.",
      [("lucia", "calm, devastating", "Lo enterramos hace tres semanas. Te hablé, Daniel. Me dijiste que no alcanzabas "
                                      "vuelo.")]),
    C(8, ["daniel", "lucia"], "puerta",
      f"{_MISMA} Daniel goes pale; he shakes his head and pulls the phone out of his pocket with trembling hands.",
      [("daniel", "stunned, stammering", "Yo nunca… Yo no…")], ["telefono"]),
    U(14, "historial", "El historial de la app: la llamada del hospital y la de Lucía, palabra por palabra."),
    C(10, ["lucia", "daniel"], "puerta",
      f"{_MISMA} Lucía, dressed in black, speaks without anger, tears running down; Daniel in soft focus with the phone.",
      [("lucia", "broken, quiet", "Te estuvo esperando toda la noche. Le decía a la enfermera: ya viene mi hijo, ya "
                                  "viene.")]),
    I(5, "daniel_roto", "La cara de Daniel se desmorona.", ["daniel"], "puerta"),
    U(6, "timbre_papa", "Suena el teléfono: «Papá». PRESENTE Legado, 30 días gratis."),
    L(10, "ramon", "Don Ramón, freshly groomed, in a spotless cardigan, in a perfect bright version of his workshop, smiles "
                   "with joy.",
      [("ramon", "joyful", "¡Chato! ¿Ya llegaste? Te tengo chilaquiles.")], esc="taller_perfecto"),
    C(8, ["daniel"], "puerta",
      "Close-up of Daniel holding the phone to his face, crying, barely able to speak.",
      [("daniel", "crying", "Papá… perdóname.")], ["telefono"]),
    L(10, "ramon", "Don Ramón tilts his head with infinite tenderness.",
      [("ramon", "tender", "¿Perdonarte de qué, Chato? Si tú nunca faltaste.")], esc="taller_perfecto"),
    C(8, ["lucia", "daniel"], "puerta",
      "Lucía, dressed in black, looks at her brother talking to the phone, disgusted and heartbroken; she takes her coat and "
      "walks away down the street.",
      [("lucia", "disgusted, heartbroken", "Eso no es mi papá.")]),
    I(6, "reloj_grabado", "El reloj de bolsillo en el banco de trabajo, grabado: «Para el que viene».", (), "taller"),
    C(10, ["daniel"], "taller",
      "Night. Daniel sits alone at his father's workbench, the baby carrier beside him and the phone face up on the bench; "
      "he turns the knob of the old wooden radio; a soft bolero plays, and the yellow canary starts to sing. Daniel cries in "
      "silence. Nobody speaks.", [], ["canario", "telefono", "reloj"]),

    # ═══════════ EPÍLOGO (13:23) ═══════════
    U(4, "carta_6meses", "SEIS MESES DESPUÉS."),
    U(12, "notif_final", "Daniel en su oficina de día: «Ánimo de Papá 97 %. Tu ánimo 91 %». Sonríe apenas y desliza."),
    U(26, "keynote_2", "Valeria Roca presenta PRESENTE Legado: 312 millones de usuarios."),
    U(22, "final", "Dos teléfonos sobre el banco a oscuras siguen platicando; créditos de LogIA."),
]

SECUENCIA = dict(
    clips_s=[p["d"] for p in PLANOS],
    video_calidad="360p",
    combinar=False,
    dialogo=True,       # los clips hablan; la voz nunca se acelera
    fundido=0.0,        # cortes secos, como serie
    ambiente=1.0,       # el audio del clip ES el diálogo
    ambiente_por={},
    carpeta_descargas="flow-llamada_domingo",
)

ESCENAS = [   # secciones musicales (SIN_VOZ); 1 compás = 4 s
    {"id": "apertura", "compases": 20, "frases": []},
    {"id": "acto1", "compases": 43, "frases": []},
    {"id": "acto2", "compases": 38, "frases": []},
    {"id": "acto3", "compases": 31, "frases": []},
    {"id": "acto4", "compases": 27, "frases": []},
    {"id": "acto5", "compases": 35, "frases": []},
    {"id": "epilogo", "compases": 16, "frases": []},
]
TRANSICIONES = [("corte", 0.0)] * (len(ESCENAS) - 1)
MUSICA = {}
MEZCLA = dict(musica=-25.0)

# Música por momentos (6-nov-2026, sesión 2): Lyria adaptada a cada acto; casi muda bajo la plática (MEZCLA duck + curva)
LYRIA = dict(
    estilo="Intimate prestige TV drama score: sparse felt piano, soft string quartet, a faint warm analog synth pad, subtle "
           "ticking clock-like pulse, melancholic and tender, restrained, cinematic, no vocals, no drums",
    escenas={
        "apertura": ("tender warm Sunday morning, gentle piano motif with a ticking pulse, a hint of unease at the end", 3),
        "acto1": ("sleek cold tech-launch glow, then intimate late-night loneliness, soft synth arpeggio over piano", 4),
        "acto2": ("bittersweet warmth, gentle hopeful montage that slowly turns sad, cello enters", 4),
        "acto3": ("quiet suspense and doubt, sustained strings, sparse piano notes, a sad tender resignation", 3),
        "acto4": ("cold news-like pulse, growing dread, low strings and heartbeat-like pulse, devastating hush at the end", 5),
        "acto5": ("grief, a slow broken piano theme, strings swell at the reveal, then fragile silence", 6),
        "epilogo": ("cold perfect corporate calm with an uncanny edge, the piano motif returns distant and hollow, fade to silence", 4),
    },
    tramos=[(["apertura"], "Begin softly. End on a held unresolved chord."),
            (["acto1"], "Begin with a cold synth shimmer. End quiet and lonely."),
            (["acto2"], "Begin warm. End sad and quiet."),
            (["acto3"], "Begin in near silence. End on a soft held note."),
            (["acto4"], "Begin with a low pulse. End in a sudden hush."),
            (["acto5"], "Begin with solo piano. End in fragile silence."),
            (["epilogo"], "Begin hollow and calm. Fade out completely to silence.")],
)
