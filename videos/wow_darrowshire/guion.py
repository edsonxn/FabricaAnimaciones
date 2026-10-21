# -*- coding: utf-8 -*-
"""La niña que sigue esperando (Villa Darrow / Darrowshire) — Crónicas de Warcraft, 16:9, 12+ min, lore OSCURO.

Pedido del usuario (20-oct-2026): FORMATO NUEVO para Warcraft = el del asteroide (`videos/asteroide_invisible/`: Flow pinta escenarios
y hojas, el código los anima como pegatinas, docs/estilo_pegatina_flow.md) + pegatinas REALES de Warcraft + clips de YouTube si hace
falta + SFX DEL PROPIO JUEGO + Lyria de terror. Historia de lore oscura y poco contada (Stalvan descartado: ya salió en el canal).
CTA del formato a la mitad y al final («si te gusta este estilo, comparte y comenta para seguir»). Voz ElevenLabs Lily (la de
wow_tres_noches, elegida por el usuario el 20-oct). 12 min MÍNIMO. Sin Overgear (campaña en pausa).

Lore y fuentes (warcraft.wiki.gg + textos de misión de Wowhead Classic; nombres en español de la API de tooltips de Wowhead, es-ES):
  - Villa Darrow (Darrowshire): pueblo humilde de las colinas del sur de Lordaeron, nombrado por el lago Darrowmere (Anales de Villa
    Darrow, libro de la misión 5154). Batalla de Villa Darrow en la Tercera Guerra; aislado de la Alianza; defensores = tropas de
    Lordaeron, paladines de la Mano de Plata y milicia del capitán Joseph Rutagrana (Redpath).
  - 1.ª oleada (esqueletos, cadáveres) rechazada; 2.ª = necrófagos campeones de Horgus el Devastador; refuerzos de paladines con Davil
    (Anales: «Crokford», nativo del pueblo; en el juego Davil Fuegoluz / Lightfire). Davil mata a Horgus y muere de su herida.
    Marduk el Negro (caballero de la muerte) arranca el alma de Joseph y la retuerce en sombra = Rutagrana el Corrompido, que contagia
    a los defensores: atacan a sus aliados y matan a los vecinos escondidos en sus casas. Población entera muerta. La Plaga se va con
    la cabeza de Horgus; la sombra siembra el mal hasta caer en una granja de las Tierras de la Peste del Oeste (Gahrron), donde queda
    su escudo junto a un granero, al que acuden los esbirros. Los caídos = necrófagos con el espíritu atrapado; los fantasmas
    recrean la batalla.
  - Familia: hijas Jessica (mayor, huyó de Lordaeron antes de la Plaga; sobrevive, Vista Eterna) y Pamela; hermana Marlene (fantasma,
    casa al sur de las ruinas de Andorhal; «escondí a mi sobrina Pamela»); hermano Carlin (vivo, Alba Argenta, Capilla de la
    Esperanza de la Luz). Culling of Stratholme (WotLK): la familia viva en una posada del camino a Stratholme, 2.º piso; Pamela
    juega con muñecas, Joseph duerme.
  - Misiones Classic (ID): La pequeña Pamela 5142 · La muñeca de Pamela 5149 (3 piezas; al acercarte sale un «Fantasma del pasado»;
    «Mi padre es el hombre más valiente del mundo… llevo aquí mucho tiempo y no ha venido por mí»; «Mantendrás alejada a la gente
    mala, ¿verdad?»; chisme «I never feel warm anymore…») · Tía Marlene 5152 · Un extraño historiador 5153 (alianza de Joseph bajo su
    monumento en el cementerio de Andorhal; su fantasma: «Save me…»; Cromi en la posada en ruinas de Andorhal: «You're not from the
    future, are you?», «too late for him now… perhaps we can help him in the past») · Los Anales de Villa Darrow 5154 (ayuntamiento
    de Andorhal, libros que invocan Guardianes decrépitos) · Carlin, el hermano de Joseph 5210 · Los villanos 5181 (cráneo de Horgus
    en un lago con fantasmas; espada destrozada de Marduk) · Los héroes 5168 (Tratado de Davil en Vega del Amparo / Cruzada
    Escarlata; escudo de Rutagrana) · Los defensores 5211 (liberar 15 espíritus) · Los merodeadores 5206 · Vuelve con Cromi 5941 ·
    La Batalla de Villa Darrow 5721 (Fardo de reliquias; gritos: «Darrowshire, to arms! The Scourge approach!», «Do not lose hope…»,
    «The Light burns bright in you, Davil…», «Defenders of Darrowshire! Rally!…», «Redpath! Your life ends, here and now!»,
    «Darrowshire! You are doomed!», «The Scourge are defeated! Darrowshire is saved!»; perdón de Joseph; la corrupción NO se puede
    impedir) · Tesoros ocultos 5942 (Pamela: «¡La batalla ha terminado! Mi papá me lo susurró», té con azúcar, la llave del cofre).
  - Cadena Classic quitada en el parche 4.0.3a (Cataclysm la rehízo); sigue en Classic y en WoW Forever (sale el 4-nov-2026).
  - NO se afirma: fechas exactas, cómo murió Marlene, nombre de la granja en español.
"""

TITULO = "La niña que sigue esperando a su padre en World of Warcraft"
ARCHIVO = "wow_darrowshire"
ESTILO_VISUAL = "pegatina_flow"      # formato nuevo: pegatinas de Flow (FICHA) + pegatinas reales de WoW + MG por código
DURACION = None
BPM = 66
GAP = 0.45
# ElevenLabs con corchetes de actuación (docs/voz.md). Escritura normal: cifras, nombres bien escritos, sin fonética.
# Lily (biblioteca pública), la narradora de wow_tres_noches; el usuario la pidió el 20-oct-2026.
VOZ = dict(motor="elevenlabs", voice_id="pFZP5JQG7iQjIQuC4Bku", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/wow_tres_noches/voz/pruebas_voz/2_lily.mp3",
           tomas=1, stability=0.5)
MEZCLA = dict(musica=-20.0, sfx=-23.0)
SUBTITULOS = False
ALIAS_QA = {   # lo que escribe Whisper con la voz de Lily -> grafía del guion (minúsculas, sin tildes)
    "villadarro": "villa darrow", "viladarro": "villa darrow", "villadaro": "villa darrow", "viladaro": "villa darrow",
    "vilabarro": "villa darrow", "villa barro": "villa darrow", "villa darro": "villa darrow",
    "josef": "joseph", "josep": "joseph", "jorgos": "horgus", "lordoran": "lordaeron", "darumir": "darrowmere",
    "ruta verana": "rutagrana",
    "orgus": "horgus", "cromie": "cromi", "chromie": "cromi", "villa barrow": "villa darrow", "villavarro": "villa darrow",
}
# «encuentres su muñeca»: las dos eses se funden al hablar y Whisper escribe «encuentre su» (1 letra)
CER_MAX_POR_FRASE = {"pamela_8": 0.02}
MUSICA = {}

ESCENAS = [
    {"id": "gancho", "pre": 1.0, "frases": [
        "[whispers] En las Cavernas del Tiempo hay una posada, en el camino a Stratholme.",
        "En el segundo piso, una niña juega con sus muñecas. [short pause] Su padre duerme en la cama de al lado.",
        "Se llaman Pamela y Joseph Rutagrana. [short pause] Y ninguno de los dos sabe lo que viene.",
        "Porque si cruzas las Tierras de la Peste del Este y bajas a las ruinas de un pueblo llamado Villa Darrow, la vas a volver a encontrar.",
        "[whispers] Más pálida. Más fría. [short pause] Y todavía esperando.",
        "[softly] «Hola. Soy Pamela. ¿Cómo te llamas?»",
        "Esta es una de las historias más tristes de World of Warcraft. [short pause] Y está escondida en un pueblo en ruinas que casi todos cruzan de largo.",
    ]},
    {"id": "pueblo", "frases": [
        "Villa Darrow era un pueblo humilde en las colinas del sur de Lordaeron, junto al lago Darrowmere, del que tomó su nombre.",
        "Durante siglos, ahí no pasó nada que valiera la pena escribir en un libro de historia.",
        "Ahí vivía la familia Rutagrana. Joseph, el padre, era capitán y dirigía la milicia del pueblo.",
        "Tenía dos hijas: Jessica, la mayor, y Pamela, la pequeña, que nunca soltaba su muñeca.",
        "Con ellos estaban la tía Marlene y el tío Carlin, el hermano de Joseph.",
        "[sighs] Era el tipo de familia que en un juego ni siquiera notarías. [short pause] Y por eso duele tanto lo que les pasó.",
    ]},
    {"id": "plaga", "frases": [
        "Entonces llegó la Plaga. [short pause] Primero, escondida en el grano que salía de los graneros de Andorhal hacia todo el reino.",
        "Los que comían ese grano enfermaban. Morían. [whispers] Y después se levantaban.",
        "Stratholme cayó. Andorhal cayó. Y la Plaga se extendió por Lordaeron como una mancha de tinta.",
        "Villa Darrow quedó aislada. Los ejércitos de la Alianza estaban demasiado lejos para llegar a tiempo.",
        "Así que el pueblo hizo lo único que podía hacer. [short pause] Quedarse a pelear.",
    ]},
    {"id": "asedio", "frases": [
        "Soldados de Lordaeron, paladines de la Mano de Plata y la milicia del capitán Rutagrana levantaron barricadas en las calles.",
        "Los primeros ataques fueron pequeños: esqueletos y cadáveres que bajaban tambaleándose desde las afueras.",
        "Y los defensores los hicieron retroceder. [short pause] Una vez. Y otra. Y otra más.",
        "Por un tiempo, Villa Darrow creyó que podía resistir.",
        "Antes de salir a pelear, Joseph dejó a Pamela con su tía Marlene.",
        "Y Marlene hizo lo que cualquiera habría hecho. [whispers] La escondió en casa, y le pidió que no saliera, pasara lo que pasara.",
    ]},
    {"id": "horgus", "frases": [
        "Entonces bajó de las colinas la segunda oleada.",
        "[serious] Ya no eran esqueletos. Eran necrófagos campeones, rápidos y hambrientos, al mando de un señor de los necrófagos: Horgus el Devastador.",
        "La línea de defensa empezó a romperse.",
        "Y justo cuando todo parecía perdido, llegaron refuerzos: paladines de la Mano de Plata, guiados por Davil Fuegoluz, un hijo del propio pueblo.",
        "[shouting] «¡No pierdan la esperanza, Villa Darrow! ¡No vamos a caer!»",
        "Horgus lo buscó en medio de la batalla. [whispers] «La Luz arde con fuerza en ti, Davil. Voy a disfrutar apagándola.»",
        "Pelearon durante mucho tiempo. [short pause] Y Davil lo mató.",
        "[sighs] Pero la herida que Horgus le dejó también lo mató a él, poco después.",
    ]},
    {"id": "marduk", "post": 1.2, "frases": [
        "Ahora el mando era del capitán Joseph Rutagrana. [short pause] Y según los Anales de Villa Darrow, Joseph pudo haber ganado.",
        "Pero entonces apareció un caballero de la muerte. [short pause] Marduk el Negro.",
        "[serious] «¡Rutagrana! Tu vida termina aquí y ahora.»",
        "Marduk no lo mató como a un soldado más. [short pause] Le arrancó el alma del cuerpo.",
        "Y la retorció hasta convertirla en una sombra. [whispers] Rutagrana el Corrompido.",
        "Y la sombra de Joseph empezó a contagiar a sus propios hombres.",
        "Los defensores de Villa Darrow se dieron la vuelta. Atacaron a sus compañeros. [long pause] Y después entraron en las casas.",
        "Las casas donde se escondían los vecinos. [short pause] Las casas donde se escondían los niños.",
        "[sighs] En Villa Darrow no sobrevivió nadie.",
    ]},
    {"id": "cta_mitad", "frases": [
        "Antes de seguir, una cosa. Este es un formato nuevo en el canal: lore de Warcraft contado como un cuento animado.",
        "Si te está gustando este estilo, compártelo y déjame un comentario. [short pause] Así sé si seguimos con más historias así.",
        "Y créeme, Azeroth tiene muchas. Unas muy oscuras. [short pause] Y otras, no tanto.",
        "[whispers] Ahora, volvamos con Pamela.",
    ]},
    {"id": "despues", "frases": [
        "Cuando ya no quedó nadie vivo, la Plaga se fue. [short pause] Se llevó la cabeza de Horgus. Y la sombra de Joseph.",
        "Rutagrana el Corrompido sembró el mal por todo Lordaeron, hasta que la Alianza por fin lo derribó en una granja apestada, al este de Andorhal.",
        "Su escudo quedó tirado junto a un granero. [whispers] Y los no-muertos todavía se acercan a él, como si algo los llamara.",
        "Los defensores caídos se levantaron como necrófagos. [short pause] Con sus espíritus atrapados dentro de esos cuerpos podridos.",
        "Y a veces, los fantasmas del pueblo vuelven a pelear la misma batalla. [whispers] Una y otra vez.",
        "Villa Darrow se quedó en silencio. [long pause] Bueno. Casi.",
    ]},
    {"id": "pamela", "frases": [
        "Años después, los aventureros que cruzan las Tierras de la Peste encuentran una casa abandonada al sur de las ruinas de Andorhal.",
        "Adentro hay un fantasma. [short pause] Es Marlene.",
        "[sad] «Murieron tantos en la batalla de Villa Darrow. Tantos murieron… [short pause] y algo peor.»",
        "«Cuando empezó la batalla, escondí a mi sobrina Pamela. [short pause] Y no sé qué fue de ella.»",
        "Así que vas a Villa Darrow. Y entre las casas quemadas hay una niña. [short pause] Transparente.",
        "[softly] «Hola. Soy Pamela. ¿Cómo te llamas?»",
        "Te cuenta que su papá es el hombre más valiente del mundo. Que la tía Marlene le dijo que se quedara en casa mientras él iba a pelear.",
        "[whispers] «Pero llevo aquí mucho tiempo. Y no ha venido por mí.»",
        "Y te pide un favor. [short pause] Que le encuentres su muñeca. La dejó en el pueblo.",
    ]},
    {"id": "muneca", "frases": [
        "La muñeca está rota en tres pedazos: la cabeza, el lado izquierdo y el lado derecho, repartidos entre las ruinas.",
        "Y cada vez que te acercas a uno, aparece un Fantasma del pasado. [short pause] Alguien que también murió ahí y nunca se fue.",
        "Cuando por fin se la devuelves, Pamela grita de alegría. [excited] «¡La encontraste! ¡Encontraste mi muñeca!»",
        "Y después te pregunta, muy bajito: [whispers] «Vas a mantener lejos a la gente mala, ¿verdad?»",
        "Si le vuelves a hablar, solo te dice una cosa. [long pause] [whispers] «Ya nunca siento calor.»",
    ]},
    {"id": "anillo", "frases": [
        "Pamela te manda de vuelta con su tía. Y Marlene por fin te cuenta la verdad.",
        "Joseph no murió como un héroe. [short pause] Su alma fue retorcida por la Plaga, y se convirtió en un monstruo.",
        "Su cuerpo fue destruido hace años. Lo único que queda de él es su alianza de bodas, bajo su monumento, en el cementerio de Andorhal.",
        "Vas al cementerio. Buscas su tumba entre las demás. Y sacas el anillo.",
        "Por un segundo, aparece el fantasma de Joseph. [long pause] [whispers] «Sálvame.»",
        "[short pause] Y desaparece.",
    ]},
    {"id": "cromi", "frases": [
        "Marlene te manda con una historiadora muy extraña, escondida en la posada en ruinas de Andorhal.",
        "Tiene forma de gnomo. [short pause] Pero en realidad es Cromi, un dragón de bronce, una guardiana del tiempo.",
        "Lo primero que te pregunta es: [curious] «No vienes del futuro, ¿verdad?»",
        "Mira el anillo y lo entiende todo. Joseph fue un gran hombre, con un pasado trágico.",
        "[serious] «Para él ya es demasiado tarde. [short pause] Pero quizá podamos ayudarlo en el pasado.»",
    ]},
    {"id": "reliquias", "frases": [
        "Su plan es una locura: reunir los restos de aquella batalla para que los fantasmas la vuelvan a pelear. [short pause] Y esta vez, cambiar el final.",
        "Primero, los Anales de Villa Darrow, en el ayuntamiento de Andorhal, entre libros malditos que despiertan a guardianes decrépitos.",
        "Cromi escribe notas en los márgenes y te manda con Carlin, el hermano de Joseph, que sigue vivo en la Capilla de la Esperanza de la Luz.",
        "Carlin te pide los restos de los villanos: el cráneo de Horgus, en un lago donde los fantasmas todavía pelean, y la espada rota de Marduk.",
        "Y los de los héroes: el tratado de Davil, en manos de la Cruzada Escarlata, y el escudo de Joseph, junto a aquel granero.",
        "[sighs] Y después viene la parte más cruel. Tienes que liberar a 15 espíritus de Villa Darrow.",
        "¿Y sabes cómo se liberan? [short pause] Matando a los necrófagos en los que se convirtieron sus defensores.",
    ]},
    {"id": "batalla", "frases": [
        "Con todo reunido, Cromi te da un fardo de reliquias y te manda a la plaza de Villa Darrow.",
        "Lo dejas en el suelo. [short pause] Y los muertos se levantan a pelear otra vez.",
        "[shouting] «¡Villa Darrow, a las armas! ¡Ya viene la Plaga!»",
        "Ahora tú estás en la batalla. Tienes que mantener vivo a Davil hasta que caiga Horgus. Y proteger al capitán Joseph.",
        "[shouting] «¡Defensores de Villa Darrow! ¡Reagrúpense! ¡Tenemos que ganar!»",
        "Y entonces vuelve a aparecer Marduk. [short pause] Y aquí está lo más terrible de toda la historia.",
        "No puedes impedir que lo corrompa. [short pause] Eso ya pasó. Y lo que ya pasó, tiene que volver a pasar.",
        "Lo único que puedes hacer es acabar con Joseph rápido, antes de que contagie a sus hombres. [whispers] Antes de que entren en las casas.",
        "[shouting] «¡Villa Darrow! ¡Estás condenada!», grita la sombra. [short pause] Y tú la derribas.",
        "Y de la sombra sale el espíritu de Joseph, limpio por primera vez en muchos años. [short pause] Y te pide perdón.",
        "«¡La Plaga ha sido derrotada! ¡Villa Darrow se ha salvado!»",
        "[long pause] [sighs] Pero lo grita un fantasma, en un pueblo donde ya no vive nadie.",
    ]},
    {"id": "te", "frases": [
        "Vuelves a la casa de Pamela.",
        "[nervous] «Oí fantasmas allá afuera», te dice. «Me susurraban cosas que daban miedo.»",
        "Y de repente sonríe. [excited] «¡La batalla terminó! Mi papá me lo susurró. Dice que espantó a los fantasmas y que ya viene a casa.»",
        "Te cuenta que preparó té. Té con azúcar. [short pause] Para cuando él llegue.",
        "Y entonces llega. El fantasma de Joseph aparece junto a la casa, y la llama por su nombre.",
        "Pamela corre hacia él. [short pause] «¡Papi! ¡Volviste!»",
        "[softly] «Te extrañé tanto, mi niña. [short pause] Por fin estoy en casa.»",
        "Antes de que te vayas, Pamela te da una llave. Su papá le dijo que abre un cofre detrás de la casa. [short pause] Es su forma de darte las gracias.",
    ]},
    {"id": "cierre", "post": 3.0, "frases": [
        "Y así termina la historia. [long pause] O eso queremos creer.",
        "Porque nada de eso cambió el pasado. Villa Darrow sigue en ruinas. Su gente sigue muerta.",
        "De toda la familia Rutagrana solo sobrevivieron dos: Carlin, y Jessica, la hermana mayor, que se fue de Lordaeron antes de que llegara la Plaga.",
        "Joseph y Pamela solo pudieron reencontrarse como lo que ya eran. [short pause] Dos fantasmas.",
        "[serious] Y hay un detalle que lo vuelve todavía más oscuro.",
        "Con Cataclysm, esta cadena de misiones se borró del juego moderno y se rehízo distinta. Pero la original sigue en Classic. [short pause] Y en WoW Forever.",
        "Así que cuando WoW Forever salga, el 4 de noviembre, ella va a estar ahí. En la misma casa. Con la misma muñeca rota.",
        "Esperando al próximo aventurero, como si fuera el primero.",
        "[whispers] «Hola. Soy Pamela. ¿Cómo te llamas?»",
        "[long pause] Si esta historia te dejó algo, compártela, y cuéntame en los comentarios qué otra historia de Azeroth quieres ver con este estilo.",
        "Te leo ahí abajo. [short pause] Y Pamela, [whispers] también te está esperando.",
    ]},
]

# PARCIAL (20-oct-2026): el saldo de ElevenLabs solo alcanzó para la voz de gancho…marduk (0:00-4:40). Mientras falte el resto,
# el video llega hasta PARCIAL_HASTA (tiempo, Lyria, SFX, mezcla y la vista previa de 0-3:00). Al recargar: PARCIAL_HASTA = None,
# `voz` → `seleccionar` → `tiempo` (las 6 primeras escenas conservan sus tiempos) → Lyria de los tramos que faltan.
PARCIAL_HASTA = None   # 20-oct: con la cuenta 2 de respaldo ya alcanza para toda la voz
if PARCIAL_HASTA:
    ESCENAS = ESCENAS[:[e["id"] for e in ESCENAS].index(PARCIAL_HASTA) + 1]

TRANSICIONES = [("continua", 0.5)] * (len(ESCENAS) - 1)

# Lyria 3.5 por API (0,08 US$ por pieza). Un tramo > 175 s se rechaza: repartir tras `tiempo` (provisional).
LYRIA = dict(
    estilo=("Dark fantasy horror score for an animated World of Warcraft lore story about a ghost girl waiting for her father in a "
            "ruined village of the Plaguelands: a fragile, slightly out-of-tune music box lullaby as the main motif, low cello and "
            "contrabass drones, distant wordless choir, cold plague wind, slow tolling bells, sparse harp and celesta; medieval, "
            "mournful and haunted; long silences, melodies kept low so a narrator can speak over it. No drum kit, no pop, no sung words."),
    escenas={
        "gancho": ("a lone, slightly detuned music box lullaby in a quiet candle-lit room; a cold low drone slowly creeps in under it", 3),
        "pueblo": ("warm, gentle and pastoral: harp, soft strings and the lullaby in a major key, a peaceful village by a lake; "
                   "near the end a single low note darkens it", 3),
        "plaga": ("the warmth drains away: low cello drones, slow tolling bells, creeping dissonant strings like a spreading stain", 5),
        "asedio": ("tense resolve: low pulsing strings and distant war drums, a brave modal theme that rises, then a hushed, "
                   "fragile ending with the lullaby half-remembered", 6),
        "horgus": ("desperate battle in slow motion: dark choir, pounding low drums far away, heroic brass that breaks", 8),
        "marduk": ("horror: icy choir clusters, a heartbeat drum, then everything collapses into a hollow, ringing silence", 9),
        "cta_mitad": ("a calm, warm storyteller's pause by candlelight: soft harp and low strings, gentle and inviting", 2),
        "despues": ("aftermath: cold wind over ashes, a slow funeral cello, distant ghostly choir echoing a battle far away", 5),
        "pamela": ("haunted and tender: the music box lullaby returns slower and detuned, glassy celesta, a ghost child's loneliness", 4),
        "muneca": ("eerie searching among ruins: whispering strings, faint chimes; a fragile burst of joy, then a chilling cold hush", 5),
        "anillo": ("graveyard dread: low drones, a slow tolling bell, a sudden icy sting at a ghost's whispered plea, then emptiness", 6),
        "cromi": ("mysterious and curious: ticking clockwork textures, shimmering bronze bells and harp arpeggios, time magic", 4),
        "reliquias": ("a purposeful dark quest march: low strings ostinato, distant drums, building determination with dread", 6),
        "batalla": ("a ghostly battle replayed: choir, war drums and tolling bells, tragic heroic brass at the peak, then a hollow "
                    "ringing aftermath", 9),
        "te": ("bittersweet reunion: the music box lullaby, tender and warm for a moment, soft strings swell gently", 4),
        "cierre": ("melancholic and haunting epilogue: the lullaby alone, slower, fading into cold wind and silence", 3),
    },
    tramos=[
        (["gancho", "pueblo"],
         "Begin with a lone music box lullaby in an empty room. Warm but fragile; end on the first cold, dissonant drone."),
        (["plaga", "asedio"],
         "Begin from a cold drone. Creeping plague dread with distant bells; a fragile hope rises, then falls; end held and uneasy."),
        (["horgus", "marduk"],
         "Begin from a tense low pulse. Desperate medieval battle in slow motion, choir and war drums far away; a dark climax; end in sudden silence."),
        (["cta_mitad", "despues", "pamela"],
         "Begin very soft and calm, almost silent. Desolate ruins and wind; the music box returns, broken and slower; end lingering."),
        (["muneca", "anillo", "cromi"],
         "Begin with eerie whispers of strings. Ghostly searching; a chilling sting at a whispered plea; then mysterious and curious; end suspended."),
        (["reliquias", "batalla"],
         "Begin with a purposeful dark march. Builds into a ghostly battle with choir and bells; tragic peak; end on a hollow, ringing aftermath."),
        (["te", "cierre"],
         "Begin with the music box lullaby, tender and bittersweet. A reunion that warms for a moment, then turns cold and haunting; end with the lullaby fading alone."),
    ],
)

if PARCIAL_HASTA:   # solo los tramos cuyas escenas ya tienen voz (los demás se piden al quitar PARCIAL_HASTA)
    _ids = {e["id"] for e in ESCENAS}
    LYRIA["tramos"] = [tr for tr in LYRIA["tramos"] if set(tr[0]) <= _ids]

# Ficha común de Flow (todas las láminas empiezan con ella): cuento oscuro pintado a mano con proporciones de Warcraft,
# para recortar y animar como pegatinas; Lordaeron apestado, frío, con UN acento cálido de vela.
FICHA = dict(
    estilo=("Hand-painted 2D cut-out animation art for a dark fairy-tale retelling of World of Warcraft lore: stylized Warcraft "
            "proportions (chunky silhouettes, big hands and shoulders, oversized armor), hand-painted textures with visible brush "
            "strokes and paper grain, clean dark ink outlines; gothic HORROR mood in plague-blighted Lordaeron: ashen greys, sickly "
            "plague green and cold moonlight blue palette with a single warm candle-orange accent, long shadows, drifting fog, "
            "eerie atmosphere, strong depth"),
    cierre=" No text, no letters, no numbers, no watermark, no logos.",
)
