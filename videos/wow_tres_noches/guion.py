# -*- coding: utf-8 -*-
"""Lo más PERTURBADOR que pasó DE VERDAD en World of Warcraft — especial de Halloween de Crónicas de Warcraft (~8 min, 16:9).
Narradora ÚNICA: el Ángel de la Resurrección (el espíritu del cementerio), que le habla al espectador de «tú». Tres noches reales,
de menos a más: un error (2005) → una plaga a propósito de Blizzard (2008) → la crueldad de los jugadores (2006). Giro final: tu
personaje también «murió» frente a ella y sigue en la pantalla de selección. Estilo «grabado de peste» dibujado por código
(docs/estilo_grabado_peste.md, kit nucleo/grabado.py; sesión 3) + clips reales yt-dlp SIEMPRE dentro de marcos grabados.
Voz ElevenLabs Lily (mujer, elegida por el usuario el 14-oct-2026) con eleven_v4 + corchetes. Sin subtítulos. Sin patrocinio.

Hechos (verificados el 14-oct-2026):
  SANGRE CORRUPTA (Wikipedia «Corrupted Blood incident» y su bibliografía):
  - 13-sep a 8-oct-2005. Zul'Gurub (banda de 20) se abrió el 13-sep; su jefe, Hakkar, lanzaba «Sangre Corrupta», que saltaba a los
    personajes cercanos; debía durar 10 s o hasta matar a Hakkar. Mataba a un nivel máximo en ≤ 30 s; a los bajos, casi al instante.
  - Las mascotas guardadas durante la pelea conservaban el efecto; al invocarlas en las capitales lo propagaron (Orgrimmar, Forjaz).
    Los PNJ se contagiaban pero no morían: portadores asintomáticos. Foros: «cientos» de cadáveres; un jugador: calles
    «literalmente blancas con los huesos de los muertos».
  - Solo los paladines podían quitarlo; los sanadores, al curar, mantenían vivos (y contagiosos) a los infectados. Hubo quien se
    contagiaba a propósito para ir a las multitudes («es divertido ver a la gente huir gritando»). Blizzard puso zonas de
    cuarentena con barreras y algunos las saltaron; otros avisaban en las entradas o se aislaron en zonas despobladas.
  - Hotfixes y reinicios no bastaron; a la semana, reinicios completos de los servidores; el 8-oct, parche: mascotas inmunes.
  - WoW tenía más de 4 millones de suscriptores. El CDC contactó a Blizzard para usar los datos (Blizzard: era un error, no había datos).
  - Lofgren y Fefferman (2007), «The untapped potential of virtual game worlds to shed light on real world epidemics», The Lancet
    Infectious Diseases 7(9):625-629, doi:10.1016/S1473-3099(07)70212-8 (Crossref ✔ 14-oct). Balicer (2007), «Modeling Infectious
    Diseases Dissemination Through Online Role-Playing Games», Epidemiology 18(2):260-261, doi:10.1097/01.ede.0000254692.80550.60
    (Crossref ✔ 14-oct).
  PLAGA ZOMBI (Engadget, «WoW Archivist: The zombie plague event», 5-nov-2014; warcraft.wiki.gg «Zombie Infestation»):
  - Empezó el 22-oct-2008 (fuentes: 22 o 23), antes de Wrath of the Lich King, A PROPÓSITO; a la vez que Halloween (Hallow's End).
  - Día 1: «cajas sospechosas» en Bahía del Botín; quien las revisaba se infectaba. Cuenta regresiva de 10 min → 5 (día 2) → 2 (día 3)
    → 1 (día 4); al llegar a cero o morir, zombi (necrófago). Día 2: cajas en todas las capitales + cucarachas apestadas.
  - Los zombis infectaban PNJ: vendedores de componentes (sin ellos no había portales para huir), subastadores, maestros de vuelo,
    maestros de batalla, guardias; pueblos como Villadorada y El Cruce, arrasados; las ciudades «cayeron una por una»; la economía se
    detuvo; la gente huyó al campo. Los zombis usaban los portales de Shattrath para ir a cualquier capital, incluso enemiga, y
    esperaban en los puntos de llegada (Torre de los Magos de Ventormenta). Muchos jugadores QUERÍAN ser zombis; otros se enfurecieron.
  - Día 6: el Alba Argenta encontró la cura. Propósito: que quisieras ver muerto al Rey Exánime.
  EL FUNERAL (Engadget «WoW Moviewatch: Serenity Now and the funeral», 8-dic-2008; JudgeHype; Servais 2015, UCLouvain):
  - 2006 (marzo/abril según la fuente), servidor JcJ Illidan (EE. UU.). Una jugadora (maga) sufrió un derrame cerebral y murió esa
    noche. Su hermandad anunció un memorial dentro del juego en las Fuentes termales de Cuna del Invierno, porque le gustaba pescar ahí.
  - La hermandad Serenity Now cayó sobre el memorial y mató a los dolientes, que por el impacto no se defendieron. Días después
    publicaron un video que lo celebraba (gameplay + correos furiosos + música); se volvió viral. Desde entonces los funerales se
    hacen en ciudades y zonas sin JcJ. Por respeto NO se dice el nombre del personaje de la jugadora.
"""

TITULO = "Lo más PERTURBADOR que pasó DE VERDAD en World of Warcraft"
ARCHIVO = "wow_tres_noches"
ESTILO_VISUAL = "documental"     # motion graphics dibujados propios; variante «grabado de peste» (docs/estilo_grabado_peste.md)
DURACION = None
BPM = 70
SUBTITULOS = False
GAP = 0.45
MEZCLA = dict(musica=-20.0, sfx=-24.0, fx=-17.0)
REVERB_VOZ = (0.22, 2.6, 5200.0)   # reverberación etérea del Ángel (mezcla, s, Hz); se añadió tras el render del tramo 4
# Narradora: el Ángel de la Resurrección (elegida por el usuario el 14-oct-2026 entre 6 muestras)
VOZ = dict(motor="elevenlabs", voice_id="pFZP5JQG7iQjIQuC4Bku", modelo="eleven_v4", idioma="es",
           referencia="C:/FabricaAnimaciones/videos/wow_tres_noches/voz/pruebas_voz/2_lily.mp3",
           tomas=1, stability=0.5)
# Nombres que Whisper escribe a su manera (CER alto sin error real de la voz)
CER_MAX_POR_FRASE = {"zulgurub_0": 0.12, "zulgurub_1": 0.12, "cdc_2": 0.15, "emboscada_0": 0.15, "funeral_1": 0.12,
                     "gancho_0": 0.05,                       # «Shhh.» → Whisper «¡Shh!» (solo ortografía)
                     "mascotas_1": 0.04, "ciudades_2": 0.04}  # «Forjaz» con la z de Lily → Whisper «Forjath» (2 semillas iguales)

# JUMPSCARES (los pidió el usuario): 4, uno por acto + el final. Cada uno va al CIERRE de su escena: el «post» de esa escena es el
# silencio (~1,2 s, todo se apaga) + el golpe de sonido + 6-8 cuadros sostenidos + 0,8 s para recuperar. SIN estrobo.
SUSTOS = {
    "humanos": "Hakkar: la cara del dios serpiente, grabada en rojo sangre, llena el cuadro de golpe",
    "portal": "un necrófago aparece pegado al borde del cuadro, a un palmo de la cámara (verde plaga)",
    "fila": "la emboscada: la carga de Serenity Now entra por la colina sobre la fila de dolientes (blanco helado)",
    "promesa": "primer plano del Ángel de la Resurrección: abre los ojos de golpe, mirando al espectador",
}

ESCENAS = [
    # ── GANCHO ─────────────────────────────────────────────────────────────────────────────────────────────────────────────
    {
        "id": "gancho", "pre": 1.6, "post": 0.6,
        "frases": [
            "[whispers] Shhh. [short pause] No te asustes. Ya nos conocemos.",
            "Cada vez que moriste en Azeroth, corriste como fantasma hasta un cementerio. [short pause] Y ahí estaba yo.",
            "[serious] Soy el Ángel de la Resurrección. He visto morir a millones de personajes. Por un mal salto, por un jefe, por una apuesta.",
            "Pero hay tres noches que no olvido. Tres noches que pasaron de verdad. [short pause] Y cada una fue peor que la anterior.",
            "[whispers] Quédate hasta la tercera. [short pause] Porque al final, te voy a contar cuándo moriste tú.",
        ],
    },
    # ── NOCHE 1: SANGRE CORRUPTA (2005) ────────────────────────────────────────────────────────────────────────────────────
    {
        "id": "zulgurub", "pre": 0.8, "post": 0.4,
        "frases": [
            "[thoughtful] La primera noche empezó el 13 de septiembre de 2005. Blizzard abrió una nueva banda en la selva: Zul'Gurub.",
            "Al fondo esperaba Hakkar, el Dios de la Sangre. [short pause] Y Hakkar tenía un hechizo llamado Sangre Corrupta.",
            "Una enfermedad que saltaba de un jugador a otro y le drenaba la vida. Pero solo debía durar unos segundos. Y solo dentro de esa sala.",
            "[sighs] Alguien olvidó un detalle. [short pause] Las mascotas.",
        ],
    },
    {
        "id": "mascotas", "pre": 0.3, "post": 0.4,
        "frases": [
            "Los cazadores guardaban a sus mascotas en plena pelea. Y una mascota guardada se guardaba con la enfermedad dentro.",
            "Al terminar, volvían a las capitales. Forjaz. Orgrimmar. [short pause] Y ahí, en medio de la gente, la llamaban.",
            "[whispers] Y la sangre salió con ella.",
        ],
    },
    {
        "id": "ciudades", "pre": 0.3, "post": 0.4,
        "frases": [
            "Un personaje de nivel máximo aguantaba unos segundos. [short pause] Uno de nivel bajo caía casi al instante.",
            "Los personajes del juego también se contagiaban, pero no morían. Eran portadores. Te vendían una espada y te pasaban la muerte.",
            "Pronto, en las calles de Forjaz había cientos de cadáveres. Un jugador escribió que el suelo estaba blanco de huesos.",
            "[sad] Y todos esos fantasmas corrieron hacia mí. Los resucitaba, volvían a la ciudad… [short pause] y volvían a morir.",
        ],
    },
    {
        "id": "humanos", "pre": 0.3, "post": 2.8,
        "frases": [
            "[thoughtful] Lo más extraño vino después. Los jugadores empezaron a comportarse como en una epidemia de verdad.",
            "Unos huyeron a los bosques, solos. Otros se quedaron en las puertas de las ciudades, avisando a los que llegaban.",
            "Los sanadores intentaban salvarlos a todos. [short pause] Y sin querer, mantenían vivos a los contagiosos.",
            "Blizzard puso cuarentenas. [short pause] Los jugadores las saltaron.",
            "Y hubo otros. [whispers] Los que se contagiaban a propósito y corrían hacia la multitud, solo para verla huir gritando.",
            "[whispers] Hakkar nunca salió de su templo. [short pause] No le hizo falta.",
        ],
    },
    {
        "id": "cdc", "pre": 0.4, "post": 0.6,
        "frases": [
            "Una semana después, Blizzard reinició todos los servidores. Como quien quema la aldea entera para detener la peste.",
            "[curious] Pero la historia no terminó ahí. Los Centros para el Control de Enfermedades de Estados Unidos le escribieron a Blizzard. Querían los datos.",
            "Y en 2007, dos epidemiólogos lo publicaron en The Lancet Infectious Diseases.",
            "Habían visto algo que ningún modelo capturaba: [short pause] cómo se comporta la gente de verdad cuando llega una epidemia.",
            "[whispers] Quince años después, el mundo entero conoció las cuarentenas. [short pause] Azeroth ya las había ensayado.",
        ],
    },
    # ── NOCHE 2: LA PLAGA ZOMBI (2008) ─────────────────────────────────────────────────────────────────────────────────────
    {
        "id": "cajas", "pre": 0.8, "post": 0.4,
        "frases": [
            "[sighs] La segunda noche fue distinta. Porque esta vez nadie se equivocó. [short pause] Esta vez, Blizzard lo hizo a propósito.",
            "Octubre de 2008. Faltaban semanas para que llegara el Rey Exánime. Hace 18 años, en estas mismas noches de Halloween.",
            "En los muelles de Bahía del Botín aparecieron unas cajas. Cajas sospechosas, sin dueño.",
            "[short pause] Y claro, los jugadores las abrieron.",
        ],
    },
    {
        "id": "reloj", "pre": 0.3, "post": 0.4,
        "frases": [
            "Quien las tocaba recibía una enfermedad con cuenta regresiva. Diez minutos. [short pause] Si el reloj llegaba a cero, o si morías…",
            "[whispers] te levantabas como necrófago. Un muerto viviente que obedecía a la Plaga. [short pause] Y que mordía.",
            "Al día siguiente, las cajas aparecieron en todas las capitales. El reloj bajó a cinco minutos. Luego a dos. [short pause] Luego a uno.",
        ],
    },
    {
        "id": "caen", "pre": 0.3, "post": 0.4,
        "frases": [
            "[nervous] Y los necrófagos no solo mordían jugadores. Mordían a los vendedores. A los subastadores. A los maestros de vuelo. A los guardias.",
            "Cada personaje del juego que caía se levantaba como uno de ellos. Y las ciudades fueron cayendo, una por una.",
            "No podías vender. No podías volar. No podías comprar con qué escapar. [short pause] La economía de Azeroth se detuvo.",
            "Los vivos huyeron al campo. [short pause] Pero en Villadorada y en El Cruce, los muertos ya los estaban esperando.",
        ],
    },
    {
        "id": "portal", "pre": 0.3, "post": 2.8,
        "frases": [
            "[thoughtful] Y entonces pasó lo que nadie esperaba. Muchos jugadores… [short pause] querían ser zombis.",
            "Se infectaban a propósito. Se organizaban en hordas, y usaban los portales para invadir las capitales enemigas.",
            "Se escondían justo donde aparecen los viajeros, en la torre de los magos de Ventormenta.",
            "[whispers] Cruzabas el portal… [short pause] y ya te estaban esperando.",
        ],
    },
    {
        "id": "cura", "pre": 0.4, "post": 0.6,
        "frases": [
            "Otros lo odiaron. Llevaban días sin poder jugar, y escribían furiosos a Blizzard.",
            "Seis días después, el Alba Argenta encontró una cura. Y la plaga se apagó.",
            "[serious] Blizzard consiguió lo que buscaba: que odiaras al Rey Exánime antes de conocerlo.",
            "[whispers] Pero yo aprendí otra cosa. Si les das una plaga… [short pause] muchos eligen ser la plaga.",
        ],
    },
    # ── NOCHE 3: EL FUNERAL (2006) ─────────────────────────────────────────────────────────────────────────────────────────
    {
        "id": "funeral", "pre": 0.8, "post": 0.4,
        "frases": [
            "[sad] La tercera noche es la que menos me gusta contar. Pasó antes que la segunda. [short pause] Pero la guardé para el final.",
            "2006. Servidor Illidan. Una jugadora sufrió un derrame cerebral. Murió esa misma noche. [short pause] En la vida real.",
            "Sus compañeros de hermandad decidieron despedirla donde la conocieron: dentro del juego.",
            "Eligieron unas aguas termales en Cuna del Invierno. [short pause] Ahí le gustaba pescar.",
            "Lo anunciaron en los foros del servidor, para que cualquiera pudiera venir a despedirse. [short pause] Cualquiera.",
        ],
    },
    {
        "id": "fila", "pre": 0.3, "post": 2.8,
        "frases": [
            "[thoughtful] Llegaron muchos. Se formaron en una fila larga junto al agua, en silencio.",
            "Illidan era un servidor de jugador contra jugador. Ahí, fuera de las ciudades, cualquiera te puede atacar.",
            "Pero nadie ataca un funeral. [short pause] [whispers] ¿Verdad?",
        ],
    },
    {
        "id": "emboscada", "pre": 0.3, "post": 0.4,
        "frases": [
            "Bajaron por la colina. Una hermandad entera, con armas y hechizos. Se llamaba Serenity Now.",
            "[serious] Y los mataron. A todos. Los dolientes estaban tan impactados que casi nadie se defendió.",
            "[sad] Esa noche llegaron a mi cementerio, uno detrás de otro. [short pause] Venían de un funeral.",
        ],
    },
    {
        "id": "video", "pre": 0.3, "post": 0.6,
        "frases": [
            "Días después, los atacantes subieron el video a internet. Con música, y con los correos furiosos de los amigos de ella.",
            "Se convirtió en uno de los videos más famosos de World of Warcraft.",
            "[thoughtful] Desde entonces, los funerales de Azeroth se hacen en las ciudades. Donde nadie puede atacarte.",
        ],
    },
    # ── EL GIRO ────────────────────────────────────────────────────────────────────────────────────────────────────────────
    {
        "id": "promesa", "pre": 0.6, "post": 2.6,
        "frases": [
            "[sighs] Un error. Una plaga a propósito. Y un funeral. [short pause] Lo más peligroso de Azeroth nunca fue un dios. Fueron ustedes.",
            "Ahora, lo prometido. [short pause] Te dije que te contaría cuándo moriste tú.",
            "[whispers] No fue un jefe. Fue el día en que cerraste el juego y no volviste.",
            "Tu personaje sigue ahí. En la pantalla de selección. Con la ropa que le pusiste, mirando a la nada.",
            "[short pause] No sabe que te fuiste. [whispers] Sigue esperando.",
        ],
    },
    {
        "id": "cierre", "pre": 0.3, "post": 3.0,
        "frases": [
            "[whispers] ¿Hace cuánto que no lo visitas?",
        ],
    },
]

TRANSICIONES = [("continua", 0.5)] * (len(ESCENAS) - 1)   # plano secuencia: los cambios de escena los dibuja escenas.py

LYRIA = dict(
    estilo="Dark medieval plague horror underscore: low choir hums, detuned hurdy-gurdy, slow funeral drum, bowed bells, "
           "dissonant cello clusters, distant wind and chains, sparse and patient, instrumental only, no vocals, no lyrics.",
    escenas={
        "gancho": ("near silence, a single cold bell, a soft wordless choir breath, an intimate whisper of dread", 2),
        "zulgurub": ("jungle ritual dread: low tribal frame drum heartbeat, hollow wooden flutes, crimson tension", 4),
        "mascotas": ("the heartbeat speeds up slightly, a sick wavering cello, something carried where it should not be", 5),
        "ciudades": ("plague spreading through a stone city: tolling bells, rising dissonant strings, mournful and huge", 7),
        "humanos": ("uneasy and human, thinning texture, nervous plucked strings, ends in sudden total silence", 6),
        "cdc": ("cold clinical calm after the storm, sustained low pad, ticking clock, sad and reflective", 3),
        "cajas": ("sickly green unease: creaking wood, low bassoon, a carnival-like music box slightly out of tune", 4),
        "reloj": ("a relentless ticking pulse, tension rising in steps, deep brass swells, a countdown feeling", 6),
        "caen": ("full undead assault: pounding war drums, dissonant choir, chaos and collapse of a city", 8),
        "portal": ("dark playful menace, ghoulish pizzicato, then thinning to a held note and sudden silence", 6),
        "cura": ("relief that is not relief: a hollow major chord turning minor, a lonely bell", 3),
        "funeral": ("a tender sorrowful lament: solo cello and soft choir, frozen winter air, deep grief", 3),
        "fila": ("very quiet, still and reverent, a held choir chord over silence, fragile", 2),
        "emboscada": ("brutal violent stabs of low strings and drums, then broken mournful remains", 8),
        "video": ("bitter aftermath, slow cello, distant cold wind, the grief lingers", 3),
        "promesa": ("intimate and eerie, a fragile music box and a cold choir breath, slowly closing in", 4),
        "cierre": ("a final whispered chord, then nothing, cold silence", 2),
    },
    tramos=[                                     # tiempos del 14-oct: 134 s · 86 s · 158 s · 153 s (Lyria da ~3 min por pieza)
        (["gancho", "zulgurub", "mascotas", "ciudades"],
         "Begin from near silence. Build slowly and steadily to a large mournful peak, end still rising."),
        (["humanos", "cdc"],
         "Begin tense and nervous, cut to dead silence for three seconds near the middle, then end on a cold sad pad."),
        (["cajas", "reloj", "caen", "portal", "cura"],
         "Begin quiet and sickly. Rise in steps to a chaotic peak, a sudden silence, then a hollow ending on a lonely bell."),
        (["funeral", "fila", "emboscada", "video", "promesa", "cierre"],
         "Begin with a tender lament. Fall to near silence, a brutal violent burst, a grieving aftermath, end in cold silence."),
    ],
)
